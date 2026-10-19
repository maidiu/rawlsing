"""Run each currently issued original-wave workload through the native ingress.

The --runtime module is installed by the competent deployment/source operator,
not loaded from an untrusted request or checkpoint. It supplies authenticated
resolver, qualified source_factory, host, purpose and an atlas_id->native packet
mapping. The resolver also supplies an independent current permitted-packet
census. This command neither generates nor signs those scientific objects.
No runtime is supplied in this return because no original grants were issued.
"""
import argparse,importlib,json,sys
from pathlib import Path

R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R.parents[1]))
from rawlsing_next.pre553_issued_workload import (
    execute_issued_workload, WorkloadAdmissionError, IssuedEstateFrontier,
    reconcile_estate_workloads,
)


def execute_current_permitted(waves, runtime=None, *, allow_test_only=False):
    expected={w["atlas_id"] for w in waves};rows=[]
    prepared=()
    frontier=None
    if runtime is not None:
        if not hasattr(runtime.resolver,"resolve_estate_frontier"):
            raise WorkloadAdmissionError("INDEPENDENT_CURRENT_PERMITTED_PACKET_FRONTIER_REQUIRED")
        frontier=runtime.resolver.resolve_estate_frontier()
        if not isinstance(frontier,IssuedEstateFrontier):
            raise WorkloadAdmissionError("AUTHENTICATED_ESTATE_FRONTIER_REQUIRED")
        scopes={"ORIGINAL_SOURCE_CURRENT_SCHEDULE"}
        if allow_test_only:scopes.add("TEST_ONLY_SOURCEFREE")
        if frontier.scope not in scopes or frontier.currentness!="CURRENT":
            raise WorkloadAdmissionError("CURRENT_ESTATE_FRONTIER_REQUIRED")
        if (frontier.host,frontier.purpose)!=(runtime.host,runtime.purpose):
            raise WorkloadAdmissionError("ESTATE_FRONTIER_HOST_PURPOSE_MISMATCH")
        prepared=reconcile_estate_workloads(waves,runtime.workloads,frontier)

    def check_current_frontier():
        if runtime.resolver.resolve_estate_frontier()!=frontier:
            raise WorkloadAdmissionError("ESTATE_FRONTIER_CHANGED_DURING_EXECUTION")

    def source_factory(ref):
        check_current_frontier()
        return runtime.source_factory(ref)

    for w in waves:
        atlas=w["atlas_id"]
        selected=[(wave,packet) for wave,packet in prepared if wave.atlas_id==atlas]
        if not selected:
            rows.append(dict(atlas_id=atlas,state="NOT_YET_ISSUED",native_manifest=None,
                owner_decisions=[atlas+":"+c for c in ["SOURCE_HOST_PURPOSE","COMPLETE_NATIVE_U","RESPONSE_ROUTING_CARRIER","SCIENTIFIC_E_PRE","CONSUMER_PURPOSE"]]))
            continue
        packets=[]
        for wave,workload in selected:
            try:
                check_current_frontier()
                result=execute_issued_workload(workload,runtime.resolver,
                    source_factory=source_factory,host=runtime.host,purpose=runtime.purpose,
                    expected_wave=wave,allow_test_only=allow_test_only)
                check_current_frontier()
            except WorkloadAdmissionError as exc:
                packets.append(dict(state="HOLD__NAMED_OWNER_DECISION",native_manifest=None,
                    decision_ref=workload.decision_ref.as_dict(),reason=str(exc)))
                continue
            # Native source/validation failures propagate, rather than becoming a grant HOLD.
            packets.append(dict(state="NATIVE_COMPLETED",scope=result.scope,
                original_wave_identity=dict(atlas_id=wave.atlas_id,dataset_id=wave.dataset_id,
                    source_family=wave.source_family,wave=wave.wave),
                decision_ref=result.decision_ref.as_dict(),envelope_sha256=result.envelope_sha256,
                native_manifest=result.manifest.semantic_projection(),manifest_ref=result.manifest.manifest_ref.as_dict(),
                receipts=[r.projection() for r in result.receipts],output_refs=[r.as_dict() for r in result.output_refs]))
            if hasattr(runtime,"persist_native_result"):
                runtime.persist_native_result(atlas,result)
        completed=all(p["state"]=="NATIVE_COMPLETED" for p in packets)
        rows.append(dict(atlas_id=atlas,state="NATIVE_COMPLETED" if completed else "HOLD__NAMED_OWNER_DECISION",
            native_manifest=packets[0]["native_manifest"] if len(packets)==1 else None,native_packets=packets))
    if {r["atlas_id"] for r in rows}!=expected or len(rows)!=35:raise ValueError("ALL35_NO_DROP")
    result=dict(schema="U43_CURRENT_PERMITTED_NATIVE_EXECUTION@2",waves=rows,
        estate_frontier_ref=None if frontier is None else frontier.frontier_ref.as_dict(),
        expected_permitted_packet_count=None if frontier is None else len(frontier.expected_workloads),
        original_measured_wave_count=sum(any(p.get("scope")=="ORIGINAL_SOURCE_GRANTED" and
            p["state"]=="NATIVE_COMPLETED" for p in r.get("native_packets",())) for r in rows),
        runtime_issuance_status=("NO_AUTHENTICATED_ORIGINAL_RUNTIME_PROVIDED" if runtime is None else
            "TEST_ONLY_SOURCEFREE_RUNTIME" if frontier.scope=="TEST_ONLY_SOURCEFREE" else "EXTERNALLY_PROVISIONED_NATIVE_RUNTIME"),
        U_E_pre_count=None if runtime is None else "SEE_AUTHENTICATED_PER_WAVE_EXPECTED_JOBS",
        all_supplied_wave_runs_completed=bool(prepared) and all(p["state"]=="NATIVE_COMPLETED"
            for r in rows for p in r.get("native_packets",())),
        is_scientific_completion=False,
        scientific_acceptance="REQUIRES_SEPARATE_COMPETENT_ADJUDICATION")
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--runtime",help="Trusted issuer/deployment-provisioned Python module")
    parser.add_argument("--output",type=Path,required=True,help="Aggregate receipt output; never raw rows")
    args=parser.parse_args()
    waves=json.loads((R/"original35_wave_execution_manifest.json").read_text())
    runtime=importlib.import_module(args.runtime) if args.runtime else None
    result=execute_current_permitted(waves,runtime)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps(dict(waves=len(result["waves"]),measured=result["original_measured_wave_count"],status=result["runtime_issuance_status"])))


if __name__=="__main__":main()
