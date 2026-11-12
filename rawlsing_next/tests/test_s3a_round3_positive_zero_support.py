"""S3-A relay: a nominally SUPPORTED zero joint fact must not be D-positive.

Real immutable #933 FF01 and real current D bridge are executed. This is a
sourcefree typed-state conservation attack, *not* an original35 source claim.
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
    EmpiricalFact, EmpiricalQuerySpec, canonicalize, exact_ref, semantic_hash,
)
from rawlsing_next.tests.test_gt12_e2b_actual_object_consumer_harness import _objects

BASE = "16a347ce308345b7d0c18b8f81b9af15b754d2b6"
BASE_FF_BLOB = "2d4371843b4b61e6a0ff387ab45c23e0fef102a1"


@pytest.fixture(scope="module")
def previous_owner():
    source = subprocess.run(
        ["git", "show", BASE + ":rawlsing_next/field_forge_conditional_support.py"],
        check=True, capture_output=True,
    ).stdout
    blob = subprocess.run(["git", "hash-object", "--stdin"], input=source,
                          capture_output=True, check=True).stdout.decode().strip()
    assert blob == BASE_FF_BLOB
    name = "rawlsing_next._s3a_previous_owner_zero"
    module = types.ModuleType(name)
    module.__package__ = "rawlsing_next"
    sys.modules[name] = module
    try:
        exec(compile(source, name, "exec"), module.__dict__)
        yield module
    finally:
        sys.modules.pop(name, None)


def _resign_supported_zero(fact):
    payload = dict(fact.semantic_fields)
    topology = canonicalize(payload["target_topology"])
    cells = topology["complete_cell_semantic_projection"]
    assert cells and sum(row["raw_numerator_support"] for row in cells) > 0
    for row in cells:
        row["raw_numerator_support"] = 0
        row["cell_state"] = "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
    payload["target_topology"] = topology
    payload["raw_numerator_support"] = 0
    payload["raw_resolved_target_support"] = 0
    changed = EmpiricalFact(
        typed_state="SUPPORTED",
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **payload,
    )
    assert changed.raw_denominator_support > 0
    assert changed.raw_numerator_support == 0
    assert semantic_hash(changed.semantic_projection()) == changed.content_hash
    return changed


def _produce(module, query, fact, conditioner, target):
    return module.produce_exact_conditional_support_profile(
        joint_fact=fact, joint_query=query,
        conditioner_ref=conditioner, target_ref=target,
        producer_permission_ceiling=(adm.GT2_TARGET_USE,),
        relation_permission_ceiling=(adm.GT2_TARGET_USE,),
    )


def test_exact_933_ff_mints_positive_with_zero_joint_support(previous_owner):
    query, fact, conditioner, target = _objects()
    zero = _resign_supported_zero(fact)
    assert zero.ref != fact.ref
    historical = _produce(previous_owner, query, zero, conditioner, target)
    assert historical.typed_state == "SUPPORTED"
    assert historical.conditional_count_profile
    assert sum(row["condition_denominator_support"]
               for row in historical.conditional_count_profile) == 0
    carried = ff.ExactConditionalSupportProfile(**{
        member.name: getattr(historical, member.name)
        for member in fields(ff.ExactConditionalSupportProfile) if member.init
    })
    admitted = bridge.admit_gt12_c_relation(carried)
    assert admitted.admission.decision is adm.AdmissionDecision.ADMITTED

    with pytest.raises(ff.FieldForgeConditionalSupportError, match="zero positive support"):
        _produce(ff, query, zero, conditioner, target)

    restored = _produce(ff, query, fact, conditioner, target)
    assert bridge.admit_gt12_c_relation(restored).admission.decision is adm.AdmissionDecision.ADMITTED


def test_actual_observed_zero_remains_typed_and_not_admitted():
    query, fact, conditioner, target = _objects(fact_state="OBSERVED_ZERO")
    negative = _produce(ff, query, fact, conditioner, target)
    assert negative.typed_state == "OBSERVED_ZERO"
    assert not negative.conditional_count_profile
    out = bridge.admit_gt12_c_relation(negative)
    assert out.admission.decision is not adm.AdmissionDecision.ADMITTED
    assert out.admission.target_use_permissions == ()


def test_exact_933_ff_promotes_query_with_no_operation_authority(previous_owner):
    """I03 rejects empty query_authority_refs; the #933 subset check does not."""
    query, fact, conditioner, target = _objects()
    material = dict(query.semantic_fields)
    material["query_authority_refs"] = ()
    changed_q = EmpiricalQuerySpec(
        typed_state=query.typed_state,
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=query.dependency_refs,
        producer_replay_locator_or_reference_root=query.producer_replay_locator_or_reference_root,
        **material,
    )
    assert not changed_q.query_authority_refs
    fact_material = dict(fact.semantic_fields)
    fact_material["empirical_query_spec_ref"] = changed_q.ref
    deps = tuple(
        changed_q.ref if exact_ref(dep) == query.ref else dep
        for dep in fact.dependency_refs
    )
    changed_f = EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=deps,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **fact_material,
    )
    assert semantic_hash(changed_q.semantic_projection()) == changed_q.content_hash
    assert semantic_hash(changed_f.semantic_projection()) == changed_f.content_hash
    assert exact_ref(changed_f.empirical_query_spec_ref) == changed_q.ref

    old_r = _produce(previous_owner, changed_q, changed_f, conditioner, target)
    old_d_type = ff.ExactConditionalSupportProfile(**{
        member.name: getattr(old_r, member.name)
        for member in fields(ff.ExactConditionalSupportProfile) if member.init
    })
    assert bridge.admit_gt12_c_relation(
        old_d_type,
    ).admission.decision is adm.AdmissionDecision.ADMITTED

    with pytest.raises(ff.FieldForgeConditionalSupportError,
                       match="positive query lacks operation-specific authority refs"):
        _produce(ff, changed_q, changed_f, conditioner, target)

    restored = _produce(ff, query, fact, conditioner, target)
    assert bridge.admit_gt12_c_relation(
        restored,
    ).admission.decision is adm.AdmissionDecision.ADMITTED
