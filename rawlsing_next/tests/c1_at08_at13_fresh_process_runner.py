#!/usr/bin/env python3
"""Fresh-process half of the C1-02 AT11 recursive-handoff composition proof.

The parent process writes a recursive handoff bundle. This runner reloads it in a
fresh Python process, replays branch membership, and composes a positioned-subject
possibility slice. The output identity-bearing observables must be reproducible.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_recursive_handoff import (
    load_recursive_handoff_bundle,
    replay_recursive_branch_membership,
)
from rawlsing_next.pre553_analytical_composition import compose_positioned_subject_possibility
from rawlsing_next.source_backed_positioned_subject_possibility import (
    PositionedSubjectPossibilityQuery,
    ConditionerBinding,
)
from rawlsing_next.tests import c1_at08_at13_fixture as fx
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate,
    _build_source,
    _predicate,
    _query,
    _query_authority,
    _registry,
    _response_leaf,
)


def _subject_fact_ref(source, question, value):
    material = {
        "schema": "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "empirical_semantic_ref": source["qrefs"][question].as_dict(),
        "exact_value": str(value),
    }
    ref = ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        f"urn:test:c1-02:subject-fact:{question}:{value}",
        semantic_hash(material),
    )
    return ref


def _fixture():
    rows = [
        {"id": "R1", "responses": {"X": 1, "H": 1, "Y": 1}},
        {"id": "R2", "responses": {"X": 1, "H": 1, "Y": 0}},
        {"id": "R3", "responses": {"X": 1, "H": 0, "Y": 1}},
        {"id": "R4", "responses": {"X": 1, "H": 0, "Y": 0}},
        {"id": "R5", "responses": {"X": 0, "H": 1, "Y": 1}},
        {"id": "R6", "responses": {"X": 0, "H": 0, "Y": 0}},
    ]
    return _build_source("c1-at11", rows)


# The depth-two fixture must be byte-identical in material to the one the parent
# court persists the bundle from, so the same source tag and rows are required.
_DEPTH2_ROWS = [
    {"id": "R1", "responses": {"X": 1, "H": 1, "Y": 1}},
    {"id": "R2", "responses": {"X": 1, "H": 1, "Y": 0}},
    {"id": "R3", "responses": {"X": 1, "H": 0, "Y": 1}},
    {"id": "R4", "responses": {"X": 1, "H": 0, "Y": 0}},
    {"id": "R5", "responses": {"X": 0, "H": 1, "Y": 1}},
    {"id": "R6", "responses": {"X": 0, "H": 0, "Y": 0}},
]


def run(child_bundle_path: Path, output_path: Path) -> dict:
    source = _fixture()
    qauth = _query_authority("c1-at11-fresh-runner")
    pairing = fx.make_pairing_authority("at11-fresh")

    bundle_ref, handoffs = load_recursive_handoff_bundle(child_bundle_path)
    if len(handoffs) != 1:
        raise AssertionError("fresh runner requires exactly one child handoff")
    handoff = handoffs[0]

    registry = _registry(source, qauth)
    child_members = replay_recursive_branch_membership(
        repository=source["repo"],
        handoff=handoff,
        authority_registry=registry,
    )

    # Compose the reloaded handoff into a C1 possibility slice.
    child_predicate = handoff.winning_predicate
    child_query = _query(
        source,
        qauth,
        child_predicate,
        ("Y",),
        tag="c1-at11-fresh-child-to-y",
    )

    subject_ref = ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "urn:test:c1-02:at11-fresh:subject",
        semantic_hash({"fixture_id": "AT11-FRESH"}),
    )
    binding = fx.make_conditioner_binding(
        binding_id="x",
        subject_fact_ref=_subject_fact_ref(source, "X", 1),
        empirical_coordinate_ref=source["qrefs"]["X"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="c1-at11-fresh-consumer",
        subject_ref=subject_ref,
        target_ref=source["qrefs"]["Y"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind="C1_AT11_FRESH_PROCESS_RECURSIVE_COMPOSITION",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at11-fresh:witness",
        consumer_query=consumer_query,
        producer_query=child_query,
        producer_predicate=child_predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["X"], 1)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )

    result = compose_positioned_subject_possibility(
        repository=source["repo"],
        empirical_query=child_query,
        predicate=child_predicate,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query,
        model_rule=fx.make_model_rule(source["universe"].ref, "at11-fresh"),
        condition_binding_witness=witness,
        recursive_handoff=handoff,
    )

    payload = {
        "bundle_ref": bundle_ref.as_dict(),
        "handoff_ref": handoff.ref.as_dict(),
        "winning_predicate_ref": child_predicate.ref.as_dict(),
        "immediate_parent_ref": handoff.immediate_parent_branch_ref.as_dict(),
        "child_member_refs": [ref.as_dict() for ref in child_members],
        "producer_route": result.producer_route,
        "analytical_state": result.analytical_state,
        "coverage_state": result.coverage_state,
        "recursive_handoff_refs": [ref.as_dict() for ref in result.recursive_handoff_refs],
        "recursive_lineage_refs": [ref.as_dict() for ref in result.recursive_lineage_refs],
        "consumer_result_state": result.consumer_result_or_null.result_state,
        "evidence_ref": result.possibility_slice_evidence_or_null.evidence_ref.as_dict(),
        "composed_result_identity_hash": result.composed_result_identity_hash,
    }
    output_path.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    return payload


def gen1_material(tag: str = "c1-at11-fresh-d2"):
    """Exact generation-one material for the fresh depth-two proof.

    The parent court persists a bundle from exactly this material, and the fresh
    process replays it. Both sides call this function so the recursive identity
    cannot drift between writer and replayer.
    """
    from rawlsing_next.pre553_recursive_handoff import execute_exact_bounded_discovery_with_handoffs
    from rawlsing_next.tests.test_pre553_discovery_exact import (
        _atom,
        _d_auth,
        _discovery_authority,
        _grammar,
        _qt,
        _rule,
    )

    source = _build_source(tag, list(_DEPTH2_ROWS))
    qauth = _query_authority("c1-at11-fresh-depth2")
    dauth1 = _d_auth("c1-at11-fresh-gen1")
    dauth2 = _d_auth("c1-at11-fresh-gen2")
    registry = _registry(source, qauth, dauth1, dauth2)

    parent = _branch_predicate(source, qauth, tag="at11-fresh-gen1-parent")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="at11-fresh-gen1-x1")
    gen1_query = _query(source, qauth, parent, ("X",), tag="at11-fresh-gen1-xq")
    gen1_grammar = _grammar(
        operation="I03-OP-c1-at11-fresh-gen1",
        atoms=[_atom("PARENT", parent, "BRANCH"), _atom("X1", x1, "RESPONSE")],
        templates=[_qt("X", gen1_query)],
        rules=[_rule(
            "child", "RECURSIVE_SUBGROUP_FORK", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="PARENT", query_template_id="X",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )
    gen1 = execute_exact_bounded_discovery_with_handoffs(
        repository=source["repo"],
        discovery_authority=_discovery_authority(source, gen1_grammar, dauth1, tag="c1-at11-fresh-gen1"),
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        predicate_catalog=(parent, x1),
        query_template_catalog=(gen1_query,),
    )
    return {
        "source": source,
        "qauth": qauth,
        "registry": registry,
        "gen1": gen1,
    }


def run_depth_two(child_bundle_path: Path, output_path: Path) -> dict:
    """Fresh-process generation two.

    Reloads the persisted generation-one handoff in this process, re-enters the
    recursive owner through the exact public recursive parent atom, produces a
    depth-two handoff, and consumes it through the C1 analytical/consumer path.
    """
    from rawlsing_next.pre553_recursive_handoff import (
        execute_exact_bounded_discovery_with_handoffs,
        recursive_parent_atom,
    )
    from rawlsing_next.tests.test_pre553_discovery_exact import (
        _atom,
        _d_auth,
        _discovery_authority,
        _grammar,
        _qt,
        _rule,
    )

    material = gen1_material()
    source = material["source"]
    qauth = material["qauth"]
    registry = material["registry"]
    gen1 = material["gen1"]
    dauth2 = _d_auth("c1-at11-fresh-gen2")

    bundle_ref, handoffs = load_recursive_handoff_bundle(child_bundle_path)
    if len(handoffs) != 1:
        raise AssertionError("fresh depth-two runner requires exactly one child handoff")
    handoff1 = handoffs[0]
    if len(gen1.handoffs) != 1 or gen1.handoffs[0].ref != handoff1.ref:
        raise AssertionError("replayed generation one does not match the persisted handoff")

    gen1_members = replay_recursive_branch_membership(
        repository=source["repo"], handoff=handoff1, authority_registry=registry,
    )

    # Generation two: the persisted branch becomes the exact recursive parent atom.
    h1_leaf = _predicate(source, qauth, _response_leaf(source, qauth, "H", 1), tag="at11-fresh-gen2-h1")
    child_atom = recursive_parent_atom(handoff1, "CHILD")
    gen2_query = _query(source, qauth, handoff1.winning_predicate, ("H",), tag="at11-fresh-gen2-hq")
    gen2_grammar = _grammar(
        operation="I03-OP-c1-at11-fresh-gen2",
        atoms=[child_atom, _atom("H1", h1_leaf, "RESPONSE")],
        templates=[_qt("H", gen2_query)],
        rules=[_rule(
            "grandchild", "RECURSIVE_SUBGROUP_FORK", "SINGLE_ATOM",
            atom_ids=("H1",), baseline_atom_id="CHILD", query_template_id="H",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )
    gen2 = execute_exact_bounded_discovery_with_handoffs(
        repository=source["repo"],
        discovery_authority=_discovery_authority(source, gen2_grammar, dauth2, tag="c1-at11-fresh-gen2"),
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        predicate_catalog=(handoff1.winning_predicate, h1_leaf),
        query_template_catalog=(gen2_query,),
    )
    if len(gen2.handoffs) != 1:
        raise AssertionError("depth-two discovery produced no unique handoff")
    handoff2 = gen2.handoffs[0]
    gen2_members = replay_recursive_branch_membership(
        repository=source["repo"], handoff=handoff2, authority_registry=registry,
    )

    # Consume the depth-two result through the C1 analytical/consumer path.
    pairing = fx.make_pairing_authority("at11-fresh-depth2")
    depth2_query = _query(source, qauth, handoff2.winning_predicate, ("Y",), tag="at11-fresh-gen2-out")
    binding = fx.make_conditioner_binding(
        binding_id="h",
        subject_fact_ref=_subject_fact_ref(source, "H", 1),
        empirical_coordinate_ref=source["qrefs"]["H"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="at11-fresh-depth2-consumer",
        subject_ref=ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
            "urn:test:c1-02:at11-fresh-depth2:subject",
            semantic_hash({"fixture_id": "AT11-FRESH-DEPTH2"}),
        ),
        target_ref=source["qrefs"]["Y"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind="C1_AT11_FRESH_DEPTH_TWO",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at11-fresh-depth2:witness",
        consumer_query=consumer_query,
        producer_query=depth2_query,
        producer_predicate=handoff2.winning_predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["H"], 1)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    result = compose_positioned_subject_possibility(
        repository=source["repo"],
        empirical_query=depth2_query,
        predicate=handoff2.winning_predicate,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query,
        model_rule=fx.make_model_rule(source["universe"].ref, "at11-fresh-depth2"),
        condition_binding_witness=witness,
        recursive_handoff=handoff2,
    )

    payload = {
        "mode": "DEPTH_TWO",
        "bundle_ref": bundle_ref.as_dict(),
        "gen1_handoff_ref": handoff1.ref.as_dict(),
        "gen2_handoff_ref": handoff2.ref.as_dict(),
        "gen1_child_member_refs": [ref.as_dict() for ref in gen1_members],
        "gen2_child_member_refs": [ref.as_dict() for ref in gen2_members],
        "gen2_immediate_parent_ref": handoff2.immediate_parent_branch_ref.as_dict(),
        "gen1_ref_present_in_gen2_ancestry": (
            handoff1.ref.as_dict()
            in handoff2.candidate_universe_definition["atoms"][0]["ancestry_refs"]
        ),
        "producer_route": result.producer_route,
        "analytical_state": result.analytical_state,
        "raw_denominator_support": result.raw_denominator_support,
        "recursive_lineage_refs": [ref.as_dict() for ref in result.recursive_lineage_refs],
        "consumer_result_state": result.consumer_result_or_null.result_state,
        "evidence_ref": result.possibility_slice_evidence_or_null.evidence_ref.as_dict(),
        "composed_result_identity_hash": result.composed_result_identity_hash,
    }
    output_path.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    return payload


def main(argv):
    if len(argv) == 3:
        run(Path(argv[1]), Path(argv[2]))
        return
    if len(argv) == 4 and argv[1] == "--depth-two":
        run_depth_two(Path(argv[2]), Path(argv[3]))
        return
    raise SystemExit(
        "usage: c1_at08_at13_fresh_process_runner.py CHILD_BUNDLE OUTPUT_JSON "
        "[--depth-two CHILD_BUNDLE OUTPUT_JSON]"
    )


if __name__ == "__main__":
    main(sys.argv)
