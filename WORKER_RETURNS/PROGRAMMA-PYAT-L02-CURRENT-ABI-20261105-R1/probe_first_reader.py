"""Consume exact R03 discovery results through existing current E41/C1/N10E."""
import json
from pathlib import Path
from probe_conditioned import run
from rawlsing_next.pre553_analytical_composition import _validate_discovery_consumption
from rawlsing_next.pre553_source_backed_c11_facade import build_source_backed_c11_repository
from rawlsing_next.pre553_universal_empirical_extension import provide_empirical_possibility_slice_ext
from rawlsing_next.pre553_empirical_objects import ExactRef,semantic_hash,canonicalize
from rawlsing_next.tests import c1_at08_at13_fixture as fx

OUTPUT=[]
def consume(direction,bundle,compilation,result):
 discovery=result.native_execution.native_result
 repository,release=build_source_backed_c11_repository(bundle.physical_stream,bundle.projection)
 wanted_arity=3 if direction=='FORWARD' else 1
 wanted_den=12 if direction=='FORWARD' else 4
 for receipt in discovery.receipts:
  if receipt.typed_state!='DISCOVERED_RESULT_SUPPORTED':continue
  fact,predicate,query=_validate_discovery_consumption(discovery_result=discovery,consumer_query=None,receipt_ref=receipt.ref)
  if fact.target_topology['arity']!=wanted_arity or fact.raw_denominator_support!=wanted_den:continue
  if direction=='REVERSE' and canonicalize(query.target_refs[0])!=bundle.question_refs['eligibility_group'].as_dict():continue
  break
 else:raise AssertionError('NO_EXACT_CONSUMABLE_DISCOVERY_RECEIPT')
 def leaves(node):
  if isinstance(node,dict):
   if node.get('op')=='LEAF' and node.get('leaf_type')=='SURVEY_RESPONSE_EVENT':return [node]
   return [leaf for value in node.values() for leaf in leaves(value)]
  if isinstance(node,(list,tuple)):return [leaf for child in node for leaf in leaves(child)]
  return []
 native_leaves=leaves(canonicalize(predicate.predicate_ast))
 pairs=[(ExactRef(**leaf['question_semantic_ref']),leaf['exact_value']) for leaf in native_leaves]
 assert pairs
 universe=bundle.projection.universes[0].ref
 pairing=fx.make_pairing_authority('l02-'+direction)
 by_ref={ref:name for name,ref in bundle.question_refs.items()}
 bindings=[fx.make_conditioner_binding(binding_id='condition-'+str(i),
   subject_fact_ref=ExactRef(**fx.subject_fact_ref({'qrefs':bundle.question_refs},by_ref[ref],value)),
   empirical_coordinate_ref=ref,comparability_authority_ref=pairing,
   source_universe_ref=universe,release_ref=release.release_ref) for i,(ref,value) in enumerate(pairs)]
 consumer=fx.make_multi_conditioner_consumer_query(query_id='l02-'+direction,
   subject_ref=ExactRef('SOURCEFREE_SUBJECT','urn:test:l02:subject',semantic_hash(direction)),
   target_ref=ExactRef(**canonicalize(query.target_refs[0])),source_universe_ref=universe,
   release_ref=release.release_ref,bindings=bindings,projection_kind='L02_CURRENT_KWAY')
 witness=fx.build_witness_for_binding(witness_object_id='urn:test:l02:witness:'+direction,
   consumer_query=consumer,producer_query=query,producer_predicate=predicate,bindings=bindings,
   coordinate_value_pairs=pairs,pairing_authority=pairing,source_universe_ref=universe,release_ref=release.release_ref)
 model=fx.make_model_rule(universe,'l02-'+direction)
 extension=provide_empirical_possibility_slice_ext(repository=repository,empirical_query=query,
   predicate=predicate,authority_registry=compilation.runtime_catalog.authority_registry,
   release_refs=(release.release_ref,),consumer_query=consumer,model_rule=model,
   condition_binding_witness=witness,discovery_result=discovery,discovery_receipt_ref=receipt.ref)
 assert extension.consumer_result_or_null.result_state=='EXACT_SUPPORTED'
 assert extension.composition_result.producer_fact_ref==fact.ref
 assert extension.composition_result.raw_denominator_support==wanted_den
 OUTPUT.append({'direction':direction,'fact_ref':fact.ref.as_dict(),'discovery_receipt_ref':receipt.ref.as_dict(),
  'query_ref':query.ref.as_dict(),'predicate_ref':predicate.ref.as_dict(),
  'extension':extension.material(),'consumer':extension.consumer_result_or_null.material()})

if __name__=='__main__':
 run(consume)
 Path(__file__).with_suffix('.json').write_text(json.dumps(OUTPUT,sort_keys=True,default=str,indent=2)+'\n')
 print(json.dumps([{'direction':row['direction'],'state':row['consumer']['result_state']} for row in OUTPUT]))
