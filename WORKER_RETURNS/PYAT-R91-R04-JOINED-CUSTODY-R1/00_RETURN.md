# R91 R04_JOINED author return — joined custody checkpoint and resume

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted.

## Identity

- Branch: `agent/opencode-pyat-r91-r04-joined-custody-r1`
- Startup: `c912497b25411ebbd3d796db139f32f5bebb6c4c`
- Contract commit: `b93b95adca3b803fc4f4c17acc712686e800377c`
- Code commit: `ef1e71628c0a89753c0c6aeea3c35c5fb06e29eb`
- Executor: same OpenCode DeepSeek V4.1-Flash MAX/Global.
- R03 accepted base: `c912497b25411ebbd3d796db139f32f5bebb6c4c`

## Delivered

Added joined custody in `pre553_issued_workload.py`:

- `capture_joined_checkpoint(results)` captures only completed
  `NativeWorkloadResult` runs, requiring full manifest receipt closure and all
  COMPLETED receipts. It retains exact decision/envelope/source/manifest,
  receipt preimages and output refs with canonical per-entry/checkpoint hashes.
- `resume_joined_workloads(...)` verifies checkpoint hash and workload
  decision/envelope/source identity; completed workloads are represented by
  retained receipts/refs and are NOT executed again. Pending workloads run
  through existing `execute_issued_workload` admission/source/Batch path with
  current grant and source rechecked. Combined output refs and receipt materials
  equal the uninterrupted sequence.
- `restore_joined_checkpoint(material)` rehydrates and verifies the canonical
  checkpoint without trusting submitted refs alone.
- Fresh-process resume loads the checkpoint and rebuilds the same R03-issued
  workloads from the retained source bundle.

Tests use actual `compile_universal_workload` R03-issued workloads and actual
U43/C11/Batch execution. Revoked currentness and wrong source edition refuse
before native work. Completed workloads are skipped (source-factory call count
proves no reexecution).

## Commands

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_workload_custody.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R91-R04-JOINED-CUSTODY-R1/junit.xml -o addopts=''
```

Exit `0`; `3 passed`, `0 failed/errors/skips`; `3.70s`. Retained R03 suite:
`16 passed`, `0 failed/errors/skips`.

## Blobs

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_issued_workload.py` | `9a576a06b9be82164e3ccd57a42ad98c22ff8a06` |
| `rawlsing_next/tests/test_universal_workload_custody.py` | `ad5259812c3761753f1cb8399680a88bc2602d9f` |

Manifest excludes itself. U43/R03/native owner semantic bodies unchanged.

## Limits

Joined resume is at workload granularity: R03 currently emits single-unit
workloads; no automatic governed-discovery caller wiring is claimed. No
byte-decoder rewrite; accepted R04.byte remains read-only reuse. No global
durable exactly-once/anti-fork, R05+, original science, CI/prod/N11/N12/Sorok or
J52/W52. Distinct reviewer required; no self-adoption.
