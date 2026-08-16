#!/usr/bin/env python3
"""Exact G4 V551J/V552J producer verification for Section85 consumers."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_pipeline_boundary_contract import (  # noqa: E402
    PIPELINE_BOUNDARY_CONTRACT_VERSION,
    inspect_artifact,
    sha256_file,
)
from section85_typed_state import Section85TypedStateError, typed_stage_state  # noqa: E402

V551J_SCHEMA_VERSION = "v2.2.3"
V551J_COMPILER_VERSION = "v551j_joint_evidence_contract_v2_2_3"
V551J_PRESENT_REQUIRED_ARTIFACTS = ("candidate", "component", "certified", "review_surface")
V552_SCHEMA_VERSION = "v3.0"
V552_COMPILER_VERSION = "v3.0"
V552J_SCHEMA_VERSION = "v1.0"
V552J_COMPILER_VERSION = "v552j_structural_join_v1"
V552J_REQUIRED_ARTIFACTS = ("v552j_structural_join_index", "v552j_join_audit")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _json_object(path: str | Path, stage: str) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise Section85TypedStateError(f"SECTION85_{stage.upper()}_MANIFEST_MISSING:{p}")
    try:
        payload = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        raise Section85TypedStateError(
            f"SECTION85_{stage.upper()}_MANIFEST_UNREADABLE:{p}:{type(exc).__name__}:{exc}"
        ) from exc
    if not isinstance(payload, dict):
        raise Section85TypedStateError(f"SECTION85_{stage.upper()}_MANIFEST_NOT_OBJECT:{p}")
    return payload


def _contract_version(payload: Mapping[str, Any]) -> str:
    return _text(payload.get("contract_version") or payload.get("boundary_contract_version"))


def _producer_identity(payload: Mapping[str, Any], stage: str) -> dict[str, str]:
    nested = payload.get("producer_scope_identity")
    scope = dict(nested) if isinstance(nested, Mapping) else {}
    identity = {
        "run_id": _text(scope.get("run_id") or payload.get("producer_run_id") or payload.get("run_id")),
        "source": _text(scope.get("source") or payload.get("source") or payload.get("source_family")),
        "wave": _text(scope.get("canonical_wave") or scope.get("wave") or payload.get("canonical_wave") or payload.get("wave")),
        "country_code": _text(scope.get("country_code") or payload.get("country_code")),
        "shard_id": _text(scope.get("shard_id") or payload.get("shard_id")),
    }
    if not identity["run_id"] or not identity["source"] or not identity["wave"]:
        raise Section85TypedStateError(f"SECTION85_{stage.upper()}_PRODUCER_SCOPE_INCOMPLETE")
    if not identity["country_code"] and not identity["shard_id"]:
        raise Section85TypedStateError(f"SECTION85_{stage.upper()}_COUNTRY_OR_SHARD_IDENTITY_REQUIRED")
    if isinstance(nested, Mapping):
        top = {
            "run_id": _text(payload.get("producer_run_id") or payload.get("run_id")),
            "source": _text(payload.get("source") or payload.get("source_family")),
            "wave": _text(payload.get("canonical_wave") or payload.get("wave")),
            "country_code": _text(payload.get("country_code")),
            "shard_id": _text(payload.get("shard_id")),
        }
        for key, value in top.items():
            if value and identity[key] and value != identity[key]:
                raise Section85TypedStateError(
                    f"SECTION85_{stage.upper()}_TOP_LEVEL_SCOPE_DISAGREEMENT:{key}:top={value}:nested={identity[key]}"
                )
    return identity


def _verify_expected_identity(actual: Mapping[str, str], expected: Mapping[str, Any] | None, stage: str) -> None:
    if not expected:
        return
    want = {
        "run_id": _text(expected.get("run_id") or expected.get("producer_run_id")),
        "source": _text(expected.get("source") or expected.get("source_family")),
        "wave": _text(expected.get("canonical_wave") or expected.get("wave")),
        "country_code": _text(expected.get("country_code")),
        "shard_id": _text(expected.get("shard_id")),
    }
    for key in ("run_id", "source", "wave"):
        if want[key] and actual[key] != want[key]:
            raise Section85TypedStateError(
                f"SECTION85_{stage.upper()}_SCOPE_MISMATCH:{key}:expected={want[key]}:actual={actual[key]}"
            )
    if want["country_code"] and actual["country_code"] != want["country_code"]:
        raise Section85TypedStateError(f"SECTION85_{stage.upper()}_SCOPE_MISMATCH:country_code")
    if not want["country_code"] and want["shard_id"] and actual["shard_id"] != want["shard_id"]:
        raise Section85TypedStateError(f"SECTION85_{stage.upper()}_SCOPE_MISMATCH:shard_id")


def _run_root(manifest_path: Path) -> Path:
    return manifest_path.parent.parent if manifest_path.parent.name == "manifest" else manifest_path.parent


def _declarations(payload: Mapping[str, Any], stage: str) -> dict[str, Mapping[str, Any]]:
    raw = payload.get("artifacts")
    if not isinstance(raw, list):
        raise Section85TypedStateError(f"SECTION85_{stage.upper()}_ARTIFACT_DECLARATIONS_MALFORMED")
    output: dict[str, Mapping[str, Any]] = {}
    for row in raw:
        if not isinstance(row, Mapping):
            raise Section85TypedStateError(f"SECTION85_{stage.upper()}_ARTIFACT_DECLARATION_NOT_OBJECT")
        name = _text(row.get("artifact") or row.get("name"))
        if not name or name in output:
            raise Section85TypedStateError(f"SECTION85_{stage.upper()}_ARTIFACT_NAME_INVALID:{name}")
        output[name] = row
    return output


def _scope_check(path: Path, identity: Mapping[str, str], stage: str, name: str) -> pd.DataFrame:
    try:
        frame = pd.read_parquet(path)
    except Exception as exc:
        raise Section85TypedStateError(
            f"SECTION85_{stage.upper()}_ARTIFACT_SCHEMA_UNREADABLE:{name}:{type(exc).__name__}:{exc}"
        ) from exc
    if frame.empty:
        return frame
    source_col = "source" if "source" in frame else "source_family" if "source_family" in frame else ""
    wave_col = "canonical_wave" if "canonical_wave" in frame else "wave" if "wave" in frame else ""
    if "run_id" not in frame or not source_col or not wave_col:
        raise Section85TypedStateError(f"SECTION85_{stage.upper()}_ARTIFACT_SCOPE_COLUMNS_MISSING:{name}")
    checks = {
        "run_id": ({_text(v) for v in frame["run_id"] if _text(v)}, {identity["run_id"]}),
        "source": ({_text(v) for v in frame[source_col] if _text(v)}, {identity["source"]}),
        "wave": ({_text(v) for v in frame[wave_col] if _text(v)}, {identity["wave"]}),
    }
    for label, (observed, expected) in checks.items():
        if observed != expected:
            raise Section85TypedStateError(
                f"SECTION85_{stage.upper()}_ARTIFACT_SCOPE_MISMATCH:{name}:{label}:expected={sorted(expected)}:actual={sorted(observed)}"
            )
    if identity["country_code"] and "country_code" in frame:
        observed = {_text(v) for v in frame["country_code"] if _text(v)}
        if observed and observed != {identity["country_code"]}:
            raise Section85TypedStateError(f"SECTION85_{stage.upper()}_ARTIFACT_SCOPE_MISMATCH:{name}:country_code")
    elif identity["shard_id"] and "shard_id" in frame:
        observed = {_text(v) for v in frame["shard_id"] if _text(v)}
        if observed and observed != {identity["shard_id"]}:
            raise Section85TypedStateError(f"SECTION85_{stage.upper()}_ARTIFACT_SCOPE_MISMATCH:{name}:shard_id")
    return frame


def _verify_canonical(
    payload: Mapping[str, Any],
    manifest_path: Path,
    *,
    stage: str,
    schema: str,
    compiler: str,
    required: tuple[str, ...],
    scope_check: tuple[str, ...],
) -> tuple[dict[str, dict[str, Any]], dict[str, pd.DataFrame]]:
    identity = _producer_identity(payload, stage)
    canonical = {n: r for n, r in _declarations(payload, stage).items() if _text(r.get("artifact_kind")) == "canonical"}
    missing = sorted(set(required) - set(canonical))
    if missing:
        raise Section85TypedStateError(f"SECTION85_{stage.upper()}_REQUIRED_CANONICAL_ARTIFACTS_MISSING:{','.join(missing)}")
    verified: dict[str, dict[str, Any]] = {}
    frames: dict[str, pd.DataFrame] = {}
    root = _run_root(manifest_path).resolve()
    for name, row in canonical.items():
        if _text(row.get("schema_version")) != schema:
            raise Section85TypedStateError(f"SECTION85_{stage.upper()}_ARTIFACT_SCHEMA_VERSION_MISMATCH:{name}")
        declared_compiler = _text(row.get("compiler_version"))
        if declared_compiler and declared_compiler != compiler:
            raise Section85TypedStateError(f"SECTION85_{stage.upper()}_ARTIFACT_COMPILER_VERSION_MISMATCH:{name}")
        rel = _text(row.get("path") or row.get("relative_path"))
        if Path(rel).suffix.lower() != ".parquet":
            raise Section85TypedStateError(f"SECTION85_{stage.upper()}_CANONICAL_ARTIFACT_NOT_PARQUET:{name}:{rel}")
        path = (manifest_path.parent / rel).resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise Section85TypedStateError(f"SECTION85_{stage.upper()}_ARTIFACT_ESCAPES_RUN_ROOT:{name}:{rel}") from exc
        declared_hash = _text(row.get("artifact_file_sha256")).lower()
        if not _SHA256_RE.fullmatch(declared_hash):
            raise Section85TypedStateError(f"SECTION85_{stage.upper()}_ARTIFACT_FILE_SHA256_INVALID:{name}")
        inspection = inspect_artifact(path)
        if not inspection.exists or not inspection.readable:
            raise Section85TypedStateError(f"SECTION85_{stage.upper()}_ARTIFACT_UNREADABLE:{name}:{inspection.error}")
        if inspection.artifact_file_sha256.lower() != declared_hash:
            raise Section85TypedStateError(
                f"SECTION85_{stage.upper()}_ARTIFACT_FILE_SHA256_MISMATCH:{name}:expected={declared_hash}:actual={inspection.artifact_file_sha256.lower()}"
            )
        if row.get("row_count") is not None and int(row["row_count"]) != int(inspection.row_count or 0):
            raise Section85TypedStateError(f"SECTION85_{stage.upper()}_ARTIFACT_ROW_COUNT_MISMATCH:{name}")
        if name in scope_check:
            frames[name] = _scope_check(path, identity, stage, name)
        verified[name] = {
            "path": str(path),
            "row_count": inspection.row_count,
            "artifact_file_sha256": inspection.artifact_file_sha256.lower(),
        }
    return verified, frames


def _classification(state: Mapping[str, Any]) -> str:
    if not state["integrity_pass"]:
        return "PRODUCER_FAILURE"
    pair = (state["evidence_status"], state["downstream_permission_status"])
    return {
        ("PRESENT", "ALLOW"): "PRESENT_ALLOWED",
        ("PRESENT", "DENY"): "PRESENT_REVIEW_ONLY",
        ("VALID_EMPTY", "NOT_APPLICABLE"): "VALID_EMPTY",
        ("VALID_EMPTY", "DENY"): "VALID_EMPTY",
        ("NOT_APPLICABLE", "NOT_APPLICABLE"): "NOT_APPLICABLE",
        ("APPLICABLE_UNRESOLVED", "DENY"): "APPLICABLE_UNRESOLVED",
    }.get(pair, "UNKNOWN_TYPED_STATE")


def _validate_pair(state: Mapping[str, Any], stage: str) -> None:
    if state["run_integrity_status"] != "PASS":
        return
    allowed = {
        "v551j": {
            ("PRESENT", "ALLOW"), ("PRESENT", "DENY"),
            ("VALID_EMPTY", "NOT_APPLICABLE"), ("VALID_EMPTY", "DENY"),
            ("NOT_APPLICABLE", "NOT_APPLICABLE"), ("APPLICABLE_UNRESOLVED", "DENY"),
        },
        "v552j": {
            ("PRESENT", "ALLOW"), ("PRESENT", "DENY"),
            ("VALID_EMPTY", "NOT_APPLICABLE"), ("NOT_APPLICABLE", "NOT_APPLICABLE"),
            ("APPLICABLE_UNRESOLVED", "DENY"),
        },
    }[stage]
    pair = (state["evidence_status"], state["downstream_permission_status"])
    if pair not in allowed:
        raise Section85TypedStateError(f"SECTION85_{stage.upper()}_STATE_PAIR_INVALID:{pair[0]}/{pair[1]}")


def verify_v551j_producer_manifest(
    manifest_path: str | Path,
    *,
    expected_identity: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    path = Path(manifest_path)
    payload = _json_object(path, "v551j")
    state = typed_stage_state(
        payload, stage="v551j",
        expected_schema_version=V551J_SCHEMA_VERSION,
        expected_compiler_version=V551J_COMPILER_VERSION,
    )
    _validate_pair(state, "v551j")
    identity = _producer_identity(payload, "v551j")
    _verify_expected_identity(identity, expected_identity, "v551j")
    required = V551J_PRESENT_REQUIRED_ARTIFACTS if state["evidence_status"] == "PRESENT" else ()
    verified, _ = _verify_canonical(
        payload, path, stage="v551j", schema=V551J_SCHEMA_VERSION,
        compiler=V551J_COMPILER_VERSION, required=required,
        scope_check=V551J_PRESENT_REQUIRED_ARTIFACTS,
    )
    return {
        **state,
        "producer_run_id": identity["run_id"], "source": identity["source"], "wave": identity["wave"],
        "country_code": identity["country_code"], "shard_id": identity["shard_id"],
        "manifest_path": str(path), "manifest_file_sha256": sha256_file(path),
        "verified_artifacts": verified, "state_classification": _classification(state),
        "review_only": state["evidence_status"] == "PRESENT" and state["downstream_permission_status"] == "DENY",
    }


def _verify_upstream(
    block: Any,
    *,
    label: str,
    schema: str,
    compiler: str,
    identity: Mapping[str, str],
) -> dict[str, str]:
    if not isinstance(block, Mapping):
        raise Section85TypedStateError(f"SECTION85_V552J_{label}_REFERENCE_MISSING")
    path_text = _text(block.get("manifest_path"))
    declared = _text(block.get("manifest_file_sha256")).lower()
    if not path_text or not _SHA256_RE.fullmatch(declared):
        raise Section85TypedStateError(f"SECTION85_V552J_{label}_MANIFEST_REFERENCE_INVALID")
    if _text(block.get("schema_version")) != schema or _text(block.get("compiler_version")) != compiler:
        raise Section85TypedStateError(f"SECTION85_V552J_{label}_VERSION_MISMATCH")
    path = Path(path_text)
    if not path.exists():
        raise Section85TypedStateError(f"SECTION85_V552J_{label}_MANIFEST_MISSING:{path}")
    actual = sha256_file(path)
    if actual != declared:
        raise Section85TypedStateError(
            f"SECTION85_V552J_{label}_MANIFEST_FILE_SHA256_MISMATCH:expected={declared}:actual={actual}"
        )
    payload = _json_object(path, f"v552j_{label.lower()}")
    if _contract_version(payload) != PIPELINE_BOUNDARY_CONTRACT_VERSION:
        raise Section85TypedStateError(f"SECTION85_V552J_{label}_BOUNDARY_CONTRACT_MISMATCH")
    if _text(payload.get("schema_version")) != schema or _text(payload.get("compiler_version")) != compiler:
        raise Section85TypedStateError(f"SECTION85_V552J_{label}_REFERENCED_VERSION_MISMATCH")
    _verify_expected_identity(_producer_identity(payload, f"v552j_{label.lower()}"), identity, f"v552j_{label.lower()}")
    return {"manifest_path": str(path), "manifest_file_sha256": actual}


def verify_v552j_producer_manifest(
    manifest_path: str | Path,
    *,
    expected_identity: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    path = Path(manifest_path)
    payload = _json_object(path, "v552j")
    state = typed_stage_state(
        payload, stage="v552j",
        expected_schema_version=V552J_SCHEMA_VERSION,
        expected_compiler_version=V552J_COMPILER_VERSION,
    )
    _validate_pair(state, "v552j")
    identity = _producer_identity(payload, "v552j")
    _verify_expected_identity(identity, expected_identity, "v552j")
    names = payload.get("canonical_artifact_names")
    if not isinstance(names, list) or set(V552J_REQUIRED_ARTIFACTS) - set(map(str, names)):
        raise Section85TypedStateError("SECTION85_V552J_CANONICAL_ARTIFACT_SET_INVALID")
    verified, frames = _verify_canonical(
        payload, path, stage="v552j", schema=V552J_SCHEMA_VERSION,
        compiler=V552J_COMPILER_VERSION, required=V552J_REQUIRED_ARTIFACTS,
        scope_check=V552J_REQUIRED_ARTIFACTS,
    )
    if payload.get("observed_zero_is_measurement_not_absence") is not True:
        raise Section85TypedStateError("SECTION85_V552J_OBSERVED_ZERO_SEMANTICS_MISSING")
    boundary = payload.get("contract_boundary")
    required_boundary = {
        "synthetic_unknown_primary_rows_allowed": False,
        "missing_constraint_metrics_are_zero": False,
        "structural_matching_requires_exact_scope_before_semantic_score": True,
        "observed_zero_distinct_from_absence_or_unresolved": True,
        "canonical_machine_format": "parquet",
    }
    if not isinstance(boundary, Mapping):
        raise Section85TypedStateError("SECTION85_V552J_CONTRACT_BOUNDARY_MISSING")
    for key, expected in required_boundary.items():
        if boundary.get(key) != expected:
            raise Section85TypedStateError(f"SECTION85_V552J_CONTRACT_BOUNDARY_MISMATCH:{key}")
    try:
        declared_zero = int(payload.get("observed_zero_count") or 0)
    except (TypeError, ValueError) as exc:
        raise Section85TypedStateError("SECTION85_V552J_OBSERVED_ZERO_COUNT_INVALID") from exc
    if declared_zero < 0:
        raise Section85TypedStateError("SECTION85_V552J_OBSERVED_ZERO_COUNT_INVALID")
    join = frames["v552j_structural_join_index"]
    actual_zero = 0
    if not join.empty:
        required = {"observed_zero", "pressure_score", "pressure_score_status", "measurement_evidence_status"}
        missing = sorted(required - set(join.columns))
        if missing:
            raise Section85TypedStateError("SECTION85_V552J_OBSERVED_ZERO_COLUMNS_MISSING:" + ",".join(missing))
        mask = join["observed_zero"].map(lambda v: v is True or _text(v).lower() in {"1", "true", "t", "yes", "y"})
        actual_zero = int(mask.sum())
        for _, row in join.loc[mask].iterrows():
            if _text(row.get("pressure_score_status")) != "OBSERVED_ZERO":
                raise Section85TypedStateError("SECTION85_V552J_OBSERVED_ZERO_STATUS_MISMATCH")
            try:
                value = float(row.get("pressure_score"))
            except (TypeError, ValueError) as exc:
                raise Section85TypedStateError("SECTION85_V552J_OBSERVED_ZERO_VALUE_INVALID") from exc
            if abs(value) > 1e-12:
                raise Section85TypedStateError("SECTION85_V552J_OBSERVED_ZERO_VALUE_NONZERO")
            if _text(row.get("measurement_evidence_status")) in {"APPLICABLE_BUT_UNRESOLVED", "NOT_APPLICABLE"}:
                raise Section85TypedStateError("SECTION85_V552J_OBSERVED_ZERO_COLLAPSES_ABSENCE")
    if actual_zero != declared_zero:
        raise Section85TypedStateError(
            f"SECTION85_V552J_OBSERVED_ZERO_COUNT_MISMATCH:declared={declared_zero}:actual={actual_zero}"
        )
    if declared_zero and state["evidence_status"] != "PRESENT":
        raise Section85TypedStateError("SECTION85_V552J_OBSERVED_ZERO_CANNOT_BE_ABSENCE_STATE")
    exact_identity = {
        "run_id": identity["run_id"], "source": identity["source"], "wave": identity["wave"],
        "country_code": identity["country_code"], "shard_id": identity["shard_id"],
    }
    upstream_v551j = _verify_upstream(
        payload.get("upstream_v551j"), label="UPSTREAM_V551J",
        schema=V551J_SCHEMA_VERSION, compiler=V551J_COMPILER_VERSION, identity=exact_identity,
    )
    upstream_v552 = _verify_upstream(
        payload.get("upstream_v552"), label="UPSTREAM_V552",
        schema=V552_SCHEMA_VERSION, compiler=V552_COMPILER_VERSION, identity=exact_identity,
    )
    return {
        **state,
        "producer_run_id": identity["run_id"], "source": identity["source"], "wave": identity["wave"],
        "country_code": identity["country_code"], "shard_id": identity["shard_id"],
        "manifest_path": str(path), "manifest_file_sha256": sha256_file(path),
        "verified_artifacts": verified, "state_classification": _classification(state),
        "observed_zero_count": declared_zero,
        "constraint_evidence_status": _text(payload.get("constraint_evidence_status")),
        "measurement_state": "OBSERVED_ZERO_PRESENT" if declared_zero else state["evidence_status"],
        "upstream_v551j": upstream_v551j, "upstream_v552": upstream_v552,
    }


def exact_producer_gate(
    manifest_path: str | Path,
    *,
    stage: str,
    expected_identity: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    try:
        if stage == "v551j":
            return verify_v551j_producer_manifest(manifest_path, expected_identity=expected_identity)
        if stage == "v552j":
            return verify_v552j_producer_manifest(manifest_path, expected_identity=expected_identity)
        raise Section85TypedStateError(f"SECTION85_UNSUPPORTED_EXACT_PRODUCER_STAGE:{stage}")
    except Section85TypedStateError as exc:
        return {
            "stage": stage, "typed_contract_valid": False, "run_integrity_status": "FAIL",
            "evidence_status": "APPLICABLE_UNRESOLVED", "downstream_permission_status": "DENY",
            "integrity_pass": False, "evidence_present": False, "operation_permitted": False,
            "valid_nonpresent_evidence_state": False, "state_classification": "PRODUCER_FAILURE",
            "failure_reason": str(exc),
        }
