from __future__ import annotations
import argparse, json, os, platform, sys, time
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from .ee_w4_harness_contract import *
from .ee_w4_harness_runtime import *

def logical_record(r:Mapping[str,Any])->dict[str,Any]:
    keys=("candidate_id","step_id","universe_id","operation_id","phase","action","eligibility_state","outcome","semantic_oracle_status","identity_oracle_status","semantic_output_sha256","deterministic_output_identity","learned_product_release_identity","learned_product_replay_identity")
    return {k:r.get(k) for k in keys}
def logical_receipt_sha256(records:Iterable[Mapping[str,Any]],plan_sha256:str)->str:
    rows=sorted((logical_record(r) for r in records),key=lambda r:(r["candidate_id"],r["step_id"]))
    return sha256_bytes(canonical_json_bytes({"plan_sha256":plan_sha256,"records":rows}))

def execute_harness(manifest:Mapping[str,Any],candidate_config:Mapping[str,Any],run_root:Path|str,*,candidate_order:Sequence[str]=CANDIDATE_IDS,monitor_interval_seconds:float=.005)->dict[str,Any]:
    plan=validate_workload_manifest(manifest); candidates=validate_candidate_config(candidate_config)
    if tuple(sorted(candidate_order))!=CANDIDATE_IDS or len(candidate_order)!=3: raise HarnessContractError("candidate_order must be a permutation of A/B/C")
    root=Path(run_root); root.mkdir(parents=True,exist_ok=True); records=[]; orders={}
    for candidate in candidate_order:
        croot=root/f"candidate_{candidate}"; scratch=croot/"scratch"; durable=croot/"durable"; logs=croot/"logs"; requests=croot/"requests"; responses=croot/"responses"
        for p in (scratch,durable,logs,requests,responses): p.mkdir(parents=True,exist_ok=True)
        orders[candidate]=[]
        for ordinal,step in enumerate(plan["steps"]):
            sid=step["step_id"]; orders[candidate].append(sid); state=step["eligibility"]["state"]
            r={"candidate_id":candidate,"step_ordinal":ordinal,"step_id":sid,"universe_id":step["universe_id"],"operation_id":step["operation_id"],"ee_requirement_ids":list(step["ee_requirement_ids"]),"phase":step["phase"],"action":step["action"],"hostile_case_id":step.get("hostile_case_id"),"eligibility_state":state,"eligibility_exact_basis":step["eligibility"]["exact_basis"],"plan_sha256":plan["plan_sha256"],"request_sha256":None,"outcome":None,"semantic_oracle_status":"NOT_RUN","identity_oracle_status":"NOT_RUN","measurement_complete":True,"failure_class":None,"wall_ns":None,"cpu_user_ns":None,"cpu_system_ns":None,"peak_rss_bytes":None,"scratch_bytes_before":None,"scratch_bytes_after":None,"peak_scratch_bytes_observed":None,"peak_scratch_file_count_observed":None,"max_single_temp_object_bytes_observed":None,"durable_bytes_before":None,"durable_bytes_after":None,"durable_bytes_created_delta":None,"source_open_count":None,"source_decode_count":None,"bytes_read":None,"bytes_written":None,"temporary_spill_bytes_reported":None,"cache_index_bytes_created":None,"rewritten_bytes":None,"semantic_output_sha256":None,"deterministic_output_identity":None,"learned_product_release_identity":None,"learned_product_replay_identity":None}
            if state!=ELIGIBLE:
                r.update(outcome=ineligible_outcome(state),semantic_oracle_status="NOT_APPLICABLE",identity_oracle_status="NOT_APPLICABLE"); records.append(r); continue
            sb=dir_stats(scratch); db=dir_stats(durable); r["scratch_bytes_before"]=sb["bytes"]; r["durable_bytes_before"]=db["bytes"]
            action=step["action"]
            if action in HARNESS_ACTIONS:
                start=time.monotonic_ns()
                try: apply_harness_action(action,scratch,durable); r.update(outcome="PASS",semantic_oracle_status="PASS",identity_oracle_status="NOT_REQUESTED")
                except BaseException: r.update(outcome="HARNESS_ACTION_FAILURE",failure_class="HARNESS_ACTION_FAILURE")
                r["wall_ns"]=time.monotonic_ns()-start; sa=dir_stats(scratch); da=dir_stats(durable); r.update(scratch_bytes_after=sa["bytes"],durable_bytes_after=da["bytes"],durable_bytes_created_delta=da["bytes"]-db["bytes"],peak_scratch_bytes_observed=max(sb["bytes"],sa["bytes"]),peak_scratch_file_count_observed=max(sb["files"],sa["files"]),max_single_temp_object_bytes_observed=max(sb["max_single_file_bytes"],sa["max_single_file_bytes"])); records.append(r); continue
            req={"schema":HARNESS_SCHEMA,"workload_id":plan["workload_id"],"plan_sha256":plan["plan_sha256"],"step_ordinal":ordinal,"step_id":sid,"universe_id":step["universe_id"],"operation_id":step["operation_id"],"phase":step["phase"],"action":action,"ee_requirement_ids":list(step["ee_requirement_ids"]),"hostile_case_id":step.get("hostile_case_id"),"request":step.get("request"),"invalidation_targets":step.get("invalidation_targets")}
            b=canonical_json_bytes(req); r["request_sha256"]=sha256_bytes(b); qp=requests/f"{ordinal:05d}-{sid}.json"; rp=responses/f"{ordinal:05d}-{sid}.json"; out=logs/f"{ordinal:05d}-{sid}.stdout"; err=logs/f"{ordinal:05d}-{sid}.stderr"; qp.write_bytes(b); rp.unlink(missing_ok=True)
            monitor=PeakMonitor(scratch,durable,monitor_interval_seconds); argv=expand_argv(candidates[candidate],qp,rp,scratch,durable)
            try: code,usage,wall=run_wait4(argv,out,err,os.environ.copy(),monitor); r["wall_ns"]=wall; r.update(rusage_metrics(usage))
            except BaseException: r.update(outcome="CANDIDATE_LAUNCH_FAILURE",failure_class="CANDIDATE_LAUNCH_FAILURE",measurement_complete=False); records.append(r); continue
            r.update(peak_scratch_bytes_observed=monitor.peak_scratch_bytes,peak_scratch_file_count_observed=monitor.peak_scratch_files,max_single_temp_object_bytes_observed=monitor.max_single_temp_object_bytes)
            if code!=0: r.update(outcome="CANDIDATE_NONZERO_EXIT",failure_class="CANDIDATE_NONZERO_EXIT",measurement_complete=False)
            elif not rp.exists(): r.update(outcome="CANDIDATE_RESPONSE_MISSING",failure_class="CANDIDATE_RESPONSE_MISSING",measurement_complete=False)
            else:
                try:
                    x=json.loads(rp.read_text());
                    if not isinstance(x,dict) or x.get("status")!="OK" or not hex64(x.get("semantic_output_sha256")): raise ValueError
                    r["semantic_output_sha256"]=x["semantic_output_sha256"]; oracle=step["oracle"]; r["semantic_oracle_status"]="PASS" if x["semantic_output_sha256"]==oracle["semantic_output_sha256"] else "FAIL"
                    ids=x.get("identities") or {}; tel=x.get("telemetry") or {}
                    if not isinstance(ids,dict) or not isinstance(tel,dict): raise ValueError
                    for k in ("deterministic_output_identity","learned_product_release_identity","learned_product_replay_identity"): r[k]=ids.get(k)
                    r["identity_oracle_status"]=identity_status(oracle,ids)
                    for k in ("source_open_count","source_decode_count","bytes_read","bytes_written","cache_index_bytes_created","rewritten_bytes"): r[k]=tel.get(k)
                    r["temporary_spill_bytes_reported"]=tel.get("temporary_spill_bytes")
                    if not isinstance(r["source_open_count"],int) or r["source_open_count"]<0 or not isinstance(r["source_decode_count"],int) or r["source_decode_count"]<0: r["measurement_complete"]=False
                    if r["semantic_oracle_status"]!="PASS": r.update(outcome="SEMANTIC_ORACLE_MISMATCH",failure_class="SEMANTIC_ORACLE_MISMATCH")
                    elif r["identity_oracle_status"]=="FAIL": r.update(outcome="IDENTITY_ORACLE_MISMATCH",failure_class="IDENTITY_ORACLE_MISMATCH")
                    elif not r["measurement_complete"]: r.update(outcome="MEASUREMENT_TELEMETRY_INCOMPLETE",failure_class="MEASUREMENT_TELEMETRY_INCOMPLETE")
                    else: r["outcome"]="PASS"
                except BaseException: r.update(outcome="CANDIDATE_RESPONSE_INVALID",failure_class="CANDIDATE_RESPONSE_INVALID",measurement_complete=False)
            sa=dir_stats(scratch); da=dir_stats(durable); r.update(scratch_bytes_after=sa["bytes"],durable_bytes_after=da["bytes"],durable_bytes_created_delta=da["bytes"]-db["bytes"]); records.append(r)
    expected=[s["step_id"] for s in plan["steps"]]; order_ok=all(orders[c]==expected for c in CANDIDATE_IDS)
    hashes=defaultdict(set)
    for r in records:
        if r["request_sha256"] is not None: hashes[r["step_id"]].add(r["request_sha256"])
    request_ok=all(len(v)==1 for v in hashes.values()); summaries={}
    for c in CANDIDATE_IDS:
        rows=[r for r in records if r["candidate_id"]==c]; e=[r for r in rows if r["eligibility_state"]==ELIGIBLE]; f=[r for r in e if r["outcome"]!="PASS"]
        summaries[c]={"declared_steps":len(rows),"eligible_steps":len(e),"ineligible_steps":len(rows)-len(e),"pass_steps":sum(r["outcome"]=="PASS" for r in e),"candidate_or_oracle_failures":len(f),"performance_eligible":bool(e) and not f and order_ok and request_ok}
    grouped=defaultdict(list)
    for r in records: grouped[(r["candidate_id"],r["universe_id"],r["operation_id"],r["phase"])].append(r)
    metric={}
    for (c,u,o,p),rows in sorted(grouped.items()): metric[f"{c}|{u}|{o}|{p}"]={"candidate_id":c,"universe_id":u,"operation_id":o,"phase":p,"rows":len(rows),"wall_ns_samples":[r["wall_ns"] for r in rows if isinstance(r["wall_ns"],int)],"note":"NO_CROSS_UNIVERSE_AGGREGATION"}
    receipt={"schema":HARNESS_SCHEMA,"status":"HARNESS_EXECUTION_RECEIPT__NO_RANKING","workload_id":plan["workload_id"],"workload_manifest_sha256":plan["manifest_sha256"],"execution_plan_sha256":plan["plan_sha256"],"candidate_ids":list(CANDIDATE_IDS),"candidate_execution_order":list(candidate_order),"exact_same_step_order_all_candidates":order_ok,"candidate_neutral_request_payloads":request_ok,"candidate_summary":summaries,"records":records,"metric_groups":metric,"environment":{"python":platform.python_version(),"implementation":platform.python_implementation(),"platform":platform.platform(),"executable":sys.executable},"laws":["SAME_MANIFEST + SAME_ELIGIBLE_UNIVERSE_CELL + SAME_OPERATION + SAME_ORACLE + SAME_METRIC_DEFINITION","COMMON_QUERY_INTERFACE != POOLED_EMPIRICAL_UNIVERSE","MISSING_AUTHORITY != CANDIDATE_FAILURE","SEMANTIC_PARITY_BEFORE_PERFORMANCE","NO_CROSS_UNIVERSE_METRIC_POOLING"]}
    receipt["logical_receipt_sha256"]=logical_receipt_sha256(records,plan["plan_sha256"]); return receipt

def main(argv:Sequence[str]|None=None)->int:
    p=argparse.ArgumentParser(); p.add_argument("--workload",required=True); p.add_argument("--candidates",required=True); p.add_argument("--run-root",required=True); p.add_argument("--receipt",required=True); n=p.parse_args(argv)
    r=execute_harness(json.loads(Path(n.workload).read_text()),json.loads(Path(n.candidates).read_text()),Path(n.run_root)); Path(n.receipt).write_bytes(canonical_json_bytes(r)); print(r["status"]); print(r["logical_receipt_sha256"]); return 0
if __name__=="__main__": raise SystemExit(main())
