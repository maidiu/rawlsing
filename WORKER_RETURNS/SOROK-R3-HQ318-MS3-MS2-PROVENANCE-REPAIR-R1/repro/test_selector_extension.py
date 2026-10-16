"""Supplemental selector expectations, frozen before probing/fixing the sentinel gap."""
from pathlib import Path
from copy import deepcopy
import sys,json
import pytest
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'staging/ms2/staging/ms1/runtime'))
import ms1_serial as M
from candidate import owner_transitions as N,can008_candidate_rule as C
from candidate.candidate_registry_fixture import CandidateRegistryFixture
@pytest.mark.parametrize('entry',['mediate','consume'])
@pytest.mark.parametrize('selector',[None,'',17,[],{},'MS3_FOREIGN_SELECTOR'],ids=['None','empty','integer','list','dict','foreign'])
def test_explicit_invalid_selector_never_skips_binding_or_becomes_valid_empty(entry,selector):
    reg=CandidateRegistryFixture();C.register_default_rule(reg);b=C.build_default_binding();ctx=N.FixtureOwnerState(reg);e1=M.fixed_e1();C.occurrence_gate(e1,reg)
    proposal,memory=M.form_and_commit_memory(reg,ctx,e1,b,'AVAILABLE_SOURCE_BOUND');assert proposal is not None
    claim=N.canonical_claim(M.ACTOR,'FIXTURE_PRIVATE_FEEDBACK_APPRAISAL','RESPECTED',M.T_E1,M.ACTOR,[e1.event_id]);ref=ctx.bind_claim(claim,e1)
    assert M.mediate(ctx=ctx,reg=reg,binding=b,e1=e1,claim_id=ref,memory=memory)['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
    before=dict(owner=ctx.checkpoint(),registry=reg.checkpoint())
    out=M.mediate(ctx=ctx,reg=reg,binding=b,e1=e1,claim_id=selector,memory=memory) if entry=='mediate' else M.consume(ctx,reg,b,M.fixed_e2(),selector)
    after=dict(owner=ctx.checkpoint(),registry=reg.checkpoint());o=R/'evidence/selector_extension/observations';o.mkdir(parents=True,exist_ok=True)
    (o/(entry+'_'+type(selector).__name__+'_'+str(len(str(selector)))+'.json')).write_text(json.dumps(dict(selector=selector,entry=entry,before=before,response=out,after=after),indent=2)+'\n')
    assert out['decision_state'] not in ['APPLIED_EPISTEMIC_TRANSITION','RESPONSE_EFFECTS_PRODUCED','RESPONSE_INPUTS_VALID_EMPTY']
    assert before==after
