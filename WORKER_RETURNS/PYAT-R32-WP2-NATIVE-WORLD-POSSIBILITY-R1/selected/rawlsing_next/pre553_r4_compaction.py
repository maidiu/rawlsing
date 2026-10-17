"""SR06 R4 functional-dependency compaction for RespondentEvent.

This is an execution representation.  Every omitted value is either a sealed
relation default, a deterministic locator function, or an explicit sparse
override.  Semantic identity is always recomputed by ``RespondentEvent``.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, RespondentEvent, canonical_json


def _ref(value: Any) -> dict[str, str] | None:
    if isinstance(value, ExactRef):
        return value.as_dict()
    if isinstance(value, Mapping) and set(value) == {"kind", "object_id", "content_hash"}:
        return {key: str(value[key]) for key in ("kind", "object_id", "content_hash")}
    return None


def _authority(value: Any) -> dict[str, str] | None:
    if isinstance(value, AuthorityRef):
        return value.as_dict()
    if isinstance(value, Mapping) and set(value) == {"authority_id", "authority_version", "authority_content_hash"}:
        return {key: str(value[key]) for key in ("authority_id", "authority_version", "authority_content_hash")}
    return None


def _json_ref(value: Any) -> str:
    return canonical_json(value.as_dict() if hasattr(value, "as_dict") else value)


def _value_parts(value: Any) -> tuple[int, int | None, str | None]:
    if value is None: return 0, None, None
    if isinstance(value, bool): return 3, int(value), None
    if isinstance(value, int): return 1, value, None
    if isinstance(value, float): return 2, None, repr(value)
    if isinstance(value, str): return 4, None, value
    return 5, None, canonical_json(value)


def _value_from_parts(kind: int, integer: int | None, text: str | None) -> Any:
    if kind == 0: return None
    if kind == 1: return integer
    if kind == 2: return float(text)
    if kind == 3: return bool(integer)
    if kind == 4: return text
    if kind == 5: return json.loads(text)
    raise ValueError(f"unknown R4 value kind {kind}")


def _sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


@dataclass(frozen=True)
class R4LocatorLaw:
    """Optional deterministic source-native locator rules for a sealed court."""
    event_id_template: str | None = None
    event_group_prefix: str | None = None
    event_group_modulus: int | None = None
    producer_root_kind: str | None = None
    producer_root_object_template: str | None = None
    producer_root_hash_seed_template: str | None = None

    def event_id(self, locator: int) -> str | None:
        return self.event_id_template.format(locator=locator) if self.event_id_template else None

    def event_group(self, locator: int) -> str | None:
        if self.event_group_prefix is None or self.event_group_modulus is None:
            return None
        return f"{self.event_group_prefix}{locator % self.event_group_modulus}"

    def producer_root(self, locator: int) -> ExactRef | None:
        if not (self.producer_root_kind and self.producer_root_object_template and self.producer_root_hash_seed_template):
            return None
        object_id = self.producer_root_object_template.format(locator=locator)
        seed = self.producer_root_hash_seed_template.format(locator=locator)
        return ExactRef(self.producer_root_kind, object_id, hashlib.sha256(seed.encode()).hexdigest())


def _dense(value: Mapping[str, Any]) -> tuple[str, str, str]:
    return str(value["kind"]), str(value["object_id"]), str(value["content_hash"])


class _DenseDimension:
    def __init__(self, name: str) -> None:
        self.name = name; self.by_value: dict[tuple[str, str, str], int] = {}; self.rows: list[dict[str, Any]] = []

    def add(self, value: Any) -> int | None:
        item = _ref(value)
        if item is None: return None
        key = _dense(item)
        if key not in self.by_value:
            ordinal = len(self.rows); self.by_value[key] = ordinal
            self.rows.append({"ordinal": ordinal, **item})
        return self.by_value[key]


class _DenseAuthorityDimension:
    def __init__(self) -> None:
        self.by_value: dict[str, int] = {}; self.rows: list[dict[str, Any]] = []

    def add(self, value: Any) -> int | None:
        item = _authority(value)
        if item is None: return None
        key = _json_ref(item)
        if key not in self.by_value:
            ordinal = len(self.rows); self.by_value[key] = ordinal; self.rows.append({"ordinal": ordinal, **item})
        return self.by_value[key]


def _state_code(value: str, states: dict[str, int]) -> int:
    if value not in states: states[value] = len(states)
    return states[value]


class R4RespondentEventWriter:
    """Streaming typed fact writer with sparse exact override relations."""

    def __init__(self, directory: str | Path, *, locator_law: R4LocatorLaw | None = None,
                 row_group_size: int = 4096, compression_level: int = 3) -> None:
        self.directory = Path(directory); self.directory.mkdir(parents=True, exist_ok=True)
        self.law = locator_law or R4LocatorLaw(); self.row_group_size = row_group_size; self.compression_level = compression_level
        self._batch: list[dict[str, Any]] = []; self._fact_writer = None; self._count = 0
        self._states: dict[str, int] = {}; self._topologies = _DenseDimension("topology")
        self._questions = _DenseDimension("question"); self._respondents = _DenseDimension("respondent")
        self._authorities: dict[str, int] = {}; self._authority_sets: list[tuple[dict[str, str], ...]] = []
        self._dependencies: dict[str, int] = {}; self._dependency_sets: list[tuple[dict[str, str], ...]] = []
        self._default_authority_set: int | None = None; self._default_dependency_set: int | None = None
        self._overrides: list[dict[str, Any]] = []; self._authority_overrides: list[dict[str, int]] = []; self._dependency_overrides: list[dict[str, int]] = []
        self._universe_default: dict[str, str] | None = None

    @staticmethod
    def _schema() -> Any:
        import pyarrow as pa
        return pa.schema([("event_locator", pa.uint32()), ("respondent_ordinal", pa.uint32()),
            ("question_ordinal", pa.uint16()), ("state_code", pa.uint8()), ("topology_ordinal", pa.uint8()),
            ("multiplicity_code", pa.uint8()), ("rank_field_code", pa.uint8()), ("rank_or_index", pa.int32()), ("raw_kind", pa.uint8()),
            ("raw_integer", pa.int64()), ("raw_text", pa.string())])

    def _flush(self) -> None:
        if not self._batch: return
        import pyarrow as pa, pyarrow.parquet as pq
        if self._fact_writer is None:
            self._fact_writer = pq.ParquetWriter(self.directory / "respondent_events.r4.parquet", self._schema(),
                compression="zstd", compression_level=self.compression_level, use_dictionary=True)
        self._fact_writer.write_table(pa.Table.from_pylist(self._batch, schema=self._schema()), row_group_size=self.row_group_size)
        self._batch.clear()

    def _set_id_or_override(self, locator: int, field: str, actual: Any, expected: Any) -> None:
        if expected != actual:
            self._overrides.append({"event_locator": locator, "field": field, "value_json": _json_ref(actual)})

    def _set_default_set(self, values: tuple[dict[str, str], ...], *, authority: bool) -> int:
        sets, index = (self._authority_sets, self._authorities) if authority else (self._dependency_sets, self._dependencies)
        key = tuple(sorted(values, key=_json_ref))
        for i, existing in enumerate(sets):
            if existing == key: return i
        ordinal = len(sets); sets.append(key)
        target = index
        for item in key:
            encoded = _json_ref(item)
            if encoded not in target: target[encoded] = len(target)
        return ordinal

    def append(self, objects: Iterable[RespondentEvent]) -> int:
        for obj in objects:
            if not isinstance(obj, RespondentEvent): raise TypeError("R4 writer accepts RespondentEvent only")
            locator = self._count; self._count += 1; f = obj.semantic_fields
            universe = _ref(f["empirical_universe_ref"])
            if self._universe_default is None: self._universe_default = universe
            elif universe != self._universe_default: self._overrides.append({"event_locator": locator, "field": "empirical_universe_ref", "value_json": _json_ref(universe)})
            event_group = f["event_group_id"]; event_id = f["response_event_id_or_deterministic_index"]; root = obj.producer_replay_locator_or_reference_root
            self._set_id_or_override(locator, "event_group_id", event_group, self.law.event_group(locator))
            self._set_id_or_override(locator, "event_id", event_id, self.law.event_id(locator))
            self._set_id_or_override(locator, "producer_root", root, self.law.producer_root(locator))
            auth = tuple(_authority(x) for x in obj.authority_snapshot_refs); deps = tuple(_ref(x) for x in obj.dependency_refs)
            auth = tuple(x for x in auth if x is not None); deps = tuple(x for x in deps if x is not None)
            auth_set = self._set_default_set(auth, authority=True); dep_set = self._set_default_set(deps, authority=False)
            if self._default_authority_set is None: self._default_authority_set = auth_set
            elif auth_set != self._default_authority_set: self._authority_overrides.append({"event_locator": locator, "set_ordinal": auth_set})
            if self._default_dependency_set is None: self._default_dependency_set = dep_set
            elif dep_set != self._default_dependency_set: self._dependency_overrides.append({"event_locator": locator, "set_ordinal": dep_set})
            multiplicity = f["multiplicity_order_rank_fields"]; kind = str(multiplicity.get("kind", ""))
            mcode = {"UNORDERED_MULTISELECT_SET": 0, "ORDERED_SEQUENCE": 1, "RANKED_RESPONSE": 2}.get(kind, 255)
            rank_field_code = 1 if "rank" in multiplicity else (2 if "multiplicity_index" in multiplicity else 0)
            rank = multiplicity.get("rank", multiplicity.get("multiplicity_index"))
            if mcode == 255 or set(multiplicity) - {"kind", "rank", "multiplicity_index"}:
                self._overrides.append({"event_locator": locator, "field": "multiplicity_order_rank_fields", "value_json": _json_ref(multiplicity)})
                mcode = 255; rank = None
            raw_kind, raw_integer, raw_text = _value_parts(f["raw_response_value"])
            if raw_kind >= 4:
                self._overrides.append({"event_locator": locator, "field": "raw_response_value", "value_json": _json_ref(f["raw_response_value"])})
                raw_text = None
            canonical = f["canonical_response_value_if_authorized"]
            if canonical is not None: self._overrides.append({"event_locator": locator, "field": "canonical_response_value_if_authorized", "value_json": _json_ref(canonical)})
            for field in ("canonical_question_ref_if_authorized", "component_or_subitem_ref", "value_transform_authority_ref"):
                if f[field] is not None:
                    self._overrides.append({"event_locator": locator, "field": field, "value_json": _json_ref(f[field])})
            self._batch.append({"event_locator": locator, "respondent_ordinal": self._respondents.add(f["scoped_respondent_ref"]),
                "question_ordinal": self._questions.add(f["native_question_ref"]), "state_code": _state_code(obj.typed_state, self._states),
                "topology_ordinal": self._topologies.add(f["response_topology_ref"]), "multiplicity_code": mcode, "rank_field_code": rank_field_code, "rank_or_index": rank,
                "raw_kind": raw_kind, "raw_integer": raw_integer if raw_kind in (1, 3) else None, "raw_text": raw_text if raw_kind in (2,) else None,
                })
            if len(self._batch) >= self.row_group_size: self._flush()
        return self._count

    def _write(self, filename: str, rows: list[dict[str, Any]], schema: Any) -> None:
        import pyarrow as pa, pyarrow.parquet as pq
        pq.write_table(pa.Table.from_pylist(rows, schema=schema), self.directory / filename,
                       compression="zstd", compression_level=self.compression_level, use_dictionary=True, row_group_size=self.row_group_size)

    def close(self) -> dict[str, int]:
        import pyarrow as pa
        self._flush()
        if self._fact_writer is not None: self._fact_writer.close()
        ref_schema = pa.schema([("ordinal", pa.uint32()), ("kind", pa.string()), ("object_id", pa.string()), ("content_hash", pa.binary(32))])
        members = {"respondent_events.r4.parquet": (self.directory / "respondent_events.r4.parquet").stat().st_size}
        for filename, dim in (("respondent_dimension.r4.parquet", self._respondents), ("question_dimension.r4.parquet", self._questions),
                              ("topology_dimension.r4.parquet", self._topologies)):
            rows = [{**row, "content_hash": bytes.fromhex(row["content_hash"])} for row in dim.rows]
            self._write(filename, rows, ref_schema); members[filename] = (self.directory / filename).stat().st_size
        authority_schema = pa.schema([("ordinal", pa.uint32()), ("value_json", pa.string())])
        self._write("authority_sets.r4.parquet", [{"ordinal": i, "value_json": _json_ref(v)} for i, v in enumerate(self._authority_sets)], authority_schema)
        self._write("dependency_sets.r4.parquet", [{"ordinal": i, "value_json": _json_ref(v)} for i, v in enumerate(self._dependency_sets)], authority_schema)
        override_schema = pa.schema([("event_locator", pa.uint32()), ("field", pa.string()), ("value_json", pa.string())])
        self._write("event_overrides.r4.parquet", self._overrides, override_schema)
        member_schema = pa.schema([("event_locator", pa.uint32()), ("set_ordinal", pa.uint32())])
        self._write("event_authority_overrides.r4.parquet", self._authority_overrides, member_schema)
        self._write("event_dependency_overrides.r4.parquet", self._dependency_overrides, member_schema)
        fixed = {"locator_law": asdict(self.law), "states": self._states, "universe_default": self._universe_default,
                 "default_authority_set": self._default_authority_set, "default_dependency_set": self._default_dependency_set}
        fixed["members"] = {path.name: _sha_file(path) for path in self.directory.glob("*.parquet")}
        (self.directory / "r4_manifest.json").write_text(json.dumps(fixed, sort_keys=True), encoding="utf-8")
        for path in self.directory.glob("*.parquet"): members[path.name] = path.stat().st_size
        return members

    @property
    def cardinalities(self) -> dict[str, int]:
        return {"events": self._count, "respondents": len(self._respondents.rows), "questions": len(self._questions.rows),
                "universes": 1 if self._universe_default is not None else 0, "topologies": len(self._topologies.rows),
                "states": len(self._states), "authority_sets": len(self._authority_sets), "dependency_sets": len(self._dependency_sets),
                "event_overrides": len(self._overrides), "authority_overrides": len(self._authority_overrides), "dependency_overrides": len(self._dependency_overrides)}


class R4RespondentEventReader:
    def __init__(self, directory: str | Path) -> None:
        import pyarrow.parquet as pq
        self.directory = Path(directory); self.manifest = json.loads((self.directory / "r4_manifest.json").read_text())
        for name, expected in self.manifest["members"].items():
            path = self.directory / name
            if not path.is_file() or _sha_file(path) != expected:
                raise ValueError(f"R4 member hash verification failed: {name}")
        self.law = R4LocatorLaw(**self.manifest["locator_law"]); self.states = {int(v): k for k, v in self.manifest["states"].items()}
        def dim(name: str) -> dict[int, dict[str, Any]]:
            return {int(r["ordinal"]): {**r, "content_hash": bytes(r["content_hash"]).hex()} for r in pq.read_table(self.directory / name).to_pylist()}
        self.respondents = dim("respondent_dimension.r4.parquet"); self.questions = dim("question_dimension.r4.parquet")
        self.topologies = dim("topology_dimension.r4.parquet")
        self.authority_sets = [tuple(json.loads(r["value_json"])) for r in pq.read_table(self.directory / "authority_sets.r4.parquet").to_pylist()]
        self.dependency_sets = [tuple(json.loads(r["value_json"])) for r in pq.read_table(self.directory / "dependency_sets.r4.parquet").to_pylist()]
        self.overrides = {}
        for row in pq.read_table(self.directory / "event_overrides.r4.parquet").to_pylist(): self.overrides.setdefault(int(row["event_locator"]), {})[row["field"]] = json.loads(row["value_json"])
        self.authority_overrides = {int(r["event_locator"]): int(r["set_ordinal"]) for r in pq.read_table(self.directory / "event_authority_overrides.r4.parquet").to_pylist()}
        self.dependency_overrides = {int(r["event_locator"]): int(r["set_ordinal"]) for r in pq.read_table(self.directory / "event_dependency_overrides.r4.parquet").to_pylist()}

    def iter_rows(self, *, batch_size: int = 8192) -> Iterator[dict[str, Any]]:
        import pyarrow.parquet as pq
        for batch in pq.ParquetFile(self.directory / "respondent_events.r4.parquet").iter_batches(batch_size=batch_size):
            yield from batch.to_pylist()

    @staticmethod
    def _ref(dim: Mapping[int, Mapping[str, Any]], ordinal: Any) -> dict[str, Any] | None:
        if ordinal is None: return None
        row = dim[int(ordinal)]; return {"kind": row["kind"], "object_id": row["object_id"], "content_hash": row["content_hash"]}

    def reconstruct(self, row: Mapping[str, Any]) -> RespondentEvent:
        i = int(row["event_locator"]); override = self.overrides.get(i, {})
        event_id = self.law.event_id(i) or override.get("event_id"); group = self.law.event_group(i) or override.get("event_group_id"); root = self.law.producer_root(i) or ExactRef(**override["producer_root"])
        auth_set = self.authority_overrides.get(i, self.manifest["default_authority_set"]); dep_set = self.dependency_overrides.get(i, self.manifest["default_dependency_set"])
        auth = tuple(AuthorityRef(**x) for x in self.authority_sets[auth_set]); deps = tuple(ExactRef(**x) for x in self.dependency_sets[dep_set])
        state = self.states[int(row["state_code"])]
        multiplicity = {0: "UNORDERED_MULTISELECT_SET", 1: "ORDERED_SEQUENCE", 2: "RANKED_RESPONSE"}.get(int(row["multiplicity_code"]))
        if multiplicity is None: multiplicity = override["multiplicity_order_rank_fields"]
        elif row["rank_or_index"] is not None:
            multiplicity = {"kind": multiplicity, ("rank" if int(row["rank_field_code"]) == 1 else "multiplicity_index"): int(row["rank_or_index"])}
        raw_kind = int(row["raw_kind"]); raw = override.get("raw_response_value") if raw_kind >= 4 else _value_from_parts(raw_kind, row["raw_integer"], row["raw_text"])
        canonical = override.get("canonical_response_value_if_authorized")
        universe = self.manifest["universe_default"]
        if "empirical_universe_ref" in override: universe = override["empirical_universe_ref"]
        transform_value = override.get("value_transform_authority_ref")
        return RespondentEvent(typed_state=state, authority_snapshot_refs=auth, dependency_refs=deps, producer_replay_locator_or_reference_root=root,
            empirical_universe_ref=universe, scoped_respondent_ref=self._ref(self.respondents, row["respondent_ordinal"]), native_question_ref=self._ref(self.questions, row["question_ordinal"]),
            canonical_question_ref_if_authorized=override.get("canonical_question_ref_if_authorized"), component_or_subitem_ref=override.get("component_or_subitem_ref"),
            event_group_id=group, response_event_id_or_deterministic_index=event_id, raw_response_value=raw, canonical_response_value_if_authorized=canonical,
            value_transform_authority_ref=transform_value, response_topology_ref=self._ref(self.topologies, row["topology_ordinal"]),
            multiplicity_order_rank_fields=multiplicity, response_state=state)

    def audit(self) -> int:
        count = 0
        for row in self.iter_rows():
            self.reconstruct(row); count += 1
        return count


def query_r4(directory: str | Path, sql: str) -> list[tuple[Any, ...]]:
    if any(token in sql.lower() for token in (".duckdb", "database_url", "sqlite", "postgres")):
        raise ValueError("persistent database paths are forbidden")
    import duckdb
    root = Path(directory); connection = duckdb.connect(":memory:")
    try:
        views = {"respondent_events": "respondent_events.r4.parquet", "respondent_dimension": "respondent_dimension.r4.parquet",
                 "question_dimension": "question_dimension.r4.parquet"}
        for view, filename in views.items():
            path = str(root / filename).replace("'", "''")
            connection.execute(f"CREATE VIEW {view} AS SELECT * FROM read_parquet('{path}')")
        return [tuple(row) for row in connection.execute(sql).fetchall()]
    finally:
        connection.close()


__all__ = ["R4LocatorLaw", "R4RespondentEventReader", "R4RespondentEventWriter", "query_r4"]
