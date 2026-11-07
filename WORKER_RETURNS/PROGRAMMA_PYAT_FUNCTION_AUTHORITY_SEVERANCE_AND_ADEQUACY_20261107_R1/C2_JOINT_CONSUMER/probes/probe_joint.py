#!/usr/bin/env python3
"""Bounded sourcefree joint-composition authority/consumer probe (C2).

Exercises the actual current N10E provider + C1 analytical composition + F8
consumer over the existing synthetic 58-row lawful nonrespondent fixture.
Never reads respondent/SAV/DTA/DB bytes; never writes outside C2 output.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

import rawlsing_next.pre553_n9_n10w_progressive_candidate as pc  # noqa: E402
from rawlsing_next.pre553_analytical_composition import (  # noqa: E402
    compose_positioned_subject_possibility,
)
from rawlsing_next.pre553_empirical_objects import ExactRef  # noqa: E402
from rawlsing_next.pre553_empirical_possibility_provider import (  # noqa: E402
    provide_empirical_possibility_slice,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (  # noqa: E402
    evaluate_positioned_subject_possibility,
)
from rawlsing_next.tests.c1_at08_at13_fixture import (  # noqa: E402
    readdress_witness_with_false_pairing,
)


def ref(value):
    if value is None:
        return None
    if hasattr(value, "as_dict"):
        return value.as_dict()
    if isinstance(value, Mapping):
        return {str(k): ref(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [ref(v) for v in value]
    if isinstance(value, str):
        return value
    return str(value)


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def attempt(fn):
    try:
        value = fn()
        return {"state": "PASS", "value": value}
    except Exception as exc:  # owner typed refusals are the evidence
        return {"state": "REFUSED", "error_type": type(exc).__name__, "detail": str(exc)}


def main() -> int:
    world = pc.build_synthetic_world()
    chain = pc.run_progressive_chain(world)
    steps = []
    for step in chain.steps:
        cells = {
            key: {
                "raw_numerator_support": cell.get("raw_numerator_support"),
                "raw_denominator_support": cell.get("raw_denominator_support"),
                "raw_probability_exact_fraction": cell.get("raw_probability_exact_fraction"),
            }
            for key, cell in step.cells.items()
        }
        steps.append({
            "step_id": step.step_id,
            "conditioners": step.conditioners,
            "producer_route": step.producer_route,
            "producer_fact_state": step.producer_fact_state,
            "raw_denominator_support": step.raw_denominator_support,
            "cells": cells,
            "consumer_state": step.consumer_state,
            "release_ref": ref(step.release_ref),
            "risk_set_ref": ref(step.risk_set_ref),
            "evidence_ref": ref(getattr(step.produced_evidence, "evidence_ref", None)),
            "uncertainty_state": step.uncertainty_state,
        })

    source = world["source"]
    conds = (("A", 1), ("B", 1))
    predicate = pc._joint_predicate(world, conds)
    producer_query = pc._producer_query(world, predicate)
    consumer_query = pc._consumer_query(world, "probe", conds)
    witness = pc._witness(world, "probe", consumer_query, producer_query, predicate, conds)
    composition = compose_positioned_subject_possibility(
        repository=source["repo"], empirical_query=producer_query, predicate=predicate,
        authority_registry=world["registry"], release_refs=(source["release_ref"],),
        consumer_query=consumer_query, model_rule=world["model_rule"],
        condition_binding_witness=witness,
    )

    # Wrong conditioner order: consumer order differs from witness order.
    reversed_query = pc._consumer_query(world, "probe-reversed", tuple(reversed(conds)))
    reversed_attempt = attempt(lambda: compose_positioned_subject_possibility(
        repository=source["repo"], empirical_query=producer_query, predicate=predicate,
        authority_registry=world["registry"], release_refs=(source["release_ref"],),
        consumer_query=reversed_query, model_rule=world["model_rule"],
        condition_binding_witness=witness,
    ))

    # False pairing value: exact value substitution must refuse.
    forged = readdress_witness_with_false_pairing(witness, conditioner_index=1, false_exact_value=0)
    false_pairing_attempt = attempt(lambda: compose_positioned_subject_possibility(
        repository=source["repo"], empirical_query=producer_query, predicate=predicate,
        authority_registry=world["registry"], release_refs=(source["release_ref"],),
        consumer_query=consumer_query, model_rule=world["model_rule"],
        condition_binding_witness=forged,
    ))

    # Wrong source universe: the consumer owner itself refuses to construct a
    # cross-source query with mismatched conditioner source/release.
    def wrong_source():
        foreign = replace(
            consumer_query,
            source_universe_ref=ExactRef("EMPIRICAL_UNIVERSE", "joit-c2-foreign", "0" * 64),
        )
        return compose_positioned_subject_possibility(
            repository=source["repo"], empirical_query=producer_query, predicate=predicate,
            authority_registry=world["registry"], release_refs=(source["release_ref"],),
            consumer_query=foreign, model_rule=world["model_rule"],
            condition_binding_witness=witness,
        )
    wrong_source_attempt = attempt(wrong_source)

    # Missing needed authority: no registry / no model rule.
    missing_authority_attempt = attempt(lambda: compose_positioned_subject_possibility(
        repository=source["repo"], empirical_query=producer_query, predicate=predicate,
        authority_registry=None, release_refs=(source["release_ref"],),
        consumer_query=consumer_query, model_rule=world["model_rule"],
        condition_binding_witness=witness,
    ))

    # Same-process deterministic rebuild: not a persisted cross-process restore.
    rebuilt = pc.run_progressive_chain(pc.build_synthetic_world())
    same_process_deterministic_rebuild = {
        "same_step_ids": [s.step_id for s in chain.steps] == [s.step_id for s in rebuilt.steps],
        "same_denominators": [s.raw_denominator_support for s in chain.steps] == [s.raw_denominator_support for s in rebuilt.steps],
        "same_cells": [s.cells for s in chain.steps] == [s.cells for s in rebuilt.steps],
        "same_evidence_refs": [ref(s.produced_evidence.evidence_ref) for s in chain.steps] == [ref(s.produced_evidence.evidence_ref) for s in rebuilt.steps],
        "same_consumer_states": [s.consumer_state for s in chain.steps] == [s.consumer_state for s in rebuilt.steps],
        "cross_process_persisted_restore": "NOT_RUN__SAME_PROCESS_REBUILD_ONLY",
    }

    # Actual first-consumer invocation evidence from the real accepted owners.
    first_consumers = [entry.get("call") for entry in chain.invocation_log]
    provider_invocations = [
        entry for entry in chain.invocation_log
        if entry.get("call") == "provide_empirical_possibility_slice"
    ]
    if not provider_invocations:
        raise RuntimeError("provider invocation log is absent")
    invocation_provider_state = provider_invocations[0]["outputs"].get("provider_state")
    if not invocation_provider_state:
        raise RuntimeError("provider invocation log has no provider_state")
    composition_invocations = [
        entry for entry in chain.invocation_log
        if entry.get("call") == "compose_positioned_subject_possibility"
    ]
    if not composition_invocations:
        raise RuntimeError("composition invocation log is absent")
    invocation_composition_state = composition_invocations[0]["outputs"].get("analytical_state")
    out = {
        "probe_id": "C2_JOINT_CURRENT_COMPOSITION_S2",
        "scope": "SOURCEFREE_COMPARE_ONLY__NO_ORIGINAL_ISSUER_TRACE",
        "fixture": pc.E03_FIXTURE_ID,
        "fixture_rows": len(pc.synthetic_world_rows()),
        "fixture_real_subject": False,
        "sourcefree_positive": {
            "provider_state": invocation_provider_state,
            "provider_state_source": "actual_invocation_log:provide_empirical_possibility_slice.outputs.provider_state",
            "composition_analytical_state": invocation_composition_state,
            "composition_raw_denominator": composition.raw_denominator_support,
            "composition_consumer_state": composition.consumer_result_or_null.result_state,
            "three_step_chain": steps,
            "first_consumers": first_consumers,
        },
        "authority_surface": {
            "producer_selector": "pre553_empirical_possibility_provider.provide_empirical_possibility_slice",
            "composition_owner": "pre553_analytical_composition.compose_positioned_subject_possibility",
            "consumer_owner": "source_backed_positioned_subject_possibility.evaluate_positioned_subject_possibility",
            "empirical_query_ref": ref(producer_query.ref),
            "predicate_ref": ref(predicate.ref),
            "consumer_query_ref": ref(consumer_query.ref),
            "release_ref": ref(source["release_ref"]),
            "risk_set_ref": ref(producer_query.risk_set_ref),
            "target_refs": [ref(x) for x in producer_query.target_refs],
            "requested_output_grain": ref(producer_query.requested_output_grain),
            "measure_basis_ref": ref(producer_query.measure_basis_ref),
            "model_rule_ref": ref(world["model_rule"].model_authority_ref),
            "historical_selected_issuer": "UNKNOWN__NO_SELECTED_ORIGINAL_J_ISSUER",
            "original_selected_document": None,
        },
        "negative_controls": {
            "wrong_order": reversed_attempt,
            "false_pairing": false_pairing_attempt,
            "wrong_source_universe": wrong_source_attempt,
            "missing_needed_authority": missing_authority_attempt,
        },
        "negative_evidence_status": {
            "wrong_order": "ASSERTED_BY_NAMED_TEST",
            "false_pairing": "ASSERTED_BY_NAMED_TEST",
            "wrong_source_universe": "OBSERVED_NOT_ASSERTED",
            "missing_needed_authority": "OBSERVED_NOT_ASSERTED",
        },
        "same_process_deterministic_rebuild": same_process_deterministic_rebuild,
        "effects": dict(chain.effects),
        "source_hashes": {
            "provider": sha_file(ROOT / "rawlsing_next/pre553_empirical_possibility_provider.py"),
            "composition": sha_file(ROOT / "rawlsing_next/pre553_analytical_composition.py"),
            "consumer": sha_file(ROOT / "rawlsing_next/source_backed_positioned_subject_possibility.py"),
            "candidate_fixture": sha_file(ROOT / "rawlsing_next/pre553_n9_n10w_progressive_candidate.py"),
        },
    }
    print(json.dumps(out, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
