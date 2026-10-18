"""GF1N Phase B qualification wrapper.

The unchanged GF1L qualification machinery expects the reviewed return to sit
directly under ``<repo>/WORKER_RETURNS`` and expects the three replay seats to
exist before ``qualify.py`` starts.  This wrapper performs only that mechanical
staging/seating (Git-pinned predecessor bytes plus the exact candidate) and then
runs the unchanged ``repair/qualify.py``.  No candidate, test or canonical file
is edited.
"""
from __future__ import annotations

import hashlib
import io
import json
import shutil
import subprocess
import tarfile
from pathlib import Path

R = Path(__file__).resolve().parents[1]
S = R / "stage"
V = S / "WORKER_RETURNS/PYAT-R33-GF1L-NATIVE-IDENTITY-I2-R1"
REPO = S
CAND = S / "WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1/court/runtime_root/gf1_pair_support_consumer.py"

PINS = {
    "E": ("WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1",
          "eeb726357204653b22458dc267dd70ba0009bd77"),
    "G": ("WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1",
          "ec5dddfcb3476c01ceb8e7f5122c5e5259b936f7"),
    "H": ("WORKER_RETURNS/PYAT-R32-GF1H-PAIR-CONSUMER-INTEGRITY-REPAIR-R1",
          "cc41ad4553d189a3c4c8152179b3d1977327c07f"),
    "J": ("WORKER_RETURNS/PYAT-R32-GF1J-INDEPENDENT-GF1H-COURT-R1",
          "f3f34bc1b7b9fd97a3ae8a9b24dd2201f42f38f5"),
    "K": ("WORKER_RETURNS/PYAT-R33-GF1K-CATEGORY-IDENTITY-REPAIR-R1",
          "1399a475e54ea33355cf641979829424625c511d"),
    "F": ("WORKER_RETURNS/PYAT-R28-GF1F-IMPLEMENTED-NATIVE-CONSUMER-INDEPENDENT-R1",
          "3dcc7d7dddfff4f1be8b4293cab92e5b4275007d"),
    "I": ("WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1",
          "c6a55f0dd5b327c40d64f96e0705ab5485559e90"),
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)


def archive(sha: str, path: str, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(git("archive", sha, path))) as tar:
        for member in tar.getmembers():
            assert not member.issym() and not member.islnk(), member.name
            assert (dest / member.name).resolve().is_relative_to(dest.resolve())
        tar.extractall(dest)


def main() -> int:
    nested = V / "stage"
    if not nested.exists():
        for path, sha in PINS.values():
            archive(sha, path, nested)
        pre_sha = "9f4a23cef1482e0a81afb1e7a65df90879931465"
        archive(pre_sha, PINS["E"][0] + "/court", nested / "pre")
        shutil.copytree(nested / "pre" / PINS["E"][0] / "court",
                        nested / PINS["I"][0] / "court", dirs_exist_ok=True)
    candidate = CAND.read_bytes()
    assert hashlib.sha256(candidate).hexdigest() == \
        "7629749e61e1204c7f2b2098548a5c136c37ab22098cd8a3490082ee3e7021d2"
    seats = [
        nested / PINS["E"][0] / "court/runtime_root/gf1_pair_support_consumer.py",
        nested / PINS["F"][0] / "candidate/court/runtime_root/gf1_pair_support_consumer.py",
        nested / PINS["I"][0] / "court/runtime_root/gf1_pair_support_consumer.py",
    ]
    for seat in seats:
        seat.parent.mkdir(parents=True, exist_ok=True)
        seat.write_bytes(candidate)
    print(json.dumps({"staged_nested": str(nested), "seats": [str(s) for s in seats],
                      "candidate_sha256": hashlib.sha256(candidate).hexdigest()}, indent=2))
    proc = subprocess.run(["python3", "-B", str(V / "repair/qualify.py")],
                          cwd=REPO, text=True)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
