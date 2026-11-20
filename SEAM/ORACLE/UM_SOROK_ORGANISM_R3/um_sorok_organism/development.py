"""Research-only psychological afterlife: typed *fictional* formation and rewiring.

This is not CAN/ADP native authority. Every admitted form is actor-specific, bound
by actual experienced event, scoped, graded, and revisable. No LLM may edit an
objective world fact or another actor's state here.
"""
from .types import stable_id, copy, GRADE
from .psychodynamics import validate_tendencies
from .organism import ACTIONS
import math

class InvalidDevelopment(ValueError): pass


def _text_list(value, error):
    if not isinstance(value,list) or any(not isinstance(x,str) for x in value):
        raise InvalidDevelopment(error)
    return value

ALLOWED={'ADD_FORM','LINK_FORMS','DIFFERENTIATE','CHANGE_RECRUITMENT_SCOPE',
         'CHANGE_STRENGTH','SET_DORMANT','REACTIVATE','REORGANIZE_PROJECT',
         'TRACE','MEMORY','ACTOR_SELF_MODEL','ADD_PROJECT','CHANGE_OTHER_MODEL','LINK_ACTIVITY',
         'ACQUIRE_COMPOSITION_METHOD','NO_CHANGE'}
KINDS={'MEDIATOR','TENSION','PRACTICE','EXPECTATION','DISCRIMINATION','RELATIONAL_INVESTMENT'}
RELATIONS={'RECRUITS','SUPPORTS','INHIBITS','COMPETES','DERIVED_FROM','CONTRADICTS'}


def validate_activity_priority(value):
    # Project importance is deliberately NOT capped at 1: existing acquired
    # purposes may have intense salience. It must, however, be a finite,
    # nonnegative number or it corrupts situated ranking and possibility.
    if (isinstance(value,bool) or not isinstance(value,(int,float)) or
            not math.isfinite(value) or value<0):
        raise InvalidDevelopment('INVALID_ACTIVITY_PRIORITY')
    return value


def admit(actor,experience,event_ref,candidates):
    """All-or-nothing psychic admission even for a multi-effect LLM proposal.

    Caller owns an actor object whose identity may be held elsewhere. Validate
    and apply on a detached candidate, then replace content only after every
    operation succeeds. A later rejected effect cannot leave an earlier
    proposed memory, project, or relationship silently installed.
    """
    candidate_actor=copy(actor)
    result=_admit_in_place(candidate_actor,experience,event_ref,candidates)
    actor.clear()
    actor.update(candidate_actor)
    return result


def _admit_in_place(actor,experience,event_ref,candidates):
    """Mutates only the stage copy; caller commits atomically with world.

    A proposal is admissible only after an event actually occurred to which the
    actor had a qualified exposure. This is *fictional sourcefree* admission,
    not validation of an empirical human-learning law.
    """
    if experience.get('actor')!=actor['id'] or not event_ref:
        raise InvalidDevelopment('ACTOR_OR_EVENT_IDENTITY_MISMATCH')
    if not experience.get('participated') and not experience.get('perceived_cues'):
        if candidates: raise InvalidDevelopment('NO_ACTOR_EXPERIENCE')
    report=[]
    for idx,c in enumerate(candidates):
        op=c.get('kind')
        if op not in ALLOWED: raise InvalidDevelopment('UNKNOWN_PSYCHIC_OPERATION')
        if op=='NO_CHANGE':report.append({'kind':op,'status':'VALID_NO_CHANGE'});continue
        evidence={'event':event_ref,'actor':actor['id'],'experience_ref':experience['ref'],
                  'grade':GRADE,'semantic_hypothesis':True}
        if op in ('ADD_FORM','DIFFERENTIATE'):
            form=copy(c.get('form',{}))
            if form.get('kind') not in KINDS or not form.get('cues') or not isinstance(form.get('enables',[]),list):
                raise InvalidDevelopment('FORM_UNQUALIFIED')
            ident=form.get('id') or stable_id('form',{'actor':actor['id'],'event':event_ref,'index':idx,'content':form})
            if ident in actor['forms']:raise InvalidDevelopment('DUPLICATE_FORM_ID')
            validate_tendencies(form)
            if any(not isinstance(op,str) or op not in ACTIONS for op in form.get('enables',[])):
                raise InvalidDevelopment('UNSUPPORTED_ACQUIRED_OPERATION')
            form.update({'id':ident,'actor':actor['id'],'origin':[event_ref],
                         'grade':GRADE,'lifecycle':form.get('lifecycle','ACTIVE'),
                         'evidence':evidence})
            form.setdefault('scope',{})
            form.setdefault('access','tacit')
            form.setdefault('strength',.4)
            form.setdefault('body_min',0)
            actor['forms'][ident]=form
            report.append({'kind':op,'form':ident,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='LINK_FORMS':
            a,b=c.get('source'),c.get('target')
            if a not in actor['forms'] or b not in actor['forms'] or c.get('relation') not in RELATIONS:
                raise InvalidDevelopment('UNRESOLVED_LINK')
            _text_list(c.get('contexts',[]),'INVALID_LINK_CONTEXTS')
            link={'source':a,'target':b,'relation':c['relation'],
                  'contexts':c.get('contexts',[]),'origin':[event_ref],
                  'evidence':evidence,'grade':GRADE}
            if link not in actor['links']:actor['links'].append(link)
            report.append({'kind':op,'from':a,'to':b,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='LINK_ACTIVITY':
            src,dst=c.get('source'),c.get('target')
            if src not in actor['forms'] or not any(p['id']==dst for p in actor['projects']):
                raise InvalidDevelopment('UNQUALIFIED_ACTIVITY_LINK')
            _text_list(c.get('contexts',[]),'INVALID_LINK_CONTEXTS')
            link={'source':src,'target':dst,'relation':'RECRUITS_ACTIVITY',
                  'contexts':c.get('contexts',[]),'origin':[event_ref],
                  'evidence':evidence,'grade':GRADE}
            if link not in actor.setdefault('activity_links',[]):actor['activity_links'].append(link)
            report.append({'kind':op,'form':src,'activity':dst,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='ACQUIRE_COMPOSITION_METHOD':
            # Not a pre-installed mature faculty: a proposed new organizing
            # *method* needs actual actor-performed practice now and historically
            # acquired, separately identified means to compose. The inference
            # remains fictional / underdetermined rather than an empirical law.
            refs=c.get('source_forms');operations=c.get('operations')
            if (not isinstance(refs,list) or len(set(refs))!=2 or
                len(refs)!=2 or any(x not in actor['forms'] for x in refs)):
                raise InvalidDevelopment('COMPOSITION_NEEDS_TWO_ACQUIRED_FORMS')
            if (not isinstance(operations,list) or len(operations)!=2 or
                len(set(operations))!=2 or any(x not in ACTIONS for x in operations)):
                raise InvalidDevelopment('COMPOSITION_NOT_AN_EXISTING_TWO_MEANS')
            if not all(actor['forms'][x].get('origin') for x in refs):
                raise InvalidDevelopment('COMPOSITION_MISSING_PRACTICE_HISTORY')
            if not all(any(x in actor['forms'][fid].get('enables',[]) for fid in refs)
                       for x in operations):
                raise InvalidDevelopment('COMPOSITION_MEANS_NOT_PRACTICED')
            enacted=experience.get('felt_enactment') or {}
            if (not experience.get('participated') or experience.get('status')!='PERFORMED' or
                    enacted.get('attempted_operation') not in operations):
                raise InvalidDevelopment('COMPOSITION_NEEDS_OWN_PERFORMED_ENCOUNTER')
            if not isinstance(c.get('hypothesized_end'),str) or not c['hypothesized_end']:
                raise InvalidDevelopment('COMPOSITION_END_UNSPECIFIED')
            locs=c.get('locations',[])
            if not isinstance(locs,list) or not all(isinstance(x,str) for x in locs):
                raise InvalidDevelopment('INVALID_COMPOSITION_SCOPE')
            ident=stable_id('method',{'actor':actor['id'],'event':event_ref,'index':idx,
              'forms':sorted(refs),'operations':operations,'end':c['hypothesized_end']})
            rule={'id':ident,'source_forms':copy(refs),'operations':copy(operations),
                'hypothesized_end':c['hypothesized_end'],'locations':copy(locs),
                'status':'ACTIVE','origin':[event_ref],'experience_ref':experience['ref'],
                'grade':GRADE,'meaning':'FICTIONAL_PROVISIONAL_ACQUIRED_METHOD',
                'no_inference_of_real_human_learning_law':True}
            actor.setdefault('composition_methods',[]).append(rule)
            report.append({'kind':op,'method':ident,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='CHANGE_RECRUITMENT_SCOPE':
            ident=c.get('form_id')
            if ident not in actor['forms']:raise InvalidDevelopment('UNKNOWN_FORM')
            new_scope=c.get('new_scope')
            if not isinstance(new_scope,dict):raise InvalidDevelopment('BAD_SCOPE')
            # Scope membership must be typed: a string is a substring matcher,
            # not a list of established context locations.
            validate_tendencies({'scope':new_scope})
            form=actor['forms'][ident]
            form.setdefault('prior_scopes',[]).append({'scope':copy(form.get('scope',{})),'event':event_ref})
            form['scope']=copy(new_scope)
            form.setdefault('changes',[]).append(evidence)
            report.append({'kind':op,'form':ident,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='CHANGE_STRENGTH':
            ident=c.get('form_id')
            if ident not in actor['forms']:raise InvalidDevelopment('UNKNOWN_FORM')
            delta=c.get('delta',0)
            if (isinstance(delta,bool) or not isinstance(delta,(int,float))
                    or not math.isfinite(delta) or abs(delta)>.35):
                raise InvalidDevelopment('UNBOUNDED_STRENGTH')
            f=actor['forms'][ident];f['strength']=round(min(1,max(0,f.get('strength',.4)+delta)),4)
            f.setdefault('changes',[]).append(evidence)
            report.append({'kind':op,'form':ident,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op in ('SET_DORMANT','REACTIVATE'):
            ident=c.get('form_id')
            if ident not in actor['forms']:raise InvalidDevelopment('UNKNOWN_FORM')
            actor['forms'][ident]['lifecycle']='DORMANT' if op=='SET_DORMANT' else 'ACTIVE'
            actor['forms'][ident].setdefault('changes',[]).append(evidence)
            report.append({'kind':op,'form':ident,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='ADD_PROJECT':
            project=copy(c.get('project',{}))
            if not project.get('object') or not isinstance(project.get('means'),list):
                raise InvalidDevelopment('INVALID_NEW_PROJECT')
            if any(not isinstance(op,str) or op not in ACTIONS for op in project['means']):
                raise InvalidDevelopment('UNSUPPORTED_ACTIVITY_MEANS')
            validate_activity_priority(project.get('priority',.4))
            if 'contextual_only' in project and type(project['contextual_only']) is not bool:
                raise InvalidDevelopment('INVALID_PROJECT_CONTEXTUAL_FLAG')
            _text_list(project.get('cue_terms',[]),'INVALID_PROJECT_CUE_TERMS')
            ident=project.get('id') or stable_id('project',{'actor':actor['id'],'event':event_ref,'index':idx})
            if any(p['id']==ident for p in actor['projects']):
                raise InvalidDevelopment('DUPLICATE_PROJECT')
            project.update({'id':ident,'origin':[event_ref],'grade':GRADE})
            project.setdefault('motive','UNSPECIFIED_ACQUIRED_MOTIVE')
            project.setdefault('status','active')
            project.setdefault('priority',.4)
            project.setdefault('cue_terms',[])
            actor['projects'].append(project)
            report.append({'kind':op,'project':ident,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='REORGANIZE_PROJECT':
            ident=c.get('project_id')
            project=next((p for p in actor['projects'] if p['id']==ident),None)
            if project is None:raise InvalidDevelopment('UNKNOWN_PROJECT')
            if 'means' in c and (not isinstance(c['means'],list) or not all(isinstance(x,str) for x in c['means'])):
                raise InvalidDevelopment('INVALID_PROJECT_MEANS')
            if 'means' in c and any(x not in ACTIONS for x in c['means']):
                raise InvalidDevelopment('UNSUPPORTED_ACTIVITY_MEANS')
            if 'priority' in c:validate_activity_priority(c['priority'])
            if 'contextual_only' in c and type(c['contextual_only']) is not bool:
                raise InvalidDevelopment('INVALID_PROJECT_CONTEXTUAL_FLAG')
            if 'cue_terms' in c:_text_list(c['cue_terms'],'INVALID_PROJECT_CUE_TERMS')
            for field in ('priority','means','object','motive','status','cue_terms','contextual_only'):
                if field in c:project[field]=copy(c[field])
            project.setdefault('history',[]).append(evidence)
            report.append({'kind':op,'project':ident,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op in ('TRACE','MEMORY'):
            _text_list(c.get('cue_terms',[]),'INVALID_TRACE_CUES')
            ref=stable_id('trace' if op=='TRACE' else 'memory',{'actor':actor['id'],'event':event_ref,'index':idx})
            entry={'id':ref,'origin':[event_ref],'experience':experience['ref'],
                   'grade':GRADE,'status':'NONDECLARATIVE' if op=='TRACE' else 'ACTOR_ACCESSIBLE',
                   'cue_terms':c.get('cue_terms',[]),'content':c.get('content',''),
                   'manifestation':c.get('manifestation','uninterpreted')}
            actor['traces' if op=='TRACE' else 'memories'].append(entry)
            report.append({'kind':op,'ref':ref,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='CHANGE_OTHER_MODEL':
            # What this actor expects of the Other is not the Other's actual state.
            other=c.get('other_ref')
            if not isinstance(other,str) or not other or other==actor['id']:
                raise InvalidDevelopment('INVALID_OTHER_REFERENCE')
            if experience.get('reciprocated_partner')!=other:
                raise InvalidDevelopment('OTHER_NOT_ENCOUNTERED_IN_THIS_EXPERIENCE')
            if not isinstance(c.get('hypothesis'),str) or not c.get('hypothesis'):
                raise InvalidDevelopment('EMPTY_RELATIONAL_HYPOTHESIS')
            actor['other_models'].setdefault(other,[]).append({
                'hypothesis':c['hypothesis'],'event':event_ref,
                'confidence':c.get('confidence','tentative'),
                'grade':GRADE,'not_other_objective_truth':True})
            report.append({'kind':op,'other_ref':other,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='ACTOR_SELF_MODEL':
            if actor['body']['language']<.25:raise InvalidDevelopment('NO_REFLECTIVE_SELF_MODEL_CAPACITY')
            actor['self_model'].setdefault('hypotheses',[]).append({'claim':c.get('claim',''),
                'confidence':c.get('confidence','uncertain'), 'origin':[event_ref], 'grade':GRADE})
            report.append({'kind':op,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
    actor.setdefault('history_refs',[]).append(event_ref)
    return report


def recurring_provisional_growth(actor,period_ref,processes):
    """Admit only actor-addressed coarse-life effects, all-or-nothing.

    Modelled coverage is NOT an individual experience and may not rewrite a
    different actor merely because they possess the same reusable form ID.
    A modeled scope generalization is not an observed microepisode or a law.
    """
    staged=copy(actor)
    outputs=[]
    if not isinstance(processes,list):
        raise InvalidDevelopment('INVALID_PERIOD_PROCESSES')
    for proc in processes:
        if not isinstance(proc,dict):
            raise InvalidDevelopment('INVALID_PERIOD_PROCESS')
        if proc.get('kind')!='practice_access' or proc.get('coverage')!='AGGREGATE_MODELED':
            continue
        if proc.get('warrants_scope_change') is not True:
            continue
        # A global, unqualified activity-coverage capsule is not a licence to
        # generalize every similarly named learned form in all family members.
        claimed_actor=proc.get('actor_id')
        if not isinstance(claimed_actor,str) or not claimed_actor:
            raise InvalidDevelopment('PERIOD_PRACTICE_REQUIRES_ACTOR')
        if claimed_actor!=staged['id']:
            continue
        fid=proc.get('form_id')
        if not isinstance(fid,str) or not fid:
            raise InvalidDevelopment('INVALID_PERIOD_FORM_REF')
        if fid not in staged['forms']:
            # Evidence for an unowned form does not fabricate that form.
            continue
        locations=proc.get('locations',[])
        if (not isinstance(locations,list) or
                any(not isinstance(place,str) or not place for place in locations)):
            raise InvalidDevelopment('INVALID_PERIOD_LOCATIONS')
        form=staged['forms'][fid]
        old=copy(form.get('scope',{}))
        try:
            validate_tendencies({'scope':old})
        except ValueError as exc:
            raise InvalidDevelopment('INVALID_PRIOR_FORM_SCOPE') from exc
        old_locations=old.get('locations',[])
        novel=sorted(set(old_locations)|set(locations))
        if set(novel)==set(old_locations):
            # Period occurred, but the actor's recruitment did not change.
            continue
        form['scope']={**old,'locations':novel}
        form.setdefault('changes',[]).append({'period':period_ref,'grade':GRADE,
            'type':'AGGREGATE_MODELED_SCOPE_GENERALIZATION'})
        outputs.append({'kind':'PERIOD_SCOPE_CHANGE','form':fid})
    actor.clear()
    actor.update(staged)
    return outputs
