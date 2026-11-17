#!/usr/bin/env python3
"""Hostile local tests for the corrected ANVIL R7 S1 / DECISION / C gates.

These fixtures use the exact protected documentary source bytes shipped under
tests/fixtures/source_118.  They prove local structure and fail-closed behavior
only; no native survey execution, independent C, source right or H1 is created.
"""
from __future__ import annotations
import copy, hashlib, json, pathlib, shutil, tempfile, unittest

from r7_integrated import check, digest, sha, DOMAINS
from r7_inventory import build_inventory
import r7_build

ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCE=ROOT/'tests/fixtures/source_118'
DOC=SOURCE/'22_R6_VALUE_AND_FUNCTION_CONSERVATION.md'
DOC_EXCERPT='Historical pre-FORGE 29/26/14, 118 mixed identity and five-test law'

def good_source_ref():
    return {'path':DOC.name,'sha256':sha(DOC.read_bytes()),'exact_excerpt':DOC_EXCERPT}

class G(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.work=pathlib.Path(self.tmp.name)
        self.evidence=self.work/'evidence';self.evidence.mkdir()
        self.inv=build_inventory(SOURCE,SOURCE/'PIN_MANIFEST.json',ROOT)
        self.inv_ptr=self.put('inventory.json',self.inv)
        self.ref=good_source_ref()
        reqs=[]
        for i,d in enumerate(DOMAINS):
            reqs.append({'id':f'R{i+1}','domain':d,
                'binding':'FUTURE_NONPRECLUSION' if d in ('SEAM_WORLD_ACTOR','FIELD_FORGE') else 'PRESENT_HARD',
                'substantive_requirement':f'{d} must preserve exact original scientific and evidence boundaries without replacing them with convenience fields',
                'why_needed':'This requirement is indispensable to the real first consumer regardless of the selected physical algorithm',
                'loss_if_missing':'Without the obligation a physically elegant source layout could erase a necessary downstream or historical distinction',
                'first_consumer':'The current sourcefree native empirical recipient and future governed possibility/world handoff',
                'architectural_consequence':'Preserve an independently inspectable representation of each relevant scientific distinction and later interface',
                'proof_or_owner_hold':'Check exact artifact semantics and replay with the qualified first consumer or preserve a named authority hold',
                'evidence':self.ref})
        self.frame={'schema':'ANVIL_R7_INTEGRATED','stage':'COMMON_FRAME',
            'workflow':'ONE_INTEGRATED_INVESTIGATION_OPTIONAL_TARGETED_DUELS','phase':'BEFORE_ARCHITECTURE_SELECTION',
            'architecture_selected':False,'mandatory_rival_architecture':False,'duel_required':False,
            'A_B_method':'OPTIONAL_SAME_QUESTION_SAME_EVIDENCE','scope':'C11_QUERY_DESIGN',
            'source_cut':'7fc00289dd801d2d0a8ce159986c7595fc27a4d9','protected_head':'a'*40,
            'user_priority_source':'Pinned user instruction selecting complete empirical system and lowest executable cost',
            'first_real_consumer':'Authorized generic sourcefree saved C11 native I03 and I05 operations',
            'currentness_gap_or_exact_verified_state':'Protected owner and runtime conditions remain external and are not authenticated by these fixtures',
            'science_authority_boundary':'Field Forge, world and actor science cannot be issued by a physical architecture author',
            'whole_program_mission':'Complete original function continuity and C11 empirical computation into later scientifically lawful world and person products',
            'source_grades_authentic_by_local_test':False,'requirements':reqs,'source_inventory':self.inv_ptr}
        nodes=[
          {'id':'N_SRC','producer':'Original source decoder and release custodian','producer_authority':'PYAT S01 source owner','input_types':['external_source'],'output_types':['raw_source'],'time_mode':'OBSERVED','first_consumer':'N_C11','decision_id':'D1','alternative_id':'A1'},
          {'id':'N_C11','producer':'Sealed thirteen-family C11 writer','producer_authority':'S2-C/S1-E physical owner','input_types':['raw_source'],'output_types':['canonical_event'],'time_mode':'OBSERVED','first_consumer':'N_CALC','decision_id':'D1','alternative_id':'A1'},
          {'id':'N_CALC','producer':'Native I03/I05/F1-F4 computation','producer_authority':'PYAT empirical computation owner','input_types':['canonical_event'],'output_types':['empirical_configuration'],'time_mode':'OBSERVED','first_consumer':'N_FIELD','decision_id':'D1','alternative_id':'A1'},
          {'id':'N_FIELD','producer':'FF01 descriptive field reader','producer_authority':'PYAT Field Forge #1009 owner','input_types':['empirical_configuration'],'output_types':['field_configuration'],'time_mode':'MODELED','first_consumer':'N_WORLD','decision_id':'D1','alternative_id':'A1'},
          {'id':'N_WORLD','producer':'N9/N10W selected world','producer_authority':'PYAT N9/N10W science owner (HELD)','input_types':['field_configuration','performed_event'],'output_types':['world_possibility','world_possible_event'],'time_mode':'FICTIONAL','first_consumer':'N_ACTOR','decision_id':'D1','alternative_id':'A1'},
          {'id':'N_ACTOR','producer':'SOROK continuing actor','producer_authority':'SOROK actor/consent owner (HELD)','input_types':['world_possibility','world_possible_event'],'output_types':['actor_state','performed_event'],'time_mode':'FICTIONAL','first_consumer':'N_WORLD','decision_id':'D1','alternative_id':'A1'}]
        edges=[
          {'id':'E1','from':'N_SRC','to':'N_C11','data_type':'raw_source','authority_grade':'DOCUMENTARY','temporal_mode':'OBSERVED','negative_or_refusal':'wrong edition or denied source refuses','invalidation_rule':'source hash or release revocation','boundary':'T1'},
          {'id':'E2','from':'N_C11','to':'N_CALC','data_type':'canonical_event','authority_grade':'DOCUMENTARY','temporal_mode':'OBSERVED','negative_or_refusal':'false same-person join or wrong denominator refuses','invalidation_rule':'C11 member or CURRENT revocation','boundary':'T2'},
          {'id':'E3','from':'N_CALC','to':'N_FIELD','data_type':'empirical_configuration','authority_grade':'DOCUMENTARY','temporal_mode':'OBSERVED','negative_or_refusal':'marginal-only substitute refuses','invalidation_rule':'source or estimand incompatibility','boundary':'T3'},
          {'id':'E4','from':'N_FIELD','to':'N_WORLD','data_type':'field_configuration','authority_grade':'DOCUMENTARY','temporal_mode':'MIXED_TYPED','negative_or_refusal':'survey opinion treated as institutional power refuses','invalidation_rule':'structural source revocation','boundary':'T4'},
          {'id':'E5','from':'N_WORLD','to':'N_ACTOR','data_type':'world_possibility','authority_grade':'DOCUMENTARY','temporal_mode':'FICTIONAL','negative_or_refusal':'respondent-to-character identity collapse refuses','invalidation_rule':'world branch invalidation','boundary':'T5'},
          {'id':'E6','from':'N_WORLD','to':'N_ACTOR','data_type':'world_possible_event','authority_grade':'DOCUMENTARY','temporal_mode':'FICTIONAL','negative_or_refusal':'no actor access yields no knowledge','invalidation_rule':'actor/world permission revocation','boundary':'T6'},
          {'id':'E7','from':'N_ACTOR','to':'N_WORLD','data_type':'performed_event','authority_grade':'DOCUMENTARY','temporal_mode':'FICTIONAL','negative_or_refusal':'fictional act cannot edit observed C11','invalidation_rule':'branch replay or committed past invalidation','boundary':'T7'}]
        self.graph={'nodes':nodes,'edges':edges}
        disp=[]
        for e in self.inv['entries']:
            g=e['group']
            if g=='K1_CAP': st='PRESENT_PRESERVED';sa='HISTORICAL_FUNCTION_RETAINED'
            elif g in ('PYAT_PC','P4R'): st='RETAINED_HISTORICAL_NONADOPTED';sa='NOT_ADOPTED' if g=='PYAT_PC' else 'HELD'
            else: st='FUTURE_NONPRECLUDED';sa='INCLUDED_NOT_ADOPTED'
            disp.append({'identity_id':e['id'],'disposition':st,'status_assertion':sa,'evidence_grade':'DOCUMENTARY',
                'design_effect':'Candidate preserves the exact identity meaning, negative and owner boundary without promoting it to adopted science',
                'first_consumer_path':'Traced from the source identity to the typed graph node and first consumer or explicit owner hold',
                'conservation_or_refusal_witness':'The identity origin hash, refusal semantics and negative case are retained and checked by the gate',
                'origin_sha256':e['origin_sha256'],'adopted_by_this_decision':False,'closed_by_this_decision':False,
                'evidence':({'path':'02_BOUNDARY_CONTRACTS.json','sha256':sha((SOURCE/'02_BOUNDARY_CONTRACTS.json').read_bytes()),'exact_excerpt':'"schema": "ANVIL_BOUNDARIES_R3"'} if g=='BOUNDARY' else {'path':'03_FROZEN_SOURCE_CUTS.json','sha256':sha((SOURCE/'03_FROZEN_SOURCE_CUTS.json').read_bytes()),'exact_excerpt':'"schema": "ANVIL_SOURCE_CUTS_R3"'} if g=='TERMINAL' else {'path':e['source_file'],'sha256':sha((SOURCE/e['source_file']).read_bytes()),'exact_excerpt':e['source_excerpt']})})
        self.decision={'schema':'ANVIL_R7_INTEGRATED','stage':'INTEGRATED_DECISION','common_frame':self.put('frame.json',self.frame),
          'frame_sha256':digest(self.frame),'decision_process':'ONE_SYNTHESIS_NO_MANDATORY_RIVAL',
          'basis':'ANALYTICAL_SOURCE_GROUNDED','grade':'AUTHOR_PROPOSED_PENDING_C',
          'architecture_description':'A test-only candidate that preserves the C11 authority and typed downstream boundaries without selecting a production backend',
          'entire_source_to_actor_dataflow':'From legitimate source through canonical C11 and native empirical computation into future field, world and actor owners',
          'algorithm_and_data_structures':'One verified event store with selective access and evidence-bearing respondent intermediates; no duplicate authority store',
          'resource_cost_reasoning':'Minimize repeated event reconstruction and retain the existing six-gibibyte aggregate resource ceiling without inventing a benchmark',
          'historical_function_conservation':'Conserve all 118 mixed identities with negative semantics, first consumers and truthful nonadoption of future science',
          'scientific_boundary_and_nonpreclusion':'Observational survey relationships cannot become structural causes, fictional world facts or actor experiences without separate competent science',
          'strongest_surviving_objection':'The current body-json layout may impose first-query cost that an authenticated selective reader cannot avoid without an alternative index',
          'why_selected_over_feasible_alternatives':'Uses accepted semantic and physical assets and introduces less compatibility and authority risk than a wholesale replacement',
          'next_actual_engineering_operation':'Publish and independently receive the prepared saved-session correction, then implement one sourcefree population execution path under existing rights',
          'single_selected_strategy':'Verified C11 with a prepared analytical execution layer (test fixture only)',
          'first_real_consumer':self.frame['first_real_consumer'],
          'alternatives_considered':[{'technical_approach':'Wholesale independent SQL-backed physical replacement','state':'VIABLE_NOT_SELECTED',
              'why_not_selected_or_held':'It would reopen canonical replay and source authentication without evidence that it resolves repeated-evaluation costs'}],
          'choice_reversers':[{'status':'RESOLVED_AT_ANALYTICAL_SCOPE','question':'Can qualified population preparation be reused without changing source truth?'}],
          'requires_full_A_B_comparison':False,'competing_implementations_mandatory':False,'architecture_claims_independent_acceptance':False,
          'targeted_duel':None,'whole_machine_graph':self.graph,
          'boundary_contract_map':{t:{'name':n} for t,n in zip(('T1','T2','T3','T4','T5','T6','T7'),
              ('source to canonical','canonical to computation','computation to field','field to world','world to encounter','encounter to actor','performed to next situation'))},
          'builder_handoff':{'first_reader_abi':'ANVIL_R7_FIRST_READER_ABI@1','input':'verified frame + source inventory','output':'six deterministic projections','negative':'refuse if any identity origin or boundary evidence mismatches','restore':'byte-identical rebuild','consumer':'distinct C then competent H1'},
          'h1_received_by_local_check':False,'protected_received_by_local_check':False,
          'identity_dispositions':disp,
          'requirement_dispositions':[{'requirement_id':r['id'],
             'disposition':'FUTURE_NONPRECLUDED' if r['binding']=='FUTURE_NONPRECLUSION' else 'PRESENT_PRESERVED',
             'evidence_grade':'DOCUMENTARY','actual_design_effect':'Keep the documented capacity and typed consumer boundary with explicit negative and restoration semantics',
             'specific_first_consumer_path':'Native saved I03 facts can feed qualified conditional and possibility interfaces under source authority',
             'conservation_or_refusal_witness':'The frozen source contracts specify denial and restoration behavior, not an actual native execution',
             'evidence':self.ref} for r in reqs]}
        self.dptr=self.put('decision.json',self.decision)
        self.c={'schema':'ANVIL_R7_INTEGRATED','stage':'INDEPENDENT_C','integrated_decision':self.dptr,
           'integrated_decision_sha256':digest(self.decision),'first_consumer':self.frame['first_real_consumer'],
           'independent_reverse_walk_of_whole_frame':'The reviewer separately traces source through C11, I03, FF and world/actor evidence including negative cases',
           'strongest_choice_reversing_objection':'The installed event index may not support conditioned joint analysis economically at survey width',
           'scientific_and_owner_boundary':'No source scientific rights or actor-level structural causality can be issued from a documentary C assessment',
           'actual_first_consumer_assessment':'This fixture does not run a real native first consumer and cannot justify adoption of original survey science',
           'historical_no_loss_assessment':'The complete historical inventory remains frozen with no recovered function automatically declared issued',
           'reviewer_relationship':'DISTINCT_NONAUTHOR_ASSERTION_PENDING_EXTERNAL_VERIFICATION',
           'choice_reversing_objection_survives':False,'verdict':'C_HOLD_EXACT',
           'boundary_court':{t:{'positive':'A valid source-consistent input produces the specified typed output at the boundary',
               'negative':'A mutated, revoked or absent input is refused at the actual boundary consumer without cached positive',
               'restore':'Exact authorized bytes and permission restore the prior positive output','grade':'SOURCE_STATIC_CONSERVED',
               'first_consumer_or_hold':'Boundary consumer named in the typed graph; owner-held where future science is not issued',
               'evidence':{'path':'02_BOUNDARY_CONTRACTS.json','sha256':sha((SOURCE/'02_BOUNDARY_CONTRACTS.json').read_bytes()),'exact_excerpt':self.quote(SOURCE/'02_BOUNDARY_CONTRACTS.json','"id":"'+t+'"')}} for t in ('T1','T2','T3','T4','T5','T6','T7')},
           'graph_audit':{'producer_authority_time_consumer_checked':True,'holes':[],'boundary_edges_checked':['T1','T2','T3','T4','T5','T6','T7']},
           'builder_handoff_review':'The handoff identifies an exact first-reader ABI, six projections, refusal and restore behavior and a named external C/H1 consumer',
           'actual_first_reader_verified':False,'local_h1_claim':False,'protected_received_locally':False,'h1_grade':'NOT_RECEIVED',
           'builder_cards':[{'id':'present','domain':'CURRENT_FIRST_CONSUMER','grade':'EXACT_BUILDER_HOLD',
             'exact_hold':'Actual native source consumer proof and competent owner execution are not part of this synthetic local test'},
             {'id':'future','domain':'FUTURE_NONPRECLUSION','grade':'EXACT_BUILDER_HOLD',
              'exact_hold':'Future actor/world source governance remains independent and cannot be invented by this local test'}],
           'original_source_granted_by_local_check':False,'owner_granted_by_local_check':False}
    def tearDown(self):self.tmp.cleanup()
    def quote(self,path,needle):
        text=path.read_text();i=text.index(needle);return text[i:i+80]
    def put(self,name,obj):
        b=(json.dumps(obj,sort_keys=True,ensure_ascii=False)+'\n').encode();(self.evidence/name).write_bytes(b)
        return {'path':name,'sha256':sha(b)}
    def frame_result(self,frame=None,source=SOURCE):
        return check('FRAME',frame or self.frame,self.evidence,source)
    def dec_result(self,decision=None):
        return check('DECISION',decision or self.decision,self.evidence,SOURCE)
    def c_result(self,c=None):
        return check('C_INTEGRATED',c or self.c,self.evidence,SOURCE)
    def assert_restore(self,call,key,errors):
        self.assertTrue(call()['status'].startswith('PASS'),call())
        old=copy.deepcopy(self.__dict__.get('_hold'))
        # caller mutates and restores explicitly in tests

    # ---------- S1 ----------
    def test_source_only_118_inventory_s1_pass(self):
        r=self.frame_result();self.assertTrue(r['status'].startswith('PASS'),r)
        self.assertEqual(118,r['identity_inventory_total'])
    def test_synthetic_r5_spine_alone_is_not_a_source(self):
        fake={'schema':'ANVIL_SPINE_R6','coverage':{}}
        f={k:v for k,v in self.frame.items() if k!='source_inventory'}
        f['historical_source_spine']=self.put('fake_spine.json',fake)
        f['historical_conservation']=self.put('fake_history.json',{'schema':'ANVIL_R7_INHERITED_CONSERVATION',
            'source_authentication':'NOT_AUTHENTICATED_BY_LOCAL_CHECK','source_spine_sha256':f['historical_source_spine']['sha256'],'coverage':{}})
        r=self.frame_result(f);self.assertIn('FRAME:NO_SOURCE_IDENTITY_INVENTORY',r['errors'])
    def test_missing_k3_row_red(self):
        bad=copy.deepcopy(self.inv);bad['entries']=[e for e in bad['entries'] if e['id']!='K1-CAP-17']
        f=copy.deepcopy(self.frame);f['source_inventory']=self.put('inv_missing.json',bad)
        r=self.frame_result(f);self.assertTrue(any('COUNT_DRIFT:K1_CAP' in x or 'K3_ID_CENSUS_CHANGED' in x for x in r['errors']),r)
    def test_missing_b10_red(self):
        bad=copy.deepcopy(self.inv);bad['entries']=[e for e in bad['entries'] if e['id']!='B-10']
        f=copy.deepcopy(self.frame);f['source_inventory']=self.put('inv_b10.json',bad)
        r=self.frame_result(f);self.assertTrue(any('COUNT_DRIFT:SEAM_B:9' in x for x in r['errors']),r)
    def test_source_byte_mutation_red_and_restore(self):
        tmp=self.work/'sourcecopy';shutil.copytree(SOURCE,tmp)
        p=tmp/'K3_CAP_29.tsv';orig=p.read_bytes();p.write_bytes(orig.replace(b'K1-CAP-01',b'K1-CAP-XX'))
        r=self.frame_result(source=tmp);self.assertTrue(any('BYTES_CHANGED' in x or 'EXCERPT_NOT_IN_SOURCE' in x for x in r['errors']),r)
        p.write_bytes(orig);r2=self.frame_result(source=tmp);self.assertTrue(r2['status'].startswith('PASS'),r2)
    def test_26_adopted_or_14_closed_red(self):
        bad=copy.deepcopy(self.inv)
        for e in bad['entries']:
            if e['id']=='PYAT-PC-R9-01':e['adopted']=True
            if e['id']=='P4R-R01':e['closed']=True
        f=copy.deepcopy(self.frame);f['source_inventory']=self.put('inv_promo.json',bad)
        r=self.frame_result(f)
        self.assertTrue(any(x.endswith('UNAUTHORIZED_ADOPTION:PYAT-PC-R9-01') for x in r['errors']),r)
        self.assertTrue(any(x.endswith('FALSE_PROOF_CLOSURE:P4R-R01') for x in r['errors']),r)

    # ---------- S3 ----------
    def test_decision_all_118_passes_pending_c(self):
        r=self.dec_result();self.assertTrue(r['status'].startswith('PASS'),r)
        self.assertEqual(118,r['identity_dispositions'])
    def test_decision_missing_one_identity_red(self):
        d=copy.deepcopy(self.decision);d['identity_dispositions'].pop()
        self.assertIn('DECISION:INCOMPLETE_118_IDENTITY_RECONCILIATION',self.dec_result(d)['errors'])
    def test_53_rows_complete_but_one_identity_missing_red(self):
        d=copy.deepcopy(self.decision);d['identity_dispositions']=[x for x in d['identity_dispositions'] if x['identity_id']!='L-05']
        d['codex_53_used_as_118']=True
        r=self.dec_result(d);self.assertIn('DECISION:INCOMPLETE_118_IDENTITY_RECONCILIATION',r['errors'])
        self.assertIn('DECISION:PARTIAL_53_CROSSWALK_SUBSTITUTES_FOR_118',r['errors'])
    def test_new_adoption_or_closure_in_decision_red(self):
        d=copy.deepcopy(self.decision)
        for x in d['identity_dispositions']:
            if x['identity_id']=='PYAT-PC-R9-02':x['adopted_by_this_decision']=True
            if x['identity_id']=='P4R-R02':x['closed_by_this_decision']=True
        r=self.dec_result(d)
        self.assertIn('DECISION:PROSPECTIVE_ADOPTION:PYAT-PC-R9-02',r['errors'])
        self.assertIn('DECISION:FALSE_PROOF_CLOSURE:P4R-R02',r['errors'])
    def test_blocking_loss_and_silent_retirement_red(self):
        d=copy.deepcopy(self.decision)
        next(x for x in d['identity_dispositions'] if x['identity_id']=='K1-CAP-03')['disposition']='BLOCKING_LOSS'
        self.assertIn('DECISION:READY_WHILE_LOSING_IDENTITY',self.dec_result(d)['errors'])
        d=copy.deepcopy(self.decision);x=next(x for x in d['identity_dispositions'] if x['identity_id']=='K1-CAP-04')
        x['disposition']='RETAINED_HISTORICAL_NONADOPTED'
        self.assertIn('DECISION:HISTORICAL_NONADOPTION_OVERUSED:K1-CAP-04',self.dec_result(d)['errors'])
    def test_local_h1_claim_red(self):
        d=copy.deepcopy(self.decision);d['h1_received_by_local_check']=True
        self.assertIn('DECISION:LOCAL_H1_CLAIM',self.dec_result(d)['errors'])
    def test_typed_graph_hole_red(self):
        d=copy.deepcopy(self.decision);d['whole_machine_graph']['edges'][0].pop('authority_grade')
        self.assertTrue(any('EDGE_FIELD' in x for x in self.dec_result(d)['errors']))
    def test_decision_requires_requirement_crosswalk_and_hard_binding(self):
        d=copy.deepcopy(self.decision);d['requirement_dispositions'].pop()
        self.assertIn('DECISION:INCOMPLETE_REQUIREMENT_RECONCILIATION',self.dec_result(d)['errors'])
        d=copy.deepcopy(self.decision);d['requirement_dispositions'][0]['disposition']='FUTURE_NONPRECLUDED'
        self.assertIn('DECISION:HARD_PRESENT_RELABELED_FUTURE:R1',self.dec_result(d)['errors'])
    def test_optional_duel_requires_same_exact_evidence(self):
        d=copy.deepcopy(self.decision);d['basis']='TARGETED_DUEL'
        duel={'schema':'ANVIL_R7_TARGETED_DUEL','shared_frame_sha256':digest(self.frame),
          'single_decision_question':'Whether selective event indexing suffices for true three-way joint evidence given the current C11 contract',
          'why_independence_is_needed':'Same-respondent semantics and access economics are both plausible choice-reversing disagreements',
          'shared_evidence_description':'Both investigators have the entire history, source and downstream source evidence, not a separate domain',
          'investigators':[{'id':x,'shared_frame_sha256':digest(self.frame),'evidence_access':'SAME_FULL_EVIDENCE',
            'assignment':'SAME_EXACT_QUESTION_INDEPENDENT_ANALYSIS','analysis':'Detailed independently reasoned result about respondent coherence and exact query output'} for x in ('A','B')],
          'integrated_adjudication':'Independent reviewer identifies the exact difference and checks it against the entire common scientific and source frame',
          'independence_proven_by_local_check':False}
        d['targeted_duel']=self.put('duel.json',duel)
        self.assertTrue(self.dec_result(d)['status'].startswith('PASS'),self.dec_result(d))
        duel['investigators'][1]['assignment']='B_ONLY_DOWNSTREAM';d['targeted_duel']=self.put('duel_bad.json',duel)
        self.assertIn('DECISION:DUEL_SPLIT_ASSIGNMENTS_FORBIDDEN',self.dec_result(d)['errors'])
    def test_no_fake_source_grants(self):
        f=copy.deepcopy(self.frame);f['source_grades_authentic_by_local_test']=True
        self.assertIn('FRAME:FALSE_SOURCE_AUTHORITY',self.frame_result(f)['errors'])
    def test_no_mandatory_ab_or_rival(self):
        d=copy.deepcopy(self.decision);d['requires_full_A_B_comparison']=True
        self.assertIn('DECISION:COMPETITION_REQUIRED',self.dec_result(d)['errors'])
        f=copy.deepcopy(self.frame);f['mandatory_rival_architecture']=True
        self.assertIn('FRAME:RIVAL_NOT_OPTIONAL',self.frame_result(f)['errors'])
        f=copy.deepcopy(self.frame);f['A_B_method']='A_ONLY_CURRENT_B_ONLY_SEAM'
        self.assertIn('FRAME:DUEL_METHOD_DISTORTED',self.frame_result(f)['errors'])

    # ---------- C ----------
    def test_c_hold_passes(self):
        r=self.c_result();self.assertTrue(r['status'].startswith('PASS'),r)
    def test_c_missing_boundary_negative_red_and_restore(self):
        c=copy.deepcopy(self.c);c['boundary_court']['T2'].pop('negative')
        r=self.c_result(c);self.assertIn('C:BOUNDARY_MISSING_NEGATIVE:T2',r['errors'])
        c=copy.deepcopy(self.c);self.assertTrue(self.c_result(c)['status'].startswith('PASS'))
    def test_c_missing_restore_red(self):
        c=copy.deepcopy(self.c);c['boundary_court']['T5'].pop('restore')
        self.assertIn('C:BOUNDARY_MISSING_RESTORE:T5',self.c_result(c)['errors'])
    def test_c_graph_hole_red(self):
        c=copy.deepcopy(self.c);c['graph_audit']['holes']=['N_WORLD:no authority grade for performed_event']
        self.assertIn('C:TYPED_GRAPH_HOLE',self.c_result(c)['errors'])
    def test_c_local_h1_red(self):
        c=copy.deepcopy(self.c);c['local_h1_claim']=True
        self.assertIn('C:LOCAL_H1_OR_PROTECTED_CLAIM',self.c_result(c)['errors'])
        c=copy.deepcopy(self.c);c['h1_grade']='ACCEPTED'
        self.assertIn('C:LOCAL_H1_ACCEPTED',self.c_result(c)['errors'])
    def test_c_self_independence_red(self):
        c=copy.deepcopy(self.c);c['reviewer_relationship']='I_AM_INDEPENDENT'
        self.assertIn('C:SELF_CERTIFIED_INDEPENDENCE',self.c_result(c)['errors'])

    # ---------- builder ----------
    def test_six_projections_deterministic_and_restore(self):
        arts,err=r7_build.build(self.decision,self.evidence,SOURCE)
        self.assertEqual([],err);self.assertEqual(set(r7_build.NAMES),set(arts))
        out=self.work/'built';man=r7_build.write(arts,out)
        self.assertEqual(6,len(man));self.assertEqual([],r7_build.verify(arts,out))
        p=out/'TYPED_GRAPH.json';orig=p.read_bytes();p.write_bytes(orig+b'x')
        self.assertIn('BYTES_CHANGED:TYPED_GRAPH.json',r7_build.verify(arts,out))
        p.write_bytes(orig);self.assertEqual([],r7_build.verify(arts,out))

if __name__=='__main__':unittest.main(verbosity=2)
