from pathlib import Path
import pandas as pd,json,re
OUT=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10_20260811'); (OUT/'ANCESTRY').mkdir(exist_ok=True)
sp=pd.read_csv(OUT/'SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10.csv.gz',low_memory=False)
r8p=Path('/mnt/data/r8_full/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R8_20260811/NARROWING/T03_T11_CROSS_RULE_DEDUPED_CANONICAL_PACKETS_R8.csv')
r8=pd.read_csv(r8p,low_memory=False)
# normalize lookup by source/wave lower code
lookup={}
for (sf,w),g in sp.groupby(['source_family','wave']):
    d={str(c).lower():[] for c in g.source_variable_code.fillna('').astype(str)}
    for _,x in g.iterrows():
        d.setdefault(str(x.source_variable_code).lower(),[]).append(str(x.question_implementation_id))
    lookup[(str(sf),str(w))]=d

def jlist(x):
    if pd.isna(x): return []
    s=str(x)
    try:
        a=json.loads(s); return a if isinstance(a,list) else [a]
    except:return [s]
# conservative tokenizer: actual source codes only, found as literal substrings with delimiter-ish boundaries
rows=[]
for _,r in r8.iterrows():
    sfs=[str(x) for x in jlist(r.source_families_json)]; ws=[str(x) for x in jlist(r.waves_json)]
    surf=' '.join(str(x) for x in jlist(r.member_surfaces_json))
    impl=set(); matched=[]
    groups=[]
    if len(sfs)==1 and len(ws)>=1:
        groups=[(sfs[0],w) for w in ws]
    elif len(sfs)==len(ws): groups=list(zip(sfs,ws))
    else:
        # scan all matching source-family groups for MULTI or encoded variants
        groups=[k for k in lookup if (not sfs or 'MULTI' in sfs or k[0] in sfs) and (not ws or 'MULTI' in ws or k[1] in ws)]
    for key in groups:
        d=lookup.get(key,{})
        for code,ids in d.items():
            if not code: continue
            # code is matched if appears as standalone-ish token; source codes may contain underscores/hyphens
            if re.search(r'(?<![A-Za-z0-9_])'+re.escape(code)+r'(?![A-Za-z0-9_])',surf,re.I):
                impl.update(ids); matched.append(key[0]+'::'+key[1]+'::'+code)
    # also semantic-unit IDs can appear in surfaces; direct scan
    for uid,g in sp[sp.sem__audit_unit_id.notna()].groupby('sem__audit_unit_id'):
        if str(uid) in surf: impl.update(g.question_implementation_id.astype(str))
    rows.append({'canonical_packet_id':r.canonical_packet_id,'queue_class':r.queue_class,'rule_hypotheses':r.rule_hypotheses,'source_families_json':r.source_families_json,'waves_json':r.waves_json,'origin_packet_ids_json':r.origin_packet_ids_json,'mapped_implementation_count':len(impl),'mapped_question_implementation_ids_json':json.dumps(sorted(impl)),'matched_source_codes_json':json.dumps(sorted(set(matched))),'crosswalk_status':'MAPPED_TO_R10_SPINE' if impl else 'NO_EXACT_IMPLEMENTATION_MAPPING_FROM_PACKET_SURFACE__PRESERVE_PACKET_AS_ANCESTRY'})
cw=pd.DataFrame(rows); cw.to_csv(OUT/'ANCESTRY/R8_89_PACKET_TO_R10_SPINE_CROSSWALK.csv',index=False)
# R8C verdict crosswalk via parent packet mapping + explicit member codes
vp=Path('/mnt/data/r8c_full/Rawlsing_R10K_S14_R8C_Vozhd_Central_Adjudication_20260811/ADJUDICATION/CENTRAL_13_RULE_VERDICTS_R8C.csv')
v=pd.read_csv(vp,low_memory=False)
pm={r.canonical_packet_id:set(jlist(r.mapped_question_implementation_ids_json)) for _,r in cw.iterrows()}
vr=[]
for _,r in v.iterrows():
    impl=set(pm.get(r.canonical_packet_id,set()))
    # match explicitly listed source codes within only packet-mapped source/wave groups where possible
    vr.append({**r.to_dict(),'r10_mapped_implementation_count':len(impl),'r10_mapped_question_implementation_ids_json':json.dumps(sorted(impl)),'r10_revalidation_status':'PRESERVED_PROVISIONAL__REVALIDATE_AFTER_DENOMINATOR_COMPLETE'})
pd.DataFrame(vr).to_csv(OUT/'ANCESTRY/R8C_33_RULE_VERDICTS_TO_R10_SPINE_CROSSWALK.csv',index=False)
summary={'r8_packet_rows':len(cw),'r8_packets_with_exact_spine_mapping':int((cw.mapped_implementation_count>0).sum()),'r8_packets_without_exact_mapping_from_surface':int((cw.mapped_implementation_count==0).sum()),'r8c_rule_verdict_rows':len(vr),'r8c_verdict_rows_with_parent_packet_spine_mapping':sum(x['r10_mapped_implementation_count']>0 for x in vr),'law':'No R8/R8C object is deleted. Exact mappings are carried forward; unmapped packet surfaces remain explicit ancestry obligations, never silent drops.'}
json.dump(summary,open(OUT/'ANCESTRY/R8_R8C_CROSSWALK_SUMMARY_R10.json','w'),indent=2)
print(summary)
