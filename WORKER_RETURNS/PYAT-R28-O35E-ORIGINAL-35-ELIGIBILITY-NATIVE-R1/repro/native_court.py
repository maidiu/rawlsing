"""O35E TEST_ONLY composition of actual native operators, not original35 U/E_pre.

The independent gate is experimental return code, not installed governance.
Native Batch only knows the manifest it is given; its full_coverage has that scope.
"""
from pathlib import Path
from dataclasses import asdict
from collections import Counter
import hashlib,json

from rawlsing_next.tests.test_pre553_route_b_production import _fixture,_execute,_h
from rawlsing_next.pre553_source_backed_c11_facade import build_source_backed_c11_repository
from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
from rawlsing_next.pre553_batch_runner import BatchManifest,BatchUnitSpec,BatchExecutionRunner,ExecutorBinding,ExecutionOutcome
from rawlsing_next.pre553_empirical_objects import ExactRef,semantic_hash
import rawlsing_next.objective_consumer_bounded_evidence as oc

HERE=Path(__file__).resolve().parents[1]
OBS=HERE/'observations'

class ScientificHold(ValueError):pass

def jsonkey(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'))

def independent_gate(expected,observed,*,live=True):
 """Multiset outer join, not cardinality or inner join, before consumer."""
 e,o=Counter(map(jsonkey,expected)),Counter(map(jsonkey,observed))
 missing,extra=e-o,o-e
 if not live:raise ScientificHold('TEST_ONLY_WARRANT_REVOKED')
 if missing or extra:raise ScientificHold(jsonkey({'missing':dict(missing),'extra':dict(extra)}))
 return {'missing':0,'extra':0,'duplicate_loss':0,'count':sum(e.values())}

def units_for(fx,release):
 return tuple(BatchUnitSpec('QUERY',r.query_ref,(release.release_ref,),(r.predicate_ref,)) for r in fx['requests'])+(
  BatchUnitSpec('DISCOVERY',fx['discovery_authority'].ref,(release.release_ref,),()),)

def consumer_for(facts):
 inputs=[]
 for fact in facts:
  available=fact.typed_state not in ('UNAVAILABLE','ZERO_SUPPORT')
  # This exact transport is TEST_ONLY. It does not certify original scientific authority.
  authority=tuple(oc.ExactRef('TEST_ONLY_AuthoritySnapshot',a.authority_id,a.authority_content_hash) for a in fact.authority_snapshot_refs)
  inputs.append(oc.PolicyInput(input_id=fact.ref.key,required=True,available=available,
   evidence_kind=oc.EvidenceKind.EMPIRICAL,
   evidence_tier=oc.EvidenceTier.SOURCE_LOCAL_CERTIFIED if available else oc.EvidenceTier.UNAVAILABLE,
   claim_ceiling=oc.ClaimCeiling.SOURCE_LOCAL_STATISTIC,
   producer_ref=oc.ExactRef(**fact.ref.as_dict()) if available else None,
   authority_refs=authority if available else (),
   omission_reason=None if available else 'TEST_ONLY_NATIVE_TYPED_'+fact.typed_state))
 return oc.evaluate_oc01_pre553_source_local(operation_id='O35E_TEST_ONLY_source_local',inputs=inputs,
  requested_claim_ceiling=oc.ClaimCeiling.SOURCE_LOCAL_STATISTIC,partial_allowed=False)

def execute_native(*,missing_weight=False,valid_empty=False,select=None,gate=True,consume=True):
 fx=_fixture(missing_weight=missing_weight,valid_empty=valid_empty)
 repo,release=build_source_backed_c11_repository(fx['stream'],fx['projection'])
 all_units=units_for(fx,release)
 expected=[u.semantic_projection() for u in all_units]
 # Expected identities are frozen before ANY I03/I05 call, derived only from
 # preregistered test fixture roles. They are never called original E_pre.
 freeze={'claim':'TEST_ONLY','expected_units':expected,'expected_sha256':semantic_hash(expected)}
 OBS.mkdir(exist_ok=True)
 name=('missing_weight' if missing_weight else 'valid_empty' if valid_empty else 'baseline')
 path=OBS/f'{name}_preexecution_plan.json'
 if path.exists():assert json.loads(path.read_text())==freeze
 else:path.write_text(json.dumps(freeze,indent=2)+'\n')
 picked=tuple(all_units[i] for i in (select if select is not None else range(len(all_units))))
 manifest=BatchManifest(picked)
 if gate:independent_gate(freeze['expected_units'],[u.semantic_projection() for u in manifest.units])
 executor=CarrierNeutralResearchExecutor(repository=repo,release_refs=(release.release_ref,),runtime_catalog=fx['catalog'])
 calls=[];facts=[];discoveries=[];expected_results={}
 reqs={r.query_ref.key:r for r in fx['requests']}
 def query(unit):
  calls.append({'kind':'I03','job_ref':unit.job_ref.as_dict()})
  r=reqs[unit.job_ref.key]
  result=executor.execute_i03(query_ref=r.query_ref,predicate_ref=r.predicate_ref)
  facts.extend(result.facts)
  refs=tuple(f.ref for f in result.facts);expected_results[unit.unit_ref.key]=refs
  return ExecutionOutcome(refs,(release.release_ref,unit.job_ref))
 def discovery(unit):
  calls.append({'kind':'I05','job_ref':unit.job_ref.as_dict()})
  result=executor.execute_i05(discovery_authority_ref=unit.job_ref)
  discoveries.append(result)
  refs=tuple(r.ref for r in result.receipts);expected_results[unit.unit_ref.key]=refs
  return ExecutionOutcome(refs,(release.release_ref,unit.job_ref,result.evaluated_frontier_ref))
 runner=BatchExecutionRunner(manifest=manifest,repository=repo)
 binding=ExactRef('TEST_ONLY_NATIVE_EXECUTOR','urn:o35e:test-only:native-callback',_h('O35E-native-callback'))
 receipts=runner.run(executors={'QUERY':ExecutorBinding(binding,query),'DISCOVERY':ExecutorBinding(binding,discovery)})
 assert runner.summary().full_coverage,[(r.state,r.failure_code) for r in receipts]
 independent_gate([{'unit':key,'results':[r.as_dict() for r in sorted(refs,key=lambda x:x.key)]} for key,refs in expected_results.items()],
  [{'unit':r.unit_ref.key,'results':[v.as_dict() for v in sorted(r.result_refs,key=lambda x:x.key)]} for r in receipts])
 # Recheck expected-work outer join after actual execution, still before consumer.
 if consume:independent_gate(expected,[u.semantic_projection() for u in manifest.units])
 consumer=consumer_for(facts) if consume else None
 return {'claim':'TEST_ONLY__NOT_ORIGINAL_SURVEY','release_ref':release.release_ref.as_dict(),
  'source_identity':{'declared_sha256':fx['stream'].source_sha256,'physical_rows':fx['stream'].row_count,
   'physical_cells':'in-memory accepted test fixture; source hash is fixture-declared, NOT an actual survey checksum'},
  'manifest':manifest.semantic_projection(),'manifest_ref':manifest.manifest_ref.as_dict(),
  'batch_summary':asdict(runner.summary()),'unit_receipts':[r.projection() for r in receipts],
  'native_calls':calls,'facts':[f.as_dict() for f in facts],
  'discovery_receipts':[r.as_dict() for d in discoveries for r in d.receipts],
  'discovery_valid_empty':[d.valid_empty for d in discoveries],
  'consumer':consumer.as_dict() if consumer else None,
  'work_antijoin':{'missing':len(all_units)-len(picked),'extra':0},
  'ordinary_consumer_grade':'OC01 policy evidence selection only; no learned-world publication or N9/N10/N11/N12/V3'}

def dump(v,path):
 def default(x):
  if hasattr(x,'as_dict'):return x.as_dict()
  raise TypeError(type(x).__name__)
 path.write_text(json.dumps(v,indent=2,ensure_ascii=False,default=default)+'\n')

if __name__=='__main__':
 result=execute_native()
 dump(result,OBS/'native_positive.json')
 print(json.dumps({'actual_calls':[c['kind'] for c in result['native_calls']],
  'fact_states':[f['typed_state'] for f in result['facts']],
  'consumer':result['consumer']['state'],'coverage':result['batch_summary']['coverage_state']}))
