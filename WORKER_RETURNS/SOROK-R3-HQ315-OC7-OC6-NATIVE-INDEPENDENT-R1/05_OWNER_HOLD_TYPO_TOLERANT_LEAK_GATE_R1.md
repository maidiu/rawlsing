# OWNER HOLD — should the test-only leak gate become typo-tolerant?

**Raised by:** HQ315 OC7 independent I2 reviewer, as a typed `OWNER_HOLD`.
**Status:** `UNRESOLVED__REQUIRES_COMPETENT_OWNER_ADJUDICATION`. This is **not** a defect report and **not** a request that any worker implement this.
**Scope:** the bounded TEST_ONLY `detect_leakage` lexical gate in the OC6 custody fixture module.

## What this reviewer decided, and what it deliberately did not decide

The OC5E hostile suite contains two cases that assert a `LeakageError` for inputs whose codepoints
fold to `lowful_answers` and `anseers_key` — not to the denied tokens `lawful_answers` and
`answer_key`. This reviewer verified at codepoint level that the substituted characters are
NFKC-stable lookalikes for the **wrong letters** (`U+03BF`→`o` where `a` belongs; `U+0455`→`s` where
`w` belongs), and concluded the two test inputs are **lexically incoherent upstream fixtures**.

On that basis this reviewer did **not** widen the fold. A substring gate on `lawful_answers`
correctly does not fire on `lowful_answers`, and manufacturing a match would be falsification.

## The wider safety question this reviewer is NOT authorised to close

There is nevertheless a real, legitimate product question hiding here, and it deserves a decision
rather than a silent disposition:

> The current gate is an **exact-substring, bounded-homoglyph** matcher. It catches a caller who
> substitutes a lookalike **character** for a denied token. It does **not** catch a caller who writes
> a **near-miss word** (`ansers_key`, `lawful_answer`, `answer keys`, `answer-key`) by any other means.

Three genuinely different positions exist, and they carry different costs:

1. **Keep exact + bounded-homoglyph only.** Cheapest, zero false-positive risk, and matches the
   documented `TEST_ONLY lexical/schema gate only` scope. Misses near-miss paraphrases.
2. **Add bounded edit-distance / tokenisation normalisation.** Catches near-misses, but expands the
   denial surface and introduces a real false-positive risk against legitimate multilingual text —
   exactly what the current design deliberately avoids. Requires a stated FP budget.
3. **Defer to an actual semantic leakage gate.** This is the only option that would address
   paraphrase-level leakage, and it needs a semantic oracle that **does not exist and cannot be
   fabricated** by a worker or a reviewer.

## Why this cannot be decided here

- Choosing between 1 and 2 is a **product safety/usability trade-off with no test-derived answer**.
  It needs an accepted owner statement about acceptable false-positive behaviour on real
  multilingual respondent text.
- Option 3 is blocked on a **missing semantic authority**, not on engineering effort.
- This reviewer's commission explicitly forbids expanding lexical matching without authority and
  forbids issuing product policy.

## Evidence the owner may wish to weigh

- Against the repaired module, correctly spelled homoglyph spellings of all disputed-target-family
  tokens **are** denied (`l\u03b1wful_answers`, `\u0430ns\u051der_key`, and 6 others).
- 14 safe multilingual / near-miss strings (Russian, Greek, Armenian, Japanese, Arabic, Hebrew,
  Hindi, Thai, Korean, Cyrillic prose, Greek prose, Latin prose, `lowful answers overall`,
  `ansers key`) produced **zero** false positives.
- So the current posture is: **sound, low-recall on paraphrase, and safe against false positives.**

## Requested owner disposition

Choose one, or supply an alternative:

- `H1` — keep the exact + bounded-homoglyph gate as-is; record the paraphrase gap as a known,
  accepted TEST_ONLY limitation. (Reviewer's own read: this is the only option currently supported by
  authority.)
- `H2` — commission a bounded false-positive/false-negative characterisation study against an
  authorised multilingual corpus before any widening. Still no implementation.
- `H3` — defer entirely until a real semantic leakage oracle exists under separate authority.

Until then this gate stays exactly as OC6 left it. **No worker should widen it on the strength of
this hold.**
