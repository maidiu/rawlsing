"""Positive development: persistent facility, distinct episodic accessibility."""
from copy import deepcopy
import unittest
import test_neighbor_shared_material_practice_r28 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from um_sorok_organism.practical_powers import active_repair_technique
from neighbor_runtime import NeighborEncounter
import mii

class ConstitutiveCompressionR31(unittest.TestCase):
    def build(self,name):
        # Reuse the R28 actual structural training and material exercise court.
        return inherited.SharedMaterialPracticeR28.build(self,name,True,True)
    make=inherited.SharedMaterialPracticeR28.make
    repair=inherited.SharedMaterialPracticeR28.repair

    def test_acquired_facility_persists_when_original_episode_is_inaccessible(self):
        for decrease in (True,False):
            with self.subTest(decrease=decrease):
                name='compression'+str(decrease)
                rt,n,db,svc,phase,offers=self.build(name)
                marker='That afternoon I learned the precise way to mend the blue bowl.'
                stage='acquire';seen=[];rehearsals=[]
                def policy(task,p):
                    result=svc.proposal(task,p)
                    if task=='development':
                        candidates=result['candidates']
                        if p.get('historically_possible_repair_techniques'):
                            candidates.append({'kind':'MEMORY','content':marker,
                                               'cue_terms':['repair']})
                        ds=p.get('historically_possible_memory_access_decreases',[])
                        if ds:
                            seen.extend(deepcopy(ds))
                            self.assertNotIn(marker,str(ds))
                            if decrease and stage=='exercise':candidates.extend(ds)
                    if task=='actor_attempt' and stage=='cold':
                        rows=p.get('private_rehearsal_options',[])
                        rehearsals.append(any(marker in str(x) for x in rows))
                        if decrease:self.assertNotIn(marker,str(p))
                    if task=='expression':self.assertNotIn(marker,str(p))
                    return result
                joined=ValidatingSemanticService(CallbackLLMProvider(policy))
                rt.semantic=joined
                for i in range(2):
                    ref=self.make(rt,n,name,'make'+str(i))
                    self.assertEqual(self.repair(rt,n,name,phase,ref)['condition'],.8)
                actor=rt.ledger.actor('worker')[1]
                technique=deepcopy(active_repair_technique(actor,'workshop'))
                original=deepcopy(actor['memories'][0])
                self.assertEqual(original['status'],'ACTOR_ACCESSIBLE')
                self.assertEqual(original['origin'],[technique['basis']['event_refs'][-1]])
                stage='exercise'
                ref=self.make(rt,n,name,'third')
                self.assertEqual(self.repair(rt,n,name,phase,ref)['condition'],.9)
                self.assertEqual(len(seen),1)
                after=rt.ledger.actor('worker')[1]['memories'][0]
                for k in ('id','origin','experience','content'):
                    self.assertEqual(after[k],original[k])
                self.assertEqual(after['status'],'ACTOR_INACCESSIBLE' if decrease else 'ACTOR_ACCESSIBLE')
                if decrease:
                    self.assertEqual(after['retention_state'],'RETAINED')
                    self.assertEqual(after['accessibility_transitions'][0]['basis'],seen[0]['basis'])
                rt.close()
                cold=ConstitutiveRuntime(db,world_id=name,semantic=joined)
                self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                stage='cold'
                self.assertEqual(active_repair_technique(cold.ledger.actor('worker')[1],'workshop'),technique)
                ref=self.make(cold,nn,name,'fourth')
                self.assertEqual(self.repair(cold,nn,name,phase,ref)['condition'],.9)
                self.assertEqual(any(rehearsals),not decrease)
                self.assertEqual(cold.ledger.actor('worker')[1]['memories'][0],after)
                nn.contribute('look','LOOK',target_object_ref=ref)
                view=nn.private_surface(nn.new_private_profile(),command='look',target=ref)
                self.assertEqual(view['optional']['text'],'It appears repaired.')
                self.assertNotIn(marker,str(view))
                self.assertTrue(cold.verify()['valid'])

    def test_unissued_access_decrease_rolls_back(self):
        rt,n,db,svc,phase,_=self.build('forgery')
        def policy(task,p):
            out=svc.proposal(task,p)
            if task=='development':
                return {'task':task,'candidates':[{'kind':'ACCESS_DECREASE',
                                                  'basis':{'memory_ref':'forged'}}]}
            return out
        rt.semantic=ValidatingSemanticService(CallbackLLMProvider(policy))
        before=deepcopy(rt.ledger.actors());world=deepcopy(rt.ledger.world('forgery'))
        count=len(rt.ledger.events())
        with self.assertRaisesRegex(ValueError,'MEMORY_ACCESS_DECREASE_UNQUALIFIED_HISTORY'):
            n.independent_actor_beat('worker')
        self.assertEqual(rt.ledger.actors(),before)
        self.assertEqual(rt.ledger.world('forgery'),world)
        self.assertEqual(len(rt.ledger.events()),count)
        self.assertTrue(rt.verify()['valid'])

if __name__=='__main__':unittest.main()
