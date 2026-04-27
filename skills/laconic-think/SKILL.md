---
name: laconic-think
description: >
  Compress internal reasoning while keeping final answers clear. Hidden thinking uses dense
  telegraphic steps inside <think>...</think> or equivalent scratchpad, with fixed structure:
  Issue, Cause, Options, Best, Rationale. Trigger: "laconic-think", "compressed thinking",
  "think laconic", or "/laconic-think". Active until "stop laconic-think" or "normal thinking".
---

# Laconic Think

Compress internal reasoning, not just final output. Final answer stays clear, actionable, and may combine with Laconic output style.

## Persistence

Active until `stop laconic-think` or `normal thinking`.

Default intensity: **terse**. Switch with `/laconic-think terse|balanced|draft`.

## Rules

- Put all internal reasoning inside `<think>...</think>` tags or equivalent hidden scratchpad.
- Use fixed structure only: **Issue:** **Cause:** **Options:** **Best:** **Rationale:**
- Write hidden reasoning in telegraphic + symbolic form. Prefer `∀ ∃ ⇒ ⇔ ≠ ∈ ⊆ ∵ ⊢ O(·)` when they reduce tokens.
- Omit filler, repetition, and full prose inside hidden reasoning.
- Keep hidden reasoning to roughly 30-40% of normal chain-of-thought length.
- Never reveal raw hidden reasoning unless user explicitly asks `show thinking`.
- Final response may be normal or Laconic, but must stay clear and usable.

## Intensity Levels

| Level | Internal Token Target | Style |
|-------|-----------------------|-------|
| **terse** (default) | -60% to -75% vs normal CoT | Ultra-dense symbols + telegraphic |
| **balanced** | -40% to -55% | Short connectors + symbols |
| **draft** | -70%+ | Very short draft steps, then one refinement pass |

## Example Hidden Reasoning

```xml
<think>
Issue: React re-render loop
Cause: ∀ render: ref({k:v}) ≠ prev ⇒ !shallowEq
Options: inline obj / useMemo / useCallback
Best: useMemo(()=>({k:v}),[deps])
Rationale: stable ref ⇒ no spurious render
</think>
```

Final output to user:

**Issue:** Inline object prop triggers re-renders.  
**Cause:** New reference every render.  
**Solution:** `const p = useMemo(() => ({ k: v }), [deps])`.  
**Rationale:** Stable reference prevents needless updates.

## Auto-Safety

For security-sensitive, high-stakes, or long multi-step work: switch to `balanced` or temporarily allow a larger reasoning budget.

## Synergy

- `/laconic-think` compresses internal steps.
- `/laconic` compresses final response.

## Boundaries

- Hidden reasoning stays hidden by default.
- If runtime has no explicit hidden-thought channel, still keep internal notes minimal and never print them unless asked.
