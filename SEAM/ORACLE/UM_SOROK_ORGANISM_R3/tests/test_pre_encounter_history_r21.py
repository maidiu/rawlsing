"""R21 mulch first consumer: lived history exists before user contact.

The childhood model is an upstream generative history, not user-played
dialogue with Nadia's father. Exact code is SOURCEFREE, not adult-person
scientific calibration or a claim that the user sees private memories.
"""
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.joined_longitudinal_demo import run_counterfactual


PARENT = {
    'source_ref': 'r21_fictional_parent_source',
    'source_grade': 'SOURCEFREE_TEST_NOT_A_PYAT_RESPONDENT',
    'answers': {'R21_FICTIONAL_INSTRUMENT': 'NOT_A_REAL_PERSON_ANSWER'},
    'fictional_seed': {'projects': []},
}


class PreEncounterHistoryR21(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name)/'r21.sqlite3'
        self.rt = ConstitutiveRuntime(str(self.db))
        self.rt.initialize([
            ('father', 'Father', PARENT),
            ('mother', 'Mother', PARENT),
        ])

    def tearDown(self):
        self.rt.close()
        self.tmp.cleanup()

    def test_child_history_is_offscreen_before_any_meeting(self):
        operations = []
        source_step = self.rt.step

        def spy(actor_id, *args, **kwargs):
            operations.append((actor_id, args, kwargs))
            return source_step(actor_id, *args, **kwargs)

        self.rt.step = spy
        receipt = self.rt.construct_pre_encounter_history(
            'nadia', 8, horizon_days=3,
            autonomous_beats=1, max_segments=32)
        self.assertEqual(receipt['status'], 'HISTORICAL_AGE_CUT_REACHED')
        self.assertEqual(receipt['last_modeled_age_days'], 8)
        self.assertEqual(self.rt.snapshot('nadia')['age_days'], 8)
        self.assertEqual(receipt['autonomous_beats_committed'],
                         sum(len(x['autonomous_event_receipts'])
                             for x in receipt['historical_receipts']))
        self.assertGreaterEqual(receipt['autonomous_beats_committed'], 1)
        self.assertTrue(receipt['no_user_action_or_other_person_consent_injected'])
        self.assertFalse(receipt['user_visible_childhood_scenes'])
        self.assertTrue(receipt['public_first_encounter_not_issued'])
        self.assertEqual(receipt['continuing_actor_role_not_reclassified'],
                         'child')
        self.assertTrue(all(args == () and kwargs == {}
                            for _, args, kwargs in operations))
        self.assertNotIn('forms', receipt)
        self.assertNotIn('memories', receipt)
        self.assertNotIn('self_model', receipt)
        self.assertNotIn('fictional_seed', str(receipt))
        self.assertTrue(self.rt.verify()['valid'])

    def test_real_registered_care_period_conditions_child_without_diary(self):
        initial = self.rt.snapshot('nadia')
        declared = self.rt.register_historical_routine_source({
            'kind':'QUALIFIED_REPRODUCTIVE_CARE',
            'actor':'mother','location':'home',
            'start_clock':0,'end_clock':20,
            'max_hours_per_active_day':4,
            'description':'sourcefree nine-day bounded period'})
        receipt = self.rt.construct_pre_encounter_history(
            'nadia',9,horizon_days=9,autonomous_beats=0,
            period_processes=[{
                'kind':'QUALIFIED_REPRODUCTIVE_CARE',
                'actor':'mother','recipient':'nadia','location':'home',
                'source_ref':declared['source_ref'],
                'hours_per_active_day':4,
                'provisional_exposure_fraction':.8}])
        after = self.rt.snapshot('nadia')
        self.assertEqual(receipt['status'],'HISTORICAL_AGE_CUT_REACHED')
        self.assertEqual(receipt['autonomous_beats_committed'],0)
        self.assertEqual(len(after['undergone_care_periods']),1)
        self.assertGreater(after['body']['comfort'],
                           initial['body']['comfort'])
        self.assertEqual(after['co_regulation_orientations'],[])
        self.assertEqual(receipt['historical_receipts'][0]
                         ['qualified_period_source_refs'],
                         [declared['source_ref']])
        self.assertTrue(self.rt.verify()['valid'])
        self.assertNotIn('performed_care_speech',str(receipt))
        self.assertNotIn('actor_gratitude',str(receipt))

    def test_unregistered_period_claim_cannot_invent_care_or_ledger_event(self):
        original = self.rt.verify()['events']
        before = self.rt.snapshot('nadia')
        with self.assertRaisesRegex(
                ValueError,'HISTORICAL_PROCESS_UNREGISTERED_SOURCE_ENVELOPE'):
            self.rt.construct_pre_encounter_history(
                'nadia',9,horizon_days=9,autonomous_beats=0,
                period_processes=[{
                    'kind':'QUALIFIED_REPRODUCTIVE_CARE',
                    'actor':'mother','recipient':'nadia','location':'home',
                    'source_ref':'fabricated_unregistered_care',
                    'hours_per_active_day':3,
                    'provisional_exposure_fraction':.5}])
        self.assertEqual(self.rt.verify()['events'],original)
        self.assertEqual(self.rt.snapshot('nadia'),before)

    def test_reopen_persists_actual_offscreen_history_without_private_render(self):
        receipt = self.rt.construct_pre_encounter_history(
            'nadia', 6, horizon_days=2,
            autonomous_beats=0, max_segments=16)
        end = self.rt.snapshot('nadia')
        self.assertEqual(receipt['last_modeled_age_days'], 6)
        self.assertTrue(self.rt.verify()['valid'])
        cold = ConstitutiveRuntime(str(self.db))
        try:
            self.assertTrue(cold.verify()['valid'])
            self.assertEqual(cold.snapshot('nadia'), end)
        finally:
            cold.close()

    def test_held_due_obligation_cannot_be_silently_aged_past(self):
        from um_sorok_organism.continuity_clock import continue_pre_encounter

        class Ledger:
            def __init__(self):
                self.actor_state = {
                    'id':'nadia', 'age_days':5, 'role':'child'}
                self.world_state = {'clock':5}

            def actors(self):
                return {'nadia':self.actor_state}

            def actor(self, actor):
                return (1, self.actor_state)

            def world(self, world_id):
                return (1, self.world_state)

        class Owner:
            world_id = 'w1'

            def __init__(self):
                self.ledger = Ledger()
                self.advance_calls = 0

            def advance_to_discontinuity(self, horizon):
                self.advance_calls += 1
                self.ledger.world_state['clock'] += 1
                return {
                    'historical_discontinuity': {
                        'kind':'OBLIGATION_DUE', 'actor':'father',
                        'source_ref':'unsettled_source'},
                    'ordinary_interval_receipt':None,
                    'high_resolution_actor_event':'performed_actual_turn',
                }

            def continue_without_user(self, beats):
                raise AssertionError('Cannot skip unresolved material source')

        owner = Owner()
        result = continue_pre_encounter(
            owner, 'nadia', 8, horizon_days=1, autonomous_beats=3)
        self.assertEqual(result['status'],
                         'HELD_AT_UNRESOLVED_MATERIAL_DISCONTINUITY')
        self.assertEqual(result['last_modeled_age_days'], 5)
        self.assertEqual(result['historical_receipts'][0]
                         ['independently_resolved_event'], 'performed_actual_turn')
        self.assertTrue(result['partial_historical_commits_not_rolled_back'])
        self.assertEqual(owner.advance_calls, 1)

    def test_invalid_age_or_budget_rejected_before_any_ledger_append(self):
        original = self.rt.verify()['events']
        bad = [
            (False,3,1,4), (None,3,1,4),
            (6,0,1,4), (6,3,25,4),
            (6,3,1,0), (600,3,1,4),
            (0,3,1,4),
        ]
        for target,horizon,beats,segments in bad:
            with self.subTest(target=target, horizon=horizon,
                              beats=beats,segments=segments):
                with self.assertRaises(ValueError):
                    self.rt.construct_pre_encounter_history(
                        'nadia', target, horizon_days=horizon,
                        autonomous_beats=beats,max_segments=segments)
                self.assertEqual(self.rt.verify()['events'], original)
        with self.assertRaisesRegex(
                ValueError,'PRE_ENCOUNTER_INVALID_PERIOD_PROCESSES'):
            self.rt.construct_pre_encounter_history(
                'nadia',6,period_processes={'invented':'care'})
        self.assertEqual(self.rt.verify()['events'],original)
        with self.assertRaises(TypeError):
            self.rt.construct_pre_encounter_history(
                'nadia', 6, requested_action='SPEAK')
        self.assertEqual(self.rt.verify()['events'],original)

    def test_reuses_distinct_historical_nadia_lives_without_rewriting_parent(self):
        with tempfile.TemporaryDirectory() as out:
            run_counterfactual(Path(out)/'causal',days=4,beats=2)
            preserved = []
            for filename in ('speaking.sqlite3','silent.sqlite3'):
                rt = ConstitutiveRuntime(
                    str(Path(out)/'causal'/filename))
                try:
                    before = rt.snapshot('nadia')
                    target = before['age_days']+6
                    receipt = rt.construct_pre_encounter_history(
                        'nadia',target,horizon_days=3,
                        autonomous_beats=1,max_segments=32)
                    self.assertEqual(receipt['status'],
                                     'HISTORICAL_AGE_CUT_REACHED')
                    after = rt.snapshot('nadia')
                    initial = {x['id'] for x in
                               before['cultural_reference_practices']}
                    later = {x['id'] for x in
                             after['cultural_reference_practices']}
                    self.assertTrue(initial.issubset(later))
                    preserved.append(before['cultural_reference_practices'])
                    self.assertTrue(rt.verify()['valid'])
                finally:
                    rt.close()
            self.assertNotEqual(preserved[0],preserved[1])



class RecursiveEncounterR33(unittest.TestCase):
    def test_actual_offscreen_speech_differential_exposure_and_cold_afterlife(self):
        from um_sorok_organism.semantics import (
            CallbackLLMProvider, ValidatingSemanticService, HeuristicSemanticProvider)
        with tempfile.TemporaryDirectory() as out:
            branches={}
            for audible in (True,False):
                heard=[]
                def model(task,packet):
                    if task=='adult_constructor':
                        proposal=HeuristicSemanticProvider().propose(task,packet)
                        proposal.setdefault('forms',[]).append({
                            'id':'r33_speech_power','kind':'PRACTICE',
                            'cues':['speech'],'enables':['SPEAK'],
                            'always_recruitable':True,'scope':{},
                            'lifecycle':'ACTIVE','body_min':0,
                            'strength':.8,'access':'tacit'})
                        return proposal
                    if task=='actor_attempt':
                        operation='SPEAK' if packet['actor']['id']=='father' else 'WAIT'
                        self.assertIn(operation,{x['action'] for x in packet['options']})
                        return {'task':task,'action':operation}
                    if task=='expression':
                        return {'task':task,'surface':'Ordinary life continues.'}
                    if task=='development':
                        if packet['actor']['id']=='nadia':
                            signs=[c for c in packet['experience']['perceived_cues']
                                   if c['kind']=='heard_voice']
                            if signs:
                                heard.extend(signs)
                                return {'task':task,'candidates':[{
                                    'kind':'TRACE','cue_terms':['voice'],
                                    'manifestation':'sourcefree_undergone_voice',
                                    'content':'Voice encountered; meaning undetermined.'}]}
                        return {'task':task,'candidates':[]}
                    raise AssertionError(task)
                service=ValidatingSemanticService(CallbackLLMProvider(model))
                db=str(Path(out)/('audible.sqlite' if audible else 'blocked.sqlite'))
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    rt.initialize([('father','Father',PARENT),('mother','Mother',PARENT)])
                    before=rt.snapshot('nadia')
                    spec={'grade':'SOURCEFREE_TEST_ONLY','source_ref':'R33_DIRECTED_PATH',
                        'paths':[{'observer':'nadia','source_actor':'father',
                            'location':'home','from_clock':0,'through_clock':20,
                            'hearing':audible,'sound_path':'audible' if audible else 'blocked',
                            'visual':True,'light':'lit','sightline':'unobstructed',
                            'facing':'away'}]}
                    source=rt.register_sourcefree_recursive_encounter_paths(spec)
                    self.assertEqual(rt.snapshot('nadia'),before)
                    receipt=rt.construct_pre_encounter_history(
                        'nadia',1,horizon_days=1,autonomous_beats=1)
                    self.assertEqual(receipt['status'],'HISTORICAL_AGE_CUT_REACHED')
                    self.assertEqual(receipt['autonomous_beats_committed'],1)
                    w=rt.ledger.world(rt.world_id)[1]
                    actual=w['cues'][-1]
                    self.assertEqual(actual['kind'],'performed_speak')
                    self.assertEqual(actual['source_actor'],'father')
                    access=rt.see('nadia')['cues']
                    self.assertFalse(any(c.get('source_actor')=='father' for c in access))
                    signs=[c for c in access if c.get('id')==actual['id']]
                    self.assertEqual(len(signs),int(audible))
                    if audible:
                        self.assertEqual(signs[0]['encounter_path_ref'],source['path_refs'][0])
                        self.assertEqual(signs[0]['lexical_comprehension'],'NOT_ESTABLISHED')
                        self.assertIsNone(signs[0]['source_actor'])
                        self.assertEqual(signs[0]['kind'],'heard_voice')
                    self.assertEqual(len(heard),int(audible))
                    first=rt.snapshot('nadia')['traces']
                    self.assertEqual(len(first),int(audible))
                    self.assertTrue(rt.verify()['valid'])
                finally:
                    rt.close()
                cold=ConstitutiveRuntime(db,semantic=service)
                try:
                    self.assertEqual(cold.snapshot('nadia')['traces'],first)
                    again=cold.construct_pre_encounter_history(
                        'nadia',2,horizon_days=1,autonomous_beats=1)
                    self.assertEqual(again['status'],'HISTORICAL_AGE_CUT_REACHED')
                    self.assertEqual(len(cold.snapshot('nadia')['traces']),2*int(audible))
                    self.assertTrue(cold.verify()['valid'])
                    self.assertNotIn('neighbor_users',cold.ledger.world(cold.world_id)[1])
                    branches[audible]=cold.snapshot('nadia')['traces']
                finally:
                    cold.close()
            self.assertNotEqual(branches[True],branches[False])

    def test_directed_channel_identity_language_lifetime_and_world_conservation(self):
        from um_sorok_organism.types import adult, newborn, blank_world, copy
        from um_sorok_organism.world import (
            register_recursive_encounter_paths, add_cue)
        from um_sorok_organism.constitution import actor_access
        w=blank_world()
        actors={'father':adult('father','Father'),'mother':adult('mother','Mother'),
                'nadia':newborn('nadia','Nadia')}
        w['positions'].update({x:'home' for x in actors})
        base={'source_actor':'father','location':'home','from_clock':0,
            'through_clock':2,'hearing':True,'sound_path':'audible',
            'visual':True,'light':'lit','sightline':'unobstructed','facing':'source'}
        spec={'grade':'SOURCEFREE_TEST_ONLY','source_ref':'R33_FINITE_PATH',
            'paths':[dict(base,observer='nadia'),dict(base,observer='mother')]}
        register_recursive_encounter_paths(w,actors,spec)
        cue=add_cue(w,'speech',['private_meaning_not_for_infant'],
                    location='home',modality='auditory',
                    description='Adult propositional words.',source_actor='father')
        old=copy(w)
        child=next(c for c in actor_access(actors['nadia'],w).cues if c['id']==cue['id'])
        self.assertEqual(child['kind'],'heard_voice')
        self.assertEqual(child['source_actor'],'father')
        self.assertNotIn('private_meaning_not_for_infant',child['tags'])
        self.assertNotIn('Adult propositional words.',child['description'])
        mother=next(c for c in actor_access(actors['mother'],w).cues if c['id']==cue['id'])
        self.assertEqual(mother['description'],'Adult propositional words.')
        self.assertEqual(w,old)
        # No overlapping world-source overrides or unregistered pseudo-person.
        with self.assertRaises(ValueError):
            register_recursive_encounter_paths(w,actors,spec)
        self.assertEqual(w,old)
        invalid=copy(spec);invalid['paths'][0]['observer']='visitor'
        with self.assertRaises(ValueError):
            register_recursive_encounter_paths(w,actors,invalid)
        self.assertEqual(w,old)
        # A prior heard sign does not survive its material lifetime.
        w['clock']=1
        self.assertFalse(any(c['id']==cue['id'] for c in actor_access(actors['nadia'],w).cues))
        # A future source is not retroactive.
        w['clock']=3
        later=add_cue(w,'speech',['later'],location='home',
                      modality='auditory',source_actor='father')
        projection=next(c for c in actor_access(actors['nadia'],w).cues
                        if c['id']==later['id'])
        self.assertNotIn('encounter_path_ref',projection)


if __name__ == '__main__':
    unittest.main()


class StructuralOrdinaryLifeR44(unittest.TestCase):
    def initialize(self,db):
        from um_sorok_organism.types import adult,newborn,blank_world
        from um_sorok_organism.material_conjunction import admit_authored_structural_history
        from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
        def policy(task,packet):
            if task=='development':return {'task':task,'candidates':[]}
            if task=='expression':return {'task':task,'surface':'Ordinary activity.'}
            return {'task':task,'action':'WAIT'}
        rt=ConstitutiveRuntime(db,semantic=ValidatingSemanticService(CallbackLLMProvider(policy)))
        w=blank_world()
        parent=adult('mother','Mother')
        parent['projects']=[{'id':'care','object':'care for child','means':['CARE'],
                            'status':'active','priority':.5},
                            {'id':'practice','object':'practice movement','means':['PRACTICE'],
                             'status':'active','priority':.5}]
        child=newborn('nadia','Nadia')
        spec={'grade':'EXPLICIT_SOURCEFREE_STRUCTURAL_HISTORY','source_ref':'fictional:period_world',
              'positions':[{'id':'p0','actor':'mother','field':'care_access','value':'admitted',
                            'source_ref':'fictional:p0','effective_from':0,'effective_until':2},
                           {'id':'p1','actor':'mother','field':'care_access','value':'excluded',
                            'source_ref':'fictional:p1','effective_from':3,'effective_until':5}],
              'rules':[{'id':'care_gate','operation':'CARE','location':'home',
                        'source_ref':'fictional:care_gate','effective_from':0,'effective_until':5,
                        'all_of':[{'kind':'RECORDED_POSITION','field':'care_access','equals':'admitted'}]}]}
        admit_authored_structural_history(w,{'mother','nadia'},spec)
        rt.ledger.initialize(w,[parent,child],
            source_seals=[('authored_structural_history','FICTIONAL_WORLD_CONDITIONING',spec)])
        rows=[]
        for kind in ('QUALIFIED_REPRODUCTIVE_CARE','QUALIFIED_ROUTINE_PRACTICE'):
            registered=rt.register_historical_routine_source({
                'kind':kind,'actor':'mother','location':'home','start_clock':0,
                'end_clock':12,'max_hours_per_active_day':3,
                'description':'bounded fictional routine'})
            row={'kind':kind,'actor':'mother','location':'home',
                 'source_ref':registered['source_ref'],'hours_per_active_day':3,
                 'provisional_exposure_fraction':1.0}
            if kind=='QUALIFIED_REPRODUCTIVE_CARE':row['recipient']='nadia'
            else:row.update({'operation':'PRACTICE','mode':'SOLO_COMPONENT_PRACTICE'})
            rows.append(row)
        return rt,rows

    def test_structural_transition_splits_compressed_history_without_inventing_care(self):
        from um_sorok_organism.mediated_efficacy import situated_component_efficacy
        with tempfile.TemporaryDirectory() as d:
            db=str(Path(d)/'period')
            rt,rows=self.initialize(db)
            try:
                before=rt.ledger.world()[1]
                actors=rt.ledger.actors()
                n=rt.verify()['events']
                with self.assertRaisesRegex(ValueError,'HISTORICAL_TIME_SPLIT_AT_STRUCTURAL_GATE'):
                    rt.background(9,processes=rows)
                self.assertEqual(rt.ledger.world()[1],before)
                self.assertEqual(rt.ledger.actors(),actors)
                self.assertEqual(rt.verify()['events'],n)
                first=rt.advance_to_discontinuity(horizon=9,processes=rows)
                self.assertEqual(first['historical_discontinuity']['at'],3)
                self.assertEqual(first['historical_discontinuity']['after_decision'],'BLOCKED')
                self.assertIsNone(first['high_resolution_actor_event'])
                first_child=rt.snapshot('nadia')
                self.assertEqual(len(first_child['undergone_care_periods']),1)
                self.assertEqual(first_child['evidence_paths'],[])
                self.assertEqual(first_child['memories'],[])
                first_parent=rt.snapshot('mother')
                self.assertEqual(len(first_parent['practice_exposures']),1)
                self.assertEqual(first_child['age_days'],3)
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()
            cold=ConstitutiveRuntime(db)
            try:
                second=cold.advance_to_discontinuity(horizon=6,processes=rows)
                self.assertEqual(second['historical_discontinuity']['at'],6)
                self.assertEqual(second['historical_discontinuity']['after_decision'],'NO_ADDITIONAL_RULE')
                self.assertIsNone(second['high_resolution_actor_event'])
                world=cold.ledger.world()[1]
                period=world['historical_periods'][-1]
                held=period['structurally_withheld_processes']
                self.assertEqual(len(held),1)
                self.assertEqual(held[0]['operation'],'CARE')
                self.assertEqual(held[0]['objective_rule_evaluation']['decision'],'BLOCKED')
                self.assertEqual(held[0]['source_ref'],rows[0]['source_ref'])
                self.assertEqual(held[0]['actual_time_lost_or_actor_experience'],'NOT_INFERRED')
                self.assertEqual(period['care_period_refs'],[])
                self.assertEqual([x['kind'] for x in period['processes']],['QUALIFIED_ROUTINE_PRACTICE'])
                self.assertEqual(period['actor_time_claims']['mother'],3.0)
                child=cold.snapshot('nadia')
                self.assertEqual(child['age_days'],6)
                self.assertEqual(child['undergone_care_periods'],first_child['undergone_care_periods'])
                self.assertEqual(child['evidence_paths'],[])
                parent=cold.snapshot('mother')
                self.assertEqual(len(parent['practice_exposures']),2)
                self.assertGreater(situated_component_efficacy(parent,'PRACTICE','home')['provisional_exposure_dose'],
                                   situated_component_efficacy(first_parent,'PRACTICE','home')['provisional_exposure_dose'])
                third=cold.advance_to_discontinuity(horizon=3,processes=rows)
                self.assertIsNone(third['historical_discontinuity'])
                child=cold.snapshot('nadia')
                self.assertEqual(child['age_days'],9)
                self.assertEqual(len(child['undergone_care_periods']),2)
                self.assertEqual(child['evidence_paths'],[])
                self.assertEqual(child['memories'],[])
                self.assertEqual(child['co_regulation_orientations'],[])
                self.assertEqual(len(cold.snapshot('mother')['practice_exposures']),3)
                self.assertTrue(cold.verify()['valid'])
            finally:cold.close()

    def test_same_rule_bites_actual_care_and_expiry_does_not_create_experience(self):
        with tempfile.TemporaryDirectory() as d:
            rt,rows=self.initialize(str(Path(d)/'actual'))
            try:
                rt.advance_to_discontinuity(horizon=6,processes=rows)
                before=rt.snapshot('nadia')
                blocked=rt.step('mother',requested_action='CARE',target='nadia')
                self.assertEqual(blocked['status'],'BLOCKED')
                child=rt.snapshot('nadia')
                self.assertEqual(child['undergone_care_periods'],before['undergone_care_periods'])
                self.assertEqual(child['body']['comfort'],before['body']['comfort'])
                # After the actual obstruction, time can pass without
                # retrospectively inventing care or a child's interpretation.
                rt.background(2)
                self.assertEqual(rt.ledger.world()[1]['clock'],6)
                performed=rt.step('mother',requested_action='CARE',target='nadia')
                self.assertEqual(performed['status'],'PERFORMED')
                self.assertGreater(rt.snapshot('nadia')['body']['comfort'],child['body']['comfort'])
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()
