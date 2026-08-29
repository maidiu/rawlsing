# C08 — GSS / WVS / EVS V550J SOURCE-FAMILY ROW-CARRIER ARCHAEOLOGY R1

Status: `PASS__EXACT_ROW_CARRIER_RECOVERED_FOR_ALL_ASSIGNED_FAMILIES`

Repository: `maidiu/rawlsing`  
Worker branch: `agent/verkhovod-c08-v550j-gss-wvs-evs-carrier-r1`  
Verified starting HEAD: `a7f481383cdb651fbc39370ed8c64ff0512b09ed`

## Holding

C08 located the exact serialized historical carrier that underlies the accepted post-Archive08 V550J reconstruction denominator:

- `2,499` source-structure rows;
- `15,990` exact membership rows.

The carrier is not reconstructed from those counts.

It is the pair of serialized objects at historical handoff ref:

`93fbd1ee96dcc167d578de454ea6cd9bd67d668a`

- `Rawlsing_P2_Normalized_Source_Structure_Registry_v1.csv`
  - Git blob `c7953f1463bc898bdef8f368eb7ebf721630b2e7`
  - manifest SHA-256 `d75d6e30373d1fd45d29ffb34fc14d135c6addf0bbb7aa64d7aed57cf45cd8dd`
  - 2,499 rows / 2,499 unique structure IDs.
- `Rawlsing_P2_Normalized_Source_Structure_Memberships_v1.csv`
  - Git blob `7dfe564753f9385ff459513cefd174fc4496bc64`
  - manifest SHA-256 `52f10099ce98f9fe9bcf161b80d50b05dfd2f584bb78c3bed007d5055f38980c`
  - 15,990 rows / 2,499 referenced structure IDs.

The tranche's own authority boundary states that memberships for GSS, WVS, EVS and Arab Barometer came from governing exposed/nested source-package membership files and that **no row-range reconstruction was used**. Its report states earlier exploratory row-range recovery for WVS/EVS/Arab was discarded.

Independent later R03 archaeology at `391114916ded6cf607eb4ab77d7c4cdf012bb1c5` separately preserves `2,499 raw source structures / 15,990 memberships` as the governing reconstruction denominator after Archive08 quarantine.

## Exact C08 source partitions

Rows were selected only by the literal serialized `source_family` value. Original row identity fields and order are preserved.

### GSS

- structures: **722**
- memberships: **2,823**
- waves:
  - 1972: 16 / 59
  - 1973: 39 / 145
  - 1984: 70 / 345
  - 1993: 97 / 394
  - 2002: 126 / 467
  - 2010: 99 / 397
  - 2016: 132 / 495
  - 2024: 143 / 521

### WVS

- structures: **115**
- memberships: **697**
- waves:
  - W1: 20 / 134
  - W4: 39 / 245
  - W7: 56 / 318

### EVS

- structures: **182**
- memberships: **1,237**
- waves:
  - 1981: 40 / 274
  - 1990: 29 / 239
  - 1999: 49 / 281
  - 2008: 27 / 219
  - 2017: 37 / 224

Assigned total: **1,019 structures / 4,757 memberships**.

These are output counts after exact row filtering, never selection denominators.

## Carrier integrity

For each assigned family:

- source-structure IDs are unique;
- every recovered structure has membership rows;
- every membership references a recovered same-family structure;
- no orphan membership exists;
- serialized `recovered_member_count` equals exact membership row count;
- serialized `declared_member_count` equals recovered member count;
- every structure is `membership_recovery_status=COMPLETE`;
- `member_order` is contiguous from 1 through N.

All checks: **PASS**.

## Recovered row files

C08 materializes six deterministic source-family carrier subsets:

- `RECOVERED_GSS_SOURCE_STRUCTURES.csv`
- `RECOVERED_GSS_SOURCE_STRUCTURE_MEMBERSHIPS.csv`
- `RECOVERED_WVS_SOURCE_STRUCTURES.csv`
- `RECOVERED_WVS_SOURCE_STRUCTURE_MEMBERSHIPS.csv`
- `RECOVERED_EVS_SOURCE_STRUCTURES.csv`
- `RECOVERED_EVS_SOURCE_STRUCTURE_MEMBERSHIPS.csv`

They are documentary carrier copies, not new authority.

## Typed missing preimages

The earlier nested source-package membership preimage files are not separately Git-addressable on the inspected historical tree. This is recorded as:

`NOT_SEPARATELY_GIT_MATERIALIZED__SERIALIZED_EXACT_ROWS_RECOVERED`

for GSS, WVS and EVS.

That state does not block C08 carrier recovery because the exact normalized rows, their full-carrier hashes, validation, and provenance statement are serialized and independently recoverable. C08 does not invent ZIP names or paths.

## Forbidden inferences preserved

No family authority was adjudicated.  
No routing/member-applicability authority was adjudicated.  
No R14 similarity was used.  
No bounded-canary rows were substituted.  
No Archive08 material was promoted.  
No C07 sibling return was inspected.  
No count-to-row reconstruction occurred.

`CARRIER_RECOVERED != V550J_FAMILY_AUTHORITY`

## HQ return

At the C08 carrier grain:

`GSS_V550J_RAW_ROW_CARRIER = RECOVERED`

`WVS_V550J_RAW_ROW_CARRIER = RECOVERED`

`EVS_V550J_RAW_ROW_CARRIER = RECOVERED`

`C08_GSS_WVS_EVS_V550J_CARRIER_RECOVERY_R1_COMPLETE`
