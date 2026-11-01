#!/usr/bin/env python3
"""Fail closed unless the destination is the exact 459-file R2 base."""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

R2_COMMIT="598d9e9eaba5143950c63317705fd09104fbf463"
R2_PATH="SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2"
MANIFEST_SHA="7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126"
VENDOR_ROWS=444

def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--dest",type=Path,required=True); ap.add_argument("--repo",type=Path,required=True); a=ap.parse_args()
    errors=[]
    manifest=a.dest/"SOURCE_MANIFEST.json"
    if not manifest.is_file(): errors.append("SOURCE_MANIFEST_MISSING")
    else:
        if hashlib.sha256(manifest.read_bytes()).hexdigest()!=MANIFEST_SHA: errors.append("SOURCE_MANIFEST_SHA256_MISMATCH")
        try: rows=json.loads(manifest.read_text(encoding="utf8")).get("files",[])
        except Exception: rows=[]
        if len(rows)!=VENDOR_ROWS: errors.append(f"VENDOR_ROWS:{len(rows)}")
        for row in rows:
            p=a.dest/row["path"]
            if not p.is_file(): errors.append("VENDOR_MISSING:"+row["path"]); continue
            if blob_sha(p.read_bytes())!=row.get("git_blob"): errors.append("VENDOR_BLOB_MISMATCH:"+row["path"])
    try:
        tree=subprocess.check_output(["git","-C",str(a.repo),"ls-tree","-r","--name-only",R2_COMMIT,"--",R2_PATH],text=True).splitlines()
    except subprocess.CalledProcessError as e:
        tree=[]
        errors.append("R2_COMMIT_UNAVAILABLE:"+str(e))
    expected={p.removeprefix(R2_PATH+"/") for p in tree}
    actual={p.relative_to(a.dest).as_posix() for p in a.dest.rglob("*") if p.is_file()} if a.dest.is_dir() else set()
    if len(expected)!=459: errors.append(f"R2_TREE_FILES:{len(expected)}")
    if expected-actual: errors.append("R2_MISSING:"+",".join(sorted(expected-actual)[:10]))
    if actual-expected: errors.append("R2_EXTRA:"+",".join(sorted(actual-expected)[:10]))
    result={"schema":"RRIF_E_R2_BASE_VALIDATION@1","ok":not errors,"errors":errors,"expected_files":len(expected),"actual_files":len(actual),"vars":len(rows) if 'rows' in locals() else 0}
    print(json.dumps(result,indent=2)); return 0 if result["ok"] else 1
if __name__=="__main__": sys.exit(main())
