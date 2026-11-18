# ANVIL CUT1 — implementer baseline and executable cut contract

## Status

**`CUT1_IMPLEMENTED_READY_FOR_DISTINCT_NONAUTHOR_REVIEW`**

- Product baseline: `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`
- Branch: `agent/anvil-engineering-cut1-20261117-r1`
- Worktree: `/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/IMPLEMENTER`
- Baseline product/test edits: **NONE**
- Implemented production files: **2**
- New focused test under `rawlsing_next`: **1**
- **Implementation status: `CUT1_IMPLEMENTED_READY_FOR_DISTINCT_NONAUTHOR_REVIEW`**
- Contract: `EXECUTABLE_CUT_CONTRACT.md`
- Owner ACK: `a744a5a4e4bb31ba9e93a650c7200c064d4d2e11`
- Implemented production blobs: integration `c568836b…`, Batch `8320f284…`
- New test: `bf00eb59…`; **5 passed**
- After-cut boundary: **70 passed, 0 failed, 28.959 s**
- Probe/witness: `evidence/`

## Actual baseline execution

Runtime, unchanged:

```text
Python 3.11.3
pyarrow 22.0.0
duckdb 1.5.2
pyreadstat 1.3.2
pytest 9.0.2
```

### Focused cut1 suite — 58/58 PASS

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q \
  -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_prepared_saved_i03.py \
  rawlsing_next/tests/test_pre553_direct_estate_i03.py \
  rawlsing_next/tests/test_pyat997_s1e_saved_native_first_consumer.py \
  rawlsing_next/tests/test_pyat991_s2d_saved_admission.py \
  rawlsing_next/tests/test_pre553_batch_runner.py
```

**58 passed, 0 failed, 0 errors, 0 skipped, 17.523 s.**

By file/class:

- prepared saved I03: 3
- direct estate I03: 7
- saved native first consumer: 24
- saved admission: 8
- native Batch runner: 16

Logs/JUnit: `evidence/baseline_cut1.txt`,
`evidence/baseline_cut1.junit.xml`.

### Batch / five-reader court — 23/23 PASS

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q \
  -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat991_s2d_five_readers.py \
  rawlsing_next/tests/test_pre553_batch_runner.py
```

**23 passed, 0 failed, 0 errors, 0 skipped, 6.13 s.**

The existing legacy saved Batch paths are real and green:

- `test_saved_batch_actual_native_scheduler`
- `test_saved_normal_matches_legacy_native_and_never_opens_source`
- `test_saved_completed_partial_absent_use_existing_resume`
- `test_saved_normal_and_completed_survive_fresh_process`

### Prepared direct path

Existing test:
`test_prepared_session_matches_baseline_and_builds_one_index` — **PASS**.

It proves:

- one `DirectEstateI03Session` index build across four operations;
- exact native fact refs/projections parity against the legacy path;
- one operation context reuse;
- prepared I05 exact discovery parity.

## Prepared ABI RED — desired new Batch feature

Existing wrappers reject the prepared subclass exactly:

```text
execute_saved_i03:
  SavedC11AdmissionError: exact SavedC11Admission required

BatchExecutionRunner(..., saved_mode=True):
  BatchIntegrityError: repository must be accepted I02 C11Repository or exact SavedC11Admission
```

Return-local witness:
`evidence/test_prepared_abi_witness.py` — **2 passed, 1.53 s**.

Probe:
`evidence/abi_probe.py` / `.json`:

- admission type: `PreparedSavedC11Admission`
- manifest SHA-256:
  `87f5c6c68da3707c4fa565b929c9411ffc6b18f161533788885dd2be943496a9`
- four queries
- both normal wrappers reject before positive execution
- disposition: `BASELINE_READY_PENDING_CURRENT_OWNER_ACK`

This is a RED for the **desired new prepared-Batch feature**, not a claim that
an existing test is failing.

## Exact cut contract

`EXECUTABLE_CUT_CONTRACT.md` specifies:

- only two production files:
  - `rawlsing_next/pre553_saved_workload_integration.py`
  - `rawlsing_next/pre553_batch_runner.py`
- exact prepared-only whitelist;
- direct vs Batch context dispatch;
- one prepared index per Batch, closed on success/error;
- per-unit CURRENT checks;
- unchanged Batch schedule/manifest/receipt/replay semantics;
- exact new focused test path and positive/refusal/restoration assertions;
- frozen saved base, prepared module, writer, evaluator, issuer,
  NORMAL/resume.

No third production file is required. `PreparedSavedC11Admission` already
provides the exact one-session context.

## Source/corrective preservation

Current pinned blobs:

- `pre553_saved_workload_integration.py` `cc8aa325…`
- `pre553_batch_runner.py` `49e3974c…`
- `pre553_prepared_saved_i03.py` `bcb146ed…`
- `pre553_saved_c11_admission.py` `22749add…`

W05 three production blobs retained exactly and match the W05
`1c37e2d` / composite `357a0fb` source cut:

- `pre553_direct_estate_i03.py` `8825832f…`
- `pre553_source_direct_parquet_estate.py` `e8622ac6…`
- `_pre553_query_eval.py` `87849f7c…`

No old-branch merge, duplicate implementation, or R03 source/science/current
grant is introduced. Current R03 corrective snapshot is preserved; no old
branch was merged.

## Owner gate

This turn stops before implementation. Before any production edit:

1. Fresh current owner ACK for the two exact files and the new focused test.
2. Confirmed current lease/session ownership.
3. Confirmation that `PreparedSavedC11Admission.prepared_i03()` is the intended
   one-session Batch reuse surface.

Only then may the same branch implement the two-file cut and test, run the
bounded positive/refusal/restoration court, and return a new exact source cut
for independent receiving.

## Holds

- Protected `5d387a9…`, source/science/current/actor/issuer, original35,
  native 100k/6 GiB, #1006, S2-A kernel, and protected merge remain untouched.
- No 1/10/100 wide or 100k run in this turn.
- No model/provider/host/account/installation change.
- No recurring wake or owner polling.

## Self-critique

- The baseline proves existing prepared direct session reuse and legacy saved
  Batch, not the new prepared Batch feature.
- The ABI RED is intentional feature evidence; it is not a failing existing
  test.
- The contract is implementation-ready but unexecuted pending ACK.
- No source/current/science right follows from this engineering baseline.

**STOP: `CUT1_IMPLEMENTED_READY_FOR_DISTINCT_NONAUTHOR_REVIEW`.**


---

## IMPLEMENTATION COMPLETE — pending distinct nonauthor review

Owner ACK `a744a5a4e4bb31ba9e93a650c7200c064d4d2e11` was received and the
exact two-file cut plus focused test was implemented on the same branch.

- Integration blob: `c568836b7ab1ce88224d4bc5c9de6dca8476a5db`
- Batch blob: `8320f28458fb85aec655d154a2527a161282f56b`
- New test blob: `bf00eb591bdee1087e9a10085d808c1ed2aadf88`
- After-cut 70-node boundary: **70 passed, 0 failed, 0 errors, 0 skipped**
- New focused tests: **5 passed**
- One `_build` for four prepared Batch operations
- Full projection/denominator/ref/replay and Batch receipt parity
- Wrong class/release/manifest/revoked CURRENT and mid-Batch revocation refuse
- Plain SavedC11Admission legacy path remains green
- Source reads/full C11 builds by the new Batch: **0/0**
- Small resource probe: `0.1597 s`, `104,222,720 B` parent RSS, `783,936 B`
  retained/fixture root

No new issuer, source/science/current grant, protected write, 100k run,
subagent, model/provider/host change, or self-acceptance. Existing baseline
logs and the pre-cut ABI RED remain preserved. STOP for a distinct nonauthor
review at this exact cut.
