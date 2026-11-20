"""TCO R3's historical-relational center put under executable pressure.

A psychic frame can change an action's PRIVATE functional attribution. It
cannot legalize world violence, mint other actors' consent, become actor's
conscious explanation, or grant an unearned physical operation.
"""
import tempfile,unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.relational import RelationalKernel, transduce
from um_sorok_organism.constitution import materialize,actor_access,compose
from um_sorok_organism.development import admit
from um_sorok_organism.types import copy


def relational_packet(relation='SUBORDINATES',contexts=None):
    return {'source_ref':'R4_HYPOTHETICAL_RELATIONAL_FIELD_NOT_SOCIAL_SCIENCE',
       'answers':{'practice':'fictional'},'fictional_seed':{'acquired_forms':[
         {'kind':'PRACTICE','content':'care through direct work','cues':['home','care'],
          'enables':['CARE'],'scope':{'locations':['home']}},
         {'kind':'MEDIATOR','content':'learned authority framing of care',
          'cues':['home','authority'],'enables':[],'scope':{'locations':['home']}}],
         'links':[{'source_index':1,'target_index':0,'relation':relation,
                   'contexts':contexts or []}],
         'projects':[{'object':'household care','means':['CARE'],
                     'priority':1,'cue_terms':['home','care']} ]}}


class RelationalTransfiguration(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.db=str(Path(self.tmp.name)/'tco_relation.db')
        self.rt=None
    def tearDown(self):
        if self.rt:self.rt.close()
        self.tmp.cleanup()

    def create(self,relation='SUBORDINATES',contexts=None,relational=None):
        self.rt=ConstitutiveRuntime(self.db,relational=relational)
        self.rt.initialize([('adult','Adult',relational_packet(relation,contexts))])
        return self.rt

    def test_form_can_be_refunctioned_without_minting_objective_moral_truth(self):
        self.create()
        situated=self.rt.situated('adult')
        currents=[c for c in situated['currents']
                  if c['kind']=='HISTORICALLY_REFUNCTIONED_MEANING']
        self.assertEqual(len(currents),1)
        frame=currents[0]
        self.assertTrue(frame['not_world_moral_verdict'])
        self.assertTrue(frame['not_actor_conscious_self_account'])
        care=next(o for o in situated['candidate_actions'] if o['action']=='CARE')
        self.assertEqual(care['relational_frames'][0]['relation'],'SUBORDINATES')
        self.assertIn('relation:'+frame['ref'],care['basis'])
        result=self.rt.step('adult',target='nadia')
        self.assertEqual(result['attempt'],'CARE')
        self.assertEqual(result['objective_outcome'],'CARE_GIVEN')
        ev=self.rt.ledger.events()[-1]['envelope']['payload']
        self.assertIn('relation:'+frame['ref'],ev['attempt']['basis'])
        self.assertNotIn('authority',str(result['public_tip']).lower())
        self.assertTrue(self.rt.verify()['valid'])

    def test_suppression_preserves_latent_history_without_granting_its_action(self):
        self.create(relation='INHIBITS')
        s=self.rt.situated('adult')
        self.assertTrue(any(c['kind']=='LATENT_RELATIONAL_CONDITION'
                            for c in s['currents']))
        # Old material remains historically constituted; not deleted from iceberg.
        self.assertEqual(len(self.rt.snapshot('adult')['forms']),3)
        self.assertTrue(s['inhibited'])
        self.assertTrue(self.rt.verify()['valid'])

    def test_conditional_relation_is_not_globally_recruited(self):
        self.create(contexts=['workshop'])
        s=self.rt.situated('adult')
        self.assertFalse(any(c['kind']=='HISTORICALLY_REFUNCTIONED_MEANING'
                             for c in s['currents']))
        self.assertFalse(any(o.get('relational_frames')
                         for o in s['candidate_actions']))

    def test_semantic_event_admission_adds_relation_with_actor_history_only(self):
        self.create()
        a=self.rt.ledger.actor('adult')[1]
        forms=[f for f in a['forms'].values() if f.get('kind') in ('PRACTICE','MEDIATOR')]
        care=next(f for f in forms if 'CARE' in f.get('enables',[]))
        authority=next(f for f in forms if 'authority' in f.get('content',''))
        personal={'actor':'adult','ref':'exp_r4','participated':True,
                  'perceived_cues':[{'id':'cue_actual','tags':['home']}],
                  'felt_enactment':None,'status':'OBSERVED'}
        before=copy(a)
        received=admit(a,personal,'obj_qualified',[{'kind':'LINK_FORMS',
             'source':authority['id'],'target':care['id'],'relation':'INTERPRETS_THROUGH'}])
        self.assertEqual(received[0]['status'],'ADMITTED_SOURCEFREE_FICTIONAL')
        self.assertEqual(len(a['links']),len(before['links'])+1)
        self.assertIn('obj_qualified',a['links'][-1]['origin'])
        self.assertEqual(a['forms'],before['forms'])

    def test_nonexistent_action_cannot_be_granted_by_ideological_frame(self):
        self.create()
        v,w=self.rt.ledger.world();_,a=self.rt.ledger.actor('adult')
        constitution=materialize(a,w);access=actor_access(a,w)
        f={k:v for k,v in constitution.forms.items() if v.get('kind')=='MEDIATOR'}
        result=transduce(constitution,access,f,[],[])
        self.assertFalse(result['candidate_actions'])
        self.assertFalse(result['operative_relations'])

    def test_relational_operation_is_replaceable_without_changing_world_owner(self):
        class R5Hypothesis(RelationalKernel):
            version='TCO_FUTURE_RELATIONAL_POLICY_TEST'
            def transduce(self,constitution,access,active_forms,inhibited,candidates):
                return {'currents':[],'candidate_actions':copy(candidates),
                        'operative_relations':[],'version':self.version}
        self.create(relational=R5Hypothesis())
        result=self.rt.situated('adult')
        self.assertFalse(any(c['kind']=='HISTORICALLY_REFUNCTIONED_MEANING'
                            for c in result['currents']))
        self.assertTrue(self.rt.verify()['valid'])

if __name__=='__main__':unittest.main()
