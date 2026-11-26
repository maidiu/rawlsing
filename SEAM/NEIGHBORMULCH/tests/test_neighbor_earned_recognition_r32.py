"""R32: same visible marking, different lawful exposure history, no human profiling."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from collections import Counter
from time import perf_counter_ns
import json
import test_neighbor_mii_cold_profile_r5 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,blank_world
from neighbor_runtime import NeighborEncounter
import mii

MARK='Blue thread crosses the left strap.'
LABEL='the blue-thread sandals'
CLOSE=MARK+' Small writing under the heel says 1937.'

class EarnedRecognitionR32(unittest.TestCase):
    def build(self, *, visible=True):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        db=str(Path(tmp.name)/'world.sqlite')
        sidecar=Path(tmp.name)/'profile.json'
        rt=ConstitutiveRuntime(db);self.addCleanup(rt.close)
        w=blank_world(rt.world_id)
        w['material_objects']['sandals']={
            'id':'sandals','location':'workshop','grade':'SOURCEFREE_TEST_ONLY',
            'public_glance':MARK if visible else 'A pair of sandals lies here.',
            'public_close':CLOSE,
            'public_recognition':{'identity':LABEL,'marking':'blue-thread-left-strap',
                                  'evidence':MARK}}
        rt.ledger.initialize(w,[adult('worker','Mara','workshop')])
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{'workshop':{'light':'lit','sightline':'unobstructed',
                'legibility':'readable','hearing':True,'sound_path':'audible'}},
            'actor_conditions':{'worker':{'facing':'entrance','visual':True,'light':'lit',
                'sightline':'unobstructed','hearing':True,'sound_path':'audible'}}},request_id='geometry')
        self.assertEqual(n.contribute('arrive','MOVE',destination='workshop')['status'],'PERFORMED')
        return rt,n,db,sidecar

    def test_familiar_marking_after_cold_reopen_without_repeating_close(self):
        rt,n,db,sidecar=self.build()
        before=n.private_surface_stored(sidecar)
        self.assertEqual(before['optional']['text'],MARK)
        self.assertEqual(before['recognition'],{})
        look=n.contribute('look','LOOK',target_object_ref='sandals')
        self.assertEqual(look['status'],'PERFORMED')
        world=deepcopy(rt.ledger.world(rt.world_id));actors=deepcopy(rt.ledger.actors())
        first=n.private_surface_stored(sidecar,command='look',target='sandals')
        self.assertEqual(first['optional']['text'],CLOSE)
        earned=first['recognition']['sandals']
        self.assertEqual(earned['identity'],LABEL)
        self.assertEqual(earned['event_id'],look['receipt'])
        self.assertEqual(earned['confidence'],'PRESENTATION_SUPPORTED')
        self.assertTrue(earned['human_recognition_not_established'])
        self.assertEqual(rt.ledger.world(rt.world_id),world)
        self.assertEqual(rt.ledger.actors(),actors)
        n.contribute('wait','WAIT')
        rt.close()
        cold=ConstitutiveRuntime(db);self.addCleanup(cold.close)
        nn=NeighborEncounter(cold,'visitor',mii_module=mii)
        before=deepcopy(cold.ledger.world(cold.world_id));ac=deepcopy(cold.ledger.actors())
        self.assertEqual(nn.load_private_profile(sidecar)['recognized'],{})
        familiar=nn.private_surface_stored(sidecar)
        fresh=nn.private_surface(nn.new_private_profile())
        self.assertEqual(familiar['optional'],fresh['optional'])
        self.assertEqual(familiar['optional']['text'],MARK)
        self.assertEqual(fresh['recognition'],{})
        again=familiar['recognition']['sandals']
        self.assertEqual(again['event_id'],look['receipt'])
        self.assertEqual(again['identity'],LABEL)
        self.assertTrue(again['prior_exposure_ref'])
        self.assertNotIn('1937',str(familiar))
        self.assertEqual(cold.ledger.world(cold.world_id),before)
        self.assertEqual(cold.ledger.actors(),ac)
        self.assertTrue(cold.verify()['valid'])

    def test_inference_economy_r12_bounded_scope_read_preserves_private_history(self):
        rt,n,db,sidecar=self.build()
        n.contribute('look','LOOK',target_object_ref='sandals')
        n.private_surface_stored(sidecar,command='look',target='sandals')
        original=rt.ledger._iter_events
        results=[]
        for waits in (4,24):
            for i in range(waits-(0 if waits==4 else 4)):
                n.contribute('wait-%d-%d'%(waits,i),'WAIT')
            root=rt.ledger.events(1)[0]['id']
            count=rt.verify()['events']
            expected_world=rt.ledger.world(rt.world_id)
            expected_actors=rt.ledger.actors()
            expected_sidecar=sidecar.read_bytes()
            observations=[]
            for legacy in (True,False):
                stats=Counter()
                def counted(limit=None):
                    stats['calls']+=1
                    # Exact old consumer: read the full list even for scope.
                    # Leave full history queries unchanged.
                    for e in original(None if legacy else limit):
                        stats['decoded_rows']+=1
                        stats['decoded_envelope_bytes']+=len(e['envelope_bytes'].encode('utf-8'))
                        yield e
                t=perf_counter_ns()
                with patch.object(rt.ledger,'_iter_events',counted):
                    p=n.load_private_profile(sidecar)
                    self.assertEqual(p['scope']['root'],root)
                    scope_cost=dict(stats)
                    view=n.private_surface(p)
                    n.save_private_profile(sidecar,p)
                    output=(view,p,sidecar.read_bytes())
                elapsed=perf_counter_ns()-t
                sidecar.write_bytes(expected_sidecar)
                observations.append((output,scope_cost,dict(stats),elapsed))
            self.assertEqual(observations[0][0],observations[1][0])
            self.assertEqual(observations[0][1]['calls'],2)
            self.assertEqual(observations[0][1]['decoded_rows'],count*2)
            self.assertEqual(observations[1][1]['decoded_rows'],2)
            self.assertEqual(observations[0][2]['calls'],observations[1][2]['calls'])
            # The surface still reads the complete relevant ledger; only
            # first-event scope requests are bounded.
            self.assertEqual(observations[0][2]['decoded_rows']-
                             observations[1][2]['decoded_rows'],4*(count-1))
            self.assertEqual(observations[1][0][0]['recognition']['sandals']['identity'],LABEL)
            self.assertNotIn('1937',str(observations[1][0][0]))
            self.assertEqual(rt.ledger.world(rt.world_id),expected_world)
            self.assertEqual(rt.ledger.actors(),expected_actors)
            self.assertTrue(rt.verify()['valid'])
            results.append({'waits':waits,'events':count,
                'legacy_scope':observations[0][1],'bounded_scope':observations[1][1],
                'legacy_total':observations[0][2],'bounded_total':observations[1][2],
                'legacy_ns':observations[0][3],'bounded_ns':observations[1][3]})
        print('INFERENCE_ECONOMY_R12_SCOPE '+json.dumps(results,sort_keys=True))

    def test_no_marking_at_glance_no_recognition_and_no_foreign_receipt(self):
        rt,n,db,sidecar=self.build(visible=False)
        n.contribute('look','LOOK',target_object_ref='sandals')
        p=n.new_private_profile()
        self.assertIn('sandals',n.private_surface(p,command='look',target='sandals')['recognition'])
        n.contribute('wait','WAIT')
        self.assertEqual(n.private_surface(p)['recognition'],{})
        # Even an edited, rehashed exposure with a foreign visitor's actual
        # event cannot confer this visitor a receipt. No cryptographic claim
        # for an otherwise app-trusted sidecar.
        rt2,nn,_,_=self.build()
        look=nn.contribute('look','LOOK',target_object_ref='sandals')
        p2=nn.new_private_profile()
        nn.private_surface(p2,command='look',target='sandals')
        other=NeighborEncounter(rt2,'other',mii_module=mii)
        other.contribute('other-arrive','MOVE',destination='workshop')
        q=other.new_private_profile()
        e=deepcopy(p2['exposures'][-1]);e['scope']=deepcopy(q['scope'])
        e['entry_hash']=mii.digest({k:v for k,v in e.items() if k!='entry_hash'})
        q['exposures']=[e];q['presentation_seq']=1
        q['recognized']=deepcopy(p2['recognized'])
        view=other.private_surface(q)
        self.assertEqual(view['recognition'],{})
        self.assertEqual(q['recognized'],{})
        self.assertEqual(view['optional']['text'],MARK)
        self.assertNotIn('1937',str(view))
        self.assertTrue(rt2.verify()['valid'])

if __name__=='__main__':unittest.main()
