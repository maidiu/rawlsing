# Rawlsing P3 Plan Sixth Executable-Closure Audit

**Date:** 2026-08-01  
**Input:** cumulative handoff v26 / Plan v6  
**Corrected release:** cumulative handoff v27 / Plan v7

## Verdict

The sixth pass found **18 bounded defects** in the v26 implementation contract. Four were immediately fatal to SQL execution: the transaction rolled back before the new functions, two validators referenced columns that do not exist, and one `ALTER TABLE` targeted a column deliberately removed in v25. The packet layer also could not accept a valid split or hierarchy-only decision, and its evidence hash did not actually bind the full delivered evidence.

The P3 ontology survived. This release does not add a database, service, graph platform, visualization system, or speculative downstream stage. It makes the already-governed distinctions executable across JSON, Python, SQL, and release validation.

## What the pass actually did

- Executed the inherited v26 verifier and test suite against a clean extraction.
- Read the 75-table DDL as one transaction rather than as a bag of reassuring strings.
- Cross-checked JSON-required fields against SQL persistence.
- Constructed valid completed decisions for split, hierarchy-only, and canonical acceptance.
- Mutated delivered semantic content while leaving nested `content_hash` strings unchanged.
- Tested Unicode normalization, line-ending normalization, set ordering, duplicate rejection, malformed date-times, release mismatch, origin reconstruction, and promotion closure.
- Added a static SQL contract checker that reads table columns, validates `ALTER TABLE` targets, enforces rollback finality, and confirms assertion-trigger wiring.

The inherited real topology is unchanged: 19,175 effective direct pair authorities, 658 proposition authorities, 657 provisionally substantive edges, 445 strict proposition-plus-response edges, 94 strict components over 304 lineages, 25 proposition-only seed components, 22 attachment-review groups, and 141 pre-signature diagnostic candidate records. None of those 141 records is canonical authority.

## Corrected defects

### 1. Ddl Transaction Rollback Premature

**Severity:** FATAL  
**Detection stage:** V26_EXECUTION  
The v26 DDL issued ROLLBACK before the v26 functions and triggers. Executing the file erased every base table before the new functions referenced them.

**Correction:** Moved the single rollback to the final statement and added a transaction-finality static gate.

### 2. Component Projection Column Stale

**Severity:** FATAL  
**Detection stage:** V26_EXECUTION  
Component closure joined p3_component_connectivity_edge through a nonexistent pair_fact_id rather than its projection_id.

**Correction:** Rewired component closure through p3_pair_projection to the governing pair fact and projected endpoints.

### 3. Internal Pair Projection Column Stale

**Severity:** FATAL  
**Detection stage:** V26_EXECUTION  
Internal-pair closure referenced nonexistent direct_pair_fact_id and therefore could not validate projection-backed direct relations.

**Correction:** Rewired closure through direct_pair_projection_id while preserving directional source roles and unordered candidate-pair storage.

### 4. Lineage Disposition Stale Foreign Key

**Severity:** FATAL  
**Detection stage:** V26_EXECUTION  
The DDL added a foreign key on p3_lineage_disposition.candidate_family_id even though the column had been removed to permit overlapping candidate participation.

**Correction:** Removed the impossible foreign key and retained candidate participation in the many-to-many candidate membership surface.

### 5. Validation Query Schema Drift

**Severity:** FATAL  
**Detection stage:** V26_EXECUTION  
Read-only validation queries used removed columns, old vocabulary codes, and the wrong canonical revision identifier.

**Correction:** Corrected all stale joins, fields, role codes, and proposed-member pair counts; added v7 closure queries.

### 6. Candidate Origin Key Not Persisted

**Severity:** HIGH  
**Detection stage:** V26_EXECUTION  
JSON required an immutable origin_key but PostgreSQL persistence omitted it.

**Correction:** Persisted a nonzero SHA-256 origin key with release-scoped uniqueness.

### 7. Candidate Event Time Not Persisted

**Severity:** HIGH  
**Detection stage:** V26_EXECUTION  
Candidate event JSON required occurred_at while SQL omitted it and could not enforce temporal order.

**Correction:** Persisted occurred_at and required strictly increasing event time and contiguous event ordinal.

### 8. Assertion Functions Not Wired

**Severity:** FATAL  
**Detection stage:** V26_EXECUTION  
Candidate-origin, adjudication-partition, split, and canonical-promotion assertions existed but no trigger or release query invoked them.

**Correction:** Added deferred constraint triggers that execute every closure assertion against the final transaction state.

### 9. Valid Split Decision Rejected

**Severity:** FATAL  
**Detection stage:** V26_PACKET_VALIDATION  
The generic member partition ignored split-result treatment, so a schema-valid complete split always failed semantic validation.

**Correction:** Made split-result membership a terminal disposition category and added a valid split fixture plus disjoint-cover tests.

### 10. Hierarchy Partition One Sided

**Severity:** FATAL  
**Detection stage:** V26_PACKET_VALIDATION  
Hierarchy-only validation counted only narrower endpoints; a valid broader/narrower pair failed, while accepted members could be smuggled into hierarchy-only status.

**Correction:** Defined hierarchy disposition as the union of governed broader and narrower candidate endpoints and prohibited incompatible status mixtures.

### 11. Terminal Disposition Overlap Unchecked

**Severity:** HIGH  
**Detection stage:** V26_PACKET_VALIDATION  
Members could occupy more than one terminal decision category under mixed child structures.

**Correction:** Enforced pairwise-disjoint terminal category sets whose union equals the candidate membership exactly.

### 12. Canonical Serializer Documentary Only

**Severity:** FATAL  
**Detection stage:** V26_IDENTITY  
The serialization contract had stale V5 identities and no executable NFC, line-ending, set-order, duplicate, or numeric rules.

**Correction:** Delivered p3_canonical_json_v7.py, executable vectors, NFC/LF normalization, set sorting, duplicate rejection, and float rejection.

### 13. Evidence Hash Not Reconstructive

**Severity:** FATAL  
**Detection stage:** V26_PACKET_VALIDATION  
The evidence hash covered selected IDs and nested hash strings rather than the full delivered evidence. Mutated semantic content could survive when its nested content_hash was left unchanged.

**Correction:** Hash the full nonrecursive delivered evidence surface, including complete signatures, response references, components, projections, pair matrix, variants, exclusions, and context.

### 14. Authority Release Coherence Unchecked

**Severity:** HIGH  
**Detection stage:** V26_PACKET_VALIDATION  
Nested packet objects could cite a different authority release from the candidate and decision.

**Correction:** Recursively require every delivered authority_release_id to equal the packet release before adjudication.

### 15. Json Formats Not Enforced

**Severity:** HIGH  
**Detection stage:** V26_PACKET_VALIDATION  
JSON Schema date-time declarations were validated without a FormatChecker, so malformed timestamps passed.

**Correction:** Use jsonschema FormatChecker for every schema validation and add a malformed-date mutation.

### 16. Origin Component Evidence Absent

**Severity:** FATAL  
**Detection stage:** V26_PACKET_VALIDATION  
Packets carried component IDs but not the component records needed to reconstruct candidate origin and membership.

**Correction:** Added origin_components to the packet and require exact reconstruction from component members plus attachment projections.

### 17. Promotion Closure Incomplete

**Severity:** FATAL  
**Detection stage:** V26_PACKET_VALIDATION  
Variant and exclusion promotions were not proven to map every and only delivered candidate object; rule-based exclusions could fabricate named members.

**Correction:** Require exact candidate-to-canonical promotion mappings, exact member partitions, owner coherence, and zero named members for rule-based exclusions.

### 18. Contract Surface Drift Undetected

**Severity:** HIGH  
**Detection stage:** V26_TESTING  
Static tests searched for reassuring strings but missed impossible SQL, stale schema names, stale vocabularies, and the V650/V651/V652 runtime-command typo.

**Correction:** Added a table/column-aware static SQL closure checker, corrected internal-pair schema and vocabularies, restored V550J/V551J/V552J names, and mutation-tested the checker.

## Executable acceptance surface

- **50 connected local JSON Schemas** resolve offline and are validated with format checking.
- **75 PostgreSQL-compatible logical tables** remain in one rollback-safe transaction; the sole `ROLLBACK` is the final statement.
- Candidate packets now carry the actual origin components required to reconstruct candidate membership.
- The evidence-bundle SHA-256 binds the full delivered nonrecursive evidence surface, not merely IDs and copied hash strings.
- Valid canonical, split, and hierarchy-only decisions all pass; cross-category overlap, incomplete partitions, ghost promotions, fabricated named exclusions, release mismatch, and stale origin evidence fail closed.
- **30 implementation and mutation tests pass.**
- The static SQL closure checker reports **PASS**, 75 tables, one final rollback, and zero known stale-column or dead-assertion findings.

## What remains unproved

No user-designated PostgreSQL target was supplied. The DDL was therefore parsed and cross-validated statically, not executed by a live PostgreSQL server. No claim of live migration or installation is made. The next trustworthy burden remains P3A execution against actual generated signatures, projections, candidates, packets, and decisions.

## Authority boundary

No P3 candidate inventory has been accepted as authority. No canonical J-family has been authored. No values were harmonized, respondents joined, database written, registry installed, live repository changed, or runtime bridge installed.

## Exact continuation

`P3A_CONTRACT_AND_PILOT_V7_IMPLEMENTATION`
