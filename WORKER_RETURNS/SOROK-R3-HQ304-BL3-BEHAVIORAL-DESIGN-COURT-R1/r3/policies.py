"""Closed synthetic responders. No oracle, evaluator, source or external access."""
import json
POLICIES=frozenset(['aware','blind','first','position','metadata','origin_leak','standing_leak','capacity_leak'])
def decode(representation,budget=1):
 """One nonempty record/chunk: linear scalar records versus grouped context."""
 if type(budget) is not int or budget<1:raise ValueError('INVALID_READ_BUDGET')
 if set(representation)=={'entries'}:
  records=[{x['field']:x['value']} for x in representation['entries']]
 elif set(representation)=={'streams'}:
  records=[v for k,v in sorted(representation['streams'].items()) if v]
 elif set(representation)=={'retrieved_context','evidence_index'}:
  records=[representation['retrieved_context']]
 else:raise ValueError('UNKNOWN_LAWFUL_REPRESENTATION')
 state={}
 for record in records[:budget]:state.update(record)
 return state,dict(records_read=min(budget,len(records)),available_records=len(records),read_budget=budget)
def choose(state,public_notice):
 action='OTHER_UNSCORABLE'
 if 'asking_cost' in state:action='REQUEST_FEEDBACK' if state['asking_cost']=='low' else 'SILENCE'
 elif 'relation' in state:action='REQUEST_WITH_REPAIR' if state['relation']=='repair_after_criticism' else 'REQUEST_WITH_CONDITIONAL_CAUTION'
 elif 'alertness' in state:action='HEIGHTENED_GUARD' if state['alertness']=='elevated' else 'NEUTRAL_RESPONSE'
 elif 'recurrence' in state:action={'peer_corrective':'NARROWED_CONSULT','same_authority':'REPEATED_QUESTION','unrelated_kindness':'NO_ACTION'}[state['recurrence']]
 elif 'belief' in state:action='ACCEPT_CERTIFICATE' if public_notice=='record entered by registrar' else 'NO_STANDING_CHANGE_ACTION'
 elif 'capacity' in state or 'practiced' in state:action='POLICING_CANDIDATE' if state.get('practiced') is True and state.get('capacity') is True else 'NO_SANCTION'
 belief=state.get('belief','NOT_ASKED')
 standing=('RECORDED' if public_notice=='record entered by registrar' else 'UNRECORDED') if 'belief' in state else 'NOT_ASKED'
 return dict(action=action,belief_report=belief,standing_report=standing,origin_claim='NO_CLAIM')
def respond(packet,policy,dispatch_position=0,budget=1):
 if policy not in POLICIES:raise ValueError('UNREGISTERED_SYNTHETIC_POLICY')
 if policy=='aware':state,receipt=decode(packet['representation'],budget)
 else:state=packet['facts']['organization'];receipt={'representation_read':False}
 answer=choose(state,packet['facts']['public_notice'])
 if policy=='first':answer['action']=packet['menu'][0]
 elif policy=='position':answer['action']=packet['menu'][0] if dispatch_position%3==1 else 'OTHER_UNSCORABLE'
 elif policy=='metadata':answer['action']=packet['menu'][0] if int(packet['response_id'][-1],16)%2==0 else 'OTHER_UNSCORABLE'
 elif policy=='origin_leak':answer['origin_claim']='CLAIMS_ORIGIN'
 elif policy=='standing_leak' and 'belief' in state:
  answer['standing_report']='RECORDED'
  if answer['belief_report']=='UNCERTAIN':answer['belief_report']='CONFIDENT'
 elif policy=='capacity_leak' and ('practiced' in state or 'capacity' in state):answer['action']='POLICING_CANDIDATE'
 if answer['action'] not in packet['menu']:answer['action']='OTHER_UNSCORABLE'
 return json.dumps(answer,sort_keys=True,separators=(',',':')),receipt
