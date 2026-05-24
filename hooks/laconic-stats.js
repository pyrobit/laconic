#!/usr/bin/env node
// laconic — /laconic-stats hook
// Reads the current session JSONL, computes output token savings, returns
// decision: block so the model never processes this command.

const fs = require('fs');
const path = require('path');
const os = require('os');
const {
  COMPRESSION_RATIOS,
  DEFAULT_MODE,
  MODEL_PRICING,
  getFlagPath,
  readFlag,
} = require('./laconic-config');

function getCwdSlug() {
  return process.cwd().replace(/[/_]/g, '-');
}

function findSessionFile(claudeDir) {
  const slug = getCwdSlug();
  const projectDir = path.join(claudeDir, 'projects', slug);
  let files;
  try {
    files = fs.readdirSync(projectDir)
      .filter(f => f.endsWith('.jsonl'))
      .map(f => {
        const p = path.join(projectDir, f);
        return { p, mtime: fs.statSync(p).mtimeMs };
      })
      .sort((a, b) => b.mtime - a.mtime);
  } catch (e) {
    return null;
  }
  return files.length ? files[0].p : null;
}

function parseSession(filePath) {
  let lines;
  try {
    lines = fs.readFileSync(filePath, 'utf8').split('\n').filter(Boolean);
  } catch (e) {
    return null;
  }

  let outputTokens = 0;
  let turns = 0;
  let model = null;

  for (const line of lines) {
    let entry;
    try { entry = JSON.parse(line); } catch (e) { continue; }
    if (entry.type !== 'assistant' || !entry.message) continue;
    const usage = entry.message.usage;
    if (!usage) continue;
    outputTokens += usage.output_tokens || 0;
    turns++;
    if (entry.message.model) model = entry.message.model;
  }

  return { outputTokens, turns, model };
}

function getPrice(model) {
  if (!model) return null;
  for (const [prefix, price] of Object.entries(MODEL_PRICING)) {
    if (model.startsWith(prefix)) return price;
  }
  return null;
}

function formatNumber(n) {
  return n.toLocaleString('en-US');
}

function buildStats(claudeDir, flagPath, share) {
  const sessionFile = findSessionFile(claudeDir);
  if (!sessionFile) {
    return 'laconic-stats: no session data yet.';
  }

  const session = parseSession(sessionFile);
  if (!session) {
    return 'laconic-stats: could not read session file.';
  }

  const activeMode = readFlag(flagPath) || DEFAULT_MODE;
  const ratio = COMPRESSION_RATIOS[activeMode] || COMPRESSION_RATIOS[DEFAULT_MODE];
  const saved = Math.round(session.outputTokens * ratio);
  const pct = Math.round(ratio * 100);

  const price = getPrice(session.model);
  const usd = price !== null
    ? `~$${((saved / 1_000_000) * price).toFixed(4)}`
    : 'n/a';

  if (share) {
    const modelShort = session.model ? session.model.replace('claude-', '') : 'unknown';
    return `laconic saved ~${formatNumber(saved)} tokens (~${pct}%) over ${session.turns} turns [${modelShort}] ${usd} saved`;
  }

  const divider = '─'.repeat(35);
  return [
    `laconic-stats  [${activeMode} mode]`,
    divider,
    `turns          ${formatNumber(session.turns)}`,
    `output tokens  ${formatNumber(session.outputTokens)}`,
    `estimated saved ~${formatNumber(saved)} tokens  (~${pct}%)`,
    `USD saved      ${usd}`,
    `model          ${session.model || 'unknown'}`,
  ].join('\n');
}

const claudeDir = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
const flagPath = getFlagPath(claudeDir);

let args = process.argv.slice(2);
const share = args.includes('--share');

// When called directly (not via mode-tracker), read the prompt from stdin
// to extract --share. When called programmatically, args come via process.argv.
let input = '';
process.stdin.on('data', chunk => { input += chunk; });
process.stdin.on('end', () => {
  try {
    if (input) {
      const data = JSON.parse(input);
      const prompt = (data.prompt || '').toLowerCase();
      const hasShare = /--share/.test(prompt);
      const text = buildStats(claudeDir, flagPath, hasShare);
      process.stdout.write(JSON.stringify({ decision: 'block', reason: text }));
    } else {
      const text = buildStats(claudeDir, flagPath, share);
      process.stdout.write(text + '\n');
    }
  } catch (e) {
    process.stdout.write(JSON.stringify({ decision: 'block', reason: 'laconic-stats: internal error.' }));
  }
});
