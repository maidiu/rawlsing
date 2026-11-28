"""R38 real one-response live turn, independent world/actor/MII owners."""
import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from importlib.util import spec_from_file_location,module_from_spec

import test_neighbor_material_support_r17 as owner_paths
from neighbor_runtime import NeighborEncounter
import mii
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,newborn,blank_world,canonical
from um_sorok_organism.world import register_recursive_encounter_paths
from live_turn_port_r38 import LiveTurnSession
from developmental_recursion.contracts import RecursionRefusal
from test_modern_generation_port_r28 import policy,action

PRIVATE="A private thought not offered to the visitor."
WORDS="I was worried about tomorrow."
def transport(callback):
    spec=spec_from_file_location("um_sorok_organism.specialist_live_transport",
        Path(__file__).parent/"um_sorok_organism"/"live_psychological_llm.py")
    mod=module_from_spec(spec);spec.loader.exec_module(mod)
    def mock(req):
        doc=json.loads(req["messages"][1]["content"])
        answer=callback(doc)
        return {"choices":[{"message":{"content":json.dumps(answer)}}]}
    return mod.ExplicitLiveTurnProvider(endpoint="https://example.invalid/chat/completions",
        model="fixture",api_key="not-a-key",allow_private_actor_data=True,
        sourcefree_live_attested=True,transport=mock,metrics_capacity=1)

def geometry(n,actors):
    n.install_sourcefree_conditions({"grade":"SOURCEFREE_TEST_ONLY",
       "user_conditions":{"workshop":{"light":"lit","sightline":"unobstructed",
          "hearing":True,"sound_path":"audible","legibility":"readable"}},
       "actor_conditions":{a:{"facing":"entrance","visual":True,"light":"lit",
          "sightline":"unobstructed","hearing":True,"sound_path":"audible"} for a in actors}},
          request_id="geometry")
    if n.contribute("entry","MOVE",destination="workshop")["status"]!="PERFORMED":
        raise AssertionError("entry not performed")

class OneResponseLiveCourt(unittest.TestCase):
    def setup_lexical(self,db):
        rt=ConstitutiveRuntime(str(db))
        speaker=adult("speaker","Speaker","workshop")
        speaker["projects"]=[{"id":"talk","object":"speak","means":["SPEAK"],"priority":.6,"status":"active"}]
        speaker["self_model"]={"private":PRIVATE}
        listener=adult("listener","Listener","workshop")
        listener["projects"]=[{"id":"work","object":"earn wage","means":["WORK"],"priority":.65,"status":"active"},
                              {"id":"rest","object":"rest","means":["REST"],"priority":.4,"status":"active"}]
        w=blank_world();register_recursive_encounter_paths(w,{"speaker":speaker,"listener":listener},
          {"grade":"SOURCEFREE_TEST_ONLY","source_ref":"fictional:live-address","paths":[
             {"observer":"listener","source_actor":"speaker","location":"workshop","from_clock":0,
              "through_clock":30,"hearing":True,"sound_path":"audible","visual":True,"light":"lit",
              "sightline":"unobstructed","facing":"source"}]})
        rt.ledger.initialize(w,[speaker,listener])
        return rt

    def test_actual_live_lexical_revaluation_cold_selection_and_no_user_replay(self):
        for target in ("listener","visitor"):
            with self.subTest(target=target),TemporaryDirectory() as d:
                f=Path(d);rt=self.setup_lexical(f/"life.sqlite")
                def call(req):
                    a=req["principal"]
                    if a=="speaker":
                        speech=policy([{"action":"SPEAK","pool":"addressed_lexical_options",
                             "option_match":{"project_id":"talk","world_request":{"addressed_party_ref":target}},
                             "speech_intent":"Share a worry."}])
                        speech["expression"]={"speech":WORDS,"surface":"Ordinary life."}
                        learn=policy([], [{"offer":"historically_possible_lexical_project_revaluations",
                             "construct":"LEXICAL_PROJECT_REVALUATION","match":{"project_id":"work",
                               "lexical_revaluation_basis":{"lexical_acquisition_route":"VOLUNTARILY_ADDRESSED_TO_SELF"}},
                             "augment":{"priority":.1,"personal_significance":"Perhaps I can take a moment to listen."}}])
                        return {"policies":{"speaker":speech,"listener":learn}}
                    return {"policies":{"listener":policy([{"action":"SELECT_HIGHEST_CURRENT_PROJECT_COURSE",
                            "project_course_actions":["WORK","REST"]},action("WAIT")])}}
                wire=transport(call)
                session=LiveTurnSession(rt,wire,f/"attempts.sqlite",sourcefree_attested=True)
                try:
                    n=NeighborEncounter(rt,"visitor",mii_module=mii)
                    self.assertEqual(session.owner_actor_beat(n,"listener")["attempt"],"WORK")
                    geometry(n,["speaker","listener"])
                    self.assertEqual(session.owner_actor_beat(n,"speaker")["attempt"],"SPEAK")
                    view=n.private_surface(n.new_private_profile())
                    self.assertIn(WORDS,canonical(view));self.assertNotIn(PRIVATE,canonical(view))
                    self.assertEqual(session.custody.receipts()[-1]["conditional_routes"].get("typed_lexical_project_revaluation",0),int(target=="listener"))
                    self.assertEqual(wire.usage_snapshot()["total"],2)
                    before=rt.verify()
                    self.assertEqual(session.after_user_contribution(n)["status"],"ALREADY_ADVANCED_AFTER_USER_OCCASION")
                    self.assertEqual(rt.verify(),before)
                    self.assertEqual(wire.usage_snapshot()["total"],2)
                finally:session.close();rt.close()
                rt=ConstitutiveRuntime(str(f/"life.sqlite"))
                session=LiveTurnSession(rt,wire,f/"attempts.sqlite",sourcefree_attested=True)
                try:
                    n=NeighborEncounter(rt,"visitor",mii_module=mii)
                    out=session.owner_actor_beat(n,"listener")
                    self.assertEqual(out["attempt"],"REST" if target=="listener" else "WORK")
                    receipts=session.custody.receipts()
                    self.assertEqual(len(receipts),3)
                    self.assertTrue(all(r["transport_receipt"]["attempts"]==1 and r["outcome"]=="ACTUAL_TURN_COMMITTED" for r in receipts))
                    self.assertEqual(wire.usage_snapshot()["evicted"],2)
                    self.assertTrue(rt.verify()["valid"])
                    print("R38_LIVE_LEXICAL "+json.dumps({"target":target,"later":out["attempt"],
                        "transport_calls":len(receipts),"local_tasks":sum(sum(r["local_semantic_tasks"].values()) for r in receipts),
                        "wire_bytes":sum(r["transport_receipt"]["request_bytes"] for r in receipts)},sort_keys=True))
                finally:session.close();rt.close()

    def test_actual_authored_occasion_and_foreign_policy_hold_no_retry(self):
        for invalid in (True,False):
            with self.subTest(invalid=invalid),TemporaryDirectory() as d:
                f=Path(d);rt=self.setup_lexical(f/"life.sqlite")
                n=NeighborEncounter(rt,"visitor",mii_module=mii);geometry(n,["speaker","listener"])
                def call(req):
                    principal=req["principal"]
                    return {"policies":{"visitor" if invalid else principal:policy([action("WAIT")])}}
                wire=transport(call);session=LiveTurnSession(rt,wire,f/"attempts.sqlite",sourcefree_attested=True)
                before=rt.verify()
                try:
                    if invalid:
                        with self.assertRaisesRegex(RecursionRefusal,"LIVE_POLICY_FOREIGN_ACTOR"):
                            session.after_user_contribution(n,profile=n.new_private_profile())
                        self.assertEqual(rt.verify(),before)
                    else:
                        out=session.after_user_contribution(n,profile=n.new_private_profile())
                        self.assertEqual(out["status"],"INDEPENDENT_ACTOR_WORLD_EVENT_COMMITTED")
                        self.assertTrue(out["new_world_event"]);self.assertNotIn(PRIVATE,canonical(out))
                    self.assertEqual(wire.usage_snapshot()["total"],1)
                finally:session.close();rt.close()
                rt=ConstitutiveRuntime(str(f/"life.sqlite"));n=NeighborEncounter(rt,"visitor",mii_module=mii)
                session=LiveTurnSession(rt,wire,f/"attempts.sqlite",sourcefree_attested=True)
                try:
                    if invalid:
                        with self.assertRaisesRegex(RecursionRefusal,"LIVE_PREVIOUS_ATTEMPT_REQUIRES_DISPOSITION"):
                            session.after_user_contribution(n)
                        self.assertEqual(rt.verify(),before)
                        self.assertEqual(session.custody.receipts()[0]["outcome"],"HELD_OWNER_OR_PROVIDER")
                    else:
                        self.assertEqual(session.after_user_contribution(n)["status"],"ALREADY_ADVANCED_AFTER_USER_OCCASION")
                    self.assertEqual(wire.usage_snapshot()["total"],1)
                    self.assertEqual(len(session.custody.receipts()),1)
                finally:session.close();rt.close()


    def test_present_polycentric_owner_four_beats_cold_resume_and_no_replayed_exposure(self):
        with TemporaryDirectory() as d:
            f=Path(d);rt=self.setup_lexical(f/"life.sqlite")
            def call(req):
                return {"policies":{req["principal"]:policy([action("WAIT")])}}
            wire=transport(call);session=LiveTurnSession(rt,wire,f/"attempts.sqlite",sourcefree_attested=True)
            try:
                n=session.bind_neighbor("visitor",mii_module=mii)
                geometry(n,["speaker","listener"])
                w=rt.ledger.world()[1];ref=w["neighbor_user_events"][-1]["event_ref"]
                target=w["clock"]+4
                profile=n.new_private_profile()
                first=n.continue_present_life_until(ref,target,max_beats=2,profile=profile)
                self.assertEqual(first["status"],"HELD_AT_BOUNDED_PRESENT_CONTINUATION")
                self.assertEqual(first["beats_committed_this_call"],2)
                self.assertEqual(len(first["new_present_surfaces"]),2)
                self.assertEqual(wire.usage_snapshot()["total"],2)
            finally:session.close();rt.close()
            rt=ConstitutiveRuntime(str(f/"life.sqlite"));session=LiveTurnSession(rt,wire,f/"attempts.sqlite",sourcefree_attested=True)
            try:
                n=session.bind_neighbor("visitor",mii_module=mii)
                second=n.continue_present_life_until(ref,target,profile=profile)
                self.assertEqual(second["status"],"AT_OR_PAST_PRESENT_TARGET")
                self.assertEqual(second["beats_committed_this_call"],2)
                self.assertEqual(len(second["new_present_surfaces"]),2)
                rows=session.custody.receipts()
                self.assertEqual({x["principal"] for x in rows},{"speaker","listener"})
                self.assertEqual(len(rows),4)
                self.assertTrue(all(x["transport_receipt"]["attempts"]==1 for x in rows))
                retry=n.continue_present_life_until(ref,target,profile=profile)
                self.assertEqual(retry["beats_committed_this_call"],0)
                self.assertEqual(retry["new_present_surfaces"],[])
                self.assertEqual(wire.usage_snapshot()["total"],4)
                self.assertTrue(rt.verify()["valid"])
                print("R40_PRESENT "+json.dumps({"beats":len(rows),"transport_calls":wire.usage_snapshot()["total"],
                      "per_mode_actual_exposures":len(first["new_present_surfaces"])+len(second["new_present_surfaces"]),
                      "actor_roster":sorted({x["principal"] for x in rows})},sort_keys=True))
            finally:session.close();rt.close()

    def test_actual_developmental_care_and_independent_refusal_in_one_response(self):
        # Actual R63 acquired personal regulation, not stipulated child trust.
        with TemporaryDirectory() as d:
            f=Path(d);rt=ConstitutiveRuntime(str(f/"life.sqlite"))
            m=adult("mother","Mother","workshop");m["body"]["rest"]=.35
            father=adult("father","Father","workshop")
            child=newborn("nadia","Nadia","workshop");child["body"]["comfort"]=.2
            for a in (m,father):
                a["projects"]=[{"id":"care:"+a["id"],"object":"care for Nadia","means":["CARE"],
                  "addressed_party_ref":"nadia","priority":.6,"status":"active"}]
            rt.ledger.initialize(blank_world(),[m,father,child])
            stage={"address":False}
            def call(req):
                a=req["principal"]
                acquire=policy([], [{"offer":"historically_possible_plural_care",
                      "resolver":"EXISTING_PLURAL_CARE_SOURCE_RESOLUTION"}])
                if a!="nadia":
                    return {"policies":{a:policy([action("CARE",{"project_id":"care:"+a,
                        "world_request":{"addressed_party_ref":"nadia"}}),action("REST")]),"nadia":acquire}}
                acquire["actions"]=([{"action":"SIGNAL","option_match":{"grounds_status":"HISTORICALLY_ACQUIRED_CO_REGULATION"},
                    "rank_by":"LATEST_PERSONALLY_SENSED_REGULATION"}] if stage["address"] else [])+[action("ORIENT"),action("WAIT")]
                return {"policies":{"nadia":acquire,"mother":policy([action("REFUSE")]),"father":policy([action("REFUSE")])}}
            wire=transport(call);session=LiveTurnSession(rt,wire,f/"attempts.sqlite",sourcefree_attested=True)
            try:
                n=NeighborEncounter(rt,"visitor",mii_module=mii)
                for aid in ("father","mother"):
                    self.assertEqual(session.owner_actor_beat(n,aid)["attempt"],"CARE")
                # Actual received care is not yet an acquired orientation.
                self.assertFalse(rt.ledger.actor("nadia")[1]["co_regulation_orientations"])
                for _ in range(2):
                    self.assertEqual(session.owner_actor_beat(n,"nadia")["attempt"],"ORIENT")
                self.assertEqual({x["caregiver_ref"] for x in rt.ledger.actor("nadia")[1]["co_regulation_orientations"]},
                                 {"mother","father"})
                stage["address"]=True
                out=session.owner_actor_beat(n,"nadia")
                self.assertEqual(out["attempt"],"SIGNAL")
                self.assertEqual(out["status"],"PARTIAL")
                evt=rt.ledger.latest_event()["envelope"]["payload"]
                self.assertIsNotNone(evt["coactor_attempt"])
                row=session.custody.receipts()[-1]
                self.assertEqual(row["local_semantic_tasks"]["actor_attempt"],2)
                self.assertEqual(wire.usage_snapshot()["total"],5)
                self.assertTrue(rt.verify()["valid"])
                print("R40_CARE "+json.dumps({"calls":5,"child_attempt":out["attempt"],"actual_status":out["status"],
                    "actual_coactor_attempt":evt["coactor_attempt"]["action"],"local_attempt_tasks":2},sort_keys=True))
            finally:session.close();rt.close()


    def test_rare_actual_private_reconsideration_after_generation_changes_live_eligibility(self):
        # Same sourcefree actor history, via the existing inherited generation
        # machinery, followed by one live private activity, then later choice.
        from test_modern_generation_port_r28 import ModernGenerationCourt,RepairCheckpoint,MEANING
        for nominate in (True,False):
            with self.subTest(nominate=nominate),TemporaryDirectory() as d:
                f=Path(d);rt,refs=ModernGenerationCourt.setup_repair(self,f/"life.sqlite")
                p=RepairCheckpoint(refs)
                g=ModernGenerationCourt.generation(self,rt,f,"worker",p)
                try:
                    b=g.bootstrap();ref=b["records"][0]["accessible"]["objective_ref"]
                    self.assertTrue(any(x["action"]=="EAT" for x in rt.situated("worker")["suspended_actions"]))
                    g.finish();g.terminal_handoff()
                finally:g.close();rt.close()
                rt=ConstitutiveRuntime(str(f/"life.sqlite"))
                calls=[]
                def call(req):
                    calls.append(req)
                    answer={"policies":{"worker":policy([action("WAIT") if len(calls)==1 else action("EAT"),action("WAIT")])}}
                    if nominate and len(calls)==1:answer["private_rehearsal"]={"objective_ref":ref,"meaning":MEANING}
                    return answer
                wire=transport(call);session=LiveTurnSession(rt,wire,f/"live.sqlite",sourcefree_attested=True)
                try:
                    food=rt.ledger.world()[1]["sites"]["home"]["food"]
                    n=NeighborEncounter(rt,"visitor",mii_module=mii)
                    first=session.owner_actor_beat(n,"worker")
                    self.assertEqual(first["attempt"],"WAIT")
                    a=rt.ledger.actor("worker")[1]
                    self.assertEqual(len(a["historical_orientations"][0].get("revisions",[])),int(nominate))
                    self.assertNotIn(MEANING,canonical(rt.ledger.world()[1]))
                finally:session.close();rt.close()
                rt=ConstitutiveRuntime(str(f/"life.sqlite"));session=LiveTurnSession(rt,wire,f/"live.sqlite",sourcefree_attested=True)
                try:
                    out=session.owner_actor_beat(NeighborEncounter(rt,"visitor",mii_module=mii),"worker")
                    self.assertEqual(out["attempt"],"EAT" if nominate else "WAIT")
                    self.assertEqual(rt.ledger.world()[1]["sites"]["home"]["food"],food-int(nominate))
                    self.assertEqual(wire.usage_snapshot()["total"],2)
                    self.assertEqual(len(session.custody.receipts()),2)
                    self.assertTrue(rt.verify()["valid"])
                    print("R41_LIVE_RECONSIDERATION "+json.dumps({"nominate":nominate,"later":out["attempt"],
                        "actual_live_calls":2,"generation_calls":len(p.requests)},sort_keys=True))
                finally:session.close();rt.close()

if __name__=="__main__":unittest.main()
