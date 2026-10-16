"""HQ303 OUT3 reviewer-authored hostile source-free test bank.

Not part of the original 137-case frozen bank. Failed assertions are retained
as newly observed REDs; owner claims and expected behavior are separate.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest
from outbox_prototype import (Journal, DeliveryState, _hash, make_prototype,
                              durable_delivery_id)
from test_rto_hostile import legacy, strict


def _strict():
    p = make_prototype()
    p.ledger.admission_decider = lambda *_: True
    return p


def _admitted_strict():
    p = _strict()
    e = p.ledger.admit(strict())
    assert e is not None
    return p, e['occurrence_id']


def test_h01_legacy_minimal_frozen_compatibility_positive():
    p = make_prototype()
    e = p.ledger.admit(legacy('LEGACY-ONLY'))
    assert e and e['admission_grade'] == 'SOURCEFREE_LEGACY_FIXTURE_NO_OWNER_AUTHORITY'


def test_h02_omitted_mode_with_opaque_issuer_fields_must_not_gain_event_or_emission():
    # Unlike minimal frozen compatibility, this resembles an unadjudicated live envelope.
    p = make_prototype()
    c = strict('UNTRUSTED')
    del c['envelope_mode']
    e = p.ledger.admit(c)
    assert e is None, 'No fixture marker or competent witness authorized this shaped envelope'
    assert p.outbox.deliveries == {}


@pytest.mark.parametrize('key,value', [
    ('WORLD_OWNER', 'NADIA'),
    ('worldOwner', 'NADIA'),
    ('MEMORY_DELTA', {'scene': 'rewritten'}),
    ('Client_Perceived', True),
])
def test_h03_case_variant_authority_directive_must_be_refused(key, value):
    p = _strict()
    c = strict()
    c['payload']['nested'] = {key: value}
    assert p.ledger.admit(c) is None
    assert p.ledger.count() == 0


@pytest.mark.parametrize('changes', [
    {'source_refs': ['   ']},
    {'participant_refs': ['']},
    {'participant_refs': ['   ']},
])
def test_h04_strict_blank_opaque_members_cannot_admit(changes):
    p = _strict()
    assert p.ledger.admit(strict(**changes)) is None


def test_h05_noniterable_parent_refs_fail_closed_without_exception():
    p = _strict()
    c = strict(parent_refs=None)
    # Malformed external data should be typed refusal rather than uncaught TypeError.
    assert p.ledger.admit(c) is None
    assert p.ledger.last_refusal is not None


def test_h06_forged_public_perceived_dict_cannot_be_read_as_perception():
    p, eid = _admitted_strict()
    p.projection.perception_decider = lambda *_: True
    assert p.projection.perceive('A', eid, perception_witness={'human_seen': True}) is False
    p.projection.perceived['A'] = [eid]
    assert not p.projection.has_perceived('A', eid)


def test_h07_global_ack_cannot_bypass_per_viewer_delivery_in_strict():
    p, eid = _admitted_strict()
    assert p.outbox.authorize_viewer(eid, 'A')
    assert p.outbox.emit_to(eid, 'A')
    # No viewer delivery has occurred.
    assert p.outbox.ack(eid) == DeliveryState.NOT_SENT
    assert not p.projection.has_opportunity('A', eid)


def test_h08_global_ack_cannot_progress_after_only_viewer_revoked():
    p, eid = _admitted_strict()
    assert p.outbox.authorize_viewer(eid, 'A')
    assert p.outbox.emit_to(eid, 'A')
    assert p.outbox.revoke_viewer(eid, 'A')
    assert p.outbox.deliver(eid) == DeliveryState.NOT_SENT
    assert p.outbox.ack(eid) == DeliveryState.NOT_SENT


def test_h09_restore_rejects_invalid_global_outbox_attempts_and_ack(tmp_path):
    p = make_prototype()
    eid = p.ledger.admit(legacy('L'))['occurrence_id']
    assert p.outbox.emit(eid)
    snap = p.snapshot()
    snap['outbox'][eid] = {'state': 'ACKNOWLEDGED', 'attempts': -4, 'ack_count': 23}
    q = make_prototype()
    with pytest.raises(ValueError):
        q.restore(snap)


def test_h10_restore_rejects_client_ack_state_with_zero_ack_count(tmp_path):
    p, eid = _admitted_strict()
    assert p.outbox.authorize_viewer(eid, 'A')
    assert p.outbox.emit_to(eid, 'A')
    assert p.outbox.deliver_to(eid, 'A')
    snap = p.snapshot()
    snap['client_deliveries'][durable_delivery_id(eid, 'A')]['state'] = 'ACKNOWLEDGED'
    q = make_prototype()
    with pytest.raises(ValueError):
        q.restore(snap)


def test_h11_cold_recover_rejects_invalid_global_receipt_even_if_rehashed(tmp_path):
    p = make_prototype()
    eid = p.ledger.admit(legacy('L'))['occurrence_id']
    p.outbox.emit(eid)
    j = Journal(tmp_path / 'cold.json')
    j.commit(p)
    doc = json.loads(j.path.read_text())
    doc['state']['outbox'][eid]['attempts'] = -17
    doc['state_digest'] = _hash(doc['state'])
    j.path.write_text(json.dumps(doc))
    driver = ("from outbox_prototype import Journal; "
              "import sys; Journal(sys.argv[1]).recover(); print('ACCEPTED')")
    cp = subprocess.run([sys.executable, '-c', driver, str(j.path)],
                        cwd=Path(__file__).parent, text=True, capture_output=True, timeout=10)
    assert cp.returncode != 0 and 'ACCEPTED' not in cp.stdout


def test_h12_external_writer_rehashed_grant_is_not_authenticated_negative_control(tmp_path):
    p, eid = _admitted_strict()
    j = Journal(tmp_path / 'cold.json')
    j.commit(p)
    doc = json.loads(j.path.read_text())
    doc['state']['viewers'][eid] = ['FORGED_VIEWER']
    doc['state_digest'] = _hash(doc['state'])
    j.path.write_text(json.dumps(doc))
    cold = j.recover()
    # NOT a safety PASS: expected proof of excluded no-key disk-authority boundary.
    assert 'FORGED_VIEWER' in cold.outbox.viewers[eid]


def test_h13_strict_negative_callback_refuses_without_entry():
    p = make_prototype()
    p.ledger.admission_decider = lambda *_: False
    assert p.ledger.admit(strict()) is None
    assert p.ledger.count() == 0


def test_h14_revocation_blocks_strict_opportunity_across_cold(tmp_path):
    p, eid = _admitted_strict()
    p.outbox.authorize_viewer(eid, 'A')
    p.outbox.emit_to(eid, 'A')
    p.outbox.deliver_to(eid, 'A')
    assert p.projection.offer('A', eid)
    p.outbox.revoke_viewer(eid, 'A')
    j = Journal(tmp_path / 'cold.json')
    j.commit(p)
    cold = j.recover()
    assert not cold.projection.has_opportunity('A', eid)
    assert cold.outbox.ack_to(eid, 'A') is None


def test_h15_v1_snapshot_cold_refuses_no_migration(tmp_path):
    j = Journal(tmp_path / 'cold.json')
    j.commit(make_prototype())
    d = json.loads(j.path.read_text())
    d['schema'] = 'OUTBOX_F2_JOURNAL_V1'
    j.path.write_text(json.dumps(d))
    with pytest.raises(ValueError, match='UNSUPPORTED_JOURNAL_SCHEMA'):
        j.recover()


def test_h16_direct_viewer_authorization_refuses_invalid_identity():
    p, eid = _admitted_strict()
    assert not p.outbox.authorize_viewer(eid, '')
    assert not p.outbox.authorize_viewer(eid, 25)


def test_h17_revocation_cannot_be_silently_reversed_without_issuer():
    p, eid = _admitted_strict()
    assert p.outbox.authorize_viewer(eid, 'A')
    assert p.outbox.revoke_viewer(eid, 'A')
    assert not p.outbox.authorize_viewer(eid, 'A')
