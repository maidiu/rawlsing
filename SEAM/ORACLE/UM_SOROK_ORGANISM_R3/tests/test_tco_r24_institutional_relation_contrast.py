"""R24 three-agent MULCH: different lived institutional occasions can revalue
already acquired psychic relations without imposing a political revelation.

This sourcefree fixture exercises the EXISTING institutional-expectation,
relational, actor-access, world and typed development owners. R24 neither
attributes an employer's hidden motives nor certifies the actor's moral view.
"""
import unittest
from dataclasses import asdict

from um_sorok_organism.types import adult, blank_world, Attempt, copy
from um_sorok_organism.world import resolve
from um_sorok_organism.constitution import actor_access
from um_sorok_organism.development import admit, InvalidDevelopment
from um_sorok_organism.relational_metabolism import link_ref
from um_sorok_organism.institutional_procedure_learning import (
    admit_public_procedure_expectation,
    possible_lived_institutional_differences,
    qualify_lived_institutional_difference,
)
from um_sorok_organism.semantics import (
    ValidatingSemanticService, CallbackLLMProvider, HeuristicSemanticProvider,
)

def old_public_practice(actor, event='objective:old_public_result'):
    actor['notice_exposures']=[{
        'public_notice_ref':'notice:personally_inspected',
        'inspected_at_clock':1,'public_words_available':['public_petition']}]
    actor['power_exercises']=[{
        'id':'personally_signed_petition',
        'operation':'SIGN_FOOD_PETITION',
        'attempt_status_analyst_receipt':'PERFORMED',
        'event_clock':2}]
    past={'actor':actor['id'],'ref':'experience:old',
          'clock':2,'perceived_cues':[{
              'kind':'performed_sign_food_petition',
              'description':'COLLECTIVE_FOOD_ACCESS_RIGHTS_CHANGED',
              'id':'cue:received_public_change'}]}
    proposal={
        'received_public_sign_ref':'cue:received_public_change',
        'own_signature_exercise_ref':'personally_signed_petition',
        'inspected_notice_ref':'notice:personally_inspected',
        'scope':'POSTED_INSTITUTIONAL_PROCEDURE'}
    report=admit_public_procedure_expectation(actor,past,event,proposal)
    assert report['kind']=='ACQUIRE_SITUATED_PUBLIC_PROCEDURE_EXPECTATION'
    return actor['institutional_expectations'][0]

def actor_with_history():
    a=adult('mother','Mother')
    a['forms']={
        'care':{'id':'care','actor':'mother','kind':'RELATIONAL_INVESTMENT',
                'origin':['actual_prior_lived_care'],'enables':['CARE'],
                'cues':['institution'],'scope':{},'lifecycle':'ACTIVE',
                'strength':.6,'body_min':0,'access':'tacit'},
        'authority':{'id':'authority','actor':'mother','kind':'MEDIATOR',
                'origin':['actual_prior_institutional_practice'],
                'enables':['SIGN_HALL_PETITION'],'cues':['institution'],
                'scope':{},'lifecycle':'ACTIVE','strength':.6,
                'body_min':0,'access':'tacit'}}
    a['links']=[{
        'source':'care','target':'authority','relation':'SUBORDINATES',
        'contexts':['hall'],'origin':['objective:prior_lived_relationship']}]
    old_public_practice(a)
    return a

def later_experience(actor='mother', *, event_ref='objective:later_blocked_hall',
                     speaker='mother',kind='performed_open_hall',
                     outcome='ATTEMPT_NOT_COMPLETED',clock=4):
    return {
        'actor':actor,'ref':'experience:later_hall',
        'clock':clock,'location':'hall',
        'perceived_cues':[{
            'id':'cue:later_unfinished_hall','kind':kind,
            'description':outcome,'source_actor':speaker}],
        'participated':True,'own_action':'OPEN_HALL','status':'BLOCKED',
        'felt_enactment':{'attempted_operation':'OPEN_HALL'}}

def proposed_revaluation(a,grounds):
    return {'kind':'REVALUE_RELATION',
            'relation_id':link_ref(a['links'][0]),
            'new_relation':'CONFLICTS_WITH',
            'lived_institutional_difference':{
                'prior_expectation_ref':grounds[0]['prior_expectation_ref'],
                'later_received_sign_ref':grounds[0]['later_received_sign_ref']}}


class InstitutionalContrastMulchR24(unittest.TestCase):
    def test_old_owner_qualified_public_practice_then_later_lived_difference(self):
        a=actor_with_history();later=later_experience()
        grounds=possible_lived_institutional_differences(
            a,later,'objective:later_blocked_hall')
        self.assertEqual(len(grounds),1)
        self.assertEqual(grounds[0]['prior_expectation_ref'],
                         a['institutional_expectations'][0]['id'])
        self.assertTrue(grounds[0]['no_necessary_ideological_conclusion'])
        self.assertEqual(grounds[0]['causal_source_of_later_obstruction'],
                         'NOT_KNOWN')
        receipt=qualify_lived_institutional_difference(
            a,later,'objective:later_blocked_hall',
            proposed_revaluation(a,grounds)['lived_institutional_difference'])
        self.assertEqual(receipt['later_perceived_source_actor_ref'],'mother')
        self.assertTrue(receipt['institutional_cause_not_concluded'])
        self.assertEqual(receipt['later_personal_experience_ref'],later['ref'])

    def test_two_event_relation_revaluation_becomes_historical_actor_causality(self):
        a=actor_with_history();before=copy(a['links'][0])
        later=later_experience()
        grounds=possible_lived_institutional_differences(
            a,later,'objective:later_blocked_hall')
        out=admit(a,later,'objective:later_blocked_hall',
                  [proposed_revaluation(a,grounds)])
        self.assertEqual(out[0]['status'],
                         'ADMITTED_SOURCEFREE_RELATIONAL_REVALUATION')
        link=a['links'][0]
        self.assertEqual(link['relation'],'CONFLICTS_WITH')
        self.assertEqual(link['origin'],before['origin'])
        self.assertEqual(link['relational_history'][0]['relation'],
                         'SUBORDINATES')
        difference=link['relational_history'][0]['lived_institutional_difference']
        self.assertEqual(difference['earlier_personal_experience_ref'],
                         'experience:old')
        self.assertEqual(difference['later_personal_experience_ref'],
                         later['ref'])
        self.assertTrue(difference['actor_moral_conclusion_not_imposed'])

    def test_same_objective_blockage_can_have_different_psychic_afterlife(self):
        a=actor_with_history();b=actor_with_history()
        later=later_experience()
        choose=proposed_revaluation(a,possible_lived_institutional_differences(
            a,later,'objective:later_blocked_hall'))
        admit(a,later,'objective:later_blocked_hall',[choose])
        # Another person can remain attached to the earlier learned sense,
        # or a model can abstain; no identical political discovery required.
        self.assertEqual(a['links'][0]['relation'],'CONFLICTS_WITH')
        self.assertEqual(b['links'][0]['relation'],'SUBORDINATES')
        self.assertEqual(b['links'][0].get('relational_history',[]),[])

    def test_llm_callback_selects_hypothesis_only_after_institutional_source(self):
        a=actor_with_history();later=later_experience()
        grounds=possible_lived_institutional_differences(
            a,later,'objective:later_blocked_hall')
        model=ValidatingSemanticService(CallbackLLMProvider(
            lambda task,packet:{
                'task':task,
                'candidates':[proposed_revaluation(a,packet[
                    'historically_possible_institutional_relational_differences'])]
            }))
        packet={'actor':{'id':'mother'},'experience':later,
                'historically_possible_institutional_relational_differences':
                    grounds}
        proposal=model.proposal('development',packet)
        self.assertEqual(a['links'][0]['relation'],'SUBORDINATES')
        admitted=admit(a,later,'objective:later_blocked_hall',
                       proposal['candidates'])
        self.assertEqual(admitted[0]['kind'],'REVALUE_RELATION')
        self.assertEqual(a['links'][0]['relation'],'CONFLICTS_WITH')

    def test_old_heuristic_does_not_invent_compulsory_moral_revision(self):
        a=actor_with_history();later=later_experience()
        packet={'actor':{'id':'mother'},'experience':later,
                'historically_possible_institutional_relational_differences':
                    possible_lived_institutional_differences(
                        a,later,'objective:later_blocked_hall')}
        proposed=HeuristicSemanticProvider().propose('development',packet)
        self.assertFalse(any(c['kind']=='REVALUE_RELATION'
                             for c in proposed['candidates']))
        self.assertEqual(a['links'][0]['relation'],'SUBORDINATES')

    def test_no_prior_public_practice_gives_no_historic_institutional_contrast(self):
        a=actor_with_history();a['institutional_expectations']=[]
        self.assertEqual(possible_lived_institutional_differences(
            a,later_experience(),'objective:later_blocked_hall'),[])

    def test_no_private_inspection_or_own_signature_cannot_be_forged(self):
        for history in ('notice_exposures','power_exercises'):
            a=actor_with_history()
            a[history]=[]
            with self.subTest(missing=history):
                self.assertEqual(possible_lived_institutional_differences(
                    a,later_experience(),'objective:later_blocked_hall'),[])
                with self.assertRaisesRegex(
                        ValueError,'R24_UNQUALIFIED_LIVED_INSTITUTIONAL_DIFFERENCE'):
                    qualify_lived_institutional_difference(
                        a,later_experience(),'objective:later_blocked_hall',{
                            'prior_expectation_ref':'invented',
                            'later_received_sign_ref':'cue:later_unfinished_hall'})

    def test_not_the_same_event_and_not_past_clock_cannot_reinterpret(self):
        a=actor_with_history()
        e=later_experience(clock=2)
        self.assertEqual(possible_lived_institutional_differences(
            a,e,'objective:later_blocked_hall'),[])
        e=later_experience(clock=4)
        self.assertEqual(possible_lived_institutional_differences(
            a,e,'objective:old_public_result'),[])

    def test_unqualified_ambient_sign_and_unobserved_other_do_not_count(self):
        for kind,speaker in (
                ('coactor_present','mother'),
                ('public_notice_visible','mother'),
                ('performed_open_hall',None)):
            a=actor_with_history()
            e=later_experience(kind=kind,speaker=speaker)
            with self.subTest(kind=kind,speaker=speaker):
                self.assertEqual(possible_lived_institutional_differences(
                    a,e,'objective:later_blocked_hall'),[])

    def test_no_proof_of_contrast_when_new_practice_succeeds(self):
        a=actor_with_history()
        e=later_experience(outcome='HALL_OPENED')
        self.assertEqual(possible_lived_institutional_differences(
            a,e,'objective:later_open_hall'),[])

    def test_absent_actor_linguistic_means_do_not_impute_institutional_theory(self):
        a=actor_with_history()
        a['body']['language']=0.05
        self.assertEqual(possible_lived_institutional_differences(
            a,later_experience(),'objective:later_blocked_hall'),[])

    def test_forged_proposal_fails_atomically_even_with_valid_old_history(self):
        a=actor_with_history();before=copy(a)
        e=later_experience()
        forged={'kind':'REVALUE_RELATION',
                'relation_id':link_ref(a['links'][0]),
                'new_relation':'CONFLICTS_WITH',
                'lived_institutional_difference':{
                    'prior_expectation_ref':'fictional_older_success',
                    'later_received_sign_ref':'cue:later_unfinished_hall'}}
        with self.assertRaisesRegex(
                InvalidDevelopment,
                'R24_UNQUALIFIED_LIVED_INSTITUTIONAL_DIFFERENCE'):
            admit(a,e,'objective:later_blocked_hall',[forged])
        self.assertEqual(a,before)

    def test_qualified_contrast_does_not_allow_same_relation_as_revaluation(self):
        a=actor_with_history();before=copy(a)
        e=later_experience()
        claim=proposed_revaluation(a,possible_lived_institutional_differences(
            a,e,'objective:later_blocked_hall'))
        claim['new_relation']='SUBORDINATES'
        with self.assertRaisesRegex(
                InvalidDevelopment,'R24_NOT_A_LATER_RELATIONAL_REVALUATION'):
            admit(a,e,'objective:later_blocked_hall',[claim])
        self.assertEqual(a,before)

    def test_second_invalid_development_cannot_commit_first_relation_change(self):
        a=actor_with_history();before=copy(a)
        e=later_experience()
        proposal=proposed_revaluation(
            a,possible_lived_institutional_differences(
                a,e,'objective:later_blocked_hall'))
        with self.assertRaises(InvalidDevelopment):
            admit(a,e,'objective:later_blocked_hall',[
                proposal,{'kind':'REVALUE_RELATION',
                          'relation_id':'forged_unacquired_relation',
                          'new_relation':'SUPPORTS'}])
        self.assertEqual(a,before)

    def test_world_owned_hall_restriction_can_make_live_personal_contrast(self):
        a=actor_with_history()
        world=blank_world()
        # The actor's earlier personally received public outcome was at
        # clock 2; the later world cannot start back at clock 0.
        world['clock']=3
        world['positions']['mother']='hall'
        outcome=resolve(world,{'mother':a},
                        Attempt(actor='mother',action='OPEN_HALL'))
        self.assertEqual(outcome.status,'BLOCKED')
        self.assertEqual(outcome.objective_description,
                         'NO_INSTITUTIONAL_AUTHORITY')
        witnessed=actor_access(a,world)
        signs=[x for x in witnessed.cues
               if x['kind']=='performed_open_hall']
        self.assertEqual(len(signs),1)
        self.assertEqual(signs[0]['description'],'ATTEMPT_NOT_COMPLETED')
        later={'actor':'mother','ref':'experience:actual_world_hall',
               'clock':world['clock'],'location':'hall',
               'own_action':'OPEN_HALL','status':'BLOCKED','participated':True,
               'perceived_cues':copy(signs)}
        contrasts=possible_lived_institutional_differences(
            a,later,'objective:actual_blocked_hall')
        self.assertEqual(len(contrasts),1)
        self.assertTrue(contrasts[0][
            'does_not_prove_same_institution_or_legitimate_authority'])
        self.assertEqual(world['sites']['hall']['access'],'controlled')


if __name__=='__main__':
    unittest.main()
