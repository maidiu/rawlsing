import pandas as pd, json, re, os, hashlib, collections, math
from pathlib import Path

BASE=Path('/mnt/data/rawlsing_exec')
CANON=BASE/'o12r2/CANONICAL_IMPLEMENTATION_REGISTRY.csv'
R6=BASE/'o12r2/INTER_QUESTION_RELATION_AUTHORITY_R2.csv'
R14=BASE/'o12r2/R14_SOURCE_NATIVE_AUTHORITY_FINAL_708047.json'
R10G=BASE/'r10g_successor/Rawlsing_DDM_R10G_O02_S08_Canonical_Coordinate_Authority_20260810/R10G_S08_FULL_3324_COORDINATE_AUTHORITY.csv'
OUT=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R4_20260811')
(OUT/'NARROWING').mkdir(parents=True,exist_ok=True)
(OUT/'PROVENANCE').mkdir(exist_ok=True)
(OUT/'AUDIT').mkdir(exist_ok=True)
(OUT/'VALIDATION').mkdir(exist_ok=True)

canon=pd.read_csv(CANON,low_memory=False)
r6=pd.read_csv(R6,low_memory=False)
r10g=pd.read_csv(R10G,low_memory=False)
r14=json.load(open(R14))['objects']

# Normalize string helper
def s(x): return '' if pd.isna(x) else str(x)
def low(*xs): return ' | '.join(s(x) for x in xs).lower()

DIRECT_FACET_CLASS={
 'coercive_legal_institution_trust':'COERCIVE_LEGAL_INSTITUTION',
 'public_service_knowledge_institution_trust':'PUBLIC_SERVICE_KNOWLEDGE_INSTITUTION',
 'religious_institution_trust':'RELIGIOUS_INSTITUTION',
 'external_supranational_institution_trust':'EXTERNAL_SUPRANATIONAL_INSTITUTION',
 'commercial_institution_trust':'COMMERCIAL_INSTITUTION',
 'media_institution_confidence':'MEDIA_INSTITUTION',
 'political_and_civic_institution_trust':'POLITICAL_GOVERNANCE_INSTITUTION',
}

# R6 T08 is sealed canary authority. Its exact member IDs are allowed to enter the class-mapping
# recovery even when a current semantic-unit join is absent; such rows remain explicit upstream blockers.
r6_t08=r6[r6.relation_type.eq('INSTITUTION_CLASS_DIFFERENTIATION')].copy()
R6_T08_MEMBER_IDS=set()
for x in r6_t08.member_question_implementation_ids:
    try: R6_T08_MEMBER_IDS.update(json.loads(x))
    except: pass

# Bounded exact-target vocabulary grounded in the July-30 candidate definitions and the later
# August-9 source-first corrections. The political-governance lane explicitly preserves the
# executive-office-vs-institution distinction found in that later work.
PATTERNS=[
 ('CIVIC_ASSOCIATIONAL_INSTITUTION', [
  r'\btrade unions?\b', r'\blabo[u]?r unions?\b', r'\borganized labo[u]?r\b',
  r'\bnon[- ]?governmental\b', r'\bngos?\b', r'\bcivil society\b',
  r'environmental organi[sz]ations?', r'environmental protection movement', r"women'?s organi[sz]ations?", r"women'?s movement", r'charitable or humanitarian organi[sz]ations?',
  r'professional (associations?|unions?)', r'voluntary associations?'
 ]),
 ('MEDIA_INSTITUTION', [r'\bthe press\b',r'^press$',r'newspapers?',r'^television$',r'^radios?$',r'media institution']),
 ('COERCIVE_LEGAL_INSTITUTION', [r'^police$',r'\bthe police\b',r'^courts?$',r'\bthe courts\b',r'courts of law',r'judiciar',r'justice system',r'armed forces',r'^army$',r'\bthe army\b']),
 ('PUBLIC_SERVICE_KNOWLEDGE_INSTITUTION', [r'education system',r'health care system',r'healthcare system',r'^universit',r'social security system',r'public schools?']),
 ('RELIGIOUS_INSTITUTION', [r'^church(es)?$',r'\bthe churches\b',r'religious institutions?',r'religious leaders?']),
 ('EXTERNAL_SUPRANATIONAL_INSTITUTION', [
  r'european union',r'united nations',r'\bnato\b',r'international monetary fund',r'\bimf\b',r'world bank',r'world health organi[sz]ation',r'\bwho\b',r'world trade organi[sz]ation',r'\bwto\b',r'international criminal court',r'\bicc\b',r'african union',r'\basean\b',r'\bapec\b',r'\bsaarc\b',r'regional organi[sz]ation'
 ]),
 ('COMMERCIAL_INSTITUTION', [r'^banks?$',r'financial institutions?',r'major companies',r'private enterprises?',r'^companies$',r'^enterprises$',r'business associations?']),
 ('POLITICAL_EXECUTIVE_OFFICE', [r'president\s*/?\s*prime minister',r'^president$',r'^prime minister$']),
 ('POLITICAL_GOVERNANCE_INSTITUTION', [
  r'^government$',r'national government',r'local government',r'regional government',r'^parliament$',r'national congress',r'^congress$',r'political parties?',r'civil service',r'electoral commission',r'election commission',r'^elections$',r'public administration',r'^state$',r'shura council',r'tax department',r'tax authorities?',r'local assembl',r'municipal or district assembly'
 ]),
]
ACTOR_NOT_INSTITUTION=[r'businesspeople',r'people who run .*government',r'foreign investors?',r'traditional leaders?',r'tribal leaders?']
AMBIG=[r'muslim brotherhood',r'islamist',r'political[- ]religious',r'charitable work']

# Semantic-unit representative table: current semantic authority rows only.
sem=canon[canon['sem__audit_unit_id'].notna() & ~canon['sem__semantic_only_anti_join'].fillna(False).astype(bool)].copy()
unitrep=sem.sort_values(['sem__audit_unit_id','question_implementation_id']).drop_duplicates('sem__audit_unit_id').copy()

def target_text(row):
    # Prefer actual target identity/label. Full question wording is used only for explicit trust/confidence
    # items or sealed R6 canaries because source-proposition target labels often contain actions/conditions.
    return low(row.get('sem__canonical_target_label'),row.get('sem__target_entity_or_object'))

def classify(row):
    facet=s(row.get('sem__canonical_facet_id'))
    role=s(row.get('sem__canonical_role'))
    qid=s(row.get('question_implementation_id'))
    tgt=target_text(row)
    full=low(row.get('sem__semantic_summary'),row.get('exact_question_text'))
    r6_member=qid in R6_T08_MEMBER_IDS
    trust_like=(role=='TARGET_CONFIDENCE_OR_TRUST' or 'trust' in full or 'confidence' in full)

    if facet=='interpersonal_trust':
        return ('','NOT_APPLICABLE_NONINSTITUTION','R10G_INTERPERSONAL_TRUST_BOUNDARY','HIGH')
    if any(re.search(p,full) for p in ACTOR_NOT_INSTITUTION):
        return ('','ACTOR_NOT_INSTITUTION','AUG09_SOURCE_FIRST_ACTOR_INSTITUTION_BOUNDARY','HIGH')
    if any(re.search(p,full) for p in AMBIG):
        return ('','REVIEW_REQUIRED_AMBIGUOUS_INSTITUTION_TYPE','AUG09_EXPLICIT_BOUNDARY_OR_AMBIGUOUS_TARGET','MEDIUM')

    # Fine current R10G institution-bearing facets are the strongest class bridge inputs.
    if facet in DIRECT_FACET_CLASS and facet!='political_and_civic_institution_trust':
        return (DIRECT_FACET_CLASS[facet],'MAPPED_CURRENT_COORDINATE','R10G_S08_FACET_TO_ORTHOGONAL_CLASS_BRIDGE','HIGH')

    # The later source-first work split the old combined governance/civic candidate, and also preserved
    # executive offices as a distinct target kind inside governance.
    if facet=='political_and_civic_institution_trust':
        scan=full if trust_like else tgt
        if re.search(r'\bpresident\b|\bprime minister\b|\bpresidency\b',scan):
            return ('POLITICAL_EXECUTIVE_OFFICE','MAPPED_SOURCE_FIRST_SUCCESSOR_BOUNDARY','AUG09_EXECUTIVE_OFFICE_VS_INSTITUTION_BOUNDARY','HIGH')
        for cls,pats in PATTERNS:
            if cls in ('CIVIC_ASSOCIATIONAL_INSTITUTION','POLITICAL_EXECUTIVE_OFFICE') and any(re.search(p,scan) for p in pats):
                return (cls,'MAPPED_SOURCE_FIRST_SUCCESSOR_BOUNDARY','AUG09_GOVERNANCE_VS_CIVIC_AND_EXECUTIVE_OFFICE_BOUNDARY','HIGH')
        return ('POLITICAL_GOVERNANCE_INSTITUTION','MAPPED_SOURCE_FIRST_SUCCESSOR_BOUNDARY','AUG09_GOVERNANCE_VS_CIVIC_SPLIT_PLUS_CURRENT_R10G_COORDINATE','HIGH')

    # Exact source-first overrides for known target-only/truncated battery children recovered in the Aug-9 ancestry.
    fam=s(row.get('source_family')); wave=s(row.get('wave')); var=s(row.get('source_variable_code')).lower()
    if fam=='LiTS' and wave=='II' and var in ('q303l','q303m'):
        return ('CIVIC_ASSOCIATIONAL_INSTITUTION','MAPPED_SOURCE_FIRST_ANCESTRY_SUPPORTED','AUG09_LITSII_Q303_SOURCE_BATTERY_RECOVERY','HIGH')

    # For un-faceted rows, do not classify any proposition merely because it mentions government/police/etc.
    # Require either an explicit trust/confidence target context or sealed R6 T08 membership.
    if trust_like or r6_member:
        scan=full if trust_like or r6_member else tgt
        hits=[]
        for cls,pats in PATTERNS:
            if any(re.search(p,scan) for p in pats): hits.append(cls)
        hits=list(dict.fromkeys(hits))
        if len(hits)==1:
            basis='SEALED_R6_T08_SOURCE_TEXT_CLASS_RECOVERY' if r6_member else 'AUG09_SOURCE_FIRST_CLASS_BOUNDARY_PLUS_EXACT_CURRENT_TARGET'
            status='MAPPED_R6_CANARY_SOURCE_TEXT' if r6_member else 'MAPPED_SOURCE_FIRST_ANCESTRY_SUPPORTED'
            return (hits[0],status,basis,'HIGH' if r6_member else 'MEDIUM_HIGH')
        if len(hits)>1:
            return ('','REVIEW_REQUIRED_CLASS_COLLISION','MULTIPLE_CLASS_PATTERNS_ON_EXACT_TARGET','MEDIUM')
        if trust_like:
            return ('','REVIEW_REQUIRED_UNMAPPED_INSTITUTION_CANDIDATE','TRUST_OR_CONFIDENCE_TARGET_WITHOUT_CLASS_COVERAGE','MEDIUM')

    return ('','OUTSIDE_CURRENT_T08_INSTITUTION_TERRAIN','NO_GOVERNED_OR_SOURCE_FIRST_CLASS_BASIS','HIGH')

# Current semantic-unit mapping ledger.
mapped=unitrep.copy()
vals=mapped.apply(classify,axis=1,result_type='expand')
vals.columns=['institution_class','class_mapping_status','class_mapping_basis','class_mapping_confidence']
mapped=pd.concat([mapped.reset_index(drop=True),vals.reset_index(drop=True)],axis=1)
mapcols=['sem__audit_unit_id','source_family','wave','source_variable_code','exact_question_text','sem__semantic_summary','sem__measured_predicate','sem__canonical_driver_id','sem__canonical_facet_id','sem__canonical_question_block_id','sem__canonical_relation_axis_id','sem__canonical_target_id','sem__canonical_target_label','sem__canonical_role','institution_class','class_mapping_status','class_mapping_basis','class_mapping_confidence','r14_object_ids_json']
mapped[mapcols].to_csv(OUT/'NARROWING/T08_INSTITUTION_CLASS_MAPPING_R4.csv',index=False)

# Full implementation classifier: preserves sealed canary/source-object rows even if the current semantic-unit join is absent.
allimpl=canon.copy()
aiv=allimpl.apply(classify,axis=1,result_type='expand'); aiv.columns=['institution_class','class_mapping_status','class_mapping_basis','class_mapping_confidence']
allimpl=pd.concat([allimpl.reset_index(drop=True),aiv.reset_index(drop=True)],axis=1)
allimpl_by_id=allimpl.set_index('question_implementation_id',drop=False)
# Current semantic implementation subset used for O11/cross-object semantic grouping.
impl=allimpl[allimpl['sem__audit_unit_id'].notna() & ~allimpl['sem__semantic_only_anti_join'].fillna(False).astype(bool)].copy()
impl_by_id=impl.set_index('question_implementation_id',drop=False)

# R6 T08 canary recovery. Recovery means the sealed relation and all exact implementation members are
# found and class-accounted; a missing current semantic unit is carried as an explicit upstream blocker.
can=[]
for _,r in r6_t08.iterrows():
    ids=json.loads(r.member_question_implementation_ids)
    rows=allimpl_by_id.loc[[x for x in ids if x in allimpl_by_id.index]].copy() if any(x in allimpl_by_id.index for x in ids) else pd.DataFrame()
    classes=sorted(set(x for x in rows.get('institution_class',pd.Series(dtype=str)).fillna('') if x))
    unmapped=int((rows.get('institution_class',pd.Series(dtype=str)).fillna('')=='').sum()) if len(rows) else len(ids)
    semgaps=int(rows.get('sem__audit_unit_id',pd.Series(dtype=str)).isna().sum()) if len(rows) else len(ids)
    gap_statuses=sorted(set(rows.loc[rows['institution_class'].fillna('').eq(''),'class_mapping_status'].fillna('').astype(str))) if len(rows) else []
    typed_gap=all(x.startswith('ACTOR_NOT_INSTITUTION') or x.startswith('REVIEW_REQUIRED_') or x.startswith('NOT_APPLICABLE_') for x in gap_statuses)
    if len(rows)==len(ids) and len(classes)>=2 and unmapped==0:
        status='RECOVERED_R6_T08_RELATION' if semgaps==0 else 'RECOVERED_R6_T08_RELATION__UPSTREAM_SEMANTIC_GAP_EXPLICIT'
    elif len(rows)==len(ids) and len(classes)>=2 and typed_gap:
        status='RECOVERED_R6_T08_RELATION__MEMBER_BOUNDARY_REVIEW'
    elif len(rows)==len(ids):
        status='RECOVERED_RELATION_WITH_UNTYPED_CLASS_GAP'
    else:
        status='IMPLEMENTATION_RESOLUTION_GAP'
    can.append({
      'relation_authority_id':r.relation_authority_id,'source_family':r.source_family,'wave':r.wave,
      'member_count':len(ids),'resolved_member_count':len(rows),'mapped_institution_member_count':int(rows['institution_class'].fillna('').ne('').sum()) if len(rows) else 0,
      'current_semantic_unit_gap_count':semgaps,
      'distinct_institution_class_count':len(classes),'institution_classes_json':json.dumps(classes),
      'unmapped_or_noninstitution_member_count':unmapped,'member_gap_statuses_json':json.dumps(gap_statuses),'canary_recovery_status':status,
      'member_question_implementation_ids':r.member_question_implementation_ids,
      'member_exact_question_texts':r.member_exact_question_texts,'evidence_ceiling':r.evidence_ceiling,
    })
can_df=pd.DataFrame(can)
can_df.to_csv(OUT/'PROVENANCE/SEALED_R6_T08_CANARY_RECOVERY_R4.csv',index=False)

# exact O11 T08 139 proxy groups using historical logic
trust=impl[(impl['sem__canonical_driver_id'].fillna('')=='trustEcology') | impl['sem__canonical_facet_id'].fillna('').str.contains('trust|institution',case=False,regex=True)].copy()
gcols=['source_family','wave','sem__canonical_question_block_id','sem__canonical_relation_axis_id','sem__canonical_role']
proxy=[]
for key,g in trust.groupby(gcols,dropna=False):
    tg=g[g['sem__canonical_target_id'].fillna('').ne('')]
    if tg['sem__canonical_target_id'].nunique()<2: continue
    units=tg.drop_duplicates('sem__audit_unit_id')
    classes=sorted(set(x for x in units['institution_class'].fillna('') if x))
    statuses=collections.Counter(units['class_mapping_status'].fillna(''))
    if len(classes)>=2:
        disp='CROSS_CLASS_PROXY_RECALL__SOURCE_STRUCTURE_REQUIRED'
    elif len(classes)==1:
        disp='WITHIN_CLASS_MULTI_TARGET__NO_T08_CLASS_DIFFERENTIATION'
    elif (units['class_mapping_status']=='NOT_APPLICABLE_NONINSTITUTION').all():
        disp='NONINSTITUTION_PROXY__NOT_APPLICABLE_T08'
    elif units['class_mapping_status'].str.startswith('REVIEW_REQUIRED').any():
        disp='CLASS_MAPPING_INCOMPLETE__REVIEW_REQUIRED'
    else:
        disp='NO_GOVERNED_INSTITUTION_CLASS_IN_PROXY_GROUP'
    proxy.append(dict(zip(gcols,key)) | {
      'semantic_unit_count':units['sem__audit_unit_id'].nunique(),
      'target_count':units['sem__canonical_target_id'].nunique(),
      'distinct_institution_class_count':len(classes),'institution_classes_json':json.dumps(classes),
      'class_status_counts_json':json.dumps(statuses,sort_keys=True),
      'semantic_unit_ids_json':json.dumps(sorted(units['sem__audit_unit_id'].astype(str).unique().tolist())),
      'disposition':disp,
      'authority_ceiling':'RECALL_ONLY__O11_PROXY_DOES_NOT_CREATE_T08_RELATION'
    })
proxy_df=pd.DataFrame(proxy)
proxy_df.to_csv(OUT/'AUDIT/O11_T08_139_PROXY_GROUP_DISPOSITION_R4.csv',index=False)

# Build family/wave/source_variable -> implementation mapping for R14 resolution.
keymap=collections.defaultdict(list)
for _,r in allimpl.iterrows():
    keymap[(s(r.source_family),s(r.wave),s(r.source_variable_code).lower())].append(r.question_implementation_id)
# aliases for R14 family labels
fam_alias={'ASB':'Asian Barometer','ArabBarometer':'Arab Barometer','Latinobarometro':'Latinobarómetro','SouthAsia':'South Asia'}

# Sealed R6 T08 membership/source-object signatures for recurrence/alias reconciliation.
r6_t08_member_sets=[]
r6_t08_source_ids=set()
for _,rr in r6_t08.iterrows():
    mids=set(json.loads(rr.member_question_implementation_ids))
    r6_t08_member_sets.append((rr.relation_authority_id,s(rr.source_family),s(rr.wave),mids))
    try: r6_t08_source_ids.update(json.loads(rr.source_structure_ids))
    except: pass

# R14 exact source-native multi-class candidate scan.
r14rows=[]
for o in r14:
    if o.get('state')!='ACCEPTED_SOURCE_NATIVE_JOINT':
        continue
    fam=fam_alias.get(s(o.get('family')),s(o.get('family'))); wave=s(o.get('wave'))
    ids=[]; unresolved=[]
    for m in o.get('members',[]):
        ms=s(m).lower()
        hits=keymap.get((fam,wave,ms),[])
        if len(hits)==1: ids.extend(hits)
        elif len(hits)>1:
            # identical source variable variants may occur; retain all but mark ambiguity
            ids.extend(hits); unresolved.append(f'{m}:MULTI_IMPL_{len(hits)}')
        else: unresolved.append(f'{m}:NO_IMPL')
    ids=list(dict.fromkeys(ids))
    rows=allimpl_by_id.loc[[x for x in ids if x in allimpl_by_id.index]].copy() if ids else pd.DataFrame()
    # preserve rows with no current semantic unit as separate implementation blockers; dedupe only populated semantic units
    if len(rows):
        with_sem=rows[rows['sem__audit_unit_id'].notna()].drop_duplicates('sem__audit_unit_id')
        no_sem=rows[rows['sem__audit_unit_id'].isna()]
        units=pd.concat([with_sem,no_sem],ignore_index=True)
    else:
        units=rows
    classes=sorted(set(x for x in units.get('institution_class',pd.Series(dtype=str)).fillna('') if x))
    impl_set=set(ids)
    r6_matches=[]
    for rid,rf,rw,rset in r6_t08_member_sets:
        if rf==fam and rw==wave and impl_set==rset:
            r6_matches.append(rid)
    # same evaluative predicate indicator: repeated canonical role or measured predicate among institution members.
    ir=units[units['institution_class'].fillna('').ne('')] if len(units) else units
    roles=collections.Counter(ir.get('sem__canonical_role',pd.Series(dtype=str)).fillna(''))
    predicates=collections.Counter(ir.get('sem__measured_predicate',pd.Series(dtype=str)).fillna(''))
    institution_count=len(ir)
    if r6_matches:
        disp='KNOWN_R6_T08_SOURCE_OBJECT_OR_ALIAS__NO_NEW_ADJUDICATION'
    elif len(classes)>=2 and institution_count>=2:
        if unresolved:
            disp='MULTICLASS_SOURCE_OBJECT__MEMBER_RESOLUTION_REVIEW'
        else:
            disp='EMIT_T08_SOURCE_OBJECT_REVIEW_CANDIDATE'
    elif institution_count>=2 and len(classes)==1:
        disp='SAME_BROAD_CLASS_PARALLEL_TARGETS__T08_REVIEW_ALLOWED_BY_R6_PRECEDENT'
    elif institution_count==1:
        disp='SINGLE_INSTITUTION_MEMBER__NO_T08_CLASS_DIFFERENTIATION'
    elif len(rows)>0 and rows['class_mapping_status'].str.startswith('REVIEW_REQUIRED').any():
        disp='SOURCE_OBJECT_CLASS_MAPPING_INCOMPLETE'
    else:
        disp='NO_GOVERNED_INSTITUTION_CLASS_MEMBERS'
    # retain all source objects in ledger for denominator accounting, but later packetize emit rows only
    r14rows.append({
      'r14_object_id':o.get('object_id'),'source_family':fam,'wave':wave,'printed_parent_id':o.get('printed_parent_id'),
      'printed_parent_text':o.get('printed_parent_text'),'member_source_ids_json':json.dumps(o.get('members',[])),
      'resolved_implementation_ids_json':json.dumps(sorted(ids)),
      'resolved_semantic_unit_ids_json':json.dumps(sorted(set(s(x) for x in units.get('sem__audit_unit_id',pd.Series(dtype=str)).dropna() if s(x)))),
      'r6_t08_exact_member_match_ids_json':json.dumps(sorted(r6_matches)),
      'resolved_implementation_count':len(ids),'resolved_semantic_unit_count':len(units),
      'institution_member_count':institution_count,'distinct_institution_class_count':len(classes),'institution_classes_json':json.dumps(classes),
      'institution_roles_json':json.dumps(roles,sort_keys=True),'institution_predicates_json':json.dumps(predicates,sort_keys=True),
      'resolution_notes_json':json.dumps(unresolved),'disposition':disp,
      'authority_ceiling':'SOURCE_STRUCTURE_PLUS_CLASS_MAPPING_REVIEW__NOT_S14_RELATION_AUTHORITY'
    })
r14df=pd.DataFrame(r14rows)
r14df.to_csv(OUT/'NARROWING/T08_R14_SOURCE_NATIVE_OBJECT_DISPOSITION_R4.csv',index=False)

# Cross-object same-wave current-semantic opportunity surface, bounded to same predicate + role and >=2 classes.
# This is deliberately hyperedge/group level, not arbitrary pairs.
cross=[]
inst=impl[impl['institution_class'].fillna('').ne('')].copy()
r14_semsets={}
for _,rr in r14df.iterrows():
    try: r14_semsets[s(rr.r14_object_id)]=set(json.loads(rr.resolved_semantic_unit_ids_json))
    except: r14_semsets[s(rr.r14_object_id)]=set()
# exact current semantic predicate/role/source-wave groups. Need at least 2 classes and at least 2 targets.
for key,g in inst.groupby(['source_family','wave','sem__measured_predicate','sem__canonical_role'],dropna=False):
    u=g.drop_duplicates('sem__audit_unit_id')
    classes=sorted(set(u['institution_class']))
    if len(classes)<2 or u['sem__canonical_target_id'].fillna('').nunique()<2: continue
    r14ids=set()
    for x in u['r14_object_ids_json'].fillna('[]'):
        try: r14ids.update(json.loads(x))
        except: pass
    uset=set(u['sem__audit_unit_id'].astype(str).unique().tolist())
    covering=[oid for oid in r14ids if uset and uset.issubset(r14_semsets.get(oid,set()))]
    if covering:
        cdisp='COVERED_BY_SINGLE_SOURCE_OBJECT_PACKET__NO_SEPARATE_CROSS_OBJECT_PACKET'
    else:
        cdisp='EMIT_CROSS_OBJECT_T08_RECALL_HYPEREDGE'
    cross.append({
      'source_family':key[0],'wave':key[1],'measured_predicate':key[2],'canonical_role':key[3],
      'semantic_unit_count':u['sem__audit_unit_id'].nunique(),'target_count':u['sem__canonical_target_id'].fillna('').nunique(),
      'distinct_institution_class_count':len(classes),'institution_classes_json':json.dumps(classes),
      'semantic_unit_ids_json':json.dumps(sorted(uset)),
      'r14_object_ids_json':json.dumps(sorted(r14ids)),'covering_single_r14_object_ids_json':json.dumps(sorted(covering)),
      'disposition':cdisp,
      'authority_ceiling':'CURRENT_SEMANTIC_COORDINATES_RECALL_ONLY__EXACT_SOURCE_RECONCILIATION_REQUIRED'
    })
crossdf=pd.DataFrame(cross)
crossdf.to_csv(OUT/'NARROWING/T08_CROSS_OBJECT_SAME_PREDICATE_RECALL_R4.csv',index=False)

# Canonical review packets: one source-object packet for genuinely novel exact source structure;
# cross-object groups are recurrence-compressed across waves when the exact semantic-unit hyperedge is identical.
pack=[]
for _,r in r14df[r14df.disposition.str.startswith('EMIT_T08')].iterrows():
    pid='T08R4-R14-'+hashlib.sha256(str(r.r14_object_id).encode()).hexdigest()[:12]
    pack.append({'packet_id':pid,'packet_type':'SOURCE_NATIVE_MULTICLASS','source_family':r.source_family,'waves':s(r.wave),
                 'evidence_object_ids':r.r14_object_id,'institution_classes_json':r.institution_classes_json,
                 'status':'UNRESOLVED_SEMANTIC_REVIEW_PACKET','rule_hypotheses':'T08','recurrence_group_size':1,
                 'notes':'Exact accepted R14 source object with >=2 mapped institution classes and no exact sealed-R6 T08 membership match. Verify common evaluative predicate and class differentiation. Source co-membership alone is not relation truth.'})
xc=crossdf[crossdf.disposition.eq('EMIT_CROSS_OBJECT_T08_RECALL_HYPEREDGE')].copy()
if len(xc):
    xgcols=['source_family','measured_predicate','canonical_role','semantic_unit_ids_json','institution_classes_json']
    for key,g in xc.groupby(xgcols,dropna=False):
        waves=sorted(set(s(x) for x in g.wave))
        r14ids=set()
        for z in g.r14_object_ids_json.fillna('[]'):
            try: r14ids.update(json.loads(z))
            except: pass
        sig='|'.join(map(str,key))
        pid='T08R4-XOBJ-'+hashlib.sha256(sig.encode()).hexdigest()[:12]
        pack.append({'packet_id':pid,'packet_type':'CROSS_OBJECT_SAME_PREDICATE_RECALL','source_family':key[0],'waves':';'.join(waves),
                     'evidence_object_ids':json.dumps(sorted(r14ids)),'institution_classes_json':key[4],
                     'status':'UNRESOLVED_SEMANTIC_REVIEW_PACKET','rule_hypotheses':'T08','recurrence_group_size':len(g),
                     'notes':'Exact same semantic-unit hyperedge is bundled across listed waves where repeated. Same-wave measured predicate+role spans multiple institution classes across source objects; recall packet only until exact source/parallel-target relation is adjudicated.'})
pk=pd.DataFrame(pack).drop_duplicates() if pack else pd.DataFrame(columns=['packet_id','packet_type','source_family','waves','evidence_object_ids','institution_classes_json','status','rule_hypotheses','recurrence_group_size','notes'])
pk.to_csv(OUT/'NARROWING/T08_CANONICAL_REVIEW_PACKETS_R4.csv',index=False)

# Ontology registry
ontology=pd.DataFrame([
 ['POLITICAL_GOVERNANCE_INSTITUTION','Representative/administrative/electoral/state institutions','Government, parliament/congress, parties, civil service, election bodies, local/regional government, public administration','People who run government as generic actors; executive office targets tracked separately; performance approval','July30 candidate + Aug9 governance/civic split + current R10G'],
 ['POLITICAL_EXECUTIVE_OFFICE','Constitutional executive offices when the source presents the office as an institutional trust/confidence target','President, Prime Minister, President/Prime Minister office','Generic people who run government; personal leader favorability','Aug9 explicit executive-office-vs-institution boundary + sealed R6 South Asia/Afro canaries'],
 ['CIVIC_ASSOCIATIONAL_INSTITUTION','Voluntary/civil-society organized institutions','Trade/labor unions, NGOs, civil-society, environmental/women organizations, charities, professional associations','Political parties; government; individual activists','Aug9 R7V source-first split'],
 ['COERCIVE_LEGAL_INSTITUTION','Institutions authorized to police, judge, punish, or use organized force','Police, courts/judiciary/justice system, military/armed forces','Experienced service satisfaction; coercive policy support','July30 candidate + source-first trust closures'],
 ['PUBLIC_SERVICE_KNOWLEDGE_INSTITUTION','Institutional systems for education, health, knowledge, or social provision','Education/health systems, universities, social security','Individual doctor/professor judgment','July30 candidate + Aug9 source-first closure'],
 ['RELIGIOUS_INSTITUTION','Institutionalized religious authorities','Churches, religious institutions/leaders in institutional-confidence context','Personal faith; political-religious movement without class adjudication','R7T source-first closure'],
 ['EXTERNAL_SUPRANATIONAL_INSTITUTION','International/regional cooperative institutions','UN, EU, NATO, IMF, World Bank, WHO, WTO, ICC, regional organizations','Foreign investors/enterprises; foreign peoples','July30 candidate corrected by Aug9 R8A'],
 ['COMMERCIAL_INSTITUTION','Organized commercial institutions','Banks, financial systems, companies, enterprises, business associations','Individual businesspeople/investors','Aug9 commercial source-first closure'],
 ['MEDIA_INSTITUTION','Institutional media organizations/channels as confidence targets','Press, newspapers, television, radio, media','Media-use frequency; proposition-specific information credibility unless explicitly institution confidence','Current R10G media institution coordinate + trust boundary work'],
],columns=['institution_class','definition','includes','excludes','ancestry_basis'])
ontology['authority_status']='T08_R4_CONTROLLED_CLASS_VOCABULARY__NARROWING_NOT_FINAL_S14_AUTHORITY'
ontology.to_csv(OUT/'NARROWING/T08_INSTITUTION_CLASS_ONTOLOGY_R4.csv',index=False)

# Summary report/status
summary={
 'checkpoint':'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R4_20260811',
 'status':'IN_PROGRESS_NOT_FROZEN','active_state':'R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR',
 'job3_authorized':False,'o12_r2_811_complete_authority':False,'workers_launched':False,
 't08':{
   'controlled_institution_classes':len(ontology),
   'semantic_units_in_mapping_ledger':len(mapped),
   'mapped_current_or_source_first_units':int(mapped['institution_class'].fillna('').ne('').sum()),
   'r6_t08_canaries_total':len(can_df),
   'r6_t08_canaries_accounted':int(can_df.canary_recovery_status.str.startswith('RECOVERED_R6_T08_RELATION').sum()),
   'r6_t08_canaries_clean':int((can_df.canary_recovery_status=='RECOVERED_R6_T08_RELATION').sum()),
   'r6_t08_canaries_member_boundary_review':int((can_df.canary_recovery_status=='RECOVERED_R6_T08_RELATION__MEMBER_BOUNDARY_REVIEW').sum()),
   'r6_t08_canaries_upstream_semantic_gap':int((can_df.canary_recovery_status=='RECOVERED_R6_T08_RELATION__UPSTREAM_SEMANTIC_GAP_EXPLICIT').sum()),
   'o11_proxy_groups_accounted':len(proxy_df),
   'r14_accepted_objects_accounted':len(r14df),
   'r14_novel_review_objects':int(r14df.disposition.str.startswith('EMIT_T08').sum()),
   'r14_known_r6_objects_or_aliases':int((r14df.disposition=='KNOWN_R6_T08_SOURCE_OBJECT_OR_ALIAS__NO_NEW_ADJUDICATION').sum()),
   'cross_object_recall_groups_total':len(crossdf),
   'cross_object_review_hyperedges':int((crossdf.disposition=='EMIT_CROSS_OBJECT_T08_RECALL_HYPEREDGE').sum()),
   'canonical_review_packets':len(pk),
   'next_dependency':'T09 reciprocal roles'
 },
 'remaining_major_rules':['T09','T10','T11'],
 'next_decision':'finish T09-T11, cross-rule packet dedupe, then worker economics',
 'repair_stack':{'done':[1,7,8],'partial':[2,3,4,5,6,9,10,14,15,23],'open':[11,12,13,16,17,18,19,20,21,22,24,25]}
}
json.dump(summary,open(OUT/'CURRENT_STATUS_R4.json','w'),indent=2)

report=f'''# T08 Institution-Class Narrowing — Checkpoint R4\n\n## Status\n\n**T08 class bridge narrowed and packetized; not final S14 relation authority. Job 3 remains blocked.**\n\n## Governing correction\nT08 requires an orthogonal institution-class mapping. Current R10G target identity/facet coordinates remain unchanged. The R4 class bridge reuses current R10G coordinates and later source-first semantic boundaries without claiming that R10G itself already contained an `institution_class` field.\n\nThe older O11 139-group trust/institution proxy is fully dispositioned but is not the T08 denominator. R6 T08 proves T08 can include non-trust evaluative predicates such as institutional authority/legitimacy.\n\n## Controlled class vocabulary\nR4 uses {len(ontology)} bounded classes: {', '.join(ontology.institution_class)}. Exact targets remain separately preserved.\n\n## R6 canaries\n- sealed T08 relations: **{len(can_df)}**\n- fully recovered with >=2 mapped institution classes: **{int(can_df.canary_recovery_status.str.startswith('RECOVERED_R6_T08_RELATION').sum())}**\n- class-gap/review canaries: **{int((~can_df.canary_recovery_status.str.startswith('RECOVERED_R6_T08_RELATION')).sum())}**\n\n## Denominator/accounting surfaces\n- semantic units in class-mapping ledger: **{len(mapped)}**\n- institution-class mapped units: **{int(mapped['institution_class'].fillna('').ne('').sum())}**\n- old O11 proxy groups dispositioned: **{len(proxy_df)}**\n- accepted R14 source objects dispositioned: **{len(r14df)}**\n- exact R14 multiclass review objects: **{int(r14df.disposition.str.startswith('EMIT_T08').sum())}**\n- same-wave same-predicate cross-object recall hyperedges: **{len(crossdf)}**\n- canonical unresolved T08 review packets: **{len(pk)}**\n\n## Epistemic ceilings\n- facet/class mapping is a bridge input, not a relation verdict.\n- source-object co-membership is retrieval evidence, not T08 truth.\n- cross-object same-predicate groups are recall only pending exact source/parallel-target adjudication.\n- no lexical similarity, embedding, source proximity, or R14 excerpt text authorizes a T08 relation.\n- August-9 source-first trust closures are reused as class-boundary evidence, but their unfinished global `trustEcology` denominator claim is not inherited.\n\n## Next\n**T09 reciprocal-role narrowing.** Final T08 semantic acceptance happens with the common S14 bridge queue at repair-stack item 18.\n'''
open(OUT/'T08_NARROWING_R4_REPORT.md','w').write(report)

readme=f'''# README FIRST — S14 Relation-Role Bridge Repair Checkpoint R4\n\nState: `R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR`\nScope: T08 institution-class narrowing successor to T07 R3.\nJob 3 authorized: **NO**\n811 final denominator: **NO**\n\nRead: `T08_NARROWING_R4_REPORT.md`, class ontology/mapping, R6 canary recovery, R14 disposition, O11 proxy disposition, packets, `CURRENT_STATUS_R4.json`, `NEXT_EXECUTION_STEPS.md`.\n\nExact next operation: **T09 reciprocal roles**.\n'''
open(OUT/'00_README_FIRST.md','w').write(readme)
open(OUT/'NEXT_EXECUTION_STEPS.md','w').write('''# Exact Resume Sequence after T08 R4\n\n1. **T09 reciprocal roles** — recover actor, recipient, proposition/action, direction and reversed direction; recover/account the known R6 T09 positive; search cross-object structures; never use wording symmetry as authority.\n2. **T10 target×condition matrices**.\n3. **T11 complementary roles**.\n4. **Compress + cross-rule dedupe T03–T11 packets**.\n5. **Measure worker economics**.\n6. **Adjudicate/freeze S14 relational-structure authority**.\n7. **Rebuild O11/S16** from actual repaired prerequisites.\n8. **Rebuild O12 T01–T13**, including T01 grain audit.\n9. **Independent completeness reconstruction + causal topology audit**.\n10. Only then freeze O12 and launch Job 3.\n''')

# Parent pins by sha
pins={}
for name,p in [('CANONICAL_IMPLEMENTATION_REGISTRY',CANON),('R6_RELATION_AUTHORITY',R6),('R14_SOURCE_NATIVE',R14),('R10G_COORDINATE_AUTHORITY',R10G)]:
    h=hashlib.sha256(open(p,'rb').read()).hexdigest(); pins[name]={'path':str(p),'sha256':h}
json.dump(pins,open(OUT/'PROVENANCE/PARENT_PINS_R4.json','w'),indent=2)

# Validation independent-ish counts/invariants
checks=[]
def chk(name,cond,detail=''):
    checks.append({'check':name,'pass':bool(cond),'detail':detail})
chk('r6_t08_count_20',len(can_df)==20,len(can_df))
chk('r6_all_impl_ids_resolved',(can_df.resolved_member_count==can_df.member_count).all(),can_df[['relation_authority_id','member_count','resolved_member_count']].to_dict('records'))
chk('r6_canaries_all_accounted',can_df.canary_recovery_status.str.startswith('RECOVERED_R6_T08_RELATION').all(),can_df[['relation_authority_id','distinct_institution_class_count','unmapped_or_noninstitution_member_count','member_gap_statuses_json','canary_recovery_status']].to_dict('records'))
chk('r6_canaries_have_multiclass_core',(can_df.distinct_institution_class_count>=2).all(),can_df[['relation_authority_id','distinct_institution_class_count']].to_dict('records'))
chk('o11_proxy_count_139',len(proxy_df)==139,len(proxy_df))
chk('r14_accepted_count',len(r14df)==sum(1 for o in r14 if o.get('state')=='ACCEPTED_SOURCE_NATIVE_JOINT'),len(r14df))
chk('no_empty_r14_disposition',r14df.disposition.fillna('').ne('').all())
chk('no_empty_proxy_disposition',proxy_df.disposition.fillna('').ne('').all())
chk('ontology_9_classes',len(ontology)==9,len(ontology))
chk('no_final_accept_in_packets',not pk.get('status',pd.Series(dtype=str)).astype(str).str.contains('ACCEPT|AUTHORITY',case=False,regex=True).any())
chk('job3_blocked',summary['job3_authorized'] is False)
chk('next_t09',summary['t08']['next_dependency']=='T09 reciprocal roles')
# ensure direct R10G facet mappings not collision
instmap=mapped[mapped.institution_class.fillna('').ne('')]
chk('one_class_per_semantic_unit',instmap.groupby('sem__audit_unit_id').institution_class.nunique().max()<=1 if len(instmap) else True)
errors=[c for c in checks if not c['pass']]
val={'validator':'validate_t08_checkpoint_r4.py-equivalent-inline','status':'PASS' if not errors else 'FAIL','checks':len(checks),'errors':len(errors),'details':checks}
json.dump(val,open(OUT/'VALIDATION/VALIDATION_RESULT_R4.json','w'),indent=2)
print(json.dumps(summary,indent=2))
print('VALIDATION',val['status'],len(checks),len(errors))
if errors:
  print('ERRORS',json.dumps(errors,indent=2))
