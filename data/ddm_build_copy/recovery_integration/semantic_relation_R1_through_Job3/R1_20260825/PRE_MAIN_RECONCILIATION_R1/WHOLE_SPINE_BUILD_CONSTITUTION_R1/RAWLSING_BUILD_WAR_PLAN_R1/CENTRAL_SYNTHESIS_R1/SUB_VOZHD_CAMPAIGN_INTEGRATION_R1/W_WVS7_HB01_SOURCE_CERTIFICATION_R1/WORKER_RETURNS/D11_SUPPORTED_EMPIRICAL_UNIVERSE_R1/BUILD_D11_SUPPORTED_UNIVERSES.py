from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

SOURCE_SHA = '2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d'
D12_REPLAY_HASH = '9d44d5097258b96c5c49faf968b85701f80ecd75df6b214a528abb6fb15ef44b'
D12_REPLAY_REF = {
    'kind':'SCOPED_RESPONDENT_REPLAY',
    'object_id':f'urn:rawlsing:pre553:gsr07:wvs7:d12-scoped-respondent-replay:sha256:{D12_REPLAY_HASH}',
    'content_hash':D12_REPLAY_HASH,
}
D12_LEDGER_SHA = 'cf0dfaae7a2f0f19b34ccc536b93e6aedbf37bf047d5d864e5c812fe9602d6a9'
URN_PREFIX='urn:rawlsing:pre553'

# Exact PRE553 identity law subset from rawlsing_next/pre553_empirical_objects.py.
def canonicalize(value):
    if value is None or isinstance(value,(str,bool,int)):
        return value
    if isinstance(value,float):
        raise ValueError('float/NaN/Infinity forbidden in semantic identity')
    if isinstance(value,dict):
        if any(not isinstance(k,str) for k in value): raise ValueError('mapping keys must be strings')
        return {k:canonicalize(value[k]) for k in sorted(value)}
    if isinstance(value,(list,tuple)):
        return [canonicalize(v) for v in value]
    if isinstance(value,(set,frozenset)):
        mats=[canonicalize(v) for v in value]
        return sorted(mats,key=canonical_json)
    raise ValueError(type(value).__name__)

def canonical_json(value):
    return json.dumps(canonicalize(value),sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)

def semantic_hash(value):
    return hashlib.sha256(canonical_json(value).encode('utf-8')).hexdigest()

def exact_ref(kind, object_id, content_hash):
    assert len(content_hash)==64 and content_hash==content_hash.lower()
    return {'kind':kind,'object_id':object_id,'content_hash':content_hash}

def derived_ref(kind, namespace, material):
    h=semantic_hash(material)
    return exact_ref(kind,f'urn:rawlsing:pre553:gsr07:wvs7:{namespace}:sha256:{h}',h)

def authority_ref(authority_id, authority_version, authority_content_hash):
    return {'authority_id':authority_id,'authority_version':authority_version,'authority_content_hash':authority_content_hash}

def canon_set(values):
    by={canonical_json(canonicalize(v)):canonicalize(v) for v in values}
    return [by[k] for k in sorted(by)]

def build_public_object(family, typed_state, authority_snapshot_refs, dependency_refs, replay_root, semantic_fields, set_like_fields=()):
    family_name,family_version=family.split('@',1)
    normalized={}
    for k,v in semantic_fields.items():
        normalized[k]=canon_set(v) if k in set_like_fields else canonicalize(v)
    # Match PRE553 _canonical_authority_ref_set / _canonical_ref_set ordering exactly.
    auths=sorted(canon_set(authority_snapshot_refs), key=lambda r: f"{r['authority_id']}|{r['authority_version']}|{r['authority_content_hash']}")
    deps=sorted(canon_set(dependency_refs), key=lambda r: f"{r['kind']}|{r['object_id']}|{r['content_hash']}")
    projection={
        'schema_id':family_name,
        'schema_version':family_version,
        'typed_state':typed_state,
        'authority_snapshot_refs':auths,
        'dependency_refs':deps,
        'producer_replay_locator_or_reference_root':canonicalize(replay_root),
        'semantic_fields':normalized,
    }
    digest=semantic_hash(projection)
    return {**projection,'object_id':f'{URN_PREFIX}:{family_name}:sha256:{digest}','content_hash':digest}

SCOPES=[
 {
  'slug':'australia-2018','country':'Australia','year':2018,'S025':362018,'B_COUNTR':36,
  'first':3231,'last':5043,'count':1813,
  'scope_hash':'698ff2e5c73274cf6961875aacf8d059c8b105d5357605a40eebfd10870bb7a3',
  'target':'Adults 18+ resident in private households in Australia',
  'frame':'Address-based sampling; mail primary contact',
  'design':'Sequential mixed-mode; self-completion online/paper; fieldwork 2018-04-03 through 2018-08-06; N=1813; response=30.2%',
  'design_detail':None,
  'sampling_geography':'Australia national private-household resident population age 18+',
  'field_time':'2018-04-03/2018-08-06',
  'evidence_refs':[
    'git:930d89b8930c21c9a8f1180093ee15ed10c495e4:GSR07R2C_WVS7_COUNTRY_UNIVERSE_DOCUMENTARY_RECOVERY',
    'git:efca0824b87415b9a99991b989eb0c8334cdcd9d:GSR07R3_WVS7_POSTBATCH_HQ_JOIN',
    'wvsa:WVSNewsShow.jsp?ID=389:WVS-Australia analytical report release',
    'wvsa:WVSNewsShow.jsp?ID=396:WVS-Australia ACSPRI methodology presentation',
  ],
 },
 {
  'slug':'great-britain-2022','country':'United Kingdom - Great Britain','year':2022,'S025':8262022,'B_COUNTR':826,
  'first':27005,'last':29613,'count':2609,
  'scope_hash':'26fb03ee5d097f0b38c6d3a86040dfd51354ec1bf0eddd85156972a670781f4c',
  'target':'Adult population age 18+ in Great Britain (England, Scotland and Wales). No groups excluded or under-represented; Scotland and Wales intentionally over-represented for analysis, with post-survey weighting for national representativeness.',
  'frame':'Royal Mail Postcode Address File (PAF), Small User version, excluding high-volume business addresses.',
  'design':'Two-stage address probability sample: stratified random PPS selection of postcode sectors, then 30 addresses per selected sector from PAF; one adult age 18+ randomly selected within participating household.',
  'design_detail':'273 postcode sectors in Great Britain; 56 in Scotland and 45 in Wales. Stratifiers: country/region, population-density tertiles, percentage owner-occupied. Rare multi-household addresses randomly subsampled electronically.',
  'sampling_geography':'Great Britain (England, Scotland and Wales), adult population age 18+',
  'field_time':'2022',
  'evidence_refs':[
    'git:471b64953b58cd39baf9368358ef782c6308957c:GSR07R3_WVS7_DOCUMENTARY_RECOVERY_W6',
    'git:efca0824b87415b9a99991b989eb0c8334cdcd9d:GSR07R3_WVS7_POSTBATCH_HQ_JOIN',
    'ihsn:catalog/12279/resource/104788:WVS7 Methodology Report Great Britain 2022',
    'ukds:SN9311:9311_wvs7_methodology_report_great_britain_2022.pdf',
  ],
 },
 {
  'slug':'northern-ireland-2022','country':'United Kingdom - Northern Ireland','year':2022,'S025':9092022,'B_COUNTR':909,
  'first':63239,'last':63685,'count':447,
  'scope_hash':'f59a8ec788a92d7b3f89b350d4b827869c918102d555169c8df2d44ce6bc5347',
  'target':'Entire adult population age 18+ of Northern Ireland; no groups excluded, over-represented, or under-represented.',
  'frame':'Royal Mail Postcode Address File (PAF), Small User version, excluding high-volume business addresses.',
  'design':'Two-stage address probability sample: stratified random PPS selection of postcode sectors, then 30 addresses per selected sector from PAF; one adult age 18+ randomly selected within participating household.',
  'design_detail':'45 postcode sectors, 30 addresses each. Stratifiers: population-density tertiles and percentage owner-occupied. Rare multi-household addresses randomly subsampled electronically.',
  'sampling_geography':'Northern Ireland, entire adult population age 18+',
  'field_time':'2022',
  'evidence_refs':[
    'git:471b64953b58cd39baf9368358ef782c6308957c:GSR07R3_WVS7_DOCUMENTARY_RECOVERY_W6',
    'git:efca0824b87415b9a99991b989eb0c8334cdcd9d:GSR07R3_WVS7_POSTBATCH_HQ_JOIN',
    'ihsn:catalog/12294/resource/104864:WVS7 Methodology Report Northern Ireland 2022',
    'ukds:SN9311:9311_wvs7_methodology_report_northern_ireland_2022.pdf',
  ],
 },
]

assert len(SCOPES)==3
assert {x['S025'] for x in SCOPES}=={362018,8262022,9092022}

MATERIALIZER_PROTOCOL=derived_ref('REPLAY_PROTOCOL','d11-supported-universe-materializer-protocol',{
 'contract':'WVS7_HB01_D11_SUPPORTED_EMPIRICAL_UNIVERSE_R1',
 'canonicalization':'PRE553_CANONICAL_JSON_SEMANTIC_HASH',
 'source_sha256':SOURCE_SHA,
 'd12_replay_ref':D12_REPLAY_REF,
 'd12_scope_ledger_sha256':D12_LEDGER_SHA,
 'authorized_scope_keys':sorted([f"{x['S025']}|{x['B_COUNTR']}|{x['year']}" for x in SCOPES]),
 'forbidden_universe_count':63,
})

def authority_snapshot(scope):
    documentary_material={
      'contract':'WVS7_HB01_D11_COUNTRY_UNIVERSE_DOCUMENTARY_AUTHORITY@1.0.0',
      'country':scope['country'],'year':scope['year'],
      'source_scope':{'S025':scope['S025'],'B_COUNTR':scope['B_COUNTR'],'A_YEAR':scope['year']},
      'positive_claims':{
        'target_population_or_coverage':scope['target'],
        'sample_frame':scope['frame'],
        'actual_sampling_design':scope['design'],
        'positive_design_detail':scope['design_detail'],
      },
      'evidence_refs':sorted(scope['evidence_refs']),
      'limits':[
        'NO_WEIGHT_OR_ESTIMAND_AUTHORITY',
        'NO_VARIANCE_ESTIMATOR_AUTHORITY_FROM_DESIGN_FACT_ALONE',
        'NO_ROUTING_AUTHORITY',
        'NO_SOURCE_RELATION_AUTHORITY',
        'NO_CROSS_COUNTRY_GENERALIZATION',
      ],
    }
    authority_content_hash=semantic_hash(documentary_material)
    aid=f"WVS7-HB01-D11-COUNTRY-UNIVERSE-{scope['slug'].upper()}"
    interpretation=semantic_hash({
      'positive_claim_grain_only':True,
      'unknowns_preserved_fail_closed':True,
      'no_incidence_missingness_complement_inference':True,
      'country_scope':scope['slug'],
    })
    replay_root=derived_ref('REPLAY_ROOT','d11-country-universe-authority-root',{
      'authority_content_hash':authority_content_hash,
      'materializer_protocol_ref':MATERIALIZER_PROTOCOL,
      'd12_replay_ref':D12_REPLAY_REF,
    })
    fields={
      'authority_id':aid,
      'authority_version':'1.0.0',
      'authority_content_hash':authority_content_hash,
      'authority_kind':'SOURCE_SEMANTICS_TOPOLOGY',
      'decision_state':'ALLOW',
      'governed_operations':('MATERIALIZE_EXACT_SUPPORTED_WVS7_EMPIRICAL_UNIVERSE',),
      'governed_object_families':('EmpiricalUniverse@1.0.0',),
      'scope_envelope':documentary_material,
      'effective_time_or_interval':str(scope['year']),
      'parent_authority_refs':(),
      'negative_limit_refs':(),
      'supersession_refs':(),
      'interpretation_semantics_fingerprint':interpretation,
      'replay_protocol_ref':MATERIALIZER_PROTOCOL,
    }
    obj=build_public_object('AuthoritySnapshot@1.0.0','ALLOW',(),(),replay_root,fields,
      {'governed_operations','governed_object_families','parent_authority_refs','negative_limit_refs','supersession_refs'})
    aref=authority_ref(aid,'1.0.0',authority_content_hash)
    return obj,aref

def universe(scope, auth_ref):
    scope_member_ref=exact_ref('SOURCE_SCOPE_MEMBER_SET',
      f"urn:rawlsing:pre553:gsr07:wvs7:source-scope-member-set:sha256:{scope['scope_hash']}",scope['scope_hash'])
    source_scope={'S025':scope['S025'],'B_COUNTR':scope['B_COUNTR'],'A_YEAR':scope['year']}
    lineage={
      'source_sha256':SOURCE_SHA,
      'source_artifact':'WVS Wave 7.sav',
      'source_archive':'F00010733-WVS_Cross-National_Wave_7_spss_v6_0.zip',
      'source_scope':source_scope,
      'source_row_ordinal_first':scope['first'],
      'source_row_ordinal_last':scope['last'],
      'source_row_count':scope['count'],
      'source_scope_member_set_ref':scope_member_ref,
      'd12_replay_ref':D12_REPLAY_REF,
      'd12_scope_ledger_sha256':D12_LEDGER_SHA,
    }
    replay_root=derived_ref('REPLAY_ROOT','d11-supported-universe-root',{
      'source_scope_member_set_ref':scope_member_ref,
      'd12_replay_ref':D12_REPLAY_REF,
      'materializer_protocol_ref':MATERIALIZER_PROTOCOL,
      'authority_ref':auth_ref,
    })
    fields={
      'raw_source_identity':{
        'source_sha256':SOURCE_SHA,
        'source_artifact':'WVS Wave 7.sav',
        'source_scope':source_scope,
      },
      'source_family':'WORLD_VALUES_SURVEY_WAVE_7',
      'study_product_release':{
        'archive':'F00010733-WVS_Cross-National_Wave_7_spss_v6_0.zip',
        'contained_source':'WVS Wave 7.sav',
      },
      'instrument_release':'WVS Wave 7 (2017) Questionnaire',
      'country_geography':scope['country'],
      'sampling_geography':scope['sampling_geography'],
      'raw_wave':'WVS Wave 7',
      'canonical_wave_if_governed':None,
      'field_or_reference_time':scope['field_time'],
      'target_population_and_sample_frame':{
        'target_population_or_coverage':scope['target'],
        'sample_frame':scope['frame'],
      },
      'sampling_design_regime':{
        'actual_sampling_design':scope['design'],
        'positive_design_detail':scope['design_detail'],
      },
      'respondent_namespace':scope_member_ref,
      'source_artifact_import_lineage':lineage,
      'harmonization_authority_ref':None,
      'source_relation_refs':(),
    }
    obj=build_public_object('EmpiricalUniverse@1.0.0','UNIVERSE_IDENTIFIED',(auth_ref,),
      (scope_member_ref,D12_REPLAY_REF),replay_root,fields,{'source_relation_refs'})
    return obj

def main(outdir):
    out=Path(outdir); out.mkdir(parents=True,exist_ok=True)
    auth_objs=[]; universes=[]
    for s in SCOPES:
        a,ar=authority_snapshot(s)
        u=universe(s,ar)
        auth_objs.append(a); universes.append(u)
    assert len(auth_objs)==3 and len(universes)==3
    assert len({x['object_id'] for x in auth_objs})==3
    assert len({x['object_id'] for x in universes})==3
    payload_a={'schema':'wvs7-hb01-d11-country-universe-authority-snapshots-v1','count':3,'objects':auth_objs}
    payload_u={'schema':'wvs7-hb01-d11-supported-empirical-universes-v1','accepted_count':3,'fail_closed_unmaterialized_count':63,'objects':universes}
    pa=out/'COUNTRY_UNIVERSE_AUTHORITY_SNAPSHOTS.json'; pu=out/'EMPIRICAL_UNIVERSE_OBJECTS.json'
    pa.write_text(json.dumps(payload_a,indent=2,sort_keys=True,ensure_ascii=False)+'\n')
    pu.write_text(json.dumps(payload_u,indent=2,sort_keys=True,ensure_ascii=False)+'\n')
    receipt={
      'authority_snapshot_count':3,
      'empirical_universe_count':3,
      'unmaterialized_fail_closed_source_scope_count':63,
      'authority_file_sha256':hashlib.sha256(pa.read_bytes()).hexdigest(),
      'universe_file_sha256':hashlib.sha256(pu.read_bytes()).hexdigest(),
      'authority_object_refs':[{'object_id':x['object_id'],'content_hash':x['content_hash']} for x in auth_objs],
      'empirical_universe_refs':[{'object_id':x['object_id'],'content_hash':x['content_hash']} for x in universes],
      'source_sha256':SOURCE_SHA,
      'd12_replay_ref':D12_REPLAY_REF,
      'd12_scope_ledger_sha256':D12_LEDGER_SHA,
      'materializer_protocol_ref':MATERIALIZER_PROTOCOL,
      'no_fourth_universe':True,
      'D_INTERVIEW_used_as_canonical_identity':False,
      'S007_used_as_canonical_identity':False,
      'source_relation_default_applied':False,
      'missingness_incidence_or_complement_inference_used':False,
    }
    (out/'RUN_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps(receipt,sort_keys=True))

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: BUILD_D11_SUPPORTED_UNIVERSES.py OUTDIR')
    main(sys.argv[1])
