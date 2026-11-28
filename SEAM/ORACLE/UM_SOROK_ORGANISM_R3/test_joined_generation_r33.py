"""R33: ancestry -> qualified childhood -> actual human encounter -> continuing history.
Pinned joined candidate, not a claim of its inherited regression health.
All policies/transport fixtures are sourcefree; no external model or human experiment.
"""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

import test_neighbor_material_support_r17 as owner_paths
from neighbor_runtime import NeighborEncounter
import mii
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import newborn,canonical
from um_sorok_organism.semantics import HeuristicSemanticProvider,ValidatingSemanticService
from um_sorok_organism.live_psychological_llm import ExplicitJSONLLMProvider
from modern_generation_port_r28 import (
    ModernDevelopmentOwner,ModernGeneration,ConditionalPolicy,link_actual_live_interval,
    CheckpointProvider)
from developmental_recursion.contracts import RecursionRefusal
from test_modern_generation_port_r28 import action,policy,event,retro,ModernGenerationCourt

WORDS="We have been living our ordinary lives."
PRIVATE="I remember the promise privately."
def care(target):
    return action("CARE",{"world_request":{"addressed_party_ref":target}})
def plural(actions,acquire=True):
    return policy(actions,[{"offer":"historically_possible_plural_care",
        "resolver":"EXISTING_PLURAL_CARE_SOURCE_RESOLUTION"}] if acquire else [])
def address():
    return {"action":"SIGNAL","option_match":{"grounds_status":"HISTORICALLY_ACQUIRED_CO_REGULATION"},
            "rank_by":"LATEST_PERSONALLY_SENSED_REGULATION"}

class LifeCheckpoint:
    def __init__(self,sid,*,acquire=True,resumed=False):
        self.sid=sid;self.acquire=acquire;self.resumed=resumed;self.requests=[]
    def call(self,r):
        self.requests.append(r);ctx=r["context"];t=ctx["clock"];n=len(self.requests)
        ret=retro(r)
        if r["mode"]=="TERMINAL":return {"retrospective":ret,"prospective":None}
        def e(name,delta,actor,pol,**kw):
            return event(ctx,f"{n}:{name}",t+delta,actor,pol,**kw)
        def fam(row,kind,**kw):
            row["circumstances"]["family"]={"kind":kind,"source_seal_id":self.sid,**kw};return row
        def child(acts):return plural(acts,self.acquire)
        if r["mode"]=="BOOTSTRAP" and not self.resumed:
            out=[e("antecedent",1,"father",{"father":policy([care("mother")],
                [{"candidate":{"kind":"MEMORY","content":PRIVATE,"cue_terms":["care"]},
                  "when":{"own_action":"CARE","status":"PERFORMED"}}])}),
                fam(e("maternal",2,"mother",{"mother":policy([action("WAIT")])}),"INTERSECTION",pathway_id="retained"),
                fam(e("encounter",3,"father",{"father":policy([care("mother")])}),"CONCEPTION"),
                fam(e("birth",5,"mother",{},span=2),"BIRTH")]
            out[-1]["operation"]="REALIZE_FAMILY_BIRTH"
        elif not self.resumed and n==2:
            out=[e("father-care",1,"father",{"father":policy([care("nadia")]),"nadia":child([])}),
                 e("mother-care",2,"mother",{"mother":policy([care("nadia")]),"nadia":child([])}),
                 e("orient1",3,"nadia",{"nadia":child([action("ORIENT")])}),
                 e("orient2",4,"nadia",{"nadia":child([action("ORIENT")])})]
        else:
            span=70 if self.resumed else 100
            first=e("ordinary",span+1,"father",{"father":policy([care("nadia"),action("REST"),action("WAIT")]),
                                                   "nadia":child([])},span=span)
            first["circumstances"]["period_ref"]="care"
            out=[first,e("mother",span+2,"mother",{"mother":policy([care("nadia"),action("REST"),action("WAIT")]),
                                                   "nadia":child([])}),
                 e("child",span+3,"nadia",{"nadia":child([action("PRACTICE"),action("ORIENT"),action("WAIT")])}),
                 e("address",span+4,"nadia",{"nadia":child([address(),action("ORIENT")]),
                     "mother":policy([action("REFUSE")]),"father":policy([action("REFUSE")])})]
        if self.resumed and r["mode"]=="BOOTSTRAP":
            refs=ctx["actor_contexts"]["father"]["recent_lived_source_refs"]
            out[-1]["circumstances"]["next_analytic_reads"]=[
                {"kind":"ACTOR_DOMAIN","actor":"father","domain":"memories"},
                {"kind":"ACTUAL_EXPERIENCE","actor":"father","objective_ref":refs[-1]["objective_ref"]}]
        return {"retrospective":ret,"prospective":out}

class JoinedGenerationCourt(unittest.TestCase):
    def generation(self,rt,folder,p,**kw):
        folder.mkdir(exist_ok=True)
        return ModernGenerationCourt.generation(self,rt,folder,"mother",p,**kw)
    def setup(self,db):
        calls=[]
        class Constructor(HeuristicSemanticProvider):
            def propose(self,task,p):
                if task=="adult_constructor":calls.append(p["actor_id"])
                return super().propose(task,p)
        rt=ConstitutiveRuntime(str(db),semantic=ValidatingSemanticService(Constructor()))
        def seed(aid):
            projects=[{"object":"continue embodied life","means":["REST","EAT"],"priority":.4},
                      {"object":"ordinary speech","means":["SPEAK"],"priority":.6},
                      {"object":"care for Nadia if present","means":["CARE"],"addressed_party_ref":"nadia","priority":.7}]
            if aid=="father":projects.append({"object":"care for Mother","means":["CARE"],
                                                 "addressed_party_ref":"mother","priority":.8})
            return {"input_kind":"THIN_BIOGRAPHY","source_grade":"EXPLICIT_FICTIONAL_HISTORICAL_INPUT",
                 "source_ref":"fictional:joined:"+aid,"biographical_context":{"ordinary_life":aid},
                 "fictional_seed":{"projects":projects}}
        rt.initialize_antecedent_adult("mother","Mother",seed("mother"),other_adults=[("father","Father",seed("father"))])
        sid=rt.register_family_pathways("mother",[{"id":"retained","source_ref":"fictional:family",
            "intersection_clock":2,"intersection_site":"home","conception_clock":3,"birth_clock":5,
            "counterpart_id":"father","counterpart_name":"Father","counterpart_packet":None,
            "child_id":"nadia","child_name":"Nadia","prior_shared_effects":"RETAIN_EXISTING_ACTUAL_HISTORY"}])["source_seal_id"]
        procs=[]
        for aid,begin,end in [("mother",9,54),("father",19,99)]:
            src=rt.register_historical_routine_source({"kind":"QUALIFIED_REPRODUCTIVE_CARE","actor":aid,
                "location":"home","start_clock":begin,"end_clock":end,"max_hours_per_active_day":2,
                "description":"bounded fictional care premise, not willingness"})
            procs.append({"kind":"QUALIFIED_REPRODUCTIVE_CARE","actor":aid,"location":"home",
                          "source_ref":src["source_ref"],"recipient":"nadia","hours_per_active_day":1.,
                          "provisional_exposure_fraction":.25})
        # Actual actor-specific reception conditions, not authored awareness.
        rt.register_sourcefree_recursive_encounter_paths({"grade":"SOURCEFREE_TEST_ONLY",
             "source_ref":"fictional:joined:hearing","paths":[{"observer":"mother","source_actor":"father",
                 "location":"home","from_clock":0,"through_clock":1000,"hearing":True,"sound_path":"audible",
                 "visual":True,"light":"lit","sightline":"unobstructed","facing":"source"}]})
        return rt,sid,{"care":procs},calls
    def test_joined_historical_and_live_modes_same_ledger(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);db=root/"life.sqlite";rt,sid,catalog,constructors=self.setup(db)
            p=LifeCheckpoint(sid);args={"family_sources":(sid,),"period_catalog":catalog,"qualified_interval_cuts":True}
            hist=root/"historical";g=self.generation(rt,hist,p,**args)
            try:
                first=g.bootstrap()
                self.assertEqual([x["objective"]["family"]["status"] for x in first["records"] if x["objective"]["family"]],
                                 ["BOUND","CONDITIONAL_CONCEPTION_ADMITTED","CHILD_BORN"])
                self.assertEqual(rt.ledger.actor("nadia")[1],newborn("nadia","Nadia"))
                self.assertEqual(constructors,["mother","father"])
                self.assertTrue(rt.ledger.actor("father")[1]["memories"])
                initial=g.advance()
                self.assertEqual([x["objective"]["attempt"] for x in initial["records"]],["CARE","CARE","ORIENT","ORIENT"])
                child=rt.ledger.actor("nadia")[1]
                self.assertEqual({x["caregiver_ref"] for x in child["co_regulation_orientations"]},{"mother","father"})
                actual_before=deepcopy(child["experienced_care_events"])
            finally:g.close();rt.close()
            for i in range(3):
                rt=ConstitutiveRuntime(str(db));g=self.generation(rt,hist,p,**args)
                try:
                    g.advance();self.assertEqual(rt.ledger.actor("nadia")[1]["age_days"],100*(i+1))
                    self.assertTrue(rt.verify()["valid"])
                    if i==2:
                        g.finish();handoff=g.terminal_handoff()
                        self.assertEqual(len(g.owner.checkpoint_receipts()),6)
                        before=deepcopy(rt.ledger.actors());prefix=rt.ledger.events()
                finally:g.close();rt.close()
            self.assertEqual(before["nadia"]["experienced_care_events"][:len(actual_before)],actual_before)
            self.assertEqual(constructors,["mother","father"])
            # Existing live owner/transport, separate from generation checkpoints.
            # The visitor acts only through actual authored commands.
            phase={"target":"visitor"}
            def mock(req):
                doc=json.loads(req["messages"][1]["content"]);task=doc["task"];packet=doc["actor_source_packet"]
                if task=="actor_attempt":
                    opts=[q for q in packet.get("addressed_lexical_options",[]) if
                          q.get("world_request",{}).get("addressed_party_ref")==phase["target"] and q.get("project_id")]
                    if len(opts)==1:
                        ans={"task":task,"practical_option_id":opts[0]["option_id"],"speech_intent":"Greet the actual visitor."}
                    else:
                        print("R33_SPEECH_UNAVAILABLE",json.dumps({"options":[o.get("action") for o in packet.get("options",[])], "addressed_count":len(opts),"body":packet.get("actor",{}).get("body")},sort_keys=True))
                        ans={"task":task,"action":"REST" if any(o.get("action")=="REST" for o in packet.get("options",[])) else "WAIT"}
                elif task=="expression":
                    ans={"task":task,"speech":WORDS} if packet.get("expression_phase")=="LEXICAL_REALIZATION_BEFORE_EXPERIENCE" else {"task":task,"surface":"Ordinary life."}
                elif task=="development":ans={"task":task,"candidates":[]}
                else:raise AssertionError(task)
                return {"choices":[{"message":{"content":json.dumps(ans)}}]}
            # Existing exact owner transport, hermetic; no per-event generation.
            wire=ExplicitJSONLLMProvider(endpoint="https://example.invalid/chat/completions",model="fixture",
                  api_key="not-a-key",allow_private_actor_data=True,transport=mock,metrics_capacity=20)
            rt=ConstitutiveRuntime(str(db),semantic=ValidatingSemanticService(wire))
            try:
                world=rt.ledger.world()[1];registry=world["routine_source_registry"]
                for period in world["historical_periods"]:
                    for proc in period["processes"]:
                        if proc.get("source_ref") in registry:
                            s=registry[proc["source_ref"]]
                            self.assertLessEqual(s["from_clock"],period["start"])
                            self.assertLessEqual(period["end"],s["through_clock"])
                self.assertTrue(world.get("reproductive_labor_periods"))
                n=NeighborEncounter(rt,"visitor",mii_module=mii)
                n.install_sourcefree_conditions({"grade":"SOURCEFREE_TEST_ONLY",
                    "user_conditions":{"home":{"light":"lit","sightline":"unobstructed","hearing":True,
                         "sound_path":"audible","legibility":"readable"}},
                    "actor_conditions":{a:{"facing":"entrance","visual":True,"light":"lit",
                         "sightline":"unobstructed","hearing":True,"sound_path":"audible"}
                         for a in ("father","mother","nadia")}},request_id="geometry")
                self.assertEqual(n.contribute("enter","MOVE",destination="home")["status"],"PERFORMED")
                # The prior 300-day trajectory actually leaves father fatigued.
                # Respect his body's refusal of SPEAK. Rest is selected via
                # the real actor policy; no injected state or forced greeting.
                attempts=[];expression_calls=None
                for _ in range(3):
                    old_count=wire.usage_snapshot()["total"]
                    out=n.independent_actor_beat("father");attempts.append(out["attempt"])
                    if out["attempt"]=="SPEAK":
                        expression_calls=sum(x["task"]=="expression" for x in wire.usage_snapshot()["receipts"][old_count:])
                        break
                self.assertEqual(attempts[0],"REST")
                self.assertEqual(out["attempt"],"SPEAK")
                self.assertEqual(out["status"],"PERFORMED")
                self.assertEqual(expression_calls,1)
                surface=n.private_surface(n.new_private_profile())
                self.assertTrue(any(x.get("spoken_text")==WORDS and
                    x.get("lexical_acquisition_route")=="VOLUNTARILY_ADDRESSED_TO_SELF" for x in surface["mandatory"]))
                self.assertNotIn(PRIVATE,canonical(surface))
                self.assertEqual(n.contribute("leave","LEAVE")["status"],"PERFORMED")
                history=deepcopy(rt.ledger.world()[1]["neighbor_user_events"])
                self.assertEqual(rt.ledger.events()[:len(prefix)],prefix)
                link=link_actual_live_interval(rt,handoff,hist/"cycle.json")
                self.assertTrue(any(x["kind"]=="ACTOR_LIFE_TRANSITION" for x in link["events"]))
                self.assertNotIn("visitor",rt.ledger.actors())
                self.assertTrue(rt.verify()["valid"])
            finally:rt.close()
            # Explicit new checkpoint epoch on exactly the same actual owner root.
            rt=ConstitutiveRuntime(str(db));after=root/"after-visitor"
            p2=LifeCheckpoint(sid,resumed=True);g=self.generation(rt,after,p2,continuity_link=link,**args)
            try:
                batch=g.bootstrap()
                self.assertEqual(p2.requests[0]["context"]["prior_generation_and_live_ancestry"],link)
                self.assertEqual(rt.ledger.actor("nadia")[1]["age_days"],370)
                self.assertEqual(rt.ledger.world()[1]["neighbor_user_events"],history)
                self.assertEqual(rt.ledger.events()[:len(prefix)],prefix)
                self.assertTrue(rt.verify()["valid"]);self.assertTrue(g.engine.verify())
            finally:g.close();rt.close()
            rt=ConstitutiveRuntime(str(db));g=self.generation(rt,after,p2,continuity_link=link,**args)
            try:
                g.advance();g.finish()
                reads=p2.requests[1]["context"]["selected_exact_analytic_reads"]
                self.assertEqual(len(reads),2)
                self.assertIn(PRIVATE,canonical(reads[0]["value"]))
                self.assertEqual(reads[1]["value"]["actor"],"father")
                self.assertNotIn("events",p2.requests[1]["context"]["prior_generation_and_live_ancestry"])
                self.assertEqual(rt.ledger.actor("nadia")[1]["age_days"],440)
                self.assertEqual(rt.ledger.world()[1]["neighbor_user_events"],history)
                self.assertEqual(constructors,["mother","father"])
                self.assertTrue(rt.verify()["valid"]);self.assertTrue(g.engine.verify())
                print("R33_JOINED_LIFE "+json.dumps({"age_days":440,"historical_calls":len(p.requests),
                    "post_live_calls":len(p2.requests),"live_task_calls":wire.usage_snapshot()["total"],
                    "native_events":rt.verify()["events"],"routine_periods":len(world["reproductive_labor_periods"]),
                    "actual_live_link_events":len(link["events"]),"actors":sorted(rt.ledger.actors())},sort_keys=True))
            finally:g.close();rt.close()

    def test_qualified_lexical_policy_matches_actual_owner_offer(self):
        # Real R42 lexical revaluation, not merely a response-schema test.
        from um_sorok_organism.types import adult,blank_world
        from um_sorok_organism.world import register_recursive_encounter_paths
        with tempfile.TemporaryDirectory() as d:
            for addressed in (True,False):
                rt=ConstitutiveRuntime(str(Path(d)/str(addressed)))
                try:
                    speaker=adult("speaker","Speaker","workshop")
                    speaker["projects"]=[{"id":"talk","object":"speak","means":["SPEAK"],"priority":.6,"status":"active"}]
                    listener=adult("listener","Listener","workshop")
                    listener["projects"]=[{"id":"work","object":"earn wage","means":["WORK"],"priority":.65,"status":"active"},
                        {"id":"rest","object":"rest","means":["REST"],"priority":.4,"status":"active"}]
                    w=blank_world();register_recursive_encounter_paths(w,{"speaker":speaker,"listener":listener},
                      {"grade":"SOURCEFREE_TEST_ONLY","source_ref":"fictional:address","paths":[
                        {"observer":"listener","source_actor":"speaker","location":"workshop","from_clock":0,"through_clock":30,
                         "hearing":True,"sound_path":"audible","visual":True,"light":"lit","sightline":"unobstructed","facing":"source"}]})
                    rt.ledger.initialize(w,[speaker,listener])
                    class LexicalCheckpoint:
                        def call(self,r):
                            ctx=r["context"];t=ctx["clock"]
                            if r["mode"]=="TERMINAL":return {"retrospective":retro(r),"prospective":None}
                            rule={"action":"SPEAK","project_id":"talk","speech_intent":"Share a worry."}
                            if addressed:
                                rule={"action":"SPEAK","pool":"addressed_lexical_options",
                                      "option_match":{"project_id":"talk","world_request":{"addressed_party_ref":"listener"}},
                                      "speech_intent":"Share a worry."}
                            speech=policy([rule]);speech["expression"]={"speech":"I was worried about tomorrow."}
                            formation=policy([], [{"offer":"historically_possible_lexical_project_revaluations",
                                "construct":"LEXICAL_PROJECT_REVALUATION","match":{"project_id":"work",
                                    "lexical_revaluation_basis":{"lexical_acquisition_route":"VOLUNTARILY_ADDRESSED_TO_SELF"}},
                                "augment":{"priority":.1,"personal_significance":"Perhaps I can take a moment to listen."}}])
                            return {"retrospective":retro(r),"prospective":[
                              event(ctx,"worked",t+1,"listener",{"listener":policy([{"action":"WORK","project_id":"work"}])}),
                              event(ctx,"speech",t+2,"speaker",{"speaker":speech,"listener":formation}),
                              event(ctx,"later",t+3,"listener",{"listener":policy([{"action":"SELECT_HIGHEST_CURRENT_PROJECT_COURSE","project_course_actions":["WORK","REST"]},action("WAIT")])})]}
                    p=LexicalCheckpoint();folder=Path(d)/("generation"+str(addressed))
                    folder.mkdir();g=ModernGeneration(ModernDevelopmentOwner(rt,"listener",folder/"ops.sqlite",
                        sourcefree_attested=True),p,folder/"batch.sqlite",folder/"cycle.json")
                    try:
                        rs=g.bootstrap()["records"]
                        self.assertEqual(rs[1]["objective"]["attempt"],"SPEAK")
                        self.assertEqual(rs[1]["consequences"]["conditional_routes"].get("typed_lexical_project_revaluation",0),int(addressed))
                        a=rt.ledger.actor("listener")[1]
                        self.assertEqual(a["projects"][0]["priority"],.1 if addressed else .65)
                        self.assertEqual(rs[2]["objective"]["attempt"],"REST" if addressed else "WORK")
                        g.finish();self.assertTrue(rt.verify()["valid"])
                    finally:g.close()
                finally:rt.close()


    def test_actual_acquired_cultural_reference_becomes_new_end_trial_and_project(self):
        # Reuse the R34 native cultural, possible-end and project owners.
        # Two explicit research setup acts are conserved as such, never
        # represented as autonomous psychological selection.
        from um_sorok_organism.types import adult,blank_world
        for acquire in (True,False):
            with self.subTest(acquire=acquire),tempfile.TemporaryDirectory() as d:
                folder=Path(d);rt=ConstitutiveRuntime(str(folder/"life.sqlite"))
                try:
                    father=adult("father","Father")
                    father["projects"]=[{"id":"make","object":"make things","means":["MAKE_OBJECT"],"priority":.6,"status":"active"}]
                    child=newborn("nadia","Nadia")
                    w=blank_world();w["sites"]["home"]["stock"]=30
                    rt.ledger.initialize(w,[father,child])
                    self.assertEqual(rt.step("father",requested_action="MAKE_OBJECT")["status"],"PERFORMED")
                    old=next(iter(rt.ledger.world()[1]["material_objects"]))
                    self.assertEqual(rt.step("father",requested_action="SPEAK",object_ref=old)["status"],"PERFORMED")
                    self.assertTrue(rt.ledger.actor("nadia")[1]["cultural_demonstrations"])
                    self.assertFalse(rt.ledger.actor("nadia")[1]["possible_ends"])
                    class CulturalCheckpoint:
                        def __init__(self):self.requests=[]
                        def call(self,r):
                            self.requests.append(r);ctx=r["context"];t=ctx["clock"]
                            if r["mode"]=="TERMINAL":return {"retrospective":retro(r),"prospective":None}
                            if r["mode"]=="BOOTSTRAP":
                                learn=[{"offer":"historically_possible_cultural_references"}] if acquire else []
                                meaning=[{"offer":"historically_possible_cross_object_significance",
                                    "construct":"CROSS_OBJECT_POSSIBLE_END","augment":{
                                    "possible_object":"discover how different made things can be cared for",
                                    "possible_means":["INSPECT"],"cue_terms":["material_object"]}}] if acquire else []
                                rows=[
                                    event(ctx,"inspect-old",t+1,"nadia",{"nadia":policy([
                                        action("INSPECT",{"project_id":None,"world_request":{"material_object_ref":old},
                                            "grounds_status":"PRESENT_MATERIAL_OBJECT_NOT_ASSUMED_MOTIVE"})],learn)}),
                                    event(ctx,"make-new",t+2,"father",{"father":policy([{"action":"MAKE_OBJECT","project_id":"make"}])}),
                                    event(ctx,"new-interest",t+3,"nadia",{"nadia":policy([
                                        action("INSPECT",{"cross_object_attention_analytic_only":{}}),action("WAIT")],meaning)})]
                            else:
                                ends=ctx["actor_contexts"]["nadia"]["possible_ends"]
                                if ends:
                                    ref=ends[0]["origin_material_object_ref"]
                                    acts=[{"action":"INSPECT","pool":"possible_end_trials",
                                         "option_match":{"source_material_object_ref":ref}},action("WAIT")]
                                    take=[action("INSPECT",{"project_id":None,"world_request":{"material_object_ref":ref},
                                          "grounds_status":"PRESENT_MATERIAL_OBJECT_NOT_ASSUMED_MOTIVE"}),action("WAIT")]
                                    takeup=[{"offer":"historically_possible_incidental_takeup",
                                            "construct":"INCIDENTAL_END_TAKEUP","augment":{"means":["INSPECT"]}}]
                                    exercise=[action("INSPECT",{"world_request":{"material_object_ref":ref},
                                            "grounds_status":"AVAILABLE_SINGLE_PROJECT_COURSE"}),action("WAIT")]
                                else:acts=take=exercise=[action("WAIT")];takeup=[]
                                rows=[event(ctx,"trial",t+1,"nadia",{"nadia":policy(acts)}),
                                    event(ctx,"takeup",t+2,"nadia",{"nadia":policy(take,takeup)}),
                                    event(ctx,"exercise",t+3,"nadia",{"nadia":policy(exercise)})]
                            return {"retrospective":retro(r),"prospective":rows}
                    p=CulturalCheckpoint()
                    g=ModernGeneration(ModernDevelopmentOwner(rt,"nadia",folder/"ops.sqlite",
                        sourcefree_attested=True),p,folder/"batch.sqlite",folder/"cycle.json")
                    try:
                        b=g.bootstrap();a=rt.ledger.actor("nadia")[1]
                        self.assertEqual(len(a["cultural_reference_practices"]),int(acquire))
                        self.assertEqual(len(a["possible_ends"]),int(acquire))
                        self.assertFalse(a["projects"])
                        self.assertEqual(b["records"][2]["objective"]["attempt"],"INSPECT" if acquire else "WAIT")
                        if acquire:self.assertNotEqual(a["possible_ends"][0]["origin_material_object_ref"],old)
                    finally:g.close();rt.close()
                    rt=ConstitutiveRuntime(str(folder/"life.sqlite"))
                    g=ModernGeneration(ModernDevelopmentOwner(rt,"nadia",folder/"ops.sqlite",
                        sourcefree_attested=True),p,folder/"batch.sqlite",folder/"cycle.json")
                    try:
                        b=g.advance();a=rt.ledger.actor("nadia")[1]
                        self.assertEqual(len(a["projects"]),int(acquire))
                        self.assertEqual(b["records"][2]["objective"]["attempt"],"INSPECT" if acquire else "WAIT")
                        if acquire:
                            self.assertTrue(any(x.get("operation")=="INSPECT" and x.get("performed_status")=="PERFORMED"
                                                for x in a["projects"][0].get("operational_history",[])))
                        g.finish();self.assertTrue(rt.verify()["valid"]);self.assertTrue(g.engine.verify())
                        print("R37_CULTURAL_END "+json.dumps({"acquire":acquire,"checkpoints":len(p.requests),
                           "acquired_references":len(a["cultural_reference_practices"]),"projects":len(a["projects"]),
                           "later_attempt":b["records"][2]["objective"]["attempt"]},sort_keys=True))
                    finally:g.close()
                finally:rt.close()

if __name__=="__main__":unittest.main()
