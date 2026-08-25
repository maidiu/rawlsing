import pandas as pd, json, hashlib, pathlib, shutil, csv, zipfile, sys
ROOT=pathlib.Path('/mnt/data'); wid=sys.argv[1]
R13BASE=ROOT/'r18a_work'/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R13_20260811'
R12BASE=ROOT/'r18a_r12'; R11BASE=ROOT/'r18a_r11'
R10BASE=next((ROOT/'r18a_r10').glob('Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10_20260811'))
R14ABASE=ROOT/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R14A_20260811'
PACKROOT=ROOT/'Rawlsing_R10K_S14_R15_WORKER_PACKS_20260811'

def jload(x):
 if pd.isna(x) or str(x).strip()=='' or str(x)=='nan': return []
 try:return json.loads(x)
 except:return []
def normrules(s):return [x.replace('S14-','') for x in str(s).split(';') if x and str(x)!='nan']
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def stable(prefix,*parts):return prefix+'-'+hashlib.sha256('|'.join(map(str,parts)).encode()).hexdigest()[:20]
assign=pd.read_csv(R14ABASE/'WORKER_ECONOMICS'/'R14A_WORKER_PACKET_ASSIGNMENT_LEDGER.csv',dtype={'wave':str}); adf=assign[assign.worker_id==wid].copy().sort_values(['source_family','wave','packet_id'])
r13=pd.read_csv(R13BASE/'PACKETS'/'R13_CROSS_RULE_DEDUPED_PACKET_LEDGER.csv',dtype={'wave':str});r13i=r13.set_index('packet_id',drop=False)
r12=pd.read_csv(R12BASE/'PACKETS'/'R12_CANONICAL_COMPRESSED_PACKET_LEDGER.csv',dtype={'wave':str});r12i=r12.set_index('packet_id',drop=False)
cdf=r13[r13.packet_id.isin(set(adf.packet_id))].copy().sort_values(['source_family','wave','packet_id'])
child_ids=[];origins=[];impls=set()
for _,rr in cdf.iterrows(): child_ids+=jload(rr.r12_child_packet_ids_json);origins+=jload(rr.raw_origin_ids_json);impls.update(jload(rr.member_implementation_ids_json))
child_ids=list(dict.fromkeys(child_ids));origins=list(dict.fromkeys(origins)); child=r12[r12.packet_id.isin(child_ids)].copy().sort_values(['source_family','wave','packet_class','packet_id'])
# load only evidence tables and filter quickly
specs=[
 ('R11_SOURCE_NATIVE_OBJECT_OPPORTUNITIES',R11BASE/'SOURCE_OBJECTS'/'R11_SOURCE_NATIVE_OBJECT_OPPORTUNITY_LEDGER.csv'),
 ('R11_SEMANTIC_COLLISION_GROUPS',R11BASE/'SEMANTIC_COLLISIONS'/'R11_DRIVER_DOMAIN_COLLISION_GROUPS.csv'),
 ('R11_T06_SAME_TARGET_SEMANTIC_PAIRS',R11BASE/'T06'/'R11_T06_SAME_TARGET_SEMANTIC_PAIR_OPPORTUNITIES.csv'),
 ('R11_T06_SEMANTIC_X_ENDPOINT_ACCOUNTING',R11BASE/'T06'/'R11_T06_ALL_SEMANTIC_UNITS_X_O04_ENDPOINT_FULL_ACCOUNTING.csv.gz'),
 ('R11_T08_INSTITUTION_CLASS_GROUPS',R11BASE/'T08'/'R11_T08_INSTITUTION_CLASS_GROUP_OPPORTUNITIES.csv'),
 ('R11_T09_T10_PARALLEL_OBJECT_ALIGNMENTS',R11BASE/'T09_T10'/'R11_PARALLEL_SOURCE_OBJECT_EQUAL_SIZE_ALIGNMENT_OPPORTUNITIES.csv'),
 ('R11_T11_SAME_TARGET_MULTIROLE_GROUPS',R11BASE/'T11'/'R11_T11_SAME_TARGET_MULTIROLE_GROUPS.csv')]
origin_set=set(origins); evidence_by_name={};found=set()
for name,p in specs:
 df=pd.read_csv(p,dtype={'wave':str},low_memory=False); sub=df[df.opportunity_id.astype(str).isin(origin_set)].copy()
 if len(sub): evidence_by_name[name]=sub;found.update(sub.opportunity_id.astype(str))
if found!=origin_set: raise SystemExit(f'{wid} origin evidence mismatch missing={len(origin_set-found)}')
spine=pd.read_csv(R10BASE/'SPINE'/'UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10.csv.gz',dtype=str,low_memory=False);ssub=spine[spine.question_implementation_id.isin(impls)].copy().sort_values(['source_family','wave','source_variable_code','question_implementation_id'])
if set(ssub.question_implementation_id)!=impls: raise SystemExit(f'{wid} spine missing')
rules=pd.read_csv(R11BASE/'RULE_RELEASE'/'S14_R11_OPPORTUNITY_RULE_RELEASE.csv',dtype=str);ontology=pd.read_csv(R10BASE/'ONTOLOGY'/'RELATION_ROLE_ONTOLOGY_R10.csv',dtype=str)
canary=pd.read_csv(R11BASE/'CANARY'/'R6_T03_T11_CANARY_RECOVERY_R11.csv',dtype={'wave':str});groups=set(zip(adf.source_family.astype(str),adf.wave.astype(str)));can_sub=canary[[(str(sf),str(w)) in groups for sf,w in zip(canary.source_family,canary.wave)]].copy()
r6x=pd.read_csv(R10BASE/'INDEX'/'R6_RELATION_ACTIVE_WAVE_CROSSWALK_R10.csv',dtype=str);types=['GENERAL_PRINCIPLE_SPECIFIC_APPLICATION','GOAL_MEANS','COMMITMENT_PERSONAL_COST','NORM_EXPECTED_CONDUCT','GENERAL_TARGET_SUBTARGET','INSTITUTION_CLASS_DIFFERENTIATION','RECIPROCAL_ROLE_REVERSAL','TARGET_CONDITION_MATRIX','COMPLEMENTARY_ROLE_CONVERGENCE'];r6x=r6x[r6x.relation_type.isin(types)].copy();r6_members={};r6_rows=[]
for _,rx in r6x.iterrows():
 ms=set();gs=set()
 for m in jload(rx.active_member_crosswalk_json):
  if isinstance(m,dict):
   if m.get('question_implementation_id'):ms.add(m['question_implementation_id'])
   gs.add((str(m.get('active_source_family')),str(m.get('active_wave'))))
 r6_members[rx.relation_authority_id]=ms
 if gs & groups:r6_rows.append(rx)
r6_sub=pd.DataFrame(r6_rows,columns=r6x.columns)
# atoms
atoms=[]
for _,rr in cdf.iterrows():
 cset=set(jload(rr.member_implementation_ids_json));known=sorted([rid for rid,ms in r6_members.items() if ms and ms.issubset(cset)])
 for cid in jload(rr.r12_child_packet_ids_json):
  ch=r12i.loc[cid];ros=jload(ch.raw_origin_ids_json);cls=ch.packet_class;rs=normrules(ch.rule_hypotheses)
  if int(ch.decision_atom_count)==0: specs2=[]
  elif cls in ['SOURCE_NATIVE_OBJECT','SEMANTIC_COLLISION_GROUP']: specs2=[(o,r,'RULE_SPECIFIC') for o in ros for r in rs]
  elif cls=='T09_T10_PARALLEL_SOURCE_OBJECT_COMPONENT':specs2=[(o,'T09;T10','COMPOSITE_T09_T10_CLASSIFICATION') for o in ros]
  elif cls in ['T06_SAME_TARGET_SEMANTIC_HYPEREDGE','T06_NORM_ENDPOINT_LINK_WORKBENCH','T08_INSTITUTION_CLASS_GROUP','T11_SAME_TARGET_MULTIROLE_GROUP']:specs2=[(o,rs[0] if rs else ch.rule_hypotheses,'RULE_SPECIFIC') for o in ros]
  else:raise SystemExit(f'unexpected class {cls}')
  if len(specs2)!=int(ch.decision_atom_count):raise SystemExit(f'{wid} child atom mismatch {cid}')
  for oid,rule_scope,kind in specs2:
   atoms.append({'worker_id':wid,'decision_atom_id':stable('R15ATOM',wid,rr.packet_id,cid,oid,rule_scope),'r13_packet_id':rr.packet_id,'r12_child_packet_id':cid,'packet_class':cls,'source_family':rr.source_family,'wave':rr.wave,'raw_origin_id':oid,'rule_scope':rule_scope,'decision_atom_kind':kind,'r13_member_implementation_ids_json':rr.member_implementation_ids_json,'r13_member_semantic_unit_ids_json':rr.member_semantic_unit_ids_json,'known_r6_relation_ids_fully_contained_json':json.dumps(known),'worker_recommendation':'','proposed_relation_objects_json':'','authorized_member_implementation_ids_json':'','rejected_member_implementation_ids_json':'','relation_role_structure':'','decisive_rationale':'','evidence_refs_json':'','routing_or_composability_note':'','blocker_reason':'','confidence':'','worker_notes':''})
atom=pd.DataFrame(atoms);expected=int(adf.decision_atom_count.sum())
if len(atom)!=expected:raise SystemExit(f'{wid} atom total {len(atom)} != {expected}')
# R8 ancestry
r8map=pd.read_csv(R12BASE/'ANCESTRY'/'R8_89_PACKET_TO_R12_COMPRESSION_CROSSWALK.csv',dtype=str);r8c=pd.read_csv(R12BASE/'ANCESTRY'/'R8C_33_RULE_VERDICTS_TO_R12_PACKETS.csv',dtype=str);childset=set(child_ids);intersects=lambda s:bool(childset&set(jload(s)));r8sub=r8map[r8map.r12_candidate_packet_ids_json.map(intersects)].copy();r8csub=r8c[r8c.r12_candidate_packet_ids_json.map(intersects)].copy()
# overlaps
xov=[]
for _,cr in cdf.iterrows():
 cset=set(jload(cr.member_implementation_ids_json))
 for _,rx in r6_sub.iterrows():
  ms=r6_members.get(rx.relation_authority_id,set()); inter=cset&ms
  if inter:xov.append({'r13_packet_id':cr.packet_id,'relation_authority_id':rx.relation_authority_id,'relation_type':rx.relation_type,'r6_member_count':len(ms),'container_overlap_count':len(inter),'container_contains_all_r6_members':ms.issubset(cset),'overlap_implementation_ids_json':json.dumps(sorted(inter))})
xov=pd.DataFrame(xov)
# write pack
W=PACKROOT/wid
if W.exists():shutil.rmtree(W)
for d in ['ASSIGNMENT','WORKBENCH','EVIDENCE','CONTRACTS','ANCESTRY','RETURN','VALIDATION']:(W/d).mkdir(parents=True,exist_ok=True)
adf.to_csv(W/'ASSIGNMENT'/'FROZEN_R14A_ASSIGNMENT.csv',index=False);cdf.to_csv(W/'ASSIGNMENT'/'R13_REVIEW_CONTAINERS.csv',index=False);child.to_csv(W/'EVIDENCE'/'R12_CHILD_PACKET_LEDGER.csv',index=False);atom.to_csv(W/'WORKBENCH'/'DECISION_ATOM_WORKBENCH.csv',index=False);atom.to_csv(W/'RETURN'/'WORKER_RETURN_TEMPLATE.csv',index=False);ssub.to_csv(W/'EVIDENCE'/'R10_SPINE_MEMBER_ROWS.csv.gz',index=False,compression='gzip')
for name,sub in evidence_by_name.items():sub.to_csv(W/'EVIDENCE'/f'{name}.csv.gz',index=False,compression='gzip')
can_sub.to_csv(W/'EVIDENCE'/'R6_T03_T11_CANARIES_IN_SOURCE_WAVES.csv',index=False);r6_sub.to_csv(W/'EVIDENCE'/'R6_ACTIVE_RELATION_CROSSWALK_IN_SOURCE_WAVES.csv',index=False);xov.to_csv(W/'EVIDENCE'/'R6_CONTAINER_OVERLAP.csv',index=False);r8sub.to_csv(W/'ANCESTRY'/'R8_PACKET_ANCESTRY_IN_SCOPE.csv',index=False);r8csub.to_csv(W/'ANCESTRY'/'R8C_PRIOR_VERDICTS_IN_SCOPE.csv',index=False);rules.to_csv(W/'CONTRACTS'/'S14_R11_OPPORTUNITY_RULE_RELEASE.csv',index=False);ontology.to_csv(W/'CONTRACTS'/'RELATION_ROLE_ONTOLOGY_R10.csv',index=False)
groups_txt=', '.join([f'{sf} {wv}' for sf,wv in sorted(groups)])
(W/'00_README_FIRST.md').write_text(f'''# {wid} — S14 R15 Successor Execution Pack\n\nImmutable assignment: **{len(adf):,} R13 containers / {expected:,} decision atoms** across {groups_txt}. R8 worker packs are superseded/DO NOT EXECUTE. Job 3 is not authorized.\n\nWork only `WORKBENCH/DECISION_ATOM_WORKBENCH.csv`; return every row exactly once in `RETURN/WORKER_RETURN_TEMPLATE.csv`. Use exact R10 spine rows and the R11 evidence row matching each `raw_origin_id`. R8C is provisional ancestry to revalidate.\n\nHard laws: T03 explicit principle→application; T04 explicit goal/end→means for same end; T05 explicit commitment→explicit personal cost tied to same commitment; T06 norm↔conduct with actor/target/action alignment and no stated→observed promotion; T08 class mapping is prerequisite not relation; T09 explicit directional reciprocal roles; T10 genuine crossed target×condition matrix; T11 distinct authorized roles converging on one narrow proposition. **T07 is not worker scope.**\n\nSemantic-act role, driver/facet/domain, lexical similarity, embeddings, source proximity/co-membership, and association are recall/context only and **never authorize** a relation.\n\n`worker_recommendation` enum: `WORKER_RECOMMEND_ACCEPT`, `WORKER_RECOMMEND_PARTIAL_ACCEPT`, `WORKER_RECOMMEND_REJECT`, `WORKER_RETAIN_EXISTING_GOVERNED_AUTHORITY`, `WORKER_BLOCKED_NEEDS_VOZHD`. Accepts must provide `proposed_relation_objects_json` with exact relation type, member implementation IDs, member roles, and narrow proposition/end/target/matrix identity. Do not widen packet membership or manufacture arbitrary subsets.\n\nDo not repair pair authority, norm-role authority, T07 hierarchy, ontology, or evidence ceilings; do not assert completeness, freeze S14, join respondents, infer personality/causality, or authorize Job 3. If evidence is insufficient or a canary seems contradicted, block and escalate.\n''')
(W/'CONTRACTS'/'WORKER_RETURN_CONTRACT.md').write_text('# Worker return contract\n\nEvery row is a recommendation only. Preserve IDs. Block rather than invent closure.\n');(W/'RETURN'/'WORKER_COMPLETION_REPORT_TEMPLATE.md').write_text(f'# {wid} completion report\n\nAssigned containers: {len(adf)}\nAssigned decision atoms: {expected}\nReturned: \nAccept: \nPartial accept: \nReject: \nRetain existing: \nBlocked: \n\n## Blocked atoms\n')
scope={'worker_id':wid,'source_wave_groups':sorted([{'source_family':sf,'wave':wv} for sf,wv in groups],key=lambda x:(x['source_family'],x['wave'])),'assigned_container_count':len(adf),'assigned_decision_atom_count':expected,'r12_child_packet_count':len(child_ids),'raw_origin_count':len(origins),'spine_member_implementation_count':len(impls),'known_r6_canary_count_in_source_waves':len(can_sub),'r8_ancestry_rows':len(r8sub),'r8c_prior_verdict_rows':len(r8csub),'job3_authorized':False};json.dump(scope,open(W/'GOVERNING_SCOPE.json','w'),indent=2)
checks=[]
def ck(n,c,d=None):checks.append({'check':n,'pass':bool(c),'detail':d})
ck('assignment_count',len(adf)==scope['assigned_container_count']);ck('r13_exact',set(cdf.packet_id)==set(adf.packet_id));ck('atoms',len(atom)==expected);ck('atom_unique',atom.decision_atom_id.nunique()==len(atom));ck('origins',set(atom.raw_origin_id)==set(origins));ck('evidence',found==set(origins));ck('spine',set(ssub.question_implementation_id)==impls);ck('no_t07',not(child.packet_class=='T07_P2_TARGET_RELATION_CONCEPT').any());ck('no_pair_blocker',not(child.packet_class=='PAIR_RULE_INPUT_AUTHORITY_BLOCKER').any());ck('no_norm_blocker',not(child.packet_class=='T06_NORM_ROLE_ASSIGNMENT_BLOCKER_WORKBENCH').any());ck('positive_atoms',(cdf.decision_atom_count>0).all());ck('job3_false',scope['job3_authorized'] is False);v={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','check_count':len(checks),'errors':[x for x in checks if not x['pass']],'checks':checks};json.dump(v,open(W/'VALIDATION'/'PACK_SELF_VALIDATION.json','w'),indent=2)
if v['status']!='PASS':raise SystemExit(v)
with open(W/'SHA256_MANIFEST.csv','w',newline='') as f:
 wr=csv.writer(f);wr.writerow(['relative_path','sha256','size_bytes'])
 for p in sorted([p for p in W.rglob('*') if p.is_file() and p.name!='SHA256_MANIFEST.csv']):wr.writerow([p.relative_to(W).as_posix(),sha(p),p.stat().st_size])
zpath=ROOT/f'Rawlsing_R10K_S14_R15_{wid}_Execution_Pack_20260811.zip';
if zpath.exists():zpath.unlink()
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,allowZip64=True) as z:
 for p in sorted(W.rglob('*')):
  if p.is_file():z.write(p,arcname=f'{wid}/{p.relative_to(W).as_posix()}')
zsha=sha(zpath);pathlib.Path(str(zpath)+'.sha256').write_text(f'{zsha}  {zpath.name}\n')
print(json.dumps({'worker':wid,'containers':len(adf),'atoms':expected,'origins':len(origins),'impls':len(impls),'zip':str(zpath),'sha256':zsha,'size':zpath.stat().st_size},indent=2))
