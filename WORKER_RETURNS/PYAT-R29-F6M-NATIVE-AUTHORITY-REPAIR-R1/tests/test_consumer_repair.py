"""Productive paths plus hostile rights, origin, provenance and exclusion paths."""
from pathlib import Path
import sys,copy,json,hashlib
from fractions import Fraction as F
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'candidate'))
sys.path.insert(0,str(ROOT/'inherited/F6C/02_TESTS'))
import f6c_worlds as C
import rawlsing_next.pre553_heterogeneous_synthesis as M
from rawlsing_next.pre553_empirical_objects import semantic_hash
FROZEN=json.loads((ROOT/'inherited/F6L/02_PHASE_A/01_WORLDS_AND_EXACT_EXPECTATIONS.json').read_text())
W={w['case']:w for w in FROZEN['worlds']}
def run(case,flags=None,threshold=None):
 w=copy.deepcopy(W[case])
 if flags is not None:
  for s,flag in zip(w['sources'],flags):s['test_origin']=flag
 if threshold is not None:w['policy']['minimum_raw_support']=threshold
 return M.synthesize(w['target'],w['sources'],w['policy'],admit=lambda *_:True)
def point_consumer(bundle,conditions,outcome,*,real_use=False):
 # A genuine decision-only gate cannot turn a partial artifact into a point.
 if bundle['decision']=='PARTIAL_IDENTIFICATION_ONLY':return {'state':'REFUSED_PARTIAL'}
 return M.conditional(bundle,conditions,outcome,use='REAL_USE' if real_use else 'SOURCEFREE_EXPERIMENT')
def cells(c):return {tuple(x['categories']):F(x['probability']) for x in c}
def rehash(out):out['content_hash']=semantic_hash({k:v for k,v in out.items() if k!='content_hash'});return out

def test_unchanged_world_a_value_reading_positive():
 out=M.synthesize(*C.world_a())
 receipt=point_consumer(out,{'material_security':'secure'},'employment_position')
 assert receipt['state']=='SUPPORTED_MODEL'
 assert F(receipt['probabilities']['formal'])==F(26,31)
 assert receipt['real_use_authorized'] is False
 assert receipt['use_scope']=='SOURCEFREE_EXPERIMENT_ONLY'
 assert cells(out['candidate']['distribution'])[('secure','formal')]==F(13,25)

@pytest.mark.parametrize('case',['P1_ORIGINAL_UNCOVERED_WORLD','P2_NOVEL_2X2_NO_POSITIVITY','P3_NOVEL_3_CATEGORY_NO_POSITIVITY'])
def test_null_joint_refused_by_decision_and_value_consumers(case):
 out=run(case);cand=out['candidate'];axis=cand['construct_topology']
 assert out['decision']=='PARTIAL_IDENTIFICATION_ONLY'
 assert out['target_joint_status']=='NO_COMPLETE_TARGET_JOINT'
 assert point_consumer(out,{},axis[-1])=={'state':'REFUSED_PARTIAL'}
 assert M.conditional(out,{},axis[-1])['reason']=='NO_COMPLETE_TARGET_JOINT'
 assert sum(cells(cand['covered_subprobability']).values(),F(0))+F(cand['uncovered_target_mass'])==1
 assert cand['distribution'] is None and cand['uncertainty']['source_disagreement_and_uncovered_bounds']

@pytest.mark.parametrize('flags',[(True,True),(False,False),(False,True),(True,False)])
def test_origin_declarations_and_fake_callback_never_authenticate_real_use(flags):
 out=run('P11_GENUINE_COMPLETE_TARGET_POSITIVE',flags)
 assert out['candidate']['distribution'] is not None # numerical feasibility survives
 assert out['real_use_authorized'] is False
 assert out['owner_admission_status']=='UNVERIFIED_INTEGRATION_BOUNDARY'
 assert out['origin_classification']==('DECLARED_TEST_ONLY' if all(flags) else 'MIXED_TEST_AND_UNVERIFIED' if any(flags) else 'UNVERIFIED_SOURCE_INPUT')
 assert all(n['authority_ceiling'] in ('TEST_ONLY','UNVERIFIED') for n in out['evidence_graph'])
 assert M.conditional(out,{},out['candidate']['construct_topology'][-1],use='REAL_USE')['reason']=='UNVERIFIED_OWNER_ADMISSION'

@pytest.mark.parametrize('flags',[(True,True),(False,False),(True,False)])
def test_mapped_values_and_provenance_are_bound_and_never_promoted(flags):
 out=run('P11_GENUINE_COMPLETE_TARGET_POSITIVE',flags)
 nodes={n['node_id']:n for n in out['evidence_graph']};base={b['source_id']:b for b in out['baseline']}
 rank={'UNVERIFIED':0,'TEST_ONLY':1}
 for n in nodes.values():
  assert all(rank[n['authority_ceiling']]<=rank[nodes[p]['authority_ceiling']] for p in n['parents'])
  if n['node_id'].startswith('mapped:'):
   b=base[n['source_id']]
   assert n['producer_ref']==b['native_summary']['product_ref']
   assert n['source_hash']==b['input_hash']==semantic_hash(b['native_summary'])
   assert n['value_hash']==semantic_hash(b['mapped_joint'])
   assert n['mapping_hash']==semantic_hash(b['native_summary']['axes'])


def test_minor_cell_survives_aggregate_threshold_and_is_not_called_protected():
 a=run('P8_DISTRIBUTED_SUPPORT_MIN_1',threshold=1)
 b=run('P8_DISTRIBUTED_SUPPORT_MIN_5_CELL_NOT_GATE',threshold=5)
 assert a['candidate']['distribution']==b['candidate']['distribution']
 assert cells(b['candidate']['distribution'])[('LOW','NO')]==F(7,50)
 assert b['candidate']['support']['Z1']['minority_cell_protection'] is False
 assert 'NOT_MINORITY_CELL_PROTECTION' in b['support_gate_semantics']


def test_dropped_source_retains_its_planned_share_as_unknown_and_preserves_native():
 out=run('P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED',threshold=150)
 c=out['candidate'];sup=c['support']['Z1']
 assert sup['excluded_sources']==['S1']
 assert [s['source_id'] for s in sup['sources']]==['S2']
 assert F(sup['sources'][0]['conditional_source_weight'])==F(1,2)
 assert F(sup['uncovered_target_share'])==F(c['uncovered_target_mass'])==F(1,2)
 assert sum(cells(c['covered_subprobability']).values(),F(0))==F(1,2)
 assert c['distribution'] is None
 assert out['baseline'][0]['native_summary']==W['P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED']['sources'][0]
 assert all(F(x['lower'])==F(1,8) and F(x['upper'])==F(5,8) for x in c['uncertainty']['source_disagreement_and_uncovered_bounds'])
 assert point_consumer(out,{},c['construct_topology'][-1])['state']=='REFUSED_PARTIAL'
 assert c['uncertainty']['sampling_variance'] is None


def test_forged_bundle_rights_and_recomputed_hash_do_not_issue_authority():
 out=run('P11_GENUINE_COMPLETE_TARGET_POSITIVE',(False,True))
 out['owner_admission_status']='VERIFIED';out['real_use_authorized']=True
 for n in out['evidence_graph']:n['authority_ceiling']='EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE'
 rehash(out)
 assert M.conditional(out,{},out['candidate']['construct_topology'][-1],use='REAL_USE')['reason']=='UNVERIFIED_OWNER_ADMISSION'


def test_partial_artifact_with_forged_complete_status_still_refuses_value_reading():
 out=run('P1_ORIGINAL_UNCOVERED_WORLD');out['decision']='SYNTHETIC_CANDIDATE';rehash(out)
 assert M.conditional(out,{},out['candidate']['construct_topology'][-1])['reason']=='NO_COMPLETE_TARGET_JOINT'


def test_positive_mass_cannot_be_hidden_by_a_forged_non_null_distribution():
 out=run('P1_ORIGINAL_UNCOVERED_WORLD');out['candidate']['distribution']=copy.deepcopy(out['candidate']['covered_subprobability']);rehash(out)
 assert M.conditional(out,{},out['candidate']['construct_topology'][-1])['reason']=='NO_COMPLETE_TARGET_JOINT'


def test_no_complete_support_still_preserves_all_native_cells():
 out=run('P8_DISTRIBUTED_SUPPORT_MIN_1',threshold=10000)
 assert F(out['candidate']['uncovered_target_mass'])==1
 assert sum(cells(out['candidate']['covered_subprobability']).values(),F(0))==0
 assert all(F(x['lower'])==0 and F(x['upper'])==1 for x in out['candidate']['uncertainty']['source_disagreement_and_uncovered_bounds'])
 assert all(len(t['cells'])==4 for b in out['baseline'] for t in b['native_summary']['strata'].values())


def test_missing_or_false_integration_callback_preserves_refusal():
 for callback in (None,lambda *_:False):
  t,s,p=C.world_a()
  for source in s:source['test_origin']=False
  with pytest.raises(M.SynthesisError):M.synthesize(t,s,p,admit=callback)


def test_backoff_graph_still_carries_complete_provenance_and_safe_ceiling():
 t,s,p=C.world_a();t['geography']='OTHER'
 out=M.synthesize(t,s,p)
 assert out['candidate'] is None
 assert out['decision']=='SOURCE_INDEXED_BACKOFF'
 assert out['real_use_authorized'] is False
 assert all(n['authority_ceiling']=='TEST_ONLY' and n.get('value_hash') for n in out['evidence_graph'])


def test_unknown_use_scope_is_not_a_permission_bypass():
 out=M.synthesize(*C.world_a())
 with pytest.raises(M.SynthesisError):M.conditional(out,{},out['candidate']['construct_topology'][-1],use='OWNER_APPROVED')
