"""Typed, normalized execution storage for the frozen C11 RespondentEvent.

The physical keys in this module are release-local join keys.  They are
derived from canonical reference bytes and are never exposed as semantic
object identities.  The logical object is rebuilt with the existing
``RespondentEvent`` constructor.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, RespondentEvent, canonical_json


def _ref_dict(value: Any) -> dict[str, str] | None:
    if isinstance(value, ExactRef):
        return value.as_dict()
    if isinstance(value, Mapping) and set(value) == {"kind", "object_id", "content_hash"}:
        return {key: str(value[key]) for key in ("kind", "object_id", "content_hash")}
    return None


def _authority_dict(value: Any) -> dict[str, str] | None:
    if isinstance(value, AuthorityRef):
        return value.as_dict()
    if isinstance(value, Mapping) and set(value) == {"authority_id", "authority_version", "authority_content_hash"}:
        return {key: str(value[key]) for key in ("authority_id", "authority_version", "authority_content_hash")}
    return None


def _key(material: Mapping[str, Any]) -> int:
    """Deterministic unsigned local key; collision checks remain mandatory."""
    digest = hashlib.sha256(canonical_json(material).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def _hash_bytes(value: str) -> bytes:
    return bytes.fromhex(value)


def _value_parts(value: Any) -> tuple[str, str | None, int | None, float | None, bool | None]:
    if value is None:
        return "NULL", None, None, None, None
    if isinstance(value, bool):
        return "BOOL", None, None, None, value
    if isinstance(value, int):
        return "INT64", None, value, None, None
    if isinstance(value, float):
        return "FLOAT64", None, None, value, None
    if isinstance(value, str):
        return "UTF8", value, None, None, None
    return "JSON", canonical_json(value), None, None, None


def _value_from_parts(kind: str, text: str | None, integer: int | None,
                      real: float | None, boolean: bool | None) -> Any:
    if kind == "NULL":
        return None
    if kind == "BOOL":
        return boolean
    if kind == "INT64":
        return integer
    if kind == "FLOAT64":
        return real
    if kind == "UTF8":
        return text
    if kind == "JSON":
        return json.loads(text)
    raise ValueError(f"unknown normalized value kind: {kind}")


@dataclass(frozen=True)
class NormalizedMember:
    name: str
    path: Path
    row_count: int
    bytes: int


class _Dimension:
    def __init__(self, name: str) -> None:
        self.name = name
        self.rows: dict[int, dict[str, Any]] = {}

    def add(self, value: Mapping[str, Any]) -> int:
        local = _key(value)
        existing = self.rows.get(local)
        if existing is not None and existing != dict(value):
            raise ValueError(f"deterministic local-key collision in {self.name}: {local}")
        self.rows[local] = dict(value)
        return local


def _ref_row(value: Mapping[str, Any]) -> dict[str, Any]:
    return {"local_key": _key(value), "kind": value["kind"],
            "object_id": value["object_id"], "content_hash": _hash_bytes(value["content_hash"])}


def _authority_row(value: Mapping[str, Any]) -> dict[str, Any]:
    return {"local_key": _key(value), "authority_id": value["authority_id"],
            "authority_version": value["authority_version"],
            "authority_content_hash": _hash_bytes(value["authority_content_hash"])}


class NormalizedRespondentEventWriter:
    """Append-only typed writer for normalized RespondentEvent storage."""

    def __init__(self, directory: str | Path, *, row_group_size: int = 4096,
                 compression_level: int = 3) -> None:
        self.directory = Path(directory); self.directory.mkdir(parents=True, exist_ok=True)
        self.row_group_size = row_group_size; self.compression_level = compression_level
        self._facts: list[dict[str, Any]] = []
        self._fact_writer: Any = None
        self._authority_members: list[dict[str, int]] = []
        self._dependency_members: list[dict[str, Any]] = []
        self._dims = {name: _Dimension(name) for name in
                      ("universe", "respondent", "question", "canonical_question", "component", "topology", "transform")}
        self._authorities = _Dimension("authority")
        self._transform_authorities = _Dimension("transform_authority")
        self._count = 0

    def _add_ref(self, dimension: str, value: Any) -> int | None:
        ref = _ref_dict(value)
        return self._dims[dimension].add(ref) if ref is not None else None

    def _add_transform(self, value: Any) -> int | None:
        authority = _authority_dict(value)
        if authority is not None:
            return self._transform_authorities.add(authority)
        ref = _ref_dict(value)
        return self._dims.setdefault("transform", _Dimension("transform")).add(ref) if ref is not None else None

    def append(self, objects: Iterable[RespondentEvent]) -> int:
        for obj in objects:
            if not isinstance(obj, RespondentEvent):
                raise TypeError("normalized writer accepts RespondentEvent objects only")
            fields = obj.semantic_fields
            event_key = self._count; self._count += 1
            root = obj.producer_replay_locator_or_reference_root
            root_is_ref = isinstance(root, ExactRef)
            row: dict[str, Any] = {
                "event_key": event_key,
                "universe_key": self._add_ref("universe", fields["empirical_universe_ref"]),
                "respondent_key": self._add_ref("respondent", fields["scoped_respondent_ref"]),
                "question_key": self._add_ref("question", fields["native_question_ref"]),
                "canonical_question_key": self._add_ref("canonical_question", fields["canonical_question_ref_if_authorized"]),
                "component_key": self._add_ref("component", fields["component_or_subitem_ref"]),
                "event_group_id": fields["event_group_id"],
                "event_id": fields["response_event_id_or_deterministic_index"],
                "typed_state": obj.typed_state,
                "response_state": fields["response_state"],
                "topology_key": self._add_ref("topology", fields["response_topology_ref"]),
                "multiplicity_order_rank_json": canonical_json(fields["multiplicity_order_rank_fields"]),
                "producer_root_kind": root.kind if root_is_ref else "__TEXT__",
                "producer_root_object_id": root.object_id if root_is_ref else str(root),
                "producer_root_content_hash": _hash_bytes(root.content_hash) if root_is_ref else None,
            }
            for prefix, value in (("raw", fields["raw_response_value"]),
                                  ("canonical", fields["canonical_response_value_if_authorized"])):
                kind, text, integer, real, boolean = _value_parts(value)
                row.update({f"{prefix}_value_kind": kind, f"{prefix}_value_text": text,
                            f"{prefix}_value_int64": integer, f"{prefix}_value_float64": real,
                            f"{prefix}_value_bool": boolean})
            row["transform_key"] = self._add_transform(fields["value_transform_authority_ref"])
            self._facts.append(row)
            for authority in obj.authority_snapshot_refs:
                item = _authority_dict(authority); assert item is not None
                self._authorities.add(item); self._authority_members.append({"event_key": event_key, "authority_key": _key(item)})
            for dependency in obj.dependency_refs:
                item = _ref_dict(dependency); assert item is not None
                self._dependency_members.append({"event_key": event_key, **_ref_row(item)})
            if len(self._facts) >= self.row_group_size:
                self._flush_facts()
        return self._count

    @staticmethod
    def _fact_schema() -> Any:
        import pyarrow as pa
        u64 = pa.uint64()
        return pa.schema([
            ("event_key", u64), ("universe_key", u64), ("respondent_key", u64), ("question_key", u64),
            ("canonical_question_key", u64), ("component_key", u64), ("event_group_id", pa.string()),
            ("event_id", pa.string()), ("typed_state", pa.string()), ("response_state", pa.string()),
            ("topology_key", u64), ("multiplicity_order_rank_json", pa.string()),
            ("raw_value_kind", pa.string()), ("raw_value_text", pa.string()), ("raw_value_int64", pa.int64()),
            ("raw_value_float64", pa.float64()), ("raw_value_bool", pa.bool_()),
            ("canonical_value_kind", pa.string()), ("canonical_value_text", pa.string()),
            ("canonical_value_int64", pa.int64()), ("canonical_value_float64", pa.float64()),
            ("canonical_value_bool", pa.bool_()), ("transform_key", u64),
            ("producer_root_kind", pa.string()), ("producer_root_object_id", pa.string()),
            ("producer_root_content_hash", pa.binary(32)),
        ])

    def _flush_facts(self) -> None:
        if not self._facts:
            return
        import pyarrow as pa
        import pyarrow.parquet as pq
        schema = self._fact_schema()
        if self._fact_writer is None:
            self._fact_writer = pq.ParquetWriter(
                self.directory / "respondent_events.normalized.parquet", schema,
                compression="zstd", compression_level=self.compression_level, use_dictionary=True)
        self._fact_writer.write_table(pa.Table.from_pylist(self._facts, schema=schema), row_group_size=self.row_group_size)
        self._facts.clear()

    def _write(self, name: str, rows: list[dict[str, Any]], schema: Any) -> NormalizedMember:
        import pyarrow as pa
        import pyarrow.parquet as pq
        path = self.directory / name
        table = pa.Table.from_pylist(rows, schema=schema)
        pq.write_table(table, path, compression="zstd", compression_level=self.compression_level,
                       use_dictionary=True, row_group_size=self.row_group_size)
        return NormalizedMember(name, path, len(rows), path.stat().st_size)

    def close(self) -> dict[str, NormalizedMember]:
        import pyarrow as pa
        self._flush_facts()
        if self._fact_writer is not None:
            self._fact_writer.close()
        fact_path = self.directory / "respondent_events.normalized.parquet"
        members = {"respondent_events.normalized.parquet": NormalizedMember(
            fact_path.name, fact_path, self._count, fact_path.stat().st_size)}
        u32 = pa.uint64()
        ref_fields = pa.schema([("local_key", u32), ("kind", pa.string()), ("object_id", pa.string()), ("content_hash", pa.binary(32))])
        for name, dim in self._dims.items():
            rows = [_ref_row(value) for value in dim.rows.values()]
            filename = f"{name}_dimension.parquet"
            members[filename] = self._write(filename, rows, ref_fields)
        auth_fields = pa.schema([("local_key", u32), ("authority_id", pa.string()), ("authority_version", pa.string()), ("authority_content_hash", pa.binary(32))])
        members["authority_dimension.parquet"] = self._write("authority_dimension.parquet", [_authority_row(v) for v in self._authorities.rows.values()], auth_fields)
        members["transform_authority_dimension.parquet"] = self._write("transform_authority_dimension.parquet", [_authority_row(v) for v in self._transform_authorities.rows.values()], auth_fields)
        members["event_authority_members.parquet"] = self._write("event_authority_members.parquet", self._authority_members, pa.schema([("event_key", u32), ("authority_key", u32)]))
        members["event_dependency_members.parquet"] = self._write("event_dependency_members.parquet", self._dependency_members, ref_fields_with_event := pa.schema([("event_key", u32), ("local_key", u32), ("kind", pa.string()), ("object_id", pa.string()), ("content_hash", pa.binary(32))]))
        return members

    @property
    def cardinalities(self) -> dict[str, int]:
        return {**{f"{name}_dimension": len(dim.rows) for name, dim in self._dims.items()},
                "authority_dimension": len(self._authorities.rows), "transform_authority_dimension": len(self._transform_authorities.rows), "event_authority_members": len(self._authority_members),
                "event_dependency_members": len(self._dependency_members), "respondent_events": self._count}


def _read_rows(path: Path) -> list[dict[str, Any]]:
    import pyarrow.parquet as pq
    return [dict(row) for row in pq.read_table(path).to_pylist()]


class NormalizedRespondentEventReader:
    def __init__(self, directory: str | Path) -> None:
        self.directory = Path(directory)
        self.dimensions = {name: {int(r["local_key"]): r for r in _read_rows(self.directory / f"{name}_dimension.parquet")}
                           for name in ("universe", "respondent", "question", "canonical_question", "component", "topology", "transform")}
        self.authorities = {int(r["local_key"]): r for r in _read_rows(self.directory / "authority_dimension.parquet")}
        self.transform_authorities = {int(r["local_key"]): r for r in _read_rows(self.directory / "transform_authority_dimension.parquet")}
        self.authority_members = _read_rows(self.directory / "event_authority_members.parquet")
        self.dependency_members = _read_rows(self.directory / "event_dependency_members.parquet")

    def iter_facts(self, *, batch_size: int = 8192) -> Iterator[dict[str, Any]]:
        import pyarrow.parquet as pq
        for batch in pq.ParquetFile(self.directory / "respondent_events.normalized.parquet").iter_batches(batch_size=batch_size):
            for row in batch.to_pylist():
                yield dict(row)

    @staticmethod
    def _ref(row: Mapping[str, Any] | None) -> dict[str, Any] | None:
        if row is None: return None
        return {"kind": row["kind"], "object_id": row["object_id"], "content_hash": bytes(row["content_hash"]).hex()}

    def reconstruct(self, row: Mapping[str, Any]) -> RespondentEvent:
        def ref(name: str, key: Any) -> dict[str, Any] | None:
            return self._ref(self.dimensions[name].get(int(key))) if key is not None else None
        auth = tuple({"authority_id": self.authorities[int(m["authority_key"])] ["authority_id"], "authority_version": self.authorities[int(m["authority_key"])] ["authority_version"], "authority_content_hash": bytes(self.authorities[int(m["authority_key"])] ["authority_content_hash"]).hex()} for m in self.authority_members if int(m["event_key"]) == int(row["event_key"]))
        deps = tuple(self._ref(m) for m in self.dependency_members if int(m["event_key"]) == int(row["event_key"]))
        def value(prefix: str) -> Any:
            return _value_from_parts(row[f"{prefix}_value_kind"], row[f"{prefix}_value_text"], row[f"{prefix}_value_int64"], row[f"{prefix}_value_float64"], row[f"{prefix}_value_bool"])
        transform = self.transform_authorities.get(int(row["transform_key"])) if row["transform_key"] is not None else None
        transform_value = ({"authority_id": transform["authority_id"], "authority_version": transform["authority_version"],
                            "authority_content_hash": bytes(transform["authority_content_hash"]).hex()} if transform is not None
                           else ref("transform", row["transform_key"]))
        root = (ExactRef(row["producer_root_kind"], row["producer_root_object_id"], bytes(row["producer_root_content_hash"]).hex())
                if row["producer_root_kind"] != "__TEXT__" else row["producer_root_object_id"])
        return RespondentEvent(typed_state=row["typed_state"], authority_snapshot_refs=auth, dependency_refs=deps,
            producer_replay_locator_or_reference_root=root,
            empirical_universe_ref=ref("universe", row["universe_key"]), scoped_respondent_ref=ref("respondent", row["respondent_key"]),
            native_question_ref=ref("question", row["question_key"]), canonical_question_ref_if_authorized=ref("canonical_question", row["canonical_question_key"]),
            component_or_subitem_ref=ref("component", row["component_key"]), event_group_id=row["event_group_id"],
            response_event_id_or_deterministic_index=row["event_id"], raw_response_value=value("raw"),
            canonical_response_value_if_authorized=value("canonical"), value_transform_authority_ref=transform_value,
            response_topology_ref=ref("topology", row["topology_key"]), multiplicity_order_rank_fields=json.loads(row["multiplicity_order_rank_json"]),
            response_state=row["response_state"])

    def audit(self) -> dict[str, int]:
        count = 0
        import pyarrow.parquet as pq
        for row in self.iter_facts():
            count += 1
            obj = self.reconstruct(row)
            if obj.ref.content_hash != obj.content_hash or obj.ref.object_id != obj.object_id:
                raise ValueError("normalized RespondentEvent identity mismatch")
        return {"respondent_events": count}


def query_normalized_relation(directory: str | Path, sql: str) -> list[tuple[Any, ...]]:
    """Run direct DuckDB SQL over normalized Parquet, using only an in-memory DB."""
    if any(token in sql.lower() for token in (".duckdb", "database_url", "sqlite", "postgres")):
        raise ValueError("persistent database paths are forbidden")
    import duckdb
    root = Path(directory)
    connection = duckdb.connect(":memory:")
    try:
        views = {
            "respondent_events": "respondent_events.normalized.parquet",
            "respondent_dimension": "respondent_dimension.parquet",
            "question_dimension": "question_dimension.parquet",
            "authority_dimension": "authority_dimension.parquet",
        }
        for view, filename in views.items():
            path = str(root / filename).replace("'", "''")
            connection.execute(f"CREATE VIEW {view} AS SELECT * FROM read_parquet('{path}')")
        return [tuple(row) for row in connection.execute(sql).fetchall()]
    finally:
        connection.close()


__all__ = ["NormalizedMember", "NormalizedRespondentEventReader", "NormalizedRespondentEventWriter",
           "query_normalized_relation"]
