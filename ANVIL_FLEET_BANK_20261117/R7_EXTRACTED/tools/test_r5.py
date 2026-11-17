#!/usr/bin/env python3
"""R5 synthetic adversarial tests. GREEN never claims live source, architecture correctness, or owner accreditation."""
import copy,hashlib,json,pathlib,tempfile,sys
from anvil import ROOT,MAN,BC,BOUND,DIMS,validate,outputs,check_dir
from check_stage import check as stage_check
from compare_candidates import full_comparison
from r5_contract import CASES,PROV

def description(s):return s+' — test-only proposed contract with exact negative and independent qualified receiving held.'
def fixture():
    sha=MAN['snapshot_sha'];evid=['SYNTHETIC-S0']
    cov={}
    for g,ids in MAN['mandatory'].items():
        cov[g]={}
        for rid in ids:
            hist=g in MAN['k3_files'];pre='HISTORICAL_NOT_ADOPTED' if g=='PYAT_PC' else 'HISTORICAL_PROOF_HELD' if g=='P4R' else 'MUST_ALLOW_FUTURE'
            rec={'necessity':pre,'status':'PRESERVE_WITHOUT_BUILD','source_anchor':description('Inherited historical source anchor '+rid),'source_semantics':description('Source meaning kept through original evidence ID '+rid),'consumer_or_hold':description('Exact actual or planned owner deliberately held '+rid),'negative_meaning':description('Never silently upgrade missing scientific or release meaning'), 'architecture_effect':description('No current physical architecture is selected at this sourcefree grade'),'evidence_ids':evid,'why':description('Evidence-grade conditional only, preserve original source semantics'),'decision_ids':['DK-PRESERVE'],'assessment_tier':'INHERITED_TYPED_REFERENCE'}
            if hist:rec.update(original_source_blob=MAN['k3_files'][g]['blob'],row_sha256='d'*64)
            if g=='PYAT_PC':rec.update(adopted=False)
            if g=='P4R':rec.update(closed=False)
            cov[g][rid]=rec
    ins={'lossless_source':'PASS_AT_SCOPE','scientific_claims':'PASS_AT_SCOPE','rights_and_fail_closed':'PASS_AT_SCOPE','true_joint':'UNPROVED_HELD','global_composition':'PASS_AT_SCOPE','rss_budget':'UNPROVED_HELD'}
    alt=lambda i,origin,state:{'id':i,'origin':origin,'status':state,'physical_arrangement':description('Candidate physical arrangement '+i),'source_preservation':description('Conserves all thirteen original family structures '+i),'preparation_reuse':description('Separate prepared respondent-level condition and query lifecycles '+i),'first_consumer':description('Native query actual or planned first reader '+i),'future_interfaces':description('No forced future actor science; typed FF/world access '+i),'cost_risks':description('Unknown 100k-wide dense and disjoint costs, test required '+i),'evidence_ids':evid,'elimination_or_selection_reason':description('Conditional initial comparison and no final accepted winner '+i)}
    def decision(did,cls,alts,sel,node,maturity=None):
        d={'id':did,'class':cls,'question':description('Find minimal evidence-preserving design at current scope '+did),'first_consumer':description('Exact next intended owner and first reader '+did),'criterion':description('No scientific source right/meaning violation allowed '+did),'alternatives':alts,'selected':sel,'discriminators':[{'id':did+'-D1','raised_by':'B_P0','outcome_if_a':description('Incumbent proves adequate on matching sourcewidth'), 'outcome_if_b':description('Rival proves decisive savings or correctness'), 'status':'PENDING','smallest_test':description('Bounded matching sourcefree query and neg restoration'), 'evidence_ids':evid,'competent_owner':description('Separate reader and compiler owner'), 'physical_or_semantic':'PHYSICAL'}],'invariants':dict(ins),'evidence_ids':evid,'global_node_ids':node,'comparison_summary':description('Both candidate arrangements remain test-only conditional and unselected scientifically'), 'no_material_rival_reason':description('Non-physical future science is independently held rather than rebuilt')}
        if maturity:d['maturity']=maturity
        return d
    nodes=[
     ('SRC','OBSERVED','DK-PRESERVE','P-A',['external_right'],['original']),
     ('C11','OBSERVED','DK-PHYSICAL','A-P',['original'],['canonical']),
     ('QUERY','DESCRIPTIVE_MODELED','DK-PHYSICAL','A-P',['canonical'],['stat']),
     ('FIELD','DESCRIPTIVE_MODELED','DK-FUTURE','F-P',['stat'],['field']),
     ('EXT','EXTERNAL_OBSERVED','DK-PRESERVE','P-A',[],['external_struct']),
     ('STRUCT','STRUCTURAL_QUALIFIED','DK-FUTURE','F-P',['field','external_struct'],['material']),
     ('WORLD','FICTIONAL_WORLD','DK-FUTURE','F-P',['material'],['world_event','event_state']),
     ('ACTOR','ACTOR_STATE','DK-FUTURE','F-P',['event_state'],['act']),
     ('ACT','HISTORY_EVENT','DK-FUTURE','F-P',['act','world_event'],['enacted']),
     ('WORLD_NEXT','FICTIONAL_WORLD','DK-FUTURE','F-P',['enacted'],['next_world']),
    ]
    graphnodes=[{'id':n,'domain':dom,'owner':description('Actual or held owner for '+n),'input_types':inp,'output_types':out,'implementation':description('Source-static illustrative interface, not an executing implementation '+n),'decision_id':did,'alternative_id':altid} for n,dom,did,altid,inp,out in nodes]
    pairs=[
      ('SRC','C11','original','T1','CANONICAL_PRESERVE','SOURCE_CERTIFIED','SOURCE_TIME_FIXED'),
      ('C11','QUERY','canonical','T2','DESCRIPTIVE_INFERENCE','SCIENCE_GRADED','SOURCE_TIME_FIXED'),
      ('QUERY','FIELD','stat','T3','DERIVED_ANALYSIS','SCIENCE_GRADED','SOURCE_TIME_FIXED'),
      ('FIELD','STRUCT','field','T4','INDEPENDENT_STRUCTURAL_ADDITION','EXTERNAL_STRUCTURAL_ISSUER','HISTORICAL_AS_OF_QUALIFIED'),
      ('EXT','STRUCT','external_struct','T4','INDEPENDENT_STRUCTURAL_ADMISSION','EXTERNAL_STRUCTURAL_ISSUER','HISTORICAL_AS_OF_QUALIFIED'),
      ('STRUCT','WORLD','material','T5','WORLD_OPPORTUNITY','WORLD_PARTICULARIZER','FICTIONAL_BRANCH_OWNED'),
      ('WORLD','ACTOR','event_state','T6','ACTOR_ACCESS','ACTOR_OWNER_GRANTED','FICTIONAL_EVENT_ACCESS_QUALIFIED'),
      ('ACTOR','ACT','act','T7','PERFORMED_ACT','ACTOR_OWNER_GRANTED','FORWARD_FICTIONAL_TIME'),
      ('WORLD','ACT','world_event','T7','EXOGENOUS_WORLD_EVENT','WORLD_PARTICULARIZER','FORWARD_FICTIONAL_TIME'),
      ('ACT','WORLD_NEXT','enacted','T7','SHARED_WORLD_EFFECT','WORLD_PARTICULARIZER','FORWARD_FICTIONAL_TIME'),
    ]
    edges=[{'id':f'E{i+1}','from':a,'to':b,'data_type':typ,'boundary':bound,'transition_class':tc,'authority_grade':ag,'temporal_mode':tm,'negative':description('Invalid attribution or history refuses'),'invalidation_rule':description('Change to source, rights or event root invalidates only authorized derived outputs'), 'strict_time_guard':'t_event_new > t_committed_previous' if tm=='FORWARD_FICTIONAL_TIME' else ''} for i,(a,b,typ,bound,tc,ag,tm) in enumerate(pairs)]
    boundaries={}
    for name,base in BOUND.items():
        boundaries[name]={'contract_name':base['name'],'first_consumer':description(base['receivers']),'positive':description('Legal origin changes real/planned reader'), 'negative':description('Source meaning/owner denied has typed refused state'),'restore':description('Exact original source and condition yields original result'),'graph_edge_ids':[x['id'] for x in edges if x['boundary']==name],'status':'SOURCE_STATIC_CONSERVED','owner':description(base['owners']),'evidence_ids':evid}
    epi={'fixture_description':description('Synthetic two instruments with different administered item histories'),'instrument_A_ancestry':'NOT_ASKED','instrument_B_ancestry':'NOT_COMPARABLE','true_three_way_joint':True,'material_evidence_independent':True,'steps':[{'boundary':k,'input':description('Correct source and modeled previous state'),'output':description('State preserves previously typed source claim'), 'ancestry_A_status':'NOT_OBSERVED','positive':description('Only admitted statement passes'),'negative':description('Not asked is not a measured zero'),'restore':description('Restore original input and result'),'real_consumer_or_hold':description('Real reader for T1/T2, otherwise expressly held'),'evidence_ids':evid,'grade':'S1_SOURCE_STATIC'} for k in BOUND],'test_grade':'SOURCE_STATIC_ONLY','negative_observability_result':description('Never infer unobserved sect absence as empirical zero'),'restore_result':description('Exact source qualified state recovers original outputs'),'source_vs_fictional_separation':description('World event and actor assertions never rewrite original questionnaire corpus')}
    workload={'locked_scenario':description('Fixed 100k sourcefree representative questionnaire, not real native benchmark'),'respondents':100000,'question_opportunities':690,'cold_distinct_operations':[1,10,100], 'rss_ceiling_bytes':6442450944,'source_width_grade':'UNRUN_SOURCEFREE_REPRESENTATIVE','measures':[{'dimension':dim,'kind':'NOT_RUN','candidate_values':{'A':None,'B':None},'evidence_ids':evid,'discriminator_effect':description('Waiting for matching test with rights and scientific function')} for dim in sorted(DIMS)],'comparison_preference':description('No material winner yet, preserve accepted code until measured rival advantage')}
    handoffs=[]
    for k in BOUND:
        handoffs.append({'id':'HD-'+k,'boundary':k,'recipient_owner':description('Appropriate scoped producer and consumer owner for '+k),'producer_symbol':description('Source static spec, exact symbol held by owner '+k),'producer_cut':'7fc00289dd801d2d0a8ce159986c7595fc27a4d9','consumer_symbol':description('Future or actual first reader held until qualified '+k),'consumer_status':'HELD','input_abi':description('Typed source, missing, risk and clock fields required for '+k),'output_abi':description('Qualified data or right refusal, with source and time lineage '+k),'transformation':description('No automatic uplift of measurement to independent actor claim'),'negative':description('Forbidden value and missing source refuse'),'restore':description('Restored legal input produces original version-bound result'),'test_command':description('To be specified by owner, no execution authorization from test fixture'),'expected_first_effect':description('Exactly one qualified producer result changes first consumer'),'source_authority':description('Appropriate independent source or scientific owner required'),'implementation_status':'SPECIFIED_OWNER_HELD','required_now_or_future':'MUST_ALLOW_FUTURE','dependencies':[],'evidence_ids':evid})
    policyhash={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['12_ORIGINAL_MANDATE_AND_DECISION_LEVERAGE.md','13_WORKLOAD_AND_DISCRIMINATORS.json','14_AUTHORITY_TRANSITION_MATRIX.json','15_OBSERVABILITY_PROVENANCE_CONTRACT.json','17_R5_DECISION_AND_TERMINAL_GATES.md']}
    cases=[]
    orig=[('ANCESTRY_OR_SECT_NOT_OBSERVED','NO','NO','NOT_OBSERVED','PERSON','SELF','UNRECONCILED','NO_SUBSTANTIVE_CLAIM','DOCUMENTED_DESIGN'),('HOUSEHOLD_VS_PERSON_GRAIN','YES','YES','VALUE','HOUSEHOLD','ADMINISTRATIVE','SAME_INSTRUMENT','QUALIFIED_DESCRIPTIVE','OBSERVED_INSTRUMENT_CONSEQUENCE'),('INTERVIEWER_VS_SELF','YES','YES','VALUE','PERSON','INTERVIEWER','SAME_INSTRUMENT','QUALIFIED_DESCRIPTIVE','OBSERVED_INSTRUMENT_CONSEQUENCE'),('TRANSLATION_OR_WAVE_NONCOMPARABLE','YES','YES','VALUE','PERSON','SELF','UNRECONCILED','QUALIFIED_DESCRIPTIVE','SCIENTIFIC_INTERPRETATION')]
    for k,asked,released,observation,unit,attr,trans,claimkind,sourcestatus in orig:
        cases.append({'case_id':k,'facets':{'eligibility':'ELIGIBLE' if asked=='YES' else 'UNKNOWN_HELD','asked':asked,'released':released,'observation':observation,'unit':unit,'attribution':attr,'translation':trans,'claim_kind':claimkind,'source_status':sourcestatus},'instrument_id':'synthetic_wvs_or_arabbar_source','country':'SYNTHETIC','wave':'SOURCEFREE-W0','question_id':'SY-Q123','unit_id_or_risk_set':'synthetic_respondent_or_household','source_ref':description('Test-only questionnaire, no original source rights'),'source_grade':'S0_DOCUMENTARY','legal_claim_kind':claimkind,'first_consumer':'I03_testonly_or_ownerheld','negative':'An original respondent claim must not be constructed out of absent information','restore':'Restore exact source and show source-based result','evidence_ids':evid})
    # Need full nontrivial K3 inventory but no deep new interpretations for inherited rows
    s={'schema':'ANVIL_SPINE_R5','baseline_sha':sha,'outcome':'CONDITIONAL_CANDIDATE','verdict_reason':description('A/B remains undecided; all sourcefree future and original source authority are held'),'decision_constitution_sha256':hashlib.sha256((ROOT/'01_DECISION_CONSTITUTION.md').read_bytes()).hexdigest(),'boundary_contract_sha256':hashlib.sha256((ROOT/'02_BOUNDARY_CONTRACTS.json').read_bytes()).hexdigest(),'r5_policy_hashes':policyhash,'evidence':[{'id':'SYNTHETIC-S0','grade':'DOCUMENTARY','locator':'sourcefree:test_r5 fixture','claim':description('No source/science/actor grant, test only'),'verification_status':'UNVERIFIED_HELD'}], 'coverage':cov,'boundaries':boundaries,'decisions':[decision('DK-PRESERVE','PRESERVE',[alt('P-A','A_INCUMBENT','SELECTED')],'P-A',['SRC','EXT']),decision('DK-PHYSICAL','PHYSICAL',[alt('A-P','A_INCUMBENT','SELECTED'),alt('B-P','B_INDEPENDENT','VIABLE_CONTESTED')],'A-P',['C11','QUERY']),decision('DK-FUTURE','FUTURE_NONPRECLUSION',[alt('F-P','A_INCUMBENT','SELECTED')],'F-P',['FIELD','STRUCT','WORLD','ACTOR','ACT','WORLD_NEXT'],'MUST_ALLOW_FUTURE')], 'architecture':{'nodes':graphnodes,'edges':edges,'invariants':description('All original sources and future rights remain separate and qualified'),'version_lifecycle':description('Each source or delegated model condition invalidates derived reader and time-scoped state only'),'first_consumer_path':['SRC','C11','QUERY'], 'future_reference_path':['SRC','C11','QUERY','FIELD','STRUCT','WORLD','ACTOR','ACT','WORLD_NEXT']},'epistemic_case':epi,'workload':workload,'handoffs':handoffs,'builder_cold_start':{'selected_handoff_id':'HD-T1','independent_reader':description('Review pending independent C, not self-completed'),'cold_start_result':'PENDING_INDEPENDENT_C','instruction_without_new_archaeology':description('Synthetic data only; source oracle and real caller owner unavailable'),'test_positive':description('Qualified response changes query'),'test_denied':description('Denied source must not produce empirical fact'),'test_restore':description('Exact original source yields identical record'),'missing_information':description('Real ABI, lawfully authenticated wave and first consumer still held'),'evidence_ids':evid},'authority':{'author_scope':'S0_S1_DOCUMENTARY','independent_review':'PENDING_C','engineering_accepted':False,'scientific_granted':False,'source_rights_granted':False,'actor_granted':False,'protected_received':False},'blockers':[{'decision_id':'DK-PHYSICAL','unproved_fact':description('No matched A/B dense and disjoint cold persisted run'),'if_positive':description('A may be more economical with complete proof'),'if_negative':description('B may be faster and should be tested with lawful POC'),'smallest_proof':description('One exact matched synthetic sourcefree A/B measurement'),'owner':description('Competent reader owner and distinct nonauthor reviewer'),'what_can_proceed':description('Already authorized unchanged C11/reader engineering'),'decision_impact':description('Choose physical arrangement only after comparable measured work')}], 'selection_policy':{'priority_order':['SOURCE_SCIENCE_RIGHTS_HARD_VETO','NEXT_ACTUAL_FIRST_CONSUMER','MATCHED_FULL_FROZEN_WORKLOAD','MINIMAL_LAWFUL_ACCEPTED_CHANGE_ABSENT_RIVAL_ADVANTAGE','FUTURE_NONPRECLUSION'],'independent_B_frame_challenge':description('Question whether physically indexed access is optimal if dense source proof dominates total cost'),'material_evidence_or_hold':description('Material cells not measured; need smallest comparable proof of physical rivals')},'operational_boundary':{'selected_tranche':'C11_QUERY_DESIGN','effect_grade':'SOURCE_STATIC_INTERFACE_ONLY','first_consumer':description('Real I03 cold first consumer, sourcefree evidence pending')},'workload_cases':[{'id':x,'evidence_grade':'UNRUN_EXACT_HOLD','reversal_logic':description('Only a paired matched experiment for this case can distinguish alternatives'),'smallest_probe':description('Actual selected first reader with positive, negative and restore'), 'evidence_ids':evid} for x in sorted(CASES)],'observability_provenance':{'contract_schema':PROV['schema'],'cases':cases},'future_interface_routes':[{'id':name,'status':'GRAPH_PATH','node_ids':{'OBSERVED_TO_DESCRIPTIVE_FIELD':['SRC','C11','QUERY','FIELD'],'EXTERNAL_TO_STRUCTURAL_WORLD':['EXT','STRUCT','WORLD'],'WORLD_TO_ACTOR':['WORLD','ACTOR'],'ACTOR_TO_PERFORMED_HISTORY':['ACTOR','ACT'],'EXOGENOUS_WORLD_HISTORY':['WORLD','ACT']}[name]} for name in sorted({'OBSERVED_TO_DESCRIPTIVE_FIELD','EXTERNAL_TO_STRUCTURAL_WORLD','WORLD_TO_ACTOR','ACTOR_TO_PERFORMED_HISTORY','EXOGENOUS_WORLD_HISTORY'})], 'unlisted_future_transition_holds':[],'product_deltas':[],'investigation_result':'NO_NEW_PRODUCT_ADVANCE'}
    return s

def main():
    import json,tempfile,copy
    s=fixture();failures=validate(s)
    assert not failures, json.dumps(failures,indent=2)
    rejected={}
    def bad(label,act,need):
        x=copy.deepcopy(s);act(x);err=validate(x)
        if not any(need in item for item in err):raise AssertionError(label+' DID NOT REJECT: '+repr(err[:15]))
        rejected[label]=next(x for x in err if need in x)
    bad('unaccounted_observability_state',lambda x:x['observability_provenance']['cases'][0]['facets'].update(asked='BLAH'),'BAD_FACET')
    bad('unobserved_ancestry_promoted',lambda x:x['observability_provenance']['cases'][0].update(legal_claim_kind='ORIGINAL_OBSERVATION'),'NOT_ASKED_TO_OBSERVED_PROMOTION')
    bad('ineligible_to_observed',lambda x:(x['observability_provenance']['cases'][1]['facets'].update(eligibility='INELIGIBLE'),x['observability_provenance']['cases'][1].update(legal_claim_kind='ORIGINAL_OBSERVATION')),'INELIGIBLE_TO_OBSERVED_PROMOTION')
    bad('household_self_promotion',lambda x:x['observability_provenance']['cases'][1].update(target_unit='PERSON',legal_claim_kind='ORIGINAL_OBSERVATION'),'HOUSEHOLD_TO_PERSON_PROMOTION')
    bad('interviewer_self_claim',lambda x:x['observability_provenance']['cases'][2].update(target_attribution='SELF'),'INTERVIEWER_TO_SELF_PROMOTION')
    bad('false_wave_harmonization',lambda x:x['observability_provenance']['cases'][3].update(claims_cross_wave_comparable=True),'UNISSUED_TRANSLATION_PROMOTION')
    bad('two_conflicting_authority_vocabs',lambda x:x['architecture']['edges'][0].update(authority='I AM MY OWN CERTIFIER'),'CONFLICTING_SECOND_AUTHORITY_VOCABULARY')
    bad('forged_source_backflow',lambda x:(x['architecture']['nodes'][0]['input_types'].append('next_world'),x['architecture']['edges'].append({**x['architecture']['edges'][0],'id':'FAKE','from':'WORLD_NEXT','to':'SRC','data_type':'next_world'})),'UNAUTHORIZED_OR_UNMODELED_TRANSITION')
    bad('missing_external_world_path',lambda x:x['future_interface_routes'].pop(1),'INCOMPLETE_FUTURE_SOURCE_WORLD_ACTOR_ROUTES')
    bad('future_path_disconnected',lambda x:x['future_interface_routes'][0].update(node_ids=['WORLD','SRC']),'DISCONNECTED_FUTURE_ROUTE')
    bad('cyclic_build_dependencies',lambda x:(x['handoffs'][0].update(dependencies=['HD-T2']),x['handoffs'][1].update(dependencies=['HD-T1'])),'CYCLIC_BUILDER_DEPENDENCIES')
    bad('rival_same_technical_design',lambda x:[x['decisions'][1]['alternatives'][1].update(**{k:x['decisions'][1]['alternatives'][0][k] for k in ('physical_arrangement','source_preservation','preparation_reuse','first_consumer','future_interfaces')})],'IDENTICAL_PHYSICAL_RIVAL')
    bad('author_pretends_external_builder',lambda x:x['builder_cold_start'].update(cold_start_result='EXECUTED_FIRST_READER_PROOF'),'AUTHOR_PRETENDS_C_REVIEW_COMPLETE')
    bad('unfrozen_source_contract',lambda x:x['r5_policy_hashes'].update({'15_OBSERVABILITY_PROVENANCE_CONTRACT.json':'0'*64}),'R5_POLICY_HASH_MISMATCH')
    bad('missing_product_progress_without_honest_no_advance',lambda x:x.pop('investigation_result'),'CONDITIONAL_PAPERWORK_DISGUISED_AS_PRODUCT_ADVANCE')
    bad('incorrect_FF_readiness',lambda x:(x['operational_boundary'].update(selected_tranche='FF_FIRST_EFFECT_DESIGN',effect_grade='SOURCE_STATIC_INTERFACE_ONLY'),x.update(outcome='DESIGN_READY_SCOPED')),'PREMATURE_FF_FIRST_EFFECT_CLAIM')
    bad('any_ready_without_comparison',lambda x:x.update(outcome='DESIGN_READY_SCOPED'),'READY_WITHOUT_MATCHED_FULL_COMPARISON')
    bad('malformed_spine_controlled',lambda x:x.update(workload=None),'MALFORMED_SPINE_REJECTED')
    with tempfile.TemporaryDirectory() as d:
        p=pathlib.Path(d);(p/'SPINE.json').write_text(json.dumps(s))
        for n,data in outputs(s).items():(p/n).write_bytes(data)
        assert not check_dir(p)
        assert len((p/'COVERAGE_TO_DECISION.tsv').read_text().splitlines())==119
        (p/'COVERAGE_TO_DECISION.tsv').write_text('corrupt')
        assert any('PROJECTION_MISSING_OR_CHANGED' in x for x in check_dir(p))
    print(json.dumps({'status':'PASS_SYNTHETIC_R5_ONLY','source_science_review':'NOT_PERFORMED','rejected':rejected,'count':len(rejected)},indent=2))
    return 0
if __name__=='__main__':sys.exit(main())
