"""Regression for the exact 459-file R2 Git-blob receiving gate."""
from __future__ import annotations
import hashlib
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
PACKET = REPO / "WORKER_RETURNS" / "SOROK-RRIF-E-RECEIVER-PACKET-FIX-F1-R1" / "candidate" / "receiving_packet"
VERIFIER = PACKET / "verify_r2_base.py"
APPLY = PACKET / "apply.sh"
R2_COMMIT = "598d9e9eaba5143950c63317705fd09104fbf463"
R2_PATH = "SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2"
MANIFEST_SHA = "7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126"


def extract_base(root: Path) -> Path:
    data = subprocess.check_output(
        ["git", "-C", str(REPO), "archive", "--format=tar", R2_COMMIT, "--", R2_PATH]
    )
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(root)
    return root / R2_PATH


def verify(dest: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VERIFIER), "--dest", str(dest), "--repo", str(REPO)],
        text=True,
        capture_output=True,
    )


def result(output: subprocess.CompletedProcess[str]) -> dict:
    return json.loads(output.stdout)


def fingerprint(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_exact_459_blob_gate_rejects_nonvendor_and_vendor_tamper_and_apply_stops(tmp_path: Path) -> None:
    dest = extract_base(tmp_path / "base")
    exact = verify(dest)
    assert exact.returncode == 0, exact.stderr + exact.stdout
    assert result(exact)["expected_files"] == 459
    assert result(exact)["actual_files"] == 459

    session = dest / "joined" / "session.py"
    original_session = session.read_bytes()
    session.write_bytes(original_session + b"\n# F2_NONVENDOR_TAMPER\n")
    tampered = verify(dest)
    assert tampered.returncode != 0
    assert "R2_BLOB_MISMATCH:joined/session.py" in result(tampered)["errors"]
    assert hashlib.sha256((dest / "SOURCE_MANIFEST.json").read_bytes()).hexdigest() == MANIFEST_SHA

    session.write_bytes(original_session)
    restored = verify(dest)
    assert restored.returncode == 0, restored.stderr + restored.stdout

    vendor = dest / "vendor" / "j" / "r31j" / "product.py"
    original_vendor = vendor.read_bytes()
    vendor.write_bytes(original_vendor + b"\n# F2_VENDOR_TAMPER\n")
    vendor_tampered = verify(dest)
    assert vendor_tampered.returncode != 0
    assert any(error.startswith("R2_BLOB_MISMATCH:vendor/j/r31j/product.py") for error in result(vendor_tampered)["errors"])
    vendor.write_bytes(original_vendor)
    assert verify(dest).returncode == 0

    session.unlink()
    session.symlink_to(dest / "joined" / "cli.py")
    linked = verify(dest)
    assert linked.returncode != 0
    assert "R2_SYMLINK:joined/session.py" in result(linked)["errors"]
    session.unlink()
    session.write_bytes(original_session)
    assert verify(dest).returncode == 0

    target = tmp_path / "apply-target"
    subprocess.run(["git", "clone", "--shared", "--no-checkout", "--quiet", str(REPO), str(target)], check=True)
    base = extract_base(target)
    session = base / "joined" / "session.py"
    session.write_bytes(session.read_bytes() + b"\n# F2_APPLY_TAMPER\n")
    before = fingerprint(base)
    stopped = subprocess.run(["sh", str(APPLY), str(target)], text=True, capture_output=True)
    assert stopped.returncode == 3
    assert "RRIF_E_BASE_R2_IDENTITY_MISMATCH" in stopped.stderr
    assert fingerprint(base) == before
    assert len(before) == 459
