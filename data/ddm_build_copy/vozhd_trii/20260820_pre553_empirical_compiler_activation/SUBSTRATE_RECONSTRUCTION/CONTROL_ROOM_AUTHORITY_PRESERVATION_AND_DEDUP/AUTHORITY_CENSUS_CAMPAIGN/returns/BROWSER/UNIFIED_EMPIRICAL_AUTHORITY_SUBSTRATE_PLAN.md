# Unified Empirical Authority Substrate — End-State Plan

Status: `PLANNED_END_STATE__H004_IDENTITY_COLLISION_RISK_CONFIRMED__H005_SPLIT_INTO_LOCAL_DELTA_PLUS_BROWSER_COURT__IMPLEMENTATION_DEFERRED`

Recorded: 2026-08-23
Updated after HARVEST-004 adjudication and H005 Browser/local split.

## Objective

Rawlsing should ultimately have one governed empirical-authority universe covering the complete usable question/variable universe across every active survey family and wave. This should be one coherent authority system, not one giant mutable flat table.

## Architectural target

Use one stable question-occurrence identity spine (`question_uid`) and normalized relations at the correct grain for response semantics, semantic role, drivers, facets, structural domains, relation axes, targets, directionality, routing/applicability, position role, family/battery membership, equivalence, source evidence, review state, provenance and supersession.

Reusable ontology objects (drivers, facets, domains, axes, targets, concepts, families, response contracts, aliases/deprecations) should have stable identities, definitions, boundary laws, provenance and lifecycle status.

Negative/non-executable states such as `NOT_APPLICABLE`, `EXCLUDED`, `CONTEXT_ONLY`, `ADMINISTRATIVE`, `REVIEW_REQUIRED`, `SOURCE_CONFLICT`, `UNRESOLVED` and `BLOCKED` are first-class authority rather than unexplained blanks.

## Preferred physical release

Planning target:

1. versioned typed Parquet relations with schemas, manifests, hashes and validation receipts;
2. a deterministic read-only DuckDB compilation for querying;
3. a derived `question_authority_master` view exposing the intuitive all-in-one question surface.

The monster master view is for inspection and consumption. The normalized authority relations remain canonical so legitimate one-to-many facts cannot be collapsed by row order.

## H004 architectural proof

HARVEST-004 provides a concrete failure case that the replacement architecture must make impossible.

The historical GSS/LiTS structural updater decided question existence using `item_id`, while existing semantic rows were overwhelmingly blank in that newer identity field. It therefore appended 10,455 second representations whose `(source,wave,var_name)` identities already existed. A separate downstream consumer keyed by `(source,wave,var_name)` and used ordinary dict last-row behavior, silently turning physical row order into effective semantic precedence.

This proves that semantic authority and structural assertions must not be forced into one flat row model whose uniqueness depends on whichever identifier a producer happens to use.

The future substrate must distinguish at least:

- question occurrence identity;
- semantic assertions about that question;
- driver/facet assertions;
- structural block/domain/axis/target assertions;
- assertion provenance/status/review state;
- explicit supersession edges where one assertion really replaces another.

One question may lawfully have multiple assertions at these different grains without becoming a duplicate question occurrence.

## H005 operational split

The original H005 order mixed local filesystem discovery with the global relational identity/coverage computation.

That is now split into:

- `HARVEST-005L`: local machine searches only for H005-responsive exact content that Browser does not already possess;
- `HARVEST-005B`: Browser HQ performs the candidate-universe, cross-carrier joins, collision census, coverage counts and identity-law implications.

Normative Browser availability is recorded in:

`H005_BROWSER_AVAILABLE_EVIDENCE_INVENTORY.csv`

Browser already has exact H001-H004 packet bytes plus governed GitHub authority and Library discovery indexes. Local harvesting is therefore a content-addressed delta, not a redundant rebuild of the H005 computation.

## Required invariants

The eventual substrate should fail closed on:

- duplicate question identities where uniqueness is declared;
- cross-identifier disagreement (`item_id` vs source/wave/variable vs source-native identity) that has not been reconciled;
- unknown ontology IDs;
- implicit row-order precedence;
- recency/path precedence;
- unproved supersession;
- heuristic assignments promoted to accepted authority;
- source/wave identity collisions;
- variable-code reuse treated as equivalence;
- unexplained accepted-to-blank transitions;
- executable authority with unresolved required dependencies.

Every authority assertion should carry its own identity, question binding, epistemic/provenance class, status and lifecycle/supersession state rather than inheriting authority from physical row position.

## Historical authority

Accepted historical authority, including V525b and later positively adjudicated manual/review artifacts, is epistemic capital. It should be carried forward where identity/applicability are proved, preserved where succession is unproved, and never mechanically re-authored merely because a later carrier lost it.

H004 specifically establishes that later structural assertions may be valuable while the flat carrier's apparent semantic replacement is invalid. The migration therefore needs **noncollapse**: preserve prior semantic authority and later structural authority as distinct assertions when both are live.

## Coverage target

The production target is the complete usable-question universe across the active 35-wave scope, with every source variable/question sufficiently inventoried to distinguish substantive production material, routing/universe controls, respondent-position material, administrative/context material, batteries/families, exclusions and unresolved/source-conflict material.

## Preconditions and current state

Before implementation of the replacement authority store:

- [x] H004 resolves the main `d62...` duplicate-producer/precedence mystery: identity/cardinality collision proved; row-order semantic supersession rejected.
- [x] Browser H005 evidence availability inventory is explicit and content-addressed.
- [ ] H005L closes the local-only question-identity carrier delta.
- [ ] H005B establishes the mechanical current-35 question-occurrence/cross-carrier coverage baseline.
- [ ] HQ adopts the governed question-occurrence identity law and cardinality contract.
- [ ] the authority census maps enough historical/manual authority to distinguish live capital from true gaps.
- [ ] the current-35 candidate and production-usable universe boundaries are governed.
- [ ] full-universe semantic/driver/structural quality is adjudicated under the accepted ontology and source authority.
- [ ] true gaps are positively proved before new manual authority is created.
- [ ] migration/replay and validation contracts for the new physical release are accepted.

The unrecovered transient pre-Register-A full driver master is historical provenance residue, not a prerequisite for designing the new identity system; Register A preserves the effective pre-shadow projection and exact existing authority bytes remain protected.

## Trii / Chetiri integration law

The unified substrate is not an isolated data-cleanup artifact.

Trii source certification determines and protects exact source identities and source-native evidence needed by the question-occurrence spine.

Chetiri compiler/persistence candidate architectures must consume the live authority universe recovered here. A physical architecture does not satisfy project requirements if it stores or serves empirical data while silently discarding semantic/structural/manual authority, negative states, provenance or governed identity.

The Control Room therefore remains the reconciliation layer between:

`TRII SOURCE TRUTH`
+
`RECOVERED EPISTEMIC CAPITAL`
+
`CHETIRI COMPILER/PERSISTENCE REQUIREMENTS`

## Terminal shape

`ONE_GOVERNED_UNIVERSE`
+
`ONE_CANONICAL_IDENTITY_SYSTEM`
+
`NORMALIZED_RELATIONS_AT_CORRECT_GRAIN`
+
`VERSIONED_PARQUET_RELEASE`
+
`DETERMINISTIC_DUCKDB_QUERY_BUNDLE`
+
`ONE_MONSTER_MASTER_VIEW`
+
`EXPLICIT_PROVENANCE_AND_NEGATIVE_STATES`
+
`EXPLICIT_SUPERSESSION_EDGES`
+
`NO_IMPLICIT_PRECEDENCE`

This is an end-state architecture plan, not present implementation authority.
