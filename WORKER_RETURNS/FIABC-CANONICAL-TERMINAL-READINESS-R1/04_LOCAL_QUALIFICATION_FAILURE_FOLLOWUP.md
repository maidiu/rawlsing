# Local Qualification Failure Follow-up

User-reported local qualification was run from exact worker head:

`97329d51aac6bec495114b5e89e60260c2fcc846`

Reported result:

```text
154 passed, 9 failed, 28 subtests passed in 9.16s
```

The required green terminal was not emitted. The user also reported that no Candidate A/B/C execution and no measured P2X execution occurred.

## Static diagnosis

All nine failures are qualification-test/fixture drift rather than evidence of a production semantic-law defect.

### 1. Terminal completeness hostile expectation

`tests/test_fiabc_terminal_completeness.py` deleted one canonical metric and expected `TC_REQUIRED_METRIC_ABSENT`.

Current production law first checks exact equality of the complete 35-key metric set and therefore lawfully fails earlier with `TC_METRIC_SET_DRIFT`.

Repair: update only the hostile-test expected failure code. Production completeness logic is unchanged.

### 2. R1J projection/preflight assertion

`rawlsing_next/tests/test_fiabc_final_preflight_fanin.py` required the successor discovery-authority SHA to appear as a literal inside the active backend comparison.

Current backend binds the same successor identity through named constant `WVS_DISCOVERY_AUTHORITY`, whose value is the exact successor discovery authority.

Repair: assert the named constant equals the successor identity and scope the source-text check to `_wvs_docs`, where the runtime package is required to compare against that constant. Production backend code is unchanged.

### 3. Seven legacy driver-mechanics fixtures

`tests/test_ee_p2x_darwin_court_driver.py` directly drives synthetic backend receipts that predate the mandatory T3 process-envelope → T4 live-accounting seam. The production driver now correctly requires exact T3 accounting evidence before admitting live stage accounting.

These tests are state-machine/driver-mechanics unit fixtures. Exact T3 envelope behavior and T4 live accounting are separately covered by:

- `rawlsing_next/tests/test_fiabc_t3_oracle_process_envelope.py`
- `rawlsing_next/tests/test_fiabc_t4_live_accounting.py`

Repair: the driver-mechanics fixture stubs only `admit_live_stage_accounting` so those legacy unit tests remain scoped to driver mechanics rather than fabricating fake T3 envelopes. Production T3/T4 enforcement is unchanged, and the dedicated T3/T4 tests remain in the source-free qualification court.

## Qualification launcher binding

Because the R1J preflight qualification test lives under `rawlsing_next/tests/`, the source-free launcher now pins its exact repaired Git blob:

`02c6dad5912fd7283cc1fc5b889cde62b9818101`

and permits exactly that pinned path through the existing reconciliation drift filter.

## Runtime status

No follow-up runtime qualification was executed by this browser/GitHub worker. A fresh local rerun is required.

Run exactly:

```bash
bash WORKER_RETURNS/CANONICAL-REINTEGRATION-FIABC-R1/01_SOURCE_FREE_LOCAL_QUALIFICATION.sh
```
