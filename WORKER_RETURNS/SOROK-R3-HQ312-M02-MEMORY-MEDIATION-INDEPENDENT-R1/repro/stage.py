"""Exact Git reconstruction inside the independent return; no owner edits."""

from pathlib import Path
import subprocess, hashlib, json, os, sys, uuid, datetime

R = Path(__file__).resolve().parents[1]
ROOT = R.parents[1]
M01 = "02187a14e75ff30dd953d3c7185d689b80e62304"
PRE = "845edf5d7c9c48b192b631dacf295afa6f587137"
P = "WORKER_RETURNS/SOROK-R3-HQ310-M01-MEMORY-MEDIATION-CAUSAL-CELL-R1"
RT = R / "runtime"
RT.mkdir(exist_ok=False)


def git(*args):
    return subprocess.check_output(["git", "-c", "gc.auto=0", "-C", str(ROOT), *args])


def blob(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


rows = []
for path in git("ls-tree", "-r", "--name-only", M01, P).decode().splitlines():
    rel = path[len(P) + 1 :]
    if rel.startswith("evidence/"):
        continue
    b = git("show", M01 + ":" + path)
    h = git("rev-parse", M01 + ":" + path).decode().strip()
    assert blob(b) == h
    dest = RT / "m01" / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(b)
    rows.append(
        {
            "commit": M01,
            "path": path,
            "blob_sha1": h,
            "sha256": hashlib.sha256(b).hexdigest(),
            "local": str(dest.relative_to(R)),
        }
    )
pre = git("show", PRE + ":" + P + "/01_PREREGISTRATION.md")
assert pre == (RT / "m01/01_PREREGISTRATION.md").read_bytes()
assert (
    subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", PRE, M01]
    ).returncode
    == 0
)
assert (
    subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "-e", PRE + ":" + P + "/repro/cell.py"],
        capture_output=True,
    ).returncode
    != 0
)
(R / "evidence/source_staging.log").write_text(
    "M01 exact return source staged; original preregistration identical, ancestor of final; cell.py absent at preregistration.\n"
)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
p = subprocess.run(
    [sys.executable, str(RT / "m01/repro/stage.py")],
    cwd=ROOT,
    env=env,
    capture_output=True,
    text=True,
)
(R / "evidence/inherited_staging.log").write_text(p.stdout + p.stderr)
assert p.returncode == 0, p.stderr
rows += json.loads((RT / "m01/02_SOURCE_IDENTITIES.json").read_text())
# Original M01 receipt local paths differ for its inherited closure; these are
# exact Git source identities, not assumptions of reviewer import placement.
(R / "02_SOURCE_IDENTITIES.json").write_text(json.dumps(rows, indent=2) + "\n")
marker = {
    "environment_id": str(uuid.uuid4()),
    "epoch_id": str(uuid.uuid4()),
    "surface": "LOCAL_SHARED_STORE",
    "owner_session_alias": "M02_INDEPENDENT_REVIEW",
    "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "sealed_startup": git("rev-parse", "HEAD").decode().strip(),
    "independence": "No M01/CAN2 authorship in this reviewer conversation; no helpers or model calls",
}
(RT / "runtime_marker.json").write_text(json.dumps(marker, indent=2) + "\n")
print("PINNED_M01_AND_INHERITED_CLOSURE_STAGED", len(rows))
