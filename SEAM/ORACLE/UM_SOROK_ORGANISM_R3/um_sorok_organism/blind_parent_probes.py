"""SORACLE P013 — bounded whole-instrument blind *operative* parent probing.

This does NOT implement PYAT sampling or qualify any questionnaire. It makes
the existing blinded parent interview more than an unconstrained model
answer string: an externally supplied source-qualified question contract can
be evaluated only against the adult's surviving operative constitution,
with model-attested source citations checked against exact permitted refs.

No cached respondent answer, questionnaire-mediator form, or source target is
included. Agreement with original answers requires a separate blind court
and PYAT-issued measurement/eligibility semantics.
"""
from .historical_parent_bridge import actor_only_interview_packet
from .types import copy,GRADE
import math

MAX_PROBES=2048
MAX_VALUES=64


def _instrument(questions):
    if type(questions) is not list or not 1<=len(questions)<=MAX_PROBES:
        raise ValueError("BLIND_PROBE_INVALID_INSTRUMENT")
    ids=set()
    for q in questions:
        if (type(q) is not dict or type(q.get("id")) is not str
                or not q["id"] or q["id"] in ids
                or type(q.get("wording")) is not str or not q["wording"]
                or type(q.get("values")) is not list
                or not 2<=len(q["values"])<=MAX_VALUES
                or any(type(v) not in (str,int,float,bool)
                       or type(v) is float and not math.isfinite(v)
                       for v in q["values"])
                or len(set(str(v) for v in q["values"]))!=len(q["values"])):
            raise ValueError("BLIND_PROBE_UNQUALIFIED_QUESTION")
        ids.add(q["id"])


def actor_evidence_roster(packet):
    """Produce identities from ACTUAL admissible adult functioning, not targets."""
    adult=packet["actor"]
    roster={}
    for key,source in adult["acquired_non_questionnaire_forms"].items():
        roster["form:"+key]={"kind":"OPERATIVE_FORM","source_ref":key}
    for p in adult["activities"]:
        if type(p) is dict and type(p.get("id")) is str:
            roster["project:"+p["id"]]={"kind":"OPERATIVE_PROJECT",
                                        "source_ref":p["id"]}
    for h in adult["experienced_participation"]:
        if type(h) is dict and type(h.get("id")) is str:
            roster["participation:"+h["id"]]={
                "kind":"ACTOR_LIVED_PARTICIPATION",
                "source_ref":h["id"]}
    for h in adult["functional_bindings"]:
        if type(h) is dict:
            ref=h.get("id") or h.get("binding_ref")
            if type(ref) is str:
                roster["functional:"+ref]={"kind":"ACQUIRED_FUNCTION",
                                           "source_ref":ref}
    return roster


def blind_operational_interview(actor,questions,semantic,world=None):
    """Typed prospective respondent test; unsupported answers must abstain.

    The evidence refs prove only that the model *selected existing sources*,
    not that those sources empirically entail the proposed answer. Qualification
    of question interpretations and actual respondent agreement is separate.
    """
    _instrument(questions)
    ids=[q["id"] for q in questions]
    packet=actor_only_interview_packet(actor,ids,world)
    roster=actor_evidence_roster(packet)
    packet["instrument"]=copy(questions)
    packet["evidence_roster"]=copy(roster)
    packet["grounding_contract"]=(
        "Every response must be an object with value exactly in that "
        "question's allowed set, source_refs a nonempty subset of the "
        "evidence_roster, and status=HYPOTHETICAL_ACTOR_FUNCTION_READOUT. "
        "Absence of adequate sources requires explicit abstention. Never "
        "reproduce a cached instrument answer or invent evidence refs.")
    reply=semantic.proposal("blind_adult_interview",packet)
    proposed=reply.get("responses",{})
    if type(proposed) is not dict or set(proposed)-set(ids):
        raise ValueError("BLIND_PROBE_INVALID_RESPONSE_KEYS")
    admissible={q["id"]:q for q in questions}
    accepted={};refused={};quality={}
    for ident in ids:
        if ident not in proposed:
            refused[ident]="NO_QUALIFIED_ANSWER_ATTEMPTED"
            continue
        candidate=proposed[ident]
        if (type(candidate) is not dict or
                candidate.get("status")!=(
                    "HYPOTHETICAL_ACTOR_FUNCTION_READOUT")):
            raise ValueError("BLIND_PROBE_NO_TYPED_HYPOTHESIS")
        value=candidate.get("value")
        if not any(type(value) is type(x) and value==x
                   for x in admissible[ident]["values"]):
            raise ValueError("BLIND_PROBE_RESPONSE_OUTSIDE_ISSUED_VALUES")
        refs=candidate.get("source_refs")
        if (type(refs) is not list or not refs
                or len(refs)!=len(set(refs))
                or any(type(x) is not str or x not in roster for x in refs)):
            raise ValueError("BLIND_PROBE_FORGED_OR_MISSING_GROUNDS")
        accepted[ident]=copy(value)
        quality[ident]={
            "evidence_ref_ids":copy(refs),
            "grounding":"REAL_ACTOR_OPERATIVE_SOURCE_ID_REFERENCED",
            "semantic_interpretation":"UNVALIDATED_HYPOTHESIS",
            "not_source_respondent_truth":True,
            "not_empirical_predictive_success":True,
            "source_grade":GRADE}
    return {
        "responses":accepted,"unanswered":[x for x in ids if x not in accepted],
        "abstention_reasons":refused,
        "question_count":len(ids),"answer_count":len(accepted),
        "actor_grounding_receipts":quality,
        "source_answer_keys_not_supplied":True,
        "respondent_fidelity":"NOT_MEASURED",
        "whole_joint_correspondence":"NOT_EVALUATED_IN_THIS_CALL",
        "source_qualification":"NEEDS_PYAT_ORIGINAL_SURVEY_INSTRUMENT",
        "provider_grade":getattr(semantic.provider,"grade",
                                "EXTERNAL_MODEL_UNQUALIFIED"),
        "grade":GRADE}
