"""Specific readset regression controls for the R2 implementation."""
from dataclasses import replace
import pytest
from kernel import (eligible,propose,fixture_grant,append_test_only,Refusal,
                    MODES,digest,asdict)
from test_local_hostile import begin,twice,rewrite_history

@pytest.mark.parametrize('mode',[m for m in MODES if m!='NO_CHANGE'])
def test_each_relation_mode_binds_exact_three_sources(mode):
    scene,state=begin()
    c=next(c for c in eligible(scene,state,'later') if c.mode==mode)
    p=propose(scene,state,'later',c.id)
    kinds={x[0] for x in p['source_preimages']}
    assert {'RELATION_RELEVANCE','RELATION_OBSERVED_HISTORY','RELATION_HISTORY_WITNESS'}<=kinds
    done=append_test_only(scene,state,p,fixture_grant(p,'child'))
    assert done.lineage[-1].source_preimages==p['source_preimages']

def test_changed_observed_history_witness_fails_historical_continuation():
    scene,state=twice()
    bad=replace(scene,history_witnesses=tuple(replace(w,observer='peer')
        if w.actor=='child' and w.history_id=='later_observed_counterpart' else w for w in scene.history_witnesses))
    with pytest.raises(Refusal,match='SOURCE_PREIMAGE'):eligible(bad,state,'future')

def test_added_valid_relation_alternative_does_not_replace_consumed_one():
    scene,state=twice();baseline=eligible(scene,state,'future')
    alternative=replace(scene.relevance[0],observer='peer')
    for records in ((alternative,)+scene.relevance,scene.relevance+(alternative,)):
        assert eligible(replace(scene,relevance=records),state,'future')==baseline

def test_an_unconsumed_alternative_can_change_after_commit():
    scene,state=begin();alt=replace(scene.relevance[0],observer='peer')
    scene=replace(scene,relevance=scene.relevance+(alt,))
    c=next(c for c in eligible(scene,state,'later') if c.mode=='DIFFERENTIATE')
    p=propose(scene,state,'later',c.id)
    selected=next(x[2] for x in p['source_preimages'] if x[0]=='RELATION_RELEVANCE')
    done=append_test_only(scene,state,p,fixture_grant(p,'child'))
    future,_=twice()
    # Preserve the exact selected receipt and remove the unconsumed alternative.
    kept=tuple(x for x in scene.relevance if digest(asdict(x))==selected)
    assert eligible(replace(future,relevance=kept),done,'future')

def test_unrelated_private_history_remains_free_after_relation_commit():
    scene,state=twice()
    bad=rewrite_history(scene,'caregiver','care_work_history',activity='new private workshop history')
    assert eligible(bad,state,'future')==eligible(scene,state,'future')

def test_relation_changed_between_proposal_and_append_fails_even_with_fixture_grant():
    scene,state=begin();c=next(c for c in eligible(scene,state,'later') if c.mode=='DIFFERENTIATE')
    p=propose(scene,state,'later',c.id);g=fixture_grant(p,'child')
    bad=replace(scene,relevance=(replace(scene.relevance[0],observer='peer'),))
    with pytest.raises(Refusal,match='PROPOSAL_RECOMPUTATION_FAILED'):
        append_test_only(bad,state,p,g)

def test_no_change_does_not_pin_an_unused_relation():
    scene,state=begin();c=next(c for c in eligible(scene,state,'later') if c.mode=='NO_CHANGE')
    p=propose(scene,state,'later',c.id)
    assert not any(x[0].startswith('RELATION_') for x in p['source_preimages'])
    assert append_test_only(scene,state,p,fixture_grant(p,'child')) is state

def test_future_relation_receipt_cannot_enable_a_relation_mode():
    scene,state=begin();bad=replace(scene,relevance=(replace(scene.relevance[0],time=99),))
    assert {c.mode for c in eligible(bad,state,'later')}=={'NO_CHANGE'}

def test_unwitnessed_observation_cannot_enable_a_relation_mode():
    scene,state=begin();bad=rewrite_history(scene,'child','later_observed_counterpart',witnessed=False)
    assert {c.mode for c in eligible(bad,state,'later')}=={'NO_CHANGE'}
