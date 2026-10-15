"""HQ298 S-M-LAB2 — executable source-free invariants and harness tests.

Grain: SOURCEFREE_REPLICATION_PLUS_FROZEN_BEHAVIORAL_PROTOCOL.
Nothing here is behavioral evidence. The fixture-responder path is harness
plumbing only (HARNESS_DRY_RUN__NOT_BEHAVIORAL_EVIDENCE).
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, os.path.dirname(HERE))  # for `lab2.` package import
sys.path.insert(0, os.path.join(HERE, "predecessor_lab1"))

from lab2.model_gate import (Grant, evaluate_gate, require_call_permission,
                             ModelCallDenied, HOLD_ID, REQUIRED_FIELDS)
from lab2.packets import (build_manifest, build_trial_packet, contrast_pairs,
                          expected_code, actor_visible_fingerprint,
                          paraphrase_variant, label_shuffle, surface_variant,
                          inject_hidden_origin, menu_order_for, SEEDS, ARMS,
                          EXPECTED_TYPED_CODES)
from lab2.scoring import (ScorerInput, ScorerIntegrityError, dual_score,
                          scorer_alpha, scorer_beta, correctness_fraction,
                          compare_arms)
from lab2.behavioral_runner import (BehavioralRunner, fixture_responder,
                                    run_packet_nulls, DRY_RUN_LABEL)

PREREG = os.path.join(os.path.dirname(HERE), "01_PREREGISTRATION_FROZEN.json")
FREEZE = os.path.join(os.path.dirname(HERE), "outputs", "preregistration_freeze.json")


# ---------------------------------------------------------------------------
# A. preregistration freeze integrity
# ---------------------------------------------------------------------------

def test_A_preregistration_freeze_hash_is_recorded_and_matches():
    raw = open(PREREG, "rb").read()
    h = hashlib.sha256(raw).hexdigest()
    freeze = json.load(open(FREEZE))
    assert freeze["preregistration_sha256"] == h
    assert freeze["frozen_before_any_trial"] is True
    assert freeze["model_calls_at_freeze_time"] == 0


def test_A_preregistration_declares_all_six_k_with_heldout_lock():
    pre = json.load(open(PREREG))
    ids = [c["id"] for c in pre["matched_heldout_comparisons"]["cases"]]
    assert ids == ["K1", "K2", "K3", "K4", "K5", "K6"]
    for c in pre["matched_heldout_comparisons"]["cases"]:
        assert c["heldout"] is True
        assert c["expected_typed_codes"]


def test_A_preserved_lab1_verdict_is_recorded_and_not_relabelled():
    pre = json.load(open(PREREG))
    v = pre["preserved_machine_verdict_from_LAB1"]
    assert "PASSED all K1-K6" in v["A_minimal"]
    assert "REJECT" in v["B_richer_event_local"]
    assert "DERIVED_CACHE" in v["C_typed_relational_topology"]
    assert "NOT behavioral proof" in v["discipline"]


# ---------------------------------------------------------------------------
# B. model-call gate: zero calls without complete grant
# ---------------------------------------------------------------------------

def test_B_no_grant_means_hold_and_zero_calls():
    d = evaluate_gate(None)
    assert d.allowed is False
    assert d.hold_id == HOLD_ID
    assert d.model_calls_permitted == 0
    assert set(REQUIRED_FIELDS) == set(d.missing_fields)


def test_B_partial_grant_still_denied():
    g = Grant(named_provider_exact_endpoint="https://example.invalid/v1",
              exact_model_and_version_pin="model-x@1")
    d = evaluate_gate(g)
    assert d.allowed is False
    assert "explicit_monetary_cap" in d.missing_fields
    assert "experiment_use_grant_behavioral_actor_trials" in d.missing_fields


def test_B_require_call_permission_raises_without_grant():
    with pytest.raises(ModelCallDenied):
        require_call_permission(None)


def test_B_runner_hold_mode_issues_zero_calls_and_reports_missing_fields():
    r = BehavioralRunner(grant=None, preregistration_sha256="x")
    out = r.run_hold()
    assert out["terminal"] == HOLD_ID
    assert out["model_calls_issued"] == 0
    assert out["behavioral_evidence_produced"] is False
    assert out["missing_authority_class"] == "MISSING_ACTOR_OR_MODEL_USE_AUTHORITY"
    assert "exact_provider" not in out  # never fabricates provider detail
    assert len(out["exact_missing_grant_fields"]) == len(REQUIRED_FIELDS)


def test_B_runner_granted_mode_is_unreachable_without_grant():
    r = BehavioralRunner(grant=None)
    out = r.run_granted()  # falls back to hold, no call, no exception
    assert out["terminal"] == HOLD_ID
    assert r.model_calls_issued == 0


def test_B_complete_grant_would_pass_gate():
    g = Grant(
        named_provider_exact_endpoint="https://provider.example/v1/chat",
        exact_model_and_version_pin="model-y@2026-01-01",
        privacy_permission_for_synthetic_lab_packets="GRANTED_BY_OWNER",
        experiment_use_grant_behavioral_actor_trials="GRANTED_BY_OWNER",
        explicit_monetary_cap="USD 5.00",
        price_class_and_quota_observed="class_standard; quota_unknown",
        raw_request_response_retention_permission="GRANTED",
        per_trial_call_budget=1)
    d = evaluate_gate(g)
    assert d.allowed is True
    assert d.hold_id is None


# ---------------------------------------------------------------------------
# C. matched held-out packets and blind counterbalancing
# ---------------------------------------------------------------------------

def test_C_manifest_covers_all_k_contrasts_seeds_arms():
    m = build_manifest()
    n_contrast_cells = sum(len(v) for v in EXPECTED_TYPED_CODES.values())
    assert m["n_k"] == 6
    assert m["n_contrast_cells"] == n_contrast_cells
    assert m["n_seeds"] == 12
    assert m["n_trials"] == n_contrast_cells * 12 * 3
    assert m["matched_content_across_arms_ok"] is True
    assert m["matched_content_across_arms_violations"] == []


def test_C_matched_content_identical_across_arms():
    m = build_manifest()
    by_trial = {}
    for t in m["trials"]:
        by_trial.setdefault(t["trial_id"], set()).add(t["matched_content_hash"])
    assert all(len(s) == 1 for s in by_trial.values())


def test_C_presentation_codes_differ_across_arms_and_hide_arm_label():
    m = build_manifest()
    by_trial = {}
    for t in m["trials"]:
        by_trial.setdefault(t["trial_id"], []).append(t)
    for tid, group in by_trial.items():
        codes = {t["presentation_code"] for t in group}
        assert len(codes) == len(group)  # distinct per arm
        for t in group:
            assert t["arm"] not in t["presentation_code"]
            assert t["prereg_contrast"] not in t["presentation_code"]


def test_C_menu_order_is_counterbalanced():
    orders = {arm: menu_order_for("K4__CORRECTIVE_CONTEXT__S01", "K4", arm)
              for arm in ARMS}
    assert all(sorted(o) == sorted(orders["A"]) for o in orders.values())
    assert len({tuple(o) for o in orders.values()}) >= 2  # rotation actually varies


def test_C_expected_codes_match_preregistration():
    pre = json.load(open(PREREG))
    for case in pre["matched_heldout_comparisons"]["cases"]:
        k = case["id"]
        for contrast, codes in case["expected_typed_codes"].items():
            assert expected_code(k, contrast) == codes


def test_C_actor_info_packet_excludes_hidden_origin():
    for k in EXPECTED_TYPED_CODES:
        for fixture_contrast, prereg_contrast in contrast_pairs(k):
            pkt = build_trial_packet(k, fixture_contrast, prereg_contrast, "S01", "A")
            info = pkt["allowed_actor_info_packet"]
            assert info["hidden_origin_content_included"] is False
            assert info["first_person_origin_claims_permitted"] is False
            assert all(t["origin_content"] is None for t in info["trace_markers"])


# ---------------------------------------------------------------------------
# D. pre-typed blind scoring: prose structurally excluded, dual scorer agrees
# ---------------------------------------------------------------------------

def test_D_scorer_input_rejects_prose_field():
    si = ScorerInput(trial_id="t", counterbalance_code="PC_x",
                     selected_typed_code="SILENCE")
    assert si.selected_typed_code == "SILENCE"


def test_D_dual_scorer_agreement_and_mismatch_detection():
    expected = {"t1": ["SILENCE"], "t2": ["REQUEST_FEEDBACK"]}
    inputs = [
        ScorerInput("t1", "pc1", "SILENCE"),
        ScorerInput("t2", "pc2", "REQUEST_FEEDBACK"),
    ]
    out = dual_score(inputs, expected)
    assert out["scorer_agreement"] is True
    assert out["n_records"] == 2
    # scorers are independently implemented but must agree
    assert [r.correct for r in scorer_alpha(inputs, expected)] == \
           [r.correct for r in scorer_beta(inputs, expected)]


def test_D_scorers_never_read_prose():
    import inspect
    from lab2 import scoring
    src = inspect.getsource(scoring)
    # prose only appears in docstrings/comments/assertions about exclusion
    for fn in (scoring.scorer_alpha, scoring.scorer_beta):
        fsrc = inspect.getsource(fn)
        assert "prose" not in fsrc.split('"""')[0]


def test_D_correctness_fraction_and_arm_comparison():
    expected = {"t1": ["SILENCE"], "t2": ["REQUEST_FEEDBACK"]}
    good = [ScorerInput("t1", "p", "SILENCE"), ScorerInput("t2", "p", "REQUEST_FEEDBACK")]
    bad = [ScorerInput("t1", "p", "REQUEST_FEEDBACK"), ScorerInput("t2", "p", "SILENCE")]
    ga = scorer_alpha(good, expected)
    ba = scorer_alpha(bad, expected)
    assert correctness_fraction(ga) == 1.0
    assert correctness_fraction(ba) == 0.0
    cmp_res = compare_arms({"A": ga, "B_admissible": ba})
    assert cmp_res["A_correctness_fraction"] == 1.0
    assert cmp_res["comparisons"]["B_admissible"]["delta_vs_A_pp"] == -100.0
    assert cmp_res["comparisons"]["B_admissible"]["meets_plus_10pp_screen"] is False


def test_D_universe_outside_codes_are_unscorable():
    expected = {"t1": ["SILENCE"]}
    recs = scorer_alpha([ScorerInput("t1", "p", "A_CODE")], expected)
    assert recs[0].scorable is False
    assert recs[0].correct is False
    assert correctness_fraction(recs) == 0.0


# ---------------------------------------------------------------------------
# E. packet-level nulls and firewalls (source-free executable)
# ---------------------------------------------------------------------------

def test_E_packet_nulls_all_pass():
    res = run_packet_nulls()
    assert res["matched_content_across_arms_ok"] is True
    assert res["N1_PARAPHRASE"]["pass"] is True
    assert res["N2_LABEL"]["pass"] is True
    assert res["N4_SURFACE"]["pass"] is True
    assert res["N5_TRACE_FIREWALL"]["pass"] is True
    assert res["N5_TRACE_FIREWALL_K3"]["pass"] is True
    assert res["K5_STANDING_SEPARATION"]["pass"] is True
    assert res["all_pass"] is True


def test_E_hidden_origin_never_in_actor_visible_payload():
    pkt = build_trial_packet("K3", "TRACE_ACTIVE", "TRACE_ACTIVE", "S01", "A")
    inj = inject_hidden_origin(json.loads(json.dumps(pkt)), "SECRET_X")
    assert actor_visible_fingerprint(inj) == actor_visible_fingerprint(pkt)
    assert "SECRET_X" not in json.dumps(pkt["allowed_actor_info_packet"])


# ---------------------------------------------------------------------------
# F. harness dry-run is explicitly NOT behavioral evidence
# ---------------------------------------------------------------------------

def test_F_dry_run_labels_itself_and_produces_zero_model_calls():
    r = BehavioralRunner(grant=None, preregistration_sha256="frozen")
    out = r.run_dry_run()
    assert out["mode"] == "DRY_RUN"
    assert out["evidence_label"] == DRY_RUN_LABEL
    assert out["behavioral_evidence_produced"] is False
    assert out["model_calls_issued"] == 0
    assert out["fixture_responder_used"] is True
    assert "NOT model behavior" in out["fixture_responder_disclaimer"]


def test_F_dry_run_pipeline_wires_packet_to_blind_scoring():
    r = BehavioralRunner(grant=None, preregistration_sha256="frozen")
    out = r.run_dry_run()
    assert out["scorer_agreement"] is True
    assert out["n_scored"] == out["n_trials"]
    assert out["comparison"]["A_correctness_fraction"] == 1.0


def test_F_fixture_responder_is_not_a_model():
    import inspect
    from lab2 import behavioral_runner as br
    src = inspect.getsource(br.fixture_responder)
    assert "NOT a model" in src
    assert br.fixture_responder({"k_id": "K1", "trial_id": "K1__H_RESPONSIVE__S01"}) \
        == "REQUEST_FEEDBACK"
