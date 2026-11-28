"""Actual modern owner consequences through inherited P2 checkpoint custody."""
import json
import importlib.util
from pathlib import Path
import tempfile
import unittest

from um_sorok_organism.types import adult,newborn,blank_world
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.practical_powers import active_repair_technique
from modern_generation_port_r28 import ModernDevelopmentOwner,ModernGeneration,CheckpointProvider
from developmental_recursion.contracts import RecursionRefusal
from developmental_recursion.model_cycle import AmbiguousModelCall

MEANING="I can make room for a meal without losing the work."

def action(action,match=None):
    return {"action":action,**({"option_match":match} if match is not None else {})}

def policy(actions, rules=(), base="NONE"):
    return {"actions":actions,"formation":{"base":base,"rules":list(rules)}}

def event(ctx,ident,clock,actor,policies,*,retro=None,span=0):
    c={"policies":policies}
    if retro is not None:c["retrospective_event_id"]=retro
    return {"event_id":ident,"event_time":clock,"operation":"CONTINUE_ACTOR_LIFE",
            "source_refs":[ctx["source_ref"]],"participants":[actor],"circumstances":c,
            **({"interval":{"mode":"ACTUAL","span":span}} if span else {})}

def retro(request,actor=None,disposition="INTERPRET_ONLY"):
    prev=request["previous"]
    if prev is None:return None
    return {"batch_id":prev["batch_id"],"history_hash":prev["history_hash"],
            "event_ids":[e["event_id"] for e in prev["events"]],
            "impressions":[{"event_id":e["event_id"],"interpretations":
                ([{"actor":actor,"meaning":MEANING,"disposition":disposition}]
                 if actor and i==0 else [])} for i,e in enumerate(prev["events"])]}

class RepairCheckpoint:
    def __init__(self,refs,admit=True):
        self.refs=refs;self.admit=admit;self.requests=[]
    def call(self,r):
        self.requests.append(r)
        ctx=r["context"];t=ctx["clock"]
        if r["mode"]=="BOOTSTRAP":
            out=[]
            for i,ref in enumerate(self.refs):
                if i:out.append(event(ctx,"rest"+str(i),t+len(out)+1,"worker",
                                      {"worker":policy([action("REST")])}))
                rules=([
                    {"candidate":{"kind":"MEMORY","content":"The repair felt like something I must keep doing.",
                                  "cue_terms":["repair"]},"when":{"own_action":"REPAIR","status":"PERFORMED"}},
                    {"candidate":{"kind":"ACQUIRE_HISTORICAL_ORIENTATION","operation":"EAT",
                                  "orientation_mode":"WITHHOLD"},"when":{"own_action":"REPAIR","status":"PERFORMED"}}
                    ] if i==0 else [{"offer":"historically_possible_repair_techniques"}])
                out.append(event(ctx,"repair"+str(i),t+len(out)+1,"worker",{"worker":policy(
                    [action("REPAIR",{"project_id":None,"world_request":{
                        "material_object_ref":ref}})],rules)}))
            return {"retrospective":None,"prospective":out}
        if r["mode"]=="TERMINAL":
            return {"retrospective":retro(r),"prospective":None}
        rr=retro(r,"worker","REHEARSE" if self.admit else "INTERPRET_ONLY")
        return {"retrospective":rr,"prospective":[
            event(ctx,"reconsider",t+1,"worker",{"worker":policy([action("WAIT")])},
                  retro="repair0" if self.admit else None),
            event(ctx,"meal",t+2,"worker",{"worker":policy([action("EAT"),action("WAIT")])}),
            event(ctx,"rest",t+3,"worker",{"worker":policy([action("REST"),action("WAIT")])})]}

class FamilyCheckpoint:
    def __init__(self):self.requests=[]
    def call(self,r):
        self.requests.append(r);ctx=r["context"];t=ctx["clock"]
        if r["mode"]=="TERMINAL":return {"retrospective":retro(r),"prospective":None}
        n=len(self.requests)
        return {"retrospective":retro(r),"prospective":[
            event(ctx,f"period{n}",t+8,"mother",{"mother":policy([action("REST"),action("WAIT")],base="LOCAL")},span=7),
            event(ctx,f"child{n}",t+9,"nadia",{"nadia":policy([action("SIGNAL"),action("WAIT")],base="LOCAL")}),
            event(ctx,f"father{n}",t+10,"father",{"father":policy([action("WORK"),action("REST"),action("WAIT")],base="LOCAL")})]}


class GenealogyCheckpoint:
    def __init__(self,sid,choose=True):
        self.sid=sid;self.choose=choose;self.requests=[]
    def call(self,r):
        self.requests.append(r);ctx=r["context"];t=ctx["clock"]
        def family(e,kind,**fields):
            e["circumstances"]["family"]={"kind":kind,"source_seal_id":self.sid,**fields}
            return e
        def pledge(target):
            return action("PLEDGE_CARE",{"world_request":{"addressed_party_ref":target}})
        if r["mode"]=="BOOTSTRAP":
            first=event(ctx,"antecedent",t+1,"father",{"father":policy([pledge("mother"),action("WAIT")],
                [{"candidate":{"kind":"MEMORY","content":"I made a promise.","cue_terms":["care"]},
                  "when":{"own_action":"PLEDGE_CARE","status":"PERFORMED"}}])})
            bind=family(event(ctx,"binding",t+2,"mother",{"mother":policy([action("WAIT")])}),
                        "INTERSECTION",pathway_id="retained" if self.choose else None)
            third=family(event(ctx,"conditional",t+3,"father",{"father":policy([pledge("mother"),action("WAIT")])}),
                         "CONCEPTION")
            birth=family(event(ctx,"birth",t+5,"mother",{},span=2),"BIRTH")
            birth["operation"]="REALIZE_FAMILY_BIRTH"
            return {"retrospective":None,"prospective":[first,bind,third,birth]}
        if r["mode"]=="TERMINAL":
            return {"retrospective":retro(r),"prospective":None}
        roster=ctx["actor_contexts"]
        first="nadia" if "nadia" in roster else "mother"
        return {"retrospective":retro(r),"prospective":[
            event(ctx,"continuing-child-or-mother",t+1,first,
                  {first:policy([action("SIGNAL"),action("WAIT")],base="LOCAL"),
                   "father":policy([action("CARE"),action("REFUSE")],base="LOCAL"),
                   **({"mother":policy([action("CARE"),action("REFUSE")],base="LOCAL")} if first!="mother" else {})}),
            event(ctx,"continuing-father",t+2,"father",
                  {"father":policy([pledge(first),action("REST"),action("WAIT")],base="LOCAL")}),
            event(ctx,"period-mother",t+6,"mother",{"mother":policy([action("REST"),action("WAIT")],base="LOCAL")},span=3)]}


class ReproductiveCheckpoint:
    """One identical conditional policy in materially divergent actual worlds."""
    def __init__(self):self.requests=[]
    def call(self,r):
        self.requests.append(r);ctx=r["context"];t=ctx["clock"]
        n=len(self.requests)
        def care(a):return action("CARE",{"project_id":"care:"+a,
                                         "world_request":{"addressed_party_ref":"nadia"}})
        def child(actions):
            return policy(actions,[{"offer":"historically_possible_plural_care",
                         "resolver":"EXISTING_PLURAL_CARE_SOURCE_RESOLUTION"}])
        if r["mode"]=="BOOTSTRAP":
            return {"retrospective":None,"prospective":[
                event(ctx,"first-father",t+1,"father",{"father":policy([care("father")]),"nadia":child([])}),
                event(ctx,"first-mother",t+2,"mother",{"mother":policy([care("mother")]),"nadia":child([])}),
                event(ctx,"first-orient",t+3,"nadia",{"nadia":child([action("ORIENT"),action("WAIT")])}),
                event(ctx,"second-orient",t+4,"nadia",{"nadia":child([action("ORIENT"),action("WAIT")])})]}
        if r["mode"]=="TERMINAL":return {"retrospective":retro(r),"prospective":None}
        first=event(ctx,f"father{n}",t+101,"father",
                    {"father":policy([care("father"),action("WAIT")]),"nadia":child([])},span=100)
        first["circumstances"]["period_ref"]="reproduction"
        return {"retrospective":retro(r),"prospective":[first,
            event(ctx,f"mother{n}",t+102,"mother",{"mother":policy([care("mother"),action("WAIT")]),"nadia":child([])}),
            event(ctx,f"address{n}",t+103,"nadia",
                  {"nadia":child([{"action":"SIGNAL","option_match":{"grounds_status":"HISTORICALLY_ACQUIRED_CO_REGULATION"},
                                    "rank_by":"LATEST_PERSONALLY_SENSED_REGULATION"},action("WAIT")]),
                   "father":policy([action("REFUSE")]),"mother":policy([action("REFUSE")])})]}

class ModernGenerationCourt(unittest.TestCase):
    def setup_repair(self,db):
        rt=ConstitutiveRuntime(str(db));w=blank_world();w["sites"]["home"]["stock"]=30
        a=adult("worker","Mara")
        a["projects"]=[{"id":"repair_training","object":"maintain things","means":["REPAIR"],"status":"active","priority":.5},
                       {"id":"ordinary_meal","object":"eat a meal","means":["EAT"],"status":"active","priority":.4}]
        rt.ledger.initialize(w,[a])
        src=rt.register_historical_routine_source({"kind":"QUALIFIED_ROUTINE_PRACTICE","actor":"worker",
            "location":"home","start_clock":0,"end_clock":7,"max_hours_per_active_day":3,
            "description":"bounded modeled component practice"})
        rt.background(7,processes=[{"kind":"QUALIFIED_ROUTINE_PRACTICE","actor":"worker","location":"home",
            "source_ref":src["source_ref"],"hours_per_active_day":3,"provisional_exposure_fraction":1.,
            "operation":"REPAIR","mode":"SOLO_COMPONENT_PRACTICE"}])
        refs=[]
        for _ in range(3):
            rt.step("worker",requested_action="REST")
            old=set(rt.ledger.world()[1]["material_objects"])
            self.assertEqual(rt.step("worker",requested_action="MAKE_OBJECT")["status"],"PERFORMED")
            refs.append((set(rt.ledger.world()[1]["material_objects"])-old).pop())
        # A real external prep, not represented as a checkpoint or model call.
        rt.step("worker",requested_action="REST")
        return rt,refs
    def generation(self,rt,folder,actor,provider,**kwargs):
        # Load the exact specialist transport against the actual owner types.
        # Mock endpoint returns the fixture's policy; not a model-quality test.
        path=Path(__file__).resolve().parent/"um_sorok_organism/live_psychological_llm.py"
        spec=importlib.util.spec_from_file_location("um_sorok_organism.r29_checkpoint_overlay",path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        def mock(req):
            prompt=req["messages"][0]["content"]
            self.assertIn("3-5 salient next event surfaces",prompt)
            self.assertIn("retrospective_event_id",prompt)
            self.assertIn("No actor appears before actual admitted birth",prompt)
            request=json.loads(req["messages"][1]["content"])
            reply=provider.call(request)
            return {"choices":[{"message":{"content":json.dumps(reply)}}]}
        transport=module.ExplicitDevelopmentalCheckpointProvider(
            endpoint="https://example.invalid/chat/completions",model="sourcefree-fixture-only",
            api_key="not-a-credential",allow_private_actor_data=True,
            sourcefree_checkpoint_attested=True,transport=mock,metrics_capacity=10)
        return ModernGeneration(ModernDevelopmentOwner(rt,actor,folder/"ops.sqlite",
            sourcefree_attested=True,**kwargs),transport,folder/"batch.sqlite",folder/"cycle.json")
    def repair_arm(self,folder,admit):
        rt,refs=self.setup_repair(folder/"life.sqlite");p=RepairCheckpoint(refs,admit)
        g=self.generation(rt,folder,"worker",p)
        try:
            first=g.bootstrap()
            self.assertEqual(len(first["records"]),5)
            self.assertEqual([r["objective"]["attempt"] for r in first["records"]],
                             ["REPAIR","REST","REPAIR","REST","REPAIR"])
            a=rt.ledger.actor("worker")[1]
            self.assertTrue(active_repair_technique(a,"home"))
            self.assertTrue(any(x["action"]=="EAT" for x in rt.situated("worker")["suspended_actions"]))
            self.assertEqual(len(p.requests),1)
            history=first["history_hash"]
        finally:g.close();rt.close()
        # Real cold reopening of both native ledger and inherited cycle.
        rt=ConstitutiveRuntime(str(folder/"life.sqlite"));g=self.generation(rt,folder,"worker",p)
        try:
            food=rt.ledger.world()[1]["sites"]["home"]["food"]
            second=g.advance()
            self.assertEqual(len(p.requests),2)
            self.assertEqual(p.requests[1]["previous"]["history_hash"],history)
            self.assertEqual(len(second["records"]),3)
            self.assertEqual(second["records"][1]["objective"]["attempt"],"EAT" if admit else "WAIT")
            self.assertEqual(rt.ledger.world()[1]["sites"]["home"]["food"],food-int(admit))
            a=rt.ledger.actor("worker")[1];row=a["historical_orientations"][0]
            self.assertEqual(len(row.get("revisions",[])),int(admit))
            if admit:self.assertEqual(row["revisions"][0]["interpretive_hypothesis_not_causal_truth"],MEANING)
            self.assertNotIn(MEANING,str(rt.ledger.world()[1]))
            g.finish();self.assertEqual(len(p.requests),3)
            receipts=g.provider.provider.usage_snapshot()["receipts"]
            self.assertEqual(len(receipts),2) # ordinary and terminal after cold reopen
            self.assertTrue(all(r["attempts"]==1 and r["transport"]=="MOCK" and
                                r["outcome"]=="PROPOSAL_RETURNED" for r in receipts))
            self.assertTrue(g.engine.verify());self.assertTrue(rt.verify()["valid"])
            print("R28_REPAIR "+json.dumps({"admit":admit,"checkpoints":len(p.requests),
                "ordinary_calls":1,"events":8,"later_attempt":second["records"][1]["objective"]["attempt"],
                "revision_count":len(row.get("revisions",[])),
                "local_semantic_tasks":sum(sum(r["consequences"]["local_semantic_tasks"].values())
                  for r in first["records"]+second["records"]),
                "requests_bytes":sum(len(json.dumps(r,sort_keys=True,separators=(",",":")).encode())
                                     for r in p.requests)},sort_keys=True))
        finally:g.close();rt.close()
    def test_retrospective_model_meaning_changes_actual_next_activity(self):
        for admit in (True,False):
            with self.subTest(admit=admit),tempfile.TemporaryDirectory() as tmp:
                self.repair_arm(Path(tmp),admit)
    def test_multi_actor_maturation_and_cold_continuation(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);rt=ConstitutiveRuntime(str(folder/"life.sqlite"))
            rt.ledger.initialize(blank_world(),[adult("mother","Mother"),adult("father","Father","workshop"),newborn("nadia","Nadia")])
            p=FamilyCheckpoint();g=self.generation(rt,folder,"nadia",p)
            try:
                first=g.bootstrap();self.assertEqual(len(first["records"]),3)
                self.assertEqual(rt.ledger.actor("nadia")[1]["age_days"],7)
                self.assertEqual(len(p.requests),1)
            finally:g.close();rt.close()
            rt=ConstitutiveRuntime(str(folder/"life.sqlite"));g=self.generation(rt,folder,"nadia",p)
            try:
                second=g.advance();self.assertEqual(len(second["records"]),3)
                self.assertEqual(rt.ledger.actor("nadia")[1]["age_days"],14)
                self.assertEqual(set(rt.ledger.actors()),{"mother","father","nadia"})
                self.assertEqual(len(p.requests),2)
                self.assertTrue(all(r["consequences"]["remote_calls_during_event"]==0
                                    for r in first["records"]+second["records"]))
                g.finish();self.assertEqual(len(p.requests),3)
                self.assertTrue(g.engine.verify());self.assertTrue(rt.verify()["valid"])
                print("R28_FAMILY "+json.dumps({"checkpoints":3,"ordinary_calls":1,"events":6,
                     "child_age_days":rt.ledger.actor("nadia")[1]["age_days"],
                     "actors":sorted(rt.ledger.actors())},sort_keys=True))
            finally:g.close();rt.close()

    def test_historical_existing_adults_to_birth_and_continuing_child(self):
        for choose in (True,False):
            with self.subTest(choose=choose),tempfile.TemporaryDirectory() as tmp:
                from um_sorok_organism.semantics import HeuristicSemanticProvider,ValidatingSemanticService
                class Counting(HeuristicSemanticProvider):
                    def __init__(self):self.calls=[]
                    def propose(self,task,packet):
                        self.calls.append(task)
                        return super().propose(task,packet)
                local=Counting()
                folder=Path(tmp);rt=ConstitutiveRuntime(str(folder/"life.sqlite"),
                    semantic=ValidatingSemanticService(local))
                def packet(who):
                    return {"input_kind":"THIN_BIOGRAPHY","source_grade":"EXPLICIT_FICTIONAL_HISTORICAL_INPUT",
                        "source_ref":"fictional:"+who,"biographical_context":{"ordinary_life":who},
                        "fictional_seed":{"projects":[{"object":"ordinary care",
                          "means":["CARE","REST","EAT"],"priority":.5}]}}
                rt.initialize_antecedent_adult("mother","Mother",packet("mother"),
                     other_adults=[("father","Father",packet("father"))])
                sid=rt.register_family_pathways("mother",[{"id":"retained","source_ref":"fictional:path",
                    "intersection_clock":2,"intersection_site":"home","conception_clock":3,"birth_clock":5,
                    "counterpart_id":"father","counterpart_name":"Father","counterpart_packet":None,
                    "child_id":"nadia","child_name":"Nadia","prior_shared_effects":"RETAIN_EXISTING_ACTUAL_HISTORY"}])["source_seal_id"]
                p=GenealogyCheckpoint(sid,choose);g=self.generation(rt,folder,"mother",p,family_sources=(sid,))
                try:
                    first=g.bootstrap()
                    self.assertEqual(len(p.requests),1)
                    self.assertEqual(len(first["records"]),4)
                    self.assertEqual(first["records"][0]["objective"]["attempt"],"PLEDGE_CARE")
                    self.assertEqual(first["records"][1]["objective"]["family"]["status"],"BOUND" if choose else "ABSTAINED")
                    self.assertEqual("nadia" in rt.ledger.actors(),choose)
                    self.assertEqual(first["records"][3]["accessible"]["by_actor"],{})
                    self.assertEqual(local.calls.count("adult_constructor"),2)
                    father=rt.ledger.actor("father")[1]
                    self.assertTrue(father["memories"])
                    self.assertTrue(rt.verify()["valid"])
                    if choose:self.assertEqual(rt.ledger.actor("nadia")[1],newborn("nadia","Nadia"))
                finally:g.close();rt.close()
                rt=ConstitutiveRuntime(str(folder/"life.sqlite"));g=self.generation(rt,folder,"mother",p,family_sources=(sid,))
                try:
                    second=g.advance();self.assertEqual(len(p.requests),2)
                    self.assertEqual(len(second["records"]),3)
                    self.assertTrue(rt.ledger.actor("father")[1]["memories"])
                    if choose:
                        self.assertIn("nadia",second["records"][0]["accessible"]["by_actor"])
                        self.assertEqual(rt.ledger.actor("nadia")[1]["age_days"],3)
                    else:self.assertNotIn("nadia",rt.ledger.actors())
                    g.finish();self.assertEqual(len(p.requests),3)
                    self.assertTrue(g.engine.verify());self.assertTrue(rt.verify()["valid"])
                    print("R29_GENEALOGY "+json.dumps({"choose":choose,"checkpoints":3,"ordinary_calls":1,
                       "surfaces":7,"actor_roster":sorted(rt.ledger.actors()),
                       "native_family_stages":[r["objective"]["family"]["status"] for r in first["records"] if r["objective"]["family"]],
                       "initial_adult_constructors":local.calls.count("adult_constructor")},sort_keys=True))
                finally:g.close();rt.close()

    def test_300_day_ordinary_life_material_contradiction_and_independent_others(self):
        for work in (True,False):
            with self.subTest(work=work),tempfile.TemporaryDirectory() as tmp:
                folder=Path(tmp);rt=ConstitutiveRuntime(str(folder/"life.sqlite"))
                m=adult("mother","Mother","workshop");m["body"]["rest"]=.35
                f=adult("father","Father","workshop")
                n=newborn("nadia","Nadia","workshop");n["body"]["comfort"]=.2
                for a in (m,f):
                    a["projects"]=[{"id":"care:"+a["id"],"object":"care for Nadia","means":["CARE"],
                        "addressed_party_ref":"nadia","priority":.6,"status":"active"}]
                m["projects"].append({"id":"wage","object":"subsistence","means":["WORK"],"priority":.5,"status":"active"})
                rt.ledger.initialize(blank_world(),[m,f,n])
                src=rt.register_historical_routine_source({"kind":"QUALIFIED_WAGE_LABOR","actor":"mother",
                    "location":"workshop","start_clock":0,"end_clock":400,"max_hours_per_active_day":8,
                    "description":"bounded aggregate material labor history"})
                proc={"kind":"QUALIFIED_WAGE_LABOR","actor":"mother","location":"workshop",
                    "source_ref":src["source_ref"],"hours_per_active_day":8,"provisional_exposure_fraction":1.}
                catalog={"reproduction":[proc] if work else []}
                p=ReproductiveCheckpoint();g=self.generation(rt,folder,"nadia",p,period_catalog=catalog)
                try:
                    boot=g.bootstrap();records=boot["records"]
                    self.assertEqual([x["objective"]["attempt"] for x in records],["CARE","CARE","ORIENT","ORIENT"])
                    self.assertEqual({x["caregiver_ref"] for x in rt.ledger.actor("nadia")[1]["co_regulation_orientations"]},
                                     {"mother","father"})
                finally:g.close();rt.close()
                first_address=None
                for cycle in range(3):
                    rt=ConstitutiveRuntime(str(folder/"life.sqlite"));g=self.generation(rt,folder,"nadia",p,period_catalog=catalog)
                    try:
                        batch=g.advance();rs=batch["records"];records+=rs
                        child=rt.ledger.actor("nadia")[1]
                        self.assertEqual(child["age_days"],100*(cycle+1))
                        self.assertEqual(len(p.requests),cycle+2)
                        if cycle==0:
                            self.assertEqual(rs[0]["objective"]["attempt"],"CARE")
                            self.assertEqual(rs[1]["objective"]["attempt"],"WAIT" if work else "CARE")
                            self.assertEqual(rs[2]["objective"]["attempt"],"SIGNAL")
                            self.assertEqual(rs[2]["objective"]["status"],"PARTIAL")
                            first_address=rs[2]["objective"]["actual"]["target"]
                            self.assertEqual(first_address,"father" if work else "mother")
                        self.assertTrue(g.engine.verify());self.assertTrue(rt.verify()["valid"])
                        if cycle==2:
                            g.finish()
                            self.assertEqual(len(p.requests),5)
                            self.assertEqual(len(records),13)
                            self.assertEqual(len(rt.ledger.world()[1]["wage_labor_periods"]),3 if work else 0)
                            print("R31_REPRODUCTION "+json.dumps({"work":work,"child_age_days":child["age_days"],
                              "checkpoints":len(p.requests),"ordinary_calls":3,"surfaces":len(records),
                              "first_address":first_address,"actual_received_care_events":len(child["experienced_care_events"]),
                              "local_semantic_tasks":sum(sum(r["consequences"]["local_semantic_tasks"].values()) for r in records),
                              "canonical_checkpoint_bytes":sum(len(json.dumps(r,sort_keys=True,separators=(",",":")).encode()) for r in p.requests),
                              "wage_periods":len(rt.ledger.world()[1]["wage_labor_periods"])},sort_keys=True))
                    finally:g.close();rt.close()
    def test_foreign_retrospective_and_unbound_carrier_refused(self):
        req={"mode":"ORDINARY","context":{},"previous":{"batch_id":"b","history_hash":"h",
             "events":[{"event_id":"e","accessible":{"objective_ref":"o","by_actor":{"a":{}}}}]}}
        def response(a,disp):
            return {"retrospective":{"batch_id":"b","history_hash":"h","event_ids":["e"],
               "impressions":[{"event_id":"e","interpretations":[{"actor":a,"meaning":"test","disposition":disp}]}]},
               "prospective":[{"participants":["a"],"circumstances":{}} for _ in range(3)]}
        with self.assertRaisesRegex(RecursionRefusal,"GEN_RETRO_ACTOR_ACCESS"):
            CheckpointProvider.bind(req,response("foreign","INTERPRET_ONLY"))
        with self.assertRaisesRegex(RecursionRefusal,"GEN_RETROSPECTIVE_CARRIER_DROPPED"):
            CheckpointProvider.bind(req,response("a","REHEARSE"))

if __name__=="__main__":unittest.main()
