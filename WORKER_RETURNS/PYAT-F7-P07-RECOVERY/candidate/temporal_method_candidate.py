"""TEST-ONLY sourcefree candidate for the recoverable pure F7 temporal core.

This module is not a production F7 owner, not a TEMPORAL_RELATION_RECEIPT
producer of record, and not a P07 owner.  It contains no historical nested
sealed resolver and imports no native extension.

It performs only four bounded operations over exact material supplied by
callers:

* exact point/closed-interval geometry over already-authorized time extents;
* explicit comparability-attestation validation over present current authority
  kinds;
* cross-universe source-equivalence consumption through the present current
  outer source-relation resolver;
* exact as-of version eligibility without latest/default/fuzzy selection.

The candidate does not infer scientific comparability from equal numbers,
shared labels, wave indexes, as-of timestamps, or cross-wave plug compatibility.
It cannot mint an EE12 comparability authority and deliberately refuses the
unissued historical ``TEMPORAL_COMPARABILITY`` kind because that kind is absent
from the current closed authority-kind set.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_authority import (
    AUTHORITY_KINDS,
    AuthorityRegistry,
    Pre553AuthorityError,
    require_positive_authority,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    Pre553IntegrityError,
    authority_ref,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_source_relations import (
    SourceRelationError,
    SourceRelationResolver,
)

CANDIDATE_SCHEMA = "PYAT_F7_P07_TEMPORAL_METHOD_CANDIDATE@1.0.0"
CANDIDATE_STATUS = (
    "TEST_ONLY_SOURCEFREE_CANDIDATE__NO_CURRENT_RECEIVER__NO_PRODUCTION_AUTHORITY"
)
TEMPORAL_EVIDENCE_KIND = "TEMPORAL_EVIDENCE"
TIME_ORDER_OPERATION = "TEMPORAL_POSITION_ORDER"
COMPARISON_OPERATION = "TEMPORAL_BOUND_QUANTITY_DIFFERENCE"
SOURCE_EQUIVALENCE_KIND = "SOURCE_SEMANTIC_EQUIVALENCE"
SOURCE_EQUIVALENCE_OPERATION = "SEMANTIC_EQUIVALENCE_ADMISSION"
SOURCE_EQUIVALENCE_SCOPE = "EXACT_BOUND_UNIVERSE_PAIR"

CANDIDATE_MINIMUM_SURFACES = (
    "construct_question_semantics",
    "response_surface_and_scale",
    "instrument_release_and_route",
    "target_population_and_geography",
    "estimand",
    "measure",
    "weight_design",
    "time_representation_and_grain",
)

_SURFACE_ANCHOR_FIELDS = {
    "construct_question_semantics": "construct_ref",
    "response_surface_and_scale": "response_surface_ref",
    "instrument_release_and_route": "route_ref",
    "target_population_and_geography": "population_ref",
    "estimand": "estimand_ref",
    "measure": "measure_ref",
    "weight_design": "weight_ref",
    "time_representation_and_grain": "temporal_time_ref",
}

_TIME_REPRESENTATIONS = frozenset({"POINT", "CLOSED_INTERVAL"})
_ATTESTATION_STATES = frozenset({"SATISFIED", "NOT_SATISFIED"})
_RELATION_STATE_PRECEDENCE = (
    "TEMPORAL_INSUFFICIENT_AUTHORITY",
    "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT",
    "TEMPORAL_NONCOMPARABLE",
    "TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION",
    "TEMPORAL_COMPARABLE_NO_DIRECTION",
    "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED",
)


class CandidateTemporalError(Pre553IntegrityError):
    """The sourcefree candidate cannot lawfully produce the requested result."""


class CandidateTemporalIntegrityError(CandidateTemporalError):
    """Exact identity, ref, geometry, or closed-shape law is violated."""


class CandidateTemporalNotComparable(CandidateTemporalError):
    """The candidate refused a comparison; no delta or direction is produced."""

    def __init__(self, decision: "TemporalMethodDecision") -> None:
        super().__init__(
            f"temporal comparison refused: {decision.relation_state} "
            f"({', '.join(decision.reasons)})")
        self.decision = decision


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CandidateTemporalIntegrityError(f"{name} must be a non-empty string")
    return value.strip()


def _exact_ref(value: Any, name: str) -> ExactRef:
    try:
        return exact_ref(value, name)
    except Pre553IntegrityError as exc:
        raise CandidateTemporalIntegrityError(str(exc)) from exc


def _exact_authority(value: Any, name: str) -> AuthorityRef:
    try:
        return authority_ref(value, name)
    except Pre553IntegrityError as exc:
        raise CandidateTemporalIntegrityError(str(exc)) from exc


def _exact_fraction(value: Any, name: str) -> Fraction:
    if isinstance(value, bool) or isinstance(value, float) or value is None:
        raise CandidateTemporalIntegrityError(
            f"{name} must be an exact int/Decimal/Fraction, not {type(value).__name__}")
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise CandidateTemporalIntegrityError(f"{name} must be finite")
        return Fraction(value)
    if isinstance(value, Fraction):
        return value
    raise CandidateTemporalIntegrityError(
        f"{name} must be an exact int/Decimal/Fraction, not {type(value).__name__}")


def _explicit_scope_contains(scope_value: Any, target: ExactRef) -> bool:
    if scope_value is None or isinstance(scope_value, (str, bytes, bytearray)):
        return False
    target_json = canonical_json(target.as_dict())
    if isinstance(scope_value, Mapping):
        return canonical_json(scope_value) == target_json
    if isinstance(scope_value, Sequence):
        return target_json in {canonical_json(item) for item in scope_value}
    return False


@dataclass(frozen=True)
class TimeExtent:
    time_ref: ExactRef
    authority_ref: AuthorityRef
    grain_ref: ExactRef
    representation: str
    start: Any
    end: Any

    def __post_init__(self) -> None:
        object.__setattr__(self, "time_ref", _exact_ref(self.time_ref, "time_ref"))
        object.__setattr__(
            self, "authority_ref", _exact_authority(self.authority_ref, "authority_ref"))
        object.__setattr__(self, "grain_ref", _exact_ref(self.grain_ref, "grain_ref"))
        representation = _text(self.representation, "representation")
        if representation not in _TIME_REPRESENTATIONS:
            raise CandidateTemporalIntegrityError(
                f"unknown time representation: {representation}")
        object.__setattr__(self, "representation", representation)
        start = _exact_fraction(self.start, "start")
        end = _exact_fraction(self.end, "end")
        if start > end:
            raise CandidateTemporalIntegrityError("time extent start exceeds end")
        if representation == "POINT" and start != end:
            raise CandidateTemporalIntegrityError("POINT extent must have start == end")
        object.__setattr__(self, "start", start)
        object.__setattr__(self, "end", end)

    def as_material(self) -> dict[str, Any]:
        return {
            "time_ref": self.time_ref.as_dict(),
            "authority_ref": self.authority_ref.as_dict(),
            "grain_ref": self.grain_ref.as_dict(),
            "representation": self.representation,
            "start": canonicalize(self.start),
            "end": canonicalize(self.end),
        }

    @classmethod
    def point(
        cls,
        *,
        time_ref: ExactRef,
        authority_ref: AuthorityRef,
        grain_ref: ExactRef,
        value: Any,
    ) -> "TimeExtent":
        return cls(
            time_ref=time_ref,
            authority_ref=authority_ref,
            grain_ref=grain_ref,
            representation="POINT",
            start=value,
            end=value,
        )

    @classmethod
    def closed_interval(
        cls,
        *,
        time_ref: ExactRef,
        authority_ref: AuthorityRef,
        grain_ref: ExactRef,
        start: Any,
        end: Any,
    ) -> "TimeExtent":
        return cls(
            time_ref=time_ref,
            authority_ref=authority_ref,
            grain_ref=grain_ref,
            representation="CLOSED_INTERVAL",
            start=start,
            end=end,
        )


@dataclass(frozen=True)
class TemporalAnchor:
    anchor_ref: ExactRef
    observation_ref: ExactRef
    source_universe_ref: ExactRef
    construct_ref: ExactRef
    response_surface_ref: ExactRef
    route_ref: ExactRef
    population_ref: ExactRef
    estimand_ref: ExactRef
    measure_ref: ExactRef
    weight_ref: ExactRef
    effective_time: TimeExtent
    quantity_ref: ExactRef | None = None
    quantity_value: Any = None

    def __post_init__(self) -> None:
        for name in (
            "anchor_ref",
            "observation_ref",
            "source_universe_ref",
            "construct_ref",
            "response_surface_ref",
            "route_ref",
            "population_ref",
            "estimand_ref",
            "measure_ref",
            "weight_ref",
        ):
            object.__setattr__(self, name, _exact_ref(getattr(self, name), name))
        if not isinstance(self.effective_time, TimeExtent):
            raise CandidateTemporalIntegrityError("effective_time must be TimeExtent")
        if self.quantity_value is None:
            if self.quantity_ref is not None:
                raise CandidateTemporalIntegrityError(
                    "quantity_ref requires an exact quantity_value")
        else:
            if self.quantity_ref is None:
                raise CandidateTemporalIntegrityError(
                    "quantity_value requires an exact quantity_ref")
            object.__setattr__(
                self, "quantity_ref", _exact_ref(self.quantity_ref, "quantity_ref"))
            object.__setattr__(
                self, "quantity_value", _exact_fraction(self.quantity_value, "quantity_value"))

    def temporal_time_ref(self) -> ExactRef:
        return self.effective_time.time_ref

    def as_material(self) -> dict[str, Any]:
        return {
            "anchor_ref": self.anchor_ref.as_dict(),
            "observation_ref": self.observation_ref.as_dict(),
            "source_universe_ref": self.source_universe_ref.as_dict(),
            "construct_ref": self.construct_ref.as_dict(),
            "response_surface_ref": self.response_surface_ref.as_dict(),
            "route_ref": self.route_ref.as_dict(),
            "population_ref": self.population_ref.as_dict(),
            "estimand_ref": self.estimand_ref.as_dict(),
            "measure_ref": self.measure_ref.as_dict(),
            "weight_ref": self.weight_ref.as_dict(),
            "effective_time": self.effective_time.as_material(),
            "quantity_ref": self.quantity_ref.as_dict() if self.quantity_ref else None,
            "quantity_value": (
                canonicalize(self.quantity_value) if self.quantity_value is not None else None),
        }


@dataclass(frozen=True)
class ComparabilityAttestation:
    surface: str
    left_ref: ExactRef
    right_ref: ExactRef
    authority_ref: AuthorityRef
    authority_kind: str
    operation: str
    state: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "surface", _text(self.surface, "surface"))
        object.__setattr__(self, "left_ref", _exact_ref(self.left_ref, "left_ref"))
        object.__setattr__(self, "right_ref", _exact_ref(self.right_ref, "right_ref"))
        object.__setattr__(
            self, "authority_ref", _exact_authority(self.authority_ref, "authority_ref"))
        object.__setattr__(
            self, "authority_kind", _text(self.authority_kind, "authority_kind"))
        object.__setattr__(self, "operation", _text(self.operation, "operation"))
        state = _text(self.state, "state")
        if state not in _ATTESTATION_STATES:
            raise CandidateTemporalIntegrityError(f"unknown attestation state: {state}")
        object.__setattr__(self, "state", state)

    def as_material(self) -> dict[str, Any]:
        return {
            "surface": self.surface,
            "left_ref": self.left_ref.as_dict(),
            "right_ref": self.right_ref.as_dict(),
            "authority_ref": self.authority_ref.as_dict(),
            "authority_kind": self.authority_kind,
            "operation": self.operation,
            "state": self.state,
        }


@dataclass(frozen=True)
class SourceEquivalenceEvidence:
    resolver: SourceRelationResolver
    relation_ref: ExactRef
    operation_scope: str
    effective_scope: str
    target_use: str

    def __post_init__(self) -> None:
        if type(self.resolver) is not SourceRelationResolver:
            raise CandidateTemporalIntegrityError(
                "source equivalence requires the present concrete outer "
                "SourceRelationResolver; duck-typed owners are refused")
        object.__setattr__(
            self, "relation_ref", _exact_ref(self.relation_ref, "relation_ref"))
        object.__setattr__(
            self, "operation_scope", _text(self.operation_scope, "operation_scope"))
        object.__setattr__(
            self, "effective_scope", _text(self.effective_scope, "effective_scope"))
        object.__setattr__(self, "target_use", _text(self.target_use, "target_use"))


@dataclass(frozen=True)
class TemporalComparabilityProfile:
    governed_use_ref: ExactRef
    required_surfaces: tuple[str, ...]
    attestations: tuple[ComparabilityAttestation, ...]
    source_equivalence: SourceEquivalenceEvidence | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "governed_use_ref", _exact_ref(self.governed_use_ref, "governed_use_ref"))
        surfaces = tuple(_text(surface, "required_surface")
                         for surface in self.required_surfaces)
        if not surfaces:
            raise CandidateTemporalIntegrityError("required_surfaces may not be empty")
        if len(surfaces) != len(set(surfaces)):
            raise CandidateTemporalIntegrityError("required_surfaces must be unique")
        object.__setattr__(self, "required_surfaces", surfaces)
        attestations = tuple(self.attestations)
        if not all(isinstance(a, ComparabilityAttestation) for a in attestations):
            raise CandidateTemporalIntegrityError(
                "attestations must be ComparabilityAttestation")
        attestation_surfaces = tuple(a.surface for a in attestations)
        if len(attestation_surfaces) != len(set(attestation_surfaces)):
            raise CandidateTemporalIntegrityError(
                "exactly one attestation per surface is allowed")
        extra = set(attestation_surfaces) - set(surfaces)
        if extra:
            raise CandidateTemporalIntegrityError(
                f"attestations contain non-required surfaces: {sorted(extra)}")
        if self.source_equivalence is not None and not isinstance(
                self.source_equivalence, SourceEquivalenceEvidence):
            raise CandidateTemporalIntegrityError(
                "source_equivalence must be SourceEquivalenceEvidence or None")


@dataclass(frozen=True)
class TemporalMethodDecision:
    comparability_status: str
    relation_state: str
    reasons: tuple[str, ...]
    satisfied_surfaces: tuple[str, ...]
    failed_surfaces: tuple[str, ...]
    geometry: Mapping[str, Any]
    direction_claim: str
    delta: Mapping[str, Any] | None
    source_equivalence_ref: Mapping[str, str] | None
    authority_snapshot_refs: tuple[Mapping[str, str], ...]
    governed_use_ref: Mapping[str, str]
    left_anchor: Mapping[str, Any]
    right_anchor: Mapping[str, Any]
    candidate_only: bool
    receipt_hash: str

    @property
    def comparable(self) -> bool:
        return self.comparability_status == "COMPARABLE"

    def as_material(self) -> dict[str, Any]:
        return {
            "schema": CANDIDATE_SCHEMA,
            "status": CANDIDATE_STATUS,
            "candidate_only": self.candidate_only,
            "governed_use_ref": dict(self.governed_use_ref),
            "left_anchor": canonicalize(self.left_anchor),
            "right_anchor": canonicalize(self.right_anchor),
            "comparability_status": self.comparability_status,
            "relation_state": self.relation_state,
            "reasons": list(self.reasons),
            "satisfied_surfaces": list(self.satisfied_surfaces),
            "failed_surfaces": list(self.failed_surfaces),
            "geometry": canonicalize(self.geometry),
            "direction_claim": self.direction_claim,
            "delta": canonicalize(self.delta) if self.delta is not None else None,
            "source_equivalence_ref": (
                dict(self.source_equivalence_ref) if self.source_equivalence_ref else None),
            "authority_snapshot_refs": [dict(ref) for ref in self.authority_snapshot_refs],
        }

    def replay_identity(self) -> str:
        return semantic_hash(self.as_material())


@dataclass(frozen=True)
class AsOfVersion:
    version_ref: ExactRef
    published: TimeExtent
    valid_from: TimeExtent | None = None
    revoked: TimeExtent | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "version_ref", _exact_ref(self.version_ref, "version_ref"))
        if not isinstance(self.published, TimeExtent) or self.published.representation != "POINT":
            raise CandidateTemporalIntegrityError(
                "as-of publication extent must be an authorized POINT")
        if self.valid_from is not None:
            if (not isinstance(self.valid_from, TimeExtent)
                    or self.valid_from.representation != "POINT"):
                raise CandidateTemporalIntegrityError(
                    "valid_from must be an authorized POINT when present")
        if self.revoked is not None:
            if (not isinstance(self.revoked, TimeExtent)
                    or self.revoked.representation != "POINT"):
                raise CandidateTemporalIntegrityError(
                    "revoked must be an authorized POINT when present")


@dataclass(frozen=True)
class AsOfSelection:
    state: str
    selected_ref: Mapping[str, str] | None
    eligible_refs: tuple[Mapping[str, str], ...]
    future_excluded_refs: tuple[Mapping[str, str], ...]
    revoked_excluded_refs: tuple[Mapping[str, str], ...]
    not_yet_valid_refs: tuple[Mapping[str, str], ...]
    as_of_ref: Mapping[str, str]
    authority_snapshot_refs: tuple[Mapping[str, str], ...]


def _resolve_positive(
    registry: AuthorityRegistry,
    ref: AuthorityRef,
    *,
    authority_kind: str,
    operation: str,
    exact_scope_refs: Sequence[ExactRef],
    target_use_ref: ExactRef | None = None,
) -> tuple[Any | None, str | None]:
    if not isinstance(registry, AuthorityRegistry):
        raise CandidateTemporalIntegrityError("registry must be a current AuthorityRegistry")
    if authority_kind not in AUTHORITY_KINDS:
        return None, "AUTHORITY_KIND_NOT_CURRENT"
    try:
        snapshot = registry.resolve_exact(ref).snapshot
    except Pre553AuthorityError:
        return None, "AUTHORITY_ABSENT"
    try:
        require_positive_authority(
            snapshot, authority_kind=authority_kind, operation=operation)
    except Pre553AuthorityError:
        return None, "AUTHORITY_NOT_POSITIVE"
    scope = snapshot.scope_envelope
    if not isinstance(scope, Mapping):
        return None, "AUTHORITY_SCOPE_MISMATCH"
    scope_refs = scope.get("predicate_or_risk_set_refs")
    if scope_refs is None:
        return None, "AUTHORITY_SCOPE_MISMATCH"
    for exact in exact_scope_refs:
        if not _explicit_scope_contains(scope_refs, exact):
            return None, "AUTHORITY_SCOPE_MISMATCH"
    if target_use_ref is not None:
        use_scope = scope.get("target_use_refs")
        if use_scope is None or not _explicit_scope_contains(use_scope, target_use_ref):
            return None, "AUTHORITY_SCOPE_MISMATCH"
    return snapshot, None


def _time_geometry(
    left: TimeExtent,
    right: TimeExtent,
    registry: AuthorityRegistry,
) -> tuple[dict[str, Any] | None, list[str], list[AuthorityRef]]:
    reasons: list[str] = []
    authorities: list[AuthorityRef] = []
    for name, extent in (("left", left), ("right", right)):
        snapshot, reason = _resolve_positive(
            registry,
            extent.authority_ref,
            authority_kind=TEMPORAL_EVIDENCE_KIND,
            operation=TIME_ORDER_OPERATION,
            exact_scope_refs=(extent.time_ref, extent.grain_ref),
        )
        if snapshot is None:
            reasons.append(f"{name}:{reason}")
        else:
            authorities.append(snapshot.authority_ref)
    if reasons:
        return None, reasons, authorities
    if left.grain_ref != right.grain_ref:
        return None, ["TEMPORAL_GEOMETRY_GRAIN_MISMATCH"], authorities

    if left.end < right.start:
        state = "LEFT_BEFORE_RIGHT"
    elif right.end < left.start:
        state = "RIGHT_BEFORE_LEFT"
    elif (left.start == right.start and left.end == right.end):
        state = "IDENTICAL"
    else:
        state = "OVERLAP"
    strict_order = state if state in {"LEFT_BEFORE_RIGHT", "RIGHT_BEFORE_LEFT"} else None
    geometry = {
        "state": state,
        "strict_order": strict_order,
        "overlaps": state == "OVERLAP",
        "left": left.as_material(),
        "right": right.as_material(),
        "grain_ref": left.grain_ref.as_dict(),
    }
    return geometry, [], authorities


def _attestation_snapshot(
    attestation: ComparabilityAttestation,
    *,
    left: TemporalAnchor,
    right: TemporalAnchor,
    registry: AuthorityRegistry,
    governed_use_ref: ExactRef,
) -> tuple[Any | None, str | None]:
    field = _SURFACE_ANCHOR_FIELDS.get(attestation.surface)
    if field is None:
        return None, f"UNKNOWN_COMPARABILITY_SURFACE:{attestation.surface}"
    expected_left = left.temporal_time_ref() if field == "temporal_time_ref" else getattr(
        left, field)
    expected_right = right.temporal_time_ref() if field == "temporal_time_ref" else getattr(
        right, field)
    if attestation.left_ref != expected_left or attestation.right_ref != expected_right:
        return None, f"ATTESTATION_BINDING_MISMATCH:{attestation.surface}"
    if attestation.state != "SATISFIED":
        return None, f"SURFACE_NOT_SATISFIED:{attestation.surface}"
    snapshot, reason = _resolve_positive(
        registry,
        attestation.authority_ref,
        authority_kind=attestation.authority_kind,
        operation=attestation.operation,
        exact_scope_refs=(attestation.left_ref, attestation.right_ref),
        target_use_ref=governed_use_ref,
    )
    if snapshot is None:
        return None, f"{reason}:{attestation.surface}"
    return snapshot, None


def _source_equivalence(
    left: TemporalAnchor,
    right: TemporalAnchor,
    evidence: SourceEquivalenceEvidence | None,
) -> tuple[AuthorityRef | None, str | None, Any | None]:
    if left.source_universe_ref == right.source_universe_ref:
        return None, None, None
    if evidence is None:
        return None, "CROSS_UNIVERSE_EQUIVALENCE_ABSENT", None
    try:
        decision = evidence.resolver.require(
            relation_kind=SOURCE_EQUIVALENCE_KIND,
            source_universe_refs=(left.source_universe_ref, right.source_universe_ref),
            operation_scope=evidence.operation_scope,
            target_use=evidence.target_use,
            effective_scope=evidence.effective_scope,
            directionality_or_symmetric="SYMMETRIC",
            relation_ref=evidence.relation_ref,
            expected_authority_operation=SOURCE_EQUIVALENCE_OPERATION,
        )
    except SourceRelationError as exc:
        return None, (
            f"CROSS_UNIVERSE_EQUIVALENCE_REFUSED:"
            f"{getattr(exc, 'state', 'INTEGRITY_ERROR')}"), None
    if not decision.authorized:
        return None, f"CROSS_UNIVERSE_EQUIVALENCE_REFUSED:{decision.state}", None
    expected_pair = tuple(sorted(
        (left.source_universe_ref, right.source_universe_ref), key=lambda ref: ref.key))
    if (decision.relation_kind != SOURCE_EQUIVALENCE_KIND
            or tuple(sorted(decision.source_universe_refs, key=lambda ref: ref.key))
            != expected_pair
            or canonicalize(decision.operation_scope) != canonicalize(evidence.operation_scope)
            or decision.target_use != evidence.target_use
            or canonicalize(decision.effective_scope) != canonicalize(evidence.effective_scope)
            or decision.authority_ref is None):
        return None, "CROSS_UNIVERSE_EQUIVALENCE_NOT_EXACT", None
    return decision.authority_ref, None, decision


def _select_state(reasons: Sequence[str]) -> str:
    if any("AUTHORITY_" in reason for reason in reasons):
        return "TEMPORAL_INSUFFICIENT_AUTHORITY"
    if any(reason.startswith("CROSS_UNIVERSE_EQUIVALENCE") for reason in reasons):
        return "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"
    return "TEMPORAL_NONCOMPARABLE"


def compare_temporal_method(
    left: TemporalAnchor,
    right: TemporalAnchor,
    *,
    profile: TemporalComparabilityProfile,
    registry: AuthorityRegistry,
) -> TemporalMethodDecision:
    if not isinstance(left, TemporalAnchor) or not isinstance(right, TemporalAnchor):
        raise CandidateTemporalIntegrityError("left and right must be TemporalAnchor")
    if not isinstance(profile, TemporalComparabilityProfile):
        raise CandidateTemporalIntegrityError(
            "profile must be TemporalComparabilityProfile")
    if not isinstance(registry, AuthorityRegistry):
        raise CandidateTemporalIntegrityError("registry must be a current AuthorityRegistry")
    if left.anchor_ref == right.anchor_ref:
        raise CandidateTemporalIntegrityError("two distinct anchor refs are required")
    if left.observation_ref == right.observation_ref:
        raise CandidateTemporalIntegrityError("one distinct observation per anchor is required")

    geometry, reasons, authorities = _time_geometry(
        left.effective_time, right.effective_time, registry)

    satisfied_surfaces: list[str] = []
    failed_surfaces: list[str] = []
    attestations = {attestation.surface: attestation for attestation in profile.attestations}
    for surface in profile.required_surfaces:
        attestation = attestations.get(surface)
        if attestation is None:
            reasons.append(f"COMPARABILITY_ATTESTATION_ABSENT:{surface}")
            failed_surfaces.append(surface)
            continue
        snapshot, reason = _attestation_snapshot(
            attestation,
            left=left,
            right=right,
            registry=registry,
            governed_use_ref=profile.governed_use_ref,
        )
        if snapshot is None:
            reasons.append(reason or f"COMPARABILITY_ATTESTATION_FAILED:{surface}")
            failed_surfaces.append(surface)
        else:
            satisfied_surfaces.append(surface)
            authorities.append(snapshot.authority_ref)

    if left.population_ref != right.population_ref:
        reasons.append("POPULATION_NOT_SHARED")
        if "target_population_and_geography" not in failed_surfaces:
            failed_surfaces.append("target_population_and_geography")

    if (left.quantity_value is None) != (right.quantity_value is None):
        reasons.append("QUANTITY_SURFACE_INCOMPLETE")
    if left.quantity_value is not None and right.quantity_value is not None:
        if left.measure_ref != right.measure_ref:
            reasons.append("MEASURE_NOT_SHARED")
        if left.quantity_ref != right.quantity_ref:
            reasons.append("QUANTITY_NOT_SHARED")

    equivalence_ref = None
    equivalence_reason = None
    if (left.source_universe_ref != right.source_universe_ref
            and profile.source_equivalence is not None
            and profile.source_equivalence.target_use
            != profile.governed_use_ref.object_id):
        reasons.append("CROSS_UNIVERSE_EQUIVALENCE_USE_MISMATCH")
    else:
        equivalence_ref, equivalence_reason, _ = _source_equivalence(
            left, right, profile.source_equivalence)
        if equivalence_reason is not None:
            reasons.append(equivalence_reason)
        if equivalence_ref is not None:
            authorities.append(equivalence_ref)

    source_ref = (
        dict(equivalence_ref.as_dict()) if equivalence_ref is not None else None)

    reasons_tuple = tuple(dict.fromkeys(reasons))
    authority_refs = tuple(
        dict(ref.as_dict()) for ref in sorted(set(authorities), key=lambda ref: ref.key))

    if reasons_tuple:
        state = _select_state(reasons_tuple)
        material = {
            "schema": CANDIDATE_SCHEMA,
            "status": CANDIDATE_STATUS,
            "candidate_only": True,
            "governed_use_ref": profile.governed_use_ref.as_dict(),
            "left_anchor": left.as_material(),
            "right_anchor": right.as_material(),
            "geometry": geometry if geometry is not None else "REFUSED",
            "comparability_status": "NOT_COMPARABLE",
            "relation_state": state,
            "reasons": list(reasons_tuple),
            "satisfied_surfaces": satisfied_surfaces,
            "failed_surfaces": failed_surfaces,
            "direction_claim": "DIRECTION_NOT_CLAIMABLE",
            "delta": None,
            "source_equivalence_ref": source_ref,
            "authority_snapshot_refs": list(authority_refs),
        }
        return TemporalMethodDecision(
            comparability_status="NOT_COMPARABLE",
            relation_state=state,
            reasons=reasons_tuple,
            satisfied_surfaces=tuple(satisfied_surfaces),
            failed_surfaces=tuple(failed_surfaces),
            geometry=canonicalize(material["geometry"]),
            direction_claim="DIRECTION_NOT_CLAIMABLE",
            delta=None,
            source_equivalence_ref=source_ref,
            authority_snapshot_refs=authority_refs,
            governed_use_ref=profile.governed_use_ref.as_dict(),
            left_anchor=canonicalize(left.as_material()),
            right_anchor=canonicalize(right.as_material()),
            candidate_only=True,
            receipt_hash=semantic_hash(material),
        )

    if geometry is None:
        raise CandidateTemporalIntegrityError("positive geometry was not produced")
    strict_order = geometry.get("strict_order")
    if geometry.get("state") == "OVERLAP":
        state = "TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION"
    elif strict_order is None:
        state = "TEMPORAL_COMPARABLE_NO_DIRECTION"
    elif left.quantity_value is None:
        state = "TEMPORAL_COMPARABLE_NO_DIRECTION"
    else:
        state = "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"

    delta = None
    direction = "DIRECTION_NOT_CLAIMABLE"
    if state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED":
        if strict_order == "LEFT_BEFORE_RIGHT":
            earlier, later = left.quantity_value, right.quantity_value
        else:
            earlier, later = right.quantity_value, left.quantity_value
        signed_delta = later - earlier
        if signed_delta == 0:
            direction = "NO_AUTHORIZED_CHANGE"
        elif signed_delta > 0:
            direction = "INCREASE"
        else:
            direction = "DECREASE"
        delta = {
            "signed_delta": canonicalize(signed_delta),
            "earlier_value": canonicalize(earlier),
            "later_value": canonicalize(later),
            "comparison_operation": COMPARISON_OPERATION,
            "zero_basis": "exact signed difference equals canonical zero",
        }

    material = {
        "schema": CANDIDATE_SCHEMA,
        "status": CANDIDATE_STATUS,
        "candidate_only": True,
        "governed_use_ref": profile.governed_use_ref.as_dict(),
        "left_anchor": left.as_material(),
        "right_anchor": right.as_material(),
        "geometry": geometry,
        "comparability_status": "COMPARABLE",
        "relation_state": state,
        "reasons": [],
        "satisfied_surfaces": satisfied_surfaces,
        "failed_surfaces": [],
        "direction_claim": direction,
        "delta": delta,
        "source_equivalence_ref": source_ref,
        "authority_snapshot_refs": list(authority_refs),
    }
    return TemporalMethodDecision(
        comparability_status="COMPARABLE",
        relation_state=state,
        reasons=(),
        satisfied_surfaces=tuple(satisfied_surfaces),
        failed_surfaces=(),
        geometry=canonicalize(geometry),
        direction_claim=direction,
        delta=delta,
        source_equivalence_ref=source_ref,
        authority_snapshot_refs=authority_refs,
        governed_use_ref=profile.governed_use_ref.as_dict(),
        left_anchor=canonicalize(left.as_material()),
        right_anchor=canonicalize(right.as_material()),
        candidate_only=True,
        receipt_hash=semantic_hash(material),
    )


def require_comparable(decision: TemporalMethodDecision) -> TemporalMethodDecision:
    if not isinstance(decision, TemporalMethodDecision):
        raise CandidateTemporalIntegrityError("decision must be TemporalMethodDecision")
    if not decision.comparable:
        raise CandidateTemporalNotComparable(decision)
    return decision


def select_as_of_version(
    versions: Iterable[AsOfVersion],
    *,
    as_of: TimeExtent,
    registry: AuthorityRegistry,
) -> AsOfSelection:
    if not isinstance(as_of, TimeExtent) or as_of.representation != "POINT":
        raise CandidateTemporalIntegrityError("as_of must be an authorized POINT extent")
    if not isinstance(registry, AuthorityRegistry):
        raise CandidateTemporalIntegrityError("registry must be a current AuthorityRegistry")
    as_of_snapshot, reason = _resolve_positive(
        registry,
        as_of.authority_ref,
        authority_kind=TEMPORAL_EVIDENCE_KIND,
        operation=TIME_ORDER_OPERATION,
        exact_scope_refs=(as_of.time_ref, as_of.grain_ref),
    )
    if as_of_snapshot is None:
        raise CandidateTemporalIntegrityError(f"as_of authority refused: {reason}")

    authorities = [as_of_snapshot.authority_ref]
    eligible: list[ExactRef] = []
    future: list[ExactRef] = []
    revoked: list[ExactRef] = []
    not_yet_valid: list[ExactRef] = []
    for version in versions:
        if not isinstance(version, AsOfVersion):
            raise CandidateTemporalIntegrityError("versions must contain AsOfVersion")
        published_snapshot, published_reason = _resolve_positive(
            registry,
            version.published.authority_ref,
            authority_kind=TEMPORAL_EVIDENCE_KIND,
            operation=TIME_ORDER_OPERATION,
            exact_scope_refs=(version.published.time_ref, version.published.grain_ref),
        )
        if published_snapshot is None:
            raise CandidateTemporalIntegrityError(
                f"publication authority refused for {version.version_ref.key}: "
                f"{published_reason}")
        authorities.append(published_snapshot.authority_ref)
        if version.published.grain_ref != as_of.grain_ref:
            raise CandidateTemporalIntegrityError(
                f"publication grain mismatch for {version.version_ref.key}")
        if version.published.start > as_of.start:
            future.append(version.version_ref)
            continue
        if version.valid_from is not None:
            valid_snapshot, valid_reason = _resolve_positive(
                registry,
                version.valid_from.authority_ref,
                authority_kind=TEMPORAL_EVIDENCE_KIND,
                operation=TIME_ORDER_OPERATION,
                exact_scope_refs=(version.valid_from.time_ref, version.valid_from.grain_ref),
            )
            if valid_snapshot is None:
                raise CandidateTemporalIntegrityError(
                    f"valid_from authority refused for {version.version_ref.key}: "
                    f"{valid_reason}")
            authorities.append(valid_snapshot.authority_ref)
            if version.valid_from.grain_ref != as_of.grain_ref:
                raise CandidateTemporalIntegrityError(
                    f"valid_from grain mismatch for {version.version_ref.key}")
            if version.valid_from.start > as_of.start:
                not_yet_valid.append(version.version_ref)
                continue
        if version.revoked is not None:
            revoked_snapshot, revoked_reason = _resolve_positive(
                registry,
                version.revoked.authority_ref,
                authority_kind=TEMPORAL_EVIDENCE_KIND,
                operation=TIME_ORDER_OPERATION,
                exact_scope_refs=(version.revoked.time_ref, version.revoked.grain_ref),
            )
            if revoked_snapshot is None:
                raise CandidateTemporalIntegrityError(
                    f"revoked authority refused for {version.version_ref.key}: "
                    f"{revoked_reason}")
            authorities.append(revoked_snapshot.authority_ref)
            if version.revoked.grain_ref != as_of.grain_ref:
                raise CandidateTemporalIntegrityError(
                    f"revoked grain mismatch for {version.version_ref.key}")
            if version.revoked.start <= as_of.start:
                revoked.append(version.version_ref)
                continue
        eligible.append(version.version_ref)

    if not eligible:
        state = "NO_ELIGIBLE_VERSION"
        selected = None
    elif len(eligible) > 1:
        state = "AMBIGUOUS_AS_OF_SELECTION"
        selected = None
    else:
        state = "SELECTED"
        selected = eligible[0]
    authority_refs = tuple(
        dict(ref.as_dict()) for ref in sorted(set(authorities), key=lambda ref: ref.key))
    return AsOfSelection(
        state=state,
        selected_ref=dict(selected.as_dict()) if selected is not None else None,
        eligible_refs=tuple(dict(ref.as_dict()) for ref in eligible),
        future_excluded_refs=tuple(dict(ref.as_dict()) for ref in future),
        revoked_excluded_refs=tuple(dict(ref.as_dict()) for ref in revoked),
        not_yet_valid_refs=tuple(dict(ref.as_dict()) for ref in not_yet_valid),
        as_of_ref=as_of.time_ref.as_dict(),
        authority_snapshot_refs=authority_refs,
    )


__all__ = [
    "CANDIDATE_SCHEMA",
    "CANDIDATE_STATUS",
    "CANDIDATE_MINIMUM_SURFACES",
    "TEMPORAL_EVIDENCE_KIND",
    "TIME_ORDER_OPERATION",
    "COMPARISON_OPERATION",
    "SOURCE_EQUIVALENCE_KIND",
    "SOURCE_EQUIVALENCE_OPERATION",
    "SOURCE_EQUIVALENCE_SCOPE",
    "CandidateTemporalError",
    "CandidateTemporalIntegrityError",
    "CandidateTemporalNotComparable",
    "TimeExtent",
    "TemporalAnchor",
    "ComparabilityAttestation",
    "SourceEquivalenceEvidence",
    "TemporalComparabilityProfile",
    "TemporalMethodDecision",
    "AsOfVersion",
    "AsOfSelection",
    "compare_temporal_method",
    "require_comparable",
    "select_as_of_version",
]
