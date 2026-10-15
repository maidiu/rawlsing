"""Reproduce all four exact M01 suites in their original runner, no test edits."""

from pathlib import Path
import subprocess, sys, os, json, time, shutil, xml.etree.ElementTree as ET

R = Path(__file__).resolve().parents[1]
M = R / "runtime/m01"
ROOT = R.parents[1]
(R / "runtime/tmp").mkdir(exist_ok=True)
env = dict(
    os.environ,
    PYTHONPATH=str(M / "repro"),
    PYTHONDONTWRITEBYTECODE="1",
    PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
    TMPDIR=str(R / "runtime/tmp"),
)
cmd = [sys.executable, str(M / "repro/run.py")]
t = time.time()
p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)


def clean(s):
    return (
        s.replace(str(R), "<RETURN>")
        .replace(str(ROOT), "<WORKTREE>")
        .replace(str(Path.home()), "<HOME>")
    )


(R / "evidence/original_413.stdout").write_text(clean(p.stdout + p.stderr))
results = []
for name, count in [("new", 94), ("can3", 97), ("author", 89), ("owners", 133)]:
    out = R / "evidence/original_413" / name
    out.mkdir(parents=True, exist_ok=True)
    for f in ["stdout.log", "junit.xml", "execution.json"]:
        source = M / "evidence" / name / f
        if source.exists():
            (out / f).write_text(clean(source.read_text()))
    xml = out / "junit.xml"
    counts = {}
    if xml.exists():
        suites = list(ET.parse(xml).getroot().iter("testsuite"))
        counts = {
            k: sum(int(x.get(k, 0)) for x in suites)
            for k in ("tests", "failures", "errors", "skipped")
        }
    results.append({"suite": name, "expected_count": count, "counts": counts})
(R / "evidence/original_413_execution.json").write_text(
    json.dumps(
        {
            "command": [clean(x) for x in cmd],
            "cwd": "<WORKTREE>",
            "exit": p.returncode,
            "seconds": time.time() - t,
            "suites": results,
        },
        indent=2,
    )
    + "\n"
)
print("ORIGINAL_M01_413_EXIT", p.returncode)
print(results)
assert p.returncode == 0 and all(
    r["counts"]
    == {"tests": r["expected_count"], "failures": 0, "errors": 0, "skipped": 0}
    for r in results
)
