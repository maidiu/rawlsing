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
    def course(self,db,both,operations=('SING','SING')):
        own_op,other_op=operations
        phase={'op':'REST','revision':None,'refuse':False}
        offers=[]
        def policy(task,p):
            if task=='expression':return {'task':task,'surface':'Ordinary life.'}
            if task=='actor_attempt':
                op=other_op if p.get('requesting_actor') else phase['op'];aid=p['actor']['id']
                if p.get('requesting_actor') and phase['refuse']:
                    return {'task':task,'action':'REFUSE'}
                if op=='LATER':
                    value=next((x['situated_component_facility']['technical_component_facility_estimate']
                                for x in p['options'] if x['action']==own_op),None)
                    op=own_op if value is not None and value>phase['threshold'] else 'WAIT'
                rows=[x for x in p.get('practical_options',[]) if x.get('operation')==op
                      and x.get('project_id')==('a-song' if aid=='a' else 'b-song')]
                if rows and op in operations:
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
                             if x['basis']['operation']==other_op]
                    if choices:return {'task':task,'candidates':[{
                        'kind':'REVISE_RECURRENT_ROUTINE','basis':choices[0]['basis'],
                        'mode':phase['revision'],'interpretive_hypothesis':'Change my own involvement.'}]}
                return {'task':task,'candidates':[]}
            raise AssertionError(task)
        service=ValidatingSemanticService(CallbackLLMProvider(policy))
        rt=ConstitutiveRuntime(str(db),semantic=service)
        aa=adult('a','A');bb=adult('b','B')
        aa['projects']=[{'id':'a-song','object':'a particular shared practice','means':[own_op],
                         'addressed_party_ref':'b','status':'active','priority':.7}]
        bb['projects']=[{'id':'b-song','object':'b particular shared practice','means':[other_op],
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
            phase['refuse']=True;beat('a',own_op,'PARTIAL');phase['refuse']=False
            for _ in range(3):
                beat('a','REST');beat('b','REST');beat('a',own_op)
            self.assertEqual({a for a,_ in offers},{'a','b'})
            sources=world()['routine_source_registry']
            self.assertEqual(len(sources),2 if both else 1)
            self.assertTrue(all(len(x['basis_event_refs'])==3 for x in sources.values()))
            if both:
                a,b=sorted(sources.values(),key=lambda x:x['actor'])
                self.assertEqual(a['basis_event_refs'],b['basis_event_refs'])
            before={a:deepcopy(actor(a)) for a in ('a','b')}
            f0={a:situated_component_efficacy(before[a],own_op if a=='a' else other_op,'home')[
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
            f1={a:situated_component_efficacy(actor(a),own_op if a=='a' else other_op,'home')[
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
                # An actual conflicting independently authored time premise
                # holds B's contingent shared course and thus A's half as well.
                start=world()['clock']
                source=rt.register_historical_routine_source({
                    'kind':'QUALIFIED_OTHER_OBLIGATION','actor':'b','location':'home',
                    'start_clock':start,'end_clock':start+3,'max_hours_per_active_day':16.,
                    'description':'Explicit bounded competing time premise'})
                rt.continue_mixed_history(start+3,cadence_origin=start,ordinary_span=3,
                    period_processes=[{'kind':'QUALIFIED_OTHER_OBLIGATION','actor':'b','location':'home',
                       'source_ref':source['source_ref'],'hours_per_active_day':16.,
                       'provisional_exposure_fraction':1.}])
                competing=[x for x in world()['historical_periods'] if x['start']>=start]
                self.assertTrue(all(len(x['processes'])==1 and x['processes'][0]['actor']=='b'
                                    for x in competing))
                self.assertTrue(any(y['reason']=='RECIPROCAL_COUNTERPART_TIME_UNRESOLVED'
                         for x in competing for y in x['situationally_withheld_processes']))
                # Actual separation prevents both sides from spending time.
                self.assertEqual(rt.step('b',requested_action='MOVE',object_ref='workshop')['status'],'PERFORMED')
                self.assertTrue(all(not x['processes'] for x in interval(3)))
                self.assertEqual(rt.step('b',requested_action='MOVE',object_ref='home')['status'],'PERFORMED')
                self.assertTrue(all(len(x['processes'])==2 for x in interval(3)))
            else:self.assertEqual(f1,f0)
            n=NeighborEncounter(rt,'visitor',mii_module=mii)
            self.assertEqual(n.contribute('return','MOVE',destination='home')['status'],'PERFORMED')
            # Same controlled recruitment policy and threshold, but the
            # earlier independently co-produced aggregate history changes
            # the operative component estimate. Later assent remains fresh.
            phase['threshold']=f0['a']+.005
            phase['op']='LATER';phase['refuse']=True
            later=rt.step('a')
            self.assertEqual((later['attempt'],later['status']),
                             (own_op,'PARTIAL') if both else ('WAIT','PERFORMED'))
            self.assertNotEqual(later['selection_grade'],'INJECTED_NOT_NATIVE_ACTOR_CHOICE')
            surface=n.private_surface(n.new_private_profile())
            self.assertNotIn('matched_counterpart_source_ref',str(surface))
            self.assertNotIn('recurrent_routines',str(surface))
            self.assertNotIn('visitor',rt.ledger.actors())
            self.assertTrue(rt.verify()['valid'])
            print('RECIPROCAL_ROUTINE',operations,both,f0,f1,later['attempt'],later['status'])
        finally:rt.close()

    def material_course(self,db,op,both):
        from um_sorok_organism.types import newborn
        from um_sorok_organism.organism import mature
        phase={'op':'REST','refuse':False,'retire':False,'learn':False}
        def policy(task,p):
            if task=='expression':return {'task':task,'surface':'Ordinary care.'}
            aid=p['actor']['id']
            if task=='actor_attempt':
                action=op if p.get('requesting_actor') else phase['op']
                if p.get('requesting_actor') and phase['refuse']:return {'task':task,'action':'REFUSE'}
                if action=='LATER':
                    acquired=[x for x in p.get('practical_options',[]) if x.get('grounds_status')=='HISTORICALLY_ACQUIRED_CO_REGULATION' and x.get('world_request',{}).get('addressed_party_ref')=='mother']
                    return {'task':task,'practical_option_id':acquired[0]['option_id']} if acquired else {'task':task,'action':'WAIT'}
                rows=[x for x in p.get('practical_options',[]) if x['operation']==action
                      and x.get('project_id') in ('mother-care','child-call','other-care')]
                if rows and action not in ('WAIT','REST'):
                    # Exact own project, with material source chosen by the
                    # existing feeder's qualified practical option if offered.
                    if action=='FEED':
                        source=[x for x in rows if x.get('selected_feeding_source')=='GIVER_HELD_FOOD']
                        if source:rows=source
                    return {'task':task,'practical_option_id':rows[0]['option_id']}
                return {'task':task,'action':action}
            if task=='development':
                if aid=='child' and phase['learn']:
                    for x in p.get('historically_possible_co_regulation',[]):
                        if x['caregiver_ref']=='mother':
                            return {'task':task,'candidates':[{'kind':'ACQUIRE_CO_REGULATION_ORIENTATION','caregiver_ref':'mother','period_refs':x['source_care_period_refs'],'perceived_cue_ref':x['current_perceived_cue_ref']}]}
                for offer in p.get('historically_possible_recurrent_routines',[]):
                    basis=offer['basis']
                    if aid=='child' and not both:continue
                    out={'kind':'ACQUIRE_RECURRENT_ROUTINE','basis':basis,'window_days':60,
                         'hours_per_active_day':2.,'provisional_exposure_fraction':1.}
                    if basis['operation']=='FEED':out['food_units_per_active_day']=1.
                    return {'task':task,'candidates':[out]}
                if aid=='child' and phase['retire']:
                    options=[x for x in p.get('historically_possible_routine_revisions',[])
                             if x['basis']['operation']=='SIGNAL']
                    if options:return {'task':task,'candidates':[{'kind':'REVISE_RECURRENT_ROUTINE',
                        'basis':options[0]['basis'],'mode':'RETIRE',
                        'interpretive_hypothesis':'No longer undertake this particular recurring call.'}]}
                return {'task':task,'candidates':[]}
            raise AssertionError(task)
        service=ValidatingSemanticService(CallbackLLMProvider(policy))
        rt=ConstitutiveRuntime(str(db),semantic=service)
        child=newborn('child','Child');mature(child,365)
        child['body']['nutrition']=.25;child['body']['comfort']=.15
        mother=adult('mother','Mother');other=adult('other','Other')
        child['projects']=[{'id':'child-call','object':'seek contingent support','means':['SIGNAL'],
                            'addressed_party_ref':'mother','priority':.7,'status':'active'}]
        mother['projects']=[{'id':'mother-care','object':'contribute care','means':['CARE','FEED'],
                            'addressed_party_ref':'child','priority':.7,'status':'active'}]
        other['projects']=[{'id':'other-care','object':'own caring course','means':['CARE'],
                            'addressed_party_ref':'child','priority':.7,'status':'active'}]
        w=blank_world();w['holdings']={'mother':{'food':8}}
        rt.ledger.initialize(w,[mother,other,child])
        def world():return rt.ledger.world()[1]
        def actor(aid):return rt.ledger.actor(aid)[1]
        def beat(aid,action):
            phase['op']=action;out=rt.step(aid)
            self.assertEqual((out['attempt'],out['status']),(action,'PERFORMED'))
            self.assertNotEqual(out['selection_grade'],'INJECTED_NOT_NATIVE_ACTOR_CHOICE')
        def interval(days):
            start=world()['clock'];phase['op']='WAIT'
            result=rt.continue_mixed_history(start+days,cadence_origin=start,ordinary_span=days)
            self.assertEqual(result['status'],'MODELED_HISTORY_CUT_REACHED')
            return [p for p in world()['historical_periods'] if p['start']>=start]
        try:
            for _ in range(3):
                beat('mother','REST');beat('child','REST');beat('child','SIGNAL')
                beat('other','REST');beat('other','CARE')
            beat('mother','REST');beat('child','REST');beat('other','REST')
            sources=world()['routine_source_registry']
            self.assertEqual(len(sources),3 if both else 2)
            self.assertTrue(any(x['actor']=='other' and not x['process'].get('coactivity_partner')
                                for x in sources.values()))
            prior=deepcopy(actor('child'))
            food=world()['holdings']['mother']['food']
            before_feeds=len(world().get('material_feeding_events',[]))
            periods=interval(8)
            for p in periods:
                self.assertEqual({x['actor'] for x in p['processes']},
                                {'mother','child','other'} if both else {'other'})
                self.assertEqual(p['actor_time_claims']['other'],2.)
                if both:
                    self.assertEqual(p['actor_time_claims']['mother'],2.)
                    self.assertEqual(p['actor_time_claims']['child'],2.)
            after=deepcopy(actor('child'))
            mother_rest_after=actor('mother')['body']['rest']
            self.assertEqual(after['experienced_care_events'],prior['experienced_care_events'])
            self.assertEqual(after['memories'],prior['memories'])
            self.assertEqual(len(world().get('material_feeding_events',[])),before_feeds)
            if op=='FEED':
                self.assertEqual(world()['holdings']['mother']['food'],0 if both else food)
                self.assertEqual(bool(world().get('material_provisioning_periods')),both)
                if both:self.assertTrue(any(x['uncovered_food_units']>0
                              for x in world()['material_provisioning_periods']))
            elif both:
                self.assertTrue(any(x.get('giver')=='mother' for x in world()['reproductive_labor_periods']))
            self.assertEqual(bool(after['practice_exposures']),both)
            if op=='FEED':
                exposure=[x for x in after.get('undergone_care_periods',[]) if x.get('historical_exposure_kind')=='MODELED_BODILY_PROVISIONING']
                self.assertEqual(bool(exposure),both)
                self.assertTrue(all(x['caregiver_ref']=='mother' and x['aggregate_modeled_nutrition_gain']>0 for x in exposure))
                self.assertFalse(after.get('co_regulation_orientations'))
                rt.close();rt=ConstitutiveRuntime(str(db),semantic=service)
                phase['learn']=True;beat('child','REST');phase['learn']=False
                formed=[x for x in actor('child').get('co_regulation_orientations',[]) if x['caregiver_ref']=='mother']
                self.assertEqual(bool(formed),both)
                if both:self.assertTrue(set(formed[0]['source_care_period_refs']) & {x['id'] for x in exposure})
                phase['op']='LATER';phase['refuse']=True
                attempt=rt.step('child');phase['refuse']=False
                self.assertEqual((attempt['attempt'],attempt['status']),('SIGNAL','PARTIAL') if both else ('WAIT','PERFORMED'))
            if both:
                # Retirement belongs to the child. Mother's project and
                # independent other-care remain, but no joint claim survives.
                phase['retire']=True;beat('child','REST');phase['retire']=False
                mother_before=deepcopy(actor('mother')['projects'])
                old=deepcopy(world()['historical_periods'])
                rt.close();rt=ConstitutiveRuntime(str(db),semantic=service)
                later=interval(4)
                self.assertTrue(all({x['actor'] for x in p['processes']}=={'other'} for p in later))
                self.assertEqual(actor('mother')['projects'][0]['recurrent_routines'][0].get('revisions',[]),
                                 mother_before[0]['recurrent_routines'][0].get('revisions',[]))
                self.assertEqual(world()['historical_periods'][:len(old)],old)
            self.assertTrue(rt.verify()['valid'])
            return after['body']['nutrition'],after['body']['comfort'],mother_rest_after
        finally:rt.close()

    def test_complementary_independent_care_and_nourishment(self):
        with tempfile.TemporaryDirectory() as d:
            for op in ('CARE','FEED'):
                yes=self.material_course(Path(d)/(op+'-yes.sqlite'),op,True)
                no=self.material_course(Path(d)/(op+'-no.sqlite'),op,False)
                if op=='CARE':
                    # Saturation is material reality, not a reason to erase
                    # actual caregiver expenditure or invent extra relief.
                    self.assertGreaterEqual(yes[1],no[1])
                    self.assertLess(yes[2],no[2])
                else:self.assertGreater(yes[0],no[0])
                print('RECIPROCAL_MATERIAL',op,yes,no)

    def test_separate_admissions_match_without_future_consent(self):
        with tempfile.TemporaryDirectory() as d:
            self.course(Path(d)/'both.sqlite',True)
            self.course(Path(d)/'one.sqlite',False)

    def test_complementary_practice_and_support(self):
        with tempfile.TemporaryDirectory() as d:
            self.course(Path(d)/'complementary.sqlite',True,('PRACTICE','JOIN'))

if __name__=='__main__':unittest.main()
