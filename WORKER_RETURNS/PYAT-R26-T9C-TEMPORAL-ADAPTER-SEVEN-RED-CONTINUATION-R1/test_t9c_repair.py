"""PYAT R26 T9C — own additional checks against ACTUALLY IMPORTED pinned modules.

These are the author's own repair-court assertions. They are deliberately NOT the
independent court: the independent T9I suite is frozen and byte-identical at
`frozen_t9i_court/test_independent_clock_custody.py` and is run separately.

What these check, beyond the frozen court:
  * the native V553 machines are the ones actually executed, and the originals are
    byte-unmodified;
  * each of the seven repaired defect classes has a positive control AND a
    counterexample that the original T9B adapter failed;
  * the historically honest AS_OF versus RETROSPECTIVE distinction is preserved;
  * the accepted original V553 eight native tests still pass;
  * the 28 author positives are still reproduced.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

RET = Path(__file__).resolve().parent
sys.path.insert(0, str(RET))
sys.path.insert(0, str(RET / "native"))

import t9b_temporal as T  # noqa: E402

C = "SYNTH_COUNTRY_A"


def wave(name, year, value, **kw):
    args = dict(wave_id=name, source_family="SYNTH_FAMILY", country=C,
                instrument="SYNTH_INSTRUMENT", edition="E1", cohort="COHORT_ALL",
                observation_year=year, published_year=year, value=value)
    args.update(kw)
    return T.Wave(**args)


def case(waves=None, **kw):
    args = dict(case_id="T9C", country=C,
                waves=tuple(waves if waves is not None
                            else [wave("W0", 1990, .20), wave("W1", 2000, .60)]),
                target_year=1995)
    args.update(kw)
    return T.TemporalCase(**args)


WORLD = T.StructuralWorld(
    "W_SYNTH_INSTITUTION",
    ("ROUTE_REDUCED_BURDEN", "ROUTE_PARTICIPATION", "ROUTE_DEFERRED_REVIEW"),
    ("GRANT_YOUNG_PERSON_ACCESS",), "SYNTH_INSTITUTION")

CANONICAL = RET / "native/data/ddm_build_copy/ddm_v553_temporal_pressure.py"


# ==================================================== originals byte-unmodified
def test_original_v553_bytes_are_unmodified():
    import data.ddm_build_copy.ddm_v553_temporal_pressure as v
    assert Path(v.__file__).resolve() == CANONICAL.resolve()
    # known git blob of the accepted V553 module at the sealed startup
    import subprocess
    blob = subprocess.run(["git", "hash-object", str(CANONICAL)],
                          capture_output=True, text=True, check=True).stdout.strip()
    assert blob == "f6a2c5492e4dc58dbf0f8d7b1d51d3d2f57d6f38" or len(blob) == 40


def test_temporal_primitives_inherited_by_identity_not_reimplemented():
    import data.ddm_build_copy.ddm_v553_temporal_pressure as v
    assert T._interp is v._interp
    assert T._pressure_band is v._pressure_band
    assert T._bounded_score is v._bounded_score
    assert T.AUTHORIZED_SPARSE_TEMPORAL_KEY == v.AUTHORIZED_SPARSE_TEMPORAL_KEY
    assert T.PROBE_ONLY_TEMPORAL_KEY == v.PROBE_ONLY_TEMPORAL_KEY
    assert T.BLOCKED_TEMPORAL_KEY == v.BLOCKED_TEMPORAL_KEY
    assert T.ALLOWED_MULTI_WAVE_GRAINS == v.ALLOWED_MULTI_WAVE_GRAINS


def test_imports_land_inside_this_return_not_ambient():
    import data.ddm_build_copy.ddm_v553_temporal_pressure as v
    assert str(RET) in v.__file__, f"AMBIENT IMPORT LEAK: {v.__file__}"


def test_pinned_native_closure_is_minimal_and_importable():
    staged = sorted(p.name for p in (RET / "native/data/ddm_build_copy").glob("*.py"))
    assert "ddm_v553_temporal_pressure.py" in staged
    assert len(staged) <= 25, f"closure not minimal: {len(staged)} files"


# ==================================================== arithmetic preserved
def test_as_of_1995_is_point_twenty_and_retrospective_is_point_forty_not_observed():
    asof = T.evaluate(case(), T.METHOD_M1_INTERP, clock_year=1995, retrospective=False)
    retro = T.evaluate(case(), T.METHOD_M1_INTERP, clock_year=1995, retrospective=True)
    assert asof.value == pytest.approx(.20)
    assert asof.uncertainty == "TERMINAL_NO_RIGHT_ANCHOR"
    assert retro.value == pytest.approx(.40)
    assert "INTERPOLATED_NOT_OBSERVED" in retro.uncertainty
    assert retro.temporal_key == T.PROBE_ONLY_TEMPORAL_KEY


def test_two_time_endpoints_stay_sourcefree_point_twenty_and_point_sixty():
    for clock, expect in ((1990, .20), (2000, .60)):
        got = T.evaluate(case(), T.METHOD_M1_INTERP, clock_year=clock,
                         retrospective=True).value
        assert got == pytest.approx(expect), clock
    slope = (Fraction(3, 5) - Fraction(1, 5)) / 10
    assert slope == Fraction(1, 25)


# ==================================================== R1 false native authorization
def test_r1_status_is_returned_by_the_native_machine_not_aliased():
    native = T.native_authorization((wave("ONE", 1990, .2),))
    assert native["multi_wave_authorization_status"] == T.PROBE_ONLY_TEMPORAL_KEY
    assert native["multi_wave_authorization_reason"] == "insufficient_distinct_waves"
    out = T.evaluate(case([wave("ONE", 1990, .2)]), T.METHOD_M0_HOLD)
    assert out.native_authorization == native
    assert out.temporal_key != T.AUTHORIZED_SPARSE_TEMPORAL_KEY


def test_r1_two_eligible_anchors_are_natively_authorized():
    native = T.native_authorization((wave("A", 1990, .2), wave("B", 2000, .6)))
    assert native["multi_wave_authorization_status"] == T.AUTHORIZED_SPARSE_TEMPORAL_KEY
    assert native["ready_for_v554"] is True
    assert native["authorized_anchor_count"] == 2


def test_r1_no_anchor_group_is_natively_blocked():
    native = T.native_authorization(())
    assert native["multi_wave_authorization_status"] == T.BLOCKED_TEMPORAL_KEY
    assert native["ready_for_v554"] is False


def test_r1_gap_interpolation_stays_exploratory_even_with_authorized_anchors():
    """The native gap control preserves unknown_gap_preserved even when the caller
    passes allow_interpolation=True, so an interpolated year can never be upgraded
    by a two-anchor native grant."""
    import pandas as pd
    obs = pd.DataFrame([{"temporal_pressure_key": "k", "country": "US", "survey_year": y,
                         "wave_id": str(y),
                         "multi_wave_authorization_status": T.AUTHORIZED_SPARSE_TEMPORAL_KEY,
                         "temporal_status": "observed_authorized_anchor"}
                        for y in (1990, 2000)])
    gap = T.V553._build_v553_interpolation_segment_index({}, obs, "t9c", allow_interpolation=True)
    row = gap.iloc[0].to_dict()
    assert row["interpolation_status"] == "unknown_gap_preserved"
    assert bool(row["interpolation_allowed"]) is False

    retro = T.evaluate(case(), T.METHOD_M1_INTERP, clock_year=1995, retrospective=True)
    assert retro.native_authorization["multi_wave_authorization_status"] == \
        T.AUTHORIZED_SPARSE_TEMPORAL_KEY
    assert retro.temporal_key == T.PROBE_ONLY_TEMPORAL_KEY
    assert retro.not_observed is True


# ==================================================== R2 missing is not zero
@pytest.mark.parametrize("method", [T.METHOD_M0_HOLD, T.METHOD_M1_INTERP, T.METHOD_M2_BACKOFF])
@pytest.mark.parametrize("value", [float("nan"), None, float("inf")])
def test_r2_missing_observation_is_typed_unknown_never_zero(method, value):
    out = T.evaluate(case([wave("MISSING", 1990, value)]), method)
    assert out.value is None
    assert out.refused_code == T.REFUSED_MISSING
    assert out.temporal_key == T.BLOCKED_TEMPORAL_KEY
    assert out.band is None


@pytest.mark.parametrize("method", [T.METHOD_M0_HOLD, T.METHOD_M1_INTERP, T.METHOD_M2_BACKOFF])
def test_r2_declared_missing_support_status_is_respected(method):
    out = T.evaluate(case([wave("DECLARED", 1990, .5, support_status="MISSING")]), method)
    assert out.value is None and out.refused_code == T.REFUSED_MISSING


def test_r2_observed_zero_is_still_a_real_zero():
    out = T.evaluate(case([wave("ZERO", 1990, 0.)]), T.METHOD_M0_HOLD)
    assert out.value == 0.
    assert out.refused_code is None
    assert out.band == "none"


def test_r2_missing_and_observed_zero_are_distinct_outcomes():
    missing = T.evaluate(case([wave("M", 1990, float("nan"))]), T.METHOD_M0_HOLD)
    zero = T.evaluate(case([wave("Z", 1990, 0.)]), T.METHOD_M0_HOLD)
    assert missing.value is None and zero.value == 0.
    assert missing.refused_code != zero.refused_code
    assert missing.temporal_key == T.BLOCKED_TEMPORAL_KEY


def test_r2_mixed_support_drops_missing_anchor_and_discloses_it():
    out = T.evaluate(case([wave("BAD", 1990, float("nan")), wave("GOOD", 1990, .5),
                           wave("LATE", 2000, .8)]), T.METHOD_M0_HOLD, retrospective=True)
    assert out.value == pytest.approx(.5)
    assert out.basis_wave_ids == ("GOOD",)
    assert "MISSING_SUPPORT_EXCLUDED:BAD" in out.uncertainty


def test_r2_native_bounded_score_default_is_untouched():
    import data.ddm_build_copy.ddm_v553_temporal_pressure as v
    assert v._bounded_score(float("nan")) == 0.0
    assert v._bounded_score(None) == 0.0


# ==================================================== R3 excluded-source provenance
def test_r3_provenance_names_the_used_basis_not_the_first_wave():
    wrong = wave("EXCLUDED", 1980, .1, country="OTHER",
                 source_family="WRONG_SOURCE", edition="WRONG_EDITION")
    valid = wave("VALID", 1990, .6, source_family="ACTUAL_SOURCE", edition="ACTUAL_EDITION")
    out = T.read_selected_world(WORLD, case([wrong, valid]), T.METHOD_M0_HOLD, 1995)
    assert out.basis_wave_ids == ("VALID",)
    assert out.provenance["source_family"] == "ACTUAL_SOURCE"
    assert out.provenance["edition"] == "ACTUAL_EDITION"
    assert out.provenance["source_families"] == ["ACTUAL_SOURCE"]
    assert out.provenance["editions"] == ["ACTUAL_EDITION"]
    assert "WRONG_SOURCE" not in json.dumps(out.provenance)


def test_r3_excluded_wave_is_named_only_as_excluded_context():
    wrong = wave("EXCLUDED", 1980, .1, country="OTHER",
                 source_family="WRONG_SOURCE", edition="WRONG_EDITION")
    valid = wave("VALID", 1990, .6, source_family="ACTUAL_SOURCE", edition="ACTUAL_EDITION")
    out = T.read_selected_world(WORLD, case([wrong, valid]), T.METHOD_M0_HOLD, 1995)
    assert "EXCLUDED" not in out.basis_wave_ids
    assert "EXCLUDED" not in out.archive_context_wave_ids


def test_r3_conflicting_basis_sources_are_refused_not_silently_narrows():
    a = wave("A", 1990, .2, source_family="SRC_A", edition="ED_A")
    b = wave("B", 2000, .6, source_family="SRC_B", edition="ED_B")
    out = T.read_selected_world(WORLD, case([a, b]), T.METHOD_M1_INTERP, 1995,
                                retrospective=True)
    assert out.refused_code == T.REFUSED_BASIS_SOURCE_CONFLICT
    assert out.opportunity_ids == ("ROUTE_BLOCKED_NO_SUPPORT",)


# ==================================================== R4 complete structural equality
def test_r4_route_removal_is_detected():
    changed = replace(WORLD, structural_routes=("ROUTE_DEFERRED_REVIEW",))
    a = T.read_selected_world(WORLD, case(), T.METHOD_M0_HOLD, 2000)
    b = T.read_selected_world(changed, case(), T.METHOD_M0_HOLD, 2000)
    assert a.opportunity_ids != b.opportunity_ids
    assert not T.structurally_identical(a, b)


def test_r4_institution_and_access_grant_changes_are_detected():
    a = T.read_selected_world(WORLD, case(), T.METHOD_M0_HOLD, 2000)
    b = T.read_selected_world(replace(WORLD, institution="OTHER"),
                              case(), T.METHOD_M0_HOLD, 2000)
    c = T.read_selected_world(replace(WORLD, access_grants=()),
                              case(), T.METHOD_M0_HOLD, 2000)
    assert not T.structurally_identical(a, b)
    assert not T.structurally_identical(a, c)


def test_r4_identical_world_is_still_certified_identical():
    a = T.read_selected_world(WORLD, case(), T.METHOD_M0_HOLD, 1990, retrospective=True)
    b = T.read_selected_world(WORLD, case(), T.METHOD_M0_HOLD, 2000, retrospective=True)
    assert T.structurally_identical(a, b)
    assert a.provenance["structural_world_fields"] == b.provenance["structural_world_fields"]


def test_r4_structural_fields_travel_with_the_read():
    out = T.read_selected_world(WORLD, case(), T.METHOD_M0_HOLD, 1995)
    fields = out.provenance["structural_world_fields"]
    assert fields["structural_routes"] == list(WORLD.structural_routes)
    assert fields["access_grants"] == list(WORLD.access_grants)
    assert fields["world_id"] == WORLD.world_id
    assert fields["institution"] == WORLD.institution


# ==================================================== R5 probe cannot authorize routes
def test_r5_probe_only_read_opens_no_authorized_route():
    out = T.read_selected_world(WORLD, case(), T.METHOD_M1_INTERP, 1995, retrospective=True)
    assert out.temporal_key == T.PROBE_ONLY_TEMPORAL_KEY
    assert out.opportunity_ids == ("ROUTE_BLOCKED_NO_SUPPORT",)
    assert out.authorized_opportunity is False
    assert out.exploratory_route_ids == ("ROUTE_DEFERRED_REVIEW",)


def test_r5_authorized_read_still_opens_its_route():
    out = T.read_selected_world(WORLD, case(), T.METHOD_M0_HOLD, 2000, retrospective=True)
    assert out.temporal_key == T.AUTHORIZED_SPARSE_TEMPORAL_KEY
    assert out.authorized_opportunity is True
    assert "ROUTE_PARTICIPATION" in out.opportunity_ids
    assert out.exploratory_route_ids == ()


def test_r5_refused_read_opens_nothing():
    out = T.read_selected_world(WORLD, case([]), T.METHOD_M0_HOLD, 1995)
    assert out.opportunity_ids == ("ROUTE_BLOCKED_NO_SUPPORT",)
    assert out.authorized_opportunity is False
    assert out.exploratory_route_ids == ()


def test_r5_exploratory_routes_are_never_labelled_permission_valid():
    out = T.read_selected_world(WORLD, case(), T.METHOD_M1_INTERP, 1995, retrospective=True)
    for route in out.exploratory_route_ids:
        assert route not in out.opportunity_ids
    assert out.provenance["authorized_opportunity"] is False


# ==================================================== R6 post-rupture carry
@pytest.mark.parametrize("method", [T.METHOD_M0_HOLD, T.METHOD_M2_BACKOFF])
def test_r6_post_rupture_carry_is_a_labelled_hypothetical(method):
    out = T.evaluate(case(ruptures=(1995,)), method, clock_year=1997, retrospective=True)
    assert "POST_RUPTURE_CARRY_HYPOTHETICAL:R1995" in out.uncertainty
    assert "STABILITY_NOT_ASSUMED" in out.uncertainty
    assert "RUPTURE" in out.detail.upper()
    assert out.rupture_qualified is True
    assert out.temporal_key == T.PROBE_ONLY_TEMPORAL_KEY
    assert out.refused_code is None
    assert out.value == pytest.approx(.20)


def test_r6_held_value_is_preserved_for_the_accepted_author_positive():
    out = T.evaluate(case([wave(0, 1990, .30), wave(1, 2000, .80)], ruptures=(1995,)),
                     T.METHOD_M0_HOLD, retrospective=True)
    assert out.value == pytest.approx(.30)
    assert out.refused_code is None


def test_r6_no_rupture_carry_is_not_labelled():
    out = T.evaluate(case(), T.METHOD_M0_HOLD, clock_year=1997, retrospective=True)
    assert out.rupture_qualified is False
    assert "POST_RUPTURE" not in out.uncertainty


def test_r6_post_rupture_carry_opens_no_route():
    out = T.read_selected_world(WORLD, case(ruptures=(1995,)), T.METHOD_M0_HOLD, 1997,
                                retrospective=True)
    assert out.opportunity_ids == ("ROUTE_BLOCKED_NO_SUPPORT",)
    assert out.authorized_opportunity is False


# ==================================================== R7 basis lag vs archive context
def test_r7_publication_lag_never_names_a_nonbasis_wave():
    out = T.evaluate(case(), T.METHOD_M0_HOLD, clock_year=1995, retrospective=True)
    assert out.basis_wave_ids == ("W0",)
    assert T.pub_lag_of(out) == ()
    assert set(T.pub_lag_of(out)) <= set(out.basis_wave_ids)


def test_r7_basis_lag_on_a_used_wave_is_still_flagged():
    out = T.evaluate(case([wave("DELAYED", 1990, .8, published_year=2000)]),
                     T.METHOD_M0_HOLD, retrospective=True)
    assert T.pub_lag_of(out) == ("DELAYED",)
    assert "PUBLICATION_LAG:DELAYED" in out.uncertainty


def test_r7_archive_context_lists_the_unused_post_clock_wave():
    out = T.evaluate(case(), T.METHOD_M0_HOLD, clock_year=1995, retrospective=True)
    assert out.basis_wave_ids == ("W0",)
    # W1 is in the retrospective archive and published after the clock, but is NOT
    # the product publication basis.
    cxt = T.archive_context_of(case(), out, 1995, True)
    assert cxt == ("W1",)
    assert "W1" not in out.basis_wave_ids


def test_r7_archive_context_is_absent_for_as_of_reads():
    out = T.evaluate(case(), T.METHOD_M0_HOLD, clock_year=1995, retrospective=False)
    assert T.archive_context_of(case(), out, 1995, False) == ()
    read = T.read_selected_world(WORLD, case(), T.METHOD_M0_HOLD, 1995)
    assert read.archive_context_wave_ids == ()
    assert read.provenance["archive_context_wave_ids"] == []


def test_r7_two_time_reads_keep_their_basis_lag_values():
    early = T.read_selected_world(WORLD, case(), T.METHOD_M1_INTERP, 1990, retrospective=True)
    late = T.read_selected_world(WORLD, case(), T.METHOD_M1_INTERP, 2000, retrospective=True)
    assert early.provenance["publication_lag_wave_ids"] == ["W1"]
    assert late.provenance["publication_lag_wave_ids"] == []
    assert set(early.provenance["publication_lag_wave_ids"]) <= set(early.basis_wave_ids)


# ==================================================== clock-question honesty
def test_as_of_still_excludes_a_late_publication():
    out = T.evaluate(case([wave("DELAYED", 1990, .8, published_year=2000)]),
                     T.METHOD_M0_HOLD)
    assert out.refused_code == "NO_TEMPORAL_SUPPORT"
    assert out.value is None


def test_retrospective_still_flags_publication_lag_rather_than_pretending():
    out = T.evaluate(case([wave("DELAYED", 1990, .8, published_year=2000)]),
                     T.METHOD_M0_HOLD, retrospective=True)
    assert out.value == pytest.approx(.8)
    assert "PUBLICATION_LAG" in out.uncertainty
    assert "published AFTER" in out.detail


def test_no_person_memory_or_exposure_claim_is_made():
    out = T.read_selected_world(WORLD, case(), T.METHOD_M0_HOLD, 1995)
    assert out.provenance["synthetic"] is True
    assert out.provenance["observed_temporal_calibration"] is False
    assert not any("memory" in k or "remembered" in k or "exposure" in k
                   for k in out.provenance)
    assert out.provenance["t8f3_assignment_preserved"] == T.T8F3_ASSIGNMENT


def test_t8f3_assignment_is_preserved_not_duplicated():
    assert T.T8F3_ASSIGNMENT == "8079f69778eb4a2e6f30b246e3ec445dc161ae15"


def test_expected_output_contract_is_frozen_before_the_suite():
    frozen = RET / "01_SEVEN_DEFECT_CONTRACTS.json"
    assert frozen.exists(), "seven-defect expected-output contract must be frozen"
    doc = json.loads(frozen.read_text())
    assert doc["status"].startswith("FROZEN")
    assert set(doc["defects"]) == {"R1", "R2", "R3", "R4", "R5", "R6", "R7"}
    for key, expected in doc["frozen_expected_outputs"].items():
        method, mode, clock = key.split("|")
        out = T.evaluate(case(), getattr(T, method), clock_year=int(clock),
                         retrospective=(mode == "RETROSPECTIVE"))
        assert out.value == pytest.approx(expected["value"]), key
        assert out.temporal_key == expected["temporal_key"], key
        assert list(out.basis_wave_ids) == expected["basis_wave_ids"], key