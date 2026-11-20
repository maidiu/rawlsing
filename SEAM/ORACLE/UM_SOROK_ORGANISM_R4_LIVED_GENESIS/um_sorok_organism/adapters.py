"""Explicit interoperability contracts with live Rawlsing owners.

NO protected repository calls are made by this research package. The adapter
accepts P3 results from the qualified upstream read API, never reads or writes
protected SQLite tables directly, and refuses missing semantic qualification.
"""
from .types import copy, GRADE, stable_id

class ContractHold(RuntimeError): pass


def from_p3_records(records, *, actor, root, branch, clock):
    """A cautious *supplementary read model*, not a second state writer.

    P3's query(project=...,counterpart=...,as_of=...) is scoped and does not
    promise global enumeration. Caller must enumerate only known lawful scopes.
    Payloads not adhering to the typed functional surface remain unresolved.
    """
    forms={};unresolved=[]
    for rec in records:
        if rec.get('actor')!=actor or rec.get('root')!=root or rec.get('branch')!=branch or rec.get('effective_from',float('inf'))>clock:
            raise ContractHold('P3_IDENTITY_OR_TIME_MISMATCH')
        payload=rec.get('payload',rec.get('payload_json',{}))
        if not isinstance(payload,dict):
            unresolved.append({'ref':rec.get('record_id'),'reason':'NONMAPPING_PAYLOAD'});continue
        semantic=payload.get('functional_semantics')
        if not semantic or not isinstance(semantic,dict) or not semantic.get('enables'):
            unresolved.append({'ref':rec.get('record_id'),'reason':'NO_ISSUED_FUNCTIONAL_SEMANTICS'});continue
        ident=rec['record_id']
        forms[ident]={'id':ident,'actor':actor,'kind':rec['kind'],
            'content':copy(semantic.get('content','')), 'cues':copy(semantic.get('cues',[])),
            'scope':copy(semantic.get('scope',{})), 'enables':copy(semantic['enables']),
            'origin':copy(rec.get('causal_parents',[])), 'grade':rec.get('grade',GRADE),
            'lifecycle':semantic.get('lifecycle','ACTIVE'),
            'strength':semantic.get('strength',.5),
            'external_source':'P3_READ_ONLY_NO_AUTHORITY_PROMOTION'}
    return {'forms':forms,'unresolved':unresolved,'source':'P3_SCOPED_QUERY',
            'read_only':True,'native_psychological_law_issued':False}


P2_P3_P6_INTEGRATION_CONTRACT={
    'base':'integration/pre-main-reconciliation-r1',
    'research_role':'SIDE_CAR_SIMULATION_AND_PURE_PROJECTIONS',
    'P2':'objective actor/world author; NEVER mutated from this package',
    'P3':'actor middle-state authority; normalized query is scoped; unknown forms HELD',
    'CAN009':'body owner; local organism is provisional and not a replacement',
    'ADP015':'relations/independent actors; local relations are world-owned fiction only',
    'ADP016_017':'memory/actor meaning; no automatic exposure-to-memory',
    'P6':'public actor-safe expression consumer, not a psychological author',
    'positive_first_consumer':'constitution->recruitment->proposed attempt->world->experience->development->later recruitment',
    'sourcefree_only':True,
    'native_owner_writer_rights':False,
    'source_science_issued':False,
    'protected_merge_rights':False,
}
