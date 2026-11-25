"""Human material production, actual independently selected repair, and
historically acquired efficacy in a common material history. No transfer of
actor competence, no shared psyche or inferred pleasure.
"""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
import test_neighbor_material_participation_r13 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,blank_world
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from um_sorok_organism.material_conjunction import admit_authored_structural_history
from um_sorok_organism.practical_powers import active_repair_technique
from neighbor_runtime import NeighborEncounter,EncounterRefusal
import mii

class SharedMaterialPracticeR28(unittest.TestCase):
    def build(self,name,allowed,nominate,grant=True):
        tmp=tempfile.TemporaryDirectory(prefix='neighbor_r28_')
        self.addCleanup(tmp.cleanup)
        db=str(Path(tmp.name)/'life.sqlite')
        phase={'target':None};offers=[]
        def policy(task,p):
            if task=='expression':
                return {'task':task,'surface':'Ordinary work.'}
            if task=='actor_attempt':
                if phase['target'] is None:
                    return {'task':task,'action':'REST'}
                rows=[x for x in p['practical_options'] if x['operation']=='REPAIR'
                      and x.get('project_id') is None
                      and x.get('world_request',{}).get('material_object_ref')==phase['target']]
                self.assertEqual(len(rows),1)
                return {'task':task,'practical_option_id':rows[0]['option_id']}
            if task=='development':
                cs=p.get('historically_possible_repair_techniques',[])
                offers.extend(deepcopy(cs))
                return {'task':task,'candidates':cs if nominate else []}
            raise AssertionError(task)
        svc=ValidatingSemanticService(CallbackLLMProvider(policy))
        rt=ConstitutiveRuntime(db,world_id=name,semantic=svc)
        self.addCleanup(rt.close)
        w=blank_world(name)
        w['sites']['workshop']['stock']=20
        w['sites']['workshop']['material_use_grants']=['worker']+(['visitor'] if grant else [])
        a=adult('worker','Mara','workshop')
        a['projects']=[{'id':'repair_training','object':'practice repair',
            'means':['REPAIR'],'priority':.5,'status':'active'}]
        spec={'grade':'EXPLICIT_SOURCEFREE_STRUCTURAL_HISTORY',
              'source_ref':'fictional:repair_training',
              'positions':[{'id':'training','actor':'worker','field':'training_access',
                'value':'admitted' if allowed else 'excluded','source_ref':'fictional:training',
                'effective_from':0,'effective_until':6}],
              'rules':[{'id':'training_gate','operation':'REPAIR','location':'workshop',
                'source_ref':'fictional:training_gate','effective_from':0,'effective_until':6,
                'all_of':[{'kind':'RECORDED_POSITION','field':'training_access','equals':'admitted'}]}]}
        admit_authored_structural_history(w,{'worker'},spec)
        rt.ledger.initialize(w,[a],source_seals=[
            ('authored_structural_history','FICTIONAL_WORLD_CONDITIONING',spec)])
        source=rt.register_historical_routine_source({
            'kind':'QUALIFIED_ROUTINE_PRACTICE','actor':'worker','location':'workshop',
            'start_clock':0,'end_clock':7,'max_hours_per_active_day':3,
            'description':'bounded modeled component practice'})
        rt.background(7,processes=[{'kind':'QUALIFIED_ROUTINE_PRACTICE',
            'actor':'worker','location':'workshop','source_ref':source['source_ref'],
            'hours_per_active_day':3,'provisional_exposure_fraction':1.,
            'operation':'REPAIR','mode':'SOLO_COMPONENT_PRACTICE'}])
        self.assertEqual(len(rt.snapshot('worker')['practice_exposures']),int(allowed))
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({
            'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{'workshop':{'light':'lit','sightline':'unobstructed',
                'hearing':True,'sound_path':'audible','legibility':'readable'}},
            'actor_conditions':{'worker':{'facing':'entrance','visual':True,
                'light':'lit','sightline':'unobstructed','hearing':True,'sound_path':'audible'}}},
            request_id='geometry')
        self.assertEqual(n.contribute('arrive','MOVE',destination='workshop')['status'],'PERFORMED')
        return rt,n,db,svc,phase,offers

    def make(self,rt,n,name,rid):
        before=deepcopy(rt.ledger.actors())
        w=rt.ledger.world(name)[1];stock=w['sites']['workshop']['stock']
        made=n.contribute(rid,'MAKE_OBJECT')
        self.assertEqual(made['status'],'PERFORMED')
        ref=made['made_object_ref']
        w=rt.ledger.world(name)[1];obj=w['material_objects'][ref]
        self.assertEqual(obj['maker'],'visitor')
        self.assertEqual(obj['owner'],'workshop_steward')
        self.assertEqual(obj['condition'],.56)
        self.assertEqual(w['sites']['workshop']['stock'],stock-2)
        self.assertEqual(rt.ledger.actors(),before)
        self.assertEqual(len(made['potential_actor_evidence']),1)
        self.assertEqual(w['neighbor_user_events'][-1]['made_object_ref'],ref)
        self.assertEqual(rt.ledger.events()[-1]['envelope']['payload']['made_object_ref'],ref)
        count=len(rt.ledger.events())
        replay=n.contribute(rid,'MAKE_OBJECT')
        self.assertEqual(replay['made_object_ref'],ref)
        self.assertEqual(len(rt.ledger.events()),count)
        return ref

    def repair(self,rt,n,name,phase,ref):
        phase['target']=None
        n.independent_actor_beat('worker')
        phase['target']=ref
        res=n.independent_actor_beat('worker')
        self.assertEqual((res['attempt'],res['status']),('REPAIR','PERFORMED'))
        self.assertNotEqual(res['selection_grade'],'INJECTED_NOT_NATIVE_ACTOR_CHOICE')
        return rt.ledger.world(name)[1]['material_objects'][ref]

    def test_actual_shared_objects_become_material_conditions_of_actor_learning(self):
        outcomes={}
        for allowed,nominate in ((True,True),(True,False),(False,True)):
            with self.subTest(allowed=allowed,nominate=nominate):
                name='shared'+str(allowed)+str(nominate)
                rt,n,db,svc,phase,offers=self.build(name,allowed,nominate)
                refs=[]
                for i in range(2):
                    ref=self.make(rt,n,name,'make'+str(i));refs.append(ref)
                    obj=self.repair(rt,n,name,phase,ref)
                    self.assertEqual(obj['condition'],.8)
                    self.assertEqual([x['actor'] for x in obj['objective_labor_history']],['visitor','worker'])
                self.assertEqual(len(offers),int(allowed))
                technique=active_repair_technique(rt.ledger.actor('worker')[1],'workshop')
                self.assertEqual(bool(technique),allowed and nominate)
                if technique:self.assertEqual(technique['basis']['distinct_worked_objects'],refs)
                rt.close()
                cold=ConstitutiveRuntime(db,world_id=name,semantic=svc)
                self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                ref=self.make(cold,nn,name,'third')
                obj=self.repair(cold,nn,name,phase,ref)
                outcomes[(allowed,nominate)]=obj['condition']
                self.assertEqual(obj['owner'],'workshop_steward')
                self.assertEqual(obj['objective_labor_history'][-1]['material_stock_units'],1)
                self.assertEqual(bool(obj['objective_labor_history'][-1].get('acquired_component_technique_ref')),allowed and nominate)
                # The finite close reader exposes condition, not the actor's
                # skill record or a relationship verdict. Same appearance
                # band need not expose the exact material difference.
                nn.contribute('look','LOOK',target_object_ref=ref)
                view=nn.private_surface(nn.new_private_profile(),command='look',target=ref)
                self.assertEqual(view['optional']['text'],'It appears repaired.')
                self.assertNotIn('acquired_component_technique_ref',str(view))
                self.assertNotIn('workshop_steward',str(view))
                self.assertNotIn('visitor',cold.ledger.actors())
                self.assertTrue(cold.verify()['valid'])
        self.assertEqual(outcomes,{(True,True):.9,(True,False):.8,(False,True):.8})

    def test_no_grant_no_object_no_sensory_sign_no_psychic_change(self):
        rt,n,_,_,_,_=self.build('denied',True,True,grant=False)
        before=deepcopy(rt.ledger.world('denied')[1]);actors=deepcopy(rt.ledger.actors())
        made=n.contribute('denied','MAKE_OBJECT')
        self.assertEqual(made['status'],'BLOCKED')
        self.assertNotIn('made_object_ref',made)
        self.assertEqual(made['potential_actor_evidence'],[])
        after=rt.ledger.world('denied')[1]
        self.assertEqual(after['material_objects'],before['material_objects'])
        self.assertEqual(after['sites']['workshop']['stock'],before['sites']['workshop']['stock'])
        self.assertEqual(rt.ledger.actors(),actors)
        count=len(rt.ledger.events())
        with self.assertRaisesRegex(EncounterRefusal,'UNAUTHORED_LOOK_OR_COVER'):
            n.contribute('forged','MAKE_OBJECT',target_object_ref='made-up')
        self.assertEqual(len(rt.ledger.events()),count)
        self.assertTrue(rt.verify()['valid'])

if __name__=='__main__':unittest.main()
