#!/usr/bin/env python3
"""Executable causal regression harness for pinned Sorok S45-S47."""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import traceback
import xml.etree.ElementTree as ET
from pathlib import Path

RETURN = Path(__file__).resolve().parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

from harness import pins  # noqa: E402
from harness.scenarios import run_scenarios  # noqa: E402

EXPECTED_FOCUSED_TESTS = {"s45": 21, "s46": 17, "s47": 17}
MODULE_NAMES = (
    "s47.bootstrap",
    "s47.session",
    "s47.conditioning",
    "s46.session",
    "s46.producer",
    "s45.session",
    "s45.fixtures",
    "s44.session",
    "s44.root",
    "s43.session",
    "s42.session",
    "s42.reader",
    "s41.event",
    "s40.session",
    "s39.producer",
    "s37.producer",
    "s37.harness",
    "candidate",
    "language_mediation.session",
    "joined.session",
    "bp1.composer",
    "bp4.world",
    "r31e.expression",
    "firstclass",
)


def _json_dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def _stage_env(stage: Path) -> dict:
    join_e = stage / pins.PINS["join_e"].base
    r31j = stage / pins.PINS["r31j"].base
    language = stage / pins.PINS["language"].base
    s36 = stage / pins.PINS["s36"].base
    s37 = stage / pins.PINS["s37"].base
    return {
        "S37_JOIN_E_RETURN": str(join_e),
        "S37_LANGUAGE_RETURN": str(language),
        "S37_S36_RETURN": str(s36),
        "S37_M35_RETURN": str(s37 / "vendor" / "m35"),
        "M35_JOIN_E_RETURN": str(join_e),
        "M35_BP2_VENDOR": str(r31j / "candidate" / "vendor" / "bp2" / "vendor"),
    }


def _configure_runtime(stage: Path) -> dict:
    env = _stage_env(stage)
    os.environ.update(env)
    s47 = stage / pins.PINS["s47"].base
    if str(s47) in sys.path:
        sys.path.remove(str(s47))
    sys.path.insert(0, str(s47))
    from s47.bootstrap import install, roots

    install()
    return {"env": env, "roots": roots()}


def _junit_counts(path: Path) -> dict:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    tests = sum(int(suite.attrib.get("tests", 0)) for suite in suites)
    failures = sum(int(suite.attrib.get("failures", 0)) for suite in suites)
    errors = sum(int(suite.attrib.get("errors", 0)) for suite in suites)
    skips = sum(int(suite.attrib.get("skipped", 0)) for suite in suites)
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
            "name": case.attrib.get("name", ""),
            "status": status,
        })
    return {
        "tests": tests,
        "PASS": tests - failures - errors - skips,
        "RED": failures,
        "ERROR": errors,
        "SKIP": skips,
        "cases": cases,
    }


def _run_original_tests(
    *,
    source_root: Path,
    stage: Path,
    logs_dir: Path,
    evidence_dir: Path,
    selection: str,
    timeout: int,
) -> dict:
    if selection == "none":
        return {
            "schema": "SOROK_S45_S47_HARNESS_ORIGINAL_TESTS@1",
            "selection": selection,
            "status": "NOT_RUN",
            "rows": {},
            "checks": {},
        }
    selected = ("s47",) if selection == "s47" else ("s45", "s46", "s47")
    logs_dir.mkdir(parents=True, exist_ok=True)
    junit_dir = evidence_dir / "junit"
    junit_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = logs_dir / "tmp"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env.update(_stage_env(stage))
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["TMPDIR"] = str(tmp_dir)
    rows = {}
    checks = {}
    for key in selected:
        pin = pins.PINS[key]
        test_dir = stage / pin.base / "tests"
        junit = junit_dir / f"{key}_full.xml"
        log = logs_dir / f"{key}_full.log"
        env["PYTHONPATH"] = str(stage / pin.base)
        command = [
            sys.executable,
            "-B",
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            f"--junitxml={junit}",
            str(test_dir),
        ]
        started = time.time()
        proc = subprocess.run(
            command,
            cwd=str(RETURN),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = round(time.time() - started, 3)
        log.write_text(proc.stdout + proc.stderr)
        counts = _junit_counts(junit) if junit.is_file() else {}
        rows[key] = {
            "cut": pin.cut,
            "package": pin.package,
            "test_dir": str(test_dir),
            "command": " ".join(command),
            "exit": proc.returncode,
            "elapsed_seconds": elapsed,
            "log": str(log.relative_to(RETURN)),
            "junit": str(junit.relative_to(RETURN)),
            "counts": {
                field: counts.get(field)
                for field in ("tests", "PASS", "RED", "ERROR", "SKIP")
            },
            "cases": counts.get("cases", []),
            "expected_tests": EXPECTED_FOCUSED_TESTS[key],
        }
        checks[key] = (
            proc.returncode == 0
            and counts.get("tests") == EXPECTED_FOCUSED_TESTS[key]
            and counts.get("RED") == 0
            and counts.get("ERROR") == 0
            and counts.get("SKIP") == 0
        )
    shutil.rmtree(tmp_dir, ignore_errors=True)
    return {
        "schema": "SOROK_S45_S47_HARNESS_ORIGINAL_TESTS@1",
        "source_root": str(source_root),
        "selection": selection,
        "status": "RUN",
        "rows": rows,
        "checks": checks,
        "all_checks_pass": all(checks.values()) if checks else True,
    }


def _pin_checks(manifest: dict, origins: dict) -> dict:
    by_key = {
        key: row["all_exact"] for key, row in manifest["pin_rows"].items()
    }
    failed_modules = {
        name: row for name, row in origins.items()
        if row["status"] != "IMPORTED" or not row["under_stage"]
    }
    return {
        "commission_pins_all_exact": all(by_key.values()),
        "m35_vendor_exact": manifest["m35_vendor"]["all_exact"],
        "modules_under_stage": not failed_modules,
        "failed_modules": failed_modules,
    }


def _parse_pinned_paths(values: list[str]) -> dict:
    rows = {}
    for value in values:
        if "=" not in value:
            raise pins.HarnessError("PINNED_PATH_NOT_KEY_VALUE:" + value)
        key, raw = value.split("=", 1)
        key = key.strip()
        if not key:
            raise pins.HarnessError("PINNED_PATH_EMPTY_KEY:" + value)
        rows[key] = Path(raw).expanduser()
    return rows


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the pinned S45-S47 performed-versus-scheduled causal "
            "regression harness."
        )
    )
    parser.add_argument(
        "--source-root",
        "--package-root",
        dest="source_root",
        type=Path,
        default=pins.DEFAULT_SOURCE_ROOT,
        help="repository/worktree root containing the pinned commits",
    )
    parser.add_argument(
        "--stage-dir",
        type=Path,
        default=RETURN / ".runtime" / "source-tree",
        help="in-checkout exact source extraction root",
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=RETURN / ".runtime" / "work",
        help="in-checkout transient scenario state root",
    )
    parser.add_argument(
        "--logs-dir",
        type=Path,
        default=RETURN / "logs",
        help="in-checkout log output root",
    )
    parser.add_argument(
        "--evidence-dir",
        type=Path,
        default=RETURN / "evidence",
        help="in-checkout evidence output root",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="final harness JSON path",
    )
    parser.add_argument("--s45-return", type=Path, default=None)
    parser.add_argument("--s46-return", type=Path, default=None)
    parser.add_argument("--s47-return", type=Path, default=None)
    parser.add_argument("--join-e-return", type=Path, default=None)
    parser.add_argument("--language-return", type=Path, default=None)
    parser.add_argument(
        "--pinned-path",
        action="append",
        default=[],
        metavar="KEY=PATH",
        help=(
            "explicit pinned path for any pin key: "
            + ",".join(sorted(pins.PINS))
        ),
    )
    parser.add_argument(
        "--original-tests",
        choices=("all", "s47", "none"),
        default="all",
        help="run original focused S45/S46/S47 tests, only S47, or none",
    )
    parser.add_argument(
        "--test-timeout",
        type=int,
        default=900,
        help="per original-test-suite timeout in seconds",
    )
    parser.add_argument(
        "--reuse-stage",
        action="store_true",
        help="keep an existing stage instead of extracting it again",
    )
    parser.add_argument(
        "--keep-work",
        action="store_true",
        help="keep transient scenario state under --work-dir",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    started = time.time()
    args = build_parser().parse_args(argv)
    source_root = args.source_root.expanduser().resolve()
    stage = args.stage_dir.expanduser().resolve()
    work_dir = args.work_dir.expanduser().resolve()
    logs_dir = args.logs_dir.expanduser().resolve()
    evidence_dir = args.evidence_dir.expanduser().resolve()
    logs_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    json_out = (
        args.json_out.expanduser().resolve()
        if args.json_out
        else evidence_dir / "harness_run.json"
    )
    explicit = _parse_pinned_paths(args.pinned_path)
    for key, value in (
        ("s45", args.s45_return),
        ("s46", args.s46_return),
        ("s47", args.s47_return),
        ("join_e", args.join_e_return),
        ("language", args.language_return),
    ):
        if value is not None:
            explicit[key] = value
    try:
        stage_manifest = pins.stage_sources(
            source_root=source_root,
            stage=stage,
            explicit_paths=explicit,
            refresh=not args.reuse_stage,
        )
        runtime = _configure_runtime(stage)
        origins = pins.module_origins(stage, MODULE_NAMES)
        original_tests = _run_original_tests(
            source_root=source_root,
            stage=stage,
            logs_dir=logs_dir,
            evidence_dir=evidence_dir,
            selection=args.original_tests,
            timeout=args.test_timeout,
        )
        if work_dir.exists():
            shutil.rmtree(work_dir)
        scenarios = run_scenarios(work_dir)
        pin_checks = _pin_checks(stage_manifest, origins)
        checks = {
            **scenarios["checks"],
            **{key: value for key, value in pin_checks.items()
               if isinstance(value, bool)},
            **{
                "original_tests_" + key: value
                for key, value in original_tests["checks"].items()
            },
        }
        report = {
            "schema": "SOROK_S45_S47_CAUSAL_HARNESS@1",
            "result": (
                "PASS"
                if all(checks.values())
                and scenarios["all_checks_pass"]
                and original_tests.get("all_checks_pass", True)
                else "FAIL"
            ),
            "grade": (
                "TEST_ONLY_ENGINEERING_CAUSAL_REGRESSION_"
                "NOT_INDEPENDENT_FINAL_REVIEW"
            ),
            "commission": {
                "base": pins.COMMISSION_BASE,
                "return": str(RETURN),
                "independent_final_review": False,
                "product_code_modified": False,
            },
            "environment": {
                "python": sys.version,
                "python_executable": sys.executable,
                "platform": platform.platform(),
                "host": platform.node(),
                "cwd": str(Path.cwd()),
                "pytest": _pytest_version(),
            },
            "inputs": {
                "source_root": str(source_root),
                "stage_dir": str(stage),
                "work_dir": str(work_dir),
                "explicit_paths": stage_manifest["explicit_paths"],
                "pins": stage_manifest["pins"],
            },
            "runtime_roots": runtime["roots"],
            "imports": origins,
            "source_manifest": stage_manifest,
            "original_tests": original_tests,
            "scenarios": scenarios,
            "checks": checks,
            "all_checks_pass": all(checks.values()),
            "limitations": [
                "TEST_ONLY engineering evidence over sourcefree synthetic roots.",
                "Not native C8/C9/C12, CAN008/CAN011, ADP, Pyat or human issuance.",
                "Not an independent final review or acceptance.",
                "No product code, expected psychology or other worker files changed.",
                "Supported S47 qualification refuses a foreign-root source; "
                "private-hook source injection outside that seam is not exercised.",
                "No external channel, human trial, provider call or paid action.",
            ],
            "commands": {
                "harness": " ".join([sys.executable, *sys.argv]),
                "original_tests": [
                    row["command"]
                    for row in original_tests["rows"].values()
                ],
            },
            "elapsed_seconds": round(time.time() - started, 3),
        }
        _json_dump(json_out, report)
        if not args.keep_work:
            shutil.rmtree(work_dir, ignore_errors=True)
        print(json.dumps({
            "result": report["result"],
            "json": str(json_out),
            "checks": report["checks"],
            "actual": {
                "root_hash": scenarios["actual"]["root_hash"],
                "material_after_interval": scenarios["actual"][
                    "material_after_interval"
                ],
                "c9_material_eligible": scenarios["actual"]["c9"][
                    "objective_material_eligible"
                ],
                "do_help": scenarios["actual"]["s45"]["do_help_strategy"],
            },
            "scheduled": {
                "root_hash": scenarios["scheduled"]["root_hash"],
                "material_after_interval": scenarios["scheduled"][
                    "material_after_interval"
                ],
                "c9_material_eligible": scenarios["scheduled"]["c9"][
                    "objective_material_eligible"
                ],
                "do_help": scenarios["scheduled"]["s45"]["do_help_strategy"],
            },
            "sever_restore": {
                "cut": scenarios["sever_restore"]["cut"],
                "restored_source_same": scenarios["sever_restore"][
                    "restored_source_same"
                ],
            },
            "wrong_root": {
                "roots_differ": scenarios["wrong_root"]["roots_differ"],
                "unresealed": scenarios["wrong_root"]["unresealed_foreign"],
                "resealed": scenarios["wrong_root"]["resealed_foreign"],
            },
            "original_tests": {
                key: row["counts"]
                for key, row in original_tests["rows"].items()
            },
        }, indent=2, sort_keys=True))
        return 0 if report["result"] == "PASS" else 1
    except Exception as exc:
        failure = {
            "schema": "SOROK_S45_S47_CAUSAL_HARNESS_FAILURE@1",
            "result": "ERROR",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
            "source_root": str(source_root),
            "stage_dir": str(stage),
            "commands": " ".join([sys.executable, *sys.argv]),
            "elapsed_seconds": round(time.time() - started, 3),
        }
        _json_dump(evidence_dir / "harness_failure.json", failure)
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 2


def _pytest_version() -> str:
    try:
        import pytest

        return getattr(pytest, "__version__", "unknown")
    except Exception:
        return "unavailable"


if __name__ == "__main__":
    raise SystemExit(main())
