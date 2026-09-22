# FIABC-QF1 — Combined Source-Independent Qualification Court

## Terminal

`FIABC_QF1_COMBINED_SOURCE_INDEPENDENT_QUALIFICATION_FAIL__EXACT_REPAIR_SET_RETURNED`

Qualification is FAIL. The static identity court passed, but `compileall` and four source-independent test surfaces remain unresolved. No production implementation was repaired during this first pass.

## Exact checkout proof

- Repository: `maidiu/rawlsing`
- Required base branch: `agent/vozhd-premain-fiabc-live-t6-final-implementation-r1`
- Required HQ seal: `44255e97119c83be86cefec032d0f0a244b00258`
- Qualification branch: `agent/rabochii-premain-fiabc-qf1-source-independent-qualification-r1`
- Qualification HEAD at execution: `44255e97119c83be86cefec032d0f0a244b00258`
- Initial working tree: clean
- Checkout source: exact remote HQ branch, because `/Users/matthewsmith/Desktop/Rawlsing` was an artifact directory and not a Git checkout

The checkout was isolated at `/Users/matthewsmith/Desktop/Rawlsing/FIABC-QF1-qualification-checkout`. Only this return packet is committed on the qualification branch.

## Runtime

- Platform: `macOS-13.2.1-x86_64-i386-64bit`
- Python: `/usr/local/bin/python3`, `Python 3.11.3`
- pytest: `9.0.2`
- The commissioned `python` executable is absent (`command not found`). Every Python test/static command was therefore run equivalently with `python3`; the exact `python` static commands are recorded as environment failures in the command ledger.

## Qualification evidence

- Required JSON validation with `python3`: PASS for all five files.
- `python3 -m compileall -q rawlsing_next`: FAIL at `rawlsing_next/ee_p2x_darwin_stage_backend.py:1102` with `SyntaxError: unexpected character after line continuation character`.
- R35-I01: PASS, 6 tests.
- R35-I02: FAIL, 8 tests passed and 1 error.
- R35-I03: FAIL, 2 tests passed and 13 failed.
- R35-Q01 hostile court: PASS, 10 tests and 29 subtests.
- T6 live R35 convergence: PASS, 6 tests.
- T2 execution binding: PASS, 5 tests.
- T3 oracle process envelope: PASS, 6 tests.
- W3-I06A process isolation: FAIL, 8 tests passed and 1 failed.
- T4 live accounting: PASS, 12 tests.
- Telemetry semantics: PASS, 18 tests.
- Lifecycle accounting: PASS, 13 tests and 2 subtests.
- PRE553 independent parity oracle: PASS, 15 tests.
- Succession preflight: PASS, 8 tests.
- I08 terminal verifier: PASS, 13 tests.
- T5 live terminal control: PASS, 12 tests.
- PRE553 authority/query/discovery spine: PASS, 60 tests.
- Additional inventoried W3-I04 runtime packaging/rebind suite: FAIL, 4 tests passed and 2 failed.
- Static identity court: PASS for every row in `FIABC-T6/04_PRESERVATION_AND_IDENTITY_LEDGER.csv`, including all required direct identities.

`PHYSICAL_EQUIVALENCE_PASS`, `SEMANTIC_PASS`, and `SOURCE_CERTIFICATION` were not collapsed by the passing hostile suites. No qualification PASS is claimed.

## Failure clusters

1. **Production syntax / live backend.** The source contains literal backslash-n sequences inside the expression at line 1102. This prevents compileall and causes the two W3-I04 AST-based tests to fail before their assertions. Owner: live backend implementation.

2. **R35-I02 hostile fixture/helper.** `test_forged_derivative_with_correct_asserted_source_sha_is_rejected` supplies a forged object without `source_receipt`, while its `_verify_wvs` helper dereferences `bundle["source_receipt"]["receipt_identity"]` at line 186. The observed error is `KeyError: 'source_receipt'`, before `verify_parentage_bundle` runs. Owner: derivative-parentage hostile fixture/helper; do not weaken the rejection law.

3. **R35-I03 fixture/contract mismatch.** Thirteen tests fail while constructing the expected evidence because `base_evidence()` supplies binary floats `1.0` and `2.0` at `test_fiabc_r35_i03_physical_equivalence.py:66`, and `canonicalize()` correctly raises `Pre553IntegrityError: float/NaN/Infinity forbidden in semantic identity` at `pre553_empirical_objects.py:190`. Owner: R35-I03 fixture/accepted exact-numeric representation. The physical guard assertions were not reached.

4. **W3-I06A test setup.** `test_scratch_and_durable_state_are_cell_local_and_foreign_marker_fails` calls `_controller(tmp_path / "second")`; `_freeze()` writes directly into that nonexistent directory and raises `FileNotFoundError`. Owner: process-isolation test setup.

The complete traceback roots and every failing test identity are in `04_FAILURE_CLUSTER_REPORT.md`.

## Source-independent boundary and exclusions

No LiTS-I raw source, WVS7 raw source, CLOSED_35 carrier, SAV bytes, real six-cell execution, WVS oracle materialization, missing real LiTS-A first-build parentage receipt, R6X reconciliation, or measured P2X was opened or run. The executed suites used repository code and synthetic/hostile fixtures only.

The later local-only physical materialization and real P2 gates are `NOT_APPLICABLE` to this court and are listed with reasons in `01_COMMAND_EXECUTION_LEDGER.csv`.

## Exact repair set returned

1. Repair the literal escaped-newline syntax in the live backend under the accepted T6 contract; do not redesign terminal or accounting semantics.
2. Repair the R35-I02 hostile fixture/helper so the malformed forged derivative reaches the production verifier and is rejected as `ParentageError`; preserve the hostile law.
3. Align the R35-I03 synthetic evidence fixture with the accepted exact-numeric contract without weakening float rejection or semantic/physical boundaries.
4. Repair the W3-I06A test setup to create its second temporary root before writing the freeze receipt; preserve the foreign-state rejection assertion.
5. Re-run the failed suites, affected T1–T6 regression families, compileall, and the static identity court before any ref movement or later local-only gate.

No merge, source materialization, R6X, or measured P2X is authorized by this return.

