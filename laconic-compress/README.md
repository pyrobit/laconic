<p align="center">
  <img src="https://em-content.zobj.net/source/apple/391/rock_1faa8.png" width="80" />
</p>

<h1 align="center">laconic-compress</h1>

<p align="center">
  <strong>shrink memory file. save token every session.</strong>
</p>

---

`laconic-compress` compresses project memory files such as `CLAUDE.md`, todos, and preferences into Laconic prose so each session loads fewer tokens.

Claude reads memory files on every session start. Smaller prose means lower recurring context cost.

## What it does

```text
/laconic-compress CLAUDE.md
```

```text
CLAUDE.md          ← compressed copy Claude reads
CLAUDE.original.md ← readable backup you edit
```

Original content is preserved in `.original.md`. Re-run the skill after edits to recompress.

## Benchmarks

Real fixture results:

| File | Original | Compressed | Saved |
|------|----------:|-----------:|------:|
| `claude-md-preferences.md` | 706 | 285 | **59.6%** |
| `project-notes.md` | 1145 | 535 | **53.3%** |
| `claude-md-project.md` | 1122 | 636 | **43.3%** |
| `todo-list.md` | 627 | 388 | **38.1%** |
| `mixed-with-code.md` | 888 | 560 | **36.9%** |
| **Average** | **898** | **481** | **46%** |

All validations passed: headings, code blocks, URLs, and file paths were preserved exactly.

## Before / After

Original:

> "I strongly prefer TypeScript with strict mode enabled for all new code. Please don't use `any` type unless there's genuinely no way around it, and if you do, leave a comment explaining the reasoning. I find that taking the time to properly type things catches a lot of bugs before they ever make it to runtime."

Compressed:

> "Prefer TypeScript strict mode always. No `any` unless unavoidable — comment why if used. Proper types catch bugs early."

Same instructions. Fewer tokens every session.

## Security

`laconic-compress` is flagged as Snyk High Risk due to subprocess and file I/O heuristics. That is a false positive. See [SECURITY.md](./SECURITY.md).

## Install

The compress skill ships with Laconic. Use:

```text
/laconic-compress <filepath>
```

Local source lives at:

```bash
laconic-compress/
```

Requires Python 3.10+.

## Supported files

| Type | Compress? |
|------|-----------|
| `.md`, `.txt`, `.rst` | Yes |
| Extensionless natural language | Yes |
| `.py`, `.js`, `.ts`, `.json`, `.yaml` | No |
| `*.original.md` | No |

## How it works

```text
/laconic-compress CLAUDE.md
        ↓
detect file type
        ↓
Claude compresses
        ↓
validate output
        ↓
if needed: targeted repair pass
        ↓
write compressed file + .original.md backup
```

Only the compression call and any targeted repair use model tokens. Detection and validation stay local.

## Preserved exactly

- Code blocks
- Inline code
- URLs and links
- File paths
- Commands
- Technical terms
- Headings
- Table structure
- Dates, versions, and numeric values

## Part of Laconic

This skill is part of [laconic](https://github.com/pyrobit/laconic).

- `laconic` makes Claude speak with structured concision.
- `laconic-compress` makes Claude read less context.
