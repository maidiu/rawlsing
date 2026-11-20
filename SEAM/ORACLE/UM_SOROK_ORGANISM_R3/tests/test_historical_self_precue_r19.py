"""SORACLE R19 sourcefree tests: P019/P022 lived organization in one organism.

These are candidate software-causality tests, not empirical developmental laws.
"""
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.types import adult, newborn, blank_world, AccessibleEncounter
from um_sorok_organism.constitution import materialize, compose
from um_sorok_organism.development import admit, InvalidDevelopment
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService


def lived(actor, event, action='SIGNAL', *, clock=1, cue=False):
    return {'actor': actor, 'ref': 'experienced:'+actor+':'+event,
            'clock':clock,'location':'home', 'own_action':action,
            'status':'PERFORMED', 'participated':True,
            'felt_enactment':{'attempted_operation':action,
                              'objective_result_not_inferred':True},
            'perceived_cues':([{'id':'signal:'+actor+':'+event,
                'modality':'auditory','tags':['uninterpreted_sound']}]
                if cue else []), 'actor_access_grade':'SOURCEFREE'}


def orientation(polarity='APPROACH',operation='SIGNAL',**additional):
    return {'kind':'ACQUIRE_HISTORICAL_ORIENTATION',
            'operation':operation,'orientation_mode':polarity,**additional}


def situated(actor):
    world=blank_world()
    world['positions'][actor['id']]='home'
    c=materialize(actor,world)
    access=AccessibleEncounter(actor=actor['id'],world_clock=0,
        location='home',cues=[],affordances=[],access_receipts=[])
    return compose(c,access)


def option(s,action='SIGNAL'):
    return next((x for x in s.candidate_actions if x['action']==action),None)


class HistoricalSelfAndPrecueR19(unittest.TestCase):
    def test_same_world_different_histories_and_no_history_control(self):
        approach=adult('approach','A'); withhold=adult('withhold','B')
        control=adult('control','C')
        admit(approach,lived('approach','e1'),'world:e1',
              [orientation('APPROACH')])
        admit(withhold,lived('withhold','e2'),'world:e2',
              [orientation('WITHHOLD')])
        a=situated(approach); b=situated(withhold); c=situated(control)
        self.assertEqual(a.accessible_cues,[])
        self.assertEqual(b.accessible_cues,[])
        self.assertTrue(any(x['kind']=='HISTORICALLY_RECRUITED_PRE_CUE_PRESSURE'
                            for x in a.currents))
        self.assertEqual(option(a)['psychodynamic_status'],
                         'ACQUIRED_APPROACH_WITHOUT_RECORDED_COUNTERCURRENT')
        self.assertIsNone(option(b))
        self.assertTrue(any(x['action']=='SIGNAL' for x in b.suspended_actions))
        self.assertFalse(any(x['kind']=='HISTORICALLY_RECRUITED_PRE_CUE_PRESSURE'
                             for x in c.currents))
        self.assertLess(option(c)['score'],option(a)['score'])

    def test_identical_ambiguous_cue_differently_recruits_lived_attention(self):
        # No present semantic cue names the learned action; both face the same
        # unclassified auditory event. Only their own lived history differs.
        one=adult('one','One'); two=adult('two','Two')
        unformed=adult('unformed','Unformed')
        admit(one,lived('one','first',cue=True),'world:first',
              [orientation('APPROACH',perceived_cue_ref='signal:one:first')])
        admit(two,lived('two','first',cue=True),'world:second',
              [orientation('WITHHOLD',perceived_cue_ref='signal:two:first')])
        cue={'id':'current:ambiguous','kind':'unclassified',
             'tags':['not_previously_named'],'modality':'auditory'}
        def encountered(actor):
            world=blank_world()
            world['positions'][actor['id']]='home'
            a=AccessibleEncounter(actor=actor['id'],world_clock=9,
                location='home',cues=[cue],affordances=[],
                access_receipts=['current:ambiguous'])
            return compose(materialize(actor,world),a)
        a,b,c=map(encountered,(one,two,unformed))
        self.assertIsNotNone(option(a))
        self.assertIsNone(option(b))
        self.assertTrue(a.attention_frame['historical_sensory_bias_is_provisional'])
        self.assertTrue(b.attention_frame['historical_sensory_bias_is_provisional'])
        self.assertFalse(c.attention_frame['historical_sensory_bias_is_provisional'])
        self.assertFalse(any(x['kind']=='HISTORICALLY_RECRUITED_PRE_CUE_PRESSURE'
                             for x in c.currents))

    def test_cue_absence_precedes_categorization_and_revision_retains_history(self):
        actor=adult('a','A')
        first=admit(actor,lived('a','first'),'world:first',
                    [orientation('APPROACH')])[0]['ref']
        earlier=situated(actor)
        self.assertIsNotNone(option(earlier))
        e2=lived('a','second',clock=2)
        admit(actor,e2,'world:second',[{'kind':'REVISE_HISTORICAL_ORIENTATION',
            'orientation_ref':first,'revision_mode':'INHIBIT'}])
        later=situated(actor)
        self.assertEqual(len(actor['historical_orientations']),1)
        self.assertEqual(actor['historical_orientations'][0]['origin_event'],'world:first')
        self.assertEqual(actor['historical_orientations'][0]['revisions'][0]['event'],
                         'world:second')
        self.assertFalse(any(x['ref']==first for x in later.currents
                              if x['kind']=='HISTORICALLY_RECRUITED_PRE_CUE_PRESSURE'))
        admit(actor,lived('a','third',clock=3),'world:third',
              [{'kind':'REVISE_HISTORICAL_ORIENTATION',
                'orientation_ref':first,'revision_mode':'REINSTATE'}])
        self.assertTrue(any(x['ref']==first for x in situated(actor).currents
                            if x['kind']=='HISTORICALLY_RECRUITED_PRE_CUE_PRESSURE'))

    def test_operative_self_requires_prior_practice_and_changes_next_composition(self):
        actor=adult('self','S')
        first=admit(actor,lived('self','e1'),'world:e1',
                    [orientation('APPROACH')])[0]['ref']
        old=option(situated(actor))['psychodynamic_status']
        self.assertEqual(old,'ACQUIRED_APPROACH_WITHOUT_RECORDED_COUNTERCURRENT')
        self_record=admit(actor,lived('self','e2',clock=2),'world:e2',
            [{'kind':'ACTOR_SELF_MODEL',
              'claim':'I may have to hold back when I am asked to signal.',
              'source_orientation_ref':first,'operative_action':'SIGNAL',
              'orientation_mode':'WITHHOLD'}])[0]
        self.assertEqual(self_record['status'],
                         'OPERATIVE_HISTORICALLY_CONDITIONED_HYPOTHESIS')
        changed=option(situated(actor))
        self.assertEqual(changed['psychodynamic_status'],
                         'UNRESOLVED_CONTRADICTION')
        self.assertEqual(len(changed['opposed_currents']['approach']),1)
        self.assertEqual(len(changed['opposed_currents']['withhold']),1)
        self.assertEqual(len(actor['self_model']['operative']),1)
        self.assertEqual(len(actor['projects']),0)
        self_ref=self_record['ref']
        admit(actor,lived('self','e3',clock=3),'world:e3',
              [{'kind':'REVISE_OPERATIVE_SELF_ORGANIZATION',
                'self_organization_ref':self_ref,'revision_mode':'INHIBIT'}])
        self.assertEqual(option(situated(actor))['psychodynamic_status'],old)
        self.assertEqual(len(actor['self_model']['operative'][0]['revisions']),1)

    def test_independent_opposed_histories_not_harmonized(self):
        actor=adult('contradict','D')
        admit(actor,lived('contradict','a'),'world:a',[orientation('APPROACH')])
        admit(actor,lived('contradict','b',clock=2),'world:b',[orientation('WITHHOLD')])
        s=situated(actor)
        self.assertEqual(option(s)['psychodynamic_status'],
                         'UNRESOLVED_CONTRADICTION')
        self.assertEqual(len([x for x in s.currents
                if x['kind']=='HISTORICALLY_RECRUITED_PRE_CUE_PRESSURE']),2)

    def test_preverbal_nadia_has_nonverbal_pressure_not_adult_self(self):
        child=newborn('nadia','Nadia')
        row=admit(child,lived('nadia','s1',cue=True),'world:s1',
            [orientation('APPROACH',perceived_cue_ref='signal:nadia:s1')])[0]
        self.assertEqual(row['kind'],'ACQUIRE_HISTORICAL_ORIENTATION')
        self.assertEqual(child['historical_orientations'][0]['access'],'NONDECLARATIVE')
        self.assertTrue(any(x['kind']=='HISTORICALLY_RECRUITED_PRE_CUE_PRESSURE'
                            for x in situated(child).currents))
        with self.assertRaises(InvalidDevelopment):
            admit(child,lived('nadia','s2',clock=2),'world:s2',
                [{'kind':'ACTOR_SELF_MODEL','claim':'I am brave',
                  'operative_action':'SIGNAL','source_orientation_ref':row['ref'],
                  'orientation_mode':'APPROACH'}])
        self.assertEqual(child['self_model'],{})

    def test_qualifications_forgery_no_cross_actor_and_no_new_rights(self):
        a=adult('a','A'); b=adult('b','B')
        before=repr(a)
        with self.assertRaises(InvalidDevelopment):
            admit(a,lived('b','foreign'),'world:foreign',
                  [orientation('APPROACH')])
        with self.assertRaises(InvalidDevelopment):
            admit(a,lived('a','phantom'),'world:phantom',
                  [orientation('APPROACH',perceived_cue_ref='unseen')])
        with self.assertRaises(InvalidDevelopment):
            admit(a,lived('a','teleport'),'world:teleport',
                  [orientation('APPROACH',operation='TELEPORT')])
        with self.assertRaises(InvalidDevelopment):
            admit(a,lived('a','dup'),'world:dup',
                  [orientation('APPROACH'),orientation('WITHHOLD')])
        self.assertEqual(repr(a),before)
        self.assertEqual(b['historical_orientations'],[])
        self.assertEqual(a['projects'],[])
        self.assertEqual(a['other_models'],{})

    def test_self_model_strings_still_do_not_grant_agency(self):
        actor=adult('a','A')
        admit(actor,lived('a','e1'),'world:e1',
              [{'kind':'ACTOR_SELF_MODEL','claim':'I am omnipotent'}])
        self.assertEqual(actor['self_model'].get('operative',[]),[])
        self.assertFalse(any(x['kind']=='HISTORICALLY_RECRUITED_PRE_CUE_PRESSURE'
                             for x in situated(actor).currents))
        with self.assertRaises(InvalidDevelopment):
            admit(actor,lived('a','e2'),'world:e2',
                  [{'kind':'ACTOR_SELF_MODEL','claim':'I can teleport',
                    'operative_action':'TELEPORT',
                    'source_orientation_ref':'invented',
                    'orientation_mode':'APPROACH'}])

    def test_cannot_turn_one_experience_into_full_self_model_or_motive(self):
        actor=adult('a','A')
        first=admit(actor,lived('a','e1'),'world:e1',
                    [orientation('APPROACH')])[0]['ref']
        before=repr(actor)
        with self.assertRaises(InvalidDevelopment):
            admit(actor,lived('a','e1'),'world:e1',
                  [{'kind':'ACTOR_SELF_MODEL','claim':'I am this',
                    'operative_action':'SIGNAL','source_orientation_ref':first,
                    'orientation_mode':'APPROACH'}])
        self.assertEqual(before,repr(actor))
        self.assertEqual(len(actor['projects']),0)

    def test_sqlite_cold_restart_preserves_operative_pre_cue_pressure(self):
        with tempfile.TemporaryDirectory() as d:
            db=str(Path(d)/'one_life.sqlite3')
            def callback(task,packet):
                if task=='development':
                    experience=packet['experience']
                    if (experience['actor']=='nadia' and
                            experience.get('own_action')=='SIGNAL'):
                        return {'task':task,'candidates':[orientation('APPROACH')]}
                    return {'task':task,'candidates':[]}
                if task=='expression':
                    return {'task':task,'surface':'A signal was heard.'}
                if task=='actor_attempt':
                    return {'task':task,'action':'WAIT'}
                raise AssertionError(task)
            service=ValidatingSemanticService(CallbackLLMProvider(callback))
            rt=ConstitutiveRuntime(db,semantic=service)
            try:
                rt.initialize()
                before=rt.situated('nadia')
                self.assertFalse(any(x['kind']=='HISTORICALLY_RECRUITED_PRE_CUE_PRESSURE'
                                     for x in before['currents']))
                rt.step('nadia',requested_action='SIGNAL')
                after=rt.situated('nadia')
                self.assertTrue(any(x['kind']=='HISTORICALLY_RECRUITED_PRE_CUE_PRESSURE'
                                    for x in after['currents']))
                self.assertTrue(rt.verify())
            finally:
                rt.close()
            cold=ConstitutiveRuntime(db)
            try:
                restored=cold.situated('nadia')
                self.assertTrue(any(x['kind']=='HISTORICALLY_RECRUITED_PRE_CUE_PRESSURE'
                                    for x in restored['currents']))
                self.assertTrue(cold.verify())
            finally:
                cold.close()


if __name__=='__main__':
    unittest.main()
