"""Pinned input reconstruction, optionally reusing verified warm static sources."""

from pathlib import Path
import subprocess, sys, json, hashlib, shutil, uuid, datetime, os

R = Path(__file__).resolve().parents[1]
ROOT = R.parents[1]
RT = R / "runtime"
RT.mkdir(exist_ok=False)
M02 = "0216d9036a87e2f60f42fd5b2870556027808419"
P = "WORKER_RETURNS/SOROK-R3-HQ312-M02-MEMORY-MEDIATION-INDEPENDENT-R1"
M01 = "02187a14e75ff30dd953d3c7185d689b80e62304"
MP = "WORKER_RETURNS/SOROK-R3-HQ310-M01-MEMORY-MEDIATION-CAUSAL-CELL-R1"


def git(*a):
    return subprocess.check_output(["git", "-c", "gc.auto=0", "-C", str(ROOT), *a])


def bh(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


rows = []
for path in git("ls-tree", "-r", "--name-only", M02, P).decode().splitlines():
    rel = path[len(P) + 1 :]
    if rel.startswith("evidence/"):
        continue
    b = git("show", M02 + ":" + path)
    h = git("rev-parse", M02 + ":" + path).decode().strip()
    assert bh(b) == h
    dest = RT / "m02" / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(b)
    rows.append(
        {
            "commit": M02,
            "path": path,
            "blob_sha1": h,
            "sha256": hashlib.sha256(b).hexdigest(),
            "local": str(dest.relative_to(R)),
        }
    )
(RT / "m02/evidence").mkdir(exist_ok=True)
warm = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
if warm is not None:
    passport = json.loads((warm / "environment_passport_delta.json").read_text())
    marker = (warm / "runtime/runtime_marker.json").read_bytes()
    assert hashlib.sha256(marker).hexdigest() == passport["runtime_marker_digest"]
    for p in (warm / "runtime/m01/repro").glob("*.py"):
        assert p.read_bytes() == git("show", M01 + ":" + MP + "/repro/" + p.name)
    for row in passport["materialized_source_refs"]:
        p = warm / row["module_file"]
        assert bh(p.read_bytes()) == row["blob_sha1"]
    target = RT / "m02/runtime/m01"
    target.parent.mkdir(exist_ok=True)
    shutil.copytree(
        warm / "runtime/m01",
        target,
        ignore=shutil.ignore_patterns(
            "__pycache__", ".pytest_cache", "evidence", "m01_body_probe"
        ),
    )
    for folder in (warm / "runtime/m01").rglob("evidence"):
        if folder.is_dir():
            (target / folder.relative_to(warm / "runtime/m01")).mkdir(
                parents=True, exist_ok=True
            )
    warm_status = (
        "VERIFIED_WARM_M02_STATIC_SOURCE_CLOSURE; no mutable-process continuity claim"
    )
else:
    p = subprocess.run(
        [sys.executable, str(RT / "m02/repro/stage.py")],
        cwd=ROOT,
        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
        capture_output=True,
        text=True,
    )
    (R / "evidence/staging.stdout").write_text(p.stdout + p.stderr)
    assert p.returncode == 0, p.stderr
    warm_status = "RECONSTRUCTED_FROM_PINNED_GIT"
# Input scientific freezes are read only. Runtime result files are not custody roots.
freeze = RT / "m02/01_INDEPENDENT_EXPECTATIONS.json"
assert (
    hashlib.sha256(freeze.read_bytes()).hexdigest()
    == "00e7090baacc67f845936f1e40bc2b602202bae5019d11b79f92d0df557fa4a4"
)
for p in (RT / "m02/runtime/m01/repro").glob("*.py"):
    assert p.read_bytes() == git("show", M01 + ":" + MP + "/repro/" + p.name)
(R / "01_INPUT_SOURCE_IDENTITIES.json").write_text(
    json.dumps(
        {
            "source_files": rows,
            "warm_source_status": warm_status,
            "original_M01_commit": M01,
            "original_M02_commit": M02,
            "original_M02_freeze_commit": "0c875790fd7341402d7eeee4a515ca67dc43ee65",
            "original_M02_freeze_sha256": hashlib.sha256(
                freeze.read_bytes()
            ).hexdigest(),
        },
        indent=2,
    )
    + "\n"
)
shutil.copytree(RT / "m02/runtime/m01/repro", RT / "frozen_m01_repro")
(RT / "tmp").mkdir()
(RT / "m02/evidence").mkdir(exist_ok=True)
(RT / "runtime_marker.json").write_text(
    json.dumps(
        {
            "environment_id": str(uuid.uuid4()),
            "epoch_id": str(uuid.uuid4()),
            "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "role": "M03_AUTHOR_NOT_ACCEPTANCE_REVIEWER",
            "source_reuse": warm_status,
        },
        indent=2,
    )
    + "\n"
)
print("M03_PINNED_SOURCE_CLOSURE_READY", warm_status)
