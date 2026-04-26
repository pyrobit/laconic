# Laconic Hooks

These hooks are bundled with the Laconic plugin and activate automatically when the plugin is installed.

If you installed Laconic standalone, run `bash hooks/install.sh` or `powershell -ExecutionPolicy Bypass -File hooks\install.ps1` to wire them into `settings.json`.

## What's Included

### `laconic-activate.js`

- Runs once when Claude Code starts
- Writes the active mode to `~/.claude/.laconic-active`
- Emits Laconic rules as hidden SessionStart context
- Detects missing statusline config and emits a setup nudge

### `laconic-mode-tracker.js`

- Fires on every user prompt
- Tracks `/laconic`, `/laconic balanced`, `/laconic-commit`, `/laconic-review`, `/laconic-compress`
- Removes the flag on `stop laconic`, `plain english`, or `normal mode`

### `laconic-statusline.sh` / `laconic-statusline.ps1`

- Reads `~/.claude/.laconic-active`
- Shows `[LACONIC]`, `[LACONIC:BALANCED]`, `[LACONIC:COMMIT]`, etc.

## Statusline Badge

The badge shows which Laconic mode is active directly in Claude Code.

Examples:
- `/laconic` -> `[LACONIC]`
- `/laconic balanced` -> `[LACONIC:BALANCED]`
- `/laconic-commit` -> `[LACONIC:COMMIT]`

Plugin installs nudge setup only when no custom `statusLine` exists. Standalone installs wire the badge automatically when possible and leave existing custom statuslines alone.

Manual setup:

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash /path/to/laconic-statusline.sh"
  }
}
```

```json
{
  "statusLine": {
    "type": "command",
    "command": "powershell -ExecutionPolicy Bypass -File C:\\path\\to\\laconic-statusline.ps1"
  }
}
```

## How It Works

```text
SessionStart hook -> writes mode -> ~/.claude/.laconic-active <- writes mode <- UserPromptSubmit hook
                                          |
                                       reads
                                          v
                                  Statusline script
                                  [LACONIC:...]
```

## Uninstall

- Claude Code plugin: `claude plugin disable laconic`
- Standalone hooks: `bash hooks/uninstall.sh` or `powershell -ExecutionPolicy Bypass -File hooks\uninstall.ps1`
