# RRIF validation and receiver proof

**Status:** WORKING CANDIDATE — NOT HQ-ADJUDICATED.

## Executed commands

```sh
python3 validators/build_ledger.py \
  --s7fix /tmp/s7fix_corrected.json \
  --out WORKER_RETURNS/RRIF-FINAL-ESTATE-FUNCTIONAL-DISPOSITION-R1
# exit 0
# 1885 families, 3135 function IDs, 2595 negatives, 845 branches, 838 tips

python3 validators/validate_rrif.py \
  --root WORKER_RETURNS/RRIF-FINAL-ESTATE-FUNCTIONAL-DISPOSITION-R1 \
  --s7fix /tmp/s7fix_corrected.json \
  --output VALIDATION_SOURCEFREE_RESULTS.json
# exit 0; result PASS

cd validators && python3 -m unittest -v test_validate_rrif.py
# exit 0; 7 tests OK
```

Machine output: `VALIDATION_SOURCEFREE_RESULTS.json`, `VALIDATION_SOURCEFREE_TEST_RESULTS.txt`, `LEDGER_BUILD_SUMMARY.json`, `POST_S7FIX_RETURN_NEGATIVES.jsonl`.

## Exact input custody

| Input | Exact identity |
|---|---|
| S7FIX return | `80bc5d9bf6624c2ea04027322947a41c347330aa` |
| S7FIX corrected artifact blob | `743f79e2e618d3e5f083c6033ba9f37f0d4c4c07` |
| S7FIX corrected artifact SHA-256 | `f7b7d4eeca135295f3d29571a13e076486be31ffab314e7308ae5e68316a71df` |
| S7FIX I3 hostile | `1b89fd49c330e4a2c976e6af8d6c1a5e6dbfb088` |
| PRE-MAIN | `8e44ca9c751049d65e6def47600b5c073ee04b29` |
| `rawlsing_next` tree | `1d88d3fbb1d18dadfda946d9cd7f309d84afa479` |
| C3/R9 | `24847592f6a40fde3c4932d0f26173012c037078` |
| P41/R08 | `aa6ca0d700f10bc349a98d98c4239c554ca221f8` |
| F7/P07 | `f8fe03cc6e6a482f428bed9e03c08e50ce1e6479` |
| PE successor | `a48c6acb7e0d3e0610dd0bc0e7b4ba2c09250253` |
| PE hostile | `33b5363a20d44cfb42b3d1e86fdb9615710adb23` |

The 47 MB artifact was read as an external source object; it was not copied into PRE-MAIN or the return tree. `FUNCTION_ID_CUSTODY.jsonl` and `BRANCH_ROSTER_845.json` carry the exact per-ID and per-branch custody.

## What passed

- 1,885/1,885 family dispositions; 3,135/3,135 exact-once IDs; 3,135/3,135 variant comparisons; 2,595/2,595 S7FIX negative records plus 8 post-S7FIX return negatives.
- 845 branch names and 838 distinct tips.
- 11 corrected boundary families: 5 outer, 5 nested, 1 join.
- No `ADOPT`, `ADAPT_MINIMAL`, native acceptance, science issuance, production receiver or fan-in accepted.
- Current path blobs in the ledger match PRE-MAIN `8e44ca9c` (checked with `git ls-tree --full-tree`).
- Six boundary owner mapping remains RED: outer AST differs, nested owner absent, emit differs.
- External zero-member families are retained but excluded from the 3,135 ID set.
- Negative records retain source object and raw finding payload.

## Current receiver proof

The ledger reports 892 families with at least one current path blob, but **0** with a proven production receiver. The distinctions are:

- `ALREADY_CURRENT` (101): exact historical source blob at PRE-MAIN; no import/adoption implied.
- `CURRENT_DIFFERENT` (80): current path exists but historical AST/implementation differs.
- `CURRENT_TEST_ONLY` (3): current references are tests only.
- `NO_REAL_RECEIVER_VERIFIED` (79): references exist but no actual caller/receiver.
- `HISTORICAL_ONLY` (95) and `NOT_RESOLVED` (149): no current path or unresolved ownership.
- `EVIDENCE_ONLY` (841): test/evidence function with no production function.

The six S7 boundary families are not allowed to use the S7FIX current mapping:

| Boundary class | Current result |
|---|---|
| Outer `SourceRelationResolver` (5) | current outer path `5b67e3f9…`; AST differs from historical; test-only/no production import |
| Nested `_make_sealed_source_relation_owner` (5) | no current nested owner; historical only |
| Joined `PhysicalSourceIncidence.iter_batches.emit` (1) | current `8732e34d…`; AST differs; static imports, executed consumer not run |

## Tests run by RRIF vs referenced tests

RRIF executed only its own JSON/JSONL validator and seven unit tests. It did **not** execute historical branch code, native P07, original survey/respondent data, actor/world code, or any recent author test suite. The ledger records `rrif_run: []` for every family.

Author-reported/referenced receipts (not accepted here):

- C3/R9: C3 55/55, G01 9/9, R9 69/69, current 105/105, custody 51/51, fault negatives 9/9; R9 current-tree cross-check has six named representation failures.
- P41/R08: P41 19/19 and 3/3 witnesses; selected-world 24/24 and exact seam 26/1 RED; bounded repair 5/5; current E03 18/18; C1/N10E/F8 69/69; learned-world 30/30; P41-style current adapter 5/5; R08 staged 113/113 + 8/8.
- F7/P07: historical 49/49 and 163/163; HQ227 134/141 with 7 failures preserved; candidate 24/24 and 2/2 mutations; current source relations 24/24; decoder/custody 73 passed/1 skipped.
- S7FIX: membership validator PASS; self-test 8/8 mutations; I3 exact AST 5/5 outer, 5/5 nested, 1/1 init variant, 4/4 emit variants, current outer 0/5, current nested absent, current emit different.

These are evidence references, not RRIF execution and not independent acceptance.

## Non-actions

No PRE-MAIN write/merge, no source-owner/Sorok write, no production import, no 47 MB source transplant, no historical branch script execution, no native P07/survey/respondent/actor run, no model/account/host switch, no self-review or self-CAS.
