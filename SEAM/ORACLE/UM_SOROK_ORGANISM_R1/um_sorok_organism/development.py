"""Research-only psychological afterlife: typed *fictional* formation and rewiring.

This is not CAN/ADP native authority. Every admitted form is actor-specific, bound
by actual experienced event, scoped, graded, and revisable. No LLM may edit an
objective world fact or another actor's state here.
"""
from .types import stable_id, copy, GRADE

class InvalidDevelopment(ValueError): pass

ALLOWED={'ADD_FORM','LINK_FORMS','DIFFERENTIATE','CHANGE_RECRUITMENT_SCOPE',
         'CHANGE_STRENGTH','SET_DORMANT','REACTIVATE','REORGANIZE_PROJECT',
         'TRACE','MEMORY','ACTOR_SELF_MODEL','ADD_PROJECT','CHANGE_OTHER_MODEL','NO_CHANGE'}
KINDS={'MEDIATOR','TENSION','PRACTICE','EXPECTATION','DISCRIMINATION','RELATIONAL_INVESTMENT'}
RELATIONS={'RECRUITS','SUPPORTS','INHIBITS','COMPETES','DERIVED_FROM','CONTRADICTS'}


def admit(actor,experience,event_ref,candidates):
    """Mutates an in-memory actor copy; caller commits atomically with world.

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
            link={'source':a,'target':b,'relation':c['relation'],
                  'contexts':c.get('contexts',[]),'origin':[event_ref],
                  'evidence':evidence,'grade':GRADE}
            if link not in actor['links']:actor['links'].append(link)
            report.append({'kind':op,'from':a,'to':b,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='CHANGE_RECRUITMENT_SCOPE':
            ident=c.get('form_id')
            if ident not in actor['forms']:raise InvalidDevelopment('UNKNOWN_FORM')
            new_scope=c.get('new_scope')
            if not isinstance(new_scope,dict):raise InvalidDevelopment('BAD_SCOPE')
            form=actor['forms'][ident]
            form.setdefault('prior_scopes',[]).append({'scope':copy(form.get('scope',{})),'event':event_ref})
            form['scope']=copy(new_scope)
            form.setdefault('changes',[]).append(evidence)
            report.append({'kind':op,'form':ident,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op=='CHANGE_STRENGTH':
            ident=c.get('form_id')
            if ident not in actor['forms']:raise InvalidDevelopment('UNKNOWN_FORM')
            delta=c.get('delta',0)
            if not isinstance(delta,(int,float)) or abs(delta)>.35:raise InvalidDevelopment('UNBOUNDED_STRENGTH')
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
            ident=project.get('id') or stable_id('project',{'actor':actor['id'],'event':event_ref,'index':idx})
            if any(p['id']==ident for p in actor['projects']):
                raise InvalidDevelopment('DUPLICATE_PROJECT')
            project.update({'id':ident,'origin':[event_ref],'grade':GRADE})
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
            for field in ('priority','means','object','status','cue_terms'):
                if field in c:project[field]=copy(c[field])
            project.setdefault('history',[]).append(evidence)
            report.append({'kind':op,'project':ident,'status':'ADMITTED_SOURCEFREE_FICTIONAL'})
        elif op in ('TRACE','MEMORY'):
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
    """No invented microepisodes; only coarse sourced period effects, including null.
    Repeated activity can provisionally change scope of an *existing* power if
    explicitly warranted by coverage. This is not a new social memory/event.
    """
    outputs=[]
    for proc in processes:
        if proc.get('kind')=='practice_access' and proc.get('coverage')=='AGGREGATE_MODELED':
            fid=proc.get('form_id')
            if fid in actor['forms'] and proc.get('warrants_scope_change') is True:
                old=copy(actor['forms'][fid].get('scope',{}))
                new_locations=sorted(set(old.get('locations',[])+proc.get('locations',[])))
                actor['forms'][fid]['scope']={**old,'locations':new_locations}
                actor['forms'][fid].setdefault('changes',[]).append({'period':period_ref,'grade':GRADE,
                    'type':'AGGREGATE_MODELED_SCOPE_GENERALIZATION'})
                outputs.append({'kind':'PERIOD_SCOPE_CHANGE','form':fid})
    return outputs
