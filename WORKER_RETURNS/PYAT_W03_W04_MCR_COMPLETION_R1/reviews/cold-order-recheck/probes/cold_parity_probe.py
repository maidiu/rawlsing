#!/usr/bin/env python3
"""Unanticipated cold/eager parity probe through the real C11/I03 selector.

Small sourcefree S2 fixtures only. No 100k benchmark, source/respondent bytes or
new engine. Writes JSON next to this probe.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from rawlsing_next._pre553_query_predicate import _build_release_index, _select_respondent_events
from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_source_backed_c11_facade import (
    build_cold_source_backed_c11_release,
    build_validated_source_backed_c11_release_from_stream,
)
from rawlsing_next.tests.test_pre553_c11_cold_reopen_i03 import _consumer_material
from rawlsing_next.tests.test_pre553_route_b_production import _fixture


def _executor(release, fixture):
    repository = C11Repository((release,))
    return CarrierNeutralResearchExecutor(repository, (release.release_ref,), fixture["catalog"])


def _run(kwargs):
    fx = _fixture(**kwargs)
    eager = build_validated_source_backed_c11_release_from_stream(fx["stream"], fx["projection"])
    cold = build_cold_source_backed_c11_release(fx["stream"], fx["projection"])
    eager_exec = _executor(eager, fx)
    cold_exec = _executor(cold, fx)
    eager_material = _consumer_material(eager_exec, fx)
    cold_material = _consumer_material(cold_exec, fx)
    sequence_rows = []
    for universe in fx["projection"].universes:
        eager_index = _build_release_index(eager, universe.ref)
        cold_index = _build_release_index(cold, universe.ref)
        for respondent_key in eager_index.events_by_respondent:
            eager_events = eager_index.events_by_respondent[respondent_key]
            cold_events = cold_index.events_by_respondent[respondent_key]
            eager_refs = [event.ref.key for event in eager_events]
            cold_refs = [event.ref.key for event in cold_events]
            if eager_refs != cold_refs:
                target = exact_ref(eager_events[0].native_question_ref)
                eager_yield = [event.ref.key for event in _select_respondent_events(
                    eager_index, respondent_key, target)]
                cold_yield = [event.ref.key for event in _select_respondent_events(
                    cold_index, respondent_key, target)]
                sequence_rows.append({
                    "universe": universe.ref.key,
                    "respondent": respondent_key,
                    "target_question": target.key,
                    "eager_refs": eager_refs,
                    "cold_refs": cold_refs,
                    "eager_selected_refs": eager_yield,
                    "cold_selected_refs": cold_yield,
                    "selector_yield_equal": eager_yield == cold_yield,
                })
    return {
        "fixture": kwargs,
        "release_equal": eager.release_ref == cold.release_ref,
        "replay_equal": eager.replay_manifest.ref == cold.replay_manifest.ref,
        "consumer_material_equal": canonical_json(eager_material) == canonical_json(cold_material),
        "public_object_material_equal": canonical_json([
            obj.as_dict() for obj in eager.public_objects
        ]) == canonical_json([obj.as_dict() for obj in cold.public_objects]),
        "event_sequence_order_equal": not sequence_rows,
        "sequence_differences": sequence_rows,
    }


def main() -> int:
    os.environ.pop("RAWLSING_C11_ACCELERATOR_POLICY", None)
    os.environ.pop("RAWLSING_C11_ACCELERATOR_DIR", None)
    results = [_run(kwargs) for kwargs in ({}, {"missing_weight": True}, {"valid_empty": True})]
    output = {
        "schema": "W03_W04_COLD_PARITY_PROBE@1",
        "sourcefree": True,
        "results": results,
        "event_sequence_parity": all(item["event_sequence_order_equal"] for item in results),
        "selector_yield_parity": all(
            all(row["selector_yield_equal"] for row in item["sequence_differences"])
            for item in results
        ),
        "selector_yield_differences": sum(
            1 for item in results for row in item["sequence_differences"]
            if not row["selector_yield_equal"]
        ),
        "consumer_material_parity": all(item["consumer_material_equal"] for item in results),
    }
    path = Path(__file__).resolve().parent / "cold_parity_probe.json"
    path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
