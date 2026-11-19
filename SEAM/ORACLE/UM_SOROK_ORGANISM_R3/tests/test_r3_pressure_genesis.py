"""R3 adversarial construction checks: no automatic 'real psychology' conclusion."""
import tempfile,unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.psychodynamics import enact_currents
from um_sorok_organism.constitution import materialize,actor_access,compose
from um_sorok_organism.development import admit, InvalidDevelopment
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService,HeuristicSemanticProvider


def parent(polarities):
    return {'source_ref':'R3_RESEARCH_FIXTURE_NOT_REAL',
        'answers':{'work':'uncertain'},
        'fictional_seed':{'acquired_forms':[
          {'kind':'PRACTICE','content':'sing as usable means','cues':['care','song','home'],
           'enables':['SING'],'scope':{'locations':['home']},
           'tendencies':[{'action':'SING','polarity':p} for p in polarities[:1]]},
          {'kind':'TENSION','content':'historically acquired avoidance of being heard',
           'cues':['care','home'],'enables':[], 'scope':{'locations':['home']},
           'tendencies':[{'action':'SING','polarity':p} for p in polarities[1:]]},
          {'kind':'PRACTICE','content':'caregiving through concrete action','cues':['care','home'],
           'enables':['CARE'],'scope':{'locations':['home']}}],
          'projects':[{'object':'care in household and perhaps sing',
           'means':(['SING'] if polarities==['APPROACH','WITHHOLD'] else ['SING','CARE']),'priority':.95,'cue_terms':['care','home']}]}}

class PressureAndGenesis(unittest.TestCase):
    def _runtime(self,ps,provider=None):
        self.tmp=tempfile.TemporaryDirectory()
        self.db=str(Path(self.tmp.name)/'r3.db')
        self.rt=ConstitutiveRuntime(self.db,provider)
        self.rt.initialize([('mother','Mother',parent(ps))])
        return self.rt
    def tearDown(self):
        if hasattr(self,'rt'):self.rt.close()
        if hasattr(self,'tmp'):self.tmp.cleanup()

    def test_without_historical_tendencies_same_surface_activity_remains_possible(self):
        r=self._runtime([])
        a=r.situated('mother')
        self.assertIn('SING',{x['action'] for x in a['candidate_actions']})
        self.assertFalse(a['antagonisms'])
        self.assertFalse(a['suspended_actions'])

    def test_only_qualified_withholding_suspends_actor_generated_action(self):
        r=self._runtime(['WITHHOLD'])
        a=r.situated('mother')
        self.assertNotIn('SING',{x['action'] for x in a['candidate_actions']})
        self.assertTrue(any(x['action']=='SING' for x in a['suspended_actions']))
        self.assertIn('CARE',{x['action'] for x in a['candidate_actions']})
        self.assertTrue(any(c['kind']=='ACQUIRED_ACTION_CURRENT' for c in a['currents']))

    def test_simultaneous_opposing_currents_neither_erase_nor_merge(self):
        r=self._runtime(['APPROACH','WITHHOLD'])
        a=r.situated('mother')
        self.assertEqual(len(a['antagonisms']),1)
        self.assertEqual(a['antagonisms'][0]['resolution'],'UNDETERMINED; NO FORCED HARMONY')
        singing=next(x for x in a['candidate_actions'] if x['action']=='SING')
        self.assertEqual(singing['psychodynamic_status'],'UNRESOLVED_CONTRADICTION')
        self.assertEqual(len(singing['opposed_currents']['approach']),1)
        self.assertEqual(len(singing['opposed_currents']['withhold']),1)
        self.assertFalse(any(x['action']=='SING' for x in a['suspended_actions']))
        self.assertEqual(r.step('mother')['attempt'],'WAIT')  # declared HEURISTIC, not human law
        self.assertEqual(r.verify()['valid'],True)

    def test_contextual_withholding_cannot_follow_form_outside_its_scope(self):
        r=self._runtime(['WITHHOLD'])
        _,w=r.ledger.world();_,a=r.ledger.actor('mother')
        w['positions']['mother']='workshop'; a['location']='workshop'
        context=compose(materialize(a,w),actor_access(a,w))
        self.assertFalse(any(x['action']=='SING' for x in context.suspended_actions))
        self.assertFalse(any(x['kind']=='ACQUIRED_ACTION_CURRENT' for x in context.currents))

    def test_same_acquired_means_later_become_new_learned_composition(self):
        def provider(task,packet):
            if task=='adult_constructor':return HeuristicSemanticProvider().propose(task,packet)
            if task=='development' and packet['actor']['id']=='mother' and packet['experience'].get('own_action')=='CARE':
                fs=packet['actor_forms']
                singer=next(fid for fid,f in fs.items() if 'SING' in f.get('enables',[]))
                carer=next(fid for fid,f in fs.items() if 'CARE' in f.get('enables',[]))
                return {'task':task,'candidates':[{'kind':'ACQUIRE_COMPOSITION_METHOD',
                   'source_forms':[singer,carer],'operations':['CARE','SING'],
                   'hypothesized_end':'experiment with alternating care and song',
                   'locations':['home']} ]}
            if task=='development':return {'task':task,'candidates':[]}
            if task=='actor_attempt':return {'task':task,'action':'WAIT'}
            return {'task':task,'surface':'opaque'}
        r=self._runtime([],ValidatingSemanticService(CallbackLLMProvider(provider)))
        before=r.possible_composed_activities('mother')
        self.assertFalse(any(tuple(x['steps'])==('CARE','SING') for x in before))
        r.step('mother',requested_action='CARE',target='nadia')
        after=r.possible_composed_activities('mother')
        new=[x for x in after if tuple(x['steps'])==('CARE','SING')]
        self.assertEqual(len(new),1)
        self.assertIn('alternating',new[0]['object'])
        self.assertEqual(len(r.ledger.actor('mother')[1]['composition_methods']),1)
        self.assertTrue(r.verify()['valid'])
        reopened=ConstitutiveRuntime(self.db)
        try:
            self.assertEqual(after,reopened.possible_composed_activities('mother'))
        finally:reopened.close()

    def test_learned_method_not_exercisable_without_its_current_means(self):
        # Sourcefree research actor has two acquired forms and an accepted
        # methods record, but the situational body and form scopes still gate it.
        def seeded(task,packet):
            if task=='adult_constructor':return HeuristicSemanticProvider().propose(task,packet)
            if task=='development' and packet['actor']['id']=='mother':
                fs=packet['actor_forms']
                src=[next(fid for fid,f in fs.items() if action in f.get('enables',[]))
                     for action in ('CARE','SING')]
                return {'task':task,'candidates':[{'kind':'ACQUIRE_COMPOSITION_METHOD',
                      'source_forms':src,'operations':['CARE','SING'],
                      'hypothesized_end':'care and song together','locations':['home']} ]}
            if task=='development':return {'task':task,'candidates':[]}
            if task=='actor_attempt':return {'task':task,'action':'WAIT'}
            return {'task':task,'surface':'uncertain'}
        r=self._runtime([],ValidatingSemanticService(CallbackLLMProvider(seeded)))
        r.step('mother',requested_action='CARE',target='nadia')
        assert r.situated('mother')['learned_compositions']
        _,w=r.ledger.world();_,a=r.ledger.actor('mother')
        w['positions']['mother']='workshop';a['location']='workshop'
        context=compose(materialize(a,w),actor_access(a,w))
        self.assertEqual(context.learned_compositions,[])
        # No world mutation was performed by this read-only prospect.
        self.assertEqual(r.see('mother')['location'],'home')

    def test_invalid_seed_dynamics_fail_without_genesis(self):
        x=parent([])
        x['fictional_seed']['acquired_forms'][0]['tendencies']=[
           {'action':'SING','polarity':'GLOBAL_HARMONY'}]
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'bad.db'))
            try:
                with self.assertRaisesRegex(ValueError,'INVALID_ACQUIRED_TENDENCIES'):
                    rt.initialize([('mother','Mother',x)])
                self.assertEqual(rt.ledger.events(),[])
            finally:rt.close()

    def test_cannot_relabel_unearned_second_order_genesis_as_learning(self):
        r=self._runtime([])
        actor=r.ledger.actor('mother')[1]
        ids=list(actor['forms'])
        singer=next(fid for fid,f in actor['forms'].items() if 'SING' in f.get('enables',[]))
        carer=next(fid for fid,f in actor['forms'].items() if 'CARE' in f.get('enables',[]))
        experience={'actor':'mother','ref':'feltA','participated':True,'status':'PERFORMED',
                    'felt_enactment':{'attempted_operation':'CARE'},'perceived_cues':[]}
        with self.assertRaisesRegex(InvalidDevelopment,'COMPOSITION_NEEDS_TWO_ACQUIRED_FORMS'):
            admit(actor,experience,'objA',[{'kind':'ACQUIRE_COMPOSITION_METHOD',
               'source_forms':[singer,'not_acquired'],'operations':['CARE','SING'],
               'hypothesized_end':'impossible magic'}])
        with self.assertRaisesRegex(InvalidDevelopment,'COMPOSITION_NOT_AN_EXISTING_TWO_MEANS'):
            admit(actor,experience,'objA',[{'kind':'ACQUIRE_COMPOSITION_METHOD',
               'source_forms':[singer,carer],'operations':['CARE','TELEPORT'],
               'hypothesized_end':'magic'}])
        with self.assertRaisesRegex(InvalidDevelopment,'COMPOSITION_NEEDS_OWN_PERFORMED_ENCOUNTER'):
            admit(actor,{**experience,'felt_enactment':None},'objA',
               [{'kind':'ACQUIRE_COMPOSITION_METHOD','source_forms':[singer,carer],
                 'operations':['CARE','SING'],'hypothesized_end':'unsupported'}])
        self.assertEqual(actor['composition_methods'],[])

if __name__=='__main__':unittest.main()
