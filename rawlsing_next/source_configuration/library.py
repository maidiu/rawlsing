"""Portable registry, index and delivery helpers for R157 source configurations.

The registry is a discovery/selection layer over the frozen SourceConfig schema and
the existing source-backed C11 factory.  It never invents source meaning or opens
original source bytes.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path
import sqlite3
from typing import Any, Iterable, Mapping

from rawlsing_next.source_configuration.evidence import load_source_roster, source_roster_entry
from rawlsing_next.source_configuration.factory import (
    build_validated_c11_release_from_config,
)
from rawlsing_next.source_configuration.fixture import load_fixture_stream, load_fixture_stream_bytes
from rawlsing_next.source_configuration.provider import (
    R157_COMMIT, R157_INDEX_PATH, FileSystemProvider, GitObjectProvider, ProviderError,
    ResourceProvider,
)
from rawlsing_next.source_configuration.reader import (
    reader_configuration_from_config,
    source_read_request_from_config,
)
from rawlsing_next.source_configuration.schema import (
    SourceConfig,
    canonical_config_hash,
    load_source_config,
    load_source_config_bytes,
)

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "rawlsing_next/source_configuration/data"
VALIDATION_DIR = ROOT / "source_pre553_validation"
INTEGRATION_DIR = VALIDATION_DIR / "integration"
INDEX_PATH = INTEGRATION_DIR / "SOURCE_LIBRARY_INDEX.json"
SQLITE_PATH = INTEGRATION_DIR / "SOURCE_LIBRARY_INDEX.sqlite"
PLAN_SEAL = "4c0c619eac747afee1d8e65e1418bf2d472da4c3"
FROZEN_P0 = "d8d7087a8e56c24042bf5945fea1c97eb0d6c710"
FROZEN_P3 = "519355ec2215409b40d566ef13c3b21f611e0726"
SOURCE_IDS = tuple(f"SRC{i:02d}" for i in range(1, 36))
PENDING_SOURCE_IDS = ("SRC27", "SRC28", "SRC29", "SRC30", "SRC33", "SRC34", "SRC35")
LOCATOR_BINDINGS_PATH = Path(__file__).resolve().parent / "source_locator_bindings.json"
PINNED_INDEX_PATH = ROOT / R157_INDEX_PATH
LOCAL_INDEX_PATH = ROOT / ".local-logs/pyat-universal35/r157-index/SOURCE_LIBRARY_INDEX.json"
LOCAL_SQLITE_PATH = ROOT / ".local-logs/pyat-universal35/r157-index/SOURCE_LIBRARY_INDEX.sqlite"


class SourceLibraryError(ValueError):
    pass


class SourceNotPrepared(SourceLibraryError):
    def __init__(self, source_id: str, status: str, detail: str = ""):
        self.source_id = source_id
        self.status = status
        self.detail = detail
        super().__init__(f"{source_id}: {status}" + (f": {detail}" if detail else ""))


class SourceArtifactError(SourceLibraryError):
    pass


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    family: str
    wave: str
    lane: str | None
    status: str
    original_config_path: str | None
    original_config_file_sha256: str | None
    original_config_canonical_sha256: str | None
    fixture_config_path: str | None
    fixture_config_file_sha256: str | None
    fixture_path: str | None
    fixture_file_sha256: str | None
    fixture_source_sha256: str | None
    native_results_path: str | None
    native_results_file_sha256: str | None
    release_ref: Mapping[str, Any] | None
    counts: Mapping[str, Any] = field(default_factory=dict)
    held: Mapping[str, Any] = field(default_factory=dict)
    details: tuple[str, ...] = ()

    @property
    def available(self) -> bool:
        return self.status == "AVAILABLE_NATIVE_RECEIPT"

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "family": self.family,
            "wave": self.wave,
            "lane": self.lane,
            "status": self.status,
            "original_config_path": self.original_config_path,
            "original_config_file_sha256": self.original_config_file_sha256,
            "original_config_canonical_sha256": self.original_config_canonical_sha256,
            "fixture_config_path": self.fixture_config_path,
            "fixture_config_file_sha256": self.fixture_config_file_sha256,
            "fixture_path": self.fixture_path,
            "fixture_file_sha256": self.fixture_file_sha256,
            "fixture_source_sha256": self.fixture_source_sha256,
            "native_results_path": self.native_results_path,
            "native_results_file_sha256": self.native_results_file_sha256,
            "release_ref": dict(self.release_ref) if self.release_ref else None,
            "counts": dict(self.counts),
            "held": dict(self.held),
            "details": list(self.details),
        }


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _exact_case_path(directory: Path, name: str) -> Path | None:
    """Return the actual directory entry whose spelling is exactly ``name``.

    ``Path.is_file()`` is case-insensitive on macOS, so it can silently accept a
    candidate spelling that does not exist on a case-sensitive checkout.  Indexed
    artifact paths must be the real committed spelling.
    """
    try:
        entries = list(directory.iterdir())
    except FileNotFoundError:
        return None
    for entry in entries:
        if entry.name == name and entry.is_file():
            return entry
    return None


def _exact_case_join(root: Path, relative: str | Path) -> Path:
    """Resolve a repository-relative path component-by-component, exact-case."""
    current = root
    for part in Path(relative).parts:
        if part in ("", "."):
            continue
        try:
            entries = list(current.iterdir())
        except FileNotFoundError:
            raise SourceArtifactError(f"missing path component {part!r} under {current}")
        child = next((entry for entry in entries if entry.name == part), None)
        if child is None:
            raise SourceArtifactError(f"non-exact path component {part!r} under {current}")
        current = child
    return current


def assert_exact_index_paths(index: Mapping[str, Any], root: Path = ROOT,
                             provider: ResourceProvider | None = None) -> None:
    """Assert every serialized source artifact path is the real directory spelling."""
    for row in index.get("sources", ()):  # type: ignore[union-attr]
        for field in ("original_config_path", "fixture_config_path", "fixture_path", "native_results_path"):
            relative = row.get(field)
            if not relative:
                continue
            if provider is not None:
                if not provider.exists(relative):
                    raise SourceArtifactError(f"{row.get('source_id')}: indexed {field} is not present: {relative}")
                continue
            path = _exact_case_join(root, relative)
            if not path.is_file():
                raise SourceArtifactError(f"{row.get('source_id')}: indexed {field} is not a file: {relative}")


def _lane_map() -> dict[str, str]:
    path = ROOT / "SOURCE_PRE553_PLAN/LANES.json"
    try:
        lanes = _json(path)["lanes"]
    except Exception:
        return {}
    return {sid: lane["lane_id"] for lane in lanes for sid in lane["source_ids"]}


def _candidate_original(source_id: str) -> Path | None:
    data = DATA_DIR / source_id
    numeric = source_id[3:]
    for name in (f"{source_id}.config.json", f"{source_id}.source.config.json",
                 f"src{numeric}.config.json", f"src{numeric}.source.config.json", "source.config.json"):
        path = _exact_case_path(data, name)
        if path is not None:
            try:
                config = load_source_config(path)
            except Exception:
                continue
            if config.config_purpose == "SOURCE_PREPARATION" and config.source_id == source_id:
                return path
    return None


def _candidate_fixture(source_id: str) -> tuple[Path, Path] | None:
    data = DATA_DIR / source_id
    validation = VALIDATION_DIR / source_id
    candidates = (
        (data, f"{source_id}.full.fixture.config.json", validation, f"{source_id}.full.fixture.json"),
        (data, f"{source_id}.fixture.config.json", validation, f"{source_id}.fixture.json"),
        (validation, f"{source_id}.full.fixture.config.json", validation, f"{source_id}.full.fixture.json"),
        (validation, f"{source_id}.fixture.config.json", validation, f"{source_id}.fixture.json"),
        (validation, "fixture.config.json", validation, "fixture.json"),
    )
    for config_dir, config_name, fixture_dir, fixture_name in candidates:
        config_path = _exact_case_path(config_dir, config_name)
        fixture_path = _exact_case_path(fixture_dir, fixture_name)
        if config_path is None or fixture_path is None:
            continue
        try:
            config = load_source_config(config_path)
            fixture = load_fixture_stream(fixture_path)
        except Exception:
            continue
        if config.config_purpose != "NONRESPONDENT_FIXTURE" or config.identity_class != "NONRESPONDENT_FIXTURE":
            continue
        if config.source_id != source_id:
            continue
        if config.active_source_sha256 != fixture.source_sha256:
            continue
        if config.active_row_count != fixture.row_count:
            continue
        return config_path, fixture_path
    return None


def _candidate_native(source_id: str) -> tuple[Path, Mapping[str, Any], Mapping[str, Any]] | None:
    validation = VALIDATION_DIR / source_id
    for name in ("FULL_NATIVE_RESULTS.json", "NATIVE_RESULTS.json",
                 "VALIDATION_RESULTS.json", f"{source_id}.validation-results.json",
                 "validation_results.json"):
        path = _exact_case_path(validation, name)
        if path is None:
            continue
        try:
            document = _json(path)
        except Exception:
            continue
        release = _find_release_ref(document)
        if release is not None:
            return path, document, release
    return None


def _find_release_ref(value: Any) -> Mapping[str, Any] | None:
    if isinstance(value, Mapping):
        ref = value.get("release_ref")
        if isinstance(ref, Mapping) and ref.get("kind") == "C11LogicalRelease":
            return ref
        if (value.get("kind") == "C11LogicalRelease"
                and isinstance(value.get("object_id"), str)
                and isinstance(value.get("content_hash"), str)):
            return value
        for item in value.values():
            found = _find_release_ref(item)
            if found is not None:
                return found
    elif isinstance(value, list):
        for item in value:
            found = _find_release_ref(item)
            if found is not None:
                return found
    return None


def _candidate_exception(source_id: str) -> Path | None:
    validation = VALIDATION_DIR / source_id
    for name in ("EXCEPTION_LEDGER.json", "EXCEPTIONS.json", f"{source_id}.exceptions.json",
                 "exception_ledger.json"):
        path = _exact_case_path(validation, name)
        if path is not None:
            return path
    return None


def _exception_summary(source_id: str) -> dict[str, Any]:
    path = _candidate_exception(source_id)
    if path is None:
        return {}
    try:
        document = _json(path)
    except Exception:
        return {"exception_path": str(path.relative_to(ROOT)), "exception_file_sha256": _sha(path)}
    summary: dict[str, Any] = {
        "exception_path": str(path.relative_to(ROOT)),
        "exception_file_sha256": _sha(path),
    }
    for key in ("residual_count", "bound_item_count", "held_item_count", "held_by_role_counts"):
        if key in document:
            summary[key] = document[key]
    held_items = document.get("held_items")
    if isinstance(held_items, list):
        summary["held_item_refs"] = [
            {
                "implementation_id": item.get("implementation_id"),
                "physical_slot": item.get("physical_slot"),
                "configuration_role": item.get("configuration_role"),
                "source_disposition": item.get("source_disposition"),
                "native_field": item.get("native_field"),
            }
            for item in held_items
            if isinstance(item, Mapping)
        ]
    return summary


def _held_counts(config: SourceConfig) -> dict[str, Any]:
    categories = Counter()
    for slot in config.document.get("physical_slots", ()):
        disposition = str(slot.get("disposition", ""))
        if disposition.startswith("HELD"):
            categories[disposition] += 1
    return {"held_slots": sum(categories.values()), "held_by_disposition": dict(sorted(categories.items()))}


def _write_sqlite(index: Mapping[str, Any], sqlite_path: str | Path | None) -> None:
    if sqlite_path is None:
        return
    sqlite_path = Path(sqlite_path)
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(sqlite_path)
    try:
        con.execute("drop table if exists sources")
        con.execute("""
            create table sources (
                source_id text primary key, family text, wave text, lane text, status text,
                original_config_path text, original_config_file_sha256 text,
                fixture_config_path text, fixture_path text,
                fixture_source_sha256 text, native_results_path text,
                release_object_id text, release_content_hash text,
                counts_json text, held_json text, details_json text
            )
        """)
        con.executemany(
            "insert into sources values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            [(r["source_id"], r["family"], r["wave"], r.get("lane"), r["status"],
              r.get("original_config_path"), r.get("original_config_file_sha256"),
              r.get("fixture_config_path"), r.get("fixture_path"),
              r.get("fixture_source_sha256"), r.get("native_results_path"),
              (r.get("release_ref") or {}).get("object_id"), (r.get("release_ref") or {}).get("content_hash"),
              json.dumps(r.get("counts", {}), sort_keys=True), json.dumps(r.get("held", {}), sort_keys=True),
              json.dumps(list(r.get("details", [])), sort_keys=True)) for r in index["sources"]])
        con.commit()
    finally:
        con.close()


def _build_pinned_index(*, index_path: str | Path | None, sqlite_path: str | Path | None,
                        provider: ResourceProvider, index_source: str | Path | None) -> dict[str, Any]:
    source_path = Path(index_source) if index_source is not None else PINNED_INDEX_PATH
    if source_path.is_file():
        document = _json(source_path)
    else:
        document = json.loads(provider.read_bytes(R157_INDEX_PATH).decode("utf-8"))
    if len(document.get("sources", ())) != 35:
        raise SourceLibraryError("pinned index does not contain exactly 35 sources")
    baseline = document.get("baseline", {})
    expected = {
        "sources": 35, "physical_columns": 18_413, "original_items": 18_276,
        "exact_relation_matches": 18_250, "unmatched_relation_ids": 26,
    }
    if baseline != expected:
        raise SourceLibraryError(f"pinned baseline mismatch: {baseline!r}")
    for row in document["sources"]:
        for field in ("original_config_path", "fixture_config_path", "fixture_path", "native_results_path"):
            relative = row.get(field)
            if relative and not provider.exists(relative):
                raise SourceArtifactError(f"{row.get('source_id')}: missing pinned {field}: {relative}")
        exception_path = (row.get("held") or {}).get("exception_path")
        if exception_path and not provider.exists(exception_path):
            raise SourceArtifactError(f"{row.get('source_id')}: missing pinned exception ledger: {exception_path}")
    target = Path(index_path) if index_path is not None else LOCAL_INDEX_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(document, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    _write_sqlite(document, sqlite_path if sqlite_path is not None else LOCAL_SQLITE_PATH)
    return document


def build_index(*, index_path: str | Path | None = None, sqlite_path: str | Path | None = None,
                provider: ResourceProvider | None = None,
                index_source: str | Path | None = None) -> dict[str, Any]:
    """Discover, validate and index the currently available canonical configs."""
    local_data = ROOT / "rawlsing_next/source_configuration/data"
    if provider is None and not (local_data.is_dir() and any(local_data.iterdir())):
        provider = GitObjectProvider()
    if provider is not None:
        return _build_pinned_index(
            index_path=index_path, sqlite_path=sqlite_path,
            provider=provider, index_source=index_source)
    index_path = Path(index_path) if index_path is not None else INDEX_PATH
    sqlite_path = Path(sqlite_path) if sqlite_path is not None else SQLITE_PATH
    index_path.parent.mkdir(parents=True, exist_ok=True)
    roster = load_source_roster()
    roster_by_id = {entry["source_id"]: entry for entry in roster["sources"]}
    lanes = _lane_map()
    records = []
    available = 0
    for source_id in SOURCE_IDS:
        entry = roster_by_id.get(source_id)
        if entry is None:
            raise SourceLibraryError(f"source roster missing {source_id}")
        original_path = _candidate_original(source_id)
        fixture_pair = _candidate_fixture(source_id) if original_path else None
        native = _candidate_native(source_id) if original_path and fixture_pair else None
        details = []
        if original_path is None:
            status = "PENDING_ACCEPTED_RETURN"
            details.append("No canonical SOURCE_PREPARATION config in this integration checkout.")
            records.append(SourceRecord(
                source_id=source_id, family=entry["family"], wave=entry["wave"], lane=lanes.get(source_id),
                status=status, original_config_path=None, original_config_file_sha256=None,
                original_config_canonical_sha256=None, fixture_config_path=None,
                fixture_config_file_sha256=None, fixture_path=None, fixture_file_sha256=None,
                fixture_source_sha256=None, native_results_path=None,
                native_results_file_sha256=None, release_ref=None, details=tuple(details)))
            continue
        original = load_source_config(original_path)
        counts = {
            "physical_slots": len(original.document.get("physical_slots", ())),
            "original_items": len(original.document.get("items", ())),
            "questions": len(original.document.get("questions", ())),
            "response_slots": len(original.document.get("response_slots", ())),
            "coordinate_slots": len(original.document.get("coordinate_slots", ())),
            "weight_slots": len(original.document.get("weight_slots", ())),
            "routing_rules": len(original.document.get("routing", ())),
        }
        if counts["physical_slots"] != int(entry["physical_columns"]):
            details.append(f"physical-slot denominator mismatch: {counts['physical_slots']} != {entry['physical_columns']}")
        if counts["original_items"] != int(entry["original_items"]):
            details.append(f"item denominator mismatch: {counts['original_items']} != {entry['original_items']}")
        if fixture_pair is None:
            status = "PREPARED_NO_FIXTURE"
            details.append("No matching nonrespondent fixture config/cells.")
        elif native is None:
            status = "PREPARED_NO_NATIVE_RESULT"
            details.append("No native release receipt for the fixture config.")
        else:
            status = "AVAILABLE_NATIVE_RECEIPT"
            available += 1
        fixture_config_path, fixture_path = fixture_pair if fixture_pair else (None, None)
        fixture_config = load_source_config(fixture_config_path) if fixture_config_path else None
        fixture_stream = load_fixture_stream(fixture_path) if fixture_path else None
        native_path, native_doc, release = native if native else (None, None, None)
        held = _held_counts(original)
        held.update(_exception_summary(source_id))
        records.append(SourceRecord(
            source_id=source_id, family=entry["family"], wave=entry["wave"], lane=lanes.get(source_id),
            status=status,
            original_config_path=str(original_path.relative_to(ROOT)),
            original_config_file_sha256=_sha(original_path),
            original_config_canonical_sha256=canonical_config_hash(original),
            fixture_config_path=str(fixture_config_path.relative_to(ROOT)) if fixture_config_path else None,
            fixture_config_file_sha256=_sha(fixture_config_path) if fixture_config_path else None,
            fixture_path=str(fixture_path.relative_to(ROOT)) if fixture_path else None,
            fixture_file_sha256=_sha(fixture_path) if fixture_path else None,
            fixture_source_sha256=fixture_config.active_source_sha256 if fixture_config else None,
            native_results_path=str(native_path.relative_to(ROOT)) if native_path else None,
            native_results_file_sha256=_sha(native_path) if native_path else None,
            release_ref=dict(release) if release else None,
            counts=counts,
            held=held,
            details=tuple(details),
        ))
    pending = [r.source_id for r in records if r.status == "PENDING_ACCEPTED_RETURN"]
    index = {
        "schema": "PYAT_R157_SOURCE_LIBRARY_INDEX@1.0.0",
        "plan_seal": PLAN_SEAL,
        "frozen_p0": FROZEN_P0,
        "frozen_p3": FROZEN_P3,
        "baseline": {
            "sources": len(SOURCE_IDS),
            "physical_columns": int(roster["counts"]["physical_columns"]),
            "original_items": int(roster["counts"]["original_items"]),
            "exact_relation_matches": int(roster["counts"]["exact_relation_matches"]),
            "unmatched_relation_ids": int(roster["counts"]["unmatched_relation_ids"]),
        },
        "counts": {
            "available": available,
            "pending": len(pending),
            "other_incomplete": len(records) - available - len(pending),
            "available_physical_slots": sum(r.counts.get("physical_slots", 0) for r in records if r.available),
            "available_original_items": sum(r.counts.get("original_items", 0) for r in records if r.available),
        },
        "pending_source_ids": pending,
        "sources": [r.as_dict() for r in records],
    }
    assert_exact_index_paths(index)
    index["path_case"] = "EXACT_DIRECTORY_ENTRY_ASSERTED"
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    if sqlite_path is not None:
        sqlite_path = Path(sqlite_path)
        sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(sqlite_path)
        try:
            con.execute("drop table if exists sources")
            con.execute("""
                create table sources (
                    source_id text primary key, family text, wave text, lane text, status text,
                    original_config_path text, original_config_file_sha256 text,
                    fixture_config_path text, fixture_path text,
                    fixture_source_sha256 text, native_results_path text,
                    release_object_id text, release_content_hash text,
                    counts_json text, held_json text, details_json text
                )
            """)
            con.executemany(
                "insert into sources values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                [(r.source_id, r.family, r.wave, r.lane, r.status, r.original_config_path,
                  r.original_config_file_sha256, r.fixture_config_path, r.fixture_path,
                  r.fixture_source_sha256, r.native_results_path,
                  (r.release_ref or {}).get("object_id"), (r.release_ref or {}).get("content_hash"),
                  json.dumps(r.counts, sort_keys=True), json.dumps(r.held, sort_keys=True),
                  json.dumps(list(r.details), sort_keys=True)) for r in records])
            con.commit()
        finally:
            con.close()
    return index


def _load_locator_bindings(path: str | Path = LOCATOR_BINDINGS_PATH) -> dict[str, Mapping[str, Any]]:
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return {row["source_id"]: row for row in document.get("rows", ()) if isinstance(row, Mapping) and row.get("source_id")}


class SourceConfigLibrary:
    """Actual callable registry over the portable index."""

    def __init__(self, *, index_path: str | Path = INDEX_PATH, root: str | Path = ROOT,
                 provider: ResourceProvider | None = None, source_root: str | Path | None = None,
                 locator_bindings_path: str | Path = LOCATOR_BINDINGS_PATH):
        self.root = Path(root).resolve()
        self.index_path = Path(index_path)
        if not self.index_path.is_file():
            raise SourceLibraryError(
                f"index missing: {self.index_path}; run `python -m rawlsing_next.source_configuration.cli build-index`")
        document = _json(self.index_path)
        self.document = document
        self.records = {row["source_id"]: row for row in document["sources"]}
        self.provider = provider
        if self.provider is None:
            try:
                sample = next(iter(self.records.values()))["original_config_path"]
                if not _exact_case_join(self.root, sample).is_file():
                    self.provider = GitObjectProvider()
            except Exception:
                self.provider = GitObjectProvider()
        self.source_root = Path(source_root).expanduser().resolve() if source_root is not None else None
        self.locator_bindings = _load_locator_bindings(locator_bindings_path)

    @classmethod
    def from_pinned_r157(cls, *, index_path: str | Path = PINNED_INDEX_PATH,
                         source_root: str | Path | None = None,
                         locator_bindings_path: str | Path = LOCATOR_BINDINGS_PATH) -> "SourceConfigLibrary":
        return cls(index_path=index_path, provider=GitObjectProvider(),
                   source_root=source_root, locator_bindings_path=locator_bindings_path)

    def record(self, source_id: str) -> Mapping[str, Any]:
        if source_id not in self.records:
            raise SourceNotPrepared(source_id, "UNKNOWN_SOURCE")
        row = self.records[source_id]
        if not row.get("status", "").startswith("AVAILABLE"):
            raise SourceNotPrepared(source_id, row.get("status", "PENDING"), "; ".join(row.get("details", [])))
        return row

    def source_ids(self) -> tuple[str, ...]:
        return tuple(self.records)

    def available_source_ids(self) -> tuple[str, ...]:
        return tuple(x for x in self.records if self.records[x].get("status") == "AVAILABLE_NATIVE_RECEIPT")

    def pending_source_ids(self) -> tuple[str, ...]:
        return tuple(self.document.get("pending_source_ids", []))

    def _artifact(self, source_id: str, kind: str) -> tuple[str, bytes | None, Mapping[str, Any]]:
        row = self.record(source_id)
        if kind == "original":
            relative = row["original_config_path"]
            expected = row["original_config_file_sha256"]
        elif kind == "fixture-config":
            relative = row["fixture_config_path"]
            expected = row["fixture_config_file_sha256"]
        elif kind == "fixture":
            relative = row["fixture_path"]
            expected = row["fixture_file_sha256"]
        else:
            raise SourceArtifactError(f"unknown artifact kind {kind!r}")
        if self.provider is not None:
            try:
                raw = self.provider.read_bytes(relative)
            except ProviderError as exc:
                raise SourceArtifactError(
                    f"{source_id}: non-exact path component or missing {kind} artifact: {relative}") from exc
            actual = hashlib.sha256(raw).hexdigest()
            if actual != expected:
                raise SourceArtifactError(f"{source_id}: {kind} SHA mismatch")
            return relative, raw, row
        path = _exact_case_join(self.root, relative)
        if not path.is_file():
            raise SourceArtifactError(f"{source_id}: missing {kind} artifact {path}")
        actual = _sha(path)
        if actual != expected:
            raise SourceArtifactError(f"{source_id}: {kind} SHA mismatch")
        return str(path), None, row

    def load_original(self, source_id: str) -> SourceConfig:
        path, raw, _ = self._artifact(source_id, "original")
        config = load_source_config_bytes(raw, path=path) if raw is not None else load_source_config(path)
        if config.source_id != source_id or config.config_purpose != "SOURCE_PREPARATION":
            raise SourceArtifactError(f"{source_id}: original config identity/purpose mismatch")
        return config

    def load_fixture_config(self, source_id: str) -> SourceConfig:
        path, raw, _ = self._artifact(source_id, "fixture-config")
        config = load_source_config_bytes(raw, path=path) if raw is not None else load_source_config(path)
        if config.source_id != source_id or config.config_purpose != "NONRESPONDENT_FIXTURE":
            raise SourceArtifactError(f"{source_id}: fixture config identity/purpose mismatch")
        return config

    def load_fixture_stream(self, source_id: str):
        path, raw, row = self._artifact(source_id, "fixture")
        stream = load_fixture_stream_bytes(raw, path=path) if raw is not None else load_fixture_stream(path)
        if stream.source_sha256 != row["fixture_source_sha256"]:
            raise SourceArtifactError(f"{source_id}: fixture stream source SHA mismatch")
        return stream

    def build_fixture_release(self, source_id: str):
        config = self.load_fixture_config(source_id)
        stream = self.load_fixture_stream(source_id)
        release = build_validated_c11_release_from_config(config, stream=stream)
        row = self.record(source_id)
        expected = (row.get("release_ref") or {}).get("content_hash")
        if expected and release.release_ref.content_hash != expected:
            raise SourceArtifactError(
                f"{source_id}: native release receipt mismatch {release.release_ref.content_hash} != {expected}")
        return release

    def validate_source(self, source_id: str) -> dict[str, Any]:
        row = self.record(source_id)
        original = self.load_original(source_id)
        fixture = self.load_fixture_config(source_id)
        stream = self.load_fixture_stream(source_id)
        roster = source_roster_entry(source_id)
        checks = {
            "original_schema": True,
            "fixture_schema": True,
            "original_source_id": original.source_id == source_id,
            "original_physical_slots": len(original.document.get("physical_slots", ())) == int(roster["physical_columns"]),
            "original_items": len(original.document.get("items", ())) == int(roster["original_items"]),
            "fixture_identity_class": fixture.identity_class == "NONRESPONDENT_FIXTURE",
            "fixture_sha_binding": fixture.active_source_sha256 == stream.source_sha256,
            "fixture_row_count": fixture.active_row_count == stream.row_count,
        }
        return {
            "corrections_applied": list(original.corrections_applied),
            "source_id": source_id,
            "status": row["status"],
            "config_path": row["original_config_path"],
            "fixture_config_path": row["fixture_config_path"],
            "fixture_path": row["fixture_path"],
            "native_results_path": row["native_results_path"],
            "checks": checks,
            "passed": all(checks.values()),
        }

    def effective_source_root(self, source_root: str | Path | None = None) -> tuple[Path | None, str]:
        if source_root is not None:
            return Path(source_root).expanduser().resolve(), "EXPLICIT_OVERRIDE"
        if self.source_root is not None:
            return self.source_root, "LIBRARY_DEFAULT"
        for name in ("R157_SOURCE_ROOT", "USER_ORIGINAL35_DATA_ROOT"):
            value = os.environ.get(name)
            if value:
                return Path(value).expanduser().resolve(), "ENVIRONMENT:" + name
        return None, "NO_SOURCE_ROOT_OVERRIDE"

    def resolve_source_path(self, source_id: str, *, source_root: str | Path | None = None,
                            source_relative_path: str | None = None) -> dict[str, Any]:
        config = self.load_original(source_id)
        root, root_source = self.effective_source_root(source_root)
        binding = self.locator_bindings.get(source_id, {})
        locator = config.document["identity"]["locator"]
        relative = source_relative_path or binding.get("relative_path")
        if relative is None and locator.get("root") == "SOURCE_ROOT":
            relative = locator.get("relative_path")
        expected = binding.get("source_sha256") or config.original_source_sha256
        if binding.get("source_sha256") and binding["source_sha256"] != config.original_source_sha256:
            return {
                "source_id": source_id, "status": "LOCATOR_BINDING_SHA_MISMATCH",
                "effective_source_root": str(root) if root else None,
                "source_root_source": root_source, "expected_source_sha256": expected,
                "source_read_performed": False,
            }
        if root is None:
            return {
                "source_id": source_id, "status": "NO_SOURCE_ROOT_OVERRIDE",
                "effective_source_root": None, "source_root_source": root_source,
                "expected_source_sha256": expected, "source_read_performed": False,
            }
        if not relative:
            return {
                "source_id": source_id, "status": "LOCATOR_REQUIRES_RELATIVE_PATH",
                "effective_source_root": str(root), "source_root_source": root_source,
                "expected_source_sha256": expected, "source_read_performed": False,
            }
        relative_path = Path(str(relative))
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise SourceArtifactError("source relative path must be non-absolute and must not escape the root")
        resolved = (root / relative_path).resolve()
        if resolved != root and root not in resolved.parents:
            raise SourceArtifactError("resolved source path escapes the effective source root")
        return {
            "source_id": source_id,
            "status": "RESOLVED_UNDER_EFFECTIVE_ROOT",
            "effective_source_root": str(root),
            "source_root_source": root_source,
            "relative_path": str(relative_path),
            "resolved_source_path": str(resolved),
            "locator_id": locator.get("locator_id"),
            "expected_source_sha256": expected,
            "binding_source_sha256": binding.get("source_sha256"),
            "binding_presence_grade": binding.get("presence_grade"),
            "source_read_performed": False,
        }

    def select(self, source_id: str, *, source_root: str | Path | None = None,
               source_relative_path: str | None = None) -> dict[str, Any]:
        row = self.record(source_id)
        original = self.load_original(source_id)
        try:
            fixture = self.load_fixture_config(source_id)
        except (SourceArtifactError, SourceNotPrepared):
            fixture = None
        reader = reader_configuration_from_config(original)
        identity = original.document["identity"]
        return {
            "schema": "PYAT_R157_SOURCE_SELECTION@1.0.0",
            "source_id": source_id,
            "status": row["status"],
            "family": row["family"],
            "wave": row["wave"],
            "original_config_path": row["original_config_path"],
            "original_config_file_sha256": row["original_config_file_sha256"],
            "original_config_canonical_sha256": row["original_config_canonical_sha256"],
            "config_purpose": original.config_purpose,
            "identity_class": original.identity_class,
            "source_format": identity["source_format"],
            "expected_source_sha256": identity["expected_source_sha256"],
            "counts": dict(row.get("counts", {})),
            "held": dict(row.get("held", {})),
            "fixture_config_path": row.get("fixture_config_path"),
            "fixture_path": row.get("fixture_path"),
            "fixture_source_sha256": row.get("fixture_source_sha256"),
            "corrections_applied": list(original.corrections_applied),
            "reader_configuration": {
                "source_sha256": reader.source_sha256,
                "encoding": reader.encoding,
                "authority_status": reader.authority_status,
                "configuration_ref": reader.configuration_ref.as_dict() if reader.configuration_ref else None,
            },
            "source_resolution": self.resolve_source_path(
                source_id, source_root=source_root, source_relative_path=source_relative_path),
            "runtime": dict(original.document.get("runtime", {})),
            "source_read_performed": False,
            "original_workload_issued": False,
        }

    def original_plan(self, source_id: str, *, source_path: str | None = None,
                      source_root: str | Path | None = None,
                      source_relative_path: str | None = None,
                      host: str, purpose: str,
                      consumer_use: str, semantic_use_scope: Iterable[str],
                      custody_locator_binding: str | None = None,
                      metadata_freeze_refs: Iterable[Any] | None = None) -> dict[str, Any]:
        config = self.load_original(source_id)
        resolution = self.resolve_source_path(
            source_id, source_root=source_root, source_relative_path=source_relative_path)
        effective_path = source_path or resolution.get("resolved_source_path")
        if not effective_path:
            raise SourceLibraryError(
                "an effective source-root override or explicit source_path is required: " + resolution["status"])
        request = source_read_request_from_config(
            config, host=host, purpose=purpose, consumer_use=consumer_use,
            semantic_use_scope=tuple(semantic_use_scope),
            custody_locator_binding=custody_locator_binding,
            metadata_freeze_refs=tuple(metadata_freeze_refs) if metadata_freeze_refs is not None else None,
        )
        reader = reader_configuration_from_config(config)
        return {
            "source_id": source_id,
            "source_path": effective_path,
            "source_resolution": resolution,
            "source_read_request": {
                "source_id": request.source_id,
                "source_sha256": request.source_sha256,
                "source_format": request.source_format,
                "custody_locator_binding": request.custody_locator_binding,
                "host": request.host,
                "purpose": request.purpose,
                "consumer_use": request.consumer_use,
                "read_operation": request.read_operation,
                "physical_read_extent": request.physical_read_extent,
                "metadata_freeze_refs": [x.as_dict() for x in request.metadata_freeze_refs],
                "semantic_use_scope": list(request.semantic_use_scope),
            },
            "reader_configuration": {
                "source_sha256": reader.source_sha256,
                "encoding": reader.encoding,
                "authority_status": reader.authority_status,
                "configuration_ref": reader.configuration_ref.as_dict() if reader.configuration_ref else None,
            },
            "required_external_arguments": [
                "source_path under the separately authorized source root",
                "a current SourceReadDecisionResolver decision for this exact request",
                "host/purpose/consumer_use/semantic_use_scope accepted by the issuer",
            ],
            "source_read_performed": False,
            "original_workload_issued": False,
            "note": "Plan only; no source bytes are opened. The existing source-read admission owner must authorize and decode separately.",
        }


__all__ = [
    "ROOT", "DATA_DIR", "VALIDATION_DIR", "INTEGRATION_DIR", "INDEX_PATH", "SQLITE_PATH",
    "PLAN_SEAL", "FROZEN_P0", "FROZEN_P3", "SOURCE_IDS", "PENDING_SOURCE_IDS",
    "SourceLibraryError", "SourceNotPrepared", "SourceArtifactError", "SourceRecord",
    "build_index", "SourceConfigLibrary", "assert_exact_index_paths",
]
