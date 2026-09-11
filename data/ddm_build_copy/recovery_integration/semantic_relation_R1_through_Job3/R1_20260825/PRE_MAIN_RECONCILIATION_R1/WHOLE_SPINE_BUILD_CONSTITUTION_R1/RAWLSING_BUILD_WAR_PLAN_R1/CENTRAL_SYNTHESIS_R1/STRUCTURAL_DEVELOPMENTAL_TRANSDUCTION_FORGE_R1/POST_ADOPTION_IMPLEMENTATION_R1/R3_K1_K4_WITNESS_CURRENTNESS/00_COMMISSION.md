# COMMISSION — SDTF R4 R3 K1-K4 PROOF / WITNESS-CURRENTNESS INTERFACE

BRANCH: `agent/rabochii-hq-sdtf-r4-r3-k1-k4-witness-currentness-r1`

LAUNCH BASE: `315ec8ba942cbf356bf1ef57471441299ae1a875`

AUTHORIZED GRAIN:
`SDTF_R4_K1_K4_PROOF_AND_TYPE_SPECIFIC_WITNESS_CURRENTNESS_INTERFACE_R1_ONLY`

MISSION:
Implement the adopted proof/currentness interface without minting actor facts or a universal witness ontology.

REUSE, DO NOT REPLACE:
- OBL060 witness/source-separation pattern blob `7f5901639107abf2ca40142f76b8fecb44b4c755`
- OBL060 R1 schema blob `1d01a35347950688dbff5913d10614928e72a764`
- `rawlsing_next/m1_temporal_v554_admission_dedup.py` blob `e8bd6376720a2de132b384e7771d71d8d39cf261`

REQUIRED:
- orthogonal K1/K2/K3/K4 assertion kind, polarity, currentness, modality, proof-adjudication;
- type-specific witness/state adapter contract, not one universal witness schema;
- exact K4 Path A and Path B from adopted companion;
- Path B requires owner-declared continuing-state semantics, supportable validity interval overlapping query/asserted interval, complete termination/supersession/invalidation coverage through query time, and no defeating closing fact;
- `UNKNOWN_NOT_PROVEN` is a no-fact adjudication output;
- explicit negative-proof contract; failed/stale/expired positive proof never becomes negative;
- bare `ACTIVE` remains umbrella current/operative descriptor, not K4-exclusive.

PROHIBITED:
- no actor facts;
- no new source authority;
- no prebuilding all domain witness families;
- no OBL062 closure;
- no main/HQ mutation.

PASS:
`SDTF_R4_R3_K1_K4_WITNESS_CURRENTNESS_INTERFACE_IMPLEMENTED__READY_FOR_INTEGRATION_QUALIFICATION`

BLOCKER:
`SDTF_R4_R3_K1_K4_WITNESS_CURRENTNESS_INTERFACE__EXACT_IMPLEMENTATION_OR_AUTHORITY_BLOCKER_PROVED`

Commit exact implementation/test identities and governed return.