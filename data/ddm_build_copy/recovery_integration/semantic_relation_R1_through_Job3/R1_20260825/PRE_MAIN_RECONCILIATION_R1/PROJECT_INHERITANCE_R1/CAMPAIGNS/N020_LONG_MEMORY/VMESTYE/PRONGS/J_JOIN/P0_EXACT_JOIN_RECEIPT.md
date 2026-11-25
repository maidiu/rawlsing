# ZL-15 R2 five-tuple P0 join audit (documentary only)

- Accepted P0 original census: **6,125 unique exact five-tuples** at blob `65c1bbe4a602341c5caacca2d58dced31a23f382`.
- 13 independently received prongs: **2,607** coverage observations, **2,496** distinct source five-tuples; exact match checks performed on `(estate_id, source_commit_sha, source_path, source_composite_id, source_grain=record_grain)`, with zero P0 tuple collisions and zero mismatched census IDs.
- **1,962** observations exactly match P0; **1,869** distinct P0 exact identities; **88** P0 identities repeat across prong coverage, contributing **93** repeated observations. Repetition is not a new function or proof.
- **645** observations do not match P0, representing **627** distinct outside-P0 identities. They remain typed outside-P0 observations; their local source existence may be documented but they are **not** promoted into the P0 census and cannot be counted as native proof.
- Thus `2,607 = 1,962 + 645` and `2,496 = 1,869 + 627`. The original 6,125 P0 census records are not replaced, expanded, or merged by this candidate.
- Original 2026-11-09 independent gate: issue #813 / PR #859 R5 `449a97480dfa5c9f7f2042d688fe1ed1869ffe91`, `ACCEPT_P1_PRONG_EVIDENCE` **only S0–S1**.
- Status: **author-computed S0–S1 reconciliation**, separately reviewable by #815/#816. This check does not establish same-meaning succession, authority effect, non-test first reader, source-native S2/S3, or protected adoption.
- Every coverage observation has a keyed auditable result in `P0_EXACT_JOIN_AUDIT.tsv`; `FULL_ID_ANTI_JOINS.tsv` has its `p0_tuple_check` values rewritten without discarding a row or modifying other fields.
