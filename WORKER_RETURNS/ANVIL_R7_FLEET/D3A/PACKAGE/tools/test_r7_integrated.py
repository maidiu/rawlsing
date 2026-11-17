#!/usr/bin/env python3
"""Hostile synthetic tests of the ACTIVE integrated ANVIL workflow.

Local structural fixtures prove no real-source or scientific sufficiency.
"""
import copy,hashlib,json,pathlib,tempfile,unittest,subprocess,sys
from test_r6 import r6_fixture
import d3a_fixture as F
from r7_integrated import check,digest,sha,DOMAINS
from r7_builder import write as build_projections
ANCHORS=F.anchors()

ROOT=pathlib.Path(__file__).resolve().parents[1]
QUOTE='The original DDM was not failed work to be replaced.'
# Source in the actual R7 package; not a claim that this is native proof.
SOURCE='22_R6_VALUE_AND_FUNCTION_CONSERVATION.md'
SOURCE_EXCERPT='Historical pre-FORGE 29/26/14, 118 mixed identity and five-test law'

class Integrated(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.work=pathlib.Path(self.tmp.name)
        self.evidence=self.work/'evidence';self.evidence.mkdir()
        # D3A correction: S1 origin is the source-qualified inventory, NOT a
        # finished R5/R6 P2 SPINE.  The SPINE remains an optional historical pointer.
        self.inv=json.loads(F.INVENTORY.read_text())
        self.hptr=self.put('inventory.json',self.inv)
        quote=SOURCE_EXCERPT
        ref={'path':SOURCE,'sha256':sha((ROOT/SOURCE).read_bytes()),'exact_excerpt':quote}
        rows=[]
        for i,d in enumerate(DOMAINS):
            rows.append({'id':f'R{i+1}','domain':d,'binding':'FUTURE_NONPRECLUSION' if d in ('SEAM_WORLD_ACTOR','FIELD_FORGE') else 'PRESENT_HARD',
              'substantive_requirement':f'{d} must preserve explicit exact original scientific and evidence boundaries without replacing them with convenience fields',
              'why_needed':'This requirement is indispensable to the real first consumer, regardless of which physical algorithm is selected',
              'loss_if_missing':'Without the obligation, a physically elegant source layout could erase a necessary downstream or historical distinction',
              'first_consumer':'The current sourcefree native empirical recipient and future governed possibility/world handoff',
              'architectural_consequence':'Preserve an independently inspectable representation of each relevant scientific distinction and later interface',
              'proof_or_owner_hold':'Check exact artifact semantics and replay with the qualified first consumer or preserve named authority hold',
              'evidence':ref})
        self.frame={'schema':'ANVIL_R7_INTEGRATED','stage':'COMMON_FRAME',
            'workflow':'ONE_INTEGRATED_INVESTIGATION_OPTIONAL_TARGETED_DUELS','phase':'BEFORE_ARCHITECTURE_SELECTION',
            'architecture_selected':False,'mandatory_rival_architecture':False,'duel_required':False,
            'A_B_method':'OPTIONAL_SAME_QUESTION_SAME_EVIDENCE','scope':'C11_QUERY_DESIGN',
            'source_cut':'7fc00289dd801d2d0a8ce159986c7595fc27a4d9','protected_head':'a'*40,
            'user_priority_source':'Pinned user instruction selecting complete empirical system and lowest executable cost',
            'first_real_consumer':'Authorized generic sourcefree saved C11 native I03 and I05 operations',
            'currentness_gap_or_exact_verified_state':'Protected owner and runtime conditions remain external and are not authenticated by these fixtures',
            'science_authority_boundary':'Field Forge, world and actor science cannot be issued by physical architecture author',
            'whole_program_mission':'Complete original function continuity and C11 empirical computation into later scientifically lawful world and person products',
            'source_grades_authentic_by_local_test':False,'requirements':rows,
            'historical_conservation':self.hptr,'historical_source_spine':None}
        self.fptr=self.put('frame.json',self.frame)
        self.decision={'schema':'ANVIL_R7_INTEGRATED','stage':'INTEGRATED_DECISION','common_frame':self.fptr,
          'frame_sha256':digest(self.frame),'decision_process':'ONE_SYNTHESIS_NO_MANDATORY_RIVAL',
          'basis':'ANALYTICAL_SOURCE_GROUNDED','grade':'AUTHOR_PROPOSED_PENDING_C',
          'architecture_description':'Retain canonical C11 authority, add a scoped derived execution interface, and explicitly preserve all proof and first-consumer boundaries',
          'entire_source_to_actor_dataflow':'From legitimate original source projection through canonical thirteen-family C11 and native I03 computation into future F1–F4, Field Forge, independent world, and continuing actor',
          'algorithm_and_data_structures':'Use one verified event store, two selective access routes, and reusable evidence-bearing respondent condition intermediates without a duplicate authority',
          'resource_cost_reasoning':'Minimize repeated event reconstruction and qualified population evaluation before changing a physical store; retain the existing six-gibibyte aggregate resource ceiling',
          'historical_function_conservation':'Conserve all 118 historical and prospective identities with the negative semantics, linked first consumers and truthful nonadoption of future science',
          'scientific_boundary_and_nonpreclusion':'Observational survey relationships cannot become structural causes, fictional world facts, or actual actor experiences without separate competent science',
          'strongest_surviving_objection':'The current body-json layout and physical positioning may impose first-query cost that an authenticated selective reader cannot avoid without an alternative indexing format',
          'why_selected_over_feasible_alternatives':'Uses accepted existing semantic and physical assets and introduces less compatibility and authority risk than switching the entire persistent representation',
          'next_actual_engineering_operation':'Publish and independently receive the prepared saved session correction, then implement one sourcefree shared population execution path under existing owner rights',
          'single_selected_strategy':'Verified C11 with prepared analytical execution layer',
          'first_real_consumer':self.frame['first_real_consumer'],
          'alternatives_considered':[{'technical_approach':'Wholesale independent SQL-backed physical release replacement', 'state':'VIABLE_NOT_SELECTED',
              'why_not_selected_or_held':'This would reopen canonical replay and source authentication boundaries without evidence that the replacement resolves the present repeated-evaluation costs'}],
          'choice_reversers':[{'status':'RESOLVED_AT_ANALYTICAL_SCOPE','question':'Can qualified population preparation be reused without changing source truth?'}],
          'requires_full_A_B_comparison':False,'competing_implementations_mandatory':False,
          'architecture_claims_independent_acceptance':False,'targeted_duel':None,
          'boundary_contract_sha256':sha((ROOT/'02_BOUNDARY_CONTRACTS.json').read_bytes()),
          'identity_dispositions':F.identity_rows(self.inv),'boundary_court':F.boundary_court(),
          'typed_graph':F.typed_graph(),
          'requirement_dispositions':[{'requirement_id':r['id'],
             'disposition':'FUTURE_NONPRECLUDED' if r['binding']=='FUTURE_NONPRECLUSION' else 'PRESENT_PRESERVED',
             'evidence_grade':'DOCUMENTARY',
             'actual_design_effect':'Keep the original documented capacity and a typed consumer boundary with explicit negative and restoration semantics',
             'specific_first_consumer_path':'Native saved I03 facts can lawfully feed qualified conditional and possibility interfaces under source authority',
             'conservation_or_refusal_witness':'Existing frozen source contracts specify the required denial and restoration behavior, not an actual executed proof',
             'evidence':ref} for r in rows]}
        self.decision['inventory_sha256']=digest(self.inv)
        self.decision['projection_manifest']=build_projections(self.decision,self.frame,self.inv,self.evidence)
        self.dptr=self.put('decision.json',self.decision)
    def tearDown(self):self.tmp.cleanup()
    def put(self,name,obj):
        b=(json.dumps(obj,sort_keys=True,ensure_ascii=False)+'\n').encode();(self.evidence/name).write_bytes(b)
        return {'path':name,'sha256':sha(b)}
    def frame_result(self):return check('FRAME',self.frame,self.evidence,ROOT,ANCHORS)
    def dec_result(self):return check('DECISION',self.decision,self.evidence,ROOT,ANCHORS)
    def test_existing_historical_spine_transfers_without_new_census(self):
        from r7_transfer_conservation import transfer
        spine=r6_fixture();obj=transfer(json.dumps(spine).encode())
        self.assertEqual(118,sum(len(v) for v in obj['coverage'].values()))
        self.assertEqual('VERBATIM_R5_R6_SEMANTIC_COVERAGE_NO_RECLASSIFICATION',obj['transfer_method'])
        self.assertFalse(any(v.get('adopted',False) for v in obj['coverage']['PYAT_PC'].values()))
    def test_obsolete_comparator_stage_fails_closed_as_live_cli(self):
        proc=subprocess.run([sys.executable,str(ROOT/'tools/r7_stage.py'),'C','not_real.json',
              '--evidence-root',str(self.evidence)],capture_output=True,text=True)
        self.assertEqual(2,proc.returncode)
        self.assertIn('R7_LEGACY_A_B_STAGE_NOT_ACTIVE',proc.stdout)
    def test_good_uncontested_integrated_decision_without_a_b(self):
        self.assertTrue(self.frame_result()['status'].startswith('PASS'),self.frame_result())
        self.assertTrue(self.dec_result()['status'].startswith('PASS'),self.dec_result())
    def test_old_required_two_architects_is_a_defect(self):
        self.frame['mandatory_rival_architecture']=True
        self.assertIn('FRAME:RIVAL_NOT_OPTIONAL',self.frame_result()['errors'])
    def test_A_and_B_cannot_split_the_source_and_downstream(self):
        self.frame['A_B_method']='A_ONLY_CURRENT_B_ONLY_SEAM'
        self.assertIn('FRAME:DUEL_METHOD_DISTORTED',self.frame_result()['errors'])
    def test_no_future_domain_unnoticed(self):
        self.frame['requirements']=[r for r in self.frame['requirements'] if r['domain']!='SEAM_WORLD_ACTOR']
        self.assertIn('FRAME:WHOLE_MISSION_DOMAIN_MISSING:SEAM_WORLD_ACTOR',self.frame_result()['errors'])
    def test_no_historical_118_id_substitution(self):
        obj=json.loads((self.evidence/'inventory.json').read_text())
        obj['rows']=[r for r in obj['rows'] if r['id']!='PYAT-PC-R9-07']
        self.frame['historical_conservation']=self.put('inventory2.json',obj)
        self.assertTrue(any('HISTORY:ID_SET_DRIFT' in e for e in self.frame_result()['errors']))
    def test_historical_row_meaning_cannot_be_rewritten(self):
        obj=json.loads((self.evidence/'inventory.json').read_text())
        next(r for r in obj['rows'] if r['group']=='K1_CAP')['source_semantics']='An invented alternative function that conflicts with the located original conservation record'
        self.frame['historical_conservation']=self.put('inventory_mutation.json',obj)
        self.assertTrue(any('SEMANTICS_NOT_GROUNDED_IN_ORIGIN' in e for e in self.frame_result()['errors']))
    def test_never_promote_historical_proposal(self):
        obj=json.loads((self.evidence/'inventory.json').read_text())
        next(r for r in obj['rows'] if r['group']=='PYAT_PC')['adopted']=True
        self.frame['historical_conservation']=self.put('inventory2.json',obj)
        self.assertTrue(any('FALSE_PROSPECTIVE_ADOPTION' in e for e in self.frame_result()['errors']))
    def test_source_pin_is_not_just_a_citation_string(self):
        self.frame['requirements'][0]['evidence']['sha256']='f'*64
        self.assertTrue(any('SOURCE_HASH_OR_QUOTE_DISAGREES' in e for e in self.frame_result()['errors']))
    def test_missing_source_not_made_into_unverified_claim(self):
        self.frame['requirements'][0]['evidence']['path']='no_such_doc.md'
        self.assertTrue(any('SOURCE_NOT_FOUND' in e for e in self.frame_result()['errors']))
    def test_decision_fails_without_requirement_crosswalk(self):
        self.decision['requirement_dispositions'].pop()
        self.assertIn('DECISION:INCOMPLETE_REQUIREMENT_RECONCILIATION',self.dec_result()['errors'])
    def test_present_obligation_cannot_be_called_future(self):
        self.decision['requirement_dispositions'][0]['disposition']='FUTURE_NONPRECLUDED'
        self.assertTrue(any('HARD_PRESENT_RELABELED_FUTURE' in e for e in self.dec_result()['errors']))
    def test_blocking_loss_cannot_win(self):
        self.decision['requirement_dispositions'][0]['disposition']='BLOCKING_LOSS'
        self.assertIn('DECISION:READY_WHILE_LOSING_REQUIRED_FUNCTION',self.dec_result()['errors'])
    def test_no_competing_implementations_required(self):
        self.decision['requires_full_A_B_comparison']=True
        self.assertIn('DECISION:COMPETITION_REQUIRED',self.dec_result()['errors'])
    def test_optional_duel_requires_same_exact_evidence(self):
        self.decision['basis']='TARGETED_DUEL'
        duel={'schema':'ANVIL_R7_TARGETED_DUEL','shared_frame_sha256':digest(self.frame),
          'single_decision_question':'Whether selective event indexing suffices for true three-way joint evidence given the current C11 contract',
          'why_independence_is_needed':'Same-respondent semantics and access economics are both plausible choice-reversing disagreements',
          'shared_evidence_description':'Both investigators have the entire history, source and downstream source evidence, not a separate domain',
          'investigators':[{'id':x,'shared_frame_sha256':digest(self.frame),
            'evidence_access':'SAME_FULL_EVIDENCE','assignment':'SAME_EXACT_QUESTION_INDEPENDENT_ANALYSIS',
            'analysis':'Detailed independently reasoned result about respondent coherence and exact query output'} for x in ('A','B')],
          'integrated_adjudication':'Independent reviewer identifies exact difference and checks it against the entire common scientific and source frame',
          'independence_proven_by_local_check':False}
        self.decision['targeted_duel']=self.put('duel.json',duel)
        self.assertTrue(self.dec_result()['status'].startswith('PASS'),self.dec_result())
        duel['investigators'][1]['assignment']='B_ONLY_DOWNSTREAM'
        self.decision['targeted_duel']=self.put('duel_bad.json',duel)
        self.assertIn('DECISION:DUEL_SPLIT_ASSIGNMENTS_FORBIDDEN',self.dec_result()['errors'])
    def test_no_fake_source_grants(self):
        self.frame['source_grades_authentic_by_local_test']=True
        self.assertIn('FRAME:FALSE_SOURCE_AUTHORITY',self.frame_result()['errors'])
    def test_no_paper_independence(self):
        c={'schema':'ANVIL_R7_INTEGRATED','stage':'INDEPENDENT_C','integrated_decision':self.dptr,
           'integrated_decision_sha256':digest(self.decision),'first_consumer':self.frame['first_real_consumer'],
           'independent_reverse_walk_of_whole_frame':'The reviewer separately traces source through I03/FF and onward to actor evidence, including negative cases.',
           'strongest_choice_reversing_objection':'The installed event index may not support conditioned joint analysis economically at survey width.',
           'scientific_and_owner_boundary':'No source scientific rights or actor-level structural causality can be issued from a documentary C assessment.',
           'actual_first_consumer_assessment':'This fixture does not run any real first-consumer and cannot justify adoption of original survey science.',
           'historical_no_loss_assessment':'The complete historical R5 contract remains frozen, with no recovered function automatically declared issued.',
           'boundary_contract_sha256':sha((ROOT/'02_BOUNDARY_CONTRACTS.json').read_bytes()),
           'boundary_court':F.boundary_court(),'typed_graph':F.typed_graph(),
           'projection_manifest':self.decision['projection_manifest'],
           'reviewer_relationship':'DISTINCT_NONAUTHOR_ASSERTION_PENDING_EXTERNAL_VERIFICATION',
           'choice_reversing_objection_survives':False,'verdict':'C_HOLD_EXACT',
           'builder_cards':[{'id':'first','domain':'CURRENT_FIRST_CONSUMER','grade':'EXACT_BUILDER_HOLD',
             'exact_hold':'Actual native source consumer proof and competent owner execution are not part of this synthetic test'},
             {'id':'future','domain':'FUTURE_NONPRECLUSION','grade':'EXACT_BUILDER_HOLD',
              'exact_hold':'Future actor/world source governance remains independent and cannot be invented by this local test'}],
           'original_source_granted_by_local_check':False,'owner_granted_by_local_check':False,
           'claims_protected_h1':False}
        self.assertTrue(check('C_INTEGRATED',c,self.evidence,ROOT,ANCHORS)['status'].startswith('PASS'))
        c['verdict']='C_CONDITIONALLY_ADMIT_DESIGN'
        self.assertIn('C:ADMIT_WITHOUT_CURRENT_BUILDER',check('C_INTEGRATED',c,self.evidence,ROOT,ANCHORS)['errors'])
        c['choice_reversing_objection_survives']=True
        self.assertIn('C:ACCEPTS_SURVIVING_REVERSER',check('C_INTEGRATED',c,self.evidence,ROOT,ANCHORS)['errors'])
        c['choice_reversing_objection_survives']=False;c['verdict']='C_HOLD_EXACT';c['reviewer_relationship']='I_AM_INDEPENDENT'
        self.assertIn('C:SELF_CERTIFIED_INDEPENDENCE',check('C_INTEGRATED',c,self.evidence,ROOT,ANCHORS)['errors'])
if __name__=='__main__':unittest.main(verbosity=2)
