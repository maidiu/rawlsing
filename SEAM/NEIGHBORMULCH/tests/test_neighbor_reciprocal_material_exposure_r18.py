"""R18: actual partial signal and independently accepted material transfer
become finite visitor exposures, not actor motives or a guaranteed response.
"""
from copy import deepcopy
from pathlib import Path
import unittest
import test_neighbor_material_support_r17 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from neighbor_runtime import NeighborEncounter
import mii

def signs(view):
    return [x for x in view['mandatory'] if x['kind']=='CO_PUBLIC_OCCURRENCE']

class ReciprocalMaterialExposureR18(unittest.TestCase):
    def build(self,name,**kwargs):
        return inherited.MaterialSupportR17.build(self,name,**kwargs)

    def test_actual_signal_human_choice_transfer_cold_private_exposure(self):
        for responds in (True,False):
            with self.subTest(responds=responds):
                name='responds' if responds else 'abstains'
                rt,n,db=self.build(name)
                other=NeighborEncounter(rt,'bystander',mii_module=mii)
                other.contribute('arrive','MOVE',destination='workshop')
                # The scheduler, not the visitor, selects the actor.
                profile=n.new_private_profile()
                beat=n.continue_independent_life_during_visit(profile=profile)
                self.assertEqual(beat['status'],'INDEPENDENT_ACTOR_WORLD_EVENT_COMMITTED')
                first=signs(beat['visitor_surface'])
                self.assertEqual([s['text'] for s in first],['A signal is directed toward you.'])
                self.assertEqual(first[0]['source_event_ref'],beat['actor_event_receipt'])
                self.assertEqual([s['text'] for s in signs(other.private_surface(other.new_private_profile()))],
                                 ['A signal sounds nearby.'])
                self.assertEqual(rt.ledger.world(name)[1]['material_feeding_events'],[])
                self.assertFalse(any(x['kind']=='PUBLIC_TIP' for x in beat['visitor_surface']['mandatory']))
                # The human independently authors the response or abstention.
                # No fabricated claim that the earlier signal caused the choice.
                n.contribute('response','OFFER_FEED' if responds else 'WAIT',
                             **({'target_actor_ref':'worker'} if responds else {}))
                rt.semantic=inherited.policy('explore',True)
                outcome=n.independent_actor_beat('worker')
                w=rt.ledger.world(name)[1]
                self.assertEqual(len(w['material_feeding_events']),int(responds))
                self.assertEqual(w['holdings']['visitor']['food'],2-int(responds))
                before=deepcopy(rt.ledger.world(name))
                actors=deepcopy(rt.ledger.actors())
                sidecar=Path(db).with_suffix('.mii.json')
                n.save_private_profile(sidecar,profile)
                surface=n.private_surface_stored(sidecar)
                exposed=signs(surface)
                self.assertEqual([s['text'] for s in exposed],
                    ['A signal is directed toward you.']+
                    (['The offered food is taken.'] if responds else []))
                self.assertTrue(all(s['source_event_ref']==outcome['receipt'] for s in exposed))
                self.assertNotIn('nutrition',str(surface))
                self.assertNotIn('joint_practices',str(surface))
                self.assertNotIn('material_feeding_ref',str(surface))
                self.assertEqual(rt.ledger.world(name),before)
                self.assertEqual(rt.ledger.actors(),actors)
                self.assertEqual([s['text'] for s in signs(other.private_surface(other.new_private_profile()))],
                                 ['A signal sounds nearby.'])
                rt.close()
                cold=ConstitutiveRuntime(db,world_id=name,semantic=inherited.policy('recruit'))
                self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                self.assertEqual(signs(nn.private_surface_stored(sidecar)),exposed)
                p=nn.load_private_profile(sidecar)
                self.assertTrue(any(s['text']=='A signal is directed toward you.'
                    for e in p['exposures'] for s in e['rendered']['mandatory']
                    if s['kind']=='CO_PUBLIC_OCCURRENCE'))
                nn.contribute('later','WAIT')
                self.assertEqual(signs(nn.private_surface_stored(sidecar)),[])
                self.assertEqual(len(cold.ledger.actor('worker')[1]['joint_practices']),int(responds))
                self.assertTrue(cold.verify()['valid'])

    def test_modalities_remain_independent_and_generic_signal_never_transfers(self):
        for hearing,visible,accept in ((False,True,True),(True,False,False),
                                      (False,False,False),(True,True,False)):
            with self.subTest(hearing=hearing,visible=visible,accept=accept):
                name='modal'+str(hearing)+str(visible)+str(accept)
                rt,n,_=self.build(name,user_hearing=hearing,user_visible=visible)
                first=n.independent_actor_beat('worker')
                self.assertEqual(first['status'],'PARTIAL')
                got=signs(n.private_surface(n.new_private_profile()))
                self.assertEqual([s['text'] for s in got],
                    (['A signal is directed toward you.' if visible else 'A signal sounds nearby.']
                     if hearing else []))
                if visible:
                    n.contribute('offer','OFFER_FEED',target_actor_ref='worker')
                    rt.semantic=inherited.policy('explore' if accept else 'generic',True)
                    n.independent_actor_beat('worker')
                    view=n.private_surface(n.new_private_profile())
                    self.assertEqual([s['text'] for s in signs(view)],
                        (['A signal is directed toward you.'] if hearing else [])+
                        (['The offered food is taken.'] if accept else []))
                    self.assertFalse(any(x['kind']=='PUBLIC_TIP' for x in view['mandatory']))
                    self.assertEqual(len(rt.ledger.world(name)[1]['material_feeding_events']),int(accept))
                self.assertTrue(rt.verify()['valid'])

if __name__=='__main__':
    unittest.main()
