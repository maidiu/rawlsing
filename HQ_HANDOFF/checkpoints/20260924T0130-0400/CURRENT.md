# RAWLSING HQ CURRENT — FIABC PRE-CANDIDATE CLOSURE DELEGATED TO CODEX

Status: `RAWLSING_FIABC_PREFLIGHT_RECEIPT_CLASSIFICATION_REPAIRED__AUTONOMOUS_PRE_CANDIDATE_CLOSURE_RECOMMENDED`

Checkpoint: `20260924T0130-0400`

Decision: `HQD-2026-09-24-092`

## RUN2 finding

RUN2 passed:
- immutable succession evidence fetch;
- runtime/source/frozen answer-key gates;
- succession producer;
- direct succession preflight;
- Darwin driver preflight.

The launcher then falsely blocked because it treated any file under `WORK_ROOT/cells` as evidence of candidate execution.

Current driver preflight intentionally writes frozen-law/preserved receipts under cell receipt directories. These mechanical receipts carry:
- `execution_performed: false`
- `measurement_performed: false`

## Repair

Launcher commit:
`68b36b3202141f855ca5cc5fa5e4200541fd8413`

Launcher blob:
`6382df7a6930d1def32ea3b555d9d0ef046d8472`

The launcher now permits only JSON files in governed cell receipt directories during preflight and requires both execution and measurement flags to be false. Any other file or state fails closed.

Protected execution remains:
`bc832181b4284ac110d2be44fc83504e04de081e`

Measured `--run` invocation is unchanged.

## Operating recommendation

Do not continue manual human retry/debug loops.

Delegate recursive pre-candidate launcher/preflight closure to Codex.

Codex may:
- inspect preserved failed work roots;
- diagnose launcher/preflight/control-plane failures;
- repair launcher/control-plane plumbing;
- run source-free tests;
- hash canonical sources where required by preflight;
- create fresh work roots and fresh protected checkouts;
- repeat until the launcher reaches a genuinely green preflight.

Codex must hard-stop before measured candidate execution unless the preflight is fully green and the execution substrate is unchanged and qualified.

Once measured `--run` begins, no adaptive repair is allowed inside that run.
