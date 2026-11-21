"""R8 red-first tests: source-qualified compressed life, sensory access and acquired project typing."""
import math
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from um_sorok_organism.types import adult, blank_world
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.world import add_cue
from um_sorok_organism.constitution import actor_access
from um_sorok_organism.development import admit, InvalidDevelopment, recurring_provisional_growth
from um_sorok_organism.activity import eligible_activities
from um_sorok_organism.types import AccessibleEncounter, Constitution
from um_sorok_organism.constitution import materialize


def exp(a='a'):
    return {'actor': a,'ref':'lived:r8','participated':True,'perceived_cues':[]}

def practiced(a):
    a['forms']={'shared_form': {'id':'shared_form','kind':'PRACTICE','cues':['sing'],'enables':['SING'],
                                  'scope':{'locations':['home']},'strength':.5}}
    return a

class CompressedLifeR8(unittest.TestCase):
    def test_r8_p064_actor_specific_period_does_not_rewrite_another_actor(self):
        # Two independent persons can acquire same form ID, but their coverage is different.
        a=practiced(adult('a','A')); b=practiced(adult('b','B'))
        process={'kind':'practice_access','coverage':'AGGREGATE_MODELED',
                 'actor_id':'a','form_id':'shared_form','warrants_scope_change':True,
                 'locations':['workshop']}
        self.assertEqual(len(recurring_provisional_growth(a,'period1',[process])),1)
        self.assertEqual(recurring_provisional_growth(b,'period1',[process]),[])
        self.assertEqual(a['forms']['shared_form']['scope']['locations'],['home','workshop'])
        self.assertEqual(b['forms']['shared_form']['scope']['locations'],['home'])

    def test_r8_p064_unowned_process_cannot_grow_any_person(self):
        a=practiced(adult('a','A')); before=deepcopy(a)
        process={'kind':'practice_access','coverage':'AGGREGATE_MODELED',
                 'form_id':'shared_form','warrants_scope_change':True,'locations':['workshop']}
        with self.assertRaisesRegex(InvalidDevelopment,'PERIOD_PRACTICE_REQUIRES_ACTOR'):
            recurring_provisional_growth(a,'period1',[process])
        self.assertEqual(a,before)

    def test_r8_p065_period_growth_candidate_batch_atomic_on_invalid_second(self):
        a=practiced(adult('a','A')); before=deepcopy(a)
        valid={'kind':'practice_access','coverage':'AGGREGATE_MODELED',
               'actor_id':'a','form_id':'shared_form','warrants_scope_change':True,
               'locations':['workshop']}
        invalid={**valid,'locations':'not-a-list'}
        with self.assertRaisesRegex(InvalidDevelopment,'INVALID_PERIOD_LOCATIONS'):
            recurring_provisional_growth(a,'period1',[valid,invalid])
        self.assertEqual(a,before)

    def test_r8_p065_valid_period_growth_conserves_original_location(self):
        a=practiced(adult('a','A'))
        process={'kind':'practice_access','coverage':'AGGREGATE_MODELED',
                 'actor_id':'a','form_id':'shared_form','warrants_scope_change':True,
                 'locations':['home','workshop','workshop']}
        recurring_provisional_growth(a,'period2',[process])
        self.assertEqual(a['forms']['shared_form']['scope']['locations'],['home','workshop'])

class SensoryIngressR8(unittest.TestCase):
    def test_r8_p066_string_tags_cannot_expand_into_individual_characters(self):
        w=blank_world();before=deepcopy(w)
        with self.assertRaisesRegex(ValueError,'INVALID_CUE_TAGS'):
            add_cue(w,'new_contact','help',location='home')
        self.assertEqual(w,before)

    def test_r8_p066_nontext_cue_tag_refused_prior_to_canon(self):
        w=blank_world();before=deepcopy(w)
        with self.assertRaisesRegex(ValueError,'INVALID_CUE_TAGS'):
            add_cue(w,'contact',['care',42],location='home')
        self.assertEqual(w,before)

    def test_r8_p067_unrecognized_modality_must_not_bypass_sensor_gate(self):
        w=blank_world();a=adult('a','A');a['body']['sensor']=0.0;w['positions']['a']='home'
        # Sourcefree world cannot assert its own special 'present' modality.
        with self.assertRaisesRegex(ValueError,'INVALID_CUE_MODALITY'):
            add_cue(w,'private',['private'],location='home',modality='present')

    def test_r8_p067_sensor_level_must_not_be_bypassed_by_case_or_unknown_modality(self):
        w=blank_world();a=adult('a','A');a['body']['sensor']=0.0;w['positions']['a']='home'
        w['cues'].append({'id':'unqualified','clock':0,'last_access_clock':0,
                          'kind':'secret','tags':['secret'],'location':'home',
                          'modality':'VISUAL','threshold':.95,'private_to':None})
        self.assertFalse(any(c.get('id')=='unqualified' for c in actor_access(a,w).cues))

    def test_r8_p067_negative_threshold_refused_before_issuing_observation(self):
        w=blank_world();before=deepcopy(w)
        with self.assertRaisesRegex(ValueError,'INVALID_CUE_THRESHOLD'):
            add_cue(w,'contact',['contact'],location='home',threshold=-.1)
        self.assertEqual(w,before)

    def test_r8_p067_valid_sensed_cue_and_private_cue_still_recruit(self):
        w=blank_world();a=adult('a','A');b=adult('b','B');w['positions'].update({'a':'home','b':'home'})
        c=add_cue(w,'song',['song'],location='home',modality='auditory',private_to='a')
        self.assertIn(c['id'],[x['id'] for x in actor_access(a,w).cues])
        self.assertNotIn(c['id'],[x['id'] for x in actor_access(b,w).cues])

    def test_r8_p066_bad_runtime_cue_does_not_commit_or_poison_recruitment(self):
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'life.db'))
            try:
                rt.initialize()
                with self.assertRaisesRegex(ValueError,'INVALID_CUE_TAGS'):
                    rt.cue('nadia',kind='contact',tags='home')
                self.assertEqual(rt.verify()['events'],1)
                self.assertEqual(rt.ledger.world()[1]['clock'],0)
                self.assertIsNotNone(rt.situated('nadia'))
            finally: rt.close()

class ProjectAdmissionR8(unittest.TestCase):
    def test_r8_p068_contextual_only_string_false_must_not_make_project_dormant(self):
        a=adult('a','A');before=deepcopy(a)
        proposal={'kind':'ADD_PROJECT','project':{'id':'p1','object':'practice singing',
               'means':['SING'],'contextual_only':'false'}}
        with self.assertRaisesRegex(InvalidDevelopment,'INVALID_PROJECT_CONTEXTUAL_FLAG'):
            admit(a,exp(),'e1',[proposal])
        self.assertEqual(a,before)

    def test_r8_p068_reorganize_contextual_flag_bool_only_and_atomic(self):
        a=adult('a','A');a['projects']=[{'id':'p1','object':'sing','means':['SING'],'priority':.6}]
        before=deepcopy(a)
        with self.assertRaisesRegex(InvalidDevelopment,'INVALID_PROJECT_CONTEXTUAL_FLAG'):
            admit(a,exp(),'e1',[{'kind':'REORGANIZE_PROJECT','project_id':'p1',
                    'contextual_only':'False'}])
        self.assertEqual(a,before)

    def test_r8_p068_valid_false_flag_keeps_project_available(self):
        a=adult('a','A')
        admit(a,exp(),'e1',[{'kind':'ADD_PROJECT','project':{'id':'p1','object':'sing',
                         'means':['SING'],'contextual_only':False}}])
        w=blank_world();w['positions']['a']='home'
        opts=eligible_activities(materialize(a,w),[],actor_access(a,w))
        self.assertEqual([o['id'] for o in opts],['p1'])

if __name__=='__main__':unittest.main()

# Additional adversarial cases: original R7 claims changes even when there is no
# newly accessible context, and malformed historic sensory data can poison reads.
class FurtherR8(unittest.TestCase):
    def test_r8_p069_no_actual_scope_expansion_is_not_a_developmental_event(self):
        a=practiced(adult('a','A')); before=deepcopy(a)
        proc={'kind':'practice_access','coverage':'AGGREGATE_MODELED','actor_id':'a',
              'form_id':'shared_form','warrants_scope_change':True,'locations':['home']}
        self.assertEqual(recurring_provisional_growth(a,'period-no-change',[proc]),[])
        self.assertEqual(a,before)

    def test_r8_p066_malformed_historical_cue_must_not_poison_recruitment(self):
        w=blank_world();a=adult('a','A');w['positions']['a']='home'
        w['cues'].append({'id':'poison','clock':0,'last_access_clock':0,
            'kind':'noise','tags':['fine',99],'location':'home','modality':'visual',
            'threshold':.05,'private_to':None})
        self.assertNotIn('poison',[x['id'] for x in actor_access(a,w).cues])

    def test_r8_p067_nan_threshold_must_not_admit_sensory_artifact(self):
        w=blank_world();before=deepcopy(w)
        with self.assertRaisesRegex(ValueError,'INVALID_CUE_THRESHOLD'):
            add_cue(w,'mist',['mist'],threshold=float('nan'))
        self.assertEqual(w,before)

    def test_r8_p064_compressed_runtime_period_scope_change_is_actor_specific(self):
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'life.db'))
            try:
                p={'answers':{'q':'yes'},'source_ref':'test-sealed'}
                rt.initialize([('a','A',p),('b','B',p)])
                v,w=rt.ledger.world()
                actors=rt.ledger.actors()
                vv={aid:rt.ledger.actor(aid)[0] for aid in actors}
                for aid in ('a','b'):
                    actors[aid]['forms']['shared_form']=practiced(adult(aid,aid))['forms']['shared_form']
                rt.ledger.commit(rt.world_id,v,w,actors,vv,'FIXTURE_SAME_FORM_ID',None,
                    {'note':'two independent persons may share a form identifier'})
                process={'kind':'practice_access','coverage':'AGGREGATE_MODELED',
                         'actor_id':'a','form_id':'shared_form',
                         'warrants_scope_change':True,'locations':['workshop']}
                rt.background(3,[process])
                self.assertEqual(rt.ledger.actor('a')[1]['forms']['shared_form']['scope']['locations'],['home','workshop'])
                self.assertEqual(rt.ledger.actor('b')[1]['forms']['shared_form']['scope']['locations'],['home'])
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()
