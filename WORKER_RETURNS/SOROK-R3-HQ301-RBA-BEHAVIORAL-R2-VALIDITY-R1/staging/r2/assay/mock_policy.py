"""Registered inert policies. No oracle access, network or actor generation."""
import json
from .scoring import FREE_TEXT_RUBRIC

POLICIES={'lawful','first','metadata','malformed','unscorable','order_sensitive','budget_fragile','origin_leak','belief_overwrite'}


def respond(request,policy):
    p=request['packet'];s=p['facts']['organization'];action='OTHER_UNSCORABLE'
    # Sourcefree hand-written plumbing control, NEVER behavioral evidence.
    if 'asking_cost' in s:action='REQUEST_FEEDBACK' if s['asking_cost']=='low' else 'SILENCE'
    elif 'relation' in s:action='REQUEST_WITH_REPAIR' if s['relation']=='repair_after_criticism' else 'REQUEST_WITH_CONDITIONAL_CAUTION'
    elif 'alertness' in s:action='HEIGHTENED_GUARD' if s['alertness']=='elevated' else 'NEUTRAL_RESPONSE'
    elif 'recurrence' in s:action={'peer_corrective':'NARROWED_CONSULT','same_authority':'REPEATED_QUESTION','unrelated_kindness':'NO_ACTION'}[s['recurrence']]
    elif 'belief' in s:action='ACCEPT_CERTIFICATE' if p['facts']['public_notice']=='record entered by registrar' else 'NO_STANDING_CHANGE_ACTION'
    elif 'practiced' in s:action='POLICING_CANDIDATE' if s['practiced'] and s['capacity'] else 'NO_SANCTION'
    belief=s.get('belief','NOT_ASKED');standing=('RECORDED' if p['facts']['public_notice']=='record entered by registrar' else 'UNRECORDED') if 'belief' in s else 'NOT_ASKED'
    origin='NO_CLAIM'
    if policy in ('first','order_sensitive'):action=p['menu'][0]
    if policy=='metadata':
        # Prior R1 lookup cannot recover a contrast from random response UUIDs.
        action='SILENCE' if 'H_PUNITIVE' in p['response_id'] else 'OTHER_UNSCORABLE'
    if policy=='unscorable' or (policy=='budget_fragile' and request['max_tokens']<256):action='OTHER_UNSCORABLE'
    if policy=='origin_leak':origin='CLAIMS_ORIGIN'
    if policy=='belief_overwrite' and belief=='UNCERTAIN' and standing=='RECORDED':belief='CONFIDENT'
    if policy=='malformed':return 'not-json'
    out=dict(action=action,belief_report=belief,standing_report=standing,origin_claim=origin)
    if request.get('response_format')=='free_text_fixture':
        return json.dumps(dict(text=FREE_TEXT_RUBRIC.get(action,'unclear'),belief_report=belief,standing_report=standing,origin_claim=origin))
    return json.dumps(out)
