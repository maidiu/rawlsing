"""R42 particular voluntary address is not privacy, trust, or consent."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
import test_neighbor_material_support_r17 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,blank_world,canonical
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from um_sorok_organism.world import register_recursive_encounter_paths
from neighbor_runtime import NeighborEncounter
import mii

WORDS='I was worried about tomorrow.'
PRIVATE='Not offered to anyone: another worry.'

class VoluntaryAddressR42(unittest.TestCase):
    def course(self,target,*,visible=True,mode='speak'):
        tmp=tempfile.TemporaryDirectory(prefix='address_r42_');self.addCleanup(tmp.cleanup)
        db=str(Path(tmp.name)/'life.sqlite')
        state={'phase':'prior','offers':{},'calls':[]}
        def cb(task,p):
            state['calls'].append(task)
            if task=='expression':
                return {'task':task,'speech':WORDS,'surface':'Generic prose.'}
            aid=p['actor']['id']
            if task=='development':
                offers=p.get('historically_possible_lexical_project_revaluations',[])
                if state['phase']=='utter':state['offers'][aid]=deepcopy(offers)
                # Distinct route can ground optional revaluation of actual
                # prior work. No forced effect of hearing the words.
                if (state['phase']=='utter' and aid=='listener' and offers
                        and offers[0]['lexical_revaluation_basis'].get('lexical_acquisition_route')
                            =='VOLUNTARILY_ADDRESSED_TO_SELF'):
                    q=offers[0]
                    return {'task':task,'candidates':[{'kind':'REORGANIZE_PROJECT',
                        'project_id':q['project_id'],'lexical_revaluation_basis':q['lexical_revaluation_basis'],
                        'priority':.1,'personal_significance':'Perhaps I can take a moment to listen.'}]}
                return {'task':task,'candidates':[]}
            if state['phase']=='prior':return {'task':task,'action':'WORK','project_id':'work'}
            if state['phase']=='later':
                courses=[(v['priority'],o['action'],v['project_id'])
                         for o in p['options'] for v in o.get('project_courses',[])]
                _,op,project=max(courses);return {'task':task,'action':op,'project_id':project}
            if mode=='silent':return {'task':task,'action':'WAIT'}
            if target is None:return {'task':task,'action':'SPEAK','project_id':'talk','speech_intent':'Share a worry.'}
            choices=[q for q in p['practical_options'] if q.get('binding_status')==
                'EXACT_CURRENT_VOLUNTARY_SPEECH_ADDRESS' and q['project_id']=='talk'
                and q['world_request']['addressed_party_ref']==target]
            self.assertEqual(len(choices),1)
            chosen={'task':task,'practical_option_id':'forged' if mode=='forge' else choices[0]['option_id']}
            if mode!='no_words':chosen['speech_intent']='Share a worry.'
            return chosen
        sem=ValidatingSemanticService(CallbackLLMProvider(cb))
        rt=ConstitutiveRuntime(db,semantic=sem);self.addCleanup(rt.close)
        w=blank_world()
        speaker=adult('speaker','Speaker','workshop')
        speaker['projects']=[{'id':'talk','object':'speak','means':['SPEAK'],'priority':.6,'status':'active'}]
        speaker['self_model']={'private':PRIVATE}
        listener=adult('listener','Listener','workshop')
        listener['projects']=[{'id':'work','object':'earn wage','means':['WORK'],'priority':.65,'status':'active'},
                             {'id':'rest','object':'rest','means':['REST'],'priority':.4,'status':'active'}]
        people=[speaker,listener]
        register_recursive_encounter_paths(w,{p['id']:p for p in people},{
            'grade':'SOURCEFREE_TEST_ONLY','source_ref':'fictional:address',
            'paths':[{'observer':'listener','source_actor':'speaker','location':'workshop',
                'from_clock':0,'through_clock':30,'hearing':True,'sound_path':'audible',
                'visual':True,'light':'lit','sightline':'unobstructed','facing':'source'}]})
        rt.ledger.initialize(w,people)
        self.assertEqual(rt.step('listener')['status'],'PERFORMED')
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{'workshop':{'light':'lit' if visible else 'dark',
                'sightline':'unobstructed' if visible else 'blocked','hearing':True,
                'sound_path':'audible','legibility':'readable'}},
            'actor_conditions':{p['id']:{'facing':'entrance','visual':True,'light':'lit',
                'sightline':'unobstructed','hearing':True,'sound_path':'audible'} for p in people}},
            request_id='geometry')
        n.contribute('arrive','MOVE',destination='workshop')
        before=deepcopy(rt.ledger.world());actors=deepcopy(rt.ledger.actors())
        state['phase']='utter';count=len(state['calls'])
        if mode in ('forge','no_words'):
            with self.assertRaisesRegex(ValueError,'UNKNOWN_OR_AMBIGUOUS_PRACTICAL_OPTION_ID|VOLUNTARY_ADDRESS_REQUIRES_EXACT_LEXICAL_CHOICE'):
                n.independent_actor_beat('speaker')
            self.assertEqual(rt.ledger.world(),before);self.assertEqual(rt.ledger.actors(),actors)
            self.assertTrue(rt.verify()['valid']);return
        out=n.independent_actor_beat('speaker')
        self.assertEqual(out['status'],'PERFORMED')
        self.assertEqual(state['calls'][count:].count('expression'),1)
        view=n.private_surface(n.new_private_profile())
        self.assertNotIn(PRIVATE,canonical(view))
        if mode=='silent':
            self.assertNotIn(WORDS,canonical(view))
            self.assertFalse(state['offers'].get('listener'))
            return
        signs=[q for q in view['mandatory'] if q.get('spoken_text')]
        self.assertEqual(len(signs),1);self.assertEqual(signs[0]['spoken_text'],WORDS)
        expected=('VOLUNTARILY_ADDRESSED_TO_SELF' if target=='visitor' else 'AUDIBLE_NOT_ADDRESSED_TO_SELF') if visible and target else None
        self.assertEqual(signs[0].get('lexical_acquisition_route'),expected)
        receipt=rt.ledger.latest_event()['envelope']['payload']
        self.assertIsNone(receipt['coactor_attempt'])
        listener_basis=state['offers']['listener'][0]['lexical_revaluation_basis']
        self.assertEqual(listener_basis.get('lexical_acquisition_route'),
            'VOLUNTARILY_ADDRESSED_TO_SELF' if target=='listener' else 'AUDIBLE_NOT_ADDRESSED_TO_SELF' if target else None)
        self.assertEqual(rt.ledger.world()[1]['material_claims'],before[1]['material_claims'])
        rt.close();cold=ConstitutiveRuntime(db,semantic=sem);self.addCleanup(cold.close)
        nn=NeighborEncounter(cold,'visitor',mii_module=mii)
        self.assertEqual([q for q in nn.private_surface(nn.new_private_profile())['mandatory'] if q.get('spoken_text')],signs)
        state['phase']='later';cash=cold.ledger.world()[1]['accounts']['listener']
        later=nn.independent_actor_beat('listener')
        self.assertTrue(cold.verify()['valid'])
        self.assertNotIn(WORDS,canonical(nn.private_surface(nn.new_private_profile())))
        return later['attempt'],cold.ledger.world()[1]['accounts']['listener']-cash

    def test_identical_words_different_address_and_cold_afterlife(self):
        self.assertEqual(self.course('listener'),('REST',0))
        self.assertEqual(self.course('visitor'),('WORK',.25))
        self.assertEqual(self.course(None),('WORK',.25))
        self.assertEqual(self.course('visitor',visible=False),('WORK',.25))

    def test_silence_and_invalid_address_are_not_disclosure(self):
        self.course('visitor',mode='silent')
        self.course('visitor',mode='forge')
        self.course('visitor',mode='no_words')

if __name__=='__main__':unittest.main()
