# Browser HQ / R03 owner handoff

## Status

`TYPED_NONISSUANCE_HOLD_INPUTS_ABSENT` for both original saved waves. This is an
unsatisfied issuance-input requirement, not a production bug in the native
stream reader or query evaluator.

## Exact code and contracts

- #1084 issuer: <https://github.com/maidiu/rawlsing/blob/357a0fbf50377788b050f5365089ed54a0548f23/rawlsing_next/pre553_governed_query_issuer_v2.py>
- Compiler contract: <https://github.com/maidiu/rawlsing/blob/357a0fbf50377788b050f5365089ed54a0548f23/rawlsing_next/pre553_universal_workload.py>
- Native preimage contract: <https://github.com/maidiu/rawlsing/blob/357a0fbf50377788b050f5365089ed54a0548f23/rawlsing_next/pre553_source_native_preimage_adapter.py>
- #1185 bridge: <https://github.com/maidiu/rawlsing/blob/3eee662d509fd78bc93d3ea26c3058d3199c960f/rawlsing_next/pre553_anvil_stream_native_i03.py>
- R3 cold-admission receipt: <https://github.com/maidiu/rawlsing/blob/0e5ae0b8ed1e828320be5cfcee7b9549655c1eeb/WORKER_RETURNS/ANVIL_P0_TWO_SAVED_WAVES_NATIVE_I03_20261120_R3/00_HANDOFF.md>
- PYAT-REQ-013: <https://github.com/maidiu/rawlsing/blob/62b94554608273a86040e2e7e2666a561100dc06/WORKER_RETURNS/PYAT_PREFF_ONE_MACHINE_C0_20261119/OPEN_REQUIREMENTS.md>

## Local evidence

Controller local evidence basenames:

- SRC04: `SRC04.post_alignment.runtime.config.json`, `SRC04_Q217_MAPPING_RECEIVING.json`, `SRC04_CONFIG_BINDING.json`
- SRC16: `SRC16.source.config.json`, `SRC16.construction.binding.json`, `SRC16.shared-profile.json`

Exact per-wave fields, residuals and owners are in `HOLDS.json`. No private
paths, manifests, respondent values, sensitive counts or rights files are copied
into this handoff.

## Decision needed

R03/NativePreimageBundle owner must state whether the six missing input classes
can be supplied with exact owner hashes and an eligible/supported operation for
each exact saved stream. If not, issue the typed no-query hold. Source/mapping
owners must adjudicate the named residual IDs before any eligibility claim.
