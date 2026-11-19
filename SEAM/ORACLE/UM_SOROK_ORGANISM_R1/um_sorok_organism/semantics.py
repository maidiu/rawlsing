"""LLM is a generative semantic component, never an owner of world/actor truth.
Dependency injection allows any externally authorized LLM. Offline fallback is
explicitly coarse heuristic fiction, not an LLM and not a human learning law.
"""
from typing import Protocol, Callable
from .types import copy, stable_id, GRADE

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
            return {'task':task,'action':possibilities[0]['action'],
                    'basis':possibilities[0].get('basis',[]),'semantic_grade':self.grade}
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
                all_known=packet.get('actor_forms',{})
                existing=next((f for f in all_known.values()
                    if f.get('kind')=='RELATIONAL_INVESTMENT' and f.get('other_ref')==other),None)
                if existing:
                    relation_candidates.append({'kind':'CHANGE_STRENGTH','form_id':existing['id'],'delta':.03})
                else:
                    relation_candidates.append({'kind':'ADD_FORM','form':{
                        'kind':'RELATIONAL_INVESTMENT','other_ref':other,
                        'content':'provisional recognition of a recurrently possible shared activity',
                        'cues':['sing','join','coactivity'], 'enables':[],
                        'scope':{'counterpart':other},'strength':.32,'access':'tacit',
                        'lifecycle':'ACTIVE','body_min':0.0,
                        'object':'possible cooperation with '+other}})
                relation_candidates.append({'kind':'CHANGE_OTHER_MODEL',
                    'other_ref':other,'hypothesis':'shared participation with '+other+
                    ' has recently occurred; future participation remains uncertain',
                    'confidence':'tentative'})
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
                    # Concrete fictional new purpose; NOT empirically warranted
                    # from one episode and not a universal child motive.
                    candidates.append({'kind':'ADD_PROJECT','project':{
                        'id':stable_id('project',{'actor':packet['actor']['id'],'clock':packet['clock'],
                                                 'object':'continue shared rhythms'}),
                        'object':'explore whether a rhythm can continue',
                        'means':['SING','PRACTICE'],'priority':.32,
                        'cue_terms':['sing','rhythm'],'status':'active'}})
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
        if task=='actor_attempt' and 'action' not in out:raise ValueError('NO_ACTION')
        if task=='development' and not isinstance(out.get('candidates'),list):raise ValueError('BAD_DEVELOPMENT_CANDIDATES')
        return out
