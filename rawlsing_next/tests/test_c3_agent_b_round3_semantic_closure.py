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
from rawlsing_next.pre553_empirical_objects import EmpiricalFact, ExactRef, exact_ref, semantic_hash
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
