"""SORACLE R11: structural intersection is an objective conjunction, not score.

Only source-qualified material rules can block a world action. Contradictory or
missing positioned evidence stays unresolved. A blocked actor sees a public
refusal, not the world's privileged administrative explanation.
"""
from .types import GRADE, copy
from .organism import ACTIONS


def admit_authored_structural_history(world, actor_ids, spec):
    """Initialize existing conjunctive material reader from authored inputs.

    No survey answers, psychology proposal, or self-declared scientific
    receipt can issue objective facts. Caller supplies explicit fictional
    world premises. All checks precede mutation of the world.
    """
    if (type(spec) is not dict or set(spec)!={'grade','source_ref','positions','rules'}
            or spec['grade']!='EXPLICIT_SOURCEFREE_STRUCTURAL_HISTORY'
            or type(spec['source_ref']) is not str or not spec['source_ref'].strip()
            or type(spec['positions']) is not list or type(spec['rules']) is not list
            or len(spec['positions'])>256 or len(spec['rules'])>128):
        raise ValueError('STRUCTURAL_HISTORY_UNQUALIFIED')
    def nonempty(x):return type(x) is str and bool(x.strip())
    def interval(row):
        a,b=row.get('effective_from'),row.get('effective_until')
        return type(a) is int and a>=0 and (b is None or type(b) is int and b>=a)
    positions=copy(spec['positions']);rules=copy(spec['rules'])
    ids=set()
    for row in positions:
        if (type(row) is not dict or set(row)!={'id','actor','field','value','source_ref',
                                               'effective_from','effective_until'}
                or not all(nonempty(row[k]) for k in ('id','actor','field','value','source_ref'))
                or row['actor'] not in actor_ids or not interval(row)
                or row['id'] in ids):
            raise ValueError('STRUCTURAL_HISTORY_INVALID_POSITION')
        ids.add(row['id'])
    for row in rules:
        if (type(row) is not dict or set(row)!={'id','operation','location','source_ref',
                                               'all_of','effective_from','effective_until'}
                or not all(nonempty(row[k]) for k in ('id','operation','location','source_ref'))
                or row['operation'] not in ACTIONS or
                row['location'] not in (*world['sites'],'*') or not interval(row)
                or row['id'] in ids or type(row['all_of']) is not list
                or not 1<=len(row['all_of'])<=12):
            raise ValueError('STRUCTURAL_HISTORY_INVALID_RULE')
        ids.add(row['id'])
        for clause in row['all_of']:
            if type(clause) is not dict:raise ValueError('STRUCTURAL_HISTORY_INVALID_CLAUSE')
            kind=clause.get('kind')
            if kind=='RECORDED_POSITION':
                valid=set(clause)=={'kind','field','equals'} and all(
                    nonempty(clause[k]) for k in ('field','equals'))
            elif kind=='CURRENT_SITE':
                valid=set(clause)=={'kind','equals'} and clause['equals'] in world['sites']
            elif kind in ('HAS_SITE_PERMISSION','SHIFT_OCCUPIED'):
                valid=set(clause)=={'kind'}
            else:valid=False
            if not valid:raise ValueError('STRUCTURAL_HISTORY_INVALID_CLAUSE')
    world['positioned_material_records'].extend(positions)
    world['institutional_access_rules'].extend(rules)
    world['structural_history_origin']={'source_ref':spec['source_ref'],
            'grade':spec['grade'],'native_structural_authority':False,
            'position_refs':[p['id'] for p in positions],
            'rule_refs':[p['id'] for p in rules]}


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
           and r.get('location') in (location,'*')
           and r.get('effective_from',0)<=world['clock']
           and (r.get('effective_until') is None or r['effective_until']>=world['clock'])]
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


def temporal_material_gate_boundaries(world,actor,location,operation,start,end):
    """Read actual source-qualified changes in the existing gate, not psyche.

    Time interval (start,end]; authored effective_until is inclusive.
    Only the existing relevant rule predicates and clocks are considered;
    compare exactly the same gate that settles a high-resolution attempt.
    This does not claim the actor sees the gate or its source.
    """
    if type(start) is not int or type(end) is not int or not 0<=start<=end:
        raise ValueError('STRUCTURAL_GATE_INVALID_INTERVAL')
    rules=[r for r in world.get('institutional_access_rules',[])
           if type(r) is dict and r.get('status','ACTIVE')=='ACTIVE'
           and r.get('operation')==operation and r.get('location') in (location,'*')]
    if not rules:return []
    times=set()
    def add(t):
        if type(t) is int and start<t<=end:times.add(t)
    def interval(r):
        add(r.get('effective_from',0))
        until=r.get('effective_until')
        if type(until) is int:add(until+1)
    fields=set();shift=False
    for r in rules:
        interval(r)
        for p in r.get('all_of',[]):
            if p.get('kind')=='RECORDED_POSITION':fields.add(p.get('field'))
            if p.get('kind')=='SHIFT_OCCUPIED':shift=True
    for row in world.get('positioned_material_records',[]):
        if type(row) is dict and row.get('actor')==actor and row.get('field') in fields:
            interval(row)
    if shift:
        schedule=world.get('ambient',{}).get('work_shifts',{})
        if type(schedule) is dict:
            shifts=schedule.get(actor,[])
            if type(shifts) is list:
                for s in shifts:
                    if type(s) is dict and s.get('source_ref'):
                        add(s.get('start'));add(s.get('end'))
    out=[]
    for t in sorted(times):
        before=evaluate_material_conjunction({**world,'clock':t-1},actor,location,operation)
        after=evaluate_material_conjunction({**world,'clock':t},actor,location,operation)
        if before!=after:
            out.append({'at':t,'kind':'STRUCTURAL_GATE_TRANSITION',
                        'actor':actor,'location':location,'operation':operation,
                        'source_refs':sorted(set(before['readset']+after['readset'])),
                        'before_decision':before['decision'],'after_decision':after['decision'],
                        'objective_clock_not_actor_experience':True,'grade':GRADE})
    return out


def next_material_gate_discontinuity(world,actors,horizon):
    """Find the earliest currently situated gate transition, without an act."""
    start=world['clock'];end=start+horizon
    best=None
    for actor in sorted(actors):
        location=world.get('positions',{}).get(actor)
        if location not in world.get('sites',{}):continue
        ops=sorted({r['operation'] for r in world.get('institutional_access_rules',[])
                    if type(r) is dict and r.get('status','ACTIVE')=='ACTIVE'
                    and r.get('location') in (location,'*') and r.get('operation') in ACTIONS})
        for op in ops:
            rows=temporal_material_gate_boundaries(world,actor,location,op,start,end)
            if rows and (best is None or rows[0]['at']<best['at']):
                best=rows[0]
                end=best['at']
    return best


def qualify_aggregate_material_gate(world,actor,location,operation,start,days):
    """Do not let compressed exposure bypass the high-resolution rule.

    A transition inside the interval requires a split; a boundary exactly
    at the end is lawful. A wholly denied/unknown modeled interval may
    proceed in time but cannot materialize that proposed participation.
    """
    if operation not in ACTIONS:return None
    if temporal_material_gate_boundaries(world,actor,location,operation,
                                         start,start+days-1):
        raise ValueError('HISTORICAL_TIME_SPLIT_AT_STRUCTURAL_GATE')
    return evaluate_material_conjunction({**world,'clock':start},actor,location,operation)
