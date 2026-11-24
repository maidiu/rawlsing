"""Actual human material conduct -> independently constituted actor's lived
inspection -> controlled semantic investment -> future actual recruitment.
Matched grant/denial; no assertion of general psychology or live LLM behavior.
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


class MaterialParticipationR13(unittest.TestCase):
    def build(self, name, granted, *, observer_facing='entrance', world_setup=None):
        tmp=tempfile.TemporaryDirectory(prefix='neighbor_r13_')
        self.addCleanup(tmp.cleanup)
        db=str(Path(tmp.name)/'world.sqlite')
        rt=ConstitutiveRuntime(db,world_id=name)
        self.addCleanup(rt.close)
        world=blank_world(name)
        world['sites']['workshop']['material_use_grants']=['worker']+(
            ['visitor'] if granted else [])
        if world_setup is not None:
            world_setup(world)
        rt.ledger.initialize(world,[adult('worker','Mara','workshop')])
        made=rt.step('worker',requested_action='MAKE_OBJECT')
        self.assertEqual(made['status'],'PERFORMED')
        obj=rt.ledger.world(name)[1]['public_history'][-1]['worked_material_object_ref']
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({
            'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{loc:{'light':'lit','sightline':'unobstructed',
                 'hearing':True,'sound_path':'audible','legibility':'readable'}
                 for loc in ('workshop','home')},
            'actor_conditions':{'worker':{'facing':observer_facing,'visual':True,
                'light':'lit','sightline':'unobstructed','hearing':True,
                'sound_path':'audible'}},
        },request_id='geometry')
        n.contribute('arrive','MOVE',destination='workshop')
        return rt,n,db,obj

    @staticmethod
    def semantic(stage):
        fallback=HeuristicSemanticProvider()
        def callback(task,packet):
            if task=='actor_attempt':
                if stage=='inspect':
                    options=[a for a in packet['practical_options']
                             if a['operation']=='INSPECT' and
                             a.get('grounds_status')=='PRESENT_MATERIAL_OBJECT_NOT_ASSUMED_MOTIVE']
                    if len(options)!=1:
                        raise AssertionError('Expected actual issued object inspection')
                    return {'task':task,'action':'INSPECT',
                            'practical_option_id':options[0]['option_id']}
                options=[a for a in packet['practical_options']
                         if a['operation']=='REPAIR' and
                         a.get('acquired_object_orientations')==['SUSTAIN']]
                if options:
                    return {'task':task,'action':'REPAIR',
                            'practical_option_id':options[0]['option_id']}
                return {'task':task,'action':'WAIT'}
            if task=='development':
                candidates=[]
                if stage=='inspect':
                    for cue in packet['experience'].get('perceived_cues',[]):
                        if cue.get('kind')=='performed_inspect' and (
                                'apparently_repaired' in cue.get('tags',[])):
                            candidates.append({'kind':'INVEST_MATERIAL_OBJECT',
                                'material_object_ref':cue['material_object_ref'],
                                'orientation':'SUSTAIN'})
                return {'task':task,'candidates':candidates}
            return fallback.propose(task,packet)
        return ValidatingSemanticService(CallbackLLMProvider(callback))

    def test_actual_grant_controls_material_effect_and_later_actor_recruitment(self):
        for grant in (True,False):
            with self.subTest(grant=grant):
                name='granted' if grant else 'denied'
                rt,n,db,ref=self.build(name,grant)
                before=deepcopy(rt.ledger.world(name)[1])
                actor_before=deepcopy(rt.ledger.actors())
                result=n.contribute('repair','REPAIR',target_object_ref=ref)
                self.assertEqual(result['status'],'PERFORMED' if grant else 'BLOCKED')
                world=rt.ledger.world(name)[1]
                obj=world['material_objects'][ref]
                self.assertEqual(obj['condition'],.8 if grant else .56)
                self.assertEqual(world['sites']['workshop']['stock'],
                    before['sites']['workshop']['stock']-(1 if grant else 0))
                self.assertEqual(obj['owner'],'workshop_steward')
                self.assertEqual(obj['maker'],'worker')
                self.assertEqual(rt.ledger.actors(),actor_before)
                self.assertNotIn('visitor',rt.ledger.actors())
                self.assertEqual(len(result['potential_actor_evidence']),1 if grant else 0)
                if grant:
                    self.assertEqual(obj['objective_labor_history'][-1]['actor'],'visitor')
                    self.assertEqual(obj['objective_labor_history'][-1]['clock'],world['clock'])
                count=rt.verify()['events']
                repeat=n.contribute('repair','REPAIR',target_object_ref=ref)
                self.assertTrue(repeat['idempotent_replay'])
                self.assertEqual(rt.verify()['events'],count)
                with self.assertRaisesRegex(EncounterRefusal,'REQUEST_REPLAY_CHANGED_PAYLOAD'):
                    n.contribute('repair','REPAIR',target_object_ref='different')
                # User has no power to specify the actor response. Both arms
                # use the same controlled actor-side semantic inspection policy.
                rt.semantic=self.semantic('inspect')
                actual=n.independent_actor_beat('worker')
                self.assertEqual(actual['status'],'PERFORMED')
                self.assertEqual(actual['attempt'],'INSPECT')
                self.assertNotEqual(actual['selection_grade'],'INJECTED_NOT_NATIVE_ACTOR_CHOICE')
                actor=rt.ledger.actor('worker')[1]
                encounters=[r for r in actor['object_encounters']
                            if r.get('personally_attempted_operation')=='INSPECT']
                self.assertTrue(encounters)
                self.assertIn('apparently_repaired' if grant else 'visibly_worn',
                              encounters[-1]['received_public_description'])
                inv=actor.get('material_investments',[])
                self.assertEqual(len(inv),1 if grant else 0)
                rt.close()
                cold=ConstitutiveRuntime(db,world_id=name,semantic=self.semantic('recruit'))
                self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                subsequent=nn.independent_actor_beat('worker')
                self.assertEqual(subsequent['attempt'],'REPAIR' if grant else 'WAIT')
                self.assertNotEqual(subsequent['selection_grade'],'INJECTED_NOT_NATIVE_ACTOR_CHOICE')
                self.assertEqual(cold.ledger.world(name)[1]['material_objects'][ref]['condition'],
                                 1.0 if grant else .56)
                self.assertTrue(cold.verify()['valid'])
                nn.contribute('look','LOOK',target_object_ref=ref)
                view=nn.private_surface(nn.new_private_profile(),command='look',target=ref)
                self.assertEqual(view['optional']['text'],
                                 'It appears sound.' if grant else 'It appears worn.')
                self.assertNotIn('material_investments',str(view))
                self.assertNotIn('workshop_steward',str(view))

    def test_actual_repair_not_automatic_actor_access(self):
        rt,n,_,ref=self.build('unseen',True,observer_facing='away')
        before=deepcopy(rt.ledger.actors())
        result=n.contribute('repair','REPAIR',target_object_ref=ref)
        self.assertEqual(result['status'],'PERFORMED')
        self.assertEqual(result['potential_actor_evidence'],[])
        self.assertEqual(rt.ledger.actors(),before)
        self.assertFalse(any(c['kind']=='visitor_material_work'
                             for c in rt.see('worker')['cues']))
        self.assertEqual(rt.ledger.world('unseen')[1]['material_objects'][ref]['condition'],.8)
        self.assertTrue(rt.verify()['valid'])


if __name__=='__main__':
    unittest.main()
