"""Reconstruct exact frozen inputs under this return only; refuse existing runtime."""

from pathlib import Path
import subprocess, hashlib, json

R = Path(__file__).resolve().parents[1]
REPOSITORY_TOP = subprocess.check_output(["git", "-C", str(R), "rev-parse", "--show-toplevel"],text=True).strip()
ROOT = Path(REPOSITORY_TOP)
C = "1de1c9c57bffa8bb663edd44af744379b028f698"
PREFIX = (
    "WORKER_RETURNS/PYAT-USERDIRECT-20261015-R11-PV2I-INDEPENDENT-ORIGINAL-SCOPE-R1/"
)
if (R / "runtime_root").exists():
    raise SystemExit(
        "EXISTING_RUNTIME_REFUSED; preserve evidence or use a fresh checkout"
    )
manifest = []
for source in subprocess.check_output(
    ["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", C, PREFIX], text=True
).splitlines():
    data = subprocess.check_output(["git", "-C", str(ROOT), "show", C + ":" + source])
    blob = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", C + ":" + source], text=True
    ).strip()
    assert (
        hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        == blob
    )
    out = R / "frozen_pv2i" / source[len(PREFIX) :]
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        assert out.read_bytes() == data
    else:
        out.write_bytes(data)
    manifest.append(
        {
            "source": source,
            "commit": C,
            "git_blob_sha1": blob,
            "sha256": hashlib.sha256(data).hexdigest(),
        }
    )
(R / "observations").mkdir(exist_ok=True)
(R / "observations/frozen_pv2i_sources.json").write_text(
    json.dumps(manifest, indent=2) + "\n"
)
exec(compile((R / "frozen_pv2i/repro/stage.py").read_text().replace("ROOT=R.parents[1]", "ROOT=Path(REPOSITORY_TOP)"), str(__file__), "exec"))
exec(compile((R / "repro/stage_retained_worker.py").read_text(), str(__file__), "exec"))
(R / "runtime_root/sitecustomize.py").write_bytes(
    (R / "repro/sitecustomize.py").read_bytes()
)

# Provision once as a trusted installation step. Cold/request paths never provision.
import os, sys

provision_env = dict(
    os.environ,
    PYTHONDONTWRITEBYTECODE="1",
    PYTHONPATH=os.pathsep.join(
        map(str, [R / "repro", R / "runtime_root", R / "runtime_root/candidate/repro"])
    ),
)
subprocess.run(
    [sys.executable, str(R / "repro/provision_owner.py")], env=provision_env, check=True
)
