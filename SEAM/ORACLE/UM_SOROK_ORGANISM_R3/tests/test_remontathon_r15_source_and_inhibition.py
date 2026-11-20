"""REMONT R15: source seal provenance and stratified inhibitor counterexamples."""
import tempfile
import unittest
from pathlib import Path
from um_sorok_organism.types import adult, blank_world, canonical, digest
from um_sorok_organism.constitution import actor_access, compose, materialize
from um_sorok_organism.world import add_cue
from um_sorok_organism.storage import ResearchLedger, Conflict


def world_and_actor():
    a = adult('amy', 'Amy')
    for name, action in [('a', 'SING'), ('b', 'WORK'), ('c', 'REPAIR')]:
        a['forms'][name] = {'id': name, 'actor': 'amy', 'kind': 'PRACTICE',
             'origin': ['event_'+name], 'cues': ['encounter'], 'enables': [action],
             'strength': 0.65, 'body_min': 0, 'lifecycle': 'ACTIVE', 'scope': {}}
    w = blank_world(); w['positions'] = {'amy': 'home'}
    add_cue(w, 'bell', ['encounter'], location='home')
    return a, w


class InhibitionTruthR15(unittest.TestCase):
    def test_suppressed_inhibitor_cannot_falsely_block_its_target_in_acyclic_court(self):
        a,w=world_and_actor()
        a['links'] = [
            {'source':'a','target':'b','relation':'INHIBITS','contexts':[]},
            {'source':'b','target':'c','relation':'INHIBITS','contexts':[]}]
        s=compose(materialize(a,w),actor_access(a,w))
        ids={f['id'] for f in s.recruited}
        self.assertEqual(ids, {'a','c'})
        self.assertEqual({x['action'] for x in s.candidate_actions}&{'SING','WORK','REPAIR'}, {'SING','REPAIR'})
        self.assertIn('b',s.inhibited)
        self.assertNotIn('c',s.inhibited)

    def test_inhibitor_chain_order_independent(self):
        a,w=world_and_actor()
        a['links'] = [
            {'source':'b','target':'c','relation':'INHIBITS','contexts':[]},
            {'source':'a','target':'b','relation':'INHIBITS','contexts':[]}]
        s=compose(materialize(a,w),actor_access(a,w))
        self.assertIn('c',{f['id'] for f in s.recruited})
        self.assertNotIn('b',{f['id'] for f in s.recruited})

    def test_mutual_inhibition_stays_conservative_not_arbitrarily_won(self):
        a,w=world_and_actor()
        a['links']=[{'source':'a','target':'b','relation':'INHIBITS','contexts':[]},
                    {'source':'b','target':'a','relation':'INHIBITS','contexts':[]}]
        s=compose(materialize(a,w),actor_access(a,w))
        ids={f['id'] for f in s.recruited}
        self.assertNotIn('a',ids); self.assertNotIn('b',ids)

    def test_inhibitor_dependent_on_vetoed_supporter_does_not_invent_action(self):
        a,w=world_and_actor()
        a['forms']['b']['cues']=['never']
        a['links']=[{'source':'a','target':'b','relation':'RECRUITS','contexts':[]},
                    {'source':'b','target':'a','relation':'INHIBITS','contexts':[]}]
        s=compose(materialize(a,w),actor_access(a,w))
        self.assertNotIn('b',{f['id'] for f in s.recruited})


class SourceSealTruthR15(unittest.TestCase):
    def ledger(self,path,seals=None):
        l=ResearchLedger(str(path));l.initialize(blank_world(),[adult('amy','Amy')],source_seals=seals)
        return l

    def test_generic_commit_cannot_forge_source_seal_event(self):
        with tempfile.TemporaryDirectory() as d:
            l=self.ledger(Path(d)/'a.sqlite')
            try:
                v,w=l.world()
                with self.assertRaisesRegex(Conflict,'RESERVED_SOURCE_EVENT_KIND'):
                    l.commit('w1',v,w,{}, {},'SOURCE_SEAL',None,
                             {'source_id':'fiction','source_digest':'no source'})
                self.assertEqual(l.verify_chain()['events'],1)
            finally:l.close()

    def test_hash_consistent_unbacked_source_event_fails_audit(self):
        with tempfile.TemporaryDirectory() as d:
            l=self.ledger(Path(d)/'a.sqlite')
            try:
                last=l.events()[-1]
                v,w=l.world(); actors=l.actors()
                envelope={'world':'w1','clock':w['clock'],'kind':'SOURCE_SEAL','actor':None,
                  'payload':{'source_id':'ghost','source_digest':'fiction'},
                  'world_digest':digest(w),'actor_digests':{aid:digest(a) for aid,a in sorted(actors.items())},
                  'source_seal_digests':{},'grade':last['envelope']['grade']}
                previous=last['chain_hash'];eid='evt_'+digest({'prev':previous,'envelope':envelope})[:20]
                ch=digest({'previous':previous,'eid':eid,'envelope':envelope})
                l.conn.execute('INSERT INTO events(eid,world_id,clock,actor_id,kind,payload,previous_hash,chain_hash) VALUES(?,?,?,?,?,?,?,?)',
                      (eid,'w1',w['clock'],None,'SOURCE_SEAL',canonical(envelope),previous,ch))
                with self.assertRaisesRegex(AssertionError,'SOURCE_SEAL_EVENT'):
                    l.verify_chain()
            finally:l.close()

    def test_auxiliary_unanchored_constraints_are_not_invisible_to_audit(self):
        with tempfile.TemporaryDirectory() as d:
            l=self.ledger(Path(d)/'a.sqlite')
            try:
                l.conn.execute("INSERT INTO constraints(id,description,status) VALUES('phantom','not sourced','ACTIVE')")
                with self.assertRaisesRegex(AssertionError,'UNANCHORED_CONSTRAINTS'):
                    l.verify_chain()
                v,w=l.world()
                with self.assertRaisesRegex(Conflict,'UNANCHORED_CONSTRAINTS'):
                    l.commit('w1',v,w,{}, {},'OBJECTIVE_CUE',None,{'test':'unanchored'})
            finally:l.close()

    def test_source_read_fails_closed_if_stored_source_bytes_changed(self):
        with tempfile.TemporaryDirectory() as d:
            l=self.ledger(Path(d)/'a.sqlite',[('seed','CONDITIONING_NOT_REAL_PERSON',{'answer':'A'})])
            try:
                self.assertEqual(l.source('seed')['content'],{'answer':'A'})
                l.conn.execute('UPDATE source_seals SET content=? WHERE id=?',
                              (canonical({'answer':'B'}),'seed'))
                with self.assertRaisesRegex(Conflict,'SOURCE_SEAL'):
                    l.source('seed')
                v,w=l.world()
                with self.assertRaisesRegex(Conflict,'SOURCE_SEAL'):
                    l.commit('w1',v,w,{}, {},'OBJECTIVE_CUE',None,{'test':'tainted'})
            finally:l.close()

    def test_invalid_initial_source_identity_fails_before_genesis(self):
        with tempfile.TemporaryDirectory() as d:
            for sid,category in [('', 'TEST'), ('ok', ''), (None, 'TEST'), ('ok', False)]:
                path=Path(d)/('case_'+str(len(str(sid)))+'_'+str(len(str(category)))+'.sqlite')
                l=ResearchLedger(str(path))
                try:
                    with self.subTest(sid=sid,category=category):
                        with self.assertRaisesRegex(Conflict,'INVALID_SOURCE_IDENTITY'):
                            l.initialize(blank_world(),[adult('amy','Amy')],
                                         source_seals=[(sid,category,{'valid':'contents'})])
                        self.assertEqual(l.conn.execute('SELECT COUNT(*) FROM worlds').fetchone()[0],0)
                        self.assertEqual(l.conn.execute('SELECT COUNT(*) FROM source_seals').fetchone()[0],0)
                finally:l.close()

    def test_invalid_late_source_identity_does_not_mutate_chain(self):
        with tempfile.TemporaryDirectory() as d:
            l=self.ledger(Path(d)/'a.sqlite')
            try:
                first=l.verify_chain()['last_hash']
                for sid,category in [('', 'TEST'), ('valid', ''), (4, 'TEST'), ('ok', True)]:
                    with self.subTest(sid=sid,category=category):
                        with self.assertRaisesRegex(Conflict,'INVALID_SOURCE_IDENTITY'):
                            l.seal_source(sid,category,{'observed':'no'})
                        self.assertEqual(l.verify_chain()['last_hash'],first)
                        self.assertEqual(l.conn.execute('SELECT COUNT(*) FROM source_seals').fetchone()[0],0)
            finally:l.close()

    def test_valid_late_seal_works_and_is_cold_verified(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'a.sqlite'
            l=self.ledger(path,[('seed','CONDITIONING_NOT_REAL_PERSON',{'answer':'A'})])
            try:
                l.seal_source('supplement','TEST_EVIDENCE',{'ref':'independent'})
                self.assertEqual(l.source('supplement')['content'],{'ref':'independent'})
                self.assertEqual(l.verify_chain()['source_seals_verified'],2)
            finally:l.close()
            cold=ResearchLedger(str(path))
            try:
                self.assertEqual(cold.source('seed')['content'],{'answer':'A'})
                self.assertEqual(cold.verify_chain()['source_seals_verified'],2)
            finally:cold.close()

if __name__=='__main__':unittest.main()
