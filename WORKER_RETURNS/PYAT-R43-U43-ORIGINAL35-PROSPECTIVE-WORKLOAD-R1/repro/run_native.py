"""Actual sourcefree Route B and M1 execution; output is explicitly not original35."""
from dataclasses import asdict
import importlib.util
import json
from pathlib import Path
import sys

R=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(R.parents[1]),str(R/"tests")]
from test_issued_workload import fixture,execute
from rawlsing_next.pre553_issued_workload import material


def main():
    spec=importlib.util.spec_from_file_location("inherited_wg0r_transport",R/"inputs/wg0x/reused_wg0r_fixture.py")
    inherited=importlib.util.module_from_spec(spec);spec.loader.exec_module(inherited)
    outputs={}
    for name,args in [("maximal",{}),("missing_weight",{"missing_weight":True}),("valid_empty",{"valid_empty":True})]:
        fx,p,resolver=fixture(**args)
        result=execute(p,resolver,fx)
        route=result.route_results[0]
        positive=inherited.learned_consumer(route)
        held=inherited.learned_consumer(route,unknown=True)
        outputs[name]=dict(scope="TEST_ONLY_SOURCEFREE__NO_ORIGINAL_SOURCE_GRANT",expected_jobs=resolver.record.expected_jobs,
            actual_jobs=[(u.job_kind,u.job_ref.as_dict()) for u in result.manifest.units],
            descriptor_sha256=result.envelope_sha256,decision_ref=result.decision_ref.as_dict(),
            manifest=result.manifest.semantic_projection(),manifest_hash=result.manifest.manifest_hash,
            receipts=[r.projection() for r in result.receipts],summary=asdict(result.summary),
            requests=[r.as_dict() for r in p.requests],
            i03_facts=[material(f) for out in route.i03_results for f in out.facts],
            i05_receipts=[material(r) for r in route.i05_result.receipts],
            route_b_replay_receipt=route.replay_receipt,
            native_graph=material(route.object_graph),
            m1_consumer_positive=material(positive),m1_consumer_prerequisite_unknown=material(held))
        assert len(result.manifest.units)==len(result.receipts)==3
        assert all(r.state=="COMPLETED" for r in result.receipts)
    path=R/"evidence/native_sourcefree_execution.json"
    path.write_text(json.dumps(material(outputs),sort_keys=True,indent=2)+"\n")
    print(json.dumps({k:dict(units=len(v["receipts"]),consumer=v["m1_consumer_positive"]["semantic_fields"]["adjudication_outcome"],unknown=v["m1_consumer_prerequisite_unknown"]["semantic_fields"]["adjudication_outcome"]) for k,v in outputs.items()},sort_keys=True))


if __name__=="__main__":main()
