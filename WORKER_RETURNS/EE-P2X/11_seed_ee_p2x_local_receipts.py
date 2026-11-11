#!/usr/bin/env python3
"""Seed EE-P2X local-court receipt skeletons without source/outcome access.

PROPOSED ONLY until HQ adopts EE-P2X-RV.  No carrier is opened and no
empirical/performance value is supplied by this script.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
EXPECT=HERE/"09_LOCAL_COURT_FROZEN_EXPECTATIONS.json"
CONTRACT=HERE/"10_LOCAL_COURT_RECEIPT_CONTRACT.json"
OUT=HERE/"LOCAL_COURT"
CELLS=[("LITS_I","A"),("LITS_I","B"),("LITS_I","C"),("WVS7","A"),("WVS7","B")]
COVERAGE=["LITS_I/A","LITS_I/B","LITS_I/C","WVS7/A","WVS7/B","WVS7/C"]

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def write(p,v,force):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists() and not force: return
    p.write_text(json.dumps(v,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def pending_metric():
    return {"state":"PENDING_LOCAL_DARWIN","value":None,"unit":"UNSET",
            "reason":"Executor must fill or type this slot; verifier rejects PENDING."}

def cell(e,c,source,candidate,idx):
    preserved=[]
    if (source,candidate)==("LITS_I","A"): preserved=["LITS_I_A_FIRST_BUILD"]
    if (source,candidate)==("LITS_I","B"): preserved=["LITS_I_B_CACHELESS_C11"]
    projection=(e["sources"]["LITS_I"]["projection_cache_identity"] if source=="LITS_I"
                else "PENDING_EXACT_WVS_GOVERNED_PROJECTION_IDENTITY")
    return {
      "schema":"RAWLSING_EE_P2X_SOURCE_CANDIDATE_RECEIPT@1.0.0",
      "source":source,"candidate":candidate,"sequence_index":idx,
      "authority":{"hq_handoff_commit":e["hq"]["handoff_commit"],
                   "lock1_manifest_blob":e["lock1"]["manifest_json_git_blob_sha1"],
                   "lock2_hash":e["lock2"]["hash"]},
      "host":{"identity_sha256":"PENDING_LOCAL_DARWIN","same_physical_host_token":"PENDING_LOCAL_DARWIN"},
      "runtime":dict(e["runtime"]),
      "bindings":{"source_sha256":e["sources"][source]["sha256"],
                  "candidate_owner_blob":e["candidates"][candidate]["owner_blob"],
                  "execution_seam_blob":e["execution_seam"]["git_blob_sha1"],
                  "projection_identity":projection,
                  "runtime_catalog_identity":"PENDING_EXACT_PREOUTCOME_RUNTIME_CATALOG_IDENTITY",
                  "candidate_provider_identity":"PENDING_EXACT_ACCEPTED_PROVIDER_IDENTITY"},
      "event_ordinals":{"oracle_frozen":None,"candidate_output_first":None,
                        "parity_complete":None,"performance_first_admitted":None},
      "oracle":{"candidate_neutral":True,"candidate_defined":False,
                "oracle_identity_sha256":"PENDING_PRE_CANDIDATE_ORACLE_IDENTITY"},
      "parity":{"semantic":"PENDING","exactref_identity":"PENDING","replay":"PENDING",
                "integrity_fail_closed":"PENDING","frontier_typed_negative":"PENDING"},
      "performance_admission":"NOT_ADMITTED",
      "metrics":{n:pending_metric() for n in c["source_candidate_receipt"]["metric_names"]},
      "behaviors":{"stale_cache":{"state":"PENDING_LOCAL_DARWIN","evidence_identity":None},
                   "corrupt_cache":{"state":"PENDING_LOCAL_DARWIN","evidence_identity":None},
                   "interruption_session_recovery":{"state":"PENDING_LOCAL_DARWIN","evidence_identity":None}},
      "outputs":{"exact_output_identity":None,"product_identity":None,"semantic_identity":None,"replay_identity":None},
      "preserved_stage_consumption":preserved,
      "disposition":"PENDING_LOCAL_DARWIN","ranking_or_selection":False}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--force",action="store_true"); a=ap.parse_args()
    e,c=load(EXPECT),load(CONTRACT)
    write(OUT/"00_COURT_RUN_MANIFEST.json",{
      "schema":"RAWLSING_EE_P2X_LOCAL_COURT_RUN_MANIFEST@1.0.0",
      "hq_handoff_commit":e["hq"]["handoff_commit"],
      "lock1_manifest_blob":e["lock1"]["manifest_json_git_blob_sha1"],
      "lock2_hash":e["lock2"]["hash"],
      "physical_host_identity_sha256":"PENDING_LOCAL_DARWIN",
      "runtime":dict(e["runtime"]),
      "coverage":[
          *[{"cell":x,"state":"PENDING_LOCAL_DARWIN",
             "cell_receipt":"WORKER_RETURNS/EE-P2X/LOCAL_COURT/cells/"+x.replace("/","__")+".json",
             "failure_receipt":None} for x in COVERAGE[:-1]],
          {"cell":"WVS7/C","state":"PRESERVED_FAILURE","cell_receipt":None,
           "failure_receipt":"WORKER_RETURNS/EE-P2X/LOCAL_COURT/failures/WVS7__C__WVS7_C_CURRENT_PORTABILITY_FAILURE.json"}
      ],
      "attempted_cells":[],
      "executed_stage_ids":[],
      "source_metric_pooling":False,
      "ranking_or_selection":False},a.force)
    for idx,(source,candidate) in enumerate(CELLS):
        write(OUT/"cells"/f"{source}__{candidate}.json",cell(e,c,source,candidate,idx),a.force)
    write(OUT/"failures"/"WVS7__C__WVS7_C_CURRENT_PORTABILITY_FAILURE.json",{
      "schema":"RAWLSING_EE_P2X_FAILURE_STOP_RECEIPT@1.0.0","source":"WVS7","candidate":"C",
      "kind":"WVS7_C_CURRENT_PORTABILITY_FAILURE",
      "blocking_scope":"NONBLOCKING_PRESERVED_CANDIDATE_EVIDENCE",
      "disposition":"WVS7_C__CURRENT_PORTABILITY_FAILURE",
      "evidence_paths":["WORKER_RETURNS/EE-P2R1/10_ABC_ADAPTER_QUALIFICATION_MATRIX.json",
                        "WORKER_RETURNS/EE-P2R1/12_WVS_C_ZERO_ACCELERATOR_ADJUDICATION.json"],
      "later_lawful_cells_suppressed":False,"synthetic_fallback_used":False},a.force)
    print("SEEDED__NO_SOURCE_ACCESS__ALL_EMPIRICAL_AND_PERFORMANCE_FIELDS_PENDING")
if __name__=="__main__": main()
