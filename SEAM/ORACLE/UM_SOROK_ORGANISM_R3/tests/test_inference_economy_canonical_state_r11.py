"""Exact byte reuse in the existing ledger's full REMONT verification.

No new trust, no persistent cache, no skipped history or actor/visitor access
change. Canonical comparison remains mandatory *before* hashing stored bytes.
"""
from collections import Counter
from pathlib import Path
from time import perf_counter_ns
from unittest.mock import patch
import sqlite3
import tempfile
import unittest

from um_sorok_organism import storage
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import canonical, digest
import test_tco_r23_relational_transduction as r32
import test_inference_economy_history_reconstruction_r8 as r8


class CanonicalStateEconomyR11(unittest.TestCase):
    def test_exact_hash_preimages(self):
        values=[None,True,1,-0.0,2.5,"é👋\n\\\"",[],{},
                {"a":[1,True,None],"z":{"β":"x"*100000}}]
        for v in values:
            raw=canonical(v)
            self.assertEqual(storage._canonical_object_hash(v,raw),digest(v))
            for cat in ("SOURCE","é\\\"\n"):
                self.assertEqual(storage._canonical_seal_hash(cat,v,raw),
                                 digest({"category":cat,"content":v}))

    def _measure(self,rt,legacy):
        counts=Counter()
        old_object=storage._canonical_object_hash
        old_seal=storage._canonical_seal_hash
        original_event=storage._canonical_event_hashes
        def state(value,raw):
            counts["snapshot_hashes"]+=1
            counts["snapshot_canonical_bytes_reused"]+=len(raw.encode("utf-8"))
            return digest(value) if legacy else old_object(value,raw)
        def seal(category,value,raw):
            counts["seal_hashes"]+=1
            counts["seal_content_bytes_reused"]+=len(raw.encode("utf-8"))
            return digest({"category":category,"content":value}) if legacy else old_seal(category,value,raw)
        def events(env,raw,prior,eid):
            counts["event_hashes"]+=1
            return original_event(env,raw,prior,eid)
        start=perf_counter_ns()
        with patch.object(storage,"_canonical_object_hash",state), \
             patch.object(storage,"_canonical_seal_hash",seal), \
             patch.object(storage,"_canonical_event_hashes",events):
            result=rt.verify()
            with rt.ledger.tx():
                rt.ledger._verify_current_anchor_locked(rt.world_id)
        return result,dict(counts),perf_counter_ns()-start

    def test_actual_history_full_audit_and_anchor_conserve_identity(self):
        rows=[]
        with tempfile.TemporaryDirectory() as tmp:
            for decision in ("abstain","revalue"):
                src=Path(tmp)/(decision+".sqlite")
                r32.CrossContextMetabolismR32._run_history(str(src),decision)
                rt=ConstitutiveRuntime(src)
                try:
                    rt.ledger.seal_source("late_economy_witness","SOURCEFREE_TEST",
                        {"unicode":"é","data":["x"*10000,None,True]})
                    expected=rt.verify()
                    original_events=rt.ledger.events()
                    values=[self._measure(rt,legacy) for legacy in (True,False,False,True)]
                    for result,counts,_ in values:
                        self.assertEqual(result,expected)
                        self.assertEqual(counts,values[0][1])
                    counts=values[0][1]
                    self.assertGreater(counts["snapshot_canonical_bytes_reused"],1000)
                    self.assertGreater(counts["seal_content_bytes_reused"],20000)
                    self.assertEqual(rt.ledger.events(),original_events)
                    rows.append({"decision":decision,"events":expected["events"],
                        "counts_per_audit_and_anchor":counts,
                        "legacy_ns":[values[i][2] for i in (0,3)],
                        "reuse_ns":[values[i][2] for i in (1,2)]})
                finally:rt.close()
                # Cold continuation under the exact same committed starting DB.
                # Reference changes only canonical digest computation.
                paths=[Path(tmp)/(decision+str(i)+".sqlite") for i in range(2)]
                for path in paths:
                    with sqlite3.connect(src) as a,sqlite3.connect(path) as b:a.backup(b)
                reader=r8.HistoricalReconstructionR8()
                with patch.object(storage,"_canonical_object_hash",lambda v,r:digest(v)), \
                     patch.object(storage,"_canonical_seal_hash",
                                  lambda cat,v,r:digest({"category":cat,"content":v})):
                    legacy,_=reader._continue(paths[0],[],False)
                fresh,_=reader._continue(paths[1],[],False)
                self.assertEqual(legacy,fresh)
        print("INFERENCE_ECONOMY_R11_CANONICAL "+canonical(rows))

    def test_noncanonical_and_changed_state_still_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            rt=ConstitutiveRuntime(Path(tmp)/"adversary.sqlite")
            try:
                rt.initialize()
                rt.ledger.seal_source("late","SOURCEFREE_TEST",{"a":"é"})
                conn=rt.ledger.conn
                clean=rt.verify()
                for table,key,ident,col in (
                    ("worlds","id",rt.world_id,"body"),
                    ("actors","id","nadia","body"),
                    ("source_seals","id","late","content")):
                    raw=conn.execute(f"SELECT {col} FROM {table} WHERE {key}=?",(ident,)).fetchone()[0]
                    for changed in (raw+" ",canonical({"a":"different"})):
                        conn.execute(f"UPDATE {table} SET {col}=? WHERE {key}=?",(changed,ident))
                        with self.assertRaises((AssertionError,KeyError,TypeError)):
                            rt.verify()
                        with self.assertRaises(storage.Conflict):
                            rt.ledger.source("late")
                        # Check that an otherwise legal append cannot launder it.
                        with self.assertRaises(storage.Conflict):
                            rt.ledger.seal_source("unauthorized","TEST",{})
                        conn.execute(f"UPDATE {table} SET {col}=? WHERE {key}=?",(raw,ident))
                        self.assertEqual(rt.verify(),clean)
            finally:rt.close()


if __name__=="__main__":
    unittest.main()
