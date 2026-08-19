#!/usr/bin/env python3
"""D05 exact respondent-ID preservation for materialized V550 shared caches.

Row counts and distinct-respondent counts are insufficient: two different ID
sets can have identical cardinality. This pass compares exact respondent-ID sets
for every physically selected source/wave/country/var cache group against the
current production response relation. It records set hashes plus missing/extra
counts and never exports the respondent IDs themselves.

Database access is REPEATABLE READ, READ ONLY. No DDL/DML.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

import psycopg2
from psycopg2 import sql

COURT=Path("data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/courts/D05")
FIELDS=["cache_path","response_relation","source","wave","canonical_wave","country_code","var_code","cache_respondent_id_count","db_respondent_id_count","cache_respondent_id_set_sha256","db_respondent_id_set_sha256","missing_db_ids_in_cache","extra_cache_ids_not_in_db","raw_respondent_id_set_equal","normalized_id_column_present","normalized_respondent_id_set_sha256","normalized_id_set_equal_to_db","status"]
FAIL_FIELDS=["failure_code","severity","scope","message"]


def root()->Path:
    return Path(subprocess.check_output(["git","rev-parse","--show-toplevel"],text=True).strip())


def write(path:Path,fields,rows):
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore"); w.writeheader(); w.writerows(rows)


def qrows(conn,text,params=None):
    with conn.cursor() as cur:
        cur.execute(text,params); names=[d.name if hasattr(d,"name") else d[0] for d in cur.description]
        return [dict(zip(names,r)) for r in cur.fetchall()]


def relation_exists(conn,name:str)->bool:
    return bool(qrows(conn,"SELECT 1 ok FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relname=%s AND c.relkind IN ('r','p','v','m','f')",(name,)))


def choose_relation(conn)->str:
    for n in ["v_ddm_response_long_facet_ready_authority","v_ddm_response_long_facet_ready"]:
        if relation_exists(conn,n): return f"public.{n}"
    return ""


def canon(v:Any)->str:
    if v is None: return ""
    s=str(v).strip()
    return "" if s.lower() in {"nan","none","null"} else s


def id_hash(values:set[str])->str:
    h=hashlib.sha256()
    for v in sorted(values):
        h.update(v.encode("utf-8")); h.update(b"\n")
    return h.hexdigest()


def main()->int:
    repo=root(); outdir=repo/COURT; failures=[]; db=os.getenv("DATABASE_URL","")
    if not db:
        write(outdir/"CACHE_IDENTITY_FAILURES.csv",FAIL_FIELDS,[{"failure_code":"D05_E_DATABASE_URL_MISSING","severity":"FATAL","scope":"database","message":"DATABASE_URL absent"}]); return 10
    try:
        import pandas as pd
    except Exception as exc:
        write(outdir/"CACHE_IDENTITY_FAILURES.csv",FAIL_FIELDS,[{"failure_code":"D05_W_SHARED_CACHE_DEPENDENCY","severity":"WARN","scope":"cache","message":str(exc)}]); return 0
    paths=sorted((repo/"data/ddm_repository_copy/v550").rglob("v550_shared_respondent_substrate.parquet")) if (repo/"data/ddm_repository_copy/v550").exists() else []
    if not paths:
        write(outdir/"CACHE_IDENTITY_EXACT.csv",FIELDS,[]); write(outdir/"CACHE_IDENTITY_FAILURES.csv",FAIL_FIELDS,[{"failure_code":"D05_W_SHARED_CACHE_NOT_MATERIALIZED","severity":"WARN","scope":"cache","message":"no shared substrate parquet found"}]); return 0
    conn=psycopg2.connect(db); conn.set_session(readonly=True,autocommit=False,isolation_level="REPEATABLE READ")
    try:
        if str(qrows(conn,"SHOW transaction_read_only")[0]["transaction_read_only"]).lower()!="on": raise RuntimeError("D05_E_NOT_READ_ONLY")
        relation=choose_relation(conn)
        if not relation: raise RuntimeError("D05_E_RESPONSE_RELATION_MISSING")
        schema,table=relation.split(".",1); rsql=sql.SQL("{}.{}").format(sql.Identifier(schema),sql.Identifier(table)); outputs=[]
        for path in paths:
            df=pd.read_parquet(path)
            required={"source","wave","canonical_wave","country_code","var_code","respondent_id"}
            if not required.issubset(df.columns):
                failures.append({"failure_code":"D05_F_SHARED_CACHE_SCHEMA","severity":"FATAL","scope":str(path),"message":f"missing={sorted(required-set(df.columns))}"}); continue
            keys=["source","wave","canonical_wave","country_code","var_code"]
            for key,group in df.groupby(keys,dropna=False):
                source,wave,cwave,country,var=map(canon,key)
                cache_ids={canon(v) for v in group["respondent_id"].tolist() if canon(v)}
                query=sql.SQL("SELECT DISTINCT respondent_id::text respondent_id FROM {} WHERE source=%s AND COALESCE(wave,'')=%s AND COALESCE(country_code,'')=%s AND UPPER(COALESCE(var_code,''))=UPPER(%s)").format(rsql)
                db_ids={canon(r["respondent_id"]) for r in qrows(conn,query,(source,wave,country,var)) if canon(r["respondent_id"])}
                missing=db_ids-cache_ids; extra=cache_ids-db_ids; raw_eq=not missing and not extra
                norm_present="respondent_id_norm" in group.columns
                norm_ids={canon(v) for v in group["respondent_id_norm"].tolist() if canon(v)} if norm_present else set()
                norm_eq=norm_present and norm_ids==db_ids
                status="EXACT_ID_SET_PARITY" if raw_eq else "RESPONDENT_ID_SET_MISMATCH"
                if not raw_eq:
                    failures.append({"failure_code":"D05_F_SHARED_CACHE_RESPONDENT_ID_DRIFT","severity":"FATAL","scope":str(path),"message":f"{source}|{wave}|{country}|{var}: missing={len(missing)} extra={len(extra)}"})
                outputs.append({"cache_path":str(path.relative_to(repo)),"response_relation":relation,"source":source,"wave":wave,"canonical_wave":cwave,"country_code":country,"var_code":var,"cache_respondent_id_count":len(cache_ids),"db_respondent_id_count":len(db_ids),"cache_respondent_id_set_sha256":id_hash(cache_ids),"db_respondent_id_set_sha256":id_hash(db_ids),"missing_db_ids_in_cache":len(missing),"extra_cache_ids_not_in_db":len(extra),"raw_respondent_id_set_equal":raw_eq,"normalized_id_column_present":norm_present,"normalized_respondent_id_set_sha256":id_hash(norm_ids) if norm_present else "","normalized_id_set_equal_to_db":norm_eq if norm_present else "","status":status})
        write(outdir/"CACHE_IDENTITY_EXACT.csv",FIELDS,outputs); write(outdir/"CACHE_IDENTITY_FAILURES.csv",FAIL_FIELDS,failures); conn.rollback(); return 15 if any(x["severity"]=="FATAL" for x in failures) else 0
    except Exception as exc:
        conn.rollback(); failures.append({"failure_code":"D05_E_CACHE_IDENTITY_QUERY_FAILED","severity":"FATAL","scope":"runtime","message":f"{type(exc).__name__}: {exc}"}); write(outdir/"CACHE_IDENTITY_FAILURES.csv",FAIL_FIELDS,failures); return 15


if __name__=="__main__": raise SystemExit(main())
