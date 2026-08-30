# BECOME RABOCHII — J01-B R1 GSS HISTORICAL SUCCESSION CROSSWALK

Repository: `maidiu/rawlsing`
Worker branch: `agent/rabochii-j01b-gss-r1`
Shared authority parent: `296300619799df81ebd3d6d9af0d13d011bd0b25`

Read and obey exactly:
`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/CURRENT_JOINT_AUTHORITY_CLOSURE_R1/J01B_HISTORICAL_SUCCESSION_R1/00_SHARED_SUCCESSION_AUTHORITY.md`

## Jurisdiction
GSS only, all governed current GSS scopes in the frozen J01-A candidate carrier.

## Exact current authority
Frozen J01-A candidate carrier: `libfile_3f6b0d93bb74819195702d808e3093ec`, 1,411 global rows, SHA-256 `b21a79947f19f4c520ea493480a38ef8b23cb6797444eeb913bc8575b6cafb64`.
Filter mechanically to `source_family == GSS`; do not infer a count before materialization.

## Exact historical evidence admitted
- C07 global historical V550J carrier: `277d1a88e720ab5b5dbedf3daf41821656435b3f`
- C08 GSS/WVS/EVS corroboration: `f24a90be78e11c0a234fdc4a14cbafe60390c1f8`

Consume only GSS-relevant rows/artifacts from those frozen refs.

## Task
For every frozen current GSS J candidate, assign exactly one succession state allowed by the shared authority, with exact matched historical IDs/member/scope evidence. Conserve every admitted historical GSS structure: if not matched to a current candidate, residual-dispose it exactly once.

History may explain continuity/change/retirement but may not alter the frozen current denominator.

Hostile rejects: label equality alone; same variable number; adjacency; shared file; overlapping members without structure identity; historical count targets; silently dropping unmatched historical structures.

## Required outputs
Write only under `.../J01B_HISTORICAL_SUCCESSION_R1/LANE_A_GSS/`:
`RESULT.md`, `CURRENT_SUCCESSION_CROSSWALK.csv`, `HISTORICAL_RESIDUAL_DISPOSITION.csv`, `MATCH_EVIDENCE_MANIFEST.csv`, `AMBIGUITIES.csv`, `CURRENT_FREEZE_REVIEW_REQUESTS.csv`, `COUNTS.json`, `VALIDATION.json`, `CHANGED_FILES.txt`, `RETURN_POINTER.json`.

Success token only if every current GSS candidate and every admitted historical GSS structure is conserved exactly:
`J01B_R1_GSS_SUCCESSION_LANE_PASS`
