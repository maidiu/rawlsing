"""Shared deterministic helpers for the R53 U53F read-only forensic index."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

SEALED = "f148f9ba34deb0ae2ad3983fe94bbcef8f004b03"
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "WORKER_RETURNS/PYAT-R53-U53F-UNIVERSAL-EXECUTION-CODEBASE-FORENSICS-R1"
EVID = OUT / "evidence"
TOOLS = OUT / "tools"


def run(args, *, cwd=ROOT, check=True, text=True):
    return subprocess.run(args, cwd=str(cwd), check=check, capture_output=True, text=text)


def git(*args, check=True):
    return run(["git", *args], check=check).stdout


def git_bytes(*args, check=True):
    return run(["git", *args], check=check, text=False).stdout


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def write_text(path: Path, text: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return sha256_text(text)


def write_json(path: Path, payload) -> str:
    return write_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def write_tsv(path: Path, header, rows) -> str:
    lines = ["\t".join(header)]
    for row in rows:
        lines.append("\t".join("" if v is None else str(v).replace("\t", " ").replace("\n", " ")
                               for v in row))
    return write_text(path, "\n".join(lines) + "\n")


def ls_tree(rev=SEALED):
    raw = git_bytes("ls-tree", "-r", "-z", rev)
    out = []
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        meta, path = entry.split(b"\t", 1)
        mode, kind, blob = meta.decode().split()
        out.append(dict(mode=mode, kind=kind, blob=blob,
                        path=path.decode("utf-8", "surrogateescape")))
    return out


def blob_sizes(blobs):
    """Map blob -> size using one cat-file --batch-check process."""
    unique = sorted(set(blobs))
    payload = "".join(blob + "\n" for blob in unique).encode()
    proc = subprocess.run(["git", "cat-file", "--batch-check"],
                          cwd=str(ROOT), input=payload, capture_output=True, check=True)
    sizes = {}
    for line in proc.stdout.decode().splitlines():
        fields = line.split()
        if len(fields) == 3:
            sizes[fields[0]] = int(fields[2])
        else:
            sizes[fields[0]] = -1
    return sizes


def read_blob(blob: str) -> bytes:
    return git_bytes("cat-file", "blob", blob)


def classify_path(path: str) -> str:
    p = path
    name = p.rsplit("/", 1)[-1]
    suffix = ("." + name.rsplit(".", 1)[-1].lower()) if "." in name else ""
    if p.startswith("rawlsing_next/"):
        if name.startswith("test_") or name.endswith("_test.py"):
            return "TEST_CODE"
        return "PRODUCTION_CODE"
    if p.startswith("data/"):
        if "/tests/" in p or name.startswith("test_") or name.endswith("_test.py"):
            return "TEST_CODE"
        if suffix in (".sav", ".dta", ".parquet", ".feather", ".sqlite", ".db",
                      ".tar", ".gz", ".zip", ".7z", ".pkl", ".h5", ".arrow"):
            return "LARGE_ARCHIVE_OR_SOURCE_BINARY"
        if suffix == ".py":
            return "LEGACY_BUILD_CODE"
        if "authority" in p.lower() or "registry" in p.lower() or "census" in p.lower():
            return "AUTHORITY_REGISTRY"
        if "fixture" in p.lower() or "/fixtures/" in p:
            return "FIXTURE_OR_TEST_DATA"
        if suffix in (".json", ".jsonl", ".tsv", ".csv", ".yaml", ".yml", ".toml"):
            return "DATA_OR_CONFIG"
        return "LEGACY_NONCODE"
    if p.startswith("PYAT_CONTROL_ROOM/") or p.startswith("CROSS_HQ_CONTROL_ROOM/"):
        return "CONTROL_OR_COMMISSION"
    if p.startswith("WORKER_COMMISSIONS/") or p.startswith("HQ_HANDOFF/"):
        return "CONTROL_OR_COMMISSION"
    if p.startswith("WORKER_RETURNS/"):
        if suffix == ".py":
            return "WORKER_BRANCH_CODE"
        return "WORKER_RETURN_ARTIFACT"
    if p.startswith("tests/") or "/tests/" in p:
        return "TEST_CODE"
    if p.startswith("section85/") or p.startswith("LOCAL_") or p.startswith("rawlsing_"):
        return "LEGACY_OR_LOCAL_EVIDENCE"
    if suffix in (".sav", ".dta", ".parquet", ".sqlite", ".db", ".tar", ".gz",
                  ".zip", ".7z", ".pkl", ".h5", ".arrow", ".pbf", ".npy", ".npz"):
        return "LARGE_ARCHIVE_OR_SOURCE_BINARY"
    if suffix in (".md", ".txt", ".rst"):
        return "DOCUMENTATION"
    if suffix in (".json", ".jsonl", ".tsv", ".csv", ".yaml", ".yml", ".toml", ".ini", ".cfg"):
        return "DATA_OR_CONFIG"
    if suffix in (".py", ".sh", ".sql", ".js", ".ts", ".html", ".css"):
        return "OTHER_CODE"
    if suffix in ("", ".gitignore", ".gitattributes", ".gitmodules"):
        return "NONCODE_OR_UNKNOWN"
    return "NONCODE_OR_UNKNOWN"


def parent_top(path: str) -> str:
    return path.split("/", 1)[0] if "/" in path else "."
