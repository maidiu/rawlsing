"""Bank HQ124 preparation. This script never reads respondent outcome values."""
from pathlib import Path
import csv,hashlib,json,subprocess,datetime
OUT=Path(__file__).resolve().parent
E=OUT/'evidence'
ROOT=OUT.parents[1]
JROOT='data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/'
DROOT=JROOT+'PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/D_CURRENT_ADMISSION_JOINT_AUTHORITY_R1/WORKERS/'
provenance=[]
def bank(commit,path,target):
 b=subprocess.check_output(['git','show',commit+':'+path],cwd=ROOT)
 (E/target).write_bytes(b)
 provenance.append({'commit':commit,'path':path,'retained':target,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)})
for fn in ['08_SOURCE_FREE_VS_LIVE_OCCUPANCY_BOUNDARY.md','09_EXACT_REMAINING_GAPS.tsv']:
 bank('e7e6fdb25031b8d0ebc1bc8b357460814f385f01','WORKER_RETURNS/PYAT-HQ123-SIX-STAGE-SOURCE-FREE-NO-LOSS-COURT-R1/'+fn,'HQ123_'+fn)
bank('44e97e420d38b6a2b0c44034929b5994a352d8b6',JROOT+'CURRENT_JOINT_AUTHORITY_CLOSURE_R1/J01A_GLOBAL_FREEZE_R4/CURRENT_J_CANDIDATE_UNIVERSE_FROZEN.csv','J01A_CANDIDATE_LIBRARY_POINTER.csv')
bank('44e97e420d38b6a2b0c44034929b5994a352d8b6',JROOT+'CURRENT_JOINT_AUTHORITY_CLOSURE_R1/J01A_GLOBAL_FREEZE_R4/RETURN_POINTER.json','J01A_RETURN_POINTER.json')
bank('ed641eb74ead4dc5db1cada84af007577758b1e2',DROOT+'D8_OBL009_J01B_GLOBAL_JOIN_COLLISION_COMPLETENESS_R1/RETURN/GLOBAL_CURRENT_SUCCESSION_CROSSWALK_POINTER.json','J01B_GLOBAL_POINTER.json')
bank('390050d959079a7bff0c0a8582a368d0b1094f96',DROOT+'D2_OBL009_J01B_WVS_EVS_SUCCESSION_R1/RETURN/CURRENT_SUCCESSION_CROSSWALK.csv','D2_OBL009_CURRENT_SUCCESSION_CROSSWALK.csv')
bank('52e5da4d5e4fcce945a2ede6a89095753144d13e',DROOT+'D5_OBL009_J01B_SOUTHASIA_LITS_SUCCESSION_R1/RETURN/RETURN_POINTER.json','J01B_D5_RETURN_POINTER.json')
(E/'AUTHORITY_RECOVERY_PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n')
assert hashlib.sha256((E/'D2_OBL009_CURRENT_SUCCESSION_CROSSWALK.csv').read_bytes()).hexdigest()=='5a067ad23537c577efbc6f625a2d7ac71ed67eab918f35cc8bc6f2d610b9322c'
assert hashlib.sha256((E/'J01A_CANDIDATE_LIBRARY_POINTER.csv').read_bytes()).hexdigest()!='b21a79947f19f4c520ea493480a38ef8b23cb6797444eeb913bc8575b6cafb64'
# A pointer with a .csv extension is not a materialized candidate carrier.
stale=E/'J01A_CURRENT_J_CANDIDATE_UNIVERSE_FROZEN.csv'
if stale.exists(): stale.unlink()
def tsv(name,fields,rows):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(rows)
def md(name,text): (OUT/name).write_text(text+'\n')
rows=[]
for s,f in [('LiTS_I','LITS_I_METADATA.json'),('WVS7','WVS7_METADATA.json')]:
 d=json.loads((E/f).read_text())
 assert d['respondent_outcome_values_accessed'] is False
 rows.append(dict(source=s,path=d['source_path'],sha256=d['source_sha256'],physical_rows=d['rows'],physical_variables=d['variables'],metadata_only_inspections=1,full_decodes=0,specimens_selected=0,selection_status='NOT_FROZEN__EXACT_CURRENT_AUTHORITY_CARRIER_UNAVAILABLE',consumed_outcome_columns='NONE',retry='NONE',retained_intermediate='evidence/'+f))
tsv('01_SOURCE_IDENTITY_AND_READ_DISCIPLINE.tsv',list(rows[0]),rows)
tsv('02_PREVALUE_SPECIMEN_SELECTION.tsv',['source','state','specimen_id','selection_rule_when_inputs_arrive','value_access','blocker'],[
 {'source':'LiTS_I','state':'PENDING__NO_SPECIMEN_SELECTED','specimen_id':'UNRESOLVED__NOT_FABRICATED','selection_rule_when_inputs_arrive':'Exactly one LiTS/2006 current J01-A specimen, prioritize exact selected-B component correspondence then minimal governed component count then lexicographic current_source_structure_id; cross-check current J01-B; freeze before value access','value_access':'NONE','blocker':'J01-A row carrier and LiTS D5 exact crosswalk unavailable'},
 {'source':'WVS7','state':'PENDING__NO_SPECIMEN_SELECTED','specimen_id':'NONE__PREFERENCE_ONLY','selection_rule_when_inputs_arrive':'Exactly one WVS/W7 current J01-A specimen, prioritize exact selected-B component correspondence then minimal governed component count then lexicographic current_source_structure_id; freeze before value access','value_access':'NONE','blocker':'J01-A row carrier unavailable; exact current J01-B lane recovered'}])
tsv('03_LIVE_J_IDENTITY_AND_COADMINISTRATION.tsv',['source','stage','state','reason','evidence'],[
 {'source':s,'stage':stage,'state':state,'reason':reason,'evidence':evidence}
 for s in ['LiTS_I','WVS7'] for stage,state,reason,evidence in [
 ('L1','PENDING_IDENTITY_AUTHORITY_ACCESS','No exact J01-A specimen row/member order/implementation bindings have been materialized','evidence/J01A_CANDIDATE_LIBRARY_POINTER.csv'),
 ('L2','NOT_EXECUTED__L1_NOT_FROZEN','Physical geometry verified; same-file component presence is not same-respondent/coadministration proof','evidence/'+('LITS_I_METADATA.json' if s=='LiTS_I' else 'WVS7_METADATA.json'))]])
for name,stage in [('04_ROLE_OCCUPANCY_AND_COMPONENT_AUTHORITY.tsv','L3/L4'),('05_LIVE_EMPIRICAL_EXECUTION_LEDGER.tsv','L5'),('06_J2I_M1_ADJUDICATION_LEDGER.tsv','L6'),('07_M2_B5_I4_LIVE_COMPOSITION_LEDGER.tsv','L7')]:
 tsv(name,['source','stage','state','reason','positive_products','automatic_current_selection'],[dict(source=s,stage=stage,state='NOT_EXECUTED__NO_FROZEN_EXACT_SPECIMEN',reason='Upstream identity/selection incomplete; no positive or negative occupancy inferred',positive_products='NONE',automatic_current_selection=False) for s in ['LiTS_I','WVS7']])
tsv('08_TYPED_NEGATIVE_AND_REFUSAL_LEDGER.tsv',['id','scope','state','classification','occupancy_inference','architecture_reopen'],[
 dict(id='ACCESS-J01A',scope='LiTS_I+WVS7',state='EXACT_CANDIDATE_ARTIFACT_NOT_MATERIALIZED',classification='AUTHORITY_ARTIFACT_ACCESS__NOT_NEGATIVE_OCCUPANCY',occupancy_inference='NONE',architecture_reopen=False),
 dict(id='ACCESS-D5',scope='LiTS_I',state='EXACT_J01B_D5_ARCHIVE_NOT_MATERIALIZED',classification='AUTHORITY_ARTIFACT_ACCESS__NOT_NEGATIVE_OCCUPANCY',occupancy_inference='NONE',architecture_reopen=False)])
md('00_RETURN.md','''# HQ124 LiTS I + WVS7 — preparation receipt; commission unfinished

Status: `PENDING_EXACT_CURRENT_J_AUTHORITY_ARTIFACT_ACCESS__NO_LIVE_OCCUPANCY_VERDICT`.

Commission: `c44df7f99fcf86763431ea8c98f74c0245c94670`, branch `agent/rabochii-pyat-hq124-lits1-wvs7-live-j-authority-load-r1`.

Declared intended scope is exactly LiTS I + WVS7, one current J specimen per source initially. No specimen has yet been frozen. No court over the 1,411-candidate estate was executed. No terminal PASS or architecture-reopen token is claimed.

Both supplied source files have the commissioned SHA-256, dimensions and variable counts. Exactly one metadata-only inspection per source has been retained. Zero full source decodes; zero respondent outcome values accessed. The LiTS metadata inspection uses the current decoder's exact-hash latin1 compatibility allowlist without invoking its full-read branch. Encoding compatibility is not semantic authority.

The branch omits the two requisite HQ123 reference files; their exact bytes were recovered from adopted court e7e6fdb25031b8d0ebc1bc8b357460814f385f01 and read. HQD-124 remains the governing architecture theorem.

The J01-A Git CSV is a one-row Library pointer, not the candidate CSV. Its bytes cannot pass the commissioned current carrier hash. Exact LiTS I candidate IDs/member order cannot be lawfully manufactured from aggregate counts, question wording or historical membership. Current J01-B's WVS/EVS D2 crosswalk was recovered and verified; the LiTS/South Asia D5 crosswalk is an exact member of a Library archive unavailable through this session's tools. No Library connector is installed, and local Desktop/Documents/Downloads searches found no materialized copy.

This is an input-access limit on completion, not a negative live result. L1–L7 ledger entries distinguish pending/not-executed from denied/unresolved occupancy. No component vectors, LearnedEmpiricalDisposition, release cores, Field Forge relation objects or lifecycle actions were fabricated.

Resume after materializing the exact authority artifacts listed in 11_NEXT_SCOPE_RECOMMENDATION.md. Hash them, select and freeze one specimen per source from current authority, then run only authorized stages. Typed-negative proving remains valid once a real selected specimen has been adjudicated.
''')
md('09_ARCHITECTURE_REOPEN_OR_NO_REOPEN.md','''# No reopen witness

`SOURCE_FREE_PRE553_ARCHITECTURE_COMPLETE_AT_AUDITED_GRAIN` remains the governing theorem. No live semantic requirement has been executed or shown unrepresentable. Missing Library bytes are not an architecture gap. This receipt makes no new completion proof and no occupancy inference.''')
md('10_FIELD_FORGE_HANDOFF_PACKET_IF_ANY.md','''# No Field Forge handoff

No live M1 disposition or retained B learned product exists in this attempt. No handoff packet is constituted; no Field Forge mutation, publication, lifecycle action, current selection or PRE-V3 permission occurred.''')
md('11_NEXT_SCOPE_RECOMMENDATION.md','''# Resume the same bounded commission

Required exact materialized artifacts:

- `CURRENT_J_CANDIDATE_UNIVERSE_FROZEN.csv`: 1,641,446 bytes, SHA-256 `b21a79947f19f4c520ea493480a38ef8b23cb6797444eeb913bc8575b6cafb64`; Library `libfile_3f6b0d93bb74819195702d808e3093ec`, file `file_000000005144822fa27f7502f6e9307b`.
- `J01B_D5_EXACT_CARRIERS.zip`: 61,875 bytes, SHA-256 `0765b7981fd710b315f8a6439be5a4ca5520c1b5fbd7bc166d72401c72774097`; Library `libfile_64dd382a81148191a7645c98972802f4`, file `file_00000000d19c81f68b3b98a73c0ef4f1`. Its `CURRENT_SUCCESSION_CROSSWALK.csv` member is 154,065 bytes, SHA-256 `2ffd94620212fc00af49c4e775b99a83144b71c72387c1da69d412c7edc7f33a`.

Do not broaden the live scope. Authority-carrier filtering is selection work, not a respondent candidate scan. Prefer exact overlap with the already-qualified selected-B governed projection, then minimal governed component count, then deterministic current ID order. A partial projection overlap does not authorize the full J candidate: selected-B WVS7 binds Q291G5/Q291P5 while current Q291G and Q291P candidate groups have six members each. A pair is not automatically a candidate, and one member is not the full group.

After exact row access, freeze the specimen receipt before any outcome read. Respect all L1–L7 gates. Decode at most once per source; retain intermediate products. A second specimen requires the commission's exact pre-value justification. If identity or role cannot be resolved, adjudicate the actual specimen at that typed grain. Do not promote this preparation/access receipt into a live typed-negative PASS.
''')
md('12_EVIDENCE_MAP.md','''# Evidence map

- `evidence/AUTHORITY_RECOVERY_PROVENANCE.json`: exact commit/path/byte hashes for recovered authoritative inputs.
- `evidence/J01A_CANDIDATE_LIBRARY_POINTER.csv`, `evidence/J01A_RETURN_POINTER.json`: unavailable current row carrier, exact expected identity and storage location.
- `evidence/J01B_GLOBAL_POINTER.json`: adopted virtual-union current contract; D2 and D5 exact carrier bindings.
- `evidence/D2_OBL009_CURRENT_SUCCESSION_CROSSWALK.csv`: byte-verified WVS/EVS lane (authority metadata only; no respondent execution).
- `evidence/J01B_D5_RETURN_POINTER.json`: exact LiTS archive/member identities.
- `evidence/HQ123_08_SOURCE_FREE_VS_LIVE_OCCUPANCY_BOUNDARY.md`, `evidence/HQ123_09_EXACT_REMAINING_GAPS.tsv`: recovered required reading at adopted court commit.
- `evidence/LITS_I_METADATA.json`, `evidence/WVS7_METADATA.json`: current source hashes, physical metadata and reader discipline; no respondent rows.
- `01` through `08`: explicit preparation/pending states; none is a claimed live success.
- `prepare_return.py`: replay of this receipt from retained metadata and pinned Git objects; never reads outcomes.
''')
manifest=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file() and p.name!='EVIDENCE_SHA256.json':manifest.append({'path':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(E/'EVIDENCE_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Preparation banked: exact raw sources verified, 0 specimens frozen, 0 full decodes, no live verdict.')
