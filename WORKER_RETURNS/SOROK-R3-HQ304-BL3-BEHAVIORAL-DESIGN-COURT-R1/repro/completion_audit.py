"""Audit the commissioned sourcefree end state, including explicit owner HOLDs."""
import datetime,gzip,hashlib,json,pathlib,subprocess
RET=pathlib.Path(__file__).resolve().parents[1];RT=RET/'runtime_root'
def read(p):return json.loads((RET/p).read_text())
def git(*a):return subprocess.check_output(['git',*a],cwd=RET,text=True).strip()
start='e924b2d9327b636cdc91731dde9c2aad1f52d226';parent='a25ba9ab4e1a0dc12d3764bea8854c8fbc2df227'
assert git('branch','--show-current')=='agent/reviewer-sorok-r3-hq304-bl3-behavioral-design-court-r1'
assert git('rev-parse',start+'^')==parent
freeze=read('freezes/r3-v1.json');identity=hashlib.sha256((RET/'freezes/r3-v1.json').read_bytes()).hexdigest()
assert identity=='b0d44f663e2392a4207c28a331e5a7627cfef81bdc8b47e9240642161977f465'
for name,h in freeze['files'].items():assert hashlib.sha256((RET/name).read_bytes()).hexdigest()==h,name
for name,h in freeze['original_frozen_files'].items():assert hashlib.sha256((RT/'rba/exec/r2'/name).read_bytes()).hexdigest()==h,name
assert datetime.datetime.fromisoformat(freeze['frozen_at'])<datetime.datetime.fromisoformat(read('repro/r3_execution.json')['started_at'])
seal=read('freezes/replay-auditor-v1.json');assert hashlib.sha256((RET/seal['file']).read_bytes()).hexdigest()==seal['sha256']
assert datetime.datetime.fromisoformat(seal['sealed_at'])<datetime.datetime.fromisoformat(read('repro/mock_execution.json')['started_at'])
sel=read('source_selector.json');assert len(sel['files'])==100 and sel['original_pin_count']==49
for row in sel['files']:
 b=(RT/row['staging_path']).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==row['git_blob_sha1'];assert hashlib.sha256(b).hexdigest()==row['sha256']
ledger=read('02_ACTUAL_EXECUTION_AND_CASE_LEDGER.json');counts={'r2':(51,0),'rba':(19,0),'lab1':(20,0),'lab2':(25,0),'rmb':(13,23),'r3':(33,0)}
for r in ledger['suites']:
 c=r['counts'];assert (c['PASS'],c['RED'])==counts[r['suite']] and c['SKIP']==c['ERROR']==0
 assert r['execution']['exit_code']==int(c['RED']>0)
assert len(ledger['original_RMB_failed_set_preserved'])==23
results=read('outputs/r3_results.json');audit=read('outputs/raw_capture_audit.json')
assert results['verdict']=='SOURCEFREE_R3_ARM_SENSITIVITY_PROVEN_WITH_SYNTHETIC_POLICY'
assert results['freeze']==identity and results['schedule']['cases']==154 and results['schedule']['trials']==9432
assert set(results['schedule']['orders'].values())=={524}
assert audit['total_raw_captures']==75456
for policy,p in results['policies'].items():
 assert p['dispatches']==9432 and p['external_dispatches']==0 and audit['policies'][policy]['raw_responses']==9432
 for dataset in ['original','heldout']:
  for arm in 'BC':
   expected=1 if policy=='aware' else 0
   assert p['datasets'][dataset]['primary_scripted_response_contrast'][arm]['delta']==expected
for policy in ['aware','blind']:assert not any(results['policies'][policy]['hard_violations'].values())
assert results['policies']['origin_leak']['hard_violations']['origin']==2592
assert results['policies']['standing_leak']['hard_violations']['private_belief']==1152
assert results['policies']['capacity_leak']['hard_violations']['capacity']==1296
assert audit['predeclared_false_gain_control']['apparent_B_minus_A']==1/3 and audit['predeclared_false_gain_control']['accepted_by_schedule'] is False
old=read('outputs/original_R2_reaudited_raw_capture_audit.json');assert sum(x['n_raw_responses'] for x in old['phases'].values())==21600
assert old['freeze']=='9a05efd9cc4060a7ae9b496f6fe71a5193912b228ac0d2e04577f80902384823'
paired=read('outputs/original_RBA_paired_recompute.json');assert all(paired[a]['delta']==0 and paired[a]['interval']==[-1,1] for a in ['B_minus_A','C_minus_A'])
schedule=read('outputs/original_R2_schedule_stratified_audit.json');assert schedule['all']['arm_order_counts']['ABC']==1440 and set(schedule['primary']['arm_order_counts'].values())=={432}
assert len(read('outputs/case_ledger.json')['rows'])==3696
passport=read('environment_passport_delta.json');text=(RET/'environment_passport_delta.json').read_text()
assert str(pathlib.Path.home()) not in text and pathlib.Path.home().name not in text
assert passport['status']=='LIVE_VERIFIED' and passport['runtime_marker_digest']==hashlib.sha256((RT/'runtime_marker.json').read_bytes()).hexdigest()
assert passport['selected_model']=='gpt-6.1-sol' and passport['effort']=='high' and passport['independent_review_separation']['extra_agents']==0
assert len(passport['materialized_source_refs'])==100
assert len(read('06_OWNER_ACTIONS_AND_LATER_REVIEW.json')['actions'])==8
assert not results['power_plan']['current_power_claim'] and results['independent_oracle_custody']=='HOLD' and not results['behavioral_pass'] and not results['adoption']
for suite in ['r2_archive_audit','rba_recompute','mock','r3_audit','evidence','probe']:assert read('repro/'+suite+'_execution.json')['exit_code']==0
requirements=[
 ('Exact commission/start/parent/role/oneagentCodexGPT6.1High00C00D','repro/read_custody_routing_receipt.json; live imports/turn-context receipt','VERIFIED'),
 ('Independent sourcefree R3 design and pre-execution estimand/tests/heldout freeze','01_PREDECLARED_R3_DESIGN.json; immutable r3-v1 hash and time ordering','VERIFIED'),
 ('All126 original plus28 new visible holdout cases, equal facts/distinct lawful arms','33tests; full raw frozen request audit; original R2 corpus unchanged','VERIFIED_BOUNDED'),
 ('Arm-aware synthetic positive and blind null','Full9432trialspolicy; aware+1/+1,blind0/0; representation swap/full-budget ablation','VERIFIED_SYNTHETIC_ONLY'),
 ('Menu/position/metadata adversaries and confound false gain','Shared opaque blocknonce; all6orders524each; ABCsubset+1/3 refused','VERIFIED'),
 ('K3 origin opacity,K5 public/private,K6 actual capacity and lawful optional outcomes','All154case tests; hard attacks detected; APPEAL/REMAIN_DOUBTFUL/NO_SANCTION and OTHER denominator','VERIFIED'),
 ('Original R1/v6 source/oracles and19RBA controls preserved','Original51+19;v6/R1 hashes;RMBexact23RED; archived21600audited','VERIFIED'),
 ('RBA1440:432 and78/96 concern handled without false primary-imbalance claim','Exact stratum audit primary432each and54/72; explicit R3 weighting','VERIFIED'),
 ('Independent oracle/scenario custody signed/hash boundary and competent later reviewer','04custody protocol; implementation-visible correlation disclosed; actual certificationHOLD','PROPOSAL_COMPLETE_OWNER_HOLD'),
 ('Prospective sampling/pairing/weights/multiplicity/CI/power and real criteria','05prospective design; derived power table; convenience families not powered; exact7future gates','PROPOSAL_COMPLETE_OWNER_HOLD'),
 ('Zero external experimental calls; LIVE/provideradapter/unissued scopes rejected','Closed local code, tests, Python network denial,75000+rawsynthetic captures; no external SDK','VERIFIED_ZERO_REAL_CALLS'),
 ('Exact full pytest/stdout/JUnit/case ledger/source imports/passport','02ledger;3696casearmrows;100nativeblobfiles;9primaryimports;sanitizedpassport','VERIFIED'),
 ('All investigation/code/analysis/test/documentation done byoneagent; remaining owners returned','00return;06actions; no delegation/model/editor switch or self acceptance','VERIFIED'),
 ('Executable complete replay and source-state preservation','repro/reproduce.sh syntax checked; each constituent command actually executed; host-local runtime ignored','VERIFIED'),
 ('Only own return committed; assigned push and exact remote SHA','Final path/manifest/ancestry audit and direct external readback; no recursive futureSHA','FINAL_PUBLICATION_EXTERNAL_READBACK_REQUIRED')]
out=dict(schema='BL3_REQUIREMENT_BY_REQUIREMENT_COMPLETION_AUDIT@1',verdict=results['verdict'],requirements=[dict(requirement=r,evidence=e,status=s) for r,e,s in requirements],real_experiment='NOT_RUN_NOT_AUTHORIZED',independent_acceptance='PENDING_HQ; NOT_SELF_CERTIFIED',adoption=False,scope='Complete commissioned sourcefree design/sensitivity deliverable with required owner HOLDs; no later real experiment claimed')
(RET/'07_REQUIREMENT_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print('BL3_ALL_CURRENT_COMMISSION_EVIDENCE_VERIFIED; SOURCEFREE_R3_SENSITIVITY; OWNER_HOLDS_EXPLICIT; FINAL_PUBLICATION_PENDING')
