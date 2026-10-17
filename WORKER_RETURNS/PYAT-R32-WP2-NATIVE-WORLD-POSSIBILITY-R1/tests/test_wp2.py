"""Fixed arithmetic and boundary assertions over actual cold native products."""
import json,os,sys,copy
from pathlib import Path
from fractions import Fraction as F
import pytest
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'repro'))
import wp2 as W
@pytest.fixture(scope='session')
def result():return json.loads(Path(os.environ['WP2_PRODUCT']).read_text())
def counts(r):return [(x['denominator'],{c['cell']:c['raw_numerator_support'] for c in x['cells']}) for x in r['empirical_steps']]
def clients(r):return [x['consumer_material'] for x in r['consumers']]
def native(r):return {x['role']:x for x in r['native_field_readset']['values_read']}

def test_actual_imports_pin_original_owner_bytes():
 # All inherited bytes currently imported must match immutable source manifest.
 m=W.import_manifest()
 for name in ['rawlsing_next.pre553_analytical_composition','rawlsing_next.pre553_empirical_possibility_provider','rawlsing_next.source_backed_positioned_subject_possibility','product.service','product.nonparent']:
  x=next(x for x in m['imports'] if x['module']==name)
  assert x['kind']=='EXACT_INHERITED_NATIVE' and x['source']['commit']
  assert str(R) in x['file']

def test_native_producer_values_and_reverse_are_computed(result):
 c=result['cases'];assert counts(c['current_rule_revision'])==[(32,{'0':14,'1':18}),(16,{'0':6,'1':10}),(8,{'0':2,'1':6})]
 assert counts(c['reverse_native_role'])==[(29,{'0':11,'1':18})]
 assert counts(c['opposite_condition'])==[(26,{'0':15,'1':11}),(12,{'0':6,'1':6}),(6,{'0':2,'1':4})]
 for key in ['reverse_native_role','opposite_condition']:assert c[key]['consumers']==[] # original clients do not accept these readsets

def test_native_full_2x2_role_reversal_and_changed_law(result):
 a=result['at07_native_2x2']
 assert a['forward']['raw_denominator']==60 and a['reverse']['raw_denominator']==62
 assert a['changed_forward']['raw_denominator']==70
 for name,x in a.items():
  assert x['provider_state']=='EXACT_SUPPORTED_SLICE_PRODUCED';assert x['identity_is_actual_composition_object']
  assert x['evidence_ref']==x['consumer_evidence_ref'];assert x['consumer_state']=='EXACT_SUPPORTED'
  assert len(x['geometry']['cells'])==2
 cells=lambda x:{c['cell']:c['raw_numerator_support'] for c in x['geometry']['cells']}
 assert cells(a['forward'])=={'yes':54,'no':6};assert cells(a['reverse'])=={'P1':54,'P2':8}
 assert cells(a['changed_forward'])=={'yes':54,'no':16}
 assert a['forward']['source_universe_ref']!=a['changed_forward']['source_universe_ref']

def test_two_historical_rules_have_actual_structured_effects(result):
 c=result['cases'];old=c['historical_rule'];new=c['current_rule_revision']
 assert old['structural_values']['training_access']['value'] is True
 assert new['structural_values']['training_access']['value'] is False
 assert old['structural_values']['exit_cost']['value']==2;assert new['structural_values']['exit_cost']['value']==8
 assert old['empirical_steps']==new['empirical_steps']
 oc,nc=clients(old),clients(new)
 assert oc[0]['structural_routes']['training']['state']=='ELIGIBLE'
 assert nc[0]['structural_routes']['training']['state']=='BLOCKED_BY_MODELED_RULE'
 assert oc[0]['structural_routes']['exit_constraint']['state']=='WITHIN_MODELED_BUDGET'
 assert nc[0]['structural_routes']['exit_constraint']['state']=='RESOURCE_CONSTRAINED'
 assert oc[1]['scenarios'][0]['feasibility']=='FEASIBLE_MODELED_PREMISE'
 assert nc[1]['scenarios'][0]['feasibility']=='INFEASIBLE_MODELED_PREMISE'
 assert oc[0]['structural_routes']['civil']['state']==nc[0]['structural_routes']['civil']['state']=='ELIGIBLE'

def test_label_control_does_not_change_the_actual_world(result):
 c=result['cases'];control=c['label_only_control'];assert control['before_display_label']!=control['after_display_label']
 assert control['before_receipt_hash']==control['after_receipt_hash'];assert control['model_request_unchanged']
 assert c['same_rule_relabel_control']==c['current_rule_revision']

def test_empirical_change_has_actual_downstream_numeric_effect(result):
 c=result['cases'];a=c['current_rule_revision'];b=c['changed_empirical_law']
 assert counts(b)==[(32,{'0':13,'1':19}),(16,{'0':5,'1':11}),(8,{'0':1,'1':7})]
 for old,new in zip(clients(a),clients(b)):
  assert [s['denominator'] for s in new['empirical']['steps']]==[32,16,8]
  assert old['empirical']['steps']!=new['empirical']['steps']
  assert [next(x['raw_numerator_support'] for x in s['cells'] if x['cell']=='1') for s in new['empirical']['steps']]==[19,11,7]
 assert clients(a)[0]['source_balance_reads'][0]['source_balance_count']==4
 assert clients(b)[0]['source_balance_reads'][0]['source_balance_count']==6
 assert a['structural_values']==b['structural_values']

def test_actual_consumers_dereference_same_producer_refs_and_keep_minority(result):
 r=result['cases']['current_rule_revision'];refs=[s['evidence_ref'] for s in r['empirical_steps']]
 for c in clients(r):
  assert [s['evidence_ref'] for s in c['empirical']['steps']]==refs
  assert all(len(s['cells'])==2 and min(x['raw_numerator_support'] for x in s['cells'])>0 for s in c['empirical']['steps'])
  reads=[x for x in c['values_read'] if x['channel']=='empirical'];assert [x['evidence_ref'] for x in reads]==refs
 actual={json.dumps(x['evidence_ref'],sort_keys=True) for x in result['actual_C1_returns'] if x['evidence_ref']}
 assert all(json.dumps(x,sort_keys=True) in actual for x in refs)
 assert result['actual_N10E_returns'] and all(x['same_composition_evidence_object'] for x in result['actual_N10E_returns'])

def test_owner_missing_and_zero_support_not_point_estimate(result):
 r=result['cases']['zero_support'];assert [x['denominator'] for x in r['empirical_steps']]==[24,8,0]
 assert r['empirical_steps'][-1]['state']=='ZERO_SUPPORT';assert r['empirical_steps'][-1]['cells']==[]
 assert r['state']=='TYPED_PARTIAL_SELECTED_WORLD'
 for c in clients(r):assert c['empirical']['steps'][-1]['state']=='ZERO_SUPPORT'

@pytest.mark.parametrize('role',[W.GSS,W.NCA])
def test_independent_source_family_revocation_is_selective(result,role):
 rr=result['cases']['source_family_revoked_'+role];before,after=rr['before'],rr['after'];other=W.NCA if role==W.GSS else W.GSS
 assert role not in native(after);assert native(after)[other]==native(before)[other]
 assert after['empirical_steps']==before['empirical_steps'];assert after['structural_values']==before['structural_values']
 assert after['state']=='TYPED_PARTIAL_SELECTED_WORLD'

@pytest.mark.parametrize('scope',['training_access','empirical'])
def test_structural_empirical_revocation_preserves_unrelated_channels(result,scope):
 r=result['cases']['revoked_'+scope];a,b=r['before'],r['after'];assert native(a)==native(b)
 if scope=='training_access':assert b['structural_values'][scope]['state']=='REVOKED' and a['empirical_steps']==b['empirical_steps']
 else:assert b['empirical_steps']==[] and a['structural_values']==b['structural_values']

def test_effective_and_publication_are_distinct_from_request_and_actor_time(result):
 c=result['cases'];r=c['effective_but_unpublished_revision'];assert r['structural_values']['training_access']['value'] is True
 assert r['structural_values']['exit_cost']['value']==2
 assert c['current_rule_revision']['structural_values']['training_access']['value'] is False
 assert result['generic_read_only_input']['actor_knowledge_time']=='NOT_REQUESTED_NO_ACTOR_OWNER'
 with pytest.raises(TypeError):W.E.SelectedWorldClock('AS_OF','2027-05-01','2027-05-01',actor_knowledge_at='2027-05-01')

@pytest.mark.parametrize('world',['world_a','world_b'])
def test_f6_independent_sources_preserved_and_not_respondent_pooled(result,world):
 x=result['f6_sourcefree'][world];b=x['native_bundle'];sources=x['input_sources']
 assert len({s['survey_lineage'] for s in sources})==2;assert len({s['sample_id'] for s in sources})==2
 assert {z['source_id'] for z in b['baseline']}=={'A','B'}
 assert all(z['native_summary']==s for z,s in zip(b['baseline'],sources))
 assert b['real_use_authorized'] is False
 assert x['ceiling']=='F6M_I2_METHOD_CANDIDATE__NO_INSTALL'

def test_f6_complete_positive_conditional_and_uncertainty(result):
 x=result['f6_sourcefree']['world_a'];b=x['native_bundle'];c=x['native_conditional_consumer']
 assert c['state']=='SUPPORTED_MODEL';assert F(c['probabilities']['formal'])==F(26,31)
 assert F(c['probabilities']['informal'])==F(5,31)
 assert b['candidate']['distribution'] is not None
 assert b['candidate']['uncertainty']['source_disagreement_and_uncovered_bounds']
 assert b['candidate']['uncertainty']['sampling_variance'] is not None
 assert c['real_use_authorized'] is False

@pytest.mark.parametrize('case',['world_b','P1_ORIGINAL_UNCOVERED_WORLD','P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED'])
def test_f6_partial_mass_remains_unknown_and_consumer_refuses(result,case):
 b=result['f6_sourcefree'][case]['native_bundle'];c=result['f6_sourcefree'][case]['native_conditional_consumer'];candidate=b['candidate']
 assert b['decision']=='PARTIAL_IDENTIFICATION_ONLY';assert candidate['distribution'] is None
 assert sum((F(x['probability']) for x in candidate['covered_subprobability']),F(0))+F(candidate['uncovered_target_mass'])==1
 assert c['reason']=='NO_COMPLETE_TARGET_JOINT';assert candidate['uncertainty']['source_disagreement_and_uncovered_bounds']
 assert b['real_use_authorized'] is False

def test_f6_excluded_native_rare_source_not_erased(result):
 b=result['f6_sourcefree']['P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED']['native_bundle'];c=b['candidate']
 assert F(c['uncovered_target_mass'])==F(1,2);assert len(b['baseline'])==2
 assert all(F(x['lower'])==F(1,8) and F(x['upper'])==F(5,8) for x in c['uncertainty']['source_disagreement_and_uncovered_bounds'])
 assert c['uncertainty']['sampling_variance'] is None

@pytest.mark.parametrize('flag',['requested_pooling','requested_person_exposure','requested_model_use'])
def test_actual_owner_refuses_law_person_or_model_promotion(flag):
 with pytest.raises(W.E.N9SelectedWorldRefusal):W.E.standard_request(label="CURRENT_TEST_CLOCK",**{flag:True})

def test_native_provider_has_no_handwritten_geometry_channel():
 with pytest.raises(TypeError):W.provide_empirical_possibility_slice(evidence={'probability':'1/2'})

def test_precise_hold_and_no_opportunity_probability_fabrication(result):
 assert result['terminal']=='OWNER_CHAIN_PARTIAL_WITH_EXACT_HOLD';assert result['hold']['code']=='NAMED_N10W_RULE_HOLD'
 assert result['installation'] is False
 for key in ['current_rule_revision','historical_rule','changed_empirical_law']:
  c=clients(result['cases'][key]);assert c[0]['route_probability'] is None
  assert c[0]['route_probability_reason']=='NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL'
  assert all(s['selection_weight'] is None for s in c[1]['scenarios'])
  assert all(x['actor_executions']==x['model_calls']==0 and x['operative_N9'] is False and x['operative_N10W'] is False for x in c)
 assert result['generic_read_only_input']['join_state']=='NO_AUTHORIZED_COMMON_WORLD_OR_RESPONDENT_JOIN'
