from __future__ import annotations
import csv, json, os, re, shutil, hashlib, pathlib, textwrap, yaml, subprocess
from collections import defaultdict
from copy import deepcopy

SELF_SOURCE_BYTES=pathlib.Path(__file__).read_bytes()

SRCROOT=pathlib.Path('/mnt/data/v24_review/extracted/Rawlsing_J_Family_Authority_Strategy_Handoff_v23_20260731')
ROOT=pathlib.Path('/mnt/data/rawlsing_v24_build/Rawlsing_J_Family_Authority_Strategy_Handoff_v24_20260731')
S45=SRCROOT/'45_P3_PLAN_SECOND_ACCEPTANCE_AUDIT_AND_HARDENING'
# Rebuild the cumulative v24 tree from the accepted v23 extraction on every run.
# This prevents hidden dependence on a previously prepared build directory.
if ROOT.exists(): shutil.rmtree(ROOT)
shutil.copytree(SRCROOT,ROOT)
S46=ROOT/'46_P3_PLAN_THIRD_BOUNDED_IMPLEMENTATION_READINESS_LOCK'
if S46.exists(): shutil.rmtree(S46)
S46.mkdir(parents=True)
for d in ['adjudication','algorithms','downstream','release','schemas','sql','upstream','validation']:
    (S46/d).mkdir()

def sha(p):
    h=hashlib.sha256();
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True,exist_ok=True)
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def read_csv(path):
    with open(path,newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))

# Copy all governing v3 inputs first, renaming v3 to v4 where sensible.
for p in S45.rglob('*'):
    if not p.is_file(): continue
    rel=p.relative_to(S45)
    if rel.parts[0]=='validation' and rel.name in {'build_handoff_v23.py','verify_handoff_v23.py'}: continue
    if p.suffix=='.docx': continue
    newparts=[x.replace('_v3','_v4').replace('v3.','v4.') for x in rel.parts]
    dst=S46.joinpath(*newparts)
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(p,dst)

# Global text replacement for copied text contracts, but preserve historical references in reports later by replacing only governing version tokens.
for p in S46.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.md','.yaml','.yml','.sql','.json','.csv','.txt','.py'}:
        try: txt=p.read_text(encoding='utf-8')
        except UnicodeDecodeError: continue
        txt=txt.replace('/p3/v3/','/p3/v4/').replace('_v3.csv','_v4.csv').replace('_v3.json','_v4.json').replace('_v3.sql','_v4.sql').replace('_v3.md','_v4.md')
        txt=txt.replace('Plan v3','Plan v4').replace('plan v3','plan v4').replace('PLAN_V3','PLAN_V4')
        p.write_text(txt,encoding='utf-8')

# Remove historical/validation outputs copied from v23; section 46 will own fresh ones.
for name in ['FINAL_RELEASE_GATE_RETURN_v23.json','V23_CUMULATIVE_VERIFIER_RETURN.json','V23_TYPE_AWARE_AND_RECURSIVE_ARCHIVE_AUDIT_RETURN.json','P3_DOCUMENT_QA_RETURN_v4.json','PLAN_V3_A11Y_AUDIT.json','MASTER_V23_A11Y_AUDIT.json','AUDIT_REPORT_A11Y_AUDIT.json','INHERITED_V22_PAYLOAD_HASHES.csv','V22_BASELINE_REVERIFICATION_RETURN.json']:
    for p in S46.rglob(name): p.unlink(missing_ok=True)
# remove fake migration skeleton and stale report/task docs to regenerate
for p in list(S46.rglob('*SKELETON*')): p.unlink()
for name in ['P3_PLAN_SECOND_ACCEPTANCE_AUDIT_AND_HARDENING_REPORT.md','TASK_RETURN.md','README_FIRST.md','ASSEMBLY_PROVENANCE_v23.md','SUPERSEDES_SECTION_44.md','SECTION_MANIFEST.csv']:
    (S46/name).unlink(missing_ok=True)

# ---------- Controlled vocabularies v4 ----------
voc=read_csv(S45/'P3_CONTROLLED_VOCABULARIES_v3.csv')
# Object type must contain only registry-backed objects, not associative rows.
remove_obj={'COLLISION_AUTHORITY_SOURCE','PAIR_FACT_EVIDENCE','PAIR_FACT_SOURCE_AUTHORITY','SIGNATURE_FIELD_EVIDENCE'}
voc=[r for r in voc if not (r['vocabulary_domain']=='object_type' and r['code'] in remove_obj)]
# Add lifecycle/enforcement domains needed by executable contract.
adds={
'delivery_state':[
 ('DELIVERED_CONTRACT','Delivered contract','Present in the governing plan section.'),
 ('DELIVERED_INPUT_AUDIT','Delivered input audit','Present, read-only, and reproducible from upstream authority.'),
 ('GENERATED_DURING_P3A','Generated during P3A','Must be emitted by P3A before phase close.'),
 ('GENERATED_DURING_P3B','Generated during P3B','Must be emitted during global adjudication.'),
 ('GENERATED_DURING_P3C','Generated during P3C','Must be emitted for closure/release.'),
 ('GENERATED_DURING_P6','Generated during P6','Requires a user-designated live target.'),
],
'enforcement_mechanism':[
 ('DDL_CHECK','DDL check constraint'),('VOCAB_TRIGGER','Vocabulary trigger'),('OBJECT_TYPE_TRIGGER','Object-type trigger'),
 ('APPEND_ONLY_TRIGGER','Append-only trigger'),('LIFECYCLE_TRIGGER','Lifecycle transition trigger'),
 ('PROMOTION_TRIGGER','Promotion-pointer trigger'),('VALIDATION_QUERY','Read-only validation query'),('FILE_VALIDATOR','File/build validator')
],
'hyperedge_participant_role':[
 ('PARENT_PROMPT','Parent prompt'),('CHILD_FAMILY','Child proposition family'),('SOURCE_STRUCTURE','Source structure'),
 ('LEFT_STRUCTURE','Left source structure'),('RIGHT_STRUCTURE','Right source structure'),('MEMBER_MAPPING','Adjudicated member mapping'),
 ('DERIVED_INDEX','Derived index'),('CONSTITUENT_ITEM','Constituent item'),('SIBLING_FAMILY','Sibling proposition family'),
 ('BROADER_TARGET','Broader target/family'),('NARROWER_TARGET','Narrower target/family'),('RESPONSE_CONTRACT','Response contract'),
 ('FAMILY_VARIANT','Family variant'),('CONSTRUCT_COORDINATE','Construct coordinate')
],
}
existing={(r['vocabulary_domain'],r['code']) for r in voc}
for dom, vals in adds.items():
    for item in vals:
        if len(item)==2:
            code,label=item; definition=label
        else:
            code,label,definition=item
        if (dom,code) not in existing:
            voc.append({'vocabulary_domain':dom,'code':code,'label':label,'definition':definition,'authority_effect':'CONTRACT_ONLY','terminal':'NO','deprecated':'NO'})
voc=sorted(voc,key=lambda r:(r['vocabulary_domain'],r['code']))
write_csv(S46/'P3_CONTROLLED_VOCABULARIES_v4.csv',voc,['vocabulary_domain','code','label','definition','authority_effect','terminal','deprecated'])

# ---------- Complete identity specification ----------
identity_rows=[
('IMPORTED_IMPLEMENTATION','INHERITED_UPSTREAM_ID','implementation_id','Use exact P2 implementation ID; never reallocate.','UPSTREAM_EXACT'),
('IMPORTED_SOURCE_LOCAL_LINEAGE','INHERITED_UPSTREAM_ID','lineage_id','Use exact P2 lineage ID; never reallocate.','UPSTREAM_EXACT'),
('IMPORTED_SOURCE_STRUCTURE','INHERITED_UPSTREAM_ID','source_structure_id','Use exact governed P2 structure ID.','UPSTREAM_EXACT'),
('IMPORTED_RESPONSE_CONTRACT','INHERITED_UPSTREAM_ID','upstream_response_contract_id','Use exact upstream response-contract identity where available.','UPSTREAM_EXACT'),
('LINEAGE_SEGMENT','CONTENT_ADDRESSED_DERIVED_ID','parent_lineage_id + sorted implementation_ids + segment_reason','Canonical JSON SHA-256; display prefix P3SEG plus first 16 hex; collision check uses full hash.','P3SEG-[0-9a-f]{16}'),
('PROPOSITION_SIGNATURE','CONTENT_ADDRESSED_DERIVED_ID','subject_id + 12 ordered signature fields + evidence states + evidence ids + schema version','Canonical JSON SHA-256; P3SIG plus first 16 hex.','P3SIG-[0-9a-f]{16}'),
('RESPONSE_CONTRACT_REFERENCE','CONTENT_ADDRESSED_DERIVED_ID','subject_id + upstream_response_contract_id + response_topology + authority artifact/hash','Canonical JSON SHA-256; P3RCR plus first 16 hex.','P3RCR-[0-9a-f]{16}'),
('STRUCTURAL_CONTEXT_REFERENCE','CONTENT_ADDRESSED_DERIVED_ID','subject_id + source_field + canonical source_value + authority artifact','Canonical JSON SHA-256; P3SCR plus first 16 hex.','P3SCR-[0-9a-f]{16}'),
('PAIR_FACT','CONTENT_ADDRESSED_DERIVED_ID','canonical endpoint pair + governing authority id + mapping version','Canonical JSON SHA-256; P3PF plus first 16 hex.','P3PF-[0-9a-f]{16}'),
('COLLISION','CONTENT_ADDRESSED_DERIVED_ID','oriented endpoints + collision type + scope + source authority ids','Canonical JSON SHA-256; P3COL plus first 16 hex.','P3COL-[0-9a-f]{16}'),
('CANDIDATE_COMPONENT','CONTENT_ADDRESSED_DERIVED_ID','sorted member ids + sorted connectivity pair facts + build rule version','Canonical JSON SHA-256; P3COMP plus first 16 hex.','P3COMP-[0-9a-f]{16}'),
('CLOSURE_OBLIGATION','CONTENT_ADDRESSED_DERIVED_ID','candidate revision + canonical endpoint pair + obligation type','Canonical JSON SHA-256; P3CLOSE plus first 16 hex.','P3CLOSE-[0-9a-f]{16}'),
('HYPEREDGE','CONTENT_ADDRESSED_DERIVED_ID','hyperedge type + authority effect + sorted typed participants + governing evidence','Canonical JSON SHA-256; P3HYP plus first 16 hex.','P3HYP-[0-9a-f]{16}'),
('DEPENDENCY','CONTENT_ADDRESSED_DERIVED_ID','dependent id + authority input id + dependency role + authority release','Canonical JSON SHA-256; P3DEP plus first 16 hex.','P3DEP-[0-9a-f]{16}'),
('CANDIDATE_PACKET','CONTENT_ADDRESSED_DERIVED_ID','candidate revision id + evidence bundle hash + packet schema version','Canonical JSON SHA-256; P3PKT plus first 16 hex.','P3PKT-[0-9a-f]{16}'),
('CANDIDATE_FAMILY','REGISTRY_ALLOCATED_DURABLE_ID','initial component identity + candidate origin type','Deterministic initial sorted allocation; append-only thereafter.','P3CAND-[0-9]{6}'),
('CANDIDATE_REVISION','REGISTRY_ALLOCATED_DURABLE_ID','candidate family id + revision ordinal','Immutable revision identity; revisions append and never overwrite.','P3CANDREV-[0-9]{6}-R[0-9]{4}'),
('FAMILY_VARIANT','REGISTRY_ALLOCATED_DURABLE_ID','owner stable id + dimension + stable semantic value key','Append-only durable variant identity.','P3VAR-[0-9]{6}'),
('FAMILY_VARIANT_REVISION','REGISTRY_ALLOCATED_DURABLE_ID','variant id + revision ordinal','Immutable release-scoped variant revision.','P3VARREV-[0-9]{6}-R[0-9]{4}'),
('FAMILY_EXCLUSION','REGISTRY_ALLOCATED_DURABLE_ID','owner stable id + exclusion type + prohibited operation + stable rule key','Append-only durable exclusion identity.','P3EXC-[0-9]{6}'),
('ADJUDICATION','REGISTRY_ALLOCATED_DURABLE_ID','candidate revision id + decision ordinal','Append-only immutable decision.','P3ADJ-[0-9]{6}'),
('CANONICAL_FAMILY','REGISTRY_ALLOCATED_DURABLE_ID','accepting adjudication id','Allocate new JFAM identity; revisions never change stable family id.','JFAM-[0-9]{6}'),
('CANONICAL_FAMILY_REVISION','REGISTRY_ALLOCATED_DURABLE_ID','canonical family id + revision ordinal','Immutable revision identity.','JFAMREV-[0-9]{6}-R[0-9]{4}'),
('DOCTRINE_DELTA','REGISTRY_ALLOCATED_DURABLE_ID','trigger candidate + doctrine ordinal','Append-only doctrine record.','P3DOC-[0-9]{5}'),
('FAMILY_GENEALOGY','REGISTRY_ALLOCATED_DURABLE_ID','adjudication id + relation type + predecessor/successor set','Append-only genealogy event.','P3GEN-[0-9]{6}'),
]
write_csv(S46/'P3_IDENTITY_KEY_SPEC_v4.csv',[
 {'object_type':a,'identity_strategy':b,'idempotency_key':c,'allocation_rule':d,'id_pattern':e} for a,b,c,d,e in identity_rows
],['object_type','identity_strategy','idempotency_key','allocation_rule','id_pattern'])

# ---------- Expanded object reference contract ----------
objrefs=[
('p3_lineage_segment','parent_lineage_id','IMPORTED_SOURCE_LOCAL_LINEAGE','YES'),
('p3_lineage_segment_member','implementation_id','IMPORTED_IMPLEMENTATION','YES'),
('p3_lineage_disposition','subject_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
('p3_proposition_signature','subject_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
('p3_response_contract_reference','subject_id','IMPORTED_IMPLEMENTATION|IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
('p3_structural_context_reference','subject_id','IMPORTED_IMPLEMENTATION|IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT|CANDIDATE_FAMILY|CANONICAL_FAMILY|FAMILY_VARIANT','YES'),
('p3_pair_fact_bundle','left_object_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
('p3_pair_fact_bundle','right_object_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
('p3_collision_scope_registry','left_object_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
('p3_collision_scope_registry','right_object_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
('p3_component_membership','member_object_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
('p3_candidate_membership','member_object_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
('p3_internal_pair_matrix','left_object_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
('p3_internal_pair_matrix','right_object_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
('p3_closure_obligation','left_object_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
('p3_closure_obligation','right_object_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
('p3_family_variant','owner_object_id','CANDIDATE_FAMILY|CANONICAL_FAMILY','YES'),
('p3_variant_membership','member_object_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
('p3_family_exclusion','owner_object_id','CANDIDATE_FAMILY|CANONICAL_FAMILY','YES'),
('p3_excluded_object','excluded_object_id','IMPORTED_IMPLEMENTATION|IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
('p3_adjudication_member','member_object_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
('p3_adjudication_hierarchy_relation','broader_object_id','CANDIDATE_FAMILY|CANONICAL_FAMILY','YES'),
('p3_adjudication_hierarchy_relation','narrower_object_id','CANDIDATE_FAMILY|CANONICAL_FAMILY','YES'),
('p3_canonical_family_membership','member_object_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
]
write_csv(S46/'P3_OBJECT_REFERENCE_TYPE_CONTRACT_v4.csv',[
 {'table_name':a,'column_name':b,'allowed_object_types':c,'required':d} for a,b,c,d in objrefs
],['table_name','column_name','allowed_object_types','required'])

# ---------- Hyperedge role/type contract ----------
hr=[]
def addh(ht,role,types,minc,maxc,effect):
    hr.append({'hyperedge_type':ht,'participant_role':role,'allowed_object_types':types,'minimum_count':minc,'maximum_count':maxc,'authority_effect_ceiling':effect})
addh('BATTERY','PARENT_PROMPT','IMPORTED_SOURCE_STRUCTURE|IMPORTED_SOURCE_LOCAL_LINEAGE',1,1,'STRUCTURAL_SUPPORT')
addh('BATTERY','CHILD_FAMILY','CANDIDATE_FAMILY|CANONICAL_FAMILY',1,'UNBOUNDED','STRUCTURAL_SUPPORT')
addh('BATTERY','SOURCE_STRUCTURE','IMPORTED_SOURCE_STRUCTURE',1,'UNBOUNDED','STRUCTURAL_SUPPORT')
addh('CROSS_SOURCE_BATTERY_ANALOGY','LEFT_STRUCTURE','IMPORTED_SOURCE_STRUCTURE',1,1,'STRUCTURAL_SUPPORT')
addh('CROSS_SOURCE_BATTERY_ANALOGY','RIGHT_STRUCTURE','IMPORTED_SOURCE_STRUCTURE',1,1,'STRUCTURAL_SUPPORT')
addh('CROSS_SOURCE_BATTERY_ANALOGY','MEMBER_MAPPING','PAIR_FACT',1,'UNBOUNDED','STRUCTURAL_SUPPORT')
addh('DERIVED_INDEX_CONSTITUTION','DERIVED_INDEX','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT',1,1,'CONSTITUTION')
addh('DERIVED_INDEX_CONSTITUTION','CONSTITUENT_ITEM','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT',1,'UNBOUNDED','CONSTITUTION')
addh('SIBLING_FAMILY_CONSTRUCT','SIBLING_FAMILY','CANDIDATE_FAMILY|CANONICAL_FAMILY',2,'UNBOUNDED','NO_FAMILY_MEMBERSHIP_AUTHORITY')
addh('SIBLING_FAMILY_CONSTRUCT','CONSTRUCT_COORDINATE','PROPOSITION_SIGNATURE',1,1,'DISCOVERY_CONTEXT')
addh('TARGET_HIERARCHY','BROADER_TARGET','CANDIDATE_FAMILY|CANONICAL_FAMILY',1,1,'HIERARCHY')
addh('TARGET_HIERARCHY','NARROWER_TARGET','CANDIDATE_FAMILY|CANONICAL_FAMILY',1,'UNBOUNDED','HIERARCHY')
addh('RESPONSE_CONTRACT_CLASS','RESPONSE_CONTRACT','IMPORTED_RESPONSE_CONTRACT|RESPONSE_CONTRACT_REFERENCE',1,'UNBOUNDED','VARIANT_ORGANIZATION')
addh('RESPONSE_CONTRACT_CLASS','FAMILY_VARIANT','FAMILY_VARIANT',1,'UNBOUNDED','VARIANT_ORGANIZATION')
write_csv(S46/'P3_HYPEREDGE_ROLE_TYPE_CONTRACT_v4.csv',hr,['hyperedge_type','participant_role','allowed_object_types','minimum_count','maximum_count','authority_effect_ceiling'])

# ---------- Artifact catalog v4 with explicit delivery state ----------
oldcat=read_csv(S45/'P3_ARTIFACT_CATALOG_v3.csv')
pathfix={
'upstream/P3_UPSTREAM_AUTHORITY_PRECEDENCE.csv':'upstream/P3_UPSTREAM_AUTHORITY_PRECEDENCE_v4.csv',
'upstream/P3_P2_TO_P3_AUTHORITY_MAPPING.csv':'upstream/P3_P2_TO_P3_AUTHORITY_MAPPING_v4.csv',
'upstream/P3_EFFECTIVE_UPSTREAM_PAIR_AUTHORITY_SURFACE.csv':'upstream/P3_EFFECTIVE_UPSTREAM_PAIR_AUTHORITY_SURFACE_v4.csv',
'p3_object_id_registry.csv':'p3_object_registry.csv',
'P3_PLAN_ACCEPTANCE_AUDIT_AND_CORRECTION_REPORT.md':'P3_PLAN_THIRD_BOUNDED_IMPLEMENTATION_READINESS_AUDIT.md',
'validation/verify_handoff_v23.py':'validation/verify_handoff_v24.py',
'validation/build_handoff_v23.py':'validation/build_handoff_v24.py',
'validation/INHERITED_V22_PAYLOAD_HASHES.csv':'validation/INHERITED_V23_PAYLOAD_HASHES.csv',
'sql/P3_SHADOW_MIGRATION_SKELETON_v3.sql':'release/P3_LIVE_INSTALLATION_BLOCKING_CONTRACT_v4.json',
}
cat=[]
actual_delivered=set()
# governing contracts and input audits that are in section 46
for p in S46.rglob('*'):
    if p.is_file(): actual_delivered.add(str(p.relative_to(S46)))
for r in oldcat:
    a=pathfix.get(r['artifact'],r['artifact'].replace('_v3','_v4').replace('v3.','v4.'))
    phase=r['first_phase']
    if a in actual_delivered or a.startswith(('P3_','sql/','upstream/','schemas/','adjudication/','algorithms/','downstream/','release/','validation/')) and a in actual_delivered:
        ds='DELIVERED_CONTRACT' if not a.startswith('upstream/') else 'DELIVERED_INPUT_AUDIT'
    elif 'P3A' in phase or phase=='ALL': ds='GENERATED_DURING_P3A'
    elif 'P3B' in phase: ds='GENERATED_DURING_P3B'
    elif 'P3C' in phase: ds='GENERATED_DURING_P3C'
    elif 'P6' in phase: ds='GENERATED_DURING_P6'
    else: ds='GENERATED_DURING_P3A'
    cat.append({**r,'artifact':a,'delivery_state':ds,'governing_contract':'DDL_OR_JSON_SCHEMA_OR_EXPLICIT_ARTIFACT_SPEC'})
# add missing bounded contracts
for a,cl,fn,ph,req,ds in [
('P3_HYPEREDGE_ROLE_TYPE_CONTRACT_v4.csv','CANONICAL_CONTRACT','Binds each hyperedge role to allowed participant types and cardinality','P3A','YES','DELIVERED_CONTRACT'),
('P3_DATABASE_ENFORCEMENT_CONTRACT_v4.csv','CANONICAL_CONTRACT','Enumerates database constraints/triggers that must exist before shadow installation','P3A/P6','YES','DELIVERED_CONTRACT'),
('P3_RELEASE_LIFECYCLE_STATE_MACHINE_v4.csv','CANONICAL_CONTRACT','Release status transitions and guards','P3A/P6','YES','DELIVERED_CONTRACT'),
('release/P3_LIVE_INSTALLATION_BLOCKING_CONTRACT_v4.json','INSTALLATION_BOUNDARY','Exact live inputs required before executable migration may be compiled','P3C/P6','YES','DELIVERED_CONTRACT'),
]:
    if not any(x['artifact']==a for x in cat):
        cat.append({'artifact':a,'class':cl,'function':fn,'first_phase':ph,'required_for_phase_close':req,'delivery_state':ds,'governing_contract':'EXPLICIT_CONTRACT'})
cat=sorted(cat,key=lambda r:r['artifact'])
write_csv(S46/'P3_ARTIFACT_CATALOG_v4.csv',cat,['artifact','class','function','first_phase','required_for_phase_close','delivery_state','governing_contract'])

# ---------- Release lifecycle ----------
rel_life=[
 {'from_status':'','to_status':'DRAFT','allowed':'YES','guard':'First release event only; event_ordinal=1.'},
 {'from_status':'DRAFT','to_status':'VALIDATED','allowed':'YES','guard':'All pre-shadow release validation gates pass.'},
 {'from_status':'VALIDATED','to_status':'SHADOW','allowed':'YES','guard':'Shadow schema load succeeds and comparison run begins.'},
 {'from_status':'SHADOW','to_status':'PROMOTED','allowed':'YES','guard':'All shadow comparison and promotion gates pass.'},
 {'from_status':'SHADOW','to_status':'ROLLED_BACK','allowed':'YES','guard':'Shadow failure or explicit rejection; current pointer unchanged.'},
 {'from_status':'PROMOTED','to_status':'SUPERSEDED','allowed':'YES','guard':'A successor release is promoted transactionally.'},
 {'from_status':'PROMOTED','to_status':'ROLLED_BACK','allowed':'YES','guard':'Emergency rollback restores prior promoted release and records evidence.'},
]
write_csv(S46/'P3_RELEASE_LIFECYCLE_STATE_MACHINE_v4.csv',rel_life,['from_status','to_status','allowed','guard'])

# ---------- Database enforcement contract ----------
enf=[
('VOCABULARY_CODES','p3_categorical_field_binding','VOCAB_TRIGGER','Every finite categorical column rejects codes absent from the loaded release contract.'),
('OBJECT_REFERENCE_TYPES','p3_object_reference_type_contract','OBJECT_TYPE_TRIGGER','Every polymorphic object reference resolves to an allowed p3_object_registry.object_type.'),
('HYPEREDGE_ROLE_TYPES','p3_hyperedge_role_type_contract','OBJECT_TYPE_TRIGGER','Hyperedge type/role/cardinality/authority-effect combinations must close exactly.'),
('IDENTITY_STRATEGY','p3_identity_key_contract','OBJECT_TYPE_TRIGGER','Every registry object uses the identity strategy and ID pattern assigned to its object type.'),
('CANDIDATE_LIFECYCLE','p3_candidate_lifecycle_transition','LIFECYCLE_TRIGGER','Candidate events are contiguous and follow the governing transition table.'),
('RELEASE_LIFECYCLE','p3_release_lifecycle_transition','LIFECYCLE_TRIGGER','Release events are contiguous and follow the governing transition table.'),
('PROMOTION_POINTER','p3_runtime_promotion_pointer','PROMOTION_TRIGGER','Pointer may target only a release whose latest event is PROMOTED.'),
('APPEND_ONLY_DECISIONS','p3_adjudication_decision|p3_adjudication_member|p3_adjudication_collision_disposition|p3_adjudication_hierarchy_relation','APPEND_ONLY_TRIGGER','Final decisions and their structured children reject UPDATE and DELETE.'),
('APPEND_ONLY_EVENTS','p3_release_status_event|p3_candidate_status_event|p3_doctrine_delta|p3_family_genealogy','APPEND_ONLY_TRIGGER','Historical authority events reject UPDATE and DELETE.'),
('NO_AUTHORITY_LEAK','p3_family_variant_revision|p3_response_contract_reference|p3_structural_context_reference|p3_hyperedge','DDL_CHECK','P3 cannot authorize value portability, P5 authority, causal authority, or runtime substitution.'),
('PAIR_ENDPOINT_ORDER','p3_pair_fact_bundle|p3_collision_scope_registry|p3_internal_pair_matrix|p3_closure_obligation','DDL_CHECK','Symmetric/unordered pairs use canonical endpoint order; directional roles remain explicit.'),
('STATUS_SPECIFIC_ADJUDICATION','p3_adjudication_decision','DDL_CHECK','Accepted, split, hierarchy, blocked, insufficient, and rejected decisions require mutually appropriate fields.'),
]
write_csv(S46/'P3_DATABASE_ENFORCEMENT_CONTRACT_v4.csv',[
 {'contract_id':a,'applies_to':b,'mechanism':c,'requirement':d,'phase':'P3A_STATIC_AND_P6_EXECUTION'} for a,b,c,d in enf
],['contract_id','applies_to','mechanism','requirement','phase'])

# ---------- Fix schemas and promote to v4 ----------
schema_dir=S46/'schemas'
# update all $id/$ref v4 already done; helper pattern map
patterns={r'^P3PF-[0-9]{8}$':r'^P3PF-[0-9a-f]{16}$',r'^P3CLOSE-[0-9]{8}$':r'^P3CLOSE-[0-9a-f]{16}$',r'^P3SEG-[0-9]{6}$':r'^P3SEG-[0-9a-f]{16}$',r'^P3COL-[0-9]{8}$':r'^P3COL-[0-9a-f]{16}$',r'^P3DEP-[0-9]{8}$':r'^P3DEP-[0-9a-f]{16}$',r'^P3PKT-[0-9]{6}$':r'^P3PKT-[0-9a-f]{16}$',r'^P3CANDREV-[0-9]{8}$':r'^P3CANDREV-[0-9]{6}-R[0-9]{4}$',r'^P3VAR-[0-9]{6}$':r'^P3VAR-[0-9]{6}$',r'^JFAMREV-[0-9]{8}$':r'^JFAMREV-[0-9]{6}-R[0-9]{4}$'}
def rec_fix(x):
    if isinstance(x,dict):
        for k,v in list(x.items()):
            if k=='pattern' and v in patterns: x[k]=patterns[v]
            else: rec_fix(v)
    elif isinstance(x,list):
        for v in x: rec_fix(v)
for p in schema_dir.glob('*.json'):
    s=json.loads(p.read_text())
    rec_fix(s)
    # authority release IDs should never be blank
    def add_min(o):
        if isinstance(o,dict):
            props=o.get('properties',{})
            for k,v in props.items():
                if k.endswith('_id') and isinstance(v,dict) and v.get('type')=='string' and 'pattern' not in v: v.setdefault('minLength',1)
                add_min(v)
            for v in o.values():
                if v is not props: add_min(v)
        elif isinstance(o,list):
            for v in o:add_min(v)
    add_min(s)
    p.write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n')
# Specific schema repairs
p=schema_dir/'closure_obligation.schema.json'; s=json.loads(p.read_text())
s['properties']['obligation_type']={'enum':['ATTACHMENT_REVIEW','DIRECT_COLLISION','HETEROGENEOUS_LINEAGE','INCOMPLETE_SIGNATURE','MERGE_OR_SIBLING_REVIEW','SIGNATURE_CONFLICT','UNRESOLVED_PAIR','UNRULED_INTERNAL_PAIR','VALUE_PORTABILITY_BOUNDARY']}
s['allOf']=[
 {'if':{'properties':{'status':{'enum':['RESOLVED_ACCEPT','RESOLVED_SPLIT','RESOLVED_EXCLUDE']}},'required':['status']},'then':{'required':['resolution_adjudication_id'],'properties':{'resolution_adjudication_id':{'type':'string','pattern':'^P3ADJ-[0-9]{6}$'}}}},
 {'if':{'properties':{'status':{'enum':['OPEN','FAIL_CLOSED']}},'required':['status']},'then':{'properties':{'resolution_adjudication_id':{'type':'null'}}}}
]
p.write_text(json.dumps(s,indent=2)+'\n')
p=schema_dir/'candidate_family.schema.json'; s=json.loads(p.read_text())
ip=s['properties']['internal_pair_counts'];
if 'direct_unresolved' not in ip['properties']:
    ip['properties']['direct_unresolved']={'type':'integer','minimum':0}
    idx=ip['required'].index('direct_collision')+1; ip['required'].insert(idx,'direct_unresolved')
p.write_text(json.dumps(s,indent=2)+'\n')
p=schema_dir/'candidate_component.schema.json'; s=json.loads(p.read_text()); s['properties']['connectivity_pair_fact_ids']['items']['pattern']='^P3PF-[0-9a-f]{16}$';p.write_text(json.dumps(s,indent=2)+'\n')
p=schema_dir/'pair_fact_bundle.schema.json'; s=json.loads(p.read_text()); s['properties']['pair_fact_id']['pattern']='^P3PF-[0-9a-f]{16}$';p.write_text(json.dumps(s,indent=2)+'\n')
p=schema_dir/'candidate_packet.schema.json'; s=json.loads(p.read_text()); s['properties']['packet_id']['pattern']='^P3PKT-[0-9a-f]{16}$';p.write_text(json.dumps(s,indent=2)+'\n')
p=schema_dir/'lineage_segment.schema.json'; s=json.loads(p.read_text()); s['properties']['segment_id']['pattern']='^P3SEG-[0-9a-f]{16}$'; s['properties']['implementation_ids']['items']['minLength']=1;p.write_text(json.dumps(s,indent=2)+'\n')
p=schema_dir/'dependency_record.schema.json'; s=json.loads(p.read_text()); s['properties']['dependency_id']['pattern']='^P3DEP-[0-9a-f]{16}$';p.write_text(json.dumps(s,indent=2)+'\n')
p=schema_dir/'collision_scope.schema.json'; s=json.loads(p.read_text()); s['properties']['collision_id']['pattern']='^P3COL-[0-9a-f]{16}$';p.write_text(json.dumps(s,indent=2)+'\n')
p=schema_dir/'collision_disposition.schema.json'; s=json.loads(p.read_text()); s['properties']['collision_id']['pattern']='^P3COL-[0-9a-f]{16}$';p.write_text(json.dumps(s,indent=2)+'\n')
p=schema_dir/'canonical_family_revision.schema.json'; s=json.loads(p.read_text()); s['properties']['family_revision_id']['pattern']='^JFAMREV-[0-9]{6}-R[0-9]{4}$';p.write_text(json.dumps(s,indent=2)+'\n')
# candidate variant may be stable variant; no change; variant assignment references stable variant.

# Rebuild schema registry later after all schemas fixed.

# ---------- Correct plan markdown ----------
oldplan=(S45/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v3_20260731.md').read_text()
plan=oldplan.replace('Implementation Plan v3','Implementation Plan v4').replace('PLAN_V3','PLAN_V4').replace('**Plan version:** v3','**Plan version:** v4')
plan=plan.replace('`P3A_CONTRACT_AND_PILOT_V3_IMPLEMENTATION`','`P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION`')
plan=plan.replace('Every accepted family requires two exclusion layers.','Every accepted family requires a rule-based exclusion layer. A named-exclusion layer is additionally required whenever actual rejected near-neighbors exist.')
plan=plan.replace('Every accepted family requires named and rule-based exclusions.','Every accepted family requires rule-based exclusions; named exclusions are required when actual rejected near-neighbors exist.')
plan=plan.replace('every accepted family has named and rule-based exclusions','every accepted family has rule-based exclusions and, when actual rejected near-neighbors exist, named exclusions')
plan=plan.replace('every family revision has members, variants, exclusions, and evidence hash','every family revision has members, exclusions, and evidence hash; variants are required only when governed variation exists')
plan=plan.replace('freeze and hash v20 P2 inputs;','freeze and hash the v20 P2 authority inputs as preserved and audited in the cumulative v24 handoff;')
plan=plan.replace('Section 45 and Plan v3 supersede the v22 machine contract. Sections 43 and 44 remain historical provenance.','Section 46 and Plan v4 supersede sections 43-45 for implementation. Sections 43-45 remain historical provenance.')
plan=plan.replace('P3A must use only the v3 contracts in section 45.','P3A must use only the v4 contracts in section 46.')
# Insert bounded third audit additions before final next-point block.
append='''\n\n# 42. Third bounded implementation-readiness lock\n\nThe third review did not add a new ontology or database layer. It closed unfinished enforcement and identity surfaces that would otherwise have forced redesign during P3A or P6.\n\n## 42.1 Delivered versus future artifacts\n\n`P3_ARTIFACT_CATALOG_v4.csv` now distinguishes delivered contracts and input audits from artifacts that P3A, P3B, P3C, or P6 must generate. A future output is never represented as though it already exists. Every delivered path must exist exactly; every future path must name its producing phase and governing contract.\n\n## 42.2 Complete identity doctrine\n\nEvery registry-backed P3 object type now has exactly one identity strategy, an idempotency key, an allocation rule, and an ID pattern. Associative evidence rows are no longer misclassified as registry objects. Content-addressed IDs use full SHA-256 collision checks and a 16-hex display suffix. Durable candidate, family, variant, decision, doctrine, and genealogy IDs remain append-only; their immutable revisions have explicit ordinal identities.\n\n## 42.3 Enforceable reference and hyperedge contracts\n\nEvery polymorphic lineage/segment/member/owner reference used by P3 has an allowed object-type contract. Hyperedges additionally have type-specific participant roles, allowed object types, minimum and maximum cardinalities, and authority-effect ceilings. A free-form hyperedge member cannot enter authority.\n\n## 42.4 Database enforcement boundary\n\nThe former non-executable migration skeleton is removed. The logical DDL now defines the contract tables and enforcement functions needed for vocabulary codes, object-reference types, identity strategies, append-only history, lifecycle transitions, and promotion pointers. `P3_LIVE_INSTALLATION_BLOCKING_CONTRACT_v4.json` states the exact live-target facts that are still unavailable. An executable migration cannot be compiled or claimed until those facts are supplied in P3C/P6. This is an explicit blocked boundary, not a scaffold presented as finished code.\n\n## 42.5 Schema and packet closure\n\nThe connected schema system now aligns content-addressed ID patterns with the identity doctrine, constrains closure-obligation types, requires resolution adjudications only for resolved obligations, and includes `DIRECT_UNRESOLVED` in candidate internal-pair counts. The file validator must prove that all seven internal-pair states sum to the expected n(n-1)/2 count.\n\n## 42.6 Final stop rule\n\nPlan v4 is frozen after this bounded readiness pass. The architecture may be reopened only when P3A execution produces a concrete contradiction, a failed invariant, or an upstream/downstream artifact that cannot be represented under the delivered contract. New conveniences, speculative services, visual systems, or alternate databases are not grounds for expansion.\n'''
# Insert before final explicit v3 appendix if possible; just append then final next point.
plan += append
plan += '\n\n# 43. Exact next execution point\n\n`P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION`\n'
(S46/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v4_20260731.md').write_text(plan)

# Repair inherited header/footer labels after DOCX generation.
from docx import Document as _DocxDocument
def _replace_header_footer_labels(path, replacements):
    _doc=_DocxDocument(path)
    for _section in _doc.sections:
        for _container in [_section.header,_section.first_page_header,_section.even_page_header,_section.footer,_section.first_page_footer,_section.even_page_footer]:
            for _p in _container.paragraphs:
                for _r in _p.runs:
                    for _a,_z in replacements.items():
                        if _a in _r.text:
                            _r.text=_r.text.replace(_a,_z)
    _doc.save(path)


from docx.oxml import OxmlElement as _OxmlElement
from docx.oxml.ns import qn as _qn
def _ensure_page_field(path):
    _doc=_DocxDocument(path)
    for _section in _doc.sections:
        _par=_section.footer.paragraphs[0]
        # Remove inherited PAGE fields so the result is deterministic.
        for _child in list(_par._p):
            if _child.tag==_qn('w:fldSimple'):
                _par._p.remove(_child)
        _fld=_OxmlElement('w:fldSimple'); _fld.set(_qn('w:instr'),'PAGE')
        _r=_OxmlElement('w:r'); _rpr=_OxmlElement('w:rPr')
        _color=_OxmlElement('w:color'); _color.set(_qn('w:val'),'64748B')
        _sz=_OxmlElement('w:sz'); _sz.set(_qn('w:val'),'16')
        _rpr.append(_color); _rpr.append(_sz); _r.append(_rpr)
        _t=_OxmlElement('w:t'); _t.text='1'; _r.append(_t); _fld.append(_r); _par._p.append(_fld)
    _doc.save(path)

# ---------- Correct algorithms ----------
alg=(S45/'algorithms/P3_ALGORITHMS_AND_PSEUDOCODE_v3.md').read_text().replace('v3','v4')
alg=alg.replace('Every accepted family requires named and rule-based exclusions.','Every accepted family requires rule-based exclusions; named exclusions are required only when actual rejected near-neighbors exist.')
alg=alg.replace('Use three strategies:','Use the complete per-object identity registry in P3_IDENTITY_KEY_SPEC_v4.csv. It applies three strategies:')
alg += '\n\n## V. Artifact lifecycle and enforcement preflight\nBefore P3A writes any artifact, resolve the artifact catalog delivery state, identity strategy, schema/DDL target, producing phase, and dependency set. Fail if a delivered path is absent, a future output is mistaken for delivered authority, an object type lacks an identity rule, a polymorphic reference lacks a type contract, or a hyperedge role lacks a cardinality/type rule.\n'
(S46/'algorithms/P3_ALGORITHMS_AND_PSEUDOCODE_v4.md').write_text(alg)

# ---------- Execution sequence v4 ----------
seq=yaml.safe_load((S45/'P3_EXECUTION_SEQUENCE_v3.yaml').read_text())
seq['plan_id']='RAWLSING_P3_STRUCTURE_ARTICULATION_IMPLEMENTATION_PLAN_V4'
seq['corrected_by_release']='Rawlsing_J_Family_Authority_Strategy_Handoff_v24_20260731'
seq['current_state']='P2_GLOBAL_CLOSED_P3_PLAN_V4_LOCKED_EXECUTION_NOT_STARTED'
seq['next_execution_point']='P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION'
for ph in seq['phases']:
    if ph['phase']=='P3A-1':
        ph['steps'] += ['Load the complete identity, object-reference, hyperedge-role, and database-enforcement contracts.','Fail if any delivered/future artifact is misclassified or any registry object lacks an identity rule.']
        ph['exit']='Every categorical field, identity, polymorphic reference, hyperedge role, and delivered artifact closes to an enforceable contract; templates validate.'
    if ph['phase']=='P3A-7':
        ph['name']='Pilot acceptance and v25 handoff'
        ph['steps'] += ['Run artifact-lifecycle, identity-coverage, reference-type, hyperedge-role, and enforcement-contract tests.']
        ph['exit']='P3 Contract and Pilot v4 accepted.'
(S46/'P3_EXECUTION_SEQUENCE_v4.yaml').write_text(yaml.safe_dump(seq,sort_keys=False,allow_unicode=True))

# ---------- Plan lock v4 ----------
lock=json.loads((S45/'P3_PLAN_LOCK_v3.json').read_text())
lock['plan_id']='RAWLSING_P3_STRUCTURE_ARTICULATION_IMPLEMENTATION_PLAN_V4';lock['plan_version']='v4';lock['planning_audit_handoff_version']='v24';lock['next_execution_point']='P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION'
lock['locked_doctrine']=[x for x in lock['locked_doctrine'] if x!='every accepted family has named and rule-based exclusions']
lock['locked_doctrine'].append('every accepted family has a rule-based exclusion; named exclusions are mandatory only when actual rejected near-neighbors exist')
lock['locked_doctrine'] += ['every registry-backed object type has one complete identity specification','delivered and future artifacts are explicitly distinguished','all polymorphic references and hyperedge roles are type/cardinality governed','no non-executable migration skeleton is represented as a finished installer']
(S46/'P3_PLAN_LOCK_v4.json').write_text(json.dumps(lock,indent=2)+'\n')

# ---------- Release live installation blocking contract ----------
blocking={
 'contract_id':'P3_LIVE_INSTALLATION_BLOCKING_CONTRACT_V4','status':'BLOCKED_MISSING_USER_DESIGNATED_LIVE_TARGET','not_a_migration':True,
 'required_before_compilation':['designated_live_repository_or_postgresql_dsn','target_shadow_schema_name','database_role_and_privilege_map','current_promoted_authority_release','upstream_runtime_table_and_column_map','backup_and_rollback_target','write_authorization','runtime_build_commands_for_v550j_v551j_v552j'],
 'compiler_inputs_when_unblocked':['p3_postgresql_compatible_ddl_v4.sql','P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v4.csv','P3_OBJECT_REFERENCE_TYPE_CONTRACT_v4.csv','P3_HYPEREDGE_ROLE_TYPE_CONTRACT_v4.csv','P3_IDENTITY_KEY_SPEC_v4.csv','P3_LIFECYCLE_STATE_MACHINE_v4.csv','P3_RELEASE_LIFECYCLE_STATE_MACHINE_v4.csv','P3_DDL_VALIDATION_QUERIES_v4.sql'],
 'required_outputs':['forward_shadow_migration.sql','rollback.sql','prepromotion_validation_return.json','shadow_runtime_comparison_return.json','promotion_transaction.sql'],
 'prohibited_claim':'No executable live migration or installation PASS may be claimed before all required live-target facts are supplied and tested.'
}
(S46/'release/P3_LIVE_INSTALLATION_BLOCKING_CONTRACT_v4.json').write_text(json.dumps(blocking,indent=2)+'\n')

# ---------- DDL v4 ----------
ddl=(S45/'sql/p3_postgresql_compatible_ddl_v3.sql').read_text().replace('v3','v4')
# Add contract tables after categorical binding table.
needle="CREATE TABLE p3_categorical_field_binding (\n    table_name TEXT NOT NULL, column_name TEXT NOT NULL, vocabulary_domain TEXT NOT NULL,\n    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),\n    PRIMARY KEY(table_name,column_name,authority_release_id)\n);"
addition=needle+"""
CREATE TABLE p3_identity_key_contract (
    object_type TEXT NOT NULL, identity_strategy TEXT NOT NULL, id_pattern TEXT NOT NULL, idempotency_key_spec TEXT NOT NULL,
    authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), PRIMARY KEY(object_type,authority_release_id)
);
CREATE TABLE p3_candidate_lifecycle_transition (
    from_stage TEXT, to_stage TEXT NOT NULL, guard_text TEXT NOT NULL, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    UNIQUE(from_stage,to_stage,authority_release_id)
);
CREATE TABLE p3_release_lifecycle_transition (
    from_status TEXT, to_status TEXT NOT NULL, guard_text TEXT NOT NULL, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    UNIQUE(from_status,to_status,authority_release_id)
);
CREATE TABLE p3_hyperedge_role_type_contract (
    hyperedge_type TEXT NOT NULL, participant_role TEXT NOT NULL, allowed_object_types TEXT[] NOT NULL,
    minimum_count INTEGER NOT NULL CHECK(minimum_count>=0), maximum_count INTEGER CHECK(maximum_count IS NULL OR maximum_count>=minimum_count),
    authority_effect_ceiling TEXT NOT NULL, authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id),
    PRIMARY KEY(hyperedge_type,participant_role,authority_release_id)
);"""
ddl=ddl.replace(needle,addition)
# Replace trigger-comment tail with complete functions/procedures.
old="""-- Per-column triggers are generated from P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v4.csv
-- during migration assembly and validated before shadow installation.

CREATE VIEW p3_current_promoted_release AS"""
new="""
CREATE OR REPLACE FUNCTION p3_enforce_object_reference_type() RETURNS trigger AS $$
DECLARE v_column TEXT := TG_ARGV[0]; v_allowed TEXT[] := string_to_array(TG_ARGV[1], '|'); v_object_id TEXT; v_actual TEXT;
BEGIN
    v_object_id := to_jsonb(NEW) ->> v_column;
    IF v_object_id IS NULL THEN RETURN NEW; END IF;
    SELECT object_type INTO v_actual FROM p3_object_registry WHERE object_id=v_object_id;
    IF v_actual IS NULL OR NOT (v_actual = ANY(v_allowed)) THEN
        RAISE EXCEPTION 'Invalid P3 object type %.%=% actual=% allowed=%', TG_TABLE_NAME, v_column, v_object_id, v_actual, v_allowed;
    END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_forbid_update_delete() RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'P3 append-only authority table % rejects %', TG_TABLE_NAME, TG_OP;
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_candidate_status_event() RETURNS trigger AS $$
DECLARE p_stage TEXT; p_ord INTEGER;
BEGIN
    SELECT to_stage,event_ordinal INTO p_stage,p_ord FROM p3_candidate_status_event
    WHERE candidate_family_id=NEW.candidate_family_id ORDER BY event_ordinal DESC LIMIT 1;
    IF p_ord IS NULL THEN
        IF NEW.event_ordinal<>1 OR NEW.from_stage IS NOT NULL OR NEW.to_stage<>'DISCOVERED' THEN RAISE EXCEPTION 'Invalid first candidate event'; END IF;
    ELSE
        IF NEW.event_ordinal<>p_ord+1 OR NEW.from_stage IS DISTINCT FROM p_stage THEN RAISE EXCEPTION 'Noncontiguous candidate event'; END IF;
        IF NOT EXISTS (SELECT 1 FROM p3_candidate_lifecycle_transition t WHERE t.from_stage=NEW.from_stage AND t.to_stage=NEW.to_stage AND t.authority_release_id=NEW.authority_release_id) THEN RAISE EXCEPTION 'Disallowed candidate transition % -> %',NEW.from_stage,NEW.to_stage; END IF;
    END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_release_status_event() RETURNS trigger AS $$
DECLARE p_status TEXT; p_ord INTEGER;
BEGIN
    SELECT status,event_ordinal INTO p_status,p_ord FROM p3_release_status_event WHERE release_id=NEW.release_id ORDER BY event_ordinal DESC LIMIT 1;
    IF p_ord IS NULL THEN
        IF NEW.event_ordinal<>1 OR NEW.status<>'DRAFT' THEN RAISE EXCEPTION 'Invalid first release event'; END IF;
    ELSE
        IF NEW.event_ordinal<>p_ord+1 THEN RAISE EXCEPTION 'Noncontiguous release event'; END IF;
        IF NOT EXISTS (SELECT 1 FROM p3_release_lifecycle_transition t WHERE t.from_status=p_status AND t.to_status=NEW.status AND t.authority_release_id=NEW.release_id) THEN RAISE EXCEPTION 'Disallowed release transition % -> %',p_status,NEW.status; END IF;
    END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_promotion_pointer() RETURNS trigger AS $$
DECLARE latest_status TEXT;
BEGIN
    SELECT status INTO latest_status FROM p3_release_status_event WHERE release_id=NEW.promoted_release_id ORDER BY event_ordinal DESC LIMIT 1;
    IF latest_status IS DISTINCT FROM 'PROMOTED' THEN RAISE EXCEPTION 'Promotion pointer requires latest PROMOTED event, got %',latest_status; END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE p3_install_contract_triggers(p_release_id TEXT) LANGUAGE plpgsql AS $$
DECLARE r RECORD; tname TEXT;
BEGIN
    FOR r IN SELECT table_name,column_name,vocabulary_domain FROM p3_categorical_field_binding WHERE authority_release_id=p_release_id LOOP
        tname := 'p3_vocab_'||substr(md5(r.table_name||'.'||r.column_name),1,16);
        EXECUTE format('DROP TRIGGER IF EXISTS %I ON %I',tname,r.table_name);
        EXECUTE format('CREATE TRIGGER %I BEFORE INSERT OR UPDATE OF %I ON %I FOR EACH ROW EXECUTE FUNCTION p3_enforce_vocab_code(%L,%L)',tname,r.column_name,r.table_name,r.vocabulary_domain,r.column_name);
    END LOOP;
    FOR r IN SELECT table_name,column_name,array_to_string(allowed_object_types,'|') allowed FROM p3_object_reference_type_contract WHERE authority_release_id=p_release_id LOOP
        tname := 'p3_type_'||substr(md5(r.table_name||'.'||r.column_name),1,16);
        EXECUTE format('DROP TRIGGER IF EXISTS %I ON %I',tname,r.table_name);
        EXECUTE format('CREATE TRIGGER %I BEFORE INSERT OR UPDATE OF %I ON %I FOR EACH ROW EXECUTE FUNCTION p3_enforce_object_reference_type(%L,%L)',tname,r.column_name,r.table_name,r.column_name,r.allowed);
    END LOOP;
END; $$;

CREATE TRIGGER p3_candidate_status_event_validate BEFORE INSERT ON p3_candidate_status_event FOR EACH ROW EXECUTE FUNCTION p3_validate_candidate_status_event();
CREATE TRIGGER p3_release_status_event_validate BEFORE INSERT ON p3_release_status_event FOR EACH ROW EXECUTE FUNCTION p3_validate_release_status_event();
CREATE TRIGGER p3_promotion_pointer_validate BEFORE INSERT OR UPDATE ON p3_runtime_promotion_pointer FOR EACH ROW EXECUTE FUNCTION p3_validate_promotion_pointer();

CREATE TRIGGER p3_adjudication_decision_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_decision FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_member_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_member FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_collision_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_collision_disposition FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_hierarchy_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_hierarchy_relation FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_release_event_immutable BEFORE UPDATE OR DELETE ON p3_release_status_event FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_candidate_event_immutable BEFORE UPDATE OR DELETE ON p3_candidate_status_event FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_doctrine_delta_immutable BEFORE UPDATE OR DELETE ON p3_doctrine_delta FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_family_genealogy_immutable BEFORE UPDATE OR DELETE ON p3_family_genealogy FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();

CREATE VIEW p3_current_promoted_release AS"""
if old not in ddl: raise RuntimeError('DDL tail marker not found')
ddl=ddl.replace(old,new)
# add status-specific adjudication check after table block via ALTER
marker="CREATE TABLE p3_adjudication_member"
check="""ALTER TABLE p3_adjudication_decision ADD CONSTRAINT p3_adjudication_status_fields CHECK (
    (decision_status IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS') AND canonical_family_id IS NOT NULL AND canonical_proposition IS NOT NULL)
 OR (decision_status NOT IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS') AND canonical_family_id IS NULL)
);
"""
ddl=ddl.replace(marker,check+marker)
(S46/'sql/p3_postgresql_compatible_ddl_v4.sql').write_text(ddl)

# ---------- Validation SQL v4 ----------
val=(S45/'sql/P3_DDL_VALIDATION_QUERIES_v3.sql').read_text().replace('v3','v4')
val += '''\n-- Q19-Q25 bounded-readiness enforcement checks.\nSELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q19_identity_contract_complete FROM p3_object_registry o LEFT JOIN p3_identity_key_contract c ON c.object_type=o.object_type AND c.authority_release_id=o.allocation_release_id WHERE c.object_type IS NULL OR c.identity_strategy<>o.identity_strategy;\nSELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q20_vocab_triggers_installed FROM p3_categorical_field_binding b WHERE NOT EXISTS (SELECT 1 FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid WHERE c.relname=b.table_name AND NOT t.tgisinternal AND pg_get_triggerdef(t.oid) LIKE '%p3_enforce_vocab_code%');\nSELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q21_type_triggers_installed FROM p3_object_reference_type_contract b WHERE NOT EXISTS (SELECT 1 FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid WHERE c.relname=b.table_name AND NOT t.tgisinternal AND pg_get_triggerdef(t.oid) LIKE '%p3_enforce_object_reference_type%');\nSELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q22_hyperedge_roles_valid FROM p3_hyperedge h JOIN p3_hyperedge_membership m USING(hyperedge_id) LEFT JOIN p3_hyperedge_role_type_contract c ON c.hyperedge_type=h.hyperedge_type AND c.participant_role=m.participant_role AND c.authority_release_id=h.authority_release_id LEFT JOIN p3_object_registry o ON o.object_id=m.object_id WHERE c.hyperedge_type IS NULL OR NOT (o.object_type=ANY(c.allowed_object_types));\nSELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q23_pair_count_states FROM p3_candidate_revision r JOIN (SELECT candidate_revision_id,COUNT(*) n FROM p3_internal_pair_matrix GROUP BY 1) x USING(candidate_revision_id) JOIN (SELECT candidate_revision_id,COUNT(*) n FROM p3_candidate_membership GROUP BY 1) m USING(candidate_revision_id) WHERE x.n<>(m.n*(m.n-1))/2;\nSELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q24_latest_pointer_promoted FROM p3_runtime_promotion_pointer p WHERE (SELECT status FROM p3_release_status_event e WHERE e.release_id=p.promoted_release_id ORDER BY event_ordinal DESC LIMIT 1) IS DISTINCT FROM 'PROMOTED';\nSELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q25_hyperedge_cardinality FROM p3_hyperedge h JOIN p3_hyperedge_role_type_contract c ON c.hyperedge_type=h.hyperedge_type AND c.authority_release_id=h.authority_release_id LEFT JOIN (SELECT hyperedge_id,participant_role,COUNT(*) n FROM p3_hyperedge_membership GROUP BY 1,2) m ON m.hyperedge_id=h.hyperedge_id AND m.participant_role=c.participant_role WHERE COALESCE(m.n,0)<c.minimum_count OR (c.maximum_count IS NOT NULL AND COALESCE(m.n,0)>c.maximum_count);\n'''
(S46/'sql/P3_DDL_VALIDATION_QUERIES_v4.sql').write_text(val)

# ---------- Categorical binding: add contract tables finite fields ----------
bind=read_csv(S45/'P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v3.csv')
# v3 names don't matter, content same
newbind=bind[:]
def addb(t,c,d,req='YES'):
    if not any(r['table_name']==t and r['column_name']==c for r in newbind): newbind.append({'table_name':t,'column_name':c,'vocabulary_domain':d,'enforcement':'DDL_CHECK_AND_OR_MIGRATION_TRIGGER','required':req})
addb('p3_candidate_lifecycle_transition','from_stage','lifecycle_stage','NO');addb('p3_candidate_lifecycle_transition','to_stage','lifecycle_stage')
addb('p3_release_lifecycle_transition','from_status','release_status','NO');addb('p3_release_lifecycle_transition','to_status','release_status')
addb('p3_hyperedge_role_type_contract','hyperedge_type','hyperedge_type');addb('p3_hyperedge_role_type_contract','participant_role','hyperedge_participant_role');addb('p3_hyperedge_role_type_contract','authority_effect_ceiling','hyperedge_authority_effect')
write_csv(S46/'P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v4.csv',newbind,['table_name','column_name','vocabulary_domain','enforcement','required'])

# ---------- Acceptance gates/test plan ----------
gates=read_csv(S45/'validation/P3_ACCEPTANCE_GATES_v3.csv')
for r in gates:
    r['requirement']=r['requirement'].replace('Every family revision has members, variants, exclusions, and evidence hash.','Every family revision has members, exclusions, and evidence hash; variants are required only when governed variation exists.')
newg=[
('P3G-056','PLAN','FATAL','Artifact catalog distinguishes delivered contracts/input audits from future outputs; every delivered path exists exactly and no future output is represented as delivered.'),
('P3G-057','PLAN','FATAL','Identity-key specification covers every registry-backed object type exactly once and every schema ID pattern agrees with it.'),
('P3G-058','PLAN','FATAL','Every polymorphic object reference and every hyperedge participant role has an allowed type/cardinality contract.'),
('P3G-059','PLAN','FATAL','No governing installation artifact is a non-executable skeleton or placeholder; unavailable live-target work is represented by an explicit blocking contract.'),
('P3G-060','PLAN','FATAL','Candidate internal-pair counts include DIRECT_UNRESOLVED and all seven states reconcile to n(n-1)/2.'),
('P3G-061','PLAN','FATAL','DDL defines executable enforcement mechanisms for vocabularies, object types, append-only authority, lifecycles, and promotion pointer semantics.'),
('P3G-062','PLAN','FATAL','Plan lock, execution sequence, artifact catalog, schemas, and exact resume controls name the same governing version and next execution point.'),
('P3G-063','PLAN','FATAL','Exclusion doctrine requires rule-based exclusions universally and named exclusions only when actual rejected near-neighbors exist; no contract contradicts this.'),
]
for a,b,c,d in newg:gates.append({'gate_id':a,'phase':b,'severity':c,'requirement':d})
write_csv(S46/'validation/P3_ACCEPTANCE_GATES_v4.csv',gates,['gate_id','phase','severity','requirement'])
tests=read_csv(S45/'validation/P3_TEST_AND_MUTATION_PLAN_v3.csv')
newt=[
('P3T-049','integration','YES','Every artifact catalog row marked delivered resolves to an exact file; every planned output is absent or explicitly generated by its phase.'),
('P3T-050','integration','YES','Identity contract covers every registry object type and pair-fact/component/signature/segment/collision/closure IDs reproduce from canonical serialization.'),
('P3T-051','mutation','YES','Remove one object-type identity row and identity-coverage gate fails.'),
('P3T-052','mutation','YES','Use an unauthorized object type in a candidate, component, variant, or hyperedge role and type/cardinality validation fails.'),
('P3T-053','mutation','YES','Omit DIRECT_UNRESOLVED from candidate pair counts or make state totals differ from n(n-1)/2 and packet closure fails.'),
('P3T-054','mutation','YES','Attempt UPDATE or DELETE on immutable adjudication or event tables and database enforcement rejects it.'),
('P3T-055','mutation','YES','Insert noncontiguous or disallowed candidate/release lifecycle event and transition trigger rejects it.'),
('P3T-056','mutation','YES','Point runtime promotion at a release whose latest status is not PROMOTED and promotion trigger rejects it.'),
('P3T-057','integration','YES','Governing section contains no scaffold, placeholder, TODO, TBD, FIXME, or unclassified future output.'),
('P3T-058','integration','YES','Plan lock, execution sequence, resume control, current state, and master handoff agree on Plan v4 and P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION.'),
]
for a,b,c,d in newt:tests.append({'test_id':a,'test_class':b,'required':c,'test_definition':d})
write_csv(S46/'validation/P3_TEST_AND_MUTATION_PLAN_v4.csv',tests,['test_id','test_class','required','test_definition'])

# ---------- Update evidence matrix unchanged name v4 and relation/lifecycle etc already copied ----------
# Correct lifecycle v4 copy from v3 already; ensure name.
# Upstream files copied with v4 names, content unchanged.

# ---------- Final bounded contract hardening discovered by independent third-pass audit ----------
# These changes finish existing v4 promises; they add no new phase, DBMS, or authority layer.

# Canonical serialization contract and fixed test vectors.
serialization_contract={
 'contract_id':'P3_CANONICAL_SERIALIZATION_CONTRACT_V4',
 'encoding':'UTF-8','unicode_normalization':'NFC','line_endings':'LF',
 'object_key_order':'lexicographic_by_unicode_code_point_after_NFC',
 'whitespace':'none_outside_strings','ensure_ascii':False,
 'allowed_scalar_types':['null','boolean','integer','string'],
 'forbidden_numeric_types':['float','decimal','NaN','Infinity','negative_zero'],
 'absent_vs_null':'distinct; include null only when the identity-key specification names the field',
 'set_like_arrays':'Only fields named in set_like_array_paths may be reordered. Normalize each element recursively, reject duplicates after normalization, then sort by canonical serialized bytes.',
 'ordered_arrays':'Preserve order exactly.',
 'hash':'SHA-256 over canonical UTF-8 bytes',
 'display_id':'object-type prefix plus first 16 lowercase hex; full 64-hex content_hash is mandatory and collisions are fatal',
 'set_like_array_paths':{
   'LINEAGE_SEGMENT':['implementation_ids'],
   'PROPOSITION_SIGNATURE':['fields.*.evidence_ids','response_topologies'],
   'PAIR_FACT':['source_authority_ids','evidence_ids'],
   'COLLISION':['source_authority_ids','downstream_effects'],
   'CANDIDATE_COMPONENT':['member_ids','connectivity_pair_fact_ids'],
   'HYPEREDGE':['members'],
   'CANDIDATE_PACKET':['exact_evidence_links']
 },
 'schema_version_in_hash':True,
 'failure_conditions':['duplicate normalized set member','unsupported scalar type','unpaired surrogate','ID prefix/full-hash collision','identity payload missing required key']
}
(S46/'P3_CANONICAL_SERIALIZATION_CONTRACT_v4.json').write_text(json.dumps(serialization_contract,indent=2,ensure_ascii=False)+'\n')
serialization_vectors={
 'contract_id':'P3_CANONICAL_SERIALIZATION_TEST_VECTORS_V4',
 'vectors':[
  {'name':'key_order_and_line_endings','a':{'b':'x\r\ny','a':1},'b':{'a':1,'b':'x\ny'},'must_match':True},
  {'name':'unicode_nfc','a':{'x':'e\u0301'},'b':{'x':'é'},'must_match':True},
  {'name':'set_order','object_type':'CANDIDATE_COMPONENT','path':'member_ids','a':{'member_ids':['b','a']},'b':{'member_ids':['a','b']},'must_match':True},
  {'name':'ordered_array','a':{'x':['b','a']},'b':{'x':['a','b']},'must_match':False},
  {'name':'null_vs_absent','a':{'x':None},'b':{},'must_match':False},
  {'name':'duplicate_set_member','object_type':'CANDIDATE_COMPONENT','path':'member_ids','a':{'member_ids':['a','a']},'must_fail':True}
 ]
}
(S46/'P3_CANONICAL_SERIALIZATION_TEST_VECTORS_v4.json').write_text(json.dumps(serialization_vectors,indent=2,ensure_ascii=False)+'\n')

# JSON Schema identity patterns and persistence-shape closure.
def load_schema(name): return json.loads((schema_dir/name).read_text())
def save_schema(name,s): (schema_dir/name).write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n')

s=load_schema('proposition_signature.schema.json'); s['properties']['signature_id']={'type':'string','pattern':'^P3SIG-[0-9a-f]{16}$'}; save_schema('proposition_signature.schema.json',s)
s=load_schema('hyperedge.schema.json'); s['properties']['hyperedge_id']={'type':'string','pattern':'^P3HYP-[0-9a-f]{16}$'}
# Hyperedge role names and minimum/maximum role counts are enforced in the connected schema as well as DDL.
role_contract=read_csv(S46/'P3_HYPEREDGE_ROLE_TYPE_CONTRACT_v4.csv')
all_roles=sorted({r['participant_role'] for r in role_contract})
s['properties']['members']['items']['properties']['participant_role']={'enum':all_roles}
s['allOf']=[]
for ht in sorted({r['hyperedge_type'] for r in role_contract}):
    rows=[r for r in role_contract if r['hyperedge_type']==ht]
    allowed_roles=[r['participant_role'] for r in rows]
    effect=rows[0]['authority_effect_ceiling']
    then={'properties':{'authority_effect':{'const':effect},'members':{'items':{'properties':{'participant_role':{'enum':allowed_roles}}},'allOf':[]}}}
    for r in rows:
        cond={'contains':{'properties':{'participant_role':{'const':r['participant_role']}},'required':['participant_role']},'minContains':int(r['minimum_count'])}
        if r['maximum_count']!='UNBOUNDED': cond['maxContains']=int(r['maximum_count'])
        then['properties']['members']['allOf'].append(cond)
    s['allOf'].append({'if':{'properties':{'hyperedge_type':{'const':ht}},'required':['hyperedge_type']},'then':then})
save_schema('hyperedge.schema.json',s)

s=load_schema('response_contract_reference.schema.json'); s['properties']['reference_id']={'type':'string','pattern':'^P3RCR-[0-9a-f]{16}$'}; save_schema('response_contract_reference.schema.json',s)
s=load_schema('structural_context_reference.schema.json'); s['properties']['reference_id']={'type':'string','pattern':'^P3SCR-[0-9a-f]{16}$'}; save_schema('structural_context_reference.schema.json',s)

s=load_schema('candidate_family.schema.json')
s['properties']['revision_number']={'type':'integer','minimum':1}
if 'revision_number' not in s['required']: s['required'].insert(s['required'].index('revision_id')+1,'revision_number')
save_schema('candidate_family.schema.json',s)

s=load_schema('candidate_variant.schema.json')
s['required']=['variant_id','variant_revision_id','revision_number','owner_object_id','variant_dimension','variant_value','member_ids','value_portability_status','authority_release_id']
s['properties']['variant_revision_id']={'type':'string','pattern':'^P3VARREV-[0-9]{6}-R[0-9]{4}$'}
s['properties']['revision_number']={'type':'integer','minimum':1}
save_schema('candidate_variant.schema.json',s)

s=load_schema('variant_assignment.schema.json')
s['properties']['variant_revision_id']={'anyOf':[{'type':'string','pattern':'^P3VARREV-[0-9]{6}-R[0-9]{4}$'},{'type':'null'}]}
save_schema('variant_assignment.schema.json',s)

# Named exclusions require named objects; rule exclusions cannot pretend to be named-member records.
s=load_schema('family_exclusion.schema.json')
s['allOf']=[
 {'if':{'properties':{'exclusion_type':{'const':'NAMED_MEMBER'}},'required':['exclusion_type']},'then':{'required':['excluded_object_ids'],'properties':{'excluded_object_ids':{'minItems':1}}}},
 {'if':{'properties':{'exclusion_type':{'const':'RULE_BASED'}},'required':['exclusion_type']},'then':{'properties':{'excluded_object_ids':{'maxItems':0}}}}
]
save_schema('family_exclusion.schema.json',s)

# Directional collisions require explicit semantic roles; symmetric collisions prohibit them.
s=load_schema('collision_scope.schema.json')
s['allOf']=[
 {'if':{'properties':{'orientation':{'const':'DIRECTIONAL'}},'required':['orientation']},'then':{'required':['left_role','right_role'],'properties':{'left_role':{'type':'string','minLength':1},'right_role':{'type':'string','minLength':1}}}},
 {'if':{'properties':{'orientation':{'const':'SYMMETRIC'}},'required':['orientation']},'then':{'properties':{'left_role':{'type':'null'},'right_role':{'type':'null'}}}}
]
save_schema('collision_scope.schema.json',s)

# Final and draft decisions carry split points explicitly. Final status rules require the appropriate structured surface.
for name,final in [('adjudication_decision.schema.json',True),('adjudication_decision_draft.schema.json',False)]:
    s=load_schema(name)
    s['properties']['split_points']={'type':'array','items':{'$ref':'https://rawlsing.local/schemas/p3/v4/split_point.schema.json'}}
    if 'split_points' not in s['required']: s['required'].insert(s['required'].index('hierarchical_relations'),'split_points')
    if final:
        s.setdefault('allOf',[]).extend([
          {'if':{'properties':{'decision_status':{'const':'SPLIT_REQUIRED'}},'required':['decision_status']},'then':{'properties':{'split_points':{'minItems':1}}}},
          {'if':{'properties':{'decision_status':{'const':'HIERARCHICAL_RELATION_ONLY'}},'required':['decision_status']},'then':{'properties':{'hierarchical_relations':{'minItems':1}}}},
          {'if':{'properties':{'decision_status':{'enum':['BLOCKED_UNRESOLVED','INSUFFICIENT_AUTHORITY']}},'required':['decision_status']},'then':{'properties':{'unresolved_boundaries':{'minItems':1}}}}
        ])
    save_schema(name,s)

# DDL hardening: revision ordinals, complete adjudication persistence, exact endpoint/role checks,
# and executable identity/vocabulary/hyperedge enforcement.
ddl_path=S46/'sql/p3_postgresql_compatible_ddl_v4.sql'; ddl=ddl_path.read_text()
ddl=ddl.replace("candidate_revision_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), candidate_family_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id),\n    lifecycle_stage", "candidate_revision_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), candidate_family_id TEXT NOT NULL REFERENCES p3_candidate_family(candidate_family_id), revision_number INTEGER NOT NULL CHECK(revision_number>=1),\n    lifecycle_stage")
ddl=ddl.replace("authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), UNIQUE(candidate_family_id,authority_release_id)", "authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), UNIQUE(candidate_family_id,revision_number), UNIQUE(candidate_family_id,authority_release_id)")
ddl=ddl.replace("variant_revision_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), variant_id TEXT NOT NULL REFERENCES p3_family_variant(variant_id),\n    variant_dimension", "variant_revision_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), variant_id TEXT NOT NULL REFERENCES p3_family_variant(variant_id), revision_number INTEGER NOT NULL CHECK(revision_number>=1),\n    variant_dimension")
ddl=ddl.replace("authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), UNIQUE(variant_id,authority_release_id)", "authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), UNIQUE(variant_id,revision_number), UNIQUE(variant_id,authority_release_id)")
ddl=ddl.replace("adjudication_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id),\n    decision_status", "adjudication_id TEXT PRIMARY KEY REFERENCES p3_object_registry(object_id), candidate_revision_id TEXT NOT NULL REFERENCES p3_candidate_revision(candidate_revision_id), decision_ordinal INTEGER NOT NULL CHECK(decision_ordinal>=1),\n    decision_status")
ddl=ddl.replace("authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), created_at TIMESTAMPTZ NOT NULL\n);", "authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), created_at TIMESTAMPTZ NOT NULL, UNIQUE(candidate_revision_id,decision_ordinal)\n);")
# Canonical symmetric endpoint storage and directional collision role semantics.
ddl=ddl.replace("authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), CHECK(left_object_id <> right_object_id),\n    CHECK(proposition_graph_allowed", "authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), CHECK(left_object_id <> right_object_id), CHECK(orientation='DIRECTIONAL' OR left_object_id < right_object_id),\n    CHECK(proposition_graph_allowed")
ddl=ddl.replace("authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), CHECK(left_object_id < right_object_id)\n);\nCREATE TABLE p3_collision_authority_source", "authority_release_id TEXT NOT NULL REFERENCES p3_authority_release(release_id), CHECK(left_object_id < right_object_id),\n    CHECK((orientation='DIRECTIONAL' AND left_role IS NOT NULL AND right_role IS NOT NULL AND left_role<>right_role) OR (orientation='SYMMETRIC' AND left_role IS NULL AND right_role IS NULL))\n);\nCREATE TABLE p3_collision_authority_source")
# Persist split points and unresolved boundaries rather than leaving them only in packet JSON.
anchor="CREATE TABLE p3_adjudication_hierarchy_relation (adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), broader_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), narrower_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), relation_role TEXT NOT NULL, PRIMARY KEY(adjudication_id,broader_object_id,narrower_object_id));"
extra=anchor+"""
CREATE TABLE p3_adjudication_split_point (
    adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), split_ordinal INTEGER NOT NULL CHECK(split_ordinal>=1),
    dimension TEXT NOT NULL, rationale TEXT NOT NULL, PRIMARY KEY(adjudication_id,split_ordinal)
);
CREATE TABLE p3_adjudication_split_member (
    adjudication_id TEXT NOT NULL, split_ordinal INTEGER NOT NULL, split_side TEXT NOT NULL CHECK(split_side IN ('LEFT','RIGHT')),
    member_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    PRIMARY KEY(adjudication_id,split_ordinal,split_side,member_object_id),
    FOREIGN KEY(adjudication_id,split_ordinal) REFERENCES p3_adjudication_split_point(adjudication_id,split_ordinal)
);
CREATE TABLE p3_adjudication_unresolved_boundary (
    adjudication_id TEXT NOT NULL REFERENCES p3_adjudication_decision(adjudication_id), boundary_id TEXT NOT NULL,
    left_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id), right_object_id TEXT NOT NULL REFERENCES p3_object_registry(object_id),
    reason TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('OPEN','FAIL_CLOSED','RESOLVED_ACCEPT','RESOLVED_EXCLUDE','RESOLVED_SPLIT')),
    PRIMARY KEY(adjudication_id,boundary_id), CHECK(left_object_id < right_object_id)
);"""
if anchor in ddl: ddl=ddl.replace(anchor,extra)
# Release-scoped vocabulary snapshot semantics: p3_vocabulary_revision is complete for each release.
ddl=ddl.replace("v_value := to_jsonb(NEW) ->> v_column;\n    IF v_value IS NOT NULL AND NOT EXISTS (\n        SELECT 1 FROM p3_vocabulary_code c\n        WHERE c.vocabulary_domain=v_domain AND c.code=v_value\n          AND c.retired_release_id IS NULL\n    )", "v_value := to_jsonb(NEW) ->> v_column;\n    IF v_value IS NOT NULL AND NOT EXISTS (\n        SELECT 1 FROM p3_vocabulary_revision c\n        WHERE c.vocabulary_domain=v_domain AND c.code=v_value\n          AND c.authority_release_id=TG_ARGV[2] AND NOT c.deprecated\n    )")
# Install identity and hyperedge enforcement functions before lifecycle functions.
fun_anchor="CREATE OR REPLACE FUNCTION p3_forbid_update_delete() RETURNS trigger AS $$"
new_functions="""CREATE OR REPLACE FUNCTION p3_enforce_identity_contract() RETURNS trigger AS $$
DECLARE c RECORD; suffix TEXT;
BEGIN
    SELECT * INTO c FROM p3_identity_key_contract WHERE object_type=NEW.object_type AND authority_release_id=NEW.allocation_release_id;
    IF c.object_type IS NULL THEN RAISE EXCEPTION 'Missing identity contract for % release %',NEW.object_type,NEW.allocation_release_id; END IF;
    IF NEW.identity_strategy<>c.identity_strategy THEN RAISE EXCEPTION 'Identity strategy mismatch for %',NEW.object_id; END IF;
    IF c.id_pattern='UPSTREAM_EXACT' THEN
        IF NEW.object_id<>NEW.idempotency_key THEN RAISE EXCEPTION 'Inherited object ID must equal exact upstream idempotency key'; END IF;
    ELSE
        IF NEW.object_id !~ ('^'||c.id_pattern||'$') THEN RAISE EXCEPTION 'Object ID % violates %',NEW.object_id,c.id_pattern; END IF;
        IF NEW.identity_strategy='CONTENT_ADDRESSED_DERIVED_ID' THEN
            IF NEW.content_hash IS NULL THEN RAISE EXCEPTION 'Content-addressed object requires full content_hash'; END IF;
            suffix:=split_part(NEW.object_id,'-',2);
            IF suffix<>substr(NEW.content_hash,1,16) THEN RAISE EXCEPTION 'Content ID prefix does not match full hash'; END IF;
        END IF;
    END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_hyperedge_member_type() RETURNS trigger AS $$
DECLARE h RECORD; c RECORD; actual TEXT;
BEGIN
    SELECT hyperedge_type,authority_effect,authority_release_id INTO h FROM p3_hyperedge WHERE hyperedge_id=NEW.hyperedge_id;
    SELECT * INTO c FROM p3_hyperedge_role_type_contract WHERE hyperedge_type=h.hyperedge_type AND participant_role=NEW.participant_role AND authority_release_id=h.authority_release_id;
    SELECT object_type INTO actual FROM p3_object_registry WHERE object_id=NEW.object_id;
    IF c.hyperedge_type IS NULL OR NOT(actual=ANY(c.allowed_object_types)) OR h.authority_effect<>c.authority_effect_ceiling THEN
        RAISE EXCEPTION 'Invalid hyperedge participant %, role %, type %, effect %',NEW.object_id,NEW.participant_role,actual,h.authority_effect;
    END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION p3_validate_hyperedge_cardinality() RETURNS trigger AS $$
DECLARE hid TEXT:=COALESCE(NEW.hyperedge_id,OLD.hyperedge_id); h RECORD; c RECORD; n INTEGER;
BEGIN
    SELECT hyperedge_type,authority_release_id INTO h FROM p3_hyperedge WHERE hyperedge_id=hid;
    IF h.hyperedge_type IS NULL THEN RETURN COALESCE(NEW,OLD); END IF;
    FOR c IN SELECT * FROM p3_hyperedge_role_type_contract WHERE hyperedge_type=h.hyperedge_type AND authority_release_id=h.authority_release_id LOOP
        SELECT COUNT(*) INTO n FROM p3_hyperedge_membership WHERE hyperedge_id=hid AND participant_role=c.participant_role;
        IF n<c.minimum_count OR (c.maximum_count IS NOT NULL AND n>c.maximum_count) THEN RAISE EXCEPTION 'Hyperedge % role % cardinality % outside [%..%]',hid,c.participant_role,n,c.minimum_count,c.maximum_count; END IF;
    END LOOP;
    RETURN COALESCE(NEW,OLD);
END; $$ LANGUAGE plpgsql;

"""+fun_anchor
if fun_anchor in ddl: ddl=ddl.replace(fun_anchor,new_functions)
# Trigger installer uses the exact vocabulary snapshot release.
ddl=ddl.replace("p3_enforce_vocab_code(%L,%L)',tname,r.column_name,r.table_name,r.vocabulary_domain,r.column_name)", "p3_enforce_vocab_code(%L,%L,%L)',tname,r.column_name,r.table_name,r.vocabulary_domain,r.column_name,p_release_id)")
# Direct enforcement triggers and immutable structured decision children/revisions.
trig_anchor="CREATE TRIGGER p3_candidate_status_event_validate BEFORE INSERT ON p3_candidate_status_event"
trig_prefix="""CREATE TRIGGER p3_object_registry_identity_validate BEFORE INSERT OR UPDATE ON p3_object_registry FOR EACH ROW EXECUTE FUNCTION p3_enforce_identity_contract();
CREATE TRIGGER p3_hyperedge_member_type_validate BEFORE INSERT OR UPDATE ON p3_hyperedge_membership FOR EACH ROW EXECUTE FUNCTION p3_validate_hyperedge_member_type();
CREATE CONSTRAINT TRIGGER p3_hyperedge_member_cardinality AFTER INSERT OR UPDATE OR DELETE ON p3_hyperedge_membership DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_hyperedge_cardinality();
CREATE CONSTRAINT TRIGGER p3_hyperedge_cardinality_after_header AFTER INSERT OR UPDATE ON p3_hyperedge DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION p3_validate_hyperedge_cardinality();

"""+trig_anchor
if trig_anchor in ddl: ddl=ddl.replace(trig_anchor,trig_prefix)
immut_anchor="CREATE TRIGGER p3_adjudication_hierarchy_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_hierarchy_relation FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();"
immut_extra=immut_anchor+"""
CREATE TRIGGER p3_adjudication_split_point_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_split_point FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_split_member_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_split_member FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_adjudication_unresolved_immutable BEFORE UPDATE OR DELETE ON p3_adjudication_unresolved_boundary FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_candidate_revision_immutable BEFORE UPDATE OR DELETE ON p3_candidate_revision FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_variant_revision_immutable BEFORE UPDATE OR DELETE ON p3_family_variant_revision FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_family_exclusion_immutable BEFORE UPDATE OR DELETE ON p3_family_exclusion FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_hyperedge_immutable BEFORE UPDATE OR DELETE ON p3_hyperedge FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();
CREATE TRIGGER p3_canonical_family_revision_immutable BEFORE UPDATE OR DELETE ON p3_canonical_family_revision FOR EACH ROW EXECUTE FUNCTION p3_forbid_update_delete();"""
if immut_anchor in ddl: ddl=ddl.replace(immut_anchor,immut_extra)
ddl_path.write_text(ddl)

# Update DDL validation queries with exact trigger and status-specific checks.
val_path=S46/'sql/P3_DDL_VALIDATION_QUERIES_v4.sql'; val=val_path.read_text().replace('generated by the v23 validator','generated by the v24 validator')
val += """
-- Q26-Q34 final bounded-readiness closure.
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q26_identity_values_valid FROM p3_object_registry o JOIN p3_identity_key_contract c ON c.object_type=o.object_type AND c.authority_release_id=o.allocation_release_id WHERE o.identity_strategy<>c.identity_strategy OR (c.id_pattern<>'UPSTREAM_EXACT' AND o.object_id !~ ('^'||c.id_pattern||'$')) OR (o.identity_strategy='CONTENT_ADDRESSED_DERIVED_ID' AND (o.content_hash IS NULL OR split_part(o.object_id,'-',2)<>substr(o.content_hash,1,16)));
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q27_candidate_revision_ordinals FROM p3_candidate_revision WHERE candidate_revision_id !~ ('^P3CANDREV-'||substring(candidate_family_id from '[0-9]{6}$')||'-R'||lpad(revision_number::text,4,'0')||'$');
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q28_variant_revision_ordinals FROM p3_family_variant_revision WHERE variant_revision_id !~ ('^P3VARREV-'||substring(variant_id from '[0-9]{6}$')||'-R'||lpad(revision_number::text,4,'0')||'$');
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q29_status_specific_decisions FROM p3_adjudication_decision a WHERE (a.decision_status='SPLIT_REQUIRED' AND NOT EXISTS (SELECT 1 FROM p3_adjudication_split_point s WHERE s.adjudication_id=a.adjudication_id)) OR (a.decision_status='HIERARCHICAL_RELATION_ONLY' AND NOT EXISTS (SELECT 1 FROM p3_adjudication_hierarchy_relation h WHERE h.adjudication_id=a.adjudication_id)) OR (a.decision_status IN ('BLOCKED_UNRESOLVED','INSUFFICIENT_AUTHORITY') AND NOT EXISTS (SELECT 1 FROM p3_adjudication_unresolved_boundary u WHERE u.adjudication_id=a.adjudication_id)) OR (a.decision_status='ACCEPTED_WITH_VARIANTS' AND NOT EXISTS (SELECT 1 FROM p3_adjudication_member m WHERE m.adjudication_id=a.adjudication_id AND m.variant_revision_id IS NOT NULL));
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q30_named_exclusion_shape FROM p3_family_exclusion e WHERE (e.exclusion_type='NAMED_MEMBER' AND NOT EXISTS (SELECT 1 FROM p3_excluded_object x WHERE x.exclusion_id=e.exclusion_id)) OR (e.exclusion_type='RULE_BASED' AND EXISTS (SELECT 1 FROM p3_excluded_object x WHERE x.exclusion_id=e.exclusion_id));
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q31_collision_roles FROM p3_collision_scope_registry WHERE (orientation='DIRECTIONAL' AND (left_role IS NULL OR right_role IS NULL OR left_role=right_role)) OR (orientation='SYMMETRIC' AND (left_role IS NOT NULL OR right_role IS NOT NULL));
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q32_symmetric_pair_order FROM p3_pair_fact_bundle WHERE orientation='SYMMETRIC' AND left_object_id>=right_object_id;
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q33_candidate_latest_stage_matches_revision FROM p3_candidate_revision r WHERE r.lifecycle_stage IS DISTINCT FROM (SELECT e.to_stage FROM p3_candidate_status_event e WHERE e.candidate_family_id=r.candidate_family_id ORDER BY e.event_ordinal DESC LIMIT 1);
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q34_vocabulary_snapshot_complete FROM p3_categorical_field_binding b WHERE NOT EXISTS (SELECT 1 FROM p3_vocabulary_revision v WHERE v.vocabulary_domain=b.vocabulary_domain AND v.authority_release_id=b.authority_release_id AND NOT v.deprecated);
"""
val_path.write_text(val)

# Object-reference and categorical binding contracts for newly normalized decision surfaces.
refs=read_csv(S46/'P3_OBJECT_REFERENCE_TYPE_CONTRACT_v4.csv')
for tn,cn,types,req in [
 ('p3_adjudication_split_member','member_object_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT','YES'),
 ('p3_adjudication_unresolved_boundary','left_object_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT|CANDIDATE_FAMILY|CANONICAL_FAMILY','YES'),
 ('p3_adjudication_unresolved_boundary','right_object_id','IMPORTED_SOURCE_LOCAL_LINEAGE|LINEAGE_SEGMENT|CANDIDATE_FAMILY|CANONICAL_FAMILY','YES')]:
    if not any(r['table_name']==tn and r['column_name']==cn for r in refs): refs.append({'table_name':tn,'column_name':cn,'allowed_object_types':types,'required':req})
write_csv(S46/'P3_OBJECT_REFERENCE_TYPE_CONTRACT_v4.csv',refs,['table_name','column_name','allowed_object_types','required'])

bindings=read_csv(S46/'P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v4.csv')
def ensure_binding(t,c,d,req='YES'):
    if not any(r['table_name']==t and r['column_name']==c for r in bindings): bindings.append({'table_name':t,'column_name':c,'vocabulary_domain':d,'enforcement':'DDL_CHECK_AND_OR_MIGRATION_TRIGGER','required':req})
ensure_binding('p3_adjudication_split_member','split_side','split_side')
ensure_binding('p3_adjudication_unresolved_boundary','status','closure_status')
write_csv(S46/'P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v4.csv',bindings,['table_name','column_name','vocabulary_domain','enforcement','required'])

# Add the one genuinely new finite vocabulary introduced by normalized split persistence.
voc=read_csv(S46/'P3_CONTROLLED_VOCABULARIES_v4.csv')
for code,label,definition in [('LEFT','Left split side','First governed side of a split point.'),('RIGHT','Right split side','Second governed side of a split point.')]:
    if not any(r['vocabulary_domain']=='split_side' and r['code']==code for r in voc): voc.append({'vocabulary_domain':'split_side','code':code,'label':label,'definition':definition,'authority_effect':'STRUCTURAL_DECISION_ONLY','terminal':'NO','deprecated':'NO'})
write_csv(S46/'P3_CONTROLLED_VOCABULARIES_v4.csv',voc,['vocabulary_domain','code','label','definition','authority_effect','terminal','deprecated'])

# Plan and algorithms: eliminate stale contract references and state the exact release-scoped vocabulary rule.
plan_path=S46/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v4_20260731.md'; plan=plan_path.read_text()
plan=plan.replace('P3_IDENTITY_KEY_SPEC_v3.csv','P3_IDENTITY_KEY_SPEC_v4.csv').replace('P3_OBJECT_REFERENCE_TYPE_CONTRACT_v3.csv','P3_OBJECT_REFERENCE_TYPE_CONTRACT_v4.csv')
plan += """

## 42.7 Final executable-joint closure

The independent verifier must compare every schema ID pattern to `P3_IDENTITY_KEY_SPEC_v4.csv`; validate candidate and variant revision ordinals; persist split points and unresolved boundaries outside packet JSON; enforce hyperedge type, participant role, authority effect, and deferred cardinality; and validate vocabulary codes against the complete snapshot for the authority release being loaded. `P3_CANONICAL_SERIALIZATION_CONTRACT_v4.json` is the sole hash/derived-ID serialization contract. These are existing P3 requirements made executable, not new architecture.
"""
plan_path.write_text(plan)
alg_path=S46/'algorithms/P3_ALGORITHMS_AND_PSEUDOCODE_v4.md'; alg=alg_path.read_text()
alg += """

## W. Exact canonical serialization and revision allocation
Use `P3_CANONICAL_SERIALIZATION_CONTRACT_v4.json` and its fixed vectors. Reject floats, duplicate normalized set members, unsupported Unicode, absent required identity keys, and prefix/full-hash collisions. Candidate and variant revisions store explicit ordinals; split points and unresolved boundaries are normalized decision children rather than packet-only prose.
"""
alg_path.write_text(alg)

# Extend gates/tests only for the concrete corrections above.
gates=read_csv(S46/'validation/P3_ACCEPTANCE_GATES_v4.csv')
for gid,req in [
 ('P3G-064','Every content-addressed JSON schema ID pattern agrees with the identity registry; response/structural references and hyperedges are not exempt.'),
 ('P3G-065','Candidate/variant/adjudication revision ordinals and split/unresolved decision children are persisted and reconstructible.'),
 ('P3G-066','Identity, release-scoped vocabulary, hyperedge type/role/effect/cardinality, collision orientation, and symmetric endpoint ordering are executable contract checks.'),
 ('P3G-067','Canonical serialization has a single machine-readable contract and fixed vectors; no stale v3 contract references remain in governing v4 files.')]:
    if not any(r['gate_id']==gid for r in gates): gates.append({'gate_id':gid,'phase':'PLAN','severity':'FATAL','requirement':req})
write_csv(S46/'validation/P3_ACCEPTANCE_GATES_v4.csv',gates,['gate_id','phase','severity','requirement'])
tests=read_csv(S46/'validation/P3_TEST_AND_MUTATION_PLAN_v4.csv')
for tid,cl,definition in [
 ('P3T-059','property','Every content-addressed schema and example obeys the identity-pattern registry.'),
 ('P3T-060','mutation','Wrong content-hash prefix, revision ordinal, or inherited upstream ID is rejected.'),
 ('P3T-061','mutation','Wrong hyperedge role, object type, authority effect, or role cardinality is rejected.'),
 ('P3T-062','mutation','Split/hierarchy/blocked decisions without their required normalized child records fail status-specific validation.'),
 ('P3T-063','property','Canonical serialization fixed vectors reproduce equivalent hashes and reject duplicate set members/floats.')]:
    if not any(r['test_id']==tid for r in tests): tests.append({'test_id':tid,'test_class':cl,'required':'YES','test_definition':definition})
write_csv(S46/'validation/P3_TEST_AND_MUTATION_PLAN_v4.csv',tests,['test_id','test_class','required','test_definition'])

# Decision schemas carry the adjudication ordinal used by the identity contract.
for name in ['adjudication_decision.schema.json','adjudication_decision_draft.schema.json']:
    s=load_schema(name)
    s['properties']['decision_ordinal']={'type':'integer','minimum':1}
    if 'decision_ordinal' not in s['required']: s['required'].insert(s['required'].index('candidate_revision_id')+1,'decision_ordinal')
    save_schema(name,s)

# Normalize delivered example/template identities to the final schema contract.
for p in (S46/'adjudication').glob('*.json'):
    obj=json.loads(p.read_text())
    def walk_ids(x):
        if isinstance(x,dict):
            for k,v in list(x.items()):
                if isinstance(v,str):
                    v=v.replace('P3SIG-000001','P3SIG-0123456789abcdef').replace('P3SIG-000002','P3SIG-fedcba9876543210')
                    v=v.replace('P3RCR-000001','P3RCR-0123456789abcdef').replace('P3RCR-000002','P3RCR-fedcba9876543210')
                    v=v.replace('P3SCR-000001','P3SCR-0123456789abcdef').replace('P3SCR-000002','P3SCR-fedcba9876543210')
                    v=v.replace('P3HYP-000001','P3HYP-0123456789abcdef')
                    x[k]=v
                else: walk_ids(v)
        elif isinstance(x,list):
            for v in x: walk_ids(v)
    walk_ids(obj)
    if p.name=='P3_CANDIDATE_PACKET_TEMPLATE_v4.json':
        obj['candidate_family']['revision_number']=1
        obj['decision_form'].setdefault('decision_ordinal',1)
        obj['decision_form'].setdefault('split_points',[])
    else:
        obj.setdefault('decision_ordinal',1)
        obj.setdefault('split_points',[])
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

# The v24 section must prove it inherited the substantive v23 payload unchanged.
mutable_roots={'MASTER_HANDOFF.md','README_FIRST.md','VALIDATION.json','PACKAGE_INDEX.csv','SHA256SUMS.csv'}
inherited=[]
for p in sorted(SRCROOT.rglob('*')):
    if not p.is_file(): continue
    rel=p.relative_to(SRCROOT)
    if rel.parts[0]=='00_START_HERE' or rel.name in mutable_roots: continue
    inherited.append({'relative_path':str(rel),'bytes':p.stat().st_size,'sha256':sha(p)})
write_csv(S46/'validation/INHERITED_V23_PAYLOAD_HASHES.csv',inherited,['relative_path','bytes','sha256'])
(S46/'ASSEMBLY_PROVENANCE_v24.md').write_text(f'''# Assembly provenance v24

- Accepted source tree: `{SRCROOT}`
- Accepted source archive: `/mnt/data/Rawlsing_J_Family_Authority_Strategy_Handoff_v23_20260731.zip`
- Source archive SHA-256: `6952a503a9f90f24d4961fd10a949d78129abe8898c22def1918c00ff84ffd4c`
- Builder: `validation/build_handoff_v24.py`
- Build rule: delete any prior v24 build tree, copy the accepted v23 extraction in full, create section 46, then regenerate mutable restart controls and package manifests.
- Inherited substantive payload proof: `validation/INHERITED_V23_PAYLOAD_HASHES.csv`
- Live database or repository writes: none.
''')

# Tighten known cross-object ID references throughout the schema set.
field_patterns={
 'candidate_family_id':'^P3CAND-[0-9]{6}$','candidate_revision_id':'^P3CANDREV-[0-9]{6}-R[0-9]{4}$',
 'canonical_family_id':'^JFAM-[0-9]{6}$','family_revision_id':'^JFAMREV-[0-9]{6}-R[0-9]{4}$',
 'canonical_signature_id':'^P3SIG-[0-9a-f]{16}$','signature_id':'^P3SIG-[0-9a-f]{16}$',
 'variant_id':'^P3VAR-[0-9]{6}$','variant_revision_id':'^P3VARREV-[0-9]{6}-R[0-9]{4}$',
 'exclusion_id':'^P3EXC-[0-9]{6}$','adjudication_id':'^P3ADJ-[0-9]{6}$',
 'resolution_adjudication_id':'^P3ADJ-[0-9]{6}$','supersedes_adjudication_id':'^P3ADJ-[0-9]{6}$','created_by_adjudication_id':'^P3ADJ-[0-9]{6}$',
 'pair_fact_id':'^P3PF-[0-9a-f]{16}$','direct_pair_fact_id':'^P3PF-[0-9a-f]{16}$',
 'collision_id':'^P3COL-[0-9a-f]{16}$','closure_obligation_id':'^P3CLOSE-[0-9a-f]{16}$','obligation_id':'^P3CLOSE-[0-9a-f]{16}$',
 'component_id':'^P3COMP-[0-9a-f]{16}$','hyperedge_id':'^P3HYP-[0-9a-f]{16}$','dependency_id':'^P3DEP-[0-9a-f]{16}$',
 'doctrine_delta_id':'^P3DOC-[0-9]{5}$','genealogy_id':'^P3GEN-[0-9]{6}$',
 'authority_release_id':'^P3-AUTHORITY-[0-9]{4}-[0-9]{2}-[0-9]{2}-R[0-9]+$',
 'created_release_id':'^P3-AUTHORITY-[0-9]{4}-[0-9]{2}-[0-9]{2}-R[0-9]+$',
 'retired_release_id':'^P3-AUTHORITY-[0-9]{4}-[0-9]{2}-[0-9]{2}-R[0-9]+$'
}
def tighten_refs(x):
    if isinstance(x,dict):
        props=x.get('properties')
        if isinstance(props,dict):
            for k,v in props.items():
                if k in field_patterns and isinstance(v,dict):
                    pat=field_patterns[k]
                    typ=v.get('type')
                    if typ=='string': props[k]={'type':'string','pattern':pat}
                    elif isinstance(typ,list) and 'null' in typ: props[k]={'anyOf':[{'type':'string','pattern':pat},{'type':'null'}]}
                    elif 'anyOf' in v:
                        for alt in v['anyOf']:
                            if alt.get('type')=='string': alt['pattern']=pat
                tighten_refs(v)
        for k,v in x.items():
            if v is not props: tighten_refs(v)
    elif isinstance(x,list):
        for v in x:tighten_refs(v)
for p in schema_dir.glob('*.json'):
    s=json.loads(p.read_text()); tighten_refs(s); save_schema(p.name,s)

# Object-registry file validation mirrors the database identity contract.
s=load_schema('object_registry.schema.json')
s.setdefault('allOf',[]).extend([
 {'if':{'properties':{'identity_strategy':{'const':'CONTENT_ADDRESSED_DERIVED_ID'}},'required':['identity_strategy']},'then':{'required':['content_hash'],'properties':{'content_hash':{'type':'string','pattern':'^[0-9a-f]{64}$'}}}},
 {'if':{'properties':{'identity_strategy':{'const':'INHERITED_UPSTREAM_ID'}},'required':['identity_strategy']},'then':{'properties':{'content_hash':{'type':'null'}}}}
])
save_schema('object_registry.schema.json',s)

# Final DDL corrections: rejected decisions cannot carry canonical propositions; trigger return is operation-safe.
ddl_path=S46/'sql/p3_postgresql_compatible_ddl_v4.sql'; ddl=ddl_path.read_text()
ddl=ddl.replace("decision_status NOT IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS') AND canonical_family_id IS NULL)","decision_status NOT IN ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS') AND canonical_family_id IS NULL AND canonical_proposition IS NULL)")
ddl=ddl.replace("RETURN COALESCE(NEW,OLD);\nEND; $$ LANGUAGE plpgsql;","IF TG_OP='DELETE' THEN RETURN OLD; ELSE RETURN NEW; END IF;\nEND; $$ LANGUAGE plpgsql;")
ddl_path.write_text(ddl)

# Add the remaining bounded release checks.
val_path=S46/'sql/P3_DDL_VALIDATION_QUERIES_v4.sql'; val=val_path.read_text()
val += """
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q35_split_points_complete FROM p3_adjudication_split_point s WHERE NOT EXISTS (SELECT 1 FROM p3_adjudication_split_member m WHERE m.adjudication_id=s.adjudication_id AND m.split_ordinal=s.split_ordinal AND m.split_side='LEFT') OR NOT EXISTS (SELECT 1 FROM p3_adjudication_split_member m WHERE m.adjudication_id=s.adjudication_id AND m.split_ordinal=s.split_ordinal AND m.split_side='RIGHT') OR EXISTS (SELECT 1 FROM p3_adjudication_split_member l JOIN p3_adjudication_split_member r USING(adjudication_id,split_ordinal,member_object_id) WHERE l.adjudication_id=s.adjudication_id AND l.split_ordinal=s.split_ordinal AND l.split_side='LEFT' AND r.split_side='RIGHT');
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q36_lineage_disposition_refs FROM p3_lineage_disposition d WHERE (d.disposition_status='CANDIDATE_MEMBER' AND (d.candidate_family_id IS NULL OR d.canonical_family_id IS NOT NULL)) OR (d.disposition_status='CANONICAL_MEMBER' AND (d.canonical_family_id IS NULL OR d.candidate_family_id IS NOT NULL)) OR (d.disposition_status NOT IN ('CANDIDATE_MEMBER','CANONICAL_MEMBER') AND (d.candidate_family_id IS NOT NULL OR d.canonical_family_id IS NOT NULL));
"""
val_path.write_text(val)

# ---------- Schema registry ----------
sreg=[]
for p in sorted(schema_dir.glob('*.json')):
    s=json.loads(p.read_text()); refs=[]
    def walk(x):
        if isinstance(x,dict):
            if '$ref' in x: refs.append(x['$ref'])
            for v in x.values():walk(v)
        elif isinstance(x,list):
            for v in x:walk(v)
    walk(s)
    sreg.append({'schema_file':str(p.relative_to(S46)),'schema_id':s['$id'],'sha256':sha(p),'references_json':json.dumps(sorted(set(refs)))})
write_csv(S46/'P3_JSON_SCHEMA_REGISTRY_v4.csv',sreg,['schema_file','schema_id','sha256','references_json'])

# ---------- Logical DDL schema dictionary from parser ----------
def parse_tables(sql):
    tables={}
    for m in re.finditer(r'CREATE TABLE\s+([A-Za-z0-9_]+)\s*\(',sql,re.I):
        name=m.group(1);start=m.end();depth=1;i=start;ins=False
        while i<len(sql) and depth:
            ch=sql[i]
            if ch=="'":
                if ins and i+1<len(sql) and sql[i+1]=="'":i+=2;continue
                ins=not ins
            elif not ins:
                if ch=='(':depth+=1
                elif ch==')':depth-=1
            i+=1
        tables[name]=sql[start:i-1]
    return tables
def split_top(body):
    out=[];buf='';d=0;ins=False;i=0
    while i<len(body):
        ch=body[i]
        if ch=="'":
            if ins and i+1<len(body) and body[i+1]=="'":buf+=ch+body[i+1];i+=2;continue
            ins=not ins;buf+=ch
        elif not ins and ch=='(':d+=1;buf+=ch
        elif not ins and ch==')':d-=1;buf+=ch
        elif not ins and ch==',' and d==0:out.append(buf.strip());buf=''
        else:buf+=ch
        i+=1
    if buf.strip():out.append(buf.strip())
    return out
tabs=parse_tables(ddl); sd=[]
for t,b in tabs.items():
    for part in split_top(b):
        if re.match(r'^(PRIMARY|FOREIGN|UNIQUE|CHECK|CONSTRAINT)\b',part,re.I):continue
        m=re.match(r'(\w+)\s+(.+)',part,re.S)
        if not m:continue
        c,rest=m.group(1),m.group(2)
        typ=re.split(r'\s+(?:NOT\s+NULL|NULL|DEFAULT|CHECK|PRIMARY|REFERENCES|UNIQUE)\b',rest,maxsplit=1,flags=re.I)[0].strip()
        req='YES' if re.search(r'\bNOT\s+NULL\b',rest,re.I) or re.search(r'\bPRIMARY\s+KEY\b',rest,re.I) else 'NO'
        key='PRIMARY' if re.search(r'\bPRIMARY\s+KEY\b',rest,re.I) else ('FOREIGN' if 'REFERENCES ' in rest.upper() else 'NONE')
        ref=''
        rm=re.search(r'REFERENCES\s+(\w+)\s*\((\w+)\)',rest,re.I)
        if rm:ref=f'{rm.group(1)}.{rm.group(2)}'
        sd.append({'table_or_artifact':t,'field':c,'logical_type':typ,'required':req,'key_role':key,'definition':f'P3 v4 logical DDL column {t}.{c}.','references':ref})
write_csv(S46/'P3_SCHEMA_DICTIONARY_v4.csv',sd,['table_or_artifact','field','logical_type','required','key_role','definition','references'])

# ---------- Update object types in vocab after identity spec ----------
# rewrite object_type domain to exactly identity object types
voc=read_csv(S46/'P3_CONTROLLED_VOCABULARIES_v4.csv')
identity_types={r['object_type'] for r in read_csv(S46/'P3_IDENTITY_KEY_SPEC_v4.csv')}
olddefs={r['code']:r for r in voc if r['vocabulary_domain']=='object_type'}
voc=[r for r in voc if r['vocabulary_domain']!='object_type']
for code in sorted(identity_types):
    r=olddefs.get(code,{'vocabulary_domain':'object_type','code':code,'label':code.replace('_',' ').title(),'definition':'Registry-backed P3 object type.','authority_effect':'IDENTITY_ONLY','terminal':'NO','deprecated':'NO'})
    voc.append(r)
voc=sorted(voc,key=lambda r:(r['vocabulary_domain'],r['code']))
write_csv(S46/'P3_CONTROLLED_VOCABULARIES_v4.csv',voc,['vocabulary_domain','code','label','definition','authority_effect','terminal','deprecated'])

# ---------- Bounded audit report ----------
report='''# Rawlsing P3 Third Bounded Implementation-Readiness Audit\n\n## Scope lock\n\nThis pass did not reopen P3 ontology, add a DBMS, create visualization infrastructure, or design speculative downstream machinery. It tested only whether Plan v3 contained improvised, scaffolded, undeveloped, contradictory, or unenforceable surfaces that would force rework during P3A or P6.\n\n## Verdict\n\nThe core family doctrine and P2-to-P3 authority model remained sound. Ten implementation defects remained and required correction before execution. Plan v4 closes them and is the frozen P3A baseline.\n\n## Corrected defects\n\n1. **Artifact lifecycle was ambiguous.** The catalog mixed delivered files with future outputs and contained stale or nonexistent paths. V4 adds explicit delivery states, exact paths, producing phases, and governing contracts.\n2. **Identity doctrine was incomplete.** Nine rows attempted to govern twenty-five registry-backed object types, while pair-fact schema IDs contradicted their content-addressed allocation rule. V4 supplies one identity strategy, key, allocation rule, and ID pattern for every registry object type.\n3. **Associative rows were misclassified as registry objects.** Evidence/source junction rows are now governed as composite-key rows rather than invented object identities.\n4. **Polymorphic reference coverage was incomplete.** Component, collision, closure, variant, exclusion, adjudication, response, and structural-context references now have explicit allowed object types.\n5. **Hyperedge membership was free-form.** V4 binds the six permitted hyperedge types to named participant roles, object types, cardinalities, and authority-effect ceilings.\n6. **Schemas still had unfinished holes.** Closure-obligation type was an unconstrained string; content-addressed ID patterns conflicted with the identity plan; candidate pair-count summaries omitted `DIRECT_UNRESOLVED`. These are repaired.\n7. **Exclusion and variant doctrine contradicted itself.** V4 requires rule-based exclusions for every accepted family and named exclusions only when rejected near-neighbors actually exist. Variants are required only when governed variation exists.\n8. **The migration file was openly a non-executable skeleton.** It is removed. V4 supplies an explicit live-installation blocking contract rather than pretending an installer exists without a designated repository, DSN, roles, schema map, backup target, or write authorization.\n9. **Database enforcement was described but not implemented in the logical contract.** V4 adds contract tables and trigger functions for vocabulary codes, object types, append-only history, candidate/release lifecycle events, and promotion pointers, plus validation queries for their installation.\n10. **The execution state was stale.** Plan lock, execution sequence, artifact catalog, and exact resume point now agree on Plan v4 and `P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION`; the P3A acceptance handoff is v25, because v24 is this readiness lock.\n\n## Stop rule\n\nNo additional architecture review is authorized before P3A. Reopening requires a concrete execution contradiction, failed invariant, or unrepresentable upstream/downstream artifact.\n'''
report += '''

## Independent-verifier findings after the initial ten corrections

The first corrected build was not released. An independent cross-contract pass found nine further executable-joint defects: stale inherited validation returns, non-reproducible root assembly, four mismatched content-ID schemas, missing revision/decision ordinals, packet-only split and unresolved structures, non-release-scoped vocabulary checks, missing identity and hyperedge triggers, incomplete endpoint/orientation enforcement, and an underspecified canonical serializer. All were corrected before v24 release. No new conceptual layer was introduced.

## Final rendered-document findings

The release gate caught two remaining stale presentation labels before packaging: the governing plan body still declared `Plan version: v3`, and inherited reference-document headers/footers still named the v23/v3 plans and the prior audit. The body metadata, headers, footers, source Markdown, assembly builder, and verifier were corrected. New fatal checks now require v24/v4 labels to agree across the machine-readable and rendered governing documents. These were release-identity defects, not new architecture.

## Final assembly reproducibility finding

The release-gate rebuild also exposed one hidden external dependency: the delivered builder copied `/mnt/data/build_v24_bounded_review.py` back into the handoff, so rerunning it could overwrite the corrected builder with an older external file. V4 now snapshots its own source before rebuilding the root, writes that exact source into the rebuilt package, and generates the whole-tree auditor itself. A clean rebuild from the accepted v23 extraction passed its pre-release verifier and reproduced all 82 substantive non-document contract files byte-for-byte.
'''
(S46/'P3_PLAN_THIRD_BOUNDED_IMPLEMENTATION_READINESS_AUDIT.md').write_text(report)
(S46/'TASK_RETURN.md').write_text(report)
(S46/'README_FIRST.md').write_text('# Section 46 - governing P3 plan v4\n\nRead the v4 plan, bounded audit, plan lock, execution sequence, artifact catalog, identity/type contracts, schemas, DDL, gates, and tests. Section 46 supersedes sections 43-45 for implementation. P3 execution has not started.\n')
(S46/'SUPERSEDES_SECTIONS_43_45.md').write_text('# Supersession\n\nSection 46 Plan v4 and its machine contracts supersede sections 43, 44, and 45 for P3 implementation. Earlier sections remain historical provenance and audit evidence.\n')
(S46/'ASSEMBLY_PROVENANCE_v24.md').write_text('# Assembly provenance v24\n\nBuilt from the byte-verified v23 outer archive by `validation/build_handoff_v24.py`. The bounded review changed only root restart/release controls and added section 46. P2 and earlier substantive P3 planning payloads remain inherited and hash-locked.\n')

# ---------- Live verifier v24 ----------
verify=r'''#!/usr/bin/env python3
from __future__ import annotations
import csv,json,re,hashlib,pathlib,sys,yaml
from jsonschema import Draft202012Validator, RefResolver
ROOT=pathlib.Path(sys.argv[1]).resolve(); SEC=ROOT/'46_P3_PLAN_THIRD_BOUNDED_IMPLEMENTATION_READINESS_LOCK'
checks=[]
def ck(name,cond,detail=''):
    checks.append((name,bool(cond),detail)); print(('PASS' if cond else 'FAIL'),name,detail)
def rc(p):
    with open(p,newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def sh(p):
    h=hashlib.sha256();h.update(pathlib.Path(p).read_bytes());return h.hexdigest()
# inherited verifier
import subprocess
p=subprocess.run([sys.executable,str(ROOT/'45_P3_PLAN_SECOND_ACCEPTANCE_AUDIT_AND_HARDENING/validation/verify_handoff_v23.py'),str(ROOT)],capture_output=True,text=True)
ck('inherited_v23_118',p.returncode==0 and '"checks_passed": 118' in p.stdout,p.returncode)
# delivered artifact catalog closure
cat=rc(SEC/'P3_ARTIFACT_CATALOG_v4.csv')
for r in cat:
    if r['delivery_state'].startswith('DELIVERED'):
        ck('delivered_'+re.sub(r'\W+','_',r['artifact']), (SEC/r['artifact']).is_file(),r['artifact'])
ck('no_catalog_duplicate_paths',len(cat)==len({r['artifact'] for r in cat}),len(cat))
# no operative unfinished markers. Negative test descriptions may name marker tokens.
bad=[]
markers={'TODO','TBD','FIXME','PLACEHOLDER'}
for pth in SEC.rglob('*'):
    if not pth.is_file(): continue
    rel=str(pth.relative_to(SEC))
    if any(m in pth.name.upper() for m in markers|{'SKELETON'}): bad.append((rel,'filename'))
    if pth.suffix.lower()=='.csv':
        try:
            for row in rc(pth):
                for k,v in row.items():
                    if str(v).strip().upper() in markers: bad.append((rel,k))
        except Exception: pass
    elif pth.suffix.lower() in {'.md','.sql','.yaml','.json','.txt'}:
        for i,line in enumerate(pth.read_text(errors='ignore').splitlines(),1):
            if re.match(r'^\s*(TODO|TBD|FIXME|PLACEHOLDER)(?:\b|:)',line,re.I): bad.append((rel,i))
ck('no_unfinished_markers',not bad,bad[:5])
# identity coverage
voc=rc(SEC/'P3_CONTROLLED_VOCABULARIES_v4.csv'); obj={r['code'] for r in voc if r['vocabulary_domain']=='object_type'}
ids=rc(SEC/'P3_IDENTITY_KEY_SPEC_v4.csv'); idtypes={r['object_type'] for r in ids}
ck('identity_covers_object_types',obj==idtypes,(len(obj),len(idtypes),sorted(obj-idtypes),sorted(idtypes-obj)))
ck('identity_unique',len(ids)==len(idtypes),len(ids))
# schemas resolve and patterns agree
reg=rc(SEC/'P3_JSON_SCHEMA_REGISTRY_v4.csv'); store={}
for r in reg:
    s=json.loads((SEC/r['schema_file']).read_text());store[s['$id']]=s;ck('schema_hash_'+pathlib.Path(r['schema_file']).stem,sh(SEC/r['schema_file'])==r['sha256'])
for sid,s in store.items(): Draft202012Validator.check_schema(s)
for sid,s in store.items():
    RefResolver.from_schema(s,store=store)
ck('schemas_valid',len(store)>=36,len(store))
# examples
for f,sid in [('adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v4.json','candidate_packet.schema.json'),('adjudication/P3_ADJUDICATION_DECISION_DRAFT_TEMPLATE_v4.json','adjudication_decision_draft.schema.json'),('adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v4.json','adjudication_decision.schema.json')]:
    inst=json.loads((SEC/f).read_text());sch=store['https://rawlsing.local/schemas/p3/v4/'+sid];errs=list(Draft202012Validator(sch,resolver=RefResolver.from_schema(sch,store=store)).iter_errors(inst));ck('example_'+pathlib.Path(f).stem,not errs,[e.message for e in errs[:2]])
# pair IDs and direct unresolved count
pf=store['https://rawlsing.local/schemas/p3/v4/pair_fact_bundle.schema.json'];ck('pair_fact_hex_pattern',pf['properties']['pair_fact_id']['pattern']=='^P3PF-[0-9a-f]{16}$')
cf=store['https://rawlsing.local/schemas/p3/v4/candidate_family.schema.json'];ipc=cf['properties']['internal_pair_counts'];ck('direct_unresolved_count','direct_unresolved' in ipc['required'])
co=store['https://rawlsing.local/schemas/p3/v4/closure_obligation.schema.json'];ck('closure_type_enum','enum' in co['properties']['obligation_type'])
# object refs and hyperedge roles
refs=rc(SEC/'P3_OBJECT_REFERENCE_TYPE_CONTRACT_v4.csv');ck('object_ref_nontrivial',len(refs)>=24,len(refs))
hr=rc(SEC/'P3_HYPEREDGE_ROLE_TYPE_CONTRACT_v4.csv');ck('all_six_hyperedges',len({r['hyperedge_type'] for r in hr})==6,len(hr))
ck('hyperedge_roles_nonblank',all(r['participant_role'] and r['allowed_object_types'] for r in hr))
# DDL enforcement present
ddl=(SEC/'sql/p3_postgresql_compatible_ddl_v4.sql').read_text()
for token in ['p3_identity_key_contract','p3_hyperedge_role_type_contract','p3_enforce_object_reference_type','p3_forbid_update_delete','p3_validate_candidate_status_event','p3_validate_release_status_event','p3_validate_promotion_pointer','p3_install_contract_triggers']:
    ck('ddl_'+token,token in ddl)
ck('ddl_rollback',ddl.rstrip().endswith('ROLLBACK;'))
# no migration skeleton, explicit block
ck('no_migration_skeleton',not list(SEC.rglob('*SKELETON*')))
block=json.loads((SEC/'release/P3_LIVE_INSTALLATION_BLOCKING_CONTRACT_v4.json').read_text());ck('installation_blocked_honestly',block['status'].startswith('BLOCKED_') and block['not_a_migration'])
# doctrine/version alignment
plan=(SEC/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v4_20260731.md').read_text();lock=json.loads((SEC/'P3_PLAN_LOCK_v4.json').read_text());seq=yaml.safe_load((SEC/'P3_EXECUTION_SEQUENCE_v4.yaml').read_text())
ck('version_alignment',lock['plan_version']=='v4' and seq['next_execution_point']=='P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION' and '`P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION`' in plan)
ck('exclusion_doctrine', (('named exclusions are required when actual rejected near-neighbors exist' in plan.lower()) or ('named exclusions are mandatory whenever there are actually rejected near-neighbors' in plan.lower())) and 'every accepted family has named and rule-based exclusions' not in plan.lower())
# root controls
state=json.loads((ROOT/'00_START_HERE/CURRENT_STATE.json').read_text());ck('root_state_v24',state['handoff_version']=='v24' and state['next_pass']=='P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION')
ck('no_p3_execution',state.get('p3_execution_started') is False)
# package no debris
badfiles=[p for p in ROOT.rglob('*') if p.name in {'.pytest_cache','__pycache__'} or p.suffix in {'.pyc','.pyo'}];ck('no_debris',not badfiles,badfiles[:3])
# inherited v23 payload preservation
inh=rc(SEC/'validation/INHERITED_V23_PAYLOAD_HASHES.csv'); mism=[]
for r in inh:
    q=ROOT/r['relative_path']
    if not q.is_file() or q.stat().st_size!=int(r['bytes']) or sh(q)!=r['sha256']: mism.append(r['relative_path'])
ck('inherited_v23_payload_exact',not mism,(len(inh),mism[:5]))
ck('no_stale_inherited_validation',not (SEC/'validation/INHERITED_V22_PAYLOAD_HASHES.csv').exists() and not (SEC/'validation/V22_BASELINE_REVERIFICATION_RETURN.json').exists())
# every actual section file is catalogued except the self-generated section manifest
catalog_paths={r['artifact'] for r in cat}
unclassified=[str(x.relative_to(SEC)) for x in SEC.rglob('*') if x.is_file() and x.name!='SECTION_MANIFEST.csv' and str(x.relative_to(SEC)) not in catalog_paths]
ck('all_actual_artifacts_classified',not unclassified,unclassified[:5])
# all declared registry ID patterns agree with their concrete schemas
idmap={r['object_type']:r['id_pattern'] for r in ids}
schema_id_map={
 'LINEAGE_SEGMENT':('lineage_segment.schema.json','segment_id'),
 'PROPOSITION_SIGNATURE':('proposition_signature.schema.json','signature_id'),
 'RESPONSE_CONTRACT_REFERENCE':('response_contract_reference.schema.json','reference_id'),
 'STRUCTURAL_CONTEXT_REFERENCE':('structural_context_reference.schema.json','reference_id'),
 'PAIR_FACT':('pair_fact_bundle.schema.json','pair_fact_id'),
 'COLLISION':('collision_scope.schema.json','collision_id'),
 'CANDIDATE_COMPONENT':('candidate_component.schema.json','component_id'),
 'CLOSURE_OBLIGATION':('closure_obligation.schema.json','closure_obligation_id'),
 'HYPEREDGE':('hyperedge.schema.json','hyperedge_id'),
 'DEPENDENCY':('dependency_record.schema.json','dependency_id'),
 'CANDIDATE_PACKET':('candidate_packet.schema.json','packet_id'),
 'CANDIDATE_FAMILY':('candidate_family.schema.json','candidate_family_id'),
 'CANDIDATE_REVISION':('candidate_family.schema.json','revision_id'),
 'FAMILY_VARIANT':('candidate_variant.schema.json','variant_id'),
 'FAMILY_VARIANT_REVISION':('candidate_variant.schema.json','variant_revision_id'),
 'FAMILY_EXCLUSION':('family_exclusion.schema.json','exclusion_id'),
 'ADJUDICATION':('adjudication_decision.schema.json','adjudication_id'),
 'CANONICAL_FAMILY':('canonical_family.schema.json','canonical_family_id'),
 'CANONICAL_FAMILY_REVISION':('canonical_family_revision.schema.json','family_revision_id'),
 'DOCTRINE_DELTA':('doctrine_delta.schema.json','doctrine_delta_id'),
 'FAMILY_GENEALOGY':('family_genealogy.schema.json','genealogy_id')}
patbad=[]
for ot,(fn,field) in schema_id_map.items():
    got=store['https://rawlsing.local/schemas/p3/v4/'+fn]['properties'][field].get('pattern')
    exp='^'+idmap[ot]+'$'
    if got!=exp: patbad.append((ot,got,exp))
ck('schema_identity_patterns_complete',not patbad,patbad)
# candidate template closes its actual internal pair matrix and revision identity
pkt=json.loads((SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v4.json').read_text())
member_ids=pkt['candidate_family']['member_ids']; n=len(member_ids); expected=n*(n-1)//2
counts=pkt['candidate_family']['internal_pair_counts']; state_to_key={'DIRECT_POSITIVE':'direct_positive','DIRECT_COLLISION':'direct_collision','DIRECT_UNRESOLVED':'direct_unresolved','HIERARCHICAL_ONLY':'hierarchical_only','UNRULED':'unruled','SIGNATURE_CONFLICT':'signature_conflict','SIGNATURE_COMPATIBLE':'signature_compatible'}
actual={k:0 for k in state_to_key.values()}
for r in pkt['internal_pair_matrix']: actual[state_to_key[r['pair_state']]]+=1
ck('packet_pair_matrix_exact',counts['expected_pairs']==expected==len(pkt['internal_pair_matrix']) and sum(counts[k] for k in state_to_key.values())==expected and all(counts[k]==v for k,v in actual.items()),(expected,counts,actual))
rev=pkt['candidate_family']; ck('candidate_revision_ordinal_consistent',rev['revision_id']==f"P3CANDREV-{rev['candidate_family_id'].split('-')[1]}-R{rev['revision_number']:04d}")
ck('decision_ordinal_present',pkt['decision_form']['decision_ordinal']>=1 and 'split_points' in pkt['decision_form'])
# canonical serialization fixed vectors
import unicodedata
def canon(x,set_paths=frozenset(),path=''):
    if isinstance(x,float): raise ValueError('float')
    if x is None or isinstance(x,(bool,int)): return x
    if isinstance(x,str): return unicodedata.normalize('NFC',x.replace('\r\n','\n').replace('\r','\n'))
    if isinstance(x,dict): return {k:canon(x[k],set_paths,(path+'.'+k).strip('.')) for k in sorted(x)}
    if isinstance(x,list):
        vals=[canon(v,set_paths,path) for v in x]
        if path in set_paths:
            ser=[json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')) for v in vals]
            if len(ser)!=len(set(ser)): raise ValueError('duplicate')
            vals=[v for _,v in sorted(zip(ser,vals),key=lambda z:z[0])]
        return vals
    raise ValueError('unsupported')
def cbytes(x,set_paths=frozenset()): return json.dumps(canon(x,set_paths),ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
vec=json.loads((SEC/'P3_CANONICAL_SERIALIZATION_TEST_VECTORS_v4.json').read_text()); verr=[]
for v in vec['vectors']:
    try:
        paths={v['path']} if 'path' in v else set(); a=cbytes(v['a'],paths)
        if v.get('must_fail'): verr.append((v['name'],'did_not_fail'))
        elif (a==cbytes(v['b'],paths))!=v['must_match']: verr.append((v['name'],'match_mismatch'))
    except Exception:
        if not v.get('must_fail'): verr.append((v['name'],'unexpected_fail'))
ck('canonical_serialization_vectors',not verr,verr)
# DDL/schema persistence joints
for token in ['revision_number INTEGER','decision_ordinal INTEGER','p3_adjudication_split_point','p3_adjudication_split_member','p3_adjudication_unresolved_boundary','p3_enforce_identity_contract','p3_validate_hyperedge_member_type','p3_validate_hyperedge_cardinality','p3_object_registry_identity_validate','p3_hyperedge_member_cardinality']:
    ck('ddl_final_'+re.sub(r'\W+','_',token),token in ddl)
# contract table/column references actually exist in DDL (simple parser sufficient for logical contract)
def ddl_tables(sql):
    out={}
    for m in re.finditer(r'CREATE TABLE\s+(\w+)\s*\(',sql,re.I):
        name=m.group(1); i=m.end(); depth=1; ins=False
        while i<len(sql) and depth:
            c=sql[i]
            if c=="'":
                if ins and i+1<len(sql) and sql[i+1]=="'": i+=2; continue
                ins=not ins
            elif not ins:
                if c=='(': depth+=1
                elif c==')': depth-=1
            i+=1
        body=sql[m.end():i-1]; parts=[];cur='';d=0;ins=False
        for c in body+',':
            if c=="'": ins=not ins
            if not ins:
                if c=='(':d+=1
                elif c==')':d-=1
            if c==',' and d==0: parts.append(cur.strip());cur='';continue
            cur+=c
        cols=set()
        for part in parts:
            mm=re.match(r'(\w+)\s+',part)
            if mm and mm.group(1).upper() not in {'PRIMARY','FOREIGN','UNIQUE','CHECK','CONSTRAINT'}: cols.add(mm.group(1))
        out[name]=cols
    return out
dtabs=ddl_tables(ddl); contract_missing=[]
for fn in ['P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v4.csv','P3_OBJECT_REFERENCE_TYPE_CONTRACT_v4.csv']:
    for r in rc(SEC/fn):
        if r['table_name'] not in dtabs or r['column_name'] not in dtabs.get(r['table_name'],set()): contract_missing.append((fn,r['table_name'],r['column_name']))
ck('ddl_contract_columns_exist',not contract_missing,contract_missing[:10])
# governing files contain no stale v3 contract references
stale=[]
for rel in ['Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v4_20260731.md','algorithms/P3_ALGORITHMS_AND_PSEUDOCODE_v4.md','sql/P3_DDL_VALIDATION_QUERIES_v4.sql','P3_PLAN_LOCK_v4.json','P3_EXECUTION_SEQUENCE_v4.yaml']:
    txt=(SEC/rel).read_text()
    for x in ['P3_IDENTITY_KEY_SPEC_v3','P3_OBJECT_REFERENCE_TYPE_CONTRACT_v3','P3A_CONTRACT_AND_PILOT_V3_IMPLEMENTATION','v23 validator']:
        if x in txt: stale.append((rel,x))
ck('no_stale_v3_governing_references',not stale,stale)

# Governing-version labels must agree in machine-readable and rendered source text.
_plan_md=(SEC/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v4_20260731.md').read_text()
ck('plan_markdown_declares_v4', '**Plan version:** v4' in _plan_md and '**Plan version:** v3' not in _plan_md, '')
from docx import Document as _VDoc
def _all_docx_text(_path):
    _d=_VDoc(_path); _parts=[p.text for p in _d.paragraphs]
    for _s in _d.sections:
        for _c in [_s.header,_s.first_page_header,_s.even_page_header,_s.footer,_s.first_page_footer,_s.even_page_footer]:
            _parts.extend(p.text for p in _c.paragraphs)
    return '\n'.join(_parts)
_plan_doc_text=_all_docx_text(SEC/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v4_20260731.docx')
_master_doc_text=_all_docx_text(ROOT/'00_START_HERE/Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v24_20260731.docx')
_audit_doc_text=_all_docx_text(SEC/'Rawlsing_P3_Plan_Third_Bounded_Implementation_Readiness_Audit_v1_20260731.docx')
ck('governing_docx_version_labels_current', 'Plan version: v4' in _plan_doc_text and 'P3 Plan v3' not in _plan_doc_text and 'Implementation Plan v3' not in _plan_doc_text and 'Master Handoff v23' not in _master_doc_text and 'Second Acceptance Audit and Hardening' not in _audit_doc_text, '')

# Final release-return validation is activated once root validation advances beyond assembly-pending state.
_root_validation=json.loads((ROOT/'VALIDATION.json').read_text())
_release_expected=_root_validation.get('status')!='BUILD_TREE_PENDING_FINAL_RELEASE_GATE'
if _release_expected:
    _qa_path=SEC/'validation/P3_DOCUMENT_QA_RETURN_v4.json'
    _tree_path=SEC/'validation/P3_WHOLE_TREE_TYPE_AND_ARCHIVE_AUDIT_RETURN_v4.json'
    _repro_path=SEC/'validation/P3_ASSEMBLY_REPRODUCIBILITY_RETURN_v4.json'
    ck('release_return_files_present', all(p.is_file() for p in [_qa_path,_tree_path,_repro_path]), '')
    if all(p.is_file() for p in [_qa_path,_tree_path,_repro_path]):
        _qa=json.loads(_qa_path.read_text()); _tree=json.loads(_tree_path.read_text()); _repro=json.loads(_repro_path.read_text())
        ck('document_qa_return_pass', _qa.get('status')=='PASS' and _qa.get('total_pages_rendered')==34 and _qa.get('total_pages_visually_inspected')==34 and _qa.get('a11y_findings')=={'high':0,'medium':0,'low':0}, _qa)
        ck('whole_tree_audit_return_pass', _tree.get('status')=='PASS' and not _tree.get('errors') and _tree.get('recursive_archive_instances')==88 and _tree.get('unique_archive_payloads')==77 and _tree.get('cache_debris_count')==0, _tree)
        ck('assembly_reproducibility_return_pass', _repro.get('status')=='PASS' and not _repro.get('differences') and _repro.get('substantive_contract_files_compared')==_repro.get('substantive_contract_files_hash_identical') and _repro.get('clean_rebuild_verifier',{}).get('status')=='PASS', _repro)

fails=[x for x in checks if not x[1]]
print(json.dumps({'status':'PASS' if not fails else 'FAIL','checks_passed':len(checks)-len(fails),'checks_total':len(checks),'failures':[x[0] for x in fails]},indent=2))
sys.exit(1 if fails else 0)
'''
(S46/'validation/verify_handoff_v24.py').write_text(verify)
os.chmod(S46/'validation/verify_handoff_v24.py',0o755)
# copy this build script into section
(S46/'validation/build_handoff_v24.py').write_bytes(SELF_SOURCE_BYTES)
os.chmod(S46/'validation/build_handoff_v24.py',0o755)

# ---------- Update copied templates to match v4 patterns ----------
def json_replace_file(p):
    t=p.read_text();
    t=t.replace('P3PKT-000001','P3PKT-0123456789abcdef').replace('P3CANDREV-00000001','P3CANDREV-000001-R0001').replace('P3PF-00000001','P3PF-0123456789abcdef').replace('P3PF-00000002','P3PF-fedcba9876543210')
    t=t.replace('P3CLOSE-00000001','P3CLOSE-0123456789abcdef').replace('P3COL-00000001','P3COL-0123456789abcdef')
    p.write_text(t)
for p in (S46/'adjudication').glob('*.json'):json_replace_file(p)
# Candidate packet summary must enumerate all seven internal pair states.
pkt_path=S46/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v4.json'
pkt=json.loads(pkt_path.read_text())
ipc=pkt['candidate_family']['internal_pair_counts']
if 'direct_unresolved' not in ipc:
    ordered={}
    for k,v in ipc.items():
        ordered[k]=v
        if k=='direct_collision': ordered['direct_unresolved']=0
    pkt['candidate_family']['internal_pair_counts']=ordered
pkt_path.write_text(json.dumps(pkt,indent=2)+'\n')

# ---------- Root controls ----------
state=json.loads((ROOT/'00_START_HERE/CURRENT_STATE.json').read_text())
state.update({'handoff_version':'v24','p3_plan_status':'V4_LOCKED_AFTER_THIRD_BOUNDED_IMPLEMENTATION_READINESS_AUDIT','next_pass':'P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION','governing_section':'46_P3_PLAN_THIRD_BOUNDED_IMPLEMENTATION_READINESS_LOCK','document_qa_pages':None})
state['authority_boundary']='GLOBAL_P2_CLOSED; P3 PLAN V4 IMPLEMENTATION CONTRACT LOCKED; NO CANDIDATE OR CANONICAL J-FAMILY AUTHORITY YET'
(ROOT/'00_START_HERE/CURRENT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
(ROOT/'00_START_HERE/EXACT_RESUME_POINT.md').write_text('# Exact resume point\n\n`P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION`\n\nRead section 46 first. Section 46 Plan v4 supersedes sections 43-45 for implementation.\n')
(ROOT/'00_START_HERE/NEXT_CHAT_OPENING_INSTRUCTION.txt').write_text('Open the v24 cumulative handoff. Read 00_START_HERE and section 46. Resume exactly at P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION. Do not reopen the architecture absent a concrete execution contradiction or failed invariant.\n')
# Root markdown controls
master=f'''# Rawlsing J-Family Authority Strategy - Master Handoff v24\n\n## Governing status\n\nGlobal P2 is closed. P3 execution has not begun. Section 46 contains the frozen Plan v4 contract after a third bounded implementation-readiness audit.\n\n## Exact continuation\n\n`P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION`\n\n## What the third pass changed\n\nIt added no new ontology or infrastructure. It completed artifact lifecycle, identity allocation, polymorphic reference types, hyperedge roles, schema closure, exclusion/variant wording, database enforcement, append-only/lifecycle/promotion contracts, and aligned all resume/version controls. The former non-executable migration skeleton was removed and replaced by an honest live-target blocking contract.\n\n## Authority boundary\n\nNo candidate families, canonical J-families, value harmonization, respondent joins, database writes, live repository changes, or runtime installation occurred.\n'''
(ROOT/'00_START_HERE/MASTER_HANDOFF.md').write_text(master)
(ROOT/'MASTER_HANDOFF.md').write_text(master)
(ROOT/'00_START_HERE/README_FIRST.md').write_text('# Start here - v24\n\nRead CURRENT_STATE.json, EXACT_RESUME_POINT.md, MASTER_HANDOFF.md, and section 46.\n')
(ROOT/'README_FIRST.md').write_text('# Rawlsing cumulative handoff v24\n\nThe governing P3 implementation contract is section 46. P3 execution has not started.\n')

# ---------- Governing DOCX generation ----------
def pandoc_docx(src, dst, reference):
    subprocess.run(['pandoc',str(src),'--reference-doc='+str(reference),'-o',str(dst)],check=True)
plan_docx=S46/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v4_20260731.docx'
audit_docx=S46/'Rawlsing_P3_Plan_Third_Bounded_Implementation_Readiness_Audit_v1_20260731.docx'
master_docx=ROOT/'00_START_HERE/Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v24_20260731.docx'
pandoc_docx(S46/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v4_20260731.md',plan_docx,S45/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v3_20260731.docx')
pandoc_docx(S46/'P3_PLAN_THIRD_BOUNDED_IMPLEMENTATION_READINESS_AUDIT.md',audit_docx,S45/'Rawlsing_P3_Plan_Second_Acceptance_Audit_and_Hardening_Report_v1_20260731.docx')
pandoc_docx(ROOT/'MASTER_HANDOFF.md',master_docx,SRCROOT/'00_START_HERE/Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v23_20260731.docx')


# ---------- Whole-tree release auditor ----------
(S46/'validation/whole_tree_type_and_archive_audit_v24.py').write_text("from __future__ import annotations\nimport ast, csv, io, json, py_compile, sys, zipfile, hashlib\nfrom collections import Counter\nfrom pathlib import Path\ntry:\n    import yaml\nexcept Exception:\n    yaml=None\nfrom docx import Document\n\nroot=Path(sys.argv[1]).resolve()\ntry:\n    csv.field_size_limit(sys.maxsize)\nexcept OverflowError:\n    csv.field_size_limit(2**31-1)\nerrors=[]\ncounts=Counter()\nRETURN_REL=Path('46_P3_PLAN_THIRD_BOUNDED_IMPLEMENTATION_READINESS_LOCK/validation/P3_WHOLE_TREE_TYPE_AND_ARCHIVE_AUDIT_RETURN_v4.json')\nfiles=[p for p in root.rglob('*') if p.is_file() and p.relative_to(root)!=RETURN_REL]\n\ndef err(path, kind, exc):\n    errors.append({'path':str(path.relative_to(root)) if isinstance(path,Path) and path.is_relative_to(root) else str(path),'kind':kind,'error':repr(exc)})\n\nfor p in files:\n    ext=p.suffix.lower()\n    counts[ext or '<none>'] += 1\n    try:\n        if ext=='.csv':\n            with p.open('r',encoding='utf-8-sig',newline='') as f:\n                list(csv.reader(f))\n        elif ext=='.json':\n            json.loads(p.read_text(encoding='utf-8-sig'))\n        elif ext in {'.yaml','.yml'}:\n            if yaml is None: raise RuntimeError('PyYAML unavailable')\n            yaml.safe_load(p.read_text(encoding='utf-8-sig'))\n        elif ext=='.py':\n            ast.parse(p.read_text(encoding='utf-8-sig'), filename=str(p))\n        elif ext=='.docx':\n            Document(str(p))\n        elif ext=='.zip':\n            with zipfile.ZipFile(p) as z:\n                bad=z.testzip()\n                if bad: raise RuntimeError(f'bad member {bad}')\n        elif ext in {'.md','.txt','.sql'}:\n            p.read_text(encoding='utf-8-sig')\n    except Exception as e:\n        err(p,'type_parse',e)\n\n# recursively test every ZIP instance, including nested ZIP payloads\narchive_instances=0\nunique_payloads=set()\nmax_depth=0\n\ndef audit_zip_bytes(data: bytes, label: str, depth: int):\n    global archive_instances, max_depth\n    archive_instances += 1\n    max_depth=max(max_depth,depth)\n    digest=hashlib.sha256(data).hexdigest()\n    unique_payloads.add(digest)\n    try:\n        with zipfile.ZipFile(io.BytesIO(data)) as z:\n            bad=z.testzip()\n            if bad: raise RuntimeError(f'bad member {bad}')\n            for info in z.infolist():\n                if info.is_dir(): continue\n                if info.filename.lower().endswith('.zip'):\n                    audit_zip_bytes(z.read(info), label+'!'+info.filename, depth+1)\n    except Exception as e:\n        errors.append({'path':label,'kind':'recursive_zip','error':repr(e)})\n\nfor p in files:\n    if p.suffix.lower()=='.zip':\n        audit_zip_bytes(p.read_bytes(),str(p.relative_to(root)),1)\n\n# no test/cache debris\ncache=[str(p.relative_to(root)) for p in root.rglob('*') if p.name in {'__pycache__','.pytest_cache'} or p.suffix in {'.pyc','.pyo'}]\nif cache:\n    errors.append({'path':'<tree>','kind':'cache_debris','error':cache[:50]})\n\nresult={\n 'status':'PASS' if not errors else 'FAIL',\n 'root':str(root),\n 'file_count_excluding_this_return':len(files),\n 'type_counts':dict(sorted(counts.items())),\n 'recursive_archive_instances':archive_instances,\n 'unique_archive_payloads':len(unique_payloads),\n 'max_archive_depth':max_depth,\n 'cache_debris_count':len(cache),\n 'errors':errors,\n}\nprint(json.dumps(result,indent=2))\nif errors: sys.exit(1)\n")
os.chmod(S46/'validation/whole_tree_type_and_archive_audit_v24.py',0o755)

# ---------- Final artifact catalog reconciliation ----------
# Catalog all delivered governing contracts explicitly, while retaining future-output rows.
cat_path=S46/'P3_ARTIFACT_CATALOG_v4.csv'
cat=read_csv(cat_path)
by={r['artifact']:r for r in cat}
core_contracts={
 'P3_ARTIFACT_CATALOG_v4.csv':('CANONICAL_CONTRACT','Complete delivered/future artifact lifecycle catalog','P3A','YES'),
 'P3_EXECUTION_SEQUENCE_v4.yaml':('CANONICAL_CONTRACT','Exact P3A through P7 execution sequence and stop conditions','P3A','YES'),
 'P3_PLAN_LOCK_v4.json':('CANONICAL_CONTRACT','Frozen plan version, scope, and reopen conditions','P3A','YES'),
 'P3_SCHEMA_DICTIONARY_v4.csv':('CANONICAL_CONTRACT','DDL-derived table and column dictionary','P3A','YES'),
 'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v4_20260731.md':('GOVERNING_PLAN','Central governing P3 plan v4','P3A','YES'),
 'P3_PLAN_THIRD_BOUNDED_IMPLEMENTATION_READINESS_AUDIT.md':('AUDIT_REPORT','Third bounded implementation-readiness findings and corrections','P3A','YES'),
 'algorithms/P3_ALGORITHMS_AND_PSEUDOCODE_v4.md':('CANONICAL_CONTRACT','Deterministic construction and adjudication algorithms','P3A','YES'),
 'downstream/P3_DOWNSTREAM_INTERFACES_v4.md':('CANONICAL_CONTRACT','Narrative downstream authority boundaries','P3A','YES'),
 'downstream/P3_DOWNSTREAM_INTERFACE_REGISTRY_v4.csv':('CANONICAL_CONTRACT','Machine-readable downstream interface registry','P3A','YES'),
 'release/P3_AUTHORITY_RELEASE_MIGRATION_ROLLBACK_PROTOCOL_v4.md':('INSTALLATION_PROTOCOL','Release, shadow migration, promotion, and rollback protocol','P3C/P6','YES'),
 'release/P3_LIVE_INSTALLATION_BLOCKING_CONTRACT_v4.json':('INSTALLATION_BOUNDARY','Exact missing live-target facts before executable migration','P3C/P6','YES'),
 'sql/p3_postgresql_compatible_ddl_v4.sql':('CANONICAL_CONTRACT','Non-writing PostgreSQL logical target contract with enforcement functions','P3A/P6','YES'),
 'sql/P3_DDL_VALIDATION_QUERIES_v4.sql':('INSTALLATION_VALIDATION','Read-only validation queries for shadow installation','P6','YES'),
 'validation/verify_handoff_v24.py':('VALIDATOR','Deep v24 cross-contract verifier','P3A','YES'),
 'validation/whole_tree_type_and_archive_audit_v24.py':('VALIDATOR','Type-aware whole-tree parser and recursive nested-ZIP integrity auditor','P3_PLAN_LOCK','YES'),
 'validation/build_handoff_v24.py':('ASSEMBLY_PROVENANCE','Path-specific reproducible v24 section builder; not a live installer','P3A','NO'),
}
for a,(cl,fn,ph,req) in core_contracts.items():
    by[a]={'artifact':a,'class':cl,'function':fn,'first_phase':ph,'required_for_phase_close':req,'delivery_state':'DELIVERED_CONTRACT','governing_contract':'EXPLICIT_CONTRACT'}
for a,r in list(by.items()):
    if (S46/a).is_file():
        r['delivery_state']='DELIVERED_INPUT_AUDIT' if a.startswith('upstream/') else 'DELIVERED_CONTRACT'
    elif r['delivery_state'].startswith('DELIVERED'):
        r['delivery_state']='MISSING_DELIVERABLE_ERROR'
# Every actual section file is classified. Schema files are governed through the schema registry,
# but still appear here as delivered contract payloads.
for pth in sorted(S46.rglob('*')):
    if not pth.is_file(): continue
    a=str(pth.relative_to(S46))
    if a not in by:
        if a.startswith('upstream/'): cl,ds='CANONICAL_INPUT_AUDIT','DELIVERED_INPUT_AUDIT'
        elif a.startswith('validation/'): cl,ds='VALIDATION_OR_PROVENANCE','DELIVERED_CONTRACT'
        elif a.startswith('schemas/'): cl,ds='JSON_SCHEMA','DELIVERED_CONTRACT'
        else: cl,ds='CANONICAL_CONTRACT','DELIVERED_CONTRACT'
        by[a]={'artifact':a,'class':cl,'function':'Delivered governing/support artifact; exact function is defined by its schema, report, or containing registry.','first_phase':'P3A','required_for_phase_close':'YES','delivery_state':ds,'governing_contract':'EXPLICIT_CONTRACT_OR_REGISTRY'}
# Normalize the three decision-child outputs that P3A must generate.
for a,fn in [
 ('p3_adjudication_split_points.csv','Normalized split-point decisions'),
 ('p3_adjudication_split_members.csv','Exact left/right member assignments for each split point'),
 ('p3_adjudication_unresolved_boundaries.csv','Normalized fail-closed unresolved decision boundaries')]:
    by[a]={'artifact':a,'class':'CANONICAL','function':fn,'first_phase':'P3A/P3B','required_for_phase_close':'YES','delivery_state':'GENERATED_DURING_P3A','governing_contract':'DDL_AND_JSON_SCHEMA'}
# Release-gate artifacts are generated after assembly and become delivered release returns.
by['validation/P3_DOCUMENT_QA_RETURN_v4.json']={'artifact':'validation/P3_DOCUMENT_QA_RETURN_v4.json','class':'VALIDATION_RETURN','function':'Final rendered-document and accessibility return for all governing v24 documents','first_phase':'P3_PLAN_LOCK','required_for_phase_close':'YES','delivery_state':'GENERATED_DURING_RELEASE_GATE','governing_contract':'DOCX_RENDER_AND_A11Y_GATE'}
by['validation/P3_WHOLE_TREE_TYPE_AND_ARCHIVE_AUDIT_RETURN_v4.json']={'artifact':'validation/P3_WHOLE_TREE_TYPE_AND_ARCHIVE_AUDIT_RETURN_v4.json','class':'VALIDATION_RETURN','function':'Final type-aware whole-tree and recursive archive audit return','first_phase':'P3_PLAN_LOCK','required_for_phase_close':'YES','delivery_state':'GENERATED_DURING_RELEASE_GATE','governing_contract':'WHOLE_TREE_TYPE_AND_ARCHIVE_AUDIT'}
by['validation/P3_ASSEMBLY_REPRODUCIBILITY_RETURN_v4.json']={'artifact':'validation/P3_ASSEMBLY_REPRODUCIBILITY_RETURN_v4.json','class':'VALIDATION_RETURN','function':'Clean rebuild and substantive machine-contract hash-equivalence return','first_phase':'P3_PLAN_LOCK','required_for_phase_close':'YES','delivery_state':'GENERATED_DURING_RELEASE_GATE','governing_contract':'SELF_CONTAINED_ASSEMBLY_REPRODUCIBILITY_GATE'}
by['validation/V24_CUMULATIVE_VERIFIER_RETURN.json']={'artifact':'validation/V24_CUMULATIVE_VERIFIER_RETURN.json','class':'VALIDATION_RETURN','function':'Structured return from the final cumulative v24 verifier on the assembled tree','first_phase':'P3_PLAN_LOCK','required_for_phase_close':'YES','delivery_state':'GENERATED_DURING_RELEASE_GATE','governing_contract':'VERIFY_HANDOFF_V24'}
if 'validation/INHERITED_V23_PAYLOAD_HASHES.csv' in by:
    by['validation/INHERITED_V23_PAYLOAD_HASHES.csv']['function']='Hashes inherited v23 substantive payload outside superseded mutable root controls'
cat=sorted(by.values(),key=lambda r:r['artifact'])
write_csv(cat_path,cat,['artifact','class','function','first_phase','required_for_phase_close','delivery_state','governing_contract'])

# ---------- Validation placeholder; final values filled after doc/package QA ----------
validation={'handoff_version':'v24','status':'BUILD_TREE_PENDING_FINAL_RELEASE_GATE','global_p2_closed':True,'p3_plan_v4_locked':True,'p3_implementation_started':False,'canonical_j_family_authority_authored':False,'governing_section':'46_P3_PLAN_THIRD_BOUNDED_IMPLEMENTATION_READINESS_LOCK','next_pass':'P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION','bounded_review_findings_corrected':22,'live_postgresql_execution':'NOT_RUN_NO_USER_DESIGNATED_POSTGRESQL_TARGET','live_repository_modified':False}
(ROOT/'VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n')

# ---------- Section manifest (excludes itself) ----------
def section_manifest():
    rows=[]
    for p in sorted(S46.rglob('*')):
        if p.is_file() and p.name!='SECTION_MANIFEST.csv': rows.append({'relative_path':str(p.relative_to(S46)),'bytes':p.stat().st_size,'sha256':sha(p)})
    write_csv(S46/'SECTION_MANIFEST.csv',rows,['relative_path','bytes','sha256'])
section_manifest()

# Ensure v24/v4 labels in inherited reference-document headers and footers.
_replace_header_footer_labels(ROOT/'00_START_HERE/Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v24_20260731.docx', {'Master Handoff v23':'Master Handoff v24'})
_replace_header_footer_labels(S46/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v4_20260731.docx', {'Implementation Plan v3':'Implementation Plan v4','P3 Plan v3':'P3 Plan v4'})
_replace_header_footer_labels(S46/'Rawlsing_P3_Plan_Third_Bounded_Implementation_Readiness_Audit_v1_20260731.docx', {'Rawlsing P3 Plan Second Acceptance Audit and Hardening':'Rawlsing P3 Third Bounded Implementation-Readiness Audit'})

_ensure_page_field(S46/'Rawlsing_P3_Plan_Third_Bounded_Implementation_Readiness_Audit_v1_20260731.docx')
print('built section46 files',sum(1 for p in S46.rglob('*') if p.is_file()))
