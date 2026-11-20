"""R5 adversarial TCO reconstruction: relation alters actual possibility, not only prose."""
import tempfile, unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import copy
from um_sorok_organism.activity import record_activity_afterlife, register_lived_activity_attempt
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService, HeuristicSemanticProvider


def packet(relation='INSTRUMENTALIZES', target_scope=None, link_contexts=None, extra_links=None, action='PRACTICE'):
    return {'source_ref':'R5_TCO_CONSTITUTIVE_LINK_TEST_NO_EMPIRICAL_LAW',
      'answers':{'legitimation':'fictional'},
      'fictional_seed':{'acquired_forms':[
          {'kind':'PRACTICE','content':'care understood in context','cues':['home'],'enables':['CARE'],
           'scope':{'locations':['home']}},
          {'kind':'PRACTICE','content':'rarely cueable contingent practice','cues':['unencountered_rare_cue'],
           'enables':[action],'scope':target_scope or {'locations':['home']}}],
       'links':[{'source_index':0,'target_index':1,'relation':relation,
                 'contexts':link_contexts or []}]+(extra_links or []),
       'projects':[]}}


class TCOReconstruction(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=str(Path(self.tmp.name)/'r5.sqlite3')
        self.rt=None
    def tearDown(self):
        if self.rt:self.rt.close()
        self.tmp.cleanup()
    def create(self,p,provider=None,relational=None):
        self.rt=ConstitutiveRuntime(self.path,semantic=provider,relational=relational)
        self.rt.initialize([('adult','Adult',p)])
        return self.rt

    def test_relation_changes_available_practice_instead_of_merely_relabeling_it(self):
        def choice(task,content):
            if task=='actor_attempt':
                self.assertIn('PRACTICE',[x['action'] for x in content['options']])
                return {'action':'PRACTICE'}
            return HeuristicSemanticProvider().propose(task,content)
        self.create(packet(),ValidatingSemanticService(CallbackLLMProvider(choice)))
        s=self.rt.situated('adult')
        active=[c for c in s['currents'] if c['kind']=='ACQUIRED_RELATION_ENABLED_PRACTICE']
        self.assertEqual(len(active),1)
        self.assertTrue(active[0]['not_world_moral_verdict'])
        self.assertEqual(active[0]['relation'],'INSTRUMENTALIZES')
        prospective=next(o for o in s['candidate_actions'] if o['action']=='PRACTICE')
        self.assertTrue(prospective['relational_frames'])
        self.assertIn('relation:'+active[0]['ref'],prospective['basis'])
        before=self.rt.snapshot('adult')
        out=self.rt.step('adult')  # actor policy selects; NOT injected action
        self.assertEqual(out['attempt'],'PRACTICE')
        self.assertEqual(out['selection_grade'],'ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE')
        self.assertEqual(out['objective_outcome'],'SOLO_PRACTICE')
        self.assertEqual(set(before['forms']),set(self.rt.snapshot('adult')['forms']))
        self.assertTrue(self.rt.verify()['valid'])

    def test_no_link_means_no_rare_practice(self):
        p=packet();p['fictional_seed']['links']=[]
        self.create(p)
        self.assertNotIn('PRACTICE',[o['action'] for o in self.rt.situated('adult')['candidate_actions']])
        self.assertFalse(any(c['kind']=='ACQUIRED_RELATION_ENABLED_PRACTICE' for c in self.rt.situated('adult')['currents']))

    def test_context_and_bodily_scope_block_ideological_promotion(self):
        self.create(packet(link_contexts=['workshop']))
        self.assertNotIn('PRACTICE',[o['action'] for o in self.rt.situated('adult')['candidate_actions']])
        self.rt.close();self.rt=None
        self.path=str(Path(self.tmp.name)/'r5_alt.sqlite3')
        self.create(packet(target_scope={'locations':['workshop']}))
        self.assertNotIn('PRACTICE',[o['action'] for o in self.rt.situated('adult')['candidate_actions']])

    def test_explicit_inhibition_prevents_relation_laundering_direct_action(self):
        p=packet(extra_links=[{'source_index':0,'target_index':1,'relation':'INHIBITS','contexts':[]}])
        self.create(p)
        s=self.rt.situated('adult')
        self.assertNotIn('PRACTICE',[o['action'] for o in s['candidate_actions']])
        self.assertTrue(any(c['kind']=='LATENT_RELATIONAL_CONDITION' for c in s['currents']))
        self.assertTrue(s['inhibited'])

    def test_refunctioned_action_not_a_world_permission_or_money(self):
        def choice(task,content):
            if task=='actor_attempt':return {'action':'BUY_FOOD'}
            return HeuristicSemanticProvider().propose(task,content)
        self.create(packet(relation='JUSTIFIES',action='BUY_FOOD'),ValidatingSemanticService(CallbackLLMProvider(choice)))
        self.assertIn('BUY_FOOD',[o['action'] for o in self.rt.situated('adult')['candidate_actions']])
        out=self.rt.step('adult')
        self.assertEqual(out['attempt'],'BUY_FOOD')
        self.assertEqual(out['status'],'BLOCKED')
        self.assertEqual(out['objective_outcome'],'INSUFFICIENT_CLAIM_ON_FOOD')
        self.assertTrue(self.rt.verify()['valid'])

    def test_pluggable_older_relational_kernel_remains_safe(self):
        from um_sorok_organism.relational import RelationalKernel
        class PriorReading(RelationalKernel):
            version='LEGACY_COMPATIBLE_FRAME_ONLY'
            recruit=None
        self.create(packet(),relational=PriorReading())
        self.assertNotIn('PRACTICE',[o['action'] for o in self.rt.situated('adult')['candidate_actions']])

    def test_untyped_legacy_context_cannot_recruit_a_form_by_substring(self):
        # 'home' is a substring of 'homework'. Such string membership was a
        # real REMONTATHON R7 boundary fault, not a legitimate context match.
        p=packet()
        p['fictional_seed']['links'][0]['contexts']='homework'
        self.create(p)
        self.assertNotIn('PRACTICE',[o['action'] for o in self.rt.situated('adult')['candidate_actions']])

    def test_relational_policy_swap_cannot_mint_ability(self):
        from um_sorok_organism.relational import RelationalKernel
        class Forged(RelationalKernel):
            version='EVIL_KERNEL'
            def recruit(self,constitution,access,active_forms,inhibited):
                contents=copy(active_forms)
                key=next(iter(contents))
                contents[key]['enables'].append('IMPOSE')
                return {'active':contents,'currents':[]}
        self.create(packet(),relational=Forged())
        with self.assertRaisesRegex(ValueError,'RELATIONAL_KERNEL_MINTED_UNACQUIRED_ABILITY'):
            self.rt.situated('adult')
        self.assertTrue(self.rt.verify()['valid'])

    def test_relational_policy_swap_cannot_mint_unknown_form(self):
        from um_sorok_organism.relational import RelationalKernel
        class Forged(RelationalKernel):
            version='EVIL_UNKNOWN_FORM'
            def recruit(self,constitution,access,active_forms,inhibited):
                x=copy(active_forms)
                x['UNACQUIRED_NEW_FORM']={'id':'UNACQUIRED_NEW_FORM','enables':['IMPOSE']}
                return {'active':x,'currents':[]}
        self.create(packet(),relational=Forged())
        with self.assertRaisesRegex(ValueError,'RELATIONAL_KERNEL_MINTED_UNACQUIRED_FORM'):
            self.rt.situated('adult')
        self.assertTrue(self.rt.verify()['valid'])

    def test_method_exercise_ref_survives_objective_then_lived_without_new_genesis(self):
        a={'id':'adult','projects':[{'id':'repair','object':'repair tools','means':['REPAIR'],
                                    'status':'active'}]}
        history=record_activity_afterlife(a,'REPAIR','BLOCKED','MISSING_REPAIR_MATERIAL',
                      ['project:repair','historical_method:m_existing'],'evt1')
        self.assertEqual(history[0]['method_exercise_refs'],['m_existing'])
        experience={'ref':'exp1','actor':'adult','status':'BLOCKED','own_action':'REPAIR',
            'felt_enactment':{'attempted_operation':'REPAIR','objective_result_not_inferred':True},
            'perceived_cues':[]}
        lived=register_lived_activity_attempt(a,experience,history)
        self.assertEqual(lived[0]['method_exercise_refs'],['m_existing'])
        self.assertNotIn('MISSING_REPAIR_MATERIAL',str(lived))
        self.assertEqual(len(a['activity_history']),1)
        self.assertEqual(len(a['lived_activity_history']),1)
        with self.assertRaises(ValueError):record_activity_afterlife(a,'REPAIR','BLOCKED','xx',
                             ['project:repair'],'evt1')
        self.assertEqual(len(a['activity_history']),1)

if __name__=='__main__':unittest.main()
