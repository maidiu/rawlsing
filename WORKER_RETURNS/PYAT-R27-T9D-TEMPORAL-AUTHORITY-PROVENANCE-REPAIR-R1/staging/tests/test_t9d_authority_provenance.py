"""PYAT R27 T9D — own repair checks for the remaining independent failures.

These are the productive adapter author's own counterexample/positive pairs for
the T9R post-inspection attacks and the four unavailable capability gates. They
are deliberately NOT the independent court: the frozen T9I suite, the frozen T9R
delta and the frozen T9R post-inspection hostiles run separately and unchanged.
"""
from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

import pytest

RET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RET / "pinned_candidate"))
sys.path.insert(0, str(RET / "pinned_candidate" / "native"))

import t9b_temporal as T  # noqa: E402

C = "SYNTH_COUNTRY_A"


def wave(name, year, value, **kw):
    args = dict(wave_id=name, source_family="SYNTH_FAMILY", country=C,
                instrument="SYNTH_INSTRUMENT", edition="E1", cohort="COHORT_ALL",
                observation_year=year, published_year=year, value=value)
    args.update(kw)
    return T.Wave(**args)


def case(waves=None, **kw):
    args = dict(case_id="T9D", country=C,
                waves=tuple(waves if waves is not None
                            else [wave("W0", 1990, .20), wave("W1", 2000, .60)]),
                target_year=1995)
    args.update(kw)
    return T.TemporalCase(**args)


WORLD = T.StructuralWorld(
    "W_SYNTH_INSTITUTION",
    ("ROUTE_REDUCED_BURDEN", "ROUTE_PARTICIPATION", "ROUTE_DEFERRED_REVIEW"),
    ("GRANT_YOUNG_PERSON_ACCESS",), "SYNTH_INSTITUTION")


def no_open_routes(x):
    return not [r for r in x.opportunity_ids if r != "ROUTE_BLOCKED_NO_SUPPORT"]


# ============================================== T9D-1 unused future authority
def test_t9d1_unused_future_wave_cannot_upgrade_held_product_authority():
    old = wave("W0", 1990, .2)
    future = wave("W1", 2000, .6)
    before = T.read_selected_world(WORLD, case([old]), T.METHOD_M0_HOLD, 1995,
                                   retrospective=True)
    after = T.read_selected_world(WORLD, case([old, future]), T.METHOD_M0_HOLD, 1995,
                                  retrospective=True)
    assert before.basis_wave_ids == after.basis_wave_ids == ("W0",)
    assert before.temporal_key == after.temporal_key == T.PROBE_ONLY_TEMPORAL_KEY
    assert not before.authorized_opportunity and not after.authorized_opportunity
    assert no_open_routes(before) and no_open_routes(after)
    assert before.opportunity_ids == after.opportunity_ids


def test_t9d1_held_estimate_is_typed_not_an_observation():
    out = T.evaluate(case(), T.METHOD_M0_HOLD, clock_year=1995, retrospective=True)
    assert out.product_observation_status == T.PRODUCT_HELD_NOT_AT_CLOCK
    interp = T.evaluate(case(), T.METHOD_M1_INTERP, clock_year=1995, retrospective=True)
    assert interp.product_observation_status == T.PRODUCT_INTERPOLATED
    obs = T.evaluate(case(), T.METHOD_M0_HOLD, clock_year=2000, retrospective=True)
    assert obs.product_observation_status == T.PRODUCT_OBSERVED_AT_CLOCK


def test_t9d1_observation_at_clock_still_authorizes_its_own_year():
    out = T.read_selected_world(WORLD, case(), T.METHOD_M0_HOLD, 2000, retrospective=True)
    assert out.product_observation_status == T.PRODUCT_OBSERVED_AT_CLOCK
    assert out.temporal_key == T.AUTHORIZED_SPARSE_TEMPORAL_KEY
    assert out.authorized_opportunity is True
    assert "ROUTE_PARTICIPATION" in out.opportunity_ids


def test_t9d1_as_of_and_retrospective_estimates_stay_historically_honest():
    asof = T.evaluate(case(), T.METHOD_M1_INTERP, clock_year=1995, retrospective=False)
    retro = T.evaluate(case(), T.METHOD_M1_INTERP, clock_year=1995, retrospective=True)
    assert asof.value == pytest.approx(.20)
    assert retro.value == pytest.approx(.40)
    assert "INTERPOLATED_NOT_OBSERVED" in retro.uncertainty
    for clock, expect in ((1990, .20), (2000, .60)):
        assert T.evaluate(case(), T.METHOD_M1_INTERP, clock_year=clock,
                          retrospective=True).value == pytest.approx(expect)


# ============================================== T9D-2 actor entitlement
@pytest.mark.parametrize("method", [T.METHOD_M0_HOLD, T.METHOD_M1_INTERP,
                                    T.METHOD_M2_BACKOFF])
def test_t9d2_empty_actor_grants_open_no_route_even_with_two_anchors(method):
    c = case([wave("OLD", 1980, .2), wave("RECENT", 1990, .6)])
    empty = T.StructuralWorld(WORLD.world_id, WORLD.structural_routes, (),
                              WORLD.institution)
    x = T.read_selected_world(empty, c, method, 1995)
    assert not x.authorized_opportunity
    assert no_open_routes(x)
    assert x.actor_opportunity_entitlement == T.ENTITLEMENT_WITHHELD


def test_t9d2_present_current_grant_restores_the_entitled_route():
    x = T.read_selected_world(WORLD, case(), T.METHOD_M0_HOLD, 2000, retrospective=True)
    assert x.actor_opportunity_entitlement == T.ENTITLEMENT_GRANTED
    assert x.authorized_opportunity is True


def test_t9d2_native_temporal_grant_and_actor_entitlement_are_distinct_fields():
    empty = T.StructuralWorld(WORLD.world_id, WORLD.structural_routes, (),
                              WORLD.institution)
    x = T.read_selected_world(empty, case(), T.METHOD_M0_HOLD, 2000, retrospective=True)
    # source-side native multi-wave grant is disclosed separately from entitlement
    assert x.provenance["native_multi_wave_authorization_status"] == \
        T.AUTHORIZED_SPARSE_TEMPORAL_KEY
    assert x.actor_opportunity_entitlement == T.ENTITLEMENT_WITHHELD
    assert x.provenance["actor_opportunity_entitlement"] == T.ENTITLEMENT_WITHHELD
    assert not x.authorized_opportunity and no_open_routes(x)


# ============================================== T9D-3 lag/rupture identity
def test_t9d3_lag_parser_does_not_swallow_rupture_qualifiers():
    c = case([wave("DELAYED", 1990, .8, published_year=2000)], ruptures=(1995,))
    x = T.evaluate(c, T.METHOD_M0_HOLD, clock_year=1997, retrospective=True)
    assert set(T.pub_lag_of(x)) <= set(x.basis_wave_ids)
    assert T.pub_lag_of(x) == ("DELAYED",)
    assert x.rupture_crossed_year == 1995
    assert x.rupture_qualified is True
    assert "POST_RUPTURE_CARRY_HYPOTHETICAL:R1995" in x.uncertainty


def test_t9d3_typed_basis_lag_and_archive_context_are_separate():
    out = T.evaluate(case(), T.METHOD_M0_HOLD, clock_year=1995, retrospective=True)
    assert out.publication_lag_wave_ids == ()
    assert out.basis_wave_ids == ("W0",)
    assert out.archive_context_wave_ids == ("W1",)
    assert set(T.pub_lag_of(out)) <= set(out.basis_wave_ids)


# ============================================== T9D-4 duplicate wave identity
def test_t9d4_duplicate_wave_id_is_refused_before_source_filtering():
    c = case([wave("DUPLICATE", 1990, .6),
              wave("DUPLICATE", 1980, .1, country="OTHER",
                   source_family="WRONG_SOURCE", edition="WRONG_EDITION")])
    x = T.read_selected_world(WORLD, c, T.METHOD_M0_HOLD, 1995)
    assert x.refused_code == T.REFUSED_DUPLICATE_WAVE_ID
    assert no_open_routes(x)
    assert x.opportunity_ids == ("ROUTE_BLOCKED_NO_SUPPORT",)


def test_t9d4_basis_provenance_binds_to_selected_objects_not_last_wins():
    wrong = wave("EXCLUDED", 1980, .1, country="OTHER",
                 source_family="WRONG_SOURCE", edition="WRONG_EDITION")
    valid = wave("VALID", 1990, .6, source_family="ACTUAL_SOURCE", edition="ACTUAL_EDITION")
    x = T.read_selected_world(WORLD, case([wrong, valid]), T.METHOD_M0_HOLD, 1995)
    assert x.basis_wave_ids == ("VALID",)
    assert x.provenance["source_family"] == "ACTUAL_SOURCE"
    assert x.provenance["edition"] == "ACTUAL_EDITION"
    assert x.provenance["basis_source_refs"] == [["ACTUAL_SOURCE", "ACTUAL_EDITION"]]


# ============================================== T9D-5 archival / source grant
def test_t9d5_archival_known_at_bound_excludes_future_publication():
    w = wave("FUTURE_PUBLICATION", 1990, .8, published_year=2030)
    out = T.evaluate(case([w]), T.METHOD_M0_HOLD, clock_year=1995, retrospective=True,
                     archival_known_at_upper_year=2020)
    assert out.value is None
    assert out.refused_code == T.REFUSED_ARCHIVAL_NOT_KNOWN_AT
    assert "FUTURE_PUBLICATION" not in out.basis_wave_ids
    open_bound = T.evaluate(case([w]), T.METHOD_M0_HOLD, clock_year=1995,
                            retrospective=True, archival_known_at_upper_year=2035)
    assert open_bound.value == pytest.approx(.8)


def test_t9d5_edition_mismatched_source_grant_is_unavailable():
    w = wave("VALID", 1990, .6, source_family="ACTUAL_SOURCE", edition="E2")
    grant = T.SourceGrant(grant_source_family="ACTUAL_SOURCE", grant_edition="E1",
                          grant_current=True)
    x = T.read_selected_world(WORLD, case([w]), T.METHOD_M0_HOLD, 1995, source_grant=grant)
    assert x.refused_code == T.REFUSED_SOURCE_GRANT_MISMATCH
    assert no_open_routes(x)


def test_t9d5_noncurrent_source_grant_is_unavailable():
    w = wave("VALID", 1990, .6, source_family="ACTUAL_SOURCE", edition="E1")
    grant = T.SourceGrant(grant_source_family="ACTUAL_SOURCE", grant_edition="E1",
                          grant_current=False)
    x = T.read_selected_world(WORLD, case([w]), T.METHOD_M0_HOLD, 1995,
                              retrospective=True, source_grant=grant)
    assert x.refused_code == T.REFUSED_SOURCE_GRANT_NOT_CURRENT
    assert no_open_routes(x)


def test_t9d5_wrong_source_owner_grant_is_unavailable():
    w = wave("VALID", 1990, .6, source_family="ACTUAL_SOURCE", edition="E1")
    grant = T.SourceGrant(grant_source_family="OTHER_SOURCE", grant_edition="E1",
                          grant_current=True)
    x = T.read_selected_world(WORLD, case([w]), T.METHOD_M0_HOLD, 1995, source_grant=grant)
    assert x.refused_code == T.REFUSED_SOURCE_GRANT_WRONG_OWNER
    assert no_open_routes(x)


def test_t9d5_missing_issuer_is_unavailable_never_synthetic_authority():
    w = wave("VALID", 1990, .6, source_family="ACTUAL_SOURCE", edition="E1")
    x = T.read_selected_world(WORLD, case([w]), T.METHOD_M0_HOLD, 1995,
                              require_source_grant=True)
    assert x.refused_code == T.REFUSED_SOURCE_GRANT_MISSING
    assert no_open_routes(x)
    assert x.authorized_opportunity is False


def test_t9d5_matching_current_source_grant_is_recorded_not_inferred():
    w0 = wave("W0", 1990, .2, source_family="ACTUAL_SOURCE", edition="E1")
    w1 = wave("W1", 2000, .6, source_family="ACTUAL_SOURCE", edition="E1")
    grant = T.SourceGrant(grant_source_family="ACTUAL_SOURCE", grant_edition="E1",
                          grant_current=True)
    x = T.read_selected_world(WORLD, case([w0, w1]), T.METHOD_M0_HOLD, 2000,
                              retrospective=True, source_grant=grant)
    assert x.refused_code is None
    assert x.provenance["source_grant_status"] == "SOURCE_GRANT_VERIFIED"
    assert x.product_observation_status == T.PRODUCT_OBSERVED_AT_CLOCK
    assert x.authorized_opportunity is True
    # presence of metadata alone never grants: the unentitled world stays withheld
    empty = T.StructuralWorld(WORLD.world_id, WORLD.structural_routes, (),
                              WORLD.institution)
    y = T.read_selected_world(empty, case([w0, w1]), T.METHOD_M0_HOLD, 2000,
                              retrospective=True, source_grant=grant)
    assert not y.authorized_opportunity and no_open_routes(y)


# ============================================== preservation controls
def test_t9d_preserves_v553_imports_by_identity():
    import data.ddm_build_copy.ddm_v553_temporal_pressure as v
    assert T._interp is v._interp
    assert T._pressure_band is v._pressure_band
    assert T._bounded_score is v._bounded_score
    assert T.AUTHORIZED_SPARSE_TEMPORAL_KEY == v.AUTHORIZED_SPARSE_TEMPORAL_KEY
    assert T.PROBE_ONLY_TEMPORAL_KEY == v.PROBE_ONLY_TEMPORAL_KEY
    assert T.BLOCKED_TEMPORAL_KEY == v.BLOCKED_TEMPORAL_KEY


def test_t9d_no_person_memory_knowledge_or_exposure_claim():
    x = T.read_selected_world(WORLD, case(), T.METHOD_M0_HOLD, 1995)
    payload = x.as_dict()
    assert not payload.get("actor_memory")
    assert not payload.get("remembered_exposure")
    assert not payload.get("actor_knowledge")
    assert not payload.get("actor_id")
    assert not any("memory" in k or "remembered" in k or "exposure" in k
                   for k in x.provenance)
    assert x.provenance["synthetic"] is True
    assert x.provenance["observed_temporal_calibration"] is False


def test_t9d_structural_constancy_still_certified():
    early = T.read_selected_world(WORLD, case(), T.METHOD_M1_INTERP, 1990, retrospective=True)
    late = T.read_selected_world(WORLD, case(), T.METHOD_M1_INTERP, 2000, retrospective=True)
    assert T.structurally_identical(early, late)
    changed = replace(WORLD, access_grants=())
    denied = T.read_selected_world(changed, case(), T.METHOD_M0_HOLD, 2000,
                                   retrospective=True)
    assert not T.structurally_identical(early, denied)
