"""R6 negative-first sourcefree material integrity tests; no economic model issuance."""
import copy
import math
import sys
import unittest
from um_sorok_organism.types import blank_world, adult, Attempt
from um_sorok_organism.world import resolve

class MaterialConservationR6(unittest.TestCase):
    @staticmethod
    def fixture(actor_id='buyer', loc='workshop'):
        w=blank_world()
        w['positions'][actor_id]=loc
        w['accounts'][actor_id]=1.0
        a={actor_id:adult(actor_id,'Test Worker',location=loc)}
        return w,a

    def assert_rejected_without_world_change(self, w, a, action, reason):
        before=copy.deepcopy(w)
        with self.assertRaisesRegex(ValueError,reason):
            resolve(w,a,Attempt(next(iter(a)),action))
        self.assertEqual(w,before)

    def test_p053_tiny_purchase_from_huge_buyer_balance_cannot_be_free(self):
        w,a=self.fixture();w['accounts']['buyer']=1e20
        self.assert_rejected_without_world_change(w,a,'BUY_FOOD','INVALID_BUYER_TRANSFER_PRECISION')

    def test_p053_tiny_credit_to_huge_seller_account_cannot_vanish(self):
        w,a=self.fixture();w['accounts']['workshop_steward']=1e20
        self.assert_rejected_without_world_change(w,a,'BUY_FOOD','INVALID_SELLER_TRANSFER_PRECISION')

    def test_p053_overflow_seller_credit_cannot_serialize_nonfinite_cash(self):
        w,a=self.fixture();w['accounts']['buyer']=sys.float_info.max
        w['sites']['workshop']['food_price']=sys.float_info.max
        w['accounts']['workshop_steward']=sys.float_info.max
        self.assert_rejected_without_world_change(w,a,'BUY_FOOD','INVALID_SELLER_TRANSFER_PRECISION')

    def test_p054_worker_wage_credit_lost_at_large_account(self):
        w,a=self.fixture();w['accounts']['buyer']=1e20
        self.assert_rejected_without_world_change(w,a,'WORK','INVALID_WORKER_TRANSFER_PRECISION')

    def test_p054_employer_wage_debit_lost_at_large_account(self):
        w,a=self.fixture();w['accounts']['workshop_steward']=1e20
        self.assert_rejected_without_world_change(w,a,'WORK','INVALID_EMPLOYER_TRANSFER_PRECISION')

    def test_p054_worker_credit_overflow_before_stock_changes(self):
        w,a=self.fixture();w['accounts']['workshop_steward']=sys.float_info.max
        w['accounts']['buyer']=sys.float_info.max
        w['institutions']['workshop_steward']['wage']=sys.float_info.max
        self.assert_rejected_without_world_change(w,a,'WORK','INVALID_WORKER_TRANSFER_PRECISION')

    def test_p055_food_stock_large_does_not_claim_decrement_that_never_happened(self):
        w,a=self.fixture();w['sites']['workshop']['food']=1e20
        self.assert_rejected_without_world_change(w,a,'BUY_FOOD','INVALID_SITE_FOOD_DELTA')

    def test_p055_owned_food_large_does_not_claim_eating_without_consumption(self):
        w,a=self.fixture();w['holdings']={'buyer':{'food':1e20}}
        self.assert_rejected_without_world_change(w,a,'EAT','INVALID_OWNED_FOOD_DELTA')

    def test_p055_owned_food_large_cannot_absorb_purchased_goods(self):
        w,a=self.fixture();w['holdings']={'buyer':{'food':1e20}}
        self.assert_rejected_without_world_change(w,a,'BUY_FOOD','INVALID_OWNED_FOOD_DELTA')

    def test_p055_work_stock_large_cannot_absorb_produced_goods(self):
        w,a=self.fixture();w['sites']['workshop']['stock']=1e20
        self.assert_rejected_without_world_change(w,a,'WORK','INVALID_SITE_STOCK_DELTA')

    def test_p055_repair_material_stock_large_must_really_decrement(self):
        w,a=self.fixture();w['sites']['workshop']['stock']=1e20
        w['sites']['workshop']['material_use_grants']=['buyer']
        self.assert_rejected_without_world_change(w,a,'REPAIR','INVALID_SITE_STOCK_DELTA')

    def test_p056_self_wage_cannot_mint_pay_from_self(self):
        w,a=self.fixture(actor_id='workshop_steward');w['accounts']['workshop_steward']=10.0
        before=copy.deepcopy(w)
        r=resolve(w,a,Attempt('workshop_steward','WORK'))
        self.assertEqual(r.status,'PERFORMED')
        self.assertEqual(w['accounts']['workshop_steward'],before['accounts']['workshop_steward'])
        self.assertEqual(w['sites']['workshop']['stock'],before['sites']['workshop']['stock']+2)
        self.assertTrue(w['material_claims'][-1]['worker_control_of_output'])
        self.assertEqual(w['material_claims'][-1]['wage'],0)

    def test_p056_self_purchase_does_not_claim_payment_without_transfer(self):
        w,a=self.fixture(actor_id='workshop_steward');w['accounts']['workshop_steward']=10.0
        before=copy.deepcopy(w)
        r=resolve(w,a,Attempt('workshop_steward','BUY_FOOD'))
        self.assertEqual(r.status,'PERFORMED')
        self.assertEqual(w['sites']['workshop']['food'],before['sites']['workshop']['food']-1)
        self.assertEqual(w['material_claims'][-1]['price_paid'],0)
        self.assertEqual(w['material_claims'][-1]['kind'],'SELF_STOCK_REALLOCATION')

    def test_p056_self_owned_food_still_accessible_without_cash(self):
        w,a=self.fixture(actor_id='workshop_steward')
        w['accounts']['workshop_steward']=0.0
        before=copy.deepcopy(w)
        r=resolve(w,a,Attempt('workshop_steward','BUY_FOOD'))
        self.assertEqual(r.status,'PERFORMED')
        self.assertEqual(w['accounts']['workshop_steward'],0.0)
        self.assertEqual(w['sites']['workshop']['food'],before['sites']['workshop']['food']-1)
        self.assertEqual(w['material_claims'][-1]['price_paid'],0)

    def test_p055_shared_food_at_extreme_count_cannot_be_consumed_without_decrement(self):
        w,a=self.fixture(loc='home');w['sites']['home']['food']=1e20
        self.assert_rejected_without_world_change(w,a,'EAT','INVALID_SITE_FOOD_DELTA')

    def test_p055_self_production_at_unrepresentable_stock_rejected(self):
        w,a=self.fixture(actor_id='workshop_steward')
        w['sites']['workshop']['stock']=1e20
        self.assert_rejected_without_world_change(w,a,'WORK','INVALID_SITE_STOCK_DELTA')

    def test_p053_repeated_sales_conserve_both_money_and_physical_goods(self):
        from decimal import Decimal
        w,a=self.fixture();w['accounts']['buyer']=100.0
        w['sites']['workshop']['food']=120;w['sites']['workshop']['food_price']=.00001
        before=Decimal(str(w['accounts']['buyer']))+Decimal(str(w['accounts']['workshop_steward']))
        for _ in range(100):
            self.assertEqual(resolve(w,a,Attempt('buyer','BUY_FOOD')).status,'PERFORMED')
        after=Decimal(str(w['accounts']['buyer']))+Decimal(str(w['accounts']['workshop_steward']))
        self.assertEqual(after,before)
        self.assertEqual(w['holdings']['buyer']['food'],100)
        self.assertEqual(w['sites']['workshop']['food'],20)
        self.assertEqual(len(w['material_claims']),100)

    def test_p054_repeated_paid_work_conserves_wage_money_and_real_stock(self):
        from decimal import Decimal
        w,a=self.fixture();w['accounts']['buyer']=0.0
        w['accounts']['workshop_steward']=100.0
        before=Decimal('100.0')
        for _ in range(120):
            self.assertEqual(resolve(w,a,Attempt('buyer','WORK')).status,'PERFORMED')
        after=Decimal(str(w['accounts']['buyer']))+Decimal(str(w['accounts']['workshop_steward']))
        self.assertEqual(after,before)
        self.assertEqual(w['sites']['workshop']['stock'],245)
        self.assertEqual(len(w['material_claims']),120)
        self.assertEqual(w.get('wage_arrears',[]),[])

    def test_p053_valid_five_decimal_cash_flow_still_works(self):
        w,a=self.fixture();w['accounts']['buyer']=1.25
        r=resolve(w,a,Attempt('buyer','BUY_FOOD'))
        self.assertEqual(r.status,'PERFORMED')
        self.assertAlmostEqual(w['accounts']['buyer'],.25)
        self.assertAlmostEqual(w['accounts']['workshop_steward'],13.)

    def test_p055_normal_material_inventory_changes_still_work(self):
        w,a=self.fixture();w['sites']['workshop']['food']=3
        r=resolve(w,a,Attempt('buyer','BUY_FOOD'))
        self.assertEqual(r.status,'PERFORMED')
        self.assertEqual(w['sites']['workshop']['food'],2)
        self.assertEqual(w['holdings']['buyer']['food'],1)
        r=resolve(w,a,Attempt('buyer','EAT'))
        self.assertEqual(r.status,'PERFORMED')
        self.assertEqual(w['holdings']['buyer']['food'],0)

if __name__=='__main__': unittest.main()
