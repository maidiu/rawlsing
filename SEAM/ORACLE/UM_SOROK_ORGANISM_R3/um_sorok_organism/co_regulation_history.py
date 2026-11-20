"""SORACLE R14: material co-regulation becomes acquired, fallible practical orientation.

One aggregate period of historically scoped care CAN be material for later
development without inventing individual care scenes. Objective care hours do
not equal love, recognized benefactor, attachment certainty, the caregiver's
future consent, or a conscious autobiographical memory.

Constitution is an actor-owned read; the only psychological writer is the
existing development.admit transaction. A later ACTUALLY SENSED co-presence
can qualify a fictional semantic proposal to seek this particular person.
The world then independently decides whether that person participates.
"""
from .types import GRADE, stable_id, copy
from .organism import eligible
from .plural_care_paths import _delta


def conserve_received_period_care(recipient, period):
    """Persist one potential lived bodily condition, not scenes or affection."""
    if type(period) is not dict or period.get('recipient')!=recipient.get('id'):
        raise ValueError('COREGULATION_WRONG_RECIPIENT')
    if not (period.get('id') and period.get('giver') and
            period.get('source_ref') and
            period.get('grade')=='SOURCEFREE_QUALIFIED_AGGREGATE_CARE'):
        raise ValueError('COREGULATION_UNQUALIFIED_PERIOD')
    hours=period.get('modeled_labor_hours')
    effect=period.get('recipient_comfort_effect_model')
    if type(hours) not in (int,float) or type(effect) not in (int,float):
        raise ValueError('COREGULATION_INVALID_PERIOD_MAGNITUDE')
    if hours<=0 or effect<=0:return None
    if recipient['body']['sensor']<.05:
        # The world may model material care without inferring that the person
        # registered its social source through this sensory system.
        return None
    ident=stable_id('undergone_care_period',{
        'actor':recipient['id'],'world_ref':period['id']})
    records=recipient.setdefault('undergone_care_periods',[])
    if any(x.get('id')==ident for x in records):
        raise ValueError('COREGULATION_DUPLICATE_PERIOD_EXPOSURE')
    row={
        'id':ident,'actor':recipient['id'],'caregiver_ref':period['giver'],
        'world_period_ref':period['id'],'source_ref':period['source_ref'],
        'location':period['site'],'from_clock':period['start_clock'],
        'through_clock':period['end_clock'],
        'aggregate_modeled_care_hours':round(hours,3),
        'aggregate_modeled_bodily_relief':round(effect,5),
        'historical_exposure_kind':'MODELED_BODILY_CO_REGULATION',
        'caregiver_consent_at_individual_unrendered_times':'NOT_PROVED',
        'actor_identified_source_of_relief':'NOT_ESTABLISHED',
        'attachment_or_trust':'NOT_ESTABLISHED',
        'conscious_memories_of_each_episode':'NOT_GENERATED',
        'grade':GRADE}
    records.append(row)
    return row


def possible_acquired_regulation(actor,experience,event_ref):
    """Current received co-presence is required to reinterpret a prior period."""
    if actor.get('id')!=experience.get('actor') or not event_ref:
        raise ValueError('COREGULATION_FOREIGN_EXPERIENCE')
    received={c['id']:c for c in experience.get('perceived_cues',[])
              if type(c) is dict and type(c.get('id')) is str
              and c.get('kind')=='coactor_present'
              and type(c.get('source_actor')) is str}
    if not received:return []
    known={x.get('caregiver_ref') for x in
           actor.get('co_regulation_orientations',[])
           if x.get('status')=='ACTIVE'}
    results=[]
    for partner in sorted({c['source_actor'] for c in received.values()}):
        if partner in known:continue
        history=[x for x in actor.get('undergone_care_periods',[])
                 if x.get('caregiver_ref')==partner and
                 x.get('aggregate_modeled_care_hours',0)>0 and
                 x.get('through_clock',float('inf'))<=
                      experience.get('clock',float('inf'))]
        if not history:continue
        cues=[c for c in received.values() if c['source_actor']==partner]
        results.append({
            'kind':'POSSIBLE_ACQUIRED_CO_REGULATION',
            'source_care_period_refs':[x['id'] for x in history[-24:]],
            'caregiver_ref':partner,'current_perceived_cue_ref':cues[0]['id'],
            'candidate_operations':['SIGNAL','ORIENT','NO_NEW_ORIENTATION'],
            'readiness':'PARTICULAR_HISTORICAL_RELATIONAL_POSSIBILITY',
            'psychic_valuation':'NOT_YET_ADMITTED',
            'not_a_conscious_attribution_of_care':True,
            'caregiver_future_behavior':'INDEPENDENT_UNKNOWN',
            'no_fictitious_microepisode':True,'grade':GRADE})
    return results[:6]


def admit_co_regulation(actor,experience,event_ref,proposal):
    if actor.get('id')!=experience.get('actor'):
        raise ValueError('COREGULATION_ADMISSION_FOREIGN_ACTOR')
    partner=proposal.get('caregiver_ref')
    cue_id=proposal.get('perceived_cue_ref')
    if type(partner) is not str or not partner or partner==actor['id']:
        raise ValueError('COREGULATION_ADMISSION_INVALID_CAREGIVER')
    matches=[c for c in experience.get('perceived_cues',[])
             if type(c) is dict and c.get('id')==cue_id and
             c.get('kind')=='coactor_present' and
             c.get('source_actor')==partner]
    if len(matches)!=1:
        raise ValueError('COREGULATION_ADMISSION_NO_LIVED_COPRESENCE')
    referenced=proposal.get('period_refs',[])
    lived_refs=proposal.get('lived_care_event_refs',[])
    if (type(referenced) is not list or type(lived_refs) is not list or
            not 1<=len(referenced)+len(lived_refs)<=40 or
            len(referenced)>24 or len(lived_refs)>16 or
            any(type(x) is not str for x in referenced+lived_refs) or
            len(set(referenced+lived_refs))!=len(referenced)+len(lived_refs)):
        raise ValueError('COREGULATION_ADMISSION_NO_QUALIFIED_SOURCES')
    personal={x['id']:x for x in actor.get('undergone_care_periods',[])
              if x.get('caregiver_ref')==partner}
    lived={x['id']:x for x in actor.get('experienced_care_events',[])
           if x.get('giver_ref')==partner and
           x.get('event_ref')!=event_ref}
    if (any(x not in personal for x in referenced) or
            any(x not in lived for x in lived_refs)):
        raise ValueError('COREGULATION_ADMISSION_FOREIGN_CARE_HISTORY')
    if any(x.get('caregiver_ref')==partner and x.get('status')=='ACTIVE'
           for x in actor.get('co_regulation_orientations',[])):
        raise ValueError('COREGULATION_ADMISSION_ALREADY_ACTIVE')
    ident=stable_id('acquired_coregulation',{
        'actor':actor['id'],'partner':partner,'event':event_ref,
        'periods':referenced,'lived_events':lived_refs,'cue':cue_id})
    row={
        'id':ident,'actor':actor['id'],'caregiver_ref':partner,
        'origin_event':event_ref,'experience_ref':experience.get('ref'),
        'current_perceived_cue_ref':cue_id,
        'source_care_period_refs':copy(referenced),
        'source_lived_care_event_refs':copy(lived_refs),
        'possible_operation':'SIGNAL','status':'ACTIVE',
        'scope_location':experience.get('location'),
        'origin_event_clock':experience.get('clock'),
        'actor_identifies_help_as_social_power':'NOT_ESTABLISHED',
        'caregiver_will_respond':'NOT_ASSUMED',
        'affection_and_moral_merit':'NOT_INFERRED',
        'conscious_actor_reason':'NOT_INFERRED',
        'hypothesis':'ACQUIRED_PARTICULAR_CO_REGULATION_ORIENTATION',
        'grade':GRADE}
    actor.setdefault('co_regulation_orientations',[]).append(row)
    return {'kind':'ACQUIRE_CO_REGULATION_ORIENTATION',
            'orientation_ref':ident,'source_periods':len(referenced),
            'source_lived_events':len(lived_refs),
            'recipient':actor['id'],'caregiver_ref':partner,'grade':GRADE}


def sourcefree_co_regulation_proposal(possibilities):
    """One uniquely sourced prior caregiver, not a universal care reflex."""
    if len(possibilities)!=1:return []
    p=possibilities[0]
    return [{'kind':'ACQUIRE_CO_REGULATION_ORIENTATION',
             'caregiver_ref':p['caregiver_ref'],
             'period_refs':p['source_care_period_refs'],
             'perceived_cue_ref':p['current_perceived_cue_ref'],
             'sourcefree_no_conscious_knowledge':True}]


def recruit_co_regulation(constitution,access):
    if constitution.actor!=access.actor:
        raise ValueError('COREGULATION_RECRUITMENT_FOREIGN_ACTOR')
    present={x.get('source_actor') for x in access.cues
             if type(x) is dict and x.get('kind')=='coactor_present'}
    offered=[];readset=[]
    if not eligible(constitution.body,'SIGNAL')[0]:
        return {'offered':offered,'readset':readset}
    # A corresponding caregiver is *present*, but can still decline to act.
    suspended=[]
    for record in constitution.co_regulation_orientations:
        if record.get('status')!='ACTIVE' or record.get('caregiver_ref') not in present:
            continue
        if record.get('scope_location') not in (None,access.location):
            continue
        if record.get('interpretation_phase')=='UNRESOLVED_AFTER_NONRESPONSE':
            # Prior care still happened; a later unsuccessful call can
            # destabilize THIS fallback without erasing material history.
            readset.append(record['id'])
            suspended.append({'orientation_ref':record['id'],
                'previous_caregiver_ref':record['caregiver_ref'],
                'history_not_deleted':True,
                'does_not_identify_caregiver_intention':True,
                'grade':GRADE})
            continue
        personally_sensed_support=[
            {'response_ref':x['id'],
             'event_clock':x.get('event_clock'),
             'bodily_regulation_sensed':True}
            for x in record.get('response_history',[])
            if x.get('felt_bodily_relief_on_this_call',False) is True
            and type(x.get('event_clock')) is int]
        personally_sensed_support += [
            {'response_ref':x['id'],'event_clock':x.get('clock'),
             'bodily_regulation_sensed':True}
            for x in getattr(constitution,'experienced_care_events',[])
            if x.get('giver_ref')==record['caregiver_ref']
            and type(x.get('clock')) is int
            and x.get('clock')>=record.get('origin_event_clock',0)]
        offered.append({
            'personally_sensed_support_history':sorted(
                personally_sensed_support,key=lambda x:x['event_clock']),
            'caregiver_ref':record['caregiver_ref'],
            'orientation_ref':record['id'],
            'source_care_period_refs':copy(record['source_care_period_refs']),
            'action':'SIGNAL',
            'score':.22,
            'historical_ground':'SOURCEFREE_LIVED_CO_REGULATION_HISTORY',
            'not_child_conscious_causal_theory':True,
            'coactor_consent':'INDEPENDENT_UNDECIDED',
            'grade':GRADE})
        readset.append(record['id'])
    return {'offered':offered,'readset':readset,
            'suspended_after_contradiction':suspended,'grade':GRADE}


def addressed_signal_alternatives(constitution,access,option):
    if option.get('action')!='SIGNAL':return []
    history=recruit_co_regulation(constitution,access)
    return [{
        'option_id':stable_id('historically_addressed_signal',{
            'actor':constitution.actor,'clock':constitution.clock,
            'partner':p['caregiver_ref'],'orientation':p['orientation_ref']}),
        'actor':constitution.actor,'as_of_clock':constitution.clock,
        'operation':'SIGNAL','project_id':None,
        'grounds_status':'HISTORICALLY_ACQUIRED_CO_REGULATION',
        'anticipated_difference':None,
        'beneficiary_as_apprehended':'NOT_INFERRED',
        'world_request':{
            'operation':'SIGNAL',
            'addressed_party_ref':p['caregiver_ref'],
            'material_object_ref':None},
        'binding_status':'HISTORICALLY_ADDRESSED_PARTNER_PRESENT',
        'origin_orientation_ref':p['orientation_ref'],
        'source_period_refs':p['source_care_period_refs'],
        'personally_sensed_support_history':copy(
            p.get('personally_sensed_support_history',[])),
        'caregiver_participation_not_required_or_assumed':True,
        'not_a_conscious_reason_or_love_claim':True,
        'source_grade':GRADE}
        for p in history['offered']]


def choose_historically_situated_signal(options,body):
    """Fallible fallback: a need-bearing actor can *try* to summon a prior carer.

    This is not a universal infant reflex; it only operates if an already
    admitted orientation and the person's actual current availability match.
    A project, contrary pressure or ambiguous eligible caregivers defeats it.
    """
    if type(body) is not dict:
        return None
    # The child can seek a historically constituted caregiver amid hunger,
    # exhaustion or discomfort. No universal 'want affection' score is
    # manufactured, and no independent Other is precommitted to respond.
    need=(body.get('comfort',1)<.43 or body.get('nutrition',1)<.55
          or body.get('rest',1)<.40)
    if not need:
        return None
    if any(o.get('project_courses') for o in options):
        return None
    qualified=[]
    for o in options:
        if o.get('action')!='SIGNAL' or o.get('psychodynamic_status')=='UNRESOLVED_CONTRADICTION':
            continue
        for alt in o.get('practical_alternatives',[]):
            if alt.get('grounds_status')=='HISTORICALLY_ACQUIRED_CO_REGULATION':
                qualified.append(alt)
    if len(qualified)!=1:return None
    return {
        'action':'SIGNAL','practical_option_id':qualified[0]['option_id'],
        'project_id':None,
        'selection_grade':'SOURCEFREE_RELATIONALLY_GROUNDED_CALL_ATTEMPT',
        'other_response_is_independently_settled':True}


def record_lived_co_regulation_response(actor, experience, selection, event_ref,
                                       bodily_before=None,bodily_after=None):
    """The learner's actually attempted signal acquires a fallible afterlife.

    'World did not join' is not automatically 'caregiver does not love me'.
    A sign of attempted action must be received by this actor. The partner
    must have been frozen in the *actor-selected practical alternative*,
    not supplied by a third-party retrospective narrative.
    """
    if experience.get('actor')!=actor.get('id') or not event_ref:
        raise ValueError('COREGULATION_RESPONSE_FOREIGN_ACTOR')
    selected=(selection or {}).get('source_co_regulation_orientation_ref')
    if selected is None:return None
    if experience.get('own_action')!='SIGNAL' or (
            experience.get('felt_enactment') or {}).get(
                'attempted_operation')!='SIGNAL':
        raise ValueError('COREGULATION_RESPONSE_NOT_OWN_SIGNAL')
    orientations=[x for x in actor.get('co_regulation_orientations',[])
                  if x.get('id')==selected]
    if len(orientations)!=1:
        raise ValueError('COREGULATION_RESPONSE_UNKNOWN_ORIENTATION')
    original=orientations[0]
    addressed=(selection or {}).get('world_request',{}).get('addressed_party_ref')
    if addressed!=original['caregiver_ref']:
        raise ValueError('COREGULATION_RESPONSE_NOT_SELECTED_CAREGIVER')
    signs=[c for c in experience.get('perceived_cues',[])
           if type(c) is dict and c.get('kind')=='performed_signal'
           and type(c.get('id')) is str and
           c.get('source_actor')==actor['id']]
    if len(signs)!=1:return None
    status=experience.get('status')
    if status not in ('PARTIAL','PERFORMED','BLOCKED'):
        return None
    delta=(_delta(bodily_before['comfort'],bodily_after['comfort'],
                  'RESPONDED_CALL_COMFORT')
           if bodily_before is not None and bodily_after is not None
           else 0.)
    felt_relief=(status=='PERFORMED' and delta>=.025)
    meaning=('UNFINISHED_ATTEMPT_WITH_RECEIVED_SIGN'
             if status=='PARTIAL' else
             'PERFORMED_SIGNAL_NOT_PROOF_OF_CARE'
             if status=='PERFORMED' else
             'BODILY_BLOCKED_SIGNAL_NOT_SOCIAL_REJECTION')
    ident=stable_id('lived_co_regulation_response',{
        'actor':actor['id'],'orientation':selected,'event':event_ref,
        'sign':signs[0]['id']})
    if any(x.get('id')==ident for x in original.get('response_history',[])):
        raise ValueError('COREGULATION_DUPLICATE_LIVED_RESPONSE')
    receipt={
        'id':ident,'actor':actor['id'],'orientation_ref':selected,
        'caregiver_ref':addressed,'event_ref':event_ref,
        'experience_ref':experience.get('ref'),
        'received_sign_ref':signs[0]['id'],
        'event_clock':experience.get('clock'),
        'body_comfort_difference_on_call':delta,
        'felt_bodily_relief_on_this_call':felt_relief,
        'relief_not_proof_of_other_intent':True,
        'attempted_operation':'SIGNAL',
        'actor_experienced_attempt_status':status,
        'received_sign_description':signs[0].get('description'),
        'analyst_qualified_experience_class':meaning,
        'caregiver_intention':'NOT_INFERRED_FROM_NONRESPONSE',
        'experienced_quality_of_care':'NOT_MEASURED',
        'does_not_retroactively_change_original_care':True,
        'grade':GRADE}
    original.setdefault('response_history',[]).append(receipt)
    return receipt


def possible_revision_after_nonresponse(actor,experience,event_ref):
    """Recurrent actually sensed unfinished calls may destabilize a shortcut.

    No permanent rupture, rejection, pathologizing diagnosis or new motive
    is declared. The semantic developmental owner may abstain or provisionally
    suspend the automatic repeat-call policy while retaining the history.
    """
    if actor.get('id')!=experience.get('actor'):
        raise ValueError('COREGULATION_REVISION_FOREIGN_ACTOR')
    candidates=[]
    for orientation in actor.get('co_regulation_orientations',[]):
        if orientation.get('status')!='ACTIVE' or orientation.get(
                'interpretation_phase','PROVISIONAL')!='PROVISIONAL':
            continue
        recent=[x for x in orientation.get('response_history',[])
                if x.get('analyst_qualified_experience_class')==
                'UNFINISHED_ATTEMPT_WITH_RECEIVED_SIGN']
        if (len({x['event_ref'] for x in recent})<2
                or recent[-1]['event_ref']!=event_ref):
            continue
        candidates.append({
            'kind':'POSSIBLE_REORGANIZATION_OF_CO_REGULATION',
            'orientation_ref':orientation['id'],
            'recent_nonresponse_ref':recent[-1]['id'],
            'contradicting_lived_response_refs':[x['id'] for x in recent[-8:]],
            'candidate':'SUSPEND_EXCLUSIVE_CALL_SHORTCUT',
            'not_an_inference_of_lack_of_love':True,
            'not_a_child_conscious_theory':True,
            'no_permanent_loss_of_prior_lived_support':True,
            'grade':GRADE})
    return candidates


def sourcefree_revision_proposal(candidates):
    """Conservative example of real actor-relative expectation revision."""
    if len(candidates)!=1:return []
    c=candidates[0]
    return [{'kind':'REVISE_CO_REGULATION_ORIENTATION',
             'orientation_ref':c['orientation_ref'],
             'latest_response_ref':c['recent_nonresponse_ref'],
             'interpretation_phase':'UNRESOLVED_AFTER_NONRESPONSE',
             'grade':GRADE}]


def admit_co_regulation_revision(actor,experience,event_ref,proposal):
    if actor.get('id')!=experience.get('actor'):
        raise ValueError('COREGULATION_REVISE_FOREIGN_ACTOR')
    ident=proposal.get('orientation_ref')
    current=[x for x in actor.get('co_regulation_orientations',[])
             if x.get('id')==ident and x.get('status')=='ACTIVE']
    if len(current)!=1:
        raise ValueError('COREGULATION_REVISE_UNKNOWN_ACTIVE_ORIENTATION')
    orientation=current[0]
    response=[x for x in orientation.get('response_history',[])
              if x.get('id')==proposal.get('latest_response_ref')
              and x.get('event_ref')==event_ref
              and x.get('analyst_qualified_experience_class')==
                 'UNFINISHED_ATTEMPT_WITH_RECEIVED_SIGN']
    if len(response)!=1:
        raise ValueError('COREGULATION_REVISE_NO_CURRENT_LIVED_RESPONSE')
    sign={c.get('id') for c in experience.get('perceived_cues',[])
          if type(c) is dict and type(c.get('id')) is str}
    if response[0]['received_sign_ref'] not in sign:
        raise ValueError('COREGULATION_REVISE_NO_CURRENT_PERCEPTION')
    previous=[x for x in orientation.get('response_history',[])
              if x.get('analyst_qualified_experience_class')==
                 'UNFINISHED_ATTEMPT_WITH_RECEIVED_SIGN']
    if len({x['event_ref'] for x in previous})<2:
        raise ValueError('COREGULATION_REVISE_LACKS_DISTINCT_HISTORY')
    phase=proposal.get('interpretation_phase')
    if phase!='UNRESOLVED_AFTER_NONRESPONSE':
        raise ValueError('COREGULATION_REVISE_UNLICENSED_PHASE')
    old=orientation.get('interpretation_phase','PROVISIONAL')
    if old==phase:
        raise ValueError('COREGULATION_REVISE_DUPLICATE_PHASE')
    orientation.setdefault('interpretation_history',[]).append({
        'before':old,'after':phase,'changed_at_event':event_ref,
        'experience_ref':experience.get('ref'),
        'new_lived_response_ref':response[0]['id'],
        'could_still_seek_other_help':'UNKNOWN',
        'caregiver_moral_truth':'NOT_INFERRED',
        'grade':GRADE})
    orientation['interpretation_phase']=phase
    return {'kind':'REVISE_CO_REGULATION_ORIENTATION',
            'orientation_ref':ident,'phase':phase,'grade':GRADE}
