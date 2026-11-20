"""SORACLE R12 — material things are historically real and personally plural.

One object can materially persist while distinct actors acquire incompatible
investments in it. A real person-specific encounter supports a semantic
hypothesis, but no objective maker/owner record proves pride, affection, shame
or a conscious reason. Invested meaning belongs to the existing actor
development owner. Once admitted, it changes later qualified *attempts*,
never the object owner's rights, production history or physical condition.
"""
from .types import stable_id, copy, GRADE
from .organism import eligible

ORIENTATIONS=frozenset({'SUSTAIN','WITHHOLD','UNRESOLVED'})


def retain_personal_object_encounter(actor,experience,event_ref):
    if actor.get('id')!=experience.get('actor') or not event_ref:
        raise ValueError('OBJECT_ENCOUNTER_FOREIGN_ACTOR')
    signs=[x for x in experience.get('perceived_cues',[])
           if isinstance(x,dict) and type(x.get('material_object_ref')) is str]
    receipts=[]
    for cue in signs:
        obj=cue['material_object_ref']
        rid=stable_id('object_experience',{
            'actor':actor['id'],'event':event_ref,
            'cue':cue.get('id'),'object':obj})
        if any(x.get('id')==rid for x in actor.get('object_encounters',[])):
            continue
        attempted=(experience.get('felt_enactment') or {}).get(
            'attempted_operation')
        row={
            'id':rid,'actor':actor['id'],
            'material_object_ref':obj,'event_ref':event_ref,
            'experience_ref':experience.get('ref'),
            'perceived_cue_ref':cue.get('id'),
            'personally_attempted_operation':attempted,
            'received_public_description':cue.get('description'),
            'source_kind':cue.get('kind'),
            'objective_owner':'NOT_INFERRED_FROM_RECEPTION',
            'other_people_meaning':'UNKNOWN_NOT_OBSERVED',
            'actor_love_shame_valuation':'NOT_ESTABLISHED',
            'grade':GRADE,
        }
        actor.setdefault('object_encounters',[]).append(row)
        receipts.append({'kind':'RETAIN_OBJECT_ENCOUNTER','ref':rid,
                         'material_object_ref':obj,'grade':GRADE})
    return receipts


def possible_object_investments(actor,experience):
    """An LLM may abduce, select none, or preserve opposed interpretations."""
    if actor.get('id')!=experience.get('actor'):
        raise ValueError('OBJECT_PROPOSAL_FOREIGN_ACTOR')
    received={c.get('material_object_ref') for c in
              experience.get('perceived_cues',[])
              if isinstance(c,dict) and
              type(c.get('material_object_ref')) is str}
    proposals=[]
    for obj in sorted(received):
        episodes=[x for x in actor.get('object_encounters',[])
                  if x.get('material_object_ref')==obj]
        if not episodes:continue
        proposals.append({
            'material_object_ref':obj,
            'first_person_source_refs':[x['id'] for x in episodes[-12:]],
            'actual_first_person_operations':[
                x.get('personally_attempted_operation') for x in episodes[-12:]],
            'candidate_meanings':['SUSTAIN','WITHHOLD','UNRESOLVED',
                                  'NO_DURABLE_ACQUISITION'],
            'recipient_not_required_to_love_own_work':True,
            'producer_not_assumed_owner':True,
            'inferences_about_past_causes':'UNRESOLVED',
            'scientific_rule':'NOT_ESTABLISHED',
            'grade':GRADE,
        })
    return proposals[:6]


def admit_material_investment(actor,experience,event_ref,candidate):
    if experience.get('actor')!=actor.get('id') or not event_ref:
        raise ValueError('OBJECT_INVESTMENT_FOREIGN_ACTOR')
    obj=candidate.get('material_object_ref')
    orientation=candidate.get('orientation')
    if type(obj) is not str or orientation not in ORIENTATIONS:
        raise ValueError('OBJECT_INVESTMENT_UNQUALIFIED')
    valid_cues=[x for x in experience.get('perceived_cues',[])
                if isinstance(x,dict) and
                x.get('material_object_ref')==obj and x.get('id')]
    if not valid_cues:
        raise ValueError('OBJECT_INVESTMENT_NOT_ACTOR_EXPERIENCED')
    prior=[x for x in actor.get('object_encounters',[])
           if x.get('material_object_ref')==obj and
           x.get('event_ref')==event_ref]
    if not prior:
        raise ValueError('OBJECT_INVESTMENT_NO_ACTUAL_PERSONAL_SOURCE')
    # Admit incompatible affects separately; no forced coherent 'true attitude'.
    record={
        'id':stable_id('material_investment',{'actor':actor['id'],
              'event':event_ref,'object':obj,'orientation':orientation,
              'source':prior[-1]['id']}),
        'actor':actor['id'],'material_object_ref':obj,
        'orientation':orientation,'origin_event':event_ref,
        'experience_ref':experience.get('ref'),
        'source_personal_encounter_refs':[x['id'] for x in prior],
        'self_understanding':'NOT_IMPUTED_BY_ANALYST',
        'actual_object_ownership':'WORLD_FACT_NOT_MODIFIED',
        'other_actor_investment':'UNKNOWN_AND_INDEPENDENT',
        'material_protection_right':'NOT_CONFERRED_BY_VALUE',
        'status':'ACTIVE','sourcefree_semantic_hypothesis':True,
        'grade':GRADE,
    }
    if any(x.get('id')==record['id'] for x in actor.get('material_investments',[])):
        raise ValueError('OBJECT_DUPLICATE_INVESTMENT')
    actor.setdefault('material_investments',[]).append(record)
    return {'kind':'INVEST_MATERIAL_OBJECT',
            'investment_ref':record['id'],
            'material_object_ref':obj,
            'not_a_public_description':True,'grade':GRADE}


def recruit_material_investments(constitution,access):
    if constitution.actor!=access.actor:
        raise ValueError('OBJECT_INVESTMENT_COMPOSITION_FOREIGN_ACTOR')
    present={c.get('material_object_ref') for c in access.cues
             if isinstance(c,dict) and
             c.get('kind')=='material_object_present'}
    admitted=[x for x in getattr(constitution,'material_investments',[])
              if x.get('material_object_ref') in present
              and x.get('status')=='ACTIVE']
    groups={}
    for x in admitted:
        groups.setdefault(x['material_object_ref'],[]).append(x)
    currents=[]
    for obj,rows in sorted(groups.items()):
        directions={x['orientation'] for x in rows}
        currents.append({
            'kind':'MATERIAL_OBJECT_HISTORICAL_INVESTMENT_RECRUITED',
            'material_object_ref':obj,
            'admitted_investment_refs':[r['id'] for r in rows],
            'concurrent_orientations':sorted(directions),
            'unresolved_competition':(
                'SUSTAIN' in directions and 'WITHHOLD' in directions),
            'world_object_owner_and_condition_not_modified':True,
            'conscious_attitude_not_necessarily_available':True,
            'grade':GRADE})
    return {'currents':currents,
            'readset':[r['id'] for r in admitted],
            'grouped':groups,'grade':GRADE}


def invested_material_action_options(constitution,access):
    recruited=recruit_material_investments(constitution,access)
    out=[]
    if not eligible(constitution.body,'REPAIR')[0]:
        return {'proposals':[],'recruitment':recruited}
    for obj,rows in sorted(recruited['grouped'].items()):
        directions={r['orientation'] for r in rows}
        if 'SUSTAIN' not in directions:continue
        out.append({
            'action':'REPAIR','score':.19,
            'object_ref':obj,
            'basis':['historical_object_investment:'+r['id'] for r in rows],
            'competing_actor_orientations':sorted(directions),
            'unresolved_conflict':('WITHHOLD' in directions),
            'object_affect_not_world_right':True,
            'grade':GRADE})
    return {'proposals':out,'recruitment':recruited}


def annotate_material_alternatives(option,invested):
    """Retain opposing investments at the PARTICULAR object alternative."""
    for alt in option.get('practical_alternatives',[]):
        ref=alt.get('world_request',{}).get('material_object_ref')
        rows=invested['recruitment']['grouped'].get(ref,[])
        if not rows:continue
        alt['acquired_object_orientations']=sorted(
            set(x['orientation'] for x in rows))
        alt['source_investment_refs']=[x['id'] for x in rows]
        alt['opposed_object_orientation_unresolved']=(
            'SUSTAIN' in alt['acquired_object_orientations'] and
            'WITHHOLD' in alt['acquired_object_orientations'])
        alt['not_a_world_permission_or_actor_self_report']=True
    return option


def choose_qualified_material_care(options):
    """One unopposed recruited object, not a universal care/ownership reflex."""
    if any(o.get('project_courses') for o in options):
        return None
    candidates=[a for o in options if o.get('action')=='REPAIR'
                for a in o.get('practical_alternatives',[])
                if a.get('acquired_object_orientations')==['SUSTAIN']
                and not a.get('opposed_object_orientation_unresolved')]
    if len({x['option_id'] for x in candidates})!=1:
        return None
    a=candidates[0]
    return {'action':'REPAIR','practical_option_id':a['option_id'],
            'project_id':None,
            'semantic_grade':'SOURCEFREE_ACQUIRED_OBJECT_MEANING_TRIAL',
            'no_conscious_reason_or_material_ownership_inferred':True}
