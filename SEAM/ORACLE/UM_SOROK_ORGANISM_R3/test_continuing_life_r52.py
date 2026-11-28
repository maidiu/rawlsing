"""R52 actual owner-mode operation, no manually stitched epoch internals."""
import json
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,blank_world
from continuing_life_r52 import ContinuingLife
from modern_generation_port_r28 import RecursionRefusal
import test_joined_generation_r33 as joined
from test_modern_generation_port_r28 import action,policy,event,retro
import mii

class Live:
    def __init__(self):self.requests=[]
    def call(self,r):
        self.requests.append(r)
        return {"policies":{r["principal"]:policy([action("REST"),action("WAIT")])}}

class ContinuingLifeCourt(unittest.TestCase):
    def test_cold_actual_family_history_live_resume(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);db=root/"life.sqlite"
            rt,sid,catalog,constructors=joined.JoinedGenerationCourt.setup(self,db)
            p=joined.LifeCheckpoint(sid);live=Live()
            opts={"family_sources":(sid,),"period_catalog":catalog,
                  "sourcefree_attested":True,"mii_module":mii}
            def open_life(rt,p):return ContinuingLife(rt,root/"operator","mother",
                       historical_provider=p,live_provider=live,**opts)
            s=open_life(rt,p)
            try:
                s.historical_checkpoint();s.historical_checkpoint();s.historical_checkpoint()
                self.assertEqual(rt.snapshot("nadia")["age_days"],100)
                self.assertEqual(s.status()["mode"],"HISTORY")
                s.finish_history()
                prefix=rt.ledger.events()
                self.assertEqual(s.status()["mode"],"LIVE")
            finally:s.close();rt.close()
            rt=ConstitutiveRuntime(str(db));s=open_life(rt,p)
            try:
                s.configure_encounter("visitor",{"grade":"SOURCEFREE_TEST_ONLY",
                    "user_conditions":{"home":{"light":"lit","sightline":"unobstructed","hearing":True,
                         "sound_path":"audible","legibility":"readable"}},
                    "actor_conditions":{a:{"facing":"entrance","visual":True,"light":"lit",
                         "sightline":"unobstructed","hearing":True,"sound_path":"audible"}
                         for a in ("father","mother","nadia")}},request_id="geometry")
                self.assertEqual(s.contribute("visitor","enter","MOVE",destination="home")["status"],"PERFORMED")
                w=rt.ledger.world()[1];ref=w["neighbor_user_events"][-1]["event_ref"];target=w["clock"]+3
                before=len(p.requests)
                with self.assertRaisesRegex(RecursionRefusal,"LIFE_VISITOR_STILL_PRESENT"):s.resume_history()
                self.assertEqual(len(p.requests),before)
                result=s.present_until("visitor",ref,target,max_beats=1)
                self.assertEqual(result["beats_committed_this_call"],1)
                self.assertEqual(len(live.requests),1)
            finally:s.close();rt.close()
            rt=ConstitutiveRuntime(str(db));s=open_life(rt,p)
            try:
                result=s.present_until("visitor",ref,target)
                self.assertEqual(result["beats_committed_this_call"],2)
                self.assertEqual(len(live.requests),3)
                retry=s.present_until("visitor",ref,target)
                self.assertEqual(retry["new_present_surfaces"],[])
                self.assertEqual(len(live.requests),3)
                self.assertNotIn(joined.PRIVATE,json.dumps(s.private_surface("visitor")))
                self.assertEqual(s.contribute("visitor","leave","LEAVE")["status"],"PERFORMED")
                actual=rt.ledger.events()
                self.assertEqual(actual[:len(prefix)],prefix)
                self.assertEqual(s.status()["mode"],"LIVE")
            finally:s.close();rt.close()
            p2=joined.LifeCheckpoint(sid,resumed=True)
            rt=ConstitutiveRuntime(str(db));s=open_life(rt,p2)
            try:
                s.resume_history();self.assertEqual(s.status()["epoch"],1)
                self.assertEqual(rt.snapshot("nadia")["age_days"],170)
                self.assertEqual(rt.ledger.events()[:len(actual)],actual)
                s.finish_history()
                self.assertEqual(constructors,["mother","father"])
                self.assertTrue(rt.verify()["valid"])
                self.assertTrue(all(r["status"]=="RETURNED" for r in s.receipts()))
                self.assertFalse(s.status()["held"])
                print("R52_OPERATOR",json.dumps({"age_days":170,"historical_calls":len(p.requests)+len(p2.requests),
                    "live_calls":len(live.requests),"native_events":len(rt.ledger.events()),
                    "operations":len(s.receipts()),"epochs":2},sort_keys=True))
            finally:s.close();rt.close()

    def test_failed_checkpoint_and_unreconciled_native_write_do_not_replay(self):
        class Broken:
            def __init__(self):self.calls=0
            def call(self,r):self.calls+=1;raise OSError("fixture ambiguous")
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);db=root/"life.sqlite";rt=ConstitutiveRuntime(str(db))
            rt.ledger.initialize(blank_world(),[adult("worker","Mara")])
            p=Broken();live=Live()
            def open_life(rt,folder):return ContinuingLife(rt,folder,"worker",historical_provider=p,
                   live_provider=live,sourcefree_attested=True)
            s=open_life(rt,root/"stale");rt.step("worker",requested_action="REST")
            try:
                self.assertTrue(s.status()["held"])
                with self.assertRaisesRegex(RecursionRefusal,"LIFE_UNRECONCILED_NATIVE_TRANSITION"):s.historical_checkpoint()
                self.assertEqual(p.calls,0)
            finally:s.close()
            s=open_life(rt,root/"ambiguous");before=rt.ledger.events()
            try:
                with self.assertRaises(RecursionRefusal):s.historical_checkpoint()
                self.assertEqual(p.calls,1);self.assertEqual(rt.ledger.events(),before)
                self.assertEqual(s.receipts()[-1]["status"],"HELD")
            finally:s.close();rt.close()
            rt=ConstitutiveRuntime(str(db));s=open_life(rt,root/"ambiguous")
            try:
                self.assertTrue(s.status()["held"])
                with self.assertRaisesRegex(RecursionRefusal,"LIFE_AMBIGUOUS_OPERATION"):s.historical_checkpoint()
                self.assertEqual(p.calls,1)
                self.assertEqual(rt.ledger.events(),before)
            finally:s.close();rt.close()


    def test_exact_compiled_live_request_same_native_lexical_afterlife(self):
        import sqlite3
        from importlib.util import spec_from_file_location,module_from_spec
        from copy import deepcopy
        import test_live_turn_r38 as old
        from live_turn_port_r38 import LiveTurnSession
        from neighbor_runtime import NeighborEncounter
        spec=spec_from_file_location("um_sorok_organism.r53_transport",
            Path(__file__).parent/"um_sorok_organism"/"live_psychological_llm.py")
        mod=module_from_spec(spec);spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as d:
            folder=Path(d);source=folder/"source.sqlite"
            rt=old.OneResponseLiveCourt.setup_lexical(self,source);rt.close()
            results=[]
            for compact in (False,True):
                db=folder/("compact.sqlite" if compact else "full.sqlite")
                with sqlite3.connect(source) as origin,sqlite3.connect(db) as dest:origin.backup(dest)
                packets=[];wire_rows=[]
                def mock(req):
                    doc=json.loads(req["messages"][1]["content"])
                    wire_rows.append(doc)
                    doc=mod.expand_live_wire_request(doc)
                    packets.append(doc)
                    a=doc["principal"]
                    if a=="speaker":
                        speak=policy([{"action":"SPEAK","pool":"addressed_lexical_options",
                            "option_match":{"project_id":"talk","world_request":{"addressed_party_ref":"listener"}},
                            "speech_intent":"Share a worry."}])
                        speak["expression"]={"speech":old.WORDS,"surface":"Ordinary life."}
                        learn=policy([], [{"offer":"historically_possible_lexical_project_revaluations",
                            "construct":"LEXICAL_PROJECT_REVALUATION","match":{"project_id":"work",
                            "lexical_revaluation_basis":{"lexical_acquisition_route":"VOLUNTARILY_ADDRESSED_TO_SELF"}},
                            "augment":{"priority":.1,"personal_significance":"Perhaps I can take a moment to listen."}}])
                        ans={"policies":{"speaker":speak,"listener":learn}}
                    else:ans={"policies":{"listener":policy([{"action":"SELECT_HIGHEST_CURRENT_PROJECT_COURSE",
                        "project_course_actions":["WORK","REST"]},action("WAIT")])}}
                    return {"choices":[{"message":{"content":json.dumps(ans)}}]}
                wire=mod.ExplicitLiveTurnProvider(endpoint="https://example.invalid/chat/completions",
                    model="fixture",api_key="not-a-key",allow_private_actor_data=True,
                    sourcefree_live_attested=True,transport=mock,metrics_capacity=8,
                    compact_exact_packet=compact,compact_structured_packet=compact)
                rt=ConstitutiveRuntime(str(db));session=LiveTurnSession(rt,wire,
                     folder/("compact-attempt.sqlite" if compact else "full-attempt.sqlite"),sourcefree_attested=True)
                try:
                    n=NeighborEncounter(rt,"visitor",mii_module=mii)
                    self.assertEqual(session.owner_actor_beat(n,"listener")["attempt"],"WORK")
                    old.geometry(n,["speaker","listener"])
                    self.assertEqual(session.owner_actor_beat(n,"speaker")["attempt"],"SPEAK")
                    view=n.private_surface(n.new_private_profile())
                    self.assertIn(old.WORDS,json.dumps(view));self.assertNotIn(old.PRIVATE,json.dumps(view))
                    self.assertEqual(session.owner_actor_beat(n,"listener")["attempt"],"REST")
                    self.assertTrue(rt.verify()["valid"])
                    result={"packets":packets,"history":rt.ledger.events(),"actors":rt.ledger.actors(),
                            "world":rt.ledger.world(),"metrics":wire.usage_snapshot()["receipts"],"view":view}
                    self.assertEqual(len(packets),3)
                    results.append(result)
                finally:session.close();rt.close()
            a,b=results
            for k in ("packets","history","actors","world","view"):self.assertEqual(a[k],b[k],k)
            full=sum(r["request_bytes"] for r in a["metrics"])
            small=sum(r["request_bytes"] for r in b["metrics"])
            self.assertLess(small,full)
            self.assertTrue(any(r["alias_count"]+r["structured_field_count"]>0 for r in b["metrics"]))
            print("R53_LIVE_EXACT",json.dumps({"full_bytes":full,"compact_bytes":small,
                "calls_each":len(a["metrics"]),"exact_native_history":True,
                "aliases":sum(r["alias_count"] for r in b["metrics"]),
                "structured":sum(r["structured_field_count"] for r in b["metrics"])},sort_keys=True))


    def test_matched_longer_history_selective_context_whole_wire_and_native_equality(self):
        import sqlite3
        from copy import deepcopy
        from importlib.util import spec_from_file_location,module_from_spec
        from modern_generation_port_r28 import ModernDevelopmentOwner,ModernGeneration
        spec=spec_from_file_location("um_sorok_organism.r54_transport",
             Path(__file__).parent/"um_sorok_organism"/"live_psychological_llm.py")
        mod=module_from_spec(spec);spec.loader.exec_module(mod)
        class MemoryCourse:
            def __init__(self):self.requests=[]
            def call(self,r):
                self.requests.append(r);ctx=r["context"];n=len(self.requests)
                if r["mode"]=="TERMINAL":return {"retrospective":retro(r),"prospective":None}
                # The older memory informs an identical semantic decision in
                # both profiles through exact selected retrieval, not through
                # a forced equivalence of actual model reasoning.
                reads=ctx["selected_exact_analytic_reads"]
                recovered=(n==6 and len(reads)==1 and
                           reads[0]["value"]["content"].startswith("Actual rest 1:0:"))
                rows=[]
                for i in range(5):
                    c={"kind":"MEMORY","content":f"Actual rest {n}:{i}: "+("the afternoon passed. "*18),
                       "cue_terms":["rest"]}
                    op="WAIT" if recovered and i==0 else "REST"
                    rows.append(event(ctx,f"{n}:{i}",ctx["clock"]+i+1,"worker",{"worker":policy(
                        [action(op)],[{"candidate":c,"when":{"own_action":"REST","status":"PERFORMED"}}])}))
                if n==4:
                    rows[-1]["circumstances"]["next_analytic_reads"]=[
                        {"kind":"ACTOR_DOMAIN_PAGE","actor":"worker","domain":"memories","offset":0,"limit":3}]
                if n==5:
                    page=reads[0]["value"]
                    rows[-1]["circumstances"]["next_analytic_reads"]=[
                        {"kind":"ACTOR_ROW","actor":"worker","domain":"memories","row_ref":page["rows"][0]["row_ref"]}]
                return {"retrospective":retro(r),"prospective":rows}
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);source=root/"source.sqlite";rt=ConstitutiveRuntime(str(source))
            rt.ledger.initialize(blank_world(),[adult("worker","Mara")]);rt.close()
            results=[]
            for compact in (False,True):
                folder=root/str(compact);folder.mkdir();db=folder/"life.sqlite"
                with sqlite3.connect(source) as origin,sqlite3.connect(db) as dest:origin.backup(dest)
                p=MemoryCourse()
                def mock(req):
                    ans=p.call(json.loads(req["messages"][1]["content"]))
                    return {"choices":[{"message":{"content":json.dumps(ans)}}]}
                wire=mod.ExplicitDevelopmentalCheckpointProvider(endpoint="https://example.invalid/chat/completions",
                    model="fixture",api_key="not-a-key",allow_private_actor_data=True,
                    sourcefree_checkpoint_attested=True,transport=mock,metrics_capacity=12)
                def open_g(rt):
                    return ModernGeneration(ModernDevelopmentOwner(rt,"worker",folder/"ops.sqlite",
                        sourcefree_attested=True,selective_memory_context=compact),
                        wire,folder/"batch.sqlite",folder/"cycle.json")
                rt=ConstitutiveRuntime(str(db));g=open_g(rt)
                try:
                    g.bootstrap()
                    for _ in range(4):g.advance()
                    self.assertEqual(len(rt.snapshot("worker")["memories"]),25)
                finally:g.close();rt.close()
                rt=ConstitutiveRuntime(str(db));g=open_g(rt)
                try:
                    batch=g.advance()
                    self.assertEqual(batch["records"][0]["objective"]["attempt"],"WAIT")
                    g.advance();g.finish()
                    self.assertTrue(g.engine.verify());self.assertTrue(rt.verify()["valid"])
                    rows=wire.usage_snapshot()["receipts"]
                    results.append({"events":rt.ledger.events(),"actors":rt.ledger.actors(),
                        "world":rt.ledger.world(),"records":rows,"retrieved":p.requests[5]["context"]["selected_exact_analytic_reads"],
                        "memories":len(rt.snapshot("worker")["memories"])})
                finally:g.close();rt.close()
            a,b=results
            for k in ("events","actors","world","retrieved","memories"):self.assertEqual(a[k],b[k],k)
            full=[r["request_bytes"] for r in a["records"]];small=[r["request_bytes"] for r in b["records"]]
            self.assertEqual(len(full),8);self.assertEqual(len(small),8)
            self.assertLess(sum(small),sum(full))
            print("R54_HISTORY_CONTEXT",json.dumps({"full_bytes":sum(full),"compact_bytes":sum(small),
                "full_by_checkpoint":full,"compact_by_checkpoint":small,"memories":a["memories"],
                "native_events":len(a["events"]),"exact_native_history":True},sort_keys=True))


    def test_acquired_relational_contradiction_revaluation_consumed_in_live_turn(self):
        from copy import deepcopy
        from modern_generation_port_r28 import ConditionalPolicy
        from live_turn_port_r38 import LiveTurnSession
        from neighbor_runtime import NeighborEncounter
        from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService,HeuristicSemanticProvider
        # Reuse the native R32 lived cross-context mechanism. The actual
        # setup/rest in the inhibited field is a disclosed research act.
        # The later independent live policy never forces a suppressed action.
        parent={"source_ref":"R56_FICTIONAL_PARENT","source_grade":"SOURCEFREE_TEST_FIXTURE_NOT_EMPIRICAL",
                "answers":{"r56":"not_a_survey_observation"},"fictional_seed":{"projects":[]}}
        for nominate in (True,False):
            with self.subTest(nominate=nominate),tempfile.TemporaryDirectory() as d:
                root=Path(d);db=root/"life.sqlite"
                fallback=HeuristicSemanticProvider()
                def setup(task,p):
                    if task!="development":return fallback.propose(task,p)
                    if p["actor"]["id"]!="mother":return {"task":task,"candidates":[]}
                    if p["experience"].get("own_action")=="WAIT" and "r56_care" not in p["actor_forms"]:
                        forms=[{"kind":"ADD_FORM","form":{"id":ident,"kind":"PRACTICE","cues":["rest"],
                            "enables":[op],"always_recruitable":True,"scope":{"locations":["workshop"]}}}
                            for ident,op in (("r56_care","CARE"),("r56_duty","REST"))]
                        forms.append({"kind":"ACQUIRE_RELATIONAL_MOTIF","motif":{
                            "source_forms":["r56_care","r56_duty"],"locations":["workshop"],"effects":[{
                                "kind":"RELATION_MEDIATION","source":"r56_care","target":"r56_duty",
                                "relation":"SUBORDINATES","mediated_action":"REST","polarity":"WITHHOLD"}]}})
                        return {"task":task,"candidates":forms}
                    return {"task":task,"candidates":p.get("historically_possible_lived_directional_orientation",[])
                        if p["experience"].get("location")=="home" else []}
                rt=ConstitutiveRuntime(str(db),semantic=ValidatingSemanticService(CallbackLLMProvider(setup)))
                try:
                    rt.initialize([("mother","Mother",parent),("father","Father",parent)])
                    rt.step("mother",requested_action="WAIT")
                    rt.step("mother",requested_action="REST");rt.step("mother",requested_action="REST")
                    old=deepcopy(rt.snapshot("mother")["relational_motifs"][0])
                    orientation=deepcopy(rt.snapshot("mother")["historical_orientations"])
                    self.assertTrue(orientation)
                    rt.step("mother",requested_action="MOVE",object_ref="workshop")
                    self.assertNotIn("REST",{o["action"] for o in rt.situated("mother")["candidate_actions"]})
                    rule={"offer":"historically_possible_lived_cross_context_revaluations",
                          "construct":"LIVED_CROSS_CONTEXT_REVALUATION",
                          "augment":{"new_relation":"SUPPORTS","new_polarity":"APPROACH",
                              "interpretive_hypothesis":"Rest may sustain care rather than betray duty."}}
                    from modern_generation_port_r28 import policy_check
                    pol=policy([], [rule] if nominate else []);policy_check(pol)
                    compiler=ConditionalPolicy({"mother":pol})
                    rt.semantic=ValidatingSemanticService(compiler)
                    self.assertEqual(rt.step("mother",requested_action="REST")["status"],"PERFORMED")
                    row=deepcopy(rt.snapshot("mother")["relational_motifs"][0])
                    self.assertEqual(compiler.routes["typed_lived_cross_context_revaluation"],int(nominate))
                    self.assertEqual(row["origin"],old["origin"])
                    self.assertEqual(rt.snapshot("mother")["historical_orientations"],orientation)
                    self.assertEqual(row["effects"][0]["polarity"],"APPROACH" if nominate else "WITHHOLD")
                finally:rt.close()
                rt=ConstitutiveRuntime(str(db));provider=Live()
                session=LiveTurnSession(rt,provider,root/"live.sqlite",sourcefree_attested=True)
                try:
                    n=NeighborEncounter(rt,"visitor",mii_module=mii)
                    out=session.owner_actor_beat(n,"mother")
                    self.assertEqual(out["attempt"],"REST" if nominate else "WAIT")
                    self.assertEqual(len(provider.requests),1)
                    self.assertEqual(rt.snapshot("mother")["relational_motifs"][0],row)
                    self.assertTrue(rt.verify()["valid"])
                    print("R56_RELATIONAL_REVALUE",json.dumps({"nominate":nominate,
                        "later":out["attempt"],"live_calls":len(provider.requests)},sort_keys=True))
                finally:session.close();rt.close()

    def test_witnessed_other_relation_formed_only_from_actual_received_directed_act(self):
        from live_turn_port_r38 import LiveTurnSession
        from neighbor_runtime import NeighborEncounter
        for present,nominate in ((True,True),(True,False),(False,True)):
            with self.subTest(present=present,nominate=nominate),tempfile.TemporaryDirectory() as d:
                root=Path(d);db=root/"life.sqlite";rt=ConstitutiveRuntime(str(db))
                a=adult("father","Father");a["projects"]=[{"id":"impose","object":"obtain compliance",
                    "means":["IMPOSE"],"addressed_party_ref":"mother","status":"active","priority":.6}]
                rt.ledger.initialize(blank_world(),[a,adult("mother","Mother"),
                    adult("witness","Witness","home" if present else "workshop")])
                class Provider:
                    def __init__(self):self.calls=0
                    def call(self,r):
                        self.calls+=1
                        policies={"father":policy([action("IMPOSE",{"project_id":"impose",
                            "world_request":{"addressed_party_ref":"mother"}})])}
                        if "witness" in r["peer_tips"]:
                            policies["witness"]=policy([], [{"offer":"historically_possible_witnessed_third_party_relations",
                                "construct":"WITNESSED_OTHER_RELATION","match":{"source_actor_ref":"father",
                                    "target_actor_ref":"mother","witnessed_act":"IMPOSE"},
                                "augment":{"hypothesis":"I may have misunderstood their relation."}}] if nominate else [])
                        return {"policies":policies}
                p=Provider();session=LiveTurnSession(rt,p,root/"live.sqlite",sourcefree_attested=True)
                try:
                    n=NeighborEncounter(rt,"visitor",mii_module=mii)
                    out=session.owner_actor_beat(n,"father")
                    self.assertEqual(out["attempt"],"IMPOSE");self.assertEqual(out["status"],"PERFORMED")
                    models=rt.snapshot("witness")["other_models"].get("father",[])
                    self.assertEqual(len(models),int(present and nominate))
                    if models:
                        self.assertEqual(models[0]["about_relation_with_ref"],"mother")
                        self.assertTrue(models[0]["not_other_private_state_or_target_consent"])
                    self.assertTrue(rt.verify()["valid"])
                    self.assertEqual(p.calls,1)
                    print("R56_WITNESSED_RELATION",json.dumps({"present":present,"nominate":nominate,
                        "retained_hypotheses":len(models),"live_calls":p.calls},sort_keys=True))
                finally:session.close();rt.close()

if __name__=="__main__":unittest.main()


class JoinedRoutineContinuityCourt(unittest.TestCase):
    """Actual independently acquired practice across generation/live/generation.

    No external routine envelope, injected behavior or invented daily exercise.
    The same compiled policy can revise a particular course on a fresh own act.
    """
    def test_shared_acquired_course_survives_and_changes_across_live_epochs(self):
        class History:
            def __init__(self):self.requests=[];self.resumed=False
            def call(self,r):
                self.requests.append(r);ctx=r["context"];clock=ctx["clock"];n=len(self.requests)
                if r["mode"]=="TERMINAL":return {"retrospective":retro(r),"prospective":None}
                def e(label,offset,actor,acts,rules=(),span=0,peers=None):
                    return event(ctx,str(n)+":"+label,clock+offset,actor,
                        {actor:policy(acts,rules),**(peers or {})},span=span)
                if self.resumed or n==4:
                    rows=[e("coarse",7,"a",[action("REST")],span=6),
                          e("rest-b",8,"b",[action("REST")]),
                          e("rest-a",9,"a",[action("REST")])]
                else:
                    nomination={"offer":"historically_possible_recurrent_routines",
                        "construct":"RECURRENT_ROUTINE","match":{"basis":{"operation":"SING"}},
                        "augment":{"window_days":80,"hours_per_active_day":2.,
                                   "provisional_exposure_fraction":.5}}
                    rows=[e("rest-a",1,"a",[action("REST")]),
                          e("rest-b",2,"b",[action("REST")]),
                          e("song",3,"a",[action("SING",{"project_id":"a-song"})],[nomination],
                            peers={"b":policy([action("SING",{"project_id":"b-song"})],[nomination])})]
                return {"retrospective":retro(r),"prospective":rows}
        class Revision:
            def __init__(self):self.requests=[];self.mode="PAUSE"
            def call(self,r):
                self.requests.append(r);aid=r["principal"]
                rules=[{"offer":"historically_possible_routine_revisions",
                    "construct":"RECURRENT_ROUTINE_REVISION","match":{"basis":{"operation":"SING"}},
                    "augment":{"mode":self.mode,"interpretive_hypothesis":"Alter my own ordinary contribution."}}] if aid=="b" else []
                return {"policies":{aid:policy([action("REST")],rules)}}
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);db=root/"life.sqlite"
            rt=ConstitutiveRuntime(str(db));a=adult("a","A");b=adult("b","B")
            for person,peer in ((a,"b"),(b,"a")):
                person["projects"]=[{"id":person["id"]+"-song","object":"sing together",
                    "means":["SING"],"addressed_party_ref":peer,"status":"active","priority":.7}]
            rt.ledger.initialize(blank_world(),[a,b])
            hist=History();live=Revision()
            def open_life():return ContinuingLife(rt,root/"operator","a",historical_provider=hist,
                        live_provider=live,sourcefree_attested=True,mii_module=mii)
            def world():return rt.ledger.world()[1]
            def routine(aid):return rt.snapshot(aid)["projects"][0]["recurrent_routines"][0]
            def periods(start):return [x for x in world()["historical_periods"] if x["start"]>=start]
            def revise(s,mode):
                live.mode=mode
                begin=len(live.requests)
                for _ in range(4):
                    s.independent_absent_beat()
                    rows=routine("b").get("revisions",[])
                    if rows and rows[-1]["mode"]==mode:
                        self.assertIn("b",[q["principal"] for q in live.requests[begin:]])
                        return
                self.fail("independent actor did not revise own routine: principals="+
                          str([q["principal"] for q in live.requests[begin:]]))
            s=open_life()
            try:
                for _ in range(3):s.historical_checkpoint()
                self.assertEqual(len(world()["routine_source_registry"]),2)
                source_a=routine("a")["id"];source_b=routine("b")["id"]
                start=world()["clock"];s.historical_checkpoint()
                self.assertTrue(periods(start))
                self.assertTrue(all({p["source_ref"] for p in x["processes"]}=={source_a,source_b}
                                    for x in periods(start)))
                self.assertEqual(sum(x["end"]-x["start"] for x in periods(start)),6)
                s.finish_history()
                revise(s,"PAUSE");self.assertFalse(routine("a").get("revisions"))
                old=deepcopy(world()["historical_periods"])
            finally:s.close();rt.close()
            rt=ConstitutiveRuntime(str(db));s=open_life()
            try:
                hist.resumed=True;start=world()["clock"];s.resume_history()
                self.assertTrue(periods(start));self.assertTrue(all(not x["processes"] for x in periods(start)))
                self.assertEqual(world()["historical_periods"][:len(old)],old)
                self.assertEqual(s.status()["epoch"],1)
                s.finish_history();revise(s,"RESUME")
                self.assertFalse(routine("a").get("revisions"))
                start=world()["clock"];s.resume_history()
                self.assertTrue(periods(start))
                self.assertTrue(all({p["source_ref"] for p in x["processes"]}=={source_a,source_b}
                                    for x in periods(start)))
                self.assertEqual(s.status()["epoch"],2)
                self.assertTrue(rt.verify()["valid"])
                self.assertTrue(all(x["status"]=="RETURNED" for x in s.receipts()))
                self.assertFalse(s.status()["held"])
                self.assertEqual(len(world()["routine_source_registry"]),2)
                self.assertEqual(len(routine("b")["revisions"]),2)
                print("R008_JOINED_ROUTINE_EPOCHS",len(hist.requests),len(live.requests),s.status()["epoch"])
            finally:s.close();rt.close()


class ElasticAppointmentEpochCourt(unittest.TestCase):
    """The same actual appointment owner across historical and live epochs."""
    def test_replacement_requires_fresh_actor_choice_after_absence_and_cold_history(self):
        from um_sorok_organism.material_conjunction import admit_authored_structural_history
        class History:
            def __init__(self):self.requests=[]
            def call(self,r):
                self.requests.append(r);ctx=r["context"];clock=ctx["clock"]
                if r["mode"]=="TERMINAL":return {"retrospective":retro(r),"prospective":None}
                n=len(self.requests)
                offsets=(1,2,4) if clock==16 else (1,2,3)
                prev=0;rows=[]
                for i,offset in enumerate(offsets):
                    rows.append(event(ctx,str(n)+":"+str(i),clock+offset,"worker",
                        {"worker":policy([action("WAIT")])},span=offset-prev-1))
                    prev=offset
                return {"retrospective":retro(r),"prospective":rows}
        class LiveAppointment:
            def __init__(self):self.requests=[];self.phase="ACCEPT_MEETING"
            def call(self,r):
                self.requests.append(r)
                op=self.phase
                rule=(action(op,{"grounds_status":"ACTUAL_ADDRESSED_MEETING_SIGN",
                                  "world_request":{"addressed_party_ref":"visitor"}})
                      if op in ("ACCEPT_MEETING","MEET_VISITOR")
                      else {"action":"WORK","project_id":"work"})
                return {"policies":{r["principal"]:policy([rule,action("WAIT")])}}
        for choose in (True,False):
            with self.subTest(choose=choose),tempfile.TemporaryDirectory() as d:
                root=Path(d);db=root/"life.sqlite"
                rt=ConstitutiveRuntime(str(db));w=blank_world()
                w["ambient"]["work_shifts"]={"worker":[{"start":14,"end":15,"source_ref":"fictional:shift"}]}
                w["ambient"]["work_shift_coverage_complete"]=True
                worker=adult("worker","Worker","workshop")
                worker["projects"]=[{"id":"work","object":"earn wage","means":["WORK"],"priority":.8,"status":"active"}]
                spec={"grade":"EXPLICIT_SOURCEFREE_STRUCTURAL_HISTORY","source_ref":"fictional:shift",
                      "positions":[],"rules":[{"id":"short_shift","operation":"WORK",
                          "location":"workshop","source_ref":"fictional:shift_gate",
                          "effective_from":0,"effective_until":None,"all_of":[{"kind":"SHIFT_OCCUPIED"}]}]}
                admit_authored_structural_history(w,{"worker"},spec)
                rt.ledger.initialize(w,[worker],source_seals=[("authored_structural_history",
                    "FICTIONAL_WORLD_CONDITIONING",spec)])
                hist=History();live=LiveAppointment()
                def open_life():return ContinuingLife(rt,root/"operator","worker",
                    historical_provider=hist,live_provider=live,sourcefree_attested=True,mii_module=mii)
                def clock():return rt.ledger.world()[1]["clock"]
                def rows(s):return {x["id"]:x for x in s.own_meetings("visitor")}
                def beat(s,occasion):
                    out=s.present_until("visitor",occasion,clock()+1)
                    self.assertEqual(out["beats_committed_this_call"],1)
                s=open_life()
                try:
                    s.historical_checkpoint();s.finish_history();self.assertEqual(clock(),3)
                    s.configure_encounter("visitor",{"grade":"SOURCEFREE_TEST_ONLY",
                        "user_conditions":{"workshop":{"light":"lit","sightline":"unobstructed",
                            "hearing":True,"sound_path":"audible","legibility":"readable"}},
                        "actor_conditions":{"worker":{"facing":"entrance","visual":True,
                            "light":"lit","sightline":"unobstructed","hearing":True,
                            "sound_path":"audible"}}},request_id="geometry")
                    s.contribute("visitor","enter","MOVE",destination="workshop")
                    first=s.contribute("visitor","old","PROPOSE_MEETING",target_actor_ref="worker",due_clock=18)
                    old=first["meeting_ref"];beat(s,first["event_ref"])
                    self.assertEqual(rows(s)[old]["status"],"ACCEPTED")
                    s.contribute("visitor","leave","LEAVE")
                    before=rt.ledger.actors()
                    s.contribute("visitor","withdraw","WITHDRAW_MEETING",target_commitment_ref=old)
                    self.assertEqual(rt.ledger.actors(),before)
                    self.assertEqual(rows(s)[old]["status"],"WITHDRAWN_BY_AUTHORED_ACT")
                    self.assertEqual(clock(),9)
                    s.resume_history();s.finish_history();self.assertEqual(clock(),12)
                    old_events=deepcopy(rt.ledger.events())
                finally:s.close();rt.close()
                rt=ConstitutiveRuntime(str(db));s=open_life()
                try:
                    s.contribute("visitor","return","MOVE",destination="workshop")
                    fresh=s.contribute("visitor","new","PROPOSE_MEETING",target_actor_ref="worker",
                                       target_commitment_ref=old,due_clock=24)
                    new=fresh["meeting_ref"];self.assertEqual(clock(),14)
                    live.phase="ACCEPT_MEETING" if choose else "WORK"
                    beat(s,fresh["event_ref"])
                    self.assertEqual(rows(s)[new]["status"],"ACCEPTED" if choose else "PROPOSED")
                    self.assertEqual(rt.ledger.world()[1]["accounts"].get("worker",0),0 if choose else .25)
                    s.contribute("visitor","leave-again","LEAVE");self.assertEqual(clock(),16)
                    s.resume_history();s.finish_history();self.assertEqual(clock(),20)
                    self.assertEqual(rt.ledger.events()[:len(old_events)],old_events)
                finally:s.close();rt.close()
                rt=ConstitutiveRuntime(str(db));s=open_life()
                try:
                    s.contribute("visitor","arrive","MOVE",destination="workshop")
                    if choose:
                        check=s.contribute("visitor","checkin","CHECK_IN_MEETING",target_commitment_ref=new)
                        live.phase="MEET_VISITOR";beat(s,check["event_ref"])
                        self.assertEqual(rows(s)[new]["status"],"MEETING_PERFORMED")
                        self.assertEqual(len(live.requests),3)
                    else:
                        with self.assertRaisesRegex(ValueError,"MEETING_CHECKIN_NOT_AUTHORIZED"):
                            s.contribute("visitor","checkin","CHECK_IN_MEETING",target_commitment_ref=new)
                        self.assertEqual(len(live.requests),2)
                        self.assertFalse(s.status()["held"])
                    self.assertEqual(rows(s)[old]["status"],"WITHDRAWN_BY_AUTHORED_ACT")
                    self.assertEqual(rows(s)[old]["replacement_meeting_ref"],new)
                    self.assertEqual(rows(s)[new]["replaces_meeting_ref"],old)
                    self.assertEqual(s.status()["epoch"],2)
                    self.assertTrue(rt.verify()["valid"])
                    print("R008_ELASTIC_APPOINTMENT_EPOCHS",choose,len(hist.requests),len(live.requests),clock())
                finally:s.close();rt.close()
