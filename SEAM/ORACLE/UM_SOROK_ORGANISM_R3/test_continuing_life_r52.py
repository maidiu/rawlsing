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

if __name__=="__main__":unittest.main()
