"""Read-only portable checks of the X3 evidence, without rerunning courts."""
from pathlib import Path
import json,hashlib,sqlite3,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
def load(p):return json.loads((ROOT/p).read_text())
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def totals(p):
    tree=ET.parse(ROOT/p)
    return [sum(int(x.get(k,0)) for x in tree.iter('testsuite')) for k in ('tests','failures','errors','skipped')]
assert totals('evidence/independent_final.xml')==[28,8,0,0]
assert totals('evidence/reproduction/b3_final.xml')==[71,0,0,0]
assert totals('evidence/reproduction/f2/junit.xml')==[42,0,0,0]
assert totals('evidence/reproduction/inherited/m3_source_preimage_3_red.xml')==[3,3,0,0]
f2=load('evidence/f2_blinded/matrix.json')
assert len(f2['rows'])==42 and all(r['result']=='PASS' for r in f2['rows'])
assert sum(r['status']=='ELIGIBLE_NONCAUSAL' for r in f2['rows'])==20
assert all(r['engine_case_id']!=r['case_id'] for r in f2['rows'])
assert all(not any('reference_oracle.py' in k for k in r['calls']) for r in f2['rows'])
native=load('evidence/reproduction/inherited/b2/f1_native_gate.log')
assert native['status']=='RED' and len(native['failures'])==17
for label in ('positive','permission_absent'):
    live=load('evidence/reproduction/loop/'+label+'.json')
    cold=load('evidence/reproduction/'+label+'_cold.log')
    assert cold['receipts']==[ep['receipt'] for ep in live['episodes']]
    for suffix in ('','_cold'):
        db=sqlite3.connect('file:'+str(ROOT/'evidence/reproduction/loop'/(label+suffix+'.sqlite'))+'?mode=ro',uri=True)
        assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        snapshot={name:db.execute('SELECT * FROM '+name+' ORDER BY 1').fetchall() for name, in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")}
        db.close();assert digest(snapshot)==live['snapshot_hash']==cold['snapshot_hash']
    assert len(live['final_middle'])==(1 if label=='positive' else 0)
    assert live['episodes'][0]['receipt']['M2_temporal_traces'][0]['actual_speech_ids']==[]
    assert live['episodes'][-1]['actor_actions'][-1]['action']=='DECLINE_CONTACT'
for label,n in (('missing_origin',1),('atomic_future_event',5),('cold_partial_missing_origin',1),('cold_partial_future_event',5)):
    r=load('evidence/sql/'+label+'.json')
    assert r['result']['code']=='REFUSAL_MUTATED_DATABASE'
    assert len(r['before']['occurrence'])==0 and len(r['after']['occurrence'])==n
manifest=load('artifact_manifest.json')
for r in manifest['files']:
    p=ROOT/r['path'];assert p.stat().st_size==r['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],r['path']
print('Verified portable evidence, exact live/cold SQLite, preserved REDs, and',len(manifest['files']),'artifact hashes.')
