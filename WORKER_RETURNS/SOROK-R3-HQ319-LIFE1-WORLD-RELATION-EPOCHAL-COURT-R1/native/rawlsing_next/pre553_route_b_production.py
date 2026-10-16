"""PYAT M01 selected Route-B execution compositor.

This module packages already-governed PRE553 owners.  It does not infer source
meaning, create authority, adjudicate learned relations, publish/current-select
learned products, perform structural admission, or affect actor/V3 state.

The caller supplies:
- one exact physical incidence/stream,
- one already-constructed GovernedC11Projection,
- one exact RuntimeObjectCatalog,
- exact I03 request refs, and
- one exact DiscoveryAuthority ref.

All semantic work remains with the existing source-backed C11, I03 and I05
owners.  M01 only composes them and emits deterministic replay material.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_c11_repository import C11LogicalRelease
from rawlsing_next.pre553_carrier_execution import (
    CarrierExecutionBindingError,
    RepositoryBuilderBinding,
    RuntimeObjectCatalog,
    bind_repository_builder,
    governed_projection_binding_receipt,
    learned_empirical_execution_receipt,
    materialize_public_object,
)
from rawlsing_next.pre553_discovery_exact import ExactBoundedDiscoveryResult
from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    validate_object_authority_closure,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    CanonicalSemanticObject,
    DiscoveryAuthority,
    DiscoveryResultReceipt,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553IntegrityError,
    canonical_json,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_physical_decoder import PhysicalSourceIncidence
from rawlsing_next.pre553_source_backed_c11_facade import (
    CONTRACT_ID as SOURCE_BACKED_C11_CONTRACT_ID,
    ExactPhysicalCellStream,
    GovernedC11Projection,
    SourceBackedC11SessionCache,
    build_source_backed_c11_repository,
)


ROUTE_B_PRODUCTION_CONTRACT_ID = "PYAT_M01_ROUTE_B_PRODUCTION_COMPOSITOR@1.0.0"
ROUTE_B_EXECUTION_RECEIPT_SCHEMA = "PYAT_M01_ROUTE_B_EXECUTION_REPLAY_RECEIPT@1.0.0"

_CONSERVED_TERMINAL_OR_NEGATIVE_STATES = frozenset({
    "VALID_EMPTY",
    "NONCOMPARABLE",
    "UNAVAILABLE",
    "NOT_APPLICABLE",
    "ZERO_SUPPORT",
    "ZERO_OVERLAP",
    "OBSERVED_ZERO",
    "LOW_SUPPORT",
    "INSUFFICIENT_SUPPORT",
    "ROUTING_UNKNOWN",
    "RULE_UNAVAILABLE",
    "WEIGHT_MISSING",
    "WEIGHT_INVALID",
    "WEIGHT_NOT_AUTHORIZED",
    "WEIGHT_BASIS_UNRESOLVED",
    "NOT_ASKED",
    "INAPPLICABLE",
    "NOT_ELIGIBLE",
    "UNKNOWN",
    "MISSING",
    "DEFERRED",
    "DISTINCT_BY_DEFAULT",
})

_EFFECTS = {
    "learned_empirical_adjudication_effect": False,
    "learned_product_publication_effect": False,
    "learned_product_current_selection_effect": False,
    "structural_truth_effect": False,
    "causal_truth_effect": False,
    "actor_v3_effect": False,
}


class RouteBProductionError(Pre553IntegrityError):
    """The exact selected-B execution package is incomplete or inconsistent."""


@dataclass(frozen=True)
class I03ExecutionRequest:
    query_ref: ExactRef
    predicate_ref: ExactRef

    def __post_init__(self) -> None:
        object.__setattr__(self, "query_ref", exact_ref(self.query_ref, "query_ref"))
        object.__setattr__(
            self, "predicate_ref", exact_ref(self.predicate_ref, "predicate_ref")
        )

    @property
    def request_identity(self) -> str:
        return semantic_hash({
            "schema": "PYAT_M01_I03_EXECUTION_REQUEST@1.0.0",
            "query_ref": self.query_ref.as_dict(),
            "predicate_ref": self.predicate_ref.as_dict(),
        })

    def as_dict(self) -> Mapping[str, Any]:
        return {
            "query_ref": self.query_ref.as_dict(),
            "predicate_ref": self.predicate_ref.as_dict(),
            "request_identity": self.request_identity,
        }


@dataclass(frozen=True)
class RouteBEmpiricalObjectGraph:
    authority_snapshots: tuple[AuthoritySnapshot, ...]
    executed_predicates: tuple[EmpiricalPredicate, ...]
    executed_queries: tuple[EmpiricalQuerySpec, ...]
    empirical_facts: tuple[EmpiricalFact, ...]
    discovery_authorities: tuple[DiscoveryAuthority, ...]
    discovery_receipts: tuple[DiscoveryResultReceipt, ...]

    def public_objects(self) -> tuple[CanonicalSemanticObject, ...]:
        return (
            *self.authority_snapshots,
            *self.executed_predicates,
            *self.executed_queries,
            *self.empirical_facts,
            *self.discovery_authorities,
            *self.discovery_receipts,
        )


@dataclass(frozen=True)
class RouteBProductionResult:
    source_identity: Mapping[str, Any]
    projection_binding_receipt: Mapping[str, Any]
    repository_binding: RepositoryBuilderBinding
    c11_release: C11LogicalRelease
    i03_results: tuple[QueryExecutionResult, ...]
    i05_result: ExactBoundedDiscoveryResult
    object_graph: RouteBEmpiricalObjectGraph
    learned_empirical_execution_receipt: Mapping[str, Any]
    replay_receipt: Mapping[str, Any]


def _canonical_objects(
    objects: Iterable[CanonicalSemanticObject],
    expected_type: type[CanonicalSemanticObject],
    label: str,
) -> tuple[CanonicalSemanticObject, ...]:
    by_ref: dict[str, CanonicalSemanticObject] = {}
    for obj in objects:
        if not isinstance(obj, expected_type):
            raise RouteBProductionError(f"{label} contains wrong exact object family")
        if semantic_hash(obj.semantic_projection()) != obj.content_hash:
            raise RouteBProductionError(f"{label} contains identity-drifted object")
        prior = by_ref.get(obj.ref.key)
        if prior is not None and canonical_json(prior.as_dict()) != canonical_json(obj.as_dict()):
            raise RouteBProductionError(f"{label} contains conflicting exact preimages")
        by_ref[obj.ref.key] = obj
    return tuple(by_ref[key] for key in sorted(by_ref))


def _canonical_authorities(
    objects: Iterable[AuthoritySnapshot],
) -> tuple[AuthoritySnapshot, ...]:
    by_authority: dict[str, AuthoritySnapshot] = {}
    for obj in objects:
        if not isinstance(obj, AuthoritySnapshot):
            raise RouteBProductionError("authority graph contains non-AuthoritySnapshot")
        if semantic_hash(obj.semantic_projection()) != obj.content_hash:
            raise RouteBProductionError("authority graph contains identity-drifted object")
        key = obj.authority_ref.key
        prior = by_authority.get(key)
        if prior is not None and canonical_json(prior.as_dict()) != canonical_json(obj.as_dict()):
            raise RouteBProductionError("one exact authority ref has conflicting preimages")
        by_authority[key] = obj
    return tuple(by_authority[key] for key in sorted(by_authority))


def _source_identity(
    source: PhysicalSourceIncidence | ExactPhysicalCellStream,
) -> Mapping[str, Any]:
    if isinstance(source, PhysicalSourceIncidence):
        material = {
            "schema": "PYAT_M01_EXACT_PHYSICAL_SOURCE_IDENTITY@1.0.0",
            "transport_kind": "PhysicalSourceIncidence",
            "source_sha256": source.source_sha256,
            "row_count": source.row_count,
            "physical_metadata_digest": source.physical_metadata_digest,
        }
    elif isinstance(source, ExactPhysicalCellStream):
        material = {
            "schema": "PYAT_M01_EXACT_PHYSICAL_SOURCE_IDENTITY@1.0.0",
            "transport_kind": "ExactPhysicalCellStream",
            "transport_identity": source.transport_identity,
            "source_sha256": source.source_sha256,
            "row_count": source.row_count,
        }
    else:
        raise RouteBProductionError(
            "source must be exact PhysicalSourceIncidence or ExactPhysicalCellStream"
        )
    return {**material, "source_identity": semantic_hash(material)}


def _normalize_i03_requests(
    requests: Iterable[I03ExecutionRequest | Mapping[str, Any]],
) -> tuple[I03ExecutionRequest, ...]:
    normalized: dict[tuple[str, str], I03ExecutionRequest] = {}
    for raw in requests:
        if isinstance(raw, I03ExecutionRequest):
            request = raw
        elif isinstance(raw, Mapping):
            if set(raw) != {"query_ref", "predicate_ref"}:
                raise RouteBProductionError(
                    "I03 request mapping must contain exactly query_ref and predicate_ref"
                )
            request = I03ExecutionRequest(
                query_ref=exact_ref(raw["query_ref"], "query_ref"),
                predicate_ref=exact_ref(raw["predicate_ref"], "predicate_ref"),
            )
        else:
            raise RouteBProductionError("I03 requests must be exact typed requests")
        key = (request.query_ref.key, request.predicate_ref.key)
        if key in normalized:
            raise RouteBProductionError("duplicate exact I03 request")
        normalized[key] = request
    if not normalized:
        raise RouteBProductionError("M01 requires one or more exact I03 requests")
    return tuple(normalized[key] for key in sorted(normalized))


def _projection_absence_states(
    projection: GovernedC11Projection,
) -> Mapping[str, str]:
    values = {
        "source_relations": projection.source_relations,
        "predicate_replay": projection.predicate_replay,
        "comparator_replay": projection.comparator_replay,
        "discovery_replay": projection.discovery_replay,
        "structural_replay": projection.structural_replay,
    }
    return {
        name: value.state
        for name, value in values.items()
        if isinstance(value, TypedAbsence)
    }


def _build_object_graph(
    *,
    projection: GovernedC11Projection,
    runtime_catalog: RuntimeObjectCatalog,
    requests: tuple[I03ExecutionRequest, ...],
    i03_results: tuple[QueryExecutionResult, ...],
    i05_result: ExactBoundedDiscoveryResult,
    discovery_authority: DiscoveryAuthority,
) -> RouteBEmpiricalObjectGraph:
    predicates = _canonical_objects(
        (
            *(runtime_catalog.resolve_predicate_exact(r.predicate_ref) for r in requests),
            *i05_result.executed_predicates,
        ),
        EmpiricalPredicate,
        "executed predicates",
    )
    queries = _canonical_objects(
        (
            *(runtime_catalog.resolve_query_exact(r.query_ref) for r in requests),
            *i05_result.executed_queries,
        ),
        EmpiricalQuerySpec,
        "executed queries",
    )
    facts = _canonical_objects(
        (
            *(fact for result in i03_results for fact in result.facts),
            *i05_result.empirical_facts,
        ),
        EmpiricalFact,
        "empirical facts",
    )
    receipts = _canonical_objects(
        i05_result.receipts,
        DiscoveryResultReceipt,
        "discovery receipts",
    )
    discoveries = _canonical_objects(
        (discovery_authority,),
        DiscoveryAuthority,
        "discovery authorities",
    )
    authorities = _canonical_authorities(
        (*projection.authority_snapshots, *runtime_catalog.authorities)
    )
    registry = AuthorityRegistry(authorities)
    for obj in (*predicates, *queries, *facts, *discoveries, *receipts):
        validate_object_authority_closure(obj, registry)
    return RouteBEmpiricalObjectGraph(
        authority_snapshots=authorities,
        executed_predicates=predicates,
        executed_queries=queries,
        empirical_facts=facts,
        discovery_authorities=discoveries,
        discovery_receipts=receipts,
    )


def _typed_state_receipt(
    *,
    release: C11LogicalRelease,
    projection: GovernedC11Projection,
    graph: RouteBEmpiricalObjectGraph,
) -> Mapping[str, Any]:
    c11_states = tuple(sorted({
        obj.typed_state
        for obj in release.public_objects
        if hasattr(obj, "typed_state")
    }))
    fact_states = tuple(sorted({obj.typed_state for obj in graph.empirical_facts}))
    discovery_states = tuple(sorted({obj.typed_state for obj in graph.discovery_receipts}))
    coverage_states = tuple(sorted({obj.coverage_state for obj in graph.discovery_receipts}))
    projection_absences = _projection_absence_states(projection)
    all_states = set(c11_states) | set(fact_states) | set(discovery_states)
    all_states |= set(coverage_states) | set(projection_absences.values())
    return {
        "c11_public_object_states": c11_states,
        "empirical_fact_states": fact_states,
        "discovery_result_states": discovery_states,
        "discovery_coverage_states": coverage_states,
        "projection_typed_absence_states": projection_absences,
        "conserved_terminal_or_negative_states": tuple(
            sorted(all_states & _CONSERVED_TERMINAL_OR_NEGATIVE_STATES)
        ),
    }


def _preimages(graph: RouteBEmpiricalObjectGraph) -> Mapping[str, Any]:
    return {
        "authority_snapshots": [obj.as_dict() for obj in graph.authority_snapshots],
        "executed_predicates": [obj.as_dict() for obj in graph.executed_predicates],
        "executed_queries": [obj.as_dict() for obj in graph.executed_queries],
        "empirical_facts": [obj.as_dict() for obj in graph.empirical_facts],
        "discovery_authorities": [obj.as_dict() for obj in graph.discovery_authorities],
        "discovery_receipts": [obj.as_dict() for obj in graph.discovery_receipts],
    }


def _dependency_material(
    *,
    source_identity: Mapping[str, Any],
    projection_receipt: Mapping[str, Any],
    projection: GovernedC11Projection,
    binding_receipt: Mapping[str, Any],
    release: C11LogicalRelease,
    runtime_catalog: RuntimeObjectCatalog,
    requests: tuple[I03ExecutionRequest, ...],
    i03_results: tuple[QueryExecutionResult, ...],
    i05_result: ExactBoundedDiscoveryResult,
    graph: RouteBEmpiricalObjectGraph,
    typed_states: Mapping[str, Any],
) -> Mapping[str, Any]:
    return {
        "contract": ROUTE_B_PRODUCTION_CONTRACT_ID,
        "source_identity": source_identity,
        "projection_binding_identity": projection_receipt["binding_identity"],
        "projection_identity_ref": projection.projection_identity_ref.as_dict(),
        "projection_authority_ref": projection.projection_authority_ref.as_dict(),
        "replay_authority_ref": projection.replay_authority_ref.as_dict(),
        "c11": {
            "release_ref": release.release_ref.as_dict(),
            "release_replay_ref": release.replay_manifest.ref.as_dict(),
            "source_artifact_ref": release.source_artifact_ref.as_dict(),
            "source_release_manifest_hash": release.source_release_manifest_hash,
            "semantic_release_hash": release.semantic_release_hash,
        },
        "repository_executor_binding_identity": binding_receipt["binding_identity"],
        "runtime_catalog_identity": runtime_catalog.receipt()["catalog_identity"],
        "i03": [
            {
                "request": request.as_dict(),
                "query_ref": result.query_ref.as_dict(),
                "release_refs": [ref.as_dict() for ref in result.release_refs],
                "fact_refs": [fact.ref.as_dict() for fact in result.facts],
            }
            for request, result in zip(requests, i03_results)
        ],
        "i05": {
            "discovery_authority_ref": i05_result.discovery_authority_ref.as_dict(),
            "candidate_grammar_ref": i05_result.candidate_grammar_ref.as_dict(),
            "evaluated_frontier_ref": i05_result.evaluated_frontier_ref.as_dict(),
            "replay_ref": i05_result.replay_ref.as_dict(),
            "candidate_count": i05_result.candidate_count,
            "covered_candidate_count": i05_result.covered_candidate_count,
            "valid_empty": i05_result.valid_empty,
            "discovery_receipt_refs": [
                obj.ref.as_dict() for obj in i05_result.receipts
            ],
            "empirical_fact_refs": [
                ref.as_dict() for ref in i05_result.empirical_fact_refs
            ],
        },
        "object_graph_refs": {
            "authority_snapshot_object_refs": [
                obj.ref.as_dict() for obj in graph.authority_snapshots
            ],
            "authority_refs": [
                obj.authority_ref.as_dict() for obj in graph.authority_snapshots
            ],
            "executed_predicate_refs": [
                obj.ref.as_dict() for obj in graph.executed_predicates
            ],
            "executed_query_refs": [
                obj.ref.as_dict() for obj in graph.executed_queries
            ],
            "empirical_fact_refs": [
                obj.ref.as_dict() for obj in graph.empirical_facts
            ],
            "discovery_authority_refs": [
                obj.ref.as_dict() for obj in graph.discovery_authorities
            ],
            "discovery_receipt_refs": [
                obj.ref.as_dict() for obj in graph.discovery_receipts
            ],
        },
        "typed_states": typed_states,
        "effects": _EFFECTS,
    }


def _build_replay_receipt(
    *,
    source_identity: Mapping[str, Any],
    projection_receipt: Mapping[str, Any],
    projection: GovernedC11Projection,
    binding_receipt: Mapping[str, Any],
    release: C11LogicalRelease,
    runtime_catalog: RuntimeObjectCatalog,
    requests: tuple[I03ExecutionRequest, ...],
    i03_results: tuple[QueryExecutionResult, ...],
    i05_result: ExactBoundedDiscoveryResult,
    graph: RouteBEmpiricalObjectGraph,
    typed_states: Mapping[str, Any],
) -> Mapping[str, Any]:
    dependency_material = _dependency_material(
        source_identity=source_identity,
        projection_receipt=projection_receipt,
        projection=projection,
        binding_receipt=binding_receipt,
        release=release,
        runtime_catalog=runtime_catalog,
        requests=requests,
        i03_results=i03_results,
        i05_result=i05_result,
        graph=graph,
        typed_states=typed_states,
    )
    material = {
        "schema": ROUTE_B_EXECUTION_RECEIPT_SCHEMA,
        "contract": ROUTE_B_PRODUCTION_CONTRACT_ID,
        "source_identity": source_identity,
        "projection_binding_receipt": projection_receipt,
        "repository_executor_binding_receipt": binding_receipt,
        "runtime_catalog_receipt": runtime_catalog.receipt(),
        "dependency_material": dependency_material,
        "dependency_root": semantic_hash(dependency_material),
        "object_preimages": _preimages(graph),
        "typed_states": typed_states,
        "effects": _EFFECTS,
    }
    return {**material, "receipt_identity": semantic_hash(material)}


def execute_route_b_production(
    *,
    source: PhysicalSourceIncidence | ExactPhysicalCellStream,
    projection: GovernedC11Projection,
    runtime_catalog: RuntimeObjectCatalog,
    i03_requests: Iterable[I03ExecutionRequest | Mapping[str, Any]],
    discovery_authority_ref: ExactRef | Mapping[str, Any],
    cache: SourceBackedC11SessionCache | None = None,
    batch_size: int = 10_000,
) -> RouteBProductionResult:
    """Compose the existing selected-B physical/C11/I03/I05 owners exactly."""
    if not isinstance(projection, GovernedC11Projection):
        raise RouteBProductionError(
            "caller-owned exact GovernedC11Projection is required"
        )
    if not isinstance(runtime_catalog, RuntimeObjectCatalog):
        raise RouteBProductionError("exact RuntimeObjectCatalog is required")
    if cache is not None and not isinstance(cache, SourceBackedC11SessionCache):
        raise RouteBProductionError("cache must be SourceBackedC11SessionCache or None")
    if not isinstance(batch_size, int) or isinstance(batch_size, bool) or batch_size < 1:
        raise RouteBProductionError("batch_size must be a positive integer")

    source_identity = _source_identity(source)
    if source_identity["source_sha256"] != projection.expected_source_sha256:
        raise RouteBProductionError("source/projection exact source identity mismatch")

    requests = _normalize_i03_requests(i03_requests)
    discovery_ref = exact_ref(
        discovery_authority_ref, "discovery_authority_ref"
    )
    discovery_authority = runtime_catalog.resolve_discovery_authority_exact(
        discovery_ref
    )

    projection_receipt = governed_projection_binding_receipt(projection)

    catalog_authority_refs = {
        snapshot.authority_ref for snapshot in runtime_catalog.authorities
    }
    required_projection_authorities = set(projection.required_authority_refs)
    if not required_projection_authorities.issubset(catalog_authority_refs):
        raise RouteBProductionError(
            "runtime catalog omits exact projection authority closure"
        )
    if projection.projection_authority_ref not in catalog_authority_refs:
        raise RouteBProductionError(
            "runtime catalog omits exact projection authority"
        )

    builder_identity = {
        "schema": "PYAT_M01_ROUTE_B_REPOSITORY_BUILDER_BINDING@1.0.0",
        "contract": ROUTE_B_PRODUCTION_CONTRACT_ID,
        "semantic_owner_contract": SOURCE_BACKED_C11_CONTRACT_ID,
        "builder": "build_source_backed_c11_repository",
        "source_identity": source_identity,
        "projection_binding_identity": projection_receipt["binding_identity"],
        "projection_identity_ref": projection.projection_identity_ref.as_dict(),
        "semantic_inference_performed": False,
        "cache_is_semantically_authoritative": False,
    }
    try:
        binding = bind_repository_builder(
            repository_builder=build_source_backed_c11_repository,
            builder_kwargs={
                "source": source,
                "projection": projection,
                "cache": cache,
                "batch_size": batch_size,
            },
            builder_identity=builder_identity,
            runtime_catalog=runtime_catalog,
        )
    except (CarrierExecutionBindingError, ValueError, TypeError) as exc:
        raise RouteBProductionError(
            f"exact source-backed repository composition failed: {exc}"
        ) from exc

    release = binding.executor.repository.resolve_release_exact(binding.release_ref)
    if release.source_artifact_ref.content_hash != source_identity["source_sha256"]:
        raise RouteBProductionError("bound C11 release/source identity drift")
    if release.release_ref != binding.release_ref:
        raise RouteBProductionError("repository binding release identity drift")

    i03_results: list[QueryExecutionResult] = []
    for request in requests:
        i03_results.append(
            binding.executor.execute_i03(
                query_ref=request.query_ref,
                predicate_ref=request.predicate_ref,
            )
        )
    i03_results_tuple = tuple(i03_results)

    i05_result = binding.executor.execute_i05(
        discovery_authority_ref=discovery_ref
    )
    learned_receipt = learned_empirical_execution_receipt(i05_result)

    graph = _build_object_graph(
        projection=projection,
        runtime_catalog=runtime_catalog,
        requests=requests,
        i03_results=i03_results_tuple,
        i05_result=i05_result,
        discovery_authority=discovery_authority,
    )
    typed_states = _typed_state_receipt(
        release=release, projection=projection, graph=graph
    )
    binding_receipt = binding.receipt()
    replay_receipt = _build_replay_receipt(
        source_identity=source_identity,
        projection_receipt=projection_receipt,
        projection=projection,
        binding_receipt=binding_receipt,
        release=release,
        runtime_catalog=runtime_catalog,
        requests=requests,
        i03_results=i03_results_tuple,
        i05_result=i05_result,
        graph=graph,
        typed_states=typed_states,
    )
    verify_route_b_replay_receipt(replay_receipt)

    return RouteBProductionResult(
        source_identity=source_identity,
        projection_binding_receipt=projection_receipt,
        repository_binding=binding,
        c11_release=release,
        i03_results=i03_results_tuple,
        i05_result=i05_result,
        object_graph=graph,
        learned_empirical_execution_receipt=learned_receipt,
        replay_receipt=replay_receipt,
    )


def verify_route_b_replay_receipt(receipt: Mapping[str, Any]) -> str:
    """Fail closed on M01 receipt/preimage tampering and return dependency root."""
    if not isinstance(receipt, Mapping):
        raise RouteBProductionError("M01 replay receipt must be a mapping")
    expected_keys = {
        "schema",
        "contract",
        "source_identity",
        "projection_binding_receipt",
        "repository_executor_binding_receipt",
        "runtime_catalog_receipt",
        "dependency_material",
        "dependency_root",
        "object_preimages",
        "typed_states",
        "effects",
        "receipt_identity",
    }
    if set(receipt) != expected_keys:
        raise RouteBProductionError("M01 replay receipt shape mismatch")
    if receipt["schema"] != ROUTE_B_EXECUTION_RECEIPT_SCHEMA:
        raise RouteBProductionError("M01 replay receipt schema mismatch")
    if receipt["contract"] != ROUTE_B_PRODUCTION_CONTRACT_ID:
        raise RouteBProductionError("M01 replay receipt contract mismatch")
    if receipt["effects"] != _EFFECTS:
        raise RouteBProductionError("M01 replay receipt attempts semantic promotion")

    dependency_material = receipt["dependency_material"]
    if not isinstance(dependency_material, Mapping):
        raise RouteBProductionError("M01 dependency material must be exact mapping")
    observed_root = semantic_hash(dependency_material)
    if observed_root != receipt["dependency_root"]:
        raise RouteBProductionError("M01 deterministic dependency root mismatch")

    without_identity = {
        key: value for key, value in receipt.items() if key != "receipt_identity"
    }
    if semantic_hash(without_identity) != receipt["receipt_identity"]:
        raise RouteBProductionError("M01 receipt identity mismatch")

    preimages = receipt["object_preimages"]
    if not isinstance(preimages, Mapping):
        raise RouteBProductionError("M01 object preimages must be a mapping")
    preimage_keys = {
        "authority_snapshots",
        "executed_predicates",
        "executed_queries",
        "empirical_facts",
        "discovery_authorities",
        "discovery_receipts",
    }
    if set(preimages) != preimage_keys:
        raise RouteBProductionError("M01 object preimage family set mismatch")

    expected_types = {
        "authority_snapshots": AuthoritySnapshot,
        "executed_predicates": EmpiricalPredicate,
        "executed_queries": EmpiricalQuerySpec,
        "empirical_facts": EmpiricalFact,
        "discovery_authorities": DiscoveryAuthority,
        "discovery_receipts": DiscoveryResultReceipt,
    }
    rebuilt: dict[str, tuple[CanonicalSemanticObject, ...]] = {}
    for family, expected_type in expected_types.items():
        documents = preimages[family]
        if not isinstance(documents, list):
            raise RouteBProductionError(f"{family} preimages must be a list")
        objects = tuple(materialize_public_object(document) for document in documents)
        if any(not isinstance(obj, expected_type) for obj in objects):
            raise RouteBProductionError(f"{family} contains wrong exact object family")
        canonical_key = (
            (lambda obj: obj.authority_ref.key)
            if family == "authority_snapshots"
            else (lambda obj: obj.ref.key)
        )
        if tuple(sorted(objects, key=canonical_key)) != objects:
            raise RouteBProductionError(f"{family} preimages are not canonically ordered")
        if len({obj.ref.key for obj in objects}) != len(objects):
            raise RouteBProductionError(f"{family} preimages contain duplicate exact ref")
        rebuilt[family] = objects

    refs = dependency_material.get("object_graph_refs")
    if not isinstance(refs, Mapping):
        raise RouteBProductionError("M01 object graph refs missing")
    expected_ref_lists = {
        "authority_snapshot_object_refs": [
            obj.ref.as_dict() for obj in rebuilt["authority_snapshots"]
        ],
        "authority_refs": [
            obj.authority_ref.as_dict() for obj in rebuilt["authority_snapshots"]
        ],
        "executed_predicate_refs": [
            obj.ref.as_dict() for obj in rebuilt["executed_predicates"]
        ],
        "executed_query_refs": [
            obj.ref.as_dict() for obj in rebuilt["executed_queries"]
        ],
        "empirical_fact_refs": [
            obj.ref.as_dict() for obj in rebuilt["empirical_facts"]
        ],
        "discovery_authority_refs": [
            obj.ref.as_dict() for obj in rebuilt["discovery_authorities"]
        ],
        "discovery_receipt_refs": [
            obj.ref.as_dict() for obj in rebuilt["discovery_receipts"]
        ],
    }
    if dict(refs) != expected_ref_lists:
        raise RouteBProductionError("M01 object graph refs/preimages do not close exactly")

    if dependency_material.get("effects") != _EFFECTS:
        raise RouteBProductionError("M01 dependency material attempts semantic promotion")
    if receipt["typed_states"] != dependency_material.get("typed_states"):
        raise RouteBProductionError("M01 typed terminal-state receipt drift")

    return receipt["dependency_root"]


__all__ = [
    "ROUTE_B_PRODUCTION_CONTRACT_ID",
    "ROUTE_B_EXECUTION_RECEIPT_SCHEMA",
    "RouteBProductionError",
    "I03ExecutionRequest",
    "RouteBEmpiricalObjectGraph",
    "RouteBProductionResult",
    "execute_route_b_production",
    "verify_route_b_replay_receipt",
]
