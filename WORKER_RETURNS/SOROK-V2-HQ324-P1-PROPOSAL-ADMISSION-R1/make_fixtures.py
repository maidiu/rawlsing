"""Author-side fixture freezer; emits only fabricated synthetic TEST-ONLY histories."""
import copy,json,hashlib
from pathlib import Path
from p1_contract import digest,evaluate,canonical,SCHEMA,CONTEXT_SCHEMA,POLICY_SCHEMA,PROB_GRADE
here=Path(__file__).parent/'fixtures'

context={
'schema':CONTEXT_SCHEMA,'world_ref':'WORLD-BIKE-1','as_of':'2026-10-17T10:00:00Z',
'places':['GARAGE-1'],'allowed_role_refs':['CHILD','CAREGIVER','PEER','NEIGHBOR'],'facts':{
 'THEFT-1':{'epistemic_class':'ADMITTED_OBJECTIVE_EVENT','occurred':True,'kind':'BIKE_STOLEN','time':'2026-10-17T09:00:00Z','known_culprit':None,'material_object_ref':'BIKE-CHILD-1'},
 'PRIVATE-CAREGIVER-1':{'epistemic_class':'PRIVATE_ACTOR_STATE','occurred':True,'kind':'UNREADABLE_CAREGIVER_CONCERN','time':'2026-10-17T08:00:00Z'},
 'DENIED-PAST-THEFT':{'epistemic_class':'ADMITTED_OBJECTIVE_EVENT','occurred':False,'kind':'OTHER_THEFT','time':'2026-10-16T09:00:00Z'}},
'people':{'CHILD-1':{'role':'CHILD','history_ref':'H-CHILD-1'},
 'CARE-1':{'role':'CAREGIVER','history_ref':'H-CARE-PROTECT'},
 'PEER-1':{'role':'PEER','history_ref':'H-PEER-BELONGING'},
 'NEIGHBOR-1':{'role':'NEIGHBOR','history_ref':'H-NEIGHBOR-INDEPENDENT'}},
'histories':{
 'H-CHILD-1':{'owner':'CHILD-1','source':'SYNTHETIC_HISTORY','summary':'child acquired bicycle through repair work; prior adult recognition varied'},
 'H-CHILD-2':{'owner':'CHILD-1','source':'SYNTHETIC_HISTORY','summary':'child bicycle gift and repeated arbitrary searches; reacts to control with caution'},
 'H-CARE-PROTECT':{'owner':'CARE-1','source':'SYNTHETIC_HISTORY','summary':'caregiver works changing shifts, has protected child without always attending emotion'},
 'H-CARE-CONTROL':{'owner':'CARE-1','source':'SYNTHETIC_HISTORY','summary':'caregiver has history of intrusive scrutiny and material safety concern'},
 'H-PEER-BELONGING':{'owner':'PEER-1','source':'SYNTHETIC_HISTORY','summary':'peer once repeated a false rumor to earn group belonging'},
 'H-NEIGHBOR-INDEPENDENT':{'owner':'NEIGHBOR-1','source':'SYNTHETIC_HISTORY','summary':'neighbor has independent daily schedule unrelated to theft'}},
'actor_access':{'CHILD-1':['THEFT-1'],'CARE-1':['THEFT-1'],'PEER-1':['THEFT-1'], 'NEIGHBOR-1':[]},
'action_opportunities':{
 'OP-CARE-SPEAK':{'actor_ref':'CARE-1','act_kind':'SPEAK_TO_CHILD','place_ref':'GARAGE-1','time':'2026-10-17T10:00:00Z'},
 'OP-PEER-SPEAK':{'actor_ref':'PEER-1','act_kind':'SPEAK_TO_CHILD','place_ref':'GARAGE-1','time':'2026-10-17T10:00:00Z'},
 'OP-CHILD-SEARCH':{'actor_ref':'CHILD-1','act_kind':'CHECK_GARAGE','place_ref':'GARAGE-1','time':'2026-10-17T10:00:00Z'},
 'OP-CARE-REPORT':{'actor_ref':'CARE-1','act_kind':'REPORT_MISSING_BIKE','place_ref':'GARAGE-1','time':'2026-10-17T10:00:00Z'}},
'material_affordances':['GARAGE_ACCESS','PHONE_AVAILABLE'],
}
def freeze_context(x):
 x['context_hash']=digest({k:v for k,v in x.items() if k!='context_hash'});return x
context=freeze_context(context)

def core(cid,part,actions,interps,courses,effects,req=None,family='OBSERVABLE_UTTERANCE'):
 return dict(candidate_id=cid,family=family,parent_event_ref='THEFT-1',time=context['as_of'],place_ref='GARAGE-1',
 participants=part,action_refs=actions,prospective_participants=[],readset=['THEFT-1'],prerequisites=req or [{'kind':'WORLD_FACT_TRUE','ref':'THEFT-1'}],
 interpretations=interps,courses=courses,possible_effects=effects,visibility=part,uncertainty='Competing possible receptions, no privileged insight or fixed psychological consequence')

def op(actor,ref,kind):return dict(actor_ref=actor,opportunity_ref=ref,act_kind=kind)
def meaning(actor,utterance,claim):
 return dict(speaker_actor_ref=actor,utterance=utterance,claim=claim,claim_kind='ATTRIBUTED_UNVERIFIED_ASSERTION',claim_world_fact_ref=None,accessible_source_refs=['THEFT-1'])
def course(cid,actor,action,description):return dict(course_id=cid,actor_ref=actor,action_ref=action,description=description)
def eff(actor,kind,description):return dict(target_actor_ref=actor,description=description,owner_required='CAN011_EXTERNAL_OWNER',effect_kind=kind,epistemic_class='HYPOTHESIS_ONLY')

care=core('ALT-CARE',["CHILD-1","CARE-1"],[op('CARE-1','OP-CARE-SPEAK','SPEAK_TO_CHILD')],
 [meaning('CARE-1','We should report this and see what can be secured.','A careful response could reduce future loss; I am worried.')],
 [course('COURSE-CARE-SPEAK','CARE-1','OP-CARE-SPEAK','Caregiver considers reassurance or practical protective speech')],
 [eff('CHILD-1','MAY_RETAIN_CONTRADICTION','Child may perceive factual prudence yet feel emotionally unheard')],
 [{'kind':'WORLD_FACT_TRUE','ref':'THEFT-1'},{'kind':'ACTOR_ACCESS','ref':'CARE-1|THEFT-1'},{'kind':'HISTORY_PRESENT','ref':'CARE-1|H-CARE-PROTECT'}])
peer=core('ALT-PEER',['CHILD-1','PEER-1'],[op('PEER-1','OP-PEER-SPEAK','SPEAK_TO_CHILD')],
 [meaning('PEER-1','People from that block always take things.','Unsubstantiated blame of neighbors in a peer rumor')],
 [course('COURSE-PEER-SPEAK','PEER-1','OP-PEER-SPEAK','Peer might circulate unsupported scapegoating rumor')],
 [eff('CHILD-1','MAY_RETAIN_CONTRADICTION','Child could reject or absorb peer narrative, unknown')],
 [{'kind':'WORLD_FACT_TRUE','ref':'THEFT-1'},{'kind':'ACTOR_ACCESS','ref':'PEER-1|THEFT-1'},{'kind':'HISTORY_PRESENT','ref':'PEER-1|H-PEER-BELONGING'}])
child=core('ALT-CHILD-SEARCH',['CHILD-1'],[op('CHILD-1','OP-CHILD-SEARCH','CHECK_GARAGE')],[],
 [course('COURSE-CHILD-SEARCH','CHILD-1','OP-CHILD-SEARCH','Child might look for lock marks before deciding what happened')],
 [eff('CHILD-1','NO_CHANGE','No durable response is required')],
 [{'kind':'WORLD_FACT_TRUE','ref':'THEFT-1'},{'kind':'MATERIAL_AFFORDANCE','ref':'GARAGE_ACCESS'}], 'MATERIAL_ACTION_PROPOSAL')
none=core('ALT-NONE',['CHILD-1'],[],[],[],[],[{'kind':'WORLD_FACT_TRUE','ref':'THEFT-1'}],'NONOCCURRENCE')

def packet(candidates,ctx=context,pid='MODEL-PACKET-1'):
 d=dict(schema=SCHEMA,epistemic_class='LLM_PROPOSAL',proposal_id=pid,world_ref=ctx['world_ref'],context_hash=ctx['context_hash'],
 as_of=ctx['as_of'],model={'provider_label':'FROZEN_FABRICATED_PACKET_NO_LIVE_MODEL','model_version':'SYNTH-1','prompt_version':'P1-PROMPT-1',
 'prompt_sha256':hashlib.sha256(b'fictional bounded LLM proposal prompt v1').hexdigest(),'sampling_record':{'kind':'FROZEN_AUTHOR_SYNTHETIC','model_draws':'NOT_RECORDED_NOT_CAUSAL'}},
 candidates=candidates)
 d['proposal_hash']=digest(d);return d

revised=copy.deepcopy(context);revised['people']['CARE-1']['history_ref']='H-CARE-CONTROL';revised['people']['CHILD-1']['history_ref']='H-CHILD-2';revised=freeze_context({k:v for k,v in revised.items() if k!='context_hash'})
changed_peer=copy.deepcopy(context);changed_peer['actor_access']['PEER-1']=[]
changed_peer=freeze_context({k:v for k,v in changed_peer.items() if k!='context_hash'})
no_theft=copy.deepcopy(context);no_theft['facts']['THEFT-1']['occurred']=False
no_theft=freeze_context({k:v for k,v in no_theft.items() if k!='context_hash'})

items={
 'context_base.json':context,
 'context_changed_histories.json':revised,
 'context_peer_not_exposed.json':changed_peer,
 'context_no_theft.json':no_theft,
 'packet_base.json':packet([care,peer,child,none]),
 'packet_order_reversed.json':packet([none,child,peer,care],context,'MODEL-PACKET-ORDER-REV'),
 'packet_changed_histories.json':packet([copy.deepcopy(care),peer,child,none],revised,'MODEL-PACKET-CHANGED-HIST'),
 'packet_changed_peer.json':packet([care,peer,child,none],changed_peer,'MODEL-PACKET-PEER-CHANGED'),
 'packet_no_theft.json':packet([care,peer,child,none],no_theft,'MODEL-PACKET-NO-THEFT'),
 'packet_valid_empty.json':packet([]),
 'packet_explicit_nonoccurrence.json':packet([none],context,'MODEL-PACKET-NONOC'),
}
# Fixture where caregiver claim/prerequisite intentionally holds only for revised history
care2=copy.deepcopy(care);care2['candidate_id']='ALT-CARE-CONTROL'
care2['prerequisites'][-1]['ref']='CARE-1|H-CARE-CONTROL'
items['packet_control_history.json']=packet([care2,none],revised,'MODEL-PACKET-CONTROL')
prospect=copy.deepcopy(care)
prospect['candidate_id']='ALT-PROSPECTIVE-NEW-CAREGIVER'
prospect['participants'].append('FUTURE-CARE-2')
prospect['prospective_participants']=[{'proposed_ref':'FUTURE-CARE-2','role_ref':'CAREGIVER',
 'independent_history_ref':'H-PENDING-FUTURE-CARE-2','owner_proposal_ref':'GENEALOGY-PENDING-1',
 'epistemic_class':'NEW_ENTITY_CANDIDATE_ONLY'}]
items['packet_prospective_person.json']=packet([prospect],context,'MODEL-PACKET-PROSPECTIVE')

base=evaluate(items['packet_base.json'],context)
assert base['decision']=='ADMIT',base
weights={'ALT-CARE':3,'ALT-PEER':2,'ALT-CHILD-SEARCH':4,'ALT-NONE':1}
policy={'schema':POLICY_SCHEMA,'policy_id':'P1-WEIGHTS-SYNTH-1','policy_version':'1.0.0',
 'parameter_source':'AUTHORED_DESIGN_HYPOTHESIS_TEST_ONLY','calibration_grade':PROB_GRADE,
 'candidate_set_hash':base['candidate_set_hash'],'weight_units':weights}
policy['policy_hash']=digest(policy)
items['policy_design_weights.json']=policy
for filename,value in items.items():
 (here/filename).write_text(json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'fixtures':{name:digest(value) for name,value in items.items()},'baseline':{k:base[k] for k in ('decision','candidate_set_hash')},'eligible':len(base['eligible_entries'])},indent=2))
