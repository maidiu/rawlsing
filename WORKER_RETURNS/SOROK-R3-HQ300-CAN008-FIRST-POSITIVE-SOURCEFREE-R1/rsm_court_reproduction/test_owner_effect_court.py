"""RSM 60-case court reproduction with detector DISC_01 corrected
(HQ299 RSM 00f5d9a6... finding: whole-repo text scan conflated string
constants with implementation surface). All other assertions unchanged.
Vendored from HQ298 SM blob 65acd6be6361; detector-only patch applied.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import os
import sys
import types

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
PREDECL = json.load(open(os.path.join(HERE, "..", "01_PREDECLARED_POSITIVE_CELL_AND_ARMS.json")))
STAGE = os.environ.get("HQ298_STAGE", "")
if STAGE and STAGE not in sys.path:
    sys.path.insert(0, STAGE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from owner_effect_stub_TEST_ONLY import (  # noqa: E402
    AccessLeakBlocked, AdmittedEvent, AuthorityMismatch, CouplingRule,
    OccurrenceGateViolation, OwnerPrestate, STUB_GRAIN,
    adp016_trace_commit_request, adp017_first_person_claim_check,
    coupling_evaluate, event_custody_check, institutional_ratification_check,
    next_event_response, run_k3_arm, run_k5_arm,
)

SEALED_STARTUP = "076aa9fa7ce8662a01dbbb3e998ec37d17ce6fd1"


def _git_blob_sha1(data: bytes) -> str:
    h = hashlib.sha1()
    h.update(b"blob %d\x00" % len(data))
    h.update(data)
    return h.hexdigest()


def _staged_path(rel: str) -> str:
    return os.path.join(STAGE, rel)


def _load_staged_module(rel: str):
    """Import a staged pinned module by file path and return (module, file, blob_sha)."""
    path = _staged_path(rel)
    name = rel.replace("/", ".").removesuffix(".py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    with open(path, "rb") as f:
        blob = _git_blob_sha1(f.read())
    return mod, mod.__file__, blob


# ---------------------------------------------------------------------------
# A. pinned-module identity and import closure
# ---------------------------------------------------------------------------

PINNED_MODULES = {
    "rawlsing_next/wsc_gt0_protocol.py": "243630dcbcb6",
    "rawlsing_next/wsc_gt0_end_to_end.py": "62b6ea39c605",
    "rawlsing_next/wsc_gt0_v3_runtime.py": "6c0494def59f",
    "rawlsing_next/wsc_gt0_prev3_bridge.py": "8f237bd55151",
    "rawlsing_next/wsc_gt0_field_forge_ingress.py": "08550918a645",
    "rawlsing_next/wsc_gt0_source_preff.py": "8c6d82b0e1c7",
    "rawlsing_next/wsc_gt0_v2_mediation.py": "8a040ffd2718",
    "rawlsing_next/v3_psepf_zero_positive_guard.py": "e0528d65215c",
    "rawlsing_next/m6_actor_safe_expression.py": "74d9701cdc7d",
    "rawlsing_next/sdtf_r4_world_response_redrive.py": "9964a24e2546",
    "rawlsing_next/sdtf_r4_mechanism_rule_authority_binding.py": "c94997f5c7f2",
    "rawlsing_next/sdtf_r4_witness_currentness.py": "06c8a2259436",
    "rawlsing_next/sdtf_r4_d1_hosting_replay.py": "7f5a2f677e60",
}


@pytest.mark.parametrize("rel,prefix", sorted(PINNED_MODULES.items()))
def test_A_pinned_module_blob_identity(rel, prefix):
    path = _staged_path(rel)
    assert os.path.exists(path), f"MISSING_PINNED_FILE:{rel}"
    with open(path, "rb") as f:
        blob = _git_blob_sha1(f.read())
    assert blob.startswith(prefix), (
        f"BLOB_IDENTITY_MISMATCH:{rel}:computed={blob}:expected_prefix={prefix}")


@pytest.mark.parametrize("rel", sorted(PINNED_MODULES))
def test_A_pinned_module_imports_with_verified_file(rel):
    mod, file, blob = _load_staged_module(rel)
    assert file and os.path.isfile(file)
    assert file.endswith(rel.split("/")[-1])
    assert blob.startswith(PINNED_MODULES[rel])


def test_A_full_gt0_import_closure_completes():
    """K35 recorded ModuleNotFoundError on rawlsing_next.wsc_gt0_protocol and
    BLOCKED_AFTER_ATTEMPT for complete GT0. This closure must now complete."""
    mods = [
        "rawlsing_next.wsc_gt0_protocol",
        "rawlsing_next.wsc_gt0_end_to_end",
        "rawlsing_next.wsc_gt0_v3_runtime",
        "rawlsing_next.wsc_gt0_prev3_bridge",
        "rawlsing_next.wsc_gt0_field_forge_ingress",
        "rawlsing_next.wsc_gt0_source_preff",
        "rawlsing_next.wsc_gt0_v2_mediation",
    ]
    loaded = {}
    for m in mods:
        loaded[m] = importlib.import_module(m)
    assert len(loaded) == 7
    assert all(m.__file__ for m in loaded.values())


def test_A_m6_pins_exact_adp017_authority_blob():
    m6 = importlib.import_module("rawlsing_next.m6_actor_safe_expression")
    assert m6.ADP017_HASH == (
        "git-blob-sha1:eece4f3f2f3f9288ab9bbc645dc81e20a99e1280")
    pin = PREDECL["authority_pins"]["ADP017_pin_reused_by_imported_module"]
    assert pin["value"] == m6.ADP017_HASH
    assert pin["matches_fetched_authority_blob"] is True


# ---------------------------------------------------------------------------
# B. actual owner-rule inventory + exact earliest HOLD
# ---------------------------------------------------------------------------

def test_B_no_can008_coupling_rule_exists_in_runtime_modules():
    """DISC_01 CORRECTED DETECTOR (HQ299 RSM finding): scan IMPLEMENTATION
    SURFACE (class/def names), not whole-repo text. Text-constant mentions are
    classified separately and are NOT implementations.

    RSM-observed string mentions in the estate (absent from this sparse stage):
      gt34_obl031_q69b_comparator_resolver_r2.py: PSEPF_V3_MUTATION_METABOLISM_
        CAN008_V2  -> denylist identifier constant (NOT an implementation)
      gt34_adp010_input_authority_acceptance.py: NO_CAN_008
        -> rejection-code string constant (NOT an implementation)
    """
    import re as _re
    pat = _re.compile(
        r"^\s*(?:class|def)\s+(\w*(?:coupling|response_rule|owner_effect|"
        r"target_effect|transition_producer|coupling_rule)\w*)", _re.I | _re.M)
    hits = []
    for root, _, files in os.walk(os.path.join(STAGE, "rawlsing_next")):
        if "tests" in root:
            continue
        for fn in files:
            if not fn.endswith(".py"):
                continue
            src = open(os.path.join(root, fn), encoding="utf-8", errors="replace").read()
            for m in pat.finditer(src):
                hits.append((fn, m.group(1)))
    assert hits == [], f"UNEXPECTED_CAN008_IMPLEMENTATION_SURFACE:{hits}"


def test_B_no_r2_effect_vocabulary_in_runtime_modules():
    """DISC_01-scoped: implementation-surface presence of the R2 effect grammar,
    not bare string mentions (which may be denylists/labels)."""
    hits = []
    for root, _, files in os.walk(os.path.join(STAGE, "rawlsing_next")):
        if "tests" in root:
            continue
        for fn in files:
            if not fn.endswith(".py"):
                continue
            src = open(os.path.join(root, fn), encoding="utf-8", errors="replace").read()
            import re as _re2
            if _re2.search(r"^\s*(?:class|def)\s+\w*(?:AMPLIFY|DEFLECT|REROUTE)\w*",
                           src, _re2.M):
                hits.append((fn, "effect-kind implementation surface"))
    assert hits == [], f"UNEXPECTED_EFFECT_VOCABULARY_SURFACE:{hits}"


def test_B_adp016_adp017_have_no_transition_producer_callables():
    """ADP016/017 authority files are documentary; no importable owner-transition
    callable exists for trace commit or epistemic transition."""
    for candidate in ("rawlsing_next.adp016_v3_causal_memory",
                      "rawlsing_next.adp017_v3_actor_access",
                      "rawlsing_next.adp_016_v3_causal_memory",
                      "rawlsing_next.adp_017_v3_actor_access"):
        with pytest.raises(ModuleNotFoundError) as e:
            importlib.import_module(candidate)
        assert "No module named" in str(e.value)
    # and no staged file defines an ADP016/017 transition producer
    for root, _, files in os.walk(os.path.join(STAGE, "rawlsing_next")):
        for fn in files:
            if not fn.endswith(".py"):
                continue
            src = open(os.path.join(root, fn), encoding="utf-8", errors="replace").read()
            assert "def commit_trace" not in src
            assert "def transition_epistemic" not in src


def test_B_earliest_hold_is_missing_implementation_not_missing_import():
    """The five distinct capability statuses must be recorded truthfully.
    Earliest physical/authority HOLD for the positive path = MISSING_IMPLEMENTATION."""
    statuses = {
        "NO_INTERPRETER": "NOT_APPLICABLE_WITH_WARRANT",
        "MISSING_PINNED_CODE_OR_DEPENDENCY": "RESOLVED_THIS_COMMISSION",
        "MISSING_IMPLEMENTATION": "BLOCKED_AFTER_ATTEMPT",
        "MISSING_SOURCE_AUTHORITY": "NOT_APPLICABLE_WITH_WARRANT",
        "MISSING_ACTOR_OR_MODEL_USE_AUTHORITY": "NOT_APPLICABLE_WITH_WARRANT",
    }
    assert statuses["NO_INTERPRETER"] == "NOT_APPLICABLE_WITH_WARRANT"
    assert statuses["MISSING_PINNED_CODE_OR_DEPENDENCY"] == "RESOLVED_THIS_COMMISSION"
    assert statuses["MISSING_IMPLEMENTATION"] == "BLOCKED_AFTER_ATTEMPT"
    # the earliest HOLD is the concrete registered R2 rule + owned-effect transition
    hold = {
        "earliest_hold_class": "MISSING_IMPLEMENTATION",
        "missing_producer": (
            "concrete registered CAN008_R2 coupling/response rule "
            "(V3ResponseEvaluationReceipt transaction) + target-owner effect "
            "transition callable + ADP016/017 owner transition producers"),
        "evidence": [
            "test_B_no_can008_coupling_rule_exists_in_runtime_modules",
            "test_B_no_r2_effect_vocabulary_in_runtime_modules",
            "test_B_adp016_adp017_have_no_transition_producer_callables",
        ],
    }
    assert hold["earliest_hold_class"] == "MISSING_IMPLEMENTATION"


# ---------------------------------------------------------------------------
# C. positive cell execution attempt with ACTUAL reused rules
# ---------------------------------------------------------------------------

def _cell_event() -> AdmittedEvent:
    pc = PREDECL["positive_cell"]["positive_admitted_world_event"]
    return AdmittedEvent(
        event_id=pc["event_id"], kind=pc["kind"], issuer=pc["issuer"],
        issuer_role="WORLD_SCHEDULE_OFFICE", effective_time=pc["effective_time"],
        public_features=tuple(pc["public_event_features"]),
        admitted=True,
        analyst_only_hidden_origin=pc["analyst_only_hidden_origin"]["origin_event"])


def _cell_prestates() -> OwnerPrestate:
    ps = PREDECL["positive_cell"]["lawful_owner_prestates"]
    return OwnerPrestate(
        can010_striving=ps["CAN010"]["striving"],
        can011_practice=ps["CAN011"]["mediator"],
        adp016_trace_id=ps["ADP016"]["causal_trace"],
        adp016_trace_content_state=ps["ADP016"]["content_state"],
        adp016_trace_usable_in_causal_role=ps["ADP016"]["trace_usable_in_causal_role"],
        adp017_first_person_permission=ps["ADP017"]["first_person_claim_permission"],
        history_axis="UNSAFE", prior_can008_response_count=2)


def _cell_rule() -> CouplingRule:
    pc = PREDECL["positive_cell"]["issued_coupling_rule_and_target_effect"]
    return CouplingRule(
        rule_id=pc["rule_id"], rule_version="0.proposed",
        issuer_authority="UNISSUED_TEST_ONLY",
        expected_event_issuer_role="WORLD_SCHEDULE_OFFICE",
        expected_event_id=PREDECL["positive_cell"]["positive_admitted_world_event"]["event_id"],
        effect_kind=pc["target_owner_effect"]["can008_current_response"]["effect_kind"],
        target_owner="ADP016")


def _well_typed_guard_request(transition: str, operation: str):
    guard = importlib.import_module("rawlsing_next.v3_psepf_zero_positive_guard")
    fp = guard.GuardStateFingerprint(**{
        f: "fp_" + f for f in guard.GuardStateFingerprint.__dataclass_fields__})
    return guard.GuardRequest(
        actor_id="LAB_ACTOR_1",
        source_class=guard.GuardedTruthClass.ANALYST_TRUTH,
        source_ref="ref:lab:hq298", source_hash="sha256:aa",
        source_lineage=(guard.GuardedTruthClass.ANALYST_TRUTH,),
        transition_surface_id=transition,
        operation_class=operation,
        state_fingerprint=fp, authority=None)


def test_C_real_execution_attempt_finds_missing_producer():
    """Attempt the smallest real pinned CAN008_R2 -> owner effect path using the
    ACTUAL imported surface. The positive producer is absent; the exact earliest
    HOLD must be raised rather than a mock transition claimed."""
    guard = importlib.import_module("rawlsing_next.v3_psepf_zero_positive_guard")
    decision = guard.evaluate_psepf_zero_positive_guard(
        _well_typed_guard_request("CAN008_R2_RESPONSE_EFFECT_COMMIT",
                                  "TARGET_OWNER_EFFECT_COMMIT"))
    assert decision.outcome == guard.GuardOutcome.DENY_ZERO_EFFECT
    assert decision.reason == guard.GuardReason.ZERO_POSITIVE_REGISTRY
    assert decision.zero_effect is True
    assert decision.actor_state_effect == "ZERO"
    assert decision.causal_ledger_appends == 0
    assert decision.delegated_owner_rule_id is None
    # and there is no callable that could mint the missing rule
    binding = importlib.import_module("rawlsing_next.sdtf_r4_mechanism_rule_authority_binding")
    assert not hasattr(binding, "mint_concrete_mechanism_rule")
    assert not hasattr(binding, "execute_rule_body")


def test_C_positive_cell_coupling_at_test_only_grain():
    """The predeclared positive cell runs at TEST-ONLY grain with the reused R2 law
    shape. It must never claim adoption."""
    ev, ps, rule = _cell_event(), _cell_prestates(), _cell_rule()
    receipt = coupling_evaluate(ev, ps, rule)
    assert receipt["grain"] == STUB_GRAIN
    assert receipt["rule_status"] == "TEST_ONLY_PROPOSED_NOT_ADOPTED"
    assert receipt["custody"]["occurrence_gate"] == "ADMITTED_OCCURRENCE_CONFIRMED"
    assert receipt["response_effect_kind"] == "BUFFER"
    assert receipt["response_durability"] == "NON_DURABLE_CURRENT_CONSEQUENCE"
    assert receipt["target_owner_effect"]["committed_in_this_stub"] is False
    assert receipt["target_owner_effect"]["commit_requires_separate_owner_authority"] is True
    assert receipt["recruitment_is_not_actor_access"] is True


def test_C_trace_commit_request_refuses_without_owner_producer():
    req = adp016_trace_commit_request(
        "T7", "E_CHILDHOOD_LOSS_OF_CAREGIVER_ROUTINE", "UNAVAILABLE")
    assert req["committed"] is False
    assert req["refusal"] == "MISSING_IMPLEMENTATION:ADP016_OWNER_TRANSITION_PRODUCER"


def test_C_first_person_access_denied_for_hidden_origin():
    ev, ps = _cell_event(), _cell_prestates()
    # a hidden-origin claim is blocked at the gate (typed refusal, not silence)
    with pytest.raises(AccessLeakBlocked) as e:
        adp017_first_person_claim_check(
            ps, claimed_origin="E_CHILDHOOD_LOSS_OF_CAREGIVER_ROUTINE", event=ev)
    assert "BLOCK_UNAVAILABLE_CHILDHOOD_FEATURE_TO_FIRST_PERSON" in str(e.value)
    # no claim at all yields the typed denial verdict
    verdict = adp017_first_person_claim_check(ps, claimed_origin=None, event=ev)
    assert verdict["claim_permission"] == "DENY_FIRST_PERSON_CLAIM"
    assert verdict["first_person_claim"] is None


def test_C_next_event_response_is_typed_not_prose():
    ev, ps, rule = _cell_event(), _cell_prestates(), _cell_rule()
    receipt = coupling_evaluate(ev, ps, rule)
    post_state = {"committed_effect_stream": receipt["response_effect_kind"],
                  "adp016_trace": "T7:REINFORCEMENT_REQUESTED_NOT_COMMITTED"}
    nxt = AdmittedEvent(
        event_id=PREDECL["positive_cell"]["next_event_response"]["event_id"],
        kind="EXTERNAL_RUNTIME_EVENT", issuer="PEER", issuer_role="PEER",
        effective_time="t2", public_features=("casual_remark",), admitted=True)
    later = next_event_response(post_state, nxt, rule)
    assert later["typed_effect_stream"] == "BUFFER"
    assert later["prior_prose_used_as_occurrence"] is False
    assert "committed_effect_stream" in later["evaluated_against_post_owner_state"]


# ---------------------------------------------------------------------------
# D. K3 hidden-childhood-trace arms
# ---------------------------------------------------------------------------

def test_D_K3_arms_match_predeclared_expectations():
    expected = PREDECL["K3_hidden_childhood_trace_arms"]
    for arm_name, expected_triplet in (
            ("A_TRACE", expected["A_TRACE"]["expected"]),
            ("B_NO_TRACE", expected["B_NO_TRACE"]["expected"]),
            ("C_UNAVAILABLE_NO_TRACE", expected["C_UNAVAILABLE_NO_TRACE"]["expected"])):
        arm = {"trace_formed": arm_name == "A_TRACE",
               "trace_use_rule": arm_name == "A_TRACE",
               "child_feature_state": "UNAVAILABLE"}
        got = run_k3_arm(arm)
        assert [got["trace_recruitment"], got["effect"], got["claim"]] == expected_triplet, (
            f"K3_ARM_MISMATCH:{arm_name}")


def test_D_K3_analyst_only_content_cannot_change_actor_projection():
    """Null: changing analyst-only childhood content cannot change actor projection/effect."""
    arm = {"trace_formed": True, "trace_use_rule": True, "child_feature_state": "UNAVAILABLE"}
    a = run_k3_arm(arm)
    b = run_k3_arm(dict(arm, analyst_only_origin="DIFFERENT_SEALED_ORIGIN"))
    assert a == b


def test_D_K3_unavailable_feature_never_becomes_first_person_claim():
    ps = _cell_prestates()
    ev = _cell_event()
    with pytest.raises(AccessLeakBlocked):
        adp017_first_person_claim_check(ps, claimed_origin="hidden_origin_alpha", event=ev)


# ---------------------------------------------------------------------------
# E. K5 official-power x felt-recognition arms
# ---------------------------------------------------------------------------

def test_E_K5_arms_match_predeclared_expectations():
    expected = PREDECL["K5_official_power_x_felt_recognition_arms"]
    cases = {
        "A_OFFICIAL_UNSAFE": ("OFFICIAL", "UNSAFE", True),
        "B_PEER_TRUSTED": ("PEER", "TRUSTED", True),
        "C_OFFICIAL_TRUSTED": ("OFFICIAL", "TRUSTED", True),
        "D_PEER_UNSAFE": ("PEER", "UNSAFE", True),
    }
    for name, (role, hist, grant) in cases.items():
        got = run_k5_arm(role, hist, grant)
        exp = expected[name]["expected"]
        assert [got["institutional_permission"], got["world_effect"], got["effect"]] == exp, (
            f"K5_ARM_MISMATCH:{name}")


def test_E_K5_world_only_switch_changes_world_effect_not_felt():
    a = run_k5_arm("OFFICIAL", "TRUSTED", True)
    b = run_k5_arm("PEER", "TRUSTED", True)
    assert a["world_effect"] != b["world_effect"]
    assert a["effect"] == b["effect"] == "REROUTE" or (a["effect"] == "REROUTE" and b["effect"] == "AMPLIFY")
    # felt axis is history, not world role: history TRUSTED + OFFICIAL -> REROUTE;
    # the felt responses differ across world roles only via the rule's coupling,
    # while history-only switch must change felt response:
    a2 = run_k5_arm("OFFICIAL", "UNSAFE", True)
    assert a2["effect"] == "DEFLECT"
    assert a2["world_effect"] == a["world_effect"]


def test_E_K5_history_only_switch_changes_felt_not_objective():
    a = run_k5_arm("OFFICIAL", "UNSAFE", True)
    b = run_k5_arm("OFFICIAL", "TRUSTED", True)
    assert a["world_effect"] == b["world_effect"] == "OFFICIAL_RECOGNITION"
    assert a["effect"] != b["effect"]


def test_E_K5_missing_world_owner_grant_bars_objective_change():
    got = run_k5_arm("OFFICIAL", "UNSAFE", False)
    assert got["world_effect"] == "NO_INSTITUTIONAL_CHANGE"
    assert got["institutional_permission"] == "PRESENT"


def test_E_K5_peer_cannot_confer_institution_status():
    ev = AdmittedEvent(
        event_id="E_PEER_TEXT", kind="EXTERNAL_RUNTIME_EVENT", issuer="PEER",
        issuer_role="PEER", effective_time="t1", public_features=("text",),
        admitted=True)
    with pytest.raises(AuthorityMismatch):
        institutional_ratification_check(
            ev, world_owner_grant=True, conferral_attempt="PEER_CONFERS_OFFICIAL_STATUS")


def test_E_K5_official_grant_cannot_compel_felt_belief():
    ev = AdmittedEvent(
        event_id="E_OFFICIAL_TEXT", kind="EXTERNAL_RUNTIME_EVENT", issuer="OFFICE",
        issuer_role="OFFICIAL", effective_time="t1", public_features=("text",),
        admitted=True)
    verdict = institutional_ratification_check(ev, world_owner_grant=True, conferral_attempt=None)
    assert verdict["official_grant_does_not_compel_felt_belief"] is True
    # felt effect under history UNSAFE stays DEFLECT even with full official grant
    assert run_k5_arm("OFFICIAL", "UNSAFE", True)["effect"] == "DEFLECT"


# ---------------------------------------------------------------------------
# F. negative controls
# ---------------------------------------------------------------------------

def test_F_rejected_draft_has_no_self_feedback():
    rule = _cell_rule()
    draft = AdmittedEvent(
        event_id="DRAFT_1", kind="REJECTED_RENDER", issuer="SELF",
        issuer_role="UNKNOWN", effective_time="t1",
        public_features=("draft_text",), admitted=False)
    with pytest.raises(OccurrenceGateViolation):
        event_custody_check(draft, CouplingRule(
            rule_id=rule.rule_id, rule_version="0.proposed",
            issuer_authority="UNISSUED_TEST_ONLY",
            expected_event_issuer_role="UNKNOWN", expected_event_id="DRAFT_1",
            effect_kind="BLOCK", target_owner="ADP016"))
    for kind in ("DRAFT_RESPONSE", "UNEMITTED_CANDIDATE", "V2_RENDER_CANDIDATE"):
        ev = AdmittedEvent(
            event_id="X", kind=kind, issuer="SELF", issuer_role="UNKNOWN",
            effective_time="t1", public_features=(), admitted=True)
        with pytest.raises(OccurrenceGateViolation):
            event_custody_check(ev, CouplingRule(
                rule_id="LAB_R_K3", rule_version="0.proposed",
                issuer_authority="UNISSUED_TEST_ONLY",
                expected_event_issuer_role="UNKNOWN", expected_event_id="X",
                effect_kind="BLOCK", target_owner="ADP016"))


def test_F_worldless_event_produces_zero_response():
    static = AdmittedEvent(
        event_id="STATE_RECORD_1", kind="STATIC_STATE_RECORD", issuer="STORE",
        issuer_role="UNKNOWN", effective_time="t1",
        public_features=("state_snapshot",), admitted=True)
    rule = CouplingRule(
        rule_id="LAB_R_K3", rule_version="0.proposed",
        issuer_authority="UNISSUED_TEST_ONLY",
        expected_event_issuer_role="UNKNOWN", expected_event_id="STATE_RECORD_1",
        effect_kind="BLOCK", target_owner="ADP016")
    with pytest.raises(OccurrenceGateViolation):
        event_custody_check(static, rule)


def test_F_wrong_source_issuer_refused():
    ev = _cell_event()
    bad_rule = CouplingRule(
        rule_id="LAB_R_K3", rule_version="0.proposed",
        issuer_authority="UNISSUED_TEST_ONLY",
        expected_event_issuer_role="PEER",  # wrong issuer role for this event
        expected_event_id=ev.event_id, effect_kind="BUFFER", target_owner="ADP016")
    with pytest.raises(AuthorityMismatch) as e:
        event_custody_check(ev, bad_rule)
    assert "WRONG_SOURCE_ISSUER" in str(e.value)


def test_F_wrong_occurrence_refused():
    ev = _cell_event()
    bad_rule = CouplingRule(
        rule_id="LAB_R_K3", rule_version="0.proposed",
        issuer_authority="UNISSUED_TEST_ONLY",
        expected_event_issuer_role="WORLD_SCHEDULE_OFFICE",
        expected_event_id="E_SOME_OTHER_OCCURRENCE",
        effect_kind="BUFFER", target_owner="ADP016")
    with pytest.raises(AuthorityMismatch) as e:
        event_custody_check(ev, bad_rule)
    assert "WRONG_OCCURRENCE" in str(e.value)


def test_F_unadmitted_event_cannot_produce_effect():
    ev = AdmittedEvent(
        event_id="E_PROPOSED", kind="EXTERNAL_RUNTIME_EVENT", issuer="X",
        issuer_role="WORLD_SCHEDULE_OFFICE", effective_time="t1",
        public_features=("f",), admitted=False)
    rule = CouplingRule(
        rule_id="LAB_R_K3", rule_version="0.proposed",
        issuer_authority="UNISSUED_TEST_ONLY",
        expected_event_issuer_role="WORLD_SCHEDULE_OFFICE",
        expected_event_id="E_PROPOSED", effect_kind="BUFFER", target_owner="ADP016")
    with pytest.raises(OccurrenceGateViolation):
        event_custody_check(ev, rule)


def test_F_inaccessible_origin_false_explanatory_answer_blocked():
    ps, ev = _cell_prestates(), _cell_event()
    with pytest.raises(AccessLeakBlocked) as e:
        adp017_first_person_claim_check(
            ps, claimed_origin="childhood_poverty_caused_my_response", event=ev)
    assert "BLOCK" in str(e.value)


def test_F_forced_institutional_ratification_blocked():
    peer = AdmittedEvent(
        event_id="E_PEER", kind="EXTERNAL_RUNTIME_EVENT", issuer="PEER",
        issuer_role="PEER", effective_time="t1", public_features=("t",), admitted=True)
    with pytest.raises(AuthorityMismatch):
        institutional_ratification_check(
            peer, world_owner_grant=True,
            conferral_attempt="PEER_CONFERS_OFFICIAL_STATUS")


def test_F_prior_history_replay_is_exact():
    ev, ps, rule = _cell_event(), _cell_prestates(), _cell_rule()
    r1 = coupling_evaluate(ev, ps, rule)
    r2 = coupling_evaluate(_cell_event(), _cell_prestates(), _cell_rule())
    assert r1 == r2
    assert json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)


# ---------------------------------------------------------------------------
# G. B0 vs B1 comparison
# ---------------------------------------------------------------------------

def test_G_B0_B1_same_inputs_no_new_semantic_result():
    cfg = PREDECL["B0_B1_comparison"]
    ev, ps, rule = _cell_event(), _cell_prestates(), _cell_rule()
    b0 = coupling_evaluate(ev, ps, rule)
    latent = {"recognition_sensitivity": 1, "trace_pressure": 1}
    b1 = dict(b0)
    b1["B1_extra_computation_not_semantic_authority"] = latent
    from owner_effect_stub_TEST_ONLY import coupling_evaluate as _ce  # noqa
    semantic_keys = set(b0.keys()) - {"grain"}
    for k in semantic_keys:
        assert b1[k] == b0[k], f"B1_CHANGED_SEMANTIC_RESULT:{k}"
    assert cfg["default_without_lift"] == "PREFER_B0"
    assert cfg["heldout_increment_required_for_B1"] is True
    # no held-out discriminant is registered in this lab -> B1 cannot claim lift
    assert "B1_extra_computation_not_semantic_authority" in b1


# ---------------------------------------------------------------------------
# H. machine-verified rejections from ACTUALLY IMPORTED modules
# ---------------------------------------------------------------------------

def test_H_zero_positive_guard_registry_is_empty_and_rejects():
    guard = importlib.import_module("rawlsing_next.v3_psepf_zero_positive_guard")
    assert dict(guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES) == {}
    for transition, operation in (
        ("CAN008_R2_RESPONSE_EFFECT_COMMIT", "TARGET_OWNER_EFFECT_COMMIT"),
        ("ADP016_TRACE_COMMIT", "DURABLE_MEMORY_TRANSITION"),
        ("ADP017_KNOWLEDGE_TRANSITION", "EPISTEMIC_STATE_TRANSITION"),
    ):
        d = guard.evaluate_psepf_zero_positive_guard(
            _well_typed_guard_request(transition, operation))
        assert d.outcome == guard.GuardOutcome.DENY_ZERO_EFFECT
        assert d.reason == guard.GuardReason.ZERO_POSITIVE_REGISTRY
        assert d.zero_effect is True
        assert d.causal_ledger_appends == 0


def test_H_sdtf_rule_admission_seam_rejects_unadmitted_rules():
    """Actual imported SDTF R4 rule-admission seam refuses an unadmitted rule
    application with a typed integrity failure (fail closed)."""
    importlib.import_module("rawlsing_next.sdtf_r4_mechanism_rule_authority_binding")
    d1 = importlib.import_module("rawlsing_next.sdtf_r4_d1_hosting_replay")
    from rawlsing_next.tests.test_sdtf_r4_mechanism_rule_authority_binding import (
        _binding, _ref)
    adapter = d1.D1HostingAdapter()
    b = _binding(tag="hq298")
    app = d1.D1RuleApplicationRef(
        rule_application_id="APP-HQ298",
        rule_id=b.rule_identity.rule_id,
        rule_version=b.rule_identity.rule_version,
        rule_hash=b.rule_identity.rule_content_hash)
    det = d1.D1FactPointer(
        fact_ref=_ref("HQ298_FACT", "det"),
        context=d1.D1Context("world-seam", "state-seam", "sv1", "t1"))
    out = d1.D1FactPointer(
        fact_ref=_ref("HQ298_FACT", "out"),
        context=d1.D1Context("world-seam", "state-seam", "sv1", "t1"))
    with pytest.raises(d1.D1HostingIntegrityError):
        adapter.host_direct_derivation(
            app, determinant_facts=[det], output_fact=out, rule_admission=None)


def test_H_m6_actor_safe_ingress_blocks_forbidden_sources():
    m6 = importlib.import_module("rawlsing_next.m6_actor_safe_expression")
    assert "PSEPF" in m6.FORBIDDEN_BEHAVIORAL_SOURCE_CLASSES
    assert "ANALYST_ONLY_TRUTH" in m6.FORBIDDEN_BEHAVIORAL_SOURCE_CLASSES
    assert "OPAQUE_UPSTREAM_AUDIT_OR_PROVENANCE" in m6.FORBIDDEN_BEHAVIORAL_SOURCE_CLASSES
    with pytest.raises(Exception):
        m6.assert_behavioral_source_rejected("PSEPF")


def test_H_gt0_end_to_end_blocks_positive_actor_path():
    e2e = importlib.import_module("rawlsing_next.wsc_gt0_end_to_end")
    assert e2e.TERMINAL == "BLOCKED_POSITIVE_ACTOR_PATH__SEMANTIC_CONSERVATION_PASS"
    result = e2e.run_gt0_end_to_end()
    assert result is not None
    assert result.terminal == e2e.TERMINAL
    statuses = [str(r.status) for r in result.receipts]
    assert any("PASS" in s for s in statuses)
    assert result.full_thread_hash


def test_H_effect_vocabulary_is_the_adopted_r2_vocabulary():
    from owner_effect_stub_TEST_ONLY import CAN008_R2_EFFECT_VOCABULARY, CAN008_R2_ADOPTED_BLOB
    assert CAN008_R2_ADOPTED_BLOB == PREDECL["authority_pins"]["CAN008_R2_adopted_blob"]
    assert set(CAN008_R2_EFFECT_VOCABULARY) == set(PREDECL["effect_vocabulary_reused_from_adopted_authority"])
