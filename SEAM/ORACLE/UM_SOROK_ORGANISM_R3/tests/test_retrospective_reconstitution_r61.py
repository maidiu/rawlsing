"""R61: a present private interpretation can change recruitment of earlier life.
No imported old impression store, new scheduler, or retrospective event rewrite.
"""
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy
from um_sorok_organism.types import adult, blank_world
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.practical_powers import active_repair_technique
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService
from um_sorok_organism.development import InvalidDevelopment


class RetrospectiveReconstitution(unittest.TestCase):
    def arm(self,db,learn,nominate,forge=False):
        state={'stage':'quiet','target':None,'offered':[],'private':[]}
        hypothesis='I can make room for a meal without losing the work.'
        def callback(task,packet):
            if task=='expression':
                self.assertNotIn(hypothesis,str(packet))
                return {'task':task,'surface':'Ordinary life.'}
            if task=='actor_attempt':
                stage=state['stage']
                if stage=='repair':
                    rows=[o for o in packet['practical_options']
                          if o['operation']=='REPAIR'
                          and o.get('world_request',{}).get('material_object_ref')==state['target']
                          and o.get('project_id') is None]
                    self.assertEqual(len(rows),1)
                    return {'task':task,'practical_option_id':rows[0]['option_id']}
                if stage=='rehearse':
                    rows=[o for o in packet['private_rehearsal_options'] if o['affect_ref'] is None]
                    self.assertEqual(len(rows),1)
                    return {'task':task,'action':'WAIT',
                            'private_rehearsal_id':rows[0]['rehearsal_id'],
                            'private_rehearsal_content':'That earlier repair comes to mind differently.'}
                if stage=='later':
                    names={x['action'] for x in packet['options']}
                    return {'task':task,'action':'EAT' if 'EAT' in names else 'WAIT'}
                return {'task':task,'action':'WAIT'}
            if task=='development':
                if state['stage']=='repair':
                    if state.get('first'):
                        return {'task':task,'candidates':[
                            {'kind':'MEMORY','content':'The repair felt like something I must keep doing.',
                             'cue_terms':['repair']},
                            {'kind':'ACQUIRE_HISTORICAL_ORIENTATION','operation':'EAT',
                             'orientation_mode':'WITHHOLD'}]}
                    if learn:
                        return {'task':task,'candidates':packet['historically_possible_repair_techniques']}
                if state['stage']=='rehearse':
                    rec=packet['actual_private_rehearsal_analyst_only']
                    if rec:state['private'].append(deepcopy(rec))
                    rows=packet.get('historically_possible_retrospective_orientation_revisions',[])
                    state['offered'].extend(deepcopy(rows))
                    if rows and (nominate or forge):
                        c=deepcopy(rows[0]);c['interpretive_hypothesis']=hypothesis
                        if forge:c['retrospective_repair_revaluation_basis']['later_event_ref']='invented'
                        return {'task':task,'candidates':[c]}
                return {'task':task,'candidates':[]}
            raise AssertionError(task)
        service=ValidatingSemanticService(CallbackLLMProvider(callback))
        rt=ConstitutiveRuntime(str(db),semantic=service)
        try:
            w=blank_world();w['sites']['home']['stock']=30
            a=adult('worker','Mara')
            a['projects']=[{'id':'repair_training','object':'maintain things',
                            'means':['REPAIR'],'status':'active','priority':.5},
                           {'id':'ordinary_meal','object':'eat a meal',
                            'means':['EAT'],'status':'active','priority':.4}]
            rt.ledger.initialize(w,[a])
            src=rt.register_historical_routine_source({
                'kind':'QUALIFIED_ROUTINE_PRACTICE','actor':'worker','location':'home',
                'start_clock':0,'end_clock':7,'max_hours_per_active_day':3,
                'description':'bounded modeled component practice'})
            rt.background(7,processes=[{'kind':'QUALIFIED_ROUTINE_PRACTICE',
                'actor':'worker','location':'home','source_ref':src['source_ref'],
                'hours_per_active_day':3,'provisional_exposure_fraction':1.,
                'operation':'REPAIR','mode':'SOLO_COMPONENT_PRACTICE'}])
            refs=[]
            for _ in range(3):
                rt.step('worker',requested_action='REST')
                old=set(rt.ledger.world()[1]['material_objects'])
                self.assertEqual(rt.step('worker',requested_action='MAKE_OBJECT')['status'],'PERFORMED')
                refs.append((set(rt.ledger.world()[1]['material_objects'])-old).pop())
            for i,target in enumerate(refs):
                state['stage']='quiet';rt.step('worker',requested_action='REST')
                state.update(stage='repair',target=target,first=i==0)
                self.assertEqual(rt.step('worker')['status'],'PERFORMED')
            actor=rt.ledger.actor('worker')[1]
            technique=active_repair_technique(actor,'home')
            self.assertEqual(bool(technique),learn)
            prior=deepcopy(actor['historical_orientations'][0])
            memory=deepcopy(actor['memories'][0])
            self.assertEqual(prior['origin_event'],memory['origin'][0])
            self.assertTrue(any(x['action']=='EAT' for x in rt.situated('worker')['suspended_actions']))
            state['stage']='rehearse'
            # Same WAIT without a selected private activity cannot install a revaluation.
            rt.step('worker',requested_action='WAIT')
            self.assertEqual(state['offered'],[])
            self.assertEqual(state['private'],[])
            old=rt.ledger.actor('worker')[1];world=rt.ledger.world()[1]
            n=rt.verify()['events']
            if forge:
                with self.assertRaisesRegex(InvalidDevelopment,'RETROSPECTIVE_REVALUATION_UNQUALIFIED'):
                    rt.step('worker')
                self.assertEqual(rt.ledger.actor('worker')[1],old)
                self.assertEqual(rt.ledger.world()[1],world)
                self.assertEqual(rt.verify()['events'],n)
                return None
            self.assertEqual(rt.step('worker')['status'],'PERFORMED')
            self.assertEqual(len(state['private']),1)
            self.assertEqual(len(state['offered']),int(learn))
            now=rt.ledger.actor('worker')[1]
            row=now['historical_orientations'][0]
            self.assertEqual({k:v for k,v in row.items() if k!='revisions'},
                             {k:v for k,v in prior.items() if k!='revisions'})
            self.assertEqual(len(row['revisions']),int(learn and nominate))
            self.assertEqual({k:v for k,v in now['memories'][0].items() if k!='private_rehearsals'},memory)
            if learn and nominate:
                rev=row['revisions'][0]
                self.assertEqual(rev['interpretive_hypothesis_not_causal_truth'],hypothesis)
                self.assertEqual(rev['retrospective_repair_revaluation_basis']['acquired_technique_ref'],technique['id'])
                self.assertNotEqual(rev['event'],prior['origin_event'])
            self.assertNotIn(hypothesis,str(rt.ledger.world()[1]))
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
        cold=ConstitutiveRuntime(str(db),semantic=service)
        try:
            self.assertEqual(cold.ledger.actor('worker')[1],now)
            state['stage']='later'
            food=cold.ledger.world()[1]['sites']['home']['food']
            result=cold.step('worker')
            self.assertEqual(result['status'],'PERFORMED')
            expected='EAT' if learn and nominate else 'WAIT'
            self.assertEqual(result['attempt'],expected)
            self.assertEqual(cold.ledger.world()[1]['sites']['home']['food'],food-int(expected=='EAT'))
            self.assertTrue(cold.verify()['valid'])
            return expected
        finally:cold.close()

    def test_retrospective_meaning_is_optional_and_requires_actual_acquired_means(self):
        with tempfile.TemporaryDirectory() as d:
            for learn,nominate in ((True,True),(True,False),(False,True)):
                with self.subTest(learn=learn,nominate=nominate):
                    self.arm(Path(d)/str((learn,nominate)),learn,nominate)

    def test_forged_later_exercise_rejects_whole_current_transition(self):
        with tempfile.TemporaryDirectory() as d:
            self.arm(Path(d)/'forged',True,True,forge=True)


if __name__=='__main__':unittest.main()
