"""REMONTATHON R4 first-fault regressions: prevent uncommitted history laundering.

These are sourcefree ledger/clock tests, not claims of native owner authority.
"""
import tempfile
import unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import canonical, digest, GRADE
from um_sorok_organism.storage import Conflict


class TestR4LedgerCausality(unittest.TestCase):
    def fresh(self, root):
        rt = ConstitutiveRuntime(str(Path(root) / 'r4.sqlite'))
        rt.initialize()
        self.assertTrue(rt.verify()['valid'])
        return rt

    def alter_world(self, rt):
        version, world = rt.ledger.world()
        world['sites']['home']['food'] += 77
        rt.ledger.conn.execute('UPDATE worlds SET body=? WHERE id=?',
                               (canonical(world), world['id']))
        with self.assertRaisesRegex(AssertionError,'LAST_WORLD_STATE_CHANGED'):
            rt.verify()

    def alter_actor(self, rt):
        _, a = rt.ledger.actor('nadia')
        a['name'] = 'IMPOSTOR_NADIA'
        rt.ledger.conn.execute('UPDATE actors SET body=? WHERE id=?',
                               (canonical(a),'nadia'))
        with self.assertRaisesRegex(AssertionError,'LAST_ACTOR_STATE_CHANGED'):
            rt.verify()

    def test_p045_uncommitted_world_cannot_be_legalized_by_next_life_step(self):
        with tempfile.TemporaryDirectory() as root:
            rt = self.fresh(root)
            try:
                self.alter_world(rt)
                with self.assertRaisesRegex(Conflict,'UNCOMMITTED_WORLD_STATE'):
                    rt.step('nadia', requested_action='WAIT')
                self.assertEqual(len(rt.ledger.events()),1)
            finally:rt.close()

    def test_p045_uncommitted_actor_cannot_be_legalized_by_next_life_step(self):
        with tempfile.TemporaryDirectory() as root:
            rt = self.fresh(root)
            try:
                self.alter_actor(rt)
                with self.assertRaisesRegex(Conflict,'UNCOMMITTED_ACTOR_STATE'):
                    rt.step('nadia', requested_action='WAIT')
                self.assertEqual(len(rt.ledger.events()),1)
            finally:rt.close()

    def test_p045_uncommitted_actor_cannot_be_legalized_by_external_cue(self):
        with tempfile.TemporaryDirectory() as root:
            rt = self.fresh(root)
            try:
                self.alter_actor(rt)
                with self.assertRaisesRegex(Conflict,'UNCOMMITTED_ACTOR_STATE'):
                    rt.cue(description='harmless cue')
                self.assertEqual(len(rt.ledger.events()),1)
            finally:rt.close()

    def test_p045_uncommitted_world_cannot_be_legalized_by_late_source_seal(self):
        with tempfile.TemporaryDirectory() as root:
            rt = self.fresh(root)
            try:
                self.alter_world(rt)
                with self.assertRaisesRegex(Conflict,'UNCOMMITTED_WORLD_STATE'):
                    rt.ledger.seal_source('source_1','SURVEY_TEST',{'yes':True})
                self.assertIsNone(rt.ledger.source('source_1'))
            finally:rt.close()

    def test_p046_deleting_genesis_cannot_be_laundered_by_new_source_seal(self):
        with tempfile.TemporaryDirectory() as root:
            rt = self.fresh(root)
            try:
                rt.ledger.conn.execute('DELETE FROM events')
                with self.assertRaisesRegex(Conflict,'MISSING_LEDGER_GENESIS'):
                    rt.ledger.seal_source('source_1','SURVEY_TEST',{'yes':True})
                self.assertIsNone(rt.ledger.source('source_1'))
                self.assertEqual(rt.ledger.events(),[])
            finally:rt.close()

    def test_p046_event_verifier_requires_actual_initialization_genesis(self):
        with tempfile.TemporaryDirectory() as root:
            rt = self.fresh(root)
            try:
                ledger=rt.ledger
                ledger.conn.execute('DELETE FROM events')
                world=ledger.world()[1]
                actors=ledger.actors()
                envelope={'world':world['id'],'clock':world['clock'],'kind':'SOURCE_SEAL',
                   'actor':None,'payload':{'source_id':'fake','source_digest':'unknown'},
                   'world_digest':digest(world),
                   'actor_digests':{aid:digest(a) for aid,a in sorted(actors.items())},
                   'grade':GRADE}
                # Fabricated event is internally hash-consistent, but is not
                # the INITIALIZATION genesis. No history is invented by test.
                prior='GENESIS'
                eid='evt_'+digest({'prev':prior,'envelope':envelope})[:20]
                chain=digest({'previous':prior,'eid':eid,'envelope':envelope})
                ledger.conn.execute('INSERT INTO events(eid,world_id,clock,actor_id,kind,payload,previous_hash,chain_hash) '
                   'VALUES(?,?,?,?,?,?,?,?)',
                   (eid,'w1',0,None,'SOURCE_SEAL',canonical(envelope),prior,chain))
                with self.assertRaisesRegex(AssertionError,'NOT_INITIALIZATION_GENESIS'):
                    rt.verify()
            finally:rt.close()

    def test_p048_second_world_cannot_be_falsely_initialized_in_same_ledger(self):
        with tempfile.TemporaryDirectory() as root:
            rt=self.fresh(root)
            second=ConstitutiveRuntime(str(Path(root)/'r4.sqlite'),world_id='world2')
            try:
                with self.assertRaisesRegex(Conflict,'MULTIWORLD_RESEARCH_DB_UNSUPPORTED'):
                    second.initialize(child_id='other_child')
                self.assertTrue(rt.verify()['valid'])
                self.assertEqual(len(rt.ledger.events()),1)
            finally:
                rt.close()
                second.close()

    def test_p047_boolean_passage_not_accepted_as_one_day(self):
        with tempfile.TemporaryDirectory() as root:
            rt = self.fresh(root)
            try:
                with self.assertRaisesRegex(ValueError,'UNSUPPORTED_TIME_PASSAGE'):
                    rt.background(True)
                self.assertEqual(rt.ledger.world()[1]['clock'],0)
                self.assertEqual(len(rt.ledger.events()),1)
            finally:rt.close()

class TestR4MaterialEconomy(unittest.TestCase):
    def test_p049_market_payment_reaches_actual_institutional_goods_controller(self):
        from um_sorok_organism.types import Attempt, adult, blank_world
        from um_sorok_organism.world import resolve
        world=blank_world()
        world['positions']['buyer']='workshop'
        world['accounts']['buyer']=3.0
        actor={'buyer':adult('buyer','Buyer',location='workshop')}
        seller='workshop_steward'
        assert world['institutions'][seller]['controls']=='workshop'
        seller_before=world['accounts'][seller]
        buyer_before=world['accounts']['buyer']
        before_sum=seller_before+buyer_before
        result=resolve(world,actor,Attempt('buyer','BUY_FOOD'))
        self.assertEqual(result.status,'PERFORMED')
        cost=world['sites']['workshop']['food_price']
        self.assertEqual(world['accounts']['buyer'],buyer_before-cost)
        self.assertEqual(world['accounts'][seller],seller_before+cost)
        self.assertAlmostEqual(world['accounts']['buyer']+world['accounts'][seller],before_sum)
        receipt=world['material_claims'][-1]
        self.assertEqual(receipt['kind'],'FOOD_PURCHASE')
        self.assertEqual(receipt['seller'],seller)
        self.assertEqual(receipt['price_paid'],cost)

    def test_p050_boolean_price_and_wage_do_not_coerce_to_money(self):
        from copy import deepcopy
        from um_sorok_organism.types import Attempt, adult, blank_world
        from um_sorok_organism.world import resolve
        for field,value,action,error in (
            ('food_price',True,'BUY_FOOD','INVALID_MATERIAL_PRICE'),
            ('wage',False,'WORK','INVALID_WAGE')):
            with self.subTest(field=field):
                world=blank_world()
                world['positions']['buyer']='workshop'
                world['accounts']['buyer']=2.0
                if field=='food_price':world['sites']['workshop'][field]=value
                else:world['institutions']['workshop_steward'][field]=value
                actors={'buyer':adult('buyer','Buyer',location='workshop')}
                before=deepcopy(world)
                with self.assertRaisesRegex(ValueError,error):
                    resolve(world,actors,Attempt('buyer',action))
                self.assertEqual(world,before)

    def test_p049_no_sellable_counterpart_at_unowned_food_site(self):
        from copy import deepcopy
        from um_sorok_organism.types import Attempt, adult, blank_world
        from um_sorok_organism.world import resolve
        world=blank_world()
        world['positions']['buyer']='home'
        world['accounts']['buyer']=3.0
        actor={'buyer':adult('buyer','Buyer')}
        before=deepcopy(world)
        result=resolve(world,actor,Attempt('buyer','BUY_FOOD'))
        self.assertEqual(result.status,'BLOCKED')
        self.assertEqual(result.objective_description,'NO_OBJECTIVE_SELLER')
        self.assertEqual(world['accounts'],before['accounts'])
        self.assertEqual(world.get('holdings',{}),before.get('holdings',{}))
        self.assertEqual(world['sites'],before['sites'])

    def test_p049_invalid_seller_account_is_rejected_before_debit_and_stock_transfer(self):
        from copy import deepcopy
        from um_sorok_organism.types import Attempt, adult, blank_world
        from um_sorok_organism.world import resolve
        world=blank_world()
        world['positions']['buyer']='workshop'
        world['accounts']['buyer']=3.0
        world['accounts']['workshop_steward']=float('nan')
        actor={'buyer':adult('buyer','Buyer',location='workshop')}
        before=deepcopy(world)
        with self.assertRaisesRegex(ValueError,'INVALID_SELLER_BALANCE'):
            resolve(world,actor,Attempt('buyer','BUY_FOOD'))
        self.assertEqual(world['accounts']['buyer'],before['accounts']['buyer'])
        self.assertEqual(world['sites'],before['sites'])
        self.assertEqual(world.get('material_claims'),before.get('material_claims'))

    def test_p049_self_sale_does_not_mint_money(self):
        from um_sorok_organism.types import Attempt, adult, blank_world
        from um_sorok_organism.world import resolve
        world=blank_world()
        world['positions']['workshop_steward']='workshop'
        actor={'workshop_steward':adult('workshop_steward','Institutional agent',location='workshop')}
        money_before=world['accounts']['workshop_steward']
        result=resolve(world,actor,Attempt('workshop_steward','BUY_FOOD'))
        self.assertEqual(result.status,'PERFORMED')
        self.assertEqual(world['accounts']['workshop_steward'],money_before)
        self.assertEqual(world['material_claims'][-1]['seller'],'workshop_steward')
