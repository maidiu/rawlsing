from __future__ import annotations
import csv, json, hashlib, shutil, zipfile, os, re
from pathlib import Path
from collections import Counter, defaultdict
import pandas as pd

BASE=Path('/mnt/data/rawlsing_job3_r3')
R5_ROOT=Path('/mnt/data/rawlsing_r5/extracted/Rawlsing_DDM_Full_Project_Orientation_Root_20260812_R5')
O12_DIR=BASE/'o12'/'O12_T15_FINAL_R3'
O10_DIR=BASE/'o10'/'o10_t15_successor'
SRC_ROOT=BASE/'source'/'Rawlsing_SourceNative_Questionnaire_Structure_Authority_R1_20260812'
OUT=BASE/'launch_build'
PACKS=OUT/'PACKS'
CENTRAL=OUT/'CENTRAL'
if OUT.exists(): shutil.rmtree(OUT)
PACKS.mkdir(parents=True); CENTRAL.mkdir(parents=True)

R5_SHA='66972be2737b9fd524b48d0f33c94c1a739ed640fa704b18ddb4052559e0b3cc'
O12_SHA='33a56598f66f1e8d4596ddc4fec3ad686ec4cc7920ab76266b05470e1c7a3757'
O10_SHA='4575eb80995ea08625209acfdc82a1d5cf5bc9960b8184331e2949db2f2e4b65'
SOURCE_SHA='e88cc035ca1d846e68ee208ec991f61f636d67ebbd19312057c8e44c37ff740d'

DEN=O12_DIR/'O12_JOB3_CANDIDATE_DENOMINATOR_T15_SUCCESSOR_R3.csv'
df=pd.read_csv(DEN, dtype=str).fillna('')
assert len(df)==1264, len(df)
expected_rule_counts={'S14-T01':544,'S14-T02':29,'S14-T05':59,'S14-T06':4,'S14-T11':477,'S14-T12':72,'S14-T13':65,'S14-T15':14}
assert df['rule_id'].value_counts().to_dict()==expected_rule_counts, df['rule_id'].value_counts().to_dict()
assert df['candidate_id'].is_unique

def loads_list(s):
    try:
        x=json.loads(s)
        return x if isinstance(x,list) else []
    except Exception: return []

df['_member_count']=df['implementation_ids'].map(lambda s:len(loads_list(s)))
df['_pair_load']=df['_member_count'].map(lambda n:n*(n-1)//2)

def burden(row):
    n=int(row['_member_count']); rule=row['rule_id']
    if n>=8 or rule in {'S14-T06','S14-T15'}: return 'high'
    if n>=4 or rule in {'S14-T05','S14-T12','S14-T13'}: return 'medium'
    return 'low'
df['_review_burden_class']=df.apply(burden,axis=1)

# Family-coherent shards. This is execution economics only, not semantic authority.
SHARDS={
 'W01':['Asian Barometer'],
 'W02':['EVS'],
 'W03':['GSS'],
 'W04':['LiTS'],
 'W05':['Arab Barometer'],
 'W06':['WVS','Latinobarómetro','Afrobarometer','South Asia'],
}
all_fams=set(df.source_family.unique())
assert set(sum(SHARDS.values(),[]))==all_fams
assert len(sum(SHARDS.values(),[]))==len(all_fams)

# Build wave-dir lookup from exact metadata.
wave_dirs={}
for md in (SRC_ROOT/'BY_WAVE').glob('*/WAVE_METADATA.json'):
    d=json.loads(md.read_text())
    wave_dirs[(str(d['source_family']),str(d['wave']))]=md.parent

# Current source context table.
src_ctx=pd.read_csv(SRC_ROOT/'IMPLEMENTATION_SOURCE_CONTEXT_R1.csv',dtype=str).fillna('')
src_ctx_idx=src_ctx.set_index('question_implementation_id',drop=False)

# Current governed topology and current O12 provenance surfaces.
current_topology=O12_DIR/'O12_EXISTING_GOVERNED_RELATION_TOPOLOGY_R3.csv'
provenance_files=[
 'O12_CHANNEL_GENERATION_LEDGER_R3.csv',
 'O12_R16G_ROLE_PAIR_CANDIDATE_REPLAY_R3.csv',
 'O12_SOURCE_OBJECT_SEARCH_DISPOSITION_R3.csv',
 'O12_T06_SOURCE_FIRST_CANDIDATES_R3.csv',
 'O12_T15_SOURCE_FIRST_CANDIDATES_R3.csv',
 'O12_UPSTREAM_DEFECT_OR_SOURCE_OBLIGATIONS_R3.csv',
 'T01_GRAIN_AUDIT_R3.csv','T02_GRAIN_AUDIT_R3.csv',
 'O12_GOVERNED_POSITIVE_SUBSET_ANTI_JOIN_R3.csv',
]

# Central workload tables.
family_metrics=[]
for fam,g in df.groupby('source_family',sort=True):
    c=Counter(g['_review_burden_class'])
    family_metrics.append({
      'source_family':fam,'candidate_count':len(g),'member_instances':int(g['_member_count'].sum()),
      'pair_load_proxy':int(g['_pair_load'].sum()),'low':c['low'],'medium':c['medium'],'high':c['high'],
      **{f'rule_{r}':int((g.rule_id==r).sum()) for r in expected_rule_counts}
    })
pd.DataFrame(family_metrics).to_csv(CENTRAL/'JOB3_R3_WORKLOAD_BY_FAMILY.csv',index=False)

wave_rule=(df.groupby(['source_family','active_wave','rule_id']).size().reset_index(name='candidate_count'))
wave_rule.to_csv(CENTRAL/'JOB3_R3_WORKLOAD_BY_FAMILY_WAVE_RULE.csv',index=False)

# shard map and candidate allocation ledger
shard_rows=[]; alloc=[]
for wid,fams in SHARDS.items():
    g=df[df.source_family.isin(fams)].copy()
    c=Counter(g['_review_burden_class'])
    shard_rows.append({
      'worker_id':wid,'source_families':json.dumps(fams,ensure_ascii=False),'candidate_count':len(g),
      'member_instances':int(g['_member_count'].sum()),'pair_load_proxy':int(g['_pair_load'].sum()),
      'low':c['low'],'medium':c['medium'],'high':c['high'],
      'active_waves':json.dumps(sorted([str(x) for x in g.active_wave.unique()]),ensure_ascii=False),
      'rule_histogram':json.dumps(g.rule_id.value_counts().sort_index().to_dict(),sort_keys=True)
    })
    for cid in g.candidate_id: alloc.append({'candidate_id':cid,'worker_id':wid})
shard_map=pd.DataFrame(shard_rows)
shard_map.to_csv(CENTRAL/'JOB3_R3_SHARD_MAP.csv',index=False)
pd.DataFrame(alloc).sort_values('candidate_id').to_csv(CENTRAL/'JOB3_R3_CANDIDATE_ALLOCATION.csv',index=False)
assert len(alloc)==1264 and len({a['candidate_id'] for a in alloc})==1264

# Economics memo.
fm=pd.DataFrame(family_metrics).set_index('source_family')
lines=[
'# Job-3 R3 worker economics decision', '',
'Governing denominator: **1,264 immutable O12 R3 candidates**. Existing 638 governed positives are calibration/context, not novel workload.', '',
'## Decision',
'Use **six family-coherent shards**. The denominator is now almost twice the old 674-row terrain and has three large standalone families. Family coherence is preserved rather than splitting a family merely to equalize row counts. This is an execution choice only; it creates no semantic authority.', '',
'Workload diagnostics use candidate count, member instances, pair-load `n(n-1)/2`, and a transparent scheduling-only burden class. The burden class is not semantic truth: `high` = 8+ members or T06/T15; `medium` = 4–7 members or T05/T12/T13; otherwise `low`.', '',
'## Shards']
for r in shard_rows:
    lines.append(f"- **{r['worker_id']}**: {r['source_families']}; {r['candidate_count']} candidates; {r['member_instances']} member instances; pair-load {r['pair_load_proxy']}; low/medium/high = {r['low']}/{r['medium']}/{r['high']}.")
lines += ['', '## Guardrails',
'- Every R3 candidate appears in exactly one shard.',
'- No 674-row or 811-row candidate membership is reused.',
'- O12 R3 candidate membership is immutable; workers adjudicate exact candidate truth only.',
'- Native questionnaire/codebook text is source semantic/structural authority; implementation IDs are machine binding.',
'- Central Vozhd retains reconciliation, defect escalation, final relation-authority IDs, and hostile validation.',
'- APP-GATE A and respondent composability remain downstream; typed-edge absence must never erase empirical V550/V550J co-travel.'
]
(CENTRAL/'JOB3_R3_WORKER_ECONOMICS_DECISION.md').write_text('\n'.join(lines)+'\n')

state={
 'state_id':'R10K_JOB3_R3_LAUNCH_PHASE_A_COMPLETE',
 'repair_stack_item':25,
 'phase':'A_MEASURE_SHARD_AND_BUILD_FRESH_PACKS',
 'status':'PHASE_A_COMPLETE__JOB3_ADJUDICATION_NOT_YET_RETURNED',
 'orientation_r5_sha256':R5_SHA,'o12_r3_sha256':O12_SHA,'o10_t15_sha256':O10_SHA,'source_native_sha256':SOURCE_SHA,
 'candidate_count':1264,'existing_governed_positive_count':638,'visible_topology':1902,
 'rule_histogram':expected_rule_counts,'worker_count':len(SHARDS),'shards':shard_rows,
 'poison_law':'DO_NOT_EXECUTE_ANY_PRE_R3_JOB3_PACK; do not use 674/811 candidate membership.',
 'next_gate':'Execute six R3 Job-3 worker packs; central reconciliation/freeze follows only after all six PASS returns.'
}
(CENTRAL/'JOB3_R3_EXECUTION_STATE.json').write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n')

# Contract copy and launch guardrails in central.
shutil.copy2(BASE/'JOB3_ADJUDICATION_CONTRACT.md',CENTRAL/'JOB3_ADJUDICATION_CONTRACT.md')
shutil.copy2(R5_ROOT/'04_NEXT_EXECUTION'/'JOB3_LAUNCH_GUARDRAILS_R5.md',CENTRAL/'JOB3_LAUNCH_GUARDRAILS_R5.md')
shutil.copy2(O10_DIR/'S14_EXECUTABLE_GENERATION_GRAMMAR_R10K_T15.csv',CENTRAL/'CURRENT_O10_S14_RULE_GRAMMAR_R10K_T15.csv')
shutil.copy2(O10_DIR/'S14_T15_NORM_PRACTICAL_REALIZATION_CONTRACT_R1.md',CENTRAL/'S14_T15_NORM_PRACTICAL_REALIZATION_CONTRACT_R1.md')

return_cols=['candidate_id','worker_id','job3_disposition','accepted_relation_type','accepted_relation_label','member_roles_json','semantic_rationale','semantic_confidence','evidence_ceiling','prohibited_inference','blocker_code','blocker_detail','candidate_scope_defect_suspected','candidate_scope_defect_note','evidence_refs_json','worker_notes']

validator=r'''#!/usr/bin/env python3
import csv,json,sys
from pathlib import Path
root=Path(__file__).resolve().parent
assigned=list(csv.DictReader(open(root/'ASSIGNED_O12_R3_CANDIDATES.csv',encoding='utf-8-sig')))
ret=list(csv.DictReader(open(root/'JOB3_ADJUDICATION_RETURN.csv',encoding='utf-8-sig')))
manifest=json.load(open(root/'SHARD_MANIFEST.json',encoding='utf-8'))
wid=manifest['worker_id']
expected={r['candidate_id']:r for r in assigned}
errs=[]
if len(ret)!=len(assigned): errs.append(f'row_count {len(ret)} != {len(assigned)}')
ids=[r.get('candidate_id','') for r in ret]
if len(ids)!=len(set(ids)): errs.append('duplicate candidate_id in return')
missing=sorted(set(expected)-set(ids)); extra=sorted(set(ids)-set(expected))
if missing: errs.append(f'missing {len(missing)} candidate_ids; first={missing[:5]}')
if extra: errs.append(f'extra {len(extra)} candidate_ids; first={extra[:5]}')
for i,r in enumerate(ret,2):
    cid=r.get('candidate_id',''); disp=r.get('job3_disposition','').strip().upper()
    if r.get('worker_id','')!=wid: errs.append(f'line {i} wrong worker_id')
    if disp not in {'ACCEPT','REJECT','BLOCKED'}: errs.append(f'line {i} invalid disposition {disp!r}'); continue
    cand=expected.get(cid)
    if not cand: continue
    defect=r.get('candidate_scope_defect_suspected','').strip().lower()
    if defect not in {'true','false','yes','no','1','0'}: errs.append(f'line {i} invalid candidate_scope_defect_suspected')
    if defect in {'true','yes','1'} and not r.get('candidate_scope_defect_note','').strip(): errs.append(f'line {i} defect flag without note')
    if not r.get('semantic_rationale','').strip(): errs.append(f'line {i} missing semantic_rationale')
    if disp=='ACCEPT':
        if r.get('accepted_relation_type','').strip()!=cand['candidate_template_class']: errs.append(f'line {i} ACCEPT relation type must equal candidate_template_class')
        for col in ['member_roles_json','semantic_confidence','evidence_ceiling','prohibited_inference','evidence_refs_json']:
            if not r.get(col,'').strip(): errs.append(f'line {i} ACCEPT missing {col}')
        for col in ['member_roles_json','evidence_refs_json']:
            try: json.loads(r.get(col,''))
            except Exception: errs.append(f'line {i} invalid JSON in {col}')
    else:
        if r.get('accepted_relation_type','').strip(): errs.append(f'line {i} {disp} must not set accepted_relation_type')
    if disp=='REJECT' and not r.get('semantic_rationale','').strip(): errs.append(f'line {i} REJECT missing failed prerequisite rationale')
    if disp=='BLOCKED':
        if not r.get('blocker_code','').strip(): errs.append(f'line {i} BLOCKED missing blocker_code')
        if not r.get('blocker_detail','').strip(): errs.append(f'line {i} BLOCKED missing blocker_detail')
print(json.dumps({'worker_id':wid,'assigned':len(assigned),'returned':len(ret),'errors':errs[:100],'error_count':len(errs),'status':'PASS' if not errs else 'FAIL'},indent=2))
sys.exit(0 if not errs else 1)
'''

# copy/filter helper

def filter_csv_by_families(src:Path,dst:Path,fams):
    try:
        x=pd.read_csv(src,dtype=str).fillna('')
    except Exception:
        shutil.copy2(src,dst); return
    col='source_family' if 'source_family' in x.columns else None
    if col:
        x=x[x[col].isin(fams)]
    x.to_csv(dst,index=False)

# Build packs.
pack_records=[]
for wid,fams in SHARDS.items():
    g=df[df.source_family.isin(fams)].copy().sort_values(['source_family','active_wave','rule_id','candidate_id'])
    pack_name=f'Rawlsing_R10K_Job3_R3_{wid}_Execution_Pack_20260812'
    d=PACKS/pack_name; d.mkdir()

    # assigned candidates without internal scheduling columns
    outcols=[c for c in df.columns if not c.startswith('_')]
    g[outcols].to_csv(d/'ASSIGNED_O12_R3_CANDIDATES.csv',index=False)
    with open(d/'ASSIGNED_O12_R3_CANDIDATES.jsonl','w',encoding='utf-8') as f:
        for rec in g[outcols].to_dict('records'): f.write(json.dumps(rec,ensure_ascii=False,separators=(',',':'))+'\n')

    # candidate member -> current native-source binding
    rows=[]; missing_ctx=[]
    for _,r in g.iterrows():
        impls=loads_list(r['implementation_ids'])
        for pos,iid in enumerate(impls,1):
            base={'candidate_id':r['candidate_id'],'rule_id':r['rule_id'],'candidate_template_class':r['candidate_template_class'],
                  'source_family':r['source_family'],'active_wave':r['active_wave'],'member_position':pos,'question_implementation_id':iid}
            if iid in src_ctx_idx.index:
                sr=src_ctx_idx.loc[iid]
                if isinstance(sr,pd.DataFrame): sr=sr.iloc[0]
                base.update({k:sr[k] for k in src_ctx.columns if k!='question_implementation_id'})
            else:
                missing_ctx.append(iid)
            rows.append(base)
    mdf=pd.DataFrame(rows)
    mdf.to_csv(d/'CANDIDATE_MEMBER_SOURCE_CONTEXT_R1.csv',index=False)
    assert not missing_ctx, (wid,len(missing_ctx),missing_ctx[:5])

    # Core contracts and current authority.
    shutil.copy2(BASE/'JOB3_ADJUDICATION_CONTRACT.md',d/'JOB3_ADJUDICATION_CONTRACT.md')
    shutil.copy2(O10_DIR/'S14_EXECUTABLE_GENERATION_GRAMMAR_R10K_T15.csv',d/'CURRENT_O10_S14_RULE_GRAMMAR_R10K_T15.csv')
    shutil.copy2(O10_DIR/'S14_T15_NORM_PRACTICAL_REALIZATION_CONTRACT_R1.md',d/'S14_T15_NORM_PRACTICAL_REALIZATION_CONTRACT_R1.md')
    shutil.copy2(current_topology,d/'CURRENT_GOVERNED_POSITIVE_RELATION_TOPOLOGY_R3.csv')
    # Current O12 provenance filtered by assigned families where possible.
    provdir=d/'CURRENT_O12_R3_PROVENANCE'; provdir.mkdir()
    for fn in provenance_files:
        src=O12_DIR/fn
        if src.exists(): filter_csv_by_families(src,provdir/fn,fams)
    shutil.copy2(O12_DIR/'O12_FINAL_FREEZE_REPORT_R3.md',provdir/'O12_FINAL_FREEZE_REPORT_R3.md')
    shutil.copy2(O12_DIR/'VALIDATION_R3.json',provdir/'O12_VALIDATION_R3.json')

    # Family/wave-native authority. Copy exact flattened wave folders for waves present in this shard.
    snd=d/'SOURCE_NATIVE_AUTHORITY'; snd.mkdir()
    shutil.copy2(SRC_ROOT/'00_README_FIRST.md',snd/'00_README_FIRST.md')
    filter_csv_by_families(SRC_ROOT/'ACTIVE_35_WAVE_NATIVE_SOURCE_REGISTRY_R1.csv',snd/'ACTIVE_WAVE_NATIVE_SOURCE_REGISTRY_R1.csv',fams)
    filter_csv_by_families(SRC_ROOT/'SOURCE_DOCUMENT_REGISTRY_R1.csv',snd/'SOURCE_DOCUMENT_REGISTRY_R1.csv',fams)  # no source_family col -> full small registry
    by=snd/'BY_WAVE'; by.mkdir()
    wave_keys=sorted(set((str(a),str(b)) for a,b in zip(g.source_family,g.active_wave)))
    missing_wave=[]
    for key in wave_keys:
        srcdir=wave_dirs.get(key)
        if srcdir is None: missing_wave.append(key); continue
        shutil.copytree(srcdir,by/srcdir.name)
    assert not missing_wave,(wid,missing_wave)

    # Return template + validator.
    with open(d/'JOB3_ADJUDICATION_RETURN.csv','w',newline='',encoding='utf-8') as f: csv.writer(f).writerow(return_cols)
    (d/'validate_job3_return.py').write_text(validator)
    os.chmod(d/'validate_job3_return.py',0o755)

    c=Counter(g['_review_burden_class'])
    manifest={
      'worker_id':wid,'assigned_source_families':fams,'assigned_waves':[{'source_family':a,'wave':b} for a,b in wave_keys],
      'candidate_count':len(g),'candidate_id_sha256':hashlib.sha256('\n'.join(sorted(g.candidate_id)).encode()).hexdigest(),
      'unique_member_implementation_count':len(set(sum((loads_list(x) for x in g.implementation_ids),[]))),
      'member_instances':int(g['_member_count'].sum()),'pair_load_proxy':int(g['_pair_load'].sum()),
      'review_burden_class':{'low':c['low'],'medium':c['medium'],'high':c['high']},
      'rule_histogram':g.rule_id.value_counts().sort_index().to_dict(),
      'orientation_r5_sha256':R5_SHA,'o12_r3_release_sha256':O12_SHA,'o10_t15_release_sha256':O10_SHA,'source_native_authority_sha256':SOURCE_SHA,
      'candidate_membership_law':'ASSIGNED_O12_R3_CANDIDATES.csv is immutable membership. No pre-R3 candidate row or pack may be imported.',
      'semantic_authority_law':'Native official questionnaire/codebook text governs source meaning/structure; current O10 grammar governs relation semantics; machine IDs bind but do not manufacture meaning.',
      'return_filename':'JOB3_ADJUDICATION_RETURN.csv','return_validator':'validate_job3_return.py'
    }
    (d/'SHARD_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')

    readme=f'''# {wid} — Rawlsing Job-3 R3 execution pack\n\nYou are Job-3 Rabochii worker **{wid}**. This is a **fresh O12 R3 pack**. The immutable candidate denominator authority is SHA-256 `{O12_SHA}` and contains exactly **1,264** novel Job-3 candidates globally.\n\nAssigned families: {', '.join(fams)}. Assigned candidates: **{len(g)}**.\n\n## Mandatory read order\n1. `JOB3_ADJUDICATION_CONTRACT.md`\n2. `CURRENT_O10_S14_RULE_GRAMMAR_R10K_T15.csv`\n3. `SHARD_MANIFEST.json`\n4. `ASSIGNED_O12_R3_CANDIDATES.csv`\n5. `CANDIDATE_MEMBER_SOURCE_CONTEXT_R1.csv`\n6. `CURRENT_O12_R3_PROVENANCE/` as needed for current generation/provenance\n7. `CURRENT_GOVERNED_POSITIVE_RELATION_TOPOLOGY_R3.csv` as calibration/ancestry only\n8. `SOURCE_NATIVE_AUTHORITY/00_README_FIRST.md`, then the exact assigned `BY_WAVE/` source surfaces as needed\n9. For any T15 row, also read `S14_T15_NORM_PRACTICAL_REALIZATION_CONTRACT_R1.md`.\n\n## Hard laws\n- Return exactly one `ACCEPT`, `REJECT`, or `BLOCKED` row for every assigned `candidate_id`.\n- The exact O12 R3 candidate object is immutable. Do not split it, rescue a subset, add candidates, or alter membership.\n- **Do not use any pre-R3 674/811 Job-3 pack or old R15/C4/R16D candidate universe as candidate authority.**\n- Native questionnaire/codebook text is semantic/structural source authority. Machine labels/coordinates are binding and navigation, not a substitute for source meaning.\n- Topic, ideology, lexical/embedding similarity, same driver/facet, empirical V550 co-travel, or plausible causal stories do not establish typed relation truth.\n- A block is not a negative. Failure to prove is not proof of mismatch.\n- Routing/composability can constrain respondent computation without erasing semantic relation truth.\n- Existing 638 governed positives are context/calibration and are not novel workload.\n- Typed relation absence/block must never erase empirical V550/V550J attitude-cloud evidence.\n\n## Return\nFill `JOB3_ADJUDICATION_RETURN.csv`, then run:\n\n`python validate_job3_return.py`\n\nThe validator must report `PASS`. Zip the **entire completed worker directory** and return it to Vozhd. Do not assign final relation-authority IDs.\n'''
    (d/'00_README_FIRST.md').write_text(readme)

    # Payload manifest (excluding itself).
    payload=[]
    for p in sorted(x for x in d.rglob('*') if x.is_file() and x.name!='PAYLOAD_SHA256_MANIFEST.csv'):
        rel=p.relative_to(d).as_posix(); b=p.read_bytes()
        payload.append((rel,hashlib.sha256(b).hexdigest(),len(b)))
    with open(d/'PAYLOAD_SHA256_MANIFEST.csv','w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['relative_path','sha256','size_bytes']); w.writerows(payload)

    # Deterministic zip with fixed timestamps.
    zpath=PACKS/(pack_name+'.zip')
    with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in d.rglob('*') if x.is_file()):
            arc=(Path(pack_name)/p.relative_to(d)).as_posix()
            info=zipfile.ZipInfo(arc,date_time=(1980,1,1,0,0,0)); info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=(0o100644 & 0xFFFF)<<16
            z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    h=hashlib.sha256(zpath.read_bytes()).hexdigest()
    (PACKS/(zpath.name+'.sha256')).write_text(f'{h}  {zpath.name}\n')
    pack_records.append({'worker_id':wid,'zip_name':zpath.name,'sha256':h,'size_bytes':zpath.stat().st_size,'candidate_count':len(g)})

# Central validation and readme.
central_validation={
 'status':'PASS','candidate_count':len(df),'candidate_ids_unique':df.candidate_id.is_unique,
 'exact_rule_histogram_match':df.rule_id.value_counts().to_dict()==expected_rule_counts,
 'worker_count':len(SHARDS),'allocation_rows':len(alloc),'allocation_unique_candidate_ids':len({a['candidate_id'] for a in alloc}),
 'allocation_exact_denominator':set(a['candidate_id'] for a in alloc)==set(df.candidate_id),
 'family_partition_exact':set(sum(SHARDS.values(),[]))==all_fams,
 'fresh_pack_records':pack_records,
 'pre_r3_pack_content_imported':False,
 'source_native_member_context_missing':0,
}
(CENTRAL/'JOB3_R3_PHASE_A_VALIDATION.json').write_text(json.dumps(central_validation,indent=2,ensure_ascii=False)+'\n')
(CENTRAL/'00_README_FIRST.md').write_text(f'''# Rawlsing R10K Job-3 R3 launch — central Phase A\n\n**PASS.** Repair-stack #25 Phase A (measure → shard → fresh-pack build) is complete against O12 R3 SHA-256 `{O12_SHA}`.\n\n- Immutable denominator: **1,264** candidates.\n- Existing governed positives: **638** contextual authority, not re-adjudicated.\n- Fresh worker packs: **6**, family-coherent, exact-cover and disjoint.\n- Any pre-R3 674/811 pack remains **DO NOT EXECUTE**.\n- Job-3 semantic adjudication itself is **not yet complete** until all six validated returns are reconciled centrally.\n\nRead `JOB3_R3_WORKER_ECONOMICS_DECISION.md`, `JOB3_R3_SHARD_MAP.csv`, `JOB3_R3_EXECUTION_STATE.json`, and `JOB3_R3_PHASE_A_VALIDATION.json`.\n''')

# Include builder for reproducibility and exact denominator snapshot in central bundle.
shutil.copy2(BASE/'build_job3_r3_launch.py',CENTRAL/'build_job3_r3_launch.py')
shutil.copy2(DEN,CENTRAL/'O12_JOB3_CANDIDATE_DENOMINATOR_T15_SUCCESSOR_R3.csv')

# Manifest and central deterministic zip.
payload=[]
for p in sorted(x for x in CENTRAL.rglob('*') if x.is_file() and x.name!='PAYLOAD_SHA256_MANIFEST.csv'):
    b=p.read_bytes(); payload.append((p.relative_to(CENTRAL).as_posix(),hashlib.sha256(b).hexdigest(),len(b)))
with open(CENTRAL/'PAYLOAD_SHA256_MANIFEST.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['relative_path','sha256','size_bytes']); w.writerows(payload)
central_name='Rawlsing_R10K_Job3_R3_Launch_PhaseA_Central_20260812'
central_zip=OUT/(central_name+'.zip')
with zipfile.ZipFile(central_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(x for x in CENTRAL.rglob('*') if x.is_file()):
        arc=(Path(central_name)/p.relative_to(CENTRAL)).as_posix(); info=zipfile.ZipInfo(arc,date_time=(1980,1,1,0,0,0)); info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=(0o100644 & 0xFFFF)<<16
        z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
ch=hashlib.sha256(central_zip.read_bytes()).hexdigest(); (OUT/(central_zip.name+'.sha256')).write_text(f'{ch}  {central_zip.name}\n')
print(json.dumps({'central_zip':str(central_zip),'central_sha256':ch,'validation':central_validation},indent=2,ensure_ascii=False))
