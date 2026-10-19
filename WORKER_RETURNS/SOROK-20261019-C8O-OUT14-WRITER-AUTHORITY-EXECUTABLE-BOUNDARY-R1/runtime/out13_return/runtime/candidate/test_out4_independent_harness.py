"""HQ308 author-origin hostile controls, distinct from the unchanged OUT3 reviewer archive.
No original S01-S28 or RTO/OUT2 test is modified. These are source-free only.
"""
import copy,json,subprocess,sys
from pathlib import Path
import pytest
from outbox_prototype import Journal,make_prototype,DeliveryState,_hash,durable_delivery_id
from test_cold_repair import strict


def inst():
    p=make_prototype();p.ledger.admission_decider=lambda _:True;return p

def event(p):
    e=p.ledger.admit(strict()); assert e;return e['occurrence_id']

def test_legacy_minimal_fixture_remains_but_is_not_owner():
    p=make_prototype();e=p.ledger.admit({'candidate_id':'L','payload':{'text':'hi'}})
    assert e and e['admission_grade']=='SOURCEFREE_LEGACY_FIXTURE_NO_OWNER_AUTHORITY'


def test_missing_mode_owner_shape_does_not_downgrade():
    p=inst();c=strict();c.pop('envelope_mode')
    assert p.ledger.admit(c) is None
    assert p.ledger.last_refusal=='MISSING_STRICT_ENVELOPE_MODE'
    assert p.ledger.count()==0

@pytest.mark.parametrize('payload',[
    {'x':{'WORLD_OWNER':'fake'}}, {'x':{'worldOwner':'fake'}},
    {'x':[{'MEMORY_DELTA':{'memory':'fake'}}]}, {'x':{'Client_Perceived':True}},
])
def test_owner_directive_variants_rejected(payload):
    p=inst();assert p.ledger.admit(strict(payload=payload)) is None
    assert p.ledger.last_refusal=='UNLICENSED_AUTHORITY_DIRECTIVE'

@pytest.mark.parametrize('refs',[[' '],['SRC-1','\t']])
def test_whitespace_source_reference_rejected(refs):
    p=inst();assert p.ledger.admit(strict(source_refs=refs)) is None
    assert p.ledger.last_refusal=='MISSING_SOURCE_AUTHORITY'

@pytest.mark.parametrize('refs',[[''],['\t','ACTOR']])
def test_empty_participants_rejected(refs):
    p=inst();assert p.ledger.admit(strict(participant_refs=refs)) is None
    assert p.ledger.last_refusal=='INVALID_PARTICIPANT_REFS'

def test_parent_none_is_typed_refusal():
    p=inst();assert p.ledger.admit(strict(parent_refs=None)) is None
    assert p.ledger.last_refusal=='INVALID_PARENT_REFS'


def test_direct_mutation_cannot_forge_human_perception():
    p=inst();eid=event(p);p.projection.perceived['A']=[eid]
    assert not p.projection.has_perceived('A',eid)
    with pytest.raises(ValueError,match='NO_PERCEPTION_OWNER'):
        p.validate_state()


def test_strict_aggregate_delivery_requires_authorized_client_witness():
    p=inst();eid=event(p);assert p.outbox.authorize_viewer(eid,'A')
    assert p.outbox.emit(eid,viewer_id='A')==DeliveryState.ADMITTED_UNDELIVERED
    assert p.outbox.deliver(eid)==DeliveryState.NOT_SENT
    assert p.outbox.ack(eid)==DeliveryState.NOT_SENT
    assert p.outbox.emit_to(eid,'A')
    assert p.outbox.deliver(eid)==DeliveryState.NOT_SENT
    assert p.outbox.deliver_to(eid,'A')['state']==DeliveryState.DELIVERED_UNACKED.value
    assert p.outbox.deliver(eid)==DeliveryState.NOT_SENT
    assert p.projection.offer('A',eid)
    assert p.outbox.deliver(eid)==DeliveryState.DELIVERED_UNACKED
    assert p.outbox.ack(eid)==DeliveryState.NOT_SENT
    assert p.outbox.ack_to(eid,'A')['state']==DeliveryState.ACKNOWLEDGED.value
    assert p.outbox.ack(eid)==DeliveryState.ACKNOWLEDGED


def test_aggregate_receipts_stop_after_sole_viewer_revoked():
    p=inst();eid=event(p);assert p.outbox.authorize_viewer(eid,'A')
    p.outbox.emit_to(eid,'A');p.outbox.deliver_to(eid,'A')
    p.outbox.revoke_viewer(eid,'A')
    assert p.outbox.deliver(eid)==DeliveryState.NOT_SENT
    assert p.outbox.ack(eid)==DeliveryState.NOT_SENT


@pytest.mark.parametrize('update',[{'attempts':-1},{'ack_count':3},{'state':'ACKNOWLEDGED','ack_count':0},
                                   {'state':'NOT_SENT','attempts':1}, {'state':'DELIVERED_UNACKED','ack_count':1}])
def test_bad_global_counts_cannot_restore(update):
    p=inst();eid=event(p);p.outbox.authorize_viewer(eid,'A');p.outbox.emit(eid,viewer_id='A')
    saved=p.snapshot();wrong=copy.deepcopy(saved);wrong['outbox'][eid].update(update)
    with pytest.raises(ValueError):p.restore(wrong)
    assert p.snapshot()==saved

@pytest.mark.parametrize('update',[{'ack_count':1,'state':'DELIVERED_UNACKED'},
                                   {'attempts':-1}, {'state':'NOT_SENT','attempts':1}])
def test_bad_client_counts_cannot_restore(update):
    p=inst();eid=event(p);p.outbox.authorize_viewer(eid,'A');p.outbox.emit_to(eid,'A')
    did=durable_delivery_id(eid,'A');saved=p.snapshot();wrong=copy.deepcopy(saved)
    wrong['client_deliveries'][did].update(update)
    with pytest.raises(ValueError):p.restore(wrong)
    assert p.snapshot()==saved


def test_empty_viewer_authorization_denied():
    p=inst();eid=event(p)
    assert not p.outbox.authorize_viewer(eid,'')
    assert not p.outbox.authorize_viewer(eid,' ')
    assert not p.outbox.emit_to(eid,'')


def test_regrant_revoked_viewer_denied_even_after_cold_recovery(tmp_path):
    p=inst();eid=event(p);p.outbox.authorize_viewer(eid,'A');p.outbox.emit_to(eid,'A')
    p.outbox.deliver_to(eid,'A');assert p.projection.offer('A',eid)
    assert p.outbox.revoke_viewer(eid,'A')
    assert not p.outbox.authorize_viewer(eid,'A')
    j=Journal(tmp_path/'j.json');j.commit(p)
    cold=j.recover()
    assert not cold.outbox.authorize_viewer(eid,'A')
    assert not cold.projection.has_opportunity('A',eid)
    assert cold.outbox.deliver_to(eid,'A') is None


def test_direct_corrupt_rehashed_snapshot_cannot_claim_negative_global_attempts(tmp_path):
    p=inst();eid=event(p);p.outbox.authorize_viewer(eid,'A');p.outbox.emit_to(eid,'A')
    j=Journal(tmp_path/'state.json');j.commit(p)
    d=json.loads(j.path.read_text());d['state']['outbox'][eid]['attempts']=-100
    d['state_digest']=_hash(d['state']);j.path.write_text(json.dumps(d))
    with pytest.raises(ValueError,match='BAD_AGGREGATE_DELIVERY_COUNTS'):j.recover()


def test_rehashed_ghost_client_ack_refused(tmp_path):
    p=inst();eid=event(p);p.outbox.authorize_viewer(eid,'A');p.outbox.emit_to(eid,'A')
    j=Journal(tmp_path/'state.json');j.commit(p)
    d=json.loads(j.path.read_text());did=durable_delivery_id(eid,'A')
    d['state']['client_deliveries'][did]['state']='ACKNOWLEDGED'
    d['state_digest']=_hash(d['state']);j.path.write_text(json.dumps(d))
    with pytest.raises(ValueError):j.recover()


def test_cold_process_crash_boundaries_preserved(tmp_path):
    driver=Path(__file__).with_name('cold_repair.py');db=tmp_path/'state.json'
    for mode in ('crash_before','verify_before','crash_after','verify_after'):
        r=subprocess.run([sys.executable,str(driver),mode,str(db)],text=True,capture_output=True,timeout=12)
        assert r.returncode==(79 if mode.startswith('crash_') else 0), (mode,r.stderr,r.stdout)


def test_failed_restore_does_not_modify_revocation_or_ledgers():
    p=inst();eid=event(p);p.outbox.authorize_viewer(eid,'A');p.outbox.revoke_viewer(eid,'A')
    pre=p.snapshot();bad=copy.deepcopy(pre);bad['revoked_viewers'][eid]=['A','A']
    with pytest.raises(ValueError):p.restore(bad)
    assert p.snapshot()==pre


def test_journal_v1_not_migrated_into_v2(tmp_path):
    j=Journal(tmp_path/'j.json');j.commit(make_prototype())
    d=json.loads(j.path.read_text());d['schema']='OUTBOX_F2_JOURNAL_V1';j.path.write_text(json.dumps(d))
    with pytest.raises(ValueError,match='UNSUPPORTED_JOURNAL_SCHEMA'):j.recover()
