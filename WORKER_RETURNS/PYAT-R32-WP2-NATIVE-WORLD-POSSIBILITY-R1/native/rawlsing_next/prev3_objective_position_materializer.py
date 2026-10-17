"""Mechanical PRE-V3 objective-position materializer.

Implements only the HQ-adopted D03 contract:
PREV3_OBJECTIVE_POSITION_MATERIALIZER_CONTRACT@1.0.0.

This module is deliberately not a position classifier or semantic owner.  It
validates exact immutable input shape, preserves typed nonpositive outcomes,
and content-addresses an already-authorized objective position assertion.
It cannot infer position truth from labels, demographics, geometry, world-root
membership, downstream need, or V3/person state.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_empirical_authority import (
    Pre553AuthorityError,
    require_exact_authority_ref,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    canonicalize,
    semantic_hash,
)

CONTRACT_ID = "PREV3_OBJECTIVE_POSITION_MATERIALIZER_CONTRACT@1.0.0"
FACT_SCHEMA_ID = "PREV3_OBJECTIVE_POSITION_FACT@1.0.0"
FACT_REF_KIND = "PREV3_OBJECTIVE_POSITION_FACT"
POSITIVE_STATE = "POSITION_FACT_AUTHORIZED"

M2_SOURCE_SLOT = "source_structural_position_ref"
M2_RECEIVING_SLOT = "receiving_structural_position_ref"
_M2_SLOTS = frozenset({M2_SOURCE_SLOT, M2_RECEIVING_SLOT})

_FORBIDDEN_SELECTOR_TOKENS = frozenset(
    {"LATEST", "DEFAULT", "FUZZY", "NEAREST", "SEMVER", "SEMVER_FALLBACK", "*"}
)
_FORBIDDEN_PERSON_TOKENS = (
    "PERSON_STATE",
    "PERSONA",
    "V3_SUBJECT",
    "V3_PERSON",
    "PSYCH",
    "BELIEF",
    "PREFERENCE",
    "MOTIVE",
    "TRAIT",
)
_FORBIDDEN_ALLOWED_USE_TOKENS = (
    "PERSON_STATE",
    "PERSONA",
    "V3_",
    "PSYCH",
    "BELIEF",
    "PREFERENCE",
    "MOTIVE",
    "TRAIT",
    "DEVELOPMENT",
)


class PositionMaterializerError(ValueError):
    """The bounded D03 materialization contract failed closed."""


class PositionResultState(str, Enum):
    POSITION_FACT_AUTHORIZED = "POSITION_FACT_AUTHORIZED"
    EXPLICIT_NEGATIVE_OBJECTIVE_POSITION = "EXPLICIT_NEGATIVE_OBJECTIVE_POSITION"
    UNAVAILABLE = "UNAVAILABLE"
    VALID_EMPTY = "VALID_EMPTY"
    MISSING_POSITION_PRODUCER_AUTHORITY = "MISSING_POSITION_PRODUCER_AUTHORITY"
    MISSING_POSITION_SEMANTIC_AUTHORITY = "MISSING_POSITION_SEMANTIC_AUTHORITY"
    MISSING_ROLE_AUTHORITY = "MISSING_ROLE_AUTHORITY"
    MISSING_SOURCE_OR_CLAIM_AUTHORITY = "MISSING_SOURCE_OR_CLAIM_AUTHORITY"
    MISSING_REQUIRED_EVIDENCE = "MISSING_REQUIRED_EVIDENCE"
    IDENTITY_UNRESOLVED = "IDENTITY_UNRESOLVED"
    APPLICABILITY_UNRESOLVED = "APPLICABILITY_UNRESOLVED"
    USE_DENIED = "USE_DENIED"
    MISSING_VALID_TIME_AUTHORITY = "MISSING_VALID_TIME_AUTHORITY"
    CURRENTNESS_UNRESOLVED = "CURRENTNESS_UNRESOLVED"
    STALE_OR_HISTORICAL_NONCURRENT = "STALE_OR_HISTORICAL_NONCURRENT"
    NONCOMPARABLE = "NONCOMPARABLE"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    INTEGRITY_FAILURE = "INTEGRITY_FAILURE"


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PositionMaterializerError(f"{name} must be non-empty text")
    text = value.strip()
    upper = text.upper()
    if upper in _FORBIDDEN_SELECTOR_TOKENS or upper.startswith(
        ("LATEST:", "DEFAULT:", "FUZZY:", "NEAREST:", "SEMVER:")
    ):
        raise PositionMaterializerError(f"{name} may not use mutable/fuzzy selector syntax")
    return text


def _exact_ref(value: Any, name: str) -> ExactRef:
    if not isinstance(value, ExactRef):
        raise PositionMaterializerError(f"{name} must be ExactRef")
    _text(value.kind, f"{name}.kind")
    _text(value.object_id, f"{name}.object_id")
    return value


def _authority_ref(value: Any, name: str) -> AuthorityRef:
    if not isinstance(value, AuthorityRef):
        raise PositionMaterializerError(f"{name} must be AuthorityRef")
    try:
        return require_exact_authority_ref(value)
    except Pre553AuthorityError as exc:
        raise PositionMaterializerError(str(exc)) from exc


def _refs(
    values: Iterable[ExactRef],
    name: str,
    *,
    require_nonempty: bool,
) -> tuple[ExactRef, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise PositionMaterializerError(f"{name} must be an iterable of ExactRef")
    refs = tuple(values)
    if require_nonempty and not refs:
        raise PositionMaterializerError(f"{name} must not be empty")
    if any(not isinstance(ref, ExactRef) for ref in refs):
        raise PositionMaterializerError(f"{name} must contain only ExactRef")
    keys = [ref.key for ref in refs]
    if len(keys) != len(set(keys)):
        raise PositionMaterializerError(f"{name} contains duplicate exact refs")
    return tuple(sorted(refs, key=lambda ref: ref.key))


def _uses(values: Iterable[str]) -> tuple[str, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise PositionMaterializerError("allowed_uses must be an iterable of exact use ids")
    normalized = tuple(sorted({_text(value, "allowed_use") for value in values}))
    if not normalized:
        raise PositionMaterializerError("allowed_uses must not be empty")
    for value in normalized:
        upper = value.upper()
        if any(token in upper for token in _FORBIDDEN_ALLOWED_USE_TOKENS):
            raise PositionMaterializerError(
                "allowed_uses may contain objective PRE-V3 uses only; person/V3 uses are forbidden"
            )
    return normalized


def _reject_person_bootstrap(ref: ExactRef, name: str) -> None:
    material = f"{ref.kind}|{ref.object_id}".upper()
    if any(token in material for token in _FORBIDDEN_PERSON_TOKENS):
        raise PositionMaterializerError(
            f"{name} may not use V3/person/psychological identity as objective position evidence"
        )


@dataclass(frozen=True, slots=True)
class ObjectivePositionInput:
    """Complete immutable positive tuple from D03 section 3.

    The tuple carries external authority identities; this materializer does not
    issue, select, or widen those authorities.
    """

    materializer_implementation_ref: ExactRef
    position_producer_authority_ref: AuthorityRef
    position_semantic_authority_ref: AuthorityRef
    entity_or_actor_ref: ExactRef
    objective_position_role_identity_ref: ExactRef
    source_universe_ref: ExactRef
    source_release_ref: ExactRef
    source_claim_ref: ExactRef
    source_claim_authority_ref: AuthorityRef
    supporting_evidence_refs: tuple[ExactRef, ...]
    position_role_receipt_ref: ExactRef | None
    position_role_not_applicable_authority_ref: AuthorityRef | None
    target_outcome_firewall_ref: ExactRef | None
    applicability_authority_ref: AuthorityRef
    applicability_receipt_ref: ExactRef
    permission_authority_ref: AuthorityRef
    allowed_uses: tuple[str, ...]
    negative_ceiling_ref: ExactRef
    valid_time_authority_ref: AuthorityRef
    valid_time_basis_ref: ExactRef
    currentness_authority_ref: AuthorityRef
    currentness_receipt_ref: ExactRef
    provenance_refs: tuple[ExactRef, ...]
    dependency_refs: tuple[ExactRef, ...]
    replay_authority_ref: AuthorityRef
    predecessor_position_fact_ref: ExactRef | None = None

    def __post_init__(self) -> None:
        exact_fields = (
            "materializer_implementation_ref",
            "entity_or_actor_ref",
            "objective_position_role_identity_ref",
            "source_universe_ref",
            "source_release_ref",
            "source_claim_ref",
            "applicability_receipt_ref",
            "negative_ceiling_ref",
            "valid_time_basis_ref",
            "currentness_receipt_ref",
        )
        authority_fields = (
            "position_producer_authority_ref",
            "position_semantic_authority_ref",
            "source_claim_authority_ref",
            "applicability_authority_ref",
            "permission_authority_ref",
            "valid_time_authority_ref",
            "currentness_authority_ref",
            "replay_authority_ref",
        )
        for name in exact_fields:
            object.__setattr__(self, name, _exact_ref(getattr(self, name), name))
        for name in authority_fields:
            object.__setattr__(self, name, _authority_ref(getattr(self, name), name))

        evidence = _refs(
            self.supporting_evidence_refs,
            "supporting_evidence_refs",
            require_nonempty=True,
        )
        provenance = _refs(self.provenance_refs, "provenance_refs", require_nonempty=True)
        dependencies = _refs(self.dependency_refs, "dependency_refs", require_nonempty=True)
        object.__setattr__(self, "supporting_evidence_refs", evidence)
        object.__setattr__(self, "provenance_refs", provenance)
        object.__setattr__(self, "dependency_refs", dependencies)
        object.__setattr__(self, "allowed_uses", _uses(self.allowed_uses))

        role_receipt = self.position_role_receipt_ref
        role_na = self.position_role_not_applicable_authority_ref
        if (role_receipt is None) == (role_na is None):
            raise PositionMaterializerError(
                "exactly one role-authority path is required: position_role_receipt_ref XOR "
                "position_role_not_applicable_authority_ref"
            )
        if role_receipt is not None:
            object.__setattr__(
                self,
                "position_role_receipt_ref",
                _exact_ref(role_receipt, "position_role_receipt_ref"),
            )
        if role_na is not None:
            object.__setattr__(
                self,
                "position_role_not_applicable_authority_ref",
                _authority_ref(role_na, "position_role_not_applicable_authority_ref"),
            )
        if self.target_outcome_firewall_ref is not None:
            object.__setattr__(
                self,
                "target_outcome_firewall_ref",
                _exact_ref(self.target_outcome_firewall_ref, "target_outcome_firewall_ref"),
            )
        if self.predecessor_position_fact_ref is not None:
            predecessor = _exact_ref(
                self.predecessor_position_fact_ref, "predecessor_position_fact_ref"
            )
            if predecessor.kind != FACT_REF_KIND:
                raise PositionMaterializerError(
                    "predecessor_position_fact_ref must be PREV3_OBJECTIVE_POSITION_FACT"
                )
            object.__setattr__(self, "predecessor_position_fact_ref", predecessor)

        _reject_person_bootstrap(self.entity_or_actor_ref, "entity_or_actor_ref")
        _reject_person_bootstrap(
            self.objective_position_role_identity_ref,
            "objective_position_role_identity_ref",
        )

    def canonical_fact_material(self) -> Mapping[str, Any]:
        return canonicalize(
            {
                "schema": FACT_SCHEMA_ID,
                "state": POSITIVE_STATE,
                "materializer_implementation_ref": self.materializer_implementation_ref,
                "position_producer_authority_ref": self.position_producer_authority_ref,
                "position_semantic_authority_ref": self.position_semantic_authority_ref,
                "entity_or_actor_ref": self.entity_or_actor_ref,
                "objective_position_role_identity_ref": self.objective_position_role_identity_ref,
                "source_universe_ref": self.source_universe_ref,
                "source_release_ref": self.source_release_ref,
                "source_claim_ref": self.source_claim_ref,
                "source_claim_authority_ref": self.source_claim_authority_ref,
                "supporting_evidence_refs": list(self.supporting_evidence_refs),
                "position_role_receipt_ref": self.position_role_receipt_ref,
                "position_role_not_applicable_authority_ref":
                    self.position_role_not_applicable_authority_ref,
                "target_outcome_firewall_ref": self.target_outcome_firewall_ref,
                "applicability_authority_ref": self.applicability_authority_ref,
                "applicability_receipt_ref": self.applicability_receipt_ref,
                "permission_authority_ref": self.permission_authority_ref,
                "allowed_uses": list(self.allowed_uses),
                "negative_ceiling_ref": self.negative_ceiling_ref,
                "valid_time_authority_ref": self.valid_time_authority_ref,
                "valid_time_basis_ref": self.valid_time_basis_ref,
                "currentness_authority_ref": self.currentness_authority_ref,
                "currentness_receipt_ref": self.currentness_receipt_ref,
                "provenance_refs": list(self.provenance_refs),
                "dependency_refs": list(self.dependency_refs),
                "replay_authority_ref": self.replay_authority_ref,
                "predecessor_position_fact_ref": self.predecessor_position_fact_ref,
            }
        )


@dataclass(frozen=True, slots=True)
class ObjectivePositionFact:
    state: PositionResultState
    fact_ref: ExactRef
    canonical_material: Mapping[str, Any]

    def __post_init__(self) -> None:
        if self.state is not PositionResultState.POSITION_FACT_AUTHORIZED:
            raise PositionMaterializerError("ObjectivePositionFact is positive-only")
        if self.fact_ref.kind != FACT_REF_KIND:
            raise PositionMaterializerError("fact_ref kind mismatch")
        expected_hash = semantic_hash(self.canonical_material)
        if self.fact_ref.content_hash != expected_hash:
            raise PositionMaterializerError("fact_ref hash does not match canonical material")
        if self.fact_ref.object_id != f"PREV3POS:{expected_hash}":
            raise PositionMaterializerError("fact_ref object_id does not match PREV3POS identity")


@dataclass(frozen=True, slots=True)
class NonpositivePositionResult:
    state: PositionResultState
    reason_ref: ExactRef
    evidence_refs: tuple[ExactRef, ...] = ()
    explicit_negative_authority_ref: AuthorityRef | None = None

    def __post_init__(self) -> None:
        if self.state is PositionResultState.POSITION_FACT_AUTHORIZED:
            raise PositionMaterializerError("positive state requires ObjectivePositionFact")
        object.__setattr__(self, "reason_ref", _exact_ref(self.reason_ref, "reason_ref"))
        object.__setattr__(
            self,
            "evidence_refs",
            _refs(self.evidence_refs, "evidence_refs", require_nonempty=False),
        )
        if self.state is PositionResultState.EXPLICIT_NEGATIVE_OBJECTIVE_POSITION:
            if self.explicit_negative_authority_ref is None or not self.evidence_refs:
                raise PositionMaterializerError(
                    "explicit negative position requires exact negative authority and evidence"
                )
            object.__setattr__(
                self,
                "explicit_negative_authority_ref",
                _authority_ref(
                    self.explicit_negative_authority_ref,
                    "explicit_negative_authority_ref",
                ),
            )
        elif self.explicit_negative_authority_ref is not None:
            raise PositionMaterializerError(
                "nonnegative nonpositive states may not carry explicit negative authority"
            )

    @property
    def fact_ref(self) -> None:
        return None


def materialize_objective_position(
    input_tuple: ObjectivePositionInput,
    *,
    require_target_outcome_firewall: bool = False,
) -> ObjectivePositionFact:
    """Content-address a fully authorized tuple without inventing missing truth.

    Authority competence/currentness is external to this mechanical producer.
    Callers must supply the exact refs/receipts issued by competent owners.  This
    function never resolves "latest" authority and never substitutes downstream
    need or source labels for any missing tuple member.
    """
    if not isinstance(input_tuple, ObjectivePositionInput):
        raise PositionMaterializerError("ObjectivePositionInput required")
    if require_target_outcome_firewall and input_tuple.target_outcome_firewall_ref is None:
        raise PositionMaterializerError(
            "constitutive role adjudication requires target_outcome_firewall_ref"
        )
    material = input_tuple.canonical_fact_material()
    fact_hash = semantic_hash(material)
    fact_ref = ExactRef(FACT_REF_KIND, f"PREV3POS:{fact_hash}", fact_hash)
    return ObjectivePositionFact(
        state=PositionResultState.POSITION_FACT_AUTHORIZED,
        fact_ref=fact_ref,
        canonical_material=material,
    )


def replay_objective_position(
    input_tuple: ObjectivePositionInput,
    expected_fact_ref: ExactRef,
    *,
    require_target_outcome_firewall: bool = False,
) -> ObjectivePositionFact:
    """Re-materialize and prove deterministic identity equality."""
    expected = _exact_ref(expected_fact_ref, "expected_fact_ref")
    replayed = materialize_objective_position(
        input_tuple,
        require_target_outcome_firewall=require_target_outcome_firewall,
    )
    if replayed.fact_ref != expected:
        raise PositionMaterializerError("deterministic replay identity mismatch")
    return replayed


def typed_nonpositive_result(
    state: PositionResultState | str,
    *,
    reason_ref: ExactRef,
    evidence_refs: Iterable[ExactRef] = (),
    explicit_negative_authority_ref: AuthorityRef | None = None,
) -> NonpositivePositionResult:
    try:
        typed_state = state if isinstance(state, PositionResultState) else PositionResultState(state)
    except (TypeError, ValueError) as exc:
        raise PositionMaterializerError("unknown D03 result state") from exc
    return NonpositivePositionResult(
        state=typed_state,
        reason_ref=reason_ref,
        evidence_refs=tuple(evidence_refs),
        explicit_negative_authority_ref=explicit_negative_authority_ref,
    )


def m2_position_ref_handoff(
    fact: ObjectivePositionFact,
    *,
    slot: str,
    requested_use: str,
    allowed_uses: Iterable[str],
) -> Mapping[str, Any]:
    """Prepare an exact-ref handoff only; never bypass M2 route/F1 authority."""
    if not isinstance(fact, ObjectivePositionFact):
        raise PositionMaterializerError("positive ObjectivePositionFact required for M2 handoff")
    if slot not in _M2_SLOTS:
        raise PositionMaterializerError("slot must be an exact M2 structural-position slot")
    requested = _text(requested_use, "requested_use")
    allowed = _uses(allowed_uses)
    if requested not in allowed:
        raise PositionMaterializerError("requested M2 use is not in the fact permission ceiling")
    return {
        slot: fact.fact_ref.as_dict(),
        "requested_use": requested,
        "d03_handoff_only": True,
        "m2_route_authority_still_required": True,
        "m2_f1_closure_still_required": True,
    }


__all__ = [
    "CONTRACT_ID",
    "FACT_SCHEMA_ID",
    "FACT_REF_KIND",
    "POSITIVE_STATE",
    "M2_SOURCE_SLOT",
    "M2_RECEIVING_SLOT",
    "PositionMaterializerError",
    "PositionResultState",
    "ObjectivePositionInput",
    "ObjectivePositionFact",
    "NonpositivePositionResult",
    "materialize_objective_position",
    "replay_objective_position",
    "typed_nonpositive_result",
    "m2_position_ref_handoff",
]
