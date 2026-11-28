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


PREPROJECT_COMPONENTS=frozenset({'SIGNAL','PRACTICE'})

def preproject_exercise_basis(actor, operation, location, source_ref, as_of):
    """An actual earlier independently selected bodily exercise, not a project.

    Only sparse child practice of rudimentary operations is in this new lane.
    An externally requested operation, joint success, imagined scene or an
    aggregate receipt cannot supply its initial detailed historical anchor.
    """
    if (actor.get('role')!='child' or operation not in PREPROJECT_COMPONENTS
            or type(source_ref) is not str or type(as_of) is not int):
        return None
    matches=[r for r in actor.get('power_exercises',[])
             if r.get('id')==source_ref and r.get('actor')==actor.get('id')
             and r.get('operation')==operation
             and r.get('encounter_location')==location
             and r.get('attempt_status_analyst_receipt')=='PERFORMED'
             and r.get('felt_attempt') is True
             and r.get('participation_configuration')=='NO_PERCEIVED_JOINT_PARTICIPATION'
             and r.get('actor_selected_preproject_exercise') is True
             and type(r.get('event_clock')) is int and r['event_clock']<=as_of]
    if len(matches)!=1:return None
    row=matches[0]
    paths=[p for p in actor.get('evidence_paths',[])
           if p.get('event')==row.get('event_ref')
           and p.get('experience_ref')==row.get('experience_ref')
           and p.get('own_action')==operation
           and p.get('practical_option_ref')==row.get('preproject_option_ref')
           and type(p.get('practical_option_ref')) is str
           and not p.get('selected_project_refs')
           and not p.get('provisional_end_trial_ref_analytic_only')]
    return row if len(paths)==1 else None


def preproject_vocal_basis(actor, location, as_of):
    """Earlier actually initiated signal + qualified ordinary participation.
    This is not an acquired desire to communicate, a word, or an Other's consent.
    """
    rows=[]
    for row in actor.get('practice_exposures',[]):
        if (row.get('actor')==actor.get('id') and row.get('operation')=='SIGNAL'
                and row.get('location')==location
                and row.get('grade')=='SOURCEFREE_CONDITIONED_AGGREGATE_PRACTICE'
                and type(row.get('modeled_practice_hours')) in (int,float)
                and 0<row['modeled_practice_hours']<=3650*16
                and type(row.get('end_clock')) is int and row['end_clock']<=as_of):
            prior=preproject_exercise_basis(actor,'SIGNAL',location,
                row.get('preproject_exercise_ref'),row.get('start_clock'))
            if prior is not None and prior['event_ref']==row.get('anchor_actual_event_ref'):
                rows.append(row)
    return max(rows,key=lambda r:(r['end_clock'],r['id'])) if rows else None


def preproject_motor_readiness(actor):
    """Separate coarse modeled dose from counted, actually performed events.

    Provisional ceiling: 30 modeled hours -> at most .024 motor floor. No
    language, remembered episodes, purpose, independent mastery or future
    support. Use cumulative hours, not number of period partitions.
    """
    total=0.0
    seen=set()
    for row in actor.get('practice_exposures',[]):
        if row.get('operation')!='PRACTICE' or not row.get('preproject_exercise_ref'):
            continue
        ref=row.get('id')
        hours=row.get('modeled_practice_hours')
        if (type(ref) is not str or ref in seen or type(hours) not in (int,float)
                or not 0<hours<=3650*16 or row.get('actor')!=actor.get('id')
                or row.get('grade')!='SOURCEFREE_CONDITIONED_AGGREGATE_PRACTICE'
                or not preproject_exercise_basis(actor,'PRACTICE',row.get('location'),
                     row['preproject_exercise_ref'],row.get('start_clock'))):
            continue
        seen.add(ref)
        total+=hours
    return round(min(.024,total*.0008),5)


def qualified_project_exercise_basis(actor,project_ref,exercise_ref,operation,location,clock):
    """The ordinary continuation of an acquired, actually exercised course.
    Reuse the existing actor's project, lived exercise, and objective course.
    Narrow R67 vocal route; a project label or a trial alone is insufficient.
    """
    from .activity import ordinary_vocal_project_site
    if (operation!='SING' or type(project_ref) is not str
            or type(exercise_ref) is not str or type(clock) is not int):return None
    ps=[p for p in actor.get('projects',[]) if p.get('id')==project_ref
        and p.get('status','active')=='active' and operation in p.get('means',[])
        and p.get('ordinary_vocal_genesis_basis')
        and ordinary_vocal_project_site(actor,p,location,clock)]
    if len(ps)!=1:return None
    p=ps[0]
    rows=[e for e in actor.get('power_exercises',[])
          if e.get('id')==exercise_ref and e.get('actor')==actor['id']
          and e.get('operation')==operation and e.get('encounter_location')==location
          and e.get('attempt_status_analyst_receipt')=='PERFORMED'
          and e.get('felt_attempt') is True
          and e.get('participation_configuration')=='NO_PERCEIVED_JOINT_PARTICIPATION'
          and type(e.get('event_clock')) is int and e['event_clock']<=clock]
    if len(rows)!=1:return None
    e=rows[0]
    paths=[q for q in actor.get('evidence_paths',[]) if q.get('event')==e.get('event_ref')
           and q.get('experience_ref')==e.get('experience_ref') and q.get('own_action')==operation
           and q.get('selected_project_refs')==[project_ref]
           and type(q.get('practical_option_ref')) is str
           and not q.get('provisional_end_trial_ref_analytic_only')]
    courses=[q for q in p.get('operational_history',[]) if q.get('event')==e.get('event_ref')
             and q.get('project')==project_ref and q.get('operation')==operation
             and q.get('performed_status')=='PERFORMED' and q.get('selected_at_actor_attempt') is True
             and q.get('intent_attribution')=='ACTOR_POLICY_SELECTED_PROJECT_COURSE']
    return e if len(paths)==len(courses)==1 else None


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
                    'ARRANGEMENT_UNRESOLVED','RECIPROCAL_COMPONENT_PRACTICE'):
        raise ValueError('ROUTINE_UNQUALIFIED_SUPPORT')
    if mode=='RECIPROCAL_COMPONENT_PRACTICE' and not (process.get('reciprocal_routine_pair_ref') and process.get('matched_counterpart_source_ref')):
        raise ValueError('ROUTINE_UNMATCHED_RECIPROCAL_EXPOSURE')
    if place!=actor.get('location'):
        return None
    prior_ref=process.get('preproject_exercise_ref')
    prior=None
    project_ref=process.get('practice_project_ref')
    project_exercise_ref=process.get('project_exercise_ref')
    project_exercise=None
    if project_ref is not None:
        confirmation=process.get('source_registry_confirmation') or {}
        if (prior_ref is not None or confirmation.get('practice_project_ref')!=project_ref
                or confirmation.get('project_exercise_ref')!=project_exercise_ref
                or confirmation.get('practice_operation')!=op
                or confirmation.get('source_ref')!=source or mode!='SOLO_COMPONENT_PRACTICE'):
            raise ValueError('PROJECT_ROUTINE_SOURCE_MISMATCH')
        project_exercise=qualified_project_exercise_basis(actor,project_ref,project_exercise_ref,op,place,start_clock)
        if project_exercise is None:raise ValueError('PROJECT_ROUTINE_NO_ACTUAL_SELECTED_EXERCISE')
        if fraction==0:return None
    elif prior_ref is not None:
        confirmation=process.get('source_registry_confirmation') or {}
        if (confirmation.get('preproject_exercise_ref')!=prior_ref
                or confirmation.get('practice_operation')!=op
                or confirmation.get('source_ref')!=source
                or mode!='SOLO_COMPONENT_PRACTICE'):
            raise ValueError('PREPROJECT_ROUTINE_SOURCE_MISMATCH')
        prior=preproject_exercise_basis(actor,op,place,prior_ref,start_clock)
        if prior is None:raise ValueError('PREPROJECT_ROUTINE_NO_ACTUAL_OWN_EXERCISE')
        if fraction==0:return None
    elif not any(p.get('status','active')=='active' and op in p.get('means',[])
                 for p in actor.get('projects',[])):
        return None
    ref=stable_id('qualified_aggregate_practice',{
        'actor':actor['id'],'source':source,'operation':op,
        'start':start_clock,'days':days,'fraction':fraction,'mode':mode,
        **({'preproject_exercise_ref':prior_ref} if prior is not None else {}),
        **({'practice_project_ref':project_ref,'project_exercise_ref':project_exercise_ref}
           if project_exercise is not None else {})})
    records=actor.setdefault('practice_exposures',[])
    if any(e.get('id')==ref for e in records):
        return {'id':ref,'already_recorded':True}
    record={
        'id':ref,'actor':actor['id'],'operation':op,
        'location':place,'source_ref':source,
        'start_clock':start_clock,'end_clock':start_clock+days,
        'modeled_participation_days':round(days*fraction,3),
        'support_configuration':mode,
        **({'reciprocal_routine_pair_ref':process['reciprocal_routine_pair_ref']}
           if mode=='RECIPROCAL_COMPONENT_PRACTICE' else {}),
        'no_claim_all_days_successful':True,
        'individual_microevents_not_invented':True,
        'other_contributions_not_automatically_authorized':True,
        'not_a_conscious_account':True,
        'grade':'SOURCEFREE_CONDITIONED_AGGREGATE_PRACTICE',
    }
    if prior is not None:
        record.update({'preproject_exercise_ref':prior_ref,
            'anchor_actual_event_ref':prior['event_ref'],
            'anchor_actual_experience_ref':prior['experience_ref'],
            'modeled_practice_hours':round(days*fraction*process['hours_per_active_day'],5),
            'no_acquired_project_required_or_created':True})
    if project_exercise is not None:
        record.update({'practice_project_ref':project_ref,'project_exercise_ref':project_exercise_ref,
            'anchor_actual_event_ref':project_exercise['event_ref'],
            'anchor_actual_experience_ref':project_exercise['experience_ref'],
            'modeled_practice_hours':round(days*fraction*process['hours_per_active_day'],5),
            'not_daily_project_selection_or_motive_fulfillment':True})
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
          +.025*(days('ASSISTED_COMPONENT_PRACTICE')+days('RECIPROCAL_COMPONENT_PRACTICE'))
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
