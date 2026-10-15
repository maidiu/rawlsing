"""Deterministic complete synthetic sweep with exact request/response retention."""
import gzip,hashlib,json,pathlib
from collections import Counter,defaultdict
from .data import ROOT,load_cases,load_key,load_schedule,verify_freeze,validate_schedule,packet,DerivedCache
from .policies import POLICIES
from .transport import MockIssuer,MockTransport
from .analysis import evaluate,paired,conditional_power_table
from .audit import violations
def main():
 freeze=verify_freeze();cases=load_cases();bycase={c['id']:c for c in cases};key=load_key();rows=load_schedule()
 schedule_audit=validate_schedule(rows,cases);output=ROOT/'outputs';summaries={}
 positive={c['id'] for c in cases if c['k']=='K6' and any(e['field']=='practiced' and e['value'] is True for e in c['history']) and c['position']['capacity'] is True}
 for policy in sorted(POLICIES):
  issuer=MockIssuer();grant=issuer.issue(freeze,policy,len(rows));transport=MockTransport(grant,issuer,freeze,policy,rows)
  cache=DerivedCache();captures={};raw_lines=[];hard=Counter();previous='GENESIS'
  for row in rows:
   p,receipt=packet(bycase[row['case']],row,cache)
   request=json.dumps(p,sort_keys=True,separators=(',',':'));raw,read=transport.call(row,p);captures[row['id']]=raw
   answer=json.loads(raw);hard.update({k:int(v) for k,v in violations(bycase[row['case']],answer,key[row['case']]).items()})
   body=dict(trial_id=row['id'],block=row['block'],case=row['case'],dataset=row['dataset'],arm=row['arm'],request_raw=request,response_raw=raw,request_sha256=hashlib.sha256(request.encode()).hexdigest(),response_sha256=hashlib.sha256(raw.encode()).hexdigest(),source_facts_digest=receipt['facts_digest'],representation_digest=receipt['representation_digest'],policy_read_receipt=read,previous=previous,freeze=freeze,evidence_grade='SYNTHETIC_MEASUREMENT_CONTROL_ONLY')
   line=json.dumps(body,sort_keys=True,separators=(',',':'));previous=hashlib.sha256(line.encode()).hexdigest();raw_lines.append(line)
  records=evaluate(rows,captures,key);per_dataset={}
  for dataset in ['original','heldout']:
   subset=[r for r in rows if r['dataset']==dataset];ids={r['id'] for r in subset};recs=[r for r in records if r['id'] in ids]
   primary=paired(recs,subset,{c for c in positive if any(x['case']==c for x in subset)},metric='policing')
   per_dataset[dataset]=dict(primary_scripted_response_contrast=primary,joint_lawful_accuracy=paired(recs,subset),fraction_joint_correct=sum(r['correct'] for r in recs)/len(recs),n_planned=len(recs),OTHER_UNSCORABLE=sum(r['coded']['action']=='OTHER_UNSCORABLE' for r in recs))
  summaries[policy]=dict(dispatches=transport.dispatches,external_dispatches=transport.external_dispatches,n_planned=len(rows),datasets=per_dataset,hard_violations=dict(hard),documentary_chain_tip=previous,raw_capture='outputs/'+policy+'_captures.jsonl.gz',raw_capture_semantics='Exact frozen full request and raw typed response, complete IDs; documentary SHA chain, not independent issuer attestation')
  (output/(policy+'_captures.jsonl.gz')).write_bytes(gzip.compress(('\n'.join(raw_lines)+'\n').encode(),mtime=0))
  print('POLICY',policy,'DISPATCHES',transport.dispatches,'PRIMARY_BA',per_dataset['original']['primary_scripted_response_contrast']['B']['delta'],'HARD',dict(hard),flush=True)
 assert all(summaries['aware']['datasets'][d]['primary_scripted_response_contrast'][arm]['delta']==1 for d in ['original','heldout'] for arm in 'BC')
 for policy in ['blind','first','position','metadata']:
  assert all(summaries[policy]['datasets'][d]['primary_scripted_response_contrast'][a]['delta']==0 for d in ['original','heldout'] for a in 'BC')
 for policy,field in [('origin_leak','origin'),('standing_leak','standing'),('capacity_leak','capacity')]:assert summaries[policy]['hard_violations'][field]>0
 assert not any(summaries['aware']['hard_violations'].values()) and not any(summaries['blind']['hard_violations'].values())
 assert verify_freeze()==freeze
 result=dict(schema='BL3_R3_SYNTHETIC_ASSAY_RESULT@1.0.0',verdict='SOURCEFREE_R3_ARM_SENSITIVITY_PROVEN_WITH_SYNTHETIC_POLICY',freeze=freeze,schedule=schedule_audit,policies=summaries,power_plan=conditional_power_table(),external_experimental_model_calls=0,actor_calls=0,independent_oracle_custody='HOLD',behavioral_pass=False,adoption=False)
 (output/'r3_results.json').write_text(json.dumps(result,indent=2)+'\n')
 print('R3_COMPLETE_SOURCEFREE_SENSITIVITY_ONLY; ZERO_EXTERNAL_EXPERIMENTAL_CALLS')
if __name__=='__main__':main()
