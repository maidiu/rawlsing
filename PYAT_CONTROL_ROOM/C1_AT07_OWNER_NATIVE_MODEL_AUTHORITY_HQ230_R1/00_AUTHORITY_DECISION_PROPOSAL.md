# C1 AT07 OWNER-NATIVE MODEL AUTHORITY — HQ230 R1 CANDIDATE

Status: `CANDIDATE_NOT_ADOPTED__READY_FOR_HOSTILE_REVIEW`

Disposition proposed to reviewer:
`C1_OWNER_NATIVE_MODEL_AUTHORITY_CANDIDATE_COMPLETE__READY_FOR_HOSTILE_REVIEW`

This packet does not edit implementation, adopt authority, promote a current selection, or reinterpret the historical fixture-only ref.

## Decision

HQ230 selects:

- **D1: A, with a non-genealogical explicit crosswalk.** The fixture ref remains exactly fixture-only. A distinct owner-native authority id is proposed. Because the fixture ref is not an owner-native PRE553 snapshot, it is evidence/predecessor in the semantic-history sense only; it is not inserted into `parent_authority_refs` or `supersession_refs`.
- **D2: new bounded authority kind** `POSITIONED_SUBJECT_EMPIRICAL_POSSIBILITY_MODEL_RULE`.
- **D3: new narrow governed family** `PositionedSubjectModelRule@1.0.0`. The already-deferred `PositionedSubjectEmpiricalPossibilityField` is not promoted by this decision.
- **D4: exact candidate authority material is frozen below.** Seal-time outer custody remains lifecycle-derived exactly as current AuthorityMaintenance law requires.
- **D5: Option B — separate exact model-rule determinant.** This is selected because the current determinant graph natively supports `AuthorityRef -> ExactRef -> dependent` propagation, and because it cleanly separates stable model law from per-invocation source-universe and walkback determinants.
- **D6: N10E wakes only after implementation of the new kind/family and hostile approval/adoption of this candidate.**

## Exact proposed identities

Owner-native authority:
`C1-AT07-POSITIONED-SUBJECT-MODEL-RULE@1.0.0 | db0060afb25dfcf7f77b35864c2dd2499e974057aca73a252a208fb93ed2fc65`

Stable model-rule object:
`PositionedSubjectModelRule@1.0.0 | urn:rawlsing:pre553:PositionedSubjectModelRule:sha256:59e82a51b26cca26aff84e42878c1c8f1c0c52e4ad4e26a5b23244999454add2 | 59e82a51b26cca26aff84e42878c1c8f1c0c52e4ad4e26a5b23244999454add2`

Replay protocol:
`PositionedSubjectModelRuleReplayProtocol@1 | urn:rawlsing:pre553:positioned-subject-model-rule-replay:sha256:4ea14ebe4f724e05a0d2560ae7f19b3f4d48522a1bd9750b0544ed976248a08e | 4ea14ebe4f724e05a0d2560ae7f19b3f4d48522a1bd9750b0544ed976248a08e`

Fixture crosswalk:
`C1FixtureModelAuthorityCrosswalk@1 | urn:rawlsing:pre553:c1-fixture-model-crosswalk:sha256:4eb8aaaaef078cc7c3da32c5232aa62b45692ec0ffb7867a0376e9a7c47071f0 | 4eb8aaaaef078cc7c3da32c5232aa62b45692ec0ffb7867a0376e9a7c47071f0`

Candidate record projection:
`Maintenance:CANDIDATE | urn:rawlsing:pre553:maintenance:candidate:sha256:dd8bdcb2181282d264793293c592a7b401c268a774faf7b15a08d89f3287c10e | dd8bdcb2181282d264793293c592a7b401c268a774faf7b15a08d89f3287c10e`

## Why this is bounded rather than an architecture reopen

No accepted model semantics change. No person/V3 boundary changes. No walkback ownership changes. No source-composition or comparability permission is created. The generic AuthorityMaintenance lifecycle and SemanticDeterminantGraph need no new cross-node law: the candidate uses their existing authority-edge and exact dependency-edge semantics.

The only ontology additions later required are one exact authority kind, one exact rule family/state, and bounded consumption/graph wiring.

## Productive adequacy

HQD-216 makes a permanent typed refusal insufficient where a productive owner can lawfully be supplied. This candidate supplies the missing bounded owner representation without claiming live-source occupancy. AT17/AT18/AT19 still require their own executed proof after implementation.

This packet remains candidate authority until independently reviewed and explicitly adopted.
