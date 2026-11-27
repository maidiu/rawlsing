"""Owner-supplied R54 fixture -> private local workload and actual exact replay.

Run from the R3 directory. This is research tooling, never an app/runtime default.
No live calls in capture or replay; no data from real people/survey respondents.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

from um_sorok_organism.inference_lab import (
    WorkloadCapture, CaptureProvider, ExactTapeProvider, verify_workload,
    load_workload, compare_frozen, save_report, LiveBudget, BudgetedLiveProvider,
    BudgetStop, selected_rows)
from um_sorok_organism.live_psychological_llm import (
    ExplicitJSONLLMProvider, _expand_exact_aliases, _expand_structured_fields)
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import canonical, digest


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
        rt=ConstitutiveRuntime(db)
        try:
            audit=rt.verify()
            if not audit["valid"]:raise ValueError("LAB_OWNER_CHAIN_INVALID")
            return {"first":first,"world":rt.ledger.world()[1],
                    "actors":rt.ledger.actors(),"events":rt.ledger.events(),
                    "audit":audit}
        finally:rt.close()


def capture_course(release,head):
    owner=_owner()
    original=owner.CallbackLLMProvider
    cap=WorkloadCapture(source_head=head,fixture="R54_RELEASED" if release else "R54_RETAINED",
                        sourcefree_fixture_attested=True)
    actual=owner_course(release,lambda cb:CaptureProvider(original(cb),cap))
    return cap.document(owner_state_sha256=digest(actual)),actual


def replay_course(document,head):
    p=verify_workload(document,source_head=head)
    if p["fixture"] not in ("R54_RELEASED","R54_RETAINED"):
        raise ValueError("LAB_UNKNOWN_OWNER_FIXTURE")
    # Match original CallbackLLMProvider's grade semantics exactly, but never
    # present this replay as live inference.
    original_grade=getattr(_owner().CallbackLLMProvider,"grade",
                          "UNSPECIFIED_SEMANTIC_ADAPTER_NO_PROVEN_GRADE")
    replay=ExactTapeProvider(document,source_head=head,original_grade=original_grade)
    actual=owner_course(p["fixture"]=="R54_RELEASED",lambda cb:replay)
    replay.finish()
    if p["owner_state_sha256"]!=digest(actual):
        raise ValueError("LAB_OWNER_STATE_REPLAY_MISMATCH")
    return actual


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


def live_arms(config,budget):
    if type(config) is not list or not config:raise ValueError("LAB_NO_LIVE_ARMS")
    arms={}
    for row in config:
        if set(row)-{"name","endpoint","model","key_env","compiled","completion_limit_field"}:
            raise ValueError("LAB_UNKNOWN_LIVE_ARM_FIELD")
        name=row["name"]
        if name in arms:raise ValueError("LAB_DUPLICATE_ARM")
        if type(row["compiled"]) is not bool:raise ValueError("LAB_INVALID_COMPILED_FLAG")
        arms[name]=BudgetedLiveProvider(budget=budget,endpoint=row["endpoint"],
              model=row["model"],api_key=os.environ[row["key_env"]],
              allow_private_actor_data=True,metrics_capacity=1,
              compact_exact_packet=row["compiled"],compact_structured_packet=row["compiled"],
              profile_semantic_demand=True,
              completion_limit_field=row.get("completion_limit_field","max_completion_tokens"))
    return arms


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    subs=parser.add_subparsers(dest="mode",required=True)
    c=subs.add_parser("capture");c.add_argument("--released",action="store_true")
    c.add_argument("--out",required=True)
    for mode in ("replay","compare-fixture","compare-live"):
        p=subs.add_parser(mode);p.add_argument("--workload",required=True)
        if mode!="replay":
            p.add_argument("--out",required=True);p.add_argument("--per-task",type=int,default=1)
            p.add_argument("--task",action="append")
        if mode=="compare-live":
            p.add_argument("--config",required=True);p.add_argument("--budget-journal",required=True)
            p.add_argument("--authorize-sourcefree-live",action="store_true")
    a=parser.parse_args(argv);head=checkout_head()
    if a.mode=="capture":
        doc,state=capture_course(a.released,head)
        save_report(a.out,doc)
        print(canonical({"workload_sha256":doc["sha256"],"source_head":head,
                         "rows":len(doc["payload"]["rows"]),"state_digest":digest(state),
                         "network_calls":0}))
        return
    doc=load_workload(a.workload,source_head=head)
    if a.mode=="replay":
        state=replay_course(doc,head)
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
        if doc["payload"]["fixture"] not in ("R54_RELEASED","R54_RETAINED"):
            raise ValueError("LAB_LIVE_UNRECOGNIZED_FIXTURE")
        # Reexecute the known owner course with exact tape inputs before any
        # remote disclosure. This is an integrity check, not human-data detection.
        replay_course(doc,head)
        with open(a.config,encoding="utf-8") as f:config=json.load(f)
        if set(config)!={"arms","budget"}:raise ValueError("LAB_CONFIG_SHAPE")
        budget=LiveBudget(journal=a.budget_journal,sourcefree_live_authorized=True,
                          **config["budget"])
        arms=live_arms(config["arms"],budget)
        planned=len(selected_rows(doc,per_task=a.per_task,tasks=a.task))*len(arms)
        if planned>budget.max_calls or planned*budget.reserve>budget.max_budget:
            raise ValueError("LAB_PLAN_EXCEEDS_AUTHORIZED_RESERVATIONS")
        result=compare_frozen(doc,arms,per_task=a.per_task,tasks=a.task)
        result["mode"]="EXPLICIT_SOURCEFREE_LIVE_PROPOSAL_ONLY"
        result["budget"]=budget.snapshot()
        # Never save API key or arbitrary upstream response in the journal.
        result["models"]={k:{"model":v.model,"endpoint":v.endpoint,
                  "compiled":v.compact_exact_packet,
                  "completion_limit_field":v.completion_limit_field} for k,v in arms.items()}
    save_report(a.out,result)
    print(canonical({"scope":result["scope"],"mode":result["mode"],
                     "status":result["status"],"observations":len(result["observations"]),
                     "totals":result["totals"],"budget":result.get("budget")}))


if __name__=="__main__":main()
