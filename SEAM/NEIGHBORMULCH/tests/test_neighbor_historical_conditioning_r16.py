"""Same encounter/constitution, differently conditioned material worlds.

No survey, PYAT import, dummy answers or alternative psychological engine.
Sourcefree dated institutional inputs exercise the existing material conjunction
owner; this is not proof of native PYAT or general historical entrance.
"""
from copy import deepcopy
import unittest
import test_neighbor_material_participation_r13 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from neighbor_runtime import NeighborEncounter
import mii


def condition(world, mode):
    if mode == 'thin':
        return
    world.setdefault('institutional_access_rules', []).append({
        'id':'repair-institution','source_ref':'authored-institution-v1',
        'operation':'REPAIR','location':'workshop',
        'all_of':[{'kind':'RECORDED_POSITION','field':'repair_authority',
                   'equals':'qualified'}]})
    records=world.setdefault('positioned_material_records',[])
    def add(actor,value,source,start=0,until=None):
        records.append({'actor':actor,'field':'repair_authority','value':value,
                        'source_ref':source,'effective_from':start,
                        'effective_until':until})
    add('worker','qualified','worker-existing-authority')
    if mode=='permitted':
        add('visitor','qualified','visitor-authority')
    elif mode=='denied':
        add('visitor','excluded','visitor-exclusion')
    elif mode=='conflict':
        add('visitor','qualified','visitor-authority')
        add('visitor','excluded','visitor-exclusion')
    elif mode=='temporal':
        add('visitor','qualified','future-grant',start=10,until=11)
    else:
        raise AssertionError(mode)


class HistoricalConditioningR16(unittest.TestCase):
    def build(self,name,mode):
        return inherited.MaterialParticipationR13.build(
            self,name,True,world_setup=lambda w:condition(w,mode))

    def test_same_psychology_consumes_material_difference_not_upstream_identity(self):
        for mode,decision,performed in (
                ('thin',None,True),('permitted','PERMITTED_BY_ALL_RULES',True),
                ('denied','BLOCKED',False),('conflict','UNRESOLVED',False)):
            with self.subTest(mode=mode):
                rt,n,db,ref=self.build(mode,mode)
                before=deepcopy(rt.ledger.actors())
                original=rt.ledger.world(mode)[1]
                result=n.contribute('work','REPAIR',target_object_ref=ref)
                self.assertEqual(result['status'],'PERFORMED' if performed else 'BLOCKED')
                self.assertEqual(rt.ledger.actors(),before)
                world=rt.ledger.world(mode)[1]
                self.assertEqual(world['sites']['workshop']['stock'],
                    original['sites']['workshop']['stock']-int(performed))
                self.assertEqual(world['material_objects'][ref]['condition'],.8 if performed else .56)
                event=world['neighbor_user_events'][-1]
                self.assertEqual(event.get('objective_material_gate_decision'),decision)
                if decision:
                    audit=world['material_gate_audit'][-1]
                    self.assertEqual(audit['evaluation']['decision'],decision)
                    self.assertEqual(audit['evaluation']['readset'],['authored-institution-v1'])
                self.assertNotIn('objective_material_gate',str(result))
                self.assertNotIn('visitor-exclusion',str(result))
                rt.semantic=inherited.MaterialParticipationR13.semantic('inspect')
                self.assertEqual(n.independent_actor_beat('worker')['attempt'],'INSPECT')
                self.assertEqual(len(rt.ledger.actor('worker')[1]['material_investments']),int(performed))
                rt.close()
                cold=ConstitutiveRuntime(db,world_id=mode,
                      semantic=inherited.MaterialParticipationR13.semantic('recruit'))
                self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                later=nn.independent_actor_beat('worker')
                self.assertEqual(later['attempt'],'REPAIR' if performed else 'WAIT')
                self.assertEqual(later['status'],'PERFORMED')
                nn.contribute('look','LOOK',target_object_ref=ref)
                view=nn.private_surface(nn.new_private_profile(),command='look',target=ref)
                self.assertEqual(view['optional']['text'],
                                 'It appears sound.' if performed else 'It appears worn.')
                self.assertNotIn('authored-institution-v1',str(view))
                self.assertNotIn('visitor-exclusion',str(view))
                self.assertTrue(cold.verify()['valid'])

    def test_dated_authority_changes_actual_permission_without_rewriting_history(self):
        rt,n,db,ref=self.build('temporal','temporal')
        early=n.contribute('early','REPAIR',target_object_ref=ref)
        self.assertEqual(early['status'],'BLOCKED')
        self.assertEqual(rt.ledger.world('temporal')[1]['neighbor_user_events'][-1]
                         ['objective_material_gate_decision'],'UNRESOLVED')
        prior_ids=[e['id'] for e in rt.ledger.events()]
        while rt.ledger.world('temporal')[1]['clock']<10:
            n.contribute('wait'+str(rt.ledger.world('temporal')[1]['clock']),'WAIT')
        rt.close()
        cold=ConstitutiveRuntime(db,world_id='temporal')
        self.addCleanup(cold.close)
        nn=NeighborEncounter(cold,'visitor',mii_module=mii)
        count=cold.verify()['events']
        self.assertEqual(nn.contribute('early','REPAIR',target_object_ref=ref)['status'],'BLOCKED')
        self.assertEqual(cold.verify()['events'],count)
        valid=nn.contribute('now','REPAIR',target_object_ref=ref)
        self.assertEqual(valid['status'],'PERFORMED')
        nn.contribute('wait-expiry','WAIT')
        expired=nn.contribute('expired','REPAIR',target_object_ref=ref)
        self.assertEqual(expired['status'],'BLOCKED')
        world=cold.ledger.world('temporal')[1]
        self.assertEqual(world['material_objects'][ref]['condition'],.8)
        self.assertEqual(world['neighbor_user_events'][-1]['objective_material_gate_decision'],'UNRESOLVED')
        self.assertEqual([e['id'] for e in cold.ledger.events()[:len(prior_ids)]],prior_ids)
        self.assertTrue(cold.verify()['valid'])


if __name__=='__main__':
    unittest.main()
