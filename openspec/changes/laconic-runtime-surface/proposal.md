## Why

The repo has been renamed to Laconic, but its live runtime surface still presents Caveman vocabulary in slash commands, badge text, setup nudges, plugin metadata, and mode names. That split makes the product feel unfinished and blocks users from discovering the newer Laconic behavior model through the runtime they actually use.

## What Changes

- Standardize the primary runtime command surface on `/laconic*` across Claude hooks, Gemini commands, Codex plugin metadata, and setup/help text.
- Change statusline badge behavior to render `[LACONIC]` and `[LACONIC:<MODE>]` instead of Caveman labels.
- Align runtime-visible prose modes with the Laconic skill (`terse`, `balanced`) instead of legacy Caveman-only levels (`lite`, `full`, `ultra`, `wenyan*`).
- Remove remaining Caveman-branded runtime surfaces so Laconic is the only public mode vocabulary.
- Consolidate runtime mode and alias definitions so command parsing, badge rendering, installer messaging, and hook reinforcement cannot drift again.

## Capabilities

### New Capabilities
- `laconic-runtime-surface`: Canonical Laconic runtime commands, badge labels, and mode vocabulary for interactive agents.

### Modified Capabilities
- None.

## Impact

- Affected code: `hooks/`, `commands/`, `plugins/laconic/skills/laconic/agents/openai.yaml`, repo instruction files, and user-facing docs that describe runtime commands or badges.
- User-facing API: slash commands, badge labels, setup nudges, and default prompt text.
- Compatibility: none. Public runtime, badges, plugin metadata, and docs use Laconic-only naming.
