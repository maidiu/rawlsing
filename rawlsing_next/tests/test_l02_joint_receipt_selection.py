"""Regression for an I05 joint receipt containing same-predicate marginal facts."""
from types import SimpleNamespace as NS
import pytest
from rawlsing_next.pre553_empirical_objects import ExactRef,semantic_hash
from rawlsing_next.pre553_analytical_composition import (
    _validate_discovery_consumption,DiscoveryConsumptionMismatch,
)


def ref(tag):return ExactRef('L02_TEST', 'urn:test:l02:'+tag,semantic_hash(tag))


def case():
    predicate=NS(ref=ref('predicate'))
    joint_query=NS(ref=ref('joint-query'),condition_predicate_ref=predicate.ref)
    marginal_query=NS(ref=ref('marginal-query'),condition_predicate_ref=predicate.ref)
    joint=NS(ref=ref('joint-fact'),condition_predicate_ref=predicate.ref,
             empirical_query_spec_ref=joint_query.ref)
    marginal=NS(ref=ref('marginal-fact'),condition_predicate_ref=predicate.ref,
                empirical_query_spec_ref=marginal_query.ref)
    receipt=NS(ref=ref('receipt'),typed_state='DISCOVERED_RESULT_SUPPORTED',
       winning_predicate_ref=predicate.ref,empirical_fact_refs=(marginal.ref,joint.ref),
       candidate_identity={'query_roles':[
           {'role':'JOINT','query_ref':joint_query.ref,'predicate_ref':predicate.ref},
           {'role':'MARGINAL_0','query_ref':marginal_query.ref,'predicate_ref':predicate.ref}]})
    discovery=NS(receipts=(receipt,),executed_predicates=(predicate,),
        executed_queries=(joint_query,marginal_query),empirical_facts=(marginal,joint))
    return discovery,receipt,joint,joint_query


@pytest.mark.parametrize('reverse',[False,True])
def test_declared_joint_is_selected_independently_of_fact_order(reverse):
    discovery,receipt,joint,query=case()
    if reverse:receipt.empirical_fact_refs=tuple(reversed(receipt.empirical_fact_refs))
    actual,_,actual_query=_validate_discovery_consumption(
        discovery_result=discovery,consumer_query=None,receipt_ref=receipt.ref)
    assert actual is joint
    assert actual_query is query


def test_missing_declared_joint_never_substitutes_a_supported_marginal():
    discovery,receipt,joint,_=case()
    receipt.empirical_fact_refs=tuple(ref for ref in receipt.empirical_fact_refs if ref!=joint.ref)
    with pytest.raises(DiscoveryConsumptionMismatch):
        _validate_discovery_consumption(discovery_result=discovery,consumer_query=None,receipt_ref=receipt.ref)


def test_ambiguous_primary_queries_refuse_instead_of_choosing_first():
    discovery,receipt,_,_=case()
    receipt.candidate_identity['query_roles'][1]['role']='JOINT'
    with pytest.raises(DiscoveryConsumptionMismatch):
        _validate_discovery_consumption(discovery_result=discovery,consumer_query=None,receipt_ref=receipt.ref)
