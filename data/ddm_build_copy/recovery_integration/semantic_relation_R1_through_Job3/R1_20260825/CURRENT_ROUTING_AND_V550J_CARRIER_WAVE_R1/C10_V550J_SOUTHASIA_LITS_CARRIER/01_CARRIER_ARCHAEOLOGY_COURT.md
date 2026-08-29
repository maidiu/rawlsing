# C10 — SOUTH ASIA / LiTS V550J SOURCE-FAMILY ROW-CARRIER ARCHAEOLOGY R1

Status: `COMPLETE__EXACT_PRESERVED_ROW_CARRIERS_RECOVERED__NO_FAMILY_OR_ROUTING_ADJUDICATION`

Repository: `maidiu/rawlsing`  
Worker branch: `agent/verkhovod-c10-v550j-southasia-lits-carrier-r1`  
Verified starting HEAD: `e64e70c7cf3559b0c1bf7c166215424604625354`

## Disposition

C10 positively recovered the exact preserved historical row carriers for the South Asia and LiTS portions of the accepted P2 2,499-structure / 15,990-membership reconciliation.

Historical carrier branch/ref:

- branch: `agent/phase-d-rank1-v550j-registry-handoff-return-20260813`
- exact ref inspected: `93fbd1ee96dcc167d578de454ea6cd9bd67d668a`
- commit message: `Record rank one V550J registry authority blocker`

The governing tranche-1 builder at that ref explicitly maps South Asia and LiTS to the four recovered source-package CSVs, reads those exact files, preserves their structure IDs, resolves member endpoints, and emits the normalized all-nine carrier.

The global validation at the same historical ref reports:

- source structures = **2,499**
- structure memberships = **15,990**
- structure inventory count = PASS 2,499/2,499
- structure member endpoints resolved = PASS 15,990/15,990
- all structure memberships match declared = PASS 2,499/2,499
- authority boundary: **no J-family membership, respondent join, registry installation, or runtime execution authorized**

No aggregate count was used to synthesize a South Asia or LiTS row.

## South Asia exact carrier

Preserved structure inventory:

`26_P2_SOUTH_ASIA_PASS1/PACKAGE_CONTENTS/03_SOURCE_STRUCTURES/Rawlsing_P2_South_Asia_Source_Structure_Inventory_v2.csv`

- Git blob: `0aa68f7305009bbea3c3ccdf80eec6d900e6ed3e`
- package SHA-256: `3dc4374164d927949f925e744a6788a4f1ff7a4c4f7426bdc1996b11ec53da17`
- exact rows: **15**
- structure ID is the exact row identity.
- W1: 7 structures / 41 declared memberships
- W2: 8 structures / 35 declared memberships

Preserved membership carrier:

`26_P2_SOUTH_ASIA_PASS1/PACKAGE_CONTENTS/03_SOURCE_STRUCTURES/Rawlsing_P2_South_Asia_Source_Structure_Memberships_v2.csv`

- Git blob: `c788e3545ed8d9c82b7e4b69b61aeecef64c174c`
- package SHA-256: `114f8839a0dd0f3f8e60d07084331938ec35275155a91d2f12d47c3a4f8cb61f`
- exact rows: **76**
- W1: 41
- W2: 35
- no missing referenced structure IDs;
- no declared/recovered member-count mismatch;
- no duplicate structure IDs;
- no duplicate `(structure_id, question_implementation_id, member_order)` membership identities.

Every South Asia structure row carries `authority_status=INVENTORY_ONLY_NOT_J_FAMILY`.

## LiTS exact carrier

Preserved structure inventory:

`27_P2_LITS_PASS1/PACKAGE_CONTENTS/03_SOURCE_STRUCTURES/Rawlsing_P2_LiTS_Source_Structure_Inventory_v2.csv`

- Git blob: `ef729b789580dee6e8399ed5af3c2c26fb656731`
- package SHA-256: `c11fea25f594d13934aa62df1472aabdb0a9b7b75230547487647c9eea3d352b`
- exact rows: **882**
- 2006: 210 structures / 2,130 memberships
- II: 192 structures / 1,320 memberships
- III: 335 structures / 3,057 memberships
- IV: 145 structures / 1,371 memberships

Preserved membership carrier:

`27_P2_LITS_PASS1/PACKAGE_CONTENTS/03_SOURCE_STRUCTURES/Rawlsing_P2_LiTS_Source_Structure_Memberships_v2.csv`

- Git blob: `3e9ce2102f6ae54f73a0f9f6beff6113ed9dc637`
- package SHA-256: `3ba3e7f1e3a3bb040def7317e7282ebb637e2ae62c4bc705dbf6cd33b38a47f8`
- exact rows: **7,878**
- 2006: 2,130
- II: 1,320
- III: 3,057
- IV: 1,371
- no missing referenced structure IDs;
- no declared/recovered member-count mismatch;
- no duplicate structure IDs;
- no duplicate `(structure_id, question_implementation_id, member_order)` membership identities.

Every LiTS structure row carries `authority_status=INVENTORY_ONLY_NOT_J_FAMILY`.

## Exact global reconciliation binding

The historical builder:

`32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1/build_p2_global_reconciliation_tranche1.py`

directly binds:

- `STRUCT_INV['South Asia']` to the recovered South Asia inventory;
- `STRUCT_MEM['South Asia']` to the recovered South Asia membership carrier;
- `STRUCT_INV['LiTS']` to the recovered LiTS inventory;
- `STRUCT_MEM['LiTS']` to the recovered LiTS membership carrier.

Its normalization preserves each historical structure ID as `source_structure_id`. For these exposed membership files it marks recovered membership rows as `EXPOSED_GOVERNING_MEMBERSHIP_FILE`, resolves exact question implementation IDs, deduplicates only exact `(source_structure_id, question_implementation_id)` duplicates, and validates recovered member counts against each declared structure count.

The validated global carrier identities are:

- `Rawlsing_P2_Normalized_Source_Structure_Registry_v1.csv`
  - Git blob: `c7953f1463bc898bdef8f368eb7ebf721630b2e7`
  - SHA-256: `d75d6e30373d1fd45d29ffb34fc14d135c6addf0bbb7aa64d7aed57cf45cd8dd`

- `Rawlsing_P2_Normalized_Source_Structure_Memberships_v1.csv`
  - Git blob: `7dfe564753f9385ff459513cefd174fc4496bc64`
  - SHA-256: `52f10099ce98f9fe9bcf161b80d50b05dfd2f584bb78c3bed007d5055f38980c`

C10 does not reconstruct those global CSVs from counts. It recovers the exact source-family input carriers that the validated global build consumed.

## Materialization

C10 materializes byte-identical copies of the four preserved historical row carriers under `PRESERVED_CARRIER/`.

The post-commit receipt must verify that each copied Git blob equals its historical source Git blob. Blob equality is the exact byte-preservation proof for this Git materialization.

## Negative ceiling

C10 does not:
- adjudicate whether any recovered structure is a V550J family;
- adjudicate routing or member applicability;
- use or inspect sibling C07-C09 returns;
- use Archive08;
- infer structures from R14 similarity, adjacency, variable prefixes, common wording, or aggregate counts;
- convert `INVENTORY_ONLY_NOT_J_FAMILY` into executable authority;
- claim the global 2,499/15,990 recovery denominator is itself product authority.

Carrier recovery only.

`C10_SOUTHASIA_LITS_V550J_CARRIER_RECOVERY_R1_COMPLETE`
