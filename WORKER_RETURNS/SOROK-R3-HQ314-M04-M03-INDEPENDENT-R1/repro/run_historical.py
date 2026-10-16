"""Replay nine literal historical failures; never reinterpret them as passes."""

from pathlib import Path
import hashlib, json, subprocess, os, sys, shutil, xml.etree.ElementTree as ET

R = Path(__file__).resolve().parents[1]
ROOT = R.parents[1]
M2 = R / "runtime/m02"
commit = "ef12349defe22a50e053a7a8080a67ab45673417"
base = "WORKER_RETURNS/SOROK-R3-HQ309-CAN3-CAN008-INDEPENDENT-R1"
refs = []
for suite in ("candidate", "rcp3"):
    name = base + "/evidence/" + suite + "/junit.xml"
    b = subprocess.check_output(["git", "show", commit + ":" + name], cwd=ROOT)
    blob = subprocess.check_output(
        ["git", "rev-parse", commit + ":" + name], cwd=ROOT, text=True
    ).strip()
    assert hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest() == blob
    p = M2 / "runtime/m01/runtime/can3/evidence" / suite / "junit.xml"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b)
    refs.append(
        {
            "commit": commit,
            "path": name,
            "blob_sha1": blob,
            "sha256": hashlib.sha256(b).hexdigest(),
        }
    )
out = R / "evidence/historical_nine"
out.mkdir(exist_ok=True)
env = dict(
    os.environ,
    PYTHONDONTWRITEBYTECODE="1",
    PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
    PYTHONPATH=str(M2 / "repro"),
    TMPDIR=str(R / "runtime/tmp"),
)
cmd = [sys.executable, str(M2 / "repro/run_historical_nine.py")]
p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)


def clean(s):
    return (
        s.replace(str(R), "[RETURN]")
        .replace(str(ROOT), "[WORKTREE]")
        .replace(str(Path.home()), "[HOME]")
    )


(out / "stdout.log").write_text(clean(p.stdout + p.stderr))
for f in (M2 / "evidence/historical_nine").glob("*"):
    if f.is_file():
        (out / f.name).write_text(clean(f.read_text()))
root = ET.parse(out / "junit.xml").getroot()
ts = list(root.iter("testsuite"))
counts = {
    k: sum(int(s.get(k, 0)) for s in ts)
    for k in ("tests", "failures", "errors", "skipped")
}
(out / "command.json").write_text(
    json.dumps(
        {
            "command": [clean(s) for s in cmd],
            "exit": p.returncode,
            "counts": counts,
            "historical_case_selection_input_refs": refs,
            "not_in_513": True,
        },
        indent=2,
    )
    + "\n"
)
print("HISTORICAL_NINE", p.returncode, counts)
assert p.returncode == 1 and counts == dict(tests=9, failures=9, errors=0, skipped=0)
