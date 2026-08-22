import hashlib
from pathlib import Path

from rawlsing_next.pre553_r5_codec import canonical_bytes
from rawlsing_next.pre553_r5_model import R5CanonicalRow, R5ReleaseIdentity
from rawlsing_next.pre553_r5_serial_turbo66 import SerialTurboBuilder, TurboConfig
from rawlsing_next.pre553_r5_trailing_audit67 import QUEUE_MAX, ReadinessTelemetry, _audit_member


def _identity():
    return R5ReleaseIdentity("t", "a"*64, {"x":"y"}, "b"*64, {"M01":("x",)}, {}, "c"*64, "d"*64)


def _rows():
    return [R5CanonicalRow("test", "Test", f"id-{i}", hashlib.sha256(canonical_bytes({"i":i})).hexdigest(), {"i":i}) for i in range(6, 0, -1)]


def test_member_ready_hook_receives_only_ordinal_and_name_after_closed_member(tmp_path):
    got=[]
    cfg=TurboConfig("t", 2, 4096, 2, 1, False, 2, 4096, 6, True)
    target=tmp_path/"sealed"
    SerialTurboBuilder(cfg, member_ready_hook=lambda ordinal, name: got.append((ordinal,name))).build(_rows(), release_identity=_identity(), target_directory=target)
    assert got == [(0,"member-00000000.r5z"),(1,"member-00000001.r5z"),(2,"member-00000002.r5z")]
    assert all(len(x)==2 for x in got)
    assert _audit_member(target/"members"/got[0][1])["row_count"] == 2


def test_authority67_queue_counter_distinguishes_pending_inflight_and_outstanding():
    t=ReadinessTelemetry()
    assert QUEUE_MAX == 8
    for _ in range(8): t.admit()
    assert t.snapshot()["pending_queue_peak"] == 8
    t.begin_audit()
    s=t.snapshot()
    assert s["pending_queue_depth"] == 7
    assert s["auditor_inflight"] == 1
    assert s["outstanding_closed_members_peak"] == 8
    t.admit()
    s=t.snapshot()
    assert s["pending_queue_depth"] == 8
    assert s["auditor_inflight_peak"] == 1
    assert s["outstanding_closed_members_peak"] == 9
    t.finish_audit()


def test_authority67_ninth_pending_member_fails_closed():
    t=ReadinessTelemetry()
    for _ in range(8): t.admit()
    import pytest
    with pytest.raises(Exception, match="pending readiness queue bound"):
        t.admit()
