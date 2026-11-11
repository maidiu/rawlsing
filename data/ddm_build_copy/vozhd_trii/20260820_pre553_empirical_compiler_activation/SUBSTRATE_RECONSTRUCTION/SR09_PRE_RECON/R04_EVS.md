# SR09-PRE R04 — EVS FAMILY RECONNAISSANCE

Status: `AUTHORIZED__NON_DISPOSITIVE__HIGH_PRIORITY`
Branch: `agent/vozhd-trii-sr09pre-r04-evs`
Write only: `SR09_PRE_RECON/RETURNS/R04/`

Read `00_COMMON_WORKER_CONTRACT.md` first and obey it exactly.

## Assigned exact sources

| source | SHA-256 | frozen reader compatibility |
|---|---|---|
| `EVS 1981.sav` | `5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2` | none |
| `EVS 1990.sav` | `66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec` | none |
| `EVS 1999.sav` | `6058644a9308aad574b95fa0afd1b026fedea289c6c95aca043aefb41ae0ab8a` | `latin1`, compatibility-execution only |
| `EVS 2008.sav` | `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379` | `latin1`, compatibility-execution only |
| `EVS 2017.sav` | `95096c2474b81ef12004726e4ed5b0919b1ea7bb672baff676ae40fb1b629bd2` | none |

## Mission

Build an adversarial future-certification burden across EVS 1981/1990/1999/2008/2017.

EVS 1999 and 2008 are already known reader-compatibility hazards. The frozen `latin1` override is **not** source-text semantic authority. Do not upgrade it by implication.

Determine at minimum:

- exact metadata/text fields whose default reader path fails or differs from the compatibility path;
- hostile Unicode/byte-sequence sentinels that later certification must replay;
- which facts are safe physical authority under compatibility execution and which remain text-authority gaps;
- user-missing declarations/ranges and source examples across all waves;
- multiple-response metadata/topology and cross-wave drift;
- candidate respondent IDs and country/wave coordinates;
- weight/design variables and evolution;
- recurrent variable/value-label drift across the long time span;
- source-native rank/slot/module/routing structures;
- any new hazard class beyond the frozen SAV/encoding contract.

Do not repair text or choose an intended encoding. Record exact evidence and the authority gap.

Required success token in `RESULT.json`:

`PRE553_SR09PRE_R04_EVS_RECON_COMPLETE`
