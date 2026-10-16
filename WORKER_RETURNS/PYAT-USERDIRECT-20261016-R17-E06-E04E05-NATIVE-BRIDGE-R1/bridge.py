"""E06 @1: explicit E04T provider injection into unmodified E05R serving.

No estimator, owner-module mutation, source issuer or installation is added.
Only Pre553AuthorityError becomes a grant-loss envelope; integrity/programming
errors remain errors and cannot be laundered into missing source support.
"""
from dataclasses import dataclass
from copy import deepcopy
import e04t_empirical as T
import e05_n9_selected_world_adapter as E
from product.service import GenericSelectedWorldService
from product.world import SelectedWorldCatalog
from product.nonparent import consume
from product.scenario import evaluate
from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_hq297_n9c_two_field_reader import TestOnlyRegistry

CONTRACT='E06_E04T_E05R_NATIVE_BRIDGE@1'
PROPOSALS=[dict(scenario_id='E06_INSTITUTIONAL',route='institutional'),dict(scenario_id='E06_CIVIL',route='civil')]

class BridgeDisabled(ValueError):pass

class E04TSelectedWorldService(GenericSelectedWorldService):
    """Named constructor seam. All service/read/record methods stay original."""
    def __init__(self,*,empirical_changed=False,support_loss=False,
                 structural_revision=True,sanction_revision=False):
        world=T.build_source(changed=empirical_changed,support_loss=support_loss)
        self.catalog=SelectedWorldCatalog(world,structural_revision=structural_revision,
                                          sanction_revision=sanction_revision)
        self.provider=T.GenericProgressiveProvider(world)
        self.value_reads=[]
        self.receipts={}

@dataclass(frozen=True)
class PreparedBridgeRead:
    request: object
    snapshot: object
    acceptance: object
    provider_binding: str

class NativeBridge:
    def __init__(self,registry_rows,*,enabled=False,**service_options):
        if enabled is not True:raise BridgeDisabled('E06_OFF_BY_DEFAULT_EXPLICIT_TRUE_REQUIRED')
        self.service=E04TSelectedWorldService(**service_options)
        self.provider=self.service.provider
        self.adapter=E.N9SelectedWorldAdapter(service=self.service,
                    registry=TestOnlyRegistry(deepcopy(registry_rows)))
        self._binding=self.provider._binding
        self._prepared={}

    def _verify_provider(self):
        if self.adapter.service is not self.service or self.service.provider is not self.provider or type(self.provider) is not T.GenericProgressiveProvider:
            raise ValueError('E06_PINNED_E04T_PROVIDER_SUBSTITUTED')
        if self.provider.world is not self.service.catalog.empirical or self.provider._identity()!=self._binding:
            raise ValueError('E06_ACCEPTED_PROVIDER_SOURCE_BINDING_CHANGED')

    def prepare(self,binding):
        self._verify_provider()
        q=E.N9SelectedWorldRequest.from_binding(binding)
        ss=self.adapter.build_snapshot(q)
        # Observe selected publication/use availability before any native query.
        if self.service.catalog.read(ss,'empirical')['state']=='SUPPORTED_TEST_ONLY':
            self.provider.progressive(q.empirical_target,q.empirical_conditions)
        acc=self.adapter.accept(q,ss)
        out=PreparedBridgeRead(q,ss,acc,self._binding)
        self._prepared[id(out)]=out
        return out

    def _envelope(self,p):
        return dict(schema=CONTRACT,grade='TEST_ONLY_SOURCEFREE_BRIDGE_CANDIDATE',
                    installed=False,independently_accepted_integration=False,
                    request=p.request.binding(),acceptance=p.acceptance.binding(),
                    provider_binding=self._binding,
                    provider_type=type(self.provider).__module__+'.'+type(self.provider).__name__,
                    e04t_current_grant_validation='ACTUAL_NATIVE_ATTACHED_REGISTRY_REQUIRED',
                    original_method_acceptance=dict(E04U='f1ca9c530f6f03053ca981b49eefc91b85be47b8',E05S='f524f60781e2e7e72278d04d6377fb1da877698a'))

    def read(self,p,*,scalar_only=False,supplied_consumers=None):
        self._verify_provider()
        if self._prepared.get(id(p)) is not p or p.provider_binding!=self._binding:
            raise ValueError('E06_FOREIGN_PREPARED_HANDOFF')
        if p.request.binding()!=self.adapter.acceptances[p.acceptance.acceptance_hash]['request_binding']:
            raise ValueError('E06_PREPARED_REQUEST_CHANGED')
        # This check uses the still-warm original E04T cache. E05R later clears
        # its provider cache as originally implemented; neither path may renew
        # the registry or replace this provider with the original E04 factory.
        try:
            if self.service.catalog.read(p.snapshot,'empirical')['state']=='SUPPORTED_TEST_ONLY':
                self.provider.progressive(p.request.empirical_target,p.request.empirical_conditions)
        except Pre553AuthorityError as exc:
            return self._grant_loss(p,exc,scalar_only=scalar_only)
        clients=[] if scalar_only else [consume(self.service,p.snapshot)['material'],
                                       evaluate(self.service,p.snapshot,deepcopy(PROPOSALS))['material']]
        if supplied_consumers is not None:clients=supplied_consumers
        receipt=self.adapter.serve(p.request,p.acceptance,p.snapshot,consumers=clients)
        out=self._envelope(p);out.update(state=receipt['state'],selected_world_receipt=receipt,
            successful_consumers=deepcopy(receipt['consumers']),
            native_query_validation_count=sum(x['call']=='CURRENT_NATIVE_QUERY_GRANT_VALIDATED' for x in self.provider.trace))
        return out

    def _grant_loss(self,p,error,*,scalar_only):
        """E04T warm refusal; E05R cold native partial or refusal, never renewal."""
        out=self._envelope(p)
        denials=[]
        # Before E05R clears cache, both exact original clients must separately
        # reject fresh use through the currently attached E04T registry.
        if not scalar_only:
            for name,call in [('NONPARENT_OPTIONS',lambda:consume(self.service,p.snapshot)),
                              ('CONCEPTION_SCENARIO_PROPOSALS',lambda:evaluate(self.service,p.snapshot,deepcopy(PROPOSALS)))]:
                before=set(self.service.receipts)
                try:call()
                except Pre553AuthorityError as exc:denials.append(dict(consumer=name,type=type(exc).__name__,reason=str(exc),fresh_receipt=False))
                else:raise AssertionError('E06_WARM_CLIENT_BYPASSED_WITHDRAWN_NATIVE_GRANT')
                assert before==set(self.service.receipts)
        # The original E05R clears the public projection cache. Original native
        # recomputation may correctly emit typed missing-authority steps rather
        # than an exception. Endorse only that actual no-values partial.
        partial=self.adapter.serve(p.request,p.acceptance,p.snapshot)
        if partial['state']!='TYPED_PARTIAL_SELECTED_WORLD' or partial['empirical_state']=='PRODUCTIVE_TEST_ONLY' or any(s['cells'] or s.get('evidence_ref') for s in partial['empirical_steps']):
            raise AssertionError('E06_E05R_BYPASSED_WITHDRAWN_NATIVE_GRANT')
        clients=[] if scalar_only else [consume(self.service,p.snapshot)['material'],
                                       evaluate(self.service,p.snapshot,deepcopy(PROPOSALS))['material']]
        partial=self.adapter.serve(p.request,p.acceptance,p.snapshot,consumers=clients)
        if any(c['consumer_material']['empirical']['state']=='PRODUCTIVE_TEST_ONLY' for c in partial['consumers']):
            raise AssertionError('E06_COLD_CLIENT_BYPASSED_WITHDRAWN_NATIVE_GRANT')
        out.update(state='DEPENDENT_EMPIRICAL_USE_REFUSED',selected_world_receipt=partial,
            successful_consumers=[],empirical_values=None,
            empirical_denial=dict(type=type(error).__name__,reason=str(error)),
            actual_warm_client_denials=denials,
            unrelated_structural_product=self.service.structural_product(p.snapshot,keys=tuple(p.request.structural_keys)),
            unrelated_native_field_readset=deepcopy(partial['native_field_readset']),
            fresh_empirical_use_authorized=False)
        return out

    def execute(self,binding,**options):return self.read(self.prepare(binding),**options)

    def archive(self,output):
        receipt=output['selected_world_receipt']
        if receipt is None:raise ValueError('NO_SERVED_E05R_RECEIPT_TO_ARCHIVE')
        return self.adapter.historical_receipt(receipt['receipt_hash'])
