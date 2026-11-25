"""R51: actual coactivity -> own exercise -> optional end -> later trial -> takeup."""
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy

from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService, HeuristicSemanticProvider
from um_sorok_organism.psychic_genesis import PRODUCTIVE_VOCAL_FAMILY
from um_sorok_organism.development import InvalidDevelopment

PARENT={'source_ref':'R51_FICTIONAL_PARENT','source_grade':'SOURCEFREE_TEST_NOT_EMPIRICAL',
        'answers':{'r51':'not a survey response'},'fictional_seed':{'projects':[]}}

class ProductiveVocalR51(unittest.TestCase):
    def run_course(self, *, admit_end=True, forge=False):
        phase='seed'
        offered=[]
        def callback(task,p):
            if task=='adult_constructor':
                return HeuristicSemanticProvider().propose(task,p)
            if task=='expression':return {'task':task,'surface':'Life continues.'}
            if task=='development':
                if p['actor']['id']!='nadia':return {'task':task,'candidates':[]}
                c=[x for x in p.get('historically_possible_genetic_ends',[])
                   if x.get('genesis_family')==PRODUCTIVE_VOCAL_FAMILY]
                if c:
                    offered.extend(deepcopy(c))
                    if forge:
                        c[0]['productive_vocal_basis']['counterpart_ref']='invented'
                    if admit_end:return {'task':task,'candidates':c}
                if phase=='takeup':
                    return {'task':task,'candidates':p.get('historically_possible_productive_vocal_takeups',[])}
                return {'task':task,'candidates':[]}
            if task=='actor_attempt':
                if p['actor']['id']=='mother':
                    return {'task':task,'action':'SING' if p.get('requesting_actor') else 'WAIT'}
                if phase=='trial':
                    trials=[t for t in p['possible_end_trials'] if t.get('operation')=='SING']
                    if trials:return {'task':task,'possible_end_trial_id':trials[0]['trial_id']}
                    return {'task':task,'action':'WAIT'}
                if phase=='project':
                    courses=[o for o in p['practical_options'] if o.get('operation')=='SING' and o.get('project_id')]
                    self.assertTrue(courses)
                    return {'task':task,'practical_option_id':courses[0]['option_id']}
                return {'task':task,'action':'SING'}
            raise AssertionError(task)
        service=ValidatingSemanticService(CallbackLLMProvider(callback))
        with tempfile.TemporaryDirectory() as tmp:
            db=str(Path(tmp)/'productive.sqlite')
            rt=ConstitutiveRuntime(db,semantic=service)
            try:
                rt.initialize([('mother','Mother',PARENT)])
                rt.background(280)
                # Both bodily actors have actually performed a vocal act before the invitation.
                rt.step('mother',requested_action='SING')
                rt.step('nadia',requested_action='SING',target='mother')
                h=rt.snapshot('nadia')['participation_history']
                self.assertTrue(any(x.get('joint_participation_perceived') and x.get('own_attempted_operation')=='SING' for x in h),h)
                self.assertFalse(any(x.get('genesis_family')==PRODUCTIVE_VOCAL_FAMILY for x in rt.snapshot('nadia')['possible_ends']))
                phase='own'
                if forge:
                    before=rt.snapshot('nadia')
                    with self.assertRaisesRegex(InvalidDevelopment,'GENESIS_PRODUCTIVE_VOCAL_HISTORY_FORGERY'):
                        rt.step('nadia')
                    self.assertEqual(before,rt.snapshot('nadia'))
                    return
                rt.step('nadia')
                self.assertTrue(offered)
                ends=[x for x in rt.snapshot('nadia')['possible_ends'] if x.get('genesis_family')==PRODUCTIVE_VOCAL_FAMILY]
                self.assertEqual(len(ends),int(admit_end))
                self.assertTrue(rt.verify()['valid'])
                if not admit_end:return
                end=ends[0]
                self.assertIsNone(end['relieved_bodily_axis'])
                self.assertEqual(end['status'],'POSSIBLE_NOT_ACQUIRED_MOTIVE')
            finally:rt.close()
            phase='trial'
            rt=ConstitutiveRuntime(db,semantic=service)
            try:
                rt.step('nadia')
                e=next(x for x in rt.snapshot('nadia')['possible_ends'] if x['id']==end['id'])
                self.assertEqual(len(e['trial_history']),1)
                self.assertEqual(e['status'],'POSSIBLE_NOT_ACQUIRED_MOTIVE')
                phase='takeup'
                rt.step('nadia')
                e=next(x for x in rt.snapshot('nadia')['possible_ends'] if x['id']==end['id'])
                self.assertEqual(e['status'],'TAKEN_UP_AS_PRACTICAL_PROJECT')
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()
            phase='project'
            rt=ConstitutiveRuntime(db,semantic=service)
            try:
                result=rt.step('nadia')
                self.assertEqual(result['status'],'PERFORMED')
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()

    def test_joint_positive_activity_can_become_own_project(self):self.run_course()
    def test_semantic_abstention_preserves_no_end(self):self.run_course(admit_end=False)
    def test_forged_counterpart_rejected_atomically(self):self.run_course(forge=True)
