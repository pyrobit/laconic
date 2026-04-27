<p align="center">
  <img src="docs/SpartanShield.png" width="120" />
</p>

<h1 align="center">laconic ⌃</h1>

<p align="center">
  <strong>User-friendly token reduction with intelligible words. Built on Caveman.</strong>
</p>

<p align="center">
  <a href="https://github.com/pyrobit/laconic/stargazers"><img src="https://img.shields.io/github/stars/pyrobit/laconic?style=flat&color=yellow" alt="Stars"></a>
  <a href="https://github.com/pyrobit/laconic/commits/main"><img src="https://img.shields.io/github/last-commit/pyrobit/laconic?style=flat" alt="Last Commit"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/pyrobit/laconic?style=flat" alt="License"></a>
</p>

<p align="center">
  <a href="#before--after">Before/After</a> •
  <a href="#install">Install</a> •
  <a href="#intensity-levels">Levels</a> •
  <a href="#laconic-skills">Skills</a> •
  <a href="#benchmarks">Benchmarks</a> •
  <a href="#evals">Evals</a>
</p>

<p align="center">
  <strong>⌃ Laconic</strong> &nbsp;·&nbsp;
  <em>structured brevity for coding agents</em>
</p>

---

A user-friendly way to save tokens without losing rigor or clarity. Laconic is a fork and small experiment built on [Caveman](https://github.com/JuliusBrussee/caveman), which already does an excellent job at aggressive token reduction.

This repo explores a different tradeoff: less compression, more structure. It may not be updated as often as Caveman. If you want the most efficient token reduction, use Caveman first.

Laconic uses telegraphic English and symbols where helpful, cuts **~65-80% of output tokens**, and keeps technical accuracy. It also includes [terse commits](#laconic-commit), [structured reviews](#laconic-review), [compressed internal reasoning](#laconic-think), and more.

## Before / After

<table>
<tr>
<td width="50%">

### 🗣️ Normal Codex (69 tokens)

> "Your component re-renders because the inline object prop gets a new reference on every render. React's shallow comparison sees a different object each time, so it re-renders the child. Move that object behind `useMemo` so the reference stays stable unless its dependencies change."

</td>
<td width="50%">

### ⌃ Laconic Codex (28 tokens)

> "**Issue:** Inline object prop causes React re-renders. **Cause:** ∀ render: ref({k:v}) ≠ prior ⇒ !shallowEqual ⇒ re-render(C). **Solution:** const p = useMemo(() => ({k: v}), [deps]). **Rationale:** Memoized ref remains stable across renders."

</td>
</tr>
<tr>
<td>

### 🗣️ Normal Codex

> "The auth middleware expiry check is off by one. It uses `<` where `<=` is needed, so a token at its exact expiry boundary can still pass validation. Change the comparison to `<=` so expired tokens are rejected consistently."

</td>
<td>

### ⌃ Laconic Codex

> "**Issue:** Auth middleware token expiry bug. **Cause:** Check uses `<` instead of `<=`. **Solution:** Change to `<=`. **Rationale:** Ensures expiry is handled correctly."

</td>
</tr>
</table>

**Same fix. 65-80% fewer words. Clear structure. Built on Caveman.**

**Pick your Laconic mode:**

<table>
<tr>
<td width="50%">

#### ⌃ Terse

> "**Issue:** Inline object prop causes React re-renders. **Cause:** ∀ render: ref({k:v}) ≠ prior ⇒ !shallowEqual ⇒ re-render(C). **Solution:** `useMemo(() => ({k: v}), [deps])`. **Rationale:** Stable ref prevents needless renders."

</td>
<td width="50%">

#### ⚖️ Balanced

> "**Issue:** Inline object prop causes React re-renders. **Cause:** Each render creates a new object reference, so shallow comparison fails. **Solution:** Memoize the object with `useMemo`. **Rationale:** Stable references let React skip unnecessary work." 

</td>
</tr>
</table>

**Same answer. Pick density or readability.**

```
┌─────────────────────────────────────┐
│  TOKENS SAVED          ████████ 65-80% │
│  TECHNICAL ACCURACY    ████████ 100%│
│  SPEED INCREASE        ████████ ~3x │
│  CLARITY               ████████ STRUCTURED │
└─────────────────────────────────────┘
```

- **Faster responses** — fewer output tokens to generate
- **Easier scanning** — less text, same answer
- **Same accuracy** — technical content stays; fluff goes ([paper](https://arxiv.org/abs/2604.00025))
- **Lower cost** — ~65-80% fewer output tokens
- **More fun** — code review, but shorter

## Install

Pick your agent. One command.

| Agent | Install |
|-------|---------|
| **Claude Code** | `claude plugin marketplace add pyrobit/laconic && claude plugin install laconic@laconic` |
| **Codex** | Clone repo → `/plugins` → Search "Laconic" → Install |
| **Gemini CLI** | `gemini extensions install https://github.com/pyrobit/laconic` |
| **Cursor** | `npx skills add pyrobit/laconic -a cursor` |
| **Windsurf** | `npx skills add pyrobit/laconic -a windsurf` |
| **Copilot** | `npx skills add pyrobit/laconic -a github-copilot` |
| **Cline** | `npx skills add pyrobit/laconic -a cline` |
| **Any other** | `npx skills add pyrobit/laconic` |

Install once. Use it every session for that target after that. One rock. That's it.

### What You Get

Auto-activation is built in for Claude Code, Gemini CLI, and the repo-local Codex setup below. `npx skills add` installs the skill for other agents, but does **not** install repo rule files or instructions, so Laconic does not auto-start there unless you add the always-on snippet below.

| Feature | Claude Code | Codex | Gemini CLI | Cursor | Windsurf | Cline | Copilot |
|---------|:-----------:|:-----:|:----------:|:------:|:--------:|:-----:|:-------:|
| Laconic mode | Y | Y | Y | Y | Y | Y | Y |
| Auto-activate every session | Y | Y¹ | Y | —² | —² | —² | —² |
| `/laconic` command | Y | Y¹ | Y | — | — | — | — |
| Mode switching (terse/balanced) | Y | Y¹ | Y | Y³ | Y³ | — | — |
| Statusline badge | Y⁴ | — | — | — | — | — | — |
| laconic-commit | Y | — | Y | Y | Y | Y | Y |
| laconic-review | Y | — | Y | Y | Y | Y | Y |
| laconic-think | Y | — | Y | Y | Y | Y | Y |
| laconic-compress | Y | Y | Y | Y | Y | Y | Y |
| laconic-help | Y | — | Y | Y | Y | Y | Y |

> [!NOTE]
> Auto-activation works differently per agent: Claude Code uses SessionStart hooks, this repo's Codex dogfood setup uses `.codex/hooks.json`, Gemini uses context files. Cursor/Windsurf/Cline/Copilot can be made always-on, but `npx skills add` installs only the skill, not the repo rule/instruction files.
>
> ¹ Codex uses `$laconic` syntax, not `/laconic`. This repo ships `.codex/hooks.json`, so Laconic auto-starts when you run Codex inside this repo. The installed plugin gives you `$laconic`. Auxiliary skills such as `laconic-commit`, `laconic-review`, `laconic-help`, and `laconic-think` are not in the Codex plugin bundle — use the SKILL.md files directly.
> ² Add the "Want it always on?" snippet below to those agents' system prompt or rule file if you want session-start activation.
> ³ Cursor and Windsurf receive the full SKILL.md with Laconic modes. Mode switching works on-demand via the skill; no slash command.
> ⁴ Available in Claude Code, but plugin install only nudges setup. Standalone `install.sh` / `install.ps1` configures it automatically when no custom `statusLine` exists.

<details>
<summary><strong>Claude Code — full details</strong></summary>

Plugin install gives you skills plus auto-loading hooks. If no custom `statusLine` is configured, Laconic prompts badge setup on the first session.

```bash
claude plugin marketplace add pyrobit/laconic
claude plugin install laconic@laconic
```

**Standalone hooks (without plugin):** If you prefer not to use the plugin system:
```bash
# macOS / Linux / WSL
bash <(curl -s https://raw.githubusercontent.com/pyrobit/laconic/main/hooks/install.sh)

# Windows (PowerShell)
irm https://raw.githubusercontent.com/pyrobit/laconic/main/hooks/install.ps1 | iex
```

Or from a local clone: `bash hooks/install.sh` / `powershell -File hooks\install.ps1`

Uninstall: `bash hooks/uninstall.sh` or `powershell -File hooks\uninstall.ps1`

**Statusline badge:** Shows `[LACONIC]`, `[LACONIC:BALANCED]`, and related states in the Claude Code status bar.

- **Plugin install:** If you do not already have a custom `statusLine`, Claude should offer to configure it on the first session
- **Standalone install:** Configured automatically by `install.sh` / `install.ps1` unless you already have a custom statusline
- **Custom statusline:** Installer leaves your existing statusline alone. See [`hooks/README.md`](hooks/README.md) for the merge snippet

</details>

<details>
<summary><strong>Codex — full details</strong></summary>

**macOS / Linux:**
1. Clone repo → Open Codex in the repo directory → `/plugins` → Search "Laconic" → Install
2. Repo-local auto-start is already wired by `.codex/hooks.json` + `.codex/config.toml`

**Windows:**
1. Enable symlinks first: `git config --global core.symlinks true` (requires Developer Mode or admin)
2. Clone repo → Open VS Code → Codex Settings → Plugins → find "Laconic" under local marketplace → Install → Reload Window
3. Codex hooks are currently disabled on Windows, so use `$laconic` to start manually

This repo also ships `.codex/hooks.json` and enables hooks in `.codex/config.toml`, so Laconic auto-activates while you run Codex inside this repo on macOS/Linux. The installed plugin gives you `$laconic`. If you want always-on behavior in other repos, copy the same `SessionStart` hook there and enable:

```toml
[features]
codex_hooks = true
```

</details>

<details>
<summary><strong>Gemini CLI — full details</strong></summary>

```bash
gemini extensions install https://github.com/pyrobit/laconic
```

Update: `gemini extensions update laconic` · Uninstall: `gemini extensions uninstall laconic`

Auto-activates via the `GEMINI.md` context file. Also ships custom Gemini commands:
- `/laconic` — switch to canonical terse mode
- `/laconic balanced` — switch to balanced mode
- `/laconic-commit` — generate terse commit message
- `/laconic-review` — one-line code review
- `/laconic-think` — compress hidden reasoning

</details>

<details>
<summary><strong>Cursor / Windsurf / Cline / Copilot — full details</strong></summary>

`npx skills add` installs the skill file only. It does **not** install the agent's rule file or system instructions, so Laconic does not auto-start. For always-on behavior, add the "Want it always on?" snippet below to your agent's rules or system prompt.

| Agent | Command | Not installed | Mode switching | Always-on location |
|-------|---------|--------------|:--------------:|--------------------|
| Cursor | `npx skills add pyrobit/laconic -a cursor` | `.cursor/rules/laconic.mdc` | Y | Cursor rules |
| Windsurf | `npx skills add pyrobit/laconic -a windsurf` | `.windsurf/rules/laconic.md` | Y | Windsurf rules |
| Cline | `npx skills add pyrobit/laconic -a cline` | `.clinerules/laconic.md` | — | Cline rules or system prompt |
| Copilot | `npx skills add pyrobit/laconic -a github-copilot` | `.github/copilot-instructions.md` + `AGENTS.md` | — | Copilot custom instructions |

Uninstall: `npx skills remove laconic`

Copilot works with Chat, Edits, and Coding Agent.

</details>

<details>
<summary><strong>Any other agent (opencode, Roo, Amp, Goose, Kiro, and 40+ more)</strong></summary>

[npx skills](https://github.com/vercel-labs/skills) supports 40+ agents:

```bash
npx skills add pyrobit/laconic           # auto-detect agent
npx skills add pyrobit/laconic -a amp
npx skills add pyrobit/laconic -a augment
npx skills add pyrobit/laconic -a goose
npx skills add pyrobit/laconic -a kiro-cli
npx skills add pyrobit/laconic -a roo
# ... and many more
```

Uninstall: `npx skills remove laconic`

> **Windows note:** `npx skills` uses symlinks by default. If symlinks fail, add `--copy`: `npx skills add pyrobit/laconic --copy`

**Important:** These agents do not have a hook system, so Laconic will not auto-start. Say `/laconic` or `/laconic balanced` each session.

**Want it always on?** Paste this into your agent's system prompt or rules file. Laconic will be active from the first message of every session:

```
Use laconic mode. Preserve exact technical substance.
Structure: Issue / Cause / Solution / Rationale.
Telegraphic English OK when still readable. Code unchanged.
ACTIVE EVERY RESPONSE. Off: "stop laconic", "plain english", or "normal mode".
```

Where to put it:
| Agent | File |
|-------|------|
| opencode | `.config/opencode/AGENTS.md` |
| Roo | `.roo/rules/laconic.md` |
| Amp | your workspace system prompt |
| Others | your agent's system prompt or rules file |

</details>

## Usage

Trigger with:
- `/laconic` or Codex `$laconic`
- `/laconic balanced`
- `/laconic-think`
- "laconic mode"
- "less tokens please"

Stop with: "stop laconic", "plain english", or "normal mode"

### Intensity Levels

| Level | Trigger | What it does |
|-------|---------|------------|
| **Terse** | `/laconic` or `/laconic terse` | Default Laconic mode. Strong compression with readable structure |
| **Balanced** | `/laconic balanced` | More connective words for complex topics while staying concise |

The level stays active until you change it or the session ends.

## Laconic Skills

### laconic-commit

`/laconic-commit` — terse commit messages. Conventional Commits. ≤50 char subject. Why over what.

### laconic-review

`/laconic-review` — one-line PR comments: `L42: 🔴 bug: user null. Add guard.` No throat-clearing.

### laconic-help

`/laconic-help` — quick-reference card. All modes, skills, commands, one command away.

### laconic-think

`/laconic-think` — compress hidden reasoning with fixed `Issue / Cause / Options / Best / Rationale` structure. Final answer stays clear; combine with `/laconic` when you also want terse user-facing output.

Best fit:
- Short debugging and root-cause analysis
- Refactors where the plan is obvious but repetitive
- High-volume expert workflows where you want less internal sprawl

Current limits:
- Best when the agent/runtime already supports hidden scratchpads or non-user-visible reasoning channels
- Current hook/runtime tracking only records `think` on/off; it does not persist `terse|balanced|draft` submodes
- Not ideal for security-sensitive, legal/medical/finance, incident response, or long architecture exploration where wider reasoning is safer

### laconic-compress

`/laconic-compress <filepath>` — Laconic makes Codex *speak* with fewer tokens. **Compress** makes Codex *read* fewer tokens.

For Codex repos, `AGENTS.md` is prime target. Laconic Compress rewrites memory files into compact prose so Codex reads less, while keeping a human-readable backup.

```
/laconic-compress AGENTS.md
```

```
AGENTS.md          ← compressed (Codex reads this in repo context — fewer tokens)
AGENTS.original.md ← human-readable backup (you read and edit this)
```

| File | Original | Compressed | Saved |
|------|----------:|----------:|------:|
| `claude-md-preferences.md` | 706 | 285 | **59.6%** |
| `project-notes.md` | 1145 | 535 | **53.3%** |
| `claude-md-project.md` | 1122 | 636 | **43.3%** |
| `todo-list.md` | 627 | 388 | **38.1%** |
| `mixed-with-code.md` | 888 | 560 | **36.9%** |
| **Average** | **898** | **481** | **46%** |

Code blocks, URLs, file paths, commands, headings, dates, and version numbers pass through untouched. Only prose is compressed. See the full [laconic-compress README](laconic-compress/README.md) for details. [Security note](./laconic-compress/SECURITY.md): Snyk flags this as high risk due to subprocess and file patterns; this is a false positive.

## Benchmarks

Real token counts from the Claude API ([reproduce locally](benchmarks/)):

<!-- BENCHMARK-TABLE-START -->
| Task | Normal (tokens) | Laconic (tokens) | Saved |
|------|---------------:|----------------:|------:|
| Explain React re-render bug | 1180 | 159 | 87% |
| Fix auth middleware token expiry | 704 | 121 | 83% |
| Set up PostgreSQL connection pool | 2347 | 380 | 84% |
| Explain git rebase vs merge | 702 | 292 | 58% |
| Refactor callback to async/await | 387 | 301 | 22% |
| Architecture: microservices vs monolith | 446 | 310 | 30% |
| Review PR for security issues | 678 | 398 | 41% |
| Docker multi-stage build | 1042 | 290 | 72% |
| Debug PostgreSQL race condition | 1200 | 232 | 81% |
| Implement React error boundary | 3454 | 456 | 87% |
| **Average** | **1214** | **294** | **65%** |

*Range: 22%–87% savings across prompts. Caveman achieves higher raw compression (~75%); Laconic trades some of that for structured clarity and easier correctness checks.*
<!-- BENCHMARK-TABLE-END -->

## Correctness Comparison

Laconic maintains **100% technical accuracy** across all benchmarks. The fixed structure keeps each claim logically traceable, with no loss of rigor.

- **Accuracy verified:** Responses to the 10 benchmark prompts in `benchmarks/prompts.json` preserve full correctness while compressing tokens.
- **Brevity can improve accuracy:** Research shows that constraining models to brief responses improved accuracy by 26 percentage points on some benchmarks and reversed performance hierarchies ([\"Brevity Constraints Reverse Performance Hierarchies in Language Models\"](https://arxiv.org/abs/2604.00025)).
- **Structured clarity:** Laconic's **Issue/Cause/Solution/Rationale** format improves scanability and makes correctness easier to verify.

> [!IMPORTANT]
> Base `/laconic` only affects output tokens. `/laconic-think` is separate, optional, and most effective on runtimes that already support hidden reasoning channels. Biggest win: **structured readability, speed, and clarity**. Cost savings are a bonus.

A March 2026 paper, ["Brevity Constraints Reverse Performance Hierarchies in Language Models"](https://arxiv.org/abs/2604.00025), found that constraining large models to brief responses **improved accuracy by 26 percentage points** on some benchmarks and reversed performance hierarchies. Verbose is not always better. Sometimes less is more correct.

## Laconic Note

**Foundation**  
Laconic builds directly on Caveman's proven token-reduction work. Credit to Julius.

**Grok Support**  
See `laconic-grok.md` — one-click custom instruction version now available.

It adds a fixed 4-part structure (**Issue • Cause • Solution • Rationale**) plus selective symbols for scanability, while keeping every technical claim traceable.

Caveman wins on pure token count.  
Laconic trades ~10-15% tokens for better logical clarity and accessibility.

Result: 65-80% savings vs normal prose with improved rigor and readability.

### Symbolic Notation Guide (Advanced)

**Example — Formal Foundation**

**Proposition (P):**  
Laconic ⊢ maximal information density ∧ rigor ∧ intelligibility

**Definitions**  
T = {Issue, Cause, Solution, Rationale}  
omit({articles, auxiliaries, fluff})  
pack(φ) ↦ {∀, ∃, ⇒, ⇔, ≠, ∵, ⊢, ∈, ⊆, O(·)}

**Symbol Index**

| Symbol | English Meaning          |
|--------|--------------------------|
| ∀      | For all                  |
| ∃      | There exists             |
| ⇒      | Implies                  |
| ⇔      | If and only if           |
| ≠      | Not equal                |
| ∈      | Element of               |
| ⊆      | Subset of                |
| ∵      | Because                  |
| ⊢      | Proves / entails         |
| ∧      | And                      |
| O(·)   | Big-O (complexity)       |

This formal style is an **optional advanced example**. Most users should stick to terse or balanced mode.

## Evals

Laconic does not just claim 65-80%. Laconic measures it.

The `evals/` directory has a three-arm eval harness that measures real token compression against a proper control, not just "verbose vs skill" but "terse vs skill". Comparing Laconic to verbose Claude alone would conflate the skill with generic terseness.

```bash
# Run the eval (needs claude CLI)
uv run python evals/llm_run.py

# Read results (no API key, runs offline)
uv run --with tiktoken python evals/measure.py
```

## Star This Repo

If Laconic saves you tokens or money, leave a star.

[![Star History Chart](https://api.star-history.com/svg?repos=pyrobit/laconic&type=Date)](https://star-history.com/#pyrobit/laconic&Date)

## 🪨 The Caveman Ecosystem

Three tools. One philosophy: **agents do more with less**.

| Repo | What | One-liner |
|------|------|-----------|
| [**laconic**](https://github.com/pyrobit/laconic) *(you are here)* | Output compression skill | Structured brevity with clear reasoning — ~65-80% fewer output tokens across Claude Code, Cursor, Gemini, Codex |
| [**cavemem**](https://github.com/JuliusBrussee/cavemem) | Cross-agent persistent memory | *why agent forget when agent can remember* — compressed SQLite + MCP, local by default |
| [**cavekit**](https://github.com/JuliusBrussee/cavekit) | Spec-driven autonomous build loop | *why agent guess when agent can know* — natural language → kits → parallel build → verified |

Install one or combine them. Each stands alone.

## Also by Julius Brussee

- **[Revu](https://github.com/JuliusBrussee/revu-swift)** — local-first macOS study app with FSRS spaced repetition, decks, exams, and study guides. [revu.cards](https://revu.cards)

## License

MIT. Use it freely.
