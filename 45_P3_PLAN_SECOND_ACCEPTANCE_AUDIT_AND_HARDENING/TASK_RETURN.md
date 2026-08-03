# Rawlsing P3 Plan Second Acceptance Audit and Hardening Report

## Verdict

The v22 plan corrected major defects, but a second independent implementation audit found additional blockers that would have forced P3A redesign. The central P3 ontology remains sound. Plan v3 hardens coverage, substantive eligibility, schema typing, persistence, identity, release, and downstream contracts before any candidate execution.

## Corrected findings

1. **Lineage coverage was implicit.** Only 399 of 13,526 lineages touch proposition authority; 2,897 are constraint-only and 10,230 have no current direct pair authority. V3 governs all lineages through a participation ledger without treating absence as uniqueness.
2. **One proposition edge is administrative metadata.** The Afrobarometer/Asian Barometer interviewer item about respondent difficulty is valid proposition identity but not a substantive J-family edge. V3 separates proposition authority from J-family eligibility.
3. **Overlap provenance was not row-complete.** V3 delivers 19,582 source-authority rows: one governing row for every effective pair plus all 407 superseded exact overlaps.
4. **Candidate risk was forced into one label.** V3 adds multi-valued diagnostic flags and prevents provisional risk labels from impersonating terminal adjudication.
5. **Nested JSON payloads remained untyped.** Split points, hierarchy, collisions, unresolved boundaries, variants, structural context, canonical propositions, rankings, and status events now have schemas.
6. **Decision schemas lacked status-specific constraints.** Accepted, rejected, split, hierarchical, and blocked outcomes now fail closed under different required fields.
7. **Release JSON contradicted append-only SQL.** Release identity and status-event schemas now match separate persistence tables.
8. **Vocabulary binding contained a nonexistent `scope` column and omitted finite fields.** V3 binds actual columns, including `scope_type`, status events, hyperedges, pair axes, diagnostic flags, and provenance roles.
9. **Candidate membership allowed multiple simultaneous roles.** V3 permits one role per member per candidate revision.
10. **Candidate ranking was catalogued but absent from the DDL.** A typed ranking table and schema now exist.
11. **Foreign keys proved existence but not object type.** A polymorphic object-reference type contract now governs lineage, implementation, candidate, family, and ownership references.
12. **Pre-promotion validation incorrectly required a promoted pointer.** V3 separates pre- and post-promotion gates.
13. **Canonical hashing lacked an exact serialization contract.** V3 fixes canonical JSON and idempotency-key rules before ID allocation.
14. **Exclusion doctrine could force fabricated named exclusions.** Rule-based exclusions are always required; named exclusions are required whenever actual rejected near-neighbors exist.
15. **The family graph did not provide a terminal treatment for nonincident lineages.** V3 adds a no-loss lineage-disposition contract. P3 may preserve a substantive source-local singleton or a constraint-only, administrative, derived, unresolved, or segmented lineage without manufacturing cross-source equivalence. Global P3 closure requires all 13,526 lineages and all 18,276 implementations to remain accounted for.

## Upstream reconciliation

- effective direct pair authorities: 19,175;
- source-authority provenance rows: 19,582;
- proposition relations: 658;
- provisional substantive candidate edges: 657;
- administrative proposition diagnostics: 1;
- proposition-incident lineages: 399;
- constraint-only lineages: 2,897;
- no-current-direct-pair lineages: 10,230.

No P3 candidate or canonical family authority was authored in this audit.
