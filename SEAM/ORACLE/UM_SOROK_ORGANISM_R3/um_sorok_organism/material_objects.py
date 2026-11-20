"""SORACLE R12 — a material object has a history independent of its meaning.

One actor can produce, inspect, later repair, remember, dislike or forget the
same artifact. The world retains its objective maker, site, material provenance,
controller and changes; nobody's current narration becomes the canonical
object. Producing labor does not automatically convey ownership, wages, love
or recognition. A subsequent actor can encounter an object made before them.
These operations are sourcefree bounded material approximations.
"""
import math
from .types import stable_id, GRADE
from .organism import eligible


def _material_right(site, actor):
    controller=site.get('controller')
    rights=site.get('material_use_grants',[])
    if type(rights) is not list:
        raise ValueError('OBJECT_INVALID_MATERIAL_RIGHTS')
    return controller is None or controller==actor or actor in rights


def _stock(site):
    value=site.get('stock',0)
    if type(value) not in (int,float) or not math.isfinite(value) or value<0:
        raise ValueError('OBJECT_INVALID_MATERIAL_STOCK')
    return value


def can_make(world,actor,location):
    site=world.get('sites',{}).get(location)
    return (type(site) is dict and _material_right(site,actor)
            and _stock(site)>=2)


def produce_artifact(world,actor_id,location):
    """Actually consume available material and preserve unequal ownership."""
    site=world.get('sites',{}).get(location)
    if not isinstance(site,dict) or not _material_right(site,actor_id):
        return {'status':'BLOCKED','outcome':'MATERIAL_USE_NOT_AUTHORIZED'}
    if _stock(site)<2:
        return {'status':'BLOCKED','outcome':'INSUFFICIENT_ARTIFACT_MATERIAL'}
    before=_stock(site)
    site['stock']=before-2
    controller=site.get('controller')
    owner=controller if type(controller) is str and controller else actor_id
    ref=stable_id('material_artifact',{
        'actor':actor_id,'world':world['id'],'clock':world['clock']+1,
        'count':len(world.setdefault('material_objects',{}))})
    obj={
        'id':ref,'kind':'WORKED_MATERIAL_ARTIFACT',
        'location':location,'created_clock':world['clock']+1,
        'maker':actor_id,'owner':owner,'possessor':owner,
        'condition':.56,'visible':True,
        'objective_labor_history':[{
            'clock':world['clock']+1,'actor':actor_id,
            'operation':'MAKE_OBJECT','material_stock_units':2,
            'site':location,'status':'PERFORMED',
            'recipient_of_output':owner,
            'consent_or_affection':'NOT_INFERRED','grade':GRADE}],
        'material_source_location':location,
        'condition_not_actor_belief':True,
        'actor_meanings':'EACH_ACTOR_OWNS_OWN_INTERPRETATION',
        'grade':GRADE,
    }
    world['material_objects'][ref]=obj
    world.setdefault('material_claims',[]).append({
        'clock':world['clock']+1,'kind':'OBJECT_PRODUCED',
        'object_ref':ref,'worker':actor_id,'actual_owner':owner,
        'material_used':2,
        'wage_entitlement':'NOT_INFERRED_FROM_PRODUCTION_ALONE',
        'owner_not_identical_with_maker':owner!=actor_id,
        'grade':GRADE})
    return {'status':'PERFORMED','outcome':'MATERIAL_ARTIFACT_PRODUCED',
            'object_ref':ref,'real_maker':actor_id,'objective_owner':owner,
            'material_consumed':2,'grade':GRADE}


def material_objects_present(world,location):
    return sorted([
        x for x in world.get('material_objects',{}).values()
        if type(x) is dict and x.get('location')==location
        and x.get('visible') is True and type(x.get('id')) is str],
        key=lambda x:x['id'])


def repair_artifact(world,actor_id,location,object_ref):
    """The real same object's condition can change across distinct workers."""
    obj=world.get('material_objects',{}).get(object_ref)
    if type(obj) is not dict or obj.get('location')!=location:
        return {'status':'BLOCKED','outcome':'MATERIAL_OBJECT_NOT_PRESENT'}
    site=world.get('sites',{}).get(location,{})
    if not _material_right(site,actor_id):
        return {'status':'BLOCKED','outcome':'REPAIR_MATERIAL_USE_NOT_AUTHORIZED'}
    if _stock(site)<1:
        return {'status':'BLOCKED','outcome':'REPAIR_MATERIAL_NOT_AVAILABLE'}
    prior=obj.get('condition')
    if type(prior) not in (int,float) or not 0<=prior<=1:
        raise ValueError('OBJECT_INVALID_CONDITION')
    if prior>=.98:
        return {'status':'PARTIAL','outcome':'ARTIFACT_ALREADY_IN_GOOD_CONDITION'}
    site['stock']=_stock(site)-1
    updated=round(min(1,prior+.24),5)
    obj['condition']=updated
    obj.setdefault('objective_labor_history',[]).append({
        'clock':world['clock']+1,'actor':actor_id,
        'operation':'REPAIR','material_stock_units':1,
        'condition_before':prior,'condition_after':updated,
        'owner_before':obj.get('owner'),
        'ownership_not_transferred_by_repair':True,
        'grade':GRADE})
    return {'status':'PERFORMED','outcome':'MATERIAL_ARTIFACT_REPAIRED',
            'object_ref':object_ref,'condition_prior':prior,
            'condition_after':updated,'owner':obj.get('owner'),
            'source_labor_event_clock':world['clock']+1,'grade':GRADE}


def object_bound_alternatives(constitution,access,action):
    """A perceived object is a material prospective target, not a learned end."""
    if action not in ('INSPECT','REPAIR'):
        return []
    visible=sorted({c.get('material_object_ref') for c in access.cues
         if isinstance(c,dict) and c.get('kind')=='material_object_present'
         and type(c.get('material_object_ref')) is str})
    alternatives=[]
    for ref in visible[:24]:
        alternatives.append({
            'option_id':stable_id('object_practical_option',{
                'actor':constitution.actor,'clock':constitution.clock,
                'operation':action,'object':ref}),
            'actor':constitution.actor,'as_of_clock':constitution.clock,
            'operation':action,'project_id':None,
            'grounds_status':'PRESENT_MATERIAL_OBJECT_NOT_ASSUMED_MOTIVE',
            'world_request':{
                'operation':action,'addressed_party_ref':None,
                'material_object_ref':ref},
            'anticipated_difference':None,
            'binding_status':'OBJECT_CURRENTLY_VISIBLE_NOT_EVIDENCE_OF_RIGHTS',
            'objective_ownership':'WORLD_OWNED_NOT_ACTOR_INFERRED',
            'source_grade':GRADE,'not_a_conscious_plan':True,
        })
    return alternatives


def material_opportunity_from_history(constitution,access):
    """An earlier actually exercised repair may prompt a MAKING attempt.

    This is one sourcefree hypothesized generalization of available means,
    not independently demonstrated craft competence.
    """
    histories=getattr(constitution,'power_exercises',[])
    practiced=[h for h in histories
               if isinstance(h,dict) and h.get('operation')=='REPAIR'
               and h.get('attempt_status_analyst_receipt')=='PERFORMED'
               and h.get('encounter_location')==access.location]
    if not practiced or 'MAKE_OBJECT' not in access.affordances:
        return {'offers':[],'readset':[],'grade':GRADE}
    allowed,_=eligible(constitution.body,'MAKE_OBJECT')
    if not allowed:
        return {'offers':[],'readset':[],'grade':GRADE}
    return {'offers':[{
        'action':'MAKE_OBJECT','score':.095,
        'basis':['HISTORICALLY_EXERCISED_MATERIAL_REPAIR']+
                ['exercise:'+h['experience_ref'] for h in practiced[-12:]],
        'opportunity':'PROSPECTIVE_MATERIAL_COMPOSITION_NOT_ACQUIRED_MASTERY',
        'object_to_be_generated_by_world':True,
        'material_right_not_granted_by_history':True,
        'grade':GRADE}],
        'readset':[h['event_ref'] for h in practiced[-12:]],
        'grade':GRADE}
