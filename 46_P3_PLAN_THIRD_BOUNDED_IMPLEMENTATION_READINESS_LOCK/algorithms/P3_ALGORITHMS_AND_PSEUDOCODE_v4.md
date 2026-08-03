# Rawlsing P3 Algorithms and Pseudocode v4

## Governing principle
P3 may generate candidates. It may not manufacture direct pair authority, canonical family authority, measurement compatibility, causal authority, strata direction, respondent joins, or runtime substitutability.

## A. Freeze the effective upstream authority surface

Inputs are both closed P2 registries. Build a canonical unordered lineage-pair key. When a pair exists in semantic-priority closure, that later authority governs. Exact-foundation authority contributes only pairs absent from semantic-priority closure. Preserve overlapping exact rows as superseded provenance.

Expected frozen counts:
- semantic-priority rows: 18,831;
- exact-foundation rows: 751;
- overlaps: 407;
- exact-only rows: 344;
- effective direct pair authorities: 19,175;
- proposition relation pairs: 658; current substantive-eligibility preflight: 657 plus one administrative diagnostic = 641 semantic-priority + 17 exact-only.

```text
for pair in semantic_priority_registry:
    effective[pair_key] = semantic_priority(pair)
    provenance[pair_key].append(any_exact_overlap_as_superseded)
for pair in exact_foundation_registry:
    if pair_key not in effective:
        effective[pair_key] = exact_only(pair)
assert len(effective) == 19175
```

## A2. Freeze source-authority provenance and lineage participation
Emit one source-authority row for every semantic and exact-foundation ruling, marking exactly one governing row per effective pair and every exact overlap as superseded provenance. Classify all 13,526 lineages as proposition-incident, constraint-only, or no-current-direct-pair-authority.

## B. Register upstream objects read-only
Preserve inherited implementation, lineage, structure, and response-contract IDs. Register their authority artifact, hash, source family, and licensing reference. Do not reallocate or mutate upstream IDs.

## C. Allocate P3 identities
Use the complete per-object identity registry in P3_IDENTITY_KEY_SPEC_v4.csv. It applies three strategies:
1. inherited upstream ID for imported P2 objects;
2. content-addressed ID for derived components and immutable normalized facts;
3. registry-allocated durable ID for candidates, canonical families, variants, exclusions, adjudications, hyperedges, and doctrine deltas.

Initial durable allocation sorts immutable idempotency keys. After the first release, allocation is append-only; insertion never renumbers existing IDs. Membership changes create revisions, not new stable family IDs.

## D. Normalize effective P2 authority
Apply `upstream/P3_P2_TO_P3_AUTHORITY_MAPPING.csv`. Preserve source ceiling and normalized P3 ceiling. Pair facts may cite multiple source authorities, but exactly one governing authority under the precedence contract. `creates_endpoint_authority` is always false: only the direct governing P2 ruling supplies the pair fact itself; graph paths never do.

## E. Recover proposition signatures
Evidence precedence:
1. direct source-native question;
2. parent prompt;
3. response dictionary;
4. adjudicated source structure;
5. lineage history;
6. direct P2 evidence;
7. corrected semantic overlay for diagnostic location only.

Every required field receives a value, evidence state, confidence, and evidence IDs. `KNOWN` requires a nonblank value and at least one authoritative evidence ID.

## F. Detect lineage drift and create P3 segments
Compare implementation-level target, operator, modality, material timeframe, condition, population/geographic scope, polarity, and direct/derived status. Material drift creates exact implementation segments while preserving the P2 lineage unchanged.

## G. Construct connectivity and constraint graphs
The proposition-authority graph contains governing `PROPOSITION_RESPONSE_IDENTITY` and `PROPOSITION_IDENTITY_ONLY` facts. A separate substantive-eligibility gate excludes administrative metadata from J-family candidate connectivity while preserving its pair authority. Constraint graph contains typed collisions, unresolved authority, hierarchy, response incompatibility, structure-only authority, heterogeneity, and redirects. Superseded exact overlap rows are provenance only and cannot create connectivity.

## H. Generate strict components
Use only proposition-response identity facts for strict components. Component IDs are content addressed from sorted members, sorted edge IDs, and build-rule version. For every component, materialize n(n-1)/2 internal pair rows.

## I. Attach proposition-only relations
Proposition-only facts create attachment or merge-or-sibling closure obligations. They never automatically merge strict components.

## J. Partition and classify candidates
Build proposition compatibility keys. `UNRECOVERED`, `HETEROGENEOUS`, and `CONFLICTING` remain blockers. Candidate classification is diagnostic and separate from lifecycle stage.

## K. Build closure obligations
Create obligations for unruled internal pairs, direct collisions, unresolved pairs, signature conflicts, incomplete signatures, heterogeneous lineages, proposition-only attachments, and value-portability boundaries.

## L. Construct variants and exclusions
Response topology, wording/translation, source response form, and explicitly governed historical intervals may form variants when proposition identity is preserved. Target, operator, modality, behavior-versus-willingness, direct-versus-derived, and materially different scope ordinarily require split or hierarchy. Every accepted family requires rule-based exclusions; named exclusions are required only when actual rejected near-neighbors exist.

## M. Construct permitted hyperedges
Battery, cross-source battery analogy, derived-index constitution, sibling-family construct, target hierarchy, and response-contract class only. `causal_authority=false` always.

## N. Rank and select pilot candidates
Lexicographic ranking orders work; no score compensates for a hard blocker. Select up to forty candidates across the risk strata in the pilot rules, including exact-only and precedence-overlap cases.

## O. Structured adjudication
Draft decisions validate against the draft schema. Completed decisions validate against the final schema, require a nonblank rationale and terminal decision status, and write immutable member/collision/hierarchy dispositions. P3 response portability remains `NOT_AUTHORIZED_BY_P3`.

## P. Canonical family creation and revision
An accepted decision allocates a stable `JFAM` identity and an immutable release-scoped revision. Membership, proposition, variants, exclusions, and evidence hashes live on the revision. Later ordinary changes append revisions; splits and merges create new family IDs plus genealogy records.

## Q. Dependencies and incremental rebuild
Every canonical and derived object declares inputs. A changed P2 ruling, vocabulary, schema, signature, or doctrine rule computes a dirty dependency closure and records the exact rebuild scope.

## R. New-wave attachment
Attach new implementations through source-local lineage review, signature comparison, drift detection, exclusion checks, variant/family decision, affected-only rebuild, and new authority release.

## S. Release, shadow install, and rollback
Release status is append-only through status events. Release snapshots identify every included object and content hash. P3 closure prepares migrations; installation occurs only in a user-designated live target, first in shadow mode, with transactional promotion or complete rollback.

## T. Determinism and no-authority-leak assertions
Input row order cannot alter outputs. Coordinate edges cannot connect components. Adding a hard negative cannot improve classification. Removing a positive edge cannot enlarge a component. No family membership grants value portability, strata direction, causal authority, or runtime substitutability.


## U. Canonical serialization and reference-type enforcement
Before hashing or ID allocation, canonicalize JSON and set-like arrays under P3_IDENTITY_KEY_SPEC_v4.csv. Validate every registry-backed polymorphic reference against P3_OBJECT_REFERENCE_TYPE_CONTRACT_v4.csv.


## V. Artifact lifecycle and enforcement preflight
Before P3A writes any artifact, resolve the artifact catalog delivery state, identity strategy, schema/DDL target, producing phase, and dependency set. Fail if a delivered path is absent, a future output is mistaken for delivered authority, an object type lacks an identity rule, a polymorphic reference lacks a type contract, or a hyperedge role lacks a cardinality/type rule.


## W. Exact canonical serialization and revision allocation
Use `P3_CANONICAL_SERIALIZATION_CONTRACT_v4.json` and its fixed vectors. Reject floats, duplicate normalized set members, unsupported Unicode, absent required identity keys, and prefix/full-hash collisions. Candidate and variant revisions store explicit ordinals; split points and unresolved boundaries are normalized decision children rather than packet-only prose.
