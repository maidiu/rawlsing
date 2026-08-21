"""Canonical relational Parquet carrier for sealed PRE553 C11 releases."""
from __future__ import annotations

from dataclasses import dataclass, fields
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from typing import Any, Mapping

from rawlsing_next.pre553_c11_integrity import C11InternalRecord, TypedAbsence
from rawlsing_next.pre553_c11_repository import C11LogicalRelease, _make_validated_release
from rawlsing_next.pre553_empirical_objects import AuthorityRef, CanonicalSemanticObject, ExactRef, canonical_json, exact_ref, semantic_hash


class ParquetCarrierError(ValueError):
    pass


RELATION_SPECS = {
    "empirical_universes": "EmpiricalUniverse", "respondent_identities": "RespondentIdentity",
    "question_variable_bindings": "QuestionVariableBinding", "respondent_events": "RespondentEvent",
    "routing_eligibility": "RoutingEligibilityFact", "empirical_coordinates": "EmpiricalCoordinateFact",
    "weight_measure": "WeightMeasureFact", "authority_snapshots": "AuthoritySnapshot",
    "source_universe_relations": "SourceUniverseRelation", "replay_bindings": "__REPLAY_BINDINGS__",
    "replay_manifest": "ReplayManifest",
}


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _encode(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    if isinstance(value, ExactRef):
        return {"__exact_ref__": value.as_dict()}
    if isinstance(value, AuthorityRef):
        return {"__authority_ref__": value.as_dict()}
    if isinstance(value, TypedAbsence):
        return {"__typed_absence__": value.as_dict()}
    if isinstance(value, Mapping):
        return {"__dict__": [[str(k), _encode(v)] for k, v in sorted(value.items())]}
    if isinstance(value, tuple):
        return {"__tuple__": [_encode(v) for v in value]}
    if isinstance(value, list):
        return {"__list__": [_encode(v) for v in value]}
    raise ParquetCarrierError(f"unsupported canonical field type: {type(value).__name__}")


def _decode(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    if "__exact_ref__" in value:
        return exact_ref(value["__exact_ref__"])
    if "__authority_ref__" in value:
        item = value["__authority_ref__"]
        return AuthorityRef(item["authority_id"], item["authority_version"], item["authority_content_hash"])
    if "__typed_absence__" in value:
        item = value["__typed_absence__"]
        return TypedAbsence(item["typed_absence_state"], item.get("detail"))
    if "__dict__" in value:
        return {k: _decode(v) for k, v in value["__dict__"]}
    if "__tuple__" in value:
        return tuple(_decode(v) for v in value["__tuple__"])
    if "__list__" in value:
        return [_decode(v) for v in value["__list__"]]
    return {k: _decode(v) for k, v in value.items()}


def _field_column(name: str, value: Any) -> tuple[str, Any]:
    if value is None or isinstance(value, (str, bool, int, float)):
        return f"field_{name}", value
    return f"field_{name}_json", canonical_json(_encode(value))


def _object_row(obj: Any) -> dict[str, Any]:
    if isinstance(obj, CanonicalSemanticObject):
        row = {"object_family": obj.FAMILY, "object_id": obj.object_id, "content_hash": obj.content_hash,
               "typed_state": obj.typed_state,
               "authority_snapshot_refs_json": canonical_json(_encode(obj.authority_snapshot_refs)),
               "dependency_refs_json": canonical_json(_encode(obj.dependency_refs)),
               "producer_replay_locator_json": canonical_json(_encode(obj.producer_replay_locator_or_reference_root))}
        values = dict(obj.semantic_fields)
    elif isinstance(obj, C11InternalRecord):
        row = {"object_family": obj.RECORD_FAMILY, "object_id": obj.object_id, "content_hash": obj.content_hash}
        values = {f.name: getattr(obj, f.name) for f in fields(obj)}
    else:
        raise ParquetCarrierError(f"unsupported C11 relation object: {type(obj).__name__}")
    for name, value in sorted(values.items()):
        key, column_value = _field_column(name, value)
        row[key] = column_value
    return row


def _logical_digest(rows: list[dict[str, Any]]) -> str:
    return _sha_bytes(canonical_json(rows).encode())


def _row_value(row: Mapping[str, Any], name: str) -> Any:
    direct, encoded = f"field_{name}", f"field_{name}_json"
    if direct in row:
        return row[direct]
    if encoded in row and row[encoded] is not None:
        return _decode(json.loads(row[encoded]))
    raise ParquetCarrierError(f"canonical relation omits required field {name}")


def _class_for_family(family: str) -> type:
    from rawlsing_next import pre553_c11_integrity as integrity
    from rawlsing_next import pre553_empirical_objects as objects
    name = family.split("@", 1)[0]
    cls = getattr(objects, name, None) or getattr(integrity, name, None)
    if cls is None:
        raise ParquetCarrierError(f"unknown canonical C11 relation family {family}")
    return cls


def _object_from_row(row: Mapping[str, Any]) -> Any:
    family, cls = row["object_family"], _class_for_family(row["object_family"])
    if issubclass(cls, CanonicalSemanticObject):
        kwargs = {"typed_state": row["typed_state"],
                  "authority_snapshot_refs": _decode(json.loads(row["authority_snapshot_refs_json"])),
                  "dependency_refs": _decode(json.loads(row["dependency_refs_json"])),
                  "producer_replay_locator_or_reference_root": _decode(json.loads(row["producer_replay_locator_json"]))}
        for key, value in row.items():
            if key.startswith("field_") and key.endswith("_json"):
                kwargs[key[6:-5]] = _decode(json.loads(value))
            elif key.startswith("field_"):
                kwargs[key[6:]] = value
        obj = cls(**kwargs)
    else:
        obj = cls(**{field.name: _row_value(row, field.name) for field in fields(cls)})
    if obj.object_id != row["object_id"] or obj.content_hash != row["content_hash"]:
        raise ParquetCarrierError(f"canonical relation object identity mismatch for {family}")
    return obj


def verify_semantic_release_root(*, identity_row: Mapping[str, Any], replay_row: Mapping[str, Any],
                                manifest: Mapping[str, Any], supplied_source_sha256: str,
                                supplied_release_id: str, supplied_semantic_hash: str) -> tuple[Any, ExactRef, dict[str, Any]]:
    """Derive the I02 release root solely from persisted identity relations."""
    try:
        replay = _object_from_row(replay_row)
        if getattr(replay, "RECORD_FAMILY", None) != "ReplayManifest":
            raise ParquetCarrierError("persisted replay row is not ReplayManifest")
        if replay.ref.object_id != replay_row["object_id"] or replay.ref.content_hash != replay_row["content_hash"]:
            raise ParquetCarrierError("persisted replay-manifest ref identity mismatch")
        source_ref = exact_ref(json.loads(identity_row["source_artifact_ref_json"]))
        identity_ref = json.loads(identity_row["release_ref_json"])
        coverage = json.loads(identity_row["m01_m18_coverage_json"])
        if (identity_ref.get("object_id") != identity_row["release_id"]
                or identity_ref.get("content_hash") != identity_row["semantic_release_hash"]):
            raise ParquetCarrierError("release identity relation ref is internally inconsistent")
        if set(coverage) != {f"M{index:02d}" for index in range(1, 19)}:
            raise ParquetCarrierError("release identity relation does not contain exact M01-M18 coverage")
        derived = semantic_hash({
            "candidate_projection_hash": replay.semantic_projection_hash,
            "replay_manifest_ref": replay.ref.as_dict(),
            "m01_m18": {key: list(value) for key, value in coverage.items()},
        })
        checks = (
            supplied_source_sha256 == source_ref.content_hash == manifest["source_artifact_ref"]["content_hash"],
            supplied_release_id == identity_row["release_id"] == manifest["release_ref"]["object_id"],
            supplied_semantic_hash == identity_row["semantic_release_hash"] == manifest["release_ref"]["content_hash"] == derived,
        )
        if not all(checks):
            raise ParquetCarrierError("persisted semantic release root does not equal supplied/manifest identity")
        return replay, source_ref, coverage
    except ParquetCarrierError:
        raise
    except Exception as exc:
        raise ParquetCarrierError("persisted semantic release root is invalid") from exc


@dataclass(frozen=True)
class PersistentManifest:
    schema_version: str
    release_ref: dict[str, Any]
    source_artifact_ref: dict[str, Any]
    members: dict[str, str]
    relation_digests: dict[str, str]
    manifest_hash: str

    def unsigned(self) -> dict[str, Any]:
        return {"schema_version": self.schema_version, "release_ref": self.release_ref,
                "source_artifact_ref": self.source_artifact_ref, "members": dict(sorted(self.members.items())),
                "relation_digests": dict(sorted(self.relation_digests.items()))}


class ParquetC11Carrier:
    SCHEMA_VERSION = "PRE553_PARQUET_C11_RELATIONAL_CARRIER@2.0.0"

    def __init__(self, root: str | Path):
        self.root = Path(root)

    def release_dir(self, release: C11LogicalRelease) -> Path:
        return self.root / "releases" / release.source_artifact_ref.content_hash / release.release_id / release.semantic_release_hash

    def _relation_objects(self, release: C11LogicalRelease) -> dict[str, list[Any]]:
        result = {name: [] for name in RELATION_SPECS}
        for obj in release.public_objects:
            family = obj.FAMILY.split("@", 1)[0]
            target = {"EmpiricalUniverse": "empirical_universes", "RespondentEvent": "respondent_events",
                      "RoutingEligibilityFact": "routing_eligibility", "EmpiricalCoordinateFact": "empirical_coordinates",
                      "AuthoritySnapshot": "authority_snapshots", "SourceUniverseRelation": "source_universe_relations",
                      "WeightMeasureFact": "weight_measure"}.get(family)
            if target:
                result[target].append(obj)
        for obj in release.internal_records:
            target = {"RespondentIdentity": "respondent_identities", "QuestionVariableBinding": "question_variable_bindings"}.get(obj.RECORD_FAMILY, "replay_bindings")
            result[target].append(obj)
        result["replay_manifest"] = [release.replay_manifest]
        return result

    def _write_tables(self, directory: Path, release: C11LogicalRelease) -> tuple[dict[str, str], dict[str, str]]:
        import pyarrow as pa
        import pyarrow.parquet as pq
        relation_digests, member_hashes = {}, {}
        for relation, objects in self._relation_objects(release).items():
            rows = sorted((_object_row(obj) for obj in objects), key=lambda row: (row.get("object_family", ""), row.get("object_id", "")))
            relation_digests[relation] = _logical_digest(rows)
            path = directory / f"{relation}.parquet"
            pq.write_table(pa.Table.from_pylist(rows) if rows else pa.table({"_empty": pa.array([], type=pa.string())}), path, compression="zstd", compression_level=3)
            member_hashes[path.name] = _sha_file(path)
        identity_rows = [{"release_id": release.release_id, "release_ref_json": canonical_json(release.release_ref.as_dict()),
                          "source_artifact_ref_json": canonical_json(release.source_artifact_ref.as_dict()),
                          "source_release_manifest_hash": release.source_release_manifest_hash,
                          "semantic_release_hash": release.semantic_release_hash,
                          "m01_m18_coverage_json": canonical_json({k: list(v) for k, v in release.m01_m18_coverage.items()})}]
        relation_digests["release_identity"] = _logical_digest(identity_rows)
        path = directory / "release_identity.parquet"
        pq.write_table(pa.Table.from_pylist(identity_rows), path, compression="zstd", compression_level=3)
        member_hashes[path.name] = _sha_file(path)
        return member_hashes, relation_digests

    def persist(self, release: C11LogicalRelease) -> Path:
        if not isinstance(release, C11LogicalRelease):
            raise ParquetCarrierError("only sealed C11LogicalRelease may be persisted")
        target, family_dir = self.release_dir(release), self.release_dir(release).parent
        if family_dir.is_dir() and not target.exists() and any(p.is_dir() for p in family_dir.iterdir()):
            raise ParquetCarrierError("same source/release identity already has a different semantic hash")
        if target.exists():
            existing = self.reopen(release.source_artifact_ref.content_hash, release.release_id, release.semantic_release_hash)
            if existing.release_ref != release.release_ref:
                raise ParquetCarrierError("conflicting same-release identity")
            return target
        self.root.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".staging-", dir=self.root))
        try:
            payload = staging / "release_payload"; payload.mkdir()
            members, relations = self._write_tables(payload, release)
            unsigned = {"schema_version": self.SCHEMA_VERSION, "release_ref": release.release_ref.as_dict(),
                        "source_artifact_ref": release.source_artifact_ref.as_dict(), "members": dict(sorted(members.items())),
                        "relation_digests": dict(sorted(relations.items()))}
            manifest = {**unsigned, "manifest_hash": _sha_bytes(canonical_json(unsigned).encode())}
            (payload / "manifest.json").write_text(canonical_json(manifest) + "\n", encoding="utf-8")
            target.parent.mkdir(parents=True, exist_ok=True); os.replace(payload, target)
            return target
        finally:
            shutil.rmtree(staging, ignore_errors=True)

    def _read_rows(self, directory: Path, relation: str) -> list[dict[str, Any]]:
        import pyarrow.parquet as pq
        return [dict(row) for row in pq.read_table(directory / f"{relation}.parquet").to_pylist() if "_empty" not in row]

    def reopen(self, source_sha256: str, release_id: str, semantic_hash: str) -> C11LogicalRelease:
        if not isinstance(source_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", source_sha256):
            raise ParquetCarrierError("exact source selector must be lowercase 64-hex SHA-256")
        if not isinstance(semantic_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", semantic_hash):
            raise ParquetCarrierError("semantic selector must be lowercase 64-hex SHA-256")
        if not isinstance(release_id, str) or not release_id or release_id in {".", ".."} or any(char in release_id for char in "/\\"):
            raise ParquetCarrierError("release selector is malformed or path-traversing")
        selector = "|".join((source_sha256, release_id, semantic_hash)).lower()
        if any(token in selector for token in ("latest", "fuzzy", "nearest", "default")):
            raise ParquetCarrierError("exact content-addressed release selectors are required")
        directory = self.root / "releases" / source_sha256 / release_id / semantic_hash
        if not directory.is_dir():
            raise ParquetCarrierError("committed release directory unavailable")
        try:
            manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ParquetCarrierError("persistent manifest missing or invalid") from exc
        unsigned = {key: manifest[key] for key in ("schema_version", "release_ref", "source_artifact_ref", "members", "relation_digests")}
        if manifest.get("manifest_hash") != _sha_bytes(canonical_json(unsigned).encode()) or manifest.get("schema_version") != self.SCHEMA_VERSION:
            raise ParquetCarrierError("persistent manifest hash/schema mismatch")
        for member, digest in manifest["members"].items():
            path = directory / member
            if not path.is_file() or _sha_file(path) != digest:
                raise ParquetCarrierError(f"missing or corrupt Parquet member: {member}")
        relations = {name: self._read_rows(directory, name) for name in (*RELATION_SPECS, "release_identity")}
        for name, rows in relations.items():
            if _logical_digest(rows) != manifest["relation_digests"].get(name):
                raise ParquetCarrierError(f"canonical relation digest mismatch: {name}")
        identity = relations["release_identity"]
        replay_rows = relations["replay_manifest"]
        if len(identity) != 1 or len(replay_rows) != 1:
            raise ParquetCarrierError("release identity relation cardinality mismatch")
        replay, source_ref, coverage = verify_semantic_release_root(
            identity_row=identity[0], replay_row=replay_rows[0], manifest=manifest,
            supplied_source_sha256=source_sha256, supplied_release_id=release_id,
            supplied_semantic_hash=semantic_hash,
        )
        objects = []
        try:
            for name in RELATION_SPECS:
                objects.extend(_object_from_row(row) for row in relations[name])
        except Exception as exc:
            if isinstance(exc, ParquetCarrierError):
                raise
            raise ParquetCarrierError("canonical relation semantics are invalid") from exc
        replay_objects = [obj for obj in objects if getattr(obj, "RECORD_FAMILY", None) == "ReplayManifest"]
        if len(replay_objects) != 1 or replay_objects[0].ref != replay.ref:
            raise ParquetCarrierError("replay manifest relation reconstruction mismatch")
        public = tuple(sorted((obj for obj in objects if isinstance(obj, CanonicalSemanticObject)), key=lambda obj: obj.ref.key))
        internal = tuple(sorted((obj for obj in objects if isinstance(obj, C11InternalRecord)
                                 and getattr(obj, "RECORD_FAMILY", None) != "ReplayManifest"), key=lambda obj: obj.ref.key))
        row = identity[0]
        try:
            release = _make_validated_release(
                release_id=row["release_id"], source_artifact_ref=source_ref,
                source_release_manifest_hash=row["source_release_manifest_hash"], semantic_release_hash=row["semantic_release_hash"],
                replay_manifest=replay, public_objects=public, internal_records=internal,
                m01_m18_coverage={key: tuple(value) for key, value in coverage.items()},
            )
        except Exception as exc:
            raise ParquetCarrierError("canonical relations cannot reconstruct sealed C11 release") from exc
        if (release.source_artifact_ref.content_hash != source_sha256
                or release.source_artifact_ref.content_hash != manifest["source_artifact_ref"]["content_hash"]
                or release.release_id != release_id
                or manifest["release_ref"].get("object_id") != release_id
                or release.semantic_release_hash != semantic_hash
                or manifest["release_ref"].get("content_hash") != semantic_hash):
            raise ParquetCarrierError("supplied selectors do not equal reconstructed/manifest identity")
        canonical_directory = self.root / "releases" / release.source_artifact_ref.content_hash / release.release_id / release.semantic_release_hash
        if canonical_directory.resolve() != directory.resolve():
            raise ParquetCarrierError("opened path is not the reconstructed content-addressed path")
        if release.release_ref.as_dict() != manifest["release_ref"] or release.source_artifact_ref.as_dict() != manifest["source_artifact_ref"]:
            raise ParquetCarrierError("canonical relation semantics conflict with manifest identity")
        closure = set(replay.closure_refs) | set(replay.source_substrate_content_refs)
        persisted_refs = {obj.ref for obj in (*release.public_objects, *release.internal_records)} | {release.source_artifact_ref}
        if not persisted_refs.issubset(closure):
            raise ParquetCarrierError("canonical persisted object/source ref is absent from replay closure")
        return release


__all__ = ["ParquetCarrierError", "PersistentManifest", "ParquetC11Carrier", "RELATION_SPECS", "verify_semantic_release_root"]
