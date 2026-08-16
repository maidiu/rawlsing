#!/usr/bin/env python3
"""Section 85 typed producer-state acceptance helpers.

This module consumes the shared rawlsing_pipeline_boundary_v1 transport contract
without inventing stage semantics. V551 v3.0 is frozen at Gate G2 and therefore
has an exact Section 85 consumer contract here. V551J/V552/V552J remain generic
shared-boundary consumers until their producer contracts are merged.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_pipeline_boundary_contract import (  # noqa: E402
    PIPELINE_BOUNDARY_CONTRACT_VERSION,
    BoundaryContractError,
    boundary_state_from_payload,
    inspect_artifact,
)

V551_SCHEMA_VERSION = "v3.0"
V551_REQUIRED_ARTIFACTS = (
    "directional_candidate_adjudication",
    "relation_evidence_atoms",
    "directional_distribution_coverage",
)
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class Section85TypedStateError(RuntimeError):
    """Fail-closed Section 85 consumer-contract error."""


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _contract_version(payload: Mapping[str, Any]) -> str:
    return _text(payload.get("contract_version") or payload.get("boundary_contract_version"))


def typed_stage_state(
    payload: Mapping[str, Any],
    *,
    stage: str,
    expected_schema_version: str | None = None,
) -> dict[str, Any]:
    """Parse one typed producer document without legacy readiness inference.

    Presence of a JSON object, legacy ready booleans, row counts and free-text
    status are deliberately insufficient. A current Section 85 gate requires the
    exact shared boundary contract and typed state fields.
    """
    if not isinstance(payload, Mapping) or not payload:
        raise Section85TypedStateError(f"SECTION85_{stage.upper()}_TYPED_DOCUMENT_MISSING")

    version = _contract_version(payload)
    if version != PIPELINE_BOUNDARY_CONTRACT_VERSION:
        raise Section85TypedStateError(
            f"SECTION85_{stage.upper()}_TYPED_CONTRACT_REQUIRED:"
            f"expected={PIPELINE_BOUNDARY_CONTRACT_VERSION}:actual={version or '<missing>'}"
        )

    if expected_schema_version is not None:
        observed_schema = _text(payload.get("schema_version"))
        if observed_schema != expected_schema_version:
            raise Section85TypedStateError(
                f"SECTION85_{stage.upper()}_SCHEMA_VERSION_MISMATCH:"
                f"expected={expected_schema_version}:actual={observed_schema or '<missing>'}"
            )

    try:
        state = boundary_state_from_payload(payload)
    except BoundaryContractError as exc:
        raise Section85TypedStateError(f"SECTION85_{stage.upper()}_TYPED_STATE_INVALID:{exc}") from exc

    integrity_pass = state.run_integrity_status == "PASS"
    operation_permitted = integrity_pass and state.downstream_permission_status == "ALLOW"
    return {
        "stage": stage,
        "typed_contract_valid": True,
        "contract_version": state.contract_version,
        "schema_version": _text(payload.get("schema_version")),
        "run_integrity_status": state.run_integrity_status,
        "evidence_status": state.evidence_status,
        "downstream_permission_status": state.downstream_permission_status,
        "integrity_pass": integrity_pass,
        "evidence_present": state.evidence_status == "PRESENT",
        "operation_permitted": operation_permitted,
        "valid_nonpresent_evidence_state": integrity_pass
        and state.evidence_status in {"VALID_EMPTY", "NOT_APPLICABLE", "APPLICABLE_UNRESOLVED"},
    }


def typed_stage_gate(
    payload: Mapping[str, Any],
    *,
    stage: str,
    expected_schema_version: str | None = None,
) -> dict[str, Any]:
    """Return a serializable fail-closed gate result instead of raising."""
    try:
        return typed_stage_state(
            payload,
            stage=stage,
            expected_schema_version=expected_schema_version,
        )
    except Section85TypedStateError as exc:
        return {
            "stage": stage,
            "typed_contract_valid": False,
            "contract_version": _contract_version(payload) if isinstance(payload, Mapping) else "",
            "schema_version": _text(payload.get("schema_version")) if isinstance(payload, Mapping) else "",
            "run_integrity_status": "FAIL",
            "evidence_status": "APPLICABLE_UNRESOLVED",
            "downstream_permission_status": "DENY",
            "integrity_pass": False,
            "evidence_present": False,
            "operation_permitted": False,
            "valid_nonpresent_evidence_state": False,
            "failure_reason": str(exc),
        }


def _artifact_declarations(payload: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    raw = payload.get("artifacts")
    if not isinstance(raw, list):
        return {}
    declarations: dict[str, Mapping[str, Any]] = {}
    for row in raw:
        if not isinstance(row, Mapping):
            continue
        name = _text(row.get("artifact") or row.get("name"))
        if name:
            declarations[name] = row
    return declarations


def validate_v551_manifest_contract(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the exact Gate-G2 V551 v3.0 consumer boundary.

    Zero relation-evidence atoms are lawful when the typed producer state says so.
    Integrity is established by the producer contract, canonical artifact
    declarations and exact file-hash declarations -- never by row_count > 0.
    """
    state = typed_stage_state(payload, stage="v551", expected_schema_version=V551_SCHEMA_VERSION)

    run_id = _text(payload.get("producer_run_id") or payload.get("run_id"))
    source = _text(payload.get("source"))
    wave = _text(payload.get("canonical_wave") or payload.get("wave"))
    country = _text(payload.get("country_code"))
    shard = _text(payload.get("shard_id"))
    if not run_id:
        raise Section85TypedStateError("SECTION85_V551_PRODUCER_RUN_ID_MISSING")
    if not source or not wave:
        raise Section85TypedStateError("SECTION85_V551_PRODUCER_SCOPE_MISSING")
    if not country and not shard:
        raise Section85TypedStateError("SECTION85_V551_COUNTRY_OR_SHARD_IDENTITY_MISSING")

    canonical_names = payload.get("canonical_artifact_names")
    if not isinstance(canonical_names, list) or not set(V551_REQUIRED_ARTIFACTS).issubset(set(map(str, canonical_names))):
        raise Section85TypedStateError("SECTION85_V551_CANONICAL_ARTIFACT_SET_INVALID")

    declarations = _artifact_declarations(payload)
    artifact_contract: dict[str, dict[str, Any]] = {}
    for name in V551_REQUIRED_ARTIFACTS:
        declaration = declarations.get(name)
        if declaration is None:
            raise Section85TypedStateError(f"SECTION85_V551_ARTIFACT_DECLARATION_MISSING:{name}")
        path = _text(declaration.get("path") or declaration.get("relative_path"))
        declared_hash = _text(declaration.get("artifact_file_sha256")).lower()
        if not path.endswith(".parquet"):
            raise Section85TypedStateError(f"SECTION85_V551_CANONICAL_ARTIFACT_NOT_PARQUET:{name}:{path}")
        if not _SHA256_RE.fullmatch(declared_hash):
            raise Section85TypedStateError(f"SECTION85_V551_ARTIFACT_FILE_SHA256_INVALID:{name}")
        row_count = declaration.get("row_count")
        if row_count is not None:
            try:
                if int(row_count) < 0:
                    raise ValueError
            except (TypeError, ValueError):
                raise Section85TypedStateError(f"SECTION85_V551_ARTIFACT_ROW_COUNT_INVALID:{name}")
        artifact_contract[name] = {
            "path": path,
            "artifact_file_sha256": declared_hash,
            "row_count": int(row_count) if row_count is not None else None,
        }

    atoms_declared_rows = artifact_contract["relation_evidence_atoms"]["row_count"]
    if atoms_declared_rows is not None and "atom_count" in payload:
        try:
            if int(payload.get("atom_count", 0)) != atoms_declared_rows:
                raise Section85TypedStateError("SECTION85_V551_ATOM_COUNT_DECLARATION_MISMATCH")
        except (TypeError, ValueError) as exc:
            raise Section85TypedStateError("SECTION85_V551_ATOM_COUNT_INVALID") from exc

    evidence = state["evidence_status"]
    permission = state["downstream_permission_status"]
    if evidence == "PRESENT" and permission != "ALLOW":
        raise Section85TypedStateError("SECTION85_V551_PRESENT_EVIDENCE_MUST_ALLOW_DOWNSTREAM")
    if evidence == "APPLICABLE_UNRESOLVED" and permission != "DENY":
        raise Section85TypedStateError("SECTION85_V551_UNRESOLVED_EVIDENCE_MUST_DENY_DOWNSTREAM")
    if evidence == "NOT_APPLICABLE" and permission != "NOT_APPLICABLE":
        raise Section85TypedStateError("SECTION85_V551_NOT_APPLICABLE_PERMISSION_MISMATCH")

    return {
        **state,
        "producer_run_id": run_id,
        "source": source,
        "wave": wave,
        "country_code": country,
        "shard_id": shard,
        "canonical_artifacts": artifact_contract,
        "atom_row_count_is_integrity_gate": False,
    }


def verify_v551_artifact_files(payload: Mapping[str, Any], run_root: str | Path) -> dict[str, Any]:
    """Verify V551 canonical bytes against producer-declared file SHA-256 values."""
    contract = validate_v551_manifest_contract(payload)
    root = Path(run_root)
    verified: dict[str, dict[str, Any]] = {}
    for name, declaration in contract["canonical_artifacts"].items():
        artifact = inspect_artifact(root / declaration["path"])
        if not artifact.exists:
            raise Section85TypedStateError(f"SECTION85_V551_ARTIFACT_MISSING:{name}")
        if not artifact.readable:
            raise Section85TypedStateError(f"SECTION85_V551_ARTIFACT_UNREADABLE:{name}:{artifact.error}")
        if artifact.artifact_file_sha256.lower() != declaration["artifact_file_sha256"]:
            raise Section85TypedStateError(
                f"SECTION85_V551_ARTIFACT_FILE_SHA256_MISMATCH:{name}:"
                f"expected={declaration['artifact_file_sha256']}:actual={artifact.artifact_file_sha256.lower()}"
            )
        verified[name] = {
            "path": artifact.path,
            "row_count": artifact.row_count,
            "artifact_file_sha256": artifact.artifact_file_sha256.lower(),
        }
    return {**contract, "verified_artifacts": verified}
