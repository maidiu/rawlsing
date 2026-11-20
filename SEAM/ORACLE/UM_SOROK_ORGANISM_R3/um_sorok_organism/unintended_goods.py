"""SORACLE R13 — previously unintended consequences may become possible ends.

An actor's activity can produce a personally accessible consequence which the
actor never tried to produce. A model may identify that consequence as *possibly
worth exploring* on a later occasion. That nomination is NOT an established
motive, conscious claim, objectively successful purpose, or retrospective
reason for the original act.

This module attaches to the existing typed NOTICE_POSSIBLE_END operation and
R10 prospective_horizon first reader. The independent world must actually
settle the original act and produce a sign available to this actor; a topic
invented by a narrator is not a source. Particular material-object continuity
is by world object ref, not by importing the analyst's lexical category into
Nadia's preverbal mind.

No deterministic human learning law is claimed.
"""
from .types import GRADE, copy


def _source_received_signs(experience):
    return [c for c in experience.get('perceived_cues',[])
            if type(c) is dict and type(c.get('id')) is str
            and c.get('id') and type(c.get('modality','visual')) is str]


def possible_unintended_goods(actor, experience, practical_selection, event_ref):
    if actor.get('id')!=experience.get('actor') or not event_ref:
        raise ValueError('NEW_END_FOREIGN_ACTOR_OR_EVENT')
    felt=experience.get('felt_enactment') or {}
    operation=felt.get('attempted_operation')
    if not experience.get('participated') or not operation:
        return []
    signed=_source_received_signs(experience)
    if not signed:
        return []
    expected=(practical_selection or {}).get('anticipated_difference')
    anticipated_terms=set()
    if type(expected) is dict:
        anticipated_terms=set(t.casefold() for t in expected.get('sign_tags',[])
                          if type(t) is str)
    already={x.get('origin_material_object_ref') for x in
             actor.get('possible_ends',[])
             if type(x) is dict and x.get('origin_material_object_ref')}
    possible=[]
    for cue in signed:
        obj=cue.get('material_object_ref')
        if type(obj) is not str or not obj or obj in already:
            continue
        if operation not in ('MAKE_OBJECT','REPAIR','INSPECT','WORK'):
            continue
        # A sign carrying the actual object ID and the actor's own prior
        # practical history warrants a possible *new* object of activity. It
        # does not prove the person likes the object or recognizes its owner.
        sign_terms=set(t.casefold() for t in cue.get('tags',[])
                       if type(t) is str)
        if anticipated_terms and sign_terms & anticipated_terms:
            # This event may still surprise in other respects, but the
            # sourcefree shortcut cannot distinguish an unanticipated end.
            continue
        possible.append({
            'source_cue_ref':cue['id'],
            'world_material_object_ref':obj,
            'historical_action':operation,
            'origin_event_ref':event_ref,
            'original_practical_object':copy(
                (practical_selection or {}).get('anticipated_difference')),
            'candidate_future_activities':['INSPECT','REPAIR','ORIENT'],
            'actor_knows_object_identity':'NOT_INFERRED',
            'actor_conscious_valuation':'NOT_INFERRED',
            'meaning_alternatives':[
                'EXPLORE_FURTHER','AVOID_OR_WITHHOLD','NO_NEW_END',
                'NEITHER_CONSCIOUS_NOR_STABLE_YET'],
            'novel_consequence_qualified_by_lived_sign':True,
            'not_original_motive':True,
            'source_grade':GRADE,
        })
    return possible[:2]


def one_sourcefree_provisional_end(qualifications, actor):
    """No universal novelty drive: admit *at most one* material possibility.

    A live semantic provider can reject every candidate or propose another
    grounded interpretation. Fallback names only a future trial possibility;
    it cannot turn the source event into a settled 'desire' or direct a
    reflected reason at a preverbal actor.
    """
    if len(qualifications)!=1:
        return []
    q=qualifications[0]
    obj=q['world_material_object_ref']
    if any(e.get('origin_material_object_ref')==obj
           for e in actor.get('possible_ends',[])):
        return []
    return [{
        'kind':'NOTICE_POSSIBLE_END',
        'perceived_cue_ref':q['source_cue_ref'],
        'possible_object':'explore a further possibility with this encountered material thing',
        'possible_means':['INSPECT','REPAIR'],
        # For preverbal actors, strings are implementation discriminants,
        # never claims of already articulated human categories.
        'cue_terms':['material_object'],
        'origin_material_object_ref':obj,
        'not_a_preexisting_actor_goal':True,
        'not_the_event_original_purpose':True,
        'semantic_grade':'SOURCEFREE_PROVISIONAL_OBJECT_POSSIBILITY',
    }]
