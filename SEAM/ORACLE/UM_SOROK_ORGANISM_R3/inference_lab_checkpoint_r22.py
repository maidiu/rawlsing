"""R22: intake the existing protected P2/P3 combined-checkpoint course.

Use the existing actual sourcefree P3 fixture and RecursionCycle. No new
event/psychological owner, provider endpoint, or prospective grammar.
This is a custody/measurement bridge; the historic provider is scripted,
its retrospective impressions do not create P3's computed effects.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from um_sorok_organism.inference_lab import (
    CHECKPOINT_TASK, WorkloadCapture, ExactTapeProvider, verify_workload,
    save_report, _local_read, size)
from um_sorok_organism.types import canonical, copy, digest

REPO=Path(__file__).resolve().parents[3]
P2="WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
P3="WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
PINS={
    P2+"/developmental_recursion/model_cycle.py":"231cab97b4bc5e2f40de3c45d179a68ba58585c5",
    P2+"/developmental_recursion/engine.py":"a777692782003e05de6c46280b5861e97516dc90",
    P2+"/developmental_recursion/p2_owner.py":"3160eb157675453c0bfee5f9bd4b400f9c999c17",
    P3+"/tests/p3_fixture_support.py":"a0c8a999947841e0f7b8082bfc807ffb1af68bbe",
    P3+"/p3/p3_owner.py":"233a89f2cf99c192717cb223a771af47efe3bbd2",
}
FIXTURE="P3_TWO_BATCH_PRIMARY"
MODES=("BOOTSTRAP","ORDINARY","TERMINAL")


def source_pins():
    for path,expected in PINS.items():
        actual=subprocess.check_output(["git","-C",str(REPO),"hash-object",str(REPO/path)],
                                      text=True).strip()
        if actual!=expected:raise ValueError("R22_INHERITED_SOURCE_DRIFT:"+path)
    return copy(PINS)


def _fixture():
    tests=REPO/P3/"tests"
    if str(tests) not in sys.path:sys.path.insert(0,str(tests))
    import p3_fixture_support as owner
    return owner


class CaptureCheckpoint:
    """Adapt CallProvider.call to the existing lab's exact capture facility.

    Neither this wrapper nor the capture provider can write actor/world state.
    Original fixture decides its original scripted response.
    """
    def __init__(self,provider,capture):
        self.provider=provider;self.capture=capture

    def call(self,request):
        return self.capture.invoke(self,CHECKPOINT_TASK,request)

    def propose(self,task,packet):
        if task!=CHECKPOINT_TASK:raise ValueError("R22_TASK")
        return self.provider.call(packet)


def capture_checkpoint(head,*,control=False):
    pins=source_pins();owner=_fixture()
    fixture=FIXTURE+("_CONTROL" if control else "")
    cap=WorkloadCapture(source_head=head,fixture=fixture,
         sourcefree_fixture_attested=True,max_rows=3,max_bytes=8*1024*1024)
    with tempfile.TemporaryDirectory(prefix="rawlsing-p3-checkpoint-") as tmp:
        case=owner.build_case(Path(tmp),**({"history_outcomes":()} if control else {}))
        try:
            case.cycle.provider=CaptureCheckpoint(case.provider,cap)
            start=case.owner.snapshot().document()
            results,timing=owner.run_chain_timed(case)
            if not case.cycle.engine.verify() or not case.owner.store.verify():
                raise ValueError("R22_OWNER_CHAIN_INVALID")
            stop=case.owner.snapshot().document()
            cycle=json.loads(case.cycle_store_path.read_text(encoding="utf-8"))
            # The local owner witness is deliberately separate from the model
            # workload; it includes private objective/readset/effect evidence.
            witness={"schema":"R22_LOCAL_P3_OWNER_WITNESS_V1",
                     "source_head":head,"source_pins":pins,"fixture":fixture,
                     "start":start,"stop":stop,"results":results,"cycle":cycle,
                     "psyche_head":case.owner.store.head()}
            # Use the historical owner measurement API rather than duplicate
            # store/resource accounting. These are local CPU/wall measurements.
            metrics=owner.measure_case(case,results,timing)
            if metrics["provider_calls"]!=len(cap.rows):
                raise ValueError("R22_CALL_COUNT_MISMATCH")
            if metrics["provider_context_bytes"]!=sum(
                len(owner.canonical(r["packet"]).encode("utf-8")) for r in cap.rows):
                raise ValueError("R22_CONTEXT_MEASUREMENT_MISMATCH")
            if case.provider.calls!=[r["packet"] for r in cap.rows]:
                raise ValueError("R22_CAPTURE_INPUT_MISMATCH")
            document=cap.document(owner_state_sha256=digest(witness))
            report=verify_checkpoint(document,witness,source_head=head)
            report["owner_measurement"]=metrics
            return document,witness,report
        finally:
            case.owner.close()


def verify_checkpoint(document,witness,*,source_head):
    p=verify_workload(document,source_head=source_head)
    if (p["fixture"] not in (FIXTURE,FIXTURE+"_CONTROL")
            or len(p["rows"])!=3 or any(r["task"]!=CHECKPOINT_TASK for r in p["rows"])
            or p["owner_state_sha256"]!=digest(witness)
            or witness.get("schema")!="R22_LOCAL_P3_OWNER_WITNESS_V1"
            or witness.get("source_head")!=source_head
            or witness.get("fixture")!=p["fixture"]
            or witness.get("source_pins")!=PINS):
        raise ValueError("R22_WITNESS_BINDING")
    owner=_fixture()
    batches=[witness["results"]["bootstrap"],witness["results"]["ordinary"]]
    if any(len(b["records"])!=3 or b["history_hash"]!=owner.digest(b["records"]) for b in batches):
        raise ValueError("R22_HISTORY_INTEGRITY")
    records=[r for b in batches for r in b["records"]]
    if (records[0]["before"]!=witness["start"] or records[-1]["after"]!=witness["stop"]
            or any(a["after"]!=b["before"] for a,b in zip(records,records[1:]))):
        raise ValueError("R22_SEQUENTIAL_STATE_DISCONTINUITY")
    cyc=witness["cycle"]
    if (cyc["phase"]!="COMPLETE" or cyc["pending"] is not None
            or cyc["model_call"] is not None or cyc["expected_owner_state"]!=witness["stop"]):
        raise ValueError("R22_CYCLE_NOT_COMPLETE")
    tape=ExactTapeProvider(document,source_head=source_head,original_grade="HERMETIC_ONLY")
    rows=[];retro=[]
    for i,r in enumerate(p["rows"]):
        req=r["packet"];ans=tape.propose(CHECKPOINT_TASK,req)
        if set(req)!={"mode","context","previous"} or req["mode"]!=MODES[i]:
            raise ValueError("R22_REQUEST_ABI")
        if set(ans)!={"retrospective","prospective"}:
            raise ValueError("R22_RESPONSE_ABI")
        previous=None if i==0 else batches[i-1]
        expected=None if previous is None else {"batch_id":previous["batch_id"],
            "history_hash":previous["history_hash"],
            "events":[{"event_id":x["event_id"],"accessible":x["accessible"]}
                      for x in previous["records"]]}
        if req["previous"]!=expected:raise ValueError("R22_PRIOR_ACCESS_MISMATCH")
        ret=ans["retrospective"];pros=ans["prospective"]
        if previous is None:
            if ret is not None:raise ValueError("R22_BOOTSTRAP_RETROSPECTION")
        else:
            if (ret["batch_id"]!=expected["batch_id"] or ret["history_hash"]!=expected["history_hash"]
                    or ret["event_ids"]!=[x["event_id"] for x in expected["events"]]):
                raise ValueError("R22_RETROSPECTIVE_SOURCE_MISMATCH")
            retro.append(ret)
        if i==2:
            if pros is not None:raise ValueError("R22_TERMINAL_PROSPECTION")
        else:
            if not 3<=len(pros)<=5:raise ValueError("R22_PROSPECTIVE_COUNT")
            committed=batches[i]["records"]
            if ([x["event_id"] for x in pros]!=[x["event_id"] for x in committed]
                    or any(owner.digest(x)!=y["proposal_hash"] for x,y in zip(pros,committed))):
                raise ValueError("R22_PROSPECTIVE_COMMITMENT_MISMATCH")
        rows.append({"mode":MODES[i],"seq":i,"request_bytes":size(req),
            "previous_accessible_bytes":size(req["previous"]),
            "context_bytes":size(req["context"]),"proposal_bytes":size(ans),
            "retrospective_bytes":size(ret),"prospective_bytes":size(pros),
            "prior_events":0 if previous is None else len(previous["records"]),
            "next_events":0 if pros is None else len(pros),
            "callback_elapsed_ns":r["elapsed_ns"],"packet_digest":r["packet_digest"],
            "provider_tokens":None})
    tape.finish()
    if (cyc["retrospectives"]!=retro or witness["results"]["terminal"]!=retro[-1]
            or cyc["proposed_impressions"]!=[
                {"batch_id":x["batch_id"],"impressions":x["impressions"]} for x in retro]):
        raise ValueError("R22_RECORDED_IMPRESSIONS_MISMATCH")
    # Existing P3 proof's distinction: computational formation is operative
    # before the ordinary checkpoint; a stored impression isn't its producer.
    formation=records[0]["consequences"]["test_only_psychological"]
    recruit=records[1]["consequences"]["test_only_psychological"]
    recruited=[x["record_hash"] for x in recruit["streams"] if x.get("record_hash")]
    if not set(recruited)<=set(records[1]["readset"]):
        raise ValueError("R22_RECRUITMENT_READSET_MISMATCH")
    if p["fixture"]==FIXTURE and len(recruited)!=2:
        raise ValueError("R22_PRIMARY_RECRUITMENT_MISSING")
    if p["fixture"]!=FIXTURE and recruited:
        raise ValueError("R22_CONTROL_RECRUITMENT_UNEXPECTED")
    return {"schema":"R22_CHECKPOINT_INTAKE_RECEIPT_V1","source_head":source_head,
        "workload_sha256":document["sha256"],"local_witness_sha256":p["owner_state_sha256"],
        "scope":"P3_SOURCEFREE_OWNER_EFFECTS_NOT_MODEL_INDUCED",
        "calls":3,"ordinary_calls":1,"event_batches":2,"realized_events":len(records),
        "request_bytes":sum(x["request_bytes"] for x in rows),"rows":rows,
        "first_formation_status":formation["status"],
        "second_event_recruited_records":len(recruited),
        "second_event_modes":[x["mode"] for x in recruit["streams"]],
        "stored_retrospective_proposals":len(retro),
        "local_witness_bytes":size(witness),"provider_tokens":None,"network_calls":0,
        "model_adequacy":"UNTESTED_CONTEXT_AND_RETROSPECTION_FIXTURE_ONLY"}


def main(argv=None):
    from inference_lab_cli import checkout_head
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workload",required=True)
    parser.add_argument("--witness",required=True)
    parser.add_argument("--report",required=True)
    parser.add_argument("--control",action="store_true")
    parser.add_argument("--verify",action="store_true")
    a=parser.parse_args(argv);head=checkout_head();source_pins()
    if a.verify:
        report=verify_checkpoint(_local_read(a.workload),_local_read(a.witness),source_head=head)
    else:
        paths=[Path(x).resolve() for x in (a.workload,a.witness,a.report)]
        if len(set(paths))!=3 or any(x.exists() for x in paths):
            raise ValueError("R22_FRESH_DISTINCT_OUTPUTS_REQUIRED")
        doc,witness,report=capture_checkpoint(head,control=a.control)
        save_report(a.workload,doc);save_report(a.witness,witness)
    save_report(a.report,report)
    print(canonical({k:v for k,v in report.items() if k not in ("owner_measurement","rows")}))


if __name__=="__main__":main()
