#!/usr/bin/env python3
"""Shared fail-closed lineage, manifest, and publication infrastructure.

This module is deliberately semantic-neutral. Stage owners declare their own
status/evidence meaning; this module only enforces transport/integrity facts:
contract version, typed state, exact scope identity, producer-declared file
hashes, canonical Parquet output, and stale-safe publication.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

import pandas as pd

PIPELINE_BOUNDARY_CONTRACT_VERSION = "rawlsing_pipeline_boundary_v1"
RUN_INTEGRITY_STATUSES = frozenset({"PASS", "FAIL"})
EVIDENCE_STATUSES = frozenset({"PRESENT", "VALID_EMPTY", "NOT_APPLICABLE", "APPLICABLE_UNRESOLVED"})
DOWNSTREAM_PERMISSION_STATUSES = frozenset({"ALLOW", "DENY", "NOT_APPLICABLE"})

_READY_LEGACY = re.compile(r"^(?:READY|PASS|PASSED|SUCCESS|COMPLETE|COMPLETED|VALIDATED|OK)(?:_[A-Z0-9]+)*$")
_BLOCKED_LEGACY = re.compile(r"^(?:BLOCKED|NOT_READY|FAILED|FAIL|EMPTY_NO|MISSING_REQUIRED)(?:_[A-Z0-9]+)*$")


class PipelineBoundaryError(RuntimeError):
    """Base class for fail-closed pipeline boundary failures."""


class DependencyLedgerError(PipelineBoundaryError):
    """Raised when an explicitly requested dependency ledger is not verifiable."""


class BoundaryContractError(PipelineBoundaryError):
    """Raised when a producer manifest violates the frozen boundary contract."""


class PublicationError(PipelineBoundaryError):
    """Raised when stale-safe publication cannot be completed."""


@dataclass(frozen=True)
class ArtifactInspection:
    path: str
    exists: bool
    readable: bool
    row_count: int | None
    artifact_file_sha256: str
    error: str = ""

    @property
    def valid_empty(self) -> bool:
        return self.exists and self.readable and self.row_count == 0


@dataclass(frozen=True)
class StatusDocument:
    path: str
    exists: bool
    readable: bool
    payload: dict[str, Any] = field(default_factory=dict)
    error: str = ""


@dataclass(frozen=True)
class BoundaryState:
    contract_version: str
    run_integrity_status: str
    evidence_status: str
    downstream_permission_status: str
    source: str = ""
    adapter: str = "typed"

    @property
    def permits_downstream(self) -> bool:
        return self.run_integrity_status == "PASS" and self.downstream_permission_status == "ALLOW"


@dataclass(frozen=True)
class BoundaryVerification:
    manifest_path: str
    state: BoundaryState
    verified_artifacts: tuple[ArtifactInspection, ...]
    identity: dict[str, str]


def sha256_file(path: str | Path) -> str:
    p = Path(path)
    digest = hashlib.sha256()
    with p.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_external_dependency_ledger(path: str | Path, expected_sha256: str) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise DependencyLedgerError(f"DEPENDENCY_LEDGER_MISSING:{p}")
    if not expected_sha256 or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_sha256):
        raise DependencyLedgerError("DEPENDENCY_LEDGER_SHA256_REQUIRED")
    actual = sha256_file(p)
    if actual.lower() != expected_sha256.lower():
        raise DependencyLedgerError(
            f"DEPENDENCY_LEDGER_SHA256_MISMATCH:expected={expected_sha256.lower()}:actual={actual.lower()}"
        )
    try:
        payload = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        raise DependencyLedgerError(f"DEPENDENCY_LEDGER_UNREADABLE:{p}:{type(exc).__name__}:{exc}") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("stages"), dict):
        raise DependencyLedgerError(f"DEPENDENCY_LEDGER_SCHEMA_INVALID:{p}")
    return payload


def _parquet_row_count(path: Path) -> int:
    try:
        import pyarrow.parquet as pq  # type: ignore

        return int(pq.ParquetFile(path).metadata.num_rows)
    except ImportError:
        return int(len(pd.read_parquet(path)))


def inspect_artifact(path: str | Path) -> ArtifactInspection:
    p = Path(path)
    if not p.exists():
        return ArtifactInspection(str(p), False, False, None, "", "MISSING")
    try:
        file_hash = sha256_file(p)
    except Exception as exc:
        return ArtifactInspection(str(p), True, False, None, "", f"HASH_ERROR:{type(exc).__name__}:{exc}")

    suffix = p.suffix.lower()
    try:
        if suffix == ".parquet":
            rows: int | None = _parquet_row_count(p)
        elif suffix == ".csv":
            rows = int(pd.read_csv(p, low_memory=False).shape[0])
        elif suffix == ".json":
            payload = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(payload, list):
                rows = len(payload)
            elif isinstance(payload, dict):
                rows = 1 if payload else 0
            else:
                rows = 1
        else:
            with p.open("rb") as handle:
                handle.read(1)
            rows = None
    except Exception as exc:
        return ArtifactInspection(
            str(p), True, False, None, file_hash, f"READ_ERROR:{type(exc).__name__}:{exc}"
        )
    return ArtifactInspection(str(p), True, True, rows, file_hash, "")


def read_status_document(path: str | Path) -> StatusDocument:
    p = Path(path)
    if not p.exists():
        return StatusDocument(str(p), False, False, error="MISSING")
    try:
        if p.suffix.lower() == ".json":
            payload = json.loads(p.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("status JSON must be an object")
        elif p.suffix.lower() == ".parquet":
            frame = pd.read_parquet(p)
            if frame.empty:
                payload = {}
            else:
                payload = {str(k): v for k, v in frame.iloc[0].to_dict().items()}
        else:
            raise ValueError(f"unsupported status document format: {p.suffix}")
    except Exception as exc:
        return StatusDocument(str(p), True, False, error=f"READ_ERROR:{type(exc).__name__}:{exc}")
    return StatusDocument(str(p), True, True, payload=payload)


def _text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()


def legacy_status_to_state(status: Any) -> BoundaryState:
    """Explicit legacy adapter. It never uses substring readiness tests."""
    text = _text(status).upper()
    if text.startswith("STATUS:"):
        text = text.split(":", 1)[1].strip()
    if _READY_LEGACY.fullmatch(text):
        return BoundaryState("legacy", "PASS", "PRESENT", "ALLOW", source=text, adapter="legacy_exact_grammar")
    if _BLOCKED_LEGACY.fullmatch(text):
        return BoundaryState("legacy", "FAIL", "APPLICABLE_UNRESOLVED", "DENY", source=text, adapter="legacy_exact_grammar")
    raise BoundaryContractError(f"LEGACY_STATUS_UNKNOWN:{text or '<empty>'}")


def boundary_state_from_payload(payload: Mapping[str, Any], status_keys: Iterable[str] = ()) -> BoundaryState:
    version = _text(payload.get("contract_version") or payload.get("boundary_contract_version"))
    if version:
        if version != PIPELINE_BOUNDARY_CONTRACT_VERSION:
            raise BoundaryContractError(f"UNSUPPORTED_BOUNDARY_CONTRACT_VERSION:{version}")
        integrity = _text(payload.get("run_integrity_status")).upper()
        evidence = _text(payload.get("evidence_status")).upper()
        permission = _text(payload.get("downstream_permission_status")).upper()
        if integrity not in RUN_INTEGRITY_STATUSES:
            raise BoundaryContractError(f"RUN_INTEGRITY_STATUS_INVALID:{integrity or '<empty>'}")
        if evidence not in EVIDENCE_STATUSES:
            raise BoundaryContractError(f"EVIDENCE_STATUS_INVALID:{evidence or '<empty>'}")
        if permission not in DOWNSTREAM_PERMISSION_STATUSES:
            raise BoundaryContractError(f"DOWNSTREAM_PERMISSION_STATUS_INVALID:{permission or '<empty>'}")
        if integrity != "PASS" and permission == "ALLOW":
            raise BoundaryContractError("DOWNSTREAM_PERMISSION_ALLOW_WITH_NONPASS_INTEGRITY")
        if evidence == "NOT_APPLICABLE" and permission not in {"NOT_APPLICABLE", "DENY"}:
            raise BoundaryContractError("NOT_APPLICABLE_EVIDENCE_CANNOT_ALLOW_DOWNSTREAM")
        return BoundaryState(version, integrity, evidence, permission)

    keys = tuple(status_keys) or ("status", "final_status", "readiness_status", "overall_status", "validation_status")
    for key in keys:
        value = _text(payload.get(key))
        if value:
            return legacy_status_to_state(value)
    raise BoundaryContractError("STATUS_FIELD_MISSING_OR_EMPTY")


def _identity_value(payload: Mapping[str, Any], keys: Iterable[str]) -> str:
    for key in keys:
        value = _text(payload.get(key))
        if value:
            return value
    return ""


def verify_exact_identity(
    payload: Mapping[str, Any],
    *,
    run_id: str,
    source: str = "",
    wave: str = "",
    country_code: str = "",
    shard_id: str = "",
) -> dict[str, str]:
    expected = {
        "run_id": (run_id, ("producer_run_id", "run_id")),
        "source": (source, ("source", "source_family", "survey_family", "canonical_source")),
        "wave": (wave, ("wave", "canonical_wave", "wave_id")),
        "country_code": (country_code, ("country_code", "country")),
        "shard_id": (shard_id, ("shard_id",)),
    }
    resolved: dict[str, str] = {}
    for label, (want, keys) in expected.items():
        if not want:
            continue
        got = _identity_value(payload, keys)
        if not got:
            raise BoundaryContractError(f"IDENTITY_FIELD_MISSING:{label}")
        if got != want:
            raise BoundaryContractError(f"IDENTITY_MISMATCH:{label}:expected={want}:actual={got}")
        resolved[label] = got
    return resolved


def _artifact_declarations(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = payload.get("artifacts") or payload.get("artifact_files") or []
    if isinstance(raw, dict):
        rows = []
        for name, value in raw.items():
            if isinstance(value, Mapping):
                row = dict(value)
                row.setdefault("name", str(name))
                rows.append(row)
        return rows
    return [dict(row) for row in raw if isinstance(row, Mapping)] if isinstance(raw, list) else []


def verify_boundary_manifest(
    manifest_path: str | Path,
    *,
    run_id: str,
    source: str = "",
    wave: str = "",
    country_code: str = "",
    shard_id: str = "",
    required_artifacts: Iterable[str] = (),
) -> BoundaryVerification:
    manifest = read_status_document(manifest_path)
    if not manifest.exists:
        raise BoundaryContractError(f"MANIFEST_MISSING:{manifest.path}")
    if not manifest.readable:
        raise BoundaryContractError(f"MANIFEST_UNREADABLE:{manifest.path}:{manifest.error}")
    payload = manifest.payload
    state = boundary_state_from_payload(payload)
    if state.contract_version != PIPELINE_BOUNDARY_CONTRACT_VERSION:
        raise BoundaryContractError("STRICT_BOUNDARY_REQUIRES_TYPED_CONTRACT")
    if not state.permits_downstream:
        raise BoundaryContractError(
            f"DOWNSTREAM_NOT_PERMITTED:integrity={state.run_integrity_status}:evidence={state.evidence_status}:permission={state.downstream_permission_status}"
        )
    identity = verify_exact_identity(
        payload, run_id=run_id, source=source, wave=wave, country_code=country_code, shard_id=shard_id
    )
    base = Path(manifest_path).parent
    declarations = _artifact_declarations(payload)
    by_path = {
        _text(row.get("path") or row.get("relative_path")): row
        for row in declarations
        if _text(row.get("path") or row.get("relative_path"))
    }
    verified: list[ArtifactInspection] = []
    for rel in required_artifacts:
        declaration = by_path.get(str(rel))
        if declaration is None:
            raise BoundaryContractError(f"ARTIFACT_DECLARATION_MISSING:{rel}")
        declared_hash = _text(declaration.get("artifact_file_sha256")).lower()
        if not re.fullmatch(r"[0-9a-f]{64}", declared_hash):
            raise BoundaryContractError(f"ARTIFACT_FILE_SHA256_MISSING_OR_INVALID:{rel}")
        artifact = inspect_artifact(base / rel)
        if not artifact.exists:
            raise BoundaryContractError(f"ARTIFACT_MISSING:{rel}")
        if not artifact.readable:
            raise BoundaryContractError(f"ARTIFACT_UNREADABLE:{rel}:{artifact.error}")
        if artifact.artifact_file_sha256.lower() != declared_hash:
            raise BoundaryContractError(
                f"ARTIFACT_FILE_SHA256_MISMATCH:{rel}:expected={declared_hash}:actual={artifact.artifact_file_sha256.lower()}"
            )
        verified.append(artifact)
    return BoundaryVerification(str(manifest_path), state, tuple(verified), identity)


def require_canonical_parquet(path: str | Path) -> Path:
    p = Path(path)
    if p.suffix.lower() != ".parquet":
        raise BoundaryContractError(f"CANONICAL_MACHINE_ARTIFACT_MUST_BE_PARQUET:{p}")
    return p


def validate_machine_output_policy(*, write_parquet: bool, write_csv: bool) -> None:
    if not write_parquet:
        raise BoundaryContractError("PARQUET_CANONICAL_OUTPUT_REQUIRED")
    _ = write_csv


def load_closed_35_waves(authority_path: str | Path) -> tuple[tuple[str, str, str], ...]:
    """Derive governed all-wave scope from the frozen active question authority."""
    path = Path(authority_path)
    if not path.exists():
        raise BoundaryContractError(f"CLOSED_35_WAVE_AUTHORITY_MISSING:{path}")
    pairs: set[tuple[str, str]] = set()
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"source_family", "canonical_wave"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise BoundaryContractError(f"CLOSED_35_WAVE_AUTHORITY_SCHEMA_INVALID:{path}")
        for row in reader:
            source = _text(row.get("source_family"))
            wave = _text(row.get("canonical_wave"))
            if source and wave:
                pairs.add((source, wave))
    ordered = tuple((source, wave, "") for source, wave in sorted(pairs, key=lambda item: (item[0], item[1])))
    if len(ordered) != 35:
        raise BoundaryContractError(f"CLOSED_35_WAVE_COUNT_MISMATCH:expected=35:actual={len(ordered)}")
    if ("Asian Barometer", "W6", "") in ordered:
        raise BoundaryContractError("CLOSED_35_WAVE_SCOPE_ILLEGAL_ASIAN_BAROMETER_W6")
    return ordered


def atomic_write_bytes(path: str | Path, content: bytes) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent))
    temp = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, target)
    except Exception:
        temp.unlink(missing_ok=True)
        raise


def atomic_write_json(path: str | Path, payload: Mapping[str, Any]) -> None:
    atomic_write_bytes(path, (json.dumps(dict(payload), indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))


def publish_staged_directory(staging_dir: str | Path, final_dir: str | Path) -> None:
    """Publish one complete stage directory, replacing stale prior contents."""
    staging = Path(staging_dir)
    final = Path(final_dir)
    if not staging.is_dir():
        raise PublicationError(f"STAGING_DIRECTORY_MISSING:{staging}")
    final.parent.mkdir(parents=True, exist_ok=True)
    backup = final.with_name(f".{final.name}.stale-{os.getpid()}")
    if backup.exists():
        shutil.rmtree(backup)
    moved_old = False
    try:
        if final.exists():
            os.replace(final, backup)
            moved_old = True
        os.replace(staging, final)
    except Exception as exc:
        if moved_old and backup.exists() and not final.exists():
            os.replace(backup, final)
        raise PublicationError(f"ATOMIC_DIRECTORY_PUBLICATION_FAILED:{final}:{type(exc).__name__}:{exc}") from exc
    if backup.exists():
        shutil.rmtree(backup)
