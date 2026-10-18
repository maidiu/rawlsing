"""Repair controls: preserve unrelated facts, genuine replay and actual lock ordering."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import json, os, select, subprocess, sys
import pytest
sys.path.insert(0,os.environ['B2_REVIEW_ROOT'])
import bridge as m

def tables(b):
    return {name:b.store.db.execute('SELECT * FROM '+name+' ORDER BY 1').fetchall() for name in ('checkpoint','occurrence','b2_ingress','b2_event_identity','joint_receipt')}

def save(name,**value):Path(os.environ['REPAIR_EVIDENCE'],name+'.json').write_text(json.dumps(value,indent=2)+'\n')

def setup(tmp_path,grant):
    b=m.Bridge(tmp_path/'state.sqlite',m.b1.initialize(m.b1.prehistory()))
    packet,context,policy=m.input_pair(b.store.state())
    witness=m.occurrence_witness(b.store.state(),packet,context)
    cap,registry=m.capability_fixture()
    b.witnesses={witness['hash']:witness};b.capability_witnesses=registry
    args=(packet,context,policy,witness,cap)
    receipt=b.advance(*args,grant=grant)
    return b,args,registry,receipt

@pytest.mark.parametrize('grant',[False,True])
def test_unrelated_legacy_identity_does_not_block_exact_replay(tmp_path,grant):
    b,args,registry,first=setup(tmp_path,grant)
    unrelated=replace(m.b1.episode(),event_id='UNRELATED_LEGACY_EVENT')
    b.store.admit_fixture(unrelated);before=tables(b)
    replay=b.advance(*args,grant=grant)
    assert replay['admitted_event']==first['admitted_event']
    assert tables(b)==before and len(before['occurrence'])==2
    save('unrelated_'+str(grant),first=first,replay=replay,before=before,after=tables(b));b.close()

@pytest.mark.parametrize('grant',[False,True])
def test_exact_duplicate_b1_insert_is_still_idempotent(tmp_path,grant):
    b,args,registry,first=setup(tmp_path,grant)
    event=deepcopy(first['admitted_event']);event.pop('hash')
    before=tables(b)
    b.store.admit_fixture(m.b1.Event(**event))
    replay=b.advance(*args,grant=grant)
    assert replay['admitted_event']==first['admitted_event']
    assert tables(b)==before and len(before['occurrence'])==1
    save('same_content_'+str(grant),replay=replay,before=before,after=tables(b));b.close()

def test_competing_legacy_writer_is_observed_after_sqlite_lock(tmp_path):
    b,args,registry,first=setup(tmp_path,False)
    packet,context,policy,witness,cap=args
    v=dict(packet=packet,context=context,policy=policy,witness=witness,cap=cap,registry=registry,observe_lock=True,kwargs={'grant':False})
    path=tmp_path/'input.json';path.write_text(json.dumps(v))
    worker=Path(os.environ['B2_REVIEW_ROOT']).parent/'tests_after/E2/process_e2.py'
    p=subprocess.Popen([sys.executable,str(worker),str(path),str(tmp_path/'state.sqlite')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    assert select.select([p.stdout],[],[],10)[0]
    assert json.loads(p.stdout.readline())['ready']
    b.store.db.execute('BEGIN IMMEDIATE')
    b.store.admit_fixture(m.b1.episode(label='CONCURRENT_LEGACY_CONFLICT'))
    before=tables(b)
    p.stdin.write('GO\n');p.stdin.flush()
    assert select.select([p.stdout],[],[],10)[0]
    assert p.stdout.readline().strip()=='BEGIN_REQUESTED'
    assert not select.select([p.stdout],[],[],0.2)[0]
    b.store.db.execute('COMMIT')
    stdout,stderr=p.communicate(timeout=15);assert p.returncode==0,stderr
    result=json.loads(stdout)
    assert result['receipt']['reason']=='EVENT_IDENTITY_LEDGER_INTEGRITY_FAILURE'
    assert result['receipt']['event_admission']=='NOT_PERFORMED' and not result['receipt']['b1_invoked']
    assert tables(b)==before
    save('competing_legacy_writer',pid=p.pid,before=before,result=result,after=tables(b));b.close()
