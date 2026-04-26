#!/usr/bin/env node
// laconic — Claude Code SessionStart activation hook
//
// Runs on every session start:
//   1. Writes flag file at $CLAUDE_CONFIG_DIR/.laconic-active (statusline reads this)
//   2. Emits Laconic ruleset as hidden SessionStart context
//   3. Detects missing statusline config and emits setup nudge

const fs = require('fs');
const path = require('path');
const os = require('os');
const {
  DEFAULT_MODE,
  findSkillPath,
  getCanonicalModeLabel,
  getDefaultMode,
  getFlagPath,
  isIndependentMode,
  safeWriteFlag,
} = require('./laconic-config');

const claudeDir = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
const flagPath = getFlagPath(claudeDir);
const settingsPath = path.join(claudeDir, 'settings.json');

const mode = getDefaultMode();

if (mode === 'off') {
  try { fs.unlinkSync(flagPath); } catch (e) {}
  process.stdout.write('OK');
  process.exit(0);
}

safeWriteFlag(flagPath, mode);

if (isIndependentMode(mode)) {
  process.stdout.write(
    'LACONIC MODE ACTIVE — level: ' + mode + '. Behavior defined by /laconic-' + mode + ' skill.'
  );
  process.exit(0);
}

const modeLabel = getCanonicalModeLabel(mode);
const skillPath = findSkillPath();
let skillContent = '';
try {
  if (skillPath) {
    skillContent = fs.readFileSync(skillPath, 'utf8');
  }
} catch (e) {
  // Standalone install without skill files — fall back below.
}

let output;

if (skillContent) {
  const body = skillContent.replace(/^---[\s\S]*?---\s*/, '');
  const filtered = body.split('\n').reduce((acc, line) => {
    const tableRowMatch = line.match(/^\|\s*\*\*(\S+?)\*\*\s*\|/);
    if (tableRowMatch) {
      if (tableRowMatch[1] === modeLabel) {
        acc.push(line);
      }
      return acc;
    }
    acc.push(line);
    return acc;
  }, []);

  output = 'LACONIC MODE ACTIVE — level: ' + modeLabel + '\n\n' + filtered.join('\n');
} else {
  output =
    'LACONIC MODE ACTIVE — level: ' + modeLabel + '\n\n' +
    'Use telegraphic English. Preserve exact technical substance. Keep structure clear.\n\n' +
    '## Persistence\n\n' +
    'ACTIVE EVERY RESPONSE. Off only: "stop laconic", "normal mode", or "plain english".\n\n' +
    'Current level: **' + modeLabel + '**. Switch: `/laconic terse|balanced`.\n\n' +
    '## Rules\n\n' +
    'Format: **Issue:** **Cause:** **Solution:** **Rationale:**. Drop filler where it helps. ' +
    'Fragments OK when still readable. Technical terms exact. Code blocks unchanged.\n\n' +
    '## Boundaries\n\n' +
    'Code/commits/PRs/security warnings: write normal.';
}

try {
  let hasStatusline = false;
  if (fs.existsSync(settingsPath)) {
    const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
    if (settings.statusLine) {
      hasStatusline = true;
    }
  }

  if (!hasStatusline) {
    const isWindows = process.platform === 'win32';
    const scriptName = isWindows ? 'laconic-statusline.ps1' : 'laconic-statusline.sh';
    const scriptPath = path.join(__dirname, scriptName);
    const command = isWindows
      ? `powershell -ExecutionPolicy Bypass -File "${scriptPath}"`
      : `bash "${scriptPath}"`;
    const statusLineSnippet =
      '"statusLine": { "type": "command", "command": ' + JSON.stringify(command) + ' }';
    output += "\n\n" +
      'STATUSLINE SETUP NEEDED: The laconic plugin includes a statusline badge showing active mode ' +
      '(e.g. [LACONIC], [LACONIC:BALANCED]). It is not configured yet. ' +
      'To enable, add this to ' + path.join(claudeDir, 'settings.json') + ': ' +
      statusLineSnippet + ' ' +
      'Proactively offer to set this up for the user on first interaction.';
  }
} catch (e) {
  // Silent fail — don't block session start over statusline detection.
}

process.stdout.write(output);
