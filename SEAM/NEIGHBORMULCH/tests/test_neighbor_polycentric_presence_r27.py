"""Several independently constituted lives continue within one actual
visitor occasion. A learned relation between activities may change one
actor's actual course, not the others' projects or the visitor's conduct.
"""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
import test_neighbor_live_interrupt_r2 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,blank_world
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from neighbor_runtime import NeighborEncounter,EncounterRefusal
import mii

class PolycentricPresenceR27(unittest.TestCase):
    def build(self,name,learn):
        tmp=tempfile.TemporaryDirectory(prefix='neighbor_r27_')
        self.addCleanup(tmp.cleanup)
        db=str(Path(tmp.name)/'life.sqlite')
        stage={'phase':'joint'}
        offered=[]
        def policy(task,p):
            aid=p.get('actor',{}).get('id')
            if task=='actor_attempt':
                if aid=='other':
                    return {'task':task,'action':'MAKE_OBJECT'}
                if aid=='remote':
                    return {'task':task,'action':'SPEAK'}
                phase=stage['phase']
                if phase=='joint':
                    return {'task':task,'action':'REST','project_ids':['restore','duty']}
                if phase in ('defer','later'):
                    rows=p['practical_options']
                    left=next(x for x in rows if x.get('project_id')=='restore' and x['operation']=='REST')
                    right=next(x for x in rows if x.get('project_id')=='duty' and x['operation']=='SPEAK')
                    if phase=='defer':
                        return {'task':task,'practical_option_id':left['option_id'],
                                'defer_course_option_id':right['option_id']}
                    currents=right.get('interactivity_currents',[])
                    self.assertEqual(left.get('interactivity_currents',[]),currents)
                    self.assertEqual(len(currents),int(learn))
                    if currents:
                        return {'task':task,'practical_option_id':right['option_id'],
                                'interactivity_relation_ref':currents[0]['relation_ref']}
                    return {'task':task,'practical_option_id':left['option_id']}
                return {'task':task,'action':'WAIT'}
            if task=='development':
                if aid!='worker':return {'task':task,'candidates':[]}
                if stage['phase']=='appraise':
                    projects={e['id']:e['project_id'] for e in p['actor_expectations_analyst_only']}
                    rows={}
                    for x in p['historically_possible_delayed_appraisals']:
                        rows.setdefault(x['expectation_ref'],x)
                    self.assertEqual({projects[x] for x in rows},{'restore','duty'})
                    return {'task':task,'candidates':[
                        {'kind':'APPRAISE_EXPECTED_DIFFERENCE','expectation_ref':x['expectation_ref'],
                         'perceived_cue_ref':x['source_perceived_cue_ref'],
                         'appraisal':('ACTOR_INTERPRETS_SUPPORTED' if projects[x['expectation_ref']]=='restore'
                                      else 'ACTOR_INTERPRETS_DISAPPOINTED')}
                        for x in rows.values()]}
                if stage['phase']=='defer':
                    rows=p['historically_possible_interactivity_relations']
                    self.assertEqual(len(rows),1)
                    offered.extend(deepcopy(rows))
                    return {'task':task,'candidates':[{'kind':'ACQUIRE_INTERACTIVITY_RELATION',
                        'basis':rows[0],'personal_sense':'Rest sustains me yet defers duty.'}] if learn else []}
                return {'task':task,'candidates':[]}
            if task=='expression':
                own=p['actor_accessible'].get('own_practical_selection') or {}
                self.assertNotIn('interactivity_deferral',own)
                self.assertNotIn('interactivity_relation_analytic_only',own)
                return {'task':task,'surface':'An ordinary interval.'}
            raise AssertionError(task)
        svc=ValidatingSemanticService(CallbackLLMProvider(policy))
        rt=ConstitutiveRuntime(db,world_id=name,semantic=svc)
        self.addCleanup(rt.close)
        a=adult('worker','Mara','home')
        a['projects']=[{'id':pid,'object':obj,'means':means,'priority':.5,'status':'active',
            'expected_difference':{'feature':obj,'direction':'PRESERVE','sign_tags':['wait']}}
            for pid,obj,means in [('restore','recover strength',['REST']),
                                  ('duty','sustain availability',['REST','SPEAK'])]]
        other=adult('other','Other','home')
        remote=adult('remote','Remote','workshop')
        w=blank_world(name);w['sites']['home']['stock']=20
        rt.ledger.initialize(w,[a,other,remote])
        rt.step('worker')
        stage['phase']='appraise';rt.step('worker')
        stage['phase']='defer';rt.step('worker')
        self.assertEqual(len(offered),1)
        self.assertEqual(len(rt.ledger.actor('worker')[1]['projects'][0].get('interactivity_relations',[])),int(learn))
        stage['phase']='later'
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({
            'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{'home':{'light':'lit','sightline':'unobstructed',
                'hearing':True,'sound_path':'audible','legibility':'readable'}},
            'actor_conditions':{aid:{'facing':'entrance','visual':True,'light':'lit',
                'sightline':'unobstructed','hearing':True,'sound_path':'audible'}
                for aid in ('worker','other','remote')}},request_id='geometry')
        return rt,n,db,svc

    def test_multiple_independent_centers_same_human_occasion_cold_resume(self):
        for learn in (True,False):
            with self.subTest(learn=learn):
                name='scene'+str(learn)
                rt,n,db,svc=self.build(name,learn)
                arrival=n.contribute('enter','MOVE',destination='home')
                self.assertEqual(arrival['status'],'PERFORMED')
                ref=arrival['event_ref']
                start=rt.ledger.world(name)[1]['clock']
                prior=deepcopy(rt.ledger.world(name)[1]['neighbor_user_events'])
                profile=n.new_private_profile()
                first=n.continue_present_life_until(ref,start+3,max_beats=1,profile=profile)
                self.assertEqual(first['status'],'HELD_AT_BOUNDED_PRESENT_CONTINUATION')
                self.assertEqual(first['beats_committed_this_call'],1)
                path=Path(db).with_suffix('.mii.json')
                n.save_private_profile(path,profile)
                rt.close()
                cold=ConstitutiveRuntime(db,world_id=name,semantic=svc)
                self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                profile=nn.load_private_profile(path)
                rest=nn.continue_present_life_until(ref,start+3,profile=profile)
                self.assertEqual(rest['status'],'AT_OR_PAST_PRESENT_TARGET')
                self.assertEqual(rest['beats_committed_this_call'],2)
                self.assertEqual(rest['actual_modeled_clock'],start+3)
                frames=first['new_present_surfaces']+rest['new_present_surfaces']
                events=cold.ledger.events()[-3:]
                self.assertEqual({e['actor_id'] for e in events},{'worker','other','remote'})
                self.assertTrue(all(e['kind']=='ACTOR_LIFE_TRANSITION' for e in events))
                actual={e['actor_id']:e['envelope']['payload']['actual'] for e in events}
                self.assertEqual(actual['worker']['action'],'SPEAK' if learn else 'REST')
                self.assertEqual(actual['other']['action'],'MAKE_OBJECT')
                self.assertEqual(actual['other']['status'],'PERFORMED')
                self.assertEqual(actual['remote']['action'],'SPEAK')
                w=cold.ledger.world(name)[1]
                self.assertEqual(w['neighbor_user_events'],prior)
                self.assertNotIn('visitor',cold.ledger.actors())
                self.assertTrue(any(o['maker']=='other' for o in w['material_objects'].values()))
                for frame,e in zip(frames,events):
                    v=frame['visitor_surface']
                    self.assertEqual(frame['modeled_clock'],e['clock'])
                    self.assertNotIn('Rest sustains me yet defers duty',str(v))
                    self.assertNotIn('interactivity_relation',str(v))
                    self.assertNotIn('remote',str(v))
                    sounds=[s for s in v['mandatory'] if s['kind']=='CO_PUBLIC_OCCURRENCE'
                            and s.get('modality')=='auditory']
                    self.assertEqual(len(sounds),int(e['actor_id']=='worker' and learn))
                    if sounds:self.assertEqual(sounds[0]['source_event_ref'],e['id'])
                nn.save_private_profile(path,profile)
                self.assertEqual(nn.load_private_profile(path),profile)
                count=len(cold.ledger.events());exposures=deepcopy(profile)
                replay=nn.continue_present_life_until(ref,start+3,profile=profile)
                self.assertEqual(replay['new_present_surfaces'],[])
                self.assertEqual(len(cold.ledger.events()),count)
                self.assertEqual(profile,exposures)
                self.assertTrue(cold.verify()['valid'])

    def test_interruption_scope_and_horizon_do_not_author_extra_life(self):
        rt,n,_,_=self.build('guards',True)
        a=n.contribute('enter','MOVE',destination='home')
        ref=a['event_ref'];start=rt.ledger.world('guards')[1]['clock']
        before=len(rt.ledger.events())
        wrong=NeighborEncounter(rt,'stranger',mii_module=mii).new_private_profile()
        with self.assertRaisesRegex(EncounterRefusal,'MII_PROFILE_SCOPE_MISMATCH'):
            n.continue_present_life_until(ref,start+1,profile=wrong)
        with self.assertRaisesRegex(EncounterRefusal,'PRESENT_OCCASION_HORIZON_OUT_OF_BOUNDS'):
            n.continue_present_life_until(ref,start+25)
        self.assertEqual(len(rt.ledger.events()),before)
        n.contribute('new','WAIT')
        count=len(rt.ledger.events())
        with self.assertRaisesRegex(EncounterRefusal,'PRESENT_OCCASION_INTERRUPTED'):
            n.continue_present_life_until(ref,start+3)
        self.assertEqual(len(rt.ledger.events()),count)
        n.contribute('leave','LEAVE')
        count=len(rt.ledger.events())
        with self.assertRaisesRegex(EncounterRefusal,'VISITOR_NOT_PRESENT'):
            n.continue_present_life_until(ref,start+3)
        self.assertEqual(len(rt.ledger.events()),count)
        self.assertTrue(rt.verify()['valid'])

if __name__=='__main__':unittest.main()
