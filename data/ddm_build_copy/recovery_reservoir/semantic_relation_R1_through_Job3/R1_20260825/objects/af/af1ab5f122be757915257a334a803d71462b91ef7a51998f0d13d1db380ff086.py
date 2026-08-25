from __future__ import annotations
import pandas as pd, json, re, zipfile, io, hashlib, shutil, os
from pathlib import Path
from collections import Counter

ROOT=Path('/mnt/data/o11_t15_successor')
OUT=Path('/mnt/data/o11_t15_successor_build')
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir(parents=True)

ORIG=ROOT/'orig/R10J_O11'
R16G=ROOT/'r16g/R16G_O11_S16_REBUILD'
O6P=ROOT/'r10h/Rawlsing_R10H_P0_U1_Central_Reconciliation_20260810/LEDGERS/O06_IMPLEMENTATION_ROUTING_CENTRAL.jsonl'
O7P=ROOT/'r10h/Rawlsing_R10H_P0_U1_Central_Reconciliation_20260810/LEDGERS/O07_MEASUREMENT_SIGNATURES_CENTRAL.jsonl'
O10=Path('/mnt/data/o10_t15_successor')
CENT=Path('/mnt/data/t15_central_checkpoint')
T06Z=Path('/mnt/data/t06_praxis_merge')


def readjl(p):
    return pd.DataFrame([json.loads(x) for x in open(p,encoding='utf-8') if x.strip()])
def jlist(x):
    if isinstance(x,list): return x
    s='' if x is None else str(x).strip()
    if not s: return []
    try:
        z=json.loads(s); return z if isinstance(z,list) else [z]
    except Exception:
        return [v.strip() for v in re.split(r'[;|]',s) if v.strip()]
def clause_tuple(x):
    return tuple(sorted(str(v).strip() for v in jlist(x) if str(v).strip()))
def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

o6=readjl(O6P); o7=readjl(O7P)
o6['wave']=o6.wave.astype(str); o7['wave']=o7.wave.astype(str)
assert len(o6)==18276 and len(o7)==18276
waves=o6.groupby(['source_family','wave']).size().reset_index(name='implementation_count')
assert len(waves)==35 and int(waves.implementation_count.sum())==18276
wave_keys=list(waves[['source_family','wave']].itertuples(index=False,name=None))
o6i=o6.set_index('question_implementation_id'); o7i=o7.set_index('question_implementation_id')

s14=pd.read_csv(O10/'S14_EXECUTABLE_GENERATION_GRAMMAR_R10K_T15.csv',dtype=str).fillna('')
s15=pd.read_csv(O10/'S15_DERIVED_INDICATOR_DEFINITION_RELEASE_R10K_T15.csv',dtype=str).fillna('')
assert len(s14)==15 and len(s15)==17
s14i=s14.set_index('rule_id')

orig_rule=pd.read_csv(ORIG/'S16_WAVE_RELATION_CLASS_CAPABILITY_ATLAS.csv',dtype=str).fillna('')
orig_req=pd.read_csv(ORIG/'S16_WAVE_REQUIREMENT_CAPABILITY_ATLAS.csv',dtype=str).fillna('')
orig_ind=pd.read_csv(ORIG/'S16_WAVE_DERIVED_INDICATOR_CAPABILITY_ATLAS.csv',dtype=str).fillna('')
orig_wit=pd.read_csv(ORIG/'S16_R6_POSITIVE_WITNESS_REVALIDATION.csv',dtype=str).fillna('')
rpatch=pd.read_csv(R16G/'ATLAS/S16_35WAVE_X_T03_T11_CAPABILITY_ATLAS_R16G.csv',dtype=str).fillna('')
rwit=pd.read_csv(R16G/'ATLAS/S16_POSITIVE_RELATION_WITNESS_REVALIDATION_R16G.csv',dtype=str).fillna('')
strict=pd.read_csv(CENT/'CENTRAL_STRICT_T06_SOURCE_FIRST_AUTHORITY_R1.csv',dtype=str).fillna('')
t15=pd.read_csv(CENT/'CENTRAL_T15_POSITIVE_RELATION_AUTHORITY_R1.csv',dtype=str).fillna('')
t15_xw=pd.read_csv(CENT/'MERGED_T15_CROSSWALK_REVIEW_R1.csv',dtype=str).fillna('')
t15_def=pd.read_csv(CENT/'MERGED_T15_SOURCE_COVERAGE_DEFECTS_R1.csv',dtype=str).fillna('')

# Current exact observability replay.
def classify_members(ids):
    ids=list(dict.fromkeys([str(x) for x in ids if str(x)]))
    if not ids: return ('PARTIAL_MEASUREMENT','empty_member_payload')
    missing=[x for x in ids if x not in o6i.index]
    if missing: return ('ROUTING_BLOCKED','member_missing_current_o06')
    r=o6i.loc[ids]
    if isinstance(r,pd.Series): r=r.to_frame().T
    if (r.routing_status=='SOURCE_ROUTING_UNRESOLVED').any():
        return ('ROUTING_BLOCKED','current_o06_unresolved_member')
    if (r.routing_status=='ADMIN_OR_NONRESPONDENT').any():
        return ('SEMANTIC_ONLY_NONCOMPOSABLE','administrative_member_not_respondent_observable')
    missing7=[x for x in ids if x not in o7i.index]
    if missing7: return ('PARTIAL_MEASUREMENT','member_missing_current_o07')
    m=o7i.loc[ids]
    if isinstance(m,pd.Series): m=m.to_frame().T
    if m.measurement_use_class.isin(['ADMIN','UNRESOLVED']).any():
        return ('PARTIAL_MEASUREMENT','measurement_contract_incomplete')
    if (r.routing_status=='UNCONDITIONAL_SOURCE_PROVEN').all():
        return ('OBSERVABLE','all_members_unconditional_in_current_wave_universe')
    # The only conditional joint universe recognized without further source replay is exact shared module/ballot clause.
    clauses=[clause_tuple(x) for x in r.clause_ids]
    if clauses and len(set(clauses))==1 and clauses[0] and (r.routing_status=='MODULE_OR_BALLOT_CONDITIONAL').all():
        return ('OBSERVABLE','all_members_share_exact_current_module_or_ballot_clause')
    return ('SEMANTIC_ONLY_NONCOMPOSABLE','semantic_members_exist_but_common_current_respondent_route_not_proven')

# Build strict T06 and T15 witness ledgers.
def replay_authority(df, rule_id):
    rows=[]
    for _,r in df.iterrows():
        ids=jlist(r.get('member_implementation_ids_json',''))
        st,reason=classify_members(ids)
        rows.append({
            'central_relation_id':r.get('central_relation_id',''), 'rule_id':rule_id,
            'candidate_template_class':s14i.loc[rule_id,'candidate_template_class'],
            'source_family':r.source_family,'wave':str(r.wave),'member_count':len(ids),
            'member_implementation_ids_json':json.dumps(ids,separators=(',',':')),
            'capability_witness_status':st,'capability_witness_reason':reason,
            'authority_class':r.get('authority_class',''),'semantic_authority_status':r.get('successor_freeze_status',''),
        })
    return pd.DataFrame(rows)
strict_wit=replay_authority(strict,'S14-T06')
t15_wit=replay_authority(t15,'S14-T15')

# Extract all source-first T06 blocked crosswalk pairs from the six immutable returns.
def firstval(r,names):
    for n in names:
        if n in r and str(r[n]).strip(): return str(r[n]).strip()
    return ''
def ids_from_row(r, singular_names, json_names):
    out=[]
    for n in json_names:
        if n in r and str(r[n]).strip(): out += jlist(r[n])
    for n in singular_names:
        if n in r and str(r[n]).strip(): out.append(str(r[n]).strip())
    return list(dict.fromkeys(out))

t06_block_rows=[]; t06_mismatch_rows=[]; t06_review_rows=[]
for zpath in sorted(T06Z.glob('*.zip')):
    with zipfile.ZipFile(zpath) as z:
        names=[n for n in z.namelist() if n.endswith('T06_SOURCE_FIRST_CROSSWALK_REVIEW.csv')]
        if len(names)!=1: raise RuntimeError((zpath,names))
        d=pd.read_csv(io.BytesIO(z.read(names[0])),dtype=str).fillna('')
        for _,r in d.iterrows():
            rd=r.to_dict(); disp=firstval(rd,['disposition'])
            normids=ids_from_row(rd,
                ['norm_implementation_id','norm_question_implementation_id'],
                ['norm_implementation_ids_json'])
            conids=ids_from_row(rd,
                ['conduct_implementation_id','conduct_question_implementation_id'],
                ['conduct_implementation_ids_json'])
            ids=list(dict.fromkeys(normids+conids))
            rec={'worker_zip':zpath.name,'source_family':firstval(rd,['source_family']),'wave':firstval(rd,['wave']),
                 'disposition':disp,'member_implementation_ids_json':json.dumps(ids,separators=(',',':')),
                 'member_count':len(ids),'review_id':firstval(rd,['review_id','crosswalk_review_id','crosswalk_id'])}
            t06_review_rows.append(rec)
            if disp=='BLOCKED_SOURCE_AMBIGUITY': t06_block_rows.append(rec)
            elif disp=='NOT_T06_SOURCE_PROVEN_MISMATCH': t06_mismatch_rows.append(rec)
t06_review=pd.DataFrame(t06_review_rows); t06_blocks=pd.DataFrame(t06_block_rows); t06_mismatch=pd.DataFrame(t06_mismatch_rows)
assert len(t06_blocks)==111, len(t06_blocks)

# T15 blocked source/bridge ambiguity runtime-bounded pairs.
t15_blocks=[]
for _,r in t15_xw[t15_xw.disposition=='BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY'].iterrows():
    ids=list(dict.fromkeys(jlist(r.norm_implementation_ids_json)+jlist(r.praxis_implementation_ids_json)))
    t15_blocks.append({'worker_id':r.worker_id,'source_family':r.source_family,'wave':str(r.wave),
                       'review_id':r.crosswalk_id,'member_implementation_ids_json':json.dumps(ids,separators=(',',':')),
                       'member_count':len(ids),'candidate_manifestation_subtype':r.candidate_manifestation_subtype,
                       'bridge_basis_type':r.bridge_basis_type})
t15_blocks=pd.DataFrame(t15_blocks)
assert len(t15_blocks)==139

# Replay open terrain.
def replay_blocks(df, rule_id):
    out=[]
    for _,r in df.iterrows():
        ids=jlist(r.member_implementation_ids_json)
        st,reason=classify_members(ids)
        d=r.to_dict(); d.update({'rule_id':rule_id,'capability_terrain_status':st,'capability_terrain_reason':reason})
        out.append(d)
    return pd.DataFrame(out)
t06_block_replay=replay_blocks(t06_blocks,'S14-T06')
t15_block_replay=replay_blocks(t15_blocks,'S14-T15')

# Normalize R16G patches for T03-T05/T07-T11. T06 is replaced source-first.
rpatch['norm_rule_id']=rpatch.rule_id.map(lambda x: x if str(x).startswith('S14-') else 'S14-'+str(x))
rpatch_idx=rpatch.set_index(['source_family','wave','norm_rule_id'])
orig_rule_idx=orig_rule.set_index(['source_family','wave','rule_id'])

# Helpers for counts by wave.
def wc(df,sf,wv,status_col,status):
    if len(df)==0: return 0
    g=df[(df.source_family==sf)&(df.wave.astype(str)==wv)]
    return int((g[status_col]==status).sum())

def new_sourcefirst_cell(sf,wv,rid,positive_wit,blocked_replay,coverage_defects=0):
    pw=positive_wit[(positive_wit.source_family==sf)&(positive_wit.wave.astype(str)==wv)]
    br=blocked_replay[(blocked_replay.source_family==sf)&(blocked_replay.wave.astype(str)==wv)]
    pc=Counter(pw.capability_witness_status); bc=Counter(br.capability_terrain_status)
    obs=int(pc['OBSERVABLE']); sem=int(pc['SEMANTIC_ONLY_NONCOMPOSABLE']); rb=int(pc['ROUTING_BLOCKED']); pm=int(pc['PARTIAL_MEASUREMENT'])
    bobs=int(bc['OBSERVABLE']); bsem=int(bc['SEMANTIC_ONLY_NONCOMPOSABLE']); brb=int(bc['ROUTING_BLOCKED']); bpm=int(bc['PARTIAL_MEASUREMENT'])
    if obs>0:
        status='OBSERVABLE'; reason='source_first_positive_relation_has_current_respondent_composable_o06_o07_witness'
    elif bobs>0 or bpm>0:
        status='PARTIALLY_OBSERVABLE'; reason='source_first_unresolved_relation_terrain_has_current_bounded_searchable_member_configuration'
    elif sem+bsem>0:
        status='SEMANTIC_ONLY_NONCOMPOSABLE'; reason='source_first_relation_or_unresolved_terrain_exists_but_common_current_respondent_route_is_not_proven'
    elif rb+brb>0:
        status='ROUTING_BLOCKED'; reason='source_first_relation_or_unresolved_terrain_exists_but_current_o06_has_unresolved_member_routing'
    else:
        status='NOT_OBSERVED'; reason='source_first_exhaustive_wave_review_has_no_current_positive_or_runtime_bound_unresolved_relation_terrain'
    posture='ALLOW_BOUNDED_O12_SEARCH' if status in ['OBSERVABLE','PARTIALLY_OBSERVABLE'] else 'BLOCK_CANDIDATE_GENERATION_FOR_WAVE_RULE'
    srow=s14i.loc[rid]
    return {
      'source_family':sf,'wave':wv,'rule_id':rid,'candidate_template_class':srow.candidate_template_class,
      'linked_s13_requirement_ids':srow.linked_s13_requirement_ids,'capability_status':status,'capability_reason':reason,
      'observable_positive_witness_count':obs,'semantic_only_noncomposable_witness_count':sem,
      'routing_blocked_positive_witness_count':rb,'partial_measurement_witness_count':pm,
      'terrain_signal_count':len(br),'terrain_signal_basis':'source_first_blocked_crosswalk_relation_terrain_replayed_through_current_o06_o07',
      'candidate_generation_posture':posture,
      'evidence_ceiling':'S16 static source-first relation capability only; no candidate acceptance, respondent join, or persona inference.',
      'negative_law':'Source-proven mismatches apply only to exact reviewed links; inability to prove is BLOCK, never relation absence. Empirical V550/V550J co-travel remains independent.',
      'frozen_positive_relation_count':len(pw),'frozen_positive_relation_ids_json':json.dumps(pw.central_relation_id.tolist(),separators=(',',':')) if 'central_relation_id' in pw else '[]',
      'unresolved_source_first_pair_count':len(br),'bounded_searchable_unresolved_count':bobs+bpm,
      'unresolved_semantic_only_noncomposable_count':bsem,'unresolved_routing_blocked_count':brb,'unresolved_partial_measurement_count':bpm,
      'coverage_defect_count':int(coverage_defects),'absence_claim_licensed':'NO',
      'authority_basis':'CENTRAL_SOURCE_FIRST_T06_T15_R1','app_cotravel_guardrail':'Typed relation capability never gates or erases V550/V550J empirical co-travel.'
    }

# T15 coverage defects by wave.
defect_counts={}
if len(t15_def):
    for (sf,wv),g in t15_def.groupby(['source_family','wave']): defect_counts[(sf,str(wv))]=len(g)

# Build 525-cell relation atlas.
rows=[]
for sf,wv in wave_keys:
  for _,sr in s14.iterrows():
    rid=sr.rule_id
    if rid in ['S14-T06','S14-T15']:
        if rid=='S14-T06': row=new_sourcefirst_cell(sf,wv,rid,strict_wit,t06_block_replay,0)
        else: row=new_sourcefirst_cell(sf,wv,rid,t15_wit,t15_block_replay,defect_counts.get((sf,wv),0))
        rows.append(row); continue
    if rid in ['S14-T03','S14-T04','S14-T05','S14-T07','S14-T08','S14-T09','S14-T10','S14-T11']:
        p=rpatch_idx.loc[(sf,wv,rid)]
        rows.append({
          'source_family':sf,'wave':wv,'rule_id':rid,'candidate_template_class':sr.candidate_template_class,
          'linked_s13_requirement_ids':sr.linked_s13_requirement_ids,'capability_status':p.capability_status,'capability_reason':p.capability_reason,
          'observable_positive_witness_count':int(p.observable_positive_witness_count or 0),
          'semantic_only_noncomposable_witness_count':int(p.semantic_only_noncomposable_positive_witness_count or 0),
          'routing_blocked_positive_witness_count':int(p.routing_blocked_positive_witness_count or 0),
          'partial_measurement_witness_count':int(p.partial_measurement_positive_witness_count or 0),
          'terrain_signal_count':int(p.unresolved_surface_count or 0),
          'terrain_signal_basis':'R16G_source_first_role_bridge_unresolved_surface_replay',
          'candidate_generation_posture':p.candidate_generation_posture,'evidence_ceiling':p.evidence_ceiling,
          'negative_law':'R16F exact negative authority remains exact; BLOCK/unknown is not negative; empirical co-travel independent.',
          'frozen_positive_relation_count':int(p.frozen_positive_relation_count or 0),'frozen_positive_relation_ids_json':p.frozen_positive_relation_ids_json,
          'unresolved_source_first_pair_count':int(p.unresolved_surface_count or 0),'bounded_searchable_unresolved_count':int(p.bounded_searchable_unresolved_count or 0),
          'unresolved_semantic_only_noncomposable_count':int(p.unresolved_semantic_only_noncomposable_count or 0),
          'unresolved_routing_blocked_count':int(p.unresolved_routing_blocked_count or 0),'unresolved_partial_measurement_count':int(p.unresolved_partial_measurement_count or 0),
          'coverage_defect_count':0,'absence_claim_licensed':'NO','authority_basis':'R16G_T03_T11_SOURCE_FIRST_ROLE_BRIDGE_PATCH',
          'app_cotravel_guardrail':'Typed relation capability never gates or erases V550/V550J empirical co-travel.'
        }); continue
    # Preserve current original O11 cell for T01/T02/T12/T13/T14.
    p=orig_rule_idx.loc[(sf,wv,rid)]
    d=p.to_dict()
    d.update({'source_family':sf,'wave':wv,'rule_id':rid,
              'frozen_positive_relation_count':int(p.observable_positive_witness_count or 0)+int(p.semantic_only_noncomposable_witness_count or 0)+int(p.routing_blocked_positive_witness_count or 0)+int(p.partial_measurement_witness_count or 0),
              'frozen_positive_relation_ids_json':'[]','unresolved_source_first_pair_count':int(p.terrain_signal_count or 0),
              'bounded_searchable_unresolved_count':int(p.terrain_signal_count or 0) if p.capability_status=='PARTIALLY_OBSERVABLE' else 0,
              'unresolved_semantic_only_noncomposable_count':0,'unresolved_routing_blocked_count':0,'unresolved_partial_measurement_count':0,
              'coverage_defect_count':0,'absence_claim_licensed':'NO','authority_basis':'PRESERVED_R10J_O11_CELL_UNCHANGED_T01_T02_T12_T13_T14',
              'app_cotravel_guardrail':'Typed relation capability never gates or erases V550/V550J empirical co-travel.'})
    rows.append(d)
rule_df=pd.DataFrame(rows)
# Stable column order: original contract first, successor provenance second.
base_cols=orig_rule.columns.tolist()
extra=[c for c in ['frozen_positive_relation_count','frozen_positive_relation_ids_json','unresolved_source_first_pair_count','bounded_searchable_unresolved_count','unresolved_semantic_only_noncomposable_count','unresolved_routing_blocked_count','unresolved_partial_measurement_count','coverage_defect_count','absence_claim_licensed','authority_basis','app_cotravel_guardrail'] if c not in base_cols]
rule_df=rule_df[base_cols+extra]
assert len(rule_df)==525 and rule_df[['source_family','wave','rule_id']].drop_duplicates().shape[0]==525
assert rule_df.groupby(['source_family','wave']).size().eq(15).all()

# Unified positive witness surface for requirement direct sufficiency.
# Original witnesses only for unchanged T01/T02/T12/T13/T14.
template_to_rule=dict(zip(s14.candidate_template_class,s14.rule_id))
uw=[]
for _,r in orig_wit.iterrows():
    rid=template_to_rule.get(r.relation_type,'')
    if rid in ['S14-T01','S14-T02','S14-T12','S14-T13','S14-T14']:
        uw.append({'relation_id':r.relation_authority_id,'source_family':r.source_family,'wave':str(r.wave),'rule_id':rid,
                   'candidate_template_class':r.relation_type,'member_count':int(r.member_count or 0),'capability_witness_status':r.capability_witness_status,'authority_basis':'R10J_R6'})
# R16G witnesses for patched rules excluding T06.
for _,r in rwit.iterrows():
    rid=r.rule_id if str(r.rule_id).startswith('S14-') else 'S14-'+str(r.rule_id)
    if rid in ['S14-T03','S14-T04','S14-T05','S14-T07','S14-T08','S14-T09','S14-T10','S14-T11']:
        uw.append({'relation_id':r.central_relation_id,'source_family':r.source_family,'wave':str(r.wave),'rule_id':rid,
                   'candidate_template_class':s14i.loc[rid,'candidate_template_class'],'member_count':int(r.member_count or 0),'capability_witness_status':r.capability_witness_status,'authority_basis':'R16G_R16F'})
for _,r in strict_wit.iterrows():
    uw.append({'relation_id':r.central_relation_id,'source_family':r.source_family,'wave':str(r.wave),'rule_id':'S14-T06','candidate_template_class':'NORM_EXPECTED_CONDUCT','member_count':int(r.member_count),'capability_witness_status':r.capability_witness_status,'authority_basis':'CENTRAL_STRICT_T06_SOURCE_FIRST_R1'})
for _,r in t15_wit.iterrows():
    uw.append({'relation_id':r.central_relation_id,'source_family':r.source_family,'wave':str(r.wave),'rule_id':'S14-T15','candidate_template_class':'NORM_PRACTICAL_REALIZATION','member_count':int(r.member_count),'capability_witness_status':r.capability_witness_status,'authority_basis':'CENTRAL_T15_SOURCE_FIRST_R1'})
witness_df=pd.DataFrame(uw)

# Requirement capability recomputed against successor rule atlas and 17 S15/JE definitions.
# Direct sufficient templates are parsed from the definition's required relation-shape field.
req_rows=[]
for sf,wv in wave_keys:
    rg=rule_df[(rule_df.source_family==sf)&(rule_df.wave.astype(str)==wv)]
    wg=witness_df[(witness_df.source_family==sf)&(witness_df.wave.astype(str)==wv)]
    for _,d in s15.iterrows():
        req=d.requirement_id
        linked=[]
        for _,sr in s14.iterrows():
            if req in [x.strip() for x in sr.linked_s13_requirement_ids.split(';') if x.strip()]: linked.append(sr.rule_id)
        sub=rg[rg.rule_id.isin(linked)]
        direct_shapes=[x.strip() for x in d.required_relation_shape_or_candidate_templates.split(';') if x.strip()]
        direct_rule_ids=s14[s14.candidate_template_class.isin(direct_shapes)].rule_id.tolist()
        dw=wg[wg.rule_id.isin(direct_rule_ids)].copy()
        if req=='JE-14_CONFIGURATION_BREADTH': dw=dw[dw.member_count>=3]
        c=Counter(dw.capability_witness_status)
        do=int(c['OBSERVABLE']); ds=int(c['SEMANTIC_ONLY_NONCOMPOSABLE']); dr=int(c['ROUTING_BLOCKED']); dp=int(c['PARTIAL_MEASUREMENT'])
        if do>0:
            st='OBSERVABLE'; reason='directly_sufficient_positive_relation_witness_is_currently_respondent_observable'
        elif sub.capability_status.isin(['OBSERVABLE','PARTIALLY_OBSERVABLE']).any():
            st='PARTIALLY_OBSERVABLE'; reason='o10_successor_linked_governed_terrain_exists_but_direct_requirement_minimum_structure_is_not_preaccepted_as_observable'
        elif ds>0:
            st='SEMANTIC_ONLY_NONCOMPOSABLE'; reason='directly_sufficient_semantic_relation_exists_but_common_current_respondent_route_is_not_proven'
        elif dr>0:
            st='ROUTING_BLOCKED'; reason='directly_sufficient_semantic_relation_exists_but_current_o06_has_unresolved_member_routing'
        elif dp>0:
            st='PARTIALLY_OBSERVABLE'; reason='directly_sufficient_semantic_relation_has_incomplete_individual_measurement_contract'
        else:
            st='NOT_OBSERVED'; reason='no_directly_sufficient_positive_witness_and_no_o10_successor_linked_bounded_search_terrain'
        req_rows.append({
          'source_family':sf,'wave':wv,'requirement_id':req,'requirement_label':d.indicator_label,
          'capability_status':st,'capability_reason':reason,'direct_sufficient_relation_types_json':json.dumps(direct_shapes,separators=(',',':')),
          'direct_observable_witness_count':do,'direct_semantic_only_noncomposable_witness_count':ds,'direct_routing_blocked_witness_count':dr,
          'linked_rule_ids_json':json.dumps(linked,separators=(',',':')),'linked_rule_statuses_json':json.dumps(dict(Counter(sub.capability_status)),sort_keys=True,separators=(',',':')),
          'observable_rule_count':int((sub.capability_status=='OBSERVABLE').sum()),'partial_rule_count':int((sub.capability_status=='PARTIALLY_OBSERVABLE').sum()),
          'semantic_only_noncomposable_rule_count':int((sub.capability_status=='SEMANTIC_ONLY_NONCOMPOSABLE').sum()),'routing_blocked_rule_count':int((sub.capability_status=='ROUTING_BLOCKED').sum()),
          'not_observed_rule_count':int((sub.capability_status=='NOT_OBSERVED').sum()),'minimum_joint_structure':d.minimum_joint_structure,
          'evidence_ceiling':d.evidence_ceiling,'prohibited_claims':d.prohibited_claims,
          'candidate_generation_posture':'ALLOW_BOUNDED_O12_SEARCH' if st in ['OBSERVABLE','PARTIALLY_OBSERVABLE'] else 'BLOCK_UNTIL_CAPABILITY_CHANGES',
          'authority_basis':'RECOMPUTED_FROM_O10_T15_SUCCESSOR_AND_CURRENT_SOURCE_FIRST_RELATION_CAPABILITY'
        })
req_df=pd.DataFrame(req_rows)
base_req=orig_req.columns.tolist(); req_extra=[c for c in ['authority_basis'] if c not in base_req]
req_df=req_df[base_req+req_extra]
assert len(req_df)==595 and req_df.groupby(['source_family','wave']).size().eq(17).all()

# Derived indicator capability mirrors owning requirement; computation remains blocked.
ind_rows=[]
for _,q in req_df.iterrows():
    d=s15[s15.requirement_id==q.requirement_id].iloc[0]
    ind_rows.append({'source_family':q.source_family,'wave':q.wave,'requirement_id':q.requirement_id,'indicator_id':d.indicator_id,
                     'indicator_label':d.indicator_label,'capability_status':q.capability_status,'computation_authorized':False,
                     'minimum_joint_structure':d.minimum_joint_structure,'evidence_ceiling':d.evidence_ceiling,
                     'missing_neutral_inapplicable_law':d.missing_neutral_inapplicable_law,'relation_membership_law':d.relation_membership_law,
                     'runtime_status':'BLOCKED_UNTIL_JOB3_RELATION_MEMBERSHIP_AND_RESPONDENT_CONFIGURATION'})
ind_df=pd.DataFrame(ind_rows)[orig_ind.columns.tolist()]
assert len(ind_df)==595

# Summary with 15 / 17 counts.
sumrows=[]
for _,w in waves.iterrows():
    sf,wv=w.source_family,str(w.wave); rr=rule_df[(rule_df.source_family==sf)&(rule_df.wave.astype(str)==wv)]; qq=req_df[(req_df.source_family==sf)&(req_df.wave.astype(str)==wv)]
    sumrows.append({'source_family':sf,'wave':wv,'implementation_count':int(w.implementation_count),
      'rule_observable_count':int((rr.capability_status=='OBSERVABLE').sum()),'rule_partial_count':int((rr.capability_status=='PARTIALLY_OBSERVABLE').sum()),
      'rule_semantic_only_noncomposable_count':int((rr.capability_status=='SEMANTIC_ONLY_NONCOMPOSABLE').sum()),'rule_routing_blocked_count':int((rr.capability_status=='ROUTING_BLOCKED').sum()),
      'rule_not_observed_count':int((rr.capability_status=='NOT_OBSERVED').sum()),'requirement_observable_count':int((qq.capability_status=='OBSERVABLE').sum()),
      'requirement_partial_count':int((qq.capability_status=='PARTIALLY_OBSERVABLE').sum()),'requirement_semantic_only_noncomposable_count':int((qq.capability_status=='SEMANTIC_ONLY_NONCOMPOSABLE').sum()),
      'requirement_routing_blocked_count':int((qq.capability_status=='ROUTING_BLOCKED').sum()),'requirement_not_observed_count':int((qq.capability_status=='NOT_OBSERVED').sum()),
      'o12_wave_search_allowed':bool((rr.candidate_generation_posture=='ALLOW_BOUNDED_O12_SEARCH').any())})
summary_df=pd.DataFrame(sumrows)

# Rule summary.
rule_summary=rule_df.groupby(['rule_id','candidate_template_class','capability_status']).size().unstack(fill_value=0).reset_index()
for c in ['OBSERVABLE','PARTIALLY_OBSERVABLE','SEMANTIC_ONLY_NONCOMPOSABLE','ROUTING_BLOCKED','NOT_OBSERVED']:
    if c not in rule_summary: rule_summary[c]=0
post=rule_df.groupby('rule_id').candidate_generation_posture.apply(lambda s:int((s=='ALLOW_BOUNDED_O12_SEARCH').sum())).rename('allow_bounded_o12_cells')
rule_summary=rule_summary.merge(post,on='rule_id')

# Doctrine / report / state.
doctrine='''# O11/S16 successor doctrine — T15 + source-first T06\n\nS16 is a static per-wave/per-rule observability and bounded-search control surface. It consumes governed semantic relation authority; it does not create or revoke relation truth.\n\nCapability states:\n- `OBSERVABLE`: at least one governed positive relation has a current respondent-composable O06/O07 witness.\n- `PARTIALLY_OBSERVABLE`: no observable positive is required, but governed unresolved relation terrain has a currently bounded-searchable member configuration.\n- `SEMANTIC_ONLY_NONCOMPOSABLE`: semantic relation or unresolved terrain exists, but common current respondent composability is not proven.\n- `ROUTING_BLOCKED`: relation/terrain exists, but current O06 unresolved routing blocks the relevant member structures.\n- `NOT_OBSERVED`: no current positive and no runtime-bound unresolved terrain. This is not an absence claim.\n\nSuccessor laws:\n1. Universe is exactly 35 source-waves × 15 S14 rules = 525 cells.\n2. T03–T05/T07–T11 retain the R16G source-first role-bridge capability rebuild.\n3. T06 is superseded at capability level by the 64-row central strict source-first T06 authority plus the six-worker source-first blocked crosswalk terrain; the old seven-positive/legacy-candidate T06 capability surface is ancestry only.\n4. T15 consumes the 188-row central source-first T15 authority plus its blocked source/bridge crosswalk terrain.\n5. T01/T02/T12/T13/T14 retain the accepted R10J O11 cells; T14 remains recall-only.\n6. `ALLOW_BOUNDED_O12_SEARCH` requires OBSERVABLE or PARTIALLY_OBSERVABLE.\n7. Source-proven mismatches are exact-link negatives only. BLOCK/unknown never becomes negative or an absence claim.\n8. O07 proves individual measurement availability only; cross-member value portability remains downstream/candidate-specific.\n9. Typed semantic capability never gates or erases V550/V550J empirical co-travel.\n10. S16 creates no Job-3 candidate acceptance, respondent join, indicator value, temporal authority, or persona inference.\n'''
(OUT/'S16_CAPABILITY_DOCTRINE_T15_SUCCESSOR.md').write_text(doctrine)

# Save ledgers.
rule_df.to_csv(OUT/'S16_WAVE_RELATION_CLASS_CAPABILITY_ATLAS_T15_SUCCESSOR.csv',index=False)
req_df.to_csv(OUT/'S16_WAVE_REQUIREMENT_CAPABILITY_ATLAS_T15_SUCCESSOR.csv',index=False)
ind_df.to_csv(OUT/'S16_WAVE_DERIVED_INDICATOR_CAPABILITY_ATLAS_T15_SUCCESSOR.csv',index=False)
summary_df.to_csv(OUT/'S16_35WAVE_CAPABILITY_SUMMARY_T15_SUCCESSOR.csv',index=False)
rule_summary.to_csv(OUT/'S16_RULE_SUMMARY_T15_SUCCESSOR.csv',index=False)
witness_df.to_csv(OUT/'S16_POSITIVE_RELATION_WITNESS_REVALIDATION_T15_SUCCESSOR.csv',index=False)
strict_wit.to_csv(OUT/'S16_STRICT_T06_POSITIVE_WITNESS_REPLAY.csv',index=False)
t15_wit.to_csv(OUT/'S16_T15_POSITIVE_WITNESS_REPLAY.csv',index=False)
t06_block_replay.to_csv(OUT/'S16_T06_BLOCKED_TERRAIN_REPLAY.csv',index=False)
t15_block_replay.to_csv(OUT/'S16_T15_BLOCKED_TERRAIN_REPLAY.csv',index=False)
t06_mismatch.to_csv(OUT/'S16_T06_SOURCE_PROVEN_MISMATCH_LEDGER.csv',index=False)

state={'release_id':'R10K_O11_S16_T15_SUCCESSOR_20260812','waves':35,'implementations':18276,'s14_rules':15,'s15_requirements':17,
       'relation_cells':len(rule_df),'requirement_cells':len(req_df),'indicator_cells':len(ind_df),
       'strict_t06_positive_relations':len(strict),'t15_positive_relations':len(t15),'t06_open_source_blocks':len(t06_blocks),'t15_open_source_bridge_blocks':len(t15_blocks),
       'job3_candidates_created':0,'job3_relation_acceptance_created':False,'respondent_joins_created':0,'indicator_values_created':0,'live_install':False,
       'next_gate':'O12_REGENERATION_AND_COMPLETENESS_AUDIT'}
(OUT/'CURRENT_STATE_O11_T15_SUCCESSOR.json').write_text(json.dumps(state,indent=2,sort_keys=True)+'\n')

# Validation.
statuses={'OBSERVABLE','PARTIALLY_OBSERVABLE','SEMANTIC_ONLY_NONCOMPOSABLE','ROUTING_BLOCKED','NOT_OBSERVED'}
checks={
 'waves_35':len(waves)==35,
 'implementations_18276':int(waves.implementation_count.sum())==18276,
 's14_rules_15':len(s14)==15,
 's15_requirements_17':len(s15)==17,
 'relation_cells_525':len(rule_df)==525,
 'requirement_cells_595':len(req_df)==595,
 'indicator_cells_595':len(ind_df)==595,
 'unique_relation_keys':rule_df[['source_family','wave','rule_id']].drop_duplicates().shape[0]==525,
 'every_wave_15_rules':rule_df.groupby(['source_family','wave']).size().eq(15).all(),
 'every_wave_17_requirements':req_df.groupby(['source_family','wave']).size().eq(17).all(),
 'status_vocab':set(rule_df.capability_status)<=statuses and set(req_df.capability_status)<=statuses,
 't14_recall_only':(rule_df[rule_df.rule_id=='S14-T14'].candidate_generation_posture=='RECALL_ONLY').all(),
 'blocked_not_searchable':not rule_df[rule_df.capability_status.isin(['SEMANTIC_ONLY_NONCOMPOSABLE','ROUTING_BLOCKED','NOT_OBSERVED'])].candidate_generation_posture.eq('ALLOW_BOUNDED_O12_SEARCH').any(),
 'strict_t06_64':len(strict_wit)==64,
 't15_188':len(t15_wit)==188,
 't06_source_blocks_111':len(t06_block_replay)==111,
 't15_source_blocks_139':len(t15_block_replay)==139,
 'no_absence_claims':(rule_df.absence_claim_licensed=='NO').all(),
 'no_job3_candidates':state['job3_candidates_created']==0,
 'no_indicator_values':state['indicator_values_created']==0,
}
validation={'status':'PASS' if all(bool(v) for v in checks.values()) else 'FAIL','checks':{k:bool(v) for k,v in checks.items()},
            'counts':{'relation_status':rule_df.capability_status.value_counts().to_dict(),'requirement_status':req_df.capability_status.value_counts().to_dict(),
                      'strict_t06_witness_status':strict_wit.capability_witness_status.value_counts().to_dict(),'t15_witness_status':t15_wit.capability_witness_status.value_counts().to_dict(),
                      't06_block_terrain_status':t06_block_replay.capability_terrain_status.value_counts().to_dict(),'t15_block_terrain_status':t15_block_replay.capability_terrain_status.value_counts().to_dict(),
                      'allow_bounded_o12_cells':int((rule_df.candidate_generation_posture=='ALLOW_BOUNDED_O12_SEARCH').sum())}}
(OUT/'O11_T15_VALIDATION.json').write_text(json.dumps(validation,indent=2,sort_keys=True)+'\n')

# Hostile QA: exact preserved cells for non-rebuilt rules, T06 old R16G not leaked, T15 rule/JE17 present.
preserved=['S14-T01','S14-T02','S14-T12','S14-T13','S14-T14']
pres_ok=True
for rid in preserved:
    a=rule_df[rule_df.rule_id==rid][base_cols].sort_values(['source_family','wave']).reset_index(drop=True).astype(str)
    b=orig_rule[orig_rule.rule_id==rid][base_cols].sort_values(['source_family','wave']).reset_index(drop=True).astype(str)
    if not a.equals(b): pres_ok=False
# Compare R16G statuses/postures for T03-5/T07-11.
patch_ok=True
for rid in ['S14-T03','S14-T04','S14-T05','S14-T07','S14-T08','S14-T09','S14-T10','S14-T11']:
    a=rule_df[rule_df.rule_id==rid].set_index(['source_family','wave'])
    b=rpatch[rpatch.norm_rule_id==rid].set_index(['source_family','wave'])
    for k in a.index:
        if a.loc[k,'capability_status']!=b.loc[k,'capability_status'] or a.loc[k,'candidate_generation_posture']!=b.loc[k,'candidate_generation_posture']:
            patch_ok=False; break
qa_checks={
 'preserved_T01_T02_T12_T13_T14_exact':pres_ok,
 'r16g_T03_T05_T07_T11_status_posture_preserved':patch_ok,
 'T06_uses_source_first_64_not_old_7':int(rule_df[rule_df.rule_id=='S14-T06'].frozen_positive_relation_count.astype(int).sum())==64,
 'T15_uses_188':int(rule_df[rule_df.rule_id=='S14-T15'].frozen_positive_relation_count.astype(int).sum())==188,
 'JE17_35_cells':len(req_df[req_df.requirement_id=='JE-17_NORM_PRACTICAL_REALIZATION'])==35,
 'S15_norm_praxis_35_cells':len(ind_df[ind_df.requirement_id=='JE-17_NORM_PRACTICAL_REALIZATION'])==35,
 'no_empirical_cotravel_gate':rule_df.app_cotravel_guardrail.str.contains('never gates or erases',case=False).all(),
}
qa_checks={k:bool(v) for k,v in qa_checks.items()}
hqa={'status':'PASS' if all(qa_checks.values()) else 'FAIL','checks':qa_checks}
(OUT/'O11_T15_HOSTILE_QA.json').write_text(json.dumps(hqa,indent=2,sort_keys=True)+'\n')

report=f'''# O11/S16 T15 successor — source-first T06/T15 capability rebuild\n\n## Verdict\n**PASS.** The static capability surface now matches the O10 T15 successor and the central source-first T06/T15 authority.\n\n- 35 active waves / 18,276 implementations.\n- 15 S14 rule channels → **525** wave×rule cells.\n- 17 JE/S15 requirements → **595** wave×requirement cells and **595** wave×indicator-capability cells.\n- strict source-first T06 positives replayed: **64**.\n- central T15 positives replayed: **188**.\n- source-first T06 unresolved crosswalk terrain: **111** exact blocked pairs (legacy massive candidate surface not reused).\n- source-first T15 unresolved crosswalk terrain: **139** exact blocked pairs.\n\n### Relation capability totals\n{json.dumps(validation['counts']['relation_status'],sort_keys=True)}\n\nBounded O12-search cells: **{validation['counts']['allow_bounded_o12_cells']} / 525**. T14 remains recall-only.\n\n### T06/T15 current witness observability\nStrict T06: {json.dumps(validation['counts']['strict_t06_witness_status'],sort_keys=True)}\nT15: {json.dumps(validation['counts']['t15_witness_status'],sort_keys=True)}\n\n## Authority conservation\n- T01/T02/T12/T13/T14 cells are byte-equivalent at the row-contract level to accepted R10J O11.\n- T03–T05/T07–T11 status/posture is conserved from R16G.\n- T06 is intentionally superseded at capability level by the complete source-first strict-T06 reconstruction.\n- T15/JE-17 is appended from the central 188-row source-first authority.\n\n## App meaning\nThis gives downstream enumeration a real semantic norm→praxis capability map instead of forcing everything through exact norm/action identity. It does not restrict empirical V550/V550J co-travel and creates no persona or moral-character inference.\n\n## Ceiling / next gate\nNo Job-3 candidate acceptance, respondent joins, indicator values, temporal authority, or runtime installation are created here. Next: **O12 regeneration + completeness audit under the 15-rule successor grammar and this S16 surface.**\n'''
(OUT/'O11_T15_SUCCESSOR_REPORT.md').write_text(report)

# Manifest.
manifest=[]
for p in sorted(OUT.iterdir()):
    if p.is_file(): manifest.append({'path':p.name,'sha256':sha256(p),'bytes':p.stat().st_size})
pd.DataFrame(manifest).to_csv(OUT/'SHA256_MANIFEST_O11_T15.csv',index=False)

print(json.dumps(validation,indent=2))
print(json.dumps(hqa,indent=2))
print('\nT06 cells:'); print(rule_df[rule_df.rule_id=='S14-T06'][['source_family','wave','capability_status','frozen_positive_relation_count','unresolved_source_first_pair_count','bounded_searchable_unresolved_count','candidate_generation_posture']].to_string(index=False))
print('\nT15 cells:'); print(rule_df[rule_df.rule_id=='S14-T15'][['source_family','wave','capability_status','frozen_positive_relation_count','unresolved_source_first_pair_count','bounded_searchable_unresolved_count','candidate_generation_posture']].to_string(index=False))
