"""R32: same visible marking, different lawful exposure history, no human profiling."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
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
