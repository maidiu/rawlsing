"""Verify retained scope, native evidence and exact relocated cold identities."""
import gzip,hashlib,json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/"repro"))
import build_frontier as b


def xml(name,tests,failures=0):
    tree=ET.parse(R/"evidence"/name)
    cases=tree.findall(".//testcase")
    result=dict(tests=len(cases),failures=len(tree.findall(".//failure")),errors=len(tree.findall(".//error")),skips=len(tree.findall(".//skipped")))
    if result!=dict(tests=tests,failures=failures,errors=0,skips=0):
        raise ValueError("ACTUAL_JUNIT_MISMATCH:"+name+":"+str(result))
    return result


def main():
    b.verify_freeze()
    data=gzip.decompress((R/"source_wave_item_operation_frontier.jsonl.gz").read_bytes())
    rows=[json.loads(x) for x in data.splitlines()]
    anti=b.verify_no_drop(rows)
    summary=json.loads((R/"evidence/original35_frontier_summary.json").read_text())
    assert hashlib.sha256(data).hexdigest()==summary["frontier_sha256"]
    assert sum(i["inherited_WG0R_disposition"] is not None for i in rows)==18276
    scope=json.loads((R/"A42_151_101_and_81_owner_demands.json").read_text())
    assert len(scope["register_151"])==151 and len(scope["ledger_101"])==101
    assert len(scope["unmatched81"])==81 and len(scope["AT_obligations"])==35
    actual=json.loads((R/"currently_permitted_native_manifests.json").read_text())
    assert len(actual["waves"])==35 and actual["original_measured_wave_count"]==0
    assert all(w["native_manifest"] is None for w in actual["waves"])
    courts={name:xml(name,n,f) for name,n,f in [
        ("u43_final.xml",46,0),("u43_relocated_cold.xml",46,0),
        ("wg0l_repaired65_restored.xml",65,0),("wg0l_relocated_cold65.xml",65,0),
        ("wg0l_descriptor_repaired.xml",9,0),("current_p10_74.xml",74,0),
        ("wg0l_exact_baseline3.xml",3,3),
        ("query_only_warm.xml",1,0),("query_only_cold.xml",1,0),
        ("final_metadata_warm.xml",8,0),("final_metadata_cold.xml",8,0)]}
    for name,n in [("final64_warm.xml",64),("final64_cold.xml",64),("exact_restored_green.xml",1)]:
        courts["estate_binding_followup/"+name]=xml("estate_binding_followup/"+name,n)
    native=json.loads((R/"evidence/native_sourcefree_execution.json").read_text())
    for k,d in native.items():
        assert len(d["receipts"])==3 and all(r["state"]=="COMPLETED" for r in d["receipts"])
        assert d["m1_consumer_positive"]["semantic_fields"]["adjudication_outcome"]=="RULE_SATISFIED"
        assert d["m1_consumer_prerequisite_unknown"]["semantic_fields"]["adjudication_outcome"]=="UNRESOLVED"
    cold=json.loads((R/"evidence/cold_identity_comparison.json").read_text())
    assert cold["all_equal"] and not cold["git_present"]
    assert json.loads((R/"evidence/proof_witness.json").read_text())["claims"][0]["fault_probe"]=="TARGET_ASSERTION_FAILED"
    for name in ["proof_witness.json","cold_proof_witness.json","inherited_descriptor_witness.json"]:
        assert json.loads((R/"evidence/estate_binding_followup"/name).read_text())["claims"][0]["fault_probe"]=="TARGET_ASSERTION_FAILED"
    estate=json.loads((R/"evidence/estate_binding_followup/native_estate_fixture.json").read_text())
    assert estate["original_measured"]==0 and estate["native_packet_count"]==3
    assert estate["independent_expected_packet_keys"]==estate["actual_native_packet_keys"]
    report=dict(state="VERIFIED_SOURCEFREE_NATIVE_AND_ORIGINAL35_ACCOUNTING__ORIGINAL_SCIENCE_INCOMPLETE",
        original_measured=0,original_U=None,original_E_pre=None,anti_join=anti,courts=courts,
        cold_identity_files=cold["files"],new_scientific_permission_issued=False,
        estate_binding_followup="64 current tests warm/cold; complete permitted packet census and original-wave/native-universe binding. Sourcefree fixture receipts never count as original measurements.",
        historical_program_reds="Old J-on-P2:20 and K-on-P3:10 remain recorded against old owners; current successor transports44/11 pass. First ENOSPC-contaminated runs are retained and not counted as passed.")
    (R/"evidence/VERIFICATION.json").write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print(json.dumps(report,sort_keys=True))


if __name__=="__main__":main()
