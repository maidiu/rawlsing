"""SORACLE R12 — practical inquiry arises from frustrated activity, not omniscience.

An actor who previously attempted something under a real obstruction may
notice that an institution publishes a relevant public notice.  Their history
can make INSPECT a possible next action.  The world decides what is actually
posted; inspecting never grants privileged access to a confidential rule,
the original reason for refusal, or a counterfactual success.  Once a notice
was personally encountered, that actor can recognize having inspected it,
without assigning belief, agreement, or complete comprehension.
"""
from .types import GRADE, stable_id, copy
from .organism import eligible


def notices_present(world, location, clock):
    out=[]
    for notice in world.get('public_notices',[]):
        if not isinstance(notice,dict) or not notice.get('public'):
            continue
        if notice.get('location') != location:
            continue
        if type(notice.get('id')) is not str or not notice['id']:
            continue
        start=notice.get('effective_from',0)
        finish=notice.get('effective_until')
        if type(start) is not int or (finish is not None
                                     and type(finish) is not int):
            continue
        if start<=clock and (finish is None or clock<=finish):
            out.append(notice)
    return sorted(out,key=lambda n:n['id'])


def offer_actor_inquiry(constitution,access):
    """Qualified historical encounter changes available investigative means.

    An apparent institutional obstacle can prompt evidence seeking even when
    the actor cannot identify that institution as the actual cause.
    """
    if constitution.actor!=access.actor:
        raise ValueError('INQUIRY_FOREIGN_ACTOR')
    visible={str(x.get('public_notice_ref'))
             for x in access.cues if isinstance(x,dict)
             and x.get('kind')=='public_notice_visible'
             and type(x.get('public_notice_ref')) is str}
    if not visible:
        return {'offered':[],'readset':[],'grade':GRADE}
    already={x.get('public_notice_ref') for x in
             getattr(constitution,'notice_exposures',[])}
    uninspected=sorted(visible-already)
    if not uninspected:
        return {'offered':[],'readset':[],'grade':GRADE}
    prior=[r for r in getattr(constitution,'power_exercises',[])
           if isinstance(r,dict) and r.get('attempt_status_analyst_receipt') in
           ('BLOCKED','PARTIAL') and
           r.get('encounter_location')==access.location]
    learned=[r for r in getattr(constitution,
              'institutional_expectations',[])
             if isinstance(r,dict) and
             r.get('status')=='PROVISIONAL' and
             r.get('operative_possible_means')=='INSPECT' and
             r.get('scope')=='POSTED_INSTITUTIONAL_PROCEDURE'
             and type(r.get('observed_at_clock')) is int
             and r['observed_at_clock']<=constitution.clock]
    if not prior and not learned:
        return {'offered':[],'readset':[],'grade':GRADE}
    allowed,_=eligible(constitution.body,'INSPECT')
    if not allowed:
        return {'offered':[],'readset':[],'grade':GRADE}
    # The old difficulty and the public sign may be unrelated. The actor
    # is allowed to investigate, not preapproved to learn a causal verdict.
    route=('HISTORICALLY_FRUSTRATED_EVIDENCE_SEEKING' if prior
           else 'HISTORICALLY_LEARNED_INSTITUTIONAL_INQUIRY')
    basis=(['HISTORICALLY_FRUSTRATED_ATTEMPT']+
           [x['experience_ref'] for x in prior[-8:]]
           if prior else
           ['HISTORICALLY_EXERCISED_COLLECTIVE_PROCEDURE']+
           [x['own_received_experience_ref'] for x in learned[-8:]])
    return {'offered':[{
        'action':'INSPECT','score':.17,
        'basis':basis,
        'source_grounds_status':route,
        'candidate_notice_refs':uninspected[:8],
        'opportunity':'ACTOR_HISTORICAL_EVIDENCE_SEEKING',
        'no_conscious_curiosity_motive_inferred':True,
        'relevant_notice_relation':'UNRESOLVED_MAY_BE_UNRELATED',
        'public_only_not_privileged_world_CAUSE':True,'grade':GRADE}],
        'readset':([x['event_ref'] for x in prior[-8:]]+
                   [x['origin_public_event_ref'] for x in learned[-8:]]),
        'candidate_notices':uninspected[:8],
        'grade':GRADE}


def retain_personal_notice_exposure(actor,experience,event_ref):
    if actor.get('id')!=experience.get('actor'):
        raise ValueError('INQUIRY_NOTICE_ACTOR_MISMATCH')
    received=[x for x in experience.get('perceived_cues',[])
              if isinstance(x,dict) and
              x.get('kind')=='performed_inspect' and
              type(x.get('public_notice_ref')) is str]
    if not received:
        return []
    records=[]
    for cue in received:
        ref=cue['public_notice_ref']
        key=stable_id('encountered_public_notice',{
            'actor':actor['id'],'event':event_ref,'notice':ref,
            'received_cue':cue.get('id')})
        if any(x.get('id')==key for x in actor.get('notice_exposures',[])):
            continue
        row={
            'id':key,'public_notice_ref':ref,
            'inspected_at_clock':experience.get('clock'),
            'event_ref':event_ref,'experience_ref':experience.get('ref'),
            'received_cue_ref':cue.get('id'),
            'public_words_available':copy(cue.get('tags',[])),
            'actor_comprehension':'NOT_ESTABLISHED',
            'actor_accepted_interpretation':'NOT_ESTABLISHED',
            'actual_hidden_rule_caused_prior_block':'NOT_ESTABLISHED',
            'grade':GRADE,
        }
        actor.setdefault('notice_exposures',[]).append(row)
        records.append({'kind':'RETAIN_PERSONAL_PUBLIC_NOTICE_EXPOSURE',
                        'ref':key,'grade':GRADE})
    return records


def choose_grounded_public_inquiry(options):
    """Sourcefree fallback when only one historically grounded notice is live.

    An institution is not compelled to tell the truth simply because an
    individual inspected its public document. The actor need not consciously
    call this behavior an investigation or a political challenge.
    """
    choices=[a for option in options if option.get('action')=='INSPECT'
             and not option.get('project_courses')
             for a in option.get('practical_alternatives',[])
             if a.get('grounds_status') in (
             'HISTORICALLY_FRUSTRATED_EVIDENCE_SEEKING',
             'HISTORICALLY_LEARNED_INSTITUTIONAL_INQUIRY')]
    distinct={a['option_id']:a for a in choices}
    if len(distinct)!=1:
        return None
    choice=next(iter(distinct.values()))
    return {
        'action':'INSPECT',
        'practical_option_id':choice['option_id'],
        'project_id':None,
        'semantic_grade':'SOURCEFREE_ACTOR_GROUNDED_EVIDENCE_SEEKING',
        'selection_is_not_conscious_explanation':True,
        'public_notice_ref_analyst_only':choice['world_request']['material_object_ref'],
    }
