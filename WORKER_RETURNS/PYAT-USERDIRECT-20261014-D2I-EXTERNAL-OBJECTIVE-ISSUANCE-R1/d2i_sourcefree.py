"""D2I: isolated, non-issued documentary-number registry and historical reader.
No publisher binary custody, N5/N6 issuer, N7/EE13 issuance or operative N9/OC05.
"""
from __future__ import annotations
from copy import deepcopy
from datetime import date
from hashlib import sha256
import json

GSS, NCA = 'GSS_RURAL_LIGHTING', 'NCA_NATIONAL_DATA_SUBSCRIPTIONS'

class CourtHold(ValueError):
    def __init__(self, code):
        self.code=code; super().__init__(code)

def h(o):
    return sha256(json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def day(s):
    try: return date.fromisoformat(s)
    except (TypeError,ValueError): raise CourtHold('INVALID_CLOCK') from None

def verify(row):
    if row.get('test_only') is not True or row.get('issued') is not False or row.get('issuer_signature') is not None: raise CourtHold('ISSUER_FORGERY')
    if row.get('source_pdf_sha256') is not None or row.get('pdf_bytes_captured') is not False: raise CourtHold('UNVERIFIED_BINARY_CUSTODY')
    if row.get('status') not in ('AVAILABLE_TEST_ONLY','REVOKED_TEST_ONLY'): raise CourtHold('UNKNOWN_FIELD_STATE')
    if row.get('permission')!='NO_FIELD_OR_EE13_GRANT': raise CourtHold('PERMISSION_FORGERY')
    if row.get('role')==GSS:
        if row['source_url']!='https://census2021.statsghana.gov.gh/gssmain/fileUpload/reportthemesub/Volume%203K_Housing%20Characteristics_240222.pdf' or row['published_at']!='2022-02-24' or row['geography']!='GHANA_RURAL' or row['unit']!='OCCUPIED_DWELLING_UNIT_MAIN_LIGHTING': raise CourtHold('GSS_SOURCE_OR_UNIT')
        v=row['values']; n=v['rural_electric_total']; d=v['rural_occupied_total']
        if any(type(x)!=int or x<0 for x in (n,d,*v['electric_subtypes'].values())) or d<=0 or n>d or len(v['electric_subtypes'])!=5 or sum(v['electric_subtypes'].values())!=n or round(n*100/d,1)!=v['published_pct']: raise CourtHold('GSS_NUMERIC_INTEGRITY')
        if sorted(row['excluded'])!=['SECONDARY_HOUSING','VACANT_DWELLINGS']: raise CourtHold('GSS_DENOMINATOR_SCOPE')
    elif row.get('role')==NCA:
        if row['source_url']!='https://nca.org.gh/wp-content/uploads/2022/07/Q4-2021-statistical-Bulletin.pdf' or row['published_at']!='2022-07-08' or row['geography']!='GHANA_NATIONAL' or row['unit']!='ACTIVE_MOBILE_DATA_SUBSCRIPTIONS_90_DAY_ACTIVITY': raise CourtHold('NCA_SOURCE_OR_UNIT')
        v=row['values']
        if any(type(x)!=int or x<0 for x in (v['subscriptions'],v['prepaid'],v['postpaid'])) or v['prepaid']+v['postpaid']!=v['subscriptions']: raise CourtHold('NCA_NUMERIC_INTEGRITY')
        if row.get('unique_persons') is not False or row.get('rural_breakout') is not None: raise CourtHold('NCA_ECOLOGICAL_FALLACY')
    else: raise CourtHold('UNKNOWN_FIELD_ROLE')
    day(row['published_at'])
    return True

class Registry:
    def __init__(self, rows):
        self.by_ref={}; self.by_role={}
        for raw in rows:
            row=deepcopy(raw); verify(row)
            if row['role'] in self.by_role: raise CourtHold('DUPLICATE_ROLE')
            ref='D2I_TEST_ONLY_FIELD:'+h(row)
            self.by_ref[ref]=row;self.by_role[row['role']]=ref
        if set(self.by_role)!={GSS,NCA}: raise CourtHold('TWO_INDEPENDENT_FIELDS_REQUIRED')
    def read(self, ref):
        if ref not in self.by_ref: raise CourtHold('STALE_OR_UNKNOWN_SOURCE_REF')
        row=deepcopy(self.by_ref[ref]); verify(row); return row


def nonpooled_relation(registry):
    return {'grade':'N7_EE13_TEST_ONLY_UNISSUED','relation':'NONPOOLED_CONTEXTUAL_CO_PRESENCE_ONLY',
            'refs':[registry.by_role[GSS],registry.by_role[NCA]],'same_population':False,
            'same_unit':False,'correlation':False,'causal':False,'issued_EE13':False}

def historical_read(registry, relation, as_of, *, partial=False, mode='HISTORICAL_PUBLICATION_AWARE', requested_person=False, requested_pool=False, requested_correlation=False, requested_model=False):
    if mode!='HISTORICAL_PUBLICATION_AWARE': raise CourtHold('OC05_OR_CURRENT_UNISSUED')
    if requested_person or requested_pool or requested_correlation or requested_model: raise CourtHold('ECOLOGICAL_OR_CAUSAL_USE_FORBIDDEN')
    if (relation.get('grade')!='N7_EE13_TEST_ONLY_UNISSUED' or relation.get('relation')!='NONPOOLED_CONTEXTUAL_CO_PRESENCE_ONLY' or relation.get('issued_EE13') is not False or relation.get('same_population') is not False or relation.get('same_unit') is not False or relation.get('correlation') is not False or relation.get('causal') is not False): raise CourtHold('EE13_FORGERY_OR_POOLING')
    refs=[registry.by_role[GSS],registry.by_role[NCA]]
    if relation.get('refs')!=refs: raise CourtHold('STALE_RELATION_REFERENCES')
    cutoff=day(as_of); read={}; denials={}
    for role,ref in zip((GSS,NCA),refs):
        try:
            x=registry.read(ref)
            if x['status']!='AVAILABLE_TEST_ONLY': raise CourtHold('SOURCE_REVOKED')
            if cutoff<day(x['published_at']): raise CourtHold('NOT_YET_PUBLISHED')
            read[role]={'ref':ref,'publisher':x['publisher'],'observed':x['observed'],
                        'published_at':x['published_at'],'unit':x['unit'],'geography':x['geography'],
                        'values':deepcopy(x['values'])}
        except CourtHold as e: denials[role]=e.code
    state='TWO_VALUES_DEREFERENCED_TEST_ONLY' if len(read)==2 else 'PARTIAL_TEST_ONLY_NONPOSITIVE' if read and partial else 'REQUIRED_SOURCE_UNAVAILABLE_HOLD'
    if state=='REQUIRED_SOURCE_UNAVAILABLE_HOLD': read={}
    snapshot={'grade':'SOURCEFREE_TEST_ONLY_NO_ISSUANCE','operative_OC05':False,'N5N6_issued':False,
              'N7_EE13_issued':False,'as_of':as_of,'status':state,'value_slots':read,
              'denials':denials,'attempted_refs':refs,'same_population':False,
              'person_inference':False,'correlation':False,'model_use':False}
    snapshot['snapshot_hash']=h(snapshot);return snapshot

def diff(a,b):
    changes=[role for role in (GSS,NCA) if a['value_slots'].get(role)!=b['value_slots'].get(role)]
    return {'changed_source_roles':changes,'unaffected_source_roles':[x for x in (GSS,NCA) if x not in changes],
            'snapshot_changed':a['snapshot_hash']!=b['snapshot_hash'],'grade':'TEST_ONLY_DEPENDENCY_DIFF_NOT_B5'}
