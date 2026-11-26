"""R52: the Other's audible exercise reorganizes a former co-performer's own project."""
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy

from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService, HeuristicSemanticProvider
from um_sorok_organism.development import InvalidDevelopment
from um_sorok_organism.psychic_genesis import PRODUCTIVE_VOCAL_FAMILY

PARENT={'source_ref':'R52_FICTIONAL_PARENT','source_grade':'SOURCEFREE_TEST_NOT_EMPIRICAL',
        'answers':{'r52':'not a survey response'},
        'fictional_seed':{'projects':[{'object':'vocal practice','means':['SING'],
                                      'priority':.5,'cue_terms':['sing']}]}}

class ProductiveWitnessR52(unittest.TestCase):
    def course(self, *, nominate, forge=False):
        phase='seed'
        offered=[]
        chosen=[]
        def callback(task,p):
            if task=='adult_constructor':
                return HeuristicSemanticProvider().propose(task,p)
            if task=='expression':return {'task':task,'surface':'Life continues.'}
            if task=='development':
                if p['actor']['id']=='mother':
                    c=p.get('historically_possible_productive_witness_reorganizations',[])
                    if phase=='project' and c:
                        offered.extend(deepcopy(c))
                        if forge:c[0]['productive_witness_basis']['counterpart_ref']='invented'
                        return {'task':task,'candidates':c if nominate else []}
                    return {'task':task,'candidates':[]}
                if p['actor']['id']=='nadia':
                    if phase=='own':
                        return {'task':task,'candidates':[x for x in p.get('historically_possible_genetic_ends',[])
                             if x.get('genesis_family')==PRODUCTIVE_VOCAL_FAMILY]}
                    if phase=='takeup':
                        return {'task':task,'candidates':p.get('historically_possible_productive_vocal_takeups',[])}
                return {'task':task,'candidates':[]}
            if task=='actor_attempt':
                if p['actor']['id']=='mother':
                    if p.get('requesting_actor'):
                        opts=[x for x in p['practical_options'] if x.get('operation')=='SING' and x.get('project_id')]
                        self.assertEqual(len(opts),1)
                        return {'task':task,'practical_option_id':opts[0]['option_id']}
                    opts=[x for x in p['practical_options'] if x.get('productive_witness_attention')]
                    if phase=='receive' and opts:
                        self.assertEqual(len(opts),1);chosen.append(deepcopy(opts[0]))
                        return {'task':task,'practical_option_id':opts[0]['option_id']}
                    return {'task':task,'action':'WAIT'}
                if phase=='trial':
                    ts=[t for t in p['possible_end_trials'] if t['operation']=='SING']
                    self.assertEqual(len(ts),1)
                    return {'task':task,'possible_end_trial_id':ts[0]['trial_id']}
                if phase=='project':
                    opts=[x for x in p['practical_options'] if x.get('operation')=='SING' and x.get('project_id')]
                    self.assertEqual(len(opts),1)
                    return {'task':task,'practical_option_id':opts[0]['option_id']}
                return {'task':task,'action':'SING'}
            raise AssertionError(task)
        service=ValidatingSemanticService(CallbackLLMProvider(callback))
        with tempfile.TemporaryDirectory() as tmp:
            db=str(Path(tmp)/'reciprocal.sqlite')
            rt=ConstitutiveRuntime(db,semantic=service)
            try:
                rt.initialize([('mother','Mother',PARENT)])
                rt.background(280)
                rt.step('nadia',requested_action='SING',target='mother')
                old=rt.snapshot('mother')['projects'][0]
                self.assertEqual(old['operational_history'][-1]['performed_status'],'PERFORMED')
                phase='own';rt.step('nadia')
                phase='trial';rt.step('nadia')
                phase='takeup';rt.step('nadia')
                self.assertEqual(len(rt.snapshot('nadia')['projects']),1)
                phase='project'
                if forge:
                    m=rt.snapshot('mother');n=rt.snapshot('nadia');w=rt.ledger.world()[1]
                    with self.assertRaisesRegex(InvalidDevelopment,'PRODUCTIVE_WITNESS_REORGANIZATION_UNQUALIFIED'):
                        rt.step('nadia')
                    self.assertEqual(rt.snapshot('mother'),m)
                    self.assertEqual(rt.snapshot('nadia'),n)
                    self.assertEqual(rt.ledger.world()[1],w)
                    return
                self.assertEqual(rt.step('nadia')['status'],'PERFORMED')
                self.assertEqual(len(offered),1)
                updated=rt.snapshot('mother')['projects'][0]
                self.assertEqual(updated['id'],old['id'])
                self.assertEqual(updated['object'],old['object'])
                self.assertEqual(updated['operational_history'],old['operational_history'])
                self.assertEqual(updated['means'],['SING','ORIENT'] if nominate else ['SING'])
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()
            phase='receive'
            cold=ConstitutiveRuntime(db,semantic=service)
            try:
                result=cold.step('mother')
                self.assertEqual(result['attempt'],'ORIENT' if nominate else 'WAIT')
                self.assertEqual(len(chosen),int(nominate))
                if nominate:
                    m=cold.snapshot('mother')
                    self.assertEqual(m['projects'][0]['operational_history'][-1]['operation'],'ORIENT')
                    self.assertEqual(m['projects'][0]['operational_history'][-1]['motive_realized'],'UNDETERMINED_BY_TECHNICAL_OUTCOME')
                    self.assertIn(chosen[0]['productive_witness_attention']['cue_ref'],
                                  m['evidence_paths'][-1]['received_cue_refs'])
                    # The old sign is no longer live; no perpetual reorienting course.
                    opts=[x for a in cold.situated('mother')['candidate_actions']
                          for x in a.get('practical_alternatives',[]) if x.get('productive_witness_attention')]
                    self.assertEqual(opts,[])
                self.assertTrue(cold.verify()['valid'])
            finally:cold.close()

    def test_reciprocal_project_refunction_reaches_cold_life(self):self.course(nominate=True)
    def test_same_received_act_can_leave_old_project_unchanged(self):self.course(nominate=False)
    def test_forgery_rolls_back_both_actors_and_world(self):self.course(nominate=True,forge=True)
