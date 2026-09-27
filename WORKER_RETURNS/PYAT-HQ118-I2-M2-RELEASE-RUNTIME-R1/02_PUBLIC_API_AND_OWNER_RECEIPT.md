# I2 M2 — PUBLIC API AND OWNER RECEIPT

## Current implementation surface

`rawlsing_next/pre553_learned_product_release.py`

Contract:

`PRE553_LEARNED_PRODUCT_RELEASE_RUNTIME@1.0.0`

## M2-owned logical types

- `ClosureObject` — immutable typed exact-ref closure.
- `ProducerSubject` — registration metadata pointing at an already producer-owned exact semantic subject.
- `ReleaseCore` — immutable content-addressed release identity.
- `RepresentationRecord` — exact representation-to-release/subject witness.
- `PublicationBinding` — immutable resolver/locator representation for one exact release.
- `ResolutionReceipt` — exact audit receipt for a single resolution operation.
- `ResolutionResult` — resolved release + producer subject + receipt.
- `ReleaseExplanation` — exact closure/lineage projection.
- `M2Repository` — exact-index in-memory runtime used as a storage-neutral reference realization.

## Public operations

- `register_producer_subject(...)`
- `constitute_closure(...)`
- `constitute_release(...)`
- `register_representation(...)`
- `publish_binding(...)`
- `resolve_release_exact(...)`
- `resolve_subject_exact(...)`
- `explain_release(...)`
- `affected_release_refs(...)`

## Release identity

ReleaseCore content identity binds exactly:
- release contract ref;
- release subject ref;
- subject kind;
- semantic producer contract ref;
- authority closure ref;
- dependency closure ref;
- determinant closure ref;
- replay/reconstruction ref;
- explanation-lineage ref.

No mutable path, endpoint, cache state, timestamp, current flag, latest/default selector, consumer permission or lifecycle publication state participates.

## Owner firewall

`ProducerSubject` does not copy/re-own producer semantics. It binds:
- exact producer subject ref;
- exact producer contract ref;
- subject kind;
- conserved typed state;
- exact semantic-anatomy ref;
- exact producer-declared closure requirements.

M2 validates these release conditions but does not author them.

Exact producer dereference is preserved by `resolve_subject_exact`.

## Resolution law

An exact release can resolve:
- directly to its registered producer subject; or
- through explicitly supplied exact PublicationBinding refs.

There is no registry operation for latest/default/nearest/fuzzy/semver selection.

Failover is explicit and ordered by the caller's exact binding refs; before failover begins every binding is verified to target the requested exact release.

## Replay grades

Replay closure must declare one exact grade:
- `EXACT_MATERIALIZED_DEREFERENCE`;
- `EXACT_DETERMINISTIC_REBUILD`;
- `EXACT_SERVICE_REEXECUTION`;
- `HISTORICAL_EXPLANATION_ONLY`.

Virtual rebuilding is accepted only for the exact deterministic-rebuild grade. Service resolution is accepted only for exact service-reexecution grade.

## Graph-only affected-set utility

`affected_release_refs(...)` traverses exact dependency/determinant membership only.

It does not classify:
- `RECERTIFIES`;
- `CORRECTS`;
- `WITHDRAWS`;
- `SUPERSEDES_COMPLETENESS_ONLY`;
- currentness or lifecycle publication.

Those remain B5/P2 jurisdiction.

Disposition:

`M2_RUNTIME_OWNER_BOUNDARY_PRESERVED`
