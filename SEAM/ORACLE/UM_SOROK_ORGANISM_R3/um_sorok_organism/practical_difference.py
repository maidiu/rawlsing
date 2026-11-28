"""Astra R7 sourcefree practical alternatives and actor-graded expectations.

An operation is not its purpose. A practical end is an anticipated material,
relational or experiential DIFFERENCE for someone, not an objective world fact.
Nothing here edits the independent world, grants permission, or identifies a
real person's unconscious motive. This module is an owner-adjacent read model.
"""
from .types import GRADE, copy, stable_id
from .distributed_power import accessible_human_counterparts, food_acceptance_alternative
from .historical_self_organization import project_dependency_course_currents

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

from .activity import productive_witness_signs, productive_witness_option


from .mediated_efficacy import preproject_vocal_basis


def familiar_destination_rows(constitution,access):
    """A personally lived earlier site can become a possible destination.

    This is an exploratory, source-qualified practical return, not a map,
    a travel motive, a claim of conscious recollection, or present permission.
    In particular, do not enumerate objective world sites or other actors'
    histories. The existing world MOVE owner settles the actual attempt.
    """
    if constitution.actor!=access.actor:return []
    paths={}
    for path in constitution.evidence_paths:
        ref=path.get('event')
        paths[ref]=None if ref in paths else path
    episode_counts={}
    for e in constitution.lived_genesis_episodes:
        ref=e.get('event_ref')
        episode_counts[ref]=episode_counts.get(ref,0)+1
    found={}
    for e in reversed(constitution.lived_genesis_episodes):
        ref=e.get('event_ref');path=paths.get(ref)
        if (type(ref) is not str or not path or episode_counts[ref]!=1
                or type(e.get('experience_ref')) is not str
                or path.get('experience_ref')!=e['experience_ref']
                or e.get('id')!=stable_id('personally_lived_genesis_episode',{
                    'actor':constitution.actor,'event':ref,'experience':e['experience_ref']})):
            continue
        felt=e.get('actor_felt_attempt')
        actual_felt=type(felt) is str and felt==path.get('own_action')
        received_relief=bool(e.get('received_relief')) and bool(
            set(e.get('received_sign_refs',[]))&set(path.get('received_cue_refs',[])))
        if not (actual_felt or received_relief):continue
        site=e.get('location')
        if (e.get('actor')!=constitution.actor or type(site) is not str or not site
                or site==access.location or site in found
                or type(e.get('clock')) is not int or e['clock']>=access.world_clock
                ):
            continue
        found[site]={'site':site,'episode_ref':e['id'],'event_ref':e['event_ref'],
                     'experience_ref':e['experience_ref'],'experienced_clock':e['clock']}
    return list(found.values())


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
        if act=='ORIENT' and project.get('productive_witness_means'):
            for cue in productive_witness_signs(project,access):
                attention=productive_witness_option(project,access,cue)
                alts.append({'option_id':attention['attention_ref'],'actor':actor,
                    'as_of_clock':clock,'operation':act,'project_id':project['id'],
                    'grounds_status':'HISTORICALLY_REFUNCTIONED_RECEPTIVE_PROJECT_COURSE',
                    'world_request':{'operation':act,'addressed_party_ref':None,'material_object_ref':None},
                    'binding_status':'PARTICULAR_CURRENT_RECEIVABLE_SIGN',
                    'anticipated_difference':None,'beneficiary_as_apprehended':None,
                    'productive_witness_attention':attention,'source_grade':GRADE,
                    'not_actor_self_account':True,'not_world_outcome':True,
                    'priority':project.get('priority',.5)})
            continue
        expected=validate_expected_difference(project.get('expected_difference'))
        object_ref=project.get('material_object_ref') if project.get('incidental_takeup_basis') is not None else None
        if project.get('incidental_takeup_basis') is not None and (
                act not in ('INSPECT','REPAIR') or type(object_ref) is not str
                or not any(c.get('kind')=='material_object_present'
                           and c.get('material_object_ref')==object_ref for c in access.cues)):
            continue
        target=project.get('addressed_party_ref')
        if project.get('provisioning_means_basis') and act in ('WORK','BUY_FOOD'):
            # Material acquisition serves a particular care undertaking but
            # is not an addressed act or a claim on the recipient.
            target=None
        if project.get('commons_provisioning_basis') and act=='CONTRIBUTE_FOOD_COMMONS':
            target=None
        conditional=project.get('dependency_conditional_means',{}).get(act)
        human_counterpart=False
        if conditional is not None:
            other=conditional.get('counterpart_ref')
            human_counterpart=(act=='SIGNAL' and other in accessible_human_counterparts(access)
                               and other not in present)
            # A new project course reuses a particular learned coordination,
            # without turning every operation into an addressed act.
            if (conditional.get('status','ACTIVE')!='ACTIVE'
                    or conditional.get('location')!=access.location
                    or (other not in present and not human_counterpart)
                    or not any(p.get('id')==conditional.get('practice_ref')
                        and p.get('actor')==actor
                        and p.get('operation')==act
                        and p.get('coactor_ref')==conditional.get('counterpart_ref')
                        and p.get('status')=='ACQUIRED_CONDITIONAL_COORDINATION_NOT_DYAD_MASTERY'
                        for p in getattr(constitution,'joint_practices',[]))):
                continue
            target=conditional['counterpart_ref']
        if target is not None and (type(target) is not str or not target):
            raise ValueError('INVALID_PROJECT_ADDRESSED_PARTY')
        reachable=target is None or target in present or human_counterpart
        bound_target=target if reachable else None
        identity={'actor':actor,'clock':clock,'action':act,
                  'project_ref':project['id'],'expected_difference':expected,
                  'addressed_party_ref':target}
        if object_ref is not None:identity['material_object_ref']=object_ref
        historical_currents=project_dependency_course_currents(
            constitution,access,project,act,conditional)
        polarities={c['polarity'] for c in historical_currents}
        alts.append({
            **({'course_historical_currents':historical_currents,
                'course_psychodynamic_status':(
                    'UNRESOLVED_CONTRADICTION' if polarities=={'APPROACH','WITHHOLD'}
                    else 'SITUATED_HISTORICAL_COURSE_ORIENTATION')}
               if historical_currents else {}),
            'option_id':stable_id('practical_option',identity),
            'actor':actor,'as_of_clock':clock,'operation':act,
            'project_id':project['id'],'grounds_status':'AVAILABLE_SINGLE_PROJECT_COURSE',
            'anticipated_difference':expected,
            'beneficiary_as_apprehended':(
                 expected.get('beneficiary_ref') if expected else None),
            'world_request':{'operation':act,'addressed_party_ref':bound_target,
                             'material_object_ref':object_ref},
            **({'dependency_conditional_means_ref':conditional['origin_event_ref'],
                'acquired_joint_practice_ref':conditional['practice_ref'],
                'partner_consent':'MUST_BE_INDEPENDENTLY_AUTHORED'}
               if conditional is not None else {}),
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
        if human_counterpart:
            alts[-1]['binding_status']='OTHER_PRESENT_BUT_INDEPENDENT_RESPONSE_REQUIRED'
            alts[-1]['counterpart_participation_kind']='HUMAN_AUTHORED_NEIGHBOR'
            accepted=food_acceptance_alternative(access,alts[-1])
            if accepted is not None:alts.append(accepted)
    if act=='SIGNAL' and constitution.role=='child':
        own={'id':actor,'role':constitution.role,
             'power_exercises':constitution.power_exercises,
             'evidence_paths':constitution.evidence_paths,
             'practice_exposures':constitution.practice_exposures}
        early=preproject_vocal_basis(own,access.location,clock)
        if early is not None:
            # An exploratory call can now be addressed without installing a
            # caregiving orientation, goal, gratitude or consent in either actor.
            for counterpart in sorted(present):
                alts.append({
                    'option_id':stable_id('preproject_addressed_vocal_trial',{
                        'actor':actor,'clock':clock,'other':counterpart,
                        'ordinary_basis':early['id']}),
                    'actor':actor,'as_of_clock':clock,'operation':act,
                    'project_id':None,'anticipated_difference':None,
                    'beneficiary_as_apprehended':None,'priority':None,
                    'grounds_status':'PREPROJECT_ORDINARY_VOCAL_EXPLORATION',
                    'world_request':{'operation':act,'addressed_party_ref':counterpart,
                                     'material_object_ref':None},
                    'binding_status':'QUALIFIED_AS_PRESENT',
                    'source_aggregate_ref':early['id'],
                    'not_actor_self_account':True,'not_world_outcome':True,
                    'other_response_not_assumed':True,'source_grade':GRADE})
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
    if act=='MOVE':
        for destination in familiar_destination_rows(constitution,access):
            site=destination['site']
            alts.append({'option_id':stable_id('familiar_destination',{
                'actor':actor,'clock':clock,'source':destination,'from':access.location}),
                'actor':actor,'as_of_clock':clock,'operation':act,'project_id':None,
                'grounds_status':'HISTORICALLY_FAMILIAR_DESTINATION',
                'binding_status':'PAST_SITE_EXPERIENCED_CURRENT_ACCESS_NOT_ESTABLISHED',
                'world_request':{'operation':act,'addressed_party_ref':None,
                                 'material_object_ref':site},
                'familiar_destination_basis':copy(destination),
                'anticipated_difference':None,'beneficiary_as_apprehended':None,
                'priority':None,'not_actor_self_account':True,'not_world_outcome':True,
                'source_grade':GRADE})
    return alts

def offer_addressed_lexical_alternatives(access,option,focal_refs):
    """One person's voluntary speech can be addressed, without a right to reply.

    Reuse existing unaddressed project/operation choices and focal presence.
    Address is not confidentiality: others may hear the actual utterance.
    """
    if option.get('action')!='SPEAK':return []
    peers=[]
    for cue in access.cues:
        if cue.get('id') not in focal_refs:continue
        other=(cue.get('source_actor') if cue.get('kind')=='coactor_present' else
               cue.get('visitor_ref') if cue.get('kind')=='visitor_vocal_partner' else None)
        if type(other) is str and other!=access.actor and not any(x[0]==other for x in peers):
            peers.append((other,cue['id']))
    out=[]
    for base in option.get('practical_alternatives',[]):
        request=base.get('world_request',{})
        if (request.get('operation')!='SPEAK' or request.get('addressed_party_ref') is not None
                or request.get('material_object_ref') is not None
                or base.get('binding_status') not in ('NO_ADDRESSED_PARTY','UNATTRIBUTED_OPERATION')):
            continue
        for other,cue_ref in peers[:8]:
            row=copy(base)
            row.update(option_id=stable_id('addressed_lexical_choice',{
                'actor':access.actor,'clock':access.world_clock,'base':base['option_id'],
                'recipient':other,'presence_cue':cue_ref}),
                binding_status='EXACT_CURRENT_VOLUNTARY_SPEECH_ADDRESS',
                grounds_status='POSSIBLE_ADDRESSED_LEXICAL_ACT',
                speech_address_presence_ref=cue_ref,
                no_reply_consent_confidentiality_or_truth_inferred=True)
            row['world_request']['addressed_party_ref']=other
            out.append(row)
    return out


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
             'appraised_sign_tags':sorted({str(t).casefold()
                 for c in experience.get('perceived_cues',[]) if c.get('id')==sign
                 for t in c.get('tags',[]) if type(t) is str}),
             'observer_causal_attribution':'NOT_ESTABLISHED',
             'objective_success':'NOT_INFERRED','grade':GRADE,
             'actor_interpretation_not_world_truth':True}
    prior['appraisal_history'].append(receipt)
    prior['state']=appraisal
    return {'kind':'APPRAISE_EXPECTED_DIFFERENCE','expectation':ident,
            'state':appraisal,'grade':GRADE}


def start_selected_expectations(actor, selection, experience, event_ref):
    """One performed operation may serve multiple ACTUALLY selected ends.

    Reuse the existing expectation writer. Never allocate unselected pooled
    possibilities, or synthesize project identity from array order. No claim
    of fulfillment, motive or actual conscious expectation follows.
    """
    if not selection:return []
    if selection.get('project_id') is not None:
        one=start_expectation(actor,selection,experience,event_ref)
        return [one] if one is not None else []
    selected=selection.get('selected_project_refs',[])
    courses=selection.get('selected_expectation_courses',[])
    if not courses:return []
    if (experience.get('own_practical_selection')!=selection
            or selection.get('actor')!=actor.get('id')
            or selection.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT'
            or selection.get('possible_end_trial') is not None
            or len(selected)<2 or len(selected)!=len(set(selected))
            or selection.get('world_request',{}).get('addressed_party_ref') is not None
            or selection.get('world_request',{}).get('material_object_ref') is not None
            or len({c['project_id'] for c in courses})!=len(courses)):
        raise ValueError('PLURAL_EXPECTATION_SELECTION_UNQUALIFIED')
    # Validate all associations before writing any.
    for c in courses:
        p=[p for p in actor.get('projects',[]) if p.get('id')==c['project_id']]
        if (c['project_id'] not in selected or len(p)!=1
                or experience.get('own_action') not in p[0].get('means',[])
                or p[0].get('addressed_party_ref') is not None
                or validate_expected_difference(p[0].get('expected_difference'))!=c['anticipated_difference']):
            raise ValueError('PLURAL_EXPECTATION_COURSE_CONTRADICTION')
        ident=stable_id('practical_option',{'actor':actor['id'],
            'clock':selection['as_of_clock'],'action':experience['own_action'],
            'project_ref':c['project_id'],'expected_difference':c['anticipated_difference'],
            'addressed_party_ref':None})
        if ident!=c['option_id']:
            raise ValueError('PLURAL_EXPECTATION_OPTION_CONTRADICTION')
        if any(e.get('id')==stable_id('expectation',{'actor':actor['id'],
                  'event':event_ref,'option':ident}) for e in actor.get('expectations',[])):
            raise ValueError('DUPLICATE_ACTOR_EXPECTATION')
    out=[]
    for c in courses:
        e=start_expectation(actor,c,experience,event_ref)
        e['shared_selected_operation_ref']=selection['option_id']
        e['shared_selected_project_refs']=copy(selected)
        out.append(e)
    return out
