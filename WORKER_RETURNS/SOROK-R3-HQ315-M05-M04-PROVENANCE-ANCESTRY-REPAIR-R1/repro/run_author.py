from pathlib import Path
import os, sys, subprocess, json, time

R = Path(__file__).resolve().parents[1]
out = R / "evidence/author"
out.mkdir(exist_ok=True)
cmd = [
    sys.executable,
    "-m",
    "pytest",
    str(R / "repro/test_author.py"),
    "-vv",
    "--tb=short",
    "--rootdir=" + str(R),
    "--confcutdir=" + str(R),
    "--import-mode=importlib",
    "-p",
    "no:cacheprovider",
    "--basetemp=" + str(R / "runtime/tmp/author"),
    "--junitxml=" + str(out / "junit.xml"),
]
p = subprocess.run(
    cmd,
    cwd=R,
    env=dict(
        os.environ,
        PYTHONDONTWRITEBYTECODE="1",
        PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
        PYTHONPATH=str(R / "repro"),
        TMPDIR=str(R / "runtime/tmp"),
    ),
    capture_output=True,
    text=True,
)


def clean(s):
    return s.replace(str(R), "[RETURN]").replace(str(Path.home()), "[HOME]")


(out / "stdout.log").write_text(clean(p.stdout + p.stderr))
xml = out / "junit.xml"
if xml.exists():
    xml.write_text(clean(xml.read_text()))
(out / "command.json").write_text(
    json.dumps({"command": [clean(x) for x in cmd], "exit": p.returncode}, indent=2)
    + "\n"
)
print("\n".join(clean(p.stdout + p.stderr).splitlines()[-24:]))
raise SystemExit(p.returncode)
