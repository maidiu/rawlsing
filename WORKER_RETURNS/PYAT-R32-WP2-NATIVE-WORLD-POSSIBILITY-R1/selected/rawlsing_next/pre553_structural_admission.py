"""PRE553 I04 exact StructuralEmpiricalAdmission decision service.

This module owns only the P06 admission decision/receipt seam and lossless
projection material. It does not execute empirical queries, infer source
relations, create generated actor positions, decide V553 temporal operations,
or select V554 basis/equivalence/precedence.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityConflict,
    Pre553AuthorityError,
    require_positive_authority,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalFact,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553IntegrityError,
    Pre553SemanticCollapseError,
    StructuralEmpiricalAdmission,
    authority_ref,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)

I04_CONTRACT_ID = "PRE553_I04_STRUCTURAL_ADMISSION_V553@1.0.0"
P06_RULE_CONTRACT_ID = "PRE553_STRUCTURAL_ADMISSION_RULE@1.0.0"
M1_BASIS_KIND = "DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION"

DECISION_PRECEDENCE = (
    "INTEGRITY_FAILURE",
    "MISSING_STRUCTURAL_ADMISSION_AUTHORITY",
    "UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY",
    "ADMISSION_DENIED",
    "NEGATIVE_AUTHORITY_ONLY",
    "SOURCE_NOT_APPLICABLE_TO_STRUCTURAL_USE",
    "EMPIRICAL_FACT_NONCOMPARABLE",
    "TEMPORAL_SCOPE_MISMATCH",
    "STRUCTURAL_TARGET_UNRESOLVED",
    "INSUFFICIENT_EVIDENCE_UNDER_RULE",
    "ADMISSION_DEFERRED",
    "VALID_EMPTY",
    "ADMITTED",
)
P06_NONPOSITIVE_DECISIONS = frozenset(DECISION_PRECEDENCE[:-1])
POSITIVE_DECISION = "ADMITTED"

# I01 freezes a deliberately coarser public state vocabulary while preserving
# the exact P06 state in admission_decision_state. I04 must not widen I01.
PUBLIC_STATE_BY_DECISION = MappingProxyType({
    "ADMITTED": "ADMITTED_FOR_EXACT_STRUCTURAL_USE",
    "MISSING_STRUCTURAL_ADMISSION_AUTHORITY": "MISSING_AUTHORITY",
    "ADMISSION_DENIED": "ADMISSION_DENIED",
    "ADMISSION_DEFERRED": "DEFERRED",
    "EMPIRICAL_FACT_NONCOMPARABLE": "NONCOMPARABLE",
    "SOURCE_NOT_APPLICABLE_TO_STRUCTURAL_USE": "OUT_OF_SCOPE",
    "INSUFFICIENT_EVIDENCE_UNDER_RULE": "INSUFFICIENT_EVIDENCE",
    "TEMPORAL_SCOPE_MISMATCH": "OUT_OF_SCOPE",
    "STRUCTURAL_TARGET_UNRESOLVED": "UNRESOLVED",
    "NEGATIVE_AUTHORITY_ONLY": "ADMISSION_DENIED",
    "UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY": "UNRESOLVED",
    "VALID_EMPTY": "UNRESOLVED",
    "INTEGRITY_FAILURE": "INTEGRITY_FAILURE",
})

DECISION_MATRIX = MappingProxyType({
    state: MappingProxyType({
        "public_typed_state": PUBLIC_STATE_BY_DECISION[state],
        "positive_structural_evidence": state == "ADMITTED",
        "m1_direct_projection_allowed": state == "ADMITTED",
        "v553_reference_allowed": True,
        "v553_positive_temporal_output_implied": False,
    })
    for state in DECISION_PRECEDENCE
})

V553_PARTICIPANT_FIELDS = (
    "role",
    "ordinal",
    "structural_empirical_admission_ref",
)
V553_INGRESS_CONTRACT = MappingProxyType({
    "semantic_input_kind": "STRUCTURAL_EMPIRICAL_ADMISSION",
    "participant_fields": V553_PARTICIPANT_FIELDS,
    "raw_empirical_fact_input_allowed": False,
    "discovery_result_direct_input_allowed": False,
    "diagnostic_score_direct_input_allowed": False,
    "p06_i04_decides_v553_required": False,
    "p06_i04_decides_temporal_operations": False,
    "p06_i04_mints_temporal_objects": False,
})

M1_DIRECT_PROJECTION_FIELDS = (
    "structural_empirical_admission_id",
    "structural_empirical_admission_content_hash",
    "admission_authority_id",
    "admission_authority_version",
    "admission_authority_hash",
    "admission_decision_state",
    "focal_structural_proposition_ref",
    "structural_semantic_identity_refs",
    "native_scope_identity_refs",
    "target_use_permission_refs",
    "effective_time_or_interval_refs_required_by_target_use",
    "source_universe_refs",
    "estimand_refs",
    "measure_and_weight_authority_refs",
    "applicable_negative_denial_noncomparability_refs",
    "interpretation_critical_authority_refs",
    "producer_replay_locator_or_reference_root",
)

SOURCE_RELATION_KINDS = frozenset({
    "SOURCE_UNIVERSE_RELATION",
    "SOURCE_EQUIVALENCE",
    "SOURCE_RESPONDENT_LINKAGE",
    "SOURCE_COMPOSITION_POOLING",
    "SOURCE_BACKFILL",
})
FORBIDDEN_INTERPRETATION_MARKERS = frozenset({
    "GENERATED_ACTOR_POSITION",
    "GENERATED_NINE_STRATUM_POSITION",
    "ACTOR_BELIEF",
    "ACTOR_PERSONA",
    "ACTOR_PSYCHE",
    "ACTOR_MEMORY",
    "ACTOR_KNOWLEDGE",
    "ACTOR_RESPONSE",
    "DIAGNOSTIC_SCORE_AS_STRUCTURAL_FACT",
})


class StructuralAdmissionError(Pre553IntegrityError):
    """I04 request/rule/receipt cannot be evaluated lawfully."""


class StructuralAdmissionProjectionError(StructuralAdmissionError):
    """A nonpositive or incomplete admission was projected as positive basis."""


@dataclass(frozen=True)
class AdmissionCondition:
    """One externally owned exact blocker/limit presented to I04.

    I04 may preserve and order such a condition; it may not invent the upstream
    fact, source, measure, temporal, or comparability authority behind it.
    """

    decision_state: str
    reason_code: str
    evidence_refs: tuple[ExactRef, ...]

    def __post_init__(self) -> None:
        if self.decision_state not in P06_NONPOSITIVE_DECISIONS:
            raise StructuralAdmissionError("AdmissionCondition must name a P06 nonpositive decision")
        if not isinstance(self.reason_code, str) or not self.reason_code.strip():
            raise StructuralAdmissionError("AdmissionCondition reason_code must be non-empty")
        object.__setattr__(self, "reason_code", self.reason_code.strip())
        refs = tuple(sorted({exact_ref(v) for v in self.evidence_refs}, key=lambda r: r.key))
        if not refs:
            raise StructuralAdmissionError("AdmissionCondition requires exact evidence refs")
        object.__setattr__(self, "evidence_refs", refs)


@dataclass(frozen=True)
class RequiredAuthorityBinding:
    role: str
    authority_ref: AuthorityRef
    authority_kind: str
    operation: str
    source_universe_ref: ExactRef | None = None
    target_use_ref: Any | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.role, str) or not self.role.strip():
            raise StructuralAdmissionError("authority binding role must be non-empty")
        object.__setattr__(self, "role", self.role.strip())
        object.__setattr__(self, "authority_ref", authority_ref(self.authority_ref))
        if not isinstance(self.authority_kind, str) or not self.authority_kind.strip():
            raise StructuralAdmissionError("authority_kind must be non-empty")
        if not isinstance(self.operation, str) or not self.operation.strip():
            raise StructuralAdmissionError("authority operation must be non-empty")
        object.__setattr__(self, "authority_kind", self.authority_kind.strip())
        object.__setattr__(self, "operation", self.operation.strip())
        if self.source_universe_ref is not None:
            object.__setattr__(self, "source_universe_ref", exact_ref(self.source_universe_ref))
        canonicalize(self.target_use_ref)


@dataclass(frozen=True)
class StructuralAdmissionRule:
    """Content-addressed P06 rule whose hash is the named admission authority hash."""

    admission_authority_ref: AuthorityRef
    admission_operation: str
    target_use: str
    allowed_empirical_fact_states: tuple[str, ...]
    allowed_empirical_fact_families: tuple[str, ...]
    allowed_empirical_query_families: tuple[str, ...]
    required_empirical_predicate_target_semantics_refs: tuple[ExactRef, ...]
    structural_target_identity_refs: tuple[ExactRef, ...]
    focal_structural_proposition_ref: ExactRef
    structural_semantic_identity_refs: tuple[ExactRef, ...]
    interpretation_or_transformation_semantics: Mapping[str, Any]
    directionality_or_role_semantics: Mapping[str, Any]
    target_use_permission_refs: tuple[ExactRef, ...]
    allowed_native_scope_identity_refs: tuple[ExactRef, ...]
    allowed_effective_time_or_interval_refs: tuple[ExactRef, ...]
    allowed_estimand_refs: tuple[ExactRef, ...]
    allowed_measure_and_weight_authority_refs: tuple[ExactRef, ...]
    allowed_uncertainty_states: tuple[str, ...]
    source_disagreement_noncomparability_policy: str
    negative_authority_refs: tuple[ExactRef, ...]
    required_authority_bindings: tuple[RequiredAuthorityBinding, ...]
    time_geography_applicability: Mapping[str, Any]
    effective_period: Mapping[str, Any]
    downstream_structural_producer_or_use: str
    replay_semantics: Mapping[str, Any]
    negative_authority_only: bool = False
    compatibility_semantic_surface_ref: ExactRef | None = None
    compatibility_parity_claim_scope: Any | None = None
    compatibility_parity_receipt_ref: ExactRef | None = None
    compatibility_retained_structural_meaning_ref: ExactRef | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "admission_authority_ref", authority_ref(self.admission_authority_ref))
        for name in (
            "admission_operation", "target_use", "source_disagreement_noncomparability_policy",
            "downstream_structural_producer_or_use",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise StructuralAdmissionError(f"{name} must be non-empty")
            object.__setattr__(self, name, value.strip())
        if not self.allowed_empirical_fact_states:
            raise StructuralAdmissionError("rule must name allowed empirical fact states")
        if not self.allowed_empirical_fact_families or not self.allowed_empirical_query_families:
            raise StructuralAdmissionError("rule must name allowed empirical fact and query families")
        if not self.required_empirical_predicate_target_semantics_refs:
            raise StructuralAdmissionError("rule must bind exact predicate/target semantics")
        if not self.structural_target_identity_refs or not self.structural_semantic_identity_refs:
            raise StructuralAdmissionError("rule must bind exact structural target/semantic identity")
        if not self.target_use_permission_refs:
            raise StructuralAdmissionError("rule must bind exact target-use permission refs")
        for field_name in (
            "required_empirical_predicate_target_semantics_refs", "structural_target_identity_refs",
            "structural_semantic_identity_refs", "target_use_permission_refs",
            "allowed_native_scope_identity_refs", "allowed_effective_time_or_interval_refs",
            "allowed_estimand_refs", "allowed_measure_and_weight_authority_refs",
            "negative_authority_refs",
        ):
            refs = tuple(sorted({exact_ref(v) for v in getattr(self, field_name)}, key=lambda r: r.key))
            object.__setattr__(self, field_name, refs)
        object.__setattr__(self, "focal_structural_proposition_ref", exact_ref(self.focal_structural_proposition_ref))
        if self.compatibility_semantic_surface_ref is not None:
            object.__setattr__(self, "compatibility_semantic_surface_ref", exact_ref(self.compatibility_semantic_surface_ref))
        if self.compatibility_parity_receipt_ref is not None:
            object.__setattr__(self, "compatibility_parity_receipt_ref", exact_ref(self.compatibility_parity_receipt_ref))
        if self.compatibility_retained_structural_meaning_ref is not None:
            object.__setattr__(self, "compatibility_retained_structural_meaning_ref", exact_ref(self.compatibility_retained_structural_meaning_ref))
        canonicalize(self.interpretation_or_transformation_semantics)
        canonicalize(self.directionality_or_role_semantics)
        canonicalize(self.time_geography_applicability)
        canonicalize(self.effective_period)
        canonicalize(self.replay_semantics)
        _reject_forbidden_interpretation(self.interpretation_or_transformation_semantics)
        _reject_forbidden_structural_targets(self.structural_target_identity_refs)
        required_kinds = {b.authority_kind for b in self.required_authority_bindings}
        if "TARGET_USE_PERMISSION" not in required_kinds:
            raise StructuralAdmissionError("rule must bind exact TARGET_USE_PERMISSION authority")
        if self.allowed_effective_time_or_interval_refs and "TEMPORAL_EVIDENCE" not in required_kinds:
            raise StructuralAdmissionError("time-scoped rule must bind exact TEMPORAL_EVIDENCE authority")
        if self.allowed_measure_and_weight_authority_refs and "WEIGHT_DESIGN_ESTIMAND" not in required_kinds:
            raise StructuralAdmissionError("measure/estimand-scoped rule must bind exact WEIGHT_DESIGN_ESTIMAND authority")

    @property
    def semantic_material(self) -> Mapping[str, Any]:
        return {
            "rule_contract_id": P06_RULE_CONTRACT_ID,
            "admission_rule_id": self.admission_authority_ref.authority_id,
            "admission_rule_version": self.admission_authority_ref.authority_version,
            "admission_operation": self.admission_operation,
            "target_use": self.target_use,
            "allowed_empirical_fact_states": sorted(set(self.allowed_empirical_fact_states)),
            "allowed_empirical_fact_families": sorted(set(self.allowed_empirical_fact_families)),
            "allowed_empirical_query_families": sorted(set(self.allowed_empirical_query_families)),
            "required_empirical_predicate_target_semantics_refs": [r.as_dict() for r in self.required_empirical_predicate_target_semantics_refs],
            "structural_target_identity_refs": [r.as_dict() for r in self.structural_target_identity_refs],
            "focal_structural_proposition_ref": self.focal_structural_proposition_ref.as_dict(),
            "structural_semantic_identity_refs": [r.as_dict() for r in self.structural_semantic_identity_refs],
            "interpretation_or_transformation_semantics": canonicalize(self.interpretation_or_transformation_semantics),
            "directionality_or_role_semantics": canonicalize(self.directionality_or_role_semantics),
            "target_use_permission_refs": [r.as_dict() for r in self.target_use_permission_refs],
            "allowed_native_scope_identity_refs": [r.as_dict() for r in self.allowed_native_scope_identity_refs],
            "allowed_effective_time_or_interval_refs": [r.as_dict() for r in self.allowed_effective_time_or_interval_refs],
            "allowed_estimand_refs": [r.as_dict() for r in self.allowed_estimand_refs],
            "allowed_measure_and_weight_authority_refs": [r.as_dict() for r in self.allowed_measure_and_weight_authority_refs],
            "allowed_uncertainty_states": sorted(set(self.allowed_uncertainty_states)),
            "source_disagreement_noncomparability_policy": self.source_disagreement_noncomparability_policy,
            "negative_authority_refs": [r.as_dict() for r in self.negative_authority_refs],
            "required_authority_bindings": [
                {
                    "role": b.role,
                    "authority_ref": b.authority_ref.as_dict(),
                    "authority_kind": b.authority_kind,
                    "operation": b.operation,
                    "source_universe_ref": b.source_universe_ref.as_dict() if b.source_universe_ref else None,
                    "target_use_ref": canonicalize(b.target_use_ref),
                }
                for b in sorted(
                    self.required_authority_bindings,
                    key=lambda x: (x.role, x.authority_ref.key, x.operation),
                )
            ],
            "time_geography_applicability": canonicalize(self.time_geography_applicability),
            "effective_period": canonicalize(self.effective_period),
            "downstream_structural_producer_or_use": self.downstream_structural_producer_or_use,
            "replay_semantics": canonicalize(self.replay_semantics),
            "negative_authority_only": self.negative_authority_only,
            "compatibility_semantic_surface_ref": self.compatibility_semantic_surface_ref.as_dict() if self.compatibility_semantic_surface_ref else None,
            "compatibility_parity_claim_scope": canonicalize(self.compatibility_parity_claim_scope),
            "compatibility_parity_receipt_ref": self.compatibility_parity_receipt_ref.as_dict() if self.compatibility_parity_receipt_ref else None,
            "compatibility_retained_structural_meaning_ref": self.compatibility_retained_structural_meaning_ref.as_dict() if self.compatibility_retained_structural_meaning_ref else None,
        }

    @property
    def admission_rule_id(self) -> str:
        return self.admission_authority_ref.authority_id

    @property
    def admission_rule_version(self) -> str:
        return self.admission_authority_ref.authority_version

    @property
    def admission_rule_hash(self) -> str:
        return self.admission_authority_ref.authority_content_hash

    def verify_content_hash_binding(self) -> None:
        if semantic_hash(self.semantic_material) != self.admission_authority_ref.authority_content_hash:
            raise StructuralAdmissionError(
                "structural-admission rule semantic hash does not match exact admission authority ref"
            )


@dataclass(frozen=True)
class StructuralAdmissionRequest:
    native_scope_identity_refs: tuple[ExactRef, ...]
    effective_time_or_interval_refs_required_by_target_use: tuple[ExactRef, ...]
    estimand_refs: tuple[ExactRef, ...]
    measure_and_weight_authority_refs: tuple[ExactRef, ...]
    support_uncertainty_refs: tuple[ExactRef, ...]
    interpretation_critical_authority_refs: tuple[ExactRef, ...]
    conditions: tuple[AdmissionCondition, ...] = ()
    discovery_result_receipt_refs: tuple[ExactRef, ...] = ()
    legacy_compatibility_refs: tuple[ExactRef, ...] = ()

    def __post_init__(self) -> None:
        for name in (
            "native_scope_identity_refs", "effective_time_or_interval_refs_required_by_target_use",
            "estimand_refs", "measure_and_weight_authority_refs", "support_uncertainty_refs",
            "interpretation_critical_authority_refs", "discovery_result_receipt_refs",
            "legacy_compatibility_refs",
        ):
            refs = tuple(sorted({exact_ref(v) for v in getattr(self, name)}, key=lambda r: r.key))
            object.__setattr__(self, name, refs)
        conditions = tuple(self.conditions)
        if any(not isinstance(c, AdmissionCondition) for c in conditions):
            raise StructuralAdmissionError("conditions must contain AdmissionCondition values")
        object.__setattr__(self, "conditions", tuple(sorted(
            conditions, key=lambda c: (DECISION_PRECEDENCE.index(c.decision_state), c.reason_code)
        )))


@dataclass(frozen=True)
class AdmissionEvaluation:
    decision_state: str
    reason_code: str
    receipt: StructuralEmpiricalAdmission
    blocking_refs: tuple[ExactRef, ...]
    m1_direct_projection: Mapping[str, Any] | None
    m1_projection_hash: str | None
    v553_participant_projection: Mapping[str, Any]


def _reject_forbidden_interpretation(value: Any) -> None:
    text = canonical_json(value).upper()
    for marker in FORBIDDEN_INTERPRETATION_MARKERS:
        if marker in text:
            raise Pre553SemanticCollapseError(
                f"forbidden cross-ontology structural interpretation: {marker}"
            )


def _reject_forbidden_structural_targets(refs: Iterable[ExactRef]) -> None:
    forbidden_fragments = (
        "GENERATED_ACTOR_POSITION", "GENERATED_NINE_STRATUM_POSITION",
        "ACTOR_BELIEF", "ACTOR_PERSONA", "ACTOR_PSYCHE", "ACTOR_RESPONSE",
    )
    for ref in refs:
        normalized = ref.kind.upper().replace("-", "_").replace(" ", "_")
        if any(fragment in normalized for fragment in forbidden_fragments):
            raise Pre553SemanticCollapseError(
                "StructuralEmpiricalAdmission target may not be generated actor position or actor psyche"
            )


def _refs_from_field(value: Any, name: str) -> tuple[ExactRef, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise StructuralAdmissionError(f"{name} must be exact-ref sequence")
    return tuple(sorted({exact_ref(v, name) for v in value}, key=lambda r: r.key))


def _verify_identity(obj: EmpiricalQuerySpec | EmpiricalFact) -> None:
    if semantic_hash(obj.semantic_projection()) != obj.content_hash:
        raise StructuralAdmissionError(f"{obj.schema_id} semantic projection/content hash mismatch")
    if obj.ref.object_id != obj.object_id or obj.ref.content_hash != obj.content_hash:
        raise StructuralAdmissionError(f"{obj.schema_id} exact reference mismatch")


def _decision_from_authority_state(snapshot: AuthoritySnapshot) -> str | None:
    state = snapshot.decision_state
    if state == "ALLOW":
        return None
    if state == "DENY":
        return "ADMISSION_DENIED"
    if state == "DEFER":
        return "ADMISSION_DEFERRED"
    if state == "MISSING_AUTHORITY":
        return "MISSING_STRUCTURAL_ADMISSION_AUTHORITY"
    if state in {"OUT_OF_SCOPE", "AUTHORITY_SCOPE_MISMATCH"}:
        return "SOURCE_NOT_APPLICABLE_TO_STRUCTURAL_USE"
    if state == "AUTHORITY_HASH_MISMATCH":
        return "INTEGRITY_FAILURE"
    return "UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY"


def _resolve_binding(
    registry: AuthorityRegistry,
    binding: RequiredAuthorityBinding,
) -> tuple[AuthoritySnapshot | None, str | None]:
    try:
        snapshot = registry.resolve_exact(binding.authority_ref).snapshot
    except (Pre553AuthorityError, Pre553AuthorityConflict):
        return None, "UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY"
    state_decision = _decision_from_authority_state(snapshot)
    if state_decision is not None:
        # External MISSING authority is a required-authority failure rather than
        # a claim that the named structural admission rule itself is absent.
        if state_decision == "MISSING_STRUCTURAL_ADMISSION_AUTHORITY":
            state_decision = "UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY"
        return snapshot, state_decision
    try:
        require_positive_authority(
            snapshot,
            authority_kind=binding.authority_kind,
            operation=binding.operation,
            source_universe_ref=(binding.source_universe_ref.as_dict() if binding.source_universe_ref else None),
            target_use_ref=binding.target_use_ref,
        )
    except Pre553AuthorityError as exc:
        text = str(exc).lower()
        role = binding.role.upper()
        if "scope" in text and role.startswith("TEMPORAL"):
            return snapshot, "TEMPORAL_SCOPE_MISMATCH"
        if "scope" in text and role.startswith("SOURCE"):
            return snapshot, "SOURCE_NOT_APPLICABLE_TO_STRUCTURAL_USE"
        return snapshot, "UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY"
    return snapshot, None


def _choose_decision(candidates: Iterable[str]) -> str:
    pool = set(candidates)
    for state in DECISION_PRECEDENCE:
        if state in pool:
            return state
    return "ADMITTED"


def _rule_membership_mismatch(required: tuple[ExactRef, ...], allowed: tuple[ExactRef, ...]) -> bool:
    if not allowed:
        return False
    return not set(required).issubset(set(allowed))


def _query_semantic_refs(query: EmpiricalQuerySpec, fact: EmpiricalFact) -> frozenset[ExactRef]:
    refs = set(_refs_from_field(query.target_refs, "query.target_refs"))
    refs.add(exact_ref(query.condition_predicate_ref, "query.condition_predicate_ref"))
    refs.add(exact_ref(query.risk_set_ref, "query.risk_set_ref"))
    refs.add(exact_ref(fact.response_state_semantics_ref, "fact.response_state_semantics_ref"))
    return frozenset(refs)


def _support_uncertainty_state(fact: EmpiricalFact) -> Mapping[str, Any]:
    return {
        "empirical_fact_state": fact.typed_state,
        "raw_numerator_support": fact.raw_numerator_support,
        "raw_denominator_support": fact.raw_denominator_support,
        "weighted_numerator_support_if_authorized": canonicalize(fact.weighted_numerator_support_if_authorized),
        "weighted_denominator_support_if_authorized": canonicalize(fact.weighted_denominator_support_if_authorized),
        "uncertainty_method_or_typed_state": canonicalize(fact.uncertainty_method_or_typed_state),
    }


def _authority_closure_material(
    *,
    query: EmpiricalQuerySpec,
    fact: EmpiricalFact,
    requested_ref: AuthorityRef,
    rule: StructuralAdmissionRule | None,
    resolved_snapshots: Iterable[AuthoritySnapshot],
) -> tuple[Mapping[str, str], ...]:
    refs = set(query.authority_snapshot_refs) | set(fact.authority_snapshot_refs) | {requested_ref}
    refs.update(snapshot.authority_ref for snapshot in resolved_snapshots)
    if rule is not None:
        refs.update(binding.authority_ref for binding in rule.required_authority_bindings)
    return tuple(ref.as_dict() for ref in sorted(refs, key=lambda r: r.key))


def evaluate_structural_empirical_admission(
    *,
    query: EmpiricalQuerySpec,
    fact: EmpiricalFact,
    requested_admission_authority_ref: AuthorityRef,
    rule: StructuralAdmissionRule | None,
    request: StructuralAdmissionRequest,
    authority_registry: AuthorityRegistry,
    producer_replay_locator_or_reference_root: ExactRef | str,
) -> AdmissionEvaluation:
    """Evaluate one exact EmpiricalFact for one exact structural use.

    Only a fully resolved, hash-bound, positive named rule may return ADMITTED.
    All other outcomes remain exact, replayable, nonpositive P06 states.
    """
    requested_ref = authority_ref(requested_admission_authority_ref)
    if not isinstance(query, EmpiricalQuerySpec) or not isinstance(fact, EmpiricalFact):
        raise StructuralAdmissionError("I04 requires exact I01 EmpiricalQuerySpec and EmpiricalFact objects")
    if not isinstance(request, StructuralAdmissionRequest):
        raise StructuralAdmissionError("request must be StructuralAdmissionRequest")
    if not isinstance(authority_registry, AuthorityRegistry):
        raise StructuralAdmissionError("authority_registry must be accepted exact AuthorityRegistry")

    decisions: list[str] = []
    reasons: list[tuple[str, str]] = []
    authority_snapshots: list[AuthoritySnapshot] = []
    blockers: set[ExactRef] = set()
    query_universes: tuple[ExactRef, ...] = ()
    fact_universes: tuple[ExactRef, ...] = ()

    for condition in request.conditions:
        decisions.append(condition.decision_state)
        reasons.append((condition.decision_state, condition.reason_code))
        blockers.update(condition.evidence_refs)

    try:
        _verify_identity(query)
        _verify_identity(fact)
        query_universes = _refs_from_field(query.empirical_universe_refs, "query.empirical_universe_refs")
        fact_universes = _refs_from_field(fact.empirical_universe_refs, "fact.empirical_universe_refs")
        fact_query_ref = exact_ref(fact.empirical_query_spec_ref, "fact.empirical_query_spec_ref")
        if fact_query_ref != query.ref:
            raise StructuralAdmissionError("EmpiricalFact does not bind supplied EmpiricalQuerySpec exactly")
        if query_universes != fact_universes:
            raise StructuralAdmissionError("query/fact source universe identity mismatch")
    except (Pre553IntegrityError, Pre553SemanticCollapseError, StructuralAdmissionError):
        decisions.append("INTEGRITY_FAILURE")
        reasons.append(("INTEGRITY_FAILURE", "I04_INPUT_IDENTITY_OR_CLOSURE_FAILURE"))

    for upstream_ref in tuple(query.authority_snapshot_refs) + tuple(fact.authority_snapshot_refs):
        try:
            upstream_snapshot = authority_registry.resolve_exact(upstream_ref).snapshot
            authority_snapshots.append(upstream_snapshot)
        except (Pre553AuthorityError, Pre553AuthorityConflict):
            decisions.append("UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY")
            reasons.append(("UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY", "UPSTREAM_QUERY_FACT_AUTHORITY_CLOSURE_UNAVAILABLE"))

    if rule is None:
        decisions.append("MISSING_STRUCTURAL_ADMISSION_AUTHORITY")
        reasons.append(("MISSING_STRUCTURAL_ADMISSION_AUTHORITY", "NO_NAMED_EXACT_STRUCTURAL_ADMISSION_RULE"))
    else:
        if rule.admission_authority_ref != requested_ref:
            decisions.append("INTEGRITY_FAILURE")
            reasons.append(("INTEGRITY_FAILURE", "REQUESTED_RULE_AUTHORITY_REF_MISMATCH"))
        try:
            rule.verify_content_hash_binding()
        except StructuralAdmissionError:
            decisions.append("INTEGRITY_FAILURE")
            reasons.append(("INTEGRITY_FAILURE", "ADMISSION_RULE_CONTENT_HASH_MISMATCH"))

        try:
            admission_snapshot = authority_registry.resolve_exact(requested_ref).snapshot
            authority_snapshots.append(admission_snapshot)
            state_decision = _decision_from_authority_state(admission_snapshot)
            if state_decision is not None:
                decisions.append(state_decision)
                reasons.append((state_decision, f"ADMISSION_AUTHORITY_STATE_{admission_snapshot.decision_state}"))
                blockers.add(ExactRef("AuthoritySnapshot@1.0.0", admission_snapshot.object_id, admission_snapshot.content_hash))
            else:
                try:
                    scoped_universes = fact_universes or (None,)
                    for universe_ref in scoped_universes:
                        require_positive_authority(
                            admission_snapshot,
                            authority_kind="STRUCTURAL_ADMISSION",
                            operation=rule.admission_operation,
                            object_family="StructuralEmpiricalAdmission",
                            source_universe_ref=(universe_ref.as_dict() if universe_ref is not None else None),
                            target_use_ref=rule.target_use,
                        )
                except Pre553AuthorityError as exc:
                    text = str(exc).lower()
                    if "source_universe_refs" in text or "scope" in text:
                        state = "SOURCE_NOT_APPLICABLE_TO_STRUCTURAL_USE"
                        reason_code = "ADMISSION_AUTHORITY_SOURCE_OR_TARGET_SCOPE_MISMATCH"
                    else:
                        state = "UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY"
                        reason_code = "ADMISSION_AUTHORITY_OPERATION_OR_FAMILY_MISMATCH"
                    decisions.append(state)
                    reasons.append((state, reason_code))
                    blockers.add(ExactRef("AuthoritySnapshot@1.0.0", admission_snapshot.object_id, admission_snapshot.content_hash))
        except (Pre553AuthorityError, Pre553AuthorityConflict):
            decisions.append("MISSING_STRUCTURAL_ADMISSION_AUTHORITY")
            reasons.append(("MISSING_STRUCTURAL_ADMISSION_AUTHORITY", "EXACT_ADMISSION_AUTHORITY_UNAVAILABLE"))

        if rule.negative_authority_only:
            decisions.append("NEGATIVE_AUTHORITY_ONLY")
            reasons.append(("NEGATIVE_AUTHORITY_ONLY", "NAMED_RULE_AUTHORIZES_NEGATIVE_LIMIT_ONLY"))

        if fact.typed_state == "NONCOMPARABLE":
            decisions.append("EMPIRICAL_FACT_NONCOMPARABLE")
            reasons.append(("EMPIRICAL_FACT_NONCOMPARABLE", "EMPIRICAL_FACT_NONCOMPARABLE"))
        elif fact.typed_state == "VALID_EMPTY":
            decisions.append("VALID_EMPTY")
            reasons.append(("VALID_EMPTY", "EMPIRICAL_FACT_VALID_EMPTY"))
        elif fact.typed_state == "INTEGRITY_FAILURE":
            decisions.append("INTEGRITY_FAILURE")
            reasons.append(("INTEGRITY_FAILURE", "EMPIRICAL_FACT_INTEGRITY_FAILURE"))
        elif fact.typed_state in {"UNAVAILABLE", "UNRESOLVED", "ZERO_OVERLAP"}:
            decisions.append("INSUFFICIENT_EVIDENCE_UNDER_RULE")
            reasons.append(("INSUFFICIENT_EVIDENCE_UNDER_RULE", f"EMPIRICAL_FACT_{fact.typed_state}"))
        elif fact.typed_state not in set(rule.allowed_empirical_fact_states):
            decisions.append("INSUFFICIENT_EVIDENCE_UNDER_RULE")
            reasons.append(("INSUFFICIENT_EVIDENCE_UNDER_RULE", "EMPIRICAL_FACT_STATE_NOT_ADMITTED_BY_RULE"))

        if fact.FAMILY not in set(rule.allowed_empirical_fact_families) and fact.schema_id not in set(rule.allowed_empirical_fact_families):
            decisions.append("ADMISSION_DENIED")
            reasons.append(("ADMISSION_DENIED", "EMPIRICAL_FACT_FAMILY_NOT_ALLOWED_BY_RULE"))
        if query.FAMILY not in set(rule.allowed_empirical_query_families) and query.schema_id not in set(rule.allowed_empirical_query_families):
            decisions.append("ADMISSION_DENIED")
            reasons.append(("ADMISSION_DENIED", "EMPIRICAL_QUERY_FAMILY_NOT_ALLOWED_BY_RULE"))

        try:
            required_semantic_refs = set(rule.required_empirical_predicate_target_semantics_refs)
            if not required_semantic_refs.issubset(_query_semantic_refs(query, fact)):
                decisions.append("ADMISSION_DENIED")
                reasons.append(("ADMISSION_DENIED", "EMPIRICAL_PREDICATE_TARGET_SEMANTICS_NOT_EXACTLY_BOUND"))
        except Pre553IntegrityError:
            decisions.append("INTEGRITY_FAILURE")
            reasons.append(("INTEGRITY_FAILURE", "EMPIRICAL_PREDICATE_TARGET_SEMANTICS_MALFORMED"))

        if _rule_membership_mismatch(request.native_scope_identity_refs, rule.allowed_native_scope_identity_refs):
            decisions.append("SOURCE_NOT_APPLICABLE_TO_STRUCTURAL_USE")
            reasons.append(("SOURCE_NOT_APPLICABLE_TO_STRUCTURAL_USE", "NATIVE_SCOPE_NOT_ALLOWED_BY_RULE"))
        if _rule_membership_mismatch(
            request.effective_time_or_interval_refs_required_by_target_use,
            rule.allowed_effective_time_or_interval_refs,
        ):
            decisions.append("TEMPORAL_SCOPE_MISMATCH")
            reasons.append(("TEMPORAL_SCOPE_MISMATCH", "RULE_LOCAL_EFFECTIVE_TIME_SCOPE_MISMATCH"))
        if _rule_membership_mismatch(request.estimand_refs, rule.allowed_estimand_refs):
            decisions.append("EMPIRICAL_FACT_NONCOMPARABLE")
            reasons.append(("EMPIRICAL_FACT_NONCOMPARABLE", "ESTIMAND_NOT_ALLOWED_BY_RULE"))
        if _rule_membership_mismatch(
            request.measure_and_weight_authority_refs,
            rule.allowed_measure_and_weight_authority_refs,
        ):
            decisions.append("EMPIRICAL_FACT_NONCOMPARABLE")
            reasons.append(("EMPIRICAL_FACT_NONCOMPARABLE", "MEASURE_WEIGHT_BASIS_NOT_ALLOWED_BY_RULE"))

        uncertainty = canonicalize(fact.uncertainty_method_or_typed_state)
        if rule.allowed_uncertainty_states:
            allowed_uncertainty = {canonical_json(x) for x in rule.allowed_uncertainty_states}
            if canonical_json(uncertainty) not in allowed_uncertainty:
                decisions.append("INSUFFICIENT_EVIDENCE_UNDER_RULE")
                reasons.append(("INSUFFICIENT_EVIDENCE_UNDER_RULE", "UNCERTAINTY_STATE_NOT_ALLOWED_BY_RULE"))

        for binding in rule.required_authority_bindings:
            snapshot, binding_decision = _resolve_binding(authority_registry, binding)
            if snapshot is not None:
                authority_snapshots.append(snapshot)
            if binding_decision is not None:
                decisions.append(binding_decision)
                reasons.append((binding_decision, f"REQUIRED_AUTHORITY_{binding.role}_{binding_decision}"))
                if snapshot is not None:
                    blockers.add(ExactRef("AuthoritySnapshot@1.0.0", snapshot.object_id, snapshot.content_hash))

        if len(fact_universes) > 1:
            relation_bindings = [
                b for b in rule.required_authority_bindings if b.authority_kind in SOURCE_RELATION_KINDS
            ]
            if not relation_bindings:
                decisions.append("UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY")
                reasons.append(("UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY", "MULTI_UNIVERSE_USE_MISSING_EXACT_SOURCE_RELATION_AUTHORITY"))

        if rule.compatibility_semantic_surface_ref is not None:
            if (
                rule.compatibility_parity_receipt_ref is None
                or rule.compatibility_retained_structural_meaning_ref is None
                or rule.compatibility_parity_claim_scope is None
            ):
                decisions.append("UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY")
                reasons.append(("UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY", "LEGACY_COMPATIBILITY_PARITY_NOT_PROVED"))
            if (
                rule.compatibility_parity_receipt_ref is None
                or rule.compatibility_parity_receipt_ref not in set(request.legacy_compatibility_refs)
            ):
                decisions.append("UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY")
                reasons.append(("UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY", "LEGACY_COMPATIBILITY_PARITY_RECEIPT_NOT_EXACTLY_BOUND"))

    decision = _choose_decision(decisions or ("ADMITTED",))
    matching_reasons = sorted(reason for state, reason in reasons if state == decision)
    reason = matching_reasons[0] if matching_reasons else "EXACT_NAMED_RULE_ALL_GATES_PASS"

    if rule is None:
        target_use = "UNRESOLVED_STRUCTURAL_USE"
        target_use_permission_refs: tuple[ExactRef, ...] = ()
        focal = ExactRef("P06MissingStructuralTarget", "MISSING", "0" * 64)
        structural_semantic_refs: tuple[ExactRef, ...] = ()
        interpretation_payload = None
        rule_negative_refs: tuple[ExactRef, ...] = ()
    else:
        target_use = rule.target_use
        target_use_permission_refs = rule.target_use_permission_refs
        focal = rule.focal_structural_proposition_ref
        structural_semantic_refs = rule.structural_semantic_identity_refs
        interpretation_payload = (
            {
                "rule_contract_id": P06_RULE_CONTRACT_ID,
                "admission_rule_id": rule.admission_rule_id,
                "admission_rule_version": rule.admission_rule_version,
                "admission_rule_hash": rule.admission_rule_hash,
                "structural_target_identity_refs": [r.as_dict() for r in rule.structural_target_identity_refs],
                "interpretation_or_transformation_semantics": canonicalize(rule.interpretation_or_transformation_semantics),
                "directionality_or_role_semantics": canonicalize(rule.directionality_or_role_semantics),
                "downstream_structural_producer_or_use": rule.downstream_structural_producer_or_use,
            }
            if decision == "ADMITTED" else None
        )
        rule_negative_refs = rule.negative_authority_refs

    blockers.update(rule_negative_refs)
    for condition in request.conditions:
        blockers.update(condition.evidence_refs)

    authority_refs = tuple(sorted(
        set(query.authority_snapshot_refs)
        | set(fact.authority_snapshot_refs)
        | {s.authority_ref for s in authority_snapshots},
        key=lambda r: r.key,
    ))
    if not authority_refs:
        # A missing named admission authority is preserved in semantic fields;
        # never fabricate a snapshot merely to satisfy the public envelope.
        authority_refs = ()
    if not authority_refs:
        raise StructuralAdmissionError("cannot construct replayable admission without exact authority closure")

    deps = tuple(sorted({
        query.ref,
        fact.ref,
        *request.discovery_result_receipt_refs,
        *request.legacy_compatibility_refs,
    }, key=lambda r: r.key))

    fields: dict[str, Any] = {
        "admission_decision_state": decision,
        "decision_reason_code": reason,
        "empirical_query_spec_ref": query.ref,
        "empirical_fact_ref": fact.ref,
        "admission_authority_ref": requested_ref.as_dict(),
        "source_universe_refs": fact_universes,
        "native_scope_identity_refs": request.native_scope_identity_refs,
        "target_use": target_use,
        "target_use_permission_refs": target_use_permission_refs,
        "focal_structural_proposition_ref": focal,
        "structural_semantic_identity_refs": structural_semantic_refs,
        "effective_time_or_interval_refs_required_by_target_use": request.effective_time_or_interval_refs_required_by_target_use,
        "estimand_refs": request.estimand_refs,
        "measure_and_weight_authority_refs": request.measure_and_weight_authority_refs,
        "support_uncertainty_state": _support_uncertainty_state(fact),
        "support_uncertainty_refs": request.support_uncertainty_refs,
        "applicable_negative_denial_noncomparability_refs": tuple(sorted(blockers, key=lambda r: r.key)),
        "interpretation_critical_authority_refs": request.interpretation_critical_authority_refs,
        "authority_closure_refs": _authority_closure_material(
            query=query,
            fact=fact,
            requested_ref=requested_ref,
            rule=rule,
            resolved_snapshots=authority_snapshots,
        ),
        "blocking_negative_present": decision != "ADMITTED" and bool(blockers),
        "discovery_result_receipt_refs": request.discovery_result_receipt_refs,
        "legacy_compatibility_refs": request.legacy_compatibility_refs,
    }
    if decision == "ADMITTED":
        fields["structural_interpretation_payload"] = interpretation_payload

    receipt = StructuralEmpiricalAdmission(
        typed_state=PUBLIC_STATE_BY_DECISION[decision],
        authority_snapshot_refs=authority_refs,
        dependency_refs=deps,
        producer_replay_locator_or_reference_root=producer_replay_locator_or_reference_root,
        **fields,
    )
    v553 = project_admission_to_v553_participant(
        receipt, role="STRUCTURAL_EMPIRICAL_ADMISSION", ordinal=0
    )
    if decision == "ADMITTED":
        projection = project_admission_to_m1_direct_basis(receipt)
        projection_hash = semantic_hash(projection)
    else:
        projection = None
        projection_hash = None
    return AdmissionEvaluation(
        decision_state=decision,
        reason_code=reason,
        receipt=receipt,
        blocking_refs=tuple(sorted(blockers, key=lambda r: r.key)),
        m1_direct_projection=projection,
        m1_projection_hash=projection_hash,
        v553_participant_projection=v553,
    )


def project_admission_to_v553_participant(
    receipt: StructuralEmpiricalAdmission,
    *,
    role: str,
    ordinal: int,
) -> Mapping[str, Any]:
    """Project only the frozen SCR553 participant envelope; no temporal decision."""
    if not isinstance(receipt, StructuralEmpiricalAdmission):
        raise StructuralAdmissionProjectionError("V553 ingress requires StructuralEmpiricalAdmission")
    if not isinstance(role, str) or not role.strip():
        raise StructuralAdmissionProjectionError("V553 participant role must be non-empty")
    if not isinstance(ordinal, int) or isinstance(ordinal, bool) or ordinal < 0:
        raise StructuralAdmissionProjectionError("V553 participant ordinal must be nonnegative integer")
    projection = {
        "role": role.strip(),
        "ordinal": ordinal,
        "structural_empirical_admission_ref": receipt.ref.as_dict(),
    }
    if tuple(projection) != V553_PARTICIPANT_FIELDS:
        raise StructuralAdmissionProjectionError("V553 participant projection contract drift")
    return MappingProxyType(projection)


def project_admission_to_m1_direct_basis(
    receipt: StructuralEmpiricalAdmission,
) -> Mapping[str, Any]:
    """Lossless P06 projection into frozen M1 direct-admission consumer slots.

    This is not a direct-V554 eligibility decision. SCR553/SCR554 remain owners
    of temporal requirement, signature, equivalence, dedup, precedence and
    F1/F2/B1.
    """
    if not isinstance(receipt, StructuralEmpiricalAdmission):
        raise StructuralAdmissionProjectionError("M1 projection requires StructuralEmpiricalAdmission")
    if receipt.admission_decision_state != "ADMITTED":
        raise StructuralAdmissionProjectionError("only ADMITTED may become direct M1 basis candidate")
    auth = authority_ref(receipt.admission_authority_ref)
    projection = {
        "structural_empirical_admission_id": receipt.object_id,
        "structural_empirical_admission_content_hash": receipt.content_hash,
        "admission_authority_id": auth.authority_id,
        "admission_authority_version": auth.authority_version,
        "admission_authority_hash": auth.authority_content_hash,
        "admission_decision_state": receipt.admission_decision_state,
        "focal_structural_proposition_ref": canonicalize(receipt.focal_structural_proposition_ref),
        "structural_semantic_identity_refs": canonicalize(receipt.structural_semantic_identity_refs),
        "native_scope_identity_refs": canonicalize(receipt.native_scope_identity_refs),
        "target_use_permission_refs": canonicalize(receipt.target_use_permission_refs),
        "effective_time_or_interval_refs_required_by_target_use": canonicalize(receipt.effective_time_or_interval_refs_required_by_target_use),
        "source_universe_refs": canonicalize(receipt.source_universe_refs),
        "estimand_refs": canonicalize(receipt.estimand_refs),
        "measure_and_weight_authority_refs": canonicalize(receipt.measure_and_weight_authority_refs),
        "applicable_negative_denial_noncomparability_refs": canonicalize(receipt.applicable_negative_denial_noncomparability_refs),
        "interpretation_critical_authority_refs": canonicalize(receipt.interpretation_critical_authority_refs),
        "producer_replay_locator_or_reference_root": canonicalize(receipt.producer_replay_locator_or_reference_root),
    }
    if tuple(projection) != M1_DIRECT_PROJECTION_FIELDS:
        raise StructuralAdmissionProjectionError("M1 direct projection contract drift")
    return MappingProxyType(projection)


__all__ = [
    "I04_CONTRACT_ID", "P06_RULE_CONTRACT_ID", "DECISION_PRECEDENCE", "DECISION_MATRIX",
    "P06_NONPOSITIVE_DECISIONS", "POSITIVE_DECISION", "PUBLIC_STATE_BY_DECISION",
    "V553_PARTICIPANT_FIELDS", "V553_INGRESS_CONTRACT", "M1_DIRECT_PROJECTION_FIELDS",
    "StructuralAdmissionError", "StructuralAdmissionProjectionError", "AdmissionCondition",
    "RequiredAuthorityBinding", "StructuralAdmissionRule", "StructuralAdmissionRequest",
    "AdmissionEvaluation", "evaluate_structural_empirical_admission",
    "project_admission_to_v553_participant", "project_admission_to_m1_direct_basis",
]
