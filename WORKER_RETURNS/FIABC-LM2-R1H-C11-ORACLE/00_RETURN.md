# FIABC-LM2-R1H — Browser-Only Common-C11 and Fresh Oracle Closure

Terminal:

`BLOCKED__FIABC_LM2_R1H__R15_REAL_MATERIAL_COMMON_C11_UNBOUND_RESPONSE_VALUE_STATE__R16_NOT_EXECUTED`

## Exact base and execution surface

- Repository: `maidiu/rawlsing`
- Exact R1G base: `dc8047580ca5039f6678afd5effc506c30bbf54d`
- Branch: `agent/rabochii-premain-fiabc-lm2-r1h-common-c11-oracle-browser-r1`
- Browser-only GitHub Actions evidence execution SHA: `2513c182d4fdc4f4cadb0e5479706f412bdb7e52`
- GitHub Actions run: `35572953550`
- Job: `106248324441`
- PR used only to trigger the browser-hosted court: #425, closed without merge.

## Gate 1 — PASS

The persisted frozen Q291 carrier was admitted exactly before R15:

- path: `WORKER_RETURNS/FIABC-LM2-R1F-CARRIER-ARCHAEOLOGY/LOCAL_OUTPUT/FIABC_LM2_R1E_FROZEN_Q291_PHYSICAL_CELL_CARRIER.json`
- SHA-256: `1aea888d8d576fc8606d56dd7a3b1a552411b8f8126ea27a54c36ff6d551dd7e`
- bytes: `83340882`
- rows: `97220`
- physical cells: `194440`
- question order: `Q291G5`, `Q291P5`
- source SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`
- structural preimage: `151907b3163959d0eb5ebb020fa5253d33447362420e465600035744112fe5bc`
- candidate neutral: `true`
- contains candidate output: `false`
- existing `validate_frozen_response_carrier`: PASS.

The court also checked exact row ordinals, exact Q291 physical variable names/ordinals (388/394), required raw witness/missing-state/declaration fields, and the exact 194,440-cell count.

## R15 — FAIL CLOSED ON REAL MATERIAL

The exact intended R15 operation was executed through the existing repaired R1E implementation:

`common_c11_receipt(CARRIER)`

Expected: strict candidate-neutral common C11 materialization under the repaired mapping/projection authority, with zero candidate output consulted.

Observed:

`rawlsing_next.pre553_source_backed_c11_facade.SourceBackedC11FacadeError: unbound response value/state; no label/frequency/missingness inference`

Failure path:

- `rawlsing_next/fiabc_lm2_r1e_common_c11.py:159`
- `rawlsing_next/fiabc_lm2_r1e_common_c11.py:155`
- `rawlsing_next/pre553_source_backed_c11_facade.py:600`
- `rawlsing_next/pre553_source_backed_c11_facade.py:537`

This occurred after the exact carrier preflight passed and after the repaired governed projection had been constructed. The strict facade found a real physical response value/state with no exact bound response rule and correctly refused inference.

No semantic patch, coercion, relabel, raw-value reinterpretation, or authority broadening was attempted. The first unbound physical value is deliberately not characterized here because the commissioned stop law requires STOP BLOCKED on R15 failure rather than a new diagnostic/semantic pass.

## R16 — NOT EXECUTED

R16 depends on successful real common C11. Because R15 failed, no fresh WVS7 oracle was frozen and `freeze_wvs7_oracle_from_common_material` was not invoked.

The historical FIABC-LM2 blocker receipt was not reused as an oracle.

## Prohibited work remained absent

- WVS7 SAV/ZIP opened: 0
- new source reads: 0
- Candidate A/B/C processes started: 0
- I03 runs: 0
- I05 runs: 0
- measured P2X runs: 0
- raw values reinterpreted: 0
- mapping authority broadened: 0
- R1E/R1F/R1G/HQ branches mutated: 0
- PR #424 mutated: 0
- merges/rebases/main movement: 0

## Disposition

Return to HQ at the R15 real-material binding contradiction. The exact carrier is valid; the current repaired projection/common-C11 path is not closed over every real physical Q291 response value/state admitted by that carrier.

