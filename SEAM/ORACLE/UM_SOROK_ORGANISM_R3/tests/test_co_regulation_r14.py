"""R14 bounded author tests: co-regulation emerges through history, not labels.

These tests are design-level and joined-runtime test specifications. A PR does
not prove they ran; independent REMONT exact HEAD execution is required.
"""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from um_sorok_organism.co_regulation_history import (
    conserve_received_period_care, possible_acquired_regulation,
    admit_co_regulation, sourcefree_co_regulation_proposal,
    recruit_co_regulation, addressed_signal_alternatives,
    choose_historically_situated_signal,
    record_lived_co_regulation_response, possible_revision_after_nonresponse,
    sourcefree_revision_proposal, admit_co_regulation_revision)
from um_sorok_organism.types import newborn
from um_sorok_organism.runtime import ConstitutiveRuntime


PARENT={'source_ref':'r14_sourcefree_fictional_parent',
        'source_grade':'SOURCEFREE_FIXTURE_NOT_A_SURVEY_RESPONDENT',
        'answers':{'R14_SOURCEFREE_ONLY':'NO_EMPIRICAL_QUESTIONNAIRE_ANSWER'},
        'fictional_seed':{'projects':[]}}


def period():
    return {'id':'period1','giver':'mother','recipient':'nadia',
            'source_ref':'scoped-source1','site':'home',
            'start_clock':0,'end_clock':20,
            'modeled_labor_hours':65,
            'recipient_comfort_effect_model':.045,
            'grade':'SOURCEFREE_QUALIFIED_AGGREGATE_CARE'}


def current_cue():
    return {'id':'presence:mother:21','kind':'coactor_present',
            'source_actor':'mother','modality':'present'}


def experience():
    return {'actor':'nadia','clock':21,'location':'home',
            'ref':'experienced-event1','participated':True,
            'perceived_cues':[current_cue()]}


class R14SourcefreeModule(unittest.TestCase):
    def setUp(self):
        self.actor=newborn('nadia','Nadia')
        self.source=conserve_received_period_care(self.actor,period())

    def test_period_is_not_automatic_attachment_or_knowledge(self):
        self.assertEqual(len(self.actor['undergone_care_periods']),1)
        self.assertEqual(self.actor['co_regulation_orientations'],[])
        self.assertEqual(self.actor['other_models'],{})
        self.assertEqual(self.actor['self_model'],{})
        self.assertEqual(self.actor['memories'],[])
        self.assertEqual(self.source['actor_identified_source_of_relief'],
                         'NOT_ESTABLISHED')
        self.assertNotIn('coactor_consent',self.source)

    def test_later_real_copresence_and_typed_owner_acquire_a_possibility(self):
        candidates=possible_acquired_regulation(
            self.actor,experience(),'event1')
        self.assertEqual(len(candidates),1)
        admitted=sourcefree_co_regulation_proposal(candidates)
        self.assertEqual(len(admitted),1)
        receipt=admit_co_regulation(
            self.actor,experience(),'event1',admitted[0])
        self.assertEqual(receipt['caregiver_ref'],'mother')
        view=SimpleNamespace(actor='nadia',body=self.actor['body'],
            clock=21,co_regulation_orientations=self.actor[
                'co_regulation_orientations'])
        access=SimpleNamespace(actor='nadia',location='home',
                                cues=[current_cue()])
        projection=recruit_co_regulation(view,access)
        self.assertEqual(len(projection['offered']),1)
        alt=addressed_signal_alternatives(
            view,access,{'action':'SIGNAL'})
        self.assertEqual(len(alt),1)
        self.assertEqual(alt[0]['world_request']['addressed_party_ref'],
                         'mother')
        # Consent is a claim about the Other's actual response, not a
        # property silently derived from an earlier lived care relationship.
        # Inspect typed keys, not non-iterable int/string values.
        self.assertFalse(any('consent' in str(key).lower() and value is True
                             for key,value in alt[0].items()))
        self.assertIsNone(choose_historically_situated_signal(
            [{'action':'SIGNAL','practical_alternatives':alt}],
            {'comfort':.8,'nutrition':.8,'rest':.8}))
        selected=choose_historically_situated_signal(
            [{'action':'SIGNAL','practical_alternatives':alt}],
            {'comfort':.4,'nutrition':.8,'rest':.8})
        self.assertEqual(selected['practical_option_id'],alt[0]['option_id'])
        self.assertIsNone(selected['project_id'])

    def test_no_assumed_person_without_sensory_history_or_present_cue(self):
        blind=newborn('nadia','Nadia')
        blind['body']['sensor']=0.
        self.assertIsNone(conserve_received_period_care(blind,period()))
        self.assertEqual(blind['undergone_care_periods'],[])
        absent={**experience(),'perceived_cues':[]}
        self.assertEqual(possible_acquired_regulation(
            self.actor,absent,'event1'),[])
        candidate=sourcefree_co_regulation_proposal(
            possible_acquired_regulation(self.actor,experience(),'event1'))[0]
        with self.assertRaisesRegex(ValueError,
                                    'COREGULATION_ADMISSION_NO_LIVED_COPRESENCE'):
            admit_co_regulation(self.actor,absent,'event1',candidate)
        with self.assertRaisesRegex(ValueError,
                                    'COREGULATION_ADMISSION_FOREIGN_CARE_HISTORY'):
            admit_co_regulation(self.actor,experience(),'event1',
                                {**candidate,'period_refs':['invented']})

    def test_opposed_or_ambiguous_relationship_does_not_pick_partner(self):
        candidate=sourcefree_co_regulation_proposal(
            possible_acquired_regulation(self.actor,experience(),'event1'))[0]
        admit_co_regulation(self.actor,experience(),'event1',candidate)
        view=SimpleNamespace(actor='nadia',body=self.actor['body'],
            clock=21,co_regulation_orientations=self.actor[
                'co_regulation_orientations'])
        access=SimpleNamespace(actor='nadia',location='home',
                                cues=[current_cue()])
        alt=addressed_signal_alternatives(
            view,access,{'action':'SIGNAL'})
        options=[{'action':'SIGNAL','practical_alternatives':alt,
                  'project_courses':[{'project_id':'different_purpose'}]}]
        self.assertIsNone(choose_historically_situated_signal(
            options,{'comfort':.2,'nutrition':.4,'rest':.1}))
        two=alt+[{
            **alt[0],'option_id':'second_option',
            'world_request':{'operation':'SIGNAL',
                             'addressed_party_ref':'father',
                             'material_object_ref':None}}]
        self.assertIsNone(choose_historically_situated_signal(
            [{'action':'SIGNAL','practical_alternatives':two}],
            {'comfort':.2,'nutrition':.4,'rest':.1}))


    def test_two_actual_unfinished_calls_can_revise_without_retroactive_erasure(self):
        actor,history,earlier,proposal=self.actor,self.source,experience(),None
        possibility=possible_acquired_regulation(actor,earlier,'first')
        proposal=sourcefree_co_regulation_proposal(possibility)[0]
        admitted=admit_co_regulation(actor,earlier,'first',proposal)
        orientation=admitted['orientation_ref']
        selection={
            'source_co_regulation_orientation_ref':orientation,
            'world_request':{'operation':'SIGNAL',
                'addressed_party_ref':'mother','material_object_ref':None}}
        def missed_call(index):
            return {'actor':'nadia','ref':'experience:'+str(index),
                'clock':25+index,'location':'home',
                'own_action':'SIGNAL','status':'PARTIAL',
                'felt_enactment':{'attempted_operation':'SIGNAL'},
                'perceived_cues':[{
                    'id':'sign:'+str(index),'kind':'performed_signal',
                    'source_actor':'nadia',
                    'description':'ATTEMPT_NOT_COMPLETED'}],
                'participated':True}
        e1=missed_call(1)
        record_lived_co_regulation_response(
            actor,e1,selection,'second')
        self.assertEqual(possible_revision_after_nonresponse(
            actor,e1,'second'),[])
        e2=missed_call(2)
        record_lived_co_regulation_response(
            actor,e2,selection,'third')
        proposals=possible_revision_after_nonresponse(
            actor,e2,'third')
        self.assertEqual(len(proposals),1)
        typed=sourcefree_revision_proposal(proposals)
        self.assertEqual(len(typed),1)
        result=admit_co_regulation_revision(
            actor,e2,'third',typed[0])
        self.assertEqual(result['phase'],'UNRESOLVED_AFTER_NONRESPONSE')
        self.assertEqual(len(actor['undergone_care_periods']),1)
        self.assertEqual(len(actor['co_regulation_orientations'][0][
            'response_history']),2)
        view=SimpleNamespace(actor='nadia',body=actor['body'],
            clock=28,co_regulation_orientations=actor[
                'co_regulation_orientations'])
        access=SimpleNamespace(actor='nadia',location='home',
                                cues=[current_cue()])
        projected=recruit_co_regulation(view,access)
        self.assertEqual(projected['offered'],[])
        self.assertEqual(len(
            projected['suspended_after_contradiction']),1)
        self.assertEqual(len(projected['readset']),1)

    def test_one_failed_or_unsensed_call_does_not_prove_rejection(self):
        actor=self.actor
        e=experience()
        proposal=sourcefree_co_regulation_proposal(
            possible_acquired_regulation(actor,e,'first'))[0]
        orientation=admit_co_regulation(
            actor,e,'first',proposal)['orientation_ref']
        selection={'source_co_regulation_orientation_ref':orientation,
                   'world_request':{'addressed_party_ref':'mother'}}
        no_sign={'actor':'nadia','ref':'later','own_action':'SIGNAL',
                 'status':'PARTIAL',
                 'felt_enactment':{'attempted_operation':'SIGNAL'},
                 'perceived_cues':[]}
        self.assertIsNone(record_lived_co_regulation_response(
            actor,no_sign,selection,'later'))
        self.assertEqual(actor['co_regulation_orientations'][0].get(
            'response_history',[]),[])
        with self.assertRaisesRegex(
                ValueError,'COREGULATION_REVISE_NO_CURRENT_LIVED_RESPONSE'):
            admit_co_regulation_revision(actor,no_sign,'later',{
                'orientation_ref':orientation,
                'latest_response_ref':'fictional',
                'interpretation_phase':'UNRESOLVED_AFTER_NONRESPONSE'})


class R14IntegratedLife(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.rt=ConstitutiveRuntime(
            str(Path(self.tmp.name)/'r14_coregulation.sqlite3'))
        self.addCleanup(self.rt.close)
        self.rt.initialize([
            ('mother','Mother',PARENT),('father','Father',PARENT)])

    def test_qualified_care_becomes_a_later_independently_answered_call(self):
        before=self.rt.snapshot('nadia')
        self.assertEqual(before['co_regulation_orientations'],[])
        source=self.rt.register_historical_routine_source({
            'kind':'QUALIFIED_REPRODUCTIVE_CARE',
            'actor':'mother','location':'home',
            'start_clock':0,'end_clock':90,
            'max_hours_per_active_day':4,
            'description':'fictional 80-day recurring household care fixture'})
        self.rt.background(80,[{
            'kind':'QUALIFIED_REPRODUCTIVE_CARE',
            'actor':'mother','recipient':'nadia','location':'home',
            'source_ref':source['source_ref'],
            'hours_per_active_day':4,
            'provisional_exposure_fraction':.8}])
        after=self.rt.snapshot('nadia')
        self.assertEqual(len(after['undergone_care_periods']),1)
        self.assertEqual(after['co_regulation_orientations'],[])
        self.assertGreater(after['body']['comfort'],before['body']['comfort'])
        # Not a new attachment until a separate real sensory encounter.
        real=self.rt.step('nadia',requested_action='ORIENT')
        self.assertEqual(real['status'],'PERFORMED')
        acquired=self.rt.snapshot('nadia')
        self.assertEqual(len(acquired['co_regulation_orientations']),1)
        self.assertEqual(acquired['co_regulation_orientations'][0][
            'caregiver_ref'],'mother')
        self.assertEqual(acquired['self_model'],{})
        # A later material need can recruit this particular recipient;
        # neither prior care nor the current call authorizes Mother's reply.
        self.rt.background(400)
        prospect=self.rt.plan('nadia')
        self.assertEqual(prospect.action,'SIGNAL')
        self.assertEqual(prospect.target,'mother')
        result=self.rt.step('nadia')
        self.assertEqual(result['attempt'],'SIGNAL')
        self.assertIsNotNone(result['coactor'])
        self.assertTrue(self.rt.verify()['valid'])

    def test_caregiver_absence_prevents_actor_bound_future_call(self):
        source=self.rt.register_historical_routine_source({
            'kind':'QUALIFIED_REPRODUCTIVE_CARE','actor':'mother',
            'location':'home','start_clock':0,'end_clock':45,
            'max_hours_per_active_day':4,
            'description':'fictional historical co-regulation fixture'})
        self.rt.background(40,[{
            'kind':'QUALIFIED_REPRODUCTIVE_CARE',
            'actor':'mother','recipient':'nadia','location':'home',
            'source_ref':source['source_ref'],
            'hours_per_active_day':4,
            'provisional_exposure_fraction':1.0}])
        self.rt.step('nadia',requested_action='ORIENT')
        self.assertEqual(len(self.rt.snapshot('nadia')[
            'co_regulation_orientations']),1)
        self.rt.step('mother',requested_action='MOVE',object_ref='workshop')
        self.rt.background(400)
        prospective=self.rt.plan('nadia')
        self.assertNotEqual(prospective.target,'mother')


if __name__=='__main__':
    unittest.main()
