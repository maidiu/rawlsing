#!/usr/bin/env python3
"""Stage-format sabotage, not independent source review."""
import copy,json
from check_stage import check
S='7fc00289dd801d2d0a8ce159986c7595fc27a4d9'
common={'schema':'ANVIL_STAGE_R5','repository':'maidiu/rawlsing','source_cut':S,'artifact_scope':'synthetic no original rights','author_role':'synthetic C external agent','sources_checked':['synthetic://test'], 'actual_execution_grade':'S0_DOCUMENTARY','own_output_path':'C.json','verdict':'C_ACCEPT_DOCUMENTARY_HOLD','stage':'C'}
c=common|{'A0_head':S,'B0_head':S,'A1_head':S,'B1_head':S,'P15_head':S,'P2_head':S,'independent_pre_read_source_check':'test only','credible_B_rival_comparison':'test only','global_graph_verified':'test only','semantic_cross_boundary_verified':'test only','K3_row_semantics_checked':'test only','raw_physics_receipts_checked':'not run','independent_frame_challenge_review':'test only','selected_first_consumer_scope':'C11_QUERY_DESIGN','cold_builder_witness':{'status':'EXACT_BUILDER_HOLD','handoff_id':'HD-T1'},'future_cold_builder_witness':{'status':'EXACT_BUILDER_HOLD','handoff_id':'HD-T6'},'all_material_defects':[],'reviewer_relationship':'DISTINCT_NONAUTHOR_REVIEWER_SELF_REPORTED_NEEDS_HOST_CONFIRMATION','scope_grade':'S0_DOCUMENTARY','limitations':'no actual cold builder','exact_decision_holds':['A/B measurements held']}
assert not check('C',c),check('C',c)
negative={}
def attack(k,obj,needle):
    es=check(obj['stage'],obj);assert any(needle in x for x in es),(k,es);negative[k]=es[:3]
x=copy.deepcopy(c);x['verdict']='C_ACCEPT_SCOPED';attack('C_held_cannot_accept',x,'C_FALSE_SCOPED_ACCEPTANCE')
x=copy.deepcopy(c);x['future_cold_builder_witness']['handoff_id']='HD-T1';attack('C_only_one_builder_sample',x,'C_ONE_COLD_BUILDER_NOT_TWO')
x=copy.deepcopy(c);x['cold_builder_witness']['status']='EXECUTED_FIRST_READER_PROOF';attack('C_forged_runner',x,'C_FAKE_EXECUTED_BUILDER')
h=common|{'stage':'H1','verdict':'HQ_CURRENTNESS_HOLD','C_review_head':S,'A_P2_head':S,'owner_authority_grade':'NOT_VERIFIED','paired_current_progress_result':'HOLD','C_verdict':'C_ACCEPT_DOCUMENTARY_HOLD','C_cold_builder_verdict':'EXACT_BUILDER_HOLD','C_first_consumer_scope':'C11_QUERY_DESIGN','product_advance_grade':'NO_NEW_PRODUCT_ADVANCE','commission_complete_YN':'NO','architecture_decidable_YN':'NO','engineering_accepted_YN':'NO','scientific_granted_YN':'NO','source_rights_granted_YN':'NO','actor_granted_YN':'NO','protected_received_YN':'NO','exact_currentness_gaps':['No owner writer lease']}
assert not check('H1',h),check('H1',h)
x=copy.deepcopy(h);x['verdict']='H1_RECEIVED_SCOPED';attack('H1_undecidable_but_received',x,'H1_FALSE_SCOPED_RECEIVING_TRUTH_TABLE')
x=copy.deepcopy(h);x.update(verdict='H1_RECEIVED_SCOPED',commission_complete_YN='YES',architecture_decidable_YN='YES',C_verdict='C_ACCEPT_SCOPED',C_cold_builder_verdict='SPECIFICATION_CONSTRUCTION_READY');attack('H1_no_owner_or_CAS',x,'H1_RECEIVING_WITH_NO_AUTHORITY_OR_CAS')
x=copy.deepcopy(h);x.update(verdict='H1_RECEIVED_CONDITIONAL',commission_complete_YN='YES',architecture_decidable_YN='NO',C_verdict='C_ACCEPT_DOCUMENTARY_HOLD',exact_decision_blocker='Matched A/B full 100k disjoint proof remains held',owner_authority_grade='VERIFIED_COMPETENT_OWNER',paired_current_progress_result='AUTHENTICATED_CAS_RECEIVED');attack('H1_no_new_product_advance',x,'H1_PAPERWORK_ONLY_CONDITIONAL_ACCEPTANCE')
x=copy.deepcopy(h);x.update(engineering_accepted_YN='YES');attack('H1_engineering_no_execution',x,'H1_ENGINEERING_WITHOUT_EXECUTED_FIRST_READER')
# P15 unmeasured B cannot declare decisive test
p=common|{'stage':'P15','verdict':'P15_MATCHED_DECISIVE_WITNESS','A0_head':S,'B0_head':S,'A1_head':S,'B1_head':S,'frozen_material_cell_sha256':'a'*64,'material_cells':[{'id':'X1','workload_case_id':'W-O','metric':'query_100_wall_s','decision_reverser':True,'A_status':'MEASURED','B_status':'UNRUN_HELD','effect_on_selection':'B could outperform','evidence_refs':['fixture://one']}],'source_or_rights_grades':'sourcefree held','actual_A_B_execution':'A measured only','first_consumer':'I03 selected saved reader','positive':'A fact','negative':'deny','restore':'restore','both_decision_consequences':'B may win or not','test_category':'EXISTING_CODE_MEASUREMENT','product_delta_or_hold':'specific missing B runner','comparison_reconciliation':'no full result','runner_receipts':['sourcefree:test'], 'actual_execution_grade':'S2_SOURCEFREE_EXECUTED'}
attack('P15_B_unmeasured_decisive_false',p,'P15_WINNER_WITHOUT_MATCHED_BOTH_SIDES')
print(json.dumps({'status':'PASS_STAGE_SYNTHETIC_ONLY','rejected':negative,'count':len(negative)},indent=2))
