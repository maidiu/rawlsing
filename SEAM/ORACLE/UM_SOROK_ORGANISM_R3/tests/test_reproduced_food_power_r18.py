"""SORACLE R18 independent receiving candidates — sourcefree, UNEXECUTED here.

Material power must be constituted, maintained and sometimes undermined by
actual actions, not assigned as psychological scores. Run exact branch and
whole inherited test court under REMONT; no author G5 claims.
"""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from um_sorok_organism.types import blank_world,adult,newborn
from um_sorok_organism.food_power_reproduction import (
    register_concession,install_gate,maintain_gate,sanction_gate,
    contribute_food_commons,effective_enforcement,food_power_opportunities,
    offer_control_transfer,accept_control_transfer)
from um_sorok_organism.food_access_struggle import (
    can_draw_shared_food,contribute_food_petition)
from um_sorok_organism.material_provisioning import (
    perform_one_actual_feeding)
from um_sorok_organism.material_dependency_history import (
    conserve_sensed_material_nonperformance,choose_lived_material_counterpath)
from um_sorok_organism.constitution import actor_access,materialize,compose
from um_sorok_organism.runtime import ConstitutiveRuntime

AUTONOMOUS='ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE'
INJECTED='INJECTED_NOT_NATIVE_ACTOR_CHOICE'
PARENT={
    'source_ref':'r18_explicit_fictional_test_only',
    'source_grade':'UNQUALIFIED_FICTIONAL_TEST_FIXTURE',
    'answers':{'r18_synthetic_condition':'not_original_survey_evidence'},
    'fictional_seed':{'projects':[]}}

def initial():
    w=blank_world()
    a={'mother':adult('mother','Mother'),'father':adult('father','Father'),
       'nadia':newborn('nadia','Nadia')}
    for who,actor in a.items():
        actor['location']='home';w['positions'][who]='home'
        if actor['role']=='adult':
            actor['projects']=[{'id':'care:'+who,'status':'active',
                'means':['CARE','FEED'],'object':'providing situated care'}]
    w['holdings']={'father':{'food':4.0},'mother':{'food':2.0}}
    w['accounts']['father']=5.0
    return w,a

def concession_spec():
    return {
        'grade':'EXPLICIT_SOURCEFREE_INSTITUTIONAL_SCENARIO',
        'site':'home','possible_controller':'father',
        'eligible_petitioners':['father','mother'],
        'quorum':2,'source_ref':'r18_fictional_concession_history'}

def inspect(actor,notice,clock=0,words=None):
    actor['notice_exposures'].append({
        'id':'inspected:'+notice+actor['id'],
        'public_notice_ref':notice,'inspected_at_clock':clock,
        'public_words_available':words or ['food_enclosure_concession'],
        'not_auto_belief':True})

def enact(w,a):
    reg=register_concession(w,a,concession_spec())
    inspect(a['father'],reg['notice_ref'])
    result=install_gate(w,a,'father','home',AUTONOMOUS)
    assert result['status']=='PERFORMED'
    return reg,result

class R18WorldPower(unittest.TestCase):
    def setUp(self):
        self.w,self.a=initial()

    def test_grant_without_actor_enactment_has_no_control(self):
        source=register_concession(self.w,self.a,concession_spec())
        self.assertTrue(can_draw_shared_food(self.w,'mother','home'))
        self.assertNotIn('household_food_board',self.w['institutions'])
        self.assertNotIn('INSTALL_PANTRY_GATE',
            food_power_opportunities(self.w,self.a['father'],'home'))
        inspect(self.a['father'],source['notice_ref'])
        self.assertIn('INSTALL_PANTRY_GATE',
            food_power_opportunities(self.w,self.a['father'],'home'))

    def test_enclosure_requires_prior_inspection_and_private_material_transfer(self):
        register_concession(self.w,self.a,concession_spec())
        denied=install_gate(self.w,self.a,'father','home',INJECTED)
        self.assertEqual(denied['status'],'BLOCKED')
        self.assertEqual(self.w['sites']['home']['food'],12)
        source=self.w['food_control_concessions']['home']
        inspect(self.a['father'],source['public_notice_ref'])
        created=install_gate(self.w,self.a,'father','home',INJECTED)
        self.assertEqual(created['status'],'PERFORMED')
        self.assertEqual(self.w['sites']['home']['food'],14)
        self.assertEqual(self.w['holdings']['father']['food'],2)
        self.assertEqual(self.w['accounts']['father'],4)
        service=self.w['food_control_concessions']['home'][
            'enforcement_service_ref']
        self.assertEqual(self.w['accounts'][service],1)
        self.assertEqual(self.w['accounts']['father']+
                         self.w['accounts'][service],5)
        self.assertEqual(self.w['institutions'][
            'household_food_board']['r18_enforcement_history'][0][
            'actor_selection_source'],INJECTED)
        self.assertFalse(can_draw_shared_food(self.w,'mother','home'))
        self.assertTrue(can_draw_shared_food(self.w,'father','home'))

    def test_legal_gate_persists_when_enforcement_expires(self):
        enact(self.w,self.a)
        self.w['clock']=5
        board=self.w['institutions']['household_food_board']
        self.assertEqual(board['food_rights'],'CONTROLLED')
        self.assertFalse(effective_enforcement(board,self.w['clock']))
        self.assertTrue(can_draw_shared_food(self.w,'mother','home'))
        self.assertTrue(board['objective_control_not_a_mental_trait'])

    def test_paid_reproduction_of_control_extends_effective_exclusion(self):
        enact(self.w,self.a)
        self.w['clock']=3
        self.assertEqual(maintain_gate(self.w,self.a,'father','home',
            AUTONOMOUS)['status'],'PERFORMED')
        self.assertEqual(self.w['accounts']['father'],3)
        service=self.w['food_control_concessions']['home'][
            'enforcement_service_ref']
        self.assertEqual(self.w['accounts'][service],2)
        self.assertEqual(self.w['accounts']['father']+
                         self.w['accounts'][service],5)
        self.w['clock']=7
        self.assertFalse(can_draw_shared_food(self.w,'mother','home'))
        self.w['clock']=9
        self.assertTrue(can_draw_shared_food(self.w,'mother','home'))

    def test_collective_rule_change_and_residual_sanction_are_distinct(self):
        enact(self.w,self.a)
        board=self.w['institutions']['household_food_board']
        for person in ('father','mother'):
            inspect(self.a[person],board['public_notice_ref'],words=[
                'public_petition','household_food','collective_food_access'])
        first=contribute_food_petition(
            self.w,self.a,'mother','home',AUTONOMOUS)
        second=contribute_food_petition(
            self.w,self.a,'father','home',AUTONOMOUS)
        self.assertFalse(first['institutional_rule_change'])
        self.assertTrue(second['institutional_rule_change'])
        self.assertTrue(can_draw_shared_food(self.w,'mother','home'))
        sanction=sanction_gate(
            self.w,self.a,'father','mother','home',AUTONOMOUS)
        self.assertEqual(sanction['status'],'PERFORMED')
        service=self.w['food_control_concessions']['home'][
            'enforcement_service_ref']
        self.assertEqual(self.w['accounts']['father'],2)
        self.assertEqual(self.w['accounts'][service],3)
        self.assertEqual(self.w['accounts']['father']+
                         self.w['accounts'][service],5)
        self.w['clock']=1
        self.assertFalse(can_draw_shared_food(self.w,'mother','home'))
        self.assertTrue(can_draw_shared_food(self.w,'nadia','home'))
        self.assertEqual(board['food_rights'],'SHARED_BY_COLLECTIVE_ACTS')
        # DCO MP-2 first consumer: a collective legal victory is not yet the
        # caregiver's effective power to provision a child. No hidden private
        # fallback may mask this sanction; the same real stock persists.
        self.w['holdings']['mother']['food']=0
        stock_before=self.w['sites']['home']['food']
        nutrition_before=self.a['nadia']['body']['nutrition']
        blocked=perform_one_actual_feeding(
            self.w,self.a,'mother','nadia','home',AUTONOMOUS)
        self.assertEqual(blocked['status'],'BLOCKED')
        self.assertEqual(self.w['sites']['home']['food'],stock_before)
        self.assertEqual(self.a['nadia']['body']['nutrition'],nutrition_before)
        self.assertEqual(board['food_rights'],'SHARED_BY_COLLECTIVE_ACTS')
        # No new legal reform, actor motive or child ideology is manufactured:
        # only the independently clocked paid exclusion has expired.
        self.w['clock']=5
        self.assertTrue(can_draw_shared_food(self.w,'mother','home'))
        actually_fed=perform_one_actual_feeding(
            self.w,self.a,'mother','nadia','home',AUTONOMOUS)
        self.assertEqual(actually_fed['status'],'PERFORMED')
        self.assertEqual(self.w['sites']['home']['food'],stock_before-1)
        self.assertGreater(self.a['nadia']['body']['nutrition'],nutrition_before)
        self.assertEqual(board['food_rights'],'SHARED_BY_COLLECTIVE_ACTS')
        self.assertEqual(self.a['nadia']['self_model'],{})

    def test_material_counterstock_survives_institutional_exclusion(self):
        enact(self.w,self.a)
        self.w['clock']=1
        # Institution holds fourteen real units, yet mother cannot access it.
        self.assertFalse(can_draw_shared_food(self.w,'mother','home'))
        # Contribute the LAST privately held unit. The next feeding
        # cannot accidentally use private holdings rather than the new
        # collectively constituted store.
        self.w['holdings']['mother']['food']=1.0
        old=self.w['holdings']['mother']['food']
        moved=contribute_food_commons(
            self.w,self.a,'mother','home',AUTONOMOUS)
        self.assertEqual(moved['status'],'PERFORMED')
        self.assertEqual(self.w['sites']['home']['food'],14)
        self.assertEqual(self.w['sites']['home']['mutual_aid_food'],1)
        self.assertEqual(self.w['holdings']['mother']['food'],old-1)
        before=self.a['nadia']['body']['nutrition']
        fed=perform_one_actual_feeding(
            self.w,self.a,'mother','nadia','home',AUTONOMOUS)
        self.assertEqual(fed['status'],'PERFORMED')
        self.assertEqual(self.w['material_feeding_events'][-1][
            'food_source'],'MUTUAL_AID_FOOD')
        self.assertEqual(self.w['sites']['home']['mutual_aid_food'],0)
        self.assertEqual(self.w['sites']['home']['food'],14)
        self.assertGreater(self.a['nadia']['body']['nutrition'],before)

    def test_property_transmission_is_two_independent_material_acts(self):
        enact(self.w,self.a)
        self.w['accounts']['mother']=2.0
        offer=offer_control_transfer(
            self.w,self.a,'father','mother','home',AUTONOMOUS)
        self.assertEqual(offer['status'],'PERFORMED')
        board=self.w['institutions']['household_food_board']
        self.assertEqual(board['controller_actor'],'father')
        self.assertFalse(can_draw_shared_food(self.w,'mother','home'))
        self.w['clock']=1
        refused=accept_control_transfer(
            self.w,self.a,'mother','home',AUTONOMOUS)
        self.assertEqual(refused['status'],'BLOCKED')
        self.assertEqual(self.w['accounts']['mother'],2)
        inspect(self.a['mother'],offer['notice_ref'],clock=1,
                words=['food_control_offer','transmissible_property_claim'])
        completed=accept_control_transfer(
            self.w,self.a,'mother','home',AUTONOMOUS)
        self.assertEqual(completed['status'],'PERFORMED')
        self.assertEqual(board['controller_actor'],'mother')
        self.assertEqual(board['r18_original_controller_actor'],'father')
        self.assertEqual(board['initially_permitted_givers'],['mother'])
        self.assertEqual(board['r18_transfer_history'][0][
            'actor_selection_source'],AUTONOMOUS)
        self.assertEqual(self.w['accounts']['father'],5)
        self.assertEqual(self.w['accounts']['mother'],1)
        self.assertFalse(can_draw_shared_food(self.w,'father','home'))
        self.assertTrue(can_draw_shared_food(self.w,'mother','home'))
        service=self.w['food_control_concessions']['home'][
            'enforcement_service_ref']
        self.assertEqual(self.w['accounts']['father']+
                         self.w['accounts']['mother']+
                         self.w['accounts'][service],7)

    def test_expired_unaccepted_transfer_cannot_install_new_controller(self):
        enact(self.w,self.a)
        self.w['accounts']['mother']=3.0
        offer=offer_control_transfer(
            self.w,self.a,'father','mother','home',AUTONOMOUS)
        self.w['clock']=5
        inspect(self.a['mother'],offer['notice_ref'],clock=1)
        old=accept_control_transfer(
            self.w,self.a,'mother','home',AUTONOMOUS)
        self.assertEqual(old['status'],'BLOCKED')
        self.assertEqual(self.w['institutions'][
            'household_food_board']['controller_actor'],'father')
        self.assertIn('OFFER_PANTRY_CONTROL_TRANSFER',
            food_power_opportunities(self.w,self.a['father'],'home'))

    def test_no_private_food_no_material_commons(self):
        self.w['holdings']['mother']['food']=0
        result=contribute_food_commons(
            self.w,self.a,'mother','home',AUTONOMOUS)
        self.assertEqual(result['status'],'BLOCKED')
        self.assertFalse(self.w.get('food_commons_history',[]))

    def test_no_other_persons_identity_or_conscious_theory_issued(self):
        enact(self.w,self.a)
        self.assertEqual(self.a['nadia']['self_model'],{})
        self.assertEqual(self.a['mother']['self_model'],{})
        self.assertEqual(self.a['father']['self_model'],{})
        for notice in self.w['public_notices']:
            self.assertNotIn('actor_ideology',notice)


class R18ActorHistory(unittest.TestCase):
    def setUp(self):
        self.w,self.a=initial()

    def test_unfinished_feeding_can_be_sensed_without_causing_class_theory(self):
        experience={
            'actor':'mother','clock':4,'location':'home',
            'ref':'experienced_failed_care_r18','own_action':'FEED',
            'status':'BLOCKED','participated':True,
            'felt_enactment':{'attempted_operation':'FEED'},
            'perceived_cues':[{
                'id':'witnessed_unfinished_feed','kind':'performed_feed',
                'source_actor':'mother','description':'ATTEMPT_NOT_COMPLETED'}]}
        row=conserve_sensed_material_nonperformance(
            self.a['mother'],experience,'objective:unfulfilled')
        self.assertEqual(row['actual_hidden_reason'],'NOT_KNOWN_TO_ACTOR')
        self.assertEqual(len(self.a['mother'][
            'material_dependency_encounters']),1)
        self.assertNotIn('capitalism',str(row).lower())
        self.w['clock']=4
        view=materialize(self.a['mother'],self.w)
        options=compose(view,actor_access(self.a['mother'],self.w))
        commons=[o for o in options.candidate_actions if o['action']==
                 'CONTRIBUTE_FOOD_COMMONS']
        self.assertEqual(len(commons),1)
        choice=choose_lived_material_counterpath(commons)
        self.assertEqual(choice['action'],'CONTRIBUTE_FOOD_COMMONS')
        self.assertEqual(choice['actor_conscious_institutional_diagnosis'],
                         'NOT_INFERRED')

    def test_future_or_foreign_history_not_recruited(self):
        self.a['mother']['material_dependency_encounters']=[{
            'id':'future','own_operation_attempted':'FEED',
            'location':'home','clock':10}]
        self.w['clock']=4
        view=materialize(self.a['mother'],self.w)
        possibilities=compose(view,actor_access(self.a['mother'],self.w))
        commons=[o for o in possibilities.candidate_actions
                 if o['action']=='CONTRIBUTE_FOOD_COMMONS']
        self.assertIsNone(choose_lived_material_counterpath(commons))
        self.assertFalse(possibilities.unknowns==[] and
                         self.a['mother']['self_model'])


class R18JoinedRuntime(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.rt=ConstitutiveRuntime(str(
            Path(self.tmp.name)/'r18.sqlite3'))
        self.addCleanup(self.rt.close)
        self.rt.initialize([
            ('mother','Mother',PARENT),('father','Father',PARENT)])
        # Explicit material-fiction fixture, not a claim these parents were
        # actually affluent or that a survey implied private food ownership.
        version,w=self.rt.ledger.world('w1')
        w.setdefault('holdings',{})['father']={'food':4.0}
        w['accounts']['father']=5.0
        self.rt.ledger.commit('w1',version,w,{}, {},
            'EXTERNAL_TEST_MATERIAL_STARTING_ASSETS',None,
            {'no_empirical_parent_inference':True})
        self.source=self.rt.register_sourcefree_pantry_concession(
            concession_spec())

    def test_live_concession_enactment_requires_actual_inspection_and_payment(self):
        notice=self.source['notice_ref']
        inspected=self.rt.step('father',requested_action='INSPECT',
                               object_ref=notice)
        self.assertEqual(inspected['status'],'PERFORMED')
        attempted=self.rt.step('father',
                     requested_action='INSTALL_PANTRY_GATE')
        self.assertEqual(attempted['status'],'PERFORMED')
        _,w=self.rt.ledger.world('w1')
        self.assertEqual(w['sites']['home']['food'],14)
        self.assertFalse(can_draw_shared_food(w,'mother','home'))
        self.assertTrue(self.rt.verify()['valid'])

    def test_live_two_actor_property_transfer_requires_later_inspection_and_payment(self):
        self.rt.step('father',requested_action='INSPECT',
                     object_ref=self.source['notice_ref'])
        self.rt.step('father',requested_action='INSTALL_PANTRY_GATE')
        version,w=self.rt.ledger.world('w1')
        w['accounts']['mother']=2.0
        self.rt.ledger.commit(
            'w1',version,w,{}, {},'EXPLICIT_FICTIONAL_BUYER_ASSETS',None,
            {'not_survey_empirical_assets':True})
        offered=self.rt.step('father',
            requested_action='OFFER_PANTRY_CONTROL_TRANSFER',target='mother')
        self.assertEqual(offered['status'],'PERFORMED')
        _,w=self.rt.ledger.world('w1')
        board=w['institutions']['household_food_board']
        self.assertEqual(board['controller_actor'],'father')
        offer_notice=board['r18_transfer_offer']['notice_ref']
        self.rt.step('mother',requested_action='INSPECT',
                     object_ref=offer_notice)
        purchased=self.rt.step('mother',
            requested_action='ACCEPT_PANTRY_CONTROL_TRANSFER')
        self.assertEqual(purchased['status'],'PERFORMED')
        _,w=self.rt.ledger.world('w1')
        board=w['institutions']['household_food_board']
        self.assertEqual(board['controller_actor'],'mother')
        self.assertEqual(len(board['r18_transfer_history']),1)
        self.assertEqual(w['accounts']['mother'],1.0)
        self.assertEqual(w['accounts']['father'],5.0)
        self.assertTrue(self.rt.verify()['valid'])

    def test_live_material_frustration_becomes_later_available_commons(self):
        self.rt.step('father',requested_action='INSPECT',
                     object_ref=self.source['notice_ref'])
        self.rt.step('father',requested_action='INSTALL_PANTRY_GATE')
        result=self.rt.step('mother',requested_action='FEED',target='nadia')
        self.assertEqual(result['status'],'BLOCKED')
        mother=self.rt.snapshot('mother')
        self.assertEqual(len(mother['material_dependency_encounters']),1)
        version,w=self.rt.ledger.world('w1')
        w.setdefault('holdings',{})['mother']={'food':1.0}
        self.rt.ledger.commit('w1',version,w,{}, {},
            'EXTERNAL_TEST_ACQUIRED_PRIVATE_FOOD',None,
            {'not_generated_from_a_survey_answer':True})
        present=self.rt.situated('mother')
        candidates=[x for x in present['candidate_actions']
                    if x['action']=='CONTRIBUTE_FOOD_COMMONS']
        self.assertEqual(len(candidates),1)
        self.assertEqual(choose_lived_material_counterpath(candidates)[
            'action'],'CONTRIBUTE_FOOD_COMMONS')
        response=self.rt.step('mother',
            requested_action='CONTRIBUTE_FOOD_COMMONS')
        self.assertEqual(response['status'],'PERFORMED')
        self.assertTrue(self.rt.verify()['valid'])


if __name__=='__main__':
    unittest.main()
