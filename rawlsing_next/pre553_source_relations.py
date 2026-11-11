"""PRE553 Wave-03 I07 source-universe relation resolution and composition guards.

This module implements the accepted P07 source-plurality law without changing
I01 public object identity, I02 C11 repository semantics, or I03 empirical-query
semantics.  Source universes are distinct by default.  A relation is usable
only when one exact SourceUniverseRelation receipt and its exact immutable
AuthoritySnapshot positively authorize that exact relation kind, source set,
operation scope, target use, effective scope and authority operation.

No relation kind implies another.  Provenance and harmonization/alias material
are descriptive only and never grant equivalence, linkage, nonduplication,
pooling, estimand composition or backfill.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityError,
    require_positive_authority,
    validate_authority_snapshot,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    P07_RELATION_DECISIONS,
    P07_RELATION_KINDS,
    Pre553IntegrityError,
    Pre553SemanticCollapseError,
    SourceUniverseRelation,
    authority_ref,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)

I07_CONTRACT_ID = "PRE553_I07_SOURCE_PLURALITY_COMPOSITION@1.0.0"
DEFAULT_RELATION_STATE = "DISTINCT_BY_DEFAULT"
I03_COMPOSITE_TARGET_USE = "I03_AUTHORIZED_COMPOSITE"

NONAUTHORIZING_RELATION_KINDS = frozenset({"PROVENANCE_ORIGIN", "HARMONIZATION_ALIAS"})
COMPOSING_RELATION_KINDS = frozenset({
    "SAMPLE_POOLING", "ESTIMAND_COMPOSITION", "BACKFILL",
})
FORBIDDEN_BACKFILL_TARGET_STATES = frozenset({
    "DECLARED_NONE", "SOURCE_NOT_APPLICABLE", "TEMPORAL_NONCOMPARABLE",
    "OBSERVED_ZERO", "ZERO_SUPPORT", "NONCOMPARABLE", "NOT_APPLICABLE",
})

RELATION_AUTHORITY_KIND: Mapping[str, str | None] = MappingProxyType({
    "SOURCE_SEMANTIC_EQUIVALENCE": "SOURCE_EQUIVALENCE",
    "RESPONDENT_LINKAGE": "SOURCE_RESPONDENT_LINKAGE",
    "OVERLAP_NON_DUPLICATION": "SOURCE_UNIVERSE_RELATION",
    "SAMPLE_POOLING": "SOURCE_COMPOSITION_POOLING",
    "ESTIMAND_COMPOSITION": "SOURCE_COMPOSITION_POOLING",
    "BACKFILL": "SOURCE_BACKFILL",
    "PROVENANCE_ORIGIN": None,
    "HARMONIZATION_ALIAS": None,
})

RELATION_REQUIRED_MATERIAL_KEYS: Mapping[str, frozenset[str]] = MappingProxyType({
    "SOURCE_SEMANTIC_EQUIVALENCE": frozenset({
        "left_semantic_ref", "right_semantic_ref", "equivalence_scope",
        "transformation_authority_refs",
    }),
    "RESPONDENT_LINKAGE": frozenset({
        "scoped_respondent_or_event_keys", "linkage_cardinality", "linkage_basis",
        "confidence_or_certainty_state_if_authorized",
    }),
    "OVERLAP_NON_DUPLICATION": frozenset({
        "sampling_unit_definition", "covered_risk_set_or_sample_scope", "overlap_state",
        "deduplication_or_partition_rule_ref_or_NONE",
    }),
    "SAMPLE_POOLING": frozenset({
        "target_query_or_estimand_ref", "risk_set_and_denominator_authority_refs",
        "sample_design_compatibility_ref", "semantic_equivalence_refs",
        "overlap_nonduplication_ref", "weight_measure_authority_refs",
        "typed_missingness_applicability_rule_ref", "composition_method_id_version_hash",
    }),
    "ESTIMAND_COMPOSITION": frozenset({
        "component_estimand_refs", "target_estimand_ref", "measure_and_scale_compatibility_refs",
        "semantic_equivalence_refs", "overlap_treatment_ref", "weight_or_mixture_rule_ref",
        "uncertainty_propagation_rule_ref_or_typed_unquantified_state",
    }),
    "BACKFILL": frozenset({
        "target_source_universe_ref", "donor_source_universe_ref", "target_semantic_ref",
        "donor_semantic_ref", "eligible_target_missingness_states", "semantic_equivalence_ref",
        "sample_estimand_design_compatibility_refs", "overlap_nonduplication_ref",
        "weight_measure_rule_refs",
    }),
    "PROVENANCE_ORIGIN": frozenset({"provenance_refs"}),
    "HARMONIZATION_ALIAS": frozenset({"alias_refs"}),
})

RELATION_DECISION_MATRIX: Mapping[str, Mapping[str, Any]] = MappingProxyType({
    "SOURCE_SEMANTIC_EQUIVALENCE": MappingProxyType({
        "default": DEFAULT_RELATION_STATE,
        "positive_authority_kind": "SOURCE_EQUIVALENCE",
        "does_not_grant": (
            "RESPONDENT_LINKAGE", "OVERLAP_NON_DUPLICATION", "SAMPLE_POOLING",
            "ESTIMAND_COMPOSITION", "BACKFILL",
        ),
    }),
    "RESPONDENT_LINKAGE": MappingProxyType({
        "default": DEFAULT_RELATION_STATE,
        "positive_authority_kind": "SOURCE_RESPONDENT_LINKAGE",
        "does_not_grant": (
            "SOURCE_SEMANTIC_EQUIVALENCE", "OVERLAP_NON_DUPLICATION", "SAMPLE_POOLING",
            "ESTIMAND_COMPOSITION", "BACKFILL",
        ),
    }),
    "OVERLAP_NON_DUPLICATION": MappingProxyType({
        "default": "UNKNOWN_OVERLAP",
        "positive_authority_kind": "SOURCE_UNIVERSE_RELATION",
        "does_not_grant": (
            "SOURCE_SEMANTIC_EQUIVALENCE", "RESPONDENT_LINKAGE", "SAMPLE_POOLING",
            "ESTIMAND_COMPOSITION", "BACKFILL",
        ),
    }),
    "SAMPLE_POOLING": MappingProxyType({
        "default": DEFAULT_RELATION_STATE,
        "positive_authority_kind": "SOURCE_COMPOSITION_POOLING",
        "does_not_grant": ("RESPONDENT_LINKAGE", "ESTIMAND_COMPOSITION", "BACKFILL"),
    }),
    "ESTIMAND_COMPOSITION": MappingProxyType({
        "default": DEFAULT_RELATION_STATE,
        "positive_authority_kind": "SOURCE_COMPOSITION_POOLING",
        "does_not_grant": ("RESPONDENT_LINKAGE", "SAMPLE_POOLING", "BACKFILL"),
    }),
    "BACKFILL": MappingProxyType({
        "default": DEFAULT_RELATION_STATE,
        "positive_authority_kind": "SOURCE_BACKFILL",
        "does_not_grant": ("RESPONDENT_LINKAGE", "SAMPLE_POOLING", "ESTIMAND_COMPOSITION"),
    }),
    "PROVENANCE_ORIGIN": MappingProxyType({
        "default": "PROVENANCE_ONLY",
        "positive_authority_kind": None,
        "does_not_grant": tuple(sorted(P07_RELATION_KINDS - {"PROVENANCE_ORIGIN"})),
    }),
    "HARMONIZATION_ALIAS": MappingProxyType({
        "default": "ALIAS_ONLY",
        "positive_authority_kind": None,
        "does_not_grant": tuple(sorted(P07_RELATION_KINDS - {"HARMONIZATION_ALIAS"})),
    }),
})


class SourceRelationError(Pre553IntegrityError):
    """Base I07 exact source-relation error."""


class SourceRelationIntegrityError(SourceRelationError):
    """A relation receipt has invalid identity or exact binding material."""


class SourceRelationAuthorizationError(SourceRelationError):
    """An exact positive relation required for an operation is not established."""

    def __init__(self, state: str, message: str) -> None:
        super().__init__(message)
        self.state = state


@dataclass(frozen=True)
class RelationDecision:
    relation_kind: str
    source_universe_refs: tuple[ExactRef, ...]
    operation_scope: Any
    target_use: str
    effective_scope: Any
    directionality_or_symmetric: Any
    state: str
    relation_ref: ExactRef | None
    authority_ref: AuthorityRef | None
    authority_operation: str | None
    reason: str
    replay_identity: str

    @property
    def authorized(self) -> bool:
        return self.state == "AUTHORIZED" and self.relation_ref is not None


@dataclass(frozen=True)
class OperationGuardReceipt:
    operation_kind: str
    source_universe_refs: tuple[ExactRef, ...]
    relation_refs: tuple[ExactRef, ...]
    authority_refs: tuple[AuthorityRef, ...]
    operation_scope: Any
    target_use: str
    effective_scope: Any
    receipt_hash: str


@dataclass(frozen=True)
class I03CompositeGuardReceipt:
    query_ref: ExactRef
    source_universe_refs: tuple[ExactRef, ...]
    semantic_equivalence_ref: ExactRef
    overlap_nonduplication_ref: ExactRef
    pooling_ref: ExactRef
    estimand_composition_ref: ExactRef
    i03_authority_refs: tuple[AuthorityRef, ...]
    guard_hash: str


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SourceRelationIntegrityError(f"{name} must be a non-empty string")
    out = value.strip()
    if out.lower() in {"latest", "default", "fuzzy", "nearest", "*"}:
        raise SourceRelationIntegrityError(f"{name} may not use mutable/fuzzy selection")
    return out


def _canonical_refs(values: Iterable[ExactRef | Mapping[str, Any]], name: str) -> tuple[ExactRef, ...]:
    refs = tuple(sorted({exact_ref(value, name) for value in values}, key=lambda ref: ref.key))
    if len(refs) < 2:
        raise SourceRelationIntegrityError("source relation requires at least two exact source universes")
    return refs


def _material_equal(left: Any, right: Any) -> bool:
    return canonical_json(left) == canonical_json(right)


def _authority_from_relation(relation: SourceUniverseRelation) -> AuthorityRef:
    try:
        ref = authority_ref(relation.relation_authority_ref, "relation_authority_ref")
    except Pre553IntegrityError as exc:
        raise SourceRelationIntegrityError(str(exc)) from exc
    if ref not in relation.authority_snapshot_refs:
        raise SourceRelationIntegrityError(
            "relation_authority_ref must be included in exact public authority_snapshot_refs closure"
        )
    return ref


def _operation_material(relation: SourceUniverseRelation) -> Mapping[str, Any]:
    material = relation.semantic_fields.get("operation_authority_material")
    if not isinstance(material, Mapping):
        raise SourceRelationIntegrityError(
            "I07 positive relation requires exact operation_authority_material mapping"
        )
    required = RELATION_REQUIRED_MATERIAL_KEYS[relation.relation_kind]
    missing = sorted(required - set(material))
    if missing:
        raise SourceRelationIntegrityError(
            f"{relation.relation_kind} operation_authority_material missing {missing!r}"
        )
    for key in required:
        value = material[key]
        if value is None and not key.endswith("_or_NONE"):
            raise SourceRelationIntegrityError(
                f"{relation.relation_kind}.{key} may not be omitted for positive authority"
            )
    return material


def _relation_replay_identity(
    *,
    relation_kind: str,
    source_universe_refs: Sequence[ExactRef],
    operation_scope: Any,
    target_use: str,
    effective_scope: Any,
    directionality_or_symmetric: Any,
    authority_ref_value: AuthorityRef,
    authority_operation: str,
    operation_authority_material: Mapping[str, Any],
    decision: str,
) -> str:
    return semantic_hash({
        "contract": I07_CONTRACT_ID,
        "relation_kind": relation_kind,
        "source_universe_refs": [ref.as_dict() for ref in source_universe_refs],
        "operation_scope": canonicalize(operation_scope),
        "target_use": target_use,
        "effective_scope": canonicalize(effective_scope),
        "directionality_or_symmetric": canonicalize(directionality_or_symmetric),
        "authority_ref": authority_ref_value.as_dict(),
        "authority_operation": authority_operation,
        "operation_authority_material": canonicalize(operation_authority_material),
        "decision": decision,
    })


def _positive_typed_state(decision: str) -> str:
    if decision == "AUTHORIZED":
        return "RELATION_AUTHORIZED_FOR_EXACT_KIND_AND_SCOPE"
    if decision == "DENIED":
        return "RELATION_DENIED"
    if decision == "NOT_APPLICABLE":
        return "RELATION_OUT_OF_SCOPE"
    if decision in {"UNKNOWN_AUTHORITY", "CONFLICTING_AUTHORITY", "EXPIRED_OR_STALE"}:
        return "UNKNOWN_SOURCE_RELATION"
    raise SourceRelationIntegrityError(f"unsupported P07 decision {decision!r}")


def make_source_universe_relation(
    *,
    relation_kind: str,
    source_universe_refs: Iterable[ExactRef | Mapping[str, Any]],
    authority_snapshot: AuthoritySnapshot,
    authority_operation: str,
    operation_scope: Any,
    target_use: str,
    effective_scope: Any,
    directionality_or_symmetric: Any,
    operation_authority_material: Mapping[str, Any],
    producer_replay_locator_or_reference_root: ExactRef | Mapping[str, Any] | str,
    decision: str = "AUTHORIZED",
    overlap_or_nonduplication_evidence_refs: Iterable[ExactRef | Mapping[str, Any]] = (),
    composition_estimand_refs: Iterable[ExactRef | Mapping[str, Any]] = (),
    deduplication_rule_ref_if_any: ExactRef | Mapping[str, Any] | None = None,
    negative_limit_refs: Iterable[ExactRef | Mapping[str, Any]] = (),
    extra_dependency_refs: Iterable[ExactRef | Mapping[str, Any]] = (),
) -> SourceUniverseRelation:
    """Create one exact I07-shaped public relation receipt.

    This factory creates no inferred relation.  The caller must provide the exact
    authority and all operation-specific material.  Positive provenance/alias
    receipts are constitutionally forbidden.
    """
    if relation_kind not in P07_RELATION_KINDS:
        raise SourceRelationIntegrityError("unknown P07 relation kind")
    if decision not in P07_RELATION_DECISIONS:
        raise SourceRelationIntegrityError("unknown P07 relation decision")
    if decision == "AUTHORIZED" and relation_kind in NONAUTHORIZING_RELATION_KINDS:
        raise Pre553SemanticCollapseError(
            f"{relation_kind} is descriptive only and cannot authorize an operation"
        )
    snapshot = validate_authority_snapshot(authority_snapshot)
    sources = _canonical_refs(source_universe_refs, "source_universe_ref")
    op = _text(authority_operation, "authority_operation")
    use = _text(target_use, "target_use")
    material = canonicalize(operation_authority_material)
    if not isinstance(material, Mapping):
        raise SourceRelationIntegrityError("operation_authority_material must be an exact mapping")
    missing = sorted(RELATION_REQUIRED_MATERIAL_KEYS[relation_kind] - set(material))
    if decision == "AUTHORIZED" and missing:
        raise SourceRelationIntegrityError(
            f"{relation_kind} operation_authority_material missing {missing!r}"
        )
    authority = snapshot.authority_ref
    if decision == "AUTHORIZED":
        expected_kind = RELATION_AUTHORITY_KIND[relation_kind]
        if expected_kind is None:
            raise Pre553SemanticCollapseError(f"{relation_kind} cannot authorize positive semantics")
        for source in sources:
            require_positive_authority(
                snapshot,
                authority_kind=expected_kind,
                operation=op,
                object_family="SourceUniverseRelation",
                source_universe_ref=source.as_dict(),
                target_use_ref=use,
                predicate_or_risk_set_ref=canonicalize(operation_scope),
            )
    replay_identity = _relation_replay_identity(
        relation_kind=relation_kind,
        source_universe_refs=sources,
        operation_scope=operation_scope,
        target_use=use,
        effective_scope=effective_scope,
        directionality_or_symmetric=directionality_or_symmetric,
        authority_ref_value=authority,
        authority_operation=op,
        operation_authority_material=material,
        decision=decision,
    )
    relation_id = f"P07REL:{replay_identity}"
    overlap_refs = tuple(exact_ref(x, "overlap_evidence_ref") for x in overlap_or_nonduplication_evidence_refs)
    estimand_refs = tuple(exact_ref(x, "composition_estimand_ref") for x in composition_estimand_refs)
    negative_refs = tuple(exact_ref(x, "negative_limit_ref") for x in negative_limit_refs)
    dependencies = tuple(sources) + tuple(exact_ref(x, "extra_dependency_ref") for x in extra_dependency_refs)
    dedup = None if deduplication_rule_ref_if_any is None else exact_ref(
        deduplication_rule_ref_if_any, "deduplication_rule_ref_if_any"
    )
    return SourceUniverseRelation(
        typed_state=_positive_typed_state(decision),
        authority_snapshot_refs=(authority,),
        dependency_refs=dependencies,
        producer_replay_locator_or_reference_root=producer_replay_locator_or_reference_root,
        relation_id=relation_id,
        relation_kind=relation_kind,
        source_universe_refs=sources,
        relation_authority_ref=authority,
        effective_scope=canonicalize(effective_scope),
        overlap_or_nonduplication_evidence_refs=overlap_refs,
        composition_estimand_refs=estimand_refs,
        deduplication_rule_ref_if_any=dedup,
        negative_limit_refs=negative_refs,
        decision=decision,
        operation_scope=canonicalize(operation_scope),
        target_use=use,
        directionality_or_symmetric=canonicalize(directionality_or_symmetric),
        authority_operation=op,
        operation_authority_material=material,
        replay_identity=replay_identity,
        i07_contract_id=I07_CONTRACT_ID,
    )


def _relation_key_material(
    *, relation_kind: str, source_universe_refs: Sequence[ExactRef], operation_scope: Any,
    target_use: str, effective_scope: Any, directionality_or_symmetric: Any,
) -> Mapping[str, Any]:
    return {
        "relation_kind": relation_kind,
        "source_universe_refs": [ref.as_dict() for ref in source_universe_refs],
        "operation_scope": canonicalize(operation_scope),
        "target_use": target_use,
        "effective_scope": canonicalize(effective_scope),
        "directionality_or_symmetric": canonicalize(directionality_or_symmetric),
    }


def _relation_key(**kwargs: Any) -> str:
    return semantic_hash(_relation_key_material(**kwargs))


class SourceRelationResolver:
    """Exact-key P07 relation resolver; absence always means distinct by default."""

    def __init__(
        self,
        *,
        relations: Iterable[SourceUniverseRelation],
        authority_registry: AuthorityRegistry,
    ) -> None:
        if not isinstance(authority_registry, AuthorityRegistry):
            raise SourceRelationIntegrityError("authority_registry must be exact I01 AuthorityRegistry")
        self._registry = authority_registry
        self._by_ref: dict[str, SourceUniverseRelation] = {}
        self._by_key: dict[str, list[SourceUniverseRelation]] = {}
        for relation in relations:
            self._validate_relation_object(relation)
            prior = self._by_ref.get(relation.ref.key)
            if prior is not None and prior != relation:
                raise SourceRelationIntegrityError("same exact relation ref has conflicting material")
            self._by_ref[relation.ref.key] = relation
            if self._has_i07_use_shape(relation):
                key = self._relation_object_key(relation)
                bucket = self._by_key.setdefault(key, [])
                if relation not in bucket:
                    bucket.append(relation)
        for bucket in self._by_key.values():
            bucket.sort(key=lambda relation: relation.ref.key)

    @classmethod
    def from_c11(
        cls,
        *,
        repository: C11Repository,
        relation_refs: Iterable[ExactRef | Mapping[str, Any]],
        authority_registry: AuthorityRegistry,
    ) -> "SourceRelationResolver":
        if not isinstance(repository, C11Repository):
            raise SourceRelationIntegrityError("repository must be accepted I02 C11Repository")
        relations: list[SourceUniverseRelation] = []
        for raw in relation_refs:
            ref = exact_ref(raw, "relation_ref")
            try:
                obj = repository.resolve_object_exact(ref)
            except KeyError as exc:
                raise SourceRelationIntegrityError(
                    "exact SourceUniverseRelation unavailable; no latest/default/fuzzy fallback"
                ) from exc
            if not isinstance(obj, SourceUniverseRelation):
                raise SourceRelationIntegrityError("exact relation ref resolves to a different object family")
            relations.append(obj)
        return cls(relations=relations, authority_registry=authority_registry)

    def _validate_relation_object(self, relation: SourceUniverseRelation) -> None:
        if not isinstance(relation, SourceUniverseRelation):
            raise SourceRelationIntegrityError("I07 resolver accepts SourceUniverseRelation@1.0.0 only")
        if semantic_hash(relation.semantic_projection()) != relation.content_hash:
            raise SourceRelationIntegrityError("SourceUniverseRelation semantic hash mismatch")
        if relation.relation_kind not in P07_RELATION_KINDS:
            raise SourceRelationIntegrityError("unknown relation kind")
        _canonical_refs(relation.source_universe_refs, "relation.source_universe_refs")
        ref = _authority_from_relation(relation)
        try:
            self._registry.resolve_exact(ref)
        except Pre553AuthorityError as exc:
            raise SourceRelationIntegrityError(
                "relation authority snapshot unavailable by exact ID/version/hash"
            ) from exc
        decision = relation.semantic_fields.get("decision")
        if decision is not None and decision not in P07_RELATION_DECISIONS:
            raise SourceRelationIntegrityError("relation decision is outside P07 state algebra")
        if decision == "AUTHORIZED":
            if relation.relation_kind in NONAUTHORIZING_RELATION_KINDS:
                raise Pre553SemanticCollapseError(
                    f"{relation.relation_kind} cannot become positive operation authority"
                )
            if relation.typed_state != "RELATION_AUTHORIZED_FOR_EXACT_KIND_AND_SCOPE":
                raise SourceRelationIntegrityError("AUTHORIZED relation must carry exact positive typed state")
            _operation_material(relation)
            self._validate_replay_identity(relation)

    @staticmethod
    def _has_i07_use_shape(relation: SourceUniverseRelation) -> bool:
        required = {
            "operation_scope", "target_use", "directionality_or_symmetric",
            "authority_operation", "operation_authority_material", "replay_identity",
        }
        return required <= set(relation.semantic_fields)

    @staticmethod
    def _relation_object_key(relation: SourceUniverseRelation) -> str:
        sources = _canonical_refs(relation.source_universe_refs, "relation.source_universe_refs")
        return _relation_key(
            relation_kind=relation.relation_kind,
            source_universe_refs=sources,
            operation_scope=relation.operation_scope,
            target_use=_text(relation.target_use, "relation.target_use"),
            effective_scope=relation.effective_scope,
            directionality_or_symmetric=relation.directionality_or_symmetric,
        )

    @staticmethod
    def _validate_replay_identity(relation: SourceUniverseRelation) -> None:
        authority = _authority_from_relation(relation)
        operation = _text(relation.authority_operation, "relation.authority_operation")
        material = _operation_material(relation)
        expected = _relation_replay_identity(
            relation_kind=relation.relation_kind,
            source_universe_refs=_canonical_refs(
                relation.source_universe_refs, "relation.source_universe_refs"
            ),
            operation_scope=relation.operation_scope,
            target_use=_text(relation.target_use, "relation.target_use"),
            effective_scope=relation.effective_scope,
            directionality_or_symmetric=relation.directionality_or_symmetric,
            authority_ref_value=authority,
            authority_operation=operation,
            operation_authority_material=material,
            decision=relation.semantic_fields.get("decision", "UNKNOWN_AUTHORITY"),
        )
        if relation.replay_identity != expected or relation.relation_id != f"P07REL:{expected}":
            raise SourceRelationIntegrityError("relation replay identity is stale or corrupt")

    def resolve_exact(self, ref: ExactRef | Mapping[str, Any]) -> SourceUniverseRelation:
        exact = exact_ref(ref, "relation_ref")
        relation = self._by_ref.get(exact.key)
        if relation is None:
            raise SourceRelationIntegrityError(
                "exact SourceUniverseRelation unavailable; no label/ID/latest/default inference"
            )
        return relation

    def _validate_positive(
        self,
        relation: SourceUniverseRelation,
        *,
        expected_authority_operation: str | None,
    ) -> tuple[AuthorityRef, str]:
        if relation.relation_kind in NONAUTHORIZING_RELATION_KINDS:
            raise SourceRelationAuthorizationError(
                DEFAULT_RELATION_STATE,
                f"{relation.relation_kind} is descriptive and has zero composition effect",
            )
        if relation.semantic_fields.get("decision") != "AUTHORIZED":
            raise SourceRelationAuthorizationError(
                str(relation.semantic_fields.get("decision", DEFAULT_RELATION_STATE)),
                "relation receipt is not a positive exact authority",
            )
        self._validate_replay_identity(relation)
        authority = _authority_from_relation(relation)
        operation = _text(relation.authority_operation, "relation.authority_operation")
        if expected_authority_operation is not None and operation != _text(
            expected_authority_operation, "expected_authority_operation"
        ):
            raise SourceRelationAuthorizationError(
                "OUT_OF_SCOPE", "exact relation authority operation does not match requested operation"
            )
        snapshot = self._registry.resolve_exact(authority).snapshot
        expected_kind = RELATION_AUTHORITY_KIND[relation.relation_kind]
        if expected_kind is None:
            raise SourceRelationAuthorizationError(
                DEFAULT_RELATION_STATE, "descriptive relation cannot authorize an operation"
            )
        sources = _canonical_refs(relation.source_universe_refs, "relation.source_universe_refs")
        try:
            for source in sources:
                require_positive_authority(
                    snapshot,
                    authority_kind=expected_kind,
                    operation=operation,
                    object_family="SourceUniverseRelation",
                    source_universe_ref=source.as_dict(),
                    target_use_ref=relation.target_use,
                    predicate_or_risk_set_ref=relation.operation_scope,
                )
        except Pre553AuthorityError as exc:
            raise SourceRelationAuthorizationError("UNKNOWN_AUTHORITY", str(exc)) from exc
        return authority, operation

    def decide(
        self,
        *,
        relation_kind: str,
        source_universe_refs: Iterable[ExactRef | Mapping[str, Any]],
        operation_scope: Any,
        target_use: str,
        effective_scope: Any,
        directionality_or_symmetric: Any = "SYMMETRIC",
        relation_ref: ExactRef | Mapping[str, Any] | None = None,
        expected_authority_operation: str | None = None,
    ) -> RelationDecision:
        if relation_kind not in P07_RELATION_KINDS:
            raise SourceRelationIntegrityError("unknown P07 relation kind")
        sources = _canonical_refs(source_universe_refs, "source_universe_ref")
        use = _text(target_use, "target_use")
        key = _relation_key(
            relation_kind=relation_kind,
            source_universe_refs=sources,
            operation_scope=operation_scope,
            target_use=use,
            effective_scope=effective_scope,
            directionality_or_symmetric=directionality_or_symmetric,
        )
        if relation_ref is None:
            candidates = tuple(self._by_key.get(key, ()))
        else:
            candidate = self.resolve_exact(relation_ref)
            candidates = (candidate,) if self._relation_object_key(candidate) == key else ()

        def result(
            state: str, reason: str, relation: SourceUniverseRelation | None = None,
            authority: AuthorityRef | None = None, operation: str | None = None,
        ) -> RelationDecision:
            replay = semantic_hash({
                "contract": I07_CONTRACT_ID,
                "request": _relation_key_material(
                    relation_kind=relation_kind, source_universe_refs=sources,
                    operation_scope=operation_scope, target_use=use,
                    effective_scope=effective_scope,
                    directionality_or_symmetric=directionality_or_symmetric,
                ),
                "state": state,
                "relation_ref": relation.ref.as_dict() if relation else None,
                "authority_ref": authority.as_dict() if authority else None,
                "authority_operation": operation,
            })
            return RelationDecision(
                relation_kind, sources, canonicalize(operation_scope), use,
                canonicalize(effective_scope), canonicalize(directionality_or_symmetric),
                state, relation.ref if relation else None, authority, operation, reason, replay,
            )

        if relation_kind in NONAUTHORIZING_RELATION_KINDS:
            return result(
                RELATION_DECISION_MATRIX[relation_kind]["default"],
                f"{relation_kind} is descriptive only and never grants adjacent relation semantics",
            )
        if not candidates:
            return result(DEFAULT_RELATION_STATE, "no exact positive relation receipt for this kind/scope/use")

        positives: list[tuple[SourceUniverseRelation, AuthorityRef, str]] = []
        negative_states: list[str] = []
        for relation in candidates:
            decision = str(relation.semantic_fields.get("decision", "UNKNOWN_AUTHORITY"))
            if decision == "AUTHORIZED":
                try:
                    authority, operation = self._validate_positive(
                        relation, expected_authority_operation=expected_authority_operation
                    )
                except SourceRelationAuthorizationError as exc:
                    negative_states.append(exc.state)
                else:
                    positives.append((relation, authority, operation))
            else:
                negative_states.append(decision)

        if len(positives) == 1 and not negative_states:
            relation, authority, operation = positives[0]
            return result("AUTHORIZED", "exact operation-specific relation authority established", relation, authority, operation)
        if len(positives) > 1 or (positives and negative_states):
            return result("CONFLICTING_AUTHORITY", "multiple or conflicting exact relation dispositions exist")
        precedence = (
            "CONFLICTING_AUTHORITY", "EXPIRED_OR_STALE", "DENIED", "NOT_APPLICABLE",
            "UNKNOWN_AUTHORITY", "OUT_OF_SCOPE",
        )
        for state in precedence:
            if state in negative_states:
                return result(state, "exact relation receipt is nonpositive or unavailable")
        return result(DEFAULT_RELATION_STATE, "no positive exact relation authority established")

    def require(self, **kwargs: Any) -> RelationDecision:
        decision = self.decide(**kwargs)
        if not decision.authorized:
            raise SourceRelationAuthorizationError(
                decision.state,
                f"{decision.relation_kind} required but decision is {decision.state}: {decision.reason}",
            )
        return decision


def _exact_relation_ref_in_material(material: Mapping[str, Any], key: str) -> ExactRef:
    if key not in material:
        raise SourceRelationIntegrityError(f"operation authority material missing {key}")
    return exact_ref(material[key], key)


def _exact_relation_ref_set_in_material(material: Mapping[str, Any], key: str) -> tuple[ExactRef, ...]:
    value = material.get(key)
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise SourceRelationIntegrityError(f"operation authority material {key} must be a sequence")
    return tuple(sorted({exact_ref(item, key) for item in value}, key=lambda ref: ref.key))


def _guard_receipt(
    *, operation_kind: str, decisions: Sequence[RelationDecision], operation_scope: Any,
    target_use: str, effective_scope: Any,
) -> OperationGuardReceipt:
    if not decisions or not all(decision.authorized for decision in decisions):
        raise SourceRelationAuthorizationError("UNKNOWN_AUTHORITY", "operation guard lacks positive relation closure")
    sources = decisions[0].source_universe_refs
    if any(decision.source_universe_refs != sources for decision in decisions):
        raise SourceRelationIntegrityError("operation guard relation source sets differ")
    relation_refs = tuple(sorted({decision.relation_ref for decision in decisions if decision.relation_ref}, key=lambda ref: ref.key))
    authority_refs = tuple(sorted({decision.authority_ref for decision in decisions if decision.authority_ref}, key=lambda ref: ref.key))
    receipt_hash = semantic_hash({
        "contract": I07_CONTRACT_ID,
        "operation_kind": operation_kind,
        "source_universe_refs": [ref.as_dict() for ref in sources],
        "relation_refs": [ref.as_dict() for ref in relation_refs],
        "authority_refs": [ref.as_dict() for ref in authority_refs],
        "operation_scope": canonicalize(operation_scope),
        "target_use": target_use,
        "effective_scope": canonicalize(effective_scope),
    })
    return OperationGuardReceipt(
        operation_kind, sources, relation_refs, authority_refs,
        canonicalize(operation_scope), target_use, canonicalize(effective_scope), receipt_hash,
    )


def guard_sample_pooling(
    *, resolver: SourceRelationResolver, source_universe_refs: Iterable[ExactRef | Mapping[str, Any]],
    operation_scope: Any, target_use: str, effective_scope: Any,
    semantic_equivalence_ref: ExactRef | Mapping[str, Any],
    overlap_nonduplication_ref: ExactRef | Mapping[str, Any],
    pooling_ref: ExactRef | Mapping[str, Any],
    pooling_authority_operation: str,
    semantic_equivalence_authority_operation: str = "I07_SOURCE_SEMANTIC_EQUIVALENCE",
    overlap_authority_operation: str = "I07_OVERLAP_NON_DUPLICATION",
) -> OperationGuardReceipt:
    sources = _canonical_refs(source_universe_refs, "source_universe_ref")
    common = dict(
        source_universe_refs=sources, operation_scope=operation_scope, target_use=target_use,
        effective_scope=effective_scope, directionality_or_symmetric="SYMMETRIC",
    )
    sem = resolver.require(
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE", relation_ref=semantic_equivalence_ref,
        expected_authority_operation=semantic_equivalence_authority_operation, **common,
    )
    overlap = resolver.require(
        relation_kind="OVERLAP_NON_DUPLICATION", relation_ref=overlap_nonduplication_ref,
        expected_authority_operation=overlap_authority_operation, **common,
    )
    pool = resolver.require(
        relation_kind="SAMPLE_POOLING", relation_ref=pooling_ref,
        expected_authority_operation=pooling_authority_operation, **common,
    )
    pool_material = _operation_material(resolver.resolve_exact(pool.relation_ref))
    semantic_refs = _exact_relation_ref_set_in_material(pool_material, "semantic_equivalence_refs")
    if sem.relation_ref not in semantic_refs:
        raise SourceRelationAuthorizationError(
            "OUT_OF_SCOPE", "pooling authority does not bind the exact semantic-equivalence receipt"
        )
    if _exact_relation_ref_in_material(pool_material, "overlap_nonduplication_ref") != overlap.relation_ref:
        raise SourceRelationAuthorizationError(
            "OUT_OF_SCOPE", "pooling authority does not bind the exact nonduplication receipt"
        )
    return _guard_receipt(
        operation_kind="SAMPLE_POOLING", decisions=(sem, overlap, pool),
        operation_scope=operation_scope, target_use=target_use, effective_scope=effective_scope,
    )


def guard_estimand_composition(
    *, resolver: SourceRelationResolver, source_universe_refs: Iterable[ExactRef | Mapping[str, Any]],
    operation_scope: Any, target_use: str, effective_scope: Any,
    semantic_equivalence_ref: ExactRef | Mapping[str, Any],
    overlap_nonduplication_ref: ExactRef | Mapping[str, Any],
    estimand_composition_ref: ExactRef | Mapping[str, Any],
    composition_authority_operation: str,
    semantic_equivalence_authority_operation: str = "I07_SOURCE_SEMANTIC_EQUIVALENCE",
    overlap_authority_operation: str = "I07_OVERLAP_NON_DUPLICATION",
) -> OperationGuardReceipt:
    sources = _canonical_refs(source_universe_refs, "source_universe_ref")
    common = dict(
        source_universe_refs=sources, operation_scope=operation_scope, target_use=target_use,
        effective_scope=effective_scope, directionality_or_symmetric="SYMMETRIC",
    )
    sem = resolver.require(
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE", relation_ref=semantic_equivalence_ref,
        expected_authority_operation=semantic_equivalence_authority_operation, **common,
    )
    overlap = resolver.require(
        relation_kind="OVERLAP_NON_DUPLICATION", relation_ref=overlap_nonduplication_ref,
        expected_authority_operation=overlap_authority_operation, **common,
    )
    composition = resolver.require(
        relation_kind="ESTIMAND_COMPOSITION", relation_ref=estimand_composition_ref,
        expected_authority_operation=composition_authority_operation, **common,
    )
    material = _operation_material(resolver.resolve_exact(composition.relation_ref))
    semantic_refs = _exact_relation_ref_set_in_material(material, "semantic_equivalence_refs")
    if sem.relation_ref not in semantic_refs:
        raise SourceRelationAuthorizationError(
            "OUT_OF_SCOPE", "estimand composition does not bind exact semantic equivalence"
        )
    if _exact_relation_ref_in_material(material, "overlap_treatment_ref") != overlap.relation_ref:
        raise SourceRelationAuthorizationError(
            "OUT_OF_SCOPE", "estimand composition does not bind exact overlap treatment"
        )
    return _guard_receipt(
        operation_kind="ESTIMAND_COMPOSITION", decisions=(sem, overlap, composition),
        operation_scope=operation_scope, target_use=target_use, effective_scope=effective_scope,
    )


def guard_backfill(
    *, resolver: SourceRelationResolver,
    target_source_universe_ref: ExactRef | Mapping[str, Any],
    donor_source_universe_ref: ExactRef | Mapping[str, Any],
    operation_scope: Any, target_use: str, effective_scope: Any,
    target_missingness_state: str,
    semantic_equivalence_ref: ExactRef | Mapping[str, Any],
    overlap_nonduplication_ref: ExactRef | Mapping[str, Any],
    backfill_ref: ExactRef | Mapping[str, Any],
    backfill_authority_operation: str,
    semantic_equivalence_authority_operation: str = "I07_SOURCE_SEMANTIC_EQUIVALENCE",
    overlap_authority_operation: str = "I07_OVERLAP_NON_DUPLICATION",
) -> OperationGuardReceipt:
    target = exact_ref(target_source_universe_ref, "target_source_universe_ref")
    donor = exact_ref(donor_source_universe_ref, "donor_source_universe_ref")
    if target == donor:
        raise SourceRelationIntegrityError("backfill donor and target universes must be distinct")
    state = _text(target_missingness_state, "target_missingness_state")
    if state in FORBIDDEN_BACKFILL_TARGET_STATES:
        raise SourceRelationAuthorizationError(
            "NOT_APPLICABLE", f"{state} is a substantive/negative state, not backfillable missingness"
        )
    sources = _canonical_refs((target, donor), "source_universe_ref")
    symmetric = dict(
        source_universe_refs=sources, operation_scope=operation_scope, target_use=target_use,
        effective_scope=effective_scope, directionality_or_symmetric="SYMMETRIC",
    )
    sem = resolver.require(
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE", relation_ref=semantic_equivalence_ref,
        expected_authority_operation=semantic_equivalence_authority_operation, **symmetric,
    )
    overlap = resolver.require(
        relation_kind="OVERLAP_NON_DUPLICATION", relation_ref=overlap_nonduplication_ref,
        expected_authority_operation=overlap_authority_operation, **symmetric,
    )
    direction = {
        "donor_source_universe_ref": donor.as_dict(),
        "target_source_universe_ref": target.as_dict(),
    }
    backfill = resolver.require(
        relation_kind="BACKFILL", relation_ref=backfill_ref,
        expected_authority_operation=backfill_authority_operation,
        source_universe_refs=sources, operation_scope=operation_scope, target_use=target_use,
        effective_scope=effective_scope, directionality_or_symmetric=direction,
    )
    material = _operation_material(resolver.resolve_exact(backfill.relation_ref))
    if exact_ref(material["target_source_universe_ref"], "backfill.target_source_universe_ref") != target:
        raise SourceRelationAuthorizationError("OUT_OF_SCOPE", "backfill target source mismatch")
    if exact_ref(material["donor_source_universe_ref"], "backfill.donor_source_universe_ref") != donor:
        raise SourceRelationAuthorizationError("OUT_OF_SCOPE", "backfill donor source mismatch")
    eligible = material["eligible_target_missingness_states"]
    if isinstance(eligible, (str, bytes, bytearray)) or not isinstance(eligible, Sequence):
        raise SourceRelationIntegrityError("eligible_target_missingness_states must be an exact sequence")
    if state not in {str(value) for value in eligible}:
        raise SourceRelationAuthorizationError(
            "NOT_APPLICABLE", "target missingness state is not named by exact backfill authority"
        )
    if exact_ref(material["semantic_equivalence_ref"], "backfill.semantic_equivalence_ref") != sem.relation_ref:
        raise SourceRelationAuthorizationError("OUT_OF_SCOPE", "backfill does not bind exact semantic equivalence")
    if exact_ref(material["overlap_nonduplication_ref"], "backfill.overlap_nonduplication_ref") != overlap.relation_ref:
        raise SourceRelationAuthorizationError("OUT_OF_SCOPE", "backfill does not bind exact nonduplication relation")
    return _guard_receipt(
        operation_kind="BACKFILL", decisions=(sem, overlap, backfill),
        operation_scope=operation_scope, target_use=target_use, effective_scope=effective_scope,
    )


def _i03_operation_scope(query: EmpiricalQuerySpec) -> Mapping[str, Any]:
    return {
        "i03_query_ref": query.ref.as_dict(),
        "condition_predicate_ref": canonicalize(query.condition_predicate_ref),
        "risk_set_ref": canonicalize(query.risk_set_ref),
        "measure_basis_ref": canonicalize(query.measure_basis_ref),
        "target_refs": canonicalize(query.target_refs),
    }


def _i03_grain(query: EmpiricalQuerySpec) -> Mapping[str, Any]:
    grain = query.requested_output_grain
    if not isinstance(grain, Mapping):
        raise SourceRelationIntegrityError("I03 requested_output_grain must be an exact mapping")
    return grain


def guard_i03_authorized_composite_query(
    *,
    query: EmpiricalQuerySpec,
    resolver: SourceRelationResolver,
    relation_refs: Mapping[str, ExactRef | Mapping[str, Any]],
) -> I03CompositeGuardReceipt:
    """Pre-guard I03 AUTHORIZED_COMPOSITE without modifying I03 semantics.

    I03 keeps its existing three authority roles.  I07 additionally requires
    exact P07 semantic-equivalence/nonduplication/pooling/estimand-composition
    receipts, and binds the I07 pooling/nonduplication/composition authority refs
    to the exact refs already carried by I03's authority bundle.
    """
    if not isinstance(query, EmpiricalQuerySpec):
        raise SourceRelationIntegrityError("query must be EmpiricalQuerySpec@1.0.0")
    if semantic_hash(query.semantic_projection()) != query.content_hash:
        raise SourceRelationIntegrityError("I03 query semantic hash mismatch")
    grain = _i03_grain(query)
    if grain.get("source_scope_mode") != "AUTHORIZED_COMPOSITE":
        raise SourceRelationAuthorizationError(
            "NOT_APPLICABLE", "I07 composite guard applies only to I03 AUTHORIZED_COMPOSITE"
        )
    required_relation_keys = {
        "SOURCE_SEMANTIC_EQUIVALENCE", "OVERLAP_NON_DUPLICATION",
        "SAMPLE_POOLING", "ESTIMAND_COMPOSITION",
    }
    if set(relation_refs) != required_relation_keys:
        raise SourceRelationAuthorizationError(
            "UNKNOWN_AUTHORITY",
            "I03 I07 guard requires exact semantic-equivalence, nonduplication, pooling and estimand-composition relation refs",
        )
    bundle = grain.get("authorized_composite_authority_refs")
    if not isinstance(bundle, Mapping):
        raise SourceRelationAuthorizationError(
            "UNKNOWN_AUTHORITY", "I03 composite query lacks its exact three-role authority bundle"
        )
    if not {"pooling", "nonduplication", "estimand_composition"} <= set(bundle):
        raise SourceRelationAuthorizationError(
            "UNKNOWN_AUTHORITY", "I03 composite authority bundle is incomplete"
        )

    def i03_role(role: str) -> tuple[AuthorityRef, str]:
        entry = bundle[role]
        if not isinstance(entry, Mapping) or set(entry) != {"authority_ref", "operation"}:
            raise SourceRelationIntegrityError(
                f"I03 {role} authority binding must contain exact authority_ref and operation only"
            )
        ref = authority_ref(entry["authority_ref"], f"i03.{role}.authority_ref")
        operation = _text(entry["operation"], f"i03.{role}.operation")
        return ref, operation

    pooling_authority, pooling_op = i03_role("pooling")
    nondup_authority, nondup_op = i03_role("nonduplication")
    estimand_authority, estimand_op = i03_role("estimand_composition")
    sources = _canonical_refs(query.empirical_universe_refs, "query.empirical_universe_refs")
    scope = _i03_operation_scope(query)
    effective_scope = grain.get("source_relation_effective_scope", {"query_ref": query.ref.as_dict()})

    sem = resolver.require(
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
        relation_ref=relation_refs["SOURCE_SEMANTIC_EQUIVALENCE"],
        expected_authority_operation="I07_SOURCE_SEMANTIC_EQUIVALENCE",
        source_universe_refs=sources, operation_scope=scope,
        target_use=I03_COMPOSITE_TARGET_USE, effective_scope=effective_scope,
        directionality_or_symmetric="SYMMETRIC",
    )
    overlap = resolver.require(
        relation_kind="OVERLAP_NON_DUPLICATION",
        relation_ref=relation_refs["OVERLAP_NON_DUPLICATION"],
        expected_authority_operation=nondup_op,
        source_universe_refs=sources, operation_scope=scope,
        target_use=I03_COMPOSITE_TARGET_USE, effective_scope=effective_scope,
        directionality_or_symmetric="SYMMETRIC",
    )
    pool = resolver.require(
        relation_kind="SAMPLE_POOLING",
        relation_ref=relation_refs["SAMPLE_POOLING"],
        expected_authority_operation=pooling_op,
        source_universe_refs=sources, operation_scope=scope,
        target_use=I03_COMPOSITE_TARGET_USE, effective_scope=effective_scope,
        directionality_or_symmetric="SYMMETRIC",
    )
    estimand = resolver.require(
        relation_kind="ESTIMAND_COMPOSITION",
        relation_ref=relation_refs["ESTIMAND_COMPOSITION"],
        expected_authority_operation=estimand_op,
        source_universe_refs=sources, operation_scope=scope,
        target_use=I03_COMPOSITE_TARGET_USE, effective_scope=effective_scope,
        directionality_or_symmetric="SYMMETRIC",
    )
    if overlap.authority_ref != nondup_authority:
        raise SourceRelationAuthorizationError(
            "OUT_OF_SCOPE", "I07 nonduplication relation authority differs from exact I03 nonduplication authority"
        )
    if pool.authority_ref != pooling_authority:
        raise SourceRelationAuthorizationError(
            "OUT_OF_SCOPE", "I07 pooling relation authority differs from exact I03 pooling authority"
        )
    if estimand.authority_ref != estimand_authority:
        raise SourceRelationAuthorizationError(
            "OUT_OF_SCOPE", "I07 estimand relation authority differs from exact I03 estimand authority"
        )

    pool_material = _operation_material(resolver.resolve_exact(pool.relation_ref))
    if sem.relation_ref not in _exact_relation_ref_set_in_material(pool_material, "semantic_equivalence_refs"):
        raise SourceRelationAuthorizationError("OUT_OF_SCOPE", "I03 pooling relation omits exact semantic equivalence")
    if _exact_relation_ref_in_material(pool_material, "overlap_nonduplication_ref") != overlap.relation_ref:
        raise SourceRelationAuthorizationError("OUT_OF_SCOPE", "I03 pooling relation omits exact nonduplication")
    composition_material = _operation_material(resolver.resolve_exact(estimand.relation_ref))
    if sem.relation_ref not in _exact_relation_ref_set_in_material(composition_material, "semantic_equivalence_refs"):
        raise SourceRelationAuthorizationError("OUT_OF_SCOPE", "I03 estimand composition omits exact semantic equivalence")
    if _exact_relation_ref_in_material(composition_material, "overlap_treatment_ref") != overlap.relation_ref:
        raise SourceRelationAuthorizationError("OUT_OF_SCOPE", "I03 estimand composition omits exact overlap treatment")

    i03_refs = tuple(sorted({pooling_authority, nondup_authority, estimand_authority}, key=lambda ref: ref.key))
    guard_hash = semantic_hash({
        "contract": I07_CONTRACT_ID,
        "query_ref": query.ref.as_dict(),
        "source_universe_refs": [ref.as_dict() for ref in sources],
        "semantic_equivalence_ref": sem.relation_ref.as_dict(),
        "overlap_nonduplication_ref": overlap.relation_ref.as_dict(),
        "pooling_ref": pool.relation_ref.as_dict(),
        "estimand_composition_ref": estimand.relation_ref.as_dict(),
        "i03_authority_refs": [ref.as_dict() for ref in i03_refs],
    })
    return I03CompositeGuardReceipt(
        query.ref, sources, sem.relation_ref, overlap.relation_ref,
        pool.relation_ref, estimand.relation_ref, i03_refs, guard_hash,
    )


def execute_i03_composite_query_guarded(
    *,
    repository: C11Repository,
    query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    authority_registry: AuthorityRegistry,
    release_refs: Iterable[ExactRef],
    relation_resolver: SourceRelationResolver,
    relation_refs: Mapping[str, ExactRef | Mapping[str, Any]],
):
    """Run unchanged I03 execution only after the exact I07 composite pre-guard."""
    guard_i03_authorized_composite_query(
        query=query, resolver=relation_resolver, relation_refs=relation_refs
    )
    from rawlsing_next.pre553_empirical_query import execute_empirical_query

    return execute_empirical_query(
        repository=repository,
        query=query,
        predicate=predicate,
        authority_registry=authority_registry,
        release_refs=release_refs,
    )


__all__ = [
    "I07_CONTRACT_ID", "DEFAULT_RELATION_STATE", "I03_COMPOSITE_TARGET_USE",
    "RELATION_AUTHORITY_KIND", "RELATION_REQUIRED_MATERIAL_KEYS", "RELATION_DECISION_MATRIX",
    "FORBIDDEN_BACKFILL_TARGET_STATES", "SourceRelationError", "SourceRelationIntegrityError",
    "SourceRelationAuthorizationError", "RelationDecision", "OperationGuardReceipt",
    "I03CompositeGuardReceipt", "make_source_universe_relation", "SourceRelationResolver",
    "guard_sample_pooling", "guard_estimand_composition", "guard_backfill",
    "guard_i03_authorized_composite_query", "execute_i03_composite_query_guarded",
]
