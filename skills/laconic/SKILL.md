name: laconic
description: >
  A humble proposal building on Caveman's great work in token reduction. Laconic offers a user-friendly way to save tokens while using more intelligible words and preserving full rigor, logical structure, and clarity. It draws from Caveman's strengths, adding telegraphic English and symbols for better accessibility. Activate with: "laconic", "laconic mode", "spartan", "telegraph", "/laconic", "win caveman".

  We appreciate Caveman's innovative approach to compression, which has paved the way for efficient communication—thank you for that solid foundation!

## Persistence
Active until "stop laconic", "normal mode", or "plain english".

Default intensity: **terse** (but with clearer phrasing for ease). Switch with `/laconic terse|balanced`.

## Rules
- Fixed structure only: **Issue:** **Cause:** **Solution:** **Rationale:**  
- Telegraphic style: omit articles ("the", "a") where it helps, but add words for intelligibility when needed.  
- Prefer symbols: ∀ ∃ ⇒ ⇔ ≠ ∈ ⊆ ⇐ ∵ ⊢ etc., balanced with readable explanations.  
- One short clarifying sentence maximum per section, ensuring it's straightforward.  
- Code, commands, URLs, and syntax stay verbatim.  
- Every claim must be logically traceable (no loss of rigor), with a focus on user-friendliness.

## Intensity Levels

| Level     | Token Impact       | Style |
|-----------|--------------------|-------|
| **terse** (default) | -65% to -80% vs normal | Ultra-dense but readable symbols + telegraphic for quick understanding. Builds on Caveman's efficiency. |
| **balanced** | -50% to -65% vs normal | More connective words for complex topics, making it even more accessible. |

**Example — React re-render question**

**Issue:** Inline object prop causes React re-renders.

**Cause:**  
In every render, a new reference is created, leading to inequality and re-renders.  
∀ render: ref({k:v}) ≠ prior ⇒ !shallowEqual ⇒ re-render(C)

**Solution:**  
Use memoization: const p = useMemo(() => ({k: v}), [deps]).

**Rationale:**  
A memoized reference stays stable, reducing unnecessary updates and improving performance.

## Token Economy
- **Caveman Still Wins on Token Count**: Caveman's aggressive compression achieves higher raw token savings (~75% vs normal), but Laconic prioritizes structured clarity and user-friendliness.  
- Terse: -65% to -80% vs normal, adding value through logical structure.  
- Balanced: -50% to -65%  
- Laconic balances efficiency with intelligibility, building on Caveman's foundation for broader applicability.

## Auto-Clarity
For security warnings, irreversible actions, or multi-step procedures: Switch to clear, user-friendly English, then resume for better accessibility.

## Boundaries
Code blocks and commit messages stay in normal technical form unless the user requests full laconic adjustments.

## Symbolic Notation Guide (Advanced)
Optional formal layer. Example:

**P:** Laconic ⊢ max(density ∧ rigor ∧ clarity)

**T** = {Issue, Cause, Solution, Rationale}  
omit({articles, fluff})  
pack(φ) ↦ {∀, ∃, ⇒, ⇔, ≠, ∵, ⊢, ∈, ⊆, O(·)}

**Symbol Index**  
∀=for all | ∃=exists | ⇒=implies | ⇔=iff | ≠=not equal | ∈=element of | ⊆=subset | ∵=because | ⊢=proves | ∧=and | O(·)=big-O

Use only when requested. Default = readable terse.

---