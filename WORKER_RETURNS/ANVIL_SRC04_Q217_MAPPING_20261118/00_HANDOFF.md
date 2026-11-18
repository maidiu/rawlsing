# SRC04 q217 successor config v3

## Result

**A real selectable successor config was materialized:**
`source.config.repaired.v3.json`

It is an additive artifact under this owned mapping return. It is **not**
selected as the live all-35 SRC04 config, and the original `.sav` is untouched.

## Exact successor

- Base v2 commit: `da23c65d1e211cb7e8ce416e98757f321b78d25e`
- Base v2 path: `rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json`
- Base file SHA-256: `5e107de4baf43f11a2a3e739e05481d8008de6f90951e86a170fb4d804ef3ff5`
- Base canonical SHA-256: `28630f26b491dcbce411667e3ad285ea42b40abf2d0176056a8a15d1ecad768d`
- **v3 path:** `WORKER_RETURNS/ANVIL_SRC04_Q217_MAPPING_20261118/source.config.repaired.v3.json`
- **v3 file SHA-256:** `5aeca1d70d2de1148c7f6aff163eeef2a3cefc3a034297e7f90ec77ed7ff3d71`
- **v3 canonical SHA-256:** `323c1447e76ad447163514f6805c26f4b7033cd34f042d1b59bee91f2274a70c`

`successor_reference.json` is the frozen selectable input reference with the
explicit scope and the instruction:

`DO_NOT_REPLACE_LIVE_SHARED_CONFIG_SELECTION_BEFORE_RECEIVING`.

## Only q217 changed

- `7.0` added to q217 labels as **Other**, from the primary source
  questionnaire scan, PDF page **5**, q217 line.
- `7.0` added as a q217 response rule:
  `SOURCE_SPECIFIC_SPECIAL`, no canonical value, no missing/refusal claim.
- `99.0` changed from `SUBSTANTIVE_RESPONSE` to **REFUSAL** using the exact
  “decline to answer” source label; canonical value cleared.
- `97.0` and `98.0` remain **DK**.
- no stored-value cell remains **MISSING**.
- known substantive codes 1,2,3,4,5,6,10 remain unchanged.
- all 180 non-q217 physical slots are unchanged.
- 177 non-q217 response slots are unchanged.
- identity, binding, questions, coordinates, weights and routing are unchanged.

Field-level evidence: `evidence/q217_v3_validation.json`.

## Questionnaire check

The prior attempt only tried text extraction, which yielded nothing. The
primary local source scan was rendered from PDF page 5 and OCR-checked at
300 dpi. Exact lines include:

```text
217q | What are your first and second most important sources
1= Television
2 = Radio
3 = Local newspaper
4 = Weekly magazines and papers
5 = Internet
6 = SMS Messages
7 = Other
97 = Not clear
98 = Can't Choose/Don't know
99 = Decline to Answer
```

- PDF: `data/Arabbarometer/ABI_Questionnaire_ENG.pdf`
- PDF SHA-256: `0814f77bcfdad3c78d5e46f49012437f25ddcbfe8bea3e565d7a26874bab4118`
- Page: **5 (1-based)**, 300 dpi rendered page SHA-256
  `11c622bf4b173c9036c0a86d6a7cfbc223f4abe60d79f97f8057119082586c75`.
- Explicit use scope: source-label corroboration only; no respondent data, no
  cross-wave or frequency inference.

There is a real source-document conflict: the physical SAV labels and processed
codebook list code `10.0 = others` and omit `7.0`, while the primary
questionnaire page lists `7 = Other` and no 10. v3 records both and does not
erase the conflict. Code 7 is retained as a source-specific special category,
not silently made a substantive analytical case.

Evidence: `evidence/questionnaire_q217_scan.json`.

## Corrected aggregate receipt

The frozen aggregate remains:

- 7,150 physically observed storage cells
- **7,112 cells with processed labels**
- **38 unlabeled observed cells = exact code 7.0**
- 187 system-missing cells (`None`)
- total 7,337

The prior receipt’s “7,150 labeled” phrasing is corrected in `receipt.json`.
The 38 unlabeled cells are now explicitly resolved to **7 = Other** only by
the primary questionnaire evidence; the historical aggregate classification is
not silently relabeled.

## Native tiny synthetic exact-cell witness

No additional source body was opened, hashed or read. A tiny synthetic
exact-cell stream was projected through the current native C11 facade using
mirrored v3 q217 states:

- raw 1.0 → `SUBSTANTIVE_RESPONSE`, canonical `"1.0"`
- raw 7.0 → `SOURCE_SPECIFIC_SPECIAL`, canonical `None`
- raw 98.0 → `DK`
- raw 99.0 → `REFUSAL`
- no stored value → `MISSING`

Raw 7 identity is retained as float64 bits `401c000000000000` in the event
witness; it is not relabeled in the raw carrier.

Evidence: `evidence/q217_native_witness.json`,
`evidence/q217_native_witness.out`.

## Reproduction

```bash
# Materialize and validate v3 from exact v2
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B \
  WORKER_RETURNS/ANVIL_SRC04_Q217_MAPPING_20261118/q217_v3.py

# Native synthetic exact-cell projection (no original source)
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B \
  WORKER_RETURNS/ANVIL_SRC04_Q217_MAPPING_20261118/q217_native_witness.py

# Tests
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q \
  -o addopts='' -p no:cacheprovider \
  WORKER_RETURNS/ANVIL_SRC04_Q217_MAPPING_20261118/tests
```

Tests: **6 passed in 0.07 s**.

## Boundaries

- Original `.sav` and running construction witness untouched.
- No additional original survey body opened, hashed or read.
- No reread/rerun of the aggregate source check.
- No live config selection replacement.
- No product/protected/config-custody changes.
- No canonical/scientific/source-rights promotion.
- No large build, broad profiling, or second inventory.

**Exact held issue:** v3 is selectable but not live-selected; the source
questionnaire/physical-codebook conflict for q217 code 7/10 remains explicitly
recorded for receiving review.
