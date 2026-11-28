"""Actual modern owner consequences through inherited P2 checkpoint custody."""
import json
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
    def generation(self,rt,folder,actor,provider):
        return ModernGeneration(ModernDevelopmentOwner(rt,actor,folder/"ops.sqlite",
            sourcefree_attested=True),provider,folder/"batch.sqlite",folder/"cycle.json")
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
