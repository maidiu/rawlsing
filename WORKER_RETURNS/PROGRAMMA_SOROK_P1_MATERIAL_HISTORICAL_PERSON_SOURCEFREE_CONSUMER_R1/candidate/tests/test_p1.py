"""P1 sourcefree four-trajectory and invariant tests."""
from __future__ import annotations

import json
import sqlite3

import pytest

from p1_consumer import run_trajectories
from p1_s35 import evaluate
from joined.session import JoinedSession
from r30a.first_session import SessionRefusal
from r31j.scenarios import evaluated
import firstclass


@pytest.fixture(scope="module")
def results(tmp_path_factory):
    root = tmp_path_factory.mktemp("p1-four")
    return run_trajectories(root)


def test_four_material_trajectories_have_required_differences(results):
    t = results["trajectories"]
    a, b, c, d = t["A"], t["B"], t["C"], t["D"]
    assert a["source"]["b_operation"] == "SHARE_TOOL"
    assert b["source"]["b_operation"] == "SHARE_TOOL"
    assert a["source"]["b_event_hash"] == b["source"]["b_event_hash"]
    assert a["a_access_admitted"] is True
    assert b["a_access_admitted"] is False
    assert a["target_id"]
    assert b["target_id"] == ""
    assert b["a_response"] is None
    assert a["a_help"]["accepted"] is True
    assert b["s35"]["status"] == "UNKNOWN_RECEIVABILITY"
    assert c["source"]["b_operation"] == "REFUSE_TOOL"
    assert c["target_id"] == ""
    assert c["a_help"]["accepted"] is False
    assert c["s35"]["status"] == "OBSERVED_CURRENT_REFUSAL"
    assert d["omitted"]["a_tools_remaining"] == 1
    assert d["performed"]["a_tools_remaining"] == 0
    assert d["omitted"]["a_help"]["strategy"] == "HELP_ACCEPT"
    assert d["performed"]["a_help"]["strategy"] == "HELP_REFUSE"
    assert d["omitted"]["a_action"] == "OMIT"
    assert d["performed"]["a_action"] == "ATTEND_OBJECT"
    assert results["invariants"]["A_B_same_b_event_hash"] is True


def test_every_s35_case_keeps_t_no_change_and_no_grant():
    cases = [
        evaluate(access=True, actions=("REQUEST_TOOL",), b_operation="SHARE_TOOL"),
        evaluate(access=False, b_operation="SHARE_TOOL"),
        evaluate(access=True, actions=(), b_operation="SHARE_TOOL"),
        evaluate(access=True, actions=(), contradictory=True, b_operation="SHARE_TOOL"),
        evaluate(access=True, actions=("EXPLICIT_REFUSAL",), b_operation="REFUSE_TOOL"),
        evaluate(access=True, actions=("ATTEND_OBJECT",), b_operation="SHARE_TOOL"),
    ]
    assert [x["status"] for x in cases] == [
        "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION",
        "UNKNOWN_RECEIVABILITY",
        "RECEIVABLE_NO_OBSERVED_UPTAKE",
        "AMBIGUOUS_CONTRADICTORY",
        "OBSERVED_CURRENT_REFUSAL",
        "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION",
    ]
    for case in cases:
        assert case["t"]["operation"] == "NO_CHANGE"
        assert case["t"]["target_proposal"] is None
        assert case["t"]["grant"] is None
        assert case["t"]["beforestate_mutation"] is False
        assert case["native"] is False


def test_s35_n3_same_message_distinct_causes_n4_label_invariance_n5_prior_acts(results):
    c = results["trajectories"]["C"]
    d = results["trajectories"]["D"]["performed"]
    assert c["a_help"]["strategy"] == d["a_help"]["strategy"] == "HELP_REFUSE"
    assert c["source"]["b_event_hash"] != d["source"]["b_event_hash"]
    assert c["s35"]["a_response"] != d["s35"]["a_response"]
    a = evaluate(access=True, actions=("REQUEST_TOOL",), b_operation="SHARE_TOOL")
    labelled = evaluate(access=True, actions=("REQUEST_TOOL",), b_operation="SHARE_TOOL",
                        labels=("class_label=ALTERED", "demographic_label=ALTERED"))
    assert a["status"] == labelled["status"]
    assert a["t"] == labelled["t"]
    prior = evaluate(access=True, actions=(), b_operation="SHARE_TOOL",
                     prior_acts=("TEST_ONLY_ENACT_1", "TEST_ONLY_ENACT_2"))
    assert prior["status"] == "RECEIVABLE_NO_OBSERVED_UPTAKE"
    assert prior["t"] == a["t"]


def test_source_preimage_forgery_replay_still_stops_before_c8(tmp_path):
    case = evaluated(share=True, e2=False)["case"]
    base = firstclass.source_from_case(case)
    mutations = {
        "wrong_owner": {"b_owner": "FAKE_OWNER"},
        "wrong_event_ref": {"b_event_ref": "TEST_ONLY_FAKE_EVENT"},
        "wrong_event_hash": {"b_event_hash": "0" * 64},
        "wrong_clock": {"b_clock": 999},
        "wrong_operation": {"b_operation": "REFUSE_TOOL", "b_quantity": 0},
        "wrong_quantity": {"b_quantity": 5},
        "wrong_e1_ref": {"a_e1_ref": "TEST_ONLY_FAKE_E1"},
        "wrong_e1_hash": {"a_e1_hash": "0" * 64},
        "wrong_e1_clock": {"a_e1_clock": 999},
    }
    for label, change in mutations.items():
        source = dict(base)
        source.update(change)
        root = tmp_path / label
        with pytest.raises(firstclass.MaterialSourceRefusal) as exc:
            firstclass.c9_only(root, case=case, source=source)
        assert exc.value.code == "MATERIAL_SOURCE_PREIMAGE_MISMATCH"
        assert not (root / "bp2").exists()


def test_no_access_history_persists_b_share_without_a_response(results):
    b = results["trajectories"]["B"]
    assert b["view"]["source"]["b_operation"] == "SHARE_TOOL"
    assert b["view"]["source"]["b_event_hash"] == results["trajectories"]["A"]["source"]["b_event_hash"]
    assert b["view"]["a_tools"] == 0
    assert b["view"]["a_access_admitted"] is False
    assert b["view"]["a_response"] is None
    assert b["view"]["target_id"] == ""
    assert b["view"]["c12"]["ok"] is True
    assert b["cold"]["c12"]["ok"] is True
    assert b["cold"]["view"]["episodes"]


def test_c12_cold_tamper_and_exact_restore(tmp_path):
    state = tmp_path / "tamper"
    session = JoinedSession.start(state, perform="omit")
    try:
        assert session.verify()["ok"] is True
    finally:
        session.close()
    db_path = state / "product" / "c12.sqlite"
    backup = db_path.read_bytes()
    db = sqlite3.connect(db_path)
    try:
        db.execute("DROP TRIGGER episode_no_update")
        row = db.execute("SELECT body FROM episode WHERE branch_id='root' AND seq=0").fetchone()
        body = json.loads(row[0])
        body["p1_tamper"] = True
        db.execute("UPDATE episode SET body=? WHERE branch_id='root' AND seq=0",
                   (json.dumps(body),))
        db.commit()
    finally:
        db.close()
    with pytest.raises(SessionRefusal):
        JoinedSession.open(state)
    db_path.write_bytes(backup)
    reopened = JoinedSession.open(state)
    try:
        assert reopened.verify()["ok"] is True
    finally:
        reopened.close()


def test_coordinated_selfhash_edit_is_custody_hold_not_production_accept(tmp_path):
    state = tmp_path / "coordinated"
    session = JoinedSession.start(state, perform="omit")
    try:
        assert session.verify()["ok"] is True
    finally:
        session.close()
    db_path = state / "product" / "c12.sqlite"
    db = sqlite3.connect(db_path)
    try:
        db.execute("DROP TRIGGER episode_no_update")
        row = db.execute("SELECT body,hash FROM episode WHERE branch_id='root' AND seq=0").fetchone()
        body = json.loads(row[0])
        body["p1_coordinated_selfhash"] = True
        from bp1.canon import digest
        preimage = {key: value for key, value in body.items() if key != "hash"}
        preimage.pop("episode_id", None)
        body["hash"] = digest(preimage)
        db.execute("UPDATE episode SET body=?,hash=? WHERE branch_id='root' AND seq=0",
                   (json.dumps(body, sort_keys=True), body["hash"]))
        db.commit()
    finally:
        db.close()
    selfhash = JoinedSession.open(state)
    try:
        assert selfhash.verify()["ok"] is True
        assert selfhash.meta.get("c12_grade") is None
    finally:
        selfhash.close()


def test_same_person_fork_preserves_root_and_alt(tmp_path):
    session = JoinedSession.start(tmp_path / "fork", perform="omit")
    try:
        fork = session.fork_alt()
        assert fork
        assert session.product.c12_verify("root")["ok"] is True
        assert session.product.c12_verify("alt")["ok"] is True
        assert session.verify()["ok"] is True
    finally:
        session.close()
