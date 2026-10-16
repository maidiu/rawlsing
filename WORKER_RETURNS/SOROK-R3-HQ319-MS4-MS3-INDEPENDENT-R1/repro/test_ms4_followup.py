"""Prospective follow-up: genuine two-owner replay; native event envelope.
Original 85 tests and all ten REDs are retained unchanged.
"""
from pathlib import Path
import sys
from dataclasses import replace
from copy import deepcopy
from unittest.mock import patch
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parent))
import test_ms4 as H
from candidate.candidate_registry_fixture import event_digest
observed=H.observed

@pytest.mark.parametrize('content',['AVAILABLE_SOURCE_BOUND','AVAILABLE_UNCERTAIN'])
@pytest.mark.parametrize('access,effect',[('CLAIM_ACCESSIBLE','REROUTE'),('CLAIM_INACCESSIBLE','BLOCK'),('CLAIM_ACCESS_UNKNOWN',None)])
@pytest.mark.parametrize('operation',['WITHDRAW','SUPERSEDE_EXACT_RECORD'])
def test_full_owner_and_registry_checkpoint_replay(content,access,effect,operation):
    a=H.seed(content,late=True);first=H.native(a);H.applied(first);H.applied(H.native(a,access,operation,first['effect']['effect_id']))
    if operation=='WITHDRAW':H.applied(H.native(a,access))
    before=H.snap(a);out=H.call(a)
    # A full checkpoint includes registry event admission and evaluations.
    rr=H.CandidateRegistryFixture();rr.restore(before['registry']);cc=H.N.FixtureOwnerState(rr);cc.restore(before['owner']);clone=dict(a,r=rr,c=cc)
    again=H.call(clone);H.remember(before=before,result=out,replay=again,after=H.snap(a),clone_after=H.snap(clone))
    assert out.get('effect_kind')==effect and not out['committed']
    assert (again['decision_state'],again.get('effect_kind'),again.get('receipt_hash'))==(out['decision_state'],out.get('effect_kind'),out.get('receipt_hash'))
    assert H.snap(clone)==H.snap(a)
    if effect is None:assert H.snap(a)==before

@pytest.mark.parametrize('access',['CLAIM_ACCESSIBLE','CLAIM_INACCESSIBLE'])
def test_second_distinct_event_fault_after_native_receipt_rolls_back_and_retries(access):
    a=H.seed();H.applied(H.native(a,access));first=H.call(a);assert first['decision_state']=='RESPONSE_EFFECTS_PRODUCED'
    e=replace(H.M.fixed_e2(),event_id='MS4_EV3_DISTINCT_LATER_REQUEST',effective_causal_time='1998-11-21T09:00:00Z',causal_parent_event_ids=(H.M.fixed_e2().event_id,),event_hash='')
    e=replace(e,event_hash=event_digest(e));before=H.snap(a);called=[];fn=H.C.build_response_receipt
    def fault(*args,**kwargs):
        out=fn(*args,**kwargs);called.append(out);raise RuntimeError('MS4_AFTER_DISTINCT_SECOND_REAL_RECEIPT')
    with patch.object(H.C,'build_response_receipt',fault):out=H.call(a,e2=e)
    H.remember(before=before,first=first,actual_receipts=called,result=out,after=H.snap(a));assert called and H.snap(a)==before
    assert out['decision_state']!='RESPONSE_EFFECTS_PRODUCED'
    retry=H.call(a,e2=e);H.remember(retry=retry)
    assert retry['decision_state']=='RESPONSE_EFFECTS_PRODUCED' and not retry['committed']
    assert retry['receipt']['precipitating_event']['event_id']==e.event_id

@pytest.mark.parametrize('features',[(),('alien_feature',)])
def test_native_e2_public_feature_scope_is_receivability_not_exact_content(features):
    a=H.seed();H.applied(H.call(a,'mediate'));e=replace(H.M.fixed_e2(),public_features=features,event_hash='');e=replace(e,event_hash=event_digest(e));before=H.snap(a);out=H.call(a,e2=e)
    H.remember(before=before,event=e,result=out,after=H.snap(a))
    if not features:
        assert out['decision_state']!='RESPONSE_EFFECTS_PRODUCED' and H.snap(a)==before
    else:
        assert out['decision_state']=='RESPONSE_EFFECTS_PRODUCED' and out['effect_kind']=='REROUTE' and not out['committed']
        assert out['receipt']['uptake_appraisal_projection']['basis']==list(features)

@pytest.mark.parametrize('access',['CLAIM_ACCESSIBLE','CLAIM_INACCESSIBLE','CLAIM_ACCESS_UNKNOWN'])
def test_full_restored_native_withdrawal_is_terminal_without_readdition(access):
    a=H.seed();first=H.native(a);H.applied(first);H.applied(H.native(a,access,'WITHDRAW',first['effect']['effect_id']));before=H.snap(a);out=H.call(a)
    H.remember(before=before,result=out,after=H.snap(a));assert not a['c'].stances and not out['committed']
    assert out.get('effect_kind')==('BLOCK' if access!='CLAIM_ACCESS_UNKNOWN' else None)
    assert out['decision_state']==('RESPONSE_EFFECTS_PRODUCED' if access!='CLAIM_ACCESS_UNKNOWN' else 'DEFER_MISSING_AUTHORITY')


def test_unknown_live_or_future_selected_transition_cannot_default_to_empty():
    a=H.seed();H.applied(H.call(a,'mediate'));c=a['c'];last=c.epistemic_transitions[-1]
    last['effect']['effective_causal_time']='1999-01-01T00:00:00Z';c._seal();H.rejected(a)
