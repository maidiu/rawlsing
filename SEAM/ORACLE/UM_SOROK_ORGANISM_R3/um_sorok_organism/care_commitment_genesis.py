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
                or _suspended_at(row,access.location)
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
                or _suspended_at(row,received['location'])
                or any(x.get('event_ref')==event_ref for x in row.get('revisions',[]))):continue
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
                not in possible_all_care_practice_revisions(actor,experience,event_ref)):
        raise ValueError('CARE_PRACTICE_REVISION_UNQUALIFIED')
    row=next(x for x in actor['care_practical_commitments']
             if x['id']==proposal['practice_ref'])
    prior_suspended=_suspended_at(row,proposal['basis']['location'])
    row.setdefault('revisions',[]).append({
        'retained_suspension':prior_suspended and proposal['revision_mode']=='KEEP_CONTRADICTORY_RECRUITMENT',
        'event_ref':event_ref,'experience_ref':experience['ref'],
        'basis':copy(proposal['basis']),
        'mode':proposal['revision_mode'],
        'interpretive_hypothesis_not_causal_truth':meaning.strip(),
        'original_practice_not_erased':True,'grade':GRADE})
    return {'kind':proposal['kind'],'practice_ref':row['id'],
            'status':{'SUSPEND_PARTICULAR_RECRUITMENT':'ADMITTED_PARTICULAR_CARE_RECRUITMENT_SUSPENSION',
                      'KEEP_CONTRADICTORY_RECRUITMENT':'ADMITTED_CARE_CONTRADICTION_WITHOUT_ABOLITION',
                      'REOPEN_PARTICULAR_RECRUITMENT':'ADMITTED_PARTICULAR_CARE_RECRUITMENT_REOPENING'}[proposal['revision_mode']],
            'grade':GRADE}


def _site_revision(row,site):
    return next((x for x in reversed(row.get('revisions',[]))
                 if x.get('basis',{}).get('location')==site),None)


def _suspended_at(row,site):
    rev=_site_revision(row,site) or {}
    return rev.get('mode')=='SUSPEND_PARTICULAR_RECRUITMENT' or rev.get('retained_suspension') is True


def _qualified_care_sources(actor,row,site):
    """Historical care sources survive later contradictory significance."""
    refs=row.get('source_contribution_refs',[])
    rows=[x for x in actor.get('care_contribution_episodes',[])
          if x.get('id') in refs and x.get('actor')==actor['id']
          and x.get('recipient_ref')==row.get('recipient_ref')
          and x.get('location')==site and x.get('selection_source')==CHOSEN
          and type(x.get('clock')) is int and x.get('bodily_cost_rest_delta',0)>0]
    if (len(refs)!=2 or len(set(refs))!=2 or len(rows)!=2
            or [x['event_ref'] for x in rows]!=row.get('source_event_refs')
            or [x['clock'] for x in rows]!=row.get('source_clock_interval')
            or rows[0]['clock']>=rows[1]['clock']):return []
    paths=actor.get('evidence_paths',[])
    if not all(any(p.get('event')==x['event_ref']
                   and p.get('experience_ref')==x['experience_ref']
                   and p.get('own_action')==x['operation'] for p in paths) for x in rows):
        return []
    return rows


def lived_care_authority_encounters(actor,experience,event_ref):
    """One can receive real power exercised by someone one has cared for.

    This neither attributes the anonymous institutional sanction to a known
    victim nor declares that earlier care caused it. Directed third-party
    imposition is independently qualified from the actually received R26
    sign. A person's own participation and a witnessed act are not merged.
    """
    aid=actor['id'];site=experience.get('location');clock=experience.get('clock')
    if (experience.get('actor')!=aid or type(clock) is not int
            or site!=actor.get('location')):return []
    paths=[p for p in actor.get('evidence_paths',[])
           if p.get('event')==event_ref and p.get('experience_ref')==experience.get('ref')]
    if len(paths)!=1:return []
    path=paths[0];signs=[]
    for c in experience.get('perceived_cues',[]):
        if (c.get('id') not in path.get('received_cue_refs',[])
                or c.get('location')!=site or c.get('clock')!=clock
                or type(c.get('source_actor')) is not str or c['source_actor']==aid):continue
        if (c.get('kind')=='performed_impose'
                and c.get('public_person_directed_act_not_private_intention') is True
                and type(c.get('actor_accessible_target_ref')) is str
                and c['actor_accessible_target_ref'] not in (aid,c['source_actor'])):
            signs.append({'source_actor_ref':c['source_actor'],'received_cue_ref':c['id'],
                          'operation':'IMPOSE','visible_target_ref':c['actor_accessible_target_ref']})
        elif c.get('kind')=='performed_sanction_pantry_access':
            rec=path.get('received_enacted_food_power')
            if (rec and rec.get('actor')==aid and rec.get('event_ref')==event_ref
                    and rec.get('experience_ref')==experience['ref']
                    and rec.get('received_cue_ref')==c['id']
                    and rec.get('source_actor_ref')==c['source_actor']
                    and rec.get('operation')=='SANCTION_PANTRY_ACCESS'
                    and rec.get('clock')==clock and rec.get('location')==site):
                signs.append({'source_actor_ref':c['source_actor'],'received_cue_ref':c['id'],
                              'operation':'SANCTION_PANTRY_ACCESS',
                              'sanction_subject':'NOT_ESTABLISHED_BY_RECEIVED_SIGN'})
    out=[]
    for row in actor.get('care_practical_commitments',[]):
        if row.get('actor')!=aid or row.get('status')!='HISTORICALLY_PRACTICED_CONTINGENT_CARE':
            continue
        sources=_qualified_care_sources(actor,row,site)
        if not sources or sources[-1]['clock']>=clock:continue
        for sign in signs:
            if sign['source_actor_ref']!=row.get('recipient_ref'):continue
            out.append({'formation_source':'WITNESSED_POWER_OF_CARE_RECIPIENT',
                        'actor':aid,'recipient_ref':row['recipient_ref'],'location':site,
                        'clock':clock,'practice_ref':row['id'],
                        'earlier_contribution_refs':copy(row['source_contribution_refs']),
                        'earlier_care_event_refs':copy(row['source_event_refs']),
                        'power_event_ref':event_ref,'power_experience_ref':experience['ref'],
                        'received_power_sign':copy(sign),
                        'care_not_proof_of_assent_causation_or_other_motive':True})
    return out[:12]


def possible_witnessed_care_revisions(actor,experience,event_ref):
    out=[]
    for b in lived_care_authority_encounters(actor,experience,event_ref):
        row=next(x for x in actor['care_practical_commitments'] if x['id']==b['practice_ref'])
        if any(x.get('event_ref')==event_ref for x in row.get('revisions',[])):continue
        modes=('KEEP_CONTRADICTORY_RECRUITMENT',) if _suspended_at(row,b['location']) else (
            'KEEP_CONTRADICTORY_RECRUITMENT','SUSPEND_PARTICULAR_RECRUITMENT')
        # KEEP on a suspended practice conserves the suspension; it is not
        # a reopening merely because an adverse occurrence is interpreted.
        for mode in modes:
            out.append({'kind':'REVISE_COSTLY_CARE_PRACTICE','practice_ref':row['id'],
                        'revision_mode':mode,'basis':copy(b)})
    return out


def _revision_clock(row,revision):
    b=revision.get('basis',{})
    return b.get('clock',(b.get('received_directed_act') or {}).get('clock'))


def possible_care_reopenings(actor,experience,event_ref):
    """Two actually renewed independent courses can qualify a new relation.

    The suspended historical shortcut is not used as proof of renewed
    willingness; the person must actually select care through another
    available course. A fresh adverse personally received event interrupts
    the renewal series. No cancellation of the prior contradiction.
    """
    aid=actor['id'];site=experience.get('location');clock=experience.get('clock')
    if (experience.get('actor')!=aid or type(clock) is not int
            or experience.get('status')!='PERFORMED'
            or experience.get('own_action') not in ACTS):return []
    paths=actor.get('evidence_paths',[]);out=[]
    for row in actor.get('care_practical_commitments',[]):
        if row.get('actor')!=aid or not _suspended_at(row,site):continue
        revision=_site_revision(row,site);after=_revision_clock(row,revision)
        if type(after) is not int or after>=clock:continue
        if not _qualified_care_sources(actor,row,site):continue
        other=row['recipient_ref']
        for p in paths:
            directed=p.get('directed_encounter',{})
            power=p.get('received_enacted_food_power',{})
            adverse=(directed.get('counterpart_ref')==other and directed.get('operation')=='IMPOSE'
                     and directed.get('location')==site)
            adverse_power=(power.get('source_actor_ref')==other and
                           power.get('operation')=='SANCTION_PANTRY_ACCESS'
                           and power.get('location')==site)
            witnessed=p.get('witnessed_directed_power',{})
            adverse_witness=(witnessed.get('source_actor_ref')==other
                             and witnessed.get('location')==site)
            for v,ok in ((directed,adverse),(power,adverse_power),(witnessed,adverse_witness)):
                if ok and type(v.get('clock')) is int and after<v['clock']<clock:
                    after=v['clock']
        renewed=[x for x in actor.get('care_contribution_episodes',[])
                 if x.get('actor')==aid and x.get('recipient_ref')==other
                 and x.get('operation')==row['operation'] and x.get('location')==site
                 and x.get('selection_source')==CHOSEN and x.get('bodily_cost_rest_delta',0)>0
                 and type(x.get('clock')) is int and after<x['clock']<=clock
                 and any(p.get('event')==x.get('event_ref')
                         and p.get('experience_ref')==x.get('experience_ref')
                         and p.get('own_action')==x['operation']
                         for p in paths)]
        renewed=sorted(renewed,key=lambda x:x['clock'])[-2:]
        if (len(renewed)!=2 or renewed[0]['clock']>=renewed[1]['clock']
                or renewed[-1]['event_ref']!=event_ref
                or renewed[-1]['experience_ref']!=experience['ref']):continue
        b={'formation_source':'RENEWED_ACTUAL_CARE_COURSES','actor':aid,
           'recipient_ref':other,'location':site,'clock':clock,
           'practice_ref':row['id'],'suspension_event_ref':revision['event_ref'],
           'renewed_contribution_refs':[x['id'] for x in renewed],
           'renewed_event_refs':[x['event_ref'] for x in renewed],
           'not_proof_of_safety_reconciliation_or_love':True}
        out.append({'kind':'REVISE_COSTLY_CARE_PRACTICE','practice_ref':row['id'],
                    'revision_mode':'REOPEN_PARTICULAR_RECRUITMENT','basis':b})
    return out[:12]


def possible_all_care_practice_revisions(actor,experience,event_ref):
    return (possible_care_practice_revisions(actor,experience,event_ref)
            +possible_witnessed_care_revisions(actor,experience,event_ref)
            +possible_care_reopenings(actor,experience,event_ref))


def annotate_care_contradictions(constitution,access,options):
    """Conserve opposed histories on the exact recipient-specific course.

    A contradiction may coexist with an available operation. Do not mark
    every possible recipient, sum valences, supply a conscious explanation,
    or remove material care/project alternatives.
    """
    currents=[];readset=set()
    for row in constitution.care_practical_commitments:
        if row.get('actor')!=constitution.actor:continue
        revisions=[x for x in row.get('revisions',[])
                   if x.get('basis',{}).get('location')==access.location]
        if not revisions:continue
        revision=revisions[-1]
        adverse=[x for x in revisions if x.get('mode') in (
            'KEEP_CONTRADICTORY_RECRUITMENT','SUSPEND_PARTICULAR_RECRUITMENT')]
        if not adverse:continue
        matching=[a for o in options if o['action']==row['operation']
                  for a in o.get('practical_alternatives',[])
                  if a.get('world_request',{}).get('addressed_party_ref')==row['recipient_ref']]
        if not matching:continue
        x={'practice_ref':row['id'],'recipient_ref':row['recipient_ref'],
           'operation':row['operation'],'location':access.location,
           'historical_care_event_refs':copy(row['source_event_refs']),
           'contradiction_event_refs':[v['event_ref'] for v in adverse],
           'latest_revision_event_ref':revision['event_ref'],
           'particular_recruitment_suspended':_suspended_at(row,access.location),
           'reopening_not_erasure_of_prior_contradiction':True,
           'not_automatic_choice_or_conscious_reason':True,'grade':GRADE}
        for a in matching:a.setdefault('care_contradictions_analytic_only',[]).append(copy(x))
        currents.append({'kind':'HISTORICALLY_CONTRADICTORY_CARE_RELATION',**x})
        readset.add(row['id'])
        readset.update(x['historical_care_event_refs']+x['contradiction_event_refs'])
    return {'currents':currents,'readset':sorted(readset)}
