import json
from pathlib import Path
from dataclasses import replace
import pytest
from native_court import (HERE,OBS,_fixture,_execute,execute_native,independent_gate,ScientificHold,dump,
 build_source_backed_c11_repository,units_for,consumer_for)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
from rawlsing_next.pre553_route_b_production import RouteBProductionError

def test_actual_c11_i03_i05_batch_oc01_positive():
 r=execute_native();dump(r,OBS/'native_positive.json')
 assert sorted(x['kind'] for x in r['native_calls'])==['I03','I03','I05']
 assert r['batch_summary']['full_coverage'] and r['work_antijoin']=={'missing':0,'extra':0}
 assert len(r['facts'])==2
 assert {f['semantic_fields']['measure_kind'] for f in r['facts']}=={'RAW','GOVERNED_WEIGHTED'}
 assert all(f['semantic_fields']['raw_denominator_support']==2 for f in r['facts'])
 frozen=json.loads((HERE/'PREREGISTERED_EXPECTATIONS.json').read_text())['testonly_native_positive']
 for fact in r['facts']:
  s=fact['semantic_fields'];cells=s['target_topology']['complete_cell_semantic_projection']
  assert {c['cell']:c['raw_numerator_support'] for c in cells}==frozen['raw_Y_numerators']
  if s['measure_kind']=='GOVERNED_WEIGHTED':
   assert s['weighted_denominator_support_if_authorized']=={'$exact_fraction':[frozen['weighted_Y_denominator'],1]}
   assert {c['cell']:c['weighted_numerator_support_if_authorized']['$exact_fraction'][0] for c in cells}==frozen['weighted_Y_numerators']
 assert r['consumer']['positive_completion']
 assert {json.dumps(x,sort_keys=True) for x in r['consumer']['selected_producer_refs']}=={
  json.dumps({'kind':'EmpiricalFact@1.0.0','object_id':f['object_id'],'content_hash':f['content_hash']},sort_keys=True) for f in r['facts']}

@pytest.mark.parametrize('selection',[(0,2),(1,2),(0,1)])
def test_omitted_native_request_before_execution_consumer(selection,monkeypatch):
 calls=[]
 import native_court
 monkeypatch.setattr(native_court.CarrierNeutralResearchExecutor,'execute_i03',lambda *a,**k:calls.append('I03'))
 monkeypatch.setattr(native_court.CarrierNeutralResearchExecutor,'execute_i05',lambda *a,**k:calls.append('I05'))
 monkeypatch.setattr(native_court,'consumer_for',lambda *a,**k:calls.append('consumer'))
 with pytest.raises(ScientificHold,match='missing'):execute_native(select=selection)
 assert calls==[]

def test_batch_full_manifest_coverage_is_not_expected_universe_coverage():
 r=execute_native(select=(0,2),gate=False,consume=False)
 dump(r,OBS/'native_subset_characterization.json')
 assert r['batch_summary']['full_coverage'] is True
 assert r['work_antijoin']['missing']==1
 assert r['consumer'] is None

def test_same_count_native_query_substitution():
 fx=_fixture();_,release=build_source_backed_c11_repository(fx['stream'],fx['projection']);units=units_for(fx,release)
 expected=[u.semantic_projection() for u in units]
 changed=[u.semantic_projection() for u in (units[0],units[0],units[2])]
 assert len(expected)==len(changed)
 with pytest.raises(ScientificHold,match='missing'):independent_gate(expected,changed)

def test_extra_native_request_before_consumer():
 fx=_fixture();_,release=build_source_backed_c11_repository(fx['stream'],fx['projection']);units=units_for(fx,release)
 expected=[u.semantic_projection() for u in units]
 foreign=_fixture(valid_empty=True)
 _,foreign_release=build_source_backed_c11_repository(foreign['stream'],foreign['projection'])
 foreign_query=units_for(foreign,foreign_release)[0]
 from rawlsing_next.pre553_batch_runner import BatchManifest
 candidate=BatchManifest((*units,foreign_query))
 assert len(candidate.units)==4
 with pytest.raises(ScientificHold,match='extra'):
  independent_gate(expected,[u.semantic_projection() for u in candidate.units])

def test_physical_source_swap_rejected_before_i03():
 fx=_fixture();calls=[]
 hostile=ExactPhysicalCellStream(source_sha256='f'*64,row_count=3,cell_iter_factory=lambda:calls.append('read') or fx['stream'].cell_iter_factory())
 with pytest.raises(RouteBProductionError,match='source/projection'):
  from rawlsing_next.pre553_route_b_production import execute_route_b_production
  execute_route_b_production(source=hostile,projection=fx['projection'],runtime_catalog=fx['catalog'],i03_requests=fx['requests'],discovery_authority_ref=fx['discovery_authority'].ref)
 assert calls==[]

def test_projection_authority_withdrawal_is_not_ignored():
 fx=_fixture()
 catalog=RuntimeObjectCatalog(authorities=tuple(a for a in fx['catalog'].authorities if a.authority_ref!=fx['projection_auth'].authority_ref),
  predicates=fx['catalog'].predicates,queries=fx['catalog'].queries,discovery_authorities=fx['catalog'].discovery_authorities)
 with pytest.raises(RouteBProductionError,match='projection authority'):_execute(fx,catalog=catalog)

def test_missing_weight_is_unavailable_to_actual_consumer():
 r=execute_native(missing_weight=True);dump(r,OBS/'native_missing_weight.json')
 assert any(f['typed_state']=='UNAVAILABLE' for f in r['facts'])
 assert r['consumer']['positive_completion'] is False
 assert r['consumer']['missing_required_input_ids']

def test_valid_empty_discovery_is_preserved():
 r=execute_native(valid_empty=True);dump(r,OBS/'native_valid_empty.json')
 assert r['discovery_valid_empty']==[True]
 assert r['discovery_receipts'][0]['typed_state']=='VALID_EMPTY'

def test_result_ref_substitution_detected_before_consumer():
 r=execute_native(consume=False)
 original=[{'unit':v['unit_ref'],'results':v['result_refs']} for v in r['unit_receipts']]
 changed=json.loads(json.dumps(original));changed[0]['results'][0]['content_hash']='f'*64
 with pytest.raises(ScientificHold):independent_gate(original,changed)

def test_testonly_revocation_blocks_before_consumer():
 with pytest.raises(ScientificHold,match='REVOKED'):independent_gate([{'id':'A'}],[{'id':'A'}],live=False)

def test_cold_replay_exact_native_receipts():
 r=execute_native();path=OBS/'cold_reference.json'
 semantic={k:r[k] for k in ('release_ref','manifest','unit_receipts','facts','discovery_receipts','consumer')}
 # Compare the exact canonical JSON transport, rather than Python tuple versus
 # JSON-list container types. Object IDs/hashes and every payload field remain.
 if path.exists():assert json.loads(path.read_text())==json.loads(json.dumps(semantic))
 else:dump(semantic,path)
