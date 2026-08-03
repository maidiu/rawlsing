from __future__ import annotations
import csv, json, hashlib, os, re, shutil, zipfile, textwrap, datetime, collections
from pathlib import Path
import yaml

SRC = Path('/mnt/data/rawlsing_v22_reaudit/Rawlsing_J_Family_Authority_Strategy_Handoff_v22_20260731')
OUTBASE = Path('/mnt/data/rawlsing_v23_build')
ROOT = OUTBASE/'Rawlsing_J_Family_Authority_Strategy_Handoff_v23_20260731'
SEC = ROOT/'45_P3_PLAN_SECOND_ACCEPTANCE_AUDIT_AND_HARDENING'
if OUTBASE.exists(): shutil.rmtree(OUTBASE)
shutil.copytree(SRC, ROOT)
SEC.mkdir(parents=True)
for d in ['upstream','schemas','sql','algorithms','adjudication','downstream','release','validation']:
    (SEC/d).mkdir(parents=True,exist_ok=True)

def sha(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()
def read_csv(p):
    with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def write_csv(p, rows, fieldnames=None):
    p.parent.mkdir(parents=True,exist_ok=True)
    if fieldnames is None:
        fieldnames=list(rows[0].keys()) if rows else []
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fieldnames,extrasaction='ignore');w.writeheader();w.writerows(rows)
def dumpj(p,obj): p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding='utf-8')

V22 = SRC/'44_P3_PLAN_ACCEPTANCE_AUDIT_AND_CORRECTION'
P2C = ROOT/'42_P2_GLOBAL_CROSS_TRANCHE_CLOSURE'
LINP = ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1/Rawlsing_P2_All_Nine_Source_Local_Lineage_Registry_v1.csv'
SEM_P = P2C/'Rawlsing_P2_Global_Semantic_Priority_Pair_Authority_Registry_v1.csv'
EX_P = P2C/'Rawlsing_P2_Global_Exact_Foundation_Authority_Registry_v1.csv'

# ---------- upstream canonical surfaces ----------
sem=read_csv(SEM_P); ex=read_csv(EX_P); lin=read_csv(LINP)
def pair_key(r): return '|'.join(sorted((r['left_lineage_id'],r['right_lineage_id'])))
sem_by={pair_key(r):r for r in sem}; ex_by={pair_key(r):r for r in ex}
all_keys=sorted(set(sem_by)|set(ex_by))
# effective surface copied/rebuilt
_eff=[]; source_rows=[]
for k in all_keys:
    if k in sem_by:
        r=sem_by[k]
        eff={
            'pair_key':k,'governing_registry':'SEMANTIC_PRIORITY_CLOSURE','governing_authority_id':r['global_semantic_authority_id'],
            'left_lineage_id':r['left_lineage_id'],'right_lineage_id':r['right_lineage_id'],
            'normalized_authority_class':r['normalized_authority_class'],'authority_status':r['authority_status'],
            'source_portability_ceiling':r['portability_ceiling'],'supersedes_exact_foundation_overlap':'YES' if k in ex_by else 'NO'
        }
        source_rows.append({'pair_key':k,'registry_code':'SEMANTIC_PRIORITY_CLOSURE','authority_id':r['global_semantic_authority_id'],'authority_role':'GOVERNING','superseded_by_authority_id':'','left_lineage_id':r['left_lineage_id'],'right_lineage_id':r['right_lineage_id']})
        if k in ex_by:
            x=ex_by[k]
            source_rows.append({'pair_key':k,'registry_code':'EXACT_FOUNDATION_CLOSURE','authority_id':x['cross_source_candidate_id'],'authority_role':'SUPERSEDED_PROVENANCE','superseded_by_authority_id':r['global_semantic_authority_id'],'left_lineage_id':x['left_lineage_id'],'right_lineage_id':x['right_lineage_id']})
    else:
        x=ex_by[k]
        eff={
            'pair_key':k,'governing_registry':'EXACT_FOUNDATION_CLOSURE','governing_authority_id':x['cross_source_candidate_id'],
            'left_lineage_id':x['left_lineage_id'],'right_lineage_id':x['right_lineage_id'],
            'normalized_authority_class':x['normalized_authority_class'],'authority_status':x['authority_status'],
            'source_portability_ceiling':x['portability_ceiling'],'supersedes_exact_foundation_overlap':'NO'
        }
        source_rows.append({'pair_key':k,'registry_code':'EXACT_FOUNDATION_CLOSURE','authority_id':x['cross_source_candidate_id'],'authority_role':'GOVERNING','superseded_by_authority_id':'','left_lineage_id':x['left_lineage_id'],'right_lineage_id':x['right_lineage_id']})
    _eff.append(eff)
write_csv(SEC/'upstream/P3_EFFECTIVE_UPSTREAM_PAIR_AUTHORITY_SURFACE_v3.csv',_eff)
write_csv(SEC/'upstream/P3_EFFECTIVE_PAIR_SOURCE_AUTHORITY_SURFACE_v3.csv',source_rows)

# mapping v3 from v22 plus family eligibility column
map2=read_csv(V22/'upstream/P3_P2_TO_P3_AUTHORITY_MAPPING.csv')
map3=[]
for r in map2:
    q=dict(r); q['proposition_graph_allowed']=q.pop('connectivity_allowed'); q['j_family_candidate_default']='YES' if q['proposition_graph_allowed']=='YES' else 'NO'; map3.append(q)
write_csv(SEC/'upstream/P3_P2_TO_P3_AUTHORITY_MAPPING_v3.csv',map3)
shutil.copy2(V22/'upstream/P3_UPSTREAM_AUTHORITY_PRECEDENCE.csv',SEC/'upstream/P3_UPSTREAM_AUTHORITY_PRECEDENCE_v3.csv')

# derive effective mapped classes, incident lineage coverage, administrative preflight
M={(r['upstream_registry'],r['upstream_normalized_authority_class'],r['upstream_authority_status'],r['upstream_portability_ceiling']):r for r in map3}
lin_by={r['lineage_id']:r for r in lin}
all_ep=collections.Counter(); prop_ep=collections.Counter(); eff_counts=collections.Counter(); prop_rows=[]
for r in _eff:
    m=M[(r['governing_registry'],r['normalized_authority_class'],r['authority_status'],r['source_portability_ceiling'])]
    eff_counts[m['p3_relation_type']]+=1
    all_ep[r['left_lineage_id']]+=1;all_ep[r['right_lineage_id']]+=1
    if m['proposition_graph_allowed']=='YES':
        prop_rows.append((r,m));prop_ep[r['left_lineage_id']]+=1;prop_ep[r['right_lineage_id']]+=1

admin_pairs=[]
for r,m in prop_rows:
    flagged=[]
    for lid in (r['left_lineage_id'],r['right_lineage_id']):
        x=lin_by[lid]
        roles=' '.join(json.loads(x['semantic_roles_json'])+json.loads(x['semantic_subroles_json'])+json.loads(x['response_topologies_json'])).lower()
        txt=x['representative_text'].lower()
        flagged.append(('administrative' in roles or 'identifier_weight_sampling_or_processing' in roles or 'respondent had difficulty answering' in txt or 'interviewer' in txt))
    if all(flagged):
        admin_pairs.append(r['pair_key'])

particip=[]
for r in lin:
    lid=r['lineage_id']
    if prop_ep[lid]: status='PROPOSITION_GRAPH_INCIDENT'
    elif all_ep[lid]: status='CONSTRAINT_ONLY_INCIDENT'
    else: status='NO_CURRENT_DIRECT_PAIR_AUTHORITY'
    particip.append({
        'lineage_id':lid,'source_family':r['source_family'],'participation_status':status,
        'effective_pair_incident_count':all_ep[lid],'proposition_pair_incident_count':prop_ep[lid],
        'signature_requirement':'FULL_P3A_SIGNATURE' if status!='NO_CURRENT_DIRECT_PAIR_AUTHORITY' else 'DEFER_UNTIL_NEW_AUTHORITY_OR_ATTACHMENT',
        'authority_note':'Absence from current direct-pair surface is not evidence of semantic uniqueness or permanent exclusion.' if status=='NO_CURRENT_DIRECT_PAIR_AUTHORITY' else ''
    })
write_csv(SEC/'upstream/P3_LINEAGE_PARTICIPATION_BASELINE_v3.csv',particip)
# Pair-level substantive eligibility preflight. Proposition authority is preserved even when downstream J-family candidacy is administrative-only.
elig=[]
for r,m in prop_rows:
    lk=lin_by[r['left_lineage_id']]; rk=lin_by[r['right_lineage_id']]
    is_admin=r['pair_key'] in admin_pairs
    elig.append({'pair_key':r['pair_key'],'governing_registry':r['governing_registry'],'governing_authority_id':r['governing_authority_id'],'p3_relation_type':m['p3_relation_type'],
                 'left_lineage_id':r['left_lineage_id'],'right_lineage_id':r['right_lineage_id'],'left_source_family':lk['source_family'],'right_source_family':rk['source_family'],
                 'proposition_graph_allowed':'YES','provisional_j_family_eligibility':'ADMINISTRATIVE_METADATA_ONLY' if is_admin else 'J_FAMILY_CANDIDATE_ELIGIBLE',
                 'preflight_rationale':'Interviewer or fieldwork administrative proposition; preserve outside substantive J-family connectivity.' if is_admin else 'Substantive proposition preflight; P3A must recompute from complete field-provenanced signatures.'})
write_csv(SEC/'upstream/P3_PROPOSITION_RELATION_ELIGIBILITY_PREFLIGHT_v3.csv',elig)
# Graph diagnostics only: these are not candidate components or family authority.
def graph_stats(edge_rows):
    parent={}
    def find(x):
        parent.setdefault(x,x)
        if parent[x]!=x: parent[x]=find(parent[x])
        return parent[x]
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[rb]=ra
    for a,b in edge_rows: union(a,b)
    groups=collections.defaultdict(list)
    for x in parent: groups[find(x)].append(x)
    sizes=sorted((len(v) for v in groups.values()),reverse=True)
    return {'node_count':len(parent),'component_count':len(groups),'largest_component_size':max(sizes or [0]),'largest_component_sizes':sizes[:20]}
all_prop_edges=[tuple(r['pair_key'].split('|')) for r,m in prop_rows]
sub_prop_edges=[tuple(r['pair_key'].split('|')) for r,m in prop_rows if r['pair_key'] not in admin_pairs]
strict_edges=[tuple(r['pair_key'].split('|')) for r,m in prop_rows if m['p3_relation_type']=='PROPOSITION_RESPONSE_IDENTITY']
dumpj(SEC/'upstream/P3_PROPOSITION_GRAPH_PREFLIGHT_RETURN_v3.json',{'authority_status':'DIAGNOSTIC_ONLY_NOT_CANDIDATE_INVENTORY','all_proposition_graph':graph_stats(all_prop_edges),'provisional_substantive_graph':graph_stats(sub_prop_edges),'strict_response_identity_graph':graph_stats(strict_edges),'all_proposition_edges':len(all_prop_edges),'provisional_substantive_edges':len(sub_prop_edges),'strict_response_identity_edges':len(strict_edges)})

# comprehensive upstream input manifest
inputs=[
 ('SEMANTIC_PRIORITY_PAIR_AUTHORITY',SEM_P,18831),('EXACT_FOUNDATION_PAIR_AUTHORITY',EX_P,751),('SOURCE_LOCAL_LINEAGES',LINP,13526),
 ('SOURCE_STRUCTURE_REGISTRY',ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1/Rawlsing_P2_Normalized_Source_Structure_Registry_v1.csv',2499),
 ('SOURCE_STRUCTURE_MEMBERSHIPS',ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1/Rawlsing_P2_Normalized_Source_Structure_Memberships_v1.csv',15990),
 ('STRUCTURE_ANALOGY_RULINGS',ROOT/'33_P2_GLOBAL_REWORDED_RELATION_AXIS_STRUCTURE_ADJUDICATION_TRANCHE2/Rawlsing_P2_Structure_Analogy_Rulings_v1.csv',19),
 ('STRUCTURE_MEMBER_RULINGS',ROOT/'33_P2_GLOBAL_REWORDED_RELATION_AXIS_STRUCTURE_ADJUDICATION_TRANCHE2/Rawlsing_P2_Structure_Member_Correspondence_Rulings_v1.csv',119),
 ('SEMANTIC_CORRECTION_OVERLAY',ROOT/'33_P2_GLOBAL_REWORDED_RELATION_AXIS_STRUCTURE_ADJUDICATION_TRANCHE2/Rawlsing_P2_Semantic_Reference_Correction_Overlay_v1.csv',30),
 ('SEMANTIC_ANOMALY_RESOLUTION',ROOT/'33_P2_GLOBAL_REWORDED_RELATION_AXIS_STRUCTURE_ADJUDICATION_TRANCHE2/Rawlsing_P2_Semantic_Reference_Anomaly_Resolution_v1.csv',30),
]
input_rows=[]
for code,p,expected in inputs:
    actual=len(read_csv(p)) if p.suffix.lower()=='.csv' else None
    input_rows.append({'input_code':code,'relative_path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'expected_rows':expected,'actual_rows':actual,'authority_mode':'READ_ONLY','required':'YES'})
write_csv(SEC/'upstream/P3_UPSTREAM_INPUT_MANIFEST_v3.csv',input_rows)

part_counts=collections.Counter(r['participation_status'] for r in particip)
summary={
 'status':'PASS','semantic_priority_pairs':len(sem),'exact_foundation_pairs':len(ex),'overlap_pairs':len(set(sem_by)&set(ex_by)),
 'exact_only_pairs':len(set(ex_by)-set(sem_by)),'effective_unique_direct_pair_authorities':len(_eff),
 'effective_relation_type_counts':dict(sorted(eff_counts.items())),
 'proposition_relation_pairs':len(prop_rows),'administrative_metadata_proposition_pairs_preflight':len(admin_pairs),
 'provisional_substantive_j_family_candidate_edges':len(prop_rows)-len(admin_pairs),
 'administrative_pair_keys':admin_pairs,
 'lineage_participation_counts':dict(part_counts),'all_lineages':len(lin),'all_effective_pair_endpoints':len(all_ep),'proposition_graph_endpoints':len(prop_ep)
}
dumpj(SEC/'upstream/P3_EFFECTIVE_INPUT_AND_COVERAGE_RETURN_v3.json',summary)

# ---------- vocabularies ----------
v2v=read_csv(V22/'P3_CONTROLLED_VOCABULARIES_v2.csv')
# Rename diagnostic classifications to avoid terminal-decision names
class_map={
 'CLEAN_FAMILY_CANDIDATE':'CLEAN_CANDIDATE','RESPONSE_VARIANT_CANDIDATE':'VARIANT_BEARING_CANDIDATE','SPLIT_REQUIRED':'SPLIT_RISK',
 'HIERARCHICAL_RELATION_ONLY':'HIERARCHY_ONLY_RISK','COLLISION_BEARING':'COLLISION_BEARING_CANDIDATE','STRUCTURAL_ANALOGY_ONLY':'STRUCTURE_ONLY_DIAGNOSTIC',
 'INSUFFICIENT_AUTHORITY':'INSUFFICIENT_AUTHORITY_RISK','REJECTED_SEMANTIC_ARTIFACT':'SEMANTIC_ARTIFACT_RISK'}
vocab=[]
for r in v2v:
    q=dict(r)
    if q['vocabulary_domain']=='candidate_classification': q['code']=class_map[q['code']];q['label']=q['code'].replace('_',' ').title();q['definition']='Non-terminal primary diagnostic classification; final authority comes only from adjudication.'
    vocab.append(q)

def add_vocab(domain,codes,definition='Governed P3 categorical value.'):
    existing={(r['vocabulary_domain'],r['code']) for r in vocab}
    for code in codes:
        if (domain,code) not in existing:
            vocab.append({'vocabulary_domain':domain,'code':code,'label':code.replace('_',' ').title(),'definition':definition,'authority_effect':'','terminal':'FALSE','deprecated':'FALSE'})
add_vocab('source_family',['GSS','WVS','EVS','Arab Barometer','Afrobarometer','Asian Barometer','Latinobarómetro','South Asia','LiTS'])
add_vocab('lineage_participation_status',['PROPOSITION_GRAPH_INCIDENT','CONSTRAINT_ONLY_INCIDENT','NO_CURRENT_DIRECT_PAIR_AUTHORITY'])
add_vocab('candidate_origin_type',['STRICT_RESPONSE_COMPONENT','PROPOSITION_ONLY_SEED','ATTACHMENT_REVIEW','NONCONNECTIVE_DIAGNOSTIC_CASE'])
add_vocab('candidate_diagnostic_flag',['RESPONSE_VARIATION','SPLIT_RISK','HARD_COLLISION','NONTRANSITIVE_PATH','HIERARCHICAL_TARGET','DERIVED_INDEX','HETEROGENEOUS_LINEAGE','STRUCTURE_SUPPORTED','SOURCE_DOMINATED','SPARSE','EXACT_ONLY_AUTHORITY','PRECEDENCE_OVERLAP','ADMINISTRATIVE_METADATA','OPEN_CLOSURE'])
add_vocab('source_authority_role',['GOVERNING','SUPERSEDED_PROVENANCE','SUPPORTING'])
add_vocab('license_provenance_state',['KNOWN','UNKNOWN','NOT_APPLICABLE'])
add_vocab('candidate_membership_role',['PROPOSED_MEMBER','ACCEPTED_MEMBER','EXCLUDED_MEMBER','HIERARCHICAL_RELATIVE'])
add_vocab('object_reference_role',['SUBJECT','LEFT_ENDPOINT','RIGHT_ENDPOINT','MEMBER','OWNER','PARENT','CHILD','BROADER','NARROWER','DEPENDENT','AUTHORITY_INPUT','CREATED_BY','SUPERSEDES'])
add_vocab('collision_orientation',['SYMMETRIC','DIRECTIONAL'])
add_vocab('pair_authority_eligibility',['J_FAMILY_CANDIDATE_ELIGIBLE','ADMINISTRATIVE_METADATA_ONLY','NONCONNECTIVE'])
add_vocab('release_validation_phase',['PRE_PROMOTION','POST_PROMOTION'])
add_vocab('pair_state',['DIRECT_UNRESOLVED'])
add_vocab('lineage_p3_disposition_status',['UNADJUDICATED','CANDIDATE_MEMBER','CANONICAL_MEMBER','SOURCE_LOCAL_SINGLETON_PRESERVED','CONSTRAINT_ONLY_PRESERVED','ADMINISTRATIVE_METADATA_PRESERVED','DERIVED_OR_INDEX_PRESERVED','BLOCKED_UNRESOLVED','OUT_OF_SCOPE_NONQUESTION','SUPERSEDED_BY_SEGMENT'])
# sorted
vocab=sorted(vocab,key=lambda r:(r['vocabulary_domain'],r['code']))
write_csv(SEC/'P3_CONTROLLED_VOCABULARIES_v3.csv',vocab)
V=collections.defaultdict(set)
for r in vocab:V[r['vocabulary_domain']].add(r['code'])

# ---------- schemas ----------
BASE='https://rawlsing.local/schemas/p3/v3/'
def schema(title,required,props,allOf=None):
    d={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':BASE+title.lower().replace(' ','_')+'.schema.json','title':title,'type':'object','required':required,'properties':props,'additionalProperties':False}
    if allOf:d['allOf']=allOf
    return d
def strp(pattern=None,nullable=False,minlen=1):
    x={'type':['string','null'] if nullable else 'string'}
    if pattern:x['pattern']=pattern
    elif not nullable:x['minLength']=minlen
    return x
hashp={'type':'string','pattern':'^[0-9a-f]{64}$'}
# reusable nested schemas
schemas={}
schemas['release_status_event.schema.json']=schema('release_status_event',['release_id','event_ordinal','status','occurred_at','evidence_hash'],{
 'release_id':strp(), 'event_ordinal':{'type':'integer','minimum':1},'status':{'enum':sorted(V['release_status'])},'occurred_at':{'type':'string','format':'date-time'},'evidence_hash':hashp})
schemas['candidate_status_event.schema.json']=schema('candidate_status_event',['candidate_family_id','event_ordinal','to_stage','guard_evidence_id','authority_release_id'],{
 'candidate_family_id':strp(), 'event_ordinal':{'type':'integer','minimum':1},'from_stage':{'anyOf':[{'enum':sorted(V['lifecycle_stage'])},{'type':'null'}]},'to_stage':{'enum':sorted(V['lifecycle_stage'])},'guard_evidence_id':strp(),'authority_release_id':strp()})
schemas['canonical_proposition.schema.json']=schema('canonical_proposition',['subject_role','operator','target','object_or_outcome','modality','timeframe','condition','population_scope','geographic_scope','polarity','derived_status','parent_context'],{
 k:{'type':['string','null']} for k in ['subject_role','operator','target','object_or_outcome','modality','timeframe','condition','population_scope','geographic_scope','polarity','derived_status','parent_context']})
schemas['variant_assignment.schema.json']=schema('variant_assignment',['variant_id','variant_dimension','variant_value','member_ids'],{
 'variant_id':strp('^P3VAR-[0-9]{6}$'),'variant_revision_id':strp(nullable=True),'variant_dimension':{'enum':sorted(V['variant_dimension'])},'variant_value':strp(),'member_ids':{'type':'array','items':strp(),'uniqueItems':True,'minItems':1}})
schemas['hierarchy_relation.schema.json']=schema('hierarchy_relation',['broader_object_id','narrower_object_id','relation_role','evidence_ids'],{
 'broader_object_id':strp(),'narrower_object_id':strp(),'relation_role':strp(),'evidence_ids':{'type':'array','items':strp(),'uniqueItems':True,'minItems':1}})
schemas['collision_disposition.schema.json']=schema('collision_disposition',['collision_id','disposition','rationale'],{'collision_id':strp('^P3COL-[0-9]{8}$'),'disposition':strp(),'rationale':strp()})
schemas['unresolved_boundary.schema.json']=schema('unresolved_boundary',['boundary_id','left_id','right_id','reason','status'],{'boundary_id':strp(),'left_id':strp(),'right_id':strp(),'reason':strp(),'status':{'enum':sorted(V['closure_status'])}})
schemas['split_point.schema.json']=schema('split_point',['dimension','left_member_ids','right_member_ids','rationale'],{'dimension':strp(),'left_member_ids':{'type':'array','items':strp(),'uniqueItems':True,'minItems':1},'right_member_ids':{'type':'array','items':strp(),'uniqueItems':True,'minItems':1},'rationale':strp()})
schemas['candidate_diagnostic_flag.schema.json']=schema('candidate_diagnostic_flag',['candidate_revision_id','flag','evidence_ids'],{'candidate_revision_id':strp(),'flag':{'enum':sorted(V['candidate_diagnostic_flag'])},'evidence_ids':{'type':'array','items':strp(),'uniqueItems':True}})
schemas['candidate_ranking.schema.json']=schema('candidate_ranking',['candidate_revision_id','primary_class_rank','hard_collision_count','open_obligation_count','signature_completeness','source_count','lineage_count','direct_positive_density','structure_support_count','response_variant_complexity','authority_release_id'],{
 'candidate_revision_id':strp(),'primary_class_rank':{'type':'integer','minimum':0},'hard_collision_count':{'type':'integer','minimum':0},'open_obligation_count':{'type':'integer','minimum':0},'signature_completeness':{'type':'number','minimum':0,'maximum':1},'source_count':{'type':'integer','minimum':1},'lineage_count':{'type':'integer','minimum':2},'direct_positive_density':{'type':'number','minimum':0,'maximum':1},'structure_support_count':{'type':'integer','minimum':0},'response_variant_complexity':{'type':'integer','minimum':0},'authority_release_id':strp()})
schemas['lineage_participation.schema.json']=schema('lineage_participation',['lineage_id','source_family','participation_status','effective_pair_incident_count','proposition_pair_incident_count','signature_requirement','authority_release_id'],{
 'lineage_id':strp(),'source_family':{'enum':sorted(V['source_family'])},'participation_status':{'enum':sorted(V['lineage_participation_status'])},'effective_pair_incident_count':{'type':'integer','minimum':0},'proposition_pair_incident_count':{'type':'integer','minimum':0},'signature_requirement':strp(),'authority_note':strp(nullable=True),'authority_release_id':strp()})
schemas['lineage_disposition.schema.json']=schema('lineage_disposition',['subject_id','subject_type','disposition_status','reason','evidence_ids','authority_release_id'],{
 'subject_id':strp(),'subject_type':{'enum':['IMPORTED_SOURCE_LOCAL_LINEAGE','LINEAGE_SEGMENT']},'disposition_status':{'enum':sorted(V['lineage_p3_disposition_status'])},'reason':strp(),'evidence_ids':{'type':'array','items':strp(),'uniqueItems':True},'candidate_family_id':strp(nullable=True),'canonical_family_id':strp(nullable=True),'authority_release_id':strp()})
schemas['response_contract_reference.schema.json']=schema('response_contract_reference',['reference_id','subject_id','response_topology','authority_artifact','p4_authority','authority_release_id'],{
 'reference_id':strp(),'subject_id':strp(),'upstream_response_contract_id':strp(nullable=True),'response_topology':{'enum':sorted(V['response_topology'])},'response_contract_hash':{'anyOf':[hashp,{'type':'null'}]},'authority_artifact':strp(),'p4_authority':{'const':False},'authority_release_id':strp()})
schemas['structural_context_reference.schema.json']=schema('structural_context_reference',['reference_id','subject_id','source_field','source_value','authority_artifact','p5_authority','authority_release_id'],{
 'reference_id':strp(),'subject_id':strp(),'source_field':strp(),'source_value':{},'authority_artifact':strp(),'p5_authority':{'const':False},'authority_release_id':strp()})

# proposition signature v3
field_vocab={'subject_role':'subject_role','operator':'operator','modality':'modality','timeframe':'timeframe_class','population_scope':'population_scope_class','geographic_scope':'geographic_scope_class','polarity':'polarity_class','derived_status':'derived_status_class'}
field_props={}
for fname in ['subject_role','operator','target','object_or_outcome','modality','timeframe','condition','population_scope','geographic_scope','polarity','derived_status','parent_context']:
    norm={'type':['string','null']}
    if fname in field_vocab: norm={'anyOf':[{'enum':sorted(V[field_vocab[fname]])},{'type':'null'}]}
    fp={'type':'object','required':['field_value','normalized_value_code','evidence_state','confidence','evidence_ids'],'properties':{
        'field_value':{'type':['string','null']},'normalized_value_code':norm,'evidence_state':{'enum':sorted(V['field_evidence_state'])},'confidence':{'enum':sorted(V['confidence_level'])},'evidence_ids':{'type':'array','items':strp(),'uniqueItems':True}},'additionalProperties':False,
        'allOf':[
          {'if':{'properties':{'evidence_state':{'const':'KNOWN'}},'required':['evidence_state']},'then':{'properties':{'field_value':{'type':'string','minLength':1},'evidence_ids':{'minItems':1},'confidence':{'enum':['HIGH','MEDIUM','LOW']}}}},
          {'if':{'properties':{'evidence_state':{'enum':['HETEROGENEOUS','CONFLICTING']}},'required':['evidence_state']},'then':{'properties':{'evidence_ids':{'minItems':2},'confidence':{'enum':['MEDIUM','LOW']}}}},
          {'if':{'properties':{'evidence_state':{'const':'DIAGNOSTIC_ONLY'}},'required':['evidence_state']},'then':{'properties':{'evidence_ids':{'minItems':1}}}},
          {'if':{'properties':{'evidence_state':{'enum':['EXPLICITLY_UNSPECIFIED','NOT_APPLICABLE','UNRECOVERED']}},'required':['evidence_state']},'then':{'properties':{'field_value':{'type':'null'},'normalized_value_code':{'type':'null'}}}}
        ]}
    field_props[fname]=fp
schemas['proposition_signature.schema.json']=schema('proposition_signature',['signature_id','subject_id','subject_type','fields','response_topologies','signature_status','content_hash','authority_release_id'],{
 'signature_id':strp('^P3SIG-[0-9]{6}$'),'subject_id':strp(),'subject_type':{'enum':['IMPORTED_SOURCE_LOCAL_LINEAGE','LINEAGE_SEGMENT']},
 'fields':{'type':'object','required':list(field_props),'properties':field_props,'additionalProperties':False},
 'response_topologies':{'type':'array','items':{'enum':sorted(V['response_topology'])},'uniqueItems':True,'minItems':1},'signature_status':{'enum':sorted(V['signature_status'])},'content_hash':hashp,'authority_release_id':strp()})

# base copies and upgrades of remaining schemas
# Object registry
objtypes=sorted(V['object_type'])
schemas['object_registry.schema.json']=schema('object_registry',['object_id','object_type','identity_strategy','idempotency_key','origin_phase','allocation_release_id','stable_identity_note'],{
 'object_id':strp(),'object_type':{'enum':objtypes},'identity_strategy':{'enum':sorted(V['identity_strategy'])},'idempotency_key':strp(),'origin_phase':strp(),'origin_authority_id':strp(nullable=True),'allocation_release_id':strp(),'retired_release_id':strp(nullable=True),'content_hash':{'anyOf':[hashp,{'type':'null'}]},'stable_identity_note':strp()})
# upstream ref
schemas['upstream_object_reference.schema.json']=schema('upstream_object_reference',['object_id','upstream_phase','upstream_object_type','upstream_object_id','authority_artifact','authority_hash','read_only','license_provenance_state'],{
 'object_id':strp(),'upstream_phase':strp(),'source_family':{'anyOf':[{'enum':sorted(V['source_family'])},{'type':'null'}]},'upstream_object_type':strp(),'upstream_object_id':strp(),'authority_artifact':strp(),'authority_hash':hashp,'license_provenance_state':{'enum':sorted(V['license_provenance_state'])},'license_provenance_ref':strp(nullable=True),'read_only':{'const':True}})
# pair fact with exact one governing and eligibility
source_auth={'type':'object','required':['registry','authority_id','authority_role'],'properties':{'registry':{'enum':sorted(V['upstream_registry'])},'authority_id':strp(),'authority_role':{'enum':sorted(V['source_authority_role'])},'superseded_by_authority_id':strp(nullable=True)},'additionalProperties':False}
pair_props={'pair_fact_id':strp('^P3PF-[0-9]{8}$'),'left_id':strp(),'right_id':strp(),'orientation':{'enum':sorted(V['relation_orientation'])},'relation_type':{'enum':sorted(V['pair_relation_type'])},
 'source_authorities':{'type':'array','minItems':1,'maxItems':2,'uniqueItems':True,'items':source_auth,'contains':{'type':'object','properties':{'authority_role':{'const':'GOVERNING'}},'required':['authority_role']},'minContains':1,'maxContains':1},
 'target_relation':{'anyOf':[{'enum':sorted(V['axis_relation'])},{'type':'null'}]},'operator_relation':{'anyOf':[{'enum':sorted(V['axis_relation'])},{'type':'null'}]},'timeframe_relation':{'anyOf':[{'enum':sorted(V['axis_relation'])},{'type':'null'}]},'response_relation':{'anyOf':[{'enum':sorted(V['axis_relation'])},{'type':'null'}]},
 'source_portability_ceiling':strp(),'p3_portability_ceiling':{'enum':sorted(V['portability_ceiling'])},'proposition_graph_allowed':{'type':'boolean'},'j_family_candidate_eligibility':{'enum':sorted(V['pair_authority_eligibility'])},'creates_endpoint_authority':{'const':False},'evidence_ids':{'type':'array','items':strp(),'uniqueItems':True,'minItems':2},'authority_release_id':strp()}
pair_allof=[
 {'if':{'properties':{'relation_type':{'enum':['PROPOSITION_RESPONSE_IDENTITY','PROPOSITION_IDENTITY_ONLY']}},'required':['relation_type']},'then':{'properties':{'proposition_graph_allowed':{'const':True}}}},
 {'if':{'properties':{'relation_type':{'enum':['NESTED_TARGET_RELATION','CONSTRUCT_COORDINATE','STRUCTURE_MEMBER_ANALOGY','EXPLICIT_NEGATIVE','REDIRECT_OTHER_DOMAIN','UNRESOLVED']}},'required':['relation_type']},'then':{'properties':{'proposition_graph_allowed':{'const':False},'j_family_candidate_eligibility':{'const':'NONCONNECTIVE'}}}},
 {'if':{'properties':{'relation_type':{'const':'NESTED_TARGET_RELATION'}},'required':['relation_type']},'then':{'properties':{'orientation':{'const':'DIRECTIONAL'}}}},
 {'if':{'properties':{'relation_type':{'enum':['PROPOSITION_RESPONSE_IDENTITY','PROPOSITION_IDENTITY_ONLY','CONSTRUCT_COORDINATE','STRUCTURE_MEMBER_ANALOGY','EXPLICIT_NEGATIVE','REDIRECT_OTHER_DOMAIN','UNRESOLVED']}},'required':['relation_type']},'then':{'properties':{'orientation':{'const':'SYMMETRIC'}}}}
]
schemas['pair_fact_bundle.schema.json']=schema('pair_fact_bundle',list(pair_props),pair_props,pair_allof)
# collision
schemas['collision_scope.schema.json']=schema('collision_scope',['collision_id','collision_type','scope_type','orientation','left_id','right_id','source_authority_ids','hard_blocker','authority_release_id'],{
 'collision_id':strp('^P3COL-[0-9]{8}$'),'collision_type':{'enum':sorted(V['collision_type'])},'scope_type':{'enum':sorted(V['collision_scope'])},'orientation':{'enum':sorted(V['collision_orientation'])},'left_id':strp(),'right_id':strp(),'left_role':strp(nullable=True),'right_role':strp(nullable=True),'source_authority_ids':{'type':'array','items':strp(),'uniqueItems':True,'minItems':1},'historical_interval':{'type':['object','null']},'source_scope':strp(nullable=True),'hard_blocker':{'type':'boolean'},'downstream_effects':{'type':'array','items':strp(),'uniqueItems':True},'authority_release_id':strp()})
# component
schemas['candidate_component.schema.json']=schema('candidate_component',['component_id','member_ids','connectivity_pair_fact_ids','build_rule_version','content_hash','authority_release_id'],{
 'component_id':strp('^P3COMP-[0-9a-f]{16}$'),'member_ids':{'type':'array','items':strp(),'uniqueItems':True,'minItems':2},'connectivity_pair_fact_ids':{'type':'array','items':strp('^P3PF-[0-9]{8}$'),'uniqueItems':True,'minItems':1},'build_rule_version':strp(),'content_hash':hashp,'authority_release_id':strp()})
# candidate family revision
internal_counts={'type':'object','required':['expected_pairs','direct_positive','direct_collision','hierarchical_only','unruled','signature_conflict','signature_compatible'],'properties':{k:{'type':'integer','minimum':0} for k in ['expected_pairs','direct_positive','direct_collision','hierarchical_only','unruled','signature_conflict','signature_compatible']},'additionalProperties':False}
schemas['candidate_family.schema.json']=schema('candidate_family',['candidate_family_id','revision_id','component_ids','member_ids','lifecycle_stage','candidate_classification','candidate_origin_type','internal_pair_counts','closure_obligation_ids','evidence_bundle_hash','authority_release_id'],{
 'candidate_family_id':strp('^P3CAND-[0-9]{6}$'),'revision_id':strp('^P3CANDREV-[0-9]{8}$'),'component_ids':{'type':'array','items':strp(),'uniqueItems':True,'minItems':1},'member_ids':{'type':'array','items':strp(),'uniqueItems':True,'minItems':2},'canonical_signature_id':strp(nullable=True),'lifecycle_stage':{'enum':sorted(V['lifecycle_stage'])},'candidate_classification':{'enum':sorted(V['candidate_classification'])},'candidate_origin_type':{'enum':sorted(V['candidate_origin_type'])},'diagnostic_flags':{'type':'array','items':{'enum':sorted(V['candidate_diagnostic_flag'])},'uniqueItems':True},'internal_pair_counts':internal_counts,'closure_obligation_ids':{'type':'array','items':strp(),'uniqueItems':True},'variant_ids':{'type':'array','items':strp(),'uniqueItems':True},'exclusion_ids':{'type':'array','items':strp(),'uniqueItems':True},'ranking':{'$ref':BASE+'candidate_ranking.schema.json'},'evidence_bundle_hash':hashp,'authority_release_id':strp()})
# candidate packet nested row schemas inline/ref
pairrow={'type':'object','required':['left_id','right_id','pair_state','pair_fact_id','collision_ids','closure_obligation_ids'],'properties':{'left_id':strp(),'right_id':strp(),'pair_state':{'enum':sorted(V['pair_state'])},'pair_fact_id':strp(nullable=True),'collision_ids':{'type':'array','items':strp(),'uniqueItems':True},'closure_obligation_ids':{'type':'array','items':strp(),'uniqueItems':True}},'additionalProperties':False}
collisionref={'type':'object','required':['collision_id','collision_type','scope_type','orientation','left_id','right_id'],'properties':{'collision_id':strp(),'collision_type':{'enum':sorted(V['collision_type'])},'scope_type':{'enum':sorted(V['collision_scope'])},'orientation':{'enum':sorted(V['collision_orientation'])},'left_id':strp(),'right_id':strp()},'additionalProperties':False}
obref={'type':'object','required':['obligation_id','obligation_type','status','left_id','right_id'],'properties':{'obligation_id':strp(),'obligation_type':{'enum':sorted(V['closure_obligation_type'])},'status':{'enum':sorted(V['closure_status'])},'left_id':strp(),'right_id':strp()},'additionalProperties':False}
packet_props={
 'packet_id':strp('^P3PKT-[0-9]{6}$'),'candidate_family':{'$ref':BASE+'candidate_family.schema.json'},'members_by_source':{'type':'object','propertyNames':{'enum':sorted(V['source_family'])},'additionalProperties':{'type':'array','items':strp(),'uniqueItems':True,'minItems':1},'minProperties':2},
 'proposition_signature_matrix':{'type':'array','items':{'$ref':BASE+'proposition_signature.schema.json'},'uniqueItems':True,'minItems':2},
 'response_contract_matrix':{'type':'array','items':{'$ref':BASE+'response_contract_reference.schema.json'},'minItems':2},
 'internal_pair_matrix':{'type':'array','items':pairrow,'minItems':1},'hard_collisions':{'type':'array','items':collisionref},
 'unresolved_pairs':{'type':'array','items':{**pairrow,'properties':{**pairrow['properties'],'pair_state':{'const':'DIRECT_UNRESOLVED'}}}},
 'unruled_pairs':{'type':'array','items':{**pairrow,'properties':{**pairrow['properties'],'pair_state':{'const':'UNRULED'}}}},
 'closure_obligations':{'type':'array','items':obref},'likely_split_points':{'type':'array','items':{'$ref':BASE+'split_point.schema.json'}},
 'proposed_variants':{'type':'array','items':{'$ref':BASE+'variant_assignment.schema.json'}},
 'explicit_exclusions':{'type':'array','minItems':1,'items':{'$ref':BASE+'family_exclusion.schema.json'}},
 'hyperedge_context':{'type':'array','items':{'$ref':BASE+'hyperedge.schema.json'}},'strata_horizon_context':{'type':'array','items':{'$ref':BASE+'structural_context_reference.schema.json'}},
 'exact_evidence_links':{'type':'array','items':strp(),'uniqueItems':True,'minItems':2},'evidence_bundle_hash':hashp,'decision_form':{'$ref':BASE+'adjudication_decision_draft.schema.json'}
}
schemas['candidate_packet.schema.json']=schema('candidate_packet',list(packet_props),packet_props)
# variants/exclusions/hyperedge etc
schemas['candidate_variant.schema.json']=schema('candidate_variant',['variant_id','owner_object_id','variant_dimension','variant_value','member_ids','value_portability_status','authority_release_id'],{'variant_id':strp('^P3VAR-[0-9]{6}$'),'owner_object_id':strp(),'variant_dimension':{'enum':sorted(V['variant_dimension'])},'variant_value':strp(),'member_ids':{'type':'array','items':strp(),'uniqueItems':True,'minItems':1},'value_portability_status':{'const':'NOT_AUTHORIZED_BY_P3'},'authority_release_id':strp()})
schemas['family_exclusion.schema.json']=schema('family_exclusion',['exclusion_id','owner_object_id','exclusion_type','prohibited_operation','evidence_or_rule','scope','tested_surface_complete','authority_release_id'],{'exclusion_id':strp('^P3EXC-[0-9]{6}$'),'owner_object_id':strp(),'exclusion_type':{'enum':sorted(V['exclusion_type'])},'prohibited_operation':strp(),'evidence_or_rule':strp(),'scope':strp(),'tested_surface_complete':{'type':'boolean'},'excluded_object_ids':{'type':'array','items':strp(),'uniqueItems':True},'authority_release_id':strp()})
schemas['hyperedge.schema.json']=schema('hyperedge',['hyperedge_id','hyperedge_type','authority_effect','causal_authority','members','authority_release_id'],{'hyperedge_id':strp('^P3HYP-[0-9]{6}$'),'hyperedge_type':{'enum':sorted(V['hyperedge_type'])},'authority_effect':{'enum':sorted(V['hyperedge_authority_effect'])},'causal_authority':{'const':False},'members':{'type':'array','items':{'type':'object','required':['object_id','participant_role'],'properties':{'object_id':strp(),'participant_role':strp()},'additionalProperties':False},'minItems':2},'authority_release_id':strp()})
# closure, dependency, doctrine, lineage segment, genealogy
for name in ['closure_obligation','dependency_record','doctrine_delta','lineage_segment','release_change_record']:
    old=json.loads((V22/'schemas'/f'{name}.schema.json').read_text());old['$id']=BASE+f'{name}.schema.json';schemas[f'{name}.schema.json']=old
# family genealogy conditional
fg_props={'genealogy_id':strp('^P3GEN-[0-9]{6}$'),'relation_type':{'enum':sorted(V['genealogy_relation_type'])},'predecessor_family_ids':{'type':'array','items':strp(),'uniqueItems':True,'minItems':1},'successor_family_ids':{'type':'array','items':strp(),'uniqueItems':True},'reason':strp(),'adjudication_id':strp(),'authority_release_id':strp()}
fg_all=[
 {'if':{'properties':{'relation_type':{'const':'SPLIT'}},'required':['relation_type']},'then':{'properties':{'predecessor_family_ids':{'maxItems':1},'successor_family_ids':{'minItems':2}}}},
 {'if':{'properties':{'relation_type':{'const':'MERGE'}},'required':['relation_type']},'then':{'properties':{'predecessor_family_ids':{'minItems':2},'successor_family_ids':{'minItems':1,'maxItems':1}}}},
 {'if':{'properties':{'relation_type':{'const':'SUPERSEDE'}},'required':['relation_type']},'then':{'properties':{'successor_family_ids':{'minItems':1}}}},
 {'if':{'properties':{'relation_type':{'const':'DEPRECATE'}},'required':['relation_type']},'then':{'properties':{'successor_family_ids':{'maxItems':0}}}}
]
schemas['family_genealogy.schema.json']=schema('family_genealogy',list(fg_props),fg_props,fg_all)
# authority release aligns with table: no embedded status
schemas['authority_release.schema.json']=schema('authority_release',['release_id','schema_version','builder_version','input_manifest_hash','created_at','object_counts','validation_return_hash'],{'release_id':strp('^P3-AUTHORITY-[0-9]{4}-[0-9]{2}-[0-9]{2}-R[0-9]+$'),'parent_release_id':strp(nullable=True),'schema_version':strp(),'builder_version':strp(),'input_manifest_hash':hashp,'created_at':{'type':'string','format':'date-time'},'object_counts':{'type':'object','additionalProperties':{'type':'integer','minimum':0}},'migration_artifact':strp(nullable=True),'rollback_artifact':strp(nullable=True),'validation_return_hash':hashp})
# decisions
common_dec_props={'adjudication_id':strp('^P3ADJ-[0-9]{6}$'),'candidate_family_id':strp(),'candidate_revision_id':strp(),'decision_status':{'anyOf':[{'enum':sorted(V['adjudication_decision_status'])},{'type':'null'}]},'canonical_family_id':strp(nullable=True),'canonical_proposition':{'anyOf':[{'$ref':BASE+'canonical_proposition.schema.json'},{'type':'null'}]},'accepted_members':{'type':'array','items':strp(),'uniqueItems':True},'excluded_members':{'type':'array','items':strp(),'uniqueItems':True},'variant_assignments':{'type':'array','items':{'$ref':BASE+'variant_assignment.schema.json'}},'hierarchical_relations':{'type':'array','items':{'$ref':BASE+'hierarchy_relation.schema.json'}},'collision_dispositions':{'type':'array','items':{'$ref':BASE+'collision_disposition.schema.json'}},'response_portability_status':{'const':'NOT_AUTHORIZED_BY_P3'},'unresolved_boundaries':{'type':'array','items':{'$ref':BASE+'unresolved_boundary.schema.json'}},'rationale':{'type':'string'},'evidence_bundle_hash':hashp,'supersedes_adjudication_id':strp(nullable=True),'authority_release_id':strp()}
draft_req=['adjudication_id','candidate_family_id','candidate_revision_id','accepted_members','excluded_members','variant_assignments','hierarchical_relations','collision_dispositions','unresolved_boundaries','response_portability_status','evidence_bundle_hash','authority_release_id']
schemas['adjudication_decision_draft.schema.json']=schema('adjudication_decision_draft',draft_req,common_dec_props)
final_props=dict(common_dec_props); final_props['decision_status']={'enum':sorted(V['adjudication_decision_status'])}; final_props['rationale']={'type':'string','minLength':1}
final_req=draft_req+['decision_status','rationale']
final_all=[
 {'if':{'properties':{'decision_status':{'enum':['ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS']}},'required':['decision_status']},'then':{'required':['canonical_family_id','canonical_proposition'],'properties':{'canonical_family_id':{'type':'string','minLength':1},'canonical_proposition':{'$ref':BASE+'canonical_proposition.schema.json'},'accepted_members':{'minItems':2}}}},
 {'if':{'properties':{'decision_status':{'const':'ACCEPTED_WITH_VARIANTS'}},'required':['decision_status']},'then':{'properties':{'variant_assignments':{'minItems':1}}}},
 {'if':{'properties':{'decision_status':{'const':'BLOCKED_UNRESOLVED'}},'required':['decision_status']},'then':{'properties':{'unresolved_boundaries':{'minItems':1}}}},
 {'if':{'properties':{'decision_status':{'enum':['REJECTED','REJECTED_SEMANTIC_ARTIFACT','INSUFFICIENT_AUTHORITY','BLOCKED_UNRESOLVED','SPLIT_REQUIRED','HIERARCHICAL_RELATION_ONLY']}},'required':['decision_status']},'then':{'properties':{'canonical_family_id':{'type':'null'},'canonical_proposition':{'type':'null'}}}}
]
schemas['adjudication_decision.schema.json']=schema('adjudication_decision',final_req,final_props,final_all)
# canonical family/revision
schemas['canonical_family.schema.json']=schema('canonical_family',['canonical_family_id','created_by_adjudication_id','created_release_id'],{'canonical_family_id':strp('^JFAM-[0-9]{6}$'),'created_by_adjudication_id':strp(),'created_release_id':strp(),'retired_release_id':strp(nullable=True)})
schemas['canonical_family_revision.schema.json']=schema('canonical_family_revision',['family_revision_id','canonical_family_id','revision_number','canonical_signature_id','canonical_proposition','member_ids','variant_ids','exclusion_ids','evidence_bundle_hash','authority_release_id'],{'family_revision_id':strp('^JFAMREV-[0-9]{8}$'),'canonical_family_id':strp(),'revision_number':{'type':'integer','minimum':1},'canonical_signature_id':strp(),'canonical_proposition':{'$ref':BASE+'canonical_proposition.schema.json'},'member_ids':{'type':'array','items':strp(),'uniqueItems':True,'minItems':2},'variant_ids':{'type':'array','items':strp(),'uniqueItems':True},'exclusion_ids':{'type':'array','items':strp(),'uniqueItems':True,'minItems':1},'evidence_bundle_hash':hashp,'authority_release_id':strp()})
# release change already adjusted id
# write schemas
for name,s in schemas.items(): dumpj(SEC/'schemas'/name,s)

# ---------- identity and reference contracts ----------
identity_rows=[
 {'object_type':'IMPORTED_IMPLEMENTATION','identity_strategy':'INHERITED_UPSTREAM_ID','idempotency_key':'implementation_id','allocation_rule':'Use exact P2 implementation ID.'},
 {'object_type':'IMPORTED_SOURCE_LOCAL_LINEAGE','identity_strategy':'INHERITED_UPSTREAM_ID','idempotency_key':'lineage_id','allocation_rule':'Use exact P2 lineage ID.'},
 {'object_type':'PAIR_FACT','identity_strategy':'CONTENT_ADDRESSED_DERIVED_ID','idempotency_key':'pair_key + governing_authority_id + mapping_version','allocation_rule':'Canonical UTF-8 JSON, sorted keys, SHA-256; display ID uses first 16 hex with collision check.'},
 {'object_type':'CANDIDATE_COMPONENT','identity_strategy':'CONTENT_ADDRESSED_DERIVED_ID','idempotency_key':'sorted member IDs + sorted connective pair-fact IDs + build rule version','allocation_rule':'Canonical UTF-8 JSON, sorted keys, SHA-256.'},
 {'object_type':'CANDIDATE_FAMILY','identity_strategy':'REGISTRY_ALLOCATED_DURABLE_ID','idempotency_key':'initial component identity + candidate origin type','allocation_rule':'Initial deterministic sorted allocation; append-only after first release.'},
 {'object_type':'CANONICAL_FAMILY','identity_strategy':'REGISTRY_ALLOCATED_DURABLE_ID','idempotency_key':'accepting adjudication ID','allocation_rule':'Allocate new JFAM ID; revisions do not change stable ID.'},
 {'object_type':'FAMILY_VARIANT','identity_strategy':'REGISTRY_ALLOCATED_DURABLE_ID','idempotency_key':'owner stable ID + dimension + stable semantic value key','allocation_rule':'Append-only.'},
 {'object_type':'FAMILY_EXCLUSION','identity_strategy':'REGISTRY_ALLOCATED_DURABLE_ID','idempotency_key':'owner stable ID + exclusion type + prohibited operation + stable rule key','allocation_rule':'Append-only.'},
 {'object_type':'ADJUDICATION','identity_strategy':'REGISTRY_ALLOCATED_DURABLE_ID','idempotency_key':'candidate revision ID + decision ordinal','allocation_rule':'Append-only immutable decision.'},
]
write_csv(SEC/'P3_IDENTITY_KEY_SPEC_v3.csv',identity_rows)
ref_rows=[
 {'table_name':'p3_lineage_segment','column_name':'parent_lineage_id','allowed_object_types':'IMPORTED_SOURCE_LOCAL_LINEAGE','required':'YES'},
 {'table_name':'p3_lineage_segment_member','column_name':'implementation_id','allowed_object_types':'IMPORTED_IMPLEMENTATION','required':'YES'},
 {'table_name':'p3_lineage_disposition','column_name':'subject_id','allowed_object_types':'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','required':'YES'},
 {'table_name':'p3_proposition_signature','column_name':'subject_id','allowed_object_types':'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','required':'YES'},
 {'table_name':'p3_pair_fact_bundle','column_name':'left_object_id','allowed_object_types':'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','required':'YES'},
 {'table_name':'p3_pair_fact_bundle','column_name':'right_object_id','allowed_object_types':'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','required':'YES'},
 {'table_name':'p3_candidate_membership','column_name':'member_object_id','allowed_object_types':'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','required':'YES'},
 {'table_name':'p3_internal_pair_matrix','column_name':'left_object_id','allowed_object_types':'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','required':'YES'},
 {'table_name':'p3_internal_pair_matrix','column_name':'right_object_id','allowed_object_types':'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','required':'YES'},
 {'table_name':'p3_canonical_family_membership','column_name':'member_object_id','allowed_object_types':'IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','required':'YES'},
 {'table_name':'p3_family_variant','column_name':'owner_object_id','allowed_object_types':'CANDIDATE_FAMILY|CANONICAL_FAMILY','required':'YES'},
 {'table_name':'p3_family_exclusion','column_name':'owner_object_id','allowed_object_types':'CANDIDATE_FAMILY|CANONICAL_FAMILY','required':'YES'},
]
write_csv(SEC/'P3_OBJECT_REFERENCE_TYPE_CONTRACT_v3.csv',ref_rows)

# ---------- DDL v3 ----------
ddl=(V22/'sql/p3_postgresql_compatible_ddl_v2.sql').read_text()
ddl=ddl.replace("'DIRECT_POSITIVE','DIRECT_COLLISION','HIERARCHICAL_ONLY','UNRULED','SIGNATURE_CONFLICT','SIGNATURE_COMPATIBLE'", "'DIRECT_POSITIVE','DIRECT_COLLISION','DIRECT_UNRESOLVED','HIERARCHICAL_ONLY','UNRULED','SIGNATURE_CONFLICT','SIGNATURE_COMPATIBLE'")
ddl=ddl.replace('Logical DDL v2','Logical DDL v3')
ddl=ddl.replace("source_family TEXT,\n    upstream_object_type", "source_family TEXT, license_provenance_state TEXT NOT NULL,\n    upstream_object_type")
ddl=ddl.replace("scope_type TEXT NOT NULL,\n    left_object_id", "scope_type TEXT NOT NULL, orientation TEXT NOT NULL CHECK(orientation IN ('SYMMETRIC','DIRECTIONAL')), left_role TEXT, right_role TEXT,\n    left_object_id")
ddl=ddl.replace('connectivity_allowed BOOLEAN NOT NULL, creates_endpoint_authority', 'proposition_graph_allowed BOOLEAN NOT NULL, j_family_candidate_eligibility TEXT NOT NULL, creates_endpoint_authority')
ddl=ddl.replace('CHECK(connectivity_allowed=FALSE OR relation_type IN', 'CHECK(proposition_graph_allowed=FALSE OR relation_type IN')
ddl=ddl.replace("candidate_classification TEXT NOT NULL CHECK(candidate_classification IN ('CLEAN_FAMILY_CANDIDATE','RESPONSE_VARIANT_CANDIDATE','SPLIT_REQUIRED','HIERARCHICAL_RELATION_ONLY','COLLISION_BEARING','STRUCTURAL_ANALOGY_ONLY','INSUFFICIENT_AUTHORITY','REJECTED_SEMANTIC_ARTIFACT')),", "candidate_classification TEXT NOT NULL CHECK(candidate_classification IN ('CLEAN_CANDIDATE','VARIANT_BEARING_CANDIDATE','SPLIT_RISK','HIERARCHY_ONLY_RISK','COLLISION_BEARING_CANDIDATE','STRUCTURE_ONLY_DIAGNOSTIC','INSUFFICIENT_AUTHORITY_RISK','SEMANTIC_ARTIFACT_RISK')),\n    candidate_origin_type TEXT NOT NULL,")
ddl=ddl.replace("PRIMARY KEY(candidate_revision_id,member_object_id,membership_role));", "PRIMARY KEY(candidate_revision_id,member_object_id));")
ddl=ddl.replace("PRIMARY KEY(candidate_revision_id,left_object_id,right_object_id), CHECK(left_object_id <> right_object_id)", "PRIMARY KEY(candidate_revision_id,left_object_id,right_object_id), CHECK(left_object_id < right_object_id)")
ddl=ddl.replace("authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), CHECK(left_object_id <> right_object_id)\n);", "authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), CHECK(left_object_id < right_object_id),\n    FOREIGN KEY(resolution_adjudication_id) REFERENCES p3_adjudication_decision(adjudication_id) DEFERRABLE INITIALLY DEFERRED\n);")
# Above FK references later table invalid at create time in PostgreSQL; remove and add later via ALTER.
ddl=ddl.replace(",\n    FOREIGN KEY(resolution_adjudication_id) REFERENCES p3_adjudication_decision(adjudication_id) DEFERRABLE INITIALLY DEFERRED","")
# Insert new tables after candidate status/member definitions
insert_after="CREATE TABLE p3_candidate_membership (candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id), member_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), membership_role TEXT NOT NULL CHECK(membership_role IN ('PROPOSED_MEMBER','ACCEPTED_MEMBER','EXCLUDED_MEMBER','HIERARCHICAL_RELATIVE')), PRIMARY KEY(candidate_revision_id,member_object_id));"
new_tables=insert_after+"\nCREATE TABLE p3_candidate_diagnostic_flag (candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id), flag TEXT NOT NULL, evidence_ids JSONB NOT NULL DEFAULT '[]'::jsonb, PRIMARY KEY(candidate_revision_id,flag));\nCREATE TABLE p3_candidate_ranking (candidate_revision_id TEXT PRIMARY KEY REFERENCES p3_candidate_revision(candidate_revision_id), primary_class_rank INTEGER NOT NULL CHECK(primary_class_rank>=0), hard_collision_count INTEGER NOT NULL CHECK(hard_collision_count>=0), open_obligation_count INTEGER NOT NULL CHECK(open_obligation_count>=0), signature_completeness NUMERIC NOT NULL CHECK(signature_completeness>=0 AND signature_completeness<=1), source_count INTEGER NOT NULL CHECK(source_count>=1), lineage_count INTEGER NOT NULL CHECK(lineage_count>=2), direct_positive_density NUMERIC NOT NULL CHECK(direct_positive_density>=0 AND direct_positive_density<=1), structure_support_count INTEGER NOT NULL CHECK(structure_support_count>=0), response_variant_complexity INTEGER NOT NULL CHECK(response_variant_complexity>=0), authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id));"
ddl=ddl.replace(insert_after,new_tables)
# lineage participation after upstream refs
needle="CREATE TABLE p3_lineage_segment ("
part_table="CREATE TABLE p3_lineage_participation (lineage_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), participation_status TEXT NOT NULL, effective_pair_incident_count INTEGER NOT NULL CHECK(effective_pair_incident_count>=0), proposition_pair_incident_count INTEGER NOT NULL CHECK(proposition_pair_incident_count>=0), signature_requirement TEXT NOT NULL, authority_note TEXT, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), PRIMARY KEY(lineage_id,authority_release_id));\nCREATE TABLE p3_lineage_disposition (subject_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), subject_type TEXT NOT NULL, disposition_status TEXT NOT NULL, reason TEXT NOT NULL, evidence_ids JSONB NOT NULL DEFAULT '[]'::jsonb, candidate_family_id TEXT, canonical_family_id TEXT, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), PRIMARY KEY(subject_id,authority_release_id));\n\n"
ddl=ddl.replace(needle,part_table+needle)
# pair source authority role
old="registry_code TEXT NOT NULL, authority_id TEXT NOT NULL,\n    governing BOOLEAN NOT NULL, superseded_by_authority_id TEXT, PRIMARY KEY(pair_fact_id,registry_code,authority_id)"
new="registry_code TEXT NOT NULL, authority_id TEXT NOT NULL, authority_role TEXT NOT NULL,\n    governing BOOLEAN NOT NULL, superseded_by_authority_id TEXT, PRIMARY KEY(pair_fact_id,registry_code,authority_id), CHECK((authority_role='GOVERNING')=governing)"
ddl=ddl.replace(old,new)
# Add deferred FK and type contract table before views
marker="CREATE TABLE p3_categorical_field_binding ("
type_table="CREATE TABLE p3_object_reference_type_contract (table_name TEXT NOT NULL, column_name TEXT NOT NULL, allowed_object_types TEXT[] NOT NULL, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), PRIMARY KEY(table_name,column_name,authority_release_id));\n\n"
ddl=ddl.replace(marker,type_table+marker)
# Remove inherited deferred ALTERs before inserting exactly one authoritative copy.
ddl=re.sub(r'\n?ALTER TABLE p3_closure_obligation ADD CONSTRAINT p3_closure_resolution_adjudication_fk[^;]+;\n?', '\n', ddl)
ddl=re.sub(r'\n?ALTER TABLE p3_adjudication_decision ADD CONSTRAINT p3_adjudication_canonical_family_fk[^;]+;\n?', '\n', ddl)
# Add ALTER after adjudication and canonical-family tables exist
alter="\nALTER TABLE p3_closure_obligation ADD CONSTRAINT p3_closure_resolution_adjudication_fk FOREIGN KEY(resolution_adjudication_id) REFERENCES p3_adjudication_decision(adjudication_id) DEFERRABLE INITIALLY DEFERRED;\nALTER TABLE p3_adjudication_decision ADD CONSTRAINT p3_adjudication_canonical_family_fk FOREIGN KEY(canonical_family_id) REFERENCES p3_canonical_family(canonical_family_id) DEFERRABLE INITIALLY DEFERRED;\nALTER TABLE p3_lineage_disposition ADD CONSTRAINT p3_lineage_disposition_candidate_family_fk FOREIGN KEY(candidate_family_id) REFERENCES p3_candidate_family(candidate_family_id) DEFERRABLE INITIALLY DEFERRED;\nALTER TABLE p3_lineage_disposition ADD CONSTRAINT p3_lineage_disposition_canonical_family_fk FOREIGN KEY(canonical_family_id) REFERENCES p3_canonical_family(canonical_family_id) DEFERRABLE INITIALLY DEFERRED;\n"
ddl=ddl.replace('CREATE TABLE p3_doctrine_delta (',alter+'\nCREATE TABLE p3_doctrine_delta (',1)
# remove obsolete rank_tuple from revision or keep diagnostic cache? remove to avoid duplicate source truth
# replace with no rank tuple
# exact literal may span
ddl=ddl.replace("    canonical_signature_id TEXT REFERENCES p3_proposition_signature(signature_id), evidence_bundle_hash CHAR(64) NOT NULL CHECK(evidence_bundle_hash ~ '^[0-9a-f]{64}$'),\n    rank_tuple JSONB NOT NULL DEFAULT '[]'::jsonb, authority_release_id", "    canonical_signature_id TEXT REFERENCES p3_proposition_signature(signature_id), evidence_bundle_hash CHAR(64) NOT NULL CHECK(evidence_bundle_hash ~ '^[0-9a-f]{64}$'),\n    authority_release_id")
# Update comment v3
ddl=ddl.replace('P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v2.csv','P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v3.csv')
(SEC/'sql/p3_postgresql_compatible_ddl_v3.sql').write_text(ddl,encoding='utf-8')

# Parse DDL columns for dictionary
blocks=dict(re.findall(r'CREATE TABLE\s+(\w+)\s*\((.*?)\);',ddl,re.S|re.I))
def split_cols(b):
    depth=0;cur='';parts=[]
    for ch in b:
        if ch=='(':depth+=1
        elif ch==')':depth-=1
        if ch==',' and depth==0:parts.append(cur.strip());cur=''
        else:cur+=ch
    if cur.strip():parts.append(cur.strip())
    return parts
columns={}
for t,b in blocks.items():
    rows=[]
    for p in split_cols(b):
        if not p or p.upper().startswith(('PRIMARY KEY','FOREIGN KEY','UNIQUE','CHECK','CONSTRAINT')):continue
        toks=p.split(); col=toks[0]; typ=toks[1] if len(toks)>1 else 'UNKNOWN'; required='YES' if 'NOT NULL' in p.upper() or 'PRIMARY KEY' in p.upper() else 'NO'
        ref='';m=re.search(r'REFERENCES\s+(\w+)\s*\((\w+)\)',p,re.I)
        if m:ref=m.group(1)+'.'+m.group(2)
        key='PK' if 'PRIMARY KEY' in p.upper() else ('FK' if ref else 'VALUE')
        rows.append({'table_or_artifact':t,'field':col,'logical_type':typ,'required':required,'key_role':key,'definition':col.replace('_',' ').capitalize()+'.','references':ref})
    columns[t]=rows
write_csv(SEC/'P3_SCHEMA_DICTIONARY_v3.csv',[r for rs in columns.values() for r in rs])

# Categorical bindings comprehensive
bindings=[]
def bind(t,c,d,required='YES'):bindings.append({'table_name':t,'column_name':c,'vocabulary_domain':d,'enforcement':'DDL_CHECK_AND_OR_MIGRATION_TRIGGER','required':required})
for item in [
 ('p3_release_status_event','status','release_status'),('p3_object_registry','object_type','object_type'),('p3_object_registry','identity_strategy','identity_strategy'),('p3_upstream_object_reference','source_family','source_family'),('p3_upstream_object_reference','license_provenance_state','license_provenance_state'),
 ('p3_lineage_participation','participation_status','lineage_participation_status'),('p3_lineage_disposition','subject_type','object_type'),('p3_lineage_disposition','disposition_status','lineage_p3_disposition_status'),('p3_lineage_segment','segment_reason','lineage_segment_reason'),('p3_proposition_signature','signature_status','signature_status'),('p3_signature_field','field_name','signature_field_name'),('p3_signature_field','evidence_state','field_evidence_state'),('p3_signature_field','confidence','confidence_level'),('p3_signature_field_evidence','evidence_type','evidence_type'),('p3_signature_field_evidence','evidence_role','evidence_role'),('p3_response_contract_reference','response_topology','response_topology'),
 ('p3_pair_fact_bundle','orientation','relation_orientation'),('p3_pair_fact_bundle','relation_type','pair_relation_type'),('p3_pair_fact_bundle','target_relation','axis_relation'),('p3_pair_fact_bundle','operator_relation','axis_relation'),('p3_pair_fact_bundle','timeframe_relation','axis_relation'),('p3_pair_fact_bundle','response_relation','axis_relation'),('p3_pair_fact_bundle','p3_portability_ceiling','portability_ceiling'),('p3_pair_fact_bundle','j_family_candidate_eligibility','pair_authority_eligibility'),('p3_pair_fact_source_authority','registry_code','upstream_registry'),('p3_pair_fact_source_authority','authority_role','source_authority_role'),('p3_pair_fact_evidence','side','evidence_side'),('p3_pair_fact_evidence','evidence_type','evidence_type'),
 ('p3_collision_scope_registry','collision_type','collision_type'),('p3_collision_scope_registry','scope_type','collision_scope'),('p3_collision_scope_registry','orientation','collision_orientation'),('p3_candidate_revision','lifecycle_stage','lifecycle_stage'),('p3_candidate_revision','candidate_classification','candidate_classification'),('p3_candidate_revision','candidate_origin_type','candidate_origin_type'),('p3_candidate_status_event','from_stage','lifecycle_stage','NO'),('p3_candidate_status_event','to_stage','lifecycle_stage'),('p3_candidate_membership','membership_role','candidate_membership_role'),('p3_candidate_diagnostic_flag','flag','candidate_diagnostic_flag'),('p3_internal_pair_matrix','pair_state','pair_state'),('p3_closure_obligation','obligation_type','closure_obligation_type'),('p3_closure_obligation','status','closure_status'),('p3_family_variant_revision','variant_dimension','variant_dimension'),('p3_family_variant_revision','value_portability_status','response_portability_status'),('p3_family_exclusion','exclusion_type','exclusion_type'),('p3_hyperedge','hyperedge_type','hyperedge_type'),('p3_hyperedge','authority_effect','hyperedge_authority_effect'),('p3_adjudication_decision','decision_status','adjudication_decision_status'),('p3_adjudication_decision','response_portability_status','response_portability_status'),('p3_adjudication_member','member_disposition','adjudication_member_disposition'),('p3_family_genealogy','relation_type','genealogy_relation_type'),('p3_family_genealogy_member','genealogy_role','genealogy_role'),('p3_doctrine_delta','required_rebuild_scope','rebuild_scope'),('p3_dependency_edge','dependency_role','dependency_role'),('p3_dependency_edge','impact_priority','impact_priority'),('p3_release_change_ledger','change_type','release_change_type'),('p3_failure_ledger','severity','failure_severity')]:
    t,c,d,*opt=item
    bind(t,c,d,opt[0] if opt else 'YES')
write_csv(SEC/'P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v3.csv',bindings)

# ---------- validation SQL ----------
valsql="""-- Rawlsing P3 logical validation queries v3. Read-only; phase-aware.
-- Q01 pre-promotion: pointer count must be 0 or 1. Post-promotion gate separately requires 1.
SELECT CASE WHEN COUNT(*)<=1 THEN 'PASS' ELSE 'FAIL' END AS q01_pointer_cardinality FROM p3_runtime_promotion_pointer;
SELECT CASE WHEN COUNT(*)=1 THEN 'PASS' ELSE 'FAIL' END AS q01b_postpromotion_pointer FROM p3_runtime_promotion_pointer;
SELECT CASE WHEN NOT EXISTS (SELECT 1 FROM p3_runtime_promotion_pointer p WHERE NOT EXISTS (SELECT 1 FROM p3_release_status_event e WHERE e.release_id=p.promoted_release_id AND e.status='PROMOTED')) THEN 'PASS' ELSE 'FAIL' END AS q02_pointer_has_promoted_event;
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q03_no_reflexive_pairs FROM p3_pair_fact_bundle WHERE left_object_id=right_object_id;
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q04_proposition_graph_types FROM p3_pair_fact_bundle WHERE proposition_graph_allowed IS DISTINCT FROM (relation_type IN ('PROPOSITION_RESPONSE_IDENTITY','PROPOSITION_IDENTITY_ONLY'));
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q05_no_path_authority FROM p3_pair_fact_bundle WHERE creates_endpoint_authority;
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q06_one_governing_source FROM p3_pair_fact_bundle p LEFT JOIN (SELECT pair_fact_id,COUNT(*) FILTER (WHERE governing) n FROM p3_pair_fact_source_authority GROUP BY pair_fact_id) s USING(pair_fact_id) WHERE COALESCE(s.n,0)<>1;
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q07_candidate_membership_unique FROM (SELECT candidate_revision_id,member_object_id,COUNT(*) n FROM p3_candidate_membership GROUP BY 1,2 HAVING COUNT(*)<>1) x;
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q08_complete_pair_matrix FROM p3_candidate_revision r JOIN (SELECT candidate_revision_id,COUNT(DISTINCT member_object_id) n FROM p3_candidate_membership GROUP BY 1) m USING(candidate_revision_id) LEFT JOIN (SELECT candidate_revision_id,COUNT(*) n FROM p3_internal_pair_matrix GROUP BY 1) x USING(candidate_revision_id) WHERE COALESCE(x.n,0)<>(m.n*(m.n-1))/2;
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q09_component_stored_counts FROM p3_candidate_component c LEFT JOIN (SELECT component_id,COUNT(*) n FROM p3_component_membership GROUP BY 1) m USING(component_id) WHERE COALESCE(m.n,0)<>c.member_count;
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q10_clean_candidate_blockers FROM p3_candidate_revision r WHERE r.candidate_classification='CLEAN_CANDIDATE' AND (EXISTS (SELECT 1 FROM p3_internal_pair_matrix x WHERE x.candidate_revision_id=r.candidate_revision_id AND x.pair_state IN ('DIRECT_COLLISION','DIRECT_UNRESOLVED','SIGNATURE_CONFLICT')) OR EXISTS (SELECT 1 FROM p3_closure_obligation o WHERE o.candidate_revision_id=r.candidate_revision_id AND o.status='OPEN'));
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q11_family_revision_complete FROM p3_canonical_family_revision f JOIN p3_proposition_signature s ON s.signature_id=f.canonical_signature_id LEFT JOIN (SELECT family_revision_id,COUNT(*) n FROM p3_canonical_family_membership GROUP BY 1) m USING(family_revision_id) WHERE COALESCE(m.n,0)<2 OR s.signature_status<>'COMPLETE';
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q12_rule_exclusion_present FROM p3_canonical_family_revision f WHERE NOT EXISTS (SELECT 1 FROM p3_family_exclusion e WHERE e.owner_object_id=f.canonical_family_id AND e.exclusion_type='RULE_BASED' AND e.authority_release_id=f.authority_release_id);
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q13_named_exclusions_when_needed FROM p3_adjudication_decision a WHERE a.decision_status IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS') AND EXISTS (SELECT 1 FROM p3_adjudication_member m WHERE m.adjudication_id=a.adjudication_id AND m.member_disposition='EXCLUDE') AND NOT EXISTS (SELECT 1 FROM p3_family_exclusion e WHERE e.owner_object_id=a.canonical_family_id AND e.exclusion_type='NAMED_MEMBER' AND e.authority_release_id=a.authority_release_id);
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q14_no_measurement_leak FROM p3_family_variant_revision WHERE value_portability_status<>'NOT_AUTHORIZED_BY_P3';
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q15_family_adjudication_consistency FROM p3_canonical_family f JOIN p3_adjudication_decision a ON a.adjudication_id=f.created_by_adjudication_id WHERE a.canonical_family_id IS DISTINCT FROM f.canonical_family_id OR a.decision_status NOT IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS');
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q15b_no_unadjudicated_at_p3_close FROM p3_lineage_disposition WHERE disposition_status='UNADJUDICATED';
-- Release event ordinals and transition chains.
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q16_release_event_contiguous FROM (SELECT release_id,MIN(event_ordinal) mi,MAX(event_ordinal) ma,COUNT(*) n FROM p3_release_status_event GROUP BY release_id HAVING MIN(event_ordinal)<>1 OR MAX(event_ordinal)<>COUNT(*)) x;
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q17_candidate_event_contiguous FROM (SELECT candidate_family_id,MIN(event_ordinal) mi,MAX(event_ordinal) ma,COUNT(*) n FROM p3_candidate_status_event GROUP BY candidate_family_id HAVING MIN(event_ordinal)<>1 OR MAX(event_ordinal)<>COUNT(*)) x;
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q18_signature_has_twelve_fields FROM p3_proposition_signature s LEFT JOIN (SELECT signature_id,COUNT(*) n FROM p3_signature_field GROUP BY 1) f USING(signature_id) WHERE COALESCE(f.n,0)<>12;
-- Polymorphic reference type checks are generated from P3_OBJECT_REFERENCE_TYPE_CONTRACT_v3.csv.
-- Genealogy cycle, relation cardinality, release parent cycle, snapshot/change-ledger diff, and lifecycle transition checks are generated by the v23 validator because they require recursive or contract-driven queries.
"""
(SEC/'sql/P3_DDL_VALIDATION_QUERIES_v3.sql').write_text(valsql)
shutil.copy2(V22/'sql/P3_SHADOW_MIGRATION_SKELETON_v2.sql',SEC/'sql/P3_SHADOW_MIGRATION_SKELETON_v3.sql')
_sp=SEC/'sql/P3_SHADOW_MIGRATION_SKELETON_v3.sql'; _sp.write_text(_sp.read_text().replace('skeleton v2','skeleton v3').replace('_v2.','_v3.'))
# release protocol copy
shutil.copy2(V22/'release/P3_AUTHORITY_RELEASE_MIGRATION_ROLLBACK_PROTOCOL_v2.md',SEC/'release/P3_AUTHORITY_RELEASE_MIGRATION_ROLLBACK_PROTOCOL_v3.md')
_rp=SEC/'release/P3_AUTHORITY_RELEASE_MIGRATION_ROLLBACK_PROTOCOL_v3.md'; _rp.write_text(_rp.read_text().replace('Protocol v2','Protocol v3').replace('_v2.','_v3.'))

# ---------- plan/support matrices ----------
# lifecycle unchanged but rename candidate classifications not in matrix
shutil.copy2(V22/'P3_LIFECYCLE_STATE_MACHINE_v2.csv',SEC/'P3_LIFECYCLE_STATE_MACHINE_v3.csv')
shutil.copy2(V22/'P3_RELATION_COMPOSITION_MATRIX_v2.csv',SEC/'P3_RELATION_COMPOSITION_MATRIX_v3.csv')
shutil.copy2(V22/'P3_EVIDENCE_SUFFICIENCY_MATRIX_v2.csv',SEC/'P3_EVIDENCE_SUFFICIENCY_MATRIX_v3.csv')
# pilot rules update
pilot=yaml.safe_load((V22/'P3_PILOT_SELECTION_RULES_v2.yaml').read_text())
pilot['global_generation_surface']['proposition_relation_pairs']=pilot['global_generation_surface'].pop('effective_connective_proposition_pairs')
pilot['global_generation_surface']['administrative_metadata_pairs_preflight']=1
pilot['global_generation_surface']['provisional_substantive_candidate_edges']=657
pilot['selection_goal']='Test family construction across substantive proposition authority, while separately retaining the administrative metadata proposition as a non-J-family diagnostic fixture.'
(SEC/'P3_PILOT_SELECTION_RULES_v3.yaml').write_text(yaml.safe_dump(pilot,sort_keys=False))
# execution sequence update
seq=yaml.safe_load((V22/'P3_EXECUTION_SEQUENCE_v2.yaml').read_text())
seq['plan_id']='RAWLSING_P3_STRUCTURE_ARTICULATION_IMPLEMENTATION_PLAN_V3';seq['corrected_by_release']='Rawlsing_J_Family_Authority_Strategy_Handoff_v23_20260731';seq['next_execution_point']='P3A_CONTRACT_AND_PILOT_V3_IMPLEMENTATION'
seq['global_controls']['effective_proposition_relation_pairs']=seq['global_controls'].pop('effective_connective_proposition_pairs');seq['global_controls']['provisional_substantive_candidate_edges']=657
seq['global_controls']['all_lineages_participation_accounted']=True
for ph in seq['phases']:
    if ph['phase']=='P3A-0':
        ph['steps'] += ['Freeze structure registry/memberships, structure rulings, semantic overlay, and the 13,526-lineage participation baseline.','Preserve both governing and superseded source-authority rows for every effective pair.']
        ph['exit']='All pair, structure, overlay, lineage, and source-authority inputs reconcile; no P2 mutation.'
    if ph['phase']=='P3A-3':
        ph['steps']=['Recover field-provenanced signatures for all 3,296 lineages incident to any effective direct pair authority.','Mark 10,230 nonincident lineages as NO_CURRENT_DIRECT_PAIR_AUTHORITY without inferring uniqueness or exclusion.','Create P3 segments only for material lineage drift.','Preserve response-contract and structural-context references without P4/P5 authority.']
    if ph['phase']=='P3A-4':
        ph['steps'][0]='Build the proposition-authority graph from 658 proposition pairs, then apply the substantive J-family eligibility gate; preserve administrative metadata relations in a separate diagnostic lane.'
    if ph['phase']=='P3A-5': ph['exit']='All 658 proposition relations and all 19,175 direct pair authorities represented; all 13,526 lineages have participation status.'
    if ph['phase']=='P3A-7': ph['name']='Pilot acceptance and v24 handoff';ph['exit']='P3 Contract and Pilot v3 accepted.'
(SEC/'P3_EXECUTION_SEQUENCE_v3.yaml').write_text(yaml.safe_dump(seq,sort_keys=False))
# plan lock
lock=json.loads((V22/'P3_PLAN_LOCK_v2.json').read_text());lock['plan_id']='RAWLSING_P3_STRUCTURE_ARTICULATION_IMPLEMENTATION_PLAN_V3';lock['plan_version']='v3';lock['planning_audit_handoff_version']='v23';lock['next_execution_point']='P3A_CONTRACT_AND_PILOT_V3_IMPLEMENTATION';lock['effective_input_surface'].update({'effective_relation_type_counts':dict(eff_counts),'proposition_graph_endpoints':len(prop_ep),'all_effective_pair_endpoints':len(all_ep),'lineages_no_current_direct_pair_authority':part_counts['NO_CURRENT_DIRECT_PAIR_AUTHORITY'],'administrative_metadata_proposition_pairs_preflight':1,'provisional_substantive_j_family_candidate_edges':657})
lock['locked_doctrine'] += ['all 13,526 lineages receive an explicit P3 participation status','absence from the current pair surface does not prove uniqueness or permanent exclusion','administrative metadata proposition identity is preserved outside substantive J-family connectivity','candidate risk classes are multi-valued diagnostic flags and cannot serve as final decisions','canonical serialization and object-reference type contracts govern all derived IDs and polymorphic references']
lock['pilot'].update({'global_relation_surface':658,'provisional_substantive_candidate_edges':657,'lineage_participation_total':13526})
dumpj(SEC/'P3_PLAN_LOCK_v3.json',lock)

# compatibility matrix update
compat=read_csv(V22/'P3_UPSTREAM_DOWNSTREAM_COMPATIBILITY_MATRIX_v2.csv')
compat.append({'interface':'P3_LINEAGE_COVERAGE','authoritative_input':'13,526 lineage registry + effective pair surface','p3_or_downstream_output':'participation status for every lineage','required_gate':'399 proposition-incident + 2,897 constraint-only + 10,230 no-current-pair reconcile','authority_mode':'COVERAGE_ACCOUNTING_ONLY','first_phase':'P3A-0'})
compat.append({'interface':'P3_ADMINISTRATIVE_METADATA','authoritative_input':'proposition identity involving administrative/interviewer metadata','p3_or_downstream_output':'non-J-family diagnostic relation','required_gate':'cannot enter substantive family connectivity','authority_mode':'PRESERVE_WITHOUT_SUBSTANTIVE_FAMILY_AUTHORITY','first_phase':'P3A-3/P3A-4'})
write_csv(SEC/'P3_UPSTREAM_DOWNSTREAM_COMPATIBILITY_MATRIX_v3.csv',compat)
# downstream docs
shutil.copy2(V22/'downstream/P3_DOWNSTREAM_INTERFACE_REGISTRY_v2.csv',SEC/'downstream/P3_DOWNSTREAM_INTERFACE_REGISTRY_v3.csv')
shutil.copy2(V22/'downstream/P3_DOWNSTREAM_INTERFACES_v2.md',SEC/'downstream/P3_DOWNSTREAM_INTERFACES_v3.md')
_dp=SEC/'downstream/P3_DOWNSTREAM_INTERFACES_v3.md'; _dp.write_text(_dp.read_text().replace('Interfaces v2','Interfaces v3').replace('_v2.','_v3.'))

# artifact catalog update
cat=read_csv(V22/'P3_ARTIFACT_CATALOG_v2.csv')
for r in cat:
    r['artifact']=r['artifact'].replace('_v2.','_v3.').replace('verify_handoff_v22.py','verify_handoff_v23.py').replace('P3_DOCUMENT_QA_RETURN_v2.json','P3_DOCUMENT_QA_RETURN_v3.json')
extra=[
 {'artifact':'upstream/P3_EFFECTIVE_PAIR_SOURCE_AUTHORITY_SURFACE_v3.csv','class':'CANONICAL_INPUT_AUDIT','function':'One row per semantic/exact source authority with governing or superseded role','first_phase':'P3A','required_for_phase_close':'YES'},
 {'artifact':'upstream/P3_LINEAGE_PARTICIPATION_BASELINE_v3.csv','class':'CANONICAL_INPUT_AUDIT','function':'Participation status for all 13,526 lineages','first_phase':'P3A','required_for_phase_close':'YES'},
 {'artifact':'upstream/P3_UPSTREAM_INPUT_MANIFEST_v3.csv','class':'CANONICAL_INPUT_CONTRACT','function':'Hashes and counts for pair, lineage, structure, and overlay authorities','first_phase':'P3A','required_for_phase_close':'YES'},
 {'artifact':'P3_OBJECT_REFERENCE_TYPE_CONTRACT_v3.csv','class':'CANONICAL_CONTRACT','function':'Allowed object types for polymorphic registry-backed references','first_phase':'P3A','required_for_phase_close':'YES'},
 {'artifact':'P3_IDENTITY_KEY_SPEC_v3.csv','class':'CANONICAL_CONTRACT','function':'Canonical idempotency keys and serialization rules','first_phase':'P3A','required_for_phase_close':'YES'},
 {'artifact':'p3_lineage_participation.csv','class':'CANONICAL','function':'Release-scoped P3 participation status for every source-local lineage','first_phase':'P3A','required_for_phase_close':'YES'},
 {'artifact':'p3_candidate_diagnostic_flags.csv','class':'DERIVED_GOVERNED','function':'Multi-valued risk and pilot-selection diagnostics','first_phase':'P3A','required_for_phase_close':'YES'},
]
cat.append({'artifact':'upstream/P3_PROPOSITION_RELATION_ELIGIBILITY_PREFLIGHT_v3.csv','class':'UPSTREAM_PREFLIGHT','function':'Separates proposition authority from provisional substantive J-family eligibility','first_phase':'P3A','required_for_phase_close':'YES'})
cat.append({'artifact':'upstream/P3_PROPOSITION_GRAPH_PREFLIGHT_RETURN_v3.json','class':'UPSTREAM_PREFLIGHT','function':'Graph-scale diagnostics without candidate authority','first_phase':'P3A','required_for_phase_close':'YES'})
cat.append({'artifact':'p3_lineage_disposition.csv','class':'CANONICAL_AUTHORITY','function':'Terminal no-loss P3 treatment for every lineage or governed segment','first_phase':'P3A','required_for_phase_close':'YES'})
cat=[r for r in cat if 'INHERITED_V21_PAYLOAD_HASHES' not in r.get('artifact','')]
cat.append({'artifact':'validation/build_handoff_v23.py','class':'ASSEMBLY_PROVENANCE','function':'Path-specific builder that produced section 45 and v23 controls; not a live installer','first_phase':'P3A','required_for_phase_close':'NO'})
cat.append({'artifact':'validation/INHERITED_V22_PAYLOAD_HASHES.csv','class':'PROVENANCE_VALIDATION','function':'Hashes inherited v22 payload outside superseded controls','first_phase':'P3A','required_for_phase_close':'YES'})
cat.extend(extra);write_csv(SEC/'P3_ARTIFACT_CATALOG_v3.csv',cat)

# ---------- Plan v3 ----------
plan=(V22/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v2_20260731.md').read_text()
plan=plan.replace('**Plan version:** v2','**Plan version:** v3').replace('P3A_CONTRACT_AND_PILOT_V2_IMPLEMENTATION','P3A_CONTRACT_AND_PILOT_V3_IMPLEMENTATION').replace('P3 Contract and Pilot v2','P3 Contract and Pilot v3')
plan=plan.replace('# Rawlsing P3 Structure Articulation and Implementation Plan v2','# Rawlsing P3 Structure Articulation and Implementation Plan v3')
plan=plan.replace('P3_RELATION_COMPOSITION_MATRIX_v2.csv','P3_RELATION_COMPOSITION_MATRIX_v3.csv')
plan=plan.replace('The v2 machine-readable pack contains:','The v3 machine-readable pack contains:')
plan=plan.replace('twenty-two connected JSON schemas','thirty-six connected JSON schemas')
plan=plan.replace('P3A must use only the v2 contracts in section 44.','P3A must use only the v3 contracts in section 45.')
plan=plan.replace('its v1 machine contract is superseded by section 44','its earlier machine contracts are superseded by section 45')

plan=plan.replace('`upstream/P3_UPSTREAM_AUTHORITY_PRECEDENCE.csv`, `upstream/P3_P2_TO_P3_AUTHORITY_MAPPING.csv`, and `upstream/P3_EFFECTIVE_UPSTREAM_PAIR_AUTHORITY_SURFACE.csv`.', '`upstream/P3_UPSTREAM_AUTHORITY_PRECEDENCE_v3.csv`, `upstream/P3_P2_TO_P3_AUTHORITY_MAPPING_v3.csv`, `upstream/P3_EFFECTIVE_UPSTREAM_PAIR_AUTHORITY_SURFACE_v3.csv`, and the row-level `P3_EFFECTIVE_PAIR_SOURCE_AUTHORITY_SURFACE_v3.csv`.')
coverage_section='''\n# 2B. Lineage participation and substantive eligibility\n\nThe effective direct-pair surface touches 3,296 of the 13,526 source-local lineages. Of these, 399 participate in at least one proposition relation and 2,897 appear only in coordinate, hierarchy, negative, redirect, or unresolved authority. The remaining 10,230 lineages have no direct pair authority in the current closed surface.\n\nP3 must account for all 13,526 lineages through `p3_lineage_participation.csv`. `NO_CURRENT_DIRECT_PAIR_AUTHORITY` means only that the closed P2 surface supplies no current direct pair ruling for that lineage. It does not prove semantic uniqueness, permanent exclusion, or ineligibility for later attachment. P3A recovers full signatures for all 3,296 pair-incident lineages; the 10,230 nonincident lineages remain read-only imported objects whose signatures are recovered only when new authority, a new wave, or an explicit attachment review makes them relevant.\n\nP2 proposition identity and substantive J-family eligibility are also separate. The current 658-pair proposition surface contains one exact-only administrative interviewer-metadata relation concerning the proportion of questions a respondent had difficulty answering. P3 preserves that proposition relation but routes it to an administrative diagnostic lane. The current preflight therefore identifies 657 provisionally substantive candidate edges. P3A must recompute this eligibility from field-provenanced signatures rather than treating the preflight count as irreversible doctrine.\n\n'''
plan=plan.replace('# 3. P3 mandate and non-mandate',coverage_section+'# 3. P3 mandate and non-mandate')
# Candidate classification section corrections
plan=plan.replace('Each candidate should be assigned one of these statuses:', 'Each candidate revision receives one non-terminal primary diagnostic classification plus zero or more diagnostic flags. These diagnostics order work and expose risk; they never constitute the adjudication decision. The primary classifications are:')
repls={'CLEAN_FAMILY_CANDIDATE':'CLEAN_CANDIDATE','RESPONSE_VARIANT_CANDIDATE':'VARIANT_BEARING_CANDIDATE','SPLIT_REQUIRED':'SPLIT_RISK','HIERARCHICAL_FAMILY_CANDIDATE':'HIERARCHY_ONLY_RISK','COLLISION_BEARING_CANDIDATE':'COLLISION_BEARING_CANDIDATE','STRUCTURAL_ANALOGY_ONLY':'STRUCTURE_ONLY_DIAGNOSTIC','INSUFFICIENT_AUTHORITY':'INSUFFICIENT_AUTHORITY_RISK','REJECTED_COMPONENT':'SEMANTIC_ARTIFACT_RISK'}
for a,b in repls.items():plan=plan.replace(a,b)
plan=plan.replace('Every accepted family has named and rule-based exclusions.', 'Every accepted family has at least one rule-based exclusion. Named exclusions are mandatory whenever the candidate or adjudication surface contains rejected near-neighbor objects; they are never fabricated merely to satisfy a count.')
plan=plan.replace('## Named exclusions\n', '## Named exclusions\n\nNamed exclusions are mandatory whenever there are actually rejected near-neighbors. They are not fabricated when no such rejected object exists.\n')
plan=plan.replace('every accepted family has named and rule-based exclusions;', 'every accepted family has a rule-based exclusion and all actually rejected near-neighbors are preserved as named exclusions;')
# Add serialization/type section before storage
serial='''\n# 33A. Canonical serialization, IDs, and polymorphic type safety\n\nEvery content hash and content-addressed ID uses canonical UTF-8 JSON with sorted object keys, no insignificant whitespace, normalized line endings, and deterministic ordering of sets before serialization. Hash inputs and idempotency-key fields are fixed in `P3_IDENTITY_KEY_SPEC_v3.csv`; display prefixes never substitute for full SHA-256 collision checks.\n\nA foreign key to `p3_object_registry` proves existence but not semantic type. `P3_OBJECT_REFERENCE_TYPE_CONTRACT_v3.csv` therefore governs every polymorphic reference. Builders and shadow-install validators must reject, for example, a structure ID used as a lineage endpoint, an implementation ID used as a family owner, or a candidate ID used where a canonical family is required.\n\n'''
plan=plan.replace('# 21. Explicit exclusion surfaces', '''# 20B. Complete lineage disposition and no-loss closure

P3 family construction is not permitted to make the 13,127 lineages outside the proposition graph disappear. Participation describes the current P2 evidence surface; disposition records the terminal P3 treatment of each lineage or governed segment.

Every one of the 13,526 source-local lineages must have exactly one current release disposition by P3 closure: candidate member, canonical member, source-local singleton preserved, constraint-only preserved, administrative metadata preserved, derived/index preserved, blocked unresolved, out-of-scope nonquestion, or superseded by governed segments. A source-local singleton is preserved as a substantive lineage without manufacturing cross-source equivalence. `NO_CURRENT_DIRECT_PAIR_AUTHORITY` never means that a lineage may be dropped.

P3A initializes the disposition ledger as `UNADJUDICATED`. It fully adjudicates the pilot surface while preserving all other lineages for later tranches. Global P3 closure requires zero `UNADJUDICATED` lineages, and all 18,276 implementations must remain reachable through their original source-local lineage or an explicitly governed P3 segment. This is lineage accounting, not a requirement that every lineage become a canonical cross-source family.

'''+'# 21. Explicit exclusion surfaces')
plan=plan.replace('# 34. Performance and implementation stack',serial+'# 34. Performance and implementation stack')
# update execution steps text
plan=plan.replace('recover signatures for all incident lineages;', 'recover signatures for all 3,296 lineages incident to any effective direct pair authority and preserve participation status for all 13,526 lineages;')
plan=plan.replace('build strict seed components;', 'apply the substantive-eligibility gate, preserve administrative proposition relations outside J-family connectivity, and build strict seed components;')
# append second audit corrections
append='''\n# 42B. V22 second-acceptance hardening\n\nThe second independent audit retained v22's central ontology but found implementation gaps that would have forced redesign during P3A. V3 corrects them before execution:\n\n- all 13,526 lineages now receive explicit participation accounting: 399 proposition-incident, 2,897 constraint-only, and 10,230 with no current direct pair authority;\n- the 658 proposition relations are separated from substantive J-family eligibility, preserving one administrative interviewer-metadata relation in a non-substantive diagnostic lane;\n- every semantic and exact-foundation source-authority row is preserved at pair level, including all 407 superseded exact overlaps;\n- candidate risk is multi-valued through diagnostic flags rather than forced into one mutually exclusive label or confused with terminal adjudication;\n- JSON schemas now type split points, hyperedge context, structural context, variant assignments, hierarchy relations, collision dispositions, unresolved boundaries, canonical propositions, rankings, status events, and lineage participation;\n- completed adjudications enforce decision-specific requirements; pair facts enforce exactly one governing source authority and relation/connectivity compatibility; genealogy schemas enforce split/merge/deprecation cardinality;\n- the release schema now matches the append-only release/status-event persistence model;\n- DDL vocabulary bindings cover the actual columns, the collision-scope typo is corrected, candidate membership is one-role-per-member per revision, candidate ranking and diagnostic tables exist, closure-resolution and canonical-family references are typed, and object-reference type contracts govern polymorphic IDs;\n- pre-promotion and post-promotion validation are separated, preventing a shadow schema with no current pointer from failing the wrong gate;\n- rule-based exclusions are always mandatory, while named exclusions are required when there are actually rejected near-neighbors rather than fabricated for formal symmetry;\n- canonical serialization and exact idempotency-key rules are fixed before any IDs are allocated.\n\nSection 45 and Plan v3 supersede the v22 machine contract. Sections 43 and 44 remain historical provenance.\n\n'''
plan=plan.replace('# 43. Final governing statement',append+'# 43. Final governing statement')
# Replace the long proposition-signature Markdown table with a compact governed list for stable DOCX pagination.
_sig_table='''| Dimension | Function |
|---|---|
| `subject_role` | Respondent, household, parent, government, institution, group, country, derived system |
| `operator` | Trust, satisfaction, support, action, willingness, expectation, preference, evaluation, and so forth |
| `target` | The concrete social object or institution |
| `object_or_outcome` | What the operator concerns |
| `modality` | Actual behavior, disposition, evaluation, belief, frequency, expectation, state, or principle |
| `timeframe` | Past, present, future, named interval, or explicitly unspecified |
| `condition` | Condition governing the proposition |
| `population_scope` | Self, household, citizens, immigrants, women, foreign workers, and so forth |
| `geographic_scope` | Local, national, named country, or explicitly unspecified |
| `polarity` | Positive, negative, exclusionary, reverse-worded |
| `derived_status` | Direct item, composite, index, calculated measure |
| `parent_context` | Battery parent supplying an elliptical operator, target, or condition |'''
_sig_list='''- `subject_role` — respondent, household, parent, government, institution, group, country, or derived system;
- `operator` — trust, satisfaction, support, action, willingness, expectation, preference, evaluation, and so forth;
- `target` — the concrete social object or institution;
- `object_or_outcome` — what the operator concerns;
- `modality` — actual behavior, disposition, evaluation, belief, frequency, expectation, state, or principle;
- `timeframe` — past, present, future, named interval, or explicitly unspecified;
- `condition` — the condition governing the proposition;
- `population_scope` — self, household, citizens, immigrants, women, foreign workers, and so forth;
- `geographic_scope` — local, national, named country, or explicitly unspecified;
- `polarity` — positive, negative, exclusionary, or reverse-worded;
- `derived_status` — direct item, composite, index, or calculated measure;
- `parent_context` — the battery parent supplying an elliptical operator, target, or condition.'''
plan=plan.replace(_sig_table,_sig_list)
(SEC/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v3_20260731.md').write_text(plan)

# Algorithms v3
alg=(V22/'algorithms/P3_ALGORITHMS_AND_PSEUDOCODE_v2.md').read_text().replace('v2','v3').replace('effective connective proposition pairs: 658','proposition relation pairs: 658; current substantive-eligibility preflight: 657 plus one administrative diagnostic')
alg=alg.replace('## B. Register upstream objects read-only','## A2. Freeze source-authority provenance and lineage participation\nEmit one source-authority row for every semantic and exact-foundation ruling, marking exactly one governing row per effective pair and every exact overlap as superseded provenance. Classify all 13,526 lineages as proposition-incident, constraint-only, or no-current-direct-pair-authority.\n\n## B. Register upstream objects read-only')
alg=alg.replace('Connectivity contains only governing `PROPOSITION_RESPONSE_IDENTITY` and `PROPOSITION_IDENTITY_ONLY` facts.', 'The proposition-authority graph contains governing `PROPOSITION_RESPONSE_IDENTITY` and `PROPOSITION_IDENTITY_ONLY` facts. A separate substantive-eligibility gate excludes administrative metadata from J-family candidate connectivity while preserving its pair authority.')
alg += '\n\n## U. Canonical serialization and reference-type enforcement\nBefore hashing or ID allocation, canonicalize JSON and set-like arrays under P3_IDENTITY_KEY_SPEC_v3.csv. Validate every registry-backed polymorphic reference against P3_OBJECT_REFERENCE_TYPE_CONTRACT_v3.csv.\n'
(SEC/'algorithms/P3_ALGORITHMS_AND_PSEUDOCODE_v3.md').write_text(alg)

# acceptance gates/test/contingency v3
ag=read_csv(V22/'validation/P3_ACCEPTANCE_GATES_v2.csv')
ag.extend([
 {'gate_id':'P3G-047','phase':'PLAN','severity':'FATAL','requirement':'All 13,526 lineages reconcile to proposition-incident, constraint-only, or no-current-direct-pair-authority participation.'},
 {'gate_id':'P3G-048','phase':'PLAN','severity':'FATAL','requirement':'Every effective pair preserves exactly one governing source-authority row and all superseded exact overlap rows.'},
 {'gate_id':'P3G-049','phase':'PLAN','severity':'FATAL','requirement':'Administrative metadata proposition relations cannot enter substantive J-family connectivity.'},
 {'gate_id':'P3G-050','phase':'PLAN','severity':'FATAL','requirement':'Every categorical binding names a real DDL table/column and every finite categorical column is bound.'},
 {'gate_id':'P3G-051','phase':'PLAN','severity':'FATAL','requirement':'Every registry-backed polymorphic reference satisfies its allowed object-type contract.'},
 {'gate_id':'P3G-052','phase':'PLAN','severity':'FATAL','requirement':'Final adjudication nested structures are typed and status-specific requirements fail closed.'},
 {'gate_id':'P3G-053','phase':'P3A','severity':'FATAL','requirement':'Candidate internal pair matrices use canonical unordered endpoint order and count distinct members exactly once.'},
 {'gate_id':'P3G-054','phase':'P3B','severity':'FATAL','requirement':'Every accepted family has rule-based exclusions and all actually excluded near-neighbors have named exclusions.'},
 {'gate_id':'P3G-055','phase':'RELEASE','severity':'FATAL','requirement':'Canonical serialization and idempotency-key rules reproduce hashes and stable IDs exactly.'},
])
write_csv(SEC/'validation/P3_ACCEPTANCE_GATES_v3.csv',ag)
tp=read_csv(V22/'validation/P3_TEST_AND_MUTATION_PLAN_v2.csv')
tp.extend([
 {'test_id':'P3T-041','test_class':'integration','required':'YES','test_definition':'All 13,526 lineages reconcile to 399 proposition-incident, 2,897 constraint-only, and 10,230 no-current-direct-pair-authority.'},
 {'test_id':'P3T-042','test_class':'mutation','required':'YES','test_definition':'Change collision binding from scope_type to a nonexistent column and validation fails.'},
 {'test_id':'P3T-043','test_class':'mutation','required':'YES','test_definition':'Insert two governing source authorities into one pair fact and schema/validator fail.'},
 {'test_id':'P3T-044','test_class':'mutation','required':'YES','test_definition':'Insert administrative metadata proposition into substantive candidate connectivity and eligibility gate fails.'},
 {'test_id':'P3T-045','test_class':'mutation','required':'YES','test_definition':'Assign two membership roles to one candidate member in one revision and uniqueness fails.'},
 {'test_id':'P3T-046','test_class':'mutation','required':'YES','test_definition':'Use wrong object type for a polymorphic reference and type-contract validation fails.'},
 {'test_id':'P3T-047','test_class':'mutation','required':'YES','test_definition':'Accept family with rejected near-neighbor but no named exclusion and close gate fails.'},
 {'test_id':'P3T-048','test_class':'property','required':'YES','test_definition':'Canonical serialization produces identical hashes across key order, row order, and platform newline variation.'},
])
write_csv(SEC/'validation/P3_TEST_AND_MUTATION_PLAN_v3.csv',tp)
cont=read_csv(V22/'validation/P3_CONTINGENCY_MATRIX_v2.csv')
cont.extend([
 {'contingency':'Lineage has no current direct pair authority','required_response':'Record NO_CURRENT_DIRECT_PAIR_AUTHORITY; do not infer uniqueness, permanent exclusion, or singleton family.','fail_closed':'YES'},
 {'contingency':'Proposition relation concerns administrative/interviewer metadata','required_response':'Preserve proposition authority in diagnostic lane; exclude from substantive J-family connectivity unless explicit downstream mandate changes.','fail_closed':'YES'},
 {'contingency':'Candidate fits multiple risk classes','required_response':'Use multi-valued diagnostic flags plus one primary review classification; do not force information loss.','fail_closed':'YES'},
 {'contingency':'Polymorphic registry reference has wrong object type','required_response':'Fatal type-contract violation; block build or migration.','fail_closed':'YES'},
 {'contingency':'Shadow schema has no promoted pointer before promotion','required_response':'Pass pre-promotion cardinality gate; require exactly one pointer only at post-promotion gate.','fail_closed':'YES'},
])
write_csv(SEC/'validation/P3_CONTINGENCY_MATRIX_v3.csv',cont)

# templates v3
packet={
 'packet_id':'P3PKT-000001','candidate_family':{
  'candidate_family_id':'P3CAND-000001','revision_id':'P3CANDREV-00000001','component_ids':['P3COMP-0123456789abcdef'],'member_ids':['p2lineage_example_a','p2lineage_example_b'],'canonical_signature_id':None,'lifecycle_stage':'ADJUDICATION_REQUIRED','candidate_classification':'CLEAN_CANDIDATE','candidate_origin_type':'STRICT_RESPONSE_COMPONENT','diagnostic_flags':[],
  'internal_pair_counts':{'expected_pairs':1,'direct_positive':1,'direct_collision':0,'hierarchical_only':0,'unruled':0,'signature_conflict':0,'signature_compatible':0},'closure_obligation_ids':[],'variant_ids':[],'exclusion_ids':['P3EXC-000001'],
  'ranking':{'candidate_revision_id':'P3CANDREV-00000001','primary_class_rank':0,'hard_collision_count':0,'open_obligation_count':0,'signature_completeness':1.0,'source_count':2,'lineage_count':2,'direct_positive_density':1.0,'structure_support_count':0,'response_variant_complexity':0,'authority_release_id':'P3-AUTHORITY-2026-08-01-R1'},
  'evidence_bundle_hash':'0'*64,'authority_release_id':'P3-AUTHORITY-2026-08-01-R1'},
 'members_by_source':{'GSS':['p2lineage_example_a'],'WVS':['p2lineage_example_b']},
 'proposition_signature_matrix':[], 'response_contract_matrix':[],
 'internal_pair_matrix':[{'left_id':'p2lineage_example_a','right_id':'p2lineage_example_b','pair_state':'DIRECT_POSITIVE','pair_fact_id':'P3PF-00000001','collision_ids':[],'closure_obligation_ids':[]}],
 'hard_collisions':[],'unresolved_pairs':[],'unruled_pairs':[],'closure_obligations':[],'likely_split_points':[],'proposed_variants':[],
 'explicit_exclusions':[{'exclusion_id':'P3EXC-000001','owner_object_id':'P3CAND-000001','exclusion_type':'RULE_BASED','prohibited_operation':'BLOCK_OPERATOR_OR_TARGET_COLLAPSE','evidence_or_rule':'Different operator or target remains outside the family.','scope':'FAMILY_WIDE','tested_surface_complete':False,'excluded_object_ids':[],'authority_release_id':'P3-AUTHORITY-2026-08-01-R1'}],
 'hyperedge_context':[],'strata_horizon_context':[],'exact_evidence_links':['evidence_left','evidence_right'],'evidence_bundle_hash':'0'*64,
 'decision_form':{'adjudication_id':'P3ADJ-000001','candidate_family_id':'P3CAND-000001','candidate_revision_id':'P3CANDREV-00000001','decision_status':None,'canonical_family_id':None,'canonical_proposition':None,'accepted_members':[],'excluded_members':[],'variant_assignments':[],'hierarchical_relations':[],'collision_dispositions':[],'response_portability_status':'NOT_AUTHORIZED_BY_P3','unresolved_boundaries':[],'rationale':'','evidence_bundle_hash':'0'*64,'supersedes_adjudication_id':None,'authority_release_id':'P3-AUTHORITY-2026-08-01-R1'}
}
# populate signatures and response refs
sigbase={'response_topologies':['ORDINAL'],'signature_status':'COMPLETE','content_hash':'0'*64,'authority_release_id':'P3-AUTHORITY-2026-08-01-R1'}
for i,lid in enumerate(['p2lineage_example_a','p2lineage_example_b'],1):
 fields={}
 for f in field_props:
  code=None; val='example'
  if f=='subject_role':code='RESPONDENT';val='respondent'
  elif f=='operator':code='TRUST';val='trust'
  elif f=='target':val='police'
  elif f=='modality':code='DIRECT_PROPOSITION';val='direct proposition'
  elif f=='timeframe':code='EXPLICITLY_UNSPECIFIED';val=None
  elif f=='population_scope':code='SELF';val='self'
  elif f=='geographic_scope':code='NATIONAL';val='national'
  elif f=='polarity':code='POSITIVE';val='positive'
  elif f=='derived_status':code='DIRECT_ITEM';val='direct item'
  elif f in ('condition','parent_context','object_or_outcome'): val=None
  state='KNOWN' if val is not None else 'NOT_APPLICABLE'
  if state!='KNOWN': code=None
  fields[f]={'field_value':val,'normalized_value_code':code,'evidence_state':state,'confidence':'HIGH' if state=='KNOWN' else 'NOT_APPLICABLE','evidence_ids':[f'evidence_{i}_{f}'] if state=='KNOWN' else []}
 packet['proposition_signature_matrix'].append({'signature_id':f'P3SIG-{i:06d}','subject_id':lid,'subject_type':'IMPORTED_SOURCE_LOCAL_LINEAGE','fields':fields,**sigbase})
 packet['response_contract_matrix'].append({'reference_id':f'P3RCR-{i:06d}','subject_id':lid,'upstream_response_contract_id':None,'response_topology':'ORDINAL','response_contract_hash':None,'authority_artifact':'example','p4_authority':False,'authority_release_id':'P3-AUTHORITY-2026-08-01-R1'})
dumpj(SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v3.json',packet)
dumpj(SEC/'adjudication/P3_ADJUDICATION_DECISION_DRAFT_TEMPLATE_v3.json',packet['decision_form'])
final=dict(packet['decision_form']);final.update({'decision_status':'ACCEPTED_CANONICAL','canonical_family_id':'JFAM-000001','canonical_proposition':{k:(packet['proposition_signature_matrix'][0]['fields'][k]['field_value']) for k in field_props},'accepted_members':['p2lineage_example_a','p2lineage_example_b'],'rationale':'Two-sided proposition authority and complete signatures support canonical admission.'})
dumpj(SEC/'adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v3.json',final)

# ---------- Report and README ----------
report=f'''# Rawlsing P3 Plan Second Acceptance Audit and Hardening Report\n\n## Verdict\n\nThe v22 plan corrected major defects, but a second independent implementation audit found additional blockers that would have forced P3A redesign. The central P3 ontology remains sound. Plan v3 hardens coverage, substantive eligibility, schema typing, persistence, identity, release, and downstream contracts before any candidate execution.\n\n## Corrected findings\n\n1. **Lineage coverage was implicit.** Only 399 of 13,526 lineages touch proposition authority; 2,897 are constraint-only and 10,230 have no current direct pair authority. V3 governs all lineages through a participation ledger without treating absence as uniqueness.\n2. **One proposition edge is administrative metadata.** The Afrobarometer/Asian Barometer interviewer item about respondent difficulty is valid proposition identity but not a substantive J-family edge. V3 separates proposition authority from J-family eligibility.\n3. **Overlap provenance was not row-complete.** V3 delivers {len(source_rows):,} source-authority rows: one governing row for every effective pair plus all 407 superseded exact overlaps.\n4. **Candidate risk was forced into one label.** V3 adds multi-valued diagnostic flags and prevents provisional risk labels from impersonating terminal adjudication.\n5. **Nested JSON payloads remained untyped.** Split points, hierarchy, collisions, unresolved boundaries, variants, structural context, canonical propositions, rankings, and status events now have schemas.\n6. **Decision schemas lacked status-specific constraints.** Accepted, rejected, split, hierarchical, and blocked outcomes now fail closed under different required fields.\n7. **Release JSON contradicted append-only SQL.** Release identity and status-event schemas now match separate persistence tables.\n8. **Vocabulary binding contained a nonexistent `scope` column and omitted finite fields.** V3 binds actual columns, including `scope_type`, status events, hyperedges, pair axes, diagnostic flags, and provenance roles.\n9. **Candidate membership allowed multiple simultaneous roles.** V3 permits one role per member per candidate revision.\n10. **Candidate ranking was catalogued but absent from the DDL.** A typed ranking table and schema now exist.\n11. **Foreign keys proved existence but not object type.** A polymorphic object-reference type contract now governs lineage, implementation, candidate, family, and ownership references.\n12. **Pre-promotion validation incorrectly required a promoted pointer.** V3 separates pre- and post-promotion gates.\n13. **Canonical hashing lacked an exact serialization contract.** V3 fixes canonical JSON and idempotency-key rules before ID allocation.\n14. **Exclusion doctrine could force fabricated named exclusions.** Rule-based exclusions are always required; named exclusions are required whenever actual rejected near-neighbors exist.
15. **The family graph did not provide a terminal treatment for nonincident lineages.** V3 adds a no-loss lineage-disposition contract. P3 may preserve a substantive source-local singleton or a constraint-only, administrative, derived, unresolved, or segmented lineage without manufacturing cross-source equivalence. Global P3 closure requires all 13,526 lineages and all 18,276 implementations to remain accounted for.\n\n## Upstream reconciliation\n\n- effective direct pair authorities: 19,175;\n- source-authority provenance rows: {len(source_rows):,};\n- proposition relations: 658;\n- provisional substantive candidate edges: 657;\n- administrative proposition diagnostics: 1;\n- proposition-incident lineages: {part_counts['PROPOSITION_GRAPH_INCIDENT']:,};\n- constraint-only lineages: {part_counts['CONSTRAINT_ONLY_INCIDENT']:,};\n- no-current-direct-pair lineages: {part_counts['NO_CURRENT_DIRECT_PAIR_AUTHORITY']:,}.\n\nNo P3 candidate or canonical family authority was authored in this audit.\n'''
(SEC/'P3_PLAN_SECOND_ACCEPTANCE_AUDIT_AND_HARDENING_REPORT.md').write_text(report)
(SEC/'README_FIRST.md').write_text('# Section 45 - P3 Plan Second Acceptance Audit and Hardening\n\nPlan v3 and this section supersede the v22 machine contract. No P3 execution occurred.\n')
(SEC/'SUPERSEDES_SECTION_44.md').write_text('Section 44 remains historical acceptance provenance. Section 45 Plan v3 governs P3A execution.\n')
(SEC/'TASK_RETURN.md').write_text(report)

# Inherited-v22 payload integrity: every v22 file outside superseded start controls and package manifests must remain byte-identical.
inherited=[]
excluded_prefixes=('00_START_HERE/',)
excluded_names={'PACKAGE_INDEX.csv','SHA256SUMS.csv','CHECKSUM_MANIFEST.sha256','VALIDATION.json','MASTER_HANDOFF.md','README_FIRST.md'}
for sp in sorted(SRC.rglob('*')):
    if not sp.is_file(): continue
    rel=sp.relative_to(SRC).as_posix()
    if rel.startswith(excluded_prefixes) or rel in excluded_names: continue
    dp=ROOT/rel
    inherited.append({'relative_path':rel,'sha256':sha(sp),'present_in_v23':'YES' if dp.exists() else 'NO','v23_sha256':sha(dp) if dp.exists() else ''})
write_csv(SEC/'validation/INHERITED_V22_PAYLOAD_HASHES.csv',inherited)

# ---------- verifier v23 ----------
verifier=r'''#!/usr/bin/env python3
from pathlib import Path
import sys,csv,json,re,hashlib,collections
from jsonschema import Draft202012Validator,FormatChecker
from referencing import Registry,Resource
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[2]
sec=root/'45_P3_PLAN_SECOND_ACCEPTANCE_AUDIT_AND_HARDENING'
checks=[]
def ck(n,c,d=''): checks.append((n,bool(c),d)); print(('PASS ' if c else 'FAIL ')+n+((' '+str(d)) if d else ''))
def rows(p):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Core counts
ret=json.loads((sec/'upstream/P3_EFFECTIVE_INPUT_AND_COVERAGE_RETURN_v3.json').read_text())
ck('effective_19175',ret['effective_unique_direct_pair_authorities']==19175,ret)
ck('proposition_658',ret['proposition_relation_pairs']==658,ret)
ck('admin_preflight_1',ret['administrative_metadata_proposition_pairs_preflight']==1,ret)
ck('substantive_preflight_657',ret['provisional_substantive_j_family_candidate_edges']==657,ret)
ck('lineage_partition',ret['lineage_participation_counts']=={'CONSTRAINT_ONLY_INCIDENT':2897,'NO_CURRENT_DIRECT_PAIR_AUTHORITY':10230,'PROPOSITION_GRAPH_INCIDENT':399},ret['lineage_participation_counts'])
part=rows(sec/'upstream/P3_LINEAGE_PARTICIPATION_BASELINE_v3.csv');ck('lineage_rows_13526',len(part)==13526,len(part));ck('lineage_unique',len({r['lineage_id'] for r in part})==13526,'')
source=rows(sec/'upstream/P3_EFFECTIVE_PAIR_SOURCE_AUTHORITY_SURFACE_v3.csv');ck('source_authority_rows_19582',len(source)==19582,len(source))
by=collections.defaultdict(list)
for r in source:by[r['pair_key']].append(r)
ck('one_governing_each',len(by)==19175 and all(sum(x['authority_role']=='GOVERNING' for x in v)==1 for v in by.values()),'')
ck('407_superseded',sum(r['authority_role']=='SUPERSEDED_PROVENANCE' for r in source)==407,'')
# input manifest
for r in rows(sec/'upstream/P3_UPSTREAM_INPUT_MANIFEST_v3.csv'):
 p=root/r['relative_path'];ck('input_'+r['input_code'],p.exists() and sha(p)==r['sha256'] and (not r['actual_rows'] or int(r['actual_rows'])==int(r['expected_rows'])),r)
# vocab/bindings
v=rows(sec/'P3_CONTROLLED_VOCABULARIES_v3.csv');V=collections.defaultdict(set)
for r in v:V[r['vocabulary_domain']].add(r['code'])
ck('vocab_unique',len(v)==len({(r['vocabulary_domain'],r['code']) for r in v}),len(v))
ddl=(sec/'sql/p3_postgresql_compatible_ddl_v3.sql').read_text();blocks=dict(re.findall(r'CREATE TABLE\s+(\w+)\s*\((.*?)\);',ddl,re.S|re.I))
def parse_cols(b):
 depth=0;cur='';ps=[]
 for ch in b:
  if ch=='(':depth+=1
  elif ch==')':depth-=1
  if ch==',' and depth==0:ps.append(cur.strip());cur=''
  else:cur+=ch
 if cur.strip():ps.append(cur.strip())
 return {p.split()[0] for p in ps if p and not p.upper().startswith(('PRIMARY KEY','FOREIGN KEY','UNIQUE','CHECK','CONSTRAINT'))}
cols={t:parse_cols(b) for t,b in blocks.items()}
for r in rows(sec/'P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v3.csv'):
 ck('binding_'+r['table_name']+'_'+r['column_name'],r['table_name'] in cols and r['column_name'] in cols[r['table_name']] and r['vocabulary_domain'] in V,r)
ck('scope_type_binding',any(r['table_name']=='p3_collision_scope_registry' and r['column_name']=='scope_type' for r in rows(sec/'P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v3.csv')),'')
ck('membership_pk_one_role','PRIMARY KEY(candidate_revision_id,member_object_id));' in ddl,'')
ck('candidate_ranking_table','CREATE TABLE p3_candidate_ranking' in ddl,'')
ck('lineage_participation_table','CREATE TABLE p3_lineage_participation' in ddl,'')
ck('ddl_rollback',ddl.strip().endswith('ROLLBACK;'),'')
# schemas
registry=Registry();schemas={};ids=[]
for p in sorted((sec/'schemas').glob('*.json')):
 s=json.loads(p.read_text());Draft202012Validator.check_schema(s);schemas[p.name]=s;ids.append(s['$id']);registry=registry.with_resource(s['$id'],Resource.from_contents(s))
ck('schema_ids_unique',len(ids)==len(set(ids)),len(ids));ck('schema_count_ge_34',len(schemas)>=34,len(schemas))
referr=[]
for n,s in schemas.items():
 try:list(Draft202012Validator(s,registry=registry,format_checker=FormatChecker()).iter_errors({}))
 except Exception as e:referr.append((n,str(e)))
ck('offline_refs',not referr,referr)
examples=[('adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v3.json','candidate_packet.schema.json'),('adjudication/P3_ADJUDICATION_DECISION_DRAFT_TEMPLATE_v3.json','adjudication_decision_draft.schema.json'),('adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v3.json','adjudication_decision.schema.json')]
for f,sn in examples:
 errs=list(Draft202012Validator(schemas[sn],registry=registry,format_checker=FormatChecker()).iter_errors(json.loads((sec/f).read_text())));ck('example_'+Path(f).stem,not errs,[e.message for e in errs[:5]])
# Mutation tests
pf=json.loads((sec/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v3.json').read_text())
# two governing authorities should fail
pair={'pair_fact_id':'P3PF-00000001','left_id':'a','right_id':'b','orientation':'SYMMETRIC','relation_type':'PROPOSITION_IDENTITY_ONLY','source_authorities':[{'registry':'SEMANTIC_PRIORITY_CLOSURE','authority_id':'x','authority_role':'GOVERNING','superseded_by_authority_id':None},{'registry':'EXACT_FOUNDATION_CLOSURE','authority_id':'y','authority_role':'GOVERNING','superseded_by_authority_id':None}],'target_relation':None,'operator_relation':None,'timeframe_relation':None,'response_relation':None,'source_portability_ceiling':'QUESTION_PROPOSITION_ONLY','p3_portability_ceiling':'QUESTION_PROPOSITION_ONLY','proposition_graph_allowed':True,'j_family_candidate_eligibility':'J_FAMILY_CANDIDATE_ELIGIBLE','creates_endpoint_authority':False,'evidence_ids':['l','r'],'authority_release_id':'r'}
ck('mutation_two_governing_fails',bool(list(Draft202012Validator(schemas['pair_fact_bundle.schema.json'],registry=registry).iter_errors(pair))),'')
# accepted decision with no canonical family fails
fd=json.loads((sec/'adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v3.json').read_text());fd['canonical_family_id']=None
ck('mutation_accepted_without_family_fails',bool(list(Draft202012Validator(schemas['adjudication_decision.schema.json'],registry=registry).iter_errors(fd))),'')
# generic object arrays prohibited in critical schemas
def generic(x):
 if isinstance(x,dict):
  if x.get('type')=='array' and x.get('items')=={'type':'object'}:return True
  return any(generic(v) for v in x.values())
 if isinstance(x,list):return any(generic(v) for v in x)
 return False
for n in ['candidate_packet.schema.json','adjudication_decision.schema.json','canonical_family_revision.schema.json']:
 ck('no_generic_'+n,not generic(schemas[n]),'')
# reference type contract
ref=rows(sec/'P3_OBJECT_REFERENCE_TYPE_CONTRACT_v3.csv');ck('reference_contract_nonempty',len(ref)>=10,len(ref));ck('reference_columns_exist',all(r['table_name'] in cols and r['column_name'] in cols[r['table_name']] for r in ref),'')
# plan phrases
plan=(sec/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v3_20260731.md').read_text().lower()
for phrase in ['10,230','administrative interviewer-metadata','canonical serialization','p3a_contract_and_pilot_v3_implementation','named exclusions are mandatory whenever']:
 ck('plan_'+re.sub(r'\W+','_',phrase),phrase.lower() in plan,phrase)
# inherited payload hashes
inh=rows(sec/'validation/INHERITED_V22_PAYLOAD_HASHES.csv')
ck('inherited_payload_nontrivial',len(inh)>900,len(inh))
ck('inherited_payload_unchanged',all(r['present_in_v23']=='YES' and r['sha256']==r['v23_sha256'] and sha(root/r['relative_path'])==r['sha256'] for r in inh),'')
# DDL structural checks beyond column extraction
table_names=re.findall(r'CREATE TABLE\s+(\w+)\s*\(',ddl,re.I)
ck('ddl_table_names_unique',len(table_names)==len(set(table_names)),[x for x in set(table_names) if table_names.count(x)>1])
constraint_names=re.findall(r'ADD CONSTRAINT\s+(\w+)',ddl,re.I)
ck('ddl_constraint_names_unique',len(constraint_names)==len(set(constraint_names)),constraint_names)
positions={m.group(1):m.start() for m in re.finditer(r'CREATE TABLE\s+(\w+)\s*\(',ddl,re.I)}
forward=[];missing=[]
for m in re.finditer(r'CREATE TABLE\s+(\w+)\s*\((.*?)\);',ddl,re.I|re.S):
 t,b=m.group(1),m.group(2)
 for ref_t in re.findall(r'REFERENCES\s+(\w+)\s*\(',b,re.I):
  if ref_t not in positions: missing.append((t,ref_t))
  elif positions[ref_t]>m.start(): forward.append((t,ref_t))
ck('ddl_reference_tables_exist',not missing,missing)
ck('ddl_no_forward_inline_references',not forward,forward)
ck('ddl_one_deferred_closure_fk',ddl.count('p3_closure_resolution_adjudication_fk')==1,ddl.count('p3_closure_resolution_adjudication_fk'))
ck('ddl_one_deferred_family_fk',ddl.count('p3_adjudication_canonical_family_fk')==1,ddl.count('p3_adjudication_canonical_family_fk'))
ck('direct_unresolved_governed','DIRECT_UNRESOLVED' in V['pair_state'] and 'DIRECT_UNRESOLVED' in ddl,'')
# packet mutation: incomplete proposition signature must fail
bad=json.loads((sec/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v3.json').read_text())
del bad['proposition_signature_matrix'][0]['fields']['operator']
ck('mutation_missing_signature_field_fails',bool(list(Draft202012Validator(schemas['candidate_packet.schema.json'],registry=registry).iter_errors(bad))),'')
elig=rows(sec/'upstream/P3_PROPOSITION_RELATION_ELIGIBILITY_PREFLIGHT_v3.csv')
ck('eligibility_preflight_658',len(elig)==658,len(elig))
ck('eligibility_admin_one',sum(r['provisional_j_family_eligibility']=='ADMINISTRATIVE_METADATA_ONLY' for r in elig)==1,'')
graph=json.loads((sec/'upstream/P3_PROPOSITION_GRAPH_PREFLIGHT_RETURN_v3.json').read_text())
ck('graph_preflight_counts',graph['all_proposition_edges']==658 and graph['provisional_substantive_edges']==657 and graph['all_proposition_graph']['node_count']==399 and graph['provisional_substantive_graph']['node_count']==397,graph)
ck('lineage_disposition_schema','lineage_disposition.schema.json' in schemas,'')
ck('lineage_disposition_table','CREATE TABLE p3_lineage_disposition' in ddl,'')
ck('lineage_disposition_binding',any(r['table_name']=='p3_lineage_disposition' and r['column_name']=='disposition_status' for r in rows(sec/'P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v3.csv')),'')
ck('plan_no_loss_lineage','zero `unadjudicated` lineages' in plan and '18,276 implementations' in plan,'')
# package cleanliness
ck('no_p3_execution',not any((sec/x).exists() for x in ['p3_candidate_families.csv','p3_canonical_families.csv']),'')
debris=[p for p in root.rglob('*') if p.is_file() and (p.suffix=='.pyc' or '__pycache__' in p.parts or '.pytest_cache' in p.parts)]
ck('no_debris',not debris,[str(x) for x in debris[:10]])
passed=sum(c for _,c,_ in checks)
print(json.dumps({'status':'PASS' if passed==len(checks) else 'FAIL','checks_passed':passed,'checks_total':len(checks),'failures':[n for n,c,d in checks if not c]},indent=2))
sys.exit(0 if passed==len(checks) else 1)
'''
(SEC/'validation/verify_handoff_v23.py').write_text(verifier)
os.chmod(SEC/'validation/verify_handoff_v23.py',0o755)

# schema registry
reg=[]
for p in sorted((SEC/'schemas').glob('*.json')):
 s=json.loads(p.read_text());refs=[]
 def walk(x):
  if isinstance(x,dict):
   if '$ref' in x:refs.append(x['$ref'])
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 walk(s)
 reg.append({'schema_file':p.name,'schema_id':s['$id'],'sha256':sha(p),'references_json':json.dumps(sorted(set(refs)))})
write_csv(SEC/'P3_JSON_SCHEMA_REGISTRY_v3.csv',reg)

# ---------- DOCX generation deferred to shell/pandoc ----------
# Root controls
state={
 'handoff_version':'v23','authority_date':'2026-07-31','global_p2_status':'CLOSED','p3_plan_status':'V3_ACCEPTED_AFTER_SECOND_AUDIT','p3_execution_started':False,
 'next_pass':'P3A_CONTRACT_AND_PILOT_V3_IMPLEMENTATION','authority_boundary':'GLOBAL_P2_CLOSED; P3 PLAN V3 ACCEPTED; NO CANDIDATE OR CANONICAL J-FAMILY AUTHORITY YET',
 'effective_direct_pair_authorities':19175,'proposition_relation_pairs':658,'provisional_substantive_candidate_edges':657,
 'lineage_participation':dict(part_counts),'administrative_metadata_proposition_pairs':1,
 'governing_section':'45_P3_PLAN_SECOND_ACCEPTANCE_AUDIT_AND_HARDENING'
}
dumpj(ROOT/'00_START_HERE/CURRENT_STATE.json',state)
(ROOT/'00_START_HERE/EXACT_RESUME_POINT.md').write_text('# Exact resume point\n\n`P3A_CONTRACT_AND_PILOT_V3_IMPLEMENTATION`\n\nRead section 45 first. Section 45 Plan v3 supersedes sections 43 and 44 for implementation.\n')
(ROOT/'00_START_HERE/NEXT_CHAT_OPENING_INSTRUCTION.txt').write_text('Open CURRENT_STATE.json and section 45. P2 is closed. Plan v3 is accepted after a second hostile implementation audit. Begin P3A_CONTRACT_AND_PILOT_V3_IMPLEMENTATION from the 19,175 effective pair authorities, 658 proposition relations, the 13,526-lineage participation baseline, and the complete structure/overlay input manifest. Preserve the administrative metadata proposition in a diagnostic lane; do not treat all proposition identity as substantive J-family eligibility. No value harmonization, respondent join, live write, or production execution.\n')
(ROOT/'00_START_HERE/MASTER_HANDOFF.md').write_text(f'''# Rawlsing J-Family Authority Strategy - Master Handoff v23\n\n## Governing state\n\nGlobal P2 is closed. P3 execution has not started. Section 45 contains the accepted Plan v3 and machine contract after a second independent hostile audit.\n\n## Exact next work\n\n`P3A_CONTRACT_AND_PILOT_V3_IMPLEMENTATION`\n\n## Critical counts\n\n- 19,175 effective direct pair authorities\n- 658 proposition relations\n- 657 provisionally substantive candidate edges\n- 1 administrative proposition diagnostic\n- 13,526 lineages: 399 proposition-incident, 2,897 constraint-only, 10,230 with no current direct pair authority\n\nNo candidate or canonical J-family authority, measurement transformation, strata direction, respondent join, database write, live registry installation, or production execution has occurred.\n''')
(ROOT/'00_START_HERE/README_FIRST.md').write_text('# Rawlsing handoff v23\n\nStart with `CURRENT_STATE.json`, the v23 master handoff, and section 45.\n')
(ROOT/'00_START_HERE/SCOPE_LOCK.json').write_text(json.dumps({'handoff_version':'v23','p2':'CLOSED','p3_plan':'V3_GOVERNING','p3_execution':False,'next':'P3A_CONTRACT_AND_PILOT_V3_IMPLEMENTATION','prohibitions':['VALUE_HARMONIZATION','RESPONDENT_JOIN','LIVE_WRITE','AUTOMATIC_CANONICAL_APPROVAL','NEW_DBMS']},indent=2)+'\n')

# Write plan lock README etc already
# Section manifest later after docx generation
# Final authoritative restart controls override inherited duplicates.
master_text='''# Rawlsing J-Family Authority Strategy - Master Handoff v23

## Governing state

Global P2 is closed. P3 execution has not started. Section 45 contains the accepted Plan v3 and machine contract after a second independent hostile audit.

## Exact next work

`P3A_CONTRACT_AND_PILOT_V3_IMPLEMENTATION`

## Critical counts

- 19,175 effective direct pair authorities
- 658 proposition relations
- 657 provisionally substantive candidate edges
- 1 administrative proposition diagnostic
- 13,526 lineages: 399 proposition-incident, 2,897 constraint-only, 10,230 with no current direct pair authority
- P3 closure requires a terminal disposition for all 13,526 lineages and continued reachability of all 18,276 implementations

No candidate or canonical J-family authority, measurement transformation, strata direction, respondent join, database write, live registry installation, or production execution has occurred.
'''
(ROOT/'00_START_HERE/MASTER_HANDOFF.md').write_text(master_text)
(ROOT/'MASTER_HANDOFF.md').write_text(master_text)
readme_text='# Rawlsing handoff v23\n\nStart with `00_START_HERE/CURRENT_STATE.json`, the v23 master handoff, and section 45. Section 45 supersedes sections 43 and 44 for P3 implementation.\n'
(ROOT/'00_START_HERE/README_FIRST.md').write_text(readme_text)
(ROOT/'README_FIRST.md').write_text(readme_text)
sup=ROOT/'00_START_HERE/SUPERSEDED_AND_NON_GOVERNING_ARTIFACTS.csv'
row='Section 44 P3 v2 machine contract,SUPERSEDED_BY_SECTION_45_V3,"Second independent audit found incomplete lineage accounting, one administrative proposition edge inside the connective preflight, residual untyped payloads, incomplete categorical and polymorphic enforcement, and release/DDL validation gaps.",Historical planning and first-audit provenance only; section 45 v3 governs execution.\n'
if 'SUPERSEDED_BY_SECTION_45_V3' not in sup.read_text():
    with sup.open('a',encoding='utf-8') as f:f.write(row)
