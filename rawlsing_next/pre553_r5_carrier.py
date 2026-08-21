"""Bounded LONG_SHARDED canonical carrier for PRE553 R5 shadow V1.

The carrier is deliberately boring: canonical newline-delimited records, bounded
external sorting, bounded independent shards, a streamed exhaustive inventory,
one immutable flat root, whole-member SHA-256, no cache, no matrix, no bitmap,
no Merkle hierarchy, and no source-family execution branches.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import asdict
import hashlib
import heapq
import json
import os
from pathlib import Path
import shutil
import tempfile
from typing import Any, Callable, Iterable, Iterator, Mapping, TextIO

from rawlsing_next.pre553_r5_codec import CODEC_VERSION, canonical_bytes, canonical_json
from rawlsing_next.pre553_r5_model import (
    CARRIER_ID, INVENTORY_SCHEMA_VERSION, ROOT_SCHEMA_VERSION, ROW_SCHEMA_VERSION,
    R5BuildConfig, R5CanonicalRow, R5Error, R5IntegrityError, R5QuarantinedError,
    R5ReleaseIdentity,
)


CARRIER_SCHEMA_VERSION = "PRE553_R5_LONG_SHARDED_CARRIER@1.0.0"


FaultHook = Callable[[str, Mapping[str, Any]], None]


def _noop_fault(_phase: str, _detail: Mapping[str, Any]) -> None:
    return None


def _sha256_file(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block); size += len(block)
    return digest.hexdigest(), size


def _fsync_file(path: Path) -> None:
    with path.open("rb") as handle:
        os.fsync(handle.fileno())


def _fsync_dir(path: Path) -> None:
    flags = getattr(os, "O_DIRECTORY", 0) | os.O_RDONLY
    fd = os.open(path, flags)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _valid_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and value == value.lower() and all(c in "0123456789abcdef" for c in value)


def _row_wire(row: R5CanonicalRow) -> bytes:
    if not all(isinstance(v, str) and v for v in (row.relation, row.object_family, row.object_id, row.content_hash)):
        raise R5Error("canonical row identity fields must be non-empty strings")
    if any("\t" in v or "\n" in v or "\r" in v or "\x1f" in v for v in (row.relation, row.object_family, row.object_id)):
        raise R5Error("canonical row identity fields may not contain control separators")
    if not _valid_sha256(row.content_hash):
        raise R5Error("canonical row content_hash must be lowercase sha256")
    payload = {
        "row_schema_version": ROW_SCHEMA_VERSION,
        "relation": row.relation,
        "object_family": row.object_family,
        "object_id": row.object_id,
        "content_hash": row.content_hash,
        "payload": row.payload,
    }
    return canonical_bytes(payload) + b"\n"


def _run_wire(row: R5CanonicalRow) -> bytes:
    key = "\x1f".join(row.identity_key).encode("utf-8")
    return key + b"\t" + _row_wire(row)


def _decode_row(line: bytes) -> R5CanonicalRow:
    try:
        item = json.loads(line.decode("ascii"))
    except Exception as exc:
        raise R5IntegrityError("canonical member row is not valid R5 JSON") from exc
    if item.get("row_schema_version") != ROW_SCHEMA_VERSION:
        raise R5IntegrityError("canonical row schema mismatch")
    try:
        row = R5CanonicalRow(item["relation"], item["object_family"], item["object_id"], item["content_hash"], item["payload"])
    except Exception as exc:
        raise R5IntegrityError("canonical member row shape invalid") from exc
    if _row_wire(row) != line:
        raise R5IntegrityError("canonical member row is not in canonical byte form")
    return row


def _identity_sort_bytes(row: R5CanonicalRow) -> bytes:
    return "\x1f".join(row.identity_key).encode("utf-8")


def _config_projection(config: R5BuildConfig) -> dict[str, int]:
    return asdict(config)


class R5LongShardedBuilder:
    def __init__(self, config: R5BuildConfig | None = None, *, fault_hook: FaultHook | None = None) -> None:
        self.config = config or R5BuildConfig()
        self.fault_hook = fault_hook or _noop_fault

    def _flush_run(self, directory: Path, run_index: int, records: list[bytes]) -> Path:
        records.sort()
        path = directory / f"run-{run_index:08d}.tmp"
        with path.open("wb") as handle:
            for record in records:
                handle.write(record)
            handle.flush(); os.fsync(handle.fileno())
        return path

    def _make_runs(self, rows: Iterable[R5CanonicalRow], work: Path) -> tuple[Path, dict[str, int]]:
        run_dir = work / "runs-0000"; run_dir.mkdir()
        manifest = work / "runs-0000.txt"
        run_index = row_count = 0
        max_rows = max_bytes = 0
        buffered: list[bytes] = []
        buffered_bytes = 0
        with manifest.open("w", encoding="utf-8", newline="\n") as mf:
            for row in rows:
                record = _run_wire(row)
                if buffered and (len(buffered) >= self.config.run_max_rows
                                 or buffered_bytes + len(record) > self.config.run_max_bytes):
                    path = self._flush_run(run_dir, run_index, buffered)
                    mf.write(path.name + "\n"); run_index += 1
                    max_rows = max(max_rows, len(buffered)); max_bytes = max(max_bytes, buffered_bytes)
                    buffered = []; buffered_bytes = 0
                buffered.append(record); buffered_bytes += len(record); row_count += 1
                if len(buffered) >= self.config.run_max_rows or buffered_bytes >= self.config.run_max_bytes:
                    path = self._flush_run(run_dir, run_index, buffered)
                    mf.write(path.name + "\n"); run_index += 1
                    max_rows = max(max_rows, len(buffered)); max_bytes = max(max_bytes, buffered_bytes)
                    buffered = []; buffered_bytes = 0
            if buffered:
                path = self._flush_run(run_dir, run_index, buffered)
                mf.write(path.name + "\n"); run_index += 1
                max_rows = max(max_rows, len(buffered)); max_bytes = max(max_bytes, buffered_bytes)
            mf.flush(); os.fsync(mf.fileno())
        if row_count == 0:
            raise R5Error("R5 canonical release cannot be empty")
        return manifest, {"input_rows": row_count, "initial_runs": run_index,
                          "max_buffered_run_rows": max_rows, "max_buffered_run_bytes": max_bytes}

    @staticmethod
    def _read_manifest_groups(manifest: Path, fan_in: int) -> Iterator[list[str]]:
        with manifest.open("r", encoding="utf-8") as handle:
            group = []
            for raw in handle:
                name = raw.rstrip("\n")
                if not name:
                    continue
                group.append(name)
                if len(group) >= fan_in:
                    yield group; group = []
            if group:
                yield group

    @staticmethod
    def _merge_run_group(source_dir: Path, names: list[str], target: Path) -> None:
        handles = [(source_dir / name).open("rb") for name in names]
        try:
            heap: list[tuple[bytes, int]] = []
            for idx, handle in enumerate(handles):
                line = handle.readline()
                if line:
                    heapq.heappush(heap, (line, idx))
            with target.open("wb") as out:
                while heap:
                    line, idx = heapq.heappop(heap)
                    out.write(line)
                    nxt = handles[idx].readline()
                    if nxt:
                        heapq.heappush(heap, (nxt, idx))
                out.flush(); os.fsync(out.fileno())
        finally:
            for handle in handles:
                handle.close()

    def _reduce_runs(self, initial_manifest: Path, work: Path) -> tuple[Path, Path, int, int]:
        manifest = initial_manifest
        source_dir = work / "runs-0000"
        pass_index = 0
        max_open = 1
        while True:
            # Count by streaming, never retaining path inventory.
            with manifest.open("r", encoding="utf-8") as handle:
                count = sum(1 for line in handle if line.strip())
            if count <= self.config.merge_fan_in:
                return manifest, source_dir, pass_index, max_open
            pass_index += 1
            target_dir = work / f"runs-{pass_index:04d}"; target_dir.mkdir()
            next_manifest = work / f"runs-{pass_index:04d}.txt"
            next_count = 0
            with next_manifest.open("w", encoding="utf-8", newline="\n") as out_manifest:
                for group in self._read_manifest_groups(manifest, self.config.merge_fan_in):
                    max_open = max(max_open, len(group))
                    target = target_dir / f"run-{next_count:08d}.tmp"
                    self._merge_run_group(source_dir, group, target)
                    out_manifest.write(target.name + "\n"); next_count += 1
                out_manifest.flush(); os.fsync(out_manifest.fileno())
            shutil.rmtree(source_dir)
            manifest.unlink()
            source_dir, manifest = target_dir, next_manifest

    @staticmethod
    def _iter_final_records(manifest: Path, source_dir: Path) -> Iterator[bytes]:
        names = []
        with manifest.open("r", encoding="utf-8") as handle:
            for line in handle:
                name = line.strip()
                if name:
                    names.append(name)
        # At this point the manifest contains <= merge_fan_in entries by construction.
        handles = [(source_dir / name).open("rb") for name in names]
        try:
            heap: list[tuple[bytes, int]] = []
            for idx, handle in enumerate(handles):
                line = handle.readline()
                if line:
                    heapq.heappush(heap, (line, idx))
            while heap:
                line, idx = heapq.heappop(heap)
                yield line
                nxt = handles[idx].readline()
                if nxt:
                    heapq.heappush(heap, (nxt, idx))
        finally:
            for handle in handles:
                handle.close()

    def build(self, rows: Iterable[R5CanonicalRow], *, release_identity: R5ReleaseIdentity,
              target_directory: str | Path) -> Mapping[str, Any]:
        target = Path(target_directory)
        if target.exists():
            raise R5Error("R5 build target must not already exist")
        target.mkdir(parents=True)
        members_dir = target / "members"; members_dir.mkdir()
        work = target / ".work"; work.mkdir()
        self.fault_hook("build_start", {"target": str(target)})
        try:
            manifest, telemetry = self._make_runs(rows, work)
            manifest, source_dir, passes, max_open = self._reduce_runs(manifest, work)
            telemetry.update({"merge_passes": passes, "max_merge_open_runs": max_open})

            inventory_path = target / "member_inventory.jsonl"
            inventory_count = shard_index = total_rows = 0
            global_logical = hashlib.sha256()
            previous_identity: tuple[str, str, str] | None = None
            current = None
            current_path: Path | None = None
            current_digest = None
            current_rows = current_bytes = 0
            current_first = current_last = None
            relation_counts: dict[str, int] = {}

            def close_shard() -> None:
                nonlocal current, current_path, current_digest, current_rows, current_bytes
                nonlocal current_first, current_last, relation_counts, inventory_count
                if current is None or current_path is None or current_digest is None:
                    return
                current.flush(); os.fsync(current.fileno()); current.close()
                descriptor = {
                    "inventory_schema_version": INVENTORY_SCHEMA_VERSION,
                    "member": current_path.name,
                    "byte_length": current_bytes,
                    "sha256": current_digest.hexdigest(),
                    "logical_digest": current_digest.hexdigest(),
                    "row_count": current_rows,
                    "first_identity": list(current_first),
                    "last_identity": list(current_last),
                    "relation_counts": dict(sorted(relation_counts.items())),
                }
                inv_handle.write(canonical_json(descriptor) + "\n"); inventory_count += 1
                current = current_path = current_digest = None
                current_rows = current_bytes = 0; current_first = current_last = None; relation_counts = {}

            with inventory_path.open("w", encoding="ascii", newline="\n") as inv_handle:
                for record in self._iter_final_records(manifest, source_dir):
                    try:
                        prefix, row_line = record.split(b"\t", 1)
                    except ValueError as exc:
                        raise R5IntegrityError("temporary run record malformed") from exc
                    row = _decode_row(row_line)
                    expected_prefix = _identity_sort_bytes(row)
                    if prefix != expected_prefix:
                        raise R5IntegrityError("temporary run identity prefix mismatch")
                    identity = row.identity_key
                    if previous_identity is not None and identity <= previous_identity:
                        if identity == previous_identity:
                            raise R5IntegrityError("duplicate canonical exact object identity")
                        raise R5IntegrityError("external merge order is noncanonical")
                    previous_identity = identity
                    if current is not None and (current_rows >= self.config.shard_max_rows
                                                or current_bytes + len(row_line) > self.config.shard_max_bytes):
                        close_shard(); shard_index += 1
                    if current is None:
                        current_path = members_dir / f"member-{shard_index:08d}.r5l"
                        current = current_path.open("wb"); current_digest = hashlib.sha256()
                        current_first = identity
                    current.write(row_line); current_digest.update(row_line); global_logical.update(row_line)
                    current_rows += 1; current_bytes += len(row_line); total_rows += 1; current_last = identity
                    relation_counts[row.relation] = relation_counts.get(row.relation, 0) + 1
                close_shard()
                inv_handle.flush(); os.fsync(inv_handle.fileno())
            self.fault_hook("members_closed", {"member_count": inventory_count, "row_count": total_rows})
            if total_rows != telemetry["input_rows"]:
                raise R5IntegrityError("row count changed during bounded external merge")
            inventory_sha, inventory_bytes = _sha256_file(inventory_path)
            release_projection = {
                "release_id": release_identity.release_id,
                "semantic_release_hash": release_identity.semantic_release_hash,
                "source_artifact_ref": dict(release_identity.source_artifact_ref),
                "source_release_manifest_hash": release_identity.source_release_manifest_hash,
                "m01_m18_coverage": {k: list(v) for k, v in sorted(release_identity.m01_m18_coverage.items())},
                "decoder_receipt": release_identity.decoder_receipt,
                "compiler_contract_digest": release_identity.compiler_contract_digest,
                "c11_authority_digest": release_identity.c11_authority_digest,
            }
            unsigned_root = {
                "root_schema_version": ROOT_SCHEMA_VERSION,
                "carrier_schema_version": CARRIER_SCHEMA_VERSION,
                "carrier_id": CARRIER_ID,
                "typed_codec_version": CODEC_VERSION,
                "release_identity": release_projection,
                "logical_stream_digest": global_logical.hexdigest(),
                "canonical_row_count": total_rows,
                "member_inventory": {"path": inventory_path.name, "sha256": inventory_sha,
                                     "byte_length": inventory_bytes, "member_count": inventory_count},
                "build_config": _config_projection(self.config),
            }
            physical_root_id = hashlib.sha256(canonical_bytes(unsigned_root)).hexdigest()
            root = {**unsigned_root, "physical_root_id": physical_root_id}
            root_path = target / "root.json"
            root_path.write_text(canonical_json(root) + "\n", encoding="ascii")
            _fsync_file(root_path); _fsync_file(inventory_path); _fsync_dir(members_dir); _fsync_dir(target)
            self.fault_hook("root_sealed", {"physical_root_id": physical_root_id})
            shutil.rmtree(work)
            telemetry.update({"final_shards": inventory_count, "canonical_rows": total_rows,
                              "physical_root_id": physical_root_id,
                              "logical_stream_digest": global_logical.hexdigest()})
            return telemetry
        except Exception:
            # Build directory is non-serving staging; caller/publisher owns cleanup policy.
            raise


class R5LongShardedReader:
    ROOT_MAX_BYTES = 2 * 1024 * 1024

    def __init__(self, release_directory: str | Path, *, expected_physical_root_id: str | None = None,
                 fault_hook: FaultHook | None = None) -> None:
        self.release_directory = Path(release_directory)
        self.fault_hook = fault_hook or _noop_fault
        self.quarantined = False
        self.root = self._load_root(expected_physical_root_id)
        self.release_identity = dict(self.root["release_identity"])
        self.config = R5BuildConfig(**self.root["build_config"])

    def _fail(self, message: str, exc: Exception | None = None) -> None:
        self.quarantined = True
        if exc is None:
            raise R5IntegrityError(message)
        raise R5IntegrityError(message) from exc

    def _require_healthy(self) -> None:
        if self.quarantined:
            raise R5QuarantinedError("R5 physical release is quarantined after canonical integrity failure")

    def _load_root(self, expected: str | None) -> Mapping[str, Any]:
        path = self.release_directory / "root.json"
        try:
            raw = path.read_bytes()
            if len(raw) > self.ROOT_MAX_BYTES:
                raise R5IntegrityError("root manifest exceeds bounded maximum")
            item = json.loads(raw.decode("ascii"))
        except Exception as exc:
            raise R5IntegrityError("R5 root manifest missing or invalid") from exc
        supplied = item.pop("physical_root_id", None)
        derived = hashlib.sha256(canonical_bytes(item)).hexdigest()
        if supplied != derived or (expected is not None and supplied != expected):
            raise R5IntegrityError("R5 physical root identity mismatch")
        if item.get("root_schema_version") != ROOT_SCHEMA_VERSION or item.get("carrier_id") != CARRIER_ID:
            raise R5IntegrityError("R5 root schema/carrier mismatch")
        return {**item, "physical_root_id": supplied}

    @contextmanager
    def _verified_spool(self, path: Path, expected_hash: str, expected_length: int):
        self._require_healthy()
        spool = tempfile.SpooledTemporaryFile(max_size=self.config.verified_spool_memory_bytes, mode="w+b")
        digest = hashlib.sha256(); length = 0
        try:
            self.fault_hook("before_verified_read", {"path": str(path)})
            with path.open("rb") as source:
                for block in iter(lambda: source.read(1024 * 1024), b""):
                    digest.update(block); length += len(block); spool.write(block)
            if length != expected_length or digest.hexdigest() != expected_hash:
                self._fail(f"missing or corrupt canonical member {path.name}")
            # Consume exactly the bytes authenticated above, not a reopened mutable path.
            spool.seek(0)
            self.fault_hook("after_verified_read", {"path": str(path), "length": length})
            yield spool
        except R5IntegrityError:
            raise
        except Exception as exc:
            self._fail(f"canonical member read failed {path.name}", exc)
        finally:
            spool.close()

    def iter_inventory(self) -> Iterator[Mapping[str, Any]]:
        self._require_healthy()
        info = self.root["member_inventory"]
        path = self.release_directory / info["path"]
        count = 0; previous_member = None
        with self._verified_spool(path, info["sha256"], info["byte_length"]) as spool:
            for raw in spool:
                try:
                    desc = json.loads(raw.decode("ascii"))
                except Exception as exc:
                    self._fail("member inventory row invalid", exc)
                if desc.get("inventory_schema_version") != INVENTORY_SCHEMA_VERSION:
                    self._fail("member inventory schema mismatch")
                member = desc.get("member")
                if (not isinstance(member, str) or not member.startswith("member-") or "/" in member or "\\" in member
                        or member in {".", ".."}):
                    self._fail("member inventory contains invalid path")
                if previous_member is not None and member <= previous_member:
                    self._fail("member inventory not strictly ordered")
                previous_member = member; count += 1
                yield desc
        if count != info["member_count"]:
            self._fail("member inventory cardinality mismatch")

    def iter_rows(self, *, relation: str | None = None) -> Iterator[R5CanonicalRow]:
        self._require_healthy()
        for desc in self.iter_inventory():
            path = self.release_directory / "members" / desc["member"]
            row_count = 0; digest = hashlib.sha256(); first = last = None; relation_counts: dict[str, int] = {}
            with self._verified_spool(path, desc["sha256"], desc["byte_length"]) as spool:
                for line in spool:
                    digest.update(line); row = _decode_row(line); row_count += 1
                    relation_counts[row.relation] = relation_counts.get(row.relation, 0) + 1
                    if first is None: first = row.identity_key
                    last = row.identity_key
                    if relation is None or row.relation == relation:
                        yield row
            if row_count != desc["row_count"] or digest.hexdigest() != desc["logical_digest"]:
                self._fail(f"logical member digest/count mismatch {desc['member']}")
            if list(first) != desc["first_identity"] or list(last) != desc["last_identity"]:
                self._fail(f"member coverage descriptor mismatch {desc['member']}")
            if dict(sorted(relation_counts.items())) != desc.get("relation_counts"):
                self._fail(f"member relation coverage mismatch {desc['member']}")

    def resolve_exact(self, relation: str, object_id: str) -> R5CanonicalRow | None:
        match = None
        for row in self.iter_rows():
            if row.relation == relation and row.object_id == object_id:
                if match is not None:
                    self._fail("exact scan found duplicate object identity")
                match = row
        return match

    def exact_scan(self, predicate: Callable[[R5CanonicalRow], bool]) -> Iterator[R5CanonicalRow]:
        # Correctness ground truth: no persistent cache/index/vocabulary is consulted.
        for row in self.iter_rows():
            if predicate(row):
                yield row

    def full_audit(self) -> Mapping[str, Any]:
        self._require_healthy()
        digest = hashlib.sha256(); rows = 0; previous = None; relations: dict[str, int] = {}
        try:
            for row in self.iter_rows():
                identity = row.identity_key
                if previous is not None and identity <= previous:
                    self._fail("full audit found duplicate/noncanonical row order")
                previous = identity
                wire = _row_wire(row); digest.update(wire); rows += 1
                relations[row.relation] = relations.get(row.relation, 0) + 1
            if rows != self.root["canonical_row_count"] or digest.hexdigest() != self.root["logical_stream_digest"]:
                self._fail("full audit semantic stream digest/count mismatch")
            return {"physical_root_id": self.root["physical_root_id"], "canonical_rows": rows,
                    "logical_stream_digest": digest.hexdigest(), "relation_counts": dict(sorted(relations.items()))}
        except R5IntegrityError:
            self.quarantined = True
            raise


__all__ = [
    "CARRIER_SCHEMA_VERSION", "R5LongShardedBuilder", "R5LongShardedReader",
    "R5BuildConfig", "R5ReleaseIdentity", "R5CanonicalRow",
]
