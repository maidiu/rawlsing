#!/usr/bin/env python3
"""Canonicalize L02 CSV output to LF and shard the full response-pattern census.

This is serialization-only. It does not alter any empirical row, statistic, branch,
weight, filter, or interpretation produced by analyze_lebanon_fracture_map.py.
"""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path

CSV_NAMES = [
    "LEBANON_BRANCH_ORACLE.csv",
    "RESPONSE_PATTERN_ORACLE.csv",
    "BRANCH_DETERMINICITY_ORACLE.csv",
    "SUPPORT_WEIGHT_MISSINGNESS_LEDGER.csv",
    "ORIGINARY_CLAIM_REPLICATION_MATRIX.csv",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_lf(src: Path, dst: Path) -> None:
    text = src.read_bytes().decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    dst.write_bytes(text.encode("utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    for name in CSV_NAMES:
        normalize_lf(args.input / name, args.out / name)

    monolith = args.out / "RESPONSE_PATTERN_ORACLE.csv"
    monolith_sha = sha256(monolith)
    lines = monolith.read_text(encoding="utf-8").splitlines(keepends=True)
    header, rows = lines[0], lines[1:]
    if len(rows) != 370:
        raise RuntimeError(f"expected 370 response-pattern rows, got {len(rows)}")

    parts = []
    for i, start in enumerate(range(0, len(rows), 50), 1):
        block = rows[start : start + 50]
        filename = f"RESPONSE_PATTERN_ORACLE_PART_{i:02d}.csv"
        part = args.out / filename
        part.write_text(header + "".join(block), encoding="utf-8", newline="")
        parts.append((i, filename, start + 1, start + len(block), len(block), sha256(part)))

    manifest = args.out / "RESPONSE_PATTERN_ORACLE_MANIFEST.csv"
    with manifest.open("w", encoding="utf-8", newline="") as f:
        f.write("schema,monolithic_replay_sha256,part,filename,data_row_start,data_row_end,data_row_count,sha256\n")
        for i, filename, start, end, count, digest in parts:
            f.write(
                f"L02_RESPONSE_PATTERN_ORACLE_SHARDED_MANIFEST@1.0.0,{monolith_sha},"
                f"{i},{filename},{start},{end},{count},{digest}\n"
            )

    print(f"monolithic={monolith_sha}")
    print(f"manifest={sha256(manifest)}")


if __name__ == "__main__":
    main()
