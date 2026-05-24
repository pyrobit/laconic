#!/usr/bin/env node
// laconic — UserPromptSubmit hook to track Laconic mode

const fs = require('fs');
const path = require('path');
const os = require('os');
const {
  getDefaultMode,
  getFlagPath,
  isActivationPrompt,
  isDeactivationPrompt,
  isIndependentMode,
  parseRuntimeCommand,
  readFlag,
  safeWriteFlag,
} = require('./laconic-config');

const claudeDir = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
const flagPath = getFlagPath(claudeDir);

let input = '';
process.stdin.on('data', chunk => { input += chunk; });
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);
    const prompt = (data.prompt || '').trim();
    const lowered = prompt.toLowerCase();

    if (/^\/laconic-stats(\s|$)/.test(lowered)) {
      const statsScript = path.join(__dirname, 'laconic-stats.js');
      const { execFileSync } = require('child_process');
      try {
        const result = execFileSync(process.execPath, [statsScript], {
          input: JSON.stringify(data),
          encoding: 'utf8',
          timeout: 5000,
        });
        process.stdout.write(result);
      } catch (e) {
        process.stdout.write(JSON.stringify({ decision: 'block', reason: 'laconic-stats: error reading session data.' }));
      }
      return;
    }

    if (isActivationPrompt(lowered) && !isDeactivationPrompt(lowered)) {
      const mode = getDefaultMode();
      if (mode !== 'off') {
        safeWriteFlag(flagPath, mode);
      }
    }

    const commandMode = parseRuntimeCommand(lowered);
    if (commandMode && commandMode !== 'off') {
      safeWriteFlag(flagPath, commandMode);
    } else if (commandMode === 'off') {
      try { fs.unlinkSync(flagPath); } catch (e) {}
    }

    if (isDeactivationPrompt(lowered)) {
      try { fs.unlinkSync(flagPath); } catch (e) {}
    }

    if (/\bnormal thinking\b/i.test(lowered) && readFlag(flagPath) === 'think') {
      try { fs.unlinkSync(flagPath); } catch (e) {}
    }

    const activeMode = readFlag(flagPath);
    if (activeMode && !isIndependentMode(activeMode)) {
      process.stdout.write(JSON.stringify({
        hookSpecificOutput: {
          hookEventName: 'UserPromptSubmit',
          additionalContext: 'LACONIC MODE ACTIVE (' + activeMode + '). ' +
            'Use Issue/Cause/Solution/Rationale. Telegraphic OK. ' +
            'Code/commits/security: write normal.'
        }
      }));
    }
  } catch (e) {
    // Silent fail
  }
});
