#!/usr/bin/env python3
"""Read-only S0/S1 reproduction for issue #720 L4. No respondent/source execution.

Usage: python WORKER_RETURNS/PROGRAMMA-PYAT-AUTHORITY-RECLOSURE-20261106-R1/L4_V551J_V552J/07_REPRODUCE_S0_SCAN.py --repo /path/to/local/rawlsing
Requires the immutable protected commit in the local Git object database.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys

BASE = "fce43498e16e4709f3c9801e8717f0fdae18126a"
CALL_RX = re.compile(r"\b(?:read_table|_load|_read_json_object|_verify_and_read_declared|_read_manifest|_v2_hash_file|file_hash|sha256_file|read_status_document|inspect_artifact|load_cached_frame|write_cached_frame|capture_run_provenance|build_v551j_joint_outputs_v2|certify_v551j_v2_2_3|recompute_[\w]+|verify_[\w]+|validate_[\w]+|build_v552j_join|build_v552j_structural_handoff|build_thin_layer|pd\.read_\w+|json\.loads|yaml\.safe_load|\.read_text|\.read_bytes|\.to_parquet|\.to_csv|\.merge|\.groupby|\.execute)\s*\(")

def git_bytes(repo: Path, ref: str, path: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(repo), "show", f"{ref}:{path}"],
        capture_output=True, check=False,
    )
    if proc.returncode:
        raise RuntimeError(f"Cannot read {ref}:{path}: {proc.stderr.decode(errors='replace')}")
    return proc.stdout

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    lane = Path(__file__).resolve().parent
    with (lane / "01_SCANNED_FILES.tsv").open(newline="", encoding="utf-8") as f:
        scanned = list(csv.DictReader(f, delimiter="\t"))
    with (lane / "02_LEGACY_CALLSITES.csv").open(newline="", encoding="utf-8") as f:
        calls = list(csv.DictReader(f))
    by_path = {}
    errors = []
    for entry in scanned:
        path = entry["repo_path"]
        data = git_bytes(args.repo, BASE, path)
        if hashlib.sha256(data).hexdigest() != entry["file_bytes_sha256"]:
            errors.append(f"FILE_SHA256_MISMATCH:{path}")
        if len(data) != int(entry["utf8_bytes"]):
            errors.append(f"BYTE_COUNT_MISMATCH:{path}")
        text = data.decode("utf-8")
        if len(text.split("\n")) != int(entry["line_count"]):
            errors.append(f"LINE_COUNT_MISMATCH:{path}")
        git_sha = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()
        if git_sha != entry["git_blob_sha1"]:
            errors.append(f"GIT_BLOB_MISMATCH:{path}")
        by_path[path] = text.split("\n")
    for call in calls:
        path = call["module"]
        line = int(call["line"])
        lines = by_path.get(path)
        if not lines or line > len(lines):
            errors.append(f"CALLSITE_FILE_OR_LINE_MISSING:{call['row_id']}")
            continue
        source = lines[line - 1].strip()
        expected = call["code_expression"]
        if not source.startswith(expected):
            errors.append(f"CALLSITE_TEXT_MISMATCH:{call['row_id']}")
        if not CALL_RX.search(source):
            errors.append(f"CALLSITE_REGEX_MISSING:{call['row_id']}")
    print(json.dumps({
        "ref": BASE,
        "scanned_files": len(scanned),
        "callsite_candidates": len(calls),
        "errors": errors,
        "status": "S0_S1_STATIC_RECEIPT_ONLY" if not errors else "STATIC_RECEIPT_MISMATCH",
        "warning": "This does not prove callsite exhaustiveness, original accepted authority, S2/native execution, or PRE553 J first-consumer parity.",
    }, sort_keys=True, indent=2))
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
