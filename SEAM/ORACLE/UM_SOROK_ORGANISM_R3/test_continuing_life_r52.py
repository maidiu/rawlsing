"""R52 actual owner-mode operation, no manually stitched epoch internals."""
import json
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


    def test_affect_qualified_private_rehearsal_new_end_trial_and_later_project(self):
        from live_turn_port_r38 import LiveTurnSession
        from neighbor_runtime import NeighborEncounter
        from test_rich_formation_r44 import rich
        from copy import deepcopy
        for nominate in (True,False):
            with self.subTest(nominate=nominate),tempfile.TemporaryDirectory() as d:
                root=Path(d);db=root/"life.sqlite";rt=ConstitutiveRuntime(str(db))
                a=adult("worker","Mara");a["projects"]=[{"id":"duty","object":"sustain availability",
                    "means":["REST","SPEAK"],"status":"active","priority":.5,
                    "expected_difference":{"feature":"availability","direction":"PRESERVE","sign_tags":["wait"]}}]
                rt.ledger.initialize(blank_world(),[a])
                secret="Quiet need not mean abandoning a commitment."
                class Provider:
                    def __init__(self):self.calls=0;self.stage=0
                    def call(self,r):
                        self.calls+=1;stage=self.stage
                        if stage==0:p=policy([{"action":"REST","project_id":"duty"}])
                        elif stage==1:p=policy([action("WAIT")],[rich("delayed_appraisals","DELAYED_APPRAISAL",appraisal="ACTOR_INTERPRETS_DISAPPOINTED")])
                        elif stage==2:p=policy([action("WAIT")],[
                            rich("activity_affects","ACTIVITY_AFFECT",affect_name="unease",personal_sense="quiet conflicts with duty",course_orientation="APPROACH"),
                            {"candidate":{"kind":"MEMORY","content":"The quiet interval felt like letting someone down.","cue_terms":["wait"]},
                             "when":{"own_action":"WAIT","status":"PERFORMED"}}])
                        elif stage==3:
                            p=policy([action("WAIT")],[{"private_construct":"NOTICE_END","augment":{
                                "possible_object":"Attend without promising availability","means":["ORIENT"]}}] if nominate else [])
                            p["private_rehearsal"]={"affect":"REQUIRED","meaning":secret}
                        elif stage==4:
                            rows=[q for q in r["principal_packet"]["possible_end_trials"] if q.get("private_rehearsal_ref")]
                            p=policy(([{"action":"ORIENT","pool":"possible_end_trials","option_match":{
                                "possible_end_ref":rows[0]["possible_end_ref"]}}] if rows else [])+[action("WAIT")])
                        elif stage==5:p=policy([action("ORIENT")],[{"private_construct":"TAKE_UP_END",
                                "augment":{"means":["ORIENT"]},"match":{"possible_object":"Attend without promising availability"}}])
                        else:p=policy([{"action":"SELECT_HIGHEST_CURRENT_PROJECT_COURSE","project_course_actions":["ORIENT"]},action("WAIT")])
                        return {"policies":{"worker":p}}
                p=Provider();session=LiveTurnSession(rt,p,root/"live.sqlite",sourcefree_attested=True)
                try:
                    n=NeighborEncounter(rt,"visitor",mii_module=mii)
                    for stage in range(4):
                        p.stage=stage;self.assertEqual(session.owner_actor_beat(n,"worker")["status"],"PERFORMED")
                    before=rt.snapshot("worker")
                    recs=[x for m in before["memories"] for x in m.get("private_rehearsals",[])]
                    self.assertEqual(len(recs),1);self.assertTrue(recs[0]["affect_ref"])
                    ends=[e for e in before["possible_ends"] if e.get("genesis_family")=="ACTUAL_PRIVATE_REHEARSAL"]
                    self.assertEqual(len(ends),int(nominate))
                    self.assertNotIn(secret,json.dumps(rt.ledger.world()[1]))
                    p.stage=4;out=session.owner_actor_beat(n,"worker")
                    self.assertEqual(out["attempt"],"ORIENT" if nominate else "WAIT")
                    self.assertFalse(any(x.get("possible_end_ref") for x in rt.snapshot("worker")["projects"]))
                    p.stage=5;self.assertEqual(session.owner_actor_beat(n,"worker")["status"],"PERFORMED")
                    after=rt.snapshot("worker")
                    projects=[x for x in after["projects"] if x.get("possible_end_ref")]
                    self.assertEqual(len(projects),int(nominate))
                    self.assertEqual(after["memories"],before["memories"])
                    if nominate:self.assertTrue(projects[0]["takeup_evidence"]["private_takeup_basis"])
                finally:session.close();rt.close()
                rt=ConstitutiveRuntime(str(db));session=LiveTurnSession(rt,p,root/"live.sqlite",sourcefree_attested=True)
                try:
                    p.stage=6;out=session.owner_actor_beat(NeighborEncounter(rt,"visitor",mii_module=mii),"worker")
                    self.assertEqual(out["attempt"],"ORIENT" if nominate else "WAIT")
                    self.assertTrue(rt.verify()["valid"])
                    self.assertEqual(p.calls,7)
                    print("R57_PRIVATE_END",json.dumps({"nominate":nominate,"later":out["attempt"],
                        "projects":len(projects),"calls":p.calls,"affect_qualified":True},sort_keys=True))
                finally:session.close();rt.close()

if __name__=="__main__":unittest.main()


    def test_one_existing_budget_across_history_live_resume_and_cold_hold(self):
        from importlib.util import spec_from_file_location,module_from_spec
        from unittest.mock import patch
        import sys
        folder=Path(__file__).parent/"um_sorok_organism"
        def module(name,path):
            spec=spec_from_file_location(name,path)
            mod=module_from_spec(spec);spec.loader.exec_module(mod);return mod
        wire=module("um_sorok_organism.r58_wire",folder/"live_psychological_llm.py")
        with patch.dict(sys.modules,{"um_sorok_organism.live_psychological_llm":wire}):
            lab=module("um_sorok_organism.r58_lab",folder/"inference_lab.py")
            with tempfile.TemporaryDirectory() as d:
                root=Path(d);db=root/"life.sqlite"
                rt,sid,catalog,_=joined.JoinedGenerationCourt.setup(self,db)
                h1=joined.LifeCheckpoint(sid);h2=joined.LifeCheckpoint(sid,resumed=True)
                l=Live();seen=[]
                b=lab.LiveBudget(journal=root/"budget.json",max_calls=6,max_wire_bytes=10000000,
                    input_token_ceiling=100000,completion_token_limit=1000,input_nanos_per_token=2,
                    output_nanos_per_token=5,max_budget_nanos=2000000,sourcefree_live_authorized=True)
                common=dict(budget=b,endpoint="https://example.invalid/chat/completions",
                    model="fixture",api_key="not-a-key",allow_private_actor_data=True,metrics_capacity=1)
                hp=lab.budgeted_combined_provider("HISTORICAL",sourcefree_checkpoint_attested=True,**common)
                lp=lab.budgeted_combined_provider("LIVE",sourcefree_live_attested=True,**common)
                def hermetic(provider,payload):
                    self.assertTrue(b.pending)
                    self.assertEqual(payload["max_completion_tokens"],1000)
                    doc=json.loads(payload["messages"][1]["content"])
                    if "mode" in doc:
                        result=(h1 if len(h1.requests)<4 else h2).call(doc)
                    else:result=l.call(doc)
                    seen.append("HISTORICAL" if "mode" in doc else "LIVE")
                    return {"choices":[{"message":{"content":json.dumps(result)}}],
                            "usage":{"prompt_tokens":200,"completion_tokens":50,"total_tokens":250}}
                def open_life(runtime):
                    return ContinuingLife(runtime,root/"operator","mother",historical_provider=hp,
                       live_provider=lp,sourcefree_attested=True,period_catalog=catalog,
                       family_sources=(sid,),mii_module=mii)
                s=open_life(rt)
                try:
                    with patch.object(wire.ExplicitJSONLLMProvider,"_request",hermetic):
                        s.historical_checkpoint();s.historical_checkpoint();s.historical_checkpoint()
                        s.finish_history()
                        self.assertEqual(rt.snapshot("nadia")["age_days"],100)
                        s.independent_absent_beat()
                        s.resume_history()
                        self.assertEqual(rt.snapshot("nadia")["age_days"],170)
                        before=rt.ledger.events()
                        # Same single allowance, no additional send in either mode.
                        with self.assertRaises(Exception):s.finish_history()
                        self.assertEqual(rt.ledger.events(),before)
                        self.assertTrue(s.status()["held"])
                        self.assertEqual(seen,["HISTORICAL"]*4+["LIVE","HISTORICAL"])
                        self.assertEqual(b.calls,6);self.assertTrue(b.stopped)
                        self.assertEqual(b.estimated_reported,3900)
                        last=hp.usage_snapshot()["receipts"][-1]
                        self.assertEqual(last["attempts"],0)
                        self.assertEqual(last["budget_disposition"],"PREFLIGHT_REFUSED")
                        self.assertIsNone(last["budget_attempt"])
                        self.assertEqual(lp.usage_snapshot()["receipts"][-1]["budget_attempt"],5)
                        import sqlite3
                        with sqlite3.connect(root/"operator"/"epoch-000001"/"ops.sqlite") as cx:
                            rows=[json.loads(x[0]) for x in cx.execute("SELECT receipt FROM checkpoint_attempts ORDER BY id")]
                        self.assertEqual(rows[0]["transport_receipt"]["budget_attempt"],6)
                        self.assertEqual(rows[-1]["transport_receipt"]["attempts"],0)
                        self.assertEqual(rows[-1]["cycle_disposition"],"HELD_OR_FAILED")
                        self.assertEqual(len(b.log.read_text().splitlines()),12)
                finally:s.close();rt.close()
                rt=ConstitutiveRuntime(str(db));s=open_life(rt)
                try:
                    with self.assertRaisesRegex(RecursionRefusal,"LIFE_AMBIGUOUS_OPERATION"):s.finish_history()
                    self.assertEqual(rt.ledger.events(),before);self.assertEqual(len(seen),6)
                finally:s.close();rt.close()

    def test_shared_budget_unknown_usage_and_concurrent_denial_are_not_free_calls(self):
        from importlib.util import spec_from_file_location,module_from_spec
        from unittest.mock import patch
        import sys
        folder=Path(__file__).parent/"um_sorok_organism"
        def module(name,path):
            spec=spec_from_file_location(name,path)
            mod=module_from_spec(spec);spec.loader.exec_module(mod);return mod
        wire=module("um_sorok_organism.r58_wire",folder/"live_psychological_llm.py")
        with patch.dict(sys.modules,{"um_sorok_organism.live_psychological_llm":wire}):
            lab=module("um_sorok_organism.r58_lab",folder/"inference_lab.py")
            with tempfile.TemporaryDirectory() as d:
                b=lab.LiveBudget(journal=Path(d)/"budget",max_calls=2,max_wire_bytes=100000,
                    input_token_ceiling=1000,completion_token_limit=100,input_nanos_per_token=2,
                    output_nanos_per_token=5,max_budget_nanos=10000,sourcefree_live_authorized=True)
                common=dict(budget=b,endpoint="https://example.invalid/chat/completions",
                    model="fixture",api_key="not-a-key",allow_private_actor_data=True,metrics_capacity=2)
                hp=lab.budgeted_combined_provider("HISTORICAL",sourcefree_checkpoint_attested=True,**common)
                lp=lab.budgeted_combined_provider("LIVE",sourcefree_live_attested=True,**common)
                request={"mode":"BOOTSTRAP","context":{"grade":
                    "PROVISIONAL_SOURCEFREE_MODERN_GENERATION_PORT_NOT_NATIVE_OR_MODEL_ADEQUACY"},"previous":None}
                live_request={"grade":"SOURCEFREE_CONDITIONAL_LIVE_TURN_NOT_MODEL_ADEQUACY","source":"fixture",
                    "principal":"a","principal_packet":{"actor":{"id":"a"}},"peer_tips":{}}
                seen=[]
                def unknown(provider,payload):
                    seen.append(payload)
                    with self.assertRaisesRegex(lab.BudgetStop,"CONCURRENT"):lp.call(live_request)
                    self.assertTrue(b.pending)
                    return {"choices":[{"message":{"content":"{}"}}],"usage":{"prompt_tokens":23}}
                with patch.object(wire.ExplicitJSONLLMProvider,"_request",unknown):
                    with self.assertRaises(lab.BudgetStop):hp.call(request)
                    with self.assertRaises(lab.BudgetStop):lp.call(live_request)
                self.assertEqual(len(seen),1);self.assertEqual(b.calls,1);self.assertTrue(b.stopped)
                self.assertEqual(hp.usage_snapshot()["receipts"][-1]["budget_disposition"],"RESERVATION_UNCERTAIN")
                self.assertEqual([x["attempts"] for x in lp.usage_snapshot()["receipts"]],[0,0])
                self.assertIn('"input_tokens":23',b.log.read_text())
                self.assertIn("UNCERTAIN_SPEND_STOP",b.log.read_text())
