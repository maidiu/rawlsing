#!/usr/bin/env python3
"""Authority-derived 20-variable V550→V552 universality smoke.

The governed universe is CLOSED_35_WAVES. Joint stages are applicability-
scoped: a governed scope with executable family authority must pass V550J →
V551J → V552J; a scope without such authority is reported as NOT_APPLICABLE
(or coverage debt) without turning absence of a nonexistent family definition
into failure of the base V550 → V551 → V552 spine.
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

from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError, load_closed_35_waves
from data.ddm_build_copy.ddm_v550_question_relation_authority import DEFAULT_AUTHORITY_PATH
from data.ddm_build_copy.ddm_v550j_registry_contract import registry_status_is_executable
from data.ddm_build_copy.ddm_v550_response_relation import AUTO_RESPONSE_RELATION

DEFAULT_JOINT_REGISTRY = REPO_ROOT / "data/ddm_build_copy/manifests/question_family_registry.yaml"
DEFAULT_RESPONSE_OPTION_MAP = REPO_ROOT / "data/ddm_build_copy/reports/V550_response_option_map.csv"
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

REGISTRY_PATH = str(DEFAULT_JOINT_REGISTRY.relative_to(REPO_ROOT))
RESPONSE_OPTION_MAP = str(DEFAULT_RESPONSE_OPTION_MAP.relative_to(REPO_ROOT))
ASSOCIATION_LANE_REGISTRY = str(DEFAULT_ASSOCIATION_LANE_REGISTRY.relative_to(REPO_ROOT))
ASSOCIATION_THRESHOLD_PROFILES = str(DEFAULT_ASSOCIATION_THRESHOLD_PROFILES.relative_to(REPO_ROOT))
ENV_FILE = str(DEFAULT_ENV_FILE.relative_to(REPO_ROOT))


def _load_governed_scope(authority_path: Path = DEFAULT_AUTHORITY_PATH) -> list[tuple[str, str, str]]:
    return list(load_closed_35_waves(authority_path))


try:
    ALL_WAVES: list[tuple[str, str, str]] = _load_governed_scope()
except BoundaryContractError:
    ALL_WAVES = []

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
    joint_mode: str = "auto"
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
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def validate_explicit_scope(waves: Iterable[tuple[str, str, str]] | None = None) -> list[str]:
    rows = list(ALL_WAVES if waves is None else waves)
    issues: list[str] = []
    if not rows:
        issues.append(f"governed_scope_unavailable:{DEFAULT_AUTHORITY_PATH}")
        return issues
    if len(rows) != 35:
        issues.append(f"governed_scope_count_expected_35_actual_{len(rows)}")
    pairs = [(family, wave) for family, wave, _ in rows]
    if len(set(pairs)) != len(pairs):
        issues.append("duplicate_family_wave_in_governed_scope")
    if ("Asian Barometer", "W6") in pairs:
        issues.append("asian_barometer_w6_present_in_closed_35_waves")
    included_excluded = sorted(wave for family, wave in pairs if family == "GSS" and wave in EXCLUDED_GSS_WAVES)
    if included_excluded:
        issues.append("excluded_gss_waves_present:" + ",".join(included_excluded))
    return issues


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
    evs = {"1981": "W1", "1990": "W2", "1999": "W3", "2008": "W4", "2017": "W5"}
    roman_numeric = {"I": "1", "II": "2", "III": "3", "IV": "4", "V": "5", "VI": "6", "VII": "7", "VIII": "8", "IX": "9"}
    numeric_labels: set[str] = set()
    if _norm(family) == "evs" and wave in evs:
        aliases.add(evs[wave])
        numeric_labels.add(evs[wave][1:])
    upper = wave.upper().strip()
    if upper in roman_numeric:
        numeric_labels.add(roman_numeric[upper])
    match = re.fullmatch(r"(?:W|R|WAVE\s*|ROUND\s*)?(\d+)", upper)
    if match:
        numeric_labels.add(match.group(1))
    for number in numeric_labels:
        aliases.update({number, f"W{number}", f"R{number}", f"Wave {number}", f"Round {number}"})
    return sorted(aliases)


def _joint_registry_payload_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _registry_var_codes(payload: dict[str, Any], family: str, wave: str) -> dict[str, list[str]]:
    source_family = str(payload.get("source_family") or "")
    aggregates = {"alllayer1scopes", "allscopes", "all"}
    if source_family and _norm(source_family) not in {_norm(family), *aggregates}:
        return {}
    wave_keys = {_norm(value) for value in _wave_aliases(family, wave)}
    out: dict[str, list[str]] = {}
    for cfg in payload.get("families") or []:
        if not isinstance(cfg, dict):
            continue
        family_source = str(cfg.get("source_family") or source_family)
        if family_source and _norm(family_source) not in {_norm(family), *aggregates}:
            continue
        eligible = cfg.get("eligible_waves") or []
        if eligible and not ({_norm(value) for value in eligible} & wave_keys):
            continue
        codes: list[str] = []
        groups = cfg.get("item_role_groups") or {}
        if isinstance(groups, dict):
            for members in groups.values():
                for row in members or []:
                    if isinstance(row, dict) and row.get("var_code"):
                        code = str(row["var_code"]).strip()
                        if code and code not in codes:
                            codes.append(code)
        if codes:
            out[str(cfg.get("family_id") or "unnamed_family")] = codes
    return out


def resolve_joint_authority(config: RuntimeConfig, family: str, wave: str, selected_vars: Iterable[str] | None = None) -> dict[str, Any]:
    selected_keys = {_norm(v) for v in selected_vars or []}
    matches: list[dict[str, Any]] = []
    rejected: list[dict[str, str]] = []
    for path in config.joint_registry_paths:
        payload = _load_yaml(path)
        if not payload:
            continue
        families = _registry_var_codes(payload, family, wave)
        if not families:
            continue
        status = str(payload.get("status") or "").strip()
        if not registry_status_is_executable(status):
            rejected.append({"path": str(path), "registry_status": status})
            continue
        overlap = {fid: [code for code in codes if not selected_keys or _norm(code) in selected_keys] for fid, codes in families.items()}
        matches.append({"path": str(path), "registry_status": status, "registry_hash": _joint_registry_payload_hash(payload), "families": families, "selected_overlap": {k: v for k, v in overlap.items() if v}})
    if not matches:
        if rejected:
            return {"applicable": False, "reason": "joint_registry_status_not_executable", "coverage_state": "APPLICABLE_UNRESOLVED", "rejected_registry_statuses": rejected, "candidate_vars": []}
        return {"applicable": False, "reason": "no_explicit_joint_registry_for_family_wave", "coverage_state": "NOT_APPLICABLE", "registry_path": "", "candidate_vars": []}
    hashes = {row["registry_hash"] for row in matches}
    if len(hashes) > 1:
        return {"applicable": False, "reason": "conflicting_joint_registries_for_family_wave", "coverage_state": "APPLICABLE_UNRESOLVED", "registry_paths": [r["path"] for r in matches], "candidate_vars": []}
    chosen = sorted(matches, key=lambda row: row["path"])[0]
    candidate_vars = [code for codes in chosen["families"].values() for code in codes]
    if selected_vars is not None and not chosen["selected_overlap"]:
        return {"applicable": False, "reason": "joint_registry_exists_but_selected_slice_has_no_family_items", "coverage_state": "NOT_APPLICABLE", "registry_path": chosen["path"], "candidate_vars": candidate_vars, "registry_status": chosen["registry_status"]}
    return {"applicable": True, "reason": "explicit_joint_registry_applies", "coverage_state": "PRESENT", "registry_path": chosen["path"], "candidate_vars": candidate_vars, "registry_status": chosen["registry_status"], "registry_hash": chosen["registry_hash"], "selected_overlap": chosen["selected_overlap"]}


def summarize_joint_authority_coverage(config: RuntimeConfig, waves: Iterable[tuple[str, str, str]] | None = None) -> dict[str, Any]:
    wave_rows = list(ALL_WAVES if waves is None else waves)
    covered, not_applicable, unresolved = [], [], []
    for family, wave, country in wave_rows:
        authority = resolve_joint_authority(config, family, wave)
        row = {"source": family, "wave": wave, "country_code": country or COUNTRY_MAP.get(family, {}).get(wave, ""), "reason": authority.get("reason", ""), "coverage_state": authority.get("coverage_state", ""), "registry_path": authority.get("registry_path", ""), "candidate_var_count": len(authority.get("candidate_vars") or [])}
        if authority.get("applicable"):
            covered.append(row)
        elif authority.get("coverage_state") == "NOT_APPLICABLE":
            not_applicable.append(row)
        else:
            unresolved.append(row)
    return {"scope_count": len(wave_rows), "applicable_scope_count": len(covered), "not_applicable_scope_count": len(not_applicable), "coverage_debt_scope_count": len(unresolved), "applicable_scopes": covered, "not_applicable_scopes": not_applicable, "coverage_debt_scopes": unresolved}


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
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _sql_normalized(column: str) -> str:
    return f"regexp_replace(translate(lower(COALESCE({column}::text, '')), 'áéíóúüñ', 'aeiouun'), '[^a-z0-9]+', '', 'g')"


def _select_question_variables(family: str, wave: str, country: str, seed: int = 42, *, config: RuntimeConfig = DEFAULT_CONFIG) -> list[str]:
    import psycopg2
    env = _load_env_file(config.env_file)
    db_url = config.db_url or os.environ.get("DATABASE_URL", "") or env.get("DATABASE_URL", "")
    if not db_url:
        raise RuntimeError("DATABASE_URL is required to select the 20-variable slice")
    qsm_rel = _validate_relation_identifier(config.qsm_relation, "qsm_relation")
    registry_rel = _validate_relation_identifier(config.canonical_registry_relation, "canonical_registry_relation")
    source_keys = sorted({_norm(v) for v in _source_aliases(family)})
    wave_keys = sorted({_norm(v) for v in _wave_aliases(family, wave)})
    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""WITH mapped_questions AS (
                SELECT DISTINCT {_sql_normalized('var_code')} AS normalized_var_key FROM {qsm_rel}
                WHERE {_sql_normalized('source')} = ANY(%s) AND {_sql_normalized('wave')} = ANY(%s))
                SELECT cr.canonical_var_code, COALESCE(cr.authority_semantic_role, '') FROM {registry_rel} cr
                JOIN mapped_questions mq ON mq.normalized_var_key = {_sql_normalized('cr.canonical_var_code')}
                WHERE {_sql_normalized('cr.canonical_source')} = ANY(%s) AND {_sql_normalized('cr.canonical_wave')} = ANY(%s)
                ORDER BY cr.canonical_var_code""", (source_keys, wave_keys, source_keys, wave_keys))
            fetched = [(str(code), str(role or "")) for code, role in cur.fetchall()]
    all_vars, seen = [], set()
    for code, role in fetched:
        key = _norm(code)
        if key and key not in seen:
            seen.add(key)
            all_vars.append((code, role))
    if not all_vars:
        return []
    buckets: dict[str, list[str]] = {name: [] for name in CATEGORIES}
    for code, role in all_vars:
        role_lower = role.lower().strip()
        category = next((name for name, words in CATEGORIES.items() if any(word in role_lower for word in words)), "relation_evidence")
        buckets[category].append(code)
    rng = random.Random(seed)
    selected: list[str] = []
    for category, target in (("demographic_context", 4), ("directional_attitudinal", 4), ("relation_evidence", 4), ("structural_mapped", 4), ("edge_ambiguous", 2), ("known_fragile", 2)):
        available = [code for code in buckets[category] if code not in selected]
        selected.extend(rng.sample(available, min(target, len(available), 20 - len(selected))))
    pool = [code for code, _ in all_vars if code not in selected]
    if len(selected) < 20:
        selected.extend(rng.sample(pool, min(20 - len(selected), len(pool))))
    rng.shuffle(selected)
    return selected[:20]


def _build_question_filter(family: str, wave: str, country: str, seed: int = 42, *, config: RuntimeConfig = DEFAULT_CONFIG, filter_root: str | Path | None = None) -> tuple[str, list[str]]:
    selected = _select_question_variables(family, wave, country, seed=seed, config=config)
    if not selected:
        return "", []
    root = Path(filter_root) if filter_root else Path("/tmp/rawlsing_20var_filters")
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{_family_wave_id(family, wave)}.json"
    path.write_text(json.dumps({"question_ids": selected, "var_codes": selected}, indent=2) + "\n", encoding="utf-8")
    return str(path), selected


def _run(cmd: list[str], *, timeout_sec: int, config: RuntimeConfig) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(config.repo_root)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if config.db_url:
        env["DATABASE_URL"] = config.db_url
    started = time.monotonic()
    try:
        proc = subprocess.run(cmd, cwd=config.repo_root, env=env, capture_output=True, text=True, timeout=timeout_sec)
        return {"exit_code": proc.returncode, "stdout_tail": (proc.stdout or "")[-4000:], "stderr_tail": (proc.stderr or "")[-4000:], "elapsed": round(time.monotonic()-started,1), "command": " ".join(cmd)}
    except subprocess.TimeoutExpired:
        return {"exit_code": -1, "stdout_tail": "", "stderr_tail": "TIMEOUT", "elapsed": round(time.monotonic()-started,1), "command": " ".join(cmd)}


def _manifest_gate(path: Path, *, row_keys: tuple[str, ...] = (), status_keys: tuple[str, ...] = ()) -> dict[str, Any]:
    payload = _load_json(path)
    if not payload:
        return {"passed": False, "failure_reason": f"missing_manifest:{path}"}
    status = next((str(payload.get(k) or "") for k in status_keys if payload.get(k)), "")
    if status.upper().startswith(("BLOCKED", "NOT_READY", "FAILED")):
        return {"passed": False, "failure_reason": f"blocked_status:{status}", "status": status}
    if row_keys:
        rows = max((int(payload.get(k) or 0) for k in row_keys), default=0)
        if rows <= 0:
            return {"passed": False, "failure_reason": "required_functional_rows_zero", "status": status, "rows": rows}
    return {"passed": True, "failure_reason": "", "status": status}


def _run_stage(cmd: list[str], gate_path: Path, *, config: RuntimeConfig, timeout: int, row_keys: tuple[str, ...] = (), status_keys: tuple[str, ...] = ()) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = _run(cmd, timeout_sec=timeout, config=config)
    if raw["exit_code"] != 0:
        return raw, {"passed": False, "failure_reason": raw.get("stderr_tail") or "nonzero_exit"}
    return raw, _manifest_gate(gate_path, row_keys=row_keys, status_keys=status_keys)


def run_preflight(config: RuntimeConfig, waves: Iterable[tuple[str, str, str]] | None = None) -> dict[str, Any]:
    wave_rows = list(ALL_WAVES if waves is None else waves)
    blockers = validate_explicit_scope(wave_rows)
    warnings: list[str] = []
    required_modules = ("pandas", "pyarrow", "psycopg2", "yaml")
    module_status = {name: importlib.util.find_spec(name) is not None for name in required_modules}
    blockers.extend(f"missing_python_module:{name}" for name, present in module_status.items() if not present)
    for name in ("build_determinicity_wave_shard_v550.py", "compile_v551_relation_evidence_atoms.py", "compile_v552_structural_ddm.py", "compile_v550j_joint_response_patterns.py", "compile_v551j_joint_evidence_packets.py", "compile_v552j_runtime_safe_structural_handoff.py"):
        if not (config.repo_root / "data/ddm_build_copy" / name).exists():
            blockers.append(f"missing_compiler:{name}")
    joint = summarize_joint_authority_coverage(config, wave_rows)
    if config.joint_mode == "required" and (joint["not_applicable_scope_count"] or joint["coverage_debt_scope_count"]):
        blockers.append("joint_mode_required_but_scope_not_fully_applicable")
    elif config.joint_mode == "auto":
        if joint["not_applicable_scope_count"]:
            warnings.append(f"joint_not_applicable_scopes:{joint['not_applicable_scope_count']}")
        if joint["coverage_debt_scope_count"]:
            warnings.append(f"joint_coverage_debt_scopes:{joint['coverage_debt_scope_count']}")
    return {"passed": not blockers, "blockers": blockers, "warnings": warnings, "module_status": module_status, "joint_authority_coverage": joint, "joint_mode": config.joint_mode, "requested_scope_count": len(wave_rows), "explicit_wave_count": len(ALL_WAVES), "scope_authority_path": str(DEFAULT_AUTHORITY_PATH)}


def run_wave(family: str, wave: str, country: str, run_ts: str, output_root: str, filter_path: str, selected_vars: list[str], config: RuntimeConfig = DEFAULT_CONFIG) -> dict[str, Any]:
    run_id = f"{_family_wave_id(family, wave)}_{run_ts}"
    shard_id = f"{family}_{wave}" + (f"_{country}" if country else "")
    result: dict[str, Any] = {"survey_family": family, "wave_id": wave, "country": country, "run_id": run_id, "selected_variable_count": len(selected_vars), "selected_variables": selected_vars, "stages": {}, "joint_branch": {}, "base_spine_passed": False, "full_chain_passed": False, "acceptance_boundary": "none", "passed": False}
    authority = resolve_joint_authority(config, family, wave, selected_vars)
    result["joint_branch"]["authority"] = authority
    registry = authority.get("registry_path") if authority.get("applicable") and config.joint_mode != "off" else None
    v550_root = Path(output_root) / "v550"
    shard_dir = v550_root / "shard_runs" / run_id / shard_id
    cmd = [sys.executable, _abs("data/ddm_build_copy/build_determinicity_wave_shard_v550.py", config), "--run-id", run_id, "--shard-id", shard_id, "--source", family, "--wave", wave, "--canonical-wave", wave, "--output-root", str(v550_root), "--question-filter-file", filter_path, "--limit-questions", "20", "--env-file", str(config.env_file), "--response-long-relation", config.response_long_relation, "--first-pass-authority-dir", str(config.first_pass_authority_dir), "--semantic-authority-dir", str(config.semantic_authority_dir), "--position-conditioning-authority-dir", str(config.position_conditioning_authority_dir), "--directionality-authority-dir", str(config.directionality_authority_dir), "--no-write-csv"]
    if country:
        cmd += ["--country", country]
    if config.db_url:
        cmd += ["--db-url", config.db_url]
    if config.response_option_map:
        cmd += ["--response-option-map", str(config.response_option_map)]
    if registry:
        cmd += ["--shared-respondent-substrate-mode", "write", "--joint-configuration-registry-path", str(registry)]
    cmd.append("--full-readiness" if config.readiness_mode == "full" else "--allow-launch-ready-fallback")
    raw, gate = _run_stage(cmd, shard_dir / "manifest.json", config=config, timeout=3600, status_keys=("status", "final_status"))
    result["stages"]["v550"] = {"exit_code": raw["exit_code"], "semantic_gate": gate}
    if not gate["passed"]:
        result.update(failure_stage="v550", functional_failure_reason=gate["failure_reason"])
        return result

    response_map = shard_dir / "core/response_option_map.parquet"
    v551_root = Path(output_root) / "v551"
    v551_dir = v551_root / shard_id
    cmd = [sys.executable, _abs("data/ddm_build_copy/compile_v551_relation_evidence_atoms.py", config), "--run-id", shard_id, "--bridge-path", str(shard_dir / "bridge/v551_bridge_index.parquet"), "--question-use-contract-path", str(shard_dir / "core/question_use_contract.parquet"), "--response-option-map-path", str(response_map), "--output-root", str(v551_root), "--v551-compile-mode", "optimized_candidate_bridge", "--v551-audit-mode", "summary", "--no-progress", "--no-write-csv"]
    raw, gate = _run_stage(cmd, v551_dir / "manifest.json", config=config, timeout=1800, row_keys=("atom_rows",), status_keys=("status", "final_status"))
    result["stages"]["v551"] = {"exit_code": raw["exit_code"], "semantic_gate": gate}
    if not gate["passed"]:
        result.update(failure_stage="v551", functional_failure_reason=gate["failure_reason"])
        return result

    v552_root = Path(output_root) / "v552"
    v552_dir = v552_root / shard_id
    cmd = [sys.executable, _abs("data/ddm_build_copy/compile_v552_structural_ddm.py", config), "--run-id", shard_id, "--atoms-path", str(v551_dir / "relation_evidence_atoms.parquet"), "--output-root", str(v552_root), "--strict-handoff", "--no-progress", "--no-write-csv"]
    raw = _run(cmd, timeout_sec=1800, config=config)
    result["stages"]["v552"] = {"exit_code": raw["exit_code"]}
    if raw["exit_code"] != 0:
        result.update(failure_stage="v552", functional_failure_reason=raw.get("stderr_tail") or "nonzero_exit")
        return result
    result["base_spine_passed"] = True
    result["acceptance_boundary"] = "base_spine"

    if config.joint_mode == "off":
        result["joint_branch"].update(status="disabled", evidence_status="NOT_APPLICABLE", downstream_permission_status="NOT_APPLICABLE")
        result["passed"] = True
        return result
    if not authority.get("applicable"):
        evidence = authority.get("coverage_state", "APPLICABLE_UNRESOLVED")
        result["joint_branch"].update(status="not_applicable" if evidence == "NOT_APPLICABLE" else "coverage_debt", evidence_status=evidence, downstream_permission_status="NOT_APPLICABLE" if evidence == "NOT_APPLICABLE" else "DENY", reason=authority.get("reason", ""))
        if config.joint_mode == "required":
            result.update(failure_stage="joint_authority_gate", functional_failure_reason=authority.get("reason", "joint_authority_missing"))
            return result
        result["passed"] = True
        return result

    v550j_root = Path(output_root) / "v550j"
    substrate_manifests = sorted((shard_dir / "checkpoints/respondent_substrate").glob("source=*/wave=*/country_code=*/v550_shared_respondent_substrate_manifest.json"))
    if not substrate_manifests:
        result.update(failure_stage="v550j_substrate", functional_failure_reason="missing_shared_respondent_substrate_manifest")
        return result
    substrate_manifest = substrate_manifests[0]
    substrate = substrate_manifest.with_name("v550_shared_respondent_substrate.parquet")
    cmd = [sys.executable, _abs("data/ddm_build_copy/compile_v550j_joint_response_patterns.py", config), "--v550-shard-dir", str(shard_dir), "--output-root", str(v550j_root), "--registry-path", str(authority["registry_path"]), "--response-option-map", str(response_map), "--question-filter-file", filter_path, "--env-file", str(config.env_file), "--association-mode", config.association_mode, "--v550j-substrate-mode", "prepared_required", "--prepared-substrate-path", str(substrate), "--prepared-substrate-manifest-path", str(substrate_manifest), "--forbid-database-access", "--no-progress", "--no-write-csv", "--with-diagnostics"]
    raw = _run(cmd, timeout_sec=1800, config=config)
    result["stages"]["v550j"] = {"exit_code": raw["exit_code"]}
    if raw["exit_code"] != 0:
        result.update(failure_stage="v550j", functional_failure_reason=raw.get("stderr_tail") or "nonzero_exit")
        return result
    joint_dir = v550j_root / "runs" / run_id / shard_id / "joint_patterns"
    v551j_root = Path(output_root) / "v551j"
    v551j_dir = v551j_root / shard_id
    cmd = [sys.executable, _abs("data/ddm_build_copy/compile_v551j_joint_evidence_packets.py", config), "--run-id", shard_id, "--v551-atoms-path", str(v551_dir / "relation_evidence_atoms.parquet"), "--v550j-pattern-index-path", str(joint_dir / "joint_response_pattern_index.parquet"), "--v550j-meaning-summary-path", str(joint_dir / "joint_pattern_meaning_summary.parquet"), "--registry-path", str(authority["registry_path"]), "--output-root", str(v551j_root), "--emit-review-surface", "--emit-certified-index", "--no-write-csv"]
    raw = _run(cmd, timeout_sec=1800, config=config)
    result["stages"]["v551j"] = {"exit_code": raw["exit_code"]}
    if raw["exit_code"] != 0:
        result.update(failure_stage="v551j", functional_failure_reason=raw.get("stderr_tail") or "nonzero_exit")
        return result
    v552j_root = Path(output_root) / "v552j"
    cmd = [sys.executable, _abs("data/ddm_build_copy/compile_v552j_runtime_safe_structural_handoff.py", config), "--run-id", shard_id, "--v551j-run-root", str(v551j_dir), "--output-root", str(v552j_root)]
    raw = _run(cmd, timeout_sec=1800, config=config)
    result["stages"]["v552j"] = {"exit_code": raw["exit_code"]}
    if raw["exit_code"] != 0:
        result.update(failure_stage="v552j", functional_failure_reason=raw.get("stderr_tail") or "nonzero_exit")
        return result
    result["joint_branch"].update(status="passed", evidence_status="PRESENT", downstream_permission_status="ALLOW")
    result["full_chain_passed"] = True
    result["acceptance_boundary"] = "full_v550_to_v552j_chain"
    result["passed"] = True
    return result


def _run_scope(scope: list[tuple[str, str, str]], *, run_ts: str, output_root: str, config: RuntimeConfig) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    filters_root = Path(output_root) / "filters"
    for index, (family, wave, country) in enumerate(scope):
        country = country or COUNTRY_MAP.get(family, {}).get(wave, "")
        try:
            filter_path, selected = _build_question_filter(family, wave, country, seed=index, config=config, filter_root=filters_root)
        except Exception as exc:
            results.append({"survey_family": family, "wave_id": wave, "country": country, "passed": False, "failure_stage": "question_filter_selection", "functional_failure_reason": str(exc)})
            if not config.diagnostic_continue:
                break
            continue
        if not selected:
            results.append({"survey_family": family, "wave_id": wave, "country": country, "passed": False, "failure_stage": "question_filter_selection", "functional_failure_reason": "no_variables_found"})
            if not config.diagnostic_continue:
                break
            continue
        result = run_wave(family, wave, country, run_ts, output_root, filter_path, selected, config)
        results.append(result)
        if not result.get("passed") and not config.diagnostic_continue:
            break
    return results


def write_summaries(results: list[dict[str, Any]], output_root: str, run_ts: str, canary_only: bool, preflight: dict[str, Any] | None = None) -> None:
    report_dir = Path(output_root) / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    payload = {"run_ts": run_ts, "scope_authority": str(DEFAULT_AUTHORITY_PATH), "preflight": preflight or {}, "results": results}
    (report_dir / "smoke_summary.json").write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    total = len(results)
    passed = sum(bool(r.get("passed")) for r in results)
    base = sum(bool(r.get("base_spine_passed")) for r in results)
    full = sum(bool(r.get("full_chain_passed")) for r in results)
    applicable = sum((r.get("joint_branch") or {}).get("authority", {}).get("applicable") is True for r in results)
    joint_pass = sum((r.get("joint_branch") or {}).get("status") == "passed" for r in results)
    lines = ["# Universality Functional Smoke Report", "", f"**Run:** {run_ts}", f"**Scope:** {'canary only' if canary_only else 'authority-derived CLOSED_35_WAVES'}", "**Base spine:** V550 → V551 → V552", "**Joint branch:** V550J → V551J → V552J only where executable governed family authority applies", "", "## Summary", "", f"- Waves attempted: {total}", f"- Base spines passed: {base}", f"- Joint-applicable scopes: {applicable}", f"- Joint-applicable chains passed: {joint_pass}", f"- Full J chains passed: {full}", f"- Waves passed at applicability-scoped acceptance boundary: {passed}", ""]
    if total and passed == total and joint_pass == applicable:
        lines.append("**READY at the applicability-scoped boundary.** Every attempted base scope passed, and every joint-applicable scope passed its J-chain.")
    else:
        lines.append(f"**NOT READY.** {passed}/{total} scopes passed; {joint_pass}/{applicable} applicable J-chains passed.")
    (report_dir / "smoke_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Authority-derived CLOSED_35_WAVES universality smoke runner")
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
    parser.add_argument("--canonical-registry-relation", default=os.environ.get("DDM_CANONICAL_REGISTRY_RELATION", DEFAULT_CANONICAL_REGISTRY_RELATION))
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
    return parser.parse_args()


def _config_from_args(args: argparse.Namespace) -> RuntimeConfig:
    registry_paths = tuple(Path(v).expanduser().resolve() for v in (args.joint_registry or [str(DEFAULT_JOINT_REGISTRY)]))
    response_map = Path(args.response_option_map).expanduser().resolve() if args.response_option_map else (DEFAULT_RESPONSE_OPTION_MAP.resolve() if DEFAULT_RESPONSE_OPTION_MAP.exists() else None)
    return RuntimeConfig(repo_root=REPO_ROOT, env_file=Path(args.env_file).expanduser().resolve(), db_url=args.db_url, qsm_relation=args.qsm_relation, canonical_registry_relation=args.canonical_registry_relation, response_option_map=response_map, joint_registry_paths=registry_paths, association_lane_registry=Path(args.association_lane_registry).expanduser().resolve(), association_threshold_profiles=Path(args.association_threshold_profiles).expanduser().resolve(), first_pass_authority_dir=Path(args.first_pass_authority_dir).expanduser().resolve(), semantic_authority_dir=Path(args.semantic_authority_dir).expanduser().resolve(), position_conditioning_authority_dir=Path(args.position_conditioning_authority_dir).expanduser().resolve(), directionality_authority_dir=Path(args.directionality_authority_dir).expanduser().resolve(), association_mode=args.association_mode, joint_mode=args.joint_mode, readiness_mode=args.readiness_mode, diagnostic_continue=args.diagnostic_continue, response_long_relation=args.response_long_relation)


def _parse_only_scope(entries: Iterable[str] | None) -> list[tuple[str, str, str]]:
    governed = {(f, w) for f, w, _ in ALL_WAVES}
    out = []
    for entry in entries or []:
        parts = [p.strip() for p in str(entry).split("|")]
        if len(parts) not in {2, 3} or not parts[0] or not parts[1]:
            raise ValueError(f"invalid --only-scope value {entry!r}")
        family, wave = parts[0], parts[1]
        if (family, wave) not in governed:
            raise ValueError(f"scope is not in CLOSED_35_WAVES: {entry!r}")
        out.append((family, wave, parts[2] if len(parts) == 3 else COUNTRY_MAP.get(family, {}).get(wave, "")))
    return out


def main() -> int:
    args = parse_args()
    config = _config_from_args(args)
    run_ts = _now()
    output_root = args.output_root or str(REPO_ROOT / f"outputs/universality_20var_35wave_v550_552j_{run_ts}")
    Path(output_root).mkdir(parents=True, exist_ok=True)
    try:
        only_scope = _parse_only_scope(args.only_scope)
    except ValueError as exc:
        _log(str(exc))
        return 2
    preflight_scope = only_scope or ([(CANARY_FAMILY, CANARY_WAVE, CANARY_COUNTRY)] if args.canary_only else (list(FAMILY_BAND) if args.family_band else list(ALL_WAVES)))
    preflight = run_preflight(config, preflight_scope)
    reports = Path(output_root) / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "preflight.json").write_text(json.dumps(preflight, indent=2) + "\n", encoding="utf-8")
    if args.preflight_only or not preflight["passed"]:
        return 0 if preflight["passed"] else 2
    if only_scope:
        results = _run_scope(only_scope, run_ts=run_ts, output_root=output_root, config=config)
        write_summaries(results, output_root, run_ts, False, preflight)
        return 0 if len(results) == len(only_scope) and all(r.get("passed") for r in results) else 1
    if args.family_band:
        results = _run_scope(FAMILY_BAND, run_ts=run_ts, output_root=output_root, config=config)
        write_summaries(results, output_root, run_ts, False, preflight)
        return 0 if len(results) == len(FAMILY_BAND) and all(r.get("passed") for r in results) else 1
    results: list[dict[str, Any]] = []
    if not args.skip_canary:
        canary = _run_scope([(CANARY_FAMILY, CANARY_WAVE, CANARY_COUNTRY)], run_ts=run_ts, output_root=output_root, config=config)
        results.extend(canary)
        if not canary or not canary[0].get("passed"):
            write_summaries(results, output_root, run_ts, True, preflight)
            return 1
    if args.canary_only:
        write_summaries(results, output_root, run_ts, True, preflight)
        return 0
    remaining = [row for row in ALL_WAVES if (row[0], row[1]) != (CANARY_FAMILY, CANARY_WAVE)] if not args.skip_canary else list(ALL_WAVES)
    results.extend(_run_scope(remaining, run_ts=run_ts, output_root=output_root, config=config))
    write_summaries(results, output_root, run_ts, False, preflight)
    return 0 if len(results) == len(ALL_WAVES) and all(r.get("passed") for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
