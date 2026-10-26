"""Recover and execute the historical V3 actor state on an isolated fixture."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import is_dataclass, asdict
import json
from pathlib import Path
from typing import Any, Mapping

from .bootstrap import IDENTITIES, SOURCE_ROOT, install

install()

from candidate import digest, seal  # noqa: E402

import hashlib  # noqa: E402

V3_FIXTURE = SOURCE_ROOT / "v3/tests/fixtures/identity_minimal.json"
RECOVERED_GRADE = "RECOVERED_HISTORICAL_V3_LEGACY_REPRODUCTION_NOT_NATIVE"
MISSING_ACTUAL = "S50_ACTUAL_ROOT_MISSING_HISTORICAL_V3_STATE"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_source() -> dict:
    doc = json.loads(IDENTITIES.read_text())
    rows = []
    for row in doc.get("selected_files_verified", []):
        path = SOURCE_ROOT / row["path"]
        actual = _sha(path) if path.is_file() else ""
        rows.append({
            "path": row["path"],
            "expected_sha256": row["sha256"],
            "actual_sha256": actual,
            "bytes": path.stat().st_size if path.is_file() else 0,
            "exact": actual == row["sha256"],
        })
    return {
        "schema": "S50_SOURCE_IDENTITY_VERIFICATION@1",
        "source_root": str(SOURCE_ROOT),
        "archive_identity": doc.get("archive_identity_not_rehashed_zip"),
        "count": len(rows),
        "all_exact": bool(rows) and all(row["exact"] for row in rows),
        "rows": rows,
        "fixture_path": str(V3_FIXTURE),
        "fixture_sha256": _sha(V3_FIXTURE) if V3_FIXTURE.is_file() else "",
    }


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _jsonable(getattr(value, key)) for key in value.__dataclass_fields__}
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _projection(state, *, identity: Mapping[str, Any]) -> dict:
    from v3.io.json_codec import state_to_json

    body = json.loads(state_to_json(state))
    return {
        "schema": "S50_READONLY_V3_ACTOR_CONTEXT_PROJECTION@1",
        "grade": RECOVERED_GRADE,
        "native": False,
        "psychology_claim": False,
        "read_only": True,
        "second_mind": False,
        "identity": dict(identity),
        "initial_state_provenance": deepcopy(body.get("initial_state_provenance") or {}),
        "year": body.get("year"),
        "age": body.get("age"),
        "capacity": deepcopy(body.get("capacity") or {}),
        "psychological_capacity": deepcopy(body.get("psychological_capacity") or {}),
        "expectation_baseline": deepcopy(body.get("expectation_baseline") or {}),
        "striving_objects": deepcopy(body.get("striving_objects") or []),
        "active_magnets": deepcopy(body.get("active_magnets") or []),
        "projects": deepcopy(body.get("projects") or []),
        "child_model": deepcopy(body.get("child_model") or {}),
        "pressure_flow_history_last": (
            deepcopy((body.get("pressure_flow_history") or [])[-1])
            if body.get("pressure_flow_history") else None
        ),
        "pressure_flow_memory": deepcopy(body.get("pressure_flow_memory") or {}),
        "surface_psyche_profile": deepcopy(body.get("surface_psyche_profile") or {}),
        "analyst_pressure_account": deepcopy(body.get("analyst_pressure_account") or {}),
        "events_this_year": deepcopy(body.get("events_this_year") or []),
        "access_restrictions": {
            "status": "UNKNOWN_NOT_INITIALIZED",
            "authorized_actor_access": False,
            "observer_surface": "READ_ONLY_PROJECTION",
        },
        "unknowns": [
            "ACTUAL_CURRENT_ACTOR_ACCESS_NOT_INITIALIZED",
            "ACTUAL_CURRENT_ACTOR_OWNED_HISTORY_NOT_BOUND",
            "ACTUAL_ROOT_MISSING_BACKBONE_STATE",
        ],
        "source_files": {
            "backbone_state": str(SOURCE_ROOT / "v3/core/state.py"),
            "identity_to_backbone": str(SOURCE_ROOT / "v3/io/identity_to_backbone.py"),
            "yearly_step": str(SOURCE_ROOT / "v3/engine/yearly_step.py"),
            "pressure_flow": str(SOURCE_ROOT / "v3/psyche/flow.py"),
            "fixture": str(V3_FIXTURE),
            "fixture_sha256": _sha(V3_FIXTURE),
        },
        "state_sha256": digest(body),
    }


def run_legacy_fixture(years: int = 1) -> dict:
    from v3.io.identity_to_backbone import backbone_state_from_identity
    from v3.core.derived import compute_all_derived
    from v3.core.config_loader import load_v3config, load_step_order
    from v3.engine.yearly_step import run_one_year
    from v3.io.json_codec import state_to_json, state_from_json

    identity = json.loads(V3_FIXTURE.read_text())
    state = backbone_state_from_identity(identity, year=2000, age=30)
    derived = compute_all_derived(state)
    config = load_v3config()
    step_order = load_step_order()
    initial_json = state_to_json(state)
    for _ in range(int(years)):
        run_one_year(state, derived, config, step_order)
    final_json = state_to_json(state)
    roundtrip = state_from_json(final_json)
    roundtrip_json = state_to_json(roundtrip)
    projection = _projection(state, identity=identity)
    return {
        "schema": "S50_LEGACY_V3_REPRODUCTION_RUN@1",
        "grade": RECOVERED_GRADE,
        "native": False,
        "psychology_claim": False,
        "fixture_only": True,
        "years": int(years),
        "fixture_sha256": _sha(V3_FIXTURE),
        "source_identity": verify_source(),
        "initial_state_sha256": digest(json.loads(initial_json)),
        "final_state_sha256": digest(json.loads(final_json)),
        "roundtrip_exact": roundtrip_json == final_json,
        "initial_provenance": deepcopy(state.initial_state_provenance),
        "year": state.year,
        "age": state.age,
        "expectation_baseline": deepcopy(state.expectation_baseline),
        "striving_count": len(state.striving_objects),
        "pressure_flow_history_count": len(state.pressure_flow_history),
        "pressure_flow_memory_nonempty": bool(state.pressure_flow_memory),
        "surface_keys": sorted(state.surface_psyche_profile),
        "analyst_keys": sorted(state.analyst_pressure_account),
        "projection": projection,
        "transforms_enabled_by_legacy_fixture": [
            "yearly_step_order", "event_sampling", "micro_drift",
            "age_increment", "pressure_flow_cycle", "derived_recompute",
        ],
        "transforms_not_authorized_for_actual_person": [
            "demographic_to_wound_framework_parent_type", "hopeful_50_parent_default",
            "blind_run_n_years", "years_as_learning_multiplier",
            "native_A_T_learning_coefficients", "two_pass_llm",
        ],
        "actual_person_commit": False,
    }


__all__ = [
    "MISSING_ACTUAL", "RECOVERED_GRADE", "V3_FIXTURE", "run_legacy_fixture",
    "verify_source", "_projection",
]
