"""Fresh-interpreter sourcefree country preparation court, actual U43/Batch.
Retain the external producer pin separately; no inherited live objects/pickle.
The existing campaign resource sampler supervises each process tree.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict,replace
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from statistics import median
from unittest.mock import patch
from tools.pyat_country_campaign_court import sample_tree,disk_snapshot,kill_tree,LIMIT

def write(path,value):
    path.write_text(json.dumps(value,sort_keys=True),encoding="utf-8")

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def geometry(rows,width,governed):
    import numpy as np
    if rows<32 or governed<80 or width<governed+2:
        raise ValueError("invalid geometry")
    values=np.random.default_rng(931).integers(0,2,(2*rows,governed))
    for offset in (0,1):
        ids=np.arange(offset,2*rows,2)
        values[ids,0]=np.arange(rows)%2
        values[ids,1]=(np.arange(rows)//2)%2
        values[ids,2]=values[ids,0]^values[ids,1]^offset
        values[ids,3]=0
        values[ids[6],3]=1
    return values

def setup(root,rows,width,governed):
    import numpy as np
    import pandas as pd
    import pyreadstat
    from rawlsing_next.pre553_physical_decoder import decode_sav
    from rawlsing_next.pre553_country_numeric_carrier import build_country
    values=geometry(rows,width,governed);n=len(values)
    data={"q"+str(i):values[:,i].astype(str) for i in range(governed)}
    for i in range(width-governed-2):
        data["v"+str(i)]=(np.arange(n,dtype=np.float64)*(1.000001+i*.00001)+i*.001
                         if i%2 else (np.arange(n)+i)%7)
    data["G"]=np.where(np.arange(n)%2==0,"A","B")
    data["W"]=1.+(np.arange(n)%3)
    source=root/"generated.sav"
    t=time.monotonic();pyreadstat.write_sav(pd.DataFrame(data),str(source))
    source_bytes=source.stat().st_size
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    with decode_sav(source,expected_source_sha256=sha) as inc:
        ordinals={v.name:v.ordinal for v in inc.variables}
        receipt=build_country(inc,country_variable="G",country_value="A",
             output=root/"country.sqlite",require_current=lambda:True,block_rows=256)
    source.unlink()
    write(root/"fixture.json",{"receipt":asdict(receipt),"ordinals":ordinals,
         "rows":rows,"width":width,"governed":governed,"source_bytes":source_bytes,
         "build_seconds":time.monotonic()-t})

def worker(root,mode,counts,report):
    from rawlsing_next.tests.test_pre553_country_numeric_economics import CountryNativeEconomics
    from rawlsing_next.tests.test_pre553_empirical_query import _ref
    from rawlsing_next import pre553_country_numeric_carrier as carrier
    from rawlsing_next import pre553_source_backed_c11_facade as facade
    from rawlsing_next import pre553_issued_workload as issued
    from rawlsing_next.pre553_empirical_objects import semantic_hash
    from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
    cfg=read(root/"fixture.json")
    receipt=carrier.CountryReceipt(**cfg["receipt"])
    rows,width,governed=cfg["rows"],cfg["width"],cfg["governed"]
    values=geometry(rows,width,governed)
    db=root/"country.sqlite";prepared=root/"validated-headers.gz"
    t=time.monotonic()
    ext=dict(root=root,db=db,receipt=receipt,ordinals=cfg["ordinals"],
             selected=values[::2,:],chosen=tuple(range(1,2*rows+1,2)),
             country="A",governed=governed,physical_width=width)
    workload,record,queries,host,purpose,_=CountryNativeEconomics()._native_batch(
        wide=True,external_case=ext)
    del values,ext
    issuance_seconds=time.monotonic()-t
    cases=[]
    for count in counts:
        requests=workload.requests[:count]
        discoveries=workload.discoveries if count==100 else ()
        jobs=issued.operation_jobs(requests,discoveries)
        decision=_ref("TEST_ONLY_DECISION","r14-"+str(count))
        u=semantic_hash({"r14":count,"source":receipt.source_sha256})
        frontier=semantic_hash({"jobs":jobs,"root":u})
        item=replace(workload,decision_ref=decision,requests=requests,discoveries=discoveries,
                     original_u_root=u,expected_frontier_root=frontier)
        grant=replace(record,decision_ref=decision,expected_jobs=jobs,
                      original_u_root=u,expected_frontier_root=frontier,
                      envelope_sha256=issued._stream_workload_digest(item))
        cases.append((item,TestOnlyDecisionResolver(grant),grant))
    kwargs=dict(require_current=lambda:True)
    if mode in ("save","restore","negative","compare"):
        kwargs["preparation_path"]=prepared
    if mode in ("restore","negative","compare"):
        kwargs["preparation_pin"]=carrier.CountryPreparationPin(**read(root/"external-producer-pin.json"))
    if mode=="negative":
        from rawlsing_next.pre553_issued_workload import WorkloadAdmissionError
        item,resolver,grant=cases[0]
        def refuses(options,exception=carrier.CountryCarrierError):
            try:
                with carrier.CountryWorkloadSession(db,receipt,**options) as session:
                    session.execute(item,resolver,host=host,purpose=purpose)
            except exception:
                return
            raise AssertionError("invalid preparation was served")
        refuses(dict(require_current=lambda:True,preparation_path=prepared))
        pin=kwargs["preparation_pin"]
        refuses(dict(kwargs,preparation_pin=replace(pin,artifact_sha256="0"*64)))
        refuses(dict(kwargs,preparation_pin=replace(pin,facade_key="wrong")))
        refuses(dict(kwargs,preparation_pin=replace(pin,release_identity="wrong")))
        with prepared.open("r+b") as file:
            byte=file.read(1);file.seek(0);file.write(bytes([byte[0]^1]))
        try:refuses(kwargs)
        finally:
            with prepared.open("r+b") as file:file.write(byte)
        resolver._record=replace(grant,currentness="REVOKED")
        try:
            with patch.object(facade,"_validate_country_produced_release",
                              side_effect=AssertionError("revoked preparation entered I02")):
                refuses(kwargs,WorkloadAdmissionError)
        finally:resolver._record=grant
        with db.open("r+b") as file:
            file.seek(-1,2);byte=file.read(1);file.seek(-1,2);file.write(bytes([byte[0]^1]))
        try:refuses(kwargs)
        finally:
            with db.open("r+b") as file:file.seek(-1,2);file.write(byte)
        # A new sidecar may be produced before a later execution failure,
        # but no external successful producer pin may escape that call.
        from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
        failed=carrier.CountryWorkloadSession(db,receipt,require_current=lambda:True,
                    preparation_path=root/"failed-headers.gz")
        try:
            with failed,patch.object(CarrierNeutralResearchExecutor,"execute_i03",
                            side_effect=RuntimeError("post-preparation intentional failure")):
                failed.execute(item,resolver,host=host,purpose=purpose)
        except RuntimeError as exc:
            assert str(exc)=="post-preparation intentional failure",str(exc)
        else:raise AssertionError("intentional failure not reached")
        assert (root/"failed-headers.gz").is_file()
        assert failed.preparation_pin is None
        (root/"failed-headers.gz").unlink()
        write(report,{"mode":mode,"negative_controls":8})
        return
    from contextlib import ExitStack
    from rawlsing_next import pre553_c11_ingest as ingest
    from rawlsing_next import pre553_c11_integrity as integrity
    from rawlsing_next import _pre553_country_preparation as preparation
    phases={}; occurrence_comparison=None
    def instrument(owner,name,label):
        fn=getattr(owner,name)
        def timed(*args,**kw):
            t=time.monotonic()
            try:return fn(*args,**kw)
            finally:
                entry=phases.setdefault(label,{"calls":0,"wall_s":0.0})
                entry["calls"]+=1
                entry["wall_s"]+=time.monotonic()-t
        return patch.object(owner,name,timed)
    occurrence=ingest.ensure_distinct_event_occurrences
    def compared(events):
        nonlocal occurrence_comparison
        # Measure on actual authenticated restored headers, separate from the
        # primary preparation timing; the paired witness is optional.
        if mode=="compare":
            times={"incumbent":[],"direct":[]}
            for order in (("incumbent","direct"),("direct","incumbent")):
                for kind in order:
                    t=time.monotonic()
                    if kind=="incumbent":
                        with patch.object(integrity,"_country_occurrence_ids_distinct",lambda _:False):
                            occurrence(events)
                    else:occurrence(events)
                    times[kind].append(time.monotonic()-t)
            occurrence_comparison={"events":len(events),"seconds":times,
                "median_seconds":{k:median(v) for k,v in times.items()},
                "both_accepted":True}
        return occurrence(events)
    calls=[]; original=facade._build_source_backed_c11_repository
    def counted(*args,**kw):
        start=time.monotonic()
        count=0; original_event=facade._event
        def event(*args,**kw):
            nonlocal count
            count+=1
            return original_event(*args,**kw)
        # Do not retain every event's call args in a Mock at survey scale.
        with ExitStack() as stack:
            stack.enter_context(patch.object(facade,"_event",event))
            for owner,name,label in (
                (ingest,"_validate_authorities","authorities"),
                (ingest,"_validate_universe_and_respondent_scope","namespace"),
                (ingest,"_validate_questions_and_events","question_occurrence"),
                (ingest,"_validate_replay","replay_validation"),
                (ingest,"_candidate_projection_semantic_hash","projection_hash"),
                (ingest,"_all_nonmanifest_refs","closure_refs"),
                (facade,"source_backed_facade_key","facade_key"),
                (facade,"project_c11_candidate_from_physical_cells","candidate_projection"),
                (preparation,"_decode_headers","header_decode"),
                (preparation,"_encode_headers","header_encode"),
                (carrier._CountryPhysicalStream,"compact_events","compact_view")):
                stack.enter_context(instrument(owner,name,label))
            stack.enter_context(patch.object(ingest,"ensure_distinct_event_occurrences",compared))
            result=original(*args,**kw)
        calls.append({"wall_s":time.monotonic()-start,"response_event_constructions":count})
        return result
    result_rows=[]
    with patch.object(facade,"_build_source_backed_c11_repository",counted):
        with carrier.CountryWorkloadSession(db,receipt,**kwargs) as session:
            for item,resolver,grant in cases:
                start=time.monotonic()
                execution=session.execute(item,resolver,host=host,purpose=purpose)
                elapsed=time.monotonic()-start
                proof=execution.result.exact_s2e_output_census(runtime_catalog=item.catalog)
                result_rows.append({"units":proof.completed_count,"wall_s":elapsed,
                    "census":proof.as_dict(),"release":execution.release_identity.as_dict()})
            pin=session.preparation_pin
    assert len(calls)==1,calls
    assert calls[0]["response_event_constructions"]==(0 if mode in ("restore","compare") else rows*governed),calls
    if mode=="save":
        write(root/"external-producer-pin.json",asdict(pin))
    write(report,{"mode":mode,"pid":os.getpid(),"issuance_seconds":issuance_seconds,
                  "preparation":calls[0],"investigations":result_rows,
                  "inclusive_preparation_phases":phases,"occurrence_comparison":occurrence_comparison})

def supervise(root,command):
    start=time.monotonic();peak={};samples=0
    env=dict(os.environ,TMPDIR=str(root/"tmp"),PYTHONUNBUFFERED="1")
    proc=subprocess.Popen([sys.executable,"-m","tools.pyat_country_preparation_court",
                           *command],env=env,start_new_session=True)
    try:
        while True:
            rss,n=sample_tree(proc.pid)
            sample={"aggregate_worker_tree_rss_bytes":rss,"live_processes":n,**disk_snapshot(root)}
            for key,value in sample.items():peak[key]=max(peak.get(key,0),value)
            samples+=1
            if rss>LIMIT:
                kill_tree(proc)
                raise RuntimeError("6 GiB sampled worker-tree limit exceeded")
            if proc.poll() is not None:break
            time.sleep(.1)
    finally:
        if proc.poll() is None:kill_tree(proc)
        proc.wait()
    if proc.returncode:raise RuntimeError("worker failed: "+str(command))
    return {"outer_wall_s":time.monotonic()-start,"sampled_peak":peak,"samples":samples}

def court(root,rows,width,governed,counts):
    if any(root.iterdir()):raise ValueError("empty private root required")
    (root/"tmp").mkdir()
    source=supervise(root,["--root",str(root),"--setup","--rows",str(rows),
                           "--width",str(width),"--governed",str(governed)])
    reports=[]
    for i,mode in enumerate(("save","cold","restore","restore","cold","compare","negative")):
        dest=root/("report-"+str(i)+".json")
        resource=supervise(root,["--root",str(root),"--worker",mode,
                   "--units",",".join(map(str,counts)),"--report",str(dest)])
        report=read(dest);report["resources"]=resource;reports.append(report)
    def evidence(report):
        return [(item["units"],item["census"],item["release"]) for item in report["investigations"]]
    reference=evidence(reports[0])
    assert all(evidence(report)==reference for report in reports[:-1])
    assert len({report["pid"] for report in reports[:-1]})==6
    pin=read(root/"external-producer-pin.json")
    timing={mode:[r["preparation"]["wall_s"] for r in reports if r["mode"]==mode]
            for mode in ("save","cold","restore")}
    print("R14_FRESH_PROCESS_PREPARATION",json.dumps({
        "geometry":read(root/"fixture.json"),"source_resources":source,
        "sidecar_bytes":pin["artifact_bytes"],"preparation_times":timing,
        "median_preparation_s":{k:median(v) for k,v in timing.items()},
        "exact_census_and_release_parity":True,"fresh_processes":6,
        "negative_controls":reports[-1]["negative_controls"],
        "workers":[{**r,"investigations":[{k:v for k,v in i.items() if k!="census"}
                for i in r.get("investigations",[])]} for r in reports],
        "retained_disk":disk_snapshot(root),
        "grade":"SOURCEFREE_PERSISTED_EVENT_HEADERS__REMAINING_I02_REBUILT__NOT_ORIGINAL_OR_WVS7"
    },sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--rows",type=int,default=128)
    p.add_argument("--width",type=int,default=300)
    p.add_argument("--governed",type=int,default=80)
    p.add_argument("--units",default="1,10,100")
    p.add_argument("--root",type=Path)
    p.add_argument("--setup",action="store_true")
    p.add_argument("--worker",choices=["save","cold","restore","negative","compare"])
    p.add_argument("--report",type=Path)
    args=p.parse_args()
    counts=tuple(int(x) for x in args.units.split(","))
    if not counts or any(not 1<=x<=100 for x in counts) or len(set(counts))!=len(counts):
        p.error("distinct counts in [1,100] required")
    if args.setup:
        setup(args.root,args.rows,args.width,args.governed)
    elif args.worker:
        worker(args.root,args.worker,counts,args.report)
    elif args.root:
        court(args.root.resolve(),args.rows,args.width,args.governed,counts)
    else:
        with tempfile.TemporaryDirectory(prefix="pyat-r14-") as root:
            court(Path(root),args.rows,args.width,args.governed,counts)

if __name__=="__main__":
    main()
