import unittest
from copy import deepcopy
from initiative import situated_actor_opportunities, choose_next_actor, continue_life


def actor(a, *, nutrition=.8, rest=.8, comfort=.8, projects=None):
    return {'id':a,'body':{'nutrition':nutrition,'rest':rest,'comfort':comfort,
            'motor':.8,'sensor':.6,'language':.7},'projects':projects or []}

class InitiativeTests(unittest.TestCase):
    def setUp(self):
        self.world={'clock':1,'sites':{'home':{},'workshop':{}},
                    'positions':{'nadia':'home','father':'workshop','mother':'home'}}
        self.actors={'nadia':actor('nadia',nutrition=.2), 'mother':actor('mother'),
                     'father':actor('father')}

    def test_need_prioritizes_opportunity_not_action(self):
        x=choose_next_actor(self.world,self.actors)
        self.assertEqual(x['actor'],'nadia')
        self.assertNotIn('action',x)
        self.assertEqual(x['unmet_body_conditions'],['nutrition'])

    def test_not_a_teleological_project_priority(self):
        self.actors['mother']['projects']=[{'id':'good_thing','status':'active'}]*99
        self.assertEqual(choose_next_actor(self.world,self.actors)['actor'],'nadia')

    def test_independent_participants_not_forged(self):
        d=next(o for o in situated_actor_opportunities(self.world,self.actors)
               if o['actor']=='nadia')
        self.assertEqual(d['co_present_actor_refs'],['mother'])
        self.assertNotIn('coactor_consent',d)
        self.assertNotIn('requesting_actor',d)

    def test_interval_fairly_rotates_after_urgent_actor(self):
        self.assertEqual(choose_next_actor(self.world,self.actors,{'nadia':1})['actor'],'father')
        self.assertEqual(choose_next_actor(self.world,self.actors,{'nadia':1,'father':1})['actor'],'mother')

    def test_real_world_read_each_beat(self):
        received=[]
        def world(): return deepcopy(self.world)
        def actors(): return deepcopy(self.actors)
        def step(a):
            received.append(a)
            self.world['clock']+=1
            self.actors[a]['body']['nutrition']=min(1,self.actors[a]['body']['nutrition']+.1)
            return {'actor':a,'clock':self.world['clock'],'receipt':f'event{len(received)}',
                    'selection_grade':'ACTOR_POLICY'}
        r=continue_life(world,actors,step,3)
        self.assertEqual(r['beats_committed'],3)
        self.assertEqual(received,['nadia','father','mother'])
        self.assertEqual([e['new_clock'] for e in r['events']],[2,3,4])
        self.assertTrue(r['no_player_action_injected'])

    def test_no_ghost_actors(self):
        self.world['positions'].pop('nadia')
        self.assertFalse(any(x['actor']=='nadia' for x in situated_actor_opportunities(self.world,self.actors)))

    def test_bad_budget_refused(self):
        for b in (0,25,-1,True,1.5):
            with self.subTest(b=b),self.assertRaises(ValueError):
                continue_life(lambda:self.world,lambda:self.actors,lambda a:None,b)

    def test_unqualified_world_result_cannot_be_recorded_as_life(self):
        with self.assertRaises(ValueError):
            continue_life(lambda:self.world,lambda:self.actors,
                          lambda a:{'actor':a,'clock':2},1)

    def test_no_actors_no_events(self):
        self.world['positions']={}
        out=continue_life(lambda:self.world,lambda:self.actors,
                          lambda _:self.fail('should not fabricate act'),3)
        self.assertEqual(out['events'],[])

    def test_malformed_bodies_not_opportunities(self):
        self.actors['nadia']['body']['rest']=float('nan')
        with self.assertRaisesRegex(ValueError,'INITIATIVE_INVALID_BODY_REST'):
            situated_actor_opportunities(self.world,self.actors)

    def test_actor_identity_cannot_be_swapped(self):
        self.actors['nadia']['id']='someone_else'
        with self.assertRaisesRegex(ValueError,'INITIATIVE_ACTOR_IDENTITY_MISMATCH'):
            choose_next_actor(self.world,self.actors)

if __name__=='__main__':unittest.main()