"""Independent cross-family adversarial probes for frozen REMONTATHON R9.
Not an implementation change; original 177 tests untouched. Nov 20 2026.
"""
import copy, math, tempfile, unittest
from pathlib import Path
from um_sorok_organism.types import Attempt, adult, blank_world, canonical
from um_sorok_organism.world import resolve, IndependentWorldAuthority, add_cue
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.storage import ResearchLedger, Conflict
from um_sorok_organism.psychodynamics import validate_tendencies
from um_sorok_organism.development import admit, InvalidDevelopment
from um_sorok_organism.semantics import HeuristicSemanticProvider


def scene():
    w=blank_world();w['positions']={'ann':'workshop','joann':'workshop'}
    a={k:adult(k,k.title(),location='workshop') for k in ('ann','joann')}
    w['accounts']['ann']=10.0;w['accounts']['joann']=10.0
    return w,a

class ReviewerWorldAndRights(unittest.TestCase):
    def test_mixed_malformed_world_grants_do_not_promote_rights(self):
        for malformed in ('joann',{'ann':True},('ann',),[1],[None],[''],True):
            with self.subTest(grant=repr(malformed)):
                w,a=scene();w['sites']['workshop']['material_use_grants']=malformed
                before=copy.deepcopy(w)
                with self.assertRaises(ValueError):resolve(w,a,Attempt('ann','REPAIR'))
                self.assertEqual(w,before)

    def test_nonmembers_may_not_consume_controlled_repair_stock(self):
        w,a=scene();w['sites']['workshop']['material_use_grants']=['joann']
        stock=w['sites']['workshop']['stock']
        res=resolve(w,a,Attempt('ann','REPAIR'))
        self.assertEqual(res.status,'BLOCKED');self.assertEqual(w['sites']['workshop']['stock'],stock)
        good=resolve(w,a,Attempt('joann','REPAIR'))
        self.assertEqual(good.status,'PERFORMED');self.assertEqual(w['sites']['workshop']['stock'],stock-1)

    def test_price_and_wage_adversarial_matrix_fails_atomic(self):
        invalid=[True,False,'1',-0.1,float('nan'),float('inf'),0.000001,1.000001]
        for operation,field in (('BUY_FOOD','food_price'),('WORK','wage')):
            for bad in invalid:
                with self.subTest(operation=operation,value=repr(bad)):
                    w,a=scene();holder=w['sites']['workshop'] if operation=='BUY_FOOD' else w['institutions']['workshop_steward']
                    holder[field]=bad
                    before=copy.deepcopy(w)
                    with self.assertRaises(ValueError):resolve(w,a,Attempt('ann',operation))
                    self.assertEqual(w,before)

    def test_normal_buyer_seller_double_entry_and_material_claim(self):
        w,a=scene();w['accounts']['workshop_steward']=2.5
        old_buyer=w['accounts']['ann'];old_seller=w['accounts']['workshop_steward']
        res=resolve(w,a,Attempt('ann','BUY_FOOD'))
        self.assertEqual(res.status,'PERFORMED')
        self.assertEqual(w['accounts']['ann'],old_buyer-1)
        self.assertEqual(w['accounts']['workshop_steward'],old_seller+1)
        self.assertEqual(w['accounts']['ann']+w['accounts']['workshop_steward'],old_buyer+old_seller)
        self.assertEqual(w['holdings']['ann']['food'],1)

    def test_large_account_no_phantom_money_or_goods(self):
        w,a=scene();w['accounts']['ann']=1e20
        w['sites']['workshop']['food_price']=0.00001
        before=copy.deepcopy(w)
        with self.assertRaises(ValueError):resolve(w,a,Attempt('ann','BUY_FOOD'))
        self.assertEqual(w,before)

    def test_large_material_stock_no_phantom_production(self):
        w,a=scene();w['sites']['workshop']['stock']=1e20
        before=copy.deepcopy(w)
        with self.assertRaises(ValueError):resolve(w,a,Attempt('ann','WORK'))
        self.assertEqual(w,before)

    def test_missing_material_site_does_not_generate_stock(self):
        w,a=scene();w['sites'].pop('workshop')
        res=resolve(w,a,Attempt('ann','WORK'))
        self.assertEqual(res.status,'BLOCKED');self.assertEqual(res.objective_description,'UNKNOWN_MATERIAL_SITE')
        self.assertEqual(w['material_claims'],[])

    def test_unqualified_partner_target_must_fail_without_world_mutation(self):
        w,a=scene();before=copy.deepcopy(w)
        owner=IndependentWorldAuthority(lambda *unused:Attempt('joann','JOIN',target='third_person'))
        with self.assertRaisesRegex(ValueError,'TARGET_MISMATCH'):
            owner.resolve(w,a,Attempt('ann','SING',target='joann'))
        self.assertEqual(w,before)

    def test_invalid_target_body_cannot_be_healed_by_care(self):
        w,a=scene();a['joann']['body']['pain']=float('nan')
        prior=copy.deepcopy(w)
        with self.assertRaisesRegex(ValueError,'INVALID_BODY_STATE'):
            resolve(w,a,Attempt('ann','CARE',target='joann'))
        self.assertEqual(w,prior)

    def test_private_credit_deficit_not_public_world_history(self):
        w,a=scene();w['accounts']['ann']=0.0
        result=resolve(w,a,Attempt('ann','BUY_FOOD'))
        self.assertEqual(result.objective_description,'INSUFFICIENT_CLAIM_ON_FOOD')
        self.assertEqual(w['public_history'][-1]['outcome'],'ATTEMPT_NOT_COMPLETED')
        self.assertNotIn('INSUFFICIENT_CLAIM_ON_FOOD',str(w['cues']))

    def test_sourcefree_no_automatic_song_project(self):
        packet={'actor':{'id':'nadia','location':'home'},'clock':1,'actor_forms':{},'selected_constitution':{'recruited':[]},'experience':{'actor':'nadia','own_action':'SING','status':'PERFORMED','participated':True,'perceived_cues':[{'kind':'song','tags':['sing']}]}}
        response=HeuristicSemanticProvider().propose('development',packet)
        self.assertFalse(any(x.get('kind')=='ADD_PROJECT' for x in response['candidates']))

class ReviewerAdmissionAndLedger(unittest.TestCase):
    def test_varied_malformed_form_scope_refused(self):
        for scope in ({'locations':'home'}, {'counterpart':[]}, {'locations':[None]}, {'locations':{'home'}}, {'counterpart':5}):
            with self.subTest(scope=str(scope)):
                with self.assertRaises(ValueError):validate_tendencies({'id':'form','scope':scope})

    def test_actor_psychic_invalid_batch_atomicity(self):
        a=adult('ann','Ann');before=copy.deepcopy(a)
        ex={'actor':'ann','ref':'ex1','participated':True,'perceived_cues':[{'tags':['care']}],'own_action':'CARE'}
        candidates=[{'kind':'ADD_PROJECT','project':{'object':'care','means':['CARE'],'priority':.7,'cue_terms':['care']}}, {'kind':'ADD_FORM','form':{'kind':'PRACTICE','cues':'home','enables':['CARE']}}]
        with self.assertRaises((ValueError,TypeError)):admit(a,ex,'e1',candidates)
        self.assertEqual(a,before)

    def test_valid_persistent_cue_time_and_expiry(self):
        with tempfile.TemporaryDirectory() as directory:
            rt=ConstitutiveRuntime(str(Path(directory)/'c.sqlite'))
            try:
                rt.initialize()
                row=rt.cue(kind='bell',tags=['bell'],lasting_ticks=3)
                ref=row['cue']['id']
                for _ in range(3):
                    self.assertIn(ref,{x['id'] for x in rt.see('nadia')['cues']})
                    rt.step('nadia',requested_action='WAIT')
                self.assertIn(ref,{x['id'] for x in rt.see('nadia')['cues']})
                rt.step('nadia',requested_action='WAIT')
                self.assertNotIn(ref,{x['id'] for x in rt.see('nadia')['cues']})
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()

    def test_uncommitted_world_state_cannot_be_laundered_by_next_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            path=str(Path(directory)/'check.db');ledger=ResearchLedger(path)
            try:
                w=blank_world();ledger.initialize(w,[adult('ann','Ann')]);wv,world=ledger.world()
                ledger.conn.execute('UPDATE worlds SET body=?',(canonical({**world,'clock':100}),))
                before=ledger.conn.execute('SELECT count(*) FROM events').fetchone()[0]
                with self.assertRaises(Conflict):ledger.commit('w1',wv,world,{}, {},'OBJECTIVE_CUE','ann',{})
                self.assertEqual(before,ledger.conn.execute('SELECT count(*) FROM events').fetchone()[0])
            finally:ledger.close()

    def test_noncanonical_event_envelope_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger=ResearchLedger(str(Path(directory)/'verify.db'))
            try:
                ledger.initialize(blank_world(),[adult('ann','Ann')])
                raw=ledger.conn.execute('SELECT payload FROM events ORDER BY seq LIMIT 1').fetchone()[0]
                ledger.conn.execute('UPDATE events SET payload=?',(' '+raw,))
                with self.assertRaises(AssertionError):ledger.verify_chain()
            finally:ledger.close()

    def test_uncommitted_extra_actor_roster_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger=ResearchLedger(str(Path(directory)/'verify.db'))
            try:
                ledger.initialize(blank_world(),[adult('ann','Ann')])
                ghost=adult('ghost','Ghost')
                ledger.conn.execute('INSERT INTO actors(id,version,body) VALUES(?,?,?)',('ghost',0,canonical(ghost)))
                with self.assertRaises(AssertionError):ledger.verify_chain()
            finally:ledger.close()

if __name__=='__main__':unittest.main()
