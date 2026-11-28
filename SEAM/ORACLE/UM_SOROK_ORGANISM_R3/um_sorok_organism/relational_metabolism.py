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
    partitions=quarantine_pairs(constitution.links,access.location)
    for link in situated_relation_links(constitution.links,access.location):
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
        for effect_index, effect in enumerate(motif["effects"]):
            if effect["kind"] == "ACTION_CURRENT":
                action_currents.append({
                    "action": effect["action"],
                    "polarity": effect["polarity"],
                    "motif_ref": mid,
                    "source_form_refs": sorted(sources),
                    "has_inhibited_source": bool(sources & blocked),
                })
            elif effect["kind"] == "RECRUIT_FORM":
                if any((source,effect['target_form']) in partitions for source in sources):
                    continue
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
                    latest=(motif.get("motif_history") or [{}])[-1]
                    bridge=latest.get("lived_cross_context_basis",{})
                    provenance=({"lived_cross_context_revaluation": {
                        "historical_orientation_ref":bridge["historical_orientation_ref"],
                        "earlier_location":bridge["earlier_location"],
                        "later_location":bridge["later_location"],
                        "revaluation_event":latest["event"],
                        "not_actor_self_knowledge":True}}
                        if bridge.get("effect_index")==effect_index else {})
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
                        **provenance,
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
    refuse_unissued_cross_context_history(motif)
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

def refuse_unissued_cross_context_history(motif):
    """The R32 provenance key is owned by later typed reorganization only."""
    if type(motif) is dict and any(
            type(row) is dict and 'lived_cross_context_basis' in row
            for row in (motif.get('motif_history') or [])):
        raise InvalidRelationalMotif('CROSS_CONTEXT_UNISSUED_HISTORY')


def possible_lived_cross_context_revaluations(actor, experience, event_ref):
    """Optional reorganization of an OLD motif through a different lived site.

    A narrow provisional bridge: the same personally enacted operation occurs
    in two material settings, but its relational significance need not be the
    same. R28-R31 supply the earlier acquired orientation and actual episodes;
    R4/R23 supply the existing motif and its acquired means. The semantic
    owner, not a valence conversion rule, proposes how the relation changes.
    No orientation is copied into the new setting or declared conscious.
    """
    aid=actor.get('id')
    clock=experience.get('clock')
    operation=experience.get('own_action')
    site=experience.get('location')
    if (experience.get('actor')!=aid or type(clock) is not int
            or type(event_ref) is not str or not event_ref
            or type(site) is not str or not site or site!=actor.get('location')
            or type(operation) is not str or operation not in ACTIONS
            or not actor.get('relational_motifs')
            or experience.get('participated') is not True
            or (experience.get('felt_enactment') or {}).get(
                'attempted_operation')!=operation):
        return []
    signs=[c for c in experience.get('perceived_cues',[])
           if type(c) is dict]
    # The shared operation must be personally received, not an ambient
    # co-presence or analyst-supplied abstract similarity.
    kind='performed_'+operation.lower()
    received=[c for c in signs if c.get('kind')==kind
              and c.get('source_actor')==aid and type(c.get('id')) is str]
    if len(received)!=1:
        return []
    sign=received[0]
    episodes=actor.get('lived_genesis_episodes',[])
    now=[w for w in episodes if w.get('actor')==aid
         and w.get('event_ref')==event_ref
         and w.get('experience_ref')==experience.get('ref')
         and w.get('clock')==clock and w.get('location')==site
         and w.get('actor_felt_attempt')==operation
         and sign['id'] in w.get('received_sign_refs',[])]
    if len(now)!=1:
        return []
    current=now[0]
    # At least a personally lived bodily difference or incomplete operation
    # is required; mere repetition of a word cannot revalue a relation.
    if not (current.get('received_relief')
            or current.get('personally_lived_adverse_course')
            or current.get('unfinished_own_activity')):
        return []
    sources=[]
    by_id={w.get('id'):w for w in episodes if w.get('actor')==aid}
    for row in actor.get('historical_orientations',[])[-128:]:
        if (row.get('actor')!=aid or row.get('acquisition')!=
                'REPEATED_LIVED_BODY_COURSE'
                or row.get('operation')!=operation
                or row.get('location')==site
                or type(row.get('origin_clock')) is not int
                or row['origin_clock']>=clock
                or type(row.get('id')) is not str):
            continue
        basis=row.get('lived_genesis_basis',{})
        witnesses=[by_id.get(basis.get(k)) for k in (
            'first_lived_episode_ref','later_lived_episode_ref')]
        if any(w is None for w in witnesses):
            continue
        if (witnesses[0]['id']==witnesses[1]['id']
                or [w.get('event_ref') for w in witnesses]!=basis.get('source_event_refs')
                or [w.get('experience_ref') for w in witnesses]!=basis.get('source_experience_refs')
                or any(w.get('event_ref')==event_ref
                       or w.get('location')!=row['location']
                       or w.get('actor_felt_attempt')!=operation
                       or type(w.get('clock')) is not int
                       or w['clock']>=clock
                       or not any(c.get('kind')==kind and c.get('source_actor')==aid
                                  for c in w.get('personally_perceived_sign_sources',[]))
                       for w in witnesses)
                or witnesses[0]['clock']>=witnesses[1]['clock']
                or witnesses[1]['event_ref']!=row.get('origin_event')
                or witnesses[1]['clock']!=row['origin_clock']):
            continue
        sources.append((row,witnesses))
    candidates=[]
    terms={str(v).lower() for c in signs
           for v in c.get('tags',[])+[c.get('kind','')]}
    forms=actor.get('forms',{})
    for motif in actor.get('relational_motifs',[]):
        if (motif.get('status','ACTIVE')!='ACTIVE'
                or not motif.get('origin') or event_ref in motif['origin']
                or any(h.get('event')==event_ref for h in motif.get('motif_history',[]))
                or (motif.get('locations') and site not in motif['locations'])
                or (motif.get('cue_terms') and not
                    terms.intersection(t.lower() for t in motif['cue_terms']))):
            continue
        witness=motif.get('witnessed_source_actor_ref')
        if witness is not None and not any(
                c.get('source_actor')==witness and c.get('kind') not in
                ('coactor_present','material_object_present','public_notice_visible')
                for c in signs):
            continue
        validate_motif(motif,forms)
        if any(forms[f].get('actor')!=aid or
               event_ref in forms[f].get('origin',[])
               for f in motif['source_forms']):
            continue
        for i,effect in enumerate(motif['effects']):
            if (effect.get('kind')!='RELATION_MEDIATION'
                    or effect.get('mediated_action')!=operation):
                continue
            for row,witnesses in sources:
                # This is an optional historical connection, not proof of
                # similarity of goods, an obligation to heal, or a motive.
                candidates.append({
                    'kind':'REORGANIZE_RELATIONAL_MOTIF',
                    'motif_id':motif['id'],
                    'lived_cross_context_basis':{
                        'historical_orientation_ref':row['id'],
                        'earlier_location':row['location'],
                        'later_location':site,
                        'earlier_orientation_mode':row['orientation_mode'],
                        'earlier_episode_refs':[w['id'] for w in witnesses],
                        'earlier_event_refs':[w['event_ref'] for w in witnesses],
                        'later_episode_ref':current['id'],
                        'later_event_ref':event_ref,
                        'later_experience_ref':experience['ref'],
                        'later_received_sign_ref':sign['id'],
                        'shared_enacted_operation':operation,
                        'effect_index':i,
                        'previous_effect':copy(effect),
                        'not_proof_of_functional_equivalence_or_causation':True,
                    },
                    'semantic_choice_required':{
                        'new_relation':sorted(RELATIONS),
                        'new_polarity':sorted(POLARITIES),
                        'or_no_change':True},
                    'grade':GRADE,
                })
                if len(candidates)>=12:
                    return candidates
    return candidates


def qualify_lived_cross_context_revaluation(actor, experience, event_ref, candidate):
    """Recompute the occasion; revise just one existing effect, never a form.

    The model can choose either polarity and any existing relation family;
    no change remains possible by abstaining. Context, action, endpoints,
    witnesses and all other effects are conserved by the existing motif owner.
    """
    permitted={'kind','motif_id','lived_cross_context_basis','new_relation',
               'new_polarity','interpretive_hypothesis'}
    if set(candidate)-permitted:
        raise InvalidRelationalMotif('CROSS_CONTEXT_UNQUALIFIED_REWRITE')
    matches=[p for p in possible_lived_cross_context_revaluations(
        actor,experience,event_ref) if p['motif_id']==candidate.get('motif_id')
        and p['lived_cross_context_basis']==candidate.get('lived_cross_context_basis')]
    if len(matches)!=1:
        raise InvalidRelationalMotif('CROSS_CONTEXT_NO_ACTOR_LIVED_BRIDGE')
    basis=copy(matches[0]['lived_cross_context_basis'])
    relation=candidate.get('new_relation')
    polarity=candidate.get('new_polarity')
    if (type(relation) is not str or relation not in RELATIONS
            or type(polarity) is not str or polarity not in POLARITIES):
        raise InvalidRelationalMotif('CROSS_CONTEXT_INVALID_SEMANTIC_CHOICE')
    hypothesis=candidate.get('interpretive_hypothesis')
    if hypothesis is not None and (type(hypothesis) is not str
            or not hypothesis.strip() or len(hypothesis)>512):
        raise InvalidRelationalMotif('CROSS_CONTEXT_INVALID_HYPOTHESIS')
    motif=next(m for m in actor['relational_motifs']
               if m['id']==candidate['motif_id'])
    effects=copy(motif['effects'])
    effect=effects[basis['effect_index']]
    if (effect['relation'],effect['polarity'])==(relation,polarity):
        raise InvalidRelationalMotif('CROSS_CONTEXT_NO_RELATIONAL_CHANGE')
    effect.update({'relation':relation,'polarity':polarity})
    basis['interpretive_hypothesis_not_causal_truth']=hypothesis
    basis['new_relation']=relation
    basis['new_polarity']=polarity
    return basis,effects



def situated_relation_links(links,location):
    """A later revaluation can be local; do not overwrite the old relation
    in every other activity field. The historical link retains its identity."""
    result=[]
    for link in links:
        rows=[x for x in link.get('contextual_revaluations',[])
              if x.get('location')==location]
        if rows:
            row=rows[-1]
            projected=copy(link);projected['relation']=row['new_relation']
            projected['contextual_revaluation_event_ref']=row['event_ref']
            result.append(projected)
        else:result.append(link)
    return result


def quarantine_pairs(links,location):
    """A contextual partition stops this associative route, not the target
    form itself, its other routes, its direct sensory recruitment or action."""
    return {(x['source'],x['target']) for x in situated_relation_links(links,location)
            if x.get('relation')=='QUARANTINES_FROM'
            and (not x.get('contexts') or location in x['contexts'])}


def possible_care_authority_revaluations(actor,experience,event_ref):
    """Connect separately lived care and thwarted material activity through
    an actual later reception of the care recipient exercising power.

    No claim that the observed power caused the earlier blocked feeding.
    The proposed relation is between the actor's already acquired forms.
    """
    from .care_commitment_genesis import lived_care_authority_encounters
    aid=actor['id'];paths=actor.get('evidence_paths',[]);forms=actor.get('forms',{})
    out=[]
    for b in lived_care_authority_encounters(actor,experience,event_ref):
        site=b['location'];clock=b['clock']
        blocked=[x for x in actor.get('material_dependency_encounters',[])
                 if x.get('actor')==aid and x.get('location')==site
                 and x.get('own_operation_attempted')=='FEED'
                 and type(x.get('clock')) is int and x['clock']<clock
                 and any(p.get('event')==x.get('event_ref')
                         and p.get('experience_ref')==x.get('experience_ref')
                         and p.get('own_action')=='FEED'
                         and x.get('received_nonperformance_sign_ref') in p.get('received_cue_refs',[])
                         for p in paths)]
        for link in actor.get('links',[]):
            if (link.get('relation') not in RELATIONS
                    or link.get('source')==link.get('target')
                    or link.get('source') not in forms or link.get('target') not in forms
                    or (link.get('contexts') and site not in link['contexts'])
                    or not link.get('origin') or event_ref in link['origin']
                    or not any(p.get('event') in link['origin'] for p in paths)
                    or any(x.get('event_ref')==event_ref for x in link.get('contextual_revaluations',[]))):
                continue
            fs=[forms[link['source']],forms[link['target']]]
            if any(f.get('actor')!=aid or not f.get('origin') or event_ref in f['origin']
                   or not any(p.get('event') in f['origin']
                              and p.get('experience_ref')==f.get('evidence',{}).get('experience_ref')
                              for p in paths) for f in fs):continue
            for i in (0,1):
                caring,frustrated=fs[i],fs[1-i]
                if not set(caring['origin']).intersection(b['earlier_care_event_refs']):continue
                matches=[x for x in blocked if x['event_ref'] in frustrated['origin']]
                if len(matches)!=1:continue
                current=situated_relation_links([link],site)[0]['relation']
                basis={'care_authority_encounter':copy(b),'relation_ref':link_ref(link),
                       'caring_form_ref':caring['id'],'material_frustration_form_ref':frustrated['id'],
                       'earlier_blocked_feeding_ref':matches[0]['id'],
                       'earlier_blocked_event_ref':matches[0]['event_ref'],
                       'previous_situated_relation':current,'location':site,
                       'not_a_proven_institutional_causal_explanation':True}
                out.append({'kind':'REVALUE_RELATION','relation_id':link_ref(link),
                            'lived_care_authority_basis':basis,
                            'new_relation_choices':sorted(RELATIONS-{current}),
                            'semantic_hypothesis_required_or_abstain':True})
                if len(out)>=12:return out
    return out


def qualify_care_authority_revaluation(actor,experience,event_ref,candidate):
    allowed={'kind','relation_id','lived_care_authority_basis','new_relation','interpretive_hypothesis'}
    if set(candidate)!=allowed:
        raise InvalidRelationalMotif('CARE_AUTHORITY_RELATION_UNQUALIFIED_FIELDS')
    h=candidate['interpretive_hypothesis']
    rows=[x for x in possible_care_authority_revaluations(actor,experience,event_ref)
          if x['relation_id']==candidate['relation_id']
          and x['lived_care_authority_basis']==candidate['lived_care_authority_basis']
          and candidate['new_relation'] in x['new_relation_choices']]
    if len(rows)!=1 or type(h) is not str or not 1<=len(h.strip())<=512:
        raise InvalidRelationalMotif('CARE_AUTHORITY_RELATION_UNQUALIFIED_HISTORY')
    b=copy(rows[0]['lived_care_authority_basis'])
    return {'event_ref':event_ref,'experience_ref':experience['ref'],
            'location':b['location'],'previous_relation':b['previous_situated_relation'],
            'new_relation':candidate['new_relation'],'basis':b,
            'interpretive_hypothesis_not_causal_truth':h.strip(),'grade':GRADE}
