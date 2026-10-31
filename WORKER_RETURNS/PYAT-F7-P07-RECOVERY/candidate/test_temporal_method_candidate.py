from __future__ import annotations

import hashlib
import importlib.util
import pathlib
import sys
from decimal import Decimal

import pytest

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    ExactRef,
    Pre553IntegrityError,
    canonicalize,
)
from rawlsing_next.pre553_source_relations import (
    SourceRelationResolver,
    make_source_universe_relation,
)

_MODULE_PATH = pathlib.Path(__file__).with_name("temporal_method_candidate.py")
_SPEC = importlib.util.spec_from_file_location(
    "pyat_f7_p07_temporal_method_candidate", _MODULE_PATH)
assert _SPEC is not None and _SPEC.loader is not None
CAND = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = CAND
_SPEC.loader.exec_module(CAND)


def _h(tag: str) -> str:
    return hashlib.sha256(tag.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:f7cand:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


GRAIN = _ref("TemporalGrain", "YEAR")
GRAIN_OTHER = _ref("TemporalGrain", "MONTH")
GOVERNED_USE = _ref("TargetUsePermission", "USE-1")
U1 = _ref("SourceUniverse", "U1")
U2 = _ref("SourceUniverse", "U2")
U3 = _ref("SourceUniverse", "U3")
POP1 = _ref("Population", "POP1")
POP2 = _ref("Population", "POP2")
CONSTRUCT1 = _ref("Construct", "C1")
CONSTRUCT2 = _ref("Construct", "C2")
RESPONSE1 = _ref("ResponseSurface", "RSP1")
ROUTE1 = _ref("InstrumentRoute", "ROUTE1")
ROUTE2 = _ref("InstrumentRoute", "ROUTE2")
EST1 = _ref("Estimand", "EST1")
MEASURE1 = _ref("Measure", "MEAS1")
WEIGHT1 = _ref("WeightDesign", "W1")
QUANTITY1 = _ref("Quantity", "Q1")


def _auth(
    tag: str,
    kind: str,
    operation: str,
    *,
    scope_refs=(),
    target_use_value=None,
    source_universe_refs="EXPLICIT_UNRESTRICTED",
    state: str = "ALLOW",
    families=("SourceUniverseRelation@1.0.0", "TemporalComparisonProbe@1.0.0"),
):
    authority_id = f"F7CAND-{tag}"
    content_hash = _h(f"authority:{tag}")
    ref = AuthorityRef(authority_id, "1.0.0", content_hash)
    target_use_refs = (
        (canonicalize(target_use_value),)
        if target_use_value is not None else "EXPLICIT_UNRESTRICTED")
    snapshot = AuthoritySnapshot(
        typed_state=state,
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("ReplayRoot", f"authority-{tag}"),
        authority_id=authority_id,
        authority_version="1.0.0",
        authority_content_hash=content_hash,
        authority_kind=kind,
        decision_state=state,
        governed_operations=(operation,),
        governed_object_families=tuple(families),
        scope_envelope={
            "source_universe_refs": source_universe_refs,
            "target_use_refs": target_use_refs,
            "predicate_or_risk_set_refs": tuple(canonicalize(v) for v in scope_refs),
        },
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"semantics:{tag}"),
        replay_protocol_ref=_ref("ReplayProtocol", "RP1"),
    )
    return ref, snapshot


def _time(tag: str, value, *, grain=GRAIN, state="ALLOW"):
    time_ref = _ref("TemporalTime", tag)
    auth_ref, snapshot = _auth(
        f"time-{tag}",
        CAND.TEMPORAL_EVIDENCE_KIND,
        CAND.TIME_ORDER_OPERATION,
        scope_refs=(time_ref, grain),
        state=state,
    )
    extent = CAND.TimeExtent.point(
        time_ref=time_ref, authority_ref=auth_ref, grain_ref=grain, value=value)
    return extent, snapshot


def _interval_time(tag: str, start, end, *, grain=GRAIN):
    time_ref = _ref("TemporalTime", tag)
    auth_ref, snapshot = _auth(
        f"time-{tag}",
        CAND.TEMPORAL_EVIDENCE_KIND,
        CAND.TIME_ORDER_OPERATION,
        scope_refs=(time_ref, grain),
    )
    extent = CAND.TimeExtent.closed_interval(
        time_ref=time_ref, authority_ref=auth_ref, grain_ref=grain,
        start=start, end=end)
    return extent, snapshot


def _anchor(
    tag: str,
    time_extent,
    *,
    universe=U1,
    population=POP1,
    construct=CONSTRUCT1,
    response_surface=RESPONSE1,
    route=ROUTE1,
    estimand=EST1,
    measure=MEASURE1,
    weight=WEIGHT1,
    quantity=None,
):
    return CAND.TemporalAnchor(
        anchor_ref=_ref("TemporalAnchor", tag),
        observation_ref=_ref("TemporalObservation", tag),
        source_universe_ref=universe,
        construct_ref=construct,
        response_surface_ref=response_surface,
        route_ref=route,
        population_ref=population,
        estimand_ref=estimand,
        measure_ref=measure,
        weight_ref=weight,
        effective_time=time_extent,
        quantity_ref=QUANTITY1 if quantity is not None else None,
        quantity_value=quantity,
    )


_SURFACE_DEFAULTS = {
    "construct_question_semantics": ("COORDINATE_SEMANTICS", "F7_CONSTRUCT_QUESTION_COMPARABILITY"),
    "response_surface_and_scale": ("SOURCE_SEMANTICS_TOPOLOGY", "F7_RESPONSE_SURFACE_COMPARABILITY"),
    "instrument_release_and_route": ("ROUTING_RISK_SET", "F7_ROUTE_COMPARABILITY"),
    "target_population_and_geography": ("ROUTING_RISK_SET", "F7_POPULATION_COMPARABILITY"),
    "estimand": ("WEIGHT_DESIGN_ESTIMAND", "F7_ESTIMAND_COMPARABILITY"),
    "measure": ("WEIGHT_DESIGN_ESTIMAND", "F7_MEASURE_COMPARABILITY"),
    "weight_design": ("WEIGHT_DESIGN_ESTIMAND", "F7_WEIGHT_COMPARABILITY"),
    "time_representation_and_grain": ("TEMPORAL_EVIDENCE", CAND.TIME_ORDER_OPERATION),
}


def _surface_ref(anchor, surface: str) -> ExactRef:
    if surface == "construct_question_semantics":
        return anchor.construct_ref
    if surface == "response_surface_and_scale":
        return anchor.response_surface_ref
    if surface == "instrument_release_and_route":
        return anchor.route_ref
    if surface == "target_population_and_geography":
        return anchor.population_ref
    if surface == "estimand":
        return anchor.estimand_ref
    if surface == "measure":
        return anchor.measure_ref
    if surface == "weight_design":
        return anchor.weight_ref
    if surface == "time_representation_and_grain":
        return anchor.effective_time.time_ref
    raise AssertionError(surface)


def _attestation(
    surface: str,
    left_ref: ExactRef,
    right_ref: ExactRef,
    *,
    state: str = "SATISFIED",
    kind: str | None = None,
    operation: str | None = None,
    authority_state: str = "ALLOW",
):
    default_kind, default_operation = _SURFACE_DEFAULTS[surface]
    authority_ref, snapshot = _auth(
        f"att-{surface}-{_h(left_ref.key + right_ref.key)[:10]}",
        kind or default_kind,
        operation or default_operation,
        scope_refs=(left_ref, right_ref),
        target_use_value=GOVERNED_USE.as_dict(),
        state=authority_state,
    )
    attestation = CAND.ComparabilityAttestation(
        surface=surface,
        left_ref=left_ref,
        right_ref=right_ref,
        authority_ref=authority_ref,
        authority_kind=kind or default_kind,
        operation=operation or default_operation,
        state=state,
    )
    return attestation, snapshot


def _profile(
    left,
    right,
    *,
    skip=(),
    state_overrides=None,
    kind_overrides=None,
    authority_state_overrides=None,
    source_equivalence=None,
):
    state_overrides = state_overrides or {}
    kind_overrides = kind_overrides or {}
    authority_state_overrides = authority_state_overrides or {}
    attestations = []
    snapshots = []
    for surface in CAND.CANDIDATE_MINIMUM_SURFACES:
        if surface in skip:
            continue
        left_ref = _surface_ref(left, surface)
        right_ref = _surface_ref(right, surface)
        attestation, snapshot = _attestation(
            surface,
            left_ref,
            right_ref,
            state=state_overrides.get(surface, "SATISFIED"),
            kind=kind_overrides.get(surface),
            authority_state=authority_state_overrides.get(surface, "ALLOW"),
        )
        attestations.append(attestation)
        snapshots.append(snapshot)
    return CAND.TemporalComparabilityProfile(
        governed_use_ref=GOVERNED_USE,
        required_surfaces=CAND.CANDIDATE_MINIMUM_SURFACES,
        attestations=tuple(attestations),
        source_equivalence=source_equivalence,
    ), snapshots


def _equivalence(
    left,
    right,
    *,
    universes=None,
    decision="AUTHORIZED",
    relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
    tag="eq",
    target_use=None,
):
    op = CAND.SOURCE_EQUIVALENCE_OPERATION
    scope = CAND.SOURCE_EQUIVALENCE_SCOPE
    target_use = GOVERNED_USE.object_id if target_use is None else target_use
    pair = universes or (left.source_universe_ref, right.source_universe_ref)
    authority_ref, snapshot = _auth(
        f"equivalence-{tag}",
        "SOURCE_EQUIVALENCE",
        op,
        scope_refs=(scope,),
        target_use_value=target_use,
        source_universe_refs=tuple(canonicalize(ref) for ref in pair),
    )
    material = {
        "left_semantic_ref": _ref("SemanticFingerprint", f"{tag}-left"),
        "right_semantic_ref": _ref("SemanticFingerprint", f"{tag}-right"),
        "equivalence_scope": scope,
        "transformation_authority_refs": (_ref("SemanticTransformation", tag),),
    }
    if relation_kind == "HARMONIZATION_ALIAS":
        material = {"alias_refs": (_ref("Alias", tag),)}
    relation = make_source_universe_relation(
        relation_kind=relation_kind,
        source_universe_refs=pair,
        authority_snapshot=snapshot,
        authority_operation=op,
        operation_scope=scope,
        target_use=target_use,
        effective_scope=scope,
        directionality_or_symmetric="SYMMETRIC",
        operation_authority_material=material,
        producer_replay_locator_or_reference_root=_ref("ReplayRoot", f"relation-{tag}"),
        decision=decision,
    )
    resolver = SourceRelationResolver(
        relations=(relation,), authority_registry=AuthorityRegistry((snapshot,)))
    evidence = CAND.SourceEquivalenceEvidence(
        resolver=resolver,
        relation_ref=relation.ref,
        operation_scope=scope,
        effective_scope=scope,
        target_use=target_use,
    )
    return evidence, snapshot


def _compare(left, right, profile, snapshots):
    return CAND.compare_temporal_method(
        left, right, profile=profile,
        registry=AuthorityRegistry(tuple(snapshots)))


def test_positive_strict_order_delta_and_replay():
    left_time, left_time_auth = _time("left", 10)
    right_time, right_time_auth = _time("right", 15)
    left = _anchor("left", left_time, quantity=10)
    right = _anchor("right", right_time, quantity=15)
    profile, snapshots = _profile(left, right)
    decision = _compare(left, right, profile, snapshots + [left_time_auth, right_time_auth])
    assert decision.comparability_status == "COMPARABLE"
    assert decision.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert decision.direction_claim == "INCREASE"
    assert decision.delta["signed_delta"] == {"$exact_fraction": [5, 1]}
    assert decision.receipt_hash == decision.replay_identity()
    assert _compare(left, right, profile, snapshots + [left_time_auth, right_time_auth]) == decision


def test_same_numeric_value_without_construct_attestation_is_not_comparable():
    left_time, left_time_auth = _time("left", 10)
    right_time, right_time_auth = _time("right", 10)
    left = _anchor("left", left_time, quantity=10)
    right = _anchor("right", right_time, quantity=10)
    profile, snapshots = _profile(left, right, skip=("construct_question_semantics",))
    decision = _compare(left, right, profile, snapshots + [left_time_auth, right_time_auth])
    assert decision.comparability_status == "NOT_COMPARABLE"
    assert decision.relation_state == "TEMPORAL_NONCOMPARABLE"
    assert "COMPARABILITY_ATTESTATION_ABSENT:construct_question_semantics" in decision.reasons
    assert decision.delta is None
    assert decision.direction_claim == "DIRECTION_NOT_CLAIMABLE"
    with pytest.raises(CAND.CandidateTemporalNotComparable):
        CAND.require_comparable(decision)


def test_equal_numbers_do_not_imply_comparability_when_surface_is_not_satisfied():
    left_time, left_time_auth = _time("left", 10)
    right_time, right_time_auth = _time("right", 10)
    left = _anchor("left", left_time, quantity=10)
    right = _anchor("right", right_time, quantity=10)
    profile, snapshots = _profile(
        left, right,
        state_overrides={"construct_question_semantics": "NOT_SATISFIED"})
    decision = _compare(left, right, profile, snapshots + [left_time_auth, right_time_auth])
    assert decision.comparability_status == "NOT_COMPARABLE"
    assert "SURFACE_NOT_SATISFIED:construct_question_semantics" in decision.reasons
    assert decision.delta is None


def test_as_of_timestamp_without_time_attestation_is_not_comparability():
    left_time, left_time_auth = _time("left", 10)
    right_time, right_time_auth = _time("right", 10)
    left = _anchor("left", left_time, quantity=10)
    right = _anchor("right", right_time, quantity=10)
    profile, snapshots = _profile(left, right, skip=("time_representation_and_grain",))
    decision = _compare(left, right, profile, snapshots + [left_time_auth, right_time_auth])
    assert decision.comparability_status == "NOT_COMPARABLE"
    assert "COMPARABILITY_ATTESTATION_ABSENT:time_representation_and_grain" in decision.reasons
    assert decision.delta is None


def test_route_attestation_bound_to_wrong_refs_is_refused():
    left_time, left_time_auth = _time("left", 10)
    right_time, right_time_auth = _time("right", 10)
    left = _anchor("left", left_time)
    right = _anchor("right", right_time)
    profile, snapshots = _profile(left, right)
    bad = CAND.ComparabilityAttestation(
        surface="instrument_release_and_route",
        left_ref=left.construct_ref,
        right_ref=right.construct_ref,
        authority_ref=profile.attestations[2].authority_ref,
        authority_kind=profile.attestations[2].authority_kind,
        operation=profile.attestations[2].operation,
        state="SATISFIED",
    )
    attestations = tuple(
        bad if a.surface == "instrument_release_and_route" else a
        for a in profile.attestations
    )
    bad_profile = CAND.TemporalComparabilityProfile(
        governed_use_ref=GOVERNED_USE,
        required_surfaces=CAND.CANDIDATE_MINIMUM_SURFACES,
        attestations=attestations,
    )
    decision = _compare(left, right, bad_profile, snapshots + [left_time_auth, right_time_auth])
    assert decision.comparability_status == "NOT_COMPARABLE"
    assert "ATTESTATION_BINDING_MISMATCH:instrument_release_and_route" in decision.reasons


def test_cross_population_comparison_is_refused_even_with_equivalence_and_equal_numbers():
    left_time, left_time_auth = _time("left", 10)
    right_time, right_time_auth = _time("right", 10)
    left = _anchor("left", left_time, universe=U1, population=POP1, quantity=10)
    right = _anchor("right", right_time, universe=U2, population=POP2, quantity=10)
    evidence, evidence_auth = _equivalence(left, right)
    profile, snapshots = _profile(left, right, source_equivalence=evidence)
    decision = _compare(
        left, right, profile,
        snapshots + [left_time_auth, right_time_auth, evidence_auth])
    assert decision.comparability_status == "NOT_COMPARABLE"
    assert "POPULATION_NOT_SHARED" in decision.reasons
    assert decision.delta is None


def test_positive_cross_universe_uses_present_outer_source_relation_resolver():
    left_time, left_time_auth = _time("left", 10)
    right_time, right_time_auth = _time("right", 15)
    left = _anchor("left", left_time, universe=U1, quantity=10)
    right = _anchor("right", right_time, universe=U2, quantity=15)
    evidence, evidence_auth = _equivalence(left, right)
    profile, snapshots = _profile(left, right, source_equivalence=evidence)
    decision = _compare(
        left, right, profile,
        snapshots + [left_time_auth, right_time_auth, evidence_auth])
    assert decision.comparability_status == "COMPARABLE"
    assert decision.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    assert decision.source_equivalence_ref is not None


def test_denied_source_relation_cannot_admit_cross_universe_pair():
    left_time, left_time_auth = _time("left", 10)
    right_time, right_time_auth = _time("right", 15)
    left = _anchor("left", left_time, universe=U1, quantity=10)
    right = _anchor("right", right_time, universe=U2, quantity=15)
    evidence, evidence_auth = _equivalence(left, right, decision="DENIED", tag="denied")
    profile, snapshots = _profile(left, right, source_equivalence=evidence)
    decision = _compare(
        left, right, profile,
        snapshots + [left_time_auth, right_time_auth, evidence_auth])
    assert decision.comparability_status == "NOT_COMPARABLE"
    assert any(reason.startswith("CROSS_UNIVERSE_EQUIVALENCE_REFUSED")
               for reason in decision.reasons)
    assert decision.delta is None


def test_alias_relation_cannot_replace_source_equivalence():
    left_time, left_time_auth = _time("left", 10)
    right_time, right_time_auth = _time("right", 15)
    left = _anchor("left", left_time, universe=U1, quantity=10)
    right = _anchor("right", right_time, universe=U2, quantity=15)
    evidence, evidence_auth = _equivalence(
        left, right, decision="DENIED", relation_kind="HARMONIZATION_ALIAS", tag="alias")
    profile, snapshots = _profile(left, right, source_equivalence=evidence)
    decision = _compare(
        left, right, profile,
        snapshots + [left_time_auth, right_time_auth, evidence_auth])
    assert decision.comparability_status == "NOT_COMPARABLE"
    assert any(reason.startswith("CROSS_UNIVERSE_EQUIVALENCE_REFUSED")
               for reason in decision.reasons)


def test_duck_typed_owner_and_resolver_subclass_are_refused():
    class _FakeResolver:
        def require(self, **kwargs):
            return object()

    class _SubclassResolver(SourceRelationResolver):
        pass

    with pytest.raises(CAND.CandidateTemporalIntegrityError):
        CAND.SourceEquivalenceEvidence(
            resolver=_FakeResolver(),
            relation_ref=_ref("SourceUniverseRelation", "fake"),
            operation_scope=CAND.SOURCE_EQUIVALENCE_SCOPE,
            effective_scope=CAND.SOURCE_EQUIVALENCE_SCOPE,
            target_use=GOVERNED_USE.object_id,
        )
    subclass = _SubclassResolver(
        relations=(), authority_registry=AuthorityRegistry(()))
    with pytest.raises(CAND.CandidateTemporalIntegrityError):
        CAND.SourceEquivalenceEvidence(
            resolver=subclass,
            relation_ref=_ref("SourceUniverseRelation", "subclass"),
            operation_scope=CAND.SOURCE_EQUIVALENCE_SCOPE,
            effective_scope=CAND.SOURCE_EQUIVALENCE_SCOPE,
            target_use=GOVERNED_USE.object_id,
        )


def test_historical_temporal_comparability_kind_is_not_a_current_authority():
    left_time, left_time_auth = _time("left", 10)
    right_time, right_time_auth = _time("right", 10)
    left = _anchor("left", left_time)
    right = _anchor("right", right_time)
    profile, snapshots = _profile(
        left, right,
        skip=("construct_question_semantics",))
    kind = "TEMPORAL_COMPARABILITY"
    dummy_ref = AuthorityRef(
        "F7CAND-historical-kind", "1.0.0", _h("historical-kind"))
    bad_attestation = CAND.ComparabilityAttestation(
        surface="construct_question_semantics",
        left_ref=left.construct_ref,
        right_ref=right.construct_ref,
        authority_ref=dummy_ref,
        authority_kind=kind,
        operation="TEMPORAL_BOUND_QUANTITY_DIFFERENCE",
        state="SATISFIED",
    )
    bad_profile = CAND.TemporalComparabilityProfile(
        governed_use_ref=GOVERNED_USE,
        required_surfaces=CAND.CANDIDATE_MINIMUM_SURFACES,
        attestations=profile.attestations + (bad_attestation,),
    )
    decision = _compare(
        left, right, bad_profile, snapshots + [left_time_auth, right_time_auth])
    assert decision.comparability_status == "NOT_COMPARABLE"
    assert "AUTHORITY_KIND_NOT_CURRENT:construct_question_semantics" in decision.reasons


def test_denied_temporal_evidence_authority_is_insufficient_authority():
    left_time, left_time_auth = _time("left", 10, state="DENY")
    right_time, right_time_auth = _time("right", 15)
    left = _anchor("left", left_time)
    right = _anchor("right", right_time)
    profile, snapshots = _profile(left, right)
    decision = _compare(
        left, right, profile, snapshots + [left_time_auth, right_time_auth])
    assert decision.comparability_status == "NOT_COMPARABLE"
    assert decision.relation_state == "TEMPORAL_INSUFFICIENT_AUTHORITY"
    assert "left:AUTHORITY_NOT_POSITIVE" in decision.reasons


def test_grain_mismatch_is_refused_without_coercion():
    left_time, left_time_auth = _time("left", 10, grain=GRAIN)
    right_time, right_time_auth = _time("right", 15, grain=GRAIN_OTHER)
    left = _anchor("left", left_time, quantity=10)
    right = _anchor("right", right_time, quantity=15)
    profile, snapshots = _profile(left, right)
    decision = _compare(left, right, profile, snapshots + [left_time_auth, right_time_auth])
    assert decision.comparability_status == "NOT_COMPARABLE"
    assert "TEMPORAL_GEOMETRY_GRAIN_MISMATCH" in decision.reasons
    assert decision.delta is None


def test_interval_overlap_never_becomes_midpoint_or_direction():
    left_time, left_time_auth = _interval_time("left", 0, 10)
    right_time, right_time_auth = _interval_time("right", 5, 15)
    left = _anchor("left", left_time, quantity=10)
    right = _anchor("right", right_time, quantity=15)
    profile, snapshots = _profile(left, right)
    decision = _compare(left, right, profile, snapshots + [left_time_auth, right_time_auth])
    assert decision.comparability_status == "COMPARABLE"
    assert decision.relation_state == "TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION"
    assert decision.direction_claim == "DIRECTION_NOT_CLAIMABLE"
    assert decision.delta is None


def test_float_nan_bool_and_string_are_refused_as_exact_inputs():
    time_ref = _ref("TemporalTime", "bad")
    auth_ref, _ = _auth(
        "bad-time",
        CAND.TEMPORAL_EVIDENCE_KIND,
        CAND.TIME_ORDER_OPERATION,
        scope_refs=(time_ref, GRAIN),
    )
    for bad in (1.5, Decimal("NaN"), True, "1"):
        with pytest.raises(CAND.CandidateTemporalIntegrityError):
            CAND.TimeExtent.point(
                time_ref=time_ref,
                authority_ref=auth_ref,
                grain_ref=GRAIN,
                value=bad,
            )


def test_as_of_selection_excludes_future_publication_and_does_not_pick_latest():
    as_of_time, as_of_auth = _time("asof", 2022)
    early_time, early_auth = _time("published-2020", 2020)
    late_time, late_auth = _time("published-2025", 2025)
    early = CAND.AsOfVersion(
        version_ref=_ref("Version", "v2020"), published=early_time)
    late = CAND.AsOfVersion(
        version_ref=_ref("Version", "v2025"), published=late_time)
    selection = CAND.select_as_of_version(
        (early, late),
        as_of=as_of_time,
        registry=AuthorityRegistry((as_of_auth, early_auth, late_auth)),
    )
    assert selection.state == "SELECTED"
    assert selection.selected_ref == early.version_ref.as_dict()
    assert selection.future_excluded_refs == (late.version_ref.as_dict(),)


def test_as_of_revoked_version_is_excluded():
    as_of_time, as_of_auth = _time("asof", 2022)
    published_time, published_auth = _time("published-2020", 2020)
    revoked_time, revoked_auth = _time("revoked-2021", 2021)
    version = CAND.AsOfVersion(
        version_ref=_ref("Version", "revoked"),
        published=published_time,
        revoked=revoked_time,
    )
    selection = CAND.select_as_of_version(
        (version,),
        as_of=as_of_time,
        registry=AuthorityRegistry((as_of_auth, published_auth, revoked_auth)),
    )
    assert selection.state == "NO_ELIGIBLE_VERSION"
    assert selection.selected_ref is None
    assert selection.revoked_excluded_refs == (version.version_ref.as_dict(),)


def test_as_of_ambiguity_refuses_latest_selection():
    as_of_time, as_of_auth = _time("asof", 2022)
    first_time, first_auth = _time("published-2020", 2020)
    second_time, second_auth = _time("published-2021", 2021)
    first = CAND.AsOfVersion(
        version_ref=_ref("Version", "v1"), published=first_time)
    second = CAND.AsOfVersion(
        version_ref=_ref("Version", "v2"), published=second_time)
    selection = CAND.select_as_of_version(
        (first, second),
        as_of=as_of_time,
        registry=AuthorityRegistry((as_of_auth, first_auth, second_auth)),
    )
    assert selection.state == "AMBIGUOUS_AS_OF_SELECTION"
    assert selection.selected_ref is None
    assert selection.eligible_refs == (
        first.version_ref.as_dict(), second.version_ref.as_dict())


def test_as_of_future_valid_from_is_not_yet_valid():
    as_of_time, as_of_auth = _time("asof", 2022)
    published_time, published_auth = _time("published-2020", 2020)
    valid_time, valid_auth = _time("valid-2024", 2024)
    version = CAND.AsOfVersion(
        version_ref=_ref("Version", "future-valid"),
        published=published_time,
        valid_from=valid_time,
    )
    selection = CAND.select_as_of_version(
        (version,),
        as_of=as_of_time,
        registry=AuthorityRegistry((as_of_auth, published_auth, valid_auth)),
    )
    assert selection.state == "NO_ELIGIBLE_VERSION"
    assert selection.not_yet_valid_refs == (version.version_ref.as_dict(),)


def test_fault_restore_matrix_named_reasons_red_then_green():
    left_time, left_time_auth = _time("left", 10)
    right_time, right_time_auth = _time("right", 15)
    left = _anchor("left", left_time, quantity=10)
    right = _anchor("right", right_time, quantity=15)

    baseline_profile, baseline_snapshots = _profile(left, right)
    baseline = _compare(
        left, right, baseline_profile,
        baseline_snapshots + [left_time_auth, right_time_auth])
    assert baseline.comparability_status == "COMPARABLE"

    mutations = (
        ("construct_question_semantics", "COMPARABILITY_ATTESTATION_ABSENT"),
        ("response_surface_and_scale", "COMPARABILITY_ATTESTATION_ABSENT"),
        ("instrument_release_and_route", "COMPARABILITY_ATTESTATION_ABSENT"),
        ("target_population_and_geography", "COMPARABILITY_ATTESTATION_ABSENT"),
        ("estimand", "COMPARABILITY_ATTESTATION_ABSENT"),
        ("measure", "COMPARABILITY_ATTESTATION_ABSENT"),
        ("weight_design", "COMPARABILITY_ATTESTATION_ABSENT"),
        ("time_representation_and_grain", "COMPARABILITY_ATTESTATION_ABSENT"),
    )
    for surface, reason_prefix in mutations:
        profile, snapshots = _profile(left, right, skip=(surface,))
        decision = _compare(
            left, right, profile,
            snapshots + [left_time_auth, right_time_auth])
        assert decision.comparability_status == "NOT_COMPARABLE"
        assert any(reason.startswith(reason_prefix) and surface in reason
                   for reason in decision.reasons)
        restored = _compare(
            left, right, baseline_profile,
            baseline_snapshots + [left_time_auth, right_time_auth])
        assert restored.comparability_status == "COMPARABLE"


def test_absent_current_source_relation_producer_is_an_explicit_gap():
    left_time, left_time_auth = _time("left", 10)
    right_time, right_time_auth = _time("right", 10)
    left = _anchor("left", left_time, universe=U1, quantity=10)
    right = _anchor("right", right_time, universe=U2, quantity=10)
    profile, snapshots = _profile(left, right)
    decision = _compare(
        left, right, profile,
        snapshots + [left_time_auth, right_time_auth])
    assert decision.comparability_status == "NOT_COMPARABLE"
    assert decision.relation_state == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT"
    assert "CROSS_UNIVERSE_EQUIVALENCE_ABSENT" in decision.reasons
    assert decision.delta is None


def test_source_relation_for_a_different_universe_pair_is_refused():
    left_time, left_time_auth = _time("left", 10)
    right_time, right_time_auth = _time("right", 15)
    left = _anchor("left", left_time, universe=U1, quantity=10)
    right = _anchor("right", right_time, universe=U2, quantity=15)
    evidence, evidence_auth = _equivalence(
        left, right, universes=(U1, U3), tag="wrong-pair")
    profile, snapshots = _profile(left, right, source_equivalence=evidence)
    decision = _compare(
        left, right, profile,
        snapshots + [left_time_auth, right_time_auth, evidence_auth])
    assert decision.comparability_status == "NOT_COMPARABLE"
    assert any(reason.startswith("CROSS_UNIVERSE_EQUIVALENCE_REFUSED")
               for reason in decision.reasons)


def test_source_equivalence_for_a_different_governed_use_is_refused():
    left_time, left_time_auth = _time("left", 10)
    right_time, right_time_auth = _time("right", 15)
    left = _anchor("left", left_time, universe=U1, quantity=10)
    right = _anchor("right", right_time, universe=U2, quantity=15)
    evidence, evidence_auth = _equivalence(
        left, right, tag="other-use", target_use="OTHER-USE")
    profile, snapshots = _profile(left, right, source_equivalence=evidence)
    decision = _compare(
        left, right, profile,
        snapshots + [left_time_auth, right_time_auth, evidence_auth])
    assert decision.comparability_status == "NOT_COMPARABLE"
    assert "CROSS_UNIVERSE_EQUIVALENCE_USE_MISMATCH" in decision.reasons
    assert decision.delta is None


def test_as_of_grain_mismatch_is_refused():
    as_of_time, as_of_auth = _time("asof", 2022)
    published_time, published_auth = _time(
        "published-2020-month", 2020, grain=GRAIN_OTHER)
    version = CAND.AsOfVersion(
        version_ref=_ref("Version", "wrong-grain"),
        published=published_time,
    )
    with pytest.raises(CAND.CandidateTemporalIntegrityError):
        CAND.select_as_of_version(
            (version,),
            as_of=as_of_time,
            registry=AuthorityRegistry((as_of_auth, published_auth)),
        )
