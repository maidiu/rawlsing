#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def run(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Reproduce Section 85 from its packaged canary archive and compare all authority hashes.")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--section", type=Path, required=True)
    parser.add_argument("--work-root", type=Path, default=None)
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    section = args.section.resolve()
    managed_temp = None
    if args.work_root is None:
        managed_temp = tempfile.TemporaryDirectory(prefix="section85_reproduction_")
        work = Path(managed_temp.name)
    else:
        work = args.work_root.resolve()
        if work.exists():
            shutil.rmtree(work)
        work.mkdir(parents=True)

    section_copy = work / "section"
    shutil.copytree(section, section_copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"))
    for name in ("authority", "outputs", "logs", "validation", "manifests"):
        target = section_copy / name
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True, exist_ok=True)

    unpack = run(["bash", str(section_copy / "unpack_canary_archive.sh"), str(work / "canary_work")])
    canary = work / "canary_work" / "universality_9family_20var_v550_552_after_bridge_repair_20260729T074523Z"
    build = run([
        sys.executable, str(section_copy / "code/build_bounded_v550j_authority.py"),
        "--repo-root", str(repo),
        "--canary-root", str(canary),
        "--output-dir", str(section_copy / "authority"),
        "--adjudications-path", str(section_copy / "inputs/BOUNDED_JOINT_CONFIGURATION_ADJUDICATIONS.json"),
    ]) if unpack.returncode == 0 else subprocess.CompletedProcess([], 1, "", "unpack failed")
    audit = run([
        sys.executable, str(section_copy / "code/audit_canary_archive_truth.py"),
        "--section", str(section_copy),
        "--canary-root", str(canary),
    ]) if build.returncode == 0 else subprocess.CompletedProcess([], 1, "", "build failed")
    plan = run([
        sys.executable, str(section_copy / "code/run_bounded_nine_v550j_v551j_v552j.py"),
        "--repo-root", str(repo),
        "--section", str(section_copy),
        "--canary-root", str(canary),
        "--output-root", str(work / "plan"),
        "--db-url", "postgresql://placeholder/not-used-in-plan",
        "--plan-only",
    ]) if audit.returncode == 0 else subprocess.CompletedProcess([], 1, "", "audit failed")

    original = section / "authority"
    regenerated = section_copy / "authority"
    original_files = {p.relative_to(original).as_posix(): p for p in original.rglob("*") if p.is_file()}
    regenerated_files = {p.relative_to(regenerated).as_posix(): p for p in regenerated.rglob("*") if p.is_file()}
    rows: list[dict[str, Any]] = []
    mismatches: list[str] = []
    for relative in sorted(set(original_files) | set(regenerated_files)):
        original_path = original_files.get(relative)
        regenerated_path = regenerated_files.get(relative)
        original_hash = sha256_file(original_path) if original_path else ""
        regenerated_hash = sha256_file(regenerated_path) if regenerated_path else ""
        matches = bool(original_path and regenerated_path and original_hash == regenerated_hash)
        rows.append({
            "file": relative,
            "original_exists": bool(original_path),
            "regenerated_exists": bool(regenerated_path),
            "original_sha256": original_hash,
            "regenerated_sha256": regenerated_hash,
            "match": matches,
        })
        if not matches:
            mismatches.append(relative)

    audit_payload = json.loads((section_copy / "outputs/CANARY_ARCHIVE_TRUTH_AUDIT.json").read_text()) if audit.returncode == 0 else {}
    plan_path = work / "plan/reports/bounded_nine_canary_execution_plan.json"
    plan_payload = json.loads(plan_path.read_text()) if plan.returncode == 0 and plan_path.exists() else {}
    plans = plan_payload.get("plan", [])
    association_mode = plan_payload.get("preflight", {}).get("association_mode", "")
    archive_path = section_copy / "inputs/universality_9family_20var_v550_552_after_bridge_repair_20260729T074523Z.zip"

    passed = (
        unpack.returncode == 0
        and build.returncode == 0
        and audit.returncode == 0
        and plan.returncode == 0
        and not mismatches
        and audit_payload.get("status") == "PASS_STATIC_CANARY_ARCHIVE_TRUTH_AUDIT"
        and len(plans) == 9
        and association_mode == "off"
    )
    result = {
        "status": "PASS_SECTION85_SELF_CONTAINED_REPRODUCTION" if passed else "FAIL_SECTION85_SELF_CONTAINED_REPRODUCTION",
        "authority_file_count": len(rows),
        "authority_hash_matches": sum(bool(row["match"]) for row in rows),
        "authority_hash_mismatches": mismatches,
        "archive_truth_audit_status": audit_payload.get("status", "NOT_RUN"),
        "plan_scope_count": len(plans),
        "plan_association_mode": association_mode,
        "source_archive_sha256": sha256_file(archive_path) if archive_path.exists() else "",
        "process_returns": {
            "unpack": unpack.returncode,
            "build": build.returncode,
            "audit": audit.returncode,
            "plan": plan.returncode,
        },
        "process_stderr": {
            "unpack": unpack.stderr[-2000:],
            "build": build.stderr[-2000:],
            "audit": audit.stderr[-2000:],
            "plan": plan.stderr[-2000:],
        },
        "rows": rows,
    }

    validation = section / "validation"
    validation.mkdir(parents=True, exist_ok=True)
    (validation / "SECTION85_SELF_CONTAINED_REPRODUCTION_RETURN.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (validation / "SECTION85_SELF_CONTAINED_REPRODUCTION_MATRIX.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "original_exists", "regenerated_exists", "original_sha256", "regenerated_sha256", "match"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps({key: value for key, value in result.items() if key not in {"rows", "process_stderr"}}, indent=2, sort_keys=True))
    if managed_temp is not None:
        managed_temp.cleanup()
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
