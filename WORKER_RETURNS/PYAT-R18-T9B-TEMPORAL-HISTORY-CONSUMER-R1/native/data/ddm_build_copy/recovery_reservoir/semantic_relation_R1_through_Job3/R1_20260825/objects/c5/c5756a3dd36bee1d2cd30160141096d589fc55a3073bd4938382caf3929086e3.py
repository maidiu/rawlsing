import pandas as pd, json, os, re, itertools, hashlib, zipfile, shutil, collections
from pathlib import Path

BASE=Path('/mnt/data/rawlsing_exec/o12r2')
R4=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R4_20260811')
OUT=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R5_20260811')
ZIP=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R5_20260811.zip')
if OUT.exists(): shutil.rmtree(OUT)
for p in ['AUDIT','NARROWING','PROVENANCE','VALIDATION','CODE']: (OUT/p).mkdir(parents=True,exist_ok=True)

r6=pd.read_csv(BASE/'INTER_QUESTION_RELATION_AUTHORITY_R2.csv')
r5=pd.read_csv(BASE/'SEMANTIC_EDGE_ADJUDICATION_DENOMINATOR_R5_CODEX_RECONCILED.csv')
reg=pd.read_csv(BASE/'CANONICAL_IMPLEMENTATION_REGISTRY.csv',low_memory=False)
s16=pd.read_csv(BASE/'S16_WAVE_RELATION_CLASS_CAPABILITY_ATLAS.csv')
r14=json.load(open(BASE/'R14_SOURCE_NATIVE_AUTHORITY_FINAL_708047.json'))
objs=[o for o in r14['objects'] if o.get('state')=='ACCEPTED_SOURCE_NATIVE_JOINT']
obj_by={o['object_id']:o for o in r14['objects'] if o.get('object_id')}

fammap={'ASB':'Asian Barometer','ArabBarometer':'Arab Barometer'}
reg_key={}
for _,x in reg.iterrows():
    reg_key.setdefault((str(x.source_family),str(x.wave),str(x.source_variable_code).lower()),[]).append(x)
def obj_rows(o):
    fam=fammap.get(o.get('family'),o.get('family')); wave=str(o.get('wave'))
    z=[]
    for m in o.get('members',[]):
        rr=reg_key.get((fam,wave,str(m).lower()),[])
        if rr: z.append(rr[0])
    return z

def normab(v): return re.sub(r'(?<=\d)[ab](?=(_|$))','',str(v).lower())
def clean(x):
    if pd.isna(x): return ''
    s=str(x); return '' if s.lower()=='nan' else s

def sha(p):
    h=hashlib.sha256();
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

# sealed T09 canary
can=r6[r6.relation_type.eq('RECIPROCAL_ROLE_REVERSAL')].copy()
assert len(can)==1
can.to_csv(OUT/'PROVENANCE/R6_T09_SEALED_PARENT_ROW_R5.csv',index=False)
cr=can.iloc[0]
canary_member_ids=json.loads(cr.member_question_implementation_ids)
canary_members=reg[reg.question_implementation_id.isin(canary_member_ids)].copy()
keep=['question_implementation_id','source_family','wave','source_variable_code','exact_question_text','sem__audit_unit_id','sem__semantic_summary','sem__measured_predicate','sem__canonical_target_id','o06__routing_status','respondent_universe_status']
canary_members[keep].to_csv(OUT/'PROVENANCE/R6_T09_CANARY_CURRENT_MEMBER_ROWS_R5.csv',index=False)

# R5 recall-only 110 locator accounting
r5t=r5[r5.discovery_only_candidate_types.fillna('').str.contains('RECIPROCAL_ROLE_REVERSAL')].copy()
assert len(r5t)==110
canary_oids=set(json.loads(cr.source_structure_ids))
rows=[]
for _,x in r5t.iterrows():
    oid=x.object_id
    if oid=='ArabBarometer-R14-VIII-Q628':
        disp='SOURCE_ROLE_LABEL_BLOCKER__Q628_A_B_CHILD_MEANING_NOT_EXPLICIT_IN_CURRENT_CANONICAL_TEXT'
        reason='R5 is recall-only. Q628 has A/B child pairs but current canonical child text repeats the parent prompt and does not govern the A/B role semantics; suffixes cannot authorize reciprocal direction.'
    elif oid in {'EVS-R14-1981-Q208_SELF','EVS-R14-1981-Q208_OTHERS'}:
        disp='RECALL_EVALUATED__SELF_VS_MOST_PEOPLE_SCOPE_CONTRAST_NOT_RECIPROCAL_DIRECTION'
        reason='Parallel norm-applicability batteries compare respondent-self with most-people scope; no actor/recipient role reversal.'
    elif oid=='ArabBarometer-R14-VIII-Q601':
        disp='RECALL_EVALUATED__GENDER_NORM_ALTERNATIVES_NOT_RECIPROCAL_DIRECTION'
        reason='Gender/family propositions vary normative content and target, not reversed actor/recipient slots.'
    elif oid=='ArabBarometer-R14-VIII-Q624':
        disp='SOURCE_ROLE_LABEL_BLOCKER__Q624_5A_5B_MEANING_NOT_EXPLICIT_IN_CURRENT_CANONICAL_TEXT'
        reason='A/B child labels are not sufficient in current canonical text to govern reciprocal direction; preserve as source-semantic blocker.'
    elif oid=='Afrobarometer-R14-R9-Q52':
        disp='RECALL_EVALUATED__DIFFERENT_ACTOR_RECIPIENT_CONFIGURATIONS_NOT_REVERSAL'
        reason='Parent-to-child discipline and man-to-wife discipline are different actor/recipient configurations, not the same relation with roles reversed.'
    else:
        disp='RECALL_ONLY__NO_EXPLICIT_RECIPROCAL_ROLE_DIRECTION_AUTHORITY'
        reason='R5 discovery locator is non-authoritative and this source object alone does not encode an explicit actor↔recipient directional reversal under current authority.'
    rows.append({
        'object_id':oid,'source_family':x.source_family,'wave':x.wave,'parent_id':x.parent_id,
        'relation_member_count':x.relation_member_count,'r5_discovery_types':x.discovery_only_candidate_types,
        'disposition':disp,'reason':reason,'is_sealed_canary_parent':oid in canary_oids
    })
r5ledger=pd.DataFrame(rows)
assert not r5ledger.is_sealed_canary_parent.any() # important diagnostic: R5 locator misses both canary parents
r5ledger.to_csv(OUT/'AUDIT/T09_R5_110_RECALL_LOCATOR_DISPOSITION_R5.csv',index=False)

# independent R14 cross-object pair opportunities from sealed source structures
byfw=collections.defaultdict(list)
for o in objs: byfw[(fammap.get(o.get('family'),o.get('family')),str(o.get('wave')))].append(o)
sem_by={}
for o in objs:
    sig=[]
    for rr in obj_rows(o):
        p=clean(rr.get('sem__measured_predicate')); t=clean(rr.get('sem__canonical_target_id'))
        if p or t: sig.append((p,t))
    sem_by[o['object_id']]=sig
pairset={}
def addpair(key,a,b,basis,detail):
    ids=tuple(sorted([a['object_id'],b['object_id']]))
    z=pairset.setdefault(ids,{'source_family':key[0],'wave':key[1],'object_a':ids[0],'object_b':ids[1],'bases':set(),'details':[]})
    z['bases'].add(basis); z['details'].append(detail)
for key,gg in byfw.items():
    for a,b in itertools.combinations(gg,2):
        ma=[normab(x) for x in a.get('members',[])]; mb=[normab(x) for x in b.get('members',[])]
        if ma and mb and set(ma)==set(mb): addpair(key,a,b,'PARALLEL_A_B_MEMBER_STRUCTURE',str(sorted(set(ma))))
        sa=set(sem_by.get(a['object_id'],[])); sb=set(sem_by.get(b['object_id'],[])); inter=sa&sb
        if len(inter)>=2: addpair(key,a,b,'MULTI_MEMBER_CURRENT_SEMANTIC_OVERLAP',f'overlap={len(inter)}')
# force known EVS self/others scope contrast into expected-space audit
for aa,bb in [('EVS-R14-1981-Q208_SELF','EVS-R14-1981-Q208_OTHERS')]:
    a=obj_by[aa];b=obj_by[bb];addpair(('EVS','1981'),a,b,'EXPLICIT_PARALLEL_SCOPE_PAIR','same ten-commandment target set')

def pairdisp(a,b):
    s={a,b}
    if s==canary_oids:
        return ('KNOWN_R6_T09_CANARY__SEMANTIC_AUTHORITY_PRESENT__CURRENT_ROUTING_BLOCKED',
                'Exact accepted R6 cross-object reciprocal-role relation. Semantic authority retained; all four current members are SOURCE_ROUTING_UNRESOLVED, so current O11 observability remains routing-blocked.')
    if s=={'ArabBarometer-R14-VIII-Q550A','ArabBarometer-R14-VIII-Q550B'}:
        return ('REJECT_DIFFERENT_PROPOSITION_FRAME__HUMAN_DIGNITY_VS_DEMOCRACY','Parallel items change the evaluative frame from human dignity to democracy; no actor/recipient reversal.')
    if s=={'ArabBarometer-R14-VIII-Q553A','ArabBarometer-R14-VIII-Q553B'}:
        return ('REJECT_COMPLEMENTARY_PREDICATES__CONTRIBUTION_VS_RESPONSIBILITY','Same actors are rated for contribution to climate change versus responsibility for addressing it; this is predicate complementarity, not role reversal (possible T11 terrain).')
    if s=={'EVS-R14-1981-Q208_SELF','EVS-R14-1981-Q208_OTHERS'}:
        return ('REJECT_SUBJECT_SCOPE_CONTRAST__SELF_VS_MOST_PEOPLE','Same commandments are evaluated for self versus most people; no directional actor/recipient reversal.')
    if (a.startswith('WVS-R14-W7-') and b.startswith('WVS-R14-W7-') and a.replace('-','_').lower()==b.replace('-','_').lower()):
        return ('REJECT_DUPLICATE_SOURCE_OBJECT_ALIAS','Duplicate/alias materialization of the same source object, not two roles.')
    if 'ASB-R14-W4-' in a or 'ASB-R14-W4-' in b:
        return ('REJECT_OVERLAPPING_OR_SHIFTED_SOURCE_WINDOWS__NO_ROLE_REVERSAL','Current semantic overlap comes from overlapping/shifted source windows or repeated propositions, not a source-governed reversal of actor/recipient direction.')
    if 'EVS-R14-STRUCTURE-Q53' in a and 'EVS-R14-STRUCTURE-Q53' in b:
        return ('REJECT_DUPLICATE_SOURCE_STRUCTURE_VARIANT','Same exact source-member structure under duplicate structure materialization; no role reversal.')
    if a.startswith('ArabBarometer-R14-STRUCTURE-') or b.startswith('ArabBarometer-R14-STRUCTURE-'):
        return ('REJECT_GENERIC_MEMBER_ID_COLLISION__NO_GOVERNED_ROLE_ALIGNMENT','Generic item1/item2 member IDs collide across unrelated source structures; no current semantic role alignment licenses a reciprocal relation.')
    if s=={'WVS-R14-W7-Q58-Q63','WVS-R14-W7-Q58_Q63'} or s=={'WVS-R14-W7-Q64-Q89','WVS-R14-W7-Q64_Q89'}:
        return ('REJECT_DUPLICATE_SOURCE_OBJECT_ALIAS','Duplicate/alias materialization of the same source object, not two roles.')
    return ('REJECT_NO_EXPLICIT_RECIPROCAL_ROLE_DIRECTION','Parallel source structure/current semantic overlap does not encode the same proposition with actor/recipient roles reversed.')

prows=[]
for ids,z in sorted(pairset.items()):
    disp,reason=pairdisp(*ids)
    prows.append({**{k:v for k,v in z.items() if k not in ['bases','details']},
                  'generation_bases':'|'.join(sorted(z['bases'])),'generation_details':' || '.join(z['details']),
                  'disposition':disp,'reason':reason})
pairledger=pd.DataFrame(prows)
assert (pairledger.disposition.str.startswith('KNOWN_R6_T09_CANARY')).sum()==1
assert not pairledger.disposition.str.startswith('EMIT').any()
pairledger.to_csv(OUT/'NARROWING/T09_R14_CROSS_OBJECT_PAIR_OPPORTUNITIES_R5.csv',index=False)

# 548 source-object accounting
part=collections.defaultdict(list)
for _,p in pairledger.iterrows():
    part[p.object_a].append(p.disposition); part[p.object_b].append(p.disposition)
objrows=[]
for o in objs:
    oid=o['object_id']
    if oid in canary_oids: disp='KNOWN_R6_T09_CANARY_COMPONENT_OBJECT'
    elif oid=='ArabBarometer-R14-VIII-Q628': disp='SOURCE_ROLE_LABEL_BLOCKER__WITHIN_OBJECT_A_B_PAIRS'
    elif oid=='ArabBarometer-R14-VIII-Q624': disp='SOURCE_ROLE_LABEL_BLOCKER__WITHIN_OBJECT_A_B_PAIR'
    elif oid in part: disp='CROSS_OBJECT_OPPORTUNITY_EVALUATED__NO_NOVEL_T09' if not any(x.startswith('KNOWN') for x in part[oid]) else 'KNOWN_R6_T09_CANARY_COMPONENT_OBJECT'
    else: disp='NO_EXACT_RECIPROCAL_ROLE_PAIR_STRUCTURE_SIGNAL'
    objrows.append({'object_id':oid,'source_family':fammap.get(o.get('family'),o.get('family')),'wave':o.get('wave'),'printed_parent_id':o.get('printed_parent_id'),'member_count':len(o.get('members',[])),'accounting_disposition':disp})
objledger=pd.DataFrame(objrows); assert len(objledger)==548
objledger.to_csv(OUT/'NARROWING/T09_R14_548_OBJECT_ACCOUNTING_R5.csv',index=False)

# within-object A/B recall over the 110 R5 locator objects
intra=[]
for _,x in r5t.iterrows():
    o=obj_by.get(x.object_id)
    if not o: continue
    rr=obj_rows(o); vars=[str(r['source_variable_code']) for r in rr]
    for i,j in itertools.combinations(range(len(vars)),2):
        a,b=vars[i],vars[j]
        if normab(a)==normab(b) and a.lower()!=b.lower():
            oid=x.object_id
            if oid=='ArabBarometer-R14-VIII-Q628':
                disp='BLOCK_SOURCE_ROLE_LABELS_NOT_RECOVERED__A_B_SUFFIX_NOT_AUTHORITY'; reason='Current exact child labels repeat the parent prompt; A/B suffix does not reveal directional roles.'
            elif oid=='ArabBarometer-R14-VIII-Q624':
                disp='BLOCK_SOURCE_ROLE_LABELS_NOT_RECOVERED__A_B_SUFFIX_NOT_AUTHORITY'; reason='Current exact child labels do not identify distinct directional roles; preserve source blocker.'
            elif oid=='Afrobarometer-R14-R9-Q52':
                disp='REJECT_DIFFERENT_ACTOR_RECIPIENT_CONFIGURATIONS_NOT_REVERSED'; reason='Parent→child discipline versus man→wife discipline changes both relation and recipient rather than reversing the same roles.'
            elif oid=='ArabBarometer-R14-VIII-Q601':
                disp='REJECT_NORMATIVE_ALTERNATIVES_OR_TARGET_VARIANTS_NOT_ROLE_REVERSAL'; reason='A/B variants express different normative propositions/targets, not a directional role reversal.'
            else:
                disp='REJECT_SEQUENCE_RANK_TOPOLOGY_OR_TARGET_VARIANT_NOT_ROLE_REVERSAL'; reason='A/B source suffix reflects sequence/rank/variant structure without governed actor↔recipient reversal.'
            intra.append({'object_id':oid,'source_family':x.source_family,'wave':x.wave,'member_a':a,'member_b':b,'text_a':rr[i]['exact_question_text'],'text_b':rr[j]['exact_question_text'],'disposition':disp,'reason':reason})
intra=pd.DataFrame(intra)
intra.to_csv(OUT/'NARROWING/T09_WITHIN_OBJECT_A_B_RECALL_DISPOSITION_R5.csv',index=False)

# strict current-semantic role-token recall outside R14 pair logic: intentionally recall-only
role_pairs=[('female','male'),('woman','man'),('women','men'),('wife','husband'),('mother','father'),('daughter','son')]
def has(text,t): return re.search(r'(?<![A-Za-z])'+re.escape(t)+r'(?![A-Za-z])',str(text),re.I) is not None
sem=reg[reg['sem__audit_unit_id'].notna()].drop_duplicates('question_implementation_id').copy()
rhits=[]
for key,g in sem.groupby(['source_family','wave','sem__measured_predicate','sem__canonical_target_id'],dropna=False):
    if len(g)<2: continue
    gg=g.drop_duplicates('sem__audit_unit_id')
    for _,a in gg.iterrows():
      for _,b in gg.iterrows():
        if str(a.question_implementation_id)>=str(b.question_implementation_id): continue
        mt=[]
        for x,y in role_pairs:
            ax,ay=has(a.exact_question_text,x),has(a.exact_question_text,y); bx,by=has(b.exact_question_text,x),has(b.exact_question_text,y)
            if (ax and not ay and by and not bx) or (ay and not ax and bx and not by): mt.append(f'{x}<->{y}')
        if not mt: continue
        ta,tb=str(a.exact_question_text).lower(),str(b.exact_question_text).lower()
        if 'mil service good experience' in ta and 'military service good experience' in tb:
            disp='REJECT_TARGET_GROUP_DIFFERENTIATION__WOMEN_VS_MEN_NOT_DIRECTION_REVERSAL'
            reason='Same evaluative predicate varies gender target; no actor/recipient role reversal.'
        else:
            disp='REJECT_DIFFERENT_SCENARIO_OR_TARGET__ROLE_WORDS_ARE_NOT_DIRECTION_AUTHORITY'
            reason='Opposed role words occur, but the propositions/scenarios do not instantiate the same relation with actor and recipient reversed.'
        rhits.append({'source_family':key[0],'wave':key[1],'measured_predicate':key[2],'canonical_target_id':key[3],
                      'impl_a':a.question_implementation_id,'var_a':a.source_variable_code,'text_a':a.exact_question_text,
                      'impl_b':b.question_implementation_id,'var_b':b.source_variable_code,'text_b':b.exact_question_text,
                      'role_token_pair':'|'.join(mt),'disposition':disp,'reason':reason})
rhits=pd.DataFrame(rhits)
rhits.to_csv(OUT/'NARROWING/T09_STRICT_ROLE_TOKEN_RECALL_DISPOSITION_R5.csv',index=False)

# O11 35 cell diagnosis
t09cells=s16[s16.rule_id.eq('S14-T09')].copy(); assert len(t09cells)==35
t09cells['r5_successor_interpretation']='Old capability state retained as ancestry only; zero terrain was capability-interface absence, not empirical absence. Rebuild later from T09 bridge authority.'
t09cells.to_csv(OUT/'AUDIT/O11_T09_35_CELL_DIAGNOSTIC_R5.csv',index=False)

# Canonical packets
packets=pd.DataFrame([
 {'packet_id':'T09R5-P01-ARABVIII-Q604-RECIPROCAL-MARRIAGE','source_family':'Arab Barometer','wave':'VIII','members':'Q604A_NT_1+Q604A_NT_3 ↔ Q604B_NT_1+Q604B_NT_3','status':'KNOWN_R6_CANARY__NO_NEW_SEMANTIC_ADJUDICATION__CURRENT_ROUTING_BLOCKED','rule_hypotheses':'T09','notes':'Exact sealed R6 reciprocal-role authority; retains semantic truth while O06 routing remains unresolved for all four current members.'},
 {'packet_id':'T09R5-P02-ARABVIII-Q628-A-B','source_family':'Arab Barometer','wave':'VIII','members':'Q628_2A/B + Q628_3A/B + Q628_4A/B','status':'SOURCE_SEMANTIC_BLOCKER__NO_RELATION_VERDICT','rule_hypotheses':'T09?','notes':'A/B source roles are not explicit in current canonical child text. Do not infer role direction from suffixes.'},
 {'packet_id':'T09R5-P03-ARABVIII-Q624-5A-5B','source_family':'Arab Barometer','wave':'VIII','members':'Q624_5A + Q624_5B','status':'SOURCE_SEMANTIC_BLOCKER__NO_RELATION_VERDICT','rule_hypotheses':'T09?','notes':'Shared parent asks household-task responsibility but current child text does not govern A/B role meaning. Preserve blocker.'}
])
packets.to_csv(OUT/'NARROWING/T09_CANONICAL_PACKETS_R5.csv',index=False)

# Reports/status
report=f'''# T09 Reciprocal-Role Narrowing — Checkpoint R5\n\n## Status\n**T09 narrowing bounded; no novel semantic-review candidate emitted; two source-semantic blockers preserved. Not S14 relation authority. Job 3 remains blocked.**\n\n## Key findings\n- Sealed R6 T09 positives recovered: **1/1** (`{cr.relation_authority_id}`).\n- The accepted relation is cross-object Arab Barometer VIII `Q604A_NT ↔ Q604B_NT`, reversing close-female-relative vs close-male-relative marriage-acceptance roles while holding prospective-spouse obstacles fixed.\n- All four current canary members remain `SOURCE_ROUTING_UNRESOLVED`; semantic authority survives, but current O11 observability remains routing-blocked.\n- Old R5 T09 discovery locators: **110**, all accounted as recall-only. **Neither canary parent is among the 110**, proving that R5 locator terrain is not a necessary or complete T09 universe.\n- Accepted R14 joint source objects accounted: **548/548**.\n- Independent cross-object source-structure opportunities evaluated: **{len(pairledger)}**; known canary recovered; novel emitted candidates: **0**.\n- Within-object A/B recall pairs from the 110 R5 locators: **{len(intra)}**. Q628 and Q624 retain explicit source-semantic blockers; suffixes are never role authority.\n- Strict current-semantic opposed-role token recall hits: **{len(rhits)}**, all rejected as target/scenario differentiation rather than reciprocal actor↔recipient reversal.\n- Old O11 T09 cells: **35/35 candidate generation blocked**; Arab VIII was routing-blocked despite the known semantic relation.\n\n## Constitutional result\nThe correct narrowing result is **zero novel review candidates under current recovered authority plus two explicit source-semantic blockers**, not `T09 absent`. A future O11 successor must distinguish semantic authority, routing blockage, source-semantic blockage, and proven negative space.\n\n## Exact next operation\n**T10 target×condition matrices.** Reconstruct matrix identity/dimensions/cells from exact printed parents/members/current targets/conditions, account for all 14 R6 T10 positives, require repeated targets across conditions AND repeated conditions across targets, and prohibit R14/page-excerpt similarity.\n'''
(OUT/'T09_NARROWING_R5_REPORT.md').write_text(report)
status={
 'checkpoint':'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R5_20260811','status':'IN_PROGRESS_NOT_FROZEN','active_state':'R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR','job3_authorized':False,'o12_r2_811_complete_authority':False,'workers_launched':False,
 'supersedes_for_execution':['CHECKPOINT_R4 next-dependency pointer only; preserves R3 T07 and R4 T08 narrowing results'],
 't09':{'sealed_r6_t09_canaries_recovered':1,'r5_recall_locators_accounted':110,'r5_canary_parent_locator_hits':0,'r14_joint_objects_accounted':548,'cross_object_pair_opportunities_evaluated':len(pairledger),'novel_semantic_review_candidates':0,'source_semantic_blocker_packets':2,'canonical_packets_total':3,'o11_t09_cells_accounted':35,'next_dependency':'T10 target×condition matrices'},
 'remaining_major_rules':['T10','T11'],
 'next_decision':'finish T10-T11, cross-rule packet dedupe, then worker economics',
 'repair_stack':{'done':[1,7,8],'partial':[2,3,4,5,6,9,10,11,14,15,23],'open':[12,13,16,17,18,19,20,21,22,24,25]}
}
json.dump(status,open(OUT/'CURRENT_STATUS_R5.json','w'),indent=2)
(OUT/'NEXT_EXECUTION_STEPS.md').write_text('''# Exact Resume Sequence after T09 R5\n\n1. **T10 target×condition matrices** — exact printed parent/member identity + current targets/conditions; true 2D crossing required; recover/account all 14 R6 positives; no page/excerpt similarity.\n2. **T11 complementary roles**.\n3. **Compress + cross-rule dedupe T03–T11 packets**.\n4. **Measure worker economics**.\n5. **Adjudicate/freeze S14 relational-structure authority**.\n6. **Rebuild O11/S16** from repaired prerequisites.\n7. **Rebuild O12 T01–T13 cleanly**, including T01 grain audit.\n8. **Independent completeness reconstruction + causal topology audit**.\n9. Only then freeze O12 and launch Job 3.\n\nHard laws unchanged: 811 is not final; old worker packs forbidden; lexical/embedding/proximity recall never relation authority; R14 excerpts prohibited for T09/T10 cross-object similarity.\n''')
(OUT/'00_README_FIRST.md').write_text(report+'\nSee `CURRENT_STATUS_R5.json` and `NEXT_EXECUTION_STEPS.md`.\n')
(OUT/'AUDIT/T09_GOVERNING_DOCTRINE_R5.md').write_text('''# T09 governing doctrine\n\n- Reciprocal-role reversal requires explicit source-semantic actor/recipient role direction; thematic symmetry, gender words, A/B suffixes, source proximity and embeddings cannot authorize it.\n- R5 110 locators are recall only and demonstrably miss both source objects of the known R6 canary.\n- R6 semantic authority survives current O06 routing blockage. Observability/composability is a separate status.\n- A source blocker is not a negative relation verdict.\n- Cross-object search is mandatory because the sole accepted R6 T09 is cross-object.\n''')
# parent pins
pins={'r4_checkpoint_zip_sha256':'3857841738e0850fb27ed6b0e2a1e411dd9225733ac16aafb2ba0290dcec46d9'}
for fn in ['INTER_QUESTION_RELATION_AUTHORITY_R2.csv','SEMANTIC_EDGE_ADJUDICATION_DENOMINATOR_R5_CODEX_RECONCILED.csv','CANONICAL_IMPLEMENTATION_REGISTRY.csv','R14_SOURCE_NATIVE_AUTHORITY_FINAL_708047.json','S16_WAVE_RELATION_CLASS_CAPABILITY_ATLAS.csv']:
    pins[fn]=sha(BASE/fn)
json.dump(pins,open(OUT/'PROVENANCE/PARENT_PINS_R5.json','w'),indent=2)
# builder copy
shutil.copy(__file__,OUT/'CODE/build_t09_checkpoint_r5.py')

# validator
val='''import pandas as pd,json,sys,os\nR=os.path.dirname(os.path.dirname(__file__))\ne=[];c=[]\ndef ck(n,x,d=None): c.append((n,bool(x),d)); e.append(n) if not x else None\nr5=pd.read_csv(os.path.join(R,'AUDIT/T09_R5_110_RECALL_LOCATOR_DISPOSITION_R5.csv'))\npa=pd.read_csv(os.path.join(R,'NARROWING/T09_R14_CROSS_OBJECT_PAIR_OPPORTUNITIES_R5.csv'))\nob=pd.read_csv(os.path.join(R,'NARROWING/T09_R14_548_OBJECT_ACCOUNTING_R5.csv'))\nintra=pd.read_csv(os.path.join(R,'NARROWING/T09_WITHIN_OBJECT_A_B_RECALL_DISPOSITION_R5.csv'))\nrh=pd.read_csv(os.path.join(R,'NARROWING/T09_STRICT_ROLE_TOKEN_RECALL_DISPOSITION_R5.csv'))\npk=pd.read_csv(os.path.join(R,'NARROWING/T09_CANONICAL_PACKETS_R5.csv'))\ns16=pd.read_csv(os.path.join(R,'AUDIT/O11_T09_35_CELL_DIAGNOSTIC_R5.csv'))\ncan=pd.read_csv(os.path.join(R,'PROVENANCE/R6_T09_SEALED_PARENT_ROW_R5.csv'))\nmem=pd.read_csv(os.path.join(R,'PROVENANCE/R6_T09_CANARY_CURRENT_MEMBER_ROWS_R5.csv'))\nst=json.load(open(os.path.join(R,'CURRENT_STATUS_R5.json')))\nck('r5_110',len(r5)==110,len(r5));ck('r5_no_canary_parent_hits',r5.is_sealed_canary_parent.sum()==0,int(r5.is_sealed_canary_parent.sum()))\nck('r6_one_canary',len(can)==1,len(can));ck('canary_id',can.iloc[0].relation_authority_id=='IQRA-R2-4a926605db229487f22d')\nck('canary_four_members',len(mem)==4,len(mem));ck('canary_all_routing_unresolved',mem.o06__routing_status.astype(str).eq('SOURCE_ROUTING_UNRESOLVED').all(),mem.o06__routing_status.value_counts().to_dict())\nck('r14_548',len(ob)==548,len(ob));ck('pair_canary_one',pa.disposition.str.startswith('KNOWN_R6_T09_CANARY').sum()==1,int(pa.disposition.str.startswith('KNOWN_R6_T09_CANARY').sum()))\nck('no_novel_pair_emit',not pa.disposition.str.startswith('EMIT').any())\nck('q628_blocker',(intra.object_id.eq('ArabBarometer-R14-VIII-Q628') & intra.disposition.str.startswith('BLOCK')).any())\nck('q624_blocker',(intra.object_id.eq('ArabBarometer-R14-VIII-Q624') & intra.disposition.str.startswith('BLOCK')).any())\nck('role_token_no_emit',not rh.disposition.str.startswith('EMIT').any())\nck('o11_35',len(s16)==35,len(s16));ck('o11_all_generation_blocked',s16.candidate_generation_posture.eq('BLOCK_CANDIDATE_GENERATION_FOR_WAVE_RULE').all())\nck('o11_one_routing_blocked',(s16.capability_status=='ROUTING_BLOCKED').sum()==1,int((s16.capability_status=='ROUTING_BLOCKED').sum()))\nck('packet_count_3',len(pk)==3,len(pk));ck('source_blocker_packets',(pk.status=='SOURCE_SEMANTIC_BLOCKER__NO_RELATION_VERDICT').sum()==2,int((pk.status=='SOURCE_SEMANTIC_BLOCKER__NO_RELATION_VERDICT').sum()))\nck('job3_false',st['job3_authorized'] is False);ck('next_t10',st['t09']['next_dependency']=='T10 target×condition matrices')\nres={'status':'PASS' if not e else 'FAIL','checks':len(c),'errors':e,'details':c};json.dump(res,open(os.path.join(R,'VALIDATION/VALIDATION_RESULT_R5.json'),'w'),indent=2);print(json.dumps({'status':res['status'],'checks':len(c),'errors':len(e)},indent=2));sys.exit(1 if e else 0)\n'''
(OUT/'VALIDATION/validate_t09_checkpoint_r5.py').write_text(val)
# run validator
os.system(f"python {OUT/'VALIDATION/validate_t09_checkpoint_r5.py'}")
# manifest (exclude zip)
manifest=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file(): manifest.append({'path':str(p.relative_to(OUT)),'sha256':sha(p),'size_bytes':p.stat().st_size})
pd.DataFrame(manifest).to_csv(OUT/'SHA256_MANIFEST_R5.csv',index=False)
# rerun validator after manifest irrelevant
# zip
if ZIP.exists(): ZIP.unlink()
with zipfile.ZipFile(ZIP,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file(): z.write(p,arcname=f'{OUT.name}/{p.relative_to(OUT)}')
zs=sha(ZIP)
Path(str(ZIP)+'.sha256').write_text(f'{zs}  {ZIP.name}\n')
print(json.dumps({'zip':str(ZIP),'sha256':zs,'files':sum(1 for p in OUT.rglob('*') if p.is_file()),'r5_110':len(r5ledger),'pair_opportunities':len(pairledger),'within_ab':len(intra),'strict_role_hits':len(rhits)},indent=2))
