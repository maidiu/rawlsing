#!/usr/bin/env python3
"""Fail closed unless the destination is the exact 459-file R2 base."""
from __future__ import annotations
import argparse, hashlib, json, os, stat, subprocess, sys
from pathlib import Path

R2_COMMIT="598d9e9eaba5143950c63317705fd09104fbf463"
R2_PATH="SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2"
MANIFEST_SHA="7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126"
VENDOR_ROWS=444
FILE_MODES={"100644", "100755"}

def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def decode_path(raw: bytes) -> str:
    return raw.decode("utf-8", "surrogateescape")

def expected_tree(repo: Path) -> tuple[dict[str, str], dict[str, str]]:
    raw=subprocess.check_output(["git","-C",str(repo),"ls-tree","-r","-z",R2_COMMIT,"--",R2_PATH])
    prefix=(R2_PATH+"/").encode()
    expected={}
    modes={}
    for record in raw.split(b"\0"):
        if not record: continue
        meta, full=record.split(b"\t",1)
        mode, kind, obj=meta.split(b" ",2)
        if not full.startswith(prefix):
            raise ValueError("R2_PATH_ESCAPE:"+decode_path(full))
        rel=decode_path(full[len(prefix):])
        if not rel or rel.startswith("/") or ".." in rel.split("/"):
            raise ValueError("R2_UNSAFE_PATH:"+rel)
        if kind!=b"blob":
            raise ValueError("R2_NON_BLOB:"+rel)
        mode_s=mode.decode("ascii")
        if mode_s not in FILE_MODES:
            raise ValueError("R2_NONREGULAR_MODE:"+rel)
        if rel in expected:
            raise ValueError("R2_DUPLICATE:"+rel)
        expected[rel]=obj.decode("ascii")
        modes[rel]=mode_s
    return expected, modes

def scan_actual(dest: Path) -> tuple[dict[str, Path], list[str]]:
    actual={}
    errors=[]
    if dest.is_symlink():
        errors.append("R2_SYMLINK:.")
        return actual, errors
    if not dest.is_dir():
        errors.append("R2_DEST_MISSING")
        return actual, errors
    def walk(directory: Path, prefix: str) -> None:
        try:
            entries=list(os.scandir(directory))
        except OSError as e:
            errors.append("R2_SCAN_ERROR:"+prefix+":"+str(e))
            return
        for entry in entries:
            rel=prefix+entry.name
            try:
                st=entry.stat(follow_symlinks=False)
            except OSError as e:
                errors.append("R2_STAT_ERROR:"+rel+":"+str(e))
                continue
            if stat.S_ISLNK(st.st_mode):
                errors.append("R2_SYMLINK:"+rel)
            elif stat.S_ISDIR(st.st_mode):
                walk(Path(entry.path), rel+"/")
            elif stat.S_ISREG(st.st_mode):
                actual[rel]=Path(entry.path)
            else:
                errors.append("R2_NONREGULAR:"+rel)
    walk(dest, "")
    return actual, errors

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--dest",type=Path,required=True); ap.add_argument("--repo",type=Path,required=True); a=ap.parse_args()
    dest=a.dest.absolute()
    errors=[]
    try:
        expected, modes=expected_tree(a.repo)
    except subprocess.CalledProcessError as e:
        expected={}; modes={}
        errors.append("R2_COMMIT_UNAVAILABLE:"+str(e))
    except ValueError as e:
        expected={}; modes={}
        errors.append(str(e))
    actual, scan_errors=scan_actual(dest)
    errors.extend(scan_errors)
    if len(expected)!=459: errors.append(f"R2_TREE_FILES:{len(expected)}")
    missing=set(expected)-set(actual)
    extra=set(actual)-set(expected)
    if missing: errors.append("R2_MISSING:"+",".join(sorted(missing)[:10]))
    if extra: errors.append("R2_EXTRA:"+",".join(sorted(extra)[:10]))
    for rel, git_blob in expected.items():
        path=actual.get(rel)
        if path is None: continue
        try:
            st=os.lstat(path)
        except OSError as e:
            errors.append("R2_STAT_ERROR:"+rel+":"+str(e)); continue
        if not stat.S_ISREG(st.st_mode):
            errors.append("R2_NONREGULAR:"+rel); continue
        if bool(st.st_mode & 0o111)!=(modes[rel]=="100755"):
            errors.append("R2_MODE_MISMATCH:"+rel)
        try: data=path.read_bytes()
        except OSError as e:
            errors.append("R2_READ_ERROR:"+rel+":"+str(e)); continue
        if blob_sha(data)!=git_blob: errors.append("R2_BLOB_MISMATCH:"+rel)
    manifest=dest/"SOURCE_MANIFEST.json"
    rows=[]
    if not manifest.is_file(): errors.append("SOURCE_MANIFEST_MISSING")
    else:
        if hashlib.sha256(manifest.read_bytes()).hexdigest()!=MANIFEST_SHA: errors.append("SOURCE_MANIFEST_SHA256_MISMATCH")
        try: rows=json.loads(manifest.read_text(encoding="utf8")).get("files",[])
        except Exception: rows=[]
        if len(rows)!=VENDOR_ROWS: errors.append(f"VENDOR_ROWS:{len(rows)}")
        for row in rows:
            rel=row.get("path","")
            if rel not in expected: errors.append("VENDOR_UNEXPECTED:"+rel); continue
            if expected[rel]!=row.get("git_blob"): errors.append("VENDOR_BLOB_MISMATCH:"+rel)
    result={"schema":"RRIF_E_R2_BASE_VALIDATION@1","ok":not errors,"errors":errors,"expected_files":len(expected),"actual_files":len(actual),"vars":len(rows)}
    print(json.dumps(result,indent=2)); return 0 if result["ok"] else 1
if __name__=="__main__": sys.exit(main())
