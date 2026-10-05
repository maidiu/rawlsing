"""Bounded F7 temporal comparison for PRE553 / PYAT HQ211 R1.

Implements exactly the contract repaired and accepted at
``c57a96897788108db7b194e4e51691d1ca8ab729``
(``PYAT-HQ210-F7-TEMPORAL-COMPARABILITY-REPAIR-R1``), itself the successor to
the HQ208 hostile review at ``f1a0dbbc8491e0d23df9005abd55b83e0261424e``.

Design law, taken from the accepted contract and not widened here:

* ``TEMPORAL_RELATION_RECEIPT`` is a **module-local closed content-addressed
  receipt**.  It is NOT a ``PUBLIC_OBJECT_FAMILIES`` member and its
  ``relation_state`` is NOT ``CanonicalSemanticObject.typed_state``.  This
  module therefore performs no ``PUBLIC_OBJECT_FAMILIES`` or ``STATE_FAMILIES``
  edit and creates no new semantic object family.
* ``relation_state`` is a deterministic function of exact inputs.  No caller
  chooses it, and no rerun changes it without changed exact determinants or
  changed authority material.
* Every detected failure is retained in ``comparability_requirement_results``;
  the 12-state precedence selects exactly one public terminal state.
* ``relation_state_reason`` is exactly one scalar reason chosen under
  state-local reason precedence.
* Existing ``AUTHORITY_STATE`` failures map to ``TEMPORAL_INSUFFICIENT_AUTHORITY``
  while the exact authority state is preserved in provenance.  No
  ``AUTHORITY_STATE`` literal is ever inserted into ``TEMPORAL_RELATION_STATE``.
* Cross-universe comparison needs two independent positive paths: the
  source-relation owner resolves ``SOURCE_EQUIVALENCE``, and this module
  resolves ``TEMPORAL_COMPARABILITY`` and consumes that exact equivalence ref.
  Neither mints nor implies the other.
* ``NO_AUTHORIZED_CHANGE`` holds only for an exact canonical-zero signed delta.
  No deadband, tolerance, inherited V553 threshold, or epsilon exists here.
* No F8 consumption, source selection, equivalence creation, pooling,
  backfill, interpolation, continuity, midpoint, rate, trend, trajectory,
  rupture, scalar temporal pressure, currentness, or actor/person inference.

Frozen surfaces this module deliberately does not mutate:
``FORBIDDEN_BACKFILL_TARGET_STATES`` (its literal ``TEMPORAL_NONCOMPARABLE``
membership stays), ``FAIL_CLOSED_STATES``, ``FORBIDDEN_SELECTOR_TOKENS``,
``EmpiricalFact.REQUIRED_FIELDS``, and any V553/V554 historical module.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_authority import (
    AUTHORITY_KINDS,
    AUTHORITY_KIND_CEILINGS,
    AuthorityRegistry,
    Pre553AuthorityConflict,
    Pre553AuthorityError,
    validate_relation_authority_only,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    Pre553IntegrityError,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)

TEMPORAL_COMPARABILITY_CONTRACT_ID = "PYAT_HQ211_F7_TEMPORAL_COMPARABILITY@1.0.0"

#: The one new authority kind, paired with its one matching ceiling entry.
TEMPORAL_COMPARABILITY_AUTHORITY_KIND = "TEMPORAL_COMPARABILITY"

#: Closed order-disposition vocabulary.  Exactly three authorized bases plus one
#: typed no-basis refusal, which is NOT an authorized order basis.
ORDER_DISPOSITIONS = frozenset({
    "CALENDAR_TOTAL_ORDER",
    "FAMILY_LOCAL_ORDINAL",
    "PARTIAL_ORDER_NO_DIRECTION",
    "ORDER_UNKNOWN_NONCOMPARABLE",
})
AUTHORIZED_ORDER_BASES = frozenset({
    "CALENDAR_TOTAL_ORDER",
    "FAMILY_LOCAL_ORDINAL",
    "PARTIAL_ORDER_NO_DIRECTION",
})
NO_BASIS_DISPOSITION = "ORDER_UNKNOWN_NONCOMPARABLE"
DIRECTION_PERMITTING_BASES = frozenset({"CALENDAR_TOTAL_ORDER", "FAMILY_LOCAL_ORDINAL"})

DIRECTION_CLAIM_STATES = frozenset({
    "INCREASE", "DECREASE", "NO_AUTHORIZED_CHANGE", "DIRECTION_NOT_CLAIMABLE",
})

#: Deterministic precedence, highest first.
RELATION_STATE_PRECEDENCE = (
    "TEMPORAL_INSUFFICIENT_AUTHORITY",
    "TEMPORAL_IDENTITY_UNRESOLVED",
    "TEMPORAL_INSUFFICIENT_ANCHORS",
    "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT",
    "TEMPORAL_MAPPING_MATERIAL_ABSENT",
    "TEMPORAL_ESTIMAND_MISMATCH",
    "TEMPORAL_MEASURE_MISMATCH",
    "TEMPORAL_NONCOMPARABLE",
    "TEMPORAL_ORDER_UNAUTHORIZED",
    "TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION",
    "TEMPORAL_COMPARABLE_NO_DIRECTION",
    "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED",
)
RELATION_STATES = frozenset(RELATION_STATE_PRECEDENCE)

#: State-local scalar reason precedence.
STATE_REASON_PRECEDENCE: Mapping[str, tuple[str, ...]] = {
    "TEMPORAL_INSUFFICIENT_AUTHORITY": (
        "AUTHORITY_HASH_MISMATCH",
        "AUTHORITY_SCOPE_MISMATCH",
        "TEMPORAL_COMPARABILITY_AUTHORITY_CONFLICT",
        "TEMPORAL_COMPARABILITY_AUTHORITY_OUT_OF_SCOPE",
        "TEMPORAL_COMPARABILITY_AUTHORITY_REF_ABSENT",
        "TEMPORAL_ORDER_BASIS_AUTHORITY_REF_ABSENT",
        "TEMPORAL_EVIDENCE_AUTHORITY_REF_ABSENT_FOR_ANCHOR",
        "TARGET_USE_PERMISSION_REF_ABSENT",
        "UNCERTAINTY_METHOD_REF_ABSENT",
        "REPLAY_PROTOCOL_REF_ABSENT",
    ),
    "TEMPORAL_IDENTITY_UNRESOLVED": (
        "TEMPORAL_IDENTITY_CONTRACT_REF_ABSENT",
        "IDENTITY_SURFACE_NOT_JOINTLY_SATISFIED",
    ),
    "TEMPORAL_INSUFFICIENT_ANCHORS": ("FEWER_THAN_TWO_AUTHORIZED_ANCHORS",),
    "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT": (
        "SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE",
        "SOURCE_EQUIVALENCE_REF_ABSENT",
    ),
    "TEMPORAL_MAPPING_MATERIAL_ABSENT": (
        "NATIVE_CANONICAL_MAPPING_REF_ABSENT",
        "FAMILY_MAPPING_NOT_POSITIVELY_AUTHORIZED",
    ),
    "TEMPORAL_ESTIMAND_MISMATCH": (
        "ESTIMAND_AUTHORITY_REF_ABSENT",
        "ESTIMANDS_DIFFER",
    ),
    "TEMPORAL_MEASURE_MISMATCH": (
        "MEASURE_AUTHORITY_REF_ABSENT",
        "MEASURE_OR_WEIGHT_DESIGN_DIFFERS",
    ),
    "TEMPORAL_NONCOMPARABLE": (
        "INTERPOLATED_ANCHOR_OR_OBSERVATION_FORBIDDEN",
        "RESPONSE_SURFACE_NOT_SHARED",
        "SCALE_HARMONIZATION_AUTHORITY_ABSENT",
        "INSTRUMENT_RELEASE_NOT_SHARED",
        "QUESTION_COORDINATE_SEMANTICS_NOT_SHARED",
        "GEOGRAPHY_NOT_SHARED",
        "TARGET_POPULATION_RISK_SET_NOT_SHARED",
        "TIME_REPRESENTATION_NONCOMPARABLE_UNDER_BOUND_AUTHORITY",
    ),
    "TEMPORAL_ORDER_UNAUTHORIZED": ("NO_PERMITTED_ORDER_BASIS_APPLIES",),
    "TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION": ("INTERVALS_OVERLAP",),
    "TEMPORAL_COMPARABLE_NO_DIRECTION": (
        "AUTHORIZED_PARTIAL_ORDER_YIELDS_NO_DIRECTION_ON_PAIR",
    ),
    "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED": (
        "AUTHORIZED_ORDERED_PAIR_UNDER_BOUND_COMPARABILITY",
    ),
}

#: Prior F7 relation states mapped onto the repaired terminal states.
PRIOR_F7_STATE_MAP: Mapping[str, str | None] = {
    "TEMPORAL_AUTHORITY_MISSING": "TEMPORAL_INSUFFICIENT_AUTHORITY",
    "TEMPORAL_AUTHORITY_CONFLICT": "TEMPORAL_INSUFFICIENT_AUTHORITY",
    "TEMPORAL_OUT_OF_SCOPE": "TEMPORAL_INSUFFICIENT_AUTHORITY",
    "TEMPORAL_INTERPOLATION_NOT_AUTHORIZED": "TEMPORAL_NONCOMPARABLE",
    "TEMPORAL_RESPONSE_SURFACE_MISMATCH": "TEMPORAL_NONCOMPARABLE",
    # PROBE_ONLY produces no receipt at all.
    "TEMPORAL_PROBE_ONLY": None,
}

#: A temporally noncomparable pair can never be backfilled into positivity.
#: Mirrors the frozen literal in ``pre553_source_relations``.
TEMPORAL_NONCOLLAPSE_STATE = "TEMPORAL_NONCOMPARABLE"
_BACKFILL_FORBIDDEN = frozenset({"TEMPORAL_NONCOMPARABLE", "NONCOMPARABLE"})

#: Comparability surfaces that force TEMPORAL_NONCOMPARABLE when not shared.
NONCOMPARABLE_SURFACES = (
    "RESPONSE_SURFACE_NOT_SHARED",
    "SCALE_HARMONIZATION_AUTHORITY_ABSENT",
    "INSTRUMENT_RELEASE_NOT_SHARED",
    "QUESTION_COORDINATE_SEMANTICS_NOT_SHARED",
    "GEOGRAPHY_NOT_SHARED",
    "TARGET_POPULATION_RISK_SET_NOT_SHARED",
    "TIME_REPRESENTATION_NONCOMPARABLE_UNDER_BOUND_AUTHORITY",
    "INTERPOLATED_ANCHOR_OR_OBSERVATION_FORBIDDEN",
)


class TemporalComparabilityError(Pre553IntegrityError):
    """A lawful temporal comparison cannot be produced as requested."""


class TemporalComparabilityIntegrityError(TemporalComparabilityError):
    """Exact input, ref, tuple, or cross-field law is violated."""


def _canonical_zero(value: Any) -> bool:
    """Exact canonical zero only.

    Zero means exactly zero for any exact numeric representation: integer,
    ``Decimal`` or ``Fraction``. That is not a coercion, because all three are
    exact and mutually orderable, and equality is checked exactly.

    What is refused is everything else: floats, booleans, non-finite decimals,
    and any inexact or banded quantity. There is no deadband, no tolerance, no
    inherited V553 threshold, and no epsilon anywhere in this module.
    """
    try:
        return _exact_sign(value) == 0
    except TemporalComparabilityIntegrityError:
        return False


def _exact_sign(value: Any) -> int:
    """Exact sign of a signed delta with no floating point and no epsilon."""
    if isinstance(value, bool):
        raise TemporalComparabilityIntegrityError("boolean is not a signed delta")
    if isinstance(value, int):
        return (value > 0) - (value < 0)
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise TemporalComparabilityIntegrityError("non-finite delta")
        return (value > 0) - (value < 0)
    if isinstance(value, Fraction):
        return (value > 0) - (value < 0)
    raise TemporalComparabilityIntegrityError(
        "signed delta must be an exact int, Decimal, or Fraction; floats are forbidden")


def _require_ref(value: Any, name: str) -> ExactRef:
    try:
        return exact_ref(value, name)
    except Pre553IntegrityError as exc:
        raise TemporalComparabilityIntegrityError(f"{name} is not an exact ref: {exc}") from exc


def _require_ref_tuple(value: Any, name: str) -> tuple[ExactRef, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, (Sequence, Iterable)):
        raise TemporalComparabilityIntegrityError(f"{name} must be a sequence of exact refs")
    items = tuple(_require_ref(v, f"{name}[{i}]") for i, v in enumerate(value))
    return items


@dataclass(frozen=True)
class TemporalComparisonRequest:
    """Exact bounded request. Nothing here is inferred or defaulted."""

    temporal_identity_contract_ref: Any
    anchor_refs: Any
    temporal_comparability_authority_ref: Any
    temporal_order_disposition: str
    temporal_order_basis_ref: Any
    comparability_requirements_ref: Any
    estimand_authority_refs: Any
    measure_authority_refs: Any
    observation_refs: Any
    uncertainty_authority_ref: Any
    governed_use_id: str
    target_use_permission_refs: Any
    provenance_and_replay_ref: Any
    temporal_evidence_authority_ref: Any = None
    temporal_order_basis_authority_ref: Any = None
    source_equivalence_ref: Any = None
    source_equivalence_authority_ref: Any = None
    source_equivalence_operation: str = "SEMANTIC_EQUIVALENCE_ADMISSION"
    native_canonical_mapping_ref: Any = None
    family_mapping_required: bool = False
    pair_crosses_source_universes: bool = False
    intervals_overlap: bool = False
    identity_surface_jointly_satisfied: bool = True
    comparability_requirement_results: tuple[Mapping[str, Any], ...] = ()
    prior_f7_state: str | None = None
    signed_delta: Any = None
    anchor_order_is_directional: bool = True


@dataclass(frozen=True)
class TemporalRelationReceipt:
    """Module-local closed content-addressed receipt.

    Deliberately NOT a ``CanonicalSemanticObject``. ``relation_state`` is a
    receipt-local validated closed field, never a ``typed_state``.
    """

    receipt_id: str
    contract_id: str
    temporal_identity_contract_ref: dict[str, str]
    anchor_refs: tuple[dict[str, str], ...]
    temporal_order_disposition: str
    temporal_order_basis_ref: dict[str, str] | None
    comparability_status: str
    comparability_requirement_results: tuple[dict[str, Any], ...]
    relation_status: str
    relation_state: str
    relation_state_reason: str
    direction_claim: str
    signed_delta: Any
    non_delta_presence: str
    authority_state_provenance: tuple[str, ...]
    source_equivalence_ref: dict[str, str] | None
    provenance_and_replay_ref: dict[str, str]
    receipt_hash: str

    def as_material(self) -> dict[str, Any]:
        """Exact deterministic replay material; excludes ``receipt_hash``."""
        return {
            "contract_id": self.contract_id,
            "receipt_id": self.receipt_id,
            "temporal_identity_contract_ref": self.temporal_identity_contract_ref,
            "anchor_refs": [dict(r) for r in self.anchor_refs],
            "temporal_order_disposition": self.temporal_order_disposition,
            "temporal_order_basis_ref": self.temporal_order_basis_ref,
            "comparability_status": self.comparability_status,
            "comparability_requirement_results": [dict(r) for r in self.comparability_requirement_results],
            "relation_status": self.relation_status,
            "relation_state": self.relation_state,
            "relation_state_reason": self.relation_state_reason,
            "direction_claim": self.direction_claim,
            "signed_delta": self.signed_delta,
            "non_delta_presence": self.non_delta_presence,
            "authority_state_provenance": list(self.authority_state_provenance),
            "source_equivalence_ref": self.source_equivalence_ref,
            "provenance_and_replay_ref": self.provenance_and_replay_ref,
        }

    def replay_identity(self) -> str:
        return semantic_hash(self.as_material())


def _resolve_positive(registry: AuthorityRegistry | None, ref: Any, kind: str, operation: str | None):
    """Resolve one exact positive authority, returning (snapshot, provenance)."""
    if ref is None:
        return None, (f"{kind}_REF_ABSENT",)
    if registry is None:
        raise TemporalComparabilityError(
            "an exact authority registry is required to resolve any temporal authority")
    try:
        snapshot = registry.require(ref, authority_kind=kind, operation=operation)
    except Pre553AuthorityConflict:
        return None, ("CONFLICT",)
    except Pre553AuthorityError as exc:
        text = str(exc)
        if "hash" in text.lower():
            return None, ("AUTHORITY_HASH_MISMATCH",)
        if "scope" in text.lower():
            return None, ("AUTHORITY_SCOPE_MISMATCH",)
        if "out_of_scope" in text.lower() or "OUT_OF_SCOPE" in text:
            return None, ("OUT_OF_SCOPE",)
        return None, ("REF_ABSENT",)
    return snapshot, ()


def _validate_kind_ceiling_pairing() -> None:
    """The registry has a strict kind/ceiling pairing law."""
    if TEMPORAL_COMPARABILITY_AUTHORITY_KIND not in AUTHORITY_KINDS:
        raise TemporalComparabilityIntegrityError(
            "TEMPORAL_COMPARABILITY must be an exact registered authority kind")
    if TEMPORAL_COMPARABILITY_AUTHORITY_KIND not in AUTHORITY_KIND_CEILINGS:
        raise TemporalComparabilityIntegrityError(
            "TEMPORAL_COMPARABILITY requires exactly one matching ceiling entry")
    for kind in AUTHORITY_KIND_CEILINGS:
        if kind not in AUTHORITY_KINDS:
            raise TemporalComparabilityIntegrityError(
                f"ceiling without kind: {kind}")


def _select_reason(state: str, detected: Sequence[str]) -> str:
    """Exactly one scalar reason under state-local precedence."""
    allowed = STATE_REASON_PRECEDENCE[state]
    for reason in allowed:
        if reason in detected:
            return reason
    # A state may be reached with no surface-specific flag (e.g. a clean
    # positive). Its first reason is then the deterministic scalar reason.
    return allowed[0]


def _validate_cross_field_tuple(receipt_fields: Mapping[str, Any]) -> None:
    """Refuse invalid cross-field tuples before any receipt is minted."""
    state = receipt_fields["relation_state"]
    disposition = receipt_fields["temporal_order_disposition"]
    basis = receipt_fields["temporal_order_basis_ref"]
    direction = receipt_fields["direction_claim"]
    delta = receipt_fields["signed_delta"]
    relation_status = receipt_fields["relation_status"]
    # Exactness is decided on the raw supplied delta, never on its canonical
    # projection, so that an exact tagged zero stays an exact zero.
    delta_is_zero = bool(receipt_fields["_delta_is_exact_zero"])

    if disposition not in ORDER_DISPOSITIONS:
        raise TemporalComparabilityIntegrityError("unknown order disposition")
    if disposition == NO_BASIS_DISPOSITION and basis is not None:
        raise TemporalComparabilityIntegrityError(
            "ORDER_UNKNOWN_NONCOMPARABLE must carry no basis ref")
    if disposition in AUTHORIZED_ORDER_BASES and basis is None:
        raise TemporalComparabilityIntegrityError(
            "an authorized order basis requires an exact basis ref")
    if disposition == NO_BASIS_DISPOSITION and state != "TEMPORAL_ORDER_UNAUTHORIZED":
        raise TemporalComparabilityIntegrityError(
            "no-basis disposition maps uniquely to TEMPORAL_ORDER_UNAUTHORIZED")
    if state == "TEMPORAL_ORDER_UNAUTHORIZED" and disposition != NO_BASIS_DISPOSITION:
        raise TemporalComparabilityIntegrityError(
            "TEMPORAL_ORDER_UNAUTHORIZED has a unique derivation from no-basis")

    if direction == "DIRECTION_NOT_CLAIMABLE" and delta is not None:
        raise TemporalComparabilityIntegrityError(
            "DIRECTION_NOT_CLAIMABLE must carry a null delta")
    if direction == "NO_AUTHORIZED_CHANGE" and not delta_is_zero:
        raise TemporalComparabilityIntegrityError(
            "NO_AUTHORIZED_CHANGE requires an exact canonical-zero delta")
    if state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED":
        if disposition not in DIRECTION_PERMITTING_BASES:
            raise TemporalComparabilityIntegrityError(
                "directional claim requires a direction-permitting authorized basis")
        if direction not in ("INCREASE", "DECREASE", "NO_AUTHORIZED_CHANGE"):
            raise TemporalComparabilityIntegrityError(
                "directional claim authorized with a non-claimable direction")
        if relation_status != "ORDERED_RELATION_AUTHORIZED":
            raise TemporalComparabilityIntegrityError(
                "directional claim requires ORDERED_RELATION_AUTHORIZED")
        if receipt_fields["comparability_status"] != "COMPARABLE":
            raise TemporalComparabilityIntegrityError(
                "directional claim requires a COMPARABLE pair")
        if delta is None:
            raise TemporalComparabilityIntegrityError(
                "directional claim requires an exact delta")
    if disposition == "PARTIAL_ORDER_NO_DIRECTION":
        if state not in ("TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION", "TEMPORAL_COMPARABLE_NO_DIRECTION"):
            raise TemporalComparabilityIntegrityError(
                "partial order may only yield the two comparable-no-direction states")
        if relation_status != "ORDER_RELATION_REFUSED" or direction != "DIRECTION_NOT_CLAIMABLE":
            raise TemporalComparabilityIntegrityError(
                "partial order must refuse the order relation and the direction")


def compare_temporal_anchors(
    request: TemporalComparisonRequest,
    registry: AuthorityRegistry | None = None,
) -> TemporalRelationReceipt:
    """Compare exactly two authorized temporal anchors under bound material.

    Deterministic: identical exact inputs and authority material always yield an
    identical receipt identity. ``relation_state`` is never caller-chosen.
    """
    _validate_kind_ceiling_pairing()

    if request.prior_f7_state is not None and request.prior_f7_state not in PRIOR_F7_STATE_MAP:
        raise TemporalComparabilityIntegrityError("unknown prior F7 state")
    if request.prior_f7_state == "TEMPORAL_PROBE_ONLY":
        # PROBE_ONLY is diagnostic output outside TEMPORAL_RELATION_RECEIPT and
        # cannot be upgraded into a claim: there is simply no receipt.
        raise TemporalComparabilityError(
            "TEMPORAL_PROBE_ONLY yields no temporal relation receipt")

    disposition = request.temporal_order_disposition
    if disposition not in ORDER_DISPOSITIONS:
        raise TemporalComparabilityIntegrityError(f"unknown order disposition: {disposition}")

    anchors = _require_ref_tuple(request.anchor_refs, "anchor_refs")
    observations = _require_ref_tuple(request.observation_refs, "observation_refs")
    estimands = _require_ref_tuple(request.estimand_authority_refs, "estimand_authority_refs")
    measures = _require_ref_tuple(request.measure_authority_refs, "measure_authority_refs")
    target_uses = _require_ref_tuple(
        request.target_use_permission_refs, "target_use_permission_refs")

    if request.governed_use_id is None or not str(request.governed_use_id).strip():
        raise TemporalComparabilityIntegrityError("governed_use_id is required")

    identity_ref = None
    if request.temporal_identity_contract_ref is not None:
        identity_ref = _require_ref(request.temporal_identity_contract_ref, "temporal_identity_contract_ref")
    requirements_ref = None
    if request.comparability_requirements_ref is not None:
        requirements_ref = _require_ref(request.comparability_requirements_ref, "comparability_requirements_ref")
    replay_ref = None
    if request.provenance_and_replay_ref is not None:
        replay_ref = _require_ref(request.provenance_and_replay_ref, "provenance_and_replay_ref")
    uncertainty_ref = None
    if request.uncertainty_authority_ref is not None:
        uncertainty_ref = _require_ref(request.uncertainty_authority_ref, "uncertainty_authority_ref")
    mapping_ref = None
    if request.native_canonical_mapping_ref is not None:
        mapping_ref = _require_ref(request.native_canonical_mapping_ref, "native_canonical_mapping_ref")

    basis_ref = None
    if request.temporal_order_basis_ref is not None:
        if disposition == NO_BASIS_DISPOSITION:
            raise TemporalComparabilityIntegrityError(
                "ORDER_UNKNOWN_NONCOMPARABLE must carry no basis ref")
        basis_ref = _require_ref(request.temporal_order_basis_ref, "temporal_order_basis_ref")

    # Every detected failure is retained; precedence later selects one state.
    detected: list[str] = []
    authority_provenance: list[str] = []

    snapshot, prov = _resolve_positive(
        registry, request.temporal_comparability_authority_ref,
        TEMPORAL_COMPARABILITY_AUTHORITY_KIND, None)
    authority_provenance.extend(f"{TEMPORAL_COMPARABILITY_AUTHORITY_KIND}:{p}" for p in prov)
    if snapshot is None:
        if "CONFLICT" in prov:
            detected.append("TEMPORAL_COMPARABILITY_AUTHORITY_CONFLICT")
        elif "OUT_OF_SCOPE" in prov:
            detected.append("TEMPORAL_COMPARABILITY_AUTHORITY_OUT_OF_SCOPE")
        else:
            detected.append("TEMPORAL_COMPARABILITY_AUTHORITY_REF_ABSENT")

    if disposition in AUTHORIZED_ORDER_BASES:
        # An authorized basis requires a positive exact basis authority under
        # TEMPORAL_EVIDENCE. The basis ref itself is an ExactRef, never an
        # AuthorityRef; it is never resolved as one.
        basis_snapshot, basis_prov = _resolve_positive(
            registry, request.temporal_order_basis_authority_ref, "TEMPORAL_EVIDENCE", None)
        if basis_snapshot is None:
            detected.append("TEMPORAL_ORDER_BASIS_AUTHORITY_REF_ABSENT")

    if request.temporal_evidence_authority_ref is None:
        detected.append("TEMPORAL_EVIDENCE_AUTHORITY_REF_ABSENT_FOR_ANCHOR")
    else:
        ev_snapshot, ev_prov = _resolve_positive(
            registry, request.temporal_evidence_authority_ref, "TEMPORAL_EVIDENCE", None)
        if ev_snapshot is None:
            detected.append("TEMPORAL_EVIDENCE_AUTHORITY_REF_ABSENT_FOR_ANCHOR")

    if not target_uses:
        detected.append("TARGET_USE_PERMISSION_REF_ABSENT")
    if uncertainty_ref is None:
        detected.append("UNCERTAINTY_METHOD_REF_ABSENT")
    if replay_ref is None:
        detected.append("REPLAY_PROTOCOL_REF_ABSENT")

    if identity_ref is None:
        detected.append("TEMPORAL_IDENTITY_CONTRACT_REF_ABSENT")
    elif not request.identity_surface_jointly_satisfied:
        detected.append("IDENTITY_SURFACE_NOT_JOINTLY_SATISFIED")

    authorized_anchor_count = len(anchors)
    if authorized_anchor_count < 2:
        detected.append("FEWER_THAN_TWO_AUTHORIZED_ANCHORS")

    # Cross-universe: two independent positive paths, never one implying the other.
    equivalence_ref = None
    equivalence_positive = False
    if request.source_equivalence_ref is not None:
        equivalence_ref = _require_ref(request.source_equivalence_ref, "source_equivalence_ref")
    if request.pair_crosses_source_universes:
        if equivalence_ref is None:
            detected.append("SOURCE_EQUIVALENCE_REF_ABSENT")
        elif request.source_equivalence_authority_ref is None:
            detected.append("SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE")
        else:
            # Path A: the source-relation owner, via the existing relation path.
            try:
                eq_snapshot = registry.require(
                    request.source_equivalence_authority_ref, authority_kind="SOURCE_EQUIVALENCE")
            except Pre553AuthorityError:
                eq_snapshot = None
            except Pre553AuthorityConflict:
                eq_snapshot = None
            if eq_snapshot is None:
                detected.append("SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE")
            else:
                try:
                    validate_relation_authority_only(
                        eq_snapshot,
                        relation_authority_kind="SOURCE_EQUIVALENCE",
                        exact_relation_operation=request.source_equivalence_operation)
                    equivalence_positive = True
                except Pre553AuthorityError:
                    detected.append("SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE")

    if request.family_mapping_required:
        if mapping_ref is None:
            detected.append("NATIVE_CANONICAL_MAPPING_REF_ABSENT")
        else:
            map_snapshot, map_prov = _resolve_positive(
                registry, mapping_ref, "NATIVE_CANONICAL_MAPPING_HARMONIZATION", None)
            if map_snapshot is None:
                detected.append("FAMILY_MAPPING_NOT_POSITIVELY_AUTHORIZED")

    if not estimands:
        detected.append("ESTIMAND_AUTHORITY_REF_ABSENT")
    elif len({r.key for r in estimands}) > 1:
        detected.append("ESTIMANDS_DIFFER")
    if not measures:
        detected.append("MEASURE_AUTHORITY_REF_ABSENT")
    elif len({r.key for r in measures}) > 1:
        detected.append("MEASURE_OR_WEIGHT_DESIGN_DIFFERS")

    declared = {str(d.get("reason")) for d in request.comparability_requirement_results if d.get("reason")}
    for surface in NONCOMPARABLE_SURFACES:
        if surface in declared:
            detected.append(surface)

    order_refused_surfaces = detected

    # Deterministic precedence selection.
    by_state: dict[str, list[str]] = {
        "TEMPORAL_INSUFFICIENT_AUTHORITY": [],
        "TEMPORAL_IDENTITY_UNRESOLVED": [],
        "TEMPORAL_INSUFFICIENT_ANCHORS": [],
        "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT": [],
        "TEMPORAL_MAPPING_MATERIAL_ABSENT": [],
        "TEMPORAL_ESTIMAND_MISMATCH": [],
        "TEMPORAL_MEASURE_MISMATCH": [],
        "TEMPORAL_NONCOMPARABLE": [],
        "TEMPORAL_ORDER_UNAUTHORIZED": [],
        "TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION": [],
        "TEMPORAL_COMPARABLE_NO_DIRECTION": [],
        "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED": [],
    }
    for reason in detected:
        if reason in STATE_REASON_PRECEDENCE["TEMPORAL_INSUFFICIENT_AUTHORITY"]:
            by_state["TEMPORAL_INSUFFICIENT_AUTHORITY"].append(reason)
        elif reason in STATE_REASON_PRECEDENCE["TEMPORAL_IDENTITY_UNRESOLVED"]:
            by_state["TEMPORAL_IDENTITY_UNRESOLVED"].append(reason)
        elif reason in STATE_REASON_PRECEDENCE["TEMPORAL_INSUFFICIENT_ANCHORS"]:
            by_state["TEMPORAL_INSUFFICIENT_ANCHORS"].append(reason)
        elif reason in STATE_REASON_PRECEDENCE["TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"]:
            by_state["TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"].append(reason)
        elif reason in STATE_REASON_PRECEDENCE["TEMPORAL_MAPPING_MATERIAL_ABSENT"]:
            by_state["TEMPORAL_MAPPING_MATERIAL_ABSENT"].append(reason)
        elif reason in STATE_REASON_PRECEDENCE["TEMPORAL_ESTIMAND_MISMATCH"]:
            by_state["TEMPORAL_ESTIMAND_MISMATCH"].append(reason)
        elif reason in STATE_REASON_PRECEDENCE["TEMPORAL_MEASURE_MISMATCH"]:
            by_state["TEMPORAL_MEASURE_MISMATCH"].append(reason)
        elif reason in STATE_REASON_PRECEDENCE["TEMPORAL_NONCOMPARABLE"]:
            by_state["TEMPORAL_NONCOMPARABLE"].append(reason)

    negative_states = (
        "TEMPORAL_INSUFFICIENT_AUTHORITY",
        "TEMPORAL_IDENTITY_UNRESOLVED",
        "TEMPORAL_INSUFFICIENT_ANCHORS",
        "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT",
        "TEMPORAL_MAPPING_MATERIAL_ABSENT",
        "TEMPORAL_ESTIMAND_MISMATCH",
        "TEMPORAL_MEASURE_MISMATCH",
        "TEMPORAL_NONCOMPARABLE",
    )
    state = None
    for candidate in RELATION_STATE_PRECEDENCE:
        if candidate in negative_states and by_state[candidate]:
            state = candidate
            break
    if state is None:
        if disposition == NO_BASIS_DISPOSITION:
            state = "TEMPORAL_ORDER_UNAUTHORIZED"
        elif disposition == "PARTIAL_ORDER_NO_DIRECTION":
            state = ("TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION" if request.intervals_overlap
                     else "TEMPORAL_COMPARABLE_NO_DIRECTION")
        else:
            state = "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"

    positive_state = state in (
        "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED",
        "TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION",
        "TEMPORAL_COMPARABLE_NO_DIRECTION",
    )
    comparable = state != "TEMPORAL_NONCOMPARABLE" and state not in (
        "TEMPORAL_INSUFFICIENT_AUTHORITY",
        "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT",
    )
    ordered = state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"

    # A direction-permitting basis requires an exact delta. The closed 12-state
    # vocabulary has no state for "ordered but delta absent", and state 9 has a
    # unique no-basis derivation, so this is an invalid request, not a receipt.
    if state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED" and request.signed_delta is None:
        raise TemporalComparabilityIntegrityError(
            "a direction-permitting authorized basis requires an exact signed delta; "
            "the closed vocabulary has no ordered-without-delta relation state")
    if request.signed_delta is None:
        direction_claim = "DIRECTION_NOT_CLAIMABLE"
    elif _exact_sign(request.signed_delta) == 0:
        direction_claim = "NO_AUTHORIZED_CHANGE"
    else:
        direction_claim = "INCREASE" if _exact_sign(request.signed_delta) > 0 else "DECREASE"

    non_delta_presence = "DELTA_PRESENT" if request.signed_delta is not None else "DELTA_NOT_CLAIMABLE"

    if disposition == "PARTIAL_ORDER_NO_DIRECTION":
        direction_claim = "DIRECTION_NOT_CLAIMABLE"
    if state in negative_states or state == "TEMPORAL_ORDER_UNAUTHORIZED":
        direction_claim = "DIRECTION_NOT_CLAIMABLE"

    delta_payload = canonicalize(request.signed_delta) if request.signed_delta is not None else None
    if direction_claim == "DIRECTION_NOT_CLAIMABLE":
        delta_payload = None

    if state == "TEMPORAL_NONCOMPARABLE":
        _require_noncollapse_refusal()

    if request.anchor_order_is_directional and ordered and len(anchors) == 2:
        anchor_material = tuple(a.as_dict() for a in anchors)
    else:
        anchor_material = tuple(a.as_dict() for a in sorted(
            anchors, key=lambda r: canonical_json(r.as_dict())))

    results = tuple(
        {"reason": r} for r in sorted(set(order_refused_surfaces) | set(declared)))

    fields = {
        "relation_state": state,
        "temporal_order_disposition": disposition,
        "temporal_order_basis_ref": basis_ref.as_dict() if basis_ref else None,
        "comparability_status": "COMPARABLE" if comparable else "NOT_COMPARABLE",
        "relation_status": "ORDERED_RELATION_AUTHORIZED" if ordered else "ORDER_RELATION_REFUSED",
        "direction_claim": direction_claim,
        "signed_delta": delta_payload,
        "non_delta_presence": non_delta_presence,
        "_delta_is_exact_zero": (
            request.signed_delta is not None and _canonical_zero(request.signed_delta)),
    }
    _validate_cross_field_tuple(fields)

    reason = _select_reason(state, detected)

    material = {
        "contract_id": TEMPORAL_COMPARABILITY_CONTRACT_ID,
        "receipt_id": f"urn:pyat:f7-temporal-relation:{semantic_hash({'anchors': [a.as_dict() for a in anchors], 'disposition': disposition})[:32]}",
        "temporal_identity_contract_ref": identity_ref.as_dict() if identity_ref else None,
        "anchor_refs": [dict(a) for a in anchor_material],
        "temporal_order_disposition": disposition,
        "temporal_order_basis_ref": basis_ref.as_dict() if basis_ref else None,
        "comparability_status": fields["comparability_status"],
        "comparability_requirement_results": [dict(r) for r in results],
        "relation_status": fields["relation_status"],
        "relation_state": state,
        "relation_state_reason": reason,
        "direction_claim": direction_claim,
        "signed_delta": delta_payload,
        "non_delta_presence": non_delta_presence,
        "authority_state_provenance": sorted(set(authority_provenance)),
        "source_equivalence_ref": equivalence_ref.as_dict() if equivalence_ref else None,
        "provenance_and_replay_ref": replay_ref.as_dict() if replay_ref else None,
    }
    receipt_hash = semantic_hash(material)
    return TemporalRelationReceipt(
        receipt_id=material["receipt_id"],
        contract_id=TEMPORAL_COMPARABILITY_CONTRACT_ID,
        temporal_identity_contract_ref=material["temporal_identity_contract_ref"],
        anchor_refs=tuple(dict(a) for a in material["anchor_refs"]),
        temporal_order_disposition=disposition,
        temporal_order_basis_ref=material["temporal_order_basis_ref"],
        comparability_status=material["comparability_status"],
        comparability_requirement_results=tuple(dict(r) for r in material["comparability_requirement_results"]),
        relation_status=material["relation_status"],
        relation_state=state,
        relation_state_reason=reason,
        direction_claim=direction_claim,
        signed_delta=delta_payload,
        non_delta_presence=non_delta_presence,
        authority_state_provenance=tuple(material["authority_state_provenance"]),
        source_equivalence_ref=material["source_equivalence_ref"],
        provenance_and_replay_ref=material["provenance_and_replay_ref"],
        receipt_hash=receipt_hash,
    )


def _require_noncollapse_refusal() -> None:
    """A noncomparable pair can never be backfilled into positivity."""
    if TEMPORAL_NONCOLLAPSE_STATE not in _BACKFILL_FORBIDDEN:
        raise TemporalComparabilityIntegrityError(
            "TEMPORAL_NONCOMPARABLE must remain a forbidden backfill target state")


def temporal_backfill_refused(relation_state: str) -> bool:
    """True when the state may never be a backfill target."""
    return relation_state in _BACKFILL_FORBIDDEN


__all__ = [
    "TEMPORAL_COMPARABILITY_CONTRACT_ID",
    "TEMPORAL_COMPARABILITY_AUTHORITY_KIND",
    "ORDER_DISPOSITIONS",
    "AUTHORIZED_ORDER_BASES",
    "NO_BASIS_DISPOSITION",
    "DIRECTION_PERMITTING_BASES",
    "DIRECTION_CLAIM_STATES",
    "RELATION_STATE_PRECEDENCE",
    "RELATION_STATES",
    "STATE_REASON_PRECEDENCE",
    "PRIOR_F7_STATE_MAP",
    "TEMPORAL_NONCOLLAPSE_STATE",
    "TemporalComparabilityError",
    "TemporalComparabilityIntegrityError",
    "TemporalComparisonRequest",
    "TemporalRelationReceipt",
    "compare_temporal_anchors",
    "temporal_backfill_refused",
]