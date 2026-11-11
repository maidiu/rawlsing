import pandas as pd, json, re, os, hashlib, zipfile, shutil, collections
from pathlib import Path
BASE=Path('/mnt/data/rawlsing_exec/o12r2')
OUT=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R7_20260811')
if OUT.exists(): shutil.rmtree(OUT)
for d in ['AUDIT','NARROWING','PROVENANCE','VALIDATION','CODE']: (OUT/d).mkdir(parents=True,exist_ok=True)
reg=pd.read_csv(BASE/'CANONICAL_IMPLEMENTATION_REGISTRY.csv',low_memory=False)
r6=pd.read_csv(BASE/'INTER_QUESTION_RELATION_AUTHORITY_R2.csv',low_memory=False)
r5=pd.read_csv(BASE/'SEMANTIC_EDGE_ADJUDICATION_DENOMINATOR_R5_CODEX_RECONCILED.csv',low_memory=False)
r14j=json.load(open(BASE/'R14_SOURCE_NATIVE_AUTHORITY_FINAL_708047.json'))
s16=pd.read_csv(BASE/'S16_WAVE_RELATION_CLASS_CAPABILITY_ATLAS.csv',low_memory=False)
# R6 62 canaries
r6t=r6[r6.relation_type.eq('COMPLEMENTARY_ROLE_CONVERGENCE')].copy()
r6t.to_csv(OUT/'PROVENANCE/R6_T11_62_SEALED_PARENT_ROWS_R7.csv',index=False)
r6_structs=set()
for s in r6t.source_structure_ids.dropna():
    try:r6_structs.update(json.loads(s))
    except:pass
# R5 118 recall locator accounting
r5t=r5[r5.discovery_only_candidate_types.fillna('').str.contains('SOURCE_NATIVE_COMMON_ROLE_SET_REVIEW')].copy()
acc=[]
for _,o in r5t.iterrows():
    oid=str(o.object_id)
    x=reg[reg.r14_object_ids_json.fillna('').str.contains(re.escape(oid),regex=True)]
    sem=x[x.sem__audit_unit_id.notna()].drop_duplicates('sem__audit_unit_id')
    direct=[]
    for target,g in sem.groupby(sem.sem__canonical_target_id.fillna('')):
        if not target: continue
        roles=sorted(set(g.sem__canonical_role.dropna().astype(str)))
        if len(roles)>=2:
            direct.append({'target':target,'roles':roles,'vars':sorted(set(g.source_variable_code.dropna().astype(str)))})
    if oid in r6_structs:
        disp='KNOWN_R6_T11_SOURCE_STRUCTURE'
        reason='Existing sealed R6 T11 authority; recall locator is calibration only.'
    elif len(sem)==0:
        disp='INPUT_AUTHORITY_INCOMPLETE__NO_CURRENT_RELATIONAL_SEMANTIC_UNITS'
        reason='R5 recall object has no current relational semantic units; cannot prove T11 absence or emit relation.'
    elif direct:
        disp='DIRECT_T11_OPPORTUNITY__ACCOUNTED_IN_INDEPENDENT_R14_SCAN'
        reason='Current exact object contains same-target multi-role structure; adjudicated in independent R14 scan.'
    else:
        disp='NO_DIRECT_T11_COMMON_TARGET_MULTIROLE_STRUCTURE_AT_CURRENT_COORDINATES'
        reason='Current mapped members do not form same-target multi-role convergence inside this exact source object; cross-object search handled separately.'
    acc.append({**o.to_dict(),'current_semantic_unit_count':len(sem),'same_target_multi_role_group_count':len(direct),'disposition':disp,'reason':reason})
pd.DataFrame(acc).to_csv(OUT/'AUDIT/R5_T11_118_RECALL_LOCATOR_DISPOSITION_R7.csv',index=False)
# Independent R14 596 source-object scan
objs=[o for o in r14j['objects'] if o.get('state') in ('ACCEPTED_SOURCE_NATIVE_JOINT','JOINT_SOURCE_NATIVE')]
scan=[]; direct_opps=[]
for o in objs:
    oid=o['object_id']
    x=reg[reg.r14_object_ids_json.fillna('').str.contains(re.escape(oid),regex=True)]
    sem=x[x.sem__audit_unit_id.notna()].drop_duplicates('sem__audit_unit_id')
    groups=[]
    for target,g in sem.groupby(sem.sem__canonical_target_id.fillna('')):
        if not target: continue
        roles=sorted(set(g.sem__canonical_role.dropna().astype(str)))
        if len(roles)>=2:
            groups.append((target,roles,sorted(set(g.sem__measured_predicate.dropna().astype(str))),sorted(set(g.source_variable_code.dropna().astype(str)))))
    if not groups:
        disp='NO_DIRECT_SAME_TARGET_MULTIROLE_T11_STRUCTURE'
    elif oid in ('LB1995-P15-SOURCE-NATIVE','LB1995-P46-SOURCE-NATIVE'):
        disp='REJECT_BOUND_MEMBERSHIP_MISMATCH__REGISTRY_ASSOCIATION_NOT_EXACT_OBJECT_MEMBER'
    elif oid in r6_structs:
        disp='KNOWN_R6_T11_SOURCE_STRUCTURE'
    else:
        disp='EMIT_SOURCE_NATIVE_T11_REVIEW_OPPORTUNITY'
        for target,roles,preds,vars_ in groups:
            direct_opps.append({'object_id':oid,'source_family':o.get('family'),'wave':o.get('wave'),'printed_parent_id':o.get('printed_parent_id'),'printed_parent_text':o.get('printed_parent_text'),'target_id':target,'roles_json':json.dumps(roles),'predicates_json':json.dumps(preds),'source_variable_codes_json':json.dumps(vars_),'disposition':'EMIT_SOURCE_NATIVE_T11_REVIEW_OPPORTUNITY'})
    scan.append({'object_id':oid,'source_family':o.get('family'),'wave':o.get('wave'),'state':o.get('state'),'exact_bound_members_json':json.dumps(o.get('members',[])),'current_semantic_unit_count':len(sem),'same_target_multi_role_group_count':len(groups),'disposition':disp})
pd.DataFrame(scan).to_csv(OUT/'NARROWING/T11_R14_596_SOURCE_OBJECT_ACCOUNTING_R7.csv',index=False)
pd.DataFrame(direct_opps).to_csv(OUT/'NARROWING/T11_SOURCE_NATIVE_DIRECT_OPPORTUNITIES_R7.csv',index=False)
# Full cross-object same-target search (not limited to block)
r=reg[reg.sem__audit_unit_id.notna()].copy()
for c in ['sem__canonical_target_id','sem__canonical_role']: r[c]=r[c].fillna('').astype(str)
r=r[(r.sem__canonical_target_id!='')&(r.sem__canonical_role!='')]
groups=[]
for key,x in r.groupby(['source_family','wave','sem__canonical_target_id']):
    roles=sorted(set(x.sem__canonical_role))
    if len(roles)<2: continue
    groups.append({'source_family':key[0],'wave':str(key[1]),'target_id':key[2],'roles_json':json.dumps(roles),'blocks_json':json.dumps(sorted(set(x.sem__canonical_question_block_id.dropna().astype(str)))),'source_variable_codes_json':json.dumps(sorted(set(x.source_variable_code.dropna().astype(str)))),'predicates_json':json.dumps(sorted(set(x.sem__measured_predicate.dropna().astype(str)))),'texts_json':json.dumps(list(dict.fromkeys(x.exact_question_text.dropna().astype(str)))),'r14_ids_json':json.dumps(sorted(set(sum([json.loads(v) if isinstance(v,str) and v.startswith('[') else [] for v in x.r14_object_ids_json.dropna()],[]))))})
full=pd.DataFrame(groups)
# manual exact semantic dispositions by (family,wave,target)
D={}
def setd(f,w,t,disp,reason,packet='',hyp='T11'):
    D[(f,str(w),t)]=(disp,reason,packet,hyp)
# rejects / redirects
for k,reason,hyp in [
(('Arab Barometer','I','target__education'),'Target coordinate joins government education performance to education as a voting criterion; not one narrow proposition.',''),
(('EVS','1981','target__abortion'),'Approval/justifiability variants are near-equivalent normative judgment terrain, not distinct complementary components.','T01/T02'),
(('EVS','1990','target__abortion'),'Church-public-role stance and abortion approval are different propositions sharing a topic target.','T03'),
(('EVS','1990','target__death'),'Reflection on death and religious-service importance at death are distinct propositions sharing a broad target.',''),
(('EVS','1990','target__homosexuality'),'Church public-role stance and personal justifiability are distinct propositions; common target alone is insufficient.','T03'),
(('EVS','1999','target__abortion'),'Approval/justifiability variants are near-equivalent judgment terrain, not complementary components.','T01/T02'),
(('EVS','1999','target__respondent_life'),'Religion importance and global happiness collide on an over-broad respondent-life target; no narrow common proposition.',''),
(('EVS','2008','target__abortion'),'Approval/justifiability variants are near-equivalent judgment terrain, not complementary components.','T01/T02'),
(('EVS','2008','target__men'),'Male fulfillment-through-children and equal home responsibility are separate gender propositions; shared target men is too broad.',''),
(('GSS','1984','target__banks_and_financial_institutions'),'Two rows are source/response-topology variants of the same trust proposition; duplicate semantics do not create complementarity.',''),
(('GSS','1984','target__executive_branch_federal_government'),'Two rows are source/response-topology variants of the same trust proposition; duplicate semantics do not create complementarity.',''),
(('GSS','1984','target__mandatory_military_service'),'Female/male target variants are target differentiation, not complementary roles by themselves.','T01/T09'),
(('WVS','W7','target__respondent_country'),'War involvement and felt closeness share a country target but not a narrow common proposition.','')]:
    setd(*k,'REJECT_T11__'+('OTHER_RELATION_TERRAIN' if hyp else 'NO_COMMON_NARROW_PROPOSITION'),reason,'',hyp)
# candidates / packets
cand=[
(('Arab Barometer','II','target__respondent_and_family'),'Current security level and year-over-year security change are distinct temporal components of one personal/family security proposition.','T11R7-P01-ARABII-SECURITY-CURRENT-CHANGE','T11;T02'),
(('EVS','1999','target__elderly_people'),'Concern, willingness to help, and source-native reasons for helping converge on one named social target; includes governed T06 canary terrain.','T11R7-P02-EVS1999-PROSOCIAL-HELP','T11;T06'),
(('EVS','1999','target__immediate_family'),'Concern and willingness to help are distinct salience/intention components for one named target.','T11R7-P02-EVS1999-PROSOCIAL-HELP','T11'),
(('EVS','1999','target__immigrants'),'Concern/willingness plus source-native help-reason components converge on the immigrants help proposition; includes governed T06 canary terrain.','T11R7-P02-EVS1999-PROSOCIAL-HELP','T11;T06'),
(('EVS','1999','target__neighborhood_people'),'Concern and willingness to help are distinct salience/intention components for one named target.','T11R7-P02-EVS1999-PROSOCIAL-HELP','T11'),
(('EVS','1999','target__sick_disabled_people'),'Concern and willingness to help are distinct salience/intention components for one named target.','T11R7-P02-EVS1999-PROSOCIAL-HELP','T11'),
(('GSS','1973','target__respondent_life'),'General happiness and exciting/dull life appraisal are distinct bounded life-evaluation components.','T11R7-P03-GSS1973-LIFE-EVALUATION','T11'),
(('GSS','1984','target__military_service'),'Experience evaluation and peace/war civic-obligation propositions form a bounded military-service configuration; gender and war/peace axes also trigger T01/T09/T10 review.','T11R7-P04-GSS1984-MILITARY-SERVICE','T11;T01;T09;T10'),
(('GSS','2010','target__elected_officials'),'Perceived influence and perceived risk knowledge are distinct actor-capacity components; narrowness requires semantic review.','T11R7-P05-GSS2010-ELECTED-OFFICIALS','T11'),
(('GSS','2024','target__mental_health_vignette_subject_x'),'Coercive intervention norms, voluntary help recommendation and social-distance response share one vignette subject but require bounded-proposition review.','T11R7-P06-GSS2024-MENTAL-HEALTH-VIGNETTE','T11;T06'),
(('GSS','2024','target__psychiatric_hospitalization'),'Danger-to-self/others conditions and hospitalization recommendation/law form a bounded treatment/risk configuration.','T11R7-P06-GSS2024-MENTAL-HEALTH-VIGNETTE','T11;T02;T06'),
(('Latinobarómetro','1995','target__national_economic_situation'),'Current, retrospective and prospective economic evaluations form a bounded temporal economic-state configuration.','T11R7-P07-TEMPORAL-STATE-CHANGE','T11;T02'),
(('Latinobarómetro','2011','target__national_economic_situation'),'Current, retrospective and prospective economic evaluations form a bounded temporal economic-state configuration.','T11R7-P07-TEMPORAL-STATE-CHANGE','T11;T02'),
(('LiTS','III','target__national_economy'),'Current satisfaction and retrospective economic change are distinct temporal components of national-economy evaluation.','T11R7-P07-TEMPORAL-STATE-CHANGE','T11;T02'),
(('LiTS','III','target__local_government'),'Overall local-government performance and change in performance are distinct temporal performance components.','T11R7-P07-TEMPORAL-STATE-CHANGE','T11;T02'),
(('South Asia','W1','target__household_economic_condition'),'Current household-economic satisfaction and change from prior years are distinct temporal components.','T11R7-P07-TEMPORAL-STATE-CHANGE','T11;T02'),
(('Latinobarómetro','1995','target__radio'),'News-use frequency and attention to political news are distinct media-use/attention components.','T11R7-P08-LATIN1995-RADIO-USE-ATTENTION','T11'),
(('Latinobarómetro','2011','target__crime'),'Crime-trend perception and perceived state problem-solving capacity are distinct crime-field components; narrowness requires review.','T11R7-P09-LATIN2011-CRIME','T11'),
(('Latinobarómetro','2011','target__united_states'),'Affective opinion and bilateral relation-quality assessment are distinct relations to the same external actor.','T11R7-P10-LATIN-BILATERAL-RELATIONS','T11'),
(('Latinobarómetro','2024','target__china'),'Affective opinion plus overall/economic/security bilateral relation quality form a bounded external-actor relation configuration.','T11R7-P10-LATIN-BILATERAL-RELATIONS','T11'),
(('Latinobarómetro','2024','target__israel'),'Affective opinion and overall bilateral relation-quality assessment are distinct relations to the same external actor.','T11R7-P10-LATIN-BILATERAL-RELATIONS','T11'),
(('Latinobarómetro','2024','target__russia'),'Affective opinion plus overall/economic/security bilateral relation quality form a bounded external-actor relation configuration.','T11R7-P10-LATIN-BILATERAL-RELATIONS','T11'),
(('Latinobarómetro','2024','target__united_states'),'Affective opinion plus overall/economic/security bilateral relation quality form a bounded external-actor relation configuration.','T11R7-P10-LATIN-BILATERAL-RELATIONS','T11'),
(('LiTS','III','target__corruption_reporting'),'Social acceptability, personal moral duty, willingness and explicit court-time cost converge on corruption reporting; preserve T05/T06 cross-rule packet.','T11R7-P11-LITSIII-CORRUPTION-REPORT','T11;T05;T06'),
(('LiTS','III','target__free_and_fair_elections'),'Normative importance and perceived existence are complementary role components for the same democratic condition.','T11R7-P12-LITSIII-IMPORTANCE-EXISTENCE','T11'),
(('LiTS','III','target__freedom_of_speech'),'Normative importance and perceived existence are complementary role components for the same democratic condition.','T11R7-P12-LITSIII-IMPORTANCE-EXISTENCE','T11'),
(('LiTS','III','target__law_and_order'),'Normative importance and perceived existence are complementary role components for the same condition.','T11R7-P12-LITSIII-IMPORTANCE-EXISTENCE','T11'),
(('LiTS','III','target__peace_and_stability'),'Normative importance and perceived existence are complementary role components for the same condition.','T11R7-P12-LITSIII-IMPORTANCE-EXISTENCE','T11'),
(('LiTS','III','target__strong_political_opposition'),'Normative importance and perceived existence are complementary role components for the same democratic condition.','T11R7-P12-LITSIII-IMPORTANCE-EXISTENCE','T11'),
(('LiTS','III','target__regional_government'),'Trust plus current and retrospective performance evaluations are distinct bounded relations to regional government.','T11R7-P13-LITSIII-REGIONAL-GOVERNMENT','T11'),
(('WVS','W7','target__family'),'Family importance and family trust are distinct salience/reliance components for one target.','T11R7-P14-WVSW7-FAMILY','T11'),
(('WVS','W7','target__god'),'Importance of God and belief in God are distinct salience/belief components.','T11R7-P15-WVSW7-GOD','T11'),
(('WVS','W7','target__government'),'Q291 government-quality components are already sealed T11 authority; Q292 distrust/caution item is a cross-object extension requiring review, not a new base packet.','T11R7-P16-WVSW7-R6-EXTENSIONS','T11'),
(('WVS','W7','target__parliament'),'Q291 parliament-quality components are already sealed T11 authority; general parliament trust is a cross-object extension requiring review.','T11R7-P16-WVSW7-R6-EXTENSIONS','T11')]
for k,reason,pid,hyp in cand: setd(*k,'EMIT_T11_REVIEW_CANDIDATE',reason,pid,hyp)
# ensure all 47 dispositioned
out=[]
for _,g in full.iterrows():
    key=(g.source_family,str(g.wave),g.target_id)
    if key not in D:
        raise RuntimeError('missing disposition '+repr(key))
    disp,reason,pid,hyp=D[key]
    out.append({**g.to_dict(),'disposition':disp,'reason':reason,'packet_id':pid,'rule_hypotheses':hyp})
cross=pd.DataFrame(out)
cross.to_csv(OUT/'NARROWING/T11_CROSS_OBJECT_47_GROUP_DISPOSITION_R7.csv',index=False)
# old O11 24 proxy audit: same block + target groups are subset of full; mark by key
old=[]
for key,x in r.groupby(['source_family','wave','sem__canonical_question_block_id','sem__canonical_target_id']):
    roles=sorted(set(x.sem__canonical_role))
    if not key[2] or not key[3] or len(roles)<2: continue
    k=(key[0],str(key[1]),key[3]); disp,reason,pid,hyp=D[k]
    old.append({'source_family':key[0],'wave':str(key[1]),'block_id':key[2],'target_id':key[3],'roles_json':json.dumps(roles),'source_variable_codes_json':json.dumps(sorted(set(x.source_variable_code.dropna().astype(str)))),'disposition':disp,'reason':reason,'packet_id':pid,'rule_hypotheses':hyp})
pd.DataFrame(old).to_csv(OUT/'AUDIT/O11_T11_OLD_PROXY_GROUP_DISPOSITION_R7.csv',index=False)
# S16 T11 cells diagnostic
rulecol=[c for c in s16.columns if c in ('rule_id','relation_rule_id','relation_class_id')][0]
s16t=s16[s16[rulecol].astype(str).eq('S14-T11')].copy()
s16t.to_csv(OUT/'AUDIT/O11_T11_35_CELL_DIAGNOSTIC_R7.csv',index=False)
# canonical packets from emits, grouping packet id; include direct source-native into EVS packet
em=cross[cross.disposition.eq('EMIT_T11_REVIEW_CANDIDATE')].copy()
pack=[]
for pid,g in em.groupby('packet_id',sort=True):
    famwaves=sorted(set(g.source_family.astype(str)+'::'+g.wave.astype(str)))
    targets=sorted(set(g.target_id.astype(str)))
    vars_=sorted(set(sum([json.loads(v) for v in g.source_variable_codes_json],[])))
    hyps=sorted(set(sum([str(v).split(';') for v in g.rule_hypotheses],[])))
    pack.append({'packet_id':pid,'status':'UNRESOLVED_SEMANTIC_REVIEW_PACKET','source_family_waves_json':json.dumps(famwaves),'targets_json':json.dumps(targets),'member_source_variable_codes_json':json.dumps(vars_),'rule_hypotheses':';'.join(hyps),'raw_group_count':len(g),'notes':'Cross-object/full-registry T11 narrowing packet. Review creates no authority until S14 adjudication.'})
packdf=pd.DataFrame(pack)
packdf.to_csv(OUT/'NARROWING/T11_CANONICAL_REVIEW_PACKETS_R7.csv',index=False)
# status/report
status={
 'checkpoint':'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R7_20260811','status':'IN_PROGRESS_NOT_FROZEN','active_state':'R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR','job3_authorized':False,'o12_r2_811_complete_authority':False,'workers_launched':False,
 't11':{'sealed_r6_canaries_accounted':len(r6t),'r5_recall_locators_accounted':len(r5t),'r14_joint_objects_accounted':len(objs),'source_native_apparent_hits':4,'source_native_valid_review_opportunities':len(direct_opps),'source_native_rejected_bound_membership_hits':2,'full_cross_object_same_target_multirole_groups':len(full),'old_o11_same_block_proxy_groups':len(old),'review_emitting_cross_object_groups':int((cross.disposition=='EMIT_T11_REVIEW_CANDIDATE').sum()),'canonical_review_packets':len(packdf),'next_dependency':'cross-rule packet dedupe T03-T11'},
 'remaining_major_rules':[],'next_decision':'merge/dedupe T03-T11 packets, measure exact unresolved workload, then worker economics',
 'repair_stack':{'done':[1,7,8],'partial':[2,3,4,5,6,9,10,11,12,13,14,15,23],'open':[16,17,18,19,20,21,22,24,25]}
}
json.dump(status,open(OUT/'CURRENT_STATUS_R7.json','w'),indent=2)
report=f'''# T11 Complementary-Role Narrowing — Checkpoint R7\n\n## Status\nT11 narrowing completed as a bounded review frontier; no new S14 relation authority is frozen here. Job 3 remains blocked.\n\n## Independent search surfaces\n- sealed R6 T11 authority accounted: **{len(r6t)} / {len(r6t)}**\n- bounded R5 T11 recall locators dispositioned: **{len(r5t)} / {len(r5t)}**\n- exact R14 joint source objects independently scanned: **{len(objs)}**\n- full current same-wave/same-target multi-role groups (across blocks): **{len(full)}**\n- old O11 same-block proxy groups: **{len(old)}**\n\n## Source-native finding\nOnly four R14 objects appear to contain current same-target/multi-role structure. EVS 1999 Q82 and Q83 are genuine exact-bound help-reason batteries and are carried into the EVS prosocial review packet. The two Latin 1995 apparent hits are rejected because the registry association does not match the exact bound P15/P46 member identities; page/object association is not allowed to manufacture T11 structure.\n\n## Cross-object finding\nThe repaired cross-object search finds {len(full)} groups, not the old proxy-only {len(old)}. **{int((cross.disposition=='EMIT_T11_REVIEW_CANDIDATE').sum())}** raw groups survive semantic narrowing and compress to **{len(packdf)} canonical packets**. All other groups receive typed rejection/redirect dispositions.\n\n## Governing law\nEach role/component must add distinct bounded information to one narrow proposition or field. Shared target, shared wording, broad topical similarity, latent-scale intuition, source proximity, and embeddings are not relation authority. Existing R6 broad configurations remain sealed authority within their jurisdiction; this checkpoint does not generalize their evidence ceiling into a latent trait model.\n\n## Next\nCross-rule canonical packet merge/dedupe for T03–T11, then exact worker-economics measurement.\n'''
open(OUT/'T11_NARROWING_R7_REPORT.md','w').write(report)
open(OUT/'NEXT_EXECUTION_STEPS.md','w').write('# Exact Resume Sequence after T11 R7\n\n1. Merge canonical review packets across T03–T11.\n2. Cross-rule deduplicate exact evidence/member packets.\n3. Account every raw opportunity to one canonical packet, terminal exclusion, or blocker.\n4. Measure exact unresolved semantic packet denominator.\n5. Decide central vs worker execution from measured workload.\n6. Adjudicate/freeze S14 relation-role authority.\n7. Rebuild O11, then O12, then independent completeness proof.\n\nNo Job 3 or old worker packs.\n')
open(OUT/'00_README_FIRST.md','w').write(report+'\nSee CURRENT_STATUS_R7.json and NEXT_EXECUTION_STEPS.md.\n')
# parent pins
pins={}
for fn in ['INTER_QUESTION_RELATION_AUTHORITY_R2.csv','CANONICAL_IMPLEMENTATION_REGISTRY.csv','SEMANTIC_EDGE_ADJUDICATION_DENOMINATOR_R5_CODEX_RECONCILED.csv','R14_SOURCE_NATIVE_AUTHORITY_FINAL_708047.json','S16_WAVE_RELATION_CLASS_CAPABILITY_ATLAS.csv']:
    b=open(BASE/fn,'rb').read(); pins[fn]={'sha256':hashlib.sha256(b).hexdigest(),'size_bytes':len(b)}
json.dump(pins,open(OUT/'PROVENANCE/PARENT_PINS_R7.json','w'),indent=2)
# validator
val='''import pandas as pd,json,sys,os\nR=os.path.dirname(os.path.dirname(__file__))\ne=[];c=0\ndef ck(n,b,d=None):\n global c;c+=1\n if not b:e.append((n,d))\nr6=pd.read_csv(os.path.join(R,'PROVENANCE/R6_T11_62_SEALED_PARENT_ROWS_R7.csv'))\nr5=pd.read_csv(os.path.join(R,'AUDIT/R5_T11_118_RECALL_LOCATOR_DISPOSITION_R7.csv'))\nr14=pd.read_csv(os.path.join(R,'NARROWING/T11_R14_596_SOURCE_OBJECT_ACCOUNTING_R7.csv'))\ndirect=pd.read_csv(os.path.join(R,'NARROWING/T11_SOURCE_NATIVE_DIRECT_OPPORTUNITIES_R7.csv'))\ncross=pd.read_csv(os.path.join(R,'NARROWING/T11_CROSS_OBJECT_47_GROUP_DISPOSITION_R7.csv'))\nold=pd.read_csv(os.path.join(R,'AUDIT/O11_T11_OLD_PROXY_GROUP_DISPOSITION_R7.csv'))\npk=pd.read_csv(os.path.join(R,'NARROWING/T11_CANONICAL_REVIEW_PACKETS_R7.csv'))\nst=json.load(open(os.path.join(R,'CURRENT_STATUS_R7.json')))\nck('r6_62',len(r6)==62,len(r6));ck('r5_118',len(r5)==118,len(r5));ck('r5_no_empty',r5.disposition.fillna('').str.len().gt(0).all())\nck('r14_596',len(r14)==596,len(r14));ck('r14_no_empty',r14.disposition.fillna('').str.len().gt(0).all())\nck('direct_valid_two',len(direct)==2,len(direct));ck('cross_47',len(cross)==47,len(cross));ck('cross_no_empty',cross.disposition.fillna('').str.len().gt(0).all())\nck('old_proxy_24',len(old)==24,len(old));ck('packets_nonempty',len(pk)>0,len(pk));ck('all_emit_have_packet',cross.loc[cross.disposition.eq('EMIT_T11_REVIEW_CANDIDATE'),'packet_id'].fillna('').str.len().gt(0).all())\nck('no_authority_accepts',not cross.disposition.str.startswith('ACCEPT').any())\nck('job3_false',st.get('job3_authorized') is False);ck('next_dedupe',st.get('t11',{}).get('next_dependency')=='cross-rule packet dedupe T03-T11')\nck('no_empty_packet_hyp',pk.rule_hypotheses.fillna('').str.len().gt(0).all())\nres={'status':'PASS' if not e else 'FAIL','checks':c,'errors':e};json.dump(res,open(os.path.join(R,'VALIDATION/VALIDATION_RESULT_R7.json'),'w'),indent=2);print(json.dumps(res,indent=2));sys.exit(1 if e else 0)\n'''
open(OUT/'VALIDATION/validate_t11_checkpoint_r7.py','w').write(val)
shutil.copy('/mnt/data/build_t11_r7.py',OUT/'CODE/build_t11_checkpoint_r7.py')
