"""SORACLE R11 / Astra 6,7,17,19: ordinary life has discontinuities.

Routine coverage is cheap; a source-qualified deadline, expiring signal or
material interruption gets a detailed *actor-owned* opportunity. No player
chooses the action. This does not invent unperformed micro-events, pretend a
scheduling threshold was an experienced violation, or close other actors'
rights. The actual runtime/world owners still author their own transactions.
"""
from .types import GRADE, stable_id
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
        if not isinstance(obligation,dict) or obligation.get('status')!='PENDING':
            continue
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
    if target['kind']=='HUMAN_OFFER_WINDOW_ELAPSES':
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
