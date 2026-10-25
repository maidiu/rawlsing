"""Generate focused S47 evidence, enlarged regression tests and source manifest."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

RET = Path(__file__).resolve().parent
REPO = RET.parents[1]
EVID = RET / "evidence"
JUNIT = RET / "junit"
LOGS = RET / "logs"
PY = sys.executable
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
ENV["PYTHONPATH"] = str(RET)
ENV.setdefault(
    "M35_JOIN_E_RETURN",
    "/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/WORKER_RETURNS/"
    "SOROK-20261022-SAME-PERSON-JOIN-R1",
)
for path in (str(RET), str(RET / "tests")):
    if path not in sys.path:
        sys.path.insert(0, path)

from s47.bootstrap import CUTS, install, roots  # noqa: E402

install()

S45_RETURN = Path(roots()["s45_return"])
S44_RETURN = Path(roots()["s44_return"])
S46_RETURN = Path(roots()["s46_return"])
S42_RETURN = Path(roots()["s42_return"])
S37_RETURN = Path(roots()["s37_return"])
S47_FILES = [
    ".gitignore", "00_RETURN.md", "run_s47.py", "run_s47_evidence.py",
    "s47/__init__.py", "s47/bootstrap.py", "s47/conditioning.py",
    "s47/errors.py", "s47/session.py",
    "tests/conftest.py", "tests/test_s47_interval_c9_conditioning.py",
]
S46_FILES = [
    "s46/__init__.py", "s46/bootstrap.py", "s46/errors.py", "s46/model.py",
    "s46/producer.py", "s46/session.py",
    "tests/conftest.py", "tests/test_s46_interval_participation.py",
]
S45_FILES = [
    "s45/__init__.py", "s45/bootstrap.py", "s45/errors.py", "s45/fixtures.py",
    "s45/language.py", "s45/session.py", "tests/test_s45_generated_root_encounter.py",
]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=str(RET), capture_output=True, text=True, check=True
    ).stdout.strip()


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def _run(cmd, log_name: str, env=None):
    proc = subprocess.run(cmd, cwd=str(RET), env=env or ENV,
                          capture_output=True, text=True)
    (LOGS / log_name).write_text(proc.stdout + proc.stderr)
    return proc


def _junit_counts(path: Path) -> dict:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    tests = sum(int(s.attrib.get("tests", 0)) for s in suites)
    failures = sum(int(s.attrib.get("failures", 0)) for s in suites)
    errors = sum(int(s.attrib.get("errors", 0)) for s in suites)
    skips = sum(int(s.attrib.get("skipped", 0)) for s in suites)
    cases = []
    for case in root.iter("testcase"):
        status = "PASS"
        if case.find("failure") is not None:
            status = "RED"
        elif case.find("error") is not None:
            status = "ERROR"
        elif case.find("skipped") is not None:
            status = "SKIP"
        cases.append({
            "classname": case.attrib.get("classname", ""),
            "name": case.attrib.get("name", ""), "status": status,
        })
    return {
        "tests": tests, "PASS": tests - failures - errors - skips,
        "RED": failures, "ERROR": errors, "SKIP": skips, "cases": cases,
    }


def test_evidence():
    rows = {}
    for name, path, env in (
        ("s47", "tests", ENV),
    ):
        xml = JUNIT / f"{name}_full.xml"
        proc = _run(
            [PY, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
             f"--junitxml={xml}", path],
            f"{name}_full.log", env=env,
        )
        counts = _junit_counts(xml)
        rows[name] = {
            "exit": proc.returncode, "junit": str(xml.relative_to(RET)),
            "counts": {key: counts[key] for key in
                       ("tests", "PASS", "RED", "ERROR", "SKIP")},
            "cases": counts["cases"],
        }
    return rows


def source_manifest():
    def pinned_rows(return_dir: Path, cut: str, files: list[str]) -> list[dict]:
        rows = []
        base = return_dir.relative_to(REPO)
        for rel in files:
            local = return_dir / rel
            local_blob = _git("hash-object", str(local))
            pinned_blob = _git("rev-parse", f"{cut}:{base / rel}")
            rows.append({
                "path": rel,
                "pinned_git_blob_sha1": pinned_blob,
                "local_git_blob_sha1": local_blob,
                "exact": local_blob == pinned_blob,
                "sha256": _sha256(local),
            })
        return rows

    s46_rows = pinned_rows(S46_RETURN, CUTS["s46"], S46_FILES)
    s45_rows = pinned_rows(S45_RETURN, CUTS["s45"], S45_FILES)
    local_rows = [{
        "path": rel, "sha256": _sha256(RET / rel),
        "git_blob_sha1": _git("hash-object", str(RET / rel)),
    } for rel in S47_FILES if (RET / rel).exists()]
    origins = {}
    for name in ("s37", "s42", "s46", "s46.session", "s47", "s47.session"):
        module = sys.modules.get(name)
        if module is not None:
            origins[name] = str(Path(getattr(module, "__file__", "")).resolve())
    from s44.root import generate_root
    from s45.fixtures import root_bundle
    bundle = root_bundle("01" * 32)
    return {
        "schema": "SOROK_S47_SOURCE_MANIFEST@1",
        "roots": roots(),
        "cuts": dict(CUTS),
        "s46_reused": {
            "rows": s46_rows,
            "all_exact": all(row["exact"] for row in s46_rows),
        },
        "s45_reused": {
            "rows": s45_rows,
            "all_exact": all(row["exact"] for row in s45_rows),
        },
        "s47_local": local_rows,
        "dependency_seams": [
            {
                "path": "WORKER_RETURNS/SOROK-20261024-S42-ONGOING-EVENT-CONSUMER-R1/s42/session.py",
                "sha256": _sha256(S42_RETURN / "s42/session.py"),
                "git_blob_sha1": _git("hash-object", str(S42_RETURN / "s42/session.py")),
                "reason": "minimal extra-conditioning-source hook before actual S42 C9 admission",
            },
            {
                "path": "WORKER_RETURNS/SOROK-20261024-S37-INTEGRATED-CONSUMER-R1/s37/producer.py",
                "sha256": _sha256(S37_RETURN / "s37/producer.py"),
                "git_blob_sha1": _git("hash-object", str(S37_RETURN / "s37/producer.py")),
                "reason": "minimal actual C9 call-site: use qualified interval sources when supplied; accepted B source path unchanged otherwise",
            },
        ],
        "source_class": "ResolvedStructuralContext",
        "source_class_material": True,
        "root_bundle_hash": bundle["bundle_hash"],
        "root_hash": generate_root(bundle).root_hash,
        "imported_origins": origins,
        "s46_origin_accepted": "SOROK-20261025-S46-INTERVAL-PARTICIPATION-CONSUMER-R1"
        in origins.get("s46.session", ""),
        "s47_origin_local": "SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1"
        in origins.get("s47.session", ""),
    }


def main() -> int:
    EVID.mkdir(exist_ok=True)
    JUNIT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="s47-evidence-", dir=str(RET)))
    try:
        entry = _run([PY, "-B", "run_s47.py"], "entrypoint.log")
        if entry.returncode != 0:
            raise RuntimeError("S47_ENTRYPOINT_FAILED:" + entry.stderr)
        report = json.loads(entry.stdout)
        (EVID / "entrypoint.json").write_text(entry.stdout)
        _write(EVID / "actual.json", report["actual"])
        _write(EVID / "scheduled.json", report["scheduled"])
        _write(EVID / "condition.json", report["condition"])
        _write(EVID / "no_interval.json", report["no_interval"])
        _write(EVID / "source_faults.json", report["source_faults"])
        tests = test_evidence()
        _write(EVID / "test_run.json", {
            "schema": "SOROK_S47_TEST_RUN@1", "rows": tests,
            "entrypoint_exit": entry.returncode,
            "checks": report["checks"],
        })
        _write(EVID / "source_manifest.json", source_manifest())
        print(json.dumps({
            "tests": {key: value["counts"] for key, value in tests.items()},
            "entrypoint_exit": entry.returncode,
            "checks": report["checks"],
            "actual": {
                "root": report["actual"]["root_hash"],
                "material_after_interval": report["actual"]["material_after_interval"],
                "c9_material": report["actual"]["c9"]["objective_material_eligible"],
                "source_in_readset": report["actual"]["c9"]["s47_source_in_readset"],
                "target": report["actual"]["c9"]["target_branch"],
            },
            "scheduled": {
                "root": report["scheduled"]["root_hash"],
                "material_after_interval": report["scheduled"]["material_after_interval"],
                "c9_material": report["scheduled"]["c9"]["objective_material_eligible"],
                "source_in_readset": report["scheduled"]["c9"]["s47_source_in_readset"],
                "target": report["scheduled"]["c9"]["target_branch"],
            },
            "condition": report["condition"],
            "source_faults": report["source_faults"],
        }, sort_keys=True))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
