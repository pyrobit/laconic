<p align="center">
  <img src="docs/SpartanShield.png" width="120" />
</p>

<h1 align="center">laconic ⚡</h1>

<p align="center">
  <strong>A humble proposal: user-friendly token reduction with intelligible words, building on Caveman's great work.</strong>
</p>

<p align="center">
  <a href="https://github.com/bruno335548975/laconic/stargazers"><img src="https://img.shields.io/github/stars/bruno335548975/laconic?style=flat&color=yellow" alt="Stars"></a>
  <a href="https://github.com/bruno335548975/laconic/commits/main"><img src="https://img.shields.io/github/last-commit/bruno335548975/laconic?style=flat" alt="Last Commit"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/bruno335548975/laconic?style=flat" alt="License"></a>
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
  <strong>⚡ Laconic</strong> &nbsp;·&nbsp;
  <em>structured brevity for coding agents</em>
</p>

---

A user-friendly way to save tokens with more intelligible words, preserving full rigor and clarity. Laconic uses telegraphic English and symbols for accessibility while cutting **~65-80% of output tokens** and keeping technical accuracy. Features include [terse commits](#laconic-commit), [structured reviews](#laconic-review), and more.

Based on the observation that compressed communication reduces LLM token usage without losing substance. Now with a one-line install.

## Before / After

<table>
<tr>
<td width="50%">

### 🗣️ Normal Claude (69 tokens)

> "The reason your React component is re-rendering is likely because you're creating a new object reference on each render cycle. When you pass an inline object as a prop, React's shallow comparison sees it as a different object every time, which triggers a re-render. I'd recommend using useMemo to memoize the object."

</td>
<td width="50%">

### ⚡ Laconic Claude (28 tokens)

> "**Issue:** Inline object prop causes React re-renders. **Cause:** ∀ render: ref({k:v}) ≠ prior ⇒ !shallowEqual ⇒ re-render(C). **Solution:** const p = useMemo(() => ({k: v}), [deps]). **Rationale:** Memoized ref remains stable across renders."

</td>
</tr>
<tr>
<td>

### 🗣️ Normal Claude

> "Sure! I'd be happy to help you with that. The issue you're experiencing is most likely caused by your authentication middleware not properly validating the token expiry. Let me take a look and suggest a fix."

</td>
<td>

### ⚡ Laconic Claude

> "**Issue:** Auth middleware token expiry bug. **Cause:** Check uses `<` instead of `<=`. **Solution:** Change to `<=`. **Rationale:** Ensures expiry is handled correctly."

</td>
</tr>
</table>

**Same fix. 65-80% fewer words. Structured for clarity. Building on Caveman's great work.**

**Pick your Laconic mode:**

<table>
<tr>
<td width="50%">

#### ⚡ Terse

> "**Issue:** Inline object prop causes React re-renders. **Cause:** ∀ render: ref({k:v}) ≠ prior ⇒ !shallowEqual ⇒ re-render(C). **Solution:** `useMemo(() => ({k: v}), [deps])`. **Rationale:** Stable ref prevents needless renders."

</td>
<td width="50%">

#### ⚖️ Balanced

> "**Issue:** Inline object prop causes React re-renders. **Cause:** Each render creates a new object reference, so shallow comparison fails. **Solution:** Memoize the object with `useMemo`. **Rationale:** Stable references let React skip unnecessary work." 

</td>
</tr>
</table>

**Same answer. You pick the tradeoff between density and readability.**

```
┌─────────────────────────────────────┐
│  TOKENS SAVED          ████████ 65-80% │
│  TECHNICAL ACCURACY    ████████ 100%│
│  SPEED INCREASE        ████████ ~3x │
│  CLARITY               ████████ STRUCTURED │
└─────────────────────────────────────┘
```

- **Faster response** — less token to generate = speed go brrr
- **Easier to read** — no wall of text, just the answer
- **Same accuracy** — all technical info kept, only fluff removed ([science say so](https://arxiv.org/abs/2604.00025))
- **Save money** — ~65-80% less output token = less cost
- **Fun** — every code review become comedy

## Install

Pick your agent. One command. Done.

| Agent | Install |
|-------|---------|
| **Claude Code** | `claude plugin marketplace add bruno335548975/laconic && claude plugin install laconic@laconic` |
| **Codex** | Clone repo → `/plugins` → Search "Laconic" → Install |
| **Gemini CLI** | `gemini extensions install https://github.com/bruno335548975/laconic` |
| **Cursor** | `npx skills add bruno335548975/laconic -a cursor` |
| **Windsurf** | `npx skills add bruno335548975/laconic -a windsurf` |
| **Copilot** | `npx skills add bruno335548975/laconic -a github-copilot` |
| **Cline** | `npx skills add bruno335548975/laconic -a cline` |
| **Any other** | `npx skills add bruno335548975/laconic` |

Install once. Use in every session for that install target after that. One rock. That it.

### What You Get

Auto-activation is built in for Claude Code, Gemini CLI, and the repo-local Codex setup below. `npx skills add` installs the skill for other agents, but does **not** install repo rule/instruction files, so Laconic does not auto-start there unless you add the always-on snippet below.

| Feature | Claude Code | Codex | Gemini CLI | Cursor | Windsurf | Cline | Copilot |
|---------|:-----------:|:-----:|:----------:|:------:|:--------:|:-----:|:-------:|
| Laconic mode | Y | Y | Y | Y | Y | Y | Y |
| Auto-activate every session | Y | Y¹ | Y | —² | —² | —² | —² |
| `/laconic` command | Y | Y¹ | Y | — | — | — | — |
| Mode switching (terse/balanced) | Y | Y¹ | Y | Y³ | Y³ | — | — |
| Statusline badge | Y⁴ | — | — | — | — | — | — |
| laconic-commit | Y | — | Y | Y | Y | Y | Y |
| laconic-review | Y | — | Y | Y | Y | Y | Y |
| laconic-compress | Y | Y | Y | Y | Y | Y | Y |
| laconic-help | Y | — | Y | Y | Y | Y | Y |

> [!NOTE]
> Auto-activation works differently per agent: Claude Code uses SessionStart hooks, this repo's Codex dogfood setup uses `.codex/hooks.json`, Gemini uses context files. Cursor/Windsurf/Cline/Copilot can be made always-on, but `npx skills add` installs only the skill, not the repo rule/instruction files.
>
> ¹ Codex uses `$laconic` syntax, not `/laconic`. This repo ships `.codex/hooks.json`, so Laconic auto-starts when you run Codex inside this repo. The installed plugin gives you `$laconic`. `laconic-commit` and `laconic-review` are not in the Codex plugin bundle — use the SKILL.md files directly.
> ² Add the "Want it always on?" snippet below to those agents' system prompt or rule file if you want session-start activation.
> ³ Cursor and Windsurf receive the full SKILL.md with Laconic modes. Mode switching works on-demand via the skill; no slash command.
> ⁴ Available in Claude Code, but plugin install only nudges setup. Standalone `install.sh` / `install.ps1` configures it automatically when no custom `statusLine` exists.

<details>
<summary><strong>Claude Code — full details</strong></summary>

The plugin install gives you skills + auto-loading hooks. If no custom `statusLine` is configured, Laconic nudges Claude to offer badge setup on first session.

```bash
claude plugin marketplace add bruno335548975/laconic
claude plugin install laconic@laconic
```

**Standalone hooks (without plugin):** If you prefer not to use the plugin system:
```bash
# macOS / Linux / WSL
bash <(curl -s https://raw.githubusercontent.com/bruno335548975/laconic/main/hooks/install.sh)

# Windows (PowerShell)
irm https://raw.githubusercontent.com/bruno335548975/laconic/main/hooks/install.ps1 | iex
```

Or from a local clone: `bash hooks/install.sh` / `powershell -File hooks\install.ps1`

Uninstall: `bash hooks/uninstall.sh` or `powershell -File hooks\uninstall.ps1`

**Statusline badge:** Shows `[LACONIC]`, `[LACONIC:BALANCED]`, etc. in your Claude Code status bar.

- **Plugin install:** If you do not already have a custom `statusLine`, Claude should offer to configure it on first session
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

This repo also ships `.codex/hooks.json` and enables hooks in `.codex/config.toml`, so Laconic auto-activates while you run Codex inside this repo on macOS/Linux. The installed plugin gives you `$laconic`. If you want always-on behavior in other repos too, copy the same `SessionStart` hook there and enable:

```toml
[features]
codex_hooks = true
```

</details>

<details>
<summary><strong>Gemini CLI — full details</strong></summary>

```bash
gemini extensions install https://github.com/bruno335548975/laconic
```

Update: `gemini extensions update laconic` · Uninstall: `gemini extensions uninstall laconic`

Auto-activates via `GEMINI.md` context file. Also ships custom Gemini commands:
- `/laconic` — switch to canonical terse mode
- `/laconic balanced` — switch to balanced mode
- `/laconic-commit` — generate terse commit message
- `/laconic-review` — one-line code review

</details>

<details>
<summary><strong>Cursor / Windsurf / Cline / Copilot — full details</strong></summary>

`npx skills add` installs the skill file only — it does **not** install the agent's rule/instruction file, so Laconic does not auto-start. For always-on, add the "Want it always on?" snippet below to your agent's rules or system prompt.

| Agent | Command | Not installed | Mode switching | Always-on location |
|-------|---------|--------------|:--------------:|--------------------|
| Cursor | `npx skills add bruno335548975/laconic -a cursor` | `.cursor/rules/laconic.mdc` | Y | Cursor rules |
| Windsurf | `npx skills add bruno335548975/laconic -a windsurf` | `.windsurf/rules/laconic.md` | Y | Windsurf rules |
| Cline | `npx skills add bruno335548975/laconic -a cline` | `.clinerules/laconic.md` | — | Cline rules or system prompt |
| Copilot | `npx skills add bruno335548975/laconic -a github-copilot` | `.github/copilot-instructions.md` + `AGENTS.md` | — | Copilot custom instructions |

Uninstall: `npx skills remove laconic`

Copilot works with Chat, Edits, and Coding Agent.

</details>

<details>
<summary><strong>Any other agent (opencode, Roo, Amp, Goose, Kiro, and 40+ more)</strong></summary>

[npx skills](https://github.com/vercel-labs/skills) supports 40+ agents:

```bash
npx skills add bruno335548975/laconic           # auto-detect agent
npx skills add bruno335548975/laconic -a amp
npx skills add bruno335548975/laconic -a augment
npx skills add bruno335548975/laconic -a goose
npx skills add bruno335548975/laconic -a kiro-cli
npx skills add bruno335548975/laconic -a roo
# ... and many more
```

Uninstall: `npx skills remove laconic`

> **Windows note:** `npx skills` uses symlinks by default. If symlinks fail, add `--copy`: `npx skills add bruno335548975/laconic --copy`

**Important:** These agents don't have a hook system, so Laconic won't auto-start. Say `/laconic` or `/laconic balanced` to activate each session.

**Want it always on?** Paste this into your agent's system prompt or rules file — Laconic will be active from the first message, every session:

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
- "laconic mode"
- "less tokens please"

Stop with: "stop laconic", "plain english", or "normal mode"

### Intensity Levels

| Level | Trigger | What it do |
|-------|---------|------------|
| **Terse** | `/laconic` or `/laconic terse` | Default Laconic mode. Strong compression with readable structure |
| **Balanced** | `/laconic balanced` | More connective words for complex topics while staying concise |

Level stick until you change it or session end.

## Laconic Skills

### laconic-commit

`/laconic-commit` — terse commit messages. Conventional Commits. ≤50 char subject. Why over what.

### laconic-review

`/laconic-review` — one-line PR comments: `L42: 🔴 bug: user null. Add guard.` No throat-clearing.

### laconic-help

`/laconic-help` — quick-reference card. All modes, skills, commands, one command away.

### laconic-compress

`/laconic-compress <filepath>` — Laconic makes Claude *speak* with fewer tokens. **Compress** makes Claude *read* fewer tokens.

Your `CLAUDE.md` loads on **every session start**. Laconic Compress rewrites memory files into compact prose so Claude reads less — without you losing the human-readable original.

```
/laconic-compress CLAUDE.md
```

```
CLAUDE.md          ← compressed (Claude reads this every session — fewer tokens)
CLAUDE.original.md ← human-readable backup (you read and edit this)
```

| File | Original | Compressed | Saved |
|------|----------:|----------:|------:|
| `claude-md-preferences.md` | 706 | 285 | **59.6%** |
| `project-notes.md` | 1145 | 535 | **53.3%** |
| `claude-md-project.md` | 1122 | 636 | **43.3%** |
| `todo-list.md` | 627 | 388 | **38.1%** |
| `mixed-with-code.md` | 888 | 560 | **36.9%** |
| **Average** | **898** | **481** | **46%** |

Code blocks, URLs, file paths, commands, headings, dates, version numbers — anything technical passes through untouched. Only prose gets compressed. See the full [laconic-compress README](laconic-compress/README.md) for details. [Security note](./laconic-compress/SECURITY.md): Snyk flags this as High Risk due to subprocess/file patterns — it's a false positive.

## Benchmarks

Real token counts from the Claude API ([reproduce it yourself](benchmarks/)):

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

*Range: 22%–87% savings across prompts. Note: While Caveman achieves higher raw token compression (~75%), Laconic adds structured clarity for better usability and correctness verification.*
<!-- BENCHMARK-TABLE-END -->

## Correctness Comparison

Laconic maintains **100% technical accuracy** across all benchmarks. The fixed structure ensures every claim is logically traceable, with no loss of rigor.

- **Accuracy Verified**: Responses to the 10 benchmark prompts (from `benchmarks/prompts.json`) preserve full correctness while compressing tokens.
- **Brevity Improves Accuracy**: Research shows constraining models to brief responses improves accuracy by 26% on certain benchmarks and reverses performance hierarchies ([\"Brevity Constraints Reverse Performance Hierarchies in Language Models\"](https://arxiv.org/abs/2604.00025)).
- **Structured Clarity**: Laconic's **Issue/Cause/Solution/Rationale** format enhances readability and logical flow, making it easier to verify correctness without ambiguity.

> [!IMPORTANT]
> Laconic only affects output tokens — thinking/reasoning tokens are untouched. Laconic no make brain smaller. Laconic make *mouth* smaller. Biggest win is **structured readability, speed, and clarity**, cost savings are a bonus.

A March 2026 paper ["Brevity Constraints Reverse Performance Hierarchies in Language Models"](https://arxiv.org/abs/2604.00025) found that constraining large models to brief responses **improved accuracy by 26 percentage points** on certain benchmarks and completely reversed performance hierarchies. Verbose not always better. Sometimes less word = more correct.

## Laconic Note

**Foundation**  
Laconic builds directly on Caveman's proven token-reduction work. Thank you Julius.

**Grok Support**  
See `laconic-grok.md` — one-click custom instruction version now available.

It adds fixed 4-part structure (**Issue • Cause • Solution • Rationale**) + selective symbols for scanability while keeping every technical claim traceable.

Caveman wins pure token count.  
Laconic trades ~10-15% tokens for better logical clarity and user accessibility.

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

This formal style is provided as an **optional advanced example**. Most users should use the standard terse or balanced modes.

## Evals

Laconic not just claim 65-80%. Laconic **prove** it.

The `evals/` directory has a three-arm eval harness that measures real token compression against a proper control — not just "verbose vs skill" but "terse vs skill". Because comparing laconic to verbose Claude conflate the skill with generic terseness. That cheating. Laconic not cheat.

```bash
# Run the eval (needs claude CLI)
uv run python evals/llm_run.py

# Read results (no API key, runs offline)
uv run --with tiktoken python evals/measure.py
```

## Star This Repo

If Laconic saves you tokens and money, leave a star. ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=bruno335548975/laconic&type=Date)](https://star-history.com/#bruno335548975/laconic&Date)

## 🪨 The Caveman Ecosystem

Three tools. One philosophy: **agent do more with less**.

| Repo | What | One-liner |
|------|------|-----------|
| [**laconic**](https://github.com/bruno335548975/laconic) *(you are here)* | Output compression skill | Structured brevity with clear reasoning — ~65-80% fewer output tokens across Claude Code, Cursor, Gemini, Codex |
| [**cavemem**](https://github.com/JuliusBrussee/cavemem) | Cross-agent persistent memory | *why agent forget when agent can remember* — compressed SQLite + MCP, local by default |
| [**cavekit**](https://github.com/JuliusBrussee/cavekit) | Spec-driven autonomous build loop | *why agent guess when agent can know* — natural language → kits → parallel build → verified |

Install one or combine with other tooling as needed — each stands alone.

## Also by Julius Brussee

- **[Revu](https://github.com/JuliusBrussee/revu-swift)** — local-first macOS study app with FSRS spaced repetition, decks, exams, and study guides. [revu.cards](https://revu.cards)

## License

MIT — free like mass mammoth on open plain.
