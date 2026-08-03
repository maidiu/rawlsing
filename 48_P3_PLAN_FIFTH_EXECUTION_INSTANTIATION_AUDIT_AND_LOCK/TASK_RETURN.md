# Rawlsing P3 Plan Fifth Execution-Instantiation Audit

**Date:** 2026-08-01  
**Input:** cumulative handoff v25 / Plan v5  
**Corrected release:** cumulative handoff v26 / Plan v6  

## Verdict

The fifth pass closed 18 bounded implementation defects: 15 defects in the v25 input contract and 3 additional release blockers caught while attempting to instantiate and verify the v26 correction. The P3 ontology was not reopened. No new database, service, visualization layer, or speculative subsystem was introduced.

## Real topology instantiated

- 658 proposition authorities; 657 provisionally substantive.
- 445 strict proposition-plus-response edges produce 94 strict components over 304 lineages.
- 212 substantive proposition-only edges divide into 1 internal support, 85 orphan-to-strict attachments, 70 strict-component bridges, and 56 outside-strict edges forming 25 proposition-only seed components.
- The strict-component/seed meta-graph produces 22 deterministic attachment-review groups.
- The resulting 141-row inventory is diagnostic and must be recomputed after signatures, segmentation, endpoint resolution, and explicit pair projection.

## Corrected defects

### 1. SEGMENT_PAIR_PROJECTION_MISSING

**Severity:** FATAL  
**Detection stage:** V25_INPUT  
Pair endpoint resolution could not create a direct segment-bound subject relation; component validators still expected original lineage IDs.  
**Correction:** Added explicit PAIR_PROJECTION authority and rewired components and internal pairs.

### 2. ATTACHMENT_REVIEW_GROUPING_UNDEFINED

**Severity:** FATAL  
**Detection stage:** V25_INPUT  
Proposition-only bridges and orphan attachments had no deterministic candidate grouping algorithm.  
**Correction:** Added deterministic meta-graph grouping and a 22-group real-topology preflight.

### 3. CANDIDATE_ORIGIN_UNDERCONSTRAINED

**Severity:** FATAL  
**Detection stage:** V25_INPUT  
Candidate members could not be reconstructed exactly from components and attachments.  
**Correction:** Added immutable origin keys, attachment projections, membership basis, and origin validation.

### 4. LINEAGE_DISPOSITION_SINGLE_CANDIDATE

**Severity:** HIGH  
**Detection stage:** V25_INPUT  
One candidate_family_id could not represent overlapping base and attachment-review participation.  
**Correction:** Replaced the one-candidate assumption with CANDIDATE_PARTICIPANT and many-to-many membership authority.

### 5. PACKET_CROSS_FIELD_VALIDATION_ABSENT

**Severity:** FATAL  
**Detection stage:** V25_INPUT  
Schema-valid packets could contain mismatched members, pair counts, summaries, rankings, hashes, or decisions.  
**Correction:** Delivered an executable semantic validator and mutation tests.

### 6. ADJUDICATION_MEMBER_CLOSURE_UNENFORCED

**Severity:** FATAL  
**Detection stage:** V25_INPUT  
Completed decisions did not necessarily disposition every proposed member exactly once.  
**Correction:** Added exact member-partition validation and canonical membership closure.

### 7. SPLIT_SUCCESSORS_UNREPRESENTED

**Severity:** FATAL  
**Detection stage:** V25_INPUT  
Split points did not create executable successor candidate groups.  
**Correction:** Added stable split-result candidates and exact disjoint member partitions.

### 8. CANDIDATE_CANONICAL_OWNERSHIP_CONFLATED

**Severity:** HIGH  
**Detection stage:** V25_INPUT  
Candidate variants and exclusions could not safely become canonical authority under immutable ownership.  
**Correction:** Added explicit variant and exclusion promotion mappings into canonical-owned authority.

### 9. SIGNATURE_WORKSET_OVERBUILT

**Severity:** MEDIUM  
**Detection stage:** V25_INPUT  
Full signatures were required for 3,296 pair-incident lineages although only 399 participate in proposition authority.  
**Correction:** Bounded initial full signatures to 399, preserved constraint evidence for 2,897, and deferred 10,230 without declaring them unique or irrelevant.

### 10. PLACEHOLDER_AUTHORITY_HASHES

**Severity:** HIGH  
**Detection stage:** V25_INPUT  
Fixtures used all-zero authority-looking hashes.  
**Correction:** Replaced them with nonzero deterministic NONAUTHORITY_TEST_FIXTURE hashes and a semantic guard.

### 11. DECISION_EVENT_TIMESTAMPS_INCOMPLETE

**Severity:** HIGH  
**Detection stage:** V25_INPUT  
Completed decisions and status events lacked complete temporal event fields across JSON and SQL.  
**Correction:** Added created_at and occurred_at fields and validation.

### 12. CANDIDATE_PREFLIGHT_RETURN_MISSING

**Severity:** MEDIUM  
**Detection stage:** V25_INPUT  
The real 658-edge topology had not been converted into a deterministic candidate-origin preflight.  
**Correction:** Delivered the 94 strict + 25 proposition-only seed + 22 attachment-review = 141 pre-signature diagnostic inventory.

### 13. CONTENT_ID_SCHEMA_CONTRADICTION

**Severity:** HIGH  
**Detection stage:** V25_INPUT  
Two content-addressed object schemas contradicted the governed identity registry.  
**Correction:** Aligned schema patterns and identity allocation rules to one canonical serialization and ID strategy.

### 14. REVISION_ORDINAL_PERSISTENCE_MISSING

**Severity:** HIGH  
**Detection stage:** V25_INPUT  
Variant and adjudication revisions lacked normalized persistent ordinals.  
**Correction:** Added explicit revision ordinals, uniqueness, and supersession constraints.

### 15. STATUS_DECISION_CHILD_PERSISTENCE_INCOMPLETE

**Severity:** FATAL  
**Detection stage:** V25_INPUT  
Split, hierarchical, and unresolved decisions had JSON forms but incomplete normalized SQL persistence.  
**Correction:** Added status-specific child tables and completeness validators.

### 16. DIRECTIONAL_PAIR_ORDERING_UNSAFE

**Severity:** FATAL  
**Detection stage:** V26_CORRECTION_QA  
A draft projection constraint lexically reordered endpoints and could reverse directional authority.  
**Correction:** Removed lexical endpoint ordering; projection preserves governed left/right roles and orientation.

### 17. PAIR_PROJECTION_PACKET_PROOF_MISSING

**Severity:** FATAL  
**Detection stage:** V26_CORRECTION_QA  
A packet could cite a direct pair without carrying the projection record that proves selected subjects and pair provenance.  
**Correction:** Required explicit projection records in packets and cross-validated projection ID, endpoints, and underlying pair fact.

### 18. EVIDENCE_HASH_RECOMPUTATION_MISSING

**Severity:** FATAL  
**Detection stage:** V26_CORRECTION_QA  
Copied matching hash strings could pass even when the delivered evidence surface did not reproduce the hash.  
**Correction:** Defined the evidence-bundle serialization surface and recompute the SHA-256 from signatures, response references, projections, pair matrix, collisions, obligations, and evidence links.

## Executable acceptance surface

- Fifty connected local JSON Schemas resolve offline.
- Candidate packets carry explicit pair projections and a complete internal pair matrix.
- The semantic validator recomputes the evidence bundle hash and validates packet/decision closure.
- Twenty-nine implementation-shaped tests cover strict graph sequencing, attachments, segmentation, directional relations, splits, promotions, identities, and mutation failures.
- PostgreSQL-compatible logical DDL preserves directional endpoints, normalized decision children, immutable identities, and canonical promotion lineage.

## Authority boundary

No P3 candidate inventory has been accepted as authority. No canonical family, response harmonization, database write, live repository change, respondent join, or runtime installation occurred.

## Exact continuation

`P3A_CONTRACT_AND_PILOT_V6_IMPLEMENTATION`
