"""C-3 Agent A: source contradiction lost BEFORE GT12 C->D provenance projection.

Strictly sourcefree. Executes the genuine frozen protected FF01 implementation
at its immutable blob, demonstrating the B-era C->D-only guard cannot see
contradictory SOURCE_ARTIFACT claims in the upstream query/fact dependency DAG.
No original35 native/scientific/actor authority is asserted.
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
    EmpiricalFact, EmpiricalQuerySpec, ExactRef, exact_ref, semantic_hash,
)
from rawlsing_next.tests.test_gt12_e2b_actual_object_consumer_harness import _objects

PROTECTED = "6a5c12f04323d74001f9632063ec907f4fc4468e"
OLD_FF_BLOB = "a70decb20747d84cbcbe27d1280babc6de88ef33"


def _source(label):
    return ExactRef("SOURCE_ARTIFACT", "Data/not-Afrobarometer-R5.sav",
                    semantic_hash({"c3_agent_a_wrong_source": label}))


def _rebuild_query(query, dependencies):
    return EmpiricalQuerySpec(
        typed_state=query.typed_state,
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=tuple(dependencies),
        producer_replay_locator_or_reference_root=(
            query.producer_replay_locator_or_reference_root),
        **dict(query.semantic_fields),
    )


def _rebuild_fact(fact, query, dependencies, *, provenance=None):
    values = dict(fact.semantic_fields)
    values["empirical_query_spec_ref"] = query.ref
    if provenance is not None:
        values["source_empirical_provenance_refs"] = tuple(provenance)
    return EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=tuple(dependencies),
        producer_replay_locator_or_reference_root=(
            fact.producer_replay_locator_or_reference_root),
        **values,
    )


def _attack(mode):
    query, fact, conditioner, target = _objects()
    bad = _source(mode)
    query_deps = tuple(query.dependency_refs)
    fact_deps = tuple(fact.dependency_refs)
    if mode == "contradictory_query":
        # Fact and relation provenance continue to claim the correct source.
        query_deps = tuple(
            bad if ref.kind == "SOURCE_ARTIFACT" else ref
            for ref in query_deps
        )
    elif mode == "extra_fact_source":
        fact_deps = (*fact_deps, bad)
    elif mode == "query_only_unpropagated":
        # No direct SOURCE_ARTIFACT survives in fact provenance; the query
        # still declares the foreign artifact and would be lost at FF01.
        query_deps = tuple(
            bad if ref.kind == "SOURCE_ARTIFACT" else ref
            for ref in query_deps
        )
        fact_deps = tuple(
            ref for ref in fact_deps if ref.kind != "SOURCE_ARTIFACT"
        )
    else:
        raise ValueError(mode)

    changed_query = _rebuild_query(query, query_deps)
    replaced_fact_deps = (
        tuple(changed_query.ref if ref == query.ref else ref
              for ref in fact_deps)
        if changed_query.ref != query.ref else fact_deps
    )
    provenance = (
        tuple(ref for raw in fact.source_empirical_provenance_refs
              for ref in (exact_ref(raw, "fact provenance ref"),)
              if ref.kind != "SOURCE_ARTIFACT")
        if mode == "query_only_unpropagated" else None
    )
    changed_fact = _rebuild_fact(
        fact, changed_query, replaced_fact_deps, provenance=provenance)
    assert exact_ref(changed_fact.empirical_query_spec_ref,
                     "changed_fact.empirical_query_spec_ref") == changed_query.ref
    assert changed_fact.risk_set_ref == changed_query.risk_set_ref
    return changed_query, changed_fact, conditioner, target


def _produce(module, query, fact, conditioner, target):
    return module.produce_exact_conditional_support_profile(
        joint_fact=fact, joint_query=query,
        conditioner_ref=conditioner, target_ref=target,
        producer_permission_ceiling=(adm.GT2_TARGET_USE,),
        relation_permission_ceiling=(adm.GT2_TARGET_USE,),
    )


@pytest.fixture(scope="module")
def old_ff_module():
    frozen = subprocess.run(
        ["git", "show",
         PROTECTED + ":rawlsing_next/field_forge_conditional_support.py"],
        check=True, capture_output=True,
    ).stdout
    blob = subprocess.run(
        ["git", "hash-object", "--stdin"], input=frozen,
        check=True, capture_output=True,
    ).stdout.decode().strip()
    assert blob == OLD_FF_BLOB
    name = "rawlsing_next._c3_agent_a_frozen_old_ff01"
    module = types.ModuleType(name)
    module.__package__ = "rawlsing_next"
    sys.modules[name] = module
    try:
        exec(compile(frozen, name, "exec"), module.__dict__)
        yield module
    finally:
        sys.modules.pop(name, None)


@pytest.mark.parametrize(
    "mode", ["contradictory_query", "extra_fact_source",
             "query_only_unpropagated"],
)
def test_genuine_original_ff01_launders_upstream_source_discrepancy(
    old_ff_module, mode,
):
    query, fact, conditioner, target = _attack(mode)
    old_relation = _produce(old_ff_module, query, fact, conditioner, target)
    assert old_relation.typed_state == "SUPPORTED"
    assert semantic_hash(old_relation.semantic_projection()) == old_relation.content_hash

    # Convert OLD FF's *type* into the exact current type without changing
    # any fields: the C->D bridge is exact-type-checked, so this is the
    # identity-preserving transport needed to exercise B's actual reader.
    relation = ff.ExactConditionalSupportProfile(**{
        item.name: getattr(old_relation, item.name)
        for item in fields(ff.ExactConditionalSupportProfile)
        if item.init
    })
    assert relation.ref == old_relation.ref
    old_bounded_d = bridge.admit_gt12_c_relation(relation)
    assert old_bounded_d.admission.decision is adm.AdmissionDecision.ADMITTED

    with pytest.raises(
        ff.FieldForgeConditionalSupportError,
        match=("contradictory physical SOURCE_ARTIFACT claims"
               "|physical SOURCE_ARTIFACT in query/fact closure is missing"),
    ):
        _produce(ff, query, fact, conditioner, target)


def test_restoration_preserves_actual_bounded_first_reader_and_relation_hash():
    query, fact, conditioner, target = _objects()
    relation = _produce(ff, query, fact, conditioner, target)
    received = bridge.admit_gt12_c_relation(relation)
    assert received.admission.decision is adm.AdmissionDecision.ADMITTED
    assert received.admission.relation_ref == relation.ref


def test_real_retained_76843_ref_transport_still_works():
    from rawlsing_next.pre553_repo_native_current_payload import (
        load_current_gt2_query_fact_from_committed_transport,
    )
    query, fact = load_current_gt2_query_fact_from_committed_transport()
    relation = _produce(ff, query, fact, query.target_refs[0], query.target_refs[1])
    result = bridge.admit_gt12_c_relation_from_fixed_current_transport(relation)
    assert result.admission.decision is adm.AdmissionDecision.ADMITTED
    assert result.admission.relation_ref == relation.ref


def test_observed_zero_is_not_upgraded_to_positive():
    from rawlsing_next.tests.test_gt12_closure_b_c_to_d_bridge import _fixture
    relation, _ = _fixture(fact_state="OBSERVED_ZERO")
    result = bridge.admit_gt12_c_relation(relation)
    assert result.admission.decision is not adm.AdmissionDecision.ADMITTED
