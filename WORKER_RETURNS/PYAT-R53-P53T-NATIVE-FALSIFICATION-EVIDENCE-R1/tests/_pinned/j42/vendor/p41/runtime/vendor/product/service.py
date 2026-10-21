"""Generic sourcefree selected-world -> exact progressive evidence service."""
from copy import deepcopy
from rawlsing_next.pre553_empirical_objects import semantic_hash
from .empirical import GenericProgressiveProvider,build_source
from .world import SelectedWorldCatalog
CONTRACT='E04_GENERIC_SELECTED_WORLD_POSSIBILITY_SERVICE_CANDIDATE@1'

class GenericSelectedWorldService:
    def __init__(self,*,empirical_changed=False,structural_revision=False,extra_field=None,support_loss=False,same_marginals=False,sanction_revision=False):
        self.catalog=SelectedWorldCatalog(build_source(changed=empirical_changed,support_loss=support_loss,same_marginals=same_marginals),structural_revision=structural_revision,extra_field=extra_field,sanction_revision=sanction_revision)
        self.provider=GenericProgressiveProvider(self.catalog.empirical);self.value_reads=[];self.receipts={}
    def select(self,**kwargs):return self.catalog.select(**kwargs)
    def structural(self,snapshot,key,consumer):
        value=self.catalog.read(snapshot,key)
        self.value_reads.append(dict(consumer=consumer,channel='structural',scope=key,source_ref=value.get('field_ref',value.get('requested_ref')),state=value['state'],value_read=value.get('value'),native_unit=value.get('unit'),snapshot_ref=snapshot.snapshot_hash))
        return value
    def possibilities(self,snapshot,*,target='Y',conditions=(('A',1),('B',1),('C',1)),consumer='GENERIC'):
        source=self.catalog.read(snapshot,'empirical')
        if source['state']!='SUPPORTED_TEST_ONLY':
            self.value_reads.append(dict(consumer=consumer,channel='empirical',scope='empirical',state=source['state'],value_read=None,snapshot_ref=snapshot.snapshot_hash))
            return dict(state=source['state'],steps=[],dependencies=['empirical'],source_ref=source.get('source_universe_ref',source.get('requested_ref')))
        expected=self.catalog.empirical_identity()
        if any(source.get(k)!=expected[k] for k in ('source_universe_ref','release_ref','risk_set_ref','rows_hash','permission_root')):raise ValueError('SOURCE_TO_QUERY_BINDING_MISMATCH')
        steps=self.provider.progressive(target,conditions)
        for step in steps:
            self.value_reads.append(dict(consumer=consumer,channel='empirical',scope='empirical',state=step['state'],evidence_ref=step.get('evidence_ref'),source_ref=step.get('source_universe_ref'),release_ref=step.get('release_ref'),value_read=deepcopy(step['cells']),denominator=step['denominator'],query_condition_order=deepcopy(step['conditioners']),target=target,snapshot_ref=snapshot.snapshot_hash))
        return dict(state='PRODUCTIVE_TEST_ONLY' if all(s['state']=='EXACT_SUPPORTED' for s in steps) else 'PARTIAL_TYPED_EMPIRICAL_SUPPORT',steps=steps,dependencies=['empirical'],native_time=expected['field_time'],claim_ceiling='SOURCE_LOCAL_EMPIRICAL_POSSIBILITY_NOT_CAUSAL_OR_PERSONAL',source_root=expected['permission_root'])
    def _record(self,material):
        material=deepcopy(material);material.update(service_contract=CONTRACT,grade='TEST_ONLY_SOURCEFREE_CANDIDATE',operative_N9=False,operative_N10W=False,new_issuer=False,actor_executions=0,model_calls=0)
        h=semantic_hash(material);self.receipts[h]=deepcopy(material);return dict(receipt_hash=h,material=material)
    def structural_product(self,snapshot,keys=('civil_open',)):
        if not isinstance(keys,(tuple,list)) or not keys or len(set(keys))!=len(keys):raise ValueError('NONEMPTY_EXACT_STRUCTURAL_READSET_REQUIRED')
        values={key:self.structural(snapshot,key,'GENERIC_STRUCTURAL_READER') for key in keys}
        return self._record(dict(consumer='GENERIC_STRUCTURAL_READER',state='VALUES_READ' if all(v['state']=='SUPPORTED_TEST_ONLY' for v in values.values()) else 'PARTIAL_TYPED_VALUES_READ',values=values,dependencies=list(keys),snapshot_ref=snapshot.snapshot_hash))
    def invalidate(self,scope):
        revocation=self.catalog.revoke(scope)
        affected=sorted(h for h,m in self.receipts.items() if scope in m.get('dependencies',[]))
        retained=sorted(h for h in self.receipts if h not in affected)
        return dict(revocation=revocation,invalidated_for_fresh_use=affected,unaffected=retained,historical_receipts_retained=True,old_receipt_hashes=list(self.receipts))
    def historical_receipt(self,receipt_hash):
        m=deepcopy(self.receipts[receipt_hash]);assert semantic_hash(m)==receipt_hash
        return dict(receipt_hash=receipt_hash,material=m,archival_only=True,fresh_use_authorized=False)
