"""Check persisted experimental receipt bytes and summarize actual counterfactuals."""
import bootstrap
from bootstrap import R
from cell import digest,source_hash,definition
from pathlib import Path
import json,hashlib,subprocess,itertools
O=R/'evidence/new/observations'
rows=[];cases={}
for p in sorted(O.glob('factorial_*.json')):
 d=json.loads(p.read_text());pre=d['pre'];post=d['post'];out=d['result'];read=out['read']
 assert digest(pre['owner_state'])==pre['owner_hash']==read['state_hash']==digest(read['actual_state'])==post['owner_hash']
 assert pre['owner_state']==post['owner_state']==read['actual_state']
 assert pre['rule_hash']==post['rule_hash']==source_hash()
 for journal in [post['history'],post['journal']]:
  last=None
  for i,e in enumerate(journal):
   assert e['seq']==i and e['prev_entry_hash']==last and e['entry_hash']==digest({k:v for k,v in e.items() if k!='entry_hash'})
   last=e['entry_hash']
 assert out['receipt']==post['journal'][-1]
 assert post['journal'][-1]['payload']['read']==read
 name=p.stem[len('factorial_'):];cases[name]=d
 rows.append(dict(case=name,event1_hash=post['events']['M01_FEEDBACK']['event_hash'],event2_hash=post['events']['M01_LATER_SHIFT_REQUEST']['event_hash'],owner_hash=pre['owner_hash'],history_hash=digest(pre['history']),streams=out['streams'],response_entry_hash=out['receipt']['entry_hash'],file=str(p.relative_to(R))))
assert len(rows)==36
assert len({r['event1_hash'] for r in rows})==len({r['event2_hash'] for r in rows})==1
fixed_owner=[]
for m,e in itertools.product(['NONE','CERTAIN','UNCERTAIN','UNAVAILABLE'],['NONE','BELIEF','INACCESSIBLE']):
 keys=[m+'_'+e+'_'+h for h in ['STORED','OMITTED','WITHHELD']];group=[cases[k] for k in keys]
 assert all(x['pre']['owner_state']==group[0]['pre']['owner_state'] and x['result']['streams']==group[0]['result']['streams'] for x in group)
 fixed_owner.append(dict(cases=keys,owner_state_identical=True,response_identical=True,owner_hash=group[0]['pre']['owner_hash']))
# Strict isolated single mediator contrasts (entire other mediator fixed).
a=cases['CERTAIN_NONE_STORED'];b=cases['UNCERTAIN_NONE_STORED'];c=cases['NONE_NONE_STORED'];e=cases['NONE_BELIEF_STORED']
assert a['pre']['history']==b['pre']['history']==c['pre']['history']==e['pre']['history']
assert a['pre']['owner_state']['stances']==b['pre']['owner_state']['stances']==c['pre']['owner_state']['stances']=={}
assert a['pre']['owner_state']['permissions']==b['pre']['owner_state']['permissions']==c['pre']['owner_state']['permissions']=={}
assert set(a['pre']['owner_state']['memories'])==set(b['pre']['owner_state']['memories'])
assert c['pre']['owner_state']['memories']==e['pre']['owner_state']['memories']=={}
summary=dict(preregistered_at_commit='845edf5d7c9c48b192b631dacf295afa6f587137',matrix=rows,fixed_entire_owner_state_history_controls=fixed_owner,strict_memory_contrast=dict(cases=['NONE_NONE_STORED','CERTAIN_NONE_STORED','UNCERTAIN_NONE_STORED'],history_identical=True,epistemic_stances_and_permissions_identical_empty=True,certain_uncertain_same_memory_id=True),strict_epistemic_contrast=dict(cases=['NONE_NONE_STORED','NONE_BELIEF_STORED'],memory_identical_empty=True,history_identical=True,canonical_claim_and_emission_identical=c['pre']['owner_state']['claims']==e['pre']['owner_state']['claims'] and c['pre']['owner_state']['emissions']==e['pre']['owner_state']['emissions']),serial='MECHANISM_IDENTIFICATION_HOLD',operative_owner='MECHANISM_IDENTIFICATION_HOLD',grade='SOURCEFREE_NEW_MEMORY_MEDIATION_CANDIDATE_REQUIRES_I2',portable_receipt_hashes_verified=True)
(R/'10_COUNTERFACTUAL_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
laws=[]
for name,h in [('CAN008_R2','b80dd6925066510ecbbfec7b427bf9f688475663'),('CAN008_R2_ADOPTION','a6bc1555489271e1adb2271ed02d46bb7f888170'),('ADP016','c6619a286e115d060ab4830889e7fc23762167a5'),('ADP017','eece4f3f2f3f9288ab9bbc645dc81e20a99e1280'),('production_guard','e0528d65215cb431196570c38bac4eae94217a1b')]:
 raw=subprocess.check_output(['git','cat-file','blob',h]);assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==h
 laws.append(dict(name=name,blob_sha1=h,sha256=hashlib.sha256(raw).hexdigest()))
new=[]
for p in sorted((R/'repro').glob('*.py')):
 raw=p.read_bytes();new.append(dict(path=str(p.relative_to(R)),blob_sha1=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),sha256=hashlib.sha256(raw).hexdigest()))
# summarize.py's own bytes are stable and content-addressable, no self-hash field is embedded in source.
(R/'09_SOURCE_CUSTODY.json').write_text(json.dumps(dict(adopted_law=laws,new_source_bodies=new,local_response_rule=definition(),local_response_source_hash=source_hash(),trusted_operative_owner_grants=False,production_registry_adoption=False,reviewer='HQ subsequent independent I2'),indent=2)+'\n')
print('RECEIPT AUDIT PASS: 36 actual cells, 12 fixed-entire-state history triplets, isolated mediator contrasts')
