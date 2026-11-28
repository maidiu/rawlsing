"""Actual separate nominations of coactivity, not pooled minds or future assent."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
import test_neighbor_material_support_r17 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,blank_world
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from um_sorok_organism.routine_sources import acquired_routine_processes
from um_sorok_organism.mediated_efficacy import situated_component_efficacy
from neighbor_runtime import NeighborEncounter
import mii

class ReciprocalOrdinaryLife(unittest.TestCase):
    def course(self,db,both):
        phase={'op':'REST','revision':None,'refuse':False}
        offers=[]
        def policy(task,p):
            if task=='expression':return {'task':task,'surface':'Ordinary life.'}
            if task=='actor_attempt':
                op=phase['op'];aid=p['actor']['id']
                if p.get('requesting_actor') and phase['refuse']:
                    return {'task':task,'action':'REFUSE'}
                rows=[x for x in p.get('practical_options',[]) if x.get('operation')==op
                      and x.get('project_id')==('a-song' if aid=='a' else 'b-song')]
                if rows and op=='SING':
                    return {'task':task,'practical_option_id':rows[0]['option_id']}
                return {'task':task,'action':op}
            if task=='development':
                aid=p['actor']['id']
                for x in p.get('historically_possible_recurrent_routines',[]):
                    if x['basis'].get('coactivity_partner'):
                        offers.append((aid,deepcopy(x)))
                        if aid=='a' or both:
                            return {'task':task,'candidates':[{'kind':'ACQUIRE_RECURRENT_ROUTINE',
                                'basis':x['basis'],'window_days':80,
                                'hours_per_active_day':3. if aid=='a' else 2.,
                                'provisional_exposure_fraction':1. if aid=='a' else .5}]}
                if phase['revision'] and aid=='b':
                    choices=[x for x in p.get('historically_possible_routine_revisions',[])
                             if x['basis']['operation']=='SING']
                    if choices:return {'task':task,'candidates':[{
                        'kind':'REVISE_RECURRENT_ROUTINE','basis':choices[0]['basis'],
                        'mode':phase['revision'],'interpretive_hypothesis':'Change my own involvement.'}]}
                return {'task':task,'candidates':[]}
            raise AssertionError(task)
        service=ValidatingSemanticService(CallbackLLMProvider(policy))
        rt=ConstitutiveRuntime(str(db),semantic=service)
        aa=adult('a','A');bb=adult('b','B')
        aa['projects']=[{'id':'a-song','object':'sing together','means':['SING'],
                         'addressed_party_ref':'b','status':'active','priority':.7}]
        bb['projects']=[{'id':'b-song','object':'sing together','means':['SING'],
                         'addressed_party_ref':'a','status':'active','priority':.7}]
        rt.ledger.initialize(blank_world(),[aa,bb])
        def world():return rt.ledger.world()[1]
        def actor(aid):return rt.ledger.actor(aid)[1]
        def beat(aid,op,status='PERFORMED'):
            phase['op']=op;out=rt.step(aid)
            self.assertEqual((out['attempt'],out['status']),(op,status))
            self.assertNotEqual(out['selection_grade'],'INJECTED_NOT_NATIVE_ACTOR_CHOICE')
            return out
        def interval(days):
            start=world()['clock']
            out=rt.continue_mixed_history(start+days,cadence_origin=start,ordinary_span=days)
            self.assertEqual(out['status'],'MODELED_HISTORY_CUT_REACHED')
            return [x for x in world()['historical_periods'] if x['start']>=start]
        def cold():
            nonlocal rt
            rt.close();rt=ConstitutiveRuntime(str(db),semantic=service)
            self.assertTrue(rt.verify()['valid'])
        try:
            # A refusal cannot become an exercise warrant.
            phase['refuse']=True;beat('a','SING','PARTIAL');phase['refuse']=False
            for _ in range(3):
                beat('a','REST');beat('b','REST');beat('a','SING')
            self.assertEqual({a for a,_ in offers},{'a','b'})
            sources=world()['routine_source_registry']
            self.assertEqual(len(sources),2 if both else 1)
            self.assertTrue(all(len(x['basis_event_refs'])==3 for x in sources.values()))
            if both:
                a,b=sorted(sources.values(),key=lambda x:x['actor'])
                self.assertEqual(a['basis_event_refs'],b['basis_event_refs'])
            before={a:deepcopy(actor(a)) for a in ('a','b')}
            f0={a:situated_component_efficacy(before[a],'SING','home')[
                'technical_component_facility_estimate'] for a in before}
            n=NeighborEncounter(rt,'visitor',mii_module=mii)
            n.install_sourcefree_conditions({'grade':'SOURCEFREE_TEST_ONLY',
                'user_conditions':{'home':{'light':'lit','sightline':'unobstructed',
                    'hearing':True,'sound_path':'audible','legibility':'readable'}},
                'actor_conditions':{a:{'facing':'entrance','visual':True,'light':'lit',
                    'sightline':'unobstructed','hearing':True,'sound_path':'audible'}
                    for a in ('a','b')}},request_id='geometry')
            n.contribute('enter','MOVE',destination='home');n.contribute('leave','LEAVE')
            visit=deepcopy(world()['neighbor_user_events']);dep=visit[-1]['event_ref']
            cold();n=NeighborEncounter(rt,'visitor',mii_module=mii)
            start=world()['clock']
            result=n.continue_absent_life_until(dep,start+20,
                    historical_cadence={'cadence_origin':start,'ordinary_span':20,'detail_beats':3})
            self.assertEqual(result['status'],'AT_OR_PAST_ABSENCE_TARGET')
            self.assertEqual(world()['neighbor_user_events'],visit)
            periods=[x for x in world()['historical_periods'] if x['start']>=start]
            for x in periods:
                self.assertEqual(len(x['processes']),2 if both else 0)
                if both:
                    self.assertEqual(len({y['reciprocal_routine_pair_ref'] for y in x['processes']}),1)
                    self.assertEqual(x['actor_time_claims'],{'a':1.,'b':1.})
                else:
                    self.assertTrue(any(y['reason']=='NO_UNAMBIGUOUS_INDEPENDENT_RECIPROCAL_ROUTINE'
                        for y in x['situationally_withheld_processes']))
            for a in ('a','b'):
                q=actor(a)
                self.assertEqual(q['power_exercises'],before[a]['power_exercises'])
                self.assertEqual(q['memories'],before[a]['memories'])
                self.assertEqual(bool(q['practice_exposures']),both)
            f1={a:situated_component_efficacy(actor(a),'SING','home')[
                'technical_component_facility_estimate'] for a in before}
            if both:
                self.assertTrue(all(f1[a]>f0[a] for a in f0))
                original=deepcopy(world()['historical_periods'])
                phase['revision']='PAUSE';beat('b','REST');phase['revision']=None
                count={a:len(actor(a)['practice_exposures']) for a in before}
                held=interval(5)
                self.assertTrue(all(not x['processes'] for x in held))
                self.assertEqual(world()['historical_periods'][:len(original)],original)
                self.assertEqual({a:len(actor(a)['practice_exposures']) for a in before},count)
                # Only B may resume B's contribution.
                phase['revision']='RESUME';beat('b','REST');phase['revision']=None
                resumed=interval(5)
                self.assertTrue(all(len(x['processes'])==2 for x in resumed))
                self.assertTrue(all(x['actor_time_claims']=={'a':1.,'b':1.} for x in resumed))
                self.assertTrue(all(len(actor(a)['practice_exposures'])>count[a] for a in before))
                # Actual separation prevents both sides from spending time.
                self.assertEqual(rt.step('b',requested_action='MOVE',object_ref='workshop')['status'],'PERFORMED')
                self.assertTrue(all(not x['processes'] for x in interval(3)))
                self.assertEqual(rt.step('b',requested_action='MOVE',object_ref='home')['status'],'PERFORMED')
                self.assertTrue(all(len(x['processes'])==2 for x in interval(3)))
            else:self.assertEqual(f1,f0)
            n=NeighborEncounter(rt,'visitor',mii_module=mii)
            self.assertEqual(n.contribute('return','MOVE',destination='home')['status'],'PERFORMED')
            phase['refuse']=True;beat('a','SING','PARTIAL')
            self.assertNotIn('visitor',rt.ledger.actors())
            self.assertTrue(rt.verify()['valid'])
            print('RECIPROCAL_ROUTINE',both,f0,f1)
        finally:rt.close()

    def test_separate_admissions_match_without_future_consent(self):
        with tempfile.TemporaryDirectory() as d:
            self.course(Path(d)/'both.sqlite',True)
            self.course(Path(d)/'one.sqlite',False)

if __name__=='__main__':unittest.main()
