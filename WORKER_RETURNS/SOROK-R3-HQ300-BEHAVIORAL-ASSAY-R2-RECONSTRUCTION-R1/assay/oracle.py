"""Evaluator-only proposed lawful sets. Never imported by provider policy.

Historical scope: LAB1 lawful sets, not an accepted psychological prediction.
Scientific independence/custody still requires the subsequent external reviewer.
"""
from .scoring import IntegrityError,validate_key


def proposed_key(cases):
    out={}
    for c in cases:
        f={e['field']:e['value'] for e in c['history']};k=c['k']
        actions={
         'K1':lambda: ['REQUEST_FEEDBACK'] if f['asking_cost']=='low' else ['SILENCE','APPEAL'],
         'K2':lambda: ['REQUEST_WITH_REPAIR'] if f['relation']=='repair_after_criticism' else ['REQUEST_WITH_CONDITIONAL_CAUTION'],
         'K3':lambda: ['HEIGHTENED_GUARD'] if f['alertness']=='elevated' else ['NEUTRAL_RESPONSE'],
         'K4':lambda: {'peer_corrective':['NARROWED_CONSULT'],'same_authority':['REPEATED_QUESTION'],'unrelated_kindness':['NO_ACTION']}[f['recurrence']],
         'K5':lambda: (['ACCEPT_CERTIFICATE','REMAIN_DOUBTFUL'] if f['belief']=='UNCERTAIN' else ['ACCEPT_CERTIFICATE']) if c['world']['ratification']['issuer']=='fixture_registrar' else ['NO_STANDING_CHANGE_ACTION','REMAIN_DOUBTFUL'],
         'K6':lambda: ['POLICING_CANDIDATE','NO_SANCTION'] if f['practiced'] and c['position']['capacity'] else ['NO_SANCTION'],
        }[k]()
        out[c['id']]=dict(actions=actions,belief_report=f.get('belief','NOT_ASKED'),
                        standing_report=('RECORDED' if c['world']['ratification']['issuer']=='fixture_registrar' else 'UNRECORDED') if k=='K5' else 'NOT_ASKED',origin_claim='NO_CLAIM')
    validate_key(out)
    return out


def audit_legality(case,answer):
    """Alternative rejection-rule channel, no frozen key or key function call."""
    h={e['field']:e['value'] for e in case['history']};a=answer['action'];k=case['k']
    if answer['origin_claim']!='NO_CLAIM':return False
    if answer['belief_report']!=h.get('belief','NOT_ASKED'):return False
    r=case['world'].get('ratification',{})
    official=(r.get('admission'),r.get('issuer'),r.get('scope'),r.get('notice'))==('ADMITTED','fixture_registrar','certification','signed_record')
    report=('RECORDED' if official else 'UNRECORDED') if k=='K5' else 'NOT_ASKED'
    if answer['standing_report']!=report:return False
    if k=='K1':return (a=='REQUEST_FEEDBACK' and h['asking_cost']=='low') or (a in {'SILENCE','APPEAL'} and h['asking_cost']=='high')
    if k=='K2':return (a,h['relation']) in {('REQUEST_WITH_REPAIR','repair_after_criticism'),('REQUEST_WITH_CONDITIONAL_CAUTION','approval_conditional_on_agreement')}
    if k=='K3':return (a=='HEIGHTENED_GUARD')==(h['alertness']=='elevated') and a in {'HEIGHTENED_GUARD','NEUTRAL_RESPONSE'}
    if k=='K4':return (a,h['recurrence']) in {('NARROWED_CONSULT','peer_corrective'),('REPEATED_QUESTION','same_authority'),('NO_ACTION','unrelated_kindness')}
    if k=='K5':
        if a=='ACCEPT_CERTIFICATE':return official
        if a=='NO_STANDING_CHANGE_ACTION':return not official
        return a=='REMAIN_DOUBTFUL' and (not official or h['belief']=='UNCERTAIN')
    if k=='K6':return a=='NO_SANCTION' or (a=='POLICING_CANDIDATE' and h['practiced'] is True and case['position']['capacity'] is True)
    return False


def check_key(cases,key,universe):
    validate_key(key)
    if set(key)!={c['id'] for c in cases}:raise IntegrityError('ORACLE_CASE_COMPLETENESS')
    for c in cases:
        expected=key[c['id']]
        for action in universe:
            result=audit_legality(c,dict(action=action,belief_report=expected['belief_report'],standing_report=expected['standing_report'],origin_claim='NO_CLAIM'))
            if result!=(action in expected['actions']):raise IntegrityError('ORACLE_RULE_DISAGREEMENT')
