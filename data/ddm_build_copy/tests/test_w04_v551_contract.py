import pandas as pd
from data.ddm_build_copy import ddm_v551_atoms as m
from data.ddm_build_copy.ddm_v551_directionality_expectation import build_v551_directionality_stamp_audit

AUTH={"h1":{"response_semantics_contract_hash":"h1","authority_intensity_semantics":"DIRECTIONAL_MAGNITUDE","projection_rule_id":"r1","authority_status":"CERTIFIED","review_status":"NO_REVIEW"},"h2":{"response_semantics_contract_hash":"h2","authority_intensity_semantics":"ORDINAL_COORDINATE","projection_rule_id":"r2","authority_status":"CERTIFIED","review_status":"NO_REVIEW","neutral_coordinate":"0.5","neutral_boundary":"0.5","negative_endpoint":"0","positive_endpoint":"1"}}
m._load_registry=lambda:AUTH

def row(**kw):
    d=dict(run_id='r',source='S',source_family='S',wave='W',canonical_wave='W',country_code='C',analysis_scope='country',source_table='answer_distribution',source_row_hash='x',question_id='q',var_code='v',position_field='',position_value='',response_value_raw='1',response_value_normalized='1',response_label='x',normalized_response_label='x',response_family='agreement_scale',response_direction='positive',response_intensity=0.8,directional_applicability_status='APPLICABLE_BY_AUTHORITY',bridge_evidence_lane='direct_relation_response',is_substantive=True,is_missing=False,is_special=False,response_semantics_contract_hash='h1',semantic_role='RELATION_EVIDENCE',semantic_role_authority_status='CERTIFIED',response_semantics_authority_status='CERTIFIED',directionality_authority_status='CERTIFIED',structural_mapping_status='COMPLETE',response_option_map_matched=True,usable_for_evidence=True,allowed_as_v551_relation_evidence=True,n_unweighted=10,n_respondents=20,n_weighted=10,pct_unweighted=.5,pct_weighted=.5,weight_status='weighted',response_topology='scalar',empirical_object_type='answer_distribution',empirical_object_id='e',driver_id='d',driver_facet_id='f',relation_axis_id='a',target_entity_id='t',manual_review_flag=False,source_structure_review_required=False,question_use_contract_hash='rowhash')
    d.update(kw);return d

def test_neutral_preserves_raw_midpoint_and_signed_zero():
    a=m.build_v551_directional_candidate_adjudication(pd.DataFrame([row(response_direction='neutral',response_intensity=.5)]));assert a.iloc[0].raw_response_intensity==.5;assert a.iloc[0].v551_signed_intensity==0

def test_neutral_missing_raw_is_promotable_and_signed_zero():
    a=m.build_v551_directional_candidate_adjudication(pd.DataFrame([row(response_direction='neutral',response_intensity=None)]));assert pd.isna(a.iloc[0].raw_response_intensity);assert a.iloc[0].raw_response_intensity_status=='MISSING';assert a.iloc[0].adjudication_outcome=='PROMOTABLE';assert a.iloc[0].v551_signed_intensity==0

def test_intensity_only_does_not_certify_direction():
    a=m.build_v551_directional_candidate_adjudication(pd.DataFrame([row(response_direction='',response_intensity=.8)]));assert a.iloc[0].adjudication_outcome=='NONPROMOTABLE_REPAIRABLE';assert 'missing_certified_response_direction' in a.iloc[0].adjudication_reason

def test_missing_positive_intensity_never_becomes_one():
    a=m.build_v551_directional_candidate_adjudication(pd.DataFrame([row(response_direction='positive',response_intensity=None)]));assert a.iloc[0].adjudication_outcome=='NONPROMOTABLE_REPAIRABLE';assert pd.isna(a.iloc[0].v551_signed_intensity)

def test_unknown_hash_known_family_blocks_exact_authority():
    a=m.build_v551_directional_candidate_adjudication(pd.DataFrame([row(response_semantics_contract_hash='unknown')]));assert a.iloc[0].adjudication_outcome=='NONPROMOTABLE_REPAIRABLE';assert 'missing_exact_response_semantics_contract_authority' in a.iloc[0].adjudication_reason

def test_applicability_candidate_includes_failed_map_and_structure():
    c=m.build_v551_certification_candidate_bridge(pd.DataFrame([row(response_option_map_matched=False,structural_mapping_status='INCOMPLETE')]));assert len(c)==1

def test_bad_sibling_does_not_suppress_clean_atom():
    f=pd.DataFrame([row(source_row_hash='a'),row(source_row_hash='b',response_direction='',response_value_normalized='2')]);atoms,non=m.build_v551_relation_evidence_atoms(f);assert len(atoms)==1 and len(non)==1;assert non.iloc[0].adjudication_outcome=='NONPROMOTABLE_REPAIRABLE'

def test_position_strata_survive_distinct_identity():
    f=pd.DataFrame([row(source_row_hash='a',position_field='sex',position_value='F'),row(source_row_hash='b',position_field='sex',position_value='M')]);a=m.build_v551_directional_candidate_adjudication(f);assert a.candidate_id.nunique()==2 and a.empirical_distribution_id.nunique()==2

def test_distribution_conservation():
    f=pd.DataFrame([row(source_row_hash='a'),row(source_row_hash='b',response_direction='',response_value_normalized='2',n_unweighted=5,n_weighted=5)]);a=m.build_v551_directional_candidate_adjudication(f);c=m.build_v551_directional_distribution_coverage(a);assert c.iloc[0].candidate_count_conserved and c.iloc[0].unweighted_mass_conserved and c.iloc[0].weighted_mass_conserved

def test_zero_promotable_is_valid_contract():
    f=pd.DataFrame([row(response_direction='')]);a=m.build_v551_directional_candidate_adjudication(f);atoms,_=m.build_v551_relation_evidence_atoms(f);c=m.build_v551_directional_distribution_coverage(a);assert len(atoms)==0;assert a.iloc[0].adjudication_outcome=='NONPROMOTABLE_REPAIRABLE';assert m.validate_v551_adjudication_contract(a)==[];assert m.validate_v551_atom_contract(atoms)==[];assert m.validate_v551_coverage_contract(c)==[]

def test_v552_state_not_in_atom_contract():
    f=pd.DataFrame([row()]);atoms,_=m.build_v551_relation_evidence_atoms(f);assert not any(c.startswith('v552_') for c in atoms.columns)

def test_old_contract_rejected():
    f=pd.DataFrame([row()]);atoms,_=m.build_v551_relation_evidence_atoms(f);atoms.loc[:,'schema_version']='v2.1';assert 'incompatible_v551_schema_version' in m.validate_v551_atom_contract(atoms)

def test_neutral_stamp_raw_missing_complete():
    f=pd.DataFrame([row(response_direction='neutral',response_intensity=None)]);a=build_v551_directionality_stamp_audit(f);assert a.iloc[0].directionality_stamp_status=='STAMPED'

def test_positive_stamp_missing_intensity_incomplete():
    f=pd.DataFrame([row(response_direction='positive',response_intensity=None)]);a=build_v551_directionality_stamp_audit(f);assert a.iloc[0].directionality_stamp_status=='MISSING_OR_INCOMPLETE_STAMP'

def test_adjudication_contract_rejects_retired_terminal_vocab():
    a=m.build_v551_directional_candidate_adjudication(pd.DataFrame([row(response_direction='')]))
    a.loc[:, 'adjudication_outcome']='BLOCKED'
    assert 'invalid_adjudication_outcome' in m.validate_v551_adjudication_contract(a)
