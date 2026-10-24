# R61 R03 R5 author return — shared capture/restore validation

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted.

## Identity

- Branch: `agent/opencode-pyat-r61-r03-total-native-workload-r1`
- Startup: `8c506f8f239204b004e4b677572898c8dba06811`
- Contract commit: `bae28794fa450bcf6ec500b47fa8886802a0aef2`
- Code commit: `5ba003e6ce0c42b690e7128fb6b7e08f409f5576`
- R4 review: `61356022db35254193605ae1cf749b1dff29794e`
- Executor: same OpenCode DeepSeek V4.1-Flash MAX/Global.

## Delivered

Extracted one pin-free shared validator
`_validate_governed_ledger_material` covering structural closure, expected jobs/
candidates/operations mapping, native receipt/fact object identity, duplicate
rejection, receipt-to-row/state/coverage/fact associations, fact coverage and
candidate/operation anti-join truth.

- `freeze_restore_checkpoint()` now runs that validator on its own canonical
  ledger before returning any checkpoint. Empty operation ledger, duplicate
  fact refs, missing expected identities or closure breaks refuse capture.
- `restore_governed_frontier_ledger(...)` checks the submitted self-hash and the
  separately provisioned original pin first, then calls the same validator.
  No unpinned fallback; fixed-pin behavior preserved.
- Shared facts across receipts remain lawful; duplicate native fact objects are
  rejected.

## Evidence

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_workload.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R61-R03-TOTAL-NATIVE-WORKLOAD-R1/revisions/r5/junit.xml -o addopts=''
```

Exit `0`; `16 passed`, `0 failed/errors/skips`; `94.59s`. Retained R01 suite:
`32 passed`. New test covers capture rejection for empty operation ledger and
duplicated fact refs with restored genuine capture.

## Blobs

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_issued_workload.py` | `31e84f49d624f5524906e9e7839d2873106f8249` |
| `rawlsing_next/pre553_native_workload_binding.py` | `dac73e484f8619088f5c6701b2b6991c07540f3b` |
| `rawlsing_next/pre553_universal_workload.py` | `8e7fe00a3ed008361d9f3c501e7782b2de3a636e` |
| `rawlsing_next/tests/test_universal_workload.py` | `33c34a3bf4d14fa59a4f7a1f7f83a3c148a241f7` |

Manifest excludes itself. Native owners/U43 unchanged.

## Limits

Local trusted-host TEST_ONLY. No R04 durable custody/cryptographic authority,
R05+, original science, CI/prod/N11/N12/Sorok/J52/W52. Distinct reviewer
required; no self-adoption.
