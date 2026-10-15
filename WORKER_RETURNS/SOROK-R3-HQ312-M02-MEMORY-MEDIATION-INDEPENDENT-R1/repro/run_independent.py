from pathlib import Path
import os, sys, subprocess, json, time

R = Path(__file__).resolve().parents[1]
ROOT = R.parents[1]
subdir = "corroboration" if sys.argv[1:] == ["corroboration"] else "independent"
out = R / "evidence" / subdir
out.mkdir(exist_ok=True)
cmd = [
    sys.executable,
    "-m",
    "pytest",
    str(R / "repro/test_independent.py"),
    "-p",
    "reviewer_observer",
    "-vv",
    "--tb=short",
    "--import-mode=importlib",
    "-p",
    "no:cacheprovider",
    "--rootdir=" + str(R),
    "--confcutdir=" + str(R),
    "--basetemp=" + str(R / "runtime/tmp/independent"),
    "--junitxml=" + str(out / "junit.xml"),
]
if subdir == "corroboration":
    cmd.remove(str(R / "repro/test_independent.py"))
    cmd.extend(
        [
            str(R / "repro/test_independent.py") + "::" + name
            for name in [
                "test_lawful_future_claim_cannot_condition_an_earlier_response",
                "test_checkpoint_claim_selector_cannot_downgrade_existing_belief_to_absence",
            ]
        ]
    )
env = dict(
    os.environ,
    M02_EVIDENCE_SUBDIR=subdir,
    PYTHONPATH=str(R / "repro"),
    PYTHONDONTWRITEBYTECODE="1",
    PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
    TMPDIR=str(R / "runtime/tmp"),
)
t = time.time()
p = subprocess.run(cmd, cwd=R, env=env, capture_output=True, text=True)


def clean(s):
    return (
        s.replace(str(R), "<RETURN>")
        .replace(str(ROOT), "<WORKTREE>")
        .replace(str(Path.home()), "<HOME>")
    )


(out / "stdout.log").write_text(clean(p.stdout + p.stderr))
xml = out / "junit.xml"
if xml.exists():
    xml.write_text(clean(xml.read_text()))
(out / "execution.json").write_text(
    json.dumps(
        {
            "command": [clean(x) for x in cmd],
            "cwd": "<RETURN>",
            "exit": p.returncode,
            "seconds": time.time() - t,
        },
        indent=2,
    )
    + "\n"
)
print("\n".join(clean(p.stdout + p.stderr).splitlines()[-26:]))
raise SystemExit(p.returncode)
