"""Exact R8 sourcefree mechanism tests (pure module, runnable without repo checkout)."""
from types import SimpleNamespace
import unittest
from copy import deepcopy
from um_sorok_organism.preproject_agency import (
    admit_preproject_anticipation, revise_preproject_anticipation,
    recruit_preproject_anticipations, fallback_nonproject_orientation,
)


def exp(actor='nadia', ref='x1', cues=None):
    return {'actor': actor, 'ref': ref, 'participated': True,
            'perceived_cues': cues if cues is not None else
            [{'id':'s1','tags':['soft_voice','approach'], 'modality':'auditory'}]}


def cand(**kw):
    return {'perceived_cue_ref':'s1','possible_operation':'SIGNAL',
            'orientation_mode':'APPROACH',**kw}


def situated(actor):
    return SimpleNamespace(actor=actor['id'], expectations=deepcopy(actor['expectations']))


def access(tags):
    return SimpleNamespace(actor='nadia', cues=[{'id':'s2','tags':tags}])


class PreprojectAgencyTests(unittest.TestCase):
    def setUp(self):
        self.actor={'id':'nadia', 'expectations':[], 'projects':[], 'body':{'language':0.0}}

    def acquired(self, event='e1', **kw):
        return admit_preproject_anticipation(self.actor, exp(), event, cand(**kw))

    def test_preverbal_acquisition_does_not_mint_project_or_proposition(self):
        receipt=self.acquired()
        self.assertTrue(receipt['not_a_motive'])
        self.assertEqual(self.actor['projects'],[])
        a=self.actor['expectations'][0]
        self.assertIsNone(a['project_id'])
        self.assertEqual(a['conceptual_access'],'NONDECLARATIVE_NOT_ACTOR_PROPOSITION')
        self.assertEqual(a['world_consequence'],'NOT_INFERRED')

    def test_unseen_sign_cannot_be_acquired(self):
        with self.assertRaisesRegex(ValueError,'UNEXPERIENCED'):
            self.acquired(perceived_cue_ref='invented')
        self.assertEqual(self.actor['expectations'],[])

    def test_does_not_mint_new_action(self):
        with self.assertRaisesRegex(ValueError,'UNLICENSED'):
            self.acquired(possible_operation='EDIT_THE_INSTITUTION')

    def test_cue_specific_recruitment_affects_future_possible_action(self):
        self.acquired()
        options=[{'action':'WAIT','basis':[]}, {'action':'SIGNAL','basis':[]}]
        result=recruit_preproject_anticipations(situated(self.actor),access(['soft_voice']),options)
        self.assertEqual(result['distinct_historical_ground_count'],1)
        self.assertEqual(options[1]['preproject_recruitment']['status'],'ACQUIRED_NONPROJECT_APPROACH')
        self.assertEqual(fallback_nonproject_orientation(options)['action'],'SIGNAL')
        self.assertIsNone(fallback_nonproject_orientation(options)['project_id'])

    def test_unseen_current_context_cannot_recruit(self):
        self.acquired()
        options=[{'action':'SIGNAL','basis':[]}]
        self.assertFalse(recruit_preproject_anticipations(situated(self.actor),access(['machine_hum']),options)['currents'])
        self.assertIsNone(fallback_nonproject_orientation(options))

    def test_mature_project_prevents_heuristic_preproject_override(self):
        self.acquired()
        options=[{'action':'WORK','project_courses':[{'project_id':'w'}]},
                 {'action':'SIGNAL','basis':[]}]
        recruit_preproject_anticipations(situated(self.actor),access(['soft_voice']),options)
        self.assertIsNone(fallback_nonproject_orientation(options))

    def test_dupe_descriptions_same_historical_ground_do_not_create_two_drives(self):
        self.acquired()
        x=deepcopy(self.actor['expectations'][0]); x['id']='other_description';self.actor['expectations'].append(x)
        options=[{'action':'SIGNAL','basis':[]}]
        p=recruit_preproject_anticipations(situated(self.actor),access(['soft_voice']),options)
        self.assertEqual(p['distinct_historical_ground_count'],1)
        self.assertTrue(p['currents'][0]['multiple_descriptions_not_multiple_drives'])
        self.assertEqual(options[0]['preproject_recruitment']['source_count_distinct'],1)

    def test_two_different_historical_events_stay_distinct_without_sum(self):
        self.acquired()
        self.acquired(event='e2')
        options=[{'action':'SIGNAL','basis':[]}]
        p=recruit_preproject_anticipations(situated(self.actor),access(['soft_voice']),options)
        self.assertEqual(p['distinct_historical_ground_count'],2)
        self.assertEqual(options[0]['preproject_recruitment']['source_count_distinct'],2)
        self.assertNotIn('intensity',options[0]['preproject_recruitment'])

    def test_opposed_histories_survive_as_conflict_and_no_fallback_choice(self):
        self.acquired()
        self.acquired(event='e2',orientation_mode='WITHHOLD')
        options=[{'action':'SIGNAL','basis':[]}]
        recruit_preproject_anticipations(situated(self.actor),access(['soft_voice']),options)
        self.assertEqual(options[0]['preproject_recruitment']['status'],
                         'UNRESOLVED_PREPROJECT_CONTRADICTION')
        self.assertIsNone(fallback_nonproject_orientation(options))

    def test_world_action_not_necessary_for_orientation(self):
        source=exp()
        source['participated']=False
        self.assertTrue(admit_preproject_anticipation(self.actor,source,'e1',cand()))

    def test_later_fallible_revaluation_recruits_differently(self):
        self.acquired()
        iden=self.actor['expectations'][0]['id']
        received=exp(ref='x2')
        receipt=revise_preproject_anticipation(self.actor,received,'e2',{
            'expectation_ref':iden,'perceived_cue_ref':'s1','orientation_mode':'WITHHOLD'})
        self.assertEqual(receipt['new_mode'],'WITHHOLD')
        self.assertEqual(self.actor['expectations'][0]['revisions'][0]['prior_mode'],'APPROACH')
        opts=[{'action':'SIGNAL','basis':[]}]
        recruit_preproject_anticipations(situated(self.actor),access(['soft_voice']),opts)
        self.assertEqual(opts[0]['preproject_recruitment']['status'],'ACQUIRED_NONPROJECT_WITHHOLD')

    def test_unknown_later_sign_cannot_rewrite_history(self):
        self.acquired()
        prior=deepcopy(self.actor)
        with self.assertRaisesRegex(ValueError,'UNSEEN'):
            revise_preproject_anticipation(self.actor,exp(ref='x2'),'e2',{
                'expectation_ref':self.actor['expectations'][0]['id'],
                'perceived_cue_ref':'never','orientation_mode':'WITHHOLD'})
        self.assertEqual(self.actor,prior)

    def test_no_same_event_retroactive_story(self):
        self.acquired()
        with self.assertRaisesRegex(ValueError,'RETROACTIVE'):
            revise_preproject_anticipation(self.actor,exp(),'e1',{
                'expectation_ref':self.actor['expectations'][0]['id'],
                'perceived_cue_ref':'s1','orientation_mode':'WITHHOLD'})

    def test_owner_actor_mismatch_refused(self):
        with self.assertRaisesRegex(ValueError,'IDENTITY'):
            admit_preproject_anticipation(self.actor,exp(actor='father'),'e1',cand())

    def test_llm_cannot_invent_independent_historical_roots(self):
        self.acquired(historical_ground_ref='invented_private_person')
        self.assertEqual(self.actor['expectations'][0]['historical_ground_ref'],'e1')

if __name__=='__main__':unittest.main()