#!/bin/bash
# laconic — statusline badge script for Claude Code
# Reads the compatibility flag file and outputs a colored Laconic badge.
#
# Usage in ~/.claude/settings.json:
#   "statusLine": { "type": "command", "command": "bash /path/to/laconic-statusline.sh" }

FLAG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/.laconic-active"

[ -L "$FLAG" ] && exit 0
[ ! -f "$FLAG" ] && exit 0

MODE=$(head -c 64 "$FLAG" 2>/dev/null | tr -d '\n\r' | tr '[:upper:]' '[:lower:]')
MODE=$(printf '%s' "$MODE" | tr -cd 'a-z0-9-')

case "$MODE" in
  off) exit 0 ;;
  terse) MODE="terse" ;;
  balanced) MODE="balanced" ;;
  commit|review|compress) ;;
  *) exit 0 ;;
esac

if [ "$MODE" = "terse" ]; then
  printf '\033[38;5;172m[LACONIC]\033[0m'
else
  SUFFIX=$(printf '%s' "$MODE" | tr '[:lower:]' '[:upper:]')
  printf '\033[38;5;172m[LACONIC:%s]\033[0m' "$SUFFIX"
fi
