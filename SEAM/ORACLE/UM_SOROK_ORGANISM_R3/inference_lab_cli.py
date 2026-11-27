"""Owner-supplied R54 fixture -> private local workload and actual exact replay.

Run from the R3 directory. This is research tooling, never an app/runtime default.
No live calls in capture or replay; no data from real people/survey respondents.
"""
import argparse
from contextlib import nullcontext
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

from um_sorok_organism.inference_lab import (
    WorkloadCapture, CaptureProvider, ExactTapeProvider, verify_workload,
    load_workload, compare_frozen, save_report, _local_read)
from um_sorok_organism import runtime as runtime_module
from um_sorok_organism.inference_lab_admission import AdmissionCapture, evaluate_admissions
from um_sorok_organism.inference_lab_campaign import build_plan, execute_plan
from um_sorok_organism.live_psychological_llm import (
    ExplicitJSONLLMProvider, _expand_exact_aliases, _expand_structured_fields)
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import canonical, copy, digest


def checkout_head():
    root=Path(__file__).resolve().parent
    def git(*args):
        return subprocess.check_output(["git","-C",str(root),*args],text=True).strip()
    if git("status","--porcelain","--untracked-files=no"):
        raise ValueError("LAB_CLEAN_TRACKED_CHECKOUT_REQUIRED")
    return git("rev-parse","HEAD")


def _owner():
    tests=Path(__file__).resolve().parent/"tests"
    if str(tests) not in sys.path:sys.path.insert(0,str(tests))
    import test_released_attention_r54 as owner
    return owner


def owner_course(release,provider_factory):
    """Owner's original performed trajectory; no new policy or semantic oracle."""
    owner=_owner()
    with tempfile.TemporaryDirectory() as tmp:
        db=Path(tmp)/"life.sqlite"
        with patch.object(owner,"CallbackLLMProvider",side_effect=provider_factory):
            first=owner.ReleasedAttentionR54().run_arm(db,release)
        # The owner's test observation is a set, not committed runtime state.
        # Canonicalize only this documented fixture observation for the lab.
        first={**first,"focus":sorted(first["focus"])}
        rt=ConstitutiveRuntime(db)
        try:
            audit=rt.verify()
            if not audit["valid"]:raise ValueError("LAB_OWNER_CHAIN_INVALID")
            return {"first":first,"world":rt.ledger.world()[1],
                    "actors":rt.ledger.actors(),"events":rt.ledger.events(),
                    "audit":audit}
        finally:rt.close()


def capture_course(release,head,*,with_admissions=False):
    owner=_owner()
    original=owner.CallbackLLMProvider
    cap=WorkloadCapture(source_head=head,fixture="R54_RELEASED" if release else "R54_RETAINED",
                        sourcefree_fixture_attested=True)
    observer=AdmissionCapture(cap) if with_admissions else None
    admit=runtime_module.admit
    def observe(*args,**kwargs):
        return observer.invoke(admit,*args,**kwargs)
    context=patch.object(runtime_module,"admit",side_effect=observe) if observer else nullcontext()
    with context:
        actual=owner_course(release,lambda cb:CaptureProvider(original(cb),cap))
    doc=cap.document(owner_state_sha256=digest(actual))
    if observer:return doc,actual,observer.document(doc,actual)
    return doc,actual


def replay_course(document,head):
    p=verify_workload(document,source_head=head)
    if p["fixture"] not in ("R54_RELEASED","R54_RETAINED"):
        raise ValueError("LAB_UNKNOWN_OWNER_FIXTURE")
    # Match original CallbackLLMProvider's grade semantics exactly, but never
    # present this replay as live inference.
    original_grade=getattr(_owner().CallbackLLMProvider,"grade",
                          "UNSPECIFIED_SEMANTIC_ADAPTER_NO_PROVEN_GRADE")
    replay=ExactTapeProvider(document,source_head=head,original_grade=original_grade)
    original=_owner().CallbackLLMProvider
    def factory(cb):
        def observe(task,packet):
            recorded=replay.propose(task,packet)
            # The owner fixture has assertion-observation lists populated by
            # its hermetic callback. Preserve them without letting the callback
            # substitute a different decision into the taped trajectory.
            observed=cb(task,copy(packet))
            if observed!=recorded:
                raise ValueError("LAB_OWNER_FIXTURE_DECISION_MISMATCH")
            return recorded
        return original(observe)
    actual=owner_course(p["fixture"]=="R54_RELEASED",factory)
    replay.finish()
    if p["owner_state_sha256"]!=digest(actual):
        raise ValueError("LAB_OWNER_STATE_REPLAY_MISMATCH")
    return actual


def replay_owner_course(document,head):
    if document["payload"]["fixture"]=="R34_ACQUIRED_LIFE_F":
        from inference_lab_r34 import replay_r34
        return replay_r34(document,head)
    return replay_course(document,head)


def fixture_arms(document):
    """Frozen exact-proposal replay, measuring actual adapter request sizes.

    Lookup is by exact task+packet digest; conflicting repeated source
    decisions are refused, not collapsed into a single semantic truth.
    """
    rows=verify_workload(document)["rows"]
    known={}
    for r in rows:
        key=(r["task"],r["packet_digest"])
        if key in known and known[key]!=r["proposal"]:
            raise ValueError("LAB_AMBIGUOUS_RECORDED_PROPOSAL")
        known[key]=r["proposal"]
    def transport(request):
        body=json.loads(request["messages"][1]["content"]);task=body["task"]
        packet=_expand_exact_aliases(task,body["actor_source_packet"],
                                     body.get("same_call_exact_aliases",{}))
        packet=_expand_structured_fields(task,packet,body.get("reconstructed_fields",{}))
        answer=known[(task,digest(packet))]
        return {"choices":[{"message":{"content":canonical(answer)}}]}
    def provider(compiled):
        return ExplicitJSONLLMProvider(endpoint="https://example.invalid/chat/completions",
          model="sourcefree-tape",api_key="not-a-key",allow_private_actor_data=True,
          transport=transport,metrics_capacity=1,compact_exact_packet=compiled,
          compact_structured_packet=compiled,profile_semantic_demand=True)
    return {"F":provider(False),"E":provider(True)}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    subs=parser.add_subparsers(dest="mode",required=True)
    c=subs.add_parser("capture");fixture=c.add_mutually_exclusive_group()
    fixture.add_argument("--released",action="store_true")
    fixture.add_argument("--r34",action="store_true",help="executed R34 full acquired-life course")
    c.add_argument("--out",required=True);c.add_argument("--admissions-out")
    p=subs.add_parser("evaluate-admissions")
    p.add_argument("--workload",required=True);p.add_argument("--witness",required=True)
    p.add_argument("--comparison",required=True);p.add_argument("--out",required=True)
    p=subs.add_parser("plan-live")
    p.add_argument("--workload",required=True);p.add_argument("--config",required=True)
    p.add_argument("--out",required=True);p.add_argument("--per-stratum",type=int,default=3)
    p.add_argument("--task",action="append")
    for mode in ("replay","compare-fixture","compare-live"):
        p=subs.add_parser(mode);p.add_argument("--workload",required=True)
        if mode!="replay":
            p.add_argument("--out",required=True)
        if mode=="compare-fixture":
            p.add_argument("--per-task",type=int,default=1);p.add_argument("--task",action="append")
        if mode=="compare-live":
            p.add_argument("--config",required=True);p.add_argument("--budget-journal",required=True)
            p.add_argument("--plan",required=True);p.add_argument("--observation-log",required=True)
            p.add_argument("--authorize-sourcefree-live",action="store_true")
    a=parser.parse_args(argv);head=checkout_head()
    if a.mode=="capture":
        if Path(a.out).exists() or (a.admissions_out and Path(a.admissions_out).exists()):
            raise ValueError("LAB_OUTPUT_ALREADY_EXISTS")
        if a.r34:
            from inference_lab_r34 import capture_r34
            result=capture_r34(head,with_admissions=bool(a.admissions_out))
        else:
            result=capture_course(a.released,head,with_admissions=bool(a.admissions_out))
        doc,state=result[:2]
        save_report(a.out,doc)
        if a.admissions_out:save_report(a.admissions_out,result[2])
        print(canonical({"workload_sha256":doc["sha256"],"source_head":head,
                         "rows":len(doc["payload"]["rows"]),"state_digest":digest(state),
                         "admission_witnesses":len(result[2]["payload"]["rows"]) if a.admissions_out else 0,
                         "network_calls":0}))
        return
    doc=load_workload(a.workload,source_head=head)
    if a.mode=="plan-live":
        # No credentials, no network. Exact request hashes and byte counts
        # are generated by the existing adapter with a hermetic transport.
        with open(a.config,encoding="utf-8") as f:config=json.load(f)
        plan=build_plan(doc,config,per_stratum=a.per_stratum,tasks=a.task)
        save_report(a.out,plan);p=plan["payload"]
        print(canonical({"plan_sha256":plan["sha256"],"status":p["status"],
            "coverage":p["coverage"],"planned_calls":p["planned_calls"],
            "planned_wire_bytes":p["planned_wire_bytes"],
            "declared_reserve_nanos":p["declared_reserve_nanos"],
            "violations":p["violations"],"network_calls":0}))
        return
    if a.mode=="evaluate-admissions":
        result=evaluate_admissions(doc,_local_read(a.witness),_local_read(a.comparison))
        save_report(a.out,result)
        print(canonical({"scope":result["scope"],"totals":result["totals"],"network_calls":0}))
        return
    if a.mode=="replay":
        state=replay_owner_course(doc,head)
        print(canonical({"workload_sha256":doc["sha256"],"state_digest":digest(state),
                         "exact_tape_replay":True,"network_calls":0}))
        return
    if Path(a.out).exists():raise ValueError("LAB_OUTPUT_ALREADY_EXISTS")
    if a.mode=="compare-fixture":
        arms=fixture_arms(doc)
        result=compare_frozen(doc,arms,per_task=a.per_task,tasks=a.task)
        result["mode"]="HERMETIC_EXACT_TAPE_NOT_LIVE"
    else:
        if not a.authorize_sourcefree_live:raise ValueError("LAB_LIVE_AUTHORIZATION_REQUIRED")
        if doc["payload"]["fixture"] not in ("R54_RELEASED","R54_RETAINED","R34_ACQUIRED_LIFE_F"):
            raise ValueError("LAB_LIVE_UNRECOGNIZED_FIXTURE")
        # Reexecute the known owner course with exact tape inputs before any
        # remote disclosure. This is an integrity check, not human-data detection.
        replay_owner_course(doc,head)
        with open(a.config,encoding="utf-8") as f:config=json.load(f)
        result=execute_plan(doc,config,_local_read(a.plan),journal=a.budget_journal,
            observation_log=a.observation_log,sourcefree_live_authorized=True)
    save_report(a.out,result)
    print(canonical({"scope":result["scope"],"mode":result["mode"],
                     "status":result["status"],"observations":len(result["observations"]),
                     "totals":result["totals"],"budget":result.get("budget")}))


if __name__=="__main__":main()
