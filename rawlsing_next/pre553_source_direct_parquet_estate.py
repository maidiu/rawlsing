"""Source-direct bounded Parquet/Zstd C11 estate (S2-C SOURCEFREE CANDIDATE).

Consumes the original 13 one-shot typed family streams as S2-B certifies them,
without constructing a C11LogicalRelease, ReplayManifest.closure_refs or a
C11Repository dictionary. S2-B's SQLite is TEMPORARY proof scratch only.

A writer-returned digest is NEVER authority. Cold reading requires independently
held exact manifest digest AND direct I02 roots, and a caller-side current grant.
Native I03 wiring, competent issuer acceptance and integrated 100k/6GiB evidence
remain distinct gates; this module must not represent those as achieved.
"""
from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
from types import MappingProxyType
from typing import Any

from rawlsing_next._pre553_direct_i02_sourcefree import (
    SourcefreeDirectI02Sections, build_sourcefree_direct_i02, _FAMILIES,
)
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_empirical_objects import (
    ExactRef, Pre553IntegrityError, RespondentEvent, canonical_json, exact_ref,
)
from rawlsing_next.pre553_parquet_carrier import _object_row, _object_from_row
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec

SCHEMA = "PYAT_S2C_DIRECT_PARQUET_SOURCEFREE@1"
_FAMILIES_IN_ORDER = tuple(_FAMILIES)
_ROOT_FIELDS = ("logical", "physical", "release", "source", "replay", "universe", "schema")
_HEX_DIGITS = frozenset("0123456789abcdef")


class DirectEstateError(ValueError):
    """Never downgrade physical failure to valid EMPTY, ZERO or UNKNOWN."""


def _hash(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for part in iter(lambda: f.read(1024 * 1024), b""):
            h.update(part)
    return h.hexdigest()


def _hex(value: str) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in _HEX_DIGITS for c in value)


def _safe_dir(path: Path) -> None:
    try:
        st = path.lstat()
    except OSError as exc:
        raise DirectEstateError("storage directory missing") from exc
    if not stat.S_ISDIR(st.st_mode) or st.st_uid != os.getuid() or (st.st_mode & 0o077):
        raise DirectEstateError("storage must be a real owner-private directory")
    if path.is_symlink():
        raise DirectEstateError("symlinked directory refused")


def _root(path: str | Path) -> Path:
    result = Path(path).absolute()
    # Caller supplies existing authorized private root. Never create source
    # derived data outside it or follow a symlink component.
    for parent in (result, *result.parents):
        if parent.is_symlink():
            raise DirectEstateError("storage path contains a symlink")
    _safe_dir(result)
    return result


def _safe_member(path: Path) -> None:
    try:
        st = path.lstat()
    except OSError as exc:
        raise DirectEstateError("committed estate member missing") from exc
    if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or path.is_symlink():
        raise DirectEstateError("nonregular, linked or redirected estate member")


def _roots(i02: ExternalI02Roots) -> dict[str, str]:
    if type(i02) is not ExternalI02Roots:
        raise DirectEstateError("exact immutable S2-B roots required")
    return {name: getattr(i02, name) for name in _ROOT_FIELDS}


def _estate_name(i02: ExternalI02Roots) -> str:
    # No source-provided release_id interpolated into any filesystem path.
    return sha256(i02.release.encode("utf-8")).hexdigest()


def _arrow_schema():
    import pyarrow as pa
    return pa.schema([
        ("ref", pa.string()), ("kind", pa.string()),
        ("object_id", pa.string()), ("content_hash", pa.string()),
        ("family", pa.string()), ("typed_state", pa.string()),
        ("universe", pa.string()), ("respondent", pa.string()),
        ("native", pa.string()), ("canonical", pa.string()),
        ("component", pa.string()), ("occurrence", pa.string()),
        ("raw_typed", pa.string()),
        ("raw_text", pa.string()), ("raw_int64", pa.int64()),
        ("raw_float64", pa.float64()), ("raw_bool", pa.bool_()),
        ("body_json", pa.string()),
    ])


def _key(value: Any) -> str:
    if value is None:
        return ""
    try:
        return exact_ref(value).key
    except Exception as exc:
        raise DirectEstateError("invalid exact event/semantic reference") from exc


_CODEC = R5TypedValueCodec()


def _row(family: str, obj: object) -> dict[str, Any]:
    if family not in _FAMILIES or type(obj) is not _FAMILIES[family]:
        raise DirectEstateError("wrong typed source family at physical boundary")
    ref = obj.ref
    event = type(obj) is RespondentEvent
    raw = obj.raw_response_value if event else None
    # R5 preserves arbitrary decoder-normalized scalar widths and float bits,
    # including distinctions a single Parquet numeric cell cannot express.
    raw_typed = canonical_json(_CODEC.encode(raw)) if event else ""
    int_value = raw if type(raw) is int and -(1 << 63) <= raw < (1 << 63) else None
    return {
        "ref": ref.key, "kind": ref.kind, "object_id": ref.object_id,
        "content_hash": ref.content_hash, "family": family,
        "typed_state": str(getattr(obj, "typed_state", "")),
        "universe": _key(getattr(obj, "empirical_universe_ref", None)),
        "respondent": _key(getattr(obj, "scoped_respondent_ref", None)),
        "native": _key(getattr(obj, "native_question_ref", None)) if event else "",
        "canonical": _key(getattr(obj, "canonical_question_ref_if_authorized", None)) if event else "",
        "component": _key(getattr(obj, "component_or_subitem_ref", None)) if event else "",
        "occurrence": canonical_json({
            "group": obj.event_group_id,
            "id": obj.response_event_id_or_deterministic_index,
            "topology": obj.multiplicity_order_rank_fields,
        }) if event else "",
        "raw_typed": raw_typed,
        "raw_text": raw if type(raw) is str else None,
        "raw_int64": int_value,
        "raw_float64": raw if type(raw) is float else None,
        "raw_bool": raw if type(raw) is bool else None,
        "body_json": canonical_json(_object_row(obj)),
    }


class _Sink:
    def __init__(self, path: Path, family: str, chunk: int):
        self.path, self.family, self.chunk = path, family, chunk
        self.schema = _arrow_schema()
        self.writer = None
        self.pending: list[dict[str, Any]] = []
        self.count = 0
        self.group_number = 0

    def add(self, obj: object) -> tuple[int, int]:
        group = self.group_number
        offset = len(self.pending)
        self.pending.append(_row(self.family, obj))
        self.count += 1
        if len(self.pending) == self.chunk:
            self.flush()
        return group, offset

    def flush(self) -> None:
        if not self.pending:
            return
        import pyarrow as pa
        import pyarrow.parquet as pq
        if self.writer is None:
            self.writer = pq.ParquetWriter(
                self.path, self.schema, compression="zstd",
                use_dictionary=True, write_statistics=True,
            )
        self.writer.write_table(
            pa.Table.from_pylist(self.pending, schema=self.schema),
            row_group_size=self.chunk,
        )
        self.pending.clear()
        self.group_number += 1

    def close(self) -> None:
        import pyarrow as pa
        import pyarrow.parquet as pq
        self.flush()
        if self.writer is None:
            pq.write_table(pa.Table.from_pylist([], schema=self.schema),
                           self.path, compression="zstd")
        else:
            self.writer.close()
            self.writer = None
        self.path.chmod(0o600)


class _IndexSink:
    """Small selector/occurrence locator; NOT a second event-body corpus."""

    def __init__(self, path: Path, chunk: int):
        self.path, self.chunk = path, chunk
        self.pending: list[dict[str, Any]] = []
        self.writer = None
        self.schema = None
        self.count = 0

    def add(self, row: Mapping[str, Any], group: int, offset: int) -> None:
        self.pending.append({
            "ref": row["ref"], "respondent": row["respondent"],
            "native": row["native"], "canonical": row["canonical"],
            "component": row["component"], "state": row["typed_state"],
            "group": group, "offset": offset,
        })
        self.count += 1
        if len(self.pending) == self.chunk:
            self.flush()

    def flush(self) -> None:
        if not self.pending:
            return
        import pyarrow as pa
        import pyarrow.parquet as pq
        if self.schema is None:
            self.schema = pa.schema([
                ("ref", pa.string()), ("respondent", pa.string()),
                ("native", pa.string()), ("canonical", pa.string()),
                ("component", pa.string()), ("state", pa.string()),
                ("group", pa.int64()), ("offset", pa.int64()),
            ])
        if self.writer is None:
            self.writer = pq.ParquetWriter(
                self.path, self.schema, compression="zstd",
                use_dictionary=True, write_statistics=True,
            )
        self.writer.write_table(pa.Table.from_pylist(self.pending, schema=self.schema),
                                row_group_size=self.chunk)
        self.pending.clear()

    def close(self) -> None:
        import pyarrow as pa
        import pyarrow.parquet as pq
        self.flush()
        if self.writer is None:
            schema = pa.schema([
                ("ref", pa.string()), ("respondent", pa.string()),
                ("native", pa.string()), ("canonical", pa.string()),
                ("component", pa.string()), ("state", pa.string()),
                ("group", pa.int64()), ("offset", pa.int64()),
            ])
            pq.write_table(pa.Table.from_pylist([], schema=schema),
                           self.path, compression="zstd")
        else:
            self.writer.close()
            self.writer = None
        self.path.chmod(0o600)


@dataclass(frozen=True)
class EstateReceipt:
    """CANDIDATE evidence, not independently accepted scientific authority."""

    path: str
    manifest_sha256: str
    i02: ExternalI02Roots
    family_counts: Mapping[str, int]
    retained_bytes: int


def write_direct_estate(
    source: SourcefreeDirectI02Sections, universe_ref: ExactRef,
    authorized_private_root: str | Path, *,
    chunk_rows: int = 512,
    expected_i02: ExternalI02Roots | None = None,
) -> EstateReceipt:
    """One pass over all 13 typed families, co-producing I02 proof and Parquet.

    Requires a caller-authorized EXISTING private directory, never silently
    defaults to a global cache or source-based host path. Source read itself
    must already have been permitted by S1-B/S1-D; this does not issue it.
    """
    if type(source) is not SourcefreeDirectI02Sections or type(universe_ref) is not ExactRef:
        raise DirectEstateError("exact direct I02 input and universe required")
    if not isinstance(chunk_rows, int) or isinstance(chunk_rows, bool) or not (1 <= chunk_rows <= 8192):
        raise DirectEstateError("bounded physical row group size required")
    if set(source.sections) != set(_FAMILIES_IN_ORDER):
        raise DirectEstateError("all thirteen typed source families required")
    root = _root(authorized_private_root)
    stage = Path(tempfile.mkdtemp(prefix=".s2c-stage-", dir=root))
    stage.chmod(0o700)
    writers = {f: _Sink(stage / (f + ".parquet"), f, chunk_rows)
               for f in _FAMILIES_IN_ORDER}
    index = _IndexSink(stage / "event_locator.parquet", chunk_rows)
    i02 = None
    published = None
    try:
        # S2-B is the sole semantic owner. Every object is forwarded unchanged
        # and validated by its real source-direct I02 builder after the writer
        # has observed the SAME iterator item; no second source read.
        def tap(family: str):
            for obj in source.sections[family]:
                group, offset = writers[family].add(obj)
                if family == "RespondentEvent":
                    index.add(writers[family].pending[-1] if writers[family].pending
                              else _row(family, obj), group, offset)
                yield obj

        wrapped = SourcefreeDirectI02Sections(
            manifest=source.manifest,
            sections=MappingProxyType({
                f: tap(f) for f in _FAMILIES_IN_ORDER
            }),
            typed_absences=source.typed_absences,
            replay_protocol_authority_ref=source.replay_protocol_authority_ref,
            replay_protocol_version=source.replay_protocol_version,
            deterministic_tie_order_rules_ref=source.deterministic_tie_order_rules_ref,
        )
        scratch = stage / ".i02-proof.sqlite"
        i02 = build_sourcefree_direct_i02(
            wrapped, universe_ref, scratch, chunk_size=min(chunk_rows, 8192),
        )
        if expected_i02 is not None and _roots(i02) != _roots(expected_i02):
            raise DirectEstateError("complete direct I02 roots differ from independent expectation")
        for writer in writers.values():
            writer.close()
        index.close()
        # Prove the physical sidecar counts match the I02-validated stream
        # census; never turn a missing locator into authenticated EMPTY.
        if index.count != writers["RespondentEvent"].count:
            raise DirectEstateError("event locator omitted or duplicated an event")
        # SQLite is proof scratch and MUST NOT become a second durable corpus.
        scratch.unlink()
        members = {}
        for member in sorted((*[f + ".parquet" for f in _FAMILIES_IN_ORDER],
                              "event_locator.parquet")):
            candidate = stage / member
            _safe_member(candidate)
            members[member] = _hash(candidate)
        counts = {family: writer.count for family, writer in writers.items()}
        meta = {
            "schema": SCHEMA, "i02": _roots(i02),
            "source_manifest_sha256": source.manifest.content_hash,
            "family_counts": counts, "event_locator_count": index.count,
            "chunk_rows": chunk_rows, "members": members,
            "body_format": "legacy_exact_object_row_json_in_same_parquet_member",
            "proof": "SOURCEFREE_UNRECEIVED_NO_SELF_ISSUED_ROOT_AUTHORITY",
        }
        manifest_bytes = (canonical_json(meta) + "\n").encode("utf-8")
        with (stage / "manifest.pending").open("xb") as f:
            f.write(manifest_bytes)
            f.flush()
            os.fsync(f.fileno())
        (stage / "manifest.pending").chmod(0o600)
        for member in members:
            with (stage / member).open("rb") as f:
                os.fsync(f.fileno())
        # The selector is derived from the exact semantic release identity.
        # Never use a raw release_id or untrusted filename in this path.
        releases = root / "releases"
        if not releases.exists():
            releases.mkdir(mode=0o700)
        _safe_dir(releases)
        target = releases / _estate_name(i02)
        if target.exists() or target.is_symlink():
            raise DirectEstateError("content-addressed release already occupied: no clobber")
        # Atomic exclusive name claim. Until manifest.json exists, readers
        # categorically refuse the incomplete directory as an orphan.
        target.mkdir(mode=0o700)
        published = target
        for member in members:
            os.replace(stage / member, target / member)
        dir_fd = os.open(target, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
        # Atomic COMMIT marker: link complete manifest to a new final name.
        os.link(stage / "manifest.pending", target / "manifest.json", follow_symlinks=False)
        dir_fd = os.open(target, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
        base_fd = os.open(releases, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(base_fd)
        finally:
            os.close(base_fd)
        result = EstateReceipt(
            str(target), sha256(manifest_bytes).hexdigest(), i02,
            MappingProxyType(counts),
            sum((target / member).stat().st_size for member in members) + len(manifest_bytes),
        )
        published = None
        return result
    except Exception:
        # Only own new uncommitted target may be removed. Never delete a
        # finished or another writer's publication in response to a failure.
        if published is not None and not (published / "manifest.json").exists():
            shutil.rmtree(published)
        raise
    finally:
        shutil.rmtree(stage, ignore_errors=True)


class VerifiedDirectEstate:
    """Independently pinned physical reader with bounded row-group loading.

    A sourcefree candidate cannot authorize itself. Caller supplies held
    manifest digest, exact previously qualified S2-B roots, and a live
    independent current/rights guard on EACH materializing call.
    """
    def __init__(
        self, root: str | Path, *, exact_path: str | Path,
        independently_held_manifest_sha256: str,
        independently_held_i02: ExternalI02Roots,
        current_authorizer: Callable[[ExternalI02Roots], bool] | None,
    ):
        self.i02 = independently_held_i02
        if type(self.i02) is not ExternalI02Roots:
            raise DirectEstateError("exact independently held direct I02 roots required")
        if not _hex(independently_held_manifest_sha256):
            raise DirectEstateError("independently held SHA-256 required")
        if current_authorizer is None or not callable(current_authorizer):
            raise DirectEstateError("independent live current/rights guard required")
        self._authorize = current_authorizer
        # Refuse before hashing or opening any source-derived estate bytes.
        self._live()
        self.root = _root(root)
        candidate = Path(exact_path).absolute()
        expected = self.root / "releases" / _estate_name(self.i02)
        if candidate != expected:
            raise DirectEstateError("nonexact estate path or mismatched release identity")
        _safe_dir(expected.parent)
        _safe_dir(expected)
        self.directory = expected
        commit = expected / "manifest.json"
        _safe_member(commit)
        if _hash(commit) != independently_held_manifest_sha256:
            raise DirectEstateError("manifest differs from independently held root")
        try:
            manifest = json.loads(commit.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise DirectEstateError("committed manifest invalid") from exc
        if manifest.get("schema") != SCHEMA or manifest.get("i02") != _roots(self.i02):
            raise DirectEstateError("estate source/replay/universe/logical/physical roots mismatch")
        required = set(f + ".parquet" for f in _FAMILIES_IN_ORDER) | {"event_locator.parquet"}
        members = manifest.get("members")
        if not isinstance(members, dict) or set(members) != required:
            raise DirectEstateError("entire expected family/selector member set required")
        for name, digest in members.items():
            member = expected / name
            _safe_member(member)
            if not _hex(digest) or _hash(member) != digest:
                raise DirectEstateError("body/index Parquet member missing or corrupt")
        census = manifest.get("family_counts")
        if not isinstance(census, dict) or set(census) != set(_FAMILIES_IN_ORDER):
            raise DirectEstateError("thirteen complete source family counts required")
        if census["RespondentEvent"] != manifest.get("event_locator_count"):
            raise DirectEstateError("physical event locator census mismatch")
        self.manifest = manifest
        self._live()

    def _live(self) -> None:
        # This callback is a required guard, NOT a grant minted by this class.
        if self._authorize(self.i02) is not True:
            raise DirectEstateError("current source/operation authority refused")

    def iter_family(self, family: str, *, batch_size: int = 512) -> Iterator[object]:
        self._live()
        if family not in _FAMILIES_IN_ORDER:
            raise DirectEstateError("unknown canonical family")
        import pyarrow.parquet as pq
        pf = pq.ParquetFile(self.directory / (family + ".parquet"))
        seen = 0
        for batch in pf.iter_batches(batch_size=batch_size, columns=["body_json", "ref", "family"]):
            self._live()
            for data in batch.to_pylist():
                if data["family"] != family:
                    raise DirectEstateError("physical body family changed")
                obj = _object_from_row(json.loads(data["body_json"]))
                if type(obj) is not _FAMILIES[family] or obj.ref.key != data["ref"]:
                    raise DirectEstateError("cold exact native identity/body mismatch")
                seen += 1
                yield obj
        if seen != self.manifest["family_counts"][family]:
            raise DirectEstateError("incomplete family during bounded reconstruction")

    def _locators(self, *, respondent: str, target: ExactRef | None,
                  native_only: bool, include_component: bool,
                  states: frozenset[str] | None) -> Iterator[Mapping[str, Any]]:
        import pyarrow.parquet as pq
        pf = pq.ParquetFile(self.directory / "event_locator.parquet")
        examined = 0
        for batch in pf.iter_batches(batch_size=512):
            self._live()
            for row in batch.to_pylist():
                examined += 1
                if row["respondent"] != respondent:
                    continue
                if states is not None and row["state"] not in states:
                    continue
                if target is not None:
                    key = target.key
                    if row["native"] != key and (
                        native_only or (
                            row["canonical"] != key and (
                                not include_component or row["component"] != key
                            )
                        )
                    ):
                        continue
                yield row
        if examined != self.manifest["event_locator_count"]:
            raise DirectEstateError("incomplete physical locator scan")

    def select_events(
        self, respondent_ref: ExactRef, target: ExactRef | None = None, *,
        native_only: bool = False, include_component: bool = False,
        states: frozenset[str] | None = None,
    ) -> Iterator[RespondentEvent]:
        """Selected on-disk row groups only; no full pq.read_table/to_pylist."""
        self._live()
        # Source semantic fields are frozen mappings, not ExactRef instances.
        # The native strict parser requires precisely three validated fields;
        # reject malformed mappings and custom reference subclasses.
        try:
            respondent_ref = exact_ref(respondent_ref, "scoped_respondent_ref")
            if target is not None:
                target = exact_ref(target, "target_ref")
        except (Pre553IntegrityError, TypeError, ValueError) as exc:
            raise DirectEstateError("exact respondent and question selectors required") from exc
        if type(respondent_ref) is not ExactRef or (target is not None and type(target) is not ExactRef):
            raise DirectEstateError("exact respondent and question selectors required")
        import pyarrow.parquet as pq
        pf = pq.ParquetFile(self.directory / "RespondentEvent.parquet")
        group = None
        rows = None
        for posting in self._locators(
            respondent=respondent_ref.key, target=target,
            native_only=native_only, include_component=include_component,
            states=states,
        ):
            self._live()
            ref, gid, offset = posting["ref"], posting["group"], posting["offset"]
            if group != gid:
                rows = pf.read_row_group(gid, columns=["body_json", "ref"]).to_pylist()
                group = gid
            if rows is None or not (0 <= offset < len(rows)):
                raise DirectEstateError("event locator points beyond row-group bounds")
            row = rows[offset]
            if row["ref"] != ref:
                raise DirectEstateError("event locator targets different native body")
            obj = _object_from_row(json.loads(row["body_json"]))
            if type(obj) is not RespondentEvent or obj.ref.key != ref:
                raise DirectEstateError("selected native event semantic identity mismatch")
            # Matching event ID does not prove respondent/question/state selection.
            # Bind every physical posting to the reconstructed canonical body.
            if (posting["respondent"] != _key(obj.scoped_respondent_ref)
                    or posting["native"] != _key(obj.native_question_ref)
                    or posting["canonical"] != _key(obj.canonical_question_ref_if_authorized)
                    or posting["component"] != _key(obj.component_or_subitem_ref)
                    or posting["state"] != str(obj.typed_state)):
                raise DirectEstateError("physical event posting disagrees with exact native body")
            yield obj

__all__ = [
    "DirectEstateError", "EstateReceipt", "VerifiedDirectEstate",
    "write_direct_estate", "SCHEMA",
]
