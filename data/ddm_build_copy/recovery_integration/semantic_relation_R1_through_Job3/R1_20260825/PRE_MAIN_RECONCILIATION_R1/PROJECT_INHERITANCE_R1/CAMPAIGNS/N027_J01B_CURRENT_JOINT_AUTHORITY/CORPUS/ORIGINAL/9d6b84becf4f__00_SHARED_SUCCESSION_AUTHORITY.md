# J01-B R1 — HISTORICAL SUCCESSION CROSSWALK SHARED AUTHORITY

Status: `BINDING_CAMPAIGN_WORKER_CONTRACT__CURRENT_DENOMINATOR_FROZEN__HISTORY_NOW_ADMITTED_FOR_SUCCESSION_ONLY`

Repository: `maidiu/rawlsing`
Frozen J01-A return: `44e97e420d38b6a2b0c44034929b5994a352d8b6`

## 1. Frozen current denominator
J01-A is closed and immutable for this phase.

Current source universe:
- rows: 1,879
- Library: `libfile_3b7ee9030f4c8191bd59fac79d2d10c6`
- SHA-256: `d74ce5266daa007c6500385922d4f66de962ab5cf8a388bbbc60cd540f6656d2`

Current J-candidate universe:
- rows: 1,411
- Library: `libfile_3f6b0d93bb74819195702d808e3093ec`
- SHA-256: `b21a79947f19f4c520ea493480a38ef8b23cb6797444eeb913bc8575b6cafb64`

Historical evidence may now be opened only to classify succession relative to that frozen current denominator.

`HISTORICAL DENOMINATOR != CURRENT DENOMINATOR`
`HISTORICAL SURVIVAL != CURRENT AUTHORITY`
`CURRENT DENOMINATOR IS NOT REOPENED BY J01-B`

No J01-B worker may add, delete, merge, split, or otherwise alter a current J01-A candidate because of historical evidence. If history reveals a possible current-source mistake, record `CURRENT_FREEZE_REVIEW_REQUESTED` as a separate exception and do not mutate the denominator.

## 2. Exact admitted historical evidence
J01-B may consume only the exact frozen historical recovery/corroboration returns:
- C07 global historical V550J carrier: `277d1a88e720ab5b5dbedf3daf41821656435b3f`
- C08 GSS/WVS/EVS corroboration: `f24a90be78e11c0a234fdc4a14cbafe60390c1f8`
- C09 Arab/Afro/Asian/Latin archaeology/corroboration: `b41957482a3c567a02862334806624910fd4bac5`
- C10 South Asia/LiTS corroboration: `03de44e4232df9a9c709f60eb3f8c8b628eb034a`

Workers may consume exact historical carrier bytes, manifests, crosswalks, source-structure identities, member lists, scope metadata, provenance and corroboration contained in those frozen returns. They may not search outside those refs for additional historical answers unless the lane command explicitly authorizes a named current/historical identity artifact solely to resolve a crosswalk ambiguity.

## 3. J01-B question
For each frozen current J candidate, determine the strongest historically-supported succession state without granting history authority over current existence or candidacy.

Allowed current-candidate succession states:
- `EXACT_CURRENT_SUCCESSOR`
- `CURRENT_SUCCESSOR_CHANGED_MEMBERSHIP`
- `CURRENT_SUCCESSOR_CHANGED_SCOPE`
- `CURRENT_SUCCESSOR_CHANGED_MEMBERSHIP_AND_SCOPE`
- `CURRENT_NEW_STRUCTURE`
- `AMBIGUOUS_SUCCESSION`
- `UNRESOLVED_IDENTITY`

For historical structures not matched to a current candidate, allowed residual states:
- `HISTORICAL_ONLY`
- `RETIRED_OR_OUT_OF_CURRENT_SCOPE`
- `AMBIGUOUS_HISTORICAL_RESIDUAL`
- `UNRESOLVED_HISTORICAL_IDENTITY`

Do not force one-to-one identity. Lawful relations may be 1:1, historical-1:current-many, historical-many:current-1, or unresolved where scope/member evolution requires it. Every claimed relation must preserve exact identity reasoning and provenance.

## 4. Match dimensions
Evaluate at minimum:
- source family;
- wave/current scope and historical wave/scope identity;
- source-native structure type/label/locator where available;
- exact or normalized source-native member identities;
- exact current and historical member sets;
- country/form/module/split scope;
- source evidence provenance;
- explicit crosswalk/corroboration evidence;
- whether apparent similarity is merely shared naming/adjacency.

No relation may be promoted solely from:
- same label;
- same variable number;
- same file;
- adjacency;
- overlapping members without structure identity;
- family-level count similarity;
- historical expected totals.

## 5. Required lane outputs
Each lane must emit:
1. `RESULT.md`
2. `CURRENT_SUCCESSION_CROSSWALK.csv` — exactly one row per frozen current candidate in lane
3. `HISTORICAL_RESIDUAL_DISPOSITION.csv` — every admitted lane historical structure not consumed by a current succession relation, exactly once
4. `MATCH_EVIDENCE_MANIFEST.csv`
5. `AMBIGUITIES.csv`
6. `CURRENT_FREEZE_REVIEW_REQUESTS.csv`
7. `COUNTS.json`
8. `VALIDATION.json`
9. `CHANGED_FILES.txt`
10. `RETURN_POINTER.json`

Large exact carriers may live in ChatGPT Library if Git transport is unsafe; Git must bind exact Library ID/path/rows/bytes/schema/SHA-256.

## 6. Current crosswalk schema minimum
For each current candidate include at least:
- `current_source_structure_id`
- `source_family`
- `wave_or_scope`
- `current_member_ids_or_native_members`
- `succession_state`
- `matched_historical_structure_ids`
- `historical_member_identity_or_set`
- `historical_scope`
- `membership_relation`
- `scope_relation`
- `match_basis`
- `historical_evidence_ref`
- `historical_evidence_hash_or_locator`
- `ambiguity_or_gap`
- `confidence_class`

Every current candidate must appear exactly once in the lane crosswalk, even if its state is `CURRENT_NEW_STRUCTURE` or `UNRESOLVED_IDENTITY`.

## 7. Historical residual completeness
Every admitted historical structure in lane jurisdiction must be either:
- referenced by at least one current succession crosswalk row; or
- emitted exactly once in `HISTORICAL_RESIDUAL_DISPOSITION.csv`.

This is historical-capital conservation, not current-denominator authority.

## 8. Sibling blindness
Each lane consumes only:
- this shared authority;
- the frozen J01-A global carriers and manifests;
- exact admitted C07-C10 returns needed by its assigned source families;
- its own lane outputs.

Do not consume sibling J01-B lane results.

## 9. Validation
Each lane must prove:
- exact current lane candidate count derived from frozen J01-A carrier;
- every current candidate exactly once;
- no out-of-lane current candidate;
- every admitted lane historical structure either matched or residual-disposed;
- no duplicate current crosswalk IDs;
- no historical evidence used to mutate current candidacy;
- no historical count-to-identity inference;
- exact evidence references/hashes/locators;
- all ambiguity typed rather than guessed.

## 10. Global phase
Lane completion does not freeze J01-B. After all family lanes return, SUB-VOZHD dispatches one deterministic sibling-consuming global J01-B join/collision/completeness court.

`LANE SUCCESSION COMPLETE != GLOBAL J01-B COMPLETE`

Only after global J01-B passes may SUB-VOZHD freeze `CURRENT_JOINT_AUTHORITY_CONTRACT@1` and release J02-J05.
