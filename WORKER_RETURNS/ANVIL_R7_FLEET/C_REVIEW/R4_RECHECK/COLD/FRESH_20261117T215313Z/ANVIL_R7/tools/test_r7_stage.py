#!/usr/bin/env python3
"""R7 phase receipt and builder gate regression; synthetic files, not independent review."""
from __future__ import annotations
import copy,hashlib,json,pathlib,tempfile,unittest,subprocess
from test_r7_decision import make_fixture,make_ledger
from r7_decision import compare,digest,sha
from r7_stage import check


def save(root,name,obj):
    b=(json.dumps(obj,sort_keys=True)+'\n').encode();(root/name).write_bytes(b);return {'path':name,'sha256':sha(b)}

class Stages(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.r=pathlib.Path(self.temp.name)
        self.data,self.frozen=make_fixture(self.r)
        self.d=save(self.r,'r7_measurements.json',self.data);self.f=save(self.r,'r7_frozen.json',self.frozen)
        self.p15={'schema':'ANVIL_R7_STAGE','stage':'P15','verdict':'P15_MATCHED_DECISIVE_WITNESS_PROVISIONAL',
            'comparison_input':self.d,'frozen_plan':self.f,'comparison_verdict':'A_DOMINATES_RECEIPT_BOUND_MATERIAL_SET','provisional_winner':'A',
            'frozen_digest':digest(self.frozen),'material_cell_ids':sorted(c['id'] for c in self.frozen['cells']),
            'first_consumer':'SOURCEFREE_I03_FULL_FIRST_READER','independent_science_or_runner_accredited':False}
    def tearDown(self):self.temp.cleanup()
    def test_positive_P15_provisional(self):
        self.assertEqual('PASS_LOCAL_RECEIPT_CONTENT_ONLY_P15_PROVISIONAL',check('P15',self.p15,self.r)['status'])
    def test_P15_cannot_selfcertify_on_fake_receipt(self):
        self.p15['comparison_input']={'path':'madeup.json','sha256':'a'*64}
        self.assertEqual('RED',check('P15',self.p15,self.r)['status'])
    def test_P15_cannot_rename_B_winner(self):
        self.p15['provisional_winner']='B';self.assertEqual('RED',check('P15',self.p15,self.r)['status'])
    def test_P15_cannot_advertise_final_independent_grade(self):
        self.p15['independent_science_or_runner_accredited']=True;self.assertEqual('RED',check('P15',self.p15,self.r)['status'])
    def test_P15_missing_one_measurement(self):
        self.data['measurements'].pop();self.p15['comparison_input']=save(self.r,'r7_measurements_incomplete.json',self.data)
        self.assertEqual('RED',check('P15',self.p15,self.r)['status'])
    def test_C_fake_receipts_rejected(self):
        self.p15_ref=save(self.r,'p15.json',self.p15)
        c={'schema':'ANVIL_R7_STAGE','stage':'C','verdict':'C_ACCEPT_SCOPED','P15_receipt':self.p15_ref,
           'P2_spine':{'path':'nonexistent.json','sha256':'e'*64},'frozen_plan':self.f,'comparison_input':self.d,
           'decision_ledger':{'path':'no_decision.json','sha256':'d'*64},'typed_boundaries':{'path':'fake.json','sha256':'f'*64},
           'reviewer_relationship':'DISTINCT_NONAUTHOR_ASSERTION_PENDING_EXTERNAL_VERIFICATION',
           'strongest_surviving_objection':{'could_change_choice':'NO','reason_and_evidence':'Nothing shown to reverse the choice at this frozen synthetic scope.'},'builder_cards':[]}
        self.assertEqual('RED',check('C',c,self.r)['status'])
    def test_C_fake_builder_symbols_rejected(self):
        from r7_stage import check_builder
        card={'grade':'SPECIFICATION_CONSTRUCTION_READY','producer_symbol':'missing.py::not_real','consumer_symbol':'missing.py::other',
              'source_head':'a'*40,'test_command':'python -m unittest test_fake','first_consumer':'fake first consumer'}
        self.assertIn('R7_BUILDER_NONEXISTENT_producer_symbol',check_builder(card,self.r,self.r))
    def test_C_held_builder_cannot_claim_scoped(self):
        from r7_stage import check_builder
        self.assertEqual([],check_builder({'grade':'EXACT_BUILDER_HOLD','exact_hold':'Real source/first consumer issuer unavailable at this source cut'},None,self.r))
    def test_C_real_existing_python_symbols_static_grade(self):
        from r7_stage import check_builder
        (self.r/'producer.py').write_text('def produce():\n    return 1\n');(self.r/'consumer.py').write_text('def consume():\n    return 2\n')
        subprocess.run(['git','init','-q',str(self.r)],check=True)
        subprocess.run(['git','-C',str(self.r),'add','producer.py','consumer.py'],check=True)
        subprocess.run(['git','-C',str(self.r),'-c','user.name=R7 Synthetic','-c','user.email=fixture@example.invalid','commit','-qm','synthetic code cut'],check=True)
        codehead=subprocess.check_output(['git','-C',str(self.r),'rev-parse','HEAD'],text=True).strip()
        card={'grade':'SPECIFICATION_CONSTRUCTION_READY','producer_symbol':'producer.py::produce','consumer_symbol':'consumer.py::consume',
              'producer_sha256':sha((self.r/'producer.py').read_bytes()),'consumer_sha256':sha((self.r/'consumer.py').read_bytes()),
              'source_head':codehead,'test_command':'python -m unittest tests.test_consumer','first_consumer':'selected sourcefree I03 consumer'}
        self.assertEqual([],check_builder(card,self.r,self.r))
        (self.r/'consumer.py').write_text('def consume():\n    return 99\n')
        card['consumer_sha256']=sha((self.r/'consumer.py').read_bytes())
        self.assertIn('R7_BUILDER_SOURCE_FILE_NOT_AT_PINNED_GIT_HEAD:consumer_symbol',check_builder(card,self.r,self.r))
        (self.r/'consumer.py').write_text('def consume():\n    return 2\n')
        card['consumer_sha256']=sha((self.r/'consumer.py').read_bytes())
        card['source_head']='b'*40
        self.assertIn('R7_BUILDER_SOURCE_HEAD_NOT_THE_CHECKED_OUT_COMMIT',check_builder(card,self.r,self.r))
    def test_H1_selfdeclared_protected_CAS_refused(self):
        p={'schema':'ANVIL_R7_STAGE','stage':'H1','verdict':'H1_RECEIVED_SCOPED',
          'C_receipt':save(self.r,'fake_C.json',{'not_independent':'yes'}),'P2_receipt':save(self.r,'fake_P2.json',{'not_valid':'yes'}),
          'scientific_granted_YN':'NO','source_rights_granted_YN':'NO','actor_granted_YN':'NO'}
        res=check('H1',p,self.r);self.assertEqual('RED',res['status']);self.assertIn('R7_H1_PROTECTED_RECEIVING_REQUIRES_LIVE_AUTHORIZED_EXTERNAL_CAS',res['errors'])
    def test_H1_source_rights_minted(self):
        p={'schema':'ANVIL_R7_STAGE','stage':'H1','verdict':'H1_READY_FOR_EXTERNAL_OWNER_RECEIVING',
          'C_receipt':save(self.r,'fake_C.json',{'no_grants':True}),'P2_receipt':save(self.r,'fake_P2.json',{'no_grants':True}),
          'scientific_granted_YN':'NO','source_rights_granted_YN':'YES','actor_granted_YN':'NO'}
        self.assertEqual('RED',check('H1',p,self.r)['status'])
    def test_positive_C_complete_synthetic_documentary_fixture(self):
        # End-to-end current selection witness with two different comparisons:
        # R6 inherited full-SPINE source semantics and R7 typed receipt vetoes.
        # The result must remain explicitly local; no independent C grant.
        from test_r6 import r6_fixture,numeric_fixture
        from r6_comparator import digest as r6_digest
        from test_r7_decision import make_ledger
        from test_r7_typed import fixture as typed_fixture
        from r7_decision import sha
        p2=r6_fixture();p2['outcome']='DESIGN_READY_SCOPED'
        p2['decisions'][1]['alternatives'][1]['status']='ELIMINATED'
        for d in p2['decisions']:
            for z in d['discriminators']:z['status']='RESOLVED'
            if d['class'] in ('PHYSICAL','PRESERVE'):
                d['invariants']={k:'PASS_AT_SCOPE' for k in d['invariants']}
        r6data,r6frozen=numeric_fixture()
        for measurement in r6data['measurements']:
            for side in ('A','B'):
                payload=json.dumps({'synthetic':True,'side':side,'cell':measurement['cell_id']}).encode()
                (self.r/measurement[side]['receipt_path']).write_bytes(payload)
                measurement[side]['receipt_sha256']=sha(payload)
        for v in r6data['hard_veto_checks']:
            v['receipt_path']='veto_r6_'+v['id']
            payload=json.dumps({'synthetic':True,'veto':v['id']}).encode()
            (self.r/v['receipt_path']).write_bytes(payload);v['receipt_sha256']=sha(payload)
        r6d=save(self.r,'r6_data.json',r6data);r6f=save(self.r,'r6_frozen.json',r6frozen)
        p2['comparison_receipt']={'input_path':r6d['path'],'input_sha256':r6d['sha256'],'frozen_path':r6f['path'],
            'frozen_sha256':r6f['sha256'],'declared_verdict':'A_DOMINATES_FULL_MATERIAL_DIMENSIONS',
            'declared_winner':'A','physical_decision_id':'DK-PHYSICAL'}
        p2['physical_decision_evidence']=[{'decision_id':'DK-PHYSICAL','selected_alternative_id':'A-P',
            'selected_candidate':'A','material_cell_ids':[c['id'] for c in r6frozen['cells']],
            'first_consumer_effect':'Actual sourcefree first receiver of the joined I03 fact is changed by this choice',
            'joint_cost_or_dependency_explanation':'The current C11 cold reader and prepared index costs are a coupled dependency',
            'source_integrity_veto_receipt':'Synthetic sourcefree only, no real issuer grant or native scientific permission'}]
        self.p15_ref=save(self.r,'p15.json',self.p15)
        p2ref=save(self.r,'p2.json',p2)
        typed=typed_fixture();typed['R5_R6_spine_sha256']=hashlib.sha256(json.dumps(p2,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
        typedref=save(self.r,'typed.json',typed)
        ledgerref=save(self.r,'r7_ledger.json',make_ledger(self.frozen))
        (self.r/'producer.py').write_text('def produce():\n    return 1\n')
        (self.r/'consumer.py').write_text('def consume():\n    return 2\n')
        subprocess.run(['git','init','-q',str(self.r)],check=True)
        subprocess.run(['git','-C',str(self.r),'add','producer.py','consumer.py'],check=True)
        subprocess.run(['git','-C',str(self.r),'-c','user.name=R7 Synthetic','-c','user.email=fixture@example.invalid','commit','-qm','synthetic source-head'],check=True)
        checked_head=subprocess.check_output(['git','-C',str(self.r),'rev-parse','HEAD'],text=True).strip()
        card={'id':'current','domain':'CURRENT_FIRST_CONSUMER','grade':'SPECIFICATION_CONSTRUCTION_READY',
              'producer_symbol':'producer.py::produce','consumer_symbol':'consumer.py::consume',
              'producer_sha256':sha((self.r/'producer.py').read_bytes()),
              'consumer_sha256':sha((self.r/'consumer.py').read_bytes()),
              'source_head':checked_head,'candidate_code_head':self.frozen['candidate_code_heads']['A'],
              'test_command':'python -m unittest tests.test_consumer','first_consumer':'sourcefree I03 integrated first consumer'}
        bridge={'schema':'ANVIL_R7_FIRST_CONSUMER_ABI_BRIDGE','candidate_code_head':self.frozen['candidate_code_heads']['A'],
            'builder_source_head':checked_head,'first_consumer':card['first_consumer'],
            'input_abi':'Sealed full C11 signed sourcefree normalized input to first existing query producer',
            'output_abi':'Typed query output with respondent negative and restore witness receipt',
            'negative_restore_test':'Wrong source/current denies then restoring exact root permits matching replay'}
        card['first_consumer_compatibility_receipt']=save(self.r,'builder_bridge.json',bridge)
        future={'id':'future','domain':'FUTURE_NONPRECLUSION','grade':'EXACT_BUILDER_HOLD',
                'exact_hold':'Future SOROK actor science remains owner-held; sourcefree extension path only'}
        packet={'schema':'ANVIL_R7_STAGE','stage':'C','verdict':'C_ACCEPT_SCOPED',
            'P15_receipt':self.p15_ref,'P2_spine':p2ref,'frozen_plan':self.f,'comparison_input':self.d,
            'decision_ledger':ledgerref,'typed_boundaries':typedref,
            'selected_candidate':'A','builder_cards':[card,future],
            'reviewer_relationship':'DISTINCT_NONAUTHOR_ASSERTION_PENDING_EXTERNAL_VERIFICATION',
            'strongest_surviving_objection':{'could_change_choice':'NO',
            'reason_and_evidence':'Within this entirely synthetic matched fixture neither alternative has a remaining quantified reversal.'}}
        result=check('C',packet,self.r,source_root=self.r)
        self.assertEqual('PASS_LOCAL_STRUCTURE_AND_RECEIPT_CONTENT_ONLY_C_PENDING_INDEPENDENT_REVIEW',result['status'],result)
        bad=copy.deepcopy(packet);bad['builder_cards'][0]['candidate_code_head']='b'*40
        self.assertIn('R7_C_BUILDER_NOT_BOUND_TO_SELECTED_CANDIDATE_HEAD',check('C',bad,self.r,source_root=self.r)['errors'])
        bad=copy.deepcopy(packet);bad['builder_cards'][0].pop('first_consumer_compatibility_receipt')
        self.assertEqual('RED',check('C',bad,self.r,source_root=self.r)['status'])
if __name__=='__main__':unittest.main(verbosity=2)
