"""SORACLE R17 — a lived collective outcome can change future practical inquiry.

Objective institutional change is not itself a resident's ideology. Only a
person with a personally received public sign, an earlier personally
inspected procedure, adequate cultural-linguistic capacity, and their own
historical contribution can *possibly* acquire a procedural expectation.
Its first use is to make inspecting another posted procedure a historical
option. It grants no property right, proof of causal theory or generalized
freedom from other institutions.
"""
from .types import GRADE, stable_id, copy

OP="ACQUIRE_SITUATED_PUBLIC_PROCEDURE_EXPECTATION"
SIGN="performed_sign_food_petition"
RESULT="COLLECTIVE_FOOD_ACCESS_RIGHTS_CHANGED"


def possible_institutional_learning(actor,experience,event_ref):
    if actor.get("id")!=experience.get("actor") or not event_ref:
        raise ValueError("INSTITUTIONAL_LEARNING_ACTOR_MISMATCH")
    if actor.get("body",{}).get("language",0)<.28:
        return []
    if type(experience.get("clock")) is not int:
        raise ValueError("INSTITUTIONAL_LEARNING_NO_EVENT_CLOCK")
    received=[x for x in experience.get("perceived_cues",[])
              if type(x) is dict and x.get("kind")==SIGN
              and x.get("description")==RESULT
              and type(x.get("id")) is str]
    if len(received)!=1:return []
    own=[
        x for x in actor.get("power_exercises",[])
        if x.get("operation")=="SIGN_FOOD_PETITION"
        and x.get("attempt_status_analyst_receipt")=="PERFORMED"
        and type(x.get("event_ref")) is str
        and type(x.get("event_clock")) is int
        and x["event_clock"]<=experience["clock"]]
    source=[
        x for x in actor.get("notice_exposures",[])
        if type(x) is dict and
        "public_petition" in x.get("public_words_available",[])
        and type(x.get("public_notice_ref")) is str
        and type(x.get("inspected_at_clock")) is int
        and x["inspected_at_clock"]<=experience["clock"]]
    if not own or not source:return []
    if any(x.get("origin_public_event_ref")==event_ref for x
           in actor.get("institutional_expectations",[])):
        return []
    return [{
        "kind":"POSSIBLE_SITUATED_COLLECTIVE_PROCEDURE_LEARNING",
        "received_public_sign_ref":received[0]["id"],
        "own_performed_signature_exercise_ref":own[-1]["id"],
        "previously_inspected_public_notice_ref":source[-1][
            "public_notice_ref"],
        "possible_operation":"INSPECT_FUTURE_POSTED_PROCEDURE",
        "not_global_class_consciousness":True,
        "not_proof_of_understanding_the_other_signers":True,
        "grade":GRADE}]


def one_bounded_proposal(rows):
    if len(rows)!=1:return []
    row=rows[0]
    return [{
        "kind":OP,
        "received_public_sign_ref":row["received_public_sign_ref"],
        "own_signature_exercise_ref":row[
            "own_performed_signature_exercise_ref"],
        "inspected_notice_ref":row[
            "previously_inspected_public_notice_ref"],
        "scope":"POSTED_INSTITUTIONAL_PROCEDURE",
        "no_claim_to_universal_emancipation":True}]


def admit_public_procedure_expectation(actor,experience,event_ref,proposal):
    if actor.get("id")!=experience.get("actor"):
        raise ValueError("INSTITUTIONAL_LEARNING_FOREIGN_ACTOR")
    if actor.get("body",{}).get("language",0)<.28:
        raise ValueError("INSTITUTIONAL_LEARNING_NO_CULTURAL_MEANS")
    if type(experience.get("clock")) is not int:
        raise ValueError("INSTITUTIONAL_LEARNING_NO_EVENT_CLOCK")
    cue=proposal.get("received_public_sign_ref")
    if len([x for x in experience.get("perceived_cues",[])
            if type(x) is dict and x.get("id")==cue and
            x.get("kind")==SIGN and x.get("description")==RESULT])!=1:
        raise ValueError("INSTITUTIONAL_LEARNING_NO_LIVED_PUBLIC_RESULT")
    exercised=proposal.get("own_signature_exercise_ref")
    if not any(x.get("id")==exercised and
               x.get("operation")=="SIGN_FOOD_PETITION" and
               x.get("attempt_status_analyst_receipt")=="PERFORMED"
               and type(x.get("event_clock")) is int
               and x["event_clock"]<=experience["clock"]
               for x in actor.get("power_exercises",[])):
        raise ValueError("INSTITUTIONAL_LEARNING_FOREIGN_SIGNATURE")
    notice=proposal.get("inspected_notice_ref")
    if not any(x.get("public_notice_ref")==notice and
               "public_petition" in x.get("public_words_available",[])
               and type(x.get("inspected_at_clock")) is int
               and x["inspected_at_clock"]<=experience["clock"]
               for x in actor.get("notice_exposures",[])):
        raise ValueError("INSTITUTIONAL_LEARNING_NO_PRIOR_INSPECTION")
    if proposal.get("scope")!="POSTED_INSTITUTIONAL_PROCEDURE":
        raise ValueError("INSTITUTIONAL_LEARNING_OVERGENERALIZED_SCOPE")
    if any(x.get("origin_public_event_ref")==event_ref for x
           in actor.get("institutional_expectations",[])):
        raise ValueError("INSTITUTIONAL_LEARNING_DUPLICATE_EVENT")
    ident=stable_id("learned_public_procedure_possibility",{
        "actor":actor["id"],"event":event_ref,
        "observed":cue,"own_signature":exercised})
    row={
        "id":ident,"actor":actor["id"],
        "origin_public_event_ref":event_ref,
        "observed_at_clock":experience["clock"],
        "own_received_experience_ref":experience["ref"],
        "received_public_change_sign_ref":cue,
        "actual_own_signature_practice_ref":exercised,
        "previously_inspected_procedure_ref":notice,
        "scope":"POSTED_INSTITUTIONAL_PROCEDURE",
        "operative_possible_means":"INSPECT",
        "actual_generalized_rights":"NOT_GRANTED",
        "truth_of_future_public_notices":"NOT_GUARANTEED",
        "all_signers_intentions":"NOT_KNOWN",
        "explicit_actor_political_theory":"NOT_INFERRED",
        "status":"PROVISIONAL",
        "grade":GRADE}
    actor.setdefault("institutional_expectations",[]).append(row)
    return {"kind":OP,"expectation_ref":ident,"grade":GRADE}


def possible_lived_institutional_differences(actor, experience, event_ref):
    """Revisit an acquired public-practice expectation after a later lived sign.

    The same historically known public procedure may be experienced in a
    materially different way on a later occasion. This makes a *possible*
    difference available to an actor-specific semantic construction model,
    not an automatic critique of institutions or praise of their authority.
    The old and new events must BOTH be in the actor's own history.
    """
    if (type(event_ref) is not str or not event_ref
            or actor.get("id") != experience.get("actor")
            or type(experience.get("ref")) is not str):
        raise ValueError("R24_INSTITUTIONAL_DIFFERENCE_ACTOR_OR_EVENT")
    clock = experience.get("clock")
    if type(clock) is not int or clock < 0:
        raise ValueError("R24_INSTITUTIONAL_DIFFERENCE_UNCLOCKED")
    if actor.get("body", {}).get("language", 0) < .28:
        return []
    cues = experience.get("perceived_cues", [])
    if type(cues) is not list:
        raise ValueError("R24_INSTITUTIONAL_DIFFERENCE_INVALID_CUES")
    # NOT all events: a live public act with an identifiable source and a
    # personally receivable result, rather than co-presence, analyst financial
    # knowledge, a notice shell or the same earlier collective outcome.
    later = [c for c in cues if type(c) is dict
             and type(c.get("id")) is str and c["id"]
             and type(c.get("source_actor")) is str and c["source_actor"]
             and type(c.get("kind")) is str
             and c["kind"].startswith("performed_")
             and c.get("description") == "ATTEMPT_NOT_COMPLETED"]
    if len(later) != 1:
        return []
    eligible_prior = []
    for row in actor.get("institutional_expectations", []):
        if (type(row) is not dict or
                row.get("scope") != "POSTED_INSTITUTIONAL_PROCEDURE" or
                row.get("status") != "PROVISIONAL" or
                type(row.get("id")) is not str or
                type(row.get("observed_at_clock")) is not int or
                row["observed_at_clock"] >= clock or
                row.get("origin_public_event_ref") == event_ref or
                type(row.get("own_received_experience_ref")) is not str):
            continue
        # The stored prior expectation was qualified through a personally
        # inspected public notice, the actor's own performed signature, and
        # a received public change. Preserve that full source lineage.
        notice = row.get("previously_inspected_procedure_ref")
        if not any(type(n) is dict
                   and n.get("public_notice_ref") == notice
                   and type(n.get("inspected_at_clock")) is int
                   and n["inspected_at_clock"] <= row["observed_at_clock"]
                   for n in actor.get("notice_exposures", [])):
            continue
        signed = row.get("actual_own_signature_practice_ref")
        if not any(type(x) is dict and x.get("id") == signed
                   and x.get("operation") == "SIGN_FOOD_PETITION"
                   and x.get("attempt_status_analyst_receipt") == "PERFORMED"
                   for x in actor.get("power_exercises", [])):
            continue
        eligible_prior.append(row)
    return [{
        "prior_expectation_ref": row["id"],
        "prior_public_event_ref": row["origin_public_event_ref"],
        "prior_actor_experience_ref": row["own_received_experience_ref"],
        "later_received_sign_ref": later[0]["id"],
        "later_perceived_source_actor_ref": later[0]["source_actor"],
        "prior_public_procedure_was_successfully_practiced": True,
        "later_practice_was_observed_unfinished": True,
        "causal_source_of_later_obstruction": "NOT_KNOWN",
        "does_not_prove_same_institution_or_legitimate_authority": True,
        "no_necessary_ideological_conclusion": True,
        "not_an_actor_conscious_theory": True,
        "grade": GRADE,
    } for row in eligible_prior[:16]]


def qualify_lived_institutional_difference(actor, experience, event_ref, claim):
    """Match a proposed historical contrast against the *freshly rederived* court.

    An LLM may propose how to REVALUE an already acquired psychological
    relation, but it cannot invent the old public practice, later sign, or
    what the institution materially did. This is a causal precondition for a
    voluntary psychodynamic reinterpretation, not its unique explanation.
    """
    if type(claim) is not dict:
        raise ValueError("R24_INVALID_INSTITUTIONAL_DIFFERENCE_CLAIM")
    grounds = possible_lived_institutional_differences(
        actor, experience, event_ref)
    eligible = [g for g in grounds if
                claim.get("prior_expectation_ref") == g["prior_expectation_ref"]
                and claim.get("later_received_sign_ref") ==
                g["later_received_sign_ref"]]
    if len(eligible) != 1:
        raise ValueError("R24_UNQUALIFIED_LIVED_INSTITUTIONAL_DIFFERENCE")
    ground = eligible[0]
    return {
        "id": stable_id("lived_institutional_difference", {
            "actor": actor["id"], "event": event_ref,
            "earlier_expectation": ground["prior_expectation_ref"],
            "later_sign": ground["later_received_sign_ref"]}),
        "earlier_expectation_ref": ground["prior_expectation_ref"],
        "earlier_personal_experience_ref": ground["prior_actor_experience_ref"],
        "later_personal_experience_ref": experience["ref"],
        "later_received_sign_ref": ground["later_received_sign_ref"],
        "later_perceived_source_actor_ref":
            ground["later_perceived_source_actor_ref"],
        "institutional_cause_not_concluded": True,
        "actor_moral_conclusion_not_imposed": True,
        "grade": GRADE,
    }
