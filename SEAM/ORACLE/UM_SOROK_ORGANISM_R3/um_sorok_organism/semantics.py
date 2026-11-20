"""LLM is a generative semantic component, never an owner of world/actor truth.
Dependency injection allows any externally authorized LLM. Offline fallback is
explicitly coarse heuristic fiction, not an LLM and not a human learning law.
"""
from typing import Protocol, Callable
from .types import copy, stable_id, GRADE
from .prospective_horizon import select_bounded_exploratory_trial

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
            # A selected operation does not automatically undertake every
            # project that happens to make it possible. Sourcefree heuristic
            # chooses ONE eligible course; a model can choose none or explicitly
            # select several, with clear provisional provenance.
            # Noticing a possible end can license one provisional trial,
            # but never a newly fabricated means or an acquired motive.
            trial=select_bounded_exploratory_trial(possibilities)
            if trial:return {'task':task,**trial}
            option=possibilities[0]
            courses=option.get('project_courses',[])
            chosen=sorted(courses,key=lambda p:(-p.get('priority',.5),p['project_id']))[0] if courses else None
            return {'task':task,'action':option['action'],
                    'project_id':chosen['project_id'] if chosen else None,
                    'purpose_selection_grade':('HEURISTIC_PROJECT_COURSE_CHOSEN'
                         if chosen else 'NO_ASSIGNED_PROJECT_END'),
                    'basis':option.get('basis',[]),'semantic_grade':self.grade}
        if task=='development':
            experience=packet.get('experience',{})
            action=experience.get('own_action')
            status=experience.get('status')
            cues=experience.get('perceived_cues',[])
            if status not in ('PERFORMED','PARTIAL'):
                return {'task':task,'candidates':[],'semantic_grade':self.grade}
            relation_candidates=[]
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
            # Later opportunity takes up a prior possible end only when an
            # independently received sign recurs in a DISTINCT event.
            tags={str(t).lower() for cue in cues for t in cue.get('tags',[])}
            event_ref=packet.get('historical_psychodynamic_context',{}).get('objective_event_ref')
            current_trial=packet.get('selected_purpose_analytic_only',{})
            for prior in packet.get('actor_possible_ends',[]):
                # The CURRENT situated trial cannot be the evidence for its
                # simultaneous promotion to an already-acquired motive.
                if (current_trial.get('status')==
                        'ACTOR_POLICY_PROVISIONAL_END_TRIAL_NOT_DURABLE_MOTIVE'
                        and prior.get('id')==current_trial.get('possible_end_ref')):
                    continue
                if (prior.get('status')=='POSSIBLE_NOT_ACQUIRED_MOTIVE' and
                        prior.get('origin_event')!=event_ref and
                        tags & {str(v).lower() for v in prior.get('cue_terms',[])}):
                    matching=next((cue.get('id') for cue in cues if
                        type(cue.get('id')) is str and
                        {str(v).lower() for v in cue.get('tags',[])} &
                        {str(v).lower() for v in prior.get('cue_terms',[])}),None)
                    if matching:
                        relation_candidates.append({'kind':'TAKE_UP_POSSIBLE_END',
                            'possible_end_ref':prior['id'],
                            'means':copy(prior['possible_means']),
                            'later_perceived_cue_ref':matching,
                            'priority':.32})
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
                    # One performed SING may allow a previously unforeseen
                    # possible end; that is not the intention of the first act
                    # and does NOT install a continuing project yet.
                    heard=next((q.get('id') for q in cues if
                        type(q.get('id')) is str and q['id']),None)
                    if heard:
                        candidates.append({'kind':'NOTICE_POSSIBLE_END',
                            'perceived_cue_ref':heard,
                            'possible_object':'explore whether a rhythm can continue',
                            'possible_means':['SING','PRACTICE'],
                            'cue_terms':['sing','rhythm']})
                return {'task':task,'candidates':candidates+relation_candidates,'semantic_grade':self.grade}
            if action=='SIGNAL' and cues:
                return {'task':task,'candidates':[{'kind':'TRACE','manifestation':'contingent reply possible',
                       'cue_terms':['signal','care']}], 'semantic_grade':self.grade}
            return {'task':task,'candidates':[],'semantic_grade':self.grade}
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
                  'origin':['fictional_seed:'+packet['actor_id']]})
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
            # Motif source indices identify explicit fictional seeded forms,
            # never answer-derived forms. Reject unsupported/forged indices.
            motifs=[]
            for i,m in enumerate(seeded.get('relational_motifs',[])):
                refs=m.get('source_indices')
                if (type(refs) is not list or not 2<=len(refs)<=4 or
                    any(type(k) is not int or k<0 or k>=len(seeded_forms) for k in refs) or
                    len(set(refs))!=len(refs)):
                    raise ValueError('INVALID_FICTIONAL_MOTIF_SEED')
                mx=copy(m)
                mx.pop('source_indices',None)
                mx['source_forms']=[seeded_forms[k]['id'] for k in refs]
                mx['id']=stable_id('seed_motif',{'actor':packet['actor_id'],'i':i,'motif':m})
                effects=[]
                for e in m.get('effects',[]):
                    item=copy(e)
                    for key,index in (('source','source_index'),('target','target_index'),
                                      ('target_form','target_form_index')):
                        if index in item:
                            n=item.pop(index)
                            if type(n) is not int or n<0 or n>=len(seeded_forms):
                                raise ValueError('INVALID_FICTIONAL_MOTIF_SEED')
                            item[key]=seeded_forms[n]['id']
                    effects.append(item)
                mx['effects']=effects
                mx['origin']=['fictional_seed:'+packet['actor_id']]
                motifs.append(mx)
            projects.append({'id':'project:ordinary_life' ,'object':'maintain everyday life',
                 'means':['REST','EAT','WORK','CARE'],'priority':.42,'cue_terms':['home','work'],
                 'status':'active','origin':[]})
            return {'task':task,'forms':forms,'links':seeded_links,'relational_motifs':motifs,'projects':projects,
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
                and 'possible_end_trial_id' not in out):
            raise ValueError('NO_ACTION_OR_ISSUED_OPTION')
        if task=='development' and not isinstance(out.get('candidates'),list):raise ValueError('BAD_DEVELOPMENT_CANDIDATES')
        return out
