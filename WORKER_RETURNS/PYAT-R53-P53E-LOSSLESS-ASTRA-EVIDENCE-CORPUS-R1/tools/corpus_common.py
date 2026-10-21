"""Shared deterministic helpers for the P53E lossless corpus.

Read-only against Git objects; writes only under the P53E return subtree unless
an explicit temporary output path is supplied by a test.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

SOURCE_REF = "fdc4d03537e649cd56c19a458ebeb3292298ff3f"
FALLBACK_SEALED_REF = "f148f9ba34deb0ae2ad3983fe94bbcef8f004b03"
U53F_RETURN = "WORKER_RETURNS/PYAT-R53-U53F-UNIVERSAL-EXECUTION-CODEBASE-FORENSICS-R1"
P53E_RETURN = "WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1"
CHUNK_BOUND = 196608  # 192 KiB, stricter than the <=200 KiB commission bound.
CHUNK_PREFIX = "part-"

# Stable human-readable shard ids for the eight originals above the chunk bound.
LARGE_SHARDS = {
    "01_REPOSITORY_SCOPE_AND_COMPLETENESS.json": "S01_01_REPOSITORY_SCOPE",
    "02_ALL_PINNED_TREE_FILES.tsv": "S02_02_ALL_PINNED_TREE_FILES",
    "03_MATERIAL_BRANCH_DIFF_FILE_BLOBS.part00.tsv": "S03_03_MATERIAL_DIFF_PART00",
    "03_MATERIAL_BRANCH_DIFF_FILE_BLOBS.part01.tsv": "S04_03_MATERIAL_DIFF_PART01",
    "06_SOURCE_SPECIFICITY_AND_FIXTURE_LEAKAGE.tsv": "S05_06_SOURCE_SPECIFICITY",
    "06B_DOCUMENT_REFERENCE_COUNTS.tsv": "S06_06B_DOCUMENT_REFERENCE_COUNTS",
    "evidence/ref_inventory.json": "S07_EVIDENCE_REF_INVENTORY",
    U53F_RETURN + "/01_REPOSITORY_SCOPE_AND_COMPLETENESS.json": "S08_NESTED_01_REPOSITORY_SCOPE",
}


def root() -> Path:
    try:
        out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
        return Path(out)
    except Exception:
        return Path.cwd()


ROOT = root()
P53E_ROOT = ROOT / P53E_RETURN
SHARDS_ROOT = P53E_ROOT / "shards"
RECEIPTS = P53E_ROOT / "receipts"


def run(args, *, cwd=None, check=True, text=True):
    return subprocess.run(
        args, cwd=str(cwd or ROOT), check=check, capture_output=True, text=text
    )


def git(*args, check=True):
    return run(["git", *args], check=check).stdout


def git_bytes(*args, check=True):
    return run(["git", *args], check=check, text=False).stdout


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_blob(blob: str) -> bytes:
    return git_bytes("cat-file", "blob", blob)


def blob_sizes(blobs):
    """Map blob id -> size or -1 for missing, without fetching promisor blobs."""
    unique = sorted(set(blobs))
    payload = "".join(blob + "\n" for blob in unique).encode()
    proc = subprocess.run(
        ["git", "cat-file", "--batch-check"],
        cwd=str(ROOT),
        input=payload,
        capture_output=True,
        check=True,
    )
    sizes = {}
    for line in proc.stdout.decode().splitlines():
        fields = line.split()
        if len(fields) == 3:
            sizes[fields[0]] = int(fields[2])
        elif fields:
            sizes[fields[0]] = -1
    return sizes


def tree_map(rev: str = SOURCE_REF):
    raw = git_bytes("ls-tree", "-r", "-z", rev)
    out = {}
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        meta, path = entry.split(b"\t", 1)
        mode, kind, blob = meta.decode().split()
        out[path.decode("utf-8", "surrogateescape")] = {
            "mode": mode,
            "kind": kind,
            "blob": blob,
        }
    return out


def commit_date(rev: str = SOURCE_REF) -> str:
    return git("show", "-s", "--format=%cI", rev).strip()


def source_return_prefix() -> str:
    return U53F_RETURN


def u53f_manifest():
    path = U53F_RETURN + "/EVIDENCE_MANIFEST.json"
    blob = tree_map()[path]["blob"]
    return json.loads(read_blob(blob).decode("utf-8")), blob


def line_metrics(data: bytes):
    lines = data.split(b"\n")
    if lines and lines[-1] == b"":
        lines = lines[:-1]
    return {
        "bytes": len(data),
        "line_count": len(lines),
        "newline_count": data.count(b"\n"),
        "ends_with_newline": data.endswith(b"\n") if data else True,
        "max_line_bytes": max((len(x) for x in lines), default=0),
    }


def row_at_offset(data: bytes, offset: int) -> int:
    """1-based physical line number containing byte offset (0-based)."""
    if offset < 0:
        raise ValueError("negative offset")
    if offset >= len(data):
        return data.count(b"\n") + (0 if data.endswith(b"\n") or not data else 1)
    return data.count(b"\n", 0, offset) + 1


def split_bytes(data: bytes, bound: int = CHUNK_BOUND):
    """Yield (start, end) byte ranges, newline-aligned when a line fits."""
    if not data:
        yield (0, 0)
        return
    start = 0
    total = len(data)
    while start < total:
        limit = min(start + bound, total)
        end = limit
        if limit < total:
            newline = data.rfind(b"\n", start, limit)
            if newline >= start:
                end = newline + 1
            # else: a single physical line exceeds the bound; split mid-row.
        yield (start, end)
        start = end


def chunk_metrics(data: bytes, start: int, end: int):
    starts_mid = start > 0 and data[start - 1 : start] != b"\n"
    ends_mid = end < len(data) and data[end - 1 : end] != b"\n"
    return {
        "byte_start": start,
        "byte_end": end,
        "bytes": end - start,
        "row_start": row_at_offset(data, start),
        "row_end": row_at_offset(data, end - 1) if end > start else row_at_offset(data, start),
        "starts_mid_row": starts_mid,
        "ends_mid_row": ends_mid,
        "newline_count": data.count(b"\n", start, end),
    }


def shard_id_for_path(path: str, index: int) -> str:
    if path in LARGE_SHARDS:
        return LARGE_SHARDS[path]
    safe = "".join(c if c.isalnum() else "_" for c in path).strip("_")[-48:]
    return f"S{index:02d}_{safe}"


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8")
    return sha256(text.encode("utf-8"))


def write_tsv(path: Path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["\t".join(header)]
    for row in rows:
        lines.append(
            "\t".join(
                "" if v is None else str(v).replace("\t", " ").replace("\r", " ").replace("\n", " ")
                for v in row
            )
        )
    text = "\n".join(lines) + "\n"
    path.write_text(text, encoding="utf-8")
    return sha256(text.encode("utf-8"))


def hash_object(path: Path) -> str:
    return git("hash-object", "--no-filters", str(path)).strip()


def progress(message: str):
    print(message, file=sys.stderr, flush=True)
