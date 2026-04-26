## Context

The repository already ships Laconic file names (`laconic-activate.js`, `laconic-statusline.sh`, `commands/laconic.toml`) but the runtime behavior still leaks Caveman terminology throughout command parsing, badge labels, setup nudges, plugin display metadata, and hook reinforcement strings. The mismatch is deeper than simple copy edits: the hook runtime still models prose intensity with Caveman-era modes (`full`, `lite`, `ultra`, `wenyan*`) while the Laconic skill defines `terse` and `balanced`.

This change crosses multiple runtime surfaces:
- Claude Code hooks and statusline
- Gemini command metadata
- Codex plugin metadata / prompts
- install/setup guidance and user-facing help text

Because those surfaces currently carry duplicated mode names and command strings, a direct text replacement would be fragile. The design should introduce one canonical runtime vocabulary.

## Goals / Non-Goals

**Goals:**
- Make `/laconic*` the primary runtime command surface everywhere users discover or trigger runtime behavior.
- Make badges and runtime messaging consistently show Laconic branding.
- Align primary prose modes with the Laconic skill vocabulary.
- Reduce future drift by centralizing mode and alias definitions.

**Non-Goals:**
- Renaming every internal file, asset, env var, or persisted flag path in the same change.
- Redesigning Laconic prose rules beyond mode alignment and runtime ergonomics.
- Reworking benchmark/eval content unless runtime-facing text depends on it.

## Decisions

### 1. Introduce canonical Laconic runtime modes
Use canonical user-facing prose modes `terse` and `balanced`, with existing auxiliary modes `commit`, `review`, and `compress`.

Rationale:
- Matches the current Laconic skill instead of preserving an obsolete command vocabulary.
- Gives users one mode language across skill docs, slash commands, and badges.
- Keeps the runtime semantics consistent with the skill.

### 2. Centralize runtime surface metadata in shared configuration
Move command prefixes, canonical modes, and alias resolution behind shared configuration used by command parsing, badge formatting, setup nudges, and installer/help messaging.

Rationale:
- Current duplication caused the repo to ship `laconic-*` filenames with Caveman runtime strings.
- Shared metadata makes future skill enhancements easier, such as new modes or a dedicated `/laconic-help`.

Alternatives considered:
- Patch each file independently.
  Rejected because drift will recur on the next rename or mode tweak.

### 3. Align internal persistence with the public Laconic name
Persist runtime state under Laconic-native names so hooks, installers, and docs no longer carry hidden Caveman naming debt.

Rationale:
- Removes confusing internal/public naming mismatches.
- Keeps install/uninstall behavior simpler.

### 4. Treat consistency as a product requirement
Keep badges, commands, prompts, and plugin metadata on the same Laconic vocabulary.

Rationale:
- Avoids split-brand experiences where commands, badges, and docs disagree.
- Gives maintainers one contract to preserve.

## Risks / Trade-offs

- Partial rename across docs, hooks, and plugin metadata -> Mitigation: drive all runtime-facing strings from shared configuration and add targeted verification.
- Existing users may depend on hidden Caveman-only levels like `wenyan` -> Mitigation: keep those out of canonical Laconic docs in this change and decide separately whether they survive as advanced modes.

## Migration Plan

1. Add canonical Laconic runtime vocabulary in shared hook/config code.
2. Update command metadata, badge rendering, setup nudges, and plugin prompts to consume canonical Laconic labels.
3. Verify `/laconic*` commands activate the correct canonical modes and produce Laconic badges.
4. Update runtime-facing docs/help text to present Laconic commands as the only public behavior.
5. Rename any remaining internal flag/env/path surfaces that still leak Caveman naming.

Rollback:
- Revert to prior command parsing and badge strings.

## Open Questions

- Should `wenyan*` survive as a documented advanced Laconic mode or be removed entirely?
- Does the repo want a first-class `/laconic-help` runtime command as part of this same cleanup, or is command discoverability handled elsewhere?
