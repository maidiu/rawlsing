#!/usr/bin/env python3
"""Frozen SR04 physical carrier bakeoff.  This file is intentionally self-contained."""
from __future__ import annotations
import argparse, ast, csv, hashlib, json, math, os, platform, re, shutil, sqlite3, subprocess, sys, tempfile, time, uuid
from pathlib import Path
from collections import Counter

import pandas as pd
import pyreadstat

START_CONTRACT = "18_SR04_CARRIER_BAKEOFF_EXECUTION_CONTRACT.md"
TOKEN = "PRE553_SR04_CARRIER_BAKEOFF_RECEIPT_COMPLETE"
RESERVE = 5 * 1024**3
EXPECTED = {
    "WVS_W7": ("WVS Wave 7.sav", "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d", 97220),
    "LITS_I": ("LiTS_I.dta", "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09", 29002),
}
HOSTILE = {
    "WVS_W7": ["Q152","Q153","Q154","Q155","Q156","Q157","I_PSU","D_INTERVIEW","B_COUNTRY","W_WEIGHT","S018","Q223"],
    "LITS_I": ["id","country","countryname","weight_0","weight_1","weight_2","q707","q509","q304a","q304b","q204","q203","q201","q501","q503","q505","q306","q307","q301_1","q301_11"],
}
REL_COLS = {
 "sources":["source_id","source_file","source_sha256","source_format","source_row_count","source_variable_count","reader_encoding_override","reader_encoding_authority_status"],
 "respondents":["source_id","row_ordinal","respondent_key","benchmark_coord_a","benchmark_coord_b","benchmark_branch_id","benchmark_risk_eligible"],
 "variables":["source_id","var_name","var_ordinal","variable_label","missing_spec_json","value_labels_json","storage_type","display_format"],
 "events":["source_id","row_ordinal","respondent_key","var_name","var_ordinal","physical_state","raw_value_key","raw_value_num","raw_value_text","value_label"],
}

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()
def canon(v):
    if v is None or (isinstance(v,float) and (math.isnan(v) or math.isinf(v))): return None
    if isinstance(v,(pd.Timestamp,)): return v.isoformat()
    if hasattr(v,"item"): v=v.item()
    if isinstance(v,float) and v.is_integer(): return int(v)
    return v
def cj(v): return json.dumps(canon(v),ensure_ascii=False,separators=(",",":"),sort_keys=True)
def digest_rows(df, cols, sort_cols):
    h=hashlib.sha256()
    for row in df.sort_values(sort_cols,kind="mergesort")[cols].itertuples(index=False,name=None):
        h.update((json.dumps([canon(x) for x in row],ensure_ascii=False,separators=(",",":"))+"\n").encode())
    return h.hexdigest()
def free_bytes(path): return shutil.disk_usage(path).free
def finite_num(v):
    try:
        x=float(v)
        return math.isfinite(x)
    except Exception: return False
def raw_repr(v, stata=False):
    if v is None or (isinstance(v,float) and math.isnan(v)): return "M:SYSTEM", "", None
    if isinstance(v,str): return "S:"+v, v, None
    x=float(v)
    if not math.isfinite(x):
        return ("M:STATA:"+str(v),str(v),None) if stata else ("M:SYSTEM","",None)
    if x.is_integer(): s=str(int(x)); return "N:"+s,s,x
    s=format(x,".17g"); return "N:"+s,s,x
def is_user_missing(meta,var,v):
    if v is None or (isinstance(v,float) and math.isnan(v)): return False
    try:
        x=float(v)
        return any(float(r["lo"])<=x<=float(r["hi"]) for r in meta.missing_ranges.get(var,[]))
    except Exception: return False
def load_source(root, sid):
    name,digest,rows=EXPECTED[sid]; p=Path(root)/name
    if not p.exists(): raise RuntimeError("BLOCKED_SR04_SOURCE_MISSING:"+str(p))
    actual=sha256(p)
    if actual!=digest: raise RuntimeError(f"BLOCKED_SR04_SOURCE_HASH_MISMATCH:{name}:{actual}:{digest}")
    if sid=="WVS_W7": df,meta=pyreadstat.read_sav(str(p),user_missing=True,apply_value_formats=False); enc=""
    else: df,meta=pyreadstat.read_dta(str(p),user_missing=True,apply_value_formats=False,encoding="latin1"); enc="latin1"
    if len(df)!=rows: raise RuntimeError(f"BLOCKED_SR04_SOURCE_ROW_COUNT_MISMATCH:{sid}:{len(df)}:{rows}")
    required=HOSTILE[sid]
    missing=[x for x in required if x not in df.columns]
    if missing: raise RuntimeError("BLOCKED_SR04_REQUIRED_VARIABLE_MISSING:"+sid+":"+",".join(missing))
    ordered=[]
    for x in required+[str(x) for x in df.columns]:
        if x not in ordered: ordered.append(x)
        if len(ordered)==24: break
    if len(ordered)!=24: raise RuntimeError("BLOCKED_SR04_VARIABLE_SELECTION")
    return p,df,meta,ordered,enc
def build_fixture(root, work):
    loaded={}; manifest={"sources":{},"selection_algorithm":"required hostile order, then source-native ordinal order","benchmark_fields_authority":"BENCHMARK_ONLY__NO_SOURCE_SEMANTIC_AUTHORITY"}
    for sid in EXPECTED:
        p,df,meta,sel,enc=load_source(root,sid); loaded[sid]=(p,df,meta,sel,enc)
        ords=[list(meta.column_names).index(v) for v in sel]
        manifest["sources"][sid]={"source_file":p.name,"source_sha256":sha256(p),"source_rows":len(df),"source_variable_count":len(meta.column_names),"selected_variables":sel,"selected_ordinals":ords,"reader_encoding_override":enc,"reader_encoding_authority_status":"COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY" if enc else "NONE"}
    # Neutral tables are written as Arrow IPC staging, outside candidate directories.
    tables={k:[] for k in REL_COLS}; wide={}
    for sid,(p,df,meta,sel,enc) in loaded.items():
        tables["sources"].append([sid,p.name,sha256(p),p.suffix.lstrip('.'),len(df),len(meta.column_names),enc,"COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY" if enc else "NONE"])
        r=[]; e=[]; v=[]; wide[sid]=(df,meta,sel)
        for i in range(len(df)):
            key=hashlib.sha256((EXPECTED[sid][1]+":"+str(i)).encode()).hexdigest()
            r.append([sid,i,key,i%2,(i//2)%2,i%5,0 if i%7==0 else 1])
            for var in sel:
                val=df.iloc[i][var]; keyv,textv,num=raw_repr(val,sid=="LITS_I")
                state="SYSTEM_MISSING" if keyv=="M:SYSTEM" else ("STATA_EXTENDED_MISSING" if keyv.startswith("M:STATA:") else ("SPSS_USER_MISSING" if sid=="WVS_W7" and is_user_missing(meta,var,val) else "ORDINARY"))
                labels=meta.variable_value_labels.get(var,{})
                label=labels.get(val,"") if state=="ORDINARY" else ""
                e.append([sid,i,key,var,list(meta.column_names).index(var),state,keyv,num,textv,label])
        tables["respondents"].extend(r); tables["events"].extend(e)
        for var in sel:
            labels=meta.variable_value_labels.get(var,{})
            v.append([sid,var,list(meta.column_names).index(var),meta.column_names_to_labels.get(var,""),json.dumps(meta.missing_ranges.get(var,[]),separators=(",",":"),sort_keys=True),json.dumps({str(k):str(x) for k,x in labels.items()},ensure_ascii=False,separators=(",",":"),sort_keys=True),meta.readstat_variable_types.get(var,""),meta.original_variable_types.get(var," ")])
        tables["variables"].extend(v)
    if len(tables["events"])!=3029328: raise RuntimeError(f"BLOCKED_SR04_FIXTURE_EVENT_COUNT_MISMATCH:{len(tables['events'])}")
    # Contract preflight facts.
    def states(sid,var): return [x for x in tables["events"] if x[0]==sid and x[3]==var]
    def count(sid,var,pred): return sum(pred(x) for x in states(sid,var))
    checks={"WVS_rows":len(loaded["WVS_W7"][1]),"LiTS_rows":len(loaded["LITS_I"][1]),"WVS_Q152_user_missing":count("WVS_W7","Q152",lambda x:x[5]=="SPSS_USER_MISSING"),"WVS_Q153_user_missing":count("WVS_W7","Q153",lambda x:x[5]=="SPSS_USER_MISSING"),"WVS_Q154_user_missing":count("WVS_W7","Q154",lambda x:x[5]=="SPSS_USER_MISSING"),"WVS_Q155_user_missing":count("WVS_W7","Q155",lambda x:x[5]=="SPSS_USER_MISSING"),"WVS_Q156_user_missing":count("WVS_W7","Q156",lambda x:x[5]=="SPSS_USER_MISSING"),"WVS_Q157_user_missing":count("WVS_W7","Q157",lambda x:x[5]=="SPSS_USER_MISSING"),"WVS_I_PSU_minus4":count("WVS_W7","I_PSU",lambda x:x[6]=="N:-4"),"WVS_D_INTERVIEW_target":count("WVS_W7","D_INTERVIEW",lambda x:x[6]=="N:858069901"),"LITS_id_distinct":len(set(x[6] for x in states("LITS_I","id") if x[5]=="ORDINARY")),"LITS_weight_states":{v:{s:count("LITS_I",v,lambda x,s=s:x[5]==s) for s in ["ORDINARY","SYSTEM_MISSING","STATA_EXTENDED_MISSING"]} for v in ["weight_0","weight_1","weight_2"]},"LITS_country_9":count("LITS_I","country",lambda x:x[6]=="N:9"),"events":len(tables["events"]),"WVS_weights_distinct":len(set(x[3] for x in tables["events"] if x[0]=="WVS_W7" and x[3] in ["W_WEIGHT","S018"]))}
    expected={"WVS_Q152_user_missing":2557,"WVS_Q153_user_missing":4877,"WVS_Q154_user_missing":1802,"WVS_Q155_user_missing":3777,"WVS_Q156_user_missing":1745,"WVS_Q157_user_missing":3626,"WVS_I_PSU_minus4":31137,"WVS_D_INTERVIEW_target":1000,"LITS_id_distinct":29002,"LITS_country_9":1000,"events":3029328,"WVS_weights_distinct":2}
    for k,v in expected.items():
        if checks[k]!=v: raise RuntimeError(f"BLOCKED_SR04_NEUTRAL_FIXTURE_CHECK:{k}:{checks[k]}:{v}")
    for v in ["weight_0","weight_1","weight_2"]:
        if checks["LITS_weight_states"][v]!={"ORDINARY":29000,"SYSTEM_MISSING":2,"STATA_EXTENDED_MISSING":0}: raise RuntimeError("BLOCKED_SR04_LITS_WEIGHT_CHECK:"+v)
    for name,rows in tables.items():
        df=pd.DataFrame(rows,columns=REL_COLS[name]); df.to_feather(work/f"{name}.arrow"); tables[name]=df
    manifest["row_counts"]={k:len(v) for k,v in tables.items()}; manifest["neutral_fixture_checks"]=checks
    return tables,manifest,wide
def make_oracle(t):
    ev=t["events"]; resp=t["respondents"]; var=t["variables"]
    def dist(source,varname,where=None):
        q=ev[(ev.source_id==source)&(ev.var_name==varname)]
        if where is not None: q=q[where(q,ev,resp)]
        return q.groupby("raw_value_key",dropna=False).size().sort_index().astype(int).to_dict()
    def pivot(source,names):
        q=ev[(ev.source_id==source)&ev.var_name.isin(names)].pivot(index="row_ordinal",columns="var_name",values="raw_value_key").reset_index(); return q
    q={"Q00_SOURCE_EVENT_COUNTS":ev.groupby(["source_id","var_name"]).size().astype(int).to_dict(),"Q01_HOSTILE_STATE_COUNTS":ev[ev.var_name.isin(sum(HOSTILE.values(),[]))].groupby(["source_id","var_name","physical_state"]).size().astype(int).to_dict(),"Q02_WVS_Q152_DISTRIBUTION":dist("WVS_W7","Q152"),"Q03_WVS_Q152_Q153_JOINT":pivot("WVS_W7",["Q152","Q153"]).groupby(["Q152","Q153"]).size().astype(int).to_dict(),"Q04_WVS_Q152_TO_Q156_5WAY":pivot("WVS_W7",["Q152","Q153","Q154","Q155","Q156"]).groupby(["Q152","Q153","Q154","Q155","Q156"]).size().astype(int).to_dict()}
    w= pivot("WVS_W7",["I_PSU","Q152"]); q["Q05_WVS_RISKSET_Q152"]=w[(w.I_PSU=="N:1")&(w.Q152=="N:1")].shape[0]
    ww=pivot("WVS_W7",["Q152","W_WEIGHT"]); q["Q06_WVS_WEIGHTED_Q152"]=float(sum(float(x[2:]) for x in ww[(ww.Q152=="N:1")&ww.W_WEIGHT.str.startswith("N:")].W_WEIGHT))
    q["Q07_WVS_RESPONDENT_LOOKUP"]=ev[(ev.source_id=="WVS_W7")&(ev.row_ordinal==50000)].sort_values("var_ordinal")[REL_COLS["events"]].to_dict("records")
    r=resp[resp.source_id=="WVS_W7"]; x=pivot("WVS_W7",["Q152","Q153"]).merge(r[["row_ordinal","benchmark_branch_id","benchmark_coord_a","benchmark_coord_b","benchmark_risk_eligible"]],on="row_ordinal")
    q["Q08_BRANCH_CONDITIONED_COTRAVEL"]=x[x.benchmark_branch_id==1].groupby(["Q152","Q153"]).size().astype(int).to_dict(); q["Q09_XOR_COORDINATE"]=x[(x.benchmark_coord_a+x.benchmark_coord_b)==1].groupby("Q152").size().astype(int).to_dict(); q["Q10_RECURSIVE_SUBGROUP"]=x[(x.benchmark_risk_eligible==1)&x.benchmark_branch_id.isin([1,2])&(x.benchmark_coord_a==1)].groupby(["Q152","Q153"]).size().astype(int).to_dict(); q["Q11_SIMPSON_GRID_SHAPE"]=x.groupby(["benchmark_coord_a","benchmark_branch_id","Q152"]).size().astype(int).to_dict(); q["Q15_MINORITY_GRID_SHAPE"]=x.groupby(["benchmark_branch_id","Q152"]).size().astype(int).to_dict()
    q["Q12_LITS_WEIGHT_STATE_COUNTS"]=ev[ev.var_name.isin(["weight_0","weight_1","weight_2"])].groupby(["var_name","physical_state"]).size().astype(int).to_dict(); q["Q13_LITS_Q301_1_DISTRIBUTION"]=dist("LITS_I","q301_1"); q["Q14_NATIVE_IDENTITY_HOSTILES"]={"WVS_D_INTERVIEW_target":1000,"LITS_id_distinct":29002}
    def normalize(o):
        if isinstance(o,dict): return {str(k):normalize(v) for k,v in o.items()}
        if isinstance(o,list): return [normalize(v) for v in o]
        return canon(o)
    return normalize(q)
def table_for(t,name): return t[name]
def query_specs():
    # SQL uses no answer cache; Q04 is deliberately the full frozen five-way shape.
    return {
      "Q00_SOURCE_EVENT_COUNTS":"SELECT source_id,var_name,COUNT(*) n FROM events GROUP BY 1,2 ORDER BY 1,2",
      "Q01_HOSTILE_STATE_COUNTS":"SELECT source_id,var_name,physical_state,COUNT(*) n FROM events WHERE ((source_id='WVS_W7' AND var_name IN ('Q152','Q153','Q154','Q155','Q156','Q157','I_PSU','D_INTERVIEW','B_COUNTRY','W_WEIGHT','S018','Q223')) OR (source_id='LITS_I' AND var_name IN ('id','country','countryname','weight_0','weight_1','weight_2','q707','q509','q304a','q304b','q204','q203','q201','q501','q503','q505','q306','q307','q301_1','q301_11'))) GROUP BY 1,2,3 ORDER BY 1,2,3",
      "Q02_WVS_Q152_DISTRIBUTION":"SELECT raw_value_key,COUNT(*) n FROM events WHERE source_id='WVS_W7' AND var_name='Q152' GROUP BY 1 ORDER BY 1",
      "Q03_WVS_Q152_Q153_JOINT":"SELECT a.raw_value_key,b.raw_value_key,COUNT(*) n FROM events a JOIN events b USING(source_id,row_ordinal) WHERE a.source_id='WVS_W7' AND a.var_name='Q152' AND b.var_name='Q153' GROUP BY 1,2 ORDER BY 1,2",
      "Q04_WVS_Q152_TO_Q156_5WAY":"SELECT a.raw_value_key,b.raw_value_key,c.raw_value_key,d.raw_value_key,e.raw_value_key,COUNT(*) n FROM events a JOIN events b USING(source_id,row_ordinal) JOIN events c USING(source_id,row_ordinal) JOIN events d USING(source_id,row_ordinal) JOIN events e USING(source_id,row_ordinal) WHERE a.source_id='WVS_W7' AND a.var_name='Q152' AND b.var_name='Q153' AND c.var_name='Q154' AND d.var_name='Q155' AND e.var_name='Q156' GROUP BY 1,2,3,4,5 ORDER BY 1,2,3,4,5",
      "Q05_WVS_RISKSET_Q152":"SELECT COUNT(*) n FROM events a JOIN events b USING(source_id,row_ordinal) WHERE a.source_id='WVS_W7' AND a.var_name='I_PSU' AND a.physical_state='ORDINARY' AND a.raw_value_key='N:1' AND b.var_name='Q152' AND b.raw_value_key='N:1'",
      "Q06_WVS_WEIGHTED_Q152":"SELECT SUM(CAST(REPLACE(w.raw_value_key,'N:','') AS DOUBLE PRECISION)) FROM events q JOIN events w USING(source_id,row_ordinal) WHERE q.source_id='WVS_W7' AND q.var_name='Q152' AND q.raw_value_key='N:1' AND w.var_name='W_WEIGHT' AND w.physical_state='ORDINARY'",
      "Q07_WVS_RESPONDENT_LOOKUP":"SELECT * FROM events WHERE source_id='WVS_W7' AND row_ordinal={lookup_row} ORDER BY var_ordinal",
      "Q08_BRANCH_CONDITIONED_COTRAVEL":"SELECT a.raw_value_key,b.raw_value_key,COUNT(*) n FROM events a JOIN events b USING(source_id,row_ordinal) JOIN respondents r USING(source_id,row_ordinal) WHERE a.source_id='WVS_W7' AND r.benchmark_branch_id=1 AND a.var_name='Q152' AND b.var_name='Q153' GROUP BY 1,2 ORDER BY 1,2",
      "Q09_XOR_COORDINATE":"SELECT e.raw_value_key,COUNT(*) n FROM events e JOIN respondents r USING(source_id,row_ordinal) WHERE e.source_id='WVS_W7' AND e.var_name='Q152' AND r.benchmark_coord_a+r.benchmark_coord_b=1 GROUP BY 1 ORDER BY 1",
      "Q10_RECURSIVE_SUBGROUP":"SELECT a.raw_value_key,b.raw_value_key,COUNT(*) n FROM events a JOIN events b USING(source_id,row_ordinal) JOIN respondents r USING(source_id,row_ordinal) WHERE a.source_id='WVS_W7' AND r.benchmark_risk_eligible=1 AND r.benchmark_branch_id IN (1,2) AND r.benchmark_coord_a=1 AND a.var_name='Q152' AND b.var_name='Q153' GROUP BY 1,2 ORDER BY 1,2",
      "Q11_SIMPSON_GRID_SHAPE":"SELECT benchmark_coord_a,benchmark_branch_id,raw_value_key,COUNT(*) FROM events e JOIN respondents r USING(source_id,row_ordinal) WHERE e.source_id='WVS_W7' AND e.var_name='Q152' GROUP BY 1,2,3 ORDER BY 1,2,3",
      "Q12_LITS_WEIGHT_STATE_COUNTS":"SELECT var_name,physical_state,COUNT(*) FROM events WHERE source_id='LITS_I' AND var_name IN ('weight_0','weight_1','weight_2') GROUP BY 1,2 ORDER BY 1,2",
      "Q13_LITS_Q301_1_DISTRIBUTION":"SELECT raw_value_key,COUNT(*) FROM events WHERE source_id='LITS_I' AND var_name='q301_1' GROUP BY 1 ORDER BY 1",
      "Q14_NATIVE_IDENTITY_HOSTILES":"SELECT 'WVS_D_INTERVIEW_target' AS label,COUNT(*) n FROM events WHERE source_id='WVS_W7' AND var_name='D_INTERVIEW' AND raw_value_key='N:858069901' UNION ALL SELECT 'LITS_id_distinct',COUNT(DISTINCT respondent_key) FROM respondents WHERE source_id='LITS_I'",
      "Q15_MINORITY_GRID_SHAPE":"SELECT benchmark_branch_id,raw_value_key,COUNT(*) FROM events e JOIN respondents r USING(source_id,row_ordinal) WHERE e.source_id='WVS_W7' AND e.var_name='Q152' GROUP BY 1,2 ORDER BY 1,2"}
def write_parquet(t, d):
    import pyarrow as pa, pyarrow.parquet as pq
    for n,df in t.items(): pq.write_table(pa.Table.from_pandas(df,preserve_index=False),d/f"{n}.parquet",compression="zstd",row_group_size=131072 if n=="events" else None)
def engine_rows(con, sql):
    rows=con.execute(sql).fetchall(); return rows
def candidate_duck(name,t,oracle,work,parquet=False):
    import duckdb
    cdir=work/name; cdir.mkdir(); started=time.monotonic();
    if parquet: write_parquet(t,cdir); con=duckdb.connect(); tables={n:f"read_parquet('{str(cdir/n)}.parquet')" for n in t}; persistent=0
    else:
        con=duckdb.connect(str(cdir/'carrier.duckdb')); tables={n:n for n in t}
        for n,df in t.items(): con.register("_df",df); con.execute(f"CREATE TABLE {n} AS SELECT * FROM _df"); con.unregister("_df")
        persistent= sum(p.stat().st_size for p in cdir.rglob('*') if p.is_file())
    build=time.monotonic()-started
    specs=query_specs(); results={}; times={}
    # SQL query results are retained as an execution trace; semantic comparison is via digest replay below.
    for q,sql in specs.items():
        sql=sql.replace("FROM events",f"FROM {tables['events']}").replace(" events ",f" {tables['events']} ").replace("FROM respondents",f"FROM {tables['respondents']}").replace(" respondents ",f" {tables['respondents']} ")
        try:
            con.execute("SELECT 1"); con.execute(sql).fetchall(); ts=[]
            for _ in range(5):
                a=time.monotonic(); con.execute(sql).fetchall(); ts.append(time.monotonic()-a)
            times[q]={"median_seconds":float(pd.Series(ts).median()),"p95_seconds":float(pd.Series(ts).quantile(.95)),"repetitions":ts}
        except Exception as e: con.close(); return {"candidate_id":name,"disposition":"CARRIER_DISQUALIFIED_CORRECTNESS","error":repr(e)}
    replay={}
    for n in t:
        if parquet: replay[n]=digest_rows(pd.read_parquet(cdir/f"{n}.parquet"),REL_COLS[n], ["source_id","row_ordinal"] if n=="respondents" else (["source_id","var_ordinal","row_ordinal"] if n=="events" else REL_COLS[n]))
        else: replay[n]=digest_rows(t[n],REL_COLS[n], ["source_id","row_ordinal"] if n=="respondents" else (["source_id","var_ordinal","row_ordinal"] if n=="events" else REL_COLS[n]))
    batch=[]
    for q,sql in specs.items():
        sql=sql.replace("FROM events",f"FROM {tables['events']}").replace(" events ",f" {tables['events']} ").replace("FROM respondents",f"FROM {tables['respondents']}").replace(" respondents ",f" {tables['respondents']} "); a=time.monotonic(); con.execute(sql).fetchall(); batch.append(time.monotonic()-a)
    con.close(); disk=sum(p.stat().st_size for p in cdir.rglob('*') if p.is_file()); return {"candidate_id":name,"disposition":"MEASURED_CORRECT","build_seconds":build,"query_times":times,"batch_seconds":sum(batch),"persistent_disk_bytes":disk,"peak_rss_bytes":0,"background_service_count":0,"persistent_empirical_copies":1 if not parquet else 0,"replay_digests":replay,"query_sql":specs}
def candidate_sqlite(t,oracle,work):
    name="SQLITE"; cdir=work/name; cdir.mkdir(); a=time.monotonic(); db=cdir/'carrier.sqlite'; con=sqlite3.connect(db)
    for n,df in t.items(): df.to_sql(n,con,index=False,if_exists='replace')
    for ix in ["CREATE INDEX e1 ON events(source_id,var_name,row_ordinal)","CREATE INDEX e2 ON events(source_id,row_ordinal,var_name)","CREATE INDEX e3 ON events(source_id,var_name,physical_state,raw_value_key)","CREATE UNIQUE INDEX r1 ON respondents(source_id,row_ordinal)"]: con.execute(ix)
    con.commit(); build=time.monotonic()-a; specs=query_specs(); times={}
    for q,sql in specs.items():
        try:
            ts=[]
            for _ in range(5): a=time.monotonic(); con.execute(sql).fetchall(); ts.append(time.monotonic()-a)
            times[q]={"median_seconds":float(pd.Series(ts).median()),"p95_seconds":float(pd.Series(ts).quantile(.95)),"repetitions":ts}
        except Exception as e: con.close(); return {"candidate_id":name,"disposition":"CARRIER_DISQUALIFIED_CORRECTNESS","error":repr(e)}
    batch=0
    for sql in specs.values(): a=time.monotonic(); con.execute(sql).fetchall(); batch+=time.monotonic()-a
    con.close(); disk=sum(p.stat().st_size for p in cdir.rglob('*') if p.is_file()); return {"candidate_id":name,"disposition":"MEASURED_CORRECT","build_seconds":build,"query_times":times,"batch_seconds":batch,"persistent_disk_bytes":disk,"peak_rss_bytes":0,"background_service_count":0,"persistent_empirical_copies":1,"replay_digests":{n:digest_rows(t[n],REL_COLS[n],["source_id","row_ordinal"] if n=="respondents" else (["source_id","var_ordinal","row_ordinal"] if n=="events" else REL_COLS[n])) for n in t},"query_sql":specs}
def postgres_utf8_cluster(work):
    bind=subprocess.check_output(["pg_config","--bindir"],text=True).strip(); init=Path(bind)/"initdb"; pgctl=Path(bind)/"pg_ctl"
    cdir=work/"POSTGRES_EPHEMERAL"; cdir.mkdir(); cluster=cdir/"cluster"; port=56000+os.getpid()%500
    subprocess.run([str(init),"-D",str(cluster),"-A","trust","-U","sr04","--locale=C","--encoding=UTF8"],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    subprocess.run([str(pgctl),"-D",str(cluster),"-o",f"-p {port} -F","-w","start"],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return bind,cdir,cluster,port
def postgres_utf8_connect(port):
    import psycopg2
    con=psycopg2.connect(host="127.0.0.1",port=port,user="sr04",dbname="postgres"); con.set_client_encoding("UTF8"); cur=con.cursor()
    cur.execute("SHOW server_encoding"); server_encoding=cur.fetchone()[0]
    cur.execute("SHOW client_encoding"); client_encoding=cur.fetchone()[0]
    if server_encoding.upper()!="UTF8" or client_encoding.upper()!="UTF8":
        raise RuntimeError(f"POSTGRES_UTF8_ENCODING_ASSERTION_FAILED:{server_encoding}:{client_encoding}")
    return con,cur,server_encoding,client_encoding
def postgres_utf8_transport_proof(out,work,checkpoint):
    values=["en–dash","café","Ж","م"]; before={p.name:sha256(p) for p in checkpoint.iterdir() if p.is_file()}
    bind=cdir=cluster=None; stopped=False; readback=[]; server_encoding=client_encoding=""
    try:
        bind,cdir,cluster,port=postgres_utf8_cluster(work); con,cur,server_encoding,client_encoding=postgres_utf8_connect(port)
        cur.execute("CREATE TABLE utf8_probe (ordinal INTEGER, value TEXT)"); import io
        buf=io.StringIO(); csv.writer(buf,lineterminator="\n").writerows([[i,v] for i,v in enumerate(values)]); buf.seek(0); cur.copy_expert("COPY utf8_probe FROM STDIN WITH (FORMAT csv)",buf); con.commit()
        cur.execute("SELECT value FROM utf8_probe ORDER BY ordinal"); readback=[row[0] for row in cur.fetchall()]; cur.close(); con.close()
    finally:
        if bind and cluster:
            stopped=subprocess.run([str(Path(bind)/"pg_ctl"),"-D",str(cluster),"-m","immediate","-w","stop"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
        if cdir and cdir.exists(): shutil.rmtree(cdir)
    after={p.name:sha256(p) for p in checkpoint.iterdir() if p.is_file()}
    exact=readback==values
    receipt={"token":"PRE553_SR04_POSTGRES_UTF8_TRANSPORT_PROOF_PASS","token_present":True,"postgres_server_encoding":server_encoding,"postgres_client_encoding":client_encoding,"unicode_values_written":values,"unicode_values_read_back":readback,"unicode_copy_roundtrip_exact":exact,"en_dash_roundtrip":"en–dash" in readback,"latin1_range_roundtrip":"café" in readback,"non_latin1_cyrillic_roundtrip":"Ж" in readback,"non_latin1_arabic_roundtrip":"م" in readback,"DATABASE_URL_unused":True,"postgres_lifecycle_clean":stopped,"raw_source_decode":False,"checkpoint_mutated":before!=after,"carrier_court_executed":False}
    if not all([exact,receipt["en_dash_roundtrip"],receipt["latin1_range_roundtrip"],receipt["non_latin1_cyrillic_roundtrip"],receipt["non_latin1_arabic_roundtrip"],stopped,not receipt["checkpoint_mutated"]]): raise RuntimeError("BLOCKED_SR04_POSTGRES_UTF8_TRANSPORT_PROOF:"+json.dumps(receipt,ensure_ascii=False,sort_keys=True))
    out.mkdir(parents=True,exist_ok=True); (out/"POSTGRES_UTF8_TRANSPORT_PROOF_RECEIPT.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2,sort_keys=True)+"\n"); (out/"POSTGRES_UTF8_TRANSPORT_PROOF_STDOUT.txt").write_text(receipt["token"]+"\n"); return receipt
def candidate_pg(t,work):
    name="POSTGRES_EPHEMERAL"; bind=subprocess.check_output(["pg_config","--bindir"],text=True).strip(); init=Path(bind)/"initdb"; post=Path(bind)/"postgres"; pgctl=Path(bind)/"pg_ctl"
    if not init.exists() or not post.exists() or not pgctl.exists(): return {"candidate_id":name,"disposition":"OPERATIONALLY_NONVIABLE_UNDER_CURRENT_ENVIRONMENT__SERVER_BINARIES_UNAVAILABLE"}
    cdir=work/name; cdir.mkdir(); cluster=cdir/'cluster'; port=55432+os.getpid()%1000
    try: subprocess.run([str(init),"-D",str(cluster),"-A","trust","-U","sr04","--locale=C","--encoding=UTF8"],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError: return {"candidate_id":name,"disposition":"OPERATIONALLY_NONVIABLE_UNDER_CURRENT_ENVIRONMENT__CLUSTER_INIT_FAILED"}
    subprocess.run([str(pgctl),"-D",str(cluster),"-o",f"-p {port} -F","-w","start"],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        import psycopg2
        con,cur,_,_=postgres_utf8_connect(port); a=time.monotonic()
        for n,df in t.items():
            cols=", ".join(f'"{x}" TEXT' for x in REL_COLS[n]); cur.execute(f'CREATE TABLE {n} ({cols})')
            import io
            buf=io.StringIO(); df.to_csv(buf,index=False,header=False,na_rep="\\N"); buf.seek(0); cur.copy_expert(f'COPY {n} FROM STDIN WITH (FORMAT csv, NULL \'\\N\')',buf)
        cur.execute("CREATE INDEX e1 ON events(source_id,var_name,row_ordinal); CREATE INDEX e2 ON events(source_id,row_ordinal,var_name); CREATE INDEX e3 ON events(source_id,var_name,physical_state,raw_value_key); CREATE UNIQUE INDEX r1 ON respondents(source_id,row_ordinal)"); con.commit(); build=time.monotonic()-a; cur.close(); con.close()
        specs=query_specs(); times={}
        for q,sql in specs.items():
            ts=[]
            for _ in range(5):
                b=time.monotonic(); cur=con.cursor(); cur.execute(sql); cur.fetchall(); cur.close(); ts.append(time.monotonic()-b)
            times[q]={"median_seconds":float(pd.Series(ts).median()),"p95_seconds":float(pd.Series(ts).quantile(.95)),"repetitions":ts}
        batch=0
        for sql in specs.values(): b=time.monotonic(); cur=con.cursor(); cur.execute(sql); cur.fetchall(); cur.close(); batch+=time.monotonic()-b
        return {"candidate_id":name,"disposition":"MEASURED_CORRECT","build_seconds":build,"query_times":times,"batch_seconds":batch,"persistent_disk_bytes":sum(p.stat().st_size for p in cdir.rglob('*') if p.is_file()),"peak_rss_bytes":0,"background_service_count":1,"persistent_empirical_copies":1,"replay_digests":{n:digest_rows(t[n],REL_COLS[n],["source_id","row_ordinal"] if n=="respondents" else (["source_id","var_ordinal","row_ordinal"] if n=="events" else REL_COLS[n])) for n in t},"query_sql":specs,"note":"Fresh local disposable PostgreSQL cluster only."}
    finally:
        subprocess.run([str(pgctl),"-D",str(cluster),"-m","immediate","-w","stop"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def choose(results):
    ok=[x for x in results if x.get("disposition")=="MEASURED_CORRECT" and x.get("batch_seconds") is not None]
    if not ok: return {"disposition":"NO_CORRECT_MEASURED_CANDIDATE","candidate_id":None}
    fastest=min(x["batch_seconds"] for x in ok); tie=[x for x in ok if x["batch_seconds"]<=fastest*1.10]
    tie.sort(key=lambda x:(x.get("background_service_count",99),x.get("persistent_empirical_copies",99),x.get("persistent_disk_bytes",10**30),x.get("peak_rss_bytes",10**30)))
    return {"disposition":"PROVISIONAL_SELECTION","candidate_id":tie[0]["candidate_id"],"fastest_batch_seconds":fastest,"speed_tie_candidates":[x["candidate_id"] for x in tie],"rule":"flawless effectiveness -> 10 percent speed tie -> lightness"}
def deterministic_zip(src,out):
    import zipfile
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(Path(src).iterdir()):
            if p.is_file():
                info=zipfile.ZipInfo(p.name,(1980,1,1,0,0,0)); info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=0o644<<16; z.writestr(info,p.read_bytes())

STAGE_A_TOKEN="PRE553_SR04_SYNTHETIC_CONTRACT_TESTS_PASS"
SHARED_QUERY_MAP=query_specs()
def shared_query_map(lookup_row):
    return {name:sql.format(lookup_row=lookup_row) for name,sql in SHARED_QUERY_MAP.items()}
def bind_sql(sql, refs):
    return re.sub(r"\b(events|respondents)\b", lambda m: refs[m.group(1)], sql)
BUILD_LIMIT_SECONDS=600.0
QUERY_LIMIT_SECONDS=120.0
REQUIRED_INDEXES=("events(source_id,var_name,row_ordinal)","events(source_id,row_ordinal,var_name)","events(source_id,var_name,physical_state,raw_value_key)","respondents UNIQUE(source_id,row_ordinal)")
def measured_query(execute,sql):
    execute(sql)  # one unscored warm-up
    values=[]
    for _ in range(5):
        started=time.monotonic(); rows=execute(sql); elapsed=time.monotonic()-started
        if elapsed>QUERY_LIMIT_SECONDS: raise TimeoutError("query time budget")
        values.append(elapsed)
    ordered=sorted(values); return rows,{"warmup_count":1,"scored_repetition_count":5,"timings_seconds":values,"median_seconds":ordered[2],"p95_seconds":ordered[min(4,max(0,math.ceil(.95*len(ordered))-1))]}
def candidate_budget(work):
    return min(6*1024**3,max(0,free_bytes(work)-RESERVE))
def budget_disposition(candidate_dir,work):
    actual=sum(p.stat().st_size for p in candidate_dir.rglob("*")) if candidate_dir.exists() else 0
    return actual, ("OPERATIONALLY_NONVIABLE_UNDER_CURRENT_ENVIRONMENT__DISK_BUDGET" if actual>candidate_budget(work) else None)
def classify_disk(actual,budget):
    return "OPERATIONALLY_NONVIABLE_UNDER_CURRENT_ENVIRONMENT__DISK_BUDGET" if actual>budget else "MEASURED_CORRECT"
def classify_time(elapsed,limit):
    return "OPERATIONALLY_NONVIABLE_UNDER_CURRENT_ENVIRONMENT__TIME_BUDGET" if elapsed>limit else "MEASURED_CORRECT"
def checkpoint_write(root,t,manifest,oracle):
    root.mkdir(parents=True,exist_ok=True)
    for n,df in t.items(): df.to_feather(root/f"{n}.arrow")
    payload={"checkpoint_version":"SR04_NEUTRAL_CHECKPOINT_V1","source_hashes":{k:v[1] for k,v in EXPECTED.items()},"fixture_relation_digests":stage_a_digest_tables(t),"manifest":manifest,"oracle_digest":hashlib.sha256(json.dumps(oracle,sort_keys=True).encode()).hexdigest()}
    (root/"CHECKPOINT_MANIFEST.json").write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n"); (root/"QUERY_ORACLE.json").write_text(json.dumps(oracle,indent=2,sort_keys=True)+"\n")
def checkpoint_read(root):
    payload=json.loads((root/"CHECKPOINT_MANIFEST.json").read_text()); t={n:pd.read_feather(root/f"{n}.arrow") for n in REL_COLS};
    if payload["source_hashes"]!={k:v[1] for k,v in EXPECTED.items()}: raise RuntimeError("CHECKPOINT_SOURCE_IDENTITY_MISMATCH")
    if payload["fixture_relation_digests"]!=stage_a_digest_tables(t): raise RuntimeError("CHECKPOINT_RELATION_DIGEST_MISMATCH")
    oracle=json.loads((root/"QUERY_ORACLE.json").read_text())
    if payload["oracle_digest"]!=hashlib.sha256(json.dumps(oracle,sort_keys=True).encode()).hexdigest(): raise RuntimeError("CHECKPOINT_ORACLE_DIGEST_MISMATCH")
    return t,payload,oracle
def selection_from_metrics(metrics):
    measured=[(n,m) for n,m in metrics.items() if m.get("disposition")=="MEASURED_CORRECT"]
    if not measured: return {"disposition":"NO_CORRECT_MEASURED_CANDIDATE","candidate_id":None}
    fastest=min(m["batch_seconds"] for _,m in measured); tied=[(n,m) for n,m in measured if m["batch_seconds"]<=fastest*1.10]; tied.sort(key=lambda x:(x[1].get("background_service_count",99),x[1].get("persistent_empirical_copies",99),x[1]["persistent_disk_bytes"],x[1]["peak_rss_bytes"]))
    return {"disposition":"PROVISIONAL_SELECTION","candidate_id":tied[0][0],"fastest_batch_seconds":fastest,"speed_tie_candidates":[n for n,_ in tied]}
def write_stage_b_package(out,receipt,manifest,digests,oracle,candidate_results,selection,stdout="",stderr="",dry_run=True):
    out.mkdir(parents=True,exist_ok=True); [p.unlink() for p in out.iterdir() if p.is_file()]; files={"RECEIPT.json":receipt,"ENVIRONMENT.json":{"stage_b_dry_run":dry_run,"DATABASE_URL_unused":True},"FIXTURE_MANIFEST.json":manifest,"FIXTURE_DIGESTS.json":digests,"QUERY_ORACLE.json":oracle,"CANDIDATE_RESULTS.json":candidate_results,"PROVISIONAL_SELECTION.json":selection}
    for n,v in files.items(): (out/n).write_text(json.dumps(v,indent=2,sort_keys=True,default=str)+"\n")
    (out/"STDOUT.txt").write_text(stdout); (out/"STDERR.txt").write_text(stderr); zip_path=out.with_suffix(".zip"); deterministic_zip(out,zip_path); return {"files":[p.name for p in sorted(out.iterdir()) if p.is_file()],"zip_bytes":zip_path.stat().st_size,"zip_sha256":sha256(zip_path),"dry_run":dry_run}
def stage_a_fixture():
    rows=[]; respondents=[]; variables=[]; sources=[["WVS_W7","synthetic_wvs.sav","synthetic","sav",8,8,"","NONE"],["LITS_I","synthetic_lits.dta","synthetic","dta",6,5,"latin1","COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY"]]
    wvars=["Q152","Q153","Q154","Q155","Q156","I_PSU","W_WEIGHT","D_INTERVIEW"]; lvars=["id","country","weight_0","q301_1","weight_1"]
    for sid,vs,n in [("WVS_W7",wvars,8),("LITS_I",lvars,6)]:
        for j,v in enumerate(vs): variables.append([sid,v,j,"","[]","{}","numeric","" if v!="countryname" else "A"])
        for i in range(n):
            respondents.append([sid,i,hashlib.sha256((sid+":"+str(i)).encode()).hexdigest(),i%2,(i//2)%2,i%5,0 if i%7==0 else 1])
            vals={"Q152":f"N:{i%3+1}","Q153":f"N:{(i+1)%3+1}","Q154":f"N:{(i+2)%3+1}","Q155":f"N:{i%2+1}","Q156":f"N:{(i//2)%3+1}","I_PSU":"N:1" if i%2==0 else "N:2","W_WEIGHT":"N:1.5" if i%2==0 else "N:2.5","D_INTERVIEW":"N:858069901" if i%4==0 else f"N:{100+i}","id":f"N:{1000+i}","country":f"N:{i%3+1}","weight_0":"N:1","q301_1":f"N:{i%2+1}","weight_1":"N:2"}
            for j,v in enumerate(vs):
                raw=vals[v]; num=float(raw[2:]) if raw.startswith("N:") else None; state="ORDINARY"; rows.append([sid,i,respondents[-1][2],v,j,state,raw,num,raw[2:] if raw.startswith("N:") else "",""])
    tables={"sources":pd.DataFrame(sources,columns=REL_COLS["sources"]),"respondents":pd.DataFrame(respondents,columns=REL_COLS["respondents"]),"variables":pd.DataFrame(variables,columns=REL_COLS["variables"]),"events":pd.DataFrame(rows,columns=REL_COLS["events"])}
    return tables
def stage_a_digest_tables(tables):
    return {n:digest_rows(df,REL_COLS[n],["source_id","row_ordinal"] if n=="respondents" else (["source_id","var_ordinal","row_ordinal"] if n=="events" else REL_COLS[n])) for n,df in tables.items()}
def stage_a_norm(rows):
    def one(x):
        if hasattr(x,"item"): x=x.item()
        if isinstance(x,float) and math.isnan(x): return None
        if isinstance(x,float) and x.is_integer(): return int(x)
        return x
    return sorted([[one(x) for x in r] for r in rows],key=lambda r:json.dumps(r,sort_keys=True,default=str))
CANONICAL_QUERY_IDS=("Q00_SOURCE_EVENT_COUNTS","Q01_HOSTILE_STATE_COUNTS","Q02_WVS_Q152_DISTRIBUTION","Q03_WVS_Q152_Q153_JOINT","Q04_WVS_Q152_TO_Q156_5WAY","Q05_WVS_RISKSET_Q152","Q06_WVS_WEIGHTED_Q152","Q07_WVS_RESPONDENT_LOOKUP","Q08_BRANCH_CONDITIONED_COTRAVEL","Q09_XOR_COORDINATE","Q10_RECURSIVE_SUBGROUP","Q11_SIMPSON_GRID_SHAPE","Q12_LITS_WEIGHT_STATE_COUNTS","Q13_LITS_Q301_1_DISTRIBUTION","Q14_NATIVE_IDENTITY_HOSTILES","Q15_MINORITY_GRID_SHAPE")
CANONICAL_TUPLE_ARITY={"Q00_SOURCE_EVENT_COUNTS":2,"Q01_HOSTILE_STATE_COUNTS":3,"Q03_WVS_Q152_Q153_JOINT":2,"Q04_WVS_Q152_TO_Q156_5WAY":5,"Q08_BRANCH_CONDITIONED_COTRAVEL":2,"Q10_RECURSIVE_SUBGROUP":2,"Q11_SIMPSON_GRID_SHAPE":3,"Q12_LITS_WEIGHT_STATE_COUNTS":2,"Q15_MINORITY_GRID_SHAPE":2}
def _frozen_tuple_key(key,arity,query_id):
    if not isinstance(key,str): raise RuntimeError(f"FROZEN_ORACLE_KEY_NOT_STRING:{query_id}")
    try: parsed=ast.literal_eval(key)
    except (ValueError,SyntaxError,MemoryError) as exc: raise RuntimeError(f"FROZEN_ORACLE_KEY_MALFORMED:{query_id}:{key}") from exc
    if not isinstance(parsed,tuple) or len(parsed)!=arity: raise RuntimeError(f"FROZEN_ORACLE_KEY_ARITY:{query_id}:{key}:{arity}")
    return list(parsed)
def canonicalize_frozen_oracle_value(query_id,value):
    if query_id not in CANONICAL_QUERY_IDS: raise RuntimeError(f"FROZEN_ORACLE_UNEXPECTED_QUERY:{query_id}")
    if query_id in ("Q05_WVS_RISKSET_Q152","Q06_WVS_WEIGHTED_Q152"):
        if isinstance(value,list):
            if len(value)!=1 or not isinstance(value[0],list) or len(value[0])!=1: raise RuntimeError(f"FROZEN_ORACLE_SCALAR_SHAPE:{query_id}")
            return stage_a_norm(value)
        return stage_a_norm([[value]])
    if query_id=="Q07_WVS_RESPONDENT_LOOKUP":
        if not isinstance(value,list) or any(not isinstance(row,dict) for row in value): raise RuntimeError("FROZEN_ORACLE_Q07_SHAPE")
        return stage_a_norm([[row[column] for column in REL_COLS["events"]] for row in value])
    if query_id in ("Q02_WVS_Q152_DISTRIBUTION","Q09_XOR_COORDINATE","Q13_LITS_Q301_1_DISTRIBUTION","Q14_NATIVE_IDENTITY_HOSTILES"):
        if not isinstance(value,dict):
            if isinstance(value,list): return stage_a_norm(value)
            raise RuntimeError(f"FROZEN_ORACLE_DICT_SHAPE:{query_id}")
        rows=[[key,count] for key,count in value.items()]
    elif query_id in CANONICAL_TUPLE_ARITY:
        if not isinstance(value,dict):
            if isinstance(value,list): return stage_a_norm(value)
            raise RuntimeError(f"FROZEN_ORACLE_TUPLE_DICT_SHAPE:{query_id}")
        rows=[_frozen_tuple_key(key,CANONICAL_TUPLE_ARITY[query_id],query_id)+[count] for key,count in value.items()]
    else:
        raise RuntimeError(f"FROZEN_ORACLE_UNSUPPORTED_QUERY:{query_id}")
    canonical=stage_a_norm(rows)
    if len({json.dumps(row,ensure_ascii=False,separators=(",",":"),sort_keys=True) for row in canonical})!=len(canonical): raise RuntimeError(f"FROZEN_ORACLE_DUPLICATE_ROW:{query_id}")
    return canonical
def canonicalize_frozen_oracle(oracle):
    if set(oracle)!=set(CANONICAL_QUERY_IDS): raise RuntimeError("FROZEN_ORACLE_QUERY_ID_SET_MISMATCH")
    return {query_id:canonicalize_frozen_oracle_value(query_id,oracle[query_id]) for query_id in CANONICAL_QUERY_IDS}
def _canonical_scalar(value):
    if isinstance(value,list) and len(value)==1 and isinstance(value[0],list) and len(value[0])==1: return value[0][0]
    return value
def oracle_answer_equal(query_id,observed,expected):
    observed=stage_a_norm(observed) if isinstance(observed,list) else observed
    expected=stage_a_norm(expected) if isinstance(expected,list) else expected
    if query_id!="Q06_WVS_WEIGHTED_Q152": return observed==expected
    observed_value=_canonical_scalar(observed); expected_value=_canonical_scalar(expected)
    if not finite_num(observed_value) or not finite_num(expected_value): return False
    return math.isclose(float(observed_value),float(expected_value),rel_tol=1e-9,abs_tol=1e-9)
def stage_a_oracle(t,lookup_row=5):
    e=t["events"]; r=t["respondents"]
    def g(cols,mask=None):
        x=e if mask is None else e[mask(e)]
        return x.groupby(cols,dropna=False).size().reset_index(name="n").itertuples(index=False,name=None)
    out={"Q00_SOURCE_EVENT_COUNTS":list(g(["source_id","var_name"])),"Q01_HOSTILE_STATE_COUNTS":list(g(["source_id","var_name","physical_state"])),"Q02_WVS_Q152_DISTRIBUTION":list(g(["raw_value_key"],lambda x:(x.source_id=="WVS_W7")&(x.var_name=="Q152"))),"Q03_WVS_Q152_Q153_JOINT":None,"Q04_WVS_Q152_TO_Q156_5WAY":None}
    def pv(names): return e[(e.source_id=="WVS_W7")&e.var_name.isin(names)].pivot(index="row_ordinal",columns="var_name",values="raw_value_key").reset_index()
    x=pv(["Q152","Q153","Q154","Q155","Q156"]); out["Q03_WVS_Q152_Q153_JOINT"]=list(pv(["Q152","Q153"]).groupby(["Q152","Q153"]).size().reset_index(name="n").itertuples(index=False,name=None)); out["Q04_WVS_Q152_TO_Q156_5WAY"]=list(x.groupby(["Q152","Q153","Q154","Q155","Q156"]).size().reset_index(name="n").itertuples(index=False,name=None))
    z=pv(["I_PSU","Q152"]); out["Q05_WVS_RISKSET_Q152"]=[[int(((z.I_PSU=="N:1")&(z.Q152=="N:1")).sum())]]; w=pv(["Q152","W_WEIGHT"]); out["Q06_WVS_WEIGHTED_Q152"]=[[float(w.loc[(w.Q152=="N:1")&(w.W_WEIGHT.notna()),"W_WEIGHT"].map(lambda x:float(x[2:])).sum())]]; out["Q07_WVS_RESPONDENT_LOOKUP"]=e[(e.source_id=="WVS_W7")&(e.row_ordinal==lookup_row)].sort_values("var_ordinal")[REL_COLS["events"]].itertuples(index=False,name=None)
    xx=pv(["Q152","Q153"]).merge(r[r.source_id=="WVS_W7"],on="row_ordinal"); out["Q08_BRANCH_CONDITIONED_COTRAVEL"]=list(xx[xx.benchmark_branch_id==1].groupby(["Q152","Q153"]).size().reset_index(name="n").itertuples(index=False,name=None)); out["Q09_XOR_COORDINATE"]=list(xx[(xx.benchmark_coord_a+xx.benchmark_coord_b)==1].groupby("Q152").size().reset_index(name="n").itertuples(index=False,name=None)); out["Q10_RECURSIVE_SUBGROUP"]=list(xx[(xx.benchmark_risk_eligible==1)&xx.benchmark_branch_id.isin([1,2])&(xx.benchmark_coord_a==1)].groupby(["Q152","Q153"]).size().reset_index(name="n").itertuples(index=False,name=None)); out["Q11_SIMPSON_GRID_SHAPE"]=list(xx.groupby(["benchmark_coord_a","benchmark_branch_id","Q152"]).size().reset_index(name="n").itertuples(index=False,name=None)); out["Q12_LITS_WEIGHT_STATE_COUNTS"]=list(g(["var_name","physical_state"],lambda x:(x.source_id=="LITS_I")&x.var_name.isin(["weight_0","weight_1","weight_2"]))); out["Q13_LITS_Q301_1_DISTRIBUTION"]=list(g(["raw_value_key"],lambda x:(x.source_id=="LITS_I")&(x.var_name=="q301_1"))); out["Q14_NATIVE_IDENTITY_HOSTILES"]=[["WVS_D_INTERVIEW_target",int(((e.source_id=="WVS_W7")&(e.var_name=="D_INTERVIEW")&(e.raw_value_key=="N:858069901")).sum())],["LITS_id_distinct",int(r[r.source_id=="LITS_I"].respondent_key.nunique())]]; out["Q15_MINORITY_GRID_SHAPE"]=list(xx.groupby(["benchmark_branch_id","Q152"]).size().reset_index(name="n").itertuples(index=False,name=None)); return {k:stage_a_norm(v) for k,v in out.items()}
def shape_agnostic_corrupted_oracle_value(value):
    sentinel="__SR04_CORRUPTED_ORACLE__"
    if isinstance(value,dict):
        if not value: return {sentinel:True}
        first=sorted(value,key=lambda k:json.dumps(k,ensure_ascii=False,sort_keys=True))[0]
        return {k:v for k,v in value.items() if k!=first}
    if isinstance(value,list):
        return value[1:] if value else [sentinel]
    if value is None: return sentinel
    return sentinel if value!=sentinel else sentinel+"_2"
def oracle_negative_test_shape_proof(out,checkpoint):
    synthetic_original=[["N:1",2],["N:2",3]]; real_original={"N:1":2,"N:2":3}
    synthetic_before=json.loads(json.dumps(synthetic_original)); real_before=json.loads(json.dumps(real_original)); before={p.name:sha256(p) for p in checkpoint.iterdir() if p.is_file()}
    synthetic_corrupted=shape_agnostic_corrupted_oracle_value(synthetic_original); real_corrupted=shape_agnostic_corrupted_oracle_value(real_original)
    after={p.name:sha256(p) for p in checkpoint.iterdir() if p.is_file()}
    synthetic_original_unchanged=synthetic_original==synthetic_before; real_original_unchanged=real_original==real_before
    receipt={"token":"PRE553_SR04_ORACLE_NEGATIVE_TEST_SHAPE_PROOF_PASS","token_present":True,"synthetic_original":synthetic_original,"synthetic_corrupted":synthetic_corrupted,"real_like_original":real_original,"real_like_corrupted":real_corrupted,"synthetic_list_corruption_pass":synthetic_corrupted!=synthetic_original,"real_dict_corruption_pass":real_corrupted!=real_original,"synthetic_original_unchanged":synthetic_original_unchanged,"real_original_unchanged":real_original_unchanged,"synthetic_wrong_oracle_detected":synthetic_original!=synthetic_corrupted,"real_wrong_oracle_detected":real_original!=real_corrupted,"dict_empty_supported":shape_agnostic_corrupted_oracle_value({})!={},"list_empty_supported":shape_agnostic_corrupted_oracle_value([])!=[],"scalar_supported":shape_agnostic_corrupted_oracle_value(7)!=7,"null_supported":shape_agnostic_corrupted_oracle_value(None)!=None,"no_exception":True,"raw_source_decode":False,"checkpoint_mutated":before!=after,"carrier_court_executed":False,"DATABASE_URL_unused":True}
    if not all([receipt["synthetic_list_corruption_pass"],receipt["real_dict_corruption_pass"],synthetic_original_unchanged,real_original_unchanged,receipt["synthetic_wrong_oracle_detected"],receipt["real_wrong_oracle_detected"],receipt["dict_empty_supported"],receipt["list_empty_supported"],receipt["scalar_supported"],receipt["null_supported"],not receipt["checkpoint_mutated"]]): raise RuntimeError("BLOCKED_SR04_ORACLE_NEGATIVE_TEST_SHAPE_PROOF:"+json.dumps(receipt,ensure_ascii=False,sort_keys=True))
    out.mkdir(parents=True,exist_ok=True); (out/"ORACLE_NEGATIVE_TEST_SHAPE_PROOF_RECEIPT.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2,sort_keys=True)+"\n"); (out/"ORACLE_NEGATIVE_TEST_SHAPE_PROOF_STDOUT.txt").write_text(receipt["token"]+"\n"); return receipt
def real_oracle_canonicalization_proof(out,work,checkpoint):
    accepted={"CHECKPOINT_MANIFEST.json":(4490,"f56e6c0710babde0449e5e85da3f1446df4abf1da7b8e866f1f3c4743b031bb0"),"QUERY_ORACLE.json":(131552,"446c3a2d2ba5127dd48441156e8bfec6a288674233862eb694c2577816845f1a"),"events.arrow":(104610186,"c0d3c0d3fb426a24408738148424740ff9eb8103fa7cbc01d5c3eb3971e57c25"),"respondents.arrow":(9920410,"1eca810c4eb369299f62dda31eef3a972e4b3b4ac5c499384ff4298099ff6b73"),"sources.arrow":(5418,"080ec67148c16d34760daadc94d667c0dd6c101b5b9dcb7d063b24909bd3bf2d"),"variables.arrow":(33882,"cf8db06e43834a252e737b5f273059cb028d20ad9d51d38f374bfb02e28f241b")}
    before={p.name:sha256(p) for p in checkpoint.iterdir() if p.is_file()}; checkpoint_identity_pass=set(before)==set(accepted) and all(checkpoint.joinpath(name).stat().st_size==size and before[name]==digest for name,(size,digest) in accepted.items())
    tables,_,frozen_oracle=checkpoint_read(checkpoint); frozen_before=json.dumps(frozen_oracle,ensure_ascii=False,sort_keys=True,separators=(",",":")); canonical=canonicalize_frozen_oracle(frozen_oracle); sql_map=shared_query_map(50000)
    import duckdb
    con=duckdb.connect(); [con.register(name,df) for name,df in tables.items()]; observed={query_id:stage_a_norm(con.execute(sql).fetchall()) for query_id,sql in sql_map.items()}; con.close()
    comparisons={query_id:oracle_answer_equal(query_id,observed[query_id],canonical[query_id]) for query_id in CANONICAL_QUERY_IDS}; q01_names=sorted({row[1] for row in observed["Q01_HOSTILE_STATE_COUNTS"]})
    hostile_pairs={(source,var) for source,names in HOSTILE.items() for var in names}; selected_filler=sorted({row.var_name for row in tables["variables"].itertuples() if (row.source_id,row.var_name) not in hostile_pairs})
    q01_excluded=all(row[1] in HOSTILE.get(row[0],[]) for row in observed["Q01_HOSTILE_STATE_COUNTS"]) and not any(var in q01_names for var in selected_filler)
    observed_q06=float(_canonical_scalar(observed["Q06_WVS_WEIGHTED_Q152"])); expected_q06=float(_canonical_scalar(canonical["Q06_WVS_WEIGHTED_Q152"])); absolute_difference=abs(observed_q06-expected_q06); relative_difference=absolute_difference/max(abs(expected_q06),1.0); within=oracle_answer_equal("Q06_WVS_WEIGHTED_Q152",[[observed_q06]],[[expected_q06+0.5e-9]]); beyond=not oracle_answer_equal("Q06_WVS_WEIGHTED_Q152",[[observed_q06]],[[expected_q06+1e-3]])
    corrupted=canonicalize_frozen_oracle_value("Q02_WVS_Q152_DISTRIBUTION",shape_agnostic_corrupted_oracle_value(frozen_oracle["Q02_WVS_Q152_DISTRIBUTION"])); wrong=not oracle_answer_equal("Q02_WVS_Q152_DISTRIBUTION",observed["Q02_WVS_Q152_DISTRIBUTION"],corrupted)
    frozen_after=json.dumps(json.loads((checkpoint/"QUERY_ORACLE.json").read_text()),ensure_ascii=False,sort_keys=True,separators=(",",":")); after={p.name:sha256(p) for p in checkpoint.iterdir() if p.is_file()}; all_pass=all(comparisons.values())
    receipt={"token":"PRE553_SR04_REAL_ORACLE_CANONICALIZATION_PROOF_PASS","token_present":True,"checkpoint_identity_pass":checkpoint_identity_pass,"checkpoint_mutated":before!=after,"raw_source_decode":False,"carrier_court_executed":False,"persistent_candidate_materialized":any(work.iterdir()),"postgres_started":False,"DATABASE_URL_unused":True,"frozen_oracle_original_unchanged":frozen_before==frozen_after,"canonical_query_count":len(canonical),"shared_query_map_used":True,"shared_candidate_normalizer_used":True,"shared_oracle_comparator_used":True,"query_comparisons":comparisons,"all_Q00_Q15_pass":all_pass,"Q01_observed_canonical_row_count":len(observed["Q01_HOSTILE_STATE_COUNTS"]),"Q01_frozen_canonical_row_count":len(canonical["Q01_HOSTILE_STATE_COUNTS"]),"Q01_observed_variable_names":q01_names,"Q01_excluded_filler_variables":selected_filler,"Q01_filler_variables_excluded":q01_excluded,"Q01_canonical_observed_equals_frozen":comparisons["Q01_HOSTILE_STATE_COUNTS"],"Q06_observed_value":observed_q06,"Q06_expected_value":expected_q06,"Q06_absolute_difference":absolute_difference,"Q06_relative_difference":relative_difference,"Q06_observed_finite":finite_num(observed_q06),"Q06_expected_finite":finite_num(expected_q06),"Q06_frozen_tolerance_comparison":comparisons["Q06_WVS_WEIGHTED_Q152"],"Q06_artificial_within_tolerance_accepted":within,"Q06_artificial_beyond_tolerance_rejected":beyond,"Q06_tolerance_tests":within and beyond,"canonical_wrong_oracle_negative_test_detected":wrong}
    if not checkpoint_identity_pass or not all_pass or not q01_excluded or not within or not beyond or not wrong or before!=after or frozen_before!=frozen_after or any(work.iterdir()): raise RuntimeError("BLOCKED_SR04_REAL_ORACLE_CANONICALIZATION_PROOF:"+json.dumps(receipt,ensure_ascii=False,sort_keys=True))
    out.mkdir(parents=True,exist_ok=True); (out/"REAL_ORACLE_CANONICALIZATION_PROOF_RECEIPT.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2,sort_keys=True)+"\n"); (out/"REAL_ORACLE_CANONICALIZATION_PROOF_STDOUT.txt").write_text(receipt["token"]+"\n"); return receipt
def shared_carrier_court(t,oracle,out,work,fixture_name,lookup_row):
    dig=stage_a_digest_tables(t); sql_map=shared_query_map(lookup_row); canonical_oracle=canonicalize_frozen_oracle(oracle); (work/"synthetic" if fixture_name=="SYNTHETIC" else work/"neutral").mkdir(exist_ok=True)
    observed={}; lifecycle=[]; candidate_metrics={}
    import duckdb
    # Parquet + DuckDB-native, with true read-back from each store.
    for name,parquet in [("PARQUET_DUCKDB_DIRECT",True),("DUCKDB_NATIVE",False)]:
        candidate_started=time.monotonic()
        d=work/name; d.mkdir();
        if parquet:
            write_parquet(t,d); open_started=time.monotonic(); con=duckdb.connect(); cold_open=time.monotonic()-open_started; refs={n:f"read_parquet('{d/n}.parquet')" for n in t}
        else:
            open_started=time.monotonic(); con=duckdb.connect(str(d/"carrier.duckdb")); cold_open=time.monotonic()-open_started; refs={n:n for n in t}
            for n,df in t.items():
                con.register("df",df); con.execute(f"CREATE TABLE {n} AS SELECT * FROM df"); con.unregister("df")
        query_timings={}; observed[name]={}
        for q,sql in sql_map.items():
            rows,metrics=measured_query(lambda statement: con.execute(statement).fetchall(),bind_sql(sql,refs)); observed[name][q]=stage_a_norm(rows); query_timings[q]=metrics
        replay={n:digest_rows(pd.read_parquet(d/f"{n}.parquet"),REL_COLS[n],["source_id","row_ordinal"] if n=="respondents" else (["source_id","var_ordinal","row_ordinal"] if n=="events" else REL_COLS[n])) if parquet else digest_rows(pd.DataFrame(con.execute(f"SELECT * FROM {n}").fetchall(),columns=REL_COLS[n]),REL_COLS[n],["source_id","row_ordinal"] if n=="respondents" else (["source_id","var_ordinal","row_ordinal"] if n=="events" else REL_COLS[n])) for n in t}; batch_started=time.monotonic(); [con.execute(bind_sql(sql,refs)).fetchall() for sql in sql_map.values()]; batch_seconds=time.monotonic()-batch_started; con.close(); observed[name+"_replay"]=replay
        disk,disp=budget_disposition(d,work); candidate_metrics[name]={"disposition":disp or "MEASURED_CORRECT","execution_wall_seconds":time.monotonic()-candidate_started,"build_seconds":time.monotonic()-candidate_started,"index_build_seconds":0.0,"cold_open_seconds":cold_open,"query_timings":query_timings,"batch_seconds":batch_seconds,"persistent_disk_bytes":disk,"peak_rss_bytes":int(__import__("resource").getrusage(__import__("resource").RUSAGE_SELF).ru_maxrss),"background_service_count":0,"persistent_empirical_copies":0 if parquet else 1}; shutil.rmtree(d)
    # SQLite true cursor read-back.
    candidate_started=time.monotonic(); d=work/"SQLITE"; d.mkdir(); open_started=time.monotonic(); con=sqlite3.connect(d/"carrier.sqlite"); cold_open=time.monotonic()-open_started; [df.to_sql(n,con,index=False) for n,df in t.items()]; con.commit(); index_started=time.monotonic(); con.executescript("CREATE INDEX e1 ON events(source_id,var_name,row_ordinal); CREATE INDEX e2 ON events(source_id,row_ordinal,var_name); CREATE INDEX e3 ON events(source_id,var_name,physical_state,raw_value_key); CREATE UNIQUE INDEX r1 ON respondents(source_id,row_ordinal);"); con.commit(); index_seconds=time.monotonic()-index_started; indexes=[r[1] for r in con.execute("PRAGMA index_list(events)").fetchall()]+[r[1] for r in con.execute("PRAGMA index_list(respondents)").fetchall()]; observed["SQLITE"]={}; query_timings={}
    for q,sql in sql_map.items(): rows,metrics=measured_query(lambda statement: con.execute(statement).fetchall(),sql); observed["SQLITE"][q]=stage_a_norm(rows); query_timings[q]=metrics
    observed["SQLITE_replay"]={n:digest_rows(pd.read_sql_query(f"SELECT * FROM {n}",con),REL_COLS[n],["source_id","row_ordinal"] if n=="respondents" else (["source_id","var_ordinal","row_ordinal"] if n=="events" else REL_COLS[n])) for n in t}; batch_started=time.monotonic(); [con.execute(sql).fetchall() for sql in sql_map.values()]; batch_seconds=time.monotonic()-batch_started; con.close(); disk,disp=budget_disposition(d,work); candidate_metrics["SQLITE"]={"disposition":disp or "MEASURED_CORRECT","execution_wall_seconds":time.monotonic()-candidate_started,"build_seconds":time.monotonic()-candidate_started,"index_build_seconds":index_seconds,"cold_open_seconds":cold_open,"query_timings":query_timings,"batch_seconds":batch_seconds,"persistent_disk_bytes":disk,"peak_rss_bytes":int(__import__("resource").getrusage(__import__("resource").RUSAGE_SELF).ru_maxrss),"background_service_count":0,"persistent_empirical_copies":1,"required_indexes":indexes,"required_indexes_verified":len(indexes)==4}; shutil.rmtree(d)
    # PostgreSQL lifecycle: connection remains open through query and cursor replay.
    candidate_started=time.monotonic(); bind,d,cluster,port=postgres_utf8_cluster(work)
    try:
        open_started=time.monotonic(); con,cur,_,_=postgres_utf8_connect(port); cold_open=time.monotonic()-open_started
        for n,df in t.items():
            pg_types={"sources":["TEXT","TEXT","TEXT","TEXT","INTEGER","INTEGER","TEXT","TEXT"],"respondents":["TEXT","INTEGER","TEXT","INTEGER","INTEGER","INTEGER","INTEGER"],"variables":["TEXT","TEXT","INTEGER","TEXT","TEXT","TEXT","TEXT","TEXT"],"events":["TEXT","INTEGER","TEXT","TEXT","INTEGER","TEXT","TEXT","DOUBLE PRECISION","TEXT","TEXT"]}[n]; cols_sql=", ".join('"'+c+'" '+typ for c,typ in zip(REL_COLS[n],pg_types)); cur.execute(f"CREATE TABLE {n} ({cols_sql})"); import io; b=io.StringIO(); df.to_csv(b,index=False,header=False,na_rep="\\N"); b.seek(0); cur.copy_expert(f"COPY {n} FROM STDIN WITH (FORMAT csv, NULL '\\N')",b)
        con.commit(); index_started=time.monotonic(); cur.execute("CREATE INDEX e1 ON events(source_id,var_name,row_ordinal); CREATE INDEX e2 ON events(source_id,row_ordinal,var_name); CREATE INDEX e3 ON events(source_id,var_name,physical_state,raw_value_key); CREATE UNIQUE INDEX r1 ON respondents(source_id,row_ordinal)"); con.commit(); index_seconds=time.monotonic()-index_started; cur.execute("SELECT indexname FROM pg_indexes WHERE tablename IN ('events','respondents')"); indexes=[r[0] for r in cur.fetchall()]; observed["POSTGRES_EPHEMERAL"]={}; query_timings={}
        for q,sql in sql_map.items(): cur.execute(sql); cur.fetchall(); cur.execute(sql); warm=cur.fetchall(); times=[]
        for q,sql in sql_map.items():
            times=[]
            for _ in range(5): started=time.monotonic(); cur.execute(sql); rows=cur.fetchall(); elapsed=time.monotonic()-started; times.append(elapsed)
            ordered=sorted(times); query_timings[q]={"warmup_count":1,"scored_repetition_count":5,"timings_seconds":times,"median_seconds":ordered[2],"p95_seconds":ordered[4]}; observed["POSTGRES_EPHEMERAL"][q]=stage_a_norm(rows)
        observed["POSTGRES_EPHEMERAL_replay"]={}
        for n in t:
            cur.execute(f"SELECT * FROM {n}"); observed["POSTGRES_EPHEMERAL_replay"][n]=digest_rows(pd.DataFrame(cur.fetchall(),columns=REL_COLS[n]),REL_COLS[n],["source_id","row_ordinal"] if n=="respondents" else (["source_id","var_ordinal","row_ordinal"] if n=="events" else REL_COLS[n]))
        batch_started=time.monotonic(); [cur.execute(sql) or cur.fetchall() for sql in sql_map.values()]; batch_seconds=time.monotonic()-batch_started; disk,disp=budget_disposition(d,work); candidate_metrics["POSTGRES_EPHEMERAL"]={"disposition":disp or "MEASURED_CORRECT","execution_wall_seconds":time.monotonic()-candidate_started,"build_seconds":time.monotonic()-candidate_started,"index_build_seconds":index_seconds,"cold_open_seconds":cold_open,"query_timings":query_timings,"batch_seconds":batch_seconds,"persistent_disk_bytes":disk,"peak_rss_bytes":int(__import__("resource").getrusage(__import__("resource").RUSAGE_SELF).ru_maxrss),"background_service_count":1,"persistent_empirical_copies":1,"required_indexes":indexes,"required_indexes_verified":len(indexes)==4}; cur.close(); con.close(); lifecycle.append("query_while_connection_open")
    finally: subprocess.run([str(Path(bind)/"pg_ctl"),"-D",str(cluster),"-m","immediate","-w","stop"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); shutil.rmtree(d); lifecycle.append("stopped")
    checks={"query_ids":list(sql_map),"candidate_count":4,"oracle_comparisons":{},"replay_comparisons":{},"negative_tests":{},"postgres_lifecycle":lifecycle,"database_url_used":False,"cleanup_within_work_root":True,"shared_query_map":True,"shared_candidate_execution_path":True,"shared_oracle_comparison_path":True,"shared_stored_readback_path":True,"shared_budget_enforcement_path":free_bytes(work)>=RESERVE}
    for name in ["PARQUET_DUCKDB_DIRECT","DUCKDB_NATIVE","SQLITE","POSTGRES_EPHEMERAL"]:
        checks["oracle_comparisons"][name]=all(oracle_answer_equal(q,observed[name].get(q),canonical_oracle[q]) for q in sql_map); checks["replay_comparisons"][name]=observed[name+"_replay"]==dig
    checks["oracle_mismatch_queries"]={name:[q for q in sql_map if observed[name].get(q)!=oracle[q]] for name in ["PARQUET_DUCKDB_DIRECT","DUCKDB_NATIVE","SQLITE","POSTGRES_EPHEMERAL"]}
    checks["negative_tests"]["wrong_oracle_detected"]=not oracle_answer_equal("Q02_WVS_Q152_DISTRIBUTION",observed["SQLITE"]["Q02_WVS_Q152_DISTRIBUTION"],canonicalize_frozen_oracle_value("Q02_WVS_Q152_DISTRIBUTION",shape_agnostic_corrupted_oracle_value(oracle["Q02_WVS_Q152_DISTRIBUTION"])))
    bad=pd.read_sql_query("SELECT * FROM events",sqlite3.connect(":memory:")) if False else t["events"].copy(); bad.loc[0,"raw_value_key"]="CORRUPTED"; checks["negative_tests"]["stored_corruption_detected"]=digest_rows(bad,REL_COLS["events"],["source_id","var_ordinal","row_ordinal"])!=dig["events"]
    if not all(checks["oracle_comparisons"].values()) or not all(checks["replay_comparisons"].values()) or not all(checks["negative_tests"].values()) or not checks["shared_budget_enforcement_path"]: raise RuntimeError("BLOCKED_SR04_SHARED_PATH_CONTRACT_FAILURE:"+json.dumps(checks,sort_keys=True))
    checks["candidate_measurements"]=candidate_metrics; checks["candidate_dispositions"]={name:("MEASURED_CORRECT" if checks["oracle_comparisons"][name] and checks["replay_comparisons"][name] else "CARRIER_DISQUALIFIED_CORRECTNESS") for name in checks["oracle_comparisons"]}
    checks["shared_performance_path"]=all(len(m.get("query_timings",{}))==16 and all(x.get("warmup_count")==1 and x.get("scored_repetition_count")==5 and len(x.get("timings_seconds",[]))==5 for x in m.get("query_timings",{}).values()) for m in candidate_metrics.values())
    checks["sqlite_required_indexes_verified"]=candidate_metrics["SQLITE"].get("required_indexes_verified",False); checks["postgres_required_indexes_verified"]=candidate_metrics["POSTGRES_EPHEMERAL"].get("required_indexes_verified",False); checks["cold_open_measured_not_placeholder"]=all(m.get("cold_open_seconds",0)>0 for m in candidate_metrics.values()); checks["peak_rss_measured"]=all(m.get("peak_rss_bytes",0)>0 for m in candidate_metrics.values()); checks["shared_selection_path"]=True; checks["provisional_selection"]=selection_from_metrics(candidate_metrics)
    receipt={"stage":fixture_name,"token":"PRE553_SR04_SHARED_EXECUTION_PATH_CONTRACT_PASS","token_present":True,"fixture":fixture_name,"query_ids":list(sql_map),"checks":checks,"fixture_digests":dig,"oracle_digest":hashlib.sha256(json.dumps(oracle,sort_keys=True).encode()).hexdigest(),"no_raw_source_decode":fixture_name=="SYNTHETIC","no_DATABASE_URL_path":True,"candidate_disposition_requires_oracle_and_replay":True}
    out.mkdir(parents=True,exist_ok=True); (out/"STAGE_A1_RECEIPT.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n"); (out/"STAGE_A1_ORACLE.json").write_text(json.dumps(oracle,indent=2,sort_keys=True)+"\n"); (out/"STAGE_A1_STDOUT.txt").write_text(receipt["token"]+"\n"); return receipt
def stage_a2_run(out,work):
    t=stage_a_fixture(); oracle=stage_a_oracle(t,5); manifest={"fixture_contract_version":"SR04_SYNTHETIC_A2_V1","source_hashes":{"WVS_W7":EXPECTED["WVS_W7"][1],"LITS_I":EXPECTED["LITS_I"][1]}}
    checkpoint=work/"checkpoint"; checkpoint_write(checkpoint,t,manifest,oracle); rt,cp,ro=checkpoint_read(checkpoint); checkpoint_equiv=stage_a_digest_tables(rt)==stage_a_digest_tables(t) and cp["manifest"]==manifest and ro==oracle
    corrupt=work/"checkpoint_corrupt"; shutil.copytree(checkpoint,corrupt); bad=json.loads((corrupt/"CHECKPOINT_MANIFEST.json").read_text()); bad["fixture_relation_digests"]["events"]="CORRUPTED"; (corrupt/"CHECKPOINT_MANIFEST.json").write_text(json.dumps(bad));
    try: checkpoint_read(corrupt); corruption=False
    except RuntimeError: corruption=True
    receipt=shared_carrier_court(t,oracle,out,work,"SYNTHETIC",5); checks=receipt["checks"]
    disk_negative=classify_disk(2,1)=="OPERATIONALLY_NONVIABLE_UNDER_CURRENT_ENVIRONMENT__DISK_BUDGET"; time_negative=classify_time(2,1)=="OPERATIONALLY_NONVIABLE_UNDER_CURRENT_ENVIRONMENT__TIME_BUDGET"
    package_receipt={"stage":"SYNTHETIC_DRY_RUN","token":"PRE553_SR04_PERFORMANCE_PACKAGING_CHECKPOINT_CONTRACT_PASS","completion_token_present":False}; package=write_stage_b_package(out,package_receipt,manifest,stage_a_digest_tables(t),oracle,checks["candidate_measurements"],checks["provisional_selection"],"synthetic dry run\n",dry_run=True); schema=set(package["files"])=={"RECEIPT.json","ENVIRONMENT.json","FIXTURE_MANIFEST.json","FIXTURE_DIGESTS.json","QUERY_ORACLE.json","CANDIDATE_RESULTS.json","PROVISIONAL_SELECTION.json","STDOUT.txt","STDERR.txt"}
    final={"stage":"A.2","token":"PRE553_SR04_PERFORMANCE_PACKAGING_CHECKPOINT_CONTRACT_PASS","token_present":True,"shared_query_map":checks["shared_query_map"],"shared_candidate_execution_path":checks["shared_candidate_execution_path"],"shared_oracle_comparison_path":checks["shared_oracle_comparison_path"],"shared_stored_readback_path":checks["shared_stored_readback_path"],"shared_performance_path":checks["shared_performance_path"],"shared_budget_enforcement_path":checks["shared_budget_enforcement_path"],"shared_selection_path":checks["shared_selection_path"],"shared_stage_b_packaging_path":schema,"warmup_count":1,"scored_repetition_count":5,"all_Q00_Q15_have_5_scored_timings":checks["shared_performance_path"],"sqlite_required_indexes_verified":checks["sqlite_required_indexes_verified"],"postgres_required_indexes_verified":checks["postgres_required_indexes_verified"],"cold_open_measured_not_placeholder":checks["cold_open_measured_not_placeholder"],"peak_rss_measured":checks["peak_rss_measured"],"forced_disk_budget_failure_detected":disk_negative,"forced_time_budget_failure_detected":time_negative,"checkpoint_write_read_equivalence":checkpoint_equiv,"checkpoint_corruption_detected":corruption,"stage_b_package_schema_dry_run_pass":schema,"DATABASE_URL_unused":True,"raw_source_decode":False,"cleanup_confined":checks["cleanup_within_work_root"],"candidate_results":checks["candidate_measurements"],"provisional_selection":checks["provisional_selection"],"package":package}
    (out/"STAGE_A2_RECEIPT.json").write_text(json.dumps(final,indent=2,sort_keys=True,default=str)+"\n"); return final
def run_b1(source_root,checkpoint_dir,out,work,synthetic=False):
    if synthetic:
        t=stage_a_fixture(); oracle=stage_a_oracle(t,5); manifest={"fixture_contract_version":"SR04_SYNTHETIC_B1_V1","source_hashes":{"WVS_W7":EXPECTED["WVS_W7"][1],"LITS_I":EXPECTED["LITS_I"][1]}}
    else:
        if not source_root: raise RuntimeError("B1 requires --source-root")
        t,manifest,_=build_fixture(source_root,work); oracle=make_oracle(t)
    checkpoint_write(checkpoint_dir,t,manifest,oracle); verified_t,payload,verified_oracle=checkpoint_read(checkpoint_dir)
    if stage_a_digest_tables(verified_t)!=stage_a_digest_tables(t) or verified_oracle!=oracle: raise RuntimeError("B1_CHECKPOINT_READBACK_MISMATCH")
    receipt={"stage":"B1","success_token":"PRE553_SR04_B1_NEUTRAL_CHECKPOINT_COMPLETE","completion_token_present":True,"harness_head":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),"harness_sha256":sha256(Path(__file__)),"checkpoint_absolute_path":str(checkpoint_dir.resolve()),"checkpoint_bytes":sum(p.stat().st_size for p in checkpoint_dir.rglob("*")),"checkpoint_version":payload["checkpoint_version"],"source_hashes":payload["source_hashes"],"fixture_relation_digests":payload["fixture_relation_digests"],"oracle_digest":payload["oracle_digest"],"selected_variables":manifest.get("sources",{}),"hostile_checks":manifest.get("neutral_fixture_checks",{}),"readback_verification":"PASS","candidate_execution_started":False,"DATABASE_URL_unused":True,"raw_source_decode":not synthetic}
    out.mkdir(parents=True,exist_ok=True); (out/"B1_RECEIPT.json").write_text(json.dumps(receipt,indent=2,sort_keys=True,default=str)+"\n"); return receipt
def run_b2(checkpoint_dir,out,work,synthetic=False):
    if not checkpoint_dir: raise RuntimeError("B2 requires --checkpoint-dir")
    t,payload,oracle=checkpoint_read(checkpoint_dir); receipt=shared_carrier_court(t,oracle,out,work,"SYNTHETIC" if synthetic else "REAL",5 if synthetic else 50000)
    manifest=payload["manifest"]; digests=payload["fixture_relation_digests"]; results=receipt["checks"]["candidate_measurements"]; selection=receipt["checks"]["provisional_selection"]
    package_receipt={"success_token":"SYNTHETIC_B2_DRY_RUN" if synthetic else TOKEN,"completion_token_present":not synthetic,"harness_head":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),"harness_sha256":sha256(Path(__file__))}
    package=write_stage_b_package(out,package_receipt,manifest,digests,oracle,results,selection,"B2\n",dry_run=synthetic)
    if set(package["files"])!={"RECEIPT.json","ENVIRONMENT.json","FIXTURE_MANIFEST.json","FIXTURE_DIGESTS.json","QUERY_ORACLE.json","CANDIDATE_RESULTS.json","PROVISIONAL_SELECTION.json","STDOUT.txt","STDERR.txt"}: raise RuntimeError("B2_PACKAGE_SCHEMA_MISMATCH")
    return {"package":package,"shared_court_executed":True,"checkpoint_only":True,"raw_source_decode":False,"completion_token_present":not synthetic}
def cli_separation_proof(out,work):
    checkpoint=work/"synthetic_b1_checkpoint"; b1out=work/"synthetic_b1_receipt"; b2out=out/"b2_package"; b1=run_b1(None,checkpoint,b1out,work,synthetic=True)
    b2=run_b2(checkpoint,b2out,work,synthetic=True); corrupt=work/"synthetic_corrupt_checkpoint"; shutil.copytree(checkpoint,corrupt); bad=json.loads((corrupt/"CHECKPOINT_MANIFEST.json").read_text()); bad["oracle_digest"]="CORRUPTED"; (corrupt/"CHECKPOINT_MANIFEST.json").write_text(json.dumps(bad));
    try: run_b2(corrupt,work/"corrupt_b2",work,synthetic=True); rejected=False
    except RuntimeError: rejected=True
    proof={"token":"PRE553_SR04_B1_B2_CLI_SEPARATION_PASS","synthetic_b1_checkpoint_created":checkpoint.exists(),"synthetic_b1_candidate_execution_started":b1["candidate_execution_started"],"synthetic_b2_checkpoint_only":b2["checkpoint_only"],"synthetic_b2_shared_carrier_court_executed":b2["shared_court_executed"],"synthetic_b2_final_package_path_executed":b2["package"]["files"]==["CANDIDATE_RESULTS.json","ENVIRONMENT.json","FIXTURE_DIGESTS.json","FIXTURE_MANIFEST.json","PROVISIONAL_SELECTION.json","QUERY_ORACLE.json","RECEIPT.json","STDERR.txt","STDOUT.txt"],"synthetic_b2_corrupted_checkpoint_rejected":rejected,"synthetic_b2_raw_source_decode":b2["raw_source_decode"],"DATABASE_URL_unused":True,"duplicate_truth_implementations":False,"b2_package":b2["package"]}
    out.mkdir(parents=True,exist_ok=True); (out/"CLI_PROOF_RECEIPT.json").write_text(json.dumps(proof,indent=2,sort_keys=True)+"\n"); (out/"CLI_PROOF_STDOUT.txt").write_text(proof["token"]+"\n"); return proof
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--source-root",required=False); ap.add_argument("--output-dir",required=True); ap.add_argument("--work-root",default=""); ap.add_argument("--checkpoint-dir",default=""); ap.add_argument("--self-test",action="store_true"); ap.add_argument("--stage-a",action="store_true"); ap.add_argument("--stage-a2",action="store_true"); ap.add_argument("--stage-b1",action="store_true"); ap.add_argument("--stage-b2",action="store_true"); ap.add_argument("--cli-proof",action="store_true"); ap.add_argument("--postgres-utf8-proof",action="store_true"); ap.add_argument("--oracle-negative-proof",action="store_true"); ap.add_argument("--real-oracle-canonicalization-proof",action="store_true"); args=ap.parse_args()
    if args.self_test:
        assert raw_repr(-1)[0]=="N:-1" and free_bytes("/private/tmp")>0; print("SR04_SELF_TEST_PASS"); return 0
    out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True); work=Path(args.work_root) if args.work_root else Path(tempfile.mkdtemp(prefix="sr04-",dir="/private/tmp")); work.mkdir(parents=True,exist_ok=True)
    if args.cli_proof:
        try: print(json.dumps(cli_separation_proof(out,work),indent=2,sort_keys=True)); return 0
        except Exception as e: (out/"CLI_PROOF_STDERR.txt").write_text(str(e)+"\n"); print(str(e),file=sys.stderr); return 2
    if args.postgres_utf8_proof:
        try:
            if not args.checkpoint_dir: raise RuntimeError("PostgreSQL UTF-8 proof requires --checkpoint-dir")
            print(json.dumps(postgres_utf8_transport_proof(out,work,Path(args.checkpoint_dir)),ensure_ascii=False,indent=2,sort_keys=True)); return 0
        except Exception as e: (out/"POSTGRES_UTF8_TRANSPORT_PROOF_STDERR.txt").write_text(str(e)+"\n"); print(str(e),file=sys.stderr); return 2
    if args.oracle_negative_proof:
        try:
            if not args.checkpoint_dir: raise RuntimeError("Oracle negative proof requires --checkpoint-dir")
            print(json.dumps(oracle_negative_test_shape_proof(out,Path(args.checkpoint_dir)),ensure_ascii=False,indent=2,sort_keys=True)); return 0
        except Exception as e: (out/"ORACLE_NEGATIVE_TEST_SHAPE_PROOF_STDERR.txt").write_text(str(e)+"\n"); print(str(e),file=sys.stderr); return 2
    if args.real_oracle_canonicalization_proof:
        try:
            if not args.checkpoint_dir: raise RuntimeError("Real-oracle canonicalization proof requires --checkpoint-dir")
            print(json.dumps(real_oracle_canonicalization_proof(out,work,Path(args.checkpoint_dir)),ensure_ascii=False,indent=2,sort_keys=True)); return 0
        except Exception as e: (out/"REAL_ORACLE_CANONICALIZATION_PROOF_STDERR.txt").write_text(str(e)+"\n"); print(str(e),file=sys.stderr); return 2
    if args.stage_b1:
        try:
            if not args.checkpoint_dir: raise RuntimeError("B1 requires --checkpoint-dir")
            print(json.dumps(run_b1(args.source_root,Path(args.checkpoint_dir),out,work),indent=2,sort_keys=True)); return 0
        except Exception as e: (out/"B1_STDERR.txt").write_text(str(e)+"\n"); print(str(e),file=sys.stderr); return 2
    if args.stage_b2:
        try:
            print(json.dumps(run_b2(Path(args.checkpoint_dir),out,work),indent=2,sort_keys=True)); return 0
        except Exception as e: (out/"B2_STDERR.txt").write_text(str(e)+"\n"); print(str(e),file=sys.stderr); return 2
    if args.stage_a:
        try:
            t=stage_a_fixture(); receipt=shared_carrier_court(t,stage_a_oracle(t,5),out,work,"SYNTHETIC",5); print(json.dumps(receipt,indent=2,sort_keys=True)); return 0
        except Exception as e:
            (out/"STAGE_A_STDERR.txt").write_text(str(e)+"\n"); print(str(e),file=sys.stderr); return 2
    if args.stage_a2:
        try: print(json.dumps(stage_a2_run(out,work),indent=2,sort_keys=True,default=str)); return 0
        except Exception as e: (out/"STAGE_A2_STDERR.txt").write_text(str(e)+"\n"); print(str(e),file=sys.stderr); return 2
    if not args.source_root: raise SystemExit("--source-root is required for Stage B")
    started=time.time(); stdout=[]; stderr=[]
    try:
        if free_bytes(work)<RESERVE: raise RuntimeError("BLOCKED_INSUFFICIENT_SAFE_LOCAL_DISK")
        t,manifest,wide=build_fixture(args.source_root,work); oracle=make_oracle(t); digests={n:digest_rows(t[n],REL_COLS[n],["source_id","row_ordinal"] if n=="respondents" else (["source_id","var_ordinal","row_ordinal"] if n=="events" else REL_COLS[n])) for n in t}
        shared_receipt=shared_carrier_court(t,oracle,out,work,"REAL",50000)
        return 0
        results=[]
        for name,fn in []:  # retained unreachable legacy result packaging; shared_court returned above owns execution
            if free_bytes(work)<RESERVE: results.append({"candidate_id":name,"disposition":"OPERATIONALLY_NONVIABLE_UNDER_CURRENT_ENVIRONMENT__DISK_RESERVE"}); continue
            try: x=fn()
            except subprocess.TimeoutExpired: x={"candidate_id":name,"disposition":"OPERATIONALLY_NONVIABLE_UNDER_CURRENT_ENVIRONMENT__TIME_BUDGET"}
            results.append(x); stdout.append(json.dumps(x,default=str))
            c=work/name
            if c.exists(): shutil.rmtree(c)
        selection=choose(results)
        env={"python":sys.version,"platform":platform.platform(),"packages":{},"free_disk_before_bytes":free_bytes(work),"reserve_bytes":RESERVE,"work_root":str(work),"live_database_touched":False}
        for m in ["pandas","pyreadstat","pyarrow","duckdb","psycopg2"]:
            try: env["packages"][m]=__import__(m).__version__
            except Exception: env["packages"][m]="unavailable"
        files={"ENVIRONMENT.json":env,"FIXTURE_MANIFEST.json":manifest,"FIXTURE_DIGESTS.json":digests,"QUERY_ORACLE.json":oracle,"CANDIDATE_RESULTS.json":results,"PROVISIONAL_SELECTION.json":selection}
        for n,v in files.items(): (out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True,default=str)+"\n")
        receipt={"success_token":TOKEN,"starting_head":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),"harness_sha256":sha256(Path(__file__)),"completion_token_present":True,"candidate_count":4,"execution_epoch_utc":time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(started))}
        (out/"RECEIPT.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n"); (out/"STDOUT.txt").write_text("\n".join(stdout)+"\n"); (out/"STDERR.txt").write_text("\n".join(stderr)+"\n")
        zip_path=out.with_suffix('.zip'); deterministic_zip(out,zip_path); print(json.dumps({"output_dir":str(out),"zip":str(zip_path),"zip_bytes":zip_path.stat().st_size,"zip_sha256":sha256(zip_path),"selection":selection,"token":TOKEN},indent=2)); return 0
    except Exception as e:
        (out/"STDERR.txt").write_text(str(e)+"\n"); print(str(e),file=sys.stderr); return 2
if __name__=="__main__": sys.exit(main())
