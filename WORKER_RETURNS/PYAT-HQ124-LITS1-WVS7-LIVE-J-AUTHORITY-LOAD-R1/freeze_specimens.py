"""Freeze the bounded court using only current authority; no raw-source values."""
from pathlib import Path
import csv,json,hashlib,datetime
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
E=OUT/'evidence'
F=E/'FROZEN_PREVALUE_SELECTION.json'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def members(s):
 if s.startswith('['): return json.loads(s.replace('\\"','"'))
 return s.split('|')
def rows(p):return list(csv.DictReader(p.open()))
if F.exists():raise SystemExit('Specimen freeze already exists; never overwrite it after source-value access.')
assert digest(E/'CURRENT_J_CANDIDATE_UNIVERSE_FROZEN.csv')=='b21a79947f19f4c520ea493480a38ef8b23cb6797444eeb913bc8575b6cafb64'
assert digest(E/'D5_CURRENT_SUCCESSION_CROSSWALK.csv')=='2ffd94620212fc00af49c4e775b99a83144b71c72387c1da69d412c7edc7f33a'
assert digest(E/'D2_OBL009_CURRENT_SUCCESSION_CROSSWALK.csv')=='5a067ad23537c577efbc6f625a2d7ac71ed67eab918f35cc8bc6f2d610b9322c'
allrows=rows(E/'CURRENT_J_CANDIDATE_UNIVERSE_FROZEN.csv')
selected=[]
for source,family,scope,slots,lane in [('LiTS_I','LiTS','2006',['q301_2','q301_7','q310','q311'],'D5_CURRENT_SUCCESSION_CROSSWALK.csv'),('WVS7','WVS','W7',['Q291G5','Q291P5'],'D2_OBL009_CURRENT_SUCCESSION_CROSSWALK.csv')]:
 authority_scope=[r for r in allrows if r['source_family']==family and r['wave_or_scope']==scope]
 def key(r):
  m=members(r['source_native_member_identities']); overlap=set(m)&set(slots)
  return (not set(m)<=set(slots),not bool(overlap),len(m),r['current_source_structure_id'])
 r=min(authority_scope,key=key)
 native=members(r['source_native_member_identities']);qids=members(r['current_question_implementation_ids']);assert len(native)==int(r['member_count'])==len(qids)
 s=next(s for s in rows(E/lane) if s['current_source_structure_id']==r['current_source_structure_id'])
 assert native==members(s['current_member_ids_or_native_members'])
 assert r['candidacy_disposition']=='CURRENT_J_CANDIDATE'
 selected.append({'source':source,'specimen_ordinal':1,'candidate_row':r,'current_joint_contract_id':'CURRENT_JOINT_AUTHORITY_CONTRACT@1','current_joint_succession_row':s,'governed_native_component_order':native,'governed_question_implementation_order':qids,'qualified_projection_slots':slots,'whole_specimen_projection_coverage':set(native)<=set(slots),'projection_missing_native_components':[x for x in native if x not in slots],'projection_intersection':[x for x in native if x in slots],'lane_file':lane,'selection_reason':'Current selected-B exact whole-set correspondence first; then any exact qualified-slot intersection; then smallest governed set; then lexicographic current ID. No outcome/statistical data used.','candidate_scope_metadata_rows_considered':len(authority_scope)})
qualified=['rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py','rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py','rawlsing_next/fiabc_lits_i_representation_authority.py','rawlsing_next/fiabc_lits_i_f02_event_representation_authority.py','rawlsing_next/fiabc_lits_i_d03_risk_set_authority.py','PYAT_CONTROL_ROOM/21_HQD122_J_ROLE_CERTIFICATION_SUCCESSION_ADOPTION.md','rawlsing_next/pre553_j_role_certification.py']
receipt={'schema':'HQ124_PREVALUE_SPECIMEN_SELECTION@1','frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commission_commit':'c44df7f99fcf86763431ea8c98f74c0245c94670','selection_count_per_source':1,'respondent_outcome_values_accessed_before_freeze':False,'source_full_decodes_before_freeze':{'LiTS_I':0,'WVS7':0},'selection_authority_file_sha256':digest(E/'CURRENT_J_CANDIDATE_UNIVERSE_FROZEN.csv'),'qualified_binders_and_role_law':[{'path':x,'sha256':digest(ROOT/x)} for x in qualified],'specimens':selected,'second_specimen':'NOT_SELECTED__FIRST_CAN_DISTINGUISH_FULL_J_SCOPE_FROM_QUALIFIED_PATH_COVERAGE','cross_source_pooling_or_comparability':'NOT_CLAIMED'}
F.write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
print('Frozen:',[(s['source'],s['candidate_row']['current_source_structure_id']) for s in selected]);print('Freeze SHA256',digest(F))
