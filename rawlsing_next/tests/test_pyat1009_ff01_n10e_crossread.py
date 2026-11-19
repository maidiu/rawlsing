"""Genuine existing N10E possibility consumer cross-checked against FF01 joint.

Two accepted executions intentionally remain independent. This proves exact
observed count conservation and consumer effect, NOT one-pass economic reuse
or authority to issue source rights, FF02, actor or representative inference.
"""
from copy import deepcopy

import pytest

from rawlsing_next.field_forge_generic_empirical_ingress import (
    FF01ObservedJoint, receive_ff01_observed_joint,
)
from rawlsing_next.field_forge_n10e_crossread import (
    FF01N10ECrossreadError, conserve_ff01_n10e_actual_read,
)
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalQuerySpec, canonical_json, semantic_hash,
)
from rawlsing_next.pre553_empirical_possibility_provider import provide_empirical_possibility_slice
from rawlsing_next.tests import (
    n10e_empirical_slice_fixture as fx,
    test_pre553_empirical_query as native,
)


def _actual_case(direction="forward", *, variant=None):
    case = fx.build_provider_case(direction, variant=variant)
    source = case["source"]
    qa = case["query_authority"]
    ff_predicate = native._branch_predicate(source, qa, tag="FF01-WHOLE-RISK")
    # The two role permutations share ONE actual k=2 joint query and all
    # complete cells. They differ only in the selected conditioner index.
    q0 = native._query(
        source, qa, ff_predicate, ("POSITION", "ANSWER"),
        risk="R", tag="FF01-AT07-SAME-SOURCE-JOINT",
    )
    spec = dict(q0.target_arity_and_topology)
    components = [dict(part) for part in spec["components"]]
    for component, name, domain in zip(
        components, ("POSITION", "ANSWER"), (("P1", "P2"), ("no", "yes"))
    ):
        component["domain"] = list(domain)
        component["target_domain_replay_ref"] = native._ref(
            "TARGET_DOMAIN", f"FF01-AT07-{name}-" + "-".join(domain),
        )
    ff_query = EmpiricalQuerySpec(
        typed_state=q0.typed_state,
        authority_snapshot_refs=q0.authority_snapshot_refs,
        dependency_refs=q0.dependency_refs,
        producer_replay_locator_or_reference_root=q0.producer_replay_locator_or_reference_root,
        **{
            **dict(q0.semantic_fields),
            "target_arity_and_topology": {**spec, "components": components},
        },
    )
    observed = native._run(
        source, qa, ff_predicate, ff_query,
        registry=case["registry"],
    )
    assert observed.facts[0].typed_state == "SUPPORTED"
    ff01 = receive_ff01_observed_joint(
        execution=observed, query=ff_query,
        conditioner_index=0 if direction == "forward" else 1,
        producer_permission_ceiling=("FF01_DESCRIPTIVE_SOURCEFREE",),
    )
    provider = provide_empirical_possibility_slice(
        repository=source["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        condition_binding_witness=case["condition_binding_witness"],
    )
    return ff01, provider, case


def _conserve(ff01, provider, case):
    return conserve_ff01_n10e_actual_read(
        ff01=ff01,
        provider=provider,
        n10e_empirical_query=case["empirical_query"],
        n10e_predicate=case["predicate"],
        n10e_consumer_query=case["consumer_query"],
    )


@pytest.mark.parametrize("direction,denominator,counts", [
    ("forward", 60, {"yes": 54, "no": 6}),
    ("reverse", 62, {"P1": 54, "P2": 8}),
])
def test_real_ff01_joint_agrees_with_existing_n10e_conditional_possibility(
    direction, denominator, counts
):
    ff01, provider, case = _actual_case(direction)
    conserved = _conserve(ff01, provider, case)
    material = conserved.material()
    assert material["raw_condition_denominator"] == denominator
    assert {row["target_state"]: row["raw_numerator_support"] for row in material["conserved_target_cells"]} == counts
    assert provider.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
    assert material["n10e_generated_evidence_ref"] == provider.generated_evidence_or_null.evidence_ref.as_dict()
    assert material["ff01_ref"] == ff01.ref.as_dict()
    assert material["n10e_provider_ref"] == provider.receipt_ref.as_dict()


def test_n10e_forward_and_inverse_have_distinct_conditioned_denominators():
    f, fp, fc = _actual_case("forward")
    r, rp, rc = _actual_case("reverse")
    a, b = _conserve(f, fp, fc), _conserve(r, rp, rc)
    assert a.ref != b.ref
    assert a.material()["raw_condition_denominator"] == 60
    assert b.material()["raw_condition_denominator"] == 62


def test_changed_actual_source_changes_n10e_reader_and_ff01_and_restore():
    f, p, c = _actual_case("forward")
    changed_f, changed_p, changed_c = _actual_case(
        "forward", variant=fx.CHANGED_SOURCE_VARIANT,
    )
    first, second = _conserve(f, p, c), _conserve(changed_f, changed_p, changed_c)
    assert first.ref != second.ref
    assert second.material()["raw_condition_denominator"] == 70
    assert {row["target_state"]: row["raw_numerator_support"] for row in second.material()["conserved_target_cells"]} == {"no": 16, "yes": 54}
    restored_f, restored_p, restored_c = _actual_case("forward")
    assert _conserve(restored_f, restored_p, restored_c).ref == first.ref


def test_cross_source_same_semantic_question_names_do_not_silently_pool():
    source_ff, _, _ = _actual_case("forward")
    _, provider, case = _actual_case(
        "forward", variant=fx.CHANGED_SOURCE_VARIANT,
    )
    with pytest.raises(FF01N10ECrossreadError, match="source/release"):
        _conserve(source_ff, provider, case)


def test_opposite_direction_at_same_source_refuses_even_if_marginals_match():
    ff, _, _ = _actual_case("forward")
    _, provider, case = _actual_case("reverse")
    with pytest.raises(FF01N10ECrossreadError, match="direction"):
        _conserve(ff, provider, case)


def test_hash_coherent_fake_ff01_count_cannot_influence_n10e_consumer():
    ff, provider, case = _actual_case("forward")
    m = deepcopy(ff.semantic_projection())
    positive = next(row for row in m["complete_cells"] if row["raw_support"] > 0)
    positive["raw_support"] += 1
    # Deliberately re-sign fake FF01 receipt to challenge cross-consumer
    # conservation beyond hash consistency, without changing real C1.
    digest = semantic_hash(m)
    fake = FF01ObservedJoint(
        canonical_json(m), digest,
        f"urn:rawlsing:ff01:observed-joint:sha256:{digest}",
    )
    with pytest.raises(FF01N10ECrossreadError, match="denominator|cells"):
        _conserve(fake, provider, case)
