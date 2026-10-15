"""NEW TEST_ONLY selected snapshot boundary over accepted M4/M5 carriage.

No N9/OC05 installation, current-world issuer or measured structural field is
claimed. Selection clocks are explicit synthetic inputs, never the wall clock.
"""
from copy import deepcopy
from datetime import date
from dataclasses import dataclass
from rawlsing_next import m4_v557_v558_publication_repository as m4
from rawlsing_next import m5_runtime_rsc_peer_prior as m5
from rawlsing_next.pre553_empirical_objects import canonicalize,semantic_hash
SCHEMA='E04_TEST_ONLY_SELECTED_WORLD_SNAPSHOT@1'
ROOT='TEST_ONLY_E04_SOURCE_ROOT'
UNITS={'training_access':'modeled policy eligibility boolean','training_fee':'modeled resource tokens','exit_cost':'modeled resource tokens','civil_sanction':'modeled sanction boolean','civil_open':'modeled route eligibility boolean'}
BASE={'training_access':True,'training_fee':2,'exit_cost':2,'civil_sanction':False,'civil_open':True}

def iso(value):
    if not isinstance(value,str) or len(value)!=10:raise ValueError('EXACT_ISO_DATE_REQUIRED')
    d=date.fromisoformat(value)
    if d.isoformat()!=value:raise ValueError('EXACT_ISO_DATE_REQUIRED')
    return d

def authority(label):return m4.AuthorityRef('urn:test:e04:'+label,'TEST_ONLY@1',semantic_hash(['TEST_ONLY',label]))
def ref(kind,value):return m4.ExactRef(kind,'urn:test:e04:'+kind.lower()+':'+str(value),semantic_hash(value))

@dataclass(frozen=True)
class SelectedSnapshot:
    material:dict
    snapshot_hash:str
    def verify(self):
        if semantic_hash(self.material)!=self.snapshot_hash:raise ValueError('SNAPSHOT_CONTENT_HASH_MISMATCH')

class SelectedWorldCatalog:
    def __init__(self,empirical,*,structural_revision=False,extra_field=None,sanction_revision=False):
        self.empirical=empirical;self.revoked=set();self.revocations=[];self.trace=[]
        self.records=[];self.handles={};self._snapshots={}
        for key,value in BASE.items():self._publish(key,value,'2026-01-01','2028-01-01','2026-03-01',revision=1)
        if structural_revision:
            self._publish('training_access',False,'2027-01-01','2028-01-01','2027-06-01',revision=2)
            self._publish('exit_cost',8,'2027-01-01','2028-01-01','2027-06-01',revision=2)
        if sanction_revision:self._publish('civil_sanction',True,'2027-01-01','2028-01-01','2027-06-01',revision=2)
        if extra_field is not None:self._publish('unrelated_stock',extra_field,'2026-01-01','2028-01-01','2026-03-01',revision=1,unit='modeled inventory units')
        self.catalog_hash=semantic_hash(dict(records=self.records,empirical=self.empirical_identity()))
    def empirical_identity(self):
        w=self.empirical;s=w['source']
        return dict(source_universe_ref=s['universe'].ref.as_dict(),release_ref=s['release_ref'].as_dict(),risk_set_ref=canonicalize(s['risk_refs']['R']),rows_hash=w['rows_hash'],permission_root=ROOT,publication=w['publication'],field_time=s['universe'].field_or_reference_time,native_geography=s['universe'].sampling_geography,native_unit='SYNTHETIC_INDIVIDUAL_RESPONDENT',grade='SYNTHETIC_NOT_OBSERVED')
    def verify(self):
        if semantic_hash(dict(records=self.records,empirical=self.empirical_identity()))!=self.catalog_hash:raise ValueError('CATALOG_CONTENT_CHANGED')
    def _publish(self,key,value,start,end,published,*,revision,unit=None):
        unit=unit or UNITS[key]
        payload=dict(schema='E04_MODELED_FIELD_VALUE@1',key=key,value=value,unit=unit,scope='US-NATIONAL_SYNTHETIC_FIXTURE',effective_from=start,effective_to=end,publication=published,source_root=ROOT,revision=revision,epistemic_class='MODELED_NOT_OBSERVED',public_rule='TEST_ONLY_INSTITUTIONAL_ROUTE_RULE@1')
        obj=m4.make_structural_object(producer_family='V555',semantic_class='E04_TEST_ONLY_FIELD',object_id='urn:test:e04:field:'+key+':'+str(revision),schema_id='E04_MODELED_FIELD_VALUE',schema_version='1',typed_state='SUPPORTED',producer_allowed_uses=('CONTEXT',),payload=payload,source_stage='E04_SYNTHETIC_PRODUCER_NOT_ISSUED_V555')
        record=dict(key=key,unit=unit,start=start,end=end,publication=published,revision=revision,ref=obj.ref.as_dict())
        self.records.append(record);self.handles[obj.content_hash]=obj
    def revoke(self,scope,reason='TEST_ONLY_PERMISSION_REVOCATION'):
        if scope!='empirical' and scope not in {r['key'] for r in self.records}:raise ValueError('UNKNOWN_PERMISSION_SCOPE')
        self.revoked.add(scope);receipt=dict(scope=scope,reason=reason,index=len(self.revocations),prior_ref=semantic_hash(self.revocations));self.revocations.append(receipt);return deepcopy(receipt)
    def permitted(self,key):return key not in self.revoked
    def _select_record(self,key,valid_at,published_asof):
        candidates=[r for r in self.records if r['key']==key and iso(r['start'])<=iso(valid_at)<iso(r['end']) and iso(r['publication'])<=iso(published_asof)]
        if not candidates:return None
        candidates.sort(key=lambda r:(r['start'],r['revision']))
        if len(candidates)>1 and (candidates[-1]['start'],candidates[-1]['revision'])==(candidates[-2]['start'],candidates[-2]['revision']):raise ValueError('AMBIGUOUS_SELECTED_RECORD')
        return candidates[-1]
    def _resolve(self,record):
        obj=self.handles[record['ref']['content_hash']]
        if obj.ref.as_dict()!=record['ref'] or obj.payload['key']!=record['key'] or obj.payload['unit']!=record['unit'] or obj.payload['source_root']!=ROOT or obj.payload['publication']!=record['publication'] or obj.payload['effective_from']!=record['start'] or obj.payload['effective_to']!=record['end']:raise ValueError('SELECTED_NATIVE_PRODUCER_BINDING_MISMATCH')
        decision=m4.V557DecisionState.ALLOW_CONTEXT_ONLY if self.permitted(record['key']) else m4.V557DecisionState.DENY_CAUSAL_USE
        gov=m4.govern_v557(obj,decision_state=decision,v557_allowed_uses=('CONTEXT',) if self.permitted(record['key']) else (),authority_ref=authority('field-permission:'+record['key']))
        locator=m4.make_producer_locator(obj,gov,logical_collection_kind='E04_TEST_ONLY_SELECTED_FIELDS',authoritative_build_id='E04:'+obj.content_hash,authoritative_build_hash=obj.content_hash,producer_contract_id='E04_MODELED_NATIVE_FIELD@1',producer_contract_version='1',producer_contract_hash=semantic_hash('E04_MODELED_NATIVE_FIELD@1'),producer_rule_bindings=(authority('fixture-field-rule'),),provenance_locator='audit://E04_TEST_ONLY/'+record['key'])
        publication=m4.build_v557_publication_bundle((m4.V557PublicationEntry(obj,gov),))
        repo=m4.build_v558_repository_bundle(publication,(m4.RepositoryEntry(obj,gov,locator),))
        query=m4.make_context_query((m4.ContextQueryItem(m4.exact_resolution_key(locator),('CONTEXT',)),));resolution=m4.resolve_v558(repo,query)
        out=dict(state=resolution.receipt.result_state,field_ref=obj.ref.as_dict(),unit=record['unit'],selection_record_refs=[s.ref.as_dict() for s in resolution.selection_records],resolution_ref=resolution.receipt.ref.as_dict(),requested_permission='CONTEXT')
        self.trace.append(dict(call='resolve_v558',field=record['key'],output=deepcopy(out)))
        if not resolution.resolved_entries:return out
        currentness=m5.make_structural_currentness_receipt(resolution,state=m5.StructuralCurrentnessState.CURRENT,authority_ref=authority('TEST_ONLY_SELECTION_CURRENTNESS'),structural_currentness_basis_ref=ref('E04_TEST_SELECTION_BASIS',obj.ref.as_dict()),decision_effective_time_ref=ref('E04_TEST_SELECTION_TIME',[record['start'],record['publication']]))
        rsc=m5.materialize_resolved_structural_context(repo,query,resolution,currentness);validation=m5.validate_resolved_structural_context(rsc,repo,query,resolution,currentness)
        # Actual values-read: find the native selected producer object and read
        # its immutable payload. A caller cannot supply a value with the request.
        selected=resolution.resolved_entries[0].producer_object_ref
        producer=next(e.obj for e in repo.entries if e.obj.ref==selected)
        payload=canonicalize(producer.payload)
        out.update(state='SUPPORTED_TEST_ONLY',value=payload['value'],payload=payload,payload_hash=semantic_hash(payload),rsc_ref=rsc.ref.as_dict(),validation_ref=validation.ref.as_dict(),currentness_ref=currentness.ref.as_dict(),currentness_grade='CURRENT_TO_TEST_SELECTION_NOT_OPERATIVE_N9')
        self.trace.append(dict(call='materialize_resolved_structural_context+validate_resolved_structural_context+producer_payload_read',field=record['key'],producer_ref=selected.as_dict(),value_read=payload['value'],native_unit=payload['unit'],rsc_ref=rsc.ref.as_dict(),validation_ref=validation.ref.as_dict()))
        return out
    def select(self,*,mode='AS_OF',valid_at='2027-09-01',published_asof='2027-09-01',test_now=None,purpose='TEST_ONLY_CONTEXT'):
        self.verify();iso(valid_at);iso(published_asof)
        if purpose!='TEST_ONLY_CONTEXT':raise ValueError('SOURCEFREE_ONLY_PURPOSE_REQUIRED')
        if mode not in ('AS_OF','HISTORICAL','TEST_CURRENT'):raise ValueError('OPERATIVE_CURRENT_NOT_AUTHORIZED')
        if mode=='TEST_CURRENT' and (test_now is None or valid_at!=test_now or published_asof!=test_now):raise ValueError('EXPLICIT_TEST_CURRENT_CLOCK_REQUIRED')
        slots={}
        for key in sorted({r['key'] for r in self.records}):
            record=self._select_record(key,valid_at,published_asof)
            slots[key]=dict(state='UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK',attempted_refs=[r['ref'] for r in self.records if r['key']==key]) if record is None else self._resolve(record)
        empirical=self.empirical_identity();available=iso(published_asof)>=iso(empirical['publication']) and iso(valid_at)>=iso('2026-01-01')
        empirical['state']='SUPPORTED_TEST_ONLY' if available and self.permitted('empirical') else 'REVOKED' if not self.permitted('empirical') else 'UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK'
        material=dict(schema=SCHEMA,catalog_hash=self.catalog_hash,mode=mode,valid_at=valid_at,published_asof=published_asof,purpose=purpose,source_permission_root=ROOT,fields=slots,empirical=empirical,operative_N9=False,operative_CURRENT=False)
        h=semantic_hash(material);self._snapshots[h]=deepcopy(material)
        return SelectedSnapshot(deepcopy(material),h)
    def read(self,snapshot,key):
        self.verify();snapshot.verify()
        if self._snapshots.get(snapshot.snapshot_hash)!=snapshot.material:raise ValueError('UNREGISTERED_SELECTED_SNAPSHOT')
        if snapshot.material['catalog_hash']!=self.catalog_hash:raise ValueError('FOREIGN_SNAPSHOT_SUBSTITUTION')
        if not self.permitted(key):return dict(state='REVOKED',scope=key,requested_ref=snapshot.material['empirical'] if key=='empirical' else snapshot.material['fields'].get(key,{}).get('field_ref'))
        return deepcopy(snapshot.material['empirical'] if key=='empirical' else snapshot.material['fields'].get(key,dict(state='UNAVAILABLE_UNKNOWN_FIELD')))
