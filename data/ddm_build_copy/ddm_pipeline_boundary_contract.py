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

from data.ddm_build_copy.ddm_source_wave_identity import (
    SourceWaveIdentityError,
    load_identity_registry,
    resolve_source_family_identity,
    resolve_source_wave_identity,
)

PIPELINE_BOUNDARY_CONTRACT_VERSION = "rawlsing_pipeline_boundary_v1"
RUN_INTEGRITY_STATUSES = frozenset({"PASS", "FAIL"})
EVIDENCE_STATUSES = frozenset({"PRESENT", "VALID_EMPTY", "NOT_APPLICABLE", "APPLICABLE_UNRESOLVED"})
DOWNSTREAM_PERMISSION_STATUSES = frozenset({"ALLOW", "DENY", "NOT_APPLICABLE"})

_READY_LEGACY = re.compile(r"^(?:READY|PASS|PASSED|SUCCESS|COMPLETE|COMPLETED|VALIDATED|OK)(?:_[A-Z0-9]+)*$")
_BLOCKED_LEGACY = re.compile(r"^(?:BLOCKED|NOT_READY|FAILED|FAIL|EMPTY_NO|MISSING_REQUIRED)(?:_[A-Z0-9]+)*$")

_SOURCE_REPRESENTATION_FIELDS = (
    "source",
    "source_family",
    "survey_family",
    "canonical_source",
    "canonical_display_source",
    "raw_source",
)
_WAVE_REPRESENTATION_FIELDS = (
    "wave",
    "canonical_wave",
    "wave_id",
    "canonical_display_wave",
    "raw_wave",
)
_SOURCE_UID_FIELDS = ("source_family_uid",)
_WAVE_UID_FIELDS = ("wave_uid",)
_IDENTITY_CONTAINER_FIELDS = (
    "producer_scope_identity",
    "scope_identity",
    "source_wave_identity",
)


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


@dataclass(frozen=True)
class SourceWaveIdentityCoherence:
    """One governed machine identity plus every historical representation seen."""

    source_family_uid: str
    wave_uid: str
    canonical_display_source: str
    canonical_display_wave: str
    source_representations: tuple[tuple[str, str], ...]
    wave_representations: tuple[tuple[str, str], ...]
    source_uid_representations: tuple[tuple[str, str], ...]
    wave_uid_representations: tuple[tuple[str, str], ...]

    @property
    def complete(self) -> bool:
        return bool(self.source_family_uid and self.wave_uid)


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


def _identity_mappings(payload: Mapping[str, Any]) -> tuple[tuple[str, Mapping[str, Any]], ...]:
    mappings: list[tuple[str, Mapping[str, Any]]] = [("", payload)]
    for field in _IDENTITY_CONTAINER_FIELDS:
        nested = payload.get(field)
        if isinstance(nested, Mapping):
            mappings.append((field, nested))
    return tuple(mappings)


def _populated_representations(
    payload: Mapping[str, Any], fields: Iterable[str]
) -> tuple[tuple[str, str], ...]:
    values: list[tuple[str, str]] = []
    for prefix, mapping in _identity_mappings(payload):
        for field in fields:
            value = _text(mapping.get(field))
            if not value:
                continue
            qualified = f"{prefix}.{field}" if prefix else field
            values.append((qualified, value))
    return tuple(values)


def _representation_summary(rows: Iterable[tuple[str, str, str]]) -> str:
    return ",".join(f"{field}={value!r}->{uid}" for field, value, uid in rows)


def validate_source_wave_identity_coherence(
    payload: Mapping[str, Any],
    *,
    expected_source: str = "",
    expected_wave: str = "",
    expected_source_family_uid: str = "",
    expected_wave_uid: str = "",
    registry_path: str | Path | None = None,
    require_complete: bool = False,
) -> SourceWaveIdentityCoherence:
    """Resolve every populated source/wave representation to one governed UID pair.

    Historical labels remain provenance only.  No source, wave, canonical, raw,
    or UID field is privileged by position or first-nonblank precedence.
    Equivalent family-scoped aliases are accepted; contradictions fail closed.
    """
    source_rows = list(_populated_representations(payload, _SOURCE_REPRESENTATION_FIELDS))
    wave_rows = list(_populated_representations(payload, _WAVE_REPRESENTATION_FIELDS))
    source_uid_rows = list(_populated_representations(payload, _SOURCE_UID_FIELDS))
    wave_uid_rows = list(_populated_representations(payload, _WAVE_UID_FIELDS))

    registry = load_identity_registry(registry_path)

    resolved_sources: list[tuple[str, str, str]] = []
    for field, value in source_rows:
        try:
            identity = resolve_source_family_identity(value, registry_path=registry_path)
        except SourceWaveIdentityError as exc:
            raise BoundaryContractError(
                f"SOURCE_IDENTITY_UNRESOLVED:{field}={value!r}:{type(exc).__name__}:{exc}"
            ) from exc
        resolved_sources.append((field, value, identity.source_family_uid))

    if _text(expected_source):
        try:
            expected_identity = resolve_source_family_identity(
                expected_source, registry_path=registry_path
            )
        except SourceWaveIdentityError as exc:
            raise BoundaryContractError(
                f"EXPECTED_SOURCE_IDENTITY_UNRESOLVED:{expected_source!r}:{type(exc).__name__}:{exc}"
            ) from exc
        resolved_sources.append(
            ("<expected_source>", _text(expected_source), expected_identity.source_family_uid)
        )

    resolved_source_uids: list[tuple[str, str, str]] = []
    for field, value in source_uid_rows:
        if value not in registry.source_uid_index:
            raise BoundaryContractError(f"SOURCE_FAMILY_UID_UNKNOWN:{field}={value!r}")
        resolved_source_uids.append((field, value, value))
    if _text(expected_source_family_uid):
        value = _text(expected_source_family_uid)
        if value not in registry.source_uid_index:
            raise BoundaryContractError(f"EXPECTED_SOURCE_FAMILY_UID_UNKNOWN:{value!r}")
        resolved_source_uids.append(("<expected_source_family_uid>", value, value))

    source_uid_candidates = {
        uid for _, _, uid in [*resolved_sources, *resolved_source_uids] if uid
    }
    if len(source_uid_candidates) > 1:
        summary = _representation_summary([*resolved_sources, *resolved_source_uids])
        raise BoundaryContractError(f"SOURCE_IDENTITY_CONTRADICTION:{summary}")
    source_uid = next(iter(source_uid_candidates), "")

    if wave_rows and not source_uid:
        raise BoundaryContractError("SOURCE_IDENTITY_REQUIRED_FOR_WAVE_REPRESENTATIONS")

    canonical_source = ""
    if source_uid:
        canonical_source = _text(
            registry.source_uid_index[source_uid].get("canonical_display_source")
        )

    resolved_waves: list[tuple[str, str, str]] = []
    for field, value in wave_rows:
        try:
            identity = resolve_source_wave_identity(
                canonical_source, value, registry_path=registry_path
            )
        except SourceWaveIdentityError as exc:
            raise BoundaryContractError(
                f"WAVE_IDENTITY_UNRESOLVED:{field}={value!r}:source_uid={source_uid or '<empty>'}:"
                f"{type(exc).__name__}:{exc}"
            ) from exc
        resolved_waves.append((field, value, identity.wave_uid))

    if _text(expected_wave):
        if not source_uid:
            raise BoundaryContractError("EXPECTED_WAVE_REQUIRES_SOURCE_IDENTITY")
        try:
            expected_identity = resolve_source_wave_identity(
                canonical_source, expected_wave, registry_path=registry_path
            )
        except SourceWaveIdentityError as exc:
            raise BoundaryContractError(
                f"EXPECTED_WAVE_IDENTITY_UNRESOLVED:{expected_wave!r}:source_uid={source_uid}:"
                f"{type(exc).__name__}:{exc}"
            ) from exc
        resolved_waves.append(("<expected_wave>", _text(expected_wave), expected_identity.wave_uid))

    resolved_wave_uids: list[tuple[str, str, str]] = []
    for field, value in wave_uid_rows:
        record = registry.wave_uid_index.get(value)
        if record is None:
            raise BoundaryContractError(f"WAVE_UID_UNKNOWN:{field}={value!r}")
        family = record.get("_family") or {}
        record_source_uid = _text(family.get("source_family_uid"))
        if source_uid and record_source_uid != source_uid:
            raise BoundaryContractError(
                f"WAVE_UID_SOURCE_CONTRADICTION:{field}={value!r}:"
                f"wave_source_uid={record_source_uid}:source_uid={source_uid}"
            )
        resolved_wave_uids.append((field, value, value))
    if _text(expected_wave_uid):
        value = _text(expected_wave_uid)
        record = registry.wave_uid_index.get(value)
        if record is None:
            raise BoundaryContractError(f"EXPECTED_WAVE_UID_UNKNOWN:{value!r}")
        family = record.get("_family") or {}
        record_source_uid = _text(family.get("source_family_uid"))
        if source_uid and record_source_uid != source_uid:
            raise BoundaryContractError(
                "EXPECTED_WAVE_UID_SOURCE_CONTRADICTION:"
                f"wave_uid={value}:wave_source_uid={record_source_uid}:source_uid={source_uid}"
            )
        resolved_wave_uids.append(("<expected_wave_uid>", value, value))

    wave_uid_candidates = {
        uid for _, _, uid in [*resolved_waves, *resolved_wave_uids] if uid
    }
    if len(wave_uid_candidates) > 1:
        summary = _representation_summary([*resolved_waves, *resolved_wave_uids])
        raise BoundaryContractError(f"WAVE_IDENTITY_CONTRADICTION:{summary}")
    wave_uid = next(iter(wave_uid_candidates), "")

    canonical_wave = ""
    if wave_uid:
        record = registry.wave_uid_index[wave_uid]
        family = record.get("_family") or {}
        record_source_uid = _text(family.get("source_family_uid"))
        if source_uid and record_source_uid != source_uid:
            raise BoundaryContractError(
                "SOURCE_WAVE_UID_PAIR_CONTRADICTION:"
                f"source_uid={source_uid}:wave_uid={wave_uid}:wave_source_uid={record_source_uid}"
            )
        if not source_uid:
            source_uid = record_source_uid
            canonical_source = _text(family.get("canonical_display_source"))
        canonical_wave = _text(record.get("canonical_display_wave"))

    if require_complete and (not source_uid or not wave_uid):
        missing = []
        if not source_uid:
            missing.append("source_family_uid")
        if not wave_uid:
            missing.append("wave_uid")
        raise BoundaryContractError(
            "SOURCE_WAVE_IDENTITY_INCOMPLETE:" + ",".join(missing)
        )

    return SourceWaveIdentityCoherence(
        source_family_uid=source_uid,
        wave_uid=wave_uid,
        canonical_display_source=canonical_source,
        canonical_display_wave=canonical_wave,
        source_representations=tuple(source_rows),
        wave_representations=tuple(wave_rows),
        source_uid_representations=tuple(source_uid_rows),
        wave_uid_representations=tuple(wave_uid_rows),
    )


def verify_manifest_source_wave_identity_coherence(
    payload: Mapping[str, Any],
    *,
    expected_source: str = "",
    expected_wave: str = "",
    expected_source_family_uid: str = "",
    expected_wave_uid: str = "",
    registry_path: str | Path | None = None,
) -> SourceWaveIdentityCoherence:
    """Reusable manifest-level UID coherence validation for producer boundaries."""
    return validate_source_wave_identity_coherence(
        payload,
        expected_source=expected_source,
        expected_wave=expected_wave,
        expected_source_family_uid=expected_source_family_uid,
        expected_wave_uid=expected_wave_uid,
        registry_path=registry_path,
        require_complete=True,
    )


def verify_frame_source_wave_identity_coherence(
    frame: pd.DataFrame,
    *,
    expected_source: str = "",
    expected_wave: str = "",
    expected_source_family_uid: str = "",
    expected_wave_uid: str = "",
    registry_path: str | Path | None = None,
    allow_empty: bool = True,
) -> dict[str, Any]:
    """Verify every row and every populated identity representation in a frame."""
    if frame.empty:
        if not allow_empty:
            raise BoundaryContractError("FRAME_SOURCE_WAVE_IDENTITY_EMPTY")
        return {
            "row_count": 0,
            "source_family_uid": _text(expected_source_family_uid),
            "wave_uid": _text(expected_wave_uid),
            "canonical_display_source": "",
            "canonical_display_wave": "",
        }

    pairs: set[tuple[str, str]] = set()
    canonical_sources: set[str] = set()
    canonical_waves: set[str] = set()
    for index, row in frame.iterrows():
        try:
            coherence = validate_source_wave_identity_coherence(
                row.to_dict(),
                expected_source=expected_source,
                expected_wave=expected_wave,
                expected_source_family_uid=expected_source_family_uid,
                expected_wave_uid=expected_wave_uid,
                registry_path=registry_path,
                require_complete=True,
            )
        except BoundaryContractError as exc:
            raise BoundaryContractError(
                f"FRAME_SOURCE_WAVE_IDENTITY_INVALID:row={index}:{exc}"
            ) from exc
        pairs.add((coherence.source_family_uid, coherence.wave_uid))
        canonical_sources.add(coherence.canonical_display_source)
        canonical_waves.add(coherence.canonical_display_wave)
    if len(pairs) != 1:
        raise BoundaryContractError(
            "FRAME_SOURCE_WAVE_UID_SCOPE_MIXED:" + ",".join(
                f"{source_uid}|{wave_uid}" for source_uid, wave_uid in sorted(pairs)
            )
        )
    source_uid, wave_uid = next(iter(pairs))
    return {
        "row_count": int(len(frame)),
        "source_family_uid": source_uid,
        "wave_uid": wave_uid,
        "canonical_display_source": next(iter(canonical_sources), ""),
        "canonical_display_wave": next(iter(canonical_waves), ""),
    }


def _verify_exact_scalar_representations(
    payload: Mapping[str, Any],
    *,
    label: str,
    expected: str,
    fields: Iterable[str],
) -> str:
    if not expected:
        return ""
    rows = _populated_representations(payload, fields)
    if not rows:
        raise BoundaryContractError(f"IDENTITY_FIELD_MISSING:{label}")
    for field, actual in rows:
        if actual != expected:
            raise BoundaryContractError(
                f"IDENTITY_MISMATCH:{label}:field={field}:expected={expected}:actual={actual}"
            )
    return expected


def verify_exact_identity(
    payload: Mapping[str, Any],
    *,
    run_id: str,
    source: str = "",
    wave: str = "",
    country_code: str = "",
    shard_id: str = "",
    source_family_uid: str = "",
    wave_uid: str = "",
) -> dict[str, str]:
    """Verify exact producer scope using UID identity plus independent scalar laws.

    Source/wave labels are ingress/provenance representations.  All populated
    representations must cohere through the W01 kernel; exact machine scope is
    the resulting source_family_uid + wave_uid.  Run, country, and shard checks
    remain independent exact comparisons and are not weakened by alias support.
    """
    resolved: dict[str, str] = {}
    resolved["run_id"] = _verify_exact_scalar_representations(
        payload,
        label="run_id",
        expected=run_id,
        fields=("producer_run_id", "run_id"),
    )

    has_source_wave = any(
        _populated_representations(payload, fields)
        for fields in (
            _SOURCE_REPRESENTATION_FIELDS,
            _WAVE_REPRESENTATION_FIELDS,
            _SOURCE_UID_FIELDS,
            _WAVE_UID_FIELDS,
        )
    )
    if source or wave or source_family_uid or wave_uid or has_source_wave:
        coherence = validate_source_wave_identity_coherence(
            payload,
            expected_source=source,
            expected_wave=wave,
            expected_source_family_uid=source_family_uid,
            expected_wave_uid=wave_uid,
            require_complete=bool(source or wave or source_family_uid or wave_uid),
        )
        if (source or source_family_uid) and not (
            coherence.source_representations or coherence.source_uid_representations
        ):
            raise BoundaryContractError("IDENTITY_FIELD_MISSING:source")
        if (wave or wave_uid) and not (
            coherence.wave_representations or coherence.wave_uid_representations
        ):
            raise BoundaryContractError("IDENTITY_FIELD_MISSING:wave")
        if coherence.source_family_uid:
            resolved["source_family_uid"] = coherence.source_family_uid
            resolved["source"] = source or coherence.canonical_display_source
        if coherence.wave_uid:
            resolved["wave_uid"] = coherence.wave_uid
            resolved["wave"] = wave or coherence.canonical_display_wave

    if country_code:
        resolved["country_code"] = _verify_exact_scalar_representations(
            payload,
            label="country_code",
            expected=country_code,
            fields=("country_code", "country"),
        )
    if shard_id:
        resolved["shard_id"] = _verify_exact_scalar_representations(
            payload,
            label="shard_id",
            expected=shard_id,
            fields=("shard_id",),
        )
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
    source_family_uid: str = "",
    wave_uid: str = "",
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
        payload,
        run_id=run_id,
        source=source,
        wave=wave,
        country_code=country_code,
        shard_id=shard_id,
        source_family_uid=source_family_uid,
        wave_uid=wave_uid,
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
