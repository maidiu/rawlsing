import json,pandas as pd,collections,re,os,hashlib
R14='/mnt/data/live_parents/o12/Rawlsing_R10K_O12_Job3_Candidate_Denominator_Completeness_Repair_R2_20260811/PARENTS/R14_SOURCE_NATIVE_AUTHORITY_FINAL_708047.json'
SP='/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10_20260811/SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10.csv.gz'
sp=pd.read_csv(SP,dtype=str,low_memory=False)
fam_alias={'ASB':'Asian Barometer','Asian Barometer':'Asian Barometer','ArabBarometer':'Arab Barometer','Arab Barometer':'Arab Barometer'}
def norm_scope(f,w):
    f=fam_alias.get(str(f),str(f)); w=str(w)
    if f=='LiTS' and w=='I': w='2006'
    return f,w
lookup=collections.defaultdict(list)
for _,r in sp[['question_implementation_id','source_family','wave','source_variable_code']].iterrows():
    lookup[(str(r.source_family),str(r.wave),str(r.source_variable_code).strip().lower())].append(str(r.question_implementation_id))

def structure_label(o):
    for k in ['native_structure_label','native_parent_identifier','printed_parent_id']:
        v=o.get(k)
        if v:return str(v).strip()
    oid=str(o.get('object_id',''))
    m=re.search(r'(?:STRUCTURE-|GROUP-)(Q[A-Z0-9_]+)',oid,re.I)
    return m.group(1) if m else ''

def raw_codes(o):
    vals=[]; methods=[]
    for k in ['members','ordered_members','printed_children_sequence']:
        v=o.get(k)
        if isinstance(v,list) and v:
            vals += [str(x).strip() for x in v if str(x).strip()]; methods.append(k)
    for k,idk in [('member_evidence','codebook_variable_id'),('crosswalk','codebook_variable_id')]:
        v=o.get(k)
        if isinstance(v,list) and v:
            z=[str(e.get(idk)).strip() for e in v if isinstance(e,dict) and e.get(idk)]
            vals += z
            if z:methods.append(k)
    return list(dict.fromkeys(vals)),methods

def fallback_candidates(code,label):
    out=[]
    c=code.strip(); lab=label.strip()
    m=re.fullmatch(r'item\s*([0-9]+[A-Za-z]?)',c,re.I)
    if m and lab:
        suf=m.group(1)
        out += [f'{lab}_{suf}', f'{lab}{suf}']
        # normalize q605a + item1 -> q605a_1; q605A_1 handled case-insensitive
    # printed child generic A/B variants occasionally written q139a when catalog keeps parent q139;
    # DO NOT collapse to parent automatically: source child identity would be lost.
    return list(dict.fromkeys(out))

d=json.load(open(R14)); rows=[]; member_rows=[]
for o in d['objects']:
    f,w=norm_scope(o['family'],o['wave']); label=structure_label(o); vals,methods=raw_codes(o)
    mapped=[]; unresolved=[]; member_details=[]
    for code in vals:
        hits=lookup.get((f,w,code.lower()),[]); basis='DIRECT_SOURCE_CODE'
        tried=[]
        if not hits:
            for cand in fallback_candidates(code,label):
                tried.append(cand)
                hh=lookup.get((f,w,cand.lower()),[])
                if hh:
                    hits=hh; basis='STRUCTURE_LABEL_PLUS_ITEM_SUFFIX'; break
        if len(hits)==1:
            mapped.append(hits[0]); member_details.append((code,hits[0],basis,tried))
        elif len(hits)>1:
            for h in hits: mapped.append(h)
            member_details.append((code,';'.join(hits),'AMBIGUOUS_MULTIPLE_IMPLEMENTATIONS',tried))
        else:
            unresolved.append(code); member_details.append((code,'','UNRESOLVED_SOURCE_MEMBER_CODE',tried))
    mapped=list(dict.fromkeys(mapped))
    rows.append({
      'object_id':o['object_id'],'schema_version':o.get('schema_version',''),'family_raw':o['family'],'wave_raw':str(o['wave']),
      'source_family':f,'wave':w,'state':o.get('state',''),'source_structure_label':label,
      'source_obligation_id':o.get('source_obligation_id',''),'printed_parent_id':o.get('printed_parent_id',''),
      'native_parent_identifier':o.get('native_parent_identifier',''),'native_structure_label':o.get('native_structure_label',''),
      'member_codes_json':json.dumps(vals),'member_code_count':len(vals),'mapped_implementation_ids_json':json.dumps(mapped),
      'mapped_implementation_count':len(mapped),'unresolved_member_codes_json':json.dumps(unresolved),'unresolved_member_code_count':len(unresolved),
      'extraction_methods':';'.join(methods),'evidence_class':o.get('evidence_class',''),
      'questionnaire_locator':o.get('questionnaire_locator',''),'questionnaire_page':o.get('questionnaire_page','')
    })
    for code,iid,basis,tried in member_details:
        member_rows.append({'object_id':o['object_id'],'source_family':f,'wave':w,'source_structure_label':label,'source_member_code':code,'question_implementation_id':iid,'mapping_basis':basis,'fallback_candidates_json':json.dumps(tried)})
out=pd.DataFrame(rows); mr=pd.DataFrame(member_rows)
out.to_csv('/mnt/data/R14_COMPREHENSIVE_OBJECT_CROSSWALK_R10A.csv',index=False); mr.to_csv('/mnt/data/R14_COMPREHENSIVE_MEMBER_CROSSWALK_R10A.csv',index=False)
print('objects',len(out),'raw member codes',out.member_code_count.sum(),'mapped occurrences',out.mapped_implementation_count.sum(),'unresolved codes',out.unresolved_member_code_count.sum(),'objects with unresolved',(out.unresolved_member_code_count>0).sum())
print('unique mapped impls',len(set(x for s in out.mapped_implementation_ids_json for x in json.loads(s))))
print('mapping basis',mr.mapping_basis.value_counts().to_dict())
print('ordered objects mapped',len(out[(out.extraction_methods.str.contains('ordered_members',na=False)) & (out.mapped_implementation_count>0)]),'/',sum(out.extraction_methods.str.contains('ordered_members',na=False)))
print('placeholder fallback mapped',sum(mr.mapping_basis=='STRUCTURE_LABEL_PLUS_ITEM_SUFFIX'))
print('unresolved sample',out[out.unresolved_member_code_count>0][['object_id','source_family','wave','source_structure_label','unresolved_member_codes_json','mapped_implementation_count']].head(30).to_string(index=False))
