#!/usr/bin/env python3
"""Build the V550 response-option normalization map."""

from __future__ import annotations

from collections import defaultdict
import hashlib
import json
import time
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_io import (
    candidate_option_columns,
    clean_text,
    confidence_from_basis,
    discover_csv_files,
    infer_context_from_path,
    infer_directionality_status,
    infer_polarity,
    infer_response_direction,
    infer_response_intensity,
    infer_response_family,
    infer_scale_direction,
    maybe_numeric,
    normalize_family,
    normalize_label,
    normalize_wave,
    parse_option_entry,
    safe_read_csv,
    split_option_text,
    is_special_label,
)
from data.ddm_build_copy.ddm_v550_family_overlay import canonical_family_key, canonical_wave_key, wave_aliases
from data.ddm_build_copy.ddm_v550_response_semantics_authority import (
    bind_governed_response_semantics_contracts,
    response_option_map_content_sha256,
)


def _row_value(row: pd.Series, *names: str) -> str:
    for name in names:
        if name in row.index:
            value = clean_text(row.get(name))
            if value:
                return value
    return ""


def _row_any(row: pd.Series, names: list[str]) -> str:
    for name in names:
        if name in row.index:
            value = clean_text(row.get(name))
            if value:
                return value
    return ""


def _wave_lookup_variants(source: str, wave: str) -> list[str]:
    family = canonical_family_key(source)
    tokens: list[str] = []
    for token in [wave, canonical_wave_key(family, wave), *wave_aliases(family, wave)]:
        cleaned = clean_text(token)
        if cleaned:
            tokens.append(cleaned)
            normalized = normalize_wave(cleaned)
            if normalized:
                tokens.append(normalized)
    out: list[str] = []
    seen: set[str] = set()
    for token in tokens:
        key = token.strip()
        if not key:
            continue
        marker = key.upper()
        if marker not in seen:
            seen.add(marker)
            out.append(key)
    return out


def _option_source_group(source_column: str, source_text: str) -> str:
    column = clean_text(source_column).lower()
    if any(token in column for token in ["dk", "dontknow", "don'tknow", "refus", "no_answer", "noanswer", "missing", "inapplicable", "iap", "special"]):
        return "special"
    if any(token in column for token in ["observed", "substantive", "response", "option", "label", "value"]):
        return "observed"
    return "unknown"


def _option_group(code: str, label: str, source_group: str) -> str:
    if source_group == "special":
        return "special"
    if is_special_label(label, code):
        return "special"
    return "substantive"


def normalize_response_code(value: object) -> str | None:
    """Return the canonical response code used by both codebooks and live rows."""
    text = clean_text(value)
    if not text:
        return None
    if text.lower() == "nan":
        return None
    num = maybe_numeric(text)
    if num is None:
        return text
    if float(num).is_integer():
        return str(int(num))
    normalized = f"{num:.12f}".rstrip("0").rstrip(".")
    return normalized


def _normalize_code(code: str) -> str:
    normalized = normalize_response_code(code)
    return normalized or ""


def _safe_int(value: str) -> int | None:
    text = clean_text(value)
    if not text:
        return None
    try:
        num = float(text)
    except Exception:
        return None


def response_semantics_contract_hash(frame: pd.DataFrame) -> str:
    """Deprecated map-level semantic-hash compatibility hook.

    A V551 response-semantics contract identity is inherited from frozen
    governed response-option authority at exact question grain.  It is never a
    digest of an arbitrary response-option-map DataFrame.  Returning blank is
    intentional: legacy global/scoped callers must not manufacture a semantic
    identity when no exact governed row-level identity is present.
    """
    return ""


def _resolve_requested_codebook_files(codebook_roots: list[Path], only_codebooks: list[str] | None) -> list[Path]:
    requested = [clean_text(item) for item in (only_codebooks or []) if clean_text(item)]
    if not requested:
        return discover_csv_files(codebook_roots)

    resolved: list[Path] = []
    missing: list[str] = []
    for item in requested:
        path = Path(item)
        if path.is_absolute() and path.exists():
            resolved.append(path)
            continue
        if path.exists():
            resolved.append(path)
            continue
        found = False
        for root in codebook_roots:
            candidate = root / path.name
            if candidate.exists():
                resolved.append(candidate)
                found = True
                break
        if not found:
            missing.append(item)
    if resolved:
        return sorted({p.resolve() for p in resolved})
    if missing:
        # Fall back to the broader scan only when none of the requested files were
        # found by direct resolution. This preserves compatibility for unusual layouts.
        files = discover_csv_files(codebook_roots)
        allowed_names = {Path(item).name for item in missing}
        return [path for path in files if path.name in allowed_names or str(path) in {str(Path(item)) for item in missing}]
    return discover_csv_files(codebook_roots)


def load_question_context_tables(
    questions_master_drivers: Path,
    questions_master_semantic: Path | None,
    question_structure_register: Path | None,
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in [questions_master_drivers, questions_master_semantic, question_structure_register]:
        if path and Path(path).exists():
            df = safe_read_csv(Path(path))
            frames.append(df)
    if not frames:
        return pd.DataFrame()
    base = frames[0].copy()
    for extra in frames[1:]:
        if extra.empty:
            continue
        merge_keys = [c for c in ["source", "wave", "var_name"] if c in base.columns and c in extra.columns]
        if merge_keys:
            extra = extra.copy()
            base = base.merge(extra, on=merge_keys, how="outer", suffixes=("", "_extra"))
            for col in extra.columns:
                if col in merge_keys or f"{col}_extra" not in base.columns:
                    continue
                base[col] = base[col].where(base[col].astype(str).str.len() > 0, base[f"{col}_extra"])
                base.drop(columns=[f"{col}_extra"], inplace=True)
    return base


def _parse_row_options(row: pd.Series) -> tuple[list[dict[str, Any]], str, list[str], bool]:
    option_cols = candidate_option_columns(pd.DataFrame([row]))
    source_columns_used: list[str] = []
    parsed = False
    opts: list[dict[str, Any]] = []
    for col in option_cols:
        val = clean_text(row.get(col))
        if not val:
            continue
        source_columns_used.append(col)
        parsed = True
        source_group = _option_source_group(col, val)
        for code, label in split_option_text(val):
            code_norm = _normalize_code(code)
            label_clean = normalize_label(label)
            special = _option_group(code_norm, label_clean, source_group) == "special"
            opts.append(
                {
                    "value_code_raw": code,
                    "value_code_normalized": code_norm,
                    "value_code_numeric": maybe_numeric(code_norm),
                    "value_label_raw": label,
                    "value_label_clean": label_clean,
                    "normalized_response_label": label_clean,
                    "option_group": "special" if special else "substantive",
                    "option_source_column": col,
                    "option_source_group": source_group,
                    "is_substantive": not special,
                    "is_missing": special,
                    "is_dk": "don't know" in label_clean.lower() or label_clean.lower() == "dk",
                    "is_refusal": "refus" in label_clean.lower(),
                    "is_no_answer": "no answer" in label_clean.lower(),
                    "is_iap": "iap" in label_clean.lower(),
                    "is_skipped": "skip" in label_clean.lower(),
                    "is_uncodeable": "uncodeable" in label_clean.lower() or "unclassifiable" in label_clean.lower(),
                    "is_not_available": "not available" in label_clean.lower(),
                    "is_not_asked": "not asked" in label_clean.lower(),
                    "is_inapplicable": "inapplicable" in label_clean.lower(),
                    "response_family": "",
                    "response_kind": "special_missing" if special else "substantive",
                    "is_ordered": False,
                    "order_index": None,
                    "order_direction": "",
                    "polarity": "none",
                    "response_direction": "",
                    "response_intensity": None,
                    "ordinal_rank": None,
                    "scale_min": None,
                    "scale_max": None,
                    "scale_direction": "",
                    "directionality_status": "unknown",
                    "measure": "",
                    "storage_type": "",
                    "format": "",
                    "option_count_declared": None,
                    "value_labels_count_declared": None,
                    "comparability_level": "distribution_only" if special else "facet_comparable",
                    "normalization_basis": f"parsed_{','.join(source_columns_used) or 'codebook'}",
                    "normalization_confidence": "high" if parsed else "low",
                    "manual_review_flag": False,
                    "manual_review_reason": "",
                    "source_column_used": ",".join(source_columns_used),
                }
            )
    return opts, ",".join(source_columns_used), [o["value_label_clean"] for o in opts], parsed


def _apply_response_directionality(options: list[dict[str, Any]], response_family: str) -> None:
    substantive = [option for option in options if not option.get("is_missing")]
    total = len(substantive)
    if total <= 0:
        for option in options:
            option["directionality_status"] = "NOT_CERTIFIED_SPECIAL" if option.get("is_missing") else "unknown"
            if option.get("is_missing"):
                option["response_direction"] = ""
                option["response_intensity"] = None
                option["ordinal_rank"] = None
                option["scale_min"] = None
                option["scale_max"] = None
                option["scale_direction"] = ""
                option["polarity"] = ""
        return
    scale_min = 1
    scale_max = total
    for rank, option in enumerate(substantive, start=1):
        label = option.get("value_label_clean") or option.get("normalized_response_label") or option.get("value_code_normalized") or ""
        status = infer_directionality_status(response_family, [label])
        if status == "unknown":
            option["response_direction"] = ""
            option["response_intensity"] = None
            option["ordinal_rank"] = None
            option["scale_min"] = None
            option["scale_max"] = None
            option["scale_direction"] = ""
            option["directionality_status"] = "unknown"
            continue
        option["ordinal_rank"] = rank
        option["scale_min"] = scale_min
        option["scale_max"] = scale_max
        option["scale_direction"] = infer_scale_direction(response_family)
        option["response_direction"] = infer_response_direction(label, response_family, rank=rank, total=total)
        option["response_intensity"] = infer_response_intensity(label, response_family, rank=rank, total=total)
        option["directionality_status"] = status
        polarity = option.get("response_direction") or ""
        option["polarity"] = polarity if polarity in {"positive", "negative", "neutral"} else "unknown"
    for option in options:
        if option.get("is_missing"):
            option["directionality_status"] = "NOT_CERTIFIED_SPECIAL"
            option["response_direction"] = ""
            option["response_intensity"] = None
            option["ordinal_rank"] = None
            option["scale_min"] = None
            option["scale_max"] = None
            option["scale_direction"] = ""
            option["polarity"] = ""


def build_response_option_map(
    *,
    codebook_roots: list[Path],
    only_codebooks: list[str] | None = None,
    questions_master_drivers: Path,
    questions_master_semantic: Path | None,
    question_structure_register: Path | None,
    question_type_taxonomy: Path | None = None,
    db_conn: Any | None = None,
    limit_questions: int | None = None,
    verbose: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    files = _resolve_requested_codebook_files(codebook_roots, only_codebooks)
    started = time.monotonic()
    if verbose:
        print(f"[V550a] resolved_codebooks={len(files)}", flush=True)
        print("[V550a] loading question context tables", flush=True)
    context = load_question_context_tables(questions_master_drivers, questions_master_semantic, question_structure_register)
    if verbose:
        print(f"[V550a +{time.monotonic() - started:0.0f}s] loaded_context_tables rows={len(context)}", flush=True)
    context_lookup: dict[tuple[str, str, str], dict[str, Any]] = {}
    if not context.empty:
        for row in context.itertuples(index=False):
            source_label = normalize_family(getattr(row, "source", getattr(row, "source_family", "")))
            source = canonical_family_key(source_label)
            wave = clean_text(getattr(row, "wave", getattr(row, "canonical_wave", "")))
            var_name = clean_text(getattr(row, "var_name", getattr(row, "question_name", getattr(row, "name", ""))))
            if source and wave and var_name:
                for wave_variant in _wave_lookup_variants(source_label, wave):
                    context_lookup[(source, wave_variant, var_name)] = row._asdict()

    rows: list[dict[str, Any]] = []
    review_rows: list[dict[str, Any]] = []
    file_summaries: list[dict[str, Any]] = []
    seen: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    if verbose:
        print(f"[V550a +{time.monotonic() - started:0.0f}s] beginning codebook scan total={len(files)}", flush=True)

    for file_index, path in enumerate(files, start=1):
        if verbose:
            elapsed = time.monotonic() - started
            print(f"[V550a +{elapsed:0.0f}s] scanning {file_index}/{len(files)} {path.name}", flush=True)
        try:
            df = safe_read_csv(path)
        except Exception as exc:
            file_summaries.append({"source_file": str(path), "status": "read_error", "error": str(exc), "rows": 0})
            if verbose:
                print(f"[V550a]   read_error: {exc}", flush=True)
            continue
        if df.empty:
            file_summaries.append({"source_file": str(path), "status": "empty", "rows": 0})
            if verbose:
                print(f"[V550a]   empty", flush=True)
            continue

        file_context = infer_context_from_path(path)
        produced = 0
        manual_reviews = 0
        row_count = len(df)
        last_progress = time.monotonic()
        rows_seen = 0
        for _, row in df.iterrows():
            rows_seen += 1
            var_name = _row_value(row, "var_name", "name")
            if not var_name:
                continue
            if limit_questions is not None and produced >= limit_questions:
                break
            question_text = _row_any(row, ["question_text", "pdf_question_text", "sav_variable_label", "label", "display_text"])
            source_label = normalize_family(_row_any(row, ["source", "source_family"]) or file_context.source_family)
            source = canonical_family_key(source_label)
            wave = clean_text(_row_any(row, ["wave", "canonical_wave"]) or file_context.wave)
            if not source_label:
                source_label = file_context.source_family
            if not source:
                source = canonical_family_key(source_label)
            if not wave:
                wave = file_context.wave
            question_id = _row_any(row, ["question_id", "item_id"]) or f"{source_label}:{wave}:{var_name}"
            context_row = {}
            for wave_variant in _wave_lookup_variants(source_label, wave):
                context_row = context_lookup.get((source, wave_variant, var_name), {})
                if context_row:
                    break
            parsed_options, source_column_used, labels, parsed = _parse_row_options(row)
            option_count_declared_raw = _row_any(row, ["value_labels_count", "option_count"])
            option_count_declared = _safe_int(option_count_declared_raw)
            storage_type = _row_any(row, ["storage_type"]) or clean_text(context_row.get("storage_type", ""))
            measure = _row_any(row, ["measure"]) or clean_text(context_row.get("measure", ""))
            response_family = infer_response_family(question_text, var_name, labels, storage_type=storage_type, measure=measure)
            if not parsed_options:
                manual_reviews += 1
                review_rows.append(
                    {
                        "source": source_label,
                        "source_family": source_label,
                        "wave": wave,
                        "canonical_wave": canonical_wave_key(source_label, wave) or wave,
                        "dataset_id": clean_text(context_row.get("dataset_id", "")),
                        "source_file": str(path),
                        "var_name": var_name,
                        "question_id": question_id,
                        "question_text": question_text,
                        "manual_review_flag": True,
                        "manual_review_reason": "no_parseable_response_options",
                        "source_column_used": "",
                        "note": clean_text(row.get("note", "")),
                    }
                )
            _apply_response_directionality(parsed_options, response_family)
            for option in parsed_options:
                option.update(
                    {
                        "run_id": "",
                        "source": source_label,
                        "source_family": source_label,
                        "wave": wave,
                        "canonical_wave": canonical_wave_key(source_label, wave) or wave,
                        "dataset_id": clean_text(context_row.get("dataset_id", "")),
                        "source_file": str(path),
                        "var_name": var_name,
                        "var_code": var_name,
                        "question_id": question_id,
                        "item_id": _row_any(row, ["item_id"]),
                        "question_text": question_text,
                        "question_text_basis": source_column_used or "codebook",
                        "response_family": response_family,
                        "measure": measure,
                        "storage_type": storage_type,
                        "format": _row_any(row, ["format"]),
                        "option_count_declared": option_count_declared,
                        "value_labels_count_declared": option_count_declared,
                        "comparability_level": "distribution_only" if option.get("is_missing") else "facet_comparable",
                        "normalization_confidence": "high" if parsed else "observed_only",
                        "manual_review_flag": False,
                        "manual_review_reason": "",
                        "driver_id": clean_text(context_row.get("driver_id", "")),
                        "driver_facet_id": clean_text(context_row.get("driver_facet_id", "")),
                        "relation_axis_id": clean_text(context_row.get("relation_axis_id", "")),
                        "target_entity_id": clean_text(context_row.get("target_entity_id", "")),
                        "mapping_status": clean_text(context_row.get("mapping_status", "")),
                        "question_type": clean_text(context_row.get("question_type", "")),
                        "handling_rule": clean_text(context_row.get("handling_rule", "")),
                        "recommended_computation": clean_text(context_row.get("recommended_computation", "")),
                        "source_structure_classification": clean_text(context_row.get("source_structure_classification", "")),
                        "source_structure_fields_joined": bool(context_row),
                        "notes": clean_text(context_row.get("notes", "")),
                    }
                )
                option["is_ordered"] = response_family in {
                    "agreement_scale",
                    "trust_scale",
                    "satisfaction_scale",
                    "importance_scale",
                    "frequency_scale",
                    "ordinal_scale",
                    "yes_no",
                    "left_right_scale",
                }
                option["order_direction"] = "ascending" if option["is_ordered"] else ""
                if option.get("polarity") in {"", "none", "unknown"}:
                    option["polarity"] = infer_polarity(response_family, labels)
                key = (source_label, wave, var_name, option["value_code_normalized"] or option["value_label_clean"])
                existing = seen.get(key)
                if existing is None or option["normalization_confidence"] >= existing.get("normalization_confidence", ""):
                    seen[key] = option
                    produced += 1
            if verbose:
                now = time.monotonic()
                if rows_seen % 100 == 0 or (now - last_progress) >= 5:
                    elapsed = now - started
                    print(
                        f"[V550a +{elapsed:0.0f}s]   {path.name}: rows_seen={rows_seen}/{row_count} "
                        f"produced={produced} manual_review={manual_reviews}",
                        flush=True,
                    )
                    last_progress = now

        file_summaries.append(
            {
                "source_file": str(path),
                "status": "ok",
                "rows": int(produced),
                "manual_review_rows": int(manual_reviews),
                "source_family": file_context.source_family,
                "wave": file_context.wave,
            }
        )
        if verbose:
            elapsed = time.monotonic() - started
            print(
                f"[V550a +{elapsed:0.0f}s] finished {path.name}: rows_seen={row_count} produced={produced} manual_review={manual_reviews}",
                flush=True,
            )

    out = pd.DataFrame(list(seen.values()))
    binding_summary = {
        "applicable_groups": 0,
        "bound_groups": 0,
        "preserved_groups": 0,
        "review_required_groups": 0,
        "unresolved_groups": 0,
    }
    if not out.empty:
        out = out.sort_values(["source", "wave", "var_name", "value_code_raw", "value_label_clean"]).reset_index(drop=True)
        out["response_semantics_status"] = "UNRESOLVED_LIVE_BUILD"
        out["response_semantics_source"] = "response_option_map_live_build"
        out["response_semantics_contract_hash"] = ""
        out, binding_summary = bind_governed_response_semantics_contracts(
            out,
            live_build=True,
        )
    content_hash = response_option_map_content_sha256(out)
    review = pd.DataFrame(review_rows)
    if not review.empty:
        review = review.drop_duplicates(subset=["source", "wave", "var_name", "question_id", "manual_review_reason"]).reset_index(drop=True)

    manifest = {
        "files_scanned": len(files),
        "files_loaded": int(sum(1 for row in file_summaries if row.get("status") == "ok")),
        "option_rows": int(len(out)),
        "manual_review_rows": int(len(review)),
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "file_summaries": file_summaries[:200],
        "warnings": [
            "Codebook-derived response options were parsed conservatively.",
            "Manual review rows are retained instead of being silently dropped.",
            "response_semantics_contract_hash is a row-level governed packet identity; whole-map content hashes are never used as V551 contract keys.",
        ],
        "response_semantics_contract_hash": "",
        "response_option_map_content_sha256": content_hash,
        "response_semantics_contract_identity_scope": "row_level_governed_packet",
        "response_semantics_contract_binding": binding_summary,
    }
    return out, review, manifest
