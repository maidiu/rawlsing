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
from math import isfinite

KINDS=frozenset({'QUALIFIED_ROUTINE_PRACTICE',
                 'QUALIFIED_REPRODUCTIVE_CARE',
                 'QUALIFIED_WAGE_LABOR',
                 'QUALIFIED_MATERIAL_FEEDING',
                 'QUALIFIED_OTHER_OBLIGATION'})
SCENARIO_CLASS='EXPLICIT_SOURCEFREE_HISTORICAL_FIXTURE'
LIVED_CLASS='SOURCEFREE_ACTOR_LIVED_ROUTINE_PROPOSAL'
ROUTINE_OPS={'CARE':'QUALIFIED_REPRODUCTIVE_CARE','FEED':'QUALIFIED_MATERIAL_FEEDING',
             'WORK':'QUALIFIED_WAGE_LABOR',
             'PRACTICE':'QUALIFIED_ROUTINE_PRACTICE','SING':'QUALIFIED_ROUTINE_PRACTICE'}
MAX_ROUTINE_WINDOW=90
# Same-operation singing and complementary practice/join are the bounded
# joint arrangements admitted here. No inference of general teamwork.
JOINT_ROUTINE_COMPLEMENTS={
    'SING':{'SING','JOIN','MAKE_SPACE'},'PRACTICE':{'JOIN','MAKE_SPACE'},
    'JOIN':{'PRACTICE','SING','MAKE_SPACE'},'MAKE_SPACE':{'SING','PRACTICE','JOIN'},
    'SIGNAL':{'CARE','FEED'},'CARE':{'SIGNAL'},'FEED':{'SIGNAL'}}


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
    if type(source) is not dict or source.get('evidence_class') not in (SCENARIO_CLASS,LIVED_CLASS):
        raise ValueError('HISTORICAL_PROCESS_UNREGISTERED_SOURCE_ENVELOPE')
    if (source.get('actor')!=process.get('actor')
            or source.get('kind')!=process.get('kind')
            or source.get('location')!=process.get('location')):
        raise ValueError('HISTORICAL_PROCESS_SOURCE_SCOPE_MISMATCH')
    if (start_clock<source['from_clock'] or
            start_clock+days>source['through_clock']):
        raise ValueError('HISTORICAL_PROCESS_SOURCE_TIME_OVERREACH')
    if source['evidence_class']==LIVED_CLASS:
        expected=source['process']
        actual={k:v for k,v in process.items() if k!='routine_window_application'}
        if actual!=expected:
            raise ValueError('LIVED_ROUTINE_SOURCE_PROCESS_MISMATCH')
    request=process.get('hours_per_active_day')
    if (type(request) not in (int,float) or
            request>source['max_hours_per_active_day']):
        raise ValueError('HISTORICAL_PROCESS_SOURCE_HOUR_OVERREACH')
    return {
        'source_ref':source['id'],
        'source_grade':source['evidence_class'],
        'source_recorded_at':source['registered_at_world_clock'],
        'author_permission':('ADMITTED_ACTOR_LOCAL_SOURCEFREE_PROPOSAL_ONLY'
                             if source['evidence_class']==LIVED_CLASS
                             else 'EXPLICIT_SOURCEFREE_SCENARIO_ONLY'),
        'not_an_empirical_PYAT_warrant':True,
    }


def routine_exercise_receipt(actor,experience,event_ref):
    """Conserve the actual actor-selected particular course, not a model's diary.

    The operation must be performed, its purpose selected, and the same
    project must have its real operational and personally lived receipt.
    An assisted exercise cannot establish an independently reproducible
    solitary routine. Care is unilateral contribution, not recipient consent.
    """
    aid=actor['id'];op=experience.get('own_action');clock=experience.get('clock')
    sel=experience.get('own_practical_selection') or {}
    refs=sel.get('selected_project_refs',[])
    partner=experience.get('reciprocated_partner')
    if (experience.get('actor')!=aid or (op not in ROUTINE_OPS and not (op in JOINT_ROUTINE_COMPLEMENTS and partner))
            or experience.get('status')!='PERFORMED'
            or experience.get('participated') is not True
            or type(clock) is not int or clock<0
            or sel.get('actor')!=aid
            or sel.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT'
            or len(refs)!=1 or sel.get('possible_end_trial') is not None):
        return None
    site=experience.get('location')
    if not isinstance(site,str) or not site:return None
    project=next((p for p in actor.get('projects',[]) if p['id']==refs[0]),None)
    if not project or project.get('status','active')!='active' or op not in project.get('means',[]):
        return None
    rows=[x for x in project.get('operational_history',[]) if x.get('event')==event_ref
          and x.get('operation')==op and x.get('performed_status')=='PERFORMED'
          and x.get('intent_attribution')=='ACTOR_POLICY_SELECTED_PROJECT_COURSE']
    if len(rows)!=1:return None
    if op=='WORK' and rows[0].get('objective_outcome')!='PRODUCED_GOODS_CONTROLLED_BY_OTHER':
        return None
    felt=experience.get('felt_enactment') or {}
    if felt.get('attempted_operation')!=op or felt.get('objective_result_not_inferred') is not True:
        return None
    recipient=(sel.get('world_request') or {}).get('addressed_party_ref')
    if partner is not None:
        # An actual independently selected addressed project and personally
        # encountered coactivity, not an invitation, presence or support label.
        if (op not in JOINT_ROUTINE_COMPLEMENTS or type(partner) is not str
                or partner==aid or recipient!=partner
                or project.get('addressed_party_ref')!=partner
                or not any(c.get('kind')=='coactor_present' and c.get('source_actor')==partner
                           for c in experience.get('perceived_cues',[]))):
            return None
    elif op in ('CARE','FEED'):
        if type(recipient) is not str or recipient==aid or project.get('addressed_party_ref')!=recipient:
            return None
    elif recipient is not None:return None
    origin=None
    if op=='FEED':
        if 'CARE' not in project.get('means',[]):return None
        feeds=[x for x in actor.get('performed_feeding_events',[])
               if x.get('event_ref')==event_ref and x.get('giver')==aid
               and x.get('recipient')==recipient and x.get('site')==site
               and x.get('original_action_was_actor_selected') is True]
        if len(feeds)!=1:return None
        origin=feeds[0].get('material_food_source')
        if origin not in ('GIVER_HELD_FOOD','MUTUAL_AID_FOOD','SHARED_SITE_FOOD'):return None
    return {'actor':aid,'project_ref':project['id'],'operation':op,'location':site,
            'recipient':recipient,'food_origin':origin,
            **({'coactivity_partner':partner} if partner else {}),'event_ref':event_ref,'experience_ref':experience['ref'],
            'clock':clock,'not_future_undertaking_or_observed_daily_history':True}


def possible_recurrent_routines(actor,experience,event_ref):
    """A repeated lived course licenses a bounded semantic nomination.

    It does not force the actor into a routine or infer future repetition.
    Distinct sources, same particular project/operation/site/recipient.
    Renewal needs fresh actual repetitions after the prior admission.
    """
    current=routine_exercise_receipt(actor,experience,event_ref)
    if current is None:return []
    project=next(p for p in actor['projects'] if p['id']==current['project_ref'])
    all_routines=[row for p in actor['projects'] for row in p.get('recurrent_routines',[])
                  if row.get('operation')==current['operation']]
    clock=current['clock']
    if any(x.get('through_clock',0)>clock for x in all_routines):return []
    last=max((x.get('admitted_clock',-1) for x in all_routines),default=-1)
    keys=('actor','project_ref','operation','location','recipient','food_origin')
    if current.get('coactivity_partner'):keys+=('coactivity_partner',)
    paths=actor.get('evidence_paths',[])
    prior=[]
    for path in reversed(paths):
        row=path.get('routine_exercise_analytic_only')
        if (not isinstance(row,dict) or not all(row.get(k)==current[k] for k in keys)
                or row.get('event_ref')!=path.get('event')
                or row.get('experience_ref')!=path.get('experience_ref')
                or type(row.get('clock')) is not int
                or not last<row['clock']<clock):
            continue
        event=row['event_ref']
        if not any(x.get('event')==event and x.get('operation')==current['operation']
                   and x.get('performed_status')=='PERFORMED'
                   and x.get('intent_attribution')=='ACTOR_POLICY_SELECTED_PROJECT_COURSE'
                   for x in project.get('operational_history',[])):
            continue
        if not any(x.get('event')==event and x.get('attempted_operation')==current['operation']
                   for x in project.get('lived_attempt_history',[])):
            continue
        if not any(x['event_ref']==event for x in prior):prior.append(row)
        if len(prior)==2:break
    if len(prior)<2:return []
    basis={k:current[k] for k in keys}
    basis.update({'exercises':copy(list(reversed(prior))+[current]),
                  'admission_event_ref':event_ref})
    return [{'kind':'ACQUIRE_RECURRENT_ROUTINE','basis':basis,
             'maximum_window_days':MAX_ROUTINE_WINDOW,
             'maximum_hours_per_active_day':4.,
             **({'maximum_food_units_per_active_day':1.} if current['operation']=='FEED' else {}),
             'not_actor_self_report_or_proof_of_future_repetition':True}]


def admit_recurrent_routine(actor,experience,event_ref,candidate):
    """Typed admission into the existing particular project, not a new psyche."""
    basis=candidate.get('basis')
    if not isinstance(basis,dict):raise ValueError('LIVED_ROUTINE_CANDIDATE_CONTRACT')
    fields={'kind','basis','window_days','hours_per_active_day','provisional_exposure_fraction'}
    if basis.get('operation')=='FEED':fields.add('food_units_per_active_day')
    if set(candidate)!=fields:raise ValueError('LIVED_ROUTINE_CANDIDATE_CONTRACT')
    if not any(x['basis']==basis for x in possible_recurrent_routines(actor,experience,event_ref)):
        raise ValueError('LIVED_ROUTINE_UNQUALIFIED_BASIS')
    days=candidate['window_days'];hours=candidate['hours_per_active_day']
    fraction=candidate['provisional_exposure_fraction']
    if (type(days) is not int or not 1<=days<=MAX_ROUTINE_WINDOW
            or type(hours) not in (int,float) or not isfinite(hours) or not 0<hours<=4
            or type(fraction) not in (int,float) or not isfinite(fraction) or not 0<fraction<=1):
        raise ValueError('LIVED_ROUTINE_UNQUALIFIED_DOSE')
    food=candidate.get('food_units_per_active_day')
    if food is not None and (type(food) not in (int,float) or not isfinite(food)
                              or not 0<food<=1 or round(food,5)!=food):
        raise ValueError('LIVED_ROUTINE_UNQUALIFIED_FOOD_DOSE')
    if basis['operation']=='FEED' and food is None:
        raise ValueError('LIVED_ROUTINE_UNQUALIFIED_FOOD_DOSE')
    project=next(p for p in actor['projects'] if p['id']==basis['project_ref'])
    clock=experience['clock']
    ref=stable_id('lived_routine',{'actor':actor['id'],'event':event_ref,'candidate':candidate})
    row={'id':ref,'actor':actor['id'],'project_ref':project['id'],
         'operation':basis['operation'],'location':basis['location'],
         'recipient':basis['recipient'],'food_origin':basis['food_origin'],
         **({'coactivity_partner':basis['coactivity_partner']} if basis.get('coactivity_partner') else {}),
         **({'food_units_per_active_day':food} if food is not None else {}),'admitted_clock':clock,'through_clock':clock+days,
         'hours_per_active_day':hours,'provisional_exposure_fraction':fraction,
         'basis':copy(basis),'grade':LIVED_CLASS,
         'future_coverage_requires_actual_qualification':True}
    project.setdefault('recurrent_routines',[]).append(row)
    return {'kind':'ACQUIRE_RECURRENT_ROUTINE','status':'ADMITTED_SOURCEFREE_FICTIONAL',
            'routine_ref':ref,'project_ref':project['id'],'grade':LIVED_CLASS}


def register_admitted_routine(world,actor,report,event_ref):
    """Register the exact admitted course in the EXISTING world source registry.

    Called inside the same runtime transaction, not from a visitor or external
    author API. The source asserts an aggregate research premise only.
    No new event, actor consent, institutional permission or witnessed day.
    """
    project=next((p for p in actor['projects'] if p['id']==report['project_ref']),None)
    rows=[] if project is None else [x for x in project.get('recurrent_routines',[])
                                      if x['id']==report['routine_ref']]
    if len(rows)!=1:raise ValueError('LIVED_ROUTINE_NO_ADMITTED_RECORD')
    row=rows[0];op=row['operation'];aid=actor['id'];site=row['location']
    if (row['basis']['admission_event_ref']!=event_ref or row['admitted_clock']!=world['clock']
            or world.get('positions',{}).get(aid)!=site
            or actor['location']!=site or op not in project.get('means',[])):
        raise ValueError('LIVED_ROUTINE_SOURCE_BOUNDARY_MISMATCH')
    if (op in ('CARE','FEED') or row.get('coactivity_partner')) and world.get('positions',{}).get(row['recipient'])!=site:
        raise ValueError('LIVED_ROUTINE_CARE_RECIPIENT_NOT_PRESENT')
    ref=row['id']
    registry=world.setdefault('routine_source_registry',{})
    if ref in registry:raise ValueError('LIVED_ROUTINE_DUPLICATE_SOURCE')
    process={'kind':ROUTINE_OPS.get(op,'QUALIFIED_ROUTINE_PRACTICE'),'actor':aid,'location':site,'source_ref':ref,
             'routine_project_ref':project['id'],'hours_per_active_day':row['hours_per_active_day'],
             'provisional_exposure_fraction':row['provisional_exposure_fraction']}
    if row.get('coactivity_partner'):process['coactivity_partner']=row['coactivity_partner']
    if op in ('CARE','FEED'):process['recipient']=row['recipient']
    if op=='FEED':process.update({'supply_origin':row['food_origin'],
                            'food_units_per_active_day':row['food_units_per_active_day']})
    if process['kind']=='QUALIFIED_ROUTINE_PRACTICE':
        process.update({'operation':op,'mode':'SOLO_COMPONENT_PRACTICE'})
        if row.get('coactivity_partner'):
            process.update({'mode':'RECIPROCAL_COMPONENT_PRACTICE',
                            'coactivity_partner':row['coactivity_partner']})
    record={'id':ref,'actor':aid,'location':site,'kind':process['kind'],
            'from_clock':row['admitted_clock'],'through_clock':row['through_clock'],
            'max_hours_per_active_day':row['hours_per_active_day'],
            'description':'Bounded actor-history-conditioned ordinary-life premise',
            'evidence_class':LIVED_CLASS,'process':process,'operation':op,
            'admission_event_ref':event_ref,
            'basis_event_refs':[x['event_ref'] for x in row['basis']['exercises']],
            'registered_at_world_clock':world['clock'],
            'not_observed_daily_events':True,'coactor_willingness_not_proved':True,
            'does_not_authorize_PYAT_source_or_native_psyche':True,
            'no_actual_history_until_qualified_period_executed':True,'grade':GRADE}
    registry[ref]=record
    return ref


def acquired_routine_processes(world):
    """Read bounded future/active premises from the existing source registry."""
    clock=world['clock']
    return [copy(x['process']) for _,x in sorted(world.get('routine_source_registry',{}).items())
            if x.get('evidence_class')==LIVED_CLASS and x.get('through_clock',0)>clock]


def live_routine_situational_reason(world,actors,process):
    """Check exact continuing project, body and institutional circumstances.

    The existing aggregate allocator still owns all time, labor and material
    settlement. A withheld premise is neither a failure experienced by its
    actor nor an assertion that future relief or consent is impossible.
    """
    row=world['routine_source_registry'][process['source_ref']]
    if row['evidence_class']!=LIVED_CLASS:return None
    a=actors[process['actor']];op=row['operation']
    matches=[p for p in a.get('projects',[]) if p['id']==process['routine_project_ref']]
    if len(matches)!=1:return 'PARTICULAR_PROJECT_NOT_AVAILABLE'
    project=matches[0]
    if project.get('status','active')!='active' or op not in project.get('means',[]):
        return 'PARTICULAR_PROJECT_NO_LONGER_RECRUITS_OPERATION'
    receipts=[x for x in project.get('recurrent_routines',[]) if x.get('id')==row['id']]
    if (len(receipts)!=1 or receipts[0]['through_clock']!=row['through_clock']
            or receipts[0]['basis']['admission_event_ref']!=row['admission_event_ref']):
        raise ValueError('LIVED_ROUTINE_ACTOR_WORLD_SOURCE_DIVERGENCE')
    if receipts[0].get('revisions',[])!=row.get('revisions',[]):
        raise ValueError('LIVED_ROUTINE_REVISION_ACTOR_WORLD_DIVERGENCE')
    if row.get('revisions'):
        state=row['revisions'][-1]['effective_dose']['state']
        if state!='ACTIVE':return 'ACTOR_ROUTINE_'+state
    if row['process'].get('coactivity_partner'):
        if project.get('addressed_party_ref')!=row['process']['coactivity_partner']:
            return 'PARTICULAR_COACTIVITY_COUNTERPART_CHANGED'
    if op in ('CARE','FEED') and project.get('addressed_party_ref')!=process.get('recipient'):
        return 'PARTICULAR_CARE_RECIPIENT_CHANGED'
    if op=='WORK':
        from .labor_dependency import work_permission
        permission=work_permission(world,a['id'],process['location'])
        if permission not in ('QUALIFIED_WORK_CONTRACT_ACTIVE','NO_ADDITIONAL_CONTRACT_REGIME'):
            # The current world work owner determines the same permission.
            # An absent/unqualified contract cannot be supplied by a routine.
            return 'CURRENT_WORK_PERMISSION_NOT_QUALIFIED:'+str(permission)
    return None


def lived_work_permission_boundaries(world,actor,site,start,end):
    """The existing wage-regime owner's inclusive sanctions are temporal facts.

    Only actual permission changes at known boundaries matter. This avoids
    assuming access over a compressed span merely because work was possible
    at its first instant. No new institution or actor interpretation.
    """
    from .labor_dependency import work_permission
    regime=world.get('work_regimes',{}).get(site)
    if not regime:return []
    times=set()
    for item in regime.get('suspensions',[]):
        if item.get('worker')==actor:
            for t in (item.get('start_clock'),item.get('through_clock',-1)+1):
                if type(t) is int and start<t<=end:times.add(t)
    return [t for t in sorted(times)
            if work_permission({**world,'clock':t-1},actor,site)!=
               work_permission({**world,'clock':t},actor,site)]


def effective_routine_dose(row):
    """Derive continuing dose without overwriting the original source."""
    revisions=row.get('revisions',[])
    if revisions:return copy(revisions[-1]['effective_dose'])
    return {'state':'ACTIVE','hours_per_active_day':row['hours_per_active_day'],
            'provisional_exposure_fraction':row['provisional_exposure_fraction'],
            **({'food_units_per_active_day':row['food_units_per_active_day']}
               if row['operation']=='FEED' else {})}


def possible_routine_revisions(actor,experience,event_ref):
    """Actual current lived occasion, optional reconstitution of own routine.

    No analyst-only absence, hidden resource fact or other person's motive
    may be installed as a reason. The actor's own embodied attempt, explicit
    selection and personally received directed act are distinct witnesses.
    The semantic proposal can alter a prospective modeled dose, not the past.
    """
    from .attention_field import personally_received_directed_act
    aid=actor['id'];clock=experience.get('clock')
    if experience.get('actor')!=aid or type(clock) is not int:return []
    paths=[p for p in actor.get('evidence_paths',[])
           if p.get('event')==event_ref and p.get('experience_ref')==experience.get('ref')]
    if len(paths)!=1:return []
    path=paths[0];site=experience.get('location')
    selected=experience.get('own_practical_selection') or {}
    own=experience.get('own_action')
    felt=experience.get('felt_enactment') or {}
    own_witness=(selected.get('status')=='ACTOR_POLICY_PRACTICAL_ATTEMPT'
                 and selected.get('actor')==aid
                 and experience.get('participated') is True
                 and own==felt.get('attempted_operation')
                 and felt.get('objective_result_not_inferred') is True
                 and own==path.get('own_action')
                 and selected.get('option_id')==path.get('practical_option_ref')
                 and selected.get('possible_end_trial') is None)
    directed=personally_received_directed_act(experience)
    if directed and directed!=path.get('directed_encounter'):directed=None
    if not own_witness and not directed:return []
    out=[]
    for project in actor.get('projects',[]):
        for row in project.get('recurrent_routines',[]):
            if (row.get('actor')!=aid or row.get('project_ref')!=project['id']
                    or row.get('admitted_clock',clock)>=clock
                    or row.get('through_clock',0)<=clock
                    or row.get('location')!=site):continue
            if any(x.get('event_ref')==event_ref for x in row.get('revisions',[])):continue
            dose=effective_routine_dose(row)
            if dose['state']=='RETIRED':continue
            # Do not make every observed micro-event a general review of
            # every historical routine. A directed act must concern the
            # actual counterpart; an own attempt is a present lived choice.
            if not own_witness and (not directed or directed['counterpart_ref']!=row.get('recipient')):
                continue
            basis={'actor':aid,'routine_ref':row['id'],'project_ref':project['id'],
                   'operation':row['operation'],'location':site,'event_ref':event_ref,
                   'experience_ref':experience['ref'],'clock':clock,
                   'prior_revision_ref':row.get('revisions',[{}])[-1].get('id') if row.get('revisions') else None,
                   'prior_effective_dose':dose,
                   'recent_modeled_own_course_analytic_only':copy(row.get('modeled_course_receipts',[])[-3:]),
                   'own_attempt':({'operation':own,'status':experience.get('status'),
                                    'selected_project_refs':copy(selected.get('selected_project_refs',[])),
                                    'option_ref':selected.get('option_id')} if own_witness else None),
                   'received_directed_act':copy(directed) if directed else None}
            modes=['RETIRE','RESUME'] if dose['state']=='PAUSED' else ['PAUSE','RETIRE','RESIZE']
            out.append({'kind':'REVISE_RECURRENT_ROUTINE','basis':basis,'allowed_modes':modes,
                        'original_ceiling':effective_routine_dose({k:v for k,v in row.items() if k!='revisions'}),
                        'through_clock':row['through_clock'],
                        'not_conscious_self_report_or_proof_of_future_action':True})
    return out[:16]


def admit_routine_revision(actor,experience,event_ref,candidate):
    offers=possible_routine_revisions(actor,experience,event_ref)
    q=next((x for x in offers if x['basis']==candidate.get('basis')),None)
    if q is None:raise ValueError('LIVED_ROUTINE_REVISION_UNQUALIFIED_BASIS')
    mode=candidate.get('mode')
    if mode not in q['allowed_modes']:raise ValueError('LIVED_ROUTINE_REVISION_INVALID_MODE')
    fields={'kind','basis','mode','interpretive_hypothesis'}
    prior=copy(q['basis']['prior_effective_dose'])
    ceiling=q['original_ceiling']
    meaning=candidate.get('interpretive_hypothesis')
    if type(meaning) is not str or not meaning.strip() or len(meaning)>512:
        raise ValueError('LIVED_ROUTINE_REVISION_INVALID_MEANING')
    if mode=='RESIZE':
        fields.add('dose')
        dose=candidate.get('dose')
        expected={k for k in ceiling if k!='state'}
        if type(dose) is not dict or set(dose)!=expected:
            raise ValueError('LIVED_ROUTINE_REVISION_INVALID_DOSE')
        for k,v in dose.items():
            if type(v) not in (int,float) or not isfinite(v) or not 0<v<=ceiling[k]:
                raise ValueError('LIVED_ROUTINE_REVISION_INVALID_DOSE')
            if k=='food_units_per_active_day' and round(v,5)!=v:
                raise ValueError('LIVED_ROUTINE_REVISION_INVALID_DOSE')
        effective={'state':'ACTIVE',**copy(dose)}
        if effective==prior:raise ValueError('LIVED_ROUTINE_REVISION_NO_CHANGE')
    else:
        effective={**prior,'state':{'PAUSE':'PAUSED','RESUME':'ACTIVE','RETIRE':'RETIRED'}[mode]}
    if set(candidate)!=fields:raise ValueError('LIVED_ROUTINE_REVISION_INVALID_FIELDS')
    basis=q['basis'];project=next(p for p in actor['projects'] if p['id']==basis['project_ref'])
    row=next(x for x in project['recurrent_routines'] if x['id']==basis['routine_ref'])
    revision={'id':stable_id('routine_revision',{'event':event_ref,'candidate':candidate}),
              'event_ref':event_ref,'clock':experience['clock'],'mode':mode,
              'basis':copy(basis),'effective_dose':effective,
              'interpretive_hypothesis':meaning,'not_retroactive_or_actor_self_report':True}
    row.setdefault('revisions',[]).append(revision)
    return {'kind':'REVISE_RECURRENT_ROUTINE','status':'ADMITTED_SOURCEFREE_FICTIONAL',
            'routine_ref':row['id'],'project_ref':project['id'],'revision_ref':revision['id'],
            'grade':LIVED_CLASS}


def register_routine_revision(world,actor,report,event_ref):
    """Atomic existing world registry projection; retain original process."""
    p=next((p for p in actor['projects'] if p['id']==report['project_ref']),None)
    row=next((x for x in (p or {}).get('recurrent_routines',[])
              if x['id']==report['routine_ref']),None)
    src=world.get('routine_source_registry',{}).get(report['routine_ref'])
    if row is None or src is None or src.get('actor')!=actor['id'] or src.get('evidence_class')!=LIVED_CLASS:
        raise ValueError('LIVED_ROUTINE_REVISION_SOURCE_MISMATCH')
    rev=row['revisions'][-1]
    if (rev['id']!=report['revision_ref'] or rev['event_ref']!=event_ref
            or rev['clock']!=world['clock']
            or src.get('revisions',[])!=row['revisions'][:-1]):
        raise ValueError('LIVED_ROUTINE_REVISION_HISTORY_MISMATCH')
    # This is internal analyst provenance, not a new visible actor cue.
    src.setdefault('revisions',[]).append(copy(rev))
    return src['id']


def realized_lived_process(world,process):
    """Use only current admitted dose, AFTER original process verification.

    The original source may be supplied by an explicit caller, but the
    caller cannot restore a suspended/retired routine or its old dose.
    """
    source=world['routine_source_registry'][process['source_ref']]
    if source.get('evidence_class')!=LIVED_CLASS or not source.get('revisions'):
        return process
    revision=source['revisions'][-1]
    dose=revision['effective_dose']
    if dose['state']!='ACTIVE':raise ValueError('LIVED_ROUTINE_INACTIVE_REALIZATION')
    return {**process,**{k:v for k,v in dose.items() if k!='state'},
            'routine_revision_ref':revision['id']}


def conserve_routine_period(world,actors,period,allocation):
    """Retain actor-local references to actual aggregate coverage and costs.

    This is a compact derived analytic carrier on the existing acquired
    routine, not a second history or a recollection of daily activity.
    Do not assign another's nutrition, private account or objective reason
    for withholding to this actor's conscious evidence. The full receipt
    remains in the existing world history.
    """
    registry=world.get('routine_source_registry',{})
    start=period['start'];end=period['end']
    held=[x for key in ('structurally_withheld_processes','bodily_withheld_processes',
                        'situationally_withheld_processes')
          for x in allocation.get(key,[])]
    effective={x['source_ref']:x for x in period['processes']
               if isinstance(x,dict) and x.get('source_ref') in registry
               and registry[x['source_ref']].get('evidence_class')==LIVED_CLASS}
    refs=set(effective)|{x['source_ref'] for x in held
                         if registry.get(x.get('source_ref'),{}).get('evidence_class')==LIVED_CLASS}
    for ref in sorted(refs):
        source=registry[ref];aid=source['actor'];proc=source['process']
        actor=actors[aid]
        p=next((x for x in actor.get('projects',[]) if x['id']==proc['routine_project_ref']),None)
        rows=[] if p is None else [x for x in p.get('recurrent_routines',[]) if x['id']==ref]
        if len(rows)!=1:
            # A missing project is a qualified withholding, not evidence
            # of a surviving actor-owned routine to which to attach receipt.
            if ref in effective:raise ValueError('LIVED_ROUTINE_EFFECT_WITHOUT_ACTOR_SOURCE')
            continue
        row=rows[0];actual=effective.get(ref)
        receipt={'period_ref':period['id'],'allocation_ref':allocation['id'],
                 'from_clock':start,'through_clock':end,
                 'coverage':'AGGREGATE_MODELED' if actual else 'NOT_QUALIFIED_FOR_MODELED_COVERAGE',
                 'own_modeled_hours':round((end-start)*actual['hours_per_active_day']*
                                    actual['provisional_exposure_fraction'],5) if actual else 0.,
                 'routine_revision_ref':(actual or {}).get('routine_revision_ref'),
                 'not_individual_experience_or_conscious_reason':True}
        if actual:
            own_refs=[]
            for key in ('reproductive_labor_periods','wage_labor_periods','material_provisioning_periods'):
                for effect in reversed(world.get(key,[])):
                    if effect.get('end_clock',-1)<end:break
                    if effect.get('source_ref')!=ref or effect.get('end_clock')!=end:continue
                    if effect.get('giver',effect.get('worker'))!=aid:continue
                    own_refs.append(effect['id'])
                    if key=='wage_labor_periods':
                        receipt['own_wage_paid_model']=effect['actual_paid_model']
                        receipt['own_wage_arrears_model']=effect['wage_arrears']
                        receipt['own_work_rest_expenditure_model']=effect['worker_rest_expenditure_model']
                    elif key=='reproductive_labor_periods':
                        receipt['own_nominal_care_rest_expenditure_model']=effect['giver_rest_expenditure_model']
                    elif key=='material_provisioning_periods':
                        receipt['own_provisioning_food_contribution_model']=effect['consumed_food_units']
            own_refs.extend(x['id'] for x in actor.get('practice_exposures',[])
                            if x.get('source_ref')==ref and x.get('end_clock')==end)
            receipt['own_aggregate_effect_refs']=own_refs
        records=row.setdefault('modeled_course_receipts',[])
        if any(x.get('period_ref')==period['id'] for x in records):
            raise ValueError('LIVED_ROUTINE_DUPLICATE_PERIOD_RECEIPT')
        records.append(receipt)


def match_reciprocal_routine_claims(world,claims):
    """Match independently admitted present claims, not a third collective will.

    Input claims have already passed exact source, actor, body, location,
    material and prospective revision qualification. Two separate actor-local
    admissions must derive from the same three actual shared event identities.
    Common coverage is conservatively bounded by BOTH doses; surplus is
    unmodeled. No repeated individual consent or daily scene is reconstructed.
    Returns per-index effective process replacements and withheld reasons.
    """
    registry=world.get('routine_source_registry',{})
    joint={i:raw for i,raw,lived,_ in claims
           if lived and raw.get('coactivity_partner')}
    matched={};held={}
    edges={}
    for i,a in joint.items():
        sa=registry[a['source_ref']]
        options=[]
        for j,b in joint.items():
            if j==i:continue
            sb=registry[b['source_ref']]
            # CARE and FEED are typed material process kinds; only practice
            # carries an operation field. Use the exact admitted source.
            if (b['actor']!=a['coactivity_partner'] or b['coactivity_partner']!=a['actor']
                    or a['location']!=b['location']
                    or sb['operation'] not in JOINT_ROUTINE_COMPLEMENTS.get(sa['operation'],set())
                    or sa['operation'] not in JOINT_ROUTINE_COMPLEMENTS.get(sb['operation'],set())):
                continue
            common=sorted(set(sa['basis_event_refs']) & set(sb['basis_event_refs']))
            if len(common)>=3:options.append((j,common))
        edges[i]=options
    for i,a in sorted(joint.items()):
        if i in matched:continue
        if len(edges[i])!=1:
            held[i]='NO_UNAMBIGUOUS_INDEPENDENT_RECIPROCAL_ROUTINE';continue
        j,common=edges[i][0];b=joint[j]
        # Both degrees computed on the original graph, not a graph shrunk
        # by iteration order. An ambiguous source cannot become eligible
        # merely because a competitor was withheld first.
        if len(edges[j])!=1 or edges[j][0][0]!=i:
            held[i]='NO_UNAMBIGUOUS_INDEPENDENT_RECIPROCAL_ROUTINE';continue
        hours=min(a['hours_per_active_day'],b['hours_per_active_day'])
        fraction=min(a['provisional_exposure_fraction'],b['provisional_exposure_fraction'])
        pair=stable_id('reciprocal_routine_pair',{'sources':sorted([a['source_ref'],b['source_ref']]),
                                                 'shared_exercises':common})
        for k,own,other in ((i,a,b),(j,b,a)):
            matched[k]={**own,'hours_per_active_day':hours,'provisional_exposure_fraction':fraction,
                        'reciprocal_routine_pair_ref':pair,
                        'matched_counterpart_source_ref':other['source_ref'],
                        'unmatched_own_claim_hours_per_day':round(
                            own['hours_per_active_day']*own['provisional_exposure_fraction']-hours*fraction,5),
                        'not_future_individual_assent_or_synchronized_daily_occurrence':True}
    for i in joint:
        if i not in matched:held.setdefault(i,'NO_UNAMBIGUOUS_INDEPENDENT_RECIPROCAL_ROUTINE')
    return matched,held
