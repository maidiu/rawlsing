"""E05A @1: sourcefree consumer packaging over EXACT accepted E05R @2.

No estimator, selected-world implementation, issuer or installation is added.
The accepted serving boundary owns request, clock, grant and client validation.
"""
from copy import deepcopy
from dataclasses import dataclass
import json
import e05_n9_selected_world_adapter as E
from product.service import GenericSelectedWorldService
from product.nonparent import consume
from product.scenario import evaluate
from rawlsing_next.pre553_hq297_n9c_two_field_reader import TestOnlyRegistry,GSS,NCA

CONTRACT='E05A_SOURCEFREE_METHOD_HANDOFF@1'
ACCEPTANCE_PIN='f524f60781e2e7e72278d04d6377fb1da877698a'
IMPLEMENTATION_PIN='84485d32c0088995f8dc664dc0517b2d27f2563d'
PROPOSALS=[dict(scenario_id='HANDOFF_INSTITUTIONAL',route='institutional'),dict(scenario_id='HANDOFF_CIVIL',route='civil')]

@dataclass(frozen=True)
class PreparedRead:
    request: object
    snapshot: object
    acceptance: object

class SourcefreeMethodHandoff:
    """Transport all actual request/acceptance/receipt material to a consumer.

    Default clients are the two exact original forward E04 clients. Separately
    granted reverse requests use explicit SCALAR_ONLY; no fake reverse client.
    Instances preserve accepted source/permission state, not a durable grant DB.
    """
    def __init__(self,adapter):
        self.adapter=adapter
        self._custody={}
        for role,ref in adapter.registry.refs_by_role().items():
            row=adapter.registry.dereference(ref)
            self._custody[role]=dict(accepted_fixture_ref=ref,fixture_only=row['fixture_only'],issued=row['issued'],source_pdf_sha256=row['source_pdf_sha256'],issuer_ref=row['issuer_ref'],permission=row['permission'],source_family=row['family'],publisher=row['publisher'],publication_date=row['publication_date'],observation_period=row['observation_period'],native_unit=row['native_unit'],native_geography=row['native_geography'],uncertainty=row['uncertainty'])

    def prepare(self,request_binding):
        request=E.N9SelectedWorldRequest.from_binding(request_binding)
        snapshot=self.adapter.build_snapshot(request)
        acceptance=self.adapter.accept(request,snapshot)
        return PreparedRead(request,snapshot,acceptance)

    def serve(self,prepared,*,consumer_mode='BOTH_ORIGINAL_CLIENTS',proposals=None):
        if consumer_mode not in ('BOTH_ORIGINAL_CLIENTS','SCALAR_ONLY'):
            raise ValueError('EXPLICIT_SOURCEFREE_CONSUMER_MODE_REQUIRED')
        clients=[]
        if consumer_mode=='BOTH_ORIGINAL_CLIENTS':
            proposals=deepcopy(PROPOSALS if proposals is None else proposals)
            # These are exact originals; E05R reexecutes/authenticates their full
            # returned material inside its serving boundary before endorsement.
            clients=[consume(self.adapter.service,prepared.snapshot)['material'],
                     evaluate(self.adapter.service,prepared.snapshot,proposals)['material']]
        receipt=self.adapter.serve(prepared.request,prepared.acceptance,prepared.snapshot,consumers=clients)
        return dict(schema=CONTRACT,status='SOURCEFREE_OFF_NOT_INSTALLED',
                    independent_method_acceptance=dict(commit=ACCEPTANCE_PIN,verdict='ACCEPT_SOURCEFREE_NONINSTALLING_SELECTED_WORLD_ONLY',boundary='EXACT_E05R_V2_SERVE_ONLY'),
                    implementation_commit=IMPLEMENTATION_PIN,
                    request=prepared.request.binding(),acceptance=prepared.acceptance.binding(),
                    selected_world_receipt=receipt,
                    consumer_values=deepcopy(receipt['consumers']),
                    native_accepted_custody=deepcopy(self._custody),
                    boundary=dict(hq_adopted=False,operative_OC05=False,operative_N9=False,operative_N10W=False,issued_EE14=False,real_source_rights=False,V3=False),
                    custody_interpretation='Native accepted custody is identity history; fresh permission/value state is the actual receipt native readset, not this historical custody projection')

    def execute(self,request_binding,**consumer_options):
        return self.serve(self.prepare(request_binding),**consumer_options)

    def archive(self,packet):
        archived=self.adapter.historical_receipt(packet['selected_world_receipt']['receipt_hash'])
        return dict(schema='E05A_ARCHIVAL_RECEIPT@1',archival_only=True,fresh_use_authorized=False,retained=archived)


def fixture_handoff(registry_rows,*,empirical_changed=False,support_loss=False):
    """Explicit TEST_ONLY source constructor; not a source/operation grant."""
    return SourcefreeMethodHandoff(E.N9SelectedWorldAdapter(
        service=GenericSelectedWorldService(structural_revision=True,
                    empirical_changed=empirical_changed,support_loss=support_loss),
        registry=TestOnlyRegistry(deepcopy(registry_rows))))


def render_markdown(packet):
    """Render actual served values; never supply independent result numerics."""
    r=packet['selected_world_receipt'];lines=['# Sourcefree selected-world handoff',
        '',packet['status']+' · '+r['state'],
        '',f"Selection: {r['selection']['mode']}; valid {r['selection']['valid_at']}; known by {r['selection']['published_asof']}.",
        '', '| Structural key | Actual value/state | Native unit |','|---|---|---|']
    for key,v in r['structural_values'].items():lines.append(f"| {key} | {v.get('value',v.get('state'))} | {v.get('unit','typed unavailable')} |")
    lines+=['','| Empirical query | Native cells/support | State |','|---|---|---|']
    for step in r['empirical_steps']:
        cells=', '.join(str(c['cell'])+': '+str(c['raw_numerator_support'])+'/'+str(step['denominator']) for c in step['cells']) or 'No numeric cells'
        lines.append(f"| {step['target']} given {step['conditioners']} | {cells} | {step['state']} |")
    lines+=['','| Native field | Actual values | Native unit / geography |','|---|---|---|']
    for v in r['native_field_readset']['values_read']:lines.append(f"| {v['role']} | {json.dumps(v['values'],sort_keys=True)} | {v['native_unit']} / {v['native_geography']} |")
    for v in r['native_field_readset']['refusals']:lines.append(f"| {v['role']} | {v['reason']} | Typed missing arm |")
    for c in r['consumers']:
        m=c['consumer_material'];lines+=['',m['consumer']+': '+m['state']]
        if 'structural_routes' in m:lines.append(json.dumps(m['structural_routes'],sort_keys=True))
        if 'scenarios' in m:lines.append(json.dumps([dict(scenario_id=s['scenario_id'],route=s['route'],feasibility=s['feasibility'],selection_weight=s['selection_weight']) for s in m['scenarios']],sort_keys=True))
    lines+=['','Request hash: '+r['request_hash'],'Receipt hash: '+r['receipt_hash'],
        '','No HQ adoption, operative OC05/N9/N10W, real source issuance or person/V3 output.']
    return '\n'.join(lines)+'\n'
