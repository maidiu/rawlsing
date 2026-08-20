# PRE553 I02 — C11 repository / ingest runtime contract

Status: `AUTHORIZED_FROM_ACCEPTED_I01_HEAD`

Exact implementation base: `b949280901b48f2ac6d4c711cd31f39b54889767`

Mission: implement the concrete logical C11 carrier/repository/ingest boundary under `rawlsing_next/**`, importing and reusing the accepted I01 public objects/authority validation rather than re-declaring them.

## Required runtime surface

The implementation may create only the following executable family (exact filenames may be split only if necessary without changing ownership):

- `rawlsing_next/pre553_c11_repository.py`
- `rawlsing_next/pre553_c11_ingest.py`
- `rawlsing_next/pre553_c11_integrity.py`
- `rawlsing_next/tests/test_pre553_c11_repository_ingest.py`

No legacy runtime import is permitted.

## Binding law

1. P10/D13 M01-M18 are the carrier obligations. Every required information class must be represented by an exact owned field/ref or explicit typed state; missing keys are never semantic absence.
2. I01's fourteen public families remain the public ontology. P10 carrier-specific records (`RespondentIdentity`, `QuestionVariableBinding`, `EmpiricalPredicateReplayBinding`, `ComparatorReplayBinding`, `DiscoveryBranchReplayBinding`, `StructuralAdmissionReplayBinding`, `ReplayManifest`) may exist only as internal C11 carrier/replay records.
3. Source-universe scope is mandatory and distinct by default. No semantic equivalence, respondent linkage, overlap treatment, pooling, composition, or backfill may be inferred.
4. Minimum response grain is one respondent event/component occurrence wherever authoritative topology permits multiplicity. Value equality may never collapse distinct occurrences.
5. Semantic order/rank/multiplicity is explicit. Container, file, row, serialization, or insertion order is never semantic order.
6. Routing/applicability/risk-set incidence is respondent-set identity, not denominator equality.
7. Empirical coordinates remain respondent-bound condition vocabulary, never generated nine-stratum positions or actor facts.
8. Weight/design/estimand authority is explicit. Missing/invalid/unauthorized weight is never silently replaced with 1.0.
9. Authority references are exact immutable ID/version/hash. No latest/default/fuzzy/nearest fallback.
10. A source package is C11-authoritative only after package-atomic validation closes all applicable M01-M18 obligations and seals exact replay/integrity identity. Partial physical presence grants no C11 authority.
11. The repository must preserve exact source/native values, canonical values only when authorized, typed special/absence states, topology, routing, coordinates, weights, authority snapshots, provenance, negative limits, and replay closure.
12. Deterministic ingest of semantically identical material must produce identical C11 semantic identities independent of insertion/storage order.
13. This tranche selects no production DB engine, file format, compression, indexing strategy, cache authority, source retirement, or deployment strategy. A deterministic in-memory/file-neutral logical repository is sufficient if it fully implements the semantic carrier contract.
14. Current Postgres/facet/shared-V550/V550J/V551/V552 surfaces are evidence and future source-adapter inputs only; they are never imported as runtime semantic owners.
15. I02 does not execute empirical queries, run discovery, decide StructuralEmpiricalAdmission, change V553+, or implement actor/V3/V2 behavior.

## Required hostile tests

At minimum cover: duplicate-looking occurrence preservation; multiselect/repeated/ranked topology; storage-order invariance; respondent namespace isolation; same-label source separation; routing-member-set distinction despite equal denominator; typed missing/DK/refusal/IAP/not-asked/invalid preservation; observed zero distinct from absence; missing-weight no-1.0; exact authority hash mismatch failure; partial-package nonauthority; M01-M18 closure audit; unauthorized canonical mapping failure; cross-universe relation noninference; deterministic replay manifest/hash; source-package tamper/hash mismatch; internal carrier record nonpromotion into public ontology.

## Return law

Return exact base/head, changed paths and blobs, test execution status, authority relied upon, claims made/refused, M01-M18 coverage matrix, and whether any accepted I01 or downstream interface changed.

Success token: `PRE553_I02_C11_REPOSITORY_INGEST_COMPLETE__READY_FOR_HQ_ACCEPTANCE`

Failure token: `BLOCKED_I02_C11_CONTRACT_CONFLICT`
