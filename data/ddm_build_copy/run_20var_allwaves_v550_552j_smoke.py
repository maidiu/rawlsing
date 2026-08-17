#!/usr/bin/env python3
"""Governed CLOSED_35 smoke over the integrated V550→V552J producer graph.

Source/wave machine identity is the W01 ``source_family_uid + wave_uid`` pair.
Historical/native/display labels are retained only as compatibility/provenance
attributes at ingress.  This module is the supported smoke implementation; the
legacy ``*_impl`` module is a compatibility re-export and owns no identity
normalization or execution policy.
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
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    BoundaryContractError,
    verify_exact_identity,
    verify_manifest_source_wave_identity_coherence,
)
from data.ddm_build_copy.ddm_pipeline_final_contracts import (
    state_token,
    verify_v550j_producer_manifest,
    verify_v551_producer_manifest,
    verify_v551j_producer_manifest,
    verify_v552_producer_manifest,
    verify_v552j_producer_manifest,
)
from data.ddm_build_copy.ddm_source_wave_identity import (
    SourceWaveIdentity,
    SourceWaveIdentityError,
    closed_35_identities,
    load_identity_registry,
    resolve_source_family_identity,
    resolve_source_wave_identity,
)
from data.ddm_build_copy.ddm_v550_response_relation import (
    AUTO_RESPONSE_RELATION,
    choose_response_relation,
)
from data.ddm_build_copy.ddm_v550_shards import shard_id_for
from data.ddm_build_copy.ddm_v550j_registry_contract import registry_status_is_executable


DEFAULT_ENV_FILE = ROOT / ".env"
DEFAULT_JOINT_REGISTRY = ROOT / "data/ddm_build_copy/manifests/question_family_registry.yaml"
DEFAULT_ASSOCIATION_LANE_REGISTRY = ROOT / "data/ddm_registries/association_lane_registry.yaml"
DEFAULT_ASSOCIATION_THRESHOLD_PROFILES = ROOT / "data/ddm_registries/association_threshold_profiles.yaml"
DEFAULT_FIRST_PASS_AUTHORITY_DIR = ROOT / "data/ddm_build_copy/reports"
DEFAULT_SEMANTIC_AUTHORITY_DIR = ROOT / "data/ddm_build_copy/reports"
DEFAULT_POSITION_CONDITIONING_AUTHORITY_DIR = ROOT / "data/ddm_build_copy/reports"
DEFAULT_DIRECTIONALITY_AUTHORITY_DIR = ROOT / "data/ddm_build_copy/directionality_authority"
DEFAULT_QSM_RELATION = "question_structural_mapping"

COMPILER_SPECS: dict[str, str] = {
    "v550": "data/ddm_build_copy/build_determinicity_wave_shard_v550.py",
    "v550j": "data/ddm_build_copy/compile_v550j_joint_response_patterns.py",
    "v551": "data/ddm_build_copy/compile_v551_relation_evidence_atoms.py",
    "v551j": "data/ddm_build_copy/compile_v551j_joint_evidence_packets.py",
    "v552": "data/ddm_build_copy/compile_v552_structural_ddm.py",
    "v552j": "data/ddm_build_copy/compile_v552j_structural_handoff.py",
}

# Country choices are smoke sampling coordinates, not source/wave identity.
# Every source/wave key is resolved through the UID catalog before it is used.
_COUNTRY_SAMPLES: dict[tuple[str, str], str] = {
    ("Afrobarometer", "R1"): "BF", ("Afrobarometer", "R5"): "SL", ("Afrobarometer", "R9"): "SZ",
    ("Arab Barometer", "I"): "LY", ("Arab Barometer", "II"): "JO", ("Arab Barometer", "V"): "QA", ("Arab Barometer", "VIII"): "LB",
    ("Asian Barometer", "W1"): "PH", ("Asian Barometer", "W4"): "SG", ("Asian Barometer", "W5"): "SG",
    ("EVS", "1981"): "BE", ("EVS", "1990"): "MT", ("EVS", "1999"): "IS", ("EVS", "2008"): "IS", ("EVS", "2017"): "NL",
    ("GSS", "1972"): "US", ("GSS", "1973"): "US", ("GSS", "1984"): "US", ("GSS", "1993"): "US",
    ("GSS", "2002"): "US", ("GSS", "2010"): "US", ("GSS", "2016"): "US", ("GSS", "2024"): "US",
    ("Latinobarómetro", "1995"): "BR", ("Latinobarómetro", "2011"): "GT", ("Latinobarómetro", "2024"): "GT",
    ("LiTS", "2006"): "BY", ("LiTS", "II"): "SE", ("LiTS", "III"): "AL", ("LiTS", "IV"): "MA",
    ("South Asia", "W1"): "IN", ("South Asia", "W2"): "BD",
    ("WVS", "W1"): "SE", ("WVS", "W4"): "DZ", ("WVS", "W7"): "RS",
}


@dataclass(frozen=True)
class RuntimeConfig:
    repo_root: Path = ROOT
    env_file: Path = DEFAULT_ENV_FILE
    db_url: str = ""
    qsm_relation: str = DEFAULT_QSM_RELATION
    response_option_map: Path | None = None
    joint_registry_paths: tuple[Path, ...] = (DEFAULT_JOINT_REGISTRY,)
    association_lane_registry: Path | None = DEFAULT_ASSOCIATION_LANE_REGISTRY
    association_threshold_profiles: Path | None = DEFAULT_ASSOCIATION_THRESHOLD_PROFILES
    first_pass_authority_dir: Path = DEFAULT_FIRST_PASS_AUTHORITY_DIR
    semantic_authority_dir: Path = DEFAULT_SEMANTIC_AUTHORITY_DIR
    position_conditioning_authority_dir: Path = DEFAULT_POSITION_CONDITIONING_AUTHORITY_DIR
    directionality_authority_dir: Path = DEFAULT_DIRECTIONALITY_AUTHORITY_DIR
    association_mode: str = "off"
    joint_mode: str = "auto"
    readiness_mode: str = "full"
    diagnostic_continue: bool = False
    response_long_relation: str = AUTO_RESPONSE_RELATION


DEFAULT_CONFIG = RuntimeConfig()
_ORIGINAL_PARSE_ARGS = None  # compatibility hook for pre-SWID importers/tests


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"", "nan", "none", "null", "unknown", "unresolved"} else text


def _validate_relation_identifier(value: str, label: str) -> str:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)?", value or ""):
        raise ValueError(f"invalid_{label}_identifier:{value!r}")
    return value


def runtime_compiler_paths(config: RuntimeConfig = DEFAULT_CONFIG) -> dict[str, Path]:
    """Return the exact compiler entrypoints used by this smoke."""
    return {stage: config.repo_root / rel for stage, rel in COMPILER_SPECS.items()}


def _country_by_uid() -> dict[str, str]:
    result: dict[str, str] = {}
    for (source, wave), country in _COUNTRY_SAMPLES.items():
        identity = resolve_source_wave_identity(source, wave, require_closed_35=True)
        if identity.wave_uid in result and result[identity.wave_uid] != country:
            raise RuntimeError(f"conflicting smoke country for {identity.wave_uid}")
        result[identity.wave_uid] = country
    return result


_COUNTRY_BY_WAVE_UID = _country_by_uid()


def _catalog_scope() -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for identity in closed_35_identities():
        country = _COUNTRY_BY_WAVE_UID.get(identity.wave_uid, "")
        if not country:
            raise RuntimeError(f"smoke country missing for governed wave_uid={identity.wave_uid}")
        rows.append((identity.canonical_display_source, identity.canonical_display_wave, country))
    if len(rows) != 35:
        raise RuntimeError(f"CLOSED_35 catalog count mismatch:{len(rows)}")
    return rows


ALL_WAVES = _catalog_scope()
FAMILY_BAND = [
    next(row for row in ALL_WAVES if row[0] == family)
    for family in sorted({family for family, _, _ in ALL_WAVES})
]
CANARY_FAMILY, CANARY_WAVE, CANARY_COUNTRY = next(
    row for row in ALL_WAVES if row[0] == "GSS" and row[1] == "2010"
)


def resolve_smoke_identity(source: str, wave: str, country: str = "") -> tuple[SourceWaveIdentity, str]:
    """Resolve one smoke scope through the single governed identity authority."""
    identity = resolve_source_wave_identity(source, wave, require_closed_35=True)
    resolved_country = _clean(country) or _COUNTRY_BY_WAVE_UID.get(identity.wave_uid, "")
    if not resolved_country:
        raise BoundaryContractError(f"SMOKE_COUNTRY_REQUIRED:{identity.uid_key}")
    return identity, resolved_country


def run_id_for_identity(identity: SourceWaveIdentity, run_ts: str) -> str:
    return f"{identity.uid_native_physical_token}_{run_ts}"


def validate_explicit_scope(waves: Iterable[tuple[str, str, str]] = ALL_WAVES) -> list[str]:
    rows = list(waves)
    issues: list[str] = []
    seen: set[tuple[str, str]] = set()
    for source, wave, country in rows:
        try:
            identity, _ = resolve_smoke_identity(source, wave, country)
        except Exception as exc:
            issues.append(f"scope_identity_invalid:{source}|{wave}:{type(exc).__name__}:{exc}")
            continue
        pair = (identity.source_family_uid, identity.wave_uid)
        if pair in seen:
            issues.append(f"duplicate_source_wave_uid:{identity.uid_key}")
        seen.add(pair)
    if len(rows) == 35:
        governed = {(i.source_family_uid, i.wave_uid) for i in closed_35_identities()}
        if seen != governed:
            missing = sorted(governed - seen)
            extra = sorted(seen - governed)
            issues.append(f"governed_scope_uid_mismatch:missing={missing}:extra={extra}")
    return issues


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _registry_scope_matches(
    payload: Mapping[str, Any],
    family_cfg: Mapping[str, Any],
    requested: SourceWaveIdentity,
) -> bool:
    source_label = _clean(family_cfg.get("source_family") or payload.get("source_family"))
    aggregate = source_label.lower().replace("_", " ").strip() in {
        "", "all", "all scopes", "all layer1 scopes", "alllayer1scopes",
    }
    if not aggregate:
        try:
            family_identity = resolve_source_family_identity(source_label)
        except SourceWaveIdentityError:
            return False
        if family_identity.source_family_uid != requested.source_family_uid:
            return False
    eligible = list(family_cfg.get("eligible_waves") or [])
    if not eligible:
        return True
    for alias in eligible:
        try:
            candidate = resolve_source_wave_identity(
                requested.canonical_display_source, alias, require_closed_35=False
            )
        except SourceWaveIdentityError:
            continue
        if candidate.wave_uid == requested.wave_uid:
            return True
    return False


def _registry_var_codes(family_cfg: Mapping[str, Any]) -> list[str]:
    codes: list[str] = []
    groups = family_cfg.get("item_role_groups") or {}
    if isinstance(groups, Mapping):
        for rows in groups.values():
            for row in rows or []:
                if isinstance(row, Mapping):
                    code = _clean(row.get("var_code"))
                    if code and code not in codes:
                        codes.append(code)
    return codes


def resolve_joint_authority(
    config: RuntimeConfig,
    family: str,
    wave: str,
    selected_vars: Iterable[str] | None = None,
) -> dict[str, Any]:
    identity, _ = resolve_smoke_identity(family, wave)
    selected = {_clean(value).upper() for value in selected_vars or [] if _clean(value)}
    matches: list[dict[str, Any]] = []
    rejected_statuses: list[dict[str, str]] = []
    for path in config.joint_registry_paths:
        payload = _load_yaml(path)
        if not payload:
            continue
        status = _clean(payload.get("status"))
        if not registry_status_is_executable(status):
            rejected_statuses.append({"path": str(path), "registry_status": status})
            continue
        for family_cfg in payload.get("families") or []:
            if not isinstance(family_cfg, Mapping) or not _registry_scope_matches(payload, family_cfg, identity):
                continue
            codes = _registry_var_codes(family_cfg)
            overlap = [code for code in codes if not selected or code.upper() in selected]
            matches.append(
                {
                    "path": str(path),
                    "payload_hash": hashlib.sha256(
                        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
                    ).hexdigest(),
                    "family_id": _clean(family_cfg.get("family_id")),
                    "candidate_vars": codes,
                    "selected_overlap": overlap,
                    "registry_status": status,
                }
            )
    if not matches:
        return {
            "applicable": False,
            "coverage_state": "NOT_APPLICABLE" if not rejected_statuses else "APPLICABLE_UNRESOLVED",
            "downstream_permission_status": "NOT_APPLICABLE" if not rejected_statuses else "DENY",
            "reason": "no_explicit_joint_registry_for_source_wave_uid" if not rejected_statuses else "matching_registry_not_executable",
            "registry_path": "",
            "source_family_uid": identity.source_family_uid,
            "wave_uid": identity.wave_uid,
            "rejected_statuses": rejected_statuses,
        }
    payload_hashes = {row["payload_hash"] for row in matches}
    if len(payload_hashes) > 1:
        raise BoundaryContractError(
            f"SMOKE_JOINT_AUTHORITY_CONFLICT:{identity.uid_key}:{sorted(payload_hashes)}"
        )
    chosen = matches[0]
    if selected and not any(row["selected_overlap"] for row in matches):
        return {
            "applicable": False,
            "coverage_state": "NOT_APPLICABLE",
            "downstream_permission_status": "NOT_APPLICABLE",
            "reason": "joint_registry_exists_but_selected_slice_has_no_family_items",
            "registry_path": chosen["path"],
            "source_family_uid": identity.source_family_uid,
            "wave_uid": identity.wave_uid,
        }
    return {
        "applicable": True,
        "coverage_state": "PRESENT",
        "downstream_permission_status": "ALLOW",
        "reason": "",
        "registry_path": chosen["path"],
        "registry_status": chosen["registry_status"],
        "family_ids": sorted({row["family_id"] for row in matches if row["family_id"]}),
        "candidate_vars": sorted({code for row in matches for code in row["candidate_vars"]}),
        "source_family_uid": identity.source_family_uid,
        "wave_uid": identity.wave_uid,
    }


def summarize_joint_authority_coverage(
    config: RuntimeConfig,
    waves: Iterable[tuple[str, str, str]] = ALL_WAVES,
) -> dict[str, Any]:
    typed: list[dict[str, Any]] = []
    for source, wave, country in waves:
        authority = resolve_joint_authority(config, source, wave)
        identity, resolved_country = resolve_smoke_identity(source, wave, country)
        typed.append(
            {
                "source": identity.canonical_display_source,
                "wave": identity.canonical_display_wave,
                "country_code": resolved_country,
                "source_family_uid": identity.source_family_uid,
                "wave_uid": identity.wave_uid,
                "coverage_state": authority["coverage_state"],
                "downstream_permission_status": authority["downstream_permission_status"],
                "reason": authority.get("reason", ""),
                "registry_path": authority.get("registry_path", ""),
            }
        )
    return {
        "required_scope_count": len(typed),
        "typed_scopes": typed,
        "applicable_scopes": [row for row in typed if row["coverage_state"] == "PRESENT"],
        "not_applicable_scopes": [row for row in typed if row["coverage_state"] == "NOT_APPLICABLE"],
        "coverage_debt_scopes": [row for row in typed if row["coverage_state"] == "APPLICABLE_UNRESOLVED"],
    }


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


def _db_url(config: RuntimeConfig) -> str:
    return config.db_url or os.environ.get("DATABASE_URL", "") or _load_env_file(config.env_file).get("DATABASE_URL", "")


def inspect_database_contract(config: RuntimeConfig, db_url: str) -> dict[str, Any]:
    result: dict[str, Any] = {"checked": False, "passed": False, "relations": {}, "error": ""}
    if not db_url or importlib.util.find_spec("psycopg2") is None:
        return result
    try:
        import psycopg2

        qsm = _validate_relation_identifier(config.qsm_relation, "qsm_relation")
        with psycopg2.connect(db_url, connect_timeout=10) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT to_regclass(%s)::text", (qsm,))
                qsm_resolved = cur.fetchone()[0]
                qsm_columns: set[str] = set()
                if qsm_resolved:
                    cur.execute(
                        """SELECT attname FROM pg_attribute
                           WHERE attrelid = to_regclass(%s) AND attnum > 0 AND NOT attisdropped""",
                        (qsm,),
                    )
                    qsm_columns = {str(row[0]) for row in cur.fetchall()}
                qsm_required = {"source_family_uid", "wave_uid", "var_code"}
                result["relations"]["qsm_relation"] = {
                    "requested": qsm,
                    "resolved": qsm_resolved or "",
                    "missing_columns": sorted(qsm_required - qsm_columns),
                }

                cur.execute(
                    """SELECT table_schema || '.' || table_name
                       FROM information_schema.views
                       WHERE table_name IN ('v_ddm_response_long_facet_ready_authority', 'v_ddm_response_long_facet_ready')
                       ORDER BY table_schema, table_name"""
                )
                available = {str(row[0]) for row in cur.fetchall()}
                try:
                    response = choose_response_relation(available, config.response_long_relation)
                    cur.execute(
                        """SELECT attname FROM pg_attribute
                           WHERE attrelid = to_regclass(%s) AND attnum > 0 AND NOT attisdropped""",
                        (response,),
                    )
                    columns = {str(row[0]) for row in cur.fetchall()}
                    required = {"respondent_id", "source_family_uid", "wave_uid", "country_code", "var_code"}
                    result["relations"]["response_long_relation"] = {
                        "requested": config.response_long_relation,
                        "resolved": response,
                        "missing_columns": sorted(required - columns),
                    }
                except Exception as exc:
                    result["relations"]["response_long_relation"] = {
                        "requested": config.response_long_relation,
                        "resolved": "",
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


def _select_question_variables(
    family: str,
    wave: str,
    country: str,
    seed: int = 42,
    *,
    config: RuntimeConfig = DEFAULT_CONFIG,
) -> list[str]:
    import psycopg2

    identity, _ = resolve_smoke_identity(family, wave, country)
    db_url = _db_url(config)
    if not db_url:
        raise RuntimeError("DATABASE_URL is required to select the 20-variable slice")
    qsm = _validate_relation_identifier(config.qsm_relation, "qsm_relation")
    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""SELECT DISTINCT var_code,
                           COALESCE(relation_axis_id, ''),
                           COALESCE(structural_domain_id, ''),
                           COALESCE(evidence_kind, '')
                    FROM {qsm}
                    WHERE source_family_uid = %s
                      AND wave_uid = %s
                    ORDER BY var_code""",
                (identity.source_family_uid, identity.wave_uid),
            )
            rows = [
                (str(code), str(axis or ""), str(domain or ""), str(evidence or ""))
                for code, axis, domain, evidence in cur.fetchall()
            ]
    if not rows:
        return []
    rng = random.Random(seed)
    authority = resolve_joint_authority(config, family, wave)
    selected: list[str] = []
    available = {code.upper(): code for code, *_ in rows}
    if authority.get("applicable"):
        for code in authority.get("candidate_vars") or []:
            if code.upper() in available and available[code.upper()] not in selected:
                selected.append(available[code.upper()])
            if len(selected) >= 6:
                break
    relation_rows = [code for code, axis, _, evidence in rows if axis or "relation" in evidence.lower()]
    structural_rows = [code for code, _, domain, _ in rows if domain]
    for pool, target in ((relation_rows, 8), (structural_rows, 6)):
        choices = [code for code in pool if code not in selected]
        rng.shuffle(choices)
        selected.extend(choices[: max(0, min(target, 20 - len(selected)))])
    remaining = [code for code, *_ in rows if code not in selected]
    rng.shuffle(remaining)
    selected.extend(remaining[: max(0, 20 - len(selected))])
    rng.shuffle(selected)
    return selected[:20]


def _build_question_filter(
    family: str,
    wave: str,
    country: str,
    seed: int,
    *,
    config: RuntimeConfig,
    filter_root: Path,
) -> tuple[str, list[str]]:
    selected = _select_question_variables(family, wave, country, seed=seed, config=config)
    if not selected:
        return "", []
    identity, _ = resolve_smoke_identity(family, wave, country)
    filter_root.mkdir(parents=True, exist_ok=True)
    path = filter_root / f"{identity.uid_native_physical_token}.json"
    path.write_text(json.dumps({"question_ids": selected, "var_codes": selected}, indent=2) + "\n", encoding="utf-8")
    return str(path), selected


def run_preflight(
    config: RuntimeConfig,
    waves: Iterable[tuple[str, str, str]] = ALL_WAVES,
) -> dict[str, Any]:
    rows = list(waves)
    blockers = validate_explicit_scope(rows)
    warnings: list[str] = []
    required_modules = ("pandas", "pyarrow", "psycopg2", "yaml")
    module_status = {name: importlib.util.find_spec(name) is not None for name in required_modules}
    blockers.extend(f"missing_python_module:{name}" for name, present in module_status.items() if not present)

    compiler_paths = runtime_compiler_paths(config)
    for stage, path in compiler_paths.items():
        if not path.exists():
            blockers.append(f"missing_runtime_compiler:{stage}:{path}")

    db_url = _db_url(config)
    if not db_url:
        blockers.append("missing_database_url")
    database_contract = inspect_database_contract(config, db_url)
    if database_contract.get("checked") and not database_contract.get("passed"):
        blockers.append("database_uid_contract_not_ready")

    for label, directory in (
        ("first_pass_authority_dir", config.first_pass_authority_dir),
        ("semantic_authority_dir", config.semantic_authority_dir),
        ("position_conditioning_authority_dir", config.position_conditioning_authority_dir),
        ("directionality_authority_dir", config.directionality_authority_dir),
    ):
        if not directory.exists():
            blockers.append(f"missing_runtime_authority_directory:{label}:{directory}")

    joint = summarize_joint_authority_coverage(config, rows)
    debt = joint["coverage_debt_scopes"]
    not_applicable = joint["not_applicable_scopes"]
    if debt:
        blockers.append(f"joint_authority_unresolved_for_scopes:{len(debt)}")
    if config.joint_mode == "required" and not_applicable:
        blockers.append(f"joint_authority_not_applicable_for_required_scopes:{len(not_applicable)}")
    elif config.joint_mode == "auto" and not_applicable:
        warnings.append(f"joint_branch_not_applicable_base_spine_only:{len(not_applicable)}")

    return {
        "passed": not blockers,
        "blockers": blockers,
        "warnings": warnings,
        "module_status": module_status,
        "db_url_present": bool(db_url),
        "database_contract": database_contract,
        "runtime_compilers": {stage: str(path) for stage, path in compiler_paths.items()},
        "joint_authority_coverage": joint,
        "requested_scope_count": len(rows),
        "requested_scopes": [
            {
                "source": resolve_smoke_identity(source, wave, country)[0].canonical_display_source,
                "wave": resolve_smoke_identity(source, wave, country)[0].canonical_display_wave,
                "country_code": resolve_smoke_identity(source, wave, country)[1],
                "source_family_uid": resolve_smoke_identity(source, wave, country)[0].source_family_uid,
                "wave_uid": resolve_smoke_identity(source, wave, country)[0].wave_uid,
            }
            for source, wave, country in rows
        ],
    }


def _run(cmd: list[str], *, config: RuntimeConfig, timeout_sec: int) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(config.repo_root)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if config.db_url:
        env["DATABASE_URL"] = config.db_url
    env["DDM_QSM_RELATION"] = config.qsm_relation
    env["DDM_RESPONSE_LONG_RELATION"] = config.response_long_relation
    started = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
            cwd=config.repo_root,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        return {
            "exit_code": proc.returncode,
            "stdout_tail": (proc.stdout or "")[-4000:],
            "stderr_tail": (proc.stderr or "")[-4000:],
            "elapsed": round(time.monotonic() - started, 1),
            "command": " ".join(str(part) for part in cmd),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "exit_code": -1,
            "stdout_tail": (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": "TIMEOUT",
            "elapsed": round(time.monotonic() - started, 1),
            "command": " ".join(str(part) for part in cmd),
        }


def _compiler(stage: str, config: RuntimeConfig) -> str:
    return str(runtime_compiler_paths(config)[stage])


def run_v550_shard(
    run_id: str,
    shard_id: str,
    family: str,
    wave: str,
    country: str,
    filter_path: str,
    output_root: str,
    registry_path: str | None,
    config: RuntimeConfig,
) -> dict[str, Any]:
    identity, country = resolve_smoke_identity(family, wave, country)
    cmd = [
        sys.executable, _compiler("v550", config),
        "--run-id", run_id,
        "--shard-id", shard_id,
        "--source", identity.canonical_display_source,
        "--wave", identity.canonical_display_wave,
        "--canonical-wave", identity.canonical_display_wave,
        "--country", country,
        "--output-root", output_root,
        "--question-filter-file", filter_path,
        "--limit-questions", "20",
        "--env-file", str(config.env_file),
        "--response-long-relation", config.response_long_relation,
        "--first-pass-authority-dir", str(config.first_pass_authority_dir),
        "--semantic-authority-dir", str(config.semantic_authority_dir),
        "--position-conditioning-authority-dir", str(config.position_conditioning_authority_dir),
        "--directionality-authority-dir", str(config.directionality_authority_dir),
        "--v550-prepared-substrate-mode", "country",
        "--finalize-source", "memory",
        "--no-write-csv",
        "--write-parquet",
    ]
    if registry_path:
        cmd += ["--shared-respondent-substrate-mode", "write", "--joint-configuration-registry-path", registry_path]
    if config.db_url:
        cmd += ["--db-url", config.db_url]
    if config.response_option_map:
        cmd += ["--response-option-map", str(config.response_option_map)]
    cmd.append("--full-readiness" if config.readiness_mode == "full" else "--allow-launch-ready-fallback")
    return _run(cmd, config=config, timeout_sec=3600)


def run_v550j(
    shard_dir: Path,
    filter_path: str,
    output_root: Path,
    registry_path: str,
    response_map_path: Path,
    substrate_path: Path,
    substrate_manifest_path: Path,
    config: RuntimeConfig,
) -> dict[str, Any]:
    cmd = [
        sys.executable, _compiler("v550j", config),
        "--v550-shard-dir", str(shard_dir),
        "--output-root", str(output_root),
        "--registry-path", registry_path,
        "--response-option-map", str(response_map_path),
        "--question-filter-file", filter_path,
        "--env-file", str(config.env_file),
        "--association-mode", config.association_mode,
        "--with-diagnostics",
        "--v550j-substrate-mode", "prepared_required",
        "--prepared-substrate-path", str(substrate_path),
        "--prepared-substrate-manifest-path", str(substrate_manifest_path),
        "--forbid-database-access",
        "--no-write-csv",
        "--write-parquet",
    ]
    if config.association_mode != "off":
        if config.association_lane_registry:
            cmd += ["--association-lane-registry-path", str(config.association_lane_registry)]
        if config.association_threshold_profiles:
            cmd += ["--association-threshold-profiles-path", str(config.association_threshold_profiles)]
    return _run(cmd, config=config, timeout_sec=1800)


def run_v551(run_id: str, bridge_path: Path, output_root: Path, config: RuntimeConfig) -> dict[str, Any]:
    return _run(
        [
            sys.executable, _compiler("v551", config),
            "--run-id", run_id,
            "--bridge-path", str(bridge_path),
            "--output-root", str(output_root),
            "--v551-compile-mode", "canonical",
            "--write-parquet",
            "--no-write-csv",
        ],
        config=config,
        timeout_sec=1800,
    )


def run_v552(run_id: str, v551_manifest_path: Path, output_root: Path, config: RuntimeConfig) -> dict[str, Any]:
    return _run(
        [
            sys.executable, _compiler("v552", config),
            "--run-id", run_id,
            "--v551-manifest-path", str(v551_manifest_path),
            "--output-root", str(output_root),
            "--strict-handoff",
            "--write-parquet",
            "--no-write-csv",
        ],
        config=config,
        timeout_sec=1800,
    )


def run_v551j(
    run_id: str,
    v551_root: Path,
    v550j_joint_root: Path,
    registry_path: str,
    output_root: Path,
    config: RuntimeConfig,
) -> dict[str, Any]:
    return _run(
        [
            sys.executable, _compiler("v551j", config),
            "--run-id", run_id,
            "--v551-atoms-path", str(v551_root / "relation_evidence_atoms.parquet"),
            "--v551-manifest-path", str(v551_root / "manifest.json"),
            "--v550j-pattern-index-path", str(v550j_joint_root / "joint_response_pattern_index.parquet"),
            "--v550j-pattern-item-index-path", str(v550j_joint_root / "joint_response_pattern_item_index.parquet"),
            "--v550j-relation-signature-path", str(v550j_joint_root / "joint_pattern_relation_signature.parquet"),
            "--v550j-manifest-path", str(v550j_joint_root / "v550j_manifest.json"),
            "--v550j-readiness-report-path", str(v550j_joint_root / "v550j_source_wave_readiness_report.json"),
            "--v550j-meaning-summary-path", str(v550j_joint_root / "joint_pattern_meaning_summary.parquet"),
            "--registry-path", registry_path,
            "--output-root", str(output_root),
            "--emit-review-surface",
            "--emit-certified-index",
            "--strict",
            "--write-parquet",
            "--no-write-csv",
        ],
        config=config,
        timeout_sec=1800,
    )


def run_v552j(
    run_id: str,
    v551j_manifest_path: Path,
    v552_manifest_path: Path,
    output_root: Path,
    config: RuntimeConfig,
) -> dict[str, Any]:
    return _run(
        [
            sys.executable, _compiler("v552j", config),
            "--run-id", run_id,
            "--v551j-manifest-path", str(v551j_manifest_path),
            "--v552-manifest-path", str(v552_manifest_path),
            "--output-root", str(output_root),
            "--write-parquet",
            "--no-write-csv",
        ],
        config=config,
        timeout_sec=1800,
    )


def _verification_gate(verified: Any) -> dict[str, Any]:
    payload = verified.manifest_payload
    return {
        "manifest_path": verified.manifest_path,
        "contract_version": verified.state.contract_version,
        "schema_version": _clean(payload.get("schema_version")),
        "compiler_version": _clean(payload.get("compiler_version")),
        "run_integrity_status": verified.state.run_integrity_status,
        "evidence_status": verified.state.evidence_status,
        "downstream_permission_status": verified.state.downstream_permission_status,
        "state": state_token(verified),
        "identity": dict(verified.identity),
        "integrity_passed": True,
        "passed": True,
        "failure_reason": "",
    }


def _v550_gate(
    manifest_path: Path,
    *,
    run_id: str,
    shard_id: str,
    identity: SourceWaveIdentity,
) -> dict[str, Any]:
    if not manifest_path.exists() and manifest_path.with_name("shard_manifest.json").exists():
        manifest_path = manifest_path.with_name("shard_manifest.json")
    if not manifest_path.exists():
        return {"passed": False, "failure_reason": "missing_v550_manifest"}
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    try:
        coherence = verify_manifest_source_wave_identity_coherence(
            payload,
            expected_source_family_uid=identity.source_family_uid,
            expected_wave_uid=identity.wave_uid,
        )
        verify_exact_identity(
            payload,
            run_id=run_id,
            shard_id=shard_id,
            source_family_uid=identity.source_family_uid,
            wave_uid=identity.wave_uid,
        )
    except BoundaryContractError as exc:
        return {"passed": False, "failure_reason": f"v550_identity_invalid:{exc}"}
    rows = int(payload.get("response_option_map_row_count") or (payload.get("rows_by_table") or {}).get("response_option_map") or 0)
    passed = bool(payload.get("success")) and rows > 0
    return {
        "passed": passed,
        "failure_reason": "" if passed else "v550_not_successful_or_response_map_empty",
        "source_family_uid": coherence.source_family_uid,
        "wave_uid": coherence.wave_uid,
        "run_id": run_id,
        "shard_id": shard_id,
        "response_option_map_row_count": rows,
    }


def _fail(result: dict[str, Any], stage: str, reason: str) -> dict[str, Any]:
    result["failure_stage"] = stage
    result["functional_failure_reason"] = reason
    result["passed"] = False
    return result


def _stage_result(raw: dict[str, Any], gate: dict[str, Any] | None = None) -> dict[str, Any]:
    row = {
        "exit_code": raw.get("exit_code", -99),
        "elapsed": raw.get("elapsed", 0),
        "process_pass": raw.get("exit_code") == 0,
    }
    if raw.get("stderr_tail"):
        row["stderr_tail"] = raw["stderr_tail"]
    if gate is not None:
        row["boundary_gate"] = gate
        row["boundary_pass"] = bool(gate.get("passed"))
    return row


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
    identity, country = resolve_smoke_identity(family, wave, country)
    run_id = run_id_for_identity(identity, run_ts)
    shard_id = shard_id_for(identity.canonical_display_source, identity.canonical_display_wave)
    result: dict[str, Any] = {
        "survey_family": identity.canonical_display_source,
        "wave_id": identity.canonical_display_wave,
        "country": country,
        "source_family_uid": identity.source_family_uid,
        "wave_uid": identity.wave_uid,
        "run_id": run_id,
        "shard_id": shard_id,
        "selected_variable_count": len(selected_vars),
        "selected_variables": selected_vars,
        "stages": {},
        "functional_checks": {},
        "joint_branch": {"traversed": False},
        "base_spine_passed": False,
        "full_chain_passed": False,
        "acceptance_boundary": "none",
        "passed": False,
    }
    output = Path(output_root)
    shard_dir = output / "v550/shard_runs" / run_id / shard_id
    authority = resolve_joint_authority(config, family, wave, selected_vars)
    result["joint_branch"]["authority"] = authority
    registry_path = authority.get("registry_path") if authority.get("applicable") and config.joint_mode != "off" else None

    raw = run_v550_shard(run_id, shard_id, family, wave, country, filter_path, str(output / "v550"), registry_path, config)
    if raw["exit_code"] != 0:
        result["stages"]["v550"] = _stage_result(raw)
        return _fail(result, "v550_process", raw.get("stderr_tail") or "v550_nonzero_exit")
    v550_gate = _v550_gate(shard_dir / "manifest.json", run_id=run_id, shard_id=shard_id, identity=identity)
    result["stages"]["v550"] = _stage_result(raw, v550_gate)
    result["functional_checks"]["v550"] = v550_gate
    if not v550_gate["passed"]:
        return _fail(result, "v550_boundary", v550_gate["failure_reason"])

    bridge = shard_dir / "bridge/v551_bridge_index.parquet"
    response_map = shard_dir / "core/response_option_map.parquet"
    if not bridge.exists() or not response_map.exists():
        return _fail(result, "v550_outputs", "missing_bridge_or_response_option_map")

    raw = run_v551(run_id, bridge, output / "v551", config)
    if raw["exit_code"] != 0:
        result["stages"]["v551"] = _stage_result(raw)
        return _fail(result, "v551_process", raw.get("stderr_tail") or "v551_nonzero_exit")
    v551_root = output / "v551" / run_id
    v551_manifest = v551_root / "manifest.json"
    try:
        gate = _verification_gate(
            verify_v551_producer_manifest(
                v551_manifest,
                run_id=run_id,
                source=identity.canonical_display_source,
                wave=identity.canonical_display_wave,
                country_code=country,
                shard_id=shard_id,
                bridge_path=bridge,
            )
        )
    except BoundaryContractError as exc:
        gate = {"passed": False, "failure_reason": f"v551_boundary_invalid:{exc}"}
    result["stages"]["v551"] = _stage_result(raw, gate)
    result["functional_checks"]["v551"] = gate
    if not gate["passed"]:
        return _fail(result, "v551_boundary", gate["failure_reason"])

    raw = run_v552(run_id, v551_manifest, output / "v552", config)
    if raw["exit_code"] != 0:
        result["stages"]["v552"] = _stage_result(raw)
        return _fail(result, "v552_process", raw.get("stderr_tail") or "v552_nonzero_exit")
    v552_root = output / "v552" / run_id
    v552_manifest = v552_root / "manifest.json"
    try:
        gate = _verification_gate(
            verify_v552_producer_manifest(
                v552_manifest,
                run_id=run_id,
                source=identity.canonical_display_source,
                wave=identity.canonical_display_wave,
                country_code=country,
                shard_id=shard_id,
                v551_manifest_path=v551_manifest,
            )
        )
    except BoundaryContractError as exc:
        gate = {"passed": False, "failure_reason": f"v552_boundary_invalid:{exc}"}
    result["stages"]["v552"] = _stage_result(raw, gate)
    result["functional_checks"]["v552"] = gate
    if not gate["passed"]:
        return _fail(result, "v552_boundary", gate["failure_reason"])
    result["base_spine_passed"] = True
    result["acceptance_boundary"] = "typed_base_spine"

    if config.joint_mode == "off" or not authority.get("applicable"):
        result["joint_branch"].update(
            traversed=False,
            status="not_traversed",
            reason=authority.get("reason") or "joint_mode_off",
        )
        if config.joint_mode == "required":
            return _fail(result, "joint_authority", result["joint_branch"]["reason"])
        result["passed"] = True
        return result

    substrate_manifests = list(
        (shard_dir / "checkpoints/respondent_substrate").rglob("v550_shared_respondent_substrate_manifest.json")
    )
    if len(substrate_manifests) != 1:
        return _fail(result, "shared_respondent_substrate", f"expected_one_substrate_manifest_actual_{len(substrate_manifests)}")
    substrate_manifest = substrate_manifests[0]
    substrate = substrate_manifest.with_name("v550_shared_respondent_substrate.parquet")
    if not substrate.exists():
        return _fail(result, "shared_respondent_substrate", "missing_substrate_parquet")

    raw = run_v550j(
        shard_dir,
        filter_path,
        output / "v550j",
        str(authority["registry_path"]),
        response_map,
        substrate,
        substrate_manifest,
        config,
    )
    joint_root = output / "v550j/runs" / run_id / shard_id / "joint_patterns"
    if raw["exit_code"] != 0:
        result["stages"]["v550j"] = _stage_result(raw)
        return _fail(result, "v550j_process", raw.get("stderr_tail") or "v550j_nonzero_exit")
    try:
        gate = _verification_gate(
            verify_v550j_producer_manifest(
                joint_root / "v550j_manifest.json",
                joint_root / "v550j_source_wave_readiness_report.json",
                run_id=run_id,
                source=identity.canonical_display_source,
                wave=identity.canonical_display_wave,
                shard_id=shard_id,
            )
        )
    except BoundaryContractError as exc:
        gate = {"passed": False, "failure_reason": f"v550j_boundary_invalid:{exc}"}
    result["stages"]["v550j"] = _stage_result(raw, gate)
    result["functional_checks"]["v550j"] = gate
    if not gate["passed"]:
        return _fail(result, "v550j_boundary", gate["failure_reason"])

    raw = run_v551j(run_id, v551_root, joint_root, str(authority["registry_path"]), output / "v551j", config)
    v551j_manifest = output / "v551j" / run_id / "manifest/manifest.json"
    if raw["exit_code"] != 0:
        result["stages"]["v551j"] = _stage_result(raw)
        return _fail(result, "v551j_process", raw.get("stderr_tail") or "v551j_nonzero_exit")
    try:
        gate = _verification_gate(
            verify_v551j_producer_manifest(
                v551j_manifest,
                run_id=run_id,
                source=identity.canonical_display_source,
                wave=identity.canonical_display_wave,
                country_code=country,
                shard_id=shard_id,
                v551_manifest_path=v551_manifest,
                v550j_manifest_path=joint_root / "v550j_manifest.json",
            )
        )
    except BoundaryContractError as exc:
        gate = {"passed": False, "failure_reason": f"v551j_boundary_invalid:{exc}"}
    result["stages"]["v551j"] = _stage_result(raw, gate)
    result["functional_checks"]["v551j"] = gate
    if not gate["passed"]:
        return _fail(result, "v551j_boundary", gate["failure_reason"])

    raw = run_v552j(run_id, v551j_manifest, v552_manifest, output / "v552j", config)
    v552j_manifest = output / "v552j" / run_id / "manifest.json"
    if raw["exit_code"] != 0:
        result["stages"]["v552j"] = _stage_result(raw)
        return _fail(result, "v552j_process", raw.get("stderr_tail") or "v552j_nonzero_exit")
    try:
        gate = _verification_gate(
            verify_v552j_producer_manifest(
                v552j_manifest,
                run_id=run_id,
                source=identity.canonical_display_source,
                wave=identity.canonical_display_wave,
                country_code=country,
                shard_id=shard_id,
                v551j_manifest_path=v551j_manifest,
                v552_manifest_path=v552_manifest,
            )
        )
    except BoundaryContractError as exc:
        gate = {"passed": False, "failure_reason": f"v552j_boundary_invalid:{exc}"}
    result["stages"]["v552j"] = _stage_result(raw, gate)
    result["functional_checks"]["v552j"] = gate
    if not gate["passed"]:
        return _fail(result, "v552j_boundary", gate["failure_reason"])

    result["joint_branch"].update(
        traversed=True,
        status="typed_graph_verified",
        reason=gate["state"],
    )
    result["full_chain_passed"] = True
    result["acceptance_boundary"] = "full_v550_to_v552j_typed_graph"
    result["passed"] = True
    return result


def write_summaries(
    results: list[dict[str, Any]],
    output_root: str,
    run_ts: str,
    canary_only: bool,
    preflight: dict[str, Any] | None = None,
) -> None:
    report = Path(output_root) / "reports"
    report.mkdir(parents=True, exist_ok=True)
    fields = [
        "survey_family", "wave_id", "source_family_uid", "wave_uid", "country",
        "base_spine_passed", "joint_branch_traversed", "full_chain_passed",
        "acceptance_boundary", "passed", "failure_stage", "functional_failure_reason",
    ]
    with (report / "smoke_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in results:
            writer.writerow(
                {
                    "survey_family": row.get("survey_family", ""),
                    "wave_id": row.get("wave_id", ""),
                    "source_family_uid": row.get("source_family_uid", ""),
                    "wave_uid": row.get("wave_uid", ""),
                    "country": row.get("country", ""),
                    "base_spine_passed": row.get("base_spine_passed", False),
                    "joint_branch_traversed": bool((row.get("joint_branch") or {}).get("traversed")),
                    "full_chain_passed": row.get("full_chain_passed", False),
                    "acceptance_boundary": row.get("acceptance_boundary", "none"),
                    "passed": row.get("passed", False),
                    "failure_stage": row.get("failure_stage", ""),
                    "functional_failure_reason": row.get("functional_failure_reason", ""),
                }
            )
    payload = {
        "run_ts": run_ts,
        "scope": "canary" if canary_only else "CLOSED_35_UID_CATALOG",
        "base_spine": ["v550", "v551", "v552"],
        "j_branch": ["v550j", "v551j", "v552j"],
        "preflight": preflight or {},
        "results": results,
    }
    (report / "smoke_summary.json").write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")

    total = len(results)
    base = sum(bool(row.get("base_spine_passed")) for row in results)
    traversed = sum(bool((row.get("joint_branch") or {}).get("traversed")) for row in results)
    full = sum(bool(row.get("full_chain_passed")) for row in results)
    passed = sum(bool(row.get("passed")) for row in results)
    lines = [
        "# Rawlsing CLOSED_35 UID Smoke Report",
        "",
        f"- Run: `{run_ts}`",
        f"- Attempted: {total}",
        f"- Base V550→V552 spines passed: {base}",
        f"- J branches actually traversed: {traversed}",
        f"- Full V550→V552J graphs passed: {full}",
        f"- Selected-boundary passes: {passed}",
        "",
        "A base-spine pass is reported independently from J-branch traversal; a non-applicable J branch is never reported as traversed.",
    ]
    (report / "smoke_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    if argv is None and callable(_ORIGINAL_PARSE_ARGS):
        parsed = _ORIGINAL_PARSE_ARGS()
        explicit = any(
            item == "--joint-mode" or str(item).startswith("--joint-mode=")
            for item in sys.argv[1:]
        )
        if not explicit:
            parsed.joint_mode = "auto"
        return parsed
    parser = argparse.ArgumentParser(description="Governed CLOSED_35 UID smoke runner")
    parser.add_argument("--output-root", default=None)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--canary-only", action="store_true")
    scope.add_argument("--family-band", action="store_true")
    parser.add_argument("--only-scope", action="append", default=None, help="Family|Wave|Country")
    parser.add_argument("--skip-canary", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE))
    parser.add_argument("--db-url", default="")
    parser.add_argument("--qsm-relation", default=os.environ.get("DDM_QSM_RELATION", DEFAULT_QSM_RELATION))
    parser.add_argument("--response-long-relation", default=os.environ.get("DDM_RESPONSE_LONG_RELATION", AUTO_RESPONSE_RELATION))
    parser.add_argument("--response-option-map", default=None)
    parser.add_argument("--joint-registry", action="append", default=None)
    parser.add_argument("--joint-mode", choices=("auto", "required", "off"), default="auto")
    parser.add_argument("--association-mode", choices=("off", "funnel_only", "candidate_trace", "publishable"), default="off")
    parser.add_argument("--association-lane-registry", default=str(DEFAULT_ASSOCIATION_LANE_REGISTRY))
    parser.add_argument("--association-threshold-profiles", default=str(DEFAULT_ASSOCIATION_THRESHOLD_PROFILES))
    parser.add_argument("--first-pass-authority-dir", default=str(DEFAULT_FIRST_PASS_AUTHORITY_DIR))
    parser.add_argument("--semantic-authority-dir", default=str(DEFAULT_SEMANTIC_AUTHORITY_DIR))
    parser.add_argument("--position-conditioning-authority-dir", default=str(DEFAULT_POSITION_CONDITIONING_AUTHORITY_DIR))
    parser.add_argument("--directionality-authority-dir", default=str(DEFAULT_DIRECTIONALITY_AUTHORITY_DIR))
    parser.add_argument("--readiness-mode", choices=("full", "launch"), default="full")
    parser.add_argument("--diagnostic-continue", action="store_true")
    return parser.parse_args(argv)


def _config_from_args(args: argparse.Namespace) -> RuntimeConfig:
    registries = tuple(
        Path(value).expanduser().resolve()
        for value in (args.joint_registry or [str(DEFAULT_JOINT_REGISTRY)])
    )
    response_map = Path(args.response_option_map).expanduser().resolve() if args.response_option_map else None
    return RuntimeConfig(
        repo_root=ROOT,
        env_file=Path(args.env_file).expanduser().resolve(),
        db_url=args.db_url,
        qsm_relation=args.qsm_relation,
        response_option_map=response_map,
        joint_registry_paths=registries,
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
    rows: list[tuple[str, str, str]] = []
    for entry in entries or []:
        parts = [part.strip() for part in str(entry).split("|")]
        if len(parts) not in {2, 3} or not parts[0] or not parts[1]:
            raise ValueError(f"invalid --only-scope value:{entry!r}")
        identity, country = resolve_smoke_identity(parts[0], parts[1], parts[2] if len(parts) == 3 else "")
        rows.append((identity.canonical_display_source, identity.canonical_display_wave, country))
    return rows


def _run_scope(
    scope: list[tuple[str, str, str]],
    *,
    run_ts: str,
    output_root: str,
    config: RuntimeConfig,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    filters = Path(output_root) / "filters"
    for index, (source, wave, country) in enumerate(scope):
        try:
            filter_path, selected = _build_question_filter(
                source, wave, country, index, config=config, filter_root=filters
            )
            if not selected:
                raise RuntimeError("no_variables_found")
            row = run_wave(source, wave, country, run_ts, output_root, filter_path, selected, config)
        except Exception as exc:
            identity, resolved_country = resolve_smoke_identity(source, wave, country)
            row = {
                "survey_family": identity.canonical_display_source,
                "wave_id": identity.canonical_display_wave,
                "source_family_uid": identity.source_family_uid,
                "wave_uid": identity.wave_uid,
                "country": resolved_country,
                "base_spine_passed": False,
                "full_chain_passed": False,
                "joint_branch": {"traversed": False},
                "passed": False,
                "failure_stage": "orchestration",
                "functional_failure_reason": f"{type(exc).__name__}:{exc}",
            }
        results.append(row)
        if not row.get("passed") and not config.diagnostic_continue:
            break
    return results


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = _config_from_args(args)
    if args.only_scope:
        scope = _parse_only_scope(args.only_scope)
    elif args.canary_only:
        scope = [(CANARY_FAMILY, CANARY_WAVE, CANARY_COUNTRY)]
    elif args.family_band:
        scope = list(FAMILY_BAND)
    else:
        scope = list(ALL_WAVES)
    if args.skip_canary:
        canary_uid = resolve_source_wave_identity(CANARY_FAMILY, CANARY_WAVE, require_closed_35=True).wave_uid
        scope = [
            row for row in scope
            if resolve_source_wave_identity(row[0], row[1], require_closed_35=True).wave_uid != canary_uid
        ]
    preflight = run_preflight(config, scope)
    run_ts = _now()
    output_root = args.output_root or str(ROOT / f"outputs/universality_20var_35wave_v550_552j/{run_ts}")
    if args.preflight_only or not preflight["passed"]:
        Path(output_root, "reports").mkdir(parents=True, exist_ok=True)
        Path(output_root, "reports/preflight.json").write_text(
            json.dumps(preflight, indent=2, default=str) + "\n", encoding="utf-8"
        )
        return 0 if args.preflight_only and preflight["passed"] else 2
    results = _run_scope(scope, run_ts=run_ts, output_root=output_root, config=config)
    write_summaries(results, output_root, run_ts, args.canary_only, preflight)
    return 0 if results and all(row.get("passed") for row in results) else 1


__all__ = [
    "ALL_WAVES", "FAMILY_BAND", "CANARY_FAMILY", "CANARY_WAVE", "CANARY_COUNTRY",
    "RuntimeConfig", "DEFAULT_CONFIG", "COMPILER_SPECS", "runtime_compiler_paths",
    "resolve_smoke_identity", "run_id_for_identity", "validate_explicit_scope",
    "resolve_joint_authority", "summarize_joint_authority_coverage", "run_preflight",
    "run_v550_shard", "run_v550j", "run_v551", "run_v551j", "run_v552", "run_v552j",
    "run_wave", "write_summaries", "parse_args", "main",
]

if __name__ == "__main__":
    raise SystemExit(main())
