# SRC04 q217 corrected v3 — focused independent review

## Verdict

**`ACCEPT_SCOPED`**

Corrected config commit: `35bb18f8e347efa432ffd7d19af9cb419c1f529f`  
V3 file SHA-256: `f007afdc0cbcd58a3f856121e265a5069f2145cce6c9ce0c112aff1f9c7d7855`  
Reviewer: `ses_e30c25800ffeT8XbyTuHekRCme` — distinct nonauthor.

## Findings

- Exact v3 file hash verified.
- Retained questionnaire page 5 says q217 `7 = Other`; retained physical SAV
  metadata says `10.0 = others` and has **no 7.0 label**. v3 does not overwrite
  or merge these labels.
- v2 vs v3: only `response_slots` q217 changes. All 181 physical slots are
  byte-equivalent; 177 non-q217 response slots unchanged.
- q217 actual v3 rules:
  - raw 7: `SOURCE_SPECIFIC_SPECIAL`, canonical `None`; raw float64 bits
    `401c000000000000` retained;
  - raw 10: `SUBSTANTIVE_RESPONSE`, canonical `"10"`; separate from 7;
  - raw 99: `REFUSAL`, canonical `None`;
  - raw 97/98: `DK`, canonical `None`;
  - stored missing: `MISSING`, canonical `None`.
- Questionnaire 7 provenance remains evidence, not a physical SAV label.
- The independent native synthetic exact-cell projection consumed the actual v3
  q217 response rules and produced 12 events with the expected states; no
  canonical promotion of raw 7.
- Focused tests: **6 passed**, exit 0, 0.06 s.

No live selection was changed; v3 remains a selectable successor only. No
product/protected edit, original survey opening/decoding, raw source read, new
architecture, matrix, or 177-field build comparison was performed. That frozen
build comparison remains separate.

Artifacts: `REVIEW_VERDICT.json`, `SOURCE_PINS.json`, `SOURCE_CHECKS.tsv`,
`rawcommands.txt`, retained questionnaire/physical/codebook evidence, independent
native witness, v2/v3 diff, tests, and exact v3 snapshot. Publish and verify.
