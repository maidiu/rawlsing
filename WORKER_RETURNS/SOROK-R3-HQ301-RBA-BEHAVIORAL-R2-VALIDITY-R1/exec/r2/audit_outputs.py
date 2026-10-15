"""Read actual raw captures and independently check schedule/serialization integrity."""
from pathlib import Path
import gzip,json,hashlib,argparse
from collections import Counter,defaultdict
from assay.transport import Frozen,MOCK_MODEL
from assay.architecture import canonical,digest
from assay.experiment import code_capture
R=Path(__file__).resolve().parent

def main(run_id):
 root=R/'receipts'/run_id;summary=json.loads((root/'summary.json').read_text())
 f=Frozen(R,R/(R/'CURRENT_FREEZE').read_text().strip());audits={}
 for name,s in summary.items():
  entries=[json.loads(line) for line in gzip.decompress((root/name/'ledger.jsonl.gz').read_bytes()).splitlines()]
  coded=json.loads(gzip.decompress((root/name/'coded_captures.json.gz').read_bytes()))
  interventions=json.loads(gzip.decompress((root/name/'intervention_receipts.json.gz').read_bytes()))
  previous='GENESIS';reserved={};captured={};request_hash={};total=0
  for entry in entries:
   b=entry['body'];assert b['previous']==previous;previous=digest(entry)
   assert b['evidence_label']=='MOCK_ONLY_NOT_BEHAVIORAL_EVIDENCE'
   if b['op']=='RESERVE':
    tid=b['trial'];row=f.rows[tid];p,unused=f.approved(tid)
    raw=b['request_raw'].encode();request=json.loads(raw)
    assert request['model']==MOCK_MODEL and request['temperature']==0 and request['seed']==17
    assert request['max_tokens']==row.get('max_tokens',256)
    assert request['response_format']==row.get('response_format','typed')
    assert request['packet']==p
    assert hashlib.sha256(raw).hexdigest()==b['request_hash']
    assert not any(x in raw.decode() for x in f.cases[row['case']]['hidden'].values())
    assert 'mistaken' not in raw.decode()
    reserved[tid]=reserved.get(tid,0)+1;request_hash[tid]=b['request_hash'];total+=b['reserved_micro']
   elif b['op']=='CAPTURE':
    assert b['request_hash']==request_hash[b['trial']]
    assert b['trial'] not in captured
    captured[b['trial']]=b['response_raw']
   else:assert b['op']=='START'
  assert len(reserved)==s['n_planned']==len(captured)==len(coded)==len(interventions)
  assert all(n==1 for n in reserved.values())
  assert all(coded[tid]==code_capture(raw,f.rows[tid]) for tid,raw in captured.items())
  assert total==s['reserved_mock_micro_units']==s['transport_attempts']==s['mock_dispatches']
  origin_violations=sum(json.loads(raw).get('origin_claim')!='NO_CLAIM' for raw in coded.values())
  key=json.loads((R/f.manifest['oracle_file']).read_text())
  belief_violations=sum(json.loads(raw).get('belief_report')!=key[f.rows[tid]['case']]['belief_report'] for tid,raw in coded.items() if f.rows[tid]['k']=='K5')
  standing_violations=sum(json.loads(raw).get('standing_report')!=key[f.rows[tid]['case']]['standing_report'] for tid,raw in coded.items() if f.rows[tid]['k']=='K5')
  cache_hits=sum(x['cache_hits'] for x in interventions.values())
  assert cache_hits>0
  audits[name]=dict(n_raw_requests=len(reserved),n_raw_responses=len(captured),
                   exact_frozen_request_matches=len(reserved),documentary_hash_chain_valid=True,
                   signatures='Validated in live mock process; ephemeral test key deliberately not archived; no issuer attestation claimed',
                   reserved_mock_units=total,positive_cache_hits=cache_hits,real_model_calls=0,
                   origin_claim_violations=origin_violations,private_belief_report_violations=belief_violations,standing_report_violations=standing_violations,
                   hard_invariant_failure=any([origin_violations,belief_violations,standing_violations]),behavioral_inference_allowed=False)
 groups=defaultdict(Counter);orders=defaultdict(Counter)
 for row in f.rows.values():
  if row.get('phase','primary')!='primary':continue
  for code in row['menu']:groups[(row['case'],row['arm'],code,len(row['menu']))][row['menu'].index(code)]+=1
  orders[(row['case'],row['arm'])][row['execution_index']]+=1
 assert all(set(c)==set(range(n)) and len(set(c.values()))==1 for (*unused,n),c in groups.items())
 assert all(set(c)=={0,1,2} and len(set(c.values()))==1 for c in orders.values())
 result=dict(freeze=f.identity,phases=audits,all_menu_positions_present_and_equal=True,all_execution_positions_equal=True,
             original_R1_sha256=hashlib.sha256((R/'original_R1_preregistration.json').read_bytes()).hexdigest(),
             sourcefree_only=True,audit_layer_code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),independent_scientific_acceptance='NOT_PERFORMED')
 (root/'raw_capture_audit.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('run_id');main(p.parse_args().run_id)
