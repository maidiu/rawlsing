"""Actual adjacent-turn vocal coordination -> optional acquired practice ->
later conditional invitation, never imported human consent or human psyche.
"""
from copy import deepcopy
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[3]
for p in (ROOT/'SEAM'/'ORACLE'/'UM_SOROK_ORGANISM_R3',
          ROOT/'WORKER_RETURNS'/'SOROK-P5-CONTINUOUS-EXPERIENCE-R1',
          ROOT/'WORKER_RETURNS'/'SOROK-P6-ONE-LIVING-HOUSE-R1',
          ROOT/'WORKER_RETURNS'/'SOROK-P4-CORE-LOOP-R1',
          ROOT,ROOT/'SEAM'/'NEIGHBORMULCH'):
    sys.path.insert(0,str(p))
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,blank_world
from um_sorok_organism.semantics import (
    CallbackLLMProvider,ValidatingSemanticService,HeuristicSemanticProvider)
from neighbor_runtime import NeighborEncounter
import mii

def policy(stage, acquire=False):
    fallback=HeuristicSemanticProvider()
    def callback(task,packet):
        if task=='actor_attempt':
            grounds=({'EXPLORATORY_VISITOR_VOCAL_INVITATION',
                      'ACTOR_PREVIOUSLY_EXPERIENCED_CONTINGENT_COACTIVITY',
                      'HISTORICALLY_ACQUIRED_CONDITIONAL_JOINT_PRACTICE'}
                     if stage=='explore' else
                     {'HISTORICALLY_ACQUIRED_CONDITIONAL_JOINT_PRACTICE'})
            offers=[x for x in packet['practical_options']
                    if x['operation']=='SING' and x.get('grounds_status') in grounds
                    and x['world_request']['addressed_party_ref']=='visitor']
            return ({'task':task,'action':'SING',
                     'practical_option_id':offers[0]['option_id']}
                    if len(offers)==1 else {'task':task,'action':'WAIT'})
        if task=='development':
            return {'task':task,'candidates':(
                packet.get('historically_possible_joint_practices',[])
                if acquire else [])}
        return fallback.propose(task,packet)
    return ValidatingSemanticService(CallbackLLMProvider(callback))

class JointPracticeR15(unittest.TestCase):
    def build(self,name,*,hearing=True,facing='entrance'):
        tmp=tempfile.TemporaryDirectory(prefix='neighbor_r15_')
        self.addCleanup(tmp.cleanup)
        db=str(Path(tmp.name)/'world.sqlite')
        rt=ConstitutiveRuntime(db,world_id=name,semantic=policy('explore'))
        self.addCleanup(rt.close)
        rt.ledger.initialize(blank_world(name),[adult('worker','Mara','workshop')])
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({
            'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{loc:{'light':'lit','sightline':'unobstructed',
                'hearing':True,'sound_path':'audible','legibility':'readable'}
                for loc in ('workshop','home')},
            'actor_conditions':{'worker':{'facing':facing,'visual':True,'light':'lit',
                'sightline':'unobstructed','hearing':hearing,
                'sound_path':'audible' if hearing else 'blocked'}}},
            request_id='geometry')
        n.contribute('arrive','MOVE',destination='workshop')
        return rt,n,db

    def test_acquired_practice_changes_cold_invitation_not_human_consent(self):
        for acquire in (True,False):
            with self.subTest(acquire=acquire):
                name='learned' if acquire else 'declined'
                rt,n,db=self.build(name)
                first=n.independent_actor_beat('worker')
                self.assertEqual(first['attempt'],'SING')
                self.assertEqual(first['status'],'PARTIAL')
                before=deepcopy(rt.ledger.actors())
                actual=n.contribute('sing','SING',target_actor_ref='worker')
                self.assertEqual(actual['status'],'PERFORMED')
                self.assertEqual(rt.ledger.actors(),before)
                rt.semantic=policy('explore',acquire)
                joined=n.independent_actor_beat('worker')
                self.assertEqual(joined['objective_outcome'],'JOINT_ACTIVITY_PERFORMED')
                self.assertEqual(joined['status'],'PERFORMED')
                actor=rt.ledger.actor('worker')[1]
                history=actor['participation_history']
                self.assertEqual(history[-2]['own_status'],'PARTIAL')
                self.assertEqual(history[-1]['reciprocated_partner_actor_visible'],'visitor')
                self.assertEqual(len(actor['joint_practices']),int(acquire))
                if acquire:
                    self.assertEqual(actor['joint_practices'][0]['source_participation_refs'],
                                     [history[-2]['id'],history[-1]['id']])
                field=rt.ledger.world(name)[1]['relations']['rel:visitor:worker']
                self.assertEqual(field['history'][-1]['contributions'][1]['committed_user_event_ref'],
                                 actual['event_ref'])
                self.assertNotIn('visitor',rt.ledger.actors())
                old_count=rt.verify()['events']
                self.assertTrue(n.contribute('sing','SING',target_actor_ref='worker')['idempotent_replay'])
                self.assertEqual(rt.verify()['events'],old_count)
                rt.close()
                cold=ConstitutiveRuntime(db,world_id=name,semantic=policy('recruit'))
                self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                later=nn.independent_actor_beat('worker')
                self.assertEqual(later['attempt'],'SING' if acquire else 'WAIT')
                self.assertEqual(later['status'],'PARTIAL' if acquire else 'PERFORMED')
                self.assertEqual(len(cold.ledger.world(name)[1]['relations']['rel:visitor:worker']['history']),1)
                nn.contribute('fresh','SING',target_actor_ref='worker')
                fresh=nn.independent_actor_beat('worker')
                self.assertEqual(fresh['attempt'],'SING' if acquire else 'WAIT')
                self.assertEqual(fresh['status'],'PERFORMED')
                self.assertEqual(len(cold.ledger.world(name)[1]['relations']['rel:visitor:worker']['history']),
                                 2 if acquire else 1)
                nn.contribute('leave','LEAVE')
                absent=nn.independent_actor_beat('worker')
                self.assertEqual(absent['attempt'],'WAIT')
                self.assertEqual(len(cold.ledger.actor('worker')[1]['joint_practices']),int(acquire))
                self.assertTrue(cold.verify()['valid'])

    def test_actual_human_voice_without_both_channels_or_freshness_not_joint_practice(self):
        for hearing,facing,stale in ((False,'entrance',False),
                                     (True,'away',False),
                                     (True,'entrance',True)):
            with self.subTest(hearing=hearing,facing=facing,stale=stale):
                name='negative'+str(hearing)+facing+str(stale)
                rt,n,_=self.build(name,hearing=hearing,facing=facing)
                n.independent_actor_beat('worker')
                out=n.contribute('sing','SING',target_actor_ref='worker')
                self.assertEqual(out['status'],'PERFORMED')
                if stale:n.contribute('elapsed','WAIT')
                rt.semantic=policy('explore',True)
                resolved=n.independent_actor_beat('worker')
                self.assertNotEqual(resolved['objective_outcome'],'JOINT_ACTIVITY_PERFORMED')
                self.assertEqual(rt.ledger.actor('worker')[1]['joint_practices'],[])
                self.assertNotIn('rel:visitor:worker',rt.ledger.world(name)[1]['relations'])
                self.assertTrue(rt.verify()['valid'])

    def test_unaddressed_singing_is_not_consent_and_cannot_bind_replay(self):
        from neighbor_runtime import EncounterRefusal
        rt,n,_=self.build('unaddressed')
        n.independent_actor_beat('worker')
        out=n.contribute('song','SING')
        self.assertEqual(out['status'],'PERFORMED')
        self.assertTrue(out['potential_actor_evidence'])
        with self.assertRaises(EncounterRefusal):
            n.contribute('song','SING',target_actor_ref='worker')
        rt.semantic=policy('explore',True)
        result=n.independent_actor_beat('worker')
        self.assertEqual(result['status'],'PARTIAL')
        self.assertEqual(rt.ledger.actor('worker')[1]['joint_practices'],[])
        self.assertNotIn('rel:visitor:worker',rt.ledger.world('unaddressed')[1]['relations'])
        self.assertTrue(rt.verify()['valid'])

if __name__=='__main__':
    unittest.main()
