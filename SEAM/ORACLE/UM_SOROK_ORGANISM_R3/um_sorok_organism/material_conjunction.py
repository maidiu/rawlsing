"""SORACLE R11: structural intersection is an objective conjunction, not score.

Only source-qualified material rules can block a world action. Contradictory or
missing positioned evidence stays unresolved. A blocked actor sees a public
refusal, not the world's privileged administrative explanation.
"""
from .types import GRADE


def _predicate(world,actor,location,p):
    kind=p.get('kind')
    if kind=='RECORDED_POSITION':
        field=p.get('field')
        records=[r for r in world.get('positioned_material_records',[])
                 if type(r) is dict and r.get('actor')==actor
                 and r.get('field')==field
                 and type(r.get('source_ref')) is str and r['source_ref']
                 and r.get('effective_from',0)<=world['clock']
                 and (r.get('effective_until') is None or
                      r['effective_until']>=world['clock'])]
        if not records:return ('UNKNOWN','NO_CURRENT_SOURCE_QUALIFIED_POSITION')
        values={str(r.get('value')) for r in records}
        if len(values)!=1:return ('UNKNOWN','CONFLICTING_POSITIONED_RECORDS')
        return ('MET' if str(p.get('equals')) in values else 'NOT_MET',
                'SOURCE_POSITIONED_CONJUNCTION')
    if kind=='CURRENT_SITE':
        return ('MET' if location==p.get('equals') else 'NOT_MET',
                'OBJECTIVE_SITE')
    if kind=='HAS_SITE_PERMISSION':
        site=world.get('sites',{}).get(location,{})
        grants=site.get('admitted',[])
        if type(grants) is not list:return ('UNKNOWN','SITE_REGISTER_UNQUALIFIED')
        return ('MET' if site.get('access')=='public' or actor in grants
                else 'NOT_MET','EFFECTIVE_PERMISSION')
    if kind=='SHIFT_OCCUPIED':
        schedule=world.get('ambient',{}).get('work_shifts',{})
        shifts=schedule.get(actor,[]) if type(schedule) is dict else []
        if type(shifts) is not list:return ('UNKNOWN','SHIFT_REGISTER_INVALID')
        active=[s for s in shifts if type(s) is dict
                and type(s.get('start')) is int
                and type(s.get('end')) is int and s.get('source_ref')
                and s['start']<=world['clock']<s['end']]
        if active:return ('MET','OBJECTIVE_ACTIVE_SHIFT')
        if world.get('ambient',{}).get('work_shift_coverage_complete') is True:
            return ('NOT_MET','COMPLETE_SOURCE_SHIFT_REGISTER')
        return ('UNKNOWN','NO_COMPLETE_SHIFT_COVERAGE')
    raise ValueError('CONJUNCTION_UNSUPPORTED_PREDICATE')


def evaluate_material_conjunction(world,actor,location,operation):
    rules=[r for r in world.get('institutional_access_rules',[])
           if type(r) is dict and r.get('status','ACTIVE')=='ACTIVE'
           and r.get('operation')==operation
           and r.get('location') in (location,'*')]
    if not rules:
        return {'decision':'NO_ADDITIONAL_RULE','readset':[],
                'unknown_not_denial':True,'grade':GRADE}
    evaluations=[]
    for rule in rules:
        if type(rule.get('source_ref')) is not str or not rule['source_ref']:
            raise ValueError('UNSOURCED_INSTITUTIONAL_RULE')
        clauses=rule.get('all_of')
        if type(clauses) is not list or not clauses:
            raise ValueError('UNQUALIFIED_CONJUNCTIVE_RULE')
        values=[_predicate(world,actor,location,p) for p in clauses]
        decision=('BLOCKED' if any(v[0]=='NOT_MET' for v in values)
                  else 'UNRESOLVED' if any(v[0]=='UNKNOWN' for v in values)
                  else 'PERMITTED_BY_RULE')
        evaluations.append({'rule_ref':rule.get('id',rule['source_ref']),
            'source_ref':rule['source_ref'],'decision':decision,
            'clause_outcomes':[{'status':v[0],'basis':v[1]} for v in values]})
    overall=('BLOCKED' if any(v['decision']=='BLOCKED' for v in evaluations)
             else 'UNRESOLVED' if any(v['decision']=='UNRESOLVED' for v in evaluations)
             else 'PERMITTED_BY_ALL_RULES')
    return {'decision':overall,'evaluations':evaluations,
        'readset':[v['source_ref'] for v in evaluations],
        'unknown_not_denial':True,'actor_explanation_not_inferred':True,
        'no_additive_demographic_weights':True,'grade':GRADE}
