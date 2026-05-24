---
name: laconic-stats
description: >
  Shows real token usage and estimated savings for the current session.
  Hook-driven — the model does not compute these numbers.
  Trigger: /laconic-stats, /laconic-stats --share
---

# Laconic Stats

When `/laconic-stats` is typed, the hook intercepts the prompt, reads the session log directly, and returns formatted stats. **No model turn is consumed — the response is instant.**

## Output

```
laconic-stats  [terse mode]
───────────────────────────────────
turns          12
output tokens  1,840
estimated saved ~1,200 tokens  (~65%)
USD saved      ~$0.0036
model          claude-sonnet-4-6
```

## Flags

| Flag | Effect |
|------|--------|
| `/laconic-stats` | Full stats card for current session |
| `/laconic-stats --share` | Single-line summary (tweet-friendly) |

## How savings are estimated

Savings are estimated from the active Laconic mode's compression ratio applied to measured output tokens:

| Mode | Estimated reduction |
|------|-------------------|
| terse | ~65% |
| balanced | ~45% |

These are estimates based on observed averages, not exact measurements.

## Relationship to RTK

RTK (`rtk gain`) tracks token savings on shell command output — the tool-use side of a session.
`laconic-stats` tracks output token savings on model responses — the prose side.
They measure different things and complement each other.

## Notes

- Stats cover the current session only. Lifetime tracking is not yet implemented.
- If no session data exists yet, a brief message is shown instead of stats.
