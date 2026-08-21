# SR09-PRE R02 — ARAB BAROMETER FAMILY RECONNAISSANCE

Status: `AUTHORIZED__NON_DISPOSITIVE`
Branch: `agent/vozhd-trii-sr09pre-r02-arab-barometer`
Write only: `SR09_PRE_RECON/RETURNS/R02/`

Read `00_COMMON_WORKER_CONTRACT.md` first and obey it exactly.

## Assigned exact sources

| source | SHA-256 |
|---|---|
| `Arab Barometer Wave 1.sav` | `2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18` |
| `Arab Barometer Wave 2.sav` | `6529841b97bd56463490d810ad24ceaa4866066d12e4651a7081682d413606a1` |
| `Arab Barometer Wave 5.sav` | `6a5cbad637ce1546833a1d4812ba6d1e8d75f85b5b199b0cf3ec5cf456068dbc` |
| `Arab Barometer Wave 8.sav` | `a5e83a953f03dd890e076a51da473051f1cfd1ca2e8ab93c2172eeb2517af998` |

## Mission

Build the future source-certification burden across Waves 1/2/5/8, with special attention to multilingual text/label behavior, routing/module structure, and longitudinal coding drift.

Determine at minimum:

- candidate respondent identity fields and scope changes;
- country/wave/region coding systems and drift;
- physical missing/user-missing declarations and exact source examples;
- ordinary labeled values that are candidates for DK/refusal/N/A semantics without promoting them to authority;
- multilingual/non-ASCII variable/value labels and exact Unicode sentinels;
- weight/design variables and naming/scope changes;
- routing/form/module indicators physically represented in the file;
- repeated/ranked/multiple-response topology;
- recurrent-variable name/ordinal/label/value-code drift;
- any behavior not already covered by the frozen generic SAV decoder contract.

Prefer hostile sentinels that exercise multilingual metadata, missing declarations, routing-relevant fields, and country/weight edges.

Required success token in `RESULT.json`:

`PRE553_SR09PRE_R02_ARAB_BAROMETER_RECON_COMPLETE`
