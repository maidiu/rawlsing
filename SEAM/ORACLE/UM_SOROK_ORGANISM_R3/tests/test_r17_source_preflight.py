"""R17: full source/chain preflight for source reads and appends."""
import json
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.storage import ResearchLedger, Conflict
from um_sorok_organism.types import adult, blank_world, canonical, digest


def ledger_with_source_and_later_event(path):
    ledger = ResearchLedger(str(path))
    ledger.initialize(blank_world(), [adult('amy', 'Amy')],
                      source_seals=[('seed', 'CONDITIONING_NOT_REAL_PERSON', {'truth': 'A'})])
    version, world = ledger.world()
    ledger.commit('w1', version, world, {}, {}, 'OBJECTIVE_CUE', None,
                  {'event': 'unaltered additional history'})
    assert ledger.verify_chain()['valid']
    return ledger


def rewrite_initial_seal_map_and_sealed_row(ledger):
    replacement = {'truth': 'B'}
    category = 'CONDITIONING_NOT_REAL_PERSON'
    sha = digest({'category': category, 'content': replacement})
    ledger.conn.execute('UPDATE source_seals SET content=? WHERE id=?',
                        (canonical(replacement), 'seed'))
    old = ledger.conn.execute('SELECT payload FROM events WHERE seq=1').fetchone()[0]
    env = json.loads(old)
    env['source_seal_digests']['seed'] = sha
    ledger.conn.execute('UPDATE events SET payload=? WHERE seq=1', (canonical(env),))
    with unittest.TestCase().assertRaises(AssertionError):
        ledger.verify_chain()


def inject_unauthorized_source_anchor_in_regular_event(ledger):
    last = ledger.events()[-1]
    assert last['kind'] == 'OBJECTIVE_CUE'
    env = dict(last['envelope'])
    env['source_seal_digests'] = {'ghost-source': 'fictional-digest'}
    eid = 'evt_' + digest({'prev': last['previous_hash'], 'envelope': env})[:20]
    chain = digest({'previous': last['previous_hash'], 'eid': eid, 'envelope': env})
    ledger.conn.execute('UPDATE events SET eid=?,payload=?,chain_hash=? WHERE seq=2',
                        (eid, canonical(env), chain))
    with unittest.TestCase().assertRaisesRegex(AssertionError, 'SOURCE_SEAL_EVENT_UNAUTHORIZED_ANCHOR'):
        ledger.verify_chain()


class R17SourceCustodyPreflightHostile(unittest.TestCase):
    def test_modified_historical_source_anchor_must_refuse_source_read(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = ledger_with_source_and_later_event(Path(d)/'research.sqlite')
            try:
                rewrite_initial_seal_map_and_sealed_row(ledger)
                with self.assertRaises(Conflict):
                    ledger.source('seed')
            finally:
                ledger.close()

    def test_modified_historical_source_anchor_must_refuse_append(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = ledger_with_source_and_later_event(Path(d)/'research.sqlite')
            try:
                rewrite_initial_seal_map_and_sealed_row(ledger)
                version, world = ledger.world()
                before = len(ledger.events())
                with self.assertRaises(Conflict):
                    ledger.commit('w1', version, world, {}, {}, 'OBJECTIVE_CUE', None,
                                  {'event': 'append after compromised genesis'})
                self.assertEqual(len(ledger.events()), before)
            finally:
                ledger.close()

    def test_source_read_refuses_unauthorized_seal_map_on_regular_event(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = ledger_with_source_and_later_event(Path(d)/'research.sqlite')
            try:
                inject_unauthorized_source_anchor_in_regular_event(ledger)
                with self.assertRaises(Conflict):
                    ledger.source('seed')
            finally:
                ledger.close()

    def test_append_refuses_unauthorized_seal_map_on_regular_event(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = ledger_with_source_and_later_event(Path(d)/'research.sqlite')
            try:
                inject_unauthorized_source_anchor_in_regular_event(ledger)
                version, world = ledger.world()
                before = len(ledger.events())
                with self.assertRaises(Conflict):
                    ledger.commit('w1', version, world, {}, {}, 'OBJECTIVE_CUE', None,
                                  {'event': 'append after illegal source map'})
                self.assertEqual(len(ledger.events()), before)
            finally:
                ledger.close()

    def test_noncanonical_source_seal_event_must_refuse_source_read(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = ledger_with_source_and_later_event(Path(d)/'research.sqlite')
            try:
                ledger.seal_source('later', 'TEST', {'new': 'sealed'})
                raw = ledger.conn.execute("SELECT payload FROM events WHERE kind='SOURCE_SEAL'").fetchone()[0]
                ledger.conn.execute("UPDATE events SET payload=? WHERE kind='SOURCE_SEAL'", (raw+' ',))
                with self.assertRaisesRegex(AssertionError, 'EVENT_ENVELOPE_NONCANONICAL_BYTES'):
                    ledger.verify_chain()
                with self.assertRaises(Conflict):
                    ledger.source('later')
            finally:
                ledger.close()

    def test_noncanonical_initialization_payload_must_refuse_source_read(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = ledger_with_source_and_later_event(Path(d)/'research.sqlite')
            try:
                raw = ledger.conn.execute('SELECT payload FROM events WHERE seq=1').fetchone()[0]
                ledger.conn.execute('UPDATE events SET payload=? WHERE seq=1', (raw+' ',))
                with self.assertRaises(AssertionError):
                    ledger.verify_chain()
                with self.assertRaises(Conflict):
                    ledger.source('seed')
            finally:
                ledger.close()

    def test_noncanonical_ordinary_payload_must_refuse_source_read(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = ledger_with_source_and_later_event(Path(d)/'research.sqlite')
            try:
                raw = ledger.conn.execute("SELECT payload FROM events WHERE kind='OBJECTIVE_CUE'").fetchone()[0]
                ledger.conn.execute("UPDATE events SET payload=? WHERE kind='OBJECTIVE_CUE'", (raw+' ',))
                with self.assertRaises(AssertionError):
                    ledger.verify_chain()
                with self.assertRaises(Conflict):
                    ledger.source('seed')
            finally:
                ledger.close()

    def test_malformed_event_envelope_is_typed_conflict(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = ledger_with_source_and_later_event(Path(d)/'research.sqlite')
            try:
                ledger.conn.execute("UPDATE events SET payload='{}' WHERE seq=1")
                with self.assertRaises(AssertionError):
                    ledger.verify_chain()
                with self.assertRaisesRegex(Conflict, 'SOURCE_HISTORY_INVALID'):
                    ledger.source('seed')
                version, world = ledger.world()
                with self.assertRaisesRegex(Conflict, 'SOURCE_HISTORY_INVALID'):
                    ledger.commit('w1', version, world, {}, {}, 'OBJECTIVE_CUE', None,
                                  {'event': 'must not append'})
                with self.assertRaisesRegex(Conflict, 'SOURCE_HISTORY_INVALID'):
                    ledger.seal_source('late', 'TEST', {'new': 'sealed'})
                self.assertEqual(len(ledger.events()), 2)
            finally:
                ledger.close()

    def test_valid_source_read_and_append_still_work(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = ledger_with_source_and_later_event(Path(d)/'research.sqlite')
            try:
                self.assertEqual(ledger.source('seed')['content'], {'truth': 'A'})
                version, world = ledger.world()
                receipt = ledger.commit('w1', version, world, {}, {}, 'OBJECTIVE_CUE', None,
                                        {'event': 'valid continuation'})
                self.assertEqual(receipt['envelope']['kind'], 'OBJECTIVE_CUE')
                self.assertTrue(ledger.verify_chain()['valid'])
            finally:
                ledger.close()


if __name__ == '__main__':
    unittest.main()
