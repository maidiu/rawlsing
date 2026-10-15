"""Nonparent consumer: modeled institutional options plus exact source support.

Counts/fractions describe the synthetic source risk set, never this worker's
motivation, identity, decision or route-selection probability.
"""
def consume(service,snapshot,*,budget_tokens=5):
    if type(budget_tokens) is not int or budget_tokens<0:raise ValueError('EXACT_NATIVE_RESOURCE_BUDGET_REQUIRED')
    start=len(service.value_reads)
    access=service.structural(snapshot,'training_access','NONPARENT_OPTIONS')
    fee=service.structural(snapshot,'training_fee','NONPARENT_OPTIONS')
    exit_cost=service.structural(snapshot,'exit_cost','NONPARENT_OPTIONS')
    civil=service.structural(snapshot,'civil_open','NONPARENT_OPTIONS')
    sanction=service.structural(snapshot,'civil_sanction','NONPARENT_OPTIONS')
    available=lambda *xs:all(x['state']=='SUPPORTED_TEST_ONLY' for x in xs)
    routes={
        'training':dict(state=('ELIGIBLE' if access['value'] and fee['value']<=budget_tokens else 'BLOCKED_BY_MODELED_RULE') if available(access,fee) else 'UNAVAILABLE_AUTHORITY_OR_CLOCK',dependencies=['training_access','training_fee'],value_refs=[access.get('field_ref'),fee.get('field_ref')]),
        'civil':dict(state=('ELIGIBLE' if civil['value'] and not sanction['value'] else 'BLOCKED_BY_MODELED_RULE') if available(civil,sanction) else 'UNAVAILABLE_AUTHORITY_OR_CLOCK',dependencies=['civil_open','civil_sanction'],value_refs=[civil.get('field_ref'),sanction.get('field_ref')]),
        'exit_constraint':dict(state=('RESOURCE_CONSTRAINED' if exit_cost['value']>budget_tokens else 'WITHIN_MODELED_BUDGET') if available(exit_cost) else 'UNAVAILABLE_AUTHORITY_OR_CLOCK',dependencies=['exit_cost'],value_refs=[exit_cost.get('field_ref')])}
    empirical=service.possibilities(snapshot,consumer='NONPARENT_OPTIONS')
    balance=[]
    for step in empirical['steps']:
        cells={c['cell']:c['raw_numerator_support'] for c in step['cells']}
        balance.append(dict(target=step['target'],conditioners=step['conditioners'],denominator=step['denominator'],source_balance_count=(cells['1']-cells['0']) if '1' in cells and '0' in cells else None,all_alternatives=step['cells'],support_state=step['state'],source_balance_null_reason=None if '1' in cells and '0' in cells else 'NO_COMPLETE_SUPPORTED_BINARY_CELLS',evidence_ref=step.get('evidence_ref')))
    return service._record(dict(consumer='NONPARENT_OPTIONS',state='OPTIONS_AND_SOURCE_SUPPORT_PRODUCED' if empirical['state']=='PRODUCTIVE_TEST_ONLY' and all(r['state']!='UNAVAILABLE_AUTHORITY_OR_CLOCK' for r in routes.values()) else 'PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT',structural_routes=routes,empirical=empirical,source_balance_reads=balance,route_probability=None,route_probability_reason='NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL',dependencies=['empirical','training_access','training_fee','exit_cost','civil_open','civil_sanction'],values_read=service.value_reads[start:],snapshot_ref=snapshot.snapshot_hash))
