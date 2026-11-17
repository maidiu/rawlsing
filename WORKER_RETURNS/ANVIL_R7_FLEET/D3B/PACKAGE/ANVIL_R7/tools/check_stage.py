#!/usr/bin/env python3
"""ANVIL R5 finite-stage consistency checker; NEVER authenticates independent review/source/owner by text.
Git readback / native runner / owner rights must be externally verified in H0/C/H1.
"""
import argparse,json,pathlib,re,sys,hashlib
STAGES={'H0','A0','B0','A1','B1','P15','C','H1'}
SHA=re.compile(r'^[0-9a-f]{40}$'); H64=re.compile(r'^[0-9a-f]{64}$')
def complete(s,k):return s.get(k) is not None and s.get(k) not in ('',[],{})
def check(stage,s,evidence_root=None):
    e=[]
    if not isinstance(s,dict):return ['NOT_OBJECT']
    r6=s.get('schema')=='ANVIL_STAGE_R6'
    if s.get('schema') not in {'ANVIL_STAGE_R5','ANVIL_STAGE_R6'} or s.get('stage')!=stage:e.append('WRONG_STAGE_OR_SCHEMA')
    if s.get('repository')!='maidiu/rawlsing' or not SHA.fullmatch(str(s.get('source_cut'))):e.append('SOURCE_CUT_UNPINNED')
    for k in ('artifact_scope','author_role','sources_checked','actual_execution_grade','own_output_path','verdict'):
        if not complete(s,k):e.append('MISSING_'+k)
    if s.get('actual_execution_grade') not in {'S0_DOCUMENTARY','S1_SOURCE_STATIC','S2_SOURCEFREE_EXECUTED','S2_NATIVE_EXECUTED'}:e.append('INVALID_EXECUTION_GRADE')
    if not isinstance(s.get('sources_checked'),list) or not s.get('sources_checked'):e.append('NO_VERIFIED_SOURCE_LIST')
    if stage=='H0':
        for k in ('programme_oath_checked','paired_progress_checked','k3_protected_sha','model_MAX_check','tool_transport_check','branch_noncollision_check','comparator_sha256','boundary_dictionary_sha256','workload_hash','authority_matrix_hash','observability_contract_hash','original_mandate_hash','owner_authority_check','browser_transport_check'):
            if not complete(s,k):e.append('H0_MISSING_'+k)
        if s.get('verdict') not in {'H0_PASS','H0_HOLD_EXACT'}:e.append('BAD_H0_VERDICT')
    if stage=='A0':
        for k in ('incumbent_surface','source_information_risks','code_execution_heads','current_first_consumer','decision_reversers','no_B_findings_read'):
            if not complete(s,k):e.append('A0_MISSING_'+k)
        if s.get('no_B_findings_read') is not True:e.append('A0_NOT_BLIND')
        if not isinstance(s.get('decision_reversers'),list) or not s.get('decision_reversers'):e.append('A0_NO_REVERSERS')
    if stage=='B0':
        for k in ('boundary_demands','source_observability_case','independent_counterarchitecture','no_A_findings_read','problem_frame_challenge'):
            if not complete(s,k):e.append('B0_MISSING_'+k)
        if s.get('no_A_findings_read') is not True:e.append('B0_NOT_BLIND')
        if set(s.get('boundary_demands',{}))!={f'T{i}' for i in range(1,8)}:e.append('B0_MISSING_BOUNDARY')
        frame=s.get('problem_frame_challenge',{})
        if not isinstance(frame,dict) or any(len(str(frame.get(k,'')))<25 for k in ('inherited_assumption','falsifier','architectural_consequence')):e.append('B0_NO_REAL_FRAME_CHALLENGE')
        rival=s.get('independent_counterarchitecture',{})
        if not isinstance(rival,dict) or any(not complete(rival,k) for k in ('canonical_layout','prepared_computation','index_lifecycle','proof_and_rights','first_consumer','physical_cost_model','potential_falsifier','status')):e.append('B0_ORNAMENTAL_RIVAL')
    if stage in {'A1','B1'}:
        for k in ('opposite_frozen_commit','self_frozen_commit','cases','one_exchange_only'):
            if not complete(s,k):e.append('P1_MISSING_'+k)
        if s.get('one_exchange_only') is not True:e.append('EXCESS_RECIPROCAL_ROUNDS')
        for k in ('opposite_frozen_commit','self_frozen_commit'):
            if not SHA.fullmatch(str(s.get(k))):e.append('P1_BAD_COMMIT_SHA_'+k)
        if not s.get('cases') and not s.get('zero_material_case_reason'):e.append('P1_NO_CASE_OR_REASON')
    if stage=='P15':
        for k in ('A0_head','B0_head','A1_head','B1_head','frozen_material_cell_sha256','material_cells','source_or_rights_grades','actual_A_B_execution','first_consumer','positive','negative','restore','both_decision_consequences','test_category','product_delta_or_hold','comparison_reconciliation'):
            if not complete(s,k):e.append('P15_MISSING_'+k)
        for k in ('A0_head','B0_head','A1_head','B1_head'):
            if not SHA.fullmatch(str(s.get(k))):e.append('P15_UNPINNED_'+k)
        if not H64.fullmatch(str(s.get('frozen_material_cell_sha256'))):e.append('P15_BAD_FROZEN_DIGEST')
        if s.get('test_category') not in {'EXISTING_CODE_MEASUREMENT','SOURCE_SEMANTIC_INSPECTION','BOUNDED_DISPOSABLE_POC_REQUIRED','SCIENTIFIC_SOURCE_ACTOR_OWNER_HELD'}:e.append('P15_UNBOUNDED_EXP_TYPE')
        for i,c in enumerate(s.get('material_cells',[]) if isinstance(s.get('material_cells'),list) else []):
            if not isinstance(c,dict) or any(not complete(c,k) for k in ('id','workload_case_id','metric','decision_reverser','A_status','B_status','effect_on_selection','evidence_refs')):e.append('P15_INCOMPLETE_MATERIAL_CELL:'+str(i))
            elif c['A_status'] not in {'MEASURED','MODELED','UNRUN_HELD'} or c['B_status'] not in {'MEASURED','MODELED','UNRUN_HELD'}:e.append('P15_BAD_MEASURE_GRADE:'+str(i))
        if s.get('verdict') not in {'P15_MATCHED_DECISIVE_WITNESS','P15_CONDITIONAL_WITNESS','P15_UNRUN_EXACT_HOLD'}:e.append('P15_BAD_VERDICT')
        if s.get('verdict')=='P15_MATCHED_DECISIVE_WITNESS':
            for c in s.get('material_cells',[]):
                if (r6 or c.get('decision_reverser')) and (c.get('A_status')!='MEASURED' or c.get('B_status')!='MEASURED'):e.append('P15_WINNER_WITHOUT_MATCHED_BOTH_SIDES')
            if r6 and s.get('comparison_reconciliation',{}).get('status') not in {'A_DOMINATES_FULL_MATERIAL_DIMENSIONS','B_DOMINATES_FULL_MATERIAL_DIMENSIONS'}:
                e.append('R6_P15_DECISIVENESS_NOT_PROVED_BY_COMPARATOR')
            if s.get('actual_execution_grade') not in {'S2_SOURCEFREE_EXECUTED','S2_NATIVE_EXECUTED'}:e.append('P15_MEASURED_WITH_NO_EXECUTION_GRADE')
            if not s.get('runner_receipts'):e.append('P15_DECISIVE_BUT_NO_RECEIPTS')
        if r6:
            if s.get('verdict')=='P15_MATCHED_DECISIVE_WITNESS' and s.get('frozen_material_cell_sha256')!=s.get('comparison_reconciliation',{}).get('frozen_sha256'):e.append('R6_P15_FROZEN_DIGEST_NOT_RECONCILED')
            if s.get('verdict')=='P15_MATCHED_DECISIVE_WITNESS' and s.get('new_choice_reverser_holds'):e.append('R6_P15_WITH_UNRESOLVED_DISCOVERED_REVERSER')
            if s.get('verdict')=='P15_MATCHED_DECISIVE_WITNESS' and s.get('unresolved_exclusions'):e.append('R6_P15_WITH_UNREVIEWED_EXCLUSIONS')
    if stage=='C':
        for k in ('A0_head','B0_head','A1_head','B1_head','P15_head','P2_head','independent_pre_read_source_check','credible_B_rival_comparison','global_graph_verified','semantic_cross_boundary_verified','K3_row_semantics_checked','raw_physics_receipts_checked','independent_frame_challenge_review','selected_first_consumer_scope','cold_builder_witness','future_cold_builder_witness','all_material_defects','reviewer_relationship','scope_grade','limitations'):
            if k not in s:e.append('C_MISSING_'+k)
        for k in ('A0_head','B0_head','A1_head','B1_head','P15_head','P2_head'):
            if not SHA.fullmatch(str(s.get(k))):e.append('C_BAD_SHA_'+k)
        actual=s.get('cold_builder_witness',{});future=s.get('future_cold_builder_witness',{})
        grades={'SPECIFICATION_CONSTRUCTION_READY','EXECUTED_FIRST_READER_PROOF','EXACT_BUILDER_HOLD'}
        if not isinstance(actual,dict) or actual.get('status') not in grades:e.append('C_INVALID_ACTUAL_BUILDER')
        if not isinstance(future,dict) or future.get('status') not in grades:e.append('C_INVALID_FUTURE_BUILDER')
        if actual.get('handoff_id')==future.get('handoff_id'):e.append('C_ONE_COLD_BUILDER_NOT_TWO')
        if actual.get('status')=='EXECUTED_FIRST_READER_PROOF' and (not actual.get('execution_receipt') or s.get('actual_execution_grade') not in {'S2_SOURCEFREE_EXECUTED','S2_NATIVE_EXECUTED'}):e.append('C_FAKE_EXECUTED_BUILDER')
        if s.get('verdict') not in {'C_ACCEPT_SCOPED','C_ACCEPT_DOCUMENTARY_HOLD','C_REVISE_EXACT_DEFECTS','C_DECISION_BLOCKED_EXACT'}:e.append('C_INVALID_VERDICT')
        if s.get('verdict')=='C_ACCEPT_SCOPED' and (s.get('all_material_defects') or actual.get('status')=='EXACT_BUILDER_HOLD'):e.append('C_FALSE_SCOPED_ACCEPTANCE')
        if s.get('verdict')=='C_ACCEPT_DOCUMENTARY_HOLD' and not s.get('exact_decision_holds'):e.append('C_CONDITIONAL_WITHOUT_EXACT_HOLD')
        if s.get('reviewer_relationship')!='DISTINCT_NONAUTHOR_REVIEWER_SELF_REPORTED_NEEDS_HOST_CONFIRMATION':e.append('C_PRETEND_INDEPENDENCE_ACCREDITATION')
        if r6:
            if s.get('verdict')=='C_ACCEPT_SCOPED' and s.get('actual_execution_grade') in {'S0_DOCUMENTARY','S1_SOURCE_STATIC'} and actual.get('status')=='EXECUTED_FIRST_READER_PROOF':e.append('R6_C_EXECUTION_CLAIM_FROM_STATIC_REVIEW')
            if s.get('verdict')=='C_ACCEPT_SCOPED' and actual.get('status')=='SPECIFICATION_CONSTRUCTION_READY':
                for field in ('producer_symbol','consumer_symbol','test_command','source_cut','scoped_input_output_abi'):
                    v=actual.get(field)
                    if not isinstance(v,str) or len(v)<12 or any(q in v.lower() for q in ('to be specified','unknown current','placeholder','future engineer')):
                        e.append('R6_C_SPECIFICATION_NOT_ACTUALLY_BUILDER_USABLE:'+field)
            objection=s.get('strongest_surviving_architecture_objection')
            if s.get('verdict')=='C_ACCEPT_SCOPED':
                if not isinstance(objection,dict) or objection.get('could_reverse') not in {'YES','NO'}:e.append('R6_C_MISSING_STRONGEST_SURVIVING_OBJECTION')
                elif objection['could_reverse']=='YES':e.append('R6_C_ACCEPTS_DESPITE_CHOICE_REVERSER')
                elif not isinstance(objection.get('why_not_reversing'),str) or len(objection['why_not_reversing'])<40:e.append('R6_C_UNSUPPORTED_NO_REVERSER')
            if s.get('verdict')=='C_ACCEPT_SCOPED' and s.get('excluded_workload_challenges_unresolved'):
                e.append('R6_C_ACCEPTS_WITH_UNRESOLVED_EXCLUSION')

    if stage=='H1':
        for k in ('C_review_head','A_P2_head','owner_authority_grade','paired_current_progress_result','C_verdict','C_cold_builder_verdict','C_first_consumer_scope','product_advance_grade','commission_complete_YN','architecture_decidable_YN','engineering_accepted_YN','scientific_granted_YN','source_rights_granted_YN','actor_granted_YN','protected_received_YN'):
            if not complete(s,k):e.append('H1_MISSING_'+k)
        for k in ('C_review_head','A_P2_head'):
            if not SHA.fullmatch(str(s.get(k))):e.append('H1_UNPINNED_'+k)
        bools=['commission_complete_YN','architecture_decidable_YN','engineering_accepted_YN','scientific_granted_YN','source_rights_granted_YN','actor_granted_YN','protected_received_YN']
        for k in bools:
            if s.get(k) not in {'YES','NO'}:e.append('H1_NOT_BINARY_'+k)
        if s.get('verdict') not in {'H1_RECEIVED_SCOPED','H1_RECEIVED_CONDITIONAL','HQ_CURRENTNESS_HOLD'}:e.append('H1_BAD_VERDICT')
        received=s.get('verdict') in {'H1_RECEIVED_SCOPED','H1_RECEIVED_CONDITIONAL'}
        if received and (s.get('owner_authority_grade')!='VERIFIED_COMPETENT_OWNER' or s.get('paired_current_progress_result')!='AUTHENTICATED_CAS_RECEIVED'):e.append('H1_RECEIVING_WITH_NO_AUTHORITY_OR_CAS')
        if s.get('verdict')=='H1_RECEIVED_SCOPED':
            if s.get('commission_complete_YN')!='YES' or s.get('architecture_decidable_YN')!='YES' or s.get('C_verdict')!='C_ACCEPT_SCOPED':e.append('H1_FALSE_SCOPED_RECEIVING_TRUTH_TABLE')
            if s.get('C_cold_builder_verdict')=='EXACT_BUILDER_HOLD':e.append('H1_HELD_BUILDER_FALSE_SCOPED')
        if s.get('verdict')=='H1_RECEIVED_CONDITIONAL':
            if s.get('product_advance_grade') not in {'INDEPENDENTLY_VERIFIED_MATERIAL_DELTA','INDEPENDENTLY_VERIFIED_NARROWER_EXECUTABLE_BLOCKER'}:e.append('H1_PAPERWORK_ONLY_CONDITIONAL_ACCEPTANCE')
            if s.get('commission_complete_YN')!='YES' or s.get('architecture_decidable_YN')!='NO' or s.get('C_verdict')!='C_ACCEPT_DOCUMENTARY_HOLD' or not complete(s,'exact_decision_blocker'):e.append('H1_FALSE_CONDITIONAL_RECEIVING')
        if s.get('engineering_accepted_YN')=='YES' and (s.get('C_cold_builder_verdict')!='EXECUTED_FIRST_READER_PROOF' or s.get('C_verdict')!='C_ACCEPT_SCOPED'):e.append('H1_ENGINEERING_WITHOUT_EXECUTED_FIRST_READER')
        if s.get('verdict')=='HQ_CURRENTNESS_HOLD' and not complete(s,'exact_currentness_gaps'):e.append('H1_VAGUE_HOLD')
        if s.get('protected_received_YN')=='YES' and s.get('paired_current_progress_result')!='AUTHENTICATED_CAS_RECEIVED':e.append('H1_FAKE_PROTECTED_RECEIVING')
        if r6:
            exact={'SPECIFICATION_CONSTRUCTION_READY','EXECUTED_FIRST_READER_PROOF','EXACT_BUILDER_HOLD'}
            if s.get('C_cold_builder_verdict') not in exact:e.append('R6_H1_UNRECOGNIZED_BUILDER_GRADE')
            if received and s.get('protected_received_YN')!='YES':e.append('R6_H1_RECEIVED_WITH_PROTECTED_NO')
            if received and s.get('paired_current_progress_result')!='AUTHENTICATED_CAS_RECEIVED':e.append('R6_H1_RECEIVED_WITHOUT_PAIRED_CAS')
            if received and s.get('C_first_consumer_scope') not in {'C11_QUERY_DESIGN','F1_F4_CONSUMER_DESIGN','FF_FIRST_EFFECT_DESIGN'}:e.append('R6_H1_UNRECOGNIZED_FIRST_CONSUMER_SCOPE')
            if received:
                receipt=s.get('authenticated_C_receipt',{})
                if not isinstance(receipt,dict) or receipt.get('C_head')!=s.get('C_review_head') or receipt.get('C_verdict')!=s.get('C_verdict') or receipt.get('builder_verdict')!=s.get('C_cold_builder_verdict') or receipt.get('first_consumer_scope')!=s.get('C_first_consumer_scope'):
                    e.append('R6_H1_C_GRADE_NOT_MATCHED_TO_C_RECEIPT')
                elif evidence_root is None:e.append('R6_H1_NO_EXTERNAL_C_RECEIPT_READBACK')
                else:
                    root=pathlib.Path(evidence_root).resolve();file=(root/receipt.get('path','')).resolve()
                    if not file.is_relative_to(root) or not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest()!=receipt.get('sha256'):
                        e.append('R6_H1_C_RECEIPT_BYTES_NOT_AUTHENTICATED')

    return sorted(set(e))

def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=sorted(STAGES));p.add_argument('path');p.add_argument('--evidence-root');a=p.parse_args()
    try:r=json.loads(pathlib.Path(a.path).read_text());e=check(a.stage,r,a.evidence_root)
    except (OSError,ValueError,TypeError,AttributeError,KeyError) as ex:e=['UNREADABLE_OR_MALFORMED:'+type(ex).__name__+':'+str(ex)]
    print(json.dumps({'status':'PASS_STRUCTURE_ONLY_NOT_AUTHENTICATED' if not e else 'RED','errors':e},indent=2));return 0 if not e else 2
if __name__=='__main__':sys.exit(main())
