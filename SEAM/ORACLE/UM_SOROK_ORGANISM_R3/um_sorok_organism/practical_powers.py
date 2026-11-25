"""SORACLE R12 — A historically exercised power is not an inherent trait.

Actual prior exercise can change the repertoire of *possible attempts*.  A
technical operation performed with help does NOT establish independent mastery;
when help disappears, it can instead license a modest, independently resolved
practice trial.  Solo performance is evidence of prior enactment in that
context, not of universal expertise.  World law, body, institutions and an
Other's future willingness retain independent authority.

Owner-adjacent sourcefree research organ, not native P3/CAN/PFF admission or a
scientifically measured theory of skill acquisition.
"""
from .types import copy, stable_id, GRADE
from .organism import eligible

# The physical vocabulary is inherited.  Substitution is allowed only for
# operations whose plausible component practice is already expressed by the
# existing organism, never generic applied competence for WORK or property.
PRACTICEABLE = frozenset({'SING', 'JOIN', 'MAKE_SPACE', 'PRACTICE'})
REPEATABLE = frozenset({'SING','JOIN','MAKE_SPACE','PRACTICE',
                        'SIGNAL','ASK','INSPECT','REPAIR','WORK',
                        'FEED','SIGN_FOOD_PETITION'})


def retain_exercised_power(actor, experience, objective_ref, location):
    """Preserve actor's personally undergone attempt and conditions of exercise.

    Does not attribute unperceived objective success, acquired skill, conscious
    motive, another actor's purpose, or the ability to perform in a new site.
    """
    if actor.get('id') != experience.get('actor') or type(objective_ref) is not str:
        raise ValueError('EXERCISE_ACTOR_OR_EVENT_MISMATCH')
    felt=experience.get('felt_enactment') or {}
    operation=felt.get('attempted_operation')
    if type(operation) is not str or operation not in REPEATABLE:
        return None
    if not experience.get('participated'):
        return None
    prior=actor.setdefault('power_exercises',[])
    key=stable_id('power_exercise',{'actor':actor['id'],
        'world_event':objective_ref,'operation':operation})
    if any(p.get('id')==key for p in prior):
        return {'kind':'ALREADY_RETAINED_EXERCISE','ref':key,
                'no_duplicate_history':True,'grade':GRADE}
    status=experience.get('status','UNKNOWN')
    partner=experience.get('reciprocated_partner')
    signs=[x.get('id') for x in experience.get('perceived_cues',[])
           if isinstance(x,dict) and type(x.get('id')) is str]
    # Real co-participation is not automatically a causal explanation for what
    # the actor accomplished. Its status is deliberately distinctive.
    configuration=('PERCEIVED_JOINT_PARTICIPATION' if partner and signs else
                   'NO_PERCEIVED_JOINT_PARTICIPATION')
    receipt={
        'id':key,'actor':actor['id'],'event_ref':objective_ref,
        'event_clock':experience.get('clock'),
        'experience_ref':experience.get('ref'),
        'operation':operation,'encounter_location':location,
        'attempt_status_analyst_receipt':status,
        'felt_attempt':True,
        'participation_configuration':configuration,
        'coactor_as_experienced':partner if configuration==
            'PERCEIVED_JOINT_PARTICIPATION' else None,
        'personally_received_sign_refs':sorted(set(signs)),
        'independent_expertise':'NOT_ESTABLISHED',
        'dependence_on_original_sponsor':'NOT_ESTABLISHED',
        'technical_skill_generalization':'NOT_ESTABLISHED',
        'available_means_in_another_site':'NOT_ESTABLISHED',
        'objective_success_not_a_motive':'NOT_INFERRED',
        'grade':GRADE,
    }
    # A particular physically worked object is not an inferred project or
    # generic motor score. Preserve only an actually self-selected and
    # personally received repair of that object.
    sel=experience.get('own_practical_selection') or {}
    obj=(sel.get('world_request') or {}).get('material_object_ref')
    if (operation=='REPAIR' and status=='PERFORMED' and not partner
            and sel.get('status')=='ACTOR_POLICY_PRACTICAL_ATTEMPT'
            and sel.get('actor')==actor['id'] and type(obj) is str
            and sel.get('possible_end_trial') is None):
        signs=[c for c in experience.get('perceived_cues',[])
               if c.get('kind')=='performed_repair' and c.get('source_actor')==actor['id']
               and c.get('material_object_ref')==obj
               and 'material_artifact_repaired' in c.get('tags',[])]
        if len(signs)==1:
            receipt['worked_object_ref']=obj
            receipt['own_selected_repair_sign_ref']=signs[0]['id']
            receipt['own_selected_option_ref']=sel['option_id']
    prior.append(receipt)
    return {'kind':'RETAIN_EXERCISED_POWER',
            'ref':key,'configuration':configuration,
            'qualified_operation':operation,
            'not_an_acquired_motive_or_mastery':True,'grade':GRADE}


def situated_exercised_repertoire(constitution, access):
    """Offer historically specific next operations, never body/work permission.

    The original partner may no longer be available. In that case assisted
    singing supplies at most an opportunity for an independent PRACTICE probe,
    not an unearned ability to realize the full prior joint performance.
    """
    if constitution.actor!=access.actor:
        raise ValueError('EXERCISE_CONSTITUTION_ACCESS_MISMATCH')
    prior=getattr(constitution,'power_exercises',[])
    present={x.get('source_actor') for x in access.cues
             if isinstance(x,dict) and x.get('kind')=='coactor_present'}
    # Human counterpart is a distinct access channel, not a roster actor.
    present |= {x.get('visitor_ref') for x in access.cues
                if x.get('kind')=='visitor_vocal_partner'
                and type(x.get('visitor_ref')) is str}
    eligible_at_site={}
    held_back=[]
    for x in prior[-512:]:
        if not isinstance(x,dict) or x.get('operation') not in REPEATABLE:
            continue
        if x.get('attempt_status_analyst_receipt')!='PERFORMED':
            # Failure can form history, not automatic future competence.
            held_back.append(x.get('id'))
            continue
        operation=x['operation']
        supported=(x.get('participation_configuration')==
                   'PERCEIVED_JOINT_PARTICIPATION')
        other=x.get('coactor_as_experienced')
        if x.get('encounter_location')!=access.location:
            held_back.append(x.get('id'))
            continue
        if supported and other not in present:
            if operation not in PRACTICEABLE:
                held_back.append(x.get('id'))
                continue
            proposed='PRACTICE'
            significance='INDEPENDENT_PRACTICE_PROBE_NOT_PRIOR_JOINT_MASTERED'
        else:
            proposed=operation
            significance=('PREVIOUSLY_EXERCISED_WITH_POSSIBLE_OTHER'
                          if supported else
                          'SITUATIONALLY_REPEATED_OPERATION_NOT_GLOBAL_MASTERY')
        allowed,_=eligible(constitution.body,proposed)
        if not allowed:
            held_back.append(x.get('id'))
            continue
        row=eligible_at_site.setdefault(proposed,{
            'action':proposed,'source_experience_refs':[],
            'support_configs':set(),'source_event_refs':[],
            'source_actor':constitution.actor,
            'location':access.location,
            'material_rights_not_granted':True,
            'independent_skill_not_inferred':True,
            'actor_motive_not_inferred':True,
            'sourcefree_grade':GRADE,
        })
        row['source_experience_refs'].append(x['experience_ref'])
        row['source_event_refs'].append(x['event_ref'])
        row['support_configs'].add(significance)
    out=[]
    for operation,row in sorted(eligible_at_site.items()):
        if operation in ('WORK','REPAIR') and access.location not in (
                'workshop','home','hall'):
            continue
        out.append({
            'action':operation,
            'basis':sorted(set(row['source_experience_refs'][-24:])),
            'source_event_refs':sorted(set(row['source_event_refs'][-24:])),
            'historical_support_statuses':sorted(row['support_configs']),
            'opportunity':'HISTORICALLY_EXERCISED_POSSIBILITY',
            'score':.115,
            'not_necessarily_a_deliberate_end':True,
            'no_automatic_motive_or_competence':True,
            'world_authority_remains_independent':True,
            'grade':GRADE,
        })
    return {'offered':out,'retained_but_unqualified_refs':sorted(set(
                    x for x in held_back if type(x) is str)),
            'readset':sorted(set(r for row in out
                        for r in row['source_event_refs'])),
            'no_a_priori_independent_mastery':True,'grade':GRADE}


def _qualified_repair_basis(actor,location,current):
    """Bounded convergence of aggregate practice and distinct actual objects.

    Modeled exposure is not a series of invented successes. Two actually
    selected and personally received repairs are a separate requirement.
    """
    if current.get('actor')!=actor['id'] or current.get('operation')!='REPAIR' or not current.get('worked_object_ref'):
        return None
    def valid(x):
        return (x.get('actor')==actor['id'] and x.get('operation')=='REPAIR'
                and x.get('encounter_location')==location
                and x.get('attempt_status_analyst_receipt')=='PERFORMED'
                and x.get('participation_configuration')=='NO_PERCEIVED_JOINT_PARTICIPATION'
                and type(x.get('worked_object_ref')) is str
                and type(x.get('event_clock')) is int
                and any(p.get('event')==x.get('event_ref')
                        and p.get('experience_ref')==x.get('experience_ref')
                        and p.get('practical_option_ref')==x.get('own_selected_option_ref')
                        and x.get('own_selected_repair_sign_ref') in p.get('received_cue_refs',[])
                        for p in actor.get('evidence_paths',[])))
    if not valid(current):return None
    prior=[x for x in actor.get('power_exercises',[]) if valid(x)
           and x['event_clock']<current['event_clock']
           and x['worked_object_ref']!=current['worked_object_ref']]
    if not prior:return None
    earlier=max(prior,key=lambda x:x['event_clock'])
    periods=[p for p in actor.get('practice_exposures',[])
             if p.get('actor')==actor['id'] and p.get('operation')=='REPAIR'
             and p.get('location')==location
             and p.get('grade')=='SOURCEFREE_CONDITIONED_AGGREGATE_PRACTICE'
             and p.get('support_configuration')=='SOLO_COMPONENT_PRACTICE'
             and type(p.get('end_clock')) is int and p['end_clock']<earlier['event_clock']
             and type(p.get('modeled_participation_days')) in (int,float)
             and p['modeled_participation_days']>0 and p.get('source_ref')]
    if sum(p['modeled_participation_days'] for p in periods)<7:return None
    return {'actor':actor['id'],'location':location,'operation':'REPAIR',
            'aggregate_practice_refs':[p['id'] for p in periods],
            'earlier_exercise_ref':earlier['id'],'later_exercise_ref':current['id'],
            'distinct_worked_objects':[earlier['worked_object_ref'],current['worked_object_ref']],
            'event_refs':[earlier['event_ref'],current['event_ref']],
            'provisional_condition_increment':.34,
            'not_universal_mastery_or_material_permission':True,'grade':GRADE}


def possible_repair_technique(actor,experience,event_ref):
    if experience.get('actor')!=actor['id']:return []
    location=experience.get('location')
    if active_repair_technique(actor,location):return []
    rows=[x for x in actor.get('power_exercises',[])
          if x.get('event_ref')==event_ref and x.get('experience_ref')==experience.get('ref')]
    if len(rows)!=1:return []
    basis=_qualified_repair_basis(actor,location,rows[0])
    return [{'kind':'ACQUIRE_REPAIR_TECHNIQUE','basis':basis}] if basis else []


def admit_repair_technique(actor,experience,event_ref,proposal):
    if proposal not in possible_repair_technique(actor,experience,event_ref):
        raise ValueError('REPAIR_TECHNIQUE_UNQUALIFIED_HISTORY')
    b=proposal['basis'];row=next(x for x in actor['power_exercises'] if x['id']==b['later_exercise_ref'])
    ident=stable_id('acquired_repair_technique',b)
    row['acquired_repair_technique']={'id':ident,'basis':copy(b),
        'fictional_component_facility_not_measured_skill':True,'grade':GRADE}
    return {'kind':proposal['kind'],'technique_ref':ident,'grade':GRADE}


def active_repair_technique(actor,location):
    # Existing actor-local exercise state is the only source of the technical
    # change. Neither the world request nor a semantic label can mint it.
    for row in reversed(actor.get('power_exercises',[])):
        rec=row.get('acquired_repair_technique')
        if not rec or rec.get('basis',{}).get('location')!=location:continue
        basis=_qualified_repair_basis(actor,location,row)
        if basis and rec.get('basis')==basis and rec.get('id')==stable_id('acquired_repair_technique',basis):
            return rec
    return None
