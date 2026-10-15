"""Exact per-test ledger and per-case/arm synthetic response census."""
import collections,gzip,hashlib,json,pathlib,xml.etree.ElementTree as ET
from r3.data import load_cases,load_key,load_schedule,verify_freeze
ROOT=pathlib.Path(__file__).resolve().parents[1]
results=[]
for suite in ['r2','rba','lab1','lab2','rmb','r3']:
 cases=[]
 for t in ET.parse(ROOT/'repro'/f'{suite}.xml').getroot().iter('testcase'):
  f=t.find('failure');e=t.find('error');s=t.find('skipped');x=f if f is not None else e if e is not None else s
  cases.append(dict(name=t.attrib['name'],status='RED' if f is not None else 'ERROR' if e is not None else 'SKIP' if s is not None else 'PASS',diagnostic=x.text if x is not None else None))
 counts={k:sum(t['status']==k for t in cases) for k in ['PASS','RED','ERROR','SKIP']}
 results.append(dict(suite=suite,counts=counts,execution=json.loads((ROOT/'repro'/f'{suite}_execution.json').read_text()),cases=cases))
actual={t['name'] for r in results if r['suite']=='rmb' for t in r['cases'] if t['status']=='RED'}
original={t.attrib['name'] for t in ET.parse(ROOT/'runtime_root/retained_rba/repro/rmb_review.xml').getroot().iter('testcase') if t.find('failure') is not None}
assert actual==original and len(actual)==23
summary=json.loads((ROOT/'outputs/r3_results.json').read_text());rows={r['id']:r for r in load_schedule()};key=load_key();case_map={c['id']:c for c in load_cases()};ledger=[]
for policy,result in summary['policies'].items():
 groups=collections.defaultdict(lambda:dict(n=0,joint_correct=0,actions=collections.Counter()))
 for line in gzip.decompress((ROOT/result['raw_capture']).read_bytes()).splitlines():
  x=json.loads(line);r=rows[x['trial_id']];a=json.loads(x['response_raw']);expected=key[r['case']];g=groups[(r['case'],r['arm'])]
  g['n']+=1;g['actions'][a['action']]+=1;g['joint_correct']+=int(a['action'] in expected['actions'] and a['action'] in r['menu'] and all(a[k]==expected[k] for k in ['belief_report','standing_report','origin_claim']))
 for (cid,arm),g in sorted(groups.items()):
  c=case_map[cid];ledger.append(dict(policy=policy,case=cid,family=c['family'],k=c['k'],dataset='heldout' if c['family'].startswith('HELDOUT') else 'original',arm=arm,n_planned=g['n'],joint_correct=g['joint_correct'],actions=dict(g['actions']),independent_scenario_custody=False))
(ROOT/'outputs/case_ledger.json').write_text(json.dumps(dict(schema='BL3_ACTUAL_CASE_ARM_CENSUS@1',rows=ledger,all_planned_outcomes_retained=True,source='Exact raw synthetic captures; no new responses sampled'),indent=2)+'\n')
obj=dict(schema='BL3_ACTUAL_EXECUTION_LEDGER@1',suites=results,original_RMB_failed_set_preserved=sorted(actual),new_R3_freeze=verify_freeze(),R3_mock_dispatches=sum(x['dispatches'] for x in summary['policies'].values()),R3_raw_capture_audit='outputs/raw_capture_audit.json',original_R2_raw_capture_audit='outputs/original_R2_reaudited_raw_capture_audit.json',original_RBA_paired_recompute='outputs/original_RBA_paired_recompute.json',setup_disclosures=['Staging report called48objects; exactmanifest has49includingdesign doc. Actual49verified.','Initial freeze check selected preregistration_v6 instead of freezes/v6. Corrected path before any R3 response/test. No frozen source changed.','Initial LAB2 suite24PASS1missing layout alias; exact original freeze receipt materialized at required path and unchanged25PASS rerun. Initial logs/JUnit retained.'],claim_ceiling=summary['verdict'],external_experimental_calls=0,oracle_custody='HOLD',real_provider_adapter='NOT_IMPLEMENTED_UNCONDITIONALLY_DENIED',adoption=False)
(ROOT/'02_ACTUAL_EXECUTION_AND_CASE_LEDGER.json').write_text(json.dumps(obj,indent=2)+'\n')
print('EXACT_CASE_LEDGER',len(ledger),'R3_RAW_RESPONSES',obj['R3_mock_dispatches'],'ORIGINAL_RMB23_SET_UNCHANGED')
for r in results:print(r['suite'],r['counts'])
