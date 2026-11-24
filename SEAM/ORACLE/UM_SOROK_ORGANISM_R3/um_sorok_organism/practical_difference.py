"""Astra R7 sourcefree practical alternatives and actor-graded expectations.

An operation is not its purpose. A practical end is an anticipated material,
relational or experiential DIFFERENCE for someone, not an objective world fact.
Nothing here edits the independent world, grants permission, or identifies a
real person's unconscious motive. This module is an owner-adjacent read model.
"""
from .types import GRADE, copy, stable_id

DIRECTIONS={'MORE','LESS','PRESERVE','CHANGE','UNKNOWN'}
APPRAISALS={'ACTOR_INTERPRETS_SUPPORTED','ACTOR_INTERPRETS_DISAPPOINTED',
            'MATERIAL_OBSTACLE_SUSPECTED','MEANING_UNRESOLVED','STILL_PENDING'}

def validate_expected_difference(value):
    if value is None:
        return None
    if type(value) is not dict:
        raise ValueError('INVALID_EXPECTED_DIFFERENCE')
    allowed={'feature','direction','affected_party_ref','beneficiary_ref',
             'sign_tags','known_costs','unresolved_costs'}
    if set(value)-allowed or len(value)>7:
        raise ValueError('INVALID_EXPECTED_DIFFERENCE')
    feature=value.get('feature')
    if type(feature) is not str or not feature.strip() or len(feature)>200:
        raise ValueError('INVALID_EXPECTED_DIFFERENCE_FEATURE')
    direction=value.get('direction','UNKNOWN')
    if direction not in DIRECTIONS:
        raise ValueError('INVALID_EXPECTED_DIFFERENCE_DIRECTION')
    for key in ('affected_party_ref','beneficiary_ref'):
        if key in value and value[key] is not None and (
                type(value[key]) is not str or not value[key] or len(value[key])>160):
            raise ValueError('INVALID_EXPECTED_DIFFERENCE_BEARER')
    for key in ('sign_tags','known_costs','unresolved_costs'):
        terms=value.get(key,[])
        if type(terms) is not list or len(terms)>16 or any(
                type(t) is not str or not t or len(t)>160 for t in terms):
            raise ValueError('INVALID_EXPECTED_DIFFERENCE_TERMS')
    return copy(value)

def practical_alternatives(constitution,access,option):
    """A named option remains distinct beneath one executable operation.

    Do not invent a beneficiary/recipient when the actor has no reference.
    Legacy action-only dispatch remains a lawful, *unattributed* alternative.
    """
    act=option['action']
    actor=constitution.actor
    clock=constitution.clock
    present={cue.get('source_actor') for cue in access.cues
             if cue.get('kind')=='coactor_present'}
    alts=[]
    for course in option.get('project_courses',[]):
        project=next((p for p in constitution.projects
                      if p['id']==course['project_id']),None)
        if project is None:continue
        expected=validate_expected_difference(project.get('expected_difference'))
        object_ref=project.get('material_object_ref') if project.get('incidental_takeup_basis') is not None else None
        if project.get('incidental_takeup_basis') is not None and (
                act not in ('INSPECT','REPAIR') or type(object_ref) is not str
                or not any(c.get('kind')=='material_object_present'
                           and c.get('material_object_ref')==object_ref for c in access.cues)):
            continue
        target=project.get('addressed_party_ref')
        if target is not None and (type(target) is not str or not target):
            raise ValueError('INVALID_PROJECT_ADDRESSED_PARTY')
        reachable=target is None or target in present
        bound_target=target if reachable else None
        identity={'actor':actor,'clock':clock,'action':act,
                  'project_ref':project['id'],'expected_difference':expected,
                  'addressed_party_ref':target}
        if object_ref is not None:identity['material_object_ref']=object_ref
        alts.append({
            'option_id':stable_id('practical_option',identity),
            'actor':actor,'as_of_clock':clock,'operation':act,
            'project_id':project['id'],'grounds_status':'AVAILABLE_SINGLE_PROJECT_COURSE',
            'anticipated_difference':expected,
            'beneficiary_as_apprehended':(
                 expected.get('beneficiary_ref') if expected else None),
            'world_request':{'operation':act,'addressed_party_ref':bound_target,
                             'material_object_ref':object_ref},
            'binding_status':('QUALIFIED_AS_PRESENT' if target and reachable else
                    'NO_ADDRESSED_PARTY' if target is None else 'UNBOUND_PARTY_NOT_PRESENT'),
            'recruitment_pressures':{
                'historic_form_or_project_basis':copy(option.get('basis',[])),
                'psychodynamic_status':option.get('psychodynamic_status','UNQUALIFIED'),
                'opposed_currents':copy(option.get('opposed_currents',{})),
                'support_currents':copy(option.get('support_currents',[])),
                'not_a_transparent_self_account':True},
            'source_grade':GRADE,'not_actor_self_account':True,
            'not_world_outcome':True,'priority':project.get('priority',.5)})
    if act=='PLEDGE_CARE':
        # An actual addressee matters: a free-floating promise cannot bind
        # some convenient future person assigned by the world narration.
        for counterpart in sorted(present):
            alts.append({
                'option_id':stable_id('addressed_care_pledge',{
                    'actor':actor,'clock':clock,'target':counterpart}),
                'actor':actor,'as_of_clock':clock,
                'operation':act,'project_id':None,
                'grounds_status':'POSSIBLE_SITUATED_FUTURE_CARE_PROMISE',
                'anticipated_difference':None,
                'beneficiary_as_apprehended':counterpart,
                'world_request':{'operation':act,
                    'addressed_party_ref':counterpart,
                    'material_object_ref':None},
                'binding_status':'OTHER_PRESENT_NOT_CONSENT_TO_LATER_CARE',
                'promise_does_not_establish_future_fulfillment':True,
                'source_grade':GRADE,'not_a_conscious_motive_deduction':True})
    alts.append({'option_id':stable_id('practical_option',{'actor':actor,'clock':clock,
                  'action':act,'project_ref':None}),
        'actor':actor,'as_of_clock':clock,'operation':act,'project_id':None,
        'grounds_status':'EXPLORATORY_OR_UNRESOLVED_PROJECT_END',
        'anticipated_difference':None,'beneficiary_as_apprehended':None,
        'world_request':{'operation':act,'addressed_party_ref':None,
                         'material_object_ref':None},
        'binding_status':'UNATTRIBUTED_OPERATION',
        'not_actor_self_account':True,'not_world_outcome':True,
        'source_grade':GRADE,'priority':None})
    return alts

def start_expectation(actor,practical_selection,experience,event_ref):
    """Record an anticipation at its actual time, NOT its objective success."""
    if not practical_selection or practical_selection.get('project_id') is None:
        return None
    expected=practical_selection.get('anticipated_difference')
    if expected is None:return None
    expected=validate_expected_difference(expected)
    ref=stable_id('expectation',{'actor':actor['id'],'event':event_ref,
                                 'option':practical_selection.get('option_id')})
    if any(x['id']==ref for x in actor.get('expectations',[])):
        raise ValueError('DUPLICATE_ACTOR_EXPECTATION')
    rec={'id':ref,'actor':actor['id'],'origin_event':event_ref,
         'origin_experience_ref':experience['ref'],
         'practical_option_id':practical_selection.get('option_id'),
         'project_id':practical_selection['project_id'],
         'anticipated_difference':expected,
         'state':'STILL_PENDING','appraisal_history':[],
         'known_to_actor':'NOT_ESTABLISHED_BY_MODEL_ATTEMPT',
         'objective_success':'NOT_INFERRED','other_paths':'UNKNOWN_NOT_OBSERVED',
         'source_grade':GRADE}
    actor.setdefault('expectations',[]).append(rec)
    return rec

def appraise_expected_difference(actor,experience,event_ref,proposal):
    """A fictional *actor-relative* revision requires ACTUALLY RECEIVED sign.

    A pending expectation may outlive its initiating world transaction. No
    missing sign is treated as refusal or disappointment; no sign proves cause.
    """
    ident=proposal.get('expectation_ref')
    prior=next((x for x in actor.get('expectations',[]) if x['id']==ident),None)
    if prior is None:raise ValueError('UNKNOWN_ACTOR_EXPECTATION')
    appraisal=proposal.get('appraisal')
    if appraisal not in APPRAISALS:raise ValueError('INVALID_ACTOR_EXPECTATION_APPRAISAL')
    sign=proposal.get('perceived_cue_ref')
    received={c.get('id') for c in experience.get('perceived_cues',[])
              if isinstance(c,dict) and type(c.get('id')) is str}
    if sign is not None and (type(sign) is not str or sign not in received):
        raise ValueError('EXPECTATION_APPRAISAL_SIGN_NOT_ACTOR_RECEIVED')
    if appraisal!='STILL_PENDING' and sign is None:
        raise ValueError('EXPECTATION_APPRAISAL_NEEDS_ACTUAL_SIGN')
    if appraisal=='STILL_PENDING' and sign is None and not experience.get('participated'):
        raise ValueError('EXPECTATION_PENDING_WITHOUT_EXPOSURE')
    receipt={'event':event_ref,'experience_ref':experience['ref'],
             'perceived_cue_ref':sign,'appraisal':appraisal,
             'actual_received_sign_refs':sorted(received),
             'observer_causal_attribution':'NOT_ESTABLISHED',
             'objective_success':'NOT_INFERRED','grade':GRADE,
             'actor_interpretation_not_world_truth':True}
    prior['appraisal_history'].append(receipt)
    prior['state']=appraisal
    return {'kind':'APPRAISE_EXPECTED_DIFFERENCE','expectation':ident,
            'state':appraisal,'grade':GRADE}
