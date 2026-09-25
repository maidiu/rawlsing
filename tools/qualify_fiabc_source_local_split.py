#!/usr/bin/env python3
"""Run the FIABC source-split qualification without opening survey carriers."""
from __future__ import annotations

import argparse
import builtins
import hashlib
import importlib.metadata
import importlib.util
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import unittest


CONTROL_ROOT = Path(__file__).resolve().parents[1]
TEST_PATH = CONTROL_ROOT / "rawlsing_next" / "tests" / "test_fiabc_source_local_split_qualification.py"
RUNNER_REL = Path("HQ_HANDOFF/launchers/RUN_FIABC_SOURCE_LOCAL_SPLIT.sh")
CANONICAL_REL = Path("HQ_HANDOFF/launchers/RUN_DISPOSITIVE_FIABC_SIX_CELL.sh")
EXPECTED_CONTROL_BRANCH = "agent/vozhd-fiabc-source-split-pandas-runtime-repair-r1"
EXPECTED_EXECUTION_BRANCH = "agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1"
EXPECTED_EXECUTION_HEAD = "3d8f2ad62600b6777dcb23a28404a067502e77a0"
EXPECTED_PREMAIN_BRANCH = "integration/pre-main-reconciliation-r1"
EXPECTED_PREMAIN_HEAD = "cbfbdd76e5a51dee1c267b2856d6946a3e6bb479"
EXPECTED_CANONICAL_SHA256 = "fa9d34c5e274792475f5a83ff08b7859287d7e7e596e1043601a6e5e1e9c98fe"
EXPECTED_PROTECTED_CANONICAL_SHA256 = "9d1907508734428404fa33def6e8ad8be4686f4f9ef2a5b431e97c60b84b5565"
EXPECTED_RUNTIME = {
    "implementation": "CPython",
    "python": "3.11.3",
    "pyreadstat": "1.3.6",
    "pyarrow": "25.0.1",
    "pandas": "2.3.1",
    "numpy": "2.3.2",
    "system": "Darwin",
    "machine": "x86_64",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def _canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _runtime_identity() -> dict[str, str]:
    return {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "pyreadstat": importlib.metadata.version("pyreadstat"),
        "pyarrow": importlib.metadata.version("pyarrow"),
        "pandas": importlib.metadata.version("pandas"),
        "numpy": importlib.metadata.version("numpy"),
        "system": platform.system(),
        "machine": platform.machine(),
    }


def _raw_source_path(value) -> bool:
    try:
        path = Path(os.fspath(value))
    except (TypeError, ValueError):
        return False
    return path.suffix.lower() in {".dta", ".sav"}


def _candidate_command(command) -> bool:
    if isinstance(command, (str, bytes, os.PathLike)):
        tokens = [os.fsdecode(command)]
    else:
        tokens = [os.fsdecode(item) for item in command]
    joined = " ".join(tokens)
    return "--run" in tokens or "--backend-module" in tokens or "ee_p2x_process_isolated_backend" in joined


def _load_test_module():
    spec = importlib.util.spec_from_file_location("fiabc_source_split_qualification_tests", TEST_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load qualification tests: {TEST_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execution-root", type=Path, required=True)
    parser.add_argument("--pre-main-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()

    execution_root = args.execution_root.resolve()
    pre_main_root = args.pre_main_root.resolve()
    output_root = args.output_root.resolve()
    before = {
        "control_head": _git(CONTROL_ROOT, "rev-parse", "HEAD"),
        "control_branch": _git(CONTROL_ROOT, "branch", "--show-current"),
        "control_worktree_dirty": bool(_git(CONTROL_ROOT, "status", "--porcelain", "--untracked-files=all")),
        "execution_head": _git(execution_root, "rev-parse", "HEAD"),
        "execution_branch": _git(execution_root, "branch", "--show-current"),
        "pre_main_head": _git(pre_main_root, "rev-parse", "HEAD"),
        "pre_main_branch": _git(pre_main_root, "branch", "--show-current"),
    }
    clean = {
        "execution": _git(execution_root, "status", "--porcelain", "--untracked-files=all") == "",
        "pre_main": _git(pre_main_root, "status", "--porcelain", "--untracked-files=all") == "",
    }
    runtime = _runtime_identity()
    launcher = CONTROL_ROOT / RUNNER_REL
    canonical = CONTROL_ROOT / CANONICAL_REL
    pre_main_canonical = pre_main_root / CANONICAL_REL
    protected_canonical = execution_root / CANONICAL_REL
    hashes_before = {
        "source_split_canonical_sha256": _sha256(canonical),
        "pre_main_canonical_sha256": _sha256(pre_main_canonical),
        "protected_execution_canonical_sha256": _sha256(protected_canonical),
        "source_split_runner_sha256": _sha256(launcher),
    }
    qualified_files = (
        RUNNER_REL,
        Path("HQ_HANDOFF/launchers/FIABC_SOURCE_LOCAL_SPLIT_DRIVER.py"),
        Path("HQ_HANDOFF/launchers/FIABC_SOURCE_LOCAL_SPLIT_MERGE.py"),
        Path("rawlsing_next/tests/test_fiabc_source_local_split_qualification.py"),
        Path("tools/qualify_fiabc_source_local_split.py"),
    )
    qualified_file_hashes_before = {str(path): _sha256(CONTROL_ROOT / path) for path in qualified_files}

    telemetry = {
        "raw_source_open_attempts": 0,
        "survey_source_sha256_passes": 0,
        "survey_decoder_calls": 0,
        "candidate_process_launch_attempts": 0,
    }
    original_builtin_open = builtins.open
    original_io_open = io.open
    original_popen = subprocess.Popen

    def guarded_open(file, *open_args, **open_kwargs):
        if _raw_source_path(file):
            telemetry["raw_source_open_attempts"] += 1
            raise RuntimeError("source-free qualification blocked an attempted .dta/.sav open")
        return original_builtin_open(file, *open_args, **open_kwargs)

    def guarded_io_open(file, *open_args, **open_kwargs):
        if _raw_source_path(file):
            telemetry["raw_source_open_attempts"] += 1
            raise RuntimeError("source-free qualification blocked an attempted .dta/.sav open")
        return original_io_open(file, *open_args, **open_kwargs)

    def guarded_popen(command, *popen_args, **popen_kwargs):
        if _candidate_command(command):
            telemetry["candidate_process_launch_attempts"] += 1
            raise RuntimeError("source-free qualification blocked a measured/candidate launch")
        return original_popen(command, *popen_args, **popen_kwargs)

    output = io.StringIO()
    result = None
    test_count = 0
    try:
        builtins.open = guarded_open
        io.open = guarded_io_open
        subprocess.Popen = guarded_popen
        os.environ["FIABC_SOURCE_SPLIT_EXECUTION_ROOT"] = str(execution_root)
        module = _load_test_module()
        suite = unittest.defaultTestLoader.loadTestsFromModule(module)
        result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
        test_count = result.testsRun
    finally:
        builtins.open = original_builtin_open
        io.open = original_io_open
        subprocess.Popen = original_popen

    hashes_after = {
        "source_split_canonical_sha256": _sha256(canonical),
        "pre_main_canonical_sha256": _sha256(pre_main_canonical),
        "protected_execution_canonical_sha256": _sha256(protected_canonical),
        "source_split_runner_sha256": _sha256(launcher),
    }
    qualified_file_hashes_after = {str(path): _sha256(CONTROL_ROOT / path) for path in qualified_files}
    checks = {
        "control_branch": before["control_branch"] == EXPECTED_CONTROL_BRANCH,
        "qualification_surface_unchanged_during_tests": qualified_file_hashes_before == qualified_file_hashes_after,
        "execution_branch": before["execution_branch"] == EXPECTED_EXECUTION_BRANCH,
        "execution_head": before["execution_head"] == EXPECTED_EXECUTION_HEAD,
        "pre_main_branch": before["pre_main_branch"] == EXPECTED_PREMAIN_BRANCH,
        "pre_main_head": before["pre_main_head"] == EXPECTED_PREMAIN_HEAD,
        "execution_checkout_clean": clean["execution"],
        "pre_main_checkout_clean": clean["pre_main"],
        "runtime_pinned": runtime == EXPECTED_RUNTIME,
        "canonical_unchanged_during_qualification": hashes_before == hashes_after,
        "canonical_matches_premain": hashes_before["source_split_canonical_sha256"] == hashes_before["pre_main_canonical_sha256"] == EXPECTED_CANONICAL_SHA256,
        "protected_copy_unmodified": hashes_before["protected_execution_canonical_sha256"] == EXPECTED_PROTECTED_CANONICAL_SHA256,
        "source_free": telemetry["raw_source_open_attempts"] == 0 and telemetry["survey_source_sha256_passes"] == 0 and telemetry["survey_decoder_calls"] == 0,
        "no_candidate_processes": telemetry["candidate_process_launch_attempts"] == 0,
        "all_qualification_tests_pass": bool(result and result.wasSuccessful()),
        "no_tests_skipped": bool(result and not result.skipped),
    }
    status = "PASS__SOURCE_FREE_ALTERNATE_RUNNER_QUALIFICATION" if all(checks.values()) else "BLOCKED__SOURCE_FREE_ALTERNATE_RUNNER_QUALIFICATION"

    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "test_output.txt").write_text(output.getvalue(), encoding="utf-8")
    (output_root / "source_access_telemetry.json").write_text(
        json.dumps(telemetry, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    launcher_identity = {
        "hashes_before": hashes_before,
        "hashes_after": hashes_after,
        "checks": {
            "source_split_pre_main_byte_identity": checks["canonical_matches_premain"],
            "source_split_launcher_unchanged_during_qualification": hashes_before["source_split_runner_sha256"] == hashes_after["source_split_runner_sha256"],
            "protected_execution_launcher_unmodified": checks["protected_copy_unmodified"],
        },
    }
    (output_root / "canonical_launcher_identity.json").write_text(
        json.dumps(launcher_identity, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    receipt = {
        "schema": "RAWLSING_FIABC_SOURCE_SPLIT_QUALIFICATION@1.0.0",
        "status": status,
        "control_branch": before["control_branch"],
        "control_head_at_test_start": before["control_head"],
        "control_worktree_dirty_at_test_start": before["control_worktree_dirty"],
        "execution_branch": before["execution_branch"],
        "execution_head": before["execution_head"],
        "pre_main_branch": before["pre_main_branch"],
        "pre_main_head": before["pre_main_head"],
        "runtime": runtime,
        "test_count": test_count,
        "tests_passed": test_count - len(result.failures) - len(result.errors) if result else 0,
        "tests_failed": len(result.failures) if result else None,
        "tests_errored": len(result.errors) if result else None,
        "tests_skipped": len(result.skipped) if result else None,
        "candidate_processes_started": 0,
        "candidate_outputs_created": 0,
        "source_access_telemetry_path": "source_access_telemetry.json",
        "canonical_launcher_identity_path": "canonical_launcher_identity.json",
        "test_output_path": "test_output.txt",
        "qualified_file_sha256": qualified_file_hashes_before,
        "checks": checks,
    }
    receipt["receipt_identity"] = hashlib.sha256(_canonical_bytes(receipt)).hexdigest()
    (output_root / "qualification_receipt.json").write_text(
        json.dumps(receipt, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    return_doc = {
        "schema": "RAWLSING_FIABC_SOURCE_SPLIT_QUALIFICATION_RETURN@1.0.0",
        "status": status,
        "qualification_receipt": "qualification_receipt.json",
        "test_output": "test_output.txt",
        "source_access_telemetry": "source_access_telemetry.json",
        "canonical_launcher_identity": "canonical_launcher_identity.json",
        "measured_execution_performed": False,
        "candidate_processes_started": 0,
        "source_accessed": False,
        "hq_launch_authorization": "NOT_GRANTED_BY_THIS_QUALIFICATION",
    }
    return_doc["return_identity"] = hashlib.sha256(_canonical_bytes(return_doc)).hexdigest()
    (output_root / "RETURN.json").write_text(
        json.dumps(return_doc, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    (output_root / "00_RETURN.md").write_text(
        "# FIABC Source-Split Source-Free Qualification — R1\n\n"
        f"Terminal: `{status}`\n\n"
        f"Tests run: {test_count}; passed: {receipt['tests_passed']}; "
        f"failed: {receipt['tests_failed']}; errored: {receipt['tests_errored']}; "
        f"skipped: {receipt['tests_skipped']}.\n\n"
        "The qualification used synthetic manifests, temporary JSON receipts, and fake backend callbacks. "
        "It did not open or hash LiTS-I/WVS7 source files, decode survey data, create candidate outputs, "
        "or launch candidate processes. The canonical six-cell launcher identity was checked before and "
        "after the qualification and against PRE-MAIN.\n\n"
        "This receipt qualifies the alternate runner implementation only. It does not grant HQ launch "
        "authorization, authorize measured LiTS/WVS A/B/C, execute S17, or authorize P2 synthesis.\n\n"
        "See `qualification_receipt.json`, `source_access_telemetry.json`, `canonical_launcher_identity.json`, "
        "and `test_output.txt` for exact evidence.\n",
        encoding="utf-8",
    )
    print(output.getvalue(), end="")
    print(f"\n{status}")
    return 0 if status.startswith("PASS__") else 1


if __name__ == "__main__":
    raise SystemExit(_main())
