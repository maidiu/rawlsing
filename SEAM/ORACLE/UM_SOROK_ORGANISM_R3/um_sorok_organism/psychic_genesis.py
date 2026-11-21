"""SORACLE P004/P011/P023 — a concrete, falsifiable history-to-new-end organ.

A failed *felt* activity and later *personally received* bodily relief can make
a future relationship to that relief prospectable. They are not proof of a
stable motive, unconscious trauma, infant verbal belief, or a universal
developmental law. The sources are in this actor's historical constitution,
not an analyst's unrestricted world archive. Only the existing development
owner may admit the proposed possible end, and only a later independent
episode can take it up as an operative project.

This is constructive sourcefree psychological abduction. Neither a single
episode nor an LLM's invented noun can create the end by itself.
"""
from .types import stable_id, copy, GRADE
from .organism import ACTIONS, eligible
import math

RELIEF_AXES=("comfort","nutrition","regulation","rest")
MIN_RELIEF=.025


def _delta(before,after):
    if type(before) is not dict or type(after) is not dict:
        raise ValueError("GENESIS_MISSING_BODILY_TRANSITION")
    observed={}
    for name in RELIEF_AXES:
        b=before.get(name);a=after.get(name)
        if (type(b) not in (int,float) or type(a) not in (int,float)
                or not math.isfinite(b) or not math.isfinite(a)
                or not 0<=b<=1 or not 0<=a<=1):
            raise ValueError("GENESIS_UNQUALIFIED_BODY")
        if a-b>=MIN_RELIEF:
            observed[name]=round(a-b,5)
    return observed


def conserve_lived_episode(actor,experience,event_ref,before,after,
                           source_selection=None):
    """Distinct written subjective/felt witness, never an objective cause."""
    if (experience.get("actor")!=actor.get("id") or
            type(event_ref) is not str or not event_ref or
            type(experience.get("clock")) is not int or
            type(experience.get("ref")) is not str):
        raise ValueError("GENESIS_FOREIGN_OR_UNCLOCKED_EXPERIENCE")
    cues=experience.get("perceived_cues")
    if type(cues) is not list or any(type(c) is not dict for c in cues):
        raise ValueError("GENESIS_INVALID_ACTOR_RECEIVED_CUES")
    refs=[c.get("id") for c in cues if type(c.get("id")) is str]
    if len(refs)!=len(set(refs)):
        raise ValueError("GENESIS_DUPLICATED_EXPOSURE")
    relief=_delta(before,after)
    own=experience.get("own_action")
    felt=experience.get("felt_enactment") or {}
    attempted=(type(own) is str and own in ACTIONS
               and experience.get("participated") is True
               and felt.get("attempted_operation")==own
               and felt.get("objective_result_not_inferred") is True)
    incomplete=(attempted and experience.get("status") in (
                "BLOCKED","PARTIAL"))
    # A material/relational event can be beneficial without being grasped as
    # "care" by a preverbal infant. Require actual sensory/bodily receipt.
    received=bool(refs) and bool(relief) and experience.get(
        "participated") is True
    if not attempted and not received:
        return None
    ref=stable_id("personally_lived_genesis_episode",{
        "actor":actor["id"],"event":event_ref,
        "experience":experience["ref"]})
    if any(x.get("id")==ref for x in actor.get(
            "lived_genesis_episodes",[])):
        raise ValueError("GENESIS_DUPLICATE_ACTOR_EVENT")
    witness={
        "id":ref,"actor":actor["id"],"event_ref":event_ref,
        "experience_ref":experience["ref"],"clock":experience["clock"],
        "location":experience.get("location"),
        "actor_felt_attempt":own if attempted else None,
        "unfinished_own_activity":bool(incomplete),
        "received_relief":copy(relief) if received else {},
        "received_sign_refs":refs,
        "received_sign_tags":sorted({str(t).lower()
            for c in cues for t in c.get("tags",[])
            if type(t) is str and t}),
        "selection_source":source_selection or "NO_OWN_SELECTED_ATTEMPT",
        "does_not_prove_original_willingness":True,
        "actor_does_not_know_objective_cause":True,
        "not_a_retrospectively_invented_episode":True,
        "grade":GRADE}
    actor.setdefault("lived_genesis_episodes",[]).append(witness)
    return witness


def possible_contrast_end(actor,experience,event_ref):
    """A fresh developmental candidate requiring different prior episodes.

    A previously lived unsuccessful activity and an *independent* later
    positive bodily receipt jointly make an otherwise absent end possible.
    An LLM may choose a richer phenomenological meaning, but it may only
    reference this actual pair, these offered means and these received signs.
    """
    if experience.get("actor")!=actor.get("id"):return []
    rows=actor.get("lived_genesis_episodes",[])
    current=[x for x in rows if x.get("event_ref")==event_ref
             and x.get("experience_ref")==experience.get("ref")]
    if len(current)!=1 or not current[0].get("received_relief"):
        return []
    cur=current[0]
    prior=[x for x in rows if x.get("actor")==actor["id"]
           and type(x.get("clock")) is int
           and x["clock"]<cur["clock"]
           and x.get("unfinished_own_activity")
           and x.get("event_ref")!=event_ref
           and type(x.get("actor_felt_attempt")) is str]
    if not prior:return []
    earlier=max(prior,key=lambda x:(x["clock"],x["id"]))
    # The new good is not an automatic attempt to repeat identical behavior.
    # It may be addressed through some operation which actually exists
    # for the actor's present developmental body; never an invented faculty.
    means=[op for op in (earlier["actor_felt_attempt"],"SIGNAL","ORIENT")
           if op in ACTIONS and eligible(actor["body"],op)[0]]
    means=list(dict.fromkeys(means))[:3]
    if not means or not cur["received_sign_refs"]:return []
    # Without personally received cue terms, no globally named "caregiver"
    # or semantic category is installed inside a child.
    # The present sign vocabulary comes from the person's own sensed cues;
    # no analyst-named generic category can stand in for an absent sign.
    cues=cur["received_sign_tags"][:12]
    if not cues:
        return []
    # An LLM may offer a fallible interpretation, but cannot *create*
    # the operative goal by replacing actual episode/operation/need identity
    # with a more attractive unlicensed narrative.
    relieved_axis=sorted(cur["received_relief"],
        key=lambda axis:(-cur["received_relief"][axis],axis))[0]
    hypothesized_end=(
        "explore whether "+earlier["actor_felt_attempt"].lower()+
        " can help obtain "+relieved_axis+
        " after the earlier unfinished attempt")
    witness=stable_id("contrasted_lived_possibility",{
        "actor":actor["id"],"first":earlier["id"],"later":cur["id"]})
    if any(e.get("genesis_witness_ref")==witness
           for e in actor.get("possible_ends",[])):
        return []
    return [{
        "kind":"ACQUIRE_GENETIC_POSSIBLE_END",
        "genesis_witness_ref":witness,
        "prior_unfinished_episode_ref":earlier["id"],
        "later_relief_episode_ref":cur["id"],
        "later_perceived_cue_ref":cur["received_sign_refs"][0],
        "possible_object":hypothesized_end,
        "relieved_bodily_axis":relieved_axis,
        "genesis_family":"SENSED_INTERRUPTION_THEN_RELIEF",
        "possible_means":means,
        "cue_terms":cues,
        "sourcefree_genesis_not_an_empirical_motive_law":True,
        "actor_conscious_explanation_not_imputed":True,
        "grade":GRADE}]


def admit_contrast_end(actor,experience,event_ref,proposal):
    """Existing development admission calls this on its staged actor copy."""
    if proposal.get("kind")!="ACQUIRE_GENETIC_POSSIBLE_END":
        raise ValueError("GENESIS_UNKNOWN_OPERATION")
    qualified=possible_contrast_end(actor,experience,event_ref)
    if len(qualified)!=1:
        raise ValueError("GENESIS_NO_DISTINCT_LIVED_CONTRAST")
    expected=qualified[0]
    for field in ("genesis_witness_ref","prior_unfinished_episode_ref",
                  "later_relief_episode_ref","later_perceived_cue_ref"):
        if proposal.get(field)!=expected[field]:
            raise ValueError("GENESIS_HISTORICAL_SOURCE_FORGERY_"+field)
    provided=proposal.get("possible_means")
    if (type(provided) is not list or not provided
            or len(provided)!=len(set(provided))
            or any(x not in expected["possible_means"] for x in provided)):
        raise ValueError("GENESIS_UNEXERCISED_FUTURE_MEANS")
    cue_terms=proposal.get("cue_terms",expected["cue_terms"])
    if (type(cue_terms) is not list or not cue_terms
            or any(type(x) is not str or x not in expected["cue_terms"]
                   for x in cue_terms)):
        raise ValueError("GENESIS_UNRECEIVED_SIGN_GENERALIZATION")
    meaning=proposal.get("possible_object")
    # Earlier sourcefree code accepted ANY string, which made the end's
    # operative content model-authored, not actually constituted by history.
    # Preserve free interpretation separately from world/actor affordance.
    if meaning!=expected["possible_object"]:
        raise ValueError("GENESIS_OPERATIVE_END_NOT_DERIVED_FROM_HISTORY")
    interpretation=proposal.get("interpretive_hypothesis")
    if (interpretation is not None and
            (type(interpretation) is not str or len(interpretation)>512)):
        raise ValueError("GENESIS_INVALID_INTERPRETIVE_HYPOTHESIS")
    ident=stable_id("historically_emergent_end",{
        "actor":actor["id"],"witness":expected["genesis_witness_ref"]})
    if any(p.get("id")==ident for p in actor.get("possible_ends",[])):
        raise ValueError("GENESIS_DUPLICATE_END")
    first=next(x for x in actor["lived_genesis_episodes"]
               if x["id"]==expected["prior_unfinished_episode_ref"])
    second=next(x for x in actor["lived_genesis_episodes"]
                if x["id"]==expected["later_relief_episode_ref"])
    end={
        "id":ident,"genesis_witness_ref":expected["genesis_witness_ref"],
        "possible_object":meaning,
        "genesis_family":expected["genesis_family"],
        "relieved_bodily_axis":expected["relieved_bodily_axis"],
        "model_interpretation_hypothesis_not_operative_end":interpretation,
        "possible_means":copy(provided),"cue_terms":copy(cue_terms),
        "status":"POSSIBLE_NOT_ACQUIRED_MOTIVE",
        "origin_event":event_ref,
        "origin_clock":experience["clock"],
        "experience_ref":experience["ref"],
        "actor_perceived_cue_ref":expected["later_perceived_cue_ref"],
        "eliciting_actor_action":first["actor_felt_attempt"],
        "actual_contrasted_episode_refs":[first["id"],second["id"]],
        "source_event_refs":[first["event_ref"],second["event_ref"]],
        "different_lived_events_required":True,
        "not_predeclared_project":True,
        "not_a_conscious_infant_end":True,
        "still_requires_future_takeup_to_become_motive":True,
        "phenomenological_meaning_is_defeasible":True,
        "grade":GRADE}
    actor.setdefault("possible_ends",[]).append(end)
    return {"kind":proposal["kind"],"possible_end":ident,
            "genesis_witness_ref":expected["genesis_witness_ref"],
            "status":"ADMITTED_CONTRASTED_POSSIBILITY_NOT_YET_MOTIVE",
            "grade":GRADE}
