# R132 resume — present source pipeline

## Status

`BLOCKED__CURRENT_NATIVE_RUNTIME_AND_SOURCE_ADMISSION_MISSING__SOURCE_NOT_READ__PIPELINE_NOT_EXECUTED`

- Branch: `agent/opencode-pyat-r131-exact-native-support-m1-replay-r1`
- Startup: `be5c76ae6640c3b644036ad7cbe271d7f95c8ee7`
- Return: `WORKER_RETURNS/PYAT-R132-PRESENT-SOURCE-PIPELINE-R1/`
- Local handoff:
  `.r61/r132-present-source-pipeline/s44_source_runtime_handoff.json`
  (SHA-256 `959786bd230bb12ff05bb35f253ab18cd29e921c0cc7625c2e24923a98353dde`)
- Actual attempt:
  `.r61/r132-present-source-pipeline/attempt/no_runtime.json`; exit `2`.

## What is actually established

- The current native launch API exists and imports:
  `rawlsing_next/pre553_issued_workload.py`, HEAD blob
  `be5ffc75287ad25ac35eb03bc5e506c00a5837a2`.
- The exact local S44 handoff is evidence only: `grant_present=false`,
  `raw_source_read=false`, selected `SRC27`, and no runtime module.
- No source file was read or hashed.
- The pipeline wrapper refused before any source factory call.

## Immediate missing field/owner

The current trusted runtime module is absent. Required fields are `resolver`,
`workloads["SRC27"]`, `source_factory`, `host`, and `purpose`; the current
source/scientific/consumer decisions are the five SRC27 decisions in
`SOURCE_PIPELINE_CALL.json`. Responsible owners are the source access/licence
custodian plus deployment host operator, native U/response/routing and
scientific Epre issuers, and the consumer purpose owner.

This is not a finding that the PRE553/Route-B/M1/M2/B5/E41/N10E/FF/V553 code is
unavailable.

## Next

Run `COMMANDS.md` with the exact authenticated runtime after the current
source admission exists. Otherwise stop at the same refusal; do not read source
or replace the runtime/grant.

## Holds

R131 old replay is stopped. R124/fullscope/C5 parallel, all source/science/
actor/protected grants, N11/N12/Sorok/J52/W52, and all35 remain unchanged.
