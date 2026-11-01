#!/usr/bin/env python3
"""Validate a complete staged RRIF-E candidate against its source preimage."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

PREIMAGE = "RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json"

def validate(root: Path) -> dict:
    path = root / PREIMAGE
    if not path.is_file():
        raise SystemExit("PREIMAGE_MISSING")
    doc = json.loads(path.read_text(encoding="utf8"))
    actual = {p.relative_to(root).as_posix(): p for p in root.rglob("*") if p.is_file()}
    listed = {row["path"]: row for row in doc.get("files", [])}
    errors = []
    if PREIMAGE in listed:
        errors.append("SELF_ENTRY_FORBIDDEN")
    unlisted = sorted(set(actual) - set(listed) - {PREIMAGE})
    missing = sorted(set(listed) - set(actual))
    if unlisted:
        errors.append("UNLISTED_FILES:" + ",".join(unlisted))
    if missing:
        errors.append("MISSING_FILES:" + ",".join(missing))
    for rel, row in listed.items():
        p = root / rel
        if not p.is_file():
            continue
        data = p.read_bytes()
        if hashlib.sha256(data).hexdigest() != row.get("sha256"):
            errors.append("SHA256_MISMATCH:" + rel)
        if len(data) != row.get("size"):
            errors.append("SIZE_MISMATCH:" + rel)
    manifest = root / "SOURCE_MANIFEST.json"
    if not manifest.is_file():
        errors.append("SOURCE_MANIFEST_MISSING")
        manifest_sha = ""
    else:
        manifest_sha = hashlib.sha256(manifest.read_bytes()).hexdigest()
        if manifest_sha != doc.get("source_manifest_sha256"):
            errors.append("SOURCE_MANIFEST_SHA256_MISMATCH")
        try:
            rows = len(json.loads(manifest.read_text(encoding="utf8")).get("files", []))
        except Exception:
            rows = -1
        if rows != 444:
            errors.append(f"SOURCE_MANIFEST_ROWS:{rows}")
    counts = doc.get("counts", {})
    if counts.get("files") != len(listed):
        errors.append("PREIMAGE_COUNT_MISMATCH")
    if counts.get("actual_regular_files") != len(actual):
        errors.append("ACTUAL_FILE_COUNT_MISMATCH")
    if counts.get("r3_extension_files") != 174:
        errors.append("R3_EXTENSION_COUNT_MISMATCH")
    if not counts.get("first_consumer_cli_included"):
        errors.append("FIRST_CONSUMER_CLI_NOT_LISTED")
    if not any(path.startswith("rrif_r3_extension/") for path in actual):
        errors.append("R3_EXTENSION_ABSENT")
    if doc.get("source_candidate_commit") != "8d9585296ff264b947559f4a78f49f73ca45e53a":
        errors.append("SOURCE_CANDIDATE_COMMIT_MISMATCH")
    if doc.get("self_exclusion", {}).get("path") != PREIMAGE or doc.get("self_exclusion", {}).get("content_addressed") is not False:
        errors.append("SELF_EXCLUSION_INVALID")
    return {"schema":"RRIF_E_PACKET_VALIDATION@1","ok":not errors,"errors":errors,"listed":len(listed),"actual":len(actual),"unlisted":unlisted,"source_manifest_sha256":manifest_sha,"r3_extension_files":sum(1 for p in actual if p.startswith("rrif_r3_extension/"))}

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--root",type=Path,required=True); a=ap.parse_args()
    try: result=validate(a.root)
    except SystemExit as e:
        print(json.dumps({"ok":False,"errors":[str(e)]},indent=2)); return 1
    print(json.dumps(result,indent=2)); return 0 if result["ok"] else 1
if __name__=="__main__": sys.exit(main())
