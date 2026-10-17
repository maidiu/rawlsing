"""F6C frozen court. FROZEN AND COMMITTED BEFORE ANY PRODUCER EXECUTION.

Every expected number is read from 01_FROZEN_SOURCEFREE_STUDY_WORLDS.json, which
was committed first. The court physically calls the pinned native producer and the
actual consumer and asserts exact rational values, exact typed errors and exact
identities. It never relaxes admissibility and never reinterprets a missing
category as an observed ZERO.
"""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.dont_write_bytecode = True

from rawlsing_next.pre553_heterogeneous_synthesis import (  # noqa: E402
    synthesize, conditional, complementary_binary_bounds, SynthesisError, METHOD,
)
import rawlsing_next.pre553_heterogeneous_synthesis as PRODUCER  # noqa: E402
from rawlsing_next.pre553_empirical_objects import semantic_hash  # noqa: E402

sys.path.insert(0, str(HERE))
import f6c_worlds as W  # noqa: E402

FROZEN = json.loads((ROOT / "01_FROZEN_SOURCEFREE_STUDY_WORLDS.json").read_text())
CELLS = [tuple(c) for c in FROZEN["shared_structure"]["cells"]]


def run_world_a():
    t, s, p = W.world_a()
    return synthesize(t, s, p)


def run_world_b():
    t, s, p = W.world_b()
    return synthesize(t, s, p)


def dist(bundle):
    return {tuple(c["categories"]): F(c["probability"]) for c in bundle["candidate"]["distribution"]}


def sub(bundle):
    return {tuple(c["categories"]): F(c["probability"])
            for c in bundle["candidate"]["covered_subprobability"]}


def ordered(bundle):
    return [tuple(k) for k in bundle["candidate"]["ordered_categories"]]


# ===========================================================================
# CUSTODY -- the corrected native producer is the one actually imported
# ===========================================================================

def test_custody_imported_module_is_the_corrected_pinned_blob():
    import hashlib
    raw = Path(PRODUCER.__file__).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert blob == "fc5e37fa5b2f0eb689593b42d95479d1327cb94c"
    assert blob != "182cc7970d7624f6614015f5a51d0602e1630d52"
    assert PRODUCER.__file__.endswith("05_NATIVE_STAGE/rawlsing_next/pre553_heterogeneous_synthesis.py")


def test_custody_contract_version_is_the_native_method():
    assert METHOD == "PRE553_TARGET_JOINT_STANDARDIZATION@1"


# ===========================================================================
# DISCRIMINATING NEGATIVE -- the delta that the inherited suite does NOT catch
# ===========================================================================

def test_delta_omitted_native_category_is_refused_as_manufactured_zero():
    """S03F Fix 1 exists ONLY in the corrected blob.

    The inherited 25-test suite passes on BOTH blobs, so it cannot detect this.
    Dropping one native category cell must be refused, never silently zero-filled.
    """
    t, s, p = W.world_a()
    s[0]["strata"]["majority"]["cells"].pop()          # remove the 4th cell
    s[0]["strata"]["majority"]["eligible_n"] = 100     # counts unchanged: hole
    with pytest.raises(SynthesisError) as exc:
        synthesize(t, s, p)
    assert "incomplete native joint domain" in str(exc.value)
    assert "silently manufactured as zero" in str(exc.value)


def test_delta_complete_domain_is_accepted():
    t, s, p = W.world_a()
    assert synthesize(t, s, p)["candidate"] is not None


def test_delta_declared_category_order_is_not_lexically_resorted():
    """S03FO: cell order follows category_map insertion order."""
    t, s, p = W.world_a()
    b = synthesize(t, s, p)
    assert ordered(b) == CELLS
    # make the declared order differ from lexical order and re-check
    t2, s2, p2 = W.world_a()
    for src in s2:
        for ax in src["axes"]:
            ax["category_map"] = dict(reversed(list(ax["category_map"].items())))
            p2["mapping_hashes"][src["source_id"]] = semantic_hash(src["axes"])
    b2 = synthesize(t2, s2, p2)
    assert ordered(b2) == [("insecure", "informal"), ("insecure", "formal"),
                           ("secure", "informal"), ("secure", "formal")]


def test_delta_outcome_as_condition_is_flagged_as_tautology():
    """S03F Fix 2: outcome-as-predicate must not masquerade as predictive."""
    b = run_world_a()
    r = conditional(b, {"employment_position": "formal"}, "employment_position")
    assert r["state"] == "DESCRIPTIVE_SELF_CONDITIONING"
    assert r["self_conditioning_status"] == "OUTCOME_LEAKAGE_TAUTOLOGY"


# ===========================================================================
# WORLD A -- legitimate overlapping-stratum standardization
# ===========================================================================

def test_world_a_frozen_standardized_joint_exact():
    b = run_world_a()
    exp = FROZEN["world_A"]["frozen_expected_native_standardized_joint"]
    assert [dist(b)[k] for k in CELLS] == [F(x) for x in exp]


def test_world_a_standardization_beats_naive_pooled_mixture():
    exp = FROZEN["world_A"]["frozen_expected_comparison"]
    truth = [F(x) for x in
             FROZEN["world_A"]["independent_expected_target_estimand"]["ground_truth_joint"]]
    t, s, p = W.world_a()
    naive = [F(x) for x in W.naive_pooled_mixture(s)]
    assert [str(x) for x in naive] == FROZEN["world_A"]["frozen_expected_naive_pooled_mixture"]
    std = [dist(run_world_a())[k] for k in CELLS]
    l1_naive = sum(abs(a - b) for a, b in zip(naive, truth))
    l1_std = sum(abs(a - b) for a, b in zip(std, truth))
    assert l1_naive == F(exp["naive_mixture_L1_error_vs_truth"])
    assert l1_std == F(exp["standardized_L1_error_vs_truth"])
    assert l1_std < l1_naive, "standardization must improve target prediction here"


def test_world_a_target_conditional_beats_naive_conditional():
    exp = FROZEN["world_A"]["frozen_expected_comparison"]
    b = run_world_a()
    r = conditional(b, {"material_security": "secure"}, "employment_position")
    assert F(r["probabilities"]["formal"]) == F(exp["standardized_P_formal_given_secure"])
    t, s, p = W.world_a()
    naive = [F(x) for x in W.naive_pooled_mixture(s)]
    naive_p = naive[0] / (naive[0] + naive[1])
    assert naive_p == F(exp["naive_P_formal_given_secure"])
    assert F(r["probabilities"]["formal"]) != naive_p


def test_world_a_consumer_state_is_supported_model():
    b = run_world_a()
    r = conditional(b, {"material_security": "secure"}, "employment_position")
    assert r["state"] == "SUPPORTED_MODEL"
    assert r["evidence_mode"] == "INFERRED"
    assert r["observed_denominator"] is None
    assert r["uncertainty"] == "CONDITIONAL_UNCERTAINTY_NOT_IDENTIFIED"
    assert sum(F(v) for v in r["probabilities"].values()) == 1


def test_world_a_minority_stratum_is_preserved_not_pruned():
    b = run_world_a()
    sup = b["candidate"]["support"]
    assert F(sup["minority"]["target_share"]) == F(
        FROZEN["world_A"]["frozen_minority_preservation"]["target_share"])
    assert all(v > 0 for v in dist(b).values()), "no cell may be pruned"
    for src, sid in ((0, "A"), (1, "B")):
        want = FROZEN["world_A"]["frozen_minority_preservation"][f"source_{sid}_minority_cells"]
        got = [c["n"] for c in b["baseline"][sid]["native_summary"]["strata"]["minority"]["cells"]]
        assert got == want, sid


def test_world_a_native_joint_and_identities_preserved():
    t, s, p = W.world_a()
    b = run_world_a()
    for original, result in zip(sorted(s, key=lambda x: x["source_id"]), b["baseline"]):
        assert result["native_summary"] == original
        assert result["input_hash"] == semantic_hash(original)
    assert b["candidate"]["sample_size"] is None
    assert b["candidate"]["dependence"] == \
        "SOURCE_JOINTS_TRANSPORTED_AND_MIXED; NO_CROSS_SURVEY_RESPONDENT_LINKS"
    assert b["contract_version"] == METHOD
    assert b["consumer_requirements_ref"] == "S03_CONSUMER_REQUIREMENTS@1"
    assert b["decision"] == "SYNTHETIC_CANDIDATE"
    assert b["real_source_qualification"] == "EXTERNAL_REVIEW_REQUIRED"


def test_world_a_replay_hash_is_stable_and_content_bound():
    b1, b2 = run_world_a(), run_world_a()
    assert b1["content_hash"] == b2["content_hash"]
    b1["candidate"]["distribution"][0]["probability"] = "1/2"
    assert b1["content_hash"] != run_world_a()["content_hash"]


# ===========================================================================
# WORLD B -- positivity violation: honest bounds, not a false point
# ===========================================================================

def test_world_b_no_false_point_distribution():
    b = run_world_b()
    assert b["candidate"]["distribution"] is None
    assert F(b["candidate"]["uncovered_target_mass"]) == F(
        FROZEN["world_B"]["frozen_expected_uncovered_target_mass"])


def test_world_b_covered_subprobability_exact():
    b = run_world_b()
    exp = FROZEN["world_B"]["frozen_expected_covered_subprobability"]
    assert [sub(b)[k] for k in CELLS] == [F(x) for x in exp]
    assert sum(sub(b).values()) == F(4, 5)


def test_world_b_consumer_refuses_rather_than_fabricating():
    b = run_world_b()
    r = conditional(b, {"material_security": "secure"}, "employment_position")
    assert r["state"] == FROZEN["world_B"]["expected_consumer_state"]
    assert r["reason"] == FROZEN["world_B"]["expected_consumer_reason"]
    assert "probabilities" not in r


def test_world_b_source_disagreement_bounds_exact():
    b = run_world_b()
    exp = FROZEN["world_B"]["frozen_expected_source_disagreement_bounds"]
    rows = {tuple(r["categories"]): (F(r["lower"]), F(r["upper"]))
            for r in b["candidate"]["uncertainty"]["source_disagreement_and_uncovered_bounds"]}
    for k in CELLS:
        assert rows[k] == (F(exp[k[0] + "_" + k[1]]["lower"]),
                           F(exp[k[0] + "_" + k[1]]["upper"])), k


def test_world_b_bias_sensitivity_bounds_exact():
    b = run_world_b()
    exp = FROZEN["world_B"]["frozen_expected_bias_sensitivity_bounds"]
    rows = {tuple(r["categories"]): (F(r["lower"]), F(r["upper"]))
            for r in b["candidate"]["uncertainty"]["bias_sensitivity_bounds"]}
    for k in CELLS:
        assert rows[k] == (F(exp[k[0] + "_" + k[1]]["lower"]),
                           F(exp[k[0] + "_" + k[1]]["upper"])), k
    radii = b["candidate"]["uncertainty"]["radii"]
    assert sum(F(v) for v in radii.values()) == F(exp["radius_sum"])


def test_world_b_envelopes_are_declared_not_confidence_intervals():
    b = run_world_b()
    u = b["candidate"]["uncertainty"]
    assert "Sensitivity envelopes are not confidence intervals" in u["limitations"]
    blob = json.dumps(b)
    for banned in ("confidence_interval", "ci_lower", "ci_upper", "confidence_interval_ref"):
        assert banned not in blob


def test_world_b_complementary_binary_bounds_exact_and_unidentified():
    exp = FROZEN["world_B"]["frozen_expected_complementary_binary_bounds"]
    r = complementary_binary_bounds(exp["arguments"]["p"], exp["arguments"]["q"])
    assert r["lower"] == exp["lower"]
    assert r["upper"] == exp["upper"]
    assert r["independence_scenario"] == exp["independence_scenario"]
    assert r["scenario_is_measured"] is False
    assert r["dependence"] == "UNIDENTIFIED"


def test_world_b_minority_stays_visible_despite_missing_full_joint():
    b = run_world_b()
    sup = b["candidate"]["support"]
    assert F(sup["minority"]["target_share"]) == F(
        FROZEN["world_B"]["frozen_minority_preservation"]["target_share"])
    assert sub(b)[("insecure", "informal")] > 0
    for sid in ("A", "B"):
        want = FROZEN["world_B"]["frozen_minority_preservation"][f"source_{sid}_minority_cells"]
        got = [c["n"] for c in b["baseline"][sid]["native_summary"]["strata"]["minority"]["cells"]]
        assert got == want


# ===========================================================================
# SOURCE-SPECIFIC FIELD VARIATION -> intended world option changes, others do not
# ===========================================================================

def test_source_specific_field_alone_changes_intended_option_only():
    """Vary only source-B geography; intended option changes, A untouched."""
    t, s, p = W.world_a()
    before = synthesize(t, s, p)
    t2, s2, p2 = W.world_a()
    s2[1]["scope"]["geography"] = "Synthetic Region B"
    after = synthesize(t2, s2, p2)
    assert after["refusals"]["B"] == ["TARGET_SCOPE_MISMATCH"]
    assert after["baseline"][0]["native_summary"] == before["baseline"][0]["native_summary"]
    assert after["candidate"] is None
    assert before["candidate"] is not None
    assert after["decision"] == "SOURCE_INDEXED_BACKOFF"


# ===========================================================================
# NEGATIVES -- each must refuse or back off, never fabricate
# ===========================================================================

def test_negative_wrong_denominator_refused():
    t, s, p = W.world_a()
    s[0]["strata"]["majority"]["eligible_n"] = 999
    with pytest.raises(SynthesisError) as e:
        synthesize(t, s, p)
    assert "conservation failed" in str(e.value)


def test_negative_exclusion_count_negative_refused():
    t, s, p = W.world_a()
    s[0]["strata"]["majority"]["excluded_n"] = -1
    with pytest.raises(SynthesisError):
        synthesize(t, s, p)


def test_negative_proxy_as_measured_independent_marginals_refused():
    t, s, p = W.world_a()
    s[0]["dependence_kind"] = "INDEPENDENT_MARGINALS"
    with pytest.raises(SynthesisError) as e:
        synthesize(t, s, p)
    assert "cannot claim measured joint" in str(e.value)


def test_negative_suppressed_table_status_refused():
    t, s, p = W.world_a()
    s[0]["strata"]["majority"]["table_status"] = "SUPPRESSED"
    with pytest.raises(SynthesisError) as e:
        synthesize(t, s, p)
    assert "cannot be treated as zeros" in str(e.value)


def test_negative_unweighted_mass_must_equal_raw_count():
    t, s, p = W.world_a()
    s[0]["strata"]["majority"]["cells"][0]["mass"] = 63
    with pytest.raises(SynthesisError) as e:
        synthesize(t, s, p)
    assert "unweighted mass must equal raw count" in str(e.value)


def test_negative_float_numeric_input_refused():
    t, s, p = W.world_a()
    s[0]["strata"]["majority"]["cells"][0]["mass"] = 64.0
    with pytest.raises(SynthesisError) as e:
        synthesize(t, s, p)
    assert "integers or rational strings" in str(e.value)


def test_negative_missing_target_id_is_keyerror_free_typed():
    t, s, p = W.world_a()
    del t["target_id"]
    with pytest.raises(KeyError):
        synthesize(t, s, p)


def test_negative_target_shares_must_sum_to_one():
    t, s, p = W.world_a()
    t["strata"] = {"majority": "4/5", "minority": "2/5"}
    with pytest.raises(SynthesisError) as e:
        synthesize(t, s, p)
    assert "must sum to one" in str(e.value)


def test_negative_source_grain_unit_mismatch_backs_off():
    t, s, p = W.world_a()
    s[0]["scope"]["unit"] = "household"
    b = synthesize(t, s, p)
    assert b["candidate"] is None
    assert "TARGET_SCOPE_MISMATCH" in b["refusals"]["A"]


def test_negative_geography_mismatch_backs_off():
    t, s, p = W.world_a()
    s[1]["scope"]["geography"] = "Elsewhere"
    b = synthesize(t, s, p)
    assert b["candidate"] is None
    assert "TARGET_SCOPE_MISMATCH" in b["refusals"]["B"]


def test_negative_boundary_mismatch_backs_off():
    t, s, p = W.world_a()
    s[0]["scope"]["boundary_ref"] = "other-boundary@1"
    b = synthesize(t, s, p)
    assert "TARGET_SCOPE_MISMATCH" in b["refusals"]["A"]


def test_negative_time_outside_clock_backs_off():
    t, s, p = W.world_a()
    t["year"] = 2013
    b = synthesize(t, s, p)
    assert b["candidate"] is None
    assert "TIME_NOT_APPLICABLE" in b["refusals"]["A"]
    assert "TIME_NOT_APPLICABLE" in b["refusals"]["B"]


def test_negative_false_overlap_claim_backs_off():
    t, s, p = W.world_a()
    p["overlap_reviews"] = {}
    b = synthesize(t, s, p)
    assert b["candidate"] is None
    assert b["overlap_diagnostics"][0]["reason"] == "OVERLAP_UNRESOLVED"
    assert b["decision"] == "SOURCE_INDEXED_BACKOFF"


def test_negative_overlap_review_without_review_ref_backs_off():
    t, s, p = W.world_a()
    p["overlap_reviews"]["A|B"] = {"status": "DISJOINT"}
    b = synthesize(t, s, p)
    assert b["overlap_diagnostics"][0]["reason"] == "OVERLAP_UNRESOLVED"


def test_negative_duplicate_sample_detected_despite_distinct_labels():
    t, s, p = W.world_a()
    s[1]["sample_id"] = s[0]["sample_id"]
    s[1]["survey_lineage"] = s[0]["survey_lineage"]
    b = synthesize(t, s, p)
    assert b["overlap_diagnostics"][0]["reason"] == "DUPLICATE_SAMPLE"
    assert b["candidate"] is None


def test_negative_zero_weight_contribution_refused():
    t, s, p = W.world_a()
    p["source_weights"]["A"] = 0
    with pytest.raises(SynthesisError) as e:
        synthesize(t, s, p)
    assert "remove a contribution explicitly" in str(e.value)


def test_negative_weights_must_name_every_source():
    t, s, p = W.world_a()
    del p["source_weights"]["B"]
    with pytest.raises(SynthesisError) as e:
        synthesize(t, s, p)
    assert "exactly name contributions" in str(e.value)


def test_negative_version_mapping_preimage_mismatch_backs_off():
    t, s, p = W.world_a()
    s[0]["axes"][0]["scale_ref"] = "wrong-version@9"
    b = synthesize(t, s, p)
    assert b["candidate"] is None
    assert b["baseline"][0]["mapped_joint"] is None
    assert "MAPPING_REVIEW_PREIMAGE_MISMATCH" in b["refusals"]["A"]


def test_negative_unqualified_mapping_keeps_native_only():
    t, s, p = W.world_a()
    s[0]["axes"][0]["mapping_confidence"] = "LOW"
    b = synthesize(t, s, p)
    assert b["baseline"][0]["mapped_joint"] is None
    assert b["baseline"][0]["native_summary"] == s[0]
    assert b["candidate"] is None


def test_negative_blocked_scale_status_backs_off():
    t, s, p = W.world_a()
    s[0]["axes"][0]["scale_status"] = "BLOCKED"
    b = synthesize(t, s, p)
    assert "SCALE_OR_POLARITY_UNQUALIFIED" in b["refusals"]["A"]


def test_negative_empty_source_support_refused():
    t, s, p = W.world_a()
    s[0]["strata"] = {}
    with pytest.raises(SynthesisError) as e:
        synthesize(t, s, p)
    assert "empty source support" in str(e.value)


def test_negative_empty_source_list_refused():
    t, s, p = W.world_a()
    with pytest.raises(SynthesisError) as e:
        synthesize(t, [], p)
    assert "empty or duplicate source IDs" in str(e.value)


def test_negative_duplicate_source_id_refused():
    t, s, p = W.world_a()
    s.append(deepcopy(s[0]))
    with pytest.raises(SynthesisError):
        synthesize(t, s, p)


def test_negative_complementary_constructs_back_off():
    t, s, p = W.world_a()
    s[1]["axes"][0]["construct_ref"] = "life_satisfaction"
    b = synthesize(t, s, p)
    assert b["candidate"] is None
    assert "NO_COMMON_JOINT_ESTIMAND_KEEP_COMPLEMENTARY_CHANNELS" in b["refusals"]["B"]


def test_negative_hidden_nonmodal_design_variance_coverage_refused():
    t, s, p = W.world_a()
    s[0]["strata"]["majority"]["design_variance"]["cells"].pop()
    with pytest.raises(SynthesisError) as e:
        synthesize(t, s, p)
    assert "design variance coverage must match mapped joint" in str(e.value)


def test_negative_missing_design_variance_yields_unknown_not_fabricated():
    t, s, p = W.world_a()
    del s[0]["strata"]["majority"]["design_variance"]
    b = synthesize(t, s, p)
    u = b["candidate"]["uncertainty"]
    assert u["sampling_variance"] is None
    assert u["sampling_status"] == "UNKNOWN_DESIGN"


def test_negative_real_source_without_admission_refused():
    t, s, p = W.world_a()
    s[0]["test_origin"] = False
    with pytest.raises(SynthesisError) as e:
        synthesize(t, s, p)
    assert "lacks external owner admission" in str(e.value)


def test_negative_real_source_admission_is_not_a_grant_itself():
    """An admit callback returning True only reaches baseline; transport still reviewed."""
    t, s, p = W.world_a()
    for src in s:
        src["test_origin"] = False
    b = synthesize(t, s, p, admit=lambda source, target, operation: True)
    assert b["test_origin"] is False
    assert b["candidate"] is None
    assert "TRANSPORT_PERMISSION_NOT_ADMITTED" in b["refusals"]["A"]
    assert b["real_source_qualification"] == "EXTERNAL_REVIEW_REQUIRED"


def test_negative_conditional_outside_topology_refused():
    b = run_world_a()
    with pytest.raises(SynthesisError) as e:
        conditional(b, {"not_a_construct": "x"}, "employment_position")
    assert "outside common joint topology" in str(e.value)


def test_negative_conditional_category_outside_support_unavailable():
    b = run_world_a()
    r = conditional(b, {"material_security": "nonexistent"}, "employment_position")
    assert r["state"] == "UNAVAILABLE"
    assert r["reason"] == "CATEGORY_OUTSIDE_MAPPED_SUPPORT"


def test_negative_consumer_rejects_mutated_bundle():
    b = run_world_a()
    b["candidate"]["distribution"][0]["probability"] = "1/2"
    with pytest.raises(SynthesisError) as e:
        conditional(b, {"material_security": "secure"}, "employment_position")
    assert "bundle replay hash mismatch" in str(e.value)


def test_negative_joint_budget_keeps_frontier_visible():
    t, s, p = W.world_a()
    p["maximum_joint_cells"] = 1
    b = synthesize(t, s, p)
    assert b["candidate"] is None
    assert "JOINT_DOMAIN_EXCEEDS_BUDGET" in b["refusals"]["A"]


def test_negative_support_threshold_is_diagnostic_not_pruning():
    t, s, p = W.world_a()
    p["minimum_raw_support"] = 1000
    b = synthesize(t, s, p)
    assert b["candidate"]["distribution"] is None
    assert b["candidate"]["uncovered_target_mass"] == "1"
    for sid in ("A", "B"):
        cells = b["baseline"][sid]["native_summary"]["strata"]["majority"]["cells"]
        assert len(cells) == 4, "native cells must survive a support threshold"


def test_negative_duplicate_joint_cell_refused():
    t, s, p = W.world_a()
    cells = s[0]["strata"]["majority"]["cells"]
    cells[1]["categories"] = list(cells[0]["categories"])
    with pytest.raises(SynthesisError) as e:
        synthesize(t, s, p)
    assert "duplicate or malformed joint cell" in str(e.value)


def test_negative_unmapped_native_category_refused():
    t, s, p = W.world_a()
    s[0]["strata"]["majority"]["cells"][0]["categories"] = ["ZZZ", "formal"]
    with pytest.raises(SynthesisError) as e:
        synthesize(t, s, p)
    assert "unmapped native category" in str(e.value)
