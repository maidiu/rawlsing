"""SORACLE R11 / Astra 6,7,17,19: ordinary life has discontinuities.

Routine coverage is cheap; a source-qualified deadline, expiring signal or
material interruption gets a detailed *actor-owned* opportunity. No player
chooses the action. This does not invent unperformed micro-events, pretend a
scheduling threshold was an experienced violation, or close other actors'
rights. The actual runtime/world owners still author their own transactions.
"""
from .types import GRADE, stable_id, copy
from .material_conjunction import next_material_gate_discontinuity

MAX_HORIZON=3650


# A human can explicitly undertake a bounded act in this modeled world.
# This is not a reciprocal agreement, a calendar notification, or evidence
# that its recipient understood the undertaking.
HUMAN_OFFER_KIND='HUMAN_PROMISED_FOOD_OFFER'

def settle_human_offer_deadlines(world):
    """Expire only this explicitly authored, fully covered event contract.

    The modeled clock is exclusive at due_clock. No unwritten discretionary
    visitor offer can occur during aggregate passage. A missed offer is not
    proof of refusal, culpability, emotion, or an actor's knowledge.
    """
    settled=[]
    for row in world.get('scheduled_obligations',[]):
        if (row.get('kind')==HUMAN_OFFER_KIND and row.get('status')=='PENDING'
                and world['clock']>=row['due_clock']):
            row['status']='WINDOW_ELAPSED_WITHOUT_AUTHORED_OFFER'
            row['settled_at_clock']=row['due_clock']
            row['no_recipient_appraisal_or_motive_inferred']=True
            settled.append(row['id'])
    return settled


def record_human_offer_commitment(world, user, recipient, location, due, event_ref):
    """Called only by the existing committed human contribution owner."""
    if type(due) is not int or not world['clock']<due<=world['clock']+MAX_HORIZON:
        raise ValueError('HUMAN_OFFER_INVALID_DEADLINE')
    if any(row.get('kind')==HUMAN_OFFER_KIND and row.get('status')=='PENDING'
           and row.get('responsible_actor')==user and row.get('recipient')==recipient
           for row in world.get('scheduled_obligations',[])):
        raise ValueError('HUMAN_OFFER_ALREADY_PENDING')
    row={'id':stable_id('human_offer_commitment',{'world':world['id'],'event':event_ref}),
         'kind':HUMAN_OFFER_KIND,'responsible_actor':user,'recipient':recipient,
         'location':location,'origin_clock':world['clock'],'due_clock':due,
         'source_user_event_ref':event_ref,'status':'PENDING',
         'recipient_consent_not_assumed':True,'grade':GRADE}
    world.setdefault('scheduled_obligations',[]).append(row)
    return row['id']


def withdraw_human_offer_commitment(world,user,commitment_ref,event_ref):
    """Prospective explicit withdrawal, never a recipient's knowledge.

    This owner settles a previously authored pending OFFER undertaking, not
    a mutually accepted appointment or a transfer. The actual exclusive
    modeled deadline and any earlier performance remain binding history.
    """
    matches=[r for r in world.get('scheduled_obligations',[])
        if r.get('id')==commitment_ref and r.get('kind')==HUMAN_OFFER_KIND
        and r.get('responsible_actor')==user]
    if len(matches)!=1:
        raise ValueError('HUMAN_WITHDRAWAL_NO_OWN_COMMITMENT')
    row=matches[0]
    if (row.get('status')!='PENDING'
            or not row['origin_clock']<world['clock']<row['due_clock']):
        raise ValueError('HUMAN_WITHDRAWAL_WINDOW_NOT_PENDING')
    row.update(status='WITHDRAWN_BY_AUTHORED_ACT',
               settled_at_clock=world['clock'],
               withdrawal_user_event_ref=event_ref,
               no_recipient_notification_or_appraisal_inferred=True)
    return row['id']


def record_authored_food_offer(world,user,recipient,location,event_ref):
    """Fulfillment is the promised OFFER, not recipient assent or feeding."""
    matches=[r for r in world.get('scheduled_obligations',[])
        if r.get('kind')==HUMAN_OFFER_KIND and r.get('status')=='PENDING'
        and r.get('responsible_actor')==user and r.get('recipient')==recipient
        and r.get('location')==location
        and r['origin_clock']<world['clock']<r['due_clock']]
    if len(matches)>1:raise ValueError('AMBIGUOUS_HUMAN_OFFER_COMMITMENT')
    if not matches:return None
    row=matches[0]
    row.update(status='OFFER_AUTHORED_IN_WINDOW',
               settled_at_clock=world['clock'],fulfillment_user_event_ref=event_ref,
               actual_transfer_not_established=True)
    return row['id']


MEETING_KIND='HUMAN_ACTOR_MEETING_WINDOW'
MEETING_OPEN=frozenset(('PROPOSED','ACCEPTED','CHECKED_IN'))
MEETING_ACTIONS={'ACCEPT_MEETING':'PROPOSE_MEETING','MEET_VISITOR':'CHECK_IN_MEETING'}
MEETING_SIGNS={'ACCEPT_MEETING':'visitor_meeting_proposal','MEET_VISITOR':'visitor_meeting_checkin'}


def meeting_record(world,ref):
    rows=[r for r in world.get('scheduled_obligations',[])
          if r.get('id')==ref and r.get('kind')==MEETING_KIND]
    if len(rows)!=1:raise ValueError('MEETING_UNKNOWN_OR_AMBIGUOUS')
    return rows[0]


def record_meeting_proposal(world,user,recipient,location,due,event_ref,*,replaces=None):
    # Two particular future modeled transitions, not hours or real-human
    # calendar time. Assent requires an immediate actual proposal encounter.
    if type(due) is not int or not world['clock']+3<due<=world['clock']+MAX_HORIZON:
        raise ValueError('MEETING_INVALID_FUTURE_WINDOW')
    if any(r.get('kind')==MEETING_KIND and r.get('status') in MEETING_OPEN
           and r.get('responsible_actor')==user and r.get('recipient')==recipient
           and r.get('due_clock')==due for r in world.get('scheduled_obligations',[])):
        raise ValueError('MEETING_DUPLICATE_OPEN_WINDOW')
    row={'id':stable_id('meeting_window',{'world':world['id'],'proposal':event_ref}),
         'kind':MEETING_KIND,'responsible_actor':user,'recipient':recipient,
         'location':location,'origin_clock':world['clock'],'due_clock':due,
         'checkin_clock':due-2,'meeting_clock':due-1,
         'source_user_event_ref':event_ref,'status':'PROPOSED',
         'no_actor_assent_or_real_calendar_inferred':True,'grade':GRADE}
    if replaces is not None:
        old=meeting_record(world,replaces)
        if (old['responsible_actor']!=user or old['recipient']!=recipient
                or old['status']!='WITHDRAWN_BY_AUTHORED_ACT'
                or old.get('replacement_meeting_ref') is not None
                or old['due_clock']==due
                or old['settled_at_clock']>=world['clock']):
            raise ValueError('MEETING_REPLACEMENT_NOT_QUALIFIED')
        row['replaces_meeting_ref']=old['id']
        old['replacement_meeting_ref']=row['id']
    world.setdefault('scheduled_obligations',[]).append(row)
    return row['id']


def withdraw_meeting(world,user,ref,event_ref):
    """Close an explicitly owned open window, without rewriting its assent.

    The administrative act consumes its actual transition. It neither
    supplies a notification nor a psychological consequence to the Other.
    A replacement is a distinct proposal with a distinct assent.
    """
    row=meeting_record(world,ref)
    if (row['responsible_actor']!=user or row['status'] not in MEETING_OPEN
            or not row['origin_clock']<world['clock']<row['meeting_clock']):
        raise ValueError('MEETING_WITHDRAWAL_NOT_QUALIFIED')
    row.update(status='WITHDRAWN_BY_AUTHORED_ACT',
               withdrawn_from_status=row['status'],settled_at_clock=world['clock'],
               withdrawal_user_event_ref=event_ref,
               no_recipient_notification_or_appraisal_inferred=True)
    return row


def qualify_meeting_checkin(world,user,ref,location):
    row=meeting_record(world,ref)
    if (row['responsible_actor']!=user or row['location']!=location
            or row['status']!='ACCEPTED'
            or world['clock']+1!=row['checkin_clock']):
        raise ValueError('MEETING_CHECKIN_NOT_AUTHORIZED_AT_THIS_CLOCK')
    return row


def record_meeting_checkin(world,user,ref,location,event_ref):
    row=meeting_record(world,ref)
    if (row['responsible_actor']!=user or row['location']!=location
            or row['status']!='ACCEPTED' or world['clock']!=row['checkin_clock']):
        raise ValueError('MEETING_CHECKIN_NOT_AUTHORIZED_AT_THIS_CLOCK')
    row.update(status='CHECKED_IN',checkin_user_event_ref=event_ref)
    return row


def settle_meeting_deadlines(world):
    settled=[]
    for row in world.get('scheduled_obligations',[]):
        if (row.get('kind')!=MEETING_KIND or row.get('status') not in MEETING_OPEN
                or world['clock']<row['meeting_clock']):continue
        row.update(status={'PROPOSED':'ELAPSED_WITHOUT_ACTOR_ASSENT',
                           'ACCEPTED':'ELAPSED_WITHOUT_ACTUAL_CHECK_IN',
                           'CHECKED_IN':'ELAPSED_WITHOUT_ACTUAL_MEETING'}[row['status']],
                   settled_at_clock=row['meeting_clock'],
                   waiting_breach_or_actor_appraisal='NOT_ESTABLISHED')
        settled.append(row['id'])
    return settled


def meeting_options(constitution,access,action):
    """Only a current actor-local qualified sign can issue an exact choice."""
    if action not in MEETING_ACTIONS:return []
    out=[]
    for cue in access.cues:
        if (cue.get('kind')!=MEETING_SIGNS[action]
                or cue.get('clock')!=access.world_clock
                or cue.get('private_to')!=constitution.actor
                or any(type(cue.get(k)) is not str for k in
                       ('meeting_ref','visitor_ref','visitor_event_ref'))
                or any(type(cue.get(k)) is not int for k in
                       ('checkin_clock','meeting_clock'))):continue
        out.append({'option_id':stable_id('meeting_choice',{
            'actor':constitution.actor,'clock':access.world_clock,
            'action':action,'cue':cue['id'],'meeting':cue['meeting_ref']}),
            'actor':constitution.actor,'as_of_clock':access.world_clock,
            'operation':action,'project_id':None,
            'grounds_status':'ACTUAL_ADDRESSED_MEETING_SIGN',
            'binding_status':'EXACT_CURRENT_HUMAN_MEETING_SIGN',
            'world_request':{'operation':action,'addressed_party_ref':cue['visitor_ref'],
                             'material_object_ref':None},
            'anticipated_difference':None,'meeting_ref':cue['meeting_ref'],
            'meeting_source_user_event_ref':cue['visitor_event_ref'],
            'meeting_source_cue_ref':cue['id'],
            'meeting_checkin_clock':cue['checkin_clock'],
            'meeting_clock':cue['meeting_clock'],
            'not_future_presence_or_shared_motive':True,'grade':GRADE})
    return out


def qualified_meeting_receipt(world,actor,attempt,ledger_event):
    """Actual user authorship, exact current source, actor selection rechecked."""
    from .types import digest
    from .organism import eligible
    op=MEETING_ACTIONS.get(attempt.action)
    if op is None or attempt.intention!='ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE':
        return None
    selected=attempt.practical_selection.get('selected_meeting')
    if type(selected) is not dict or type(ledger_event) is not dict:return None
    env=ledger_event.get('envelope',{});payload=env.get('payload',{})
    loc=world.get('positions',{}).get(actor['id'])
    visitor=world.get('neighbor_users',{}).get(attempt.target,{})
    if (ledger_event.get('kind')!='NEIGHBOR_USER_CONTRIBUTION'
            or env.get('world')!=world['id'] or ledger_event.get('clock')!=world['clock']
            or payload.get('performed') is not True or payload.get('user')!=attempt.target
            or visitor.get('present') is not True or visitor.get('location')!=loc
            or attempt.target in world['positions']
            or selected.get('meeting_source_user_event_ref')!=payload.get('user_event_ref')
            or not eligible(actor['body'],attempt.action)[0]):return None
    events=[e for e in world.get('neighbor_user_events',[])
            if e.get('event_ref')==payload.get('user_event_ref')]
    if len(events)!=1:return None
    e=events[0];ref=selected.get('meeting_ref')
    try:row=meeting_record(world,ref)
    except ValueError:return None
    authored={'user':attempt.target,'operation':op,'text':None,'destination':None}
    if op=='PROPOSE_MEETING':
        authored.update(target_actor_ref=actor['id'],due_clock=row['due_clock'])
        if 'replaces_meeting_ref' in row:
            if e.get('target_commitment_ref')!=row['replaces_meeting_ref']:return None
            authored['target_commitment_ref']=row['replaces_meeting_ref']
        valid=(row['status']=='PROPOSED' and row['origin_clock']==world['clock']
               and row['source_user_event_ref']==e.get('event_ref')
               and world['clock']+1<row['checkin_clock'])
    else:
        authored.update(target_commitment_ref=ref)
        valid=(row['status']=='CHECKED_IN' and row['checkin_clock']==world['clock']
               and row['checkin_user_event_ref']==e.get('event_ref')
               and row['meeting_clock']==world['clock']+1)
    if (not valid or row['responsible_actor']!=attempt.target
            or row['recipient']!=actor['id'] or row['location']!=loc
            or e.get('operation')!=op or e.get('status')!='PERFORMED'
            or e.get('user')!=attempt.target or e.get('destination')!=loc
            or e.get('clock')!=world['clock'] or e.get('meeting_ref')!=ref
            or payload.get('meeting_ref')!=ref
            or e.get('payload_hash')!=digest(authored)
            or payload.get('payload_hash')!=e['payload_hash']
            or e.get('event_ref')!=stable_id('neighbor_user',{
                'user':attempt.target,'request_id':e.get('request_id'),
                'payload_hash':e['payload_hash']})):return None
    signs=[q for q in world.get('cues',[])
           if q.get('id')==selected.get('meeting_source_cue_ref')
           and q.get('id') in payload.get('candidate_cue_refs',[])
           and q.get('kind')==MEETING_SIGNS[attempt.action]
           and q.get('private_to')==actor['id'] and q.get('location')==loc
           and q.get('visitor_ref')==attempt.target
           and q.get('visitor_event_ref')==e['event_ref']
           and q.get('meeting_ref')==ref and q.get('clock')==world['clock']
           and q.get('last_access_clock',-1)>=world['clock']
           and q.get('checkin_clock')==row['checkin_clock']
           and q.get('meeting_clock')==row['meeting_clock']
           and actor['body']['sensor']>=q.get('threshold',.05)]
    if len(signs)!=1:return None
    return {'actor':actor['id'],'visitor_ref':attempt.target,'operation':op,
            'meeting_ref':ref,'user_event_ref':e['event_ref'],
            'ledger_ref':ledger_event['id'],'clock':world['clock'],
            'cue':dict(signs[0]),'grade':GRADE}


def perform_meeting_action(world,attempt,receipt):
    if (receipt is None or receipt.get('actor')!=attempt.actor
            or receipt.get('operation')!=MEETING_ACTIONS.get(attempt.action)):
        return 'BLOCKED','NO_QUALIFIED_CURRENT_MEETING_OCCASION',None
    row=meeting_record(world,receipt['meeting_ref'])
    if attempt.action=='ACCEPT_MEETING':
        row.update(status='ACCEPTED',accepted_at_clock=world['clock']+1,
                   acceptance_source_user_event_ref=receipt['user_event_ref'])
        return 'PERFORMED','PARTICULAR_MEETING_ACCEPTED',row['id']
    row.update(status='MEETING_PERFORMED',settled_at_clock=world['clock']+1,
               actual_actor_ref=attempt.actor,
               no_future_consent_or_shared_motive_inferred=True)
    return 'PERFORMED','PARTICULAR_MEETING_PERFORMED',row['id']


def next_discontinuity(world, actors, horizon):
    if type(horizon) is not int or not 1<=horizon<=MAX_HORIZON:
        raise ValueError('CONTINUITY_UNSUPPORTED_HORIZON')
    clock=world.get('clock')
    if type(clock) is not int or clock < 0:
        raise ValueError('CONTINUITY_INVALID_WORLD_CLOCK')
    end=clock+horizon
    candidates=[]
    family=world.get('family_genesis',{})
    if family.get('stage')=='CONCEPTION_ADMITTED':
        birth=family['selected_pathway']['birth_clock']
        if clock<=birth<=end:
            candidates.append({'at':birth,'kind':'CONDITIONAL_FAMILY_BIRTH','actor':None,
                'source_ref':family['conception']['id'],'grade':GRADE})
    for obligation in world.get('scheduled_obligations',[]):
        if not isinstance(obligation,dict):continue
        if obligation.get('kind')==MEETING_KIND:
            if (obligation.get('status') in MEETING_OPEN
                    and clock<obligation['meeting_clock']<=end):
                candidates.append({'at':obligation['meeting_clock'],
                    'kind':'MEETING_WINDOW_ELAPSES','actor':None,
                    'source_ref':obligation['id'],
                    'not_waiting_breach_or_actor_appraisal':True})
            continue
        if obligation.get('status')!='PENDING':continue
        due=obligation.get('due_clock')
        actor=obligation.get('responsible_actor')
        if type(due) is not int or due < 0:
            raise ValueError('CONTINUITY_INVALID_DUE_CLOCK')
        if obligation.get('kind')==HUMAN_OFFER_KIND:
            if clock<due<=end:
                candidates.append({'at':due,'kind':'HUMAN_OFFER_WINDOW_ELAPSES',
                    'actor':None,'source_ref':obligation['id'],
                    'not_actor_knowledge_or_moral_breach':True})
            continue
        if actor not in actors:
            # A record remains objectively pending even when its bearer is
            # unavailable; inventing a substitute would be false coactivity.
            continue
        if due<=end:
            candidates.append({'at':max(clock,due),'kind':'OBLIGATION_DUE',
                'actor':actor,'source_ref':obligation.get('id'),
                'not_proof_of_broken_promise':True})
    for cue in world.get('cues',[]):
        if not isinstance(cue,dict):continue
        expiry=cue.get('last_access_clock')
        if type(expiry) is int and clock<expiry+1<=end:
            candidates.append({'at':expiry+1,'kind':'PUBLIC_SIGN_EXPIRES',
                'actor':None,'source_ref':cue.get('id'),
                'expiration_not_actor_forgetting':True})
    structural=next_material_gate_discontinuity(world,actors,horizon)
    if structural:candidates.append(structural)
    candidates.sort(key=lambda d:(d['at'],
                        -1 if d['kind']=='CONDITIONAL_FAMILY_BIRTH' else
                        0 if d['kind']=='OBLIGATION_DUE' else
                        1 if d['kind']=='STRUCTURAL_GATE_TRANSITION' else 2,
                        str(d.get('source_ref'))))
    return candidates[0] if candidates else None


def continue_to_discontinuity(runtime, horizon=30, processes=None):
    """Actual period and actor step, rather than an invented diary montage.

    A due obligation gives its bearer an OCCASION, not a forced CARE action.
    The next actor attempt goes through native research actor policy and world.
    An overdue obligation with unrepresented microhistory is unresolved, not
    proof of immoral abandonment.
    """
    if type(horizon) is not int or not 1<=horizon<=MAX_HORIZON:
        raise ValueError('CONTINUITY_UNSUPPORTED_HORIZON')
    if processes is not None and (
            type(processes) is not list or len(processes)>512):
        raise ValueError('CONTINUITY_INVALID_PERIOD_PROCESS_LIST')
    world=runtime.ledger.world(runtime.world_id)[1]
    actors=runtime.ledger.actors()
    target=next_discontinuity(world,actors,horizon)
    if target is None:
        aggregate=runtime.background(horizon,processes=processes)
        return {'historical_discontinuity':None,
                'ordinary_interval_receipt':aggregate['receipt'],
                'high_resolution_actor_event':None,
                'unwritten_microevents_remain_unknown':True,
                'grade':GRADE}
    advance=target['at']-world['clock']
    ordinary=None
    if advance>0:
        ordinary=runtime.background(advance,processes=processes)
    if target['kind']=='CONDITIONAL_FAMILY_BIRTH':
        birth=runtime.realize_family_birth()
        return {'historical_discontinuity':target,
                'ordinary_interval_receipt':ordinary['receipt'] if ordinary else None,
                'high_resolution_actor_event':None,'family_birth_receipt':birth['receipt'],
                'new_actor':birth['actor'],'unwritten_microevents_remain_unknown':True,'grade':GRADE}
    if target['kind'] in ('HUMAN_OFFER_WINDOW_ELAPSES','MEETING_WINDOW_ELAPSES'):
        return {'historical_discontinuity':target,
                'ordinary_interval_receipt':ordinary['receipt'] if ordinary else None,
                'high_resolution_actor_event':None,
                'no_human_action_or_actor_appraisal_injected':True,
                'grade':GRADE}
    if target['kind']=='STRUCTURAL_GATE_TRANSITION':
        return {'historical_discontinuity':target,
                'ordinary_interval_receipt':ordinary['receipt'] if ordinary else None,
                'high_resolution_actor_event':None,
                'objective_change_not_actor_exposure_or_conduct':True,
                'unwritten_microevents_remain_unknown':True,'grade':GRADE}
    if target['kind']=='PUBLIC_SIGN_EXPIRES':
        return {'historical_discontinuity':target,
                'ordinary_interval_receipt':ordinary['receipt'] if ordinary else None,
                'high_resolution_actor_event':None,
                'expired_sign_not_deleted_from_history':True,
                'unwritten_microevents_remain_unknown':True,'grade':GRADE}
    # A real unsettled material obligation offers a situated initiative turn.
    # Actor may delay, refuse, fulfil, do something else or be physically
    # blocked. That independently enacted result is not the scheduler's act.
    actual=runtime.step(target['actor'])
    return {'historical_discontinuity':target,
            'ordinary_interval_receipt':ordinary['receipt'] if ordinary else None,
            'high_resolution_actor_event':actual['receipt'],
            'actor':actual['actor'],
            'attempted_operation':actual['attempt'],
            'scheduler_did_not_inject_action_or_consent':True,
            'fulfillment_not_inferred_from_elapsed_clock':True,
            'grade':GRADE}


def continue_pre_encounter(runtime, subject_id, target_age_days, *,
                           horizon_days=365, autonomous_beats=2,
                           max_segments=240, period_processes=None):
    """Construct historical time *before* the user encounters this person.

    This composes the EXISTING sourcefree owners: material interruptions,
    aggregate ordinary life, actor-selected activity, independent Others,
    and cold-persisted world/psyche. Neither the user nor this scheduler
    chooses the parents' or child's actions.

    Reaching a modeled age is not scientific adult-person construction, an
    adult social-role transfer, an invented diary, a first user meeting,
    or permission to disclose another actor's private history.
    """
    if type(subject_id) is not str or not subject_id:
        raise ValueError('PRE_ENCOUNTER_SUBJECT_REQUIRED')
    for value, low, high, code in (
        (target_age_days, 1, 120*365, 'PRE_ENCOUNTER_INVALID_TARGET_AGE'),
        (horizon_days, 1, MAX_HORIZON, 'PRE_ENCOUNTER_INVALID_HORIZON'),
        (autonomous_beats, 0, 24, 'PRE_ENCOUNTER_INVALID_BEAT_BUDGET'),
        (max_segments, 1, 240, 'PRE_ENCOUNTER_INVALID_SEGMENT_BUDGET'),
    ):
        if type(value) is not int or not low <= value <= high:
            raise ValueError(code)
    if period_processes is not None and (
            type(period_processes) is not list or len(period_processes)>512):
        raise ValueError('PRE_ENCOUNTER_INVALID_PERIOD_PROCESSES')
    actors = runtime.ledger.actors()
    if subject_id not in actors or actors[subject_id].get('id') != subject_id:
        raise ValueError('PRE_ENCOUNTER_UNREGISTERED_SUBJECT')
    initial = actors[subject_id].get('age_days')
    if type(initial) is not int or initial < 0:
        raise ValueError('PRE_ENCOUNTER_INVALID_SUBJECT_AGE')
    if target_age_days <= initial:
        raise ValueError('PRE_ENCOUNTER_TARGET_NOT_IN_FUTURE')
    # A finite budget is checked *before* making any persistent transition.
    # An unforeseen real discontinuity may still consume an additional segment;
    # then a complete partial-state receipt is returned without fake rollback.
    minimum = (target_age_days - initial + horizon_days - 1)//horizon_days
    if minimum > max_segments:
        raise ValueError('PRE_ENCOUNTER_SEGMENT_BUDGET_INSUFFICIENT')

    segments = []
    committed_beats = 0
    for _ in range(max_segments):
        present = runtime.ledger.actor(subject_id)[1]
        before = present['age_days']
        if before >= target_age_days:
            break
        span = min(horizon_days, target_age_days-before)
        # Material reproduction is forwarded to the existing R13 period
        # allocator, which validates exact source, location, scarce hours,
        # caregiver cost and historical interval BEFORE its own commit.
        kw = ({'processes':period_processes}
              if period_processes is not None else {})
        continuity = runtime.advance_to_discontinuity(horizon=span, **kw)
        later = runtime.ledger.actor(subject_id)[1]
        after = later.get('age_days')
        if type(after) is not int or after < before or after > before+span:
            # The existing continuity owner has already committed or refused
            # its own operation. Never silently pretend to have rolled it back.
            raise ValueError('PRE_ENCOUNTER_SOURCE_AGE_CONTRADICTION')
        entry = {
            'subject_age_before': before,
            'subject_age_after': after,
            'ordinary_interval_receipt':
                continuity.get('ordinary_interval_receipt'),
            'qualified_period_source_refs': (
                [p['source_ref'] for p in period_processes
                 if type(p) is dict and
                 type(p.get('source_ref')) is str]
                if continuity.get('ordinary_interval_receipt')
                and period_processes is not None else []),
            'material_discontinuity': continuity.get('historical_discontinuity'),
            'independently_resolved_event':
                continuity.get('high_resolution_actor_event'),
            'autonomous_event_receipts': [],
            'sourcefree_unwritten_microevents_remain_unknown': True,
        }
        if after == before:
            # A presently due unsettled obligation may give its owner an
            # actual decision turn without advancing the aggregate clock.
            # Do not rewrite its failure into a fictional missed childhood,
            # ignore a pending obligation, or loop forever on it.
            segments.append(entry)
            return _pre_encounter_receipt(
                runtime, subject_id, initial, target_age_days, segments,
                committed_beats, 'HELD_AT_UNRESOLVED_MATERIAL_DISCONTINUITY')
        if autonomous_beats:
            live = runtime.continue_without_user(beats=autonomous_beats)
            actual = live.get('events', [])
            if (live.get('no_player_action_injected') is not True or
                    live.get('beats_committed') != len(actual)):
                raise ValueError('PRE_ENCOUNTER_UNQUALIFIED_AUTONOMOUS_RETURN')
            entry['autonomous_event_receipts'] = [
                event['objective_receipt'] for event in actual]
            committed_beats += len(actual)
        segments.append(entry)

    final_age = runtime.ledger.actor(subject_id)[1]['age_days']
    status = ('HISTORICAL_AGE_CUT_REACHED'
              if final_age == target_age_days
              else 'HELD_AT_FINITE_SEGMENT_BUDGET')
    return _pre_encounter_receipt(
        runtime, subject_id, initial, target_age_days, segments,
        committed_beats, status)


def _pre_encounter_receipt(runtime, subject_id, initial, target, segments,
                           committed_beats, status):
    # Never return materialize(), situated(), the full private actor record,
    # model proposals, hidden parental relationships or a narrated scene.
    actor = runtime.ledger.actor(subject_id)[1]
    world = runtime.ledger.world(runtime.world_id)[1]
    return {
        'subject_ref': subject_id,
        'status': status,
        'initial_modeled_age_days': initial,
        'target_modeled_age_days': target,
        'last_modeled_age_days': actor['age_days'],
        'last_objective_world_clock': world['clock'],
        'aggregate_segments': len(segments),
        'autonomous_beats_committed': committed_beats,
        'historical_receipts': segments,
        'continuing_actor_role_not_reclassified': actor['role'],
        'user_visible_childhood_scenes': False,
        'no_user_action_or_other_person_consent_injected': True,
        'unwritten_events_unknown_not_simulated': True,
        'chronological_age_not_automatic_adult_psychology': True,
        'social_adult_status_not_issued': True,
        'public_first_encounter_not_issued': True,
        'private_actor_and_family_psychology_not_rendered': True,
        'sourcefree_underidentified_maturation': True,
        'partial_historical_commits_not_rolled_back': (
            status != 'HISTORICAL_AGE_CUT_REACHED'),
        'grade': GRADE,
    }



def qualify_contingent_world_notice(world, actors, proposal):
    """Qualify a *shared candidate occasion* in one independently continuing world.

    The same proposal may be offered to many copy-on-write continuities. The
    committed world of EACH continuity decides applicability; an inapplicable
    offer must not advance its clock, alter a person or manufacture an event.
    This admits only a sourcefree physical notice/sign, NOT an accident,
    injury, health outcome, treatment effect or actor response. Actual material
    consequences require the already competent world/event owners.
    """
    if type(proposal) is not dict or set(proposal) != {
            'offer_id', 'at_world_clock', 'location', 'kind', 'tags',
            'description', 'required_actor_locations'}:
        raise ValueError('CONTINGENT_NOTICE_INVALID_CONTRACT')
    offer_id=proposal['offer_id']
    clock=proposal['at_world_clock']
    location=proposal['location']
    kind=proposal['kind']
    tags=proposal['tags']
    desc=proposal['description']
    requires=proposal['required_actor_locations']
    if (type(offer_id) is not str or not offer_id.strip()
            or len(offer_id)>120
            or type(clock) is not int or clock < 0
            or type(location) is not str or not location
            or type(kind) is not str or not kind
            or type(desc) is not str or len(desc)>500
            or type(tags) is not list or len(tags)>24
            or any(type(t) is not str or not t for t in tags)
            or type(requires) is not dict or len(requires)>12):
        raise ValueError('CONTINGENT_NOTICE_INVALID_SOURCEFREE_PROPOSAL')
    if (type(world) is not dict or type(actors) is not dict
            or type(world.get('clock')) is not int
            or type(world.get('positions')) is not dict
            or type(world.get('sites')) is not dict):
        raise ValueError('CONTINGENT_NOTICE_INVALID_WORLD')
    for aid,site in requires.items():
        if (type(aid) is not str or aid not in actors
                or type(site) is not str or site not in world['sites']):
            raise ValueError('CONTINGENT_NOTICE_UNQUALIFIED_ACTOR_OR_SITE')
    if clock != world['clock']:
        return {'status':'INAPPLICABLE_WORLD_CLOCK',
                'offer_id':offer_id,'world_id':world.get('id')}
    if location not in world['sites']:
        return {'status':'INAPPLICABLE_SITE_NO_LONGER_EXISTS',
                'offer_id':offer_id,'world_id':world.get('id')}
    if any(world['positions'].get(aid)!=site for aid,site in requires.items()):
        return {'status':'INAPPLICABLE_ACTOR_LIFE_DIVERGED',
                'offer_id':offer_id,'world_id':world.get('id')}
    return {'status':'ELIGIBLE_SOURCEFREE_NOTICE_ONLY',
            'offer_id':offer_id,'world_id':world.get('id'),
            'no_world_outcome_or_actor_knowledge_inferred':True,
            'not_an_external_news_source_verification':True}


def qualify_mixed_history_schedule(world,processes):
    """Registered aggregate premises, not an unconditional life script."""
    from .routine_sources import verify_qualified_period_envelope
    from .historical_social_reproduction import _typecheck
    if type(processes) is not list or len(processes)>512:
        raise ValueError('MIXED_HISTORY_INVALID_ROUTINE_SCHEDULE')
    result=[];seen=set()
    for process in processes:
        _typecheck(process)
        if process['source_ref'] in seen:
            raise ValueError('MIXED_HISTORY_DUPLICATE_ROUTINE_SOURCE')
        seen.add(process['source_ref'])
        source=world.get('routine_source_registry',{}).get(process['source_ref'])
        if type(source) is not dict:
            raise ValueError('HISTORICAL_PROCESS_UNREGISTERED_SOURCE_ENVELOPE')
        start=source['from_clock'];end=source['through_clock']
        verify_qualified_period_envelope(world,process,start,1)
        row=copy(process)
        row['routine_window_application']='SITUATED_CONDITIONAL_ROUTINE'
        result.append((start,end,row))
    return result


def mixed_history_interval(schedule,clock,limit):
    """Cut at the first source boundary; expired/future premises are inactive."""
    active=[]
    for start,end,row in schedule:
        if clock<start:limit=min(limit,start)
        elif clock<end:
            limit=min(limit,end);active.append(copy(row))
    return limit,active


def qualified_recurrent_interval(world,schedule,clock,limit):
    """One shared owner read for both mixed history and checkpoint generation.

    A newly admitted ordinary-life source is operative without the analyst
    repeating it in a period catalog. Its exact original basis still enters
    the existing allocator, which resolves the current revision and pairing.
    """
    from .routine_sources import acquired_routine_processes,lived_work_permission_boundaries
    live=acquired_routine_processes(world)
    explicit_refs={row['source_ref'] for _,_,row in schedule}
    dynamic=qualify_mixed_history_schedule(world,[p for p in live
                if p['source_ref'] not in explicit_refs])
    end,active=mixed_history_interval(schedule+dynamic,clock,limit)
    for p in active:
        if p['kind']=='QUALIFIED_WAGE_LABOR':
            times=lived_work_permission_boundaries(world,p['actor'],p['location'],clock,end)
            if times:end=min(end,times[0])
    if end<=clock:raise ValueError('MIXED_HISTORY_EMPTY_ROUTINE_INTERVAL')
    return end,active


def continue_mixed_history(runtime,target_clock,*,cadence_origin=0,
                           ordinary_span=30,detail_beats=3,max_segments=240,
                           period_processes=None):
    """One continuing life before and between actual visitor encounters.

    Alternate aggregate reproduction and genuinely selected detailed activity.
    The existing continuity owner handles discontinuities and conditional birth;
    the existing initiative owner selects who, never what. Absolute modeled
    phase and actual ledger counts, not a new scheduler cursor, permit cold
    continuation without replaying a person. The cadence is a research
    resolution choice, not a biological period, human calendar or adult end.
    """
    from .initiative import choose_next_actor
    for value,low,high,code in (
        (target_clock,0,10**9,'TARGET'),(cadence_origin,0,10**9,'ORIGIN'),
        (ordinary_span,1,MAX_HORIZON,'SPAN'),(detail_beats,1,24,'DETAIL'),
        (max_segments,1,240,'SEGMENTS')):
        if type(value) is not int or not low<=value<=high:
            raise ValueError('MIXED_HISTORY_INVALID_'+code)
    world=runtime.ledger.world(runtime.world_id)[1];initial=world['clock']
    if cadence_origin>initial or target_clock<initial:
        raise ValueError('MIXED_HISTORY_NONPROSPECTIVE_CLOCK')
    if any(x.get('present') is True for x in world.get('neighbor_users',{}).values()):
        raise ValueError('MIXED_HISTORY_PRESENT_VISITOR_REQUIRES_PRESENT_OWNER')
    schedule=qualify_mixed_history_schedule(world,period_processes if period_processes is not None else [])
    visitor_history=copy(world.get('neighbor_user_events',[]))
    entries=[];reason=None;cycle=ordinary_span+detail_beats
    def read():
        w=runtime.ledger.world(runtime.world_id)[1]
        if (any(x.get('present') is True for x in w.get('neighbor_users',{}).values())
                or w.get('neighbor_user_events',[])!=visitor_history):
            raise ValueError('MIXED_HISTORY_VISITOR_BOUNDARY_CHANGED')
        return w
    while len(entries)<max_segments:
        world=read();clock=world['clock']
        family=world.get('family_genesis',{})
        if family.get('stage')=='CONCEPTION_ADMITTED':
            birth=family['selected_pathway']['birth_clock']
            if birth<clock:
                reason='MISSED_CONDITIONAL_BIRTH_BOUNDARY';break
            if birth==clock:
                result=runtime.advance_to_discontinuity(horizon=1,processes=[])
                if not result.get('family_birth_receipt') or read()['clock']!=clock:
                    raise ValueError('MIXED_HISTORY_BIRTH_OWNER_RETURN')
                entries.append({'kind':'CONDITIONAL_BIRTH','from_clock':clock,
                    'through_clock':clock,'receipt':result['family_birth_receipt']})
                continue
        if clock>=target_clock:break
        actors=runtime.ledger.actors()
        position=(clock-cadence_origin)%cycle
        detail_start=clock-position+ordinary_span
        boundary=next_discontinuity(world,actors,1)
        if boundary and boundary['kind']=='OBLIGATION_DUE' and boundary['at']==clock:
            result=runtime.advance_to_discontinuity(horizon=1,processes=[])
            after=read()['clock']
            row={'kind':'DUE_ACTOR_OCCASION','source_ref':boundary['source_ref'],
                'receipt':result.get('high_resolution_actor_event'),'from_clock':clock,
                'through_clock':after}
            if not row['receipt']:raise ValueError('MIXED_HISTORY_DUE_OWNER_NO_RECEIPT')
            entries.append(row)
            if after!=clock+1:raise ValueError('MIXED_HISTORY_DETAIL_CLOCK_CONTRADICTION')
            # Stop at an unresolved due act rather than making an actor repeat
            # the same occasion forever. Prior real progress remains committed.
            if any(x.get('id')==row['source_ref'] and x.get('status')=='PENDING'
                   for x in read().get('scheduled_obligations',[])):
                reason='DUE_OBLIGATION_STILL_UNRESOLVED';break
        elif position>=ordinary_span:
            counts=runtime.ledger.actor_life_counts_after(runtime.world_id,detail_start,clock)
            choice=choose_next_actor(world,actors,counts)
            if choice is None:reason='NO_SITUATED_ACTOR';break
            result=runtime.step(choice['actor'])
            if (result.get('selection_grade')=='INJECTED_NOT_NATIVE_ACTOR_CHOICE'
                    or not result.get('receipt')):
                raise ValueError('MIXED_HISTORY_NONINDEPENDENT_ACTOR_RETURN')
            after=read()['clock']
            entries.append({'kind':'INDEPENDENT_DETAIL','receipt':result['receipt'],
                'from_clock':clock,'through_clock':after})
            if after!=clock+1:raise ValueError('MIXED_HISTORY_DETAIL_CLOCK_CONTRADICTION')
        else:
            end=min(target_clock,detail_start,clock+MAX_HORIZON)
            end,active=qualified_recurrent_interval(world,schedule,clock,end)
            boundary=next_discontinuity(world,actors,end-clock)
            # Stop exactly at the interruption, not one actor beat beyond it.
            # The next loop dispatches an actually due act/birth. No retroactive
            # care, assumed consent or fabricated microscenes.
            if boundary:end=boundary['at']
            if end<=clock:raise ValueError('MIXED_HISTORY_ZERO_PROGRESS_BOUNDARY')
            result=runtime.background(end-clock,processes=active)
            after=read()['clock']
            entries.append({'kind':'QUALIFIED_ORDINARY_INTERVAL','receipt':result['receipt'],
                'from_clock':clock,'through_clock':after,
                'source_refs':[p['source_ref'] for p in active],
                'discontinuity':boundary['kind'] if boundary else None})
            if after!=end:raise ValueError('MIXED_HISTORY_AGGREGATE_CLOCK_CONTRADICTION')
        if after<=clock or after>target_clock:
            raise ValueError('MIXED_HISTORY_OWNER_ADVANCED_OUTSIDE_BOUNDARY')
    final=read();clock=final['clock'];family=final.get('family_genesis',{})
    unresolved_birth=(family.get('stage')=='CONCEPTION_ADMITTED'
                      and family['selected_pathway']['birth_clock']<=clock)
    reached=(clock==target_clock and not unresolved_birth and reason is None)
    return {'status':'MODELED_HISTORY_CUT_REACHED' if reached else 'HELD_AT_MIXED_HISTORY_BOUNDARY',
        'hold_reason':None if reached else reason or 'FINITE_SEGMENT_BUDGET',
        'initial_modeled_clock':initial,'target_modeled_clock':target_clock,
        'actual_modeled_clock':clock,'segments':entries,
        'ordinary_intervals':sum(e['kind']=='QUALIFIED_ORDINARY_INTERVAL' for e in entries),
        'independent_actor_beats':sum(e['kind'] in ('INDEPENDENT_DETAIL','DUE_ACTOR_OCCASION') for e in entries),
        'conditional_births':sum(e['kind']=='CONDITIONAL_BIRTH' for e in entries),
        'no_visitor_action_or_reconstructed_microevent':True,
        'not_real_time_or_developmental_science':True,'grade':GRADE}
