from __future__ import annotations
from pathlib import Path
import json,copy,subprocess,sys,itertools,re
import pandas as pd
import pytest
from referencing import Registry,Resource
from jsonschema import Draft202012Validator,ValidationError
ROOT=Path(__file__).resolve().parents[2];SEC=ROOT/'48_P3_PLAN_FIFTH_EXECUTION_INSTANTIATION_AUDIT_AND_LOCK'
def loadj(p):return json.loads(Path(p).read_text())
def schemas():
 pairs=[]
 for p in sorted((SEC/'schemas').glob('*.json')):
  o=loadj(p);Draft202012Validator.check_schema(o);pairs.append((o['$id'],Resource.from_contents(o)))
 return Registry().with_resources(pairs)
REG=schemas()
def validate(s,o):Draft202012Validator(loadj(SEC/'schemas'/s),registry=REG).validate(o)
def semantic(pkt,dec=None):
 from validate_p3_candidate_packet_v6 import validate_packet
 return validate_packet(pkt,dec)

def test_upstream_and_topology_counts():
 p=loadj(SEC/'upstream/P3_EXECUTION_INSTANTIATION_PREFLIGHT_RETURN_v6.json')
 assert p['effective_pair_authorities']==19175 and p['proposition_authorities']==658 and p['provisional_substantive_edges']==657
 assert p['strict']=={'edges':445,'subjects':304,'components':94,'largest_component_size':13}
 assert p['proposition_only']['edges']==212 and p['proposition_only']['seed_components']==25
 assert p['attachment_review_groups']==22 and p['pre_signature_candidate_records']==141

def test_signature_workset_bounded():
 x=pd.read_csv(SEC/'upstream/P3_SIGNATURE_WORKSET_v6.csv',keep_default_na=False)
 assert len(x)==13526 and x.lineage_id.nunique()==13526
 assert (x.signature_requirement=='FULL_P3A_SIGNATURE').sum()==399
 assert (x.signature_requirement=='P2_CONSTRAINT_EVIDENCE_PRESERVED').sum()==2897
 assert (x.candidate_boundary_priority=='YES').sum()==1884 # 399 proposition +1485 boundary
 assert (x.signature_requirement=='DEFER_UNTIL_PROMOTED_OR_NEW_AUTHORITY').sum()==10230

def test_attachment_groups_exact_and_order_invariant():
 g=pd.read_csv(SEC/'upstream/P3_ATTACHMENT_REVIEW_GROUPS_PREFLIGHT_v6.csv',keep_default_na=False)
 assert len(g)==22 and g.attachment_review_group_id.nunique()==22
 assert g.cross_boundary_pair_count.sum()==155
 assert g.candidate_origin_key.str.match(r'^[0-9a-f]{64}$').all()

def test_pair_projection_schema_blocks_blank():
 x={'projection_id':'P3PROJ-0123456789abcdef','pair_fact_id':'P3PF-0123456789abcdef','left_subject_id':'a','right_subject_id':'b','projection_basis':'SEGMENT_BINDING','evidence_ids':['e'],'authority_release_id':'P3-AUTHORITY-2026-08-01-R1'}
 validate('pair_projection.schema.json',x)
 x['evidence_ids']=[]
 with pytest.raises(ValidationError):validate('pair_projection.schema.json',x)

def test_component_connectivity_requires_projection():
 x={'component_id':'P3COMP-0123456789abcdef','projection_id':'P3PROJ-0123456789abcdef','authority_release_id':'P3-AUTHORITY-2026-08-01-R1'}
 validate('component_connectivity_edge.schema.json',x)
 x={'component_id':x['component_id'],'pair_fact_id':'P3PF-0123456789abcdef','authority_release_id':x['authority_release_id']}
 with pytest.raises(ValidationError):validate('component_connectivity_edge.schema.json',x)

def test_candidate_origins_conditional():
 p=loadj(SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v6.json')['candidate_family'];validate('candidate_family.schema.json',p)
 q=copy.deepcopy(p);q['candidate_origin_type']='ATTACHMENT_REVIEW';q['component_ids']=[];q['attachment_projection_ids']=[]
 with pytest.raises(ValidationError):validate('candidate_family.schema.json',q)
 q['attachment_projection_ids']=['P3PROJ-0123456789abcdef'];validate('candidate_family.schema.json',q)
 q['candidate_origin_type']='NONCONNECTIVE_DIAGNOSTIC_CASE'
 with pytest.raises(ValidationError):validate('candidate_family.schema.json',q)

def test_lineage_disposition_allows_overlapping_candidate_participation():
 x={'subject_id':'l','subject_type':'IMPORTED_SOURCE_LOCAL_LINEAGE','disposition_status':'CANDIDATE_PARTICIPANT','reason':'appears in base and attachment review candidates','evidence_ids':['e'],'canonical_family_id':None,'authority_release_id':'P3-AUTHORITY-2026-08-01-R1'}
 validate('lineage_disposition.schema.json',x)
 assert 'candidate_family_id' not in loadj(SEC/'schemas/lineage_disposition.schema.json')['properties']

def test_status_event_timestamp_required():
 x={'candidate_family_id':'P3CAND-000001','candidate_revision_id':'P3CANDREV-000001-R0001','event_ordinal':1,'from_stage':None,'to_stage':'DISCOVERED','guard_evidence_id':'e','authority_release_id':'P3-AUTHORITY-2026-08-01-R1'}
 with pytest.raises(ValidationError):validate('candidate_status_event.schema.json',x)
 x['occurred_at']='2026-08-01T00:00:00Z';validate('candidate_status_event.schema.json',x)

def test_schema_examples_validate():
 validate('candidate_packet.schema.json',loadj(SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v6.json'))
 validate('adjudication_decision_draft.schema.json',loadj(SEC/'adjudication/P3_ADJUDICATION_DECISION_DRAFT_TEMPLATE_v6.json'))
 validate('adjudication_decision.schema.json',loadj(SEC/'adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v6.json'))

def test_semantic_packet_validator_passes_fixture():
 assert semantic(SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v6.json')['status']=='PASS'

def mutate_packet(tmp_path,fn):
 p=loadj(SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v6.json');fn(p);q=tmp_path/'p.json';q.write_text(json.dumps(p));return q

def test_semantic_rejects_members_by_source_mismatch(tmp_path):
 q=mutate_packet(tmp_path,lambda p:p['members_by_source']['GSS'].append('outsider'))
 with pytest.raises(Exception):semantic(q)

def test_semantic_rejects_incomplete_pair_matrix(tmp_path):
 q=mutate_packet(tmp_path,lambda p:p.__setitem__('internal_pair_matrix',[]))
 with pytest.raises(Exception):semantic(q)

def test_semantic_rejects_count_mismatch(tmp_path):
 q=mutate_packet(tmp_path,lambda p:p['candidate_family']['internal_pair_counts'].__setitem__('direct_positive',0))
 with pytest.raises(ValueError):semantic(q)

def test_semantic_rejects_collision_summary_mismatch(tmp_path):
 q=mutate_packet(tmp_path,lambda p:p['hard_collisions'].append({'collision_id':'P3COL-0123456789abcdef','collision_type':'BLOCK_SAME_PROPOSITION','scope_type':'LINEAGE_PAIR','orientation':'SYMMETRIC','left_id':'p2lineage_example_a','right_id':'p2lineage_example_b'}))
 with pytest.raises(ValueError):semantic(q)

def test_semantic_rejects_wrong_decision_revision(tmp_path):
 q=mutate_packet(tmp_path,lambda p:p['decision_form'].__setitem__('candidate_revision_id','P3CANDREV-999999-R0001'))
 with pytest.raises(ValueError):semantic(q)

def test_semantic_rejects_hash_mismatch(tmp_path):
 q=mutate_packet(tmp_path,lambda p:p['decision_form'].__setitem__('evidence_bundle_hash','1'*64))
 with pytest.raises(ValueError):semantic(q)

def test_semantic_rejects_ranking_mismatch(tmp_path):
 q=mutate_packet(tmp_path,lambda p:p['candidate_family']['ranking'].__setitem__('lineage_count',3))
 with pytest.raises(ValueError):semantic(q)

def test_zero_hashes_removed():
 for p in (SEC/'adjudication').glob('*.json'):assert '0'*64 not in p.read_text()

def test_split_result_requires_successor_partition(tmp_path):
 p=loadj(SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v6.json');d=p['decision_form'];d.update({'decision_status':'SPLIT_REQUIRED','rationale':'split','split_points':[{'dimension':'TARGET','left_member_ids':['p2lineage_example_a'],'right_member_ids':['p2lineage_example_b'],'rationale':'targets differ'}],'split_results':[{'result_ordinal':1,'successor_candidate_family_id':'P3CAND-000002','successor_origin_key':'1'*64,'member_ids':['p2lineage_example_a'],'rationale':'a'},{'result_ordinal':2,'successor_candidate_family_id':'P3CAND-000003','successor_origin_key':'2'*64,'member_ids':['p2lineage_example_a'],'rationale':'bad duplicate'}]})
 p['decision_form']=d;q=tmp_path/'p.json';q.write_text(json.dumps(p))
 with pytest.raises(ValueError):semantic(q)

def test_ddl_contains_instantiation_surfaces():
 ddl=(SEC/'sql/p3_postgresql_compatible_ddl_v6.sql').read_text()
 for x in ['p3_pair_projection','p3_candidate_attachment_projection','membership_basis','p3_adjudication_split_result','p3_variant_promotion','p3_exclusion_promotion','created_by_adjudication_id','occurred_at TIMESTAMPTZ','p3_validate_pair_projection','p3_assert_candidate_origin','p3_assert_adjudication_member_partition']:
  assert x in ddl

def test_identity_and_vocab_closure():
 i=pd.read_csv(SEC/'P3_IDENTITY_KEY_SPEC_v6.csv',keep_default_na=False);assert (i.object_type=='PAIR_PROJECTION').sum()==1
 v=pd.read_csv(SEC/'P3_CONTROLLED_VOCABULARIES_v6.csv',keep_default_na=False);assert ((v.vocabulary_domain=='pair_projection_basis')&(v.code=='SEGMENT_BINDING')).any()

def test_artifact_catalog_includes_new_executable_surfaces():
 c=pd.read_csv(SEC/'P3_ARTIFACT_CATALOG_v6.csv',keep_default_na=False)
 for x in ['schemas/pair_projection.schema.json','validation/validate_p3_candidate_packet_v6.py','upstream/P3_ATTACHMENT_REVIEW_GROUPS_PREFLIGHT_v6.csv','upstream/P3_SIGNATURE_WORKSET_v6.csv']:
  assert x in set(c.artifact)

def test_plan_no_full_signature_overbuild():
 import yaml
 seq=yaml.safe_load((SEC/'P3_EXECUTION_SEQUENCE_v6.yaml').read_text())
 p3a3=next(x for x in seq['phases'] if x['phase']=='P3A-3')
 joined=' '.join(p3a3['steps'])
 assert '399 proposition-incident lineages' in joined
 assert '2,897 constraint-only lineages' in joined

def test_no_stale_section47_paths():
 for p in [SEC/'validation/verify_handoff_v26.py',SEC/'validation/test_p3_plan_v6.py']:
  for line in p.read_text().splitlines():
   if line.strip().startswith('SEC='):
    assert "47_P3_PLAN" not in line


def test_ddl_has_no_empty_validation_stubs_or_forward_table_refs():
 ddl=(SEC/'sql/p3_postgresql_compatible_ddl_v6.sql').read_text()
 assert not re.search(r'BEGIN\s+RETURN NEW;\s+END',ddl,re.S|re.I)
 positions={m.group(1):m.start() for m in re.finditer(r'CREATE TABLE\s+(\w+)',ddl,re.I)}
 for m in re.finditer(r'REFERENCES\s+(\w+)',ddl,re.I):
  if m.group(1) in positions: assert positions[m.group(1)]<m.start(),m.group(1)

def test_promotion_ids_use_governed_variant_and_exclusion_identities():
 v=loadj(SEC/'schemas/variant_promotion.schema.json');e=loadj(SEC/'schemas/exclusion_promotion.schema.json')
 assert v['properties']['canonical_variant_revision_id']['pattern'].startswith('^P3VARREV')
 assert e['properties']['canonical_exclusion_id']['pattern'].startswith('^P3EXC')


def test_semantic_rejects_projection_endpoint_mismatch(tmp_path):
 q=mutate_packet(tmp_path,lambda p:p['pair_projections'][0].__setitem__('right_subject_id','outsider'))
 with pytest.raises(ValueError):semantic(q)

def test_semantic_rejects_nonrecomputing_evidence_hash(tmp_path):
 q=mutate_packet(tmp_path,lambda p:p['exact_evidence_links'].append('new_evidence_not_hashed'))
 with pytest.raises(ValueError):semantic(q)

def test_directional_pair_projection_is_not_lexically_reordered():
 ddl=(SEC/'sql/p3_postgresql_compatible_ddl_v6.sql').read_text()
 table=re.search(r'CREATE TABLE p3_pair_projection\s*\((.*?)\);',ddl,re.S|re.I).group(1)
 assert 'left_subject_id < right_subject_id' not in table
 assert "endpoint_side='LEFT'" in ddl and "endpoint_side='RIGHT'" in ddl
