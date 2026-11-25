"""R12: actual R11 saved sourcefree empirical path -> independent R48 world.

Same sourcefree repertoire evidence and same public account, different explicit
institutional allocation premise. The actual runtime owns experience and revision.
No native WVS results, live LLM, or automatic inference of a person's position.
"""
from copy import deepcopy

import pytest

from test_repertoire_inquiry import _session, run
from authored_world_handoff import prepare_repertoire_authored_history, verify_handoff, repertoire_source_seals
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import blank_world, adult
from um_sorok_organism.material_conjunction import admit_authored_structural_history
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService


def authored_alternative(inquiry, access):
    # An independent relief channel can change the practical ability to
    # refuse employer-controlled resources. Neither the presence nor the
    # eligibility rule follows from survey answers.
    return prepare_repertoire_authored_history(
        inquiry, scenario_id="fictional-independent-relief-" + access,
        rationale="Contrast practical subsistence options under the same selective entitlement repertoire.",
        positions=[{"id": "position", "actor": "worker", "field": "relief_access",
                    "value": access, "effective_from": 0, "effective_until": 1}],
        rules=[{"id": "gate", "operation": "EAT", "location": "home",
                "effective_from": 0, "effective_until": 1,
                "all_of": [{"kind": "RECORDED_POSITION", "field": "relief_access",
                            "equals": "admitted"}]}],
        public_notices=[{"id": "food_notice", "public": True, "location": "home",
                         "public_terms": ["eat", "available"],
                         "public_text": "Food is available here.",
                         "effective_from": 0, "effective_until": 20}])


def run_world(db, handoff):
    assert verify_handoff(handoff)
    stage = "read"

    def policy(task, packet):
        if task == "expression":
            return {"task": task, "surface": "Ordinary activity."}
        if task == "actor_attempt":
            rows = [x for o in packet["options"] if o["action"] == "EAT"
                    for x in o.get("fallible_notice_expectations", [])]
            if stage in ("attempt", "later"):
                assert len(rows) == 1
                if rows[0]["anticipated_availability"] == "AVAILABLE":
                    return {"task": task, "action": "EAT", "project_id": "food",
                            "notice_expectation_ref": rows[0]["expectation_ref"]}
            return {"task": task, "action": "WAIT"}
        if task == "development":
            if stage == "read":
                rows = packet["historically_possible_notice_expectations"]
                assert len(rows) == 1
                return {"task": task, "candidates": [{
                    "kind": "ACQUIRE_NOTICE_EXPECTATION", "basis": rows[0],
                    "anticipated_availability": "AVAILABLE"}]}
            if stage == "attempt":
                rows = packet["historically_possible_notice_revisions"]
                assert len(rows) == 1 and rows[0]["actual_hidden_cause"] == "NOT_KNOWN"
                return {"task": task, "candidates": [{
                    "kind": "REVISE_NOTICE_EXPECTATION", "basis": rows[0],
                    "revision": "UNAVAILABLE" if rows[0]["own_course"] == "INCOMPLETE" else "RETAIN"}]}
            return {"task": task, "candidates": []}
        raise AssertionError(task)

    service = ValidatingSemanticService(CallbackLLMProvider(policy))
    rt = ConstitutiveRuntime(str(db), semantic=service)
    try:
        w = blank_world()
        # Research-only authored public sign, never a psychological fact.
        w["public_notices"] = deepcopy(handoff["evidence"]["public_notices"])
        spec = handoff["authored_structural_history"]
        admit_authored_structural_history(w, {"worker"}, spec)
        a = adult("worker", "Mara")
        a["projects"] = [{"id": "food", "object": "sustain nutrition",
                          "means": ["EAT"], "priority": .5, "status": "active"}]
        rt.ledger.initialize(w, [a], source_seals=repertoire_source_seals(handoff))
        assert rt.step("worker", requested_action="INSPECT", object_ref="food_notice")["status"] == "PERFORMED"
        assert rt.ledger.actor("worker")[1]["institutional_expectations"][0]["anticipated_availability"] == "AVAILABLE"
        stage = "attempt"
        before = rt.ledger.world()[1]["sites"]["home"]["food"]
        attempted = rt.step("worker")
        delta = rt.ledger.world()[1]["sites"]["home"]["food"] - before
        acquired = rt.ledger.actor("worker")[1]["institutional_expectations"][0]
        assert rt.verify()["valid"]
    finally:
        rt.close()
    # Reopen the actual same-world continuation, not a newly created actor.
    rt = ConstitutiveRuntime(str(db), semantic=service)
    try:
        stage = "later"
        source = rt.ledger.source(handoff["authored_structural_history"]["source_ref"])
        assert source["category"] == "FICTIONAL_FF_REPERTOIRE_CONDITIONING_NOT_NATIVE_ISSUANCE"
        assert source["content"] == handoff and verify_handoff(source["content"])
        assert rt.ledger.source("authored_structural_history")["content"] == handoff["authored_structural_history"]
        before = rt.ledger.world()[1]["sites"]["home"]["food"]
        later = rt.step("worker")
        later_delta = rt.ledger.world()[1]["sites"]["home"]["food"] - before
        assert rt.ledger.world()[1]["public_notices"][0]["public_text"] == "Food is available here."
        assert rt.verify()["valid"]
    finally:
        rt.close()
    return attempted["status"], delta, acquired["anticipated_availability"], later["attempt"], later_delta


def test_actual_inquiry_to_two_institutional_alternatives_and_cold_lived_course(tmp_path, monkeypatch):
    session, q = _session(tmp_path / "survey", monkeypatch, 0)
    with session:
        inquiry = run(session, q)
    assert inquiry["reverse"]["material"]["raw_selected_full_case_n"] == 1
    allowed, denied = [authored_alternative(inquiry, a) for a in ("admitted", "excluded")]
    assert allowed["evidence"] == denied["evidence"]
    assert allowed["content_hash"] != denied["content_hash"]
    assert run_world(tmp_path / "allowed.db", allowed) == ("PERFORMED", -1, "AVAILABLE", "EAT", -1)
    assert run_world(tmp_path / "denied.db", denied) == ("BLOCKED", 0, "UNAVAILABLE", "WAIT", 0)


def test_native_context_and_altered_projection_cannot_enter_experiment(tmp_path, monkeypatch):
    session, q = _session(tmp_path, monkeypatch, 0)
    with session:
        inquiry = run(session, q)
    bad = deepcopy(inquiry)
    bad["independent_native_context"] = {"grade": "NATIVE_RETROSPECTIVE_CONTEXT_NOT_WORLD_AUTHORITY",
                                         "observations": []}
    with pytest.raises(ValueError):
        authored_alternative(bad, "admitted")
    bad = deepcopy(inquiry)
    bad["reverse"]["material"]["complete_output_cells"][0]["raw_count"] += 1
    with pytest.raises(ValueError):
        authored_alternative(bad, "admitted")
    packet = authored_alternative(inquiry, "admitted")
    packet["authored_structural_history"]["positions"][0]["value"] = "excluded"
    assert not verify_handoff(packet)


def test_existing_ledger_refuses_tampered_repertoire_sidecar(tmp_path, monkeypatch):
    import sqlite3
    from um_sorok_organism.storage import Conflict
    session, q = _session(tmp_path / "survey", monkeypatch, 0)
    with session:
        inquiry = run(session, q)
    packet = authored_alternative(inquiry, "admitted")
    db = str(tmp_path / "tampered.db")
    rt = ConstitutiveRuntime(db)
    try:
        w = blank_world()
        spec = packet["authored_structural_history"]
        w["public_notices"] = deepcopy(packet["evidence"]["public_notices"])
        admit_authored_structural_history(w, {"worker"}, spec)
        rt.ledger.initialize(w, [adult("worker", "Mara")],
                             source_seals=repertoire_source_seals(packet))
        assert rt.ledger.source(spec["source_ref"])["content"] == packet
    finally:
        rt.close()
    with sqlite3.connect(db) as conn:
        conn.execute("UPDATE source_seals SET content=? WHERE id=?", ("{}", spec["source_ref"]))
    rt = ConstitutiveRuntime(db)
    try:
        with pytest.raises(Conflict):
            rt.ledger.source(spec["source_ref"])
    finally:
        rt.close()
