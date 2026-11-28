"""R23: actual expressive afterlife -> visitor exposure -> continuing actor.

Read-only specialist instrumentation of the existing R35 owner course.
No model-facing packet is constructed from the private MII witness.
No new expression grammar, narrator, world or actor policy.
"""
import argparse
from collections import Counter
from pathlib import Path
import subprocess
import sys
from time import perf_counter_ns
from unittest.mock import patch

from um_sorok_organism.inference_lab import (
    WorkloadCapture, verify_workload, compare_frozen, save_report, _local_read, size)
from um_sorok_organism.types import canonical, copy, digest
from inference_lab_cli import fixture_arms

REPO=Path(__file__).resolve().parents[3]
NEIGHBOR="SEAM/NEIGHBORMULCH"
R3="SEAM/ORACLE/UM_SOROK_ORGANISM_R3"
PINS={
    NEIGHBOR+"/tests/test_neighbor_expressive_reentry_r35.py":"f45fa64c4a2780ceb8ef09a54e72a281b0c57ea5",
    NEIGHBOR+"/neighbor_runtime.py":"a38244acd9282fcd960f9aab1437a502d8593ada",
    R3+"/um_sorok_organism/runtime.py":"e31cc5caf60a926aacfe683c697e5fcd1d0f5cea",
    R3+"/um_sorok_organism/semantics.py":"3dd67a27b1cc02df68808f32318a9ace7c583fb5",
    "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/mii.py":"5d0a816a6fe298beb7eac23baed0129ca72669c0",
}
ARMS={"acquired":{},"unheard":{"visitor_hears":False},
      "unacquired":{"learn":False},"unaddressed":{"acknowledge":False}}

def source_pins():
    for path,expected in PINS.items():
        actual=subprocess.check_output(["git","-C",str(REPO),"hash-object",str(REPO/path)],text=True).strip()
        if actual!=expected:raise ValueError("R23_INHERITED_SOURCE_DRIFT:"+path)
    return copy(PINS)

def _fixture():
    tests=REPO/NEIGHBOR/"tests"
    if str(tests) not in sys.path:sys.path.insert(0,str(tests))
    import test_neighbor_expressive_reentry_r35 as owner
    return owner

def _state(rt):
    return digest({"world":rt.ledger.world(),"actors":rt.ledger.actors()})

class _Call:
    def __init__(self,fn):self.fn=fn
    def propose(self,task,packet):return self.fn(task,packet)

def capture_surface(head,arm="acquired"):
    pins=source_pins();owner=_fixture()
    if arm not in ARMS:raise ValueError("R23_ARM")
    cap=WorkloadCapture(source_head=head,fixture="R35_SURFACE_"+arm,
        sourcefree_fixture_attested=True)
    calls=Counter();steps=[];surfaces=[]
    original_proposal=owner.ValidatingSemanticService.proposal
    original_step=owner.ConstitutiveRuntime.step
    original_surface=owner.NeighborEncounter.private_surface
    original_mii=owner.mii.surface
    def proposal(service,task,packet):
        calls[task]+=1
        if task!="expression":return original_proposal(service,task,packet)
        return cap.invoke(_Call(lambda t,p:original_proposal(service,t,p)),task,packet)
    def step(rt,*args,**kwargs):
        start=len(cap.rows)
        result=original_step(rt,*args,**kwargs)
        if len(cap.rows)!=start+1:raise ValueError("R23_EXPRESSION_PER_STEP")
        event=rt.ledger.latest_event()
        if (event["id"]!=result["receipt"] or event["kind"]!="ACTOR_LIFE_TRANSITION"):
            raise ValueError("R23_EVENT_BINDING")
        steps.append({"seq":start,"event":copy(event),"result":copy(result)})
        return result
    def surface(neighbor,profile,*args,**kwargs):
        rt=neighbor.runtime;before=_state(rt);event=copy(rt.ledger.latest_event())
        inputs=[];n=sum(calls.values());p0=len(profile["exposures"])
        def mii_surface(*a,**kw):
            start=perf_counter_ns()
            value=original_mii(*a,**kw)
            inputs.append({"args":copy(list(a)),"kwargs":copy(kw),"value":copy(value),
                           "elapsed_ns":perf_counter_ns()-start})
            return value
        start=perf_counter_ns()
        with patch.object(owner.mii,"surface",new=mii_surface):
            view=original_surface(neighbor,profile,*args,**kwargs)
        duration=perf_counter_ns()-start
        if before!=_state(rt) or rt.ledger.latest_event()!=event:
            raise ValueError("R23_SURFACE_WROTE_OWNER")
        if len(inputs)!=1 or sum(calls.values())!=n:
            raise ValueError("R23_SURFACE_BOUNDARY")
        if not rt.verify()["valid"]:raise ValueError("R23_CHAIN_INVALID")
        surfaces.append({"event":event,"state_sha256":before,"view":copy(view),
            "mii_local_trace":inputs[0],"exposure_count_before":p0,
            "exposure_count_after":len(profile["exposures"]),
            "semantic_calls":sum(calls.values())-n,"elapsed_ns":duration})
        return view
    with patch.object(owner.ValidatingSemanticService,"proposal",new=proposal),\
         patch.object(owner.ConstitutiveRuntime,"step",new=step),\
         patch.object(owner.NeighborEncounter,"private_surface",new=surface):
        outcome=owner.ExpressiveReentryR35().course(**ARMS[arm])
    witness={"schema":"R23_LOCAL_SURFACE_WITNESS_V1","source_head":head,
        "source_pins":pins,"arm":arm,"steps":steps,"surfaces":surfaces,
        "course_outcome":outcome,"task_counts":dict(calls)}
    document=cap.document(owner_state_sha256=digest(witness))
    return document,witness,verify_surface(document,witness,source_head=head)

def verify_surface(document,witness,*,source_head):
    p=verify_workload(document,source_head=source_head)
    arm=witness.get("arm")
    if (arm not in ARMS or p["fixture"]!="R35_SURFACE_"+arm
            or p["owner_state_sha256"]!=digest(witness)
            or witness.get("source_head")!=source_head
            or witness.get("source_pins")!=PINS
            or witness.get("schema")!="R23_LOCAL_SURFACE_WITNESS_V1"):
        raise ValueError("R23_WITNESS_BINDING")
    rows=p["rows"];steps=witness["steps"];surfaces=witness["surfaces"]
    if (len(steps)!=len(rows) or len(surfaces)!=1
            or witness["task_counts"].get("expression")!=len(rows)):
        raise ValueError("R23_CAPTURE_COVERAGE")
    for i,(row,step) in enumerate(zip(rows,steps)):
        packet=row["packet"];result=step["result"];event=step["event"]
        if (step["seq"]!=i or row["task"]!="expression"
                or set(packet)!={"actor_id","actual","actor_accessible","restriction"}
                or packet["restriction"]!="NO_INNER_PSYCHIC_OMNISCIENCE"
                or packet["actor_id"]!=event["actor_id"]
                or result["receipt"]!=event["id"] or result["clock"]!=event["clock"]
                or result["actor"]!=packet["actor_id"]
                or packet["actual"]["action"]!=result["attempt"]
                or packet["actual"]["status"]!=result["status"]
                or row["proposal"].get("surface")!=result["public_tip"]):
            raise ValueError("R23_EXPRESSION_EVENT_MISMATCH")
    surface=surfaces[0];view=surface["view"];trace=surface["mii_local_trace"]
    matched=[s for s in steps if s["event"]==surface["event"]]
    if len(matched)!=1 or matched[0]["result"]["attempt"]!="SPEAK":
        raise ValueError("R23_SURFACE_EVENT_MISMATCH")
    if (surface["semantic_calls"]!=0 or trace["value"]["mandatory"]!=view["mandatory"]
            or trace["value"]["optional"]!=view["optional"]):
        raise ValueError("R23_MII_PRESENTATION_MISMATCH")
    signs=[s for s in view["mandatory"] if s["kind"]=="CO_PUBLIC_OCCURRENCE"
           and s.get("modality")=="auditory"]
    out=witness["course_outcome"]
    if bool(signs)!=out["heard"] or len(signs)>1:
        raise ValueError("R23_AUDITORY_ACCESS_MISMATCH")
    if signs:
        sign=signs[0]
        if (sign["source_event_ref"]!=surface["event"]["id"]
                or sign["speaker_identity"]!="NOT_ESTABLISHED"
                or sign["lexical_content"]!="NOT_CAPTURED_OR_RECONSTRUCTED"
                or sign["text"]!=("Speech with brief pauses." if out["cadence"]=="HALTING"
                                 else "Speech sounds nearby.")):
            raise ValueError("R23_TYPED_SIGN_MISMATCH")
    if "private unease" in canonical(view):
        raise ValueError("R23_HIDDEN_FORM_DISCLOSURE")
    # Use the existing exact F/E adapter only for the actual actor packet.
    # MII is a deterministic owner reader, not a model workload.
    seq=matched[0]["seq"]
    comparison=compare_frozen(document,fixture_arms(document),sequence_ids=[seq])
    if any(x["outcome"]!="PROPOSAL_RETURNED" or not x["equals_recorded_proposal"]
           for x in comparison["observations"]):
        raise ValueError("R23_EXPRESSION_REPLAY")
    return {"schema":"R23_ACTUAL_SURFACE_INTAKE_V1","source_head":source_head,
        "arm":arm,"workload_sha256":document["sha256"],"witness_sha256":p["owner_state_sha256"],
        "task_counts":witness["task_counts"],"expression_calls":len(rows),
        "expression_packet_bytes":sum(size(r["packet"]) for r in rows),
        "target_expression_seq":seq,"target_expression_packet_bytes":size(rows[seq]["packet"]),
        "target_expression_proposal_bytes":size(rows[seq]["proposal"]),
        "F_E_wire_bytes":{x["arm"]:x["metric"]["request_bytes"] for x in comparison["observations"]},
        "target_typed_auditory_sign_count":len(signs),
        "visitor_view_bytes":size(view),"mii_local_input_bytes":size(trace["kwargs"]),
        "mii_surface_ns":trace["elapsed_ns"],"visitor_total_surface_ns":surface["elapsed_ns"],
        "visitor_surface_semantic_calls":0,"course_outcome":out,
        "scope":"HERMETIC_EXISTING_OWNER_COURSE_NOT_TYPED_SPEECH_GENERATION",
        "provider_tokens":None,"network_calls":0}

def main(argv=None):
    from inference_lab_cli import checkout_head
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arm",choices=list(ARMS),default="acquired")
    for name in ("workload","witness","report"):parser.add_argument("--"+name,required=True)
    parser.add_argument("--verify",action="store_true")
    a=parser.parse_args(argv);head=checkout_head();source_pins()
    if a.verify:
        report=verify_surface(_local_read(a.workload),_local_read(a.witness),source_head=head)
    else:
        paths=[Path(x).resolve() for x in (a.workload,a.witness,a.report)]
        if len(set(paths))!=3 or any(x.exists() for x in paths):
            raise ValueError("R23_FRESH_DISTINCT_OUTPUTS_REQUIRED")
        doc,witness,report=capture_surface(head,a.arm)
        save_report(a.workload,doc);save_report(a.witness,witness)
    save_report(a.report,report);print(canonical(report))

if __name__=="__main__":main()
