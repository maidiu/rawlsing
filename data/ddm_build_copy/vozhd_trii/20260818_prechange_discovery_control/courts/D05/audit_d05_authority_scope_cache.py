#!/usr/bin/env python3
"""D05 extended authority/scope/cache audit.

Called automatically by run_d05_empirical_audit.sh after the core runner. This
script adds the three checks that must not be replaced by schema inference:

1. current production R1 question-relation authority resolution for every
   populated raw source/wave/country/var identity;
2. canonical_question_registry reconciliation when the reconcile schema is
   physically installed, plus CLOSED_35 actual-vs-governed source/wave scope;
3. selected-row and predicate-preservation checks for every materialized V550
   shared respondent substrate parquet found under data/ddm_repository_copy/v550.

Database work is one REPEATABLE READ, READ ONLY transaction. No DDL/DML.
"""
from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import psycopg2
from psycopg2 import sql

BASE_SHA = "bf9a0434eb2096d5c4725cf483ec757fd319b6af"
BRANCH = "agent/vozhd-trii-d05-empirical-substrate"
COURT = Path("data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/courts/D05")
POSITION_FIELDS = ["sex", "age", "age_group", "education_level", "income_level", "religion_label", "urban_rural", "region", "ethnicity", "language", "employment", "marital", "household_size", "class_level"]

R1_FIELDS = ["source", "raw_wave", "canonical_wave", "country_code", "var_code", "response_rows", "r1_resolution_status", "r1_match_count", "r1_question_id", "r1_authority_status", "r1_relation_use_status", "r1_mapping_status", "r1_authority_rule_id", "r1_authority_sha256"]
CANON_FIELDS = ["source", "raw_wave", "canonical_wave", "country_code", "var_code", "response_rows", "registry_schema", "canonical_exact_matches", "alias_matches", "question_id", "disposition", "status"]
SCOPE_FIELDS = ["source", "raw_wave", "canonical_wave", "country_code", "respondents", "closed_35_expected", "status"]
CACHE_FIELDS = ["cache_path", "response_relation", "source", "wave", "canonical_wave", "country_code", "var_code", "cache_rows", "cache_respondents", "db_rows", "db_respondents", "row_count_equal", "respondent_count_equal", "position_fields_present_json", "missing_position_fields_json", "typed_missingness_present", "response_topology_fields_present", "selection_columns_present", "predicate_preserving", "status"]
FAIL_FIELDS = ["failure_code", "severity", "scope", "message"]


def git(repo: Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(repo), *args], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def root() -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / ".git").exists():
            return parent
    r = git(Path.cwd(), "rev-parse", "--show-toplevel")
    if not r:
        raise RuntimeError("D05_E_REPO_ROOT")
    return Path(r).resolve()


def write(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)


def dictrows(cur) -> list[dict[str, Any]]:
    names = [d.name if hasattr(d, "name") else d[0] for d in cur.description]
    return [dict(zip(names, row)) for row in cur.fetchall()]


def query(conn, text: Any, params: Any = None) -> list[dict[str, Any]]:
    with conn.cursor() as cur:
        cur.execute(text, params)
        return dictrows(cur)


def relation_exists(conn, schema: str, name: str) -> bool:
    return bool(query(conn, "SELECT 1 ok FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname=%s AND c.relname=%s AND c.relkind IN ('r','p','v','m','f')", (schema, name)))


def relation_columns(conn, schema: str, name: str) -> set[str]:
    return {r["column_name"] for r in query(conn, "SELECT column_name FROM information_schema.columns WHERE table_schema=%s AND table_name=%s", (schema, name))}


def discover_unique_schema(conn, table_name: str, failures: list[dict[str, str]]) -> str:
    rs = query(conn, "SELECT n.nspname schema_name FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace WHERE c.relname=%s AND c.relkind IN ('r','p','v','m','f') ORDER BY n.nspname", (table_name,))
    schemas = [r["schema_name"] for r in rs]
    if len(schemas) > 1:
        failures.append({"failure_code":"D05_E_AUTHORITY_SCHEMA_AMBIGUOUS","severity":"FATAL","scope":table_name,"message":f"multiple schemas={schemas}"})
        return ""
    if not schemas:
        failures.append({"failure_code":"D05_W_CANONICAL_REGISTRY_NOT_INSTALLED","severity":"WARN","scope":table_name,"message":"relation not installed"})
        return ""
    return schemas[0]


def raw_keys(conn) -> list[dict[str, Any]]:
    return query(conn, """
      SELECT r.source,COALESCE(r.wave,'') raw_wave,COALESCE(r.country_code,'') country_code,
             COALESCE(resp.var_code,'') var_code,COUNT(*)::bigint response_rows
      FROM public.survey_microdata_responses resp
      JOIN public.survey_microdata_respondents r ON r.id=resp.respondent_id
      GROUP BY 1,2,3,4 ORDER BY 1,2,3,4
    """)


def audit_r1(repo: Path, conn, keys: list[dict[str, Any]], failures: list[dict[str, str]]) -> tuple[list[dict[str, Any]], dict[tuple[str,str], bool]]:
    if str(repo) not in sys.path:
        sys.path.insert(0, str(repo))
    from data.ddm_build_copy.ddm_v550_question_relation_authority import (
        active_closed_35_waves,
        canonical_source_family,
        canonical_wave,
        load_question_relation_authority,
        resolve_question_relation_authority,
    )
    index = load_question_relation_authority()
    closed = {(s, w) for s, w, _ in active_closed_35_waves()}
    out=[]
    for k in keys:
        source = canonical_source_family(k["source"])
        wave = canonical_wave(source, k["raw_wave"])
        res = resolve_question_relation_authority(source_family=source, canonical_wave_value=wave, country_code=k["country_code"], var_code=k["var_code"], authority_path=index.path)
        row = res.authority_row or {}
        out.append({"source":k["source"],"raw_wave":k["raw_wave"],"canonical_wave":wave,"country_code":k["country_code"],"var_code":k["var_code"],"response_rows":k["response_rows"],"r1_resolution_status":res.status,"r1_match_count":res.match_count,"r1_question_id":row.get("question_id", ""),"r1_authority_status":row.get("authority_status", ""),"r1_relation_use_status":row.get("relation_use_status", ""),"r1_mapping_status":row.get("mapping_status", ""),"r1_authority_rule_id":row.get("authority_rule_id", ""),"r1_authority_sha256":index.file_sha256})
    return out, {x: True for x in closed}


def audit_canonical_registry(conn, keys: list[dict[str, Any]], failures: list[dict[str, str]]) -> list[dict[str, Any]]:
    schema = discover_unique_schema(conn, "canonical_question_registry", failures)
    if not schema:
        return []
    has_alias = relation_exists(conn, schema, "question_variable_alias")
    cqr = sql.SQL("{}.canonical_question_registry").format(sql.Identifier(schema))
    qva = sql.SQL("{}.question_variable_alias").format(sql.Identifier(schema))
    # Use production R1 canonicalizers for source/wave; registry identity itself is
    # exact after canonicalization. Alias matching follows the installed alias table.
    repo = root()
    if str(repo) not in sys.path: sys.path.insert(0, str(repo))
    from data.ddm_build_copy.ddm_v550_question_relation_authority import canonical_source_family, canonical_wave
    out=[]
    for k in keys:
        source=canonical_source_family(k["source"]); wave=canonical_wave(source,k["raw_wave"]); var=k["var_code"]
        exact_q = sql.SQL("SELECT question_id,COALESCE(disposition,'') disposition FROM {} WHERE canonical_source=%s AND canonical_wave=%s AND UPPER(canonical_var_code)=UPPER(%s)").format(cqr)
        exact=query(conn,exact_q,(source,wave,var))
        aliases=[]
        if has_alias:
            alias_q=sql.SQL("SELECT canonical_var_code FROM {} WHERE canonical_source=%s AND canonical_wave=%s AND (UPPER(raw_var_code)=UPPER(%s) OR normalized_raw_var_key=LOWER(%s))").format(qva)
            aliases=query(conn,alias_q,(source,wave,var,var))
        canonical_vars=sorted({r["canonical_var_code"] for r in aliases})
        alias_rows=[]
        for cv in canonical_vars:
            alias_rows.extend(query(conn,exact_q,(source,wave,cv)))
        all_rows=exact+alias_rows
        uniq={(str(r.get('question_id','')),str(r.get('disposition',''))) for r in all_rows}
        if len(uniq)==1:
            qid,disp=next(iter(uniq)); status='EXACT' if exact else 'ALIAS'
        elif len(uniq)>1:
            qid=disp=''; status='AMBIGUOUS'
        else:
            qid=disp=''; status='UNMAPPED'
        out.append({"source":k['source'],"raw_wave":k['raw_wave'],"canonical_wave":wave,"country_code":k['country_code'],"var_code":var,"response_rows":k['response_rows'],"registry_schema":schema,"canonical_exact_matches":len(exact),"alias_matches":len(alias_rows),"question_id":qid,"disposition":disp,"status":status})
    return out


def audit_scope(conn, closed_map: dict[tuple[str,str],bool]) -> list[dict[str,Any]]:
    repo=root()
    if str(repo) not in sys.path: sys.path.insert(0,str(repo))
    from data.ddm_build_copy.ddm_v550_question_relation_authority import canonical_source_family, canonical_wave
    rs=query(conn,"SELECT source,COALESCE(wave,'') raw_wave,COALESCE(country_code,'') country_code,COUNT(*)::bigint respondents FROM public.survey_microdata_respondents GROUP BY 1,2,3 ORDER BY 1,2,3")
    out=[]
    for r in rs:
        s=canonical_source_family(r['source']); w=canonical_wave(s,r['raw_wave']); expected=(s,w) in closed_map
        out.append({"source":r['source'],"raw_wave":r['raw_wave'],"canonical_wave":w,"country_code":r['country_code'],"respondents":r['respondents'],"closed_35_expected":expected,"status":"EXPECTED_POPULATED" if expected else "POPULATED_OUTSIDE_CLOSED_35"})
    present={(canonical_source_family(r['source']),canonical_wave(canonical_source_family(r['source']),r['raw_wave'])) for r in rs}
    for s,w in sorted(closed_map):
        if (s,w) not in present:
            out.append({"source":s,"raw_wave":"","canonical_wave":w,"country_code":"","respondents":0,"closed_35_expected":True,"status":"EXPECTED_WAVE_NOT_POPULATED"})
    return out


def choose_response_relation(conn) -> str:
    for name in ["v_ddm_response_long_facet_ready_authority","v_ddm_response_long_facet_ready"]:
        if relation_exists(conn,"public",name): return f"public.{name}"
    return ""


def audit_cache(repo: Path, conn, failures: list[dict[str,str]]) -> list[dict[str,Any]]:
    paths=sorted((repo/"data/ddm_repository_copy/v550").rglob("v550_shared_respondent_substrate.parquet")) if (repo/"data/ddm_repository_copy/v550").exists() else []
    if not paths:
        failures.append({"failure_code":"D05_W_SHARED_CACHE_NOT_MATERIALIZED","severity":"WARN","scope":"v550_shared_respondent_substrate","message":"no materialized cache found"}); return []
    try:
        import pandas as pd
    except Exception as exc:
        failures.append({"failure_code":"D05_W_SHARED_CACHE_DEPENDENCY","severity":"WARN","scope":"cache","message":str(exc)}); return []
    response_rel=choose_response_relation(conn)
    if not response_rel:
        failures.append({"failure_code":"D05_E_RESPONSE_RELATION_MISSING","severity":"FATAL","scope":"cache","message":"neither governed response relation exists"}); return []
    schema,table=response_rel.split('.',1); dbcols=relation_columns(conn,schema,table)
    out=[]
    for path in paths:
        try: df=pd.read_parquet(path)
        except Exception as exc:
            failures.append({"failure_code":"D05_W_SHARED_CACHE_READ","severity":"WARN","scope":str(path),"message":str(exc)}); continue
        required={"source","wave","canonical_wave","country_code","respondent_id","var_code"}
        if not required.issubset(df.columns):
            failures.append({"failure_code":"D05_F_SHARED_CACHE_SCHEMA","severity":"FATAL","scope":str(path),"message":f"missing={sorted(required-set(df.columns))}"}); continue
        present_pos=sorted(set(POSITION_FIELDS)&set(df.columns)); missing_pos=sorted(set(POSITION_FIELDS)-set(df.columns))
        typed=all(x in df.columns for x in ["is_missing","is_dk","is_refusal","is_iap","is_valid_substantive_response"])
        topology=all(x in df.columns for x in ["question_type","handling_rule"])
        selection=all(x in df.columns for x in ["selection_role","base_fixture_selected","joint_configuration_selected"])
        grp=df.groupby(["source","wave","canonical_wave","country_code","var_code"],dropna=False).agg(cache_rows=("respondent_id","size"),cache_respondents=("respondent_id","nunique")).reset_index()
        for g in grp.itertuples(index=False):
            name_sql=sql.SQL("{}.{}").format(sql.Identifier(schema),sql.Identifier(table))
            q=sql.SQL("SELECT COUNT(*)::bigint db_rows,COUNT(DISTINCT respondent_id)::bigint db_respondents FROM {} WHERE source=%s AND COALESCE(wave,'')=%s AND COALESCE(country_code,'')=%s AND UPPER(COALESCE(var_code,''))=UPPER(%s)").format(name_sql)
            d=query(conn,q,(str(g.source),str(g.wave),str(g.country_code),str(g.var_code)))[0]
            roweq=int(g.cache_rows)==int(d['db_rows']); respeq=int(g.cache_respondents)==int(d['db_respondents']); pred=(not missing_pos) and typed and topology
            status='SELECTED_ROW_PARITY' if roweq and respeq else 'CACHE_SELECTED_ROW_MISMATCH'
            if status!='SELECTED_ROW_PARITY': failures.append({"failure_code":"D05_F_SHARED_CACHE_PARITY","severity":"FATAL","scope":str(path),"message":f"{g.source}|{g.wave}|{g.country_code}|{g.var_code}: cache_rows={g.cache_rows}, db_rows={d['db_rows']}"})
            if missing_pos: status = status + '|POSITION_PREDICATES_INCOMPLETE'
            out.append({"cache_path":str(path.relative_to(repo)),"response_relation":response_rel,"source":g.source,"wave":g.wave,"canonical_wave":g.canonical_wave,"country_code":g.country_code,"var_code":g.var_code,"cache_rows":int(g.cache_rows),"cache_respondents":int(g.cache_respondents),"db_rows":int(d['db_rows']),"db_respondents":int(d['db_respondents']),"row_count_equal":roweq,"respondent_count_equal":respeq,"position_fields_present_json":json.dumps(present_pos),"missing_position_fields_json":json.dumps(missing_pos),"typed_missingness_present":typed,"response_topology_fields_present":topology,"selection_columns_present":selection,"predicate_preserving":pred,"status":status})
    return out


def main() -> int:
    repo=root(); out=repo/COURT; failures=[]
    if git(repo,"rev-parse","--abbrev-ref","HEAD") != BRANCH:
        failures.append({"failure_code":"D05_E_WRONG_BRANCH","severity":"FATAL","scope":"repository","message":"wrong branch"})
    db=os.getenv("DATABASE_URL","")
    if not db:
        write(out/"EXTENDED_FAILURES.csv",FAIL_FIELDS,[{"failure_code":"D05_E_DATABASE_URL_MISSING","severity":"FATAL","scope":"database","message":"DATABASE_URL absent"}]); return 10
    conn=psycopg2.connect(db); conn.set_session(readonly=True,autocommit=False,isolation_level='REPEATABLE READ')
    try:
        ro=query(conn,"SHOW transaction_read_only")[0]["transaction_read_only"]
        if str(ro).lower()!='on': raise RuntimeError("D05_E_NOT_READ_ONLY")
        keys=raw_keys(conn)
        r1,closed=audit_r1(repo,conn,keys,failures); write(out/"R1_AUTHORITY_JOIN_AUDIT.csv",R1_FIELDS,r1)
        canon=audit_canonical_registry(conn,keys,failures); write(out/"CANONICAL_REGISTRY_JOIN_AUDIT.csv",CANON_FIELDS,canon)
        scope=audit_scope(conn,closed); write(out/"GOVERNED_SCOPE_COMPARISON.csv",SCOPE_FIELDS,scope)
        cache=audit_cache(repo,conn,failures); write(out/"CACHE_SELECTED_PARITY.csv",CACHE_FIELDS,cache)
        write(out/"EXTENDED_FAILURES.csv",FAIL_FIELDS,failures)
        summary={"r1_raw_keys":len(r1),"r1_response_rows_resolved":sum(int(x['response_rows']) for x in r1 if str(x['r1_resolution_status']).startswith('RESOLVED_')),"r1_response_rows_blocked":sum(int(x['response_rows']) for x in r1 if str(x['r1_resolution_status']).startswith('BLOCKED_')),"canonical_registry_installed":bool(canon),"canonical_unmapped_response_rows":sum(int(x['response_rows']) for x in canon if x['status']=='UNMAPPED'),"canonical_ambiguous_response_rows":sum(int(x['response_rows']) for x in canon if x['status']=='AMBIGUOUS'),"closed_35_missing_waves":sum(1 for x in scope if x['status']=='EXPECTED_WAVE_NOT_POPULATED'),"populated_outside_closed_35_rows":sum(1 for x in scope if x['status']=='POPULATED_OUTSIDE_CLOSED_35'),"cache_groups_audited":len(cache),"cache_parity_failures":sum(1 for x in cache if 'CACHE_SELECTED_ROW_MISMATCH' in x['status']),"predicate_incomplete_cache_groups":sum(1 for x in cache if not x['predicate_preserving']),"failures":failures}
        (out/"EXTENDED_AUDIT_SUMMARY.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        conn.rollback(); return 15 if any(x['severity']=='FATAL' for x in failures) else 0
    except Exception as exc:
        conn.rollback(); failures.append({"failure_code":"D05_E_EXTENDED_QUERY_FAILED","severity":"FATAL","scope":"runtime","message":f"{type(exc).__name__}: {exc}"}); write(out/"EXTENDED_FAILURES.csv",FAIL_FIELDS,failures); return 15


if __name__ == "__main__":
    raise SystemExit(main())
