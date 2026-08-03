from __future__ import annotations
from pathlib import Path
import copy,json,sys
import pandas as pd
import pytest
from jsonschema import Draft202012Validator,FormatChecker,ValidationError
from referencing import Registry,Resource

ROOT=Path(__file__).resolve().parents[2]
SEC=ROOT/'49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK'
sys.path.insert(0,str(SEC/'validation'))
from validate_p3_candidate_packet_v7 import validate_packet,evidence_surface
from p3_canonical_json_v7 import canonical_bytes,canonical_sha256
from static_sql_contract_check_v7 import check as sql_check

def loadj(p): return json.loads(Path(p).read_text())
def registry():
    pairs=[]
    for p in sorted((SEC/'schemas').glob('*.json')):
        o=loadj(p); Draft202012Validator.check_schema(o); pairs.append((o['$id'],Resource.from_contents(o)))
    return Registry().with_resources(pairs)
REG=registry()
def validate(name,obj): Draft202012Validator(loadj(SEC/'schemas'/name),registry=REG,format_checker=FormatChecker()).validate(obj)
def packet(): return loadj(SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v7.json')
def write_packet(tmp_path,p,name='p.json'):
    q=tmp_path/name; q.write_text(json.dumps(p)); return q
def rehash(p):
    h=canonical_sha256(evidence_surface(p)); p['evidence_bundle_hash']=h; p['candidate_family']['evidence_bundle_hash']=h; p['decision_form']['evidence_bundle_hash']=h; return p

# Inherited topology remains unchanged.
def test_upstream_counts():
    p=loadj(SEC/'upstream/P3_EXECUTION_INSTANTIATION_PREFLIGHT_RETURN_v7.json')
    assert p['effective_pair_authorities']==19175 and p['proposition_authorities']==658 and p['provisional_substantive_edges']==657
    assert p['strict']=={'edges':445,'subjects':304,'components':94,'largest_component_size':13}
    assert p['proposition_only']['edges']==212 and p['proposition_only']['seed_components']==25
    assert p['attachment_review_groups']==22 and p['pre_signature_candidate_records']==141

def test_signature_workset_bounded():
    x=pd.read_csv(SEC/'upstream/P3_SIGNATURE_WORKSET_v7.csv',keep_default_na=False)
    assert len(x)==13526 and x.lineage_id.nunique()==13526
    assert (x.signature_requirement=='FULL_P3A_SIGNATURE').sum()==399
    assert (x.signature_requirement=='P2_CONSTRAINT_EVIDENCE_PRESERVED').sum()==2897
    assert (x.signature_requirement=='DEFER_UNTIL_PROMOTED_OR_NEW_AUTHORITY').sum()==10230

def test_all_schemas_compile():
    assert len(list((SEC/'schemas').glob('*.json')))>=50

def test_packet_schema_and_semantic_fixture():
    p=packet(); validate('candidate_packet.schema.json',p)
    assert validate_packet(SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v7.json')['status']=='PASS'

def test_valid_accepted_split_and_hierarchy():
    pkt=SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v7.json'
    for f,status in [('P3_ADJUDICATION_DECISION_EXAMPLE_v7.json','ACCEPTED_CANONICAL'),('status_fixtures/VALID_SPLIT_DECISION_v7.json','SPLIT_REQUIRED'),('status_fixtures/VALID_HIERARCHY_DECISION_v7.json','HIERARCHICAL_RELATION_ONLY')]:
        assert validate_packet(pkt,SEC/'adjudication'/f)['decision_status']==status

def test_schema_date_time_format_enforced():
    d=loadj(SEC/'adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v7.json'); d['created_at']='not-a-date'
    with pytest.raises(ValidationError): validate('adjudication_decision.schema.json',d)

def test_full_evidence_hash_detects_signature_mutation(tmp_path):
    p=packet(); p['proposition_signature_matrix'][0]['fields']['target']['field_value']='military'
    # Nested content_hash deliberately left unchanged: full evidence hashing must still catch it.
    with pytest.raises(ValueError,match='full delivered evidence'): validate_packet(write_packet(tmp_path,p))

def test_origin_components_required_and_exact(tmp_path):
    p=packet(); p['origin_components'][0]['member_ids']=[p['candidate_family']['member_ids'][0],'outsider_origin_member']; rehash(p)
    with pytest.raises(ValueError,match='origin does not reconstruct'): validate_packet(write_packet(tmp_path,p))

def test_release_coherence_enforced_after_rehash(tmp_path):
    p=packet(); p['proposition_signature_matrix'][0]['authority_release_id']='P3-AUTHORITY-2026-08-01-R9'; rehash(p)
    with pytest.raises(ValueError,match='authority-release mismatch'): validate_packet(write_packet(tmp_path,p))

def test_projection_surface_includes_attachment_and_direct_only(tmp_path):
    p=packet(); p['pair_projections'].append(copy.deepcopy(p['pair_projections'][0])); p['pair_projections'][-1]['projection_id']='P3PROJ-fedcba9876543210'; rehash(p)
    with pytest.raises(ValueError,match='projection surface'): validate_packet(write_packet(tmp_path,p))

def test_candidate_variant_and_exclusion_ids_reconcile(tmp_path):
    p=packet(); p['candidate_family']['exclusion_ids']=[]; rehash(p)
    with pytest.raises(ValueError,match='exclusion_ids'): validate_packet(write_packet(tmp_path,p))

def test_rule_exclusion_promotion_cannot_fabricate_member(tmp_path):
    d=loadj(SEC/'adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v7.json'); d['exclusion_promotions'][0]['excluded_member_ids']=[packet()['candidate_family']['member_ids'][0]]
    q=tmp_path/'d.json'; q.write_text(json.dumps(d))
    with pytest.raises(ValueError,match='cannot fabricate'): validate_packet(SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v7.json',q)

def test_valid_split_was_impossible_in_v6_and_now_passes():
    assert validate_packet(SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v7.json',SEC/'adjudication/status_fixtures/VALID_SPLIT_DECISION_v7.json')['status']=='PASS'

def test_split_duplicate_member_rejected(tmp_path):
    d=loadj(SEC/'adjudication/status_fixtures/VALID_SPLIT_DECISION_v7.json'); d['split_results'][1]['member_ids']=d['split_results'][0]['member_ids']
    q=tmp_path/'d.json'; q.write_text(json.dumps(d))
    with pytest.raises(ValueError): validate_packet(SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v7.json',q)

def test_hierarchy_uses_both_endpoints_not_only_narrower():
    assert validate_packet(SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v7.json',SEC/'adjudication/status_fixtures/VALID_HIERARCHY_DECISION_v7.json')['status']=='PASS'

def test_hierarchy_cannot_smuggle_accepted_members(tmp_path):
    d=loadj(SEC/'adjudication/status_fixtures/VALID_HIERARCHY_DECISION_v7.json'); d['accepted_members']=[packet()['candidate_family']['member_ids'][0]]
    with pytest.raises(ValidationError): validate('adjudication_decision.schema.json',d)

def test_terminal_disposition_overlap_rejected(tmp_path):
    d=loadj(SEC/'adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v7.json'); d['excluded_members']=[d['accepted_members'][0]]
    q=tmp_path/'d.json';q.write_text(json.dumps(d))
    with pytest.raises(ValueError,match='multiple terminal'): validate_packet(SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v7.json',q)

def test_canonical_serialization_vectors():
    v=loadj(SEC/'P3_CANONICAL_SERIALIZATION_TEST_VECTORS_v7.json')
    assert v['contract_id']=='P3_CANONICAL_SERIALIZATION_CONTRACT_V7'
    for x in v['vectors']:
        assert canonical_bytes(x['input']).decode()==x['canonical_utf8']
        assert canonical_sha256(x['input'])==x['sha256']

def test_canonical_unicode_and_line_endings_equivalent():
    assert canonical_sha256({'x':'é'})==canonical_sha256({'x':'e\u0301'})
    assert canonical_sha256({'x':'a\nb\nc'})==canonical_sha256({'x':'a\r\nb\rc'})

def test_canonical_set_sort_and_duplicate_rejection():
    assert canonical_sha256({'member_ids':['a','b']})==canonical_sha256({'member_ids':['b','a']})
    with pytest.raises(ValueError): canonical_bytes({'member_ids':['a','a']})

def test_canonical_float_rejected():
    with pytest.raises(TypeError): canonical_bytes({'x':1.0})

def test_sql_static_checker_passes():
    r=sql_check(SEC/'sql/p3_postgresql_compatible_ddl_v7.sql',SEC/'sql/P3_DDL_VALIDATION_QUERIES_v7.sql')
    assert r['status']=='PASS',r

def test_sql_rollback_is_final():
    ddl=(SEC/'sql/p3_postgresql_compatible_ddl_v7.sql').read_text().strip()
    assert ddl.endswith('ROLLBACK;') and ddl.count('\nROLLBACK;')==1

def test_sql_projection_columns_and_no_stale_lineage_fk():
    ddl=(SEC/'sql/p3_postgresql_compatible_ddl_v7.sql').read_text()
    assert 'e.pair_fact_id' not in ddl and 'x.direct_pair_fact_id' not in ddl
    assert 'p3_lineage_disposition_candidate_family_fk' not in ddl
    assert 'origin_key CHAR(64)' in ddl and 'occurred_at TIMESTAMPTZ NOT NULL' in ddl

def test_sql_assertions_are_trigger_wired():
    ddl=(SEC/'sql/p3_postgresql_compatible_ddl_v7.sql').read_text()
    for x in ['p3_candidate_origin_revision_closure','p3_adjudication_partition_decision_closure','PERFORM p3_assert_candidate_origin(rid)','PERFORM p3_assert_split_result_partition(aid)','PERFORM p3_assert_canonical_promotion_closure(aid)']: assert x in ddl

def test_validation_queries_use_real_columns_and_codes():
    q=(SEC/'sql/P3_DDL_VALIDATION_QUERIES_v7.sql').read_text()
    for x in ['candidate_family_id IS NULL','CANDIDATE_MEMBER','HIERARCHICAL_RELATIVE','canonical_family_revision_id']: assert x not in q
    assert "membership_role='PROPOSED_MEMBER'" in q and 'JOIN p3_pair_projection pr USING(projection_id)' in q

def test_internal_pair_schema_projection_only():
    o=loadj(SEC/'schemas/internal_pair_record.schema.json')
    assert 'direct_pair_projection_id' in o['properties'] and 'direct_pair_fact_id' not in o['properties']

def test_live_install_commands_use_actual_runtime_versions():
    o=loadj(SEC/'release/P3_LIVE_INSTALLATION_BLOCKING_CONTRACT_v7.json')
    assert o['contract_id'].endswith('_V7')
    assert 'runtime_build_commands_for_v550j_v551j_v552j' in o['required_before_compilation']

def test_vocabulary_matches_ddl():
    x=pd.read_csv(SEC/'P3_CONTROLLED_VOCABULARIES_v7.csv',keep_default_na=False)
    assert ((x.vocabulary_domain=='candidate_membership_role')&(x.code=='PROPOSED_HIERARCHICAL_CONTEXT')).any()
    assert not ((x.vocabulary_domain=='lineage_p3_disposition_status')&(x.code=='CANDIDATE_MEMBER')).any()

def test_plan_signature_scope_not_reexpanded():
    import yaml
    seq=yaml.safe_load((SEC/'P3_EXECUTION_SEQUENCE_v7.yaml').read_text())
    p3a3=next(x for x in seq['phases'] if x['phase']=='P3A-3')
    joined=' '.join(p3a3['steps'])
    assert '399 proposition-incident lineages' in joined and '2,897 constraint-only lineages' in joined
