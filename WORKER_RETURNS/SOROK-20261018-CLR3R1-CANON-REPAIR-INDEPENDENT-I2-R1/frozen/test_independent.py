"""Prospective I2 probes: expectations stay RED when the candidate violates them.

No candidate code or historical expectations are edited. Trust-boundary probes
are conditional, and do not imply that normal producer execution is wrong.
"""
import sys
from pathlib import Path
from copy import deepcopy
from dataclasses import asdict
from unittest.mock import patch
import pytest

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'reconstructed/clr3'))
import recursive_court as c

@pytest.fixture(scope='module')
def routine():
    return c.run_trajectory('ROUTINE', location='hall_drawer')

def frame(run):
    return deepcopy(run['source_preimages']['episode-theft'])

def test_same_actor_object_at_same_time_cannot_occupy_two_places(routine):
    """Public admit calls; no privileged ledger edit or checksum replacement."""
    first = frame(routine)
    second = deepcopy(first)
    second['id'] = 'distinct-source-same-episode-time'
    ledger = c.CanonLedger()
    original = ledger.admit(first, c.propose_realization(first, 'hall_drawer'))
    assert original['clock'] == 24
    other = c.propose_realization(second, 'garage_shelf')
    assert other['clock'] == original['clock']
    assert other['facts']['lock_id'] == original['facts']['lock_id']
    with pytest.raises(ValueError):
        ledger.admit(second, other)

def test_inconsistent_producer_frame_not_a_validated_computed_transition(routine):
    """Conditional stronger ingress contract: untrusted producer supplies frame.

    This does not alter an admitted preimage; it probes the initial admission
    boundary. A trusted producer is an explicit alternative proof assumption.
    """
    source = frame(routine)
    assert any(e['id']=='actual-shared-attention' for e in source['effect']['selected_events'])
    source['resolved']['father_present'] = False
    candidate = c.propose_realization(source)
    assert 'Father was still at work.' in candidate['text']
    with pytest.raises(ValueError):
        c.CanonLedger().admit(source, candidate)

def test_material_inputs_not_workplace_labels_control_child_numerics():
    original = c.r1_world.work_facts
    def opaque(outcome):
        value = original(outcome)
        value['kind'] = 'OPAQUE_LABEL_SAME_FOR_ALL'
        return value
    reference = {w:c.run_trajectory(w) for w in c.r1_world.WORK_OUTCOMES}
    with patch.object(c.r1_world, 'work_facts', opaque):
        relabelled = {w:c.run_trajectory(w) for w in c.r1_world.WORK_OUTCOMES}
    for w in reference:
        assert reference[w]['resolved']['father_response']==relabelled[w]['resolved']['father_response']
        assert reference[w]['final_state']==relabelled[w]['final_state']
    assert relabelled['ROUTINE']['final_state']!=relabelled['RAISE_WITH_OVERTIME']['final_state']

def test_canon_detail_drives_task_while_numerical_outcomes_may_converge():
    a=c.run_trajectory('ROUTINE',location='hall_drawer')
    b=c.run_trajectory('ROUTINE',location='garage_shelf')
    assert a['later']['target_location']!=b['later']['target_location']
    assert a['later']['canon_read']['field']=='facts.lock_location'
    assert a['immediate']==b['immediate'] and a['final_state']==b['final_state']
    assert a['delayed_feedback']['actual_activity_source']!=b['delayed_feedback']['actual_activity_source']
    assert a['delayed_feedback']['legacy_deltas']==b['delayed_feedback']['legacy_deltas']

def test_owned_source_copy_survives_caller_mutation(routine):
    source=frame(routine)
    ledger=c.CanonLedger()
    admitted=ledger.admit(source,c.propose_realization(source))
    original_hash=admitted['source_hash']
    source['proposal']['raw_packet']['event_candidates'].clear()
    source['effect']['before']['capacity']['money']=-999
    assert ledger.verify()
    assert c.digest(ledger._sources[admitted['source_ref']])==original_hash
    assert ledger.later_consume(admitted['id'])['target_location']=='hall_drawer'

def test_ordinary_evolution_precedes_incident_without_all_field_delta_requirement():
    state=c.initial_state()
    config,order=c.config_and_order()
    before=asdict(state)
    tick=c.advance(state,config,order,10,'independent_ordinary_probe')
    assert tick['before']==before and tick['after']['age']==7
    assert tick['after']['events_this_year']==[]
    assert any(x['path'].startswith('capacity.') for x in tick['numeric_changes'])
    assert any(tick['before'][k]==tick['after'][k] for k in before)
    assert tick['pressure_status']=='clean'
