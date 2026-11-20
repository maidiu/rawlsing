"""Fresh hostile probes authored for PR #1198 review, separate from candidate tests."""
import unittest, tempfile
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService
from um_sorok_organism.development import InvalidDevelopment
from um_sorok_organism.constitution import actor_access
from um_sorok_organism.types import adult, blank_world
from um_sorok_organism.world import add_cue

class NewTrialIssuerChallenges(unittest.TestCase):
    def setUp(self):
        self.d=tempfile.TemporaryDirectory();self.addCleanup(self.d.cleanup)
        self.path=str(Path(self.d.name)/'life.sqlite')
        self.rt=ConstitutiveRuntime(self.path);self.addCleanup(self.rt.close)
        self.rt.initialize();self.rt.background(280)
        self.rt.step('nadia',requested_action='SING')
        self.end=self.rt.snapshot('nadia')['possible_ends'][0]
        self.assertEqual(self.end['status'],'POSSIBLE_NOT_ACQUIRED_MOTIVE')

    def cb(self, dev=[], trial_handler=None):
        def callback(task,packet):
            if task=='actor_attempt':
                ticket=next(t for t in packet['possible_end_trials'] if t['operation']=='SING')
                return trial_handler(ticket) if trial_handler else {'task':task,'possible_end_trial_id':ticket['trial_id']}
            if task=='development':return {'task':task,'candidates':dev}
            return {'task':task,'surface':'observed'}
        self.rt.semantic=ValidatingSemanticService(CallbackLLMProvider(callback))

    def test_actor_qualified_ticket_cannot_be_foreign(self):
        self.cb(trial_handler=lambda t:{'task':'actor_attempt','possible_end_trial_id':t['trial_id'].replace('end_trial_', 'end_trial_fake_')})
        before=self.rt.ledger.world()[1]['clock']
        with self.assertRaisesRegex(ValueError,'UNISSUED_OR_AMBIGUOUS_POSSIBLE_END_TRIAL'):
            self.rt.step('nadia')
        self.assertEqual(self.rt.ledger.world()[1]['clock'],before)
        self.assertFalse(self.rt.snapshot('nadia')['possible_ends'][0].get('trial_history'))
        self.assertTrue(self.rt.verify()['valid'])

    def test_current_trial_add_project_with_an_unrelated_id_still_rejected(self):
        self.cb([{'kind':'ADD_PROJECT','project':{
            'id':'an_entirely_disguised_project','object':'a new kingdom',
            'motive':'ADULT_DESTINY_FROM_SINGING','means':['REST'],'priority':.1,
            'status':'dormant'}}])
        before=self.rt.ledger.world()[1]['clock']
        before_actor=self.rt.ledger.actor('nadia')[1]
        with self.assertRaisesRegex(InvalidDevelopment,'CURRENT_TRIAL_NOT_MATURE_MOTIVE'):
            self.rt.step('nadia')
        self.assertEqual(self.rt.ledger.world()[1]['clock'],before)
        self.assertEqual(self.rt.ledger.actor('nadia')[1],before_actor)
        self.assertTrue(self.rt.verify()['valid'])

    def test_atomic_notice_then_illegal_project_does_not_mint_another_possible_end(self):
        self.cb([{'kind':'NOTICE_POSSIBLE_END','possible_object':'fictive aim',
                  'possible_means':['SING'],'cue_terms':['song'], 'perceived_cue_ref':'invented'},
                 {'kind':'ADD_PROJECT','project':{'object':'mature destiny',
                 'motive':'RETROACTIVE','means':['SING']}}])
        before=self.rt.ledger.world()[1]['clock']
        before_ends=self.rt.snapshot('nadia')['possible_ends']
        with self.assertRaisesRegex(InvalidDevelopment,'CURRENT_TRIAL_NOT_MATURE_MOTIVE'):
            self.rt.step('nadia')
        self.assertEqual(self.rt.snapshot('nadia')['possible_ends'],before_ends)
        self.assertEqual(self.rt.ledger.world()[1]['clock'],before)

    def test_actual_issued_trial_can_repeat_as_distinct_actor_history_events(self):
        self.cb()
        before_roster=sorted(self.rt.ledger.actors())
        self.rt.step('nadia')
        self.rt.step('nadia')
        end=self.rt.snapshot('nadia')['possible_ends'][0]
        self.assertEqual(len(end['trial_history']),2)
        self.assertEqual(len({e['event_ref'] for e in end['trial_history']}),2)
        self.assertEqual(sorted(self.rt.ledger.actors()),before_roster)
        self.assertTrue(self.rt.verify()['valid'])
        self.rt.close()
        other=ConstitutiveRuntime(self.path)
        try:
            self.assertTrue(other.verify()['valid'])
            self.assertEqual(other.snapshot('nadia')['possible_ends'][0]['trial_history'],end['trial_history'])
        finally:other.close()

class NewEmbodimentCases(unittest.TestCase):
    def test_sensor_invalidity_never_admits_cues(self):
        w=blank_world();w['clock']=1;w['positions']={'ann':'home'}
        add_cue(w,'quiet_song',['song'],location='home',threshold=.75)
        for value in (float('nan'),float('inf'),float('-inf'),True,'1'):
            with self.subTest(value=repr(value)):
                a=adult('ann','Ann');a['body']['sensor']=value
                with self.assertRaises(ValueError):actor_access(a,w)

if __name__=='__main__':unittest.main()
