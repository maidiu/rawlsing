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

from rawlsing_next.pre553_r157_projection_adapter import SourceConfig  # noqa: E402
from rawlsing_next.tests.test_pyat940_s1b_support import make_config, write_fixture  # noqa: E402
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState  # noqa: E402
from rawlsing_next.pre553_source_i02_handoff import SourceI02Refusal, _unresolved_response_state  # noqa: E402
from rawlsing_next.pre553_empirical_objects import canonical_json  # noqa: E402
from rawlsing_next.pre553_c11_integrity import TypedAbsence  # noqa: E402
from rawlsing_next._pre553_query_common import _ReleaseIndex  # noqa: E402
from rawlsing_next._pre553_query_predicate import _eval_predicate  # noqa: E402
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry  # noqa: E402
from sqlite_free_single_pass import build_single_pass  # noqa: E402
from streaming_estate import open_stream_native_estate  # noqa: E402


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


def _mapped_signature(event):
    return (
        canonical_json(event.scoped_respondent_ref),
        canonical_json(event.native_question_ref),
        event.response_state,
        canonical_json(event.raw_response_value),
        canonical_json(event.response_topology_ref),
        canonical_json(event.multiplicity_order_rank_fields),
        canonical_json(event.canonical_response_value_if_authorized),
    )


def _i03_not_witness(estate, events):
    """Use the saved I03 predicate evaluator on a saved condition + NOT.

    This is a RED witness, not a new semantic rule.  A NOT over the saved
    substantive-state condition must not silently take an unresolved event as
    a positive condition member.
    """
    identities = {r.ref.key: r for r in estate.iter_family("RespondentIdentity", batch_size=16)}
    unresolved = [e for e in events if e.typed_state != "SUBSTANTIVE_RESPONSE"]
    if not unresolved:
        return {"available": False, "red": False}
    event = unresolved[0]
    def _resp_key(value):
        return "|".join((value["kind"], value["object_id"], value["content_hash"])) if isinstance(value, Mapping) else value.key
    key = _resp_key(event.scoped_respondent_ref)
    respondent = identities[key]
    same = tuple(e for e in events if _resp_key(e.scoped_respondent_ref) == key)
    universe = next(estate.iter_family("EmpiricalUniverse", batch_size=8))
    auths = tuple(estate.iter_family("AuthoritySnapshot", batch_size=64))
    registry = AuthorityRegistry(auths)
    leaf = {
        "op": "LEAF",
        "leaf_type": "TYPED_RESPONSE_STATE",
        "empirical_universe_ref": dict(universe.ref.as_dict()),
        "question_semantic_ref": dict(event.native_question_ref),
        "typed_state_ref": dict(event.response_topology_ref),
        "state_semantic_authority_ref": event.authority_snapshot_refs[0].as_dict(),
        "typed_state": "SUBSTANTIVE_RESPONSE",
    }
    node = {"op": "NOT", "children": [leaf]}
    index = _ReleaseIndex(
        release=None,
        universe=universe,
        respondents={key: respondent},
        events_by_respondent={key: same},
        coordinates_by_respondent={key: ()},
        routing_by_respondent={key: ()},
        weights_by_respondent={key: ()},
        source_relations=(),
    )
    used, used_auth = [], []
    try:
        leaf_result = _eval_predicate(
            leaf, respondent=respondent, index=index, registry=registry,
            used=used, used_auth=used_auth,
        )
        result = _eval_predicate(
            node, respondent=respondent, index=index, registry=registry,
            used=used, used_auth=used_auth,
        )
        return {"available": True, "leaf": bool(leaf_result), "red": bool(result), "error": None}
    except Exception as exc:
        return {"available": True, "leaf": None, "red": False, "error": type(exc).__name__}

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
    base_cfg = SourceConfig(copy.deepcopy(doc))
    (root / "private-raw").mkdir(mode=0o700, parents=True, exist_ok=True)
    (root / "private-base").mkdir(mode=0o700, parents=True, exist_ok=True)
    raw_rec = build_single_pass(
        config=raw_cfg, source_path=path, private_root=root / "private-raw",
        chunk_rows=2, compact_spool=True,
    )
    base_rec = build_single_pass(
        config=base_cfg, source_path=path, private_root=root / "private-base",
        chunk_rows=2, compact_spool=True,
    )
    raw_estate, raw_events = _read(root / "private-raw", raw_rec)
    _, base_events = _read(root / "private-base", base_rec)
    raw_mapped = {_mapped_signature(e) for e in raw_events if e.typed_state == "SUBSTANTIVE_RESPONSE"}
    base_mapped = {_mapped_signature(e) for e in base_events if e.typed_state == "SUBSTANTIVE_RESPONSE"}
    states = {}
    for event in raw_events:
        states[event.typed_state] = states.get(event.typed_state, 0) + 1
    unresolved = [e for e in raw_events if e.typed_state != "SUBSTANTIVE_RESPONSE"]
    i03 = _i03_not_witness(raw_estate, raw_events)
    return {
        "source_format": source_format,
        "rows": rows,
        "event_count": len(raw_events),
        "state_counts": dict(sorted(states.items())),
        "mapped_matched_rows": raw_mapped <= base_mapped,
        "mapped_signature_count": len(raw_mapped),
        "unresolved_count": len(unresolved),
        "raw_witness_preserved": all(_raw_witness_ok(e) for e in unresolved),
        "i03_condition_plus_not": i03,
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
        "mapped_matched_rows": a["mapped_matched_rows"] and b["mapped_matched_rows"],
        "raw_witness_preserved": a["raw_witness_preserved"] and b["raw_witness_preserved"],
        "invalid_physical_input_refused": invalid_refused,
        "i03_not_red_proven": a["i03_condition_plus_not"].get("available")
        and a["i03_condition_plus_not"].get("red") is True
        and b["i03_condition_plus_not"].get("available")
        and b["i03_condition_plus_not"].get("red") is True,
    }
    status = "SHARED_RAW_LANE_TEST_PASS_WITH_I03_RED" if all(checks.values()) else "SHARED_RAW_LANE_TEST_FAILED"
    print(json.dumps({
        "status": status, "checks": checks,
        "sav": a, "dta": b,
        "raw_tokens_published": False,
        "source_read_performed": False,
    }, sort_keys=True))
    return 0 if all(checks.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
