#!/usr/bin/env python3
"""Build a consolidated question structure register.

This register merges:
- the canonical semantic/driver master
- the per-file structural audit manifest
- the per-file audit rows
- the question type taxonomy

The goal is to make every question/response shape explicit before any long
compute loop runs. The output is question-centric, but it also records file-level
status so the ingester knows what is safe, partial, or needs manual handling.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
DDM_ROOT = ROOT / "data" / "ddm_build_copy"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v550_source_structure import derive_source_structure_classification, source_structure_review_required


MANIFEST_PATH = DDM_ROOT / "manifests" / "source_structure_validation_manifest.csv"
TAXONOMY_PATH = DDM_ROOT / "manifests" / "question_type_taxonomy.yaml"
MASTER_PATH = ROOT / "data" / "final_codebooks" / "questions_master_drivers.csv"
OUT_CSV = DDM_ROOT / "manifests" / "question_structure_register.csv"
OUT_YAML = DDM_ROOT / "manifests" / "question_structure_register.yaml"


def clean(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and pd.isna(value):
        return ""
    text = str(value).strip()
    if text.lower() in {"nan", "<na>", "none"}:
        return ""
    return text


def truthy(value: Any) -> bool:
    return clean(value).lower() in {"1", "true", "yes", "y"}


def load_manifest() -> pd.DataFrame:
    csv.field_size_limit(sys.maxsize)
    df = pd.read_csv(MANIFEST_PATH)
    df["canonical_intended"] = df["canonical_intended"].apply(truthy)
    return df


def load_taxonomy() -> dict[str, dict[str, str]]:
    raw = yaml.safe_load(TAXONOMY_PATH.read_text(encoding="utf-8"))
    out: dict[str, dict[str, str]] = {}
    for row in raw.get("question_types", []):
        qk = clean(row.get("question_kind"))
        if not qk:
            continue
        out[qk] = {
            "structural_role": clean(row.get("structural_role")),
            "default_handling": clean(row.get("default_handling")),
            "recommended_computation": clean(row.get("recommended_computation")),
            "do_not_do": clean(row.get("do_not_do")),
        }
    return out


def load_master() -> pd.DataFrame:
    df = pd.read_csv(MASTER_PATH)
    for col in df.columns:
        if df[col].dtype == "O":
            df[col] = df[col].fillna("").astype(str)
    return df


def file_audit_rows(audit_csv: Path) -> pd.DataFrame:
    df = pd.read_csv(audit_csv)
    for col in df.columns:
        if df[col].dtype == "O":
            df[col] = df[col].fillna("").astype(str)
    return df


def access_pattern(row: pd.Series) -> str:
    record_kind = clean(row.get("record_kind"))
    match_type = clean(row.get("source_match_type"))
    kind = clean(row.get("classification_kind"))
    role = clean(row.get("structural_role"))
    child_count = int(float(clean(row.get("child_count")) or 0))

    if role == "metadata":
        return "metadata_field"
    if record_kind == "source_column" and match_type == "child_of_parent":
        return "child_column_of_parent"
    if record_kind == "source_column" and match_type == "true_extra":
        return "source_extra_column"
    if kind in {"multi_select", "matrix", "split_block"} and child_count > 0:
        return "parent_with_children"
    if kind == "stem":
        return "structural_stem"
    if kind == "open_text":
        return "direct_text_answer"
    return "direct_answer_column"


def build_register() -> pd.DataFrame:
    manifest = load_manifest()
    taxonomy = load_taxonomy()
    master = load_master()

    master_lookup = {
        (clean(row.source), clean(row.wave), clean(row.var_name)): row._asdict()
        for row in master.itertuples(index=False)
    }

    merged_rows: list[dict[str, Any]] = []
    canonical = manifest.loc[manifest["canonical_intended"]].copy()
    canonical = canonical[canonical["audit_csv"].astype(str).str.strip().isin({"", ".", "nan", "None"}) == False]

    for _, file_row in canonical.iterrows():
        audit_path = Path(clean(file_row["audit_csv"]))
        if not audit_path.exists() or audit_path.is_dir():
            continue
        audit = file_audit_rows(audit_path)
        file_context = {
            "dataset_id": clean(file_row.get("dataset_id")),
            "source": clean(file_row.get("source") or file_row.get("source_family")),
            "source_family": clean(file_row.get("source_family")),
            "wave": clean(file_row.get("wave")),
            "canonical_wave": clean(file_row.get("canonical_wave")),
            "canonical_intended": truthy(file_row.get("canonical_intended")),
            "raw_path": clean(file_row.get("raw_path")),
            "codebook_path": clean(file_row.get("codebook_path")),
            "raw_read_status": clean(file_row.get("raw_read_status")),
            "raw_exists": truthy(file_row.get("raw_exists")),
            "codebook_exists": truthy(file_row.get("codebook_exists")),
            "raw_row_count": clean(file_row.get("raw_row_count")),
            "raw_column_count": clean(file_row.get("raw_column_count")),
            "audit_status": clean(file_row.get("audit_status")),
            "manual_review_count": clean(file_row.get("manual_review_count")),
            "source_structure_disagrees_count": clean(file_row.get("source_structure_disagrees_count")),
            "codebook_stale_count": clean(file_row.get("codebook_stale_count")),
            "codebook_trustworthy_count": clean(file_row.get("codebook_trustworthy_count")),
            "source_present_count": clean(file_row.get("source_present_count")),
            "problem_fields": clean(file_row.get("problem_fields")),
            "high_level_conclusion": clean(file_row.get("high_level_conclusion")),
            "audit_error": clean(file_row.get("audit_error")),
        }

        for _, row in audit.iterrows():
            name = clean(row.get("name"))
            record_kind = clean(row.get("record_kind"))
            lookup_name = clean(row.get("matched_codebook_var")) or name
            master_row = master_lookup.get((file_context["source_family"], file_context["canonical_wave"], lookup_name), {})

            question_kind = clean(row.get("classification_kind"))
            taxonomy_row = taxonomy.get(question_kind, {})
            review_required = source_structure_review_required(
                {
                    **file_context,
                    **row.to_dict(),
                    "question_type": question_kind,
                    "handling_rule": taxonomy_row.get("default_handling", ""),
                    "recommended_computation": taxonomy_row.get("recommended_computation", ""),
                    "question_type_structural_role": taxonomy_row.get("structural_role", ""),
                }
            )
            merged_rows.append(
                {
                    **file_context,
                    "record_kind": record_kind,
                    "question_name": name,
                    "var_name": clean(row.get("matched_source_column")) or name,
                    "question_id": f"{file_context['source_family']}:{file_context['canonical_wave']}:{name}",
                    "classification_kind": question_kind,
                    "structural_role": clean(row.get("structural_role")),
                    "scope": clean(row.get("scope")),
                    "matched_codebook_var": clean(row.get("matched_codebook_var")),
                    "parent_var_name": clean(row.get("matched_codebook_var")),
                    "matched_source_column": clean(row.get("matched_source_column")),
                    "source_match_type": clean(row.get("source_match_type")),
                    "source_present": clean(row.get("source_present")),
                    "child_count": clean(row.get("child_count")),
                    "child_columns": clean(row.get("child_columns")),
                    "source_nonnull_count": clean(row.get("source_nonnull_count")),
                    "source_unique_nonnull_count": clean(row.get("source_unique_nonnull_count")),
                    "source_value_label_count": clean(row.get("source_value_label_count")),
                    "response_option_count": clean(row.get("response_option_count")),
                    "question_text": clean(row.get("question_text")),
                    "codebook_options_trustworthy": clean(row.get("codebook_options_trustworthy")),
                    "codebook_options_stale": clean(row.get("codebook_options_stale")),
                    "source_structure_disagrees_with_codebook": clean(row.get("source_structure_disagrees_with_codebook")),
                    "needs_manual_review": clean(row.get("needs_manual_review")),
                    "evidence": clean(row.get("evidence")),
                    "notes": clean(row.get("notes")),
                    "access_pattern": access_pattern(row),
                    "access_expression": (
                        clean(row.get("matched_source_column"))
                        if clean(row.get("matched_source_column"))
                        else clean(row.get("matched_codebook_var")) or name
                    ),
                    "question_type": question_kind,
                    "handling_rule": taxonomy_row.get("default_handling", ""),
                    "recommended_computation": taxonomy_row.get("recommended_computation", ""),
                    "do_not_do": taxonomy_row.get("do_not_do", ""),
                    "question_type_structural_role": taxonomy_row.get("structural_role", ""),
                    "source_structure_classification": derive_source_structure_classification(
                        {
                            **file_context,
                            **row.to_dict(),
                            "question_type": question_kind,
                            "handling_rule": taxonomy_row.get("default_handling", ""),
                            "recommended_computation": taxonomy_row.get("recommended_computation", ""),
                            "question_type_structural_role": taxonomy_row.get("structural_role", ""),
                            "source_structure_source": "source_structure_validation_manifest+question_type_taxonomy",
                        }
                    ),
                    "source_structure_basis": "source_structure_validation_manifest+question_type_taxonomy",
                    "source_structure_review_required": review_required,
                    "source_structure_confidence": "low" if review_required else "high",
                    "source_structure_source": "source_structure_validation_manifest+question_type_taxonomy",
                    "final_driver_id": clean(master_row.get("final_driver_id")),
                    "final_driver_scope": clean(master_row.get("final_driver_scope")),
                    "final_driver_label": clean(master_row.get("final_driver_label")),
                    "final_driver_origin": clean(master_row.get("final_driver_origin")),
                    "semantic_scope": clean(master_row.get("semantic_scope")),
                    "semantic_primary_driver": clean(master_row.get("semantic_primary_driver")),
                    "semantic_secondary_driver": clean(master_row.get("semantic_secondary_driver")),
                    "semantic_shared_driver": clean(master_row.get("semantic_shared_driver")),
                    "semantic_regional_driver": clean(master_row.get("semantic_regional_driver")),
                    "semantic_notes": clean(master_row.get("semantic_notes")),
                }
            )

    out = pd.DataFrame(merged_rows)
    if out.empty:
        raise RuntimeError("No question structure rows were assembled.")

    out = out.sort_values(
        ["source_family", "canonical_wave", "question_name", "record_kind"],
        ascending=[True, True, True, True],
    ).reset_index(drop=True)
    return out


def write_outputs(df: pd.DataFrame) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)
    payload = {
        "status": "green_question_structure_register_written",
        "row_count": int(len(df)),
        "source_families": sorted(df["source_family"].dropna().astype(str).unique().tolist()),
        "canonical_waves": sorted(df["canonical_wave"].dropna().astype(str).unique().tolist()),
        "record_kinds": df["record_kind"].value_counts().to_dict(),
        "question_types": df["question_type"].value_counts().to_dict(),
        "manual_review_rows": int((df["needs_manual_review"].astype(str).str.lower() == "yes").sum()),
        "output_file": str(OUT_CSV),
        "notes": [
            "This register merges the semantic driver atlas with file-level source structure.",
            "access_pattern and access_expression are the forward-looking ingest hints for split parents and children.",
            "Don't know / refusal remain preserved at the structure layer and are not silently erased.",
        ],
    }
    OUT_YAML.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def main() -> int:
    df = build_register()
    write_outputs(df)
    print(f"Wrote {len(df)} question structure rows to {OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
