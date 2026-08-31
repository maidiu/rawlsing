# J01-A R4 — GLOBAL CURRENT-ONLY JOIN / COLLISION / COMPLETENESS / FREEZE COURT

Status: `PASS__FROZEN`

Success token: `J01A_CURRENT_ONLY_GLOBAL_FREEZE_PASS`

## Frozen current-only denominators

- `CURRENT_SOURCE_STRUCTURE_UNIVERSE`: **1,879** exact current source structures.
- `CURRENT_J_CANDIDATE_UNIVERSE`: **1,411** exact current J candidates.
- Current families: **9/9**. Governed scopes: **35/35**.

The denominators were derived from exact materialized rows. The prior 1,879 / 1,411 arithmetic was treated only as a hostile post-derivation check and was not used to add, delete, or stop identity discovery.

## Immutable freeze transport

The two frozen carriers were uploaded into `/J01A_CURRENT_ONLY_GLOBAL_FREEZE_R4/`, then rematerialized and re-hashed byte-for-byte.

- Source carrier: `libfile_3b7ee9030f4c8191bd59fac79d2d10c6` / `file_00000000e28c822f86958de710573152`; 1,879 rows; 2,268,501 bytes; SHA-256 `d74ce5266daa007c6500385922d4f66de962ab5cf8a388bbbc60cd540f6656d2`.
- Candidate carrier: `libfile_3f6b0d93bb74819195702d808e3093ec` / `file_000000005144822fa27f7502f6e9307b`; 1,411 rows; 1,641,446 bytes; SHA-256 `b21a79947f19f4c520ea493480a38ef8b23cb6797444eeb913bc8575b6cafb64`.

Both round-trip hashes and row counts match exactly. The 1,870-row global source-evidence manifest is also Library-bound at `libfile_4ff56bd0bc4881919155590b15180c09` / `file_00000000f030822fb09d5822b8d815e7`, 589,324 bytes, SHA-256 `09c30143de456e82afa254cdd1121dc9ca171dfa71298e19fff9dbdbec9af50a`, and passed the same rematerialization/rehash gate. The 37-row global source-gap ledger is Library-bound at `libfile_d032817f535c81918a6318165011762a` / `file_00000000eeac822f90e2a464b92acdf1`, 37,016 bytes, SHA-256 `cefb323e82c13bd58b64b7060b2856d37e33582781d7d7dd5d7e4b63b573271c`, also round-trip verified.

## Global collision and subset court

- Duplicate `current_source_structure_id`: **0**.
- Duplicate deterministic global identity SHA-256: **0**.
- Candidate IDs absent from source universe: **0**.
- Candidacy-derived candidates vs union of exact terminal lane candidate carriers: **1,411 / 1,411 byte-semantic core matches**.
- Cross-family leakage: **0**.
- Superseded Asian R2 rows retained: **0**. Asian R3 is terminal.

## WVS R3 patch

The exact 110-row WVS patch was independently reconstructed from the exact R2 WVS rows plus the R3 terminal rules and hashes to the pinned SHA-256 `7cbaa3fbf0ec93a68247612f4059fe66456ab537e8ad980e27990066a1289638`. Every one of 110 WVS source IDs is hit exactly once and all 110 R2 binding-payload hashes re-compute exactly. Binding-change count is zero.

Terminal WVS disposition: 78 exact bindings preserved; 27 W1 typed canonical-crosswalk gaps; 1 W4 V77 partial binding; 4 W7 MENA current-source / governed-catalog nonmembership gaps. WVS candidacy remains exactly **109 / 110**.

## Completeness, candidacy, binding gaps

All 35 governed current scopes are complete at the available current-source authority ceiling or carry an exact typed source/member ceiling. Missing current-member authority and missing source bytes were never converted into non-J or structural absence. The merged global source-gap ledger contains **37** exact terminal gap entries.

Candidacy dispositions:
- `CURRENT_J_CANDIDATE`: 1,411
- `SOURCE_GROUPING_ONLY_NON_J`: 318
- `UNRESOLVED_CANDIDACY`: 108
- `ADMINISTRATIVE_GROUP`: 42

Member-binding state: 1,827 rows retain exact member binding; 52 rows retain nonexact/partial typed member-binding states. Sixty rows have a nonempty binding/scope-gap field because eight exact-binding rows also preserve an independent scope gap.

## R1 provisional lineage-loss ruling

Authority 01 Section 3 passes **8 / 8** conditions. The original frozen 299/257 R1 carrier bytes remain genuinely unrecoverable, and **zero** missing R1 semantic rows were reconstructed or inferred. The derivative procedural lineage requirement is lawfully retired under permanent code:

`R1_PROVISIONAL_LINEAGE_UNRECOVERABLE_STORAGE_ARTIFACT`

This is explicitly not a claim of recovered R1 lineage.

## Blindness and release

Historical J evidence remained sealed throughout denominator formation. No C07/C08/C09/C10 carrier contents, historical 2,499/15,990 identities as targets, historical V550J/P2 J memberships, or Archive08 promoted answers were consumed.

**J01-A is frozen. J01-B is lawfully releasable by SUB-VOZHD. This worker does not perform J01-B.**
