#!/usr/bin/env python3
"""Targeted oldMac+mainMac R7 correction mutation tests; all synthetic and unauthenticated."""
import copy,hashlib,json,pathlib,subprocess,tempfile,unittest
from test_r7_decision import make_fixture, replace_receipt
from r7_decision import compare,digest,sha,ROOT,POL,floor_for
from r7_analytical_elimination import check as check_elimination

class R7Synthesis(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.tmp.name)
        self.data,self.frozen=make_fixture(self.root)
    def tearDown(self):self.tmp.cleanup()
    def result(self):return compare(self.data,self.frozen,self.root)
    def freeze(self):self.data['frozen_sha256']=digest(self.frozen)
    def add_owner_rule(self,bound=3.0):
        order=[x['id'] for x in self.frozen['cells']]
        rule={'frozen_before_results':True,'results_already_seen':False,
            'independent_C_adjudication_pending':True,
            'order':order,'max_acceptable_regression_ratio':{x:bound for x in order},
            'owner_decision_source':'Pinned synthetic owner court source; requires independent live external authentication',
            'owner_source_sha256':'f'*64,
            'B_pre_result_challenge':'Candidate B presented all frozen cells and material source and query obligations for review',
            'first_consumer_cost_basis':'Actual sourcefree I03 1/10/100 distinct operations, dense and weighted first reader',
            'source_cut':self.frozen['source_cut'],'scope':self.frozen['scope']}
        receipt={key:rule[key] for key in ('order','max_acceptable_regression_ratio','owner_decision_source',
                    'owner_source_sha256','B_pre_result_challenge','first_consumer_cost_basis','source_cut','scope')}
        receipt.update(schema='ANVIL_R7_OWNER_PRIORITY_RECEIPT',frozen_before_results=True,
                       authority_grade='OWNER_ASSERTED_PENDING_EXTERNAL_AUTHENTICATION')
        blob=(json.dumps(receipt,sort_keys=True)+'\n').encode();(self.root/'owner_priority.json').write_bytes(blob)
        rule['owner_priority_receipt']={'path':'owner_priority.json','sha256':sha(blob)}
        self.frozen['priority_rule']=rule;self.freeze()
    def choose_B_one_cell(self,value=6):
        i=next(i for i,m in enumerate(self.data['measurements']) if m['cell_id'].endswith('query_100_wall_s'))
        replace_receipt(self.root,self.data,i,'B',{'low':value-1,'value':value,'high':value+1})
    def test_current_C11_scope_no_world_performance(self):
        self.assertNotIn(('W-U','cross_world_100_wall_s'),floor_for('C11_QUERY_DESIGN'))
        self.assertEqual('A_DOMINATES_RECEIPT_BOUND_MATERIAL_SET',self.result()['status'])
    def test_field_forge_scope_requires_real_world_metric(self):
        self.frozen['scope']='FF_FIRST_EFFECT_DESIGN';self.freeze()
        r=self.result();self.assertEqual('RED',r['status'])
        self.assertTrue(any('W-U' in x for x in r['errors']))
    def test_dense_query_cannot_be_dropped_even_if_build_good(self):
        self.assertIn(('W-D','query_100_wall_s'),floor_for('C11_QUERY_DESIGN'))
        for v in (self.frozen['cells'],self.data['measurements']):
            v[:]=[c for c in v if c.get('id',c.get('cell_id'))!='W-D__query_100_wall_s']
        self.freeze();self.assertEqual('RED',self.result()['status'])
    def test_sparse_wide_instrument_cannot_substitute_dense_events(self):
        # W-D with 100k people, 600 opportunities, but only 3.2 events/person is sparse.
        i=next(i for i,m in enumerate(self.data['measurements']) if m['cell_id']=='W-D__query_100_wall_s')
        replace_receipt(self.root,self.data,i,'A',{'event_count':320000})
        self.assertEqual('RED',self.result()['status'])
    def test_sparse_instrument_must_still_be_wide(self):
        i=next(i for i,m in enumerate(self.data['measurements']) if m['cell_id']=='W-S__query_100_wall_s')
        replace_receipt(self.root,self.data,i,'A',{'source_width':3})
        self.assertEqual('RED',self.result()['status'])
    def test_single_mixed_tradeoff_is_not_automatic_winner(self):
        self.choose_B_one_cell()
        self.assertEqual(('MATERIAL_TRADEOFF_OWNER_PRIORITY_NOT_FROZEN',None),
                         (self.result()['status'],self.result()['winner']))
    def test_owner_priority_is_provisional_not_authenticated(self):
        self.choose_B_one_cell();self.add_owner_rule(3.0)
        r=self.result();self.assertEqual('A_PRIORITY_WIN_PENDING_INDEPENDENT_C',r['status'],r)
        self.assertEqual('A',r['winner']);self.assertIn('NOT_COMPETENT_OWNER_SELECTION',r['reviewer_grade'])
    def test_regression_exceeds_frozen_bound(self):
        self.choose_B_one_cell(value=2);self.add_owner_rule(1.1)
        r=self.result();self.assertEqual(('TRADEOFF_EXCEEDS_FROZEN_REGRESSION_LIMITS',None),(r['status'],r['winner']))
        self.assertTrue(r['excessive_cells'])
    def test_owner_receipt_byte_tampering_refused(self):
        self.choose_B_one_cell();self.add_owner_rule()
        (self.root/'owner_priority.json').write_text('{}')
        self.assertEqual('RED',self.result()['status'])
    def test_owner_receipt_semantic_mismatch_refused(self):
        self.choose_B_one_cell();self.add_owner_rule()
        path=self.root/'owner_priority.json';r=json.loads(path.read_text());r['order'].reverse()
        b=(json.dumps(r,sort_keys=True)+'\n').encode();path.write_bytes(b)
        self.frozen['priority_rule']['owner_priority_receipt']['sha256']=sha(b);self.freeze()
        v=self.result();self.assertEqual('RED',v['status'])
        self.assertTrue(any('R7_PRIORITY_RECEIPT_CONTENT_DRIFT' in x for x in v['errors']))
    def test_post_result_priority_and_false_owner_disallowed(self):
        self.choose_B_one_cell();self.add_owner_rule()
        self.frozen['priority_rule']['results_already_seen']=True;self.freeze()
        self.assertEqual('RED',self.result()['status'])
        self.frozen['priority_rule']['results_already_seen']=False
        self.frozen['priority_rule']['independent_C_adjudication_pending']=False;self.freeze()
        self.assertEqual('RED',self.result()['status'])
    def test_extra_future_world_metric_not_silent_C11_floor(self):
        self.frozen['cells'][0]['workload_case_id']='W-U';self.freeze()
        self.assertEqual('RED',self.result()['status'])
    def test_priority_no_unmatched_rival_and_no_metric_elision(self):
        self.choose_B_one_cell();self.add_owner_rule()
        self.data['measurements'][0]['B']['status']='UNRUN_HELD'
        self.assertEqual('RED',self.result()['status'])
    def _analytical_proof(self):
        repo=self.root/'code';repo.mkdir();(repo/'candidate.py').write_text('def incompatible_consumer_contract():\n    return "no source role available for exact respondent response"\n')
        subprocess.run(['git','init','-q',str(repo)],check=True)
        subprocess.run(['git','-C',str(repo),'add','candidate.py'],check=True)
        subprocess.run(['git','-C',str(repo),'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixed candidate'],check=True)
        head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
        self.frozen['candidate_code_heads']['B']=head;self.freeze()
        contract=self.root/'contract.txt';contract.write_text('Exact source role and respondent response semantics must be provided for all selected first-consumer operations.\n')
        proof={'schema':'ANVIL_R7_ANALYTICAL_ELIMINATION','frozen_sha256':digest(self.frozen),
               'source_cut':self.frozen['source_cut'],'scope':self.frozen['scope'],
               'candidate_code_head':head,'eliminated_candidate':'B','proof_type':'CONTRACT_CONTRADICTION',
               'necessary_capability':'Actual current respondent and role integrity must remain available to the first native I03 receiver',
               'unavoidable_contradiction':'This frozen candidate binds an event without the respondent source role required by the frozen consumer',
               'first_consumer_effect':'The exact first consumer would be unable to distinguish respondents or validate role-specific survey events',
               'source_semantic_negative_or_restoration':'A forged source selector must refuse and restored canonical respondent identity must replay identically',
               'strongest_surviving_reverser':'A compatible producer providing the exact required respondent-role mapping would disprove the elimination',
               'how_an_independent_reviewer_can_disprove':'Inspect the committed candidate code and supply the missing exact respondent-role mapping to the specified first consumer',
               'requires_competitor_implementation':False,'proposes_unconditional_winner':False,
               'premises':[{'kind':'FROZEN_CONTRACT','path':'contract.txt','sha256':sha(contract.read_bytes()),
                            'exact_excerpt':'Exact source role and respondent response semantics must be provided for all selected first-consumer operations.'},
                           {'kind':'CANDIDATE_CODE','path':'candidate.py','sha256':sha((repo/'candidate.py').read_bytes()),
                            'exact_excerpt':'    return "no source role available for exact respondent response"'}]}
        return proof,repo
    def test_analytical_exact_evidence_no_competitor_build_required(self):
        p,src=self._analytical_proof();r=check_elimination(p,self.frozen,self.root,src)
        self.assertEqual('PROVISIONAL_ANALYTICAL_ELIMINATION__C_MUST_AUTHENTICATE_AND_ADJUDICATE',r['status'],r)
        self.assertIsNone(r['winner'])
    def test_analytical_fake_premise_or_head_cannot_win(self):
        p,src=self._analytical_proof();p['premises'][0]['exact_excerpt']='Imaginary binding contract never present'
        self.assertEqual('RED',check_elimination(p,self.frozen,self.root,src)['status'])
        p['premises'][0]['exact_excerpt']='Exact source role and respondent response semantics must be provided for all selected first-consumer operations.'
        p['proposes_unconditional_winner']=True
        self.assertEqual('RED',check_elimination(p,self.frozen,self.root,src)['status'])
        p['proposes_unconditional_winner']=False;p['candidate_code_head']='a'*40
        self.assertEqual('RED',check_elimination(p,self.frozen,self.root,src)['status'])
    def test_analytical_stage_accepts_evidence_only_never_a_winner(self):
        from r7_stage import check as check_stage
        p,src=self._analytical_proof()
        a=(json.dumps(self.frozen,sort_keys=True)+'\n').encode()
        b=(json.dumps(p,sort_keys=True)+'\n').encode()
        (self.root/'freeze.json').write_bytes(a);(self.root/'proof.json').write_bytes(b)
        packet={'schema':'ANVIL_R7_STAGE','stage':'ANALYTICAL','verdict':'ANALYTICAL_PROOF_SUBMITTED_FOR_C',
                'frozen_plan':{'path':'freeze.json','sha256':sha(a)},
                'analytical_proof':{'path':'proof.json','sha256':sha(b)}}
        result=check_stage('ANALYTICAL',packet,self.root,source_root=src)
        self.assertEqual('PASS_LOCAL_ANALYTICAL_EVIDENCE_ONLY__C_AND_OWNER_PENDING',result['status'],result)
        packet['verdict']='ANALYTICALLY_APPROVED_WINNER'
        self.assertEqual('RED',check_stage('ANALYTICAL',packet,self.root,source_root=src)['status'])
    def test_priority_C_requires_actual_review_and_reverser(self):
        from r7_stage import check_priority_C
        self.choose_B_one_cell();self.add_owner_rule()
        result=self.result();self.assertEqual('A_PRIORITY_WIN_PENDING_INDEPENDENT_C',result['status'])
        missing=check_priority_C({},result,self.frozen)
        self.assertIn('R7_C_PRIORITY_WIN_WITHOUT_CHALLENGED_PRIORITY_REVIEW',missing)
        good={'priority_adjudication':{
            'priority_source_sha256':'f'*64,'selected_candidate':'A','independent_external_review_pending':True,
            'first_consumer_priority_justification':'The owner gives the exact first consumer practical query costs priority over construction time in the frozen scope.',
            'B_strongest_concrete_objection':'B is demonstrably cheaper on a dense query and a rigorous challenger must test whether the better query cost would reverse the selection.',
            'why_every_regression_is_acceptable':'Every measured sacrifice is bounded by the actual frozen per-cell ratio and checked using conservative interval extremes.',
            'what_would_reverse_selection':'A materially different B code or workload that violates the frozen per-cell loss ratio would reopen the substantive comparison.'}}
        self.assertEqual([],check_priority_C(good,result,self.frozen))
        good['priority_adjudication']['priority_source_sha256']='e'*64
        self.assertIn('R7_C_PRIORITY_NOT_BOUND_TO_OWNER_SOURCE',check_priority_C(good,result,self.frozen))
    def test_analytical_missing_rival_not_evidence(self):
        p,src=self._analytical_proof();p['unavoidable_contradiction']='Competitor has not been built'
        self.assertEqual('RED',check_elimination(p,self.frozen,self.root,src)['status'])

if __name__=='__main__':unittest.main(verbosity=2)
