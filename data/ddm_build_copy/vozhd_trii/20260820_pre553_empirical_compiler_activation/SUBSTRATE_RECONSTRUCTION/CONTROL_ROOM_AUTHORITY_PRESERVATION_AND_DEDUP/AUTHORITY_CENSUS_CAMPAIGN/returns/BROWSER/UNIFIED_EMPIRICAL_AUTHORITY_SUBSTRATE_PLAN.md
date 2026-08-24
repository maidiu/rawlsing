# Unified Empirical Authority Substrate — End-State Plan

Status: `PLANNED_END_STATE__IMPLEMENTATION_DEFERRED_PENDING_AUTHORITY_RECOVERY`

Recorded: 2026-08-23

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

## Required invariants

The eventual substrate should fail closed on duplicate keys where uniqueness is declared, unknown ontology IDs, implicit row-order precedence, recency/path precedence, unproved supersession, heuristic assignments promoted to accepted authority, source/wave identity collisions, variable-code reuse treated as equivalence, unexplained accepted-to-blank transitions, and executable authority with unresolved required dependencies.

## Historical authority

Accepted historical authority, including V525b and later positively adjudicated manual/review artifacts, is epistemic capital. It should be carried forward where identity/applicability are proved, preserved where succession is unproved, and never mechanically re-authored merely because a later carrier lost it.

## Coverage target

The production target is the complete usable-question universe across the active 35-wave scope, with every source variable/question sufficiently inventoried to distinguish substantive production material, routing/universe controls, respondent-position material, administrative/context material, batteries/families, exclusions and unresolved/source-conflict material.

## Preconditions

Do not implement the replacement authority store until:

- HARVEST-004 resolves or explicitly bounds the `d62...` producer and duplicate-precedence lineage;
- the authority census maps the historical/manual authority that must survive;
- true gaps are separated from unlocated or unproved-supersession cases;
- HQ adopts an explicit schema, identity, provenance and cardinality contract;
- the current-35 usable-universe identity baseline is governed.

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
`NO_IMPLICIT_PRECEDENCE`

This is an end-state architecture plan, not present implementation authority.