#!/usr/bin/env python3
"""ANVIL R5 structural/typed campaign contract. DOES NOT validate scientific truth or independence.
All ready checks are *author P2 proposal* checks. C/H1 separately authenticate independent review and receiving.
"""
import hashlib,json,pathlib,re
from collections import defaultdict
ROOT=pathlib.Path(__file__).resolve().parents[1]
RULES={key:json.loads((ROOT/key).read_text()) for key in ['13_WORKLOAD_AND_DISCRIMINATORS.json','14_AUTHORITY_TRANSITION_MATRIX.json','15_OBSERVABILITY_PROVENANCE_CONTRACT.json']}
ALLOWED={(x['from_domain'],x['to_domain'],x['transition_class'],x['authority_grade'],x['temporal_mode']) for x in RULES['14_AUTHORITY_TRANSITION_MATRIX.json']['allowed']}
CASES={c['id'] for c in RULES['13_WORKLOAD_AND_DISCRIMINATORS.json']['cases']}
NECESSARY_ROUTES={'OBSERVED_TO_DESCRIPTIVE_FIELD','EXTERNAL_TO_STRUCTURAL_WORLD','WORLD_TO_ACTOR','ACTOR_TO_PERFORMED_HISTORY','EXOGENOUS_WORLD_HISTORY'}
DOMAINS=set(RULES['14_AUTHORITY_TRANSITION_MATRIX.json']['subject_domains'])
PROV=RULES['15_OBSERVABILITY_PROVENANCE_CONTRACT.json']

def enough(x,n=20):return isinstance(x,str) and len(x.strip())>=n and x.strip().lower() not in ('not applicable','unknown','todo','tbd','yes','no')
def cyclic(graph):
    seen=set();active=set()
    def walk(n):
        if n in active:return True
        if n in seen:return False
        seen.add(n);active.add(n)
        res=any(walk(k) for k in graph.get(n,[]))
        active.remove(n);return res
    return any(walk(k) for k in graph)
def reach(graph,a,b):
    todo=[a];seen=set()
    while todo:
        n=todo.pop()
        if n==b:return True
        if n not in seen:
            seen.add(n);todo.extend(graph.get(n,[]))
    return False

def check_spine(s,evidence_root=None,strict_repo=None):
    errors=[];ready=s.get('outcome')=='DESIGN_READY_SCOPED';r6=s.get('schema')=='ANVIL_SPINE_R6'
    if ready and not r6:errors.append('R6_READY_REQUIRES_R6_POLICY')
    if r6:
        rp=ROOT/'20_R6_MATERIAL_DECISION_CONSTITUTION.json'
        if s.get('r6_material_policy_sha256')!=hashlib.sha256(rp.read_bytes()).hexdigest():errors.append('R6_MATERIAL_CONSTITUTION_HASH_MISMATCH')
    for name in ['12_ORIGINAL_MANDATE_AND_DECISION_LEVERAGE.md','13_WORKLOAD_AND_DISCRIMINATORS.json','14_AUTHORITY_TRANSITION_MATRIX.json','15_OBSERVABILITY_PROVENANCE_CONTRACT.json','17_R5_DECISION_AND_TERMINAL_GATES.md']:
        actual=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
        if s.get('r5_policy_hashes',{}).get(name)!=actual:errors.append('R5_POLICY_HASH_MISMATCH:'+name)
    comparison=s.get('selection_policy')
    if not isinstance(comparison,dict):errors.append('MISSING_SELECTION_POLICY');comparison={}
    priority=['SOURCE_SCIENCE_RIGHTS_HARD_VETO','NEXT_ACTUAL_FIRST_CONSUMER','MATCHED_FULL_FROZEN_WORKLOAD','MINIMAL_LAWFUL_ACCEPTED_CHANGE_ABSENT_RIVAL_ADVANTAGE','FUTURE_NONPRECLUSION']
    if comparison.get('priority_order')!=priority:errors.append('SELECTION_PRIORITY_NOT_FROZEN')
    if not enough(comparison.get('independent_B_frame_challenge'),40):errors.append('NO_B_PROBLEM_FRAME_CHALLENGE')
    if not enough(comparison.get('material_evidence_or_hold'),40):errors.append('NO_EXACT_COMPARATIVE_JUSTIFICATION')
    op=s.get('operational_boundary')
    if not isinstance(op,dict):errors.append('MISSING_SCOPED_FIRST_CONSUMER');op={}
    if op.get('selected_tranche') not in {'C11_QUERY_DESIGN','F1_F4_CONSUMER_DESIGN','FF_FIRST_EFFECT_DESIGN'}:errors.append('UNBOUNDED_DESIGN_READY_SCOPE')
    if op.get('effect_grade') not in {'SOURCE_STATIC_INTERFACE_ONLY','EXECUTED_SOURCEFREE_FIRST_EFFECT','EXECUTED_NATIVE_FIRST_EFFECT'}:errors.append('BAD_FIRST_EFFECT_GRADE')
    if op.get('selected_tranche')=='FF_FIRST_EFFECT_DESIGN' and ready and op.get('effect_grade')=='SOURCE_STATIC_INTERFACE_ONLY':errors.append('PREMATURE_FF_FIRST_EFFECT_CLAIM')
    if not enough(op.get('first_consumer'),20):errors.append('SCOPED_FIRST_CONSUMER_NOT_NAMED')
    # Workload matrix is PREDEFINED, but only discriminating cells selected at P15 are physically mandatory.
    cs=s.get('workload_cases')
    if not isinstance(cs,list):cs=[]
    cmap={x.get('id'):x for x in cs if isinstance(x,dict)}
    if set(cmap)!=CASES or len(cs)!=len(CASES):errors.append('INCOMPLETE_R5_WORKLOAD_SHAPE_CONSIDERATION')
    for case in cs:
        if not isinstance(case,dict):continue
        if case.get('evidence_grade') not in {'MEASURED_MATCHED','MODELED_WITH_UNCERTAINTY','SOURCE_STATIC_ONLY','UNRUN_EXACT_HOLD'}:errors.append('BAD_WORKLOAD_PROOF_GRADE:'+str(case.get('id')))
        if not enough(case.get('reversal_logic'),30):errors.append('NONDISCRIMINATING_WORKLOAD:'+str(case.get('id')))
        if not enough(case.get('smallest_probe'),25):errors.append('NO_MINIMUM_DECISIVE_PROBE:'+str(case.get('id')))
    # R5 grade prohibitions: no future scientific execution proof demanded to choose a sound current storage representation.
    for d in s.get('decisions',[]):
        if not isinstance(d,dict):continue
        if d.get('class')=='FUTURE_NONPRECLUSION' and ready and d.get('maturity') not in {'MUST_ALLOW_FUTURE','CONSERVE_NOW'}:errors.append('FUTURE_DESIGN_DISGUISED_AS_CURRENT_BUILD')
        alts=d.get('alternatives',[])
        if d.get('class')=='PHYSICAL' and isinstance(alts,list):
            a=[x for x in alts if isinstance(x,dict) and x.get('origin')=='A_INCUMBENT']
            b=[x for x in alts if isinstance(x,dict) and x.get('origin')=='B_INDEPENDENT']
            if a and b:
                fields=('physical_arrangement','source_preservation','preparation_reuse','first_consumer','future_interfaces')
                if all(a[0].get(k)==b[0].get(k) for k in fields):errors.append('IDENTICAL_PHYSICAL_RIVAL_IN_DIFFERENT_ORIGIN_WRAPPER')
    # Typed observability: independent axes with exact instrument and source semantics rather than flat enum.
    prov=s.get('observability_provenance',{})
    if not isinstance(prov,dict):prov={}
    required_cases=set(PROV['required_cases'])
    if prov.get('contract_schema')!=PROV['schema']:errors.append('OBSERVABILITY_PROVENANCE_SCHEMA_MISMATCH')
    rows=prov.get('cases',[])
    if not isinstance(rows,list):rows=[]
    cmap={x.get('case_id'):x for x in rows if isinstance(x,dict)}
    if set(cmap)!=required_cases or len(rows)!=len(required_cases):errors.append('MISSING_OR_DUPLICATED_ORTHOGONAL_PROVENANCE_CASE')
    for key,row in cmap.items():
        fields=row.get('facets',{})
        for axis,values in PROV['axes'].items():
            if fields.get(axis) not in values:errors.append('BAD_FACET:'+str(key)+':'+axis)
        for req in ('instrument_id','country','wave','question_id','unit_id_or_risk_set','source_ref','source_grade','legal_claim_kind','first_consumer','negative','restore','evidence_ids'):
            if req not in row or row[req] in ('',None,[]):errors.append('PROVENANCE_MISSING_'+req+':'+str(key))
        if row.get('legal_claim_kind')=='ORIGINAL_OBSERVATION':
            if fields.get('observation')!='VALUE':errors.append('NONVALUE_TO_ORIGINAL_OBSERVATION:'+str(key))
            if fields.get('source_status') in {'MODEL_OR_FICTION','SCIENTIFIC_INTERPRETATION','UNKNOWN_HELD','DOCUMENTED_DESIGN'}:errors.append('UNISSUED_SOURCE_TO_ORIGINAL_OBSERVATION:'+str(key))
            if fields.get('claim_kind')!='ORIGINAL_OBSERVATION':errors.append('FACET_CLAIM_CONTRADICTS_ORIGINAL:'+str(key))
            if fields.get('eligibility')!='ELIGIBLE' or fields.get('asked')!='YES' or fields.get('released')!='YES':errors.append('ORIGINAL_OBSERVATION_UNQUALIFIED_SOURCE:'+str(key))
        if r6 and row.get('target_unit') not in {'PERSON','HOUSEHOLD','INSTITUTION','GROUP','OTHER_DOCUMENTED'}:
            errors.append('R6_MISSING_EXPLICIT_TARGET_GRAIN:'+str(key))
        if r6 and row.get('target_unit')=='PERSON' and fields.get('unit')!='PERSON' and row.get('legal_claim_kind')=='ORIGINAL_OBSERVATION':
            errors.append('R6_NONPERSON_TO_PERSON_PROMOTION:'+str(key))
        if fields.get('eligibility')=='INELIGIBLE' and row.get('legal_claim_kind')=='ORIGINAL_OBSERVATION':errors.append('INELIGIBLE_TO_OBSERVED_PROMOTION:'+str(key))
        if fields.get('asked')=='NO' and row.get('legal_claim_kind')=='ORIGINAL_OBSERVATION':errors.append('NOT_ASKED_TO_OBSERVED_PROMOTION:'+str(key))
        if fields.get('released')=='NO' and row.get('legal_claim_kind')=='ORIGINAL_OBSERVATION':errors.append('NOT_RELEASED_TO_OBSERVED_PROMOTION:'+str(key))
        if fields.get('unit')=='HOUSEHOLD' and row.get('target_unit')=='PERSON' and row.get('legal_claim_kind')=='ORIGINAL_OBSERVATION':errors.append('HOUSEHOLD_TO_PERSON_PROMOTION:'+str(key))
        if fields.get('attribution')=='INTERVIEWER' and row.get('target_attribution')=='SELF':errors.append('INTERVIEWER_TO_SELF_PROMOTION:'+str(key))
        if fields.get('translation')=='UNRECONCILED' and row.get('claims_cross_wave_comparable'):errors.append('UNISSUED_TRANSLATION_PROMOTION:'+str(key))
        if fields.get('claim_kind') in {'MODEL_INFERENCE','FICTIONAL_FACT'} and row.get('legal_claim_kind')=='ORIGINAL_OBSERVATION':errors.append('INFERRED_OR_FICTIONAL_TO_OBSERVED:'+str(key))
        if (fields.get('asked')=='NO' or fields.get('released')=='NO' or fields.get('eligibility')=='INELIGIBLE') and row.get('conclusion_kind') in {'ZERO_PREVALENCE','NO_EFFECT'}:errors.append('ABSENCE_TO_ZERO:'+str(key))
    if r6:
        novel=s.get('novel_source_meaning_probe')
        if not isinstance(novel,dict):errors.append('R6_MISSING_NOVEL_SOURCE_MEANING_PROBE')
        else:
            for k in ('source_identity','new_unanticipated_ambiguity','source_design_vs_respondent_answer','first_consumer','positive','forbidden_promotion','restoration','evidence_receipt_or_exact_owner_hold'):
                if not enough(novel.get(k),25):errors.append('R6_NOVEL_SOURCE_MEANING_MISSING:'+k)
        epi=s.get('epistemic_case',{})
        if epi.get('instrument_A_ancestry') in {'NOT_ASKED','NOT_OBSERVED','UNKNOWN_HELD'}:
            steps=epi.get('steps',[])
            if not any(z.get('ancestry_A_status')=='NOT_OBSERVED' for z in steps if isinstance(z,dict)):
                errors.append('R6_OBSERVABILITY_BLINDSPOT_ERASED')
            if all(z.get('ancestry_A_status')=='NOT_APPLICABLE' for z in steps if isinstance(z,dict)):
                errors.append('R6_ALL_BOUNDARIES_WAIVED_OBSERVABILITY')
    # One canonical edge transition vocabulary. Unlisted *future* requirements held, not assumed impossible.
    arch=s.get('architecture',{})
    nodes=arch.get('nodes',[]) if isinstance(arch,dict) else []
    edges=arch.get('edges',[]) if isinstance(arch,dict) else []
    nmap={n.get('id'):n for n in nodes if isinstance(n,dict)}
    graph=defaultdict(list);sourcegraph=defaultdict(list)
    for edge in edges:
        if not isinstance(edge,dict):continue
        ident=str(edge.get('id'))
        if set(edge)&{'grade','authority','clock'}:errors.append('CONFLICTING_SECOND_AUTHORITY_VOCABULARY:'+ident)
        src=nmap.get(edge.get('from'),{});dest=nmap.get(edge.get('to'),{})
        pair=(src.get('domain'),dest.get('domain'),edge.get('transition_class'),edge.get('authority_grade'),edge.get('temporal_mode'))
        if pair not in ALLOWED:errors.append('UNAUTHORIZED_OR_UNMODELED_TRANSITION:'+ident)
        if not enough(edge.get('invalidation_rule'),20):errors.append('MISSING_DERIVATION_INVALIDATION:'+ident)
        if edge.get('temporal_mode')=='FORWARD_FICTIONAL_TIME' and not enough(edge.get('strict_time_guard'),20):errors.append('UNPROVED_FUTURE_TIME_GUARD:'+ident)
        if src and dest:
            graph[edge['from']].append(edge['to'])
            if src.get('domain') in {'OBSERVED','DESCRIPTIVE_MODELED','STRUCTURAL_QUALIFIED','EXTERNAL_OBSERVED'} and dest.get('domain') in {'OBSERVED','DESCRIPTIVE_MODELED','STRUCTURAL_QUALIFIED','EXTERNAL_OBSERVED'}:sourcegraph[edge['from']].append(edge['to'])
    if cyclic(sourcegraph):errors.append('SOURCE_AND_STRUCTURE_CAUSAL_CYCLE')
    # All cycles must have every cyclic edge timestamped for fictional-state progression, and no source state participating.
    for edge in edges:
        if not isinstance(edge,dict):continue
        a,b=edge.get('from'),edge.get('to')
        if b in graph and reach(graph,b,a) and edge.get('temporal_mode') not in {'FORWARD_FICTIONAL_TIME','FICTIONAL_EVENT_ACCESS_QUALIFIED'}:errors.append('UNTIMED_GLOBAL_CYCLE:'+str(edge.get('id')))
    handoffs=s.get('handoffs',[])
    hgraph={h.get('id'):[] for h in handoffs if isinstance(h,dict)}
    for h in handoffs:
        if isinstance(h,dict):hgraph[h.get('id')]=[x for x in h.get('dependencies',[]) if x in hgraph]
    if cyclic(hgraph):errors.append('CYCLIC_BUILDER_DEPENDENCIES')
    routes=s.get('future_interface_routes',[])
    if not isinstance(routes,list):routes=[]
    byroute={x.get('id'):x for x in routes if isinstance(x,dict)}
    if set(byroute)!=NECESSARY_ROUTES or len(routes)!=len(NECESSARY_ROUTES):errors.append('INCOMPLETE_FUTURE_SOURCE_WORLD_ACTOR_ROUTES')
    for rid,r in byroute.items():
        if r.get('status')=='GRAPH_PATH':
            nids=r.get('node_ids',[])
            if not isinstance(nids,list) or len(nids)<2 or any(n not in nmap for n in nids):errors.append('MISSING_FUTURE_ROUTE_NODES:'+rid)
            elif not all(reach(graph,a,b) for a,b in zip(nids,nids[1:])):errors.append('DISCONNECTED_FUTURE_ROUTE:'+rid)
        elif r.get('status')=='OWNER_HELD_NONPRECLUSION':
            if not enough(r.get('required_information_preserved'),45) or not enough(r.get('missing_issuer_or_implementation'),35):errors.append('FUTURE_ROUTE_HOLD_NOT_ACTIONABLE:'+rid)
        else:errors.append('UNQUALIFIED_FUTURE_ROUTE:'+rid)
    if r6:
        expectations={
          'OBSERVED_TO_DESCRIPTIVE_FIELD':('OBSERVED','DESCRIPTIVE_MODELED',set()),
          'EXTERNAL_TO_STRUCTURAL_WORLD':('EXTERNAL_OBSERVED','FICTIONAL_WORLD',{'STRUCTURAL_QUALIFIED'}),
          'WORLD_TO_ACTOR':('FICTIONAL_WORLD','ACTOR_STATE',set()),
          'ACTOR_TO_PERFORMED_HISTORY':('ACTOR_STATE','HISTORY_EVENT',set()),
          'EXOGENOUS_WORLD_HISTORY':('FICTIONAL_WORLD','HISTORY_EVENT',set())
        }
        edgepairs={(e.get('from'),e.get('to')):e for e in edges if isinstance(e,dict)}
        for rid,r in byroute.items():
            if rid not in expectations or r.get('status')!='GRAPH_PATH':continue
            ids=r.get('node_ids',[])
            if not isinstance(ids,list) or len(ids)<2 or any(i not in nmap for i in ids):continue
            start,end,intermediates=expectations[rid]
            domains=[nmap[i].get('domain') for i in ids]
            if domains[0]!=start or domains[-1]!=end or not intermediates.issubset(set(domains)):
                errors.append('R6_FUTURE_ROUTE_WRONG_TARGET_DOMAIN:'+rid)
            if any((a,b) not in edgepairs for a,b in zip(ids,ids[1:])):
                errors.append('R6_ROUTE_NOT_AN_EXPLICIT_TYPED_EDGE_PATH:'+rid)
            if rid=='EXOGENOUS_WORLD_HISTORY' and not any(edgepairs.get((a,b),{}).get('transition_class')=='EXOGENOUS_WORLD_EVENT' for a,b in zip(ids,ids[1:])):
                errors.append('R6_EXOGENOUS_EVENT_MISCAST_AS_ACTOR_ACTION')
        reference=arch.get('future_reference_path',[])
        if not isinstance(reference,list) or not reference or not {'ACTOR_STATE','HISTORY_EVENT'}.issubset({nmap.get(i,{}).get('domain') for i in reference}):
            errors.append('R6_FUTURE_REFERENCE_PATH_STOPS_BEFORE_PERSON')
        if not any(nmap.get(i,{}).get('domain')=='FICTIONAL_WORLD' for i in reference):
            errors.append('R6_FUTURE_REFERENCE_PATH_SKIPS_WORLD')
        for h in handoffs:
            if not isinstance(h,dict):continue
            if h.get('implementation_status')=='READY_FOR_IMPLEMENTER':
                for field in ('producer_symbol','consumer_symbol','test_command','input_abi','output_abi'):
                    v=h.get(field)
                    if not enough(v,16) or any(t in v.lower() for t in ('to be specified','unknown current','future engineer','placeholder','not yet implemented')):
                        errors.append('R6_FAKE_BUILDER_READY:'+str(h.get('id'))+':'+field)
    holds=s.get('unlisted_future_transition_holds',[])
    if not isinstance(holds,list):errors.append('BAD_UNLISTED_FUTURE_TRANSITION_HOLDS')
    else:
        for i,r in enumerate(holds):
            if not isinstance(r,dict) or not all(enough(r.get(k),30) for k in ('reason_required','first_consumer','owner_and_issuer','preservation_path')):errors.append('UNQUALIFIED_NEW_FUTURE_TRANSITION:'+str(i))
    # R5 physical comparison: output must be a hash-bound externally sourced comparator, never prose winner alone.
    if ready and any(d.get('class')=='PHYSICAL' for d in s.get('decisions',[]) if isinstance(d,dict)):
        comp=s.get('comparison_receipt',{})
        if not isinstance(comp,dict):comp={}
        for k in ('input_path','input_sha256','frozen_path','frozen_sha256','declared_verdict','declared_winner','physical_decision_id'):
            if not comp.get(k):errors.append('READY_WITHOUT_MATCHED_FULL_COMPARISON_'+k)
        if comp.get('declared_winner') not in {'A','B'}:errors.append('NO_EXPLICIT_VERIFIED_PHYSICAL_WINNER')
        if evidence_root is None:errors.append('READY_REQUIRES_INDEPENDENT_MATCHED_COMPARATOR_READBACK')
        else:
            import sys
            sys.path.insert(0,str(ROOT/'tools'))
            from r6_comparator import r6_full_comparison
            root=pathlib.Path(evidence_root).resolve()
            try:
                paths=[]
                for k,h in (('input_path','input_sha256'),('frozen_path','frozen_sha256')):
                    path=(root/comp[k]).resolve()
                    if not path.is_relative_to(root) or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=comp[h]:raise ValueError('MISMATCH:'+k)
                    paths.append(path)
                result=r6_full_comparison(json.loads(paths[0].read_text()),json.loads(paths[1].read_text()),evidence_root=evidence_root)
                if result.get('status')!=comp.get('declared_verdict'):errors.append('PHYSICAL_CHOICE_CONTRADICTS_MATCHED_RECEIPT')
                winner=result.get('winner')
                if not winner:
                    errors.append('R6_NO_WINNER_WHILE_DECISIVE_UNCERTAINTY_OR_EXCLUSION_REMAINS')
                if winner!=comp.get('declared_winner'):errors.append('PHYSICAL_CHOICE_CONTRADICTS_MATCHED_RECEIPT')
                if r6:
                    ph=[d for d in s.get('decisions',[]) if isinstance(d,dict) and d.get('class')=='PHYSICAL']
                    mappings=s.get('physical_decision_evidence',[])
                    if not isinstance(mappings,list):mappings=[]
                    ids=[m.get('decision_id') for m in mappings if isinstance(m,dict)]
                    if len(ids)!=len(set(ids)) or set(ids)!={d.get('id') for d in ph}:
                        errors.append('R6_PHYSICAL_DECISION_TO_EVIDENCE_CLOSURE_INCOMPLETE')
                    for m in mappings:
                        if not isinstance(m,dict):continue
                        d2=next((d for d in ph if d.get('id')==m.get('decision_id')),None)
                        if not d2:continue
                        if m.get('selected_alternative_id')!=d2.get('selected'):
                            errors.append('R6_PHYSICAL_SELECTED_ALTERNATIVE_MISMATCH:'+str(d2.get('id')))
                        if m.get('selected_candidate')!=winner:
                            errors.append('R6_PHYSICAL_DECISION_BORROWS_OTHER_WINNER:'+str(d2.get('id')))
                        if not isinstance(m.get('material_cell_ids'),list) or not m['material_cell_ids'] or not set(m['material_cell_ids']).issubset({c.get('id') for c in json.loads(paths[1].read_text()).get('cells',[])}):
                            errors.append('R6_PHYSICAL_DECISION_WITHOUT_RELEVANT_CELLS:'+str(d2.get('id')))
                        for k in ('first_consumer_effect','joint_cost_or_dependency_explanation','source_integrity_veto_receipt'):
                            if not enough(m.get(k),35):errors.append('R6_PHYSICAL_EVIDENCE_MISSING_'+k+':'+str(d2.get('id')))
                d=next((d for d in s['decisions'] if d.get('id')==comp['physical_decision_id']),None)
                if not d or not any(x.get('id')==d.get('selected') and (x.get('origin')=='A_INCUMBENT' if winner=='A' else x.get('origin')=='B_INDEPENDENT') for x in d.get('alternatives',[])):errors.append('SPINE_SELECTED_DIFFERENT_PHYSICAL_WINNER')
            except (OSError,KeyError,ValueError,TypeError) as ex:errors.append('COMPARISON_READBACK_FAILED:'+str(ex)[:120])
    # R5 positive product delta requirement for purportedly productive conditional/blocked investigation.
    if s.get('outcome') in {'CONDITIONAL_CANDIDATE','DECISION_BLOCKED_EXACT'}:
        deltas=s.get('product_deltas',[])
        if not isinstance(deltas,list) or not deltas:
            if s.get('investigation_result')!='NO_NEW_PRODUCT_ADVANCE':errors.append('CONDITIONAL_PAPERWORK_DISGUISED_AS_PRODUCT_ADVANCE')
        else:
            for i,r in enumerate(deltas):
                if not isinstance(r,dict):errors.append('INVALID_PRODUCT_DELTA:'+str(i));continue
                if r.get('kind') not in {'ELIMINATED_ALTERNATIVE','CONSEQUENTIAL_FALSIFIER','QUALIFIED_INTERFACE','PROVED_CLAIM_PROHIBITION','NARROWER_EXECUTABLE_BLOCKER'}:errors.append('INVALID_PRODUCT_DELTA_KIND:'+str(i))
                if r6:
                    evidence={e.get('id'):e for e in s.get('evidence',[]) if isinstance(e,dict)}
                    link=evidence.get(r.get('exact_evidence_id'))
                    if not link:errors.append('R6_PRODUCT_ADVANCE_UNLINKED_TO_EVIDENCE:'+str(i))
                    elif link.get('verification_status') not in {'INDEPENDENTLY_VERIFIED_AT_SCOPE','EXTERNALLY_AUTHENTICATED_AT_SCOPE'}:
                        errors.append('R6_PRODUCT_ADVANCE_NOT_INDEPENDENTLY_PROVEN:'+str(i))
                for k in ('before','after','exact_evidence_id','first_consumer','previous_blocker','new_effect','independent_verification_requirement'):
                    if not enough(r.get(k),15):errors.append('PRODUCT_DELTA_MISSING_'+k+':'+str(i))
    return sorted(set(errors))
