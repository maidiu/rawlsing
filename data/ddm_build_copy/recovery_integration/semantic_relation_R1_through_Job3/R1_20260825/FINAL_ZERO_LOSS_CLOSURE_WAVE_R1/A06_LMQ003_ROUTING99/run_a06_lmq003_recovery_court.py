#!/usr/bin/env python3
"""A06 LMQ-003 recovery court: exact historical 99 membership, fail closed."""
from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path
import pandas as pd

EXPECTED_REGISTRY_SHA="a91239a5e630c554d2c397f739a60f1313ea8ab7377780ee3c64f4969e49267b"
EXPECTED_S0_SHA="c8b6cfd4a027a4b7b2c04c47d7ca0e37640082595ac058e77f99a0810d671554"
EXPECTED_R14_SHA="fa1d4d91692b7e5349657d0e3becd3ee248d8d4a76ceec1dd5238d34843a7fa0"
EXPECTED_CHECKPOINT_SHA="84fa0cf71488f69c9c362619d8fb557ea6f48828da095dd4b551a439e190b388"
TARGET_STATUS="SOURCE_ROUTING_SIGNAL_REQUIRES_EXACT_PREDICATE_COMPILATION"
EXPECTED_DENOMINATOR=99
EXPECTED_WRAPPER="Rawlsing_R3_Routing_Applicability_Retrieval_Delta_20260808.zip"
EXPECTED_WRAPPER_SHA="e27ceb340eac5d7124e44b80081e5c0309a342326c045df6d6f6d0cd71910c46"
EXPECTED_OUTPUTS=("question_applicability_predicate_authority_full_v1.json","routing_provenance_ledger.csv","routing_authority_compile_summary.json","routing_unresolved_ledger.csv")

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024), b""): h.update(b)
    return h.hexdigest()

def names_recursive(zpath: Path):
    out=[]
    with zipfile.ZipFile(zpath) as z:
        out.extend(z.namelist())
        for n in z.namelist():
            if n.lower().endswith(".zip") and z.getinfo(n).file_size < 100_000_000:
                tmp=zpath.parent/"__nested_a06.zip"; tmp.write_bytes(z.read(n))
                try:
                    with zipfile.ZipFile(tmp) as nz: out.extend(f"{n}::{x}" for x in nz.namelist())
                finally: tmp.unlink(missing_ok=True)
    return out

def main():
    ap=argparse.ArgumentParser()
    for x in ("registry","s0","r14","checkpoint","receipt"): ap.add_argument(f"--{x}",type=Path,required=True)
    a=ap.parse_args()
    hashes={"registry":sha256_file(a.registry),"s0":sha256_file(a.s0),"r14":sha256_file(a.r14),"checkpoint":sha256_file(a.checkpoint)}
    assert hashes=={"registry":EXPECTED_REGISTRY_SHA,"s0":EXPECTED_S0_SHA,"r14":EXPECTED_R14_SHA,"checkpoint":EXPECTED_CHECKPOINT_SHA}
    reg=pd.read_csv(a.registry,dtype=str).fillna(""); s0=pd.read_csv(a.s0,dtype=str).fillna(""); r14=pd.read_csv(a.r14,dtype=str).fillna("")
    assert len(reg)==700
    rkey=["source_family","canonical_wave","var_code"]; skey=["source_family","wave","source_variable_code"]
    assert not reg.duplicated(rkey).any() and not s0.duplicated(skey).any()
    joined=reg.merge(s0[skey+["question_implementation_id","routing_signal_status","respondent_universe_status"]],left_on=rkey,right_on=skey,how="left",indicator=True)
    assert len(joined)==700 and (joined["_merge"]=="both").all()
    later_counts=joined["routing_signal_status"].value_counts().to_dict()
    marker=sum(int(frame.astype(str).apply(lambda c:c.str.contains(TARGET_STATUS,regex=False).sum()).sum()) for frame in (reg,s0,r14))
    archive_names=names_recursive(a.checkpoint)
    archive_hits=[n for n in archive_names if EXPECTED_WRAPPER.lower() in n.lower() or any(x.lower() in n.lower() for x in EXPECTED_OUTPUTS)]
    source_column_presence=int(reg["var_code"].ne("").sum())
    tests={
      "registry_exact_hash_and_700_rows":"PASS",
      "registry_to_successor_exact_key_join_700_of_700":"PASS",
      "no_fuzzy_matching_used":"PASS",
      "later_routing_statuses_not_substituted_for_historical_99":"PASS" if all(v!=99 for v in later_counts.values()) else "FAIL",
      "source_column_presence_not_substituted_for_historical_99":"PASS" if source_column_presence!=99 else "FAIL",
      "historical_target_membership_marker_absent_from_inspected_row_artifacts":"PASS" if marker==0 else "FAIL",
      "checkpoint_does_not_materialize_wrapper_or_expected_outputs":"PASS" if not archive_hits else "FAIL"}
    assert set(tests.values())=={"PASS"}
    receipt={"schema":"A06_LMQ003_EXACT_IDENTITY_RECOVERY_COURT@1.0.0","status":"BLOCKED_EXACT_HISTORICAL_ROW_IDENTITIES_NOT_RECOVERED","historical_target_status":TARGET_STATUS,"historical_denominator":99,"exact_historical_rows_positively_recovered":0,"exact_historical_rows_remaining_blocked":99,"wrapper":{"name":EXPECTED_WRAPPER,"inventory_sha256":EXPECTED_WRAPPER_SHA,"payload_materialized":False,"used_as_semantic_input":False},"input_sha256":hashes,"registry_rows":len(reg),"exact_registry_successor_join_rows":int((joined["_merge"]=="both").sum()),"later_routing_signal_status_counts":later_counts,"historical_target_marker_occurrences_in_inspected_row_artifacts":marker,"checkpoint_archive_target_hits":archive_hits,"hostile_tests":tests,"negative_ceiling":["AGGREGATE_99_COUNT != EXACT_99_ROW_IDENTITIES","SOURCE_COLUMN_PRESENCE != ROUTING_AUTHORITY","LATER_ROUTING_SIGNAL_STATUS != HISTORICAL_R3_PARTITION_MEMBERSHIP","QUESTION_TEXT_OR_THEME != HISTORICAL_ROW_IDENTITY","EXACT_700_KEY_CONTINUITY != PROOF_OF_WHICH_99_ROWS","CURRENT_ROUTING_PREDICATE_ENGINE != ROW_SPECIFIC_ROUTING_AUTHORITY"],"disposition":"LMQ003_REMAINS_OPEN__99_OF_99_EXACT_HISTORICAL_SOURCE_SIGNALED_ROW_IDENTITIES_UNRECOVERED"}
    a.receipt.write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":receipt["status"],"tests_passed":len(tests),"tests_failed":0,"recovered":0,"blocked":99},sort_keys=True))
if __name__=="__main__": main()
