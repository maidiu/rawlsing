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
