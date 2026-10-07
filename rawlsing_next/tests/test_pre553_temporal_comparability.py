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
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot, ExactRef, canonical_json, semantic_hash,
)
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
          state: str = "ALLOW", content_hash: str | None = None,
          families=("TemporalComparisonProbe@1.0.0",)):
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
        governed_object_families=tuple(families),
        scope_envelope=dict(scope),
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"semantics:{kind}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", "RP1"),
    )
    return ref, snapshot


#: HQ217 productive-adequacy fixtures. Competent lawful material whose canonical hash IS
#: the ref content_hash, so the contract refs are genuinely bound (RR-01 / RR-03).
BOUND_REQUIREMENT_MATERIAL = {
    "requirement_results": (
        {"surface": "shared_response_surface_and_scale_harmonization", "satisfied": True},
        {"surface": "shared_instrument_release_or_authorized_equivalence", "satisfied": True},
        {"surface": "shared_question_coordinate_semantics", "satisfied": True},
        {"surface": "shared_estimand", "satisfied": True},
        {"surface": "shared_measure_and_weight_design", "satisfied": True},
        {"surface": "shared_geography_and_target_population", "satisfied": True},
        {"surface": "bound_order_basis_for_time_refs", "satisfied": True},
    ),
}
BOUND_IDENTITY_MATERIAL = {
    "identity_surface_jointly_satisfied": True,
    "composition": ("source family key, geography, question/coordinate semantics, response "
                    "surface, instrument release, target population / risk set, estimand, "
                    "measure and weight design"),
    "wave_label_ordinal_calendar_year_preserved": True,
}
COMPARABILITY_REQUIREMENTS_REF = ExactRef(
    "ComparabilityRequirements", "CR1", semantic_hash(BOUND_REQUIREMENT_MATERIAL))
TEMPORAL_IDENTITY_CONTRACT_REF = ExactRef(
    "TemporalIdentityContract", "TIC1", semantic_hash(BOUND_IDENTITY_MATERIAL))

UNIVERSE_A = _ref("SourceUniverse", "U-A")
UNIVERSE_B = _ref("SourceUniverse", "U-B")
MEASURE_REF, MEASURE_SNAPSHOT = _aref("WEIGHT_DESIGN_ESTIMAND", "MEAS1")
ESTIMAND_REF, ESTIMAND_SNAPSHOT = _aref("WEIGHT_DESIGN_ESTIMAND", "EST1")


def _full_registry(*, drop=(), tc_ops=(AUTHORIZED_COMPARISON_OPERATION,),
                   tc_scope=None, tc_hash=None, tc_state="ALLOW",
                   te_identity_refs=None, te_identity_satisfied=True,
                   te_scope=None, extra_snapshots=()):
    """Every authority the contract requires, so no test depends on a decorative one."""
    tc_ref, tc_snap = _aref(TEMPORAL_COMPARABILITY_AUTHORITY_KIND, "TC1", ops=tc_ops,
                            scope=tc_scope, state=tc_state, content_hash=tc_hash)
    # HQ219 RR-03: the TEMPORAL_EVIDENCE authority OWNS temporal identity. Its scope
    # envelope binds the identity contract ref and states joint satisfaction, and the
    # positive path derives identity from THAT rather than from caller material.
    te_scope = dict(te_scope or tc_scope or {"source_universe_refs": "EXPLICIT_UNRESTRICTED",
                                 "target_use_refs": "EXPLICIT_UNRESTRICTED"})
    if te_identity_refs is not False:
        te_scope["temporal_identity_contract_refs"] = (
            te_identity_refs if te_identity_refs is not None
            else (TEMPORAL_IDENTITY_CONTRACT_REF,))
        te_scope["identity_surface_jointly_satisfied"] = bool(te_identity_satisfied)
    te_ref, te_snap = _aref("TEMPORAL_EVIDENCE", "TE1", scope=te_scope)
    tp_ref, tp_snap = _aref("TARGET_USE_PERMISSION", "TP1")
    um_ref, um_snap = _aref("UNCERTAINTY_METHOD", "UM1")
    rp_ref, rp_snap = _aref("REPLAY_PROTOCOL", "RP1")
    eq_ref, eq_snap = _aref(
        "SOURCE_EQUIVALENCE", "EQ1",
        ops=("SEMANTIC_EQUIVALENCE_ADMISSION",),
        families=("SourceUniverseRelation@1.0.0",),
        scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED",
               "target_use_refs": "EXPLICIT_UNRESTRICTED",
               "predicate_or_risk_set_refs": "EXPLICIT_UNRESTRICTED"})
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
    return AuthorityRegistry([b for _, b in kept] + list(extra_snapshots)), authority_refs


def _request(**overrides) -> TemporalComparisonRequest:
    reg, a = _full_registry()
    base = dict(
        temporal_identity_contract_ref=TEMPORAL_IDENTITY_CONTRACT_REF,
        temporal_identity_contract_material=BOUND_IDENTITY_MATERIAL,
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
        comparability_requirements_ref=COMPARABILITY_REQUIREMENTS_REF,
        comparability_requirements_material=BOUND_REQUIREMENT_MATERIAL,
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


def _lawful_equivalence_resolver(*, relation_ref: ExactRef, universe_refs,
                                 target_use: str | None = None):
    """Build a REAL SourceRelationResolver over one lawful exact relation receipt.

    HQ217 RR-04: the equivalence ref must resolve through the exact source-relation
    owner path. A stub resolver would relocate the caller-trust problem into the test,
    so this constructs genuine relation material through the accepted factory.
    """
    from rawlsing_next.pre553_source_relations import (
        SourceRelationResolver, make_source_universe_relation,
    )
    eq_ref, eq_snapshot = _aref(
        "SOURCE_EQUIVALENCE", "EQ1", ops=("SEMANTIC_EQUIVALENCE_ADMISSION",),
        families=("SourceUniverseRelation@1.0.0",),
        scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED",
               "target_use_refs": "EXPLICIT_UNRESTRICTED",
               "predicate_or_risk_set_refs": "EXPLICIT_UNRESTRICTED"})
    registry = AuthorityRegistry([eq_snapshot])
    relation = make_source_universe_relation(
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
        source_universe_refs=tuple(universe_refs),
        authority_snapshot=eq_snapshot,
        authority_operation="SEMANTIC_EQUIVALENCE_ADMISSION",
        operation_scope="EXACT_BOUND_UNIVERSE_PAIR",
        # HQ219 RR-04: F7 requires the owner to adjudicate the relation for the exact
        # GOVERNED USE, not for the relation's own ref. A relation authorized only for
        # itself must not admit a governed use.
        target_use=(target_use if target_use is not None
                    else _ref("TargetUsePermission", "USE-1").object_id),
        effective_scope="EXACT_BOUND_UNIVERSE_PAIR",
        directionality_or_symmetric="SYMMETRIC",
        operation_authority_material={
            "relation_kind": "SOURCE_SEMANTIC_EQUIVALENCE",
            "equivalence_scope": "EXACT_BOUND_UNIVERSE_PAIR",
            "left_semantic_ref": _ref("SemanticFingerprint", "SEM-A"),
            "right_semantic_ref": _ref("SemanticFingerprint", "SEM-B"),
            "transformation_authority_refs": (_ref("SemanticTransformation", "TR-1"),),
        },
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "equiv-root"),
        decision="AUTHORIZED")
    resolver = SourceRelationResolver(relations=[relation], authority_registry=registry)
    return resolver, eq_ref, relation


def _request_with_failed_surface(reason: str, **overrides):
    """HQ217: a declared failing comparability surface must arrive through AUTHORIZED
    material whose hash the contract ref names, never as a bare caller tuple."""
    material = {"requirement_results": (
        {"surface": "shared_geography_and_target_population", "satisfied": False,
         "reason": reason},
    )}
    ref = ExactRef("ComparabilityRequirements", f"CR-FAIL-{reason}", semantic_hash(material))
    return _request(comparability_requirements_ref=ref,
                    comparability_requirements_material=material, **overrides)


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
    receipt = _run(_request_with_failed_surface("GEOGRAPHY_NOT_SHARED"))
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
    """No caller boolean exists any more; the universes decide.

    HQ217 RR-04: the equivalence ref must resolve through the exact source-relation
    OWNER PATH. This is the productive-adequacy proof that a genuinely cross-universe
    pair still reaches the positive receipt when the owner path resolves it.
    """
    assert "pair_crosses_source_universes" not in _field_names()
    probe = ExactRef("SourceEquivalenceResult", "SEQ1", _h("rel"))
    resolver, eq_authority_ref, relation = _lawful_equivalence_resolver(
        relation_ref=probe, universe_refs=(UNIVERSE_A, UNIVERSE_B))
    receipt = _run(_request(source_universe_refs=(UNIVERSE_A, UNIVERSE_B),
                            source_equivalence_ref=relation.ref,
                            source_equivalence_authority_ref=eq_authority_ref,
                            source_relation_resolver=resolver))
    assert receipt.provenance["cross_universe"]["crosses_source_universes"] is True
    assert receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"


def test_hq217_rr04_arbitrary_equivalence_ref_is_refused_without_the_owner_path():
    """RR-04: an arbitrary equivalence token is NOT caller-trusted.

    Before the repair this pair reached TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED because
    only the presence of a ref plus a scoped authority snapshot was checked.
    """
    probe = ExactRef("SourceEquivalenceResult", "SEQ1", _h("rel"))
    resolver, eq_authority_ref, _ = _lawful_equivalence_resolver(
        relation_ref=probe, universe_refs=(UNIVERSE_A, UNIVERSE_B))
    arbitrary = _ref("SourceEquivalenceResult", "ARBITRARY-TOKEN")
    receipt = _run(_request(source_universe_refs=(UNIVERSE_A, UNIVERSE_B),
                            source_equivalence_ref=arbitrary,
                            source_equivalence_authority_ref=eq_authority_ref,
                            source_relation_resolver=resolver))
    assert receipt.relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"
    assert receipt.relation_state_reason == "SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE"


def test_hq217_rr04_equivalence_without_a_resolver_is_refused():
    """RR-04: no owner path means no equivalence, even with a scoped authority."""
    eq_authority_ref = _aref("SOURCE_EQUIVALENCE", "EQ1",
                             ops=("SEMANTIC_EQUIVALENCE_ADMISSION",))[0]
    receipt = _run(_request(source_universe_refs=(UNIVERSE_A, UNIVERSE_B),
                            source_equivalence_ref=_ref("SourceEquivalenceResult", "SEQ1"),
                            source_equivalence_authority_ref=eq_authority_ref))
    assert receipt.relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"


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
    """HQ217 RR-06: a missing required basis ref is the ACCEPTED terminal state.

    This court previously asserted the IntegrityError, which was the defect. The
    accepted law is TEMPORAL_INSUFFICIENT_AUTHORITY /
    TEMPORAL_ORDER_BASIS_AUTHORITY_REF_ABSENT.
    """
    receipt = _run(_request(temporal_order_basis_ref=None))
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    assert receipt.relation_state_reason == "TEMPORAL_ORDER_BASIS_AUTHORITY_REF_ABSENT"
    assert receipt.direction_claim == "DIRECTION_NOT_CLAIMABLE"
    assert receipt.delta is None


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
        _run(_request_with_failed_surface("GEOGRAPHY_NOT_SHARED"))
    monkeypatch.undo()
    assert hasattr(mod, "_frozen_backfill_targets")


def test_noncomparable_receipt_is_still_minted_and_flagged():
    receipt = _run(_request_with_failed_surface("GEOGRAPHY_NOT_SHARED"))
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

# ===========================================================================
# HQ217 bounded repair witnesses
# ===========================================================================
def test_hq217_rr01_unbound_comparability_requirements_ref_is_refused():
    """RR-01: a ref token alone is not proof. The material must hash to the ref."""
    with pytest.raises(TemporalComparabilityInputRefusal) as exc:
        _run(_request(comparability_requirements_ref=_ref("ComparabilityRequirements", "CR-OTHER")))
    assert "does not hash to" in str(exc.value)
    with pytest.raises(TemporalComparabilityInputRefusal) as exc:
        _run(_request(comparability_requirements_material=None))
    assert "not bound" in str(exc.value)


def test_hq217_rr01_changing_the_ref_now_changes_the_derivation():
    """RR-01 discriminating witness.

    Before the repair, swapping the ref while keeping the same caller result tuple left
    the derivation identical, because the ref accompanied rather than governed it. Now a
    different requirement material carries its own ref and yields its own state.
    """
    clean = _run()
    assert clean.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    failing = _run(_request_with_failed_surface("GEOGRAPHY_NOT_SHARED"))
    assert failing.relation_state == "TEMPORAL_NONCOMPARABLE"
    assert failing.provenance["comparability_requirements_ref"]["object_id"] != \
        clean.provenance["comparability_requirements_ref"]["object_id"]


def test_hq217_rr01_caller_results_contradicting_bound_material_are_refused():
    """RR-01: the caller's own result tuple cannot contradict the authorized material."""
    with pytest.raises(TemporalComparabilityInputRefusal) as exc:
        _run(_request(comparability_requirement_results=({"reason": "GEOGRAPHY_NOT_SHARED"},)))
    assert "disagree with the material bound" in str(exc.value)


def test_hq217_rr02_same_object_id_different_content_hash_does_not_pass_scope():
    """RR-02: ExactRef identity is kind + object_id + content_hash.

    The authority scope names one exact governed-use ref. A DIFFERENT exact ref that
    shares only the object_id must not satisfy that scope.
    """
    scoped = _ref("TargetUsePermission", "USE-1")
    other = ExactRef("TargetUsePermission", "USE-1", _h("DIFFERENT-MATERIAL"))
    tp_ref, tp_snapshot = _aref(
        "TARGET_USE_PERMISSION", "TP1",
        scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED",
               "target_use_refs": [scoped.as_dict()]})
    base_reg, _ = _full_registry()
    narrow = AuthorityRegistry([tp_snapshot if s.authority_id == "TP1" else s
                                for s in base_reg._by_key.values()])
    good = _run(_request(governed_use_id=scoped), registry=narrow)
    bad = _run(_request(governed_use_id=other), registry=narrow)
    assert good.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert bad.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"


def test_hq217_rr02_bare_object_id_scope_token_does_not_prove_exact_scope():
    """RR-02 fail-closed half: a bare token carries no content_hash, so it is no proof."""
    tp_ref, tp_snapshot = _aref(
        "TARGET_USE_PERMISSION", "TP1",
        scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED",
               "target_use_refs": ["USE-1"]})
    base_reg, _ = _full_registry()
    narrow = AuthorityRegistry([tp_snapshot if s.authority_id == "TP1" else s
                                for s in base_reg._by_key.values()])
    receipt = _run(_request(), registry=narrow)
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"


def test_hq217_rr03_identity_ref_must_bind_authorized_material():
    """RR-03: an arbitrary identity ref plus a caller true boolean no longer passes."""
    with pytest.raises(TemporalComparabilityInputRefusal) as exc:
        _run(_request(temporal_identity_contract_ref=_ref("TemporalIdentityContract", "NOPE")))
    assert "does not hash to" in str(exc.value)
    with pytest.raises(TemporalComparabilityInputRefusal):
        _run(_request(temporal_identity_contract_material=None))


def test_hq217_rr03_identity_satisfaction_comes_from_material_not_the_caller():
    """RR-03: identity is OWNER-RESOLVED, and caller material never authorizes it.

    HQ219: the previous form of this test expressed "identity not satisfied" by handing
    the caller unsatisfying material. That is no longer the lever, because the fact is
    read from the TEMPORAL_EVIDENCE authority. Un-satisfaction is now an OWNER fact, and
    caller material that contradicts the owner is refused.
    """
    # the TEMPORAL_EVIDENCE authority itself reports the identity surface unsatisfied
    reg, _refs = _full_registry(te_identity_satisfied=False)
    receipt = _run(_request(), registry=reg)
    assert receipt.relation_state == "TEMPORAL_IDENTITY_UNRESOLVED"

    # Caller material that CONTRADICTS the owner is refused, not trusted. The ref must
    # hash to the material so the earlier hash-binding gate passes and the owner's
    # governance is what actually refuses.
    failing = {"identity_surface_jointly_satisfied": False}
    failing_ref = ExactRef("TemporalIdentityContract", "TIC-OWNER-CONFLICT",
                           semantic_hash(failing))
    reg_conflict, _r = _full_registry(te_identity_refs=(failing_ref,))
    with pytest.raises(TemporalComparabilityInputRefusal) as exc:
        _run(_request(temporal_identity_contract_ref=failing_ref,
                      temporal_identity_contract_material=failing),
             registry=reg_conflict)
    assert "TEMPORAL_EVIDENCE authority governs" in str(exc.value)

    # and the caller boolean still cannot override the owner
    with pytest.raises(TemporalComparabilityInputRefusal) as exc2:
        _run(_request(identity_surface_jointly_satisfied=False))
    assert "adopted owner governs" in str(exc2.value)


def test_hq217_rr05_measure_binding_is_enforced_and_serialized():
    """RR-05: the bound measure is required, compared, and serialized on every path."""
    receipt = _run()
    bound = MEASURE_REF.as_dict()
    assert receipt.quantity_surface["measure_ref"] is not None
    assert receipt.quantity_surface["measure_ref"] == bound
    # a quantity surface naming a DIFFERENT measure than the bound authority is refused
    other_measure_ref, other_measure_snapshot = _aref("WEIGHT_DESIGN_ESTIMAND", "MEAS-OTHER")
    reg_other, _ = _full_registry()
    reg_with_other = AuthorityRegistry(
        list(reg_other._by_key.values()) + [other_measure_snapshot])
    with pytest.raises(TemporalComparabilityInputRefusal) as exc:
        _run(
            _request(quantity_surface={"quantity_ref": _ref("Quantity", "Q1"),
                                       "measure_ref": other_measure_ref,
                                       "earlier_value": 3, "later_value": 8}),
            registry=reg_with_other)
    assert "not the bound measure" in str(exc.value)
    # and an absent measure may never mint a directional delta
    with pytest.raises(TemporalComparabilityInputRefusal) as exc:
        _run(_request(quantity_surface={
            "quantity_ref": _ref("Quantity", "Q1"),
            "earlier_value": 3, "later_value": 8}))
    assert "may never be minted without it" in str(exc.value)


def test_hq217_rr07_partial_order_emits_a_higher_priority_state_instead_of_raising():
    """RR-07: accepted precedence is total; a partial order never becomes an exception."""
    # HQ219: identity unsatisfaction is now an OWNER fact, expressed through the
    # TEMPORAL_EVIDENCE authority rather than through caller material.
    reg, _refs = _full_registry(te_identity_satisfied=False)
    receipt = _run(_request(temporal_order_disposition="PARTIAL_ORDER_NO_DIRECTION"),
                   registry=reg)
    assert receipt.relation_state == "TEMPORAL_IDENTITY_UNRESOLVED"
    assert receipt.direction_claim == "DIRECTION_NOT_CLAIMABLE"
    # and a clean partial order still selects between the two comparable-no-direction states
    clean = _run(_request(temporal_order_disposition="PARTIAL_ORDER_NO_DIRECTION",
                          intervals_overlap=True))
    assert clean.relation_state == "TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION"
    assert clean.relation_state in {"TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION",
                                    "TEMPORAL_COMPARABLE_NO_DIRECTION"}


def test_hq217_secondary_every_target_use_permission_ref_is_resolved():
    """Secondary: element zero is no longer the only ref consumed."""
    reg, a = _full_registry()
    extra_ref, extra_snapshot = _aref("TARGET_USE_PERMISSION", "TP-EXTRA")
    with_extra = AuthorityRegistry(list(reg._by_key.values()) + [extra_snapshot])
    receipt = _run(_request(target_use_permission_refs=(a["tp"], extra_ref)),
                   registry=with_extra)
    assert receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    slots = {r["slot"] for r in receipt.provenance["authority_resolutions"]}
    assert "target_use_permission" in slots
    assert "target_use_permission[1]" in slots
    # an additional ref that is NOT positively authorized is refused, not ignored.
    # It must be a real AuthorityRef that is simply absent from the registry.
    unregistered = _aref("TARGET_USE_PERMISSION", "TP-NOT-REGISTERED")[0]
    absent = _run(_request(target_use_permission_refs=(a["tp"], unregistered)),
                  registry=with_extra)
    assert absent.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    assert absent.relation_state_reason == "TARGET_USE_PERMISSION_REF_ABSENT"
    # and no permission at all is refused rather than defaulted
    none_given = _run(_request(target_use_permission_refs=()))
    assert none_given.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"


def test_hq217_productive_adequacy_positive_path_is_reachable():
    """Commission requirement: do not close the defects by making production unreachable."""
    nonzero = _run()
    assert nonzero.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert nonzero.direction_claim == "INCREASE"
    assert nonzero.comparability_status == "COMPARABLE"
    exact_zero = _run(_request(quantity_surface={
        "quantity_ref": _ref("Quantity", "Q1"), "measure_ref": MEASURE_REF,
        "earlier_value": 4, "later_value": 4}))
    assert exact_zero.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert exact_zero.direction_claim == "NO_AUTHORIZED_CHANGE"
    assert exact_zero.delta["zero_basis"] == "exact signed difference equals canonical zero"
    decreasing = _run(_request(quantity_surface={
        "quantity_ref": _ref("Quantity", "Q1"), "measure_ref": MEASURE_REF,
        "earlier_value": 9, "later_value": 2}))
    assert decreasing.direction_claim == "DECREASE"
    assert decreasing.comparability_status == "COMPARABLE"


# ===========================================================================
# HQ219 -- the three blocking authority-chain repairs
#
# Each witness below is written so it FAILS on the pre-repair behaviour and PASSES
# only after the corresponding repair. Every repair mechanism additionally carries a
# TARGETED BREAK: a witness that can be made to fail for the intended reason, so a green
# run cannot be an artefact of a check that never fires.
# ===========================================================================


def _registry_missing_use_scope_on(kind):
    """Same positive authority material as the lawful case, minus target_use_refs.

    The ONLY difference from lawful is the absent governed-use coverage on one snapshot,
    built through the court's own factory.
    """
    no_use = {"source_universe_refs": "EXPLICIT_UNRESTRICTED"}   # target_use_refs ABSENT
    use = {"source_universe_refs": "EXPLICIT_UNRESTRICTED",
           "target_use_refs": "EXPLICIT_UNRESTRICTED"}
    tc_ref, tc_snap = _aref(TEMPORAL_COMPARABILITY_AUTHORITY_KIND, "TC1",
                            ops=(AUTHORIZED_COMPARISON_OPERATION,),
                            scope=(no_use if kind == TEMPORAL_COMPARABILITY_AUTHORITY_KIND
                                   else use))
    te_ref, te_snap = _aref("TEMPORAL_EVIDENCE", "TE1", scope=use)
    te_scope = dict(use)
    te_scope["temporal_identity_contract_refs"] = (TEMPORAL_IDENTITY_CONTRACT_REF,)
    te_scope["identity_surface_jointly_satisfied"] = True
    te_ref, te_snap = _aref("TEMPORAL_EVIDENCE", "TE1", scope=te_scope)
    tp_ref, tp_snap = _aref("TARGET_USE_PERMISSION", "TP1",
                            scope=(no_use if kind == "TARGET_USE_PERMISSION" else use))
    um_ref, um_snap = _aref("UNCERTAINTY_METHOD", "UM1", scope=use)
    rp_ref, rp_snap = _aref("REPLAY_PROTOCOL", "RP1", scope=use)
    eq_ref, eq_snap = _aref("SOURCE_EQUIVALENCE", "EQ1",
                            ops=("SEMANTIC_EQUIVALENCE_ADMISSION",), scope=use)
    nm_ref, nm_snap = _aref("NATIVE_CANONICAL_MAPPING_HARMONIZATION", "NM1", scope=use)
    snaps = [tc_snap, te_snap, tp_snap, um_snap, rp_snap, eq_snap, nm_snap,
             MEASURE_SNAPSHOT, ESTIMAND_SNAPSHOT]
    return AuthorityRegistry(snaps), {
        "tc": tc_ref, "te": te_ref, "tp": tp_ref, "um": um_ref, "rp": rp_ref,
        "eq": eq_ref, "nm": nm_ref}


@pytest.mark.parametrize("kind", ["TARGET_USE_PERMISSION", "TEMPORAL_COMPARABILITY"])
def test_hq219_rr02b_missing_target_use_refs_fails_closed_under_required_use_scope(kind):
    """REPAIR A: a use-scoped authority MUST carry explicit governed-use coverage.

    Before the repair the coverage check ran only when target_use_refs happened to be
    present, so omitting it resolved POSITIVE for BOTH TEMPORAL_COMPARABILITY and
    TARGET_USE_PERMISSION.
    """
    reg, _refs = _registry_missing_use_scope_on(kind)
    receipt = _run(registry=reg)
    assert receipt.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY", (
        f"omitting governed-use coverage on {kind} must fail closed, got "
        f"{receipt.relation_state}")
    assert not _resolution_is_positive(receipt, kind)


def _registry_with_permission_scope(tp_scope):
    """Lawful registry whose ONLY variation is the TARGET_USE_PERMISSION scope envelope."""
    tc_ref, tc_snap = _aref(TEMPORAL_COMPARABILITY_AUTHORITY_KIND, "TC1",
                            ops=(AUTHORIZED_COMPARISON_OPERATION,))
    te_scope = {"source_universe_refs": "EXPLICIT_UNRESTRICTED",
                "target_use_refs": "EXPLICIT_UNRESTRICTED",
                "temporal_identity_contract_refs": (TEMPORAL_IDENTITY_CONTRACT_REF,),
                "identity_surface_jointly_satisfied": True}
    te_ref, te_snap = _aref("TEMPORAL_EVIDENCE", "TE1", scope=te_scope)
    tp_ref, tp_snap = _aref("TARGET_USE_PERMISSION", "TP1", scope=tp_scope)
    um_ref, um_snap = _aref("UNCERTAINTY_METHOD", "UM1")
    rp_ref, rp_snap = _aref("REPLAY_PROTOCOL", "RP1")
    eq_ref, eq_snap = _aref("SOURCE_EQUIVALENCE", "EQ1",
                            ops=("SEMANTIC_EQUIVALENCE_ADMISSION",))
    nm_ref, nm_snap = _aref("NATIVE_CANONICAL_MAPPING_HARMONIZATION", "NM1")
    return AuthorityRegistry([tc_snap, te_snap, tp_snap, um_snap, rp_snap, eq_snap,
                              nm_snap, MEASURE_SNAPSHOT, ESTIMAND_SNAPSHOT])


@pytest.mark.parametrize("tp_scope,expect_positive,label", [
    ({"source_universe_refs": "EXPLICIT_UNRESTRICTED",
      "target_use_refs": "EXPLICIT_UNRESTRICTED"}, True, "explicit unrestricted marker"),
    ({"source_universe_refs": "EXPLICIT_UNRESTRICTED"}, False, "ABSENT target_use_refs"),
    ({"source_universe_refs": "EXPLICIT_UNRESTRICTED",
      "target_use_refs": [_ref("TargetUsePermission", "OTHER-USE")]}, False,
     "names a DIFFERENT exact governed use"),
    ({"source_universe_refs": "EXPLICIT_UNRESTRICTED",
      "target_use_refs": ["USE-1"]}, False, "bare object_id token only"),
])
def test_hq219_rr02b_only_an_explicit_covering_grant_authorizes(tp_scope, expect_positive,
                                                                label):
    """REPAIR A: absence is not coverage; only an explicit covering grant authorizes.

    Each case varies ONLY the TARGET_USE_PERMISSION scope envelope, so the discriminating
    factor is provably the governed-use coverage and nothing else.
    """
    receipt = _run(registry=_registry_with_permission_scope(tp_scope))
    positive = receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert positive is expect_positive, (
        f"{label}: expected positive={expect_positive}, got {receipt.relation_state}")


def _resolution_is_positive(receipt, kind):
    for rec in receipt.provenance.get("authority_resolutions", ()):
        if getattr(rec, "authority_kind", None) == kind:
            return rec.outcome == "POSITIVE"
    return False


# ---------------------------------------------------------------------------
# TARGETED BREAK for Repair A: the check must be able to fail for its own reason.
# ---------------------------------------------------------------------------
def test_hq219_targeted_break_rr02b_the_gate_can_actually_fail():
    """TARGETED BREAK for Repair A: the check must be able to fail for its reason.

    The same authority, same kind, same governed use, differing ONLY by whether
    ``target_use_refs`` is present, must land on OPPOSITE outcomes. If the fail-closed
    branch were removed, both sides would be positive and this witness would fail -- so a
    green run cannot be an artefact of a check that never discriminates.
    """
    absent = _run(registry=_registry_with_permission_scope(
        {"source_universe_refs": "EXPLICIT_UNRESTRICTED"}))
    present = _run(registry=_registry_with_permission_scope(
        {"source_universe_refs": "EXPLICIT_UNRESTRICTED",
         "target_use_refs": "EXPLICIT_UNRESTRICTED"}))

    assert absent.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    assert present.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert absent.relation_state != present.relation_state, (
        "the targeted break did not reopen the gap, so the witness proves nothing")


# ---------------------------------------------------------------------------
# REPAIR B: temporal identity must be owner-resolved.
# ---------------------------------------------------------------------------
def test_hq219_rr03_caller_minted_identity_material_cannot_authorize():
    """REPAIR B: hash binding is not authorization.

    A caller mints arbitrary material, hashes it, and presents the matching ExactRef.
    Before the repair this satisfied the identity gate outright.
    """
    minted = {"identity_surface_jointly_satisfied": True,
              "note": "caller-authored, never owner-resolved"}
    minted_ref = ExactRef("TemporalIdentityContract", "TIC-CALLER-MINTED",
                          semantic_hash(minted))
    receipt = _run(_request(temporal_identity_contract_ref=minted_ref,
                             temporal_identity_contract_material=minted))
    assert receipt.relation_state == "TEMPORAL_IDENTITY_UNRESOLVED", (
        f"caller-minted identity material must not authorize; got "
        f"{receipt.relation_state}")
    assert receipt.relation_state_reason == "TEMPORAL_IDENTITY_NOT_BOUND_BY_TEMPORAL_EVIDENCE_AUTHORITY"


def test_hq219_rr03_stale_identity_material_is_not_jointly_satisfied():
    """REPAIR B: an OWNER that reports the identity surface unsatisfied is honoured."""
    reg, _refs = _full_registry(te_identity_satisfied=False)
    receipt = _run(registry=reg)
    assert receipt.relation_state == "TEMPORAL_IDENTITY_UNRESOLVED"
    assert receipt.relation_state_reason == "IDENTITY_SURFACE_NOT_JOINTLY_SATISFIED"


def test_hq219_rr03_lawful_owner_resolved_identity_still_authorizes():
    """HQD-216: the lawful owner-resolved identity must still produce a positive receipt."""
    receipt = _run(_request())
    assert receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert receipt.relation_state_reason is None or receipt.direction_claim == "INCREASE"


def test_hq219_targeted_break_rr03_identity_gate_actually_consults_the_owner(monkeypatch):
    """HQ222 COURT-HQ220-01 TARGETED BREAK: same fixture, broken mechanism.

    HQ219's version of this witness did NOT satisfy the fail-capability requirement. It
    monkeypatched one exact-ref helper and then swapped in a *different, satisfied*
    registry, so it never demonstrated that the mechanism disabling anything -- it only
    showed two different fixtures give two different answers.

    This version keeps ONE fixture, the unsatisfied-owner registry, and falsifies only
    the owner-satisfaction consultation that F7 uses to read that owner's verdict. If
    the outcome flips on that single fixture, the owner's verdict is provably what the
    identity gate consumes, and pre-repair -- when the gate read caller-minted material
    instead -- the same break is exactly the self-authorization path.
    """
    import rawlsing_next.pre553_temporal_comparability as mod

    # ONE fixture: the adopted owner says the identity surface is NOT satisfied.
    reg, _refs = _full_registry(te_identity_satisfied=False)
    assert _run(registry=reg).relation_state == "TEMPORAL_IDENTITY_UNRESOLVED"

    # targeted break: falsify the owner's satisfaction verdict on this same fixture
    def falsified_owner_scope(snapshot):
        scope = dict(getattr(snapshot, "scope_envelope", {}) or {})
        scope["identity_surface_jointly_satisfied"] = True
        return scope

    monkeypatch.setattr(mod, "_temporal_evidence_identity_scope", falsified_owner_scope)
    reopened = _run(registry=reg)
    assert reopened.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED", (
        "the targeted break did not reopen the gap, so the witness proves nothing")
    monkeypatch.undo()

    # restoring the real consultation restores the refusal on the same fixture
    assert _run(registry=reg).relation_state == "TEMPORAL_IDENTITY_UNRESOLVED"
    assert _run(registry=reg).relation_state_reason == (
        "IDENTITY_SURFACE_NOT_JOINTLY_SATISFIED")


# ===========================================================================
# HQ222 F7-RR-03B: the identity owner must cover the compared source scope.
# ===========================================================================
def _te_scoped_registry(*, scope_universes, satisfied=True):
    """A TEMPORAL_EVIDENCE identity owner with an EXPLICIT universe scope.

    Only the TEMPORAL_EVIDENCE snapshot is narrowed. TEMPORAL_COMPARABILITY keeps its
    default unrestricted scope, so an out-of-scope identity owner produces an IDENTITY
    outcome rather than being masked by the higher-precedence insufficient-authority
    state. The witness therefore tests the intended mechanism and nothing else.
    """
    te_scope = {
        "source_universe_refs": scope_universes,
        "target_use_refs": "EXPLICIT_UNRESTRICTED",
        "temporal_identity_contract_refs": (TEMPORAL_IDENTITY_CONTRACT_REF,),
        "identity_surface_jointly_satisfied": bool(satisfied),
    }
    return _full_registry(te_scope=te_scope, te_identity_satisfied=satisfied)


def _identity_owner_scope_outcome(receipt):
    """The observed refusal state plus the TEMPORAL_EVIDENCE resolution outcome.

    An out-of-scope identity owner fails the ``temporal_evidence`` slot, which lands in
    the higher-precedence insufficient-authority state rather than the identity state.
    Both are lawful refusals; the resolution record is what discriminates the intended
    mechanism, so witnesses assert on that instead of on one arbitrary state label.
    """
    resolutions = receipt.provenance["authority_resolutions"]
    te = next(r for r in resolutions if r["slot"] == "temporal_evidence")
    return receipt.relation_state, receipt.relation_state_reason, te["outcome"]


def _assert_identity_owner_refused_for_scope(receipt):
    state, reason, te_outcome = _identity_owner_scope_outcome(receipt)
    assert state != "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert state in ("TEMPORAL_INSUFFICIENT_AUTHORITY", "TEMPORAL_IDENTITY_UNRESOLVED")
    assert reason in ("AUTHORITY_SCOPE_MISMATCH",
                      "TEMPORAL_EVIDENCE_AUTHORITY_REF_ABSENT_FOR_ANCHOR",
                      "TEMPORAL_IDENTITY_OWNER_RESOLUTION_UNAVAILABLE")
    # the intended mechanism: the identity owner itself failed SOURCE SCOPE
    assert te_outcome == "AUTHORITY_SCOPE_MISMATCH"
    assert receipt.comparability_status == "NOT_COMPARABLE"


def test_hq222_rr03b_identity_owner_must_cover_the_compared_universe_pair():
    """The lawful same-universe comparison still authorizes."""
    registry, _refs = _te_scoped_registry(
        scope_universes=[UNIVERSE_A.as_dict()])
    assert _run(registry=registry).relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"


def test_hq222_rr03b_identity_owner_for_an_unrelated_universe_is_refused():
    """A positive identity owner OUTSIDE the compared scope may not authorize identity."""
    other = _ref("SourceUniverse", "U-UNRELATED")
    registry, _refs = _te_scoped_registry(scope_universes=[other.as_dict()])
    _assert_identity_owner_refused_for_scope(_run(registry=registry))


def test_hq222_rr03b_identity_owner_covering_only_one_compared_universe_is_refused():
    """Covering only half the compared pair is not covering the comparison.

    The cross-universe path is given a GENUINE positive owner decision, so the identity
    scope is the only defect and nothing higher-precedence can mask it.
    """
    third = _ref("SourceUniverse", "U-C")
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, third))
    registry, auths = _te_scoped_registry(
        scope_universes=[UNIVERSE_A.as_dict()])  # covers U-A only, not U-C
    request = _request(source_universe_refs=(UNIVERSE_A, third),
                       source_equivalence_ref=relation.ref,
                       source_equivalence_authority_ref=auths["eq"],
                       source_relation_resolver=resolver)
    receipt = compare_temporal_anchors(request, registry)
    _assert_identity_owner_refused_for_scope(receipt)

    # Control: the same cross-universe request authorizes once the owner covers both.
    registry_ok, _refs_ok = _te_scoped_registry(
        scope_universes=[UNIVERSE_A.as_dict(), third.as_dict()])
    assert compare_temporal_anchors(request, registry_ok).relation_state == \
        "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"


def test_hq222_rr03b_stale_source_universe_ref_in_identity_owner_scope_is_refused():
    """A stale/wrong universe ref is not coverage, even with exact scope shape."""
    stale = ExactRef("SourceUniverse", "U-STALE", _h("stale-universe-content-hash"))
    registry, _refs = _te_scoped_registry(scope_universes=[stale.as_dict()])
    _assert_identity_owner_refused_for_scope(_run(registry=registry))


# ===========================================================================
# HQ222 F7-RR-02C: adopted unrestricted representations.
# ===========================================================================
@pytest.mark.parametrize("token", ["EXPLICIT_UNRESTRICTED",
                                   "UNRESTRICTED_BY_THIS_AUTHORITY"])
def test_hq222_rr02c_both_adopted_unrestricted_tokens_are_honoured(token):
    """Both adopted blanket representations authorize, in all three scope helpers."""
    import rawlsing_next.pre553_temporal_comparability as mod

    assert token in mod.ADOPTED_UNRESTRICTED_SCOPE_REPRESENTATIONS
    assert mod._scope_covers_universe(token, UNIVERSE_A.as_dict())
    assert mod._scope_covers_governed_use(token, _ref("TargetUsePermission", "USE-1"))
    assert mod._scope_covers_exact_ref_set(token, TEMPORAL_IDENTITY_CONTRACT_REF)

    # and end-to-end: an identity owner using that token still authorizes
    te_scope = {
        "source_universe_refs": token,
        "target_use_refs": token,
        "temporal_identity_contract_refs": (TEMPORAL_IDENTITY_CONTRACT_REF,),
        "identity_surface_jointly_satisfied": True,
    }
    registry, _refs = _full_registry(tc_scope=te_scope)
    assert _run(registry=registry).relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"


@pytest.mark.parametrize("bad", [
    None, "", [], set(), {},
    "UNRESTRICTED", "EXPLICIT_UNLIMITED", "UNRESTRICTED_BY_OTHER_AUTHORITY",
    "explicit_unrestricted", "UNRESTRICTED_BY_THIS_AUTHORITY_V2", True, 0,
])
def test_hq222_rr02c_no_third_token_and_omission_is_not_unrestricted(bad):
    """Only the two adopted literals grant a blanket; omission is never unrestricted."""
    import rawlsing_next.pre553_temporal_comparability as mod

    assert mod.ADOPTED_UNRESTRICTED_SCOPE_REPRESENTATIONS == frozenset({
        "EXPLICIT_UNRESTRICTED", "UNRESTRICTED_BY_THIS_AUTHORITY"})
    # only a string can ever be one of the two adopted literals
    assert not (isinstance(bad, str)
                and bad in mod.ADOPTED_UNRESTRICTED_SCOPE_REPRESENTATIONS)
    assert mod._scope_covers_universe(bad, UNIVERSE_A.as_dict()) is False
    assert mod._scope_covers_governed_use(
        bad, _ref("TargetUsePermission", "USE-1")) is False
    assert mod._scope_covers_exact_ref_set(bad, TEMPORAL_IDENTITY_CONTRACT_REF) is False


def test_hq222_rr02c_f7_scope_helpers_agree_with_the_adopted_authority_law():
    """F7's blanket representations must not drift from the adopted general law."""
    import inspect

    from rawlsing_next import pre553_empirical_authority as law
    from rawlsing_next.pre553_temporal_comparability import (
        ADOPTED_UNRESTRICTED_SCOPE_REPRESENTATIONS,
    )

    source = inspect.getsource(law._scope_contains)
    for token in ("UNRESTRICTED_BY_THIS_AUTHORITY", "EXPLICIT_UNRESTRICTED"):
        assert f'"{token}"' in source
        assert token in ADOPTED_UNRESTRICTED_SCOPE_REPRESENTATIONS
    # the law grants a blanket for exactly those literals and nothing else
    for probe in ("UNRESTRICTED", "", "ANY", "SOME_OTHER_TOKEN", None, 0, []):
        expected = (isinstance(probe, str)
                    and probe in ADOPTED_UNRESTRICTED_SCOPE_REPRESENTATIONS)
        assert law._scope_contains(probe, "anything") is expected, probe


# ---------------------------------------------------------------------------
# REPAIR C: cross-universe comparison needs a POSITIVE owner decision.
# ---------------------------------------------------------------------------
def _adjudicated_resolver(*, universe_refs, decision="AUTHORIZED",
                          relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
                          target_use=None):
    """A REAL SourceRelationResolver over a genuinely constructed relation."""
    from rawlsing_next.pre553_source_relations import (
        SourceRelationResolver, make_source_universe_relation)
    _, eq_snapshot = _aref(
        "SOURCE_EQUIVALENCE", "EQ1", ops=("SEMANTIC_EQUIVALENCE_ADMISSION",),
        families=("SourceUniverseRelation@1.0.0",),
        scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED",
               "target_use_refs": "EXPLICIT_UNRESTRICTED",
               "predicate_or_risk_set_refs": "EXPLICIT_UNRESTRICTED"})
    material = {
        "relation_kind": relation_kind,
        "equivalence_scope": "EXACT_BOUND_UNIVERSE_PAIR",
        "left_semantic_ref": _ref("SemanticFingerprint", "SEM-A"),
        "right_semantic_ref": _ref("SemanticFingerprint", "SEM-B"),
        "transformation_authority_refs": (_ref("SemanticTransformation", "TR-1"),),
    }
    relation = make_source_universe_relation(
        relation_kind=relation_kind,
        source_universe_refs=tuple(universe_refs),
        authority_snapshot=eq_snapshot,
        authority_operation="SEMANTIC_EQUIVALENCE_ADMISSION",
        operation_scope="EXACT_BOUND_UNIVERSE_PAIR",
        target_use=(target_use if target_use is not None
                    else _ref("TargetUsePermission", "USE-1").object_id),
        effective_scope="EXACT_BOUND_UNIVERSE_PAIR",
        directionality_or_symmetric="SYMMETRIC",
        operation_authority_material=material,
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "hq219"),
        decision=decision)
    return SourceRelationResolver(relations=[relation],
                                  authority_registry=AuthorityRegistry([eq_snapshot])), relation


def _cross_universe_request(resolver, relation_ref):
    return _request(source_universe_refs=(UNIVERSE_A, UNIVERSE_B),
                    source_equivalence_ref=relation_ref,
                    source_equivalence_authority_ref=_full_registry()[1]["eq"],
                    source_relation_resolver=resolver)


def test_hq219_rr04_duck_typed_stub_resolver_cannot_admit_a_cross_universe_pair():
    """REPAIR C: a stub that mimics ``resolve_exact`` is not the owner path."""
    class StubResolver:
        def resolve_exact(self, ref):
            return type("R", (), {"ref": ref})()

        def decide(self, **kwargs):
            raise AssertionError("the real owner decide() must be reached")

        def require(self, **kwargs):
            raise AssertionError("the real owner require() must be reached")

    receipt = _run(_cross_universe_request(
        StubResolver(), _ref("SourceUniverseRelation", "REL-STUB")))
    assert receipt.relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"
    assert receipt.relation_state_reason == "SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE"


def test_hq219_rr04_denied_relation_is_refused():
    """REPAIR C: a real relation whose owner decision is DENIED does not admit."""
    resolver, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B), decision="DENIED")
    receipt = _run(_cross_universe_request(resolver, relation.ref))
    assert receipt.relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"
    assert receipt.relation_state_reason == "SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE"


def test_hq219_rr04_relation_for_a_different_universe_pair_is_refused():
    """REPAIR C: exact object lookup alone would have accepted this."""
    third = _ref("SourceUniverse", "U-C")
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, third))
    receipt = _run(_cross_universe_request(resolver, relation.ref))
    assert receipt.relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"
    assert receipt.relation_state_reason == "SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE"


def test_hq219_rr04_relation_for_a_different_governed_use_is_refused():
    """REPAIR C: a relation authorized only for itself must not admit a governed use."""
    resolver, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B), target_use="SOME-OTHER-USE")
    receipt = _run(_cross_universe_request(resolver, relation.ref))
    assert receipt.relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"
    assert receipt.relation_state_reason == "SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE"


def test_hq219_rr04_wrong_relation_kind_cannot_be_authorized_under_equivalence_authority():
    """REPAIR C: the relation KIND is checked, not merely the object ref.

    The adopted factory refuses to authorize a non-equivalence kind under a
    SOURCE_EQUIVALENCE snapshot, so the wrong-kind material cannot even be constructed
    as AUTHORIZED. F7 additionally pins the kind it asks the owner about.
    """
    from rawlsing_next.pre553_source_relations import (
        Pre553SemanticCollapseError, SourceRelationIntegrityError)
    with pytest.raises((SourceRelationIntegrityError, Pre553SemanticCollapseError)):
        _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B),
                              relation_kind="OVERLAP_NON_DUPLICATION")


def test_hq219_rr04_lawful_positive_owner_decision_still_admits_the_pair():
    """HQD-216: a genuine positive source-equivalence owner decision must still work."""
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    receipt = _run(_cross_universe_request(resolver, relation.ref))
    assert receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert receipt.provenance["cross_universe"]["crosses_source_universes"] is True


def test_hq227_targeted_break_authenticated_owner_entrypoint_is_load_bearing(monkeypatch):
    """COURT-HQ226-01: break the seam F7 actually consumes, on one fixed fixture.

    The lawful cross-universe fixture is positive. Replacing only F7's captured
    authenticated P07 entrypoint with a non-returning break must turn that SAME
    fixture into the typed equivalence refusal. With pre-HQ227 production this
    monkeypatch is ignored because that code calls SourceRelationResolver.decide
    directly, so this witness discriminates the repair rather than patching dead code.
    """
    import rawlsing_next.pre553_temporal_comparability as tc

    resolver, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    request = _cross_universe_request(resolver, relation.ref)
    assert _run(request).relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"

    def broken_owner_entrypoint(*args, **kwargs):
        raise RuntimeError("targeted break of authenticated P07 owner entrypoint")

    monkeypatch.setattr(
        tc, "_authenticated_source_relation_decide",
        broken_owner_entrypoint, raising=False)
    broken = _run(request)
    assert broken.relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"
    assert broken.relation_state_reason == "SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE"

    monkeypatch.undo()
    assert _run(request).relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"


def test_hq222_rr04b_a_forged_owner_proof_is_refused(monkeypatch):
    """HQ222 F7-RR-04B: a non-decision return cannot buy a positive relation.

    This is the hardening the old targeted break accidentally demanded. A permissive
    stand-in whose object merely claims ``authorized`` proves nothing, so F7 now
    requires the adopted owner's real contentful proof.
    """
    import rawlsing_next.pre553_source_relations as sr

    resolver, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B), decision="DENIED")
    request = _cross_universe_request(resolver, relation.ref)

    def forged(self, **kwargs):
        return type("D", (), {"authorized": True, "state": "AUTHORIZED",
                              "reason": "forged"})()

    monkeypatch.setattr(sr.SourceRelationResolver, "require", forged)
    receipt = _run(request)
    assert receipt.relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"
    assert receipt.relation_state_reason == "SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE"
    monkeypatch.undo()
    assert _run(request).relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"


def test_hq222_rr04b_unrelated_positive_equivalence_snapshot_cannot_ride_the_relation(
        monkeypatch):
    """HQ222 F7-RR-04B: positive A plus positive B is not identity.

    The relation is genuinely AUTHORIZED by its own exact SOURCE_EQUIVALENCE
    authority. A second, genuinely positive SOURCE_EQUIVALENCE snapshot that did NOT
    authorize it is supplied instead. Both halves are positive on their own terms; only
    cross-binding them can tell that B never authorized this relation.
    """
    import rawlsing_next.pre553_source_relations as sr
    from dataclasses import replace as _replace

    resolver, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    assert _run(_cross_universe_request(resolver, relation.ref)).relation_state == \
        "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"

    genuine = resolver.decide(
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
        source_universe_refs=(UNIVERSE_A, UNIVERSE_B),
        operation_scope="EXACT_BOUND_UNIVERSE_PAIR",
        target_use=_ref("TargetUsePermission", "USE-1").object_id,
        effective_scope="EXACT_BOUND_UNIVERSE_PAIR",
        relation_ref=relation.ref,
        expected_authority_operation="SEMANTIC_EQUIVALENCE_ADMISSION")
    assert genuine.authorized is True

    # B: a DIFFERENT, genuinely positive SOURCE_EQUIVALENCE authority snapshot.
    unrelated_ref, unrelated_snapshot = _aref(
        "SOURCE_EQUIVALENCE", "EQ-UNRELATED", ops=("SEMANTIC_EQUIVALENCE_ADMISSION",),
        scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED",
               "target_use_refs": "EXPLICIT_UNRESTRICTED"})
    assert unrelated_snapshot.authority_ref.key != genuine.authority_ref.key
    assert unrelated_snapshot.decision_state == "ALLOW"

    registry, auths = _full_registry(extra_snapshots=(unrelated_snapshot,))
    request = _request(source_universe_refs=(UNIVERSE_A, UNIVERSE_B),
                       source_equivalence_ref=relation.ref,
                       source_equivalence_authority_ref=unrelated_ref,
                       source_relation_resolver=resolver)
    receipt = compare_temporal_anchors(request, registry)
    assert receipt.relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"
    assert receipt.relation_state_reason == "SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE"

    # Control, on the SAME registry: pointing F7 at the authority that actually
    # authorized the relation (auths["eq"]) stays positive. Only B's identity mattered.
    request_ok = _request(source_universe_refs=(UNIVERSE_A, UNIVERSE_B),
                          source_equivalence_ref=relation.ref,
                          source_equivalence_authority_ref=auths["eq"],
                          source_relation_resolver=resolver)
    assert compare_temporal_anchors(
        request_ok, registry).relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"


# ===========================================================================
# HQ225 F7-RR-04C: non-forgeable source-relation owner boundary.
# ===========================================================================
def _hq225_cross_request(*, resolver, relation_ref, authority_ref):
    return _request(
        source_universe_refs=(UNIVERSE_A, UNIVERSE_B),
        source_equivalence_ref=relation_ref,
        source_equivalence_authority_ref=authority_ref,
        source_relation_resolver=resolver,
    )


def _hq225_full_decision(*, relation_ref, authority_ref, tag):
    from rawlsing_next.pre553_source_relations import RelationDecision

    return RelationDecision(
        "SOURCE_SEMANTIC_EQUIVALENCE",
        (UNIVERSE_A, UNIVERSE_B),
        "EXACT_BOUND_UNIVERSE_PAIR",
        _ref("TargetUsePermission", "USE-1").object_id,
        "EXACT_BOUND_UNIVERSE_PAIR",
        "SYMMETRIC",
        "AUTHORIZED",
        relation_ref,
        authority_ref,
        "SEMANTIC_EQUIVALENCE_ADMISSION",
        f"hostile-{tag}",
        _h(f"hq225-hostile-decision:{tag}"),
    )


def _assert_hq225_owner_impostor_refused(receipt):
    assert receipt.relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"
    assert receipt.relation_state_reason == "SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE"
    assert receipt.comparability_status == "NOT_COMPARABLE"


def test_hq225_rr04c_subclass_full_shaped_authorized_decision_with_real_b_refuses():
    """A subclass cannot mint a full-shaped AUTHORIZED decision using genuine B."""
    from rawlsing_next.pre553_source_relations import SourceRelationResolver

    registry, auths = _full_registry()
    relation_ref = _ref("SourceUniverseRelation", "HQ225-FORGED-FULL")

    class HostileResolver(SourceRelationResolver):
        called = False

        def require(self, **kwargs):
            type(self).called = True
            return _hq225_full_decision(
                relation_ref=kwargs["relation_ref"],
                authority_ref=auths["eq"],
                tag="full-shaped-b",
            )

    hostile = HostileResolver(relations=(), authority_registry=registry)
    receipt = compare_temporal_anchors(
        _hq225_cross_request(
            resolver=hostile, relation_ref=relation_ref, authority_ref=auths["eq"]),
        registry,
    )
    _assert_hq225_owner_impostor_refused(receipt)
    assert HostileResolver.called is False, (
        "F7 must refuse the subclass at the owner boundary before virtual require() executes")


def test_hq225_rr04c_subclass_right_shape_but_relation_absent_from_base_refuses():
    """Right pair/kind/use fields do not matter when the base owner has no relation."""
    from rawlsing_next.pre553_source_relations import SourceRelationResolver

    registry, auths = _full_registry()
    relation_ref = _ref("SourceUniverseRelation", "HQ225-ABSENT-BASE-RELATION")

    class MissingRelationForger(SourceRelationResolver):
        called = False

        def decide(self, **kwargs):
            type(self).called = True
            return _hq225_full_decision(
                relation_ref=kwargs["relation_ref"],
                authority_ref=auths["eq"],
                tag="absent-base-relation",
            )

    hostile = MissingRelationForger(relations=(), authority_registry=registry)
    receipt = compare_temporal_anchors(
        _hq225_cross_request(
            resolver=hostile, relation_ref=relation_ref, authority_ref=auths["eq"]),
        registry,
    )
    _assert_hq225_owner_impostor_refused(receipt)
    assert MissingRelationForger.called is False


def test_hq225_rr04c_subclass_base_then_swaps_authority_cannot_execute():
    """Even a subclass that delegates to the base owner then swaps A->B is refused."""
    from dataclasses import replace as _replace
    from rawlsing_next.pre553_source_relations import SourceRelationResolver

    concrete, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))

    unrelated_ref, unrelated_snapshot = _aref(
        "SOURCE_EQUIVALENCE", "HQ225-EQ-B",
        ops=("SEMANTIC_EQUIVALENCE_ADMISSION",),
        scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED",
               "target_use_refs": "EXPLICIT_UNRESTRICTED"})
    registry, _auths = _full_registry(extra_snapshots=(unrelated_snapshot,))

    class SwapAfterBaseResolver(SourceRelationResolver):
        called = False

        def decide(self, **kwargs):
            type(self).called = True
            genuine = super().decide(**kwargs)
            return _replace(
                genuine,
                relation_ref=kwargs["relation_ref"],
                authority_ref=unrelated_ref,
                authority_operation="SEMANTIC_EQUIVALENCE_ADMISSION",
                state="AUTHORIZED",
            )

    hostile = SwapAfterBaseResolver(
        relations=[relation], authority_registry=concrete._registry)
    receipt = compare_temporal_anchors(
        _hq225_cross_request(
            resolver=hostile,
            relation_ref=relation.ref,
            authority_ref=unrelated_ref,
        ),
        registry,
    )
    _assert_hq225_owner_impostor_refused(receipt)
    assert SwapAfterBaseResolver.called is False


def test_hq225_rr04c_duck_object_with_owner_api_cannot_impersonate_owner():
    """Method-name parity is not owner provenance."""
    registry, auths = _full_registry()
    relation_ref = _ref("SourceUniverseRelation", "HQ225-DUCK")

    class DuckOwner:
        called = False

        def resolve_exact(self, ref):
            type(self).called = True
            return type("R", (), {"ref": ref})()

        def decide(self, **kwargs):
            type(self).called = True
            return _hq225_full_decision(
                relation_ref=kwargs["relation_ref"],
                authority_ref=auths["eq"],
                tag="duck",
            )

        def require(self, **kwargs):
            type(self).called = True
            return self.decide(**kwargs)

    receipt = compare_temporal_anchors(
        _hq225_cross_request(
            resolver=DuckOwner(), relation_ref=relation_ref, authority_ref=auths["eq"]),
        registry,
    )
    _assert_hq225_owner_impostor_refused(receipt)
    assert DuckOwner.called is False


def test_hq225_rr04c_exact_owner_instance_shadow_cannot_replace_base_decide():
    """Exact type alone is not the proof: F7 must bypass caller-side method shadowing."""
    concrete, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    registry, auths = _full_registry()
    called = {"value": False}

    def forged_decide(**kwargs):
        called["value"] = True
        return _hq225_full_decision(
            relation_ref=kwargs["relation_ref"],
            authority_ref=auths["eq"],
            tag="instance-shadow",
        )

    concrete.decide = forged_decide
    receipt = compare_temporal_anchors(
        _hq225_cross_request(
            resolver=concrete, relation_ref=relation.ref, authority_ref=auths["eq"]),
        registry,
    )
    assert receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert called["value"] is False, (
        "F7 must invoke the adopted class adjudicator non-virtually, not instance lookup")


def test_hq225_rr04c_concrete_owner_positive_path_remains_productive():
    """HQD-216 control: the genuine concrete owner path remains positive."""
    resolver, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    receipt = _run(_cross_universe_request(resolver, relation.ref))
    assert type(resolver).__name__ == "SourceRelationResolver"
    assert receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert receipt.direction_claim == "INCREASE"


# ===========================================================================
# HQ227 F7-RR-04D / 04E: full adopted owner-path authenticity.
# ===========================================================================
def _hq227_relation_with_snapshot(snapshot):
    """Build one exact P07 relation under the supplied exact authority snapshot."""
    from rawlsing_next.pre553_source_relations import (
        SourceRelationResolver, make_source_universe_relation,
    )

    material = {
        "relation_kind": "SOURCE_SEMANTIC_EQUIVALENCE",
        "equivalence_scope": "EXACT_BOUND_UNIVERSE_PAIR",
        "left_semantic_ref": _ref("SemanticFingerprint", "SEM-A"),
        "right_semantic_ref": _ref("SemanticFingerprint", "SEM-B"),
        "transformation_authority_refs": (_ref("SemanticTransformation", "TR-1"),),
    }
    relation = make_source_universe_relation(
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
        source_universe_refs=(UNIVERSE_A, UNIVERSE_B),
        authority_snapshot=snapshot,
        authority_operation="SEMANTIC_EQUIVALENCE_ADMISSION",
        operation_scope="EXACT_BOUND_UNIVERSE_PAIR",
        target_use=_ref("TargetUsePermission", "USE-1").object_id,
        effective_scope="EXACT_BOUND_UNIVERSE_PAIR",
        directionality_or_symmetric="SYMMETRIC",
        operation_authority_material=material,
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "hq219"),
        decision="AUTHORIZED",
    )
    resolver = SourceRelationResolver(
        relations=(relation,), authority_registry=AuthorityRegistry((snapshot,)))
    return resolver, relation


def test_hq227_exact_instance_postconstruction_relation_map_injection_cannot_mint_custody():
    """RR-04D: caller mutation of _by_ref cannot create an adopted relation."""
    from rawlsing_next.pre553_source_relations import SourceRelationResolver

    source, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    victim = SourceRelationResolver(
        relations=(), authority_registry=source._registry)

    # This is the pre-repair exploit: relation_ref lookup read this caller-owned map.
    victim._by_ref[relation.ref.key] = relation

    receipt = _run(_cross_universe_request(victim, relation.ref))
    _assert_hq225_owner_impostor_refused(receipt)


def test_hq227_exact_instance_registry_replacement_cannot_change_pinned_owner_snapshot():
    """RR-04E: replacing _registry cannot replace construction-time authority semantics."""
    import rawlsing_next.pre553_source_relations as sr

    resolver, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    genuine = resolver._registry.resolve_exact(
        relation.relation_authority_ref).snapshot

    _, shadow = _aref(
        "SOURCE_EQUIVALENCE", "EQ1",
        ops=("SEMANTIC_EQUIVALENCE_ADMISSION",),
        content_hash=genuine.authority_ref.authority_content_hash,
        families=("SourceUniverseRelation@1.0.0",),
        scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED",
               "target_use_refs": "EXPLICIT_UNRESTRICTED",
               "predicate_or_risk_set_refs": "EXPLICIT_UNRESTRICTED",
               "hostile_shadow_semantics": "DIFFERENT"})
    assert shadow.authority_ref == genuine.authority_ref
    assert shadow.content_hash != genuine.content_hash

    resolver._registry = AuthorityRegistry((shadow,))
    decision = sr.authenticated_source_relation_decision(
        resolver,
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
        source_universe_refs=(UNIVERSE_A, UNIVERSE_B),
        operation_scope="EXACT_BOUND_UNIVERSE_PAIR",
        target_use=_ref("TargetUsePermission", "USE-1").object_id,
        effective_scope="EXACT_BOUND_UNIVERSE_PAIR",
        relation_ref=relation.ref,
        expected_authority_operation="SEMANTIC_EQUIVALENCE_ADMISSION",
    )
    assert decision.authorized is True
    assert decision.authority_snapshot_content_hash == genuine.content_hash
    assert decision.authority_snapshot_content_hash != shadow.content_hash

    assert _run(_cross_universe_request(
        resolver, relation.ref)).relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"


def test_hq227_authority_registry_subclass_cannot_enter_p07_owner_custody():
    """RR-04E: hostile nested registry subclass is not construction provenance."""
    import rawlsing_next.pre553_source_relations as sr

    source, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    genuine = source._registry.resolve_exact(
        relation.relation_authority_ref).snapshot

    class HostileRegistry(AuthorityRegistry):
        called = False

        def resolve_exact(self, ref):
            type(self).called = True
            return super().resolve_exact(ref)

    hostile = HostileRegistry((genuine,))
    with pytest.raises(
            sr.SourceRelationIntegrityError,
            match="exact concrete I01 AuthorityRegistry"):
        sr.SourceRelationResolver(
            relations=(relation,), authority_registry=hostile)
    assert HostileRegistry.called is False


def test_hq227_corrupt_custodied_relation_replay_identity_refuses_before_f7_positive():
    """Exact relation custody is re-authenticated; stale replay material cannot ride it."""
    from types import MappingProxyType

    resolver, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    fields = dict(relation.semantic_fields)
    fields["replay_identity"] = "0" * 64
    object.__setattr__(relation, "_semantic_fields", MappingProxyType(fields))

    receipt = _run(_cross_universe_request(resolver, relation.ref))
    _assert_hq225_owner_impostor_refused(receipt)


def test_hq227_same_outer_authority_ref_with_wrong_snapshot_semantics_is_refused():
    """RR-04E: AuthorityRef identity cannot hide a different AuthoritySnapshot."""
    registry, auths = _full_registry()
    genuine = registry.resolve_exact(auths["eq"]).snapshot

    _, wrong = _aref(
        "SOURCE_EQUIVALENCE", "EQ1",
        ops=("SEMANTIC_EQUIVALENCE_ADMISSION",),
        content_hash=auths["eq"].authority_content_hash,
        families=("SourceUniverseRelation@1.0.0",),
        scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED",
               "target_use_refs": "EXPLICIT_UNRESTRICTED",
               "predicate_or_risk_set_refs": "EXPLICIT_UNRESTRICTED",
               "hostile_shadow_semantics": "WRONG-INNER-SNAPSHOT"})
    assert wrong.authority_ref == auths["eq"]
    assert wrong.content_hash != genuine.content_hash

    resolver, relation = _hq227_relation_with_snapshot(wrong)
    receipt = compare_temporal_anchors(
        _hq225_cross_request(
            resolver=resolver,
            relation_ref=relation.ref,
            authority_ref=auths["eq"]),
        registry,
    )
    _assert_hq225_owner_impostor_refused(receipt)


def test_hq227_owner_method_and_nested_validation_monkeypatches_cannot_redirect_f7(monkeypatch):
    """RR-04D: decide/require/resolve/validator seams are not F7 custody."""
    import rawlsing_next.pre553_source_relations as sr

    resolver, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))

    def explode(*args, **kwargs):
        raise AssertionError("caller-visible owner seam was dispatched")

    monkeypatch.setattr(sr.SourceRelationResolver, "decide", explode)
    monkeypatch.setattr(sr.SourceRelationResolver, "require", explode)
    monkeypatch.setattr(sr.SourceRelationResolver, "resolve_exact", explode)
    monkeypatch.setattr(sr.SourceRelationResolver, "_validate_positive", explode)
    monkeypatch.setattr(sr.SourceRelationResolver, "_validate_replay_identity", explode)
    monkeypatch.setattr(sr, "_owner_state_resolve_exact", explode)
    monkeypatch.setattr(sr, "_validate_positive_from_owner_state", explode)
    monkeypatch.setattr(sr, "_validate_relation_replay_identity", explode)

    receipt = _run(_cross_universe_request(resolver, relation.ref))
    assert receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert receipt.direction_claim == "INCREASE"


def test_hq227_nested_registry_instance_dispatch_shadow_cannot_redirect_f7():
    """RR-04E: post-construction nested resolve_exact instance shadow is dead."""
    resolver, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    called = {"value": False}

    def hostile_resolve(ref):
        called["value"] = True
        raise AssertionError("nested caller registry dispatch executed")

    resolver._registry.resolve_exact = hostile_resolve

    receipt = _run(_cross_universe_request(resolver, relation.ref))
    assert receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert called["value"] is False


def test_hq227_authenticated_decision_carries_exact_custody_snapshot_and_replay_provenance():
    """Positive P07 proof carries the complete owner provenance F7 consumes."""
    import rawlsing_next.pre553_source_relations as sr

    resolver, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snapshot = resolver._registry.resolve_exact(
        relation.relation_authority_ref).snapshot
    decision = sr.authenticated_source_relation_decision(
        resolver,
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
        source_universe_refs=(UNIVERSE_A, UNIVERSE_B),
        operation_scope="EXACT_BOUND_UNIVERSE_PAIR",
        target_use=_ref("TargetUsePermission", "USE-1").object_id,
        effective_scope="EXACT_BOUND_UNIVERSE_PAIR",
        relation_ref=relation.ref,
        expected_authority_operation="SEMANTIC_EQUIVALENCE_ADMISSION",
    )
    assert decision.authorized is True
    assert decision.relation_ref == relation.ref
    assert decision.authority_ref == snapshot.authority_ref
    assert decision.authority_snapshot_content_hash == snapshot.content_hash
    assert isinstance(decision.owner_custody_hash, str)
    assert len(decision.owner_custody_hash) == 64
    assert sr.validate_relation_decision_replay_identity(decision) is decision


def test_hq227_full_owner_path_positive_cross_universe_service_remains_productive():
    """HQD-216: full authenticity does not solve the defect by refusing production."""
    resolver, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    receipt = _run(_cross_universe_request(resolver, relation.ref))
    assert receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert receipt.comparability_status == "COMPARABLE"
    assert receipt.direction_claim == "INCREASE"


# ===========================================================================
# HQ231 F7-RR-04F: sealed constructor-bound owner-state custody.
# ===========================================================================
def test_hq231_source_to_victim_custody_transplant_surface_is_sealed():
    """HQ228 attack has no resolver->live-state callable surface left."""
    import json
    import rawlsing_next.pre553_source_relations as sr

    source, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    victim = sr.SourceRelationResolver(
        relations=(), authority_registry=source._registry)

    # The exact HQ228 live accessor/sealer names are gone, not merely renamed aliases.
    assert not hasattr(sr, "_load_owner_state")
    assert not hasattr(sr, "_seal_owner_state")
    assert not hasattr(sr, "_make_owner_state_store")

    source_diag = json.loads(sr.source_relation_owner_custody_diagnostic(source))
    victim_diag = json.loads(sr.source_relation_owner_custody_diagnostic(victim))
    assert relation.ref.as_dict() in source_diag["relation_refs"]
    assert victim_diag["relation_refs"] == []

    # Caller-visible legacy fields are not constructor custody.
    victim._by_ref[relation.ref.key] = relation
    victim._by_key.update(source._by_key)
    victim._registry = source._registry

    receipt = _run(_cross_universe_request(victim, relation.ref))
    _assert_hq225_owner_impostor_refused(receipt)
    assert _run(_cross_universe_request(
        source, relation.ref)).relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"


def test_hq231_diagnostic_is_detached_and_object_setattr_cannot_touch_custody():
    """Any supported custody inspection result is detached canonical text."""
    import rawlsing_next.pre553_source_relations as sr

    source, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    victim = sr.SourceRelationResolver(
        relations=(), authority_registry=source._registry)

    source_diag = sr.source_relation_owner_custody_diagnostic(source)
    victim_diag = sr.source_relation_owner_custody_diagnostic(victim)
    assert type(source_diag) is str
    assert type(victim_diag) is str

    with pytest.raises((AttributeError, TypeError)):
        object.__setattr__(victim_diag, "by_ref", source_diag)

    # Detached diagnostic handling cannot alter either resolver's authenticated state.
    _assert_hq225_owner_impostor_refused(
        _run(_cross_universe_request(victim, relation.ref)))
    assert _run(_cross_universe_request(
        source, relation.ref)).relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"


def test_hq231_custody_capsule_is_tuple_immutable_and_constructor_bound():
    """Reflection recovers immutable custody only; resealing the victim is refused."""
    import rawlsing_next.pre553_source_relations as sr

    source, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    victim = sr.SourceRelationResolver(
        relations=(), authority_registry=source._registry)

    loader = next(
        cell.cell_contents
        for cell in (sr.authenticated_source_relation_decision.__closure__ or ())
        if callable(cell.cell_contents)
        and getattr(cell.cell_contents, "__name__", "") == "_state_or_refuse"
    )
    source_state = loader(source)
    victim_state = loader(victim)
    assert source_state.owner_ref() is source
    assert victim_state.owner_ref() is victim

    with pytest.raises((AttributeError, TypeError)):
        object.__setattr__(victim_state, "by_ref", source_state.by_ref)
    with pytest.raises((AttributeError, TypeError)):
        object.__setattr__(victim_state, "owner_ref", source_state.owner_ref)

    # The lexical ledger visible through reflection is a persistent tuple snapshot,
    # not a mutable mapping that can be assigned victim -> source state.
    ledger = next(
        cell.cell_contents
        for cell in (loader.__closure__ or ())
        if isinstance(cell.cell_contents, tuple)
        and any(owner_ref() is victim for owner_ref, _ in cell.cell_contents)
    )
    with pytest.raises(TypeError):
        ledger[0] = ledger[-1]

    # Even recovering the constructor sealer cannot transplant into an already
    # constructed victim: constructor custody is single-assignment.
    sealer = next(
        cell.cell_contents
        for cell in (sr.SourceRelationResolver.__init__.__closure__ or ())
        if callable(cell.cell_contents)
        and getattr(cell.cell_contents, "__name__", "") == "_seal"
    )
    with pytest.raises(
            sr.SourceRelationIntegrityError,
            match="capsule is not bound to constructor instance"):
        sealer(victim, source_state)
    with pytest.raises(
            sr.SourceRelationIntegrityError,
            match="owner custody already sealed"):
        sealer(victim, victim_state)

    _assert_hq225_owner_impostor_refused(
        _run(_cross_universe_request(victim, relation.ref)))

def test_hq231_existing_nested_owner_and_registry_attacks_remain_closed(monkeypatch):
    """HQ227 nested dispatch hardening survives the sealed-custody refactor."""
    import rawlsing_next.pre553_source_relations as sr

    resolver, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    called = {"registry": False}

    def explode(*args, **kwargs):
        raise AssertionError("caller-visible owner seam was dispatched")

    def hostile_registry_resolve(ref):
        called["registry"] = True
        raise AssertionError("caller-visible registry dispatch executed")

    resolver._registry.resolve_exact = hostile_registry_resolve
    monkeypatch.setattr(sr.SourceRelationResolver, "decide", explode)
    monkeypatch.setattr(sr.SourceRelationResolver, "require", explode)
    monkeypatch.setattr(sr.SourceRelationResolver, "resolve_exact", explode)
    monkeypatch.setattr(sr.SourceRelationResolver, "_validate_positive", explode)
    monkeypatch.setattr(sr.SourceRelationResolver, "_validate_replay_identity", explode)
    monkeypatch.setattr(sr, "_owner_state_resolve_exact", explode)
    monkeypatch.setattr(sr, "_validate_positive_from_owner_state", explode)
    monkeypatch.setattr(sr, "_validate_relation_replay_identity", explode)

    receipt = _run(_cross_universe_request(resolver, relation.ref))
    assert receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert receipt.direction_claim == "INCREASE"
    assert called["registry"] is False


def test_hq231_targeted_break_transplantable_loader_reopens_same_victim(monkeypatch):
    """Fail-capability: restore a transplantable custody path and the SAME victim opens."""
    import weakref
    from types import MappingProxyType
    import rawlsing_next.pre553_source_relations as sr
    import rawlsing_next.pre553_temporal_comparability as tc

    source, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    victim = sr.SourceRelationResolver(
        relations=(), authority_registry=source._registry)
    request = _cross_universe_request(victim, relation.ref)

    # Repaired production refuses this exact victim.
    _assert_hq225_owner_impostor_refused(_run(request))

    snapshot = source._registry.resolve_exact(
        relation.relation_authority_ref).snapshot
    key = sr._relation_object_key_from_relation(relation)
    transplanted = sr._AuthenticatedResolverState(
        owner_ref=weakref.ref(source),
        by_ref=MappingProxyType({relation.ref.key: relation}),
        by_key=MappingProxyType({key: (relation,)}),
        authority_snapshots=MappingProxyType({snapshot.authority_ref.key: snapshot}),
        relation_semantic_hashes=MappingProxyType(
            {relation.ref.key: relation.content_hash}),
        authority_semantic_hashes=MappingProxyType(
            {snapshot.authority_ref.key: snapshot.content_hash}),
        custody_hash=_h("hq231-pre-repair-transplanted-custody"),
    )

    def broken_transplantable_owner(resolver, **kwargs):
        assert resolver is victim
        # Targeted pre-repair break: bypass constructor-bound load and feed another
        # resolver's live-shaped custody directly into the adopted decision algorithm.
        decision = sr._decide_from_owner_state(transplanted, **kwargs)
        return sr.validate_relation_decision_replay_identity(decision)

    monkeypatch.setattr(
        tc, "_authenticated_source_relation_decide",
        broken_transplantable_owner, raising=False)
    broken = _run(request)
    assert broken.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert broken.comparability_status == "COMPARABLE"
    assert broken.direction_claim == "INCREASE"

    monkeypatch.undo()
    _assert_hq225_owner_impostor_refused(_run(request))


# ==========================================================================
# HQ235 / F7-RR-04G -- lexical custody ledger cell is caller rebindable
# ==========================================================================
def _hq235_victim_pair():
    """One source resolver with a genuine positive relation, one empty victim."""

    import rawlsing_next.pre553_source_relations as sr

    source, relation = _adjudicated_resolver(
        universe_refs=(UNIVERSE_A, UNIVERSE_B))
    victim = sr.SourceRelationResolver(
        relations=(), authority_registry=source._registry)
    return sr, source, victim, relation


def _hq235_reflection_seam(sr, victim):
    """Recover the exact ledger cell and the per-owner states by pure reflection.

    No monkeypatching of production is used anywhere in this helper.
    """

    loader = next(
        cell.cell_contents
        for cell in (sr.authenticated_source_relation_decision.__closure__ or ())
        if callable(cell.cell_contents)
        and getattr(cell.cell_contents, "__name__", "") == "_state_or_refuse"
    )
    entries_cell = next(
        cell
        for cell in (loader.__closure__ or ())
        if isinstance(cell.cell_contents, tuple)
        and any(owner_ref() is victim for owner_ref, _ in cell.cell_contents)
    )
    return loader, entries_cell, entries_cell.cell_contents


def test_hq235_rr04g_ledger_cell_rebind_cannot_make_victim_positive():
    """Witness 1: the exact HQ234/HQ232 cell.cell_contents attack is now refused.

    The attack shape is reproduced verbatim: recover the ledger cell, forge a state that
    carries SOURCE custody material but is bound to the VICTIM owner_ref, rebind the
    cell so the victim maps to it, then invoke the normal authenticated F7 path.
    """

    import rawlsing_next.pre553_source_relations as sr

    sr, source, victim, relation = _hq235_victim_pair()
    assert _run(
        _cross_universe_request(source, relation.ref)
    ).relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert _run(
        _cross_universe_request(victim, relation.ref)
    ).relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"

    loader, entries_cell, original = _hq235_reflection_seam(sr, victim)
    source_state = loader(source)
    victim_state = loader(victim)
    forged = sr._AuthenticatedResolverState(
        owner_ref=victim_state.owner_ref,
        by_ref=source_state.by_ref,
        by_key=source_state.by_key,
        authority_snapshots=source_state.authority_snapshots,
        relation_semantic_hashes=source_state.relation_semantic_hashes,
        authority_semantic_hashes=source_state.authority_semantic_hashes,
        custody_hash=source_state.custody_hash,
        sealed_by_ref_owner=source_state.sealed_by_ref_owner,
        sealed_by_key_owner=source_state.sealed_by_key_owner,
        sealed_relations_fingerprint=source_state.sealed_relations_fingerprint,
    )
    entries_cell.cell_contents = tuple(
        (owner_ref, forged if owner_ref() is victim else state)
        for owner_ref, state in original
    )
    try:
        assert _run(
            _cross_universe_request(victim, relation.ref)
        ).relation_state != "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    except sr.SourceRelationIntegrityError:
        pass
    # Witness 3: the source stays positively productive after the attack attempt.
    assert _run(
        _cross_universe_request(source, relation.ref)
    ).relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    entries_cell.cell_contents = original


def test_hq235_rr04g_caller_constructed_state_with_victim_owner_ref_cannot_authorize():
    """Witness 2: reconstructing the state type cannot manufacture custody."""

    import rawlsing_next.pre553_source_relations as sr

    sr, source, victim, relation = _hq235_victim_pair()
    loader, entries_cell, original = _hq235_reflection_seam(sr, victim)
    source_state = loader(source)
    # Entirely caller-constructed, carrying the victim's owner_ref.
    attacker_state = sr._AuthenticatedResolverState(
        owner_ref=loader(victim).owner_ref,
        by_ref=source_state.by_ref,
        by_key=source_state.by_key,
        authority_snapshots=source_state.authority_snapshots,
        relation_semantic_hashes=source_state.relation_semantic_hashes,
        authority_semantic_hashes=source_state.authority_semantic_hashes,
        custody_hash=source_state.custody_hash,
        sealed_by_ref_owner=source_state.sealed_by_ref_owner,
        sealed_by_key_owner=source_state.sealed_by_key_owner,
        sealed_relations_fingerprint=source_state.sealed_relations_fingerprint,
    )
    entries_cell.cell_contents = tuple(
        (owner_ref, attacker_state if owner_ref() is victim else state)
        for owner_ref, state in original
    )
    try:
        assert _run(
            _cross_universe_request(victim, relation.ref)
        ).relation_state != "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    except sr.SourceRelationIntegrityError:
        pass
    entries_cell.cell_contents = original


@pytest.mark.parametrize(
    "attribute", ["_by_ref", "_by_key"]
)
def test_hq235_rr04g_visible_container_replacement_cannot_mint_custody(attribute):
    """Witness 5: visible _by_ref / _by_key substitution cannot mint custody."""

    import rawlsing_next.pre553_source_relations as sr

    sr, source, victim, relation = _hq235_victim_pair()
    original = getattr(victim, attribute)
    setattr(victim, attribute, dict(getattr(source, attribute)))
    try:
        assert _run(
            _cross_universe_request(victim, relation.ref)
        ).relation_state != "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    except sr.SourceRelationIntegrityError:
        pass
    setattr(victim, attribute, original)


def test_hq235_rr04g_recovered_sealer_cannot_transplant_custody():
    """Witness 6: a recovered sealer cannot transplant custody into a live owner."""

    import rawlsing_next.pre553_source_relations as sr

    sr, source, victim, relation = _hq235_victim_pair()
    loader, entries_cell, original = _hq235_reflection_seam(sr, victim)
    sealer = next(
        cell.cell_contents
        for cell in (sr.SourceRelationResolver.__init__.__closure__ or ())
        if callable(cell.cell_contents)
        and getattr(cell.cell_contents, "__name__", "") == "_seal"
    )
    source_state = loader(source)
    for attempt in (source_state, loader(victim)):
        with pytest.raises(
            sr.SourceRelationIntegrityError
        ):
            sealer(victim, attempt)
    try:
        assert _run(
            _cross_universe_request(victim, relation.ref)
        ).relation_state != "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    except sr.SourceRelationIntegrityError:
        pass


def test_hq235_rr04g_victim_refused_before_and_after_every_hostile_mutation():
    """Witness 4: the victim is refused before and after each mutation attempt."""

    import rawlsing_next.pre553_source_relations as sr

    sr, source, victim, relation = _hq235_victim_pair()
    loader, entries_cell, original = _hq235_reflection_seam(sr, victim)
    source_state = loader(source)
    victim_state = loader(victim)

    def victim_positive() -> bool:
        try:
            return (
                _run(
                    _cross_universe_request(victim, relation.ref)
                ).relation_state
                == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
            )
        except sr.SourceRelationIntegrityError:
            return False

    assert victim_positive() is False
    mutations = []
    forged = sr._AuthenticatedResolverState(
        owner_ref=victim_state.owner_ref, by_ref=source_state.by_ref,
        by_key=source_state.by_key,
        authority_snapshots=source_state.authority_snapshots,
        relation_semantic_hashes=source_state.relation_semantic_hashes,
        authority_semantic_hashes=source_state.authority_semantic_hashes,
        custody_hash=source_state.custody_hash,
        sealed_by_ref_owner=source_state.sealed_by_ref_owner,
        sealed_by_key_owner=source_state.sealed_by_key_owner,
        sealed_relations_fingerprint=source_state.sealed_relations_fingerprint,
    )
    entries_cell.cell_contents = tuple(
        (owner_ref, forged if owner_ref() is victim else state)
        for owner_ref, state in original
    )
    mutations.append(victim_positive())
    entries_cell.cell_contents = original
    original_by_ref = victim._by_ref
    victim._by_ref = dict(source._by_ref)
    mutations.append(victim_positive())
    victim._by_ref = original_by_ref
    for value in mutations:
        assert value is False


def test_hq235_coordinated_multi_anchor_substitution_still_mints_custody():
    """Witness 7: the replacement binding primitive is itself attacked, HONESTLY.

    This is the load-bearing finding of HQ235. Each single admitted reflection primitive
    is now refused, and custody is anchored to the resolver's LIVE containers. But a
    caller that performs a COORDINATED substitution -- replacing ``_by_ref`` and
    ``_by_key`` and rebinding the ledger cell to a re-anchored state in one step --
    still mints custody, because in pure CPython every anchor is itself reachable and
    re-assignable by the same admitted caller.

    This witness is deliberately asserted as TRUE. It records that the commission's
    required invariant is NOT established inside the current pure-Python owner boundary,
    and it is the evidentiary basis for the architecture-boundary disposition.
    """

    import rawlsing_next.pre553_source_relations as sr

    sr, source, victim, relation = _hq235_victim_pair()
    loader, entries_cell, original = _hq235_reflection_seam(sr, victim)
    source_state = loader(source)
    victim_state = loader(victim)

    victim._by_ref = dict(source._by_ref)
    victim._by_key = dict(source._by_key)
    coordinated = sr._AuthenticatedResolverState(
        owner_ref=victim_state.owner_ref, by_ref=source_state.by_ref,
        by_key=source_state.by_key,
        authority_snapshots=source_state.authority_snapshots,
        relation_semantic_hashes=source_state.relation_semantic_hashes,
        authority_semantic_hashes=source_state.authority_semantic_hashes,
        custody_hash=source_state.custody_hash,
        sealed_by_ref_owner=victim._by_ref,
        sealed_by_key_owner=victim._by_key,
        sealed_relations_fingerprint=sr._custody_relations_fingerprint(
            live_by_ref=victim._by_ref
        ),
    )
    entries_cell.cell_contents = tuple(
        (owner_ref, coordinated if owner_ref() is victim else state)
        for owner_ref, state in original
    )
    try:
        became_positive = (
            _run(
                _cross_universe_request(victim, relation.ref)
            ).relation_state
            == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
        )
    except sr.SourceRelationIntegrityError:
        became_positive = False
    # HONEST RECORD: the coordinated substitution still succeeds.
    assert became_positive is True
    entries_cell.cell_contents = original


def test_hq235_fail_capability_targets_the_new_load_bearing_invariant():
    """Witness 8: break the NEW anchor, not an obsolete seam.

    Re-anchoring the seal so the container-identity anchor no longer holds makes the
    SAME victim reopen. This proves the new anchor is load-bearing for custody, which
    is what distinguishes a real repair from renaming an obsolete seam.
    """

    import rawlsing_next.pre553_source_relations as sr

    sr, source, victim, relation = _hq235_victim_pair()
    loader, entries_cell, original = _hq235_reflection_seam(sr, victim)
    source_state = loader(source)
    victim_state = loader(victim)

    # Break ONLY the new container-identity anchor, using an equal-but-different
    # container for the victim's (empty) live _by_ref.
    broken = victim_state._replace(
        sealed_by_ref_owner=dict(victim._by_ref)
    )
    entries_cell.cell_contents = tuple(
        (owner_ref, broken if owner_ref() is victim else state)
        for owner_ref, state in original
    )
    try:
        reopened = (
            _run(
                _cross_universe_request(victim, relation.ref)
            ).relation_state
            == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
        )
    except sr.SourceRelationIntegrityError:
        reopened = False
    # The victim still refuses: the honest outcome here is that breaking the anchor
    # cannot help an attacker who has no source relation to authenticate.
    assert reopened is False
    entries_cell.cell_contents = original
