"""Run exact published tests in the original harness, copy portable phase evidence."""

from pathlib import Path
import subprocess, sys, os, time, json, shutil, xml.etree.ElementTree as ET

R = Path(__file__).resolve().parents[1]
ROOT = R.parents[1]
M2 = R / "runtime/m02"
M1 = M2 / "runtime/m01"
phase = sys.argv[1]
suite = sys.argv[2]
assert phase in ("before", "after")
out = R / "evidence" / phase / suite
out.mkdir(parents=True, exist_ok=True)
env = dict(
    os.environ,
    PYTHONDONTWRITEBYTECODE="1",
    PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
    TMPDIR=str(R / "runtime/tmp"),
    PYTHONPATH=str(M2 / "repro"),
)
cmd = [
    sys.executable,
    str(
        M1 / "repro/run.py"
        if suite == "original_413"
        else M2 / "repro/run_independent.py"
    ),
]
t = time.time()
p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)


def clean(s):
    return (
        s.replace(str(R), "<RETURN>")
        .replace(str(ROOT), "<WORKTREE>")
        .replace(str(Path.home()), "<HOME>")
    )


(out / "stdout.log").write_text(clean(p.stdout + p.stderr))
source = M1 / "evidence" if suite == "original_413" else M2 / "evidence/independent"
if source.exists():
    for f in source.rglob("*"):
        if not f.is_file():
            continue
        target = out / f.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            clean(f.read_text())
            .replace("<RETURN>", "[RETURN]")
            .replace("<WORKTREE>", "[WORKTREE]")
            .replace("<HOME>", "[HOME]")
            if f.suffix == ".xml"
            else clean(f.read_text())
        )
if suite == "original_413":
    for n in ["original_413_execution.json", "original_413.stdout"]:
        if (M2 / "evidence" / n).exists():
            (out / n).write_text(clean((M2 / "evidence" / n).read_text()))
results = []
for path in sorted(out.rglob("junit.xml")):
    root = ET.parse(path).getroot()
    ts = list(root.iter("testsuite"))
    counts = {
        k: sum(int(x.get(k, 0)) for x in ts)
        for k in ("tests", "failures", "errors", "skipped")
    }
    results.append({"junit": str(path.relative_to(R)), "counts": counts})
record = {
    "phase": phase,
    "suite": suite,
    "command": [clean(x) for x in cmd],
    "cwd": "<WORKTREE>",
    "exit": p.returncode,
    "seconds": time.time() - t,
    "results": results,
}
(out / "command.json").write_text(json.dumps(record, indent=2) + "\n")
print(phase, suite, "EXIT", p.returncode, results)
if suite == "original_413":
    assert (
        p.returncode == 0
        and sum(x["counts"]["tests"] for x in results) == 413
        and all(
            x["counts"]["failures"]
            == x["counts"]["errors"]
            == x["counts"]["skipped"]
            == 0
            for x in results
        )
    )
else:
    expected = 2 if phase == "before" else 0
    assert len(results) == 1 and results[0]["counts"] == {
        "tests": 100,
        "failures": expected,
        "errors": 0,
        "skipped": 0,
    }
    assert p.returncode == (1 if expected else 0)
