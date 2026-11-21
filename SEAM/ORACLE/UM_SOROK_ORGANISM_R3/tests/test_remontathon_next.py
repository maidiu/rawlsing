"""REMONTATHON regression targets: real sourcefree failures, no native owner claims."""
import copy, json, tempfile, unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult, blank_world, Attempt
from um_sorok_organism.development import admit, InvalidDevelopment
from um_sorok_organism.world import resolve
from um_sorok_organism.constitution import actor_access

PACKET={'source_ref':'remont_source_fixture','answers':{'work':'yes'}}

class REMONTATHONBugs(unittest.TestCase):
    def test_p018_source_seal_tamper_is_caught_by_event_chain(self):
        with tempfile.TemporaryDirectory() as folder:
            rt=ConstitutiveRuntime(str(Path(folder)/'life.db'))
            try:
                rt.initialize([('worker','Worker',PACKET)])
                self.assertTrue(rt.verify()['valid'])
                original=rt.ledger.source('fictional_source:worker')
                self.assertIsNotNone(original)
                rt.ledger.conn.execute("UPDATE source_seals SET content=? WHERE id=?",
                    (json.dumps({'answers':{'work':'contrary_forged'}}),'fictional_source:worker'))
                with self.assertRaisesRegex(AssertionError,'SOURCE_SEAL'):
                    rt.verify()
            finally:rt.close()

    def test_p027_development_batch_rejection_is_all_or_nothing(self):
        a=adult('a','A'); initial=copy.deepcopy(a)
        exp={'actor':'a','ref':'lived','participated':True,'status':'PERFORMED','perceived_cues':[]}
        with self.assertRaisesRegex(InvalidDevelopment,'UNSUPPORTED_ACTIVITY_MEANS'):
            admit(a,exp,'objective_1',[
                {'kind':'ADD_PROJECT','project':{'object':'practical care','means':['CARE']}},
                {'kind':'ADD_PROJECT','project':{'object':'impossible physical means','means':['TELEPORT']}}
            ])
        self.assertEqual(a,initial)

    def test_p028_nan_strength_delta_does_not_promote_form(self):
        a=adult('a','A'); a['forms']['f']={'id':'f','kind':'PRACTICE','strength':.4}
        before=copy.deepcopy(a)
        exp={'actor':'a','ref':'lived','participated':True,'status':'PERFORMED','perceived_cues':[]}
        with self.assertRaisesRegex(InvalidDevelopment,'UNBOUNDED_STRENGTH'):
            admit(a,exp,'objective_2',[{'kind':'CHANGE_STRENGTH','form_id':'f','delta':float('nan')}])
        self.assertEqual(a,before)

    def test_p029_buyer_nan_balance_fails_before_world_mutation(self):
        w=blank_world();w['positions']['p']='workshop';w['accounts']['p']=float('nan')
        a={'p':adult('p','P',location='workshop')};before=copy.deepcopy(w)
        with self.assertRaisesRegex(ValueError,'INVALID_BUYER_BALANCE'):
            resolve(w,a,Attempt('p','BUY_FOOD'))
        self.assertEqual(w['sites'],before['sites'])
        self.assertEqual(w['accounts']['p']!=w['accounts']['p'],True)
        self.assertEqual(w['clock'],before['clock'])

    def test_p030_nonfinite_site_stock_cannot_be_consumed_or_produced(self):
        for action in ('REPAIR','WORK'):
            with self.subTest(action=action):
                w=blank_world();w['positions']['p']='home';w['sites']['home']['stock']=float('nan')
                a={'p':adult('p','P',location='home')};before=copy.deepcopy(w)
                with self.assertRaisesRegex(ValueError,'INVALID_SITE_STOCK'):
                    resolve(w,a,Attempt('p',action))
                self.assertEqual(w['clock'],before['clock'])
                self.assertEqual(w['public_history'],before['public_history'])

    def test_p031_failed_purchase_private_money_reason_not_public_cue(self):
        w=blank_world();w['positions']['p']='workshop';w['positions']['witness']='workshop'
        a={'p':adult('p','P',location='workshop'), 'witness':adult('witness','W',location='workshop')}
        r=resolve(w,a,Attempt('p','BUY_FOOD'))
        self.assertEqual(r.status,'BLOCKED')
        self.assertEqual(r.objective_description,'INSUFFICIENT_CLAIM_ON_FOOD')
        see=actor_access(a['witness'],w)
        self.assertTrue(see.cues)
        self.assertNotIn('INSUFFICIENT_CLAIM_ON_FOOD',str(see.cues))

if __name__=='__main__':unittest.main()

class RecruitmentChainRegressions(unittest.TestCase):
    def _make(self,seed=('a',),edge_pairs=()):
        from um_sorok_organism.constitution import materialize,compose,actor_access
        from um_sorok_organism.world import add_cue
        a=adult('test','Test')
        for fid in 'abcdefg':
            a['forms'][fid]={'id':fid,'kind':'PRACTICE','cues':['ping'] if fid in seed else [],
                             'enables':[],'scope':{},'lifecycle':'ACTIVE','strength':.5,
                             'body_min':0,'origin':['fictional:trace']}
        a['links']=[{'source':x,'target':y,'relation':kind} for x,y,kind in edge_pairs]
        w=blank_world();w['positions']['test']='home'
        add_cue(w,'ping',['ping'],location='home')
        return compose(materialize(a,w),actor_access(a,w))

    def test_p012_reverse_order_five_link_recruitment_reaches_fixed_point(self):
        edges=[(x,y,'RECRUITS') for x,y in zip('abcdef','bcdefg')]
        out=self._make(edge_pairs=edges[::-1])
        self.assertIn('g',{f['id'] for f in out.recruited})

    def test_p012_inhibited_direct_seed_cannot_recruit_false_descendant(self):
        edges=[('b','c','RECRUITS'),('a','b','INHIBITS')]
        out=self._make(seed=('a','b'),edge_pairs=edges)
        self.assertNotIn('b',{f['id'] for f in out.recruited})
        self.assertNotIn('c',{f['id'] for f in out.recruited})

class IntegrityAndFormationRegressions(unittest.TestCase):
    def test_p032_chain_rejects_phantom_uncommitted_actor(self):
        from um_sorok_organism.types import canonical
        with tempfile.TemporaryDirectory() as folder:
            rt=ConstitutiveRuntime(str(Path(folder)/'life.db'))
            try:
                rt.initialize([('worker','Worker',PACKET)])
                self.assertTrue(rt.verify()['valid'])
                forged=adult('forged','Forged')
                rt.ledger.conn.execute('INSERT INTO actors VALUES(?,?,?)',
                                       ('forged',0,canonical(forged)))
                with self.assertRaisesRegex(AssertionError,'UNCOMMITTED_ACTOR_SET'):
                    rt.verify()
            finally:rt.close()

    def test_p033_bad_seed_form_strength_refused_before_initializing_actor(self):
        packet={'source_ref':'negative','answers':{'w':'one'},
                'fictional_seed':{'acquired_forms':[{'kind':'PRACTICE','cues':['home'],
                 'enables':['SING'],'strength':'infinite charisma'}]}}
        with tempfile.TemporaryDirectory() as folder:
            rt=ConstitutiveRuntime(str(Path(folder)/'life.db'))
            try:
                with self.assertRaisesRegex(ValueError,'INVALID_ACQUIRED_FORM_PARAMETERS'):
                    rt.initialize([('worker','Worker',packet)])
                self.assertEqual(rt.ledger.events(),[])
            finally:rt.close()

    def test_p034_bad_project_priority_cannot_break_recruitment(self):
        packet={'source_ref':'negative','answers':{'w':'one'},
                'fictional_seed':{'projects':[{'object':'future song',
                 'means':['SING'],'priority':'too high','cue_terms':['home']}]}}
        with tempfile.TemporaryDirectory() as folder:
            rt=ConstitutiveRuntime(str(Path(folder)/'life.db'))
            try:
                with self.assertRaisesRegex(ValueError,'INVALID_ACTIVITY_PRIORITY'):
                    rt.initialize([('worker','Worker',packet)])
                self.assertEqual(rt.ledger.events(),[])
            finally:rt.close()

    def test_p005_underpaid_work_records_unpaid_wage_debt(self):
        w=blank_world();w['positions']['worker']='workshop'
        w['accounts']['workshop_steward']=.1
        actors={'worker':adult('worker','Worker',location='workshop')}
        r=resolve(w,actors,Attempt('worker','WORK'))
        self.assertEqual(r.status,'PERFORMED')
        claim=w['material_claims'][-1]
        self.assertEqual(claim['wage'],.1)
        self.assertAlmostEqual(claim['wage_due'],.25)
        self.assertAlmostEqual(claim['wage_unpaid'],.15)
        self.assertEqual(w['wage_arrears'][-1]['worker'],'worker')
        self.assertAlmostEqual(w['wage_arrears'][-1]['amount'],.15)

    def test_p031_tip_does_not_narrate_private_financial_reason(self):
        with tempfile.TemporaryDirectory() as folder:
            rt=ConstitutiveRuntime(str(Path(folder)/'life.db'))
            try:
                rt.initialize([('worker','Worker',PACKET)])
                rt.step('worker',requested_action='MOVE',object_ref='workshop')
                result=rt.step('worker',requested_action='BUY_FOOD')
                self.assertEqual(result['objective_outcome'],'INSUFFICIENT_CLAIM_ON_FOOD')
                self.assertNotIn('insufficient claim',result['public_tip'].lower())
                self.assertIn('attempt not completed',result['public_tip'].lower())
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()

class FurtherMaterialAndBodyRegressions(unittest.TestCase):
    def test_p029_nonfinite_worker_balance_cannot_poison_wage_payment(self):
        w=blank_world();w['positions']['p']='workshop';w['accounts']['p']=float('nan')
        a={'p':adult('p','P',location='workshop')};stock=w['sites']['workshop']['stock']
        with self.assertRaisesRegex(ValueError,'INVALID_WORKER_BALANCE'):
            resolve(w,a,Attempt('p','WORK'))
        self.assertEqual(w['sites']['workshop']['stock'],stock)
        self.assertEqual(w['material_claims'],[])

    def test_p036_nonfinite_holdings_cannot_poison_food_purchase(self):
        w=blank_world();w['positions']['p']='workshop';w['accounts']['p']=3.0
        w['holdings']={'p':{'food':float('nan')}}
        a={'p':adult('p','P',location='workshop')}
        stock=w['sites']['workshop']['food'];balance=w['accounts']['p']
        with self.assertRaisesRegex(ValueError,'INVALID_OWNED_FOOD'):
            resolve(w,a,Attempt('p','BUY_FOOD'))
        self.assertEqual(w['sites']['workshop']['food'],stock)
        self.assertEqual(w['accounts']['p'],balance)
        self.assertEqual(w['clock'],0)

    def test_p037_nonfinite_body_does_not_get_transformed_into_valid_performed_action(self):
        from um_sorok_organism.organism import eligible
        w=blank_world();w['positions']['p']='workshop'
        a=adult('p','P',location='workshop');a['body']['motor']=float('nan')
        with self.assertRaisesRegex(ValueError,'INVALID_BODY_STATE'):
            eligible(a['body'],'WORK')
        with self.assertRaisesRegex(ValueError,'INVALID_BODY_STATE'):
            resolve(w,{'p':a},Attempt('p','WORK'))
        self.assertEqual(w['sites']['workshop']['stock'],5)
        self.assertEqual(w['clock'],0)

class SourceSealStrictness(unittest.TestCase):
    def test_p018_late_seal_is_chain_anchored_and_cold_reopen_checks_it(self):
        with tempfile.TemporaryDirectory() as folder:
            path=str(Path(folder)/'state.db')
            rt=ConstitutiveRuntime(path)
            try:
                rt.initialize([('worker','W',PACKET)])
                self.assertEqual(rt.verify()['source_seals_verified'],1)
                rt.ledger.seal_source('source:late','EXTERNAL_FIXTURE',{'x':19})
                self.assertEqual(rt.verify()['source_seals_verified'],2)
                self.assertEqual(rt.ledger.events()[-1]['envelope']['kind'],'SOURCE_SEAL')
            finally:rt.close()
            rt=ConstitutiveRuntime(path)
            try:
                self.assertTrue(rt.verify()['valid'])
                rt.ledger.conn.execute("DELETE FROM source_seals WHERE id=?",('source:late',))
                with self.assertRaisesRegex(AssertionError,'SOURCE_SEAL'):
                    rt.verify()
            finally:rt.close()

class ObjectiveLedgerAuthorityRegressions(unittest.TestCase):
    def test_p038_ghost_event_actor_cannot_be_written_as_world_history(self):
        with tempfile.TemporaryDirectory() as folder:
            rt=ConstitutiveRuntime(str(Path(folder)/'life.db'))
            try:
                rt.initialize([('worker','Worker',PACKET)])
                before=len(rt.ledger.events());v,w=rt.ledger.world()
                with self.assertRaisesRegex(Exception,'UNKNOWN_EVENT_ACTOR'):
                    rt.ledger.commit('w1',v,w,{}, {},'ACTOR_LIFE_TRANSITION',
                                     'ghost',{'action':'FAKE_HELP'})
                self.assertEqual(len(rt.ledger.events()),before)
            finally:rt.close()

    def test_p038_ghost_position_cannot_manufacture_copresent_other(self):
        with tempfile.TemporaryDirectory() as folder:
            rt=ConstitutiveRuntime(str(Path(folder)/'life.db'))
            try:
                rt.initialize([('worker','Worker',PACKET)])
                before=len(rt.ledger.events());v,w=rt.ledger.world()
                w['positions']['ghost']='home'
                with self.assertRaisesRegex(Exception,'UNREGISTERED_WORLD_POSITION'):
                    rt.ledger.commit('w1',v,w,{}, {},'OBJECTIVE_CUE',
                                     None,{'kind':'fake_presence'})
                self.assertEqual(len(rt.ledger.events()),before)
            finally:rt.close()

    def test_p039_retrograde_world_clock_cannot_commit(self):
        with tempfile.TemporaryDirectory() as folder:
            rt=ConstitutiveRuntime(str(Path(folder)/'life.db'))
            try:
                rt.initialize([('worker','Worker',PACKET)])
                rt.background(10)
                before=len(rt.ledger.events());v,w=rt.ledger.world()
                w['clock']=1
                with self.assertRaisesRegex(Exception,'WORLD_CLOCK_REGRESSION'):
                    rt.ledger.commit('w1',v,w,{}, {},'OBJECTIVE_CUE',
                                     None,{'kind':'retroactive_false_event'})
                self.assertEqual(len(rt.ledger.events()),before)
            finally:rt.close()

class LedgerAdversarialRoundTwo(unittest.TestCase):
    def test_p040_event_table_headers_cannot_disagree_with_hashed_envelope(self):
        with tempfile.TemporaryDirectory() as folder:
            rt=ConstitutiveRuntime(str(Path(folder)/'state.db'))
            try:
                rt.initialize([('a','A',PACKET)])
                rt.ledger.conn.execute("UPDATE events SET kind='FORGED_LIFE',actor_id='ghost' WHERE seq=1")
                with self.assertRaisesRegex(AssertionError,'EVENT_HEADER_ENVELOPE_MISMATCH'):
                    rt.verify()
            finally:rt.close()

    def test_p018_seal_canonical_bytes_cannot_change_under_same_semantic_digest(self):
        with tempfile.TemporaryDirectory() as folder:
            rt=ConstitutiveRuntime(str(Path(folder)/'state.db'))
            try:
                rt.initialize([('a','A',PACKET)])
                sid='fictional_source:a'
                old=rt.ledger.conn.execute('SELECT content FROM source_seals WHERE id=?',(sid,)).fetchone()[0]
                rt.ledger.conn.execute('UPDATE source_seals SET content=? WHERE id=?',(' '+old+' ',sid))
                with self.assertRaisesRegex(AssertionError,'SOURCE_SEAL_NONCANONICAL_BYTES'):
                    rt.verify()
            finally:rt.close()

    def test_p041_optimized_python_does_not_disable_integrity_assertions(self):
        import subprocess,sys
        with tempfile.TemporaryDirectory() as folder:
            path=str(Path(folder)/'state.db')
            rt=ConstitutiveRuntime(path)
            try:
                rt.initialize([('a','A',PACKET)])
                rt.ledger.conn.execute("UPDATE events SET previous_hash='FORGED' WHERE seq=1")
            finally:rt.close()
            code=('import sys\nfrom um_sorok_organism.runtime import ConstitutiveRuntime\n'
                  'rt=ConstitutiveRuntime(sys.argv[1])\n'
                  'try:\n rt.verify()\nexcept AssertionError:\n sys.exit(0)\n'
                  'sys.exit(1)\n')
            result=subprocess.run([sys.executable,'-O','-c',code,path],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,
                             'Optimized Python incorrectly accepted tampered ancestry: '+result.stderr)

    def test_p039_bool_is_not_an_objective_world_clock(self):
        with tempfile.TemporaryDirectory() as folder:
            rt=ConstitutiveRuntime(str(Path(folder)/'state.db'))
            try:
                rt.initialize([('a','A',PACKET)])
                v,w=rt.ledger.world();w['clock']=True
                with self.assertRaisesRegex(Exception,'WORLD_CLOCK_REGRESSION'):
                    rt.ledger.commit('w1',v,w,{}, {},'OBJECTIVE_CUE',None,{'kind':'bad_bool_clock'})
            finally:rt.close()
