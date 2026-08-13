#!/usr/bin/env python3
"""Truthful 20-variable universality smoke for the explicit 36-wave scope.

Mandatory base spine for every wave:
    V550 -> V551 -> V552

Required full-chain branch for the universality acceptance run:
    V550J -> V551J -> V552J

The base spine can be diagnosed separately with ``--joint-mode auto`` or
``--joint-mode off``, but a default all-wave pass requires explicit joint-family
authority and a successful J-chain for every one of the 36 waves.

A subprocess exit code of zero is process success only.  Every stage with a
readiness artifact is checked before the wave can pass.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import random
import re
import subprocess
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, NamedTuple

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from data.ddm_build_copy.ddm_v550j_registry_contract import (
    EXECUTABLE_JOINT_REGISTRY_STATUSES,
    registry_status_is_executable,
)
from data.ddm_build_copy.ddm_v550_response_relation import (
    AUTO_RESPONSE_RELATION,
    choose_response_relation,
)

DEFAULT_JOINT_REGISTRY = REPO_ROOT / "data/ddm_build_copy/manifests/question_family_registry.yaml"
DEFAULT_RESPONSE_OPTION_MAP = REPO_ROOT / "data/ddm_build_copy/reports/V550_response_option_map.csv"
DEFAULT_RESPONSE_MAP_BUILD_INPUTS = (
    REPO_ROOT / "data/FINAL CODEBOOKS/FINAL FINAL CODEBOOKS",
    REPO_ROOT / "chatgpt_v550_readiness_addendum/codebooks/questions_master_drivers.csv",
    REPO_ROOT / "chatgpt_v550_readiness_addendum/codebooks/questions_master_semantic.csv",
    REPO_ROOT / "chatgpt_v550_readiness_addendum/manifests/question_structure_register.csv",
    REPO_ROOT / "chatgpt_v550_readiness_addendum/manifests/question_type_taxonomy.yaml",
)
DEFAULT_ASSOCIATION_LANE_REGISTRY = REPO_ROOT / "data/ddm_registries/association_lane_registry.yaml"
DEFAULT_ASSOCIATION_THRESHOLD_PROFILES = REPO_ROOT / "data/ddm_registries/association_threshold_profiles.yaml"
DEFAULT_AUTHORITY_OVERLAY_DIR = REPO_ROOT / "data/ddm_build_copy/reports"
DEFAULT_FIRST_PASS_AUTHORITY_DIR = DEFAULT_AUTHORITY_OVERLAY_DIR
DEFAULT_SEMANTIC_AUTHORITY_DIR = DEFAULT_AUTHORITY_OVERLAY_DIR
DEFAULT_POSITION_CONDITIONING_AUTHORITY_DIR = DEFAULT_AUTHORITY_OVERLAY_DIR
DEFAULT_DIRECTIONALITY_AUTHORITY_DIR = REPO_ROOT / "data/ddm_build_copy/directionality_authority"
DEFAULT_ENV_FILE = REPO_ROOT / ".env"
DEFAULT_QSM_RELATION = "question_structural_mapping"
DEFAULT_CANONICAL_REGISTRY_RELATION = "canonical_question_registry"

# Backward-compatible names used by existing tests/importers.
REGISTRY_PATH = str(DEFAULT_JOINT_REGISTRY.relative_to(REPO_ROOT))
RESPONSE_OPTION_MAP = str(DEFAULT_RESPONSE_OPTION_MAP.relative_to(REPO_ROOT))
ASSOCIATION_LANE_REGISTRY = str(DEFAULT_ASSOCIATION_LANE_REGISTRY.relative_to(REPO_ROOT))
ASSOCIATION_THRESHOLD_PROFILES = str(DEFAULT_ASSOCIATION_THRESHOLD_PROFILES.relative_to(REPO_ROOT))
ENV_FILE = str(DEFAULT_ENV_FILE.relative_to(REPO_ROOT))

FAMILY_BAND: list[tuple[str, str, str]] = [
    ("Afrobarometer", "R1", ""),
    ("Arab Barometer", "I", ""),
    ("Asian Barometer", "W1", ""),
    ("EVS", "1981", ""),
    ("GSS", "2010", "US"),
    ("Latinobarómetro", "1995", ""),
    ("LiTS", "2006", ""),
    ("South Asia", "W1", ""),
    ("WVS", "W1", ""),
]

# Deliberate allowlist.  GSS 1982, 2004, and 2014 are intentionally excluded.
ALL_WAVES: list[tuple[str, str, str]] = [
    ("Afrobarometer", "R1", ""), ("Afrobarometer", "R5", ""), ("Afrobarometer", "R9", ""),
    ("Arab Barometer", "I", ""), ("Arab Barometer", "II", ""), ("Arab Barometer", "V", ""), ("Arab Barometer", "VIII", ""),
    ("Asian Barometer", "W1", ""), ("Asian Barometer", "W4", ""), ("Asian Barometer", "W5", ""), ("Asian Barometer", "W6", ""),
    ("EVS", "1981", ""), ("EVS", "1990", ""), ("EVS", "1999", ""), ("EVS", "2008", ""), ("EVS", "2017", ""),
    ("GSS", "1972", ""), ("GSS", "1973", ""), ("GSS", "1984", ""), ("GSS", "1993", ""),
    ("GSS", "2002", ""), ("GSS", "2010", ""), ("GSS", "2016", ""), ("GSS", "2024", ""),
    ("Latinobarómetro", "1995", ""), ("Latinobarómetro", "2011", ""), ("Latinobarómetro", "2024", ""),
    ("LiTS", "2006", ""), ("LiTS", "II", ""), ("LiTS", "III", ""), ("LiTS", "IV", ""),
    ("South Asia", "W1", ""), ("South Asia", "W2", ""),
    ("WVS", "W1", ""), ("WVS", "W4", ""), ("WVS", "W7", ""),
]

EXCLUDED_GSS_WAVES = {"1982", "2004", "2014"}
CANARY_FAMILY = "GSS"
CANARY_WAVE = "2010"
CANARY_COUNTRY = "US"

COUNTRY_MAP: dict[str, dict[str, str]] = {
    "Afrobarometer": {"R1": "BF", "R5": "SL", "R9": "SZ"},
    "Arab Barometer": {"I": "LY", "II": "JO", "V": "QA", "VIII": "LB"},
    "Asian Barometer": {"W1": "PH", "W4": "SG", "W5": "SG", "W6": "ID"},
    "EVS": {"1981": "BE", "1990": "MT", "1999": "IS", "2008": "IS", "2017": "NL"},
    "GSS": {"1972": "US", "1973": "US", "1984": "US", "1993": "US", "2002": "US", "2010": "US", "2016": "US", "2024": "US"},
    "Latinobarómetro": {"1995": "BR", "2011": "GT", "2024": "GT"},
    "LiTS": {"2006": "BY", "II": "SE", "III": "AL", "IV": "MA"},
    "South Asia": {"W1": "IN", "W2": "BD"},
    "WVS": {"W1": "SE", "W4": "DZ", "W7": "RS"},
}

CATEGORIES = {
    "demographic_context": {"admin", "administrative_metadata", "demographic", "context"},
    "directional_attitudinal": {"opinion", "value", "behavior", "attitude"},
    "relation_evidence": {"relation_evidence", "relational_evidence"},
    "structural_mapped": {"substantive", "mapped"},
    "edge_ambiguous": {"blocked_unknown", "blocked_review", "uncertain"},
    "known_fragile": {"position_coordinate", "structural_context"},
}

IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)?$")


class RuntimeConfig(NamedTuple):
    repo_root: Path = REPO_ROOT
    env_file: Path = DEFAULT_ENV_FILE
    db_url: str = ""
    qsm_relation: str = DEFAULT_QSM_RELATION
    canonical_registry_relation: str = DEFAULT_CANONICAL_REGISTRY_RELATION
    response_option_map: Path | None = None
    joint_registry_paths: tuple[Path, ...] = (DEFAULT_JOINT_REGISTRY,)
    association_lane_registry: Path | None = DEFAULT_ASSOCIATION_LANE_REGISTRY
    association_threshold_profiles: Path | None = DEFAULT_ASSOCIATION_THRESHOLD_PROFILES
    first_pass_authority_dir: Path = DEFAULT_FIRST_PASS_AUTHORITY_DIR
    semantic_authority_dir: Path = DEFAULT_SEMANTIC_AUTHORITY_DIR
    position_conditioning_authority_dir: Path = DEFAULT_POSITION_CONDITIONING_AUTHORITY_DIR
    directionality_authority_dir: Path = DEFAULT_DIRECTIONALITY_AUTHORITY_DIR
    association_mode: str = "off"
    joint_mode: str = "required"
    readiness_mode: str = "full"
    diagnostic_continue: bool = False
    response_long_relation: str = AUTO_RESPONSE_RELATION


DEFAULT_CONFIG = RuntimeConfig()


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _log(message: str) -> None:
    print(f"[{_now()}] {message}", flush=True)


def _strip_accents(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def _norm(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", _strip_accents(value).lower())


def _family_wave_id(family: str, wave: str) -> str:
    return f"{_norm(family)}_{_norm(wave)}"


def _abs(path: str | Path, config: RuntimeConfig = DEFAULT_CONFIG) -> str:
    p = Path(path)
    return str(p if p.is_absolute() else config.repo_root / p)


def _response_map_build_inputs(config: RuntimeConfig) -> tuple[Path, ...]:
    """Return response-map builder inputs anchored to the active repo root."""
    root = config.repo_root
    return (
        root / "data/FINAL CODEBOOKS/FINAL FINAL CODEBOOKS",
        root / "chatgpt_v550_readiness_addendum/codebooks/questions_master_drivers.csv",
        root / "chatgpt_v550_readiness_addendum/codebooks/questions_master_semantic.csv",
        root / "chatgpt_v550_readiness_addendum/manifests/question_structure_register.csv",
        root / "chatgpt_v550_readiness_addendum/manifests/question_type_taxonomy.yaml",
    )


def _default_response_option_map(repo_root: Path) -> Path | None:
    candidate = repo_root / "data/ddm_build_copy/reports/V550_response_option_map.csv"
    return candidate.resolve() if candidate.exists() else None


def _redact(value: str) -> str:
    if "postgres" not in value:
        return value
    return re.sub(r"(postgres(?:ql)?://)([^@/]+)@", r"\1<redacted>@", value)


def _run(
    cmd: list[str],
    cwd: str | Path = REPO_ROOT,
    timeout_sec: int | None = None,
    *,
    config: RuntimeConfig = DEFAULT_CONFIG,
) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(config.repo_root)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    forbid_database_access = "--forbid-database-access" in {str(part) for part in cmd}
    if forbid_database_access:
        env.pop("DATABASE_URL", None)
    elif config.db_url:
        env["DATABASE_URL"] = config.db_url
    env["DDM_QSM_RELATION"] = config.qsm_relation
    env["DDM_CANONICAL_REGISTRY_RELATION"] = config.canonical_registry_relation
    if config.response_long_relation and config.response_long_relation.lower() != AUTO_RESPONSE_RELATION:
        env["DDM_RESPONSE_LONG_RELATION"] = config.response_long_relation
    display_cmd = " ".join(_redact(str(part)) for part in cmd)
    _log(f"  RUN: {display_cmd[:500]}")
    started = time.monotonic()
    try:
        proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout_sec)
    except subprocess.TimeoutExpired as exc:
        return {
            "exit_code": -1,
            "stdout_tail": (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": "TIMEOUT",
            "elapsed": round(time.monotonic() - started, 1),
            "command": display_cmd,
        }
    except Exception as exc:  # pragma: no cover - defensive process boundary
        return {
            "exit_code": -2,
            "stdout_tail": "",
            "stderr_tail": str(exc),
            "elapsed": round(time.monotonic() - started, 1),
            "command": display_cmd,
        }
    return {
        "exit_code": proc.returncode,
        "stdout_tail": (proc.stdout or "")[-4000:],
        "stderr_tail": (proc.stderr or "")[-4000:],
        "elapsed": round(time.monotonic() - started, 1),
        "command": display_cmd,
    }


def _invoke_run(
    cmd: list[str],
    *,
    timeout_sec: int | None,
    config: RuntimeConfig,
) -> dict[str, Any]:
    """Keep legacy monkeypatches working for the default runtime config."""
    if config == DEFAULT_CONFIG:
        return _run(cmd, timeout_sec=timeout_sec)
    return _run(cmd, timeout_sec=timeout_sec, config=config)


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    return str(value or "").strip().lower() in {"1", "true", "t", "yes", "y", "on"}


def _load_json(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return {}
    try:
        payload = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def validate_explicit_scope(waves: Iterable[tuple[str, str, str]] = ALL_WAVES) -> list[str]:
    rows = list(waves)
    issues: list[str] = []
    if len(rows) != 36:
        issues.append(f"explicit_scope_count_expected_36_actual_{len(rows)}")
    pairs = [(family, wave) for family, wave, _ in rows]
    if len(set(pairs)) != len(pairs):
        issues.append("duplicate_family_wave_in_explicit_scope")
    included_excluded = sorted(wave for family, wave in pairs if family == "GSS" and wave in EXCLUDED_GSS_WAVES)
    if included_excluded:
        issues.append("excluded_gss_waves_present:" + ",".join(included_excluded))
    expected_gss = {"1972", "1973", "1984", "1993", "2002", "2010", "2016", "2024"}
    actual_gss = {wave for family, wave in pairs if family == "GSS"}
    if actual_gss != expected_gss:
        issues.append(f"gss_scope_mismatch_expected_{sorted(expected_gss)}_actual_{sorted(actual_gss)}")
    return issues


def _validate_relation_identifier(value: str, label: str) -> str:
    if not IDENTIFIER_RE.fullmatch(value or ""):
        raise ValueError(f"invalid_{label}_identifier:{value!r}")
    return value


def _load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def inspect_database_contract(config: RuntimeConfig, db_url: str) -> dict[str, Any]:
    """Validate relation existence and the columns used by selection SQL."""
    result: dict[str, Any] = {"checked": False, "passed": False, "relations": {}, "error": ""}
    if not db_url or importlib.util.find_spec("psycopg2") is None:
        return result
    try:
        import psycopg2

        requirements = {
            "qsm_relation": (config.qsm_relation, {"source", "wave", "var_code"}),
            "canonical_registry_relation": (
                config.canonical_registry_relation,
                {"canonical_source", "canonical_wave", "canonical_var_code", "authority_semantic_role"},
            ),
        }
        with psycopg2.connect(db_url, connect_timeout=10) as conn:
            with conn.cursor() as cur:
                for label, (relation, required_columns) in requirements.items():
                    cur.execute("SELECT to_regclass(%s)::text", (relation,))
                    resolved = cur.fetchone()[0]
                    row = {"requested": relation, "resolved": resolved or "", "columns": [], "missing_columns": []}
                    if resolved:
                        cur.execute(
                            """SELECT attname
                               FROM pg_attribute
                               WHERE attrelid = to_regclass(%s)
                                 AND attnum > 0
                                 AND NOT attisdropped""",
                            (relation,),
                        )
                        columns = {str(item[0]) for item in cur.fetchall()}
                        row["columns"] = sorted(columns)
                        row["missing_columns"] = sorted(required_columns - columns)
                    result["relations"][label] = row

                cur.execute(
                    """SELECT table_schema || '.' || table_name
                       FROM information_schema.views
                       WHERE table_name IN ('v_ddm_response_long_facet_ready_authority', 'v_ddm_response_long_facet_ready')
                       ORDER BY table_schema, table_name"""
                )
                available_response_relations = {str(row[0]) for row in cur.fetchall()}
                try:
                    resolved_response_relation = choose_response_relation(
                        available_response_relations,
                        config.response_long_relation,
                    )
                    cur.execute(
                        """SELECT attname
                           FROM pg_attribute
                           WHERE attrelid = to_regclass(%s)
                             AND attnum > 0
                             AND NOT attisdropped""",
                        (resolved_response_relation,),
                    )
                    response_columns = {str(item[0]) for item in cur.fetchall()}
                    required_response_columns = {
                        "respondent_id", "source", "wave", "canonical_wave", "country_code", "var_code"
                    }
                    result["relations"]["response_long_relation"] = {
                        "requested": config.response_long_relation,
                        "resolved": resolved_response_relation,
                        "available": sorted(available_response_relations),
                        "columns": sorted(response_columns),
                        "missing_columns": sorted(required_response_columns - response_columns),
                    }
                except Exception as exc:
                    result["relations"]["response_long_relation"] = {
                        "requested": config.response_long_relation,
                        "resolved": "",
                        "available": sorted(available_response_relations),
                        "columns": [],
                        "missing_columns": [],
                        "error": str(exc),
                    }
        result["checked"] = True
        result["passed"] = all(
            row.get("resolved") and not row.get("missing_columns") and not row.get("error")
            for row in result["relations"].values()
        )
    except Exception as exc:
        result["checked"] = True
        result["error"] = str(exc)
    return result


def _connect_database_for_preflight(config: RuntimeConfig, db_url: str):
    if not db_url or importlib.util.find_spec("psycopg2") is None:
        return None
    import psycopg2

    return psycopg2.connect(db_url, connect_timeout=10)


def inspect_structural_registry_scope_coverage(
    config: RuntimeConfig,
    db_url: str,
    waves: Iterable[tuple[str, str, str]],
    selected_variables_by_scope: dict[tuple[str, str, str], list[str]] | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {"checked": False, "scopes": [], "missing_scope_count": 0, "missing_selected_relation_count": 0, "error": ""}
    conn = None
    try:
        conn = _connect_database_for_preflight(config, db_url)
        if conn is None:
            return result
        qsm_rel = _validate_relation_identifier(config.qsm_relation, "qsm_relation")
        registry_rel = _validate_relation_identifier(config.canonical_registry_relation, "canonical_registry_relation")
        with conn.cursor() as cur:
            for index, (family, wave, country) in enumerate(waves):
                country = country or COUNTRY_MAP.get(family, {}).get(wave, "")
                source_keys = sorted({_norm(value) for value in _source_aliases(family)})
                wave_keys = sorted({_norm(value) for value in _wave_aliases(family, wave)})
                selected = selected_variables_by_scope.get((family, wave, country), []) if selected_variables_by_scope else []
                selected_keys = sorted({_norm(value) for value in selected if _norm(value)})
                cur.execute(
                    f"""SELECT source, wave, COUNT(*) AS row_count, COUNT(DISTINCT var_code) AS var_count
                        FROM {qsm_rel}
                        WHERE {_sql_normalized('source')} = ANY(%s)
                          AND {_sql_normalized('wave')} = ANY(%s)
                        GROUP BY source, wave
                        ORDER BY source, wave""",
                    (source_keys, wave_keys),
                )
                qsm_rows = cur.fetchall()
                cur.execute(
                    f"""SELECT canonical_source, canonical_wave, COUNT(*) AS row_count, COUNT(DISTINCT canonical_var_code) AS var_count
                        FROM {registry_rel}
                        WHERE {_sql_normalized('canonical_source')} = ANY(%s)
                          AND {_sql_normalized('canonical_wave')} = ANY(%s)
                        GROUP BY canonical_source, canonical_wave
                        ORDER BY canonical_source, canonical_wave""",
                    (source_keys, wave_keys),
                )
                registry_rows = cur.fetchall()
                qsm_selected_overlap = 0
                registry_selected_overlap = 0
                selected_relation_eligible_count = 0
                selected_relation_missing_structural_count = 0
                if selected_keys:
                    cur.execute(
                        f"""SELECT COUNT(DISTINCT {_sql_normalized('var_code')})
                            FROM {qsm_rel}
                            WHERE {_sql_normalized('source')} = ANY(%s)
                              AND {_sql_normalized('wave')} = ANY(%s)
                              AND {_sql_normalized('var_code')} = ANY(%s)""",
                        (source_keys, wave_keys, selected_keys),
                    )
                    qsm_selected_overlap = int(cur.fetchone()[0] or 0)
                    cur.execute(
                        f"""SELECT COUNT(DISTINCT {_sql_normalized('canonical_var_code')})
                            FROM {registry_rel}
                            WHERE {_sql_normalized('canonical_source')} = ANY(%s)
                              AND {_sql_normalized('canonical_wave')} = ANY(%s)
                              AND {_sql_normalized('canonical_var_code')} = ANY(%s)""",
                        (source_keys, wave_keys, selected_keys),
                    )
                    registry_selected_overlap = int(cur.fetchone()[0] or 0)
                    cur.execute(
                        f"""WITH selected_registry AS (
                               SELECT DISTINCT {_sql_normalized('canonical_var_code')} AS normalized_var_key
                               FROM {registry_rel}
                               WHERE {_sql_normalized('canonical_source')} = ANY(%s)
                                 AND {_sql_normalized('canonical_wave')} = ANY(%s)
                                 AND {_sql_normalized('canonical_var_code')} = ANY(%s)
                                 AND COALESCE(allowed_as_v551_relation_evidence, false)
                             ),
                             selected_structural AS (
                               SELECT DISTINCT {_sql_normalized('var_code')} AS normalized_var_key
                               FROM {qsm_rel}
                               WHERE {_sql_normalized('source')} = ANY(%s)
                                 AND {_sql_normalized('wave')} = ANY(%s)
                                 AND {_sql_normalized('var_code')} = ANY(%s)
                             )
                             SELECT COUNT(*) AS eligible_count,
                                    COUNT(*) FILTER (WHERE ss.normalized_var_key IS NULL) AS missing_count
                             FROM selected_registry sr
                             LEFT JOIN selected_structural ss USING (normalized_var_key)""",
                        (source_keys, wave_keys, selected_keys, source_keys, wave_keys, selected_keys),
                    )
                    selected_relation_eligible_count, selected_relation_missing_structural_count = [int(value or 0) for value in cur.fetchone()]
                scope = {
                    "survey_family": family,
                    "wave": wave,
                    "country_code": country,
                    "selected_variable_count": len(selected),
                    "qsm_row_count": int(sum(row[2] for row in qsm_rows)),
                    "qsm_var_count": int(sum(row[3] for row in qsm_rows)),
                    "canonical_registry_row_count": int(sum(row[2] for row in registry_rows)),
                    "canonical_registry_var_count": int(sum(row[3] for row in registry_rows)),
                    "qsm_selected_overlap": qsm_selected_overlap,
                    "canonical_registry_selected_overlap": registry_selected_overlap,
                    "selected_relation_eligible_count": selected_relation_eligible_count,
                    "selected_relation_missing_structural_count": selected_relation_missing_structural_count,
                    "qsm_identifiers_present": [{"source": row[0], "wave": row[1], "rows": int(row[2]), "vars": int(row[3])} for row in qsm_rows],
                    "canonical_identifiers_present": [{"source": row[0], "wave": row[1], "rows": int(row[2]), "vars": int(row[3])} for row in registry_rows],
                }
                result["scopes"].append(scope)
        result["checked"] = True
        result["missing_scope_count"] = sum(
            1 for row in result["scopes"]
            if int(row["qsm_row_count"]) <= 0 or int(row["canonical_registry_row_count"]) <= 0
        )
        result["missing_selected_relation_count"] = sum(
            1 for row in result["scopes"]
            if int(row["selected_relation_missing_structural_count"]) > 0
        )
    except Exception as exc:
        result["checked"] = True
        result["error"] = str(exc)
    finally:
        if conn is not None:
            conn.close()
    return result


def inspect_selected_response_coverage(
    config: RuntimeConfig,
    db_url: str,
    waves: Iterable[tuple[str, str, str]],
    selected_variables_by_scope: dict[tuple[str, str, str], list[str]] | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {"checked": False, "scopes": [], "missing_selected_response_count": 0, "error": ""}
    conn = None
    try:
        conn = _connect_database_for_preflight(config, db_url)
        if conn is None:
            return result
        response_relation = (
            inspect_database_contract(config, db_url)
            .get("relations", {})
            .get("response_long_relation", {})
            .get("resolved")
            or "public.v_ddm_response_long_facet_ready"
        )
        with conn.cursor() as cur:
            for family, wave, country in waves:
                country = country or COUNTRY_MAP.get(family, {}).get(wave, "")
                selected = selected_variables_by_scope.get((family, wave, country), []) if selected_variables_by_scope else []
                selected_keys = sorted({_norm(value) for value in selected if _norm(value)})
                source_keys = sorted({_norm(value) for value in _source_aliases(family)})
                wave_keys = sorted({_norm(value) for value in _wave_aliases(family, wave)})
                selected_response_overlap = 0
                respondent_count = 0
                if selected_keys:
                    cur.execute(
                        f"""SELECT COUNT(DISTINCT respondent_id), COUNT(DISTINCT {_sql_normalized('var_code')})
                            FROM {response_relation}
                            WHERE {_sql_normalized('source')} = ANY(%s)
                              AND ({_sql_normalized('wave')} = ANY(%s) OR {_sql_normalized('canonical_wave')} = ANY(%s))
                              AND country_code = %s
                              AND {_sql_normalized('var_code')} = ANY(%s)""",
                        (source_keys, wave_keys, wave_keys, country, selected_keys),
                    )
                    respondent_count, selected_response_overlap = [int(value or 0) for value in cur.fetchone()]
                result["scopes"].append({
                    "survey_family": family,
                    "wave": wave,
                    "country_code": country,
                    "selected_variable_count": len(selected),
                    "selected_response_overlap": selected_response_overlap,
                    "respondents_with_selected_responses": respondent_count,
                })
        result["checked"] = True
        result["missing_selected_response_count"] = sum(
            1 for row in result["scopes"]
            if int(row["selected_variable_count"]) > 0 and int(row["selected_response_overlap"]) <= 0
        )
    except Exception as exc:
        result["checked"] = True
        result["error"] = str(exc)
    finally:
        if conn is not None:
            conn.close()
    return result


def summarize_overlay_authority_coverage(
    config: RuntimeConfig,
    waves: Iterable[tuple[str, str, str]] = ALL_WAVES,
) -> dict[str, Any]:
    """Resolve each governed overlay type against the requested smoke scope."""
    from data.ddm_build_copy.ddm_v550_family_overlay import load_family_overlay

    wave_rows = list(waves)
    specs = {
        "first_pass_authority": config.first_pass_authority_dir,
        "semantic_authority": config.semantic_authority_dir,
        "position_conditioning": config.position_conditioning_authority_dir,
        "directionality": config.directionality_authority_dir,
    }
    result: dict[str, Any] = {"scope_count": len(wave_rows), "types": {}}
    for overlay_type, root in specs.items():
        covered: list[dict[str, Any]] = []
        missing: list[dict[str, Any]] = []
        invalid: list[dict[str, Any]] = []
        for family, wave, _ in wave_rows:
            loaded = load_family_overlay(
                family,
                wave,
                overlay_type,
                required=True,
                search_roots=[root],
            )
            row = {
                "survey_family": family,
                "wave": wave,
                "status": loaded.status,
                "path": loaded.path,
                "row_count": int(loaded.row_count or 0),
                "message": loaded.message,
            }
            if loaded.status == "FOUND" and loaded.row_count > 0:
                covered.append(row)
            elif loaded.status == "INVALID_SCHEMA":
                invalid.append(row)
            else:
                missing.append(row)
        result["types"][overlay_type] = {
            "root": str(root),
            "covered_count": len(covered),
            "missing_count": len(missing),
            "invalid_count": len(invalid),
            "covered_scopes": covered,
            "missing_scopes": missing,
            "invalid_scopes": invalid,
        }
    return result



def run_preflight(
    config: RuntimeConfig,
    waves: Iterable[tuple[str, str, str]] = ALL_WAVES,
) -> dict[str, Any]:
    wave_rows = list(waves)
    blockers: list[str] = []
    warnings: list[str] = []
    scope_issues = validate_explicit_scope()
    blockers.extend(scope_issues)

    required_modules = ("pandas", "pyarrow", "psycopg2", "dotenv", "yaml")
    module_status = {name: importlib.util.find_spec(name) is not None for name in required_modules}
    blockers.extend(f"missing_python_module:{name}" for name, present in module_status.items() if not present)

    try:
        _validate_relation_identifier(config.qsm_relation, "qsm_relation")
        _validate_relation_identifier(config.canonical_registry_relation, "canonical_registry_relation")
    except ValueError as exc:
        blockers.append(str(exc))

    env_values = _load_env_file(config.env_file)
    db_url = config.db_url or os.environ.get("DATABASE_URL", "") or env_values.get("DATABASE_URL", "")
    if not db_url:
        blockers.append("missing_database_url")
    if not config.env_file.exists() and not config.db_url and not os.environ.get("DATABASE_URL"):
        warnings.append(f"env_file_missing:{config.env_file}")

    database_contract = inspect_database_contract(config, db_url)
    if database_contract.get("checked"):
        if database_contract.get("error"):
            blockers.append("database_contract_check_failed:" + str(database_contract["error"]))
        else:
            for label, row in database_contract.get("relations", {}).items():
                if not row.get("resolved"):
                    blockers.append(f"database_relation_missing:{label}:{row.get('requested', '')}")
                elif row.get("missing_columns"):
                    blockers.append(f"database_relation_columns_missing:{label}:" + ",".join(row["missing_columns"]))

    required_scripts = (
        "build_determinicity_wave_shard_v550.py",
        "compile_v551_relation_evidence_atoms.py",
        "compile_v552_structural_ddm.py",
        "compile_v550j_joint_response_patterns.py",
        "compile_v551j_joint_evidence_packets.py",
        "compile_v552j_runtime_safe_structural_handoff.py",
    )
    for name in required_scripts:
        path = config.repo_root / "data/ddm_build_copy" / name
        if not path.exists():
            blockers.append(f"missing_compiler:{path}")

    response_map_builder_missing: list[str] = []
    if config.response_option_map is not None and not config.response_option_map.exists():
        blockers.append(f"explicit_response_option_map_missing:{config.response_option_map}")
    if config.response_option_map is None:
        response_map_builder_missing = [str(path) for path in _response_map_build_inputs(config) if not path.exists()]
        if response_map_builder_missing:
            blockers.append("response_option_map_missing_and_builder_inputs_unavailable")
        else:
            warnings.append("response_option_map_will_be_built_from_repository_codebooks_then_reused_from_shard")

    existing_registries = [str(path) for path in config.joint_registry_paths if path.exists()]
    missing_registries = [str(path) for path in config.joint_registry_paths if not path.exists()]
    if missing_registries:
        warnings.extend(f"joint_registry_missing:{path}" for path in missing_registries)

    joint_authority_coverage = summarize_joint_authority_coverage(config, wave_rows)
    missing_joint_scopes = joint_authority_coverage["missing_scopes"]
    if config.joint_mode == "required" and missing_joint_scopes:
        blockers.append(f"joint_authority_missing_for_scopes:{len(missing_joint_scopes)}")
    elif config.joint_mode == "auto" and missing_joint_scopes:
        warnings.append(f"joint_authority_missing_for_scopes_base_only:{len(missing_joint_scopes)}")

    if config.association_mode != "off":
        for label, path in (
            ("association_lane_registry", config.association_lane_registry),
            ("association_threshold_profiles", config.association_threshold_profiles),
        ):
            if path is None or not path.exists():
                blockers.append(f"{label}_missing_for_association_mode:{path}")

    overlay_authority_coverage = summarize_overlay_authority_coverage(config, wave_rows)
    for overlay_type, detail in overlay_authority_coverage["types"].items():
        if detail["invalid_count"]:
            blockers.append(f"{overlay_type}_invalid_for_scopes:{detail['invalid_count']}")
        if detail["missing_count"]:
            blockers.append(f"{overlay_type}_missing_for_scopes:{detail['missing_count']}")

    selected_variables_by_scope: dict[tuple[str, str, str], list[str]] = {}
    selected_variable_errors: list[dict[str, str]] = []
    if db_url and module_status.get("psycopg2") and database_contract.get("passed"):
        for index, (family, wave, country) in enumerate(wave_rows):
            country = country or COUNTRY_MAP.get(family, {}).get(wave, "")
            try:
                selected_variables_by_scope[(family, wave, country)] = _select_question_variables(
                    family,
                    wave,
                    country,
                    seed=index,
                    config=config,
                )
            except Exception as exc:
                selected_variable_errors.append({
                    "survey_family": family,
                    "wave": wave,
                    "country_code": country,
                    "error": str(exc),
                })
        blockers.extend(
            f"selected_variable_selection_failed:{row['survey_family']}:{row['wave']}:{row['error']}"
            for row in selected_variable_errors
        )

    structural_registry_coverage = inspect_structural_registry_scope_coverage(
        config,
        db_url,
        wave_rows,
        selected_variables_by_scope=selected_variables_by_scope,
    )
    if structural_registry_coverage.get("error"):
        blockers.append("structural_registry_coverage_check_failed:" + str(structural_registry_coverage["error"]))
    elif structural_registry_coverage.get("checked"):
        missing_scope_rows = [
            row for row in structural_registry_coverage.get("scopes", [])
            if int(row.get("qsm_row_count", 0)) <= 0 or int(row.get("canonical_registry_row_count", 0)) <= 0
        ]
        if missing_scope_rows:
            blockers.append(f"BLOCKED_MISSING_STRUCTURAL_REGISTRY_SCOPE:{len(missing_scope_rows)}")
        missing_relation_rows = [
            row for row in structural_registry_coverage.get("scopes", [])
            if int(row.get("selected_relation_missing_structural_count", 0)) > 0
        ]
        if missing_relation_rows:
            blockers.append(f"selected_relation_eligible_variables_missing_structural_rows:{len(missing_relation_rows)}")

    selected_response_coverage = inspect_selected_response_coverage(
        config,
        db_url,
        wave_rows,
        selected_variables_by_scope=selected_variables_by_scope,
    )
    if selected_response_coverage.get("error"):
        blockers.append("selected_response_coverage_check_failed:" + str(selected_response_coverage["error"]))
    elif selected_response_coverage.get("checked"):
        missing_response_rows = [
            row for row in selected_response_coverage.get("scopes", [])
            if int(row.get("selected_variable_count", 0)) > 0 and int(row.get("selected_response_overlap", 0)) <= 0
        ]
        if missing_response_rows:
            blockers.append(f"selected_variable_response_coverage_missing:{len(missing_response_rows)}")

    return {
        "passed": not blockers,
        "blockers": blockers,
        "warnings": warnings,
        "module_status": module_status,
        "db_url_present": bool(db_url),
        "env_file": str(config.env_file),
        "qsm_relation": config.qsm_relation,
        "canonical_registry_relation": config.canonical_registry_relation,
        "response_option_map": str(config.response_option_map or ""),
        "response_map_builder_missing_inputs": response_map_builder_missing,
        "database_contract": database_contract,
        "joint_registry_paths_existing": existing_registries,
        "joint_registry_paths_missing": missing_registries,
        "joint_authority_coverage": joint_authority_coverage,
        "overlay_authority_coverage": overlay_authority_coverage,
        "selected_variable_errors": selected_variable_errors,
        "selected_variables_by_scope": [
            {
                "survey_family": family,
                "wave": wave,
                "country_code": country,
                "selected_variables": values,
            }
            for (family, wave, country), values in sorted(selected_variables_by_scope.items())
        ],
        "structural_registry_coverage": structural_registry_coverage,
        "selected_response_coverage": selected_response_coverage,
        "association_mode": config.association_mode,
        "joint_mode": config.joint_mode,
        "readiness_mode": config.readiness_mode,
        "requested_scope_count": len(wave_rows),
        "requested_scopes": [
            {
                "survey_family": family,
                "wave": wave,
                "country_code": country or COUNTRY_MAP.get(family, {}).get(wave, ""),
            }
            for family, wave, country in wave_rows
        ],
        "explicit_wave_count": len(ALL_WAVES),
    }


def _iter_quc_rows(quc_path: Path) -> Iterable[dict[str, Any]]:
    if quc_path.suffix.lower() == ".parquet":
        import pandas as pd

        return pd.read_parquet(quc_path).fillna("").to_dict(orient="records")
    with quc_path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _parquet_rows(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        return int(len(pd.read_parquet(path)))
    except Exception:
        return 0


def summarize_quc_functional_gate(quc_path: str | Path) -> dict[str, Any]:
    quc_path = Path(quc_path)
    summary: dict[str, Any] = {
        "quc_path": str(quc_path),
        "quc_exists": quc_path.exists(),
        "relation_rows": 0,
        "semantic_certified_rows": 0,
        "directionality_certified_rows": 0,
        "allowed_v551_rows": 0,
        "current_directional_atom_eligible_rows": 0,
        "passed": False,
        "failure_reason": "",
    }
    if not summary["quc_exists"]:
        summary["failure_reason"] = "missing_v550_question_use_contract"
        return summary
    for row in _iter_quc_rows(quc_path):
        if str(row.get("semantic_role", "")).strip().upper() != "RELATION_EVIDENCE":
            continue
        summary["relation_rows"] += 1
        if str(row.get("semantic_role_authority_status", "")).strip().upper() == "CERTIFIED":
            summary["semantic_certified_rows"] += 1
        if str(row.get("directionality_authority_status", "")).strip().upper() == "CERTIFIED":
            summary["directionality_certified_rows"] += 1
        if _truthy(row.get("allowed_as_v551_relation_evidence")):
            summary["allowed_v551_rows"] += 1
        if _truthy(row.get("current_directional_atom_eligible")):
            summary["current_directional_atom_eligible_rows"] += 1
    requirements = (
        ("relation_rows", "no_relation_evidence_rows"),
        ("semantic_certified_rows", "no_semantic_authority_certified_relation_rows"),
        ("directionality_certified_rows", "no_directionality_authority_certified_relation_rows"),
        ("allowed_v551_rows", "no_allowed_v551_relation_evidence_rows"),
        ("current_directional_atom_eligible_rows", "no_current_directional_atom_eligible_rows"),
    )
    for key, reason in requirements:
        if int(summary[key]) <= 0:
            summary["failure_reason"] = reason
            return summary
    summary["passed"] = True
    return summary


def summarize_v550_manifest_gate(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path)
    if not manifest_path.exists() and manifest_path.name == "manifest.json":
        fallback = manifest_path.with_name("shard_manifest.json")
        if fallback.exists():
            manifest_path = fallback
    payload = _load_json(manifest_path)
    response_option_map_row_count = int(
        payload.get("response_option_map_row_count")
        or (payload.get("rows_by_table") or {}).get("response_option_map")
        or 0
    )
    success = _truthy(payload.get("success"))
    promotable = _truthy(payload.get("promotable"))
    passed = bool(payload) and success and response_option_map_row_count > 0
    if passed:
        failure_reason = ""
    elif not payload:
        failure_reason = "missing_v550_manifest"
    elif not success:
        failure_reason = "v550_not_successful"
    elif response_option_map_row_count <= 0:
        failure_reason = "v550_response_option_map_rows_zero"
    else:
        failure_reason = "v550_not_promotable"
    return {
        "manifest_path": str(manifest_path),
        "manifest_exists": manifest_path.exists(),
        "success": success,
        "promotable": promotable,
        "response_option_map_row_count": response_option_map_row_count,
        "response_semantics_contract_hash": str(payload.get("response_semantics_contract_hash") or ""),
        "passed": passed,
        "failure_reason": failure_reason,
    }


def summarize_v551_functional_gate(path: str | Path) -> dict[str, Any]:
    payload = _load_json(path)
    atom_rows = int(payload.get("atom_rows") or 0)
    return {
        "manifest_path": str(path),
        "manifest_exists": Path(path).exists(),
        "status": payload.get("status", ""),
        "candidate_bridge_rows": int(payload.get("candidate_bridge_rows") or 0),
        "atom_rows": atom_rows,
        "passed": bool(payload) and atom_rows > 0,
        "failure_reason": "" if payload and atom_rows > 0 else ("missing_v551_manifest" if not payload else "v551_atom_rows_zero"),
    }


def summarize_v552_functional_gate(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path)
    payload = _load_json(manifest_path)
    if not payload:
        current_manifest = manifest_path.with_name("manifest.json")
        payload = _load_json(current_manifest)
        if payload:
            manifest_path = current_manifest
    atom_rows = int(payload.get("atoms_row_count") or payload.get("input_atom_rows") or 0)
    status = str(payload.get("final_status") or payload.get("status") or "")
    normalized_status = status.upper().removeprefix("STATUS: ").strip()
    structural_ready = normalized_status in {
        "READY_V552_STRUCTURAL_HANDOFF",
        "READY_V552_STRUCTURAL_PRESSURE_CONTRACT",
    }
    if not payload:
        failure_reason = "missing_v552_manifest"
    elif atom_rows <= 0:
        failure_reason = "v552_atoms_row_count_zero"
    elif status.upper() == "STATUS: NOT_READY_STRUCTURAL_GROUPING_MISSING":
        failure_reason = "v552_structural_grouping_missing"
    elif status.upper() == "STATUS: READY_V552_STATUS_ONLY_INSUFFICIENT_DIRECTIONALITY":
        failure_reason = "v552_insufficient_directionality_for_structural_handoff"
    elif not structural_ready:
        failure_reason = "v552_not_structural_handoff_ready"
    else:
        failure_reason = ""
    return {
        "manifest_path": str(manifest_path),
        "manifest_exists": manifest_path.exists(),
        "final_status": status,
        "atoms_row_count": atom_rows,
        "passed": not failure_reason,
        "failure_reason": failure_reason,
    }

def summarize_v550j_functional_gate(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path)
    payload = _load_json(manifest_path)
    tables = payload.get("tables") if isinstance(payload.get("tables"), dict) else {}
    pattern_rows = int((tables.get("joint_response_pattern_index") or {}).get("rows") or 0)
    meaning_rows = int((tables.get("joint_pattern_meaning_summary") or {}).get("rows") or 0)
    validation_status = str(payload.get("validation_status") or "")

    readiness_path = manifest_path.with_name("v550j_source_wave_readiness_report.json")
    readiness = _load_json(readiness_path)
    readiness_status = str(readiness.get("readiness_status") or "")
    registry_status = str(readiness.get("family_registry_status") or "")
    blocking_issues = readiness.get("blocking_issues") or []
    if not isinstance(blocking_issues, list):
        blocking_issues = [str(blocking_issues)]

    if not payload:
        failure_reason = "missing_v550j_manifest"
    elif not readiness:
        failure_reason = "missing_v550j_source_wave_readiness_report"
    elif not _truthy(payload.get("success")):
        failure_reason = "v550j_manifest_success_false"
    elif validation_status.lower() != "pass":
        failure_reason = "v550j_output_validation_not_pass"
    elif registry_status != "applicable":
        failure_reason = "v550j_family_registry_not_applicable"
    elif readiness_status == "failed_validation" or blocking_issues:
        failure_reason = "v550j_source_wave_readiness_blocked"
    elif pattern_rows <= 0:
        failure_reason = "v550j_pattern_rows_zero"
    elif meaning_rows <= 0:
        failure_reason = "v550j_meaning_rows_zero"
    else:
        failure_reason = ""

    return {
        "manifest_path": str(manifest_path),
        "manifest_exists": manifest_path.exists(),
        "readiness_path": str(readiness_path),
        "readiness_exists": readiness_path.exists(),
        "validation_status": validation_status,
        "readiness_status": readiness_status,
        "family_registry_status": registry_status,
        "blocking_issues": blocking_issues,
        "pattern_rows": pattern_rows,
        "meaning_rows": meaning_rows,
        "passed": not failure_reason,
        "failure_reason": failure_reason,
    }

def summarize_v551j_functional_gate(root: str | Path) -> dict[str, Any]:
    root_path = Path(root)
    current_readiness_path = root_path / "manifest/v551j_readiness_report.json"
    current_contract_path = root_path / "manifest/v551j_packet_contract_validation_report.json"
    manifest_path = root_path / "manifest/manifest.json"
    packet_path = root_path / "manifest/v551j_packet_readiness_report.json"
    review_path = root_path / "manifest/v551j_review_readiness_report.json"
    cert_path = root_path / "manifest/v551j_certification_readiness_report.json"
    provenance_path = root_path / "manifest/v551j_input_provenance_manifest.json"
    certified_index_path = root_path / "packets/v551j_certified_joint_packet_index.parquet"
    legacy_certified_index_path = root_path / "packets/v551j_certified_packet_index.parquet"
    reviewable_sidecar_path = root_path / "packets/v551j_review_surface.parquet"
    legacy_reviewable_sidecar_path = root_path / "packets/v551j_reviewable_evidence_sidecar.parquet"
    candidate_index_path = root_path / "packets/v551j_joint_packet_candidate_index.parquet"

    current_readiness = _load_json(current_readiness_path)
    current_contract = _load_json(current_contract_path)
    manifest = _load_json(manifest_path)
    packet = _load_json(packet_path) or current_readiness
    review = _load_json(review_path) or current_readiness
    cert = _load_json(cert_path) or current_readiness
    provenance = _load_json(provenance_path)

    manifest_counts = manifest.get("row_counts", {}) if isinstance(manifest.get("row_counts"), dict) else {}
    certified_index_resolved = certified_index_path if certified_index_path.exists() else legacy_certified_index_path
    reviewable_sidecar_resolved = reviewable_sidecar_path if reviewable_sidecar_path.exists() else legacy_reviewable_sidecar_path
    packet_rows = int(
        packet.get("candidate_packet_rows")
        or packet.get("candidate_packet_count")
        or manifest_counts.get("candidate")
        or _parquet_rows(candidate_index_path)
        or 0
    )
    review_rows = int(
        review.get("review_surface_rows")
        or manifest_counts.get("review")
        or _parquet_rows(reviewable_sidecar_path)
        or _parquet_rows(legacy_reviewable_sidecar_path)
        or 0
    )
    certified_rows = int(
        cert.get("certified_packet_rows")
        or cert.get("certified_packet_count")
        or manifest_counts.get("certified")
        or _parquet_rows(certified_index_resolved)
        or 0
    )
    packet_status = str(packet.get("final_status") or "")
    review_status = str(review.get("final_status") or "")
    certification_status = str(cert.get("final_status") or "")
    provenance_status = str(provenance.get("final_status") or packet_status or "")
    candidate_contract_valid = _truthy(
        packet.get("candidate_contract_valid")
        if "candidate_contract_valid" in packet
        else current_contract.get("candidate_contract_valid")
    )
    component_contract_valid = _truthy(
        packet.get("component_contract_valid")
        if "component_contract_valid" in packet
        else current_contract.get("component_contract_valid")
    )

    required_artifacts = {
        "current_readiness": current_readiness_path,
        "packet_contract_validation": current_contract_path,
        "manifest": manifest_path,
        "input_provenance": provenance_path,
        "candidate_packet_index": candidate_index_path,
        "certified_packet_index": certified_index_resolved,
        "reviewable_evidence_sidecar": reviewable_sidecar_resolved,
    }
    missing_artifacts = [name for name, path in required_artifacts.items() if not path.exists()]

    if missing_artifacts:
        failure_reason = "v551j_missing_required_artifacts:" + ",".join(missing_artifacts)
    elif not candidate_contract_valid:
        failure_reason = "v551j_candidate_contract_invalid"
    elif not component_contract_valid:
        failure_reason = "v551j_component_contract_invalid"
    elif packet_status.upper().startswith("NOT_READY"):
        failure_reason = "v551j_packet_readiness_blocked"
    elif packet_rows <= 0:
        failure_reason = "v551j_candidate_packet_rows_zero"
    elif review_status.upper().startswith("NOT_READY"):
        failure_reason = "v551j_review_readiness_blocked"
    elif review_rows <= 0:
        failure_reason = "v551j_review_surface_rows_zero"
    elif certification_status.upper().startswith("NOT_READY"):
        failure_reason = "v551j_certification_readiness_blocked"
    elif certified_rows <= 0:
        failure_reason = "v551j_certified_packet_rows_zero"
    elif not certification_status.upper().startswith("READY_V551J_EVIDENCE_CERTIFIED"):
        failure_reason = "v551j_certification_status_unrecognized"
    elif provenance_status.upper().startswith("NOT_READY"):
        failure_reason = "v551j_provenance_readiness_blocked"
    elif provenance_status != certification_status:
        failure_reason = "v551j_provenance_certification_status_mismatch"
    else:
        failure_reason = ""

    return {
        "root": str(root_path),
        "packet_status": packet_status,
        "review_status": review_status,
        "certification_status": certification_status,
        "provenance_status": provenance_status,
        "candidate_packet_rows": packet_rows,
        "review_surface_rows": review_rows,
        "certified_packet_rows": certified_rows,
        "required_artifacts": {name: str(path) for name, path in required_artifacts.items()},
        "compatibility_aliases": {
            "legacy_packet_readiness": str(packet_path),
            "legacy_review_readiness": str(review_path),
            "legacy_certification_readiness": str(cert_path),
            "legacy_certified_packet_index": str(legacy_certified_index_path),
            "legacy_reviewable_evidence_sidecar": str(legacy_reviewable_sidecar_path),
            "current_readiness": str(current_readiness_path),
            "current_packet_contract_validation": str(current_contract_path),
            "current_candidate_packet_index": str(candidate_index_path),
            "current_review_surface": str(reviewable_sidecar_path),
            "current_certified_joint_packet_index": str(certified_index_path),
        },
        "missing_required_artifacts": missing_artifacts,
        "candidate_contract_valid": candidate_contract_valid,
        "component_contract_valid": component_contract_valid,
        "passed": not failure_reason,
        "failure_reason": failure_reason,
    }


def summarize_v552j_functional_gate(path: str | Path) -> dict[str, Any]:
    payload = _load_json(path)
    status = str(payload.get("status") or "")
    adapter_ready = _truthy(payload.get("adapter_preflight_ready"))
    probe_ready = _truthy(payload.get("ready_for_v553_probe"))
    missing_required = payload.get("missing_required_inputs_json", "[]")
    try:
        missing_list = json.loads(missing_required) if isinstance(missing_required, str) else list(missing_required or [])
    except Exception:
        missing_list = [str(missing_required)]
    passed = bool(payload) and adapter_ready and probe_ready and not status.upper().startswith("BLOCKED") and not missing_list
    return {
        "readiness_path": str(path),
        "readiness_exists": Path(path).exists(),
        "status": status,
        "adapter_preflight_ready": adapter_ready,
        "ready_for_v553_probe": probe_ready,
        "ready_for_v553_temporal_field": _truthy(payload.get("ready_for_v553_temporal_field")),
        "packet_rows": int(payload.get("packet_rows") or 0),
        "missing_required_inputs": missing_list,
        "passed": passed,
        "failure_reason": "" if passed else ("missing_v552j_readiness" if not payload else "v552j_semantic_gate_blocked"),
    }


def _source_aliases(family: str) -> list[str]:
    aliases = {family}
    aliases_by_key = {
        "gss": {"GSS", "General Social Survey"},
        "wvs": {"WVS", "World Values Survey"},
        "evs": {"EVS", "European Values Study"},
        "afrobarometer": {"Afrobarometer", "Afro Barometer"},
        "arabbarometer": {"Arab Barometer", "ArabBarometer"},
        "asianbarometer": {"Asian Barometer", "AsianBarometer", "Asian Barometer Survey"},
        "latinobarometro": {"Latinobarometro", "Latinobarómetro"},
        "lits": {"LiTS", "Life in Transition Survey"},
        "southasia": {"South Asia", "South Asia Barometer"},
    }
    aliases.update(aliases_by_key.get(_norm(family), set()))
    return sorted(aliases)

def _wave_aliases(family: str, wave: str) -> list[str]:
    aliases = {wave}
    family_key = _norm(family)
    evs = {"1981": "W1", "1990": "W2", "1999": "W3", "2008": "W4", "2017": "W5"}
    roman_numeric = {"I": "1", "II": "2", "III": "3", "IV": "4", "V": "5", "VI": "6", "VII": "7", "VIII": "8", "IX": "9"}
    numeric_labels: set[str] = set()
    if family_key == "evs":
        if wave in evs:
            aliases.add(evs[wave])
            numeric_labels.add(evs[wave][1:])
        for year, label in evs.items():
            if wave.upper() == label:
                aliases.add(year)
                numeric_labels.add(label[1:])
    upper_wave = wave.upper().strip()
    if upper_wave in roman_numeric:
        numeric_labels.add(roman_numeric[upper_wave])
    match = re.fullmatch(r"(?:W|R|WAVE\s*|ROUND\s*)?(\d+)", upper_wave)
    if match:
        numeric_labels.add(match.group(1))
    for number in numeric_labels:
        aliases.update({number, f"W{number}", f"R{number}", f"Wave {number}", f"Round {number}"})
    return sorted(aliases)


def _registry_var_codes(payload: dict[str, Any], family: str, wave: str) -> dict[str, list[str]]:
    source_family = str(payload.get("source_family") or "")
    aggregate_sources = {"alllayer1scopes", "allscopes", "all"}
    if source_family and _norm(source_family) not in {_norm(family), *aggregate_sources}:
        return {}
    wave_keys = {_norm(value) for value in _wave_aliases(family, wave)}
    output: dict[str, list[str]] = {}
    for family_cfg in payload.get("families") or []:
        if not isinstance(family_cfg, dict):
            continue
        family_source = str(family_cfg.get("source_family") or source_family)
        if family_source and _norm(family_source) not in {_norm(family), *aggregate_sources}:
            continue
        eligible = family_cfg.get("eligible_waves") or []
        if eligible and not ({_norm(value) for value in eligible} & wave_keys):
            continue
        codes: list[str] = []
        groups = family_cfg.get("item_role_groups") or {}
        if isinstance(groups, dict):
            for rows in groups.values():
                for row in rows or []:
                    if isinstance(row, dict) and row.get("var_code"):
                        code = str(row["var_code"]).strip()
                        if code and code not in codes:
                            codes.append(code)
        if codes:
            output[str(family_cfg.get("family_id") or "unnamed_family")] = codes
    return output


def _joint_registry_payload_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _joint_registry_status_is_executable(value: Any) -> bool:
    return registry_status_is_executable(value)


def resolve_joint_authority(config: RuntimeConfig, family: str, wave: str, selected_vars: Iterable[str] | None = None) -> dict[str, Any]:
    selected_keys = {_norm(value) for value in selected_vars or []}
    matching: list[dict[str, Any]] = []
    rejected_statuses: list[dict[str, str]] = []
    for path in config.joint_registry_paths:
        payload = _load_yaml(path)
        if not payload:
            continue
        families = _registry_var_codes(payload, family, wave)
        if not families:
            continue
        registry_status = str(payload.get("status") or "").strip()
        if not _joint_registry_status_is_executable(registry_status):
            rejected_statuses.append({"path": str(path), "registry_status": registry_status})
            continue
        overlap = {
            family_id: [code for code in codes if not selected_keys or _norm(code) in selected_keys]
            for family_id, codes in families.items()
        }
        applicable = {family_id: codes for family_id, codes in overlap.items() if codes}
        matching.append({
            "path": str(path),
            "registry_status": registry_status,
            "registry_hash": _joint_registry_payload_hash(payload),
            "families": families,
            "selected_overlap": applicable,
        })
    if not matching:
        if rejected_statuses:
            return {
                "applicable": False,
                "reason": "joint_registry_status_not_executable",
                "registry_path": "",
                "registry_paths": [row["path"] for row in rejected_statuses],
                "rejected_registry_statuses": rejected_statuses,
                "candidate_vars": [],
            }
        return {"applicable": False, "reason": "no_explicit_joint_registry_for_family_wave", "registry_path": "", "candidate_vars": []}

    distinct_hashes = {row["registry_hash"] for row in matching}
    if len(distinct_hashes) > 1:
        candidate_vars = sorted({code for row in matching for codes in row["families"].values() for code in codes})
        return {
            "applicable": False,
            "reason": "conflicting_joint_registries_for_family_wave",
            "registry_path": "",
            "registry_paths": [row["path"] for row in matching],
            "registry_hashes": [row["registry_hash"] for row in matching],
            "candidate_vars": candidate_vars,
        }

    # Exact duplicate copies are operationally equivalent. Choose deterministically
    # and preserve the duplicate paths in the diagnostic record.
    chosen = sorted(matching, key=lambda row: row["path"])[0]
    candidate_vars = [code for codes in chosen["families"].values() for code in codes]
    duplicate_paths = [row["path"] for row in matching if row["path"] != chosen["path"]]
    if selected_vars is not None and not chosen["selected_overlap"]:
        return {
            "applicable": False,
            "reason": "joint_registry_exists_but_selected_slice_has_no_family_items",
            "registry_path": chosen["path"],
            "duplicate_registry_paths": duplicate_paths,
            "candidate_vars": candidate_vars,
            "registry_status": chosen["registry_status"],
        }
    return {
        "applicable": True,
        "reason": "explicit_joint_registry_applies",
        "registry_path": chosen["path"],
        "duplicate_registry_paths": duplicate_paths,
        "candidate_vars": candidate_vars,
        "registry_status": chosen["registry_status"],
        "registry_hash": chosen["registry_hash"],
        "selected_overlap": chosen["selected_overlap"],
    }


def summarize_joint_authority_coverage(
    config: RuntimeConfig,
    waves: Iterable[tuple[str, str, str]] = ALL_WAVES,
) -> dict[str, Any]:
    wave_rows = list(waves)
    covered: list[dict[str, Any]] = []
    missing: list[dict[str, Any]] = []
    for family, wave, country in wave_rows:
        authority = resolve_joint_authority(config, family, wave)
        record = {
            "source": family,
            "wave": wave,
            "country_code": country or COUNTRY_MAP.get(family, {}).get(wave, ""),
            "reason": authority.get("reason", ""),
            "registry_path": authority.get("registry_path", ""),
            "registry_status": authority.get("registry_status", ""),
            "candidate_var_count": len(authority.get("candidate_vars") or []),
        }
        (covered if authority.get("applicable") else missing).append(record)
    missing_by_family: dict[str, list[str]] = {}
    for row in missing:
        missing_by_family.setdefault(str(row["source"]), []).append(str(row["wave"]))
    return {
        "required_scope_count": len(wave_rows),
        "covered_scope_count": len(covered),
        "missing_scope_count": len(missing),
        "covered_scopes": covered,
        "missing_scopes": missing,
        "missing_by_family": missing_by_family,
        "full_chain_authority_complete": not missing,
    }


def _sql_normalized(column: str) -> str:
    return f"regexp_replace(translate(lower(COALESCE({column}::text, '')), 'áéíóúüñ', 'aeiouun'), '[^a-z0-9]+', '', 'g')"


def _select_question_variables(
    family: str,
    wave: str,
    country: str,
    seed: int = 42,
    *,
    config: RuntimeConfig = DEFAULT_CONFIG,
) -> list[str]:
    import psycopg2
    from dotenv import load_dotenv

    load_dotenv(config.env_file)
    db_url = config.db_url or os.environ.get("DATABASE_URL", "")
    if not db_url:
        raise RuntimeError("DATABASE_URL is required to select the 20-variable slice")
    qsm_rel = _validate_relation_identifier(config.qsm_relation, "qsm_relation")
    registry_rel = _validate_relation_identifier(config.canonical_registry_relation, "canonical_registry_relation")
    source_keys = sorted({_norm(value) for value in _source_aliases(family)})
    wave_keys = sorted({_norm(value) for value in _wave_aliases(family, wave)})

    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""WITH mapped_questions AS (
                       SELECT DISTINCT {_sql_normalized('var_code')} AS normalized_var_key
                       FROM {qsm_rel}
                       WHERE {_sql_normalized('source')} = ANY(%s)
                         AND {_sql_normalized('wave')} = ANY(%s)
                     )
                     SELECT cr.canonical_var_code, COALESCE(cr.authority_semantic_role, '')
                     FROM {registry_rel} cr
                     JOIN mapped_questions mq
                       ON mq.normalized_var_key = {_sql_normalized('cr.canonical_var_code')}
                     WHERE {_sql_normalized('cr.canonical_source')} = ANY(%s)
                       AND {_sql_normalized('cr.canonical_wave')} = ANY(%s)
                     ORDER BY cr.canonical_var_code""",
                (source_keys, wave_keys, source_keys, wave_keys),
            )
            fetched = [(str(code), str(role or "")) for code, role in cur.fetchall()]
    # A registry may contain multiple aliases or authority rows for one
    # canonical question.  The smoke slice is a set of questions, not a sample
    # of registry rows, so deduplicate before category sampling.
    all_vars: list[tuple[str, str]] = []
    seen_var_keys: set[str] = set()
    for code, role in fetched:
        key = _norm(code)
        if not key or key in seen_var_keys:
            continue
        seen_var_keys.add(key)
        all_vars.append((code, role))
    if not all_vars:
        return "", []

    available_by_key = {_norm(code): code for code, _ in all_vars}
    authority = resolve_joint_authority(config, family, wave)
    selected: list[str] = []
    if authority.get("applicable"):
        registry_payload = _load_yaml(Path(authority["registry_path"]))
        family_candidates = _registry_var_codes(registry_payload, family, wave)
        for codes in family_candidates.values():
            present = [available_by_key[_norm(code)] for code in codes if _norm(code) in available_by_key]
            if len(present) >= 3:
                selected.extend(present[: min(6, len(present))])
                break

    buckets: dict[str, list[str]] = {category: [] for category in CATEGORIES}
    for code, role in all_vars:
        role_lower = role.lower().strip()
        category = next((name for name, words in CATEGORIES.items() if any(word in role_lower for word in words)), "relation_evidence")
        buckets[category].append(code)

    rng = random.Random(seed)
    targets = [
        ("demographic_context", 4),
        ("directional_attitudinal", 4),
        ("relation_evidence", 4),
        ("structural_mapped", 4),
        ("edge_ambiguous", 2),
        ("known_fragile", 2),
    ]
    for category, target in targets:
        room = max(0, 20 - len(selected))
        if not room:
            break
        available = [code for code in buckets[category] if code not in selected]
        count = min(target, room, len(available))
        if count:
            selected.extend(rng.sample(available, count))
    pool = [code for code, _ in all_vars if code not in selected]
    if len(selected) < 20 and pool:
        selected.extend(rng.sample(pool, min(20 - len(selected), len(pool))))
    selected = list(dict.fromkeys(selected))[:20]
    rng.shuffle(selected)
    return selected


def _build_question_filter(
    family: str,
    wave: str,
    country: str,
    seed: int = 42,
    *,
    config: RuntimeConfig = DEFAULT_CONFIG,
    filter_root: str | Path | None = None,
) -> tuple[str, list[str]]:
    selected = _select_question_variables(family, wave, country, seed=seed, config=config)
    if not selected:
        return "", []

    root = Path(filter_root) if filter_root else Path("/tmp") / "rawlsing_20var_filters"
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{_family_wave_id(family, wave)}.json"
    path.write_text(json.dumps({"question_ids": selected, "var_codes": selected}, indent=2) + "\n", encoding="utf-8")
    return str(path), selected


def _stage_result(raw: dict[str, Any], semantic: dict[str, Any] | None = None) -> dict[str, Any]:
    result = {
        "exit_code": raw.get("exit_code", -99),
        "elapsed": raw.get("elapsed", 0),
        "process_pass": raw.get("exit_code") == 0,
    }
    if raw.get("stderr_tail"):
        result["stderr_tail"] = raw["stderr_tail"]
    if semantic is not None:
        result["semantic_gate"] = semantic
        result["semantic_pass"] = bool(semantic.get("passed"))
    return result


def run_v550_shard(
    run_id: str,
    shard_id: str,
    family: str,
    wave: str,
    country: str,
    filter_path: str,
    output_root: str,
    registry_path: str | None = None,
    config: RuntimeConfig = DEFAULT_CONFIG,
) -> dict[str, Any]:
    cmd = [
        sys.executable,
        _abs("data/ddm_build_copy/build_determinicity_wave_shard_v550.py", config),
        "--run-id", run_id,
        "--shard-id", shard_id,
        "--source", family,
        "--wave", wave,
        "--canonical-wave", wave,
        "--output-root", output_root,
        "--question-filter-file", filter_path,
        "--limit-questions", "20",
        "--env-file", str(config.env_file),
        "--response-long-relation", str(config.response_long_relation),
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
    return _invoke_run(cmd, timeout_sec=3600, config=config)


def run_v551(shard_id: str, bridge_path: str, quc_path: str, response_map_path: str, output_root: str, config: RuntimeConfig = DEFAULT_CONFIG) -> dict[str, Any]:
    cmd = [
        sys.executable,
        _abs("data/ddm_build_copy/compile_v551_relation_evidence_atoms.py", config),
        "--run-id", shard_id,
        "--bridge-path", bridge_path,
        "--question-use-contract-path", quc_path,
        "--response-option-map-path", response_map_path,
        "--output-root", output_root,
        "--v551-compile-mode", "optimized_candidate_bridge",
        "--v551-audit-mode", "summary",
        "--no-progress",
        "--no-write-csv",
    ]
    return _invoke_run(cmd, timeout_sec=1800, config=config)


def run_v552(shard_id: str, atoms_path: str, output_root: str, config: RuntimeConfig = DEFAULT_CONFIG) -> dict[str, Any]:
    cmd = [
        sys.executable,
        _abs("data/ddm_build_copy/compile_v552_structural_ddm.py", config),
        "--run-id", shard_id,
        "--atoms-path", atoms_path,
        "--output-root", output_root,
        "--strict-handoff",
        "--no-progress",
        "--no-write-csv",
    ]
    return _invoke_run(cmd, timeout_sec=1800, config=config)


def run_v550j(
    run_id: str,
    shard_dir: str,
    filter_path: str,
    output_root: str,
    registry_path: str,
    response_map_path: str,
    prepared_substrate_path: str | None = None,
    prepared_substrate_manifest_path: str | None = None,
    config: RuntimeConfig = DEFAULT_CONFIG,
) -> dict[str, Any]:
    cmd = [
        sys.executable,
        _abs("data/ddm_build_copy/compile_v550j_joint_response_patterns.py", config),
        "--v550-shard-dir", shard_dir,
        "--output-root", output_root,
        "--registry-path", registry_path,
        "--response-option-map", response_map_path,
        "--question-filter-file", filter_path,
        "--env-file", str(config.env_file),
        "--association-mode", config.association_mode,
        "--no-progress",
        "--no-write-csv",
        "--with-diagnostics",
    ]
    if prepared_substrate_path and prepared_substrate_manifest_path:
        cmd.extend([
            "--v550j-substrate-mode", "prepared_required",
            "--prepared-substrate-path", prepared_substrate_path,
            "--prepared-substrate-manifest-path", prepared_substrate_manifest_path,
            "--forbid-database-access",
        ])
    elif config.db_url:
        cmd.extend(["--db-url", config.db_url])
    if config.association_mode != "off":
        if config.association_lane_registry:
            cmd.extend(["--association-lane-registry-path", str(config.association_lane_registry)])
        if config.association_threshold_profiles:
            cmd.extend(["--association-threshold-profiles-path", str(config.association_threshold_profiles)])
    return _invoke_run(cmd, timeout_sec=1800, config=config)


V552_CONTEXT_FILES = {
    "--v552-question-semantic-hierarchy-path": "question_semantic_hierarchy.parquet",
    "--v552-structural-channel-index-path": "structural_channel_index.parquet",
    "--v552-relation-axis-pressure-path": "relation_axis_pressure.parquet",
    "--v552-target-entity-pressure-path": "target_entity_pressure.parquet",
    "--v552-driver-facet-pressure-path": "driver_facet_pressure.parquet",
    "--v552-contradiction-surface-path": "contradiction_surface.parquet",
    "--v552-horizon-constraint-index-path": "horizon_constraint_index.parquet",
    "--v552-parent-prior-manifest-path": "parent_prior_manifest.parquet",
}

V552J_EXTRA_FILES = {
    "--v552-artifact-authority-index-path": "v552_artifact_authority_index.parquet",
    "--v552-known-absence-register-path": "v552_known_absence_register.parquet",
    "--v552-structural-fact-index-path": "v552_structural_fact_index.parquet",
    "--v552-temporal-key-source-index-path": "v552_temporal_key_source_index.parquet",
}


def _append_existing_context(cmd: list[str], structural_dir: str | Path, mapping: dict[str, str]) -> None:
    root = Path(structural_dir)
    for flag, filename in mapping.items():
        path = root / filename
        if path.exists():
            cmd.extend([flag, str(path)])


def run_v551j(
    shard_id: str,
    atoms_path: str,
    pattern_index_path: str,
    meaning_summary_path: str,
    output_root: str,
    v552_structural_dir: str,
    config: RuntimeConfig = DEFAULT_CONFIG,
    registry_path: str | None = None,
) -> dict[str, Any]:
    pattern_root = Path(pattern_index_path).parent
    cmd = [
        sys.executable,
        _abs("data/ddm_build_copy/compile_v551j_joint_evidence_packets.py", config),
        "--run-id", shard_id,
        "--v551-atoms-path", atoms_path,
        "--v550j-pattern-index-path", pattern_index_path,
        "--v550j-pattern-item-index-path", str(pattern_root / "joint_response_pattern_item_index.parquet"),
        "--v550j-relation-signature-path", str(pattern_root / "joint_pattern_relation_signature.parquet"),
        "--v550j-manifest-path", str(pattern_root / "v550j_manifest.json"),
        "--v550j-readiness-report-path", str(pattern_root / "v550j_source_wave_readiness_report.json"),
        "--registry-path", str(registry_path or DEFAULT_JOINT_REGISTRY),
        "--v550j-meaning-summary-path", meaning_summary_path,
        "--output-root", output_root,
        "--emit-review-surface",
        "--emit-certified-index",
        "--no-write-csv",
    ]
    _append_existing_context(cmd, v552_structural_dir, V552_CONTEXT_FILES)
    return _invoke_run(cmd, timeout_sec=1800, config=config)


def run_v552j(
    shard_id: str,
    v551j_run_root: str,
    output_root: str,
    v552_structural_dir: str,
    config: RuntimeConfig = DEFAULT_CONFIG,
) -> dict[str, Any]:
    cmd = [
        sys.executable,
        _abs("data/ddm_build_copy/compile_v552j_runtime_safe_structural_handoff.py", config),
        "--run-id", shard_id,
        "--v551j-run-root", v551j_run_root,
        "--output-root", output_root,
    ]
    _append_existing_context(cmd, v552_structural_dir, {**V552_CONTEXT_FILES, **V552J_EXTRA_FILES})
    return _invoke_run(cmd, timeout_sec=1800, config=config)


def _fail(result: dict[str, Any], stage: str, reason: str) -> dict[str, Any]:
    result["failure_stage"] = stage
    result["functional_failure_reason"] = reason
    result["passed"] = False
    return result


def run_wave(
    family: str,
    wave: str,
    country: str,
    run_ts: str,
    output_root: str,
    filter_path: str,
    selected_vars: list[str],
    config: RuntimeConfig = DEFAULT_CONFIG,
) -> dict[str, Any]:
    run_id = f"{_family_wave_id(family, wave)}_{run_ts}"
    shard_id = f"{family}_{wave}" + (f"_{country}" if country else "")
    result: dict[str, Any] = {
        "survey_family": family,
        "wave_id": wave,
        "country": country,
        "run_id": run_id,
        "selected_variable_count": len(selected_vars),
        "selected_variables": selected_vars,
        "stages": {},
        "functional_checks": {},
        "joint_branch": {},
        "base_spine_passed": False,
        "full_chain_passed": False,
        "acceptance_boundary": "none",
        "passed": False,
    }

    _log(f"WAVE {family} {wave} ({country}) — {len(selected_vars)} variables")
    shard_dir = Path(output_root) / "v550" / "shard_runs" / run_id / shard_id
    authority = resolve_joint_authority(config, family, wave, selected_vars)
    result["joint_branch"]["authority"] = authority

    registry_path_for_v550 = authority["registry_path"] if authority.get("applicable") and config.joint_mode != "off" else None
    raw = run_v550_shard(run_id, shard_id, family, wave, country, filter_path, str(Path(output_root) / "v550"), registry_path_for_v550, config)
    if raw["exit_code"] != 0:
        result["stages"]["v550"] = _stage_result(raw)
        return _fail(result, "v550_process", raw.get("stderr_tail") or "v550_nonzero_exit")
    v550_gate = summarize_v550_manifest_gate(shard_dir / "manifest.json")
    result["stages"]["v550"] = _stage_result(raw, v550_gate)
    result["functional_checks"]["v550_manifest"] = v550_gate
    if not v550_gate["passed"]:
        return _fail(result, "v550_manifest_gate", v550_gate["failure_reason"])

    quc_gate = summarize_quc_functional_gate(shard_dir / "core/question_use_contract.parquet")
    result["functional_checks"]["v550_quc"] = quc_gate
    if not quc_gate["passed"]:
        return _fail(result, "v550_quc_gate", quc_gate["failure_reason"])

    response_map_path = shard_dir / "core/response_option_map.parquet"
    if not response_map_path.exists():
        return _fail(result, "v550_response_semantics_contract", "missing_scoped_response_option_map_artifact")

    bridge_path = shard_dir / "bridge/v551_bridge_index.parquet"
    quc_path = shard_dir / "core/question_use_contract.parquet"
    v551_root = Path(output_root) / "v551"
    raw = run_v551(shard_id, str(bridge_path), str(quc_path), str(response_map_path), str(v551_root), config)
    if raw["exit_code"] != 0:
        result["stages"]["v551"] = _stage_result(raw)
        return _fail(result, "v551_process", raw.get("stderr_tail") or "v551_nonzero_exit")
    v551_gate = summarize_v551_functional_gate(v551_root / shard_id / "manifest.json")
    result["stages"]["v551"] = _stage_result(raw, v551_gate)
    result["functional_checks"]["v551"] = v551_gate
    if not v551_gate["passed"]:
        return _fail(result, "v551_gate", v551_gate["failure_reason"])

    atoms_path = v551_root / shard_id / "relation_evidence_atoms.parquet"
    v552_root = Path(output_root) / "v552"
    raw = run_v552(shard_id, str(atoms_path), str(v552_root), config)
    if raw["exit_code"] != 0:
        result["stages"]["v552"] = _stage_result(raw)
        return _fail(result, "v552_process", raw.get("stderr_tail") or "v552_nonzero_exit")
    v552_gate = summarize_v552_functional_gate(v552_root / shard_id / "manifest/v552_input_provenance_manifest.json")
    result["stages"]["v552"] = _stage_result(raw, v552_gate)
    result["functional_checks"]["v552"] = v552_gate
    if not v552_gate["passed"]:
        return _fail(result, "v552_gate", v552_gate["failure_reason"])

    result["base_spine_passed"] = True
    result["acceptance_boundary"] = "base_spine"

    if config.joint_mode == "off":
        result["joint_branch"]["status"] = "disabled_by_explicit_mode"
        result["joint_branch"]["reason"] = "joint_mode_off"
        result["passed"] = True
        return result
    if not authority.get("applicable"):
        result["joint_branch"]["status"] = "authority_missing"
        result["joint_branch"]["reason"] = authority.get("reason", "joint_authority_missing")
        if config.joint_mode == "required":
            return _fail(result, "joint_authority_gate", result["joint_branch"]["reason"] or "joint_authority_missing")
        result["passed"] = True
        return result

    v550j_root = Path(output_root) / "v550j"
    substrate_manifests = sorted((shard_dir / "checkpoints/respondent_substrate").glob("source=*/wave=*/country_code=*/v550_shared_respondent_substrate_manifest.json"))
    if not substrate_manifests:
        return _fail(result, "shared_respondent_substrate_gate", "missing_shared_respondent_substrate_manifest")
    substrate_manifest = substrate_manifests[0]
    substrate_parquet = substrate_manifest.with_name("v550_shared_respondent_substrate.parquet")
    if not substrate_parquet.exists():
        return _fail(result, "shared_respondent_substrate_gate", "missing_shared_respondent_substrate_parquet")
    result["joint_branch"]["shared_respondent_substrate"] = {
        "parquet_path": str(substrate_parquet),
        "manifest_path": str(substrate_manifest),
    }
    raw = run_v550j(
        run_id,
        str(shard_dir),
        filter_path,
        str(v550j_root),
        authority["registry_path"],
        str(response_map_path),
        str(substrate_parquet),
        str(substrate_manifest),
        config,
    )
    v550j_artifact_root = v550j_root / "runs" / run_id / shard_id / "joint_patterns"
    if raw["exit_code"] != 0:
        result["stages"]["v550j"] = _stage_result(raw)
        return _fail(result, "v550j_process", raw.get("stderr_tail") or "v550j_nonzero_exit")
    v550j_gate = summarize_v550j_functional_gate(v550j_artifact_root / "v550j_manifest.json")
    result["stages"]["v550j"] = _stage_result(raw, v550j_gate)
    result["functional_checks"]["v550j"] = v550j_gate
    if not v550j_gate["passed"]:
        return _fail(result, "v550j_gate", v550j_gate["failure_reason"])

    pattern_index = v550j_artifact_root / "joint_response_pattern_index.parquet"
    meaning_summary = v550j_artifact_root / "joint_pattern_meaning_summary.parquet"
    v552_structural_dir = v552_root / shard_id / "structural"
    v551j_root = Path(output_root) / "v551j"
    raw = run_v551j(shard_id, str(atoms_path), str(pattern_index), str(meaning_summary), str(v551j_root), str(v552_structural_dir), config, str(authority["registry_path"]))
    v551j_run_root = v551j_root / shard_id
    if raw["exit_code"] != 0:
        result["stages"]["v551j"] = _stage_result(raw)
        return _fail(result, "v551j_process", raw.get("stderr_tail") or "v551j_nonzero_exit")
    v551j_gate = summarize_v551j_functional_gate(v551j_run_root)
    result["stages"]["v551j"] = _stage_result(raw, v551j_gate)
    result["functional_checks"]["v551j"] = v551j_gate
    if not v551j_gate["passed"]:
        return _fail(result, "v551j_gate", v551j_gate["failure_reason"])

    v552j_root = Path(output_root) / "v552j"
    raw = run_v552j(shard_id, str(v551j_run_root), str(v552j_root), str(v552_structural_dir), config)
    v552j_readiness = v552j_root / shard_id / "manifest/v552j_readiness_report.json"
    if raw["exit_code"] != 0:
        result["stages"]["v552j"] = _stage_result(raw)
        return _fail(result, "v552j_process", raw.get("stderr_tail") or "v552j_nonzero_exit")
    v552j_gate = summarize_v552j_functional_gate(v552j_readiness)
    result["stages"]["v552j"] = _stage_result(raw, v552j_gate)
    result["functional_checks"]["v552j"] = v552j_gate
    if not v552j_gate["passed"]:
        return _fail(result, "v552j_gate", v552j_gate["failure_reason"])

    result["joint_branch"]["status"] = "passed"
    result["full_chain_passed"] = True
    result["acceptance_boundary"] = "full_v550_to_v552j_chain"
    result["passed"] = True
    return result


def write_summaries(results: list[dict[str, Any]], output_root: str, run_ts: str, canary_only: bool, preflight: dict[str, Any] | None = None) -> None:
    report_dir = Path(output_root) / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    fields = [
        "survey_family", "wave_id", "country", "selected_variable_count", "passed", "failure_stage",
        "functional_failure_reason", "base_spine_passed", "full_chain_passed", "acceptance_boundary",
        "joint_branch_status", "joint_branch_reason", "v550_exit", "v551_exit",
        "v552_exit", "v550j_exit", "v551j_exit", "v552j_exit", "v551_atom_rows", "v552_atom_rows",
        "v550j_pattern_rows", "v551j_certified_rows", "v552j_status", "v552j_probe_ready",
    ]
    with (report_dir / "smoke_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for result in results:
            stages = result.get("stages", {})
            checks = result.get("functional_checks", {})
            joint = result.get("joint_branch", {})
            writer.writerow({
                "survey_family": result.get("survey_family", ""),
                "wave_id": result.get("wave_id", ""),
                "country": result.get("country", ""),
                "selected_variable_count": result.get("selected_variable_count", 0),
                "passed": result.get("passed", False),
                "failure_stage": result.get("failure_stage", ""),
                "functional_failure_reason": result.get("functional_failure_reason", ""),
                "base_spine_passed": result.get("base_spine_passed", False),
                "full_chain_passed": result.get("full_chain_passed", False),
                "acceptance_boundary": result.get("acceptance_boundary", "none"),
                "joint_branch_status": joint.get("status", ""),
                "joint_branch_reason": joint.get("reason", ""),
                "v550_exit": stages.get("v550", {}).get("exit_code", ""),
                "v551_exit": stages.get("v551", {}).get("exit_code", ""),
                "v552_exit": stages.get("v552", {}).get("exit_code", ""),
                "v550j_exit": stages.get("v550j", {}).get("exit_code", ""),
                "v551j_exit": stages.get("v551j", {}).get("exit_code", ""),
                "v552j_exit": stages.get("v552j", {}).get("exit_code", ""),
                "v551_atom_rows": checks.get("v551", {}).get("atom_rows", ""),
                "v552_atom_rows": checks.get("v552", {}).get("atoms_row_count", ""),
                "v550j_pattern_rows": checks.get("v550j", {}).get("pattern_rows", ""),
                "v551j_certified_rows": checks.get("v551j", {}).get("certified_packet_rows", ""),
                "v552j_status": checks.get("v552j", {}).get("status", ""),
                "v552j_probe_ready": checks.get("v552j", {}).get("ready_for_v553_probe", ""),
            })
    payload = {"run_ts": run_ts, "preflight": preflight or {}, "results": results}
    (report_dir / "smoke_summary.json").write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")

    total = len(results)
    passed = sum(bool(row.get("passed")) for row in results)
    failed = total - passed
    base_passed = sum(bool(row.get("base_spine_passed")) for row in results)
    full_chain_passed = sum(bool(row.get("full_chain_passed")) for row in results)
    scope_label = "canary only" if canary_only else "explicit 36-wave allowlist"
    lines = [
        "# Universality Functional Smoke Report",
        "",
        f"**Run:** {run_ts}",
        f"**Scope:** {scope_label}",
        "**Base spine:** V550 → V551 → V552",
        "**Full-chain acceptance:** V550J → V551J → V552J is required for every wave unless a diagnostic base-only mode was explicitly selected",
        "",
        "## Summary",
        "",
        f"- Waves attempted: {total}",
        f"- Base spines passed: {base_passed}",
        f"- Full V550→V552J chains passed: {full_chain_passed}",
        f"- Waves passed at the selected acceptance boundary: {passed}",
        f"- Waves failed: {failed}",
        "",
    ]
    if preflight:
        lines.extend([
            "## Preflight",
            "",
            f"- Passed: {preflight.get('passed', False)}",
            f"- Blockers: {len(preflight.get('blockers', []))}",
            f"- Warnings: {len(preflight.get('warnings', []))}",
            "",
        ])
    lines.extend(["## Failures", ""])
    failures = [row for row in results if not row.get("passed")]
    if not failures:
        lines.append("None.")
    else:
        for row in failures:
            lines.append(f"- {row['survey_family']} {row['wave_id']}: {row.get('failure_stage', 'unknown')} — {row.get('functional_failure_reason', '')}")
    lines.extend(["", "## Readiness", ""])
    if total and passed == total:
        lines.append(f"**READY at the selected boundary.** All {total} attempted waves passed. Full all-wave readiness still requires `full_chain_passed={total}`.")
    else:
        lines.append(f"**NOT READY.** Only {passed}/{total} waves passed functional gates. {failed} attempted waves remain blocked.")
    (report_dir / "smoke_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Truthful explicit-36-wave universality smoke runner")
    parser.add_argument("--output-root", default=None)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--canary-only", action="store_true")
    scope.add_argument("--family-band", action="store_true")
    parser.add_argument(
        "--only-scope",
        action="append",
        default=None,
        help="Run one explicit scope entry as 'Family|Wave|Country'. May be repeated.",
    )
    parser.add_argument("--skip-canary", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE))
    parser.add_argument("--db-url", default="")
    parser.add_argument("--qsm-relation", default=os.environ.get("DDM_QSM_RELATION", DEFAULT_QSM_RELATION))
    parser.add_argument("--canonical-registry-relation", default=os.environ.get("DDM_CANONICAL_REGISTRY_RELATION", DEFAULT_CANONICAL_REGISTRY_RELATION))
    parser.add_argument(
        "--response-long-relation",
        default=os.environ.get("DDM_RESPONSE_LONG_RELATION", AUTO_RESPONSE_RELATION),
        help="Respondent-long relation for V550. 'auto' prefers the authority-enriched view when present.",
    )
    parser.add_argument("--response-option-map", default=None)
    parser.add_argument("--joint-registry", action="append", default=None)
    parser.add_argument("--joint-mode", choices=("auto", "required", "off"), default="required")
    parser.add_argument("--association-mode", choices=("off", "funnel_only", "candidate_trace", "publishable"), default="off")
    parser.add_argument("--association-lane-registry", default=str(DEFAULT_ASSOCIATION_LANE_REGISTRY))
    parser.add_argument("--association-threshold-profiles", default=str(DEFAULT_ASSOCIATION_THRESHOLD_PROFILES))
    parser.add_argument("--first-pass-authority-dir", default=str(DEFAULT_FIRST_PASS_AUTHORITY_DIR))
    parser.add_argument("--semantic-authority-dir", default=str(DEFAULT_SEMANTIC_AUTHORITY_DIR))
    parser.add_argument("--position-conditioning-authority-dir", default=str(DEFAULT_POSITION_CONDITIONING_AUTHORITY_DIR))
    parser.add_argument("--directionality-authority-dir", default=str(DEFAULT_DIRECTIONALITY_AUTHORITY_DIR))
    parser.add_argument("--readiness-mode", choices=("full", "launch"), default="full")
    parser.add_argument("--diagnostic-continue", action="store_true")
    return parser.parse_args()


def _config_from_args(args: argparse.Namespace) -> RuntimeConfig:
    registry_paths = tuple(Path(value).expanduser().resolve() for value in (args.joint_registry or [str(DEFAULT_JOINT_REGISTRY)]))
    response_map = (
        Path(args.response_option_map).expanduser().resolve()
        if args.response_option_map
        else _default_response_option_map(REPO_ROOT)
    )
    return RuntimeConfig(
        repo_root=REPO_ROOT,
        env_file=Path(args.env_file).expanduser().resolve(),
        db_url=args.db_url,
        qsm_relation=args.qsm_relation,
        canonical_registry_relation=args.canonical_registry_relation,
        response_option_map=response_map,
        joint_registry_paths=registry_paths,
        association_lane_registry=Path(args.association_lane_registry).expanduser().resolve() if args.association_lane_registry else None,
        association_threshold_profiles=Path(args.association_threshold_profiles).expanduser().resolve() if args.association_threshold_profiles else None,
        first_pass_authority_dir=Path(args.first_pass_authority_dir).expanduser().resolve(),
        semantic_authority_dir=Path(args.semantic_authority_dir).expanduser().resolve(),
        position_conditioning_authority_dir=Path(args.position_conditioning_authority_dir).expanduser().resolve(),
        directionality_authority_dir=Path(args.directionality_authority_dir).expanduser().resolve(),
        association_mode=args.association_mode,
        joint_mode=args.joint_mode,
        readiness_mode=args.readiness_mode,
        diagnostic_continue=args.diagnostic_continue,
        response_long_relation=args.response_long_relation,
    )


def _parse_only_scope(entries: Iterable[str] | None) -> list[tuple[str, str, str]]:
    scope: list[tuple[str, str, str]] = []
    for entry in entries or []:
        parts = [part.strip() for part in str(entry).split("|")]
        if len(parts) not in {2, 3} or not parts[0] or not parts[1]:
            raise ValueError(f"invalid --only-scope value {entry!r}; expected 'Family|Wave|Country'")
        family, wave = parts[0], parts[1]
        country = parts[2] if len(parts) == 3 else COUNTRY_MAP.get(family, {}).get(wave, "")
        if (family, wave) not in {(known_family, known_wave) for known_family, known_wave, _ in ALL_WAVES}:
            raise ValueError(f"--only-scope value is not in the explicit 36-wave allowlist: {entry!r}")
        scope.append((family, wave, country))
    return scope


def _run_scope(scope: list[tuple[str, str, str]], *, run_ts: str, output_root: str, config: RuntimeConfig) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    filters_root = Path(output_root) / "filters"
    for index, (family, wave, country) in enumerate(scope):
        country = country or COUNTRY_MAP.get(family, {}).get(wave, "")
        try:
            filter_path, selected = _build_question_filter(family, wave, country, seed=index, config=config, filter_root=filters_root)
        except Exception as exc:
            results.append({
                "survey_family": family,
                "wave_id": wave,
                "country": country,
                "selected_variable_count": 0,
                "selected_variables": [],
                "stages": {},
                "functional_checks": {},
                "joint_branch": {},
                "passed": False,
                "failure_stage": "question_filter_selection",
                "functional_failure_reason": str(exc),
            })
            if not config.diagnostic_continue:
                break
            continue
        if not selected:
            results.append({
                "survey_family": family,
                "wave_id": wave,
                "country": country,
                "selected_variable_count": 0,
                "selected_variables": [],
                "stages": {},
                "functional_checks": {},
                "joint_branch": {},
                "passed": False,
                "failure_stage": "question_filter_selection",
                "functional_failure_reason": "no_variables_found",
            })
            if not config.diagnostic_continue:
                break
            continue
        result = run_wave(family, wave, country, run_ts, output_root, filter_path, selected, config)
        results.append(result)
        if not result.get("passed") and not config.diagnostic_continue:
            break
    return results


def main() -> int:
    args = parse_args()
    config = _config_from_args(args)
    run_ts = _now()
    output_root = args.output_root or str(REPO_ROOT / f"outputs/universality_20var_36wave_v550_552j_{run_ts}")
    Path(output_root).mkdir(parents=True, exist_ok=True)
    try:
        only_scope = _parse_only_scope(args.only_scope)
    except ValueError as exc:
        _log(str(exc))
        return 2

    if only_scope:
        preflight_scope = only_scope
    elif args.canary_only:
        preflight_scope = [(CANARY_FAMILY, CANARY_WAVE, CANARY_COUNTRY)]
    elif args.family_band:
        preflight_scope = list(FAMILY_BAND)
    else:
        preflight_scope = list(ALL_WAVES)

    preflight = run_preflight(config, preflight_scope)
    reports = Path(output_root) / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "preflight.json").write_text(json.dumps(preflight, indent=2) + "\n", encoding="utf-8")
    if args.preflight_only or not preflight["passed"]:
        _log(f"Preflight passed={preflight['passed']} blockers={len(preflight['blockers'])} warnings={len(preflight['warnings'])}")
        if preflight["blockers"]:
            for blocker in preflight["blockers"]:
                _log(f"  BLOCKER: {blocker}")
        return 0 if preflight["passed"] else 2

    if only_scope:
        results = _run_scope(only_scope, run_ts=run_ts, output_root=output_root, config=config)
        write_summaries(results, output_root, run_ts, canary_only=False, preflight=preflight)
        return 0 if len(results) == len(only_scope) and all(row.get("passed") for row in results) else 1

    if args.family_band:
        results = _run_scope(FAMILY_BAND, run_ts=run_ts, output_root=output_root, config=config)
        write_summaries(results, output_root, run_ts, canary_only=False, preflight=preflight)
        return 0 if len(results) == len(FAMILY_BAND) and all(row.get("passed") for row in results) else 1

    results: list[dict[str, Any]] = []
    if not args.skip_canary:
        canary = _run_scope([(CANARY_FAMILY, CANARY_WAVE, CANARY_COUNTRY)], run_ts=run_ts, output_root=output_root, config=config)
        results.extend(canary)
        if not canary or not canary[0].get("passed"):
            write_summaries(results, output_root, run_ts, canary_only=True, preflight=preflight)
            return 1
    if args.canary_only:
        write_summaries(results, output_root, run_ts, canary_only=True, preflight=preflight)
        return 0

    # Avoid rerunning the canary inside the full allowlist.
    remaining = [row for row in ALL_WAVES if (row[0], row[1]) != (CANARY_FAMILY, CANARY_WAVE)] if not args.skip_canary else list(ALL_WAVES)
    results.extend(_run_scope(remaining, run_ts=run_ts, output_root=output_root, config=config))
    write_summaries(results, output_root, run_ts, canary_only=False, preflight=preflight)
    return 0 if len(results) == len(ALL_WAVES) and all(row.get("passed") for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
