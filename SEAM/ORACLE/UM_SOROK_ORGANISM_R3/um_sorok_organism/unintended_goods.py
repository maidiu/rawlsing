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
from .types import GRADE, copy, stable_id
from .cultural_mediation import qualified_exercised_cultural_sources


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
        # A stricter optional construction: a personally performed material
        # activity has an explicitly selected prior project and a received
        # sign outside its stated expected difference. This is novelty
        # relative to that expectation, not proof of unconscious intention.
        selection=practical_selection or {}
        project=selection.get('project_id')
        strict=(operation=='MAKE_OBJECT' and experience.get('status')=='PERFORMED'
                and cue.get('kind')=='performed_make_object'
                and type(project) is str and bool(anticipated_terms)
                and bool(sign_terms) and not (anticipated_terms & sign_terms))
        basis=({'id':stable_id('incidental_object_end',{
                    'actor':actor['id'],'event':event_ref,'cue':cue['id'],
                    'object':obj,'project':project}),
                'original_project_ref':project,'origin_event_ref':event_ref,
                'source_cue_ref':cue['id'],'world_material_object_ref':obj,
                'original_expected_difference':copy(expected)}
               if strict else None)
        possible.append({
            **({'incidental_object_end_basis':basis} if basis is not None else {}),
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
        **({'incidental_object_end_basis':copy(q['incidental_object_end_basis'])}
           if q.get('incidental_object_end_basis') is not None else {}),
        'not_a_preexisting_actor_goal':True,
        'not_the_event_original_purpose':True,
        'semantic_grade':'SOURCEFREE_PROVISIONAL_OBJECT_POSSIBILITY',
    }]

def qualify_incidental_object_takeup(actor, experience, event_ref, end):
    """Distinct completed exploratory trial followed by another actual
    independent same-object operation, not arbitrary shared cue vocabulary."""
    basis=end.get('incidental_object_end_basis')
    if type(basis) is not dict or experience.get('actor')!=actor.get('id'):
        return None
    obj=basis['world_material_object_ref']
    if (experience.get('status')!='PERFORMED'
            or experience.get('participated') is not True
            or experience.get('own_action') not in ('INSPECT','REPAIR')
            or event_ref==end['origin_event']):
        return None
    selection=experience.get('own_practical_selection') or {}
    if (selection.get('possible_end_trial') is not None
            or selection.get('world_request',{}).get('material_object_ref')!=obj):
        return None
    actual=[c for c in _source_received_signs(experience)
            if c.get('kind')=='performed_'+experience['own_action'].lower()
            and c.get('material_object_ref')==obj]
    trials=[t for t in end.get('trial_history',[])
            if t.get('event_ref') not in (end['origin_event'],event_ref)
            and t.get('operation') in ('INSPECT','REPAIR')
            and t.get('actor_experienced_status')=='PERFORMED'
            and t.get('source_material_object_ref')==obj]
    if len(actual)!=1 or not trials:return None
    return {'possible_end_ref':end['id'],'later_perceived_cue_ref':actual[0]['id'],
            'source_trial_ref':trials[-1]['id'],'source_object_ref':obj,
            'origin_incidental_good_ref':basis['id']}


def possible_cross_object_significance(actor, experience, event_ref):
    """A previously exercised way of attending can mediate a new encounter.

    Offer an open semantic occasion, not a proposed similarity or meaning.
    Distinct particular objects, prior acquired cultural reference and a
    later independently selected inspection supply the minimum witness.
    The prior object's presence, explicit recollection and speaker's current
    presence are not required. No automatic transfer of ownership, meaning,
    competence, or permission. No new end without semantic nomination.
    """
    aid=actor.get('id')
    clock=experience.get('clock')
    selection=experience.get('own_practical_selection') or {}
    if (experience.get('actor')!=aid or type(clock) is not int
            or experience.get('participated') is not True
            or experience.get('status')!='PERFORMED'
            or experience.get('own_action')!='INSPECT'
            or selection.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT'
            or selection.get('possible_end_trial') is not None):
        return []
    request=selection.get('world_request') or {}
    obj=request.get('material_object_ref')
    if request.get('operation')!='INSPECT' or type(obj) is not str:
        return []
    signs=[c for c in _source_received_signs(experience)
           if c.get('kind')=='performed_inspect'
           and c.get('source_actor')==aid and c.get('material_object_ref')==obj]
    if len(signs)!=1:return []
    sign=signs[0]
    encounters=actor.get('object_encounters',[])
    current=[e for e in encounters if e.get('actor')==aid
             and e.get('event_ref')==event_ref
             and e.get('experience_ref')==experience.get('ref')
             and e.get('material_object_ref')==obj
             and e.get('perceived_cue_ref')==sign['id']
             and e.get('personally_attempted_operation')=='INSPECT']
    if len(current)!=1:return []
    # Do not repeatedly reinterpret the same encounter/old practice pair
    # after an end has already been constituted, even after its takeup.
    seen={(e.get('incidental_object_end_basis',{}).get('source_practice_ref'),
           e.get('origin_material_object_ref')) for e in actor.get('possible_ends',[])}
    out=[]
    demos=actor.get('cultural_demonstrations',[])
    for practice,source,exercised in qualified_exercised_cultural_sources(
            aid,clock,actor.get('cultural_reference_practices',[]),demos,encounters):
        old=practice['object_ref']
        events=practice['source_event_refs']
        if old==obj or event_ref in events or (practice['id'],obj) in seen:
            continue
        basis={'source_practice_ref':practice['id'],
               'source_demonstration_ref':source['id'],
               'source_exercised_encounter_ref':exercised['id'],
               'source_event_refs':copy(events),
               'earlier_material_object_ref':old,
               'world_material_object_ref':obj,
               'origin_event_ref':event_ref,
               'source_cue_ref':sign['id'],
               'current_encounter_ref':current[0]['id'],
               'current_project_refs':copy(selection.get('selected_project_refs',[])),
               'relation_kind':'POSSIBLE_REFUNCTIONING_OF_ACQUIRED_ATTENTION',
               'not_proof_of_similarity_or_recollection':True}
        basis['id']=stable_id('cross_object_significance',basis)
        out.append({'source_cue_ref':sign['id'],'world_material_object_ref':obj,
                    'incidental_object_end_basis':basis,
                    'earlier_exercised_description':exercised.get('received_public_description'),
                    'current_received_description':current[0].get('received_public_description'),
                    'candidate_future_activities':['INSPECT','REPAIR'],
                    'meaning_not_preselected':True,
                    'source_grade':GRADE})
    # Independently nominate oldest and most recent qualified practices.
    # This bounded sampling is provisional, not a law of human association.
    out.sort(key=lambda q: next(p['origin_clock'] for p in
        actor['cultural_reference_practices']
        if p['id']==q['incidental_object_end_basis']['source_practice_ref']))
    return out if len(out)<=2 else [out[0],out[-1]]
