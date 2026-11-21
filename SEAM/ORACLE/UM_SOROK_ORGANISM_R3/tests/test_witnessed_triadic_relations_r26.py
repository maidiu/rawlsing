"""R26: world-owned directed conduct -> distinct third-party lived relation models.

Sourcefree research-only. Execute at the exact candidate Git SHA; do not
interpret a passing fixture as scientific psychology or native actor authority.
"""
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.types import Attempt, adult, blank_world, copy
from um_sorok_organism.world import resolve
from um_sorok_organism.constitution import actor_access
from um_sorok_organism.relational_metabolism import (
    possible_witnessed_third_party_relation,
)
from um_sorok_organism.development import admit, InvalidDevelopment
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import (
    CallbackLLMProvider, HeuristicSemanticProvider, ValidatingSemanticService,
)


def family():
    persons = {aid: adult(aid, aid.title()) for aid in
               ('father', 'mother', 'nadia', 'brother')}
    world = blank_world()
    world['positions'] = {aid: 'home' for aid in persons}
    return world, persons


def witness_experience(actor_id, access):
    cues = [c for c in access.cues
            if c.get('kind')=='performed_impose']
    return {'actor':actor_id, 'ref':'experience:'+actor_id,
            'participated':False,'status':'OBSERVED',
            'reciprocated_partner':None,'perceived_cues':cues}


def reinterpretation(occasion, hypothesis):
    return {'kind':'CHANGE_OTHER_MODEL',
            'other_ref':occasion['source_actor_ref'],
            'about_relation_with_ref':occasion['target_actor_ref'],
            'witnessed_cue_ref':occasion['witnessed_cue_ref'],
            'hypothesis':hypothesis}


class WitnessedTriadicRelationsR26(unittest.TestCase):
    def test_actual_directed_world_act_supplies_bounded_public_target(self):
        world, actors = family()
        done = resolve(world,actors,Attempt('father','IMPOSE',target='mother'))
        self.assertEqual(done.status,'PERFORMED')
        access = actor_access(actors['nadia'],world)
        occasions = possible_witnessed_third_party_relation(
            actors['nadia'],witness_experience('nadia',access))
        self.assertEqual(len(occasions),1)
        self.assertEqual(occasions[0]['source_actor_ref'],'father')
        self.assertEqual(occasions[0]['target_actor_ref'],'mother')
        self.assertEqual(occasions[0]['witnessed_act'],'IMPOSE')
        self.assertTrue(occasions[0]['no_mandatory_revaluation'])
        self.assertEqual(len(world['relations']['rel:father:mother']['history']),1)
        self.assertTrue(world['relations']['rel:father:mother']['history'][0][
            'not_consent_or_private_psychological_meaning'])
        self.assertNotIn('consent',occasions[0])
        self.assertNotIn('psychological_truth',occasions[0])

    def test_both_siblings_can_form_different_personal_reinterpretations(self):
        world, actors=family()
        actors['nadia']['other_models']['father']=[
            {'hypothesis':'I admire how he supports our family'}]
        actors['brother']['other_models']['father']=[
            {'hypothesis':'I doubt his promises'}]
        resolve(world,actors,Attempt('father','IMPOSE',target='mother'))
        before=copy(world)
        n_exp=witness_experience('nadia',actor_access(actors['nadia'],world))
        b_exp=witness_experience('brother',actor_access(actors['brother'],world))
        n=possible_witnessed_third_party_relation(actors['nadia'],n_exp)[0]
        b=possible_witnessed_third_party_relation(actors['brother'],b_exp)[0]
        self.assertNotEqual(
            n['prior_source_models_actor_hypotheses_only'],
            b['prior_source_models_actor_hypotheses_only'])
        admit(actors['nadia'],n_exp,'event:1',[
            reinterpretation(n,'I now question his treatment of mother')])
        admit(actors['brother'],b_exp,'event:1',[
            reinterpretation(b,'I see a conflict but still identify with him')])
        self.assertEqual(actors['nadia']['other_models']['father'][-1][
            'about_relation_with_ref'],'mother')
        self.assertNotEqual(
            actors['nadia']['other_models']['father'][-1]['hypothesis'],
            actors['brother']['other_models']['father'][-1]['hypothesis'])
        self.assertEqual(world,before)
        self.assertNotIn('mother',actors['nadia']['other_models'])

    def test_no_witness_cannot_be_upgraded_to_third_person_knowledge(self):
        world,actors=family()
        evidence={'actor':'nadia','ref':'exp:invented','participated':False,
                  'reciprocated_partner':None,
                  'perceived_cues':[{
                      'id':'claim','kind':'performed_impose',
                      'source_actor':'father','actor_accessible_target_ref':'mother'}]}
        proposal={'kind':'CHANGE_OTHER_MODEL','other_ref':'father',
                  'about_relation_with_ref':'mother',
                  'witnessed_cue_ref':'claim',
                  'hypothesis':'He did this to mother'}
        prior=copy(actors['nadia'])
        with self.assertRaisesRegex(InvalidDevelopment,'THIRD_PARTY_RELATION_NOT_ACTOR_WITNESSED'):
            admit(actors['nadia'],evidence,'event:invented',[proposal])
        self.assertEqual(actors['nadia'],prior)

    def test_wrong_target_source_or_cue_cannot_pass_and_admission_is_atomic(self):
        world,actors=family()
        resolve(world,actors,Attempt('father','IMPOSE',target='mother'))
        exp=witness_experience('nadia',actor_access(actors['nadia'],world))
        occ=possible_witnessed_third_party_relation(actors['nadia'],exp)[0]
        legitimate=reinterpretation(occ,'I am uncertain')
        prior=copy(actors['nadia'])
        for bad in (
            {**legitimate,'about_relation_with_ref':'brother'},
            {**legitimate,'other_ref':'brother'},
            {**legitimate,'witnessed_cue_ref':'wrong'},
            {**legitimate,'about_relation_with_ref':'nadia'},
        ):
            with self.assertRaises(InvalidDevelopment):
                admit(actors['nadia'],exp,'event:2',[legitimate,bad])
            self.assertEqual(actors['nadia'],prior)

    def test_absent_target_is_not_forged_as_a_witnessed_relation(self):
        world,actors=family()
        world['positions']['mother']='hall'
        outcome=resolve(world,actors,Attempt('father','CARE',target='mother'))
        self.assertEqual(outcome.status,'PARTIAL')
        access=actor_access(actors['nadia'],world)
        candidate=possible_witnessed_third_party_relation(
            actors['nadia'],{'actor':'nadia','perceived_cues':access.cues})
        self.assertEqual(candidate,[])
        self.assertEqual(world['relations'],{})

    def test_real_runtime_uses_one_world_event_and_actor_local_semantic_proposal(self):
        fallback=HeuristicSemanticProvider()
        seen=[]
        def provider(task,packet):
            if task=='development' and packet['actor']['id']=='sister':
                occasions=packet['historically_possible_witnessed_third_party_relations']
                if occasions:
                    seen.extend(copy(occasions))
                    return {'task':task,'candidates':[
                        reinterpretation(occasions[0],
                            'I may have misunderstood their relationship')]}
            return fallback.propose(task,packet)
        packets=[(aid,aid.title(),{'answers':{'sample':'fictional-only'}})
                 for aid in ('father','mother','sister')]
        with tempfile.TemporaryDirectory() as folder:
            rt=ConstitutiveRuntime(
                Path(folder)/'triad.sqlite',
                semantic=ValidatingSemanticService(CallbackLLMProvider(provider)))
            try:
                rt.initialize(packets)
                rt.step('father',requested_action='IMPOSE',target='mother')
                self.assertEqual(len(seen),1)
                self.assertEqual(seen[0]['source_actor_ref'],'father')
                self.assertEqual(seen[0]['target_actor_ref'],'mother')
                witness=rt.snapshot('sister')['other_models']
                self.assertEqual(witness['father'][-1][
                    'about_relation_with_ref'],'mother')
                self.assertTrue(witness['father'][-1][
                    'not_other_private_state_or_target_consent'])
                self.assertNotIn('father',rt.snapshot('nadia')['other_models'])
                self.assertTrue(rt.verify()['valid'])
            finally:
                rt.close()


if __name__=='__main__':
    unittest.main()
