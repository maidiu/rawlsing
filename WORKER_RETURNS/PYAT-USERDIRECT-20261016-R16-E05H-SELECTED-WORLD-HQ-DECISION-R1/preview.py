"""Opt-in prospective consumer input over unchanged E05A/E05R. No installation."""
from copy import deepcopy
from handoff import fixture_handoff
import e05_n9_selected_world_adapter as E

class PreviewDisabled(RuntimeError): pass

def read_preview(handoff, binding, *, enabled=False, prepared=None):
    if enabled is not True:
        raise PreviewDisabled('OFF_BY_DEFAULT_EXPLICIT_TRUE_REQUIRED')
    prepared = handoff.prepare(binding) if prepared is None else prepared
    if prepared.request.binding() != binding:
        raise ValueError('PREVIEW_REQUEST_BINDING_MISMATCH')
    # The existing handoff invokes both original consumers and E05R authenticates
    # their actual full material. No numbers are derived by this wrapper.
    packet = handoff.serve(prepared)
    if packet['request'] != binding:
        raise ValueError('PREVIEW_REQUEST_BINDING_MISMATCH')
    receipt = packet['selected_world_receipt']
    assert packet['acceptance']['request_hash'] == receipt['request_hash']
    assert packet['acceptance']['snapshot_hash'] == receipt['snapshot_hash']
    assert len(packet['consumer_values']) == 2
    return dict(schema='E05H_PROSPECTIVE_CONSUMER_INPUT@1',
                enabled_for_this_call=True, default_enabled=False,
                consumer_acceptance='ACTUAL_TWO_ORIGINAL_CLIENTS_READ_AND_E05R_AUTHENTICATED',
                prospective_destinations=['N9/OC05', 'N10W'],
                installed=False, packet=deepcopy(packet))
