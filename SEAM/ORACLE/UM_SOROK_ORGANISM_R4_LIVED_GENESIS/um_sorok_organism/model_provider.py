"""Optional real generative-semantic LLM adapter.

The offline demo works without credentials. With explicit configuration and a
live reachable OpenAI-compatible chat-completions endpoint, this adapter sends
only the task-specific, prequalified semantic packet. It cannot directly mutate
world, body, or actor state: all proposals are validated downstream.

NETWORK NOT EXERCISED IN THE CURRENT RESEARCH SANDBOX. This code supplies an
integration interface, not a claim that an LLM was actually called here.
"""
import json, os, urllib.request, urllib.error
from .types import copy

SEMANTIC_TASK_INSTRUCTIONS={
 'adult_constructor': (
  'Construct a rich, contradictory but materially intelligible FICTIONAL adult '+
  'constitution from a qualified full pseudo-respondent and a historical field. '+
  'The source answers constrain public initial observations but DO NOT identify '+
  'their real respondent\'s private psyche. Return forms, links, projects, '+
  'fictional_backfill. Forms must have id, kind, cues, enables, scope, access, '+
  'object, strength. Distinguish interpretive proposals and uncertain histories. '+
  'Never make another person\'s conduct or survey source facts up.'),
 'actor_attempt': (
  'From the actor\'s OWN accessible situation, presently recruited psychology, '+
  'bodily abilities, object-directed activity and explicitly supplied eligible '+
  'options, choose one ACTION that is literally present in options. '+
  'It can be ordinary continuation or refusal, not a maximally dramatic event. '+
  'No omniscient world facts; no invented other-person participation.'),
 'development': (
  'Propose possible FICTIONAL psychological afterlife caused by THIS actor\'s '+
  'accessible experience and acquired capabilities. These are fallible '+
  'sourcefree hypotheses, not laws of human learning. Use candidate kinds '+
  'ADD_FORM, LINK_FORMS, DIFFERENTIATE, CHANGE_RECRUITMENT_SCOPE, '+
  'CHANGE_STRENGTH, SET_DORMANT, REACTIVATE, REORGANIZE_PROJECT, ADD_PROJECT, '+
  'TRACE, MEMORY, ACTOR_SELF_MODEL, NO_CHANGE. Preserve nonchange. An infant '+
  'can acquire sensory, temporal, motor, affective and relational practices '+
  'without adult linguistic concepts. Analysts may use mature language '+
  'but must not assign that conceptual competence to the child. Every '+
  'proposed form must be operative, with cues and possible effects, not a '+
  'pretentious personality gloss. No fabrication of unexperienced facts.'),
 'expression': (
  'Render a short actor-accessible outward surface only. The person may be '+
  'silent, evasive, mistaken, conflicted or refuse. Do not disclose the full '+
  'psychological iceberg or analyst-side history. Do not invent material '+
  'outcomes beyond actual actor-perceived results.'),
}

class OpenAICompatibleJSONProvider:
    """Explicit opt-in stdlib HTTP transport for live structured model calls.

    Endpoint defaults to OpenAI-compatible POST /v1/chat/completions. This is
    not tied to a particular service and has not been connectivity tested here.
    """
    grade='LIVE_LLM_PROPOSAL_ONLY_NOT_CANONICAL_TRUTH'
    def __init__(self, model, api_key, endpoint='https://api.openai.com/v1/chat/completions',timeout=35):
        if not model or not api_key:raise ValueError('EXPLICIT_MODEL_AND_API_KEY_REQUIRED')
        if not endpoint.startswith('https://'):raise ValueError('HTTPS_ENDPOINT_REQUIRED')
        self.model=model;self.key=api_key;self.endpoint=endpoint;self.timeout=timeout

    @classmethod
    def from_environment(cls):
        return cls(os.environ.get('UM_SOROK_LLM_MODEL'),
                   os.environ.get('UM_SOROK_LLM_API_KEY'),
                   os.environ.get('UM_SOROK_LLM_ENDPOINT','https://api.openai.com/v1/chat/completions'))

    def propose(self,task,packet):
        if task not in SEMANTIC_TASK_INSTRUCTIONS:raise ValueError('UNKNOWN_LLM_SEMANTIC_TASK')
        body={'model':self.model,'temperature':.35,
              'response_format':{'type':'json_object'},
              'messages':[{'role':'system','content':(
                  'You are a provisional semantic constructor for the Rawlsing '+
                  'research FICTION. Return ONLY a JSON object. '+
                  SEMANTIC_TASK_INSTRUCTIONS[task])},
                  {'role':'user','content':json.dumps({'task':task,'packet':copy(packet)},ensure_ascii=False)}]}
        req=urllib.request.Request(self.endpoint,data=json.dumps(body).encode('utf-8'),
                headers={'Authorization':'Bearer '+self.key,'Content-Type':'application/json'},
                method='POST')
        try:
            with urllib.request.urlopen(req,timeout=self.timeout) as response:
                raw=json.load(response)
        except (urllib.error.URLError,TimeoutError) as e:
            raise RuntimeError('LLM_PROVIDER_UNAVAILABLE') from e
        choices=raw.get('choices',[])
        if not choices or not isinstance(choices[0].get('message',{}).get('content'),str):
            raise ValueError('UNSUPPORTED_LLM_REPLY_SHAPE')
        out=json.loads(choices[0]['message']['content'])
        if not isinstance(out,dict):raise ValueError('LLM_MUST_RETURN_OBJECT')
        out.setdefault('task',task)
        out['semantic_grade']=self.grade
        return out
