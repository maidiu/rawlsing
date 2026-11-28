"""R27: test the specialist transport in unchanged exact owner lexical courts.
Mock answers are the original fixture policy, not model comprehension evidence.
No network, no credentials, no replay of private tapes or new runtime authority.
"""
import argparse
from collections import Counter
import importlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from inference_lab_owner_intake_r25 import PINS, R3, NEIGHBOR, git, need

def court(root, lane, compact):
    head, fixture, blob = PINS[lane]
    need(git(root,"rev-parse","HEAD")==head,"R27_OWNER_HEAD")
    need(not git(root,"status","--porcelain","--untracked-files=no"),"R27_OWNER_DIRTY")
    need(git(root,"hash-object",str(root/fixture))==blob,"R27_FIXTURE_BLOB")
    sys.path[:0]=[str(root/R3),str(root/R3/"tests"),str(root/NEIGHBOR),str(root/NEIGHBOR/"tests")]
    from um_sorok_organism.types import canonical
    from um_sorok_organism.semantics import CallbackLLMProvider
    # The adapter is the exact specialist candidate; owner package is unchanged.
    path=Path(__file__).resolve().parent/"um_sorok_organism/live_psychological_llm.py"
    spec=importlib.util.spec_from_file_location("um_sorok_organism.r27_transport_overlay",path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    owner=importlib.import_module(fixture.stem)
    original=CallbackLLMProvider.propose
    rows=[]
    def through_wire(self,task,packet):
        def mock(req):
            body=json.loads(req["messages"][1]["content"])
            need(body=={"task":task,"actor_source_packet":packet},"R27_PACKET_NOT_EXACT")
            prompt=req["messages"][0]["content"]
            lexical=task=="expression" and packet.get("expression_phase")=="LEXICAL_REALIZATION_BEFORE_EXPERIENCE"
            revaluation=task=="development" and bool(packet.get("historically_possible_lexical_project_revaluations"))
            speak=task=="actor_attempt" and any(type(o) is dict and o.get("action")=="SPEAK" for o in packet.get("options",[]))
            need(("For LEXICAL_REALIZATION_BEFORE_EXPERIENCE return" in prompt)==lexical,"R27_LEXICAL_CLAUSE")
            need(("For historically_possible_lexical_project_revaluations" in prompt)==revaluation,"R27_REVALUATION_CLAUSE")
            need(("For an independently selected eligible SPEAK" in prompt)==speak,"R27_SELECTION_CLAUSE")
            answer=original(self,task,body["actor_source_packet"])
            rows.append({"task":task,"lexical":lexical,"revaluation":revaluation,"speak":speak,
                         "packet_bytes":len(canonical(packet).encode("utf-8")),
                         "request_bytes":len(canonical(req).encode("utf-8")),
                         "response_bytes":len(canonical(answer).encode("utf-8")),
                         "nomination":bool(answer.get("candidates")),
                         "speech_shape":type(answer.get("speech")).__name__ if lexical else None})
            return {"choices":[{"message":{"content":canonical(answer)}}]}
        provider=module.ExplicitJSONLLMProvider(endpoint="https://example.invalid/chat/completions",
                model="sourcefree-fixture-only",api_key="not-a-credential",allow_private_actor_data=True,
                transport=mock,compact_task_prompt=compact,metrics_capacity=1)
        value=provider.propose(task,packet)
        receipt=provider.usage_snapshot()["receipts"][0]
        need(receipt["attempts"]==1 and receipt["transport"]=="MOCK" and
             receipt["request_bytes"]==rows[-1]["request_bytes"] and
             all(v is None for v in receipt["usage"].values()),"R27_RECEIPT")
        return value
    cls=owner.LexicalOccurrenceR39 if lane=="R39" else owner.PolycentricLexicalR40
    with patch.object(CallbackLLMProvider,"propose",new=through_wire):
        result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    need(result.wasSuccessful(),"R27_OWNER_ADMISSION_FAILED")
    need(any(r["lexical"] for r in rows) and any(r["speak"] for r in rows),"R27_MISSING_SPEECH_WORK")
    if lane=="R39":
        need(any(r["speech_shape"]=="dict" for r in rows),"R27_MALFORMED_CONTROL_MISSING")
    else:
        need(any(r["revaluation"] and r["nomination"] for r in rows) and
             any(r["revaluation"] and not r["nomination"] for r in rows),"R27_REVALUATION_CONTROLS")
    return {"owner":head,"lane":lane,"compact":compact,"tests":result.testsRun,
            "calls":len(rows),"task_counts":dict(Counter(r["task"] for r in rows)),
            "lexical":sum(r["lexical"] for r in rows),"revaluation":sum(r["revaluation"] for r in rows),
            "speak_eligible":sum(r["speak"] for r in rows),
            "packet_bytes":sum(r["packet_bytes"] for r in rows),
            "request_bytes":sum(r["request_bytes"] for r in rows),
            "response_bytes":sum(r["response_bytes"] for r in rows),
            "target_request_bytes":sum(r["request_bytes"] for r in rows if r["lexical"] or r["revaluation"]),
            "grade":"MOCK_TRANSPORT_OWNER_ADMISSION_NOT_MODEL_ADEQUACY"}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--owner-root",required=True,type=Path)
    p.add_argument("--lane",required=True,choices=("R39","R40"));a=p.parse_args()
    full=court(a.owner_root.resolve(),a.lane,False);compact=court(a.owner_root.resolve(),a.lane,True)
    for k in ("calls","task_counts","lexical","revaluation","packet_bytes","response_bytes"):
        need(full[k]==compact[k],"R27_PROMPT_VARIANT_CHANGED_FIXTURE_"+k)
    need(compact["request_bytes"]<full["request_bytes"],"R27_NO_REQUEST_REDUCTION")
    print("R27_TRANSPORT "+json.dumps({"full":full,"compact":compact},sort_keys=True))
