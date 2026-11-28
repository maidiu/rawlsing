"""R25: measure actual R61/R39 owner courses in separate immutable checkouts.
No owner source edits, live provider invocation, or forced joined runtime.
"""
import argparse
from collections import Counter
from contextlib import ExitStack
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from time import perf_counter_ns
import unittest
from unittest.mock import patch

R3 = Path("SEAM/ORACLE/UM_SOROK_ORGANISM_R3")
NEIGHBOR = Path("SEAM/NEIGHBORMULCH")
PINS = {
    "R61": ("2bef1d25fb6faa87fe9c97656febf4bb92876d83",
            R3 / "tests/test_retrospective_reconstitution_r61.py",
            "616765ede05951e257c8ca8738263f138f21fb49"),
    "R62": ("ee66a124476596ea0464e87ac2839191bdc1d651",
            R3 / "tests/test_existing_family_continuity_r62.py",
            "1d1f4f6aab3f44d79e3ebffbba92165b41d953f4"),
    "R40": ("a95cb4c11cc62d808d5c7780c0326dca00827b91",
            NEIGHBOR / "tests/test_neighbor_polycentric_lexical_r40.py",
            "def6e585079cddb4bda106ae5e1c5f8fd1c33717"),
    "R39": ("4d104a17c4ec9126484faac4e6f13d5050162051",
            NEIGHBOR / "tests/test_neighbor_lexical_occurrence_r39.py",
            "d5f818248dbd82d10a5e87b35c1028b0e322261e"),
}
LAB = Path(__file__).resolve().parent / "um_sorok_organism/inference_lab.py"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def run(root, lane, output=None):
    head, fixture, blob = PINS[lane]
    need(git(root, "rev-parse", "HEAD") == head, "R25_OWNER_HEAD")
    need(not git(root, "status", "--porcelain", "--untracked-files=no"), "R25_OWNER_DIRTY")
    need(git(root, "hash-object", str(root / fixture)) == blob, "R25_FIXTURE_BLOB")
    sys.path[:0] = [str(root/R3), str(root/R3/"tests"), str(root/NEIGHBOR), str(root/NEIGHBOR/"tests")]
    from um_sorok_organism import types
    from um_sorok_organism.runtime import ConstitutiveRuntime
    from um_sorok_organism.semantics import ValidatingSemanticService
    # Reuse existing capture/verification code with exact owner's own types.
    # No specialist adapter is sent or installed into the owner package.
    spec = importlib.util.spec_from_file_location("um_sorok_organism.inference_lab_r25_overlay", LAB)
    lab = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lab)
    owner = importlib.import_module(fixture.stem)
    all_cases = []
    active = None
    proposal0 = ValidatingSemanticService.proposal
    step0 = ConstitutiveRuntime.step

    def begin(name):
        nonlocal active
        active = {"name":name, "cap":lab.WorkloadCapture(source_head=head,
            fixture="R25_"+lane+"_"+name, sourcefree_fixture_attested=True), "steps":[],
            "views":[], "calls":[], "operations":[], "result":None}
        all_cases.append(active)

    class Caller:
        def __init__(self, service): self.service = service
        def propose(self, task, packet): return proposal0(self.service, task, packet)

    def proposal(service, task, packet):
        need(active is not None, "R25_NO_ACTIVE_CASE")
        cap = active["cap"]
        start = perf_counter_ns()
        call = {"task":task, "packet_bytes":lab.size(packet), "seq":len(cap.rows), "status":"STARTED"}
        active["calls"].append(call)
        try:
            answer = cap.invoke(Caller(service), task, packet)
            call["status"] = "RETURNED"
            return answer
        except Exception as exc:
            call["status"] = type(exc).__name__
            raise
        finally:
            call["elapsed_ns"] = perf_counter_ns()-start

    def state(rt):
        return types.digest({"world":rt.ledger.world(),"actors":rt.ledger.actors(),
                             "events":rt.ledger.events()})

    def step(rt, *args, **kwargs):
        cap = active["cap"]
        start = len(cap.rows)
        before = state(rt)
        count = len(rt.ledger.events())
        t0 = perf_counter_ns()
        try:
            result = step0(rt, *args, **kwargs)
        except Exception as exc:
            after = state(rt)
            need(before == after, "R25_REJECTED_STEP_CHANGED_OWNER")
            active["steps"].append({"start":start,"end":len(cap.rows),"status":"REJECTED",
                "error":type(exc).__name__,"event_count_before":count,
                "event_count_after":len(rt.ledger.events()),"before":before,"after":after,
                "elapsed_ns":perf_counter_ns()-t0})
            raise
        event = rt.ledger.events()[-1]
        need(result["receipt"] == event["id"], "R25_STEP_EVENT")
        active["steps"].append({"start":start,"end":len(cap.rows),"status":"COMMITTED",
            "event":types.copy(event),"result":types.copy(result),"before":before,"after":state(rt),
            "event_count_before":count,"event_count_after":len(rt.ledger.events()),
            "elapsed_ns":perf_counter_ns()-t0})
        return result

    def family_operation(name, original):
        def wrapped(rt, *args, **kwargs):
            cap = active["cap"]
            start = len(cap.rows)
            before = None if name == "initialize_antecedent_adult" else state(rt)
            t0 = perf_counter_ns()
            status = "RETURNED"
            try:
                return original(rt, *args, **kwargs)
            except Exception as exc:
                status = type(exc).__name__
                if before is not None:
                    need(before == state(rt), "R26_REJECTED_FAMILY_CHANGED_STATE")
                raise
            finally:
                active["operations"].append({"operation":name,"start":start,"end":len(cap.rows),
                    "status":status,"elapsed_ns":perf_counter_ns()-t0})
        return wrapped

    with patch.object(ValidatingSemanticService,"proposal",new=proposal), patch.object(ConstitutiveRuntime,"step",new=step):
        if lane == "R61":
            for name, learn, nominate, forge in [
                ("admit",True,True,False),("abstain",True,False,False),
                ("no_means",False,True,False),("forged",True,True,True)]:
                begin(name)
                with tempfile.TemporaryDirectory() as d:
                    active["result"] = owner.RetrospectiveReconstitution().arm(Path(d)/"life.sqlite",learn,nominate,forge)
        elif lane == "R62":
            cls = owner.ExistingFamilyContinuity
            names = ("initialize_antecedent_adult", "register_family_pathways",
                     "select_family_intersection", "admit_family_conception", "realize_family_birth")
            with ExitStack() as stack:
                for name in names:
                    stack.enter_context(patch.object(ConstitutiveRuntime,name,
                        new=family_operation(name,getattr(ConstitutiveRuntime,name))))
                for name in unittest.defaultTestLoader.getTestCaseNames(cls):
                    begin(name)
                    result = unittest.TextTestRunner(verbosity=1).run(unittest.TestSuite([cls(name)]))
                    need(result.wasSuccessful(),"R26_ORIGINAL_FAMILY_COURT_FAILED")
        elif lane == "R40":
            cls = owner.PolycentricLexicalR40
            course0 = cls.course
            surface0 = owner.NeighborEncounter.private_surface
            def course(self,mode="admit"):
                begin(mode)
                active["result"] = course0(self,mode)
                return active["result"]
            def surface(neighbor,*args,**kwargs):
                rt=neighbor.runtime
                before=state(rt); start=len(active["calls"]); t0=perf_counter_ns()
                view=surface0(neighbor,*args,**kwargs)
                need(before==state(rt) and start==len(active["calls"]),"R26_SURFACE_SIDE_EFFECT")
                active["views"].append({"view":types.copy(view),"event":types.copy(rt.ledger.events()[-1]),
                    "elapsed_ns":perf_counter_ns()-t0})
                return view
            with patch.object(cls,"course",new=course), patch.object(owner.NeighborEncounter,"private_surface",new=surface):
                result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
                need(result.wasSuccessful(),"R26_ORIGINAL_POLYCENTRIC_COURT_FAILED")
        else:
            cls = owner.LexicalOccurrenceR39
            build0 = cls.build
            surface0 = owner.NeighborEncounter.private_surface
            def build(self, mode="speak", hear=True, see=True):
                begin(f"{mode}_{int(hear)}_{int(see)}")
                return build0(self,mode,hear,see)
            def surface(neighbor,*args,**kwargs):
                rt = neighbor.runtime
                before=state(rt); start=len(active["calls"]); t0=perf_counter_ns()
                view=surface0(neighbor,*args,**kwargs)
                need(before==state(rt) and start==len(active["calls"]), "R25_SURFACE_SIDE_EFFECT")
                active["views"].append({"view":types.copy(view),"event":types.copy(rt.ledger.latest_event()),
                    "elapsed_ns":perf_counter_ns()-t0})
                return view
            with patch.object(cls,"build",new=build), patch.object(owner.NeighborEncounter,"private_surface",new=surface):
                result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
                need(result.wasSuccessful(), "R25_ORIGINAL_OWNER_COURT_FAILED")

    reports=[]
    for case in all_cases:
        cap=case["cap"]
        need(not cap.failed, "R25_INCOMPLETE_CAPTURE")
        witness={"lane":lane,"case":case["name"],"steps":case["steps"],"views":case["views"],
                 "calls":case["calls"],"operations":case["operations"],"result":case["result"]}
        doc=cap.document(owner_state_sha256=types.digest(witness))
        rows=lab.verify_workload(doc,source_head=head)["rows"]
        assigned=[i for st in case["steps"] for i in range(st["start"],st["end"])]
        # Other owner operations may legitimately invoke outside step.
        need(len(assigned)==len(set(assigned)), "R25_DUPLICATE_STEP_CALL")
        targets=[]
        for r in rows:
            p=r["packet"]
            lexical=p.get("expression_phase")=="LEXICAL_REALIZATION_BEFORE_EXPERIENCE"
            retro=r["task"]=="development" and bool(p.get("actual_private_rehearsal_analyst_only"))
            revalue = r["task"]=="development" and bool(p.get("historically_possible_lexical_project_revaluations"))
            if lexical or retro or revalue:
                bound=[s for s in case["steps"] if s["start"]<=r["seq"]<s["end"]]
                need(len(bound)==1,"R25_TARGET_STEP")
                targets.append({"seq":r["seq"],"task":r["task"],"packet_bytes":lab.size(p),
                    "proposal_bytes":lab.size(r["proposal"]),"step_status":bound[0]["status"],
                    "step_attempt":bound[0].get("result",{}).get("attempt"),
                    "offered_revisions":len(p.get("historically_possible_retrospective_orientation_revisions",[])),
                    "proposed_candidates":len(r["proposal"].get("candidates",[])),
                    "actor_id":p.get("actor",{}).get("id"),
                    "lexical_revaluation_offers":len(p.get("historically_possible_lexical_project_revaluations",[]))})
        operation_reports=[]
        for op in case["operations"]:
            group=rows[op["start"]:op["end"]]
            operation_reports.append({**op,"task_counts":dict(Counter(r["task"] for r in group)),
                "packet_bytes":sum(lab.size(r["packet"]) for r in group),
                "proposal_bytes":sum(lab.size(r["proposal"]) for r in group)})
        family_indices=[i for op in case["operations"] for i in range(op["start"],op["end"])]
        need(len(family_indices)==len(set(family_indices)) and not set(family_indices)&set(assigned),
             "R26_AMBIGUOUS_OPERATION_CALL")
        result={"case":case["name"],"task_counts":dict(Counter(r["task"] for r in rows)),
                "packet_bytes":sum(lab.size(r["packet"]) for r in rows),
                "proposal_bytes":sum(lab.size(r["proposal"]) for r in rows),
                "calls_outside_step":len(rows)-len(assigned),"targets":targets,
                "family_operations":operation_reports,"unassigned_calls":len(rows)-len(assigned)-len(family_indices),
                "rejected_steps":sum(st["status"]=="REJECTED" for st in case["steps"]),
                "views":[{"bytes":lab.size(v["view"]),"lexical_rows":sum(bool(x.get("spoken_text")) for x in v["view"]["mandatory"]),
                           "elapsed_ns":v["elapsed_ns"]} for v in case["views"]],
                "later_result":case["result"]}
        reports.append(result)
        if output:
            lab.save_report(output/(case["name"]+".workload.json"),doc)
            lab.save_report(output/(case["name"]+".witness.json"),witness)
    if lane=="R61":
        need([r["later_result"] for r in reports]==["EAT","WAIT","WAIT",None],"R25_RETRO_CONSEQUENCE")
        need(all(len(r["targets"])==1 for r in reports),"R25_RETRO_COVERAGE")
        need([r["targets"][0]["offered_revisions"] for r in reports]==[1,1,0,1],"R25_RETRO_OFFERS")
        need([r["targets"][0]["step_status"] for r in reports]==["COMMITTED","COMMITTED","COMMITTED","REJECTED"],"R25_RETRO_ADMISSION")
    elif lane=="R62":
        need(len(reports)==2,"R26_FAMILY_CASES")
        positive=next(r for r in reports if r["case"].startswith("test_actual"))
        negative=next(r for r in reports if r["case"].startswith("test_unlocated"))
        for r in reports:
            need(r["unassigned_calls"]==0,"R26_UNASSIGNED_FAMILY_CALL")
            need(r["task_counts"].get("adult_constructor")==2,"R26_CONSTRUCTOR_COUNT")
            init=next(o for o in r["family_operations"] if o["operation"]=="initialize_antecedent_adult")
            need(init["task_counts"]=={"adult_constructor":2},"R26_INITIALIZATION_CALLS")
        bind=next(o for o in positive["family_operations"] if o["operation"]=="select_family_intersection")
        need(bind["status"]=="RETURNED" and bind["task_counts"]=={"family_pathway_selection":1},
             "R26_RETAINED_BINDING_REGENERATED_OR_UNMEASURED")
        for op in positive["family_operations"]:
            if op["operation"] in ("register_family_pathways","admit_family_conception","realize_family_birth"):
                need(not op["task_counts"],"R26_LOCAL_FAMILY_OPERATION_SEMANTIC_CALL")
        refused=next(o for o in negative["family_operations"] if o["operation"]=="select_family_intersection")
        need(refused["status"]=="ValueError" and not refused["task_counts"],"R26_UNLOCATED_SELECTION_CALL")
    elif lane=="R40":
        by={r["case"]:r for r in reports}
        need(set(by)=={"admit","null","forge"},"R26_POLYCENTRIC_CASES")
        for name,r in by.items():
            lexical=[t for t in r["targets"] if t["task"]=="expression"]
            offers=[t for t in r["targets"] if t["lexical_revaluation_offers"]]
            need(len(lexical)==1,"R26_SINGLE_LEXICAL_CALL")
            if name!="forge":
                need({t["actor_id"] for t in offers}=={"first","second","null"},
                     "R26_LISTENER_OFFER_COVERAGE")
                need(all(t["step_status"]=="COMMITTED" for t in offers),"R26_LISTENER_ADMISSION")
                need(len(r["views"])==1 and r["views"][0]["lexical_rows"]==1,"R26_VIEW")
            else:
                need(r["rejected_steps"]==1 and lexical[0]["step_status"]=="REJECTED",
                     "R26_FOREIGN_BASIS_ROLLBACK")
        need(tuple(by["admit"]["later_result"]["first"])==("REST",0),"R26_COLD_REST")
        need(tuple(by["null"]["later_result"]["first"])==("WORK",.25),"R26_COLD_WORK")
    else:
        need(len(reports)==6,"R25_LEXICAL_ARMS")
        need(sum(len(r["targets"]) for r in reports)==3,"R25_LEXICAL_TARGETS")
        need(sum(r["rejected_steps"] for r in reports)==2,"R25_LEXICAL_REJECTIONS")
    return {"scope":"EXACT_SEPARATE_HERMETIC_OWNER_COURSES_NOT_LIVE_OR_JOINED",
            "source_head":head,"fixture_blob":blob,"lane":lane,"reports":reports,"network_calls":0,
            "provider_tokens":None,"wire_bytes":None}


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--owner-root",type=Path,required=True)
    p.add_argument("--lane",choices=PINS,required=True)
    p.add_argument("--private-output",type=Path)
    a=p.parse_args()
    if a.private_output:
        a.private_output.mkdir(mode=0o700,parents=False,exist_ok=False)
    print("INFERENCE_LAB_R25 "+json.dumps(run(a.owner_root.resolve(),a.lane,a.private_output),sort_keys=True))
