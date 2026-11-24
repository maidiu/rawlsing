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


def _adverse_body_course(before,after):
    """Personally measurable cost, NOT proof an attempted act caused harm.

    Bounded sourcefree axes only; never infer another person's intentions,
    happiness, trauma, or whether the actor ought to avoid the operation.
    """
    if type(before) is not dict or type(after) is not dict:
        raise ValueError("GENESIS_MISSING_BODILY_TRANSITION")
    observed={}
    for name,op in (("pain","rises"),("comfort","falls")):
        b=before.get(name);a=after.get(name)
        if (type(b) not in (int,float) or type(a) not in (int,float)
                or not math.isfinite(b) or not math.isfinite(a)
                or not 0<=b<=1 or not 0<=a<=1):
            raise ValueError("GENESIS_UNQUALIFIED_BODY")
        delta=a-b if op=="rises" else b-a
        if delta>=MIN_RELIEF:
            observed[name]=round(delta,5)
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
    adverse=_adverse_body_course(before,after)
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
        "personally_lived_adverse_course":copy(adverse) if attempted else {},
        "adverse_course_not_objective_causation":True,
        "received_sign_refs":refs,
        "personally_perceived_sign_sources":[
            {"cue_ref":c["id"],"kind":c.get("kind"),
             "source_actor":c.get("source_actor")}
            for c in cues if type(c.get("id")) is str],
        "received_sign_tags":sorted({str(t).lower()
            for c in cues for t in c.get("tags",[])
            if type(t) is str and t}),
        "selection_source":source_selection or "NO_OWN_SELECTED_ATTEMPT",
        "selected_addressed_party_ref":(
            ((experience.get("own_practical_selection") or {}).get("world_request") or {})
            .get("addressed_party_ref")),
        "selected_practical_option_ref":(
            (experience.get("own_practical_selection") or {}).get("option_id")),
        "does_not_prove_original_willingness":True,
        "actor_does_not_know_objective_cause":True,
        "not_a_retrospectively_invented_episode":True,
        "grade":GRADE}
    actor.setdefault("lived_genesis_episodes",[]).append(witness)
    return witness


def _dependency_contrast(actor, experience, event_ref, current):
    """An actual conditional joint practice, later failed addressed use,
    and a distinct independently enacted means of bodily relief.

    This does not equate nourishment with love, prove permanent loss of
    the Other, or transfer their material power to the actor.
    """
    if (experience.get("status")!="PERFORMED"
            or experience.get("reciprocated_partner") is not None
            or current.get("actor_felt_attempt")!="EAT"
            or not current.get("received_relief",{}).get("nutrition")
            or current.get("unfinished_own_activity")):
        return None
    signs=[s for s in current.get("personally_perceived_sign_sources",[])
           if s.get("kind")=="performed_eat" and s.get("source_actor")==actor["id"]]
    if len(signs)!=1 or not current.get("received_sign_tags"):return None
    rows=actor.get("lived_genesis_episodes",[])
    participation=actor.get("participation_history",[])
    eligible_practices=[]
    for practice in actor.get("joint_practices",[])[-64:]:
        if (practice.get("actor")!=actor["id"]
                or practice.get("operation")!="SIGNAL"
                or practice.get("location")!=current.get("location")
                or practice.get("status")!="ACQUIRED_CONDITIONAL_COORDINATION_NOT_DYAD_MASTERY"):
            continue
        origin=practice.get("origin_event_refs",[])
        refs=practice.get("source_participation_refs",[])
        if len(origin)!=2 or len(refs)!=2:continue
        other=practice.get("coactor_ref")
        supported=[x for x in participation if x.get("id")==refs[1]
                   and x.get("actor")==actor["id"]
                   and x.get("event_ref")==origin[1]
                   and x.get("own_attempted_operation")=="SIGNAL"
                   and x.get("own_status")=="PERFORMED"
                   and x.get("joint_participation_perceived")
                   and x.get("reciprocated_partner_actor_visible")==other]
        if len(supported)!=1:continue
        success=[x for x in rows if x.get("actor")==actor["id"]
                 and x.get("event_ref")==origin[1]
                 and x.get("experience_ref")==supported[0].get("experience_ref")
                 and x.get("actor_felt_attempt")=="SIGNAL"
                 and x.get("received_relief",{}).get("nutrition")
                 and not x.get("unfinished_own_activity")]
        if len(success)!=1:continue
        success=success[0]
        losses=[x for x in rows if x.get("actor")==actor["id"]
                and success["clock"]<x["clock"]<current["clock"]
                and x.get("location")==current.get("location")
                and x.get("actor_felt_attempt")=="SIGNAL"
                and x.get("selected_addressed_party_ref")==other
                and x.get("unfinished_own_activity")
                and not x.get("received_relief",{}).get("nutrition")]
        if not losses:continue
        loss=losses[-1]
        witness=[x for x in participation if x.get("actor")==actor["id"]
                 and x.get("event_ref")==loss["event_ref"]
                 and x.get("experience_ref")==loss["experience_ref"]
                 and x.get("own_status") in ("PARTIAL","BLOCKED")
                 and not x.get("joint_participation_perceived")]
        if len(witness)!=1:continue
        if any(e.get("dependency_loss_basis",{}).get("failed_episode_ref")==loss["id"]
               and e.get("dependency_loss_basis",{}).get("practice_ref")==practice["id"]
               for e in actor.get("possible_ends",[])):continue
        eligible_practices.append((practice,success,loss,witness[0]))
    # Multiple distinct histories remain competing, not pooled into one.
    if len(eligible_practices)!=1:return None
    practice,success,loss,failed=eligible_practices[0]
    basis={"practice_ref":practice["id"],"supported_episode_ref":success["id"],
           "failed_episode_ref":loss["id"],"failed_participation_ref":failed["id"],
           "independent_episode_ref":current["id"],"historical_counterpart_ref":practice["coactor_ref"],
           "supported_event_ref":success["event_ref"],"failed_event_ref":loss["event_ref"],
           "independent_event_ref":event_ref,
           "loss_of_successful_coordination_not_permanent_absence":True}
    witness=stable_id("dependency_contrast",{"actor":actor["id"],"basis":basis})
    reading={"mode":"TRY_INDEPENDENT_MEANS_AFTER_INTERRUPTED_SUPPORT",
             "candidate_ref":stable_id("genetic_end_reading",{"witness":witness}),
             "object":"explore independent nourishment after an unfinished learned coordination",
             "means":["EAT"],"addressed_party_ref":None,
             "source_received_sign_ref":signs[0]["cue_ref"]}
    return {"kind":"ACQUIRE_GENETIC_POSSIBLE_END",
            "genesis_witness_ref":witness,
            "prior_unfinished_episode_ref":loss["id"],
            "later_relief_episode_ref":current["id"],
            "later_perceived_cue_ref":signs[0]["cue_ref"],
            "possible_object":reading["object"],"licensed_end_constructions":[reading],
            "chosen_end_mode":reading["mode"],"chosen_end_candidate_ref":reading["candidate_ref"],
            "relieved_bodily_axis":"nutrition",
            "genesis_family":"INTERRUPTED_ACQUIRED_SUPPORT_THEN_INDEPENDENT_RELIEF",
            "possible_means":["EAT"],"cue_terms":current["received_sign_tags"][:12],
            "dependency_loss_basis":basis,
            "sourcefree_genesis_not_an_empirical_motive_law":True,
            "actor_conscious_explanation_not_imputed":True,"grade":GRADE}


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
    dependency=_dependency_contrast(actor,experience,event_ref,cur)
    if dependency is not None:return [dependency]
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
    # The same material history can support distinct, competing *possible*
    # organizations. The LLM may select one typed interpretation; it cannot
    # supply an unseen caregiver, unattained bodily benefit, or invented act.
    licensed=[{
        "mode":"EXPERIMENT_WITH_OWN_PRIOR_OPERATION",
        "candidate_ref":stable_id("genetic_end_reading",{
            "actor":actor["id"],"later":cur["id"],"mode":"OWN_ACT"}),
        "object":hypothesized_end,
        "means":means,
        "addressed_party_ref":None,
        "source_received_sign_ref":cur["received_sign_refs"][0],
    }]
    independent_others=sorted({
        x["source_actor"] for x in cur.get(
            "personally_perceived_sign_sources",[])
        if type(x.get("source_actor")) is str
        and x["source_actor"]!=actor["id"]
        and x.get("kind") in (
            "performed_care","performed_feed","performed_signal")})
    if earlier["actor_felt_attempt"]=="SIGNAL" and (
            "SIGNAL" in means):
        for other in independent_others[:2]:
            sourced=next(x for x in cur["personally_perceived_sign_sources"]
                if x["source_actor"]==other and x.get("kind") in (
                    "performed_care","performed_feed","performed_signal"))
            licensed.append({
                "mode":"TRY_ADDRESSING_PERSONALLY_PERCEIVED_RESPONDER",
                "candidate_ref":stable_id("genetic_end_reading",{
                    "actor":actor["id"],"later":cur["id"],
                    "mode":"RESPONDER","other":other}),
                "object":"try signaling toward a previously sensed "+
                         "responder when seeking "+relieved_axis,
                "means":["SIGNAL"],"addressed_party_ref":other,
                "source_received_sign_ref":sourced["cue_ref"],
            })
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
        "licensed_end_constructions":licensed,
        "chosen_end_mode":licensed[0]["mode"],
        "chosen_end_candidate_ref":licensed[0]["candidate_ref"],
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
                  "later_relief_episode_ref"):
        if proposal.get(field)!=expected[field]:
            raise ValueError("GENESIS_HISTORICAL_SOURCE_FORGERY_"+field)
    if (proposal.get("genesis_family",expected["genesis_family"])!=expected["genesis_family"]
            or proposal.get("dependency_loss_basis")!=expected.get("dependency_loss_basis")):
        raise ValueError("GENESIS_DEPENDENCY_HISTORY_FORGERY")
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
    selected_ref=proposal.get("chosen_end_candidate_ref",
                              expected["chosen_end_candidate_ref"])
    licensed=[v for v in expected["licensed_end_constructions"]
              if v["candidate_ref"]==selected_ref]
    if len(licensed)!=1:
        raise ValueError("GENESIS_UNLICENSED_QUALITATIVE_END")
    selected=licensed[0]
    # Distinct actually sensed responders may be represented by different
    # cue identities. The model must identify the EXACT one for its chosen
    # interpretation, rather than inherit the generic first cue.
    if proposal.get("later_perceived_cue_ref")!=selected[
            "source_received_sign_ref"]:
        raise ValueError("GENESIS_SELECTED_RESPONDER_SIGN_FORGED")
    mode=selected["mode"]
    if (proposal.get("chosen_end_mode",mode)!=mode or
            type(selected_ref) is not str):
        raise ValueError("GENESIS_END_MODE_CONFLICT")
    meaning=proposal.get("possible_object")
    # Reconstruct a contextual operation from lived sources, rather than
    # granting an arbitrary LLM-authored goal. A model can choose between
    # *licensed alternative readings* of one contradictory history.
    if meaning!=selected["object"]:
        raise ValueError("GENESIS_OPERATIVE_END_NOT_DERIVED_FROM_HISTORY")
    if any(x not in selected["means"] for x in provided):
        raise ValueError("GENESIS_SELECTED_END_MEANS_INCOMPATIBLE")
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
        "genetic_end_mode":mode,
        "genetic_end_candidate_ref":selected_ref,
        "addressed_party_ref":selected["addressed_party_ref"],
        "source_responding_sign_ref":selected["source_received_sign_ref"],
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
    if expected.get("dependency_loss_basis"):
        basis=copy(expected["dependency_loss_basis"])
        end["dependency_loss_basis"]=basis
        end["actual_contrasted_episode_refs"].insert(0,basis["supported_episode_ref"])
        end["source_event_refs"].insert(0,basis["supported_event_ref"])
        end["no_automatic_disaffection_or_independent_mastery"]=True
    actor.setdefault("possible_ends",[]).append(end)
    return {"kind":proposal["kind"],"possible_end":ident,
            "genesis_witness_ref":expected["genesis_witness_ref"],
            "status":"ADMITTED_CONTRASTED_POSSIBILITY_NOT_YET_MOTIVE",
            "grade":GRADE}


def possible_dependency_project_takeups(actor, experience, event_ref):
    """Offer a later enduring undertaking, not a reward for successful eating.

    The same dependency-derived end must have recruited an actual earlier
    trial. A distinct later self-selected nontrial course supplies the
    occasion for optional semantic reorganization. Original relation,
    event and practical power remain distinct from the newly acquired end.
    """
    aid=actor.get("id")
    clock=experience.get("clock")
    selected=experience.get("own_practical_selection") or {}
    request=selected.get("world_request") or {}
    if (experience.get("actor")!=aid or type(clock) is not int
            or experience.get("own_action")!="EAT"
            or experience.get("status")!="PERFORMED"
            or not experience.get("participated")
            or (experience.get("felt_enactment") or {}).get("attempted_operation")!="EAT"
            or selected.get("actor")!=aid
            or selected.get("status")!="ACTOR_POLICY_PRACTICAL_ATTEMPT"
            or selected.get("possible_end_trial") is not None
            or selected.get("selected_project_refs")!=[]
            or type(selected.get("option_id")) is not str
            or request.get("operation")!="EAT"
            or request.get("addressed_party_ref") is not None
            or experience.get("reciprocated_partner") is not None):
        return []
    rows=actor.get("lived_genesis_episodes",[])
    now=[x for x in rows if x.get("actor")==aid and x.get("event_ref")==event_ref
         and x.get("experience_ref")==experience.get("ref") and x.get("clock")==clock
         and x.get("actor_felt_attempt")=="EAT"
         and x.get("selected_practical_option_ref")==selected["option_id"]
         and x.get("received_relief",{}).get("nutrition")
         and not x.get("unfinished_own_activity")
         and not x.get("personally_lived_adverse_course")]
    if len(now)!=1:return []
    cur=now[0]
    signs=[c for c in experience.get("perceived_cues",[])
           if c.get("kind")=="performed_eat" and c.get("source_actor")==aid
           and c.get("id") in cur["received_sign_refs"]]
    if len(signs)!=1:return []
    candidates=[]
    for end in actor.get("possible_ends",[])[-128:]:
        if (end.get("status")!="POSSIBLE_NOT_ACQUIRED_MOTIVE"
                or end.get("genesis_family")!="INTERRUPTED_ACQUIRED_SUPPORT_THEN_INDEPENDENT_RELIEF"
                or end.get("possible_means")!=["EAT"]
                or not end.get("dependency_loss_basis")):continue
        origin=end["dependency_loss_basis"]
        seed=[x for x in rows if x.get("id")==origin.get("independent_episode_ref")
              and x.get("actor")==aid and x.get("event_ref")==end.get("origin_event")]
        if len(seed)!=1 or seed[0].get("location")!=cur.get("location"):continue
        if not ({str(t).casefold() for t in signs[0].get("tags",[])}
                & {str(t).casefold() for t in end.get("cue_terms",[])}):continue
        trials=[]
        for t in end.get("trial_history",[]):
            if (t.get("operation")!="EAT" or t.get("actor_experienced_status")!="PERFORMED"
                    or t.get("eliciting_possible_end_ref")!=end["id"]
                    or t.get("event_ref")==event_ref):continue
            lived=[x for x in rows if x.get("actor")==aid and x.get("event_ref")==t.get("event_ref")
                   and x.get("experience_ref")==t.get("experience_ref")
                   and x.get("actor_felt_attempt")=="EAT"
                   and seed[0]["clock"]<x["clock"]<clock
                   and x.get("location")==cur.get("location")
                   and x.get("received_relief",{}).get("nutrition")
                   and not x.get("unfinished_own_activity")
                   and not x.get("personally_lived_adverse_course")
                   and set(t.get("received_sign_refs",[]))&set(x.get("received_sign_refs",[]))]
            if len(lived)==1:trials.append((t,lived[0]))
        if not trials:continue
        t,prior=max(trials,key=lambda pair:pair[1]["clock"])
        basis={"dependency_practice_ref":origin["practice_ref"],
               "origin_independent_episode_ref":seed[0]["id"],
               "earlier_lived_trial_ref":t["id"],"earlier_trial_episode_ref":prior["id"],
               "later_independent_episode_ref":cur["id"],"later_selected_option_ref":selected["option_id"],
               "source_event_refs":[seed[0]["event_ref"],prior["event_ref"],event_ref],
               "not_proof_of_motive_fulfillment_or_mastery":True}
        candidates.append({"kind":"TAKE_UP_POSSIBLE_END","possible_end_ref":end["id"],
                           "later_perceived_cue_ref":signs[0]["id"],"means":["EAT"],
                           "priority":.4,"dependency_takeup_basis":basis})
    return candidates[:3]
