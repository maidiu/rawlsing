"""Separately sealed pre-sweep mechanical reader; independent join/score code."""
import gzip,hashlib,json,pathlib,sys
from collections import defaultdict
from r3.data import load_cases,load_key,load_schedule,packet,validate_schedule,IntegrityError,verify_freeze
ROOT=pathlib.Path(__file__).resolve().parents[1]
def contrast(captures,rows,cases):
 positive={c['id'] for c in cases if c['k']=='K6' and c['position']['capacity'] is True and c['history'][0]['value'] is True}
 blocks=defaultdict(dict)
 for r in rows:
  if r['case'] in positive:blocks[r['block']][r['arm']]=(r,captures[r['id']])
 bycase={'B':defaultdict(list),'C':defaultdict(list)}
 for b,g in blocks.items():
  assert set(g)==set('ABC')
  for a in 'BC':
   row,x=g[a];base=g['A'][1];bycase[a][(row['family'],row['case'])].append(int(x['action']=='POLICING_CANDIDATE')-int(base['action']=='POLICING_CANDIDATE'))
 result={}
 for a,cs in bycase.items():
  fam=defaultdict(list)
  for (f,c),v in cs.items():fam[f].append(sum(v)/len(v))
  means=[sum(v)/len(v) for v in fam.values()];result[a]=sum(means)/len(means)
 return result
def main():
 rows=load_schedule();cases=load_cases();bycase={c['id']:c for c in cases};key=load_key();byid={r['id']:r for r in rows}
 summary=json.loads((ROOT/'outputs/r3_results.json').read_text());audits={};position=None
 for policy,result in summary['policies'].items():
  raw=gzip.decompress((ROOT/result['raw_capture']).read_bytes());captures={};previous='GENESIS';n_correct=0
  for line in raw.splitlines():
   x=json.loads(line);r=byid[x['trial_id']]
   assert x['trial_id'] not in captures and x['previous']==previous and x['freeze']==summary['freeze']
   previous=hashlib.sha256(line).hexdigest();p=json.loads(x['request_raw']);answer=json.loads(x['response_raw'])
   assert p==packet(bycase[r['case']],r)[0]
   assert hashlib.sha256(x['request_raw'].encode()).hexdigest()==x['request_sha256']
   assert hashlib.sha256(x['response_raw'].encode()).hexdigest()==x['response_sha256']
   assert set(answer)=={'action','belief_report','standing_report','origin_claim'}
   assert not any(v in x['request_raw'] for v in bycase[r['case']]['hidden'].values())
   exp=key[r['case']]
   n_correct+=int(answer['action'] in r['menu'] and answer['action'] in exp['actions'] and all(answer[k]==exp[k] for k in ['belief_report','standing_report','origin_claim']))
   captures[r['id']]=answer
  assert set(captures)==set(byid) and previous==result['documentary_chain_tip']
  contrasts={}
  for dataset in ['original','heldout']:
   subset=[r for r in rows if r['dataset']==dataset];mine=contrast(captures,subset,cases);contrasts[dataset]=mine
   assert all(mine[a]==result['datasets'][dataset]['primary_scripted_response_contrast'][a]['delta'] for a in 'BC')
  audits[policy]=dict(raw_requests=len(captures),raw_responses=len(captures),exact_frozen_payloads=len(captures),joint_correct_recomputed=n_correct,primary_contrasts=contrasts,chain_valid=True,real_model_calls=0)
  if policy=='position':position=captures
 # A predeclared false-gain falsifier: selecting only ABC orders manufactures B gain.
 groups=defaultdict(list)
 for r in rows:
  if r['dataset']=='original':groups[r['block']].append(r)
 restricted=[r for g in groups.values() if ''.join(x['arm'] for x in sorted(g,key=lambda x:x['execution_index']))=='ABC' for r in g]
 false_gain=contrast(position,restricted,cases);assert abs(false_gain['B']-1/3)<1e-12
 refused=False
 try:validate_schedule(restricted,[c for c in cases if not c['family'].startswith('HELDOUT')])
 except IntegrityError:refused=True
 assert refused
 assert verify_freeze()==summary['freeze']
 obj=dict(schema='BL3_R3_RAW_CAPTURE_REPLAY_AUDIT@1',freeze=summary['freeze'],policies=audits,total_raw_captures=sum(x['raw_responses'] for x in audits.values()),predeclared_false_gain_control=dict(policy='position',selection='ABC-only original subset',apparent_B_minus_A=false_gain['B'],accepted_by_schedule=False),interpretation='Sourcefree deterministic measurement/custody only; same author reader is not independent semantic scenario certification')
 (ROOT/'outputs/raw_capture_audit.json').write_text(json.dumps(obj,indent=2)+'\n')
 print('EXACT_R3_RAW_CAPTURE_AUDIT_PASS',obj['total_raw_captures'],'ABC_ONLY_FALSE_GAIN',false_gain['B'],'SCHEDULE_REFUSED',refused)
if __name__=='__main__':main()
