"""R4: historical relation-of-relation metabolism, derived from the actor's iceberg.

A sourcefree PRE-A0 Personal Relational Field *consumer*, NOT a new native
psychological store, unconscious truth oracle, or clinical model. It projects
already admitted relations and motifs into current recruitment and action.
The actor does not manage this machinery consciously; the semantic renderer
must not acquire these private currents as self-knowledge.
"""
from __future__ import annotations

from .types import GRADE, copy, stable_id
from .organism import ACTIONS

# PRE-A0's historically specified relation families, not a universal force scale.
RELATIONS = frozenset({
    "RECRUITS", "SUPPORTS", "INHIBITS", "COMPETES", "CONTRADICTS", "DERIVED_FROM",
    "REINFORCES", "LICENSES", "JUSTIFIES", "SUBORDINATES", "SUPPRESSES",
    "COMPENSATES_FOR", "RATIONALIZES", "INTERPRETS_THROUGH", "CONFLICTS_WITH",
    "QUARANTINES_FROM", "ACTIVATES", "INSTRUMENTALIZES",
    "MUTUALLY_REINFORCES", "MUTUALLY_CONSTRAINS", "REVALUES",
})
# Motifs are *acquired configurations* of previously acquired actor forms.
# They may route possible action or interpret the significance of a relation.
# They do not invent new action opcodes, facts about other minds, or world power.
EFFECTS = frozenset({"ACTION_CURRENT", "RELATION_MEDIATION", "RECRUIT_FORM"})
POLARITIES = frozenset({"APPROACH", "WITHHOLD"})


class InvalidRelationalMotif(ValueError):
    pass


def link_ref(link):
    """Stable identification of an admitted relation even for inherited R3 edges.

    Historical revisions keep the ID; content-changing links without an ID
    retain a deterministic endpoint/relation identity on first admission.
    """
    return link.get("id") or stable_id("psychic_relation", {
        "source": link["source"], "target": link["target"],
        "relation": link["relation"], "origin": link.get("origin", []),
    })


def validate_motif(motif, forms):
    """Reject psychological free variables and unconstrained model programs."""
    if not isinstance(motif, dict):
        raise InvalidRelationalMotif("INVALID_MOTIF")
    sources = motif.get("source_forms")
    if (type(sources) is not list or not 2 <= len(sources) <= 4
            or any(type(x) is not str or x not in forms for x in sources)
            or len(set(sources)) != len(sources)):
        raise InvalidRelationalMotif("MOTIF_REQUIRES_TWO_TO_FOUR_ACQUIRED_FORMS")
    if any(not forms[x].get("origin") for x in sources):
        raise InvalidRelationalMotif("MOTIF_REQUIRES_ACTUAL_FORM_ANCESTRY")
    # An actor-specific historical relation to an identifiable Other may
    # require an actually *received event* from that Other, not mere
    # co-presence, a generic label or an analyst's claim of authority.
    witness = motif.get("witnessed_source_actor_ref")
    if witness is not None and (type(witness) is not str or not witness.strip()):
        raise InvalidRelationalMotif("INVALID_MOTIF_WITNESSED_SOURCE_ACTOR")
    cues = motif.get("cue_terms", [])
    locations = motif.get("locations", [])
    if (type(cues) is not list or type(locations) is not list
            or len(cues) > 20 or len(locations) > 12
            or any(type(s) is not str or not s for s in cues + locations)):
        raise InvalidRelationalMotif("INVALID_MOTIF_CONTEXT")
    effects = motif.get("effects", [])
    if type(effects) is not list or not 1 <= len(effects) <= 8:
        raise InvalidRelationalMotif("MOTIF_REQUIRES_BOUNDED_EFFECTS")
    for effect in effects:
        if not isinstance(effect, dict) or effect.get("kind") not in EFFECTS:
            raise InvalidRelationalMotif("INVALID_MOTIF_EFFECT")
        if effect["kind"] == "ACTION_CURRENT":
            if (effect.get("action") not in ACTIONS
                    or effect.get("polarity") not in POLARITIES):
                raise InvalidRelationalMotif("MOTIF_ACTION_NOT_QUALIFIED")
        elif effect["kind"] == "RELATION_MEDIATION":
            if (effect.get("source") not in sources or
                    effect.get("target") not in sources or
                    effect["source"] == effect["target"] or
                    effect.get("relation") not in RELATIONS):
                raise InvalidRelationalMotif("MOTIF_RELATION_NOT_QUALIFIED")
            # A learned relation can *also* carry an operative transduction,
            # but only into an ability already acquired by its TARGET form.
            # No learned theology/ideology may conjure a world permission,
            # physical operation, agency of another person, or fixed morality.
            if ("mediated_action" in effect or "polarity" in effect):
                target = forms[effect["target"]]
                action = effect.get("mediated_action")
                enables = target.get("enables", [])
                if (type(action) is not str or action not in ACTIONS
                        or type(enables) is not list or action not in enables
                        or effect.get("polarity") not in POLARITIES):
                    raise InvalidRelationalMotif(
                        "MOTIF_MEDIATED_ACTION_NOT_ACQUIRED_BY_TARGET")
        else:
            # A historical configuration can recruit an *already acquired*
            # third form across cues; it cannot invent the target, bypass its
            # organismic scope, or override an independently admitted veto.
            target = effect.get("target_form")
            if (type(target) is not str or target not in forms
                    or target in sources or not forms[target].get("origin")):
                raise InvalidRelationalMotif("MOTIF_RECRUITMENT_TARGET_UNQUALIFIED")
    if motif.get("status", "ACTIVE") not in ("ACTIVE", "DORMANT"):
        raise InvalidRelationalMotif("INVALID_MOTIF_STATUS")
    return True


def _tokens(access):
    return {str(v).lower() for c in access.cues
            for v in c.get("tags", []) + [c.get("kind", "")]}


def _in_context(qualified, access, cues):
    return ((not qualified.get("contexts")
             or access.location in qualified["contexts"])
            and (not qualified.get("locations")
                 or access.location in qualified["locations"])
            and (not qualified.get("cue_terms")
                 or bool({str(x).lower() for x in qualified["cue_terms"]} & cues)))


def derive_relational_metabolism(constitution, access, active_forms, inhibited):
    """Pure, context-bounded person×event relation projection.

    An *inhibited* form may still shape another current through a historically
    admitted relation, but is never thereby restored to direct action/ability.
    A motif with two source forms fires only when both are situatedly reached
    and at least one remains active. Its effects remain private, provisional,
    and tied to a real actor-specific historical ancestor.
    """
    forms = constitution.forms
    active = set(active_forms)
    blocked = set(inhibited) & set(forms)
    situated = active | blocked
    cues = _tokens(access)
    currents = []
    action_currents = []
    recruitment_candidates = []
    readset = set()
    for link in constitution.links:
        if (link.get("source") not in situated
                or link.get("target") not in situated
                or not _in_context(link, access, cues)):
            continue
        relation = link.get("relation")
        if relation not in RELATIONS:
            continue
        lid = link_ref(link)
        both_direct = link["source"] in active and link["target"] in active
        currents.append({
            "kind": ("OPERATIVE_RELATION" if both_direct
                     else "INDIRECT_INHIBITED_RELATION"),
            "relation_ref": lid,
            "relation": relation,
            "source_form_ref": link["source"],
            "target_form_ref": link["target"],
            "source_directly_recruited": link["source"] in active,
            "target_directly_recruited": link["target"] in active,
            "actor_access": "NONCONSCIOUS_POSSIBLE_NOT_PROVEN",
            "not_an_objective_world_fact": True,
            "grade": GRADE,
        })
        readset.add(lid)

    for motif in getattr(constitution, "relational_motifs", []):
        validate_motif(motif, forms)
        if motif.get("status", "ACTIVE") != "ACTIVE":
            continue
        if not _in_context(motif, access, cues):
            continue
        witnessed_actor = motif.get("witnessed_source_actor_ref")
        if witnessed_actor is not None and not any(
                cue.get("source_actor") == witnessed_actor
                and cue.get("kind") not in (
                    "coactor_present", "material_object_present",
                    "public_notice_visible")
                for cue in access.cues):
            continue
        sources = set(motif["source_forms"])
        if not sources <= situated or not sources & active:
            continue
        mid = motif["id"]
        readset.add(mid)
        currents.append({
            "kind": "ACQUIRED_RELATIONAL_CONFIGURATION",
            "motif_ref": mid,
            "source_form_refs": sorted(sources),
            "inhibited_source_refs": sorted(sources & blocked),
            "origin": copy(motif.get("origin", [])),
            "not_a_self_known_reason": True,
            "grade": GRADE,
        })
        for effect in motif["effects"]:
            if effect["kind"] == "ACTION_CURRENT":
                action_currents.append({
                    "action": effect["action"],
                    "polarity": effect["polarity"],
                    "motif_ref": mid,
                    "source_form_refs": sorted(sources),
                    "has_inhibited_source": bool(sources & blocked),
                })
            elif effect["kind"] == "RECRUIT_FORM":
                recruitment_candidates.append({
                    "target_form": effect["target_form"],
                    "motif_ref": mid,
                    "source_form_refs": sorted(sources),
                    "suppressed_source_refs": sorted(sources & blocked),
                    "qualification": "SITUATED_ACQUIRED_ASSOCIATIVE_RECRUITMENT",
                    "grade": GRADE,
                })
            else:
                # Relational mediation is not merely a diagnostic label.
                # A historically acquired way of interpreting care through
                # institutional discipline, for example, can make an
                # *already acquired* practical operation newly attractive
                # or aversive. The source may remain inhibited; the TARGET
                # must remain directly recruited, not be resurrected.
                operative = "mediated_action" in effect
                target_direct = effect["target"] in active
                currents.append({
                    "kind": "ACQUIRED_PERSONAL_SENSE_MEDIATION",
                    "motif_ref": mid,
                    "source_form_ref": effect["source"],
                    "target_form_ref": effect["target"],
                    "relation": effect["relation"],
                    "has_inhibited_source": effect["source"] in blocked,
                    "target_directly_recruited": target_direct,
                    "operative_mediation": operative and target_direct,
                    "not_objective_justification_of_conduct": True,
                    "no_automatic_motive_fulfillment": True,
                    "grade": GRADE,
                })
                if operative and target_direct:
                    action_currents.append({
                        "action": effect["mediated_action"],
                        "polarity": effect["polarity"],
                        "motif_ref": mid,
                        "source_form_refs": sorted(sources),
                        "has_inhibited_source": bool(sources & blocked),
                        "mode": "HISTORICALLY_ACQUIRED_RELATION_TRANSDUCTION",
                        "mediation_relation": effect["relation"],
                        "mediation_source_ref": effect["source"],
                        "mediation_target_ref": effect["target"],
                        "not_actor_self_account": True,
                        "not_objective_justification_of_conduct": True,
                    })
    return {
        "currents": currents,
        "action_currents": action_currents,
        "recruitment_candidates": recruitment_candidates,
        "readset": sorted(readset),
        "grade": GRADE,
        "not_a_clinical_unconscious_etiology": True,
    }


def admit_motif(actor, candidate, event_ref, experience, index):
    """Prepare one bounded, actor-owned fictional motif for atomic admission."""
    motif = copy(candidate.get("motif", {}))
    validate_motif(motif, actor["forms"])
    witness = motif.get("witnessed_source_actor_ref")
    # A semantic proposal cannot manufacture having recognized or actually
    # received a particular person's act. This sourcefree witness requirement
    # applies at acquisition, not only later during recruitment.
    if witness is not None and not any(
            isinstance(cue, dict) and cue.get("source_actor") == witness
            for cue in experience.get("perceived_cues", [])):
        raise InvalidRelationalMotif("MOTIF_WITNESSED_OTHER_NOT_RECEIVED")
    if (not experience.get("participated")
            and not experience.get("perceived_cues")):
        raise InvalidRelationalMotif("MOTIF_HAS_NO_ACTOR_EXPERIENCE")
    if len(actor.get("relational_motifs", [])) >= 256:
        raise InvalidRelationalMotif("MOTIF_STORAGE_BUDGET")
    # The proposal must not acquire an unrecognized social authority or an
    # objective event; all referenced forms are existing actor-owned history.
    motif["id"] = stable_id("relational_motif", {
        "actor": actor["id"], "event": event_ref, "index": index,
        "sources": sorted(motif["source_forms"]), "effects": motif["effects"],
    })
    if any(x.get("id") == motif["id"] for x in actor.get("relational_motifs", [])):
        raise InvalidRelationalMotif("DUPLICATE_RELATIONAL_MOTIF")
    motif["origin"] = [event_ref]
    motif["experience_ref"] = experience["ref"]
    motif["grade"] = GRADE
    motif["status"] = "ACTIVE"
    motif["not_a_validated_unconscious_explanation"] = True
    motif.setdefault("cue_terms", [])
    motif.setdefault("locations", [])
    return motif


def possible_witnessed_third_party_relation(actor, experience):
    """A third person may revalue a relation they actually witnessed.

    The objective source/target and performed act come from the world-owned
    public sign, subsequently gated by this actor's own sensory access.
    Earlier other-models are ONLY this actor's provisional hypotheses.
    The candidate never alters a relation, invents another's motive, or makes
    an unseen household event into actor memory. A model may propose NO_CHANGE.
    """
    if experience.get('actor')!=actor.get('id'):
        return []
    previous=actor.get('other_models',{})
    if type(previous) is not dict:
        return []
    candidates=[]
    for cue in experience.get('perceived_cues',[]):
        if type(cue) is not dict:
            continue
        kind=cue.get('kind')
        source=cue.get('source_actor')
        target=cue.get('actor_accessible_target_ref')
        if (kind not in ('performed_care','performed_feed','performed_impose')
                or cue.get('public_person_directed_act_not_private_intention') is not True
                or type(cue.get('id')) is not str
                or type(source) is not str or type(target) is not str
                or source==target or actor['id'] in (source,target)):
            continue
        old_source=previous.get(source,[])
        old_target=previous.get(target,[])
        candidates.append({
            'kind':'WITNESSED_THIRD_PARTY_RELATION_OCCASION',
            'actor':actor['id'],'source_actor_ref':source,
            'target_actor_ref':target,'witnessed_act':kind.removeprefix('performed_').upper(),
            'witnessed_cue_ref':cue['id'],
            'prior_source_models_actor_hypotheses_only':copy(
                old_source[-3:] if type(old_source) is list else []),
            'prior_target_models_actor_hypotheses_only':copy(
                old_target[-3:] if type(old_target) is list else []),
            'no_mandatory_revaluation':True,
            'no_private_other_psychology_or_consent_inferred':True,
            'grade':GRADE})
    return candidates[:4]
