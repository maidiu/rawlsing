#!/usr/bin/env python3
"""Consumer-side verification for typed Rawlsing producer boundaries.

The shared boundary module defines transport/integrity primitives.  This module
adds consumer policy without owning stage semantics: strict contract/version
checks, exact producer scope identity, producer-declared artifact-file hashes,
canonical Parquet enforcement, and typed state preservation even when a healthy
producer does not permit the next semantic operation.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    ArtifactInspection,
    BoundaryContractError,
    BoundaryState,
    PIPELINE_BOUNDARY_CONTRACT_VERSION,
    boundary_state_from_payload,
    inspect_artifact,
    read_status_document,
    require_canonical_parquet,
    verify_exact_identity,
)

V551_V3_SCHEMA_VERSION = "v3.0"
V551_V3_COMPILER_VERSION = "v3.0"
V551_V3_CANONICAL_ARTIFACTS = (
    "directional_candidate_adjudication.parquet",
    "relation_evidence_atoms.parquet",
    "directional_distribution_coverage.parquet",
)


@dataclass(frozen=True)
class ProducerBoundaryVerification:
    manifest_path: str
    state: BoundaryState
    verified_artifacts: tuple[ArtifactInspection, ...]
    identity: dict[str, str]
    manifest_payload: dict[str, Any]

    @property
    def integrity_passed(self) -> bool:
        return self.state.run_integrity_status == "PASS"

    @property
    def downstream_permitted(self) -> bool:
        return self.state.downstream_permission_status == "ALLOW"


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _artifact_declarations(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = payload.get("artifacts") or payload.get("artifact_files") or []
    if isinstance(raw, dict):
        rows: list[dict[str, Any]] = []
        for name, value in raw.items():
            if not isinstance(value, Mapping):
                continue
            row = dict(value)
            row.setdefault("artifact", str(name))
            rows.append(row)
        return rows
    if isinstance(raw, list):
        return [dict(row) for row in raw if isinstance(row, Mapping)]
    return []


def _int(value: Any, *, field: str) -> int:
    try:
        out = int(value)
    except Exception as exc:
        raise BoundaryContractError(f"INTEGER_FIELD_INVALID:{field}:{value!r}") from exc
    if out < 0:
        raise BoundaryContractError(f"INTEGER_FIELD_NEGATIVE:{field}:{out}")
    return out


def verify_producer_boundary_manifest(
    manifest_path: str | Path,
    *,
    run_id: str,
    source: str = "",
    wave: str = "",
    country_code: str = "",
    shard_id: str = "",
    required_artifacts: Iterable[str] = (),
    required_schema_version: str = "",
    required_compiler_version: str = "",
    require_downstream_permission: bool = False,
) -> ProducerBoundaryVerification:
    """Verify producer integrity independently from operation permission.

    A producer may be healthy while declaring that the next semantic operation
    is not applicable or is blocked by unresolved evidence.  ``require_downstream_permission``
    is therefore an explicit consumer choice rather than an integrity shortcut.
    """
    manifest = read_status_document(manifest_path)
    if not manifest.exists:
        raise BoundaryContractError(f"MANIFEST_MISSING:{manifest.path}")
    if not manifest.readable:
        raise BoundaryContractError(f"MANIFEST_UNREADABLE:{manifest.path}:{manifest.error}")
    payload = manifest.payload
    state = boundary_state_from_payload(payload)
    if state.contract_version != PIPELINE_BOUNDARY_CONTRACT_VERSION:
        raise BoundaryContractError(
            f"UNSUPPORTED_BOUNDARY_CONTRACT_VERSION:{state.contract_version}"
        )
    if state.run_integrity_status != "PASS":
        raise BoundaryContractError(f"PRODUCER_RUN_INTEGRITY_FAILED:{state.run_integrity_status}")
    if require_downstream_permission and state.downstream_permission_status != "ALLOW":
        raise BoundaryContractError(
            "DOWNSTREAM_NOT_PERMITTED:"
            f"integrity={state.run_integrity_status}:"
            f"evidence={state.evidence_status}:"
            f"permission={state.downstream_permission_status}"
        )

    if required_schema_version and _text(payload.get("schema_version")) != required_schema_version:
        raise BoundaryContractError(
            "PRODUCER_SCHEMA_VERSION_MISMATCH:"
            f"expected={required_schema_version}:actual={_text(payload.get('schema_version')) or '<empty>'}"
        )
    if required_compiler_version and _text(payload.get("compiler_version")) != required_compiler_version:
        raise BoundaryContractError(
            "PRODUCER_COMPILER_VERSION_MISMATCH:"
            f"expected={required_compiler_version}:actual={_text(payload.get('compiler_version')) or '<empty>'}"
        )

    identity = verify_exact_identity(
        payload,
        run_id=run_id,
        source=source,
        wave=wave,
        country_code=country_code,
        shard_id=shard_id,
    )
    declarations = _artifact_declarations(payload)
    by_path = {
        _text(row.get("path") or row.get("relative_path")): row
        for row in declarations
        if _text(row.get("path") or row.get("relative_path"))
    }
    manifest_dir = Path(manifest_path).parent
    verified: list[ArtifactInspection] = []
    for rel in required_artifacts:
        rel_text = str(rel)
        require_canonical_parquet(rel_text)
        declaration = by_path.get(rel_text)
        if declaration is None:
            raise BoundaryContractError(f"ARTIFACT_DECLARATION_MISSING:{rel_text}")
        declared_hash = _text(declaration.get("artifact_file_sha256")).lower()
        if not re.fullmatch(r"[0-9a-f]{64}", declared_hash):
            raise BoundaryContractError(f"ARTIFACT_FILE_SHA256_MISSING_OR_INVALID:{rel_text}")
        if required_schema_version:
            artifact_schema = _text(declaration.get("schema_version"))
            if artifact_schema and artifact_schema != required_schema_version:
                raise BoundaryContractError(
                    "ARTIFACT_SCHEMA_VERSION_MISMATCH:"
                    f"{rel_text}:expected={required_schema_version}:actual={artifact_schema}"
                )
        artifact = inspect_artifact(manifest_dir / rel_text)
        if not artifact.exists:
            raise BoundaryContractError(f"ARTIFACT_MISSING:{rel_text}")
        if not artifact.readable:
            raise BoundaryContractError(f"ARTIFACT_UNREADABLE:{rel_text}:{artifact.error}")
        if artifact.artifact_file_sha256.lower() != declared_hash:
            raise BoundaryContractError(
                "ARTIFACT_FILE_SHA256_MISMATCH:"
                f"{rel_text}:expected={declared_hash}:actual={artifact.artifact_file_sha256.lower()}"
            )
        if "row_count" in declaration and artifact.row_count is not None:
            declared_rows = _int(declaration.get("row_count"), field=f"artifacts[{rel_text}].row_count")
            if declared_rows != artifact.row_count:
                raise BoundaryContractError(
                    f"ARTIFACT_ROW_COUNT_MISMATCH:{rel_text}:expected={declared_rows}:actual={artifact.row_count}"
                )
        verified.append(artifact)
    return ProducerBoundaryVerification(
        manifest_path=str(manifest_path),
        state=state,
        verified_artifacts=tuple(verified),
        identity=identity,
        manifest_payload=dict(payload),
    )


def verify_v551_v3_producer_manifest(
    manifest_path: str | Path,
    *,
    run_id: str,
    source: str,
    wave: str,
    country_code: str = "",
    shard_id: str = "",
) -> ProducerBoundaryVerification:
    """Verify the merged V551 v3.0 producer contract exactly."""
    verified = verify_producer_boundary_manifest(
        manifest_path,
        run_id=run_id,
        source=source,
        wave=wave,
        country_code=country_code,
        shard_id=shard_id,
        required_artifacts=V551_V3_CANONICAL_ARTIFACTS,
        required_schema_version=V551_V3_SCHEMA_VERSION,
        required_compiler_version=V551_V3_COMPILER_VERSION,
        require_downstream_permission=False,
    )
    payload = verified.manifest_payload
    canonical_names = tuple(str(value) for value in payload.get("canonical_artifact_names") or [])
    expected_names = tuple(Path(path).stem for path in V551_V3_CANONICAL_ARTIFACTS)
    if canonical_names != expected_names:
        raise BoundaryContractError(
            f"V551_CANONICAL_ARTIFACT_NAMES_MISMATCH:expected={expected_names}:actual={canonical_names}"
        )

    candidate_count = _int(payload.get("candidate_count"), field="candidate_count")
    promotable_count = _int(payload.get("promotable_candidate_count"), field="promotable_candidate_count")
    nonpromotable_count = _int(payload.get("nonpromotable_candidate_count"), field="nonpromotable_candidate_count")
    atom_count = _int(payload.get("atom_count"), field="atom_count")
    coverage_rows = _int(payload.get("distribution_coverage_rows"), field="distribution_coverage_rows")
    if candidate_count != promotable_count + nonpromotable_count:
        raise BoundaryContractError(
            "V551_CANDIDATE_COUNT_NOT_CONSERVED:"
            f"candidate={candidate_count}:promotable={promotable_count}:nonpromotable={nonpromotable_count}"
        )
    if atom_count != promotable_count:
        raise BoundaryContractError(
            f"V551_ATOM_PROMOTABLE_COUNT_MISMATCH:atoms={atom_count}:promotable={promotable_count}"
        )

    rows_by_name = {
        Path(item.path).name: item.row_count
        for item in verified.verified_artifacts
    }
    expected_rows = {
        "directional_candidate_adjudication.parquet": candidate_count,
        "relation_evidence_atoms.parquet": atom_count,
        "directional_distribution_coverage.parquet": coverage_rows,
    }
    for name, expected in expected_rows.items():
        actual = rows_by_name.get(name)
        if actual != expected:
            raise BoundaryContractError(
                f"V551_ARTIFACT_TOP_LEVEL_COUNT_MISMATCH:{name}:expected={expected}:actual={actual}"
            )

    state = verified.state
    if state.evidence_status == "PRESENT":
        if state.downstream_permission_status != "ALLOW" or atom_count <= 0:
            raise BoundaryContractError("V551_PRESENT_STATE_INCONSISTENT")
    elif state.evidence_status == "APPLICABLE_UNRESOLVED":
        if state.downstream_permission_status != "DENY" or candidate_count <= 0 or atom_count != 0:
            raise BoundaryContractError("V551_APPLICABLE_UNRESOLVED_STATE_INCONSISTENT")
    elif state.evidence_status == "NOT_APPLICABLE":
        if state.downstream_permission_status != "NOT_APPLICABLE" or candidate_count != 0 or atom_count != 0:
            raise BoundaryContractError("V551_NOT_APPLICABLE_STATE_INCONSISTENT")
    else:
        raise BoundaryContractError(f"V551_EVIDENCE_STATUS_UNSUPPORTED:{state.evidence_status}")
    return verified
