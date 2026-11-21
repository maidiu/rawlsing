"""HQR R3 S3-A: exact FF01 query/fact closure before the C-to-D projection.

SOURCEFREE differential only. A self-re-signed EmpiricalFact is NOT an original
survey result or proof of physical-source tampering. The test exposes a
pre-existing internal inconsistency that the relation projection loses.
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
from rawlsing_next.pre553_empirical_objects import EmpiricalFact, ExactRef, semantic_hash
from rawlsing_next.tests.test_gt12_e2b_actual_object_consumer_harness import _objects

INHERITED_HEAD = "265526a69c3a7a52365cf908709a4ef85ef9092e"
INHERITED_FF_BLOB = "583003dce5acf92ead1d67bab085ad5602c0990d"


@pytest.fixture(scope="module")
def inherited_ff():
    original = subprocess.run(
        ["git", "show",
         INHERITED_HEAD + ":rawlsing_next/field_forge_conditional_support.py"],
        check=True, capture_output=True,
    ).stdout
    actual_blob = subprocess.run(
        ["git", "hash-object", "--stdin"],
        input=original, check=True, capture_output=True,
    ).stdout.decode().strip()
    assert actual_blob == INHERITED_FF_BLOB
    name = "rawlsing_next._hqr_s3a_inherited_ff"
    module = types.ModuleType(name)
    module.__package__ = "rawlsing_next"
    sys.modules[name] = module
    try:
        exec(compile(original, name, "exec"), module.__dict__)
        yield module
    finally:
        sys.modules.pop(name, None)


def _resign_fact(fact, key, value):
    payload = dict(fact.semantic_fields)
    payload[key] = value
    return EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=(
            fact.producer_replay_locator_or_reference_root),
        **payload,
    )


def _produce(owner, query, fact, conditioner, target):
    return owner.produce_exact_conditional_support_profile(
        joint_fact=fact, joint_query=query,
        conditioner_ref=conditioner, target_ref=target,
        producer_permission_ceiling=(adm.GT2_TARGET_USE,),
        relation_permission_ceiling=(adm.GT2_TARGET_USE,),
    )


@pytest.mark.parametrize("dimension,field,kind", [
    ("predicate", "condition_predicate_ref", "PREDICATE"),
    ("measure", "measure_basis_ref", "MEASURE_BASIS"),
    ("response_semantics", "response_state_semantics_ref", "RESPONSE_STATE_SEMANTICS"),
    ("risk_type", "risk_set_type", ""),
])
def test_original_ff01_to_d_admitted_inconsistent_query_fact_but_repair_refuses(
    inherited_ff, dimension, field, kind,
):
    query, fact, conditioner, target = _objects()
    value = (
        ExactRef(kind, "urn:test:hqr-s3a:wrong-" + dimension, semantic_hash({"s3a-incompatible": dimension}))
        if kind else "INCOMPATIBLE_RISK_SET_TYPE"
    )
    changed = _resign_fact(fact, field, value)
    assert changed.ref != fact.ref
    assert changed.empirical_query_spec_ref == fact.empirical_query_spec_ref
    assert changed.risk_set_ref == fact.risk_set_ref

    # Historical immutable HEAD is executed, not asserted from a text diff.
    old_relation = _produce(inherited_ff, query, changed, conditioner, target)
    compatible_type = ff.ExactConditionalSupportProfile(**{
        member.name: getattr(old_relation, member.name)
        for member in fields(ff.ExactConditionalSupportProfile) if member.init
    })
    old_d = bridge.admit_gt12_c_relation(compatible_type)
    assert old_d.admission.decision is adm.AdmissionDecision.ADMITTED
    assert old_d.evidence.relation_ref == compatible_type.ref

    # The repaired FF01 owner must prevent D from ever seeing the inconsistent
    # typed object; no new D scientific, source or authority grant is minted.
    with pytest.raises(ff.FieldForgeConditionalSupportError, match="query/fact .* mismatch"):
        _produce(ff, query, changed, conditioner, target)

    # A valid sourcefree companion still reaches the actual D first consumer.
    correct = _produce(ff, query, fact, conditioner, target)
    assert bridge.admit_gt12_c_relation(correct).admission.decision is adm.AdmissionDecision.ADMITTED
