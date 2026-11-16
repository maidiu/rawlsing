"""Closed research data boundary. No claim of semantic proof over arbitrary prose.

Unclassified containers/fields/text are withheld or refused. Hash/ID fields have
separate finite provenance bindings; a string looking like a hash grants nothing.
"""
from .core import h_obj
import re
REDACTED='__FUTURE_CHILD_MATERIAL_REDACTED_EMBARGO__'
ROUTES={'ROUTE_LOCAL_CLOSED','ROUTE_INSTITUTIONAL','ROUTE_UNCONVENTIONAL','ROUTE_MOBILITY'}
PLACES={'INST_WORKSHOP_A','INST_EVENING_CLASS_B','INST_COMMUNITY_D','INST_TRANSIT_E','IMPOSSIBLE_SITE'}
KINDS={'KNOWN_COUNTERPART','PROVISIONAL_COUNTERPART','NONOCCURRENCE'}
EC_KEYS={'time_or_interval','required_state_predicates','required_relation_objective_refs','second_parent_structure_and_position_constraints','conception_witness_requirements','admissible_world_context_refs','place'}
CANDIDATE_KEYS={'candidate_local_id','candidate_kind','route_kind_id','endpoint_constraints','assumptions','falsifiers','plausibility_rank_ordinal','candidate_origin','model_relative_plausibility_NOT_frequency','class_key','requires_joint_propensity','model_reference','counterpart_ref'}
SAFE_ANNOTATIONS={'workplace adjacency contact','evening class enrollment','no shared shift overlap','class not attended','same workplace adjacency in different wording'}
MARKER=re.compile(r'future[\s_-]*child|child[\s_-]*(outcome|personality|adversity|wound|health|education)|desired[\s_-]*(wound|adversity)',re.I)

def leak_paths(value,path='$'):
 found=[]
 if isinstance(value,dict):
  for k,v in value.items():
   if not isinstance(k,str) or MARKER.search(k):found.append(path+'.<prohibited-field>')
   found+=leak_paths(v,path+'.'+str(k))
 elif isinstance(value,(list,tuple)):
  for i,v in enumerate(value):found+=leak_paths(v,path+'['+str(i)+']')
 elif isinstance(value,str):
  if MARKER.search(value):found.append(path)
 elif value is not None and type(value) not in {int,float,bool}:found.append(path+'.<unclassified-container>')
 return found


def canonical_constraints(ec):
 if not isinstance(ec,dict):return {'UNCLASSIFIED_ENDPOINT':ec}
 out={}
 for k,v in ec.items():
  if isinstance(v,list):out[k]=sorted(v,key=lambda x:h_obj(x))
  else:out[k]=v
 return out


def semantic_candidate(c):
 # Raw annotations are retained outside this executable identity. They cannot
 # supply predicates; output admission separately rejects unknown annotation text.
 operative={k:v for k,v in c.items() if k not in {'candidate_local_id','assumptions','falsifiers','plausibility_rank_ordinal','candidate_origin','model_relative_plausibility_NOT_frequency','model_reference','class_key'}}
 if 'endpoint_constraints' in operative:operative['endpoint_constraints']=canonical_constraints(operative['endpoint_constraints'])
 return operative


def isin(value,values):
 return isinstance(value,str) and value in values


def output_findings(candidate):
 problems=leak_paths(candidate)
 if not isinstance(candidate,dict):return problems+['CANDIDATE_NOT_OBJECT']
 problems+=['UNCLASSIFIED_CANDIDATE_FIELD:'+str(k) for k in set(candidate)-CANDIDATE_KEYS]
 if not isin(candidate.get('candidate_kind'),KINDS):problems+=['UNKNOWN_CANDIDATE_KIND']
 if not isin(candidate.get('route_kind_id'),ROUTES):problems+=['UNKNOWN_ROUTE']
 local_id=candidate.get('candidate_local_id')
 if not isinstance(local_id,str) or not (re.fullmatch(r'C_FROZEN_[0-9]+',local_id) or re.fullmatch(r'SEM_[0-9a-f]{64}',local_id) or local_id in {'G15_SECOND_ENDPOINT_CLASS','A_PARAPHRASE'}):problems+=['UNREGISTERED_LOCAL_ID_GRAMMAR']
 if 'plausibility_rank_ordinal' in candidate and (type(candidate['plausibility_rank_ordinal']) is not int or candidate['plausibility_rank_ordinal']<0):problems+=['UNCLASSIFIED_ORDINAL']
 if 'model_reference' in candidate and not isin(candidate['model_reference'],{'see proposal record'}):problems+=['UNCLASSIFIED_MODEL_SOURCE']
 if 'candidate_origin' in candidate and not isin(candidate['candidate_origin'],{'LLM_PROPOSAL','FROZEN_LAB'}):problems+=['UNCLASSIFIED_PROPOSAL_SOURCE']
 if 'counterpart_ref' in candidate and candidate['counterpart_ref']!='F_EXISTING':problems+=['UNISSUED_COUNTERPART']
 if 'requires_joint_propensity' in candidate and type(candidate['requires_joint_propensity']) is not bool:problems+=['UNCLASSIFIED_JOINT_REQUEST']
 ec=candidate.get('endpoint_constraints')
 if not isinstance(ec,dict):return problems+['ENDPOINT_NOT_OBJECT']
 problems+=['UNCLASSIFIED_ENDPOINT_FIELD:'+str(k) for k in set(ec)-EC_KEYS]
 for k,v in ec.items():
  if k=='time_or_interval':
   if v!='T_ENCOUNTER_LAB_WINDOW':problems+=['UNCLASSIFIED_CLOCK']
  elif k=='place':
   if not isin(v,PLACES):problems+=['UNCLASSIFIED_PLACE']
  elif k=='required_state_predicates':
   if not isinstance(v,list):problems+=['PREDICATES_NOT_LIST'];continue
   for p in v:
    if not isinstance(p,dict) or set(p)!={'field','equals'}:problems+=['UNCLASSIFIED_PREDICATE'];continue
    if p['field']=='place' and isin(p['equals'],PLACES):continue
    if p['field']=='availability_status' and isin(p['equals'],{'available_for_encounter','unavailable'}):continue
    if p['field']=='material_position' and isin(p['equals'],{'waged_repair','waged_finishing'}):continue
    problems+=['UNISSUED_ENDPOINT_PREDICATE']
  else:
   vocab={'required_relation_objective_refs':{'REL_ENCOUNTER_WITNESSED'},'second_parent_structure_and_position_constraints':{'waged_artisan_local','evening_class_attendee'},'conception_witness_requirements':{'ENCOUNTER_WITNESS_MIN_1'},'admissible_world_context_refs':set()}.get(k,set())
   if not isinstance(v,list) or any(not isinstance(x,str) or x not in vocab for x in v):problems+=['UNCLASSIFIED_ENDPOINT_SOURCE:'+k]
 for k in ['assumptions','falsifiers']:
  v=candidate.get(k,[])
  if not isinstance(v,list) or any(not isinstance(x,str) or x not in SAFE_ANNOTATIONS for x in v):problems+=['UNCLASSIFIED_PROSE:'+k]
 # No base64/hex/url decode heuristics: text outside the finite grammar is held.
 return sorted(set(problems))


def visible_prompt_parts(anchor,target,world,route):
 findings=[]
 def closed(obj,allowed,path):
  if not isinstance(obj,dict):findings.append(path);return REDACTED
  out={}
  for k,v in obj.items():
   if k not in allowed or leak_paths({k:v}):
    safe_key=k if k in {'future_child_outcome_label','future_child_personality','future_child_desired_adversity_tag','future_child_health_outcome','future_child_education_outcome','any_field_derived_from_future_child'} else 'UNCLASSIFIED_FIELD_'+str(len(out))
    out[safe_key]=REDACTED;findings.append(path+'.<withheld-field>')
   else:out[k]=v
  return out
 # Bind historical psyche to the actual frozen prefix. Unknown extra content is
 # never delegated to a model for interpretation. Full resolution is separate.
 history=anchor.get('history_events',[]);ids={e.get('event_id') for e in history}
 allowed_labels={e.get('payload',{}).get(k) for e in history for k in ['attitude','practice','striving']};allowed_labels.discard(None)
 psyche={}
 for d in ['attitudes','practices','strivings']:
  items=anchor.get('psyche',{}).get(d,[]);clean=[]
  if not isinstance(items,list):items=[];findings.append('psyche.'+d)
  for item in items:
   if not isinstance(item,dict) or set(item)-{'attitude','practice','striving','causal_event_refs','formation_event_ref','formed_value'} or leak_paths(item):findings.append('psyche.'+d);continue
   label=item.get({'attitudes':'attitude','practices':'practice','strivings':'striving'}[d]);refs=item.get('causal_event_refs',[])
   if label not in allowed_labels or not isinstance(refs,list) or any(x not in ids for x in refs):findings.append('psyche.'+d);continue
   # Only the label and resolvable reference list are model-visible; numeric
   # formed values stay with the transition owner, not arbitrary nested text.
   from .history import derive_psyche
   expected=derive_psyche(history)
   clean.append(dict(item) if item in expected.get(d,[]) else {k:v for k,v in item.items() if k!='formed_value'})
  psyche[d]=clean
 for k in set(anchor.get('psyche',{}))-set(psyche):psyche['UNCLASSIFIED_FIELD_'+str(len(psyche))]=REDACTED;findings.append('psyche.<withheld-field>')
 a={k:anchor.get(k) for k in ['actor_id','variant','t_preconception','known_counterpart_identity_ref_or_null','already_generated_child_refs','mobility_history_present']}
 # Provenance-bound identity payload is allowed only at this explicit boundary.
 if (leak_paths(a) or not isin(a['actor_id'],{'LAB_MOTHER_M0','LAB_MOTHER_M2','LAB_MOTHER_MP'})
     or not isin(a['variant'],{'M0','M2','MP'}) or a['t_preconception']!='T_PRECONCEPTION_LAB_BOUNDARY'
     or (a['known_counterpart_identity_ref_or_null'] is not None and a['known_counterpart_identity_ref_or_null']!='F_EXISTING')
     or a['already_generated_child_refs'] not in [[],['LAB_OLDER_CHILD_O1']]):
  a={k:REDACTED for k in a};findings.append('anchor.identity')
 a['psyche']=psyche
 routes=anchor.get('route_availability',[])
 if not isinstance(routes,list) or any(not isin(x,ROUTES) for x in routes):a['route_availability']=REDACTED;findings.append('anchor.routes')
 else:a['route_availability']=list(routes)
 t=closed(target,{'target_id','mother_anchor_hash','target_status','known_counterpart_ref_or_null','planned_boundary_time_or_interval','candidate_generation_policy_ref','cursor_increments','focal_slot_ref','prohibited_future_input_hash'},'target')
 # Opaque target fields are not displayed; exact source hashes remain in receipts.
 for k in list(t):
  if k not in {'target_status','cursor_increments'}:t[k]=REDACTED
 if t.get('target_status') is not None and not isin(t.get('target_status'),{'TARGET_PENDING','PENDING_NONCAUSAL'}):t['target_status']=REDACTED;findings.append('target.status')
 w=closed(world,{'world_id','premise_version','routes','institutions'},'world')
 for k in list(w):
  if k=='world_id':
   if not isin(w[k],{'WORLD_SYNTHTIC_LAB_001','G13_WORLD'}):w[k]=REDACTED;findings.append('world.id')
  elif k=='premise_version':
   if w[k]!='SYNTH_WORLD@1.0.0':w[k]=REDACTED;findings.append('world.version')
  elif k=='routes':
   w[k]=[dict(route_id=x['route_id']) for x in w[k] if isinstance(x,dict) and isin(x.get('route_id'),ROUTES)] if isinstance(w[k],list) else REDACTED
  elif k=='institutions':
   w[k]=[dict(inst_id=x['inst_id']) for x in w[k] if isinstance(x,dict) and isin(x.get('inst_id'),PLACES)] if isinstance(w[k],list) else REDACTED
 rf=route if (isinstance(route,str) and route in ROUTES) or route is None else REDACTED
 if rf==REDACTED:findings.append('route_filter')
 return a,t,w,rf,findings
