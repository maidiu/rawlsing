"""Disposable S3 storage/posting-index sourcefree scale court (NOT native I03).

Builds deliberately *non-authoritative* synthetic physical records through
EXISTING four-store Store S3 schema. Replays its exact commit/full 13-family
body-audit/cold-open/query pathway without using or reading any real survey.
Synthetic bodies are intentionally NOT valid C11 scientific objects.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import statistics
import time
import traceback

from .stores import FAMILIES, Store, StoreFailure, canonical, digest
from . import runner

GRADE = "SOURCEFREE_SYNTHETIC_PHYSICAL_S3_ONLY__NOT_NATIVE_I03_OR_SURVEY"


def parse_cases(raw: str) -> tuple[tuple[int,int],...]:
    cases=[]
    try:
        for part in raw.split(","):
            a,b=part.split(":")
            case=(int(a),int(b))
            if case[0]<1 or not 1<=case[1]<=100 or case in cases:
                raise ValueError("row/question counts invalid or duplicated")
            cases.append(case)
    except (ValueError,TypeError) as exc:
        raise argparse.ArgumentTypeError("expected unique rows:questions cases with 1..100 questions") from exc
    if not cases:
        raise argparse.ArgumentTypeError("at least one case required")
    return tuple(cases)


def ref(kind: str, pos: int) -> str:
    return (kind+"@1.0.0|urn:rawlsing:sourcefree:s3scale:"+kind+":"+str(pos)
            +"|"+format(pos,"064x"))


def make_row(family: str, object_ref: str, *, respondent: str="", native: str="",
             raw_typed: str="0") -> dict:
    # Synthetic body is NOT a valid Rawlsing scientific object by design.
    body={"schema":"BENCHMARK_PHYSICAL_NOT_C11","family":family,"ref":object_ref,
          "respondent":respondent,"native":native,
          "typed_state":"SOURCEFREE_SCALED_STATE","raw_typed":raw_typed,
          "payload":"short encoded physical row for controlled scale only"}
    return {"family":family,"ref":object_ref,"body_json":canonical(body),
            "respondent":respondent or None,"native":native or None,
            "typed_state":"SOURCEFREE_SCALED_STATE","raw_typed":raw_typed}


def _digest_record(hasher, ref_key: str, body: str):
    serial=ref_key.encode()+b"\x00"+body.encode()
    hasher.update(len(serial).to_bytes(8,"big"));hasher.update(serial)


def _single_case(root: Path, respondents: int, questions: int,
                 *, keep: bool, max_rss_gib: int) -> dict:
    case_dir=root/(f"r{respondents}-q{questions}")
    case_dir.mkdir(exist_ok=False)
    dbpath=case_dir/"synthetic_s3.sqlite"
    identity={"schema":"BENCHMARK_PHYSICAL_NOT_C11","source_id":"SOURCEFREE_ONLY",
              "rows":respondents,"questions":questions}
    output={"status":"RUNNING","respondents":respondents,"questions":questions,
            "synthetic_cells":respondents*questions,"grade":GRADE,
            "database":str(dbpath),"stages_s":{},"physical_probes":[],
            "source_identity":identity}
    emit=runner.EventLogger(case_dir/"progress.jsonl","SOURCEFREE_S3")
    store=None
    try:
        with runner.Resources(case_dir,emit,ceiling=max_rss_gib*1024**3) as watch:
            started=time.perf_counter()
            store=Store("S3",dbpath,case_dir,create=True,source_identity=identity,progress=emit)
            records={}
            for family in FAMILIES:
                h=hashlib.sha256();count=0
                if family=="RespondentIdentity":
                    for rid in range(respondents):
                        key=ref("RespondentIdentity",rid)
                        row=make_row(family,key)
                        store.add_row(family,count,row,0,count)
                        _digest_record(h,key,row["body_json"])
                        count+=1
                        if count % 2048==0:store.commit_batch()
                elif family=="QuestionVariableBinding":
                    for q in range(questions):
                        key=ref("QuestionVariableBinding",q)
                        row=make_row(family,key,native=ref("NATIVE_QUESTION",q))
                        store.add_row(family,count,row,0,count,
                                      binding=(ref("NATIVE_QUESTION",q),None,None))
                        _digest_record(h,key,row["body_json"]);count+=1
                elif family=="RespondentEvent":
                    for q in range(questions):
                        question=ref("NATIVE_QUESTION",q)
                        for rid in range(respondents):
                            pos=q*respondents+rid
                            key=ref("RespondentEvent",pos)
                            row=make_row(family,key,respondent=ref("RespondentIdentity",rid),
                                         native=question,raw_typed=str((q+rid)%8))
                            store.add_row(family,count,row,0,count)
                            _digest_record(h,key,row["body_json"]);count+=1
                            if count%2048==0:store.commit_batch()
                            if count%30000==0:
                                watch.check()
                                emit(stage="sourcefree_build",completed=count,
                                     declared=respondents*questions)
                store.commit_batch()
                records[family]={"count":count,"digest":h.hexdigest()}
                watch.check()
            output["stages_s"]["synthetic_store_build"]=round(time.perf_counter()-started,6)
            started=time.perf_counter()
            store.finish({"schema":"BENCHMARK_PHYSICAL_NOT_C11","family_counts":{
                k:v["count"] for k,v in records.items()}},records)
            output["stages_s"]["pre_audit_finish"]=round(time.perf_counter()-started,6)
            started=time.perf_counter()
            audited=store.audit_families(emit)
            output["stages_s"]["complete_13_family_body_audit"]=round(
                time.perf_counter()-started,6)
            if audited!=records:
                raise StoreFailure("sourcefree full body audit drift")
            store.close();store=None
            started=time.perf_counter()
            store=Store("S3",dbpath,case_dir,create=False,
                        source_identity=identity,read_only=True)
            output["stages_s"]["cold_connection_open"]=round(time.perf_counter()-started,6)
            if store.db.execute("PRAGMA query_only").fetchone()[0]!=1:
                raise StoreFailure("sourcefree reopen must be read-only")
            refs=store.get_question_refs(questions)
            if len(refs)!=questions:
                raise StoreFailure("sourcefree distinct target count drift")
            for target in refs:
                started=time.perf_counter()
                q=store.probe_query(target)
                q["measured_wall_ms"]=(time.perf_counter()-started)*1000
                if q["events"]!=respondents or q["respondents"]!=respondents or q["groups"]!=8:
                    raise StoreFailure("synthetic sourcefree physical outcome drift")
                output["physical_probes"].append(q)
            watch.check()
            output["physical_ms_per_query_median"]=round(statistics.median(
                x["measured_wall_ms"] for x in output["physical_probes"]),3)
            output["physical_ms_per_query_mean"]=round(statistics.mean(
                x["measured_wall_ms"] for x in output["physical_probes"]),3)
            output["per_question_physical_grade"]="SQL_GROUP_BY_ONLY__NOT_NATIVE_FACT"
            output["store_bytes"]=dbpath.stat().st_size
        output["peak_process_tree_rss_bytes"]=watch.peak_rss
        output["status"]="SOURCEFREE_PHYSICAL_EXECUTED"
    except BaseException as exc:
        output.update(status="SOURCEFREE_PHYSICAL_FAILED",error_type=type(exc).__name__,
                      error=str(exc),traceback=traceback.format_exc(limit=10))
    finally:
        if store is not None:store.close()
        emit(stage="final",status=output["status"]);emit.close()
        # Never delete an existing or user-supplied corpus. The case folder
        # was created above with exist_ok=False and contains ONLY our synthetic
        # output; remove just its generated SQLite, retain small receipts.
        if not keep:
            for suffix in ("","-wal","-shm"):
                path=Path(str(dbpath)+suffix)
                if path.is_file():path.unlink()
            output["synthetic_database_cleaned"]=True
        (case_dir/"report.json").write_text(json.dumps(output,indent=2)+"\n")
    return output


def main(argv=None):
    p=argparse.ArgumentParser(description="Disposable S3 scale at simulated respondent/question counts")
    p.add_argument("--work-root",type=Path,required=True,
                   help="existing scratch/output directory; new child is created, never overwritten")
    p.add_argument("--cases",type=parse_cases,default=((1500,1),(7337,1),(30000,1),(97220,1)))
    p.add_argument("--max-cells",type=int,default=1_500_000)
    p.add_argument("--max-rss-gib",type=int,default=6)
    p.add_argument("--keep-synthetic-db",action="store_true")
    args=p.parse_args(argv)
    if args.max_cells<1 or args.max_rss_gib<1 or args.max_rss_gib>6:
        p.error("positive max cells and 1..6 GiB process RSS cap required")
    if any(n*q>args.max_cells for n,q in args.cases):
        p.error("selected rows×questions exceed --max-cells cap; select fewer questions or explicitly raise cap")
    args.work_root=args.work_root.expanduser().resolve()
    if not args.work_root.is_dir():p.error("--work-root must already exist")
    if shutil.disk_usage(args.work_root).free<4*1024**3:
        p.error("at least 4 GiB free scratch space required before synthetic construction")
    root=args.work_root/("S3-SOURCEFREE-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")+"-"+str(os.getpid()))
    root.mkdir(exist_ok=False)
    reports=[]
    try:
        for n,q in args.cases:
            report=_single_case(root,n,q,keep=args.keep_synthetic_db,max_rss_gib=args.max_rss_gib)
            reports.append(report)
            if report["status"]!="SOURCEFREE_PHYSICAL_EXECUTED":break
    finally:
        (root/"summary.json").write_text(json.dumps({"grade":GRADE,
           "status":"SOURCEFREE_PHYSICAL_EXECUTED" if len(reports)==len(args.cases) and all(
               x["status"]=="SOURCEFREE_PHYSICAL_EXECUTED" for x in reports) else "PARTIAL_OR_FAILED",
           "reports":reports,"no_original_survey_access":True,
           "not_native_i03":True},indent=2)+"\n")
    print(canonical({"summary":str(root/"summary.json"),"status":reports[-1]["status"]}))
    return 0 if len(reports)==len(args.cases) and all(
        x["status"]=="SOURCEFREE_PHYSICAL_EXECUTED" for x in reports) else 2

if __name__=="__main__":
    raise SystemExit(main())
