"""Additional OUT2 combinations on fixed source-free boundary; original courts untouched."""
import copy,json,os,subprocess,sys
from pathlib import Path
import pytest
from outbox_prototype import make_prototype,Journal,durable_delivery_id,_hash
from test_rto_hostile import strict,legacy

@pytest.mark.parametrize('mode',['STRlCT','legacy',None,'',[],{'grant':True}])
def test_explicit_mode_with_fake_owner_grant_never_downgrades(mode):
    p=make_prototype();p.ledger.admission_decider=lambda _:True
    c=strict();c['envelope_mode']=mode
    assert p.ledger.admit(c) is None
    assert p.ledger.last_refusal=='UNKNOWN_ENVELOPE_MODE'
    assert p.ledger.count()==0

@pytest.mark.parametrize('nested',[
    {'metadata':{'admitted_event_id':'EVENT-FORGED'}},
    {'steps':[{'final_state':{'material':'moved'}}]},
    {'effects':{'world_owner':'ISSUER-FORGED'}},
    {'facts':[{'objective_job':'fired'}]},
])
def test_nested_directives_no_override_even_callback_true(nested):
    p=make_prototype();p.ledger.admission_decider=lambda _:True
    c=strict();c['payload']=nested
    assert p.ledger.admit(c) is None
    assert p.ledger.last_refusal=='UNLICENSED_AUTHORITY_DIRECTIVE'

@pytest.mark.parametrize('key',['producer_instance_ref','expected_v3_history_hash','payload_hash','render_context_hash'])
def test_opaque_lineage_collision_persists_over_snapshot(key):
    p=make_prototype();p.ledger.admission_decider=lambda _:True
    original=strict(**{key:'OPAQUE-A'});e=p.ledger.admit(original)
    assert e and p.ledger.count()==1
    snap=p.snapshot()
    p2=make_prototype();p2.ledger.admission_decider=lambda _:True;p2.restore(snap)
    changed=strict(**{key:'OPAQUE-B'})
    assert p2.ledger.admit(changed) is None
    assert p2.ledger.last_refusal=='CANDIDATE_IDENTITY_CONFLICT'
    assert p2.ledger.count()==1


def test_revocation_after_positive_fixture_delivery_and_ack_not_perception(tmp_path):
    p=make_prototype();p.ledger.admission_decider=lambda _:True
    eid=p.ledger.admit(strict())['occurrence_id']
    assert p.outbox.authorize_viewer(eid,'viewer')
    assert p.outbox.emit_to(eid,'viewer')
    assert p.outbox.deliver_to(eid,'viewer')
    assert p.projection.offer('viewer',eid)
    assert p.projection.has_opportunity('viewer',eid)
    assert p.outbox.revoke_viewer(eid,'viewer')
    assert not p.projection.has_opportunity('viewer',eid)
    assert p.outbox.ack_to(eid,'viewer') is None
    assert p.outbox.deliver_to(eid,'viewer') is None
    assert not p.projection.perceive('viewer',eid,perception_witness='FAKE')
    j=Journal(tmp_path/'j.json');j.commit(p)
    cold=j.recover()
    assert cold.ledger.count()==1
    assert not cold.projection.has_opportunity('viewer',eid)
    assert not cold.projection.has_perceived('viewer',eid)
    assert cold.outbox.ack_to(eid,'viewer') is None


def test_failed_restore_preserves_live_journal_and_all_live_fields():
    p=make_prototype();eid=p.ledger.admit(legacy('BEFORE'))['occurrence_id']
    p.world_state['synthetic']='old';p.outbox.emit(eid);p.projection.offer('A',eid)
    old=p.snapshot();bad=copy.deepcopy(old)
    bad['ledger'][0]['payload']['utterance']='ALTERED'
    bad['outbox'][eid]['attempts']=12
    with pytest.raises(ValueError):p.restore(bad)
    assert p.snapshot()==old


def test_snapshot_forged_non_ghost_same_user_perceived_rejected():
    p=make_prototype();eid=p.ledger.admit(legacy('S'))['occurrence_id']
    assert p.projection.offer('A',eid)
    forged=p.snapshot();forged['perceived']['A']=[eid]
    with pytest.raises(ValueError,match='NO_PERCEPTION_OWNER'):p.restore(forged)
    assert not p.projection.has_perceived('A',eid)


def test_snapshot_attempt_zero_witness_forgery_rejected(tmp_path):
    p=make_prototype();eid=p.ledger.admit(legacy('S'))['occurrence_id']
    p.outbox.authorize_viewer(eid,'A');p.outbox.emit_to(eid,'A')
    bad=p.snapshot();did=durable_delivery_id(eid,'A')
    bad['client_deliveries'][did]['attempts']=0
    with pytest.raises(ValueError,match='FORGED_LAST_ATTEMPT_ID'):p.restore(bad)
    assert p.outbox.client_deliveries[did]['attempts']==1


def test_old_journal_preimage_schema_refused_without_migration(tmp_path):
    j=Journal(tmp_path/'j.json');p=make_prototype();j.commit(p)
    d=json.loads(j.path.read_text());d['schema']='OUTBOX_F2_JOURNAL_V1'
    j.path.write_text(json.dumps(d))
    with pytest.raises(ValueError,match='UNSUPPORTED_JOURNAL_SCHEMA'):j.recover()


def test_hash_correct_but_material_world_state_refused_in_cold_recovery(tmp_path):
    j=Journal(tmp_path/'j.json');p=make_prototype();j.commit(p)
    d=json.loads(j.path.read_text());d['state']['world']['mug']='fake-moved'
    d['state_digest']=_hash(d['state']);j.path.write_text(json.dumps(d))
    with pytest.raises(ValueError,match='WORLD_STATE_REQUIRES_EXTERNAL_OWNER'):j.recover()


def test_input_and_event_are_not_mutable_aliases():
    p=make_prototype();p.ledger.admission_decider=lambda _:True
    c=strict();ev=p.ledger.admit(c);identity=ev['identity_digest']
    c['payload']['utterance']='MALICIOUS';ev['payload']['utterance']='MALICIOUS2'
    committed=p.ledger.get('OCC-0001')
    assert committed['payload']['utterance']=='Hello'
    assert committed['identity_digest']==identity
    assert p.ledger.admit(strict()) is not None


def test_strict_opportunity_requires_per_viewer_delivered_fixture():
    p=make_prototype();p.ledger.admission_decider=lambda _:True
    eid=p.ledger.admit(strict())['occurrence_id']
    assert p.outbox.authorize_viewer(eid,'A') and p.outbox.authorize_viewer(eid,'B')
    assert p.outbox.emit_to(eid,'A')
    assert not p.projection.offer('A',eid)
    assert p.outbox.deliver_to(eid,'A')
    assert p.projection.offer('A',eid)
    assert not p.projection.offer('B',eid)
    assert not p.projection.perceive('A',eid,perception_witness={'fake':True})


def _step(mode,path,expected):
    r=subprocess.run([sys.executable,str(Path(__file__).with_name('out2_cold_driver.py')),mode,str(path)],capture_output=True,text=True,timeout=20)
    assert r.returncode==expected,(mode,r.returncode,r.stderr,r.stdout)


def test_new_cold_exit79_before_rename(tmp_path):
    path=tmp_path/'cold.json'
    _step('crash_before',path,79)
    assert not path.exists()
    _step('verify_before',path,0)


def test_new_cold_exit79_after_commit_revocation_and_second_cold_process(tmp_path):
    path=tmp_path/'cold.json'
    _step('crash_after',path,79)
    _step('revoke_after',path,0)
    _step('verify_revocation',path,0)
