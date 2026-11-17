#!/usr/bin/env python3
"""Adversarial ANVIL R6 structural suite. ALL DATA SYNTHETIC. NO SOURCE/ENGINEERING ACCREDITATION."""
import copy,json,os,pathlib,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import r6

HASH='a'*40

def sample_claim():
    return {'release':'sourcefree-rel-1','instrument':'synthetic instrument V1','country':'fictional test country','wave':'R1 test wave','question':'Q1 original test option',
            'source_ref':'sourcefree questionnaire receipt','evidence_ref':'test-fixture-not-native','source_unit':'PERSON','target_unit':'PERSON',
            'asked':'YES','released':'YES','observation':'VALUE','eligibility':'ELIGIBLE','unit':'PERSON','attribution':'SELF','target_attribution':'SELF',
            'source_status':'DOCUMENTED_RESPONDENT_RESPONSE','translation':'SAME_INSTRUMENT',
            'original_code_ref':'sourcefree-original-option-1','record_value_ref':'sourcefree-respondent-row-44-value','claim_kind':'RESPONDENT_ORIGINAL_VALUE','target_is_respondent_claim':True}

def sample_meta():
    c=sample_claim();c.update({'claim_kind':'INSTRUMENT_METADATA','source_status':'DOCUMENTED_DESIGN', 'asked':'NO','released':'NO','observation':'NOT_OBSERVED',
      'eligibility':'UNKNOWN_HELD','target_is_respondent_claim':False,'attribution':'NOT_APPLICABLE','target_attribution':'NOT_APPLICABLE'})
    return c

def evidence_entry(grade='S2_SOURCEFREE_EXECUTED'):
    return {'grade':grade,'description':'synthetic only NO real execution','source_ref':'synthetic-sourcefree-fixture-reference',
      'raw_receipt_ref':'synthetic-untrusted-receipt-for-unit-test','code_head':HASH,'independent_checked':True}

def gen_plan():
    cells=[]
    for i,(w,d,m) in enumerate(r6.POL['minimal_design_wide_matrix']):
        cells.append({'id':f'M{i:02}','workload':w,'dimension':d,'metric':m,'decision_id':'P-C11',
          'selection_reverser_A':'If A is worse here, B could win the architecture',
          'selection_reverser_B':'If B is worse here, A could win the architecture',
          'input_sha':r6.digest(['test-fixture',w,d,m]),'runner_identity':'SYNTHETIC_RUNNER_SIMULATED_ONLY',
          'negative_restore':'fictional denied then exact restored fixture','first_consumer':'sourcefree direct cold I03 and F4 test first consumer',
          'source_grade':'S2_SOURCEFREE_EXECUTED'})
    plan={'schema':'ANVIL_R6_PLAN_1','scope':'C11_QUERY_DESIGN','version':1,'parent_digest':None,'phase':'BEFORE_FIRST_RESULT',
          'policy_digest':r6.filehash(ROOT/'contracts/policy.json'),'A0_head':HASH,'B0_head':'b'*40,'first_results_seen':False,'cells':cells,'exclusions':[]}
    plan['freeze_digest']=r6.planhash(plan)
    return plan

def gen_measure(plan):
    evidence={};rows=[]
    for i,c in enumerate(plan['cells']):
        ea='evidence_A_'+c['id']; eb='evidence_B_'+c['id'];evidence[ea]=evidence_entry();evidence[eb]=evidence_entry()
        rows.append({'cell_id':c['id'],'fixture_hash':c['input_sha'],'runner_identity':c['runner_identity'],
            'A':{'status':'MEASURED','low':1.0,'high':1.1,'evidence_id':ea},
            'B':{'status':'MEASURED','low':2.0,'high':2.1,'evidence_id':eb}})
    return {'schema':'ANVIL_R6_MEASUREMENTS_1','freeze_digest':plan['freeze_digest'],'results':rows,'evidence':evidence}

def gen_graph():
    ns=[{'id':'OBS','domain':'OBSERVED'},{'id':'DES','domain':'DESCRIPTIVE_MODELED'}, {'id':'EXT','domain':'EXTERNAL_OBSERVED'},
        {'id':'STR','domain':'STRUCTURAL_QUALIFIED'}, {'id':'WORLD','domain':'FICTIONAL_WORLD'}, {'id':'ACT','domain':'ACTOR_STATE'},
        {'id':'HIST','domain':'HISTORY_EVENT'}]
    specs=[('e1','OBS','DES','DESCRIPTIVE_INFERENCE','SCIENCE_GRADED'),
           ('e2','EXT','STR','INDEPENDENT_STRUCTURAL_ISSUANCE','EXTERNAL_STRUCTURAL_ISSUER'),
           ('e3','STR','WORLD','WORLD_OPPORTUNITY','WORLD_PARTICULARIZER'),
           ('e4','WORLD','ACT','ACTOR_ACCESS_OR_LEARNING','ACTOR_OWNER'),
           ('e5','ACT','HIST','PERFORMED_ACT','ACTOR_OWNER'),
           ('e6','WORLD','HIST','EXOGENOUS_WORLD_EVENT','WORLD_OWNER')]
    edges=[{'id':id,'from':f,'to':t,'transition':trans,'authority':a,'clock':'qualified source/fiction history time boundary',
           'payload':'qualified source and sourcefree semantic payload','negative':'held unsupported access must refuse','owner':'competent owner independently authenticated',
           'evidence_ref':'test-only hypothetical source fixture'} for id,f,t,trans,a in specs]
    ids={'OBSERVED_TO_DESCRIPTIVE':['e1'],'EXTERNAL_TO_STRUCTURAL_WORLD':['e2','e3'],
        'WORLD_TO_ACTOR':['e4'],'ACTOR_TO_HISTORY':['e5'],'EXOGENOUS_TO_HISTORY':['e6']}
    routes={id:{'edge_ids':edges,'first_consumer':'qualified first consumer or prospective lawfully held owner',
                 'source_or_world_clock':'historical source and fictional actor times separate',
                 'preserved_information':'original source identity typed provenance and negatives',
                 'legitimate_owner':'independently competent separate producer and receiver owners',
                 'negative_or_hold':'actor/source permissions held where not executed',
                 'proof_grade':'OWNER_HELD_WITH_FEASIBLE_EXTENSION',
                 'extension_abi':'versioned proposed external owner interface and frozen payload'} for id,edges in ids.items()}
    return ns,edges,routes

def gen_spine(plan,measure):
    comparison=r6.comparison(plan,measure)
    ns,edges,routes=gen_graph();ev={'e0':evidence_entry('S1_SOURCE_STATIC'), 'e1':evidence_entry(), 'e2':evidence_entry()}
    handoff={'id':'HANDOFF-1','implementation_status':'READY_FOR_IMPLEMENTER','owner':'qualified technical owner after source-authority check',
      'input_abi':'signed sealed C11 selected exact sourcefree I03 API','output_abi':'typed empirical fact including negative and result replay',
      'negative':'severed source release must return typed denied result','currentness':'authorized CURRENT release recertification on use',
      'rights_grade':'sourcefree scope only; no real survey permission','first_effect':'changed actual selected query returns changed first fact',
      'dependency':'source writer and cold estate are verified before native I03','test_command':'python -m pytest tests/test_native_i03_real.py -q',
      'first_consumer':'rawlsing_next native I03 direct first reader under scoped owner',
      'producer_symbol':'rawlsing_next/pre553_direct_estate_i03.py::DirectEstateI03Session',
      'consumer_symbol':'rawlsing_next/pre553_empirical_query.py::execute_empirical_query',
      'source_cut':HASH,'first_consumer_grade':'EXACT_STATIC_IMPLEMENTATION_ABI'}
    return {'schema':'ANVIL_R6_SPINE_1','policy_digest':r6.filehash(ROOT/'contracts/policy.json'),
      'source_registry_digest':r6.filehash(ROOT/'contracts/source_registry.json'),
      'freeze_digest':plan['freeze_digest'],'comparison_digest':r6.digest(comparison), 'scope':plan['scope'],
      'author_proposed_grade':'DESIGN_READY_SCOPED','builder_cold_start':'PENDING_INDEPENDENT_C','selected_candidate':'A',
      'historical_inheritance':{'families':29,'K3_not_adopted_count':26,'P4R_held_count':14,'exact_ids':sum(r6.SRC['mandatory'].values(),[])},
      'claims':[sample_meta(),sample_claim()],'nodes':ns,'edges':edges,'routes':routes,'evidence':ev,
      'physical_decisions':[{'id':'P-C11','selected':'A','cell_ids':[x['id'] for x in plan['cells']],
        'actual_first_consumer':'actual scoped sourcefree cold I03 first reader','first_consumer_node_id':'DES',
        'dependency_effect':'all physical choices reuse the same selected sourcefree direct estate and query path',
        'shared_evidence_scope':'DIRECTLY_MEASURED','hard_veto_evidence_ids':['e0']}],
      'handoffs':[handoff], 'semantic_witnesses':{'W-R':'e1','W-J':'e1','W-X':'e1'},
      'product_deltas':[{'grade':'NO_NEW_PRODUCT_ADVANCE','before_evidence':'e0','after_evidence':'e1',
        'changed_first_consumer_effect':'synthetic fixture only; does not establish actual progress'}]}

class R6Adversarial(unittest.TestCase):
  def setUp(self):
    self.p=gen_plan();self.m=gen_measure(self.p);self.c=r6.comparison(self.p,self.m);self.s=gen_spine(self.p,self.m)
  def test_source_inventory_exact(self):
    self.assertEqual([len(v) for v in r6.SRC['mandatory'].values()],[29,26,14,10,8,8,7,16]);self.assertEqual(sum(map(len,r6.SRC['mandatory'].values())),118)
    self.assertEqual(r6.SRC['snapshot_sha'],r6.POL['operating_cut'])
  def test_positive_synthetic_comparison(self):
    self.assertEqual([],r6.plan_errors(self.p));self.assertEqual('A_ADVANTAGE_AT_COMPLETE_SCOPE',self.c['status']);self.assertEqual([],r6.validate_spine(self.s,self.p,self.m,self.c))
  def test_freeze_missing_or_tampered(self):
    p=copy.deepcopy(self.p);p.pop('freeze_digest');self.assertIn('FREEZE_HASH_MISSING_OR_STALE',r6.plan_errors(p))
    p=copy.deepcopy(self.p);p['cells'][0]['metric']='query_10_wall_s';self.assertIn('FREEZE_HASH_MISSING_OR_STALE',r6.plan_errors(p))
  def test_only_build_across_all_seven(self):
    p=copy.deepcopy(self.p);p['cells']=[{**self.p['cells'][0],'id':'X'+w,'workload':w} for w in r6.POL['workloads']];p['freeze_digest']=r6.planhash(p)
    x=r6.comparison(p,gen_measure(p));self.assertEqual('RED',x['status']);self.assertTrue(any('MANDATORY_DIMENSION_GAPS' in e for e in x['errors']))
  def test_six_excluded(self):
    p=copy.deepcopy(self.p);p['cells']=[self.p['cells'][0]];p['exclusions']=[{'workload':w,'specific_nonmateriality':'Due to synthetic test only owner claims not material','first_consumer_consequence':'Supposedly no effect on first consumer sourcefree I03','B_objection_or_concurrence':'B concurs conditionally after source-specific argument','owner':'independent qualified reviewer to determine materiality','H0_source_ref':'Sourcefree fixture only and no native rights','disposition':'B_CONCURS_PENDING_C'} for w in list(r6.POL['workloads'])[1:]]
    p['freeze_digest']=r6.planhash(p);x=r6.comparison(p,gen_measure(p));self.assertEqual('RED',x['status'])
  def test_unrun_rival_never_wins(self):
    m=copy.deepcopy(self.m);m['results'][0]['B']['status']='UNRUN_HELD';self.assertEqual('MISSING_MATCHED_DECISIVE_EVIDENCE',r6.comparison(self.p,m)['status'])
  def test_uncertain_rival_no_incumbent_tie_break(self):
    m=copy.deepcopy(self.m);m['results'][0]['B']['low']=0.5;m['results'][0]['B']['high']=3.5
    self.assertEqual('PARETO_OR_UNRESOLVED',r6.comparison(self.p,m)['status'])
  def test_comparison_not_winner_when_exclusions(self):
    p=copy.deepcopy(self.p);p['exclusions']=[{'workload':'W-R','specific_nonmateriality':'Synthetic explanatory sentence only','first_consumer_consequence':'Examined independent source first consumer','B_objection_or_concurrence':'Objected to by independent actual architect','owner':'source owner qualified independently','H0_source_ref':'sourcefree original test exemplar','disposition':'CHALLENGED_PENDING_C'}]
    p['cells']=[c for c in p['cells'] if c['workload']!='W-R'];p['freeze_digest']=r6.planhash(p)
    self.assertEqual('RED',r6.comparison(p,gen_measure(p))['status'])
  def test_B_prediscovery_versioning(self):
    p=copy.deepcopy(self.p);p['version']=2;p['parent_digest']=self.p['freeze_digest'];p['discovery']={'origin':'INDEPENDENT_B_PRE_RESULT','B_frozen_objection_sha':'b'*40,
      'source_finding_ref':'genuine sourcefree first-reader issue tuple','new_discriminator':'unmodeled repeated predicate invalidation cost',
      'why_original_frame_incomplete':'original frame omitted another reused subpopulation role',
      'controller_pre_result_freeze_ref':'protected immutable controller pre-result receipt'}
    p['freeze_digest']=r6.planhash(p);self.assertFalse(r6.plan_errors(p,self.p))
    p['first_results_seen']=True;p['freeze_digest']=r6.planhash(p);self.assertIn('POSTRESULT_AMENDMENT_NOT_LAWFUL_IN_PLACE',r6.plan_errors(p,self.p))
    p['first_results_seen']=False;p['cells'].pop();p['freeze_digest']=r6.planhash(p);self.assertIn('AMENDMENT_DROPPED_OLD_CELL',r6.plan_errors(p,self.p))
  def test_true_original_observation(self):self.assertEqual([],r6.validate_source_claim(sample_claim()))
  def test_missing_value_no_original(self):
    c=sample_claim();c['observation']='NOT_OBSERVED';self.assertIn('UNOBSERVED_TO_SUBSTANTIVE_SOURCE_VALUE',r6.validate_source_claim(c))
  def test_model_cannot_be_original(self):
    c=sample_claim();c['source_status']='MODEL_OR_FICTION';self.assertIn('MODEL_OR_FICTION_PROMOTED',r6.validate_source_claim(c))
  def test_household_cannot_be_person(self):
    c=sample_claim();c['unit']='HOUSEHOLD';c['source_unit']='HOUSEHOLD';self.assertIn('SOURCE_TARGET_UNIT_COLLAPSE',r6.validate_source_claim(c))
  def test_interviewer_not_self(self):
    c=sample_claim();c['attribution']='INTERVIEWER';self.assertIn('INTERVIEWER_OR_ADMIN_TO_SELF',r6.validate_source_claim(c))
  def test_uncertified_wave_semantics(self):
    c=sample_claim();c['claim_wave_comparable']=True;c['translation']='UNRECONCILED';self.assertIn('UNLICENSED_WAVE_SEMANTIC_EQUIVALENCE',r6.validate_source_claim(c))
  def test_missing_no_effect(self):
    c=sample_claim();c['observation']='NOT_OBSERVED';c['claim_no_effect_from_absence']=True;self.assertIn('MISSING_TO_NO_EFFECT',r6.validate_source_claim(c))
  def test_instrument_metadata_absence_allowed(self):self.assertEqual([],r6.validate_source_claim(sample_meta()))
  def test_metadata_not_respondent(self):
    c=sample_meta();c['target_is_respondent_claim']=True;self.assertIn('METADATA_FALSE_RESPONDENT_CLAIM',r6.validate_source_claim(c))
  def test_design_intent_unproved(self):
    c=sample_meta();c['claim_kind']='INTERPRETIVE_HYPOTHESIS';c['stated_as_design_intent']=True
    self.assertIn('INTERPRETATION_AS_DESIGN_INTENT',r6.validate_source_claim(c))
  def test_world_to_actor_src_C11_spoof(self):
    s=copy.deepcopy(self.s);s['routes']['WORLD_TO_ACTOR']['edge_ids']=['e1'];self.assertIn('ROUTE_DOMAIN_SPOOF:WORLD_TO_ACTOR',r6.validate_graph(s))
  def test_graph_forbidden_causal_promotion(self):
    s=copy.deepcopy(self.s);s['edges'][0]['to']='STR';self.assertTrue(any('GRAPH_FORBIDDEN_TRANSITION' in e for e in r6.validate_graph(s)))
  def test_graph_shadow_authority(self):
    s=copy.deepcopy(self.s);s['edges'][0]['grade']='SOURCE_CERTIFIED';self.assertTrue(any('SECOND_VOCABULARY' in e for e in r6.validate_graph(s)))
  def test_ready_placeholder_consumer_rejected(self):
    h=copy.deepcopy(self.s['handoffs'][0]);h['consumer_symbol']='to be specified by future engineer'
    self.assertIn('READY_BUT_PLACEHOLDER_consumer_symbol',r6.validate_handoff(h))
  def test_held_future_card_allowed(self):
    h=copy.deepcopy(self.s['handoffs'][0]);h.update({'implementation_status':'OWNER_HELD','producer_symbol':'NONE','consumer_symbol':'NONE','source_cut':'NONE',
      'held_reason':'External science owner has not issued the actor interpretation contract','first_consumer_grade':'OWNER_HELD'})
    self.assertFalse(r6.validate_handoff(h))
  def test_physical_decision_borrowing_unrelated_cells(self):
    s=copy.deepcopy(self.s);other=copy.deepcopy(s['physical_decisions'][0]);other['id']='P-UNRELATED';other['dependency_effect']='new unrelated layout decision would require own supporting data'
    s['physical_decisions'].append(other)
    self.assertTrue(any('PHYSICAL_BORROWED_UNRELATED_COMPARISON' in e for e in r6.validate_spine(s,self.p,self.m,self.c)))
  def test_original_response_must_be_documented_respondent_record(self):
    c=sample_claim();c['source_status']='DOCUMENTED_DESIGN'
    self.assertIn('NON_SOURCE_TO_ORIGINAL_VALUE',r6.validate_source_claim(c))
    c=sample_claim();c.pop('record_value_ref')
    self.assertIn('SOURCE_VALUE_WITHOUT_SELECTED_RESPONDENT_RECORD',r6.validate_source_claim(c))
  def test_selected_consumer_must_be_in_global_graph(self):
    s=copy.deepcopy(self.s);s['physical_decisions'][0]['first_consumer_node_id']='INVENTED'
    self.assertIn('PHYSICAL_CONSUMER_NOT_IN_GLOBAL_GRAPH',r6.validate_spine(s,self.p,self.m,self.c))
  def test_orphan_physical_decision(self):
    s=copy.deepcopy(self.s);s['physical_decisions'][0]['cell_ids']=[]
    self.assertTrue(any('PHYSICAL_WITHOUT' in e for e in r6.validate_spine(s,self.p,self.m,self.c)))
  def test_118_conservation(self):
    s=copy.deepcopy(self.s);s['historical_inheritance']['exact_ids'].pop()
    self.assertIn('118_IDENTITY_CONSERVATION_MISMATCH',r6.validate_spine(s,self.p,self.m,self.c))
    s=copy.deepcopy(self.s);s['historical_inheritance']['K3_not_adopted_count']=25
    self.assertIn('K3_FUNCTION_CONSERVATION_MISMATCH',r6.validate_spine(s,self.p,self.m,self.c))
  def test_fake_product_delta(self):
    s=copy.deepcopy(self.s);s['product_deltas'][0]['after_evidence']='FAKE-EVIDENCE-ID'
    self.assertTrue(any('DELTA_UNPROVED_AFTER' in e for e in r6.validate_spine(s,self.p,self.m,self.c)))
  def test_ready_with_unmeasured_rival(self):
    m=copy.deepcopy(self.m);m['results'][0]['B']['status']='UNRUN_HELD';res=r6.comparison(self.p,m)
    s=copy.deepcopy(self.s);s['comparison_digest']=r6.digest(res)
    self.assertIn('READY_NOT_SUPPORTED_BY_COMPLETE_COMPARISON',r6.validate_spine(s,self.p,m,res))
  def test_author_C_chronology(self):
    s=copy.deepcopy(self.s);s['builder_cold_start']='EXECUTED_FIRST_READER_PROOF'
    self.assertIn('AUTHOR_FABRICATED_FUTURE_BUILDER',r6.validate_spine(s,self.p,self.m,self.c))
  def test_P15_verdict_alias_rejected(self):
    x={'schema':'ANVIL_R6_STAGE_1','stage':'P15','verdict':'A_PROVED_AT_SCOPE','source_cut':'frozen source code HEAD','owner':'actual bound physical test owner'}
    self.assertIn('STAGE_INVALID_VERDICT',r6.check_stage('P15',x))
  def test_H1_unknown_c_grade_rejected(self):
    x={'schema':'ANVIL_R6_STAGE_1','stage':'H1','verdict':'H1_RECEIVED_SCOPED','source_cut':'real source head','owner':'verified competent owner','C_receipt':{'builder_grade':'INDETERMINATE_RANDOM','verdict':'C_ACCEPT_SCOPED','head':HASH,'P2_head':HASH,'future_builder_grade':'EXACT_BUILDER_HOLD'},
       'P2_head':HASH, 'owner_authority':'VERIFIED_COMPETENT_OWNER','protected_received_YN':'YES','paired_progress_CAS':'AUTHENTICATED_CAS_RECEIVED',
       'CAS_commit_sha':HASH,'CAS_receipt_evidence':'authentic example not actual','architecture_decidable_YN':'YES','commission_complete_YN':'YES',
       'engineering_accepted_YN':'NO','scientific_granted_YN':'NO','source_rights_granted_YN':'NO','actor_granted_YN':'NO'}
    self.assertIn('H1_UNKNOWN_BUILDER_GRADE',r6.check_stage('H1',x))
  def test_H1_without_CAS_rejected(self):
    x={'schema':'ANVIL_R6_STAGE_1','stage':'H1','verdict':'H1_RECEIVED_SCOPED','source_cut':'real source head','owner':'verified competent owner','C_receipt':{'builder_grade':'SPECIFICATION_CONSTRUCTION_READY','verdict':'C_ACCEPT_SCOPED','head':HASH,'P2_head':HASH,'future_builder_grade':'EXACT_BUILDER_HOLD'},
       'P2_head':HASH,'owner_authority':'VERIFIED_COMPETENT_OWNER','protected_received_YN':'NO','paired_progress_CAS':'HOLD',
       'architecture_decidable_YN':'YES','commission_complete_YN':'YES','engineering_accepted_YN':'NO',
       'scientific_granted_YN':'NO','source_rights_granted_YN':'NO','actor_granted_YN':'NO'}
    self.assertIn('H1_NOT_ACTUALLY_RECEIVED',r6.check_stage('H1',x))
  def test_C_review_must_have_two_builder_cards(self):
    x={'schema':'ANVIL_R6_STAGE_1','stage':'C','verdict':'C_ACCEPT_SCOPED', 'source_cut':'synthetic exact source static',
      'owner':'independent reviewer identity requires external verification','P2_frozen_head':HASH,
      'builder_grade':'SPECIFICATION_CONSTRUCTION_READY','future_builder_grade':'EXACT_BUILDER_HOLD',
      'raw_comparison_verified':True,'semantic_paths_verified':True,'first_consumer_scope_verified':True,
      'current_handoff_id':'the same card number','future_handoff_id':'the same card number'}
    self.assertIn('C_NOT_TWO_DISTINCT_BUILDER_CARDS',r6.check_stage('C',x))
  def test_engineering_not_promoted_from_source_static(self):
    x={'schema':'ANVIL_R6_STAGE_1','stage':'H1','verdict':'HQ_CURRENTNESS_HOLD','source_cut':'real source head','owner':'verified competent owner',
       'C_receipt':{'builder_grade':'SPECIFICATION_CONSTRUCTION_READY','verdict':'C_ACCEPT_DOCUMENTARY_HOLD','head':HASH,'P2_head':HASH,'future_builder_grade':'EXACT_BUILDER_HOLD'},
       'P2_head':HASH,'exact_hold':'owner CAS and actor source missing','engineering_accepted_YN':'YES',
       'architecture_decidable_YN':'NO','commission_complete_YN':'YES','scientific_granted_YN':'NO','source_rights_granted_YN':'NO',
       'actor_granted_YN':'NO','protected_received_YN':'NO'}
    self.assertIn('H1_ENGINEERING_WITHOUT_EXECUTED_FIRST_EFFECT',r6.check_stage('H1',x))
  def test_deterministic_render_tamper_detection(self):
    with tempfile.TemporaryDirectory() as td:
      m=r6.render(self.s,td);self.assertEqual(118,len(pathlib.Path(td,'REQUIREMENT_CONSERVATION.jsonl').read_text().splitlines()))
      pathlib.Path(td,'DESIGN_DECISION.md').write_text('mutated')
      self.assertNotEqual(r6.filehash(pathlib.Path(td,'DESIGN_DECISION.md')),m['DESIGN_DECISION.md'])

if __name__=='__main__':
    v=unittest.main(verbosity=2)
