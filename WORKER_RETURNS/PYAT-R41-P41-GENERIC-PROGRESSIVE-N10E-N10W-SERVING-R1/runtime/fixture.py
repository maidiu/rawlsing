"""TEST_ONLY native production and explicit fixture lifecycle bindings, not issuance."""
from dataclasses import dataclass
from unittest.mock import patch
import bootstrap
from rawlsing_next import pre553_n9_n10w_progressive_candidate as e03
from product.service import GenericSelectedWorldService
from rawlsing_next import pre553_empirical_query as pq
from rawlsing_next import pre553_empirical_objects as eo
from rawlsing_next import pre553_learned_empirical_adjudication as m1
from rawlsing_next import pre553_learned_product_release as m2
from rawlsing_next import pre553_learned_product_lifecycle as b5
from rawlsing_next import pre553_learned_world_composition as i4
from rawlsing_next.tests.test_pre553_empirical_query import _auth,_ref
from rawlsing_next.tests.test_pre553_learned_empirical_adjudication import _binding,_registry,CLAIM_FAMILY,CLAIM_RULE

CONDITIONS=(('A',1),('B',1),('C',1))
def ref(kind,tag):
    h=eo.semantic_hash([kind,tag]);return eo.ExactRef(kind,'urn:test:e04l:'+kind+':'+h,h)

@dataclass
class Prepared:
    service: object
    snapshot: object
    repository: object
    lifecycle: object
    composition: object
    objects: dict
    records: dict
    native_provider: object
    contract: object

def prepare(*,same_marginals=False,support_loss=False,measured_null=False):
    if measured_null:
        rows=[]
        for a in (0,1):
            for b in (0,1):
                for c in (0,1):
                    for y in (0,1):
                        for n in range(4):rows.append(dict(id=f'n{a}{b}{c}{y}{n}',responses=dict(A=a,B=b,C=c,Y=y)))
        with patch.object(e03,'synthetic_world_rows',return_value=rows):service=GenericSelectedWorldService()
    else:service=GenericSelectedWorldService(same_marginals=same_marginals,support_loss=support_loss)
    provider=service.provider;world=provider.world;s=world['source']
    objects={};records={};facts=[];queries=[];predicates=[];receipts=[]
    discovery_auth=_auth('e04l-discovery','DISCOVERY_FRONTIER',families=('EmpiricalFact@1.0.0','EmpiricalQuerySpec@1.0.0','EmpiricalPredicate@1.0.0'))
    grammar=_ref('Grammar','e04l-exact-prefixes')
    discovery=eo.DiscoveryAuthority(typed_state='EXACT_BOUNDED_AUTHORIZED',authority_snapshot_refs=(discovery_auth.authority_ref,),dependency_refs=(),producer_replay_locator_or_reference_root=_ref('REPLAY_ROOT','e04l-discovery'),candidate_grammar_ref=grammar,candidate_universe_definition={'target':'Y','ordered_prefixes':[[list(x) for x in CONDITIONS[:n]] for n in (1,2,3)]},source_universe_scope='EXPLICIT_UNRESTRICTED',risk_set_scope='EXPLICIT_UNRESTRICTED',topology_scope='BINARY_Y_ON_EXACT_ABC_PREFIXES',measure_scope='RAW',support_rules={'minimum':1},validation_rules={'contract':'PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0'},coverage_claim='COMPLETE_FOR_EXACT_DECLARED_FRONTIER',pruning_contract={'none':True},algorithm_identity_if_semantically_required='E04L_DIRECT_C11@1.0.0',tie_order_rules={'order':'CANONICAL'},rng_policy_if_any=None,mode='EXACT_BOUNDED')
    for n in (1,2,3):
        conditions=CONDITIONS[:n];step=provider.step('Y',conditions)
        predicate=e03._joint_predicate(world,conditions);query=e03._producer_query(world,predicate,'Y')
        result=pq.execute_empirical_query(repository=s['repo'],query=query,predicate=predicate,authority_registry=world['registry'],release_refs=(s['release_ref'],))
        fact=result.facts[0]
        if fact.ref.as_dict()!=step['producer_fact_ref']:raise ValueError('NATIVE_PRODUCER_FACT_MISMATCH')
        facts.append(fact);queries.append(query);predicates.append(predicate)
        for obj in (fact,query,predicate):objects[obj.ref.key]=obj
        records[('Y',conditions)]=dict(fact_ref=fact.ref,query_ref=query.ref,predicate_ref=predicate.ref,template=step,template_hash=eo.semantic_hash(step))
        receipt=eo.DiscoveryResultReceipt(typed_state='DISCOVERED_RESULT_SUPPORTED' if fact.typed_state=='SUPPORTED' else 'INSUFFICIENT_SUPPORT',authority_snapshot_refs=(discovery_auth.authority_ref,),dependency_refs=(discovery.ref,ref('Frontier',str(n)),predicate.ref,query.ref,fact.ref,grammar),producer_replay_locator_or_reference_root=_ref('REPLAY_ROOT','e04l-'+str(n)),discovery_authority_ref=discovery.ref,candidate_identity={'query_roles':[{'predicate_ref':predicate.ref,'query_ref':query.ref}]},winning_predicate_ref=predicate.ref,empirical_fact_refs=(fact.ref,),validation_fact_refs=(),coverage_state='EVALUATED_SUPPORTED' if fact.typed_state=='SUPPORTED' else 'EVALUATED_VALID_EMPTY',evaluated_frontier_ref=ref('Frontier',str(n)),branch_or_parent_ancestry_refs=(),support_uncertainty_state=fact.typed_state,replay_ref=ref('Replay',fact.content_hash))
        receipts.append(receipt)
    validator_auth=_auth('e04l-validator','TARGET_USE_PERMISSION',families=('EmpiricalFact@1.0.0',));binding=_binding(validator_auth)
    bundle=m1.build_m1_adjudication_input_bundle(requested_claim_family_id=CLAIM_FAMILY,requested_claim_rule_id=CLAIM_RULE,selected_discovery_receipts=receipts,discovery_authority_catalog=(discovery,),empirical_fact_catalog=facts,empirical_query_catalog=queries,empirical_predicate_catalog=predicates,authority_snapshots=(*world['registry']._by_key.values(),discovery_auth,validator_auth),requested_scope={'fixture':'E04L_TEST_ONLY_PREFIX_READTHROUGH'},additional_dependency_refs=(s['release_ref'],))
    disposition=m1.adjudicate_learned_empirical(bundle,binding,validator_registry=_registry(binding))
    if disposition.adjudication_outcome!='RULE_SATISFIED':raise ValueError(disposition.reason_code)
    objects[disposition.ref.key]=disposition
    contract=i4.LearnedWorldProductContractBinding(route='M1_M2_B5',product_family_ref=ref('ProductFamily','e04l'),producer_owner_ref=ref('ProducerOwner','m1'),producer_contract_ref=i4.M1_DISPOSITION_PRODUCER_CONTRACT_REF,release_subject_kind='TYPED_DISPOSITION',selection_scope_ref=ref('SelectionScope','e04l'),producer_permission_ceiling_ref=ref('PermissionCeiling','E04_TEST_ONLY'),consumer_product_purpose_ref=ref('ConsumerPurpose','NONPARENT_OPTIONS'),m1_family_rule_binding_ref=binding.ref,lifecycle_actions=('REGISTER','PUBLISH','SELECT_CURRENT'),registration_event_authority_ref=ref('LifecycleAuthority','register'),registration_event_rule_ref=ref('LifecycleRule','register'),publication_event_authority_ref=ref('LifecycleAuthority','publish'),publication_event_rule_ref=ref('LifecycleRule','publish'),selection_purpose_ref=ref('SelectionPurpose','serve'),selection_event_authority_ref=ref('LifecycleAuthority','select'),selection_event_rule_ref=ref('LifecycleRule','select'),selection_attestation_ref=ref('SelectionAttestation','select'))
    repository=m2.M2Repository();lifecycle=b5.LearnedProductLifecycleExecutor()
    composition=i4.compose_learned_world(contract,m2_repository=repository,lifecycle_executor=lifecycle,m1_disposition=disposition)
    if composition.receipt.terminal_state!='RULE_SATISFIED':raise ValueError(composition.receipt.reason_code)
    return Prepared(service,service.select(mode='AS_OF',valid_at='2027-09-01',published_asof='2027-09-01'),repository,lifecycle,composition,objects,records,provider,contract)
