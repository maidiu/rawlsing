"""Sourcefree SR-P005 regression: material custody and invalid economic transfer.

Tests witness *world effects*; they don't issue real institution/economic science.
"""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from um_sorok_organism.types import Attempt, adult, blank_world
from um_sorok_organism.world import resolve
from um_sorok_organism.runtime import ConstitutiveRuntime


def world_at_workshop():
    world=blank_world()
    world['positions']['worker']='workshop'
    return world,{'worker':adult('worker','Worker',location='workshop')}


class SRP005WorldRegression(unittest.TestCase):
    def test_controlled_materials_cannot_be_consumed_by_ungranted_visitor(self):
        world,actors=world_at_workshop()
        stock=world['sites']['workshop']['stock']
        actual=resolve(world,actors,Attempt('worker','REPAIR'))
        self.assertEqual(actual.status,'BLOCKED')
        self.assertEqual(actual.objective_description,'MATERIAL_USE_NOT_AUTHORIZED')
        self.assertEqual(world['sites']['workshop']['stock'],stock)

    def test_explicit_site_material_grant_allows_repair_but_not_ownership_transfer(self):
        world,actors=world_at_workshop()
        world['sites']['workshop']['material_use_grants']=['worker']
        stock=world['sites']['workshop']['stock']
        actual=resolve(world,actors,Attempt('worker','REPAIR'))
        self.assertEqual(actual.status,'PERFORMED')
        self.assertEqual(actual.objective_description,'REPAIR_PERFORMED')
        self.assertEqual(world['sites']['workshop']['stock'],stock-1)
        self.assertEqual(world['sites']['workshop']['controller'],'workshop_steward')

    def test_invalid_negative_food_price_refused_before_material_or_money_mutation(self):
        world,actors=world_at_workshop()
        world['accounts']['worker']=0.0
        world['sites']['workshop']['food_price']=-3.0
        before=deepcopy(world)
        with self.assertRaisesRegex(ValueError,'INVALID_MATERIAL_PRICE'):
            resolve(world,actors,Attempt('worker','BUY_FOOD'))
        self.assertEqual(world,before)

    def test_invalid_negative_wage_refused_before_production_or_money_mutation(self):
        world,actors=world_at_workshop()
        world['accounts']['worker']=0.0
        world['institutions']['workshop_steward']['wage']=-5.0
        before=deepcopy(world)
        with self.assertRaisesRegex(ValueError,'INVALID_WAGE'):
            resolve(world,actors,Attempt('worker','WORK'))
        self.assertEqual(world,before)

    def test_institutionally_controlled_hall_stock_not_free_when_site_label_missing(self):
        world=blank_world()
        world['positions']['visitor']='hall'
        actors={'visitor':adult('visitor','Visitor',location='hall')}
        stock=world['sites']['hall']['stock']
        self.assertNotIn('controller',world['sites']['hall'])
        self.assertEqual(world['institutions']['hall_board']['controls'],'hall')
        actual=resolve(world,actors,Attempt('visitor','REPAIR'))
        self.assertEqual(actual.status,'BLOCKED')
        self.assertEqual(actual.objective_description,'MATERIAL_USE_NOT_AUTHORIZED')
        self.assertEqual(world['sites']['hall']['stock'],stock)

    def test_mismatched_controller_cannot_reclassify_controlled_stock_as_unowned(self):
        world,actors=world_at_workshop()
        world['institutions']['workshop_steward']['controls']='hall'
        before=deepcopy(world['sites']['workshop'])
        actual=resolve(world,actors,Attempt('worker','WORK'))
        self.assertEqual(actual.status,'BLOCKED')
        self.assertEqual(actual.objective_description,'MATERIAL_CONTROLLER_UNQUALIFIED')
        self.assertEqual(world['sites']['workshop'],before)
        self.assertEqual(world['material_claims'],[])

    def test_nonfinite_price_and_wage_fail_closed(self):
        for operation,field_owner,field_name,invalid,error in (
            ('BUY_FOOD','site','food_price',float('inf'),'INVALID_MATERIAL_PRICE'),
            ('WORK','institution','wage',float('nan'),'INVALID_WAGE')):
            with self.subTest(operation=operation):
                world,actors=world_at_workshop()
                world['accounts']['worker']=0.0
                target=(world['sites']['workshop'] if field_owner=='site'
                        else world['institutions']['workshop_steward'])
                target[field_name]=invalid
                before=deepcopy(world)
                with self.assertRaisesRegex(ValueError,error):
                    resolve(world,actors,Attempt('worker',operation))
                self.assertEqual(world,before)

    def test_site_material_access_is_live_world_power_not_actor_belief(self):
        packet={'source_ref':'synthetic','answers':{'fictional_question':'possible'},'fictional_seed':{'projects':[]}}
        with tempfile.TemporaryDirectory() as d:
            path=str(Path(d)/'sr005.sqlite')
            rt=ConstitutiveRuntime(path)
            try:
                rt.initialize([('worker','Worker',packet)])
                self.assertEqual(rt.step('worker',requested_action='MOVE',object_ref='workshop')['status'],'PERFORMED')
                stock=rt.ledger.world()[1]['sites']['workshop']['stock']
                blocked=rt.step('worker',requested_action='REPAIR')
                self.assertEqual(blocked['status'],'BLOCKED')
                self.assertEqual(blocked['objective_outcome'],'MATERIAL_USE_NOT_AUTHORIZED')
                self.assertEqual(rt.ledger.world()[1]['sites']['workshop']['stock'],stock)
                self.assertTrue(rt.verify()['valid'])
            finally:
                rt.close()


if __name__=='__main__':
    unittest.main()
