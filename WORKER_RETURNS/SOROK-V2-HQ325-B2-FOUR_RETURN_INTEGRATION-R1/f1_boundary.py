"""B2 optional F1 ingress-envelope guard, never the independent reference oracle.

This validates transport/source/owner invariants before any witness admission.
It does not manufacture a typed B1 history from F1's hypothetical prose/state.
"""
import hashlib,json


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()


def envelope_gate(case):
    p=case['proposal'];event=case['world']['event'];actors={a['id']:a for a in case['actors']}
    actor=actors.get(p['actor_id']);rules=case['rules'];sources={s['id']:s for s in case['sources']}
    reasons=[]
    if actor is None:return dict(status='DENIED',reasons=['ACTOR_UNKNOWN'])
    if p['event_ref']!=event['id'] or not event['admitted']:reasons.append('NO_ADMITTED_EVENT')
    if p['clock']<event['time']:reasons.append('FUTURE_EVENT')
    if p['clock']<actor['as_of']:reasons.append('STALE_CLOCK')
    if digest(actor['state'])!=p['prestate_hash']:reasons.append('STALE_PRESTATE')
    rule=rules.get(p['rule_ref'])
    if rule is None:reasons.append('UNREGISTERED_CAN008_RULE')
    elif rule['owner']!='CAN008':reasons.append('WRONG_CAN008_OWNER')
    if not case['permission'].get('actor_response'):reasons.append('CAN008_PERMISSION_DENIED')
    if not set(p['requires_caps']).issubset(actor['capacities']):reasons.append('CAPACITY_NOT_QUALIFIED')
    if p['probability_grade'] not in ('NONE','UNVALIDATED_TEST_HYPOTHESIS'):
        reasons.append('UNISSUED_PROBABILITY_AUTHORITY')
    if not set(p['meaning_modes']).issubset({'proposition','affect','practice','public','no_effect'}):
        reasons.append('UNTYPED_INTERPRETATION')
    for ref in p['observed_refs']:
        source=sources.get(ref)
        if not source or source['time']>p['clock'] or source['visible_to'] not in ('public',p['actor_id']):
            reasons.append('ACTOR_ACCESS_VIOLATION')
        elif source['kind']=='trace':reasons.append('INACCESSIBLE_TRACE_AS_CONSCIOUS_OBSERVATION')
    for ref in p['recruited_refs']:
        source=sources.get(ref)
        if not source or source['time']>p['clock']:reasons.append('INVALID_CAUSAL_SOURCE')
        elif source['visible_to'] not in ('public',p['actor_id']):reasons.append('FOREIGN_PRIVATE_CAUSAL_SOURCE')
        if source and source['kind']=='trace' and ref in p['observed_refs']:reasons.append('TRACE_EXPOSED')
    if any(ref not in sources or sources[ref]['kind']!='claim' for ref in p['claim_refs']):
        reasons.append('UNATTRIBUTED_CLAIM')
    if p.get('objective_thief_group') is not None:reasons.append('PEER_PREJUDICE_LAUNDERED_AS_FACT')
    if p.get('scripted_by_age') or p.get('direct_demographic_edge'):reasons.append('UNLICENSED_PSYCHOLOGICAL_SHORTCUT')
    if p.get('renderer_writes_cause'):reasons.append('RENDERER_CAUSAL_FORGERY')
    owner_by_domain={'mediator':'CAN011','practice':'CAN011','tension':'CAN011','memory':'ADP016',
                     'access':'ADP017','striving':'CAN010','relationship':'ADP015','external':'ADP019'}
    for effect in p['effects']:
        owner=owner_by_domain.get(effect['domain'])
        if effect['owner']!=owner:reasons.append('EFFECT_WRONG_OWNER')
        if effect['actor_id']!=p['actor_id']:reasons.append('CROSS_ACTOR_DIRECT_WRITE')
        if not case['permission'].get(effect['owner']):reasons.append('FOREIGN_OWNER_PERMISSION_DENIED')
        effect_rule=rules.get(effect['rule_ref'])
        if effect_rule is None or effect_rule['owner']!=effect['owner']:reasons.append('UNREGISTERED_EFFECT_RULE')
        if effect['prestate_hash']!=digest(actor['state']):reasons.append('EFFECT_STALE_PRESTATE')
        if effect['as_of']!=p['clock']:reasons.append('CROSS_OWNER_CLOCK_MISMATCH')
        if not set(effect['cause_refs']).issubset(set(p['recruited_refs'])|{event['id']}):
            reasons.append('EFFECT_CAUSE_NOT_RECRUITED')
    if reasons:return dict(status='DENIED',reasons=sorted(set(reasons)))
    if p['requires_owner_rule_missing']:return dict(status='DEFERRED',reasons=['OWNER_RULE_NOT_ISSUED'])
    return None # no implicit authorization to translate the remaining psychology


def unsupported_reason(case):
    proposal=case['proposal']
    if proposal['effects']:
        return 'F1 proposed '+','.join(e['domain'] for e in proposal['effects'])+' effect lacks the typed enacted-history/update-rule predicate required by pinned B1 CREATE mediator; no semantic substitution.'
    if proposal['actor_id']!='child':
        return 'Pinned B1 only implements focal child response; no typed initialization/response law for '+proposal['actor_id']+'.'
    return 'Frozen actor state and source prose do not supply B1 typed plan-comparison prehistory or a C07 comparable witness. Refuse to infer them from narrative; no exact native positive/empty mapping.'
