---
name: laconic-help
description: >
  Quick-reference card for all laconic modes, skills, and commands.
  One-shot display, not a persistent mode. Trigger: /laconic-help,
  "laconic help", "what laconic commands", "how do I use laconic".
---

# Laconic Help

Display this reference card when invoked. One-shot — do NOT change mode, write flag files, or persist anything. Output in laconic style.

## Modes

| Mode | Trigger | What change |
|------|---------|-------------|
| **Terse** | `/laconic` or `/laconic terse` | Default laconic mode. Structured, tight, still readable. |
| **Balanced** | `/laconic balanced` | More connective words for complex topics. |

Mode stick until changed or session end.

## Skills

| Skill | Trigger | What it do |
|-------|---------|-----------|
| **laconic-commit** | `/laconic-commit` | Terse commit messages. Conventional Commits. ≤50 char subject. |
| **laconic-review** | `/laconic-review` | One-line PR comments: `L42: bug: user null. Add guard.` |
| **laconic-think** | `/laconic-think` | Compress hidden reasoning. Final answer stay clear. |
| **laconic-compress** | `/laconic-compress <file>` | Compress .md files to laconic prose. Saves input tokens. |
| **laconic-help** | `/laconic-help` | This card. |

## Deactivate

Say "stop laconic", "plain english", or "normal mode". Resume anytime with `/laconic`.

## Configure Default Mode

Default mode = `terse`. Change it:

**Environment variable** (highest priority):
```bash
export LACONIC_DEFAULT_MODE=balanced
```

**Config file** (`~/.config/laconic/config.json`):
```json
{ "defaultMode": "balanced" }
```

Set `"off"` to disable auto-activation on session start. User can still activate manually with `/laconic`.

Resolution: env var > config file > `terse`.

## More

Full docs: https://github.com/pyrobit/laconic
