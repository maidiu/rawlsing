"""Recurrent life may become internally contradictory and historically revisable.

Actual independent performed courses, not fabricated daily acts or externally
selected permanent projects. Controlled sourcefree policy compares two
materially different nominations without claiming universal psychology.
"""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
import test_neighbor_material_support_r17 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,newborn,blank_world
from um_sorok_organism.organism import mature
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from um_sorok_organism.development import InvalidDevelopment
from um_sorok_organism.routine_sources import acquired_routine_processes
from neighbor_runtime import NeighborEncounter
import mii

class ContinuingRevision(unittest.TestCase):
    def course(self,db,pause):
        phase={'action':'WAIT','revision':None,'forge':False,'offers':[]}
        def policy(task,p):
            if task=='expression':
                self.assertNotIn('recent_modeled_own_course_analytic_only',str(p.get('actor_accessible',{})))
                return {'task':task,'surface':'Ordinary life continues.'}
            if task=='actor_attempt':
                if p.get('requesting_actor'):return {'task':task,'action':'REFUSE'}
                action=phase['action']
                rows=[x for x in p.get('practical_options',[])
                      if x.get('operation')==action and x.get('project_id')]
                if rows and action not in ('WAIT','REST'):
                    return {'task':task,'practical_option_id':rows[0]['option_id']}
                return {'task':task,'action':action}
            if task=='development':
                rows=p.get('historically_possible_recurrent_routines',[])
                if rows:
                    basis=rows[0]['basis']
                    candidate={'kind':'ACQUIRE_RECURRENT_ROUTINE','basis':basis,
                               'window_days':90,'hours_per_active_day':4.,
                               'provisional_exposure_fraction':1.}
                    if basis['operation']=='FEED':candidate['food_units_per_active_day']=1.
                    return {'task':task,'candidates':[candidate]}
                revision=phase['revision']
                if p['actor']['id']=='mother' and revision is not None:
                    mode,op=revision
                    choices=[x for x in p.get('historically_possible_routine_revisions',[])
                             if x['basis']['operation']==op]
                    if choices:
                        basis=deepcopy(choices[0]['basis']);phase['offers'].append(deepcopy(basis))
                        if phase['forge']:basis['routine_ref']='foreign'
                        v={'kind':'REVISE_RECURRENT_ROUTINE','basis':basis,'mode':mode,
                           'interpretive_hypothesis':'A possible change in the organization of this lived course.'}
                        if mode=='RESIZE':
                            v['dose']={k:(1. if k=='hours_per_active_day' else value)
                                       for k,value in choices[0]['original_ceiling'].items() if k!='state'}
                        return {'task':task,'candidates':[v]}
                return {'task':task,'candidates':[]}
            raise AssertionError(task)
        service=ValidatingSemanticService(CallbackLLMProvider(policy))
        rt=ConstitutiveRuntime(str(db),semantic=service)
        w=blank_world();w['sites']['workshop']['food']=0
        w['holdings']={'mother':{'food':12},'father':{'food':0}}
        mother=adult('mother','Mother','workshop')
        father=adult('father','Father','workshop')
        child=newborn('nadia','Nadia');mature(child,365);child['location']='workshop'
        child['body']['nutrition']=.15;child['body']['comfort']=.15
        def project(pid,means,**extra):
            return {'id':pid,'object':pid,'means':means,'priority':.7,'status':'active',**extra}
        mother['projects']=[project('care',['CARE','FEED'],addressed_party_ref='nadia'),
            project('wage',['WORK']),project('practice',['PRACTICE']),project('vocal',['SING']),
            project('meal',['EAT'])]
        father['projects']=[project('father-care',['CARE'],addressed_party_ref='nadia')]
        rt.ledger.initialize(w,[mother,father,child])
        def world():return rt.ledger.world()[1]
        def actor(aid):return rt.ledger.actor(aid)[1]
        def beat(aid,action,status='PERFORMED'):
            phase['action']=action
            out=rt.step(aid)
            self.assertEqual((out['attempt'],out['status']),(action,status))
            self.assertNotEqual(out['selection_grade'],'INJECTED_NOT_NATIVE_ACTOR_CHOICE')
            return out
        def rest(aid):
            beat(aid,'REST');beat(aid,'REST')
        def interval(days):
            start=world()['clock'];phase['action']='WAIT'
            result=rt.continue_mixed_history(start+days,cadence_origin=start,
                    ordinary_span=days,detail_beats=3)
            self.assertEqual(result['status'],'MODELED_HISTORY_CUT_REACHED')
        def routine(op,aid='mother'):
            return next(x for p in actor(aid)['projects'] for x in p.get('recurrent_routines',[])
                        if x['operation']==op)
        def revise(mode,op):
            phase['revision']=(mode,op)
            beat('mother','REST')
            phase['revision']=None
        try:
            for op in ('CARE','FEED','WORK','PRACTICE','SING'):
                for _ in range(3):
                    rest('mother');beat('mother',op)
            for _ in range(3):
                rest('father');beat('father','CARE')
            rest('mother')
            self.assertEqual(len(acquired_routine_processes(world())),6)
            self.assertEqual(world()['holdings']['mother']['food'],9)
            prior_sources=deepcopy(world()['routine_source_registry'])
            wage=world()['accounts']['mother'];micro=deepcopy(world()['public_history'])
            before_child=deepcopy(actor('nadia'))
            interval(2)
            after=world()
            period=after['historical_periods'][-1]
            self.assertEqual(period['actor_time_claims']['father'],4.)
            self.assertEqual(period['actor_time_claims']['mother'],0.)
            held=period['situationally_withheld_processes']
            self.assertEqual(len(held),5)
            self.assertTrue(all(x['actor']=='mother' and x['reason']==
                    'UNRESOLVED_COMPETING_ROUTINE_TIME_CLAIMS' for x in held))
            self.assertEqual(after['public_history'],micro)
            self.assertEqual(after['accounts']['mother'],wage)
            self.assertEqual(after['holdings']['mother']['food'],9)
            self.assertEqual(actor('nadia')['experienced_care_events'],before_child['experienced_care_events'])
            self.assertTrue(after['reproductive_labor_periods'])
            self.assertTrue(all(x['giver']=='father' for x in after['reproductive_labor_periods']))
            self.assertEqual(routine(pause)['modeled_course_receipts'][-1]['coverage'],
                             'NOT_QUALIFIED_FOR_MODELED_COVERAGE')
            # The failure is objective, not invented experienced causal knowledge.
            self.assertNotIn('UNRESOLVED_COMPETING_ROUTINE_TIME_CLAIMS',str(routine(pause)))
            prior_periods=deepcopy(after['historical_periods'])
            phase['revision']=('PAUSE',pause);phase['forge']=True
            old_w=deepcopy(rt.ledger.world());old_a=deepcopy(rt.ledger.actors())
            phase['action']='REST'
            with self.assertRaisesRegex(InvalidDevelopment,'LIVED_ROUTINE_REVISION_UNQUALIFIED_BASIS'):
                rt.step('mother')
            self.assertEqual(rt.ledger.world(),old_w);self.assertEqual(rt.ledger.actors(),old_a)
            phase['forge']=False
            revise('PAUSE',pause)
            self.assertEqual(routine(pause)['revisions'][-1]['effective_dose']['state'],'PAUSED')
            self.assertTrue(phase['offers'][-1]['recent_modeled_own_course_analytic_only'])
            self.assertEqual(world()['historical_periods'],prior_periods)
            ref=routine(pause)['id']
            self.assertEqual({k:v for k,v in world()['routine_source_registry'][ref].items()
                             if k!='revisions'},prior_sources[ref])
            # Actual absence and cold read use the new distribution, not a
            # caller replay of the old process dose or imagined visitor.
            n=NeighborEncounter(rt,'visitor',mii_module=mii)
            n.install_sourcefree_conditions({'grade':'SOURCEFREE_TEST_ONLY',
                'user_conditions':{'workshop':{'light':'lit','sightline':'unobstructed',
                  'hearing':True,'sound_path':'audible','legibility':'readable'}},
                'actor_conditions':{aid:{'facing':'entrance','visual':True,'light':'lit',
                    'sightline':'unobstructed','hearing':True,'sound_path':'audible'}
                    for aid in ('mother','father','nadia')}},request_id='geometry')
            self.assertEqual(n.contribute('arrive','MOVE',destination='workshop')['status'],'PERFORMED')
            self.assertEqual(n.contribute('depart','LEAVE')['status'],'PERFORMED')
            human=deepcopy(world()['neighbor_user_events']);start=world()['clock']
            dep=human[-1]['event_ref'];rt.close()
            rt=ConstitutiveRuntime(str(db),semantic=service)
            n=NeighborEncounter(rt,'visitor',mii_module=mii)
            result=n.continue_absent_life_until(dep,start+10,historical_cadence={
                    'cadence_origin':start,'ordinary_span':10,'detail_beats':3})
            self.assertEqual(result['status'],'AT_OR_PAST_ABSENCE_TARGET')
            self.assertEqual(world()['neighbor_user_events'],human)
            period=world()['historical_periods'][-1]
            self.assertEqual(period['actor_time_claims']['mother'],16.)
            self.assertEqual(period['actor_time_claims']['father'],4.)
            self.assertTrue(any(x['source_ref']==ref and x['reason']=='ACTOR_ROUTINE_PAUSED'
                                for x in period['situationally_withheld_processes']))
            self.assertEqual(len(world()['material_feeding_events']),3)
            self.assertEqual(world()['holdings']['mother']['food'],0 if pause=='WORK' else 9)
            after_wage=world()['accounts']['mother']
            self.assertEqual(after_wage>wage,pause=='FEED')
            nutrition=actor('nadia')['body']['nutrition']
            self.assertEqual(n.contribute('return','MOVE',destination='workshop')['status'],'PERFORMED')
            phase['action']='EAT';meal=n.independent_actor_beat('mother')
            self.assertEqual((meal['attempt'],meal['status']),('EAT','BLOCKED' if pause=='WORK' else 'PERFORMED'))
            self.assertNotIn('modeled_course_receipts',str(n.private_surface(n.new_private_profile())))
            self.assertEqual(n.contribute('leave-again','LEAVE')['status'],'PERFORMED')
            # A second actual historically situated change redistributes
            # the SAME bounded set; no forced new project or overwritten past.
            revise('RETIRE','PRACTICE')
            revise('RESUME',pause)
            revise('RESIZE','SING')
            self.assertEqual(routine('PRACTICE')['revisions'][-1]['effective_dose']['state'],'RETIRED')
            self.assertEqual(routine(pause)['revisions'][-1]['effective_dose']['state'],'ACTIVE')
            self.assertEqual(routine('SING')['revisions'][-1]['effective_dose']['hours_per_active_day'],1.)
            prior=deepcopy(world()['historical_periods'])
            final_start=world()['clock']
            interval(2)
            self.assertEqual(world()['historical_periods'][:len(prior)],prior)
            last=world()['historical_periods'][-1]
            self.assertEqual(last['actor_time_claims']['mother'],13.)
            sing=next(x for x in last['processes'] if x['source_ref']==routine('SING')['id'])
            self.assertEqual(sing['hours_per_active_day'],1.)
            self.assertEqual(sing['routine_revision_ref'],routine('SING')['revisions'][-1]['id'])
            final_receipts=[x for x in routine('SING')['modeled_course_receipts']
                            if x['from_clock']>=final_start]
            self.assertEqual(sum(x['own_modeled_hours'] for x in final_receipts),2.)
            self.assertEqual(sum(x['through_clock']-x['from_clock'] for x in final_receipts),2.)
            self.assertTrue(rt.verify()['valid'])
            return {'pause':pause,'nutrition':nutrition,'wage':after_wage,'meal':meal['status'],
                    'initial_withheld':5,'new_hours':last['actor_time_claims']['mother'],
                    'actual_child_care_events':len(actor('nadia')['experienced_care_events'])}
        finally:rt.close()

    def test_conflicting_actual_courses_reconstitute_material_life(self):
        with tempfile.TemporaryDirectory() as d:
            a=self.course(Path(d)/'work.sqlite','WORK')
            b=self.course(Path(d)/'feeding.sqlite','FEED')
            self.assertGreater(a['nutrition'],b['nutrition'])
            self.assertGreater(b['wage'],a['wage'])
            self.assertEqual((a['meal'],b['meal']),('BLOCKED','PERFORMED'))
            print('R008_CONTINUING_CONTRADICTION',a,b)

class RelationalRoutineRevision(unittest.TestCase):
    def course(self,db,nominate):
        phase={'action':'CARE','revision':False,'received':[]}
        def policy(task,p):
            if task=='expression':return {'task':task,'surface':'Ordinary life.'}
            if task=='actor_attempt':
                if p.get('requesting_actor'):return {'task':task,'action':'REFUSE'}
                op=phase['action']
                rows=[x for x in p.get('practical_options',[]) if x['operation']==op and x.get('project_id')]
                if rows:return {'task':task,'practical_option_id':rows[0]['option_id']}
                return {'task':task,'action':op}
            if task=='development':
                candidates=[]
                if phase['action']=='CARE':
                    candidates.extend(p.get('historically_possible_care_practices',[]))
                    for offer in p.get('historically_possible_recurrent_routines',[]):
                        candidates.append({'kind':'ACQUIRE_RECURRENT_ROUTINE',
                            'basis':offer['basis'],'window_days':60,
                            'hours_per_active_day':2.,'provisional_exposure_fraction':1.})
                if phase['revision'] and p['actor']['id']=='giver':
                    old=p.get('historically_possible_care_practice_revisions',[])
                    new=[x for x in p.get('historically_possible_routine_revisions',[])
                         if x['basis'].get('received_directed_act')]
                    phase['received'].extend(deepcopy(new))
                    if nominate:
                        candidates.extend({**x,'interpretive_hypothesis':'This contribution may need to stop.'}
                                          for x in old)
                        candidates.extend({'kind':'REVISE_RECURRENT_ROUTINE','basis':x['basis'],
                                           'mode':'PAUSE','interpretive_hypothesis':
                                           'This particular recurrent care may need to stop.'} for x in new)
                return {'task':task,'candidates':candidates}
            raise AssertionError(task)
        svc=ValidatingSemanticService(CallbackLLMProvider(policy))
        rt=ConstitutiveRuntime(str(db),semantic=svc)
        try:
            people=[adult(x,x) for x in ('giver','second','recipient','third')]
            for a in people[:2]:
                a['projects']=[{'id':'care-'+a['id'],'object':'care for recipient','means':['CARE'],
                    'addressed_party_ref':'recipient','priority':.7,'status':'active'}]
            rt.ledger.initialize(blank_world(),people)
            for aid in ('giver','second'):
                for _ in range(3):
                    phase['action']='CARE'
                    self.assertEqual(rt.step(aid)['status'],'PERFORMED')
                    phase['action']='REST';rt.step(aid)
            def world():return rt.ledger.world()[1]
            def actor(aid):return rt.ledger.actor(aid)[1]
            prior=deepcopy(actor('giver'))
            self.assertEqual(len(prior['care_practical_commitments']),1)
            self.assertEqual(len(acquired_routine_processes(world())),2)
            phase['revision']=True;phase['action']='WAIT'
            # Inherited R64 explicit scenario act, not asserted autonomous.
            self.assertEqual(rt.step('third',requested_action='IMPOSE',target='giver')['status'],'PERFORMED')
            self.assertFalse(phase['received'])
            self.assertEqual(rt.step('recipient',requested_action='IMPOSE',target='giver')['status'],'PERFORMED')
            self.assertEqual(len(phase['received']),1)
            phase['revision']=False
            after=actor('giver')
            self.assertEqual(after['care_contribution_episodes'],prior['care_contribution_episodes'])
            self.assertEqual(bool(after['care_practical_commitments'][0].get('revisions')),nominate)
            row=after['projects'][0]['recurrent_routines'][0]
            self.assertEqual(bool(row.get('revisions')),nominate)
            self.assertFalse(actor('second')['projects'][0]['recurrent_routines'][0].get('revisions'))
            # Neither the actual other caregiver nor their time is taken over.
            start=world()['clock'];rt.close()
            rt=ConstitutiveRuntime(str(db),semantic=svc)
            result=rt.continue_mixed_history(start+10,cadence_origin=start,ordinary_span=10)
            self.assertEqual(result['status'],'MODELED_HISTORY_CUT_REACHED')
            labor=world()['reproductive_labor_periods']
            self.assertEqual(sum(x['modeled_labor_hours'] for x in labor if x['giver']=='second'),20.)
            self.assertEqual(sum(x['modeled_labor_hours'] for x in labor if x['giver']=='giver'),
                             0. if nominate else 20.)
            # Prior care is retained, and generic available care is not outlawed.
            self.assertTrue(any(x.get('action')=='CARE' for x in rt.situated('giver')['candidate_actions']))
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()

    def test_personally_received_adverse_act_can_reconstitute_recurring_care_without_substitution(self):
        with tempfile.TemporaryDirectory() as d:
            self.course(Path(d)/'retained.sqlite',False)
            self.course(Path(d)/'paused.sqlite',True)

if __name__=='__main__':unittest.main()
