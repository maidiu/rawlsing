"""R008: detailed and compressed preproject child activity, one causal life.
Sourcefree controlled exercise; no measured childhood learning law.
"""
import tempfile
import unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import newborn, adult, blank_world
from um_sorok_organism.organism import eligible, conserved_motor_exercise
from um_sorok_organism.mediated_efficacy import preproject_motor_readiness
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService


class EarlyOrdinaryPractice(unittest.TestCase):
    def runtime(self, db, stage):
        def model(task, packet):
            if task=='development':return {'task':task,'candidates':[]}
            if task=='expression':return {'task':task,'surface':'Ordinary activity.'}
            if task=='actor_attempt':
                names={x['action'] for x in packet['options']}
                action=stage['action']
                if action=='LATER':action='SING' if 'SING' in names else 'WAIT'
                self.assertIn(action,names)
                return {'task':task,'action':action}
            raise AssertionError(task)
        return ConstitutiveRuntime(str(db),semantic=ValidatingSemanticService(CallbackLLMProvider(model)))

    def child(self, rt):
        return rt.ledger.actor('nadia')[1]

    def source(self, rt, operation, ref, days):
        w=rt.ledger.world()[1]
        source=rt.register_historical_routine_source({
            'kind':'QUALIFIED_ROUTINE_PRACTICE','actor':'nadia','location':'home',
            'start_clock':w['clock'],'end_clock':w['clock']+days,
            'max_hours_per_active_day':1,'description':'bounded ordinary bodily exploration',
            'operation':operation,'preproject_exercise_ref':ref})
        return {'kind':'QUALIFIED_ROUTINE_PRACTICE','actor':'nadia','location':'home',
                'source_ref':source['source_ref'],'hours_per_active_day':1,
                'provisional_exposure_fraction':1.,'operation':operation,
                'mode':'SOLO_COMPONENT_PRACTICE','preproject_exercise_ref':ref}

    def anchor(self, rt, operation):
        rows=[r for r in self.child(rt)['power_exercises']
              if r['operation']==operation and r.get('actor_selected_preproject_exercise')]
        self.assertEqual(len(rows),1)
        return rows[0]['id']

    def arm(self, db, aggregate, split=False):
        stage={'action':'SIGNAL'}
        rt=self.runtime(db,stage)
        try:
            rt.ledger.initialize(blank_world(),[newborn('nadia','Nadia')])
            self.assertEqual(rt.step('nadia')['attempt'],'SIGNAL')
            signal_ref=self.anchor(rt,'SIGNAL')
            proc=self.source(rt,'SIGNAL',signal_ref,100)
            before=rt.verify()['events']
            prior=self.child(rt)
            for wrong,code in [
                (dict(proc,operation='PRACTICE'),'PREPROJECT_ROUTINE_SOURCE_SCOPE_MISMATCH'),
                (dict(proc,preproject_exercise_ref='forged'),'PREPROJECT_ROUTINE_SOURCE_SCOPE_MISMATCH')]:
                with self.assertRaisesRegex(ValueError,code):rt.background(10,[wrong])
                self.assertEqual(rt.verify()['events'],before)
                self.assertEqual(self.child(rt),prior)
            period=rt.background(100-self.child(rt)['age_days'],[proc])['period']
            self.assertEqual(len(period['qualified_aggregate_practice_refs']),1)
            self.assertEqual(len(period['preproject_practice_loads']),1)
            self.assertEqual(self.child(rt)['projects'],[])
            self.assertEqual(self.child(rt)['forms'],{})
            options=rt.situated('nadia')['candidate_actions']
            practice=next(o for o in options if o['action']=='PRACTICE')
            self.assertIn('RUDIMENTARY_EXPLORATORY_OPPORTUNITY_NOT_ACQUIRED_MEANS',
                          practice['historical_support_statuses'])
            self.assertEqual(practice['practical_aggregate_sources'],
                             period['qualified_aggregate_practice_refs'])
            stage['action']='PRACTICE'
            self.assertEqual(rt.step('nadia')['status'],'PERFORMED')
            practice_ref=self.anchor(rt,'PRACTICE')
            self.assertEqual(conserved_motor_exercise(self.child(rt)),.008)
            span=125-self.child(rt)['age_days']
            proc=self.source(rt,'PRACTICE',practice_ref,span)
            before=rt.verify()['events']
            with self.assertRaisesRegex(ValueError,'PREPROJECT_ROUTINE_DUPLICATE_COMPONENT_WINDOW'):
                rt.background(1,[proc,proc])
            self.assertEqual(rt.verify()['events'],before)
            if split:
                rt.background(10,[proc] if aggregate else [])
                rt.background(span-10,[proc] if aggregate else [])
            else:rt.background(span,[proc] if aggregate else [])
            child=self.child(rt)
            self.assertEqual(child['age_days'],125)
            self.assertEqual(child['projects'],[])
            self.assertEqual(child['forms'],{})
            self.assertEqual(child['memories'],[])
            self.assertEqual(child['body']['language'],0)
            self.assertEqual(conserved_motor_exercise(child),.008)
            self.assertEqual(preproject_motor_readiness(child)>0,aggregate)
            self.assertEqual(eligible(child['body'],'SING')[0],aggregate)
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
        cold=self.runtime(db,stage)
        try:
            self.assertEqual(self.child(cold),child)
            stage['action']='LATER'
            actual=cold.step('nadia')
            self.assertEqual(actual['attempt'],'SING' if aggregate else 'WAIT')
            self.assertEqual(actual['status'],'PERFORMED')
            self.assertTrue(cold.verify()['valid'])
            return child
        finally:cold.close()

    def test_matched_life_and_partitioned_dose(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            whole=self.arm(p/'whole.db',True)
            split=self.arm(p/'split.db',True,True)
            absent=self.arm(p/'absent.db',False)
            self.assertEqual(preproject_motor_readiness(whole),preproject_motor_readiness(split))
            self.assertEqual(whole['body']['motor'],split['body']['motor'])
            self.assertGreater(whole['body']['motor'],absent['body']['motor'])
            self.assertLess(whole['body']['rest'],absent['body']['rest'])

    def test_injected_or_unlived_exercise_cannot_license_ordinary_dose(self):
        with tempfile.TemporaryDirectory() as d:
            rt=self.runtime(Path(d)/'negative.db',{'action':'WAIT'})
            try:
                rt.ledger.initialize(blank_world(),[newborn('nadia','Nadia')])
                rt.step('nadia',requested_action='SIGNAL')
                ref=self.child(rt)['power_exercises'][-1]['id']
                before=rt.verify()['events']
                for bad in (ref,'unlived'):
                    with self.assertRaisesRegex(ValueError,'PREPROJECT_SOURCE_NO_ACTUAL_OWN_EXERCISE'):
                        self.source(rt,'SIGNAL',bad,10)
                    self.assertEqual(rt.verify()['events'],before)
                self.assertEqual(self.child(rt)['practice_exposures'],[])
            finally:rt.close()


    def test_ordinary_history_recruits_plural_actual_social_response(self):
        """One life, ordinary bodily formation, distinct independent Others,
        optional semantic admission, and a cold actor-owned expressive capacity.
        """
        with tempfile.TemporaryDirectory() as d:
            db=Path(d)/'plural-vocal.db'
            stage={'action':'SIGNAL','other':None,'admit':True,'reply':'SPEAK'}
            def policy(task,packet):
                if task=='expression':return {'task':task,'surface':'Ordinary activity.'}
                if task=='development':
                    candidates=packet.get('historically_possible_social_vocal_development',[])
                    return {'task':task,'candidates':candidates if stage['admit'] else []}
                if task=='actor_attempt':
                    aid=packet['actor']['id']
                    if aid!='nadia':
                        return {'task':task,'action':stage['reply'] if packet.get('requesting_actor') else 'REST'}
                    operation=stage['action']
                    out={'task':task,'action':operation}
                    if stage['other'] is not None and operation=='SIGNAL':
                        found=[a for a in packet['practical_options']
                            if a.get('grounds_status')=='PREPROJECT_ORDINARY_VOCAL_EXPLORATION'
                            and a['world_request']['addressed_party_ref']==stage['other']]
                        self.assertEqual(len(found),1)
                        out['practical_option_id']=found[0]['option_id']
                    return out
                raise AssertionError(task)
            def runtime():
                return ConstitutiveRuntime(str(db),semantic=ValidatingSemanticService(CallbackLLMProvider(policy)))
            rt=runtime()
            try:
                adults=[adult('father','Father'),adult('mother','Mother')]
                for person in adults:
                    person['projects']=[{'id':'vocal:'+person['id'],'object':'vocal activity',
                        'means':['SPEAK'],'priority':.2,'cue_terms':['home'],'status':'active'}]
                rt.ledger.initialize(blank_world(),[newborn('nadia','Nadia'),*adults])
                self.assertEqual(rt.step('nadia')['status'],'PERFORMED')
                ref=self.anchor(rt,'SIGNAL')
                proc=self.source(rt,'SIGNAL',ref,180)
                rt.background(180,[proc])
                self.assertEqual(self.child(rt)['cultural_demonstrations'],[])
                self.assertEqual(self.child(rt)['body']['language'],0)
                stage['other']='father'
                a=rt.step('nadia')
                self.assertEqual(a['coactor'],'SPEAK')
                self.assertEqual(len(self.child(rt)['vocal_turn_experiences']),1)
                rt.background(14)
                stage['other']='mother'
                stage['reply']='REFUSE'
                rt.step('nadia')
                self.assertEqual(len(self.child(rt)['vocal_turn_experiences']),1)
                self.assertEqual(self.child(rt)['body']['language'],0)
                stage['reply']='SPEAK'
                b=rt.step('nadia')
                self.assertEqual(b['coactor'],'SPEAK')
                child=self.child(rt)
                self.assertEqual(child['body']['language'],.07)
                acquired=child['vocal_coordination_practices'][0]
                self.assertEqual(acquired['earlier_source_other_ref'],'father')
                self.assertEqual(acquired['source_other_ref'],'mother')
                self.assertEqual(acquired['source_route'],'ORDINARY_ACTOR_ADDRESSED_RESPONSIVE_LIFE')
                stage['other']='father'
                rt.step('nadia')
                self.assertEqual(self.child(rt)['body']['language'],.07)
                rt.background(14)
                stage['admit']=False
                rt.step('nadia')
                self.assertEqual(self.child(rt)['body']['language'],.07)
                self.assertTrue(rt.verify()['valid'])
                child=self.child(rt)
            finally:rt.close()
            cold=runtime()
            try:
                self.assertEqual(self.child(cold),child)
                self.assertEqual(child['cultural_demonstrations'],[])
                self.assertEqual(child['projects'],[])
                self.assertFalse(eligible(child['body'],'SPEAK')[0])
                self.assertTrue(cold.verify()['valid'])
            finally:cold.close()


    def expressive_arm(self,db,admit):
        """Matched long childhood continuations with finite material support.
        Every responsive exchange is actually performed, never a synthetic
        repeated conversational history. Semantic admission differs by arm.
        """
        stage={'action':'SIGNAL','other':None,'reply':'SPEAK'}
        def policy(task,packet):
            if task=='expression':return {'task':task,'surface':'Ordinary activity.'}
            if task=='development':
                return {'task':task,'candidates':packet.get(
                    'historically_possible_social_vocal_development',[]) if admit else []}
            if task=='actor_attempt':
                aid=packet['actor']['id']
                if aid!='nadia':
                    return {'task':task,'action':stage['reply'] if packet.get('requesting_actor') else 'REST'}
                action=stage['action']
                if action=='LATER':
                    action='SPEAK' if any(o['action']=='SPEAK' for o in packet['options']) else 'SIGNAL'
                out={'task':task,'action':action}
                if action=='SIGNAL' and stage['other'] is not None:
                    options=[o for o in packet['practical_options'] if
                        o.get('grounds_status')=='PREPROJECT_ORDINARY_VOCAL_EXPLORATION'
                        and o['world_request']['addressed_party_ref']==stage['other']]
                    self.assertEqual(len(options),1)
                    out['practical_option_id']=options[0]['option_id']
                return out
            raise AssertionError(task)
        def runtime():
            return ConstitutiveRuntime(str(db),semantic=ValidatingSemanticService(CallbackLLMProvider(policy)))
        rt=runtime()
        try:
            adults=[adult('father','Father'),adult('mother','Mother')]
            for person in adults:
                person['projects']=[{'id':'vocal:'+person['id'],'object':'vocal and care activity',
                    'means':['SPEAK','FEED'],'priority':.2,'cue_terms':['home'],'status':'active'}]
            rt.ledger.initialize(blank_world(),[newborn('nadia','Nadia'),*adults])
            rt.step('nadia')
            proc=self.source(rt,'SIGNAL',self.anchor(rt,'SIGNAL'),180)
            rt.background(180,[proc])
            # All adult replies are independently planned. Feeding is real
            # material reproduction, not linguistic instruction or a vocal turn.
            stage['other']='father'
            stage['reply']='FEED'
            before=self.child(rt)['body']['nutrition']
            fed=rt.step('nadia')
            self.assertEqual(fed['coactor'],'FEED')
            self.assertGreater(self.child(rt)['body']['nutrition'],before)
            self.assertEqual(self.child(rt)['vocal_turn_experiences'],[])
            stage['reply']='SPEAK'
            rt.step('nadia')
            rt.background(14)
            stage['other']='mother'
            rt.step('nadia')
            rt.background(450-self.child(rt)['age_days'])
            for i in range(4):
                stage['action']='REST';stage['other']=None
                rt.step('nadia')
                rt.step('father');rt.step('mother')
                stage['action']='SIGNAL'
                stage['other']='father' if i%2==0 else 'mother'
                stage['reply']='SPEAK'
                self.assertEqual(rt.step('nadia')['coactor'],'SPEAK')
                rt.background(14)
            child=self.child(rt)
            self.assertEqual(child['body']['language'],.35 if admit else 0)
            self.assertEqual(len(child['vocal_turn_experiences']),6)
            self.assertEqual(len(child['vocal_coordination_practices']),5 if admit else 0)
            self.assertEqual(child['projects'],[])
            self.assertEqual(child['cultural_demonstrations'],[])
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
        cold=runtime()
        try:
            self.assertEqual(self.child(cold),child)
            stage['action']='LATER';stage['other']=None
            if admit:
                option=next(o for o in cold.situated('nadia')['candidate_actions'] if o['action']=='SPEAK')
                self.assertIn('ACQUIRED_ORDINARY_SOCIAL_VOCAL_COORDINATION_NOT_WORDS',
                              option['historical_support_statuses'])
            else:self.assertNotIn('SPEAK',[o['action'] for o in cold.situated('nadia')['candidate_actions']])
            result=cold.step('nadia')
            self.assertEqual(result['attempt'],'SPEAK' if admit else 'SIGNAL')
            self.assertEqual(result['status'],'PERFORMED')
            world=cold.ledger.world()[1]
            self.assertEqual(world['cues'][-1]['kind'],'performed_speak' if admit else 'performed_signal')
            self.assertTrue(cold.verify()['valid'])
            return child['age_days']
        finally:cold.close()

    def test_matched_life_reaches_actual_public_expression_only_via_admission(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.expressive_arm(Path(d)/'admit.db',True),
                             self.expressive_arm(Path(d)/'abstain.db',False))
