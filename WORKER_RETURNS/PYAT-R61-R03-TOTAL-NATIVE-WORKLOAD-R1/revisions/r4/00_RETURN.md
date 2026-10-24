# R61 R03 R4 author return — fixed external checkpoint restore

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted.

## Identity

- Branch: `agent/opencode-pyat-r61-r03-total-native-workload-r1`
- Startup: `5b28d09602a35d4c5d5f060f450956c612ab3580`
- Contract commit: `496bacae2deee56f8c827157a63ea7a7416e9a21`
- Code commit: `61ce7975d822688edd9525a10ad7fa9048f69455`
- R61AV decision: `7a36e8091eda463c736f4ca0528d47f061b26cce`
- R3 review: `7d8396329ed8ac2df86c82bb46e785a0dc487cde`
- Executor: same OpenCode DeepSeek V4.1-Flash MAX/Global.

## Delivered

`GovernedFrontierResult.freeze_restore_checkpoint()` validates the live result's
candidate/operation no-drop, expected operations/jobs, native receipt/fact
closure and duplicate-fact rejection before returning the canonical whole-result
checkpoint. Failed/incomplete results cannot acquire a checkpoint.

`restore_governed_frontier_ledger(ledger, *, expected_checkpoint_ref)` now
requires the separately provisioned original pin. Missing pin, self-hash
mismatch, or pin mismatch refuses before releasing a result. The submitted
self-hash and external pin must both equal the recomputed canonical material
hash; prior full structural/closure/multiplicity validation still runs.
No native rerun, new issuance or budget charge occurs.

Tests exercise genuine restore with the real pin, missing pin, coordinated fact
deletion/duplication, expected job/predicate substitution with both mutable
copies and recomputed hashes, failed-live capture refusal, and a fresh-process
restore from independently supplied pin. Prior governed D3/joint/conditional/
minority/pending/value and HELD/UNKNOWN positives remain.

## Commands

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_workload.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R61-R03-TOTAL-NATIVE-WORKLOAD-R1/revisions/r4/junit.xml -o addopts=''
```

Exit `0`; `15 passed`, `0 failed/errors/skips`; `70.49s`. Retained R01 suite:
`32 passed`, `0 failed/errors/skips`. JUnit/logs present.

## Blobs

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_issued_workload.py` | `31e84f49d624f5524906e9e7839d2873106f8249` |
| `rawlsing_next/pre553_native_workload_binding.py` | `dac73e484f8619088f5c6701b2b6991c07540f3b` |
| `rawlsing_next/pre553_universal_workload.py` | `8e780b2430b8a6a930f45329596cfdec2f1aa46c` |
| `rawlsing_next/tests/test_universal_workload.py` | `9adbb081122c6f097f42e01203b3c835cbf7b17b` |

Manifest excludes itself. `native_receipt_anti_join`/native owners unchanged.

## Limits

Local trusted-host TEST_ONLY only. Trusted-host replacement of both pin and
candidate is excluded as in R61AF. No R04 durable custody/cryptographic
authority, R05+, original science, CI/prod/N11/N12/Sorok/J52/W52. Distinct
reviewer required; no self-adoption.
