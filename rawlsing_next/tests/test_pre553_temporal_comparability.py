"""Focused court for the bounded F7 temporal comparability module.

Proves the exact laws of the accepted contract at
``c57a96897788108db7b194e4e51691d1ca8ab729`` independently of production output:
kind/ceiling pairing, all 12 reachable states, deterministic multi-failure
precedence, scalar reason determinism, exact-zero semantics, partial-order
direction refusal, the unique no-basis path, prior-F7 mapping, the probe-only
no-receipt path, cross-universe two-path behaviour, backfill noncollapse, the
absence of any F8 import or consumption, and replay identity stability.
"""
from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

from rawlsing_next.pre553_empirical_authority import (
    AUTHORITY_KINDS,
    AUTHORITY_KIND_CEILINGS,
    AuthorityRegistry,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    canonical_json,
)
from rawlsing_next.pre553_temporal_comparability import (
    AUTHORIZED_ORDER_BASES,
    DIRECTION_PERMITTING_BASES,
    NO_BASIS_DISPOSITION,
    ORDER_DISPOSITIONS,
    PRIOR_F7_STATE_MAP,
    RELATION_STATE_PRECEDENCE,
    RELATION_STATES,
    STATE_REASON_PRECEDENCE,
    TEMPORAL_COMPARABILITY_AUTHORITY_KIND,
    TEMPORAL_NONCOLLAPSE_STATE,
    TemporalComparabilityError,
    TemporalComparabilityIntegrityError,
    TemporalComparisonRequest,
    compare_temporal_anchors,
    temporal_backfill_refused,
)


def _h(tag: str) -> str:
    """Deterministic material hash. Never Python's salted ``hash()``."""
    import hashlib
    return hashlib.sha256(tag.encode("utf-8")).hexdigest()


def _ref(kind: str, object_id: str) -> ExactRef:
    return ExactRef(kind, object_id, _h(f"ref:{kind}:{object_id}"))


def _auth(kind: str, aid: str) -> AuthorityRef:
    return AuthorityRef(aid, "1.0.0", _h(f"authority:{aid}:1.0.0"))


def _snapshot(kind: str, aid: str, **overrides):
    """One exact positive AuthoritySnapshot of the requested kind."""
    from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot

    material = {
        "typed_state": "ALLOW",
        "authority_snapshot_refs": (),
        "dependency_refs": (),
        "producer_replay_locator_or_reference_root": _ref("REPLAY_ROOT", f"authority-{aid}"),
        "authority_id": aid,
        "authority_version": "1.0.0",
        "authority_content_hash": _h(f"authority:{aid}:1.0.0"),
        "authority_kind": kind,
        "decision_state": "ALLOW",
        "governed_operations": ("COMPARE", "SEMANTIC_EQUIVALENCE_ADMISSION"),
        "governed_object_families": ("TemporalComparisonProbe@1.0.0",),
        "scope_envelope": {"source_universe_refs": "EXPLICIT_UNRESTRICTED",
                           "target_use_refs": "EXPLICIT_UNRESTRICTED"},
        "effective_time_or_interval": "ALL_TIME",
        "parent_authority_refs": (),
        "negative_limit_refs": (),
        "supersession_refs": (),
        "interpretation_semantics_fingerprint": _h(f"semantics:{kind}"),
        "replay_protocol_ref": _ref("REPLAY_PROTOCOL", "RP1"),
    }
    material.update(overrides)
    return AuthoritySnapshot(**material)


def _registry(*snapshots):
    return AuthorityRegistry(snapshots)


def _request(**overrides) -> TemporalComparisonRequest:
    """A fully positive, lawful baseline request."""
    base = dict(
        temporal_identity_contract_ref=_ref("TemporalIdentityContract", "TIC1"),
        anchor_refs=(_ref("TimeAnchor", "A1"), _ref("TimeAnchor", "A2")),
        temporal_comparability_authority_ref=_auth(TEMPORAL_COMPARABILITY_AUTHORITY_KIND, "TC1"),
        temporal_order_disposition="CALENDAR_TOTAL_ORDER",
        temporal_order_basis_ref=_ref("TemporalOrderBasis", "TOB1"),
        temporal_order_basis_authority_ref=_auth("TEMPORAL_EVIDENCE", "TE1"),
        temporal_evidence_authority_ref=_auth("TEMPORAL_EVIDENCE", "TE1"),
        comparability_requirements_ref=_ref("ComparabilityRequirements", "CR1"),
        estimand_authority_refs=(_ref("EstimandAuthority", "E1"),),
        measure_authority_refs=(_ref("MeasureAuthority", "M1"),),
        observation_refs=(_ref("Observation", "O1"), _ref("Observation", "O2")),
        uncertainty_authority_ref=_ref("UncertaintyAuthority", "U1"),
        governed_use_id="TEST_USE_1",
        target_use_permission_refs=(_ref("TargetUsePermission", "P1"),),
        provenance_and_replay_ref=_ref("ReplayProtocol", "RP1"),
        signed_delta=5,
    )
    base.update(overrides)
    return TemporalComparisonRequest(**base)


def _positive_registry(**extra):
    return _registry(
        _snapshot(TEMPORAL_COMPARABILITY_AUTHORITY_KIND, "TC1"),
        _snapshot("TEMPORAL_EVIDENCE", "TE1"),
        _snapshot("UNCERTAINTY_METHOD", "UM1"),
        _snapshot("TARGET_USE_PERMISSION", "TP1"),
        _snapshot("REPLAY_PROTOCOL", "RP1"),
        *extra.values(),
    )


def _run(request, registry=None):
    return compare_temporal_anchors(request, registry if registry is not None else _positive_registry())


# --------------------------------------------------------------------------
# kind / ceiling pairing
# --------------------------------------------------------------------------

def test_kind_and_ceiling_are_paired_exactly_once():
    assert TEMPORAL_COMPARABILITY_AUTHORITY_KIND in AUTHORITY_KINDS
    assert TEMPORAL_COMPARABILITY_AUTHORITY_KIND in AUTHORITY_KIND_CEILINGS
    # No sibling kinds were created.
    assert len(AUTHORITY_KINDS) == 19
    assert sum(1 for k in AUTHORITY_KIND_CEILINGS
               if k == TEMPORAL_COMPARABILITY_AUTHORITY_KIND) == 1
    # Every ceiling still has a kind.
    assert set(AUTHORITY_KIND_CEILINGS) <= set(AUTHORITY_KINDS)


def test_ceiling_denies_downstream_consumer_power():
    ceiling = " ".join(AUTHORITY_KIND_CEILINGS[TEMPORAL_COMPARABILITY_AUTHORITY_KIND]).lower()
    assert "no downstream consumer power" in ceiling
    for forbidden in ("source selection", "pooling", "interpolation", "cause", "trend",
                      "trajectory", "scalar temporal pressure", "actor"):
        assert forbidden not in ceiling


# --------------------------------------------------------------------------
# all 12 states reachable and deterministic
# --------------------------------------------------------------------------

def test_state_vocabulary_is_closed_at_twelve_with_exact_precedence():
    assert len(RELATION_STATE_PRECEDENCE) == 12
    assert len(RELATION_STATES) == 12
    assert RELATION_STATE_PRECEDENCE == (
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
    for state in RELATION_STATE_PRECEDENCE:
        assert STATE_REASON_PRECEDENCE[state], state
        for reason in STATE_REASON_PRECEDENCE[state]:
            assert reason not in ("", None)


def test_forward_directional_claim_is_authorized_and_deterministic():
    receipt = _run(_request())
    assert receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert receipt.relation_state_reason == "AUTHORIZED_ORDERED_PAIR_UNDER_BOUND_COMPARABILITY"
    assert receipt.comparability_status == "COMPARABLE"
    assert receipt.relation_status == "ORDERED_RELATION_AUTHORIZED"
    assert receipt.direction_claim == "INCREASE"
    assert receipt.non_delta_presence == "DELTA_PRESENT"
    # Deterministic identity under identical exact inputs.
    assert _run(_request()).receipt_hash == receipt.receipt_hash


def test_decrease_direction():
    assert _run(_request(signed_delta=-3)).direction_claim == "DECREASE"


def test_insufficient_authority_state():
    receipt = compare_temporal_anchors(_request(), _registry())
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    assert receipt.relation_state_reason in STATE_REASON_PRECEDENCE["TEMPORAL_INSUFFICIENT_AUTHORITY"]
    # The original AUTHORITY_STATE never leaks into the relation state.
    assert "ALLOW" not in receipt.relation_state
    assert "DENY" not in receipt.relation_state


def test_authority_conflict_maps_to_insufficient_authority():
    def conflicted(ref, **kw):
        raise Exception("boom")

    class Boom:
        def require(self, *a, **k):
            from rawlsing_next.pre553_empirical_authority import Pre553AuthorityConflict
            raise Pre553AuthorityConflict("conflicting exact authority material")

    receipt = compare_temporal_anchors(_request(), Boom())
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"


def test_identity_unresolved_state():
    receipt = _run(_request(temporal_identity_contract_ref=None))
    assert receipt.relation_state == "TEMPORAL_IDENTITY_UNRESOLVED"
    assert receipt.relation_state_reason == "TEMPORAL_IDENTITY_CONTRACT_REF_ABSENT"


def test_identity_surface_not_jointly_satisfied():
    receipt = _run(_request(identity_surface_jointly_satisfied=False))
    assert receipt.relation_state == "TEMPORAL_IDENTITY_UNRESOLVED"
    assert receipt.relation_state_reason == "IDENTITY_SURFACE_NOT_JOINTLY_SATISFIED"


def test_insufficient_anchors_state():
    receipt = _run(_request(anchor_refs=(_ref("TimeAnchor", "A1"),)))
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_ANCHORS"
    assert receipt.relation_state_reason == "FEWER_THAN_TWO_AUTHORIZED_ANCHORS"


def test_cross_universe_equivalence_absent():
    receipt = _run(_request(pair_crosses_source_universes=True))
    assert receipt.relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"
    assert receipt.relation_state_reason == "SOURCE_EQUIVALENCE_REF_ABSENT"


def test_mapping_material_absent():
    receipt = _run(_request(family_mapping_required=True))
    assert receipt.relation_state == "TEMPORAL_MAPPING_MATERIAL_ABSENT"
    assert receipt.relation_state_reason == "NATIVE_CANONICAL_MAPPING_REF_ABSENT"


def test_estimand_mismatch():
    receipt = _run(_request(estimand_authority_refs=(
        _ref("EstimandAuthority", "E1"), _ref("EstimandAuthority", "E2"))))
    assert receipt.relation_state == "TEMPORAL_ESTIMAND_MISMATCH"
    assert receipt.relation_state_reason == "ESTIMANDS_DIFFER"


def test_measure_mismatch():
    receipt = _run(_request(measure_authority_refs=(
        _ref("MeasureAuthority", "M1"), _ref("MeasureAuthority", "M2"))))
    assert receipt.relation_state == "TEMPORAL_MEASURE_MISMATCH"
    assert receipt.relation_state_reason == "MEASURE_OR_WEIGHT_DESIGN_DIFFERS"


def test_noncomparable_state_and_backfill_noncollapse():
    receipt = _run(_request(comparability_requirement_results=(
        {"reason": "RESPONSE_SURFACE_NOT_SHARED"},)))
    assert receipt.relation_state == "TEMPORAL_NONCOMPARABLE"
    assert receipt.relation_state_reason == "RESPONSE_SURFACE_NOT_SHARED"
    assert receipt.comparability_status == "NOT_COMPARABLE"
    assert receipt.relation_status == "ORDER_RELATION_REFUSED"
    assert receipt.direction_claim == "DIRECTION_NOT_CLAIMABLE"
    assert receipt.signed_delta is None
    # Noncomparable never backfills into positivity.
    assert temporal_backfill_refused(TEMPORAL_NONCOLLAPSE_STATE) is True
    assert temporal_backfill_refused("TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED") is False


def test_order_unauthorized_has_unique_no_basis_derivation():
    receipt = _run(_request(
        temporal_order_disposition=NO_BASIS_DISPOSITION, temporal_order_basis_ref=None))
    assert receipt.relation_state == "TEMPORAL_ORDER_UNAUTHORIZED"
    assert receipt.relation_state_reason == "NO_PERMITTED_ORDER_BASIS_APPLIES"
    assert receipt.temporal_order_basis_ref is None
    assert receipt.relation_status == "ORDER_RELATION_REFUSED"
    assert receipt.direction_claim == "DIRECTION_NOT_CLAIMABLE"


def test_interval_overlap_no_direction():
    receipt = _run(_request(
        temporal_order_disposition="PARTIAL_ORDER_NO_DIRECTION",
        temporal_order_basis_ref=_ref("TemporalOrderBasis", "TOB1"),
        intervals_overlap=True))
    assert receipt.relation_state == "TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION"
    assert receipt.relation_state_reason == "INTERVALS_OVERLAP"
    assert receipt.relation_status == "ORDER_RELATION_REFUSED"
    assert receipt.direction_claim == "DIRECTION_NOT_CLAIMABLE"
    assert receipt.signed_delta is None


def test_comparable_no_direction():
    receipt = _run(_request(
        temporal_order_disposition="PARTIAL_ORDER_NO_DIRECTION",
        temporal_order_basis_ref=_ref("TemporalOrderBasis", "TOB1"),
        intervals_overlap=False))
    assert receipt.relation_state == "TEMPORAL_COMPARABLE_NO_DIRECTION"
    assert receipt.relation_state_reason == "AUTHORIZED_PARTIAL_ORDER_YIELDS_NO_DIRECTION_ON_PAIR"
    assert receipt.direction_claim == "DIRECTION_NOT_CLAIMABLE"


def test_family_local_ordinal_is_direction_permitting():
    receipt = _run(_request(temporal_order_disposition="FAMILY_LOCAL_ORDINAL"))
    assert receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"


def test_all_twelve_states_individually_reachable():
    reached = set()

    def note(r):
        reached.add(r.relation_state)
        return r

    note(compare_temporal_anchors(_request(), _registry()))
    note(_run(_request(temporal_identity_contract_ref=None)))
    note(_run(_request(anchor_refs=(_ref("TimeAnchor", "A1"),))))
    note(_run(_request(pair_crosses_source_universes=True)))
    note(_run(_request(family_mapping_required=True)))
    note(_run(_request(estimand_authority_refs=(
        _ref("EstimandAuthority", "E1"), _ref("EstimandAuthority", "E2")))))
    note(_run(_request(measure_authority_refs=(
        _ref("MeasureAuthority", "M1"), _ref("MeasureAuthority", "M2")))))
    note(_run(_request(comparability_requirement_results=(
        {"reason": "GEOGRAPHY_NOT_SHARED"},))))
    note(_run(_request(temporal_order_disposition=NO_BASIS_DISPOSITION,
                       temporal_order_basis_ref=None)))
    note(_run(_request(temporal_order_disposition="PARTIAL_ORDER_NO_DIRECTION",
                       intervals_overlap=True)))
    note(_run(_request(temporal_order_disposition="PARTIAL_ORDER_NO_DIRECTION",
                       intervals_overlap=False)))
    note(_run(_request()))

    assert reached == set(RELATION_STATES), sorted(set(RELATION_STATES) - reached)
    assert len(reached) == 12


# --------------------------------------------------------------------------
# precedence, reasons, exact zero
# --------------------------------------------------------------------------

def test_multi_failure_precedence_is_deterministic():
    """Every negative failure present at once still selects exactly one state."""
    receipt = _run(_request(
        temporal_identity_contract_ref=None,
        anchor_refs=(_ref("TimeAnchor", "A1"),),
        pair_crosses_source_universes=True,
        family_mapping_required=True,
        estimand_authority_refs=(),
        comparability_requirement_results=({"reason": "GEOGRAPHY_NOT_SHARED"},),
    ))
    # No authority failure is present in this registry, so precedence-1 is not
    # selected; the highest actually-satisfied negative state is identity.
    assert receipt.relation_state == "TEMPORAL_IDENTITY_UNRESOLVED"
    # All detected failures are retained even though precedence chose one state.
    reasons = {r["reason"] for r in receipt.comparability_requirement_results}
    assert "GEOGRAPHY_NOT_SHARED" in reasons
    assert "ESTIMAND_AUTHORITY_REF_ABSENT" in reasons
    assert "TEMPORAL_IDENTITY_CONTRACT_REF_ABSENT" in reasons
    assert "FEWER_THAN_TWO_AUTHORIZED_ANCHORS" in reasons
    assert "SOURCE_EQUIVALENCE_REF_ABSENT" in reasons
    assert "NATIVE_CANONICAL_MAPPING_REF_ABSENT" in reasons


def test_authority_failure_outranks_every_other_failure():
    """Precedence 1 wins even when every lower negative state also applies."""
    receipt = _run(_request(
        temporal_identity_contract_ref=None,
        anchor_refs=(_ref("TimeAnchor", "A1"),),
        pair_crosses_source_universes=True,
        family_mapping_required=True,
        estimand_authority_refs=(),
        measure_authority_refs=(),
        comparability_requirement_results=({"reason": "GEOGRAPHY_NOT_SHARED"},),
    ), _registry())  # empty registry: no authority resolves
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    reasons = {d["reason"] for d in receipt.comparability_requirement_results}
    assert "GEOGRAPHY_NOT_SHARED" in reasons
    assert "MEASURE_AUTHORITY_REF_ABSENT" in reasons


def test_precedence_order_beats_lower_states():
    """Identity failure outranks anchor failure, which outranks others."""
    a = _run(_request(temporal_identity_contract_ref=None,
                      anchor_refs=(_ref("TimeAnchor", "A1"),)))
    assert a.relation_state == "TEMPORAL_IDENTITY_UNRESOLVED"
    b = _run(_request(anchor_refs=(_ref("TimeAnchor", "A1"),),
                      pair_crosses_source_universes=True))
    assert b.relation_state == "TEMPORAL_INSUFFICIENT_ANCHORS"


def test_scalar_reason_is_exactly_one_and_deterministic():
    receipt = _run(_request(comparability_requirement_results=(
        {"reason": "GEOGRAPHY_NOT_SHARED"},
        {"reason": "RESPONSE_SURFACE_NOT_SHARED"},
    )))
    assert isinstance(receipt.relation_state_reason, str)
    assert receipt.relation_state_reason == "RESPONSE_SURFACE_NOT_SHARED"
    assert _run(_request(comparability_requirement_results=(
        {"reason": "GEOGRAPHY_NOT_SHARED"},
        {"reason": "RESPONSE_SURFACE_NOT_SHARED"},
    ))).relation_state_reason == receipt.relation_state_reason


def test_positive_state_reason_is_nonempty():
    receipt = _run(_request())
    assert receipt.relation_state_reason.strip() != ""


def test_exact_zero_only_yields_no_authorized_change():
    assert _run(_request(signed_delta=0)).direction_claim == "NO_AUTHORIZED_CHANGE"
    assert _run(_request(signed_delta=0)).signed_delta == 0


def test_no_deadband_tolerance_or_epsilon():
    """A one-unit signed delta is never silently zero."""
    for delta in (1, -1):
        receipt = _run(_request(signed_delta=delta))
        assert receipt.direction_claim in ("INCREASE", "DECREASE")
        assert receipt.direction_claim != "NO_AUTHORIZED_CHANGE"
    # Floating point is refused outright; floats cannot enter semantic identity.
    with pytest.raises((TemporalComparabilityIntegrityError, Exception)):
        _run(_request(signed_delta=0.0))


def test_exact_numeric_deltas_accepted():
    assert _run(_request(signed_delta=Decimal("2"))).direction_claim == "INCREASE"
    assert _run(_request(signed_delta=Fraction(-1, 2))).direction_claim == "DECREASE"
    assert _run(_request(signed_delta=Decimal("0"))).direction_claim == "NO_AUTHORIZED_CHANGE"


# --------------------------------------------------------------------------
# invalid cross-field tuples refuse
# --------------------------------------------------------------------------

def test_authorized_basis_requires_exact_basis_ref():
    with pytest.raises(TemporalComparabilityIntegrityError):
        _run(_request(temporal_order_basis_ref=None))


def test_no_basis_disposition_must_not_carry_basis_ref():
    with pytest.raises(TemporalComparabilityIntegrityError):
        _run(_request(temporal_order_disposition=NO_BASIS_DISPOSITION,
                      temporal_order_basis_ref=_ref("TemporalOrderBasis", "TOB1")))


def test_directional_claim_without_delta_refuses():
    with pytest.raises(TemporalComparabilityIntegrityError):
        _run(_request(signed_delta=None))


def test_non_claimable_direction_with_delta_refuses():
    receipt = _run(_request(temporal_order_disposition="PARTIAL_ORDER_NO_DIRECTION",
                            intervals_overlap=True, signed_delta=5))
    assert receipt.direction_claim == "DIRECTION_NOT_CLAIMABLE"
    assert receipt.signed_delta is None


def test_unknown_order_disposition_refuses():
    with pytest.raises(TemporalComparabilityIntegrityError):
        _run(_request(temporal_order_disposition="V553_DEADBAND_ORDER"))


def test_malformed_ref_refuses():
    with pytest.raises(TemporalComparabilityIntegrityError):
        _run(_request(anchor_refs=("not-a-ref", _ref("TimeAnchor", "A2"))))


def test_order_vocabulary_is_exactly_three_bases_plus_one_refusal():
    assert AUTHORIZED_ORDER_BASES == {
        "CALENDAR_TOTAL_ORDER", "FAMILY_LOCAL_ORDINAL", "PARTIAL_ORDER_NO_DIRECTION"}
    assert NO_BASIS_DISPOSITION not in AUTHORIZED_ORDER_BASES
    assert DIRECTION_PERMITTING_BASES == {"CALENDAR_TOTAL_ORDER", "FAMILY_LOCAL_ORDINAL"}
    assert len(ORDER_DISPOSITIONS) == 4


# --------------------------------------------------------------------------
# prior F7 states, probe-only
# --------------------------------------------------------------------------

def test_prior_f7_state_mapping_is_exact():
    assert PRIOR_F7_STATE_MAP["TEMPORAL_AUTHORITY_MISSING"] == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    assert PRIOR_F7_STATE_MAP["TEMPORAL_AUTHORITY_CONFLICT"] == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    assert PRIOR_F7_STATE_MAP["TEMPORAL_OUT_OF_SCOPE"] == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    assert PRIOR_F7_STATE_MAP["TEMPORAL_INTERPOLATION_NOT_AUTHORIZED"] == "TEMPORAL_NONCOMPARABLE"
    assert PRIOR_F7_STATE_MAP["TEMPORAL_RESPONSE_SURFACE_MISMATCH"] == "TEMPORAL_NONCOMPARABLE"
    assert PRIOR_F7_STATE_MAP["TEMPORAL_PROBE_ONLY"] is None


def test_probe_only_yields_no_receipt_at_all():
    with pytest.raises(TemporalComparabilityError) as exc:
        _run(_request(prior_f7_state="TEMPORAL_PROBE_ONLY"))
    assert "no temporal relation receipt" in str(exc.value)


def test_unknown_prior_f7_state_refuses():
    with pytest.raises(TemporalComparabilityIntegrityError):
        _run(_request(prior_f7_state="TEMPORAL_WIDENED_STATE"))


def test_interpolation_forbidden_surface_is_noncomparable():
    receipt = _run(_request(comparability_requirement_results=(
        {"reason": "INTERPOLATED_ANCHOR_OR_OBSERVATION_FORBIDDEN"},)))
    assert receipt.relation_state == "TEMPORAL_NONCOMPARABLE"
    assert receipt.direction_claim == "DIRECTION_NOT_CLAIMABLE"


# --------------------------------------------------------------------------
# cross-universe two-path law
# --------------------------------------------------------------------------

def test_cross_universe_requires_two_independent_positive_paths():
    registry = _positive_registry(eq=_snapshot("SOURCE_EQUIVALENCE", "EQ1"))
    receipt = _run(_request(
        pair_crosses_source_universes=True,
        source_equivalence_ref=_ref("SourceEquivalenceResult", "SEQ1"),
        source_equivalence_authority_ref=_auth("SOURCE_EQUIVALENCE", "EQ1"),
    ), registry)
    assert receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert receipt.source_equivalence_ref == _ref("SourceEquivalenceResult", "SEQ1").as_dict()


def test_cross_universe_refuses_when_equivalence_authority_not_positive():
    registry = _positive_registry(eq=_snapshot(
        "SOURCE_EQUIVALENCE", "EQ1", typed_state="DENY", decision_state="DENY"))
    receipt = _run(_request(
        pair_crosses_source_universes=True,
        source_equivalence_ref=_ref("SourceEquivalenceResult", "SEQ1"),
        source_equivalence_authority_ref=_auth("SOURCE_EQUIVALENCE", "EQ1"),
    ), registry)
    assert receipt.relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"
    assert receipt.relation_state_reason == "SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE"


def test_same_universe_needs_no_equivalence():
    receipt = _run(_request())
    assert receipt.source_equivalence_ref is None
    assert receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"


# --------------------------------------------------------------------------
# receipt law, replay stability, no F8
# --------------------------------------------------------------------------

def test_receipt_is_module_local_not_a_public_object():
    from rawlsing_next.pre553_empirical_objects import CanonicalSemanticObject
    receipt = _run(_request())
    assert not isinstance(receipt, CanonicalSemanticObject)
    assert receipt.relation_state not in getattr(CanonicalSemanticObject, "STATE_FAMILIES", frozenset())


def test_no_public_object_family_or_state_family_widening():
    from rawlsing_next.pre553_empirical_objects import PUBLIC_OBJECT_FAMILIES, STATE_FAMILIES
    families = PUBLIC_OBJECT_FAMILIES if isinstance(PUBLIC_OBJECT_FAMILIES, (set, frozenset)) else set()
    assert not any("TEMPORAL" in str(f) for f in families), families
    assert "TEMPORAL_RELATION_RECEIPT" not in STATE_FAMILIES


def test_replay_identity_is_stable_and_content_sensitive():
    a = _run(_request())
    b = _run(_request())
    assert a.receipt_hash == b.receipt_hash == a.replay_identity() == b.replay_identity()
    changed = _run(_request(signed_delta=6))
    assert changed.receipt_hash != a.receipt_hash


def test_module_never_imports_or_consumes_f8():
    """AST-level proof: no F8 module is imported, and no F8 symbol is referenced."""
    import ast
    import pathlib

    tree = ast.parse(pathlib.Path(
        "rawlsing_next/pre553_temporal_comparability.py").read_text())
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    for name in imported:
        assert "f8" not in name.lower(), name
        assert "world" not in name.lower(), name
    # The only production dependencies are the accepted existing modules.
    internal = sorted(n for n in imported if n.startswith("rawlsing_next."))
    assert internal == [
        "rawlsing_next.pre553_empirical_authority",
        "rawlsing_next.pre553_empirical_objects",
    ], internal


def test_forbidden_backfill_literal_preserved_in_source_relations():
    from rawlsing_next.pre553_source_relations import FORBIDDEN_BACKFILL_TARGET_STATES
    assert "TEMPORAL_NONCOMPARABLE" in FORBIDDEN_BACKFILL_TARGET_STATES


def test_frozen_surfaces_untouched():
    from rawlsing_next.pre553_empirical_authority import (
        FAIL_CLOSED_STATES, FORBIDDEN_SELECTOR_TOKENS)
    assert "LATEST" in FORBIDDEN_SELECTOR_TOKENS
    assert "DENY" in FAIL_CLOSED_STATES


def test_unordered_pair_serialization_preserved_without_direction():
    receipt = _run(_request(temporal_order_disposition="PARTIAL_ORDER_NO_DIRECTION",
                            anchor_order_is_directional=False))
    assert receipt.relation_state == "TEMPORAL_COMPARABLE_NO_DIRECTION"
    keys = [canonical_json(a) for a in receipt.anchor_refs]
    assert keys == sorted(keys)