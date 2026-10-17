"""Exact, scoped negative source-authority evidence; not a universal absence claim."""
from pathlib import Path
import hashlib,json,subprocess
HERE=Path(__file__).resolve().parents[1];REPO=HERE.parents[1]
PIN='eede2b8bdb9fcdcc1d4187912f8e00773869c22c'
PACKET='98874e4559c4837dfd5922182fb5fa7bd4a00d0d'
E2BI='e894c8f5cb394b07d9c63ee702cfead23e9e81b5'
CP='HQ_HANDOFF/checkpoints/20261017-PYAT-HQ-R28-SIX-RETURN-SCIENCE-AND-FIVE-ORIGINAL-PRODUCT-LANES-R1/'

def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def record(commit,path,terms=()):
 b=git('show',f'{commit}:{path}');lines=b.decode().splitlines()
 return {'commit':commit,'path':path,'git_blob':git('rev-parse',f'{commit}:{path}').decode().strip(),
  'sha256':hashlib.sha256(b).hexdigest(),'selected_lines':[{'line':i,'text':v} for i,v in enumerate(lines,1) if any(t.lower() in v.lower() for t in terms)]}

def main():
 pointer=json.loads(git('show',f'{PIN}:HQ_HANDOFF/LATEST.json'))
 assert pointer['handoff_commit']==PACKET
 assert git('show',f'{PIN}:{CP}CURRENT.md')==git('show',f'{PACKET}:{CP}CURRENT.md')
 evidence=[record(PIN,'HQ_HANDOFF/LATEST.json'),record(PACKET,CP+'CURRENT.md',('Top unresolved','No U/E_pre','SOURCEFREE methods ONLY')),
  record('246fcdf7b25c6b160c0a167e4284e08d04194505','WORKER_COMMISSIONS/PYAT-R28-O35E-ORIGINAL35-ELIGIBILITY-NATIVE-CRITICAL-PATH-R1/00_COMMISSION.md',('sourcefree access','signed','No source data')),
  record(E2BI,'WORKER_RETURNS/PYAT-HQ280-E2BI-ISSUER-SEAL-CONTEXT-EXPECTATION-R1/00_RETURN.md',('Disposition:','Narrow outstanding','literal exact original','original source recomputation')),
  record(E2BI,'WORKER_RETURNS/PYAT-HQ280-E2BI-ISSUER-SEAL-CONTEXT-EXPECTATION-R1/01_EXACT_COMPETENT_ISSUER_GRAPH.json'),
  record(PIN,'PYAT_CONTROL_ROOM/WHOLE_MACHINE_ASSESSMENT_AND_PLAN_20261011_R1/SOURCE35_RECONCILIATION.json'),
  record(PIN,'PYAT_CONTROL_ROOM/WHOLE_MACHINE_ASSESSMENT_AND_PLAN_20261011_R1/ACTION_PLAN.md',('E2B-I bounded','signed/adopted','No source grant')),
  record(PIN,'PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/WAVE_BARRIERS.md',('GT12','Uganda','LiTS','GSS2024')),
  record(PIN,'PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ272_M01_F01_SOURCE_NATIVE_TRIPLE_AND_FF02_SEMANTIC_INTAKE_R1.md',('freshly streamed','c9200ba','3afcecd','No GT3 act','not automatically')),
  record('0533516fe939bb1d91be108b4bf05249639afbae','WORKER_COMMISSIONS/PYAT-R28-WG0O-RELEASE-AUTHORITY-RESIDUAL-COURT-R1/00_COMMISSION.md',('rel.authorities','No original35'))]
 graph=json.loads(git('show',f'{E2BI}:WORKER_RETURNS/PYAT-HQ280-E2BI-ISSUER-SEAL-CONTEXT-EXPECTATION-R1/01_EXACT_COMPETENT_ISSUER_GRAPH.json'))
 original=json.loads((HERE/'PREREGISTERED_EXPECTATIONS.json').read_text())
 holds=[]
 for i,case in enumerate(original['unexecuted_original_controls']):
  holds.append({'case':case,'status':'NOT_EXECUTED__UNCONSTRUCTIBLE_ORIGINAL_SOURCE_AUTHORITY',
   'original_eligible_item_ref':None,'preserved_metadata_item_for_prospective_owner_review':original['five_preserved_relation_item_omission_controls'][i] if i<5 else None,
   'reason':'QRA metadata identity and structural relation disposition do not issue source-original operation eligibility; no verified current signed U/E_pre and source-execution warrant for this commission.',
   'not_counted_as_pass':True,'consumer_called':False})
 out={'schema':'O35E_SOURCE_GRANT_NEGATIVE_EVIDENCE@1','canonical_read_cut':PIN,
  'pointer_relevant_fields':{k:pointer[k] for k in ('checkpoint_id','handoff_commit','new_operative_grants','measured_execution_authorized','measured_execution_authorized_via_warrant','p2_authorized','oc05_installation_authorized','n11_accepted','n12_v3_wake_authorized','next_action')},
  'scope_of_negative':'No verified currently applicable original-source + prospective U/E_pre issuance for this assigned new native experiment. Not a claim that original sources, historical bounded lawful uses, or competent humans do not exist.',
  'historical_gt12_context':{'status':'PRESERVED_NOT_REEXECUTED_NOT_WIDENED','exact_source_refs':graph['exact_source_refs'],'missing_issuer_edges':graph['missing_edges'],
   'forbidden_shortcut':'Existing CONTEXT replay permission is not new SAV/I03/I05/Batch, all35 U/E_pre or a backdated prospective expectation.'},
  'original_negative_controls':holds,'signed_original_warrants_verified_for_this_run':0,'original_data_reads':0,'new_U_or_E_pre_issuances':0,
  'evidence':evidence}
 (HERE/'source_grant_negative_evidence.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
 protocols=[record(PIN,p) for p in (
  'PYAT_CONTROL_ROOM/00D_WARM_EXECUTION_PASSPORT_AND_MONEY_FIRST_AGENT_DISPENSATION_R1.md',
  'PYAT_CONTROL_ROOM/SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md',
  'PYAT_CONTROL_ROOM/00_WHOLE_MACHINE_AUTOMATION_DOCTRINE_R1.md',
  'PYAT_CONTROL_ROOM/26_HQD216_PRODUCTIVE_ADEQUACY_AND_PREV3_EMPIRICAL_GATE_LAW.md',
  'PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/README.md',
  'PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/AUTOMATED_WORKLOAD_CONSTRUCTION_CRITICAL_GATE.md')]
 protocols += [record('3c33688506840869e1f05f4230248ce950b78d6c','SOROK_PRODUCT_CONTROL_ROOM/'+p) for p in (
  '00C_HQ_PROMPT_DISPENSATION_AGENT_ROUTING_AND_ORCHESTRATION_CONSTITUTION_R1.md',
  '00D_WARM_ENVIRONMENT_PASSPORT_AND_COST_AWARE_AGENT_DISPENSATION_R1.md')]
 protocols += [record('d800848bbff502658c9f1ed50fce73f1fc7dcad7','WORKER_RETURNS/PYAT-R18-EST1-ORIGINAL-ESTATE-CRITICAL-PATH-R1/'+p) for p in (
  '00_RETURN_AND_FIRST_ORIGINAL_REALIZATION_EDGE.md',
  '03_WG0P4_WG0L_HANDOFF_AND_AUTHORITY_BOUNDARY.md',
  '04_NEXT_COMPETENT_ISSUERS_AND_REAL_CONSUMER_GATE.md')]
 (HERE/'READ_SET.json').write_text(json.dumps({'protocol_read_cut':protocols,'source_authority_read_cut':'source_grant_negative_evidence.json'},indent=2)+'\n')
 print(json.dumps({'exact_sources':len(evidence),'original_controls_not_executed':len(holds),'verified_original_run_grants':0}))

if __name__=='__main__':main()
