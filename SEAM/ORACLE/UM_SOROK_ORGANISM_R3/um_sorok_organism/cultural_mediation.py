"""SORACLE R3: world-grounded cultural object mediation, not installed language.

A particular other person can enact public SPEAK with a materially present,
visible object. The learner only has an accessible auditory/visual *occasion*,
not the speaker's word, private intention or a mastered semantic category.
A distinct learner-initiated investigation of that same object can condition
a reusable, provisional way to attend to it. The world keeps object identity
and ownership. The learner keeps only personally acquired practices.

These are typed fictional hypotheses, not a universal social-learning law.
"""
from .types import copy, stable_id, GRADE
from .organism import eligible

DEMONSTRATION_KIND="performed_speak"
ACQUIRED="ACQUIRED_SITUATED_PUBLIC_OBJECT_REFERENCE"
SUSPENDED="SUSPENDED_AFTER_FAILED_OBJECT_INQUIRY"


def _present_obj(world,actor_id,object_ref):
    loc=world.get("positions",{}).get(actor_id)
    obj=world.get("material_objects",{}).get(object_ref)
    return (type(obj) is dict and obj.get("id")==object_ref
            and obj.get("visible") is True
            and obj.get("location")==loc)


def conserve_personally_heard_reference(actor,experience,event_ref,world):
    """Retain the actual source sign, never the speaker's alleged intention."""
    if (experience.get("actor")!=actor.get("id")
            or type(event_ref) is not str or not event_ref
            or type(experience.get("clock")) is not int
            or experience.get("clock")!=world.get("clock")):
        raise ValueError("CULTURE_EXPERIENCE_NOT_AT_ACTUAL_WORLD_EVENT")
    rows=[]
    for cue in experience.get("perceived_cues",[]):
        if not (type(cue) is dict and
                cue.get("kind")==DEMONSTRATION_KIND
                and cue.get("actual_spoken_object_demonstration") is True
                and type(cue.get("source_actor")) is str
                and cue["source_actor"]!=actor["id"]
                and type(cue.get("id")) is str
                and type(cue.get("material_object_ref")) is str):
            continue
        obj=cue["material_object_ref"]
        if not _present_obj(world,actor["id"],obj):continue
        if cue.get("modality")!="auditory":continue
        ref=stable_id("personally_heard_object_reference",{
            "actor":actor["id"],"event":event_ref,"cue":cue["id"],
            "object":obj})
        if any(x.get("id")==ref for x in actor.get("cultural_demonstrations",[])):
            raise ValueError("CULTURE_DUPLICATED_PERSONAL_DEMONSTRATION")
        row={"id":ref,"actor":actor["id"],"event_ref":event_ref,
            "experience_ref":experience["ref"],
            "clock":experience["clock"],
            "heard_source_actor":cue["source_actor"],
            "received_public_sign_ref":cue["id"],
            "object_ref":obj,"location":experience.get("location"),
            "speaker_was_observed_not_assumed_teacher":True,
            "public_sound_actually_heard":True,
            "object_materially_present":True,
            "specific_word_not_encoded":True,
            "speaker_private_meaning_not_known":True,
            "not_yet_an_acquired_cultural_meaning":True,
            "grade":GRADE}
        actor.setdefault("cultural_demonstrations",[]).append(row)
        rows.append(row)
    return rows


def possible_cultural_object_inquiry(actor,experience,event_ref):
    """Formation requires a distinct *own actual investigation* of this object."""
    if experience.get("actor")!=actor.get("id"):return []
    if not (experience.get("own_action")=="INSPECT"
            and experience.get("status")=="PERFORMED"
            and (experience.get("felt_enactment") or {}).get(
                "attempted_operation")=="INSPECT"
            and type(experience.get("clock")) is int):
        return []
    signs=[c for c in experience.get("perceived_cues",[])
           if type(c) is dict and c.get("kind")=="performed_inspect"
           and type(c.get("material_object_ref")) is str
           and type(c.get("id")) is str
           and c.get("source_actor")==actor["id"]]
    if len(signs)!=1:return []
    obj=signs[0]["material_object_ref"]
    prior=[x for x in actor.get("cultural_demonstrations",[])
           if x.get("actor")==actor["id"]
           and x.get("object_ref")==obj
           and x.get("event_ref")!=event_ref
           and x.get("location")==experience.get("location")
           and type(x.get("clock")) is int
           and x["clock"]<experience["clock"]]
    if not prior:return []
    earlier=max(prior,key=lambda x:(x["clock"],x["id"]))
    identity=stable_id("situated_public_object_reference",{
        "actor":actor["id"],"demonstration":earlier["id"],
        "investigation":event_ref,"object":obj})
    if any(x.get("id")==identity for x in actor.get(
            "cultural_reference_practices",[])):
        return []
    return [{
        "kind":"ACQUIRE_SITUATED_CULTURAL_REFERENCE",
        "practice_ref":identity,"object_ref":obj,
        "demonstration_ref":earlier["id"],
        "personal_inspection_sign_ref":signs[0]["id"],
        "speaker_ref":earlier["heard_source_actor"],
        "hypothesis":"ATTEND_AGAIN_TO_OBJECT_PUBLICLY_REFERRED_TO_BY_OTHER",
        "no_lexical_understanding_or_inferred_private_intent":True,
        "grade":GRADE}]


def admit_cultural_reference(actor,experience,event_ref,proposal):
    possible=possible_cultural_object_inquiry(actor,experience,event_ref)
    if len(possible)!=1:raise ValueError("CULTURE_NO_INDEPENDENT_PRACTICED_REFERENCE")
    required=possible[0]
    for key in ("practice_ref","object_ref","demonstration_ref",
                "personal_inspection_sign_ref","speaker_ref","hypothesis"):
        if proposal.get(key)!=required[key]:
            raise ValueError("CULTURE_UNSOURCED_"+key)
    old=next(x for x in actor["cultural_demonstrations"]
             if x["id"]==required["demonstration_ref"])
    rec={"id":required["practice_ref"],"actor":actor["id"],
         "object_ref":required["object_ref"],
         "particular_speaker_ref":required["speaker_ref"],
         "source_demonstration_ref":old["id"],
         "source_investigation_ref":required["personal_inspection_sign_ref"],
         "source_event_refs":[old["event_ref"],event_ref],
         "origin_clock":experience["clock"],
         "location":experience.get("location"),
         "status":ACQUIRED,"operation":"INSPECT",
         "function":"PERSONALLY_PRACTICED_FOLLOWING_OF_OTHER_PUBLIC_ATTENTION",
         "not_learning_any_specific_word":True,
         "not_assuming_speaker_was_teaching":True,
         "not_a_universal_cultural_fitness_score":True,
         "other_private_meaning_unavailable":True,
         "material_owner_not_transferred":True,
         "revisions":[],"grade":GRADE}
    actor.setdefault("cultural_reference_practices",[]).append(rec)
    return {"kind":proposal["kind"],"reference_ref":rec["id"],
            "status":"ACQUIRED_SOURCEFREE_SITUATED_REFERENCE_NOT_WORD",
            "grade":GRADE}


def cultural_object_alternatives(constitution,access,option):
    """One person's own exposure changes their next exact-object option."""
    if option.get("action")!="INSPECT" or "INSPECT" not in access.affordances:
        return []
    ok,_=eligible(constitution.body,"INSPECT")
    if not ok:return []
    available={c.get("material_object_ref") for c in access.cues
              if type(c) is dict and c.get("kind")=="material_object_present"}
    proposals=[]
    already=set()
    for record in reversed(getattr(constitution,
                                   "cultural_reference_practices",[])):
        obj=record.get("object_ref")
        if (record.get("status")!=ACQUIRED or
                obj in already or obj not in available or
                record.get("location")!=access.location):
            continue
        already.add(obj)
        proposals.append({
            "option_id":stable_id("culturally_acquired_object_inquiry",{
                "actor":constitution.actor,"clock":constitution.clock,
                "reference":record["id"]}),
            "actor":constitution.actor,"as_of_clock":constitution.clock,
            "operation":"INSPECT","project_id":None,
            "grounds_status":"ACTOR_ACQUIRED_SITUATED_CULTURAL_REFERENCE",
            "world_request":{"operation":"INSPECT",
                "material_object_ref":obj,"addressed_party_ref":None},
            "binding_status":"ACTUAL_PRESENT_OBJECT_NOT_SEMANTIC_MASTERY",
            "cultural_reference_ref":record["id"],
            "source_event_refs":copy(record["source_event_refs"]),
            "not_a_granted_property_right":True,
            "not_a_mindreading_claim":True,
            "grade":GRADE})
    for record in reversed(getattr(constitution,"cultural_demonstrations",[])):
        obj=record.get("object_ref")
        if obj in already or obj not in available or (
                record.get("location")!=access.location):
            continue
        already.add(obj)
        proposals.append({
            "option_id":stable_id("personally_heard_object_trial",{
                "actor":constitution.actor,"clock":constitution.clock,
                "demonstration":record["id"]}),
            "actor":constitution.actor,"as_of_clock":constitution.clock,
            "operation":"INSPECT","project_id":None,
            "grounds_status":"UNTESTED_PERSONALLY_HEARD_PUBLIC_OBJECT_REFERENCE",
            "world_request":{"operation":"INSPECT",
                "material_object_ref":obj,"addressed_party_ref":None},
            "binding_status":"OBJECT_PRESENT_NO_MEANING_YET_ACQUIRED",
            "source_demonstration_ref":record["id"],
            "speaker_private_intent":"UNKNOWN",
            "grade":GRADE})
    return proposals


def choose_culturally_situated_object_inquiry(options):
    """No invisible preference slider: pick one warranted exact-object trial.

    Abstain on incompatible projects, active opposed current or several equally
    learned referents. This is a sourcefree fallback policy, not human science.
    """
    if any(o.get("project_courses")
           or o.get("psychodynamic_status")=="UNRESOLVED_CONTRADICTION"
           for o in options):
        return None
    alts=[a for o in options if o.get("action")=="INSPECT"
          for a in o.get("practical_alternatives",[])
          if a.get("grounds_status") in (
              "ACTOR_ACQUIRED_SITUATED_CULTURAL_REFERENCE",
              "UNTESTED_PERSONALLY_HEARD_PUBLIC_OBJECT_REFERENCE")]
    strong=[a for a in alts if a["grounds_status"]==(
        "ACTOR_ACQUIRED_SITUATED_CULTURAL_REFERENCE")]
    eligible_set=strong if strong else alts
    if len(eligible_set)!=1:return None
    return {
        "action":"INSPECT",
        "practical_option_id":eligible_set[0]["option_id"],
        "sourcefree_policy":"PARTICULAR_ACTOR_HISTORY_GUIDES_INQUIRY",
        "speaker_does_not_select_childs_action":True,
        "not_an_inferred_conscious_intention":True}


def possible_reference_revision(actor,experience,event_ref):
    """Material frustration changes practice without denying the past."""
    if experience.get("actor")!=actor.get("id") or (
            experience.get("own_action")!="INSPECT" or
            experience.get("status")!="PARTIAL" or
            (experience.get("felt_enactment") or {}).get(
                "attempted_operation")!="INSPECT"):
        return []
    # An incomplete INSPECT is NOT automatically an object-specific failure.
    # Require the actor's independently frozen exact-object practical choice.
    choice=experience.get("own_practical_selection") or {}
    if choice.get("world_request",{}).get("operation")!="INSPECT":
        return []
    obj=choice.get("world_request",{}).get("material_object_ref")
    refs=[r for r in actor.get("cultural_reference_practices",[])
          if r.get("object_ref")==obj and r.get("status")==ACQUIRED]
    if len(refs)!=1:return []
    return [{"kind":"REVISE_SITUATED_CULTURAL_REFERENCE",
             "practice_ref":refs[0]["id"],
             "source_failed_attempt_event":event_ref,
             "status":"SUSPEND_AFTER_PERSONALLY_FAILED_INQUIRY",
             "does_not_prove_false_word_meaning":True,"grade":GRADE}]


def admit_reference_revision(actor,experience,event_ref,proposal):
    cands=possible_reference_revision(actor,experience,event_ref)
    if len(cands)!=1 or any(proposal.get(k)!=cands[0][k]
                           for k in ("practice_ref",
                                     "source_failed_attempt_event","status")):
        raise ValueError("CULTURE_REVISION_UNQUALIFIED")
    record=next(r for r in actor["cultural_reference_practices"]
                if r["id"]==cands[0]["practice_ref"])
    record["revisions"].append({"event_ref":event_ref,
         "prior_status":record["status"],"next_status":SUSPENDED,
         "experience_ref":experience["ref"],
         "not_a_refutation_of_other_person_intent":True,
         "grade":GRADE})
    record["status"]=SUSPENDED
    return {"kind":proposal["kind"],"reference_ref":record["id"],
            "status":"SUSPENDED_BY_ACTOR_FAILED_INQUIRY_NOT_FALSE_MEANING",
            "grade":GRADE}


def qualified_exercised_cultural_sources(actor_id, clock, practices, demos, encounters):
    """Common historical qualification for R55 formation and R56 recruitment.

    A source is an admitted cultural reference with its own earlier heard
    demonstration and actual investigation, not a recalled proposition.
    No assertion that an analyst's historical relation is the actor's concept.
    """
    for practice in practices:
        acquired=practice.get('origin_clock')
        old=practice.get('object_ref')
        events=practice.get('source_event_refs',[])
        if (practice.get('actor')!=actor_id or practice.get('status')!=ACQUIRED
                or type(old) is not str or type(acquired) is not int
                or acquired>=clock or len(events)!=2 or len(set(events))!=2):
            continue
        source=[d for d in demos if d.get('id')==practice.get('source_demonstration_ref')
                and d.get('actor')==actor_id and d.get('object_ref')==old
                and d.get('event_ref')==events[0]
                and d.get('heard_source_actor')==practice.get('particular_speaker_ref')
                and type(d.get('clock')) is int and d['clock']<acquired]
        exercised=[e for e in encounters if e.get('actor')==actor_id
                   and e.get('event_ref')==events[1]
                   and e.get('material_object_ref')==old
                   and e.get('perceived_cue_ref')==practice.get('source_investigation_ref')
                   and e.get('personally_attempted_operation')=='INSPECT']
        if len(source)==len(exercised)==1:
            yield practice,source[0],exercised[0]


def recruit_cross_object_attention(constitution,access):
    """An exercised social way of attending can mediate a NEW material thing.

    A current accessible sign of that particular Other actually making a
    different visible object can recruit a former way of attending. This is
    a provisional contextual transfer, not semantic equivalence, inferred
    teaching intention, recognition of ownership, or a new acquired end.
    One bounded focal nomination; retain actual sign and source identities.
    """
    if constitution.actor!=access.actor:
        raise ValueError('CULTURE_ATTENTION_FOREIGN_ACTOR')
    if ('INSPECT' not in access.affordances
            or not eligible(constitution.body,'INSPECT')[0]):
        return []
    present={c.get('material_object_ref'):c for c in access.cues
             if c.get('kind')=='material_object_present'
             and c.get('location')==access.location
             and c.get('clock')==access.world_clock}
    signs=[c for c in access.cues
           if c.get('kind')=='performed_make_object'
           and c.get('modality')=='visual'
           and c.get('clock')==access.world_clock
           and c.get('location')==access.location
           and c.get('material_object_ref') in present
           and type(c.get('source_actor')) is str
           and c['source_actor']!=constitution.actor]
    if not signs:return []
    sources=list(qualified_exercised_cultural_sources(
        constitution.actor,constitution.clock,
        constitution.cultural_reference_practices,
        constitution.cultural_demonstrations,constitution.object_encounters))
    out=[]
    for practice,demo,exercised in sources:
        for sign in signs:
            obj=sign['material_object_ref']
            if (obj==practice['object_ref']
                    or sign['source_actor']!=demo['heard_source_actor']):
                continue
            # Do not grant a novel orientation after the actor has already
            # independently investigated this particular object. Mere prior
            # passive reception of its making is not a completed inquiry.
            if any(e.get('actor')==constitution.actor
                   and e.get('material_object_ref')==obj
                   and e.get('source_kind')=='performed_inspect'
                   and e.get('personally_attempted_operation')=='INSPECT'
                   for e in constitution.object_encounters):
                continue
            basis={'actor':constitution.actor,'as_of_clock':access.world_clock,
                   'location':access.location,'source_practice_ref':practice['id'],
                   'source_demonstration_ref':demo['id'],
                   'source_exercised_encounter_ref':exercised['id'],
                   'earlier_material_object_ref':practice['object_ref'],
                   'new_material_object_ref':obj,
                   'current_making_sign_ref':sign['id'],
                   'current_visible_object_cue_ref':present[obj]['id'],
                   'particular_other_ref':sign['source_actor']}
            out.append({**basis,
                'recruitment_ref':stable_id('cross_object_attention',basis),
                'kind':'ACQUIRED_SOCIAL_ATTENTION_RECRUITED_ACROSS_OBJECTS',
                'not_a_conscious_analogy_or_motive':True,
                'not_actual_attention_or_material_permission':True,
                'grade':GRADE})
    # Ambiguity remains a real limitation; pick a bounded historically
    # qualified occasion, without a numeric strength or ranking of desires.
    return sorted(out,key=lambda x:(x['current_making_sign_ref'],
                                    x['source_practice_ref']))[:1]
