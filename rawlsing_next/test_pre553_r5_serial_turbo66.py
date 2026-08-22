import hashlib
from pathlib import Path

import pytest

from rawlsing_next.pre553_r5_codec import canonical_bytes
from rawlsing_next.pre553_r5_model import R5CanonicalRow, R5ReleaseIdentity, R5IntegrityError
from rawlsing_next.pre553_r5_serial_turbo66 import (
    BASELINE, FREE_SPACE_HARD_ABORT, RSS_HARD_ABORT, SCRATCH_HARD_ABORT,
    SerialTurboBuilder, TurboConfig, actual_fan_in, filesystem_action, rss_action,
    scratch_action,
)


def test_authority_66_variants_are_single_process_and_baseline_root_is_explicit():
    assert BASELINE.temp_fsync is True
    assert BASELINE.temp_level == 6
    assert BASELINE.baseline_layout is True
    assert TurboConfig("V5", 65536, 64 * 2**20, 64, None, False, 16384, 16 * 2**20, 6).temp_level is None


def test_authority_66_final_relayout_is_explicit():
    v6 = TurboConfig("V6B", 65536, 64 * 2**20, 64, 1, False, 524288, 512 * 2**20, 6, False)
    assert v6.baseline_layout is False
    assert v6.shard_max_rows == 524288
    assert v6.final_level == 6


def test_safety_governor_boundaries_without_allocating_memory():
    assert rss_action(0) == "NORMAL"
    assert rss_action(2 * 1024**3) == "ALLOWED_SLOW_BAND"
    assert rss_action(3 * 1024**3) == "STOP_DISPATCH"
    assert rss_action(RSS_HARD_ABORT) == "HARD_ABORT"
    assert scratch_action(4 * 1024**3) == "WARNING"
    assert scratch_action(SCRATCH_HARD_ABORT) == "HARD_ABORT"
    assert filesystem_action(FREE_SPACE_HARD_ABORT - 1) == "HARD_ABORT"


def test_rlimit_fan_in_reserves_runtime_descriptors_without_raising_limit():
    assert actual_fan_in(64, soft_limit=128) == 64
    assert actual_fan_in(128, soft_limit=128) == 64
    assert actual_fan_in(128, soft_limit=80) == 16


def _identity():
    return R5ReleaseIdentity("test-release", "a" * 64, {"kind": "test"}, "b" * 64, {"M01": ("test",)}, {}, "c" * 64, "d" * 64)


def _rows():
    return [R5CanonicalRow("test", "Test", f"id-{i}", hashlib.sha256(canonical_bytes({"i": i})).hexdigest(), {"i": i}) for i in (2, 1, 3)]


def _build(tmp_path: Path, cfg: TurboConfig):
    target = tmp_path / cfg.name
    return target, SerialTurboBuilder(cfg).build(_rows(), release_identity=_identity(), target_directory=target)


def test_temp_gzip6_gzip1_and_raw_have_identical_baseline_final_output(tmp_path):
    configs = [
        TurboConfig("gzip6", 65536, 64 * 2**20, 64, 6, False, 16384, 16 * 2**20, 6, True),
        TurboConfig("gzip1", 65536, 64 * 2**20, 64, 1, False, 16384, 16 * 2**20, 6, True),
        TurboConfig("raw", 65536, 64 * 2**20, 64, None, False, 16384, 16 * 2**20, 6, True),
    ]
    outputs = []
    for cfg in configs:
        target, _ = _build(tmp_path, cfg)
        outputs.append({p.relative_to(target): p.read_bytes() for p in sorted(target.rglob("*")) if p.is_file() and ".work" not in p.parts})
    assert outputs[0] == outputs[1] == outputs[2]


def test_duplicate_identity_is_rejected_and_no_root_is_sealed(tmp_path):
    row = _rows()[0]
    target = tmp_path / "duplicate"
    with pytest.raises(R5IntegrityError):
        SerialTurboBuilder(BASELINE).build([row, row], release_identity=_identity(), target_directory=target)
    assert not (target / "root.json").exists()


def test_corrupt_temp_record_fails_closed():
    from rawlsing_next.pre553_r5_serial_turbo66 import _read_record
    with pytest.raises(R5IntegrityError):
        _read_record(__import__("io").BytesIO(b"\x00\x00"))


def test_success_cleanup_removes_disposable_work_and_repeated_runs_are_deterministic(tmp_path):
    first, _ = _build(tmp_path, TurboConfig("deterministic-a", 2, 4096, 2, 1, False, 16384, 16 * 2**20, 6, True))
    second, _ = _build(tmp_path, TurboConfig("deterministic-b", 2, 4096, 2, 1, False, 16384, 16 * 2**20, 6, True))
    assert not (first / ".work").exists()
    assert (first / "root.json").read_bytes() == (second / "root.json").read_bytes()
    assert (first / "member_inventory.jsonl").read_bytes() == (second / "member_inventory.jsonl").read_bytes()


def test_fsync_failure_before_root_closure_cannot_publish_root(tmp_path, monkeypatch):
    import rawlsing_next.pre553_r5_serial_turbo66 as turbo
    def fail(_path, _enabled):
        raise OSError("injected temporary durability failure")
    monkeypatch.setattr(turbo, "_fsync", fail)
    target = tmp_path / "fsync-failure"
    with pytest.raises(OSError):
        SerialTurboBuilder(BASELINE).build(_rows(), release_identity=_identity(), target_directory=target)
    assert not (target / "root.json").exists()
