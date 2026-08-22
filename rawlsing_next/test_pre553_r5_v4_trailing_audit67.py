import gzip
from io import BytesIO
import hashlib

import pytest

from rawlsing_next import pre553_r5_compact_carrier as frozen
from rawlsing_next.pre553_r5_serial_turbo66 import BASELINE, SerialTurboBuilder
from rawlsing_next.pre553_r5_codec import canonical_bytes
from rawlsing_next.pre553_r5_model import R5CanonicalRow, R5ReleaseIdentity
from rawlsing_next.pre553_r5_v4_trailing_audit67 import _audit_member


def _identity():
    return R5ReleaseIdentity("test-release", "a" * 64, {"kind": "test"}, "b" * 64, {"M01": ("test",)}, {}, "c" * 64, "d" * 64)


def _rows():
    return [R5CanonicalRow("test", "Test", f"id-{i}", hashlib.sha256(canonical_bytes({"i": i})).hexdigest(), {"i": i}) for i in (2, 1, 3)]


def _member(tmp_path):
    target = tmp_path / "sealed"
    SerialTurboBuilder(BASELINE).build(_rows(), release_identity=_identity(), target_directory=target)
    return next((target / "members").glob("*.r5z"))


def test_trailing_audit_independently_recomputes_closed_member(tmp_path):
    item = _audit_member(_member(tmp_path))
    assert item["row_count"] == 3
    assert item["sha256"]
    assert item["logical_digest"]


def test_corrupt_and_truncated_closed_member_fail_closed(tmp_path):
    path = _member(tmp_path)
    original = path.read_bytes()
    path.write_bytes(original[:-7])
    with pytest.raises(RuntimeError): _audit_member(path)
    path.write_bytes(b"not-gzip")
    with pytest.raises(RuntimeError): _audit_member(path)


def test_readiness_ordinal_protocol_is_strict(tmp_path):
    path = _member(tmp_path)
    assert path.name == "member-00000000.r5z"
