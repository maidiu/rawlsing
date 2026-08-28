# MX02 MINIMUM COMMON CONTRACT DELTA

Status: `ONE_SMALL_COMMON_REF_ONLY_RECEIPT_REQUIRED`

This is a returned semantic-contract requirement only. MX02 does **not** install it and does not modify any production `rawlsing_next/**` contract.

## 1. First irreducible missing function

The existing PRE-V3 stack can preserve exact producer-owned component objects and references through publication/repository/reload, but there is no accepted common semantic owner for this exact statement:

> For one exact vector subject and one exact governed authority dimension, this is the complete governed component set; these are the producer-owned typed component authority states/values; therefore the projection disposition is heterogeneous, incomplete, governed-empty, denied/noncomparable, or complete-unanimous-nonempty and scalarizable.

The minimum delta is therefore a **ref-only vector closure/projection receipt**, provisionally:

`ComponentAuthorityVectorReceipt@1.0.0`

The name is provisional. The required semantic function is binding.

## 2. Object grain

Exactly one:

`VECTOR SUBJECT × AUTHORITY DIMENSION × GOVERNED COMPONENT SET × PROJECTION DECISION`

This receipt is not the packet itself and is not a component payload store.

Hard laws:

`PACKET != SCALAR`

`COMPONENT_AUTHORITY != PARENT_LABEL`

`PUBLICATION != REOWNERSHIP`

## 3. Minimum required fields

### Receipt identity

- receipt schema ID/version;
- stable receipt object ID/content hash;
- exact vector-subject ref;
- exact authority-dimension/field-contract ref;
- exact vector-rule/scalarization-authority ref;
- producer replay locator or immutable reference root.

### Governed component bindings

One binding for every governed component, preserving where applicable:

- `component_id`;
- exact `component_ref` including producer object/hash;
- authoritative producer family;
- component role;
- semantic ordinal or null;
- multiplicity index;
- authority-state token;
- exact authoritative-value binding or content digest;
- exact value/field authority ref;
- negative/denial/noncomparability refs.

The receipt must not copy a component payload and then claim ownership of the copied value. It binds the exact producer-owned value/state.

### Closure proof

- declared governed component count;
- bound component count;
- exact missing/ambiguous/unresolved component IDs;
- `complete_coverage`;
- exact coverage-proof hash/material;
- `all_governed_components_nonempty`;
- exact governed-empty IDs;
- exact denied/noncomparable IDs where applicable;
- `unanimous_authoritative_value`;
- distinct authoritative values or digests when heterogeneous;
- proof refs sufficient for fresh replay.

### Projection disposition

One typed disposition, at minimum:

- `VECTOR_HETEROGENEOUS_COMPLETE`
- `VECTOR_INCOMPLETE_COVERAGE`
- `VECTOR_GOVERNED_EMPTY_COMPONENT`
- `VECTOR_DENIED_OR_NONCOMPARABLE_COMPONENT`
- `SCALARIZED_COMPLETE_UNANIMOUS_NONEMPTY`

A scalar field/value may be non-null **only** for the last disposition.

## 4. Binding scalarization law

`SCALARIZE iff COMPLETE_COVERAGE && ALL_GOVERNED_COMPONENTS_NONEMPTY && UNANIMOUS_AUTHORITATIVE_VALUE`

Required hostile rejections:

- complete heterogeneous values -> no scalar;
- unanimous matched subset with incomplete coverage -> no scalar;
- complete coverage containing governed empty -> no scalar;
- denial/noncomparability -> no scalar absent a separately governed operation;
- complete unanimous non-empty -> scalar permitted, with vector and proof retained.

Forbidden substitutions:

- average;
- majority;
- first component;
- parent label;
- null/default coercion;
- drop empty/unresolved component;
- inferred membership from adjacency/co-location;
- semantic reownership by V557/V558.

## 5. Relationship to current objects

### V551J

Current V551J component machinery already supplies substantial input capital: stable component IDs, item order, component contracts, exact V551 atom links, unresolved/blocked component states, packet component-completeness checks and structural fields. This delta must **reuse those producer-owned refs**, not replace them with a second component store.

### I04

StructuralEmpiricalAdmission remains P06 admission authority. It must not absorb this new semantic responsibility merely because it already carries structural and negative refs.

### V557/V558 / M4

M4 already supplies exact mixed-producer publication, producer-preserving locators, role/order/cardinality/multiplicity reference edges, permission monotonicity and standalone closure. Once a lawful vector receipt exists, publication/repository may preserve it or its exact refs under the finally governed producer/publication contract.

MX02 does **not** authorize spoofing `ComponentAuthorityVectorReceipt` as V554/V555/V556 merely to satisfy the current V557 root allowlist. The eventual integration point must be separately governed.

## 6. What is NOT required

MX02 does not justify:

- a new component data warehouse;
- a new route-specific vector family;
- resurrection of old V552J courier semantics;
- copying every component field into one packet scalar row;
- rewriting V551J or V552J;
- changing M4 ownership law;
- changing V553/V554/V555/V556 semantics;
- A/B/C architecture changes;
- C09 work;
- V3 runtime work.

## 7. Fresh replay acceptance

A future implementation of the minimum receipt passes MX02 semantic closure only if a fresh reload from exact immutable refs reproduces exactly:

1. vector subject identity;
2. authority-dimension identity;
3. governed component identities;
4. producer ownership and hashes;
5. roles/order/multiplicity where governed;
6. component typed states/value bindings;
7. coverage proof;
8. non-empty proof;
9. unanimity/heterogeneity proof;
10. scalar disposition and scalar value where lawful;
11. negative refs and use ceiling.

Any hidden-latest, fuzzy repair, inferred missing component, or publication-time reownership fails closed.

## 8. HQ return

Minimum semantic delta: **one common producer-ref-binding vector closure/projection receipt**.

Physical carrier delta: **none proved necessary**.

Architecture redesign: **not authorized and not required by this result**.
