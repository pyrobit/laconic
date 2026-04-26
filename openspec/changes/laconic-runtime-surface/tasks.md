## 1. Canonical runtime model

- [x] 1.1 Define canonical Laconic runtime modes in shared hook/config code.
- [x] 1.2 Update runtime command parsing to accept `/laconic*` as the public commands and persist canonical Laconic state.
- [x] 1.3 Ensure per-turn reinforcement and session-start guidance use canonical Laconic naming and skip auxiliary modes correctly.

## 2. Badge and command surface

- [x] 2.1 Update statusline renderers to show `[LACONIC]` and `[LACONIC:<MODE>]` from canonical mode values.
- [x] 2.2 Update built-in command metadata, plugin prompts, and setup nudges to advertise `/laconic`, `/laconic terse`, `/laconic balanced`, and Laconic-branded auxiliary commands.
- [x] 2.3 Verify canonical Laconic commands produce Laconic-branded badge output and canonical stored mode values.

## 3. Docs and follow-through

- [x] 3.1 Update runtime-facing docs and installer messaging so Laconic commands are the only documented runtime commands.
- [x] 3.2 Add or update tests/verification steps for canonical command parsing and badge rendering.
- [x] 3.3 Review deferred follow-ups for advanced-mode handling (`wenyan*`, runtime help ergonomics) and capture any out-of-scope work separately.
