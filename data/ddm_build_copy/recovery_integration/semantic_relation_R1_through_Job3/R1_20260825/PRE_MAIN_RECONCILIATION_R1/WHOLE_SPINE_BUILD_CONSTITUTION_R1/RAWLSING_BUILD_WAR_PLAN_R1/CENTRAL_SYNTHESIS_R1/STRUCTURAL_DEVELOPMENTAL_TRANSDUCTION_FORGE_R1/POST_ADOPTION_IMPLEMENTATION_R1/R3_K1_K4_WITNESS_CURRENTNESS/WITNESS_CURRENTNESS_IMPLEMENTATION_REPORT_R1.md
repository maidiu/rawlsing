# WITNESS CURRENTNESS IMPLEMENTATION REPORT R1

Status: `IMPLEMENTED__FOCUSED_G3_INTERFACE`

## Production implementation identity

`rawlsing_next/sdtf_r4_witness_currentness.py`

Tested Git blob identity of the implementation content:
`06c8a2259436e7209bad4e4b3f8c314b18446fe6`

The module provides:

- orthogonal assertion-axis enums and `AssertionRequestR1`;
- proof-visible `CurrentnessCheckR1` and `WitnessCurrentnessEvidenceR1` adapter surface;
- `evaluate_witness_currentness_r1` fail-closed currentness evaluation;
- `TypeSpecificWitnessAdapterR1` protocol over native owner witness/state records;
- exact K4 Path-A and Path-B evidence surfaces;
- `adjudicate_assertion_r1` proof adjudication with explicit negative-proof separation;
- first-failing-role visibility for replacement/revocation/unknown currentness;
- no actor-fact constructor, no source-authority constructor, and no universal witness record.

## Reuse disposition

The implementation does not mutate or replace the frozen reuse surfaces:

- `rawlsing_next/v3_contact_witness_independence_source_authority_candidate_r2.py` blob `7f5901639107abf2ca40142f76b8fecb44b4c755`;
- `rawlsing_next/v3_contact_witness_independence_source_authority_candidate_r1.py` blob `1d01a35347950688dbff5913d10614928e72a764`;
- `rawlsing_next/m1_temporal_v554_admission_dedup.py` blob `e8bd6376720a2de132b384e7771d71d8d39cf261`.

Their separation discipline is reused by requiring exact owner/type refs and owner-supplied authority/dependency currentness checks.  The new interface does not promote OBL060 candidate semantics to project-current authority.

## Scope containment

No D2/D3/D4/P6 semantics are created.  No OBL062 ingress is implemented or closed.  No concrete mechanism rule, coefficient, actor fact, source authority, or domain witness family is created.  No main/HQ state is mutated.
