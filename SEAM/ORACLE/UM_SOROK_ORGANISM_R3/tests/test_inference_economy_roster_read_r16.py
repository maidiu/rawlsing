"""Single-statement version/body roster read. Keep full audit and CAS."""
from collections import Counter
from pathlib import Path
from time import perf_counter_ns
from unittest.mock import patch
import tempfile
import unittest

from um_sorok_organism import storage
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import canonical
import test_tco_r23_relational_transduction as r32


def legacy_read(ledger):
    versions={aid:ledger.actor(aid)[0] for aid in ledger.actors()}
    actors=ledger.actors()
    return versions,actors


class RosterReadEconomyR16(unittest.TestCase):
    def _course(self,path,legacy):
        counts=Counter();sizes=Counter();times=[]
        original=storage.ResearchLedger.actors_with_versions
        original_load=storage.json.loads
        def roster(ledger):
            n=0;size=0;queries=[]
            def loads(raw,*args,**kw):
                nonlocal n,size
                n+=1;size+=len(raw.encode("utf-8"))
                return original_load(raw,*args,**kw)
            start=perf_counter_ns()
            ledger.conn.set_trace_callback(queries.append)
            try:
                with patch.object(storage.json,"loads",loads):
                    result=(legacy_read if legacy else original)(ledger)
            finally:ledger.conn.set_trace_callback(None)
            times.append(perf_counter_ns()-start)
            self.assertEqual(len(result[0]),len(result[1]))
            count=len(result[1])
            self.assertEqual(n,(3 if legacy else 1)*count)
            self.assertEqual(len(queries),count+2 if legacy else 1)
            counts["reads"]+=1;counts["queries"]+=len(queries)
            counts["decoded_actor_bodies"]+=n
            sizes["decoded_body_bytes"]+=size
            return result
        with patch.object(storage.ResearchLedger,"actors_with_versions",roster):
            service,*_=r32.CrossContextMetabolismR32._run_history(str(path),"revalue")
            rt=ConstitutiveRuntime(path,semantic=service)
            try:
                actual=rt.step("mother")
                period=rt.background(30)
                state={"actors":rt.ledger.actors(),"world":rt.ledger.world()[1],
                       "events":rt.ledger.events(),"audit":rt.verify(),
                       "actual":actual,"period":period}
                self.assertTrue(state["audit"]["valid"])
                self.assertEqual(actual["attempt"],"REST")
            finally:rt.close()
        return state,{**dict(counts),**dict(sizes),"elapsed_ns":sum(times)}

    def test_real_revaluation_and_compressed_life_preserve_complete_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            a,old=self._course(Path(tmp)/"old.sqlite",True)
            b,new=self._course(Path(tmp)/"new.sqlite",False)
        self.assertEqual(a,b)
        self.assertEqual(old["reads"],new["reads"])
        self.assertEqual(old["decoded_actor_bodies"],3*new["decoded_actor_bodies"])
        self.assertEqual(old["decoded_body_bytes"],3*new["decoded_body_bytes"])
        print("INFERENCE_ECONOMY_R16_ROSTER "+canonical({"old":old,"new":new,
              "exact_complete_history":True}))

    def test_cas_remains_authoritative_and_no_trusted_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"stale.sqlite"
            rt=ConstitutiveRuntime(path)
            try:
                rt.initialize()
                wv,world=rt.ledger.world(rt.world_id)
                versions,actors=rt.ledger.actors_with_versions()
                self.assertEqual((versions,actors),legacy_read(rt.ledger))
                # A real later transition makes all earlier read versions stale.
                other=ConstitutiveRuntime(path)
                try:other.background(1)
                finally:other.close()
                before=rt.verify()
                with self.assertRaisesRegex(storage.Conflict,"STALE_WORLD"):
                    rt.ledger.commit(rt.world_id,wv,world,actors,versions,
                                     "SOURCEFREE_TEST_ATTEMPT",None,{})
                current_v,current_w=rt.ledger.world(rt.world_id)
                fresh_versions,fresh_actors=rt.ledger.actors_with_versions()
                self.assertNotEqual(fresh_versions,versions)
                with self.assertRaisesRegex(storage.Conflict,"STALE_ACTOR"):
                    rt.ledger.commit(rt.world_id,current_v,current_w,
                        fresh_actors,versions,"SOURCEFREE_TEST_ATTEMPT",None,{})
                self.assertEqual(rt.verify(),before)
                self.assertEqual(rt.ledger.actors_with_versions(),(fresh_versions,fresh_actors))
            finally:rt.close()


if __name__=="__main__":unittest.main()
