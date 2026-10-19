"""Extra repair controls for refusal atomicity and compatible elaboration."""
from copy import deepcopy
import pytest
import recursive_court as c

@pytest.fixture(scope='module')
def frames():
    return {w:deepcopy(c.run_trajectory(w)['source_preimages']['episode-theft'])
            for w in ('ROUTINE','RAISE_WITH_OVERTIME')}

def fresh(frames,workplace='ROUTINE',source_id='second-source'):
    frame=deepcopy(frames[workplace]);frame['id']=source_id
    return frame

@pytest.mark.parametrize('first,second',[('hall_drawer','garage_shelf'),('garage_shelf','hall_drawer')])
def test_location_conflict_refuses_in_both_orders_without_partial_write(frames,first,second):
    ledger=c.CanonLedger();a=fresh(frames,source_id='first-source')
    admitted=ledger.admit(a,c.propose_realization(a,first))
    before=(ledger.entries,deepcopy(ledger._sources))
    b=fresh(frames)
    with pytest.raises(ValueError,match='CANON_OBJECT_LOCATION_CONFLICT'):
        ledger.admit(b,c.propose_realization(b,second))
    assert (ledger.entries,ledger._sources)==before
    assert ledger.verify() and ledger.later_consume(admitted['id'])['target_location']==first
    # A refusal must not poison the source ID for a corrected, compatible retry.
    corrected=ledger.admit(b,c.propose_realization(b,first))
    assert corrected['source_ref']==b['id'] and len(ledger.entries)==2

def test_same_time_compatible_particulars_and_alternative_wording_remain_allowed(frames):
    ledger=c.CanonLedger();a=fresh(frames,source_id='first-source');b=fresh(frames)
    first=ledger.admit(a,c.propose_realization(a,'hall_drawer','plain'))
    second=ledger.admit(b,c.propose_realization(b,'hall_drawer','alternate'))
    assert first['text']!=second['text'] and first['facts']==second['facts']
    assert ledger.entries[0]==first and ledger.verify()

def test_distinct_counterfactual_worlds_can_admit_different_particulars(frames):
    a=fresh(frames);b=fresh(frames)
    left=c.CanonLedger().admit(a,c.propose_realization(a,'hall_drawer'))
    right=c.CanonLedger().admit(b,c.propose_realization(b,'garage_shelf'))
    assert left['clock']==right['clock'] and left['facts']['lock_location']!=right['facts']['lock_location']

def test_later_observation_does_not_rewrite_earlier_location(frames):
    ledger=c.CanonLedger();a=fresh(frames,source_id='first-source');b=fresh(frames)
    first=ledger.admit(a,c.propose_realization(a,'hall_drawer'))
    later=c.propose_realization(b,'garage_shelf');later['clock']=26
    ledger.admit(b,later)
    assert ledger.entries[0]==first and ledger.verify()
    assert ledger.later_consume(first['id'])['target_location']=='hall_drawer'

@pytest.mark.parametrize('workplace', ['ROUTINE','RAISE_WITH_OVERTIME'])
def test_presence_conflict_refuses_in_both_directions_with_atomic_retry(frames,workplace):
    source=fresh(frames,workplace);ledger=c.CanonLedger()
    source['resolved']['father_present']=not source['resolved']['father_present']
    with pytest.raises(ValueError,match='SOURCE_ENCOUNTER_MISMATCH'):
        ledger.admit(source,c.propose_realization(source))
    assert ledger.entries==[] and ledger._sources=={}
    source['resolved']['father_present']=not source['resolved']['father_present']
    ledger.admit(source,c.propose_realization(source))
    assert ledger.verify() and len(ledger.entries)==1

def test_matching_flags_do_not_hide_contradictory_material_time(frames):
    source=fresh(frames);source['resolved']['father_response']['available_minutes']=3
    with pytest.raises(ValueError,match='SOURCE_ENCOUNTER_MISMATCH'):
        c.CanonLedger().admit(source,c.propose_realization(source))

@pytest.mark.parametrize('change', ['wrong_kind','missing_care','duplicate'])
def test_selected_attention_event_must_retain_its_recorded_contract(frames,change):
    source=fresh(frames)
    attention=next(e for e in source['effect']['selected_events'] if e['id']=='actual-shared-attention')
    if change=='wrong_kind':attention['kind']='practice'
    elif change=='missing_care':attention['magnets']['offers']=[]
    else:source['effect']['selected_events'].append(deepcopy(attention))
    with pytest.raises(ValueError,match='SOURCE_ENCOUNTER_MISMATCH'):
        c.CanonLedger().admit(source,c.propose_realization(source))
