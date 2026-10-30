#!/usr/bin/env python3
"""H06 bounded receipt harness for the existing C1-02 AT11 recursive product.

Reuses the existing owner-produced source-free fixture and the existing I05
discovery, recursive-handoff, analytical-composition and positioned-subject
consumer owners. It adds no production engine and no semantic authority.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import rawlsing_next.tests.test_pre553_analytical_composition_higher_order as t
from rawlsing_next.pre553_recursive_handoff import (
    write_recursive_handoff_bundle,
)


def _ref(obj):
    return None if obj is None else obj.as_dict()


def _refs(values):
    return [value.as_dict() for value in values]


def build_case():
    source = t._at11_source()
    qauth = t._query_authority("c1-at11-fresh-runner")
    dauth = t._d_auth("c1-at11-fresh-runner-discovery")
    pairing = t.fx.make_pairing_authority("at11-h06-receipt")
    registry = t._registry(source, qauth, dauth)

    parent = t._branch_predicate(
        source,
        qauth,
        members=tuple(
            source["respondents"][rid] for rid in ("R1", "R2", "R3", "R4", "R5", "R6")
        ),
        tag="c1-at11-fresh-runner-parent",
    )
    x1 = t._predicate(
        source, qauth, t._response_leaf(source, qauth, "X", 1), tag="c1-at11-fresh-runner-x1"
    )
    x_query = t._query(
        source, qauth, parent, ("X",), tag="c1-at11-fresh-runner-g1-x"
    )
    grammar = t._grammar(
        operation="I03-OP-c1-at11-fresh-runner-discovery",
        atoms=[t._atom("PARENT", parent, "BRANCH"), t._atom("X1", x1, "RESPONSE")],
        templates=[t._qt("X", x_query)],
        rules=[
            t._rule(
                "child",
                "RECURSIVE_SUBGROUP_FORK",
                "SINGLE_ATOM",
                atom_ids=("X1",),
                baseline_atom_id="PARENT",
                query_template_id="X",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            )
        ],
        k=2,
    )
    authority = t._discovery_authority(
        source, grammar, dauth, tag="c1-at11-fresh-runner-g1"
    )
    g1 = t.execute_exact_bounded_discovery_with_handoffs(
        repository=source["repo"],
        discovery_authority=authority,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        predicate_catalog=(parent, x1),
        query_template_catalog=(x_query,),
    )
    handoff = g1.handoffs[0]
    child_predicate = handoff.winning_predicate
    child_query = t._query(
        source, qauth, child_predicate, ("Y",), tag="c1-at11-h06-receipt-child-to-y"
    )
    subject_ref = t.ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "urn:test:c1-02:at11-h06:subject",
        t.semantic_hash({"fixture_id": "AT11-H06"}),
    )
    binding = t.fx.make_conditioner_binding(
        binding_id="x",
        subject_fact_ref=t.ExactRef(**t._subject_fact_ref(source, "X", 1)),
        empirical_coordinate_ref=source["qrefs"]["X"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = t.fx.make_multi_conditioner_consumer_query(
        query_id="c1-at11-h06-consumer",
        subject_ref=subject_ref,
        target_ref=source["qrefs"]["Y"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind="C1_AT11_RECURSIVE_HANDOFF_CONDITIONAL_DISTRIBUTION",
    )
    witness = t.fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at11-h06:witness",
        consumer_query=consumer_query,
        producer_query=child_query,
        producer_predicate=child_predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["X"], 1)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    result = t.compose_positioned_subject_possibility(
        repository=source["repo"],
        empirical_query=child_query,
        predicate=child_predicate,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query,
        model_rule=t.fx.make_model_rule(source["universe"].ref, "at11-h06"),
        condition_binding_witness=witness,
        recursive_handoff=handoff,
    )
    assert result.producer_route == "MX01R2_RECURSIVE_TO_POSITIONED_SUBJECT"
    assert result.analytical_state == "SUPPORTED"
    assert result.consumer_result_or_null is not None
    assert result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
    assert result.recursive_handoff_refs == (handoff.ref,)
    assert handoff.immediate_parent_branch_ref in result.recursive_lineage_refs
    assert result.coverage_state == "RECURSIVE_DEPTH_CONTINUATION"
    return source, g1, handoff, result, child_query, child_predicate


def replay_case(g1):
    outputs = []
    with tempfile.TemporaryDirectory(prefix="h06-replay-") as td:
        tmp = Path(td)
        bundle_path = tmp / "child.bundle.json"
        write_recursive_handoff_bundle(bundle_path, g1.handoffs)
        repo_root = Path(__file__).resolve().parents[3]
        for index in (1, 2):
            out = tmp / f"fresh-{index}.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "rawlsing_next.tests.c1_at08_at13_fresh_process_runner",
                    str(bundle_path),
                    str(out),
                ],
                cwd=repo_root,
                check=True,
                text=True,
                capture_output=True,
            )
            assert completed.returncode == 0
            outputs.append(json.loads(out.read_text(encoding="utf-8")))
    assert outputs[0] == outputs[1]
    return outputs


def build_minority_case():
    source = t.fx.minority_fixture()
    qauth = t._query_authority("c1-at10-minority")
    dauth = t._d_auth("at10-minority-discovery")
    registry = t._registry(source, qauth, dauth)
    all_p = t._branch_predicate(source, qauth, tag="at10-all")
    groups = {
        group: t._predicate(
            source, qauth, t._coordinate_leaf(source, "G", group), tag=f"at10-atom-{group}"
        )
        for group in ("A", "B", "C")
    }
    yq = t._query(source, qauth, all_p, ("Y",), tag="at10-y")
    grammar = t._grammar(
        operation="I03-OP-at10-minority-discovery",
        atoms=[t._atom("ALL", all_p, "BRANCH")]
        + [t._atom(group, predicate, "COORDINATE") for group, predicate in groups.items()],
        templates=[t._qt("Y", yq)],
        rules=[
            t._rule(
                f"minority-{group}",
                "MINORITY_OR_NONMODAL_DEPARTURE",
                "SINGLE_ATOM",
                atom_ids=(group,),
                baseline_atom_id="ALL",
                query_template_id="Y",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            )
            for group in ("A", "B", "C")
        ],
        k=2,
    )
    discovery = t._execute_discovery(
        source,
        qauth,
        dauth,
        grammar,
        (all_p, *groups.values()),
        (yq,),
        authority=t._discovery_authority(source, grammar, dauth, tag="at10-minority"),
    )
    supported = [r for r in discovery.receipts if r.typed_state == "DISCOVERED_RESULT_SUPPORTED"]
    assert len(supported) == 3
    pred_by_ref = {p.ref: p for p in discovery.executed_predicates}
    query_by_ref = {q.ref: q for q in discovery.executed_queries}
    fact_by_ref = {f.ref: f for f in discovery.empirical_facts}
    branches = []
    for receipt in supported:
        predicate = pred_by_ref[t.ExactRef(**receipt.winning_predicate_ref)]
        fact = next(
            fact_by_ref[t.ExactRef(**ref)]
            for ref in receipt.empirical_fact_refs
            if t.ExactRef(**ref) in fact_by_ref
            and t.ExactRef(**fact_by_ref[t.ExactRef(**ref)].condition_predicate_ref) == predicate.ref
        )
        query = query_by_ref[t.ExactRef(**fact.empirical_query_spec_ref)]
        pairing = t.fx.make_pairing_authority("at10-minority")
        atom_values = t._atom_values(predicate.predicate_ast, source["crefs"]["G"].as_dict())
        assert len(atom_values) == 1
        atom_group = atom_values[0]
        binding = t.fx.make_conditioner_binding(
            binding_id="g",
            subject_fact_ref=t.ExactRef(**t.fx.subject_fact_ref(source, "G", atom_group)),
            empirical_coordinate_ref=source["crefs"]["G"],
            comparability_authority_ref=pairing,
            source_universe_ref=source["universe"].ref,
            release_ref=source["release_ref"],
        )
        consumer_query = t.fx.make_multi_conditioner_consumer_query(
            query_id=f"at10-consumer-{atom_group}",
            subject_ref=t.ExactRef(
                "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
                f"urn:test:c1-02:at10-subject-{atom_group}",
                t.semantic_hash({"fixture_id": f"AT10-{atom_group}"}),
            ),
            target_ref=source["qrefs"]["Y"],
            source_universe_ref=source["universe"].ref,
            release_ref=source["release_ref"],
            bindings=[binding],
            projection_kind="C1_AT10_MINORITY_BRANCH",
        )
        witness = t.fx.build_witness_for_binding(
            witness_object_id=f"urn:test:c1-02:at10-witness-{atom_group}",
            consumer_query=consumer_query,
            producer_query=query,
            producer_predicate=predicate,
            bindings=[binding],
            coordinate_value_pairs=[(source["crefs"]["G"], atom_group)],
            pairing_authority=pairing,
            source_universe_ref=source["universe"].ref,
            release_ref=source["release_ref"],
            leaf_type="EMPIRICAL_POSITION_COORDINATE",
        )
        result = t.compose_positioned_subject_possibility(
            repository=source["repo"],
            empirical_query=query,
            predicate=predicate,
            authority_registry=registry,
            release_refs=(source["release_ref"],),
            consumer_query=consumer_query,
            model_rule=t.fx.make_model_rule(source["universe"].ref, "at10-minority"),
            condition_binding_witness=witness,
            discovery_result=discovery,
            discovery_receipt_ref=receipt.ref,
        )
        assert result.producer_route == "I05_EXACT_BOUNDED_TO_POSITIONED_SUBJECT"
        assert result.analytical_state == "SUPPORTED"
        assert result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
        branches.append(
            {
                "group": atom_group,
                "denominator": fact.raw_denominator_support,
                "composed_result_identity_hash": result.composed_result_identity_hash,
                "producer_query_ref": query.ref.as_dict(),
                "producer_predicate_ref": predicate.ref.as_dict(),
                "producer_fact_ref": fact.ref.as_dict(),
                "consumer_query_ref": consumer_query.ref.as_dict(),
                "witness_ref": witness.witness_ref.as_dict(),
                "model_rule_hash": result.consumer_model_rule_hash,
                "consumer_result_state": result.consumer_result_or_null.result_state,
                "consumer_result_hash": result.consumer_result_or_null.result_hash,
                "complete_cell_geometry": result.complete_cell_geometry,
                "denominator_member_ref_count": len(result.denominator_member_refs),
                "discovery_receipt_ref": receipt.ref.as_dict(),
            }
        )
    identities = {b["composed_result_identity_hash"] for b in branches}
    assert len(identities) == 3
    return {
        "product_grade": "SOURCEFREE_SYNTHETIC_FIXTURE_CAPABILITY__AT10_MODAL_MINORITY_COUNTERPATTERN",
        "producer_function": "rawlsing_next.pre553_discovery_exact.execute_exact_bounded_discovery",
        "composition_function": "rawlsing_next.pre553_analytical_composition.compose_positioned_subject_possibility",
        "consumer_function": "rawlsing_next.source_backed_positioned_subject_possibility.evaluate_positioned_subject_possibility",
        "producer_route": "I05_EXACT_BOUNDED_TO_POSITIONED_SUBJECT",
        "branch_count": len(branches),
        "denominators": sorted(b["denominator"] for b in branches),
        "distinct_composed_identities": len(identities),
        "branches": branches,
        "oracle": t.fx.MINORITY_ORACLE,
    }


def main():
    source, g1, handoff, result, child_query, child_predicate = build_case()
    replay = replay_case(g1)
    minority = build_minority_case()
    consumer = result.consumer_result_or_null
    receipt = {
        "schema": "PYAT_H06_EXECUTED_PRODUCT_RECEIPT@1",
        "product_grade": "SOURCEFREE_SYNTHETIC_FIXTURE_CAPABILITY__NOT_ORIGINAL_SURVEY_OCCUPANCY",
        "producer": {
            "function": "rawlsing_next.pre553_recursive_handoff.execute_exact_bounded_discovery_with_handoffs",
            "discovery_owner": "rawlsing_next.pre553_discovery_exact",
            "source_fixture": "rawlsing_next.tests.test_pre553_analytical_composition_higher_order._at11_source",
            "source_tag": "c1-at11",
            "handoff_ref": handoff.ref.as_dict(),
            "parent_branch_ref": handoff.immediate_parent_branch_ref.as_dict(),
            "discovery_receipt_state": g1.discovery_result.receipts[0].typed_state,
            "producer_query_ref": child_query.ref.as_dict(),
            "producer_predicate_ref": child_predicate.ref.as_dict(),
        },
        "composition": {
            "function": "rawlsing_next.pre553_analytical_composition.compose_positioned_subject_possibility",
            "route": result.producer_route,
            "analytical_state": result.analytical_state,
            "coverage_state": result.coverage_state,
            "consumer_query_ref": result.consumer_query_ref.as_dict(),
            "witness_ref": result.condition_binding_witness_ref_or_hash.as_dict(),
            "model_rule_hash": result.consumer_model_rule_hash,
            "composed_result_identity_hash": result.composed_result_identity_hash,
            "recursive_handoff_refs": _refs(result.recursive_handoff_refs),
            "recursive_lineage_refs": _refs(result.recursive_lineage_refs),
        },
        "supporting_products": {"at10_modal_minority_counterpattern": minority},
        "consumer": {
            "function": "rawlsing_next.source_backed_positioned_subject_possibility.evaluate_positioned_subject_possibility",
            "result_state": consumer.result_state,
            "result_hash": consumer.result_hash,
            "exact_disposition": consumer.exact_disposition,
            "exact_reason": consumer.exact_reason,
            "exact_geometry": consumer.exact_geometry,
            "model_rule_hash": consumer.model_rule_hash,
            "source_universe_ref": consumer.source_universe_ref.as_dict(),
            "release_ref": consumer.release_ref.as_dict(),
            "target_ref": consumer.target_ref.as_dict(),
            "replay_determinants": _refs(consumer.replay_determinants),
        },
        "retained_product": {
            "source_universe_refs": result.source_universe_refs[0].as_dict(),
            "release_refs": result.release_refs[0].as_dict(),
            "raw_denominator_support": result.raw_denominator_support,
            "measure_kind": result.measure_kind,
            "denominator_member_ref_count": len(result.denominator_member_refs),
            "risk_set_member_ref_count": len(result.risk_set_member_refs),
            "complete_cell_geometry": result.complete_cell_geometry,
            "target_arity_and_topology": result.target_arity_and_topology,
            "uncertainty_state": result.uncertainty_state,
            "authority_refs": _refs(result.authority_refs),
            "provenance_refs": _refs(result.provenance_refs),
            "dependency_refs_count": len(result.dependency_refs),
            "replay_refs": _refs(result.replay_refs),
        },
        "replay": {
            "fresh_process_equal": True,
            "run_count": len(replay),
            "outputs": replay,
        },
        "first_consumer": "The existing positioned-subject possibility consumer receives an exact recursive conditional distribution and returns EXACT_SUPPORTED; no semantic-relation authority is added.",
        "limitations": [
            "Synthetic source-free fixture; not original survey execution or 35-wave occupancy.",
            "No new CAN/ADP/SCI05/Pyat semantic or actor authority.",
            "No PRE-MAIN merge or adoption.",
        ],
    }
    out = Path(__file__).resolve().parents[1] / "02_EXECUTED_PRODUCT_RECEIPT.json"
    out.write_text(json.dumps(receipt, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps({
        "receipt": str(out),
        "producer_route": result.producer_route,
        "artifacts": result.analytical_state,
        "consumer_state": consumer.result_state,
        "denominator": result.raw_denominator_support,
        "cells": len(result.complete_cell_geometry),
        "replay_equal": True,
    }, indent=2))


if __name__ == "__main__":
    main()
