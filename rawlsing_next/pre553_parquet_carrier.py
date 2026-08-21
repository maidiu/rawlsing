"""Immutable content-addressed Parquet carrier for sealed C11 releases."""
from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
import base64
import hashlib
import json
import os
from pathlib import Path
import importlib
import shutil
import tempfile
from typing import Any

from rawlsing_next.pre553_c11_repository import C11LogicalRelease, _make_validated_release
from rawlsing_next.pre553_empirical_objects import AuthorityRef, CanonicalSemanticObject, ExactRef, canonical_json


class ParquetCarrierError(ValueError):
    pass


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _json(value: Any) -> str:
    return canonical_json(value)


def _encode(value: Any) -> Any:
    """Stable tagged representation; avoids pickle/mappingproxy dependence."""
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    if isinstance(value, (ExactRef, AuthorityRef)):
        return {"__ref__": value.__class__.__name__, **value.as_dict()}
    if isinstance(value, dict):
        return {"__dict__": [[str(k), _encode(v)] for k, v in sorted(value.items())]}
    if hasattr(value, "items") and value.__class__.__name__ == "mappingproxy":
        return {"__dict__": [[str(k), _encode(v)] for k, v in sorted(value.items())]}
    if isinstance(value, tuple):
        return {"__tuple__": [_encode(v) for v in value]}
    if isinstance(value, CanonicalSemanticObject):
        return {"__semantic_object__": [value.__class__.__module__, value.__class__.__qualname__],
                "typed_state": _encode(value.typed_state),
                "authority_snapshot_refs": _encode(value.authority_snapshot_refs),
                "dependency_refs": _encode(value.dependency_refs),
                "producer_replay_locator_or_reference_root": _encode(value.producer_replay_locator_or_reference_root),
                "semantic_fields": _encode(dict(value.semantic_fields))}
    if is_dataclass(value):
        return {"__dataclass__": [value.__class__.__module__, value.__class__.__qualname__],
                "fields": {f.name: _encode(getattr(value, f.name)) for f in fields(value)
                            if f.name != "_validation_seal"}}
    if hasattr(value, "value") and value.__class__.__module__ == "enum":
        return {"__enum__": [value.__class__.__module__, value.__class__.__qualname__, value.value]}
    raise ParquetCarrierError(f"unsupported release value type: {type(value).__name__}")


def _class_for(module_name: str, qualname: str) -> type:
    result: Any = importlib.import_module(module_name)
    for part in qualname.split("."):
        result = getattr(result, part)
    return result


def _decode(value: Any) -> Any:
    if isinstance(value, list):
        return [_decode(v) for v in value]
    if not isinstance(value, dict):
        return value
    if "__ref__" in value:
        cls = ExactRef if value["__ref__"] == "ExactRef" else AuthorityRef
        return cls(value["kind"], value["object_id"], value["content_hash"]) if cls is ExactRef else cls(
            value["authority_id"], value["authority_version"], value["authority_content_hash"])
    if "__dict__" in value:
        return {k: _decode(v) for k, v in value["__dict__"]}
    if "__tuple__" in value:
        return tuple(_decode(v) for v in value["__tuple__"])
    if "__semantic_object__" in value:
        cls = _class_for(*value["__semantic_object__"])
        return cls(typed_state=_decode(value["typed_state"]),
                   authority_snapshot_refs=_decode(value["authority_snapshot_refs"]),
                   dependency_refs=_decode(value["dependency_refs"]),
                   producer_replay_locator_or_reference_root=_decode(
                       value["producer_replay_locator_or_reference_root"]),
                   **_decode(value["semantic_fields"]))
    if "__dataclass__" in value:
        cls = _class_for(*value["__dataclass__"])
        kwargs = {k: _decode(v) for k, v in value["fields"].items()}
        if cls is C11LogicalRelease:
            return _make_validated_release(**kwargs)
        return cls(**kwargs)
    return {k: _decode(v) for k, v in value.items()}


@dataclass(frozen=True)
class PersistentManifest:
    schema_version: str
    release_ref: dict[str, Any]
    source_artifact_ref: dict[str, Any]
    members: dict[str, str]
    member_rows: dict[str, int]
    manifest_hash: str

    def unsigned(self) -> dict[str, Any]:
        return {"schema_version": self.schema_version, "release_ref": self.release_ref,
                "source_artifact_ref": self.source_artifact_ref, "members": dict(sorted(self.members.items())),
                "member_rows": dict(sorted(self.member_rows.items()))}

    def as_dict(self) -> dict[str, Any]:
        return {**self.unsigned(), "manifest_hash": self.manifest_hash}


class ParquetC11Carrier:
    """Parquet-only persistence.  DuckDB is never opened by this class."""

    SCHEMA_VERSION = "PRE553_PARQUET_C11_CARRIER@1.0.0"
    MEMBERS = ("release.parquet", "objects.parquet")

    def __init__(self, root: str | Path):
        self.root = Path(root)

    def release_dir(self, release: C11LogicalRelease) -> Path:
        return self.root / "releases" / release.source_artifact_ref.content_hash / release.release_id / release.semantic_release_hash

    def _write_tables(self, directory: Path, release: C11LogicalRelease) -> dict[str, int]:
        import pyarrow as pa
        import pyarrow.parquet as pq
        release_blob = base64.b64encode(_json(_encode(release)).encode()).decode("ascii")
        release_rows = [{"release_id": release.release_id, "release_ref": _json(release.release_ref.as_dict()),
                         "source_artifact_ref": _json(release.source_artifact_ref.as_dict()),
                         "source_release_manifest_hash": release.source_release_manifest_hash,
                         "semantic_release_hash": release.semantic_release_hash,
                         "replay_manifest_ref": _json(release.replay_manifest.ref.as_dict()),
                         "m01_m18_coverage": _json({k: list(v) for k, v in release.m01_m18_coverage.items()}),
                         "release_pickle_b64": release_blob}]
        objects = []
        for obj in (*release.public_objects, *release.internal_records, release.replay_manifest):
            objects.append({"ref": _json(obj.ref.as_dict()), "family": obj.ref.kind,
                            "content_hash": obj.ref.content_hash,
                            "object_pickle_b64": base64.b64encode(_json(_encode(obj)).encode()).decode("ascii")})
        pq.write_table(pa.Table.from_pylist(release_rows), directory / "release.parquet", compression="zstd", compression_level=3)
        pq.write_table(pa.Table.from_pylist(objects), directory / "objects.parquet", compression="zstd", compression_level=3)
        return {"release.parquet": len(release_rows), "objects.parquet": len(objects)}

    def persist(self, release: C11LogicalRelease) -> Path:
        if not isinstance(release, C11LogicalRelease):
            raise ParquetCarrierError("only sealed C11LogicalRelease may be persisted")
        target = self.release_dir(release)
        release_family_dir = target.parent
        if release_family_dir.is_dir():
            prior_dirs = [p for p in release_family_dir.iterdir() if p.is_dir() and not p.name.startswith(".staging-")]
            if prior_dirs and not target.exists():
                raise ParquetCarrierError("same source/release identity already has a different semantic hash")
        if target.exists():
            existing = self.reopen(release.source_artifact_ref.content_hash, release.release_id, release.semantic_release_hash)
            if existing.release_ref != release.release_ref:
                raise ParquetCarrierError("conflicting same-release identity")
            return target
        self.root.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".staging-", dir=self.root))
        try:
            staged_release = staging / "release_payload"
            staged_release.mkdir()
            rows = self._write_tables(staged_release, release)
            members = {name: _sha_file(staged_release / name) for name in self.MEMBERS}
            unsigned = {"schema_version": self.SCHEMA_VERSION, "release_ref": release.release_ref.as_dict(),
                        "source_artifact_ref": release.source_artifact_ref.as_dict(), "members": dict(sorted(members.items())),
                        "member_rows": dict(sorted(rows.items()))}
            manifest_hash = _sha_bytes(_json(unsigned).encode())
            manifest = {**unsigned, "manifest_hash": manifest_hash}
            (staged_release / "manifest.json").write_text(_json(manifest) + "\n", encoding="utf-8")
            for path in (staged_release / "release.parquet", staged_release / "objects.parquet", staged_release / "manifest.json"):
                with path.open("rb") as f: os.fsync(f.fileno())
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(staged_release, target)
            return target
        finally:
            shutil.rmtree(staging, ignore_errors=True)

    def reopen(self, source_sha256: str, release_id: str, semantic_hash: str) -> C11LogicalRelease:
        selector_text = "|".join((source_sha256, release_id, semantic_hash)).lower()
        if any(token in selector_text for token in ("latest", "fuzzy", "nearest", "default")):
            raise ParquetCarrierError("exact content-addressed release selectors are required")
        directory = self.root / "releases" / source_sha256 / release_id / semantic_hash
        if not directory.is_dir() or any(p.name.startswith(".staging-") for p in self.root.glob(".staging-*")):
            raise ParquetCarrierError("committed release directory unavailable")
        manifest_path = directory / "manifest.json"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ParquetCarrierError("persistent manifest missing or invalid") from exc
        unsigned = {k: manifest[k] for k in ("schema_version", "release_ref", "source_artifact_ref", "members", "member_rows")}
        if manifest.get("manifest_hash") != _sha_bytes(_json(unsigned).encode()):
            raise ParquetCarrierError("persistent manifest hash mismatch")
        if manifest["schema_version"] != self.SCHEMA_VERSION or set(manifest["members"]) != set(self.MEMBERS):
            raise ParquetCarrierError("persistent manifest schema/member mismatch")
        for name in self.MEMBERS:
            path = directory / name
            if not path.is_file() or _sha_file(path) != manifest["members"][name]:
                raise ParquetCarrierError(f"missing or corrupt Parquet member: {name}")
        try:
            import pyarrow.parquet as pq
            table = pq.read_table(directory / "release.parquet")
            if table.num_rows != 1:
                raise ParquetCarrierError("release member row count mismatch")
            objects_table = pq.read_table(directory / "objects.parquet")
            if objects_table.num_rows != int(manifest["member_rows"]["objects.parquet"]):
                raise ParquetCarrierError("objects member row count mismatch")
            blob = table.column("release_pickle_b64")[0].as_py()
            release = _decode(json.loads(base64.b64decode(blob).decode()))
        except ParquetCarrierError:
            raise
        except Exception as exc:
            raise ParquetCarrierError("release member unreadable") from exc
        if not isinstance(release, C11LogicalRelease) or release.release_ref.as_dict() != manifest["release_ref"]:
            raise ParquetCarrierError("release identity mismatch")
        return release


__all__ = ["ParquetCarrierError", "PersistentManifest", "ParquetC11Carrier"]
