"""Relation-first C11 execution primitives.

This module is deliberately an execution layer.  It does not introduce a
second semantic model: object rows are produced with the existing
``_object_row`` encoder and are checked with the existing object constructors
when an exact object is requested.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import pickle
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

from rawlsing_next.pre553_empirical_objects import AuthorityRef, CanonicalSemanticObject, ExactRef, canonical_json
from rawlsing_next.pre553_parquet_carrier import (
    RELATION_SPECS, _object_from_row, _sha_file, _class_for_family,
)


_RELATION_FAMILY = {name: family for name, family in RELATION_SPECS.items()
                    if family != "__REPLAY_BINDINGS__"}


def _digest_row(row: Mapping[str, Any]) -> str:
    material = {key: ({"__bytes_hex__": value.hex()} if isinstance(value, bytes) else value)
                for key, value in row.items()}
    return canonical_json(material)


class _CompactDictionary:
    def __init__(self) -> None:
        self.values: dict[str, list[Any]] = {"s": [], "e": [], "a": []}
        self.index: dict[str, dict[str, int]] = {"s": {}, "e": {}, "a": {}}

    def key(self, kind: str, value: Any) -> int:
        material = canonical_json(value.as_dict() if hasattr(value, "as_dict") else value)
        existing = self.index[kind].get(material)
        if existing is not None:
            return existing
        number = len(self.values[kind]); self.index[kind][material] = number; self.values[kind].append(value)
        return number

    def rows(self, relation: str) -> list[dict[str, Any]]:
        rows = []
        for kind, values in self.values.items():
            for key, value in enumerate(values):
                rows.append({"relation": relation, "kind": kind, "key": key,
                             "value_json": canonical_json(value.as_dict() if hasattr(value, "as_dict") else value)})
        return rows


def _compact_payload(obj: Any, relation: str, dictionary: _CompactDictionary) -> bytes:
    """Encode semantic constructor inputs only; identity is always recomputed."""
    def plain(value: Any) -> Any:
        if isinstance(value, ExactRef):
            return ("e", dictionary.key("e", value))
        if isinstance(value, AuthorityRef):
            return ("a", dictionary.key("a", value))
        if isinstance(value, str):
            return ("s", dictionary.key("s", value))
        if isinstance(value, Mapping):
            return {key: plain(value[key]) for key in sorted(value)}
        if isinstance(value, tuple):
            return tuple(plain(item) for item in value)
        if isinstance(value, list):
            return [plain(item) for item in value]
        return value
    if isinstance(obj, CanonicalSemanticObject):
        material = ("public", obj.typed_state, plain(obj.authority_snapshot_refs),
                    plain(obj.dependency_refs), plain(obj.producer_replay_locator_or_reference_root),
                    plain(dict(obj.semantic_fields)))
    else:
        from dataclasses import fields
        material = ("internal", getattr(obj, "RECORD_FAMILY", ""),
                    plain({field.name: getattr(obj, field.name) for field in fields(obj)}))
    return pickle.dumps(material, protocol=5)


def _compact_row(obj: Any, relation: str, dictionary: _CompactDictionary) -> dict[str, Any]:
    row: dict[str, Any] = {"compact_payload": _compact_payload(obj, relation, dictionary)}
    if relation == "respondent_events":
        row["typed_state"] = obj.typed_state
        row["response_state"] = obj.response_state
        row["event_id"] = str(obj.response_event_id_or_deterministic_index)
    return row


def _compact_object_from_row(row: Mapping[str, Any], relation: str, dictionary: _CompactDictionary | None = None) -> Any:
    """Decode one compact row and invoke the existing semantic constructor."""
    if "compact_payload" not in row:
        return _object_from_row(row)
    material = pickle.loads(bytes(row["compact_payload"]))
    if dictionary is None:
        raise ValueError("compact row dictionary is required for exact reconstruction")
    def restore(value: Any) -> Any:
        if isinstance(value, tuple) and len(value) == 2 and value[0] in {"s", "e", "a"}:
            return dictionary.values[value[0]][value[1]]
        if isinstance(value, Mapping):
            return {key: restore(item) for key, item in value.items()}
        if isinstance(value, tuple):
            return tuple(restore(item) for item in value)
        if isinstance(value, list):
            return [restore(item) for item in value]
        return value
    material = restore(material)
    if material[0] == "public":
        family = _RELATION_FAMILY.get(relation)
        if family is None:
            raise ValueError(f"compact relation family is not fixed: {relation}")
        cls = _class_for_family(family)
        _, typed_state, authority_refs, dependency_refs, producer_root, semantic_fields = material
        obj = cls(typed_state=typed_state, authority_snapshot_refs=authority_refs,
                   dependency_refs=dependency_refs,
                   producer_replay_locator_or_reference_root=producer_root,
                   **semantic_fields)
    else:
        _, object_family, fields_material = material
        cls = _class_for_family(object_family)
        obj = cls(**fields_material)
    return obj


def _digest_rows(rows: Iterable[Mapping[str, Any]]) -> str:
    """Hash canonical rows without retaining the relation in memory."""
    digest = hashlib.sha256()
    digest.update(b"[")
    first = True
    for row in rows:
        if not first:
            digest.update(b",")
        first = False
        digest.update(_digest_row(dict(row)).encode("utf-8"))
    digest.update(b"]")
    return digest.hexdigest()


def _iter_parquet_rows(path: Path, *, batch_size: int = 8192) -> Iterator[dict[str, Any]]:
    import pyarrow.parquet as pq
    for batch in pq.ParquetFile(path).iter_batches(batch_size=batch_size):
        for row in batch.to_pylist():
            if "_empty" not in row:
                yield dict(row)


def read_compact_dictionary(path: str | Path) -> _CompactDictionary:
    import pyarrow.parquet as pq
    dictionary = _CompactDictionary()
    for row in pq.read_table(path).to_pylist():
        kind, key, value = row["kind"], int(row["key"]), json.loads(row["value_json"])
        if kind in {"e", "a"}:
            value = ExactRef(**value) if kind == "e" else AuthorityRef(
                value["authority_id"], value["authority_version"], value["authority_content_hash"])
        while len(dictionary.values[kind]) <= key:
            dictionary.values[kind].append(None)
        dictionary.values[kind][key] = value
    return dictionary


@dataclass(frozen=True)
class RelationMember:
    name: str
    path: Path
    logical_digest: str
    byte_sha256: str
    row_count: int


@dataclass(frozen=True)
class RelationC11ReleaseHandle:
    """Small exact release identity; opening it never reconstructs all objects."""

    release_directory: Path
    source_artifact_ref: ExactRef
    release_ref: ExactRef
    replay_manifest_ref: ExactRef
    m01_m18_coverage: Mapping[str, tuple[str, ...]]
    members: Mapping[str, RelationMember]
    relation_digests: Mapping[str, str]
    dictionaries: Mapping[str, _CompactDictionary] | None = None

    @property
    def semantic_release_hash(self) -> str:
        return self.release_ref.content_hash

    def resolve_object_exact(self, ref: ExactRef) -> Any:
        """Reconstruct only the exact requested row."""
        key = ref.key
        for member in self.members.values():
            if (not member.name.endswith(".parquet") or member.name == "release_identity.parquet"
                    or member.name.endswith(".dictionary.parquet")):
                continue
            for row in _iter_parquet_rows(member.path):
                relation = member.name[:-8]
                obj = _compact_object_from_row(row, relation, (self.dictionaries or {}).get(relation))
                if obj.ref.key == key:
                    return obj
        raise KeyError("exact relation-backed object unavailable; no fallback permitted")

    def audit(self) -> dict[str, Any]:
        """Stream rows and verify every persisted row's deterministic identity."""
        counts: dict[str, int] = {}
        digests: dict[str, str] = {}
        for name, member in self.members.items():
            if (not name.endswith(".parquet") or name == "release_identity.parquet"
                    or name.endswith(".dictionary.parquet")):
                continue
            rows = _iter_parquet_rows(member.path)
            count = 0
            digest = hashlib.sha256(); digest.update(b"[")
            first = True
            for row in rows:
                _compact_object_from_row(row, name[:-8], (self.dictionaries or {}).get(name[:-8]))
                if not first:
                    digest.update(b",")
                first = False
                digest.update(_digest_row(row).encode("utf-8"))
                count += 1
            relation = name[:-8]
            counts[relation] = count
            digest.update(b"]")
            digests[relation] = digest.hexdigest()
            if digests[relation] != self.relation_digests.get(relation):
                raise ValueError(f"relation digest mismatch: {relation}")
        return {"row_counts": counts, "relation_digests": digests}


class RelationFirstParquetWriter:
    """Incremental Parquet publisher for homogeneous canonical relation batches."""

    def __init__(self, directory: str | Path, *, row_group_size: int = 4096,
                 compression_level: int = 3):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.row_group_size = row_group_size
        self.compression_level = compression_level
        self._writers: dict[str, Any] = {}
        self._schemas: dict[str, Any] = {}
        self._digests: dict[str, hashlib._Hash] = {}
        self._counts: dict[str, int] = {}
        self._dictionaries: dict[str, _CompactDictionary] = {}

    def append(self, relation: str, objects: Iterable[Any]) -> int:
        if relation not in RELATION_SPECS:
            raise ValueError(f"unknown C11 relation: {relation}")
        import pyarrow as pa
        import pyarrow.parquet as pq
        dictionary = self._dictionaries.setdefault(relation, _CompactDictionary())
        rows = [_compact_row(obj, relation, dictionary) for obj in objects]
        if not rows:
            return 0
        table = pa.Table.from_pylist(rows)
        writer = self._writers.get(relation)
        if writer is None:
            path = self.directory / f"{relation}.parquet"
            writer = pq.ParquetWriter(path, table.schema, compression="zstd", compression_level=self.compression_level,
                                      use_dictionary=True)
            self._writers[relation] = writer
            self._schemas[relation] = table.schema
            digest = hashlib.sha256(); digest.update(b"["); self._digests[relation] = digest
        elif table.schema != self._schemas[relation]:
            raise ValueError(f"relation {relation} changed canonical schema across batches")
        writer.write_table(table, row_group_size=self.row_group_size)
        digest = self._digests[relation]
        for row in rows:
            if self._counts.get(relation, 0):
                digest.update(b",")
            digest.update(_digest_row(row).encode("utf-8"))
            self._counts[relation] = self._counts.get(relation, 0) + 1
        return len(rows)

    def close(self) -> dict[str, RelationMember]:
        for writer in self._writers.values():
            writer.close()
        for digest in self._digests.values():
            digest.update(b"]")
        import pyarrow as pa
        import pyarrow.parquet as pq
        for relation, dictionary in self._dictionaries.items():
            if not any(dictionary.values.values()):
                continue
            path = self.directory / f"{relation}.dictionary.parquet"
            pq.write_table(pa.Table.from_pylist(dictionary.rows(relation)), path, compression="zstd",
                           compression_level=self.compression_level)
        members = {
            relation: RelationMember(
                name=f"{relation}.parquet", path=self.directory / f"{relation}.parquet",
                logical_digest=self._digests[relation].hexdigest(),
                byte_sha256=_sha_file(self.directory / f"{relation}.parquet"),
                row_count=self._counts[relation],
            ) for relation in self._writers
        }
        for relation, dictionary in self._dictionaries.items():
            if not any(dictionary.values.values()):
                continue
            path = self.directory / f"{relation}.dictionary.parquet"
            members[f"{relation}.dictionary.parquet"] = RelationMember(
                name=path.name, path=path,
                logical_digest=_digest_rows(_iter_parquet_rows(path)),
                byte_sha256=_sha_file(path),
                row_count=sum(1 for _ in _iter_parquet_rows(path)),
            )
        return members

    @property
    def dictionaries(self) -> Mapping[str, _CompactDictionary]:
        return self._dictionaries


def stream_relation_rows(path: str | Path, *, batch_size: int = 8192) -> Iterator[dict[str, Any]]:
    """Public bounded iterator for direct relational consumers."""
    yield from _iter_parquet_rows(Path(path), batch_size=batch_size)


def storage_budget(members: Mapping[str, RelationMember], *, fixed_metadata_bytes: int,
                   atomic_staging_peak_bytes: int, scratch_execution_peak_bytes: int,
                   nonauthoritative_cache_bytes: int = 0,
                   respondent_event_count: int = 0) -> dict[str, Any]:
    """Return the Authority-44 storage receipt from measured carrier members."""
    by_member = {member.name: member.path.stat().st_size for member in members.values()}
    canonical = fixed_metadata_bytes + sum(by_member.values())
    event_bytes = by_member.get("respondent_events.parquet", 0)
    return {
        "CANONICAL_STEADY_STATE_BYTES": canonical,
        "BY_CANONICAL_RELATION_MEMBER_BYTES": by_member,
        "FIXED_PER_RELEASE_METADATA_BYTES": fixed_metadata_bytes,
        "EVENT_BEARING_RELATION_BYTES": event_bytes,
        "CANONICAL_BYTES_PER_RESPONDENT_EVENT": (event_bytes / respondent_event_count
                                                  if respondent_event_count else None),
        "ATOMIC_STAGING_PEAK_BYTES": atomic_staging_peak_bytes,
        "SCRATCH_EXECUTION_PEAK_BYTES": scratch_execution_peak_bytes,
        "NONAUTHORITATIVE_CACHE_BYTES": nonauthoritative_cache_bytes,
        "POST_SUCCESS_RETAINED_BYTES": canonical,
        "ZSTD_CONFIGURATION": {"compression": "zstd", "compression_level": 3,
                                "use_dictionary": True},
        "ROW_GROUP_CONFIGURATION": {"target_rows": 4096},
        "SOURCE_VARIABLE_METADATA_NORMALIZED": True,
        "SOURCE_VARIABLE_METADATA_PROOF": (
            "Respondent-event rows retain exact source/question/topology refs and raw values; "
            "source-variable labels, dictionaries, declarations and topology metadata are "
            "stored in governing source-substrate relations, never copied into each event row."
        ),
    }


def projection_only_storage(*, fixed_metadata_bytes: int, bytes_per_event: float,
                            event_count: int, corpus: str) -> dict[str, Any]:
    """Corrected fixed-plus-event projection; never uses wide-object P1 bytes."""
    projected_event_bytes = bytes_per_event * event_count
    total = fixed_metadata_bytes + projected_event_bytes
    return {"corpus": corpus, "basis": "MEASURED_CORRECTED_RELATION_BYTES_PER_EVENT",
            "status": "PROJECTION_ONLY", "physical_cells": event_count,
            "fixed_metadata_bytes": fixed_metadata_bytes,
            "event_scaled_bytes": projected_event_bytes,
            "steady_state_bytes": total,
            "bytes_per_event": bytes_per_event}


def open_relation_handle(carrier: Any, *, source_sha256: str, release_id: str,
                         semantic_hash: str) -> RelationC11ReleaseHandle:
    """Open only the exact manifest/identity root of a published carrier."""
    import json
    directory = Path(carrier.root) / "releases" / source_sha256 / release_id / semantic_hash
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("release_ref", {}).get("object_id") != release_id or manifest.get("release_ref", {}).get("content_hash") != semantic_hash:
        raise ValueError("relation handle selector does not match manifest")
    import pyarrow.parquet as pq
    identity = pq.read_table(directory / "release_identity.parquet", columns=[
        "release_ref_json", "source_artifact_ref_json", "m01_m18_coverage_json"]).to_pylist()
    dictionaries = {}
    for path in directory.glob("*.dictionary.parquet"):
        dictionaries[path.name[:-len(".dictionary.parquet")]] = read_compact_dictionary(path)
    replay = list(_iter_parquet_rows(directory / "replay_manifest.parquet"))
    if len(identity) != 1 or len(replay) != 1:
        raise ValueError("relation handle identity cardinality mismatch")
    identity_row, replay_row = identity[0], replay[0]
    source_ref = ExactRef(**json.loads(identity_row["source_artifact_ref_json"]))
    release_ref = ExactRef(**json.loads(identity_row["release_ref_json"]))
    replay_obj = _compact_object_from_row(replay_row, "replay_manifest", dictionaries.get("replay_manifest"))
    replay_ref = replay_obj.ref
    members = {}
    for name, byte_hash in manifest["members"].items():
        path = directory / name
        if not path.is_file() or _sha_file(path) != byte_hash:
            raise ValueError(f"missing or corrupt relation member: {name}")
        if (name.endswith(".parquet") and name != "release_identity.parquet"
                and not name.endswith(".dictionary.parquet")):
            relation = name[:-8]
            rows = _iter_parquet_rows(path)
            digest = _digest_rows(rows)
            members[name] = RelationMember(name, path, digest, byte_hash, sum(1 for _ in _iter_parquet_rows(path)))
        else:
            members[name] = RelationMember(name, path, manifest["relation_digests"].get(name[:-8], ""), byte_hash, 1)
    coverage = json.loads(identity_row["m01_m18_coverage_json"])
    return RelationC11ReleaseHandle(directory, source_ref, release_ref, replay_ref,
                                    {key: tuple(value) for key, value in coverage.items()},
                                    members, manifest["relation_digests"], dictionaries)


def query_relation_handle(handle: RelationC11ReleaseHandle, sql: str) -> list[tuple[Any, ...]]:
    """Run direct DuckDB SQL over a verified lightweight handle."""
    if ".duckdb" in sql.lower() or "database_url" in sql.lower() or "sqlite" in sql.lower():
        raise ValueError("file-backed/database-url authority paths are forbidden")
    import duckdb
    connection = duckdb.connect(database=":memory:")
    try:
        for name in handle.members:
            if not name.endswith(".parquet") or name.endswith(".dictionary.parquet"):
                continue
            path = str(handle.release_directory / name).replace("'", "''")
            connection.execute(f"CREATE VIEW {name[:-8]} AS SELECT * FROM read_parquet('{path}')")
        return [tuple(row) for row in connection.execute(sql).fetchall()]
    finally:
        connection.close()


__all__ = [
    "RelationC11ReleaseHandle", "RelationFirstParquetWriter", "RelationMember",
    "open_relation_handle", "projection_only_storage", "query_relation_handle",
    "storage_budget", "stream_relation_rows", "read_compact_dictionary",
]
