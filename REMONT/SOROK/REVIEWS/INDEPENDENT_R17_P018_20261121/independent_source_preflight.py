"""Independent R17 P018 receiving. Sourcefree SQLite fault injections.
Not part of the R17 author 289-test suite.
"""
import tempfile
import json
import unittest
from pathlib import Path

from um_sorok_organism.storage import ResearchLedger, Conflict
from um_sorok_organism.types import adult, blank_world, canonical, digest


def clean(path):
    ledger = ResearchLedger(str(path))
    ledger.initialize(blank_world(), [adult('amy', 'Amy')],
                      source_seals=[('seed', 'CONDITIONING_NOT_REAL_PERSON', {'truth':'A'})])
    version, world = ledger.world()
    ledger.commit('w1', version, world, {}, {}, 'OBJECTIVE_CUE', None, {'event':'original'})
    assert ledger.verify_chain()['valid']
    return ledger


def assert_no_operational_ingress(test,ledger):
    before_events=list(ledger.events())
    before_world=ledger.world()
    with test.assertRaisesRegex(Conflict, 'SOURCE_HISTORY_INVALID|UNCOMMITTED|MISSING_LEDGER_GENESIS'):
        ledger.source('seed')
    with test.assertRaisesRegex(Conflict, 'SOURCE_HISTORY_INVALID|UNCOMMITTED|MISSING_LEDGER_GENESIS'):
        ledger.source('unknown')
    with test.assertRaisesRegex(Conflict, 'SOURCE_HISTORY_INVALID|UNCOMMITTED|MISSING_LEDGER_GENESIS'):
        ledger.commit('w1',before_world[0],before_world[1],{}, {},'OBJECTIVE_CUE',None,{'test':'bad append'})
    with test.assertRaisesRegex(Conflict, 'SOURCE_HISTORY_INVALID|UNCOMMITTED|MISSING_LEDGER_GENESIS'):
        ledger.seal_source('later','TEST',{'new':True})
    test.assertEqual(ledger.events(),before_events)
    test.assertEqual(ledger.world(),before_world)
    test.assertIsNone(ledger.conn.execute('SELECT 1 FROM source_seals WHERE id=?',('later',)).fetchone())


class R17IndependentSourcePreflight(unittest.TestCase):
    def test_canonical_equivalent_source_bytes_altered_blocks_all_ingresses(self):
        with tempfile.TemporaryDirectory() as d:
            l=clean(Path(d)/'x.db')
            try:
                raw=l.conn.execute('SELECT content FROM source_seals WHERE id=?',('seed',)).fetchone()[0]
                l.conn.execute('UPDATE source_seals SET content=? WHERE id=?',(' '+raw,'seed'))
                assert_no_operational_ingress(self,l)
            finally:l.close()

    def test_unauthorized_extra_source_row_blocks_all_ingresses(self):
        with tempfile.TemporaryDirectory() as d:
            l=clean(Path(d)/'x.db')
            try:
                l.conn.execute('INSERT INTO source_seals(id,type,content) VALUES(?,?,?)',('unanchored','TEST',canonical({'a':3})))
                assert_no_operational_ingress(self,l)
            finally:l.close()

    def test_recomputed_last_event_hash_does_not_authorize_source_map(self):
        with tempfile.TemporaryDirectory() as d:
            l=clean(Path(d)/'x.db')
            try:
                row=l.events()[-1]
                env=dict(row['envelope'])
                env['source_seal_digests']={'fake':'123456'}
                eid='evt_'+digest({'prev':row['previous_hash'],'envelope':env})[:20]
                chain=digest({'previous':row['previous_hash'],'eid':eid,'envelope':env})
                l.conn.execute('UPDATE events SET eid=?,payload=?,chain_hash=? WHERE kind=?',(eid,canonical(env),chain,'OBJECTIVE_CUE'))
                assert_no_operational_ingress(self,l)
            finally:l.close()

    def test_altered_history_event_header_blocks_reads_and_append(self):
        with tempfile.TemporaryDirectory() as d:
            l=clean(Path(d)/'x.db')
            try:
                l.conn.execute('UPDATE events SET clock=clock+123 WHERE kind=?',('OBJECTIVE_CUE',))
                assert_no_operational_ingress(self,l)
            finally:l.close()

    def test_malformed_json_historical_event_returns_typed_conflict(self):
        with tempfile.TemporaryDirectory() as d:
            l=clean(Path(d)/'x.db')
            try:
                l.conn.execute("UPDATE events SET payload=? WHERE kind=?", ('not valid json {','OBJECTIVE_CUE'))
                v,w=l.world()
                with self.assertRaisesRegex(Conflict,'SOURCE_HISTORY_INVALID'):
                    l.source('seed')
                with self.assertRaisesRegex(Conflict,'SOURCE_HISTORY_INVALID'):
                    l.commit('w1',v,w,{}, {},'OBJECTIVE_CUE',None,{'event':'should not append'})
                with self.assertRaisesRegex(Conflict,'SOURCE_HISTORY_INVALID'):
                    l.seal_source('later','TEST',{'hello':1})
                self.assertEqual(l.conn.execute('SELECT COUNT(*) FROM events').fetchone()[0],2)
                self.assertIsNone(l.conn.execute("SELECT 1 FROM source_seals WHERE id='later'").fetchone())
            finally:l.close()

    def test_extra_unanchored_constraints_state_blocks_ingresses(self):
        with tempfile.TemporaryDirectory() as d:
            l=clean(Path(d)/'x.db')
            try:
                # Discover actual constraints table schema, respecting the domain contract.
                cols=[r[1] for r in l.conn.execute('PRAGMA table_info(constraints)').fetchall()]
                values=['x' if 'id' in c else 'bogus' for c in cols]
                l.conn.execute('INSERT INTO constraints VALUES('+','.join('?' for _ in cols)+')', values)
                assert_no_operational_ingress(self,l)
            finally:l.close()

    def test_canonical_snapshot_ghost_world_refuses_every_operation(self):
        with tempfile.TemporaryDirectory() as d:
            l=clean(Path(d)/'x.db')
            try:
                l.conn.execute('INSERT INTO worlds VALUES(?,?,?)',('w2',0,canonical(blank_world('w2'))))
                assert_no_operational_ingress(self,l)
            finally:l.close()

    def test_valid_late_source_seal_then_append_and_reopen(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.db'
            l=clean(p)
            try:
                l.seal_source('later','TEST',{'memory':'public'})
                v,w=l.world()
                e=l.commit('w1',v,w,{}, {},'OBJECTIVE_CUE',None,{'event':'after late source'})
                self.assertIsNotNone(e['id'])
                self.assertEqual(l.source('seed')['content'],{'truth':'A'})
                self.assertEqual(l.source('later')['content'],{'memory':'public'})
                self.assertTrue(l.verify_chain()['valid'])
            finally:l.close()
            l2=ResearchLedger(str(p))
            try:
                self.assertTrue(l2.verify_chain()['valid'])
                self.assertEqual(l2.source('later')['content'],{'memory':'public'})
            finally:l2.close()

if __name__=='__main__':unittest.main()
