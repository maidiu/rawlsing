# PRE553 runtime namespace and interface law

## Executable geography

All new executable implementation and executable tests belong under `rawlsing_next/**`.

Planned namespace after contract acceptance:

- `rawlsing_next/pre553/object_model.py`
- `rawlsing_next/pre553/authority.py`
- `rawlsing_next/pre553/c11_repository.py`
- `rawlsing_next/pre553/c11_ingest.py`
- `rawlsing_next/pre553/c11_integrity.py`
- `rawlsing_next/pre553/empirical_predicate.py`
- `rawlsing_next/pre553/empirical_query.py`
- `rawlsing_next/pre553/discovery.py`
- `rawlsing_next/pre553/discovery_replay.py`
- `rawlsing_next/pre553/source_equivalence.py`
- `rawlsing_next/pre553/source_plurality.py`
- `rawlsing_next/pre553/structural_admission.py`
- `rawlsing_next/pre553/v553_ingress.py`
- executable tests under `rawlsing_next/tests/`.

Names are provisional until Wave-01 HQ synthesis; workers must not create these files during preflight.

## Forbidden executable geography

No new runtime or executable tests under:

- `data/ddm_build/**`
- `data/ddm_build_copy/**`

The sole write exception is governance/spec/evidence under `data/ddm_build_copy/vozhd_trii/**`.

## Downstream boundary

Accepted downstream executable head is `e51730e461a15b0ad20f02f2efb4bccd751c2c81`.

Pre553 must target the already-accepted M1/V553-V554 ingress semantics rather than changing them by convenience. M1 direct admission projections already require exact StructuralEmpiricalAdmission identity/hash, authority, focal proposition, structural semantic identity, native scope, target-use permissions, temporal requirements, source universe, estimand, weight/measure authority, applicable negatives, interpretation-critical authority, and replay root.

Any proposed pre553 contract unable to populate those fields must fail closed or prove a real contradiction to HQ; it may not erase fields from M1.

## Canonical object boundary

The campaign must distinguish at least:

`EmpiricalUniverse`
`RespondentEvent`
`EmpiricalCoordinateFact`
`RoutingEligibilityFact`
`WeightMeasureFact`
`AuthoritySnapshot`
`SourceUniverseRelation`
`EmpiricalPredicate`
`EmpiricalQuerySpec`
`EmpiricalFact`
`DiscoveryAuthority`
`DiscoveryResultReceipt`
`StructuralEmpiricalAdmission`
`ReplayReceipt`

The first reservoir milestone does not require `ActorComparatorReceipt`, `PositionedSubjectEmpiricalPossibilityField`, or `V3EmpiricalPossibilityInput`; those remain target architecture but are deferred from the critical path.

## Deep carrier law

D13 C11 M01-M18 is the minimum information frontier. Implementations may store more but may not store less without proof of exact information equivalence for every D12 required frontier query.

Current Postgres/facet/shared-V550 surfaces are migration inputs and validation oracles only. They were statically proven insufficient as the complete future-frontier carrier. Legacy helpers may not be imported into the new runtime merely because they exist.

## Cache law

Any materialized E1/E2/branch/diagnostic view is optional and nonauthoritative. Cache miss must be resolvable through exact C11 replay. Cache contents never widen authority, source composition, workload authority, structural meaning, or actor semantics.