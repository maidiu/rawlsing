"""Publish actual TEST_ONLY packet receipts; no original source data or grant."""
import hashlib,json,sys
from pathlib import Path

R=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(R.parents[1]),str(R/"tests"),str(R/"repro")]
from test_estate_execution import estate_fixture
from execute_permitted import execute_current_permitted
from rawlsing_next.pre553_issued_workload import material


def main():
    waves,runtime,declarations,calls,persisted=estate_fixture()
    result=execute_current_permitted(waves,runtime,allow_test_only=True)
    expected={p.decision_ref.key for p in declarations}
    actual={r.decision_ref.key for atlas,r in persisted}
    assert expected==actual and len(calls)==len(persisted)==3
    assert all(len(r.receipts)==3 and r.native_outputs and r.route_results for atlas,r in persisted)
    assert result["original_measured_wave_count"]==0 and result["all_supplied_wave_runs_completed"]
    payload=dict(scope="TEST_ONLY_SOURCEFREE_ROSTER_BINDING_SIMULATION__NOT_ORIGINAL_SOURCE_PERMISSION_OR_MEASUREMENT",
        roster_slots_are_test_assignments=True,original_measured=0,
        independent_expected_packet_keys=sorted(expected),actual_native_packet_keys=sorted(actual),
        native_packet_count=len(persisted),source_factory_call_count=len(calls),
        estate_receipt=result,native=[dict(atlas_id=atlas,scope=r.scope,
            decision_ref=r.decision_ref.as_dict(),manifest=r.manifest.semantic_projection(),
            envelope_sha256=r.envelope_sha256,receipts=[x.projection() for x in r.receipts],
            i03_facts=[material(f) for route in r.route_results for out in route.i03_results for f in out.facts],
            i05_receipts=[material(x) for route in r.route_results for x in route.i05_result.receipts],
            native_output_refs=[x.as_dict() for x in r.output_refs]) for atlas,r in persisted])
    output=R/"evidence/estate_binding_followup/native_estate_fixture.json"
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(payload,sort_keys=True,indent=2)+"\n")
    print(json.dumps(dict(scope=payload["scope"],packets=3,native_batch_receipts=9,original_measured=0,
        sha256=hashlib.sha256(output.read_bytes()).hexdigest())))


if __name__=="__main__":main()
