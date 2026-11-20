"""LLM is a generative semantic component, never an owner of world/actor truth.
Dependency injection allows any externally authorized LLM. Offline fallback is
explicitly coarse heuristic fiction, not an LLM and not a human learning law.
"""
from typing import Protocol, Callable
from .types import copy, stable_id, GRADE
from .preproject_agency import fallback_nonproject_orientation, fallback_nonproject_deferral
from .prospective_horizon import select_bounded_exploratory_trial
from .distributed_power import choose_uncompelled_assistance
from .practical_inquiry import choose_grounded_public_inquiry
from .material_investments import choose_qualified_material_care

class SemanticProvider(Protocol):
    def propose(self,task:str,packet:dict)->dict: ...

class CallbackLLMProvider:
    """Adapter for an external model callback with JSON-in/JSON-out.
    No API calls are assumed or secretly made. Caller supplies implementation.
    """
    def __init__(self,fn:Callable[[str,dict],dict]):self.fn=fn
    def propose(self,task,packet):
        response=self.fn(task,copy(packet))
        if not isinstance(response,dict):raise TypeError('LLM_MUST_RETURN_STRUCTURED_DICT')
        if response.get('task') not in (None,task):raise ValueError('MODEL_TASK_MISMATCH')
        return copy(response)

class HeuristicSemanticProvider:
    """Always available incomplete sourcefree substitute, kept visible in receipts."""
    grade='SOURCEFREE_RULE_BASED_PLACEHOLDER_NO_LLM'
    def propose(self,task,packet):
        if task=='actor_attempt':
            possibilities=packet.get('options',[])
            if not possibilities:return {'task':task,'action':'WAIT','basis':['NONE']}
            # deliberately choose among actually available options; does not mint actions.
            if possibilities[0].get('psychodynamic_status')=='UNRESOLVED_CONTRADICTION':
                # This is a declared primitive *deferral* policy, not proof
                # that any human with conflict necessarily freezes or avoids.
                available={o['action'] for o in possibilities}
                if 'WAIT' in available:
                    return {'task':task,'action':'WAIT','basis':['SOURCEFREE_HEURISTIC_CONFLICT_DEFERRAL'],
                            'semantic_grade':self.grade}
            # The embodied child's acquired, nonpropositional anticipation may
            # alter a future attempt without first inventing an adult project.
            # When rival currents coexist, this heuristic MUST NOT decide.
            orientation=fallback_nonproject_orientation(possibilities)
            if orientation:
                return {'task':task,**orientation}
            # The first R8 code review found that merely recording learned
            # negative pressure would let the older default still select it.
            # This bounded policy MAY defer if an acquired tacit WITHHOLD or
            # unresolved contradiction has no uncontested nonproject approach.
            deferral=fallback_nonproject_deferral(possibilities)
            if deferral:
                return {'task':task,**deferral}
            # Actual historical alternatives can organize provisional action
            # before a settled purpose exists. An experienced future occasion
            # might create a new motive, but this selection does not assert one.
            trial=select_bounded_exploratory_trial(possibilities)
            if trial:
                return {'task':task,**trial}
            # A previously witnessed reciprocal signal can be tried again,
            # without assigning an enduring attachment or commandeering the
            # responder. Actor's body bounds the immediate offline proposal.
            assisted=choose_uncompelled_assistance(
                possibilities,packet.get('actor',{}).get('body',{}))
            if assisted:
                return {'task':task,**assisted}
            inquiry=choose_grounded_public_inquiry(possibilities)
            if inquiry:
                return {'task':task,**inquiry}
            object_action=choose_qualified_material_care(possibilities)
            if object_action:
                return {'task':task,**object_action}
            # Select at most one historically available undertaking, not the
            # pooled basis of all projects that share the chosen operation.
            # This deterministic priority/tie policy is fictional fallback,
            # NOT an empirically recovered conscious motive.
            option=possibilities[0]
            courses=option.get('project_courses',[])
            bindable={a['project_id'] for a in option.get('practical_alternatives',[])
                      if a.get('project_id') is not None
                      and a.get('binding_status')!='UNBOUND_PARTY_NOT_PRESENT'}
            available=[c for c in courses if c['project_id'] in bindable]
            if available:
                selected=sorted(available,key=lambda x:(
                    -x.get('priority',.5),str(x['project_id'])))[0]
                project_ref=selected['project_id']
            else:
                project_ref=None
            alternative=next((a for a in option.get('practical_alternatives',[])
                 if a.get('project_id')==project_ref),None)
            return {'task':task,'action':option['action'],
                    'project_id':project_ref,
                    **({'practical_option_id':alternative['option_id']}
                        if alternative else {}),
                    'purpose_selection_grade':('HEURISTIC_PROJECT_COURSE_CHOSEN'
                         if project_ref is not None else 'NO_ASSIGNED_PROJECT_END'),
                    'basis':option.get('basis',[]),'semantic_grade':self.grade}
        if task=='development':
            experience=packet.get('experience',{})
            action=experience.get('own_action')
            status=experience.get('status')
            cues=experience.get('perceived_cues',[])
            # Sourcefree fallback can now turn a real lived bodily transition
            # into a PROVISIONAL nonverbal proposal, even when the actor was
            # the recipient of care rather than a voluntary co-performer.
            # A live LLM receives the same evidence-grade candidates and may
            # instead nominate no change. No adult end/idea is inferred.
            lived=copy(packet.get('historically_proposed_preproject',[]))
            if status not in ('PERFORMED','PARTIAL'):
                return {'task':task,'candidates':lived,'semantic_grade':self.grade}
            relation_candidates=lived+copy(
                packet.get('historically_proposed_functional',[]))
            other=experience.get('reciprocated_partner')
            if other and cues:
                # A genuinely performed joint occurrence can leave a trace and
                # a tentative expectation; it does NOT prove love, approval,
                # relational investment, or a stable shared competency.
                relation_candidates.append({'kind':'TRACE',
                    'content':'coactivity occurred; its future meaning remains undetermined',
                    'manifestation':'joint_activity_contingency_possible',
                    'cue_terms':[other,'coactivity']})
                relation_candidates.append({'kind':'CHANGE_OTHER_MODEL',
                    'other_ref':other,'hypothesis':'shared participation with '+other+
                    ' has recently occurred; future participation remains uncertain',
                    'confidence':'tentative'})
            # A prior sensed possibility can become a provisional practical
            # end only in a DIFFERENT experienced event. The first act was
            # exploratory, not retroactively undertaken for the later end.
            tags={str(tag).lower() for cue in cues
                  for tag in cue.get('tags',[])}
            for candidate in packet.get('actor_possible_ends',[]):
                if (candidate.get('status')=='POSSIBLE_NOT_ACQUIRED_MOTIVE'
                        and candidate.get('origin_event')!=packet.get(
                             'historical_psychodynamic_context',{}).get('objective_event_ref')
                        and tags & {str(x).lower() for x in candidate.get('cue_terms',[])}):
                    # The fallback may name an actually received later sign.
                    # It may never make up an unseen cue or confer knowledge
                    # of why that sign became psychically important.
                    matching_sign=next((cue.get('id') for cue in cues
                        if type(cue.get('id')) is str and
                        {str(t).lower() for t in cue.get('tags',[])}
                        & {str(t).lower() for t in candidate.get('cue_terms',[])}),None)
                    relation_candidates.append({
                        'kind':'TAKE_UP_POSSIBLE_END',
                        'possible_end_ref':candidate['id'],
                        'means':copy(candidate['possible_means']),
                        'priority':.32,
                        **({'later_perceived_cue_ref':matching_sign}
                            if matching_sign is not None else {}),
                    })
                    break
            if action in ('PRACTICE','SING','JOIN','MAKE_SPACE') and cues:
                # Existing forms can generalize in scope rather than minting
                # endlessly duplicated skills. This is a provisional fictional
                # hypothesis and requires *actual* actor participation.
                forms=packet.get('selected_constitution',{}).get('recruited',[])
                all_forms=packet.get('actor_forms',{})
                origin=next((f for f in all_forms.values() if action in f.get('enables',[])
                       and f.get('kind')=='PRACTICE'),None)
                if origin:
                    old=origin.get('scope',{}).get('locations',[])
                    place=packet['actor']['location']
                    if old and place not in old:
                        return {'task':task,'candidates':[{'kind':'CHANGE_RECRUITMENT_SCOPE',
                            'form_id':origin['id'], 'new_scope':{'locations':sorted(set(old+[place]))}}]+relation_candidates,
                            'semantic_grade':self.grade}
                    return {'task':task,'candidates':[{'kind':'CHANGE_STRENGTH',
                          'form_id':origin['id'],'delta':.04}]+relation_candidates, 'semantic_grade':self.grade}
                fid=stable_id('form',{'actor':packet['actor']['id'],'act':action,'clock':packet['clock']})
                form={'id':fid,'kind':'PRACTICE','content':'practiced '+action.lower(),
                      'cues':sorted({tag for cue in cues for tag in cue.get('tags',[])}|{action.lower()}),
                      'enables':[action], 'scope':{'locations':[packet['actor']['location']]},
                      'strength':.45,'access':'tacit','lifecycle':'ACTIVE','body_min':.1,
                      'origin':[],'grade':GRADE}
                candidates=[{'kind':'ADD_FORM','form':form}]
                if action=='SING':
                    previous=next((f for f in all_forms.values() if 'PRACTICE' in f.get('enables',[])),None)
                    if previous:
                        candidates.append({'kind':'LINK_FORMS',
                            'source':previous['id'],'target':fid,'relation':'SUPPORTS'})
                    # A first performed song may expose an unanticipated
                    # *possible end*. It is NOT yet why the person acted.
                    # Only a later experienced episode can give it project
                    # status, and neither step asserts an empirical human law.
                    received=next((q.get('id') for q in cues
                         if type(q.get('id')) is str and q.get('id')),None)
                    if received:
                        candidates.append({'kind':'NOTICE_POSSIBLE_END',
                            'perceived_cue_ref':received,
                            'possible_object':'explore whether a rhythm can continue',
                            'possible_means':['SING','PRACTICE'],
                            'cue_terms':['sing','rhythm']})
                return {'task':task,'candidates':candidates+relation_candidates,'semantic_grade':self.grade}
            if action=='SIGNAL' and cues:
                return {'task':task,'candidates':[{'kind':'TRACE','manifestation':'contingent reply possible',
                       'cue_terms':['signal','care']}]+relation_candidates, 'semantic_grade':self.grade}
            return {'task':task,'candidates':relation_candidates,'semantic_grade':self.grade}
        if task=='blind_adult_interview':
            # A sourcefree fallback has no independently generated survey
            # response law. Silence is preferable to resurrecting the
            # questionnaire-keyed cached answer as a false blind success.
            return {'task':task,'responses':{},
                'status':'NO_INDEPENDENT_FALLBACK_INTERVIEW_EVALUATOR',
                'semantic_grade':self.grade}
        if task=='adult_constructor':
            target=packet['pseudo_respondent']
            answers=target.get('answers',{})
            forms=[];projects=[]
            for question,answer in sorted(answers.items()):
                # NOT an inference of actual respondent psyche; fictional hypothesis
                # of interpretive means. The question remains part of admission lineage.
                fid=stable_id('belief',{'q':question,'a':answer,'id':packet['actor_id']})
                forms.append({'id':fid,'kind':'MEDIATOR','functional_role':'INTERPRETIVE_ORIENTING',
                    'content':f'fictional interpretive stance regarding {question}: {answer}',
                    'cues':[str(question).lower(),'survey','interview'],
                    'enables':['SPEAK'], 'scope':{},'strength':.55,'access':'articulated',
                    'lifecycle':'ACTIVE','body_min':0,'origin':[], 'object':question,
                    'asserted_answer':answer,'grade':'FICTIONAL_ABDUCTIVE_INITIALIZATION'})
            seeded=target.get('fictional_seed',{})
            for i,spec in enumerate(seeded.get('acquired_forms',[])):
                fid=stable_id('seed_form',{'actor':packet['actor_id'],'i':i,'spec':spec})
                forms.append({'id':fid,'kind':spec.get('kind','PRACTICE'),
                  'functional_role':spec.get('functional_role','EMBEDDING_RELATION'),
                  'content':spec.get('content','fictionally acquired operation'),
                  'cues':spec.get('cues',[]),'enables':spec.get('enables',[]),
                  'scope':spec.get('scope',{}),'strength':spec.get('strength',.5),
                  'access':spec.get('access','tacit'),'lifecycle':'ACTIVE',
                  'body_min':spec.get('body_min',.1),'object':spec.get('object'),
                  'tendencies':spec.get('tendencies',[]),
                  'grade':'EXPLICIT_FICTIONAL_BACKFILL_NOT_SURVEY_INFERENCE'})
            for p in seeded.get('projects',[]):
                projects.append({'id':stable_id('seed_project',{'actor':packet['actor_id'],'p':p}),
                  'object':p.get('object','continued life'),
                  'means':p.get('means',[]),'priority':p.get('priority',.5),
                  'cue_terms':p.get('cue_terms',[]),'status':'active',
                  'origin':['fictional_seed:'+packet['actor_id']],
                  **{k:copy(p[k]) for k in ('expected_difference','addressed_party_ref')
                     if k in p}})
            # Explicit fictional-backfill link geometry. Indexes point only to
            # the extra seeded forms, never to empirical question-answer forms.
            seeded_forms=forms[len(answers):]
            seeded_links=[]
            for edge in seeded.get('links',[]):
                left,right=edge.get('source_index'),edge.get('target_index')
                if not isinstance(left,int) or not isinstance(right,int) or left<0 or right<0 or left>=len(seeded_forms) or right>=len(seeded_forms):
                    raise ValueError('INVALID_FICTIONAL_RELATION_SEED')
                seeded_links.append({'source':seeded_forms[left]['id'],
                    'target':seeded_forms[right]['id'],
                    'relation':edge['relation'], 'contexts':edge.get('contexts',[]),
                    'grade':'FICTIONAL_BACKFILL_HYPOTHESIS'})
            projects.append({'id':'project:ordinary_life','object':'maintain everyday life',
                 'means':['REST','EAT','WORK','CARE'],'priority':.42,'cue_terms':['home','work'],
                 'status':'active','origin':[]})
            return {'task':task,'forms':forms,'links':seeded_links,'projects':projects,
                    'fictional_backfill':{'summary':'Compressed possible adult life; no source respondent history identified',
                      'coverage':'HYPOTHETICAL','unknown':['specific childhood scenes']},
                    'semantic_grade':self.grade}
        if task=='expression':
            e=packet['actual']
            return {'task':task,'speech':None,'surface':f"{e['action'].lower()} — {e['outcome'].lower().replace('_',' ')}",
                    'semantic_grade':self.grade}
        raise ValueError('UNSUPPORTED_SEMANTIC_TASK:'+task)

class ValidatingSemanticService:
    def __init__(self,provider=None): self.provider=provider or HeuristicSemanticProvider()
    def proposal(self,task,packet):
        out=self.provider.propose(task,packet)
        if not isinstance(out,dict):raise ValueError('BAD_SEMANTIC_PACKET')
        if (task=='actor_attempt' and 'action' not in out
                and 'practical_option_id' not in out):
            raise ValueError('NO_ACTION_OR_PRACTICAL_OPTION')
        if task=='development' and not isinstance(out.get('candidates'),list):raise ValueError('BAD_DEVELOPMENT_CANDIDATES')
        return out
