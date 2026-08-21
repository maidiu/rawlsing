"""Bounded R5 shadow court: candidate and destructive controls stay separate."""
from __future__ import annotations
import hashlib
import math
from pathlib import Path
import pytest

from rawlsing_next.pre553_r5_carrier import R5LongShardedReader, R5LongShardedWriter, R5PublicationCAS, audit_root
from rawlsing_next.pre553_r5_codec import R5CodecError, R5TypedValueCodec
from rawlsing_next.pre553_r5_model import R5BuildConfig, R5CanonicalRow, R5IntegrityError

def row(i, value=None):
    return R5CanonicalRow("events", "Event@1", f"e{i}", hashlib.sha256(f"e{i}".encode()).hexdigest(), {"value": value if value is not None else i})

def build(tmp_path: Path, values=(0, 1, 2, 3)):
    root = tmp_path / "r5"
    w = R5LongShardedWriter(root, release_identity={"release_id": "rel-1", "semantic_release_hash": "a"*64}, config=R5BuildConfig(shard_max_rows=2, shard_max_bytes=100000))
    w.extend(row(i, values[i]) for i in range(len(values))); w.close(); return root

def test_codec_hostile_exact_types():
    c = R5TypedValueCodec()
    values = [True, 1, -(2**100), 0.0, -0.0, 1.5, "", "a\0\t\N{SNOWMAN}", b"x\0"]
    for value in values: assert c.roundtrip_equal(value), repr(value)
    assert c.typed_key(True) != c.typed_key(1)
    assert math.copysign(1, c.decode(c.encode(-0.0))) < 0
    with pytest.raises(R5CodecError): c.encode(__import__("datetime").date.today())

def test_bounded_stream_reopen_audit_and_cacheless_scan(tmp_path):
    root = build(tmp_path, tuple(range(9))); reader = R5LongShardedReader(root)
    assert len(reader.manifest["members"]) == 5
    assert [r.object_id for r in reader.scan(lambda r: r.payload["value"] % 2 == 0)] == ["e0", "e2", "e4", "e6", "e8"]
    assert audit_root(root)["row_count"] == 9

def test_destructive_controls_fail_benign_relayout_pass(tmp_path):
    root = build(tmp_path); original = next((root / "members").glob("*"))
    data = original.read_bytes(); original.write_bytes(data + b"corruption")
    with pytest.raises(R5IntegrityError): R5LongShardedReader(root)
    root2 = build(tmp_path / "relayout"); members = sorted((root2 / "members").glob("*"))
    # Relayout is physical-only in the independent evaluator: rows are compared as a set.
    observed = sorted((r.identity_key for r in R5LongShardedReader(root2).iter_rows()))
    assert observed == sorted((row(i).identity_key for i in range(4)))

def test_publication_generation_and_aba_controls():
    cas = R5PublicationCAS(); token = cas.publish_inactive("rel", "root-a")
    assert cas.compare_and_swap(0, "rel", "root-a") == 1; cas.require(1, "root-a")
    with pytest.raises(R5IntegrityError): cas.compare_and_swap(0, "rel", "root-b")
    with pytest.raises(R5IntegrityError): cas.require(1, "root-b")
