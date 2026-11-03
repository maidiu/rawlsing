"""Adversarial sourcefree tests for LIVE-02, using real Git identities.

Run only on a local repo containing exact W8-R/7bf/JOIN-V/P1/RRIF source cuts.
All state/journal writes occur under pytest tmp_path, never committed P0/P1 state.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

import evidence_store as es
import living_reference as lr
import live_update_adapter as ad

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures"


def packet(name):
    return json.loads((FIXTURE / name).read_text(encoding="utf-8"))


def state_env(tmp_path):
    journal = tmp_path / "evidence" / "journal.jsonl"
    state_path = tmp_path / "state.json"
    lr.commit_event(lr._event("GENESIS", {"baseline_sha": lr.ENGINEERING_BASELINE},
                              created_at="2026-11-03T11:00:00+00:00"),
                    journal_path=journal, state_path=state_path)
    return journal, state_path


def append_fixture(state_path, fixture, head=None):
    journal = lr._journal_path(state_path)
    return ad.commit_delta(fixture, state_path=state_path,
                           expected_head=head or es.journal_head(journal))


@pytest.fixture(scope="module", autouse=True)
def source_preflight():
    # Do not silently skip. An exact fetch is a required runner precondition.
    idx = ad.guide_index()
    assert idx["cut"] == ad.GUIDE_SHA and len(idx["gates"]) == 83
    for name in ("join_e_scoped_review.json", "s35_authored_sourcefree.json",
                 "rrif_r2_negative.json"):
        f = packet(name)
        assert f["guide_sha"] == ad.GUIDE_SHA
        assert lr._git(["cat-file", "-t", f["return_sha"]]) == "commit"


def test_real_join_e_then_s35_cold_replay_and_one_entry_work_now(tmp_path):
    journal, st = state_env(tmp_path)
    joined = append_fixture(st, packet("join_e_scoped_review.json"))
    assert joined["applied"]["status"] == "SCOPED_SOURCEFREE_ACCEPTED"
    p1 = append_fixture(st, packet("s35_authored_sourcefree.json"))
    assert p1["applied"]["status"] == "SOURCE_PRESENT_CANDIDATE"
    loaded = lr._load_state(st)
    cold = lr.rebuild_from_journal(journal, operating=True)
    assert loaded["state_digest"] == cold["state_digest"]
    assert loaded["journal_head"] == cold["journal_head"]
    assert loaded["work_now"]["programma_live"]["changed_refs"] == ["E021@VERIFY", "O05@ACCEPT"]
    now = ad.query(loaded, "work-now")
    assert any(x["ref"] == "E021@VERIFY" for x in now["live_phase_changes"])
    assert any(x["ref"] == "O05@ACCEPT" for x in now["live_phase_changes"])
    s35 = next(x for x in now["live_phase_changes"] if x["ref"] == "O05@ACCEPT")
    assert s35["receipts"][0]["code_reader"] == "NONE"
    assert loaded["programma_live"]["native_person_human_claims"] == "NONE_ISSUED"
    assert not any(r["target_stage_issued"] for r in loaded["programma_live"]["gates"].values())
    assert loaded["programma_live"]["gates"]["G-C9-T-ANY"]["decision"] == "MODE_UNSELECTED_HOLD"
    assert loaded["programma_live"]["gates"]["G-C9-T-IF-ACQUIRED"]["decision"] == "MODE_UNSELECTED_HOLD"


def test_duplicate_event_idempotent_no_new_journal_or_state_revision(tmp_path):
    journal, st = state_env(tmp_path)
    p = packet("join_e_scoped_review.json")
    first = append_fixture(st, p)
    before = journal.read_bytes()
    rev = lr._load_state(st)["revision"]
    second = append_fixture(st, p, head=first["event"]["prev_event_hash"])
    assert second["status"] == "DUPLICATE_PROGRAMMA_DELTA_IDEMPOTENT"
    assert second["no_write"] is True
    assert journal.read_bytes() == before
    assert lr._load_state(st)["revision"] == rev


def test_exact_order_inversion_same_claims_not_different_science(tmp_path):
    j1, s1 = state_env(tmp_path / "a")
    j2, s2 = state_env(tmp_path / "b")
    j = packet("join_e_scoped_review.json")
    p = packet("s35_authored_sourcefree.json")
    append_fixture(s1, j); append_fixture(s1, p)
    append_fixture(s2, p); append_fixture(s2, j)
    a = lr._load_state(s1)["programma_live"]
    b = lr._load_state(s2)["programma_live"]
    assert a["changed_refs"] == b["changed_refs"]
    assert a["active_receipts"] == b["active_receipts"] == 2
    assert {k: v["decision"] for k, v in a["gates"].items()} == {
        k: v["decision"] for k, v in b["gates"].items()}
    assert es.read_journal(j1)[-1]["kind"] == "PROGRAMMA_DELTA"


def test_missing_transition_is_not_inferred(tmp_path):
    _, st = state_env(tmp_path)
    append_fixture(st, packet("join_e_scoped_review.json"))
    state = lr._load_state(st)
    since = ad.query(state, "changes-since", "JOIN_E_7BF_SCOPED_REVIEW")
    assert since["count"] == 0
    assert "O05@ACCEPT" not in state["programma_live"]["changed_refs"]
    assert state["programma_live"]["gates"]["G-C9-T-ANY"]["decision"] == "MODE_UNSELECTED_HOLD"


def test_independent_negative_exact_cut_preserves_unrelated_join_acceptance(tmp_path):
    journal, st = state_env(tmp_path)
    append_fixture(st, packet("join_e_scoped_review.json"))
    append_fixture(st, packet("rrif_r2_negative.json"))
    s = lr._load_state(st)
    assert s["programma_live"]["active_receipts"] == 2
    d = {x["ref"]: x for x in s["programma_live"]["pending"]}
    assert d["E021@VERIFY"]["receipts"][0]["kind"] == "SCOPED_REVIEW"
    assert d["C12@VERIFY"]["receipts"][0]["kind"] == "REVIEW_REVISE"
    assert d["C12@VERIFY"]["receipts"][0]["source_cut"] == ad.REVIEW_RRIF_SUBJECT
    assert not s["programma_live"]["gates"]["G-C12-SF-VERIFY"]["target_stage_issued"]
    assert not s["programma_live"]["gates"]["G-C12-NATIVE-INTEGRATE"]["target_stage_issued"]
    assert lr.rebuild_from_journal(journal, operating=True)["state_digest"] == s["state_digest"]


@pytest.mark.parametrize("mutation,reason", [
    (lambda f: f.update({"owner_slot": "SOROK_HQ"}), "FABRICATED_OR_MISMATCHED_OWNER_SLOT"),
    (lambda f: f.update({"grade": "NATIVE"}), "UNISSUED_NATIVE_OWNER_OR_HUMAN_GRADE"),
    (lambda f: f.update({"guide_sha": "f" * 40}), "GUIDE_CUT_MISMATCH"),
    (lambda f: f["source"].update({"blob": "f" * 40}), "FORGED_OR_MISSING_GIT_SOURCE"),
    (lambda f: f["coordinate"].update({"root": "C784_NEW_ROOT"}), "SCOPED_ACCEPTANCE_CROSS_ROOT"),
    (lambda f: f["coordinate"].update({"first_consumer_symbol": "unavailable_symbol"}), "FIRST_CONSUMER_SYMBOL_NOT_IN_CODE"),
    (lambda f: f["coordinate"].update({"code_sha": "f" * 40}), "CODE_SHA_CROSS_CUT"),
    (lambda f: f.update({"caller_verified": True}), "CALLER_SELF_GRANT_NOT_EVIDENCE"),
    (lambda f: f.update({"claim_mode": "POSITIVE_ACQUISITION"}), "OWNER_SELECTOR_NOT_ISSUED"),
    (lambda f: f["review"].update({"commit": "f" * 40}), "SCOPED_ACCEPTANCE_CROSS_REVIEW"),
    (lambda f: f["coordinate"].update({"code": None, "first_consumer_symbol": "NONE"}), "REVIEW_CONSUMER_CODE_REQUIRED"),
])
def test_forgery_and_cross_cut_refusals_do_not_append(tmp_path, mutation, reason):
    journal, st = state_env(tmp_path)
    source = packet("join_e_scoped_review.json")
    mutation(source)
    before = journal.read_bytes()
    with pytest.raises(ad.DeltaRefused, match=reason):
        append_fixture(st, source)
    assert journal.read_bytes() == before


def test_strict_cas_rejects_concurrent_writer_but_preserves_original_append_path(tmp_path):
    journal, st = state_env(tmp_path)
    stale = es.journal_head(journal)
    append_fixture(st, packet("join_e_scoped_review.json"), head=stale)
    before = journal.read_bytes()
    with pytest.raises(lr.StaleStateRevision, match="PROGRAMMA_DELTA_STALE_CAS_HEAD"):
        append_fixture(st, packet("s35_authored_sourcefree.json"), head=stale)
    assert journal.read_bytes() == before
    assert lr._load_state(st)["programma_live"]["changes"] == 1


def test_duplicate_transition_id_different_body_is_refused(tmp_path):
    journal, st = state_env(tmp_path)
    initial = packet("s35_authored_sourcefree.json")
    append_fixture(st, initial)
    changed = copy.deepcopy(initial)
    changed["next_evidence"] = "EVIDENCE SWAPPED UNDER SAME ID"
    before = journal.read_bytes()
    with pytest.raises(ValueError, match="DUPLICATE_PROGRAMMA_DELTA_ID_DIFFERENT_PAYLOAD"):
        append_fixture(st, changed)
    assert journal.read_bytes() == before


def test_source_free_author_fixture_never_implies_positive_acquisition(tmp_path):
    _, st = state_env(tmp_path)
    append_fixture(st, packet("s35_authored_sourcefree.json"))
    state = lr._load_state(st)
    assert state["axes"]["CAN011_RULE_T_MISSING"]["science"] != "ORIGINAL_ISSUED"
    assert state["programma_live"]["gates"]["G-O05-POSITIVE-ACCEPT"]["decision"] != "ELIGIBLE_PREREQUISITES_ONLY"
    assert state["programma_live"]["gates"]["G-C9-T-ANY"]["decision"] == "MODE_UNSELECTED_HOLD"
    assert ad.query(state, "candidate-patch")["status"] == "HQ_REVIEW_PATCH_CANDIDATE_NOT_APPLIED"


def test_existing_p0_p1_withdrawal_engine_is_reused_not_replaced(tmp_path):
    journal, st = state_env(tmp_path)
    # The existing journal retains requests and qualification; a caller-provided
    # unqualified source withdrawal is refused by existing P0/P1 transition law.
    fixture = {
        "node_id": "P1_B_MATERIAL_SOURCE",
        "dimension": "source_recovery",
        "to": "SOURCE_WITHDRAWN",
        "evidence": {"kind": "SOURCE_WITHDRAWAL", "basis": "SOURCE_OWNER_WITHDRAWAL",
                     "authority": "UNVERIFIED_CALLER", "scope": ["DIFFERENT_NODE"]},
    }
    lr.commit_event(lr._event("TRANSITION_REQUEST", {"fixture": fixture}),
                    journal_path=journal, state_path=st)
    state = lr._load_state(st)
    assert state["journal_applied"][-1]["status"] == "REFUSED"
    assert state["axes"]["P1_B_MATERIAL_SOURCE"]["source_recovery"] != "SOURCE_WITHDRAWN"
    assert state["readiness"]["science"] == "HOLD_NOT_ISSUED"


def test_original_qualified_withdraw_restore_and_negative_independence(tmp_path):
    journal, st = state_env(tmp_path)
    append_fixture(st, packet("join_e_scoped_review.json"))
    baseline = lr._load_state(st)
    join_before = [x for x in baseline["programma_live"]["pending"]
                   if x["ref"] == "E021@VERIFY"][0]
    node_id = "P1_B_MATERIAL_SOURCE"
    ref = lr._node_map(baseline)[node_id]["source_refs"][0]
    source = {"commit": ref["commit"], "path": ref["path"],
              "blob": ref.get("blob") or ref.get("object_id"), "object_type": "blob"}
    basis = "QUALIFIED_ABSENCE_VERIFICATION"
    withdrawal = lr.commit_event(lr._event("EVIDENCE_WITHDRAWAL", {
        "node_id": node_id, "basis": basis, "authority": "SOROK_HQ",
        "scope": [node_id], "reason": "sourcefree qualified absence challenge",
    }), journal_path=journal, state_path=st)
    lr.commit_event(lr._event("TRANSITION_REQUEST", {"fixture": {
        "node_id": node_id, "dimension": "source_recovery",
        "to": "SOURCE_NOT_FOUND",
        "evidence": {"kind": "SOURCE_WITHDRAWAL", "basis": basis,
                     "authority": "SOROK_HQ", "scope": [node_id],
                     "withdrawal_event_id": withdrawal["event"]["event_id"]},
    }}), journal_path=journal, state_path=st)
    withdrawn = lr._load_state(st)
    assert withdrawn["axes"][node_id]["source_recovery"] == "SOURCE_NOT_FOUND"
    assert withdrawn["programma_live"]["native_person_human_claims"] == "NONE_ISSUED"
    assert next(x for x in withdrawn["programma_live"]["pending"]
                if x["ref"] == "E021@VERIFY")["receipts"] == join_before["receipts"]
    lr.commit_event(lr._event("TRANSITION_REQUEST", {"fixture": {
        "node_id": node_id, "dimension": "source_recovery",
        "to": "SOURCE_VERIFIED",
        "evidence": {"kind": "SOURCE_RECORD", "source": source},
    }}), journal_path=journal, state_path=st)
    restored = lr._load_state(st)
    assert restored["axes"][node_id]["source_recovery"] == "SOURCE_VERIFIED"
    assert restored["programma_live"]["native_person_human_claims"] == "NONE_ISSUED"
    assert lr.rebuild_from_journal(journal, operating=True)["state_digest"] == restored["state_digest"]


def test_unverified_event_erasure_of_delta_refused_and_replay_fail_closed(tmp_path):
    journal, st = state_env(tmp_path)
    accepted = append_fixture(st, packet("join_e_scoped_review.json"))
    eid = accepted["event"]["event_id"]
    spoof = lr._event("EVIDENCE_WITHDRAWAL", {
        "withdraws_event_id": eid, "basis": "SOURCE_OWNER_WITHDRAWAL",
        "authority": "SOROK_HQ", "node_id": "JOIN_E_7BF",
        "reason": "caller-written claim is not source-owner custody",
    })
    before = journal.read_bytes()
    with pytest.raises(ValueError, match="PROGRAMMA_DELTA_EVENT_ERASURE_REQUIRES_VERIFIED_OWNER_CUSTODY"):
        lr.commit_event(spoof, journal_path=journal, state_path=st)
    assert journal.read_bytes() == before
    # Even if a lower-level actor bypasses the commit API and directly appends,
    # replay does not let a textual principal silently suppress DELTA evidence.
    es.append_event(journal, spoof)
    cold = lr.rebuild_from_journal(journal, operating=True)
    assert cold["programma_live"]["active_receipts"] == 1
    assert any(r["transition_id"] == "JOIN_E_7BF_SCOPED_REVIEW" for r in cold["programma_deltas"])


def test_unrelated_real_git_source_cannot_manufacture_node_claim(tmp_path):
    journal, st = state_env(tmp_path)
    f = packet("s35_authored_sourcefree.json")
    wrong = packet("join_e_scoped_review.json")
    f["source"] = wrong["source"]
    f["return_sha"] = wrong["return_sha"]
    f["subject_sha"] = wrong["subject_sha"]
    f["locator"] = wrong["locator"]
    f["coordinate"]["source_cut"] = wrong["subject_sha"]
    before = journal.read_bytes()
    with pytest.raises(ad.DeltaRefused, match="RETURN_SOURCE_NOT_A_NODE_ORIGINAL_SOURCE"):
        append_fixture(st, f)
    assert journal.read_bytes() == before


def test_first_entry_without_new_delta_discloses_unprocessed_work(tmp_path):
    _, st = state_env(tmp_path)
    state = lr._load_state(st)
    answer = ad.query(state, "freshness")
    assert answer["changes_since_guide_cut"] == 0
    assert answer["pending_qualification"] == "NO_NEW_PROGRAMMA_DELTA_INGESTED__HISTORICAL_BASELINE_ONLY"
    assert answer["adoption"] == "OWNER_PENDING"
