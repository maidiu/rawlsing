# Actual Python tests, mutations and restore

## 1. Environment and candidate source

```text
Device: oldMac
OS: macOS 13.7.8 x86_64
Python: 3.11.3
pytest: 9.1.1
Candidate:
SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/WORKING_O_INDEX_CANDIDATE_R1
Review subject: 96af4f15c993c7a4f32da4cc31ef3175903a0d5c
Commission head: bc8cfb77a8fbae1f37e7b2086839e19c71d07513
```

Candidate hashes before and after all review activity:

```text
01_SOURCE_OF_TRUTH_REGISTRY.json
e01207908cf2d9b3aecd8dff8d4706abc31a82cf8d4ae96ddc5760bd67d7657e
02_L0_L5_LINKED_ORCHESTRATION_INDEX.json
27c118e073343664e12d19e5a304689245904e87d99ce7843aeabd2895900a45
validate_index.py
7caa5665ab3058762342fce79af8ce6b3952c2779d26935b78a36ead5a4ea5e6
test_validate_index.py
e35c9280ec12af0479ce8c6dd057b08444d6bbe4bc8b0758f01bd8fae93a0ecb
```

All mutations were performed in temporary copies. The candidate was not
modified. The final original-candidate validation returned `PASS`.

## 2. Intact validator and tests

```sh
PYTHONDONTWRITEBYTECODE=1 python3 validate_index.py \
  --output /tmp/oindex-validation.json
```

Exit `0`. Result `PASS` with:

```text
sorok_rows=144
pyat_rows=23
pyat_f_gates=8
four_assets=4
l3_nodes=74
edges=431
traversals=3
owner_slots=40
priority_decisions_made=0
typed_index_cycles=66
```

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -o addopts='' -q test_validate_index.py
# 9 passed
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_validate_index.py
# Ran 9 tests in 0.192s — OK
```

The 9 tests are one positive and eight mutation tests. The package’s
`05_VALIDATOR_AND_READBACK.md` still reports an old seven-test/six-mutation/
188-node/414-edge result; that text is stale and is not cited as proof here.

## 3. Required adversarial mutations

Each run copied the candidate into a temporary directory and called the
candidate validator.

| # | Mutation | Result | Claimed reason |
|---:|---|---|---|
| 1 | `S0.evidence_source = None` | **REJECTED** | `S0: missing evidence source` |
| 2 | `S16.evidence_source.blob = 0*40` | **REJECTED** | `S16: exact program-map blob` |
| 3 | blank source metadata timestamp | **REJECTED** | `S0: source time/currentness` |
| 4 | `A5.native_product_accepted = true` | **REJECTED** | `A5: native promotion` |
| 5 | remove required `A5` row | **REJECTED** | `expected 144 Sorok rows, got 143` |
| 6 | remove `PYAT_N12` row | **REJECTED** | `expected 23 Pyat rows, got 22` |
| 7 | remove `M01` dependency edge | **REJECTED** | `orphan L3 functions: ['M01']` |
| 8 | claimed source-to-consumer path with fabricated non-S source | **PASSED — DEFECT** | validator did not compare the path/blob to Git |

Mutation 8 used a real metadata commit (`5fc1d43e…`) with
`path=FORGED/NOT_A_SOURCE.py`, `blob=1*40`, and
`first_consumer=ADOPTED_NATIVE_CONSUMER_WITHOUT_SOURCE` on `A5`. The validator
returned `PASS`. This is the exact required negative that must fail and does
not.

## 4. Additional source-fidelity mutations

| Mutation | Result | Meaning |
|---|---|---|
| non-empty forged timestamp `FORGED_TIMESTAMP` on a real metadata commit | **PASSED — DEFECT** | timestamp is checked only for non-empty, not Git equivalence |
| `PYAT_N11` source path `NOT_A_PYAT_SOURCE`, blob `2*40`, real commit | **PASSED — DEFECT** | Pyat source path/blob not compared to Git |
| forged metadata path `FORGED_PATH` | **PASSED — DEFECT** | metadata path is not checked |

The validator therefore proves internal consistency, but not source-object
identity, despite the source-exact map claim.

## 5. Static source audit

The registry’s own source fields were independently checked against Git:

- `136/144` Sorok rows resolve to an existing commit/path and (where present)
  blob.
- `3` Sorok rows use a path absent at the stated commit:
  `B3A`, `B3AS`, `S39_S52`.
- `5` Sorok rows have `blob = null`:
  `B1`, `B2`, `B3`, `BP2P4J`, `R15_V2`; the first four resolve to actual blobs,
  while `R15_V2` is a tree path.
- All `23/23` Pyat source paths and blobs resolve to Git. A forged path/blob can
  still pass the validator, because it only checks presence/format.

Exact actual corrections and path evidence are in
`03_WHOLE_PRODUCT_MAPPING_PATH_ADVERSARIAL_REVIEW.md`.

## 6. Restore

After all temporary mutations, the original candidate was revalidated:

```text
RESTORE_VALIDATE PASS
counts: 144 rows, 23 Pyat rows, 4 assets, 74 L3, 431 edges,
        3 traversals, 40 slots, 0 priority decisions, 66 typed cycles
```

The original candidate source hashes above are unchanged.

## 7. NOT_RUN

- Full original R6/R7 branch test suites; only R6/R7 source/return evidence was
  read.
- Four returned asset test suites: CP-A5-R2, C9C12-R2, B-F1CR-R2, V3CORE-R1.
  Counts are cited only from their author returns and remain unpooled.
- Any native source, survey, provider/model call, production import, PRE-MAIN
  mutation, branch rewrite or candidate code execution.
- The old `VALIDATION_RESULTS.json` / `VALIDATOR_TEST_RESULTS.txt` are not used
  as proof of the corrected candidate; only the fresh runs above are.
