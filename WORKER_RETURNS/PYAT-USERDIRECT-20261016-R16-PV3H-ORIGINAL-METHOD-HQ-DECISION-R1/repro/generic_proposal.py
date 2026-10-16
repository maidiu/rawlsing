"""Lossless native I03 proposal-input reader; no Field Forge relation issuance.

Values come from native facts before the specialized Field Forge projection.
No accepted relation is relabeled, and no generic semantic principal is assumed.
"""
import bootstrap
from copy import deepcopy
from rawlsing_next.pre553_empirical_objects import semantic_hash, canonical_json
SCHEMA='GENERIC_TWO_BINARY_ITEM_CONDITIONAL_SUPPORT_METHOD_PROPOSAL@1'
class ProposalInputHold(ValueError):pass
def require(ok,why):
 if not ok:raise ProposalInputHold(why)

def derive_entry(link,facts,decision):
 identity=link['original_identity'];o=identity['original'];op=identity['operation'];m=link['consumer_material']
 require(semantic_hash(identity)==link['original_expected_work_key'],'ORIGINAL_OPERATION_IDENTITY_MISMATCH')
 require(decision['namespace']==o['respondent_namespace'] and not decision['withdrawn'],'NAMESPACE_OR_CURRENT_USE_DENIED')
 require(decision['edition']==o['source_release_ref']['content_hash'] and list(decision['ceiling'])==['SOURCE_FREE_DEV'],'SOURCE_EDITION_OR_PERMISSION_MISMATCH')
 require(o['respondent_unit']=='TEST_ONLY_ADULT' and len(o['native_item_refs'])==2 and o['option_scope']==['0','1'],'ORIGINAL_GRAIN_OR_DOMAIN_UNSUPPORTED')
 if op['slot']=='DISCOVERY':
  require(list(op['semantic_roles'])==['BASE'] and not op['condition_order'],'DISCOVERY_ROLE_IDENTITY_MISMATCH')
 else:
  require(list(op['semantic_roles'])==['CONDITIONER','TARGET'] and len(op['condition_order'])==2 and len(set(op['condition_order']))==2,'ROLE_BINDING_MISSING')
 require(m['producer_fact_ref']==link['producer_result_ref'],'FACT_BINDING_MISMATCH')
 matching=[f for f in facts if f['ref']==link['producer_result_ref'] and f['query_ref']==m['producer_query_ref']]
 require(bool(matching),'ACTUAL_NATIVE_FACT_OR_QUERY_MISSING');fact=matching[0];projection=fact['projection'];query=fact['query'];sf=projection['semantic_fields'];q=query['semantic_fields']
 require(semantic_hash(projection)==fact['ref']['content_hash'] and semantic_hash(query)==fact['query_ref']['content_hash'],'NATIVE_FACT_OR_QUERY_HASH_MISMATCH')
 require(q['target_refs']==o['native_item_refs'],'ORIGINAL_NATIVE_TARGET_ORDER_MISMATCH')
 require(canonical_json(sf['risk_set_ref'])==canonical_json(m['risk_set_ref']) and canonical_json(sf['empirical_universe_refs'])==canonical_json(m['empirical_universe_refs'])==canonical_json([o['empirical_universe_ref']]),'RISK_OR_UNIVERSE_MISMATCH')
 require(sf['empirical_query_spec_ref']==fact['query_ref'],'NATIVE_FACT_QUERY_MISMATCH')
 components=q['target_arity_and_topology']['components']
 require(len(components)==2 and all(x['domain']==['0','1'] and x['included_states']==['SUBSTANTIVE_RESPONSE'] for x in components),'UNSUPPORTED_MISSING_OR_OPTION_CODING')
 require(q['requested_output_grain']['measure_kind']=='RAW' and sf['measure_kind']=='RAW','UNISSUED_WEIGHT_OR_PROBABILITY')
 require(list(m['producer_permission_ceiling'])==list(m['relation_permission_ceiling'])==['SOURCE_FREE_DEV'],'CEILING_WIDENING')
 entry=dict(schema=SCHEMA,kind='PROPOSAL_INPUT_EVIDENCE_NOT_FIELD_FORGE_RELATION',expected_work_key=link['original_expected_work_key'],namespace=o['respondent_namespace'],slot=op['slot'],original_scope=deepcopy(identity),native_item_refs=deepcopy(o['native_item_refs']),native_role_order=deepcopy(op['condition_order']),native_role_binding_source=('Original DISCOVERY BASE plus actual winning query order; generic target/conditioner binding NOT issued' if op['slot']=='DISCOVERY' else 'Exact original TEST_ONLY operation declaration; no generic semantic signature'),query_ref=deepcopy(fact['query_ref']),fact_ref=deepcopy(fact['ref']),condition_predicate_ref=deepcopy(sf['condition_predicate_ref']),risk_set_ref=deepcopy(sf['risk_set_ref']),empirical_universe_refs=deepcopy(sf['empirical_universe_refs']),fact_typed_state=projection['typed_state'],native_fact_cells=deepcopy(sf['target_topology']['complete_cell_semantic_projection']),raw_denominator_support=sf['raw_denominator_support'],raw_resolved_target_support=sf['raw_resolved_target_support'],native_topology=deepcopy(q['target_arity_and_topology']),measure_basis_ref=deepcopy(sf['measure_basis_ref']),response_state_semantics_ref=deepcopy(sf['response_state_semantics_ref']),uncertainty=sf['uncertainty_method_or_typed_state'],source_provenance_refs=deepcopy(sf['source_empirical_provenance_refs']),producer_replay_ref=deepcopy(sf['replay_ref']),native_authorities=deepcopy(projection['authority_snapshot_refs']),current_decision=deepcopy(decision),actual_P01_unit=deepcopy(link['batch_unit_ref']),specialized_comparator_ref=deepcopy(link['consumer_ref']),proposed_generic_relation='GENERIC_NATIVE_SEMANTICS_HOLD',issuer_signature=None)
 entry['evidence_hash']=semantic_hash(entry);return entry

def build_proposal(api,register,report,trace,namespace=None):
 # Real owner validation, not a serialized "allowed" bit supplied by caller.
 current=api.read_current_consumer_material(register,report,namespace=namespace)
 entries=[derive_entry(x,trace['I03'],current['current_decisions'][x['original_identity']['original']['respondent_namespace']]) for x in current['links']]
 held=[dict(expected_work_key=x['expected_work_key'],exact_native_held=deepcopy(x),hold='ORDERED_OWNER_NOT_ISSUED') for x in report['nonrunnable']]
 return dict(schema=SCHEMA,status='TEST_ONLY_METHOD_PROPOSAL_INPUTS_READ',entries=entries,held=held,expected_root=report['pv3_custody']['expected_root'],denied_namespaces=current['denied_namespaces'],generic_relation='GENERIC_NATIVE_SEMANTICS_HOLD',HQ_adoption=None,semantic_signature=None)
