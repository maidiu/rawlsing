# MX02 HOSTILE CASES

Binding oracle:

`SCALARIZE iff COMPLETE_COVERAGE && ALL_GOVERNED_COMPONENTS_NONEMPTY && UNANIMOUS_AUTHORITATIVE_VALUE`

The experiment separates **carrier representability** from **lawful semantic authority**. A generic payload that can hold the bits is not enough.

## H1 — HETEROGENEOUS_COMPLETE

Fixture:

- governed components: `c1`, `c2`;
- exact component coverage: complete;
- component values: `stratum:A`, `stratum:B`;
- values are both non-empty and authoritative;
- producers may differ.

Required result:

- ordered component vector survives;
- producer refs survive;
- scalar is blank/absent;
- disposition: `VECTOR_HETEROGENEOUS_COMPLETE`.

Modern finding:

- V551J component identity/order and M4 exact refs/edges can preserve the evidence;
- no accepted common semantic receipt owns the heterogeneity/scalar-forbidden decision.

Disposition: `FAIL_CLOSED__MISSING_COMMON_VECTOR_RECEIPT`.

Historical anchor: Section35 / accepted `A010`.

## H2 — INCOMPLETE_COVERAGE

Fixture:

- governed components: `c1`, `c2`;
- only `c1` is resolved/present for the projected authority dimension, or `c2` is explicitly unresolved;
- the resolved subset is internally unanimous.

Required result:

- incomplete governed set remains visible;
- matched-subset unanimity does not count as packet/vector unanimity;
- scalar forbidden;
- disposition: `VECTOR_INCOMPLETE_COVERAGE`.

Modern finding:

- current V551J exposes unresolved components and packet-level component-contract completeness/order integrity;
- M4 can preserve explicit negative/unresolved dependencies;
- no common vector receipt binds the exact governed set to the exact authority dimension and certifies completeness.

Disposition: `FAIL_CLOSED__MISSING_COMMON_COVERAGE_RECEIPT`.

Historical anchor: Section35 / accepted `A011`.

## H3 — GOVERNED_EMPTY_COMPONENT

Fixture:

- governed components: `c1`, `c2`;
- complete identity coverage;
- `c1 = stratum:A`;
- `c2 = GOVERNED_EMPTY` under its producer authority.

Required result:

- typed governed-empty state survives;
- empty is not silently dropped;
- empty is not coerced to zero/default;
- scalar forbidden;
- disposition: `VECTOR_GOVERNED_EMPTY_COMPONENT`.

Modern finding:

- negative/typed states and exact negative refs can be carried;
- no accepted common vector projection authority binds governed-empty semantics to the scalarization gate.

Disposition: `FAIL_CLOSED__MISSING_COMMON_EMPTY_SCALARIZATION_OWNER`.

Historical anchor: Section35 / accepted `A012`.

## H4 — UNANIMOUS_COMPLETE_NONEMPTY

Fixture:

- governed components: `c1`, `c2`;
- exact complete coverage;
- both authoritative values are `stratum:A`;
- no empty/unresolved/noncomparability state.

Required result:

- vector remains replayable as source proof;
- scalar projection is lawful;
- scalar value: `stratum:A`;
- disposition: `SCALARIZED_COMPLETE_UNANIMOUS_NONEMPTY`;
- scalar must carry exact completeness/unanimity proof.

Modern finding:

- equality can be computed from dereferenced producer values;
- current common contracts do not authorize a consumer, V557, or V558 to mint that scalar as semantic authority.

Disposition: `FAIL_CLOSED__NO_ACCEPTED_COMMON_SCALAR_PROJECTION_AUTHORITY`.

Historical anchor: Section35 scalarization law recovered by R03/R04.

## H5 — MIXED_PRODUCER_PUBLICATION

Fixture:

- `c1` and `c2` are exact immutable component refs;
- the refs are owned by distinct lawful producers;
- publication/repository reload must preserve producer tuple, component identity and reference role without flattening or reownership.

Required result:

- exact producer identity survives;
- exact content hashes survive;
- role/order/cardinality/multiplicity metadata survives where governed;
- permission only narrows;
- no filler transformation is required solely for publication.

Modern finding:

- M4 provides this machinery directly through `StructuralObject`, `V557GovernanceRecord`, `ProducerLocator`, `ReferenceEdge`, and `V558RepositoryBundle`;
- M4 explicitly verifies producer tuple preservation and exact role-preserving dependency closure.

Disposition: `STATIC_CONTRACT_PROOF_PASS__CARRIER_ONLY`.

Negative ceiling:

This PASS does not authorize M4 to become the owner of component-vector semantics.

## Executable oracle receipt

`mx02_component_vector_harness.py` executed the five scalar-oracle cases in an isolated standard-library harness. `HARNESS_RECEIPT.json` records 5/5 assertions passing.

That execution proves the binding oracle is internally discriminating; it does not substitute for the exact-current-code semantic sufficiency adjudication recorded in `MODERN_OBJECT_SUFFICIENCY_MATRIX.csv`.
