"""Local, sourcefree physical-layout regression tests (not native C11 G5)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from .stores import ARMS,FAMILIES,Store,StoreFailure,canonical

class MockBatch:
    def __init__(self, rows):
        self.rows=rows
    def to_pylist(self):
        return self.rows

class MockParquet:
    def __init__(self, rows):
        self.rows=rows
    def read_row_group(self, gid, columns=None):
        return MockBatch([{k:r[k] for k in columns} if columns else r for r in self.rows])
    def close(self):
        pass

def fixture():
    respondents=["RespondentIdentity@1.0.0|r1|"+"a"*64,
                 "RespondentIdentity@1.0.0|r2|"+"b"*64]
    qs=["QUESTION|Q"+str(i)+"|"+"c"*64 for i in range(3)]
    out={f:[] for f in FAMILIES}
    for family in FAMILIES:
        n=2 if family=="RespondentIdentity" else (1 if family!="RespondentEvent" else 6)
        for i in range(n):
            r=respondents[i] if family=="RespondentIdentity" else family+"|item"+str(i)+"|"+"e"*64
            if family=="RespondentEvent":
                r=family+"|event"+str(i)+"|"+hashlib.sha256(str(i).encode()).hexdigest()
            data={"family":family,"ref":r,"typed_state":"OBSERVED",
                  "universe":"UNIVERSE|one|"+"f"*64,
                  "respondent":respondents[i%2] if family in (
                      "RespondentEvent","RoutingEligibilityFact",
                      "EmpiricalCoordinateFact","WeightMeasureFact") else "",
                  "native":qs[(i//2)%3] if family=="RespondentEvent" else "",
                  "canonical":"","component":"","raw_typed":'{"t":"int","v":"2"}',
                  "body_json":canonical({"ref":r,"family":family,
                                         "payload":"AAaa"+"value"*3})}
            out[family].append(data)
    return out,qs,respondents

def family_expected(rows):
    result={}
    for fam,rr in rows.items():
        h=hashlib.sha256()
        for row in rr:
            buf=(row["ref"]+"\x00"+row["body_json"]).encode()
            h.update(len(buf).to_bytes(8,"big"));h.update(buf)
        result[fam]={"count":len(rr),"digest":h.hexdigest()}
    return result

class PhysicalStoresTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.home=Path(self.tmp.name)
        self.data,self.qs,self.respondents=fixture()
        self.identity={"schema":"ANVIL_STREAM_C11_ESTATE@1",
                       "manifest_sha256":"f"*64,
                       "source_id":"SOURCEFREE_TEST",
                       "roots":{"logical":"a"*64}}
        self.expected=family_expected(self.data)
    def tearDown(self):
        self.tmp.cleanup()

    def build(self,name):
        p=self.home/(name+".sqlite")
        store=Store(name,p,self.home,create=True,source_identity=self.identity)
        for fam,rows in self.data.items():
            if name=="H":
                store._pq[fam]=MockParquet(rows)
            for idx,row in enumerate(rows):
                routing=(self.qs[0],"RISK|set|"+"d"*64) if fam=="RoutingEligibilityFact" else None
                store.add_row(fam,idx,row,0,idx,routing=routing)
            store.commit_batch()
        store.finish({"schema":"ANVIL_STREAM_C11_ESTATE@1"},self.expected)
        self.assertEqual(store.get_meta("state"),"AUDIT_PENDING")
        store.audit_families()
        self.assertEqual(store.get_meta("state"),"COMMITTED")
        return store

    def test_all_four_exact_body_and_positive_queries(self):
        reports={}
        for name in ARMS:
            with self.subTest(arm=name):
                s=self.build(name)
                self.assertEqual(s.audit_families(),self.expected)
                q=s.get_question_refs(3)
                self.assertEqual(len(q),3)
                self.assertEqual({x["respondents"] for x in (
                    s.probe_query(target) for target in q)}, {2})
                self.assertEqual(s.joint_probe(q)["co_present_respondents"],2)
                if name=="S1":
                    # Full TEXT lookup is a direct SQL key, not a preflight
                    # dictionary membership test; absence is established by
                    # the resulting zero rows or strict fetch_body refusal.
                    self.assertEqual(s.find_id("missing|ref"),"missing|ref")
                else:
                    self.assertIsNone(s.find_id("missing|ref"))
                initial=s.stats()["objects"]
                s.store_result("op-1",{"q":"sourcefree"},"TEST_ONLY",{"answer":[3,4]},12.5)
                self.assertEqual(s.db.execute("SELECT COUNT(*) FROM results").fetchone()[0],1)
                self.assertEqual(s.stats()["objects"],initial)
                reports[name]=[s.probe_query(ref)["digest"] for ref in self.qs]
                s.close()
        self.assertEqual(len({tuple(v) for v in reports.values()}),1)

    def _build_unsealed(self, name):
        store=Store(name,self.home/(name+".sqlite"),self.home,
                    create=True,source_identity=self.identity)
        for fam,rows in self.data.items():
            if name=="H":
                store._pq[fam]=MockParquet(rows)
            for idx,row in enumerate(rows):
                routing=(self.qs[0],"RISK|set|"+"d"*64) if fam=="RoutingEligibilityFact" else None
                store.add_row(fam,idx,row,0,idx,routing=routing)
            store.commit_batch()
        store.finish({"schema":"ANVIL_STREAM_C11_ESTATE@1"},self.expected)
        return store

    def test_unfinished_audit_cannot_publish_or_cold_reopen(self):
        s=self._build_unsealed("S2")
        self.assertEqual(s.get_meta("state"),"AUDIT_PENDING")
        s.close()
        with self.assertRaisesRegex(StoreFailure,"uncommitted or interrupted"):
            Store("S2",self.home/"S2.sqlite",self.home,
                  create=False,source_identity=self.identity)

    def test_index_corruption_before_audit_never_publishes(self):
        s=self._build_unsealed("S2")
        s.db.execute("DELETE FROM events WHERE oid=?",(
            s.find_id(self.data["RespondentEvent"][0]["ref"]),))
        s.db.commit()
        with self.assertRaisesRegex(StoreFailure,"event index lost"):
            s.audit_families()
        self.assertEqual(s.get_meta("state"),"AUDIT_PENDING")
        s.close()

    def test_wrong_source_reopen_refuses(self):
        s=self.build("S2");s.close()
        with self.assertRaisesRegex(StoreFailure,"another exact source"):
            Store("S2",self.home/"S2.sqlite",self.home,create=False,
                  source_identity={"another":True})

    def test_sqlite_stays_queryable_after_reopen(self):
        s=self.build("S3");s.close()
        reopened=Store("S3",self.home/"S3.sqlite",self.home,
                       create=False,source_identity=self.identity)
        self.assertEqual(reopened.audit_families(),self.expected)
        self.assertEqual(reopened.db.execute("SELECT COUNT(*) FROM events").fetchone()[0],6)
        reopened.close()

    def test_corrupted_body_is_detected_by_full_audit(self):
        s=self.build("S2")
        key=s.find_id(self.data["RespondentEvent"][0]["ref"])
        s.db.execute("UPDATE objects SET body=? WHERE oid=?", (b"not zlib",key))
        s.db.commit()
        self.assertEqual(s.db.execute("PRAGMA integrity_check").fetchone()[0],"ok")
        with self.assertRaises(StoreFailure):
            s.audit_families()
        s.close()

    def test_hash_collision_refuses_without_aliasing(self):
        s=self.build("S3")
        fp=hashlib.sha256(b"completely-new-ref").digest()
        original=s.find_id(self.data["RespondentEvent"][0]["ref"])
        s.db.execute("UPDATE refs SET fp=? WHERE id=?", (fp,original))
        s.db.commit()
        with self.assertRaisesRegex(StoreFailure,"fingerprint collision"):
            s.intern("completely-new-ref")
        s.close()

    def test_indexed_union_matches_legacy_or_for_alias_overlap_states_and_order(self):
        s=self.build("S3")
        respondent=s.find_id(self.respondents[0])
        target=s.find_id(self.qs[0])
        events=list(s.db.execute(
            "SELECT oid FROM events WHERE rid=? ORDER BY oid",(respondent,)
        ))
        self.assertEqual(len(events),3)
        s.db.execute(
            "UPDATE events SET canonical=?,state=? WHERE oid=?",
            (target,"OBSERVED",events[0]["oid"]),
        )
        s.db.execute(
            "UPDATE events SET canonical=?,component=?,state=? WHERE oid=?",
            (target,target,"MISSING",events[1]["oid"]),
        )
        s.db.execute(
            "UPDATE events SET component=?,state=? WHERE oid=?",
            (target,"REFUSAL",events[2]["oid"]),
        )
        s.db.commit()

        def legacy(include_component,native_only,states):
            rid=s.find_id(self.respondents[0])
            tid=s.find_id(self.qs[0])
            if native_only:
                where,params="native=?",[tid]
            elif include_component:
                where,params="(native=? OR canonical=? OR component=?)",[tid]*3
            else:
                where,params="(native=? OR canonical=?)",[tid]*2
            sql=f"SELECT oid FROM events WHERE rid=? AND {where}"
            args=[rid]+params
            if states is not None:
                sql+=" AND state IN ("+",".join("?" for _ in states)+")"
                args.extend(sorted(states))
            keys=[r["oid"] for r in s.db.execute(sql,args)]
            return [s.fetch_body(oid) for oid in sorted(keys,key=s.exact_ref)]

        cases=[
            (True,False,None),(True,False,frozenset({"OBSERVED"})),
            (True,False,frozenset({"OBSERVED","REFUSAL"})),
            (True,False,frozenset()),(False,False,None),
            (False,True,None),(False,True,frozenset({"MISSING"})),
        ]
        for include_component,native_only,states in cases:
            with self.subTest(include_component=include_component,
                              native_only=native_only,states=states):
                actual=list(s.select_events(
                    respondent=self.respondents[0],target=self.qs[0],
                    native_only=native_only,include_component=include_component,
                    states=states,
                ))
                self.assertEqual(actual,legacy(include_component,native_only,states))
        self.assertEqual(list(s.select_events(
            respondent=self.respondents[0],target="missing|target")),[])
        self.assertEqual(list(s.select_events(
            respondent="missing|respondent",target=self.qs[0])),[])
        s.close()

    def test_reference_cache_eviction_and_reopen_preserve_identity(self):
        s=self.build("S3")
        ref=self.data["RespondentEvent"][0]["ref"]
        idx=s.find_id(ref)
        self.assertEqual(s.exact_ref(idx),ref)
        s._ref_cache.clear()
        s._exact_cache.clear()
        for i in range(30000):
            s._ref_cache[f"uncached-{i}"]=i
            s._exact_cache[i]=f"uncached-{i}"
        self.assertEqual(s.find_id(ref),idx)
        self.assertEqual(s.exact_ref(idx),ref)
        self.assertLessEqual(len(s._ref_cache),30000)
        self.assertLessEqual(len(s._exact_cache),30000)
        s.close()
        reopened=Store("S3",self.home/"S3.sqlite",self.home,
                       create=False,source_identity=self.identity)
        self.assertEqual(reopened.find_id(ref),idx)
        self.assertEqual(reopened.exact_ref(idx),ref)
        reopened.close()

    def test_original_canonical_ref_round_trip(self):
        for arm in ARMS:
            with self.subTest(arm=arm):
                s=self.build(arm)
                for event in self.data["RespondentEvent"]:
                    idx=s.find_id(event["ref"])
                    ref,body=s.fetch_body(idx)
                    self.assertEqual(ref,event["ref"])
                    self.assertEqual(body,event["body_json"])
                s.close()

if __name__=="__main__":
    unittest.main()
