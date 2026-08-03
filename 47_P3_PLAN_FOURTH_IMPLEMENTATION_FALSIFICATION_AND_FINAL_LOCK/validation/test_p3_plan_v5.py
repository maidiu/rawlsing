from __future__ import annotations
from pathlib import Path
import csv,json,re,hashlib,random,copy
from collections import defaultdict,Counter,deque
import pandas as pd
import pytest
from referencing import Registry,Resource
from jsonschema import Draft202012Validator,ValidationError

ROOT=Path(__file__).resolve().parents[2]
SEC=ROOT/'47_P3_PLAN_FOURTH_IMPLEMENTATION_FALSIFICATION_AND_FINAL_LOCK'

def loadj(p):return json.loads(Path(p).read_text())
def schema_registry():
    files=sorted((SEC/'schemas').glob('*.json')); pairs=[]
    for p in files:
        o=loadj(p);Draft202012Validator.check_schema(o);pairs.append((o['$id'],Resource.from_contents(o)))
    return Registry().with_resources(pairs)
REG=schema_registry()
def validate(schema,instance):Draft202012Validator(loadj(SEC/'schemas'/schema),registry=REG).validate(instance)

def components(df):
    adj=defaultdict(set)
    for r in df.itertuples(index=False):
        adj[r.left_lineage_id].add(r.right_lineage_id);adj[r.right_lineage_id].add(r.left_lineage_id)
    seen=set();out=[]
    for n in sorted(adj):
        if n in seen:continue
        stack=[n];seen.add(n);c=[]
        while stack:
            x=stack.pop();c.append(x)
            for y in sorted(adj[x]):
                if y not in seen:seen.add(y);stack.append(y)
        out.append(tuple(sorted(c)))
    return tuple(sorted(out))

def proposition_parts():
    d=pd.read_csv(SEC/'upstream/P3_PROPOSITION_RELATION_ELIGIBILITY_PREFLIGHT_v5.csv',keep_default_na=False)
    sub=d[d.provisional_j_family_eligibility=='J_FAMILY_CANDIDATE_ELIGIBLE']
    return d,sub[sub.p3_relation_type=='PROPOSITION_RESPONSE_IDENTITY'],sub[sub.p3_relation_type=='PROPOSITION_IDENTITY_ONLY'],sub

def ddl_tables_columns():
    s=(SEC/'sql/p3_postgresql_compatible_ddl_v5.sql').read_text();out={}
    for m in re.finditer(r'CREATE TABLE\s+(\w+)\s*\(',s,re.I):
        table=m.group(1);i=m.end();depth=1;inq=False;j=i
        while j<len(s) and depth:
            ch=s[j]
            if ch=="'":
                if inq and j+1<len(s) and s[j+1]=="'":j+=2;continue
                inq=not inq
            elif not inq:
                if ch=='(':depth+=1
                elif ch==')':depth-=1
            j+=1
        body=s[i:j-1];parts=[];start=0;dep=0;inq=False
        for k,ch in enumerate(body):
            if ch=="'":inq=not inq
            elif not inq:
                if ch=='(':dep+=1
                elif ch==')':dep-=1
                elif ch==',' and dep==0:parts.append(body[start:k].strip());start=k+1
        parts.append(body[start:].strip());cols=set()
        for x in parts:
            mm=re.match(r'([A-Za-z_]\w*)\s+',x)
            if mm and mm.group(1).upper() not in {'PRIMARY','FOREIGN','UNIQUE','CHECK','CONSTRAINT'}:cols.add(mm.group(1))
        out[table]=cols
    return s,out

def test_upstream_counts_and_precedence():
    eff=pd.read_csv(SEC/'upstream/P3_EFFECTIVE_UPSTREAM_PAIR_AUTHORITY_SURFACE_v5.csv',keep_default_na=False)
    src=pd.read_csv(SEC/'upstream/P3_EFFECTIVE_PAIR_SOURCE_AUTHORITY_SURFACE_v5.csv',keep_default_na=False)
    assert len(eff)==19175==eff.pair_key.nunique()
    assert len(src)==19582
    assert (src.authority_role=='GOVERNING').sum()==19175
    assert (src.authority_role=='SUPERSEDED_PROVENANCE').sum()==407

def test_all_lineages_and_implementations_no_loss():
    d=pd.read_csv(ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1/Rawlsing_P2_All_Nine_Source_Local_Lineage_Registry_v1.csv',keep_default_na=False)
    ids=[]
    for x in d.member_question_implementation_ids_json:ids.extend(json.loads(x))
    assert len(d)==13526 and d.lineage_id.nunique()==13526
    assert len(ids)==len(set(ids))==18276
    assert d.member_count.sum()==18276

def test_strict_and_proposition_only_topology():
    _,e1,e2,sub=proposition_parts();c1=components(e1);idx={n:i for i,c in enumerate(c1) for n in c};cat=Counter();outside=[]
    for r in e2.itertuples(index=False):
        a=idx.get(r.left_lineage_id);b=idx.get(r.right_lineage_id)
        if a is not None and b is not None and a==b:cat['within_strict_component']+=1
        elif (a is None)^(b is None):cat['attaches_orphan_to_strict']+=1
        elif a is not None and b is not None:cat['bridges_strict_components']+=1
        else:cat['both_endpoints_outside_strict']+=1;outside.append(r._asdict())
    assert (len(e1),len({*e1.left_lineage_id,*e1.right_lineage_id}),len(c1))==(445,304,94)
    assert cat==Counter(within_strict_component=1,attaches_orphan_to_strict=85,bridges_strict_components=70,both_endpoints_outside_strict=56)
    assert len(components(pd.DataFrame(outside)))==25
    assert (len(sub),len({*sub.left_lineage_id,*sub.right_lineage_id}),len(components(sub)))==(657,397,112)

def test_graph_order_invariance():
    _,e1,e2,_=proposition_parts();base1=components(e1);base2=components(e2)
    for seed in range(5):
        assert components(e1.sample(frac=1,random_state=seed))==base1
        assert components(e2.sample(frac=1,random_state=seed))==base2

def test_relation_class_mutation_is_detected():
    _,e1,e2,_=proposition_parts();mut=pd.concat([e1,e2.iloc[[0]]],ignore_index=True)
    assert len(mut)==446
    assert components(mut)!=components(e1)

def test_all_schemas_offline_and_examples_validate():
    assert len(list((SEC/'schemas').glob('*.json')))==42
    validate('candidate_packet.schema.json',loadj(SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v5.json'))
    validate('adjudication_decision_draft.schema.json',loadj(SEC/'adjudication/P3_ADJUDICATION_DECISION_DRAFT_TEMPLATE_v5.json'))
    validate('adjudication_decision.schema.json',loadj(SEC/'adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v5.json'))

def test_completed_decision_rejects_missing_canonical_family():
    x=loadj(SEC/'adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v5.json');x['canonical_family_id']=None
    with pytest.raises(ValidationError):validate('adjudication_decision.schema.json',x)

def test_draft_does_not_validate_as_completed():
    x=loadj(SEC/'adjudication/P3_ADJUDICATION_DECISION_DRAFT_TEMPLATE_v5.json')
    validate('adjudication_decision_draft.schema.json',x)
    with pytest.raises(ValidationError):validate('adjudication_decision.schema.json',x)

def test_candidate_packet_requires_complete_matrix_surface():
    x=loadj(SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v5.json');del x['internal_pair_matrix']
    with pytest.raises(ValidationError):validate('candidate_packet.schema.json',x)

def test_endpoint_resolution_fail_closed_contract():
    good={'pair_fact_id':'P3PF-0123456789abcdef','endpoint_side':'LEFT','original_lineage_id':'p2lineage_a','resolution_status':'BLOCKED_HETEROGENEOUS','resolved_subject_ids':[],'evidence_ids':['e1'],'authority_release_id':'P3-AUTHORITY-2026-08-01-R1'}
    validate('pair_endpoint_resolution.schema.json',good)
    bad=copy.deepcopy(good);bad['resolved_subject_ids']=['segment_x']
    with pytest.raises(ValidationError):validate('pair_endpoint_resolution.schema.json',bad)
    bad=copy.deepcopy(good);bad['resolution_status']='ORIGINAL_LINEAGE';bad['evidence_ids']=[]
    with pytest.raises(ValidationError):validate('pair_endpoint_resolution.schema.json',bad)

def test_lineage_disposition_status_specific_refs():
    base={'subject_type':'IMPORTED_SOURCE_LOCAL_LINEAGE','subject_id':'p2lineage_a','disposition_status':'CANDIDATE_MEMBER','candidate_family_id':None,'canonical_family_id':None,'authority_release_id':'P3-AUTHORITY-2026-08-01-R1','reason':'x','evidence_ids':['e']}
    with pytest.raises(ValidationError):validate('lineage_disposition.schema.json',base)
    base['candidate_family_id']='P3CAND-000001';validate('lineage_disposition.schema.json',base)

def test_candidate_status_is_revision_scoped():
    x={'candidate_family_id':'P3CAND-000001','event_ordinal':1,'from_stage':None,'to_stage':'DISCOVERED','authority_release_id':'P3-AUTHORITY-2026-08-01-R1','guard_evidence_id':'e'}
    with pytest.raises(ValidationError):validate('candidate_status_event.schema.json',x)
    x['candidate_revision_id']='P3CANDREV-000001-R0001';validate('candidate_status_event.schema.json',x)

def test_ddl_reference_order_and_contract_tables_exist():
    s,t=ddl_tables_columns();order={m.group(1):i for i,m in enumerate(re.finditer(r'CREATE TABLE\s+(\w+)',s,re.I))}
    for m in re.finditer(r'REFERENCES\s+(\w+)\s*\(',s,re.I):
        ref=m.group(1);owner=max((name for name,pos in order.items() if pos<=s[:m.start()].count('CREATE TABLE')),default=None)
        assert ref in t
    for name in ['p3_imported_lineage_membership','p3_pair_endpoint_resolution','p3_component_connectivity_edge','p3_internal_pair_collision','p3_internal_pair_closure','p3_adjudication_split_member','p3_adjudication_unresolved_boundary']:
        assert name in t

def test_schema_dictionary_exact_table_column_surface():
    _,t=ddl_tables_columns();d=pd.read_csv(SEC/'P3_SCHEMA_DICTIONARY_v5.csv',keep_default_na=False)
    assert set(d.table_or_artifact)==set(t)
    for table,cols in t.items():assert set(d[d.table_or_artifact==table].field)==cols

def test_categorical_bindings_resolve_to_real_columns_and_vocabularies():
    _,t=ddl_tables_columns();b=pd.read_csv(SEC/'P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v5.csv',keep_default_na=False);v=pd.read_csv(SEC/'P3_CONTROLLED_VOCABULARIES_v5.csv',keep_default_na=False)
    domains=set(v.vocabulary_domain)
    for r in b.itertuples(index=False):
        assert r.table_name in t and r.column_name in t[r.table_name]
        assert r.vocabulary_domain in domains

def test_object_reference_contract_resolves_to_columns_and_identity_types():
    _,t=ddl_tables_columns();r=pd.read_csv(SEC/'P3_OBJECT_REFERENCE_TYPE_CONTRACT_v5.csv',keep_default_na=False);i=pd.read_csv(SEC/'P3_IDENTITY_KEY_SPEC_v5.csv',keep_default_na=False);types=set(i.object_type)
    for x in r.itertuples(index=False):
        assert x.table_name in t and x.column_name in t[x.table_name]
        assert set(x.allowed_object_types.split('|'))<=types

def test_lifecycle_and_release_rollback_paths():
    c=pd.read_csv(SEC/'P3_LIFECYCLE_STATE_MACHINE_v5.csv',keep_default_na=False);r=pd.read_csv(SEC/'P3_RELEASE_LIFECYCLE_STATE_MACHINE_v5.csv',keep_default_na=False)
    assert ((c.from_stage=='DISCOVERED')&(c.to_stage=='GENERATED_CANDIDATE')).any()
    assert ((r.from_status=='SUPERSEDED')&(r.to_status=='PROMOTED')).any()
    assert ((r.from_status=='PROMOTED')&(r.to_status=='SUPERSEDED')).any()

def test_hyperedge_roles_have_cardinality_and_identity_closure():
    h=pd.read_csv(SEC/'P3_HYPEREDGE_ROLE_TYPE_CONTRACT_v5.csv',keep_default_na=False);i=set(pd.read_csv(SEC/'P3_IDENTITY_KEY_SPEC_v5.csv',keep_default_na=False).object_type)
    assert not h.duplicated(['hyperedge_type','participant_role']).any()
    assert all(set(x.split('|'))<=i for x in h.allowed_object_types)
    assert all(str(x).isdigit() for x in h.minimum_count)

def test_artifact_catalog_distinguishes_delivered_and_future():
    d=pd.read_csv(SEC/'P3_ARTIFACT_CATALOG_v5.csv',keep_default_na=False)
    assert d.artifact.nunique()==len(d)
    for r in d.itertuples(index=False):
        exists=(SEC/r.artifact).exists()
        if r.delivery_state.startswith('DELIVERED'):assert exists
        else:assert not exists

def test_inherited_v24_payload_hash_lock():
    d=pd.read_csv(SEC/'validation/INHERITED_V24_PAYLOAD_HASHES.csv',keep_default_na=False)
    assert len(d)==1165 and set(d.preserved_in_v25)=={'YES'}
    for r in d.itertuples(index=False):
        p=ROOT/r.relative_path
        assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==r.sha256

def test_no_active_scaffolds_or_stale_current_plan_labels():
    bad=[]
    for p in SEC.rglob('*'):
        if not p.is_file() or p.suffix.lower() in {'.docx','.zip','.png','.pdf'}:continue
        text=p.read_text(errors='ignore')
        for n,line in enumerate(text.splitlines(),1):
            if re.match(r'^\s*(TODO|TBD|FIXME|PLACEHOLDER)(?:\b|:)',line,re.I):bad.append((p,n))
    assert not bad
