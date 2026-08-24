# Latinobarómetro 1995 p26 — Quarantine and Successor Candidate

## Current state

`Latinobarómetro|1995|p26` is inside QRA700 and is currently marked directional on `representative_responsiveness` toward `deputies_and_senators`.

The source proposition is:

> Which is closer to your way of thinking: 1) The deputies and senators are concerned about what people think or 2) The deputies and senators aren't concerned about what people think

The source response contract is:

- `1` — The deputies and senators are concerned about what people think
- `2` — The deputies and senators aren't concerned about what people think
- `8` — No know (don't read)
- `0` — No answer

The current QRA positive anchor is substantive option 1. The current QRA negative anchor is **option 8**, a source-special non-substantive state. This is unsafe and remains quarantined.

## Bounded successor assertion candidate

Candidate status: `CANDIDATE_ONLY__NOT_INSTALLED`.

- lawful directionality: **YES**
- response geometry: binary substantive contrast signed to the existing `representative_responsiveness` axis
- positive anchor: **The deputies and senators are concerned about what people think**
- negative anchor: **The deputies and senators aren't concerned about what people think**
- special states excluded from sign: `No know (don't read)`, `No answer`
- item reversal: no change required
- current O07 `BINARY_TRADEOFF`: compatible with the corrected two-substantive-option geometry; no O07 correction is counted for p26

The sign is not inferred from codes `1` and `2`. It follows from the named source propositions and the already governed `representative_responsiveness` relation axis. Numeric code order is evidentially irrelevant.

`REC04_P26_DISPOSITION = SUCCESSOR_CANDIDATE__QRA_ASSERTION_DEFECTIVE`
