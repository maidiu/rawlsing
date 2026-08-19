# SV3A — Source Component Preservation Law

## Binding recommendation

The thin V3 wrapper MUST preserve the PSEPF's source-indexed structure as an exact manifest. It may not reduce a mixed-source field to one wrapper-level state, one pooled distribution, one winning source, one aggregate confidence, or one availability flag.

This is necessary because source components may lawfully disagree in kind, not merely degree: one can be positive while another is unsupported, valid-empty, noncomparable, unknown or conflicting. Erasing that vector changes the empirical object.

## Required component record

For each component required by the accepted PSEPF contract, `source_components[]` MUST carry:

- exact `component_id`;
- exact `component_ref` and `component_content_hash`;
- exact `source_universe_ref` and hash or exact equivalent source identity;
- boundary `component_state`;
- exact `producer_state_subtype` when the producer is more specific than the boundary state;
- exact refs/hashes for the authority that supports that state;
- exact negative/noncomparability/conflict refs when applicable;
- exact component effective-time basis refs where material;
- exact externally-owned refresh/requery metadata refs where supplied.

The record MAY carry administrative storage locators only when they are exact immutable locators. Such locators are nonsemantic and never replace producer identity.

## Completeness invariant

For one exact PSEPF root:

`wrapper component identities == exact required PSEPF component identities`.

The wrapper MUST fail closed if a required component is omitted, duplicated incompatibly, replaced by another source, hash-mismatched, or introduced without a PSEPF-declared component identity.

A wrapper may not advertise itself as complete merely because all positive components are present while negative, unsupported, valid-empty, noncomparable or unknown components are absent.

## State preservation

Boundary minimum states:

- `POSITIVE`
- `UNSUPPORTED`
- `VALID_EMPTY`
- `NONCOMPARABLE`
- `UNKNOWN`
- `CONFLICT`
- `INTEGRITY_FAILURE`

These are not permission classes and not actor-state classes.

Where upstream authority distinguishes finer states, exact distinctions MUST survive. In particular, if PSEPF/source authority distinguishes low support, observed zero, zero support, structural zero, sample absence, missing authority, or a named negative/noncomparability reason, the wrapper must retain that exact subtype and supporting refs rather than flattening it into generic `UNSUPPORTED` or `UNKNOWN`.

## No composition by convenience

The wrapper creates **no** authority for:

- source semantic equivalence;
- respondent identity linkage;
- sample pooling;
- risk-set pooling;
- estimand equivalence;
- measure/weight compatibility;
- averaging;
- voting/majority;
- confidence-weighted combination;
- latest-source preference;
- source priority by file or branch order;
- winner-take-all selection;
- filling one source from another;
- treating provenance reachability as composability.

If an accepted upstream operation-specific authority has already created a composed PSEPF component, the wrapper may reference that exact producer-owned component. It may not recreate the composition or infer that independently listed source components are jointly composable.

## No geometry duplication

The component manifest is not a place to smuggle field geometry into V3 intake. Forbidden per-component convenience fields include:

- copied modal cells;
- copied mass/probability tables;
- top-k modes;
- dominant mode;
- marginal distributions;
- summarized J-way coordinates;
- normalized probability vectors;
- source-specific actor labels or predicted responses.

V3 must dereference the exact PSEPF/component content when geometry is needed under later read-permission authority.

## Mixed-state examples

The following must remain representable without contradiction:

1. Source A `POSITIVE`; Source B `NONCOMPARABLE`.
2. Source A `POSITIVE`; Source B `VALID_EMPTY`; Source C `UNKNOWN`.
3. Source A `UNSUPPORTED` with producer subtype `ZERO_SUPPORT`; Source B `POSITIVE` with a minority mode.
4. Source A and B both `POSITIVE` but carry an exact producer-declared `CONFLICT`/noncomposition relation.
5. All sources `VALID_EMPTY`, where that valid-empty state is producer-governed.
6. One source component fails hash verification while others are positive. The affected component is `INTEGRITY_FAILURE`; if it is required for the exact PSEPF root, wrapper envelope integrity fails closed rather than silently dropping it.

No example above may be reduced to one global `supported=true/false` without loss.

## Canonical serialization

Component records may be sorted by an exact canonical component key for deterministic wrapper bytes only when the PSEPF contract declares component list order nonsemantic. Any producer-declared semantic order must be preserved exactly.

Serialization order never creates source precedence.

## Actor firewall

A source component's state, mass, mode, cohort/comparator metadata or relative prevalence is evidence about the possibility field. It is not evidence that the generated actor currently holds, knows, remembers, believes, identifies with, says or does the corresponding thing.

Therefore the wrapper MUST NOT expose source-component data through actor-semantic field names or APIs. ActorComparatorReceipt references remain provenance-only even when technically dereferenceable for audit.
