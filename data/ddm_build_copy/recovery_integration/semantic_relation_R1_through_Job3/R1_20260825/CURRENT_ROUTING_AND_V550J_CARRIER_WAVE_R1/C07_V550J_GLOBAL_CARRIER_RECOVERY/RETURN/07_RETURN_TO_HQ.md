# C07 — V550J 2,499 / 15,990 EXACT ROW-CARRIER RECOVERY R1 — RETURN TO HQ

Status: `COMPLETE__EXACT_HISTORICAL_ROW_CARRIER_RECOVERED__NO_SYNTHESIZED_IDENTITIES__NO_J_AUTHORITY_PROMOTION`

Worker branch: `agent/verkhovod-c07-v550j-global-carrier-recovery-r1`  
Exact starting HEAD: `e2f20cc8d442e053e60e10b517601d16fb395297`  
Governing Authority 45: `16a212b7343206c81634b26f2546ad8b60a77475`

## Dispositive recovery

C07 recovered the **pre-existing exact normalized P2 source-structure carrier** from retained Library history. The two original files are:

- `Rawlsing_P2_Normalized_Source_Structure_Registry_v1.csv` — **2,499 rows**, 2,595,849 bytes, SHA-256 `d75d6e30373d1fd45d29ffb34fc14d135c6addf0bbb7aa64d7aed57cf45cd8dd`;
- `Rawlsing_P2_Normalized_Source_Structure_Memberships_v1.csv` — **15,990 rows**, 2,752,901 bytes, SHA-256 `52f10099ce98f9fe9bcf161b80d50b05dfd2f584bb78c3bed007d5055f38980c`.

Those exact SHA-256s are already recorded in the historical tranche-1 section manifest/tree inventory. C07 did not create structure identities, member identities, or rows to satisfy the headline totals. The totals follow from the recovered rows.

The exact recovered carrier is persisted in Library at `/Rawlsing/C07_V550J_GLOBAL_CARRIER_RECOVERY_R1/C07_EXACT_P2_SOURCE_STRUCTURE_CARRIER.tar.xz` (`library_file_id = libfile_cec6f3a01f988191b94a97354d0b9143`). The archive SHA-256 is `1687b4fea789aabf90e3906f104250f4d7bfa0055586a71066598fd9541f0286`. A fresh Library materialization was byte-identical to the local recovery archive. The validator extracts both members and requires the original historical byte hashes and sizes above.

## Row-derived source-family partition

- Afrobarometer: 230 structures / 1,264 memberships
- Arab Barometer: 159 structures / 856 memberships
- Asian Barometer: 71 structures / 479 memberships
- EVS: 182 structures / 1,237 memberships
- GSS: 722 structures / 2,823 memberships
- Latinobarómetro: 123 structures / 680 memberships
- LiTS: 882 structures / 7,878 memberships
- South Asia: 15 structures / 76 memberships
- WVS: 115 structures / 697 memberships

Structure-family rows sum to **2,499**. Membership-family rows sum to **15,990**. The companion partition manifest also gives every family×wave row count; its totals independently reconcile to the same carrier totals.

## Row-integrity proof

Validation PASS establishes from the recovered rows:

- 2,499 unique `source_structure_id` values;
- all 2,499 structure IDs have membership rows and there are zero orphan membership structure IDs;
- every structure's actual membership-row count equals both its `declared_member_count` and `recovered_member_count`;
- declared and recovered member-count sums are both 15,990;
- membership source family and wave agree with the registry for every row;
- each structure's `member_order` is unique and covers exactly `1..N` (physical CSV order is not treated as semantic order);
- zero blank `source_variable_code`, `question_implementation_id`, or `lineage_id` values;
- zero exact duplicate registry rows, zero exact duplicate membership rows, and zero duplicate `(source_structure_id, member_order)` keys.

## Historical reconstruction provenance

The recovered tranche-1 builder documents the lawful carrier construction:

- all nine source-native structure inventories feed the registry;
- membership files are read directly where exposed for Afrobarometer, Asian Barometer, Latinobarómetro, South Asia and LiTS;
- GSS, WVS, EVS and Arab Barometer memberships are recovered from their governing nested source-package ZIPs;
- an earlier exploratory row-range reconstruction was explicitly discarded because it over-included WVS/EVS/Arab members;
- final membership rows are exact source memberships joined to existing implementation and lineage IDs, not identities generated from aggregate counts.

## Authority ceiling preserved

This is a **recovery/adjudication carrier**, not executable V550J authority. Every registry row retains `cross_source_use_status = DISCOVERY_STRUCTURE_ONLY_NOT_J_FAMILY_AUTHORITY`. Historical source-authority statuses likewise remain inventory/reference statuses; C07 changes none of them.

No structure recurrence, shared label, member co-occurrence, or recovered membership is promoted into J-family identity, respondent composition, routing authority, collision authority, or executable V550J registry status. The nineteen historical structure analogies remain provisional search context only.

This is consistent with A10's LMQ-002/LMQ-005 holding: `EXACT_RECOVERY_DENOMINATOR != EXECUTABLE_PRODUCTWIDE_J_AUTHORITY`. C07 closes the **carrier-recovery** dependency only; later V550J courts must adjudicate the recovered rows under exact source-family/routing/member-applicability authority.

## Sibling blindness / noninterference

- C08–C10 consumed: **NO**.
- sibling-current-wave findings consumed: **NO**.
- Archive08 promoted: **NO**.
- routing court performed: **NO**.
- J-family adjudication performed: **NO**.
- production/runtime code mutated: **NO**.

## Return artifacts

Persisted exact carrier:

- Library `/Rawlsing/C07_V550J_GLOBAL_CARRIER_RECOVERY_R1/C07_EXACT_P2_SOURCE_STRUCTURE_CARRIER.tar.xz` — deterministic archive containing both byte-identical recovered historical CSVs; SHA-256 `1687b4fea789aabf90e3906f104250f4d7bfa0055586a71066598fd9541f0286`.

Worker-branch receipts:

- `03_SOURCE_FAMILY_WAVE_PARTITION_MANIFEST.csv` — row-derived family and family×wave counts;
- `04_CARRIER_PROVENANCE_MANIFEST.json` — exact historical hashes, Library source/persisted carrier, authority chain and negative ceiling;
- `05_VALIDATION_RECEIPT.json` — hostile row-integrity + Library roundtrip receipt;
- `06_PROVENANCE_CHAIN.csv` — Authority45/B06–B09/A10/R03/historical-Library/current-carrier chain;
- `validate_c07_v550j_exact_carrier.py` — standalone replay validator accepting a materialized carrier path.

Validation: `PASS`.

Success token: `C07_V550J_EXACT_ROW_CARRIER_RECOVERY_R1_COMPLETE`
