#!/usr/bin/env python3
"""Rawlsing Layer-1 35-wave pre-V553 contract audit harness.

This harness is deliberately additive.  It imports the currently installed
``run_20var_allwaves_v550_552j_smoke.py`` implementation and uses its stage
compilers, readiness gates, shared-substrate route, and no-DB V550J contract.
It replaces only the old fixed 20-variable/36-wave scope selection with:

* the frozen 35-wave active scope;
* morphology-aware, deterministic variable selection;
* whole-country execution with bounded variables;
* exact current J-family inclusion when a registry is available;
* nonrespondent-only artifact collection and privacy scanning;
* point-to-point field-presence and preservation evidence.

The program never treats a zero exit code as semantic success.  It delegates
stage-specific readiness gates to the installed runner and adds audit gates of
its own.  Execution is opt-in via ``--execute``; plan mode is the default.
"""
from __future__ import annotations

import argparse
import csv
import dataclasses
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence
from zipfile import ZipFile

try:
    import pandas as pd
except Exception as exc:  # pragma: no cover - import gate
    raise SystemExit(f"pandas is required: {exc}")

ACTIVE_SCOPES: tuple[tuple[str, str], ...] = (
    ("Afrobarometer", "R1"), ("Afrobarometer", "R5"), ("Afrobarometer", "R9"),
    ("Arab Barometer", "I"), ("Arab Barometer", "II"), ("Arab Barometer", "V"), ("Arab Barometer", "VIII"),
    ("Asian Barometer", "W1"), ("Asian Barometer", "W4"), ("Asian Barometer", "W5"),
    ("EVS", "1981"), ("EVS", "1990"), ("EVS", "1999"), ("EVS", "2008"), ("EVS", "2017"),
    ("GSS", "1972"), ("GSS", "1973"), ("GSS", "1984"), ("GSS", "1993"),
    ("GSS", "2002"), ("GSS", "2010"), ("GSS", "2016"), ("GSS", "2024"),
    ("Latinobarómetro", "1995"), ("Latinobarómetro", "2011"), ("Latinobarómetro", "2024"),
    ("LiTS", "2006"), ("LiTS", "II"), ("LiTS", "III"), ("LiTS", "IV"),
    ("South Asia", "W1"), ("South Asia", "W2"),
    ("WVS", "W1"), ("WVS", "W4"), ("WVS", "W7"),
)

DEFAULT_COUNTRIES: dict[str, dict[str, str]] = {
    "Afrobarometer": {"R1": "BF", "R5": "SL", "R9": "SZ"},
    "Arab Barometer": {"I": "LY", "II": "JO", "V": "QA", "VIII": "LB"},
    "Asian Barometer": {"W1": "PH", "W4": "SG", "W5": "SG"},
    "EVS": {"1981": "BE", "1990": "MT", "1999": "IS", "2008": "IS", "2017": "NL"},
    "GSS": {"1972": "US", "1973": "US", "1984": "US", "1993": "US", "2002": "US", "2010": "US", "2016": "US", "2024": "US"},
    "Latinobarómetro": {"1995": "BR", "2011": "GT", "2024": "GT"},
    "LiTS": {"2006": "BY", "II": "SE", "III": "AL", "IV": "MA"},
    "South Asia": {"W1": "IN", "W2": "BD"},
    "WVS": {"W1": "SE", "W4": "DZ", "W7": "RS"},
}

# Morphologies are intentionally overlapping.  The selector is a deterministic
# greedy set-cover, not a one-row/one-category classifier.
MORPHOLOGY_TAGS: tuple[str, ...] = (
    "directional_relation",
    "nondirectional_relation",
    "structural_context",
    "position_coordinate",
    "binary",
    "ordinal",
    "nominal",
    "scalar",
    "multiselect_or_repeated",
    "derived_or_recoded",
    "routed_or_conditional",
    "country_or_split_variant",
    "missingness_semantics",
    "pressure_linkage_candidate",
    "review_or_authority_gap",
)

PRIVACY_PATH_PATTERNS = (
    re.compile(r"v550_shared_respondent_substrate.*\.(?:parquet|csv)$", re.I),
    re.compile(r"respondent.*(?:membership|response|substrate).*\.(?:parquet|csv)$", re.I),
    re.compile(r"raw.*(?:respondent|response).*\.(?:parquet|csv)$", re.I),
)
PRIVACY_COLUMN_PATTERNS = (
    re.compile(r"^(?:respondent|case|person|record|interview)(?:_?id|_?key|_?number)$", re.I),
    re.compile(r"^(?:raw_)?response_value$", re.I),
)

SECRET_PATTERNS = (
    (re.compile(r"(postgres(?:ql)?://)([^@\s/]+)@", re.I), r"\1<redacted>@"),
    (re.compile(r"(?im)^(DATABASE_URL\s*=\s*).+$"), r"\1<redacted>"),
    (re.compile(r"(?i)(password\s*[=:]\s*)[^\s,;]+"), r"\1<redacted>"),
)

DEEP_CATALOG_RE = re.compile(r"Deep_Question_Node_Catalog.*\.csv$", re.I)
ACTIVE_SCOPE_RE = re.compile(r"Rawlsing_J_Family_Active_35_Wave_Scope.*\.csv$", re.I)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def strip_accents(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def norm(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", strip_accents(value).lower())


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "t", "yes", "y", "on"}


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json_sha256(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        keys: list[str] = []
        seen: set[str] = set()
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.add(key)
                    keys.append(key)
        fieldnames = keys
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: _csv_value(row.get(k, "")) for k in fieldnames})


def _csv_value(value: Any) -> Any:
    if isinstance(value, (list, tuple, set, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return value


def find_member(names: Iterable[str], pattern: re.Pattern[str]) -> str:
    matches = [name for name in names if pattern.search(Path(name).name)]
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one member matching {pattern.pattern!r}; found {len(matches)}: {matches[:10]}")
    return matches[0]


def load_active_scope_from_zip(handoff_zip: Path) -> pd.DataFrame:
    with ZipFile(handoff_zip) as zf:
        member = find_member(zf.namelist(), ACTIVE_SCOPE_RE)
        df = pd.read_csv(io.BytesIO(zf.read(member)), dtype=str).fillna("")
    observed = [(str(r.source_family), str(r.wave)) for r in df.itertuples(index=False)]
    if tuple(observed) != ACTIVE_SCOPES:
        raise RuntimeError("active scope file does not match the frozen 35-wave order")
    return df


def load_deep_catalogs_from_zip(handoff_zip: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    with ZipFile(handoff_zip) as zf:
        members = sorted(name for name in zf.namelist() if DEEP_CATALOG_RE.search(Path(name).name))
        if len(members) != 9:
            raise RuntimeError(f"expected nine source-local deep catalogs; found {len(members)}")
        for member in members:
            frame = pd.read_csv(io.BytesIO(zf.read(member)), low_memory=False)
            frame["_catalog_member"] = member
            frames.append(frame)
    merged = pd.concat(frames, ignore_index=True, sort=False)
    required = {"question_implementation_id", "source_family", "wave", "source_variable_code", "exact_question_text"}
    missing = sorted(required - set(merged.columns))
    if missing:
        raise RuntimeError(f"deep catalogs missing required columns: {missing}")
    merged["source_family"] = merged["source_family"].astype(str)
    merged["wave"] = merged["wave"].astype(str)
    active_keys = {(norm(f), norm(w)) for f, w in ACTIVE_SCOPES}
    merged["_active"] = [
        (norm(f), norm(w)) in active_keys
        for f, w in zip(merged["source_family"], merged["wave"])
    ]
    return merged.loc[merged["_active"]].copy()


def normalize_role(row: Mapping[str, Any]) -> str:
    return "|".join(
        str(row.get(key, "") or "").lower()
        for key in ("semantic_lane", "semantic_role", "semantic_subrole", "semantic_tags", "evidence_lane")
    )


def morphology_tags(row: Mapping[str, Any]) -> set[str]:
    tags: set[str] = set()
    role = normalize_role(row)
    topology = str(row.get("response_topology", "") or "").lower()
    measure = str(row.get("measure", "") or "").lower()
    variant = str(row.get("implementation_variant_class", "") or "").lower()
    routing = str(row.get("routing_signal_status", "") or "").lower()
    horizon = str(row.get("horizon_affordance", "") or "").lower()
    binding = str(row.get("response_binding_status", "") or "").lower()
    directional = truthy(row.get("current_directional_atom_eligible")) or str(row.get("directional_certification_status", "")).upper() == "CERTIFIED"

    if "relation" in role and directional:
        tags.add("directional_relation")
    if "relation" in role and not directional:
        tags.add("nondirectional_relation")
    if "structural" in role or "structural" in horizon:
        tags.add("structural_context")
    if "position" in role or str(row.get("position_conditioning", "")).lower() == "yes":
        tags.add("position_coordinate")
    if topology.startswith("binary") or topology == "forced_contrast":
        tags.add("binary")
    if "ordinal" in topology or measure == "ordinal" or topology in {"ranked_choice", "ranking_or_multiselect"}:
        tags.add("ordinal")
    if "nominal" in topology or measure == "nominal":
        tags.add("nominal")
    if "scalar" in topology or measure in {"scale", "ratio"}:
        tags.add("scalar")
    if "multiselect" in topology or "repeated" in variant or str(row.get("parent_group_id", "") or "").strip():
        tags.add("multiselect_or_repeated")
    if "derived" in role or "recoded" in role or "derived" in variant:
        tags.add("derived_or_recoded")
    if (("routing" in routing and "no_" not in routing) or "conditional" in variant or "split" in variant):
        tags.add("routed_or_conditional")
    if any(token in variant for token in ("country", "national", "split", "merged_multi_country")):
        tags.add("country_or_split_variant")
    if any(truthy(row.get(key)) for key in ("has_dk", "has_refusal", "has_no_answer", "has_iap", "has_skipped", "has_not_asked", "has_inapplicable")):
        tags.add("missingness_semantics")
    if "pressure" in str(row.get("semantic_tags", "") or "").lower() or any(token in horizon for token in ("relation", "directional", "structural", "topology")):
        tags.add("pressure_linkage_candidate")
    if truthy(row.get("manual_review_required")) or "blocked" in binding or "gap" in binding or "review" in role:
        tags.add("review_or_authority_gap")
    return tags


def eligible_for_selection(row: Mapping[str, Any]) -> bool:
    code = str(row.get("source_variable_code", "") or "").strip()
    if not code:
        return False
    role = normalize_role(row)
    if "administrative" in role or re.search(r"(?:^|\|)admin(?:\||$)", role):
        return False
    if str(row.get("response_topology", "") or "").lower() == "administrative":
        return False
    if str(row.get("source_text_status", "") or "").upper() in {"MISSING", "SOURCE_TEXT_MISSING"}:
        return False
    return True


def row_quality_score(row: Mapping[str, Any]) -> float:
    score = 0.0
    if str(row.get("response_binding_status", "") or "").lower() == "bound":
        score += 5.0
    if str(row.get("authority_status", "") or "").lower() in {"source_reviewed", "accepted", "certified"}:
        score += 3.0
    if str(row.get("deep_review_status", "") or "").upper() not in {"", "NOT_STARTED", "UNREVIEWED"}:
        score += 2.0
    if str(row.get("directional_certification_status", "") or "").upper() == "CERTIFIED":
        score += 2.0
    if str(row.get("exact_question_text", "") or "").strip():
        score += 1.0
    if str(row.get("response_contract_hashes", "") or "").strip():
        score += 1.0
    if truthy(row.get("manual_review_required")):
        score -= 1.0  # retain through explicit morphology quota, not accidental preference
    return score


def parse_scope(value: str) -> tuple[str, str, str]:
    parts = [p.strip() for p in value.split("|")]
    if len(parts) not in {2, 3} or not parts[0] or not parts[1]:
        raise argparse.ArgumentTypeError("scope must be Family|Wave or Family|Wave|Country")
    family, wave = parts[0], parts[1]
    if (family, wave) not in ACTIVE_SCOPES:
        raise argparse.ArgumentTypeError(f"scope is not active: {family}|{wave}")
    country = parts[2] if len(parts) == 3 else DEFAULT_COUNTRIES[family][wave]
    return family, wave, country


def default_scope_rows() -> list[dict[str, str]]:
    return [
        {"source_family": family, "wave": wave, "country_code": DEFAULT_COUNTRIES[family][wave]}
        for family, wave in ACTIVE_SCOPES
    ]


def select_variables_for_scope(
    catalog: pd.DataFrame,
    family: str,
    wave: str,
    *,
    min_vars: int,
    target_vars: int,
    max_vars: int,
    available_var_keys: set[str] | None = None,
    registry_family_groups: Sequence[Sequence[str]] = (),
) -> tuple[list[str], list[dict[str, Any]], dict[str, Any]]:
    scope = catalog[(catalog["source_family"].map(norm) == norm(family)) & (catalog["wave"].map(norm) == norm(wave))].copy()
    if scope.empty:
        raise RuntimeError(f"no catalog rows for {family} {wave}")
    rows: list[dict[str, Any]] = []
    seen_codes: set[str] = set()
    for raw in scope.to_dict(orient="records"):
        raw = {key: ("" if pd.isna(value) else value) for key, value in raw.items()}
        if not eligible_for_selection(raw):
            continue
        code = str(raw.get("source_variable_code", "")).strip()
        key = norm(code)
        if not key or key in seen_codes:
            continue
        if available_var_keys is not None and key not in available_var_keys:
            continue
        seen_codes.add(key)
        raw["_tags"] = morphology_tags(raw)
        raw["_quality"] = row_quality_score(raw)
        raw["_code"] = code
        rows.append(raw)
    if not rows:
        raise RuntimeError(f"no eligible variables for {family} {wave}")

    by_key = {norm(row["_code"]): row for row in rows}
    selected: list[str] = []
    reasons: dict[str, set[str]] = defaultdict(set)

    # Include one real J-family group first so V550J has a meaningful joint
    # configuration. Choose the group with the best catalog coverage and tag spread.
    group_candidates: list[tuple[tuple[int, int, float, str], list[str]]] = []
    for group in registry_family_groups:
        present = [by_key[norm(code)]["_code"] for code in group if norm(code) in by_key]
        present = list(dict.fromkeys(present))
        if len(present) < 2:
            continue
        tag_union = set().union(*(by_key[norm(code)]["_tags"] for code in present))
        quality = sum(float(by_key[norm(code)]["_quality"]) for code in present)
        group_candidates.append(((-len(tag_union), -min(len(present), 8), -quality, "|".join(sorted(present))), present))
    if group_candidates:
        _, chosen = min(group_candidates, key=lambda x: x[0])
        for code in chosen[: min(8, max_vars)]:
            if code not in selected:
                selected.append(code)
                reasons[code].add("joint_family_seed")

    uncovered = set(MORPHOLOGY_TAGS)
    for code in selected:
        uncovered -= set(by_key[norm(code)]["_tags"])

    # Greedy deterministic set cover with quality and conceptual diversity.
    used_concepts: set[str] = set()
    used_contracts: set[str] = set()
    while len(selected) < target_vars:
        candidates = []
        for row in rows:
            code = row["_code"]
            if code in selected:
                continue
            tags = set(row["_tags"])
            new_tags = tags & uncovered
            concept = str(row.get("question_concept_id", "") or "")
            contract = str(row.get("response_contract_hashes", "") or "")
            diversity = int(bool(concept and concept not in used_concepts)) + int(bool(contract and contract not in used_contracts))
            rank = (
                -len(new_tags),
                -diversity,
                -float(row["_quality"]),
                str(row.get("question_implementation_id", "")),
                code,
            )
            candidates.append((rank, row, new_tags))
        if not candidates:
            break
        _, chosen, new_tags = min(candidates, key=lambda x: x[0])
        code = chosen["_code"]
        selected.append(code)
        reasons[code].update(new_tags or {"diversity_fill"})
        uncovered -= set(chosen["_tags"])
        concept = str(chosen.get("question_concept_id", "") or "")
        contract = str(chosen.get("response_contract_hashes", "") or "")
        if concept:
            used_concepts.add(concept)
        if contract:
            used_contracts.add(contract)
        if not uncovered and len(selected) >= min_vars:
            break

    # Fill to minimum with highest-quality distinct rows.
    if len(selected) < min_vars:
        for row in sorted(rows, key=lambda r: (-float(r["_quality"]), str(r.get("question_implementation_id", "")), r["_code"])):
            if row["_code"] in selected:
                continue
            selected.append(row["_code"])
            reasons[row["_code"]].add("minimum_fill")
            if len(selected) >= min_vars:
                break

    selected = selected[:max_vars]
    detail_rows: list[dict[str, Any]] = []
    for order, code in enumerate(selected, start=1):
        row = by_key[norm(code)]
        detail_rows.append({
            "source_family": family,
            "wave": wave,
            "selection_order": order,
            "source_variable_code": code,
            "question_implementation_id": row.get("question_implementation_id", ""),
            "question_concept_id": row.get("question_concept_id", ""),
            "question_text": row.get("exact_question_text", ""),
            "response_topology": row.get("response_topology", ""),
            "semantic_role": row.get("semantic_role", ""),
            "semantic_subrole": row.get("semantic_subrole", ""),
            "response_binding_status": row.get("response_binding_status", ""),
            "directional_certification_status": row.get("directional_certification_status", ""),
            "morphology_tags": sorted(row["_tags"]),
            "selection_reasons": sorted(reasons[code]),
            "quality_score": row["_quality"],
            "catalog_member": row.get("_catalog_member", ""),
        })
    coverage = Counter(tag for row in detail_rows for tag in row["morphology_tags"])
    summary = {
        "source_family": family,
        "wave": wave,
        "eligible_variable_count": len(rows),
        "selected_variable_count": len(selected),
        "covered_morphologies": sorted(k for k, v in coverage.items() if v),
        "missing_morphologies": sorted(set(MORPHOLOGY_TAGS) - set(coverage)),
        "morphology_counts": dict(sorted(coverage.items())),
        "selection_hash": canonical_json_sha256(selected),
        "joint_family_seed_used": any("joint_family_seed" in reasons[c] for c in selected),
    }
    return selected, detail_rows, summary


def dynamic_import(path: Path, module_name: str = "rawlsing_current_smoke") -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def find_current_runner(repo_root: Path, explicit: Path | None = None) -> Path:
    if explicit:
        path = explicit if explicit.is_absolute() else repo_root / explicit
        if not path.exists():
            raise FileNotFoundError(path)
        return path
    matches = list(repo_root.glob("**/run_20var_allwaves_v550_552j_smoke.py"))
    # Prefer the runtime reproducibility copy.
    matches.sort(key=lambda p: ("runtime_reproducibility_code" not in str(p), len(str(p))))
    if not matches:
        raise FileNotFoundError("current all-wave runner not found")
    return matches[0]


def load_registry_groups(base: Any, config: Any, family: str, wave: str) -> list[list[str]]:
    try:
        authority = base.resolve_joint_authority(config, family, wave)
        if not authority.get("applicable"):
            return []
        payload = base._load_yaml(Path(authority["registry_path"]))
        groups = base._registry_var_codes(payload, family, wave)
        return [list(values) for _, values in sorted(groups.items())]
    except Exception:
        return []


def available_registry_variables(base: Any, config: Any, family: str, wave: str) -> dict[str, str]:
    """Return normalized variable key -> authority role from the live DB."""
    import psycopg2
    from dotenv import load_dotenv

    load_dotenv(config.env_file)
    db_url = config.db_url or os.environ.get("DATABASE_URL", "")
    if not db_url:
        raise RuntimeError("DATABASE_URL is required for execution")
    qsm_rel = base._validate_relation_identifier(config.qsm_relation, "qsm_relation")
    registry_rel = base._validate_relation_identifier(config.canonical_registry_relation, "canonical_registry_relation")
    source_keys = sorted({base._norm(value) for value in base._source_aliases(family)})
    wave_keys = sorted({base._norm(value) for value in base._wave_aliases(family, wave)})
    sql_norm = base._sql_normalized
    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""WITH mapped_questions AS (
                       SELECT DISTINCT {sql_norm('var_code')} AS normalized_var_key
                       FROM {qsm_rel}
                       WHERE {sql_norm('source')} = ANY(%s)
                         AND {sql_norm('wave')} = ANY(%s)
                     )
                     SELECT cr.canonical_var_code, COALESCE(cr.authority_semantic_role, '')
                     FROM {registry_rel} cr
                     JOIN mapped_questions mq
                       ON mq.normalized_var_key = {sql_norm('cr.canonical_var_code')}
                     WHERE {sql_norm('cr.canonical_source')} = ANY(%s)
                       AND {sql_norm('cr.canonical_wave')} = ANY(%s)
                     ORDER BY cr.canonical_var_code""",
                (source_keys, wave_keys, source_keys, wave_keys),
            )
            return {norm(code): str(role or "") for code, role in cur.fetchall() if norm(code)}


def install_dynamic_v550_limit(base: Any) -> None:
    """Replace only the fixed ``--limit-questions 20`` call with filter size."""
    original_invoke = base._invoke_run

    def run_v550_shard(
        run_id: str,
        shard_id: str,
        family: str,
        wave: str,
        country: str,
        filter_path: str,
        output_root: str,
        registry_path: str | None = None,
        config: Any = None,
    ) -> dict[str, Any]:
        config = config or base.DEFAULT_CONFIG
        payload = json.loads(Path(filter_path).read_text(encoding="utf-8"))
        selected = list(dict.fromkeys(payload.get("question_ids") or payload.get("var_codes") or []))
        if not selected:
            raise RuntimeError("empty question filter")
        cmd = [
            sys.executable,
            base._abs("data/ddm_build_copy/build_determinicity_wave_shard_v550.py", config),
            "--run-id", run_id,
            "--shard-id", shard_id,
            "--source", family,
            "--wave", wave,
            "--canonical-wave", wave,
            "--output-root", output_root,
            "--question-filter-file", filter_path,
            "--limit-questions", str(len(selected)),
            "--env-file", str(config.env_file),
            "--first-pass-authority-dir", str(config.first_pass_authority_dir),
            "--semantic-authority-dir", str(config.semantic_authority_dir),
            "--position-conditioning-authority-dir", str(config.position_conditioning_authority_dir),
            "--directionality-authority-dir", str(config.directionality_authority_dir),
            "--v550-prepared-substrate-mode", "country",
            "--finalize-source", "memory",
            "--no-write-csv",
        ]
        if registry_path:
            cmd.extend([
                "--shared-respondent-substrate-mode", "write",
                "--joint-configuration-registry-path", registry_path,
            ])
        if country:
            cmd.extend(["--country", country])
        if config.db_url:
            cmd.extend(["--db-url", config.db_url])
        if config.response_option_map:
            cmd.extend(["--response-option-map", str(config.response_option_map)])
        if config.readiness_mode == "full":
            cmd.append("--full-readiness")
        elif config.readiness_mode == "launch":
            cmd.append("--allow-launch-ready-fallback")
        else:
            raise ValueError(f"unsupported readiness_mode:{config.readiness_mode}")
        return original_invoke(cmd, timeout_sec=3600, config=config)

    base.run_v550_shard = run_v550_shard


def build_config(base: Any, args: argparse.Namespace, runtime_root: Path, git_root: Path) -> Any:
    default_registry = runtime_root / "data/ddm_build_copy/manifests/question_family_registry.yaml"
    registry_paths = tuple(Path(p).expanduser().resolve() for p in (args.joint_registry or [str(default_registry)]))
    response_map = Path(args.response_option_map).expanduser().resolve() if args.response_option_map else base._default_response_option_map(runtime_root)
    default_env = git_root / ".env" if (git_root / ".env").exists() else runtime_root / ".env"
    return base.RuntimeConfig(
        repo_root=runtime_root,
        env_file=Path(args.env_file or default_env).expanduser().resolve(),
        db_url=args.db_url,
        qsm_relation=args.qsm_relation,
        canonical_registry_relation=args.canonical_registry_relation,
        response_option_map=response_map,
        joint_registry_paths=registry_paths,
        association_lane_registry=(runtime_root / "data/ddm_registries/association_lane_registry.yaml"),
        association_threshold_profiles=(runtime_root / "data/ddm_registries/association_threshold_profiles.yaml"),
        first_pass_authority_dir=Path(args.first_pass_authority_dir or runtime_root / "data/ddm_build_copy/reports").resolve(),
        semantic_authority_dir=Path(args.semantic_authority_dir or runtime_root / "data/ddm_build_copy/reports").resolve(),
        position_conditioning_authority_dir=Path(args.position_conditioning_authority_dir or runtime_root / "data/ddm_build_copy/reports").resolve(),
        directionality_authority_dir=Path(args.directionality_authority_dir or runtime_root / "data/ddm_build_copy/directionality_authority").resolve(),
        association_mode=args.association_mode,
        joint_mode="required",
        readiness_mode=args.readiness_mode,
        diagnostic_continue=True,
    )


def scope_slug(family: str, wave: str, country: str) -> str:
    return f"{norm(family)}_{norm(wave)}_{norm(country)}"


def write_filter(path: Path, selected: Sequence[str]) -> None:
    write_json(path, {"question_ids": list(selected), "var_codes": list(selected)})


def redact_text(text: str) -> str:
    for pattern, replacement in SECRET_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def copy_nonrespondent_artifacts(source_root: Path, destination: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    inventory: list[dict[str, Any]] = []
    privacy_findings: list[dict[str, Any]] = []
    if not source_root.exists():
        return inventory, privacy_findings
    for path in sorted(source_root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(source_root)
        rel_text = rel.as_posix()
        forbidden_path = next((p.pattern for p in PRIVACY_PATH_PATTERNS if p.search(path.name) or p.search(rel_text)), "")
        if forbidden_path:
            privacy_findings.append({"path": rel_text, "finding": "forbidden_path", "rule": forbidden_path})
            continue
        # Parquet files are aggregate by default, but inspect columns for obvious
        # respondent-level identifiers before packaging.
        forbidden_columns: list[str] = []
        if path.suffix.lower() == ".parquet":
            try:
                import pyarrow.parquet as pq
                columns = pq.ParquetFile(path).schema.names
                forbidden_columns = [c for c in columns if any(p.search(c) for p in PRIVACY_COLUMN_PATTERNS)]
            except Exception as exc:
                privacy_findings.append({"path": rel_text, "finding": "parquet_schema_unreadable", "rule": str(exc)})
                continue
        if forbidden_columns:
            privacy_findings.append({"path": rel_text, "finding": "forbidden_columns", "rule": forbidden_columns})
            continue
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix.lower() in {".txt", ".log", ".md", ".json", ".yaml", ".yml", ".csv"} and path.stat().st_size <= 32 * 1024 * 1024:
            try:
                text = path.read_text(encoding="utf-8")
                target.write_text(redact_text(text), encoding="utf-8")
            except UnicodeDecodeError:
                shutil.copy2(path, target)
        else:
            shutil.copy2(path, target)
        inventory.append({
            "relative_path": rel_text,
            "size_bytes": target.stat().st_size,
            "sha256": sha256_file(target),
        })
    return inventory, privacy_findings


def discover_artifact_fields(output_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(output_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".parquet", ".csv", ".json"}:
            continue
        rel = path.relative_to(output_root).as_posix()
        stage = next((part.lower() for part in path.parts if re.fullmatch(r"v55[0-9]j?", part.lower())), "")
        try:
            if path.suffix.lower() == ".parquet":
                import pyarrow.parquet as pq
                pf = pq.ParquetFile(path)
                for index, name in enumerate(pf.schema.names):
                    rows.append({"stage": stage, "artifact": rel, "field": name, "field_order": index, "format": "parquet"})
            elif path.suffix.lower() == ".csv":
                with path.open(newline="", encoding="utf-8-sig") as handle:
                    header = next(csv.reader(handle), [])
                for index, name in enumerate(header):
                    rows.append({"stage": stage, "artifact": rel, "field": name, "field_order": index, "format": "csv"})
            else:
                payload = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(payload, dict):
                    for index, name in enumerate(sorted(payload)):
                        rows.append({"stage": stage, "artifact": rel, "field": name, "field_order": index, "format": "json_top_level"})
        except Exception as exc:
            rows.append({"stage": stage, "artifact": rel, "field": "", "field_order": -1, "format": "ERROR", "error": str(exc)})
    return rows


def build_basic_conservation_checks(field_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_stage: dict[str, set[str]] = defaultdict(set)
    for row in field_rows:
        by_stage[str(row.get("stage", ""))].add(str(row.get("field", "")))
    checks = [
        ("v550j", "pattern_id", "v551j", {"pattern_id", "source_v550j_pattern_id"}),
        ("v551", "empirical_distribution_id", "v551j", {"empirical_distribution_id", "v551_empirical_distribution_id"}),
        ("v551j", "packet_id", "v552j", {"packet_id", "source_v551j_packet_id"}),
        ("v551j", "certification_status", "v552j", {"certification_status", "source_v551j_certification_status"}),
        ("v552", "pressure_score", "v552j", {"pressure_score", "source_v552_pressure_score"}),
        ("v552", "pressure_measurement_hash", "v552j", {"pressure_measurement_hash", "source_v552_pressure_measurement_hash"}),
        ("v552", "empirical_distribution_id", "v552j", {"empirical_distribution_id", "source_v552_empirical_distribution_id"}),
    ]
    results: list[dict[str, Any]] = []
    for source_stage, source_field, dest_stage, acceptable in checks:
        source_present = source_field in by_stage.get(source_stage, set())
        matched = sorted(acceptable & by_stage.get(dest_stage, set()))
        results.append({
            "source_stage": source_stage,
            "source_field": source_field,
            "source_present": source_present,
            "destination_stage": dest_stage,
            "acceptable_destination_fields": sorted(acceptable),
            "matched_destination_fields": matched,
            "status": "PRESENT" if source_present and matched else ("SOURCE_ABSENT" if not source_present else "DESTINATION_ABSENT"),
        })
    return results


def package_manifest(root: Path) -> list[dict[str, Any]]:
    return [
        {"relative_path": p.relative_to(root).as_posix(), "size_bytes": p.stat().st_size, "sha256": sha256_file(p)}
        for p in sorted(root.rglob("*")) if p.is_file()
    ]


def run_plan(args: argparse.Namespace) -> int:
    handoff_zip = Path(args.handoff_zip).expanduser().resolve()
    if not handoff_zip.exists():
        raise FileNotFoundError(handoff_zip)
    output_root = Path(args.output_root).expanduser().resolve()
    report_root = output_root / "reports"
    filter_root = output_root / "filters"
    report_root.mkdir(parents=True, exist_ok=True)
    filter_root.mkdir(parents=True, exist_ok=True)

    active_df = load_active_scope_from_zip(handoff_zip)
    catalog = load_deep_catalogs_from_zip(handoff_zip)
    scopes = [parse_scope(value) for value in args.only_scope] if args.only_scope else [
        (row["source_family"], row["wave"], DEFAULT_COUNTRIES[row["source_family"]][row["wave"]])
        for row in active_df.to_dict(orient="records")
    ]

    base = config = None
    repo_root: Path | None = None
    runtime_root: Path | None = None
    if args.repo_root:
        repo_root = Path(args.repo_root).expanduser().resolve()
        runner_path = find_current_runner(repo_root, Path(args.current_runner) if args.current_runner else None)
        runtime_root = runner_path.parents[2]
        base = dynamic_import(runner_path)
        config = build_config(base, args, runtime_root, repo_root)

    scope_rows: list[dict[str, Any]] = []
    selection_rows: list[dict[str, Any]] = []
    morphology_rows: list[dict[str, Any]] = []
    run_plan_rows: list[dict[str, Any]] = []

    for index, (family, wave, country) in enumerate(scopes):
        available: set[str] | None = None
        groups: list[list[str]] = []
        availability_status = "catalog_only"
        if args.execute:
            if base is None or config is None:
                raise RuntimeError("--execute requires --repo-root")
            available_map = available_registry_variables(base, config, family, wave)
            available = set(available_map)
            groups = load_registry_groups(base, config, family, wave)
            availability_status = "live_registry_intersection"
        elif base is not None and config is not None:
            groups = load_registry_groups(base, config, family, wave)
            availability_status = "catalog_plus_registry_file"

        selected, details, summary = select_variables_for_scope(
            catalog,
            family,
            wave,
            min_vars=args.min_vars,
            target_vars=args.target_vars,
            max_vars=args.max_vars,
            available_var_keys=available,
            registry_family_groups=groups,
        )
        filter_path = filter_root / f"{scope_slug(family, wave, country)}.json"
        write_filter(filter_path, selected)
        for row in details:
            row["country_code"] = country
            selection_rows.append(row)
        summary["country_code"] = country
        morphology_rows.append(summary)
        scope_rows.append({
            "scope_order": index + 1,
            "source_family": family,
            "wave": wave,
            "country_code": country,
            "respondent_scope": "all_respondents_in_selected_country",
            "variable_scope": "bounded_contract_covering",
            "selected_variable_count": len(selected),
            "selection_hash": summary["selection_hash"],
            "availability_basis": availability_status,
            "filter_path": str(filter_path),
        })
        run_plan_rows.append({
            "scope_order": index + 1,
            "source_family": family,
            "wave": wave,
            "country_code": country,
            "filter_path": str(filter_path),
            "selected_variables": selected,
            "selected_variable_count": len(selected),
            "status": "PLANNED",
        })

    write_csv(report_root / "AUDIT_SCOPE_MATRIX.csv", scope_rows)
    write_csv(report_root / "AUDIT_VARIABLE_SELECTION.csv", selection_rows)
    write_csv(report_root / "AUDIT_FAMILY_COVERAGE_MATRIX.csv", [
        {"source_family": r["source_family"], "wave": r["wave"], "country_code": r["country_code"],
         "joint_family_seed_used": r["joint_family_seed_used"], "selected_variable_count": r["selected_variable_count"]}
        for r in morphology_rows
    ])
    write_json(report_root / "AUDIT_MORPHOLOGY_COVERAGE_SUMMARY.json", {
        "scope_count": len(scopes),
        "active_scope_count_expected": 35,
        "all_active_scopes_planned": len(scopes) == 35,
        "morphologies": list(MORPHOLOGY_TAGS),
        "scopes": morphology_rows,
    })
    write_json(report_root / "LAYER1_RUN_PLAN.json", {
        "schema_version": "rawlsing.layer1.run_plan.v1",
        "created_at": utc_now(),
        "handoff_zip": str(handoff_zip),
        "handoff_zip_sha256": sha256_file(handoff_zip),
        "git_root": str(repo_root or ""),
        "runtime_root": str(runtime_root or ""),
        "scope_count": len(scopes),
        "min_vars": args.min_vars,
        "target_vars": args.target_vars,
        "max_vars": args.max_vars,
        "execution_requested": bool(args.execute),
        "scopes": run_plan_rows,
    })

    if not args.execute:
        write_json(report_root / "LAYER1_STATUS.json", {
            "status": "PLAN_COMPLETE_NOT_EXECUTED",
            "scope_count": len(scopes),
            "selected_variable_count_total": sum(r["selected_variable_count"] for r in scope_rows),
        })
        manifest = package_manifest(output_root)
        write_csv(report_root / "SHA256SUMS.csv", manifest)
        return 0

    assert base is not None and config is not None and repo_root is not None and runtime_root is not None
    install_dynamic_v550_limit(base)
    execution_root = output_root / "live_outputs"
    execution_root.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    for row in run_plan_rows:
        family, wave, country = row["source_family"], row["wave"], row["country_code"]
        selected = list(row["selected_variables"])
        try:
            result = base.run_wave(
                family,
                wave,
                country,
                utc_now(),
                str(execution_root),
                row["filter_path"],
                selected,
                config,
            )
        except Exception as exc:
            result = {
                "survey_family": family,
                "wave_id": wave,
                "country": country,
                "passed": False,
                "failure_stage": "layer1_harness_exception",
                "functional_failure_reason": str(exc),
            }
        results.append(result)
        write_json(report_root / "RUN_STATUS_INCREMENTAL.json", results)

    base.write_summaries(results, str(execution_root), utc_now(), canary_only=False, preflight=None)
    write_json(report_root / "RUN_STATUS.json", results)

    package_root = output_root / "nonrespondent_package"
    inventory, privacy_findings = copy_nonrespondent_artifacts(execution_root, package_root)
    write_csv(report_root / "NONRESPONDENT_ARTIFACT_INVENTORY.csv", inventory)
    write_csv(report_root / "PRIVACY_SCAN.csv", privacy_findings, fieldnames=["path", "finding", "rule"])
    field_rows = discover_artifact_fields(package_root)
    write_csv(report_root / "ARTIFACT_FIELD_INVENTORY.csv", field_rows)
    conservation = build_basic_conservation_checks(field_rows)
    write_csv(report_root / "BASIC_POINT_TO_POINT_CONSERVATION_CHECKS.csv", conservation)

    status = {
        "status": "EXECUTION_COMPLETE" if all(r.get("passed") for r in results) else "EXECUTION_COMPLETE_WITH_FAILURES",
        "scope_count": len(results),
        "passed_scope_count": sum(bool(r.get("passed")) for r in results),
        "failed_scope_count": sum(not bool(r.get("passed")) for r in results),
        "privacy_finding_count": len(privacy_findings),
        "basic_conservation_failure_count": sum(r["status"] != "PRESENT" for r in conservation),
    }
    write_json(report_root / "LAYER1_STATUS.json", status)
    manifest = package_manifest(output_root)
    write_csv(report_root / "SHA256SUMS.csv", manifest)
    return 0 if status["failed_scope_count"] == 0 and not privacy_findings else 1


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff-zip", required=True, help="Cumulative handoff ZIP containing active scope and nine deep catalogs")
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--repo-root", default="", help="Exact current Rawlsing repository; required for --execute")
    parser.add_argument("--current-runner", default="", help="Optional path relative to repo root")
    parser.add_argument("--only-scope", action="append", default=[], help="Family|Wave or Family|Wave|Country")
    parser.add_argument("--min-vars", type=int, default=20)
    parser.add_argument("--target-vars", type=int, default=36)
    parser.add_argument("--max-vars", type=int, default=50)
    parser.add_argument("--execute", action="store_true", help="Actually run the live fused pipeline; default is plan only")
    parser.add_argument("--env-file", default="")
    parser.add_argument("--db-url", default="")
    parser.add_argument("--qsm-relation", default=os.environ.get("DDM_QSM_RELATION", "question_structural_mapping"))
    parser.add_argument("--canonical-registry-relation", default=os.environ.get("DDM_CANONICAL_REGISTRY_RELATION", "canonical_question_registry"))
    parser.add_argument("--response-option-map", default="")
    parser.add_argument("--joint-registry", action="append", default=[])
    parser.add_argument("--association-mode", choices=("off", "funnel_only", "candidate_trace", "publishable"), default="off")
    parser.add_argument("--readiness-mode", choices=("full", "launch"), default="full")
    parser.add_argument("--first-pass-authority-dir", default="")
    parser.add_argument("--semantic-authority-dir", default="")
    parser.add_argument("--position-conditioning-authority-dir", default="")
    parser.add_argument("--directionality-authority-dir", default="")
    args = parser.parse_args(argv)
    if not (1 <= args.min_vars <= args.target_vars <= args.max_vars):
        parser.error("require 1 <= min-vars <= target-vars <= max-vars")
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        return run_plan(args)
    except Exception as exc:
        output_root = Path(args.output_root).expanduser().resolve()
        output_root.mkdir(parents=True, exist_ok=True)
        write_json(output_root / "FATAL_ERROR.json", {"status": "FAIL", "error": str(exc), "timestamp": utc_now()})
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
