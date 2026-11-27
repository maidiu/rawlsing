"""Actual cultural reference -> later different thing -> new possible end.

Sourcefree callback contrast, not native LLM discovery or human learning law.
"""
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import (
    CallbackLLMProvider, ValidatingSemanticService, HeuristicSemanticProvider)
from um_sorok_organism.development import InvalidDevelopment
from test_cultural_mediation_r3 import SEED

class CrossObjectGenerability(unittest.TestCase):
    def arm(self, db, acquired, forge=False):
        state={'phase':'old','new':None}
        seen=[]
        def callback(task,packet):
            if task=='adult_constructor':
                return HeuristicSemanticProvider().propose(task,packet)
            if task=='development':
                if packet['actor']['id']!='nadia':
                    return {'task':task,'candidates':[]}
                if state['phase']=='old' and acquired:
                    return {'task':task,'candidates':packet.get(
                        'historically_possible_cultural_references',[])}
                if state['phase']=='new':
                    q=packet.get('historically_possible_cross_object_significance',[])
                    seen.extend(deepcopy(q))
                    if q:
                        basis=deepcopy(q[0]['incidental_object_end_basis'])
                        if forge:basis['source_practice_ref']='foreign'
                        return {'task':task,'candidates':[{
                            'kind':'NOTICE_POSSIBLE_END',
                            'perceived_cue_ref':q[0]['source_cue_ref'],
                            'origin_material_object_ref':q[0]['world_material_object_ref'],
                            'possible_object':'discover how different made things can be cared for',
                            'possible_means':['INSPECT'],
                            'cue_terms':['material_object'],
                            'incidental_object_end_basis':basis}]}
                if state['phase']=='takeup':
                    q=packet.get('historically_possible_incidental_takeup',[])
                    if q:return {'task':task,'candidates':[{
                        'kind':'TAKE_UP_POSSIBLE_END',
                        'possible_end_ref':q[0]['possible_end_ref'],
                        'later_perceived_cue_ref':q[0]['later_perceived_cue_ref'],
                        'incidental_takeup_basis':q[0],'means':['INSPECT']}]}
                return {'task':task,'candidates':[]}
            if task=='actor_attempt':
                if packet['actor']['id']!='nadia':
                    return {'task':task,'action':'WAIT'}
                if state['phase']=='old':
                    return HeuristicSemanticProvider().propose(task,packet)
                if state['phase']=='trial':
                    opts=[t for t in packet.get('possible_end_trials',[])
                          if t.get('source_material_object_ref')==state['new']]
                    if opts:return {'task':task,'possible_end_trial_id':opts[0]['trial_id']}
                    return {'task':task,'action':'WAIT'}
                opts=[a for a in packet.get('practical_options',[])
                      if a['operation']=='INSPECT'
                      and a.get('world_request',{}).get('material_object_ref')==state['new']
                      and (a.get('project_id') is not None)==(state['phase']=='project')]
                if opts:return {'task':task,'practical_option_id':opts[0]['option_id']}
                return {'task':task,'action':'WAIT'}
            if task=='expression':
                return {'task':task,'surface':'The ordinary activity continues.'}
            raise AssertionError(task)
        service=ValidatingSemanticService(CallbackLLMProvider(callback))
        rt=ConstitutiveRuntime(str(db),semantic=service)
        try:
            rt.initialize([('father','Father',SEED),('mother','Mother',SEED)])
            self.assertEqual(rt.step('father',requested_action='MAKE_OBJECT')['status'],'PERFORMED')
            old=next(iter(rt.ledger.world('w1')[1]['material_objects']))
            rt.step('father',requested_action='SPEAK',object_ref=old)
            self.assertEqual(rt.step('nadia')['attempt'],'INSPECT')
            a=rt.snapshot('nadia')
            self.assertEqual(len(a['cultural_reference_practices']),int(acquired))
            self.assertEqual(a['possible_ends'],[])
            self.assertEqual(a['projects'],[])
            state['phase']='gap'
            rt.step('mother',requested_action='REST')
            self.assertEqual(rt.step('father',requested_action='MAKE_OBJECT')['status'],'PERFORMED')
            new=next(x for x in rt.ledger.world('w1')[1]['material_objects'] if x!=old)
            state['new']=new
            state['phase']='new'
            if forge:
                before=deepcopy(rt.snapshot('nadia'))
                with self.assertRaises(InvalidDevelopment):rt.step('nadia')
                self.assertEqual(rt.snapshot('nadia'),before)
                self.assertTrue(rt.verify()['valid'])
                return
            self.assertEqual(rt.step('nadia')['attempt'],'INSPECT')
            a=rt.snapshot('nadia')
            self.assertEqual(len(a['possible_ends']),int(acquired))
            self.assertEqual(a['memories'],[])
            self.assertEqual(a['projects'],[])
            if acquired:
                self.assertEqual(seen[0]['incidental_object_end_basis']['earlier_material_object_ref'],old)
                self.assertEqual(a['possible_ends'][0]['origin_material_object_ref'],new)
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
        cold=ConstitutiveRuntime(str(db),semantic=service)
        try:
            state['phase']='trial'
            outcome=cold.step('nadia')
            self.assertEqual(outcome['attempt'],'INSPECT' if acquired else 'WAIT')
            state['phase']='takeup'
            cold.step('nadia')
            self.assertEqual(len(cold.snapshot('nadia')['projects']),int(acquired))
            if acquired:
                self.assertEqual(cold.snapshot('nadia')['projects'][0]['material_object_ref'],new)
            state['phase']='project'
            outcome=cold.step('nadia')
            self.assertEqual(outcome['attempt'],'INSPECT' if acquired else 'WAIT')
            self.assertTrue(cold.verify()['valid'])
        finally:cold.close()

    def test_same_later_object_distinct_acquired_history(self):
        with tempfile.TemporaryDirectory() as d:
            self.arm(Path(d)/'acquired.sqlite',True)
            self.arm(Path(d)/'abstained.sqlite',False)

    def test_forged_acquired_source_ref_refused(self):
        with tempfile.TemporaryDirectory() as d:
            self.arm(Path(d)/'forged.sqlite',True,True)
