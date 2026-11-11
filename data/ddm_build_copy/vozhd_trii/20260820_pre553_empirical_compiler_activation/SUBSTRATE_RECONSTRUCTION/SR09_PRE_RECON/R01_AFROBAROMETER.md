# SR09-PRE R01 — AFROBAROMETER FAMILY RECONNAISSANCE

Status: `AUTHORIZED__NON_DISPOSITIVE`
Branch: `agent/vozhd-trii-sr09pre-r01-afrobarometer`
Write only: `SR09_PRE_RECON/RETURNS/R01/`

Read `00_COMMON_WORKER_CONTRACT.md` first and obey it exactly.

## Assigned exact sources

| source | SHA-256 |
|---|---|
| `Afro Barometer Round 1.sav` | `6c9869a7cc7321cc74efb708835e21c8b65286a25c76deac45aba84d75697ee2` |
| `Afro Barometer Round 5.sav` | `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651` |
| `Afro Barometer Round 9.sav` | `3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8` |

## Mission

Build the future source-certification burden for Afrobarometer across R1/R5/R9, emphasizing longitudinal schema evolution rather than treating each round independently.

Determine at minimum:

- candidate respondent IDs and whether uniqueness/scope behavior changes across rounds;
- country/region/wave coordinates and coding drift;
- all physical missing/user-missing mechanisms actually exercised;
- weight/PSU/stratum/cluster candidates and cross-round naming/coding drift;
- value-label and variable-label drift for apparently recurrent concepts;
- repeated/ranked/multiple-response topology physically encoded;
- source-native routing/form/module clues;
- exact hostile sentinels for each distinct hazard class;
- whether any observed R1/R5/R9 behavior is not already covered by the frozen generic SAV contract.

Do not map concepts across waves semantically merely because labels look similar. Record apparent matches as drift evidence only.

Required success token in `RESULT.json`:

`PRE553_SR09PRE_R01_AFROBAROMETER_RECON_COMPLETE`
