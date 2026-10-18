"""WP2I independent tests implementing frozen P01-P14; originals untouched."""
import copy,json,sys,os
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import pytest
R=Path(__file__).resolve().parents[1];WROOT=R/'runtime/candidate_checkout/WORKER_RETURNS/PYAT-R32-WP2-NATIVE-WORLD-POSSIBILITY-R1'
sys.path.insert(0,str(WROOT/'repro'))
import wp2 as W
from product import empirical as EP
from product.world import SelectedSnapshot
from rawlsing_next.pre553_empirical_objects import semantic_hash
PRODUCT=json.loads((R/'04_ORIGINAL_NEW_REAL_JUNIT_COLD/independent_cold_a.json').read_text())
RECOMPUTED={}
def raw_counts(rows,target,conditions):
 selected=[r for r in rows if all(r['responses'][k]==v for k,v in conditions)]
 c=Counter(str(r['responses'][target]) for r in selected)
 return len(selected),dict(sorted(c.items()))
def observed(step):return step['denominator'],{c['cell']:c['raw_numerator_support'] for c in step['cells']}
@pytest.mark.parametrize('key,target,conditions',[
 ('current_rule_revision','Y',[('A',1),('B',1),('C',1)]),
 ('opposite_condition','Y',[('A',0),('B',1),('C',1)]),
 ('reverse_native_role','A',[('Y',1)]),
 ('changed_empirical_law','Y',[('A',1),('B',1),('C',1)]),
 ('zero_support','Y',[('A',1),('B',1),('C',1)])])
def test_recount_native_rows_without_composition_estimator(key,target,conditions):
 rows=copy.deepcopy(EP.e03.synthetic_world_rows())
 if key=='changed_empirical_law':next(r for r in rows if all(r['responses'][k]==1 for k in 'ABC') and r['responses']['Y']==0)['responses']['Y']=1
 if key=='zero_support':rows=[r for r in rows if not all(r['responses'][k]==1 for k in 'ABC')]
 exact=[raw_counts(rows,target,conditions[:n]) for n in range(1,len(conditions)+1)]
 assert exact==[observed(s) for s in PRODUCT['cases'][key]['empirical_steps']]
 RECOMPUTED[key]=dict(source_rows=len(rows),counts=exact,fractions=[None if d==0 else str(F(c.get('1',0),d)) for d,c in exact])
@pytest.mark.parametrize('direction,rows,target,conditions',[
 ('forward','base','ANSWER',[('POSITION','P1')]),('reverse','base','POSITION',[('ANSWER','yes')]),('changed_forward','changed','ANSWER',[('POSITION','P1')])])
def test_at07_independent_direct_risk_set_enumeration(direction,rows,target,conditions):
 rows=W.AT07.changed_source_rows() if rows=='changed' else W.AT07.at07_rows()
 d,c=raw_counts(rows,target,conditions);o=PRODUCT['at07_native_2x2'][direction]
 assert d==o['raw_denominator'];assert c=={x['cell']:x['raw_numerator_support'] for x in o['geometry']['cells']}
 RECOMPUTED['AT07_'+direction]=dict(denominator=d,cells=c)
@pytest.mark.parametrize('name',['world_a','world_b'])
def test_f6_recompute_from_native_stratum_tables_without_synthesis(name):
 x=PRODUCT['f6_sourcefree'][name];target=x['input_target'];sources=x['input_sources'];policy=x['input_policy'];joint=defaultdict(F);bounds_low=defaultdict(F);bounds_high=defaultdict(F);uncovered=F(0)
 domain=[tuple(c) for c in x['native_bundle']['candidate']['ordered_categories']]
 for z,share in target['strata'].items():
  share=F(share);ps=[]
  for s in sources:
   table=s['strata'].get(z)
   if table is None or table['eligible_n']<policy['minimum_raw_support']:continue
   mass=sum((F(c['mass']) for c in table['cells']),F(0));prob={tuple(axis['category_map'][v] for axis,v in zip(s['axes'],c['categories'])):F(c['mass'])/mass for c in table['cells']}
   ps.append((s['source_id'],prob))
  if not ps:uncovered+=share;continue
  total_weight=sum(F(policy['source_weights'][sid]) for sid,_ in ps)
  for k in domain:
   joint[k]+=share*sum((F(policy['source_weights'][sid])*p[k] for sid,p in ps),F(0))/total_weight
   bounds_low[k]+=share*min(p[k] for _,p in ps);bounds_high[k]+=share*max(p[k] for _,p in ps)
 candidate=x['native_bundle']['candidate'];native={tuple(c['categories']):F(c['probability']) for c in candidate['covered_subprobability']}
 assert dict(joint)==native;assert uncovered==F(candidate['uncovered_target_mass'])
 assert sum(joint.values(),F(0))+uncovered==1
 for b in candidate['uncertainty']['source_disagreement_and_uncovered_bounds']:
  k=tuple(b['categories']);assert F(b['lower'])==bounds_low[k];assert F(b['upper'])==bounds_high[k]+uncovered
 if uncovered:assert candidate['distribution'] is None and x['native_conditional_consumer']['reason']=='NO_COMPLETE_TARGET_JOINT'
 else:
  conditional=joint[('secure','formal')]/sum(p for k,p in joint.items() if k[0]=='secure');assert conditional==F(26,31)
  assert F(x['native_conditional_consumer']['probabilities']['formal'])==conditional
 RECOMPUTED['F6_'+name]=dict(joint={str(k):str(v) for k,v in joint.items()},uncovered=str(uncovered),bounds={str(k):[str(bounds_low[k]),str(bounds_high[k]+uncovered)] for k in domain})

def test_same_clock_structural_intervention_separates_clock_from_rule():
 q=W.E.standard_request(label='CURRENT_TEST_CLOCK')
 before=W.execute(W.make(structural_revision=False),q)[-1];after=W.execute(W.make(structural_revision=True),q)[-1]
 assert before['selection']==after['selection'];assert before['empirical_steps']==after['empirical_steps']
 assert before['native_field_readset']==after['native_field_readset']
 assert [c['consumer_material']['empirical'] for c in before['consumers']]==[c['consumer_material']['empirical'] for c in after['consumers']]
 assert before['consumers'][0]['consumer_material']['structural_routes']['training']['state']=='ELIGIBLE'
 assert after['consumers'][0]['consumer_material']['structural_routes']['training']['state']=='BLOCKED_BY_MODELED_RULE'
 assert before['consumers'][1]['consumer_material']['scenarios'][0]['feasibility']=='FEASIBLE_MODELED_PREMISE'
 assert after['consumers'][1]['consumer_material']['scenarios'][0]['feasibility']=='INFEASIBLE_MODELED_PREMISE'
 RECOMPUTED['same_clock_structural_control']=dict(selection=before['selection'],empirical_identical=True,native_readset_identical=True,training_before=True,training_after=False)

@pytest.mark.parametrize('valid,published,expected',[
 ('2026-12-31','2027-09-01',True),('2027-01-01','2027-05-31',True),('2027-01-01','2027-06-01',False),('2027-09-01','2027-05-31',True),('2027-09-01','2027-06-01',False)])
def test_effective_and_publication_boundary_cross_product(valid,published,expected):
 a=W.make(structural_revision=True);q=W.E.standard_request(label='CURRENT_TEST_CLOCK');q=W.E.N9SelectedWorldRequest(**{**q.__dict__,'clock':W.E.SelectedWorldClock('AS_OF',valid,published)})
 r=W.execute(a,q)[-1];assert r['structural_values']['training_access']['value'] is expected
 assert r['structural_values']['exit_cost']['value']==(2 if expected else 8)

@pytest.mark.parametrize('tamper',['world','root','grant'])
def test_rehashed_caller_snapshot_is_not_native_owner_acceptance(tamper):
 a=W.make();q=W.E.standard_request(label='CURRENT_TEST_CLOCK');s=a.build_snapshot(q);m=copy.deepcopy(s.material)
 if tamper=='world':m['valid_at']='2025-01-01'
 if tamper=='root':m['source_permission_root']='CALLER_ROOT'
 if tamper=='grant':m['purpose']='OPERATIVE_CURRENT'
 forged=SelectedSnapshot(m,semantic_hash(m))
 with pytest.raises(ValueError):a.accept(q,forged)

@pytest.mark.parametrize('scope',['training_access','empirical'])
def test_old_successful_client_material_refused_after_native_revocation(scope):
 a,q,s,accept,receipt=W.execute();old=[c['consumer_material'] for c in receipt['consumers']]
 a.invalidate(scope)
 with pytest.raises(ValueError,match='CONSUMER_MATERIAL_NOT_EXACT_ORIGINAL_OUTPUT'):a.serve(q,accept,s,consumers=old)
 fresh=[W.consume(a.service,s)['material'],W.evaluate(a.service,s,W.PROPOSALS)['material']]
 after=a.serve(q,accept,s,consumers=fresh);assert after['state']=='TYPED_PARTIAL_SELECTED_WORLD'
 if scope=='empirical':assert after['empirical_steps']==[]
 else:assert after['empirical_steps']==receipt['empirical_steps']

@pytest.mark.parametrize('role',[W.GSS,W.NCA])
def test_native_registry_permission_substitution_never_reuses_old_positive(role):
 a,q,s,accept,r=W.execute();rows=W.rows();next(v for v in rows if v['role']==role)['permission']='FORGED_NEW_GRANT'
 with pytest.raises(W.E.TestOnlyReadError,match='REAL_USE_PERMISSION_NOT_ISSUED'):
  a.registry=W.TestOnlyRegistry(rows)
  a.serve(q,accept,s)

def test_real_proposal_label_change_leaves_all_modelled_results_fixed():
 a=W.make(structural_revision=True);q=W.E.standard_request(label='CURRENT_TEST_CLOCK');s=a.build_snapshot(q)
 p=copy.deepcopy(W.PROPOSALS);p[0]['scenario_id']='INDEPENDENT_RELABELED_ONLY'
 first=W.evaluate(a.service,s,W.PROPOSALS)['material'];second=W.evaluate(a.service,s,p)['material']
 first['scenarios'][0]['scenario_id']=p[0]['scenario_id']
 assert first==second

@pytest.mark.parametrize('case',['current_rule_revision','historical_rule','changed_empirical_law','zero_support'])
def test_scientific_route_and_selection_permission_nulls(case):
 r=PRODUCT['cases'][case];nonparent,proposal=[x['consumer_material'] for x in r['consumers']]
 assert nonparent['route_probability'] is None and nonparent['route_probability_reason']=='NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL'
 assert all(s['selection_weight'] is None and s['weight_reason']=='NO_SCENARIO_SELECTION_MODEL_OR_ISSUER' for s in proposal['scenarios'])
 assert r['model_use'] is r['operative_N9'] is r['operative_OC05'] is r['new_issuer'] is False
 assert PRODUCT['generic_read_only_input']['state']=='UNINSTALLED_TEST_ONLY_PORT'
 assert PRODUCT['generic_read_only_input']['actor_knowledge_time']=='NOT_REQUESTED_NO_ACTOR_OWNER'

def test_actual_cold_process_owner_observations():
 proof=json.loads((R/'04_ORIGINAL_NEW_REAL_JUNIT_COLD/independent_cold_replay.json').read_text())
 assert proof['distinct_processes'] and proof['byte_identical']
 assert len(PRODUCT['actual_C1_returns'])==79;assert len(PRODUCT['actual_N10E_returns'])==28
 assert all(v['same_composition_evidence_object'] for v in PRODUCT['actual_N10E_returns'])
 counts=PRODUCT['call_counts'];m4=sum(v['count'] for v in counts if v['function']=='resolve_v558');m5=sum(v['count'] for v in counts if v['function']=='materialize_resolved_structural_context')
 assert (m4,m5)==(180,60)
 imports=json.loads((R/'04_ORIGINAL_NEW_REAL_JUNIT_COLD/independent_cold_a.imports.json').read_text())['imports']
 assert not any('GF1E' in x['file'] or 'GF1H' in x['file'] for x in imports)

@pytest.fixture(scope='session',autouse=True)
def save_recomputations():
 yield
 (R/'03_NATIVE_VALUE_AND_SCIENTIFIC_RECOMPUTATIONS.json').write_text(json.dumps(RECOMPUTED,indent=2)+'\n')

def test_excluded_source_weight_becomes_unknown_mass_without_renormalizing():
 x=PRODUCT['f6_sourcefree']['P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED'];weights=x['input_policy']['source_weights'];total=sum((F(v) for v in weights.values()),F(0));covered=defaultdict(F);unknown=F(0)
 for s in x['input_sources']:
  weight=F(weights[s['source_id']])/total;table=s['strata']['Z1'];n=table['eligible_n']
  if n<x['input_policy']['minimum_raw_support']:unknown+=weight;continue
  for cell in table['cells']:
   key=tuple(axis['category_map'][code] for axis,code in zip(s['axes'],cell['categories']))
   covered[key]+=weight*F(cell['mass'])/sum(F(c['mass']) for c in table['cells'])
 assert unknown==F(1,2);assert set(covered.values())=={F(1,8)}
 native=x['native_bundle']['candidate'];assert native['distribution'] is None
 assert {tuple(c['categories']):F(c['probability']) for c in native['covered_subprobability']}==covered
 for b in native['uncertainty']['source_disagreement_and_uncovered_bounds']:
  k=tuple(b['categories']);assert F(b['lower'])==covered[k] and F(b['upper'])==covered[k]+unknown
 RECOMPUTED['F6_excluded_source']=dict(unknown_mass=str(unknown),cell_lower='1/8',cell_upper='5/8',distribution=None)

def test_empirical_only_change_rebinds_every_consumer_release_with_same_rule():
 before=PRODUCT['cases']['current_rule_revision'];after=PRODUCT['cases']['changed_empirical_law']
 assert before['selection']==after['selection'];assert before['structural_values']==after['structural_values']
 for b,a in zip(before['empirical_steps'],after['empirical_steps']):
  assert b['source_universe_ref']!=a['source_universe_ref'];assert b['release_ref']!=a['release_ref'];assert b['evidence_ref']!=a['evidence_ref']
  for consumer in after['consumers']:
   actual=consumer['consumer_material']['empirical']['steps'];assert any(s['evidence_ref']==a['evidence_ref'] and s['cells']==a['cells'] for s in actual)

def test_actor_knowledge_clock_is_not_a_world_clock_grant():
 with pytest.raises(TypeError):W.E.SelectedWorldClock('AS_OF','2027-09-01','2027-09-01',actor_knowledge_at='2026-01-01')
 with pytest.raises(W.E.N9SelectedWorldRefusal):W.E.standard_request(label='CURRENT_TEST_CLOCK',requested_person_exposure=True)
 assert PRODUCT['generic_read_only_input']['actor_executions']==0
