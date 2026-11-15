# SR09-PRE R09 — WVS FAMILY RECONNAISSANCE

Status: `AUTHORIZED__NON_DISPOSITIVE__KNOWN_HOSTILE_BASELINE`
Branch: `agent/vozhd-trii-sr09pre-r09-wvs`
Write only: `SR09_PRE_RECON/RETURNS/R09/`

Read `00_COMMON_WORKER_CONTRACT.md` first and obey it exactly.

## Assigned exact sources

| source | SHA-256 |
|---|---|
| `WVS Wave 1.sav` | `051bf450568f44181559a5b2bfbe58b4f05b58bc806643d0c63353c937ff0824` |
| `WVS Wave 4.sav` | `c6757ed187655c8b9af88ae4c23c00f066696a641af2f316b4343272ea1d4a0a` |
| `WVS Wave 7.sav` | `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d` |

## Mission

Use WVS Wave 7 as the deeply measured hostile baseline, then determine exactly which burdens transfer to W1/W4 and which are release-specific.

Known W7 facts are evidence, not assumptions about W1/W4.

Determine at minimum:

- physical missing/user-missing declarations across W1/W4/W7;
- candidate respondent identity and country/wave coordinates;
- duplicate/noninjective native-ID hazards analogous to W7 `D_INTERVIEW`, if present;
- design/PSU/weight candidates and cross-wave drift;
- ordered/ranked/repeated question topology;
- recurrent variable-name/label/value-code drift;
- country code and source-scope coordinate evolution;
- ordinary labeled semantic-code candidates;
- exact hostile sentinels for W1 and W4, plus reference to the already-known W7 hostile classes;
- whether W1/W4 reveal any new SAV hazard class not exercised by W7;
- which future WVS certification fixtures can lawfully be shared and which must be wave-specific.

Do not import W7 semantics into W1/W4 merely because variable names or numeric codes resemble one another.

Required success token in `RESULT.json`:

`PRE553_SR09PRE_R09_WVS_RECON_COMPLETE`
