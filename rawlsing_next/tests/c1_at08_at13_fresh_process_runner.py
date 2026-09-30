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
    _build_source,
    _query,
    _query_authority,
    _registry,
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


def main(argv):
    if len(argv) != 3:
        raise SystemExit("usage: c1_at08_at13_fresh_process_runner.py CHILD_BUNDLE OUTPUT_JSON")
    run(Path(argv[1]), Path(argv[2]))


if __name__ == "__main__":
    main(sys.argv)
