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
                vocal=packet.get('historically_possible_social_vocal_development',[]) if admit else []
                culture=packet.get('historically_possible_cultural_references',[])
                return {'task':task,'candidates':vocal+culture}
            if task=='actor_attempt':
                aid=packet['actor']['id']
                if aid!='nadia':
                    if aid=='mother' and stage.get('observer_inspect'):
                        found=[o for o in packet['practical_options'] if
                            o.get('grounds_status')=='UNTESTED_PERSONALLY_HEARD_PUBLIC_OBJECT_REFERENCE']
                        self.assertEqual(len(found),1)
                        return {'task':task,'practical_option_id':found[0]['option_id']}
                    return {'task':task,'action':stage['reply'] if packet.get('requesting_actor') else 'REST'}
                action=stage['action']
                if action=='LATER':
                    action='SPEAK' if any(o['action']=='SPEAK' for o in packet['options']) else 'SIGNAL'
                out={'task':task,'action':action}
                if action in ('INSPECT','SPEAK'):
                    ground=('UNTESTED_PERSONALLY_HEARD_PUBLIC_OBJECT_REFERENCE' if action=='INSPECT'
                            else 'ACQUIRED_CULTURAL_ATTENTION_MEETS_ACQUIRED_VOCAL_COORDINATION')
                    found=[o for o in packet['practical_options'] if o.get('grounds_status')==ground]
                    self.assertEqual(len(found),1)
                    out['practical_option_id']=found[0]['option_id']
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
            # Actual material production, actual public speech, then the
            # child's independently selected exact-object inquiry. Both
            # arms acquire this reference; only the vocal arm can enact it
            # as a new publicly accessible expression.
            self.assertEqual(rt.step('father',requested_action='MAKE_OBJECT')['status'],'PERFORMED')
            world=rt.ledger.world()[1]
            obj=next(iter(world['material_objects']))
            self.assertEqual(rt.step('father',requested_action='SPEAK',object_ref=obj)['status'],'PERFORMED')
            stage['action']='INSPECT';stage['other']=None
            self.assertEqual(rt.step('nadia')['status'],'PERFORMED')
            child=self.child(rt)
            self.assertEqual(len(child['cultural_reference_practices']),1)
            self.assertEqual(child['cultural_reference_practices'][0]['object_ref'],obj)
            self.assertEqual(child['projects'],[])
            # The inherited historical qualifier requires strictly earlier
            # acquisition, not recruitment in the same world-clock beat.
            self.assertEqual(child['cultural_reference_practices'][0]['origin_clock'],rt.ledger.world()[1]['clock'])
            self.assertEqual(rt.step('mother')['status'],'PERFORMED')
            child=self.child(rt)
            self.assertLess(child['cultural_reference_practices'][0]['origin_clock'],rt.ledger.world()[1]['clock'])
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
            if admit:
                self.assertEqual(world['cues'][-1]['material_object_ref'],obj)
                self.assertTrue(world['cues'][-1]['actual_spoken_object_demonstration'])
            # The child becomes an actual cultural source for the adult
            # through her own activity, not just the recipient of culture.
            stage['observer_inspect']=True
            self.assertEqual(cold.step('mother')['status'],'PERFORMED')
            learned=cold.ledger.actor('mother')[1]['cultural_reference_practices']
            self.assertEqual(len(learned),1)
            self.assertEqual(learned[0]['particular_speaker_ref'],'nadia' if admit else 'father')
            self.assertEqual(learned[0]['object_ref'],obj)
            self.assertEqual(cold.ledger.world()[1]['material_objects'][obj]['owner'],'father')
            self.assertTrue(cold.verify()['valid'])
            return child['age_days']
        finally:cold.close()

    def test_matched_life_reaches_actual_public_expression_only_via_admission(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.expressive_arm(Path(d)/'admit.db',True),
                             self.expressive_arm(Path(d)/'abstain.db',False))


    def productive_ordinary_arm(self,db,admit_end,forge=False,practice=None,witness=None,transfer=None,affect=None):
        """From ordinary infancy through plural response to self-generated end.
        Same acquired capacity in both arms; a later trial is not a project.
        No joint SING, no actual deficit/relief required, no injected child act.
        """
        from copy import deepcopy
        from um_sorok_organism.development import InvalidDevelopment
        phase={'name':'signal','other':None}
        seen=[]
        def model(task,p):
            aid=p.get('actor',{}).get('id')
            if task=='expression':return {'task':task,'surface':'Ordinary life.'}
            if task=='development':
                if aid!='nadia':
                    if aid=='mother' and phase['name']=='own' and witness is not None:
                        choices=p.get('historically_possible_productive_witness_reorganizations',[])
                        self.assertEqual(len(choices),1)
                        self.assertEqual(choices[0]['productive_witness_basis']['source_route'],
                                         'ACTUAL_RESPONSIVE_SPEECH_THEN_OTHER_SOLO_SOUND')
                        return {'task':task,'candidates':choices if witness else []}
                    return {'task':task,'candidates':[]}
                candidates=p.get('historically_possible_social_vocal_development',[])
                ends=[x for x in p.get('historically_possible_genetic_ends',[])
                      if x.get('productive_vocal_basis',{}).get('source_route')==
                         'ORDINARY_RESPONSIVE_COORDINATION_THEN_OWN_EXERCISE']
                if ends:
                    seen.extend(deepcopy(ends))
                    if forge:
                        ends[0]['productive_vocal_basis']['source_other_refs']=['invented','mother']
                    if admit_end:candidates=candidates+ends
                if phase['name']=='takeup':
                    new=p.get('historically_possible_productive_vocal_takeups',[])
                    if affect is not None:
                        for c in new:c['expected_difference']={'feature':'further own vocal exercise',
                            'direction':'MORE','sign_tags':['sing']}
                    candidates=candidates+new
                if affect is not None and phase['name'] in ('home_affect','local_affect','local_opposition'):
                    choices=[b for b in p.get('historically_possible_activity_affects',[])
                             if b.get('formation_source')=='OWN_ORDINARY_PROJECT_EXERCISE'
                             and b.get('object_affect_ref') is None]
                    self.assertEqual(len(choices),1)
                    orientation='WITHHOLD' if phase['name']=='local_affect' else 'APPROACH'
                    if affect=='forge':choices[0]['origin_exercise_sign_ref']='invented'
                    if affect:candidates=candidates+[{'kind':'ACQUIRE_ACTIVITY_AFFECT','basis':choices[0],
                         'affect_name':'reticence' if orientation=='WITHHOLD' else 'absorbed interest',
                         'personal_sense':'a provisional significance of the actually exercised concern',
                         'course_orientation':orientation}]
                if phase['name']=='transfer_probe' and transfer is not None:
                    choices=p.get('historically_possible_ordinary_context_transfers',[])
                    self.assertEqual(len(choices),1)
                    if transfer=='forge':
                        choices[0]['ordinary_vocal_context_transfer']['local_other_ref']='invented'
                    if transfer:candidates=candidates+choices
                return {'task':task,'candidates':candidates}
            if task=='actor_attempt':
                if aid!='nadia':
                    if p.get('requesting_actor'):
                        if witness is not None:
                            opts=[o for o in p['practical_options'] if o['operation']=='SPEAK' and o.get('project_id')]
                            self.assertEqual(len(opts),1)
                            return {'task':task,'practical_option_id':opts[0]['option_id']}
                        return {'task':task,'action':'SPEAK'}
                    if aid=='mother' and phase['name']=='witness':
                        opts=[o for o in p['practical_options'] if o.get('productive_witness_attention')]
                        self.assertEqual(len(opts),int(witness))
                        if opts:return {'task':task,'practical_option_id':opts[0]['option_id']}
                    return {'task':task,'action':'REST'}
                if phase['name']=='signal':
                    if phase['other'] is None:return {'task':task,'action':'SIGNAL'}
                    a=[x for x in p['practical_options']
                       if x.get('grounds_status')=='PREPROJECT_ORDINARY_VOCAL_EXPLORATION'
                       and x['world_request']['addressed_party_ref']==phase['other']]
                    self.assertEqual(len(a),1)
                    return {'task':task,'practical_option_id':a[0]['option_id']}
                if phase['name']=='trial':
                    a=[t for t in p['possible_end_trials'] if t.get('historical_ordinary_vocal_basis_ref')]
                    if not admit_end:
                        self.assertEqual(a,[])
                        return {'task':task,'action':'WAIT'}
                    self.assertEqual(len(a),1)
                    self.assertTrue(a[0]['not_current_external_sign_or_present_other_required'])
                    return {'task':task,'possible_end_trial_id':a[0]['trial_id']}
                if phase['name']=='transfer_probe':
                    a=[o for o in p['practical_options'] if o['operation']=='SING']
                    self.assertTrue(a)
                    self.assertTrue(all(not o.get('project_id') for o in a))
                    return {'task':task,'practical_option_id':a[0]['option_id']}
                if phase['name'] in ('home_affect','local_affect','local_opposition','affect_choice','home_choice','local_alone'):
                    a=[o for o in p['practical_options'] if o['operation']=='SING' and o.get('project_id')]
                    self.assertEqual(len(a),1)
                    rows=a[0].get('course_affective_organizations',[])
                    if phase['name']=='affect_choice':
                        self.assertEqual({x['course_orientation'] for x in rows},
                                         {'APPROACH','WITHHOLD'} if affect else set())
                        return {'task':task,'action':'WAIT'} if affect else {'task':task,'practical_option_id':a[0]['option_id']}
                    if phase['name']=='home_choice':
                        self.assertEqual({x['course_orientation'] for x in rows},{'APPROACH'} if affect else set())
                        self.assertTrue(all(x['basis']['location']=='home' for x in rows))
                    if phase['name']=='local_alone':self.assertEqual(rows,[])
                    return {'task':task,'practical_option_id':a[0]['option_id']}
                if phase['name']=='transferred':
                    a=[o for o in p['practical_options'] if o['operation']=='SING' and o.get('project_id')]
                    self.assertEqual(len(a),int(bool(transfer)))
                    return {'task':task,'practical_option_id':a[0]['option_id']} if a else {'task':task,'action':'WAIT'}
                if phase['name']=='recovery':
                    return {'task':task,'action':'REST'}
                if phase['name']=='after_period':
                    a=[o for o in p['practical_options'] if o['operation']=='SING' and o.get('project_id')]
                    return {'task':task,'practical_option_id':a[0]['option_id']} if a else {'task':task,'action':'REST'}
                if phase['name']=='project':
                    a=[o for o in p['practical_options'] if o['operation']=='SING' and o.get('project_id')]
                    if not admit_end:
                        self.assertEqual(a,[])
                        return {'task':task,'action':'WAIT'}
                    self.assertEqual(len(a),1)
                    return {'task':task,'practical_option_id':a[0]['option_id']}
                return {'task':task,'action':'SING'}
            raise AssertionError(task)
        def runtime():
            return ConstitutiveRuntime(str(db),semantic=ValidatingSemanticService(CallbackLLMProvider(model)))
        rt=runtime()
        try:
            adults=[adult('father','Father'),adult('mother','Mother')]
            for a in adults:a['projects']=[{'id':'speech:'+a['id'],'object':'ordinary vocal activity',
                'means':['SPEAK'],'priority':.2,'cue_terms':['home'],'status':'active'}]
            rt.ledger.initialize(blank_world(),[newborn('nadia','Nadia'),*adults])
            rt.step('nadia')
            proc=self.source(rt,'SIGNAL',self.anchor(rt,'SIGNAL'),180)
            rt.background(180,[proc])
            phase['other']='father';rt.step('nadia')
            rt.background(14)
            phase['other']='mother';rt.step('nadia')
            rt.step('mother')
            child=self.child(rt)
            self.assertEqual(child['body']['language'],.07)
            self.assertEqual(child['projects'],[])
            self.assertEqual(child['possible_ends'],[])
            self.assertFalse(any(x.get('own_attempted_operation')=='SING'
                                 for x in child['participation_history']))
            phase['name']='own'
            if forge:
                before=rt.verify()['events']
                with self.assertRaisesRegex(InvalidDevelopment,'GENESIS_PRODUCTIVE_VOCAL_HISTORY_FORGERY'):
                    rt.step('nadia')
                self.assertEqual(rt.verify()['events'],before)
                self.assertEqual(self.child(rt),child)
                return
            self.assertEqual(rt.step('nadia')['attempt'],'SING')
            child=self.child(rt)
            self.assertTrue(seen)
            self.assertEqual(len(child['possible_ends']),int(admit_end))
            self.assertEqual(child['projects'],[])
            if admit_end:
                end=child['possible_ends'][0]
                self.assertEqual(end['productive_vocal_basis']['source_other_refs'],['father','mother'])
                self.assertEqual(len(set(end['source_event_refs'])),3)
            # Actual intervening passage removes the initiating vocal cue;
            # prospective recruitment is historical rather than cue replay.
            rt.background(2)
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
        rt=runtime()
        try:
            phase['name']='trial'
            self.assertEqual(rt.step('nadia')['attempt'],'SING' if admit_end else 'WAIT')
            if admit_end:
                self.assertEqual(len(self.child(rt)['possible_ends'][0]['trial_history']),1)
                self.assertEqual(self.child(rt)['projects'],[])
            phase['name']='takeup'
            self.assertEqual(rt.step('nadia')['status'],'PERFORMED')
            child=self.child(rt)
            self.assertEqual(len(child['projects']),int(admit_end))
            if admit_end:
                project=child['projects'][0]
                self.assertEqual(len(set(project['takeup_evidence']['productive_vocal_takeup_basis']['source_event_refs'])),5)
                self.assertEqual(project['ordinary_vocal_genesis_basis']['source_other_refs'],['father','mother'])
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
        rt=runtime()
        try:
            phase['name']='project'
            self.assertEqual(rt.step('nadia')['attempt'],'SING' if admit_end else 'WAIT')
            self.assertTrue(rt.verify()['valid'])
            if witness is not None:
                mother=rt.ledger.actor('mother')[1]
                self.assertEqual(mother['projects'][0]['means'],['SPEAK','ORIENT'] if witness else ['SPEAK'])
                self.assertEqual(rt.ledger.actor('father')[1]['projects'][0]['means'],['SPEAK'])
                self.assertEqual(len(mother['projects'][0]['operational_history']),1)
                # Continue from the committed actual child sound, with a cold
                # parent projection. No access to the child's end or motive.
                rt.close()
                rt=runtime()
                phase['name']='witness'
                result=rt.step('mother')
                self.assertEqual(result['attempt'],'ORIENT' if witness else 'REST')
                self.assertTrue(rt.verify()['valid'])
                m=rt.ledger.actor('mother')[1]
                if witness:
                    self.assertEqual(m['projects'][0]['operational_history'][-1]['operation'],'ORIENT')
                    self.assertEqual(m['projects'][0]['productive_witness_means']['counterpart_ref'],'nadia')
                    self.assertFalse(any(o.get('productive_witness_attention')
                        for a in rt.situated('mother')['candidate_actions'] for o in a.get('practical_alternatives',[])))
                return m
            if transfer is not None:
                if affect is not None:
                    phase['name']='home_affect'
                    if affect=='forge':
                        before=self.child(rt);count=rt.verify()['events']
                        with self.assertRaisesRegex(InvalidDevelopment,'ACTIVITY_AFFECT_UNQUALIFIED_HISTORY'):
                            rt.step('nadia')
                        self.assertEqual(before,self.child(rt))
                        self.assertEqual(count,rt.verify()['events'])
                        return
                    self.assertEqual(rt.step('nadia')['attempt'],'SING')
                child=self.child(rt);project=child['projects'][0]
                rt.background(180)
                phase['name']='recovery'
                rt.step('nadia')
                self.assertEqual(rt.step('father',requested_action='MOVE',object_ref='workshop')['objective_outcome'],'MOVED')
                self.assertEqual(rt.step('nadia',requested_action='MOVE',object_ref='workshop')['objective_outcome'],'MOVED')
                opts=lambda: [o for a in rt.situated('nadia')['candidate_actions'] for o in a.get('practical_alternatives',[]) if o['operation']=='SING']
                self.assertFalse(any(o.get('project_id') for o in opts()))
                self.assertEqual(rt.step('father',requested_action='SING')['status'],'PERFORMED')
                self.assertTrue(any(not o.get('project_id') for o in opts()))
                phase['name']='transfer_probe'
                if transfer=='forge':
                    before=self.child(rt);count=rt.verify()['events']
                    with self.assertRaisesRegex(InvalidDevelopment,'ORDINARY_VOCAL_CONTEXT_TRANSFER_UNQUALIFIED'):
                        rt.step('nadia')
                    self.assertEqual(before,self.child(rt))
                    self.assertEqual(count,rt.verify()['events'])
                    return
                self.assertEqual(rt.step('nadia')['attempt'],'SING')
                child=self.child(rt)
                self.assertEqual(child['projects'][0]['id'],project['id'])
                self.assertEqual(len(child['projects'][0].get('ordinary_vocal_context_transfers',[])),int(bool(transfer)))
                rt.close();rt=runtime()
                phase['name']='transferred'
                self.assertEqual(rt.step('nadia')['attempt'],'SING' if transfer else 'WAIT')
                self.assertTrue(rt.verify()['valid'])
                if affect is not None:
                    phase['name']='local_affect';self.assertEqual(rt.step('nadia')['attempt'],'SING')
                    phase['name']='recovery';rt.step('nadia')
                    phase['name']='local_opposition';self.assertEqual(rt.step('nadia')['attempt'],'SING')
                    rt.close();rt=runtime()
                    phase['name']='affect_choice'
                    self.assertEqual(rt.step('nadia')['attempt'],'WAIT' if affect else 'SING')
                    self.assertEqual(rt.step('father',requested_action='MOVE',object_ref='home')['objective_outcome'],'MOVED')
                    phase['name']='local_alone';self.assertEqual(rt.step('nadia')['attempt'],'SING')
                phase['name']='recovery';rt.step('nadia')
                self.assertEqual(rt.step('nadia',requested_action='MOVE',object_ref='home')['objective_outcome'],'MOVED')
                phase['name']='home_choice' if affect is not None else 'project'
                self.assertEqual(rt.step('nadia')['attempt'],'SING')
                self.assertTrue(rt.verify()['valid'])
                return self.child(rt)
            if practice is None:return self.child(rt)
            child=self.child(rt)
            project=child['projects'][0]
            exercises=[x for x in child['power_exercises'] if x['operation']=='SING']
            clock=rt.ledger.world()[1]['clock']
            spec={'kind':'QUALIFIED_ROUTINE_PRACTICE','actor':'nadia','location':'home',
                  'start_clock':clock,'end_clock':clock+365,'max_hours_per_active_day':3,
                  'description':'sourcefree stress court: ordinary recurrent vocal project activity',
                  'operation':'SING','practice_project_ref':project['id'],
                  'project_exercise_ref':exercises[-1]['id']}
            before=rt.verify()['events']
            with self.assertRaisesRegex(ValueError,'PROJECT_SOURCE_NO_ACTUAL_SELECTED_EXERCISE'):
                rt.register_historical_routine_source(dict(spec,project_exercise_ref=exercises[0]['id']))
            self.assertEqual(rt.verify()['events'],before)
            source=rt.register_historical_routine_source(spec)
            proc={'kind':spec['kind'],'actor':'nadia','location':'home','source_ref':source['source_ref'],
                  'hours_per_active_day':3,'provisional_exposure_fraction':1.,
                  'operation':'SING','mode':'SOLO_COMPONENT_PRACTICE',
                  'practice_project_ref':project['id'],'project_exercise_ref':exercises[-1]['id']}
            before=rt.verify()['events']
            with self.assertRaisesRegex(ValueError,'PROJECT_ROUTINE_SOURCE_SCOPE_MISMATCH'):
                rt.background(1,[dict(proc,practice_project_ref='forged')])
            with self.assertRaisesRegex(ValueError,'PROJECT_ROUTINE_DUPLICATE_COMPONENT_WINDOW'):
                rt.background(1,[proc,proc])
            self.assertEqual(rt.verify()['events'],before)
            period=rt.background(365,[proc] if practice else [])['period']
            after=self.child(rt)
            self.assertEqual(after['age_days'],child['age_days']+365)
            self.assertEqual(after['projects'],child['projects'])
            self.assertEqual(after['power_exercises'],child['power_exercises'])
            self.assertEqual(after['memories'],child['memories'])
            self.assertEqual(len(period['qualified_aggregate_practice_refs']),int(practice))
            if practice:
                load=period['project_practice_loads'][0]
                self.assertEqual(load['modeled_hours'],1095)
                self.assertEqual(load['practice_project_ref'],project['id'])
                self.assertEqual(after['practice_exposures'][-1]['anchor_actual_event_ref'],
                                 exercises[-1]['event_ref'])
            self.assertEqual(eligible(after['body'],'SING')[0],not practice)
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
        rt=runtime()
        try:
            self.assertEqual(self.child(rt),after)
            phase['name']='after_period'
            first=rt.step('nadia')
            self.assertEqual(first['attempt'],'REST' if practice else 'SING')
            self.assertEqual(first['status'],'PERFORMED')
            self.assertEqual(self.child(rt)['projects'][0]['id'],project['id'])
            if practice:
                self.assertTrue(eligible(self.child(rt)['body'],'SING')[0])
                self.assertEqual(rt.step('nadia')['attempt'],'SING')
            self.assertTrue(rt.verify()['valid'])
            return after
        finally:rt.close()

    def test_ordinary_acquired_power_can_become_own_end_and_later_project(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)
            yes=self.productive_ordinary_arm(path/'yes.db',True)
            no=self.productive_ordinary_arm(path/'no.db',False)
            self.assertEqual(yes['body']['language'],no['body']['language'])
            self.assertEqual(len(yes['projects']),1)
            self.assertEqual(no['projects'],[])
            self.productive_ordinary_arm(path/'forged.db',True,True)


    def test_acquired_project_ordinary_activity_changes_body_without_erasing_wanting(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            active=self.productive_ordinary_arm(p/'active.db',True,practice=True)
            absent=self.productive_ordinary_arm(p/'absent.db',True,practice=False)
            self.assertEqual(active['age_days'],absent['age_days'])
            self.assertEqual(active['projects'],absent['projects'])
            self.assertLess(active['body']['rest'],absent['body']['rest'])


    def test_independently_responsive_adult_can_reorganize_own_project_through_child_sound(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            yes=self.productive_ordinary_arm(p/'hear.db',True,witness=True)
            no=self.productive_ordinary_arm(p/'abstain.db',True,witness=False)
            self.assertEqual(yes['projects'][0]['object'],no['projects'][0]['object'])
            self.assertEqual(yes['projects'][0]['operational_history'][0],
                             no['projects'][0]['operational_history'][0])
            self.assertEqual(yes['projects'][0]['means'],['SPEAK','ORIENT'])
            self.assertEqual(no['projects'][0]['means'],['SPEAK'])


    def test_acquired_ordinary_concern_transfers_only_after_actual_local_exploration_and_admission(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            yes=self.productive_ordinary_arm(p/'transfer.db',True,transfer=True)
            no=self.productive_ordinary_arm(p/'abstain.db',True,transfer=False)
            self.assertEqual(yes['projects'][0]['object'],no['projects'][0]['object'])
            self.assertEqual(yes['projects'][0]['origin'],no['projects'][0]['origin'])
            self.assertEqual(len(yes['projects'][0]['ordinary_vocal_context_transfers']),1)
            self.assertNotIn('ordinary_vocal_context_transfers',no['projects'][0])
            self.productive_ordinary_arm(p/'forge.db',True,transfer='forge')


    def test_same_acquired_concern_can_form_opposed_and_locally_differentiated_personal_significance(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            yes=self.productive_ordinary_arm(p/'opposed.db',True,transfer=True,affect=True)
            no=self.productive_ordinary_arm(p/'abstain.db',True,transfer=True,affect=False)
            aff=[a for e in yes['expectations'] for a in e.get('affective_organizations',[])]
            self.assertEqual(len(aff),3)
            self.assertEqual({a['basis']['location'] for a in aff},{'home','workshop'})
            self.assertEqual(len({a['origin_event_ref'] for a in aff}),3)
            self.assertFalse(any(e.get('affective_organizations') for e in no['expectations']))
            self.assertEqual(yes['projects'][0]['object'],no['projects'][0]['object'])
            self.productive_ordinary_arm(p/'forge_affect.db',True,transfer=True,affect='forge')
