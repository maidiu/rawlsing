#!/usr/bin/env python3
"""
Build a demographic/support-field register from the question structure register.

This does not replace the microdata cache. It makes the demographic surface area
explicit across families and waves so we can audit and use it consistently in DDM.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN_PATH = ROOT / "ddm_build_copy" / "manifests" / "question_structure_register.csv"
OUT_PATH = ROOT / "ddm_build_copy" / "manifests" / "demographic_field_register.csv"
OUT_YAML = ROOT / "ddm_build_copy" / "manifests" / "demographic_field_register.yaml"

csv.field_size_limit(10_000_000)

DEMOGRAPHIC_PATTERNS = [
    (re.compile(r"\b(sex|gender|male|female)\b", re.I), "sex_gender"),
    (re.compile(r"\b(age|birth year|date of birth|born)\b", re.I), "age"),
    (re.compile(r"\b(education|school|literacy|qualification|degree|years of schooling)\b", re.I), "education"),
    (re.compile(r"\b(income|earnings|wage|financial|poverty|wealth|decile)\b", re.I), "income"),
    (re.compile(r"\b(urban|rural|village|town|city|settlement|locality|residence)\b", re.I), "urban_rural"),
    (re.compile(r"\b(religion|religious|church|mosque|temple|faith|denomination|denominational)\b", re.I), "religion"),
    (re.compile(r"\b(marital|spouse|husband|wife|partner|single|married|divorced|widowed)\b", re.I), "marital"),
    (re.compile(r"\b(employment|employed|job|occupation|work|labor force|unemployment|unemployed)\b", re.I), "employment"),
    (re.compile(r"\b(household|family size|children|child|dependen|respondent's mother|respondent's father)\b", re.I), "household"),
    (re.compile(r"\b(language|mother tongue|home language|speak at home|linguistic)\b", re.I), "language"),
    (re.compile(r"\b(ethnic|ethnicity|race|racial|tribe|indigenous|nationality|origin)\b", re.I), "identity"),
    (re.compile(r"\b(region|province|district|county|state|admin1|geography)\b", re.I), "region"),
    (re.compile(r"\b(class|strata|socioeconomic|socio-economic|social class)\b", re.I), "class"),
    (re.compile(r"\b(migration|migrant|immigrant|foreign born|citizenship|national)\b", re.I), "mobility_identity"),
]


def looks_demographic(row: dict[str, str]) -> tuple[bool, str, float]:
    text_bits = " ".join(
        str(row.get(k, "") or "")
        for k in (
            "question_text",
            "question_name",
            "question_id",
            "final_driver_label",
            "semantic_notes",
            "evidence",
            "notes",
            "var_name",
            "matched_source_column",
        )
    ).strip()
    low = text_bits.lower()

    if row.get("final_driver_scope") in {"metadata", "shared", "regional"} and row.get("question_type") in {
        "single_choice",
        "derived_or_reference",
        "open_text",
        "matrix",
        "split_block",
    }:
        for rx, kind in DEMOGRAPHIC_PATTERNS:
            if rx.search(low):
                return True, kind, 0.96
        if row.get("final_driver_scope") == "metadata":
            return True, "metadata_support", 0.80

    for rx, kind in DEMOGRAPHIC_PATTERNS:
        if rx.search(low):
            return True, kind, 0.88

    return False, "", 0.0


def main() -> None:
    rows: list[dict[str, str]] = []
    by_kind = Counter()
    by_family = Counter()

    with IN_PATH.open(newline="", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            is_demo, kind, confidence = looks_demographic(row)
            if not is_demo:
                continue
            out = {
                "source_family": row.get("source_family") or row.get("source") or "",
                "wave": row.get("wave") or row.get("canonical_wave") or "",
                "question_id": row.get("question_id") or "",
                "var_name": row.get("question_name") or row.get("var_name") or "",
                "question_text": row.get("question_text") or "",
                "final_driver_id": row.get("final_driver_id") or "",
                "final_driver_label": row.get("final_driver_label") or "",
                "final_driver_scope": row.get("final_driver_scope") or "",
                "question_type": row.get("question_type") or "",
                "structural_role": row.get("structural_role") or "",
                "source_match_type": row.get("source_match_type") or "",
                "access_pattern": row.get("access_pattern") or "",
                "access_expression": row.get("access_expression") or "",
                "demographic_kind": kind,
                "demographic_confidence": f"{confidence:.2f}",
                "evidence": row.get("evidence") or "",
            }
            rows.append(out)
            by_kind[kind] += 1
            by_family[out["source_family"]] += 1

    rows.sort(key=lambda r: (r["source_family"], r["wave"], r["demographic_kind"], r["var_name"]))

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "source_family",
                "wave",
                "question_id",
                "var_name",
                "question_text",
                "final_driver_id",
                "final_driver_label",
                "final_driver_scope",
                "question_type",
                "structural_role",
                "source_match_type",
                "access_pattern",
                "access_expression",
                "demographic_kind",
                "demographic_confidence",
                "evidence",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    payload = {
        "status": "ok",
        "register_path": str(OUT_PATH),
        "row_count": len(rows),
        "kind_counts": dict(by_kind),
        "family_counts": dict(by_family),
        "note": "This is a demographic/support-field register derived from the question structure register; it complements the microdata cache and does not replace the raw survey loaders.",
    }
    OUT_YAML.write_text(
        "\n".join(
            [
                f"status: {payload['status']}",
                f"register_path: {payload['register_path']}",
                f"row_count: {payload['row_count']}",
                "kind_counts:",
                *[f"  {k}: {v}" for k, v in sorted(by_kind.items())],
                "family_counts:",
                *[f"  {k}: {v}" for k, v in sorted(by_family.items())],
                f"note: {payload['note']}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
