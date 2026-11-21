"""TCO R25: repeated personal work becomes an *optional* historical orientation.

Exercises original practical-powers, livelihood, semantic development,
historical self-organization, situated recruitment and objective world owners.
Nothing here imputes an employer's motives or a worker's political belief.
"""
import unittest
import tempfile
from pathlib import Path

from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import (
    adult, blank_world, Attempt, copy, stable_id,
)
from um_sorok_organism.practical_powers import retain_exercised_power
from um_sorok_organism.livelihood_history import (
    possible_recurrent_work_orientation,
    qualify_recurrent_work_orientation,
)
from um_sorok_organism.development import admit, InvalidDevelopment
from um_sorok_organism.historical_self_organization import pre_cue_pressures
from um_sorok_organism.constitution import materialize, actor_access, compose
from um_sorok_organism.world import resolve
from um_sorok_organism.semantics import (
    CallbackLLMProvider, ValidatingSemanticService,
    HeuristicSemanticProvider,
)


def work_experience(actor='mother',clock=1,*,site='home',
                    status='PERFORMED',event_ref=None,
                    source_actor=None,kind='performed_work'):
    event_ref = event_ref or f'objective:work:{clock}'
    cue = {
        'id':f'sensory:own_work:{clock}','kind':kind,
        'source_actor':actor if source_actor is None else source_actor,
        'modality':'visual',
        'description': ('MATERIAL_STOCK_PRODUCED' if status=='PERFORMED'
                        else 'ATTEMPT_NOT_COMPLETED'),
        'tags':['work']}
    return {
        'actor':actor,'ref':f'personal:work:{clock}',
        'clock':clock,'location':site,'status':status,
        'own_action':'WORK','participated':True,
        'felt_enactment':{'attempted_operation':'WORK'},
        'perceived_cues':[cue]},event_ref


def past_work(actor,clock,status='PERFORMED',**kwargs):
    experience,ref=work_experience(actor['id'],clock,status=status,**kwargs)
    retain_exercised_power(actor,experience,ref,experience['location'])
    return experience,ref


def make_actor():
    a=adult('mother','Mother')
    past_work(a,1,'PERFORMED')
    past_work(a,2,'BLOCKED')
    return a


def grounds(a,clock=3,**kwargs):
    e,ref=work_experience(clock=clock,**kwargs)
    found=possible_recurrent_work_orientation(a,e,ref)
    return e,ref,found


def proposal(g,polarity='WITHHOLD'):
    return {
        'kind':'ACQUIRE_HISTORICAL_ORIENTATION',
        'operation':'WORK',
        'orientation_mode':polarity,
        'perceived_cue_ref':g['current_received_work_sign_ref'],
        'recurrent_work_practice':{
            'prior_exercised_work_refs':list(g['prior_exercised_work_refs']),
            'current_received_work_sign_ref':g[
                'current_received_work_sign_ref'],
            'current_world_event_ref':g['current_world_event_ref'],
        }}


class TCORecurrentWorkR25(unittest.TestCase):
    def test_two_earlier_material_episodes_make_third_a_possible_source(self):
        a=make_actor()
        e,ref,g=grounds(a)
        self.assertEqual(len(g),1)
        self.assertEqual(g[0]['prior_world_event_refs'],
                         ['objective:work:1','objective:work:2'])
        self.assertEqual(g[0]['current_world_event_ref'],ref)
        self.assertEqual(g[0]['current_experience_ref'],e['ref'])
        self.assertEqual(g[0]['choice_of_approach_withhold_or_no_change'],
                         'OPEN')
        self.assertTrue(g[0]['not_a_conscious_work_ethic'])
        self.assertEqual(len(a['historical_orientations']),0)

    def test_model_proposal_admitted_through_existing_history_owner(self):
        a=make_actor()
        e,ref,g=grounds(a)
        semantic=ValidatingSemanticService(CallbackLLMProvider(
            lambda task,packet:{
                'task':task,
                'candidates':[proposal(packet[
                    'historically_possible_recurrent_livelihood_orientation'][0],
                    'WITHHOLD')]}))
        response=semantic.proposal('development',{
            'actor':{'id':'mother'},'experience':e,
            'historically_possible_recurrent_livelihood_orientation':g})
        self.assertEqual(a['historical_orientations'],[])
        result=admit(a,e,ref,response['candidates'])
        self.assertEqual(result[0]['kind'],'ACQUIRE_HISTORICAL_ORIENTATION')
        row=a['historical_orientations'][0]
        self.assertEqual(row['orientation_mode'],'WITHHOLD')
        self.assertEqual(row['operation'],'WORK')
        self.assertEqual(row['origin_event'],ref)
        self.assertEqual(row['recurrent_livelihood_ground']
                         ['previous_objective_attempt_refs'],
                         ['objective:work:1','objective:work:2'])
        self.assertTrue(row[
            'no_inevitable_compliance_resistance_or_conscious_theory'])

    def test_acquired_withhold_now_changes_future_own_work_recruitment(self):
        a=make_actor();e,ref,g=grounds(a)
        admit(a,e,ref,[proposal(g[0],'WITHHOLD')])
        world=blank_world();world['positions']['mother']='home'
        access=actor_access(a,world)
        c=materialize(a,world)
        result=compose(c,access)
        historic=pre_cue_pressures(c,access)
        self.assertEqual(len(historic['currents']),1)
        self.assertEqual(historic['currents'][0]['action'],'WORK')
        self.assertEqual(historic['currents'][0]['polarity'],'WITHHOLD')
        self.assertTrue(any(x['action']=='WORK'
                            and x['status']=='SITUATED_ACQUIRED_INHIBITION'
                            for x in result.suspended_actions))
        self.assertNotIn('WORK',[x['action'] for x in result.candidate_actions])

    def test_same_work_history_can_produce_approach_or_no_new_orientation(self):
        approach=make_actor()
        e,ref,g=grounds(approach)
        admit(approach,e,ref,[proposal(g[0],'APPROACH')])
        abstain=make_actor()
        self.assertEqual(len(abstain['historical_orientations']),0)
        w=blank_world();w['positions']['mother']='home'
        future=compose(materialize(approach,w),actor_access(approach,w))
        self.assertTrue(any(
            x['action']=='WORK' and
            x['psychodynamic_status']=='ACQUIRED_APPROACH_WITHOUT_RECORDED_COUNTERCURRENT'
            for x in future.candidate_actions))
        self.assertNotEqual(approach['historical_orientations'],
                            abstain['historical_orientations'])

    def test_fourth_episode_can_produce_opposed_lived_orientations(self):
        a=make_actor();e,ref,g=grounds(a)
        admit(a,e,ref,[proposal(g[0],'WITHHOLD')])
        retain_exercised_power(a,e,ref,e['location'])
        e4,ref4,g4=grounds(a,clock=4)
        self.assertEqual(len(g4),1)
        admit(a,e4,ref4,[proposal(g4[0],'APPROACH')])
        w=blank_world();w['positions']['mother']='home'
        view=compose(materialize(a,w),actor_access(a,w))
        opposed=[x for x in view.antagonisms if x['action']=='WORK']
        self.assertEqual(len(opposed),1)
        self.assertEqual(opposed[0]['resolution'],
                         'UNDETERMINED; NO FORCED HARMONY')
        self.assertEqual(len(a['historical_orientations']),2)

    def test_single_earlier_episode_is_not_a_recurrent_life(self):
        a=adult('mother','Mother');past_work(a,1)
        e,ref=work_experience(clock=2)
        self.assertEqual(possible_recurrent_work_orientation(a,e,ref),[])

    def test_same_episode_twice_cannot_buy_fake_historical_depth(self):
        a=adult('mother','Mother')
        past_work(a,1)
        a['power_exercises'].append(copy(a['power_exercises'][0]))
        e,ref=work_experience(clock=2)
        self.assertEqual(possible_recurrent_work_orientation(a,e,ref),[])

    def test_same_clock_replayed_events_cannot_be_three_episodes(self):
        a=adult('mother','Mother')
        past_work(a,1,event_ref='objective:work:first')
        past_work(a,1,event_ref='objective:work:second')
        e,ref=work_experience(clock=2)
        self.assertEqual(possible_recurrent_work_orientation(a,e,ref),[])

    def test_previous_work_in_other_site_is_not_portable_disposition(self):
        a=adult('mother','Mother')
        past_work(a,1,site='market')
        past_work(a,2,site='market')
        e,ref=work_experience(clock=3,site='home')
        self.assertEqual(possible_recurrent_work_orientation(a,e,ref),[])

    def test_no_personally_received_current_work_sign_is_not_an_episode(self):
        a=make_actor()
        for change in ('absent','wrong_speaker','wrong_kind','wrong_result'):
            e,ref=work_experience(clock=3)
            if change=='absent':e['perceived_cues']=[]
            if change=='wrong_speaker':
                e['perceived_cues'][0]['source_actor']='employer'
            if change=='wrong_kind':
                e['perceived_cues'][0]['kind']='public_notice_visible'
            if change=='wrong_result':
                e['status']='BLOCKED'
            with self.subTest(change=change):
                self.assertEqual(possible_recurrent_work_orientation(
                    a,e,ref),[])

    def test_unqualified_or_foreign_later_experience_cannot_form_person(self):
        a=make_actor()
        for change in ('not_participated','no_felt_work','not_work',
                       'foreign','clock_backward'):
            e,ref=work_experience(clock=3)
            if change=='not_participated':e['participated']=False
            if change=='no_felt_work':e['felt_enactment']={}
            if change=='not_work':e['own_action']='REST'
            if change=='foreign':e['actor']='father'
            if change=='clock_backward':e['clock']=1
            with self.subTest(change=change):
                if change in ('foreign',):
                    with self.assertRaises(ValueError):
                        possible_recurrent_work_orientation(a,e,ref)
                else:
                    self.assertEqual(possible_recurrent_work_orientation(
                        a,e,ref),[])

    def test_malicious_llm_cannot_forge_prior_work_or_change_operation(self):
        for scenario in ('fake_prior','fake_sign','wrong_operation'):
            a=make_actor();before=copy(a)
            e,ref,g=grounds(a)
            p=proposal(g[0])
            if scenario=='fake_prior':
                p['recurrent_work_practice'][
                    'prior_exercised_work_refs'][0]='invented'
            if scenario=='fake_sign':
                p['recurrent_work_practice'][
                    'current_received_work_sign_ref']='unseen'
            if scenario=='wrong_operation':
                p['operation']='IMPOSE'
            with self.subTest(scenario=scenario):
                with self.assertRaises(InvalidDevelopment):
                    admit(a,e,ref,[p])
                self.assertEqual(a,before)

    def test_missing_later_received_sign_cannot_ride_valid_prior_events(self):
        a=make_actor();before=copy(a)
        e,ref,g=grounds(a)
        p=proposal(g[0])
        p['perceived_cue_ref']='not_actual'
        with self.assertRaises(InvalidDevelopment):
            admit(a,e,ref,[p])
        self.assertEqual(a,before)

    def test_second_invalid_candidate_does_not_commit_first_work_orientation(self):
        a=make_actor();before=copy(a)
        e,ref,g=grounds(a)
        with self.assertRaises(InvalidDevelopment):
            admit(a,e,ref,[proposal(g[0]),{
                'kind':'ACQUIRE_HISTORICAL_ORIENTATION','operation':'IMPOSE',
                'perceived_cue_ref':'forged','orientation_mode':'APPROACH',
                'recurrent_work_practice':g[0]}])
        self.assertEqual(a,before)

    def test_fallback_does_not_deduce_moral_work_ethic_or_automatic_protest(self):
        a=make_actor()
        e,ref,g=grounds(a)
        out=HeuristicSemanticProvider().propose('development',{
            'experience':e,'actor':{'id':'mother'},
            'historically_possible_recurrent_livelihood_orientation':g})
        self.assertFalse(any(x.get('kind')=='ACQUIRE_HISTORICAL_ORIENTATION'
                             and x.get('recurrent_work_practice')
                             for x in out['candidates']))
        self.assertEqual(a['historical_orientations'],[])

    def test_real_runtime_delivers_its_own_work_history_to_development_model(self):
        # This is an actual SQLite/runtime/afterlife first consumer; the
        # scheduler is NOT entitled to declare the actor's reason for working.
        class ObservingSemantics:
            def __init__(self):
                self.base=ValidatingSemanticService()
                self.packet_history=[]
            def proposal(self,task,packet):
                if (task=='development' and
                        packet.get('actor',{}).get('id')=='mother'):
                    self.packet_history.append(copy(packet.get(
                        'historically_possible_recurrent_livelihood_orientation',[])))
                return self.base.proposal(task,packet)

        fake_parent={
            'source_ref':'r25_sourcefree_fictional_parent_not_PYAT',
            'source_grade':'SOURCEFREE_TEST_NOT_SURVEY_EVIDENCE',
            'answers':{'R25_SYNTHETIC':'NOT_A_RESPONDENT_ANSWER'},
            'fictional_seed':{'projects':[]}}
        with tempfile.TemporaryDirectory() as d:
            db=str(Path(d)/'r25_repeated_livelihood.sqlite3')
            semantic=ObservingSemantics()
            rt=ConstitutiveRuntime(db,semantic=semantic)
            rt.initialize([('father','Father',fake_parent),
                           ('mother','Mother',fake_parent)])
            try:
                for _ in range(3):
                    rt.step('mother',requested_action='WORK')
                self.assertEqual(len(semantic.packet_history),3)
                self.assertEqual(semantic.packet_history[0],[])
                self.assertEqual(semantic.packet_history[1],[])
                self.assertEqual(len(semantic.packet_history[2]),1)
                self.assertEqual(semantic.packet_history[2][0]
                                 ['possible_operation'],'WORK')
                self.assertEqual(len(rt.ledger.actor('mother')[1]
                                     ['historical_orientations']),0)
                self.assertTrue(rt.verify()['valid'])
            finally:
                rt.close()
            cold=ConstitutiveRuntime(db)
            try:
                self.assertTrue(cold.verify()['valid'])
                self.assertEqual(len(cold.ledger.actor('mother')[1]
                                     ['power_exercises']),3)
            finally:
                cold.close()

    def test_real_world_work_events_supply_lived_signs_without_hidden_wage_motive(self):
        a=adult('mother','Mother')
        world=blank_world()
        world['positions']['mother']='home'
        actors={'mother':a}
        latest=None
        for clock in (1,2,3):
            outcome=resolve(world,actors,Attempt(actor='mother',action='WORK'))
            self.assertIn(outcome.status,('PERFORMED','PARTIAL','BLOCKED'))
            cues=[c for c in actor_access(a,world).cues
                  if c.get('kind')=='performed_work'
                  and c.get('source_actor')=='mother']
            self.assertEqual(len(cues),1)
            experience={
                'actor':'mother','ref':f'lived:world:work:{clock}',
                'clock':world['clock'],'location':'home',
                'own_action':'WORK','participated':True,
                'status':outcome.status,
                'felt_enactment':{'attempted_operation':'WORK'},
                'perceived_cues':copy(cues)}
            event_ref=stable_id('objective_work_fixture',{
                'world_clock':world['clock'],'action':clock})
            if clock<3:
                retain_exercised_power(a,experience,event_ref,'home')
            else:
                latest=possible_recurrent_work_orientation(
                    a,experience,event_ref)
        self.assertEqual(len(latest),1)
        self.assertEqual(latest[0]['possible_operation'],'WORK')
        self.assertTrue(latest[0][
            'no_employer_intention_or_wage_account_knowledge_imputed'])

if __name__=='__main__':
    unittest.main()
