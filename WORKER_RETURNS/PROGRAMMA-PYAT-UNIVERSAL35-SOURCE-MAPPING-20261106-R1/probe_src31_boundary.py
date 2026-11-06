#!/usr/bin/env python3
"""Bounded SRC31 original-column response-binding RED/PASS probe.

Reads the caller-configured read-only original SRC31 SAV, selects only the
affected response columns plus their routing, and prints aggregate states only.
It never prints or writes respondent rows, native keys or raw source bytes.
"""
from __future__ import annotations

import collections
import copy
import json
import pathlib
import signal
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from rawlsing_next.pre553_physical_decoder import PhysicalMissingState, decode_sav
from rawlsing_next.pre553_source_backed_c11_facade import (
    physical_value_binding_key,
    project_c11_candidate_from_physical_cells,
)
from rawlsing_next.source_configuration.factory import build_governed_c11_projection
from rawlsing_next.source_configuration.library import SourceConfigLibrary
from rawlsing_next.source_configuration.provider import GitObjectProvider
from rawlsing_next.source_configuration.schema import SourceConfig


class ProbeTimeout(Exception):
    pass


def main() -> int:
    signal.signal(signal.SIGALRM, lambda _s, _f: (_ for _ in ()).throw(ProbeTimeout("timeout")))
    signal.alarm(180)
    binding = json.loads(pathlib.Path(".local-logs/pyat-universal35/source-runtime-binding.local.json").read_text())
    root = pathlib.Path(binding["USER_ORIGINAL35_DATA_ROOT"])
    library = SourceConfigLibrary.from_pinned_r157()
    corrected = library.load_original("SRC31")
    base = SourceConfig(json.loads(GitObjectProvider().read_bytes(
        "rawlsing_next/source_configuration/data/SRC31/source.config.json").decode()))
    path = root / library.locator_bindings["SRC31"]["relative_path"]
    incidence = decode_sav(path, expected_source_sha256=corrected.active_source_sha256)
    old_declared = {}
    for slot in base.document["response_slots"]:
        key = (slot["slot"]["ordinal"], slot["slot"]["name"])
        old_declared[key] = {
            physical_value_binding_key(v["raw_value"], PhysicalMissingState(v["missing_state"]),
                                       v.get("source_missing_declaration"))
            for v in slot["values"]
        }
    affected = set()
    for batch in incidence.iter_batches(100_000):
        for cell in batch:
            key = (cell.variable_ordinal, cell.variable_name)
            if key in old_declared and physical_value_binding_key(
                    cell.raw_value, cell.missing_state, cell.source_missing_declaration) not in old_declared[key]:
                affected.add(key)
    question_ids = {
        slot["question_id"] for slot in corrected.document["response_slots"]
        if (slot["slot"]["ordinal"], slot["slot"]["name"]) in affected
    }

    def selected(document):
        out = copy.deepcopy(document)
        out["response_slots"] = [
            s for s in out["response_slots"]
            if (s["slot"]["ordinal"], s["slot"]["name"]) in affected]
        out["questions"] = [q for q in out["questions"] if q["question_id"] in question_ids]
        out["routing"] = [r for r in out["routing"] if r["question_id"] in question_ids]
        out["weight_slots"] = []
        out["slot_owner_sets"] = [
            x for x in out.get("slot_owner_sets", [])
            if (x["slot"]["ordinal"], x["slot"]["name"]) in affected]
        out["supported_scope"]["supported_question_ids"] = [
            q for q in out["supported_scope"]["supported_question_ids"] if q in question_ids]
        return SourceConfig(out)

    old = selected(base.document)
    fixed = selected(corrected.document)
    red = None
    try:
        projection = build_governed_c11_projection(old)
        project_c11_candidate_from_physical_cells(
            source_sha256=old.active_source_sha256, row_count=old.active_row_count,
            cells=incidence.iter_cells(), projection=projection)
    except Exception as error:  # expected RED
        red = type(error).__name__ + ": " + str(error)[:180]
    started = time.time()
    projection = build_governed_c11_projection(fixed)
    candidate = project_c11_candidate_from_physical_cells(
        source_sha256=fixed.active_source_sha256, row_count=fixed.active_row_count,
        cells=incidence.iter_cells(), projection=projection)
    states = collections.Counter(event.response_state for event in candidate.respondent_events)
    c10 = next(s for s in fixed.document["response_slots"] if s["slot"]["name"] == "c10ai")
    c10_states = {str(v["raw_value"]): v["response_state"] for v in c10["values"]
                  if v["raw_value"] in (98.0, 99.0)}
    incidence.close()
    signal.alarm(0)
    result = {
        "schema": "PYAT_UNIVERSAL35_SRC31_BOUNDARY_PROOF@1",
        "source_id": "SRC31",
        "source_sha256": corrected.original_source_sha256,
        "corrections_applied": len(corrected.corrections_applied),
        "affected_slots": [list(key) for key in sorted(affected)],
        "old_config_refusal": red,
        "corrected_candidate_events": len(candidate.respondent_events),
        "corrected_response_states": dict(states),
        "c10ai_missing_value_states": c10_states,
        "mapping_boundary": "PASS_SELECTED_ORIGINAL_COLUMNS",
        "full_release_validation": "NOT_RUN__POSITIVE_AUTHORITY_DEFER_EXPECTED",
        "candidate_seconds": round(time.time() - started, 2),
        "respondent_rows_emitted": False,
        "raw_bytes_committed": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
