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

if __name__=="__main__":unittest.main()
