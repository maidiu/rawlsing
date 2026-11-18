# SRC04 q217 successor config v3 — provenance correction

## Verdict

**Corrected actual v3 is published as a selectable successor, not live-selected.**

The physical SAV metadata field `physical_slots` is now **byte-equivalent in
content to exact repaired-v2**. In particular:

- q217 physical value labels remain v2's `10.0 = others`;
- q217 physical value labels contain **no `7.0` label**;
- code 7 remains a distinct raw `SOURCE_SPECIFIC_SPECIAL` response rule in the
  q217 source mapping;
- the questionnaire `7 = Other` corroboration is kept separately in pinned
  page-5 evidence, not embedded in physical SAV metadata;
- code 10 remains distinct (`others`), with no equivalence to 7;
- code 99 is `REFUSAL`; 97/98 are `DK`; no stored value is `MISSING`.

## Exact corrected v3

- Base v2 commit: `da23c65d1e211cb7e8ce416e98757f321b78d25e`
- Base v2 path: `rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json`
- Base file SHA-256: `5e107de4baf43f11a2a3e739e05481d8008de6f90951e86a170fb4d804ef3ff5`
- Base canonical SHA-256: `28630f26b491dcbce411667e3ad285ea42b40abf2d0176056a8a15d1ecad768d`
- **v3 path:** `WORKER_RETURNS/ANVIL_SRC04_Q217_MAPPING_20261118/source.config.repaired.v3.json`
- **v3 file SHA-256:** `f007afdc0cbcd58a3f856121e265a5069f2145cce6c9ce0c112aff1f9c7d7855`
- **v3 canonical SHA-256:** `a3d3267cc37f7f6d2f6267d777c414f285be58ff5e7ea88b8bc9ac0d74c1269f`

`successor_reference.json` is the selectable input reference with scope
`Q217_ONLY__PHYSICAL_METADATA_EXACT_V2__NO_LIVE_SELECTION`.

## Field-level diff

- **physical_slots:** 181/181 unchanged content, byte-equivalent to v2.
- **q217 `value_labels`:** exact v2 labels; no 7; 10=others.
- **response_slots:** one q217-only change:
  - add raw `7.0` as `SOURCE_SPECIFIC_SPECIAL`, canonical `None`;
  - change raw `99.0` to `REFUSAL`, canonical `None`.
- identity, binding, questions, coordinates, weights, routing: unchanged.
- response slots 177/177 non-q217 unchanged.
- no additional fields.

Evidence: `evidence/q217_v3_validation.json`.

## Questionnaire label provenance

Primary local source scan, PDF page **5** (1-based), q217:

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

- PDF SHA-256: `0814f77bcfdad3c78d5e46f49012437f25ddcbfe8bea3e565d7a26874bab4118`
- Page render SHA-256: `11c622bf4b173c9036c0a86d6a7cfbc223f4abe60d79f97f8057119082586c75`
- Use scope: source-label corroboration only; no respondent data, no
  cross-wave/frequency inference.

The processed physical labels/codebook list `10 = others` and omit 7. Both are
recorded; v3 does not embed the questionnaire 7 label into physical metadata
and does not equate 7 and 10.

## Native tiny synthetic exact-cell proof

The synthetic witness now consumes the **actual v3 q217 response rules** and
projects twelve tiny exact cells (1,2,3,4,5,6,7,10,97,98,99,None):

| raw | state | canonical |
|---:|---|---|
| 1 | SUBSTANTIVE_RESPONSE | `"1"` |
| 7 | SOURCE_SPECIFIC_SPECIAL | None |
| 10 | SUBSTANTIVE_RESPONSE | `"10"` |
| 97 | DK | None |
| 98 | DK | None |
| 99 | REFUSAL | None |
| None | MISSING | None |

Raw 7 is retained as float64 bits `401c000000000000`. The synthetic witness
does not claim physical SAV label 7.

Evidence: `evidence/q217_native_witness.json`,
`evidence/q217_native_witness.out`.

## Corrected aggregate receipt

- 7,337 total rows
- 7,112 processed-label cells
- 38 unlabeled processed code-7 cells
- 187 system-missing cells
- 7,150 physically observed storage cells, of which 38 are unlabeled

`receipt.json` status is corrected to
`SELECTABLE_V3_Q217_SPECIAL__PHYSICAL_METADATA_BYTE_EQUIVALENT_TO_V2__NOT_LIVE_SELECTED`.
The old candidate validation is retained only as prior evidence; actual v3 is
the corrected successor above.

## Reproduction

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B \
  WORKER_RETURNS/ANVIL_SRC04_Q217_MAPPING_20261118/q217_v3.py

PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B \
  WORKER_RETURNS/ANVIL_SRC04_Q217_MAPPING_20261118/q217_native_witness.py

PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q \
  -o addopts='' -p no:cacheprovider \
  WORKER_RETURNS/ANVIL_SRC04_Q217_MAPPING_20261118/tests
```

Tests: **6 passed in 0.07 s**.

## Boundaries

- Original `.sav` untouched; no additional source-body read/hash.
- Running construction witness and live shared config selection untouched.
- No product/protected/config-custody edits.
- No respondent records, IDs, individual values, row combinations or samples
  emitted.
- No canonical/scientific/rights promotion; no large build.
