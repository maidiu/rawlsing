"""S3-A independent follow-up: forbidden positive query states and missing issuers.

Executes the exact unmodified #931 producer and its real D first consumer before
testing the repaired producer. Only sourcefree consistency is asserted; neither
valid hashes nor D's risk label constitute physical source/rights certification.
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
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, EmpiricalFact, EmpiricalQuerySpec, exact_ref, semantic_hash,
)
from rawlsing_next.tests.test_gt12_e2b_actual_object_consumer_harness import _objects

PRE_REPAIR_HEAD = "bcb3d5d913ac345d5adf7a9e45ca6d2eac9fb981"
PRE_REPAIR_FF_BLOB = "16b6c21746a14e37ae35a4ee9653c0dabb1a9079"


@pytest.fixture(scope="module")
def predecessor_ff():
    source = subprocess.run(
        ["git", "show", PRE_REPAIR_HEAD + ":rawlsing_next/field_forge_conditional_support.py"],
        capture_output=True, check=True,
    ).stdout
    observed_sha = subprocess.run(
        ["git", "hash-object", "--stdin"], input=source,
        capture_output=True, check=True,
    ).stdout.decode().strip()
    assert observed_sha == PRE_REPAIR_FF_BLOB
    name = "rawlsing_next._s3a_predecessor_exact_ff"
    module = types.ModuleType(name)
    module.__package__ = "rawlsing_next"
    sys.modules[name] = module
    try:
        exec(compile(source, name, "exec"), module.__dict__)
        yield module
    finally:
        sys.modules.pop(name, None)


def _rewrite_query(query, *, state=None, extra_use_authority=None):
    material = dict(query.semantic_fields)
    if extra_use_authority is not None:
        material["query_authority_refs"] = (
            *query.query_authority_refs, extra_use_authority,
        )
    return EmpiricalQuerySpec(
        typed_state=state or query.typed_state,
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=query.dependency_refs,
        producer_replay_locator_or_reference_root=query.producer_replay_locator_or_reference_root,
        **material,
    )


def _rebind_fact(fact, old_query, new_query):
    material = dict(fact.semantic_fields)
    material["empirical_query_spec_ref"] = new_query.ref
    dependencies = tuple(
        new_query.ref if exact_ref(ref) == old_query.ref else ref
        for ref in fact.dependency_refs
    )
    return EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=dependencies,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **material,
    )


def _produce(owner, q, f, conditioner, target):
    return owner.produce_exact_conditional_support_profile(
        joint_fact=f, joint_query=q,
        conditioner_ref=conditioner, target_ref=target,
        producer_permission_ceiling=(adm.GT2_TARGET_USE,),
        relation_permission_ceiling=(adm.GT2_TARGET_USE,),
    )


@pytest.mark.parametrize("kind", ["UNAUTHORIZED_QUERY", "MISSING_OPERATION_ISSUER"])
def test_exact_931_ff_mints_unauthorized_positive_d_but_repair_refuses(
    predecessor_ff, kind,
):
    original_q, original_f, conditioner, target = _objects()
    if kind == "UNAUTHORIZED_QUERY":
        changed_q = _rewrite_query(original_q, state="QUERY_UNAUTHORIZED")
        expected = "non-authorized query state"
    else:
        foreign = AuthorityRef(
            "S3A-UNISSUED-OPERATION", "R1",
            semantic_hash({"s3a": "unissued-operation-authority"}),
        )
        assert foreign not in original_f.authority_snapshot_refs
        changed_q = _rewrite_query(
            original_q, extra_use_authority=foreign,
        )
        expected = "query-specific authority refs"
    changed_f = _rebind_fact(original_f, original_q, changed_q)
    assert changed_f.typed_state == "SUPPORTED"
    assert exact_ref(changed_f.empirical_query_spec_ref) == changed_q.ref
    assert exact_ref(changed_f.risk_set_ref) == exact_ref(changed_q.risk_set_ref)
    assert semantic_hash(changed_q.semantic_projection()) == changed_q.content_hash
    assert semantic_hash(changed_f.semantic_projection()) == changed_f.content_hash

    old_result = _produce(predecessor_ff, changed_q, changed_f, conditioner, target)
    exact_d_type = ff.ExactConditionalSupportProfile(**{
        item.name: getattr(old_result, item.name)
        for item in fields(ff.ExactConditionalSupportProfile) if item.init
    })
    assert exact_d_type.ref == old_result.ref
    old_d = bridge.admit_gt12_c_relation(exact_d_type)
    assert old_d.admission.decision is adm.AdmissionDecision.ADMITTED

    with pytest.raises(ff.FieldForgeConditionalSupportError, match=expected):
        _produce(ff, changed_q, changed_f, conditioner, target)

    restored = _produce(ff, original_q, original_f, conditioner, target)
    assert bridge.admit_gt12_c_relation(
        restored,
    ).admission.decision is adm.AdmissionDecision.ADMITTED


def test_unissued_query_negative_remains_typed_and_not_admitted():
    original_q, original_f, conditioner, target = _objects(fact_state="OBSERVED_ZERO")
    foreign = AuthorityRef(
        "S3A-UNISSUED-NEGATIVE", "R1",
        semantic_hash({"s3a": "unissued-negative-authority"}),
    )
    changed_q = _rewrite_query(
        original_q, state="QUERY_UNAUTHORIZED",
        extra_use_authority=foreign,
    )
    changed_f = _rebind_fact(original_f, original_q, changed_q)
    relation = _produce(ff, changed_q, changed_f, conditioner, target)
    assert relation.typed_state == "OBSERVED_ZERO"
    assert relation.producer_state_blocking
    assert not relation.conditional_count_profile
    result = bridge.admit_gt12_c_relation(relation)
    assert result.admission.decision is not adm.AdmissionDecision.ADMITTED
    assert result.admission.target_use_permissions == ()
