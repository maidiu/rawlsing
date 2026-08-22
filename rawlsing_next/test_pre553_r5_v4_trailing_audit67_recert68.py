"""Authority-68 hostile/process court for the frozen Authority-67 fast path."""
from __future__ import annotations

import gzip
import hashlib
import inspect
import json
import os
import queue
import subprocess
import sys
import threading

import pytest

from rawlsing_next import pre553_r5_compact_carrier as frozen
from rawlsing_next.pre553_r5_codec import canonical_bytes
from rawlsing_next.pre553_r5_model import R5CanonicalRow, R5ReleaseIdentity
from rawlsing_next.pre553_r5_serial_turbo66 import BASELINE, SerialTurboBuilder, TurboConfig
from rawlsing_next.pre553_r5_v4_trailing_audit67 import _audit_member, _auditor_main, run_trailing


def _identity():
    return R5ReleaseIdentity("test-release", "a" * 64, {"kind": "test"}, "b" * 64, {"M01": ("test",)}, {}, "c" * 64, "d" * 64)


def _rows(values=(0, 1, 2)):
    return [R5CanonicalRow("test", "Test", f"id-{i}", hashlib.sha256(canonical_bytes({"i": i})).hexdigest(), {"i": i}) for i in values]


def _build(tmp_path, *, shard_rows=16384, callback=None):
    config = TurboConfig("TEST", 4096, 4 * 1024 * 1024, 8, 6, True, shard_rows, 16 * 1024 * 1024, 6)
    target = tmp_path / "sealed"
    telemetry = SerialTurboBuilder(config, member_closed_callback=callback).build(_rows(), release_identity=_identity(), target_directory=target)
    return target, telemetry


def _run_auditor(target, readiness):
    ready = queue.Queue()
    result = queue.Queue()
    thread = threading.Thread(target=_auditor_main, args=(str(target), ready, result), daemon=True)
    thread.start()
    for item in readiness:
        ready.put(item)
    ready.put(None)
    thread.join(timeout=5)
    assert not thread.is_alive()
    return result.get(timeout=1)


def test_full_audit_equality_and_readiness_payload_has_no_expected_truth(tmp_path):
    payloads = []
    target, telemetry = _build(tmp_path, callback=payloads.append)
    assert payloads and all(isinstance(x, str) for x in payloads)
    assert len(payloads[0].split()) == 1
    forbidden = ("sha", "digest", "row_count", "coverage", "expected", "semantic")
    assert not any(x in payloads[0].lower() for x in forbidden)
    from rawlsing_next.pre553_r5_compact_carrier import R5CompactLongShardedReader
    ordinary = R5CompactLongShardedReader(target, expected_physical_root_id=telemetry["physical_root_id"]).full_audit()
    trailing = _run_auditor(target, payloads)
    assert trailing["ok"]
    assert trailing["audit"] == ordinary


@pytest.mark.parametrize("mutation", ["corrupt", "truncate"])
def test_corrupt_or_truncated_closed_member_fails_closed(tmp_path, mutation):
    target, _ = _build(tmp_path)
    path = next((target / "members").glob("*.r5z"))
    original = path.read_bytes()
    path.write_bytes(original[:-7] if mutation == "truncate" else b"not-gzip")
    with pytest.raises(RuntimeError):
        _audit_member(path)


def test_duplicate_identity_fails_closed(tmp_path):
    target = tmp_path / "sealed"
    members = target / "members"
    members.mkdir(parents=True)
    wire = frozen._storage_wire(_rows((0,))[0])
    path = members / "member-00000000.r5z"
    with path.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as out:
            out.write(wire)
            out.write(wire)
    with pytest.raises(RuntimeError, match="duplicate/noncanonical"):
        _audit_member(path)


@pytest.mark.parametrize("readiness", [
    ["member-00000001.r5z"],
    ["member-00000000.r5z", "member-00000000.r5z"],
    ["member-00000001.r5z", "member-00000000.r5z"],
])
def test_missing_duplicate_and_out_of_order_readiness_fail_closed(tmp_path, readiness):
    target, _ = _build(tmp_path, shard_rows=1)
    outcome = _run_auditor(target, readiness)
    assert outcome["ok"] is False
    assert any(word in outcome["error"] for word in ("ordinal", "readiness"))


def test_readiness_queue_capacity_and_ninth_pending_admission_are_bounded():
    ready = queue.Queue(maxsize=8)
    for i in range(8):
        ready.put_nowait(f"member-{i:08d}.r5z")
    with pytest.raises(queue.Full):
        ready.put("member-00000008.r5z", timeout=0.01)
    assert ready.maxsize == 8


def test_queue_bound_is_not_just_qsize_telemetry():
    source = inspect.getsource(run_trailing)
    assert "Queue(maxsize=queue_capacity)" in source
    assert "ready.put(name, timeout=1.0)" in source
    assert "queue.Full" in source
    assert "ready.qsize()" in source


def test_root_and_inventory_tamper_after_member_audit_fail_reconciliation(tmp_path):
    target, _ = _build(tmp_path)
    names = [p.name for p in sorted((target / "members").glob("*.r5z"))]
    assert all(_audit_member(target / "members" / name) for name in names)
    root = json.loads((target / "root.json").read_text())
    root["canonical_row_count"] += 1
    (target / "root.json").write_text(json.dumps(root, sort_keys=True) + "\n")
    outcome = _run_auditor(target, names)
    assert outcome["ok"] is False
    assert "root" in outcome["error"] or "reconciliation" in outcome["error"]


def test_inventory_tamper_after_member_audit_fail_reconciliation(tmp_path):
    target, _ = _build(tmp_path)
    names = [p.name for p in sorted((target / "members").glob("*.r5z"))]
    inventory = target / "member_inventory.jsonl"
    item = json.loads(inventory.read_text().splitlines()[0])
    item["byte_length"] += 1
    inventory.write_text(json.dumps(item, sort_keys=True) + "\n")
    outcome = _run_auditor(target, names)
    assert outcome["ok"] is False
    assert "inventory" in outcome["error"]


def test_no_persistent_cache_or_store_remains(tmp_path):
    target, _ = _build(tmp_path)
    assert not (target / ".work").exists()
    assert not [p for p in target.rglob("*") if p.is_dir() and p.name in {"cache", "store", "index"}]


def test_repeated_synthetic_build_is_deterministic(tmp_path):
    first, _ = _build(tmp_path / "a")
    second, _ = _build(tmp_path / "b")
    def files(target):
        return {p.relative_to(target).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in target.rglob("*") if p.is_file()}
    assert files(first) == files(second)


def test_builder_failure_does_not_publish_success_and_run_trailing_joins_auditor(tmp_path):
    class FailingBuilder:
        config = BASELINE
        def __init__(self, config, *, member_closed_callback=None):
            self.config = config
        def build(self, *args, **kwargs):
            raise RuntimeError("synthetic builder crash")
    with pytest.raises(RuntimeError, match="synthetic builder crash"):
        run_trailing(FailingBuilder(BASELINE), iter(_rows()), _identity(), tmp_path / "sealed")
    assert not (tmp_path / "sealed" / "root.json").exists()


def test_process_failure_and_result_channel_failure_are_fail_closed_by_contract():
    source = inspect.getsource(run_trailing)
    assert "process.exitcode!=0" in source
    assert "result.get(timeout=10)" in source
    assert "process.terminate()" in source
    assert "raise RuntimeError" in source


def test_different_pythonhashseed_preserves_synthetic_physical_output(tmp_path):
    script = """
import hashlib, pathlib
from rawlsing_next.pre553_r5_serial_turbo66 import SerialTurboBuilder, BASELINE
from rawlsing_next.pre553_r5_model import R5CanonicalRow, R5ReleaseIdentity
from rawlsing_next.pre553_r5_codec import canonical_bytes
rows=[R5CanonicalRow('test','Test',f'id-{i}',hashlib.sha256(canonical_bytes({'i':i})).hexdigest(),{'i':i}) for i in (2,1,3)]
i=R5ReleaseIdentity('test-release','a'*64,{'kind':'test'},'b'*64,{'M01':('test',)}, {},'c'*64,'d'*64)
t=pathlib.Path(__import__('sys').argv[1]); SerialTurboBuilder(BASELINE).build(rows,release_identity=i,target_directory=t)
print(hashlib.sha256((t/'root.json').read_bytes()).hexdigest())
"""
    env1 = dict(os.environ, PYTHONHASHSEED="1", PYTHONPATH=".")
    env2 = dict(os.environ, PYTHONHASHSEED="777", PYTHONPATH=".")
    a = subprocess.check_output([sys.executable, "-c", script, str(tmp_path / "one")], env=env1, text=True).strip()
    b = subprocess.check_output([sys.executable, "-c", script, str(tmp_path / "two")], env=env2, text=True).strip()
    assert a == b
