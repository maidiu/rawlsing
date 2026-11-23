"""Opt-in, read-only S3 native-repeat and distinct-physical economics courts.

NO new source issuer, no synthetic native operation, no C11 store rebuild.
Requires the original held R2/issued operation for native mode; physical
mode still checks source/currentness and audits every saved body.

Run with the exact original four-store code checkout plus this additive module.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from statistics import median
import time
import traceback
from datetime import datetime, timezone
from typing import Any

from . import runner
from .native import execute_issued, open_native_session
from .stores import FAMILIES, Store, StoreFailure, canonical, digest

GRADE_NATIVE = "TEST_ONLY_ORIGINAL_Q103_REPEAT__NOT_DISTINCT_OPERATIONS_OR_PRODUCTION"
GRADE_PHYSICAL = "PHYSICAL_ONLY_1_10_100_DISTINCT__NOT_ISSUED_NATIVE_I03"


def parse_counts(value: str) -> tuple[int, ...]:
    try:
        counts = tuple(int(v) for v in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected comma-separated positive integer counts") from exc
    if not counts or any(n < 1 or n > 100 for n in counts) or len(set(counts)) != len(counts):
        raise argparse.ArgumentTypeError("counts must be unique integers in 1..100")
    return counts


def _percentile(values: list[float], fraction: float) -> float:
    return sorted(values)[int((len(values)-1)*fraction)]


def _stats(values: list[float]) -> dict[str, float]:
    return {"executions":len(values),"total_s":round(sum(values),6),
            "median_ms":round(1000*median(values),3),
            "p95_ms":round(1000*_percentile(values,0.95),3),
            "min_ms":round(1000*min(values),3),
            "max_ms":round(1000*max(values),3)}


def _require_prior(run_dir: Path):
    db = run_dir/"S3"/"permanent.sqlite"
    report_path = run_dir/"S3"/"report.json"
    identity_path = run_dir/"held_source_identity.json"
    if not all(p.is_file() for p in (db,report_path,identity_path)):
        raise StoreFailure("S3 existing audited database, original report and held identity required")
    prior = json.loads(report_path.read_text())
    identity = json.loads(identity_path.read_text())
    if (prior.get("arm")!="S3" or prior.get("source_identity")!=identity
            or "full_corpus_body_audit" not in prior.get("stages_s",{})
            or set(prior.get("family_records",{}))!=set(FAMILIES)):
        raise StoreFailure("original S3 thirteen-family audit or source identity absent")
    return db, prior, identity, report_path


def _native_repeat(store: Store, source: Any, cfg: dict, config_path: Path,
                   prior: dict, counts: tuple[int,...], fresh_samples: int,
                   emit, watch):
    started=time.perf_counter()
    issued, grade = runner._native_operations(cfg,config_path.parent,source,emit)
    reconstruction=time.perf_counter()-started
    if len(issued)!=1 or grade != "ORIGINAL_ISSUED_OPERATION_OBJECTS_PROVIDED_BY_EXTERNAL_OWNER":
        raise StoreFailure("repeat court requires exactly one externally issued original operation")
    op=issued[0]
    baseline = prior.get("query_report",{}).get("native",[])
    if len(baseline)!=1 or baseline[0].get("output") is None:
        raise StoreFailure("original S3 result missing; cannot establish repeat-result parity")
    expected = baseline[0]["output"]
    expected_digest = digest(canonical(expected).encode())

    live_stats = {
        "live_calls": 0, "live_seconds": 0.0,
        "authorize_calls": 0, "authorize_seconds": 0.0,
    }
    original_live = source.verified._live
    original_authorize = source.verified._authorize

    def counted_live():
        started = time.perf_counter()
        try:
            return original_live()
        finally:
            live_stats["live_calls"] += 1
            live_stats["live_seconds"] += time.perf_counter() - started

    def counted_authorize(held):
        started = time.perf_counter()
        try:
            return original_authorize(held)
        finally:
            live_stats["authorize_calls"] += 1
            live_stats["authorize_seconds"] += time.perf_counter() - started

    object.__setattr__(source.verified, "_live", counted_live)
    object.__setattr__(source.verified, "_authorize", counted_authorize)

    def checked_execute(*, prepared_session=None):
        source.verified._live()
        val=execute_issued(store,source.verified,op,prepared_session=prepared_session)
        source.verified._live()
        if digest(canonical(val).encode())!=expected_digest or val!=expected:
            raise StoreFailure("repeat Q103 result differs from original exact native output")
        watch.check()
        return val

    fresh=[]
    for i in range(fresh_samples):
        st=time.perf_counter()
        checked_execute()  # creates a NEW native session, never a new SQLite
        fresh.append(time.perf_counter()-st)
        emit(stage="fresh_native_repeat",completed=i+1,declared=fresh_samples)
    st=time.perf_counter()
    session=open_native_session(store,source.verified,op.get("recorded_plan"))
    prepare_s=time.perf_counter()-st
    profile_path = os.environ.get("PYAT_S3_PROFILE_OUT")
    profile_live = None
    profile_execution_s = None
    if profile_path:
        import cProfile
        before_live = dict(live_stats)
        profile = cProfile.Profile()
        started = time.perf_counter()
        profile.enable()
        try:
            checked_execute(prepared_session=session)
        finally:
            profile.disable()
            profile_execution_s = time.perf_counter() - started
            profile.dump_stats(profile_path)
        profile_live = {
            key: live_stats[key] - before_live[key]
            for key in live_stats
        }
    batches=[]
    for n in counts:
        durations=[]
        for j in range(n):
            st=time.perf_counter()
            checked_execute(prepared_session=session)
            durations.append(time.perf_counter()-st)
            if j==0 or (j+1)%10==0 or j+1==n:
                emit(stage="prepared_native_repeat",batch=n,completed=j+1,declared=n)
        batches.append({"count":n,**_stats(durations)})
    return {
        "grade":GRADE_NATIVE,"operation_name":op.get("name",op["query"].ref.key),
        "distinct_issued_operations":1,
        "same_original_operation_repeated":True,
        "source_scoped_original_issuer_reconstruction_s":round(reconstruction,6),
        "initial_native_session_prepare_s":round(prepare_s,6),
        "fresh_session_per_execution":_stats(fresh) if fresh else None,
        "one_prepared_session_batches":batches,
        "exact_original_output_sha256":expected_digest,
        "original_native_fact_state":expected["facts"][0]["state"],
        "native_producer":"existing rawlsing_next.pre553_empirical_query.execute_empirical_query",
        "s04_producer":"existing rawlsing_next.pre553_s04_observed_research.receive_s04_i03_research",
        "live_guard": {
            "live_calls": live_stats["live_calls"],
            "live_seconds": round(live_stats["live_seconds"], 6),
            "authorize_calls": live_stats["authorize_calls"],
            "authorize_seconds": round(live_stats["authorize_seconds"], 6),
        },
        "profile_execution_s": (
            round(profile_execution_s, 6) if profile_execution_s is not None else None
        ),
        "profile_execution_live_guard": (
            {key: round(value, 6) for key, value in profile_live.items()}
            if profile_live is not None else None
        ),
        "profile_path": profile_path,
    }


def _distinct_physical(store: Store, prior: dict, counts: tuple[int,...],
                       repeats: int, emit, watch):
    refs=store.get_question_refs(max(counts))
    if len(refs)<max(counts) or len(set(refs))!=len(refs):
        raise StoreFailure("not enough source-native distinct physical questions")
    prior_probes={x["target_ref"]:x for x in prior.get("query_report",{}).get("physical_probes",[])}
    if not all(ref in prior_probes for ref in refs):
        raise StoreFailure("original S3 physical probe baseline missing selected exact questions")
    batches=[]
    for n in counts:
        scored=[]
        for round_idx in range(repeats):
            durations=[]
            for target in refs[:n]:
                st=time.perf_counter()
                result=store.probe_query(target)
                durations.append(time.perf_counter()-st)
                original=prior_probes[target]
                for k in ("digest","events","respondents","groups"):
                    if result[k]!=original[k]:
                        raise StoreFailure("S3 physical probe drift: "+k)
            scored.append(_stats(durations))
            watch.check()
            emit(stage="distinct_physical",batch=n,completed=round_idx+1,declared=repeats)
        batches.append({"distinct_questions":n,"repetitions":repeats,
                        "rounds":scored,"median_batch_total_ms":round(
                            1000*median([a["total_s"] for a in scored]),3)})
    return {"grade":GRADE_PHYSICAL,"batches":batches,
            "distinct_ref_list_sha256":digest(canonical(refs).encode()),
            "original_physical_probe_digest_parity":True,
            "note":"SQL GROUP BY only; does not execute or estimate native I03/S04"}


def run(config_path: Path, existing_run: Path, *, mode: str,
        counts: tuple[int,...]=(1,10,100), fresh_samples: int=3,
        physical_repeats: int=3) -> dict:
    config_path=config_path.expanduser().resolve()
    existing_run=existing_run.expanduser().resolve()
    if mode not in ("native-repeat","physical-distinct"):
        raise StoreFailure("unsupported mode")
    if not 0<=fresh_samples<=10 or not 1<=physical_repeats<=10:
        raise StoreFailure("sample parameters exceed safe bounded runner limits")
    if not counts or any(n<1 or n>100 for n in counts) or len(set(counts))!=len(counts):
        raise StoreFailure("counts must be unique in 1..100")
    config=json.loads(config_path.read_text())
    if config.get("schema")!="PYAT_FOUR_PERMANENT_STORE_BUNDLE@1":
        raise StoreFailure("wrong original bundle schema")
    db,prior,identity,report_path=_require_prior(existing_run)
    orig_stat=db.stat()
    report_bytes=report_path.read_bytes()
    output_root=existing_run/"native_replays"
    output_root.mkdir(exist_ok=True)
    folder=output_root/("S3-prepared-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")+"-"+str(os.getpid()))
    folder.mkdir(exist_ok=False)
    emit=runner.EventLogger(folder/"progress.jsonl","S3_PREPARED")
    out={"schema":"PYAT_S3_PREPARED_COST_COURT@1","status":"RUNNING",
         "mode":mode,"grade":GRADE_NATIVE if mode=="native-repeat" else GRADE_PHYSICAL,
         "existing_run":str(existing_run),"original_db":str(db),
         "report_directory":str(folder),"no_store_rebuild":True,
         "original_db_open_mode":"SQLITE_READ_ONLY", "counts":list(counts),
         "host":runner._host_details(),"source_identity":identity,
         "stages_s":{},"original_report_sha256":hashlib.sha256(report_bytes).hexdigest()}
    store=None
    try:
        with runner.Resources(folder,emit) as watch:
            st=time.perf_counter()
            source=runner.InputEstate(config,config_path.parent,emit)
            out["stages_s"]["source_admission"]=round(time.perf_counter()-st,6)
            if source.identity!=identity:
                raise StoreFailure("source differs from original S3 run")
            store=Store("S3",db,source.estate_path,create=False,
                        source_identity=source.identity,progress=emit,read_only=True)
            if store.db.execute("PRAGMA query_only").fetchone()[0]!=1:
                raise StoreFailure("saved store is not SQL read-only")
            st=time.perf_counter()
            audit=store.audit_families(emit)
            out["stages_s"]["one_time_repeat_full_corpus_audit"]=round(time.perf_counter()-st,6)
            if audit!=prior["family_records"]:
                raise StoreFailure("13-family full audit differs from original S3 report")
            watch.check()
            if mode=="native-repeat":
                out["measurement"]=_native_repeat(store,source,config,config_path,
                              prior,counts,fresh_samples,emit,watch)
            else:
                out["measurement"]=_distinct_physical(store,prior,counts,
                                                    physical_repeats,emit,watch)
            source.verified._live()
            watch.check()
        out["resources"]={"peak_process_tree_rss_bytes":watch.peak_rss,
                          "sampled_cpu_user_s":round(watch.peak_sampled_cpu_user_s,6),
                          "sampled_cpu_system_s":round(watch.peak_sampled_cpu_system_s,6),
                          "logical_cpus":watch.logical_cpus,
                          "samples":watch.sample_count,
                          "cpu_grade":"SAMPLED_PROCESS_TREE"}
        out["status"]="EXECUTED_TEST_ONLY" if mode=="native-repeat" else "EXECUTED_PHYSICAL_ONLY"
    except BaseException as exc:
        out.update(status="HELD_OR_FAILED",error_type=type(exc).__name__,error=str(exc),
                   traceback=traceback.format_exc(limit=12))
        emit(stage="failed",error_type=type(exc).__name__)
    finally:
        if store is not None:
            store.close()
        now_stat=db.stat()
        out["original_sqlite_stat_unchanged"]=(now_stat.st_size==orig_stat.st_size
                            and now_stat.st_mtime_ns==orig_stat.st_mtime_ns)
        out["original_report_unchanged"]=(report_path.read_bytes()==report_bytes)
        if not out["original_sqlite_stat_unchanged"] or not out["original_report_unchanged"]:
            out.update(status="HELD_OR_FAILED",error="original S3 SQLite/report changed during read-only court")
        out["completed_utc"]=datetime.now(timezone.utc).isoformat()
        (folder/"prepared_report.json").write_text(json.dumps(out,indent=2,default=str)+"\n")
        emit(stage="final",status=out["status"])
        emit.close()
    return out


def main(argv=None) -> int:
    p=argparse.ArgumentParser(description="S3 existing-store prepared Q103 / distinct physical benchmark")
    p.add_argument("--config",type=Path,required=True)
    p.add_argument("--existing-run",type=Path,required=True)
    p.add_argument("--mode",choices=("native-repeat","physical-distinct"),required=True)
    p.add_argument("--counts",type=parse_counts,default=(1,10,100))
    p.add_argument("--fresh-samples",type=int,default=3)
    p.add_argument("--physical-repeats",type=int,default=3)
    args=p.parse_args(argv)
    try:
        report=run(args.config,args.existing_run,mode=args.mode,counts=args.counts,
                   fresh_samples=args.fresh_samples,physical_repeats=args.physical_repeats)
        print(canonical({"status":report["status"],"report_dir":report["report_directory"]}))
        return 0 if report["status"].startswith("EXECUTED_") else 2
    except (StoreFailure,OSError,ValueError) as exc:
        print("S3_PREPARED_HOLD "+type(exc).__name__+": "+str(exc),file=__import__("sys").stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())
