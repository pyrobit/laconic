#!/usr/bin/env python3
from collections import Counter
import re
from pathlib import Path

URL_REGEX = re.compile(r"https?://[^\s)]+")
FENCE_OPEN_REGEX = re.compile(r"^(\s{0,3})(`{3,}|~{3,})(.*)$")
HEADING_REGEX = re.compile(r"^(#{1,6})\s+(.*)", re.MULTILINE)
BULLET_REGEX = re.compile(r"^\s*[-*+]\s+", re.MULTILINE)
INLINE_CODE_REGEX = re.compile(r"(?P<fence>`+)(?!`)(?P<body>.+?)(?<!`)(?P=fence)", re.DOTALL)
ENV_VAR_REGEX = re.compile(r"\$[A-Z_][A-Z0-9_]*\b")
COMMAND_LINE_REGEX = re.compile(
    r"^\s*(?:[-*+]\s+|\d+\.\s+)?(?:\$|#)?\s*"
    r"(?:npm|pnpm|yarn|bun|node|python\d*|pip|uv|git|docker|kubectl|cargo|go|make|cmake|gradle|mvn|npx|bash|sh|powershell|pwsh|claude|codex|gemini)\b[^\n]*$",
    re.MULTILINE,
)

# Conservative path detection. Match explicit path prefixes or slash-separated
# paths that end in a file-like segment with an extension. Avoids prose pairs
# like "pros/cons" or "state/lifecycle" being treated as filesystem paths.
PATH_REGEX = re.compile(
    r"(?:@/|~/|\./|\.\./|/|[A-Za-z]:\\)[\w\-/\\\.]+"
    r"|(?:[\w\-\.]+[/\\])+[\w\-\.]*\.[A-Za-z0-9]{1,8}\b"
)


class ValidationResult:
    def __init__(self):
        self.is_valid = True
        self.errors = []
        self.warnings = []

    def add_error(self, msg):
        self.is_valid = False
        self.errors.append(msg)

    def add_warning(self, msg):
        self.warnings.append(msg)


def read_file(path: Path) -> str:
    return path.read_text(errors="ignore")


# ---------- Extractors ----------


def extract_headings(text):
    return [(level, title.strip()) for level, title in HEADING_REGEX.findall(text)]


def extract_code_blocks(text):
    """Line-based fenced code block extractor.

    Handles ``` and ~~~ fences with variable length (CommonMark: closing
    fence must use same char and be at least as long as opening). Supports
    nested fences (e.g. an outer 4-backtick block wrapping inner 3-backtick
    content).
    """
    blocks = []
    lines = text.split("\n")
    i = 0
    n = len(lines)
    while i < n:
        m = FENCE_OPEN_REGEX.match(lines[i])
        if not m:
            i += 1
            continue
        fence_char = m.group(2)[0]
        fence_len = len(m.group(2))
        open_line = lines[i]
        block_lines = [open_line]
        i += 1
        closed = False
        while i < n:
            close_m = FENCE_OPEN_REGEX.match(lines[i])
            if (
                close_m
                and close_m.group(2)[0] == fence_char
                and len(close_m.group(2)) >= fence_len
                and close_m.group(3).strip() == ""
            ):
                block_lines.append(lines[i])
                closed = True
                i += 1
                break
            block_lines.append(lines[i])
            i += 1
        if closed:
            blocks.append("\n".join(block_lines))
        # Unclosed fences are silently skipped — they indicate malformed markdown
        # and including them would cause false-positive validation failures.
    return blocks


def extract_urls(text):
    return set(URL_REGEX.findall(text))


def extract_paths(text):
    return set(PATH_REGEX.findall(text))


def strip_code_blocks(text):
    stripped = text
    for block in extract_code_blocks(text):
        stripped = stripped.replace(block, "\n", 1)
    return stripped


def extract_inline_code(text):
    stripped = strip_code_blocks(text)
    return [m.group(0) for m in INLINE_CODE_REGEX.finditer(stripped)]


def extract_env_vars(text):
    return set(ENV_VAR_REGEX.findall(text))


def extract_commands(text):
    stripped = strip_code_blocks(text)
    return [line.strip() for line in COMMAND_LINE_REGEX.findall(stripped)]


def count_bullets(text):
    return len(BULLET_REGEX.findall(text))


# ---------- Validators ----------


def validate_headings(orig, comp, result):
    h1 = extract_headings(orig)
    h2 = extract_headings(comp)

    if len(h1) != len(h2):
        result.add_error(f"Heading count mismatch: {len(h1)} vs {len(h2)}")

    if h1 != h2:
        result.add_error("Heading text/order changed")


def validate_code_blocks(orig, comp, result):
    c1 = extract_code_blocks(orig)
    c2 = extract_code_blocks(comp)

    if c1 != c2:
        result.add_error("Code blocks not preserved exactly")


def validate_urls(orig, comp, result):
    u1 = extract_urls(orig)
    u2 = extract_urls(comp)

    if u1 != u2:
        result.add_error(f"URL mismatch: lost={u1 - u2}, added={u2 - u1}")


def validate_paths(orig, comp, result):
    p1 = extract_paths(orig)
    p2 = extract_paths(comp)

    missing = p1 - p2
    if missing:
        result.add_error(f"Path mismatch: lost={missing}")


def validate_inline_code(orig, comp, result):
    c1 = Counter(extract_inline_code(orig))
    c2 = Counter(extract_inline_code(comp))

    missing = sorted(token for token, count in c1.items() if c2[token] < count)
    if missing:
        result.add_error(f"Inline code not preserved exactly: missing={missing}")


def validate_env_vars(orig, comp, result):
    e1 = extract_env_vars(orig)
    e2 = extract_env_vars(comp)

    if e1 != e2:
        result.add_error(f"Environment variable mismatch: lost={e1 - e2}, added={e2 - e1}")


def validate_commands(orig, comp, result):
    c1 = extract_commands(orig)
    c2 = extract_commands(comp)

    if c1 != c2:
        result.add_error("Standalone command lines not preserved exactly")


def validate_bullets(orig, comp, result):
    b1 = count_bullets(orig)
    b2 = count_bullets(comp)

    if b1 == 0:
        return

    diff = abs(b1 - b2) / b1

    if diff > 0.15:
        result.add_warning(f"Bullet count changed too much: {b1} -> {b2}")


# ---------- Main ----------


def validate(original_path: Path, compressed_path: Path) -> ValidationResult:
    result = ValidationResult()

    orig = read_file(original_path)
    comp = read_file(compressed_path)

    validate_headings(orig, comp, result)
    validate_code_blocks(orig, comp, result)
    validate_inline_code(orig, comp, result)
    validate_urls(orig, comp, result)
    validate_paths(orig, comp, result)
    validate_env_vars(orig, comp, result)
    validate_commands(orig, comp, result)
    validate_bullets(orig, comp, result)

    return result


# ---------- CLI ----------

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python validate.py <original> <compressed>")
        sys.exit(1)

    orig = Path(sys.argv[1]).resolve()
    comp = Path(sys.argv[2]).resolve()

    res = validate(orig, comp)

    print(f"\nValid: {res.is_valid}")

    if res.errors:
        print("\nErrors:")
        for e in res.errors:
            print(f"  - {e}")

    if res.warnings:
        print("\nWarnings:")
        for w in res.warnings:
            print(f"  - {w}")
