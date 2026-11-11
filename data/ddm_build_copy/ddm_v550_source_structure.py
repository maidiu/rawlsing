#!/usr/bin/env python3
"""Source-structure helpers for V550 through-V552 compilation.

This module centralizes the deterministic source-structure classification and
join logic used by the register builder, shard builder, and source-structure
population audit.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any, Mapping

import pandas as pd
import re

from data.ddm_build_copy.ddm_survey_identity import canonical_family_key

ROOT = Path(__file__).resolve().parents[2]
DDM_ROOT = ROOT / "data" / "ddm_build_copy"
DEFAULT_STRUCTURE_REGISTER = DDM_ROOT / "manifests" / "question_structure_register.csv"
DEFAULT_TAXONOMY = DDM_ROOT / "manifests" / "question_type_taxonomy.yaml"
DEFAULT_VALIDATION_MANIFEST = DDM_ROOT / "manifests" / "source_structure_validation_manifest.csv"
DEFAULT_SOURCE_STRUCTURE_VALIDATION_OUTPUT = ROOT / "data" / "ddm_repository_copy" / "v550" / "validation"

POSITIVE_TOKENS = {"yes", "true", "1", "y", "on"}
_JOIN_KEY_PATTERN = re.compile(r"[^a-z0-9]+")
_SES_RELATION_EVIDENCE_PATTERN = re.compile(
    r"^(?:"
    r"(?:masei|pasei|cosei|sei10|spsei(?:10)?)(?:[_-]?\d{2,4})?(?:educ|inc)?"
    r"|spden(?:[_-]?\d{2,4})?"
    r"|numemps(?:[_-]?\d{2,4})?"
    r")$"
)

POSITION_CONTINUOUS_FIELDS = {
    "age",
    "age_years",
    "income",
    "income_amount",
    "household_size",
    "children_count",
    "num_children",
    "years_education",
}

RESPONDENT_POSITION_FIELDS = {
    "age_group",
    "sex",
    "gender",
    "education",
    "education_level",
    "income_level",
    "religion_label",
    "urban_rural",
    "region",
    "ethnicity",
    "language",
    "employment",
    "marital",
    "country",
    "country_code",
}

ADMINISTRATIVE_FIELDS = {
    "respondent_id",
    "case_id",
    "vpsu",
    "vstrat",
    "psu",
    "strata",
    "cluster",
    "weight",
    "weight_value",
    "weight_status",
    "wtss",
    "wtssall",
    "wtssnr",
    "wtssps",
    "source_file",
    "source",
    "source_family",
    "wave",
    "canonical_wave",
    "country_code",
    "survey_year",
    "year",
}

WEIGHT_FIELDS = {
    "weight",
    "weight_value",
    "weight_status",
    "wtss",
    "wtssall",
    "wtssnr",
    "wtssps",
    "sampling_weight",
    "poststrat_weight",
    "design_weight",
}

OPEN_TEXT_TYPES = {"open_text", "text", "free_text"}
HARD_ADMIN_FIELDS = {
    "respondent_id",
    "case_id",
    "source_file",
    "dataset_id",
    "upload_date",
}
SURVEY_WEIGHT_FIELDS = {
    "weight",
    "weight_value",
    "weight_status",
    "wtss",
    "wtssall",
    "wtssnr",
    "wtssps",
    "sampling_weight",
    "poststrat_weight",
    "design_weight",
}
SURVEY_DESIGN_FIELDS = {
    "vpsu",
    "vstrat",
    "psu",
    "strata",
    "cluster",
}
RESPONDENT_POSITION_FIELDS = {
    "age_group",
    "sex",
    "gender",
    "education",
    "education_level",
    "income",
    "income_level",
    "religion_label",
    "urban_rural",
    "region",
    "ethnicity",
    "language",
    "employment",
    "marital",
}
CONTINUOUS_POSITION_FIELDS = {
    "age",
    "age_years",
    "income",
    "income_amount",
    "household_size",
    "children_count",
    "num_children",
    "years_education",
}


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return str(value).strip()


def _normalized(value: Any) -> str:
    return _clean(value).lower()


def _to_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and not pd.isna(value):
        return value != 0
    text = _clean(value).lower()
    if text in POSITIVE_TOKENS:
        return True
    if text in {"0", "false", "f", "no", "n", "off", "", "nan", "none"}:
        return False
    return default


def _first_nonempty(row: Mapping[str, Any], *names: str, default: str = "") -> str:
    for name in names:
        value = _clean(row.get(name))
        if value:
            return value
    return default


def _source_structure_source(row: Mapping[str, Any]) -> str:
    source = _clean(row.get("source_structure_source"))
    if source:
        return source
    return "question_structure_register+question_type_taxonomy"


def _join_confidence_to_source_structure_confidence(join_confidence: str) -> str:
    value = _normalized(join_confidence)
    if value in {"exact", "unique"}:
        return "high"
    if value in {"manual"}:
        return "medium"
    if value in {"ambiguous", "missing", ""}:
        return "low"
    return "medium"


def _normalized_join_key(value: Any) -> str:
    """Normalize join-like identifiers so punctuation-delimited waves still match.

    This intentionally collapses separators like `:`, `-`, `/`, spaces, and
    repeated punctuation into a single underscore. The goal is to make wave
    naming differences harmless while still preserving the alphanumeric spine
    of the identifier.
    """
    cleaned = _clean(value).lower()
    if not cleaned:
        return ""
    cleaned = _JOIN_KEY_PATTERN.sub("_", cleaned)
    return re.sub(r"_+", "_", cleaned).strip("_")


def _normalized_question_id(value: Any) -> str:
    return _normalized_join_key(value)


def _row_field_value(row: Any, field: str, default: Any = "") -> Any:
    if isinstance(row, Mapping):
        return row.get(field, default)
    if hasattr(row, field):
        return getattr(row, field)
    if hasattr(row, "get"):
        try:
            return row.get(field, default)
        except TypeError:
            pass
    return default


def _is_ses_relation_evidence(row: Any) -> bool:
    """Legacy GSS adapter for derived SES/spouse variables.

    These variable names are GSS conventions.  They must never classify a
    similarly named variable from another survey family.
    """
    source = _clean(
        _row_field_value(row, "source")
        or _row_field_value(row, "source_family")
    )
    if canonical_family_key(source) != "gss":
        return False
    for field in ("var_code", "var_name", "question_id", "matched_codebook_var", "question_name"):
        value = _clean(_row_field_value(row, field))
        if value and _SES_RELATION_EVIDENCE_PATTERN.match(_normalized_join_key(value)):
            return True
    return False


def _candidate_texts(row: Mapping[str, Any]) -> list[str]:
    fields = [
        "var_code",
        "var_name",
        "question_name",
        "matched_codebook_var",
        "matched_source_column",
        "parent_var_name",
        "question_text",
        "question_type",
        "handling_rule",
        "recommended_computation",
    ]
    return [_normalized(row.get(field)) for field in fields if _clean(row.get(field))]


def _candidate_text(row: Mapping[str, Any]) -> str:
    return " ".join(token for token in _candidate_texts(row) if token)


def _text_has_token(text: str, token: str) -> bool:
    text = _normalized(text)
    token = _normalized(token)
    if not text or not token:
        return False
    pattern = rf"(^|[^a-z0-9]){re.escape(token)}([^a-z0-9]|$)"
    return re.search(pattern, text) is not None


def _any_field_matches(row: Mapping[str, Any], tokens: set[str], *, include_candidate_blob: bool = True) -> bool:
    fields = [
        "var_code",
        "var_name",
        "question_name",
        "matched_codebook_var",
        "matched_source_column",
        "parent_var_name",
        "question_text",
    ]
    for field in fields:
        value = _clean(row.get(field))
        if value and _normalized(value) in tokens:
            return True
        if value:
            for token in tokens:
                if _text_has_token(value, token):
                    return True
    if include_candidate_blob:
        candidate_blob = _candidate_text(row)
        for token in tokens:
            if _text_has_token(candidate_blob, token):
                return True
    return False


def derive_source_structure_classification(row: Mapping[str, Any]) -> str:
    """Return a deterministic non-blank source-structure class."""
    kind = _normalized(row.get("question_type"))
    handling = _normalized(row.get("handling_rule"))
    computation = _normalized(row.get("recommended_computation"))
    structural_role = _normalized(row.get("question_type_structural_role"))
    access_pattern = _normalized(row.get("access_pattern"))
    final_scope = _normalized(row.get("final_driver_scope"))
    source_match_type = _normalized(row.get("source_match_type"))
    child_count = int(float(_clean(row.get("child_count")) or 0) or 0)
    candidate_blob = _candidate_text(row)
    var_code = _normalized(row.get("var_code") or row.get("var_name"))
    question_name = _normalized(row.get("question_name"))
    matched_source_column = _normalized(row.get("matched_source_column"))
    matched_codebook_var = _normalized(row.get("matched_codebook_var"))
    parent_var_name = _normalized(row.get("parent_var_name"))

    if _is_ses_relation_evidence(row):
        return "substantive_scale"

    if kind in OPEN_TEXT_TYPES or _any_field_matches(row, {"open_text", "free_text", "free text", "text response", "qualitative"}):
        return "open_text_excluded"

    if (
        _any_field_matches(row, HARD_ADMIN_FIELDS)
        or final_scope == "metadata"
        or handling == "administrative_metadata"
        or structural_role == "metadata"
    ):
        return "administrative_metadata"

    if _any_field_matches(row, SURVEY_WEIGHT_FIELDS) or _text_has_token(handling, "weight") or _text_has_token(computation, "weight") or final_scope == "weight":
        return "survey_weight_or_design_metadata"

    if _any_field_matches(row, SURVEY_DESIGN_FIELDS) or _text_has_token(handling, "design") or final_scope == "design":
        return "survey_design_metadata"

    if _any_field_matches(row, {"country_code", "country code"}) or var_code == "country_code" or matched_source_column == "country_code":
        return "structural_context"

    if _any_field_matches(row, RESPONDENT_POSITION_FIELDS):
        return "respondent_position_coordinate"

    if _any_field_matches(row, CONTINUOUS_POSITION_FIELDS):
        return "continuous_position_coordinate"

    if kind == "multi_select" or _text_has_token(candidate_blob, "multi select") or source_match_type == "child_of_parent":
        return "multi_select_child"
    if kind == "matrix" or _text_has_token(candidate_blob, "matrix") or _text_has_token(access_pattern, "row"):
        return "matrix_child"
    if kind in {"single_choice", "scale"} or any(_text_has_token(computation, token) for token in ["response distribution", "distribution", "driver-mapped cloud", "ordinal"]) or any(_text_has_token(candidate_blob, token) for token in ["agree", "trust", "confidence", "satisfaction", "importance", "frequency"]):
        if kind == "single_choice" or _text_has_token(candidate_blob, "single choice"):
            return "substantive_single_choice"
        return "substantive_scale"
    if kind == "stem":
        return "structural_context"
    if kind == "derived_or_reference":
        return "structural_context"

    if "context" in final_scope or handling in {"structural_context", "administrative_metadata"}:
        return "structural_context"

    return "unknown"


def source_structure_review_required(row: Mapping[str, Any], classification: str | None = None) -> bool:
    classification = classification or derive_source_structure_classification(row)
    review_flag = _to_bool(row.get("needs_manual_review")) or _to_bool(row.get("review_required"))
    return review_flag or classification == "unknown"


def load_question_structure_register(path: Path | None = None) -> pd.DataFrame:
    override = os.environ.get("DDM_QUESTION_STRUCTURE_REGISTER", "").strip()
    resolved = Path(path or override or DEFAULT_STRUCTURE_REGISTER)
    if not resolved.exists():
        return pd.DataFrame()
    frame = pd.read_csv(resolved, low_memory=False)
    if "var_code" not in frame.columns and "var_name" in frame.columns:
        frame["var_code"] = frame["var_name"]
    for column in ["question_id", "var_code", "var_name", "matched_codebook_var", "matched_source_column", "parent_var_name", "question_name"]:
        if column in frame.columns:
            frame[f"{column}_normalized"] = frame[column].map(_normalized_join_key)
    for column in ["source_structure_review_required", "source_structure_fields_joined"]:
        if column in frame.columns:
            frame[column] = frame[column].map(lambda value: _to_bool(value, False))
    return frame


def _normalize_keys(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    for column in ["source", "wave", "canonical_wave", "question_id", "var_code", "var_name", "question_name", "matched_codebook_var", "matched_source_column", "parent_var_name"]:
        if column in out.columns:
            out[column] = out[column].fillna("").astype(str).str.strip()
            if column in {"question_id", "var_code", "var_name", "question_name", "matched_codebook_var", "matched_source_column", "parent_var_name"}:
                out[f"{column}_normalized"] = out[column].map(_normalized_join_key)
    return out


def match_source_structure_row(question_row: Mapping[str, Any], register: pd.DataFrame) -> tuple[dict[str, Any], str, str]:
    """Return the best deterministic register row and the join key/confidence."""
    if register.empty:
        classification = derive_source_structure_classification(question_row)
        return {
            "question_type": _clean(question_row.get("question_type")),
            "handling_rule": _clean(question_row.get("handling_rule")),
            "recommended_computation": _clean(question_row.get("recommended_computation")),
            "question_type_structural_role": _clean(question_row.get("question_type_structural_role")),
            "source_structure_classification": classification,
            "source_structure_basis": "missing_register",
            "source_structure_confidence": "low",
            "source_structure_review_required": True,
            "source_structure_source": _source_structure_source(question_row),
            "source_structure_fields_joined": False,
        }, "none", "missing_register"

    register = _normalize_keys(register)
    for column in ["question_id", "var_code", "var_name", "matched_codebook_var", "matched_source_column", "parent_var_name", "question_name"]:
        normalized_column = f"{column}_normalized"
        if column in register.columns and normalized_column not in register.columns:
            register[normalized_column] = register[column].map(_normalized_join_key)
    source = _clean(question_row.get("source") or question_row.get("source_family"))
    wave = _clean(question_row.get("canonical_wave") or question_row.get("wave"))
    question_id = _clean(question_row.get("question_id"))
    var_code = _clean(question_row.get("var_code") or question_row.get("var_name"))
    var_name = _clean(question_row.get("var_name") or question_row.get("matched_codebook_var") or question_row.get("question_name"))
    question_id_key = _normalized_question_id(question_id)

    source_mask = register["source"].eq(source) if "source" in register.columns else pd.Series([False] * len(register), index=register.index)
    wave_mask = pd.Series([True] * len(register), index=register.index)
    for wave_col in ["canonical_wave", "wave"]:
        if wave_col in register.columns and wave:
            wave_mask &= register[wave_col].eq(wave) | register[wave_col].eq(_clean(question_row.get("wave")))

    candidates: list[tuple[str, str, pd.DataFrame]] = []
    if question_id and "question_id" in register.columns:
        df = register.loc[source_mask & wave_mask & register["question_id"].eq(question_id)]
        candidates.append(("source+wave+question_id", "exact", df))
    if question_id_key and "question_id_normalized" in register.columns:
        df = register.loc[source_mask & wave_mask & register["question_id_normalized"].eq(question_id_key)]
        candidates.append(("source+wave+question_id_normalized", "exact", df))
    if var_code and "var_code" in register.columns:
        df = register.loc[source_mask & wave_mask & register["var_code"].eq(var_code)]
        candidates.append(("source+wave+var_code", "exact", df))
    if var_code and "var_code_normalized" in register.columns:
        df = register.loc[source_mask & wave_mask & register["var_code_normalized"].eq(_normalized_join_key(var_code))]
        candidates.append(("source+wave+var_code_normalized", "exact", df))
    if var_name and "var_name" in register.columns:
        df = register.loc[source_mask & wave_mask & register["var_name"].eq(var_name)]
        candidates.append(("source+wave+var_name", "exact", df))
    if var_name and "var_name_normalized" in register.columns:
        df = register.loc[source_mask & wave_mask & register["var_name_normalized"].eq(_normalized_join_key(var_name))]
        candidates.append(("source+wave+var_name_normalized", "exact", df))
    if question_id and "question_id" in register.columns:
        scoped = register.loc[source_mask & register["question_id"].eq(question_id)]
        if len(scoped) == 1:
            candidates.append(("source+question_id", "unique", scoped))
    if question_id_key and "question_id_normalized" in register.columns:
        scoped = register.loc[source_mask & register["question_id_normalized"].eq(question_id_key)]
        if len(scoped) == 1:
            candidates.append(("source+question_id_normalized", "unique", scoped))
    if var_code and "var_code" in register.columns:
        scoped = register.loc[source_mask & register["var_code"].eq(var_code)]
        if len(scoped) == 1:
            candidates.append(("source+var_code", "unique", scoped))
    if var_code and "var_code_normalized" in register.columns:
        scoped = register.loc[source_mask & register["var_code_normalized"].eq(_normalized_join_key(var_code))]
        if len(scoped) == 1:
            candidates.append(("source+var_code_normalized", "unique", scoped))
    if var_name and "var_name" in register.columns:
        scoped = register.loc[source_mask & register["var_name"].eq(var_name)]
        if len(scoped) == 1:
            candidates.append(("source+var_name", "unique", scoped))
    if var_name and "var_name_normalized" in register.columns:
        scoped = register.loc[source_mask & register["var_name_normalized"].eq(_normalized_join_key(var_name))]
        if len(scoped) == 1:
            candidates.append(("source+var_name_normalized", "unique", scoped))
    if "global_universal" in register.columns and "global_unique" in register.columns and var_code:
        scoped = register.loc[register["global_universal"].map(_to_bool, na_action="ignore") & register["global_unique"].map(_to_bool, na_action="ignore") & register["var_code"].eq(var_code)]
        if len(scoped) == 1:
            candidates.append(("global_unique", "manual", scoped))

    chosen_key = "source_structure_register"
    join_confidence = "manual"
    chosen = pd.DataFrame()
    for key, confidence, frame in candidates:
        if len(frame) == 1:
            chosen_key = key
            join_confidence = confidence
            chosen = frame.iloc[[0]].copy()
            break
        if len(frame) > 1 and chosen.empty:
            chosen_key = key
            join_confidence = "ambiguous"
            chosen = frame.copy()

    if chosen.empty:
        classification = derive_source_structure_classification(question_row)
        return {
            "question_type": _clean(question_row.get("question_type")) or "unknown",
            "handling_rule": _clean(question_row.get("handling_rule")) or "unknown",
            "recommended_computation": _clean(question_row.get("recommended_computation")) or "unknown",
            "question_type_structural_role": _clean(question_row.get("question_type_structural_role")),
            "source_structure_classification": classification,
            "source_structure_basis": "derived_from_question_type_taxonomy",
            "source_structure_confidence": "low",
            "source_structure_review_required": True,
            "source_structure_source": _source_structure_source(question_row),
            "source_structure_fields_joined": False,
        }, chosen_key, "missing"

    row = chosen.iloc[0].to_dict()
    classification = _clean(row.get("source_structure_classification")) or derive_source_structure_classification({**question_row, **row})
    review_required = source_structure_review_required({**question_row, **row}, classification)
    source_structure_basis = chosen_key
    source_structure_confidence = _join_confidence_to_source_structure_confidence(join_confidence)
    return {
        "question_type": _clean(row.get("question_type")) or _clean(question_row.get("question_type")) or "unknown",
        "handling_rule": _clean(row.get("handling_rule")) or _clean(question_row.get("handling_rule")) or "unknown",
        "recommended_computation": _clean(row.get("recommended_computation")) or _clean(question_row.get("recommended_computation")) or "unknown",
        "question_type_structural_role": _clean(row.get("question_type_structural_role")) or _clean(question_row.get("question_type_structural_role")) or "",
        "source_structure_classification": classification or "unknown",
        "source_structure_basis": source_structure_basis,
        "source_structure_confidence": source_structure_confidence,
        "source_structure_review_required": review_required,
        "source_structure_source": _source_structure_source(row) if _clean(row.get("source_structure_source")) else _source_structure_source(question_row),
        "source_structure_fields_joined": True,
    }, chosen_key, join_confidence


def build_source_structure_population_audit(question_rows: pd.DataFrame, register: pd.DataFrame) -> pd.DataFrame:
    if question_rows.empty:
        return pd.DataFrame(columns=[
            "source",
            "wave",
            "canonical_wave",
            "question_id",
            "var_code",
            "question_text",
            "question_type",
            "handling_rule",
            "recommended_computation",
            "question_type_structural_role",
            "source_structure_classification",
            "source_structure_basis",
            "source_structure_confidence",
            "source_structure_source",
            "source_structure_join_key",
            "source_structure_join_confidence",
            "source_structure_fields_joined",
            "source_structure_review_required",
            "semantic_role",
            "allowed_as_v551_relation_evidence",
            "review_required",
            "manual_override_used",
            "high_risk_blocked_due_to_missing_structure",
            "disallowed_reason",
        ])
    rows: list[dict[str, Any]] = []
    for record in question_rows.to_dict(orient="records"):
        matched, join_key, join_confidence = match_source_structure_row(record, register)
        row = {
            "source": _clean(record.get("source") or record.get("source_family")),
            "wave": _clean(record.get("wave")),
            "canonical_wave": _clean(record.get("canonical_wave")),
            "question_id": _clean(record.get("question_id")),
            "var_code": _clean(record.get("var_code") or record.get("var_name")),
            "question_text": _clean(record.get("question_text")),
            "question_type": matched["question_type"],
            "handling_rule": matched["handling_rule"],
            "recommended_computation": matched["recommended_computation"],
            "question_type_structural_role": matched["question_type_structural_role"],
            "source_structure_classification": matched["source_structure_classification"],
            "source_structure_basis": matched["source_structure_basis"],
            "source_structure_confidence": matched["source_structure_confidence"],
            "source_structure_source": matched["source_structure_source"],
            "source_structure_join_key": join_key,
            "source_structure_join_confidence": join_confidence,
            "source_structure_fields_joined": matched["source_structure_fields_joined"],
            "source_structure_review_required": matched["source_structure_review_required"],
            "semantic_role": _clean(record.get("semantic_role")),
            "allowed_as_v551_relation_evidence": _to_bool(record.get("allowed_as_v551_relation_evidence"), False),
            "review_required": _to_bool(record.get("review_required"), False) or matched["source_structure_review_required"],
            "manual_override_used": _to_bool(record.get("manual_override_used"), False),
            "high_risk_blocked_due_to_missing_structure": bool(
                matched["source_structure_fields_joined"] is False or matched["source_structure_classification"] in {"unknown", ""}
            ),
            "disallowed_reason": _clean(record.get("disallowed_reason")),
        }
        rows.append(row)
    return pd.DataFrame(rows)


def write_source_structure_population_audit(audit: pd.DataFrame, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    audit.to_csv(output_path, index=False)
    return output_path
