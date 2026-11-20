"""Independent R15 P012/P018 hostile sourcefree receiving cases.

These are not author-side reproduction tests.  They exercise the actual ledger
and actor constitution at the exact frozen R15 source cut.
"""
import itertools
import json
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.storage import ResearchLedger, Conflict
from um_sorok_organism.types import adult, blank_world, canonical, digest
from um_sorok_organism.world import add_cue
from um_sorok_organism.constitution import actor_access, materialize, compose


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
    # Canonical envelope updated, but NOT the historical chain/eid: provenance
    # breaks, as the full auditor correctly detects.
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
    # The event hash is internally valid; the source issuer is not.
    with unittest.TestCase().assertRaisesRegex(AssertionError, 'SOURCE_SEAL_EVENT_UNAUTHORIZED_ANCHOR'):
        ledger.verify_chain()


class R15SourceCustodyPreflightHostile(unittest.TestCase):
    def test_modified_historical_source_anchor_must_refuse_source_read(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = ledger_with_source_and_later_event(Path(d)/'research.sqlite')
            try:
                rewrite_initial_seal_map_and_sealed_row(ledger)
                with self.assertRaises(Conflict, msg='P018 must not return tampered source'):
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
                with self.assertRaises(Conflict, msg='P018 must not append to invalid historical source anchor'):
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
                with self.assertRaisesRegex(AssertionError,'EVENT_ENVELOPE_NONCANONICAL_BYTES'):
                    ledger.verify_chain()
                with self.assertRaises(Conflict):
                    ledger.source('later')
            finally:
                ledger.close()


class R15InhibitionAcyclicOracle(unittest.TestCase):
    def test_all_64_four_form_acyclic_inhibition_graphs(self):
        ids = ['a', 'b', 'c', 'd']
        pairs = list(itertools.combinations(ids, 2))
        actor = adult('amy', 'Amy')
        actor['forms'] = {
            name: {'id': name, 'actor': 'amy', 'kind': 'PRACTICE',
                   'origin': ['historical_'+name], 'cues': ['encounter'],
                   'enables': ['SING'], 'strength': .6, 'body_min': 0,
                   'lifecycle': 'ACTIVE', 'scope': {}}
            for name in ids}
        world = blank_world()
        world['positions'] = {'amy': 'home'}
        add_cue(world, 'bell', ['encounter'], location='home')
        access = actor_access(actor, world)
        for mask in range(1 << len(pairs)):
            edges = {a: set() for a in ids}
            actor['links'] = []
            for i, (src, dst) in enumerate(pairs):
                if mask & (1 << i):
                    edges[src].add(dst)
                    actor['links'].append({'source': src, 'target': dst, 'relation': 'INHIBITS', 'contexts': []})
            expected = set()
            for name in ids:
                if not any(name in edges[survivor] for survivor in expected):
                    expected.add(name)
            composed = compose(materialize(actor, world), access)
            result = {f['id'] for f in composed.recruited}
            with self.subTest(graph=mask):
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
