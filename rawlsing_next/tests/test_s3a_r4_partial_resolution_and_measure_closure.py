"""S3-A R4 sourcefree hostile differential: FF01-positive must be I03-possible.

Actual immutable #936 FF01 is executed against the real current D first reader.
A content-addressed re-signature is NOT proof of original source validity. The
failure is the I03 internal semantic closure being discarded before D admission.
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
from rawlsing_next.pre553_empirical_objects import EmpiricalFact, canonicalize, semantic_hash
from rawlsing_next.tests.test_gt12_e2b_actual_object_consumer_harness import _objects

PRE_REPAIR_HEAD = "40529f300a3f655210f03d82532cb1e8b9b7c76c"
PRE_REPAIR_FF_BLOB = "62a93a34bf6bad7f77bd9eda11d1effb4187964f"


@pytest.fixture(scope="module")
def previous_owner():
    source = subprocess.run(
        ["git", "show", PRE_REPAIR_HEAD + ":rawlsing_next/field_forge_conditional_support.py"],
        capture_output=True, check=True,
    ).stdout
    old_blob = subprocess.run(
        ["git", "hash-object", "--stdin"], input=source,
        capture_output=True, check=True,
    ).stdout.decode().strip()
    assert old_blob == PRE_REPAIR_FF_BLOB
    name = "rawlsing_next._s3a_r4_exact_pre_repair_ff"
    module = types.ModuleType(name)
    module.__package__ = "rawlsing_next"
    sys.modules[name] = module
    try:
        exec(compile(source, name, "exec"), module.__dict__)
        yield module
    finally:
        sys.modules.pop(name, None)


def _re_sign(fact, changes):
    material = dict(fact.semantic_fields)
    material.update(changes)
    new = EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **material,
    )
    assert semantic_hash(new.semantic_projection()) == new.content_hash
    assert new.ref != fact.ref
    return new


def _produce(owner, query, fact, conditioner, target):
    return owner.produce_exact_conditional_support_profile(
        joint_fact=fact, joint_query=query,
        conditioner_ref=conditioner, target_ref=target,
        producer_permission_ceiling=(adm.GT2_TARGET_USE,),
        relation_permission_ceiling=(adm.GT2_TARGET_USE,),
    )


def _d_admits_old(owner, query, fact, conditioner, target):
    relation = _produce(owner, query, fact, conditioner, target)
    assert relation.typed_state == "SUPPORTED"
    current_type = ff.ExactConditionalSupportProfile(**{
        field.name: getattr(relation, field.name)
        for field in fields(ff.ExactConditionalSupportProfile) if field.init
    })
    assert current_type.ref == relation.ref
    receipt = bridge.admit_gt12_c_relation(current_type)
    assert receipt.admission.decision is adm.AdmissionDecision.ADMITTED
    return receipt


@pytest.mark.parametrize("mode,expected", [
    ("partial_target_resolution", "SUPPORTED.*fully resolved target denominator"),
    ("uncertainty_semantics", "query/fact uncertainty semantics mismatch"),
    ("raw_cell_with_weight", "RAW cell carries weighted support"),
])
def test_936_first_reader_admits_fact_that_i03_cannot_mark_supported(
    previous_owner, mode, expected,
):
    query, valid, conditioner, target = _objects()
    assert valid.raw_numerator_support == valid.raw_denominator_support
    if mode == "partial_target_resolution":
        # Positive numerator but one denominator member has no resolved target:
        # I03 _evaluate_index_group returns UNRESOLVED, not SUPPORTED.
        # D nevertheless stamps the *same* frozen risk-set label.
        bad = _re_sign(valid, {
            "raw_denominator_support": valid.raw_denominator_support + 1,
        })
        assert 0 < bad.raw_numerator_support < bad.raw_denominator_support
    elif mode == "uncertainty_semantics":
        grain = query.requested_output_grain
        assert grain["uncertainty_method_or_typed_state"] == valid.uncertainty_method_or_typed_state
        bad = _re_sign(valid, {
            "uncertainty_method_or_typed_state": "SELF_SIGNED_UNAUTHORIZED_UNCERTAINTY_METHOD",
        })
    else:
        topo = canonicalize(valid.target_topology)
        cells = topo["complete_cell_semantic_projection"]
        assert cells and all(row["weighted_numerator_support_if_authorized"] is None for row in cells)
        cells[0]["weighted_numerator_support_if_authorized"] = {"$exact_fraction": [7, 1]}
        bad = _re_sign(valid, {"target_topology": topo})
        assert bad.weighted_numerator_support_if_authorized is None
        assert bad.weighted_denominator_support_if_authorized is None

    # IMMUTABLE #936 producer, real D entrypoint and evaluator, not a mock:
    _d_admits_old(previous_owner, query, bad, conditioner, target)
    with pytest.raises(ff.FieldForgeConditionalSupportError, match=expected):
        _produce(ff, query, bad, conditioner, target)

    # No accidental blockade of legitimate full target resolution, RAW
    # no-weight observations or original query uncertainty meaning.
    restored = _produce(ff, query, valid, conditioner, target)
    assert bridge.admit_gt12_c_relation(
        restored,
    ).admission.decision is adm.AdmissionDecision.ADMITTED


def test_typed_nonpositive_conservation():
    q, f, c, t = _objects(fact_state="OBSERVED_ZERO")
    blocked = _produce(ff, q, f, c, t)
    assert blocked.typed_state == "OBSERVED_ZERO"
    assert blocked.producer_state_blocking
    assert not blocked.conditional_count_profile
    result = bridge.admit_gt12_c_relation(blocked)
    assert result.admission.decision is not adm.AdmissionDecision.ADMITTED
    assert result.admission.target_use_permissions == ()
