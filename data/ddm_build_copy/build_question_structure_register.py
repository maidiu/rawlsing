#!/usr/bin/env python3
"""Build the UID-bearing question structure register from hash-bound audit authority."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
DDM_ROOT = ROOT / "data" / "ddm_build_copy"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_source_wave_identity import (
    SourceWaveIdentityError,
    closed_35_identities,
    resolve_source_wave_identity,
)
from data.ddm_build_copy.ddm_v550_source_structure import (
    derive_source_structure_classification,
    source_structure_review_required,
)

MANIFEST_PATH = DDM_ROOT / "manifests" / "source_structure_validation_manifest.csv"
AUDIT_BINDING_PATH = DDM_ROOT / "manifests" / "source_structure_audit_binding_35wave_v1.json"
TAXONOMY_PATH = DDM_ROOT / "manifests" / "question_type_taxonomy.yaml"
MASTER_PATH = ROOT / "data" / "final_codebooks" / "questions_master_drivers.csv"
OUT_CSV = DDM_ROOT / "manifests" / "question_structure_register.csv"
OUT_YAML = DDM_ROOT / "manifests" / "question_structure_register.yaml"
DEFAULT_AUDIT_ROOT = DDM_ROOT / "reports" / "source_structure_audits"

BINDING_SCHEMA = "source_structure_audit_binding_35wave_v1"
READY_BINDING_STATUS = "READY_HASH_BOUND"

SEMANTIC_MASTER_FIELDS = (
    "final_driver_id",
    "final_driver_scope",
    "final_driver_label",
    "final_driver_origin",
    "semantic_scope",
    "semantic_primary_driver",
    "semantic_secondary_driver",
    "semantic_shared_driver",
    "semantic_regional_driver",
    "semantic_notes",
)


def clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "<na>", "none"} else text


def truthy(value: Any) -> bool:
    return clean(value).lower() in {"1", "true", "yes", "y"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def expected_closed_35_wave_uids() -> set[str]:
    identities = closed_35_identities()
    if len(identities) != 35:
        raise RuntimeError(f"CLOSED_35_IDENTITY_CENSUS_MISMATCH:{len(identities)}")
    return {item.wave_uid for item in identities}


def audit_root() -> Path:
    override = os.environ.get("DDM_SOURCE_STRUCTURE_AUDIT_ROOT", "").strip()
    return Path(override).expanduser().resolve() if override else DEFAULT_AUDIT_ROOT.resolve()


def load_manifest() -> pd.DataFrame:
    csv.field_size_limit(sys.maxsize)
    frame = pd.read_csv(MANIFEST_PATH, low_memory=False)
    return frame.fillna("")


def load_audit_binding(path: Path = AUDIT_BINDING_PATH) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if clean(payload.get("schema")) != BINDING_SCHEMA:
        raise RuntimeError("SOURCE_STRUCTURE_BINDING_SCHEMA_MISMATCH")
    if clean(payload.get("status")) != READY_BINDING_STATUS:
        raise RuntimeError(
            "SOURCE_STRUCTURE_BINDING_NOT_READY:"
            + clean(payload.get("status") or "UNKNOWN")
        )
    expected = expected_closed_35_wave_uids()
    declared = {clean(value) for value in payload.get("expected_wave_uids", []) if clean(value)}
    observed = {clean(value) for value in payload.get("observed_wave_uids", []) if clean(value)}
    if (
        declared != expected
        or observed != expected
        or len(payload.get("expected_wave_uids", [])) != 35
        or len(payload.get("observed_wave_uids", [])) != 35
    ):
        raise RuntimeError(
            "SOURCE_STRUCTURE_BINDING_SCOPE_MISMATCH:"
            f"declared={len(declared)} observed={len(observed)} expected={len(expected)}"
        )
    if any("asian_barometer_w6" in value for value in observed):
        raise RuntimeError("SOURCE_STRUCTURE_BINDING_EXCLUDED_W6_PRESENT")
    return payload


def resolve_bound_audit_artifacts(
    binding: dict[str, Any],
    *,
    root: Path | None = None,
) -> list[tuple[dict[str, Any], Path]]:
    root = (root or audit_root()).resolve()
    artifacts = binding.get("artifacts") or []
    if len(artifacts) != 35:
        raise RuntimeError(f"SOURCE_STRUCTURE_BINDING_ARTIFACT_COUNT_MISMATCH:{len(artifacts)}")
    resolved: list[tuple[dict[str, Any], Path]] = []
    observed_uids: set[str] = set()
    for artifact in artifacts:
        wave_uid = clean(artifact.get("wave_uid"))
        if not truthy(artifact.get("closed_35_member")):
            raise RuntimeError(f"SOURCE_STRUCTURE_BINDING_NONPRODUCTION_ARTIFACT:{wave_uid}")
        if "asian_barometer_w6" in wave_uid:
            raise RuntimeError("SOURCE_STRUCTURE_BINDING_EXCLUDED_W6_PRESENT")
        filename = clean(artifact.get("audit_file"))
        expected_hash = clean(artifact.get("audit_sha256"))
        if not filename or Path(filename).is_absolute() or Path(filename).name != filename:
            raise RuntimeError(f"SOURCE_STRUCTURE_BINDING_NONPORTABLE_PATH:{filename}")
        if not expected_hash:
            raise RuntimeError(f"SOURCE_STRUCTURE_BINDING_MISSING_HASH:{filename}")
        path = (root / filename).resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise RuntimeError(f"SOURCE_STRUCTURE_BINDING_PATH_ESCAPE:{filename}") from exc
        if not path.is_file():
            raise RuntimeError(f"SOURCE_STRUCTURE_BOUND_AUDIT_MISSING:{filename}")
        actual_hash = sha256_file(path)
        if actual_hash != expected_hash:
            raise RuntimeError(
                f"SOURCE_STRUCTURE_BOUND_AUDIT_HASH_MISMATCH:{filename}:"
                f"expected={expected_hash}:actual={actual_hash}"
            )
        if wave_uid in observed_uids:
            raise RuntimeError(f"SOURCE_STRUCTURE_BINDING_DUPLICATE_WAVE_UID:{wave_uid}")
        identity = resolve_source_wave_identity(
            clean(artifact.get("canonical_display_source")),
            clean(artifact.get("canonical_display_wave")),
            require_closed_35=True,
        )
        if (
            identity.source_family_uid != clean(artifact.get("source_family_uid"))
            or identity.wave_uid != wave_uid
        ):
            raise RuntimeError(f"SOURCE_STRUCTURE_BINDING_IDENTITY_MISMATCH:{wave_uid}")
        observed_uids.add(wave_uid)
        resolved.append((artifact, path))
    expected = expected_closed_35_wave_uids()
    if observed_uids != expected:
        raise RuntimeError(
            "SOURCE_STRUCTURE_BOUND_AUDIT_UID_COVERAGE_MISMATCH:"
            f"missing={sorted(expected-observed_uids)}:"
            f"unexpected={sorted(observed_uids-expected)}"
        )
    return resolved


def identity_context_from_artifact(
    artifact: dict[str, Any],
    file_row: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Add governed identity without changing legacy field semantics."""
    file_row = file_row or {}
    legacy_source = clean(file_row.get("source") or file_row.get("source_family"))
    legacy_family = clean(file_row.get("source_family")) or legacy_source
    legacy_wave = clean(file_row.get("wave")) or clean(artifact.get("raw_wave"))
    legacy_canonical_wave = clean(file_row.get("canonical_wave")) or clean(artifact.get("canonical_display_wave"))
    return {
        "dataset_id": clean(artifact.get("dataset_id")),
        "source": legacy_source or clean(artifact.get("raw_source")),
        "source_family": legacy_family or clean(artifact.get("canonical_display_source")),
        "wave": legacy_wave,
        "canonical_wave": legacy_canonical_wave,
        "raw_source": clean(artifact.get("raw_source")),
        "raw_wave": clean(artifact.get("raw_wave")),
        "canonical_display_source": clean(artifact.get("canonical_display_source")),
        "canonical_display_wave": clean(artifact.get("canonical_display_wave")),
        "source_family_uid": clean(artifact.get("source_family_uid")),
        "wave_uid": clean(artifact.get("wave_uid")),
        "governance_state": clean(artifact.get("governance_state")),
        "closed_35_member": truthy(artifact.get("closed_35_member")),
        "canonical_intended": truthy(artifact.get("closed_35_member")),
        # Legacy local paths are provenance only. Nothing in this context opens them.
        "raw_path": clean(file_row.get("raw_path") or artifact.get("legacy_raw_path_provenance")),
        "codebook_path": clean(file_row.get("codebook_path") or artifact.get("legacy_codebook_path_provenance")),
        "raw_read_status": clean(file_row.get("raw_read_status")),
        "raw_exists": truthy(file_row.get("raw_exists")),
        "codebook_exists": truthy(file_row.get("codebook_exists")),
        "raw_row_count": clean(file_row.get("raw_row_count")),
        "raw_column_count": clean(file_row.get("raw_column_count")),
        "audit_status": clean(file_row.get("audit_status")),
        "audit_sha256": clean(artifact.get("audit_sha256")),
        "manual_review_count": clean(file_row.get("manual_review_count")),
        "source_structure_disagrees_count": clean(file_row.get("source_structure_disagrees_count")),
        "codebook_stale_count": clean(file_row.get("codebook_stale_count")),
        "codebook_trustworthy_count": clean(file_row.get("codebook_trustworthy_count")),
        "source_present_count": clean(file_row.get("source_present_count")),
        "problem_fields": clean(file_row.get("problem_fields")),
        "high_level_conclusion": clean(file_row.get("high_level_conclusion")),
        "audit_error": clean(file_row.get("audit_error")),
    }


def load_taxonomy() -> dict[str, dict[str, str]]:
    raw = yaml.safe_load(TAXONOMY_PATH.read_text(encoding="utf-8")) or {}
    out: dict[str, dict[str, str]] = {}
    for row in raw.get("question_types", []):
        qk = clean(row.get("question_kind"))
        if qk:
            out[qk] = {
                "structural_role": clean(row.get("structural_role")),
                "default_handling": clean(row.get("default_handling")),
                "recommended_computation": clean(row.get("recommended_computation")),
                "do_not_do": clean(row.get("do_not_do")),
            }
    return out


def load_master() -> pd.DataFrame:
    frame = pd.read_csv(MASTER_PATH, low_memory=False)
    for column in frame.columns:
        if frame[column].dtype == "O":
            frame[column] = frame[column].fillna("").astype(str)
    return frame


def file_audit_rows(audit_csv: Path) -> pd.DataFrame:
    frame = pd.read_csv(audit_csv, low_memory=False)
    for column in frame.columns:
        if frame[column].dtype == "O":
            frame[column] = frame[column].fillna("").astype(str)
    return frame


def _resolve_master_identity(row: dict[str, Any]):
    source = clean(row.get("source") or row.get("source_family"))
    wave = clean(row.get("wave") or row.get("canonical_wave"))
    try:
        return resolve_source_wave_identity(source, wave)
    except SourceWaveIdentityError:
        return None


def build_master_lookup(master: pd.DataFrame) -> dict[tuple[str, str, str], dict[str, Any]]:
    lookup: dict[tuple[str, str, str], dict[str, Any]] = {}
    semantic_fingerprint: dict[tuple[str, str, str], tuple[str, ...]] = {}
    for row in master.to_dict(orient="records"):
        identity = _resolve_master_identity(row)
        var_name = clean(row.get("var_name"))
        if identity is None or not var_name:
            continue
        key = (identity.source_family_uid, identity.wave_uid, var_name)
        fingerprint = tuple(clean(row.get(field)) for field in SEMANTIC_MASTER_FIELDS)
        if key in semantic_fingerprint and semantic_fingerprint[key] != fingerprint:
            raise RuntimeError(
                "CONFLICTING_MASTER_SEMANTICS_FOR_UID:"
                + "|".join(key)
            )
        lookup[key] = row
        semantic_fingerprint[key] = fingerprint
    return lookup


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


def validate_qsr_publication_scope(frame: pd.DataFrame) -> dict[str, Any]:
    expected = expected_closed_35_wave_uids()
    if frame.empty or "wave_uid" not in frame.columns:
        raise RuntimeError("QSR_PUBLICATION_EMPTY_OR_UIDLESS")
    observed = {clean(value) for value in frame["wave_uid"].tolist() if clean(value)}
    if observed != expected:
        raise RuntimeError(
            "QSR_PUBLICATION_UID_COVERAGE_MISMATCH:"
            f"missing={sorted(expected-observed)}:"
            f"unexpected={sorted(observed-expected)}"
        )
    if "closed_35_member" in frame.columns and not frame["closed_35_member"].map(truthy).all():
        raise RuntimeError("QSR_PUBLICATION_CONTAINS_NONPRODUCTION_ROWS")
    if any("asian_barometer_w6" in value for value in observed):
        raise RuntimeError("QSR_PUBLICATION_EXCLUDED_W6_PRESENT")
    return {"status": "PASS", "wave_uid_count": len(observed)}


def build_register() -> pd.DataFrame:
    manifest = load_manifest()
    manifest_lookup = {
        clean(row.get("dataset_id")): row for row in manifest.to_dict(orient="records")
        if clean(row.get("dataset_id"))
    }
    binding = load_audit_binding()
    bound_audits = resolve_bound_audit_artifacts(binding)
    taxonomy = load_taxonomy()
    master_lookup = build_master_lookup(load_master())

    merged_rows: list[dict[str, Any]] = []
    for artifact, audit_path in bound_audits:
        wave_uid = clean(artifact.get("wave_uid"))
        source_uid = clean(artifact.get("source_family_uid"))
        dataset_id = clean(artifact.get("dataset_id"))
        file_row = manifest_lookup.get(dataset_id, {})
        audit = file_audit_rows(audit_path)

        file_context = identity_context_from_artifact(artifact, file_row)

        for _, row in audit.iterrows():
            name = clean(row.get("name"))
            record_kind = clean(row.get("record_kind"))
            lookup_name = clean(row.get("matched_codebook_var")) or name
            master_row = master_lookup.get((source_uid, wave_uid, lookup_name), {})
            question_kind = clean(row.get("classification_kind"))
            taxonomy_row = taxonomy.get(question_kind, {})
            semantic_input = {
                **file_context,
                **row.to_dict(),
                "question_type": question_kind,
                "handling_rule": taxonomy_row.get("default_handling", ""),
                "recommended_computation": taxonomy_row.get("recommended_computation", ""),
                "question_type_structural_role": taxonomy_row.get("structural_role", ""),
            }
            review_required = source_structure_review_required(semantic_input)
            merged = {
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
                "access_expression": clean(row.get("matched_source_column")) or clean(row.get("matched_codebook_var")) or name,
                "question_type": question_kind,
                "handling_rule": taxonomy_row.get("default_handling", ""),
                "recommended_computation": taxonomy_row.get("recommended_computation", ""),
                "do_not_do": taxonomy_row.get("do_not_do", ""),
                "question_type_structural_role": taxonomy_row.get("structural_role", ""),
                "source_structure_classification": derive_source_structure_classification({
                    **semantic_input,
                    "source_structure_source": "source_structure_validation_manifest+question_type_taxonomy",
                }),
                "source_structure_basis": "source_structure_validation_manifest+question_type_taxonomy",
                "source_structure_review_required": review_required,
                "source_structure_confidence": "low" if review_required else "high",
                "source_structure_source": "source_structure_validation_manifest+question_type_taxonomy",
            }
            for field in SEMANTIC_MASTER_FIELDS:
                merged[field] = clean(master_row.get(field))
            merged_rows.append(merged)

    out = pd.DataFrame(merged_rows)
    if out.empty:
        raise RuntimeError("No question structure rows were assembled.")
    out = out.sort_values(
        ["source_family", "canonical_wave", "question_name", "record_kind"],
        ascending=[True, True, True, True],
    ).reset_index(drop=True)
    validate_qsr_publication_scope(out)
    return out


def write_outputs(df: pd.DataFrame) -> None:
    scope = validate_qsr_publication_scope(df)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    tmp_csv = OUT_CSV.with_suffix(".csv.tmp")
    df.to_csv(tmp_csv, index=False)
    payload = {
        "status": "green_question_structure_register_written",
        "publication_scope": "CLOSED_35",
        "wave_uid_count": scope["wave_uid_count"],
        "row_count": int(len(df)),
        "source_families": sorted(df["source_family"].dropna().astype(str).unique().tolist()),
        "canonical_waves": sorted(df["canonical_wave"].dropna().astype(str).unique().tolist()),
        "canonical_display_waves": sorted(df["canonical_display_wave"].astype(str).unique().tolist()),
        "wave_uids": sorted(df["wave_uid"].astype(str).unique().tolist()),
        "record_kinds": df["record_kind"].value_counts().to_dict(),
        "question_types": df["question_type"].value_counts().to_dict(),
        "manual_review_rows": int((df["needs_manual_review"].astype(str).str.lower() == "yes").sum()),
        "output_file": OUT_CSV.relative_to(ROOT).as_posix(),
        "audit_binding": AUDIT_BINDING_PATH.relative_to(ROOT).as_posix(),
        "notes": [
            "Raw/native source and wave are preserved separately from governed display labels and UIDs.",
            "All execution audit inputs are portable relative filenames with verified SHA-256 content binding.",
            "Question semantics and source-structure classifications are inherited unchanged from their existing authority surfaces.",
        ],
    }
    tmp_yaml = OUT_YAML.with_suffix(".yaml.tmp")
    tmp_yaml.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
    tmp_csv.replace(OUT_CSV)
    tmp_yaml.replace(OUT_YAML)


def main() -> int:
    frame = build_register()
    write_outputs(frame)
    print(f"Wrote {len(frame)} question structure rows to {OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
