"""Focused S49 independent B producer tests."""
from __future__ import annotations
import pytest
from s49.bootstrap import install
install()
from s45.fixtures import root_bundle
from s37.harness import case_for, source_for
from s49.session import S49Session
from s49.errors import S49Refusal
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


def test_stripped_s49_source_fails_at_base_normal_guard(tmp_path):
    from s49.actor import generate_b, perform_b_attempt
    from s49.session import _source_from_b_event
    s=_start(tmp_path/"strip")
    try:
        record_b_observation(s)
        gen=generate_b(s,source_records=controlled_b_sources(s))
        s._append("S49_B_ACTOR_TURN",{"schema":"SOROK_S49_INDEPENDENT_ACTOR_PRODUCER@1","stage":"GENERATION","controlled":True,"generation":gen,"source_grade":"TEST_ONLY_S49_CONTROLLED_B_MODEL_PREMISE","missing_context":""})
        attempt=perform_b_attempt(s,gen)
        case,source,event=_source_from_b_event(s,generation_body=gen,attempt=attempt)
        stripped={k:v for k,v in source.items() if not str(k).startswith("s49_")}
        with pytest.raises(S49Refusal) as exc:
            s.admit_event(case=case,source=stripped,history_event_refs=(s.read_events()[-1]["e1_event_id"],),event_time=s.clock()+1)
        assert exc.value.code=="S49_NORMAL_CONSUMER_CHAIN_MISSING"
    finally: s.close()


def test_base_guard_rejects_forged_chain_even_with_instance_override(tmp_path):
    from s49.actor import generate_b, perform_b_attempt
    from s49.session import _source_from_b_event
    from copy import deepcopy
    s=_start(tmp_path/"baseguard")
    try:
        record_b_observation(s)
        gen=generate_b(s,source_records=controlled_b_sources(s))
        s._append("S49_B_ACTOR_TURN",{"schema":"SOROK_S49_INDEPENDENT_ACTOR_PRODUCER@1","stage":"GENERATION","controlled":True,"generation":gen,"source_grade":"TEST_ONLY_S49_CONTROLLED_B_MODEL_PREMISE","missing_context":""})
        attempt=perform_b_attempt(s,gen)
        case,source,event=_source_from_b_event(s,generation_body=gen,attempt=attempt)
        forged=deepcopy(source); forged["s49_source_chain_hash"]="FORGED_CHAIN"
        s._validate_admit_source_chain=lambda *a,**k: None
        with pytest.raises(S49Refusal):
            s.admit_event(case=case,source=forged,history_event_refs=(s.read_events()[-1]["e1_event_id"],),event_time=s.clock()+1)
    finally: s.close()


def _canonical_consumer_source(session):
    from s49.actor import generate_b, perform_b_attempt
    from s49.session import _source_from_b_event
    record_b_observation(session)
    gen=generate_b(session,source_records=controlled_b_sources(session))
    session._append("S49_B_ACTOR_TURN",{"schema":"SOROK_S49_INDEPENDENT_ACTOR_PRODUCER@1","stage":"GENERATION","controlled":True,"generation":gen,"source_grade":"TEST_ONLY_S49_CONTROLLED_B_MODEL_PREMISE","missing_context":""})
    attempt=perform_b_attempt(session,gen)
    return _source_from_b_event(session,generation_body=gen,attempt=attempt)


def test_normal_consumer_requires_canonical_performer_then_restores(tmp_path):
    from unittest.mock import patch
    s=_start(tmp_path/"performer-cut")
    try:
        case,source,event=_canonical_consumer_source(s)
        real_episodes=s.product.store.episodes
        def no_performer(branch):
            return [row for row in real_episodes(branch) if not (
                row.get("kind")=="S49_B_ACTOR_RESULT"
                and (row.get("body") or {}).get("stage")=="B_PERFORMER"
            )]
        with patch.object(s.product.store,"episodes",side_effect=no_performer):
            with pytest.raises(S49Refusal) as exc:
                s.admit_event(case=case,source=source,history_event_refs=(s.read_events()[-1]["e1_event_id"],),event_time=s.clock()+1)
            assert exc.value.code=="S49_NORMAL_CONSUMER_PERFORMER_MISSING"
        admitted=s.admit_event(case=case,source=source,history_event_refs=(s.read_events()[-1]["e1_event_id"],),event_time=s.clock()+1)
        assert admitted["status"]=="OK"
    finally: s.close()


def test_normal_consumer_rejects_rehashed_attempt_substitution(tmp_path):
    from copy import deepcopy
    from s49.session import _source_from_b_event
    s=_start(tmp_path/"attempt-sub")
    try:
        case,source,event=_canonical_consumer_source(s)
        forged=deepcopy(source)
        forged["s49_attempt_hash"]="FORGED_ATTEMPT"
        with pytest.raises(S49Refusal) as exc:
            s.admit_event(case=case,source=forged,history_event_refs=(s.read_events()[-1]["e1_event_id"],),event_time=s.clock()+1)
        assert exc.value.code=="S49_NORMAL_CONSUMER_ATTEMPT_SUBSTITUTED"
        assert len(s.read_events())==1
    finally: s.close()
