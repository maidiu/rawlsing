#!/usr/bin/env python3
"""Run source-structure audits and publish a portable CLOSED_35 audit binding.

Semantic classification remains owned by the existing survey_structure_audit backend.
This wrapper owns only source/wave identity ingress, execution-path portability,
content hashes, and exact CLOSED_35 publication completeness.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_source_wave_identity import (
    SourceWaveIdentity,
    SourceWaveIdentityError,
    closed_35_identities,
    resolve_source_wave_identity,
)

DDM_ROOT = ROOT / "data" / "ddm_build_copy"
MANIFEST_IN = DDM_ROOT / "manifests" / "file_accounting_manifest.csv"
VALIDATION_MANIFEST_OUT = DDM_ROOT / "manifests" / "source_structure_validation_manifest.csv"
VALIDATION_REPORT_OUT = DDM_ROOT / "manifests" / "source_structure_validation_report.yaml"
PROBLEM_FILES_OUT = DDM_ROOT / "manifests" / "source_structure_problem_files.csv"
TAXONOMY_OUT = DDM_ROOT / "manifests" / "question_type_taxonomy.yaml"
AUDIT_BINDING_OUT = DDM_ROOT / "manifests" / "source_structure_audit_binding_35wave_v1.json"
AUDIT_DIR = DDM_ROOT / "reports" / "source_structure_audits"
CODEBOOK_DIR = ROOT / "data" / "FINAL CODEBOOKS" / "FINAL FINAL CODEBOOKS"

AUDIT_BINDING_SCHEMA = "source_structure_audit_binding_35wave_v1"
READY_BINDING_STATUS = "READY_HASH_BOUND"

# Filenames are compatibility locators only. Governed production membership comes
# exclusively from ddm_source_wave_identity.
CODEBOOK_FILENAME_BY_WAVE_UID = {
    "wv_arab_barometer_i_v1": "Arab Barometer Wave 1 codebook.csv",
    "wv_arab_barometer_ii_v1": "Arab Barometer Wave 2 codebook.csv",
    "wv_arab_barometer_v_v1": "Arab Barometer Wave 5 codebook.csv",
    "wv_arab_barometer_viii_v1": "Arab Barometer Wave 8 codebook.csv",
    "wv_afrobarometer_r1_v1": "Afrobarometer Round 1 codebook.csv",
    "wv_afrobarometer_r5_v1": "Afrobarometer Round 5 codebook.csv",
    "wv_afrobarometer_r9_v1": "Afrobarometer Round 9 codebook.csv",
    "wv_asian_barometer_w1_v1": "Asian Barometer Wave 1 codebook.csv",
    "wv_asian_barometer_w4_v1": "Asian Barometer Wave 4 codebook.csv",
    "wv_asian_barometer_w5_v1": "Asian Barometer Wave 5 codebook.csv",
    "wv_asian_barometer_w6_v1": "Asian Barometer Wave 6 codebook.csv",
    "wv_south_asia_w1_v1": "South Asia Wave 1 codebook.csv",
    "wv_south_asia_w2_v1": "South Asia Wave 2 codebook.csv",
    "wv_latinobarometro_1995_v1": "Latinobarometro 1995 codebook.csv",
    "wv_latinobarometro_2011_v1": "Latinobarometro 2011 codebook.csv",
    "wv_latinobarometro_2024_v1": "Latinobarometro 2024 codebook.csv",
    "wv_evs_1981_v1": "EVS Wave 1 codebook 1981.csv",
    "wv_evs_1990_v1": "EVS Wave 2 codebook 1990.csv",
    "wv_evs_1999_v1": "EVS Wave 3 codebook 1999.csv",
    "wv_evs_2008_v1": "EVS Wave 4 codebook 2008.csv",
    "wv_evs_2017_v1": "EVS Wave 5 codebook 2017.csv",
    "wv_wvs_w1_v1": "World Values Survey Wave 1 codebook.csv",
    "wv_wvs_w4_v1": "World Values Survey Wave 4 codebook.csv",
    "wv_wvs_w7_v1": "World Values Survey Wave 7 codebook.csv",
    "wv_gss_1972_v1": "GSS1972-codebook.csv",
    "wv_gss_1973_v1": "GSS1973-codebook.csv",
    "wv_gss_1984_v1": "GSS1984-codebook.csv",
    "wv_gss_1993_v1": "GSS1993-codebook.csv",
    "wv_gss_2002_v1": "GSS2002-codebook.csv",
    "wv_gss_2010_v1": "GSS2010-codebook.csv",
    "wv_gss_2016_v1": "GSS2016-codebook.csv",
    "wv_gss_2024_v1": "GSS2024-codebook.csv",
    "wv_lits_2006_v1": "LiTS-I-codebook.csv",
    "wv_lits_ii_v1": "LiTS-II-codebook.csv",
    "wv_lits_iii_v1": "LiTS-III-codebook.csv",
    "wv_lits_iv_v1": "LiTS-IV-codebook.csv",
}


def _load_audit_backend():
    try:
        from data.final_codebooks.survey_structure_audit import build_wave_audit, write_audit_outputs
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "SOURCE_STRUCTURE_AUDIT_BACKEND_MISSING: restore "
            "data/final_codebooks/survey_structure_audit.py"
        ) from exc
    return build_wave_audit, write_audit_outputs


def _clean(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _truthy(value: Any) -> bool:
    return _clean(value).lower() in {"1", "true", "yes", "y"}


def _slugify(value: str) -> str:
    slug = "".join(ch if ch.isalnum() else "_" for ch in value).strip("_")
    while "__" in slug:
        slug = slug.replace("__", "_")
    return slug or "unnamed"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _repo_relative(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError as exc:
        raise RuntimeError(f"NONPORTABLE_GENERATED_AUDIT_PATH:{resolved}") from exc


def resolve_ingress_identity(source: Any, wave: Any) -> SourceWaveIdentity | None:
    """Resolve only through the W01 kernel; unresolved historical objects stay nonproduction."""
    try:
        return resolve_source_wave_identity(source, wave)
    except SourceWaveIdentityError:
        return None


def codebook_path_for(identity: SourceWaveIdentity | None) -> Path | None:
    if identity is None:
        return None
    filename = CODEBOOK_FILENAME_BY_WAVE_UID.get(identity.wave_uid, "")
    return (CODEBOOK_DIR / filename) if filename else None


def load_manifest_rows() -> list[dict[str, Any]]:
    csv.field_size_limit(sys.maxsize)
    with MANIFEST_IN.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_prior_validation_context() -> dict[str, dict[str, Any]]:
    """Preserve legacy validation labels as compatibility provenance."""
    if not VALIDATION_MANIFEST_OUT.exists():
        return {}
    with VALIDATION_MANIFEST_OUT.open(encoding="utf-8", newline="") as f:
        return {
            _clean(row.get("dataset_id")): row
            for row in csv.DictReader(f)
            if _clean(row.get("dataset_id"))
        }


def build_taxonomy() -> list[dict[str, Any]]:
    # Semantic taxonomy unchanged from the pre-SWID validator.
    return [
        {"question_kind": "single_choice", "structural_role": "answer",
         "default_handling": "Compute one distribution over labeled response options; keep don't know and refusal as meaningful categories when present.",
         "recommended_computation": "Distribution, conditional splits, branch comparisons, and driver-mapped cloud summaries.",
         "do_not_do": "Do not flatten into a binary unless the codebook and source structure are explicitly binary."},
        {"question_kind": "multi_select", "structural_role": "stem",
         "default_handling": "Keep the child columns separate; compute option prevalence and co-occurrence instead of forcing one category.",
         "recommended_computation": "Per-option prevalence, option bundles, co-selection patterns, branch clouds.",
         "do_not_do": "Do not collapse to one nominal answer unless the source file itself is already one-hot encoded and the codebook says so."},
        {"question_kind": "matrix", "structural_role": "stem",
         "default_handling": "Treat each child row as its own question and keep row-level distributions intact.",
         "recommended_computation": "Row-by-row distributions, within-matrix contrast, row clusters, row-level driver clouds.",
         "do_not_do": "Do not average rows together unless the survey design explicitly defines a scale index."},
        {"question_kind": "split_block", "structural_role": "stem",
         "default_handling": "Treat each child block separately and preserve the split logic.",
         "recommended_computation": "Parallel branch summaries, split-block comparisons, and block-specific clouds.",
         "do_not_do": "Do not merge the children back into one pseudo-question unless the codebook and source match exactly."},
        {"question_kind": "open_text", "structural_role": "answer",
         "default_handling": "Do not force numeric scoring; preserve text for later NLP or manual coding.",
         "recommended_computation": "Text extraction, topic coding, and curated qualitative review.",
         "do_not_do": "Do not invent numeric ordinals or scale scores."},
        {"question_kind": "stem", "structural_role": "stem",
         "default_handling": "Treat as a parent item that organizes child columns but is not itself a scored answer.",
         "recommended_computation": "Structural grouping only.",
         "do_not_do": "Do not analyze as a substantive opinion response."},
        {"question_kind": "derived_or_reference", "structural_role": "metadata",
         "default_handling": "Use as context, provenance, or conditioning only.",
         "recommended_computation": "Conditioning, joins, sample definition, or source metadata.",
         "do_not_do": "Do not count as a substantive attitude or opinion item."},
        {"question_kind": "source_extra", "structural_role": "source_extra",
         "default_handling": "Flag as a source-side column that is not represented directly in the codebook row set.",
         "recommended_computation": "Manual review and source-to-codebook reconciliation.",
         "do_not_do": "Do not silently drop if the source file still meaningfully contributes to the structure."},
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
        "manual_review_count": sum(_clean(r.get("needs_manual_review")) == "yes" for r in rows),
        "source_structure_disagrees_count": sum(_clean(r.get("source_structure_disagrees_with_codebook")) == "yes" for r in rows),
        "codebook_stale_count": sum(_clean(r.get("codebook_options_stale")) == "yes" for r in rows),
        "codebook_trustworthy_count": sum(_clean(r.get("codebook_options_trustworthy")) == "yes" for r in rows),
        "source_present_count": sum(_clean(r.get("source_present")) == "yes" for r in rows),
    }
    conclusions = []
    for kind, text in [
        ("multi_select", "multi-select families require child-column handling"),
        ("matrix", "matrix families require row-level handling"),
        ("split_block", "split blocks require child-block handling"),
        ("single_choice", "single-choice answers can be scored directly"),
        ("open_text", "open-text answers require text handling, not numeric scoring"),
    ]:
        if kind_counts.get(kind):
            conclusions.append(text)
    summary["high_level_conclusion"] = "; ".join(conclusions)
    return summary, sorted(set(flagged_names))


def _identity_payload(identity: SourceWaveIdentity | None, raw_source: str, raw_wave: str) -> dict[str, Any]:
    if identity is None:
        return {
            "raw_source": raw_source,
            "raw_wave": raw_wave,
            "canonical_display_source": "",
            "canonical_display_wave": "",
            "source_family_uid": "",
            "wave_uid": "",
            "governance_state": "",
            "closed_35_member": False,
            "canonical_intended": False,
        }
    return {
        "raw_source": raw_source,
        "raw_wave": raw_wave,
        "canonical_display_source": identity.canonical_display_source,
        "canonical_display_wave": identity.canonical_display_wave,
        "source_family_uid": identity.source_family_uid,
        "wave_uid": identity.wave_uid,
        "governance_state": identity.governance_state,
        "closed_35_member": identity.closed_35_member,
        "canonical_intended": identity.production_authorized,
    }


def _write_blocked_audit_yaml(path: Path, base: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(
            {
                "dataset_id": base.get("dataset_id", ""),
                "source_family": base.get("source_family", ""),
                "wave": base.get("wave", ""),
                "canonical_wave": base.get("canonical_wave", ""),
                "source_family_uid": base.get("source_family_uid", ""),
                "wave_uid": base.get("wave_uid", ""),
                "status": base.get("audit_status", ""),
                "read_status": base.get("raw_read_status", ""),
                "error": base.get("audit_error", ""),
                "raw_path": base.get("raw_path", ""),
                "codebook_path": base.get("codebook_path", ""),
            },
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )


def audit_one(row: dict[str, Any], prior: dict[str, Any] | None = None) -> dict[str, Any]:
    dataset_id = _clean(row.get("dataset_id"))
    raw_source = _clean(row.get("source_family") or row.get("source"))
    raw_wave = _clean(row.get("wave"))
    identity = resolve_ingress_identity(raw_source, raw_wave)
    identity_payload = _identity_payload(identity, raw_source, raw_wave)
    prior = prior or {}

    raw_path = Path(_clean(row.get("path")))
    codebook_path = codebook_path_for(identity)
    read_status = _clean(row.get("read_status"))
    raw_exists = raw_path.exists()
    codebook_exists = bool(codebook_path and codebook_path.exists())

    base = {
        "dataset_id": dataset_id,
        "source_family": _clean(prior.get("source_family")) or identity_payload["canonical_display_source"] or raw_source,
        "wave": _clean(prior.get("wave")) or raw_wave,
        "canonical_wave": _clean(prior.get("canonical_wave")) or identity_payload["canonical_display_wave"],
        **identity_payload,
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
        "audit_sha256": "",
        "audit_yaml_sha256": "",
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
        _write_blocked_audit_yaml(out_yaml, base)
        return base

    try:
        build_wave_audit, write_audit_outputs = _load_audit_backend()
        audit_rows, summary = build_wave_audit(raw_path, str(codebook_path) if codebook_path else "")
    except Exception as exc:  # pragma: no cover
        base["audit_status"] = "blocked_raw_unreadable" if "readstat" in repr(exc).lower() else "blocked_audit_error"
        base["audit_error"] = repr(exc)
        _write_blocked_audit_yaml(out_yaml, base)
        return base

    write_audit_outputs(audit_rows, summary, out_csv, out_yaml)
    compact, problem_fields = summarize_rows(audit_rows)
    base.update({
        "audit_status": "green" if compact["manual_review_count"] == 0 and compact["source_structure_disagrees_count"] == 0 else "partial_review",
        "audit_csv": _repo_relative(out_csv),
        "audit_yaml": _repo_relative(out_yaml),
        "audit_sha256": _sha256(out_csv),
        "audit_yaml_sha256": _sha256(out_yaml) if out_yaml.exists() else "",
        "kind_counts": json.dumps(compact["kind_counts"], sort_keys=True),
        "source_match_counts": json.dumps(compact["source_match_counts"], sort_keys=True),
        "manual_review_count": compact["manual_review_count"],
        "source_structure_disagrees_count": compact["source_structure_disagrees_count"],
        "codebook_stale_count": compact["codebook_stale_count"],
        "codebook_trustworthy_count": compact["codebook_trustworthy_count"],
        "source_present_count": compact["source_present_count"],
        "problem_fields": "|".join(problem_fields[:40]),
        "high_level_conclusion": compact["high_level_conclusion"],
    })
    if not codebook_exists:
        if identity is not None and identity.production_authorized:
            base["audit_status"] = "partial_missing_codebook"
        elif base["audit_status"] == "green":
            base["audit_status"] = "raw_only_no_codebook"
    return base


def expected_closed_35_wave_uids() -> set[str]:
    return {identity.wave_uid for identity in closed_35_identities()}


def build_audit_binding(validation_rows: list[dict[str, Any]]) -> dict[str, Any]:
    expected = expected_closed_35_wave_uids()
    governed_rows = [row for row in validation_rows if _truthy(row.get("closed_35_member"))]
    artifacts: list[dict[str, Any]] = []
    blockers: list[str] = []

    for row in governed_rows:
        wave_uid = _clean(row.get("wave_uid"))
        audit_rel = _clean(row.get("audit_csv"))
        audit_hash = _clean(row.get("audit_sha256"))
        if not wave_uid or not audit_rel or not audit_hash:
            blockers.append(f"unbound:{_clean(row.get('dataset_id'))}:{wave_uid or 'NO_UID'}")
            continue
        if Path(audit_rel).is_absolute():
            blockers.append(f"absolute_audit_path:{_clean(row.get('dataset_id'))}")
            continue
        artifacts.append({
            "dataset_id": _clean(row.get("dataset_id")),
            "raw_source": _clean(row.get("raw_source")),
            "raw_wave": _clean(row.get("raw_wave")),
            "canonical_display_source": _clean(row.get("canonical_display_source")),
            "canonical_display_wave": _clean(row.get("canonical_display_wave")),
            "source_family_uid": _clean(row.get("source_family_uid")),
            "wave_uid": wave_uid,
            "governance_state": _clean(row.get("governance_state")),
            "closed_35_member": True,
            "audit_file": Path(audit_rel).name,
            "audit_sha256": audit_hash,
            "legacy_raw_path_provenance": _clean(row.get("raw_path")),
            "legacy_codebook_path_provenance": _clean(row.get("codebook_path")),
        })

    observed = {artifact["wave_uid"] for artifact in artifacts}
    counts = Counter(artifact["wave_uid"] for artifact in artifacts)
    duplicates = sorted(uid for uid, count in counts.items() if count != 1)
    missing = sorted(expected - observed)
    unexpected = sorted(observed - expected)
    if len(artifacts) != 35:
        blockers.append(f"artifact_count:{len(artifacts)}")
    if duplicates:
        blockers.append("duplicate_wave_uids:" + ",".join(duplicates))
    if missing:
        blockers.append("missing_wave_uids:" + ",".join(missing))
    if unexpected:
        blockers.append("unexpected_wave_uids:" + ",".join(unexpected))

    status = READY_BINDING_STATUS if not blockers and observed == expected else "BLOCKED_INCOMPLETE_OR_UNBOUND"
    return {
        "schema": AUDIT_BINDING_SCHEMA,
        "status": status,
        "authority_scope": "CLOSED_35",
        "expected_wave_uid_count": 35,
        "expected_wave_uids": sorted(expected),
        "observed_wave_uid_count": len(observed),
        "observed_wave_uids": sorted(observed),
        "audit_root_contract": {
            "default_repo_relative_root": "data/ddm_build_copy/reports/source_structure_audits",
            "environment_override": "DDM_SOURCE_STRUCTURE_AUDIT_ROOT",
            "absolute_paths_forbidden_in_binding": True,
            "legacy_absolute_paths_are_provenance_only": True,
        },
        "artifacts": sorted(artifacts, key=lambda x: (x["wave_uid"], x["dataset_id"])),
        "blockers": blockers,
    }


def write_validation_manifest(validation_rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "dataset_id", "source_family", "wave", "canonical_wave", "canonical_intended",
        "raw_source", "raw_wave", "canonical_display_source", "canonical_display_wave",
        "source_family_uid", "wave_uid", "governance_state", "closed_35_member",
        "raw_path", "codebook_path", "raw_read_status", "raw_exists", "codebook_exists",
        "raw_row_count", "raw_column_count", "audit_status", "audit_csv", "audit_yaml",
        "audit_sha256", "audit_yaml_sha256", "kind_counts", "source_match_counts",
        "manual_review_count", "source_structure_disagrees_count", "codebook_stale_count",
        "codebook_trustworthy_count", "source_present_count", "problem_fields",
        "high_level_conclusion", "audit_error",
    ]
    with VALIDATION_MANIFEST_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in validation_rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def main() -> int:
    manifest_rows = load_manifest_rows()
    raw_rows = [row for row in manifest_rows if _clean(row.get("artifact_kind")) == "raw_data"]
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    prior_context = load_prior_validation_context()
    validation_rows = [
        audit_one(row, prior_context.get(_clean(row.get("dataset_id")), {}))
        for row in raw_rows
    ]
    write_validation_manifest(validation_rows)

    binding = build_audit_binding(validation_rows)
    AUDIT_BINDING_OUT.write_text(
        json.dumps(binding, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    problem_rows = [row for row in validation_rows if row["audit_status"] != "green"]
    with PROBLEM_FILES_OUT.open("w", encoding="utf-8", newline="") as f:
        fields = ["dataset_id", "source_family", "wave", "canonical_wave", "wave_uid",
                  "closed_35_member", "audit_status", "raw_read_status", "codebook_exists",
                  "problem_fields", "audit_error"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in problem_rows:
            writer.writerow({key: row.get(key, "") for key in fields})

    taxonomy = {
        "schema": "source_structure_question_type_taxonomy_v1",
        "global_policy": {
            "special_responses": "Preserve don't know, refusal, and similar responses as meaningful analytical signals unless a specific question type absolutely requires a different treatment.",
            "raw_vs_codebook": "A raw file can be structurally readable but still disagree with the codebook, which means the question type and compute method must be decided from the source shape, not only the codebook text.",
            "compute_rule": "No overnight batch should run until the portable hash-bound CLOSED_35 audit binding is exact-scope complete.",
        },
        "question_types": build_taxonomy(),
    }
    TAXONOMY_OUT.write_text(yaml.safe_dump(taxonomy, sort_keys=False, allow_unicode=True), encoding="utf-8")

    report = {
        "status": "green_source_structure_validation_written" if binding["status"] == READY_BINDING_STATUS else "blocked_source_structure_validation_not_publishable",
        "raw_files_checked": len(raw_rows),
        "green_files": sum(row["audit_status"] == "green" for row in validation_rows),
        "partial_files": sum(row["audit_status"].startswith(("partial", "raw_only")) for row in validation_rows),
        "blocked_files": sum(row["audit_status"].startswith("blocked") for row in validation_rows),
        "closed_35_expected_wave_uid_count": 35,
        "closed_35_observed_wave_uid_count": binding["observed_wave_uid_count"],
        "closed_35_binding_status": binding["status"],
        "binding": _repo_relative(AUDIT_BINDING_OUT),
        "manifest": _repo_relative(VALIDATION_MANIFEST_OUT),
        "problem_files": _repo_relative(PROBLEM_FILES_OUT),
        "taxonomy": _repo_relative(TAXONOMY_OUT),
    }
    VALIDATION_REPORT_OUT.write_text(yaml.safe_dump(report, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(yaml.safe_dump(report, sort_keys=False, allow_unicode=True).strip())
    return 0 if binding["status"] == READY_BINDING_STATUS else 1


if __name__ == "__main__":
    raise SystemExit(main())
