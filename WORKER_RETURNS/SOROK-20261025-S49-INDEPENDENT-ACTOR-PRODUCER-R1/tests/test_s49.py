"""Focused S49 independent B producer tests."""
from __future__ import annotations
import pytest
from s49.bootstrap import install
install()
from s45.fixtures import root_bundle
from s37.harness import case_for, source_for
from s49.session import S49Session
from s49.actor import MISSING_B_CONTEXT, controlled_b_sources, record_b_observation


def _start(state):
    case=case_for(True)
    return S49Session.start(state,bundle=root_bundle("01"*32),case=case,source=source_for(case),language_context={"milieu_id":"workshop"})

def _identity(s):
    w=s.world()
    return (len(w.events),s.clock(),w.actor_state["B"].get("material_remaining"),len(s.read_events()),s.read_root()["root_hash"])

def test_actual_root_without_b_context_holds_without_b_event_or_c8(tmp_path):
    s=_start(tmp_path/"actual")
    try:
        record_b_observation(s)
        before=_identity(s)
        r=s.produce_b_turn(controlled=False)
        assert r["status"]=="SOURCE_OWNER_HOLD"
        assert r["reason"]==MISSING_B_CONTEXT
        assert r["event_ref"]==""
        assert _identity(s)==before
        assert s.verify()["ok"] is True
    finally: s.close()

def test_controlled_b_refusal_is_generated_performed_and_consumed(tmp_path):
    s=_start(tmp_path/"controlled")
    try:
        record_b_observation(s)
        r=s.produce_b_turn(controlled=True)
        print(r)
        assert r["status"]=="OK"
        assert r["attempt"]["actor_id"]=="TEST_ONLY_BP1_R26V_ACTOR_B"
        assert r["attempt"]["option_id"]=="EXPLICIT_REFUSAL"
        assert r["attempt"]["performed"] is True
        assert r["b_source_operation"]=="REFUSE_TOOL"
        assert r["event_ref"]
        assert s.verify()["ok"] is True
    finally: s.close()

def test_controlled_b_generation_is_role_parameterized(tmp_path):
    s=_start(tmp_path/"role")
    try:
        record_b_observation(s)
        r=s.produce_b_turn(controlled=True)
        gen=r["generation_ref"]
        assert r["attempt"]["actor_id"]!="TEST_ONLY_BP1_R26V_ACTOR_A"
        assert r["attempt"]["generation_hash"]==gen
        assert r["b_source_event_ref"]
    finally: s.close()

def test_controlled_source_cut_holds_then_restores(tmp_path):
    s=_start(tmp_path/"cut")
    try:
        assert controlled_b_sources(s)
        record_b_observation(s)
        r1=s.produce_b_turn(controlled=True)
        assert r1["status"]=="OK"
        # controlled cut represented by no sources
        r2=s.produce_b_turn(controlled=False)
        assert r2["status"]=="SOURCE_OWNER_HOLD"
        assert r2["event_ref"]==""
        record_b_observation(s)
        before=_identity(s)
        r3=s.produce_b_turn(controlled=True)
        assert r3["status"] in {"OK", "OPEN"}
        assert r3["attempt"]["performed"] is True
        assert _identity(s)!=before
    finally: s.close()

def test_controlled_positive_is_not_actual_grade(tmp_path):
    s=_start(tmp_path/"grade")
    try:
        record_b_observation(s)
        r=s.produce_b_turn(controlled=True)
        assert r["controlled"] is True
        assert r["native"] is False
        assert r["psychology_claim"] is False
        turns=s.b_turns()
        assert any(row["body"].get("source_grade")=="TEST_ONLY_S49_CONTROLLED_B_MODEL_PREMISE" for row in turns)
    finally: s.close()


def test_b_request_attempt_is_denied_by_actual_world_constraint(tmp_path):
    from s39.sources import make_source
    from s49.actor import generate_b, perform_b_attempt
    s=_start(tmp_path/"denied")
    try:
        bid=s.world().actor_state["B"]["actor_id"]
        records=[
            make_source(source_ref="TEST_ONLY_S49_B_URGENT",source_class="CURRENT_PROJECT",actor_id=bid,branch_id=s.branch_id,as_of=s.clock(),predicate="REPAIR_URGENT",value=1),
            make_source(source_ref="TEST_ONLY_S49_B_OTHER_SHARE",source_class="HISTORICAL_EPISODE",actor_id=bid,branch_id=s.branch_id,as_of=s.clock(),predicate="PRIOR_B_SHARE",value=1,content={"other_party":"A"}),
        ]
        record_b_observation(s)
        gen=generate_b(s,source_records=records)
        assert gen["generation"]["selected_option"]=="REQUEST_TOOL"
        w=s.world(); w.actor_state["B"]["free_hours"]=0; w.actor_state["B"]["tools_remaining"]=0
        s.product._checkpoint(s.branch_id, s.clock(), w)
        attempt=perform_b_attempt(s,gen)
        assert attempt["status"]=="DENIED"
        assert attempt["performed"] is False
        assert attempt["event_id"]==""
    finally: s.close()


def test_b_access_requires_actual_observation_not_presence(tmp_path):
    from s49.actor import _b_access
    s=_start(tmp_path/"no-access")
    try:
        world=s.world(); world.positions["B"]="market"; s.product._checkpoint(s.branch_id,s.clock(),world)
        ev=s.read_events()[-1]
        a=_b_access(s,ev)
        assert a["access_status"]=="NOT_WITNESSED"
        assert a["source_ref"]=="S49_NO_OBSERVED_B_ACCESS"
    finally: s.close()


def test_forged_generation_is_rejected_before_world_event(tmp_path):
    from copy import deepcopy
    from s49.actor import generate_b, perform_b_attempt
    s=_start(tmp_path/"forged")
    try:
        record_b_observation(s)
        gen=generate_b(s,source_records=controlled_b_sources(s))
        before=len(s.world().events)
        forged=deepcopy(gen); forged["actor_id"]="FORGED_ACTOR"; forged["branch_id"]="FORGED_BRANCH"; forged["event_ref"]="FORGED_EVENT"
        r=perform_b_attempt(s,forged)
        assert r["status"]=="DENIED"
        assert r["performed"] is False
        assert len(s.world().events)==before
    finally: s.close()


def test_controlled_positive_source_chain_is_bound_into_normal_consumer(tmp_path):
    s=_start(tmp_path/"chain")
    try:
        record_b_observation(s)
        r=s.produce_b_turn(controlled=True)
        assert r["status"]=="OK"
        ev=s.read_events()[-1]
        assert r["b_source_event_ref"]
        assert r["generation_ref"]
        assert r["attempt"]["generation_hash"]==r["generation_ref"]
        assert ev["e1_event_id"]==r["event_ref"]
        # source chain fields are in the B source event/result episode
        found=[]
        for row in s.product.store.episodes(s.branch_id):
            body=row.get("body") or {}
            if body.get("stage")=="NORMAL_CONSUMER":
                found.append(body)
        assert found and found[-1].get("b_source_operation")=="REFUSE_TOOL"
    finally: s.close()
