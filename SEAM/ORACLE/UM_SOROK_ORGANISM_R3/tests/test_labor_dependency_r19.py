"""SORACLE R19 — wage dependence, worker interruption, funded relief and Nadia.

Executable original-repository integration candidates. NOT executed by SORACLE
and not accredited by REMONT until exact HEAD checkout and full regression.
All occupational conditions are declared fictional research fixtures.
"""
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.types import adult,newborn,blank_world,Attempt
from um_sorok_organism.world import resolve
from um_sorok_organism.labor_dependency import (
    register_work_regime,work_permission,accept_work_terms,
    suspend_worker,withdraw_labor,fund_worker_relief,draw_worker_relief,
    actor_work_opportunities)
from um_sorok_organism.livelihood_history import (
    conserve_incomplete_work,sourcefree_relief_recruitment)
from um_sorok_organism.constitution import actor_access,materialize,compose
from um_sorok_organism.runtime import ConstitutiveRuntime

AUTONOMOUS='ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE'
INJECTED='INJECTED_NOT_NATIVE_ACTOR_CHOICE'
PARENT={
    'source_ref':'r19_fictional_not_PYAT',
    'source_grade':'UNQUALIFIED_FICTIONAL_TEST_FIXTURE',
    'answers':{'r19_synthetic':'no_real_respondent_hypothesis'},
    'fictional_seed':{'projects':[]}}

def fixture():
    w=blank_world()
    a={'mother':adult('mother','Mother'),
       'father':adult('father','Father'),
       'nadia':newborn('nadia','Nadia')}
    for person in a.values():
        w['positions'][person['id']]='workshop'
        person['location']='workshop'
    w['accounts'].update({'mother':0,'father':0})
    return w,a

def employment_spec():
    return {
        'grade':'EXPLICIT_SOURCEFREE_INSTITUTIONAL_SCENARIO',
        'source_ref':'r19_sourcefree_existing_enterprise_employment',
        'site':'workshop','controller':'workshop_steward',
        'eligible_workers':['mother','father'],
        'delegates':['father']}

def saw_notice(actor,ref,clock=0):
    actor['notice_exposures'].append({
        'id':'actually_inspected:'+actor['id']+':'+ref,
        'public_notice_ref':ref,
        'inspected_at_clock':clock,
        'public_words_available':['wage_work','contract_terms'],
        'no_automatic_political_ideology':True})

class WageRelationWorld(unittest.TestCase):
    def setUp(self):
        self.w,self.a=fixture()
        self.ref=register_work_regime(self.w,self.a,employment_spec())

    def test_world_registration_does_not_create_worker_contract(self):
        self.assertEqual(work_permission(self.w,'mother','workshop'),
                         'NO_ACCEPTED_WAGE_CONTRACT')
        self.assertFalse(self.w['work_regimes']['workshop']['contracts'])
        self.assertEqual(self.a['mother']['self_model'],{})
        self.assertEqual(self.w['accounts']['mother'],0)

    def test_distinct_inspection_and_worker_acceptance_precede_paid_work(self):
        rejected=accept_work_terms(
            self.w,self.a,'mother','workshop',INJECTED)
        self.assertEqual(rejected['status'],'BLOCKED')
        notice=self.ref['terms_notice_ref']
        saw_notice(self.a['mother'],notice)
        accepted=accept_work_terms(
            self.w,self.a,'mother','workshop',INJECTED)
        self.assertEqual(accepted['status'],'PERFORMED')
        self.assertEqual(work_permission(self.w,'mother','workshop'),
                         'QUALIFIED_WORK_CONTRACT_ACTIVE')
        self.assertEqual(self.w['work_regimes']['workshop']['contracts'][
            'mother']['actor_selection_source'],INJECTED)
        self.assertEqual(self.a['mother']['self_model'],{})

    def test_employer_financed_sanction_controls_access_not_bodily_power(self):
        saw_notice(self.a['mother'],self.ref['terms_notice_ref'])
        accept_work_terms(self.w,self.a,'mother','workshop',AUTONOMOUS)
        before=self.w['accounts']['workshop_steward']
        status=suspend_worker(
            self.w,self.a,'father','mother','workshop',AUTONOMOUS)
        self.assertEqual(status['status'],'PERFORMED')
        self.assertEqual(work_permission(self.w,'mother','workshop'),
                         'QUALIFIED_WORK_CONTRACT_ACTIVE')
        # Sourcefree sanctions start next clock and do not rewrite the
        # worker's historical contract or pretend she approved punishment.
        self.w['clock']=1
        self.assertEqual(work_permission(self.w,'mother','workshop'),
                         'EMPLOYER_SANCTION_PREVENTS_PAID_WORK')
        regime=self.w['work_regimes']['workshop']
        service=regime['enforcement_service_ref']
        self.assertEqual(self.w['accounts']['workshop_steward'],before-1)
        self.assertEqual(self.w['accounts'][service],1)
        self.assertEqual(self.w['accounts']['workshop_steward']+
                         self.w['accounts'][service],before)
        self.assertTrue(regime['contracts']['mother']['status']=='ACTIVE')
        self.w['clock']=5
        self.assertEqual(work_permission(self.w,'mother','workshop'),
                         'QUALIFIED_WORK_CONTRACT_ACTIVE')

    def test_worker_not_employer_authors_withdrawal(self):
        saw_notice(self.a['mother'],self.ref['terms_notice_ref'])
        accept_work_terms(self.w,self.a,'mother','workshop',AUTONOMOUS)
        ended=withdraw_labor(
            self.w,self.a,'mother','workshop',AUTONOMOUS)
        self.assertEqual(ended['status'],'PERFORMED')
        self.assertEqual(work_permission(self.w,'mother','workshop'),
                         'NO_ACCEPTED_WAGE_CONTRACT')
        self.assertEqual(self.w['work_regimes']['workshop']['contracts'][
            'mother']['withdrawal_selection_source'],AUTONOMOUS)
        self.assertEqual(self.w['accounts']['mother'],0)

    def test_worker_relief_must_be_earned_and_physically_funded(self):
        saw_notice(self.a['mother'],self.ref['terms_notice_ref'])
        saw_notice(self.a['father'],self.ref['terms_notice_ref'])
        accept_work_terms(self.w,self.a,'mother','workshop',AUTONOMOUS)
        accept_work_terms(self.w,self.a,'father','workshop',AUTONOMOUS)
        # A stocked private account alone is not evidence of earned wages.
        self.w['accounts']['father']=5
        no_fake_wage=fund_worker_relief(
            self.w,self.a,'father','workshop',AUTONOMOUS)
        self.assertEqual(no_fake_wage['status'],'BLOCKED')
        # Earn the wage by executing the ORIGINAL work owner, rather than
        # fabricating a claim row that only resembles the actual source.
        performed=resolve(self.w,self.a,Attempt(
            actor='father',action='WORK',intention=AUTONOMOUS))
        self.assertEqual(performed.status,'PERFORMED')
        self.assertEqual(performed.objective_description,
                         'PRODUCED_GOODS_CONTROLLED_BY_OTHER')
        self.assertEqual(self.w['material_claims'][-1]['wage'],.25)
        contributed=fund_worker_relief(
            self.w,self.a,'father','workshop',AUTONOMOUS)
        self.assertEqual(contributed['status'],'PERFORMED')
        # Initial money is not a bottomless claim against one wage.
        duplicated=fund_worker_relief(
            self.w,self.a,'father','workshop',AUTONOMOUS)
        self.assertEqual(duplicated['status'],'BLOCKED')
        fund=self.w['work_regimes']['workshop']['relief_pool_ref']
        self.assertEqual(self.w['accounts'][fund],.25)
        suspend_worker(self.w,self.a,'father','mother','workshop',AUTONOMOUS)
        self.w['clock']=2
        drew=draw_worker_relief(
            self.w,self.a,'mother','workshop',AUTONOMOUS)
        self.assertEqual(drew['status'],'PERFORMED')
        self.assertEqual(self.w['accounts'][fund],0)
        self.assertEqual(self.w['accounts']['mother'],.25)
        self.assertEqual(draw_worker_relief(
            self.w,self.a,'mother','workshop',AUTONOMOUS)['status'],
            'BLOCKED')
        self.assertTrue(self.w['work_regimes']['workshop'][
            'contracts']['mother']['status']=='ACTIVE')

    def test_suspension_does_not_seize_other_worksite_or_person(self):
        unrelated=adult('outsider','Outsider')
        self.a['outsider']=unrelated
        self.w['positions']['outsider']='home'
        unrelated['location']='home'
        denied=suspend_worker(
            self.w,self.a,'father','outsider','workshop',AUTONOMOUS)
        self.assertEqual(denied['status'],'BLOCKED')
        self.assertEqual(work_permission(self.w,'outsider','home'),
                         'NO_ADDITIONAL_CONTRACT_REGIME')


class WorkInActorHistory(unittest.TestCase):
    def setUp(self):
        self.w,self.a=fixture()
        self.ref=register_work_regime(self.w,self.a,employment_spec())

    def test_actually_unfinished_work_may_recruit_real_funded_relief(self):
        exp={'actor':'mother','clock':4,'location':'workshop',
             'ref':'experienced_unfinished_work','own_action':'WORK',
             'status':'BLOCKED','participated':True,
             'felt_enactment':{'attempted_operation':'WORK'},
             'perceived_cues':[{'kind':'performed_work',
                 'source_actor':'mother','id':'actual_ended_work_sign',
                 'description':'ATTEMPT_NOT_COMPLETED'}]}
        row=conserve_incomplete_work(
            self.a['mother'],exp,'objective:blocked_worker')
        self.assertEqual(row['reason_employer_or_body_or_structural'],
                         'NOT_INFERRED')
        self.assertEqual(self.a['mother']['self_model'],{})
        saw_notice(self.a['mother'],self.ref['terms_notice_ref'])
        accept_work_terms(self.w,self.a,'mother','workshop',AUTONOMOUS)
        self.w['clock']=4
        self.w['work_regimes']['workshop']['suspensions'].append({
            'worker':'mother','start_clock':3,'through_clock':5})
        self.w['accounts'][self.w['work_regimes']['workshop'][
            'relief_pool_ref']]=.25
        view=compose(materialize(self.a['mother'],self.w),
                     actor_access(self.a['mother'],self.w))
        offers=[x for x in view.candidate_actions if x['action']==
                'DRAW_WAGE_RELIEF']
        self.assertEqual(len(offers),1)
        proposal=sourcefree_relief_recruitment(offers)
        self.assertEqual(proposal['action'],'DRAW_WAGE_RELIEF')
        self.assertEqual(proposal['lived_source_ref'],row['id'])

    def test_future_experience_cannot_speak_in_past(self):
        self.a['mother']['labor_dependency_encounters']=[{
            'id':'future_worker','own_attempted_work':'WORK',
            'location':'workshop','clock':99}]
        self.w['clock']=2
        view=compose(materialize(self.a['mother'],self.w),
                     actor_access(self.a['mother'],self.w))
        offered=[x for x in view.candidate_actions if x['action']==
                 'DRAW_WAGE_RELIEF']
        self.assertIsNone(sourcefree_relief_recruitment(offered))


class JoinedWageLife(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.rt=ConstitutiveRuntime(str(
            Path(self.tmp.name)/'r19_wages.sqlite3'))
        self.addCleanup(self.rt.close)
        self.rt.initialize([
            ('mother','Mother',PARENT),
            ('father','Father',PARENT)])
        self.registered=self.rt.register_sourcefree_work_regime(
            employment_spec())

    def test_wage_work_requires_received_terms_then_actor_contract(self):
        self.rt.step('mother',requested_action='MOVE',
                     object_ref='workshop')
        blocked=self.rt.step('mother',requested_action='WORK')
        self.assertEqual(blocked['status'],'BLOCKED')
        self.rt.step('mother',requested_action='INSPECT',
                     object_ref=self.registered['terms_notice_ref'])
        accepted=self.rt.step('mother',requested_action='ACCEPT_WORK_TERMS')
        self.assertEqual(accepted['status'],'PERFORMED')
        done=self.rt.step('mother',requested_action='WORK')
        self.assertEqual(done['status'],'PERFORMED')
        _,w=self.rt.ledger.world('w1')
        self.assertEqual(w['accounts']['mother'],.25)
        self.assertEqual(w['accounts']['workshop_steward'],11.75)
        self.assertTrue(self.rt.verify()['valid'])

    def test_wage_earned_becomes_food_for_child_through_independent_world(self):
        self.rt.step('mother',requested_action='MOVE',object_ref='workshop')
        self.rt.step('mother',requested_action='INSPECT',
                     object_ref=self.registered['terms_notice_ref'])
        self.rt.step('mother',requested_action='ACCEPT_WORK_TERMS')
        self.rt.step('mother',requested_action='WORK')
        version,w=self.rt.ledger.world('w1')
        w['sites']['workshop']['food_price']=.25
        self.rt.ledger.commit('w1',version,w,{}, {},
           'EXPLICIT_FICTIONAL_SHORTAGE_PRICE',None,
           {'price_not_empirically_issued':True})
        purchased=self.rt.step('mother',requested_action='BUY_FOOD')
        self.assertEqual(purchased['status'],'PERFORMED')
        self.rt.step('mother',requested_action='MOVE',object_ref='home')
        before=self.rt.snapshot('nadia')['body']['nutrition']
        fed=self.rt.step('mother',requested_action='FEED',target='nadia')
        self.assertEqual(fed['status'],'PERFORMED')
        self.assertGreater(self.rt.snapshot('nadia')['body']['nutrition'],
                           before)
        _,w=self.rt.ledger.world('w1')
        self.assertEqual(w['material_feeding_events'][-1]['food_source'],
                         'GIVER_HELD_FOOD')
        self.assertTrue(self.rt.verify()['valid'])

    def test_joined_employer_sanction_and_real_wage_relief(self):
        # Distinct adult action streams and real employer money meet at one
        # continuing world. Nadia never inherits the workers' adult concepts.
        for person in ('mother','father'):
            self.assertEqual(self.rt.step(
                person,requested_action='MOVE',
                object_ref='workshop')['status'],'PERFORMED')
            self.assertEqual(self.rt.step(
                person,requested_action='INSPECT',
                object_ref=self.registered['terms_notice_ref'])['status'],
                'PERFORMED')
            self.assertEqual(self.rt.step(
                person,requested_action='ACCEPT_WORK_TERMS')['status'],
                'PERFORMED')
        self.assertEqual(self.rt.step(
            'father',requested_action='WORK')['status'],'PERFORMED')
        self.assertEqual(self.rt.step(
            'mother',requested_action='WORK')['status'],'PERFORMED')
        self.assertEqual(self.rt.step(
            'father',requested_action='CONTRIBUTE_WAGE_RELIEF')['status'],
            'PERFORMED')
        before=self.rt.ledger.world('w1')[1]
        total_before=sum(before['accounts'].values())
        sanction=self.rt.step('father',requested_action='SUSPEND_WAGE_WORK',
                             target='mother')
        self.assertEqual(sanction['status'],'PERFORMED')
        blocked=self.rt.step('mother',requested_action='WORK')
        self.assertEqual(blocked['status'],'BLOCKED')
        self.assertEqual(self.rt.snapshot('mother')[
            'labor_dependency_encounters'][0]['own_attempted_work'],'WORK')
        self.assertEqual(self.rt.snapshot('nadia')[
            'labor_dependency_encounters'],[])
        candidates=[x for x in self.rt.situated('mother')[
            'candidate_actions'] if x['action']=='DRAW_WAGE_RELIEF']
        self.assertEqual(len(candidates),1)
        self.assertTrue(candidates[0].get('labor_relief_ground'))
        paid=self.rt.step('mother',requested_action='DRAW_WAGE_RELIEF')
        self.assertEqual(paid['status'],'PERFORMED')
        world=self.rt.ledger.world('w1')[1]
        self.assertEqual(world['accounts'][
            self.registered['relief_pool_ref']],0)
        self.assertEqual(world['accounts']['mother'],.5)
        self.assertEqual(sum(world['accounts'].values()),total_before)
        self.assertTrue(self.rt.verify()['valid'])

    def test_employer_suspension_requires_named_present_actor_target(self):
        for person in ('mother','father'):
            self.rt.step(person,requested_action='MOVE',
                         object_ref='workshop')
        self.rt.step('mother',requested_action='INSPECT',
                     object_ref=self.registered['terms_notice_ref'])
        self.rt.step('mother',requested_action='ACCEPT_WORK_TERMS')
        targets=[a for x in self.rt.situated('father')['candidate_actions']
                 if x['action']=='SUSPEND_WAGE_WORK'
                 for a in x['practical_alternatives']
                 if a['world_request']['addressed_party_ref']=='mother']
        self.assertEqual(len(targets),1)
        self.assertEqual(targets[0]['binding_status'],
                         'ACTUALLY_COPRESENT_TARGET')
        self.assertTrue(targets[0][
            'world_will_requalify_authority_at_execution'])


if __name__=='__main__':
    unittest.main()
