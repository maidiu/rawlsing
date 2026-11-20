"""SORACLE R13 — explicit, scoped source registry for modeled ordinary lives.

A string labeled 'source_ref' is not itself a warrant for hundreds of
fictional training/care/work days. The research runner may explicitly declare
a sourcefree scenario envelope (who, which ongoing practice, where, how many
hours, during what window); the world keeps that declaration and subsequent
aggregate usage separately. It does NOT thereby become PYAT source authority,
proof of events, an independent coactor's consent, or scientific evidence.
"""
from .types import stable_id, copy, GRADE
from .organism import eligible

KINDS=frozenset({'QUALIFIED_ROUTINE_PRACTICE',
                 'QUALIFIED_REPRODUCTIVE_CARE',
                 'QUALIFIED_WAGE_LABOR',
                 'QUALIFIED_MATERIAL_FEEDING',
                 'QUALIFIED_OTHER_OBLIGATION'})
SCENARIO_CLASS='EXPLICIT_SOURCEFREE_HISTORICAL_FIXTURE'


def register_sourcefree_period_envelope(world,actors,spec):
    if type(spec) is not dict or spec.get('kind') not in KINDS:
        raise ValueError('ROUTINE_SOURCE_UNKNOWN_KIND')
    actor=spec.get('actor')
    location=spec.get('location')
    if actor not in actors or type(location) is not str or not location:
        raise ValueError('ROUTINE_SOURCE_UNREGISTERED_ACTOR_OR_SITE')
    if (world.get('positions',{}).get(actor)!=location
            or actors[actor].get('location')!=location):
        raise ValueError('ROUTINE_SOURCE_NOT_CURRENT_ACTOR_SITE')
    start=spec.get('start_clock')
    end=spec.get('end_clock')
    max_daily=spec.get('max_hours_per_active_day')
    if (type(start) is not int or type(end) is not int
            or start<world['clock'] or end<=start or end-start>3650):
        raise ValueError('ROUTINE_SOURCE_INVALID_TIME_WINDOW')
    if (type(max_daily) not in (int,float) or
            not 0<max_daily<=16):
        raise ValueError('ROUTINE_SOURCE_INVALID_HOUR_CEILING')
    if type(spec.get('description')) is not str or not spec['description'].strip():
        raise ValueError('ROUTINE_SOURCE_MISSING_EXPLICIT_PROPOSAL')
    key=stable_id('routine_sourcefree_envelope',{
        'world':world['id'],'actor':actor,'kind':spec['kind'],
        'location':location,'start':start,'end':end,
        'max_hours':max_daily,'description':spec['description']})
    if key in world.setdefault('routine_source_registry',{}):
        raise ValueError('ROUTINE_SOURCE_DUPLICATE')
    record={
        'id':key,'actor':actor,'location':location,
        'kind':spec['kind'],'from_clock':start,'through_clock':end,
        'max_hours_per_active_day':float(max_daily),
        'description':spec['description'],
        'evidence_class':SCENARIO_CLASS,
        'not_observed_daily_events':True,
        'does_not_authorize_PYAT_source_or_native_psyche':True,
        'coactor_willingness_not_proved':True,
        'no_actual_history_until_qualified_period_executed':True,
        'registered_at_world_clock':world['clock'],'grade':GRADE,
    }
    world['routine_source_registry'][key]=record
    return record


def verify_qualified_period_envelope(world,process,start_clock,days):
    source=world.get('routine_source_registry',{}).get(
        process.get('source_ref'))
    if type(source) is not dict or source.get('evidence_class')!=SCENARIO_CLASS:
        raise ValueError('HISTORICAL_PROCESS_UNREGISTERED_SOURCE_ENVELOPE')
    if (source.get('actor')!=process.get('actor')
            or source.get('kind')!=process.get('kind')
            or source.get('location')!=process.get('location')):
        raise ValueError('HISTORICAL_PROCESS_SOURCE_SCOPE_MISMATCH')
    if (start_clock<source['from_clock'] or
            start_clock+days>source['through_clock']):
        raise ValueError('HISTORICAL_PROCESS_SOURCE_TIME_OVERREACH')
    request=process.get('hours_per_active_day')
    if (type(request) not in (int,float) or
            request>source['max_hours_per_active_day']):
        raise ValueError('HISTORICAL_PROCESS_SOURCE_HOUR_OVERREACH')
    return {
        'source_ref':source['id'],
        'source_grade':source['evidence_class'],
        'source_recorded_at':source['registered_at_world_clock'],
        'author_permission':'EXPLICIT_SOURCEFREE_SCENARIO_ONLY',
        'not_an_empirical_PYAT_warrant':True,
    }
