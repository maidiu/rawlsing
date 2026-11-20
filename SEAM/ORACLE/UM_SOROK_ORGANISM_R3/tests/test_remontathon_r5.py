"""R5 sourcefree: monetary precision must not mint cash or erase wages."""
from copy import deepcopy
import unittest
from um_sorok_organism.types import blank_world,adult,Attempt
from um_sorok_organism.world import resolve

class TestR5ExactMonetaryClaims(unittest.TestCase):
    @staticmethod
    def fixture():
        w=blank_world();w['positions']['buyer']='workshop';w['accounts']['buyer']=1.0
        return w, {'buyer':adult('buyer','Buyer',location='workshop')}

    def test_p051_subtick_positive_food_price_not_rounded_into_free_goods(self):
        w,a=self.fixture();w['sites']['workshop']['food_price']=.000004
        before=deepcopy(w)
        with self.assertRaisesRegex(ValueError,'INVALID_MATERIAL_PRICE_PRECISION'):
            resolve(w,a,Attempt('buyer','BUY_FOOD'))
        self.assertEqual(w,before)

    def test_p051_subtick_positive_wage_does_not_disappear(self):
        w,a=self.fixture();w['institutions']['workshop_steward']['wage']=.000004
        before=deepcopy(w)
        with self.assertRaisesRegex(ValueError,'INVALID_WAGE_PRECISION'):
            resolve(w,a,Attempt('buyer','WORK'))
        self.assertEqual(w,before)

    def test_p052_unrepresentable_buyer_claim_cannot_mint_value_on_rounding(self):
        w,a=self.fixture();w['accounts']['buyer']=.000006
        w['sites']['workshop']['food_price']=.00001
        before=deepcopy(w)
        with self.assertRaisesRegex(ValueError,'INVALID_BUYER_BALANCE_PRECISION'):
            resolve(w,a,Attempt('buyer','BUY_FOOD'))
        self.assertEqual(w,before)

    def test_p052_unrepresentable_seller_claim_cannot_leak_credit(self):
        w,a=self.fixture();w['accounts']['workshop_steward']=.000006
        before=deepcopy(w)
        with self.assertRaisesRegex(ValueError,'INVALID_SELLER_BALANCE_PRECISION'):
            resolve(w,a,Attempt('buyer','BUY_FOOD'))
        self.assertEqual(w,before)

    def test_p052_unrepresentable_employer_balance_cannot_create_paid_wages(self):
        w,a=self.fixture();w['accounts']['workshop_steward']=.000006
        w['institutions']['workshop_steward']['wage']=.00001
        before=deepcopy(w)
        with self.assertRaisesRegex(ValueError,'INVALID_CONTROLLER_BALANCE_PRECISION'):
            resolve(w,a,Attempt('buyer','WORK'))
        self.assertEqual(w,before)

    def test_p052_unrepresentable_worker_balance_cannot_change_paid_wages(self):
        w,a=self.fixture();w['accounts']['buyer']=.000006
        before=deepcopy(w)
        with self.assertRaisesRegex(ValueError,'INVALID_WORKER_BALANCE_PRECISION'):
            resolve(w,a,Attempt('buyer','WORK'))
        self.assertEqual(w,before)

    def test_p051_valid_five_decimal_money_remains_transferable(self):
        w,a=self.fixture()
        w['sites']['workshop']['food_price']=.00001
        buyer_before=w['accounts']['buyer'];seller_before=w['accounts']['workshop_steward']
        response=resolve(w,a,Attempt('buyer','BUY_FOOD'))
        self.assertEqual(response.status,'PERFORMED')
        self.assertAlmostEqual(w['accounts']['buyer'],buyer_before-.00001)
        self.assertAlmostEqual(w['accounts']['workshop_steward'],seller_before+.00001)
        self.assertEqual(w['material_claims'][-1]['price_paid'],.00001)
