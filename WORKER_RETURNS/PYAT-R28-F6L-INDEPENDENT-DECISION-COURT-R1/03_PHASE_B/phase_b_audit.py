"""F6L Phase-B audit of the governed F6K return.

Reads the F6K branch through git objects only; writes an audit receipt.  It does
not modify F6K, F6J or the author tree.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
F6K = "537cb5195bf4f51ee4abc0ce097155c3a3a69291"
F6K_START = "813742d970d5484a53b7eac2fa3ba2fa76297432"
F6K_DIR = "WORKER_RETURNS/PYAT-R28-F6K-F6-DECISION-ADMISSION-REPAIR-R1"
F6J = "825b2d8050b550f1d52d3129883584fee2ef36c2"
F6J_FREEZE = "e476ccc090ae0175a540e94c5c382d7e2a8453f0"
F6C = "9aa0e7d3a0cf9ab7654ce8e3d5cb15060235a48f"
NATIVE_SOURCE = "1428c2e92bce1a49efd87378cb23df936d646dc5"
NATIVE_BLOB = "fc5e37fa5b2f0eb689593b42d95479d1327cb94c"


def git(*args):
    return subprocess.run(["git", *args], cwd=str(RET), capture_output=True,
                          text=True, check=True).stdout


def blob(commit, path):
    return git("rev-parse", f"{commit}:{path}").strip()


def main():
    tip = git("rev-parse", "origin/agent/rabochii-pyat-r28-f6k-decision-admission-consumer-contract-repair-r1").strip()
    files = [p for p in git("ls-tree", "-r", "--name-only", "--full-tree", tip).splitlines()
             if p.startswith(F6K_DIR + "/")]
    map_text = git("show", f"{tip}:{F6K_DIR}/01_DEFECT_REPAIR_MAP.json")
    status_text = git("show", f"{tip}:{F6K_DIR}/00_REPAIR_STATUS.md")
    repair_map = json.loads(map_text)
    py_files = [p for p in files if p.endswith(".py")]
    producer_changes = git("diff", "--name-only", F6K_START, tip, "--",
                           "rawlsing_next/pre553_heterogeneous_synthesis.py").splitlines()

    # F6J commit delta-only check
    f6j_delta = git("diff-tree", "--no-commit-id", "--name-only", "-r", F6J).splitlines()
    f6j_ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", F6J_FREEZE, F6J],
        cwd=str(RET), capture_output=True, text=True).returncode == 0

    # Native producer absent at the F6L sealed startup.
    startup_has_producer = subprocess.run(
        ["git", "cat-file", "-e", f"31123f370af50bdf036cab32dd6d7594b36a5f22:rawlsing_next/pre553_heterogeneous_synthesis.py"],
        cwd=str(RET), capture_output=True, text=True).returncode == 0

    # Exact code-site attribution, from the staged producer bytes.
    src = (RET / "01_STAGED_NATIVE/rawlsing_next/pre553_heterogeneous_synthesis.py").read_text()
    lines = src.splitlines()
    sites = {
        "decision_null_defect": {
            "line": 343,
            "code": lines[342].strip(),
            "file": "rawlsing_next/pre553_heterogeneous_synthesis.py",
        },
        "baseline_admission_bypass": {
            "line": 210,
            "code": lines[209].strip(),
            "file": "rawlsing_next/pre553_heterogeneous_synthesis.py",
        },
        "transport_admission_bypass": {
            "line": 221,
            "code": lines[220].strip(),
            "file": "rawlsing_next/pre553_heterogeneous_synthesis.py",
        },
        "mapped_node_missing_ceiling": {
            "line": 259,
            "code": "\n".join(lines[258:262]).strip(),
            "file": "rawlsing_next/pre553_heterogeneous_synthesis.py",
        },
        "stratum_total_support_gate": {
            "line": 282,
            "code": lines[281].strip(),
            "file": "rawlsing_next/pre553_heterogeneous_synthesis.py",
        },
        "author_path_suffix_control": {
            "line": 69,
            "code": (RET / "01_SOURCE_TRANSPORT/F6C_RUNTIME/02_TESTS/test_f6c_frozen_court.py")
                    .read_text().splitlines()[68].strip(),
            "file": "WORKER_RETURNS/PYAT-R23-F6C-NATIVE-F6-COMPARATIVE-CONTINUATION-R1/02_TESTS/test_f6c_frozen_court.py",
        },
    }

    # F6K map attribution is not code-accurate.
    attribution_errors = []
    for item in repair_map["repair_map"]:
        actual = None
        if item["id"] == 1:
            actual = sites["decision_null_defect"]["file"]
        elif item["id"] in (2, 3):
            actual = sites["baseline_admission_bypass"]["file"]
        elif item["id"] == 4:
            actual = sites["mapped_node_missing_ceiling"]["file"]
        elif item["id"] == 5:
            actual = sites["stratum_total_support_gate"]["file"]
        elif item["id"] == 6:
            actual = sites["author_path_suffix_control"]["file"]
        claimed = item["file"]
        if actual and actual not in claimed:
            attribution_errors.append({
                "id": item["id"], "claimed_file": claimed, "actual_file": actual,
                "defect": item["defect"],
            })

    payload = {
        "schema": "PYAT_R28_F6L_F6K_RETURN_AUDIT@1",
        "f6k_branch": "agent/rabochii-pyat-r28-f6k-decision-admission-consumer-contract-repair-r1",
        "f6k_startup": F6K_START,
        "f6k_tip": tip,
        "f6k_return_files": files,
        "f6k_return_python_files": py_files,
        "f6k_return_file_hashes": {
            p: hashlib.sha256(git("show", f"{tip}:{p}").encode()).hexdigest()
            for p in files
        },
        "f6k_status_outcome": repair_map.get("outcome"),
        "f6k_repair_code_shipped": repair_map.get("repair_code_shipped"),
        "f6k_suites_executed": repair_map.get("suites_executed"),
        "f6k_has_repair_code": bool(py_files),
        "f6k_changed_native_producer": producer_changes,
        "f6k_status_terminal": repair_map.get("terminal"),
        "f6j_commit_delta_only": f6j_delta,
        "f6j_freeze_is_ancestor": f6j_ancestor,
        "native_producer_absent_at_f6l_startup": not startup_has_producer,
        "native_source_commit": NATIVE_SOURCE,
        "native_producer_git_blob": NATIVE_BLOB,
        "exact_code_sites": sites,
        "f6k_attribution_errors": attribution_errors,
        "review_conclusion": (
            "F6K is a typed hold with no repair code and no executed suite. "
            "Its split of F6J findings is directionally correct, but its defect "
            "map attributes producer defects to fixture/consumer files and is not "
            "a code-accurate repair plan. No repaired candidate exists for Phase-B "
            "acceptance."
        ),
        "status_text_sha256": hashlib.sha256(status_text.encode()).hexdigest(),
        "map_text_sha256": hashlib.sha256(map_text.encode()).hexdigest(),
    }
    out = RET / "03_PHASE_B/00_F6K_RETURN_AUDIT.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in payload.items()
                      if k not in ("exact_code_sites", "f6k_return_file_hashes")},
                     indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
