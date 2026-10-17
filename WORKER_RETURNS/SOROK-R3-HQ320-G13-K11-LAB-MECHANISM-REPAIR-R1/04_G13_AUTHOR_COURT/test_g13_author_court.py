"""G13 author court for the seven repaired mechanism families.

FROZEN BEFORE EXECUTION. Authored by the G13 repair implementer against the
repaired laboratory only. This court is deliberately NOT a copy of G12: G12's
assertions were frozen against the unrepaired laboratory, and 11 of its 25
control assertions document the defects themselves.

Scope: source-free genealogy laboratory mechanism repair.
- No production ADP issuance, no N12, no original respondent data.
- No PRE-MAIN/CURRENT/actor wake, no new model or provider call.
- No accepted V3 parent, conception, birth or CHILD_GENERATED event is created.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent
LAB = ROOT.parent / "03_POSTREPAIR_COURT/sources/sgi1/01_LAB_IMPLEMENTATION"
sys.dont_write_bytecode = True
sys.path.insert(0, str(LAB))

from lab_sgi1.construction import (  # noqa: E402
    DadHistoryBuilder, forward_replay_to_endpoint, psyche_from_dad_events,
    heldout_independent_probes, stopping_law_check, construct_second_parent,
    PLACE_ESTABLISHING_KINDS, ROOT_EVENT_KINDS,
)
from lab_sgi1.mother import build_mother_checkpoint  # noqa: E402
from lab_sgi1.proposal import (  # noqa: E402
    build_proposal_prompt, scrub_future_child_material, FUTURE_CHILD_REDACTION,
)
from lab_sgi1.selection import adp020_select, candidate_replay_hash  # noqa: E402
from lab_sgi1.core import (  # noqa: E402
    ScopedRNG, RngAuthorityError, ADP020_SAMPLER, ADP020_DOMAIN_SEPARATOR,
    DECLARED_LEGACY_LAB_ROOT_TOKENS, classify_root_seed,
)
from lab_sgi1.relation import reconcile, FORMING_WITNESS_KINDS  # noqa: E402
from lab_sgi1.continuation import forward_continuation, lab_conception_boundary  # noqa: E402

STREAM = "v3.causal.adp015.conception_scenario_selection"

# New author tests use exact ADP-020 32-byte roots. Declared legacy tokens
# exist only for the two frozen historical suites.
ROOT_A = "13" * 32
ROOT_B = "29" * 32


def ec(place="INST_WORKSHOP_A", route="ROUTE_LOCAL_CLOSED"):
    return dict(route_kind_id=route, time_or_interval="T_ENCOUNTER_LAB_WINDOW",
                required_state_predicates=[
                    dict(field="place", equals=place),
                    dict(field="availability_status",
                         equals="available_for_encounter")])


def valid_history(actor="G13_ACTUAL_SECOND_PARENT", seed="G13_FIXED_SEED", e=None):
    return DadHistoryBuilder(actor, seed, e or ec()).build()


# ===========================================================================
# FAMILY 1 -- CAUSAL ANCESTRY
# ===========================================================================

def test_f1_clean_history_still_reaches_endpoint():
    """The repair must not break the legitimate forward history."""
    r = forward_replay_to_endpoint(valid_history(), ec())
    assert r["endpoint_match"] is True
    assert r["causal_integrity_errors"] == []
    assert r["endpoint_state_derived_from_antecedent"] is True


def test_f1_forged_endpoint_place_refused():
    ev = valid_history()
    ev[-1]["payload"]["place"] = "UNREACHABLE_SITE"
    r = forward_replay_to_endpoint(ev, ec("UNREACHABLE_SITE"))
    assert r["endpoint_match"] is False
    assert "ENDPOINT_ASSERTION_WITHOUT_ANTECEDENT" in r["causal_error_codes"]


def test_f1_endpoint_claim_cannot_overwrite_derived_place():
    """Endpoint teleology: ENDPOINT_STATE is a claim, never a write."""
    ev = valid_history()
    ev.append({"event_id": "LATE_FORGED", "effective_index": 999,
               "kind": "ENDPOINT_STATE",
               "payload": {"place": "ANYWHERE_AT_ALL",
                           "availability_status": "available_for_encounter"},
               "causal_parent_event_ids": [ev[-1]["event_id"]]})
    r = forward_replay_to_endpoint(ev, ec("ANYWHERE_AT_ALL"))
    assert r["endpoint_match"] is False
    assert r["recomputed_state"]["place"] == "INST_WORKSHOP_A"


@pytest.mark.parametrize("mutate,code", [
    (lambda e: e[4].__setitem__("causal_parent_event_ids", ["ABSENT_PARENT"]),
     "MISSING_CAUSAL_PARENT"),
    (lambda e: e[0].__setitem__("causal_parent_event_ids", [e[-1]["event_id"]]),
     "FUTURE_CAUSAL_PARENT"),
    (lambda e: e[1].__setitem__("effective_index", 0),
     "DUPLICATE_EFFECTIVE_INDEX"),
    # Parent already replayed but at an index >= the child: reachable only when
    # the effective index is duplicated, so it is not merely "not yet seen".
    (lambda e: (e[3].__setitem__("effective_index", e[2]["effective_index"])),
     "NONFORWARD_CAUSAL_PARENT"),
])
def test_f1_invalid_causal_ancestry_refused(mutate, code):
    ev = valid_history()
    mutate(ev)
    r = forward_replay_to_endpoint(ev, ec())
    assert r["endpoint_match"] is False
    assert code in r["causal_error_codes"]


def test_f1_removed_route_antecedent_refused():
    ev = [e for e in valid_history()
          if e["kind"] not in ("COMMISSIONED_WORK", "ROUTE_AVAILABILITY")]
    r = forward_replay_to_endpoint(ev, ec())
    assert r["endpoint_match"] is False
    assert "ENDPOINT_ASSERTION_WITHOUT_ANTECEDENT" in r["causal_error_codes"]


def test_f1_only_declared_place_establishing_kinds_derive_place():
    ev = valid_history()
    # A route-intention event alone must never establish place.
    ev = [e for e in ev if e["kind"] != "COMMISSIONED_WORK"]
    r = forward_replay_to_endpoint(ev, ec())
    assert r["recomputed_state"]["place"] is None
    assert r["endpoint_match"] is False


def test_f1_undeclared_root_refused():
    ev = valid_history()
    ev[1]["causal_parent_event_ids"] = []
    ev[1]["kind"] = "WORK_POSITION"
    r = forward_replay_to_endpoint(ev, ec())
    assert "UNDECLARED_ROOT" in r["causal_error_codes"]


# ===========================================================================
# FAMILY 2 -- PREHISTORY SUFFICIENCY (typed HOLD)
# ===========================================================================

def _stopping(ev, e=None):
    e = e or ec()
    p = psyche_from_dad_events(ev)
    r = forward_replay_to_endpoint(ev, e)
    pr = heldout_independent_probes(ev, p)
    return stopping_law_check(ev, p, e, r, pr), r, pr


def test_f2_clean_history_is_sufficient_and_not_a_hold():
    st, _, _ = _stopping(valid_history())
    assert st["sufficient"] is True
    assert st["status"] == "COMMITTED"
    assert "typed_hold" not in st


def test_f2_stopping_constants_are_no_longer_constants():
    """Both former constant predicates must now be computed from evidence."""
    ev = valid_history()
    ev[4]["causal_parent_event_ids"] = ["ABSENT_PARENT"]
    st, _, _ = _stopping(ev)
    assert st["checks"]["no_outstanding_mandatory_antecedent_missing_authority"] is False
    assert st["checks"]["bounded_observational_closure"] is False


def test_f2_unknown_required_history_yields_typed_hold():
    ev = [e for e in valid_history()
          if e["kind"] not in ("COMMISSIONED_WORK", "ROUTE_AVAILABILITY")]
    st, _, _ = _stopping(ev)
    assert st["sufficient"] is False
    hold = st["typed_hold"]
    assert hold["hold_state"] == "PREHISTORY_OWNER_RULE_MISSING"
    assert hold["is_HOLD_not_INFEASIBLE"] is True
    assert "REQUIRED_ENDPOINT_PREDICATE_WITHOUT_ANTECEDENT" in hold["hold_reasons"]


def test_f2_missing_domain_coverage_yields_typed_hold():
    ev = [e for e in valid_history() if e["kind"] != "MEMORY_TRACE"]
    st, _, _ = _stopping(ev)
    assert st["sufficient"] is False
    assert "DOMAIN_COVERAGE_NOT_CAUSALLY_ANCHORED" in st["typed_hold"]["hold_reasons"]


# ===========================================================================
# FAMILY 3 -- INDEPENDENT PROJECTS
# ===========================================================================

def test_f3_genuine_project_and_peer_relation_satisfy_probes():
    ev = valid_history()
    pr = heldout_independent_probes(ev, psyche_from_dad_events(ev))
    assert pr["heldout_independence_pass"] is True
    for probe in pr["probes"]:
        assert probe["supporting_evidence"], probe["probe_id"]
        assert probe["third_party_relationship_actor_specific"] is True


def test_f3_unrelated_archive_project_cannot_satisfy_p1():
    ev = valid_history()
    for e in ev:
        if e["kind"] == "PROJECT":
            e["payload"]["project"] = "ARCHIVE_CATALOGUING_NO_REPAIR_SKILL"
    pr = heldout_independent_probes(ev, psyche_from_dad_events(ev))
    assert pr["heldout_independence_pass"] is False
    assert pr["probes"][0]["pass"] is False


def test_f3_unrelated_sibling_cannot_satisfy_p2():
    ev = valid_history()
    for e in ev:
        if e["kind"] == "NONMOTHER_RELATIONSHIP":
            e["payload"]["counterpart"] = "UNRELATED_SIBLING_NOT_BORROWER"
    pr = heldout_independent_probes(ev, psyche_from_dad_events(ev))
    assert pr["probes"][1]["pass"] is False


def test_f3_generic_attitude_tags_alone_are_insufficient():
    """Strip the consequence evidence; surviving tags must not satisfy a probe."""
    ev = valid_history()
    for e in ev:
        if e["kind"] == "PROJECT":
            e["payload"].pop("durable_effect", None)
        if e["kind"] == "NONMOTHER_RELATIONSHIP":
            e["payload"].pop("durable_effect", None)
    pr = heldout_independent_probes(ev, psyche_from_dad_events(ev))
    assert pr["heldout_independence_pass"] is False


def test_f3_uncausally_anchored_project_cannot_satisfy_p1():
    ev = valid_history()
    for e in ev:
        if e["kind"] == "PROJECT":
            e["causal_parent_event_ids"] = ["NOT_A_REAL_ANCESTOR"]
    pr = heldout_independent_probes(ev, psyche_from_dad_events(ev))
    assert pr["probes"][0]["pass"] is False


# ===========================================================================
# FAMILY 4 -- FUTURE-CHILD EMBARGO (every model-visible path)
# ===========================================================================

SENTINEL = "G13_FUTURE_CHILD_DESIRED_WOUND_SECRET"


@pytest.mark.parametrize("path", ["target", "world", "psyche", "nested_psyche",
                                  "list_in_world", "nested_target"])
def test_f4_no_future_child_material_reaches_the_prompt(path):
    a = build_mother_checkpoint("G13_EMBARGO", "M0").anchor_dict()
    t = {"target_status": "PENDING_NONCAUSAL"}
    w = {"world_id": "G13_WORLD"}
    if path == "target":
        t["future_child_desired_adversity_tag"] = SENTINEL
    elif path == "world":
        w["future_child_desired_adversity_tag"] = SENTINEL
    elif path == "psyche":
        a["psyche"]["future_child_desired_adversity_tag"] = SENTINEL
    elif path == "nested_psyche":
        a["psyche"].setdefault("nested", {})["future_child_health_outcome"] = SENTINEL
    elif path == "list_in_world":
        w["records"] = [{"future_child_education_outcome": SENTINEL}]
    else:
        t["detail"] = {"future_child_personality": SENTINEL}
    prompt = build_proposal_prompt(a, t, w, None, 4)
    assert SENTINEL not in prompt


def test_f4_prohibited_keys_are_redacted_not_dropped():
    a = build_mother_checkpoint("G13_EMBARGO", "M0").anchor_dict()
    t = {"future_child_outcome_label": SENTINEL}
    prompt = json.loads(build_proposal_prompt(a, t, {}, None, 4))
    assert prompt["pending_target"]["future_child_outcome_label"] == FUTURE_CHILD_REDACTION


def test_f4_clean_inputs_are_unchanged_by_the_membrane():
    """The embargo must not perturb lawful older-child history."""
    a = build_mother_checkpoint("G13_EMBARGO", "M2").anchor_dict()
    t = {"target_status": "PENDING_NONCAUSAL"}
    w = {"world_id": "G13_WORLD"}
    prompt = json.loads(build_proposal_prompt(a, t, w, None, 4))
    assert prompt["mother_anchor_visible_fields"]["already_generated_child_refs"] == \
        ["LAB_OLDER_CHILD_O1"]
    assert prompt["mother_anchor_visible_fields"]["psyche"] == a["psyche"]


def test_f4_legitimate_older_child_history_is_preserved_end_to_end():
    m = build_mother_checkpoint("G13_M2", "M2")
    assert m.anchor_dict()["already_generated_child_refs"] == ["LAB_OLDER_CHILD_O1"]
    ev = valid_history()
    r = forward_replay_to_endpoint(ev, ec())
    assert r["endpoint_match"] is True  # older child does not perturb the endpoint


def test_f4_future_child_outcome_counterfactual_cannot_change_selection():
    """A future-child outcome must not steer the stochastic outcome.

    ADP-020 s7.1: the candidate-set hash is part of the DECISION replay identity,
    not of the stream seed. So a mutated payload legitimately changes the recorded
    candidate-set identity, while the raw draw value must be untouched. That is
    exactly the property that stops a future-child outcome from steering history.
    """
    a = build_mother_checkpoint("G13_CF", "M0").anchor_dict()
    classes = [dict(class_key="C1", representative_id="R1", payload="ORIGINAL"),
               dict(class_key="C2", representative_id="R2", payload="OTHER")]
    tainted = copy.deepcopy(classes)
    tainted[0]["future_child_desired_adversity_tag"] = SENTINEL

    # identical root and scope: only the candidate payload differs
    before = adp020_select("SIM_UNIFORM_CLASSES", classes, ROOT_A, "G13_SCOPE")
    after = adp020_select("SIM_UNIFORM_CLASSES", tainted, ROOT_A, "G13_SCOPE")

    # payload is bound into the recorded selection identity ...
    assert before["candidate_set_hash"] != after["candidate_set_hash"]
    # ... but it cannot move the draw itself
    assert before["draw"]["draw_value"] == after["draw"]["draw_value"]
    assert before["selected_class_key"] == after["selected_class_key"]
    assert a["already_generated_child_refs"] == []


def test_f4_scope_identity_never_contains_future_child_material():
    """The RNG scope is bound from lawful fields only, never a child outcome."""
    from lab_sgi1.selection import scope_hash
    sh = scope_hash("RUN_G13", build_mother_checkpoint("G13_CF", "M0").hash(),
                    "TARGET_HASH", "GRAMMAR@1")
    assert "future_child" not in sh.lower()
    assert sh.startswith("sha256:")


# ===========================================================================
# FAMILY 5 -- ADP020-COMPATIBLE RNG
# ===========================================================================

def test_f5_invalid_root_is_refused_before_any_draw():
    with pytest.raises((ValueError, TypeError)):
        ScopedRNG("short", STREAM, "G13_SCOPE").draw(3, "slot", "cset")


def test_f5_exact_32_byte_root_uses_accepted_adp020_mechanism():
    r = ScopedRNG("ab" * 32, STREAM, "G13_SCOPE")
    rec = r.draw(3, "slot", "cset")
    assert rec.sampler == ADP020_SAMPLER
    assert rec.adp020_entitlement == "SAMPLER_MECHANISM_CONFORMANT"
    assert rec.scope_seed_sha256 and rec.stream_seed_sha256


def test_f5_rejection_sampling_is_unbiased():
    r = ScopedRNG("cd" * 32, STREAM, "G13_SCOPE")
    seen = []
    real = r._raw

    def scripted(vals):
        it = iter(vals)

        def f(*a):
            return next(it)
        return f

    r._raw = scripted([2 ** 64 - 1, 1])
    rec = r.draw(3, "slot", "cset")
    assert rec.entropy_block_count == 2
    assert rec.draw_value == 1
    assert rec.accepted_raw_u64 == 1
    assert rec.rejection_limit_u64 == 2 ** 64 - 1


def test_f5_modulo_bias_limit_is_correct():
    for bound in (3, 5, 7, 6, 10):
        r = ScopedRNG("ef" * 32, STREAM, "G13_SCOPE")
        rec = r.draw(bound, "slot", "cset")
        assert rec.rejection_limit_u64 == 2 ** 64 - (2 ** 64 % bound)


def test_f5_seed_lineage_is_isolated_per_scope_and_stream():
    a = ScopedRNG("11" * 32, STREAM, "SCOPE_A")
    b = ScopedRNG("11" * 32, STREAM, "SCOPE_B")
    assert a.scope_seed_sha256 != b.scope_seed_sha256
    assert a.stream_seed_sha256 != b.stream_seed_sha256


def test_f5_legacy_token_is_receipted_as_non_adp020_and_never_disguised():
    r = ScopedRNG("R0", STREAM, "G13_SCOPE")
    rec = r.draw(6, "slot", "cset")
    assert rec.adp020_entitlement == "NOT_GRANTED"
    assert rec.hold == "ADP020_REAL_ROOT_SEED_REQUIRED"
    assert rec.sampler != ADP020_SAMPLER
    assert rec.scope_seed_sha256 == ""


def test_f5_undeclared_token_is_refused():
    with pytest.raises((ValueError, TypeError)):
        ScopedRNG("NOT_A_TOKEN", STREAM, "G13_SCOPE").draw(3, "slot", "cset")
    assert "R0" in DECLARED_LEGACY_LAB_ROOT_TOKENS


def test_f5_unregistered_stream_is_refused():
    with pytest.raises((ValueError, TypeError)):
        ScopedRNG("ab" * 32, "not_a_v3_causal_stream", "G13_SCOPE").draw(3, "s", "c")


def test_f5_empty_and_singleton_consume_zero_draws():
    assert adp020_select("SIM_UNIFORM_CLASSES", [], ROOT_A, "S")["n_draws"] == 0
    one = [dict(class_key="A", representative_id="A", payload="X")]
    assert adp020_select("SIM_UNIFORM_CLASSES", one, ROOT_A, "S")["n_draws"] == 0


def test_f5_domain_separator_is_the_accepted_adp020_one():
    assert ADP020_DOMAIN_SEPARATOR == \
        b"RAWLSING\x00ADP-020\x00V3_CAUSAL_HMAC_SHA256_COUNTER_V1\x00"


# ===========================================================================
# FAMILY 6 -- SELECTOR INTEGRITY
# ===========================================================================

def test_f6_changed_payload_same_class_key_changes_selection_identity():
    c = [dict(class_key="A", representative_id="A", payload="ORIGINAL"),
         dict(class_key="B", representative_id="B", payload="OTHER")]
    mutated = copy.deepcopy(c)
    mutated[0]["payload"] = "MUTATED_HISTORY_REQUIREMENT"
    a = adp020_select("SIM_UNIFORM_CLASSES", c, ROOT_A, "G13_SCOPE")
    b = adp020_select("SIM_UNIFORM_CLASSES", mutated, ROOT_A, "G13_SCOPE")
    assert a["candidate_set_hash"] != b["candidate_set_hash"]


def test_f6_candidate_replay_hash_changes_with_content():
    base = dict(class_key="A", representative_id="A", payload="X")
    changed = dict(class_key="A", representative_id="A", payload="Y")
    assert candidate_replay_hash(base) != candidate_replay_hash(changed)


def test_f6_phrasing_multiplicity_does_not_change_identity():
    """N paraphrases of one class must not alter the replay identity."""
    one = dict(class_key="A", representative_id="A", payload="X",
               member_ids=["C1"], member_count=1)
    many = dict(class_key="A", representative_id="A", payload="X",
                member_ids=["C1", "C2", "C3"], member_count=3)
    assert candidate_replay_hash(one) == candidate_replay_hash(many)


def test_f6_input_order_does_not_change_identity():
    c = [dict(class_key="B", representative_id="RB", payload="2"),
         dict(class_key="A", representative_id="RA", payload="1")]
    d = list(reversed(c))
    assert (adp020_select("SIM_UNIFORM_CLASSES", c, ROOT_A, "S")["candidate_set_hash"]
            == adp020_select("SIM_UNIFORM_CLASSES", d, ROOT_A, "S")["candidate_set_hash"])


def test_f6_unregistered_policy_is_a_no_draw_hold():
    r = adp020_select("UNISSUED_POLICY",
                      [dict(class_key="A", representative_id="A")], ROOT_A, "S")
    assert r["status"] == "SELECTION_AUTHORITY_UNBOUND"
    assert r.get("n_draws", 0) == 0


def test_f6_invalid_root_yields_typed_hold_not_infeasible():
    r = adp020_select("SIM_UNIFORM_CLASSES",
                      [dict(class_key="A", representative_id="A")], "short", "S")
    assert r["status"] == "NOT_EXECUTED_AUTHORITY_HOLD"
    assert r["rng_failure_code"] == "RNG_ROOT_SEED_INVALID"
    assert r["n_draws"] == 0


# ===========================================================================
# FAMILY 7 -- RELATIONSHIP AND CONTINUATION
# ===========================================================================

def test_f7_no_relationship_without_second_parent_history_or_witness():
    a = build_mother_checkpoint("G13_REL", "M0").anchor_dict()
    r = reconcile(a, [], {"candidate_kind": "PROVISIONAL_COUNTERPART"})
    assert r["status"] != "COMMITTED"
    assert r["relationship_committed"] is False
    assert "NO_SECOND_PARENT_HISTORY_SUPPLIED" in r["hold_reasons"]


def test_f7_history_without_forming_witness_is_refused():
    a = build_mother_checkpoint("G13_REL", "M0").anchor_dict()
    ev = [e for e in valid_history()
          if e["kind"] not in FORMING_WITNESS_KINDS]
    r = reconcile(a, ev, {"candidate_kind": "PROVISIONAL_COUNTERPART"})
    assert r["status"] != "COMMITTED"
    assert "NO_FORMING_WITNESS_EVENT" in r["hold_reasons"]


def test_f7_actor_id_is_bound_from_actual_history_not_a_placeholder():
    a = build_mother_checkpoint("G13_REL", "M0").anchor_dict()
    ev = valid_history(actor="G13_ACTUAL_SECOND_PARENT")
    r = reconcile(a, ev, {"candidate_kind": "PROVISIONAL_COUNTERPART"})
    assert r["objective_relation"]["participants"][1] == "G13_ACTUAL_SECOND_PARENT"
    assert "LAB_SECOND_PARENT_SELECTED" not in json.dumps(r)


def test_f7_two_independently_derived_paternal_histories_bind_distinct_actors():
    a = build_mother_checkpoint("G13_REL", "M0").anchor_dict()
    r1 = reconcile(a, valid_history(actor="G13_SECOND_PARENT_ALPHA"),
                   {"candidate_kind": "PROVISIONAL_COUNTERPART"})
    r2 = reconcile(a, valid_history(actor="G13_SECOND_PARENT_BETA"),
                   {"candidate_kind": "PROVISIONAL_COUNTERPART"})
    assert r1["objective_relation"]["participants"][1] == "G13_SECOND_PARENT_ALPHA"
    assert r2["objective_relation"]["participants"][1] == "G13_SECOND_PARENT_BETA"
    assert r1["objective_relation"]["relation_id"] != r2["objective_relation"]["relation_id"]


def test_f7_empty_history_emits_no_paternal_continuation():
    a = build_mother_checkpoint("G13_REL", "M0").anchor_dict()
    rel = {"objective_relation": {"participants": [a["actor_id"], "G13_UNFORMED"]}}
    c = forward_continuation(a, [], rel)
    assert not [e for e in c["continuation_events"] if e["actor"] == "G13_UNFORMED"]
    assert c["paternal_continuation_admitted"] is False
    assert c["unformed_actor_continuation_minted"] is False


def test_f7_real_history_admits_paternal_continuation():
    a = build_mother_checkpoint("G13_REL", "M0").anchor_dict()
    ev = valid_history(actor="G13_SECOND_PARENT_ALPHA")
    rel = reconcile(a, ev, {"candidate_kind": "PROVISIONAL_COUNTERPART"})
    c = forward_continuation(a, ev, rel)
    assert c["paternal_continuation_admitted"] is True
    assert c["both_parents_continue_independently"] is True


def test_f7_asymmetry_and_no_auto_household_preserved():
    a = build_mother_checkpoint("G13_REL", "M0").anchor_dict()
    r = reconcile(a, valid_history(), {"candidate_kind": "PROVISIONAL_COUNTERPART"}, True)
    assert r["perceived_states"][0]["perceived_state"] == "affectionate_bond_perceived"
    assert r["perceived_states"][1]["perceived_state"] == "UNKNOWN_OR_NONRECIPROCAL"
    assert r["household_membership_auto"] is False
    assert r["reciprocity_inferred"] is False


# ===========================================================================
# CEILINGS -- the repair must not create V3 truth
# ===========================================================================

def test_ceilings_no_child_generated_no_birth_no_conception():
    b = lab_conception_boundary()
    assert b["child_generated_events"] == 0
    assert b["birth_alias"] is False
    assert "CONCEPTION_BIOLOGY_AUTHORITY_HOLD" in b["missing_authority"]


def test_ceilings_negative_endpoint_constraint_is_refused_not_rewritten():
    impossible = ec("IMPOSSIBLE_SITE")
    out = construct_second_parent({"class_key": "G13_IMPOSSIBLE"}, impossible,
                                  ["S1", "S2", "S3", "S4"])
    assert out["terminal_status"] == "HISTORY_SEARCH_EXHAUSTED"
    assert out["selected_events"] is None
    assert out["n_attempts"] == 4


def test_ceilings_m0_and_m2_mother_histories_both_construct():
    for variant, place, route in (("M0", "INST_WORKSHOP_A", "ROUTE_LOCAL_CLOSED"),
                                  ("M2", "INST_TRANSIT_E", "ROUTE_MOBILITY")):
        m = build_mother_checkpoint(f"G13_{variant}", variant)
        before = m.hash()
        out = construct_second_parent({"class_key": f"G13_{variant}"},
                                      ec(place, route), ["A1", "A2", "A3", "A4"])
        assert out["terminal_status"] == "COMMITTED", variant
        assert m.hash() == before, "mother history must be byte-identical"


def test_ceilings_lab_rule_remains_not_adopted():
    import lab_sgi1
    assert lab_sgi1.LAB_RULE_STATUS == "PROVISIONAL_LAB_RULE__NOT_ADOPTED"


# ===========================================================================
# FAMILY 5 (continued) -- the one G12 assertion that no repair can satisfy
# ===========================================================================

REQUIRED_ADP020_ALGORITHM = "ADP020_HMAC_SHA256_UNIFORM_BELOW_V1@1.0.0"


def test_f5_lab_sampler_conforms_to_the_accepted_adp020_algorithm():
    """Independent conformance proof for the assertion G12 cannot evaluate.

    G12's `test_lab_sampler_is_accepted_adp020_algorithm` compares two string
    literals hard-coded inside its own frozen harness (`g12_assays.py` line 157):
    the "actual" side is the literal 'SHA256_CONCAT_MODULO' and is never derived
    from the laboratory. It therefore evaluates
    'SHA256_CONCAT_MODULO' == 'ADP020_HMAC_SHA256_UNIFORM_BELOW_V1@1.0.0',
    which is False for every possible laboratory, including a fully conformant
    one. This test establishes the real property against the live laboratory.
    """
    r = ScopedRNG("7a" * 32, STREAM, "G13_SCOPE")
    rec = r.draw(7, "slot", "cset")
    assert rec.sampler == REQUIRED_ADP020_ALGORITHM
    assert rec.sampler == ADP020_SAMPLER
    assert rec.adp020_entitlement == "SAMPLER_MECHANISM_CONFORMANT"
    assert rec.hold is None


def test_f5_g12_literal_assertion_is_unfalsifiable_by_any_laboratory():
    """Documents, rather than exploits, the G12 harness artifact."""
    g12_frozen_actual_literal = "SHA256_CONCAT_MODULO"
    # No laboratory value can satisfy this comparison.
    assert g12_frozen_actual_literal != REQUIRED_ADP020_ALGORITHM
    # The repaired laboratory satisfies the *intended* property instead.
    r = ScopedRNG("7b" * 32, STREAM, "G13_SCOPE")
    assert r.draw(7, "slot", "cset").sampler == REQUIRED_ADP020_ALGORITHM
