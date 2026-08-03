#!/usr/bin/env python3
"""Run a file-by-file structural audit of raw survey sources against codebooks.

This wrapper uses the existing survey_structure_audit module so the repo has a
single structural-audit rule set for:
- raw header / column shape
- codebook var_name alignment
- child-column / split-block detection
- matrix / multi-select detection
- open-text and metadata detection

It writes per-file audit outputs plus a repo-wide manifest that can be used as
the preflight gate before any long overnight compute loop.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


DDM_ROOT = ROOT / "data" / "ddm_build_copy"
MANIFEST_IN = DDM_ROOT / "manifests" / "file_accounting_manifest.csv"
VALIDATION_MANIFEST_OUT = DDM_ROOT / "manifests" / "source_structure_validation_manifest.csv"
VALIDATION_REPORT_OUT = DDM_ROOT / "manifests" / "source_structure_validation_report.yaml"
PROBLEM_FILES_OUT = DDM_ROOT / "manifests" / "source_structure_problem_files.csv"
TAXONOMY_OUT = DDM_ROOT / "manifests" / "question_type_taxonomy.yaml"
AUDIT_DIR = DDM_ROOT / "reports" / "source_structure_audits"
CODEBOOK_DIR = ROOT / "data" / "FINAL CODEBOOKS" / "FINAL FINAL CODEBOOKS"

INTENDED_CANONICAL_PAIRS = {
    ("Arab Barometer", "W1"),
    ("Arab Barometer", "W2"),
    ("Arab Barometer", "W5"),
    ("Arab Barometer", "W8"),
    ("Afrobarometer", "R1"),
    ("Afrobarometer", "R5"),
    ("Afrobarometer", "R9"),
    ("Asian Barometer", "W1"),
    ("Asian Barometer", "W4"),
    ("Asian Barometer", "W5"),
    ("Asian Barometer", "W6"),
    ("South Asia", "W1"),
    ("South Asia", "W2"),
    ("Latinobarómetro", "1995"),
    ("Latinobarómetro", "2011"),
    ("Latinobarómetro", "2024"),
    ("EVS", "W1"),
    ("EVS", "1990"),
    ("EVS", "W3"),
    ("EVS", "2008"),
    ("EVS", "2017"),
    ("WVS", "W1"),
    ("WVS", "W4"),
    ("WVS", "W7"),
    ("GSS", "1972"),
    ("GSS", "1973"),
    ("GSS", "1982"),
    ("GSS", "1984"),
    ("GSS", "1993"),
    ("GSS", "2002"),
    ("GSS", "2010"),
    ("GSS", "2016"),
    ("GSS", "2024"),
    ("LiTS", "2006"),
    ("LiTS", "II"),
    ("LiTS", "III"),
    ("LiTS", "IV"),
}

CODEBOOK_FILENAME_BY_PAIR = {
    ("Arab Barometer", "W1"): "Arab Barometer Wave 1 codebook.csv",
    ("Arab Barometer", "W2"): "Arab Barometer Wave 2 codebook.csv",
    ("Arab Barometer", "W5"): "Arab Barometer Wave 5 codebook.csv",
    ("Arab Barometer", "W8"): "Arab Barometer Wave 8 codebook.csv",
    ("Afrobarometer", "R1"): "Afrobarometer Round 1 codebook.csv",
    ("Afrobarometer", "R5"): "Afrobarometer Round 5 codebook.csv",
    ("Afrobarometer", "R9"): "Afrobarometer Round 9 codebook.csv",
    ("Asian Barometer", "W1"): "Asian Barometer Wave 1 codebook.csv",
    ("Asian Barometer", "W4"): "Asian Barometer Wave 4 codebook.csv",
    ("Asian Barometer", "W5"): "Asian Barometer Wave 5 codebook.csv",
    ("Asian Barometer", "W6"): "Asian Barometer Wave 6 codebook.csv",
    ("South Asia", "W1"): "South Asia Wave 1 codebook.csv",
    ("South Asia", "W2"): "South Asia Wave 2 codebook.csv",
    ("Latinobarómetro", "1995"): "Latinobarometro 1995 codebook.csv",
    ("Latinobarómetro", "2011"): "Latinobarometro 2011 codebook.csv",
    ("Latinobarómetro", "2024"): "Latinobarometro 2024 codebook.csv",
    ("EVS", "W1"): "EVS Wave 1 codebook 1981.csv",
    ("EVS", "1990"): "EVS Wave 2 codebook 1990.csv",
    ("EVS", "2008"): "EVS Wave 4 codebook 2008.csv",
    ("EVS", "2017"): "EVS Wave 5 codebook 2017.csv",
    ("EVS", "W3"): "EVS Wave 3 codebook 1999.csv",
    ("EVS", "TREND"): "EVS 1981-2017 Trend codebook.csv",
    ("WVS", "W1"): "World Values Survey Wave 1 codebook.csv",
    ("WVS", "W4"): "World Values Survey Wave 4 codebook.csv",
    ("WVS", "W7"): "World Values Survey Wave 7 codebook.csv",
    ("GSS", "1972"): "GSS1972-codebook.csv",
    ("GSS", "1973"): "GSS1973-codebook.csv",
    ("GSS", "1982"): "GSS1982-codebook.csv",
    ("GSS", "1984"): "GSS1984-codebook.csv",
    ("GSS", "1993"): "GSS1993-codebook.csv",
    ("GSS", "2002"): "GSS2002-codebook.csv",
    ("GSS", "2010"): "GSS2010-codebook.csv",
    ("GSS", "2016"): "GSS2016-codebook.csv",
    ("GSS", "2024"): "GSS2024-codebook.csv",
    ("LiTS", "2006"): "LiTS-I-codebook.csv",
    ("LiTS", "II"): "LiTS-II-codebook.csv",
    ("LiTS", "III"): "LiTS-III-codebook.csv",
    ("LiTS", "IV"): "LiTS-IV-codebook.csv",
}



def _load_audit_backend():
    try:
        from data.final_codebooks.survey_structure_audit import build_wave_audit, write_audit_outputs
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "SOURCE_STRUCTURE_AUDIT_BACKEND_MISSING: restore data/final_codebooks/survey_structure_audit.py "
            "before running the repository-wide source-structure audit"
        ) from exc
    return build_wave_audit, write_audit_outputs

def _clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_family(value: Any) -> str:
    cleaned = _clean(value)
    return {
        "Latinobarometro": "Latinobarómetro",
        "Asian Barometer Wave 5": "Asian Barometer",
        "South Asia Wave 1": "South Asia",
        "South Asia Wave 2": "South Asia",
    }.get(cleaned, cleaned)


def _truthy(value: Any) -> bool:
    return _clean(value).lower() in {"1", "true", "yes", "y"}


def _slugify(value: str) -> str:
    out = []
    for ch in value:
        if ch.isalnum():
            out.append(ch)
        else:
            out.append("_")
    slug = "".join(out).strip("_")
    while "__" in slug:
        slug = slug.replace("__", "_")
    return slug or "unnamed"


def canonical_wave_label(source_family: str, raw_wave: str) -> str:
    source_family = _normalize_family(source_family)
    raw_wave = _clean(raw_wave)
    if source_family == "Arab Barometer":
        mapping = {
            "Wave 1": "W1",
            "Wave 2": "W2",
            "Wave 5": "W5",
            "Wave 8": "W8",
            "I": "W1",
            "II": "W2",
            "III": "W3",
            "IV": "W4",
            "V": "W5",
            "VI_pt_i": "W6a",
            "VI_pt_ii": "W6b",
            "VI_pt_iii": "W6c",
            "VII": "W7",
            "VIII": "W8",
        }
        return mapping.get(raw_wave, raw_wave)
    if source_family == "Afrobarometer":
        mapping = {"Round 1": "R1", "Round 5": "R5", "Round 9": "R9"}
        return mapping.get(raw_wave, raw_wave)
    if source_family == "Asian Barometer":
        mapping = {"Wave 1": "W1", "Wave 4": "W4", "Wave 5": "W5", "Wave 6": "W6"}
        return mapping.get(raw_wave, raw_wave)
    if source_family == "South Asia":
        mapping = {"Wave 1": "W1", "Wave 2": "W2"}
        return mapping.get(raw_wave, raw_wave)
    if source_family == "Latinobarómetro":
        mapping = {"1995": "1995", "2011": "2011", "2024": "2024"}
        return mapping.get(raw_wave, raw_wave)
    if source_family == "EVS":
        if "TREND" in raw_wave.upper():
            return "TREND"
        if "1981" in raw_wave:
            return "W1"
        if "1990" in raw_wave:
            return "1990"
        if "2008" in raw_wave:
            return "2008"
        if "2017" in raw_wave:
            return "2017"
        if "1999" in raw_wave:
            return "W3"
        if raw_wave.upper() in {"W2", "W4", "W5"}:
            return {"W2": "1990", "W4": "2008", "W5": "2017"}[raw_wave.upper()]
    if source_family == "WVS":
        mapping = {"Wave 1": "W1", "Wave 4": "W4", "Wave 7": "W7"}
        return mapping.get(raw_wave, raw_wave)
    if source_family == "GSS":
        mapping = {"1972": "1972", "1973": "1973", "1982": "1982", "1984": "1984", "1993": "1993", "2002": "2002", "2010": "2010", "2016": "2016", "2024": "2024"}
        return mapping.get(raw_wave, raw_wave)
    if source_family == "LiTS":
        mapping = {"2006": "2006", "II": "II", "III": "III", "IV": "IV"}
        return mapping.get(raw_wave, raw_wave)
    return raw_wave


def codebook_path_for(source_family: str, canonical_wave: str) -> Path:
    family = _normalize_family(source_family)
    wave = _clean(canonical_wave)
    filename = CODEBOOK_FILENAME_BY_PAIR.get((family, wave), "")
    if not filename:
        return Path("")
    return CODEBOOK_DIR / filename


def load_manifest_rows() -> list[dict[str, Any]]:
    csv.field_size_limit(sys.maxsize)
    rows: list[dict[str, Any]] = []
    with MANIFEST_IN.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["source_family"] = _normalize_family(row.get("source_family"))
            rows.append(row)
    return rows


def build_taxonomy() -> list[dict[str, Any]]:
    return [
        {
            "question_kind": "single_choice",
            "structural_role": "answer",
            "default_handling": "Compute one distribution over labeled response options; keep don't know and refusal as meaningful categories when present.",
            "recommended_computation": "Distribution, conditional splits, branch comparisons, and driver-mapped cloud summaries.",
            "do_not_do": "Do not flatten into a binary unless the codebook and source structure are explicitly binary.",
        },
        {
            "question_kind": "multi_select",
            "structural_role": "stem",
            "default_handling": "Keep the child columns separate; compute option prevalence and co-occurrence instead of forcing one category.",
            "recommended_computation": "Per-option prevalence, option bundles, co-selection patterns, branch clouds.",
            "do_not_do": "Do not collapse to one nominal answer unless the source file itself is already one-hot encoded and the codebook says so.",
        },
        {
            "question_kind": "matrix",
            "structural_role": "stem",
            "default_handling": "Treat each child row as its own question and keep row-level distributions intact.",
            "recommended_computation": "Row-by-row distributions, within-matrix contrast, row clusters, row-level driver clouds.",
            "do_not_do": "Do not average rows together unless the survey design explicitly defines a scale index.",
        },
        {
            "question_kind": "split_block",
            "structural_role": "stem",
            "default_handling": "Treat each child block separately and preserve the split logic.",
            "recommended_computation": "Parallel branch summaries, split-block comparisons, and block-specific clouds.",
            "do_not_do": "Do not merge the children back into one pseudo-question unless the codebook and source match exactly.",
        },
        {
            "question_kind": "open_text",
            "structural_role": "answer",
            "default_handling": "Do not force numeric scoring; preserve text for later NLP or manual coding.",
            "recommended_computation": "Text extraction, topic coding, and curated qualitative review.",
            "do_not_do": "Do not invent numeric ordinals or scale scores.",
        },
        {
            "question_kind": "stem",
            "structural_role": "stem",
            "default_handling": "Treat as a parent item that organizes child columns but is not itself a scored answer.",
            "recommended_computation": "Structural grouping only.",
            "do_not_do": "Do not analyze as a substantive opinion response.",
        },
        {
            "question_kind": "derived_or_reference",
            "structural_role": "metadata",
            "default_handling": "Use as context, provenance, or conditioning only.",
            "recommended_computation": "Conditioning, joins, sample definition, or source metadata.",
            "do_not_do": "Do not count as a substantive attitude or opinion item.",
        },
        {
            "question_kind": "source_extra",
            "structural_role": "source_extra",
            "default_handling": "Flag as a source-side column that is not represented directly in the codebook row set.",
            "recommended_computation": "Manual review and source-to-codebook reconciliation.",
            "do_not_do": "Do not silently drop if the source file still meaningfully contributes to the structure.",
        },
    ]


def summarize_rows(rows: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    kind_counts = Counter()
    match_counts = Counter()
    flagged_names: list[str] = []
    for row in rows:
        kind_counts[_clean(row.get("classification_kind"))] += 1
        match_counts[_clean(row.get("source_match_type"))] += 1
        if _clean(row.get("needs_manual_review")) == "yes" or _clean(row.get("source_structure_disagrees_with_codebook")) == "yes":
            name = _clean(row.get("name"))
            if name:
                flagged_names.append(name)
    summary = {
        "kind_counts": dict(kind_counts),
        "source_match_counts": dict(match_counts),
        "record_count": len(rows),
        "manual_review_count": sum(1 for row in rows if _clean(row.get("needs_manual_review")) == "yes"),
        "source_structure_disagrees_count": sum(1 for row in rows if _clean(row.get("source_structure_disagrees_with_codebook")) == "yes"),
        "codebook_stale_count": sum(1 for row in rows if _clean(row.get("codebook_options_stale")) == "yes"),
        "codebook_trustworthy_count": sum(1 for row in rows if _clean(row.get("codebook_options_trustworthy")) == "yes"),
        "source_present_count": sum(1 for row in rows if _clean(row.get("source_present")) == "yes"),
        "high_level_conclusion": "",
    }
    conclusions = []
    if kind_counts.get("multi_select"):
        conclusions.append("multi-select families require child-column handling")
    if kind_counts.get("matrix"):
        conclusions.append("matrix families require row-level handling")
    if kind_counts.get("split_block"):
        conclusions.append("split blocks require child-block handling")
    if kind_counts.get("single_choice"):
        conclusions.append("single-choice answers can be scored directly")
    if kind_counts.get("open_text"):
        conclusions.append("open-text answers require text handling, not numeric scoring")
    summary["high_level_conclusion"] = "; ".join(conclusions)
    return summary, sorted(set(flagged_names))


def audit_one(row: dict[str, Any]) -> dict[str, Any]:
    dataset_id = _clean(row.get("dataset_id"))
    source_family = _clean(row.get("source_family"))
    wave = _clean(row.get("wave"))
    raw_path = Path(_clean(row.get("path")))
    canonical_wave = canonical_wave_label(source_family, wave)
    codebook_path = codebook_path_for(source_family, canonical_wave)
    read_status = _clean(row.get("read_status"))
    canonical_intended = (source_family, canonical_wave) in INTENDED_CANONICAL_PAIRS
    raw_exists = raw_path.exists()
    codebook_exists = bool(codebook_path and codebook_path.exists())

    base = {
        "dataset_id": dataset_id,
        "source_family": source_family,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "canonical_intended": canonical_intended,
        "raw_path": str(raw_path),
        "codebook_path": str(codebook_path) if codebook_path else "",
        "raw_read_status": read_status,
        "raw_exists": raw_exists,
        "codebook_exists": codebook_exists,
        "raw_row_count": _clean(row.get("row_count")),
        "raw_column_count": _clean(row.get("column_count")),
        "audit_status": "",
        "audit_csv": "",
        "audit_yaml": "",
        "audit_error": "",
        "kind_counts": "{}",
        "source_match_counts": "{}",
        "manual_review_count": 0,
        "source_structure_disagrees_count": 0,
        "codebook_stale_count": 0,
        "codebook_trustworthy_count": 0,
        "source_present_count": 0,
        "problem_fields": "",
        "high_level_conclusion": "",
    }

    out_prefix = AUDIT_DIR / _slugify(dataset_id)
    out_csv = out_prefix.with_suffix(".csv")
    out_yaml = out_prefix.with_suffix(".yaml")

    if not raw_exists:
        base["audit_status"] = "blocked_raw_missing"
        base["audit_error"] = "raw file not present on disk"
        out_yaml.parent.mkdir(parents=True, exist_ok=True)
        with out_yaml.open("w", encoding="utf-8") as f:
            yaml.safe_dump(
                {
                    "dataset_id": dataset_id,
                    "source_family": source_family,
                    "wave": wave,
                    "status": base["audit_status"],
                    "error": base["audit_error"],
                    "raw_path": str(raw_path),
                    "codebook_path": str(codebook_path) if codebook_path else "",
                },
                f,
                sort_keys=False,
                allow_unicode=True,
            )
        return base

    try:
        build_wave_audit, write_audit_outputs = _load_audit_backend()
        rows, summary = build_wave_audit(raw_path, str(codebook_path) if codebook_path else "")
    except Exception as exc:  # pragma: no cover - defensive guard for odd source files
        base["audit_status"] = "blocked_raw_unreadable" if "readstat" in repr(exc).lower() else "blocked_audit_error"
        base["audit_error"] = repr(exc)
        out_yaml.parent.mkdir(parents=True, exist_ok=True)
        with out_yaml.open("w", encoding="utf-8") as f:
            yaml.safe_dump(
                {
                    "dataset_id": dataset_id,
                    "source_family": source_family,
                    "wave": wave,
                    "status": base["audit_status"],
                    "read_status": read_status,
                    "error": base["audit_error"],
                    "raw_path": str(raw_path),
                    "codebook_path": str(codebook_path) if codebook_path else "",
                },
                f,
                sort_keys=False,
                allow_unicode=True,
            )
        return base

    write_audit_outputs(rows, summary, out_csv, out_yaml)
    compact, problem_fields = summarize_rows(rows)
    base.update(
        {
            "audit_status": "green" if compact["manual_review_count"] == 0 and compact["source_structure_disagrees_count"] == 0 else "partial_review",
            "audit_csv": str(out_csv),
            "audit_yaml": str(out_yaml),
            "kind_counts": json.dumps(compact["kind_counts"], sort_keys=True),
            "source_match_counts": json.dumps(compact["source_match_counts"], sort_keys=True),
            "manual_review_count": compact["manual_review_count"],
            "source_structure_disagrees_count": compact["source_structure_disagrees_count"],
            "codebook_stale_count": compact["codebook_stale_count"],
            "codebook_trustworthy_count": compact["codebook_trustworthy_count"],
            "source_present_count": compact["source_present_count"],
            "problem_fields": "|".join(problem_fields[:40]),
            "high_level_conclusion": compact["high_level_conclusion"],
        }
    )

    if not codebook_exists:
        if canonical_intended:
            base["audit_status"] = "partial_missing_codebook"
        elif base["audit_status"] == "green":
            base["audit_status"] = "raw_only_no_codebook"

    return base


def main() -> int:
    manifest_rows = load_manifest_rows()
    raw_rows = [row for row in manifest_rows if _clean(row.get("artifact_kind")) == "raw_data"]

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    validation_rows = [audit_one(row) for row in raw_rows]

    fieldnames = [
        "dataset_id",
        "source_family",
        "wave",
        "canonical_wave",
        "canonical_intended",
        "raw_path",
        "codebook_path",
        "raw_read_status",
        "raw_exists",
        "codebook_exists",
        "raw_row_count",
        "raw_column_count",
        "audit_status",
        "audit_csv",
        "audit_yaml",
        "kind_counts",
        "source_match_counts",
        "manual_review_count",
        "source_structure_disagrees_count",
        "codebook_stale_count",
        "codebook_trustworthy_count",
        "source_present_count",
        "problem_fields",
        "high_level_conclusion",
        "audit_error",
    ]
    with VALIDATION_MANIFEST_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in validation_rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})

    problem_rows = [row for row in validation_rows if row["audit_status"] != "green"]
    with PROBLEM_FILES_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["dataset_id", "source_family", "wave", "canonical_wave", "audit_status", "raw_read_status", "codebook_exists", "problem_fields", "audit_error"])
        writer.writeheader()
        for row in problem_rows:
            writer.writerow({key: row.get(key, "") for key in writer.fieldnames})

    taxonomy = {
        "schema": "source_structure_question_type_taxonomy_v1",
        "global_policy": {
            "special_responses": "Preserve don't know, refusal, and similar responses as meaningful analytical signals unless a specific question type absolutely requires a different treatment.",
            "raw_vs_codebook": "A raw file can be structurally readable but still disagree with the codebook, which means the question type and compute method must be decided from the source shape, not only the codebook text.",
            "compute_rule": "No overnight batch should run until the file-level audit manifest is green or intentionally accepted for the known partial cases.",
        },
        "question_types": build_taxonomy(),
    }
    with TAXONOMY_OUT.open("w", encoding="utf-8") as f:
        yaml.safe_dump(taxonomy, f, sort_keys=False, allow_unicode=True)

    report = {
        "status": "green_source_structure_validation_written",
        "raw_files_checked": len(raw_rows),
        "green_files": sum(1 for row in validation_rows if row["audit_status"] == "green"),
        "partial_files": sum(1 for row in validation_rows if row["audit_status"].startswith("partial") or row["audit_status"].startswith("raw_only")),
        "blocked_files": sum(1 for row in validation_rows if row["audit_status"].startswith("blocked")),
        "canonical_intended_raw_files": sum(1 for row in validation_rows if row["canonical_intended"]),
        "problem_file_count": len(problem_rows),
        "manifest": str(VALIDATION_MANIFEST_OUT),
        "problem_files": str(PROBLEM_FILES_OUT),
        "taxonomy": str(TAXONOMY_OUT),
    }
    with VALIDATION_REPORT_OUT.open("w", encoding="utf-8") as f:
        yaml.safe_dump(report, f, sort_keys=False, allow_unicode=True)

    print(yaml.safe_dump(report, sort_keys=False, allow_unicode=True).strip())
    return 0 if report["blocked_files"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
