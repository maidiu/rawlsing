"""SORACLE R12 — mediated efficacy without metaphysical 'independent power'.

World/analyst, operative history, and reflective self-understanding are
distinct epistemic levels.  A graded technical component is not a socially
self-originating capacity, material permission, right over an Other, motive,
or actor's conscious account. Learning rates are sourcefree heuristics, not
human science. Sparse individual scenes and long compressed practice periods
have different evidential precision.
"""
from math import exp
from .types import GRADE, stable_id

COMPONENTS=frozenset({'PRACTICE','SING','JOIN','MAKE_SPACE','SIGNAL',
                      'SPEAK','ASK','REPAIR','MAKE_OBJECT','WORK'})


def _fraction(x):
    if type(x) not in (int,float) or not 0 <= x <= 1:
        raise ValueError('INVALID_MODELED_PRACTICE_FRACTION')
    return float(x)


def conserve_compressed_practice(actor, process, start_clock, days):
    """Bounded *aggregate* participation, never fictitious single events.

    A qualifying process is explicitly sourced, actor-specific, site-specific,
    tied to an actual active project. Merely advancing time doesn't cause
    learning or automatically obtain help, goods, or a right to participate.
    """
    if type(process) is not dict or process.get('kind')!='QUALIFIED_ROUTINE_PRACTICE':
        return None
    if process.get('actor')!=actor.get('id'):
        return None
    op=process.get('operation')
    place=process.get('location')
    source=process.get('source_ref')
    if op not in COMPONENTS or type(place) is not str or not place:
        raise ValueError('ROUTINE_UNKNOWN_COMPONENT_OR_SITE')
    if type(source) is not str or not source:
        raise ValueError('ROUTINE_MISSING_SOURCE')
    if type(days) is not int or not 1<=days<=3650:
        raise ValueError('ROUTINE_INVALID_DURATION')
    fraction=_fraction(process.get('provisional_exposure_fraction'))
    mode=process.get('mode','ARRANGEMENT_UNRESOLVED')
    if mode not in ('SOLO_COMPONENT_PRACTICE','ASSISTED_COMPONENT_PRACTICE',
                    'ARRANGEMENT_UNRESOLVED'):
        raise ValueError('ROUTINE_UNQUALIFIED_SUPPORT')
    if place!=actor.get('location'):
        return None
    if not any(p.get('status','active')=='active' and op in p.get('means',[])
               for p in actor.get('projects',[])):
        return None
    ref=stable_id('qualified_aggregate_practice',{
        'actor':actor['id'],'source':source,'operation':op,
        'start':start_clock,'days':days,'fraction':fraction,'mode':mode})
    records=actor.setdefault('practice_exposures',[])
    if any(e.get('id')==ref for e in records):
        return {'id':ref,'already_recorded':True}
    record={
        'id':ref,'actor':actor['id'],'operation':op,
        'location':place,'source_ref':source,
        'start_clock':start_clock,'end_clock':start_clock+days,
        'modeled_participation_days':round(days*fraction,3),
        'support_configuration':mode,
        'no_claim_all_days_successful':True,
        'individual_microevents_not_invented':True,
        'other_contributions_not_automatically_authorized':True,
        'not_a_conscious_account':True,
        'grade':'SOURCEFREE_CONDITIONED_AGGREGATE_PRACTICE',
    }
    records.append(record)
    return record


def situated_component_efficacy(actor,operation,location):
    """One operation in one setting; separate modeled level and uncertainty.

    A high-resolution PERFORMED scene indicates participation, not measured
    success quality. Aggregates can generate meaningful provisional competence
    without producing an impossible number of precise observed events.
    """
    if operation not in COMPONENTS:
        return {'operation':operation,'component_facility':'NOT_MODELED',
                'not_a_global_mastery_claim':True,'grade':GRADE}
    episodes=[e for e in actor.get('power_exercises',[])
              if isinstance(e,dict) and e.get('operation')==operation
              and e.get('encounter_location')==location
              and e.get('attempt_status_analyst_receipt')=='PERFORMED']
    solo=[e for e in episodes if e.get('participation_configuration')==
          'NO_PERCEIVED_JOINT_PARTICIPATION']
    joint=[e for e in episodes if e.get('participation_configuration')==
           'PERCEIVED_JOINT_PARTICIPATION']
    historical=[x for x in actor.get('practice_exposures',[])
                if isinstance(x,dict) and x.get('operation')==operation
                and x.get('location')==location and x.get('source_ref')]
    def days(mode):
        return sum(x.get('modeled_participation_days',0) for x in historical
                   if x.get('support_configuration')==mode)
    # This is a sourcefree programming policy, not a measured learning law.
    dose=(len(solo)+.35*len(joint)
          +.08*days('SOLO_COMPONENT_PRACTICE')
          +.025*days('ASSISTED_COMPONENT_PRACTICE')
          +.008*days('ARRANGEMENT_UNRESOLVED'))
    estimate=round(.12+.70*(1-exp(-dose/14)),4)
    # In particular, 1,000 compressed opportunities are NOT 1,000 witnessed
    # successes. Keep interval width comparatively large for low-resolution
    # historical evidence, even when estimated facility increases.
    precision=.12+.48*(1-exp(-len(episodes)/16))+.10*(
        1-exp(-len(historical)/5))
    width=.5*(1-precision)
    return {
        'operation':operation,'location':location,
        'technical_component_facility_estimate':estimate,
        'epistemic_range':[round(max(0,estimate-width),4),
                           round(min(1,estimate+width),4)],
        'actual_participation_events':len(episodes),
        'same_site_solo_component_events':len(solo),
        'same_site_joint_component_events':len(joint),
        'qualified_compressed_practice_periods':len(historical),
        'provisional_exposure_dose':round(dose,4),
        'source_world_event_refs':[x['event_ref'] for x in episodes[-24:]],
        'source_aggregate_refs':[x['id'] for x in historical[-24:]],
        'mastery_not_an_individual_global_scalar':True,
        'practical_competence_not_socially_self_originating':True,
        'facility_not_objective_permission':True,
        'facility_not_others_consent_or_love':True,
        'facility_not_actor_self_understanding':True,
        'PERFORMED_not_quality_measurement':True,
        'grade':GRADE,
    }


def objective_arrangement(actor, world, operation, location,
                          *, actual_other_participants=()):
    """Objective access and independently issued cooperation are distinct."""
    site=world.get('sites',{}).get(location,{})
    admitted=site.get('admitted',[])
    granted=site.get('material_use_grants',[])
    if not isinstance(admitted,list) or not isinstance(granted,list):
        raise ValueError('UNQUALIFIED_WORLD_PERMISSION_REGISTER')
    controller=site.get('controller')
    return {
        'actor':actor['id'],'operation':operation,'location':location,
        'situated_component':situated_component_efficacy(
            actor,operation,location),
        'site_access':site.get('access')=='public' or actor['id'] in admitted,
        'material_command':controller in (None,actor['id'])
                            or actor['id'] in granted,
        'actual_other_contributors':sorted(set(actual_other_participants)),
        'other_participation_never_implied_by_actor_skill':True,
        'control_over_others_conduct':'SEPARATE_WORLD_RELATION',
        'capacity_to_mobilize_others':'SEPARATE_HISTORICAL_RELATION',
        'actor_own_understanding':'NOT_ESTABLISHED',
        'independent_power_as_metaphysical_category':'REJECTED',
        'grade':GRADE,
    }


def seed_fictional_adult_training(actor, proposals, *, source_grade):
    """History-rich adult entrance without invented individual success scenes.

    A hypothetical adult may have practiced thousands of occasions during
    decades not individually simulated. A provider must propose plausible
    bounded periods; it may NOT convert survey answer positions into skill
    proofs. The result is constitutive *fictional* backfill with large
    uncertainty, not measured respondent development or a memory the actor
    can consciously recount.
    """
    if actor.get('role')!='adult' or type(proposals) is not list:
        raise ValueError('ADULT_PRACTICE_BACKFILL_UNQUALIFIED')
    if len(proposals)>64:
        raise ValueError('ADULT_PRACTICE_BACKFILL_TOO_MANY_PERIODS')
    rows=[]
    for index,p in enumerate(proposals):
        if type(p) is not dict:
            raise ValueError('ADULT_PRACTICE_BACKFILL_NOT_STRUCTURED')
        op=p.get('operation')
        place=p.get('location')
        duration=p.get('duration_days')
        period=p.get('past_period_ref')
        if op not in COMPONENTS or type(place) is not str or not place:
            raise ValueError('ADULT_PRACTICE_BACKFILL_UNKNOWN_COMPONENT')
        if type(duration) is not int or not 0<=duration<=actor['age_days']:
            raise ValueError('ADULT_PRACTICE_BACKFILL_IMPOSSIBLE_DURATION')
        if type(period) is not str or not period:
            raise ValueError('ADULT_PRACTICE_BACKFILL_NO_PERIOD_SOURCE')
        fraction=_fraction(p.get('participation_fraction'))
        mode=p.get('support_configuration','ARRANGEMENT_UNRESOLVED')
        if mode not in ('SOLO_COMPONENT_PRACTICE',
                        'ASSISTED_COMPONENT_PRACTICE',
                        'ARRANGEMENT_UNRESOLVED'):
            raise ValueError('ADULT_PRACTICE_BACKFILL_UNKNOWN_ARRANGEMENT')
        ident=stable_id('fictional_adult_practice',{
            'actor':actor['id'],'index':index,'period':period,
            'component':op,'place':place,'duration':duration,
            'fraction':fraction,'mode':mode})
        if any(x.get('id')==ident for x in actor.get('practice_exposures',[])):
            raise ValueError('ADULT_PRACTICE_BACKFILL_DUPLICATE')
        row={
            'id':ident,'actor':actor['id'],'operation':op,
            'location':place,
            'source_ref':'FICTIONAL_HISTORICAL_ABDUCTION:'+period,
            'modeled_participation_days':round(duration*fraction,3),
            'support_configuration':mode,
            'estimated_period_length_days':duration,
            'actual_individual_events':'NOT_RECONSTRUCTED',
            'adult_skill_is_not_measured_from_survey':True,
            'does_not_grant_permission_or_supporter_consent':True,
            'does_not_force_self_knowledge':True,
            'historical_source_grade':source_grade,
            'grade':'SOURCEFREE_UNDERIDENTIFIED_ADULT_BACKFILL',
        }
        actor.setdefault('practice_exposures',[]).append(row)
        rows.append(row)
    return rows
