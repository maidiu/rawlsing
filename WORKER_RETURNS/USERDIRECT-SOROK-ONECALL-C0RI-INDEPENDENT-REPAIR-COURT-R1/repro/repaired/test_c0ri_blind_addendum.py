"""C0RI blind ADDENDUM, made while C0R branch was still at its commission seal.
Original H01/H02 remain byte frozen and are recognized as non-discriminating.
These tests inspect TARGET occurrence identities, never incidental deferrals.
"""
from copy import deepcopy
import pytest
import onecall_c0 as c


def test_S01_late_source_substitution_refuses_actual_event_append(monkeypatch):
    original=c.apply_admitted
    def attack(state,p,year,rules):
        state['world']['source_ref']='FORGED_AFTER_PACKET_VALIDATION'
        return original(state,p,year,rules)
    monkeypatch.setattr(c,'apply_admitted',attack)
    try:
        outcome=c.run()
    except (ValueError,PermissionError,RuntimeError,AssertionError):
        return
    records=outcome['causal']['final_state']['events']
    assert records==[], 'A swapped live source still produced committed mock events'


def test_S02_existing_event_id_cannot_be_reused_on_restart():
    state=c.initial_state()
    state['events'].append({'id':c.fact_id(2020,'practice'),'year':2020,
                            'day':30,'action':'PRIOR_COMMITTED_DISTINCT_PAYLOAD'})
    try:
        result=c.run(initial=state)
    except (ValueError,PermissionError,RuntimeError,AssertionError):
        return
    ids=[x['id'] for x in result['causal']['final_state']['events']]
    assert len(ids)==len(set(ids)), 'Duplicate committed event ID on cold restart'


def test_S03_missing_child_parent_is_never_admitted_by_fallback(monkeypatch):
    old=c.fixed_candidates
    def f(year):
        if year!=2020:return []
        return [c.candidate(2020,20,'parent','PRACTICE_OBSERVED'),
                c.candidate(2020,80,'child','PROJECT_TASK',min_practice=1,
                            prerequisites=[c.fact_id(2020,'parent')])]
    monkeypatch.setattr(c,'fixed_candidates',f)
    x=c.run(rules={'licensed_objective_actions':['PROJECT_TASK']})
    ids={e['id'] for e in x['causal']['final_state']['events']}
    assert c.fact_id(2020,'parent') not in ids
    assert c.fact_id(2020,'child') not in ids


def test_S04_validated_same_year_parent_must_revalidate_child_after_commit(monkeypatch):
    def f(year):
        if year!=2020:return []
        return [c.candidate(2020,20,'parent','PRACTICE_OBSERVED'),
                c.candidate(2020,80,'child','PROJECT_TASK',min_practice=1,
                            prerequisites=[c.fact_id(2020,'parent')])]
    monkeypatch.setattr(c,'fixed_candidates',f)
    x=c.run()
    ids={e['id'] for e in x['causal']['final_state']['events']}
    assert c.fact_id(2020,'parent') in ids
    assert c.fact_id(2020,'child') in ids
