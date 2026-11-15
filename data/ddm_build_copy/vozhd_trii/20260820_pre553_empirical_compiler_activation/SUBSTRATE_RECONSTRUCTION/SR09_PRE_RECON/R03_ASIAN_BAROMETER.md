# SR09-PRE R03 — ASIAN BAROMETER FAMILY RECONNAISSANCE

Status: `AUTHORIZED__NON_DISPOSITIVE`
Branch: `agent/vozhd-trii-sr09pre-r03-asian-barometer`
Write only: `SR09_PRE_RECON/RETURNS/R03/`

Read `00_COMMON_WORKER_CONTRACT.md` first and obey it exactly.

## Assigned exact sources

| source | SHA-256 |
|---|---|
| `Asian Barometer Wave 1.sav` | `ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2` |
| `Asian Barometer Wave 4.sav` | `4d914817509d0e5f3adde49707df148f696992055937f085080a016002a39200` |
| `Asian Barometer Wave 5.sav` | `2576e428ff8de3c8d93a418c9120a1c2955ab7b1f35961d8c18fa562bc4b5e63` |

## Mission

Build the future source-certification burden across Waves 1/4/5, with special attention to country-system drift, topology, and source-native module structure.

Determine at minimum:

- candidate respondent IDs and their measured uniqueness/scope;
- country/wave/region coding systems across all three waves;
- physical missing and user-missing declarations;
- weight/design variables and cross-wave drift;
- multiple-response/repeated/ranked slot structures, including source metadata where present;
- module/form/routing indicators physically represented;
- variable/value-label drift for recurrent names or apparent concepts;
- unusual storage/display/measure metadata;
- exact hostile sentinels per hazard class;
- whether any wave behavior extends beyond the generic SAV contract.

Asian Barometer Wave 6 is outside CLOSED_35 and must not be substituted, added, or used as certification evidence.

Required success token in `RESULT.json`:

`PRE553_SR09PRE_R03_ASIAN_BAROMETER_RECON_COMPLETE`
