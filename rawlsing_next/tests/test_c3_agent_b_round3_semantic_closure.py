"""C-3 Agent B round 3: cross-object semantic closure at FF01 first reader.

Sourcefree hostile construction. Historical module loaded from immutable
Agent A round-2 candidate, not an invented oracle. A passing historical
counterexample is not source-native / survey-use evidence.
"""
from __future__ import annotations

from dataclasses import fields
import subprocess
import sys
import types

import pytest

from rawlsing_next import field_forge_conditional_support as ff
from rawlsing_next import gt12_c_to_d_relation_bridge as bridge
from rawlsing_next import wave1_ff_prev3_relation_admission as adm
from rawlsing_next.pre553_empirical_objects import AuthorityRef, EmpiricalFact, EmpiricalQuerySpec, ExactRef, exact_ref, semantic_hash
from rawlsing_next.tests.test_gt12_e2b_actual_object_consumer_harness import _objects

R2_SHA = "265526a69c3a7a52365cf908709a4ef85ef9092e"
R2_BLOB = "583003dce5acf92ead1d67bab085ad5602c0990d"  # replaced after independent Git blob read

def _wrong(kind: str, mode: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:c3-r3:{mode}", semantic_hash({"c3-r3": mode}))


def _alter_fact(fact: EmpiricalFact, mode: str) -> EmpiricalFact:
    fields_map = dict(fact.semantic_fields)
    dependencies = tuple(fact.dependency_refs)
    if mode == "condition_predicate":
        replacement = _wrong("PREDICATE", mode)
        fields_map["condition_predicate_ref"] = replacement
        dependencies = (*dependencies, replacement)
    elif mode == "measure_basis":
        fields_map["measure_basis_ref"] = _wrong("MEASURE_BASIS", mode)
    elif mode == "response_semantics":
        fields_map["response_state_semantics_ref"] = _wrong("RESPONSE_STATE_SEMANTICS", mode)
    else:
        raise ValueError(mode)
    return EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=dependencies,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **fields_map,
    )


def _produce(module, query, fact, conditioner, target):
    return module.produce_exact_conditional_support_profile(
        joint_fact=fact, joint_query=query,
        conditioner_ref=conditioner, target_ref=target,
        producer_permission_ceiling=(adm.GT2_TARGET_USE,),
        relation_permission_ceiling=(adm.GT2_TARGET_USE,),
    )


@pytest.fixture(scope="module")
def agent_a_round2_ff():
    baseline = subprocess.run(
        ["git", "show", R2_SHA + ":rawlsing_next/field_forge_conditional_support.py"],
        check=True, capture_output=True,
    ).stdout
    identity = subprocess.run(
        ["git", "hash-object", "--stdin"], input=baseline,
        check=True, capture_output=True,
    ).stdout.decode().strip()
    assert identity == R2_BLOB
    name = "rawlsing_next._c3_b_round3_immutable_a_ff"
    module = types.ModuleType(name)
    module.__package__ = "rawlsing_next"
    sys.modules[name] = module
    try:
        exec(compile(baseline, name, "exec"), module.__dict__)
        yield module
    finally:
        sys.modules.pop(name, None)


@pytest.mark.parametrize("mode,expected", [
    ("condition_predicate", "condition predicate"),
    ("measure_basis", "measure basis"),
    ("response_semantics", "response-state semantics"),
])
def test_round2_ff_accepts_semantically_different_fact_but_round3_refuses(
    agent_a_round2_ff, mode, expected,
):
    query, original, conditioner, target = _objects()
    fact = _alter_fact(original, mode)
    assert fact.ref != original.ref
    assert semantic_hash(query.semantic_projection()) == query.content_hash
    assert semantic_hash(fact.semantic_projection()) == fact.content_hash
    assert exact_ref(fact.empirical_query_spec_ref) == query.ref
    assert exact_ref(fact.risk_set_ref) == exact_ref(query.risk_set_ref)

    previous = _produce(agent_a_round2_ff, query, fact, conditioner, target)
    # Convert isolated old module's exact object into real current downstream
    # typed ABI, without modifying semantic material.
    relation = ff.ExactConditionalSupportProfile(**{
        field.name: getattr(previous, field.name)
        for field in fields(ff.ExactConditionalSupportProfile) if field.init
    })
    assert relation.ref == previous.ref
    assert bridge.admit_gt12_c_relation(relation).admission.decision is adm.AdmissionDecision.ADMITTED

    with pytest.raises(ff.FieldForgeConditionalSupportError, match=expected):
        _produce(ff, query, fact, conditioner, target)

    restored = _produce(ff, query, original, conditioner, target)
    assert bridge.admit_gt12_c_relation(restored).admission.decision is adm.AdmissionDecision.ADMITTED


def test_retained_current_r1c_and_bound_first_reader_survive():
    from rawlsing_next.pre553_repo_native_current_payload import (
        load_current_gt2_query_fact_from_committed_transport,
    )
    q, f = load_current_gt2_query_fact_from_committed_transport()
    relation = _produce(ff, q, f, q.target_refs[0], q.target_refs[1])
    assert bridge.admit_gt12_c_relation_from_verified_current_objects(
        relation, joint_query=q, joint_fact=f,
    ).admission.decision is adm.AdmissionDecision.ADMITTED


def test_round2_allows_unresolved_query_to_mint_positive_ff_and_d(agent_a_round2_ff):
    query, fact, conditioner, target = _objects()
    unresolved = EmpiricalQuerySpec(
        typed_state="UNRESOLVED",
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=query.dependency_refs,
        producer_replay_locator_or_reference_root=query.producer_replay_locator_or_reference_root,
        **dict(query.semantic_fields),
    )
    semantics = dict(fact.semantic_fields)
    semantics["empirical_query_spec_ref"] = unresolved.ref
    updated_dependencies = tuple(
        unresolved.ref if exact_ref(ref) == query.ref else ref
        for ref in fact.dependency_refs
    )
    signed_fact = EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=updated_dependencies,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **semantics,
    )
    assert signed_fact.typed_state == "SUPPORTED"
    assert unresolved.typed_state == "UNRESOLVED"
    assert exact_ref(signed_fact.empirical_query_spec_ref) == unresolved.ref

    prior = _produce(agent_a_round2_ff, unresolved, signed_fact, conditioner, target)
    prior_as_current = ff.ExactConditionalSupportProfile(**{
        field.name: getattr(prior, field.name)
        for field in fields(ff.ExactConditionalSupportProfile) if field.init
    })
    assert bridge.admit_gt12_c_relation(prior_as_current).admission.decision is adm.AdmissionDecision.ADMITTED
    with pytest.raises(ff.FieldForgeConditionalSupportError,
                       match="positive fact cannot derive.*nonpositive query"):
        _produce(ff, unresolved, signed_fact, conditioner, target)
    restored = _produce(ff, query, fact, conditioner, target)
    assert bridge.admit_gt12_c_relation(restored).admission.decision is adm.AdmissionDecision.ADMITTED


def test_query_specific_issuance_authority_is_not_silently_dropped(agent_a_round2_ff):
    q, f, c, target = _objects()
    foreign = AuthorityRef(
        "UNISSUED-FOREIGN-QUERY-OPERATOR", "R1",
        semantic_hash({"c3-r3": "foreign-query-grant"}),
    )
    q_fields = dict(q.semantic_fields)
    q_fields["query_authority_refs"] = (foreign,)
    forged_query = EmpiricalQuerySpec(
        typed_state=q.typed_state,
        authority_snapshot_refs=q.authority_snapshot_refs,
        dependency_refs=q.dependency_refs,
        producer_replay_locator_or_reference_root=q.producer_replay_locator_or_reference_root,
        **q_fields,
    )
    fact_fields = dict(f.semantic_fields)
    fact_fields["empirical_query_spec_ref"] = forged_query.ref
    rewritten_deps = tuple(
        forged_query.ref if exact_ref(ref) == q.ref else ref
        for ref in f.dependency_refs
    )
    forged_fact = EmpiricalFact(
        typed_state=f.typed_state,
        authority_snapshot_refs=f.authority_snapshot_refs,
        dependency_refs=rewritten_deps,
        producer_replay_locator_or_reference_root=f.producer_replay_locator_or_reference_root,
        **fact_fields,
    )
    assert foreign not in f.authority_snapshot_refs
    assert forged_query.ref == exact_ref(forged_fact.empirical_query_spec_ref)
    old_relation = _produce(agent_a_round2_ff, forged_query, forged_fact, c, target)
    typed_relation = ff.ExactConditionalSupportProfile(**{
        item.name: getattr(old_relation, item.name)
        for item in fields(ff.ExactConditionalSupportProfile) if item.init
    })
    assert bridge.admit_gt12_c_relation(typed_relation).admission.decision is adm.AdmissionDecision.ADMITTED
    with pytest.raises(ff.FieldForgeConditionalSupportError,
                       match="query-specific authority refs"):
        _produce(ff, forged_query, forged_fact, c, target)
    restored = _produce(ff, q, f, c, target)
    assert bridge.admit_gt12_c_relation(restored).admission.decision is adm.AdmissionDecision.ADMITTED
