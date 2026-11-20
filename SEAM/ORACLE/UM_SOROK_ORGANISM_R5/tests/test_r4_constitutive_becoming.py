"""TCO R4 adversarial tests: material participation generates future differences.

These are executable sourcefree counterexamples and conservative engineering
contracts, NOT evidence of a human developmental or affective law.
"""
import tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.activity import record_activity_afterlife
from um_sorok_organism.plans import propose_compositions
from um_sorok_organism.becoming import LivedDifferenceKernel
from um_sorok_organism.semantics import HeuristicSemanticProvider,CallbackLLMProvider,ValidatingSemanticService
from um_sorok_organism.types import copy


def project_packet():
    return {'source_ref':'R4_FICTIONAL_CASE_NOT_POPULATION_DATA',
     'answers':{'work':'uncertain'},'fictional_seed':{'projects':[
       {'object':'repair a workshop for collective use','means':['REPAIR','WORK'],
        'priority':.95,'cue_terms':['repair','stock'],'status':'active'}]}}


class TCOConstitutiveR4(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=str(Path(self.tmp.name)/'living.db')
        self.rt=None
    def tearDown(self):
        if self.rt:self.rt.close()
        self.tmp.cleanup()

    def create(self,packet=None,provider=None,becoming=None):
        self.rt=ConstitutiveRuntime(self.path,provider,becoming=becoming)
        self.rt.initialize([('worker','Worker',packet or project_packet())])
        return self.rt

    def project(self):
        return next(p['id'] for p in self.rt.ledger.actor('worker')[1]['projects']
                    if 'repair a workshop' in p['object'])

    def research_world_stock(self,value):
        """Explicitly audited world-state test fixture, not actor perception."""
        v,w=self.rt.ledger.world()
        w['sites']['workshop']['stock']=value
        self.rt.ledger.commit(self.rt.world_id,v,w,{}, {},
           'EXTERNAL_RESEARCH_STOCK_FIXTURE',None,{'stock':value,'not_actor_knowledge':True})

    def test_blocked_attempt_persists_objective_and_lived_separately(self):
        def actor(task,packet):
            if task=='actor_attempt':return {'action':'REPAIR','project_ids':[self.project()]}
            return HeuristicSemanticProvider().propose(task,packet)
        self.create(provider=ValidatingSemanticService(CallbackLLMProvider(actor)))
        self.rt.step('worker',requested_action='MOVE',object_ref='workshop')
        self.research_world_stock(0)
        r=self.rt.step('worker')
        self.assertEqual(r['status'],'BLOCKED')
        person=self.rt.ledger.actor('worker')[1]
        obj=person['activity_history'][-1];lived=person['lived_activity_history'][-1]
        self.assertEqual(obj['performed_status'],'BLOCKED')
        self.assertEqual(obj['objective_outcome'],'MISSING_REPAIR_MATERIAL')
        self.assertEqual(lived['somatic_course'],'INTERRUPTED')
        self.assertEqual(lived['objective_outcome'],'NOT_INFERRED')
        self.assertNotIn('MISSING_REPAIR_MATERIAL',str(lived))
        self.assertEqual(person['projects'][0]['latest_lived_attempt'],lived)
        self.assertEqual(self.rt.situated('worker')['currents'][0]['kind'],'ONGOING_ACTIVITY')
        self.assertTrue(self.rt.verify()['valid'])
        self.rt.close();self.rt=None
        reopened=ConstitutiveRuntime(self.path)
        try:
            self.assertEqual(reopened.ledger.actor('worker')[1]['lived_activity_history'][-1],lived)
            self.assertTrue(reopened.verify()['valid'])
        finally:reopened.close()

    def test_duplicate_activity_preflight_is_atomic_even_in_memory(self):
        self.create()
        actor=self.rt.ledger.actor('worker')[1]
        actor['projects']=[{'id':'a','object':'first','means':['WORK']},
                           {'id':'b','object':'second','means':['WORK'],
                            'operational_history':[{'event':'already'}]}]
        before=copy(actor)
        with self.assertRaisesRegex(ValueError,'DUPLICATE_ACTIVITY_EVENT_FOR_PROJECT'):
            record_activity_afterlife(actor,'WORK','PARTIAL','OBJECTIVE_CAUSE',
                ['project:a','project:b'],'already')
        self.assertEqual(actor,before)

    def test_ambiguous_shared_operation_does_not_forge_dual_intention(self):
        packet={'source_ref':'R4_DOUBLE_PURPOSE_FIXTURE','answers':{'work':'uncertain'},'fictional_seed':{
          'projects':[{'object':'earn wages','means':['WORK'],'priority':1},
                      {'object':'help a friend','means':['WORK'],'priority':.9}]}}
        self.create(packet)
        r=self.rt.step('worker')
        self.assertEqual(r['attempt'],'WORK')
        self.assertEqual(self.rt.ledger.actor('worker')[1].get('activity_history',[]),[])
        self.assertTrue(self.rt.verify()['valid'])

    def test_forged_model_project_intention_is_rejected_no_world_mutation(self):
        def actor(task,packet):
            if task=='actor_attempt':return {'action':'REPAIR','project_ids':['a_stolen_project']}
            return HeuristicSemanticProvider().propose(task,packet)
        self.create(provider=ValidatingSemanticService(CallbackLLMProvider(actor)))
        before=self.rt.verify()['events']
        with self.assertRaisesRegex(ValueError,'MODEL_PROJECT_INTENTION_NOT_SUPPORTED'):
            self.rt.step('worker')
        self.assertEqual(self.rt.verify()['events'],before)

    def test_foreign_means_not_laundered_into_any_project(self):
        options=[{'action':'WORK','basis':['project:job']},
                 {'action':'REPAIR','basis':['project:job']},
                 {'action':'SING','basis':['project:music']},
                 {'action':'PRACTICE','basis':['project:music']}]
        currents=[{'kind':'ONGOING_ACTIVITY','ref':'job','object':'repair things',
                   'means':['WORK','REPAIR']},
                  {'kind':'ONGOING_ACTIVITY','ref':'music','object':'share rhythm',
                   'means':['SING','PRACTICE']},
                  {'kind':'ONGOING_ACTIVITY','ref':'third','object':'unknown',
                   'means':['SING','WORK']}]
        got=propose_compositions(SimpleNamespace(actor='worker',currents=currents,
                                      candidate_actions=options,learned_compositions=[]))
        self.assertEqual({r.object for r in got},{'repair things','share rhythm'})
        self.assertTrue(all(not any(x.startswith('project:') and x!='project:'+('job' if r.object=='repair things' else 'music')
                                        for x in r.basis) for r in got))

    def test_repeated_personal_contrast_changes_future_attention_not_motive(self):
        sequence=iter(['REPAIR','WORK','REPAIR'])
        def actor(task,packet):
            if task=='actor_attempt':return {'action':next(sequence),'project_ids':[self.project()]}
            return HeuristicSemanticProvider().propose(task,packet)
        self.create(provider=ValidatingSemanticService(CallbackLLMProvider(actor)))
        self.rt.step('worker',requested_action='MOVE',object_ref='workshop')
        self.research_world_stock(0)
        for i in range(3):self.rt.step('worker')
        person=self.rt.ledger.actor('worker')[1]
        self.assertEqual(len(person['acquired_discriminations']),1)
        d=next(iter(person['acquired_discriminations'].values()))
        self.assertEqual(d['courses'],['CONTINUED','INTERRUPTED'])
        self.assertEqual(d['interpretation'],'OPEN_NOT_CAUSALLY_EXPLAINED')
        self.assertEqual(len(d['origin_events']),2)
        self.assertTrue(any(x['kind']=='HISTORY_CONDITIONED_ATTENTION'
                            for x in self.rt.situated('worker')['currents']))
        self.assertFalse(person['composition_methods'])
        self.assertEqual(len(person['historical_composition_methods']),0)

    def test_two_separate_earned_practical_sequences_generate_and_exercise_method(self):
        sequence=iter(['REPAIR','WORK','REPAIR']*2)
        def actor(task,packet):
            if task=='actor_attempt':return {'action':next(sequence),'project_ids':[self.project()]}
            return HeuristicSemanticProvider().propose(task,packet)
        self.create(provider=ValidatingSemanticService(CallbackLLMProvider(actor)))
        self.rt.step('worker',requested_action='MOVE',object_ref='workshop')
        for i in range(2):
            for _ in range(3):self.rt.step('worker',requested_action='REST')
            self.research_world_stock(0)
            for j in range(3):self.rt.step('worker')
        person=self.rt.ledger.actor('worker')[1]
        self.assertEqual(len(person['historical_composition_methods']),1)
        m=next(iter(person['historical_composition_methods'].values()))
        self.assertEqual(m['operations'],['WORK','REPAIR'])
        self.assertEqual(len(m['source_events']),2)
        self.assertEqual(len({x for seq in m['source_events'] for x in seq}),6)
        derived=[x for x in self.rt.possible_composed_activities('worker')
                 if m['id'] in x['basis']]
        self.assertEqual(len(derived),1)
        self.assertIn('project:'+self.project(),derived[0]['basis'])
        # R4 actor continues its own learned procedure. Caller supplies NO action/plan.
        for _ in range(3):self.rt.step('worker',requested_action='REST')
        self.research_world_stock(0)
        after=self.rt.continue_life('worker')
        self.assertEqual([r['attempt'] for r in after['attempts']],['WORK','REPAIR'])
        self.assertTrue(all(r['selection_grade'].startswith('ACTOR_HISTORY_DERIVED')
                            for r in after['attempts']))
        self.assertTrue(self.rt.verify()['valid'])
        self.rt.close();self.rt=None
        reopened=ConstitutiveRuntime(self.path)
        try:
            self.assertIn(m['id'],reopened.ledger.actor('worker')[1]['historical_composition_methods'])
            self.assertTrue(any(m['id'] in x['basis'] for x in
                                reopened.possible_composed_activities('worker')))
            self.assertTrue(reopened.verify()['valid'])
        finally:reopened.close()

    def test_false_temporal_succession_cannot_invent_material_enabling_means(self):
        # An initial naive R4 would acquire SING->REPAIR simply because an
        # external world fixture secretly replenished stock between operations.
        # The revised world-qualified genesis requires B's *actual* material
        # affordance delta to support A's previously failed condition.
        packet={'source_ref':'R4_FALSE_CAUSATION_FIXTURE','answers':{'work':'uncertain'},
             'fictional_seed':{'projects':[{'object':'repair an institution',
                  'means':['REPAIR','SING'],'priority':.95,'cue_terms':['repair','song']}]}}
        sequence=iter(['REPAIR','SING','REPAIR']*2)
        def actor(task,packet):
            if task=='actor_attempt':
                ident=next(p['id'] for p in self.rt.ledger.actor('worker')[1]['projects']
                           if p['object']=='repair an institution')
                return {'action':next(sequence),'project_ids':[ident]}
            return HeuristicSemanticProvider().propose(task,packet)
        self.create(packet,ValidatingSemanticService(CallbackLLMProvider(actor)))
        self.rt.step('worker',requested_action='MOVE',object_ref='workshop')
        for _ in range(2):
            for __ in range(2):self.rt.step('worker',requested_action='REST')
            self.research_world_stock(0)
            blocked=self.rt.step('worker')
            self.assertEqual(blocked['status'],'BLOCKED')
            unrelated=self.rt.step('worker')
            self.assertEqual(unrelated['attempt'],'SING')
            self.research_world_stock(2) # independent, not caused by singing
            success=self.rt.step('worker')
            self.assertEqual(success['status'],'PERFORMED')
        person=self.rt.ledger.actor('worker')[1]
        self.assertEqual(person['historical_composition_methods'],{})
        self.assertEqual(self.rt.continue_life('worker')['attempts'],[])
        self.assertTrue(self.rt.verify()['valid'])

    def test_ordinary_co_presence_without_bodily_contingency_does_not_create_attachment(self):
        self.create()
        for _ in range(3):self.rt.step('nadia',requested_action='SIGNAL')
        n=self.rt.ledger.actor('nadia')[1]
        self.assertEqual(n['nonconceptual_orientations'],{})
        self.assertFalse(any(c['kind']=='NONCONCEPTUAL_ACQUIRED_ORIENTATION'
                             for c in self.rt.situated('nadia')['currents']))
        self.assertTrue(self.rt.verify()['valid'])

    def test_absent_history_never_generates_magic_second_order_method(self):
        self.create()
        self.assertEqual(self.rt.ledger.actor('worker')[1]['historical_composition_methods'],{})
        r=self.rt.continue_life('worker')
        self.assertEqual(r['attempts'],[])
        self.assertEqual(r['reason'],'NO_QUALIFIED_ACQUIRED_METHOD')
        self.assertEqual(self.rt.verify()['events'],1)

    def test_infant_care_contingency_orients_attention_without_inventing_love(self):
        packet={'source_ref':'R4_CARE_FIXTURE','answers':{'work':'uncertain'},'fictional_seed':{
          'projects':[{'object':'respond to infant signal','means':['CARE'],
                       'priority':.99,'cue_terms':['signal','care']}]}}
        self.create(packet)
        before=self.rt.snapshot('nadia')
        self.assertEqual(before['forms'],{})
        for _ in range(2):
            resp=self.rt.step('nadia',requested_action='SIGNAL',target='worker')
            self.assertEqual(resp['objective_outcome'],'JOINT_ACTIVITY_PERFORMED')
        nadia=self.rt.ledger.actor('nadia')[1]
        self.assertEqual(len(nadia['nonconceptual_orientations']),1)
        self.assertEqual(nadia['body']['language'],0)
        orient=next(iter(nadia['nonconceptual_orientations'].values()))
        self.assertTrue(orient['not_attachment_or_other_intention'])
        a=self.rt.see('nadia')
        self.assertTrue(any(orient['id'] in c.get('actor_attention_refs',[]) for c in a['cues']))
        self.assertTrue(any(c['kind']=='NONCONCEPTUAL_ACQUIRED_ORIENTATION'
                            for c in self.rt.situated('nadia')['currents']))
        self.assertEqual(nadia['other_models'].get('worker',{}).get('affection'),None)
        self.assertTrue(self.rt.verify()['valid'])

    def test_attention_orientations_do_not_mint_inaccessible_other(self):
        self.create()
        wv,w=self.rt.ledger.world()
        a=self.rt.ledger.actor('worker')[1]
        a['nonconceptual_orientations']={'old':{'id':'old','actor':'worker',
                       'other':'unknown_person','cue_terms':['unknown_person'],
                       'source_experience_refs':['exp_old']}}
        from um_sorok_organism.constitution import actor_access
        access=actor_access(a,w)
        self.assertFalse(any('old' in c.get('actor_attention_refs',[]) for c in access.cues))
        self.assertTrue(self.rt.verify()['valid'])

    def test_kernel_can_be_replaced_without_rewriting_world_history(self):
        class NoPrivateOrientationKernel(LivedDifferenceKernel):
            version='TCO_R5_PROPOSED_ALTERNATIVE_TEST'
            def orient(self,const,access):return [],[]
        self.create(becoming=NoPrivateOrientationKernel())
        self.assertEqual(self.rt.becoming.version,'TCO_R5_PROPOSED_ALTERNATIVE_TEST')
        self.assertTrue(self.rt.verify()['valid'])

if __name__=='__main__':unittest.main()
