"""R39 actual independently selected lexical action, not a narrated utterance."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
import test_neighbor_material_support_r17 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,newborn,blank_world,canonical
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from um_sorok_organism.world import register_recursive_encounter_paths
from neighbor_runtime import NeighborEncounter
import mii

WORDS='I finished the work.'  # A speech claim, not proof of actual work.
PRIVATE='Unspoken worry about tomorrow.'
AIM='Tell the nearby person that the work is finished.'

class LexicalOccurrenceR39(unittest.TestCase):
    def build(self,mode='speak',hear=True,see=True):
        tmp=tempfile.TemporaryDirectory(prefix='lexical_r39_')
        self.addCleanup(tmp.cleanup)
        db=str(Path(tmp.name)/'life.sqlite')
        state={'mode':mode,'calls':[],'experience':{}}
        def cb(task,p):
            state['calls'].append((task,deepcopy(p)))
            if task=='actor_attempt':
                if p['actor']['id']!='speaker':return {'task':task,'action':'WAIT'}
                if state['mode']=='wait':return {'task':task,'action':'WAIT'}
                if state['mode']=='forged':return {'task':task,'action':'WAIT','speech_intent':AIM}
                return {'task':task,'action':'SPEAK','project_id':'talk','speech_intent':AIM}
            if task=='expression':
                if p.get('expression_phase')=='LEXICAL_REALIZATION_BEFORE_EXPERIENCE':
                    self.assertNotIn(PRIVATE,canonical(p))
                    self.assertNotIn('selected_constitution',p)
                    return {'task':task,'speech':{'bad':'shape'} if state['mode']=='malformed' else WORDS,
                            'surface':'UNTRUSTED_EXTRA_DESCRIPTION'}
                return {'task':task,'speech':'NOT_AN_OCCURRENCE','surface':'Generic description.'}
            if task=='development':
                state['experience'][p['actor']['id']]=deepcopy(p['experience'])
                return {'task':task,'candidates':[]}
            raise AssertionError(task)
        sem=ValidatingSemanticService(CallbackLLMProvider(cb))
        rt=ConstitutiveRuntime(db,semantic=sem)
        self.addCleanup(rt.close)
        w=blank_world()
        speaker=adult('speaker','Speaker')
        speaker['projects']=[{'id':'talk','object':'speak','means':['SPEAK'],'priority':.6,'status':'active'}]
        speaker['self_model']={'private':PRIVATE}
        people=[speaker,adult('hearer','Hearer'),adult('deaf','Deaf'),newborn('child','Child'),adult('unknown','Unknown')]
        for person in people:w['positions'][person['id']]='home'
        def path(observer,hearing,visual):
            return {'observer':observer,'source_actor':'speaker','location':'home','from_clock':0,
                'through_clock':30,'hearing':hearing,'sound_path':'audible' if hearing else 'blocked',
                'visual':visual,'light':'lit','sightline':'unobstructed','facing':'source' if visual else 'away'}
        register_recursive_encounter_paths(w,{p['id']:p for p in people},{
            'grade':'SOURCEFREE_TEST_ONLY','source_ref':'fictional:acoustics',
            'paths':[path('hearer',True,False),path('deaf',False,True),path('child',True,True)]})
        if mode=='blocked':
            w['institutional_access_rules'].append({'id':'silenced','source_ref':'fixture:rule',
                'operation':'SPEAK','location':'home',
                'all_of':[{'kind':'CURRENT_SITE','equals':'workshop'}]})
        rt.ledger.initialize(w,people)
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{'home':{'light':'lit' if see else 'dark',
                'sightline':'unobstructed' if see else 'blocked',
                'hearing':hear,'sound_path':'audible' if hear else 'blocked','legibility':'readable'}},
            'actor_conditions':{p['id']:{'facing':'entrance','visual':True,
                'light':'lit','sightline':'unobstructed','hearing':True,'sound_path':'audible'} for p in people}},
            request_id='geometry')
        n.contribute('arrive','MOVE',destination='home')
        return rt,n,db,state,sem

    def test_actual_words_actor_specific_receipts_and_cold_finite_surface(self):
        rt,n,db,state,sem=self.build(see=False)
        out=n.independent_actor_beat('speaker')
        self.assertEqual(out['status'],'PERFORMED')
        self.assertIsNone(out['public_tip'])
        self.assertEqual(sum(t=='expression' for t,p in state['calls']),1)
        self.assertLess([t for t,p in state['calls']].index('expression'),
                        [t for t,p in state['calls']].index('development'))
        world=rt.ledger.world()[1]
        self.assertEqual(world['material_claims'],[])
        self.assertEqual(world['cues'][-1]['spoken_text'],WORDS)
        for aid in ('speaker','hearer'):
            self.assertIn(WORDS,canonical(state['experience'][aid]['perceived_cues']))
        hearer=next(q for q in state['experience']['hearer']['perceived_cues'] if q.get('spoken_text'))
        self.assertIsNone(hearer['source_actor'])
        for aid in ('deaf','child','unknown'):
            self.assertNotIn(WORDS,canonical(state['experience'].get(aid,{})))
        before=deepcopy(rt.ledger.world());actors=deepcopy(rt.ledger.actors())
        profile=n.new_private_profile()
        view=n.private_surface(profile)
        signs=[x for x in view['mandatory'] if x.get('spoken_text')]
        self.assertEqual(len(signs),1);self.assertEqual(signs[0]['spoken_text'],WORDS)
        self.assertEqual(signs[0]['speaker_identity'],'NOT_ESTABLISHED')
        self.assertEqual(signs[0]['source_event_ref'],out['receipt'])
        self.assertNotIn(PRIVATE,canonical(view))
        self.assertNotIn(AIM,canonical(view))
        self.assertNotIn('UNTRUSTED_EXTRA_DESCRIPTION',canonical(view))
        self.assertEqual(rt.ledger.world(),before);self.assertEqual(rt.ledger.actors(),actors)
        rt.close()
        cold=ConstitutiveRuntime(db,semantic=sem);self.addCleanup(cold.close)
        nn=NeighborEncounter(cold,'visitor',mii_module=mii)
        self.assertIn(WORDS,canonical(nn.private_surface(profile)))
        state['mode']='wait'
        nn.independent_actor_beat('speaker')
        self.assertNotIn(WORDS,canonical(nn.private_surface(profile)))
        self.assertTrue(cold.verify()['valid'])

    def test_silence_blocked_and_unheard_distinct(self):
        for mode,hear in [('wait',True),('blocked',True),('speak',False)]:
            with self.subTest(mode=mode):
                rt,n,db,state,sem=self.build(mode,hear=hear)
                out=n.independent_actor_beat('speaker')
                view=n.private_surface(n.new_private_profile())
                self.assertNotIn(WORDS,canonical(view))
                self.assertNotIn('NOT_AN_OCCURRENCE',canonical(view))
                self.assertNotIn('UNTRUSTED_EXTRA_DESCRIPTION',canonical(view))
                self.assertEqual('spoken_text' in rt.ledger.world()[1]['cues'][-1],mode=='speak')
                self.assertEqual(out['status'],'BLOCKED' if mode=='blocked' else 'PERFORMED')
                self.assertEqual(sum(t=='expression' for t,p in state['calls']),1)

    def test_malformed_or_wrong_operation_rolls_back(self):
        for mode in ('malformed','forged'):
            rt,n,db,state,sem=self.build(mode)
            before=deepcopy(rt.ledger.world());actors=deepcopy(rt.ledger.actors())
            events=deepcopy(rt.ledger.events())
            with self.assertRaisesRegex(ValueError,'LEXICAL_REALIZATION_INVALID_SPEECH|SPEECH_INTENT_NOT_QUALIFIED'):
                n.independent_actor_beat('speaker')
            self.assertEqual(rt.ledger.world(),before)
            self.assertEqual(rt.ledger.actors(),actors)
            self.assertEqual(rt.ledger.events(),events)
            self.assertTrue(rt.verify()['valid'])

if __name__=='__main__':unittest.main()
