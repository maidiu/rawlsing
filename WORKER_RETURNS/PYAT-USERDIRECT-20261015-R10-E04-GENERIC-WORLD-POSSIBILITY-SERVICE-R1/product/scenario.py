"""Separate downstream generic conception-scenario PROPOSAL evaluator.

No parents, relationships, conception occurrence, personality or weights are
constructed. A proposal is not a person, sampled endpoint or realized event.
"""
def evaluate(service,snapshot,scenarios):
    if not isinstance(scenarios,(list,tuple)) or not scenarios:raise ValueError('FINITE_PROPOSALS_REQUIRED')
    preflight_ids=set()
    for proposal in scenarios:
        if not isinstance(proposal,dict) or set(proposal)!={'scenario_id','route'} or not isinstance(proposal['scenario_id'],str) or not proposal['scenario_id'].strip() or proposal['scenario_id'] in preflight_ids or proposal['route'] not in ('institutional','civil'):raise ValueError('EXACT_FINITE_SCENARIO_GRAMMAR_REQUIRED')
        preflight_ids.add(proposal['scenario_id'])
    ids=set();start=len(service.value_reads);results=[]
    # Separate consumer implementation, not a renamed nonparent output.
    evidence=service.possibilities(snapshot,consumer='CONCEPTION_SCENARIO_PROPOSALS')
    for proposal in scenarios:
        if set(proposal)!={'scenario_id','route'} or not isinstance(proposal['scenario_id'],str) or not proposal['scenario_id'].strip() or proposal['scenario_id'] in ids:raise ValueError('EXACT_SCENARIO_ID_ROUTE_ONLY; no child outcomes, persons or weights')
        ids.add(proposal['scenario_id']);route=proposal['route']
        if route=='institutional':
            access=service.structural(snapshot,'training_access','CONCEPTION_SCENARIO_PROPOSALS')
            feasibility='FEASIBLE_MODELED_PREMISE' if access['state']=='SUPPORTED_TEST_ONLY' and access['value'] is True else 'INFEASIBLE_MODELED_PREMISE' if access['state']=='SUPPORTED_TEST_ONLY' else 'UNKNOWN_PREMISE'
            dependencies=['training_access'];refs=[access.get('field_ref')]
        elif route=='civil':
            opened=service.structural(snapshot,'civil_open','CONCEPTION_SCENARIO_PROPOSALS');sanction=service.structural(snapshot,'civil_sanction','CONCEPTION_SCENARIO_PROPOSALS')
            feasibility='UNKNOWN_PREMISE'
            if opened['state']==sanction['state']=='SUPPORTED_TEST_ONLY':feasibility='FEASIBLE_MODELED_PREMISE' if opened['value'] and not sanction['value'] else 'INFEASIBLE_MODELED_PREMISE'
            dependencies=['civil_open','civil_sanction'];refs=[opened.get('field_ref'),sanction.get('field_ref')]
        else:raise ValueError('UNKNOWN_ROUTE_REMAINS_UNSUPPORTED')
        profiles=[dict(denominator=s['denominator'],complete_native_cells=s['cells'],conditioners=s['conditioners'],evidence_ref=s.get('evidence_ref')) for s in evidence['steps']]
        results.append(dict(scenario_id=proposal['scenario_id'],route=route,feasibility=feasibility,structural_value_refs=refs,empirical_profiles=profiles,selection_weight=None,weight_reason='NO_SCENARIO_SELECTION_MODEL_OR_ISSUER',dependencies=dependencies))
    deps=sorted({'empirical'}|{d for r in results for d in r['dependencies']})
    return service._record(dict(consumer='CONCEPTION_SCENARIO_PROPOSALS',state='FINITE_PROPOSALS_EVALUATED' if evidence['state']=='PRODUCTIVE_TEST_ONLY' and all(r['feasibility']!='UNKNOWN_PREMISE' for r in results) else 'PARTIAL_PROPOSALS_EVALUATED',scenarios=results,empirical=evidence,person_generation=False,actual_conception=False,relationships_generated=False,values_read=service.value_reads[start:],dependencies=deps,snapshot_ref=snapshot.snapshot_hash))
