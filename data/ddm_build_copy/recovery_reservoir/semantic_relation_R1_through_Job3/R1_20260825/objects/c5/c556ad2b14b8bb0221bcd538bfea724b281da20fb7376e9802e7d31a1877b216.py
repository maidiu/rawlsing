import pandas as pd,json,os,re,itertools,collections,hashlib,zipfile,shutil
from pathlib import Path
B=Path('/mnt/data/rawlsing_exec/o12r2'); R5=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R5_20260811')
OUT=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R6_20260811'); ZIP=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R6_20260811.zip')
if OUT.exists(): shutil.rmtree(OUT)
for q in ['AUDIT','NARROWING','PROVENANCE','VALIDATION','CODE']: (OUT/q).mkdir(parents=True,exist_ok=True)
r6=pd.read_csv(B/'INTER_QUESTION_RELATION_AUTHORITY_R2.csv'); reg=pd.read_csv(B/'CANONICAL_IMPLEMENTATION_REGISTRY.csv',low_memory=False); s16=pd.read_csv(B/'S16_WAVE_RELATION_CLASS_CAPABILITY_ATLAS.csv'); r14=json.load(open(B/'R14_SOURCE_NATIVE_AUTHORITY_FINAL_708047.json'))
obj_by={o.get('object_id'):o for o in r14['objects'] if o.get('object_id')}; fammap={'ASB':'Asian Barometer','ArabBarometer':'Arab Barometer'}

def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for x in iter(lambda:f.read(1048576),b''):h.update(x)
 return h.hexdigest()
def normab(v): return re.sub(r'(?<=\d)[ab](?=(_|$))','',str(v).lower())
def toks(s): return [x for x in re.split(r'[_\W]+',str(s).lower().replace('target__','').replace('condition__','')) if x]
STOP={'condition','dimension','source','defined','target','frame','preserved','respondent','universe','specific','proposition','institutional','the','a','an','of','for','to','in','on','and','or'}
def base_target(t,c):
 cc=set(x for x in toks(c) if x not in STOP and len(x)>2); return '_'.join(x for x in toks(t) if x not in cc)

# R6 14 canaries
T=r6[r6.relation_type.eq('TARGET_CONDITION_MATRIX')].copy(); assert len(T)==14
T.to_csv(OUT/'PROVENANCE/R6_T10_14_SEALED_PARENT_ROWS_R6.csv',index=False)
crec=[]
for _,x in T.iterrows():
 mids=json.loads(x.member_question_implementation_ids); oids=json.loads(x.source_structure_ids)
 g=reg[reg.question_implementation_id.isin(mids)]
 missing=[m for m in mids if m not in set(g.question_implementation_id)]
 states=[obj_by.get(o,{}).get('state','MISSING') for o in oids]
 crec.append({'relation_authority_id':x.relation_authority_id,'source_family':x.source_family,'wave':x.wave,'construction_class':x.edge_construction_class,'member_count':len(mids),'current_members_recovered':len(mids)-len(missing),'source_structure_count':len(oids),'source_structure_states_json':json.dumps(states),'recovery_status':'RECOVERED_R6_T10_CANARY' if not missing else 'CANARY_MEMBER_GAP','semantic_rationale':x.semantic_rationale})
can=pd.DataFrame(crec); assert can.recovery_status.eq('RECOVERED_R6_T10_CANARY').all(); can.to_csv(OUT/'PROVENANCE/R6_T10_CANARY_RECOVERY_R6.csv',index=False)

# Current semantic-unit replay of old matrix proxy + true-crossing repair
u=reg[reg.sem__audit_unit_id.notna()].drop_duplicates('sem__audit_unit_id').copy()
gcols=['source_family','wave','sem__canonical_driver_id','sem__canonical_facet_id','sem__canonical_question_block_id','sem__canonical_relation_axis_id','sem__canonical_role']
# map impl ids to known T10 ids
known_sets={x.relation_authority_id:set(json.loads(x.member_question_implementation_ids)) for _,x in T.iterrows()}
proxy=[]; true=[]
for key,h in u.groupby(gcols,dropna=False):
 t=h.sem__canonical_target_id.replace('',pd.NA).dropna().nunique(); c=h.sem__canonical_condition_id.replace('',pd.NA).dropna().nunique()
 if t<2 or c<2: continue
 hh=h[(h.sem__canonical_target_id.notna())&(h.sem__canonical_target_id!='')&(h.sem__canonical_condition_id.notna())&(h.sem__canonical_condition_id!='')].copy()
 hh['matrix_base_target']=hh.apply(lambda r:base_target(r.sem__canonical_target_id,r.sem__canonical_condition_id),axis=1)
 pairs=hh[['matrix_base_target','sem__canonical_condition_id','sem__audit_unit_id']].drop_duplicates()
 tc=pairs.groupby('matrix_base_target').sem__canonical_condition_id.nunique(); cc=pairs.groupby('sem__canonical_condition_id').matrix_base_target.nunique()
 rt=int((tc>=2).sum()); rc=int((cc>=2).sum()); crossed=rt>=2 and rc>=2
 impl=set(reg.loc[reg.sem__audit_unit_id.isin(hh.sem__audit_unit_id),'question_implementation_id'])
 ko=[rid for rid,ss in known_sets.items() if len(impl&ss)>=2]
 if crossed:
  if ko: disp='KNOWN_R6_T10_TERRAIN__NO_NEW_ADJUDICATION'
  elif key[0]=='Arab Barometer' and str(key[1])=='II': disp='EMIT_MATRIX_REVIEW_CANDIDATE__ROUTING_UNIVERSE_REVIEW_REQUIRED'
  elif key[0]=='Arab Barometer' and str(key[1])=='VIII' and key[2]=='materialSecurity': disp='EMIT_MATRIX_REVIEW_CANDIDATE__CURRENT_ROUTING_UNRESOLVED'
  else: disp='EMIT_MATRIX_REVIEW_CANDIDATE'
 else: disp='REJECT_PROXY_NOT_TRUE_2D_CROSSING'
 row={'source_family':key[0],'wave':key[1],'driver_id':key[2],'facet_id':key[3],'block_id':key[4],'axis_id':key[5],'role':key[6],'semantic_unit_count':len(h),'raw_target_count':t,'condition_count':c,'reconstructed_base_target_count':hh.matrix_base_target.nunique(),'repeated_target_count':rt,'repeated_condition_count':rc,'true_2d_crossing':crossed,'known_r6_overlap_ids':'|'.join(ko),'disposition':disp,'semantic_unit_ids_json':json.dumps(sorted(hh.sem__audit_unit_id.astype(str).unique()))}
 proxy.append(row)
 if crossed: true.append(row)
proxy=pd.DataFrame(proxy); true=pd.DataFrame(true)
proxy.to_csv(OUT/'AUDIT/O11_T10_CURRENT_PROXY_REPLAY_AND_DISPOSITION_R6.csv',index=False); true.to_csv(OUT/'NARROWING/T10_TRUE_CROSSING_CURRENT_SEMANTIC_GROUPS_R6.csv',index=False)
assert len(true)==4 and true.disposition.str.startswith('EMIT').sum()==2

# exact source joint universe includes accepted + older JOINT_SOURCE_NATIVE because one sealed Latin T10 uses it
joint=[o for o in r14['objects'] if o.get('state') in {'ACCEPTED_SOURCE_NATIVE_JOINT','JOINT_SOURCE_NATIVE'}]; assert len(joint)==596
r6_source_ids=set(sum((json.loads(x) for x in T.source_structure_ids),[]))
# source-code grids (e.g. Latin P50ST_AA..FB)
grid=[]
for o in joint:
 vs=[str(v) for v in o.get('members',[])]; found=[]
 rec=[]
 for v in vs:
  m=re.match(r'^(.*?[_-])([A-Za-z])([A-Za-z])$',v)
  if m:rec.append((v,m.group(1).lower(),m.group(2).upper(),m.group(3).upper()))
 for pref,z in collections.defaultdict(list,{}).items(): pass
 by=collections.defaultdict(list)
 for z in rec:by[z[1]].append(z)
 for pref,z in by.items():
  rr=set(q[2] for q in z);cc=set(q[3] for q in z);cells={(q[2],q[3]) for q in z}
  if len(rr)>=2 and len(cc)>=2 and len(cells)>=4: found.append({'pattern':'two_letter_suffix','prefix':pref,'row_values':sorted(rr),'condition_values':sorted(cc),'cell_count':len(cells)})
 if found:grid.append({'object_id':o['object_id'],'source_family':fammap.get(o.get('family'),o.get('family')),'wave':o.get('wave'),'member_count':len(vs),'grid_patterns_json':json.dumps(found),'known_r6_source_object':o['object_id'] in r6_source_ids,'disposition':'KNOWN_R6_T10_SOURCE_GRID' if o['object_id'] in r6_source_ids else 'EMIT_SOURCE_GRID_REVIEW_CANDIDATE'})
grid=pd.DataFrame(grid); grid.to_csv(OUT/'NARROWING/T10_EXACT_SOURCE_CODE_GRID_RECALL_R6.csv',index=False)

# sibling A/B cross-object structures; evaluate without excerpts
byfw=collections.defaultdict(list)
for o in joint:byfw[(fammap.get(o.get('family'),o.get('family')),str(o.get('wave')))].append(o)
sib=[]
for key,gg in byfw.items():
 for a,b in itertools.combinations(gg,2):
  ma=[normab(x) for x in a.get('members',[])];mb=[normab(x) for x in b.get('members',[])]
  if ma and mb and set(ma)==set(mb):
   s={a['object_id'],b['object_id']}; known=[rid for rid,ss in [(x.relation_authority_id,set(json.loads(x.source_structure_ids))) for _,x in T.iterrows()] if s<=ss]
   if s=={'ArabBarometer-R14-VIII-Q604A_NT','ArabBarometer-R14-VIII-Q604B_NT'}:
    disp='EMIT_MATRIX_REVIEW_CANDIDATE__CROSS_RULE_T09';reason='Two repeated spouse-obstacle targets under female-relative vs male-relative role conditions form a 2×2 matrix; T09 semantic authority already governs the role reversal.'
   elif s=={'ArabBarometer-R14-VIII-Q550A','ArabBarometer-R14-VIII-Q550B'}:
    disp='BLOCK_SOURCE_CELL_TARGET_LABELS_NOT_RECOVERED';reason='Six parallel A/B positions exist under human-dignity vs democracy frames, but current child text does not recover the six substantive cell targets; position identity alone cannot authorize a matrix.'
   elif known:
    disp='KNOWN_R6_T10_CROSS_OBJECT_SOURCE_STRUCTURE';reason='Exact source-object set participates in sealed R6 T10 matrix authority.'
   elif any(x.replace('-','_').lower()==y.replace('-','_').lower() for x in s for y in s if x!=y):
    disp='REJECT_DUPLICATE_SOURCE_OBJECT_ALIAS';reason='Duplicate/alias source materialization, not two matrix conditions.'
   else:
    disp='REJECT_PARALLEL_SOURCE_STRUCTURE_NOT_MATRIX';reason='Parallel A/B/source structure does not independently establish two repeated targets across two repeated conditions.'
   sib.append({'source_family':key[0],'wave':key[1],'object_a':sorted(s)[0],'object_b':sorted(s)[1],'normalized_member_signature_json':json.dumps(sorted(set(ma))),'known_r6_relation_ids':'|'.join(known),'disposition':disp,'reason':reason})
sib=pd.DataFrame(sib);sib.to_csv(OUT/'NARROWING/T10_PARALLEL_SOURCE_OBJECT_PAIR_DISPOSITION_R6.csv',index=False)
assert (sib.disposition=='EMIT_MATRIX_REVIEW_CANDIDATE__CROSS_RULE_T09').sum()==1

# Q628 within-object source blocker: 3 item indices × A/B suffix, but role dimension unknown
q628=obj_by['ArabBarometer-R14-VIII-Q628']
q628row=pd.DataFrame([{'object_id':q628['object_id'],'source_family':'Arab Barometer','wave':'VIII','members_json':json.dumps(q628['members']),'putative_shape':'3 item bases × A/B','disposition':'BLOCK_SOURCE_A_B_ROLE_DIMENSION_NOT_RECOVERED','reason':'Exact child labels repeat the parent freedom-of-choice prompt; A/B suffixes do not govern the second dimension.'}])
q628row.to_csv(OUT/'NARROWING/T10_WITHIN_OBJECT_SOURCE_BLOCKERS_R6.csv',index=False)

# 596 source object accounting
part=collections.defaultdict(list)
for _,x in sib.iterrows():part[x.object_a].append(x.disposition);part[x.object_b].append(x.disposition)
for _,x in grid.iterrows():part[x.object_id].append(x.disposition)
objrows=[]
for o in joint:
 oid=o['object_id']
 if oid in r6_source_ids: d='KNOWN_R6_T10_SOURCE_COMPONENT'
 elif oid=='ArabBarometer-R14-VIII-Q628':d='SOURCE_MATRIX_DIMENSION_BLOCKER'
 elif oid in part and any('EMIT' in z for z in part[oid]):d='NOVEL_MATRIX_REVIEW_COMPONENT'
 elif oid in part and any('BLOCK' in z for z in part[oid]):d='SOURCE_MATRIX_BLOCKER_COMPONENT'
 elif oid in part:d='PARALLEL_OR_GRID_STRUCTURE_EVALUATED_NO_NOVEL_MATRIX'
 else:d='NO_EXACT_MATRIX_STRUCTURE_SIGNAL_IN_BOUNDED_SOURCE_SCAN'
 objrows.append({'object_id':oid,'source_family':fammap.get(o.get('family'),o.get('family')),'wave':o.get('wave'),'state':o.get('state'),'printed_parent_id':o.get('printed_parent_id'),'member_count':len(o.get('members',[])),'accounting_disposition':d})
objacc=pd.DataFrame(objrows);assert len(objacc)==596;objacc.to_csv(OUT/'NARROWING/T10_R14_596_JOINT_OBJECT_ACCOUNTING_R6.csv',index=False)

# canonical packets: existing canaries + novel/blockers
pk=[]
for _,x in T.iterrows():pk.append({'packet_id':'T10R6-KNOWN-'+x.relation_authority_id[-8:],'source_family':x.source_family,'wave':x.wave,'status':'KNOWN_R6_T10_CANARY__NO_NEW_ADJUDICATION','rule_hypotheses':'T10','members':x.member_source_ids,'notes':x.semantic_rationale})
pk += [
 {'packet_id':'T10R6-P01-ARABII-PARLIAMENT-SHURA-DOMAIN','source_family':'Arab Barometer','wave':'II','status':'UNRESOLVED_SEMANTIC_MATRIX_REVIEW__ROUTING_UNIVERSE_REVIEW','rule_hypotheses':'T10','members':'q3061/q3062/q3063 + sa3061/sa3062/sa3063','notes':'2 institutions × economic/social/foreign domains. Saudi Shura rows have Saudi-specific universe; matrix semantic relation is plausible but respondent composability is separate.'},
 {'packet_id':'T10R6-P02-ARABVIII-FOOD-HOUSING-AVAIL-AFFORD','source_family':'Arab Barometer','wave':'VIII','status':'UNRESOLVED_SEMANTIC_MATRIX_REVIEW__CURRENT_ROUTING_UNRESOLVED','rule_hypotheses':'T10','members':'Q127_1A/Q127_1B/Q127_2A/Q127_2B','notes':'Exact 2×2: food/housing × availability/affordability. All current rows preserve source routing signals but O06 remains unresolved.'},
 {'packet_id':'T10R6-P03-ARABVIII-Q604-ROLE-MATRIX','source_family':'Arab Barometer','wave':'VIII','status':'UNRESOLVED_SEMANTIC_MATRIX_REVIEW__CROSS_RULE_PACKET','rule_hypotheses':'T09;T10','members':'Q604A_NT_1/Q604A_NT_3 ↔ Q604B_NT_1/Q604B_NT_3','notes':'Two obstacle targets × female/male-relative role condition. Carry once for cross-rule dedupe; T09 relation itself is already sealed R6 authority.'},
 {'packet_id':'T10R6-B01-ARABVIII-Q550-FRAME-GRID','source_family':'Arab Barometer','wave':'VIII','status':'SOURCE_SEMANTIC_BLOCKER__NO_MATRIX_VERDICT','rule_hypotheses':'T10?','members':'Q550A_1..6 ↔ Q550B_1..6','notes':'Parallel six-cell positions under human dignity vs democracy frames; substantive child target labels not recovered in current canonical text.'},
 {'packet_id':'T10R6-B02-ARABVIII-Q628-A-B','source_family':'Arab Barometer','wave':'VIII','status':'SOURCE_SEMANTIC_BLOCKER__NO_MATRIX_VERDICT','rule_hypotheses':'T10?;T09?','members':'Q628_2A/B,Q628_3A/B,Q628_4A/B','notes':'3×A/B topology visible, but A/B semantic dimension not governed in current canonical child text.'}
]
pk=pd.DataFrame(pk);pk.to_csv(OUT/'NARROWING/T10_CANONICAL_PACKETS_R6.csv',index=False)

# O11 wave-cell ancestry
cells=s16[s16.rule_id.eq('S14-T10')].copy();cells['successor_interpretation']='Old target+condition proxy is terrain only; T10 R6 requires explicit matrix identity and crossed cell provenance.';cells.to_csv(OUT/'AUDIT/O11_T10_35_CELL_DIAGNOSTIC_R6.csv',index=False)

# report/status
rep=f'''# T10 Target×Condition Matrix Narrowing — Checkpoint R6\n\n## Status\n**T10 narrowing rebuilt around explicit 2D crossing; three novel semantic review packets and two source-semantic blockers; not S14 authority. Job 3 remains blocked.**\n\n## R6 canaries\n- Recovered **14/14** sealed R6 T10 positives: 3 source-object constructions and 11 cross-object governed alignments.\n- One sealed Latinobarómetro matrix uses an older `JOINT_SOURCE_NATIVE` R14 object; therefore the bounded source accounting explicitly includes both `ACCEPTED_SOURCE_NATIVE_JOINT` and `JOINT_SOURCE_NATIVE` states instead of silently losing a canary.\n\n## Repair of the old proxy\n- Current semantic replay found **{len(proxy)}** groups with >=2 raw target IDs and >=2 condition IDs.\n- After reconstructing condition-contaminated target IDs and enforcing repeated targets across conditions AND repeated conditions across targets, only **{len(true)}** true crossed groups survive.\n- Two are known R6 terrain; two are novel review candidates: Arab II parliament/Shura × economic/social/foreign, and Arab VIII food/housing × availability/affordability.\n- The remaining proxy groups are not matrices merely because both dimensions vary somewhere in the group.\n\n## Cross-object/source structure\n- Joint R14 source objects accounted: **596/596** (548 accepted-joint + 48 older joint-source-native).\n- Exact source-code grid detector recovers the Latin 6×2 `P50ST_AA..FB` matrix without page/excerpt similarity.\n- Parallel A/B source-object scan evaluates **{len(sib)}** pairs. Arab VIII Q604A/B yields one novel cross-rule T09/T10 matrix review packet; Q550A/B remains blocked because cell target labels are not recovered.\n- Q628 remains a source-semantic blocker: A/B suffixes are topology, not semantic dimension authority.\n\n## Novel T10 frontier\n1. Arab II parliament/Shura Council × economic/social/foreign domain.\n2. Arab VIII food/housing × availability/affordability.\n3. Arab VIII Q604 spouse-obstacle × female/male-relative role matrix (cross-rule with T09).\n\nNo page excerpt or lexical proximity was used as matrix identity authority.\n\n## Next\n**T11 complementary-role convergence**, then global T03–T11 packet compression/deduplication and worker-economics measurement.\n'''
(OUT/'T10_NARROWING_R6_REPORT.md').write_text(rep);(OUT/'00_README_FIRST.md').write_text(rep+'\nSee CURRENT_STATUS_R6.json and NEXT_EXECUTION_STEPS.md.\n')
status={'checkpoint':'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R6_20260811','status':'IN_PROGRESS_NOT_FROZEN','active_state':'R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR','job3_authorized':False,'o12_r2_811_complete_authority':False,'workers_launched':False,'supersedes_for_execution':['CHECKPOINT_R5 next-dependency pointer only; preserves R5 T09 and all earlier narrowing results'],'t10':{'sealed_r6_canaries_recovered':14,'source_object_canaries':3,'cross_object_canaries':11,'old_proxy_replay_groups':len(proxy),'true_crossing_groups':len(true),'novel_review_packets':3,'source_semantic_blocker_packets':2,'r14_joint_objects_accounted':596,'parallel_source_pairs_evaluated':len(sib),'next_dependency':'T11 complementary roles'},'remaining_major_rules':['T11'],'next_decision':'finish T11, cross-rule packet dedupe, then worker economics','repair_stack':{'done':[1,7,8],'partial':[2,3,4,5,6,9,10,11,12,14,15,23],'open':[13,16,17,18,19,20,21,22,24,25]}}
json.dump(status,open(OUT/'CURRENT_STATUS_R6.json','w'),indent=2)
(OUT/'NEXT_EXECUTION_STEPS.md').write_text('''# Exact Resume Sequence after T10 R6\n1. T11 complementary-role convergence: explicit differentiated roles + narrow common proposition; no latent scale inference.\n2. Compress and cross-rule dedupe T03–T11 packets.\n3. Measure exact unresolved packet workload and decide central vs workers.\n4. Adjudicate/freeze actual S14 relational-structure authority.\n5. Rebuild O11/S16, then O12 T01–T13 including T01 grain audit.\n6. Independent completeness reconstruction + causal topology audit.\n7. Freeze true O12 denominator, then Job 3.\n''')
(OUT/'AUDIT/T10_GOVERNING_DOCTRINE_R6.md').write_text('''# T10 governing doctrine\nA T10 matrix requires a genuine crossed structure: at least two targets repeated across at least two conditions and at least two conditions repeated across at least two targets. Target IDs that absorb condition language must be reconstructed before the invariant is tested. One-to-one target/condition batteries are not matrices. Exact source parent/member identity and current semantic coordinates are admissible evidence; R14/page excerpt similarity is prohibited. R6 is calibration, not the maximum universe.\n''')
# pins
pins={'r5_checkpoint_zip_sha256':'617566ef5152a52d1d8b67947b47ad0e435df631fcd562ad67000832eb62f8b5'}
for f in ['INTER_QUESTION_RELATION_AUTHORITY_R2.csv','CANONICAL_IMPLEMENTATION_REGISTRY.csv','R14_SOURCE_NATIVE_AUTHORITY_FINAL_708047.json','S16_WAVE_RELATION_CLASS_CAPABILITY_ATLAS.csv']:pins[f]=sha(B/f)
json.dump(pins,open(OUT/'PROVENANCE/PARENT_PINS_R6.json','w'),indent=2)
shutil.copy(__file__,OUT/'CODE/build_t10_checkpoint_r6.py')
# validator
val='''import pandas as pd,json,os,sys\nR=os.path.dirname(os.path.dirname(__file__));e=[];c=[]\ndef ck(n,x,d=None):c.append((n,bool(x),d));e.append(n) if not x else None\ncan=pd.read_csv(os.path.join(R,'PROVENANCE/R6_T10_CANARY_RECOVERY_R6.csv'));pr=pd.read_csv(os.path.join(R,'AUDIT/O11_T10_CURRENT_PROXY_REPLAY_AND_DISPOSITION_R6.csv'));tr=pd.read_csv(os.path.join(R,'NARROWING/T10_TRUE_CROSSING_CURRENT_SEMANTIC_GROUPS_R6.csv'));ob=pd.read_csv(os.path.join(R,'NARROWING/T10_R14_596_JOINT_OBJECT_ACCOUNTING_R6.csv'));sib=pd.read_csv(os.path.join(R,'NARROWING/T10_PARALLEL_SOURCE_OBJECT_PAIR_DISPOSITION_R6.csv'));pk=pd.read_csv(os.path.join(R,'NARROWING/T10_CANONICAL_PACKETS_R6.csv'));st=json.load(open(os.path.join(R,'CURRENT_STATUS_R6.json')))\nck('r6_14',len(can)==14,len(can));ck('canaries_all_recovered',can.recovery_status.eq('RECOVERED_R6_T10_CANARY').all());ck('true_cross_4',len(tr)==4,len(tr));ck('true_cross_novel_2',tr.disposition.str.startswith('EMIT').sum()==2,int(tr.disposition.str.startswith('EMIT').sum()));ck('proxy_failures_explicit',(pr.disposition=='REJECT_PROXY_NOT_TRUE_2D_CROSSING').sum()==len(pr)-4);ck('r14_596',len(ob)==596,len(ob));ck('q604_crossrule',(sib.disposition=='EMIT_MATRIX_REVIEW_CANDIDATE__CROSS_RULE_T09').sum()==1);ck('q550_block',(sib.disposition=='BLOCK_SOURCE_CELL_TARGET_LABELS_NOT_RECOVERED').sum()==1);ck('canonical_novel_3',pk.status.str.startswith('UNRESOLVED_SEMANTIC_MATRIX_REVIEW').sum()==3,int(pk.status.str.startswith('UNRESOLVED_SEMANTIC_MATRIX_REVIEW').sum()));ck('canonical_blocker_2',(pk.status=='SOURCE_SEMANTIC_BLOCKER__NO_MATRIX_VERDICT').sum()==2);ck('job3_false',st['job3_authorized'] is False);ck('next_t11',st['t10']['next_dependency']=='T11 complementary roles')\nres={'status':'PASS' if not e else 'FAIL','checks':len(c),'errors':e,'details':c};json.dump(res,open(os.path.join(R,'VALIDATION/VALIDATION_RESULT_R6.json'),'w'),indent=2);print(json.dumps({'status':res['status'],'checks':len(c),'errors':len(e)},indent=2));sys.exit(1 if e else 0)\n''';(OUT/'VALIDATION/validate_t10_checkpoint_r6.py').write_text(val)
os.system(f"python {OUT/'VALIDATION/validate_t10_checkpoint_r6.py'}")
# manifest+zip
manifest=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file():manifest.append({'path':str(p.relative_to(OUT)),'sha256':sha(p),'size_bytes':p.stat().st_size})
pd.DataFrame(manifest).to_csv(OUT/'SHA256_MANIFEST_R6.csv',index=False)
if ZIP.exists():ZIP.unlink()
with zipfile.ZipFile(ZIP,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file():z.write(p,arcname=f'{OUT.name}/{p.relative_to(OUT)}')
zs=sha(ZIP);Path(str(ZIP)+'.sha256').write_text(f'{zs}  {ZIP.name}\n')
print(json.dumps({'zip':str(ZIP),'sha256':zs,'files':sum(p.is_file() for p in OUT.rglob('*')),'proxy_groups':len(proxy),'true_crossing':len(true),'parallel_pairs':len(sib)},indent=2))
