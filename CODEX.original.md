# CODEX.md — laconic

## README is a product artifact

README is product front door. Non-technical people read it to decide if Laconic is worth installing. Treat it like UI copy.

Rules for README changes:
- Keep install paths complete and accurate.
- Keep before/after examples easy to spot.
- Keep benchmark claims tied to real data in `benchmarks/` and `evals/`.
- Translate agent internals into plain user-facing language when possible.

## Project overview

Laconic makes AI coding agents answer in structured concise prose. It cuts filler while keeping technical accuracy. Distribution includes Claude Code hooks, Codex plugin assets, Gemini extension metadata, repo rule files, and portable `npx skills` surfaces.

## Source of truth

Edit these files directly:

| File | Purpose |
|------|---------|
| `skills/laconic/SKILL.md` | Core Laconic behavior |
| `rules/laconic-activate.md` | Always-on rule text synced into agent-specific rule files |
| `skills/laconic-commit/SKILL.md` | Commit-message skill |
| `skills/laconic-review/SKILL.md` | Review-comment skill |
| `skills/laconic-help/SKILL.md` | Quick help card |
| `laconic-compress/SKILL.md` | Compress skill behavior |

Synced copies:

| File | Synced from |
|------|-------------|
| `laconic/SKILL.md` | `skills/laconic/SKILL.md` |
| `plugins/laconic/skills/laconic/SKILL.md` | `skills/laconic/SKILL.md` |
| `.cursor/skills/laconic/SKILL.md` | `skills/laconic/SKILL.md` |
| `.windsurf/skills/laconic/SKILL.md` | `skills/laconic/SKILL.md` |
| `laconic.skill` | ZIP of `skills/laconic/` |
| `.clinerules/laconic.md` | `rules/laconic-activate.md` |
| `.github/copilot-instructions.md` | `rules/laconic-activate.md` |
| `.cursor/rules/laconic.mdc` | `rules/laconic-activate.md` + Cursor frontmatter |
| `.windsurf/rules/laconic.md` | `rules/laconic-activate.md` + Windsurf frontmatter |
| `skills/laconic-compress/` | `laconic-compress/` |
| `plugins/laconic/skills/laconic-compress/` | `laconic-compress/` |

## Codex runtime

Repo-local Codex activation lives in `.codex/` and plugin assets live in `plugins/laconic/`.

- Hook config: `.codex/hooks.json`
- Feature flag: `.codex/config.toml`
- Plugin bundle: `plugins/laconic/`
- Command surface: `$laconic`

Behavior:
- SessionStart hook emits Laconic activation rule on `startup|resume`.
- `.codex/config.toml` enables repo-local hooks with `codex_hooks = true`.
- Codex uses `$laconic`, not `/laconic`.
- Repo-local auto-start works on macOS/Linux. On Windows, install plugin but start manually with `$laconic`.

Maintenance rules:
- Keep `.codex/hooks.json` activation text aligned with `rules/laconic-activate.md`.
- Keep hook command side-effect free beyond emitting rule text.
- Preserve `.codex/config.toml` hook enablement unless user asks otherwise.

## Skills

Primary modes:
- `terse`
- `balanced`

Independent skills:
- `laconic-commit`
- `laconic-review`
- `laconic-help`
- `laconic-compress`

`laconic-compress` rewrites prose-heavy memory files, preserves code/URLs/paths, and saves `<filename>.original.md` backups.

Codex notes:
- Plugin bundle gives `$laconic`.
- `laconic-commit` and `laconic-review` are not in Codex plugin bundle; use `SKILL.md` files directly.
- For repo memory, `AGENTS.md` is usually higher-value than `CODEX.md`.

## Distribution

| Agent | Mechanism | Auto-activates? |
|-------|-----------|----------------|
| Claude Code | Hooks + plugin metadata | Yes |
| Codex | `plugins/laconic/` + repo hook config | Yes on supported local sessions |
| Gemini CLI | `gemini-extension.json` + `GEMINI.md` | Yes |
| Cursor | `.cursor/rules/laconic.mdc` | Yes |
| Windsurf | `.windsurf/rules/laconic.md` | Yes |
| Cline | `.clinerules/laconic.md` | Yes |
| Copilot | `.github/copilot-instructions.md` + `AGENTS.md` | Yes |
| Others | `npx skills add bruno335548975/laconic` | No |

## Evals and benchmarks

`evals/` measures Laconic against control arms:
- `__baseline__`
- `__terse__`
- `<skill>`

Honest comparison is skill vs `__terse__`, not skill vs baseline.

`benchmarks/` runs real prompts through the Claude API and updates README benchmark table from committed JSON results.

## Working rules

- Edit source files, then resync copies.
- Keep naming Laconic-only. No Caveman compatibility surface remains.
- Do not fabricate benchmark or eval numbers.
- Preserve README’s user-facing quality.
