"""SORACLE R20 — worker-specific wage struggle afterlife.

A person who actually endorses a posted demand, withholds activity, or
personally inspects a later public wage decision can have a differentiated
history. None implies the person understands class relations, wishes to
strike, or knew an employer's private choice before inspecting public words.
The heuristic actor selection below is explicitly provisional fiction.
"""
from .types import stable_id,GRADE
from .wage_bargaining import AUTHOR,WITHHOLD,EMPLOYER_ACCEPT,EMPLOYER_REJECT

ACTS=frozenset((AUTHOR,WITHHOLD,EMPLOYER_ACCEPT,EMPLOYER_REJECT))


def record_worker_bargaining_experience(actor,experience,event_ref):
    if actor.get("id")!=experience.get("actor"):
        raise ValueError("R20_BARGAINING_FOREIGN_ACTOR")
    op=experience.get("own_action")
    clock=experience.get("clock")
    if type(clock) is not int or clock<0:
        raise ValueError("R20_BARGAINING_BAD_CLOCK")
    if not experience.get("participated"):
        return None
    observed=None
    if op in ACTS:
        if (experience.get("status")!="PERFORMED"
                or (experience.get("felt_enactment") or {}).get(
                    "attempted_operation")!=op):
            return None
        received=[x for x in experience.get("perceived_cues",[])
                  if type(x) is dict and
                  x.get("kind")=="performed_"+op.lower()
                  and x.get("source_actor")==actor["id"]
                  and type(x.get("id")) is str]
        if len(received)!=1:return None
        observed=received[0]
        classification="ACTOR_PERFORMED_WAGE_CONTEST_ACTION"
    elif op=="INSPECT":
        # Concrete earlier act of inspecting a public result, not omniscience
        # from being a bystander in the same institution.
        matching=[x for x in actor.get("notice_exposures",[])
                  if type(x) is dict and
                  type(x.get("inspected_at_clock")) is int
                  and x["inspected_at_clock"]==clock
                  and "wage_outcome" in x.get(
                      "public_words_available",[])]
        prior=[x for x in actor.get("wage_bargaining_experiences",[])
               if x.get("operation") in (AUTHOR,WITHHOLD)
               and type(x.get("clock")) is int and x["clock"]<clock]
        if len(matching)!=1 or not prior:
            return None
        observed={
            "id":matching[0]["id"],
            "public_notice_ref":matching[0]["public_notice_ref"]}
        classification="LATER_PUBLIC_EMPLOYER_RESULT_PERSONALLY_INSPECTED"
    else:
        return None
    ref=stable_id("actor_wage_contestation_experience",{
        "actor":actor["id"],"clock":clock,
        "event":event_ref,"public":observed["id"]})
    if any(x.get("id")==ref for x in actor.get(
            "wage_bargaining_experiences",[])):
        raise ValueError("R20_BARGAINING_DUPLICATE_LIVED_EXPERIENCE")
    row={
        "id":ref,"actor":actor["id"],
        "operation":op,"clock":clock,
        "event_ref":event_ref,
        "experience_ref":experience["ref"],
        "classification":classification,
        "personally_received_sign_ref":observed["id"],
        "public_result_notice_ref":observed.get("public_notice_ref"),
        "scope":"SPECIFIC_WAGE_INSTITUTION_AND_PUBLIC_WORDS",
        "labor_rights_did_not_depend_on_conscious_ideology":True,
        "inferred_private_employer_motive":"NOT_KNOWN",
        "recipients_comprehension_not_automatically_equal":True,
        "grade":GRADE}
    actor.setdefault("wage_bargaining_experiences",[]).append(row)
    return row


def choose_actor_bargaining_stance(options,body):
    """Offer at most one noncontradicted action from lived activity history.

    The default is NOT a universal human law, and it cannot force another's
    endorsement, a colleague's withdrawal or an employer's pay decision.
    """
    if type(body) is not dict:return None
    for operation,field in (
            (AUTHOR,"wage_bargaining_ground"),
            (WITHHOLD,"wage_withholding_ground")):
        found=[]
        for option in options:
            if option.get("action")!=operation:
                continue
            ground=option.get(field)
            if not isinstance(ground,dict):continue
            personal=(
                ground.get("actor_personally_performed_work_ref")
                if operation==AUTHOR else
                ground.get("actor_lived_prior_endorsement_ref"))
            if type(personal) is not str or not personal:
                continue
            if (option.get("psychodynamic_status")==
                    "UNRESOLVED_CONTRADICTION"
                    or option.get("preproject_recruitment",{}).get(
                        "status") in (
                        "ACQUIRED_NONPROJECT_WITHHOLD",
                        "UNRESOLVED_PREPROJECT_CONTRADICTION")
                    or option.get("project_courses")):
                continue
            found.append(option)
        if len(found)!=1:continue
        # Material hardship can motivate attention to wages, but this does
        # not decree that anyone must strike. Withholding requires bodily
        # reserves to allow autonomous choice in sourcefree heuristic.
        if operation==WITHHOLD and (
                body.get("nutrition",0)<.55 or body.get("rest",0)<.30):
            continue
        return {
            "action":operation,"project_id":None,
            "selection_grade":"SOURCEFREE_HISTORICAL_WORKER_WAGE_STANCE",
            "own_lived_source_ref":(
                found[0][field][
                    "actor_personally_performed_work_ref"]
                if operation==AUTHOR else
                found[0][field][
                    "actor_lived_prior_endorsement_ref"]),
            "employer_response_not_under_worker_control":True,
            "no_generalized_political_identity_inferred":True}
    return None
