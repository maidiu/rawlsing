from __future__ import annotations

from rawlsing_next.pre553_empirical_objects import EmpiricalFact, EmpiricalQuerySpec, exact_ref, semantic_hash
from rawlsing_next.pre553_repo_native_seal import load_current_gt2_query_fact


PREDICATE = "bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3"
QUERY = "e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0"
FACT = "540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46"
REPLAY = "c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f"


def test_real_current_no_library_load_checkpoint():
    query, fact = load_current_gt2_query_fact()

    assert type(query) is EmpiricalQuerySpec
    assert type(fact) is EmpiricalFact
    assert query.content_hash == QUERY
    assert fact.content_hash == FACT
    assert semantic_hash(query.semantic_projection()) == QUERY
    assert semantic_hash(fact.semantic_projection()) == FACT

    predicate = exact_ref(query.condition_predicate_ref, "query.condition_predicate_ref")
    replay = exact_ref(fact.replay_ref, "fact.replay_ref")
    assert predicate.content_hash == PREDICATE
    assert replay.content_hash == REPLAY
    assert exact_ref(fact.empirical_query_spec_ref, "fact.empirical_query_spec_ref") == query.ref
    assert exact_ref(fact.condition_predicate_ref, "fact.condition_predicate_ref") == predicate

    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 19_210

    targets = tuple(exact_ref(ref, "query.target_refs") for ref in query.target_refs)
    components = query.target_arity_and_topology["components"]
    component_refs = tuple(exact_ref(item["target_ref"], "component.target_ref") for item in components)
    assert targets == component_refs
    assert len(targets) == 2
    assert targets[0].object_id == "question_impl.phase0.2fb3a62609dad4c1306d"
    assert targets[1].object_id == "question_impl.phase0.67f036c0efb7fb98ff4a"
