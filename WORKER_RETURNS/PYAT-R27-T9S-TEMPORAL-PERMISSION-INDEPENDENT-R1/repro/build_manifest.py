"""T9S Phase A — build the source manifest with real Git/NUL preimage hashes.

The pinned reviewer copy under T9R phase_b/pinned_candidate is verified to be
byte-identical to the T9C candidate commit, and each local file's Git blob is
matched against the candidate commit's own rev-parse.
"""
import hashlib
import json
import subprocess
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
PINCAND = (RET.parent / "PYAT-R26-T9R-INDEPENDENT-TEMPORAL-DELTA-R1"
           / "phase_b" / "pinned_candidate")
NATIVE = PINCAND / "native" / "data" / "ddm_build_copy"
T9C = "9a33c2dcaa7ac0d50606416ab965488c9782934b"
T9C_PREFIX = "WORKER_RETURNS/PYAT-R26-T9C-TEMPORAL-ADAPTER-SEVEN-RED-CONTINUATION-R1/"


def blob(p: Path) -> str:
    b = p.read_bytes()
    h = hashlib.sha1()
    h.update(b"blob " + str(len(b)).encode() + b"\0" + b)
    return h.hexdigest()


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git_blob_of(path: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(RET), "rev-parse", T9C + ":" + path], text=True).strip()


rows = []
for name in ("ddm_v553_temporal_identity.py", "ddm_v553_temporal_pressure.py",
             "ddm_v553_harmonization.py", "ddm_v553_canonical_harmonization.py",
             "ddm_v553_schema.py"):
    local = NATIVE / name
    rows.append(dict(local=str(local.relative_to(RET.parent)),
                     git_path=T9C_PREFIX + "native/data/ddm_build_copy/" + name,
                     git_blob_sha1=git_blob_of(T9C_PREFIX + "native/data/ddm_build_copy/" + name),
                     local_git_blob_sha1=blob(local), sha256=sha256(local),
                     bytes=local.stat().st_size))

for name in ("t9b_temporal.py", "test_t9c_repair.py"):
    local = PINCAND / name
    rows.append(dict(local=str(local.relative_to(RET.parent)),
                     git_path=T9C_PREFIX + name,
                     git_blob_sha1=git_blob_of(T9C_PREFIX + name),
                     local_git_blob_sha1=blob(local), sha256=sha256(local),
                     bytes=local.stat().st_size))

for r in rows:
    assert r["git_blob_sha1"] == r["local_git_blob_sha1"], r["local"]

manifest = dict(
    schema="T9S_PHASE_A_SOURCE_MANIFEST@1",
    candidate_pin=T9C,
    candidate_repair_payload="d6e062684ca34b99ee9713c8c0affa0ed5c27f25",
    pinned_copy_verified_identical_to_candidate=True,
    note="Each file's Git NUL-blob SHA-1 is derived from local bytes and matched to the T9C candidate commit's rev-parse.",
    files=rows,
)
(RET / "02_PHASE_A_SOURCE_MANIFEST.json").write_text(
    json.dumps(manifest, indent=1, sort_keys=True) + "\n")
print("manifest entries", len(rows), "— all Git blobs match local bytes")
for r in rows:
    print("  ", Path(r["local"]).name, r["git_blob_sha1"][:12], r["sha256"][:12])
