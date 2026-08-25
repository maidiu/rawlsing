from pathlib import Path
import pandas as pd, json, re, hashlib, csv, gzip, os, shutil, zipfile
from itertools import combinations
from collections import Counter, defaultdict

BASE=Path('/mnt/data/rawlsing_exec/o12r2')
OUT=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R9_20260811')
if OUT.exists(): shutil.rmtree(OUT)
for sub in ['AUDIT','PAIR_CENSUS','PROVENANCE','VALIDATION','CODE']:(OUT/sub).mkdir(parents=True,exist_ok=True)

cols=['question_implementation_id','source_family','wave','source_variable_code','exact_question_text',
      'sem__audit_unit_id','sem__semantic_summary','sem__measured_predicate','sem__target_entity_or_object',
      'sem__condition_time_horizon_or_qualifier','sem__proposition_subtype','sem__canonical_driver_id',
      'sem__canonical_facet_id','sem__canonical_component_id','sem__canonical_structural_domain_id',
      'sem__canonical_question_block_id','sem__block_kind','sem__canonical_relation_axis_id','sem__canonical_target_id',
      'sem__canonical_target_label','sem__canonical_condition_id','sem__canonical_condition_label','sem__canonical_role',
      'sem__coordinate_confidence','sem__semantic_only_anti_join','r14_object_ids_json','respondent_universe_status','routing_signal_status']
reg=pd.read_csv(BASE/'CANONICAL_IMPLEMENTATION_REGISTRY.csv',usecols=cols,low_memory=False)
r6=pd.read_csv(BASE/'INTER_QUESTION_RELATION_AUTHORITY_R2.csv',low_memory=False)
for c in reg.columns: reg[c]=reg[c].fillna('').astype(str)
sem=reg[reg.sem__audit_unit_id.ne('')].copy()

def first_nonblank(s):
    for x in s:
        x=str(x).strip()
        if x and x.lower()!='nan':return x
    return ''
def joinuniq(s):
    out=[]
    for x in s:
        x=str(x).strip()
        if x and x.lower()!='nan' and x not in out:out.append(x)
    return ' || '.join(out)
g=['source_family','wave','sem__audit_unit_id']
agg={c:first_nonblank for c in cols if c not in g+['question_implementation_id','source_variable_code','exact_question_text','r14_object_ids_json']}
agg.update(question_implementation_id=joinuniq,source_variable_code=joinuniq,exact_question_text=joinuniq,r14_object_ids_json=joinuniq)
uw=sem.groupby(g,dropna=False).agg(agg).reset_index()

# deterministic all-same-source-wave pair census
pair_path=OUT/'PAIR_CENSUS/ALL_SAME_SOURCE_WAVE_SEMANTIC_UNIT_PAIRS_R9.csv.gz'
fields=['pair_id','source_family','wave','unit_a','unit_b','codes_a','codes_b','role_a','role_b',
        'same_driver','same_facet','same_component','same_domain','same_block','same_axis','same_target','same_condition','same_predicate',
        'r14_overlap','lexical_role_recall_signal']
counts=Counter(); total=0
role_rx=re.compile(r'\b(principle|general|specific|application|apply|goal|end|means|mechanism|method|achiev|commit|duty|oblig|cost|pay|tax|price|income|sacrifice|burden|willing|conduct|behavior|behaviour|intend|expect|subtarget|institution|recipro|recipient|matrix|condition|role)\b',re.I)
with gzip.open(pair_path,'wt',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for (sf,wave),h in uw.groupby(['source_family','wave'],sort=True):
        rows=list(h.to_dict('records'))
        for a,b in combinations(rows,2):
            ua,ub=a['sem__audit_unit_id'],b['sem__audit_unit_id']
            if ub<ua:a,b=b,a;ua,ub=ub,ua
            def eq(c):
                x=str(a.get(c,'')).strip();y=str(b.get(c,'')).strip();return int(bool(x and y and x==y))
            r14a=set(re.findall(r'[A-Za-z0-9_\-]+',str(a.get('r14_object_ids_json',''))))
            r14b=set(re.findall(r'[A-Za-z0-9_\-]+',str(b.get('r14_object_ids_json',''))))
            txt=' '.join([a.get('sem__semantic_summary',''),a.get('exact_question_text',''),b.get('sem__semantic_summary',''),b.get('exact_question_text','')])
            flags={
                'same_driver':eq('sem__canonical_driver_id'),'same_facet':eq('sem__canonical_facet_id'),'same_component':eq('sem__canonical_component_id'),
                'same_domain':eq('sem__canonical_structural_domain_id'),'same_block':eq('sem__canonical_question_block_id'),'same_axis':eq('sem__canonical_relation_axis_id'),
                'same_target':eq('sem__canonical_target_id'),'same_condition':eq('sem__canonical_condition_id'),'same_predicate':eq('sem__measured_predicate'),
                'r14_overlap':int(bool(r14a & r14b)),'lexical_role_recall_signal':int(bool(role_rx.search(txt)))
            }
            key=f'{sf}|{wave}|{ua}|{ub}';pid='S14PAIR-'+hashlib.sha256(key.encode()).hexdigest()[:20]
            row={'pair_id':pid,'source_family':sf,'wave':wave,'unit_a':ua,'unit_b':ub,'codes_a':a.get('source_variable_code',''),'codes_b':b.get('source_variable_code',''),'role_a':a.get('sem__canonical_role',''),'role_b':b.get('sem__canonical_role',''),**flags}
            w.writerow(row);total+=1
            for k,v in flags.items():counts[k]+=v
            if any(flags.values()):counts['any_signal']+=1

# R6 T03-T11 pair-level canary coverage against census identity universe
rtypes=['GENERAL_PRINCIPLE_SPECIFIC_APPLICATION','GOAL_MEANS','COMMITMENT_PERSONAL_COST','NORM_EXPECTED_CONDUCT','GENERAL_TARGET_SUBTARGET','INSTITUTION_CLASS_DIFFERENTIATION','RECIPROCAL_ROLE_REVERSAL','TARGET_CONDITION_MATRIX','COMPLEMENTARY_ROLE_CONVERGENCE']
# implementation -> sem membership(s)
implmap=defaultdict(list)
for _,r in sem.iterrows(): implmap[r.question_implementation_id].append((r.source_family,str(r.wave),r.sem__audit_unit_id))
canrows=[]; all_ok=True
for _,r in r6[r6.relation_type.isin(rtypes)].iterrows():
    try: impls=json.loads(r.member_question_implementation_ids) if isinstance(r.member_question_implementation_ids,str) else []
    except: impls=[]
    mapped=[]
    for iid in impls:
        mapped += implmap.get(str(iid),[])
    # only matching the relation source/wave
    units=sorted(set(u for sf,w,u in mapped if sf==str(r.source_family) and w==str(r.wave)))
    expected_pairs=len(units)*(len(units)-1)//2
    ok=(len(units)>=2)
    all_ok &= ok
    canrows.append(dict(relation_authority_id=r.relation_authority_id,relation_type=r.relation_type,source_family=r.source_family,wave=r.wave,member_implementation_count=len(impls),mapped_semantic_unit_count=len(units),pair_census_pairs_implied=expected_pairs,coverage_status='COVERED_BY_COMPLETE_SOURCE_WAVE_PAIR_CENSUS' if ok else 'MAPPING_GAP_REQUIRES_EXPLICIT_REVIEW'))
pd.DataFrame(canrows).to_csv(OUT/'PROVENANCE/R6_T03_T11_PAIR_CENSUS_CANARY_COVERAGE_R9.csv',index=False)

summary={
 'semantic_unit_count_global':int(uw.sem__audit_unit_id.nunique()),
 'source_wave_semantic_membership_rows':int(len(uw)),
 'source_wave_group_count':int(uw.groupby(['source_family','wave']).ngroups),
 'all_same_source_wave_unordered_pairs':int(total),
 'signal_counts':{k:int(v) for k,v in counts.items()},
 'r6_t03_t11_relation_count':int(len(canrows)),
 'r6_pair_census_canary_mapping_all_have_at_least_two_units':bool(all_ok),
 'pair_census_role':'COMPLETE_BASE_UNIVERSE_FOR_CORRECTIVE_RULE_SPECIFIC_SCREENING__NOT_RELATION_AUTHORITY',
 'law':['Every same-source-wave semantic-unit pair is present exactly once.','Equality/lexical columns are recall and mechanical features only; none authorizes a relation.','Rule-specific T03-T11 eligibility/disposition must be built as a successor over this census plus sealed source/target/class/matrix authorities.']
}
json.dump(summary,open(OUT/'PAIR_CENSUS/PAIR_CENSUS_SUMMARY_R9.json','w'),indent=2)

# Mechanical revalidation results captured from the hostile pass
mechanical={
 'status':'PASS_BYTES_AND_PACKAGING__FAIL_PREMATURE_COMPLETENESS_PROMOTION',
 'checkpoints':{
  'R3':{'validator_checks':27,'manifest_files':14,'bad_manifest':0},
  'R4':{'validator_checks':27,'manifest_files':18,'bad_manifest':0},
  'R5':{'validator_checks':19,'manifest_files':18,'bad_manifest':0},
  'R6':{'validator_checks':12,'manifest_files':19,'bad_manifest':0},
  'R7':{'validator_checks':15,'manifest_files':16,'bad_manifest':0},
  'R8':{'validator_checks':30,'manifest_files':22,'bad_manifest':0},
  'R8_ADJUDICATION_FREEZE':{'validator_checks':13,'manifest_files':12,'bad_manifest':0},
  'R8C':{'validator_checks':9,'manifest_files':12,'bad_manifest':0}},
 'interpretation':'Artifact integrity is clean. The failure is epistemic: R8 promoted bounded/curated narrowing frontiers into a dispatch-complete denominator without satisfying repair item #14.'
}
json.dump(mechanical,open(OUT/'AUDIT/MECHANICAL_REVALIDATION_R9.json','w'),indent=2)

stack={
 'governing_checklist':'user 25-item full repair stack',
 'done':[1,7,8],
 'partial':[2,3,4,5,6,9,10,11,12,13,15,16,18,23],
 'open':[14,17,19,20,21,22,24,25],
 'corrections':{
  '9-13':'Previously crossed off too aggressively. Their checkpoints explicitly freeze narrowing frontiers, not final S14 authority; they return to PARTIAL until item 18 authority freeze.',
  '14':'REOPENED/OPEN. Global denominator-complete disposition proof was not established.',
  '16':'PARTIAL/REOPENED because cross-rule dedupe was applied to an incompletely proven input denominator.',
  '17':'REVOKED/OPEN. 66/53/13 worker economics is ancestry only until corrected denominator is proven.',
  '18':'PARTIAL. R8C central decisions are preserved as provisional adjudications requiring revalidation against corrected denominator.'}
}
json.dump(stack,open(OUT/'REPAIR_STACK_R9.json','w'),indent=2)

status={
 'checkpoint':'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R9_20260811',
 'status':'CORRECTIVE_HOSTILE_QA_IN_PROGRESS_NOT_FROZEN',
 'active_state':'R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR',
 'job3_authorized':False,'o12_r2_811_complete_authority':False,
 'r8_denominator_66_dispatch_authority':False,
 'r8_worker_packs_execution_status':'DO_NOT_EXECUTE__SUPERSEDED_FOR_DISPATCH_BY_R9_CORRECTIVE_DENOMINATOR_AUDIT',
 'r8c_central_decisions_status':'PRESERVE_AS_PROVISIONAL_SEMANTIC_ADJUDICATION_ANCESTRY__REVALIDATE_AFTER_R9_DENOMINATOR',
 'root_cause':'R8 mechanically validated its own bounded reconstruction/proxy/R14 surfaces but did not independently prove T03-T11 opportunity completeness. T03-T05 reconstruction was hand-curated; R3-R7 explicitly called their outputs bounded narrowing frontiers.',
 'corrective_base':summary,
 'next_dependency':'Build denominator-complete rule-specific T03-T11 opportunity/disposition ledgers over the 364,094-pair census plus governed non-pair structures; recompress/dedupe; remeasure worker economics; only then issue new worker packs.'
}
json.dump(status,open(OUT/'CURRENT_STATUS_R9.json','w'),indent=2)

report=f'''# R9 Hostile Postmortem — S14 denominator / dispatch correction\n\n## Verdict\n\n**Mechanical/package state: PASS.  R8 semantic-dispatch completeness claim: REVOKED.**\n\nThe hostile audit re-ran the validators/manifests for R3, R4, R5, R6, R7, R8, the R8 adjudication freeze, and R8C. All are byte/mechanically coherent. The defect is not corruption. It is a shared-assumption completeness error.\n\nR3–R7 explicitly describe themselves as **bounded narrowing frontiers, not final S14 authority**. R3 specifically says that no exclusion is proof outside its declared coverage and that global denominator-complete proof remains repair item #14. R8 nevertheless reconstructed T03–T05 with a hand-curated packet list, dispositioned the known O11 proxy groups and 596 R14 source objects, merged the bounded R3–R7 frontiers, then froze 66 unresolved packets and derived 53/13 worker economics. That leap was not justified.\n\n## Governance correction\n\n- Preserve R3–R7 narrowing artifacts and their valid canary/accounting findings.\n- Preserve R8 and its 66/53/13 result as diagnostic ancestry only.\n- **Do not execute W01–W04 R8 worker packs.** They are mechanically sound but denominator-incomplete.\n- Preserve R8C's 13 central decisions as provisional semantic adjudications; none is final S14 authority and all must be revalidated when the corrected denominator is known.\n- Job 3 remains blocked.\n\n## Independent denominator base installed in R9\n\nR9 now constructs the denominator from outside the candidate generator: the current semantic substrate contains **{summary['semantic_unit_count_global']:,} unique semantic units**, **{summary['source_wave_semantic_membership_rows']:,} source-wave semantic memberships**, across **{summary['source_wave_group_count']} source-wave groups**. Exhaustively enumerating every unordered within-source-wave pair yields **{summary['all_same_source_wave_unordered_pairs']:,} pairs**.\n\nThe pair file is `PAIR_CENSUS/ALL_SAME_SOURCE_WAVE_SEMANTIC_UNIT_PAIRS_R9.csv.gz`. Its equality/source-overlap/lexical columns are strictly retrieval or mechanical features. They do not authorize a relation.\n\nThis is the base from which T03–T11 rule-specific opportunity ledgers must now be built. Pair-based rules can no longer disappear because an earlier generator never looked at the pair. Matrix/hierarchy/class/source-structure rules must additionally use their governed non-pair substrates.\n\n## Repair-stack correction\n\nFully complete remains: **#1, #7, #8**.\n\nT07–T11 (#9–#13) are **narrowed but not authority-complete**, so they are PARTIAL, not crossed off. #14 is OPEN. #15/#16 are partial and require rerun after the corrected denominator. #17 worker economics is REVOKED/OPEN. #18 remains partial because R8C decisions exist but S14 cannot freeze yet.\n\n## Next exact operation\n\n1. Create rule-specific denominator-complete T03–T11 opportunity/disposition ledgers from the R9 pair census plus P2/P3 target hierarchy, T08 class substrate, source-parent structures, O04 endpoint authority, and exact matrix/source authorities.\n2. Require all sealed R6 T03–T11 positives as canaries and explicit negative-space accounting.\n3. Recompress into canonical packets and algorithmically cross-rule dedupe by exact evidence/member sets plus governed source-structure identity—not hand-coded packet names.\n4. Recompute worker economics.\n5. Only then generate successor worker packs and resume item #18.\n'''
open(OUT/'R9_HOSTILE_QA_REPORT.md','w').write(report)

rev='''# DO NOT EXECUTE — R8 adjudication denominator and worker packs\n\nR8's artifacts are mechanically valid ancestry but **are not dispatch-authoritative** after the R9 hostile audit.\n\nReason: the 66/53/13 denominator was derived from bounded/curated T03–T11 narrowing surfaces before global repair item #14 (denominator-complete disposition proof) had been satisfied.\n\n- Preserve R8 freeze and W01–W04 ZIPs unchanged for provenance.\n- Do not execute or reconcile them as the S14 adjudication denominator.\n- R8C central decisions remain provisional ancestry and must be revalidated.\n- Successor worker packs may be generated only after R9 denominator-complete reconstruction and new worker-economics measurement.\n'''
open(OUT/'R8_DISPATCH_REVOCATION.md','w').write(rev)

nextmd='''# Next execution steps — R9 corrective denominator audit\n\n1. Do not dispatch R8 W01–W04.\n2. Use `PAIR_CENSUS/ALL_SAME_SOURCE_WAVE_SEMANTIC_UNIT_PAIRS_R9.csv.gz` as the independent pair base.\n3. Build T03/T04/T05 rule-specific high-recall opportunity ledgers first; explicitly recover all 12 R6 T03–T05 canaries and account the earlier ~104/~1/~10 diagnostic frontier rather than replacing it with hand-selected packets.\n4. Re-audit T06–T11 against the same global item-#14 standard; preserve R2–R7 local results, but do not treat bounded exclusions as global absence.\n5. Add non-pair authorities where required: O04 endpoints for T06; P2/P3 hierarchy for T07; institution-class mapping for T08; exact actor/recipient/source-parent structures for T09; exact matrix/source structures for T10; exact role/common-proposition structures for T11.\n6. Every opportunity must map to candidate packet, known authority, mechanical exclusion with necessary-condition rationale, negative authority, explicit blocker, or source/routing gap.\n7. Compress and dedupe algorithmically by evidence/member/source-structure identity.\n8. Recompute worker economics; generate fresh packs only if the corrected denominator still warrants sharding.\n9. Reconcile preserved R8C decisions into successor S14 authority only after the corrected denominator is frozen.\n10. Job 3 remains blocked.\n'''
open(OUT/'NEXT_EXECUTION_STEPS.md','w').write(nextmd)

readme='''# README FIRST — R9 Hostile QA / dispatch revocation\n\nState: R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR. Job 3: NO.\n\nR9 supersedes R8 **only for completeness/dispatch claims**. R3–R8 and R8C remain immutable ancestry.\n\nRead in order: `CURRENT_STATUS_R9.json`, `R9_HOSTILE_QA_REPORT.md`, `R8_DISPATCH_REVOCATION.md`, `REPAIR_STACK_R9.json`, pair-census summary, then `NEXT_EXECUTION_STEPS.md`.\n'''
open(OUT/'00_README_FIRST.md','w').write(readme)

pointer='''# ACTIVE EXECUTION POINTER — R9 hostile QA correction\n\nActive state: `R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR`\n\nCurrent governing checkpoint: `CHECKPOINT_R9_20260811`.\n\nR8 66/53/13 review denominator: **REVOKED FOR DISPATCH; diagnostic ancestry only.**\nR8 W01–W04 packs: **DO NOT EXECUTE.**\nR8C central adjudications: **preserve provisionally; revalidate after corrected denominator.**\nJob 3: **NOT AUTHORIZED.**\n\nResume by building denominator-complete T03–T11 rule-specific opportunity ledgers over the R9 complete same-source-wave pair census plus governed non-pair source/target/endpoint structures.\n'''
open(OUT/'ACTIVE_EXECUTION_POINTER_R9.md','w').write(pointer)

# Copy builder itself
shutil.copy2('/mnt/data/build_r9_hostile_qa.py',OUT/'CODE/build_r9_hostile_qa.py')

# validator
val='''from pathlib import Path\nimport json,csv,gzip,hashlib,sys\nR=Path(__file__).resolve().parents[1]\nerrs=[];checks=[]\ndef ck(n,c,d=None):\n checks.append({'check':n,'pass':bool(c),'detail':d});\n if not c:errs.append(n)\ns=json.load(open(R/'CURRENT_STATUS_R9.json'))\nck('job3_false',s['job3_authorized'] is False)\nck('r8_dispatch_revoked',s['r8_denominator_66_dispatch_authority'] is False)\nck('packs_poisoned','DO_NOT_EXECUTE' in s['r8_worker_packs_execution_status'])\np=json.load(open(R/'PAIR_CENSUS/PAIR_CENSUS_SUMMARY_R9.json'))\nck('units_3324',p['semantic_unit_count_global']==3324,p['semantic_unit_count_global'])\nck('memberships_4565',p['source_wave_semantic_membership_rows']==4565,p['source_wave_semantic_membership_rows'])\nck('groups_35',p['source_wave_group_count']==35,p['source_wave_group_count'])\nck('pairs_364094',p['all_same_source_wave_unordered_pairs']==364094,p['all_same_source_wave_unordered_pairs'])\n# stream count + uniqueness\nseen=set();n=0;dupe=0\nwith gzip.open(R/'PAIR_CENSUS/ALL_SAME_SOURCE_WAVE_SEMANTIC_UNIT_PAIRS_R9.csv.gz','rt',encoding='utf-8',newline='') as f:\n for row in csv.DictReader(f):\n  n+=1; pid=row['pair_id']; dupe += pid in seen; seen.add(pid)\nck('pair_file_rows',n==364094,n);ck('pair_id_unique',dupe==0,dupe)\nst=json.load(open(R/'REPAIR_STACK_R9.json'))\nck('stack_done_exact',st['done']==[1,7,8],st['done'])\nck('item14_open',14 in st['open'])\nck('item17_open',17 in st['open'])\nck('items9_13_partial',all(x in st['partial'] for x in range(9,14)))\n# canary coverage file count = R6 T03-T11 relations 117\nwith open(R/'PROVENANCE/R6_T03_T11_PAIR_CENSUS_CANARY_COVERAGE_R9.csv',newline='',encoding='utf-8') as f: cr=list(csv.DictReader(f))\nck('r6_t03_t11_relations_117',len(cr)==117,len(cr))\nck('canary_mapping_status_nonblank',all(r['coverage_status'] for r in cr))\nres={'status':'PASS' if not errs else 'FAIL','check_count':len(checks),'errors':errs,'checks':checks}\njson.dump(res,open(R/'VALIDATION/VALIDATION_RESULT_R9.json','w'),indent=2)\nprint(json.dumps({'status':res['status'],'checks':len(checks),'errors':errs}))\nsys.exit(0 if not errs else 1)\n'''
open(OUT/'VALIDATION/validate_r9.py','w').write(val)
# run first validation before manifest
os.system(f"python3 '{OUT/'VALIDATION/validate_r9.py'}'")

# manifest excluding manifest itself and zip
manifest=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file() and p.name!='SHA256_MANIFEST_R9.csv':
        manifest.append((str(p.relative_to(OUT)),hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size))
with open(OUT/'SHA256_MANIFEST_R9.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['relative_path','sha256','size_bytes']);w.writerows(manifest)
# zip deterministic-ish standard
zip_path=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R9_20260811.zip')
if zip_path.exists():zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():z.write(p,arcname=str(p.relative_to(OUT)))
zh=hashlib.sha256(zip_path.read_bytes()).hexdigest()
open(str(zip_path)+'.sha256','w').write(f'{zh}  {zip_path.name}\n')
print(json.dumps({'out':str(OUT),'zip':str(zip_path),'sha256':zh,'manifest_files':len(manifest),'pairs':total,'canaries':len(canrows)},indent=2))
