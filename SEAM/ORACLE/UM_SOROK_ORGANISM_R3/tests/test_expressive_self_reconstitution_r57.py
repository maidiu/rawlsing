"""R57: actually received own expression can reorganize the next course.

Matched sourcefree callbacks; no human affect law, no forced interpretation.
"""
import copy
import tempfile
import unittest
from pathlib import Path
from um_sorok_organism.types import adult, blank_world
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService
from um_sorok_organism.development import InvalidDevelopment

class ExpressiveSelfReconstitution(unittest.TestCase):
    def arm(self,db,nominate,*,forge=False):
        stage='start'; final_receipts={}; received=[]; offers=[]
        def policy(task,packet):
            if task=='actor_attempt':
                if packet['actor']['id']!='worker':return {'task':task,'action':'WAIT'}
                if stage=='start':return {'task':task,'action':'REST','project_id':'duty'}
                if stage in ('speech','receive','later'):
                    rows=[x for x in packet['practical_options']
                          if x.get('project_id')=='duty' and x['operation']=='SPEAK']
                    self.assertEqual(len(rows),1)
                    affects=rows[0]['course_affective_organizations']
                    if stage=='later':
                        acquired=[a for a in affects if a['basis'].get('formation_source')
                                  =='OWN_PERFORMED_EXPRESSION']
                        received.extend(copy.deepcopy(acquired))
                        if any(a['course_orientation']=='WITHHOLD' for a in acquired):
                            return {'task':task,'action':'WAIT'}
                    return {'task':task,'practical_option_id':rows[0]['option_id']}
                return {'task':task,'action':'WAIT'}
            if task=='expression':
                self.assertNotIn('selected_course_affects_analytic_only',
                    (packet['actor_accessible'].get('own_practical_selection') or {}))
                self.assertNotIn('unease about my own speech',str(packet))
                return {'task':task,'surface':'Ordinary activity.'}
            if task=='development':
                aid=packet['actor']['id'];ex=packet['experience']
                if stage=='receive':final_receipts[aid]=copy.deepcopy(ex)
                if aid!='worker':return {'task':task,'candidates':[]}
                if stage=='appraise':
                    row=packet['historically_possible_delayed_appraisals'][0]
                    return {'task':task,'candidates':[{'kind':'APPRAISE_EXPECTED_DIFFERENCE',
                        'expectation_ref':row['expectation_ref'],
                        'perceived_cue_ref':row['source_perceived_cue_ref'],
                        'appraisal':'ACTOR_INTERPRETS_DISAPPOINTED'}]}
                if stage=='affect':
                    row=packet['historically_possible_activity_affects'][0]
                    return {'task':task,'candidates':[{'kind':'ACQUIRE_ACTIVITY_AFFECT',
                        'basis':row,'affect_name':'private unease',
                        'personal_sense':'quiet conflicts with duty','course_orientation':'APPROACH'}]}
                if stage=='speech':
                    rows=packet['historically_possible_expressive_practices']
                    if rows:return {'task':task,'candidates':[{'kind':'ACQUIRE_EXPRESSIVE_PRACTICE',
                        'basis':rows[0]['basis'],'cadence':'HALTING'}]}
                if stage=='receive':
                    rows=packet.get('historically_possible_self_expression_affects',[])
                    self.assertEqual(len(rows),1)
                    offers.extend(copy.deepcopy(rows))
                    if nominate:
                        basis=copy.deepcopy(rows[0])
                        if forge:basis['current_cue_ref']='foreign-cue'
                        return {'task':task,'candidates':[{'kind':'ACQUIRE_ACTIVITY_AFFECT',
                            'basis':basis,'affect_name':'unease about my own speech',
                            'personal_sense':'my effort to speak can itself become uncomfortable',
                            'course_orientation':'WITHHOLD'}]}
                return {'task':task,'candidates':[]}
            raise AssertionError(task)
        service=ValidatingSemanticService(CallbackLLMProvider(policy))
        rt=ConstitutiveRuntime(str(db),semantic=service)
        try:
            a=adult('worker','Mara')
            a['projects']=[{'id':'duty','object':'sustain availability',
                'means':['REST','SPEAK'],'status':'active','priority':.5,
                'expected_difference':{'feature':'availability','direction':'PRESERVE',
                                       'sign_tags':['wait']}}]
            rt.ledger.initialize(blank_world(),[a,adult('hearer','Hearer'),adult('blocked','Blocked')])
            rt.register_sourcefree_recursive_encounter_paths({
                'grade':'SOURCEFREE_TEST_ONLY','source_ref':'R57_SOUND',
                'paths':[{'observer':aid,'source_actor':'worker','location':'home',
                    'from_clock':0,'through_clock':30,'hearing':audible,
                    'sound_path':'audible' if audible else 'blocked',
                    'visual':True,'light':'lit','sightline':'unobstructed','facing':'away'}
                    for aid,audible in [('hearer',True),('blocked',False)]]})
            rt.step('worker')
            stage='appraise';rt.step('worker')
            stage='affect';rt.step('worker')
            for _ in range(2):
                stage='quiet';rt.step('worker')
                stage='speech';self.assertEqual(rt.step('worker')['status'],'PERFORMED')
                self.assertNotIn('vocal_cadence',rt.ledger.world()[1]['cues'][-1])
            actor=rt.snapshot('worker')
            parent=copy.deepcopy(actor['expectations'][0]['affective_organizations'][0])
            self.assertEqual(parent['expressive_practice']['cadence'],'HALTING')
            stage='quiet';rt.step('worker')
            stage='receive'
            if forge:
                before=copy.deepcopy(rt.snapshot('worker'));world=copy.deepcopy(rt.ledger.world())
                with self.assertRaisesRegex(InvalidDevelopment,'ACTIVITY_AFFECT_UNQUALIFIED_HISTORY'):
                    rt.step('worker')
                self.assertEqual(rt.snapshot('worker'),before)
                self.assertEqual(rt.ledger.world(),world)
                self.assertTrue(rt.verify()['valid'])
                return
            self.assertEqual(rt.step('worker')['status'],'PERFORMED')
            cue=rt.ledger.world()[1]['cues'][-1]
            self.assertEqual(cue['vocal_cadence'],'HALTING')
            self.assertNotIn('private unease',str(cue))
            own=rt.snapshot('worker')['evidence_paths'][-1]['own_vocal_reception']
            self.assertEqual(own['cue_ref'],cue['id'])
            hear=next(c for c in final_receipts['hearer']['perceived_cues'] if c['id']==cue['id'])
            self.assertEqual(hear['vocal_cadence'],'HALTING')
            self.assertNotIn('blocked',final_receipts)
            self.assertEqual(len(offers),1)
            a=rt.snapshot('worker');rows=a['expectations'][0]['affective_organizations']
            self.assertEqual(rows[0],parent)
            self.assertEqual(len(rows),1+int(nominate))
            self.assertEqual(a['memories'],[])
            if nominate:
                self.assertEqual(rows[1]['basis']['object_affect_ref'],parent['id'])
                self.assertEqual(rows[1]['basis']['current_cue_ref'],cue['id'])
                self.assertEqual(rows[1]['depth'],2)
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
        cold=ConstitutiveRuntime(str(db),semantic=service)
        try:
            stage='quiet';cold.step('worker')
            stage='later';result=cold.step('worker')
            self.assertEqual(result['attempt'],'WAIT' if nominate else 'SPEAK')
            self.assertEqual(len(received),int(nominate))
            self.assertEqual(cold.snapshot('worker')['expectations'][0]['affective_organizations'][0],parent)
            self.assertTrue(cold.verify()['valid'])
            return cue['vocal_cadence'], result['attempt']
        finally:cold.close()

    def test_same_performed_expression_different_psychological_afterlife(self):
        with tempfile.TemporaryDirectory() as d:
            a=self.arm(Path(d)/'formed.sqlite',True)
            b=self.arm(Path(d)/'abstained.sqlite',False)
            self.assertEqual(a,('HALTING','WAIT'))
            self.assertEqual(b,('HALTING','SPEAK'))

    def test_foreign_self_receipt_rolls_back(self):
        with tempfile.TemporaryDirectory() as d:
            self.arm(Path(d)/'forged.sqlite',True,forge=True)
