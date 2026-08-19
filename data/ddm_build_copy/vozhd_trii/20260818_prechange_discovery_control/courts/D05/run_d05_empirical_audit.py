#!/usr/bin/env python3
"""D05 populated empirical substrate audit — read-only, fixed-semantics runner.

Canonical invocation (no semantic arguments):

    DATABASE_URL='postgresql://...' python \
      data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/courts/D05/run_d05_empirical_audit.py

Operational-only switches exist for connection/repository/timeout/provenance paths.
All database observations are taken inside one REPEATABLE READ, READ ONLY
transaction. The program issues no DDL or DML and writes only under courts/D05.
See D05_AUDIT_CONTRACT.json for exact relation, column, invariant, failure-code,
and output-schema law.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
import traceback
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

try:
    import psycopg2
    from psycopg2 import sql
except Exception as exc:
    print(f"D05_E_RUNTIME_DEPENDENCY: psycopg2 unavailable: {exc}", file=sys.stderr)
    raise SystemExit(20)

COURT_REL = Path("data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/courts/D05")
CONTROL_REL = Path("data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control")
BASE_SHA = "bf9a0434eb2096d5c4725cf483ec757fd319b6af"
REQUIRED_BRANCH = "agent/vozhd-trii-d05-empirical-substrate"

LOCKED_HASHES = {
    "Rawlsing_WVS_public_schema.sql": "2c3f4a9ebec1e6c0cf62e8827ab982e52243c5c8899c961cd0e30b489573ec76",
    "Rawlsing_WVS_authority_reconcile_schema.sql": "57e8c58c9444be9c34df54765e1801a9819f7a15fd02ddaa9a8e194e57596877",
    "rawlsing_v5_ddm_production_continuation_pack_v2_ATTITUDE_CLOUD_LOCKED.zip": "e9c66a9638371966d620ef73c30f03c5dcca255cd874acbdf66e3738654b5861",
    "rawlsing_v5_home_stretch_build_pack_v18_FINAL_LOCKED_NO_GHOSTS.zip": "a654014fb56032544fc4044ee230cf69823e076cb5f3e4fc3df91eb3148f12bd",
    "rawlsing_chatlog_DDM_chatgpt_1.txt": "b0ff181b0d1f6a591b005b829aafeb27b0740249332b49e08bd381800ab1745a",
}

REQUIRED_RELATIONS = {
    "public.survey_microdata_respondents": (True, ["id", "source", "wave", "country_code", "survey_year"]),
    "public.survey_microdata_responses": (True, ["respondent_id", "var_code", "value_raw", "value_text"]),
    "public.survey_weight_fact": (False, ["respondent_id", "weight_name", "weight_value", "weight_type", "source_var", "source", "wave", "is_primary"]),
    "public.respondent_position_fact": (False, ["respondent_id", "source_family", "wave", "country_code", "survey_year", "sex", "age", "education_level", "income_level", "income_source_note", "urban_rural", "religion_label", "marital", "employment", "class_level", "household_size", "language", "region", "ethnicity", "position_source_table", "position_completeness_score"]),
    "public.question_structural_mapping": (False, ["source", "wave", "question_id", "var_code", "display_text", "legacy_final_driver_id", "final_driver_label", "final_driver_scope", "final_driver_origin", "driver_id", "driver_facet_id", "question_block_id", "structural_domain_id", "relation_axis_id", "target_entity_id", "mapping_status", "evidence_kind", "strata_relevance", "channel_affordances", "forbidden_inference", "does_not_measure", "review_notes", "loaded_at"]),
    "public.survey_authority_compendium": (False, []),
    "public.v_ddm_response_long_facet_ready": (False, ["respondent_id", "source", "wave", "canonical_wave", "country_code", "survey_year", "var_code", "value_raw", "value_text", "weight_value", "weight_name", "weight_status", "sex", "age", "age_group", "education_level", "income_level", "religion_label", "urban_rural", "region", "ethnicity", "language", "employment", "marital", "household_size", "position_source_table", "position_completeness_score", "question_id", "question_block_id", "structural_domain_id", "driver_id", "driver_facet_id", "relation_axis_id", "target_entity_id", "mapping_status", "legacy_final_driver_id", "legacy_driver_leak_flag"]),
    "public.v_ddm_response_long_facet_ready_authority": (False, ["respondent_id", "source", "wave", "canonical_wave", "country_code", "var_code"]),
    "public.ddm_demographic_field_register": (False, []),
}

POSITION_FIELDS = ["sex", "age", "age_group", "education_level", "income_level", "religion_label", "urban_rural", "region", "ethnicity", "language", "employment", "marital", "household_size", "class_level"]
TYPED_FLAGS = ["is_missing", "is_dk", "is_refusal", "is_iap", "is_valid_substantive_response"]

OUTPUTS = {
    "RELATION_PREFLIGHT.csv": ["relation", "relation_kind", "exists", "fatal_if_absent", "required_columns_json", "actual_columns_json", "missing_columns_json", "row_count", "status", "failure_code"],
    "SOURCE_WAVE_READINESS.csv": ["source", "raw_wave", "canonical_wave", "country_code", "survey_year", "respondents", "response_rows", "responded_respondents", "distinct_var_codes", "facet_rows", "facet_respondents", "authority_facet_rows", "authority_facet_respondents", "raw_minus_facet_rows", "raw_minus_authority_rows"],
    "POSITION_FIELD_COMPLETENESS.csv": ["field_name", "field_origin", "source_family", "wave", "respondent_rows", "nonmissing_rows", "missing_rows", "coverage_pct", "distinct_nonmissing_values", "physical_column_present", "register_var_name", "register_question_id", "status"],
    "QUESTION_OVERLAP_SUMMARY.csv": ["source", "wave", "country_code", "question_x", "question_y", "respondents_x", "respondents_y", "respondents_overlap", "respondents_union", "overlap_pct_of_x", "overlap_pct_of_y", "jaccard_pct", "respondents_overlap_unique_each", "cotravel_possible", "duplicate_compromised_overlap"],
    "WEIGHT_COVERAGE.csv": ["source", "wave", "respondents", "respondents_with_any_weight", "respondents_with_primary_weight", "respondents_missing_primary_weight", "respondents_with_multiple_primary_weights", "weight_rows", "primary_weight_rows", "null_primary_weights", "zero_primary_weights", "negative_primary_weights", "nonfinite_primary_weights", "weight_names_json", "weight_types_json", "source_vars_json", "status"],
    "IDENTITY_JOIN_AUDIT.csv": ["source", "wave", "country_code", "response_rows", "exactly_joined_rows", "fallback_joined_rows", "ambiguous_rows", "unmapped_rows", "blocked_rows", "excluded_rows", "distinct_var_codes", "distinct_question_ids", "exact_join_pct", "join_status"],
    "RESPONSE_MULTIPLICITY_AUDIT.csv": ["source", "wave", "country_code", "respondents", "response_rows", "distinct_respondent_var_pairs", "duplicate_var_pairs", "duplicate_var_excess_rows", "respondent_question_pairs", "duplicate_canonical_question_pairs", "canonical_duplicate_excess_rows", "min_questions_per_respondent", "p50_questions_per_respondent", "p90_questions_per_respondent", "p99_questions_per_respondent", "max_questions_per_respondent", "min_response_rows_per_respondent", "p50_response_rows_per_respondent", "p90_response_rows_per_respondent", "p99_response_rows_per_respondent", "max_response_rows_per_respondent"],
    "TYPED_MISSINGNESS_PREVALENCE.csv": ["relation", "source", "wave", "country_code", "metric", "rows", "flagged_rows", "prevalence_pct", "status"],
    "RESPONSE_TOPOLOGY_AUDIT.csv": ["relation", "source", "wave", "var_code", "question_id", "question_type", "response_topology", "handling_rule", "source_structure_classification", "response_rows", "distinct_respondents", "distinct_raw_values", "duplicate_respondent_var_pairs", "status"],
    "FACET_READY_PARITY_AUDIT.csv": ["relation", "source", "wave", "country_code", "raw_rows", "facet_rows", "raw_keys", "facet_keys", "raw_rows_missing_from_facet", "facet_rows_without_raw", "multiplicity_mismatch_keys", "value_raw_mismatch_rows", "value_text_mismatch_rows", "respondent_linkage_preserved", "p_y_given_position_possible", "p_y_given_position_conjunction_possible", "p_y_given_x_response_possible", "p_y_given_x_response_and_position_possible", "status"],
    "INFORMATION_LOSS_AUDIT.csv": ["surface", "property", "evidence_type", "observed_value", "invariant", "status", "failure_code"],
    "STATIC_EVIDENCE_PROVENANCE.csv": ["path_or_name", "provenance_kind", "exists_locally", "sha256_expected", "sha256_actual", "hash_match", "git_blob_sha", "status"],
    "INVARIANT_RESULTS.csv": ["invariant_id", "scope", "description", "observed", "expected", "passed", "severity", "failure_code"],
    "FAILURES.csv": ["failure_code", "severity", "scope", "message"],
}

STATIC_FILES = [
    "data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/README.md",
    "data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/00_FULL_MACHINE_VISION.md",
    "data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/01_FINDINGS_LEDGER.md",
    "data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/02_RESOURCE_INDEX.md",
    "data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/03_ASSUMPTION_AND_UNKNOWN_REGISTER.md",
    "data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/04_DISCOVERY_COURTS_REGISTER.md",
    "data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/05_DECISION_PROTOCOL.md",
    "data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/06_FIRST_WAVE_LAUNCH_REGISTER.md",
    "data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/DISCOVERY_REGISTER.json",
    "data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/evidence/conversation_inputs/SHA256SUMS.txt",
    "data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/evidence/conversation_inputs/Rawlsing_WVS_authority_reconcile_schema.sql",
    "data/ddm_build_copy/apply_postgres_facet_ready_substrate.py",
    "data/ddm_build_copy/build_demographic_field_register.py",
    "data/ddm_build_copy/build_response_option_map_v550.py",
    "data/ddm_build_copy/build_determinicity_repository_v550.py",
    "data/ddm_build_copy/build_determinicity_wave_shard_v550.py",
    "data/ddm_build_copy/ddm_v550_shared_respondent_substrate.py",
    "data/ddm_build_copy/ddm_v550_shared_cache.py",
    "data/ddm_build_copy/ddm_v550_response_relation.py",
    "data/ddm_build_copy/ddm_v550_question_relation_authority.py",
    "data/ddm_build_copy/ddm_v550_question_use.py",
    "data/ddm_build_copy/ddm_v550_position_distribution.py",
    "data/ddm_build_copy/ddm_v550_distributions.py",
    "data/ddm_build_copy/ddm_v550_branching.py",
    "data/ddm_build_copy/ddm_v550_clouds.py",
    "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/00_README_FIRST.md",
    "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv",
    "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/question_structural_mapping_live_PLUS4_FINAL_APPLIED_R1.csv",
    "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/CANONICAL_COORDINATE_REGISTRY_FINAL_R1.csv",
    "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/GOVERNING_PROVENANCE_R1.csv",
    "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/FINAL_HOSTILE_QA_R1.json",
    "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/SHA256SUMS.csv",
    "data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/RAWLSING_GOVERNING_SPIRIT.md",
    "data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/TERMINAL_DEMAND_ENVELOPE.md",
    "data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/ARCHITECTURE_PASS_LAW.md",
]


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def pct(n: Any, d: Any) -> float:
    return round(100.0 * int(n) / int(d), 6) if int(d or 0) else 0.0


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(repo: Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(repo), *args], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def repo_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / ".git").exists():
            return parent
    found = git(Path.cwd(), "rev-parse", "--show-toplevel")
    if not found:
        raise RuntimeError("D05_E_REPO_ROOT: cannot locate repository root")
    return Path(found).resolve()


def write_csv(path: Path, fields: Sequence[str], rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})


def rows(cur) -> list[dict[str, Any]]:
    names = [d.name if hasattr(d, "name") else d[0] for d in cur.description]
    return [dict(zip(names, r)) for r in cur.fetchall()]


def rel(name: str) -> sql.Composed:
    schema, table = name.split(".", 1)
    return sql.SQL("{}.{}").format(sql.Identifier(schema), sql.Identifier(table))


class Audit:
    def __init__(self, repo: Path):
        self.repo = repo
        self.out = repo / COURT_REL
        self.out.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.failures: list[dict[str, str]] = []
        self.invariants: list[dict[str, Any]] = []
        self.exists: dict[str, bool] = {}
        self.columns: dict[str, set[str]] = {}
        self.started = utcnow()

    def fail(self, code: str, severity: str, scope: str, message: str) -> None:
        self.failures.append({"failure_code": code, "severity": severity, "scope": scope, "message": message})

    def inv(self, iid: str, scope: str, desc: str, observed: Any, expected: Any, passed: bool, severity: str, code: str = "") -> None:
        self.invariants.append({"invariant_id": iid, "scope": scope, "description": desc, "observed": json.dumps(observed, sort_keys=True, default=str) if isinstance(observed, (dict, list)) else observed, "expected": json.dumps(expected, sort_keys=True, default=str) if isinstance(expected, (dict, list)) else expected, "passed": passed, "severity": severity, "failure_code": "" if passed else code})
        if not passed and code:
            self.fail(code, severity, scope, f"{desc}; observed={observed!r}; expected={expected!r}")

    def query(self, text: Any, params: Any = None, scope: str = "query") -> list[dict[str, Any]]:
        try:
            with self.conn.cursor() as cur:
                cur.execute(text, params)
                return rows(cur)
        except Exception as exc:
            self.fail("D05_E_QUERY_FAILED", "FATAL", scope, f"{type(exc).__name__}: {exc}")
            raise


def static_provenance(a: Audit, public_schema: str | None) -> list[dict[str, Any]]:
    manifest = a.repo / CONTROL_REL / "evidence/conversation_inputs/SHA256SUMS.txt"
    parsed = {}
    if manifest.exists():
        for line in manifest.read_text(encoding="utf-8").splitlines():
            bits = line.strip().split(None, 1)
            if len(bits) == 2:
                parsed[bits[1].strip()] = bits[0]
    a.inv("D05-I-PROV-001", str(manifest.relative_to(a.repo)), "SHA256SUMS exactly equals locked evidence identities", parsed, LOCKED_HASHES, parsed == LOCKED_HASHES, "FATAL", "D05_E_STATIC_PROVENANCE_MISMATCH")
    out = []
    for rp in STATIC_FILES:
        p = a.repo / rp
        actual = sha256_file(p) if p.is_file() else ""
        expected = LOCKED_HASHES.get(p.name, "")
        match: Any = actual == expected if expected and actual else ""
        status = "OK" if p.is_file() else "MISSING_STATIC_EVIDENCE"
        if expected and actual and actual != expected:
            status = "HASH_MISMATCH"
            a.fail("D05_E_STATIC_PROVENANCE_MISMATCH", "FATAL", rp, f"expected {expected}; got {actual}")
        out.append({"path_or_name": rp, "provenance_kind": "CHECKED_IN", "exists_locally": p.is_file(), "sha256_expected": expected, "sha256_actual": actual, "hash_match": match, "git_blob_sha": git(a.repo, "rev-parse", f"HEAD:{rp}") if p.exists() else "", "status": status})
    external = ["Rawlsing_WVS_public_schema.sql", "rawlsing_v5_ddm_production_continuation_pack_v2_ATTITUDE_CLOUD_LOCKED.zip", "rawlsing_v5_home_stretch_build_pack_v18_FINAL_LOCKED_NO_GHOSTS.zip", "rawlsing_chatlog_DDM_chatgpt_1.txt"]
    for name in external:
        p = Path(public_schema).resolve() if name == "Rawlsing_WVS_public_schema.sql" and public_schema else None
        actual = sha256_file(p) if p and p.is_file() else ""
        expected = LOCKED_HASHES[name]
        status = "VERIFIED_EXTERNAL" if actual == expected else ("HASH_MISMATCH" if actual else "HASH_ADDRESSED_EXTERNAL_NOT_MATERIALIZED")
        if actual and actual != expected:
            a.fail("D05_E_STATIC_PROVENANCE_MISMATCH", "FATAL", name, f"expected {expected}; got {actual}")
        out.append({"path_or_name": str(p) if p else name, "provenance_kind": "EXTERNAL_HASH_ADDRESSED", "exists_locally": bool(p and p.is_file()), "sha256_expected": expected, "sha256_actual": actual, "hash_match": actual == expected if actual else "", "git_blob_sha": "", "status": status})
    return out


def preflight(a: Audit) -> list[dict[str, Any]]:
    out = []
    for name, (fatal, required) in REQUIRED_RELATIONS.items():
        schema, table = name.split(".", 1)
        found = a.query("""SELECT c.relkind::text relkind FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname=%s AND c.relname=%s AND c.relkind IN ('r','p','v','m','f')""", (schema, table), f"preflight:{name}")
        exists = bool(found)
        cols = set()
        if exists:
            cols = {r["column_name"] for r in a.query("SELECT column_name FROM information_schema.columns WHERE table_schema=%s AND table_name=%s ORDER BY ordinal_position", (schema, table), f"columns:{name}")}
        a.exists[name] = exists
        a.columns[name] = cols
        missing = sorted(set(required) - cols)
        code = ""
        status = "OK"
        if not exists:
            code = "D05_E_REQUIRED_RELATION_MISSING" if fatal else "D05_W_RELATION_ABSENT"
            status = "FATAL_MISSING_RELATION" if fatal else "ABSENT"
            a.fail(code, "FATAL" if fatal else "WARN", name, "relation absent")
        elif missing:
            code = "D05_E_REQUIRED_COLUMN_MISSING" if fatal else "D05_W_COLUMN_ABSENT"
            status = "FATAL_MISSING_COLUMNS" if fatal else "PARTIAL_COLUMNS"
            a.fail(code, "FATAL" if fatal else "WARN", name, f"missing={missing}")
        n = ""
        if exists:
            with a.conn.cursor() as cur:
                cur.execute(sql.SQL("SELECT COUNT(*)::bigint FROM {}").format(rel(name)))
                n = cur.fetchone()[0]
        kinds = {"r":"table", "p":"partitioned_table", "v":"view", "m":"materialized_view", "f":"foreign_table"}
        out.append({"relation": name, "relation_kind": kinds.get(found[0]["relkind"], found[0]["relkind"]) if found else "", "exists": exists, "fatal_if_absent": fatal, "required_columns_json": json.dumps(required), "actual_columns_json": json.dumps(sorted(cols)), "missing_columns_json": json.dumps(missing), "row_count": n, "status": status, "failure_code": code})
    return out


def source_wave(a: Audit) -> list[dict[str, Any]]:
    base = a.query("""
      SELECT r.source,COALESCE(r.wave,'') raw_wave,COALESCE(r.country_code,'') country_code,r.survey_year,
             COUNT(DISTINCT r.id)::bigint respondents,COUNT(resp.respondent_id)::bigint response_rows,
             COUNT(DISTINCT resp.respondent_id)::bigint responded_respondents,
             COUNT(DISTINCT UPPER(COALESCE(resp.var_code,''))) FILTER (WHERE resp.respondent_id IS NOT NULL)::bigint distinct_var_codes
      FROM public.survey_microdata_respondents r LEFT JOIN public.survey_microdata_responses resp ON resp.respondent_id=r.id
      GROUP BY 1,2,3,4 ORDER BY 1,2,3,4
    """, scope="source_wave")
    def counts(name: str) -> dict[tuple[str, str, str], dict[str, Any]]:
        if not a.exists.get(name): return {}
        query = sql.SQL("""SELECT source,COALESCE(wave,'') wave,COALESCE(country_code,'') country_code,string_agg(DISTINCT COALESCE(canonical_wave,''),'|' ORDER BY COALESCE(canonical_wave,'')) canonical_wave,COUNT(*)::bigint n,COUNT(DISTINCT respondent_id)::bigint respondents FROM {} GROUP BY 1,2,3""").format(rel(name))
        rr = a.query(query, scope=f"scope:{name}")
        return {(str(x['source']), str(x['wave']), str(x['country_code'])): x for x in rr}
    f = counts("public.v_ddm_response_long_facet_ready")
    au = counts("public.v_ddm_response_long_facet_ready_authority")
    out=[]
    for r in base:
        k=(str(r['source']),str(r['raw_wave']),str(r['country_code'])); x=f.get(k,{}); y=au.get(k,{})
        out.append({**r,"canonical_wave":y.get('canonical_wave') or x.get('canonical_wave') or r['raw_wave'],"facet_rows":x.get('n',''),"facet_respondents":x.get('respondents',''),"authority_facet_rows":y.get('n',''),"authority_facet_respondents":y.get('respondents',''),"raw_minus_facet_rows":int(r['response_rows'])-int(x['n']) if x else "","raw_minus_authority_rows":int(r['response_rows'])-int(y['n']) if y else ""})
    return out


def multiplicity(a: Audit) -> list[dict[str, Any]]:
    if not a.exists.get("public.question_structural_mapping"): return []
    return a.query("""
      WITH b AS (
        SELECT r.source,COALESCE(r.wave,'') wave,COALESCE(r.country_code,'') country_code,resp.respondent_id,UPPER(COALESCE(resp.var_code,'')) var_code,
          COALESCE((SELECT q.question_id FROM public.question_structural_mapping q WHERE q.source=r.source AND UPPER(q.var_code)=UPPER(resp.var_code) AND (q.wave=COALESCE(r.wave,'') OR q.wave='' OR q.wave IS NULL) ORDER BY CASE WHEN q.wave=COALESCE(r.wave,'') THEN 0 ELSE 1 END,q.loaded_at DESC NULLS LAST LIMIT 1),resp.var_code) question_id
        FROM public.survey_microdata_responses resp JOIN public.survey_microdata_respondents r ON r.id=resp.respondent_id
      ), rv AS (SELECT source,wave,country_code,respondent_id,var_code,COUNT(*)::bigint n FROM b GROUP BY 1,2,3,4,5),
      rq AS (SELECT source,wave,country_code,respondent_id,question_id,COUNT(*)::bigint n FROM b GROUP BY 1,2,3,4,5),
      pr AS (SELECT source,wave,country_code,respondent_id,COUNT(DISTINCT var_code)::bigint questions,COUNT(*)::bigint response_rows FROM b GROUP BY 1,2,3,4),
      d AS (SELECT source,wave,country_code,MIN(questions)::bigint min_questions_per_respondent,percentile_disc(.5) WITHIN GROUP(ORDER BY questions)::bigint p50_questions_per_respondent,percentile_disc(.9) WITHIN GROUP(ORDER BY questions)::bigint p90_questions_per_respondent,percentile_disc(.99) WITHIN GROUP(ORDER BY questions)::bigint p99_questions_per_respondent,MAX(questions)::bigint max_questions_per_respondent,MIN(response_rows)::bigint min_response_rows_per_respondent,percentile_disc(.5) WITHIN GROUP(ORDER BY response_rows)::bigint p50_response_rows_per_respondent,percentile_disc(.9) WITHIN GROUP(ORDER BY response_rows)::bigint p90_response_rows_per_respondent,percentile_disc(.99) WITHIN GROUP(ORDER BY response_rows)::bigint p99_response_rows_per_respondent,MAX(response_rows)::bigint max_response_rows_per_respondent FROM pr GROUP BY 1,2,3),
      g AS (SELECT b.source,b.wave,b.country_code,COUNT(DISTINCT b.respondent_id)::bigint respondents,COUNT(*)::bigint response_rows,COUNT(DISTINCT (b.respondent_id,b.var_code))::bigint distinct_respondent_var_pairs,(SELECT COUNT(*) FROM rv x WHERE (x.source,x.wave,x.country_code)=(b.source,b.wave,b.country_code) AND x.n>1)::bigint duplicate_var_pairs,(SELECT COALESCE(SUM(x.n-1),0) FROM rv x WHERE (x.source,x.wave,x.country_code)=(b.source,b.wave,b.country_code) AND x.n>1)::bigint duplicate_var_excess_rows,COUNT(DISTINCT (b.respondent_id,b.question_id))::bigint respondent_question_pairs,(SELECT COUNT(*) FROM rq x WHERE (x.source,x.wave,x.country_code)=(b.source,b.wave,b.country_code) AND x.n>1)::bigint duplicate_canonical_question_pairs,(SELECT COALESCE(SUM(x.n-1),0) FROM rq x WHERE (x.source,x.wave,x.country_code)=(b.source,b.wave,b.country_code) AND x.n>1)::bigint canonical_duplicate_excess_rows FROM b GROUP BY 1,2,3)
      SELECT g.*,d.min_questions_per_respondent,d.p50_questions_per_respondent,d.p90_questions_per_respondent,d.p99_questions_per_respondent,d.max_questions_per_respondent,d.min_response_rows_per_respondent,d.p50_response_rows_per_respondent,d.p90_response_rows_per_respondent,d.p99_response_rows_per_respondent,d.max_response_rows_per_respondent FROM g JOIN d USING(source,wave,country_code) ORDER BY 1,2,3
    """, scope="multiplicity")


def overlaps(a: Audit) -> list[dict[str, Any]]:
    rr=a.query("""
      WITH rq AS (SELECT r.source,COALESCE(r.wave,'') wave,COALESCE(r.country_code,'') country_code,resp.respondent_id,UPPER(resp.var_code) var_code,COUNT(*)::bigint n_rows FROM public.survey_microdata_responses resp JOIN public.survey_microdata_respondents r ON r.id=resp.respondent_id WHERE COALESCE(resp.var_code,'')<>'' GROUP BY 1,2,3,4,5),
      t AS (SELECT source,wave,country_code,var_code,COUNT(*)::bigint n FROM rq GROUP BY 1,2,3,4),
      p AS (SELECT x.source,x.wave,x.country_code,x.var_code question_x,y.var_code question_y,COUNT(*)::bigint ov,COUNT(*) FILTER(WHERE x.n_rows=1 AND y.n_rows=1)::bigint ov_unique,COUNT(*) FILTER(WHERE x.n_rows>1 OR y.n_rows>1)::bigint dup FROM rq x JOIN rq y ON y.source=x.source AND y.wave=x.wave AND y.country_code=x.country_code AND y.respondent_id=x.respondent_id AND y.var_code>x.var_code GROUP BY 1,2,3,4,5)
      SELECT p.*,tx.n respondents_x,ty.n respondents_y,(tx.n+ty.n-p.ov)::bigint respondents_union FROM p JOIN t tx ON (tx.source,tx.wave,tx.country_code,tx.var_code)=(p.source,p.wave,p.country_code,p.question_x) JOIN t ty ON (ty.source,ty.wave,ty.country_code,ty.var_code)=(p.source,p.wave,p.country_code,p.question_y) ORDER BY 1,2,3,4,5
    """, scope="question_overlap_all_pairs")
    out=[]
    for r in rr:
        ov=int(r['ov']); nx=int(r['respondents_x']); ny=int(r['respondents_y']); un=int(r['respondents_union'])
        out.append({"source":r['source'],"wave":r['wave'],"country_code":r['country_code'],"question_x":r['question_x'],"question_y":r['question_y'],"respondents_x":nx,"respondents_y":ny,"respondents_overlap":ov,"respondents_union":un,"overlap_pct_of_x":pct(ov,nx),"overlap_pct_of_y":pct(ov,ny),"jaccard_pct":pct(ov,un),"respondents_overlap_unique_each":r['ov_unique'],"cotravel_possible":ov>0,"duplicate_compromised_overlap":r['dup']})
    return out


def positions(a: Audit) -> list[dict[str, Any]]:
    name="public.respondent_position_fact"; out=[]
    if not a.exists.get(name): return out
    cols=a.columns[name]
    for field in [x for x in POSITION_FIELDS if x!="age_group"]:
        if field not in cols:
            out.append({"field_name":field,"field_origin":"required_position_surface","physical_column_present":False,"status":"COLUMN_ABSENT"}); continue
        query=sql.SQL("""SELECT COALESCE(source_family,'') source_family,COALESCE(wave,'') wave,COUNT(*)::bigint respondent_rows,COUNT(*) FILTER(WHERE NULLIF(BTRIM(COALESCE({f}::text,'')),'') IS NOT NULL)::bigint nonmissing_rows,COUNT(*) FILTER(WHERE NULLIF(BTRIM(COALESCE({f}::text,'')),'') IS NULL)::bigint missing_rows,COUNT(DISTINCT NULLIF(BTRIM(COALESCE({f}::text,'')),''))::bigint distinct_nonmissing_values FROM public.respondent_position_fact GROUP BY 1,2 ORDER BY 1,2""").format(f=sql.Identifier(field))
        for r in a.query(query, scope=f"position:{field}"):
            out.append({"field_name":field,"field_origin":"respondent_position_fact","source_family":r['source_family'],"wave":r['wave'],"respondent_rows":r['respondent_rows'],"nonmissing_rows":r['nonmissing_rows'],"missing_rows":r['missing_rows'],"coverage_pct":pct(r['nonmissing_rows'],r['respondent_rows']),"distinct_nonmissing_values":r['distinct_nonmissing_values'],"physical_column_present":True,"register_var_name":"","register_question_id":"","status":"OK"})
    out.append({"field_name":"age_group","field_origin":"facet_ready_derived_from_age","physical_column_present":"age_group" in a.columns.get("public.v_ddm_response_long_facet_ready",set()),"status":"DERIVED_NOT_POSITION_FACT"})
    reg="public.ddm_demographic_field_register"
    need={"source_family","wave","var_name","question_id","demographic_kind"}
    if a.exists.get(reg) and need.issubset(a.columns[reg]):
        for r in a.query("SELECT COALESCE(demographic_kind,'') field_name,COALESCE(source_family,'') source_family,COALESCE(wave,'') wave,COALESCE(var_name,'') register_var_name,COALESCE(question_id,'') register_question_id FROM public.ddm_demographic_field_register ORDER BY 2,3,1,4,5", scope="demographic_register"):
            out.append({**r,"field_origin":"demographic_field_register_candidate","physical_column_present":r['field_name'] in cols,"status":"REGISTER_CANDIDATE_NOT_ASSUMED_PHYSICAL"})
    return out


def weights(a: Audit) -> list[dict[str, Any]]:
    if not a.exists.get("public.survey_weight_fact"): return []
    rr=a.query("""
      WITH rr AS (SELECT source,COALESCE(wave,'') wave,COUNT(*)::bigint respondents FROM public.survey_microdata_respondents GROUP BY 1,2),
      w AS (SELECT r.source,COALESCE(r.wave,'') wave,COUNT(wf.*)::bigint weight_rows,COUNT(wf.*) FILTER(WHERE wf.is_primary)::bigint primary_weight_rows,COUNT(DISTINCT wf.respondent_id)::bigint respondents_with_any_weight,COUNT(DISTINCT wf.respondent_id) FILTER(WHERE wf.is_primary)::bigint respondents_with_primary_weight,COUNT(wf.*) FILTER(WHERE wf.is_primary AND wf.weight_value IS NULL)::bigint null_primary_weights,COUNT(wf.*) FILTER(WHERE wf.is_primary AND wf.weight_value=0)::bigint zero_primary_weights,COUNT(wf.*) FILTER(WHERE wf.is_primary AND wf.weight_value<0)::bigint negative_primary_weights,COUNT(wf.*) FILTER(WHERE wf.is_primary AND wf.weight_value::text IN ('NaN','Infinity','-Infinity'))::bigint nonfinite_primary_weights,jsonb_agg(DISTINCT wf.weight_name) FILTER(WHERE wf.weight_name IS NOT NULL)::text weight_names_json,jsonb_agg(DISTINCT wf.weight_type) FILTER(WHERE wf.weight_type IS NOT NULL)::text weight_types_json,jsonb_agg(DISTINCT wf.source_var) FILTER(WHERE wf.source_var IS NOT NULL)::text source_vars_json FROM public.survey_microdata_respondents r LEFT JOIN public.survey_weight_fact wf ON wf.respondent_id=r.id GROUP BY 1,2),
      m AS (SELECT source,wave,COUNT(*)::bigint n FROM (SELECT r.source,COALESCE(r.wave,'') wave,wf.respondent_id FROM public.survey_weight_fact wf JOIN public.survey_microdata_respondents r ON r.id=wf.respondent_id WHERE wf.is_primary GROUP BY 1,2,3 HAVING COUNT(*)>1) z GROUP BY 1,2)
      SELECT rr.source,rr.wave,rr.respondents,COALESCE(w.respondents_with_any_weight,0)::bigint respondents_with_any_weight,COALESCE(w.respondents_with_primary_weight,0)::bigint respondents_with_primary_weight,(rr.respondents-COALESCE(w.respondents_with_primary_weight,0))::bigint respondents_missing_primary_weight,COALESCE(m.n,0)::bigint respondents_with_multiple_primary_weights,COALESCE(w.weight_rows,0)::bigint weight_rows,COALESCE(w.primary_weight_rows,0)::bigint primary_weight_rows,COALESCE(w.null_primary_weights,0)::bigint null_primary_weights,COALESCE(w.zero_primary_weights,0)::bigint zero_primary_weights,COALESCE(w.negative_primary_weights,0)::bigint negative_primary_weights,COALESCE(w.nonfinite_primary_weights,0)::bigint nonfinite_primary_weights,COALESCE(w.weight_names_json,'[]') weight_names_json,COALESCE(w.weight_types_json,'[]') weight_types_json,COALESCE(w.source_vars_json,'[]') source_vars_json FROM rr LEFT JOIN w USING(source,wave) LEFT JOIN m USING(source,wave) ORDER BY 1,2
    """, scope="weights")
    for r in rr:
        path=sum(int(r[k]) for k in ["respondents_with_multiple_primary_weights","null_primary_weights","zero_primary_weights","negative_primary_weights","nonfinite_primary_weights"])
        r['status']='PATHOLOGY_PRESENT' if path else ('PRIMARY_WEIGHT_GAPS' if int(r['respondents_missing_primary_weight']) else 'OK')
    return rr


def joins(a: Audit) -> list[dict[str, Any]]:
    if not a.exists.get("public.question_structural_mapping"): return []
    rr=a.query("""
      WITH b AS (SELECT r.source,COALESCE(r.wave,'') wave,COALESCE(r.country_code,'') country_code,resp.var_code,
        (SELECT COUNT(*) FROM public.question_structural_mapping q WHERE q.source=r.source AND UPPER(q.var_code)=UPPER(resp.var_code) AND q.wave=COALESCE(r.wave,'')) exact_n,
        (SELECT COUNT(*) FROM public.question_structural_mapping q WHERE q.source=r.source AND UPPER(q.var_code)=UPPER(resp.var_code) AND (q.wave='' OR q.wave IS NULL)) fallback_n,
        (SELECT q.question_id FROM public.question_structural_mapping q WHERE q.source=r.source AND UPPER(q.var_code)=UPPER(resp.var_code) AND (q.wave=COALESCE(r.wave,'') OR q.wave='' OR q.wave IS NULL) ORDER BY CASE WHEN q.wave=COALESCE(r.wave,'') THEN 0 ELSE 1 END,q.loaded_at DESC NULLS LAST LIMIT 1) question_id,
        (SELECT COALESCE(q.mapping_status,'') FROM public.question_structural_mapping q WHERE q.source=r.source AND UPPER(q.var_code)=UPPER(resp.var_code) AND (q.wave=COALESCE(r.wave,'') OR q.wave='' OR q.wave IS NULL) ORDER BY CASE WHEN q.wave=COALESCE(r.wave,'') THEN 0 ELSE 1 END,q.loaded_at DESC NULLS LAST LIMIT 1) mapping_status
        FROM public.survey_microdata_responses resp JOIN public.survey_microdata_respondents r ON r.id=resp.respondent_id)
      SELECT source,wave,country_code,COUNT(*)::bigint response_rows,COUNT(*) FILTER(WHERE exact_n=1)::bigint exactly_joined_rows,COUNT(*) FILTER(WHERE exact_n=0 AND fallback_n=1)::bigint fallback_joined_rows,COUNT(*) FILTER(WHERE exact_n>1 OR (exact_n=0 AND fallback_n>1))::bigint ambiguous_rows,COUNT(*) FILTER(WHERE exact_n=0 AND fallback_n=0)::bigint unmapped_rows,COUNT(*) FILTER(WHERE LOWER(mapping_status) LIKE '%block%')::bigint blocked_rows,COUNT(*) FILTER(WHERE LOWER(mapping_status) LIKE '%exclud%')::bigint excluded_rows,COUNT(DISTINCT UPPER(COALESCE(var_code,'')))::bigint distinct_var_codes,COUNT(DISTINCT question_id)::bigint distinct_question_ids FROM b GROUP BY 1,2,3 ORDER BY 1,2,3
    """, scope="identity_join")
    for r in rr:
        r['exact_join_pct']=pct(r['exactly_joined_rows'],r['response_rows']); r['join_status']='AMBIGUOUS' if int(r['ambiguous_rows']) else ('UNMAPPED' if int(r['unmapped_rows']) else 'OK')
    return rr


def typed_missing(a: Audit) -> list[dict[str, Any]]:
    out=[]
    for name in ["public.v_ddm_response_long_facet_ready_authority","public.v_ddm_response_long_facet_ready"]:
        if not a.exists.get(name): continue
        cols=a.columns[name]
        for metric in TYPED_FLAGS:
            if metric not in cols:
                out.append({"relation":name,"metric":metric,"status":"COLUMN_NOT_EXPOSED"}); a.fail("D05_W_TYPED_MISSINGNESS_NOT_EXPOSED","WARN",name,f"{metric} absent"); continue
            query=sql.SQL("SELECT COALESCE(source,'') source,COALESCE(wave,'') wave,COALESCE(country_code,'') country_code,COUNT(*)::bigint rows,COUNT(*) FILTER(WHERE COALESCE({},false))::bigint flagged_rows FROM {} GROUP BY 1,2,3 ORDER BY 1,2,3").format(sql.Identifier(metric),rel(name))
            for r in a.query(query, scope=f"typed:{name}:{metric}"):
                out.append({"relation":name,**r,"metric":metric,"prevalence_pct":pct(r['flagged_rows'],r['rows']),"status":"OK"})
    return out


def topology(a: Audit) -> list[dict[str, Any]]:
    name=next((n for n in ["public.v_ddm_response_long_facet_ready_authority","public.v_ddm_response_long_facet_ready"] if a.exists.get(n)),None)
    if not name: return []
    c=a.columns[name]
    def expr(x: str, fallback: str="''") -> Any: return sql.Identifier(x) if x in c else sql.SQL(fallback)
    query=sql.SQL("""SELECT {lit} relation,COALESCE(source,'') source,COALESCE(wave,'') wave,COALESCE(var_code,'') var_code,{qid}::text question_id,{qt}::text question_type,{rt}::text response_topology,{hr}::text handling_rule,{ssc}::text source_structure_classification,COUNT(*)::bigint response_rows,COUNT(DISTINCT respondent_id)::bigint distinct_respondents,COUNT(DISTINCT {raw})::bigint distinct_raw_values,(COUNT(*)-COUNT(DISTINCT (respondent_id,var_code)))::bigint duplicate_respondent_var_pairs FROM {r} GROUP BY 1,2,3,4,5,6,7,8,9 ORDER BY 2,3,4""").format(lit=sql.Literal(name),qid=expr('question_id'),qt=expr('question_type'),rt=expr('response_topology'),hr=expr('handling_rule'),ssc=expr('source_structure_classification'),raw=expr('value_raw','var_code'),r=rel(name))
    rr=a.query(query,scope="topology")
    for r in rr: r['status']='AUTHORITY_TOPOLOGY_OBSERVED' if str(r.get('question_type') or r.get('response_topology') or '').strip() else 'TOPOLOGY_AUTHORITY_NOT_EXPOSED'
    return rr


def parity(a: Audit) -> list[dict[str, Any]]:
    out=[]
    for name in ["public.v_ddm_response_long_facet_ready","public.v_ddm_response_long_facet_ready_authority"]:
        if not a.exists.get(name): continue
        c=a.columns[name]; required={"respondent_id","source","wave","country_code","var_code"}
        if not required.issubset(c): continue
        rv='value_raw' in c; tv='value_text' in c
        query=sql.SQL("""WITH raw AS (SELECT r.source,COALESCE(r.wave,'') wave,COALESCE(r.country_code,'') country_code,resp.respondent_id,UPPER(COALESCE(resp.var_code,'')) var_code,COUNT(*)::bigint n,{ra} raw_values,{ta} text_values FROM public.survey_microdata_responses resp JOIN public.survey_microdata_respondents r ON r.id=resp.respondent_id GROUP BY 1,2,3,4,5),fac AS (SELECT source,COALESCE(wave,'') wave,COALESCE(country_code,'') country_code,respondent_id,UPPER(COALESCE(var_code,'')) var_code,COUNT(*)::bigint n,{fa} raw_values,{fta} text_values FROM {r} GROUP BY 1,2,3,4,5),cmp AS (SELECT COALESCE(raw.source,fac.source) source,COALESCE(raw.wave,fac.wave) wave,COALESCE(raw.country_code,fac.country_code) country_code,raw.n raw_n,fac.n fac_n,raw.raw_values rr,fac.raw_values fr,raw.text_values rt,fac.text_values ft FROM raw FULL OUTER JOIN fac USING(source,wave,country_code,respondent_id,var_code)) SELECT source,wave,country_code,COALESCE(SUM(raw_n),0)::bigint raw_rows,COALESCE(SUM(fac_n),0)::bigint facet_rows,COUNT(*) FILTER(WHERE raw_n IS NOT NULL)::bigint raw_keys,COUNT(*) FILTER(WHERE fac_n IS NOT NULL)::bigint facet_keys,COALESCE(SUM(raw_n) FILTER(WHERE fac_n IS NULL),0)::bigint raw_rows_missing_from_facet,COALESCE(SUM(fac_n) FILTER(WHERE raw_n IS NULL),0)::bigint facet_rows_without_raw,COUNT(*) FILTER(WHERE raw_n IS DISTINCT FROM fac_n AND raw_n IS NOT NULL AND fac_n IS NOT NULL)::bigint multiplicity_mismatch_keys,COUNT(*) FILTER(WHERE raw_n IS NOT NULL AND fac_n IS NOT NULL AND rr IS DISTINCT FROM fr)::bigint value_raw_mismatch_rows,COUNT(*) FILTER(WHERE raw_n IS NOT NULL AND fac_n IS NOT NULL AND rt IS DISTINCT FROM ft)::bigint value_text_mismatch_rows FROM cmp GROUP BY 1,2,3 ORDER BY 1,2,3""").format(ra=sql.SQL("jsonb_agg(COALESCE(resp.value_raw::text,'') ORDER BY COALESCE(resp.value_raw::text,''))") if rv else sql.SQL("'[]'::jsonb"),ta=sql.SQL("jsonb_agg(COALESCE(resp.value_text::text,'') ORDER BY COALESCE(resp.value_text::text,''))") if tv else sql.SQL("'[]'::jsonb"),fa=sql.SQL("jsonb_agg(COALESCE(value_raw::text,'') ORDER BY COALESCE(value_raw::text,''))") if rv else sql.SQL("'[]'::jsonb"),fta=sql.SQL("jsonb_agg(COALESCE(value_text::text,'') ORDER BY COALESCE(value_text::text,''))") if tv else sql.SQL("'[]'::jsonb"),r=rel(name))
        rr=a.query(query,scope=f"parity:{name}")
        position_ok=all(x in c for x in ["sex","age","education_level","income_level","religion_label","urban_rural","region","ethnicity","language","employment","marital","household_size"])
        for r in rr:
            ok=int(r['raw_rows_missing_from_facet'])==0 and int(r['facet_rows_without_raw'])==0 and int(r['multiplicity_mismatch_keys'])==0
            out.append({"relation":name,**r,"respondent_linkage_preserved":ok,"p_y_given_position_possible":ok and position_ok,"p_y_given_position_conjunction_possible":ok and position_ok,"p_y_given_x_response_possible":ok,"p_y_given_x_response_and_position_possible":ok and position_ok,"status":"ROW_AND_KEY_PARITY" if ok else "PARITY_FAILURE"})
    return out


def information_loss(a: Audit, mult: list[dict[str,Any]], w: list[dict[str,Any]], par: list[dict[str,Any]]) -> list[dict[str,Any]]:
    out=[]
    def add(surface,prop,evidence,value,invariant,status,code=""): out.append({"surface":surface,"property":prop,"evidence_type":evidence,"observed_value":value,"invariant":invariant,"status":status,"failure_code":code})
    orphan=a.query("SELECT COUNT(*)::bigint n FROM public.survey_microdata_responses x LEFT JOIN public.survey_microdata_respondents r ON r.id=x.respondent_id WHERE r.id IS NULL",scope="orphans")[0]['n']
    add('survey_microdata_responses','respondent_linkage','database',orphan,'orphan response rows = 0','PASS' if int(orphan)==0 else 'FAIL','D05_F_ORPHAN_RESPONSE' if int(orphan) else '')
    dup=sum(int(x['duplicate_var_excess_rows']) for x in mult); add('survey_microdata_responses','multiple_response_rows','database',dup,'multiplicity is measured rather than collapsed','PRESENT' if dup else 'ABSENT')
    for x in par:
        loss=int(x['raw_rows_missing_from_facet'])+int(x['facet_rows_without_raw'])+int(x['multiplicity_mismatch_keys']); add(x['relation'],'row_multiplicity_parity','database',loss,'facet preserves raw respondent/var multiplicity','PASS' if loss==0 else 'FAIL','D05_F_FACET_MULTIPLICITY_LOSS' if loss else '')
        add(x['relation'],'raw_code_multiset','database',x['value_raw_mismatch_rows'],'value_raw multiset preserved per respondent/var','PASS' if int(x['value_raw_mismatch_rows'])==0 else 'FAIL','D05_F_RAW_CODE_LOSS' if int(x['value_raw_mismatch_rows']) else '')
    mp=sum(int(x['respondents_with_multiple_primary_weights']) for x in w); add('facet_ready_weight_pick','multiple_primary_weights','database+implementation',mp,'at most one primary weight exists per respondent','PASS' if mp==0 else 'INFORMATION_SELECTION_RISK','D05_F_MULTIPLE_PRIMARY_WEIGHT_SELECTION' if mp else '')
    ac=a.columns.get('public.v_ddm_response_long_facet_ready_authority',set()); routing=any(x in ac for x in ['is_iap','routing_status','not_asked','asked_flag']); add('authority_facet_ready','routing_typed_state','schema',routing,'IAP/not-asked/routing state explicitly represented','PRESENT' if routing else 'UNPROVED_OR_ABSENT','D05_W_ROUTING_NOT_EXPOSED' if not routing else '')
    wc={x.lower() for x in a.columns.get('public.survey_weight_fact',set())}; design=sorted(wc & {'psu','stratum','strata','cluster','fpc','replicate_weight','variance_weight'}); add('survey_weight_fact','design_based_inference_metadata','schema',json.dumps(design),'scalar weight is not design authority','PRESENT' if design else 'NOT_REPRESENTED_IN_WEIGHT_FACT')
    # Static transformations known from current implementation; data checks above decide whether they actually lose rows.
    add('v_ddm_response_long_facet_ready','canonical_wave','implementation','COALESCE(r.wave,\'\')','historical facet-ready does not invent canonicalization beyond raw wave fallback','TRANSFORMATION_RECORDED')
    add('v_ddm_response_long_facet_ready','age_group','implementation','derived from age cutpoints <30,<45,<60,else 60+','age remains present alongside derived group','DERIVATION_RECORDED')
    add('v_ddm_response_long_facet_ready','question_mapping_choice','implementation','LATERAL ... ORDER BY exact-wave first, loaded_at DESC, LIMIT 1','ambiguous mapping candidates are separately counted by IDENTITY_JOIN_AUDIT','SELECTION_RECORDED')
    return out


def cache_audit(a: Audit) -> list[dict[str,Any]]:
    found=[]; root=a.repo/'data/ddm_repository_copy/v550'
    if root.exists(): found=list(root.rglob('v550_shared_respondent_substrate.parquet'))
    if not found:
        a.fail('D05_W_SHARED_CACHE_NOT_MATERIALIZED','WARN','v550_shared_respondent_substrate','no materialized shared substrate under data/ddm_repository_copy/v550')
        return [{"surface":"v550_shared_respondent_substrate","property":"materialized_cache","evidence_type":"filesystem","observed_value":"0 files","invariant":"materialized cache must be present to prove cache losslessness","status":"UNPROVED_NOT_MATERIALIZED","failure_code":"D05_W_SHARED_CACHE_NOT_MATERIALIZED"}]
    try: import pandas as pd
    except Exception as exc:
        return [{"surface":"v550_shared_respondent_substrate","property":"cache_read","evidence_type":"filesystem","observed_value":str(exc),"invariant":"cache must be readable","status":"UNPROVED_DEPENDENCY","failure_code":"D05_W_SHARED_CACHE_DEPENDENCY"}]
    req={"source","wave","canonical_wave","country_code","respondent_id","var_code","question_id","response_value","response_label","is_missing","is_dk","is_refusal","is_iap","is_valid_substantive_response","selection_role","base_fixture_selected","joint_configuration_selected"}; out=[]
    for p in sorted(found):
        try:
            df=pd.read_parquet(p); missing=sorted(req-set(df.columns)); selection=all(x in df.columns for x in ['selection_role','base_fixture_selected','joint_configuration_selected'])
            out.append({"surface":str(p.relative_to(a.repo)),"property":"cache_schema_and_selection","evidence_type":"filesystem","observed_value":json.dumps({"rows":len(df),"missing":missing,"selection_columns":selection},sort_keys=True),"invariant":"cache selection must be explicit and never equated to raw source equivalence","status":"SELECTIVE_CACHE" if selection else ('SCHEMA_COMPLETE' if not missing else 'SCHEMA_INCOMPLETE'),"failure_code":"D05_F_SHARED_CACHE_SCHEMA" if missing else ''})
        except Exception as exc: out.append({"surface":str(p.relative_to(a.repo)),"property":"cache_read","evidence_type":"filesystem","observed_value":str(exc),"invariant":"cache must be readable","status":"READ_FAILED","failure_code":"D05_W_SHARED_CACHE_READ"})
    return out


def invariants(a: Audit, mult, ov, w, j, par) -> None:
    n=a.query('SELECT COUNT(*)::bigint n,COUNT(DISTINCT id)::bigint d,COUNT(*) FILTER(WHERE id IS NULL)::bigint nulls FROM public.survey_microdata_respondents',scope='inv:id')[0]
    a.inv('D05-I-ID-001','survey_microdata_respondents','id globally unique',n['d'],n['n'],int(n['d'])==int(n['n']),'FATAL','D05_F_DUPLICATE_RESPONDENT_ID'); a.inv('D05-I-ID-002','survey_microdata_respondents','id non-null',n['nulls'],0,int(n['nulls'])==0,'FATAL','D05_F_NULL_RESPONDENT_ID')
    orphan=a.query('SELECT COUNT(*)::bigint n FROM public.survey_microdata_responses x LEFT JOIN public.survey_microdata_respondents r ON r.id=x.respondent_id WHERE r.id IS NULL',scope='inv:orphan')[0]['n']; a.inv('D05-I-ID-003','survey_microdata_responses','every response has respondent parent',orphan,0,int(orphan)==0,'FATAL','D05_F_ORPHAN_RESPONSE')
    for x in ov: a.inv('D05-I-OVL-001',f"{x['source']}|{x['wave']}|{x['country_code']}|{x['question_x']}|{x['question_y']}",'overlap <= both marginals',x['respondents_overlap'],f"<= {min(int(x['respondents_x']),int(x['respondents_y']))}",0<=int(x['respondents_overlap'])<=min(int(x['respondents_x']),int(x['respondents_y'])),'FATAL','D05_F_OVERLAP_IMPOSSIBLE')
    for x in w: a.inv('D05-I-WGT-001',f"{x['source']}|{x['wave']}",'primary-weight respondents <= respondents',x['respondents_with_primary_weight'],f"<= {x['respondents']}",int(x['respondents_with_primary_weight'])<=int(x['respondents']),'FATAL','D05_F_WEIGHT_CARDINALITY')
    for x in j:
        parts=sum(int(x[k]) for k in ['exactly_joined_rows','fallback_joined_rows','ambiguous_rows','unmapped_rows']); a.inv('D05-I-JOIN-001',f"{x['source']}|{x['wave']}|{x['country_code']}",'join buckets partition response rows',parts,x['response_rows'],parts==int(x['response_rows']),'FATAL','D05_F_JOIN_PARTITION')
    for x in par:
        loss=int(x['raw_rows_missing_from_facet'])+int(x['facet_rows_without_raw'])+int(x['multiplicity_mismatch_keys']); a.inv('D05-I-FACET-001',f"{x['relation']}|{x['source']}|{x['wave']}|{x['country_code']}",'facet respondent/var multiplicity equals raw',loss,0,loss==0,'FATAL','D05_F_FACET_MULTIPLICITY_LOSS')


def finish(a: Audit, verdict: str, source_equiv: str, db: dict[str,Any] | None = None) -> None:
    write_csv(a.out/'INVARIANT_RESULTS.csv',OUTPUTS['INVARIANT_RESULTS.csv'],a.invariants); write_csv(a.out/'FAILURES.csv',OUTPUTS['FAILURES.csv'],a.failures)
    payload={"court":"D05","contract_version":"D05-EMPIRICAL-SUBSTRATE-AUDIT-R2","verdict":verdict,"source_equivalent_classification":source_equiv,"started_at":a.started,"finished_at":utcnow(),"repository":{"branch":git(a.repo,'rev-parse','--abbrev-ref','HEAD'),"head_sha":git(a.repo,'rev-parse','HEAD'),"required_branch":REQUIRED_BRANCH,"base_sha":BASE_SHA},"database":db or {},"failure_counts":dict(Counter(x['severity'] for x in a.failures)),"failures":a.failures,"outputs":sorted(OUTPUTS),"output_schemas":OUTPUTS,"read_only_guarantee":"one PostgreSQL REPEATABLE READ, READ ONLY transaction; no DDL/DML"}
    (a.out/'AUDIT_RUN.json').write_text(json.dumps(payload,indent=2,sort_keys=True,default=str)+'\n',encoding='utf-8')


def args() -> argparse.Namespace:
    p=argparse.ArgumentParser(); p.add_argument('--database-url',default=os.getenv('DATABASE_URL','')); p.add_argument('--repo-root'); p.add_argument('--statement-timeout-ms',type=int,default=0); p.add_argument('--public-schema-path'); return p.parse_args()


def main() -> int:
    ar=args()
    try: root=repo_root(ar.repo_root)
    except Exception as exc: print(str(exc),file=sys.stderr); return 21
    a=Audit(root); branch=git(root,'rev-parse','--abbrev-ref','HEAD'); base_ok=subprocess.call(['git','-C',str(root),'merge-base','--is-ancestor',BASE_SHA,'HEAD'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)==0
    a.inv('D05-I-GIT-001','repository','required D05 branch',branch,REQUIRED_BRANCH,branch==REQUIRED_BRANCH,'FATAL','D05_E_WRONG_BRANCH'); a.inv('D05-I-GIT-002','repository','commanded base is ancestor',base_ok,True,base_ok,'FATAL','D05_E_WRONG_BASE')
    prov=static_provenance(a,ar.public_schema_path); write_csv(a.out/'STATIC_EVIDENCE_PROVENANCE.csv',OUTPUTS['STATIC_EVIDENCE_PROVENANCE.csv'],prov)
    if not ar.database_url:
        a.fail('D05_E_DATABASE_URL_MISSING','FATAL','database','DATABASE_URL / --database-url absent'); finish(a,'BLOCKED_MISSING_POPULATED_DATA_ACCESS','NOT_RUN'); return 10
    try:
        a.conn=psycopg2.connect(ar.database_url); a.conn.set_session(readonly=True,autocommit=False,isolation_level='REPEATABLE READ')
        with a.conn.cursor() as cur:
            if ar.statement_timeout_ms>0: cur.execute('SET LOCAL statement_timeout = %s',(ar.statement_timeout_ms,))
            cur.execute('SHOW transaction_read_only'); ro=str(cur.fetchone()[0]).lower()=='on'; cur.execute('SELECT current_database(),current_user,pg_is_in_recovery(),txid_current_snapshot()::text'); dbname,user,recovery,snapshot=cur.fetchone()
        a.inv('D05-I-DB-001','database','transaction read only',ro,True,ro,'FATAL','D05_E_NOT_READ_ONLY')
        if not ro: finish(a,'AUDIT_FAILED_NOT_READ_ONLY','NOT_RUN'); return 12
    except Exception as exc:
        a.fail('D05_E_DATABASE_CONNECT','FATAL','database',f"{type(exc).__name__}: {exc}"); finish(a,'BLOCKED_MISSING_POPULATED_DATA_ACCESS','NOT_RUN'); return 11
    try:
        pf=preflight(a); write_csv(a.out/'RELATION_PREFLIGHT.csv',OUTPUTS['RELATION_PREFLIGHT.csv'],pf)
        if any(x['severity']=='FATAL' and x['failure_code'] in {'D05_E_REQUIRED_RELATION_MISSING','D05_E_REQUIRED_COLUMN_MISSING'} for x in a.failures):
            finish(a,'AUDIT_BLOCKED_RELATION_CONTRACT','NOT_RUN'); a.conn.rollback(); return 13
        sw=source_wave(a); write_csv(a.out/'SOURCE_WAVE_READINESS.csv',OUTPUTS['SOURCE_WAVE_READINESS.csv'],sw)
        m=multiplicity(a); write_csv(a.out/'RESPONSE_MULTIPLICITY_AUDIT.csv',OUTPUTS['RESPONSE_MULTIPLICITY_AUDIT.csv'],m)
        ov=overlaps(a); write_csv(a.out/'QUESTION_OVERLAP_SUMMARY.csv',OUTPUTS['QUESTION_OVERLAP_SUMMARY.csv'],ov)
        pos=positions(a); write_csv(a.out/'POSITION_FIELD_COMPLETENESS.csv',OUTPUTS['POSITION_FIELD_COMPLETENESS.csv'],pos)
        w=weights(a); write_csv(a.out/'WEIGHT_COVERAGE.csv',OUTPUTS['WEIGHT_COVERAGE.csv'],w)
        j=joins(a); write_csv(a.out/'IDENTITY_JOIN_AUDIT.csv',OUTPUTS['IDENTITY_JOIN_AUDIT.csv'],j)
        tm=typed_missing(a); write_csv(a.out/'TYPED_MISSINGNESS_PREVALENCE.csv',OUTPUTS['TYPED_MISSINGNESS_PREVALENCE.csv'],tm)
        top=topology(a); write_csv(a.out/'RESPONSE_TOPOLOGY_AUDIT.csv',OUTPUTS['RESPONSE_TOPOLOGY_AUDIT.csv'],top)
        par=parity(a); write_csv(a.out/'FACET_READY_PARITY_AUDIT.csv',OUTPUTS['FACET_READY_PARITY_AUDIT.csv'],par)
        info=information_loss(a,m,w,par)+cache_audit(a); write_csv(a.out/'INFORMATION_LOSS_AUDIT.csv',OUTPUTS['INFORMATION_LOSS_AUDIT.csv'],info)
        invariants(a,m,ov,w,j,par)
        fatal=any(x['severity']=='FATAL' for x in a.failures); known_loss=any(x['status'] in {'FAIL','INFORMATION_SELECTION_RISK'} for x in info); unknown=any(x['status'] in {'UNPROVED_OR_ABSENT','NOT_REPRESENTED_IN_WEIGHT_FACT','UNPROVED_NOT_MATERIALIZED'} for x in info)
        source_equiv='NOT_SOURCE_EQUIVALENT' if fatal else ('DERIVED_CACHE_WITH_KNOWN_LOSS' if known_loss else ('POTENTIALLY_SOURCE_EQUIVALENT_UNPROVED' if unknown or par else 'DERIVED_CACHE_WITH_UNKNOWN_LOSS'))
        finish(a,'AUDIT_COMPLETE_WITH_FATAL_FINDINGS' if fatal else 'AUDIT_COMPLETE',source_equiv,{"database":dbname,"database_user":user,"pg_is_in_recovery":bool(recovery),"snapshot":snapshot,"transaction_read_only":True}); a.conn.rollback(); return 15 if fatal else 0
    except Exception as exc:
        a.fail('D05_E_QUERY_FAILED','FATAL','runtime',f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}")
        try: a.conn.rollback()
        except Exception: pass
        finish(a,'AUDIT_FAILED_QUERY','NOT_RUN'); return 15


if __name__ == '__main__':
    raise SystemExit(main())
