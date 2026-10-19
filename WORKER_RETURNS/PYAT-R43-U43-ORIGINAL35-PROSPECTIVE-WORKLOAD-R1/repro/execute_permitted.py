"""Run each currently issued original-wave workload through the native ingress.

The --runtime module is installed by the competent deployment/source operator,
not loaded from an untrusted request or checkpoint. It supplies authenticated
resolver, qualified source_factory, host, purpose and an atlas_id->NativeWorkload
mapping. This command neither generates nor signs those scientific objects.
No runtime is supplied in this return because no original grants were issued.
"""
import argparse,importlib,json,sys
from pathlib import Path

R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R.parents[1]))
from rawlsing_next.pre553_issued_workload import execute_issued_workload,WorkloadAdmissionError


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--runtime",help="Trusted issuer/deployment-provisioned Python module")
    parser.add_argument("--output",type=Path,required=True,help="Aggregate receipt output; never raw rows")
    args=parser.parse_args()
    waves=json.loads((R/"original35_wave_execution_manifest.json").read_text())
    expected={w["atlas_id"] for w in waves};rows=[]
    runtime=importlib.import_module(args.runtime) if args.runtime else None
    permitted={} if runtime is None else runtime.workloads
    if not set(permitted)<=expected:raise ValueError("UNEXPECTED_WAVE_OUTSIDE_ORIGINAL35")
    for w in waves:
        atlas=w["atlas_id"]
        if atlas not in permitted:
            rows.append(dict(atlas_id=atlas,state="NOT_YET_ISSUED",native_manifest=None,
                owner_decisions=[atlas+":"+c for c in ["SOURCE_HOST_PURPOSE","COMPLETE_NATIVE_U","RESPONSE_ROUTING_CARRIER","SCIENTIFIC_E_PRE","CONSUMER_PURPOSE"]]))
            continue
        workload=permitted[atlas]
        try:
            result=execute_issued_workload(workload,runtime.resolver,
                source_factory=runtime.source_factory,host=runtime.host,purpose=runtime.purpose)
        except WorkloadAdmissionError as exc:
            rows.append(dict(atlas_id=atlas,state="HOLD__NAMED_OWNER_DECISION",native_manifest=None,reason=str(exc)))
            continue
        # Native source/validation failures propagate, rather than becoming a grant HOLD.
        rows.append(dict(atlas_id=atlas,state="NATIVE_COMPLETED",scope=result.scope,
            decision_ref=result.decision_ref.as_dict(),envelope_sha256=result.envelope_sha256,
            native_manifest=result.manifest.semantic_projection(),manifest_ref=result.manifest.manifest_ref.as_dict(),
            receipts=[r.projection() for r in result.receipts],output_refs=[r.as_dict() for r in result.output_refs]))
        if hasattr(runtime,"persist_native_result"):
            runtime.persist_native_result(atlas,result)
    if {r["atlas_id"] for r in rows}!=expected or len(rows)!=35:raise ValueError("ALL35_NO_DROP")
    result=dict(schema="U43_CURRENT_PERMITTED_NATIVE_EXECUTION@1",waves=rows,
        original_measured_wave_count=sum(r["state"]=="NATIVE_COMPLETED" for r in rows),
        runtime_issuance_status="NO_AUTHENTICATED_ORIGINAL_RUNTIME_PROVIDED" if runtime is None else "EXTERNALLY_PROVISIONED_NATIVE_RUNTIME",
        U_E_pre_count=None if runtime is None else "SEE_AUTHENTICATED_PER_WAVE_EXPECTED_JOBS",
        all_supplied_wave_runs_completed=all(r["state"]=="NATIVE_COMPLETED" for r in rows),
        is_scientific_completion=False,
        scientific_acceptance="REQUIRES_SEPARATE_COMPETENT_ADJUDICATION")
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps(dict(waves=len(rows),measured=result["original_measured_wave_count"],status=result["runtime_issuance_status"])))


if __name__=="__main__":main()
