"""Bounded F7 temporal comparison for PRE553 / PYAT HQ214 bounded repair R1.

Repairs the HQ211 implementation against the HQ213 hostile review
(``F7_TEMPORAL_IMPLEMENTATION_PARTIAL__BOUNDED_REPAIR_REQUIRED``) while
realizing exactly the contract accepted at
``c57a96897788108db7b194e4e51691d1ca8ab729``.

The HQ213 review's central finding was that the HQ211 surface carried the right
vocabulary but the machinery was fail-open: a positive directional claim could be
minted with fabricated refs that resolved nowhere. This revision repairs the
machinery, not the prose.

What actually changed, by finding:

* ``F-DIR-01`` / Repair 1 - every contract-required authority is now resolved to
  a positive exact snapshot or a typed fail-closed outcome. Presence of a ref
  string is never sufficient.
* ``F-DIR-02`` / Repair 2 - ``TEMPORAL_COMPARABILITY`` is resolved
  operation-scoped and governed-use-scoped. ``AUTHORITY_HASH_MISMATCH`` and
  ``AUTHORITY_SCOPE_MISMATCH`` are reachable receipt reasons.
* ``F-CARD-01`` / Repair 3 - exactly two anchors and two observations, one
  observation bound to each anchor. 3+ refuses.
* ``F-REQ-01`` / Repair 4 - ``comparability_requirements_ref`` is required and
  resolved, and its surfaces participate in derivation.
* ``F-DELTA-01`` / Repair 5 - the caller can no longer mint a dispositive delta.
  The exact delta is derived from the bound quantity surface under an exact
  authorized comparison operation.
* ``F-RCPT-01`` / Repair 6 - the receipt carries the accepted 18-field closed
  contract, using the contract's own field names, including ``quantity_surface``,
  ``delta``, ``uncertainty_state``, ``intervening_span_state``,
  ``governed_use_id``, ``authority_snapshot_refs`` and ``provenance``.
* ``F-PRIOR-01`` / Repair 7 - ``prior_f7_state`` participates in derivation.
* ``F-XU-01`` / Repair 8 - cross-universe status is derived from the bound
  per-anchor source-universe refs, never from a caller boolean, and an exact
  positive ``SOURCE_EQUIVALENCE`` must cover the actual pair.
* ``F-ORDER-01`` / HQ214 adjudication C - no-basis yields
  ``TEMPORAL_ORDER_UNAUTHORIZED`` only when no higher-precedence failure was
  selected; otherwise the higher state is emitted and the no-basis observation is
  retained in provenance. The module no longer raises on that combination.
* HQ214 adjudication B - ``comparability_status`` is ``NOT_COMPARABLE`` for all
  nine negative/refusal states and ``COMPARABLE`` only for the three lawful
  comparability states.
* ``F-BACKFILL-01`` / Repair 9 - the backfill guard consults the live frozen
  ``FORBIDDEN_BACKFILL_TARGET_STATES``, not a module-local copy.
* ``F-NONE-01`` - a missing registry is a typed refusal, never an ``AttributeError``.

Power ceiling is unchanged. This module never consumes F8, never selects sources,
never creates source equivalence, pooling or linkage, and never performs
interpolation, continuity, midpoint, trend, rate, trajectory, rupture, currentness,
scalar temporal pressure, causal interpretation, or actor/person inference.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from fractions import Fraction
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_authority import (
    AUTHORITY_KINDS,
    AUTHORITY_KIND_CEILINGS,
    AuthorityRegistry,
    AuthoritySnapshot,
    Pre553AuthorityConflict,
    Pre553AuthorityError,
    require_positive_authority,
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

TEMPORAL_COMPARABILITY_CONTRACT_ID = "PYAT_HQ211_F7_TEMPORAL_COMPARABILITY@1.1.0"

TEMPORAL_COMPARABILITY_AUTHORITY_KIND = "TEMPORAL_COMPARABILITY"

#: The exact authorized comparison operation this producer can bind.
AUTHORIZED_COMPARISON_OPERATION = "TEMPORAL_BOUND_QUANTITY_DIFFERENCE"
#: The relation operation used on the source-relation path for equivalence.
SOURCE_EQUIVALENCE_RELATION_OPERATION = "SEMANTIC_EQUIVALENCE_ADMISSION"

#: HQ219 RR-04: the exact relation kind and exact scope F7 requires when it asks the
#: adopted source-relation owner to admit a cross-universe pair. These are requirements
#: F7 imposes, not authorities it creates: the owner still decides.
SOURCE_EQUIVALENCE_REQUIRED_RELATION_KIND = "SOURCE_SEMANTIC_EQUIVALENCE"
SOURCE_EQUIVALENCE_REQUIRED_SCOPE = "EXACT_BOUND_UNIVERSE_PAIR"

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

UNCERTAINTY_STATES = frozenset({
    "QUANTIFIED_UNDER_BOUND_METHOD",
    "UNCERTAINTY_UNQUANTIFIED",
    "UNCERTAINTY_METHOD_ABSENT",
})
INTERVENING_SPAN_STATES = frozenset({"NO_INTERVENING_GAP", "TEMPORAL_GAP_INTERVENING"})
DIRECTION_CLAIM_STATES = frozenset({
    "INCREASE", "DECREASE", "NO_AUTHORIZED_CHANGE", "DIRECTION_NOT_CLAIMABLE",
})

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

#: HQ214 adjudication B - the only states that may carry COMPARABLE.
COMPARABLE_STATES = frozenset({
    "TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION",
    "TEMPORAL_COMPARABLE_NO_DIRECTION",
    "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED",
})

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
        "ESTIMAND_AUTHORITY_NOT_POSITIVE",
        "MEASURE_AUTHORITY_NOT_POSITIVE",
    ),
    "TEMPORAL_IDENTITY_UNRESOLVED": (
        "TEMPORAL_IDENTITY_CONTRACT_REF_ABSENT",
        "IDENTITY_SURFACE_NOT_JOINTLY_SATISFIED",
        # HQ219 RR-03: identity must be OWNER-RESOLVED. An identity the
        # TEMPORAL_EVIDENCE authority does not bind, and an identity the owner cannot be
        # consulted about, are identity refusals rather than soft signals. Both reuse the
        # EXISTING state; no new relation state is introduced.
        "TEMPORAL_IDENTITY_NOT_BOUND_BY_TEMPORAL_EVIDENCE_AUTHORITY",
        "TEMPORAL_IDENTITY_OWNER_RESOLUTION_UNAVAILABLE",
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

#: Repair 7 - prior F7 states now participate in derivation rather than sit inert.
PRIOR_F7_STATE_MAP: Mapping[str, str] = {
    "TEMPORAL_AUTHORITY_MISSING": "TEMPORAL_COMPARABILITY_AUTHORITY_REF_ABSENT",
    "TEMPORAL_AUTHORITY_CONFLICT": "TEMPORAL_COMPARABILITY_AUTHORITY_CONFLICT",
    "TEMPORAL_OUT_OF_SCOPE": "TEMPORAL_COMPARABILITY_AUTHORITY_OUT_OF_SCOPE",
    "TEMPORAL_INTERPOLATION_NOT_AUTHORIZED": "INTERPOLATED_ANCHOR_OR_OBSERVATION_FORBIDDEN",
    "TEMPORAL_RESPONSE_SURFACE_MISMATCH": "RESPONSE_SURFACE_NOT_SHARED",
}
PRIOR_F7_NO_RECEIPT_STATES = frozenset({"TEMPORAL_PROBE_ONLY"})

NONCOMPARABLE_SURFACES = tuple(STATE_REASON_PRECEDENCE["TEMPORAL_NONCOMPARABLE"])

NEGATIVE_STATES = frozenset(RELATION_STATE_PRECEDENCE) - COMPARABLE_STATES


class TemporalComparabilityError(Pre553IntegrityError):
    """A lawful temporal comparison cannot be produced as requested."""


class TemporalComparabilityInputRefusal(TemporalComparabilityError):
    """HQ214 adjudication A - typed refusal before any receipt is emitted."""


class TemporalComparabilityIntegrityError(TemporalComparabilityError):
    """Exact input, ref, tuple, or cross-field law is violated."""


# ---------------------------------------------------------------------------
# exact numeric law
# ---------------------------------------------------------------------------

#: HQ219 RR-04: the ADOPTED source-relation owner type. F7 requires the real
#: resolver, so a duck-typed stub cannot stand in for the owner decision path.
#: FORBIDDEN_BACKFILL_TARGET_STATES is imported here too so this module imports the
#: adopted relation owner exactly once.
import rawlsing_next.pre553_source_relations as _adopted_source_relations

#: The adopted owner type. Read as an ATTRIBUTE of the adopted module rather than a
#: from-import, so the module is imported exactly once AND ``FORBIDDEN_BACKFILL_TARGET_STATES``
#: keeps being read LIVE off the frozen surface, which the backfill guard's liveness
#: test depends on.
SourceRelationResolver = _adopted_source_relations.SourceRelationResolver

def _exact_number(value: Any, name: str) -> int | Decimal | Fraction:
    if isinstance(value, bool):
        raise TemporalComparabilityIntegrityError(f"{name} must be an exact number, not bool")
    if isinstance(value, int):
        return value
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise TemporalComparabilityIntegrityError(f"{name} must be finite")
        return value
    if isinstance(value, Fraction):
        return value
    raise TemporalComparabilityIntegrityError(
        f"{name} must be an exact int, Decimal, or Fraction; floats are forbidden")


def _exact_sign(value: Any) -> int:
    number = _exact_number(value, "value")
    return (number > 0) - (number < 0)


def _canonical_zero(value: Any) -> bool:
    """Exact zero only: exact sign equals zero.

    Zero is zero for any exact numeric representation, which is not a coercion
    because all three are exact and mutually orderable. Floats, booleans and
    non-finite values are refused. There is no deadband, tolerance, inherited
    V553 threshold, or epsilon anywhere.
    """
    try:
        return _exact_sign(value) == 0
    except TemporalComparabilityIntegrityError:
        return False


def _exact_difference(later: Any, earlier: Any) -> int | Decimal | Fraction:
    """The exact signed difference, computed rather than caller-minted."""
    a = _exact_number(later, "later_value")
    b = _exact_number(earlier, "earlier_value")
    return a - b


# ---------------------------------------------------------------------------
# ref helpers
# ---------------------------------------------------------------------------

def _require_ref(value: Any, name: str) -> ExactRef:
    try:
        return exact_ref(value, name)
    except Pre553IntegrityError as exc:
        raise TemporalComparabilityIntegrityError(f"{name} is not an exact ref: {exc}") from exc


def _require_ref_tuple(value: Any, name: str) -> tuple[ExactRef, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, (Sequence, Iterable)):
        raise TemporalComparabilityIntegrityError(f"{name} must be a sequence of exact refs")
    return tuple(_require_ref(v, f"{name}[{i}]") for i, v in enumerate(value))


def _require_authority_ref(value: Any, name: str) -> AuthorityRef:
    if isinstance(value, AuthorityRef):
        return value
    if isinstance(value, Mapping):
        try:
            keys = set(value)
        except TypeError as exc:  # pragma: no cover - defensive
            raise TemporalComparabilityIntegrityError(f"{name} is malformed") from exc
        if keys == {"authority_id", "authority_version", "authority_content_hash"}:
            return AuthorityRef(value["authority_id"], value["authority_version"],
                                value["authority_content_hash"])
    raise TemporalComparabilityIntegrityError(f"{name} must be an exact AuthorityRef")


def _require_authority_tuple(value: Any, name: str) -> tuple[AuthorityRef, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, (Sequence, Iterable)):
        raise TemporalComparabilityIntegrityError(f"{name} must be a sequence of AuthorityRef")
    return tuple(_require_authority_ref(v, f"{name}[{i}]") for i, v in enumerate(value))


# ---------------------------------------------------------------------------
# authority resolution (Repair 1 + Repair 2)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AuthorityResolutionRecord:
    """Exact typed outcome of one required authority resolution."""

    slot: str
    authority_kind: str
    authority_ref: AuthorityRef | None
    outcome: str
    detail: str | None = None
    operation: str | None = None
    governed_use_id: str | None = None

    def as_material(self) -> dict[str, Any]:
        return {
            "slot": self.slot,
            "authority_kind": self.authority_kind,
            "authority_ref": self.authority_ref.as_dict() if self.authority_ref else None,
            "outcome": self.outcome,
            "detail": self.detail,
            "operation": self.operation,
            "governed_use_id": self.governed_use_id,
        }


POSITIVE = "POSITIVE"
ABSENT = "ABSENT"
CONFLICT = "CONFLICT"
HASH_MISMATCH = "AUTHORITY_HASH_MISMATCH"
SCOPE_MISMATCH = "AUTHORITY_SCOPE_MISMATCH"
OUT_OF_SCOPE = "OUT_OF_SCOPE"


def _known_snapshots(registry: AuthorityRegistry) -> tuple[AuthoritySnapshot, ...]:
    """Registered snapshots, for immutable-hash diagnostics only."""
    by_key = getattr(registry, "_by_key", None)
    if isinstance(by_key, Mapping):
        return tuple(by_key.values())
    return ()


def _bind_ref_to_material(ref: ExactRef, material: Any, *, ref_slot: str,
                          material_slot: str) -> Mapping[str, Any]:
    """HQ217 RR-01/RR-03: a ref token alone is not proof.

    The contract ref names an exact requirement/identity material set. A ref is only
    bound when the caller supplies that material AND its canonical hash equals the
    ref's content_hash. An unbound ref yields a typed refusal, never a silent pass and
    never a caller-trusted boolean.
    """
    if material is None:
        raise TemporalComparabilityInputRefusal(
            f"{ref_slot} is not bound: {material_slot} is required and must hash to the "
            f"ref's content_hash; a ref token alone is not proof")
    try:
        actual = semantic_hash(material)
    except Exception as exc:  # material must be canonicalizable
        raise TemporalComparabilityInputRefusal(
            f"{material_slot} is not canonicalizable exact material: {exc}") from exc
    if actual != ref.content_hash:
        raise TemporalComparabilityInputRefusal(
            f"{material_slot} does not hash to {ref_slot}.content_hash; the supplied "
            "material is not the exact material the ref names")
    return material


#: HQ222 F7-RR-02C: the exact set of adopted explicit-unrestricted scope
#: representations. This mirrors ``pre553_empirical_authority._scope_contains``,
#: which already treats both literals as positive. F7 previously recognized only
#: ``EXPLICIT_UNRESTRICTED``, so a competent authority expressed with the other
#: adopted representation was silently reinterpreted as non-authority.
#:
#: This constant adds NO third token, and OMISSION is never unrestricted: the
#: helpers below still return False for None, for an empty collection, and for
#: any other literal. Only these two exact adopted literals grant a blanket.
ADOPTED_UNRESTRICTED_SCOPE_REPRESENTATIONS = frozenset({
    "EXPLICIT_UNRESTRICTED",
    "UNRESTRICTED_BY_THIS_AUTHORITY",
})


def _scope_is_adopted_unrestricted(scope_value: Any) -> bool:
    """True only for one of the two adopted explicit-unrestricted literals."""
    return (isinstance(scope_value, str)
            and scope_value in ADOPTED_UNRESTRICTED_SCOPE_REPRESENTATIONS)


def _temporal_evidence_identity_scope(snapshot: Any) -> Mapping[str, Any]:
    """HQ222 COURT-HQ220-01: read the identity-owning authority's scope envelope.

    This is the single seam through which F7 consults the adopted TEMPORAL_EVIDENCE
    authority about temporal identity. It exists so the court can break owner
    satisfaction consultation on ONE fixed fixture and prove the gate is genuinely
    load-bearing, instead of swapping in a different, satisfied registry.
    """
    return dict(getattr(snapshot, "scope_envelope", {}) or {})


def _relation_decision_defect(
    decision: Any,
    *,
    relation_kind: str,
    relation_ref: ExactRef | None,
    source_universe_refs: Sequence[ExactRef],
    target_use: str,
    operation_scope: Any,
) -> str | None:
    """HQ222 F7-RR-04B: does the returned owner decision prove what F7 asked for?

    ``require`` already refuses a non-authorized decision, but it does not promise
    that a non-raising return describes the exact request F7 made. This re-checks
    the returned proof against the request so a permissive owner cannot smuggle an
    unrelated positive relation past F7. Returns a reason string, or None when the
    decision is an exact proof of the request.
    """
    if decision is None:
        return "no owner decision was returned"
    if not getattr(decision, "authorized", False):
        return "returned owner decision is not an authorized decision"
    if getattr(decision, "relation_kind", None) != relation_kind:
        return "returned owner decision carries a different relation kind"
    returned_ref = getattr(decision, "relation_ref", None)
    if returned_ref is None:
        return "returned owner decision carries no authorized relation ref"
    expected_ref = exact_ref(relation_ref, "equivalence_ref") if relation_ref is not None else None
    if expected_ref is not None and returned_ref.key != expected_ref.key:
        return "returned owner decision authorized a different relation ref"
    if getattr(decision, "authority_ref", None) is None:
        return "returned owner decision names no relation-authorizing authority"
    returned_sources = tuple(getattr(decision, "source_universe_refs", ()) or ())
    if len(returned_sources) != len(source_universe_refs) or {
            ref.key for ref in returned_sources} != {ref.key for ref in source_universe_refs}:
        return "returned owner decision covers a different source universe pair"
    if canonicalize(getattr(decision, "target_use", None)) != canonicalize(target_use):
        return "returned owner decision was adjudicated for a different target use"
    if canonicalize(getattr(decision, "operation_scope", None)) != canonicalize(
            operation_scope):
        return "returned owner decision was adjudicated for a different operation scope"
    return None


def _scope_covers_exact_ref_set(scope_value: Any, target_ref: Any) -> bool:
    """HQ219 RR-03: does this scope value cover the exact target ref by FULL identity?

    Complete ExactRef identity (kind + object_id + content_hash) is required. A bare
    object_id token is not coverage, and absence is not coverage. This mirrors
    ``_scope_covers_governed_use`` deliberately, so identity coverage and governed-use
    coverage are judged by one rule.
    """
    if isinstance(scope_value, str):
        # HQ222 F7-RR-02C: BOTH adopted explicit-unrestricted literals count.
        # Nothing else does, and omission is not unrestricted.
        return _scope_is_adopted_unrestricted(scope_value)
    if not isinstance(scope_value, (set, frozenset, list, tuple)):
        return False
    target = target_ref.as_dict() if hasattr(target_ref, "as_dict") else target_ref
    target = canonicalize(target)
    for entry in scope_value:
        if isinstance(entry, str):
            continue  # a bare object_id token is not exact coverage
        candidate = canonicalize(entry)
        if candidate == target:
            return True
    return False


def _scope_covers_governed_use(scope_value: Any, governed_use_ref: Any) -> bool:
    """HQ217 RR-02: governed-use scope must match the COMPLETE ExactRef identity.

    ExactRef identity is kind + object_id + content_hash. The previous check compared a
    bare object_id, so two DIFFERENT exact governed-use refs that shared only an
    object_id both satisfied the same scope. A scope entry now covers the governed use
    only when it names the full exact identity. A bare object_id token in scope is NOT
    sufficient evidence of governed-use scope and is treated as no coverage (fail-closed).
    """
    if isinstance(scope_value, str):
        # HQ222 F7-RR-02C: both adopted explicit-unrestricted literals count.
        return _scope_is_adopted_unrestricted(scope_value)
    if not isinstance(scope_value, (set, frozenset, list, tuple)):
        return False
    target = governed_use_ref.as_dict() if hasattr(governed_use_ref, "as_dict") else governed_use_ref
    target = canonicalize(target)
    for entry in scope_value:
        if isinstance(entry, str):
            # A bare token carries no content_hash, so it cannot evidence exact scope.
            continue
        candidate = entry.as_dict() if hasattr(entry, "as_dict") else entry
        if canonicalize(candidate) == target:
            return True
    return False


def _scope_covers_universe(scope_value: Any, universe: Any) -> bool:
    # HQ222 F7-RR-02C: both adopted explicit-unrestricted literals count; omission
    # does not, and a bare string token still is not exact universe coverage.
    if isinstance(scope_value, str):
        return _scope_is_adopted_unrestricted(scope_value)
    if isinstance(scope_value, (set, frozenset, list, tuple)):
        target = canonicalize(universe)
        return any(canonicalize(v) == target for v in scope_value)
    return False


def resolve_required_authority(
    registry: AuthorityRegistry | None,
    ref: AuthorityRef | None,
    *,
    slot: str,
    authority_kind: str,
    operation: str | None = None,
    governed_use_id: str | None = None,
    required_universe_refs: Sequence[Any] = (),
    require_use_scope: bool = False,
) -> tuple[AuthorityResolutionRecord, AuthoritySnapshot | None]:
    """Resolve one contract-required authority to a typed outcome.

    Presence of a ref string is never enough: the exact snapshot must exist,
    its immutable content hash must match, the exact operation must be governed,
    and any required scope must actually cover the bound material.
    """
    if ref is None:
        return AuthorityResolutionRecord(slot, authority_kind, None, ABSENT), None
    if registry is None:
        # F-NONE-01: a missing registry is a typed absence, never an AttributeError.
        return AuthorityResolutionRecord(
            slot, authority_kind, ref, ABSENT, "no exact authority registry supplied"), None

    try:
        resolution = registry.resolve_exact(ref)
        snapshot = resolution.snapshot
    except Pre553AuthorityConflict as exc:
        return AuthorityResolutionRecord(
            slot, authority_kind, ref, CONFLICT, str(exc), operation, governed_use_id), None
    except Pre553AuthorityError as exc:
        # An exact ref that names a known authority id/version but a different
        # content hash is a real immutable-integrity violation, not mere absence.
        for candidate in _known_snapshots(registry):
            if (candidate.authority_id == ref.authority_id
                    and candidate.authority_version == ref.authority_version):
                if candidate.authority_ref.authority_content_hash != ref.authority_content_hash:
                    return AuthorityResolutionRecord(
                        slot, authority_kind, ref, HASH_MISMATCH,
                        "bound exact ref content hash differs from the registered "
                        "immutable authority content hash",
                        operation, governed_use_id), None
                return AuthorityResolutionRecord(
                    slot, authority_kind, ref, ABSENT,
                    "exact authority is not registered under this exact ref",
                    operation, governed_use_id), None
        return AuthorityResolutionRecord(
            slot, authority_kind, ref, ABSENT, str(exc), operation, governed_use_id), None

    if snapshot.authority_ref != ref:
        return AuthorityResolutionRecord(
            slot, authority_kind, ref, HASH_MISMATCH,
            "resolved snapshot content hash differs from the bound exact ref",
            operation, governed_use_id), None

    if snapshot.authority_kind != authority_kind:
        return AuthorityResolutionRecord(
            slot, authority_kind, ref, SCOPE_MISMATCH,
            f"exact authority kind is {snapshot.authority_kind}", operation, governed_use_id), None

    if snapshot.decision_state != "ALLOW":
        outcome = OUT_OF_SCOPE if snapshot.decision_state == "OUT_OF_SCOPE" else ABSENT
        return AuthorityResolutionRecord(
            slot, authority_kind, ref, outcome,
            f"exact decision_state is {snapshot.decision_state}", operation, governed_use_id), None

    try:
        require_positive_authority(snapshot, authority_kind=authority_kind, operation=operation)
    except Pre553AuthorityError as exc:
        text = str(exc)
        if "hash" in text.lower():
            outcome = HASH_MISMATCH
        elif "scope" in text.lower():
            outcome = SCOPE_MISMATCH
        else:
            outcome = SCOPE_MISMATCH
        return AuthorityResolutionRecord(
            slot, authority_kind, ref, outcome, text, operation, governed_use_id), None

    scope = snapshot.scope_envelope
    for universe in required_universe_refs:
        if not _scope_covers_universe(scope.get("source_universe_refs"), universe):
            return AuthorityResolutionRecord(
                slot, authority_kind, ref, SCOPE_MISMATCH,
                "exact authority scope does not cover a bound source universe",
                operation, governed_use_id), None

    # HQ219 RR-02B: a use-scoped authority must carry EXPLICIT governed-use coverage.
    #
    # Previously the coverage check ran only when ``target_use_refs`` happened to be
    # present, so a positive snapshot whose scope envelope OMITTED it still resolved
    # POSITIVE. Absence is not coverage: omitting the key asserted nothing, and reading
    # that silence as unrestricted would let an authority authorize a governed use it
    # never named.
    #
    # An EXPLICIT unrestricted marker is still honoured -- that is a positive, deliberately
    # authored representation recognised by ``_scope_covers_governed_use``, which is a
    # different thing from omitting the key. Only the omission fails closed. This single
    # site governs every F7 path that declares use scope required, which includes both
    # TEMPORAL_COMPARABILITY and TARGET_USE_PERMISSION.
    if require_use_scope and governed_use_id is not None:
        governed = scope.get("target_use_refs")
        if governed is None:
            return AuthorityResolutionRecord(
                slot, authority_kind, ref, SCOPE_MISMATCH,
                "use-scoped authority declares no governed-use coverage: its scope envelope "
                "omits target_use_refs, and absence is not coverage",
                operation, governed_use_id), None
        if not _scope_covers_governed_use(governed, governed_use_id):
            return AuthorityResolutionRecord(
                slot, authority_kind, ref, SCOPE_MISMATCH,
                "exact authority scope does not cover the governed use",
                operation, governed_use_id), None

    return AuthorityResolutionRecord(
        slot, authority_kind, ref, POSITIVE, None, operation, governed_use_id), snapshot


# ---------------------------------------------------------------------------
# request / receipt
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TemporalComparisonRequest:
    """Exact bounded request. Nothing is inferred, defaulted, or minted."""

    # exact identity and pair material
    temporal_identity_contract_ref: Any
    anchor_refs: Any
    observation_refs: Any
    source_universe_refs: Any
    governed_use_id: Any

    # order law
    temporal_order_disposition: str
    temporal_order_basis_ref: Any = None

    # required authority surface, all exact AuthorityRefs
    temporal_comparability_authority_ref: Any = None
    temporal_order_basis_authority_ref: Any = None
    temporal_evidence_authority_ref: Any = None
    estimand_authority_refs: Any = ()
    measure_authority_refs: Any = ()
    target_use_permission_refs: Any = ()
    uncertainty_authority_ref: Any = None
    replay_protocol_authority_ref: Any = None
    native_canonical_mapping_authority_ref: Any = None
    source_equivalence_authority_ref: Any = None

    # exact refs required by the contract
    comparability_requirements_ref: Any = None
    source_equivalence_ref: Any = None
    native_canonical_mapping_ref: Any = None

    # HQ217 RR-01/RR-03/RR-04: the exact material each contract ref names. A ref token
    # alone is not proof, so the material is supplied and its hash must equal the ref's
    # content_hash. The surfaces consumed below are derived from THIS material.
    comparability_requirements_material: Any = None
    temporal_identity_contract_material: Any = None

    # HQ217 RR-04: the exact source-relation OWNER PATH. source_equivalence_ref is
    # resolved through this resolver, never accepted as a caller-trusted token.
    source_relation_resolver: Any = None

    # bound comparison operation and quantity surface (Repair 5)
    comparison_operation: str = AUTHORIZED_COMPARISON_OPERATION
    quantity_surface: Any = None

    uncertainty_state: str = "QUANTIFIED_UNDER_BOUND_METHOD"
    intervening_span_state: str = "NO_INTERVENING_GAP"
    family_mapping_required: bool = False
    intervals_overlap: bool = False
    identity_surface_jointly_satisfied: bool = True
    comparability_requirement_results: tuple[Mapping[str, Any], ...] = ()
    prior_f7_state: str | None = None


@dataclass(frozen=True)
class TemporalRelationReceipt:
    """Module-local closed content-addressed receipt.

    Deliberately NOT a ``CanonicalSemanticObject``. ``relation_state`` is a
    receipt-local validated closed field, never a ``typed_state``. Field names
    are the accepted contract's own names.
    """

    receipt_id: str
    temporal_identity_contract_ref: dict[str, str] | None
    anchor_refs: tuple[dict[str, str], ...]
    temporal_order_disposition: str
    temporal_order_basis_ref: dict[str, str] | None
    comparability_status: str
    comparability_requirement_results: tuple[dict[str, Any], ...]
    relation_status: str
    direction_claim: str
    quantity_surface: dict[str, Any]
    delta: dict[str, Any] | None
    non_delta_presence: str
    uncertainty_state: str
    intervening_span_state: str
    relation_state: str
    relation_state_reason: str
    governed_use_id: dict[str, str]
    authority_snapshot_refs: tuple[dict[str, str], ...]
    provenance: dict[str, Any]
    receipt_hash: str

    def as_material(self) -> dict[str, Any]:
        """Exact deterministic replay material; excludes ``receipt_hash``."""
        return {
            "receipt_id": self.receipt_id,
            "temporal_identity_contract_ref": self.temporal_identity_contract_ref,
            "anchor_refs": [dict(r) for r in self.anchor_refs],
            "temporal_order_disposition": self.temporal_order_disposition,
            "temporal_order_basis_ref": self.temporal_order_basis_ref,
            "comparability_status": self.comparability_status,
            "comparability_requirement_results": [dict(r) for r in self.comparability_requirement_results],
            "relation_status": self.relation_status,
            "direction_claim": self.direction_claim,
            "quantity_surface": self.quantity_surface,
            "delta": self.delta,
            "non_delta_presence": self.non_delta_presence,
            "uncertainty_state": self.uncertainty_state,
            "intervening_span_state": self.intervening_span_state,
            "relation_state": self.relation_state,
            "relation_state_reason": self.relation_state_reason,
            "governed_use_id": self.governed_use_id,
            "authority_snapshot_refs": [dict(r) for r in self.authority_snapshot_refs],
            "provenance": self.provenance,
        }

    def replay_identity(self) -> str:
        return semantic_hash(self.as_material())


def _request_field_names() -> tuple[str, ...]:
    return tuple(f.name for f in __import__("dataclasses").fields(TemporalComparisonRequest))


def _select_reason(state: str, detected: Sequence[str]) -> str:
    allowed = STATE_REASON_PRECEDENCE[state]
    for reason in allowed:
        if reason in detected:
            return reason
    return allowed[0]


def _validate_kind_ceiling_pairing() -> None:
    if TEMPORAL_COMPARABILITY_AUTHORITY_KIND not in AUTHORITY_KINDS:
        raise TemporalComparabilityIntegrityError(
            "TEMPORAL_COMPARABILITY must be an exact registered authority kind")
    if TEMPORAL_COMPARABILITY_AUTHORITY_KIND not in AUTHORITY_KIND_CEILINGS:
        raise TemporalComparabilityIntegrityError(
            "TEMPORAL_COMPARABILITY requires exactly one matching ceiling entry")
    for kind in AUTHORITY_KIND_CEILINGS:
        if kind not in AUTHORITY_KINDS:
            raise TemporalComparabilityIntegrityError(f"ceiling without kind: {kind}")
    if set(AUTHORITY_KINDS) != set(AUTHORITY_KIND_CEILINGS):
        raise TemporalComparabilityIntegrityError(
            "every authority kind must have exactly one ceiling entry")


#: The live frozen surface, consulted rather than copied (Repair 9).
def _frozen_backfill_targets() -> frozenset[str]:
    return frozenset(_adopted_source_relations.FORBIDDEN_BACKFILL_TARGET_STATES)


def temporal_backfill_refused(relation_state: str) -> bool:
    """True when the live frozen surface forbids this state as a backfill target."""
    return relation_state in _frozen_backfill_targets()


def compare_temporal_anchors(
    request: TemporalComparisonRequest,
    registry: AuthorityRegistry | None = None,
) -> TemporalRelationReceipt:
    """Compare exactly two authorized temporal anchors under bound material.

    Deterministic: identical exact inputs and authority material always yield an
    identical receipt identity. ``relation_state`` is never caller-chosen.
    """
    _validate_kind_ceiling_pairing()

    # ---- Repair 7: prior F7 state participates, or refuses with no receipt ----
    prior_refusals: list[str] = []
    if request.prior_f7_state is not None:
        if request.prior_f7_state in PRIOR_F7_NO_RECEIPT_STATES:
            raise TemporalComparabilityError(
                f"{request.prior_f7_state} yields no temporal relation receipt")
        if request.prior_f7_state not in PRIOR_F7_STATE_MAP:
            raise TemporalComparabilityIntegrityError(
                f"unknown prior F7 state: {request.prior_f7_state}")
        prior_refusals.append(PRIOR_F7_STATE_MAP[request.prior_f7_state])

    disposition = request.temporal_order_disposition
    if disposition not in ORDER_DISPOSITIONS:
        raise TemporalComparabilityIntegrityError(f"unknown order disposition: {disposition}")

    # ---- Repair 3: exact cardinality, 2 anchors and 2 bound observations ----
    anchors = _require_ref_tuple(request.anchor_refs, "anchor_refs")
    observations = _require_ref_tuple(request.observation_refs, "observation_refs")
    universes = _require_ref_tuple(request.source_universe_refs, "source_universe_refs")
    if len(anchors) > 2:
        raise TemporalComparabilityInputRefusal(
            "exactly two authorized anchors are required; "
            f"{len(anchors)} supplied (contract exact_cardinality=2)")
    if len(universes) > 2:
        raise TemporalComparabilityInputRefusal(
            "at most two source-universe refs are required; "
            f"{len(universes)} supplied (contract exact_cardinality=2)")
    if len(observations) != 2:
        raise TemporalComparabilityInputRefusal(
            "exactly two observation refs are required, one per anchor; "
            f"{len(observations)} supplied")
    if len(universes) != 2:
        raise TemporalComparabilityInputRefusal(
            "exactly two source-universe refs are required, one per anchor; "
            f"{len(universes)} supplied")
    cardinality_short = len(anchors) < 2
    bound_observation_bindings = tuple(
        {"anchor": a.as_dict(), "observation": o.as_dict()}
        for a, o in zip(anchors, observations))
    if cardinality_short:
        bound_observation_bindings = ()

    governed_use_id = _require_ref(request.governed_use_id, "governed_use_id")

    identity_ref = None
    identity_material: Mapping[str, Any] | None = None
    if request.temporal_identity_contract_ref is not None:
        identity_ref = _require_ref(request.temporal_identity_contract_ref,
                                    "temporal_identity_contract_ref")
        identity_material = _bind_ref_to_material(
            identity_ref, request.temporal_identity_contract_material,
            ref_slot="temporal_identity_contract_ref",
            material_slot="temporal_identity_contract_material")

    # ---- Repair 4: comparability_requirements_ref is required and resolved ----
    if request.comparability_requirements_ref is None:
        raise TemporalComparabilityInputRefusal(
            "comparability_requirements_ref is contract-required")
    requirements_ref = _require_ref(request.comparability_requirements_ref,
                                    "comparability_requirements_ref")
    requirements_material = _bind_ref_to_material(
        requirements_ref, request.comparability_requirements_material,
        ref_slot="comparability_requirements_ref",
        material_slot="comparability_requirements_material")
    # The consumed surface set is DERIVED from the bound material, so the ref governs
    # the derivation instead of accompanying it.
    bound_requirement_results = tuple(
        dict(r) for r in (requirements_material.get("requirement_results")
                          if isinstance(requirements_material, Mapping)
                          else requirements_material))

    mapping_ref = None
    if request.native_canonical_mapping_ref is not None:
        mapping_ref = _require_ref(request.native_canonical_mapping_ref,
                                   "native_canonical_mapping_ref")
    equivalence_ref = None
    if request.source_equivalence_ref is not None:
        equivalence_ref = _require_ref(request.source_equivalence_ref, "source_equivalence_ref")
    basis_ref = None
    if (disposition in AUTHORIZED_ORDER_BASES
            and request.temporal_order_basis_ref is None):
        # RR-06: an authorized disposition with no basis ref is the accepted
        # insufficient-authority terminal, not a cross-field IntegrityError.
        missing_basis_ref = True
    else:
        missing_basis_ref = False
    if request.temporal_order_basis_ref is not None:
        if disposition == NO_BASIS_DISPOSITION:
            raise TemporalComparabilityIntegrityError(
                "ORDER_UNKNOWN_NONCOMPARABLE must carry no basis ref")
        basis_ref = _require_ref(request.temporal_order_basis_ref, "temporal_order_basis_ref")

    if request.uncertainty_state not in UNCERTAINTY_STATES:
        raise TemporalComparabilityIntegrityError("unknown uncertainty_state")
    if request.intervening_span_state not in INTERVENING_SPAN_STATES:
        raise TemporalComparabilityIntegrityError("unknown intervening_span_state")

    # ---- Repair 8: cross-universe is material-derived, never a caller boolean ----
    crosses_universes = universes[0].key != universes[1].key

    detected: list[str] = []
    resolutions: list[AuthorityResolutionRecord] = []
    positive_snapshots: list[AuthoritySnapshot] = []
    #: HQ219 RR-03: the POSITIVE snapshot resolved for each slot, keyed by slot name.
    #: The identity gate reads the TEMPORAL_EVIDENCE snapshot from here, so the
    #: joint-satisfaction fact comes from the adopted authority that owns identity
    #: material rather than from caller-supplied material.
    slot_snapshots: dict[str, AuthoritySnapshot] = {}

    def resolve(slot, ref, kind, *, operation=None, universe_refs=(), use_scope=False):
        record, snapshot = resolve_required_authority(
            registry, ref, slot=slot, authority_kind=kind, operation=operation,
            governed_use_id=governed_use_id,
            required_universe_refs=universe_refs, require_use_scope=use_scope)
        resolutions.append(record)
        if snapshot is not None:
            positive_snapshots.append(snapshot)
            slot_snapshots[slot] = snapshot
        return record

    # ---- Repair 1 + 2: every required authority resolved to a typed outcome ----
    tc = resolve("temporal_comparability", request.temporal_comparability_authority_ref,
                 TEMPORAL_COMPARABILITY_AUTHORITY_KIND,
                 operation=request.comparison_operation, use_scope=True)
    if tc.outcome != POSITIVE:
        detected.append({
            CONFLICT: "TEMPORAL_COMPARABILITY_AUTHORITY_CONFLICT",
            OUT_OF_SCOPE: "TEMPORAL_COMPARABILITY_AUTHORITY_OUT_OF_SCOPE",
            HASH_MISMATCH: "AUTHORITY_HASH_MISMATCH",
            SCOPE_MISMATCH: "AUTHORITY_SCOPE_MISMATCH",
        }.get(tc.outcome, "TEMPORAL_COMPARABILITY_AUTHORITY_REF_ABSENT"))

    # HQ222 F7-RR-03B: the identity-owning TEMPORAL_EVIDENCE authority must cover the
    # exact compared source scope. It was previously resolved with no required
    # universes, so an actual but out-of-scope TEMPORAL_EVIDENCE snapshot could own
    # identity for this comparison purely because it carried the identity scope keys.
    # Accepted owner archaeology treats temporal identity as source-native scoping
    # material, so the owner must be in-scope for the pair being compared.
    te = resolve("temporal_evidence", request.temporal_evidence_authority_ref,
                 "TEMPORAL_EVIDENCE",
                 universe_refs=(universes[0], universes[1]))
    if te.outcome != POSITIVE:
        detected.append({
            HASH_MISMATCH: "AUTHORITY_HASH_MISMATCH",
            SCOPE_MISMATCH: "AUTHORITY_SCOPE_MISMATCH",
        }.get(te.outcome, "TEMPORAL_EVIDENCE_AUTHORITY_REF_ABSENT_FOR_ANCHOR"))

    if disposition in AUTHORIZED_ORDER_BASES:
        tb = resolve("temporal_order_basis", request.temporal_order_basis_authority_ref,
                     "TEMPORAL_EVIDENCE")
        if tb.outcome != POSITIVE:
            detected.append({
                HASH_MISMATCH: "AUTHORITY_HASH_MISMATCH",
                SCOPE_MISMATCH: "AUTHORITY_SCOPE_MISMATCH",
            }.get(tb.outcome, "TEMPORAL_ORDER_BASIS_AUTHORITY_REF_ABSENT"))

    # Every supplied target-use permission ref is resolved, not only element zero. A
    # silently ignored additional permission was a real gap: the receipt would claim a
    # governed use that one bound permission did not cover.
    tp_refs = tuple(request.target_use_permission_refs or ())
    if not tp_refs:
        detected.append("TARGET_USE_PERMISSION_REF_ABSENT")
    for index, tp_ref in enumerate(tp_refs):
        slot = "target_use_permission" if index == 0 else f"target_use_permission[{index}]"
        tp = resolve(slot, tp_ref, "TARGET_USE_PERMISSION", universe_refs=(), use_scope=True)
        if tp.outcome != POSITIVE:
            detected.append({
                HASH_MISMATCH: "AUTHORITY_HASH_MISMATCH",
                SCOPE_MISMATCH: "AUTHORITY_SCOPE_MISMATCH",
            }.get(tp.outcome, "TARGET_USE_PERMISSION_REF_ABSENT"))

    um = resolve("uncertainty_method", request.uncertainty_authority_ref, "UNCERTAINTY_METHOD")
    if um.outcome != POSITIVE:
        detected.append({
            HASH_MISMATCH: "AUTHORITY_HASH_MISMATCH",
            SCOPE_MISMATCH: "AUTHORITY_SCOPE_MISMATCH",
        }.get(um.outcome, "UNCERTAINTY_METHOD_REF_ABSENT"))
        uncertainty_state = "UNCERTAINTY_METHOD_ABSENT"
    else:
        # A quantified claim requires a positively resolved exact uncertainty
        # method; without one the claim may not be presented as quantified.
        uncertainty_state = ("QUANTIFIED_UNDER_BOUND_METHOD"
                             if request.uncertainty_state == "QUANTIFIED_UNDER_BOUND_METHOD"
                             else request.uncertainty_state)

    rp = resolve("replay_protocol", request.replay_protocol_authority_ref, "REPLAY_PROTOCOL")
    if rp.outcome != POSITIVE:
        detected.append({
            HASH_MISMATCH: "AUTHORITY_HASH_MISMATCH",
            SCOPE_MISMATCH: "AUTHORITY_SCOPE_MISMATCH",
        }.get(rp.outcome, "REPLAY_PROTOCOL_REF_ABSENT"))

    est_refs = _require_authority_tuple(request.estimand_authority_refs, "estimand_authority_refs")
    est_snapshots = []
    for index, ref in enumerate(est_refs):
        est_snapshots.append(resolve(f"estimand[{index}]", ref, "WEIGHT_DESIGN_ESTIMAND"))
    if not est_snapshots or any(r.outcome != POSITIVE for r in est_snapshots):
        detected.append("ESTIMAND_AUTHORITY_NOT_POSITIVE")
    elif len({r.authority_ref.key for r in est_snapshots}) > 1:
        detected.append("ESTIMANDS_DIFFER")

    mea_refs = _require_authority_tuple(request.measure_authority_refs, "measure_authority_refs")
    mea_snapshots = []
    for index, ref in enumerate(mea_refs):
        mea_snapshots.append(resolve(f"measure[{index}]", ref, "WEIGHT_DESIGN_ESTIMAND"))
    if not mea_snapshots or any(r.outcome != POSITIVE for r in mea_snapshots):
        detected.append("MEASURE_AUTHORITY_NOT_POSITIVE")
    elif len({r.authority_ref.key for r in mea_snapshots}) > 1:
        detected.append("MEASURE_OR_WEIGHT_DESIGN_DIFFERS")

    if request.family_mapping_required:
        nm = resolve("native_canonical_mapping", request.native_canonical_mapping_authority_ref,
                     "NATIVE_CANONICAL_MAPPING_HARMONIZATION")
        if mapping_ref is None:
            detected.append("NATIVE_CANONICAL_MAPPING_REF_ABSENT")
        elif nm.outcome != POSITIVE:
            detected.append("FAMILY_MAPPING_NOT_POSITIVELY_AUTHORIZED")

    # Cross-universe two independent positive paths (Repair 8).
    if crosses_universes:
        if equivalence_ref is None:
            detected.append("SOURCE_EQUIVALENCE_REF_ABSENT")
        else:
            # RR-04: resolve the relation through the exact source-relation OWNER PATH
            # first. An arbitrary caller token must never be accepted here.
            resolver = request.source_relation_resolver
            #: HQ222 F7-RR-04B: the exact owner decision, once captured. Stays None
            #: unless the adopted owner returned a real AUTHORIZED decision, so a
            #: later cross-bind can never read an unproven authority.
            relation_decision = None
            if resolver is None:
                detected.append("SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE")
            else:
                # HQ219 RR-04: exact object lookup is NOT adjudication.
                #
                # ``resolve_exact`` returns whatever relation carries the requested ref.
                # It does not require the relation to be AUTHORIZED, does not check the
                # relation KIND, does not check that the relation binds the exact
                # universe PAIR, and does not check scope, use, or authority. A
                # duck-typed stub, a DENIED relation, a relation of another kind, and a
                # relation for a different pair all satisfied it, while an independent
                # positive SOURCE_EQUIVALENCE snapshot satisfied the authority half. That
                # split brain is the defect.
                #
                # The adopted owner exposes exactly the adjudication this needs:
                # ``require`` runs ``decide`` and refuses unless the decision is
                # AUTHORIZED, and the owner itself validates relation kind, the exact
                # source pair, operation scope, effective scope, target use, and the
                # authority that authorizes the relation. F7 therefore consumes the real
                # owner decision and creates no equivalence authority of its own.
                if not isinstance(resolver, SourceRelationResolver):
                    # A stub that merely mimics ``resolve_exact`` is not the owner path.
                    detected.append("SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE")
                else:
                    # ------------------------------------------------------
                    # HQ222 F7-RR-04B: CONSERVE THE OWNER'S ACTUAL DECISION.
                    #
                    # HQ219 called the adopted owner and then discarded the
                    # returned RelationDecision, manufacturing a local POSITIVE
                    # record from the requested ref instead. The adopted owner
                    # returns the exact authorized ``relation_ref`` AND the exact
                    # relation-authorizing ``authority_ref``. Discarding it proved
                    # only "some owner decision is positive", while the separately
                    # supplied SOURCE_EQUIVALENCE snapshot B proved only "some
                    # caller-supplied snapshot is positive". Positive + positive is
                    # not identity: a genuine relation authorized by A could ride
                    # alongside an unrelated positive B, and the receipt then
                    # misstated its authority ancestry.
                    #
                    # The returned decision is now captured, its exact identity is
                    # validated against what F7 actually asked for, and its exact
                    # relation-authorizing authority is what F7 records.
                    # ------------------------------------------------------
                    try:
                        relation_decision = resolver.require(
                            relation_kind=SOURCE_EQUIVALENCE_REQUIRED_RELATION_KIND,
                            source_universe_refs=(universes[0], universes[1]),
                            operation_scope=SOURCE_EQUIVALENCE_REQUIRED_SCOPE,
                            target_use=(governed_use_id.object_id
                                        if governed_use_id is not None else ""),
                            effective_scope=SOURCE_EQUIVALENCE_REQUIRED_SCOPE,
                            relation_ref=equivalence_ref,
                            expected_authority_operation=(
                                SOURCE_EQUIVALENCE_RELATION_OPERATION),
                        )
                    except Exception:
                        relation_decision = None
                        detected.append("SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE")
                    else:
                        defect = _relation_decision_defect(
                            relation_decision,
                            relation_kind=SOURCE_EQUIVALENCE_REQUIRED_RELATION_KIND,
                            relation_ref=equivalence_ref,
                            source_universe_refs=(universes[0], universes[1]),
                            target_use=(governed_use_id.object_id
                                        if governed_use_id is not None else ""),
                            operation_scope=SOURCE_EQUIVALENCE_REQUIRED_SCOPE,
                        )
                        if defect is not None:
                            detected.append("SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE")
                        else:
                            resolutions.append(AuthorityResolutionRecord(
                                "source_equivalence_relation", "SOURCE_EQUIVALENCE",
                                relation_decision.authority_ref, POSITIVE,
                                "exact relation-authorizing authority returned by the "
                                "adopted source-relation owner for the exact relation "
                                "ref, kind, universe pair, scope and use",
                                relation_decision.authority_operation, governed_use_id))
            eq_record, eq_snapshot = resolve_required_authority(
                registry, request.source_equivalence_authority_ref,
                slot="source_equivalence", authority_kind="SOURCE_EQUIVALENCE",
                operation=SOURCE_EQUIVALENCE_RELATION_OPERATION,
                governed_use_id=governed_use_id,
                required_universe_refs=(universes[0], universes[1]), require_use_scope=True)
            resolutions.append(eq_record)
            if eq_snapshot is not None:
                positive_snapshots.append(eq_snapshot)
            if eq_record.outcome != POSITIVE:
                detected.append("SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE")
            else:
                try:
                    validate_relation_authority_only(
                        eq_snapshot,
                        relation_authority_kind="SOURCE_EQUIVALENCE",
                        exact_relation_operation=SOURCE_EQUIVALENCE_RELATION_OPERATION)
                except Pre553AuthorityError:
                    detected.append("SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE")
                else:
                    # ------------------------------------------------------
                    # HQ222 F7-RR-04B, no A/B split: the supplied SOURCE_EQUIVALENCE
                    # snapshot must BE the authority that authorized the returned
                    # relation decision. Two independent positive snapshots that
                    # are not each other are no proof of anything.
                    # ------------------------------------------------------
                    authorized_by = getattr(relation_decision, "authority_ref", None)
                    if authorized_by is not None and (
                            eq_snapshot.authority_ref.key != authorized_by.key):
                        detected.append("SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE")

    # Identity and declared comparability surfaces.
    if cardinality_short:
        detected.append("FEWER_THAN_TWO_AUTHORIZED_ANCHORS")
    if missing_basis_ref:
        detected.append("TEMPORAL_ORDER_BASIS_AUTHORITY_REF_ABSENT")

    if identity_ref is None:
        detected.append("TEMPORAL_IDENTITY_CONTRACT_REF_ABSENT")
    else:
        # ------------------------------------------------------------------
        # HQ219 RR-03: temporal identity must be OWNER-RESOLVED.
        #
        # The previous gate read ``identity_surface_jointly_satisfied`` out of
        # ``temporal_identity_contract_material`` -- material the CALLER supplied and
        # merely hashed. A caller could therefore mint any mapping, hash it, present the
        # matching ExactRef, and satisfy the identity gate with an unrelated positive
        # TEMPORAL_EVIDENCE snapshot sitting in the registry. Hash binding proved only
        # that the caller was self-consistent, never that identity was authorized.
        #
        # The joint-satisfaction fact now comes from the ADOPTED TEMPORAL_EVIDENCE
        # authority -- the owner path that owns identity material. The caller's ref may
        # IDENTIFY which identity contract is requested; it may not itself constitute
        # authorization. No new identity owner, registry, or authority kind is created:
        # this reads the existing TEMPORAL_EVIDENCE snapshot's scope envelope.
        # ------------------------------------------------------------------
        te_snapshot = slot_snapshots.get("temporal_evidence")
        owner_identity_ok = False
        owner_binds_identity = False

        if te_snapshot is None:
            detected.append("TEMPORAL_IDENTITY_OWNER_RESOLUTION_UNAVAILABLE")
        else:
            owner_scope = _temporal_evidence_identity_scope(te_snapshot)
            owner_refs = owner_scope.get("temporal_identity_contract_refs")
            owner_binds_identity = _scope_covers_exact_ref_set(owner_refs, identity_ref)
            if not owner_binds_identity:
                detected.append("TEMPORAL_IDENTITY_NOT_BOUND_BY_TEMPORAL_EVIDENCE_AUTHORITY")
            else:
                owner_identity_ok = bool(
                    owner_scope.get("identity_surface_jointly_satisfied"))

        if owner_binds_identity:
            if not owner_identity_ok:
                detected.append("IDENTITY_SURFACE_NOT_JOINTLY_SATISFIED")
            elif isinstance(identity_material, Mapping) and not bool(
                    identity_material.get("identity_surface_jointly_satisfied")):
                raise TemporalComparabilityInputRefusal(
                    "caller temporal_identity_contract_material claims the identity surface "
                    "is not jointly satisfied, but the TEMPORAL_EVIDENCE authority governs it "
                    "as satisfied; the adopted owner governs")
            elif not request.identity_surface_jointly_satisfied:
                raise TemporalComparabilityInputRefusal(
                    "caller identity_surface_jointly_satisfied contradicts the "
                    "TEMPORAL_EVIDENCE-authorised identity material; the adopted owner governs")

    # RR-01: surfaces come from the bound requirement material. A caller-supplied result
    # tuple that disagrees with it is refused, so the ref cannot be decorative.
    if (request.comparability_requirement_results
            and tuple(dict(r) for r in request.comparability_requirement_results)
            != bound_requirement_results):
        raise TemporalComparabilityInputRefusal(
            "caller comparability_requirement_results disagree with the material bound to "
            "comparability_requirements_ref")
    for surface in NONCOMPARABLE_SURFACES:
        if any(d.get("reason") == surface for d in bound_requirement_results):
            detected.append(surface)

    # Repair 7 material: the prior-F7 refusal is a real detected surface.
    for reason in prior_refusals:
        detected.append(reason)

    # ---- Repair 5: derive the delta under the bound authorized operation ----
    quantity_surface: dict[str, Any] = {}
    derived_delta: Any = None
    delta_authority_ok = tc.outcome == POSITIVE
    if request.comparison_operation != AUTHORIZED_COMPARISON_OPERATION:
        raise TemporalComparabilityInputRefusal(
            f"unsupported comparison operation: {request.comparison_operation}")

    needs_delta = disposition in DIRECTION_PERMITTING_BASES and not cardinality_short
    if request.quantity_surface is None:
        if needs_delta:
            raise TemporalComparabilityInputRefusal(
                "quantity_surface is required to derive an exact delta under the "
                "bound authorized comparison operation")
        quantity_surface = {"presence": "NOT_REQUIRED_FOR_THIS_DISPOSITION"}
    else:
        if not isinstance(request.quantity_surface, Mapping):
            raise TemporalComparabilityIntegrityError("quantity_surface must be an exact mapping")
        missing_keys = [k for k in ("quantity_ref", "earlier_value", "later_value")
                        if k not in request.quantity_surface]
        if missing_keys:
            if needs_delta:
                raise TemporalComparabilityInputRefusal(
                    "the bound authorized comparison operation cannot derive an exact "
                    f"delta: quantity_surface is missing {sorted(missing_keys)}")
            raise TemporalComparabilityIntegrityError(
                f"quantity_surface requires exact {sorted(missing_keys)}")
        quantity_ref = _require_ref(request.quantity_surface["quantity_ref"], "quantity_ref")
        # The quantity must be the bound measure, or the claim is not about it.
        bound_measures = {r.authority_ref.key for r in mea_snapshots if r.authority_ref}
        # RR-05: the quantity surface must name the bound measure on EVERY path. The
        # previous code parsed measure_ref as an ExactRef only, swallowed the resulting
        # exception into None, and then skipped the comparison entirely -- so a valid
        # AuthorityRef fixture serialized as null and a directional delta could be minted
        # with no exact bound measure. Both exact-ref forms are now accepted and compared.
        raw_measure = request.quantity_surface.get("measure_ref")
        if raw_measure is None:
            raise TemporalComparabilityInputRefusal(
                "quantity_surface measure_ref is required and must be the bound measure "
                "authority; a directional delta may never be minted without it")
        measure_identity: dict[str, Any] | None = None
        measure_key: str | None = None
        if hasattr(raw_measure, "as_dict"):
            measure_identity = raw_measure.as_dict()
            measure_key = getattr(raw_measure, "key", None)
        elif isinstance(raw_measure, Mapping):
            measure_identity = dict(raw_measure)
            try:
                measure_key = _require_ref(raw_measure, "measure_ref").key
            except TemporalComparabilityIntegrityError:
                try:
                    measure_key = _require_authority_ref(raw_measure, "measure_ref").key
                except TemporalComparabilityError:
                    measure_key = None
        if measure_key is None:
            raise TemporalComparabilityInputRefusal(
                "quantity_surface measure_ref must be an exact ref or an exact authority ref")
        if bound_measures and measure_key not in bound_measures:
            raise TemporalComparabilityInputRefusal(
                "quantity_surface measure_ref is not the bound measure authority")
        earlier = _exact_number(request.quantity_surface["earlier_value"], "earlier_value")
        later = _exact_number(request.quantity_surface["later_value"], "later_value")
        derived_delta = later - earlier
        quantity_surface = {
            "quantity_ref": quantity_ref.as_dict(),
            "measure_ref": measure_identity,
            "earlier_value": canonicalize(earlier),
            "later_value": canonicalize(later),
            "comparison_operation": request.comparison_operation,
            "observation_binding": [dict(b) for b in bound_observation_bindings],
        }

    # ---- HQ214 adjudication A: typed pre-receipt refusal, never a 13th state ----
    ordered_candidate = needs_delta and not detected
    if ordered_candidate and not delta_authority_ok:
        raise TemporalComparabilityInputRefusal(
            "the bound authorized comparison operation cannot authorize an exact delta")
    if needs_delta and derived_delta is None:
        raise TemporalComparabilityInputRefusal(
            "a direction-permitting authorized basis cannot yield the required exact "
            "delta under the bound comparison operation; refusing before any receipt")

    # ---- HQ214 adjudication C: precedence dominates the isolated CFI-03 tuple ----
    by_state: dict[str, list[str]] = {s: [] for s in RELATION_STATE_PRECEDENCE}
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
    for reason in detected:
        for state in negative_states:
            if reason in STATE_REASON_PRECEDENCE[state]:
                by_state[state].append(reason)
                break

    state: str | None = None
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

    # HQ214 adjudication B.
    comparable = state in COMPARABLE_STATES
    ordered = state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"

    if ordered:
        if _canonical_zero(derived_delta):
            direction_claim = "NO_AUTHORIZED_CHANGE"
        else:
            direction_claim = "INCREASE" if _exact_sign(derived_delta) > 0 else "DECREASE"
        delta_payload = {
            "signed_delta": canonicalize(derived_delta),
            "earlier_value": quantity_surface["earlier_value"],
            "later_value": quantity_surface["later_value"],
            "comparison_operation": request.comparison_operation,
            "zero_basis": "exact signed difference equals canonical zero",
        }
        non_delta_presence = "DELTA_PRESENT"
    else:
        direction_claim = "DIRECTION_NOT_CLAIMABLE"
        delta_payload = None
        non_delta_presence = "DELTA_NOT_CLAIMABLE"

    # RR-07: accepted precedence is total. A partial-order REQUEST may legitimately
    # coincide with a higher-priority terminal failure (for example an unresolved
    # identity). That higher-priority state is emitted; it is never converted into an
    # exception. The partial-order disposition only SELECTS between the two
    # comparable-no-direction states when nothing higher-priority was detected.
    if disposition == "PARTIAL_ORDER_NO_DIRECTION" and state in COMPARABLE_STATES:
        if state not in ("TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION",
                         "TEMPORAL_COMPARABLE_NO_DIRECTION"):
            raise TemporalComparabilityIntegrityError(
                "partial order may only yield the two comparable-no-direction states")

    # Repair 9: consult the live frozen surface on every noncomparable outcome.
    if state == "TEMPORAL_NONCOMPARABLE":
        if not temporal_backfill_refused(state):
            raise TemporalComparabilityIntegrityError(
                "TEMPORAL_NONCOMPARABLE must remain a forbidden backfill target state")

    results = tuple({"reason": r} for r in sorted(set(detected)))

    anchor_material = tuple(a.as_dict() for a in anchors)

    receipt_id = "urn:pyat:f7-temporal-relation:" + semantic_hash({
        "anchors": [a.as_dict() for a in anchors],
        "disposition": disposition,
        "use": governed_use_id.as_dict(),
    })[:32]

    material: dict[str, Any] = {
        "receipt_id": receipt_id,
        "temporal_identity_contract_ref": identity_ref.as_dict() if identity_ref else None,
        "anchor_refs": [dict(a) for a in anchor_material],
        "temporal_order_disposition": disposition,
        "temporal_order_basis_ref": basis_ref.as_dict() if basis_ref else None,
        "comparability_status": "COMPARABLE" if comparable else "NOT_COMPARABLE",
        "comparability_requirement_results": [dict(r) for r in results],
        "relation_status": "ORDERED_RELATION_AUTHORIZED" if ordered else "ORDER_RELATION_REFUSED",
        "direction_claim": direction_claim,
        "quantity_surface": quantity_surface,
        "delta": delta_payload,
        "non_delta_presence": non_delta_presence,
        "uncertainty_state": uncertainty_state,
        "intervening_span_state": request.intervening_span_state,
        "relation_state": state,
        "relation_state_reason": _select_reason(state, detected),
        "governed_use_id": governed_use_id.as_dict(),
        "authority_snapshot_refs": sorted(
            (s.authority_ref.as_dict() for s in positive_snapshots
             if s.authority_ref is not None), key=lambda d: canonical_json(d)),
        "provenance": {
            "comparability_requirements_ref": requirements_ref.as_dict(),
            "comparison_operation": request.comparison_operation,
            "canonical_projection_rule": (
                "semantic_hash over canonical_json of the closed receipt material; "
                "sorted keys, no floats, no NaN/Infinity"),
            "cross_universe": {
                "crosses_source_universes": crosses_universes,
                "derivation": "material-derived from bound per-anchor source_universe_refs",
                "bound_universe_refs": [u.as_dict() for u in universes],
                "source_equivalence_ref": equivalence_ref.as_dict() if equivalence_ref else None,
                "consumed_only_never_minted": True,
            },
            "no_basis_observation": disposition == NO_BASIS_DISPOSITION,
            "authority_resolutions": [r.as_material() for r in resolutions],
            "observation_binding": [dict(b) for b in bound_observation_bindings],
            "prior_f7_state": request.prior_f7_state,
            "declared_comparability_surfaces": [
                dict(d) for d in bound_requirement_results],
            "comparability_requirements_ref": requirements_ref.as_dict(),
            "comparability_requirements_material_hash_bound": True,
        },
    }

    _validate_receipt_cross_field_law(material)
    receipt_hash = semantic_hash(material)
    return TemporalRelationReceipt(
        receipt_id=material["receipt_id"],
        temporal_identity_contract_ref=material["temporal_identity_contract_ref"],
        anchor_refs=tuple(dict(a) for a in material["anchor_refs"]),
        temporal_order_disposition=material["temporal_order_disposition"],
        temporal_order_basis_ref=material["temporal_order_basis_ref"],
        comparability_status=material["comparability_status"],
        comparability_requirement_results=tuple(
            dict(r) for r in material["comparability_requirement_results"]),
        relation_status=material["relation_status"],
        direction_claim=material["direction_claim"],
        quantity_surface=material["quantity_surface"],
        delta=material["delta"],
        non_delta_presence=material["non_delta_presence"],
        uncertainty_state=material["uncertainty_state"],
        intervening_span_state=material["intervening_span_state"],
        relation_state=material["relation_state"],
        relation_state_reason=material["relation_state_reason"],
        governed_use_id=material["governed_use_id"],
        authority_snapshot_refs=tuple(dict(r) for r in material["authority_snapshot_refs"]),
        provenance=material["provenance"],
        receipt_hash=receipt_hash,
    )


def _validate_receipt_cross_field_law(material: Mapping[str, Any]) -> None:
    """CFI-01 through CFI-04 plus the contract's invalid-combination refusals."""
    state = material["relation_state"]
    disposition = material["temporal_order_disposition"]
    basis = material["temporal_order_basis_ref"]
    direction = material["direction_claim"]
    delta = material["delta"]
    relation_status = material["relation_status"]
    reason = material["relation_state_reason"]

    if state not in RELATION_STATES:
        raise TemporalComparabilityIntegrityError("unknown relation state")
    if disposition not in ORDER_DISPOSITIONS:
        raise TemporalComparabilityIntegrityError("unknown order disposition")
    if disposition == NO_BASIS_DISPOSITION and basis is not None:
        raise TemporalComparabilityIntegrityError(
            "ORDER_UNKNOWN_NONCOMPARABLE must carry no basis ref")
    if disposition in AUTHORIZED_ORDER_BASES and basis is None:
        # RR-06: a missing required basis ref is the ACCEPTED insufficient-authority
        # terminal (TEMPORAL_INSUFFICIENT_AUTHORITY /
        # TEMPORAL_ORDER_BASIS_AUTHORITY_REF_ABSENT), not a cross-field integrity
        # error. The absence is reported as a typed refusal state instead.
        if state != "TEMPORAL_INSUFFICIENT_AUTHORITY" or \
                reason != "TEMPORAL_ORDER_BASIS_AUTHORITY_REF_ABSENT":
            raise TemporalComparabilityIntegrityError(
                "an authorized order basis requires an exact basis ref, and no accepted "
                "refusal state reported the absence")
    if disposition == NO_BASIS_DISPOSITION and state == "TEMPORAL_ORDER_UNAUTHORIZED":
        if relation_status != "ORDER_RELATION_REFUSED":
            raise TemporalComparabilityIntegrityError(
                "no-basis must refuse the order relation")
        if direction != "DIRECTION_NOT_CLAIMABLE" or delta is not None:
            raise TemporalComparabilityIntegrityError(
                "no-basis must refuse the direction and carry a null delta")
    if state not in COMPARABLE_STATES and material["comparability_status"] != "NOT_COMPARABLE":
        raise TemporalComparabilityIntegrityError(
            "only the three lawful comparability states may carry COMPARABLE")
    if state in COMPARABLE_STATES and material["comparability_status"] != "COMPARABLE":
        raise TemporalComparabilityIntegrityError(
            "a lawful comparability state must carry COMPARABLE")
    if direction == "DIRECTION_NOT_CLAIMABLE" and delta is not None:
        raise TemporalComparabilityIntegrityError(
            "DIRECTION_NOT_CLAIMABLE must carry a null delta")
    if direction == "NO_AUTHORIZED_CHANGE":
        if not _canonical_zero(delta["signed_delta"]):
            raise TemporalComparabilityIntegrityError(
                "NO_AUTHORIZED_CHANGE requires an exact canonical-zero delta")
    if state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED":
        if disposition not in DIRECTION_PERMITTING_BASES:
            raise TemporalComparabilityIntegrityError(
                "directional claim requires a direction-permitting authorized basis")
        if relation_status != "ORDERED_RELATION_AUTHORIZED":
            raise TemporalComparabilityIntegrityError(
                "directional claim requires ORDERED_RELATION_AUTHORIZED")
        if direction not in ("INCREASE", "DECREASE", "NO_AUTHORIZED_CHANGE"):
            raise TemporalComparabilityIntegrityError(
                "directional claim authorized with a non-claimable direction")
        if delta is None or material["non_delta_presence"] != "DELTA_PRESENT":
            raise TemporalComparabilityIntegrityError(
                "directional claim requires a present exact delta")
    if disposition == "PARTIAL_ORDER_NO_DIRECTION":
        if relation_status != "ORDER_RELATION_REFUSED" or direction != "DIRECTION_NOT_CLAIMABLE":
            raise TemporalComparabilityIntegrityError(
                "partial order must refuse the order relation and the direction")


__all__ = [
    "TEMPORAL_COMPARABILITY_CONTRACT_ID",
    "TEMPORAL_COMPARABILITY_AUTHORITY_KIND",
    "AUTHORIZED_COMPARISON_OPERATION",
    "SOURCE_EQUIVALENCE_RELATION_OPERATION",
    "ORDER_DISPOSITIONS",
    "AUTHORIZED_ORDER_BASES",
    "NO_BASIS_DISPOSITION",
    "DIRECTION_PERMITTING_BASES",
    "DIRECTION_CLAIM_STATES",
    "UNCERTAINTY_STATES",
    "INTERVENING_SPAN_STATES",
    "RELATION_STATE_PRECEDENCE",
    "RELATION_STATES",
    "COMPARABLE_STATES",
    "NEGATIVE_STATES",
    "STATE_REASON_PRECEDENCE",
    "PRIOR_F7_STATE_MAP",
    "PRIOR_F7_NO_RECEIPT_STATES",
    "AuthorityResolutionRecord",
    "TemporalComparabilityError",
    "TemporalComparabilityInputRefusal",
    "TemporalComparabilityIntegrityError",
    "TemporalComparisonRequest",
    "TemporalRelationReceipt",
    "compare_temporal_anchors",
    "resolve_required_authority",
    "temporal_backfill_refused",
]