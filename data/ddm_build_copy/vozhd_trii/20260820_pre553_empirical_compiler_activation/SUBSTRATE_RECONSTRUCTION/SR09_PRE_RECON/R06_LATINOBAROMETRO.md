# SR09-PRE R06 — LATINOBAROMETRO FAMILY RECONNAISSANCE

Status: `AUTHORIZED__NON_DISPOSITIVE`
Branch: `agent/vozhd-trii-sr09pre-r06-latinobarometro`
Write only: `SR09_PRE_RECON/RETURNS/R06/`

Read `00_COMMON_WORKER_CONTRACT.md` first and obey it exactly.

## Assigned exact sources

| source | SHA-256 |
|---|---|
| `Latinobarometro 1995.sav` | `4b7fc6da17dfddafd6a835717e8dc06981208eb4120fa33bdd16e12ae95926f7` |
| `Latinobarometro 2011.sav` | `a44e89e08e564e4e175199eeeabfa6163f32f4ba0a19a6c3f5b4752de6cca22e` |
| `Latinobarometro 2024.sav` | `ff5cef18c87969026e7f993d09f10c38a547bf81d5d398784fb59b960b7b0a40` |

## Mission

Build the future-certification burden across 1995/2011/2024, emphasizing country/sample identity and long-period coding drift.

Determine at minimum:

- candidate respondent IDs and source-row identity hazards;
- country/region/year/sample coordinates and code-system changes;
- user-missing/system-missing declarations and exact examples;
- weight/design candidates and cross-release drift;
- recurrent variable-name, label, and value-code drift;
- ordinary labeled nonresponse values that require later semantic authority;
- multilingual/diacritic/Unicode label sentinels;
- routing/module/form and repeated/ranked topology physically represented;
- exact hostile sentinels per distinct hazard class;
- whether any release behavior falls outside the generic SAV contract.

Do not treat apparently stable Spanish-language labels as proof of canonical equivalence across years.

Required success token in `RESULT.json`:

`PRE553_SR09PRE_R06_LATINOBAROMETRO_RECON_COMPLETE`
