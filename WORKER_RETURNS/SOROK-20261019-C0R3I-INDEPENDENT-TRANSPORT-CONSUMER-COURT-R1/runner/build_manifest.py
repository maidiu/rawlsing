#!/usr/bin/env python3
"""Build the C0R3 source and actual-import custody manifest."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
CAND = RETURN / "candidate"
RUNTIME = CAND / "stage" / "runtime"
LEDGER = CAND / "stage" / "_c0p_runtime_ledger.json"
OUT = RETURN / "01_SOURCE_AND_IMPORT_CUSTODY.json"
PATCHES = CAND / "patches"
PATCHES.mkdir(exist_ok=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(REPO), *args], text=True).strip()


def verify_git(commit: str, repo_path: str, file: Path):
    expected = git("rev-parse", f"{commit}:{repo_path}")
    actual = git_blob(file.read_bytes())
    return dict(commit=commit, repo_path=repo_path, expected_blob=expected,
                actual_blob=actual, match=expected == actual)


C0R2_COMMIT = "55d2daa4bab41c5ff4ffdc196c8d36d300c3d60f"
C0R2_PATH = ("WORKER_RETURNS/SOROK-V2-HQ323-C0R2-GIT-BACKED-REPAIR-R1/"
             "tests/test_c0r2_adversarial.py")
C0R2_BYTES = subprocess.check_output(
    ["git", "-C", str(REPO), "show", f"{C0R2_COMMIT}:{C0R2_PATH}"])
C0R2_TEST_LINE = C0R2_BYTES.decode().splitlines()[71]
C0R2_TEST_BLOB = git("rev-parse", f"{C0R2_COMMIT}:{C0R2_PATH}")
C0R2_TEST_SHA = hashlib.sha256(C0R2_BYTES).hexdigest()


def main() -> int:
    ledger = json.loads(LEDGER.read_text())
    native = []
    for row in ledger["ledger"]:
        path = RUNTIME / row["staged"]
        check = verify_git(row["commit"], row["repo_path"], path)
        native.append(dict(
            staged=row["staged"], source_commit=row["commit"],
            source_path=row["repo_path"], bytes=path.stat().st_size,
            git_blob=git_blob(path.read_bytes()), sha256=sha256(path),
            git_blob_match=check["match"],
            expected_git_blob=check["expected_blob"]))
    probe = subprocess.run(
        [sys.executable, "-B", str(RETURN / "runner" / "import_probe.py"),
         str(RETURN)], capture_output=True, text=True, check=True, cwd=RETURN)
    imports = json.loads(probe.stdout)
    original_files = {
        "original_c0p_first_author": ("154a4dd5615d47f014ca90eb1234b16e983bf5c1",
            "WORKER_RETURNS/SOROK-R3-HQ319-C0P-GENERIC-PORT-POSITIVE-R1/repro/c0p_two_contract_port.py",
            RETURN / "original/c0p_first_author.py"),
        "original_c0p_repaired_author": ("55d2daa4bab41c5ff4ffdc196c8d36d300c3d60f",
            "WORKER_RETURNS/SOROK-R3-HQ319-C0P-GENERIC-PORT-POSITIVE-R1/repro/c0p_two_contract_port.py",
            RETURN / "original/c0p_repaired_author.py"),
        "original_c0x_receiver": ("b02deee1bac9393921845caa657841c40408eaf6",
            "WORKER_RETURNS/SOROK-20261019-C0X-C0-C10-DUAL-OWNER-RECEIVER-COMPLETION-R1/c0x_world_receiver.py",
            RETURN / "original/c0x_world_receiver.py"),
    }
    originals = {}
    for name, (commit, repo_path, file) in original_files.items():
        check = verify_git(commit, repo_path, file)
        originals[name] = dict(commit=commit, repo_path=repo_path,
                               bytes=file.stat().st_size,
                               git_blob=git_blob(file.read_bytes()),
                               sha256=sha256(file), match=check["match"])
    historical_tests = {
        "c0p49": ("154a4dd5615d47f014ca90eb1234b16e983bf5c1",
                  "WORKER_RETURNS/SOROK-R3-HQ319-C0P-GENERIC-PORT-POSITIVE-R1/tests/test_c0p_generic_port.py"),
        "c0i50": ("2dacd87636352a6c805e03b3d07581193a06264b",
                  "WORKER_RETURNS/SOROK-R3-HQ320-C0I-C0P-INDEPENDENT-R1/repro/test_c0i.py"),
        "c0r2_23": ("55d2daa4bab41c5ff4ffdc196c8d36d300c3d60f",
                    "WORKER_RETURNS/SOROK-V2-HQ323-C0R2-GIT-BACKED-REPAIR-R1/tests/test_c0r2_adversarial.py"),
        "c0x_15": ("b02deee1bac9393921845caa657841c40408eaf6",
                   "WORKER_RETURNS/SOROK-20261019-C0X-C0-C10-DUAL-OWNER-RECEIVER-COMPLETION-R1/tests/test_c0x_receiving_consumer.py"),
        "k9_8": ("9831293f9fd53813db04d33be5bbdc177542f8ce",
                 "WORKER_RETURNS/PYAT-USERDIRECT-20261014-R5-SC0F3-REAL-OWNER-REPAIR-R1/repro/inputs/port/port/test_k9_provider_swap.py"),
        "k10_28": ("9831293f9fd53813db04d33be5bbdc177542f8ce",
                   "WORKER_RETURNS/PYAT-USERDIRECT-20261014-R5-SC0F3-REAL-OWNER-REPAIR-R1/repro/inputs/port/port/test_k10_structural_conservation.py"),
    }
    tests = {}
    for name, (commit, repo_path) in historical_tests.items():
        expected = git("rev-parse", f"{commit}:{repo_path}")
        tests[name] = dict(commit=commit, repo_path=repo_path,
                           git_blob=expected)
    corrected = {}
    for name, parent in (("facade", "original_c0p_repaired_author"),
                         ("receiver", "original_c0x_receiver")):
        file = (CAND / "upstream/c0p_two_contract_port.py") if name == "facade" \
            else (CAND / "c0x_world_receiver.py")
        corrected[name] = dict(path=file.relative_to(RETURN).as_posix(),
                               sha256=sha256(file), bytes=file.stat().st_size,
                               parent=parent,
                               parent_blob=originals[parent]["git_blob"])
        original_rel = ("original/c0p_repaired_author.py" if name == "facade"
                        else "original/c0x_world_receiver.py")
        target_rel = file.relative_to(RETURN).as_posix()
        diff = subprocess.run(
            ["diff", "-u", original_rel, target_rel], capture_output=True,
            text=True, cwd=RETURN)
        patch = PATCHES / (name + "_c0r3.patch")
        patch.write_text(diff.stdout)
        corrected[name]["patch"] = patch.relative_to(RETURN).as_posix()
        corrected[name]["patch_sha256"] = sha256(patch)
    manifest = dict(
        schema="SOROK_C0R3_SOURCE_AND_IMPORT_CUSTODY@1",
        sealed_startup="0a0f8e99d9117a88a51d67b3b2b51f4f618cbaab",
        branch="agent/rabochii-sorok-20261019-c0r3-c0x-endtoend-transport-repair-r1",
        native29=dict(count=len(native), all_git_blob_match=all(
            row["git_blob_match"] for row in native),
            total_bytes=sum(row["bytes"] for row in native),
            closure_resolves=ledger.get("closure_resolves"),
            modules=native),
        actual_imports=imports,
        originals=originals,
        corrected=corrected,
        historical_tests=tests,
        c0r2_vacuous_test=dict(
            commit="55d2daa4bab41c5ff4ffdc196c8d36d300c3d60f",
            path="WORKER_RETURNS/SOROK-V2-HQ323-C0R2-GIT-BACKED-REPAIR-R1/tests/test_c0r2_adversarial.py",
            test="test_r1_relocation_changes_no_consumer_value",
            original_line=72,
            line_text=C0R2_TEST_LINE,
            git_blob=C0R2_TEST_BLOB,
            sha256=C0R2_TEST_SHA,
            preserved_byte_exact=True,
            note="The inherited 'or True' line is not edited and is not counted as proof; the new relocation/source-consumer test replaces its evidentiary role."),
        native_adp_can_authority="NONE",
    )
    OUT.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n")
    print(json.dumps(dict(native=len(native), imports=len(imports),
                          native_all=manifest["native29"]["all_git_blob_match"],
                          originals_match=all(v["match"] for v in originals.values())),
                     indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
