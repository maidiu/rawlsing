"""Single-command, four-arm persistent C11 storage decision runner.

Runs no SAV/DTA ingestion. Original C11 estate and external authority pins
are REQUIRED for full tests; default failure is an explicit HOLD.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import sqlite3
import statistics
import subprocess
import sys
import threading
import time
import traceback
from typing import Any

from .stores import ARMS, FAMILIES, SCHEMA, Store, StoreFailure, canonical, digest, size_tree
from .native import execute_issued

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_SCHEMA = "PYAT_C11_FOUR_STORE_COMPARISON_REPORT@1"
MAX_RSS = 6 * 1024**3

def utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def load_file_module(path: Path, name: str):
    if not path.is_file():
        raise StoreFailure("required local authority/operations provider unavailable: " + str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise StoreFailure("invalid local provider module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def resolve(root: Path, value: str) -> Path:
    p = Path(value).expanduser()
    return p if p.is_absolute() else (root / p).resolve()

class EventLogger:
    def __init__(self, path: Path, arm: str):
        self.path = path
        self.arm = arm
        self._fh = path.open("w", encoding="utf-8")
        self.started = time.monotonic()
        self.lock = threading.Lock()
    def __call__(self, **kwargs):
        event = {"utc": utc(), "arm": self.arm,
                 "elapsed_s": round(time.monotonic()-self.started,3), **kwargs}
        with self.lock:
            self._fh.write(canonical(event)+"\n")
            self._fh.flush()
        # Emit machine-readable and human-readable live progress unbuffered.
        msg = ("[{arm}] {stage} {family} {completed} "
               "elapsed={elapsed_s}s").format(
                   arm=self.arm, stage=event.get("stage","event"),
                   family=event.get("family",""), completed=event.get("completed",""),
                   elapsed_s=event["elapsed_s"])
        print(msg, flush=True)
    def close(self):
        self._fh.close()

class Resources:
    """Measures process+child RSS and output directory disk every 0.5 seconds."""
    def __init__(self, target: Path, emit: EventLogger, ceiling: int = MAX_RSS):
        self.target, self.emit, self.ceiling = target, emit, ceiling
        self.peak_rss = 0
        self.peak_disk = 0
        self.sample_count = 0
        self.abort_reason = None
        self.peak_sampled_cpu_user_s = 0.0
        self.peak_sampled_cpu_system_s = 0.0
        self.peak_sampled_io_read_bytes = 0
        self.peak_sampled_io_write_bytes = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop,daemon=True)
        self._proc = None
    def __enter__(self):
        try:
            import psutil
            self._proc = psutil.Process(os.getpid())
        except ImportError as exc:
            raise StoreFailure("psutil required for verified process-tree resource accounting") from exc
        self._thread.start()
        return self
    def __exit__(self, *args):
        self._stop.set()
        self._thread.join(timeout=3)
    def _loop(self):
        while not self._stop.wait(0.5):
            try:
                procs = [self._proc]+self._proc.children(recursive=True)
                rss = sum(p.memory_info().rss for p in procs if p.is_running())
                self.peak_rss = max(self.peak_rss,rss)
                self.peak_disk = max(self.peak_disk,size_tree(self.target))
                self.sample_count += 1
                cpu_user,cpu_system,io_read,io_write = 0.,0.,0,0
                for process in procs:
                    try:
                        t=process.cpu_times()
                        cpu_user+=t.user
                        cpu_system+=t.system
                        io=process.io_counters()
                        io_read+=io.read_bytes
                        io_write+=io.write_bytes
                    except Exception:
                        continue
                self.peak_sampled_cpu_user_s=max(self.peak_sampled_cpu_user_s,cpu_user)
                self.peak_sampled_cpu_system_s=max(self.peak_sampled_cpu_system_s,cpu_system)
                self.peak_sampled_io_read_bytes=max(self.peak_sampled_io_read_bytes,io_read)
                self.peak_sampled_io_write_bytes=max(self.peak_sampled_io_write_bytes,io_write)
                if rss > self.ceiling:
                    self.abort_reason = "process-tree RSS crossed 6 GiB cap"
                if shutil.disk_usage(self.target).free < 2*1024**3:
                    self.abort_reason = "output filesystem has less than 2 GiB free"
                if self.sample_count % 20 == 0:
                    self.emit(stage="resources", rss_bytes=rss,
                              peak_rss_bytes=self.peak_rss,
                              peak_disk_bytes=self.peak_disk)
            except Exception as exc:
                self.abort_reason = "resource sampling failed: "+str(exc)
                break
    def check(self):
        if self.abort_reason:
            raise StoreFailure(self.abort_reason)

def _encode_record(h, ref: str, body: str) -> None:
    blob = ref.encode() + b"\x00" + body.encode()
    h.update(len(blob).to_bytes(8,"big"))
    h.update(blob)

class InputEstate:
    """Existing accepted ANVIL source gate; no replay/seal is self-issued."""
    def __init__(self, config: dict, bundle_root: Path, emit):
        from rawlsing_next.pre553_anvil_stream_native_i03 import (
            HeldStreamPins, VerifiedAnvilStreamEstate,
        )
        self.r2_custody = None
        if config.get("r2_decision_file"):
            # Original R2 user/source decision directly; no manually written
            # Python authority hook is needed for this narrower custody mode.
            from .existing_r2 import R2Custody
            self.r2_custody = R2Custody(
                resolve(bundle_root,config["r2_decision_file"]),
                config["source_id"],
                required_host=config["required_host"],
                required_purpose=config["required_purpose"],
            )
            self.held=self.r2_custody.pins
            self.estate_path=self.r2_custody.estate_path
            self.estate_root=self.r2_custody.estate_root
            self._provider=self.r2_custody
        else:
            self.estate_path = resolve(bundle_root,config["estate_path"])
            self.estate_root = resolve(bundle_root,config["estate_root"])
            pin_file = resolve(bundle_root,config["held_pins"])
            pins = json.loads(pin_file.read_text())
            self.held = HeldStreamPins(
                source_id=pins["source_id"], source_sha256=pins["source_sha256"],
                manifest_sha256=pins["manifest_sha256"],
                exact_release_path=pins["exact_release_path"],
                roots=pins["roots"],
            )
            auth_path = resolve(bundle_root,config["authority_provider"])
            self._provider = load_file_module(
                auth_path,"pyat_bench_external_current_provider")
            if not callable(getattr(self._provider,"check_current",None)):
                raise StoreFailure("independent authority provider must export check_current(held_pins)")
        if self._provider.check_current(self.held) is not True:
            raise StoreFailure("CURRENT/source authority refused before estate admission")
        emit(stage="source_admission", completed="begin")
        self.verified = VerifiedAnvilStreamEstate(
            root=self.estate_root, exact_path=self.estate_path,
            independently_held=self.held,
            current_authorizer=self._provider.check_current,
        )
        self.manifest = json.loads((self.estate_path / "manifest.json").read_text())
        self.identity = {
            "schema": self.manifest["schema"],
            "manifest_sha256": self.held.manifest_sha256,
            "roots": dict(self.held.roots),
            "source_id": self.held.source_id,
        }
        self.source_bytes = sum((self.estate_path / n).stat().st_size
                              for n in self.manifest["members"])
        emit(stage="source_admission", completed="accepted_source_scoped", 
             source_bytes=self.source_bytes,
             events=self.manifest["family_counts"]["RespondentEvent"])

    def _native_body_check(self, row: dict, family: str):
        from rawlsing_next.pre553_parquet_carrier import _object_from_row
        from rawlsing_next.pre553_source_direct_parquet_estate import _row
        from rawlsing_next._pre553_direct_i02_sourcefree import _FAMILIES
        obj = _object_from_row(json.loads(row["body_json"]))
        if type(obj) is not _FAMILIES[family] or obj.ref.key != row["ref"]:
            raise StoreFailure("source family/body/ref mismatch: "+family)
        expected = _row(family,obj)
        for field, value in expected.items():
            actual = row[field]
            if field == "raw_float64" and isinstance(value,float):
                import math, struct
                if math.isnan(value):
                    if not isinstance(actual,float) or not math.isnan(actual):
                        raise StoreFailure("native R5 physical NaN state mismatch")
                    continue
                if not isinstance(actual,float) or struct.pack(">d",actual)!=struct.pack(">d",value):
                    raise StoreFailure("source raw float64 bit drift")
            elif actual != value:
                raise StoreFailure("original body and typed projection differ: "+field)
        return obj

    def feed(self, store: Store, progress, resources: Resources, *, batch_commit: int = 2048):
        import pyarrow.parquet as pq
        records = {}
        for family in FAMILIES:
            self.verified._live()
            path = self.estate_path / (family + ".parquet")
            count = 0
            h = hashlib.sha256()
            with pq.ParquetFile(path) as source:
                locator = (pq.ParquetFile(self.estate_path / "event_locator.parquet")
                           if family == "RespondentEvent" else None)
                try:
                    for gid in range(source.num_row_groups):
                        self.verified._live()
                        # Materialize only the physical writer's bounded row group.
                        batch = source.read_row_group(gid).to_pylist()
                        loc = locator.read_row_group(gid).to_pylist() if locator else None
                        if loc is not None and len(loc) != len(batch):
                            raise StoreFailure("event locator hides physical rows")
                        for off,row in enumerate(batch):
                            if loc is not None:
                                posting = loc[off]
                                if (posting["group"]!=gid or posting["offset"]!=off
                                    or any(posting[k]!=row[k if k!="state" else "typed_state"]
                                           for k in ("ref","respondent","native","canonical","component","state"))):
                                    raise StoreFailure("source body/locator mismatch")
                            obj = self._native_body_check(row,family)
                            routing = None
                            binding = None
                            if family=="QuestionVariableBinding":
                                from rawlsing_next.pre553_empirical_objects import exact_ref
                                def maybe_exact(value):
                                    try:
                                        return exact_ref(value).key
                                    except Exception:
                                        return None
                                binding=(exact_ref(obj.native_question_ref).key,
                                         maybe_exact(obj.canonical_question_ref_or_typed_absence),
                                         maybe_exact(obj.component_subitem_ref_or_typed_absence))
                            if family=="RoutingEligibilityFact":
                                from rawlsing_next.pre553_empirical_objects import exact_ref
                                routing=(exact_ref(obj.question_or_target_ref).key,
                                         exact_ref(obj.risk_set_ref).key)
                            store.add_row(family,count,row,gid,off,routing=routing,binding=binding)
                            _encode_record(h,row["ref"],row["body_json"])
                            count += 1
                            if count % batch_commit == 0:
                                store.commit_batch()
                            if count % 10000 == 0:
                                resources.check()
                                progress(stage="build",family=family,completed=count,
                                         declared=self.manifest["family_counts"][family])
                        resources.check()
                finally:
                    if locator:
                        locator.close()
            store.commit_batch()
            if count != self.manifest["family_counts"][family]:
                raise StoreFailure("source-derived declared family count failure: "+family)
            records[family]={"count":count,"digest":h.hexdigest()}
            progress(stage="family_complete",family=family,completed=count)
        return records

def _native_operations(config: dict, root: Path, source: InputEstate, emit):
    pathname = config.get("operations_provider")
    recorded = config.get("q103_recorded_operation_file")
    if pathname and recorded:
        raise StoreFailure("select original issued operation provider OR R2 Q103, not both")
    if recorded:
        if source.r2_custody is None:
            raise StoreFailure("R2 Q103 direct operation requires same held R2 custody")
        from .existing_r2 import read_recorded_operation
        emit(stage="issued_operations",completed="reconstruct_original_q103_once")
        use_file=config.get("q103_universe_use_decision_file")
        supplied=[read_recorded_operation(
            source.verified,custody=source.r2_custody,
            operation_file=resolve(root,recorded),
            universe_use_file=resolve(root,use_file) if use_file else None,
        )]
    elif pathname:
        mod=load_file_module(resolve(root,pathname),"pyat_bench_existing_issued_operations")
        fn=getattr(mod,"provide_operations",None)
        if not callable(fn):
            raise StoreFailure("operations provider must export provide_operations(verified_estate)")
        emit(stage="issued_operations",completed="building_once_from_existing_source_authority")
        supplied=list(fn(source.verified))
    else:
        emit(stage="issued_operations", status="HELD_NO_ORIGINAL_ISSUER")
        return [],"HELD_NO_ORIGINAL_ISSUER"
    names=[]
    for op in supplied:
        if not isinstance(op,dict) or not all(k in op for k in ("query","predicate","authority_registry")):
            raise StoreFailure("issued operation provider lacks original exact query/predicate/authority")
        names.append(op.get("name",op["query"].ref.key))
    if len(names)!=len(set(names)):
        raise StoreFailure("repeated operation identity cannot count as distinct issued queries")
    emit(stage="issued_operations",completed=len(supplied))
    return supplied,"ORIGINAL_ISSUED_OPERATION_OBJECTS_PROVIDED_BY_EXTERNAL_OWNER"

def _engine_report(store: Store, source: InputEstate, issued: list, emit, resources, config):
    report = {"physical_probes":[],"native":[],"native_status":None,"evidence_recovery":[]}
    refs=store.get_question_refs(min(100,int(config.get("physical_question_limit",100))))
    for n,ref in enumerate(refs):
        t=time.perf_counter()
        result=store.probe_query(ref)
        report["physical_probes"].append(result)
        store.store_result("physical:"+hashlib.sha256(ref.encode()).hexdigest(),
                           {"ref":ref,"grade":"PHYSICAL_OBSERVATION_ONLY"},
                           "PHYSICAL_ONLY",result,(time.perf_counter()-t)*1000)
        if (n+1) % 10==0 or n+1==len(refs):
            resources.check()
            emit(stage="physical_questions",completed=n+1,declared=len(refs))
    report["physical_joint"]=store.joint_probe(refs)
    report["steady_state_matrix"]=[]
    for size in (1,10,100):
        if len(refs)<size:
            report["steady_state_matrix"].append({
                "distinct_requested":size,"status":"INSUFFICIENT_PHYSICAL_QUESTIONS",
                "actual":len(refs)})
            continue
        durations=[]
        start=time.perf_counter()
        for target in refs[:size]:
            st=time.perf_counter()
            store.probe_query(target)
            durations.append((time.perf_counter()-st)*1000)
        report["steady_state_matrix"].append({
            "distinct_requested":size,
            "status":"PHYSICAL_ONLY_NO_SCIENTIFIC_ISSUANCE",
            "total_ms":round((time.perf_counter()-start)*1000,3),
            "median_ms":round(statistics.median(durations),3),
            "max_ms":round(max(durations),3),
            "p95_ms":round(sorted(durations)[max(0,int(0.95*(len(durations)-1)))],3)})
        resources.check()
        emit(stage="steady_state_distinct",completed=size)
    report["fresh_process_probes"]=[]
    cold_limit=min(len(refs),int(config.get("cold_reopen_limit",10)))
    source_idfile=Path(config["_held_identity_path"])
    sample_refs=config.get("evidence_reference_sample",[])
    if cold_limit and sample_refs:
        for j,target in enumerate(refs[:cold_limit]):
            # SQL-only child gets deliberately absent Parquet source directory.
            estate=(store.estate_path if store.name=="H"
                    else store.path.parent/"NO_PARQUET_DEPENDENCY_ALLOWED")
            cmd=[sys.executable,"-m","tools.pyat_c11_four_store.cold_worker",
                 "--arm",store.name,"--database",str(store.path),
                 "--estate",str(estate),"--source-identity",str(source_idfile),
                 "--target",target,"--evidence-ref",sample_refs[0]]
            st=time.perf_counter()
            p=subprocess.run(cmd,capture_output=True,text=True,
                             timeout=int(config.get("cold_worker_timeout_seconds",600)))
            if p.returncode:
                raise StoreFailure("cold process refused arm "+store.name+
                                   " code "+str(p.returncode)+" "+p.stderr[-1500:])
            observation=json.loads(p.stdout.strip())
            if observation["query"]["target_ref"]!=target:
                raise StoreFailure("cold worker changed exact question")
            report["fresh_process_probes"].append(observation)
            emit(stage="cold_new_process",completed=j+1,declared=cold_limit,
                 duration_ms=round((time.perf_counter()-st)*1000,3))
            resources.check()
    # Full-body recovery from SAME exact ref set for every arm.
    selected=config.get("evidence_reference_sample",[])
    for n in (1,100,3000,100000):
        requested=selected[:n]
        if not requested:
            continue
        h=hashlib.sha256()
        t=time.perf_counter()
        found=0
        for ref in requested:
            oid=store.find_id(ref)
            if oid is None:
                raise StoreFailure("missing exact evidence reference in one arm")
            retrieved,body=store.fetch_body(oid)
            if retrieved!=ref:
                raise StoreFailure("external evidence identity substitution")
            _encode_record(h,retrieved,body)
            found+=1
        report["evidence_recovery"].append(
            {"requested":min(n,len(selected)),"found":found,
             "digest":h.hexdigest(),"elapsed_s":round(time.perf_counter()-t,4)}
        )
        emit(stage="evidence",completed=found)
    if not issued:
        report["native_status"]="HELD_NO_ORIGINAL_ISSUER"
    else:
        report["native_status"]="TEST_ONLY_SAVED_READ_ADAPTER_USING_EXISTING_I03"
        for i,op in enumerate(issued):
            resources.check()
            name=op.get("name",op["query"].ref.key)
            t=time.perf_counter()
            try:
                val=execute_issued(store,source.verified,op)
            except Exception:
                # Never convert a native validation error into a positive
                # scientific fact or silently label it source unavailable.
                emit(stage="native_refused",completed=i,name=str(name))
                raise
            dt=(time.perf_counter()-t)*1000
            report["native"].append({"name":str(name),"output":val,"elapsed_ms":round(dt,3)})
            store.store_result("native:"+hashlib.sha256(str(name).encode()).hexdigest(),
                               {"name":str(name),"query_ref":op["query"].ref.key},
                               "NATIVE_TESTONLY",val,dt)
            emit(stage="native",completed=i+1,declared=len(issued),
                 duration_ms=round(dt,3))
    report["physics_hash"]=digest(canonical(
        [(q["target_ref"],q["digest"],q["events"],q["respondents"]) for q in report["physical_probes"]]
    ).encode())
    report["native_hash"]=digest(canonical(
        [(op["name"],op["output"]) for op in report["native"]]
    ).encode()) if report["native"] else None
    return report

def _sample_evidence(estate: Path, n: int, emit):
    import pyarrow.parquet as pq
    refs=[]
    with pq.ParquetFile(estate/"RespondentEvent.parquet") as source:
        for gid in range(source.num_row_groups):
            rows=source.read_row_group(gid,columns=["ref"])["ref"].to_pylist()
            refs.extend(rows[:max(0,n-len(refs))])
            if len(refs)>=n:
                break
    emit(stage="common_evidence_refs",completed=len(refs))
    return refs

def _preflight_disk(source: InputEstate, output: Path, config: dict):
    free=shutil.disk_usage(output).free
    # Conservatively reserve enough for multiple full TEXT/keyed stores and
    # WAL/scratch.  Never guess physical full-SQLite size from sampled index.
    required=max(int(config.get("minimum_free_gib",12))*1024**3,source.source_bytes*5)
    if free<required:
        raise StoreFailure(
            "insufficient free disk for safe 4-arm build: free="+str(free)+
            " required="+str(required)+
            "; choose an external scratch/output drive; source remains untouched")

def _host_details():
    d={"os":platform.platform(),"python":sys.version,"sqlite":sqlite3.sqlite_version,
       "processor":platform.processor(),"machine":platform.machine(),"utc":utc()}
    try:
        import pyarrow
        d["pyarrow"]=pyarrow.__version__
    except ImportError:
        d["pyarrow"]="MISSING"
    return d

def run(config_path: Path, *, only: str | None = None) -> dict:
    root=config_path.resolve().parent
    config=json.loads(config_path.read_text())
    if config.get("schema") != "PYAT_FOUR_PERMANENT_STORE_BUNDLE@1":
        raise StoreFailure("wrong bundle/config contract")
    output=resolve(root,os.environ.get("PYAT_BENCH_OUTPUT_DIR",config["output_dir"]))
    output.mkdir(parents=True,exist_ok=True)
    run_tag=config.get("run_id") or datetime.now().strftime("%Y%m%dT%H%M%S")
    run_dir=output/run_tag
    run_dir.mkdir(parents=False,exist_ok=False)
    common=EventLogger(run_dir/"progress.jsonl","COMMON")
    result={"schema":BENCHMARK_SCHEMA,"status":"RUNNING","started":utc(),
            "config_sha256":digest(config_path.read_bytes()),
            "host":_host_details(),"arms":{},"comparison":None}
    try:
        with Resources(run_dir,common) as common_r:
            t=time.perf_counter()
            source=InputEstate(config,root,common)
            result["source_admission_s"]=round(time.perf_counter()-t,3)
            _preflight_disk(source,run_dir,config)
            issued,issuer_grade=_native_operations(config,root,source,common)
            result["original_operation_provider_grade"]=issuer_grade
            result["original_issued_operations"]=len(issued)
            config["evidence_reference_sample"]=_sample_evidence(
                source.estate_path,int(config.get("evidence_sample_limit",100000)),common)
            result["source_identity"]=source.identity
            result["source_retained_bytes"]=source.source_bytes
            identity_file=run_dir/"held_source_identity.json"
            identity_file.write_text(canonical(source.identity)+"\n")
            config["_held_identity_path"]=str(identity_file)
            common_r.check()
        for arm in (ARMS if only is None else (only,)):
            folder=run_dir/arm
            folder.mkdir()
            emit=EventLogger(folder/"progress.jsonl",arm)
            report={"arm":arm,"status":"RUNNING","started":utc(),
                    "source_identity":source.identity,"host":result["host"],
                    "stages_s":{}, "metrics":{}}
            s=None
            try:
                with Resources(folder,emit) as watch:
                    t=time.perf_counter()
                    s=Store(arm,folder/"permanent.sqlite",source.estate_path,
                            create=True,source_identity=source.identity,progress=emit)
                    records=source.feed(s,emit,watch,
                                        batch_commit=int(config.get("batch_commit",2048)))
                    report["stages_s"]["build_from_already_saved_c11"]=round(time.perf_counter()-t,3)
                    t=time.perf_counter()
                    s.finish(source.manifest,records)
                    report["stages_s"]["publish_commit"]=round(time.perf_counter()-t,3)
                    t=time.perf_counter()
                    audited=s.audit_families(emit)
                    report["stages_s"]["full_corpus_body_audit"]=round(time.perf_counter()-t,3)
                    report["family_records"]=audited
                    s.close();s=None
                    t=time.perf_counter()
                    s=Store(arm,folder/"permanent.sqlite",source.estate_path,
                            create=False,source_identity=source.identity,progress=emit)
                    report["stages_s"]["fresh_connection_open"]=round(time.perf_counter()-t,4)
                    t=time.perf_counter()
                    report["query_report"]=_engine_report(s,source,issued,emit,watch,config)
                    report["stages_s"]["queries_and_persisted_results"]=round(time.perf_counter()-t,3)
                    report["metrics"]=s.stats()
                    report["metrics"]["required_permanent_bytes"] = (
                        source.source_bytes + size_tree(folder) if arm=="H" else size_tree(folder))
                    report["metrics"]["source_parquet_required_for_queries"]=arm=="H"
                    watch.check()
                report["resources"]={"peak_process_tree_rss_bytes":watch.peak_rss,
                                     "peak_output_disk_bytes":watch.peak_disk,
                                     "sampled_cpu_user_s":watch.peak_sampled_cpu_user_s,
                                     "sampled_cpu_system_s":watch.peak_sampled_cpu_system_s,
                                     "sampled_io_read_bytes":watch.peak_sampled_io_read_bytes,
                                     "sampled_io_write_bytes":watch.peak_sampled_io_write_bytes,
                                     "samples":watch.sample_count}
                report["status"]="COMPLETED_PHYSICAL_AND_NATIVE_WHERE_ISSUED"
                report["completed"]=utc()
                emit(stage="arm_complete",completed=arm)
            except BaseException as exc:
                report["status"]="FAILED_OR_HELD"
                report["error_type"]=type(exc).__name__
                report["error"]=str(exc)
                report["traceback"]=traceback.format_exc(limit=12)
                emit(stage="arm_failed",error=report["error"])
                # Capture failure and proceed to next arm only if configured,
                # never claim comparative parity on an incomplete candidate.
                if not config.get("continue_after_arm_failure",True):
                    raise
            finally:
                if s is not None:
                    s.close()
                (folder/"report.json").write_text(json.dumps(report,indent=2,default=str)+"\n")
                emit.close()
                result["arms"][arm]=report
                (run_dir/"comparison.json").write_text(json.dumps(result,indent=2,default=str)+"\n")
        completed={x:a for x,a in result["arms"].items()
                   if a["status"]=="COMPLETED_PHYSICAL_AND_NATIVE_WHERE_ISSUED"}
        if len(completed)==4:
            fs=[a["family_records"] for a in completed.values()]
            probes=[a["query_report"]["physics_hash"] for a in completed.values()]
            native=[a["query_report"]["native_hash"] for a in completed.values()]
            source_parity=len({canonical(x) for x in fs})==1
            physical_parity=len(set(probes))==1
            native_parity=(all(x is not None for x in native)
                           and len(set(native))==1)
            result["comparison"]={
                "source_family_body_parity":source_parity,
                "physical_query_parity":physical_parity,
                "native_i03_fact_parity":native_parity if issued else "HELD_NO_ORIGINAL_ISSUER",
                "scientific_issued_operations":len(issued),
                "automatic_canonical_selection":"NOT_AUTHORIZED_BY_TESTONLY_PHYSICAL_ADAPTER",
                "four_arm_complete":True,
            }
            if not source_parity or not physical_parity or (issued and not native_parity):
                result["status"]="SEMANTIC_PARITY_FAILURE"
            else:
                result["status"]=("SOURCE_STATIC_TEST_COMPLETE__NATIVE_TESTONLY" if issued
                                  else "PHYSICAL_COMPLETE__ORIGINAL_ISSUER_HOLD")
        else:
            result["status"]="INCOMPLETE_ARMS_NO_WINNER"
        from .economics import measured_economics
        result["measured_economics"]=measured_economics(
            result["arms"],source_bytes=result.get("source_retained_bytes",0),
        )
        if completed:
            with (run_dir/"summary.csv").open("w",newline="") as f:
                writer=csv.writer(f)
                writer.writerow(["arm","status","required_permanent_bytes",
                                 "build_s","full_audit_s","query_s","peak_rss_bytes",
                                 "native_issued"])
                for name,a in result["arms"].items():
                    st=a.get("stages_s",{});m=a.get("metrics",{})
                    writer.writerow([
                        name,a["status"],m.get("required_permanent_bytes"),
                        st.get("build_from_already_saved_c11"),
                        st.get("full_corpus_body_audit"),
                        st.get("queries_and_persisted_results"),
                        a.get("resources",{}).get("peak_process_tree_rss_bytes"),
                        len(a.get("query_report",{}).get("native",[]))
                    ])
        result["completed"]=utc()
        return result
    except BaseException as exc:
        result["status"]="SOURCE_AUTHORITY_RESOURCE_OR_RUNNER_HOLD"
        result["failure"]={
            "type":type(exc).__name__,
            "message":str(exc),
            "traceback":traceback.format_exc(limit=14),
        }
        result["completed"]=utc()
        common(stage="run_failed_or_held",status=result["status"],
               failure_type=type(exc).__name__)
        raise
    finally:
        (run_dir/"comparison.json").write_text(json.dumps(result,indent=2,default=str)+"\n")
        common(stage="run_final",status=result["status"])
        common.close()

def main(argv=None):
    p=argparse.ArgumentParser(description="Four permanent C11 stores, one command and separate reports")
    p.add_argument("--config",type=Path,default=Path("bundle.json"))
    p.add_argument("--only",choices=ARMS)
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args(argv)
    if args.self_test:
        import unittest
        from . import test_stores
        suite=unittest.defaultTestLoader.loadTestsFromModule(test_stores)
        ret=unittest.TextTestRunner(verbosity=2).run(suite)
        return 0 if ret.wasSuccessful() else 1
    try:
        r=run(args.config,only=args.only)
        print(canonical({"result":r["status"],
                         "report_dir":str(resolve(args.config.resolve().parent,
                                json.loads(args.config.read_text())["output_dir"]))}),flush=True)
        return 0 if r["status"] in (
            "SOURCE_STATIC_TEST_COMPLETE__NATIVE_TESTONLY",
            "PHYSICAL_COMPLETE__ORIGINAL_ISSUER_HOLD") else 2
    except Exception as exc:
        print("BENCHMARK_HOLD_OR_FAILURE "+type(exc).__name__+" "+str(exc),
              file=sys.stderr,flush=True)
        traceback.print_exc()
        return 2

if __name__=="__main__":
    raise SystemExit(main())
