#!/usr/bin/env python3
"""Sourcefree proof for the shared raw response construction lane.

The frozen candidate tree is never edited.  The preserved worker handoff copy
is loaded as the isolated module used by the sourcefree construction path.
No real source bytes are opened; raw tokens are never printed.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import sys
from pathlib import Path
from collections.abc import Mapping

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# Load the preserved authored handoff implementation as the isolated module.
_worker = Path(os.environ.get(
    "ANVIL_WORKER_HANDOFF",
    HERE / "pre553_source_i02_handoff.worker.py",
)).absolute()
_name = "rawlsing_next.pre553_source_i02_handoff"
_spec = importlib.util.spec_from_file_location(_name, _worker)
if _spec is None or _spec.loader is None:
    raise SystemExit("WORKER_HANDOFF_MODULE_NOT_LOADABLE")
_module = importlib.util.module_from_spec(_spec)
sys.modules[_name] = _module
_spec.loader.exec_module(_module)

from rawlsing_next.pre553_r157_projection_adapter import SourceConfig
from rawlsing_next.pre553_source_i02_handoff import (
    build_governed_c11_projection, decode_dta, decode_sav, row_native_keys_from_transport,
)  # noqa: E402
from rawlsing_next.tests.test_pyat940_s1b_support import make_config, write_fixture  # noqa: E402
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState  # noqa: E402
from rawlsing_next.pre553_source_i02_handoff import SourceI02Refusal, _unresolved_response_state  # noqa: E402
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, canonical_json  # noqa: E402
from rawlsing_next._pre553_direct_i02_sourcefree import SourcefreeDirectI02Sections  # noqa: E402
from rawlsing_next.pre553_source_direct_parquet_estate import _FAMILIES_IN_ORDER  # noqa: E402
from streaming_estate import StreamRoots, open_stream_native_estate, write_streaming_estate  # noqa: E402
from sqlite_free_single_pass import build_single_pass  # noqa: E402


def _strip_unmapped(doc: dict, keep_raw: float) -> dict:
    out = copy.deepcopy(doc)
    slot = next(s for s in out["response_slots"] if s["slot"]["name"] == "q101")
    slot["values"] = [
        value for value in slot["values"]
        if isinstance(value.get("raw_value"), (int, float))
        and float(value["raw_value"]) == float(keep_raw)
    ]
    if not slot["values"]:
        raise AssertionError("fixture lost its mapped response rule")
    return out


def _read(root: Path, rec):
    estate = open_stream_native_estate(
        root, rec.path, rec.manifest_sha256, rec.roots,
        current_authorizer=lambda roots: roots == rec.roots,
    )
    events = list(estate.iter_family("RespondentEvent", batch_size=8))
    return estate, events


def _raw_witness_ok(event) -> bool:
    raw = event.raw_response_value
    if not isinstance(raw, Mapping) or "$raw_physical_value" not in raw:
        return False
    material = raw["$raw_physical_value"]
    return isinstance(material, Mapping) and "token" in material


def _event_key(event):
    return (
        canonical_json(event.scoped_respondent_ref),
        canonical_json(event.native_question_ref),
        str(event.multiplicity_order_rank_fields.get("index")),
    )


def _event_signature(event):
    return (event.ref.key, canonical_json(event.semantic_projection()))


def _expected_mapped_keys(path, cfg, values, keep_raw):
    """Independent expected positions from fixture input + mapped-only config."""
    fmt = cfg.document["identity"]["source_format"]
    incidence = decode_sav(path) if fmt == "SAV" else decode_dta(path)
    keys = row_native_keys_from_transport(cfg, incidence=incidence, batch_size=4)
    projection = build_governed_c11_projection(
        cfg,
        source_sha256=incidence.source_sha256,
        row_count=incidence.row_count,
        row_native_keys=keys,
    )
    row_refs = {binding.row_ordinal: binding.respondent_ref for binding in projection.row_bindings}
    qref = projection.questions[0].native_question_ref
    occurrence = cfg.document["response_slots"][0]["values"][0]["occurrences"][0]["key"]
    return {
        (canonical_json(row_refs[row]), canonical_json(qref), str(occurrence))
        for row, value in enumerate(values, 1)
        if value == keep_raw and row in row_refs
    }

class _ManifestProxy:
    def __init__(self, content_hash, release_id, counts, source_ref):
        self.content_hash = content_hash
        self.release_id = release_id
        self.declared_record_counts_by_logical_family = counts
        self.source_artifact_ref = source_ref

    def semantic_projection(self):
        return {"source_manifest_sha256": self.content_hash,
                "release_id": self.release_id}


def _ref_from_key(key):
    kind, object_id, content_hash = key.split("|", 2)
    return ExactRef(kind, object_id, content_hash)


def _build_mutated_estate(root: Path, raw_estate, raw_rec, remove_key):
    """Remove one mapped saved event and fully rebuild through the writer."""
    sections = {}
    removed = None
    for family in _FAMILIES_IN_ORDER:
        objects = list(raw_estate.iter_family(family, batch_size=8))
        if family == "RespondentEvent":
            kept = []
            for obj in objects:
                if removed is None and _event_key(obj) == remove_key:
                    removed = obj
                else:
                    kept.append(obj)
            objects = kept
        sections[family] = tuple(objects)
    if removed is None:
        raise AssertionError("mapped saved row to delete was not found")
    roots = raw_estate.i02
    counts = dict(raw_estate.manifest["family_counts"])
    counts["RespondentEvent"] -= 1
    release_id = roots.release.split("|", 2)[1]
    manifest = _ManifestProxy(
        raw_estate.manifest["manifest_sha256"], release_id, counts,
        _ref_from_key(roots.source),
    )
    source = SourcefreeDirectI02Sections(
        manifest=manifest,
        sections=sections,
        typed_absences={},
        replay_protocol_authority_ref=AuthorityRef(
            "REPLAY_PROTOCOL", "1.0.0", roots.replay),
        replay_protocol_version="1.0.0",
        deterministic_tie_order_rules_ref=ExactRef(
            "ORDER_RULE", "CANONICAL-REF-SORT", roots.logical),
    )
    mutated_root = root / "private-mutated"
    mutated_root.mkdir(mode=0o700, parents=True, exist_ok=True)
    mut_rec = write_streaming_estate(
        source, _ref_from_key(roots.universe), mutated_root, chunk_rows=2,
    )
    _, events = _read(mutated_root, mut_rec)
    return removed, mut_rec, events, sections


def _one_fixture(root: Path, *, source_format: str, values, missing_range=False,
                 extended_missing=False, keep_raw=1.0):
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    path, source_sha, rows = write_fixture(
        root / "src", source_format=source_format, values=values,
        missing_range=missing_range, extended_missing=extended_missing,
    )
    doc = make_config(
        source_format=source_format, active_source_sha256=source_sha,
        row_count=rows, keyed=True, values=values,
        user_missing_range=missing_range, extended_missing=extended_missing,
    )
    raw_cfg = SourceConfig(_strip_unmapped(doc, keep_raw))
    control_cfg = SourceConfig(_strip_unmapped(copy.deepcopy(doc), keep_raw))
    expected_keys = _expected_mapped_keys(path, raw_cfg, values, keep_raw)
    (root / "private-raw").mkdir(mode=0o700, parents=True, exist_ok=True)
    (root / "private-control").mkdir(mode=0o700, parents=True, exist_ok=True)
    raw_rec = build_single_pass(
        config=raw_cfg, source_path=path, private_root=root / "private-raw",
        chunk_rows=2, compact_spool=True,
    )
    control_rec = build_single_pass(
        config=control_cfg, source_path=path, private_root=root / "private-control",
        chunk_rows=2, compact_spool=True,
    )
    raw_estate, raw_events = _read(root / "private-raw", raw_rec)
    _, control_events = _read(root / "private-control", control_rec)
    raw_selected = {_event_signature(e) for e in raw_events if _event_key(e) in expected_keys}
    control_selected = {_event_signature(e) for e in control_events if _event_key(e) in expected_keys}
    # The deliberately deleted mapped response must be removed from a saved
    # estate, then fully rebuilt through the actual writer and cold reopened.
    remove_event = next(
        (e for e in raw_events if _event_key(e) in expected_keys), None)
    if remove_event is None:
        raise AssertionError("no mapped saved event available for deletion")
    removed, mut_rec, mutated_events, _sections = _build_mutated_estate(
        root, raw_estate, raw_rec, _event_key(remove_event))
    mutated_selected = {
        _event_signature(e) for e in mutated_events if _event_key(e) in expected_keys
    }
    missing = control_selected - mutated_selected
    saved_deletion_fails = (
        len(mutated_selected) == len(expected_keys) - 1
        and missing == {_event_signature(remove_event)}
        and mutated_selected != control_selected
    )
    _, restored_events = _read(root / "private-raw", raw_rec)
    restored_selected = {
        _event_signature(e) for e in restored_events if _event_key(e) in expected_keys
    }
    saved_restore_equal = restored_selected == control_selected and len(restored_selected) == len(expected_keys)
    states = {}
    for event in raw_events:
        states[event.typed_state] = states.get(event.typed_state, 0) + 1
    unresolved = [e for e in raw_events if e.typed_state != "SUBSTANTIVE_RESPONSE"]
    return {
        "source_format": source_format,
        "rows": rows,
        "event_count": len(raw_events),
        "state_counts": dict(sorted(states.items())),
        "mapped_expected_count": len(expected_keys),
        "mapped_raw_count": len(raw_selected),
        "mapped_control_count": len(control_selected),
        "mapped_exact": raw_selected == control_selected and len(raw_selected) == len(expected_keys),
        "saved_row_deletion_fails": saved_deletion_fails,
        "saved_row_deletion_missing_ref": _event_signature(remove_event)[0],
        "saved_row_restore_equal": saved_restore_equal,
        "unresolved_count": len(unresolved),
        "raw_witness_preserved": all(_raw_witness_ok(e) for e in unresolved),
        "cold_reopen": True,
    }


def main() -> int:
    root = Path(os.environ["ANVIL_RAW_LANE_TEST_ROOT"]).absolute()
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    a = _one_fixture(
        root / "sav-range", source_format="SAV",
        values=(1.0, 2.0, 7.0), missing_range=True, keep_raw=1.0,
    )
    b = _one_fixture(
        root / "dta-extended", source_format="DTA",
        values=(1.0, "a", 2.0, 1.0), extended_missing=True, keep_raw=1.0,
    )
    invalid_refused = False
    try:
        _unresolved_response_state(PhysicalCell(
            1, 1, "q101", 99.0, PhysicalMissingState.PHYSICAL_STATE_UNKNOWN, None))
    except SourceI02Refusal:
        invalid_refused = True
    checks = {
        "two_shapes": a["source_format"] != b["source_format"] and a["rows"] != b["rows"],
        "declared_missing_preserved": a["state_counts"].get("MISSING", 0) == 1
        and b["state_counts"].get("MISSING", 0) == 1,
        "observed_unresolved_preserved": a["state_counts"].get("INVALID_UNRESOLVED", 0) == 1
        and b["state_counts"].get("INVALID_UNRESOLVED", 0) == 1,
        "no_substantive_shift": a["state_counts"].get("SUBSTANTIVE_RESPONSE", 0) == 1
        and b["state_counts"].get("SUBSTANTIVE_RESPONSE", 0) == 2,
        "mapped_exact": a["mapped_exact"] and b["mapped_exact"],
        "saved_row_deletion_fails": a["saved_row_deletion_fails"] and b["saved_row_deletion_fails"],
        "saved_row_restore_equal": a["saved_row_restore_equal"] and b["saved_row_restore_equal"],
        "raw_witness_preserved": a["raw_witness_preserved"] and b["raw_witness_preserved"],
        "invalid_physical_input_refused": invalid_refused,
    }
    status = "SHARED_RAW_LANE_TEST_PASS_MAPPED_EXACT" if all(checks.values()) else "SHARED_RAW_LANE_TEST_FAILED"
    print(json.dumps({
        "status": status, "checks": checks,
        "sav": a, "dta": b,
        "raw_tokens_published": False,
        "source_read_performed": False,
    }, sort_keys=True))
    return 0 if all(checks.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
