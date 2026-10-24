# R91 R04_JOINED R3 author return — restored native output identity

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted.

## Identity

- Branch: `agent/opencode-pyat-r91-r04-joined-custody-r1`
- Startup: `dfeaab23998291be81abe4caecd08de663053eaa`
- Contract commit: `cca9d5d50f6571fc6ca08135bc17f6b33d229833`
- Code commit: `6068ab9e53b652ab603b30f8db55738393daff9b`
- R04V R2 review: `239f492272bd72011f53570020a4b0cdc27dff27`
- Executor: same OpenCode DeepSeek V4.1-Flash MAX/Global.

## Sole repair

Checkpoint output custody now stores full identity-bearing output material:

- query outputs: exact `QueryExecutionResult.query_ref`, fact preimages,
  `source_scope_mode`, exact release refs;
- discovery outputs: contract/authority/grammar/evaluated-frontier/replay,
  coverage/counts, receipt preimages, exact fact refs/facts, executed
  predicate/query refs and valid-empty.

Cold restore reconstructs actual native `QueryExecutionResult` objects and a
frozen, validated `RetainedDiscoveryResultView` (fact/receipt ordering and
closure checked). Mutable facts-only `SimpleNamespace` output views are gone.
Partial prior outputs use the same constructors and feed the existing Batch
resume path. All prior pin/manifest/partial/no-rerun behavior is retained.

## Evidence

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_workload_custody.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R91-R04-JOINED-CUSTODY-R1/revisions/r3/junit.xml -o addopts=''
```

Exit `0`; `6 passed`, `0 failed/errors/skips`; `19.04s`. Retained R03 suite:
`16 passed`, `0 failed/errors/skips`.

New test asserts restored query `QueryExecutionResult.query_ref/facts/release_refs`
equal uninterrupted and restored discovery `RetainedDiscoveryResultView`
evaluated-frontier/replay/fact/receipt identities equal original; view mutation
raises `FrozenInstanceError`.

## Blobs

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_issued_workload.py` | `be5ffc75287ad25ac35eb03bc5e506c00a5837a2` |
| `rawlsing_next/tests/test_universal_workload_custody.py` | `074f5373ed28693aa75af44e28c8dff4c8bd46a0` |

Manifest excludes itself. Native owners/R03/U43 unchanged.

## Limits

Sourcefree TEST_ONLY local trusted host. No R05+, original science,
global exactly-once, CI/prod/N11/N12/Sorok/J52/W52. Distinct reviewer required;
no self-adoption.
