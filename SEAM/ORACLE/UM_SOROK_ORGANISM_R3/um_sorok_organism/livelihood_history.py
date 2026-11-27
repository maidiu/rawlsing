"""SORACLE R19 — personally experienced income obstruction, not assumed ideology.

An actor may sense that its own WORK attempt was unfinished and later use
actually existing worker relief, while the causal employment decision remains
in the independent world. No automatic belief about an employer's motives.
"""
from .types import stable_id,GRADE


def conserve_incomplete_work(actor,experience,event_ref):
    if actor.get("id")!=experience.get("actor"):
        raise ValueError("R19_WORK_EXPERIENCE_FOREIGN_ACTOR")
    if (experience.get("own_action")!="WORK"
            or experience.get("status") not in ("PARTIAL","BLOCKED")
            or not experience.get("participated")
            or (experience.get("felt_enactment") or {}).get(
                "attempted_operation")!="WORK"):
        return None
    seen=[x for x in experience.get("perceived_cues",[])
          if type(x) is dict and
          x.get("kind")=="performed_work"
          and x.get("source_actor")==actor["id"]
          and x.get("description")=="ATTEMPT_NOT_COMPLETED"
          and type(x.get("id")) is str]
    if len(seen)!=1:return None
    if type(experience.get("clock")) is not int:
        raise ValueError("R19_WORK_EXPERIENCE_NO_CLOCK")
    ident=stable_id("lived_unfinished_wage_activity",{
        "actor":actor["id"],"event":event_ref,
        "cue":seen[0]["id"]})
    if any(x.get("id")==ident for x in actor.get(
            "labor_dependency_encounters",[])):
        raise ValueError("R19_WORK_EXPERIENCE_DUPLICATE")
    row={
        "id":ident,"actor":actor["id"],
        "clock":experience["clock"],"location":experience.get("location"),
        "experience_ref":experience["ref"],"world_event_ref":event_ref,
        "own_attempted_work":"WORK",
        "received_unfinished_sign_ref":seen[0]["id"],
        "reason_employer_or_body_or_structural":"NOT_INFERRED",
        "future_income_absent_or_lost":"NOT_YET_MEASURED_BY_TIP",
        "not_developed_political_consciousness":True,
        "grade":GRADE}
    actor.setdefault("labor_dependency_encounters",[]).append(row)
    return row


def sourcefree_relief_recruitment(options):
    """The fallible next action remains the actor's option, not relief owed."""
    candidates=[]
    for option in options:
        if option.get("action")!="DRAW_WAGE_RELIEF":
            continue
        ground=option.get("labor_relief_ground")
        if not ground or type(ground.get("personal_failed_work_ref")) is not str:
            continue
        if option.get("psychodynamic_status")=="UNRESOLVED_CONTRADICTION":
            continue
        if option.get("preproject_recruitment",{}).get("status") in (
                "ACQUIRED_NONPROJECT_WITHHOLD",
                "UNRESOLVED_PREPROJECT_CONTRADICTION"):
            continue
        if option.get("project_courses"):
            continue
        candidates.append(option)
    if len(candidates)!=1:return None
    return {
        "action":"DRAW_WAGE_RELIEF",
        "project_id":None,
        "selection_grade":"SOURCEFREE_LIVED_UNFINISHED_WORK_RELIEF_POSSIBILITY",
        "lived_source_ref":candidates[0]["labor_relief_ground"][
            "personal_failed_work_ref"],
        "employer_motive_not_known":True,
        "collective_entitlement_not_inferred":True}

def possible_recurrent_work_orientation(actor, experience, event_ref):
    """A source-qualified historical *possibility*, not a work personality.

    R25 uses the actor's actual R6 power-exercise receipts: two distinct
    earlier personally performed/attempted WORK episodes, then a later own
    WORK experience with one sensory-accessible public sign. Financial
    control, an employer's reasons, and whether the person learns to endure
    or withhold work remain separate and underdetermined.
    """
    if (actor.get("id") != experience.get("actor")
            or type(event_ref) is not str or not event_ref
            or type(experience.get("ref")) is not str):
        raise ValueError("R25_WORK_HISTORY_ACTOR_OR_EVENT_MISMATCH")
    clock = experience.get("clock")
    if type(clock) is not int or clock < 0:
        raise ValueError("R25_WORK_HISTORY_UNCLOCKED")
    site = experience.get("location")
    if (type(site) is not str or not site
            or site != actor.get("location")):
        return []
    if (experience.get("own_action") != "WORK"
            or experience.get("participated") is not True
            or (experience.get("felt_enactment") or {}).get(
                "attempted_operation") != "WORK"
            or experience.get("status") not in
                ("PERFORMED", "PARTIAL", "BLOCKED")):
        return []
    cues = experience.get("perceived_cues", [])
    if type(cues) is not list:
        raise ValueError("R25_WORK_HISTORY_INVALID_PERSONAL_CUES")
    # The actor's sensor-qualified world projection carries less than the
    # actual world audit: a blocked WORK sign is not a diagnosis of wage
    # discipline or a claim that the employer intended the obstruction.
    signs = [c for c in cues if type(c) is dict
             and c.get("kind") == "performed_work"
             and c.get("source_actor") == actor["id"]
             and type(c.get("id")) is str and c["id"]
             and ((experience["status"] == "PERFORMED"
                   and c.get("description") != "ATTEMPT_NOT_COMPLETED")
                  or (experience["status"] in ("BLOCKED", "PARTIAL")
                      and c.get("description") == "ATTEMPT_NOT_COMPLETED"))]
    if len(signs) != 1:
        return []
    previous = {}
    for row in actor.get("power_exercises", []):
        if (type(row) is not dict or row.get("actor") != actor["id"]
                or row.get("operation") != "WORK"
                or row.get("felt_attempt") is not True
                or row.get("encounter_location") != site
                or type(row.get("id")) is not str
                or type(row.get("event_ref")) is not str
                or row["event_ref"] == event_ref
                or type(row.get("event_clock")) is not int
                or row.get("id") != stable_id("power_exercise", {
                    "actor": actor["id"], "world_event": row["event_ref"],
                    "operation": "WORK"})
                or row["event_clock"] >= clock
                or row.get("attempt_status_analyst_receipt") not in
                    ("PERFORMED", "PARTIAL", "BLOCKED")
                or type(row.get("personally_received_sign_refs")) is not list
                or not row["personally_received_sign_refs"]
                or any(type(x) is not str or not x
                       for x in row["personally_received_sign_refs"])):
            continue
        # Do not turn repeated receipts of the SAME objective attempt into
        # the independent lived occasions needed to form a work history.
        if row["event_ref"] in previous:
            continue
        previous[row["event_ref"]] = row
    prior = sorted(previous.values(), key=lambda r: (
        r["event_clock"], r["event_ref"]))
    if len(prior) < 2:
        return []
    first, second = prior[-2:]
    if first["event_clock"] >= second["event_clock"]:
        return []
    return [{
        "prior_exercised_work_refs": [first["id"], second["id"]],
        "prior_world_event_refs": [first["event_ref"], second["event_ref"]],
        "current_received_work_sign_ref": signs[0]["id"],
        "current_world_event_ref": event_ref,
        "current_experience_ref": experience["ref"],
        "current_site": site,
        "possible_operation": "WORK",
        "choice_of_approach_withhold_or_no_change": "OPEN",
        "not_a_conscious_work_ethic": True,
        "no_employer_intention_or_wage_account_knowledge_imputed": True,
        "not_a_work_contract_or_property_right": True,
        "grade": GRADE,
    }]


def qualify_recurrent_work_orientation(actor, experience, event_ref, claim):
    """Admit only a model-selected meaning supported by three own episodes."""
    if type(claim) is not dict:
        raise ValueError("R25_INVALID_WORK_HISTORY_CLAIM")
    qualified = possible_recurrent_work_orientation(
        actor, experience, event_ref)
    matches = [q for q in qualified
               if claim.get("prior_exercised_work_refs") ==
                    q["prior_exercised_work_refs"]
               and claim.get("current_received_work_sign_ref") ==
                    q["current_received_work_sign_ref"]
               and claim.get("current_world_event_ref") ==
                    q["current_world_event_ref"]]
    if len(matches) != 1:
        raise ValueError("R25_WORK_HISTORY_SOURCE_NOT_QUALIFIED")
    q = matches[0]
    return {
        "id": stable_id("actor_recurrent_work_life", {
            "actor": actor["id"], "event": event_ref,
            "prior": q["prior_world_event_refs"],
            "current": q["current_received_work_sign_ref"]}),
        "previous_personal_work_exercise_refs":
            list(q["prior_exercised_work_refs"]),
        "previous_objective_attempt_refs":
            list(q["prior_world_event_refs"]),
        "present_received_public_sign_ref":
            q["current_received_work_sign_ref"],
        "present_personal_experience_ref":
            q["current_experience_ref"],
        "site": q["current_site"],
        "actor_acquired_interpretation": "MODEL_PROPOSED_NOT_NECESSARY",
        "world_cause_and_employer_intentions": "UNRESOLVED",
        "grade": GRADE,
    }


def possible_relief_reconstitution(actor, experience, event_ref):
    """Actually exercised temporary relief can qualify a change in a work orientation.

    Neither a funded transfer nor a suspended contract proves freedom from
    wage dependence. This limited semantic occasion concerns a previously
    acquired practical approach to WORK, not a diagnosis or a class identity.
    """
    aid=actor['id']; clock=experience.get('clock'); site=experience.get('location')
    selection=experience.get('own_practical_selection') or {}
    if (experience.get('actor')!=aid or type(clock) is not int
            or site!=actor.get('location') or experience.get('own_action')!='DRAW_WAGE_RELIEF'
            or experience.get('status')!='PERFORMED'
            or experience.get('participated') is not True
            or selection.get('actor')!=aid
            or selection.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT'):
        return []
    signs=[c for c in experience.get('perceived_cues',[])
           if c.get('kind')=='performed_draw_wage_relief'
           and c.get('source_actor')==aid
           and c.get('description')=='REAL_WAGE_RELIEF_TRANSFERRED'
           and type(c.get('id')) is str]
    if len(signs)!=1:return []
    paths=[x for x in actor.get('evidence_paths',[])
           if x.get('event')==event_ref and x.get('experience_ref')==experience.get('ref')
           and x.get('own_action')=='DRAW_WAGE_RELIEF'
           and signs[0]['id'] in x.get('received_cue_refs',[])]
    if len(paths)!=1:return []
    out=[]
    for row in actor.get('historical_orientations',[]):
        ground=row.get('recurrent_livelihood_ground')
        if (not ground or row.get('actor')!=aid or row.get('location')!=site
                or row.get('operation')!='WORK' or row.get('orientation_mode')!='APPROACH'
                or row.get('revisions') or type(row.get('origin_clock')) is not int
                or row['origin_clock']>=clock):continue
        failures=[f for f in actor.get('labor_dependency_encounters',[])
                  if f.get('actor')==aid and f.get('location')==site
                  and type(f.get('clock')) is int and row['origin_clock']<f['clock']<clock
                  and f.get('own_attempted_work')=='WORK'
                  and any(p.get('event')==f.get('world_event_ref')
                          and p.get('experience_ref')==f.get('experience_ref')
                          and f.get('received_unfinished_sign_ref') in p.get('received_cue_refs',[])
                          for p in actor.get('evidence_paths',[]))]
        if not failures:continue
        f=max(failures,key=lambda x:x['clock'])
        if not any(p.get('event')==row['origin_event']
                   and p.get('experience_ref')==row['origin_experience_ref']
                   and ground.get('present_received_public_sign_ref') in p.get('received_cue_refs',[])
                   for p in actor.get('evidence_paths',[])):continue
        basis={'actor':aid,'location':site,'orientation_ref':row['id'],
               'orientation_origin_event':row['origin_event'],
               'unfinished_work_ref':f['id'],'unfinished_work_event_ref':f['world_event_ref'],
               'relief_event_ref':event_ref,'relief_experience_ref':experience['ref'],
               'received_relief_sign_ref':signs[0]['id'],
               'not_proof_of_independence_or_controller_intent':True}
        out.append({'kind':'REVISE_HISTORICAL_ORIENTATION','orientation_ref':row['id'],
                    'revision_mode':'INHIBIT','perceived_cue_ref':signs[0]['id'],
                    'relief_reconstitution_basis':basis})
    return out[:8]
