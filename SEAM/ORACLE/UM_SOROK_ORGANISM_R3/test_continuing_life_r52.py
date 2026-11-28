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


    def test_R79_actual_developing_child_affect_memory_through_checkpoint_encounter_and_resumption(self):
        """Continue the actual R78 childhood at its already acquired local concern.
        No injected child project, generic memory substitute or old owner checkout.
        Both arms use the same actual affect and policy; only qualified memory
        nomination order differs. The visitor is an authored fictional fixture.
        """
        import importlib.util
        from copy import deepcopy
        from um_sorok_organism.types import canonical
        spec=importlib.util.spec_from_file_location("actual_r78_childhood",
            Path(__file__).parent/"tests"/"test_early_ordinary_practice_r66.py")
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        secret="The sound was mine, but doing it here felt difficult."
        rehearsal="I can stop and be quiet for a while."
        obj="make room for a quieter pause"
        for nominate in (True,False):
            with self.subTest(nominate=nominate),tempfile.TemporaryDirectory() as d:
                root=Path(d);db=root/"life.sqlite"
                def continue_actual(rt,reopen):
                    entry=deepcopy(rt.ledger.actor("nadia")[1]);proj=entry["projects"][0]["id"]
                    work=[p for p in rt.ledger.actor("father")[1]["projects"] if p["object"]=="subsistence"]
                    self.assertEqual(len(work),1);work_proj=work[0]["id"]
                    shared_projects={a:next(p["id"] for p in rt.ledger.actor(a)[1]["projects"]
                        if p["object"]=="ordinary shared singing") for a in ("father","mother")}
                    self.assertEqual(entry["location"],"workshop")
                    self.assertEqual(entry["body"]["language"],.35)
                    self.assertEqual(entry["memories"],[])
                    self.assertEqual(len(entry["projects"]),1)
                    match={"formation_source":"OWN_ORDINARY_PROJECT_EXERCISE","object_affect_ref":None,
                           "project_ref":proj}
                    def affect(orientation):
                        return {"offer":"historically_possible_activity_affects","construct":"ACTIVITY_AFFECT",
                            "match":match,"augment":{"affect_name":"reticence" if orientation=="WITHHOLD" else "interest",
                                "personal_sense":"a provisional significance of the actually exercised concern",
                                "course_orientation":orientation}}
                    memory={"offer":"historically_possible_activity_affects","construct":"ORDINARY_AFFECT_MEMORY",
                            "match":match,"augment":{"content":secret,"cue_terms":["sing"]}}
                    def sing():return {"action":"SING","project_id":proj}
                    def course():
                        return policy([{"action":"SELECT_HIGHEST_CURRENT_PROJECT_COURSE",
                                        "project_course_actions":["REST"]},sing(),action("WAIT")])
                    def rows(r,plan):
                        ctx=r["context"];t=ctx["clock"];out=[]
                        for i,(who,p,span) in enumerate(plan):
                            t+=span+1
                            out.append(event(ctx,"r79:"+str(t)+":"+str(i),t,who,p if who in p else {who:p},span=span))
                        return {"retrospective":retro(r),"prospective":out}
                    class History:
                        def __init__(self,resumed=False):self.calls=[];self.resumed=resumed
                        def call(self,r):
                            self.calls.append(r)
                            if r["mode"]=="TERMINAL":return {"retrospective":retro(r),"prospective":None}
                            if self.resumed:
                                if not r["context"]["prior_generation_and_live_ancestry"]:
                                    raise AssertionError("actual live ancestry absent")
                                n=len(self.calls)
                                if n==1:
                                    return rows(r,[("nadia",course(),0),("father",policy([action("REST")]),0),
                                                   ("nadia",course(),0)])
                                if n==2:
                                    # Actual previously constituted adult, not
                                    # a new wage-labor personality. Three exact
                                    # independently selected material courses.
                                    work=action("WORK",{"project_id":work_proj})
                                    routine={"offer":"historically_possible_recurrent_routines",
                                        "construct":"RECURRENT_ROUTINE",
                                        "match":{"basis":{"actor":"father","operation":"WORK","project_ref":work_proj}},
                                        "augment":{"window_days":60,"hours_per_active_day":2.,
                                                   "provisional_exposure_fraction":.5}}
                                    return rows(r,[("father",policy([work]),0),
                                        ("father",policy([action("REST")]),0),("father",policy([work]),0),
                                        ("father",policy([action("REST")]),0),("father",policy([work],[routine]),0)])
                                if n==3:
                                    def revise(mode):
                                        return {"offer":"historically_possible_routine_revisions","construct":"ROUTINE_REVISION",
                                            "match":{"basis":{"actor":"father","operation":"WORK","project_ref":work_proj}},
                                            "augment":{"mode":mode,"interpretive_hypothesis":"Change my own continued work."}}
                                    # Source comes from ACTUAL previous admitted
                                    # routine, not an authored period catalog.
                                    return rows(r,[("nadia",course(),10),
                                        ("father",policy([action("REST")],[revise("PAUSE")]),0),
                                        ("nadia",course(),5),
                                        ("father",policy([action("REST")],[revise("RESUME")]),0),
                                        ("nadia",course(),5)])
                                def move(site):
                                    return policy([action("MOVE",{"grounds_status":"HISTORICALLY_FAMILIAR_DESTINATION",
                                        "world_request":{"material_object_ref":site}})])
                                def shared(nominate_routine=False,refuse=False):
                                    out={}
                                    for a,peer in (("father","mother"),("mother","father")):
                                        rule={"offer":"historically_possible_recurrent_routines",
                                            "construct":"RECURRENT_ROUTINE",
                                            "match":{"basis":{"actor":a,"operation":"SING","project_ref":shared_projects[a],
                                                              "coactivity_partner":peer}},
                                            "augment":{"window_days":45,"hours_per_active_day":2.,
                                                       "provisional_exposure_fraction":.5}}
                                        out[a]=policy([action("REFUSE")] if refuse and a=="mother" else
                                              [action("SING",{"project_id":shared_projects[a]})],
                                              [rule] if nominate_routine else [])
                                    return out
                                if n==4:
                                    return rows(r,[("father",policy([action("REST")]),0),
                                        ("father",move("home"),0),("nadia",move("home"),0),
                                        ("father",shared(refuse=True),0),("father",policy([action("REST")]),0)])
                                if n==5:
                                    return rows(r,[("mother",policy([action("REST")]),0),("father",shared(),0),
                                        ("father",policy([action("REST")]),0),
                                        ("mother",policy([action("REST")]),0),("father",shared(),0)])
                                if n==6:
                                    return rows(r,[("father",policy([action("REST")]),0),("mother",policy([action("REST")]),0),
                                        ("father",shared(nominate_routine=True),0)])
                                if n==7:
                                    return rows(r,[("nadia",course(),4),
                                        ("father",policy([action("REST")]),0),
                                        ("father",move("workshop"),0),("nadia",move("workshop"),0),
                                        ("nadia",course(),4)])
                                raise AssertionError("unexpected resumed call")
                            n=len(self.calls)
                            if n==1:
                                first=[affect("WITHHOLD"),memory] if nominate else [memory,affect("WITHHOLD")]
                                return rows(r,[("nadia",policy([sing()],first),0),
                                               ("nadia",policy([action("REST")]),0),
                                               ("nadia",policy([sing()],[affect("APPROACH")]),0)])
                            if n==2:
                                p=policy([action("WAIT")],[{"private_construct":"NOTICE_END",
                                    "augment":{"possible_object":obj,"means":["REST"]}}])
                                if nominate:
                                    m=r["context"]["actor_contexts"]["nadia"]["accessible_memories"][0]
                                    p["private_rehearsal"]={"affect":"REQUIRED","memory_ref":m["id"],
                                        "affect_ref":m["ordinary_affect_memory"]["affect_ref"],"meaning":rehearsal}
                                return rows(r,[("nadia",policy([action("WAIT")]),0),
                                               ("nadia",policy([action("REST")]),2),("nadia",p,0)])
                            if n==3:
                                ends=[e for e in r["context"]["actor_contexts"]["nadia"]["possible_ends"]
                                      if e.get("genesis_family")=="ACTUAL_PRIVATE_REHEARSAL"]
                                rules=([{"action":"REST","pool":"possible_end_trials","option_match":{
                                    "possible_end_ref":ends[0]["id"]}}] if ends else [])+[action("WAIT")]
                                takeup={"private_construct":"TAKE_UP_END","match":{"possible_object":obj},
                                        "augment":{"means":["REST"]}}
                                return rows(r,[("nadia",policy(rules),0),
                                    ("nadia",policy([action("REST")],[takeup]),0),("nadia",course(),0)])
                            raise AssertionError("unexpected historical call")
                    class LiveCourse:
                        def __init__(self):self.calls=[]
                        def call(self,r):
                            self.calls.append(r)
                            aid=r["principal"]
                            return {"policies":{aid:course() if aid=="nadia" else policy([action("REST"),action("WAIT")])}}
                    h=History();live=LiveCourse()
                    def op(runtime,hist):return ContinuingLife(runtime,root/"operator","nadia",
                        historical_provider=hist,live_provider=live,sourcefree_attested=True,mii_module=mii)
                    s=op(rt,h)
                    try:
                        prefix=rt.ledger.events()
                        s.historical_checkpoint()
                        child=rt.ledger.actor("nadia")[1]
                        self.assertEqual(len(child["memories"]),int(nominate))
                        aff=[a for e in child["expectations"] for a in e.get("affective_organizations",[])
                             if a["basis"]["location"]=="workshop"]
                        self.assertEqual({a["course_orientation"] for a in aff},{"APPROACH","WITHHOLD"})
                        if nominate:self.assertEqual(child["memories"][0]["ordinary_affect_memory"]["affect_ref"],
                            next(a["id"] for a in aff if a["course_orientation"]=="WITHHOLD"))
                        s.historical_checkpoint()
                        child=rt.ledger.actor("nadia")[1]
                        self.assertEqual(len(child["projects"]),1)
                        self.assertEqual(len([e for e in child["possible_ends"] if
                            e.get("genesis_family")=="ACTUAL_PRIVATE_REHEARSAL"]),int(nominate))
                    finally:s.close()
                    # Cold history continuation, not a regenerated child.
                    cold=ConstitutiveRuntime(str(db));s=op(cold,h)
                    try:
                        s.historical_checkpoint()
                        child=cold.ledger.actor("nadia")[1]
                        self.assertEqual(len(child["projects"]),1+int(nominate))
                        if nominate:
                            p=child["projects"][1]
                            self.assertEqual(p["takeup_evidence"]["private_takeup_basis"]["ordinary_affect_memory"],
                                             child["memories"][0]["ordinary_affect_memory"])
                            self.assertEqual(p["operational_history"][-1]["operation"],"REST")
                        else:self.assertEqual(child["projects"][0]["operational_history"][-1]["operation"],"SING")
                        s.finish_history()
                        self.assertEqual(cold.ledger.events()[:len(prefix)],prefix)
                        pre_live=cold.ledger.events()
                        s.configure_encounter("visitor",{"grade":"SOURCEFREE_TEST_ONLY",
                            "user_conditions":{"workshop":{"light":"lit","sightline":"unobstructed",
                                "hearing":True,"sound_path":"audible","legibility":"readable"}},
                            "actor_conditions":{a:{"facing":"entrance","visual":True,"light":"lit",
                                "sightline":"unobstructed","hearing":True,"sound_path":"audible"}
                                for a in ("father","mother","nadia")}},request_id="geometry")
                        self.assertEqual(s.contribute("visitor","enter","MOVE",destination="workshop")["status"],"PERFORMED")
                        self.assertEqual(s.contribute("visitor","say","SAY",text="There is room to be here.",
                                                      target_actor_ref="nadia")["status"],"PERFORMED")
                        w=cold.ledger.world()[1];ref=w["neighbor_user_events"][-1]["event_ref"];target=w["clock"]+4
                        with self.assertRaisesRegex(RecursionRefusal,"LIFE_VISITOR_STILL_PRESENT"):s.resume_history()
                        self.assertEqual(s.present_until("visitor",ref,target,max_beats=1)["beats_committed_this_call"],1)
                    finally:s.close();cold.close()
                    cold=ConstitutiveRuntime(str(db));s=op(cold,h)
                    try:
                        s.present_until("visitor",ref,target)
                        calls=len(live.calls);self.assertEqual(calls,4)
                        self.assertEqual(s.present_until("visitor",ref,target)["new_present_surfaces"],[])
                        self.assertEqual(len(live.calls),calls)
                        self.assertIn("nadia",{q["principal"] for q in live.calls})
                        view=canonical(s.private_surface("visitor"))
                        self.assertNotIn(secret,view);self.assertNotIn(rehearsal,view)
                        self.assertNotIn(secret,canonical(cold.ledger.world()[1]))
                        self.assertEqual(s.contribute("visitor","leave","LEAVE")["status"],"PERFORMED")
                        actual=cold.ledger.events();self.assertEqual(actual[:len(pre_live)],pre_live)
                    finally:s.close();cold.close()
                    h2=History(resumed=True);cold=ConstitutiveRuntime(str(db));s=op(cold,h2)
                    try:
                        s.resume_history()
                        self.assertEqual(s.status()["epoch"],1)
                        self.assertEqual(cold.ledger.events()[:len(actual)],actual)
                        result=cold.ledger.actor("nadia")[1]
                        p=result["projects"][-1]
                        self.assertEqual(p["operational_history"][-1]["operation"],"REST" if nominate else "SING")
                        s.historical_checkpoint()
                        before_period=deepcopy(cold.ledger.world()[1])
                        father=deepcopy(cold.ledger.actor("father")[1])
                        child_before=deepcopy(cold.ledger.actor("nadia")[1])
                        sources=[q for q in before_period["routine_source_registry"].values()
                                 if q["actor"]=="father" and q.get("operation")=="WORK"]
                        self.assertEqual(len(sources),1)
                        src=sources[0];self.assertEqual(len(set(src["basis_event_refs"])),3)
                        self.assertEqual(src["evidence_class"],"SOURCEFREE_ACTOR_LIVED_ROUTINE_PROPOSAL")
                        s.historical_checkpoint()
                        after=cold.ledger.world()[1]
                        periods=[q for q in after["historical_periods"] if q["start"]>=before_period["clock"]]
                        active=[q for q in periods if any(x["source_ref"]==src["id"] for x in q["processes"])]
                        held=[q for q in periods if any(x["source_ref"]==src["id"] and
                              x["reason"]=="ACTOR_ROUTINE_PAUSED" for x in q.get("situationally_withheld_processes",[]))]
                        self.assertEqual(sum(q["end"]-q["start"] for q in active),15)
                        self.assertEqual(sum(q["end"]-q["start"] for q in held),5)
                        self.assertEqual(sum(q["modeled_labor_hours"] for q in after["wage_labor_periods"]
                                             if q["source_ref"]==src["id"]),15.)
                        self.assertEqual([x["mode"] for x in after["routine_source_registry"][src["id"]]["revisions"]],
                                         ["PAUSE","RESUME"])
                        self.assertEqual(cold.ledger.actor("father")[1]["memories"],father["memories"])
                        result=cold.ledger.actor("nadia")[1];p=result["projects"][-1]
                        self.assertEqual(result["memories"],child_before["memories"])
                        self.assertEqual(p["operational_history"][-1]["operation"],"REST" if nominate else "SING")
                        self.assertEqual(cold.ledger.events()[:len(actual)],actual)
                        # R82: the same actual family can return to personally
                        # experienced sites, form independent reciprocal routines,
                        # and carry both private and material history across departure.
                        s.historical_checkpoint()
                        w=cold.ledger.world()[1]
                        self.assertEqual(w["positions"]["father"],"home")
                        self.assertEqual(w["positions"]["nadia"],"home")
                        s.historical_checkpoint()
                        s.historical_checkpoint()
                        w=cold.ledger.world()[1]
                        pair=[q for q in w["routine_source_registry"].values()
                              if q.get("operation")=="SING"]
                        self.assertEqual({q["actor"] for q in pair},{"father","mother"})
                        self.assertEqual(len(pair),2)
                        self.assertEqual(pair[0]["basis_event_refs"],pair[1]["basis_event_refs"])
                        self.assertEqual(len(set(pair[0]["basis_event_refs"])),3)
                        before_pair=deepcopy(w);before_pair_events=cold.ledger.events()
                    finally:s.close();cold.close()
                    cold=ConstitutiveRuntime(str(db));s=op(cold,h2)
                    try:
                        s.historical_checkpoint()
                        w=cold.ledger.world()[1]
                        self.assertEqual(w["positions"]["father"],"workshop")
                        self.assertEqual(w["positions"]["nadia"],"workshop")
                        pair_refs={q["id"] for q in pair}
                        periods=[q for q in w["historical_periods"] if q["start"]>=before_pair["clock"]]
                        self.assertEqual(sum(q["end"]-q["start"] for q in periods
                            if pair_refs.issubset({v["source_ref"] for v in q["processes"]})),4)
                        self.assertEqual(sum(q["end"]-q["start"] for q in periods
                            if any(v["source_ref"]==src["id"] for v in q["processes"])),4)
                        self.assertTrue(all(not (pair_refs & {v["source_ref"] for v in q["processes"]}
                            and any(v["source_ref"]==src["id"] for v in q["processes"])) for q in periods))
                        self.assertEqual(cold.ledger.events()[:len(before_pair_events)],before_pair_events)
                        result=cold.ledger.actor("nadia")[1];p=result["projects"][-1]
                        self.assertEqual(result["memories"],child_before["memories"])
                        self.assertEqual(p["operational_history"][-1]["operation"],"REST" if nominate else "SING")
                        s.finish_history()
                        self.assertTrue(cold.verify()["valid"])
                        self.assertTrue(all(x["status"]=="RETURNED" for x in s.receipts()))
                        self.assertFalse(s.status()["held"])
                        print("R79_JOINED_CHILD",json.dumps({"nominate":nominate,"age_days":result["age_days"],
                            "projects":len(result["projects"]),"historical_calls":len(h.calls)+len(h2.calls),
                            "live_calls":calls,"native_events":len(cold.ledger.events()),
                            "actual_later_course":p["operational_history"][-1]["operation"],
                            "modeled_wage_hours":19,"paused_days":5,"actual_work_anchor_events":3,
                            "same_family_reciprocal_days":4,"actual_reciprocal_anchor_events":3},sort_keys=True))
                        return result
                    finally:s.close();cold.close()
                result=mod.EarlyOrdinaryPractice().productive_ordinary_arm(db,True,transfer=True,affect=True,
                    private=nominate,antecedent=True,continuation=continue_actual,reciprocal_antecedent=True)
                self.assertEqual(len(result["projects"]),1+int(nominate))


    def test_R82_familiar_destination_is_actor_local_not_world_permission(self):
        from modern_generation_port_r28 import ConditionalPolicy
        from um_sorok_organism.semantics import ValidatingSemanticService
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/"life.sqlite"))
            try:
                # Authored starting placement, not a claim of enduring
                # institutional admission. The actor actually lives there.
                rt.ledger.initialize(blank_world(),[adult("a","A",location="hall"),adult("b","B")])
                self.assertEqual(rt.step("a",requested_action="REST")["status"],"PERFORMED")
                self.assertEqual(rt.step("a",requested_action="MOVE",object_ref="home")["objective_outcome"],"MOVED")
                rt.step("b",requested_action="REST")
                def destinations(a):
                    return [o for q in rt.situated(a)["candidate_actions"]
                            for o in q.get("practical_alternatives",[])
                            if o.get("grounds_status")=="HISTORICALLY_FAMILIAR_DESTINATION"]
                opts=destinations("a");self.assertEqual(len(opts),1)
                self.assertEqual(opts[0]["world_request"]["material_object_ref"],"hall")
                self.assertEqual(destinations("b"),[])
                self.assertNotIn("workshop",[v["world_request"]["material_object_ref"] for v in opts])
                # An action label by itself cannot silently pick a destination.
                rt.semantic=ValidatingSemanticService(ConditionalPolicy({"a":policy([action("MOVE")])}))
                self.assertIsNone(rt.plan("a").object_ref)
                pol=policy([action("MOVE",{"grounds_status":"HISTORICALLY_FAMILIAR_DESTINATION",
                                           "world_request":{"material_object_ref":"hall"}})])
                rt.semantic=ValidatingSemanticService(ConditionalPolicy({"a":pol}))
                out=rt.step("a")
                self.assertEqual(out["attempt"],"MOVE")
                self.assertEqual(out["objective_outcome"],"INSTITUTIONAL_ACCESS_DENIED")
                self.assertEqual(rt.ledger.actor("a")[1]["location"],"home")
                path=rt.ledger.actor("a")[1]["evidence_paths"][-1]
                witness=path["pre_world_operative_policy_witness_analytic_only"]["familiar_destination_choice"]
                self.assertEqual(witness["source"],opts[0]["familiar_destination_basis"])
                self.assertTrue(rt.verify()["valid"])
            finally:rt.close()


    def test_R81_independent_reciprocal_routine_through_actual_checkpoint_interval_and_revision(self):
        """Same shared semantic compiler and owner; no injected future assent."""
        from copy import deepcopy
        from um_sorok_organism.mediated_efficacy import situated_component_efficacy
        for both in (True,False):
            with self.subTest(both=both),tempfile.TemporaryDirectory() as d:
                root=Path(d);db=root/"life.sqlite";rt=ConstitutiveRuntime(str(db))
                aa=adult("a","A");bb=adult("b","B")
                for actor,peer in ((aa,"b"),(bb,"a")):
                    actor["projects"]=[{"id":actor["id"]+"-song","object":"a particular shared practice",
                        "means":["SING"],"addressed_party_ref":peer,"status":"active","priority":.7}]
                rt.ledger.initialize(blank_world(),[aa,bb])
                def own(a,op,rules=()):
                    return {a:policy([action(op)],rules)}
                def shared(nominate=False,refuse=False):
                    out={}
                    for a,peer in (("a","b"),("b","a")):
                        f=[]
                        if nominate and (a=="a" or both):
                            f=[{"offer":"historically_possible_recurrent_routines","construct":"RECURRENT_ROUTINE",
                                "match":{"basis":{"actor":a,"operation":"SING","project_ref":a+"-song",
                                                  "coactivity_partner":peer}},
                                "augment":{"window_days":80,"hours_per_active_day":3. if a=="a" else 2.,
                                           "provisional_exposure_fraction":1. if a=="a" else .5}}]
                        out[a]=policy([action("REFUSE")] if refuse and a=="b" else
                                      [action("SING",{"project_id":a+"-song"})],f)
                    return out
                def revise(mode):
                    return [{"offer":"historically_possible_routine_revisions","construct":"ROUTINE_REVISION",
                        "match":{"basis":{"actor":"b","operation":"SING","project_ref":"b-song"}},
                        "augment":{"mode":mode,"interpretive_hypothesis":"Change my own involvement."}}]
                class H:
                    def __init__(self):self.calls=[]
                    def call(self,r):
                        self.calls.append(r)
                        if r["mode"]=="TERMINAL":return {"retrospective":retro(r),"prospective":None}
                        n=len(self.calls);ctx=r["context"];t=ctx["clock"];out=[]
                        if n==1:
                            plan=[("a",shared(refuse=True),0),("a",own("a","REST"),0),
                                  ("b",own("b","REST"),0),("a",shared(),0)]
                        elif n==2:
                            plan=[("a",own("a","REST"),0),("b",own("b","REST"),0),
                                  ("a",shared(),0),("a",own("a","REST"),0),
                                  ("b",own("b","REST"),0)]
                        elif n==3:
                            plan=[("a",shared(nominate=True),0),("a",own("a","REST"),0),
                                  ("b",own("b","REST"),0)]
                        elif n==4:
                            plan=[("a",own("a","REST"),10),("b",own("b","REST",revise("PAUSE") if both else []),0),
                                  ("a",own("a","REST"),5),("b",own("b","REST",revise("RESUME") if both else []),0),
                                  ("a",own("a","REST"),5)]
                        else:raise AssertionError("unexpected checkpoint")
                        for i,(a,pol,span) in enumerate(plan):
                            t+=span+1
                            out.append(event(ctx,"r81:"+str(n)+":"+str(i),t,a,pol,span=span))
                        return {"retrospective":retro(r),"prospective":out}
                h=H();live=Live()
                def open_session(runtime):return ContinuingLife(runtime,root/"operator","a",
                    historical_provider=h,live_provider=live,sourcefree_attested=True)
                s=open_session(rt)
                try:
                    for _ in range(3):s.historical_checkpoint()
                    w=rt.ledger.world()[1];sources=w["routine_source_registry"]
                    self.assertEqual(len(sources),2 if both else 1)
                    self.assertTrue(all(len(set(x["basis_event_refs"]))==3 for x in sources.values()))
                    if both:
                        a,b=sorted(sources.values(),key=lambda q:q["actor"])
                        self.assertEqual(a["basis_event_refs"],b["basis_event_refs"])
                    prefix=rt.ledger.events();before=deepcopy(rt.ledger.actors());clock=w["clock"]
                    f0={a:situated_component_efficacy(before[a],"SING","home")[
                        "technical_component_facility_estimate"] for a in before}
                finally:s.close();rt.close()
                rt=ConstitutiveRuntime(str(db));s=open_session(rt)
                try:
                    s.historical_checkpoint()
                    w=rt.ledger.world()[1];periods=[q for q in w["historical_periods"] if q["start"]>=clock]
                    active=[q for q in periods if q["processes"]]
                    self.assertEqual(sum(q["end"]-q["start"] for q in active),15 if both else 0)
                    self.assertTrue(all(len(q["processes"])==2 and q["actor_time_claims"]=={"a":1.,"b":1.}
                                        and len({p["reciprocal_routine_pair_ref"] for p in q["processes"]})==1
                                        for q in active))
                    held=[q for q in periods if not q["processes"]]
                    self.assertEqual(sum(q["end"]-q["start"] for q in held),5 if both else 20)
                    if both:
                        self.assertTrue(any(p["reason"]=="ACTOR_ROUTINE_PAUSED"
                            for q in held for p in q.get("situationally_withheld_processes",[])))
                    self.assertTrue(any(p["reason"]=="NO_UNAMBIGUOUS_INDEPENDENT_RECIPROCAL_ROUTINE"
                        for q in held for p in q.get("situationally_withheld_processes",[])))
                    for a in before:
                        q=rt.ledger.actor(a)[1]
                        self.assertEqual(q["memories"],before[a]["memories"])
                        self.assertEqual(q["power_exercises"],before[a]["power_exercises"])
                        f1=situated_component_efficacy(q,"SING","home")["technical_component_facility_estimate"]
                        self.assertEqual(f1>f0[a],both)
                    self.assertEqual(rt.ledger.events()[:len(prefix)],prefix)
                    s.finish_history()
                    self.assertTrue(rt.verify()["valid"])
                    self.assertTrue(all(q["status"]=="RETURNED" for q in s.receipts()))
                    self.assertFalse(live.requests)
                    print("R81_RECIPROCAL_CHECKPOINT",json.dumps({"both":both,
                        "active_days":15 if both else 0,"withheld_days":5 if both else 20,
                        "actual_anchor_events":3,"historical_calls":len(h.calls)},sort_keys=True))
                finally:s.close();rt.close()

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



    def test_heterogeneous_exact_allocation_actual_life_and_conserved_budget(self):
        from importlib.util import spec_from_file_location,module_from_spec
        from unittest.mock import patch
        import sys
        folder=Path(__file__).parent/"um_sorok_organism"
        def module(name,path):
            spec=spec_from_file_location(name,path)
            mod=module_from_spec(spec);spec.loader.exec_module(mod);return mod
        wire=module("um_sorok_organism.r59_wire",folder/"live_psychological_llm.py")
        with patch.dict(sys.modules,{"um_sorok_organism.live_psychological_llm":wire}):
            lab=module("um_sorok_organism.r59_lab",folder/"inference_lab.py")
            with tempfile.TemporaryDirectory() as d:
                root=Path(d);head="604f3d1a51a21c53523a2040b30e234b556785fa"
                capture=lab.WorkloadCapture(source_head=head,fixture="whole-life-r59",
                    sourcefree_fixture_attested=True)
                def setup(where,hp,lp):
                    where.mkdir()
                    rt,sid,catalog,_=joined.JoinedGenerationCourt.setup(self,where/"life.sqlite")
                    return rt,sid,catalog
                def run(rt,where,sid,catalog,hp,lp):
                    s=ContinuingLife(rt,where/"operator","mother",historical_provider=hp,
                        live_provider=lp,sourcefree_attested=True,period_catalog=catalog,
                        family_sources=(sid,),mii_module=mii)
                    try:
                        for _ in range(3):s.historical_checkpoint()
                        s.finish_history();s.independent_absent_beat();s.resume_history()
                        s.finish_history()
                        return rt.ledger.events()
                    finally:s.close()
                class History:
                    def __init__(self,sid):
                        self.a=joined.LifeCheckpoint(sid);self.b=joined.LifeCheckpoint(sid,resumed=True)
                    def call(self,req):
                        return (self.a if len(self.a.requests)<4 else self.b).call(req)
                one=root/"reference";rt,sid,catalog=setup(one,None,None)
                try:
                    baseline=run(rt,one,sid,catalog,lab.CombinedCaptureProvider(History(sid),capture,"HISTORICAL"),
                        lab.CombinedCaptureProvider(Live(),capture,"LIVE"))
                finally:rt.close()
                tape=capture.document();rows=lab.verify_workload(tape,source_head=head)["rows"]
                self.assertEqual([x["task"] for x in rows],
                    [lab.CHECKPOINT_TASK]*4+[lab.LIVE_TURN_TASK]+[lab.CHECKPOINT_TASK]*2)
                # Exact matched request qualification, deliberately hermetic;
                # equal fixture answers do NOT qualify any actual model.
                live_row=rows[4]; endpoint="https://example.invalid/chat/completions"
                def profile(model,a,b,c,e):
                    return dict(model=model,endpoint=endpoint,input_token_ceiling=a,
                        completion_token_limit=b,input_nanos_per_token=c,output_nanos_per_token=e)
                b=lab.LiveBudget(journal=root/"budget",max_calls=7,max_wire_bytes=10000000,
                    input_token_ceiling=100000,completion_token_limit=1000,input_nanos_per_token=5,
                    output_nanos_per_token=10,max_budget_nanos=4000000,sourcefree_live_authorized=True,
                    profiles={"reference":profile("reference-model",100000,1000,5,10),
                              "economy":profile("economy-model",80000,500,1,3)})
                def opts(model,mode):
                    return dict(endpoint=endpoint,model=model,api_key="not-a-key",
                        allow_private_actor_data=True,**({"sourcefree_checkpoint_attested":True}
                            if mode=="HISTORICAL" else {"sourcefree_live_attested":True}))
                qualification=dict(owner_head=head,mode="LIVE",request_digest=live_row["packet_digest"],
                    reference_profile="reference",candidate_profile="economy",
                    qualification_digest=lab.digest({"scope":"HERMETIC_ONLY","workload":tape["sha256"]}))
                def router(mode,qualifications=()):
                    return lab.CombinedAllocationProvider(mode,owner_head=head,budget=b,
                        reference_profile="reference",provider_options={p:opts(p+"-model",mode)
                            for p in ("reference","economy")},qualifications=qualifications,
                        sourcefree_allocation_authorized=True)
                hp=router("HISTORICAL");unqualified=router("LIVE")
                qualification.update(reference_identity=unqualified.profile_identity("reference"),
                    candidate_identity=unqualified.profile_identity("economy"))
                lp=router("LIVE",[qualification])
                two=root/"allocation";rt,sid,catalog=setup(two,None,None)
                history=History(sid);live=Live();seen=[]
                def hermetic(provider,payload):
                    doc=json.loads(payload["messages"][1]["content"])
                    seen.append((payload["model"],payload["max_completion_tokens"]))
                    proposal=history.call(doc) if "mode" in doc else live.call(doc)
                    return {"choices":[{"message":{"content":json.dumps(proposal)}}],
                            "usage":{"prompt_tokens":200,"completion_tokens":50,"total_tokens":250}}
                try:
                    with patch.object(wire.ExplicitJSONLLMProvider,"_request",hermetic):
                        actual=run(rt,two,sid,catalog,hp,lp)
                    self.assertEqual(actual,baseline)
                    self.assertEqual(seen,[("reference-model",1000)]*4+[("economy-model",500)]
                        +[("reference-model",1000)]*2)
                    self.assertEqual(b.calls,7)
                    self.assertEqual(b.reserved,6*510000+81500)
                    self.assertEqual(b.estimated_reported,6*1500+350)
                    self.assertEqual(lp.usage_snapshot()["receipts"][-1]["allocation_basis"],
                        "EXACT_REVIEWED_REQUEST")
                    self.assertEqual(hp.usage_snapshot()["receipts"][-1]["allocation_basis"],
                        "REFERENCE_UNMATCHED")
                    import sqlite3
                    with sqlite3.connect(two/"operator"/"live.sqlite") as cx:
                        records=[json.loads(x[0]) for x in cx.execute("SELECT receipt FROM turns ORDER BY rowid")]
                    self.assertEqual(records[-1]["transport_receipt"]["budget_profile"],"economy")
                    self.assertEqual(records[-1]["transport_receipt"]["allocation_qualification_digest"],
                        qualification["qualification_digest"])
                    self.assertEqual(len(b.log.read_text().splitlines()),14)
                    historical=[]
                    for epoch in ("epoch-000000","epoch-000001"):
                        with sqlite3.connect(two/"operator"/epoch/"ops.sqlite") as cx:
                            historical.extend(json.loads(x[0]) for x in cx.execute(
                                "SELECT receipt FROM checkpoint_attempts ORDER BY id"))
                    report=lab.reconcile_budget_owner_receipts(b,historical_receipts=historical,
                        live_receipts=records)
                    self.assertEqual(report["profiles"]["reference"]["owner_operations_returned"],6)
                    self.assertEqual(report["profiles"]["economy"]["owner_operations_returned"],1)
                    self.assertEqual(report["profiles"]["economy"]["known_rate_estimate_nanos"],350)
                    self.assertEqual(report["profiles"]["reference"]["known_rate_estimate_nanos"],9000)
                    self.assertEqual(report["profiles"]["reference"]["unlinked"],0)
                    self.assertEqual(report["profiles"]["economy"]["unlinked"],0)
                    self.assertEqual(lab.reconcile_budget_owner_receipts(b)["profiles"]["economy"]["unlinked"],1)
                    with self.assertRaisesRegex(ValueError,"OWNER_LINK"):
                        lab.reconcile_budget_owner_receipts(b,live_receipts=records+records)
                    print("R59_R60_ALLOCATION",json.dumps(report["profiles"],sort_keys=True))
                    # One mutation of the actual request loses qualification.
                    changed=lab.copy(live_row["packet"]);changed["source"]="unmatched-source"
                    with patch.object(wire.ExplicitJSONLLMProvider,"_request",hermetic):
                        with self.assertRaises(lab.BudgetStop):lp.call(changed)
                    self.assertEqual(len(seen),7)
                    self.assertEqual(lp.usage_snapshot()["receipts"][-1]["allocation_profile"],"reference")
                    self.assertEqual(lp.usage_snapshot()["receipts"][-1]["attempts"],0)
                finally:rt.close()
                bad=dict(qualification,owner_head="0"*40)
                with self.assertRaisesRegex(ValueError,"QUALIFICATION_INVALID"):router("LIVE",[bad])
                bad=dict(qualification,candidate_identity="0"*64)
                with self.assertRaisesRegex(ValueError,"QUALIFICATION_INVALID"):router("LIVE",[bad])



    def test_reviewed_demand_envelope_on_varying_actual_owner_courses(self):
        from importlib.util import spec_from_file_location,module_from_spec
        from unittest.mock import patch
        import sys
        folder=Path(__file__).parent/"um_sorok_organism"
        def module(name,path):
            spec=spec_from_file_location(name,path)
            mod=module_from_spec(spec);spec.loader.exec_module(mod);return mod
        wire=module("um_sorok_organism.r61_wire",folder/"live_psychological_llm.py")
        with patch.dict(sys.modules,{"um_sorok_organism.live_psychological_llm":wire}):
            lab=module("um_sorok_organism.r61_lab",folder/"inference_lab.py")
            with tempfile.TemporaryDirectory() as d:
                root=Path(d);head="604f3d1a51a21c53523a2040b30e234b556785fa"
                endpoint="https://example.invalid/chat/completions"
                def profile(name,rate):
                    return dict(model=name,endpoint=endpoint,input_token_ceiling=100000,
                        completion_token_limit=1000,input_nanos_per_token=rate,output_nanos_per_token=rate)
                def budget(label):
                    return lab.LiveBudget(journal=root/label,max_calls=20,max_wire_bytes=20000000,
                        input_token_ceiling=100000,completion_token_limit=1000,input_nanos_per_token=5,
                        output_nanos_per_token=5,max_budget_nanos=10000000,sourcefree_live_authorized=True,
                        profiles={"reference":profile("reference",5),"economy":profile("economy",1)})
                def opts(name,mode):
                    return dict(model=name,endpoint=endpoint,api_key="not-a-key",allow_private_actor_data=True,
                        **({"sourcefree_checkpoint_attested":True} if mode=="HISTORICAL"
                        else {"sourcefree_live_attested":True}))
                def router(mode,b,env=None,dispatch=False,reference="reference"):
                    return lab.CombinedAllocationProvider(mode,owner_head=head,budget=b,
                        reference_profile=reference,provider_options={n:opts(n,mode)
                        for n in ("reference","economy")},sourcefree_allocation_authorized=True,
                        demand_envelope=env,sourcefree_envelope_dispatch=dispatch)
                def setup(label,n):
                    path=root/label;path.mkdir()
                    rt,sid,catalog,_=joined.JoinedGenerationCourt.setup(self,path/"life.sqlite",
                        extra_projects={"father":[{"object":"ordinary "+("x"*n),
                                                  "means":["REST"],"priority":.1}]})
                    return path,rt,sid,catalog
                class History:
                    def __init__(self,sid):
                        self.a=joined.LifeCheckpoint(sid);self.b=joined.LifeCheckpoint(sid,resumed=True)
                    def call(self,r):
                        return (self.a if len(self.a.requests)<4 else self.b).call(r)
                def execute(path,rt,sid,catalog,hp,lp,full=False):
                    s=ContinuingLife(rt,path/"operator","mother",historical_provider=hp,live_provider=lp,
                        sourcefree_attested=True,period_catalog=catalog,family_sources=(sid,),mii_module=mii)
                    try:
                        s.historical_checkpoint()
                        if full:
                            s.historical_checkpoint();s.historical_checkpoint();s.finish_history()
                            s.independent_absent_beat();s.resume_history();s.finish_history()
                        self.assertTrue(rt.verify()["valid"])
                        return rt.ledger.events()
                    finally:s.close();rt.close()
                def capture_course(label,n):
                    path,rt,sid,catalog=setup(label,n)
                    c=lab.WorkloadCapture(source_head=head,fixture=label,sourcefree_fixture_attested=True)
                    baseline=execute(path,rt,sid,catalog,
                        lab.CombinedCaptureProvider(History(sid),c,"HISTORICAL"),
                        lab.CombinedCaptureProvider(Live(),c,"LIVE"))
                    return c.document(owner_state_sha256=lab.digest(baseline)),baseline
                b=budget("calibration-budget");identity=router("HISTORICAL",b)
                ids={n:identity.profile_identity(n) for n in ("reference","economy")}
                courses=[]
                for label,n,partition in (("fit-small",1,"FIT"),("fit-large",90,"FIT"),("heldout",35,"HOLDOUT")):
                    tape,baseline=capture_course(label,n)
                    # Both declared mock profiles traverse the actual same owner.
                    # Review is explicitly hermetic, not an external adequacy judgment.
                    owner_results={}
                    for arm in ("reference","economy"):
                        path,rt,sid,catalog=setup(label+"-"+arm,n)
                        provider=router("HISTORICAL",b,reference=arm)
                        history=History(sid)
                        def answer(self,payload):
                            req=json.loads(payload["messages"][1]["content"])
                            return {"choices":[{"message":{"content":json.dumps(history.call(req))}}],
                                    "usage":{"prompt_tokens":200,"completion_tokens":50}}
                        with patch.object(wire.ExplicitJSONLLMProvider,"_request",answer):
                            outcome=execute(path,rt,sid,catalog,provider,Live())
                        self.assertEqual(outcome,baseline)
                        import sqlite3
                        with sqlite3.connect(path/"operator"/"epoch-000000"/"ops.sqlite") as cx:
                            rec=json.loads(cx.execute("SELECT receipt FROM checkpoint_attempts").fetchone()[0])
                        self.assertEqual(rec["cycle_disposition"],"CYCLE_RETURNED")
                        owner_results[arm]={"receipt":rec,"native_digest":lab.digest(outcome)}
                    row=tape["payload"]["rows"][0]
                    review=lab.paired_owner_review(tape,0,mode="HISTORICAL",budget=b,
                        reference_receipt=owner_results["reference"]["receipt"],
                        candidate_receipt=owner_results["economy"]["receipt"],
                        reference_identity=ids["reference"],candidate_identity=ids["economy"],
                        quality_verdict="ADEQUATE",
                        quality_evidence_digest=lab.digest({"fixture_only":True,"arms":owner_results}))
                    self.assertEqual(review["reference_cost_nanos"],1250)
                    self.assertEqual(review["candidate_cost_nanos"],250)
                    self.assertEqual(review["request_digest"],row["packet_digest"])
                    courses.append({"workload":tape,"partition":partition,"reviews":[review]})
                def envelope(c):
                    return lab.CombinedDemandEnvelope(mode="HISTORICAL",owner_head=head,
                        reference_profile="reference",candidate_profile="economy",
                        reference_identity=ids["reference"],candidate_identity=ids["economy"],
                        courses=c,sourcefree_review_attested=True)
                e=envelope(courses);print("R61_ENVELOPE",json.dumps(e.summary(),sort_keys=True))
                self.assertGreater(e.summary()["qualified_shapes"],0)
                unseen,baseline=capture_course("novel",55)
                packet=unseen["payload"]["rows"][0]["packet"]
                self.assertEqual(e.assess(packet),"NOVEL_WITHIN_REVIEWED_ENVELOPE")
                novel=lab.copy(packet);novel["context"]["new_qualified_owner_field"]=[]
                self.assertEqual(e.assess(novel),"NO_QUALIFIED_SHAPE")
                adverse=lab.copy(courses);adverse[-1]["reviews"][0]["quality_verdict"]="INADEQUATE"
                self.assertEqual(envelope(adverse).summary()["qualified_shapes"],0)
                partial=lab.copy(courses);partial[-1]["reviews"]=[]
                with self.assertRaisesRegex(ValueError,"INCOMPLETE_REVIEW"):envelope(partial)
                # Actual fourth course, not in the fit or holdout. Shadow is
                # safe default; explicit sourcefree trial actually routes.
                b2=budget("unseen-budget")
                shadow=router("HISTORICAL",b2,e)
                path,rt,sid,catalog=setup("novel-reference",55)
                history=History(sid);sent=[]
                def transport(self,payload):
                    sent.append(payload["model"]);req=json.loads(payload["messages"][1]["content"])
                    return {"choices":[{"message":{"content":json.dumps(history.call(req))}}],
                            "usage":{"prompt_tokens":200,"completion_tokens":50}}
                with patch.object(wire.ExplicitJSONLLMProvider,"_request",transport):
                    self.assertEqual(execute(path,rt,sid,catalog,shadow,Live()),baseline)
                self.assertEqual(sent,["reference"])
                self.assertEqual(shadow.usage_snapshot()["receipts"][-1]["envelope_decision"],
                    "NOVEL_WITHIN_REVIEWED_ENVELOPE")
                active=router("HISTORICAL",b2,e,True)
                path,rt,sid,catalog=setup("novel-active",55);history=History(sid)
                with patch.object(wire.ExplicitJSONLLMProvider,"_request",transport):
                    self.assertEqual(execute(path,rt,sid,catalog,active,Live()),baseline)
                self.assertEqual(sent,["reference","economy"])
                self.assertEqual(active.usage_snapshot()["receipts"][-1]["allocation_basis"],
                    "SOURCEFREE_EXPERIMENTAL_ENVELOPE")
                # A failed actual owner operation still costs money; there
                # must be no opportunistic fallback or repeated send.
                path,rt,sid,catalog=setup("novel-failure",55)
                failing=router("HISTORICAL",b2,e,True)
                def bad(self,payload):
                    sent.append(payload["model"])
                    return {"choices":[{"message":{"content":"{}"}}],
                            "usage":{"prompt_tokens":200,"completion_tokens":50}}
                life=ContinuingLife(rt,path/"operator","mother",historical_provider=failing,
                    live_provider=Live(),sourcefree_attested=True,period_catalog=catalog,
                    family_sources=(sid,),mii_module=mii)
                try:
                    before=rt.ledger.events()
                    with patch.object(wire.ExplicitJSONLLMProvider,"_request",bad):
                        with self.assertRaises(Exception):life.historical_checkpoint()
                    self.assertEqual(rt.ledger.events(),before);self.assertTrue(life.status()["held"])
                    self.assertEqual(sent,["reference","economy","economy"])
                finally:life.close();rt.close()
                records=[]
                for label in ("novel-reference","novel-active","novel-failure"):
                    with sqlite3.connect(root/label/"operator"/"epoch-000000"/"ops.sqlite") as cx:
                        records.extend(json.loads(x[0]) for x in cx.execute("SELECT receipt FROM checkpoint_attempts"))
                report=lab.reconcile_budget_owner_receipts(b2,historical_receipts=records)
                self.assertEqual(report["profiles"]["economy"]["held_or_other"],1)
                self.assertEqual(report["profiles"]["economy"]["owner_operations_returned"],1)
                self.assertEqual(report["profiles"]["economy"]["known_rate_estimate_nanos"],500)
                self.assertEqual(report["profiles"]["reference"]["owner_operations_returned"],1)
                print("R61_HELD_COST",json.dumps(report["profiles"],sort_keys=True))



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


class PluralReciprocalLifeCourt(unittest.TestCase):
    """One actor's two particular relationships, not a collective will.

    Both independent dyads have actual exercises, distinct source claims
    and one shared finite world allocator. One person's withdrawal must not
    eliminate the other relationship or attribute motives to its partners.
    """
    def test_distinct_reciprocal_courses_continue_through_selective_pause_and_resume(self):
        class History:
            def __init__(self):self.requests=[];self.coarse=False
            def call(self,r):
                self.requests.append(r);ctx=r["context"];clock=ctx["clock"];n=len(self.requests)
                if r["mode"]=="TERMINAL":return {"retrospective":retro(r),"prospective":None}
                def e(label,offset,actor,acts,rules=(),span=0,peers=None):
                    return event(ctx,str(n)+":"+label,clock+offset,actor,
                        {actor:policy(acts,rules),**(peers or {})},span=span)
                def nominate(project):
                    return {"offer":"historically_possible_recurrent_routines",
                            "construct":"RECURRENT_ROUTINE","match":{"basis":{"project_ref":project}},
                            "augment":{"window_days":80,"hours_per_active_day":2.,
                                       "provisional_exposure_fraction":.5}}
                def song(peer,offset):
                    return e("song-"+peer,offset,"a",
                             [action("SING",{"project_id":"a-"+peer})],[nominate("a-"+peer)],
                             peers={peer:policy([action("SING",{"project_id":peer+"-a"})],
                                                [nominate(peer+"-a")])})
                rows=([e("coarse",7,"a",[action("REST")],span=6),
                       e("rest-b",8,"b",[action("REST")]),e("rest-c",9,"c",[action("REST")])]
                      if self.coarse else
                      [song("b",1),song("c",2),e("rest",3,"a",[action("REST")])])
                return {"retrospective":retro(r),"prospective":rows}
        class Live:
            def __init__(self):self.requests=[];self.mode="PAUSE";self.retire_both=False
            def call(self,r):
                self.requests.append(r);aid=r["principal"]
                project=("b-a" if aid=="b" else "a-b" if aid=="a" and self.retire_both else None)
                rules=[{"offer":"historically_possible_routine_revisions",
                        "construct":"RECURRENT_ROUTINE_REVISION","match":{"basis":{"project_ref":project}},
                        "augment":{"mode":self.mode,"interpretive_hypothesis":"Alter my own undertaking."}}] if project else []
                return {"policies":{aid:policy([action("REST")],rules)}}
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);db=root/"life.sqlite"
            rt=ConstitutiveRuntime(str(db))
            people=[adult(a,a.upper()) for a in ("a","b","c")]
            for person,peers in zip(people,(("b","c"),("a",),("a",))):
                person["projects"]=[{"id":person["id"]+"-"+peer,
                    "object":"sing with "+peer,"means":["SING"],"addressed_party_ref":peer,
                    "status":"active","priority":.7} for peer in peers]
            rt.ledger.initialize(blank_world(),people)
            hist=History();live=Live()
            def open_life():return ContinuingLife(rt,root/"operator","a",
                       historical_provider=hist,live_provider=live,sourcefree_attested=True,mii_module=mii)
            def world():return rt.ledger.world()[1]
            def routine(aid,project):
                p=next(x for x in rt.snapshot(aid)["projects"] if x["id"]==project)
                return p["recurrent_routines"][0]
            def periods(start):
                return [x for x in world()["historical_periods"] if x["start"]>=start]
            def coverage(start,expected):
                rows=periods(start)
                self.assertEqual(sum(x["end"]-x["start"] for x in rows),6)
                for x in rows:
                    self.assertEqual({p["source_ref"] for p in x["processes"]},expected)
                    pairs={}
                    for p in x["processes"]:
                        pairs.setdefault(p["reciprocal_routine_pair_ref"],[]).append(p)
                    self.assertTrue(all(len(v)==2 and v[0]["actor"]!=v[1]["actor"] for v in pairs.values()))
                    self.assertEqual(len(pairs),len(expected)//2)
                    loads=x["lived_practice_loads"]
                    self.assertEqual({c["source_ref"] for load in loads for c in load["claims"]},expected)
                    for load in loads:
                        self.assertGreater(load["realized_rest_expenditure_model"],0)
                        self.assertAlmostEqual(load["rest_before"]-load["rest_after"],
                                               load["realized_rest_expenditure_model"],places=5)
                        self.assertAlmostEqual(load["modeled_hours"],
                            sum(c["modeled_hours"] for c in load["claims"]),places=5)
                    a_load=next(load for load in loads if load["actor"]=="a")
                    self.assertEqual(len(a_load["claims"]),len(expected)//2)
            def revise(s,mode):
                live.mode=mode
                for _ in range(6):
                    s.independent_absent_beat()
                    rows=routine("b","b-a").get("revisions",[])
                    if rows and rows[-1]["mode"]==mode:return
                self.fail("B did not independently revise: "+str([r["principal"] for r in live.requests]))
            s=open_life()
            try:
                for _ in range(3):s.historical_checkpoint()
                ids={p:routine(a,p)["id"] for a,p in (("a","a-b"),("a","a-c"),("b","b-a"),("c","c-a"))}
                self.assertEqual(len(set(ids.values())),4)
                self.assertEqual(set(world()["routine_source_registry"]),set(ids.values()))
                for p,q in (("a-b","b-a"),("a-c","c-a")):
                    self.assertEqual(world()["routine_source_registry"][ids[p]]["basis_event_refs"],
                                     world()["routine_source_registry"][ids[q]]["basis_event_refs"])
                self.assertFalse(set(world()["routine_source_registry"][ids["a-b"]]["basis_event_refs"]) &
                                 set(world()["routine_source_registry"][ids["a-c"]]["basis_event_refs"]))
                hist.coarse=True;start=world()["clock"];s.historical_checkpoint()
                coverage(start,set(ids.values()))
                allocations=[x for x in world()["historical_time_allocations"] if x["start_clock"]>=start]
                self.assertTrue(allocations)
                self.assertTrue(all(x["actor_hour_claims_per_day"]=={"a":2.,"b":1.,"c":1.} for x in allocations))
                s.finish_history();revise(s,"PAUSE")
                old=deepcopy(world()["historical_periods"])
            finally:s.close();rt.close()
            rt=ConstitutiveRuntime(str(db));s=open_life()
            try:
                start=world()["clock"];s.resume_history()
                coverage(start,{ids["a-c"],ids["c-a"]})
                self.assertEqual(world()["historical_periods"][:len(old)],old)
                s.finish_history();revise(s,"RESUME")
                start=world()["clock"];s.resume_history();coverage(start,set(ids.values()))
                for a,p in (("a","a-b"),("a","a-c"),("c","c-a")):
                    self.assertFalse(routine(a,p).get("revisions"))
                self.assertEqual(len(routine("b","b-a")["revisions"]),2)
                self.assertEqual(set(world()["routine_source_registry"]),set(ids.values()))
                # A retired course cannot be silently resumed. Both actors
                # independently retire, then independently admit a new course
                # after three new actual shared exercises. The other relation
                # is neither retired nor automatically renewed.
                s.finish_history();live.mode="RETIRE";live.retire_both=True
                for _ in range(9):
                    s.independent_absent_beat()
                    if all(routine(a,p).get("revisions") and
                           routine(a,p)["revisions"][-1]["mode"]=="RETIRE"
                           for a,p in (("a","a-b"),("b","b-a"))):break
                else:self.fail("Both actors did not independently retire their own contribution")
                retired=max(routine(a,p)["revisions"][-1]["clock"] for a,p in (("a","a-b"),("b","b-a")))
                hist.coarse=False
                s.resume_history();s.historical_checkpoint()
                self.assertEqual(set(world()["routine_source_registry"]),set(ids.values()))
                s.historical_checkpoint()
                def last(a,p):
                    return next(x for x in rt.snapshot(a)["projects"] if x["id"]==p)["recurrent_routines"][-1]
                new_a=last("a","a-b");new_b=last("b","b-a")
                self.assertNotEqual(new_a["id"],ids["a-b"]);self.assertNotEqual(new_b["id"],ids["b-a"])
                self.assertEqual([x["event_ref"] for x in new_a["basis"]["exercises"]],
                                 [x["event_ref"] for x in new_b["basis"]["exercises"]])
                self.assertTrue(all(x["clock"]>retired for x in new_a["basis"]["exercises"]))
                self.assertEqual(set(world()["routine_source_registry"]),
                                 set(ids.values())|{new_a["id"],new_b["id"]})
                self.assertEqual(last("a","a-c")["id"],ids["a-c"])
                self.assertEqual(last("c","c-a")["id"],ids["c-a"])
                hist.coarse=True;start=world()["clock"];s.historical_checkpoint()
                coverage(start,{new_a["id"],new_b["id"],ids["a-c"],ids["c-a"]})
                self.assertTrue(rt.verify()["valid"])
                self.assertFalse(s.status()["held"])
                print("R008_PLURAL_RECIPROCAL_EPOCHS",len(hist.requests),len(live.requests),s.status()["epoch"])
            finally:s.close();rt.close()


class GenealogicalSubsistenceCourt(unittest.TestCase):
    """Adult historical construction and newborn maturation in one scarce pool.

    All meal/feeding claims originate in actual independently selected acts.
    The same two claimants compete again during compression; no scripted
    household provision envelope, invented caregiver or daily event.
    """
    def test_parent_self_reproduction_competes_with_child_nourishment(self):
        class History:
            def __init__(self,sid,meal,feed):
                self.requests=[];self.family=joined.LifeCheckpoint(sid)
                self.meal=meal;self.feed=feed;self.coarse=False
            def call(self,r):
                self.requests.append(r);ctx=r["context"];clock=ctx["clock"];n=len(self.requests)
                if r["mode"]=="TERMINAL":return {"retrospective":retro(r),"prospective":None}
                if n==1:return self.family.call(r)
                def e(label,offset,actor,acts,rules=(),span=0):
                    return event(ctx,str(n)+":"+label,clock+offset,actor,
                         {actor:policy(acts,rules)},span=span)
                def nominate(op):
                    return {"offer":"historically_possible_recurrent_routines",
                            "construct":"RECURRENT_ROUTINE","match":{"basis":{"operation":op}},
                            "augment":{"window_days":90,"hours_per_active_day":1.,
                                       "provisional_exposure_fraction":.25,"food_units_per_active_day":1.}}
                if self.coarse:
                    rows=[e("ordinary",61,"nadia",[action("ORIENT"),action("WAIT")],span=60),
                          e("mother-rest",62,"mother",[action("REST")]),
                          e("father-rest",63,"father",[action("REST")])]
                else:
                    rows=[e("mother-meal",1,"mother",[action("EAT",{"project_id":self.meal})],[nominate("EAT")]),
                          e("father-feed",2,"father",[action("FEED",{"project_id":self.feed})],[nominate("FEED")]),
                          e("child",3,"nadia",[action("ORIENT")])]
                return {"retrospective":retro(r),"prospective":rows}
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);db=root/"life.sqlite"
            rt,sid,_,constructors=joined.JoinedGenerationCourt.setup(self,db,
                extra_projects={"father":[{"object":"materially nourish Nadia","means":["CARE","FEED"],
                                           "addressed_party_ref":"nadia","priority":.85}]})
            meal=next(x["id"] for x in rt.snapshot("mother")["projects"] if "EAT" in x["means"])
            feed=next(x["id"] for x in rt.snapshot("father")["projects"] if "FEED" in x["means"])
            hist=History(sid,meal,feed);live=Live()
            def open_life():return ContinuingLife(rt,root/"operator","mother",
                       historical_provider=hist,live_provider=live,sourcefree_attested=True,
                       family_sources=(sid,),mii_module=mii)
            def world():return rt.ledger.world()[1]
            def routine(a,p):
                return next(x for x in rt.snapshot(a)["projects"] if x["id"]==p)["recurrent_routines"][0]
            s=open_life()
            try:
                s.historical_checkpoint()
                self.assertEqual(constructors,["mother","father"])
                self.assertEqual(rt.snapshot("nadia")["age_days"],0)
                for _ in range(3):s.historical_checkpoint()
                mr=routine("mother",meal);fr=routine("father",feed)
                self.assertEqual(mr["food_origin"],"SHARED_SITE_FOOD")
                self.assertEqual(fr["food_origin"],"SHARED_SITE_FOOD")
                self.assertEqual(len(mr["basis"]["exercises"]),3)
                self.assertEqual(len(fr["basis"]["exercises"]),3)
                self.assertEqual(world()["sites"]["home"]["food"],6)
                age=rt.snapshot("nadia")["age_days"]
                before=deepcopy(rt.ledger.events())
                hist.coarse=True;start=world()["clock"];s.historical_checkpoint()
                periods=[x for x in world()["historical_periods"] if x["start"]>=start]
                self.assertEqual(sum(x["end"]-x["start"] for x in periods),60)
                own=world()["material_self_meal_periods"]
                other=world()["material_provisioning_periods"]
                self.assertTrue(all(x["giver"]==x["recipient"]=="mother" and x["self_meal"] for x in own))
                self.assertTrue(all(x["giver"]=="father" and x["recipient"]=="nadia" for x in other))
                self.assertAlmostEqual(sum(x["consumed_food_units"] for x in own+other),6,places=5)
                self.assertAlmostEqual(sum(x["consumed_food_units"] for x in own),3,places=5)
                self.assertAlmostEqual(sum(x["consumed_food_units"] for x in other),3,places=5)
                self.assertEqual(world()["sites"]["home"]["food"],0)
                self.assertTrue(any(x["uncovered_food_units"]>0 for x in own))
                self.assertTrue(any(x["uncovered_food_units"]>0 for x in other))
                self.assertEqual(rt.snapshot("nadia")["age_days"],age+60)
                self.assertFalse(any(x.get("caregiver_ref")=="mother" for x in rt.snapshot("mother")["undergone_care_periods"]))
                self.assertTrue(any(x.get("caregiver_ref")=="father" for x in rt.snapshot("nadia")["undergone_care_periods"]))
                self.assertEqual(rt.ledger.events()[:len(before)],before)
                self.assertTrue(any(x.get("own_self_meal_consumption_model",0)>0 for x in routine("mother",meal)["modeled_course_receipts"]))
                s.finish_history();old=deepcopy(rt.ledger.events())
            finally:s.close();rt.close()
            rt=ConstitutiveRuntime(str(db));s=open_life()
            try:
                # Real independent absence then resumed history with no
                # replenishment grant. Source expiry must cut coverage.
                s.independent_absent_beat();s.resume_history()
                self.assertEqual(world()["sites"]["home"]["food"],0)
                self.assertEqual(sum(x["consumed_food_units"] for x in world()["material_self_meal_periods"]),3)
                self.assertEqual(sum(x["consumed_food_units"] for x in world()["material_provisioning_periods"]),3)
                self.assertEqual(rt.ledger.events()[:len(old)],old)
                self.assertEqual(constructors,["mother","father"])
                self.assertTrue(rt.verify()["valid"])
                self.assertFalse(s.status()["held"])
                print("R008_GENEALOGICAL_SUBSISTENCE",rt.snapshot("nadia")["age_days"],len(hist.requests),len(live.requests))
            finally:s.close();rt.close()


class ActorCounterofferEpochCourt(unittest.TestCase):
    """A visitor proposes, an independent Other counters, a visitor chooses.

    Neither the actor's proposed time nor an actual user acceptance is
    permission to fabricate attendance, notice, thought, or lost wages.
    """
    def test_counteroffer_requires_actual_user_assent_and_actual_later_meeting(self):
        from neighbor_runtime import EncounterRefusal
        from um_sorok_organism.material_conjunction import admit_authored_structural_history
        class History:
            def __init__(self):self.requests=[];self.target=None
            def call(self,r):
                self.requests.append(r);ctx=r["context"];clock=ctx["clock"]
                if r["mode"]=="TERMINAL":return {"retrospective":retro(r),"prospective":None}
                horizon=3 if self.target is None else self.target-clock
                self.target=None
                n=len(self.requests)
                moments=[(clock+1,"WAIT"),(clock+2,"WAIT")]
                end=clock+horizon
                if clock+2<17<=end:moments.append((17,"WORK"))
                if moments[-1][0]<end:moments.append((end,"WAIT"))
                prev=clock;rows=[]
                for j,(at,op) in enumerate(moments):
                    rule={"action":"WORK","project_id":"work"} if op=="WORK" else action("WAIT")
                    rows.append(event(ctx,str(n)+":"+str(j),at,"worker",
                        {"worker":policy([rule])},span=at-prev-1))
                    prev=at
                return {"retrospective":retro(r),"prospective":rows}
        class LiveCounter:
            def __init__(self):self.requests=[];self.phase="COUNTER_MEETING"
            def call(self,r):
                self.requests.append(r)
                match={"grounds_status":"ACTUAL_ADDRESSED_MEETING_SIGN",
                       "world_request":{"addressed_party_ref":"visitor"}}
                if self.phase=="COUNTER_MEETING":match["counter_due_clock"]=21
                return {"policies":{r["principal"]:policy([action(self.phase,match),action("WAIT")])}}
        for accept in (True,False):
            with self.subTest(accept=accept),tempfile.TemporaryDirectory() as d:
                root=Path(d);db=root/"life.sqlite"
                rt=ConstitutiveRuntime(str(db));w=blank_world()
                w["ambient"]["work_shifts"]={"worker":[{"start":16,"end":17,"source_ref":"fictional:counter-shift"}]}
                w["ambient"]["work_shift_coverage_complete"]=True
                worker=adult("worker","Worker","workshop")
                worker["projects"]=[{"id":"work","object":"earn wage","means":["WORK"],"priority":.8,"status":"active"}]
                spec={"grade":"EXPLICIT_SOURCEFREE_STRUCTURAL_HISTORY","source_ref":"fictional:counter-shift",
                    "positions":[],"rules":[{"id":"counter_shift","operation":"WORK",
                    "location":"workshop","source_ref":"fictional:counter-shift-gate",
                    "effective_from":0,"effective_until":None,"all_of":[{"kind":"SHIFT_OCCUPIED"}]}]}
                admit_authored_structural_history(w,{"worker"},spec)
                rt.ledger.initialize(w,[worker],source_seals=[("authored_structural_history",
                    "FICTIONAL_WORLD_CONDITIONING",spec)])
                hist=History();live=LiveCounter()
                def open_life():return ContinuingLife(rt,root/"operator","worker",
                    historical_provider=hist,live_provider=live,sourcefree_attested=True,mii_module=mii)
                def clock():return rt.ledger.world()[1]["clock"]
                def rows(s):return {x["id"]:x for x in s.own_meetings("visitor")}
                s=open_life()
                try:
                    s.historical_checkpoint();s.finish_history()
                    s.configure_encounter("visitor",{"grade":"SOURCEFREE_TEST_ONLY",
                        "user_conditions":{"workshop":{"light":"lit","sightline":"unobstructed",
                            "hearing":True,"sound_path":"audible","legibility":"readable"}},
                        "actor_conditions":{"worker":{"facing":"entrance","visual":True,
                            "light":"lit","sightline":"unobstructed","hearing":True,
                            "sound_path":"audible"}}},request_id="geometry")
                    s.contribute("visitor","enter","MOVE",destination="workshop")
                    first=s.contribute("visitor","proposal","PROPOSE_MEETING",target_actor_ref="worker",due_clock=18)
                    old=first["meeting_ref"]
                    self.assertEqual(rows(s)[old]["status"],"PROPOSED")
                    before=rt.snapshot("worker")["body"]["rest"]
                    s.present_until("visitor",first["event_ref"],clock()+1)
                    self.assertEqual(clock(),7)
                    self.assertEqual(rows(s)[old]["status"],"COUNTERED_BY_ACTOR")
                    new=rows(s)[old]["counter_meeting_ref"]
                    self.assertNotEqual(old,new)
                    self.assertEqual(rows(s)[old]["due_clock"],18)
                    self.assertEqual(rows(s)[new]["due_clock"],21)
                    self.assertEqual(rows(s)[new]["counteroffer_from_meeting_ref"],old)
                    self.assertEqual(rows(s)[new]["status"],"ACTOR_COUNTEROFFER_PENDING")
                    self.assertLess(rt.snapshot("worker")["body"]["rest"],before)
                    prefix=deepcopy(rt.ledger.events())
                finally:s.close();rt.close()
                rt=ConstitutiveRuntime(str(db));s=open_life()
                try:
                    before=deepcopy(rt.ledger.world())
                    with self.assertRaisesRegex(ValueError,"MEETING_COUNTER_ACCEPTANCE_NOT_QUALIFIED"):
                        s.contribute("visitor","wrong","ACCEPT_COUNTER_MEETING",target_commitment_ref=old)
                    self.assertEqual(rt.ledger.world(),before)
                    self.assertEqual(s.own_meetings("outsider"),[])
                    self.assertFalse(s.status()["held"])
                    if accept:
                        old_actor=deepcopy(rt.ledger.actors())
                        consent=s.contribute("visitor","accept","ACCEPT_COUNTER_MEETING",target_commitment_ref=new)
                        self.assertEqual(consent["potential_actor_evidence"],[])
                        self.assertEqual(rt.ledger.actors(),old_actor)
                        self.assertEqual(rows(s)[new]["status"],"ACCEPTED")
                        self.assertEqual(rows(s)[new]["acceptance_source_user_event_ref"],consent["event_ref"])
                        self.assertTrue(s.contribute("visitor","accept","ACCEPT_COUNTER_MEETING",
                                                     target_commitment_ref=new)["idempotent_replay"])
                    s.contribute("visitor","leave","LEAVE")
                    hist.target=17 if accept else 21
                    s.resume_history();s.finish_history()
                    # Actual alternative life at the abandoned original
                    # meeting time, not a counterfactual wage or reason.
                    self.assertEqual(rt.ledger.world()[1]["accounts"].get("worker",0),.25)
                    work=[x for x in rt.ledger.world()[1]["public_history"] if x.get("action")=="WORK"]
                    self.assertEqual([(x["clock"],x["status"]) for x in work],[(17,"PERFORMED")])
                    self.assertEqual(rt.ledger.events()[:len(prefix)],prefix)
                finally:s.close();rt.close()
                rt=ConstitutiveRuntime(str(db));s=open_life()
                try:
                    if accept:
                        s.contribute("visitor","return","MOVE",destination="workshop")
                        check=s.contribute("visitor","checkin","CHECK_IN_MEETING",target_commitment_ref=new)
                        live.phase="MEET_VISITOR"
                        s.present_until("visitor",check["event_ref"],clock()+1)
                        self.assertEqual(rows(s)[new]["status"],"MEETING_PERFORMED")
                        self.assertEqual(len(live.requests),2)
                    else:
                        self.assertEqual(rows(s)[new]["status"],"ELAPSED_WITHOUT_USER_ACCEPTANCE")
                        self.assertEqual(len(live.requests),1)
                    self.assertEqual(rows(s)[old]["status"],"COUNTERED_BY_ACTOR")
                    self.assertEqual(rows(s)[old]["due_clock"],18)
                    self.assertFalse(s.status()["held"])
                    self.assertTrue(rt.verify()["valid"])
                    print("R008_ACTOR_COUNTEROFFER",accept,clock(),len(hist.requests),len(live.requests))
                finally:s.close();rt.close()
