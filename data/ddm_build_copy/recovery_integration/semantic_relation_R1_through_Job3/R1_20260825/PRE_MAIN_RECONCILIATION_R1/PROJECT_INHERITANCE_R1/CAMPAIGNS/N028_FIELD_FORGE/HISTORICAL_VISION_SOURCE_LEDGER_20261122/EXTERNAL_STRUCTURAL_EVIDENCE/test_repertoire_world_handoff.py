"""R12: actual R11 saved sourcefree empirical path -> independent R48 world.

Same sourcefree repertoire evidence and same public account, different explicit
institutional allocation premise. The actual runtime owns experience and revision.
No native WVS results, live LLM, or automatic inference of a person's position.
"""
from copy import deepcopy

import pytest

from test_repertoire_inquiry import _session, run, _concept_session, _develop_run
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


def _formation_case(concept, access):
    from authored_world_handoff import formation_repertoire_offers, prepare_formation_authored_history
    offers=formation_repertoire_offers(concept)
    # Two different positive repertoires from the same exact observed
    # position slice, not two demographic identities.
    sl=next(s for s in offers["slices"] if s["inquiry"]=="entitlement"
            and len(s["position_axes"])==2 and len(s["offer_ids"])>=2)
    first,second=sl["offer_ids"][:2]
    def formation(id,oid,controller,renewal):
        return {"id":id,"arena":"relief provision","carrier_roles":["worker","household"],
                "offer_ids":[oid],"public_notice_ids":["food_notice"],
                "interpretation":"fictional rival institutional practice",
                "reproduction_channels":[{"resource":"food","provider_role":"provision group",
                    "controller_role":controller,"beneficiary_role":"household",
                    "cost_bearer_role":"worker","renewal_condition":renewal,"rule_id":"gate"}]}
    return prepare_formation_authored_history(concept,scenario_id="formation-"+access,
        rationale="Same source-local rival repertoire possibilities; independently authored provision.",
        formation_choices=[formation("patron",first,"patron","employment continues"),
                           formation("mutual-aid",second,"collective","reserve renewed")],
        positions=[{"id":"position","actor":"worker","field":"relief_access",
                    "value":access,"effective_from":0,"effective_until":1}],
        rules=[{"id":"gate","operation":"EAT","location":"home","effective_from":0,
                "effective_until":1,"all_of":[{"kind":"RECORDED_POSITION",
                                              "field":"relief_access","equals":"admitted"}]}],
        public_notices=[{"id":"food_notice","public":True,"location":"home",
                         "public_terms":["eat","available"],"public_text":"Food is available here.",
                         "effective_from":0,"effective_until":20}])


def test_r17_actual_concept_to_overlapping_formations_and_world_course(tmp_path,monkeypatch):
    session,inquiries=_concept_session(tmp_path/"survey",monkeypatch)
    with session:
        concept=_develop_run(session,inquiries)
    admitted,excluded=[_formation_case(concept,a) for a in ("admitted","excluded")]
    assert verify_handoff(admitted) and verify_handoff(excluded)
    assert admitted["evidence"]==excluded["evidence"]
    assert admitted["content_hash"]!=excluded["content_hash"]
    r=admitted["evidence"]["relations"][0]
    assert r["shared_possible_carrier_roles"]==["household","worker"]
    assert len(r["distinct_supported_motif_pairs"])==1
    assert not r["shared_resource_channels"][0]["same_controller"]
    assert r["actual_membership_or_conflict"]=="NOT_INFERRED"
    for f in admitted["evidence"]["formations"]:
        assert len(f["retained_alternatives"])>=2
        assert len(f["selected_offers"])==1
    assert run_world(tmp_path/"allowed-formation.db",admitted)==("PERFORMED",-1,"AVAILABLE","EAT",-1)
    assert run_world(tmp_path/"denied-formation.db",excluded)==("BLOCKED",0,"UNAVAILABLE","WAIT",0)


def test_r17_altered_concept_or_unobserved_offer_refused(tmp_path,monkeypatch):
    from authored_world_handoff import prepare_formation_authored_history, formation_repertoire_offers
    session,inquiries=_concept_session(tmp_path/"survey",monkeypatch)
    with session:
        concept=_develop_run(session,inquiries)
    packet=_formation_case(concept,"admitted")
    broken=deepcopy(concept)
    broken["records"][0]["local_discovery"]["records"][0]["candidates"][0]["baseline_n"]+=1
    with pytest.raises(ValueError,match="sealed record"):
        formation_repertoire_offers(broken)
    choices=deepcopy(packet["evidence"]["formation_choices"])
    choices[0]["offer_ids"]=["invented"]
    with pytest.raises(ValueError,match="positive scoped offers"):
        prepare_formation_authored_history(concept,formation_choices=choices,
            public_notices=packet["evidence"]["public_notices"],**packet["fictional_choice"])
    choices=deepcopy(packet["evidence"]["formation_choices"])
    choices[0]["reproduction_channels"][0]["rule_id"]="invented"
    with pytest.raises(ValueError,match="authored material rule"):
        prepare_formation_authored_history(concept,formation_choices=choices,
            public_notices=packet["evidence"]["public_notices"],**packet["fictional_choice"])


def test_r17_distinct_cohorts_and_unselected_inquiries_remain_separate(tmp_path,monkeypatch):
    from authored_world_handoff import formation_repertoire_offers
    session,inquiries=_concept_session(tmp_path/"survey",monkeypatch)
    with session:
        concept=_develop_run(session,inquiries,query_budget=2)
    out=formation_repertoire_offers(concept)
    assert {s["inquiry"] for s in out["slices"]}=={"entitlement","property"}
    assert len({s["knowledge_ref"]["content_hash"] for s in out["slices"]})==2
    assert out["unexamined"]==[{"id":"authority","state":"UNKNOWN_SCHEDULED"}]
    assert out["pooled_joint"] is None
