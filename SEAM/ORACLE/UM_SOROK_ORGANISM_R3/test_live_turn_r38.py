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

if __name__=="__main__":unittest.main()
