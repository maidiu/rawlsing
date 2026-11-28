"""R41 independently selected consumption competes with another's livelihood.
Actual multi-center household history, not a welfare optimization or scripted
collective mind. Child is an explicit older-child fixture, not infant science.
"""
import unittest
from copy import deepcopy
from pathlib import Path
import tempfile
import test_neighbor_material_support_r17 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,newborn,blank_world,canonical
from um_sorok_organism.organism import mature
from um_sorok_organism.material_provisioning import settle_selected_self_meal
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from um_sorok_organism.world import register_recursive_encounter_paths
from neighbor_runtime import NeighborEncounter
import mii

class SharedReproductionR41(unittest.TestCase):
    def course(self,source,*,carer_chooses=True,carer_sees=True,visitor_help=False,forge=False):
        tmp=tempfile.TemporaryDirectory(prefix='shared_reproduction_r41_')
        self.addCleanup(tmp.cleanup)
        db=str(Path(tmp.name)/'life.sqlite')
        state={'phase':'prior','packets':[]}
        def cb(task,p):
            state['packets'].append((task,deepcopy(p)))
            if task=='expression':return {'task':task,'surface':'Ordinary activity.'}
            if task=='development':return {'task':task,'candidates':[]}
            aid=p['actor']['id'];phase=state['phase'];opts=p['practical_options']
            if aid=='adult' and phase=='meal_choice':
                choices=[x for x in opts if x['operation']=='EAT' and x['project_id']=='meal'
                         and x.get('selected_self_meal_source')==source]
                self.assertEqual(len(choices),1)
                return {'task':task,'practical_option_id':'forged' if forge else choices[0]['option_id']}
            if aid=='child' and phase=='offer':
                choices=[x for x in opts if x['operation']=='SIGNAL' and x.get('human_food_offer_ref')]
                self.assertEqual(len(choices),1)
                return {'task':task,'practical_option_id':choices[0]['option_id']}
            if aid=='carer' and phase=='respond':
                # The carer is not given another actor's private nutrition,
                # the adult's selected pool, or the investigator's course arm.
                incomplete=any(q.get('kind')=='performed_eat' and q.get('source_actor')=='child'
                               and q.get('description')=='ATTEMPT_NOT_COMPLETED'
                               for q in p['accessible']['cues'])
                if incomplete and carer_chooses:
                    choices=[x for x in opts if x['operation']=='FEED'
                             and x['project_id']=='care'
                             and x['world_request']['addressed_party_ref']=='child']
                    self.assertEqual(len(choices),1)
                    return {'task':task,'practical_option_id':choices[0]['option_id']}
                return {'task':task,'action':'WAIT'}
            return {'task':task,'action':'EAT','project_id':'meal'}
        sem=ValidatingSemanticService(CallbackLLMProvider(cb))
        rt=ConstitutiveRuntime(db,semantic=sem);self.addCleanup(rt.close)
        w=blank_world();w['sites']['home']['food']=0;w['sites']['home']['mutual_aid_food']=1
        w['holdings']={'adult':{'food':1},'child':{'food':1},'carer':{'food':1},
                       'visitor':{'food':1}}
        people=[adult('adult','Adult'),newborn('child','Child'),adult('carer','Carer')]
        for person in people:
            person['projects']=[{'id':'meal','object':'own meal','means':['EAT'],
                                  'priority':.6,'status':'active'}]
        mature(people[1],5*365);people[1]['body']['nutrition']=.25
        people[2]['projects'].append({'id':'care','object':'provide food to child','means':['FEED'],
                        'addressed_party_ref':'child','priority':.7,'status':'active'})
        register_recursive_encounter_paths(w,{a['id']:a for a in people},{
            'grade':'SOURCEFREE_TEST_ONLY','source_ref':'fictional:household_visual',
            'paths':[{'observer':'carer','source_actor':'child','location':'home',
                'from_clock':0,'through_clock':100,'hearing':True,'sound_path':'audible',
                'visual':carer_sees,'light':'lit','sightline':'unobstructed',
                'facing':'source' if carer_sees else 'away'}]})
        rt.ledger.initialize(w,people)
        # Actual ordinary activity precedes any visitor. This child already
        # exercises eating, rather than being created at encounter arrival.
        self.assertEqual(rt.step('child')['status'],'PERFORMED')
        old=deepcopy(rt.ledger.actor('child')[1]['projects'][0]['operational_history'])
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{'home':{'light':'lit','sightline':'unobstructed',
                'hearing':True,'sound_path':'audible','legibility':'readable'}},
            'actor_conditions':{a['id']:{'facing':'entrance','visual':True,'light':'lit',
                'sightline':'unobstructed','hearing':True,'sound_path':'audible'} for a in people}},
            request_id='geometry')
        n.contribute('arrive','MOVE',destination='home')
        state['phase']='meal_choice';before=deepcopy(rt.ledger.world());actors=deepcopy(rt.ledger.actors())
        if forge:
            with self.assertRaisesRegex(ValueError,'UNKNOWN_OR_AMBIGUOUS_PRACTICAL_OPTION_ID'):
                n.independent_actor_beat('adult')
            self.assertEqual(rt.ledger.world(),before);self.assertEqual(rt.ledger.actors(),actors)
            self.assertTrue(rt.verify()['valid']);return
        out=n.independent_actor_beat('adult');self.assertEqual(out['status'],'PERFORMED')
        receipt=rt.ledger.latest_event()['envelope']['payload']['actual']['selected_self_meal_receipt']
        self.assertEqual(receipt['food_source'],source)
        self.assertEqual(receipt['pool_before']-receipt['pool_after'],1)
        w=rt.ledger.world()[1]
        self.assertNotIn('selected_self_meal_receipt',w['public_history'][-1])
        self.assertEqual(w['cues'][-1]['description'],'ATE_FOOD')
        self.assertEqual(w['holdings']['adult']['food'],int(source=='MUTUAL_AID_FOOD'))
        state['phase']='child';child=n.independent_actor_beat('child')
        child_fed=source=='GIVER_HELD_FOOD'
        self.assertEqual(child['status'],'PERFORMED' if child_fed else 'BLOCKED')
        if visitor_help and not child_fed:
            # A real, separately authored offer. Never pre-author a human act
            # from an earlier meal or the child's objective bodily need.
            n.contribute('offer','OFFER_FEED',target_actor_ref='child')
            state['phase']='offer'
            self.assertEqual(n.independent_actor_beat('child')['status'],'PERFORMED')
        state['phase']='respond';carer=n.independent_actor_beat('carer')
        substituted=not child_fed and not visitor_help and carer_sees and carer_chooses
        self.assertEqual(carer['attempt'],'FEED' if substituted else 'WAIT')
        w=rt.ledger.world()[1]
        self.assertEqual(len(w['material_feeding_events']),int(substituted or (visitor_help and not child_fed)))
        self.assertEqual(w['holdings']['carer']['food'],int(not substituted))
        self.assertEqual(rt.ledger.actor('child')[1]['projects'][0]['operational_history'][:len(old)],old)
        self.assertNotIn('visitor',rt.ledger.actors())
        labor=deepcopy(w['social_reproductive_labor']);child_body=deepcopy(rt.ledger.actor('child')[1]['body'])
        rt.close();cold=ConstitutiveRuntime(db,semantic=sem);self.addCleanup(cold.close)
        nn=NeighborEncounter(cold,'visitor',mii_module=mii)
        state['phase']='late'
        meal=nn.independent_actor_beat('carer')
        self.assertEqual(meal['status'],'BLOCKED' if substituted else 'PERFORMED')
        self.assertEqual(cold.ledger.world()[1]['social_reproductive_labor'],labor)
        self.assertTrue(cold.verify()['valid'])
        return {'child_eat':child['status'],'carer':carer['attempt'],'meal':meal['status'],
                'child_nutrition':child_body['nutrition'],'labor':len(labor)}

    def test_common_pool_competes_with_child_and_third_party_later_meal(self):
        own=self.course('GIVER_HELD_FOOD')
        common=self.course('MUTUAL_AID_FOOD')
        self.assertEqual((own['child_eat'],own['carer'],own['meal']),('PERFORMED','WAIT','PERFORMED'))
        self.assertEqual((common['child_eat'],common['carer'],common['meal']),('BLOCKED','FEED','BLOCKED'))

    def test_no_automatic_substitution_and_actual_human_offer(self):
        decline=self.course('MUTUAL_AID_FOOD',carer_chooses=False)
        unseen=self.course('MUTUAL_AID_FOOD',carer_sees=False)
        human=self.course('MUTUAL_AID_FOOD',visitor_help=True)
        for arm in (decline,unseen,human):
            self.assertEqual((arm['carer'],arm['meal']),('WAIT','PERFORMED'))
        self.assertEqual(decline['labor'],0);self.assertEqual(unseen['labor'],0)
        self.assertEqual(human['labor'],1)
        self.assertGreater(human['child_nutrition'],decline['child_nutrition'])

    def test_forged_and_unavailable_selection_never_falls_through(self):
        self.course('MUTUAL_AID_FOOD',forge=True)
        w=blank_world();w['positions']={'a':'home'};w['holdings']={'a':{'food':1}}
        before=deepcopy(w)
        for source in ('MUTUAL_AID_FOOD',['GIVER_HELD_FOOD']):
            status,_,receipt=settle_selected_self_meal(w,'a','home',source,
                'ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE')
            self.assertEqual(status,'BLOCKED');self.assertIsNone(receipt);self.assertEqual(w,before)

if __name__=='__main__':unittest.main()
