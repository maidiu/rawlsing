"""S3-A round 5: sourcefree I03 respondent-extent closure before FF01->D.

Compare immutable #943 FF01 with the real D first consumer. A hash-valid,
self-signed fact is not native source evidence. We check only inequalities and
enumerable identities that the sourcefree fact *itself* declares. This cannot
authenticate whether a same-count forged population actually exists.
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
    EmpiricalFact, ExactRef, canonicalize, exact_ref, semantic_hash,
)
from rawlsing_next.tests.test_gt12_e2b_actual_object_consumer_harness import _objects

PREDECESSOR_HEAD = "59f1f69f894c1cac982e7385587b097d83235d37"
PREDECESSOR_FF_BLOB = "f1c529f9bbb6c3cc8d7ff45e55cc5877d2e98faa"


@pytest.fixture(scope="module")
def predecessor_owner():
    source = subprocess.run(
        ["git", "show", PREDECESSOR_HEAD + ":rawlsing_next/field_forge_conditional_support.py"],
        check=True, capture_output=True,
    ).stdout
    blob = subprocess.run(
        ["git", "hash-object", "--stdin"], input=source,
        check=True, capture_output=True,
    ).stdout.decode().strip()
    assert blob == PREDECESSOR_FF_BLOB
    name = "rawlsing_next._s3a_r5_immutable_predecessor"
    module = types.ModuleType(name)
    module.__package__ = "rawlsing_next"
    sys.modules[name] = module
    try:
        exec(compile(source, name, "exec"), module.__dict__)
        yield module
    finally:
        sys.modules.pop(name, None)


def _respondent(n, *, kind="C11Internal:RespondentIdentity"):
    return ExactRef(
        kind,
        f"urn:test:s3a:r5:respondent:{n}",
        semantic_hash({"s3a-r5-respondent": n, "kind": kind}),
    )


def _resign(fact, **updates):
    material = dict(fact.semantic_fields)
    material.update(updates)
    changed = EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **material,
    )
    assert semantic_hash(changed.semantic_projection()) == changed.content_hash
    return changed


def _compact_supported(fact, *, risk_members, denominator_members, omit=()):
    """Reduce *condition-selected* denominator to 3; never change risk identity."""
    material = dict(fact.semantic_fields)
    topology = canonicalize(fact.target_topology)
    counts = (2, 1, 0, 0)
    assert len(topology["complete_cell_semantic_projection"]) == len(counts)
    for row, count in zip(topology["complete_cell_semantic_projection"], counts):
        row["raw_numerator_support"] = count
        row["cell_state"] = (
            "OBSERVED_POSITIVE" if count else "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
        )
    material.update(
        target_topology=topology,
        raw_numerator_support=3,
        raw_denominator_support=3,
        raw_resolved_target_support=3,
    )
    if "risk_set_member_refs" not in omit:
        material["risk_set_member_refs"] = risk_members
    if "denominator_member_refs" not in omit:
        material["denominator_member_refs"] = denominator_members
    return _resign(fact, **material)


def _produce(owner, query, fact, c, t):
    return owner.produce_exact_conditional_support_profile(
        joint_fact=fact, joint_query=query,
        conditioner_ref=c, target_ref=t,
        producer_permission_ceiling=(adm.GT2_TARGET_USE,),
        relation_permission_ceiling=(adm.GT2_TARGET_USE,),
    )


def _previous_d_admitted(owner, query, fact, c, t):
    r = _produce(owner, query, fact, c, t)
    relation = ff.ExactConditionalSupportProfile(**{
        member.name: getattr(r, member.name)
        for member in fields(ff.ExactConditionalSupportProfile)
        if member.init
    })
    assert r.ref == relation.ref
    d = bridge.admit_gt12_c_relation(relation)
    assert d.admission.decision is adm.AdmissionDecision.ADMITTED
    return relation


@pytest.mark.parametrize("mode,reason", [
    ("short_denominator", "denominator member count mismatch"),
    ("duplicate_denominator", "duplicate denominator member"),
    ("outside_risk", "denominator member outside risk set"),
    ("duplicate_risk", "duplicate risk-set member"),
    ("orphan_risk_only", "risk-set and denominator members must be declared together"),
    ("orphan_denominator_only", "risk-set and denominator members must be declared together"),
    ("foreign_member_family", "respondent member kind mismatch"),
])
def test_943_self_signed_extent_d_admitted_but_ff01_repair_refuses(
    predecessor_owner, mode, reason,
):
    query, fact, c, t = _objects()
    r1, r2, r3, r4, outside = [_respondent(i) for i in range(5)]
    risk = (r1, r2, r3, r4)
    denom = (r1, r2, r3)
    omit = ()
    if mode == "short_denominator":
        denom = (r1, r2)
    elif mode == "duplicate_denominator":
        denom = (r1, r1, r2)
    elif mode == "outside_risk":
        denom = (r1, r2, outside)
    elif mode == "duplicate_risk":
        risk = (r1, r1, r2, r3)
    elif mode == "orphan_risk_only":
        omit = ("denominator_member_refs",)
    elif mode == "orphan_denominator_only":
        omit = ("risk_set_member_refs",)
    elif mode == "foreign_member_family":
        alien = _respondent("alien", kind="SOURCE_ARTIFACT")
        risk = (r1, r2, alien, r4)
        denom = (r1, r2, alien)
    bad = _compact_supported(
        fact, risk_members=risk, denominator_members=denom, omit=omit,
    )
    assert bad.typed_state == "SUPPORTED"
    assert bad.raw_denominator_support == 3
    assert bad.raw_numerator_support == 3
    assert bad.ref != fact.ref
    # Historical actual first consumer was D-positive, not merely a hash check.
    _previous_d_admitted(predecessor_owner, query, bad, c, t)
    with pytest.raises(ff.FieldForgeConditionalSupportError, match=reason):
        _produce(ff, query, bad, c, t)

    # Restore an actual allowed condition-selected subset of a larger risk set.
    good = _compact_supported(
        fact, risk_members=(r1, r2, r3, r4),
        denominator_members=(r1, r2, r3),
    )
    assert bridge.admit_gt12_c_relation(
        _produce(ff, query, good, c, t)
    ).admission.decision is adm.AdmissionDecision.ADMITTED


def test_no_declared_members_preserves_existing_sourcefree_synthetic_scaffold():
    q, fact, c, t = _objects()
    assert "risk_set_member_refs" not in fact.semantic_fields
    assert "denominator_member_refs" not in fact.semantic_fields
    # Existing historical bare sourcefree fixture remains a permitted *D-shaped*
    # test, not an I03 membership-certified physical-source fact.
    out = bridge.admit_gt12_c_relation(_produce(ff, q, fact, c, t))
    assert out.admission.decision is adm.AdmissionDecision.ADMITTED
    assert out.sourcefree_origin_path.endswith("ORIGIN_UNVERIFIED")


def test_observed_zero_remains_nonpromotable_even_without_member_extent():
    q, fact, c, t = _objects(fact_state="OBSERVED_ZERO")
    relation = _produce(ff, q, fact, c, t)
    result = bridge.admit_gt12_c_relation(relation)
    assert relation.typed_state == "OBSERVED_ZERO"
    assert result.admission.decision is not adm.AdmissionDecision.ADMITTED
    assert result.admission.target_use_permissions == ()


def test_retained_exact_current_q86_one_missing_member_before_d(
    predecessor_owner,
):
    """Actual committed 19,210-member Q86 sourcefree object, not a toy census.

    The re-signed *mutation* is adversarial synthetic, NOT original-SAV proof.
    """
    from rawlsing_next import pre553_repo_native_current_payload as payload

    query, fact = payload.load_current_gt2_query_fact_from_committed_transport()
    original = tuple(exact_ref(ref) for ref in fact.denominator_member_refs)
    risk = tuple(exact_ref(ref) for ref in fact.risk_set_member_refs)
    assert len(original) == fact.raw_denominator_support == 19_210
    assert set(original) == set(risk)

    one_missing = _resign(fact, denominator_member_refs=original[:-1])
    assert one_missing.ref != fact.ref
    relation = _previous_d_admitted(
        predecessor_owner, query, one_missing,
        query.target_refs[0], query.target_refs[1],
    )
    assert relation.producer_fact_ref == one_missing.ref
    with pytest.raises(ff.FieldForgeConditionalSupportError,
                       match="denominator member count mismatch"):
        _produce(ff, query, one_missing, query.target_refs[0], query.target_refs[1])
    # The existing strict-current path never accepted the changed exact fact.
    with pytest.raises(bridge.GT12CToDBridgeError):
        bridge.admit_gt12_c_relation_from_verified_current_objects(
            relation, joint_query=query, joint_fact=one_missing,
        )

    restored = _produce(ff, query, fact, query.target_refs[0], query.target_refs[1])
    out = bridge.admit_gt12_c_relation_from_verified_current_objects(
        restored, joint_query=query, joint_fact=fact,
    )
    assert out.admission.decision is adm.AdmissionDecision.ADMITTED
    assert out.sourcefree_origin_path == "EXACT_PINNED_R1C_TRANSPORT_CONTENT__SOURCEFREE_ONLY"
