"""SORACLE R15 — plural situated care paths, not a universal attachment scalar.

R14's singleton fallback left a child with two real caregivers unable to
construct either history. And an abstract period could override recent,
personally lived contradictory encounters. This module recovers real source
events and provides distinct, revisable actor-owned practical opportunities.

No caregiver is 'good', 'bad', 'trusted', loved or causally understood by
definition; a clock/relief witness is an analyst-qualified condition for a
semantic proposal, not an infallible mental state or law of attachment.
"""
from math import isfinite
from .types import GRADE, stable_id, copy


def _delta(before,after,name):
    if type(before) not in (float,int) or type(after) not in (float,int):
        raise ValueError('PLURAL_CARE_UNQUALIFIED_BODY_'+name)
    if not all(isfinite(float(x)) and 0<=x<=1 for x in (before,after)):
        raise ValueError('PLURAL_CARE_INVALID_BODY_'+name)
    return round(float(after)-float(before),5)


def conserve_lived_high_resolution_care(actor,experience,event_ref,before,after):
    """One ACTUAL personally sensed care event, no narrated daily history.

    The high-resolution world performed CARE on this actor, the actor
    received the provider's public sensory sign, and their own body changed.
    Preserve all three, without forcing an affective or reflective meaning.
    """
    if actor.get('id')!=experience.get('actor') or not event_ref:
        raise ValueError('PLURAL_CARE_EXPERIENCE_ACTOR_MISMATCH')
    if type(experience.get('clock')) is not int or experience['clock']<0:
        raise ValueError('PLURAL_CARE_INVALID_EXPERIENCE_CLOCK')
    if (experience.get('own_action')!='RECEIVED_CARE'
            or experience.get('felt_effect')!='SOMATIC_CARE_CANDIDATE'
            or not experience.get('participated')):
        return None
    cues=[c for c in experience.get('perceived_cues',[])
          if type(c) is dict and c.get('kind')=='performed_care'
          and type(c.get('source_actor')) is str
          and c.get('source_actor')!=actor['id']
          and type(c.get('id')) is str]
    if len(cues)!=1:
        return None
    giver=cues[0]['source_actor']
    gain=_delta(before['comfort'],after['comfort'],'COMFORT')
    nutrition=_delta(before['nutrition'],after['nutrition'],'NUTRITION')
    if gain<=0 and nutrition<=0:
        return None
    ident=stable_id('personally_experienced_care',{
        'actor':actor['id'],'event':event_ref,'care_cue':cues[0]['id']})
    entries=actor.setdefault('experienced_care_events',[])
    if any(e.get('id')==ident for e in entries):
        raise ValueError('PLURAL_CARE_DUPLICATED_LIVED_EVENT')
    row={
        'id':ident,'actor':actor['id'],'giver_ref':giver,
        'event_ref':event_ref,'experience_ref':experience['ref'],
        'received_cue_ref':cues[0]['id'],
        'location':experience.get('location'),
        'clock':experience.get('clock'),
        'actual_felt_body_change_model':{
            'comfort':gain,'nutrition':nutrition},
        'lived_bodily_regulation':'SOURCEFREE_EVENT_QUALIFIED',
        'cause_or_love_known_to_actor':'NOT_ESTABLISHED',
        'caregiver_past_or_future_consistency':'NOT_ESTABLISHED',
        'other_person_private_meaning':'INACCESSIBLE',
        'not_aggregate_daily_episode':'ACTUAL_WORLD_TRANSACTION',
        'grade':GRADE}
    entries.append(row)
    return row


def plural_acquisition_candidate(actor,experience,event_ref):
    """Bilateral lived histories can seed distinct orientations at later times.

    Explicitly prevents treating simultaneous presence of two formerly
    helpful people as 'no history'. The fallback picks only a *uniquely*
    grounded person whose latest high-resolution event is most recent.
    If candidates tie, only a semantic proposal can choose; no actor-wide
    one-parent preference or default mother/father hierarchy is installed.
    """
    if actor['id']!=experience.get('actor'):
        raise ValueError('PLURAL_CARE_FOREIGN_ACTOR')
    if type(experience.get('clock')) is not int or experience['clock']<0:
        raise ValueError('PLURAL_CARE_INVALID_EXPERIENCE_CLOCK')
    present={c.get('source_actor'):c.get('id')
             for c in experience.get('perceived_cues',[])
             if type(c) is dict and c.get('kind')=='coactor_present'
             and type(c.get('source_actor')) is str}
    prior={o.get('caregiver_ref') for o in
           actor.get('co_regulation_orientations',[])
           if o.get('status')=='ACTIVE'}
    rows=[]
    for caregiver,cue in sorted(present.items()):
        if caregiver in prior:continue
        highres=[h for h in actor.get('experienced_care_events',[])
                 if h.get('giver_ref')==caregiver
                 and type(h.get('clock')) is int
                 and h['clock']<experience.get('clock',-1)]
        aggregate=[h for h in actor.get('undergone_care_periods',[])
                   if h.get('caregiver_ref')==caregiver
                   and h.get('through_clock',float('inf'))<=
                       experience.get('clock',-1)]
        if not highres and not aggregate:continue
        rows.append({
            'caregiver_ref':caregiver,'perceived_cue_ref':cue,
            'high_resolution_care_refs':[h['id'] for h in highres[-16:]],
            'aggregate_care_refs':[h['id'] for h in aggregate[-16:]],
            'last_personally_lived_care_clock':max(
                (h['clock'] for h in highres),default=None),
            'has_actual_particular_lived_care':bool(highres),
            'aggregate_not_equal_to_personally_witnessed_daily_events':True,
            'not_a_conscious_relative_caregiver_ranking':True,
            'grade':GRADE})
    return rows


def choose_one_grounded_plural_acquisition(rows):
    """Heuristic makes one warranted proposal; semantic constructor may abstain.

    An actual remembered-by-model bodily event outranks a hypothetical
    aggregate for *source resolution only*, never as a universal preference.
    Ties remain open and never choose by gender, name or array order.
    """
    if not rows:return []
    if len(rows)==1:
        winner=rows[0]
    else:
        witnessed=[x for x in rows
                   if x.get('last_personally_lived_care_clock') is not None]
        if not witnessed:return []
        most_recent=max(x['last_personally_lived_care_clock']
                        for x in witnessed)
        best=[x for x in witnessed
              if x['last_personally_lived_care_clock']==most_recent]
        if len(best)!=1:return []
        winner=best[0]
    return [{
        'kind':'ACQUIRE_CO_REGULATION_ORIENTATION',
        'caregiver_ref':winner['caregiver_ref'],
        'perceived_cue_ref':winner['perceived_cue_ref'],
        'period_refs':copy(winner['aggregate_care_refs']),
        'lived_care_event_refs':copy(winner['high_resolution_care_refs']),
        'sourcefree_plurally_conditioned_not_a_person_preference_law':True,
    }]


def plural_addressed_signal_choice(options,body):
    """Only ACTOR-QUALIFIED personal response histories can break rivalry.

    Two merely co-present caregivers with equally unresolved trajectories do
    not become a forced winner. When distinct actor-lived support evidence
    exists, a unique latest personally sensed relief can select one address
    as a *fallible provisional next act*. Independent Others still decide.
    """
    if type(body) is not dict or not (
            body.get('comfort',1)<.43 or body.get('nutrition',1)<.55
            or body.get('rest',1)<.40):
        return None
    if any(o.get('project_courses') for o in options):
        return None
    alts=[]
    for option in options:
        if option.get('action')!='SIGNAL':continue
        if option.get('psychodynamic_status')=='UNRESOLVED_CONTRADICTION':
            continue
        if option.get('preproject_recruitment',{}).get('status') in (
                'ACQUIRED_NONPROJECT_WITHHOLD',
                'UNRESOLVED_PREPROJECT_CONTRADICTION'):
            continue
        for alt in option.get('practical_alternatives',[]):
            if alt.get('grounds_status')!='HISTORICALLY_ACQUIRED_CO_REGULATION':
                continue
            alts.append(alt)
    if not alts:return None
    if len(alts)==1:
        chosen=alts[0]
        contrast='ONE_CURRENTLY_QUALIFIED_RELATION'
    else:
        witnessed=[]
        for alt in alts:
            supports=alt.get('personally_sensed_support_history',[])
            if type(supports) is not list:continue
            valid=[x for x in supports if type(x) is dict
                   and type(x.get('event_clock')) is int
                   and type(x.get('response_ref')) is str
                   and x.get('bodily_regulation_sensed') is True]
            if valid:
                most_recent=max(valid,key=lambda x:x['event_clock'])
                witnessed.append((most_recent['event_clock'],alt))
        if not witnessed:return None
        clock=max(x[0] for x in witnessed)
        best=[alt for when,alt in witnessed if when==clock]
        if len(best)!=1:return None
        chosen=best[0]
        contrast='DISTINCT_ACTOR_LIVED_RECENT_RESPONSE_NOT_GLOBAL_GOOD_PARENT'
    return {
        'action':'SIGNAL','practical_option_id':chosen['option_id'],
        'project_id':None,
        'selection_grade':'SOURCEFREE_PLURAL_RELATIONAL_ATTEMPT',
        'sourcefree_historical_contrast':contrast,
        'other_response_is_independently_settled':True,
        'actor_moral_judgment_or_conscious_reason':'NOT_INFERRED'}


def sourcequalified_reopening(actor,experience,event_ref):
    """Reconsider a suspended relation after NEW actually experienced care.

    It is not enough that the caregiver is present again, forgiven, or
    described as kind. An independent CARE action must actually affect this
    actor's own body and leave a received source-linked perceptual sign.
    """
    if actor['id']!=experience.get('actor'):
        raise ValueError('PLURAL_CARE_REOPEN_FOREIGN_ACTOR')
    recent=[x for x in actor.get('experienced_care_events',[])
            if x.get('event_ref')==event_ref]
    out=[]
    for lived in recent:
        caregiver=lived['giver_ref']
        for prior in actor.get('co_regulation_orientations',[]):
            if prior.get('caregiver_ref')!=caregiver or (
                    prior.get('interpretation_phase')
                    !='UNRESOLVED_AFTER_NONRESPONSE'):
                continue
            out.append({
                'kind':'POSSIBLE_REOPEN_AFTER_MATERIAL_CARE',
                'orientation_ref':prior['id'],
                'source_personally_lived_care_ref':lived['id'],
                'caregiver_ref':caregiver,
                'received_source_cue_ref':lived['received_cue_ref'],
                'would_not_erase_previous_nonresponses':True,
                'not_an_automatic_renewed_trust':True,
                'grade':GRADE})
    return out


def propose_one_reopening(rows):
    if len(rows)!=1:return []
    x=rows[0]
    return [{'kind':'REOPEN_CO_REGULATION_ORIENTATION',
        'orientation_ref':x['orientation_ref'],
        'care_event_ref':x['source_personally_lived_care_ref'],
        'perceived_cue_ref':x['received_source_cue_ref'],
        'reopened_without_forgetting':True}]


def admit_reopening(actor,experience,event_ref,proposal):
    if actor['id']!=experience.get('actor'):
        raise ValueError('PLURAL_CARE_REOPEN_FOREIGN_ACTOR')
    orientation=next((x for x in actor.get('co_regulation_orientations',[])
        if x.get('id')==proposal.get('orientation_ref')),None)
    if orientation is None or orientation.get('interpretation_phase')!=(
            'UNRESOLVED_AFTER_NONRESPONSE'):
        raise ValueError('PLURAL_CARE_REOPEN_NOT_SUSPENDED')
    lived=[x for x in actor.get('experienced_care_events',[])
           if x.get('id')==proposal.get('care_event_ref')
           and x.get('event_ref')==event_ref
           and x.get('giver_ref')==orientation.get('caregiver_ref')
           and x.get('received_cue_ref')==proposal.get('perceived_cue_ref')]
    if len(lived)!=1 or not any(
            c.get('id')==proposal.get('perceived_cue_ref') and
            c.get('kind')=='performed_care' and
            c.get('source_actor')==orientation['caregiver_ref']
            for c in experience.get('perceived_cues',[])
            if type(c) is dict):
        raise ValueError('PLURAL_CARE_REOPEN_NO_NEW_RECEIVED_CARE')
    if not any(v>0 for v in lived[0][
            'actual_felt_body_change_model'].values()):
        raise ValueError('PLURAL_CARE_REOPEN_NO_LIVED_BODY_DIFFERENCE')
    old=orientation['interpretation_phase']
    new='OPEN_AFTER_LIVED_CARE_NOT_SETTLED_TRUST'
    orientation.setdefault('interpretation_history',[]).append({
        'before':old,'after':new,'event_ref':event_ref,
        'personally_lived_care_ref':lived[0]['id'],
        'old_nonresponses_not_erased':True,
        'no_claim_to_caregiver_future_constancy':True,
        'grade':GRADE})
    orientation['interpretation_phase']=new
    return {'kind':'REOPEN_CO_REGULATION_ORIENTATION',
            'orientation_ref':orientation['id'],
            'phase':new,'grade':GRADE}
