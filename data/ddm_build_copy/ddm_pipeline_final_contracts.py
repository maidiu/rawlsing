#!/usr/bin/env python3
"""Final W05 consumer verification for the merged V550J→V552J producer graph.

This module does not define stage semantics.  It pins the producer contracts
already merged at G4 and verifies transport/integrity facts before W05 lineage,
preflight, or smoke code treats a stage as a coherent producer: exact version,
run/scope identity, typed state, manifest-declared canonical Parquet bytes, and
upstream manifest hashes where the producer declares a dependency.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable, Mapping

from data.ddm_build_copy.ddm_pipeline_boundary_consumer import (
    ProducerBoundaryVerification,
    verify_producer_boundary_manifest,
    verify_v551_v3_producer_manifest,
)
from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    ArtifactInspection,
    BoundaryContractError,
    PIPELINE_BOUNDARY_CONTRACT_VERSION,
    boundary_state_from_payload,
    inspect_artifact,
    read_status_document,
    sha256_file,
    verify_exact_identity,
)

V550J_SCHEMA_VERSION = "v1"
V550J_COMPILER_VERSION = "v550j_joint_response_patterns_producer_v1"
V550J_GOVERNED_TABLES = (
    "joint_response_pattern_index",
    "joint_response_pattern_item_index",
    "joint_pattern_relation_signature",
)

V551J_SCHEMA_VERSION = "v2.2.3"
V551J_COMPILER_VERSION = "v551j_joint_evidence_contract_v2_2_3"
V551J_CANONICAL_PACKET_FILES = (
    "../packets/v551j_joint_packet_candidate_index.parquet",
    "../packets/v551j_certified_joint_packet_index.parquet",
    "../packets/v551j_review_surface.parquet",
)

V552_SCHEMA_VERSION = "v3.0"
V552_COMPILER_VERSION = "v3.0"
V552_REQUIRED_FILES = (
    "structural/v552_structural_fact_index.parquet",
    "structural/v552_temporal_key_source_index.parquet",
)

V552J_SCHEMA_VERSION = "v1.0"
V552J_COMPILER_VERSION = "v552j_structural_join_v1"
V552J_CANONICAL_FILES = (
    "packets/v552j_structural_join_index.parquet",
    "audits/v552j_join_audit.parquet",
)


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _typed_payload(path: str | Path, label: str) -> tuple[dict[str, Any], Any]:
    document = read_status_document(path)
    if not document.exists:
        raise BoundaryContractError(f"{label}_MANIFEST_MISSING:{path}")
    if not document.readable:
        raise BoundaryContractError(f"{label}_MANIFEST_UNREADABLE:{path}:{document.error}")
    payload = document.payload
    state = boundary_state_from_payload(payload)
    if state.contract_version != PIPELINE_BOUNDARY_CONTRACT_VERSION:
        raise BoundaryContractError(
            f"{label}_BOUNDARY_CONTRACT_VERSION_MISMATCH:{state.contract_version}"
        )
    if state.run_integrity_status != "PASS":
        raise BoundaryContractError(f"{label}_RUN_INTEGRITY_NOT_PASS:{state.run_integrity_status}")
    return payload, state


def _state_consistency(label: str, evidence: str, permission: str) -> None:
    if evidence == "PRESENT":
        if permission not in {"ALLOW", "DENY"}:
            raise BoundaryContractError(f"{label}_PRESENT_PERMISSION_INVALID:{permission}")
        return
    if evidence == "APPLICABLE_UNRESOLVED":
        if permission != "DENY":
            raise BoundaryContractError(f"{label}_UNRESOLVED_PERMISSION_INVALID:{permission}")
        return
    if evidence in {"VALID_EMPTY", "NOT_APPLICABLE"}:
        if permission not in {"NOT_APPLICABLE", "DENY"}:
            raise BoundaryContractError(f"{label}_EMPTY_PERMISSION_INVALID:{permission}")
        return
    raise BoundaryContractError(f"{label}_EVIDENCE_STATUS_UNSUPPORTED:{evidence}")


def _require_artifacts_inside_run_root(
    verified: ProducerBoundaryVerification, manifest_path: str | Path, label: str
) -> None:
    manifest = Path(manifest_path).resolve()
    run_root = manifest.parent.parent if manifest.parent.name == "manifest" else manifest.parent
    for artifact in verified.verified_artifacts:
        try:
            Path(artifact.path).resolve().relative_to(run_root)
        except ValueError as exc:
            raise BoundaryContractError(
                f"{label}_ARTIFACT_ESCAPES_RUN_ROOT:{artifact.path}"
            ) from exc


def _artifact_rows(verified: ProducerBoundaryVerification) -> dict[str, int]:
    return {
        Path(item.path).name: int(item.row_count or 0)
        for item in verified.verified_artifacts
    }


def _artifact_declarations(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = payload.get("artifacts") or []
    return [dict(row) for row in raw if isinstance(row, Mapping)] if isinstance(raw, list) else []


def _declared_matching_paths(payload: Mapping[str, Any], basenames: Iterable[str]) -> tuple[str, ...]:
    wanted = set(basenames)
    paths: list[str] = []
    for row in _artifact_declarations(payload):
        rel = _text(row.get("path") or row.get("relative_path"))
        if (
            rel
            and Path(rel).name in wanted
            and rel.endswith(".parquet")
            and _text(row.get("artifact_kind")) == "canonical"
        ):
            paths.append(rel)
    return tuple(paths)


def _require_hash_field(payload: Mapping[str, Any], field: str, actual_path: str | Path, label: str) -> None:
    declared = _text(payload.get(field)).lower()
    if not re.fullmatch(r"[0-9a-f]{64}", declared):
        raise BoundaryContractError(f"{label}_{field.upper()}_MISSING_OR_INVALID")
    actual = sha256_file(actual_path).lower()
    if declared != actual:
        raise BoundaryContractError(
            f"{label}_{field.upper()}_MISMATCH:expected={declared}:actual={actual}"
        )


def _require_nested_manifest_hash(
    payload: Mapping[str, Any],
    key: str,
    actual_path: str | Path,
    *,
    label: str,
    schema_version: str,
    compiler_version: str,
) -> None:
    nested = payload.get(key)
    if not isinstance(nested, Mapping):
        raise BoundaryContractError(f"{label}_{key.upper()}_DECLARATION_MISSING")
    declared_hash = _text(nested.get("manifest_file_sha256")).lower()
    if not re.fullmatch(r"[0-9a-f]{64}", declared_hash):
        raise BoundaryContractError(f"{label}_{key.upper()}_MANIFEST_HASH_INVALID")
    actual_hash = sha256_file(actual_path).lower()
    if declared_hash != actual_hash:
        raise BoundaryContractError(
            f"{label}_{key.upper()}_MANIFEST_HASH_MISMATCH:expected={declared_hash}:actual={actual_hash}"
        )
    if _text(nested.get("schema_version")) != schema_version:
        raise BoundaryContractError(f"{label}_{key.upper()}_SCHEMA_VERSION_MISMATCH")
    if _text(nested.get("compiler_version")) != compiler_version:
        raise BoundaryContractError(f"{label}_{key.upper()}_COMPILER_VERSION_MISMATCH")


def _v550j_table_path(manifest_path: Path, table_name: str, declaration: Mapping[str, Any]) -> Path:
    declared_text = _text(declaration.get("parquet_path"))
    if not declared_text:
        raise BoundaryContractError(f"V550J_TABLE_PARQUET_PATH_MISSING:{table_name}")
    if Path(declared_text).suffix.lower() != ".parquet":
        raise BoundaryContractError(f"V550J_TABLE_CANONICAL_PARQUET_REQUIRED:{table_name}")
    expected = (manifest_path.parent / f"{table_name}.parquet").resolve()
    declared = Path(declared_text)
    if declared.name != expected.name:
        raise BoundaryContractError(
            f"V550J_TABLE_PATH_MISMATCH:{table_name}:declared={declared_text}:expected={expected}"
        )
    if declared.is_absolute() and declared.resolve() != expected:
        raise BoundaryContractError(
            f"V550J_TABLE_PATH_MISMATCH:{table_name}:declared={declared}:expected={expected}"
        )
    return expected


def verify_v550j_producer_manifest(
    manifest_path: str | Path,
    readiness_path: str | Path,
    *,
    run_id: str,
    source: str,
    wave: str,
    shard_id: str,
) -> ProducerBoundaryVerification:
    manifest_path = Path(manifest_path)
    payload, state = _typed_payload(manifest_path, "V550J")
    readiness, readiness_state = _typed_payload(readiness_path, "V550J_READINESS")
    for label, doc in (("V550J", payload), ("V550J_READINESS", readiness)):
        if _text(doc.get("schema_version")) != V550J_SCHEMA_VERSION:
            raise BoundaryContractError(f"{label}_SCHEMA_VERSION_MISMATCH")
        if _text(doc.get("compiler_version")) != V550J_COMPILER_VERSION:
            raise BoundaryContractError(f"{label}_COMPILER_VERSION_MISMATCH")
        verify_exact_identity(doc, run_id=run_id, source=source, wave=wave, shard_id=shard_id)
    if (
        state.evidence_status != readiness_state.evidence_status
        or state.downstream_permission_status != readiness_state.downstream_permission_status
    ):
        raise BoundaryContractError("V550J_MANIFEST_READINESS_STATE_MISMATCH")
    _state_consistency("V550J", state.evidence_status, state.downstream_permission_status)

    tables = payload.get("tables")
    if not isinstance(tables, Mapping):
        raise BoundaryContractError("V550J_TABLE_DECLARATIONS_MALFORMED")
    canonical_names = payload.get("canonical_artifact_names")
    if not isinstance(canonical_names, list) or not set(V550J_GOVERNED_TABLES).issubset(
        {str(value) for value in canonical_names}
    ):
        raise BoundaryContractError("V550J_CANONICAL_ARTIFACT_SET_INCOMPLETE")

    verified_artifacts: list[ArtifactInspection] = []
    row_counts: list[int] = []
    for table_name in V550J_GOVERNED_TABLES:
        declaration = tables.get(table_name)
        if not isinstance(declaration, Mapping):
            raise BoundaryContractError(f"V550J_TABLE_DECLARATION_MISSING:{table_name}")
        if _text(declaration.get("artifact_kind")) != "canonical":
            raise BoundaryContractError(f"V550J_TABLE_NOT_CANONICAL:{table_name}")
        if _text(declaration.get("schema_version")) != V550J_SCHEMA_VERSION:
            raise BoundaryContractError(f"V550J_TABLE_SCHEMA_VERSION_MISMATCH:{table_name}")
        if _text(declaration.get("compiler_version")) != V550J_COMPILER_VERSION:
            raise BoundaryContractError(f"V550J_TABLE_COMPILER_VERSION_MISMATCH:{table_name}")
        path = _v550j_table_path(manifest_path, table_name, declaration)
        inspection = inspect_artifact(path)
        if not inspection.exists or not inspection.readable:
            raise BoundaryContractError(f"V550J_TABLE_UNREADABLE:{table_name}:{inspection.error}")
        declared_hash = _text(declaration.get("artifact_file_sha256")).lower()
        if not re.fullmatch(r"[0-9a-f]{64}", declared_hash):
            raise BoundaryContractError(f"V550J_TABLE_ARTIFACT_FILE_SHA256_INVALID:{table_name}")
        if inspection.artifact_file_sha256.lower() != declared_hash:
            raise BoundaryContractError(
                f"V550J_TABLE_ARTIFACT_FILE_SHA256_MISMATCH:{table_name}"
            )
        declared_rows = declaration.get("rows")
        if declared_rows is None or int(declared_rows) != int(inspection.row_count or 0):
            raise BoundaryContractError(f"V550J_TABLE_ROW_COUNT_MISMATCH:{table_name}")
        verified_artifacts.append(inspection)
        row_counts.append(int(inspection.row_count or 0))

    if state.evidence_status == "PRESENT":
        if state.downstream_permission_status != "ALLOW" or any(rows <= 0 for rows in row_counts):
            raise BoundaryContractError("V550J_PRESENT_STATE_INCONSISTENT")
    elif state.evidence_status in {"VALID_EMPTY", "NOT_APPLICABLE"}:
        if any(rows != 0 for rows in row_counts):
            raise BoundaryContractError("V550J_EMPTY_STATE_HAS_ROWS")
    return ProducerBoundaryVerification(
        manifest_path=str(manifest_path),
        state=state,
        verified_artifacts=tuple(verified_artifacts),
        identity={"run_id": run_id, "source": source, "wave": wave, "shard_id": shard_id},
        manifest_payload=dict(payload),
    )


def verify_v551_producer_manifest(
    manifest_path: str | Path,
    *,
    run_id: str,
    source: str,
    wave: str,
    country_code: str = "",
    shard_id: str = "",
    bridge_path: str | Path | None = None,
) -> ProducerBoundaryVerification:
    verified = verify_v551_v3_producer_manifest(
        manifest_path,
        run_id=run_id,
        source=source,
        wave=wave,
        country_code=country_code,
        shard_id=shard_id,
    )
    if bridge_path is not None:
        _require_hash_field(
            verified.manifest_payload,
            "producer_bridge_file_sha256",
            bridge_path,
            "V551",
        )
    return verified


def _producer_identity_kwargs(
    payload: Mapping[str, Any],
    *,
    country_code: str,
    shard_id: str,
    label: str,
) -> dict[str, str]:
    raw = payload.get("producer_scope_identity")
    scope = dict(raw) if isinstance(raw, Mapping) else {}
    manifest_country = _text(scope.get("country_code") or payload.get("country_code"))
    manifest_shard = _text(scope.get("shard_id") or payload.get("shard_id"))
    if manifest_country:
        if not country_code:
            raise BoundaryContractError(f"{label}_EXPECTED_COUNTRY_REQUIRED:{manifest_country}")
        if country_code != manifest_country:
            raise BoundaryContractError(
                f"{label}_COUNTRY_IDENTITY_MISMATCH:expected={country_code}:actual={manifest_country}"
            )
        if manifest_shard:
            if not shard_id:
                raise BoundaryContractError(f"{label}_EXPECTED_SHARD_REQUIRED:{manifest_shard}")
            if shard_id != manifest_shard:
                raise BoundaryContractError(
                    f"{label}_SHARD_IDENTITY_MISMATCH:expected={shard_id}:actual={manifest_shard}"
                )
        return {"country_code": country_code, "shard_id": shard_id if manifest_shard else ""}
    if manifest_shard:
        if not shard_id:
            raise BoundaryContractError(f"{label}_EXPECTED_SHARD_REQUIRED:{manifest_shard}")
        if shard_id != manifest_shard:
            raise BoundaryContractError(
                f"{label}_SHARD_IDENTITY_MISMATCH:expected={shard_id}:actual={manifest_shard}"
            )
        return {"country_code": "", "shard_id": shard_id}
    raise BoundaryContractError(f"{label}_COUNTRY_OR_SHARD_IDENTITY_MISSING")


def verify_v551j_producer_manifest(
    manifest_path: str | Path,
    *,
    run_id: str,
    source: str,
    wave: str,
    country_code: str = "",
    shard_id: str = "",
    v551_manifest_path: str | Path | None = None,
    v550j_manifest_path: str | Path | None = None,
) -> ProducerBoundaryVerification:
    payload, state = _typed_payload(manifest_path, "V551J")
    _state_consistency("V551J", state.evidence_status, state.downstream_permission_status)
    declared = _declared_matching_paths(
        payload,
        ("v551j_joint_packet_candidate_index.parquet", "v551j_certified_joint_packet_index.parquet", "v551j_review_surface.parquet"),
    )
    if state.evidence_status == "PRESENT" and len(set(Path(path).name for path in declared)) != 3:
        raise BoundaryContractError("V551J_PRESENT_CANONICAL_PACKET_SET_INCOMPLETE")
    identity_kwargs = _producer_identity_kwargs(
        payload, country_code=country_code, shard_id=shard_id, label="V551J"
    )
    verified = verify_producer_boundary_manifest(
        manifest_path,
        run_id=run_id,
        source=source,
        wave=wave,
        country_code=identity_kwargs["country_code"],
        shard_id=identity_kwargs["shard_id"],
        required_artifacts=declared,
        required_schema_version=V551J_SCHEMA_VERSION,
        required_compiler_version=V551J_COMPILER_VERSION,
        require_downstream_permission=False,
    )
    _require_artifacts_inside_run_root(verified, manifest_path, "V551J")
    rows = _artifact_rows(verified)
    candidate_rows = rows.get("v551j_joint_packet_candidate_index.parquet", 0)
    certified_rows = rows.get("v551j_certified_joint_packet_index.parquet", 0)
    review_rows = rows.get("v551j_review_surface.parquet", 0)
    if state.evidence_status == "PRESENT" and candidate_rows <= 0:
        raise BoundaryContractError("V551J_PRESENT_WITHOUT_CANDIDATES")
    if state.downstream_permission_status == "ALLOW" and certified_rows <= 0:
        raise BoundaryContractError("V551J_ALLOW_WITHOUT_CERTIFIED_PACKET")
    if state.evidence_status in {"VALID_EMPTY", "NOT_APPLICABLE"} and any(
        value > 0 for value in (candidate_rows, certified_rows, review_rows)
    ):
        raise BoundaryContractError("V551J_EMPTY_STATE_HAS_PACKET_ROWS")

    v550j_declared = _text(verified.manifest_payload.get("v550j_upstream_manifest_sha256"))
    v551_declared = _text(verified.manifest_payload.get("v551_upstream_manifest_sha256"))
    if state.evidence_status == "PRESENT":
        if not v550j_declared or not v551_declared:
            raise BoundaryContractError("V551J_PRESENT_REQUIRES_BOTH_UPSTREAM_MANIFEST_HASHES")
    elif not (v550j_declared or v551_declared):
        raise BoundaryContractError("V551J_TYPED_EMPTY_UPSTREAM_MANIFEST_HASH_MISSING")

    if v550j_declared:
        if v550j_manifest_path is None:
            raise BoundaryContractError("V551J_DECLARED_V550J_UPSTREAM_MANIFEST_REQUIRED")
        _require_hash_field(verified.manifest_payload, "v550j_upstream_manifest_sha256", v550j_manifest_path, "V551J")
    if v551_declared:
        if v551_manifest_path is None:
            raise BoundaryContractError("V551J_DECLARED_V551_UPSTREAM_MANIFEST_REQUIRED")
        _require_hash_field(verified.manifest_payload, "v551_upstream_manifest_sha256", v551_manifest_path, "V551J")
    return verified


def verify_v552_producer_manifest(
    manifest_path: str | Path,
    *,
    run_id: str,
    source: str,
    wave: str,
    country_code: str = "",
    shard_id: str = "",
    v551_manifest_path: str | Path | None = None,
) -> ProducerBoundaryVerification:
    payload, state = _typed_payload(manifest_path, "V552")
    _state_consistency("V552", state.evidence_status, state.downstream_permission_status)
    verified = verify_producer_boundary_manifest(
        manifest_path,
        run_id=run_id,
        source=source,
        wave=wave,
        country_code=country_code,
        shard_id=shard_id,
        required_artifacts=V552_REQUIRED_FILES,
        required_schema_version=V552_SCHEMA_VERSION,
        required_compiler_version=V552_COMPILER_VERSION,
        require_downstream_permission=False,
    )
    _require_artifacts_inside_run_root(verified, manifest_path, "V552")
    if v551_manifest_path is not None:
        _require_nested_manifest_hash(
            verified.manifest_payload,
            "upstream_v551",
            v551_manifest_path,
            label="V552",
            schema_version="v3.0",
            compiler_version="v3.0",
        )
    return verified


def verify_v552j_producer_manifest(
    manifest_path: str | Path,
    *,
    run_id: str,
    source: str,
    wave: str,
    country_code: str = "",
    shard_id: str = "",
    v551j_manifest_path: str | Path | None = None,
    v552_manifest_path: str | Path | None = None,
) -> ProducerBoundaryVerification:
    payload, state = _typed_payload(manifest_path, "V552J")
    _state_consistency("V552J", state.evidence_status, state.downstream_permission_status)
    identity_kwargs = _producer_identity_kwargs(
        payload, country_code=country_code, shard_id=shard_id, label="V552J"
    )
    verified = verify_producer_boundary_manifest(
        manifest_path,
        run_id=run_id,
        source=source,
        wave=wave,
        country_code=identity_kwargs["country_code"],
        shard_id=identity_kwargs["shard_id"],
        required_artifacts=V552J_CANONICAL_FILES,
        required_schema_version=V552J_SCHEMA_VERSION,
        required_compiler_version=V552J_COMPILER_VERSION,
        require_downstream_permission=False,
    )
    _require_artifacts_inside_run_root(verified, manifest_path, "V552J")
    names = tuple(str(value) for value in verified.manifest_payload.get("canonical_artifact_names") or [])
    if names != ("v552j_structural_join_index", "v552j_join_audit"):
        raise BoundaryContractError(f"V552J_CANONICAL_ARTIFACT_NAMES_MISMATCH:{names}")
    if v551j_manifest_path is not None:
        _require_nested_manifest_hash(
            verified.manifest_payload,
            "upstream_v551j",
            v551j_manifest_path,
            label="V552J",
            schema_version=V551J_SCHEMA_VERSION,
            compiler_version=V551J_COMPILER_VERSION,
        )
    if v552_manifest_path is not None:
        _require_nested_manifest_hash(
            verified.manifest_payload,
            "upstream_v552",
            v552_manifest_path,
            label="V552J",
            schema_version=V552_SCHEMA_VERSION,
            compiler_version=V552_COMPILER_VERSION,
        )
    return verified


def state_token(verified: ProducerBoundaryVerification) -> str:
    state = verified.state
    return "/".join(
        (state.run_integrity_status, state.evidence_status, state.downstream_permission_status)
    )


__all__ = [
    "V550J_SCHEMA_VERSION",
    "V550J_COMPILER_VERSION",
    "V551J_SCHEMA_VERSION",
    "V551J_COMPILER_VERSION",
    "V552_SCHEMA_VERSION",
    "V552_COMPILER_VERSION",
    "V552J_SCHEMA_VERSION",
    "V552J_COMPILER_VERSION",
    "verify_v550j_producer_manifest",
    "verify_v551_producer_manifest",
    "verify_v551j_producer_manifest",
    "verify_v552_producer_manifest",
    "verify_v552j_producer_manifest",
    "state_token",
]
