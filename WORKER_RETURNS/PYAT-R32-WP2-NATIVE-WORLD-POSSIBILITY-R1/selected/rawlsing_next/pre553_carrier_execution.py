"""Carrier-neutral PRE553 C11 -> I03/I05 production execution seam.

This module is deliberately non-semantic infrastructure.  It never infers source
meaning, chooses a wave, discovers a physical column, selects a risk set, or
changes candidate A/B/C meaning.  Source/wave authority packages must supply
complete PRE553 objects and a sealed C11 repository.  This layer only:

1. re-materializes already serialized canonical PRE553 objects under their own
   deterministic identity law;
2. resolves exact refs without latest/default/fuzzy fallback; and
3. executes the existing I03/I05 contracts against an exact C11 repository.

A hash is never inverted here.  If a canonical object preimage is absent, the
caller must fail closed or obtain it from governed authority lineage.
"""
from __future__ import annotations

from dataclasses import dataclass, fields as dataclass_fields
from typing import Any, Callable, Iterable, Mapping

from rawlsing_next._pre553_query_common import (
    QUERY_EXECUTION_CONTRACT_ID,
    QueryExecutionResult,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_discovery_exact import (
    I05_CONTRACT_ID,
    ExactBoundedDiscoveryResult,
    execute_exact_bounded_discovery,
)
from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    validate_object_authority_closure,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    CanonicalSemanticObject,
    canonicalize,
    DiscoveryAuthority,
    DiscoveryResultReceipt,
    EmpiricalCoordinateFact,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    EmpiricalUniverse,
    ExactRef,
    Pre553IntegrityError,
    ReplayReceipt,
    RespondentEvent,
    RoutingEligibilityFact,
    SourceUniverseRelation,
    StructuralEmpiricalAdmission,
    WeightMeasureFact,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_source_backed_c11_facade import GovernedC11Projection


CARRIER_EXECUTION_CONTRACT_ID = (
    "PRE553_CARRIER_NEUTRAL_C11_I03_I05_EXECUTION_BINDING@1.0.0"
)


class CarrierExecutionBindingError(Pre553IntegrityError):
    """The supplied exact execution binding cannot lawfully be materialized."""


_PUBLIC_CLASS_BY_SCHEMA: Mapping[tuple[str, str], type[CanonicalSemanticObject]] = {
    ("EmpiricalUniverse", "1.0.0"): EmpiricalUniverse,
    ("RespondentEvent", "1.0.0"): RespondentEvent,
    ("EmpiricalCoordinateFact", "1.0.0"): EmpiricalCoordinateFact,
    ("RoutingEligibilityFact", "1.0.0"): RoutingEligibilityFact,
    ("WeightMeasureFact", "1.0.0"): WeightMeasureFact,
    ("AuthoritySnapshot", "1.0.0"): AuthoritySnapshot,
    ("SourceUniverseRelation", "1.0.0"): SourceUniverseRelation,
    ("EmpiricalPredicate", "1.0.0"): EmpiricalPredicate,
    ("EmpiricalQuerySpec", "1.0.0"): EmpiricalQuerySpec,
    ("EmpiricalFact", "1.0.0"): EmpiricalFact,
    ("DiscoveryAuthority", "1.0.0"): DiscoveryAuthority,
    ("DiscoveryResultReceipt", "1.0.0"): DiscoveryResultReceipt,
    ("StructuralEmpiricalAdmission", "1.0.0"): StructuralEmpiricalAdmission,
    ("ReplayReceipt", "1.0.0"): ReplayReceipt,
}

_SERIALIZED_PUBLIC_KEYS = frozenset({
    "schema_id",
    "schema_version",
    "typed_state",
    "authority_snapshot_refs",
    "dependency_refs",
    "producer_replay_locator_or_reference_root",
    "semantic_fields",
    "object_id",
    "content_hash",
})


def materialize_public_object(document: Mapping[str, Any]) -> CanonicalSemanticObject:
    """Re-materialize one exact PRE553 public object from its full canonical preimage.

    This is deserialization, not semantic construction.  The existing PRE553
    constructor recomputes the semantic projection and rejects any supplied
    object_id/content_hash that does not match byte-for-byte canonical meaning.
    No aliases, version elision, inferred fields, or hash inversion exist.
    """
    if not isinstance(document, Mapping):
        raise CarrierExecutionBindingError("canonical object preimage must be a mapping")
    if frozenset(document) != _SERIALIZED_PUBLIC_KEYS:
        missing = sorted(_SERIALIZED_PUBLIC_KEYS - frozenset(document))
        extra = sorted(frozenset(document) - _SERIALIZED_PUBLIC_KEYS)
        raise CarrierExecutionBindingError(
            f"canonical object preimage shape mismatch: missing={missing!r} extra={extra!r}"
        )
    schema_id = document.get("schema_id")
    schema_version = document.get("schema_version")
    cls = _PUBLIC_CLASS_BY_SCHEMA.get((schema_id, schema_version))
    if cls is None:
        raise CarrierExecutionBindingError(
            f"unsupported exact PRE553 public schema {schema_id!r}@{schema_version!r}"
        )
    fields = document.get("semantic_fields")
    if not isinstance(fields, Mapping):
        raise CarrierExecutionBindingError("canonical object semantic_fields must be a mapping")
    try:
        obj = cls(
            schema_id=schema_id,
            schema_version=schema_version,
            typed_state=document.get("typed_state"),
            authority_snapshot_refs=document.get("authority_snapshot_refs", ()),
            dependency_refs=document.get("dependency_refs", ()),
            producer_replay_locator_or_reference_root=document.get(
                "producer_replay_locator_or_reference_root"
            ),
            object_id=document.get("object_id"),
            content_hash=document.get("content_hash"),
            **dict(fields),
        )
    except (TypeError, ValueError, Pre553IntegrityError) as exc:
        raise CarrierExecutionBindingError(
            f"canonical object preimage failed exact materialization: {exc}"
        ) from exc
    return obj


def _canonical_objects(
    objects: Iterable[CanonicalSemanticObject],
    expected_type: type[CanonicalSemanticObject],
    label: str,
) -> tuple[CanonicalSemanticObject, ...]:
    by_key: dict[str, CanonicalSemanticObject] = {}
    for obj in objects:
        if not isinstance(obj, expected_type):
            raise CarrierExecutionBindingError(f"{label} contains wrong public object type")
        if semantic_hash(obj.semantic_projection()) != obj.content_hash:
            raise CarrierExecutionBindingError(f"{label} contains identity-drifted object")
        if obj.ref.key in by_key:
            raise CarrierExecutionBindingError(f"{label} contains duplicate exact ref")
        by_key[obj.ref.key] = obj
    return tuple(by_key[key] for key in sorted(by_key))


def bind_governed_c11_projection(
    projection_fields: Mapping[str, Any],
) -> GovernedC11Projection:
    """Bind one exact governed projection from already-authorized inputs.

    Every GovernedC11Projection field, including fields with constructor
    defaults, must be supplied explicitly. This function performs no source-
    family lookup, label interpretation, value inspection, or defaulting.
    """
    if not isinstance(projection_fields, Mapping):
        raise CarrierExecutionBindingError("projection_fields must be an exact mapping")
    required = tuple(field.name for field in dataclass_fields(GovernedC11Projection))
    supplied = tuple(projection_fields.keys())
    if set(supplied) != set(required) or len(supplied) != len(required):
        missing = sorted(set(required) - set(supplied))
        extra = sorted(set(supplied) - set(required))
        raise CarrierExecutionBindingError(
            f"projection binding must be complete and exact: missing={missing!r} extra={extra!r}"
        )
    try:
        return GovernedC11Projection(**{name: projection_fields[name] for name in required})
    except Exception as exc:
        raise CarrierExecutionBindingError(
            f"governed projection binding rejected by existing contract: {exc}"
        ) from exc


def governed_projection_binding_receipt(
    projection: GovernedC11Projection,
) -> Mapping[str, Any]:
    if not isinstance(projection, GovernedC11Projection):
        raise CarrierExecutionBindingError("GovernedC11Projection required")
    material = {
        "schema": "PRE553_GOVERNED_C11_PROJECTION_BINDING_RECEIPT@1.0.0",
        "contract": CARRIER_EXECUTION_CONTRACT_ID,
        "projection_identity_ref": projection.projection_identity_ref.as_dict(),
        "projection_cache_identity": projection.cache_identity,
        "source_sha256": projection.expected_source_sha256,
        "source_family_id": projection.source_family_id,
        "study_product_id": projection.study_product_id,
        "release_id": projection.release_id,
        "instrument_release_id": projection.instrument_release_id,
        "universe_count": len(projection.universes),
        "respondent_count": len(projection.respondents),
        "row_binding_count": len(projection.row_bindings),
        "question_binding_count": len(projection.questions),
        "response_slot_count": len(projection.response_slots),
        "coordinate_slot_count": len(projection.coordinate_slots),
        "weight_slot_count": len(projection.weight_slots),
        "routing_fact_count": len(projection.routing),
        "authority_snapshot_count": len(projection.authority_snapshots),
        "slot_owner_set_count": len(projection.slot_owner_sets),
        "semantic_inference_performed": False,
    }
    return {**material, "binding_identity": semantic_hash(material)}


@dataclass(frozen=True)
class RepositoryBuilderBinding:
    """Candidate-neutral composition of an exact repository builder and runner."""

    executor: "CarrierNeutralResearchExecutor"
    builder_identity: Mapping[str, Any]
    release_ref: ExactRef

    def receipt(self) -> Mapping[str, Any]:
        material = {
            "schema": "PRE553_REPOSITORY_BUILDER_EXECUTION_BINDING@1.0.0",
            "contract": CARRIER_EXECUTION_CONTRACT_ID,
            "builder_identity": canonicalize(self.builder_identity),
            "release_ref": self.release_ref.as_dict(),
            "executor_binding": self.executor.binding_receipt(),
            "candidate_semantic_branching": False,
        }
        return {**material, "binding_identity": semantic_hash(material)}


def bind_repository_builder(
    *,
    repository_builder: Callable[..., Any],
    builder_kwargs: Mapping[str, Any],
    builder_identity: Mapping[str, Any],
    runtime_catalog: "RuntimeObjectCatalog",
) -> RepositoryBuilderBinding:
    """Run accepted physical/C11 owner code and attach the common I03/I05 runner."""
    if not callable(repository_builder):
        raise CarrierExecutionBindingError("repository_builder must be callable")
    if not isinstance(builder_kwargs, Mapping) or not isinstance(builder_identity, Mapping):
        raise CarrierExecutionBindingError("builder kwargs/identity must be mappings")
    built = repository_builder(**dict(builder_kwargs))
    if not isinstance(built, tuple) or len(built) < 2:
        raise CarrierExecutionBindingError(
            "repository builder must return (C11Repository, release, ...)"
        )
    repository, release = built[0], built[1]
    if not isinstance(repository, C11Repository):
        raise CarrierExecutionBindingError("repository builder returned non-C11 repository")
    release_ref = getattr(release, "release_ref", None)
    if not isinstance(release_ref, ExactRef):
        raise CarrierExecutionBindingError("repository builder release lacks exact release_ref")
    try:
        repository.resolve_release_exact(release_ref)
    except KeyError as exc:
        raise CarrierExecutionBindingError(
            "repository builder returned release absent from returned repository"
        ) from exc
    executor = CarrierNeutralResearchExecutor(
        repository=repository,
        release_refs=(release_ref,),
        runtime_catalog=runtime_catalog,
    )
    return RepositoryBuilderBinding(
        executor=executor,
        builder_identity=canonicalize(builder_identity),
        release_ref=release_ref,
    )

@dataclass(frozen=True)
class RuntimeObjectCatalog:
    """Exact, content-addressed PRE553 execution catalog.

    The catalog contains object preimages, not merely refs.  AuthorityRegistry
    remains the sole authority resolver and therefore preserves its exact-only,
    fail-closed law.
    """

    authorities: tuple[AuthoritySnapshot, ...]
    predicates: tuple[EmpiricalPredicate, ...]
    queries: tuple[EmpiricalQuerySpec, ...]
    discovery_authorities: tuple[DiscoveryAuthority, ...]

    def __post_init__(self) -> None:
        authorities = _canonical_objects(
            self.authorities, AuthoritySnapshot, "authorities"
        )
        predicates = _canonical_objects(self.predicates, EmpiricalPredicate, "predicates")
        queries = _canonical_objects(self.queries, EmpiricalQuerySpec, "queries")
        discoveries = _canonical_objects(
            self.discovery_authorities, DiscoveryAuthority, "discovery_authorities"
        )
        object.__setattr__(self, "authorities", authorities)
        object.__setattr__(self, "predicates", predicates)
        object.__setattr__(self, "queries", queries)
        object.__setattr__(self, "discovery_authorities", discoveries)

        registry = AuthorityRegistry(authorities)
        for obj in (*predicates, *queries, *discoveries):
            validate_object_authority_closure(obj, registry)

    @classmethod
    def from_documents(
        cls,
        *,
        authority_documents: Iterable[Mapping[str, Any]],
        predicate_documents: Iterable[Mapping[str, Any]],
        query_documents: Iterable[Mapping[str, Any]],
        discovery_authority_documents: Iterable[Mapping[str, Any]] = (),
    ) -> "RuntimeObjectCatalog":
        authorities = tuple(materialize_public_object(x) for x in authority_documents)
        predicates = tuple(materialize_public_object(x) for x in predicate_documents)
        queries = tuple(materialize_public_object(x) for x in query_documents)
        discoveries = tuple(
            materialize_public_object(x) for x in discovery_authority_documents
        )
        expected = (
            ("authority_documents", authorities, AuthoritySnapshot),
            ("predicate_documents", predicates, EmpiricalPredicate),
            ("query_documents", queries, EmpiricalQuerySpec),
            ("discovery_authority_documents", discoveries, DiscoveryAuthority),
        )
        for label, objects, expected_type in expected:
            if any(not isinstance(obj, expected_type) for obj in objects):
                raise CarrierExecutionBindingError(
                    f"{label} contains a canonical object of the wrong exact family"
                )
        return cls(
            authorities=authorities,
            predicates=predicates,
            queries=queries,
            discovery_authorities=discoveries,
        )

    @property
    def authority_registry(self) -> AuthorityRegistry:
        return AuthorityRegistry(self.authorities)

    @property
    def predicate_refs(self) -> tuple[ExactRef, ...]:
        return tuple(x.ref for x in self.predicates)

    @property
    def query_refs(self) -> tuple[ExactRef, ...]:
        return tuple(x.ref for x in self.queries)

    @property
    def discovery_authority_refs(self) -> tuple[ExactRef, ...]:
        return tuple(x.ref for x in self.discovery_authorities)

    def _resolve(self, ref: ExactRef | Mapping[str, Any], objects, label: str):
        exact = exact_ref(ref, label)
        matches = [obj for obj in objects if obj.ref == exact]
        if len(matches) != 1:
            raise CarrierExecutionBindingError(
                f"{label} exact preimage unavailable; no latest/default/fuzzy/hash-inversion fallback"
            )
        return matches[0]

    def resolve_predicate_exact(
        self, ref: ExactRef | Mapping[str, Any]
    ) -> EmpiricalPredicate:
        return self._resolve(ref, self.predicates, "predicate_ref")

    def resolve_query_exact(
        self, ref: ExactRef | Mapping[str, Any]
    ) -> EmpiricalQuerySpec:
        return self._resolve(ref, self.queries, "query_ref")

    def resolve_discovery_authority_exact(
        self, ref: ExactRef | Mapping[str, Any]
    ) -> DiscoveryAuthority:
        return self._resolve(ref, self.discovery_authorities, "discovery_authority_ref")

    def receipt(self) -> Mapping[str, Any]:
        material = {
            "contract": CARRIER_EXECUTION_CONTRACT_ID,
            "authorities": [x.ref.as_dict() for x in self.authorities],
            "predicates": [x.ref.as_dict() for x in self.predicates],
            "queries": [x.ref.as_dict() for x in self.queries],
            "discovery_authorities": [
                x.ref.as_dict() for x in self.discovery_authorities
            ],
        }
        return {**material, "catalog_identity": semantic_hash(material)}


@dataclass(frozen=True)
class CarrierNeutralResearchExecutor:
    """One I03/I05 executor above the candidate-specific physical layer."""

    repository: C11Repository
    release_refs: tuple[ExactRef, ...]
    runtime_catalog: RuntimeObjectCatalog

    def __post_init__(self) -> None:
        if not isinstance(self.repository, C11Repository):
            raise CarrierExecutionBindingError("repository must be an exact C11Repository")
        refs = tuple(
            sorted(
                {exact_ref(ref, "release_ref") for ref in self.release_refs},
                key=lambda ref: ref.key,
            )
        )
        if not refs:
            raise CarrierExecutionBindingError("one or more exact C11 releases are required")
        for ref in refs:
            try:
                self.repository.resolve_release_exact(ref)
            except KeyError as exc:
                raise CarrierExecutionBindingError(
                    "bound C11 release unavailable; no fallback permitted"
                ) from exc
        object.__setattr__(self, "release_refs", refs)

    def execute_i03(
        self,
        *,
        query_ref: ExactRef | Mapping[str, Any],
        predicate_ref: ExactRef | Mapping[str, Any],
    ) -> QueryExecutionResult:
        query = self.runtime_catalog.resolve_query_exact(query_ref)
        predicate = self.runtime_catalog.resolve_predicate_exact(predicate_ref)
        condition_ref = exact_ref(query.condition_predicate_ref, "query.condition_predicate_ref")
        if condition_ref != predicate.ref:
            raise CarrierExecutionBindingError(
                "supplied predicate_ref is not the exact query condition predicate"
            )
        return execute_empirical_query(
            repository=self.repository,
            query=query,
            predicate=predicate,
            authority_registry=self.runtime_catalog.authority_registry,
            release_refs=self.release_refs,
        )

    def execute_i05(
        self,
        *,
        discovery_authority_ref: ExactRef | Mapping[str, Any],
    ) -> ExactBoundedDiscoveryResult:
        authority = self.runtime_catalog.resolve_discovery_authority_exact(
            discovery_authority_ref
        )
        return execute_exact_bounded_discovery(
            repository=self.repository,
            discovery_authority=authority,
            authority_registry=self.runtime_catalog.authority_registry,
            release_refs=self.release_refs,
            predicate_catalog=self.runtime_catalog.predicates,
            query_template_catalog=self.runtime_catalog.queries,
        )

    def binding_receipt(self) -> Mapping[str, Any]:
        material = {
            "schema": "PRE553_CARRIER_NEUTRAL_EXECUTION_BINDING_RECEIPT@1.0.0",
            "contract": CARRIER_EXECUTION_CONTRACT_ID,
            "i03_contract": QUERY_EXECUTION_CONTRACT_ID,
            "i05_contract": I05_CONTRACT_ID,
            "repository_snapshot_identity": self.repository.snapshot_identity(),
            "repository_snapshot_hash": semantic_hash(self.repository.snapshot_identity()),
            "release_refs": [x.as_dict() for x in self.release_refs],
            "runtime_catalog": self.runtime_catalog.receipt(),
        }
        return {**material, "binding_identity": semantic_hash(material)}


def learned_empirical_execution_receipt(
    result: ExactBoundedDiscoveryResult,
) -> Mapping[str, Any]:
    """Return a carrier-neutral learned-empirical execution envelope.

    This does not perform structural admission and does not encode a source-
    specific research interpretation.  Workload-specific products (for example
    ASTRA-D04-R2's P0-P4 packaging) remain research-layer consumers of these
    exact I05 receipts.
    """
    if not isinstance(result, ExactBoundedDiscoveryResult):
        raise CarrierExecutionBindingError("expected exact I05 execution result")
    material = {
        "schema": "PRE553_LEARNED_EMPIRICAL_EXECUTION_RECEIPT@1.0.0",
        "claim_kind": "LEARNED_EMPIRICAL_EXECUTION_ONLY",
        "i05_contract": result.contract_id,
        "discovery_authority_ref": result.discovery_authority_ref.as_dict(),
        "candidate_grammar_ref": result.candidate_grammar_ref.as_dict(),
        "evaluated_frontier_ref": result.evaluated_frontier_ref.as_dict(),
        "coverage_claim": result.coverage_claim,
        "candidate_count": result.candidate_count,
        "covered_candidate_count": result.covered_candidate_count,
        "discovery_receipt_refs": [x.ref.as_dict() for x in result.receipts],
        "empirical_fact_refs": [x.as_dict() for x in result.empirical_fact_refs],
        "valid_empty": result.valid_empty,
        "replay_ref": result.replay_ref.as_dict(),
        "structural_truth_effect": False,
        "causal_truth_effect": False,
        "actor_v3_effect": False,
    }
    return {**material, "execution_identity": semantic_hash(material)}


__all__ = [
    "CARRIER_EXECUTION_CONTRACT_ID",
    "CarrierExecutionBindingError",
    "RuntimeObjectCatalog",
    "CarrierNeutralResearchExecutor",
    "RepositoryBuilderBinding",
    "materialize_public_object",
    "bind_governed_c11_projection",
    "governed_projection_binding_receipt",
    "bind_repository_builder",
    "learned_empirical_execution_receipt",
]
