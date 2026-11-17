#!/usr/bin/env python3
"""R6 hostile mutations + positive numeric comparison, not source-native scientific proof."""
import copy,hashlib,json,pathlib,sys,tempfile,shutil
from test_r5 import fixture,description
from anvil import validate
from r6_comparator import r6_full_comparison, POLICY,digest
from check_stage import check
ROOT=pathlib.Path(__file__).resolve().parents[1]
P=hashlib.sha256((ROOT/'20_R6_MATERIAL_DECISION_CONSTITUTION.json').read_bytes()).hexdigest()
E='7fc00289dd801d2d0a8ce159986c7595fc27a4d9'

def r6_fixture():
    s=fixture();s['schema']='ANVIL_SPINE_R6';s['r6_material_policy_sha256']=P
    s['novel_source_meaning_probe']={k:description('Sourcefree unseen lexical ambiguity '+k) for k in ('source_identity','new_unanticipated_ambiguity','source_design_vs_respondent_answer','first_consumer','positive','forbidden_promotion','restoration','evidence_receipt_or_exact_owner_hold')}
    for r in s['observability_provenance']['cases']:
        r['target_unit']=r['facets']['unit']
    return s

def numeric_fixture():
    frozen={'schema':'ANVIL_R6_FROZEN_MATERIAL_CELLS','material_floor_sha256':P,'cells':[],'exclusions':[],'discovered_discriminators':[]}
    for case,metrics in POLICY['metric_floor_by_case'].items():
        for metric in metrics:
            cid=case+'_'+metric
            frozen['cells'].append({'id':cid,'workload_case_id':case,'metric':metric,'source_cut':'7fc00289dd801d2d0a8ce159986c7595fc27a4d9','source_grade':'SOURCEFREE_SYNTHETIC','fixture_id':'sourcefree_100k_full_width','runner_id':'host_exact_fixture','input_identity':'same questionnaire and qualified form denominator','runner_identity':'same matched physical executor','negative_restore_oracle':'denied and restored before chosen first consumer','decision_reversal_if_A':'A violates the limit or consumes more end to end','decision_reversal_if_B':'B violates the limit or consumes more end to end','required_claim_grade':'S2_SOURCEFREE_EXECUTED'})
    measurements=[]
    for c in frozen['cells']:
        entry={k:c[k] for k in ('source_cut','source_grade','fixture_id','runner_id')}
        entry.update(cell_id=c['id'],A={'status':'MEASURED','value':10,'low':9,'high':11,'receipt_path':'a_'+c['id'],'receipt_sha256':'a'*64},B={'status':'MEASURED','value':20,'low':19,'high':21,'receipt_path':'b_'+c['id'],'receipt_sha256':'b'*64})
        measurements.append(entry)
    data={'schema':'ANVIL_R6_COMPARATOR_INPUT','candidate_ids':['A','B'],'frozen_sha256':digest(frozen),'hard_vetoes':{'A':[],'B':[]},'hard_veto_checks':[{'id':i,'status':'PASS_AT_CLAIMED_SCOPE','evidence_ref':'sourcefree synthetic fixture no original survey','receipt_path':'veto_'+i,'receipt_sha256':'c'*64} for i in POLICY['required_non_numeric_vetoes']],'measurements':measurements}
    return data,frozen

def main():
    out={};s=r6_fixture();assert not validate(s),validate(s)
    def attack(label,fn,marker):
        t=copy.deepcopy(s);fn(t);es=validate(t)
        assert any(marker in e for e in es),(label,es[:15]);out[label]=next(e for e in es if marker in e)
    attack('false_unobserved_original',lambda x:(x['observability_provenance']['cases'][0]['facets'].update(asked='YES',released='YES',eligibility='ELIGIBLE',observation='NOT_OBSERVED',source_status='OBSERVED_INSTRUMENT_CONSEQUENCE',claim_kind='ORIGINAL_OBSERVATION'),x['observability_provenance']['cases'][0].update(legal_claim_kind='ORIGINAL_OBSERVATION')),'NONVALUE_TO_ORIGINAL_OBSERVATION')
    attack('fiction_as_original',lambda x:(x['observability_provenance']['cases'][0]['facets'].update(asked='YES',released='YES',eligibility='ELIGIBLE',observation='VALUE',source_status='MODEL_OR_FICTION',claim_kind='ORIGINAL_OBSERVATION'),x['observability_provenance']['cases'][0].update(legal_claim_kind='ORIGINAL_OBSERVATION')),'UNISSUED_SOURCE_TO_ORIGINAL_OBSERVATION')
    attack('unattributed_household',lambda x:x['observability_provenance']['cases'][1].pop('target_unit'),'R6_MISSING_EXPLICIT_TARGET_GRAIN')
    attack('source_to_C11_future_path',lambda x:x['architecture'].update(future_reference_path=['SRC','C11']),'R6_FUTURE_REFERENCE_PATH_STOPS_BEFORE_PERSON')
    attack('world_actor_degenerated',lambda x:next(r for r in x['future_interface_routes'] if r['id']=='WORLD_TO_ACTOR').update(node_ids=['SRC','C11']),'R6_FUTURE_ROUTE_WRONG_TARGET_DOMAIN')
    attack('exogenous_cast_as_actor',lambda x:next(r for r in x['future_interface_routes'] if r['id']=='EXOGENOUS_WORLD_HISTORY').update(node_ids=['ACTOR','ACT']),'R6_FUTURE_ROUTE_WRONG_TARGET_DOMAIN')
    attack('blindspot_all_NA',lambda x:[r.update(ancestry_A_status='NOT_APPLICABLE') for r in x['epistemic_case']['steps']],'R6_ALL_BOUNDARIES_WAIVED_OBSERVABILITY')
    attack('missing_novel_case',lambda x:x.pop('novel_source_meaning_probe'),'R6_MISSING_NOVEL_SOURCE_MEANING_PROBE')
    data,frozen=numeric_fixture()
    runner_root=pathlib.Path(tempfile.mkdtemp(prefix='anvil_r6_synthetic_'))
    for m in data['measurements']:
        for side in ('A','B'):
            name=m[side]['receipt_path'];contents=json.dumps({'synthetic':True,'side':side,'cell':m['cell_id']}).encode()
            (runner_root/name).write_bytes(contents);m[side]['receipt_sha256']=hashlib.sha256(contents).hexdigest()
    for v in data['hard_veto_checks']:
        contents=json.dumps({'synthetic':True,'veto':v['id']}).encode()
        (runner_root/v['receipt_path']).write_bytes(contents);v['receipt_sha256']=hashlib.sha256(contents).hexdigest()
    r=r6_full_comparison(data,frozen,evidence_root=runner_root)
    assert r['status']=='A_DOMINATES_FULL_MATERIAL_DIMENSIONS' and r['winner']=='A',r
    out['full_positive_numeric']='A_DOMINATES_FULL_MATERIAL_DIMENSIONS'
    def cattack(label,fn,expected):
        a=copy.deepcopy(data);b=copy.deepcopy(frozen);fn(a,b)
        v=r6_full_comparison(a,b,evidence_root=runner_root)
        assert v['status']==expected,(label,v)
        out[label]=v['status']
    cattack('false_all_build_only',lambda a,b:(b.update(cells=[c for c in b['cells'] if c['metric']=='build_wall_s'],exclusions=[]),a.update(measurements=[x for x in a['measurements'] if 'build_wall_s' in x['cell_id']],frozen_sha256=digest(dict(b,cells=[c for c in b['cells'] if c['metric']=='build_wall_s'],exclusions=[])))),'RED')
    def exclude_six(a,b):
        rest=b['cells'][:1];excluded=[c for c in b['cells'] if c not in rest]
        b['cells']=rest;b['exclusions']=[{'workload_case_id':c['workload_case_id'],'metric':c['metric'],'B_challenge_status':'INDEPENDENT_B_NONREVERSING_WITH_EVIDENCE','reason_not_material':description('Bounded reason scoped original compared workload'),'bounded_reversal_argument':description('If this changes candidate ranking the claimed scope must be held'),'first_consumer_impact':description('Consumer receives declared narrowed query and source rights'),'B_evidence_ref':description('Independent B source-static objection read and pinned'),'C_adjudication_required':description('Independent C must verify this before owner receiving'),'scope_effect':description('Specific material workload dimension excluded from physical claim')} for c in excluded]
        a['measurements']=a['measurements'][:1];a['frozen_sha256']=digest(b)
    cattack('six_exclusions_not_dominance',exclude_six,'EXCLUSIONS_REQUIRE_C_INDEPENDENT_COURT')
    cattack('digest_missing',lambda a,b:a.pop('frozen_sha256'),'RED')
    cattack('B_missing',lambda a,b:a['measurements'][0]['B'].update(status='UNRUN_HELD'),'MISSING_DECISIVE_EVIDENCE')
    cattack('one_overlap_no_tiebreak',lambda a,b:(a['measurements'][0]['A'].update(low=8,value=15,high=22)),'PARETO_NONDECISIVE')
    cattack('hard_veto_unknown',lambda a,b:a['hard_veto_checks'][0].update(status='HELD_WITH_EXACT_OWNER'),'HARD_VETO_UNPROVED')
    cattack('true_B_superiority',lambda a,b:[(m['A'].update(value=20,low=19,high=21),m['B'].update(value=10,low=9,high=11)) for m in a['measurements']],'B_DOMINATES_FULL_MATERIAL_DIMENSIONS')
    stage_common={'schema':'ANVIL_STAGE_R6','repository':'maidiu/rawlsing','source_cut':E,'artifact_scope':'sourcefree first reader only','author_role':'scoped sourcefree reviewer','sources_checked':['exact hypothetical fixture'], 'actual_execution_grade':'S0_DOCUMENTARY','own_output_path':'stage.json','stage':'H1', 'C_review_head':E,'A_P2_head':E,'owner_authority_grade':'VERIFIED_COMPETENT_OWNER','paired_current_progress_result':'AUTHENTICATED_CAS_RECEIVED','C_verdict':'C_ACCEPT_SCOPED','C_cold_builder_verdict':'SPECIFICATION_CONSTRUCTION_READY','C_first_consumer_scope':'C11_QUERY_DESIGN','product_advance_grade':'INDEPENDENTLY_VERIFIED_MATERIAL_DELTA','commission_complete_YN':'YES','architecture_decidable_YN':'YES','engineering_accepted_YN':'NO','scientific_granted_YN':'NO','source_rights_granted_YN':'NO','actor_granted_YN':'NO','protected_received_YN':'NO','verdict':'H1_RECEIVED_SCOPED'}
    v=check('H1',stage_common)
    assert 'R6_H1_RECEIVED_WITH_PROTECTED_NO' in v,v
    stage_common['protected_received_YN']='YES';stage_common['C_cold_builder_verdict']='UNRECOGNIZED_INDETERMINATE';v=check('H1',stage_common)
    assert 'R6_H1_UNRECOGNIZED_BUILDER_GRADE' in v,v
    stage_common['C_cold_builder_verdict']='SPECIFICATION_CONSTRUCTION_READY';v=check('H1',stage_common)
    assert 'R6_H1_C_GRADE_NOT_MATCHED_TO_C_RECEIPT' in v,v
    out['H1_unrecognized_and_receipt_holds']='REJECTED'
    shutil.rmtree(runner_root)
    print(json.dumps({'status':'PASS_R6_STRUCTURAL_SYNTHETIC_NOT_AUTHENTICATED','count':len(out),'cases':out},indent=2))
if __name__=='__main__':main()
