#!/usr/bin/env python3
"""R7 adversarial contract tests. ALL POSITIVES ARE SYNTHETIC; NO EXTERNAL AUTHORITY."""
import copy,hashlib,json,pathlib,sys,tempfile,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import fixtures,r7
HASH='a'*40

class R7Tests(unittest.TestCase):
  def setUp(self):
    self.tmp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.tmp.name)
    self.p,self.m,self.c,self.s=fixtures.make(self.root)
  def tearDown(self):self.tmp.cleanup()
  def cmp(self,p=None,m=None,parent=None):return r7.comparison(p or self.p,m or self.m,parent,self.root)
  def errs(self,p=None,m=None,s=None,parent=None):
    p=p or self.p;m=m or self.m;s=s or self.s
    c=self.cmp(p,m,parent);s['comparison_digest']=r7.digest(c)
    return r7.validate_spine(s,p,m,c,self.root)
  def test_00_positive(self):
    self.assertEqual([],r7.plan_errors(self.p));self.assertEqual('A_ADVANTAGE_AT_COMPLETE_SCOPE',self.c['status'])
    self.assertEqual([],self.errs());self.assertEqual(22,len(self.p['cells']))
  def test_01_original_118(self):
    self.assertEqual([29,26,14,10,8,8,7,16],[len(x) for x in r7.SRC['mandatory'].values()])
    self.assertEqual(118,len(sum(r7.SRC['mandatory'].values(),[])))
  def test_02_floor_sparse_only_build(self):
    p=copy.deepcopy(self.p);p['cells']=[c for c in p['cells'] if c['metric']=='build_wall_s'];p['freeze_digest']=r7.planhash(p)
    self.assertIn('MANDATORY_DIMENSION_GAPS',','.join(r7.plan_errors(p)))
  def test_03_floor_includes_1q_scratch_dense(self):
    req=r7.required_floor('C11_QUERY_DESIGN')
    for x in [('W-S','QUERY','query_1_wall_s'),('W-D','QUERY','query_100_wall_s'),('W-D','STORAGE','scratch_peak_bytes'),('W-J','QUERY','query_100_wall_s')]:self.assertIn(x,req)
  def test_04_ff_future_not_false_C11_gate(self):
    self.assertNotIn('W-U',r7.POL['mandatory_floor_by_scope']['C11_QUERY_DESIGN'])
    self.assertIn('W-U',r7.POL['mandatory_floor_by_scope']['FF_FIRST_EFFECT_DESIGN'])
  def test_05_missing_freeze(self):
    p=copy.deepcopy(self.p);p.pop('freeze_digest');self.assertIn('FREEZE_HASH_MISSING_OR_STALE',r7.plan_errors(p))
  def test_06_after_result_amendment(self):
    p=copy.deepcopy(self.p);p.update(version=2,parent_digest=self.p['freeze_digest'],first_results_seen=True,discovery=self.disc('EXACT_HOLD_PENDING_C'));p['freeze_digest']=r7.planhash(p)
    self.assertIn('POSTRESULT_AMENDMENT_NOT_LAWFUL_IN_PLACE',r7.plan_errors(p,self.p))
  def disc(self,res):return {'origin':'INDEPENDENT_B_PRE_RESULT','B_frozen_objection_sha':'b'*40,
       'source_finding_ref':'ANVIL selected original source and actual downstream first-consumer negative',
       'new_discriminator':'cold dense recursive chosen population across repeated worlds',
       'why_original_frame_incomplete':'actual architecture selection could reverse under this new case',
       'controller_pre_result_freeze_ref':'independent pre-result freeze source-grade receipt',
       'discriminator_id':'B-DISC-001','resolution':res}
  def amend(self,res,added=False):
    p=copy.deepcopy(self.p);p.update(version=2,parent_digest=self.p['freeze_digest'],first_results_seen=False,discovery=self.disc(res))
    if added:
      q=copy.deepcopy(p['cells'][-1]);q.update(id='B-NEW-01',discriminator_id='B-DISC-001',input_sha=r7.digest('unique B cold density stress'))
      p['cells'].append(q);p['discovery']['new_cell_ids']=['B-NEW-01']
    p['freeze_digest']=r7.planhash(p);return p
  def test_07_discovery_without_new_cell(self):
    p=self.amend('MEASURED_ADDED_CELLS');self.assertIn('DISCOVERY_DID_NOT_EXPAND_COMPARISON',r7.plan_errors(p,self.p))
  def test_08_discovery_requires_parent(self):
    p=self.amend('MEASURED_ADDED_CELLS',True)
    self.assertIn('AMENDMENT_PARENT_REQUIRED',r7.plan_errors(p))
  def test_09_discovery_exact_hold_not_winner(self):
    p=self.amend('EXACT_HOLD_PENDING_C');m=copy.deepcopy(self.m);m['freeze_digest']=p['freeze_digest'];c=self.cmp(p,m,self.p)
    self.assertEqual('DISCOVERED_REVERSER_EXACT_HOLD',c['status'])
  def test_10_discovery_missing_measured_cell_rejected(self):
    p=self.amend('MEASURED_ADDED_CELLS',True);m=copy.deepcopy(self.m);m['freeze_digest']=p['freeze_digest']
    self.assertIn('MISSING_FROZEN_CELL_RESULT:B-NEW-01',self.cmp(p,m,self.p)['errors'])
  def test_11_discovery_added_cell_wrong_binding(self):
    p=self.amend('MEASURED_ADDED_CELLS',True);p['cells'][-1]['discriminator_id']='SOME_OTHER';p['freeze_digest']=r7.planhash(p)
    self.assertIn('DISCOVERY_NEW_CELL_NOT_BOUND_TO_DISCOVERY',r7.plan_errors(p,self.p))
  def test_12_missing_raw_measurement(self):
    (self.root/'receipts/A_M00.json').unlink();self.assertIn('MEASUREMENT_RECEIPT_NOT_FOUND',','.join(self.cmp()['errors']))
  def test_13_rehashed_arbitrary_text_receipt(self):
    e=self.m['evidence']['receipt_A_M00'];p=self.root/e['raw_receipt_ref'];p.write_text('arbitrary hello world');e['raw_sha256']=r7.filehash(p)
    self.assertIn('MEASUREMENT_RECEIPT_INVALID_JSON',','.join(self.cmp()['errors']))
  def test_14_rehashed_wrong_candidate(self):
    e=self.m['evidence']['receipt_A_M00'];p=self.root/e['raw_receipt_ref'];d=json.loads(p.read_text());d['candidate']='B';p.write_text(json.dumps(d));e['raw_sha256']=r7.filehash(p)
    self.assertIn('MEASUREMENT_CONTENT_CONTRADICTION:candidate',','.join(self.cmp()['errors']))
  def test_15_rehashed_wrong_metric(self):
    e=self.m['evidence']['receipt_A_M00'];p=self.root/e['raw_receipt_ref'];d=json.loads(p.read_text());d['metric']='build_wall_s_wrong';p.write_text(json.dumps(d));e['raw_sha256']=r7.filehash(p)
    self.assertIn('MEASUREMENT_CONTENT_CONTRADICTION:metric',','.join(self.cmp()['errors']))
  def test_15a_B_disguised_as_A_design_rejected(self):
    e=self.m['evidence']['receipt_B_M00'];p=self.root/e['raw_receipt_ref'];d=json.loads(p.read_text());d['design_frozen_head']=self.p['A0_head'];p.write_text(json.dumps(d));e['raw_sha256']=r7.filehash(p)
    self.assertIn('MEASUREMENT_CONTENT_CONTRADICTION:design_frozen_head',','.join(self.cmp()['errors']))
  def test_15b_bytes_reported_as_seconds_rejected(self):
    cell=next(c for c in self.p['cells'] if c['metric'].endswith('_bytes'))
    e=self.m['evidence']['receipt_A_'+cell['id']];p=self.root/e['raw_receipt_ref'];d=json.loads(p.read_text());d['unit']='SECONDS';p.write_text(json.dumps(d));e['raw_sha256']=r7.filehash(p)
    self.assertIn('MEASUREMENT_CONTENT_CONTRADICTION:unit',','.join(self.cmp()['errors']))
  def test_15c_same_design_heads_rejected(self):
    p=copy.deepcopy(self.p);p['B0_head']=p['A0_head'];p['freeze_digest']=r7.planhash(p)
    self.assertIn('NOT_TWO_DISTINCT_FROZEN_DESIGNS',r7.plan_errors(p))
  def test_16_rehashed_wrong_low(self):
    e=self.m['evidence']['receipt_A_M00'];p=self.root/e['raw_receipt_ref'];d=json.loads(p.read_text());d['low']=999;p.write_text(json.dumps(d));e['raw_sha256']=r7.filehash(p)
    self.assertIn('MEASUREMENT_CONTENT_CONTRADICTION:low',','.join(self.cmp()['errors']))
  def test_17_no_evidence_root_failclosed(self):self.assertEqual('RED',r7.comparison(self.p,self.m)['status'])
  def test_18_non_exec_modeled(self):
    m=copy.deepcopy(self.m);m['results'][0]['B']['status']='MODELED';self.assertEqual('MISSING_MATCHED_DECISIVE_EVIDENCE',self.cmp(m=m)['status'])
  def test_19_opposite_advantage_tradeoff(self):
    m=copy.deepcopy(self.m);v=m['results'][0]
    a,b=v['A'],v['B'];a['low'],a['high'],b['low'],b['high']=3.,3.1,1.,1.1
    for side in ('A','B'):
      e=m['evidence'][v[side]['evidence_id']];p=self.root/e['raw_receipt_ref'];d=json.loads(p.read_text());d['low']=v[side]['low'];d['high']=v[side]['high'];p.write_text(json.dumps(d));e['raw_sha256']=r7.filehash(p)
    self.assertEqual('TRADEOFF_OWNER_DECISION',self.cmp(m=m)['status'])
  def test_20_overlap_blocks_winner(self):
    m=copy.deepcopy(self.m);v=m['results'][0];v['A']['high']=2.05
    e=m['evidence'][v['A']['evidence_id']];p=self.root/e['raw_receipt_ref'];d=json.loads(p.read_text());d['high']=2.05;p.write_text(json.dumps(d));e['raw_sha256']=r7.filehash(p)
    self.assertEqual('PARETO_OR_UNRESOLVED',self.cmp(m=m)['status'])
  def configured_tradeoff(self):
    p=copy.deepcopy(self.p);p['priority_rule']={'frozen_before_results':True,'order':[c['id'] for c in p['cells']],
       'max_acceptable_regression_ratio':{c['id']:4.0 for c in p['cells']},
       'owner_decision_source':'synthetic qualified owner priority written pre-result',
       'B_pre_result_challenge':'B may contest the original choice of objective priority',
       'source_id':'priority rule synthetic first consumer scope governance',
       'first_consumer_cost_basis':'one repeat session and its first actual cold consumer economics'}
    p['freeze_digest']=r7.planhash(p)
    m=copy.deepcopy(self.m);m['freeze_digest']=p['freeze_digest']
    v=m['results'][1];v['A']['low'],v['A']['high'],v['B']['low'],v['B']['high']=3.,3.1,1.,1.1
    for side in ('A','B'):
      e=m['evidence'][v[side]['evidence_id']];f=self.root/e['raw_receipt_ref'];d=json.loads(f.read_text());d['low']=v[side]['low'];d['high']=v[side]['high'];f.write_text(json.dumps(d));e['raw_sha256']=r7.filehash(f)
    return p,m
  def test_20a_owner_predeclared_tradeoff_possible(self):
    p,m=self.configured_tradeoff();self.assertEqual([],r7.plan_errors(p))
    self.assertEqual('A_PRIORITY_WIN_PENDING_INDEPENDENT_C',self.cmp(p,m)['status'])
  def test_20b_tradeoff_without_predeclared_priorities_holds(self):
    p,m=self.configured_tradeoff();p.pop('priority_rule');p['freeze_digest']=r7.planhash(p);m['freeze_digest']=p['freeze_digest']
    self.assertEqual('TRADEOFF_OWNER_DECISION',self.cmp(p,m)['status'])
  def test_20c_tradeoff_loss_bound_blocks(self):
    p,m=self.configured_tradeoff();bad=m['results'][1]['cell_id'];p['priority_rule']['max_acceptable_regression_ratio'][bad]=1.5
    p['freeze_digest']=r7.planhash(p);m['freeze_digest']=p['freeze_digest']
    self.assertEqual('TRADEOFF_EXCEEDS_PREDECLARED_LOSS_BOUNDS',self.cmp(p,m)['status'])
  def test_20d_tradeoff_priority_not_frozen(self):
    p,m=self.configured_tradeoff();p['priority_rule']['frozen_before_results']=False;p['freeze_digest']=r7.planhash(p);m['freeze_digest']=p['freeze_digest']
    self.assertIn('PRIORITY_POSTRESULT_CHANGE',self.cmp(p,m)['errors'])
  def test_21_six_exclusions_no_winner(self):
    p=copy.deepcopy(self.p);p['exclusions']=[{'workload':'W-U','specific_nonmateriality':'future owner has no runnable current Q world scope','first_consumer_consequence':'not needed for immediate C11 operator','B_objection_or_concurrence':'B explicitly questions new world cost','owner':'prospective first consumer science owner','H0_source_ref':'R7 source workshop only','disposition':'CHALLENGED_PENDING_C'}]
    p['freeze_digest']=r7.planhash(p);m=copy.deepcopy(self.m);m['freeze_digest']=p['freeze_digest'];self.assertEqual('SCOPE_EXCLUSIONS_REQUIRE_INDEPENDENT_C',self.cmp(p,m)['status'])
  def test_21a_over_six_gib_receipt_cannot_win(self):
    m=copy.deepcopy(self.m)
    i=next(i for i,x in enumerate(self.p['cells']) if x['metric']=='process_tree_peak_rss_bytes')
    row=m['results'][i]
    for side in ('A','B'):
      v=row[side];v['low']=float(r7.POL['rss_ceiling_bytes']+10000000);v['high']=v['low']+1000
      entry=m['evidence'][v['evidence_id']];f=self.root/entry['raw_receipt_ref'];obj=json.loads(f.read_text());obj['low']=v['low'];obj['high']=v['high']
      f.write_text(json.dumps(obj));entry['raw_sha256']=r7.filehash(f)
    self.assertIn('HARD_RSS_CEILING_VIOLATION',','.join(self.cmp(m=m)['errors']))
  def test_22_missing_veto(self):
    m=copy.deepcopy(self.m);m['veto_receipts'].pop();self.assertIn('VETO_INCOMPLETE_OR_DUPLICATE_CANDIDATE',self.cmp(m=m)['errors'])
  def test_23_false_veto_content(self):
    m=copy.deepcopy(self.m);v=m['veto_receipts'][0];p=self.root/v['path'];d=json.loads(p.read_text());d['status']='HOLD';p.write_text(json.dumps(d));v['sha256']=r7.filehash(p)
    self.assertIn('VETO_NOT_PROVED',','.join(self.cmp(m=m)['errors']))
  def test_23a_one_candidate_veto_false(self):
    m=copy.deepcopy(self.m);v=next(v for v in m['veto_receipts'] if v['candidate']=='B')
    p=self.root/v['path'];d=json.loads(p.read_text());d['status']='HOLD';p.write_text(json.dumps(d));v['sha256']=r7.filehash(p)
    self.assertIn('VETO_NOT_PROVED',','.join(self.cmp(m=m)['errors']))
  def test_24_bad_original_response(self):
    c=fixtures.claim();c['source_status']='OBSERVED_INSTRUMENT_CONSEQUENCE';self.assertIn('NON_SOURCE_TO_ORIGINAL_VALUE',r7.validate_source_claim(c))
    c=fixtures.claim();c.pop('record_value_ref');self.assertIn('SOURCE_VALUE_WITHOUT_SELECTED_RESPONDENT_RECORD',r7.validate_source_claim(c))
  def test_25_invalid_source_status(self):
    c=fixtures.claim();c['source_status']='MODEL_OR_FICTION';self.assertIn('MODEL_OR_FICTION_PROMOTED',r7.validate_source_claim(c))
  def test_26_unobserved_value(self):
    c=fixtures.claim();c['observation']='NOT_OBSERVED';self.assertIn('UNOBSERVED_TO_SUBSTANTIVE_SOURCE_VALUE',r7.validate_source_claim(c))
  def test_27_household_person(self):
    c=fixtures.claim();c['unit']='HOUSEHOLD';self.assertIn('SOURCE_TARGET_UNIT_COLLAPSE',r7.validate_source_claim(c))
  def test_28_interviewer_to_self(self):
    c=fixtures.claim();c['attribution']='INTERVIEWER';self.assertIn('INTERVIEWER_OR_ADMIN_TO_SELF',r7.validate_source_claim(c))
  def test_29_false_semantic_wave(self):
    c=fixtures.claim();c['claim_wave_comparable']=True;c['translation']='UNRECONCILED';self.assertIn('UNLICENSED_WAVE_SEMANTIC_EQUIVALENCE',r7.validate_source_claim(c))
  def test_30_fake_future_route(self):
    s=copy.deepcopy(self.s);s['routes']['WORLD_TO_ACTOR']['edge_ids']=['G0'];self.assertIn('ROUTE_DOMAIN_SPOOF:WORLD_TO_ACTOR',r7.validate_graph(s))
  def test_31_fake_world_consumer_ref(self):
    s=copy.deepcopy(self.s);s['routes']['WORLD_TO_ACTOR']['first_consumer_node_id']='DESCRIPTIVE_MODELED';self.assertIn('ROUTE_CONSUMER_NODE_WRONG:WORLD_TO_ACTOR',r7.validate_graph(s))
  def test_32_shadow_authority(self):
    s=copy.deepcopy(self.s);s['edges'][0]['grade']='UNAUTHORIZED_SOURCE_CERTIFIED';self.assertIn('GRAPH_CONTRADICTORY_SECOND_VOCABULARY:grade',r7.validate_graph(s))
  def test_33_actor_as_original_source(self):
    s=copy.deepcopy(self.s);s['edges'][0]['authority']='ACTOR_OWNER';self.assertIn('GRAPH_FORBIDDEN_TRANSITION:G0',r7.validate_graph(s))
  def test_34_placeholder_handoff(self):
    h=copy.deepcopy(self.s['handoffs'][0]);h['consumer_symbol']='to be specified by future engineer';self.assertIn('READY_BUT_PLACEHOLDER_consumer_symbol',r7.validate_handoff(h))
  def test_35_held_handoff_valid(self):
    h=copy.deepcopy(self.s['handoffs'][0]);h.update(implementation_status='OWNER_HELD',held_reason='source owner has not issued this particular reader',producer_symbol='NONE',consumer_symbol='NONE',source_cut='NONE',first_consumer_grade='OWNER_HELD')
    self.assertEqual([],r7.validate_handoff(h))
  def test_36_second_unrelated_physical_borrow(self):
    s=copy.deepcopy(self.s);d=copy.deepcopy(s['physical_decisions'][0]);d['id']='UNRELATED_SECOND_CHOICE';s['physical_decisions'].append(d)
    self.assertIn('PHYSICAL_BORROWED_UNRELATED_COMPARISON',','.join(self.errs(s=s)))
  def test_36a_wrong_handoff_decision_rejected(self):
    s=copy.deepcopy(self.s);s['handoffs'][0]['decision_id']='SOME_OTHER_PHYSICAL_CHOICE'
    self.assertIn('PHYSICAL_WRONG_HANDOFF_DECISION_OR_DOMAIN',','.join(self.errs(s=s)))
  def test_36b_no_handoff_on_selected_decision(self):
    s=copy.deepcopy(self.s);s['physical_decisions'][0].pop('handoff_id')
    self.assertIn('PHYSICAL_NO_EXACT_FIRST_CONSUMER_HANDOFF',','.join(self.errs(s=s)))
  def test_36c_derived_evidence_fake_parent(self):
    s=copy.deepcopy(self.s);d=copy.deepcopy(s['physical_decisions'][0]);d['id']='NEW-OPT';d['shared_evidence_scope']='DERIVED_WITH_EXPLICIT_DEPENDENCY'
    d['qualified_source_decision_id']='FICTIONAL_NONEXISTENT_PARENT';d['handoff_id']='HANDOFF-P-C11'
    s['physical_decisions'].append(d)
    self.assertIn('PHYSICAL_NONEXISTENT_OR_SELF_REFERENTIAL_EVIDENCE_PARENT',','.join(self.errs(s=s)))
  def test_37_tamper_semantic_witness(self):
    (self.root/'semantic/W-R.json').write_text('{}');self.assertIn('READY_SEMANTIC_RECEIPT_HASH_MISMATCH',','.join(self.errs()))
  def test_38_no_semantic_witness_root(self):
    self.assertIn('READY_SEMANTIC_BYTES_UNAVAILABLE',','.join(r7.validate_spine(self.s,self.p,self.m,self.c)))
  def test_39_orphan_inherited_id(self):
    s=copy.deepcopy(self.s);s['historical_inheritance']['exact_ids'].pop();self.assertIn('118_IDENTITY_CONSERVATION_MISMATCH',self.errs(s=s))
  def test_40_P2_cannot_claim_future_builder(self):
    s=copy.deepcopy(self.s);s['builder_cold_start']='EXECUTED_FIRST_READER_PROOF';self.assertIn('AUTHOR_FABRICATED_FUTURE_BUILDER',self.errs(s=s))
  def test_41_H1_wrong_grade(self):
    h={'schema':'ANVIL_R7_STAGE_1','stage':'H1','verdict':'H1_RECEIVED_SCOPED','source_cut':'source witness reviewed at exact head','owner':'qualified owner',
       'P2_head':HASH,'owner_authority':'VERIFIED_COMPETENT_OWNER','protected_received_YN':'YES','paired_progress_CAS':'AUTHENTICATED_CAS_RECEIVED',
       'CAS_commit_sha':HASH,'CAS_receipt_evidence':'claimed full receiving','architecture_decidable_YN':'YES','commission_complete_YN':'YES',
       'engineering_accepted_YN':'NO','scientific_granted_YN':'NO','source_rights_granted_YN':'NO','actor_granted_YN':'NO',
       'C_receipt':{'builder_grade':'SPURIOUS','future_builder_grade':'EXACT_BUILDER_HOLD','verdict':'C_ACCEPT_SCOPED','head':HASH,'P2_head':HASH}}
    self.assertIn('H1_UNKNOWN_BUILDER_GRADE',r7.check_stage_r7('H1',h,self.root))
  def C(self):
    refs={}
    for key,doc in [('plan',self.p),('measurements',self.m),('spine',self.s),('comparison',self.c)]:
      refs[key]=fixtures.put(self.root,'court/'+key+'.json',doc)
    return {'reviewed_artifacts':refs,'reviewed_plan_digest':self.p['freeze_digest'],
      'reviewed_comparison_digest':r7.digest(self.c),'reviewed_spine_sha256':refs['spine']['sha256'],
      'selected_candidate':'A','reviewed_first_consumer_handoff_id':'HANDOFF-P-C11',
      'schema':'ANVIL_R7_STAGE_1','stage':'C','verdict':'C_ACCEPT_SCOPED',
      'source_cut':'synthetic scope SHA at sourcecut no native claim','owner':'independent C test role - simulated',
      'P2_frozen_head':HASH,'review_head':'c'*40,
      'builder_grade':'SPECIFICATION_CONSTRUCTION_READY','future_builder_grade':'EXACT_BUILDER_HOLD',
      'current_handoff_id':'C11-ABI-TEST','future_handoff_id':'FUTURE-SOROK-ABSTRACT',
      'raw_comparison_verified':True,'semantic_paths_verified':True,'first_consumer_scope_verified':True,
      'strongest_surviving_architecture_objection':{'could_reverse':'NO','why_not_reversing':'Synthetic exhaustive chosen metrics support A in test only, not real science.','refuting_cell_ids':['M00']},
      'adversarial_comparison_scope_review':'synthetic review of physical cost and missing measurement obligations',
      'scientific_source_boundary_review':'synthetic review with original-value illegal claims independently tested',
      'reviewer_role':'DISTINCT_NONAUTHOR'}
  def H1(self,receipt_c=None,receipt_cas=None):
    c=receipt_c if receipt_c is not None else self.C()
    cdata=fixtures.put(self.root,'court/C.json',c)
    cas={'schema':'ANVIL_R7_CAS_READBACK_1','branch':'integration/pre-main-reconciliation-r1',
      'observed_sha':HASH,'expected_parent_sha':'b'*40,'paired_progress_grade':'RECEIVED_PAIRED_MD_JSON',
      'progress_md_sha256':'1'*64,'progress_json_sha256':'2'*64,'receiving_owner':'SYNTHETIC owner cannot grant real CAS',
      'external_readback_ref':'SYNTHETIC no real GitHub CAS readback'}
    if receipt_cas is not None:cas=receipt_cas
    casdata=fixtures.put(self.root,'court/CAS.json',cas)
    return {'schema':'ANVIL_R7_STAGE_1','stage':'H1','verdict':'H1_RECEIVED_SCOPED',
      'source_cut':'synthetic prospective sourcecut no real HQ appointment','owner':'synthetic mock receiving owner',
      'P2_head':HASH,'owner_authority':'VERIFIED_COMPETENT_OWNER','protected_received_YN':'YES',
      'paired_progress_CAS':'AUTHENTICATED_CAS_RECEIVED','CAS_commit_sha':HASH,
      'CAS_receipt_evidence':'synthetic mock not authenticated real evidence',
      'architecture_decidable_YN':'YES','commission_complete_YN':'YES','engineering_accepted_YN':'NO',
      'scientific_granted_YN':'NO','source_rights_granted_YN':'NO','actor_granted_YN':'NO',
      'C_receipt':{'builder_grade':c.get('builder_grade'),'future_builder_grade':c.get('future_builder_grade'),
        'verdict':c.get('verdict'),'head':c.get('review_head'),'P2_head':c.get('P2_frozen_head')},
      'authenticated_C_receipt':cdata,'authenticated_CAS_receipt':casdata,
      'verified_owner_identity_ref':'SYNTHETIC owner authority cannot be attested locally',
      'verified_live_branch_readback':'SYNTHETIC no live external GitHub receipt',
      'independent_C_identity_ref':'SYNTHETIC external issuer identity unverified'}
  def test_42_C_missing_strongest_objection(self):
    c=self.C();c.pop('strongest_surviving_architecture_objection');self.assertIn('C_STRONGEST_OBJECTION_UNRESOLVED',r7.check_stage_r7('C',c,self.root))
  def test_43_C_actual_reverser(self):
    c=self.C();c['strongest_surviving_architecture_objection']['could_reverse']='YES';self.assertIn('C_STRONGEST_OBJECTION_UNRESOLVED',r7.check_stage_r7('C',c,self.root))
  def test_44_C_self_review(self):
    c=self.C();c['reviewer_role']='AUTHOR';self.assertIn('C_SELF_REVIEW',r7.check_stage_r7('C',c,self.root))
  def test_44e_C_must_adjudicate_predeclared_tradeoff(self):
    p,m=self.configured_tradeoff();comp=self.cmp(p,m)
    spine=copy.deepcopy(self.s);spine['freeze_digest']=p['freeze_digest'];spine['comparison_digest']=r7.digest(comp)
    self.assertEqual([],r7.validate_spine(spine,p,m,comp,self.root))
    self.p,self.m,self.c,self.s=p,m,comp,spine
    c=self.C()
    self.assertIn('C_TRADEOFF_NOT_INDEPENDENTLY_ADJUDICATED',r7.check_stage_r7('C',c,self.root))
    c['independent_tradeoff_adjudication']={'disposition':'ACCEPT_OWNER_PREDECLARED_TRADEOFF_AT_SCOPE',
      'all_material_losses_within_frozen_bounds':True,
      'owner_priority_source_ref':'synthetic source of pre-result owner priority court only',
      'B_challenge_substantive_response':'synthetic B challenge answered by materially bounded regression test',
      'why_priority_governs_first_consumer':'synthetic owner objective prioritizes chosen real first-consumer query'}
    self.assertEqual([],r7.check_stage_r7('C',c,self.root))
  def test_44a_C_rehashed_unrelated_comparison_content(self):
    c=self.C();f=self.root/c['reviewed_artifacts']['comparison']['path'];d=json.loads(f.read_text());d['status']='B_ADVANTAGE_AT_COMPLETE_SCOPE'
    f.write_text(json.dumps(d));c['reviewed_artifacts']['comparison']['sha256']=r7.filehash(f)
    self.assertIn('C_RECOMPUTED_COMPARISON_DIFFERS',r7.check_stage_r7('C',c,self.root))
  def test_44b_C_wrong_selected_first_consumer(self):
    c=self.C();c['reviewed_first_consumer_handoff_id']='UNRELATED_FUTURE_CARD'
    self.assertIn('C_UNREVIEWED_REAL_FIRST_CONSUMER',r7.check_stage_r7('C',c,self.root))
  def test_44c_C_wrong_comparison_digest(self):
    c=self.C();c['reviewed_comparison_digest']='0'*64
    self.assertIn('C_REVIEWED_COMPARISON_DIGEST_DISAGREES',r7.check_stage_r7('C',c,self.root))
  def test_44d_C_objection_without_evidence_cells(self):
    c=self.C();c['strongest_surviving_architecture_objection']['refuting_cell_ids']=[]
    self.assertIn('C_NO_FROZEN_EVIDENCE_AGAINST_SURVIVING_OBJECTION',r7.check_stage_r7('C',c,self.root))
  def test_45_H1_local_positive_consistency_only(self):self.assertEqual([],r7.check_stage_r7('H1',self.H1(),self.root))
  def test_46_H1_arbitrary_C_content(self):
    h=self.H1();c=self.root/h['authenticated_C_receipt']['path'];c.write_text('something arbitrary');h['authenticated_C_receipt']['sha256']=r7.filehash(c)
    self.assertIn('H1_C_RECEIPT_INVALID_JSON',r7.check_stage_r7('H1',h,self.root))
  def test_47_H1_C_wrong_verdict_content(self):
    h=self.H1();c=self.root/h['authenticated_C_receipt']['path'];d=json.loads(c.read_text());d['verdict']='C_REVISE_EXACT_DEFECTS';c.write_text(json.dumps(d));h['authenticated_C_receipt']['sha256']=r7.filehash(c)
    self.assertIn('H1_C_CONTENT_DISAGREES_verdict',r7.check_stage_r7('H1',h,self.root))
  def test_48_H1_C_wrong_P2(self):
    h=self.H1();c=self.root/h['authenticated_C_receipt']['path'];d=json.loads(c.read_text());d['P2_frozen_head']='d'*40;c.write_text(json.dumps(d));h['authenticated_C_receipt']['sha256']=r7.filehash(c)
    self.assertIn('H1_C_CONTENT_DISAGREES_P2_head',r7.check_stage_r7('H1',h,self.root))
  def test_49_H1_wrong_CAS_content(self):
    h=self.H1();f=self.root/h['authenticated_CAS_receipt']['path'];d=json.loads(f.read_text());d['observed_sha']='b'*40;f.write_text(json.dumps(d));h['authenticated_CAS_receipt']['sha256']=r7.filehash(f)
    self.assertIn('H1_CAS_SHA_DISAGREES',r7.check_stage_r7('H1',h,self.root))
  def test_50_H1_no_CAS_bytes(self):
    h=self.H1();(self.root/h['authenticated_CAS_receipt']['path']).unlink();self.assertIn('H1_CAS_RECEIPT_NOT_FOUND',r7.check_stage_r7('H1',h,self.root))
  def test_51_H1_false_CAS_progress(self):
    h=self.H1();f=self.root/h['authenticated_CAS_receipt']['path'];d=json.loads(f.read_text());d['paired_progress_grade']='PENDING';f.write_text(json.dumps(d));h['authenticated_CAS_receipt']['sha256']=r7.filehash(f)
    self.assertIn('H1_UNPAIRED_PROGRESS',r7.check_stage_r7('H1',h,self.root))
  def test_52_C_no_future_implemented(self):
    c=self.C();self.assertEqual('EXACT_BUILDER_HOLD',c['future_builder_grade'])
    self.assertEqual([],r7.check_stage_r7('C',c,self.root))
  def conditional(self):
    ident='DELTA-SOURCEFREE-FIRST-CONSUMER-1'
    before={'schema':'ANVIL_R7_EFFECT_RECEIPT_1','effect_digest':'a'*64,
      'first_consumer_symbol':'rawlsing_next/example.py::real_scoped_reader',
      'code_head':HASH,'source_ref':'sourcefree original local first consumer',
      'proof_method':'sourcefree test of absence before lawful scoped repair'}
    after=dict(before,effect_digest='b'*64,proof_method='sourcefree test of newly qualified first consumer after repair')
    bre=fixtures.put(self.root,'delta/before.json',before);are=fixtures.put(self.root,'delta/after.json',after)
    delta={'schema':'ANVIL_R7_PRODUCT_DELTA_1','id':ident,
      'grade':'VERIFIED_NEW_QUALIFIED_INTERFACE','first_consumer_symbol':before['first_consumer_symbol'],
      'before':bre,'after':are,
      'qualified_product_owner':'qualified sourcefree consumer owner to review no rights expansion',
      'requirement_source_ref':'current C11 qualified sourcefree I03 first consumer',
      'causal_change_explanation':'fake test only demonstrates validator catches changed first consumer signature'}
    dref=fixtures.put(self.root,'delta/delta.json',delta)
    c=self.C();c.update(verdict='C_ACCEPT_DOCUMENTARY_HOLD',builder_grade='EXACT_BUILDER_HOLD',
      exact_hold='held original source/rights and unresolved material measured design',
      independent_verified_delta_id=ident,before_evidence_sha256=bre['sha256'],after_evidence_sha256=are['sha256'])
    h=self.H1(receipt_c=c);h.update(verdict='H1_RECEIVED_CONDITIONAL',architecture_decidable_YN='NO',
       exact_hold='held real source and remaining choice-reversing original survey workload',
       product_advance_grade='VERIFIED_NEW_QUALIFIED_INTERFACE',product_delta_evidence_ref=ident,
       authenticated_product_delta=dref)
    return h,delta,c
  def test_52a_conditional_receiving_content_positive_synthetic(self):
    h,d,c=self.conditional();self.assertEqual([],r7.check_stage_r7('H1',h,self.root))
  def test_52b_conditional_missing_delta_file(self):
    h,d,c=self.conditional();(self.root/h['authenticated_product_delta']['path']).unlink()
    self.assertIn('H1_PRODUCT_DELTA_RECEIPT_NOT_FOUND',r7.check_stage_r7('H1',h,self.root))
  def test_52c_conditional_unchanged_before_after(self):
    h,d,c=self.conditional();f=self.root/d['after']['path'];v=json.loads(f.read_text());v['effect_digest']='a'*64;f.write_text(json.dumps(v))
    d['after']['sha256']=r7.filehash(f);t=self.root/h['authenticated_product_delta']['path'];t.write_text(json.dumps(d));h['authenticated_product_delta']['sha256']=r7.filehash(t)
    self.assertIn('H1_PRODUCT_NOT_MATERIALLY_CHANGED',r7.check_stage_r7('H1',h,self.root))
  def test_52d_conditional_C_not_reviewed_delta(self):
    h,d,c=self.conditional();f=self.root/h['authenticated_C_receipt']['path'];v=json.loads(f.read_text());v.pop('independent_verified_delta_id');f.write_text(json.dumps(v));h['authenticated_C_receipt']['sha256']=r7.filehash(f)
    self.assertIn('H1_C_DID_NOT_INDEPENDENTLY_VERIFY_DELTA',r7.check_stage_r7('H1',h,self.root))
  def test_52e_conditional_different_consumer(self):
    h,d,c=self.conditional();f=self.root/d['after']['path'];v=json.loads(f.read_text());v['first_consumer_symbol']='unrelated_new_consumer::different_method';f.write_text(json.dumps(v))
    d['after']['sha256']=r7.filehash(f);t=self.root/h['authenticated_product_delta']['path'];t.write_text(json.dumps(d));h['authenticated_product_delta']['sha256']=r7.filehash(t)
    self.assertIn('H1_PRODUCT_FIRST_CONSUMER_NOT_SAME:after',r7.check_stage_r7('H1',h,self.root))
  def test_53_render_118(self):
    d=self.root/'render';r7.render(self.s,d)
    self.assertEqual(118,len((d/'REQUIREMENT_CONSERVATION.jsonl').read_text().splitlines()))
    ledger=json.loads((d/'RENDER_SHA256.json').read_text());self.assertEqual(r7.filehash(d/'DESIGN_DECISION.md'),ledger['DESIGN_DECISION.md'])
  def test_54_render_tamper(self):
    d=self.root/'render';r7.render(self.s,d);ledger=json.loads((d/'RENDER_SHA256.json').read_text());(d/'DESIGN_DECISION.md').write_text('forged')
    self.assertNotEqual(r7.filehash(d/'DESIGN_DECISION.md'),ledger['DESIGN_DECISION.md'])

if __name__=='__main__':unittest.main(verbosity=2)
