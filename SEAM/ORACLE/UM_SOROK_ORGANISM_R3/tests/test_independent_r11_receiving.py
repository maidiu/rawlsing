"""Independent R11 receiving: exact first-fault negatives and positive boundaries.
These are reviewer-authored (not in the author's 232-test suite).
"""
import tempfile
import unittest
from pathlib import Path
from um_sorok_organism.storage import ResearchLedger
from um_sorok_organism.types import blank_world, adult, canonical
from um_sorok_organism.constitution import actor_access
from um_sorok_organism.world import add_cue
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService
from um_sorok_organism.development import InvalidDevelopment

class R10Continuity(unittest.TestCase):
    def test_p070_uncommitted_second_world_cannot_verify(self):
        with tempfile.TemporaryDirectory() as d:
            l=ResearchLedger(str(Path(d)/'x.sqlite'))
            try:
                l.initialize(blank_world(),[adult('ann','Ann')])
                l.conn.execute('INSERT INTO worlds(id,version,body) VALUES (?,?,?)',
                     ('w2',0,canonical(blank_world('w2'))))
                with self.assertRaisesRegex(AssertionError,'UNCOMMITTED_WORLD_ROSTER'):
                    l.verify_chain()
            finally:l.close()

    def test_p070_uncommitted_noncanonical_actor_world_snapshot_bytes_rejected(self):
        for table in ('worlds','actors'):
            with self.subTest(table=table),tempfile.TemporaryDirectory() as d:
                l=ResearchLedger(str(Path(d)/'x.sqlite'))
                try:
                    l.initialize(blank_world(),[adult('ann','Ann')])
                    row=l.conn.execute('SELECT body FROM '+table+' LIMIT 1').fetchone()[0]
                    l.conn.execute('UPDATE '+table+' SET body=?',(' '+row,))
                    with self.assertRaisesRegex(AssertionError,'NONCANONICAL|CHANGED'):
                        l.verify_chain()
                finally:l.close()

    def test_p071_malformed_actor_sensor_not_a_perceptual_license(self):
        w=blank_world();w['clock']=1;w['positions']={'ann':'home'}
        c=add_cue(w,'distant_bell',['bell'],location='home',threshold=.95)
        a=adult('ann','Ann');a['body']['sensor']=float('nan')
        with self.assertRaisesRegex(ValueError,'INVALID_BODY_STATE:sensor'):
            actor_access(a,w)

class TrialAuthority(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.rt=ConstitutiveRuntime(str(Path(self.t.name)/'life.sqlite'))
        self.addCleanup(self.rt.close)
        self.rt.initialize();self.rt.background(280)
        self.rt.step('nadia',requested_action='SING')
        self.end=self.rt.snapshot('nadia')['possible_ends'][0]
        self.assertEqual(self.end['status'],'POSSIBLE_NOT_ACQUIRED_MOTIVE')

    def test_malicious_provider_claims_foreign_trial_history_at_development(self):
        def f(task,packet):
            if task=='actor_attempt':
                trial=next(t for t in packet['possible_end_trials'] if t['operation']=='SING')
                return {'task':task,'possible_end_trial_id':trial['trial_id']}
            if task=='development':
                return {'task':task,'candidates':[{'kind':'RECORD_POSSIBLE_END_TRIAL',
                    'trial':{'actor':'not_nadia','possible_end_ref':self.end['id'],'operation':'SING'}}]}
            return {'task':task,'surface':'ok'}
        self.rt.semantic=ValidatingSemanticService(CallbackLLMProvider(f))
        before=self.rt.ledger.world()[1]['clock']
        with self.assertRaises(InvalidDevelopment):self.rt.step('nadia')
        self.assertEqual(self.rt.ledger.world()[1]['clock'],before)
        self.assertFalse(self.rt.snapshot('nadia')['possible_ends'][0].get('trial_history'))

    def test_malicious_model_relabels_current_trial_via_new_project(self):
        # Distinct from TAKE_UP guard; the general-purpose ADD_PROJECT route
        # must not claim the current just-executed trial was an acquired motive.
        def f(task,packet):
            if task=='actor_attempt':
                t=next(t for t in packet['possible_end_trials'] if t['operation']=='SING')
                return {'task':task,'possible_end_trial_id':t['trial_id']}
            if task=='development':
                return {'task':task,'candidates':[{'kind':'ADD_PROJECT','project':{
                    'object':self.end['possible_object'], 'means':['SING'],
                    'motive':'MATURE_RHYTHM_MOTIVE_FROM_TRIAL','priority':.8,
                    'cue_terms':['sing']}}]}
            return {'task':task,'surface':'ok'}
        self.rt.semantic=ValidatingSemanticService(CallbackLLMProvider(f))
        before=self.rt.ledger.world()[1]['clock']
        # A correct bounded trial issuer should reject this in the same event
        # or leave the attempted operation unclassified as durable motive.
        try:
            self.rt.step('nadia')
        except (InvalidDevelopment,ValueError):return
        projects=self.rt.snapshot('nadia')['projects']
        self.assertFalse(any(p.get('motive')=='MATURE_RHYTHM_MOTIVE_FROM_TRIAL' for p in projects),
            'CURRENT_TRIAL_MOTIVE_CAN_BE_MINTED_VIA_ADD_PROJECT: '+repr(projects))
        self.assertEqual(self.rt.ledger.world()[1]['clock'],before+1)

    def test_valid_selected_trial_retains_actor_history_and_world_chain(self):
        def f(task,packet):
            if task=='actor_attempt':
                trial=next(t for t in packet['possible_end_trials'] if t['operation']=='SING')
                return {'task':task,'possible_end_trial_id':trial['trial_id']}
            if task=='development':return {'task':task,'candidates':[]}
            return {'task':task,'surface':'public only'}
        self.rt.semantic=ValidatingSemanticService(CallbackLLMProvider(f))
        self.rt.step('nadia')
        end=self.rt.snapshot('nadia')['possible_ends'][0]
        self.assertEqual(end['status'],'POSSIBLE_NOT_ACQUIRED_MOTIVE')
        self.assertEqual(len(end['trial_history']),1)
        self.assertTrue(self.rt.verify()['valid'])

if __name__=='__main__':unittest.main()
