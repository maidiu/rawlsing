"""Collective praxis: actual independently authored contributions change a
material permission and its later first consumer, without a shared psyche.
"""
from copy import deepcopy
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[3]
for p in (ROOT/'SEAM'/'ORACLE'/'UM_SOROK_ORGANISM_R3',
          ROOT/'WORKER_RETURNS'/'SOROK-P5-CONTINUOUS-EXPERIENCE-R1',
          ROOT/'WORKER_RETURNS'/'SOROK-P6-ONE-LIVING-HOUSE-R1',
          ROOT/'WORKER_RETURNS'/'SOROK-P4-CORE-LOOP-R1',
          ROOT, ROOT/'SEAM'/'NEIGHBORMULCH'):
    sys.path.insert(0,str(p))
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult, blank_world
from um_sorok_organism.semantics import (
    CallbackLLMProvider, ValidatingSemanticService, HeuristicSemanticProvider)
from neighbor_runtime import NeighborEncounter, EncounterRefusal
import mii


def policy(sign):
    fallback=HeuristicSemanticProvider()
    def callback(task,packet):
        if task=='actor_attempt':
            available={o['action'] for o in packet['options']}
            return {'task':task,'action':'SIGN_HALL_PETITION'
                    if sign and 'SIGN_HALL_PETITION' in available else 'WAIT'}
        if task=='development':
            return {'task':task,'candidates':[]}
        return fallback.propose(task,packet)
    return ValidatingSemanticService(CallbackLLMProvider(callback))


class CollectiveAccessR14(unittest.TestCase):
    def build(self,name,*,rule=None):
        tmp=tempfile.TemporaryDirectory(prefix='neighbor_r14_')
        self.addCleanup(tmp.cleanup)
        db=str(Path(tmp.name)/'world.sqlite')
        rt=ConstitutiveRuntime(db,world_id=name)
        self.addCleanup(rt.close)
        world=blank_world(name)
        world['neighbor_routes']={'workshop':['hall','home'],'hall':['workshop'],
                                  'home':['workshop']}
        if rule is not None:
            world['institutional_access_rules'].append(rule)
        world['public_notices'].append({
            'id':'hall-public-notice','location':'workshop','public':True,
            'effective_from':0,'effective_until':None,
            'public_text':'Petition: two distinct contributions open the hall.',
            'public_terms':['petition','hall']})
        rt.ledger.initialize(world,[adult('worker','Mara','workshop'),
                                   adult('elsewhere','Lea','home')])
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({
            'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{loc:{'light':'lit','sightline':'unobstructed',
                'hearing':True,'sound_path':'audible','legibility':'readable'}
                for loc in ('workshop','home','hall')},
            'actor_conditions':{a:{'facing':'entrance','visual':True,'light':'lit',
                'sightline':'unobstructed','hearing':True,'sound_path':'audible'}
                for a in ('worker','elsewhere')}},request_id='geometry')
        self.assertEqual(n.contribute('arrive','MOVE',destination='workshop')['status'],'PERFORMED')
        self.assertEqual(n.contribute('look','LOOK',target_object_ref='hall-public-notice')['status'],'PERFORMED')
        self.assertIn('two distinct',n.private_surface(n.new_private_profile(),
            command='look',target='hall-public-notice')['optional']['text'])
        self.assertEqual(n.contribute('before','MOVE',destination='hall')['status'],'BLOCKED')
        return rt,n,db

    def test_independent_contributions_change_actual_access_not_shared_motive(self):
        for actor_sign,user_sign in ((True,True),(False,True),(True,False)):
            with self.subTest(actor=actor_sign,user=user_sign):
                name='branch'+str(actor_sign)+str(user_sign)
                rt,n,db=self.build(name)
                rt.semantic=policy(actor_sign)
                result=n.independent_actor_beat('worker')
                self.assertEqual(result['attempt'],'SIGN_HALL_PETITION' if actor_sign else 'WAIT')
                self.assertNotEqual(result['selection_grade'],'INJECTED_NOT_NATIVE_ACTOR_CHOICE')
                before=deepcopy(rt.ledger.actors())
                turn=n.contribute('human','SIGN_HALL_PETITION' if user_sign else 'WAIT')
                self.assertEqual(turn['status'],'PERFORMED')
                self.assertEqual(rt.ledger.actors(),before)
                world=rt.ledger.world(name)[1]
                board=world['institutions']['hall_board']
                expected=actor_sign and user_sign
                self.assertEqual(len(board['hall_petition_signatures']),int(actor_sign)+int(user_sign))
                self.assertEqual(world['sites']['hall']['access'],'public' if expected else 'controlled')
                self.assertEqual(len(board['rule_history']),int(expected))
                count=rt.verify()['events']
                self.assertTrue(n.contribute('human','SIGN_HALL_PETITION' if user_sign else 'WAIT')['idempotent_replay'])
                self.assertEqual(rt.verify()['events'],count)
                if user_sign:
                    self.assertEqual(n.contribute('duplicate','SIGN_HALL_PETITION')['status'],'BLOCKED')
                    self.assertEqual(len(rt.ledger.world(name)[1]['institutions']['hall_board']['hall_petition_signatures']),
                                     int(actor_sign)+int(user_sign))
                rt.close()
                cold=ConstitutiveRuntime(db,world_id=name)
                self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                self.assertEqual(nn.contribute('after','MOVE',destination='hall')['status'],
                                 'PERFORMED' if expected else 'BLOCKED')
                # An absent non-signatory receives the actual changed right,
                # not the propositional knowledge or intentions of signers.
                self.assertEqual(cold.ledger.actor('elsewhere')[1],before['elsewhere'])
                later=cold.step('elsewhere',requested_action='MOVE',object_ref='hall')
                self.assertEqual(later['status'],'PERFORMED' if expected else 'BLOCKED')
                self.assertTrue(cold.verify()['valid'])

    def test_structural_rule_blocks_actual_human_contribution_despite_visible_notice(self):
        rule={'id':'sourcefree-exclusion','source_ref':'fixture-rule',
              'operation':'SIGN_HALL_PETITION','location':'workshop',
              'all_of':[{'kind':'RECORDED_POSITION','field':'eligibility','equals':'member'}]}
        rt,n,_=self.build('excluded',rule=rule)
        before=deepcopy(rt.ledger.world('excluded')[1]['institutions'])
        result=n.contribute('sign','SIGN_HALL_PETITION')
        self.assertEqual(result['status'],'BLOCKED')
        self.assertEqual(result['potential_actor_evidence'],[])
        self.assertEqual(rt.ledger.world('excluded')[1]['institutions'],before)
        with self.assertRaisesRegex(EncounterRefusal,'USER_CANNOT_IMPERSONATE_ACTOR'):
            NeighborEncounter(rt,'worker',mii_module=mii)
        self.assertTrue(rt.verify()['valid'])


if __name__=='__main__':
    unittest.main()
