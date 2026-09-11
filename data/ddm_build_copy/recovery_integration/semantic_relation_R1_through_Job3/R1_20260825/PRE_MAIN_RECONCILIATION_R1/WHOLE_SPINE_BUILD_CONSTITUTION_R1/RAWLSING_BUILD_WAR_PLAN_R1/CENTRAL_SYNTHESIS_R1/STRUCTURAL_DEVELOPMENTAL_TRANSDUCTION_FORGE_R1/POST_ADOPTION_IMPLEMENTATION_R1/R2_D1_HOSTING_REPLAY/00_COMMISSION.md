# COMMISSION — SDTF R4 R2 D1 HOSTING / DEPENDENCY / INVALIDATION / REPLAY

BRANCH: `agent/rabochii-hq-sdtf-r4-r2-d1-hosting-replay-r1`

LAUNCH BASE: `315ec8ba942cbf356bf1ef57471441299ae1a875`

AUTHORIZED GRAIN:
`SDTF_R4_D1_HOSTING_DIRECT_DERIVATION_REVERSE_DEPENDENCY_INVALIDATION_REPLAY_R1_ONLY`

MISSION:
Implement the smallest physical hosting and dependency/replay substrate required by adopted D1' without inventing a replacement database or public ontology.

REUSE, DO NOT REPLACE:
- `rawlsing_next/m4_v557_v558_publication_repository.py` blob `8ec5c8e1c1a3cb7e998bb6cf0972ac87f396e360`
- `rawlsing_next/pre553_replay_audit.py` blob `86e0b9c518633735f2527b89fb72fca1a40dc2cc`
- `rawlsing_next/pre553_c11_repository.py` blob `67c6eb6494522cd11aab1b93d0e73f9cef6036f3`
- `rawlsing_next/m1_temporal_v554_admission_dedup.py` blob `e8bd6376720a2de132b384e7771d71d8d39cf261`

REQUIRED:
- host semantic obligations equivalent to `MECHANISM_RULE_RECORD`, `RULE_APPLICATION_RECORD`, `OBJECTIVE_POSITIONED_CONSEQUENCE_RECORD`, `EVIDENCE_WITNESS_RECORD` using existing exact-ref/CAS machinery where lawful;
- direct determinant -> exact rule application -> derived consequence edges;
- reverse dependency discoverability;
- affected-application-only reevaluation;
- invalidate/close unsupported outputs without opposite-fact synthesis;
- dependent-only redrive, preserving unrelated and historical facts;
- no same world/state/version/valid-time self-ancestry;
- deterministic replay receipt/parity.

PROHIBITED:
- no new database if existing V558/CAS repository can carry the graph;
- no concrete mechanism rules or actor facts;
- no world writer;
- no OBL062 closure;
- no global actor reset;
- no main/HQ mutation.

PASS:
`SDTF_R4_R2_D1_HOSTING_DEPENDENCY_INVALIDATION_REPLAY_IMPLEMENTED__READY_FOR_INTEGRATION_QUALIFICATION`

BLOCKER:
`SDTF_R4_R2_D1_HOSTING_DEPENDENCY_INVALIDATION_REPLAY__EXACT_IMPLEMENTATION_OR_AUTHORITY_BLOCKER_PROVED`

Commit exact implementation/test identities and governed return.