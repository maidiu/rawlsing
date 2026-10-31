# R61 current negative and positive oracles; historical V2K dependency

## Current source cut

- Branch base/startup: `87755f02ec5c37499b09e80db6fbdcc9316a6b15`.
- Current PRE-MAIN recheck: `d0342290b257f85c3e8931f9962e0aecabc84ed3`.
- `rawlsing_next` tree: `1d88d3fbb1d18dadfda946d9cd7f309d84afa479` at both cuts.
- Current source blobs:
  - `pre553_issued_workload.py` `31e84f49d624f5524906e9e7839d2873106f8249`
  - `pre553_native_workload_binding.py` `dac73e484f8619088f5c6701b2b6991c07540f3b`
  - `pre553_universal_workload.py` `8e7fe00a3ed008361d9f3c501e7782b2de3a636e`
  - `pre553_source_native_preimage_adapter.py` `a6299c1a6e8b26bd055ced1f49e5b757f20ccd8c`
  - `pre553_source_backed_c11_facade.py` `8a761119e4a8d68eb291fc4edfadb52e027f8284`

## Author 8 current negative oracles

Command, run from the review worktree:

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -m pytest -q -p no:cacheprovider \
  /tmp/opencode/v2k-hostile/test_current_r61_contract_negatives.py
```

Actual result: **8 passed, exit 0**.

| Oracle | Actual refusal |
|---|---|
| Baseline exact TEST_ONLY admission | accepted exact record |
| Foreign issuer / wrong decision ref | `CURRENT_AUTHENTICATED_ISSUER_RECORD_REQUIRED` |
| Removed held row / extra expected job | `EXPECTED_EXECUTED_OPERATION_IDENTITY_MULTISET_MISMATCH` |
| Mutated expected-work identity / envelope | `ENTIRE_EXECUTION_DESCRIPTOR_NOT_THE_ISSUED_ENVELOPE` |
| Wrong role / target-condition direction | `QUERY_TARGET_CONDITION_DIRECTION_MISMATCH` |
| Replay / prior caller receipts | `RESTORE_THROUGH_EXISTING_ISSUED_FACT_RECEIPT_CUSTODY_REQUIRED` |
| Wrong source edition / source factory | `SOURCE_FACTORY_RETURNED_WRONG_EDITION` |
| Severed current resolver | resolver `RuntimeError` is not laundered |

These are current R61 tests. They are not historical V2K tests and do not
establish an original-source positive.

## Current 105 universal tests

Command:

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_universal_grammar.py \
  rawlsing_next/tests/test_universal_workload.py \
  rawlsing_next/tests/test_universal_source_byte_custody.py \
  rawlsing_next/tests/test_universal_source_projection.py
```

Actual result: **105 passed, exit 0** (`136.39s`). This is current universal
module coverage, not a row-level E3 acceptance of all historical branches.

## Independent current sourcefree positive

The author return said full current native positive was `NOT_TESTED`. This court
turned that into an actual sourcefree positive through the current
`NativePreimageBundle`/`NativeWorkload`/`IssuedWorkloadRecord` path:

- Synthetic SAV source: `build_s3` with 6 respondents × 2 occasions.
- Operation fixture: `SCORE = 0`.
- `build_projection_catalog` -> `build_test_only_workload` ->
  `execute_test_only_workload`.
- Scope: `TEST_ONLY_SOURCEFREE`.
- Actual result: `BatchSummary(batch_state='COMPLETED',
  coverage_state='FULL_MANIFEST_COVERAGE', full_coverage=True,
  total_units=1, completed_units=1, failed_units=0,
  actual_execution_receipts=1)`.
- `NativeWorkloadResult`: 1 native output, 1 receipt, 0 route results (no
  discovery units), 1 output ref.

Representative positive run (the synthetic SAV bytes make the envelope hash
run-specific):

```text
SCOPE TEST_ONLY_SOURCEFREE
NATIVE_OUTPUTS 1
RECEIPTS 1
SUMMARY BatchSummary(... batch_state='COMPLETED' ... full_coverage=True ...)
```

This positively exercises the current sourcefree workload path at its declared
test-only scope. It is **not** an original-source receiver and does not grant
source/scientific use.

The same independent court ran 8 actual-path negatives (9 tests including the
positive): **9 passed, exit 0**.

| Actual mutation | Actual refusal |
|---|---|
| `TestOnlyDecisionResolver` with foreign decision ref | `WorkloadBindingRefusal: UNKNOWN_DECISION_REF` |
| Lying resolver returning a foreign record | `WorkloadAdmissionError: CURRENT_AUTHENTICATED_ISSUER_RECORD_REQUIRED` |
| Extra expected job / removed held row | `WorkloadAdmissionError: EXPECTED_EXECUTED_OPERATION_IDENTITY_MULTISET_MISMATCH` |
| Mutated envelope hash | `WorkloadAdmissionError: ENTIRE_EXECUTION_DESCRIPTOR_NOT_THE_ISSUED_ENVELOPE` |
| Wrong source edition | `WorkloadAdmissionError: SOURCE_FACTORY_RETURNED_WRONG_EDITION` |
| Prior receipts / replay | `WorkloadAdmissionError: RESTORE_THROUGH_EXISTING_ISSUED_FACT_RECEIPT_CUSTODY_REQUIRED` |
| Wrong role / predicate direction | `WorkloadAdmissionError: QUERY_TARGET_CONDITION_DIRECTION_MISMATCH` |
| Severed resolver | `RuntimeError: CURRENT_DECISION_DEPENDENCY_SEVERED` |

The independent positive/negative suite is at
`/tmp/opencode/v2k-hostile/test_current_positive_and_actual_negatives.py`
(not committed; test artifact outside the review branch).

## Historical V2K: dependency failure preserved

### Original V2K at `694fb45085cd5e4891949921a44edb77c3f603f2`

Command:

```bash
PV_RETURN=$PWD/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1 \
PYTHONPATH=. python3 -m pytest -q \
  rawlsing_next/tests/test_hq295_v2k_original_identity_successor.py \
  rawlsing_next/tests/test_postastra_pv_v2k_independent.py
```

Actual result: **2 collection errors, exit 2**.

```text
ImportError: cannot import name 'pre553_original_workload_contract_v2_candidate'
```

This is a preserved historical dependency failure. No green was inferred.

### Exact repair tree at `9647d851a2d9b6e93e6711eec7a65325fb83aaa1`

Command:

```bash
PYTHONPATH=. python3 -m pytest -q \
  WORKER_RETURNS/PYAT-R3-PE-V2K-SCOPED-RECOVERY/tests/test_v2k_dependency_severance.py
```

Actual result: **1 passed / 1 failed, exit 1**.

- `test_current_issued_workload_is_not_v2k_abi` passes.
- `test_v2k_import_fails_when_exact_dependency_severed` fails because the V2K
  module itself is absent at `9647d851`; the observed error is
  `No module named 'rawlsing_next.pre553_original_identity_v2k_successor_candidate'`,
  not the expected severed-dependency message.

This independently confirms S7's **1 pass / 1 fail**, not the prior 2/2 claim.

### Historical 63-pass restoration: prior manifest is incomplete

Following `V2K_DEPENDENCY_RESTORATION.json` literally restored five source
modules, but collection still failed because
`pre553_governed_batch_checkpoint_integration_candidate` was not listed. Adding
that module from `5eb51c6868f4919c31758e0fa96c52f755564fa4` produced the claimed
**63 passed** historical replay. This is a provenance defect in the prior
restoration manifest: the documented list is not sufficient to reproduce the
63-pass claim without an extra dependency.

The 50/1 exact dependency/owner suites were not rerun in this court; the
111-test aggregate is not available as one exact suite. No 63/63 current ABI
claim is made.

## 38 decisions

`V2K_38_FUNCTION_DECISION_COURT.jsonl` re-adjudicates the author's 38 rows.
Results:

- 13 `UPHOLD_RETAIN_CURRENT`
- 3 `UPHOLD_RETAIN_CURRENT_EQUIVALENT`
- 8 `UPHOLD_RETIRE`
- 2 `UPHOLD_SUPERSEDED_BY_CURRENT`
- 2 `UPHOLD_RETIRE_NO_CURRENT_CONSUMER`
- 2 `UPHOLD_RETIRE_EXACT_KEY`
- 2 `UPHOLD_RETIRE_DEPENDENT_ON_UNISSUED_AUTHORITY`
- 2 `UPHOLD_RETIRE_EVIDENCE_ONLY`
- 1 `UPHOLD_RETIRE_EXACT_KEY__PARTIAL_FIELD_EQUIVALENCE`
- 1 `UPHOLD_HOLD__ANTI_JOIN_NOT_CURRENT`
- 1 `UPHOLD_SUPERSEDED_TYPED_ERROR`
- 1 `UPHOLD_ADAPT_WITH_REVISION`

All 37 source rows' current paths/blobs match the author's values. All old V2K
symbols are absent from current `rawlsing_next` and have no current import.
The one test row is an author artifact, not a source function.

The only preserved HOLD is the old item/namespace/release/routing C11 anti-join
(`_validate_original_against_c11`, historical
`pre553_original_identity_v2k_successor_candidate.py:218`). Current `admit`
(`pre553_issued_workload.py:211`) checks source edition,
expected jobs, envelope, query direction and catalog, but not the original
release/universe/item/routing anti-join. The independent sourcefree positive
does not exercise it. If a real original-source current consumer appears, this
invariant must be preserved or reimplemented; it is not a reason to transplant
the old module.

## Verdict

- **V2K retirement decision is upheld at current sourcefree scope.** Current
  R61 is a different ABI; the old exact V2K interface is not a current consumer.
- **No original-source positive.** The new positive is sourcefree synthetic.
- **Anti-join HOLD remains.** It is the one historical invariant a future real
  original-source consumer may need.
- **No 63/63 current claim.** 63 historical passes require exact old deps plus a
  missing documented dependency; they are historical replay only.
