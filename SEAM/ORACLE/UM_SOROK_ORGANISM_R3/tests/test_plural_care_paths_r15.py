"""R15 sourcefree negative-control and joined-life regression candidates.

Execute at exact GitHub author HEAD. Imported source modules, not assertions
about real attachment laws or original respondents. No PR self-certification.
"""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from um_sorok_organism.types import newborn
from um_sorok_organism.plural_care_paths import (
    conserve_lived_high_resolution_care, plural_acquisition_candidate,
    choose_one_grounded_plural_acquisition, plural_addressed_signal_choice,
    sourcequalified_reopening, propose_one_reopening, admit_reopening)
from um_sorok_organism.co_regulation_history import (
    admit_co_regulation, recruit_co_regulation, addressed_signal_alternatives)
from um_sorok_organism.runtime import ConstitutiveRuntime


PARENT={'source_ref':'r15_sourcefree_fictional_parent',
        'answers':{},'fictional_seed':{'projects':[]}}


def body(nutrition=.6,comfort=.5):
    return {'nutrition':nutrition,'comfort':comfort}


def lived_care(actor,who,clock,ref):
    experience={
        'actor':actor['id'],'clock':clock,'location':'home',
        'ref':'experience:'+ref,'participated':True,
        'own_action':'RECEIVED_CARE',
        'felt_effect':'SOMATIC_CARE_CANDIDATE',
        'perceived_cues':[{
            'id':'care_sign:'+ref,'kind':'performed_care',
            'source_actor':who}]}
    return conserve_lived_high_resolution_care(
        actor,experience,'world:'+ref,body(),body(.66,.68))


def current_experience(actor_id='nadia',clock=10,people=('mother','father')):
    return {'actor':actor_id,'clock':clock,'location':'home',
            'ref':'experience:present:'+str(clock),
            'participated':True,'own_action':'ORIENT',
            'perceived_cues':[{
                'id':'present:'+who+':'+str(clock),
                'kind':'coactor_present','source_actor':who}
                for who in people]}


class PluralCareSourcefree(unittest.TestCase):
    def setUp(self):
        self.nadia=newborn('nadia','Nadia')

    def test_two_real_caregivers_can_be_acquired_across_successive_encounters(self):
        mother=lived_care(self.nadia,'mother',1,'mother')
        father=lived_care(self.nadia,'father',2,'father')
        self.assertEqual(len(self.nadia['experienced_care_events']),2)
        self.assertEqual(self.nadia['co_regulation_orientations'],[])
        now=current_experience(clock=3)
        possible=plural_acquisition_candidate(self.nadia,now,'e3')
        self.assertEqual({x['caregiver_ref'] for x in possible},
                         {'mother','father'})
        first=choose_one_grounded_plural_acquisition(possible)
        self.assertEqual(first[0]['caregiver_ref'],'father')
        admit_co_regulation(self.nadia,now,'e3',first[0])
        second_exp=current_experience(clock=4)
        second=choose_one_grounded_plural_acquisition(
            plural_acquisition_candidate(self.nadia,second_exp,'e4'))
        self.assertEqual(second[0]['caregiver_ref'],'mother')
        admit_co_regulation(self.nadia,second_exp,'e4',second[0])
        self.assertEqual(len(self.nadia['co_regulation_orientations']),2)
        self.assertEqual(self.nadia['memories'],[])
        self.assertEqual(self.nadia['self_model'],{})
        self.assertEqual(self.nadia['other_models'],{})
        self.assertEqual({
            x['caregiver_ref'] for x in self.nadia['co_regulation_orientations']},
            {'mother','father'})

    def test_co_presence_not_care_and_current_world_cue_not_a_retrospective_source(self):
        now=current_experience(clock=2)
        self.assertEqual(plural_acquisition_candidate(self.nadia,now,'e2'),[])
        invented={'actor':'nadia','clock':1,'location':'home',
                  'ref':'counterfeit','participated':True,
                  'own_action':'RECEIVED_CARE',
                  'felt_effect':'SOMATIC_CARE_CANDIDATE',
                  'perceived_cues':[]}
        self.assertIsNone(conserve_lived_high_resolution_care(
            self.nadia,invented,'e1',body(),body(.66,.68)))
        now={'actor':'nadia','clock':2,'location':'home',
             'ref':'e2','participated':True,
             'own_action':'RECEIVED_CARE',
             'felt_effect':'SOMATIC_CARE_CANDIDATE',
             'perceived_cues':[{'id':'seen-now','kind':'performed_care',
                                'source_actor':'mother'}]}
        conserve_lived_high_resolution_care(
            self.nadia,now,'e2',body(),body(.66,.68))
        # Same event may not double as a previously acquired source.
        self.assertEqual(plural_acquisition_candidate(
            self.nadia,{**current_experience(clock=2)},'e2'),[])
        with self.assertRaisesRegex(
                ValueError,'COREGULATION_ADMISSION_FOREIGN_CARE_HISTORY'):
            admit_co_regulation(
                self.nadia,now,'e2',{
                'caregiver_ref':'father','period_refs':[],
                'lived_care_event_refs':[self.nadia[
                    'experienced_care_events'][0]['id']],
                'perceived_cue_ref':'seen-now'})

    def test_equal_aggregate_care_does_not_impose_parent_hierarchy(self):
        rows=[{'caregiver_ref':'mother','perceived_cue_ref':'cm',
                'high_resolution_care_refs':[],
                'aggregate_care_refs':['m'],
                'last_personally_lived_care_clock':None},
              {'caregiver_ref':'father','perceived_cue_ref':'cf',
                'high_resolution_care_refs':[],
                'aggregate_care_refs':['f'],
                'last_personally_lived_care_clock':None}]
        self.assertEqual(choose_one_grounded_plural_acquisition(rows),[])
        rows[0]['last_personally_lived_care_clock']=5
        rows[0]['high_resolution_care_refs']=['rm']
        rows[1]['last_personally_lived_care_clock']=5
        rows[1]['high_resolution_care_refs']=['rf']
        self.assertEqual(choose_one_grounded_plural_acquisition(rows),[])

    def test_plurally_offered_call_needs_distinct_lived_support(self):
        for i,giver in enumerate(('mother','father'),1):
            lived_care(self.nadia,giver,i,giver)
        for i,giver in enumerate(('mother','father'),3):
            experience=current_experience(clock=i,people=(giver,))
            proposal=choose_one_grounded_plural_acquisition(
                plural_acquisition_candidate(self.nadia,experience,'e'+str(i)))[0]
            admit_co_regulation(self.nadia,experience,'e'+str(i),proposal)
        view=SimpleNamespace(
            actor='nadia',clock=5,body=self.nadia['body'],
            co_regulation_orientations=self.nadia['co_regulation_orientations'],
            experienced_care_events=self.nadia['experienced_care_events'])
        access=SimpleNamespace(actor='nadia',location='home',
            cues=current_experience(clock=5)['perceived_cues'])
        alternatives=addressed_signal_alternatives(
            view,access,{'action':'SIGNAL'})
        self.assertEqual(len(alternatives),2)
        option={'action':'SIGNAL','practical_alternatives':alternatives}
        needy={'comfort':.2,'nutrition':.4,'rest':.3}
        self.assertIsNone(plural_addressed_signal_choice([option],needy))
        # A new real, personally received care incident after orientation
        # supplies a distinct later response; it is not a global moral rank.
        lived_care(self.nadia,'mother',7,'mother-again')
        view.experienced_care_events=self.nadia['experienced_care_events']
        later=addressed_signal_alternatives(view,access,{'action':'SIGNAL'})
        chosen=plural_addressed_signal_choice(
            [{'action':'SIGNAL','practical_alternatives':later}],needy)
        self.assertIsNotNone(chosen)
        matching=next(x for x in later
            if x['option_id']==chosen['practical_option_id'])
        self.assertEqual(matching['world_request']['addressed_party_ref'],'mother')
        # No universal selection when no material bodily need.
        self.assertIsNone(plural_addressed_signal_choice(
            [{'action':'SIGNAL','practical_alternatives':later}],
            {'comfort':.8,'nutrition':.8,'rest':.8}))

    def test_lived_care_can_reopen_contradicted_relation_without_forgetting(self):
        lived_care(self.nadia,'mother',1,'first')
        e=current_experience(clock=2,people=('mother',))
        p=choose_one_grounded_plural_acquisition(
            plural_acquisition_candidate(self.nadia,e,'event2'))[0]
        admit_co_regulation(self.nadia,e,'event2',p)
        relation=self.nadia['co_regulation_orientations'][0]
        relation['interpretation_phase']='UNRESOLVED_AFTER_NONRESPONSE'
        relation['response_history']=[{'id':'previous_unfinished',
            'event_ref':'old_conflict'}]
        witness=lived_care(self.nadia,'mother',4,'repair')
        new={'actor':'nadia','clock':4,'location':'home',
             'ref':'experience:repair','participated':True,
             'own_action':'RECEIVED_CARE',
             'felt_effect':'SOMATIC_CARE_CANDIDATE',
             'perceived_cues':[{'id':'care_sign:repair',
                                'kind':'performed_care',
                                'source_actor':'mother'}]}
        choices=sourcequalified_reopening(self.nadia,new,'world:repair')
        self.assertEqual(len(choices),1)
        proposal=propose_one_reopening(choices)[0]
        accepted=admit_reopening(self.nadia,new,'world:repair',proposal)
        self.assertEqual(accepted['phase'],
                         'OPEN_AFTER_LIVED_CARE_NOT_SETTLED_TRUST')
        self.assertEqual(relation['response_history'][0]['id'],
                         'previous_unfinished')
        self.assertEqual(len(relation['interpretation_history']),1)
        with self.assertRaisesRegex(ValueError,'PLURAL_CARE_REOPEN_NOT_SUSPENDED'):
            admit_reopening(self.nadia,new,'world:repair',proposal)


class PluralCareJoinedRuntime(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.runtime=ConstitutiveRuntime(str(
            Path(self.tmp.name)/'plural-cares.sqlite3'))
        self.addCleanup(self.runtime.close)
        self.runtime.initialize([
            ('mother','Mother',PARENT),('father','Father',PARENT)])

    def test_real_world_care_can_generate_two_distinct_acquired_orientations(self):
        self.runtime.step('mother',requested_action='CARE',target='nadia')
        self.runtime.step('father',requested_action='CARE',target='nadia')
        nadia=self.runtime.snapshot('nadia')
        self.assertEqual(len(nadia['experienced_care_events']),2)
        self.assertEqual(nadia['co_regulation_orientations'],[])
        self.runtime.step('nadia',requested_action='ORIENT')
        acquired=self.runtime.snapshot('nadia')
        self.assertEqual(len(acquired['co_regulation_orientations']),1)
        self.assertEqual(acquired['co_regulation_orientations'][0][
            'caregiver_ref'],'father')
        self.runtime.step('nadia',requested_action='ORIENT')
        after=self.runtime.snapshot('nadia')
        self.assertEqual(len(after['co_regulation_orientations']),2)
        self.assertEqual({x['caregiver_ref'] for x in after[
            'co_regulation_orientations']},{'mother','father'})
        self.assertEqual(after['self_model'],{})
        self.assertTrue(self.runtime.verify()['valid'])

    def test_new_real_care_differentiates_later_material_call_without_forcing_reply(self):
        self.runtime.step('mother',requested_action='CARE',target='nadia')
        self.runtime.step('father',requested_action='CARE',target='nadia')
        self.runtime.step('nadia',requested_action='ORIENT')
        self.runtime.step('nadia',requested_action='ORIENT')
        self.runtime.step('mother',requested_action='CARE',target='nadia')
        self.runtime.background(400)
        chosen=self.runtime.plan('nadia')
        self.assertEqual(chosen.action,'SIGNAL')
        self.assertEqual(chosen.target,'mother')
        self.assertEqual(chosen.practical_selection[
            'actor_has_explicit_reason'],'NOT_ESTABLISHED')
        event=self.runtime.step('nadia')
        self.assertEqual(event['attempt'],'SIGNAL')
        self.assertTrue(self.runtime.verify()['valid'])

    def test_absent_caregiver_does_not_confuse_other_independent_actors(self):
        self.runtime.step('mother',requested_action='CARE',target='nadia')
        self.runtime.step('father',requested_action='CARE',target='nadia')
        self.runtime.step('nadia',requested_action='ORIENT')
        self.runtime.step('nadia',requested_action='ORIENT')
        self.runtime.step('mother',requested_action='MOVE',
                          object_ref='workshop')
        situated=self.runtime.situated('nadia')
        for option in situated['candidate_actions']:
            for alt in option.get('practical_alternatives',[]):
                if alt.get('grounds_status')=='HISTORICALLY_ACQUIRED_CO_REGULATION':
                    self.assertNotEqual(
                        alt['world_request']['addressed_party_ref'],'mother')
        self.assertTrue(self.runtime.verify()['valid'])


if __name__=='__main__':
    unittest.main()
