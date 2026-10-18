"""GF1N Phase B exact staging and source attestation.

Materializes the pinned predecessor trees from Git bytes into the ignored
``stage/`` directory inside this commissioned return.  It never edits canonical
or original files: it only seats the exact GF1M follow-up candidate at the
original runtime consumer seat inside the staged copy.

Run from the repository worktree root: python3 -B <this file>
"""
from __future__ import annotations

import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path

R = Path(__file__).resolve().parents[1]
REPO = Path(subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], cwd=R, text=True).strip())
S = R / "stage"
OUT = R / "phase_b"

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
    "AUTHOR": ("WORKER_RETURNS/PYAT-R33-GF1L-NATIVE-IDENTITY-I2-R1",
               "d97a5df8c03d02ca3c7433937550cdb6774537b5"),
}
CANDIDATE_COMMIT = "a8fcb6953f2795b7bc698f9f019f4782f80026c9"
CANDIDATE_PATH = ("WORKER_RETURNS/PYAT-R34-GF1M-INDEPENDENT-CURRENT-GF1-R1/"
                  "author_followup_nonfinite/gf1_pair_support_consumer.py")
CANDIDATE_SHA = "7629749e61e1204c7f2b2098548a5c136c37ab22098cd8a3490082ee3e7021d2"
CANDIDATE_BLOB = "c5dfb119ee730e968c54be9f085fd3a6d78fa787"
FROZEN26_PATH = ("WORKER_RETURNS/PYAT-R34-GF1M-INDEPENDENT-CURRENT-GF1-R1/"
                 "03_REAL_JUNIT_282_NESTED44_COLD_AND_NEW_ADVERSARIALS/test_independent_domains.py")
FROZEN26_BLOB = "5f74164917d3531b3827ff54e843c47c64b1999c"
AUTHOR22_PATH = ("WORKER_RETURNS/PYAT-R34-GF1M-INDEPENDENT-CURRENT-GF1-R1/"
                 "author_followup_nonfinite/test_nonfinite_refusal.py")


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=REPO)


def ids(raw: bytes) -> dict:
    return {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "git_blob_sha1": hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(),
        "bytes": len(raw),
    }


def archive(sha: str, path: str, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    raw = git("archive", sha, path)
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        for member in tar.getmembers():
            assert not member.issym() and not member.islnk(), member.name
            assert (dest / member.name).resolve().is_relative_to(dest.resolve()), member.name
        tar.extractall(dest)


def main() -> None:
    manifest = {"schema": "PYAT_R34_GF1N_PHASE_B_STAGING_MANIFEST@1",
                "repo": str(REPO), "stage": str(S), "pins": {}}
    for name, (path, sha) in PINS.items():
        archive(sha, path, S)
        manifest["pins"][name] = {"path": path, "commit": sha}

    # Original GF1I court seat is the retained pre-GF1I native court.
    pre_sha = "9f4a23cef1482e0a81afb1e7a65df90879931465"
    archive(pre_sha, PINS["E"][0] + "/court", S / "pre")
    import shutil
    shutil.copytree(S / "pre" / PINS["E"][0] / "court", S / PINS["I"][0] / "court",
                    dirs_exist_ok=True)
    manifest["pre_court_commit"] = pre_sha

    # Exact candidate bytes from Git.
    candidate = git("show", CANDIDATE_COMMIT + ":" + CANDIDATE_PATH)
    assert hashlib.sha256(candidate).hexdigest() == CANDIDATE_SHA, "candidate sha256"
    assert ids(candidate)["git_blob_sha1"] == CANDIDATE_BLOB, "candidate blob"
    E = S / PINS["E"][0]
    V = S / PINS["AUTHOR"][0]
    seat = E / "court/runtime_root/gf1_pair_support_consumer.py"
    prior = seat.read_bytes()
    seat.write_bytes(candidate)
    author_seat = V / "repair/gf1_pair_support_consumer.py"
    author_prior = author_seat.read_bytes()
    author_seat.write_bytes(candidate)
    manifest["candidate"] = {"commit": CANDIDATE_COMMIT, "path": CANDIDATE_PATH,
                             **ids(candidate), "seated": str(seat)}
    manifest["prior_consumer_ids"] = ids(prior)
    manifest["prior_author_consumer_ids"] = ids(author_prior)

    # Exact frozen original26 and author22 test bytes (copied, never edited).
    f26 = git("show", CANDIDATE_COMMIT + ":" + FROZEN26_PATH)
    assert ids(f26)["git_blob_sha1"] == FROZEN26_BLOB, "frozen26 blob"
    (OUT / "test_independent_domains.py").write_bytes(f26)
    (OUT / "test_nonfinite_refusal.py").write_bytes(
        git("show", CANDIDATE_COMMIT + ":" + AUTHOR22_PATH))
    manifest["frozen26"] = {"path": FROZEN26_PATH, **ids(f26)}
    manifest["author22"] = {"path": AUTHOR22_PATH,
                            **ids(git("show", CANDIDATE_COMMIT + ":" + AUTHOR22_PATH))}

    # Original74 source attestation: selector rows vs runtime bytes vs Git bytes.
    selector = json.loads((E / "court/source_selector.json").read_text())
    rows = []
    for row in selector["files"]:
        local = E / "court/runtime_root" / row["staged_path"]
        raw = local.read_bytes()
        original = git("show", row["commit"] + ":" + row["source_path"])
        got = ids(raw)
        assert raw == original, "source bytes differ: " + row["staged_path"]
        assert all(got[k] == row[k] for k in ("sha256", "git_blob_sha1", "bytes")), row["staged_path"]
        rows.append({"staged_path": row["staged_path"], "commit": row["commit"],
                     "source_path": row["source_path"], **got})
    assert len(rows) == 74, len(rows)
    manifest["native74"] = {"count": 74, "all_git_exact": True,
                            "python_files": sum(1 for r in rows if r["staged_path"].endswith(".py")),
                            "rows": rows}

    (OUT / "STAGING_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"staged": True, "native74": len(rows),
                      "candidate_sha256": manifest["candidate"]["sha256"],
                      "candidate_blob": manifest["candidate"]["git_blob_sha1"],
                      "frozen26_blob": manifest["frozen26"]["git_blob_sha1"]}, indent=2))


if __name__ == "__main__":
    main()
