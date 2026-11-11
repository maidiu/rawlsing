# SR09-PRE R07 — LiTS FAMILY RECONNAISSANCE

Status: `AUTHORIZED__NON_DISPOSITIVE__HIGH_PRIORITY`
Branch: `agent/vozhd-trii-sr09pre-r07-lits`
Write only: `SR09_PRE_RECON/RETURNS/R07/`

Read `00_COMMON_WORKER_CONTRACT.md` first and obey it exactly.

## Assigned exact sources

| source | SHA-256 | frozen reader compatibility |
|---|---|---|
| `LiTS_I.dta` | `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09` | `latin1`, compatibility-execution only |
| `LiTS_II.dta` | `c43d0e1821c51398817d7dfdfad2c0a4a5bb0d492f6a58096670e623bb6130e9` | `latin1`, compatibility-execution only |
| `LiTS_III.dta` | `368ae5d07a44975a2f0a9ce3b1e564988a966b2632e28075c56a24d60065bcc8` | `latin1`, compatibility-execution only |
| `LiTS_IV.dta` | `14e1032755c4f42d8d3dc61647097ccd7605ba281551e53953c76d22a223cd1c` | `latin1`, compatibility-execution only |

## Mission

Build an adversarial future-certification burden across all four LiTS releases using LiTS I as a known hostile baseline, while independently measuring II/III/IV rather than assuming the same behavior.

The frozen `latin1` reader configuration is compatibility-execution only and is not source-text semantic authority.

Determine at minimum:

- native respondent-ID candidates, uniqueness, null behavior, and cross-release identity changes;
- country/countryname and other source-scope coordinate systems, including any coding changes analogous to the known LiTS-I country hazard;
- Stata system missing and any extended missing behavior;
- ordinary numeric/string values carrying labels suggestive of DK/refusal/N/A, kept as semantic candidates only;
- all weight/design candidates and exact missing-state behavior;
- encoding/text metadata hazards and fields whose decoded text remains authority-limited;
- variable/value-label/storage/display-format drift across I/II/III/IV;
- routing/module/repeated/ranked structures physically represented;
- exact hostile sentinels for every distinct DTA hazard class;
- whether LiTS II/III/IV expose any new physical class beyond the frozen DTA contract.

Explicitly compare II/III/IV against the already-measured LiTS-I hazards, but do not assume LiTS-I code mappings or country semantics transfer across releases.

Required success token in `RESULT.json`:

`PRE553_SR09PRE_R07_LITS_RECON_COMPLETE`
