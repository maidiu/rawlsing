"""Authority-69 hostile equivalence tests for the additive single-pass audit."""
from __future__ import annotations

import gzip
import hashlib
import json
import os
import subprocess
import sys

import pytest

from rawlsing_next import pre553_r5_compact_carrier as frozen
from rawlsing_next.pre553_r5_codec import canonical_bytes, canonical_json
from rawlsing_next.pre553_r5_compact_carrier import R5LongShardedBuilder, R5LongShardedReader
from rawlsing_next.pre553_r5_model import R5BuildConfig, R5CanonicalRow, R5IntegrityError, R5QuarantinedError, R5ReleaseIdentity
from rawlsing_next.pre553_r5_single_pass_audit69 import single_pass_full_audit


def _hash(value):
    return hashlib.sha256(value.encode()).hexdigest()


def _identity(tag="x"):
    return R5ReleaseIdentity(
        f"REL-{tag}", _hash(f"semantic:{tag}"), {"kind": "SOURCE_ARTIFACT", "object_id": f"src:{tag}", "content_hash": _hash(f"source:{tag}")},
        _hash(f"manifest:{tag}"), {f"M{i:02d}": (f"proof-{i}",) for i in range(1, 19)}, {"decoder": "frozen"}, _hash("compiler"), _hash("c11"),
    )


def _rows(n=12):
    for i in range(n):
        payload = {"i": i, "state": "OBSERVED" if i % 2 else "MISSING"}
        yield R5CanonicalRow("relation_a" if i % 2 else "relation_b", "Family@1", f"id-{i:04d}", _hash(canonical_json(payload)), payload)


def _config(**changes):
    base = dict(run_max_rows=3, run_max_bytes=700, shard_max_rows=100, shard_max_bytes=16000, merge_fan_in=2, verified_spool_memory_bytes=128)
    base.update(changes)
    return R5BuildConfig(**base)


def _build(tmp_path, *, rows=12, config=None):
    target = tmp_path / "release"
    telemetry = R5LongShardedBuilder(config or _config()).build(_rows(rows), release_identity=_identity(), target_directory=target)
    return target, telemetry


def _single(target, expected=None):
    reader = R5LongShardedReader(target, expected_physical_root_id=expected)
    return reader, single_pass_full_audit(reader)


def _rebind(target, *, inventory=None, root_changes=None):
    root = json.loads((target / "root.json").read_text())
    if inventory is not None:
        (target / "member_inventory.jsonl").write_bytes(inventory)
        root["member_inventory"]["sha256"] = hashlib.sha256(inventory).hexdigest()
        root["member_inventory"]["byte_length"] = len(inventory)
    if root_changes:
        root.update(root_changes)
    root.pop("physical_root_id", None)
    root["physical_root_id"] = hashlib.sha256(canonical_bytes(root)).hexdigest()
    (target / "root.json").write_text(canonical_json(root) + "\n")


def _inventory_items(target):
    return [json.loads(line) for line in (target / "member_inventory.jsonl").read_text().splitlines()]


def _write_inventory(target, items):
    return ("\n".join(canonical_json(item) for item in items) + "\n").encode()


def test_single_pass_equals_full_audit_and_calls_logical_wire_once_per_row(tmp_path):
    target, telemetry = _build(tmp_path)
    ordinary = R5LongShardedReader(target, expected_physical_root_id=telemetry["physical_root_id"]).full_audit()
    calls = []
    def counted(row):
        calls.append(row.identity_key)
        return frozen._logical_wire(row)
    actual = single_pass_full_audit(R5LongShardedReader(target, expected_physical_root_id=telemetry["physical_root_id"]), logical_wire=counted)
    assert actual == ordinary
    assert len(calls) == ordinary["canonical_rows"]
    assert len(set(calls)) == ordinary["canonical_rows"]


@pytest.mark.parametrize("mutation", ["corrupt", "truncate"])
def test_corrupt_or_truncated_member_fails_closed(tmp_path, mutation):
    target, _ = _build(tmp_path)
    path = next((target / "members").glob("*.r5z"))
    data = path.read_bytes()
    path.write_bytes(b"not-gzip" if mutation == "corrupt" else data[:-7])
    with pytest.raises(R5IntegrityError):
        _single(target)


def test_member_hash_and_length_mismatch_fail_before_consumption(tmp_path):
    target, _ = _build(tmp_path)
    items = _inventory_items(target)
    items[0]["sha256"] = "0" * 64
    items[0]["byte_length"] += 1
    _rebind(target, inventory=_write_inventory(target, items))
    with pytest.raises(R5IntegrityError):
        _single(target)


@pytest.mark.parametrize("change", ["cardinality", "order", "schema"])
def test_inventory_cardinality_order_schema_mismatch_fails_closed(tmp_path, change):
    target, _ = _build(tmp_path, config=_config(shard_max_rows=3))
    items = _inventory_items(target)
    if change == "cardinality":
        items.pop()
        root_changes = {"member_inventory": {**json.loads((target / "root.json").read_text())["member_inventory"], "member_count": len(items)}}
    elif change == "order":
        items = list(reversed(items))
        root_changes = None
    else:
        items[0]["inventory_schema_version"] = "bad"
        root_changes = None
    inventory = _write_inventory(target, items)
    _rebind(target, inventory=inventory)
    if root_changes:
        root = json.loads((target / "root.json").read_text())
        root.update(root_changes)
        root.pop("physical_root_id", None)
        root["physical_root_id"] = hashlib.sha256(canonical_bytes(root)).hexdigest()
        (target / "root.json").write_text(canonical_json(root) + "\n")
    with pytest.raises(R5IntegrityError):
        _single(target)


@pytest.mark.parametrize("field", ["logical_digest", "row_count", "first_identity", "last_identity", "relation_counts"])
def test_member_descriptor_mismatch_fails_closed(tmp_path, field):
    target, _ = _build(tmp_path)
    items = _inventory_items(target)
    if field == "logical_digest":
        items[0][field] = "0" * 64
    elif field == "row_count":
        items[0][field] += 1
    elif field in {"first_identity", "last_identity"}:
        items[0][field] = ["wrong", "wrong", "wrong", "wrong"]
    else:
        items[0][field] = {"wrong": 1}
    _rebind(target, inventory=_write_inventory(target, items))
    with pytest.raises(R5IntegrityError):
        _single(target)


@pytest.mark.parametrize("field", ["canonical_row_count", "logical_stream_digest"])
def test_global_root_semantic_mismatch_fails_closed(tmp_path, field):
    target, _ = _build(tmp_path)
    root = json.loads((target / "root.json").read_text())
    root[field] = (root[field] + 1) if field == "canonical_row_count" else "0" * 64
    _rebind(target, root_changes={field: root[field]})
    with pytest.raises(R5IntegrityError):
        _single(target)


def test_root_self_hash_and_expected_root_mismatch_fail_closed(tmp_path):
    target, telemetry = _build(tmp_path)
    root = json.loads((target / "root.json").read_text())
    root["canonical_row_count"] += 1
    (target / "root.json").write_text(canonical_json(root) + "\n")
    with pytest.raises(R5IntegrityError):
        _single(target)
    target, telemetry = _build(tmp_path / "second")
    with pytest.raises(R5IntegrityError):
        _single(target, expected="0" * 64)


def test_duplicate_global_order_fails_closed(tmp_path):
    target, _ = _build(tmp_path, rows=4)
    path = next((target / "members").glob("*.r5z"))
    with gzip.GzipFile(fileobj=path.open("rb"), mode="rb") as gz:
        lines = list(gz)
    with path.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz:
            gz.writelines([lines[0], lines[0], *lines[1:]])
    items = _inventory_items(target)
    row0 = frozen._decode_storage(lines[0])
    items[0].update({"byte_length": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "row_count": len(lines) + 1, "logical_digest": hashlib.sha256(b"".join(frozen._logical_wire(frozen._decode_storage(x)) for x in [lines[0], lines[0], *lines[1:]])).hexdigest(), "first_identity": list(row0.identity_key), "last_identity": list(frozen._decode_storage(lines[-1]).identity_key)})
    _rebind(target, inventory=_write_inventory(target, items))
    with pytest.raises(R5IntegrityError):
        _single(target)


def test_quarantine_after_single_pass_failure_is_preserved(tmp_path):
    target, _ = _build(tmp_path)
    path = next((target / "members").glob("*.r5z"))
    path.write_bytes(path.read_bytes()[:-1])
    reader = R5LongShardedReader(target)
    with pytest.raises(R5IntegrityError):
        single_pass_full_audit(reader)
    assert reader.quarantined
    with pytest.raises(R5QuarantinedError):
        single_pass_full_audit(reader)


def test_repeated_runs_and_different_hashseed_are_deterministic(tmp_path):
    left, _ = _build(tmp_path / "left")
    right, _ = _build(tmp_path / "right")
    assert (left / "root.json").read_bytes() == (right / "root.json").read_bytes()
    assert (left / "member_inventory.jsonl").read_bytes() == (right / "member_inventory.jsonl").read_bytes()
    code = """import hashlib, json, pathlib
from rawlsing_next.pre553_r5_single_pass_audit69 import single_pass_full_audit
from rawlsing_next.pre553_r5_compact_carrier import R5LongShardedReader
p=pathlib.Path(__import__('sys').argv[1]); print(json.dumps(single_pass_full_audit(R5LongShardedReader(p)), sort_keys=True))
"""
    outputs = []
    for seed in ("1", "777"):
        env = dict(os.environ, PYTHONHASHSEED=seed, PYTHONPATH=".")
        outputs.append(subprocess.check_output([sys.executable, "-c", code, str(left)], env=env, text=True))
    assert outputs[0] == outputs[1]


def test_no_persistent_cache_or_store(tmp_path):
    target, _ = _build(tmp_path)
    assert not [p for p in target.rglob("*") if p.is_dir() and p.name in {"cache", "store", "index", "bitmap", "matrix"}]
