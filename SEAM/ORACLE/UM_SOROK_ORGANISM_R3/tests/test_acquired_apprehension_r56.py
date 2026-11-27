"""An acquired way of attending changes an actual later choice BEFORE formation.

Sourcefree callback policy, not evidence of human learning or live-model
discovery. Same objective conduct, same accessible current material sign,
different prior acquisition. No new action, memory, explicit concept or goal.
"""
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import (
    CallbackLLMProvider, ValidatingSemanticService, HeuristicSemanticProvider)
from test_cultural_mediation_r3 import SEED

class AcquiredApprehension(unittest.TestCase):
    def arm(self,db,acquire,*,different_maker=False,expire=False,forge=False):
        phase={'old':True}
        observed=[]
        def cb(task,packet):
            if task=='adult_constructor':
                return HeuristicSemanticProvider().propose(task,packet)
            if task=='development':
                return {'task':task,'candidates':(
                    packet.get('historically_possible_cultural_references',[])
                    if phase['old'] and acquire and packet['actor']['id']=='nadia'
                    else [])}
            if task=='actor_attempt':
                if phase['old']:
                    return HeuristicSemanticProvider().propose(task,packet)
                rows=[o for o in packet.get('practical_options',[])
                      if o.get('cross_object_attention_analytic_only')]
                if rows:
                    return {'task':task,'practical_option_id':(
                        'forged' if forge else rows[0]['option_id'])}
                return {'task':task,'action':'WAIT'}
            if task=='expression':
                observed.append(deepcopy(packet))
                return {'task':task,'surface':'ordinary activity'}
            raise AssertionError(task)
        service=ValidatingSemanticService(CallbackLLMProvider(cb))
        rt=ConstitutiveRuntime(str(db),semantic=service)
        try:
            rt.initialize([('father','Father',SEED),('mother','Mother',SEED)])
            self.assertEqual(rt.step('father',requested_action='MAKE_OBJECT')['status'],'PERFORMED')
            old=next(iter(rt.ledger.world('w1')[1]['material_objects']))
            rt.step('father',requested_action='SPEAK',object_ref=old)
            self.assertEqual(rt.step('nadia')['attempt'],'INSPECT')
            self.assertEqual(len(rt.snapshot('nadia')['cultural_reference_practices']),int(acquire))
            self.assertEqual(rt.snapshot('nadia')['possible_ends'],[])
            phase['old']=False
            self.assertEqual(rt.step('mother' if different_maker else 'father',
                                     requested_action='MAKE_OBJECT')['status'],'PERFORMED')
            new=next(x for x in rt.ledger.world('w1')[1]['material_objects'] if x!=old)
            if expire:rt.step('mother',requested_action='REST')
        finally:rt.close()
        rt=ConstitutiveRuntime(str(db),semantic=service)
        try:
            before=deepcopy(rt.snapshot('nadia'))
            view=rt.situated('nadia')
            frame=view['attention_frame']
            rows=frame.get('cross_object_attention',[])
            expected=acquire and not different_maker and not expire
            self.assertEqual(len(rows),int(expected))
            self.assertLessEqual(len(frame['focally_eligible_cue_refs']),frame['focal_capacity_provisional'])
            self.assertEqual(rt.snapshot('nadia'),before)
            if expected:
                row=rows[0]
                self.assertEqual(row['new_material_object_ref'],new)
                self.assertEqual(row['earlier_material_object_ref'],old)
                self.assertIn(row['source_practice_ref'],view['readset'])
                self.assertIn(row['current_visible_object_cue_ref'],frame['focally_eligible_cue_refs'])
                self.assertIn(row,view['currents'])
            if forge:
                world=deepcopy(rt.ledger.world('w1'))
                with self.assertRaises(ValueError):rt.step('nadia')
                self.assertEqual(rt.snapshot('nadia'),before)
                self.assertEqual(rt.ledger.world('w1'),world)
                self.assertTrue(rt.verify()['valid'])
                return
            result=rt.step('nadia')
            self.assertEqual(result['attempt'],'INSPECT' if expected else 'WAIT')
            after=rt.snapshot('nadia')
            self.assertEqual(after['possible_ends'],[])
            self.assertEqual(after['projects'],[])
            self.assertEqual(after['memories'],[])
            evidence=after['evidence_paths'][-1]
            if expected:
                self.assertEqual(evidence['selected_cross_object_attention_analytic_only'],rows[0])
                self.assertNotIn('cross_object_attention_analytic_only',
                    observed[-1]['actor_accessible'].get('own_practical_selection') or {})
                self.assertNotIn('cross_object_attention',rt.situated('nadia')['attention_frame'])
            else:
                self.assertNotIn('selected_cross_object_attention_analytic_only',evidence)
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()

    def test_same_objective_event_different_acquired_apprehension(self):
        with tempfile.TemporaryDirectory() as d:
            self.arm(Path(d)/'acquired.sqlite',True)
            self.arm(Path(d)/'not_acquired.sqlite',False)

    def test_other_maker_and_expired_sign_do_not_transfer(self):
        with tempfile.TemporaryDirectory() as d:
            self.arm(Path(d)/'other.sqlite',True,different_maker=True)
            self.arm(Path(d)/'expired.sqlite',True,expire=True)

    def test_unissued_practical_id_is_not_world_authority(self):
        with tempfile.TemporaryDirectory() as d:
            self.arm(Path(d)/'forge.sqlite',True,forge=True)
