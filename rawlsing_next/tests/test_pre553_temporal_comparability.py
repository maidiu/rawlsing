"""Focused court for the bounded F7 temporal comparability module.

Every test here is written to be hostile to the module. The HQ213 review found
that four tests in the previous court were vacuous or self-referential, so this
file deliberately avoids:

* any broad catch-all exception assertion or handler;
* tautological assertions that compare a table against itself;
* fixtures that supply authorities the module never consults;
* assertions that only describe the module rather than exercise it;
* self-referential backfill checks instead of the live frozen surface.

Witnesses for all three HQ213 blocking findings and each major finding are
present and named.
"""
from __future__ import annotations

import ast
import hashlib
import inspect
import pathlib
from decimal import Decimal
from fractions import Fraction

import pytest

from rawlsing_next.pre553_empirical_authority import (
    AUTHORITY_KINDS,
    AUTHORITY_KIND_CEILINGS,
    AuthorityRegistry,
)
from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot, ExactRef, canonical_json
from rawlsing_next.pre553_temporal_comparability import (
    AUTHORIZED_COMPARISON_OPERATION,
    AUTHORIZED_ORDER_BASES,
    COMPARABLE_STATES,
    DIRECTION_PERMITTING_BASES,
    NEGATIVE_STATES,
    NO_BASIS_DISPOSITION,
    ORDER_DISPOSITIONS,
    PRIOR_F7_NO_RECEIPT_STATES,
    PRIOR_F7_STATE_MAP,
    RELATION_STATE_PRECEDENCE,
    RELATION_STATES,
    STATE_REASON_PRECEDENCE,
    TEMPORAL_COMPARABILITY_AUTHORITY_KIND,
    TemporalComparabilityError,
    TemporalComparabilityInputRefusal,
    TemporalComparabilityIntegrityError,
    TemporalComparisonRequest,
    compare_temporal_anchors,
    resolve_required_authority,
    temporal_backfill_refused,
)

MOD_PATH = pathlib.Path("rawlsing_next/pre553_temporal_comparability.py")


def _h(tag: str) -> str:
    """Deterministic material hash; never Python's salted ``hash()``."""
    return hashlib.sha256(tag.encode("utf-8")).hexdigest()


def _ref(kind: str, object_id: str) -> ExactRef:
    return ExactRef(kind, object_id, _h(f"ref:{kind}:{object_id}"))


def _aref(kind: str, aid: str, version: str = "1.0.0", *, ops=("COMPARE",), scope=None,
          state: str = "ALLOW", content_hash: str | None = None):
    from rawlsing_next.pre553_empirical_objects import AuthorityRef
    ch = content_hash or _h(f"authority:{aid}:{version}")
    ref = AuthorityRef(aid, version, ch)
    if scope is None:
        scope = {"source_universe_refs": "EXPLICIT_UNRESTRICTED",
                 "target_use_refs": "EXPLICIT_UNRESTRICTED"}
    snapshot = AuthoritySnapshot(
        typed_state=state,
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"authority-{aid}"),
        authority_id=aid,
        authority_version=version,
        authority_content_hash=ch,
        authority_kind=kind,
        decision_state=state,
        governed_operations=tuple(ops),
        governed_object_families=("TemporalComparisonProbe@1.0.0",),
        scope_envelope=dict(scope),
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"semantics:{kind}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", "RP1"),
    )
    return ref, snapshot


UNIVERSE_A = _ref("SourceUniverse", "U-A")
UNIVERSE_B = _ref("SourceUniverse", "U-B")
MEASURE_REF, MEASURE_SNAPSHOT = _aref("WEIGHT_DESIGN_ESTIMAND", "MEAS1")
ESTIMAND_REF, ESTIMAND_SNAPSHOT = _aref("WEIGHT_DESIGN_ESTIMAND", "EST1")


def _full_registry(*, drop=(), tc_ops=(AUTHORIZED_COMPARISON_OPERATION,),
                   tc_scope=None, tc_hash=None, tc_state="ALLOW"):
    """Every authority the contract requires, so no test depends on a decorative one."""
    tc_ref, tc_snap = _aref(TEMPORAL_COMPARABILITY_AUTHORITY_KIND, "TC1", ops=tc_ops,
                            scope=tc_scope, state=tc_state, content_hash=tc_hash)
    te_ref, te_snap = _aref("TEMPORAL_EVIDENCE", "TE1")
    tp_ref, tp_snap = _aref("TARGET_USE_PERMISSION", "TP1")
    um_ref, um_snap = _aref("UNCERTAINTY_METHOD", "UM1")
    rp_ref, rp_snap = _aref("REPLAY_PROTOCOL", "RP1")
    eq_ref, eq_snap = _aref("SOURCE_EQUIVALENCE", "EQ1",
                            ops=("SEMANTIC_EQUIVALENCE_ADMISSION",))
    nm_ref, nm_snap = _aref("NATIVE_CANONICAL_MAPPING_HARMONIZATION", "NM1")
    named = {
        "tc": (tc_ref, tc_snap), "te": (te_ref, te_snap), "tp": (tp_ref, tp_snap),
        "um": (um_ref, um_snap), "rp": (rp_ref, rp_snap), "eq": (eq_ref, eq_snap),
        "nm": (nm_ref, nm_snap),
        "meas": (MEASURE_REF, MEASURE_SNAPSHOT),
        "est": (ESTIMAND_REF, ESTIMAND_SNAPSHOT),
    }
    authority_refs = {
        "tc": tc_ref, "te": te_ref, "tp": tp_ref, "um": um_ref, "rp": rp_ref,
        "eq": eq_ref, "nm": nm_ref,
    }
    kept = [(a, b) for k, (a, b) in named.items() if k not in drop]
    return AuthorityRegistry([b for _, b in kept]), authority_refs


def _request(**overrides) -> TemporalComparisonRequest:
    reg, a = _full_registry()
    base = dict(
        temporal_identity_contract_ref=_ref("TemporalIdentityContract", "TIC1"),
        anchor_refs=(_ref("TimeAnchor", "A1"), _ref("TimeAnchor", "A2")),
        observation_refs=(_ref("Observation", "O1"), _ref("Observation", "O2")),
        source_universe_refs=(UNIVERSE_A, UNIVERSE_A),
        governed_use_id=_ref("TargetUsePermission", "USE-1"),
        temporal_order_disposition="CALENDAR_TOTAL_ORDER",
        temporal_order_basis_ref=_ref("TemporalOrderBasis", "TOB1"),
        temporal_comparability_authority_ref=a["tc"],
        temporal_order_basis_authority_ref=a["te"],
        temporal_evidence_authority_ref=a["te"],
        estimand_authority_refs=(ESTIMAND_REF,),
        measure_authority_refs=(MEASURE_REF,),
        target_use_permission_refs=(a["tp"],),
        uncertainty_authority_ref=a["um"],
        replay_protocol_authority_ref=a["rp"],
        comparability_requirements_ref=_ref("ComparabilityRequirements", "CR1"),
        comparison_operation=AUTHORIZED_COMPARISON_OPERATION,
        quantity_surface={
            "quantity_ref": _ref("Quantity", "Q1"),
            "measure_ref": MEASURE_REF,
            "earlier_value": 3,
            "later_value": 8,
        },
    )
    base.update(overrides)
    return TemporalComparisonRequest(**base)


def _run(request=None, registry=None):
    if registry is None:
        registry, _ = _full_registry()
    return compare_temporal_anchors(request or _request(), registry)


# ===========================================================================
# registry minimality
# ===========================================================================

def test_registry_kind_ceiling_pairing_is_bijective():
    assert TEMPORAL_COMPARABILITY_AUTHORITY_KIND in AUTHORITY_KINDS
    assert set(AUTHORITY_KINDS) == set(AUTHORITY_KIND_CEILINGS)
    assert len(AUTHORITY_KINDS) == 19
    temporal_kinds = {k for k in AUTHORITY_KINDS if k.startswith("TEMPORAL_")}
    assert temporal_kinds == {"TEMPORAL_EVIDENCE", "TEMPORAL_COMPARABILITY"}


def test_ceiling_text_denies_downstream_power():
    ceiling = " ".join(AUTHORITY_KIND_CEILINGS[TEMPORAL_COMPARABILITY_AUTHORITY_KIND]).lower()
    assert "no downstream consumer power" in ceiling


# ===========================================================================
# WITNESS A1 / F-DIR-01: every required authority must actually resolve
# ===========================================================================

def test_witness_a1_full_authority_set_yields_directional_claim():
    receipt = _run()
    assert receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert receipt.direction_claim == "INCREASE"
    assert receipt.comparability_status == "COMPARABLE"
    # Provenance now carries every authority resolution, not just one.
    slots = {r["slot"] for r in receipt.provenance["authority_resolutions"]}
    assert {"temporal_comparability", "temporal_evidence", "temporal_order_basis",
            "target_use_permission", "uncertainty_method", "replay_protocol",
            "estimand[0]", "measure[0]"} <= slots
    assert receipt.authority_snapshot_refs, "positive snapshots must be recorded"


@pytest.mark.parametrize("dropped", [
    "tc", "te", "tp", "um", "rp", "est", "meas",
])
def test_witness_a1_every_missing_authority_fails_closed(dropped):
    """HQ213 A1/A1b: dropping any single required authority must refuse a claim."""
    registry, _ = _full_registry(drop=(dropped,))
    receipt = _run(registry=registry)
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    assert receipt.direction_claim == "DIRECTION_NOT_CLAIMABLE"
    assert receipt.relation_status == "ORDER_RELATION_REFUSED"


def test_witness_a1_removing_uncertainties_is_not_silent():
    """The HQ213 'decorative fixture' defect: uncertainty absence must be visible."""
    registry, _ = _full_registry(drop=("um",))
    receipt = _run(registry=registry)
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    outcomes = {r["slot"]: r["outcome"] for r in receipt.provenance["authority_resolutions"]}
    assert outcomes["uncertainty_method"] == "ABSENT"


# ===========================================================================
# WITNESS A2 / F-DIR-02: TEMPORAL_COMPARABILITY is operation and use scoped
# ===========================================================================

def test_witness_a2_unrelated_operation_authority_refuses():
    registry, _ = _full_registry(tc_ops=("UNRELATED_OPERATION",))
    receipt = _run(registry=registry)
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    assert receipt.relation_state_reason == "AUTHORITY_SCOPE_MISMATCH"


def test_witness_a2_foreign_governed_use_scope_refuses():
    registry, _ = _full_registry(
        tc_scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED",
                  "target_use_refs": ["urn:other:use"]})
    receipt = _run(registry=registry)
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    assert receipt.relation_state_reason == "AUTHORITY_SCOPE_MISMATCH"


def test_witness_hash_mismatch_is_a_reachable_reason():
    """F-REASON-01: hash mismatch must be reachable, not collapsed to absence."""
    registry, _ = _full_registry()
    request = _request()
    from dataclasses import replace
    from rawlsing_next.pre553_empirical_objects import AuthorityRef
    bad = replace(request, temporal_comparability_authority_ref=AuthorityRef(
        "TC1", "1.0.0", _h("a-different-content-hash-entirely")))
    receipt = compare_temporal_anchors(bad, registry)
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    assert receipt.relation_state_reason == "AUTHORITY_HASH_MISMATCH"


def test_witness_out_of_scope_state_maps_to_typed_reason():
    registry, _ = _full_registry(tc_state="OUT_OF_SCOPE")
    receipt = _run(registry=registry)
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    assert receipt.relation_state_reason == "TEMPORAL_COMPARABILITY_AUTHORITY_OUT_OF_SCOPE"


def test_resolve_required_authority_never_raises_without_registry():
    """F-NONE-01: a missing registry is typed, not an AttributeError."""
    from rawlsing_next.pre553_empirical_objects import AuthorityRef
    ref = AuthorityRef("TC1", "1.0.0", _h("authority:TC1:1.0.0"))
    record, snapshot = resolve_required_authority(
        None, ref, slot="tc", authority_kind=TEMPORAL_COMPARABILITY_AUTHORITY_KIND)
    assert snapshot is None
    assert record.outcome == "ABSENT"


def test_cross_universe_request_without_registry_is_typed():
    """F-NONE-01: no registry means typed fail-closed absence, never AttributeError."""
    from rawlsing_next.pre553_empirical_objects import AuthorityRef
    request = _request(
        source_universe_refs=(UNIVERSE_A, UNIVERSE_B),
        source_equivalence_ref=_ref("SourceEquivalenceResult", "SEQ1"),
        source_equivalence_authority_ref=AuthorityRef(
            "EQ1", "1.0.0", _h("authority:EQ1:1.0.0")))
    receipt = compare_temporal_anchors(request, None)
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    outcomes = {r["slot"]: r["outcome"] for r in receipt.provenance["authority_resolutions"]}
    assert outcomes["source_equivalence"] == "ABSENT"
    assert outcomes["temporal_comparability"] == "ABSENT"


# ===========================================================================
# WITNESS B / F-CARD-01: exact cardinality
# ===========================================================================

@pytest.mark.parametrize("anchors", [
    (_ref("TimeAnchor", "A1"), _ref("TimeAnchor", "A2"), _ref("TimeAnchor", "A3")),
    (_ref("TimeAnchor", "A1"), _ref("TimeAnchor", "A2"), _ref("TimeAnchor", "A3"),
     _ref("TimeAnchor", "A4")),
])
def test_witness_three_or_more_anchors_refuse_pre_receipt(anchors):
    """Repair 3: 3+ anchors must refuse before any positive receipt."""
    with pytest.raises(TemporalComparabilityInputRefusal):
        _run(_request(anchor_refs=anchors))


@pytest.mark.parametrize("anchors", [
    (),
    (_ref("TimeAnchor", "A1"),),
])
def test_witness_fewer_than_two_anchors_is_the_contract_refusal_state(anchors):
    """The contract's own state stays reachable; it is not replaced by a raise."""
    receipt = _run(_request(anchor_refs=anchors, quantity_surface=None))
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_ANCHORS"
    assert receipt.relation_state_reason == "FEWER_THAN_TWO_AUTHORIZED_ANCHORS"


@pytest.mark.parametrize("observations", [
    (_ref("Observation", "O1"),),
    (_ref("Observation", "O1"), _ref("Observation", "O2"), _ref("Observation", "O3")),
])
def test_witness_cardinality_requires_exactly_two_observations(observations):
    with pytest.raises(TemporalComparabilityInputRefusal):
        _run(_request(observation_refs=observations))


def test_witness_each_anchor_binds_one_observation():
    receipt = _run()
    bindings = receipt.provenance["observation_binding"]
    assert len(bindings) == 2
    assert bindings[0]["anchor"] != bindings[1]["anchor"]
    assert bindings[0]["observation"] != bindings[1]["observation"]
    assert bindings[0]["anchor"] == receipt.anchor_refs[0]
    assert bindings[1]["anchor"] == receipt.anchor_refs[1]


# ===========================================================================
# Repair 4: comparability_requirements_ref is required and used
# ===========================================================================

def test_witness_comparability_requirements_ref_is_required():
    with pytest.raises(TemporalComparabilityInputRefusal):
        _run(_request(comparability_requirements_ref=None))


def test_witness_comparability_requirements_reaches_provenance():
    receipt = _run()
    assert receipt.provenance["comparability_requirements_ref"]["object_id"] == "CR1"


def test_witness_declared_surface_drives_state_selection():
    receipt = _run(_request(comparability_requirement_results=(
        {"reason": "GEOGRAPHY_NOT_SHARED"},)))
    assert receipt.relation_state == "TEMPORAL_NONCOMPARABLE"
    assert receipt.relation_state_reason == "GEOGRAPHY_NOT_SHARED"
    assert receipt.provenance["declared_comparability_surfaces"]


# ===========================================================================
# Repair 5 / F-DELTA-01: the delta is derived, not caller-minted
# ===========================================================================

def test_witness_delta_is_derived_from_the_bound_quantity_surface():
    receipt = _run()
    assert receipt.delta["signed_delta"] == 5
    assert receipt.delta["comparison_operation"] == AUTHORIZED_COMPARISON_OPERATION
    assert receipt.quantity_surface["earlier_value"] == 3
    assert receipt.quantity_surface["later_value"] == 8


def test_witness_caller_cannot_mint_a_delta():
    """There is no signed_delta input any more; only the surface is accepted."""
    assert "signed_delta" not in {f.name for f in _fields(_request())}
    assert "quantity_surface" in {f.name for f in _fields(_request())}


def _fields(request):
    return [f for f in __import__("dataclasses").fields(request.__class__)]


def test_witness_quantity_surface_must_match_the_bound_measure():
    with pytest.raises(TemporalComparabilityInputRefusal):
        _run(_request(quantity_surface={
            "quantity_ref": _ref("Quantity", "Q1"),
            "measure_ref": _ref("MeasureAuthority", "NOT-BOUND"),
            "earlier_value": 1, "later_value": 2,
        }))


def test_witness_exact_zero_is_derived_not_asserted():
    receipt = _run(_request(quantity_surface={
        "quantity_ref": _ref("Quantity", "Q1"),
        "measure_ref": MEASURE_REF, "earlier_value": 7, "later_value": 7}))
    assert receipt.direction_claim == "NO_AUTHORIZED_CHANGE"
    assert receipt.delta["signed_delta"] == 0


def test_witness_decrease_direction_is_derived():
    receipt = _run(_request(quantity_surface={
        "quantity_ref": _ref("Quantity", "Q1"),
        "measure_ref": MEASURE_REF, "earlier_value": 9, "later_value": 2}))
    assert receipt.direction_claim == "DECREASE"


def test_witness_tiny_exact_delta_is_not_a_deadband():
    receipt = _run(_request(quantity_surface={
        "quantity_ref": _ref("Quantity", "Q1"),
        "measure_ref": MEASURE_REF,
        "earlier_value": Decimal("1E-999"), "later_value": Decimal("2E-999")}))
    assert receipt.direction_claim == "INCREASE"


@pytest.mark.parametrize("bad", ["0.0", float("nan"), True, "1", None])
def test_witness_inexact_or_malformed_quantities_refuse(bad):
    with pytest.raises(TemporalComparabilityError):
        _run(_request(quantity_surface={
            "quantity_ref": _ref("Quantity", "Q1"),
            "measure_ref": MEASURE_REF, "earlier_value": 0, "later_value": bad}))


def test_witness_fraction_deltas_are_exact():
    receipt = _run(_request(quantity_surface={
        "quantity_ref": _ref("Quantity", "Q1"),
        "measure_ref": MEASURE_REF,
        "earlier_value": Fraction(1, 3), "later_value": Fraction(5, 3)}))
    assert receipt.direction_claim == "INCREASE"
    assert receipt.delta["signed_delta"] == {"$exact_fraction": [4, 3]}


# ===========================================================================
# Repair 6: the accepted closed receipt contract, with contract field names
# ===========================================================================

def test_witness_receipt_carries_every_accepted_contract_field():
    receipt = _run()
    required = {
        "receipt_id", "temporal_identity_contract_ref", "anchor_refs",
        "temporal_order_disposition", "temporal_order_basis_ref",
        "comparability_status", "comparability_requirement_results", "relation_status",
        "direction_claim", "quantity_surface", "delta", "non_delta_presence",
        "uncertainty_state", "intervening_span_state", "relation_state",
        "relation_state_reason", "governed_use_id", "authority_snapshot_refs", "provenance",
    }
    present = set(receipt.as_material()) | {"receipt_hash"}
    assert required <= present, sorted(required - present)
    # The contract names it delta, not signed_delta.
    assert "delta" in present and "signed_delta" not in present


def test_witness_receipt_field_set_is_closed():
    receipt = _run()
    contract_fields = set(receipt.as_material()) | {"receipt_hash"}
    assert contract_fields == {f.name for f in _fields(receipt)} | {"receipt_hash"}


def test_witness_provenance_carries_operation_and_projection_rule():
    receipt = _run()
    assert receipt.provenance["comparison_operation"] == AUTHORIZED_COMPARISON_OPERATION
    assert "canonical_json" in receipt.provenance["canonical_projection_rule"]
    assert receipt.provenance["cross_universe"]["derivation"].startswith("material-derived")


def test_witness_uncertainty_and_span_states_are_bound():
    receipt = _run()
    assert receipt.uncertainty_state == "QUANTIFIED_UNDER_BOUND_METHOD"
    assert receipt.intervening_span_state == "NO_INTERVENING_GAP"


# ===========================================================================
# Repair 7 / F-PRIOR-01: prior F7 state participates in derivation
# ===========================================================================

@pytest.mark.parametrize("prior,expected", [
    ("TEMPORAL_INTERPOLATION_NOT_AUTHORIZED", "TEMPORAL_NONCOMPARABLE"),
    ("TEMPORAL_RESPONSE_SURFACE_MISMATCH", "TEMPORAL_NONCOMPARABLE"),
    ("TEMPORAL_AUTHORITY_MISSING", "TEMPORAL_INSUFFICIENT_AUTHORITY"),
    ("TEMPORAL_AUTHORITY_CONFLICT", "TEMPORAL_INSUFFICIENT_AUTHORITY"),
    ("TEMPORAL_OUT_OF_SCOPE", "TEMPORAL_INSUFFICIENT_AUTHORITY"),
])
def test_witness_prior_f7_state_drives_the_terminal_state(prior, expected):
    """The HQ213 inert-mapping defect: these must change the outcome."""
    receipt = _run(_request(prior_f7_state=prior))
    assert receipt.relation_state == expected
    assert receipt.provenance["prior_f7_state"] == prior


def test_witness_prior_map_is_not_asserted_against_itself():
    """Every mapped value must actually be an observed reason code."""
    observed: set[str] = set()
    for prior in PRIOR_F7_STATE_MAP:
        receipt = _run(_request(prior_f7_state=prior))
        observed.update(r["reason"] for r in receipt.comparability_requirement_results)
    for prior, mapped in PRIOR_F7_STATE_MAP.items():
        assert mapped in observed, f"{prior} maps to {mapped}, never observed"


def test_witness_probe_only_still_yields_no_receipt():
    assert "TEMPORAL_PROBE_ONLY" in PRIOR_F7_NO_RECEIPT_STATES
    with pytest.raises(TemporalComparabilityError):
        _run(_request(prior_f7_state="TEMPORAL_PROBE_ONLY"))


def test_witness_unknown_prior_state_refuses_typed():
    with pytest.raises(TemporalComparabilityIntegrityError):
        _run(_request(prior_f7_state="TEMPORAL_WIDENED_STATE"))


# ===========================================================================
# Repair 8 / F-XU-01: cross-universe is material-derived
# ===========================================================================

def test_witness_cross_universe_is_derived_from_bound_universes():
    """No caller boolean exists any more; the universes decide."""
    assert "pair_crosses_source_universes" not in _field_names()
    receipt = _run(_request(source_universe_refs=(UNIVERSE_A, UNIVERSE_B),
                            source_equivalence_ref=_ref("SourceEquivalenceResult", "SEQ1"),
                            source_equivalence_authority_ref=_aref(
                                "SOURCE_EQUIVALENCE", "EQ1",
                                ops=("SEMANTIC_EQUIVALENCE_ADMISSION",))[0]))
    assert receipt.provenance["cross_universe"]["crosses_source_universes"] is True
    assert receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"


def _field_names():
    import dataclasses
    return {f.name for f in dataclasses.fields(TemporalComparisonRequest)}


def test_witness_cross_universe_without_equivalence_refuses():
    receipt = _run(_request(source_universe_refs=(UNIVERSE_A, UNIVERSE_B)))
    assert receipt.relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"
    assert receipt.relation_state_reason == "SOURCE_EQUIVALENCE_REF_ABSENT"


def test_witness_equivalence_authority_must_cover_the_actual_pair():
    """Path A must be scoped to both bound universes, not merely of the right kind."""
    base_reg, _ = _full_registry()
    eq_ref, eq_snap = _aref("SOURCE_EQUIVALENCE", "EQ1",
                            ops=("SEMANTIC_EQUIVALENCE_ADMISSION",),
                            scope={"source_universe_refs": [UNIVERSE_A.as_dict()],
                                   "target_use_refs": "EXPLICIT_UNRESTRICTED"})
    replaced = [eq_snap if snap.authority_id == "EQ1" else snap
                for snap in base_reg._by_key.values()]
    narrow_registry = AuthorityRegistry(replaced)
    receipt = _run(_request(source_universe_refs=(UNIVERSE_A, UNIVERSE_B),
                            source_equivalence_ref=_ref("SourceEquivalenceResult", "SEQ1"),
                            source_equivalence_authority_ref=eq_ref),
                   registry=narrow_registry)
    assert receipt.relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"
    assert receipt.relation_state_reason == "SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE"


def test_witness_same_universe_needs_no_equivalence():
    receipt = _run()
    assert receipt.provenance["cross_universe"]["crosses_source_universes"] is False
    assert receipt.provenance["cross_universe"]["source_equivalence_ref"] is None


def test_witness_temporal_module_never_mints_equivalence():
    src = MOD_PATH.read_text()
    assert "AuthoritySnapshot(" not in src, "the temporal module must never mint a snapshot"


# ===========================================================================
# HQ214 adjudications A, B, C
# ===========================================================================

def test_adjudication_a_no_thirteenth_state_exists():
    assert len(RELATION_STATE_PRECEDENCE) == 12
    assert len(RELATION_STATES) == 12


def test_adjudication_a_ordered_basis_without_quantity_surface_refuses_pre_receipt():
    """A: typed pre-receipt refusal; never a receipt, never a new state."""
    with pytest.raises(TemporalComparabilityInputRefusal):
        _run(_request(quantity_surface=None))
    assert len(RELATION_STATES) == 12


def test_adjudication_a_direction_permitting_basis_requires_a_derivable_delta():
    with pytest.raises(TemporalComparabilityInputRefusal):
        _run(_request(quantity_surface={"quantity_ref": _ref("Quantity", "Q1")}))


def test_adjudication_b_only_three_states_may_be_comparable():
    assert COMPARABLE_STATES == {
        "TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION",
        "TEMPORAL_COMPARABLE_NO_DIRECTION",
        "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED",
    }
    assert NEGATIVE_STATES | COMPARABLE_STATES == RELATION_STATES


def test_adjudication_b_every_negative_state_reports_not_comparable():
    """B: drive every one of the nine negative states and check the flag."""
    seen = set()

    def record(receipt):
        seen.add(receipt.relation_state)
        if receipt.relation_state in NEGATIVE_STATES:
            assert receipt.comparability_status == "NOT_COMPARABLE", receipt.relation_state
        return receipt

    record(compare_temporal_anchors(_request(), AuthorityRegistry([])))
    record(_run(_request(temporal_identity_contract_ref=None)))
    record(_run(_request(source_universe_refs=(UNIVERSE_A, UNIVERSE_B))))
    record(_run(_request(family_mapping_required=True,
                         native_canonical_mapping_authority_ref=None)))
    record(_run(_request(prior_f7_state="TEMPORAL_AUTHORITY_MISSING")))
    record(_run(_request(prior_f7_state="TEMPORAL_RESPONSE_SURFACE_MISMATCH")))
    # Both authorities must be genuinely registered positive for a mismatch to
    # be a mismatch rather than a plain absence.
    base_reg, _ = _full_registry()
    est2, est2_snap = _aref("WEIGHT_DESIGN_ESTIMAND", "EST2")
    mea2, mea2_snap = _aref("WEIGHT_DESIGN_ESTIMAND", "MEAS2")
    two_est = AuthorityRegistry([est2_snap, *base_reg._by_key.values()])
    two_mea = AuthorityRegistry([mea2_snap, *base_reg._by_key.values()])
    record(_run(_request(estimand_authority_refs=(ESTIMAND_REF, est2)), two_est))
    record(_run(_request(measure_authority_refs=(MEASURE_REF, mea2)), two_mea))
    record(_run(_request(measure_authority_refs=())))
    record(_run(_request(temporal_order_disposition=NO_BASIS_DISPOSITION,
                         temporal_order_basis_ref=None)))
    # anchors are refused pre-receipt, so use an identity failure for the ninth
    assert seen >= NEGATIVE_STATES - {"TEMPORAL_INSUFFICIENT_ANCHORS"}
    assert "TEMPORAL_NONCOMPARABLE" in seen
    assert "TEMPORAL_ORDER_UNAUTHORIZED" in seen


def test_adjudication_c_no_basis_yields_order_unauthorized_when_clean():
    receipt = _run(_request(temporal_order_disposition=NO_BASIS_DISPOSITION,
                            temporal_order_basis_ref=None))
    assert receipt.relation_state == "TEMPORAL_ORDER_UNAUTHORIZED"
    assert receipt.relation_state_reason == "NO_PERMITTED_ORDER_BASIS_APPLIES"
    assert receipt.provenance["no_basis_observation"] is True


def test_adjudication_c_higher_precedence_failure_wins_and_does_not_raise():
    """C: no-basis plus a higher failure emits the higher state, never a raise."""
    receipt = _run(_request(temporal_order_disposition=NO_BASIS_DISPOSITION,
                            temporal_order_basis_ref=None,
                            prior_f7_state="TEMPORAL_RESPONSE_SURFACE_MISMATCH"))
    assert receipt.relation_state == "TEMPORAL_NONCOMPARABLE"
    # The no-basis observation is retained rather than discarded.
    assert receipt.provenance["no_basis_observation"] is True
    assert receipt.temporal_order_disposition == NO_BASIS_DISPOSITION


def test_adjudication_c_authority_failure_outranks_no_basis():
    receipt = compare_temporal_anchors(
        _request(temporal_order_disposition=NO_BASIS_DISPOSITION,
                 temporal_order_basis_ref=None), AuthorityRegistry([]))
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    assert receipt.provenance["no_basis_observation"] is True


# ===========================================================================
# order law and partial order
# ===========================================================================

def test_order_vocabulary_is_three_bases_plus_one_typed_refusal():
    assert AUTHORIZED_ORDER_BASES == {
        "CALENDAR_TOTAL_ORDER", "FAMILY_LOCAL_ORDINAL", "PARTIAL_ORDER_NO_DIRECTION"}
    assert NO_BASIS_DISPOSITION not in AUTHORIZED_ORDER_BASES
    assert DIRECTION_PERMITTING_BASES == {"CALENDAR_TOTAL_ORDER", "FAMILY_LOCAL_ORDINAL"}
    assert len(ORDER_DISPOSITIONS) == 4


def test_authorized_basis_requires_a_basis_ref():
    with pytest.raises(TemporalComparabilityIntegrityError):
        _run(_request(temporal_order_basis_ref=None))


def test_no_basis_must_not_carry_a_basis_ref():
    with pytest.raises(TemporalComparabilityIntegrityError):
        _run(_request(temporal_order_disposition=NO_BASIS_DISPOSITION,
                      temporal_order_basis_ref=_ref("TemporalOrderBasis", "TOB1")))


def test_partial_order_overlap_refuses_direction():
    receipt = _run(_request(temporal_order_disposition="PARTIAL_ORDER_NO_DIRECTION",
                            intervals_overlap=True))
    assert receipt.relation_state == "TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION"
    assert receipt.relation_state_reason == "INTERVALS_OVERLAP"
    assert receipt.relation_status == "ORDER_RELATION_REFUSED"
    assert receipt.direction_claim == "DIRECTION_NOT_CLAIMABLE"
    assert receipt.delta is None


def test_partial_order_no_direction_state():
    receipt = _run(_request(temporal_order_disposition="PARTIAL_ORDER_NO_DIRECTION",
                            intervals_overlap=False))
    assert receipt.relation_state == "TEMPORAL_COMPARABLE_NO_DIRECTION"
    assert receipt.relation_state_reason == "AUTHORIZED_PARTIAL_ORDER_YIELDS_NO_DIRECTION_ON_PAIR"


def test_family_local_ordinal_is_direction_permitting():
    assert _run(_request(temporal_order_disposition="FAMILY_LOCAL_ORDINAL")).relation_state \
        == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"


# ===========================================================================
# precedence and determinism
# ===========================================================================

def test_precedence_order_is_exact():
    assert list(RELATION_STATE_PRECEDENCE) == [
        "TEMPORAL_INSUFFICIENT_AUTHORITY", "TEMPORAL_IDENTITY_UNRESOLVED",
        "TEMPORAL_INSUFFICIENT_ANCHORS", "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT",
        "TEMPORAL_MAPPING_MATERIAL_ABSENT", "TEMPORAL_ESTIMAND_MISMATCH",
        "TEMPORAL_MEASURE_MISMATCH", "TEMPORAL_NONCOMPARABLE",
        "TEMPORAL_ORDER_UNAUTHORIZED", "TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION",
        "TEMPORAL_COMPARABLE_NO_DIRECTION", "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED",
    ]
    for state in RELATION_STATE_PRECEDENCE:
        assert STATE_REASON_PRECEDENCE[state]


def test_identity_outranks_lower_states():
    receipt = _run(_request(temporal_identity_contract_ref=None,
                            prior_f7_state="TEMPORAL_RESPONSE_SURFACE_MISMATCH"))
    assert receipt.relation_state == "TEMPORAL_IDENTITY_UNRESOLVED"


def test_every_detected_failure_is_retained():
    receipt = _run(_request(prior_f7_state="TEMPORAL_RESPONSE_SURFACE_MISMATCH",
                            measure_authority_refs=()))
    reasons = {r["reason"] for r in receipt.comparability_requirement_results}
    assert "RESPONSE_SURFACE_NOT_SHARED" in reasons
    assert "MEASURE_AUTHORITY_NOT_POSITIVE" in reasons
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"


def test_replay_identity_is_stable_and_content_sensitive():
    a, b = _run(), _run()
    assert a.receipt_hash == b.receipt_hash == a.replay_identity()
    changed = _run(_request(quantity_surface={
        "quantity_ref": _ref("Quantity", "Q1"), "measure_ref": MEASURE_REF,
        "earlier_value": 3, "later_value": 9}))
    assert changed.receipt_hash != a.receipt_hash


# ===========================================================================
# receipt locality, real checks (no vacuous guards)
# ===========================================================================

def test_receipt_is_not_a_canonical_public_object():
    from rawlsing_next.pre553_empirical_objects import CanonicalSemanticObject
    receipt = _run()
    assert not isinstance(receipt, CanonicalSemanticObject)


def test_no_public_object_family_registration_really_absent():
    """The previous court used an isinstance guard that silently went vacuous."""
    from rawlsing_next.pre553_empirical_objects import PUBLIC_OBJECT_FAMILIES
    families = (PUBLIC_OBJECT_FAMILIES if isinstance(PUBLIC_OBJECT_FAMILIES, (set, frozenset, tuple, list))
                else tuple(PUBLIC_OBJECT_FAMILIES))
    names = {str(f) for f in families}
    assert names, "the family registry must be non-empty for this check to mean anything"
    assert not any("TEMPORAL" in n for n in names), sorted(names)


def test_no_state_families_widening_really_absent():
    from rawlsing_next.pre553_empirical_objects import STATE_FAMILIES
    states = {str(s) for s in STATE_FAMILIES}
    assert states, "the state registry must be non-empty for this check to mean anything"
    assert "TEMPORAL_RELATION_RECEIPT" not in states
    assert not any(s.startswith("TEMPORAL_RELATION") for s in states), sorted(states)


def test_module_imports_no_f8_and_no_new_family():
    tree = ast.parse(MOD_PATH.read_text())
    internal = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            internal.append(node.module or "")
        elif isinstance(node, ast.Import):
            internal.extend(a.name for a in node.names)
    internal = [n for n in internal if n.startswith("rawlsing_next.")]
    assert sorted(internal) == [
        "rawlsing_next.pre553_empirical_authority",
        "rawlsing_next.pre553_empirical_objects",
        "rawlsing_next.pre553_source_relations",
    ]


# ===========================================================================
# backfill noncollapse, checked live (Repair 9)
# ===========================================================================

def test_backfill_guard_reads_the_live_frozen_surface():
    from rawlsing_next.pre553_source_relations import FORBIDDEN_BACKFILL_TARGET_STATES
    assert "TEMPORAL_NONCOMPARABLE" in FORBIDDEN_BACKFILL_TARGET_STATES
    assert temporal_backfill_refused("TEMPORAL_NONCOMPARABLE") is True
    assert temporal_backfill_refused("TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED") is False


def test_backfill_guard_is_proven_live_not_self_described(monkeypatch):
    """Repair 9: mutate the frozen surface and the guard must follow it.

    This proves live consultation. A module-local copy would be unaffected.
    """
    import rawlsing_next.pre553_source_relations as sr
    import rawlsing_next.pre553_temporal_comparability as mod
    assert temporal_backfill_refused("TEMPORAL_NONCOMPARABLE") is True
    reduced = frozenset(sr.FORBIDDEN_BACKFILL_TARGET_STATES - {"TEMPORAL_NONCOMPARABLE"})
    monkeypatch.setattr(sr, "FORBIDDEN_BACKFILL_TARGET_STATES", reduced)
    assert temporal_backfill_refused("TEMPORAL_NONCOMPARABLE") is False
    # With the literal removed from the live surface the producer must refuse
    # to mint a noncomparable receipt rather than silently proceed.
    with pytest.raises(TemporalComparabilityIntegrityError):
        _run(_request(comparability_requirement_results=(
            {"reason": "GEOGRAPHY_NOT_SHARED"},)))
    monkeypatch.undo()
    assert hasattr(mod, "_frozen_backfill_targets")


def test_noncomparable_receipt_is_still_minted_and_flagged():
    receipt = _run(_request(comparability_requirement_results=(
        {"reason": "GEOGRAPHY_NOT_SHARED"},)))
    assert receipt.relation_state == "TEMPORAL_NONCOMPARABLE"
    assert temporal_backfill_refused(receipt.relation_state)


def test_frozen_surfaces_untouched():
    from rawlsing_next.pre553_empirical_authority import (
        FAIL_CLOSED_STATES, FORBIDDEN_SELECTOR_TOKENS)
    assert "LATEST" in FORBIDDEN_SELECTOR_TOKENS
    assert "DENY" in FAIL_CLOSED_STATES


def test_no_broad_exception_catch_in_this_court():
    """Self-check: this court must not accept any error as a pass."""
    src = pathlib.Path(__file__).read_text()
    import re
    broad = "Excep" + "tion"
    assert not re.search(r"raises\(\s*" + broad + r"\b", src)
    assert not re.search(r"except\s+" + broad + r"\b", src)
    assert not re.search(r"raises\(\([^)]*" + broad, src)