"""T9S Phase B — pin the exact T9D candidate source under phase_b/.

Copies the T9D staging tree (repaired adapter + native closure + frozen test
suites + vectors) from the verified T9D commit and re-derives Git NUL-blob SHA-1
+ sha256 for every staged file, matching each to the candidate commit's own
rev-parse.  Phase A files are never overwritten.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
T9D = "d4969f513be0b3691f1bbf45813d17fc171a51a7"
T9D_STAGING = "WORKER_RETURNS/PYAT-R27-T9D-TEMPORAL-AUTHORITY-PROVENANCE-REPAIR-R1/staging"


def blob(p: Path) -> str:
    b = p.read_bytes()
    h = hashlib.sha1()
    h.update(b"blob " + str(len(b)).encode() + b"\0" + b)
    return h.hexdigest()


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git_blob_of(path: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(RET), "rev-parse", T9D + ":" + path], text=True).strip()


names = subprocess.check_output(
    ["git", "-C", str(RET), "ls-tree", "-r", "--name-only", "--full-tree", T9D, T9D_STAGING],
    text=True).splitlines()

(RET / "phase_b").mkdir(parents=True, exist_ok=True)

rows = []
for src in names:
    rel = src[len(T9D_STAGING) + 1:]
    data = subprocess.check_output(["git", "-C", str(RET), "show", T9D + ":" + src])
    out = RET / "phase_b" / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    rows.append(dict(rel=rel, git_blob_sha1=git_blob_of(src),
                     local_git_blob_sha1=blob(out), sha256=sha256(out),
                     bytes=len(data)))

for r in rows:
    assert r["git_blob_sha1"] == r["local_git_blob_sha1"], r["rel"]

manifest = dict(schema="T9S_PHASE_B_SOURCE_MANIFEST@1", candidate=T9D,
                staging_prefix=T9D_STAGING, files=rows)
(RET / "phase_b" / "SOURCE_MANIFEST.json").write_text(
    json.dumps(manifest, indent=1, sort_keys=True) + "\n")

adapter = RET / "phase_b" / "pinned_candidate" / "t9b_temporal.py"
print("staged", len(rows), "files; adapter sha256", sha256(adapter))
print("adapter git blob", blob(adapter))
