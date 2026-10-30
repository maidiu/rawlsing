# H04 hostile code and runtime review

## Reviewed identity

- H03 commit: `b26e4cab577bb33d0d80489322c0c4efebd2df17`.
- Parent: `2e3e3dece53fbfdd2a419e4cd538559b8b9ed1d7`.
- Changed production/test files:
  - `rawlsing_next/wave1_gt12_i03_positive_facts.py` — blob `2a0c47cc5f727a9d5269244da24ab28257009d06`.
  - `rawlsing_next/pre553_retained_gt2_analytical_preparation.py` — blob `e73a5d6a2ca8763fdaafca9a8d8486d5c7def038`.
  - `rawlsing_next/tests/test_pre553_retained_gt2_n10e_analytical_preparation.py` — blob `c02cdf5a8b2e28737051034e2a0f8b9214a28a64`.
- The diff from H02 is 11 added files and 2,787 insertions; no existing file is modified except the additive `wave1_gt12_i03_positive_facts.py` helper/export.

## Code review

### Modified I03 adapter

The only change to an existing production module is:

- import `SimpleNamespace`;
- add `reconstruct_gt2_risk_cohort_predicate`;
- export it in `__all__`.

The helper validates the exact query/fact types, query/fact linkage, predicate/risk-set identity, target order `[Q86B, Q86A]`, one query authority, one universe, 19,210 risk members and denominator support. It reconstructs the predicate with the existing owner's `_predicate_for_members` law and requires the resulting identity to equal both the query and fact predicate refs. It does not call `execute_empirical_query`, open source material, or create a rule/authority. The diff does not change any existing function body.

### New preparation module

`load_retained_gt2_analytical_preparation()` takes no arguments. It:

1. loads the exact fixed committed GT2 query/fact through the existing loader;
2. checks query/fact/replay/predicate identities against the pinned constants;
3. reconstructs the exact predicate and checks `bd91b405…`;
4. calls the existing Field Forge owner with `STRUCTURAL_MEDIATION_INPUT` and Q86B→Q86A;
5. verifies 36 joint cells, 19,210 support, six rows and the six denominators;
6. exposes a deterministic content-addressed preparation with typed-null provider/consumer/replay fields;
7. refuses the N10E route with six exact missing determinants.

There is no `os.environ`, `getenv`, caller path, caller geometry, caller probability, mutable global cache or alternate engine in the new module. The only file reads are through the existing fixed-transport loader. The preparation is deterministic: two loads produce the same `preparation_ref` (`0ef9fc9c1ce71f53c802a195584782ecb813d015b505c80bb4450bf4d119e101` in this run).

### Non-blocking observations

1. `_value_bearing_leaf_count` duplicates the composition owner's leaf-law logic instead of importing a shared helper. For this exact predicate it is verified equal to `composition._actual_leaves(predicate) == []`, so the current result is correct. Future law drift could desynchronize the reporting count; the test would not necessarily catch it unless the same predicate changes.
2. `N10EDeterminant.ref_or_null` and `joint_cells` hold mutable mappings inside frozen dataclasses. The preparation is internally constructed and not exposed as an authorization boundary, but a caller could mutate a nested mapping and change `preparation_hash` after construction. This is a hardening opportunity, not an observed acceptance bypass.

Neither observation changes the verdict.

## Executed tests

All commands were run from the review worktree root with `PYTHONDONTWRITEBYTECODE=1`.

| Court | Command | Result |
|---|---|---|
| H03 preparation | `python3 -m pytest rawlsing_next/tests/test_pre553_retained_gt2_n10e_analytical_preparation.py -q` | **18 passed**, 0 failed/errors/skipped, 63.20 s |
| H02 structural | `python3 -m pytest rawlsing_next/tests/test_pre553_gt2_structural_positive_realization_court.py -q` | **40 passed**, 0 failed/errors/skipped, 116.58 s |
| Synthetic N10E provider | `python3 -m pytest rawlsing_next/tests/test_pre553_empirical_possibility_provider.py -q` | **43 passed**, 0 failed/errors/skipped, 15.72 s |
| Supporting analytical route | `python3 -m pytest rawlsing_next/tests/test_pre553_repo_native_current_rehydration.py rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py rawlsing_next/tests/test_wave1_gt12_a2_real_gt1.py -q` | **25 passed, 1 failed**, 14.17 s |

The single failure is the already-recorded pre-existing A2 RED:

`test_wave1_gt12_a2_real_gt1.py::test_a2_claim_scoped_authorities_bind_actual_release_universe_and_replay`

`GT12BI03BindingError: validated projection domain omits an observed exact source-native response state`.

It reproduces at the untouched parent and is outside H03's retained-fact connection. H03 did not repair it; I did not repair it.

### Sparse-worktree fixture correction

The first provider-court run failed 40/43 with `FileNotFoundError` for exact fixture paths absent from the sparse review checkout:

- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/03_SYNTHETIC_AUTHORITY_FREEZE.json`
- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3/02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json`
- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R8/04_CURRENT_AT07_IDENTITY_SPINE.json`
- `WORKER_RETURNS/PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1/FORWARD_SUCCESSOR_CANONICAL.json` and `REVERSE_SUCCESSOR_CANONICAL.json`

After adding those exact directories to the sparse checkout, 43/43 passed. This is a review-worktree completeness issue, not an H03 implementation defect. The H03 full-worktree evidence is therefore reproducible.

## Evidence identity verification

I recomputed the seven return-artifact SHA-256 values in `05_COMMITTED_FILES_AND_CHECKSUMS.json`; all match. I recomputed the three candidate Git blobs and SHA-256 values; all match. The committed 18-test JUnit has 18 tests, 0 failures/errors/skips and SHA-256 `5dc151a8eb40551cee0e67d8153d8a0a03a61bfbe8e29b30cf3ce9d5f239557c`, matching `05`.

## Independent negative attacks

| Attack | Observed |
|---|---|
| Swapped Q86B/Q86A query through `_new_query` | Refused: `GT12BI03BindingError: fact does not bind the supplied exact query` |
| Tampered `raw_denominator_support` | Refused: `retained denominator support drift` |
| Tampered one 36-cell count | Refused by Field Forge: `joint cell counts do not equal producer raw numerator support` |
| Reverse conditioner/target | Refused: `query target role/order must be exactly [Q86B CONDITIONER, Q86A TARGET]` |
| Non-query object | Refused: `query must be EmpiricalQuerySpec@1.0.0` |
| Fake provider/consumer/replay fields | Refused by `RetainedGT2AnalyticalPreparation.__post_init__`; 18-test court covers all three |
| HQ230 as GT2 authority | Refused by scope; HQ230 is `CANDIDATE_NOT_ADOPTED`, AT07-only |

## Independent measurements

- Predicate: `bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3`, leaf type `DERIVED_BRANCH_COHORT`, value-bearing leaves 0.
- Joint cells: 36; support 19,210; zero cells 23.
- Conditioner denominators: `(6784, 11787, 624, 0, 0, 15)`; sum 19,210.
- Source SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`.
- Preparation ref: `0ef9fc9c1ce71f53c802a195584782ecb813d015b505c80bb4450bf4d119e101` in this environment.
- Relation ref: `1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19`.

## Verdict

ENGINEERING: **PASS / ACCEPT_SCOPED** for the H03 preparation. There is no established implementation defect requiring `H03_INDEX_OR_IMPLEMENTATION_REVISE`. The result remains a preparation, not an N10E consumer execution.
