"""Offline source-integrity gate for the byte-exact C9-R3B TEST_ONLY recovery.

This is an engineering provenance gate, NOT a C9 original-science or runtime grant.
Run:
  python3 verify_recovered_source.py
  python3 verify_recovered_source.py --pytest
  python3 verify_recovered_source.py --pytest --allow-skips-for-recon-only

A test exit 0 with source-dependent skips is NEVER a full-acceptance PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "RECOVERY_SOURCE_MANIFEST_R1.json"


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def inspect_sources() -> dict:
    spec = json.loads(MANIFEST.read_text(encoding="utf-8"))
    checked = {}
    for relative, original_blob in spec["source_files"].items():
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError("MISSING_RECOVERED_SOURCE:" + relative)
        actual = git_blob_sha1(path.read_bytes())
        if actual != original_blob:
            raise RuntimeError(
                "ORIGINAL_SOURCE_MISMATCH:" + relative + ":"
                + original_blob + "!=" + actual
            )
        checked[relative] = actual
    return {"source_status": "EXACT_GIT_BLOBS", "source_files": checked}


def run_pytest(allow_source_skips: bool) -> dict:
    with tempfile.TemporaryDirectory(prefix="sorok-c9r3-recovery-") as work:
        xml_path = Path(work) / "junit.xml"
        command = [
            sys.executable, "-m", "pytest", "-q",
            str(ROOT / "tests" / "test_c9_r3.py"),
            "--junitxml", str(xml_path),
        ]
        result = subprocess.run(
            command, cwd=ROOT, text=True,
            capture_output=True, check=False,
        )
        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
        if not xml_path.is_file():
            raise RuntimeError("PYTEST_NO_JUNIT__NO_EXECUTION_PROOF")
        tree = ET.parse(xml_path).getroot()
        suites = [tree] if tree.tag == "testsuite" else list(tree.findall(".//testsuite"))
        if not suites:
            raise RuntimeError("JUNIT_MISSING_SUITE")
        totals = {
            attr: sum(int(s.get(attr, "0")) for s in suites)
            for attr in ("tests", "failures", "errors", "skipped")
        }
        verdict = {
            "scope": "SYN02_C9_R3B_SOURCEFREE_ONLY",
            "return_code": result.returncode,
            "totals": totals,
            "complete_proof": (
                result.returncode == 0
                and totals["tests"] == 15
                and totals["failures"] == 0
                and totals["errors"] == 0
                and totals["skipped"] == 0
            ),
            "source_dependence": "S36_C12_LEGACY_ABSOLUTE_PATHS_IN_ORIGINAL_TESTS",
        }
        if result.returncode != 0 or totals["tests"] != 15:
            raise RuntimeError("SOURCEFREE_TESTS_FAILED_OR_WRONG_COUNT:" + str(verdict))
        if totals["skipped"] and not allow_source_skips:
            raise RuntimeError("PARTIAL_ONLY__SKIPPED_SOURCE_COURTS__NOT_ACCEPTED:" + str(verdict))
        if totals["skipped"]:
            verdict["acceptance"] = "RECON_ONLY__NOT_FULL_COURT"
        else:
            verdict["acceptance"] = "TEST_ONLY_SOURCEFREE_COURT__NO_NATIVE"
        return verdict


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pytest", action="store_true")
    parser.add_argument("--allow-skips-for-recon-only", action="store_true")
    args = parser.parse_args()
    print(json.dumps(inspect_sources(), sort_keys=True))
    if args.pytest:
        verdict = run_pytest(args.allow_skips_for_recon_only)
        print(json.dumps(verdict, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, ValueError) as exc:
        print("HOLD:", exc, file=sys.stderr)
        raise SystemExit(2)
