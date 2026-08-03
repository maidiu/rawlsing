#!/usr/bin/env python3
"""Regenerate the source dataset manifest from the live file accounting manifest.

This keeps the source inventory aligned with the actual raw-file accounting rows
that are already used by the structural validator and downstream registers.
"""

from __future__ import annotations

import csv
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
DDM_ROOT = ROOT / "data" / "ddm_build_copy"
IN_PATH = DDM_ROOT / "manifests" / "file_accounting_manifest.csv"
OUT_CSV = DDM_ROOT / "manifests" / "source_dataset_manifest.csv"
OUT_YAML = DDM_ROOT / "manifests" / "source_dataset_manifest.yaml"


def load_raw_rows() -> list[dict[str, str]]:
    csv.field_size_limit(10_000_000)
    rows: list[dict[str, str]] = []
    with IN_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("artifact_kind") != "raw_data":
                continue
            rows.append(
                {
                    "dataset_id": row.get("dataset_id", ""),
                    "source_family": row.get("source_family", ""),
                    "wave": row.get("wave", ""),
                    "path": row.get("path", ""),
                    "relative_path": row.get("relative_path", ""),
                    "format": row.get("format", ""),
                    "size_bytes": row.get("size_bytes", ""),
                    "sha256": row.get("sha256", ""),
                    "classification_confidence": float(row.get("classification_confidence", "0") or 0),
                }
            )
    return rows


def write_outputs(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "dataset_id",
                "source_family",
                "wave",
                "path",
                "relative_path",
                "format",
                "size_bytes",
                "sha256",
                "classification_confidence",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    payload = {
        "source_roots": [
            str(ROOT / "data" / "Data"),
            str(ROOT / "data" / "GSS"),
            str(ROOT / "data" / "LiTS"),
        ],
        "count": len(rows),
        "datasets": rows,
    }
    OUT_YAML.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")


def main() -> int:
    rows = load_raw_rows()
    write_outputs(rows)
    print(f"Wrote {len(rows)} raw datasets to {OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
