"""SORACLE P006/P015 — caregiver-side acquired practical investment in care.

An adult's repeated, personally experienced, independently selected CARE
or FEED activity directed at the SAME particular Other may form an operative
conditional care practice. Actual material/bodily cost, distinct encounters
and source actor choice are required. The recipient's affection, approval,
future consent or adult caregiver's 'love' is not inferred.

This complements the child's receiving/co-regulation histories rather than
replacing them or using a scalar relationship score.
"""
from .types import stable_id,copy,GRADE
from .organism import eligible

ACTS=frozenset(("CARE","FEED"))
CHOSEN="ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE"


def conserve_costly_offered_care(actor,experience,event_ref,attempt,
                                world_event,before,after):
    if (type(actor) is not dict or type(experience) is not dict or
            experience.get("actor")!=actor.get("id")
            or type(event_ref) is not str or not event_ref):
        raise ValueError("CARE_COMMITMENT_FOREIGN_SOURCE")
    if (not attempt or getattr(attempt,"actor",None)!=actor["id"]
            or getattr(attempt,"action",None) not in ACTS
            or getattr(attempt,"intention",None)!=CHOSEN):
        return None
    if (experience.get("own_action")!=attempt.action or
            (experience.get("felt_enactment") or {}).get(
                "attempted_operation")!=attempt.action or
            experience.get("status")!="PERFORMED"
            or world_event.get("status")!="PERFORMED"):
        return None
    target=getattr(attempt,"target",None)
    if type(target) is not str or not target or target==actor["id"]:
        return None
    direct=(world_event.get("actor")==actor["id"]
            and world_event.get("action")==attempt.action
            and world_event.get("target")==target
            and world_event.get("outcome") in (
                "CARE_GIVEN","MATERIAL_FEEDING_SUCCEEDED",
                "FEEDING_ACTUALLY_PROVIDED"))
    as_other=(world_event.get("coactor")==actor["id"]
            and world_event.get("coactor_action")==attempt.action
            and world_event.get("actor")==target
            and world_event.get("action")=="SIGNAL"
            and world_event.get("outcome")=="JOINT_ACTIVITY_PERFORMED")
    if not (direct or as_other):
        return None
    if not any(x.get("kind")=="coactor_present"
               and x.get("source_actor")==target
               for x in experience.get("perceived_cues",[])
               if type(x) is dict):
        return None
    spent=(before.get("rest",0)-after.get("rest",0))
    if type(spent) not in (int,float) or spent<=0:
        return None
    if type(experience.get("clock")) is not int:
        raise ValueError("CARE_COMMITMENT_UNCLOCKED_SOURCE")
    ref=stable_id("costly_personally_offered_care",{
        "actor":actor["id"],"target":target,
        "event":event_ref,"operation":attempt.action})
    rows=actor.setdefault("care_contribution_episodes",[])
    if any(x.get("id")==ref for x in rows):
        raise ValueError("CARE_COMMITMENT_DUPLICATE_EPISODE")
    row={
        "id":ref,"actor":actor["id"],
        "recipient_ref":target,
        "operation":attempt.action,
        "event_ref":event_ref,
        "experience_ref":experience["ref"],
        "clock":experience["clock"],"location":experience.get("location"),
        "bodily_cost_rest_delta":round(spent,5),
        "selection_source":attempt.intention,
        "actually_received_attempt_sign":True,
        "world_performed_success_analyst_only":True,
        "subjective_felt_affection":"NOT_INFERRED",
        "recipient_willingness_or_love":"NOT_INFERRED",
        "not_conscious_motive_or_religious_virtue":True,
        "grade":GRADE}
    rows.append(row)
    return row


def candidate_care_commitment(actor,experience,event_ref):
    if experience.get("actor")!=actor.get("id"):return []
    rows=actor.get("care_contribution_episodes",[])
    current=[x for x in rows if x.get("event_ref")==event_ref
             and x.get("experience_ref")==experience.get("ref")]
    if len(current)!=1:return []
    now=current[0]
    history=[x for x in rows
             if x.get("recipient_ref")==now["recipient_ref"]
             and type(x.get("clock")) is int
             and x["clock"]<now["clock"]
             and x.get("selection_source")==CHOSEN
             and x.get("bodily_cost_rest_delta",0)>0
             and x.get("event_ref")!=event_ref]
    if not history:return []
    prior=max(history,key=lambda x:(x["clock"],x["id"]))
    ident=stable_id("practiced_particular_care",{
        "actor":actor["id"],"prior":prior["id"],
        "later":now["id"],"recipient":now["recipient_ref"]})
    if any(x.get("id")==ident for x in actor.get(
            "care_practical_commitments",[])):
        return []
    return [{
        "kind":"ACQUIRE_COSTLY_CARE_PRACTICE",
        "practice_ref":ident,
        "earlier_offered_care_ref":prior["id"],
        "later_offered_care_ref":now["id"],
        "recipient_ref":now["recipient_ref"],
        "locally_practiced_operation":now["operation"],
        "sustained_activity_not_love":True,
        "grade":GRADE}]


def admit_care_commitment(actor,experience,event_ref,proposal):
    candidates=candidate_care_commitment(actor,experience,event_ref)
    if len(candidates)!=1:
        raise ValueError("CARE_COMMITMENT_NO_TWO_DISTINCT_ACTOR_SELECTED_ACTS")
    expected=candidates[0]
    for key in ("practice_ref","earlier_offered_care_ref",
                "later_offered_care_ref","recipient_ref",
                "locally_practiced_operation"):
        if proposal.get(key)!=expected[key]:
            raise ValueError("CARE_COMMITMENT_FORGED_"+key)
    old=next(x for x in actor["care_contribution_episodes"]
             if x["id"]==expected["earlier_offered_care_ref"])
    new=next(x for x in actor["care_contribution_episodes"]
             if x["id"]==expected["later_offered_care_ref"])
    rec={
        "id":expected["practice_ref"],"actor":actor["id"],
        "recipient_ref":expected["recipient_ref"],
        "operation":expected["locally_practiced_operation"],
        "source_contribution_refs":[old["id"],new["id"]],
        "source_event_refs":[old["event_ref"],new["event_ref"]],
        "source_clock_interval":[old["clock"],new["clock"]],
        "status":"HISTORICALLY_PRACTICED_CONTINGENT_CARE",
        "costs_actually_incurred_not_perpetually_paid":True,
        "no_automatic_love_or_assent":True,
        "other_independently_becoming":True,
        "grade":GRADE}
    actor.setdefault("care_practical_commitments",[]).append(rec)
    return {"kind":proposal["kind"],"practice_ref":rec["id"],
            "status":"ADMITTED_PRACTICED_CARE_NOT_UNCONDITIONAL_LOVE",
            "grade":GRADE}


def practiced_care_alternatives(constitution,access,option):
    if constitution.actor!=access.actor or option.get("action") not in ACTS:
        return []
    if not eligible(constitution.body,option["action"])[0]:
        return []
    present={c.get("source_actor") for c in access.cues
             if type(c) is dict and c.get("kind")=="coactor_present"}
    results=[]
    for row in getattr(constitution,"care_practical_commitments",[]):
        if (row.get("status")!=(
                "HISTORICALLY_PRACTICED_CONTINGENT_CARE")
                or any(x.get('mode')=='SUSPEND_PARTICULAR_RECRUITMENT'
                       and x.get('basis',{}).get('location')==access.location
                       for x in row.get('revisions',[]))
                or row.get("operation")!=option["action"]
                or row.get("recipient_ref") not in present):
            continue
        results.append({
            "option_id":stable_id("practiced_care_option",{
                "actor":constitution.actor,"clock":constitution.clock,
                "practice":row["id"],"operation":option["action"]}),
            "actor":constitution.actor,"as_of_clock":constitution.clock,
            "operation":option["action"],"project_id":None,
            "grounds_status":"HISTORICALLY_PRACTICED_PARTICULAR_CARE",
            "practice_ref":row["id"],
            "source_event_refs":copy(row["source_event_refs"]),
            "world_request":{
                "operation":option["action"],
                "addressed_party_ref":row["recipient_ref"],
                "material_object_ref":None},
            "binding_status":"OTHER_PRESENT_WORLD_STILL_QUALIFIES_CARE",
            "not_automatic_love_or_recipient_assent":True,
            "future_sufficient_bodily_material_resources":"WORLD_MUST_CHECK",
            "grade":GRADE})
    return results


def possible_care_practice_revisions(actor,experience,event_ref):
    """A recipient can also exercise power against the giver.

    Actual historically practiced care and a later personally received
    directed imposition are distinct facts. This provisional operation can
    suspend the PARTICULAR acquired shortcut, not erase care, withdraw all
    possible care, diagnose abuse, or identify why the Other acted.
    """
    from .attention_field import personally_received_directed_act
    aid=actor.get('id')
    received=personally_received_directed_act(experience)
    if (experience.get('actor')!=aid or not received
            or received['operation']!='IMPOSE'):return []
    paths=actor.get('evidence_paths',[])
    present=[p for p in paths if p.get('event')==event_ref
             and p.get('experience_ref')==experience.get('ref')
             and p.get('directed_encounter')==received
             and received['cue_ref'] in p.get('received_cue_refs',[])]
    if len(present)!=1:return []
    out=[]
    for row in actor.get('care_practical_commitments',[]):
        if (row.get('actor')!=aid
                or row.get('recipient_ref')!=received['counterpart_ref']
                or row.get('status')!='HISTORICALLY_PRACTICED_CONTINGENT_CARE'
                or row.get('revisions')):continue
        refs=row.get('source_contribution_refs',[])
        source=[x for x in actor.get('care_contribution_episodes',[])
                if x.get('id') in refs and x.get('actor')==aid
                and x.get('recipient_ref')==received['counterpart_ref']
                and x.get('location')==received['location']
                and x.get('selection_source')==CHOSEN
                and x.get('bodily_cost_rest_delta',0)>0
                and type(x.get('clock')) is int
                and x['clock']<received['clock']]
        if (len(refs)!=2 or len(source)!=2 or len(set(refs))!=2
                or [x['event_ref'] for x in source]!=row['source_event_refs']
                or [x['clock'] for x in source]!=row['source_clock_interval']
                or source[0]['clock']>=source[1]['clock']):continue
        if not all(any(p.get('event')==x['event_ref']
                       and p.get('experience_ref')==x['experience_ref']
                       and p.get('own_action')==x['operation']
                       for p in paths) for x in source):continue
        out.append({'kind':'REVISE_COSTLY_CARE_PRACTICE',
                    'practice_ref':row['id'],'revision_mode':'SUSPEND_PARTICULAR_RECRUITMENT',
                    'basis':{'actor':aid,'recipient_ref':received['counterpart_ref'],
                             'location':received['location'],
                             'earlier_contribution_refs':copy(refs),
                             'imposition_event_ref':event_ref,
                             'imposition_experience_ref':experience['ref'],
                             'received_directed_act':copy(received),
                             'not_care_as_consent_or_proof_of_motive':True}})
    return out[:16]


def admit_care_practice_revision(actor,experience,event_ref,proposal):
    meaning=proposal.get('interpretive_hypothesis')
    if (type(meaning) is not str or not meaning.strip() or len(meaning)>512
            or {k:v for k,v in proposal.items() if k!='interpretive_hypothesis'}
                not in possible_care_practice_revisions(actor,experience,event_ref)):
        raise ValueError('CARE_PRACTICE_REVISION_UNQUALIFIED')
    row=next(x for x in actor['care_practical_commitments']
             if x['id']==proposal['practice_ref'])
    row.setdefault('revisions',[]).append({
        'event_ref':event_ref,'experience_ref':experience['ref'],
        'basis':copy(proposal['basis']),
        'mode':proposal['revision_mode'],
        'interpretive_hypothesis_not_causal_truth':meaning.strip(),
        'original_practice_not_erased':True,'grade':GRADE})
    return {'kind':proposal['kind'],'practice_ref':row['id'],
            'status':'ADMITTED_PARTICULAR_CARE_RECRUITMENT_SUSPENSION','grade':GRADE}
