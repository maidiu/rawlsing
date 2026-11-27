"""Matched sourcefree country lifetime cost, baseline and candidate fresh processes.
Use one generated source and country file. Never compare different survey data.
The original native issuer, I02, I03/I05 and S2E remain the execution owners.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict,replace
import json,os,subprocess,sys,tempfile,time
from pathlib import Path
from statistics import median
from unittest.mock import patch

BASE="c129e5cad7545bdd2c63a81e15959148b45c7bda"

def worker(root,mode,report):
    from tools.pyat_country_preparation_court import read,write,geometry,target_domains
    from rawlsing_next.tests.test_pre553_country_numeric_economics import CountryNativeEconomics
    from rawlsing_next.tests.test_pre553_empirical_query import _ref,_cell_map
    from rawlsing_next import pre553_country_numeric_carrier as carrier
    from rawlsing_next import pre553_source_backed_c11_facade as facade
    from rawlsing_next import pre553_issued_workload as issued
    from rawlsing_next.pre553_empirical_objects import semantic_hash,exact_ref
    from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
    from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
    import numpy as np
    import inspect
    cfg=read(root/"fixture.json");receipt=carrier.CountryReceipt(**cfg["receipt"])
    rows,width,governed=cfg["rows"],cfg["width"],cfg["governed"]
    values=geometry(rows,width,governed,True)
    db=root/"country.sqlite";prepared=report.parent/"headers.gz"
    start=time.monotonic()
    workload,record,queries,host,purpose,qrefs=CountryNativeEconomics()._native_batch(wide=True,
        external_case=dict(root=root,db=db,receipt=receipt,ordinals=cfg["ordinals"],
           selected=values[::2,:],chosen=tuple(range(1,2*rows+1,2)),country="A",
           governed=governed,physical_width=width,target_domains=target_domains(governed,True)))
    issuance=time.monotonic()-start
    cases=[]
    # Real distinct issued decisions. Revisit overlapping targets/predicates
    # just as a progressive investigation does; never skip the native calls.
    for label,count,lo in (("first",1,0),("ten",10,0),("hundred",100,0),("revisit",50,50)):
        req=workload.requests[lo:lo+count]
        ds=workload.discoveries if count==100 else ()
        jobs=issued.operation_jobs(req,ds);decision=_ref("TEST_ONLY_DECISION","lifetime-"+label)
        u=semantic_hash({"lifetime":label,"source":receipt.source_sha256})
        frontier=semantic_hash({"jobs":jobs,"root":u})
        item=replace(workload,decision_ref=decision,requests=req,discoveries=ds,
                     original_u_root=u,expected_frontier_root=frontier)
        grant=replace(record,decision_ref=decision,expected_jobs=jobs,
                      original_u_root=u,expected_frontier_root=frontier,
                      envelope_sha256=issued._stream_workload_digest(item))
        cases.append((label,item,TestOnlyDecisionResolver(grant)))
    issue_all=time.monotonic()-start
    kwargs=dict(require_current=lambda:True,preparation_path=prepared)
    if "reuse_query_preparation" in inspect.signature(carrier.CountryWorkloadSession).parameters:
        kwargs["reuse_query_preparation"]=True
    if "omit_preparation_group_plane" in inspect.signature(carrier.CountryWorkloadSession).parameters:
        kwargs["omit_preparation_group_plane"]=True
    if mode=="restore":
        from rawlsing_next._pre553_country_preparation import CountryPreparationPin
        kwargs["preparation_pin"]=CountryPreparationPin(**read(report.parent/"pin.json"))
    counts={k:0 for k in ("I02","I03","I05","admission","scope_check","scope_current","nonrouting_pin","projection_identity","full_file_auth")}
    phases={k:0. for k in counts}
    def monitor(owner,name,label):
        original=getattr(owner,name)
        def invoke(*a,**kw):
            counts[label]+=1;t=time.monotonic()
            try:return original(*a,**kw)
            finally:phases[label]+=time.monotonic()-t
        return patch.object(owner,name,invoke)
    qindices={q.ref.key:i for i,q in enumerate(queries)}
    axes={r.key:i for i,r in enumerate(qrefs.values())}
    selected=values[::2,:]
    def source_counts(result):
        checked=0
        for unit in result.manifest.units:
            if unit.job_kind!="QUERY":continue
            i=qindices[unit.job_ref.key];query=queries[i]
            fact=result.outputs_by_unit[unit.unit_hash].facts[0]
            mask=(np.ones(rows,dtype=bool) if i in (0,99) else
                  selected[:,0]==1 if i<=50 else selected[:,1]==0)
            assert fact.raw_denominator_support==int(mask.sum()),i
            for cell,record0 in _cell_map(fact).items():
                vals=(cell,) if isinstance(cell,str) else cell
                check=mask.copy()
                for ref,val in zip(query.target_refs,vals):
                    check &= selected[:,axes[exact_ref(ref).key]]==int(val)
                assert record0["raw_numerator_support"]==int(check.sum()),(i,cell)
            checked+=1
        return checked
    evidence=[];times=[];group_receipt=None
    from contextlib import ExitStack
    with ExitStack() as stack:
        for owner,name,label in (
            (facade,"_validate_country_produced_release","I02"),
            (CarrierNeutralResearchExecutor,"execute_i03","I03"),
            (CarrierNeutralResearchExecutor,"execute_i05","I05"),
            (issued,"_admit","admission"),
            (issued._CountryAdmissionScope,"check","scope_check"),
            (issued._CountryAdmissionScope,"current_only","scope_current"),
            (issued._NonRoutingEnvelopePin,"matches","nonrouting_pin"),
            (facade._CountryProjectionPin,"matches","projection_identity"),
            (carrier.CountryReader,"verify_full","full_file_auth"),
        ):
            stack.enter_context(monitor(owner,name,label))
        with carrier.CountryWorkloadSession(db,receipt,**kwargs) as session:
            for label,item,resolver in cases:
                prior_phases=phases.copy()
                prior_counts=counts.copy()
                t=time.monotonic()
                execution=session.execute(item,resolver,host=host,purpose=purpose)
                elapsed=time.monotonic()-t
                proof=execution.result.exact_s2e_output_census(runtime_catalog=item.catalog)
                checked=source_counts(execution.result)
                times.append({"label":label,"wall_s":elapsed,"source_counts":checked,
                    "inclusive_s":{k:phases[k]-prior_phases[k] for k in phases},
                    "phase_calls":{k:counts[k]-prior_counts[k] for k in counts}})
                evidence.append((label,proof.as_dict(),execution.release_identity.as_dict()))
                del execution,proof
            scope=getattr(session,"_query_scope",None)
            if scope is not None:group_receipt=dict(scope.receipt())
            pin=session.preparation_pin
        assert counts["I02"]==1 and counts["I03"]>=161 and counts["I05"]==1,counts
    if mode=="save":write(report.parent/"pin.json",asdict(pin))
    write(report,{"mode":mode,"issuance_s":issuance,"all_issuance_s":issue_all,
        "country_bytes":db.stat().st_size,"routing_payload_bytes":workload.projection.routing.payload_bytes,
        "preparation_bytes":prepared.stat().st_size,"counts":counts,"inclusive_s":phases,
        "investigations":times,"group_receipt":group_receipt,"evidence":evidence})
    print("LIFETIME_WORKER",json.dumps({k:v for k,v in read(report).items() if k!="evidence"}),flush=True)

def court(rows):
    from tools.pyat_country_preparation_court import setup,read
    from tools.pyat_country_campaign_court import sample_tree,disk_snapshot,kill_tree,LIMIT
    repo=Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="pyat-lifetime-") as temp:
        root=Path(temp);data=root/"fixture";data.mkdir(mode=0o700)
        setup(data,rows,613,390,True)
        baseline=root/"baseline-code"
        subprocess.run(["git","worktree","add","--detach",str(baseline),BASE],cwd=repo,check=True)
        reports={}
        try:
            for variant,checkout in (("baseline",baseline),("candidate",repo)):
                dest=root/variant;dest.mkdir(mode=0o700)
                for mode in ("save","restore"):
                    report=dest/(mode+".json")
                    env=dict(os.environ,PYTHONPATH=str(checkout),PYTHONUNBUFFERED="1")
                    t=time.monotonic();peak=0;samples=0;disk={}
                    proc=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),"--worker",mode,
                        "--root",str(data),"--report",str(report)],cwd=checkout,env=env,start_new_session=True)
                    try:
                        while True:
                            rss,_=sample_tree(proc.pid);peak=max(peak,rss);samples+=1
                            for k,v in disk_snapshot(dest).items():disk[k]=max(disk.get(k,0),v)
                            if rss>LIMIT:kill_tree(proc);raise RuntimeError("sampled worker memory limit exceeded")
                            if proc.poll() is not None:break
                            time.sleep(.1)
                    finally:
                        if proc.poll() is None:kill_tree(proc)
                        proc.wait()
                    if proc.returncode:raise RuntimeError(variant+" "+mode+" worker failed")
                    value=read(report);value.update(outer_wall_s=time.monotonic()-t,
                      sampled_peak_tree_rss=peak,resource_samples=samples,sampled_disk_peak=disk)
                    reports[(variant,mode)]=value
            first=reports[("baseline","save")]["evidence"]
            assert all(x["evidence"]==first for x in reports.values()),"exact release/census drift"
            print("LIFETIME_MATCHED",json.dumps({"rows":rows,"width":613,"governed":390,
                "physical_setup":read(data/"fixture.json"),
                "exact_census_and_release_parity":True,
                "reports":[dict(variant=k[0],**{a:b for a,b in v.items() if a!="evidence"})
                           for k,v in reports.items()],
                "grade":"MATCHED_SOURCEFREE_WVS7_WIDTH_AND_RESPONSE_SLOT_COUNT__NOT_ORIGINAL"},sort_keys=True),flush=True)
        finally:
            subprocess.run(["git","worktree","remove","--force",str(baseline)],cwd=repo,check=True)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--rows",type=int,default=128)
    parser.add_argument("--worker",choices=("save","restore"))
    parser.add_argument("--root",type=Path)
    parser.add_argument("--report",type=Path)
    args=parser.parse_args()
    if args.worker:
        # Script is shared by both arms, but all actual owners are imported
        # from the independently selected checkout, not the candidate.
        sys.path.insert(0,os.getcwd())
        worker(args.root,args.worker,args.report)
    else:court(args.rows)
