"""Bounded LONG_SHARDED R5 shadow carrier.

The carrier is deliberately flat and disposable: canonical rows are written as
independently closed JSONL members, with a streamed inventory and one immutable
root manifest.  It is not a serving or fallback implementation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import os
import tempfile
from typing import Any, Callable, Iterable, Iterator, Mapping

from rawlsing_next.pre553_r5_codec import R5TypedValueCodec, canonical_bytes
from rawlsing_next.pre553_r5_model import (CARRIER_ID, INVENTORY_SCHEMA_VERSION,
    ROOT_SCHEMA_VERSION, R5BuildConfig, R5CanonicalRow, R5IntegrityError,
    R5QuarantinedError)


def _row_dict(row: R5CanonicalRow) -> dict[str, Any]:
    return {"relation": row.relation, "object_family": row.object_family,
            "object_id": row.object_id, "content_hash": row.content_hash,
            "payload": row.payload}


def _row_from(value: Mapping[str, Any]) -> R5CanonicalRow:
    try:
        return R5CanonicalRow(str(value["relation"]), str(value["object_family"]),
            str(value["object_id"]), str(value["content_hash"]), value["payload"])
    except (KeyError, TypeError) as exc:
        raise R5IntegrityError("malformed canonical row") from exc


def _sha(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256(); size = 0
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block); size += len(block)
    return digest.hexdigest(), size


@dataclass(frozen=True)
class R5Member:
    name: str
    sha256: str
    byte_length: int
    row_count: int
    first_key: tuple[str, str, str] | None
    last_key: tuple[str, str, str] | None


class R5LongShardedWriter:
    """Serial bounded writer.  It retains only the active member counters."""
    def __init__(self, root: str | Path, *, release_identity: Mapping[str, Any],
                 config: R5BuildConfig | None = None, codec: R5TypedValueCodec | None = None):
        self.root = Path(root); self.config = config or R5BuildConfig(); self.codec = codec or R5TypedValueCodec()
        self.release_identity = dict(release_identity); self._members: list[R5Member] = []
        self._handle = None; self._path: Path | None = None; self._count = 0; self._bytes = 0
        self._first = None; self._last = None; self._closed = False
        self.root.mkdir(parents=True, exist_ok=False)
        (self.root / "members").mkdir()

    @property
    def members(self) -> tuple[R5Member, ...]: return tuple(self._members)

    def _open(self) -> None:
        name = f"member-{len(self._members):08d}.jsonl"
        self._path = self.root / "members" / name
        self._handle = self._path.open("wb"); self._count = self._bytes = 0
        self._first = self._last = None

    def _seal(self) -> None:
        if self._handle is None or self._path is None: return
        self._handle.flush(); os.fsync(self._handle.fileno()); self._handle.close()
        digest, length = _sha(self._path)
        self._members.append(R5Member(self._path.relative_to(self.root).as_posix(), digest,
            length, self._count, self._first, self._last))
        self._handle = self._path = None

    def add(self, row: R5CanonicalRow) -> None:
        if self._closed: raise R5IntegrityError("writer is closed")
        if not isinstance(row, R5CanonicalRow): raise R5IntegrityError("canonical row required")
        encoded = canonical_bytes(_row_dict(row)) + b"\n"
        if self._handle is None: self._open()
        if self._count and (self._count >= self.config.shard_max_rows or
                            self._bytes + len(encoded) > self.config.shard_max_bytes):
            self._seal(); self._open()
        self._handle.write(encoded); self._count += 1; self._bytes += len(encoded)
        key = row.identity_key
        if self._first is None: self._first = key
        self._last = key

    def extend(self, rows: Iterable[R5CanonicalRow]) -> None:
        for row in rows: self.add(row)

    def close(self) -> Path:
        if self._closed: return self.root / "root.json"
        self._seal()
        inventory = self.root / "inventory.jsonl"
        with inventory.open("wb") as handle:
            for member in self._members:
                handle.write(canonical_bytes(asdict(member)) + b"\n")
        inv_sha, inv_len = _sha(inventory)
        manifest = {"schema": ROOT_SCHEMA_VERSION, "carrier": CARRIER_ID,
            "release_identity": self.release_identity,
            "semantic_release_id": self.release_identity.get("release_id"),
            "physical_root_id": None, "inventory": {"path": "inventory.jsonl", "sha256": inv_sha, "byte_length": inv_len,
                "member_count": len(self._members)}, "members": [asdict(m) for m in self._members]}
        manifest["physical_root_id"] = hashlib.sha256(canonical_bytes(manifest)).hexdigest()
        root = self.root / "root.json"; root.write_bytes(canonical_bytes(manifest) + b"\n")
        self._closed = True
        return root


class R5LongShardedReader:
    def __init__(self, root: str | Path, *, verify: bool = True):
        self.root = Path(root); self.quarantined = False
        try:
            self.manifest = json.loads((self.root / "root.json").read_text())
            if self.manifest.get("schema") != ROOT_SCHEMA_VERSION or self.manifest.get("carrier") != CARRIER_ID:
                raise R5IntegrityError("root schema/carrier mismatch")
            if verify: self._verify()
        except Exception as exc:
            self.quarantined = True
            if isinstance(exc, R5IntegrityError): raise
            raise R5IntegrityError("sealed root cannot be opened") from exc

    @property
    def release_identity(self) -> Mapping[str, Any]: return self.manifest["release_identity"]
    @property
    def physical_root_id(self) -> str: return self.manifest["physical_root_id"]

    def _verify(self) -> None:
        inventory = self.root / self.manifest["inventory"]["path"]
        if _sha(inventory) != (self.manifest["inventory"]["sha256"], self.manifest["inventory"]["byte_length"]):
            raise R5IntegrityError("inventory hash/length mismatch")
        for item in self.manifest["members"]:
            path = self.root / item["name"]
            if not path.exists() or _sha(path) != (item["sha256"], item["byte_length"]):
                raise R5IntegrityError("member hash/length mismatch")

    def iter_rows(self, *, relation: str | None = None) -> Iterator[R5CanonicalRow]:
        if self.quarantined: raise R5QuarantinedError("quarantined root")
        for item in self.manifest["members"]:
            with (self.root / item["name"]).open() as handle:
                for line in handle:
                    row = _row_from(json.loads(line))
                    if relation is None or row.relation == relation: yield row

    def resolve_exact(self, relation: str, object_id: str) -> R5CanonicalRow | None:
        for row in self.iter_rows(relation=relation):
            if row.object_id == object_id: return row
        return None

    def scan(self, predicate: Callable[[R5CanonicalRow], bool]) -> Iterator[R5CanonicalRow]:
        yield from (row for row in self.iter_rows() if predicate(row))


def audit_root(root: str | Path) -> dict[str, Any]:
    reader = R5LongShardedReader(root, verify=True); rows = 0; relations: dict[str, int] = {}
    for row in reader.iter_rows(): rows += 1; relations[row.relation] = relations.get(row.relation, 0) + 1
    return {"physical_root_id": reader.physical_root_id, "member_count": len(reader.manifest["members"]),
            "row_count": rows, "relations": dict(sorted(relations.items())), "status": "PASS"}


class R5PublicationCAS:
    """Isolated generation-stamped selector simulator; no production switch."""
    def __init__(self): self.generation = 0; self.active: tuple[str, str] | None = None
    def publish_inactive(self, semantic_release_id: str, physical_root_id: str) -> int:
        if not semantic_release_id or not physical_root_id: raise R5IntegrityError("publication binding required")
        return self.generation + 1
    def compare_and_swap(self, expected_generation: int, semantic_release_id: str, physical_root_id: str) -> int:
        if expected_generation != self.generation: raise R5IntegrityError("stale publication generation")
        self.generation += 1; self.active = (semantic_release_id, physical_root_id); return self.generation
    def require(self, generation: int, root: str) -> None:
        if generation != self.generation or self.active is None or self.active[1] != root:
            raise R5IntegrityError("query root pin/generation mismatch")


__all__ = ["R5Member", "R5LongShardedWriter", "R5LongShardedReader", "audit_root", "R5PublicationCAS"]
