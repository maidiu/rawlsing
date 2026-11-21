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
