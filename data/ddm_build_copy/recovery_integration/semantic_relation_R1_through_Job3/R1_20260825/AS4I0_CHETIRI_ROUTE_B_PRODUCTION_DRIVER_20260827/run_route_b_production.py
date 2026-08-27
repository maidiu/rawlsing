#!/usr/bin/env python3
"""One-command governed Route-B entry point. This lane does not invoke it."""
import argparse,json
from pathlib import Path
from rawlsing_next.pre553_as4i0_route_b_driver import build_route_b_source_session,execute_route_b_production,load_and_validate_as3r2,require_runtime_catalog_payload

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True,type=Path); p.add_argument("--as3r2",required=True,type=Path)
    p.add_argument("--runtime-catalog",required=True,type=Path); p.add_argument("--as2b-builder",required=True,type=Path)
    p.add_argument("--as2a-dir",required=True,type=Path); p.add_argument("--receipt",required=True,type=Path)
    a=p.parse_args(); seal=load_and_validate_as3r2(a.as3r2)
    predicates,queries=require_runtime_catalog_payload(a.runtime_catalog,seal)
    session=build_route_b_source_session(a.source,a.as2b_builder,a.as2a_dir)
    result=execute_route_b_production(seal,session,(x.as_dict() for x in predicates),(x.as_dict() for x in queries))
    out={"schema":"AS4I0_ROUTE_B_EXECUTION_RECEIPT@1.0.0","status":"PASS","candidate_count":result.candidate_count,"covered_candidate_count":result.covered_candidate_count,"evaluated_frontier_ref":result.evaluated_frontier_ref.as_dict(),"frontier_replay_ref":result.replay_ref.as_dict(),"result_receipt_count":len(result.receipts),"empirical_fact_ref_count":len(result.empirical_fact_refs),"persistent_transformed_empirical_payload_files":[],"session_boundary":"SOURCE_BACKED_C11_SESSION_CLOSED_BEFORE_RECEIPT_WRITE"}
    a.receipt.parent.mkdir(parents=True,exist_ok=True); a.receipt.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(out,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
