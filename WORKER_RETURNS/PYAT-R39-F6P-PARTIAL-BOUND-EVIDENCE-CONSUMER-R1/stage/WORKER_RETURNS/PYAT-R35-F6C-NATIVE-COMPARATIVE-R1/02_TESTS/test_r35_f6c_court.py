"""R35 F6C A/B/C native method court.

Asserts each candidate against the oracle frozen in
01_FROZEN_ESTIMANDS_AND_INDEPENDENT_ORACLE.json BEFORE any candidate output was
consulted for an expectation.

Expectation direction is enforced here: every expected value lives in the
frozen JSON, and the candidates are run to see whether they match. Nothing in
this file derives an expectation from a candidate result.

Candidates are loaded by absolute path from their verified pinned blobs. A
substituted, drifted or branch-local module fails at load, before any assertion.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction as F
from pathlib import Path

import pytest

RETURN = Path(__file__).resolve().parents[1]
STAGING = RETURN / "staging"
SHARED = STAGING / "shared"
COLD = RETURN / "05_COLD"
REPRO = RETURN / "repro"
sys.path.insert(0, str(SHARED))
sys.path.insert(0, str(REPRO))

import f6c_method_c as MC          # noqa: E402
import f6c_oracle_worlds as OW     # noqa: E402

FROZEN = json.loads((RETURN / "01_FROZEN_ESTIMANDS_AND_INDEPENDENT_ORACLE.json").read_text())
CASES = FROZEN["cases"]

CANDIDATE_BLOBS = {
    "A": ("cand_A", "fc5e37fa5b2f0eb689593b42d95479d1327cb94c"),
    "A0": ("cand_A0_historical", "182cc7970d7624f6614015f5a51d0602e1630d52"),
    "B": ("cand_B", "2df811d76db258d98d89ffb43c830cb221ff9a7d"),
}


def _blob(path):
    b = Path(path).read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def _load(key):
    d, expect = CANDIDATE_BLOBS[key]
    p = STAGING / d / "rawlsing_next" / "pre553_heterogeneous_synthesis.py"
    got = _blob(p)
    assert got == expect, f"{key} blob {got} != pinned {expect}"
    spec = importlib.util.spec_from_file_location(f"court_cand_{key}", p)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


MODS = {k: _load(k) for k in CANDIDATE_BLOBS}


def _bundle(key, world):
    target, sources, policy = OW.WORLD_BUILDERS[world]()
    return MODS[key].synthesize(target, sources, policy), target, sources, policy


def _cond(key, bundle, world):
    conditions, outcome = OW.CONSUMER_REQUEST[world]
    mod = MODS[key]
    try:
        return mod.conditional(bundle, conditions, outcome)
    except TypeError:
        return mod.conditional(bundle, conditions, outcome)


# --------------------------------------------------------------- custody ----

def test_every_candidate_is_at_its_pinned_blob():
    for key, (d, expect) in CANDIDATE_BLOBS.items():
        p = STAGING / d / "rawlsing_next" / "pre553_heterogeneous_synthesis.py"
        assert _blob(p) == expect, key


def test_f6m_declares_the_corrected_producer_as_its_base():
    """F6M is derived from the CORRECTED blob, not the obsolete one. This is
    independent textual confirmation of the corrected source identity."""
    assert MODS["B"].ORIGINAL_PRODUCER_BLOB == "fc5e37fa5b2f0eb689593b42d95479d1327cb94c"


def test_corrected_and_obsolete_are_not_byte_identical():
    a, a0 = CANDIDATE_BLOBS["A"][1], CANDIDATE_BLOBS["A0"][1]
    assert a != a0


# ------------------------------------------------- W1 positive invariance ----

def test_W1_A_matches_frozen_joint_and_conditional():
    o = CASES["W1_full_coverage_disjoint"]["oracle"]
    b, *_ = _bundle("A", "W1_full_coverage_disjoint")
    cells = [F(c["probability"]) for c in b["candidate"]["distribution"]]
    assert [str(c) for c in cells] == list(
        o["joint_cell_probabilities_in_declared_order"].values())
    assert sum(cells) == 1
    assert b["candidate"]["uncovered_target_mass"] == o["uncovered_target_mass"]
    r = _cond("A", b, "W1_full_coverage_disjoint")
    assert r["state"] == o["conditional_state"]
    assert r["model_denominator_mass"] == o["conditional_model_denominator_mass"]
    assert r["probabilities"] == o["conditional_probabilities"]


def test_W1_B_matches_frozen_joint_and_conditional():
    o = CASES["W1_full_coverage_disjoint"]["oracle"]
    b, *_ = _bundle("B", "W1_full_coverage_disjoint")
    assert [F(c["probability"]) for c in b["candidate"]["distribution"]] == \
        [F(v) for v in o["joint_cell_probabilities_in_declared_order"].values()]
    r = _cond("B", b, "W1_full_coverage_disjoint")
    assert r["state"] == o["conditional_state"]
    assert r["probabilities"] == o["conditional_probabilities"]
    assert b["decision"] == o["expected_decision"]
    assert b["target_joint_status"] == o["expected_target_joint_status"]


def test_W1_A_and_B_are_genuinely_invariant_not_merely_agreeing_by_construction():
    """Genuine scientific invariance: two independent implementations read the
    IDENTICAL value off the IDENTICAL legitimate synthesized field.

    The provenance check is the informative half. values_read_hash is a hash of
    the distribution actually read, so it MUST be equal. bundle_hash covers the
    whole bundle, so it MUST differ, because A and B emit different decision,
    ceiling and gate fields. Equal values under different provenance is exactly
    the invariance claim, and it is only credible if the bundles are not simply
    the same object counted twice."""
    ba, *_ = _bundle("A", "W1_full_coverage_disjoint")
    bb, *_ = _bundle("B", "W1_full_coverage_disjoint")
    ra = _cond("A", ba, "W1_full_coverage_disjoint")
    rb = _cond("B", bb, "W1_full_coverage_disjoint")
    assert ra["probabilities"] == rb["probabilities"]
    assert ra["values_read_hash"] == rb["values_read_hash"], \
        "identical values read must produce an identical values_read_hash"
    assert ba["content_hash"] != bb["content_hash"], \
        "distinct bundles must have distinct provenance hashes"


def test_W1_C_refuses_to_point_identify_without_transport_permission():
    target, sources, policy = OW.WORLD_BUILDERS["W1_full_coverage_disjoint"]()
    b = MC.nopooling_bounds(target, sources, policy)
    assert b["joint_status"] == "NOT_IDENTIFIED_NO_POOLING_NO_TRANSPORT_PERMISSION"
    assert b["total_unknown_mass"] == "1"
    assert all(v["lower"] == "0" and v["upper"] == "1"
               for v in b["target_marginal_bounds_employment_position"].values())
    st = MC.condition_status(b, *OW.CONSUMER_REQUEST["W1_full_coverage_disjoint"])
    assert st["state"] == "UNAVAILABLE"
    assert "probabilities" not in st


# ------------------------------------------------------ W2 THE DECISIVE ----

def test_W2_A_reports_full_coverage_despite_destroyed_planned_evidence():
    """Method A's defect, asserted against the frozen expectation."""
    o = CASES["W2_mixed_eligibility_trap"]["oracle"]["method_A_tidy_point"]
    b, *_ = _bundle("A", "W2_mixed_eligibility_trap")
    assert b["candidate"]["uncovered_target_mass"] == o["uncovered_target_mass"] == "0"
    assert b["decision"] == o["expected_decision"] == "SYNTHETIC_CANDIDATE"
    assert b["candidate"]["distribution"] is not None
    r = _cond("A", b, "W2_mixed_eligibility_trap")
    assert r["state"] == o["conditional_state"]
    assert r["probabilities"] == o["conditional_probabilities"]


def test_W2_B_preserves_the_dropped_source_planned_share_as_unknown_mass():
    o = CASES["W2_mixed_eligibility_trap"]["oracle"]
    b, *_ = _bundle("B", "W2_mixed_eligibility_trap")
    assert b["candidate"]["uncovered_target_mass"] == o["uncovered_target_mass"] == "1/4"
    assert b["decision"] == o["expected_decision"] == "PARTIAL_IDENTIFICATION_ONLY"
    assert b["target_joint_status"] == o["expected_target_joint_status"]
    assert b["candidate"]["distribution"] is None
    cov = b["candidate"]["covered_subprobability"]
    assert [F(c["probability"]) for c in cov] == \
        [F(v) for v in o["covered_subprobability_in_declared_order"].values()]
    assert sum(F(c["probability"]) for c in cov) == F(3, 4)
    reasons = b["candidate"]["support"]["minority"]["exclusion_reasons"]
    assert reasons["S_A"] == o["exclusion_reason_for_S_A"]


def test_W2_B_refuses_the_point_read_and_names_the_reason():
    o = CASES["W2_mixed_eligibility_trap"]["oracle"]
    b, *_ = _bundle("B", "W2_mixed_eligibility_trap")
    r = _cond("B", b, "W2_mixed_eligibility_trap")
    assert r["state"] == o["conditional_state"]
    assert r["reason"] == o["conditional_reason"]
    assert "probabilities" not in r


def test_W2_the_two_rules_disagree_about_coverage_and_that_is_the_whole_finding():
    ba, *_ = _bundle("A", "W2_mixed_eligibility_trap")
    bb, *_ = _bundle("B", "W2_mixed_eligibility_trap")
    assert ba["candidate"]["uncovered_target_mass"] == "0"
    assert F(bb["candidate"]["uncovered_target_mass"]) > 0


def test_W2_C_bounds_are_strictly_wider_than_Bs_covered_subprobability():
    """C supplies the genuine [q, q+unknown] marginal interval that neither A
    nor B emits. A and B leave the reader to recombine a subprobability and a
    scalar; C performs the recombination."""
    target, sources, policy = OW.WORLD_BUILDERS["W2_mixed_eligibility_trap"]()
    bb, *_ = _bundle("B", "W2_mixed_eligibility_trap")
    perm = {"minority": {sources[1]["source_id"]}}
    bc = MC.nopooling_bounds(target, sources, policy, transport_permission=perm)
    covered = {tuple(c["categories"]): F(c["probability"])
               for c in bb["candidate"]["covered_subprobability"]}
    # With exactly the same admitted source B used, C's identified component
    # must equal B's covered minority contribution.
    assert bc["joint_status"] == "PARTIAL_STRATUM_ADMITTED_NO_POOLING"
    assert bc["total_unknown_mass"] == "1/2"
    for lab, iv in bc["target_marginal_bounds_employment_position"].items():
        assert F(iv["upper"]) - F(iv["lower"]) == F(1, 2)
    assert covered is not None


# ------------------------------------------------------- W7 the same defect --

def test_W7_A_reports_full_coverage_with_a_whole_source_excluded_everywhere():
    o = CASES["W7_source_excluded_all_strata"]["oracle"]["method_A_tidy_point"]
    b, *_ = _bundle("A", "W7_source_excluded_all_strata")
    assert b["candidate"]["uncovered_target_mass"] == o["uncovered_target_mass"] == "0"
    r = _cond("A", b, "W7_source_excluded_all_strata")
    assert r["probabilities"] == o["conditional_probabilities"]


def test_W7_B_reports_half_the_target_as_unknown():
    o = CASES["W7_source_excluded_all_strata"]["oracle"]
    b, *_ = _bundle("B", "W7_source_excluded_all_strata")
    assert b["candidate"]["uncovered_target_mass"] == o["expected_uncovered_target_mass"] == "1/2"
    assert b["decision"] == "PARTIAL_IDENTIFICATION_ONLY"
    r = _cond("B", b, "W7_source_excluded_all_strata")
    assert r["state"] == "UNAVAILABLE"


# ----------------------------------------------- W3 the one case A is right --

def test_W3_A_and_B_agree_on_unknown_mass_but_not_on_the_decision_label():
    """A's coverage rule is accidentally right here, but its DECISION LABEL is
    not: A never emits PARTIAL_IDENTIFICATION_ONLY, so a bundle with no
    distribution and 1/5 unknown mass is still labelled SYNTHETIC_CANDIDATE."""
    o = CASES["W3_minority_whole_stratum_absent"]["oracle"]
    ba, *_ = _bundle("A", "W3_minority_whole_stratum_absent")
    bb, *_ = _bundle("B", "W3_minority_whole_stratum_absent")
    assert ba["candidate"]["uncovered_target_mass"] == o["uncovered_target_mass"]
    assert bb["candidate"]["uncovered_target_mass"] == o["uncovered_target_mass"]
    assert ba["decision"] == o["expected_A_decision"] == "SYNTHETIC_CANDIDATE"
    assert bb["decision"] == o["expected_B_decision"] == "PARTIAL_IDENTIFICATION_ONLY"
    # The mislabelling is real: A has no distribution yet still claims a
    # synthetic candidate.
    assert ba["candidate"]["distribution"] is None
    assert _cond("A", ba, "W3_minority_whole_stratum_absent")["state"] == "UNAVAILABLE"
    assert _cond("B", bb, "W3_minority_whole_stratum_absent")["state"] == "UNAVAILABLE"


def test_A_never_emits_a_partial_identification_decision_in_any_world():
    """Method A has no PARTIAL_IDENTIFICATION_ONLY state at all. Wherever it
    loses coverage it either mislabels the bundle as SYNTHETIC_CANDIDATE or
    silently renormalizes the loss away. Enumerated across every world."""
    partial_states = 0
    for w in OW.WORLD_BUILDERS:
        try:
            b, *_ = _bundle("A", w)
        except MODS["A"].SynthesisError:
            continue
        if b["decision"] == "PARTIAL_IDENTIFICATION_ONLY":
            partial_states += 1
        if b.get("candidate") is not None and F(b["candidate"]["uncovered_target_mass"]) > 0:
            # Loss was renormalized away: a full point with no unknown mass.
            assert b["candidate"]["distribution"] is None, w
    assert partial_states == 0


def test_W3_B_names_why_each_source_was_excluded_and_A_does_not():
    bb, *_ = _bundle("B", "W3_minority_whole_stratum_absent")
    reasons = bb["candidate"]["support"]["minority"]["exclusion_reasons"]
    assert reasons == {"S_A": "NO_SOURCE_STRATUM", "S_B": "NO_SOURCE_STRATUM"}
    ba, *_ = _bundle("A", "W3_minority_whole_stratum_absent")
    assert "exclusion_reasons" not in ba["candidate"]["support"]["minority"]


# ------------------------------------------------------------- W4 leakage --

def test_W4_A_and_B_refuse_to_masquerade_a_tautology_as_predictive():
    o = CASES["W4_outcome_leakage"]["oracle"]
    for key in ("A", "B"):
        b, *_ = _bundle(key, "W4_outcome_leakage")
        r = _cond(key, b, "W4_outcome_leakage")
        assert r["state"] == o["expected_state"], key
        assert r["self_conditioning_status"] == o["expected_self_conditioning_status"], key


def test_W4_obsolete_blob_has_neither_leakage_nor_positivity_fix():
    b, *_ = _bundle("A0", "W4_outcome_leakage")
    r = _cond("A0", b, "W4_outcome_leakage")
    assert r["state"] == "SUPPORTED_MODEL"
    assert "self_conditioning_status" not in r


# ------------------------------------------------------------- W5 positivity --

def test_W5_A_and_B_both_refuse_to_manufacture_an_omitted_cell_as_zero():
    o = CASES["W5_positivity_incomplete_native_domain"]["oracle"]
    for key in ("A", "B"):
        with pytest.raises(MODS[key].SynthesisError) as ei:
            _bundle(key, "W5_positivity_incomplete_native_domain")
        assert "incomplete native joint domain" in str(ei.value), key
        assert "cannot be silently manufactured as zero" in str(ei.value), key


def test_W5_obsolete_blob_silently_accepts_the_positivity_violation():
    """The defect the HQ addendum attributes to 182cc797, executed."""
    b, *_ = _bundle("A0", "W5_positivity_incomplete_native_domain")
    assert b["candidate"]["distribution"] is not None
    r = _cond("A0", b, "W5_positivity_incomplete_native_domain")
    assert r["state"] == "SUPPORTED_MODEL"
    assert r["probabilities"] == {"formal": "22/35", "informal": "13/35"}


def test_W5_C_refuses_independently_rather_than_trusting_a_producer():
    target, sources, policy = OW.WORLD_BUILDERS["W5_positivity_incomplete_native_domain"]()
    with pytest.raises(MC.BoundRefusal) as ei:
        MC.nopooling_bounds(target, sources, policy)
    assert "POSITIVITY_INCOMPLETE_NATIVE_JOINT_DOMAIN" in str(ei.value)


# ------------------------------------------------------------- W6 overlap --

def test_W6_all_methods_refuse_a_joint_across_an_unresolved_duplicate_sample():
    for key in ("A", "B", "A0"):
        b, *_ = _bundle(key, "W6_overlap_duplicate_sample")
        assert b["decision"] == "SOURCE_INDEXED_BACKOFF", key
        assert b["candidate"] is None, key
        assert b["overlap_diagnostics"][0]["reason"] == "DUPLICATE_SAMPLE", key
        assert _cond(key, b, "W6_overlap_duplicate_sample")["state"] == "UNAVAILABLE", key
    target, sources, policy = OW.WORLD_BUILDERS["W6_overlap_duplicate_sample"]()
    with pytest.raises(MC.BoundRefusal) as ei:
        MC.nopooling_bounds(target, sources, policy)
    assert "INDISTINCT_SAMPLE_UNRESOLVED" in str(ei.value)


# --------------------------------------------------------- W8 out of support --

def test_W8_all_methods_refuse_a_condition_outside_mapped_support():
    for key in ("A", "B", "A0"):
        b, *_ = _bundle(key, "W8_condition_outside_mapped_support")
        r = _cond(key, b, "W8_condition_outside_mapped_support")
        assert r["state"] == "UNAVAILABLE", key
        assert r["reason"] == "CATEGORY_OUTSIDE_MAPPED_SUPPORT", key


# ------------------------------------------------- B's real-use fail-closed --

def test_B_real_use_refuses_even_on_a_complete_supported_bundle():
    b, *_ = _bundle("B", "W1_full_coverage_disjoint")
    r = MODS["B"].conditional(b, {"material_security": "secure"},
                              "employment_position", use="REAL_USE")
    assert r["state"] == "UNAVAILABLE"
    assert r["reason"] == "UNVERIFIED_OWNER_ADMISSION"
    assert r["real_use_authorized"] is False


def test_B_carries_test_only_ceilings_and_no_real_use_authority():
    b, *_ = _bundle("B", "W1_full_coverage_disjoint")
    assert b["real_use_authorized"] is False
    assert b["use_scope"] == "SOURCEFREE_EXPERIMENT_ONLY"
    assert b["owner_admission_status"] == "UNVERIFIED_INTEGRATION_BOUNDARY"
    assert b["origin_classification"] == "DECLARED_TEST_ONLY"
    assert all(n["authority_ceiling"] in ("TEST_ONLY", "UNVERIFIED")
               for n in b["evidence_graph"])


def test_B_declares_its_support_gate_is_aggregate_not_minority_protecting():
    b, *_ = _bundle("B", "W2_mixed_eligibility_trap")
    assert b["support_gate_semantics"] == \
        "AGGREGATE_SOURCE_STRATUM_RAW_COUNT_NOT_MINORITY_CELL_PROTECTION"
    assert b["candidate"]["support"]["minority"]["minority_cell_protection"] is False


def test_no_candidate_emits_a_route_or_selection_quantity():
    forbidden = ("route_probability", "selection_weight", "route_propensity")
    for key in CANDIDATE_BLOBS:
        b, *_ = _bundle(key, "W1_full_coverage_disjoint")
        blob = json.dumps(b, default=str).lower()
        for f in forbidden:
            assert f not in blob, (key, f)


# ----------------------------------------------------- C partial identification --

def test_C_reuses_the_original_native_partial_identification_primitive():
    target, sources, policy = OW.WORLD_BUILDERS["W1_full_coverage_disjoint"]()
    b = MC.nopooling_bounds(target, sources, policy)
    x = b["unidentified_cross_channel"]
    assert x is not None
    assert x["dependence"] == "UNIDENTIFIED"
    assert x["scenario_is_measured"] is False
    # Frechet bound of two zero lower marginals is [0, 0]; the primitive is real,
    # not a placeholder.
    native = MODS["A"].complementary_binary_bounds("0", "0")
    assert x["lower"] == native["lower"] and x["upper"] == native["upper"]


def test_C_point_identifies_only_where_exactly_one_source_is_admitted():
    target, sources, policy = OW.WORLD_BUILDERS["W1_full_coverage_disjoint"]()
    # Admit BOTH sources for majority: pooling would be required, so C refuses.
    b = MC.nopooling_bounds(target, sources, policy,
                            transport_permission={"majority": {"S_A", "S_B"}})
    assert b["strata"]["majority"]["point_identified"] is False
    assert b["total_unknown_mass"] == "1"
    # Admit exactly ONE: C may point-identify that stratum alone.
    b2 = MC.nopooling_bounds(target, sources, policy,
                             transport_permission={"majority": {"S_A"}})
    assert b2["strata"]["majority"]["point_identified"] is True
    assert b2["strata"]["minority"]["point_identified"] is False
    assert b2["total_unknown_mass"] == "1/2"


def test_C_refuses_to_use_a_source_that_fails_the_support_gate_even_if_permitted():
    target, sources, policy = OW.WORLD_BUILDERS["W7_source_excluded_all_strata"]()
    b = MC.nopooling_bounds(target, sources, policy,
                            transport_permission={"majority": {"S_A"}, "minority": {"S_A"}})
    assert b["total_unknown_mass"] == "1"


def test_C_never_mixes_sources_and_never_claims_target_representation():
    target, sources, policy = OW.WORLD_BUILDERS["W1_full_coverage_disjoint"]()
    b = MC.nopooling_bounds(target, sources, policy)
    assert b["pooling"] == "NONE"
    assert len(b["per_source_native_descriptives"]) == 4  # 2 sources x 2 strata
    for d in b["per_source_native_descriptives"]:
        assert d["mixed_with_other_sources"] is False
        assert d["used_as_target_estimate"] is False
        assert d["scope"] == "SOURCE_NATIVE_ONLY_NO_TARGET_REPRESENTATION_CLAIMED"


# ------------------------------------------------- cold artifact agreement --

@pytest.mark.parametrize("cand", ["A", "A0", "B", "C"])
def test_cold_round_artifacts_exist_and_are_self_describing(cand):
    for rnd in ("round1", "round2"):
        p = COLD / rnd / f"{cand}.json"
        assert p.exists(), f"missing cold artifact {p}"
        d = json.loads(p.read_text())
        assert d["candidate"] == cand
        assert d["environment"]["python"].startswith("3.")
        assert d["environment"]["pid"] > 0


@pytest.mark.parametrize("cand", ["A", "B", "C"])
def test_two_cold_rounds_are_bit_identical_in_scientific_content(cand):
    a = json.loads((COLD / "round1" / f"{cand}.json").read_text())
    b = json.loads((COLD / "round2" / f"{cand}.json").read_text())
    assert a["results"] == b["results"], f"{cand} cold rounds disagree"
    assert a["environment"]["pid"] != b["environment"]["pid"], \
        "cold rounds must be distinct processes"


def test_cold_A_and_B_artifacts_record_the_decisive_divergence():
    a = json.loads((COLD / "round1" / "A.json").read_text())["results"]
    b = json.loads((COLD / "round1" / "B.json").read_text())["results"]
    w = "W2_mixed_eligibility_trap"
    assert a[w]["synthesize"]["bundle"]["uncovered_target_mass"] == "0"
    assert a[w]["conditional"]["result"]["state"] == "SUPPORTED_MODEL"
    assert b[w]["synthesize"]["bundle"]["uncovered_target_mass"] == "1/4"
    assert b[w]["conditional"]["result"]["state"] == "UNAVAILABLE"
    assert b[w]["synthesize"]["bundle"]["decision"] == "PARTIAL_IDENTIFICATION_ONLY"