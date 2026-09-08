"""Compact LONG_SHARDED physical carrier for PRE553 R5.

V2 preserves the exact R5CanonicalRow projection while avoiding the V1 mistake
of serializing a self-describing canonical JSON object for every source cell.
Physical-cell rows use a compact tagged array and deterministic reconstruction;
other relations use a generic exact escape. Independent members and external
sort runs are gzip-compressed with deterministic headers.
"""
from __future__ import annotations
from contextlib import contextmanager
from dataclasses import asdict
import gzip, hashlib, heapq, json, os, shutil, struct, tempfile
from pathlib import Path
from typing import Any, Callable, Mapping
from rawlsing_next.pre553_r5_codec import CODEC_VERSION, canonical_bytes, canonical_json
from rawlsing_next.pre553_r5_model import (
    CARRIER_ID, INVENTORY_SCHEMA_VERSION, ROOT_SCHEMA_VERSION, ROW_SCHEMA_VERSION,
    R5BuildConfig, R5CanonicalRow, R5Error, R5IntegrityError, R5QuarantinedError,
    R5ReleaseIdentity,
)

CARRIER_SCHEMA_VERSION = "PRE553_R5_LONG_SHARDED_CARRIER@2.0.0"
MEMBER_ENCODING = "GZIP_COMPACT_JSONL@2.0.0"
CELL_RELATION = "source_physical_cells"
CELL_FAMILY = "R5PhysicalCell@1.0.0"
FaultHook = Callable[[str, Mapping[str, Any]], None]


def _noop_fault(_phase, _detail):
    return None


def _sha256_file(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
            size += len(block)
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
    return (
        isinstance(value, str)
        and len(value) == 64
        and value == value.lower()
        and all(c in "0123456789abcdef" for c in value)
    )


def _logical_wire(row: R5CanonicalRow) -> bytes:
    if not all(
        isinstance(v, str) and v
        for v in (row.relation, row.object_family, row.object_id, row.content_hash)
    ):
        raise R5Error("canonical row identity fields must be non-empty strings")
    if any(
        any(c in v for c in ("\t", "\n", "\r", "\x1f"))
        for v in (row.relation, row.object_family, row.object_id)
    ):
        raise R5Error("canonical row identity fields contain forbidden separators")
    if not _valid_sha256(row.content_hash):
        raise R5Error("canonical row content_hash must be lowercase sha256")
    return canonical_bytes(
        {
            "row_schema_version": ROW_SCHEMA_VERSION,
            "relation": row.relation,
            "object_family": row.object_family,
            "object_id": row.object_id,
            "content_hash": row.content_hash,
            "payload": row.payload,
        }
    ) + b"\n"


def _storage_wire(row: R5CanonicalRow) -> bytes:
    payload = row.payload
    if row.relation == CELL_RELATION and row.object_family == CELL_FAMILY:
        required = {
            "seam_version",
            "source_sha256",
            "row_ordinal",
            "variable_ordinal",
            "variable_name",
            "raw_value",
            "missing_state",
            "source_missing_declaration",
            "raw_value_label",
            "explicit_source_coordinates",
            "source_cell_locator",
        }
        if set(payload) != required:
            raise R5Error("physical-cell payload shape is not compact-V2 exact")
        if not _valid_sha256(payload["source_sha256"]):
            raise R5Error("physical-cell source SHA-256 invalid")
        row_no = int(payload["row_ordinal"])
        var_no = int(payload["variable_ordinal"])
        if list(payload["explicit_source_coordinates"]) != [row_no, var_no]:
            raise R5Error(
                "physical-cell explicit coordinates diverge from row/variable ordinals"
            )
        expected_id = f"source:{payload['source_sha256']}:cell:{row_no}:{var_no}"
        if row.object_id != expected_id:
            raise R5Error(
                "physical-cell object id is not reconstructable from frozen coordinates"
            )
        expected_hash = hashlib.sha256(canonical_bytes(payload)).hexdigest()
        if row.content_hash != expected_hash:
            raise R5Error(
                "physical-cell content hash does not match canonical payload"
            )
        # Tag 1. These fields are retained; relation/family/object_id/content_hash
        # and explicit coordinates are deterministic exact reconstruction functions.
        item = [
            1,
            payload["seam_version"],
            payload["source_sha256"],
            row_no,
            var_no,
            payload["variable_name"],
            payload["raw_value"],
            payload["missing_state"],
            payload["source_missing_declaration"],
            payload["raw_value_label"],
            payload["source_cell_locator"],
        ]
    else:
        # Generic exact escape for low-volume/non-cell relations.
        item = [
            0,
            row.relation,
            row.object_family,
            row.object_id,
            row.content_hash,
            row.payload,
        ]
    return canonical_bytes(item) + b"\n"


def _decode_storage(line: bytes) -> R5CanonicalRow:
    try:
        item = json.loads(line.decode("ascii"))
    except Exception as exc:
        raise R5IntegrityError(
            "compact member row is not valid canonical JSON"
        ) from exc
    if not isinstance(item, list) or not item:
        raise R5IntegrityError("compact member row shape invalid")
    if item[0] == 1:
        if len(item) != 11:
            raise R5IntegrityError("compact physical-cell row arity invalid")
        (
            _, seam, source_sha, row_no, var_no, var_name, raw_value,
            missing_state, missing_decl, raw_label, locator,
        ) = item
        payload = {
            "seam_version": seam,
            "source_sha256": source_sha,
            "row_ordinal": int(row_no),
            "variable_ordinal": int(var_no),
            "variable_name": var_name,
            "raw_value": raw_value,
            "missing_state": missing_state,
            "source_missing_declaration": missing_decl,
            "raw_value_label": raw_label,
            "explicit_source_coordinates": [int(row_no), int(var_no)],
            "source_cell_locator": locator,
        }
        object_id = f"source:{source_sha}:cell:{int(row_no)}:{int(var_no)}"
        content_hash = hashlib.sha256(canonical_bytes(payload)).hexdigest()
        row = R5CanonicalRow(
            CELL_RELATION, CELL_FAMILY, object_id, content_hash, payload
        )
    elif item[0] == 0:
        if len(item) != 6:
            raise R5IntegrityError("generic compact row arity invalid")
        _, relation, family, object_id, content_hash, payload = item
        row = R5CanonicalRow(
            relation, family, object_id, content_hash, payload
        )
        if not _valid_sha256(content_hash):
            raise R5IntegrityError("generic row hash invalid")
    else:
        raise R5IntegrityError("unknown compact row tag")
    if _storage_wire(row) != line:
        raise R5IntegrityError(
            "compact row is not canonical/reconstructable byte form"
        )
    return row


def _sort_key(row: R5CanonicalRow) -> bytes:
    return b"\x1f".join(v.encode("utf-8") for v in row.identity_key)


def _config_projection(config: R5BuildConfig) -> dict[str, int]:
    return asdict(config)


def _gzip_writer(path: Path):
    raw = path.open("wb")
    gz = gzip.GzipFile(
        filename="", mode="wb", fileobj=raw, compresslevel=6, mtime=0
    )
    return raw, gz


def _write_record(handle, key: bytes, data: bytes) -> None:
    handle.write(struct.pack(">II", len(key), len(data)))
    handle.write(key)
    handle.write(data)


def _read_record(handle):
    header = handle.read(8)
    if not header:
        return None
    if len(header) != 8:
        raise R5IntegrityError("truncated compact run header")
    key_length, data_length = struct.unpack(">II", header)
    key = handle.read(key_length)
    data = handle.read(data_length)
    if len(key) != key_length or len(data) != data_length:
        raise R5IntegrityError("truncated compact run record")
    return key, data


class R5CompactLongShardedBuilder:
    def __init__(
        self,
        config: R5BuildConfig | None = None,
        *,
        fault_hook: FaultHook | None = None,
    ) -> None:
        self.config = config or R5BuildConfig()
        self.fault_hook = fault_hook or _noop_fault

    def _flush_run(
        self, directory: Path, index: int, records: list[tuple[bytes, bytes]]
    ) -> Path:
        records.sort(key=lambda x: x[0])
        path = directory / f"run-{index:08d}.tmp.gz"
        raw, gz = _gzip_writer(path)
        try:
            for key, data in records:
                _write_record(gz, key, data)
            gz.close()
            raw.flush()
            os.fsync(raw.fileno())
        finally:
            raw.close()
        return path

    def _make_runs(self, rows, work):
        run_dir = work / "runs-0000"
        run_dir.mkdir()
        manifest = work / "runs-0000.txt"
        index = count = 0
        max_rows = max_bytes = 0
        buffered: list[tuple[bytes, bytes]] = []
        buffered_bytes = 0
        with manifest.open("w", encoding="utf-8", newline="\n") as out:
            for row in rows:
                key = _sort_key(row)
                data = _storage_wire(row)
                size = len(key) + len(data) + 8
                if buffered and (
                    len(buffered) >= self.config.run_max_rows
                    or buffered_bytes + size > self.config.run_max_bytes
                ):
                    path = self._flush_run(run_dir, index, buffered)
                    out.write(path.name + "\n")
                    index += 1
                    max_rows = max(max_rows, len(buffered))
                    max_bytes = max(max_bytes, buffered_bytes)
                    buffered = []
                    buffered_bytes = 0
                buffered.append((key, data))
                buffered_bytes += size
                count += 1
                if (
                    len(buffered) >= self.config.run_max_rows
                    or buffered_bytes >= self.config.run_max_bytes
                ):
                    path = self._flush_run(run_dir, index, buffered)
                    out.write(path.name + "\n")
                    index += 1
                    max_rows = max(max_rows, len(buffered))
                    max_bytes = max(max_bytes, buffered_bytes)
                    buffered = []
                    buffered_bytes = 0
            if buffered:
                path = self._flush_run(run_dir, index, buffered)
                out.write(path.name + "\n")
                index += 1
                max_rows = max(max_rows, len(buffered))
                max_bytes = max(max_bytes, buffered_bytes)
            out.flush()
            os.fsync(out.fileno())
        if not count:
            raise R5Error("R5 canonical release cannot be empty")
        return manifest, {
            "input_rows": count,
            "initial_runs": index,
            "max_buffered_run_rows": max_rows,
            "max_buffered_run_bytes": max_bytes,
        }

    @staticmethod
    def _groups(manifest: Path, fan_in: int):
        with manifest.open("r", encoding="utf-8") as handle:
            group = []
            for raw in handle:
                name = raw.strip()
                if not name:
                    continue
                group.append(name)
                if len(group) >= fan_in:
                    yield group
                    group = []
            if group:
                yield group

    @staticmethod
    def _merge_group(source_dir: Path, names: list[str], target: Path) -> None:
        raws = [(source_dir / name).open("rb") for name in names]
        handles = [gzip.GzipFile(mode="rb", fileobj=raw) for raw in raws]
        try:
            heap = []
            for index, handle in enumerate(handles):
                record = _read_record(handle)
                if record:
                    heapq.heappush(heap, (record[0], index, record[1]))
            raw, gz = _gzip_writer(target)
            try:
                while heap:
                    key, index, data = heapq.heappop(heap)
                    _write_record(gz, key, data)
                    nxt = _read_record(handles[index])
                    if nxt:
                        heapq.heappush(heap, (nxt[0], index, nxt[1]))
                gz.close()
                raw.flush()
                os.fsync(raw.fileno())
            finally:
                raw.close()
        finally:
            for handle in handles:
                handle.close()
            for raw in raws:
                raw.close()

    def _reduce(self, manifest: Path, work: Path):
        source_dir = work / "runs-0000"
        pass_index = 0
        max_open = 1
        while True:
            with manifest.open("r", encoding="utf-8") as handle:
                count = sum(1 for line in handle if line.strip())
            if count <= self.config.merge_fan_in:
                return manifest, source_dir, pass_index, max_open
            pass_index += 1
            target_dir = work / f"runs-{pass_index:04d}"
            target_dir.mkdir()
            next_manifest = work / f"runs-{pass_index:04d}.txt"
            next_count = 0
            with next_manifest.open("w", encoding="utf-8", newline="\n") as out:
                for group in self._groups(manifest, self.config.merge_fan_in):
                    max_open = max(max_open, len(group))
                    target = target_dir / f"run-{next_count:08d}.tmp.gz"
                    self._merge_group(source_dir, group, target)
                    out.write(target.name + "\n")
                    next_count += 1
                out.flush()
                os.fsync(out.fileno())
            shutil.rmtree(source_dir)
            manifest.unlink()
            source_dir, manifest = target_dir, next_manifest

    @staticmethod
    def _iter_final(manifest: Path, source_dir: Path):
        names = [
            line.strip()
            for line in manifest.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        raws = [(source_dir / name).open("rb") for name in names]
        handles = [gzip.GzipFile(mode="rb", fileobj=raw) for raw in raws]
        try:
            heap = []
            for index, handle in enumerate(handles):
                record = _read_record(handle)
                if record:
                    heapq.heappush(heap, (record[0], index, record[1]))
            while heap:
                key, index, data = heapq.heappop(heap)
                yield key, data
                nxt = _read_record(handles[index])
                if nxt:
                    heapq.heappush(heap, (nxt[0], index, nxt[1]))
        finally:
            for handle in handles:
                handle.close()
            for raw in raws:
                raw.close()

    def build(
        self,
        rows,
        *,
        release_identity: R5ReleaseIdentity,
        target_directory,
    ):
        target = Path(target_directory)
        if target.exists():
            raise R5Error("R5 build target must not already exist")
        target.mkdir(parents=True)
        members_dir = target / "members"
        members_dir.mkdir()
        work = target / ".work"
        work.mkdir()
        self.fault_hook("build_start", {"target": str(target)})

        manifest, telemetry = self._make_runs(rows, work)
        manifest, source_dir, passes, max_open = self._reduce(manifest, work)
        telemetry.update(
            {"merge_passes": passes, "max_merge_open_runs": max_open}
        )

        inventory = target / "member_inventory.jsonl"
        inventory_count = shard_index = total_rows = 0
        global_logical = hashlib.sha256()
        previous_identity = None
        current_raw = current_gz = current_path = None
        current_rows = current_uncompressed = 0
        current_first = current_last = None
        current_logical = None
        relation_counts: dict[str, int] = {}
        actual_member_bytes = 0

        with inventory.open("w", encoding="ascii", newline="\n") as inv_handle:
            def close_shard() -> None:
                nonlocal current_raw, current_gz, current_path
                nonlocal current_rows, current_uncompressed
                nonlocal current_first, current_last, current_logical
                nonlocal relation_counts, inventory_count, actual_member_bytes
                if current_gz is None:
                    return
                current_gz.close()
                current_raw.flush()
                os.fsync(current_raw.fileno())
                current_raw.close()
                sha256, byte_length = _sha256_file(current_path)
                actual_member_bytes += byte_length
                descriptor = {
                    "inventory_schema_version": INVENTORY_SCHEMA_VERSION,
                    "member": current_path.name,
                    "member_encoding": MEMBER_ENCODING,
                    "byte_length": byte_length,
                    "sha256": sha256,
                    "logical_digest": current_logical.hexdigest(),
                    "row_count": current_rows,
                    "first_identity": list(current_first),
                    "last_identity": list(current_last),
                    "relation_counts": dict(sorted(relation_counts.items())),
                }
                inv_handle.write(canonical_json(descriptor) + "\n")
                inventory_count += 1
                current_raw = current_gz = current_path = None
                current_rows = current_uncompressed = 0
                current_first = current_last = None
                current_logical = None
                relation_counts = {}

            for key, data in self._iter_final(manifest, source_dir):
                row = _decode_storage(data)
                if key != _sort_key(row):
                    raise R5IntegrityError("temporary run identity mismatch")
                identity = row.identity_key
                if previous_identity is not None and identity <= previous_identity:
                    raise R5IntegrityError(
                        "duplicate/noncanonical exact identity"
                    )
                previous_identity = identity
                if current_gz is not None and (
                    current_rows >= self.config.shard_max_rows
                    or current_uncompressed + len(data) > self.config.shard_max_bytes
                ):
                    close_shard()
                    shard_index += 1
                if current_gz is None:
                    current_path = (
                        members_dir / f"member-{shard_index:08d}.r5z"
                    )
                    current_raw, current_gz = _gzip_writer(current_path)
                    current_first = identity
                    current_logical = hashlib.sha256()
                current_gz.write(data)
                logical_wire = _logical_wire(row)
                current_logical.update(logical_wire)
                global_logical.update(logical_wire)
                current_rows += 1
                current_uncompressed += len(data)
                total_rows += 1
                current_last = identity
                relation_counts[row.relation] = (
                    relation_counts.get(row.relation, 0) + 1
                )
            close_shard()
            inv_handle.flush()
            os.fsync(inv_handle.fileno())

        if total_rows != telemetry["input_rows"]:
            raise R5IntegrityError("row count changed during merge")
        inventory_sha, inventory_bytes = _sha256_file(inventory)
        release_projection = {
            "release_id": release_identity.release_id,
            "semantic_release_hash": release_identity.semantic_release_hash,
            "source_artifact_ref": dict(release_identity.source_artifact_ref),
            "source_release_manifest_hash": release_identity.source_release_manifest_hash,
            "m01_m18_coverage": {
                k: list(v)
                for k, v in sorted(release_identity.m01_m18_coverage.items())
            },
            "decoder_receipt": release_identity.decoder_receipt,
            "compiler_contract_digest": release_identity.compiler_contract_digest,
            "c11_authority_digest": release_identity.c11_authority_digest,
        }
        unsigned_root = {
            "root_schema_version": ROOT_SCHEMA_VERSION,
            "carrier_schema_version": CARRIER_SCHEMA_VERSION,
            "carrier_id": CARRIER_ID,
            "member_encoding": MEMBER_ENCODING,
            "typed_codec_version": CODEC_VERSION,
            "release_identity": release_projection,
            "logical_stream_digest": global_logical.hexdigest(),
            "canonical_row_count": total_rows,
            "member_inventory": {
                "path": inventory.name,
                "sha256": inventory_sha,
                "byte_length": inventory_bytes,
                "member_count": inventory_count,
            },
            "build_config": _config_projection(self.config),
        }
        physical_root_id = hashlib.sha256(
            canonical_bytes(unsigned_root)
        ).hexdigest()
        root = {**unsigned_root, "physical_root_id": physical_root_id}
        root_path = target / "root.json"
        root_path.write_text(
            canonical_json(root) + "\n", encoding="ascii"
        )
        _fsync_file(root_path)
        _fsync_file(inventory)
        _fsync_dir(members_dir)
        _fsync_dir(target)
        self.fault_hook(
            "root_sealed", {"physical_root_id": physical_root_id}
        )
        shutil.rmtree(work)
        root_bytes = root_path.stat().st_size
        steady_state_bytes = actual_member_bytes + inventory_bytes + root_bytes
        telemetry.update(
            {
                "final_shards": inventory_count,
                "canonical_rows": total_rows,
                "physical_root_id": physical_root_id,
                "logical_stream_digest": global_logical.hexdigest(),
                "member_bytes": actual_member_bytes,
                "inventory_bytes": inventory_bytes,
                "root_bytes": root_bytes,
                "canonical_steady_state_bytes": steady_state_bytes,
                "canonical_bytes_per_row": steady_state_bytes / total_rows,
            }
        )
        return telemetry


class R5CompactLongShardedReader:
    ROOT_MAX_BYTES = 2 * 1024 * 1024

    def __init__(
        self,
        release_directory,
        *,
        expected_physical_root_id=None,
        fault_hook=None,
    ) -> None:
        self.release_directory = Path(release_directory)
        self.fault_hook = fault_hook or _noop_fault
        self.quarantined = False
        self.root = self._load_root(expected_physical_root_id)
        self.release_identity = dict(self.root["release_identity"])
        self.config = R5BuildConfig(**self.root["build_config"])

    def _fail(self, message, exc=None):
        self.quarantined = True
        raise R5IntegrityError(message) from exc

    def _require(self) -> None:
        if self.quarantined:
            raise R5QuarantinedError(
                "R5 physical release is quarantined after canonical integrity failure"
            )

    def _load_root(self, expected):
        path = self.release_directory / "root.json"
        try:
            raw = path.read_bytes()
            item = json.loads(raw.decode("ascii"))
        except Exception as exc:
            raise R5IntegrityError(
                "R5 root manifest missing or invalid"
            ) from exc
        if len(raw) > self.ROOT_MAX_BYTES:
            raise R5IntegrityError("root manifest exceeds bounded maximum")
        supplied = item.pop("physical_root_id", None)
        derived = hashlib.sha256(canonical_bytes(item)).hexdigest()
        if supplied != derived or (
            expected is not None and supplied != expected
        ):
            raise R5IntegrityError("R5 physical root identity mismatch")
        if (
            item.get("root_schema_version") != ROOT_SCHEMA_VERSION
            or item.get("carrier_id") != CARRIER_ID
            or item.get("member_encoding") != MEMBER_ENCODING
        ):
            raise R5IntegrityError("R5 root schema/carrier/encoding mismatch")
        return {**item, "physical_root_id": supplied}

    @contextmanager
    def _verified_spool(self, path, expected_hash, expected_length):
        self._require()
        spool = tempfile.SpooledTemporaryFile(
            max_size=self.config.verified_spool_memory_bytes, mode="w+b"
        )
        digest = hashlib.sha256()
        length = 0
        try:
            self.fault_hook("before_verified_read", {"path": str(path)})
            with path.open("rb") as source:
                for block in iter(lambda: source.read(1024 * 1024), b""):
                    digest.update(block)
                    length += len(block)
                    spool.write(block)
            if length != expected_length or digest.hexdigest() != expected_hash:
                self._fail(f"missing or corrupt canonical member {path.name}")
            spool.seek(0)
            self.fault_hook(
                "after_verified_read", {"path": str(path), "length": length}
            )
            yield spool
        except R5IntegrityError:
            raise
        except Exception as exc:
            self._fail(f"canonical member read failed {path.name}", exc)
        finally:
            spool.close()

    def iter_inventory(self):
        self._require()
        info = self.root["member_inventory"]
        path = self.release_directory / info["path"]
        count = 0
        previous = None
        with self._verified_spool(
            path, info["sha256"], info["byte_length"]
        ) as spool:
            for raw in spool:
                try:
                    descriptor = json.loads(raw.decode("ascii"))
                except Exception as exc:
                    self._fail("member inventory row invalid", exc)
                if (
                    descriptor.get("inventory_schema_version")
                    != INVENTORY_SCHEMA_VERSION
                    or descriptor.get("member_encoding") != MEMBER_ENCODING
                ):
                    self._fail("member inventory schema/encoding mismatch")
                member = descriptor.get("member")
                if (
                    not isinstance(member, str)
                    or not member.startswith("member-")
                    or "/" in member
                    or "\\" in member
                ):
                    self._fail("member inventory invalid path")
                if previous is not None and member <= previous:
                    self._fail("member inventory not ordered")
                previous = member
                count += 1
                yield descriptor
        if count != info["member_count"]:
            self._fail("member inventory cardinality mismatch")

    def iter_rows(self, *, relation=None):
        self._require()
        for descriptor in self.iter_inventory():
            path = self.release_directory / "members" / descriptor["member"]
            rows = 0
            logical = hashlib.sha256()
            first = last = None
            relations: dict[str, int] = {}
            with self._verified_spool(
                path, descriptor["sha256"], descriptor["byte_length"]
            ) as spool:
                try:
                    gz = gzip.GzipFile(mode="rb", fileobj=spool)
                    for line in gz:
                        row = _decode_storage(line)
                        logical_wire = _logical_wire(row)
                        logical.update(logical_wire)
                        rows += 1
                        relations[row.relation] = relations.get(row.relation, 0) + 1
                        if first is None:
                            first = row.identity_key
                        last = row.identity_key
                        if relation is None or row.relation == relation:
                            yield row
                    gz.close()
                except R5IntegrityError:
                    raise
                except Exception as exc:
                    self._fail(
                        f"compressed member decode failed {descriptor['member']}",
                        exc,
                    )
            if (
                rows != descriptor["row_count"]
                or logical.hexdigest() != descriptor["logical_digest"]
            ):
                self._fail(
                    f"logical member digest/count mismatch {descriptor['member']}"
                )
            if (
                list(first) != descriptor["first_identity"]
                or list(last) != descriptor["last_identity"]
                or dict(sorted(relations.items()))
                != descriptor["relation_counts"]
            ):
                self._fail(
                    f"member coverage descriptor mismatch {descriptor['member']}"
                )

    def resolve_exact(self, relation, object_id):
        match = None
        for row in self.iter_rows():
            if row.relation == relation and row.object_id == object_id:
                if match is not None:
                    self._fail("exact scan found duplicate object identity")
                match = row
        return match

    def exact_scan(self, predicate):
        for row in self.iter_rows():
            if predicate(row):
                yield row

    def full_audit(self):
        self._require()
        digest = hashlib.sha256()
        rows = 0
        previous = None
        relations: dict[str, int] = {}
        for row in self.iter_rows():
            if previous is not None and row.identity_key <= previous:
                self._fail(
                    "full audit found duplicate/noncanonical row order"
                )
            previous = row.identity_key
            digest.update(_logical_wire(row))
            rows += 1
            relations[row.relation] = relations.get(row.relation, 0) + 1
        if (
            rows != self.root["canonical_row_count"]
            or digest.hexdigest() != self.root["logical_stream_digest"]
        ):
            self._fail("full audit semantic stream digest/count mismatch")
        return {
            "physical_root_id": self.root["physical_root_id"],
            "canonical_rows": rows,
            "logical_stream_digest": digest.hexdigest(),
            "relation_counts": dict(sorted(relations.items())),
        }


R5LongShardedBuilder = R5CompactLongShardedBuilder
R5LongShardedReader = R5CompactLongShardedReader

__all__ = [
    "CARRIER_SCHEMA_VERSION",
    "MEMBER_ENCODING",
    "R5CompactLongShardedBuilder",
    "R5CompactLongShardedReader",
    "R5LongShardedBuilder",
    "R5LongShardedReader",
    "R5BuildConfig",
    "R5ReleaseIdentity",
    "R5CanonicalRow",
]
