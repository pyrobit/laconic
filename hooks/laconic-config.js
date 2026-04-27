#!/usr/bin/env node
// laconic — shared runtime configuration helpers
//
// Resolution order for default mode:
//   1. LACONIC_DEFAULT_MODE environment variable
//   2. Config file defaultMode field:
//      - $XDG_CONFIG_HOME/laconic/config.json
//      - ~/.config/laconic/config.json
//      - %APPDATA%\laconic\config.json
//   3. 'terse'

const fs = require('fs');
const path = require('path');
const os = require('os');

const FLAG_FILE_NAME = '.laconic-active';
const DEFAULT_MODE = 'terse';
const CANONICAL_PROSE_MODES = ['terse', 'balanced'];
const INDEPENDENT_MODES = ['commit', 'review', 'compress', 'think'];
const VALID_MODES = ['off', ...CANONICAL_PROSE_MODES, ...INDEPENDENT_MODES];
const COMMAND_MODE_ALIASES = {
  terse: 'terse',
  balanced: 'balanced',
};

function normalizeMode(mode, fallback = null) {
  if (typeof mode !== 'string') return fallback;
  const raw = mode.trim().toLowerCase();
  if (!raw) return fallback;
  if (VALID_MODES.includes(raw)) return raw;
  return fallback;
}

function getConfigDir(appName) {
  if (process.env.XDG_CONFIG_HOME) {
    return path.join(process.env.XDG_CONFIG_HOME, appName);
  }
  if (process.platform === 'win32') {
    return path.join(
      process.env.APPDATA || path.join(os.homedir(), 'AppData', 'Roaming'),
      appName
    );
  }
  return path.join(os.homedir(), '.config', appName);
}

function getConfigPathCandidates() {
  return [path.join(getConfigDir('laconic'), 'config.json')];
}

function getConfigPath() {
  return getConfigPathCandidates()[0];
}

function getDefaultMode() {
  const envCandidates = [process.env.LACONIC_DEFAULT_MODE];
  for (const envMode of envCandidates) {
    const normalized = normalizeMode(envMode);
    if (normalized) return normalized;
  }

  for (const configPath of getConfigPathCandidates()) {
    try {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      const normalized = normalizeMode(config.defaultMode);
      if (normalized) return normalized;
    } catch (e) {
      // Config file doesn't exist or is invalid — try next candidate.
    }
  }

  return DEFAULT_MODE;
}

function isIndependentMode(mode) {
  return INDEPENDENT_MODES.includes(mode);
}

function getCanonicalModeLabel(mode) {
  return normalizeMode(mode, DEFAULT_MODE);
}

function getStatuslineText(mode) {
  const canonical = normalizeMode(mode);
  if (!canonical || canonical === 'off') return '';
  if (canonical === DEFAULT_MODE) return '[LACONIC]';
  return `[LACONIC:${canonical.toUpperCase()}]`;
}

function getFlagPath(claudeDir) {
  return path.join(claudeDir, FLAG_FILE_NAME);
}

function parseRuntimeCommand(prompt) {
  if (typeof prompt !== 'string') return null;
  const lowered = prompt.trim().toLowerCase();
  if (!lowered.startsWith('/')) return null;

  const [cmd, arg = ''] = lowered.split(/\s+/, 2);
  const directCommands = {
    '/laconic-commit': 'commit',
    '/laconic-review': 'review',
    '/laconic-think': 'think',
    '/laconic:think': 'think',
    '/laconic:laconic-think': 'think',
    '/laconic-compress': 'compress',
    '/laconic:compress': 'compress',
    '/laconic:laconic-compress': 'compress',
  };

  if (directCommands[cmd]) {
    return directCommands[cmd];
  }

  const primaryCommands = new Set(['/laconic', '/laconic:laconic']);
  if (!primaryCommands.has(cmd)) {
    return null;
  }

  if (!arg) {
    return getDefaultMode();
  }

  return COMMAND_MODE_ALIASES[arg] || getDefaultMode();
}

function isActivationPrompt(prompt) {
  if (typeof prompt !== 'string') return false;
  const text = prompt.trim().toLowerCase();
  if (!text) return false;

  if (/^(laconic|spartan|telegraph)$/.test(text)) {
    return true;
  }

  const mentionsStyle = /\b(laconic|spartan|telegraph)\b/.test(text);
  const asksToActivate = /\b(activate|enable|turn on|start|use|talk like|write like|respond like)\b/.test(text);
  if (mentionsStyle && asksToActivate && !isDeactivationPrompt(text)) {
    return true;
  }

  return /\blaconic\s+mode\b/.test(text) && !isDeactivationPrompt(text);
}

function isDeactivationPrompt(prompt) {
  if (typeof prompt !== 'string') return false;
  return (
    /\b(stop|disable|deactivate|turn off)\b.*\blaconic\b/i.test(prompt) ||
    /\blaconic\b.*\b(stop|disable|deactivate|turn off)\b/i.test(prompt) ||
    /\bnormal mode\b/i.test(prompt) ||
    /\bplain english\b/i.test(prompt)
  );
}

function findSkillPath() {
  const candidates = [path.join(__dirname, '..', 'skills', 'laconic', 'SKILL.md')];
  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) return candidate;
  }
  return null;
}

// Symlink-safe flag file write.
// Refuses symlinks at the target file and at the immediate parent directory,
// uses O_NOFOLLOW where available, writes atomically via temp + rename with
// 0600 permissions. Protects against local attackers replacing the predictable
// flag path (~/.claude/.laconic-active) with a symlink to clobber other files.
//
// Does NOT walk the full ancestor chain — macOS has /tmp -> /private/tmp and
// many legitimate setups route through symlinked home dirs, so a full walk
// produces false positives. The attack surface requires write access to the
// immediate parent, which is what we check.
//
// Silent-fails on any filesystem error — the flag is best-effort.
function safeWriteFlag(flagPath, content) {
  try {
    const flagDir = path.dirname(flagPath);
    fs.mkdirSync(flagDir, { recursive: true });

    try {
      if (fs.lstatSync(flagDir).isSymbolicLink()) return;
    } catch (e) {
      return;
    }

    try {
      if (fs.lstatSync(flagPath).isSymbolicLink()) return;
    } catch (e) {
      if (e.code !== 'ENOENT') return;
    }

    const tempPath = path.join(flagDir, `${FLAG_FILE_NAME}.${process.pid}.${Date.now()}`);
    const O_NOFOLLOW = typeof fs.constants.O_NOFOLLOW === 'number' ? fs.constants.O_NOFOLLOW : 0;
    const flags = fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_EXCL | O_NOFOLLOW;
    let fd;
    try {
      fd = fs.openSync(tempPath, flags, 0o600);
      fs.writeSync(fd, String(content));
      try { fs.fchmodSync(fd, 0o600); } catch (e) { /* best-effort on Windows */ }
    } finally {
      if (fd !== undefined) fs.closeSync(fd);
    }
    fs.renameSync(tempPath, flagPath);
  } catch (e) {
    // Silent fail — flag is best-effort
  }
}

// Symlink-safe, size-capped, whitelist-validated flag file read.
// Returns canonical Laconic mode names.
const MAX_FLAG_BYTES = 64;

function readFlag(flagPath) {
  try {
    let st;
    try {
      st = fs.lstatSync(flagPath);
    } catch (e) {
      return null;
    }
    if (st.isSymbolicLink() || !st.isFile()) return null;
    if (st.size > MAX_FLAG_BYTES) return null;

    const O_NOFOLLOW = typeof fs.constants.O_NOFOLLOW === 'number' ? fs.constants.O_NOFOLLOW : 0;
    const flags = fs.constants.O_RDONLY | O_NOFOLLOW;
    let fd;
    let out;
    try {
      fd = fs.openSync(flagPath, flags);
      const buf = Buffer.alloc(MAX_FLAG_BYTES);
      const n = fs.readSync(fd, buf, 0, MAX_FLAG_BYTES, 0);
      out = buf.slice(0, n).toString('utf8');
    } finally {
      if (fd !== undefined) fs.closeSync(fd);
    }

    return normalizeMode(out);
  } catch (e) {
    return null;
  }
}

module.exports = {
  CANONICAL_PROSE_MODES,
  DEFAULT_MODE,
  FLAG_FILE_NAME,
  INDEPENDENT_MODES,
  VALID_MODES,
  findSkillPath,
  getCanonicalModeLabel,
  getConfigDir,
  getConfigPath,
  getConfigPathCandidates,
  getDefaultMode,
  getFlagPath,
  getStatuslineText,
  isActivationPrompt,
  isDeactivationPrompt,
  isIndependentMode,
  normalizeMode,
  parseRuntimeCommand,
  readFlag,
  safeWriteFlag,
};
