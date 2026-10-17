#!/usr/bin/env python3
"""Fresh-process half of the C1-03R AT18 analytical replay-grade proof.

This runner is a *fresh Python process*. It reads a retained-determinant **input**
artifact that contains only the exact refs needed to reconstruct and re-execute the
accepted producer/composition path. It contains no expected output, no result/evidence
ref, no denominator support and no geometry.

The runner does not read any stored answer: it recomputes the identity here and prints
it. The parent court holds the oracle and performs the comparison. A stored-output
deserialization could not satisfy this runner.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

from rawlsing_next.pre553_analytical_composition import (
    compose_positioned_subject_possibility,
)
from rawlsing_next.pre553_empirical_objects import authority_ref, exact_ref
from rawlsing_next.pre553_analytical_replay_dependency import (
    assert_runner_input_carries_no_answer,
)
from rawlsing_next.tests import c1_at18_at19_fixture as fx


def rebuild_case(determinants: dict) -> dict:
    """Rebuild the accepted analytical case and verify it matches the retained refs."""

    direction = determinants["direction"]
    case = fx.build_case(direction)

    checks = {
        "empirical_query_ref": case["empirical_query"].ref,
        "predicate_ref": case["predicate"].ref,
        "condition_binding_witness_ref": case["condition_binding_witness"].witness_ref,
        "consumer_query_ref": case["consumer_query"].ref,
        "source_universe_ref": case["source"]["universe"].ref,
    }
    for key, rebuilt in checks.items():
        retained = exact_ref(determinants[key], key)
        if rebuilt != retained:
            raise AssertionError(
                f"retained determinant {key} did not rebuild exactly: "
                f"{rebuilt.key} != {retained.key}"
            )
    if case["predicate"].predicate_hash != determinants["predicate_hash"]:
        raise AssertionError("retained predicate_hash did not rebuild exactly")
    if case["model_rule"].rule_hash != determinants["model_rule_hash"]:
        raise AssertionError("retained model_rule_hash did not rebuild exactly")

    retained_releases = tuple(
        exact_ref(x, "release_ref") for x in determinants["release_refs"]
    )
    if tuple(case["release_refs"]) != retained_releases:
        raise AssertionError("retained release refs did not rebuild exactly")

    retained_authorities = tuple(
        authority_ref(x, "authority_ref") for x in determinants["authority_snapshot_refs"]
    )
    rebuilt_authorities = tuple(case["empirical_query"].authority_snapshot_refs)
    if sorted(rebuilt_authorities, key=lambda r: r.key) != sorted(
        retained_authorities, key=lambda r: r.key
    ):
        raise AssertionError("retained authority snapshot refs did not rebuild exactly")
    return case


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: runner <retained_determinants.json>", file=sys.stderr)
        return 2
    determinants = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    # Fail closed if the input artifact ever carries an expected answer.
    assert_runner_input_carries_no_answer(determinants)

    # Fresh empirical recomputation: rebuild determinants from the synthetic law and
    # re-execute the accepted composition owner in this process.
    case = rebuild_case(determinants)
    composition = compose_positioned_subject_possibility(
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        condition_binding_witness=case["condition_binding_witness"],
    )

    payload = {
        "producer_route": composition.producer_route,
        "analytical_state": composition.analytical_state,
        "composed_result_identity_hash": composition.composed_result_identity_hash,
        "producer_query_ref": composition.producer_query_ref.as_dict(),
        "producer_predicate_ref": composition.producer_predicate_ref.as_dict(),
        "producer_fact_ref": composition.producer_fact_ref.as_dict(),
        "consumer_query_ref": composition.consumer_query_ref.as_dict(),
        "raw_denominator_support": composition.raw_denominator_support,
        "cell_numerators": {
            cell["cell"]: cell["raw_numerator_support"]
            for cell in composition.complete_cell_geometry
        },
        "evidence_ref_or_null": (
            None
            if composition.possibility_slice_evidence_or_null is None
            else composition.possibility_slice_evidence_or_null.evidence_ref.as_dict()
        ),
        "consumer_result_hash_or_null": (
            None
            if composition.consumer_result_or_null is None
            else composition.consumer_result_or_null.result_hash
        ),
        "consumer_result_state_or_null": (
            None
            if composition.consumer_result_or_null is None
            else composition.consumer_result_or_null.result_state
        ),
    }
    sys.stdout.write(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
