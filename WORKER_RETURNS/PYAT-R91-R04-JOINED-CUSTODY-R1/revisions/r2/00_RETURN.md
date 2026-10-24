# R91 R04_JOINED R2 author return — actual native partial restart

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted.

## Identity

- Branch: `agent/opencode-pyat-r91-r04-joined-custody-r1`
- Startup: `a88ccd140f30fe621140ee98841c6ce57ae9cab4`
- Contract commit: `7b84cf20df2fc2bfea3b00e57f42047df55cb5e0`
- Code commit: `c0c4b9e15a84546ca200d8da85bd3979832e7b1e`
- R04V review: `50b8bee9e59d4c13fffeda319e257b37b5593356`
- Executor: same OpenCode DeepSeek V4.1-Flash MAX/Global.

## Delivered

- `capture_joined_checkpoint` now accepts actual R03 governed
  `NativeDiscoveryExecution` (native_result/manifest/receipts/facts) and actual
  `NativeWorkloadResult`, retaining original manifest unit specs, receipt
  preimages, completed output fact OBJECT material by unit, exact output refs
  and source/envelope/decision identity.
- Completed discovery capture/resume retains original native facts and original
  manifest; no synthetic manifest or empty outputs.
- Real partial multi-unit `NativeWorkloadResult` prefix (`max_units=1`) is
  captured and resumed; completed units are not rerun, pending units execute
  through the existing Batch lead, and combined output refs match the
  uninterrupted run.
- Joined checkpoint now requires the separately provisioned original
  `checkpoint_hash` pin on restore/resume. Missing/wrong pin and self-rehashed
  forged checkpoint refuse. No pin is taken from submitted payload.
- Current grant/source identity is rechecked before pending native work;
  revoked/wrong-source cases refuse.

## Evidence

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_workload_custody.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R91-R04-JOINED-CUSTODY-R1/revisions/r2/junit.xml -o addopts=''
```

Exit `0`; `5 passed`, `0 failed/errors/skips`; `10.56s`. Retained R03 suite:
`16 passed`, `0 failed/errors/skips`.

Tests include actual governed discovery capture/retained facts, partial
multi-unit native prefix/resume with completed-unit non-rerun, genuine pin
restore, missing/wrong pin refusal, revoked/wrong-source refusal, and
fresh-process full-prefix resume.

## Blobs

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_issued_workload.py` | `5ce71e6fdc4bb6e9ee3b9075616fa50432394a0d` |
| `rawlsing_next/tests/test_universal_workload_custody.py` | `94cdeecbda03ca17b4226b2d2fb571f3e16d7068` |

Manifest excludes itself. R03/native owner/U43 bodies unchanged; R04.byte
decoder read-only.

## Limits

Fresh-process evidence is full-prefix; actual partial resume is in-process at
this return. No indivisible discovery split, new lineage engine, R05+, original
science, global exactly-once, CI/prod/N11/N12/Sorok/J52/W52. No self-adoption;
distinct reviewer required.
