# SUB-VOZHD D — OBL009 J01-B GSS HISTORICAL SUCCESSION R1 — RESULT

Status: `PASS__SUBV_D_OBL009_J01B_GSS_SUCCESSION_CURRENT_GRAIN_R1`

Worker branch: `agent/rabochii-subv-d-obl009-j01b-gss-succession-r1`  
Starting HEAD / command commit: `ba90a8a107c2dcc4e8867977943f0f41c41acee2`  
Commissioning ancestry: `66686d7a97fad4310e1b6b390ab3d787d2929e88`

This return classifies **GSS historical succession only**. It does not mutate J01-A, consume sibling J01-B returns, close global J01-B, or create project-current authority.

## Frozen/current materialization

Fresh materialization of the exact frozen J01-A candidate carrier verified:
- Library `libfile_3f6b0d93bb74819195702d808e3093ec` / file `file_000000005144822fa27f7502f6e9307b`
- 1,411 global candidates / 1,641,446 bytes
- SHA-256 `b21a79947f19f4c520ea493480a38ef8b23cb6797444eeb913bc8575b6cafb64`

Mechanical family filtering yields **662 GSS current candidates**; the exact carrier has one row per candidate.

## Admitted historical materialization

C07 exact carrier was freshly materialized from Library archive `libfile_cec6f3a01f988191b94a97354d0b9143` and verified:
- archive SHA-256 `1687b4fea789aabf90e3906f104250f4d7bfa0055586a71066598fd9541f0286`
- registry: 2,499 rows / SHA-256 `d75d6e30373d1fd45d29ffb34fc14d135c6addf0bbb7aa64d7aed57cf45cd8dd`
- memberships: 15,990 rows / SHA-256 `52f10099ce98f9fe9bcf161b80d50b05dfd2f584bb78c3bed007d5055f38980c`

Mechanical GSS filtering yields **722 historical GSS structures / 2,823 memberships** and independently reproduces C08's committed partition blobs exactly:
- structures `f50b7cd8aa7056287cab8103886537d31485beac`
- memberships `79c29e1e07a2d581b47238d4924ca8f0735796ee`

## Succession adjudication

Current GSS candidates (662 total):
- `CURRENT_SUCCESSOR_CHANGED_SCOPE`: 120
- `CURRENT_SUCCESSOR_CHANGED_MEMBERSHIP_AND_SCOPE`: 107
- `AMBIGUOUS_SUCCESSION`: 28
- `UNRESOLVED_IDENTITY`: 198
- `CURRENT_NEW_STRUCTURE`: 209
- `EXACT_CURRENT_SUCCESSOR`: 0
- `CURRENT_SUCCESSOR_CHANGED_MEMBERSHIP`: 0

The zero exact-successor count is substantive: historical GSS is wave-scoped while every frozen current GSS candidate carries finer module/form/split scope. Exact member-set continuities therefore remain scope-changed.

Identity rules are conservative:
1. exact relation: same wave + exact native member-code set + exact question-implementation-id set;
2. changed membership: strict exact containment + a **unique** nonblank historical structure label prefixing every current member code;
3. multiple structural anchors => `AMBIGUOUS_SUCCESSION`;
4. overlap without structural identity => `UNRESOLVED_IDENTITY`;
5. `CURRENT_NEW_STRUCTURE` only when the exact admitted same-wave historical carrier has zero member/qimpl overlap.

No identity is inferred from label equality alone, variable number, adjacency, file co-location, member overlap alone, or historical count targets.

## Historical-capital conservation

- admitted historical GSS structures: 722
- referenced by current exact/changed/ambiguous relations: 137
- residual-disposed exactly once: 585
- conservation: `137 + 585 = 722`

Residuals: `HISTORICAL_ONLY` 473; `UNRESOLVED_HISTORICAL_IDENTITY` 112.

## Exact carrier transport

The write channel could not stream the multi-megabyte plaintext carriers directly from the execution container, and Library was at quota. No rows were dropped. The five exact CSV carrier bytes are therefore packed **inside Git** as deterministic `EXACT_RETURN_CARRIERS.tar.xz`, encoded across 6 base64 part files.

- packed archive SHA-256: `b414235e8e7cc22a9de97f98807805c94e4aa1a8ceea84c4a0edbbd3485e54ac`
- base64 parts: 6 / total base64 chars 102316
- reconstruct: `cat EXACT_RETURN_CARRIERS.tar.xz.b64.part* | base64 -d > EXACT_RETURN_CARRIERS.tar.xz`
- extract: `tar -xJf EXACT_RETURN_CARRIERS.tar.xz`

The required large CSV paths in Git are transport receipts binding archive member name, exact row count, byte count and SHA-256. Extraction yields the exact required carriers:
- `CURRENT_SUCCESSION_CROSSWALK.csv` — rows 662, bytes 599193, SHA-256 `ca34a1145c346b9fde477364e983356aab41b2bde4f365e2c1aaf522012bf098`
- `HISTORICAL_RESIDUAL_DISPOSITION.csv` — rows 585, bytes 308049, SHA-256 `3f9bbdcba880a383184632c3f806516b1b863577ac584cce4b966545f86362b0`
- `MATCH_EVIDENCE_MANIFEST.csv` — rows 703, bytes 973361, SHA-256 `f5bab95a3d93d3a78f7c95e073514d684f1981be2bdc4e4cf22d2690017c58a5`
- `AMBIGUITIES.csv` — rows 338, bytes 198578, SHA-256 `294e9920755a4faaa6ad7c276c9f8b42db52a242dd34577cc68bf9250a1fa537`
- `CURRENT_FREEZE_REVIEW_REQUESTS.csv` — rows 0, bytes 126, SHA-256 `b6b6332a3d8e5d35a2d1346f196d40b57818ef826f327fbdbd1ec13b9a3f1726`

`CURRENT_FREEZE_REVIEW_REQUESTS.csv` is also stored directly because it is small; it contains 0 requests. J01-A remains untouched.

## Authority ceiling

`CANDIDATE != PROJECT_CURRENT`.

Lane PASS proves only the GSS succession carrier at current grain. Global J01-B still requires all five family lanes followed by the separate sibling-consuming join/collision/completeness court.

Terminal:

`PASS__SUBV_D_OBL009_J01B_GSS_SUCCESSION_CURRENT_GRAIN_R1`
