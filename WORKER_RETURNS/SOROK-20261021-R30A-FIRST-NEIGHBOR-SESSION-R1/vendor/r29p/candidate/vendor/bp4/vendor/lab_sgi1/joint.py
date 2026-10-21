"""Separately owned source-free material event and two performed adult actions.

This research observer is not an ADP010/019 issuer. No trust from a denial string,
solo co-presence, narrator, or hash prefix. Replay re-executes both actor actions.

G18 source-owner boundary
=========================
A caller-supplied dictionary with ``owner_id``, ``permission``,
``payment_per_actor`` and a recomputed ``event_id`` cannot authenticate itself.
The sourcefree trusted fixture origin below *issues* a bounded receipt over the
exact material payload (owner, scope, permission, schedule, units, clock) and,
separately, over every actually performed participation action (actor, history
hash, material receipt, before/after state). Consumers verify the MAC, the
canonical body and the bounded schedule before reading any value.

This is TEST_ONLY fixture-origin authenticity at declared sourcefree scope. It is
NOT native CAN/ADP issuance, NOT a person/actor/biology grant, and the HMAC key
is a deterministic local fixture anchor, not an external issuer secret. A caller
can never turn a forged/rehashed dict into a receipt by recomputing a public
hash: the receipt MAC is not a public checksum, and the material schedule is
bounded independently of the MAC.
"""
from copy import deepcopy
from hashlib import sha256
import hmac

from .core import h_obj, canon
from .history import replay_history, derive_psyche, validate_psyche

JOINT_OWNER = 'G15_INDEPENDENT_MATERIAL_OBSERVER'
SOURCE_RECEIPT_SCHEMA = 'SOROK_G18_SOURCE_ISSUED_MATERIAL_RECEIPT@1'
ACTION_RECEIPT_SCHEMA = 'SOROK_G18_SOURCE_PERFORMED_ACTION_RECEIPT@1'
FIXTURE_SCOPE = 'SOURCEFREE_TRUSTED_FIXTURE_ORIGIN_ONLY'
SOURCE_GRADE = 'SOURCEFREE_RESEARCH_FIXTURE_ISSUED__NOT_NATIVE'
NATIVE_GRANT = 'NOT_GRANTED'
ORIGIN_KEY_ID = 'G18_SOURCEFREE_FIXTURE_ORIGIN_HMAC_KEY_1'
MATERIAL_PAYMENT_PER_ACTOR = 2
MATERIAL_TASK_HOURS = 1
MATERIAL_MAX_UNITS = 8
MATERIAL_MAX_PAYMENT = 8
MATERIAL_MAX_TASK_HOURS = 4

JOINT_REGISTRY = dict(
    owner_id=JOINT_OWNER,
    scope='SOURCEFREE_RESEARCH_ONLY',
    native_grant=NATIVE_GRANT,
    rule='TWO_PROJECT_TASK_EXCHANGE_R1',
    source_receipt_schema=SOURCE_RECEIPT_SCHEMA,
    action_receipt_schema=ACTION_RECEIPT_SCHEMA,
    source_grade=SOURCE_GRADE,
    fixture_scope=FIXTURE_SCOPE,
    issuer='TEST_ONLY_FIXTURE_ORIGIN_NOT_NATIVE_ADP_OR_CAN',
)

# Deterministic test-only fixture trust anchor. Explicitly NOT native authority
# and NOT a claimed external issuer secret.
_FIXTURE_ORIGIN_KEY = sha256(
    b'RAWLSING\x00SOROK-G18\x00SOURCEFREE-TRUSTED-FIXTURE-ORIGIN\x00'
    b'TEST-ONLY-NOT-NATIVE-AUTHORITY'
).digest()

_MATERIAL_PAYLOAD_FIELDS = (
    'owner_id', 'permission', 'effective_index', 'place',
    'material_units', 'payment_per_actor', 'task_hours', 'permit',
)
_MATERIAL_PACKET_FIELDS = frozenset(_MATERIAL_PAYLOAD_FIELDS) | {
    'event_id', 'source_receipt'}
_RECEIPT_FIELDS = frozenset({
    'schema', 'source_owner', 'scope', 'source_grade', 'native_grant',
    'body_hash', 'origin_key_id', 'mac'})
_ACTION_BODY_FIELDS = frozenset({
    'owner_id', 'kind', 'status', 'effective_index', 'history_hash',
    'material_event_ref', 'causal_parent_event_ids', 'before', 'after',
    'values_read'})
_ACTION_PACKET_FIELDS = _ACTION_BODY_FIELDS | {'event_id', 'source_receipt'}
_ACTION_RECEIPT_FIELDS = frozenset({
    'schema', 'source_owner', 'scope', 'source_grade', 'native_grant',
    'material_receipt_id', 'material_event_ref', 'actor', 'history_hash',
    'action_status', 'body_hash', 'origin_key_id', 'mac'})
_MATERIAL_MAC_DOMAIN = 'SOROK_G18_MATERIAL_SOURCE_RECEIPT'
_ACTION_MAC_DOMAIN = 'SOROK_G18_PERFORMED_ACTION_RECEIPT'


class MaterialSourceRefusal(ValueError):
    """A material packet is not an exact source-issued fixture event."""


def _mac(domain, body, receipt_fields):
    message = (
        domain.encode('utf-8') + b'\x1f' + canon(body) + b'\x1f'
        + canon(receipt_fields))
    return 'hmac-sha256:' + hmac.new(
        _FIXTURE_ORIGIN_KEY, message, sha256).hexdigest()


def _receipt_without_mac(receipt):
    return {k: v for k, v in receipt.items() if k != 'mac'}


def _material_payload(material):
    return {k: material[k] for k in _MATERIAL_PAYLOAD_FIELDS}


def _material_receipt(payload):
    receipt = dict(
        schema=SOURCE_RECEIPT_SCHEMA,
        source_owner=JOINT_OWNER,
        scope=FIXTURE_SCOPE,
        source_grade=SOURCE_GRADE,
        native_grant=NATIVE_GRANT,
        body_hash=h_obj(payload),
        origin_key_id=ORIGIN_KEY_ID,
    )
    receipt['mac'] = _mac(_MATERIAL_MAC_DOMAIN, payload, receipt)
    return receipt


def material_joint_opportunity(effective_index=100, permit=True, units=1,
                               payment_per_actor=MATERIAL_PAYMENT_PER_ACTOR,
                               task_hours=MATERIAL_TASK_HOURS):
    """Issue one bounded sourcefree material event with a fixture-origin receipt.

    The owner declares a bounded task-cost schedule. A caller may select a
    schedule point inside that declared range; it cannot mint 100000 cash or an
    arbitrary afterstate through this API. The selected point is covered by the
    receipt.
    """
    if type(effective_index) is not int or effective_index < 0:
        raise ValueError('INVALID_MATERIAL_EFFECTIVE_INDEX')
    if type(permit) is not bool:
        raise ValueError('INVALID_MATERIAL_PERMIT_TYPE')
    if type(units) is not int or not (1 <= units <= MATERIAL_MAX_UNITS):
        raise ValueError('MATERIAL_UNITS_OUTSIDE_SOURCE_SCHEDULE')
    if type(payment_per_actor) is not int or not (
            1 <= payment_per_actor <= MATERIAL_MAX_PAYMENT):
        raise ValueError('MATERIAL_PAYMENT_OUTSIDE_SOURCE_SCHEDULE')
    if type(task_hours) is not int or not (
            1 <= task_hours <= MATERIAL_MAX_TASK_HOURS):
        raise ValueError('MATERIAL_TASK_HOURS_OUTSIDE_SOURCE_SCHEDULE')
    payload = dict(
        owner_id=JOINT_OWNER,
        permission='RESEARCH_JOINT_WITNESS_ONLY',
        effective_index=effective_index,
        place='INST_WORKSHOP_A',
        material_units=units,
        payment_per_actor=payment_per_actor,
        task_hours=task_hours,
        permit=permit,
    )
    receipt = _material_receipt(payload)
    material = dict(payload)
    material['source_receipt'] = receipt
    material['event_id'] = h_obj(material)
    return material


def _material_problem(material):
    """Return the exact source-refusal reason, or None for an authentic packet."""
    if not isinstance(material, dict):
        return 'MATERIAL_PACKET_NOT_OBJECT'
    if set(material) != _MATERIAL_PACKET_FIELDS:
        return 'MATERIAL_PACKET_SHAPE_NOT_SOURCE_SCHEMA'
    receipt = material.get('source_receipt')
    if not isinstance(receipt, dict) or set(receipt) != _RECEIPT_FIELDS:
        return 'SOURCE_RECEIPT_SHAPE_NOT_ISSUED'
    if receipt.get('schema') != SOURCE_RECEIPT_SCHEMA:
        return 'SOURCE_RECEIPT_SCHEMA_UNKNOWN'
    if receipt.get('source_owner') != JOINT_OWNER:
        return 'SOURCE_OWNER_NOT_FIXTURE_ORIGIN'
    if receipt.get('scope') != FIXTURE_SCOPE:
        return 'SOURCE_SCOPE_NOT_FIXTURE_ONLY'
    if receipt.get('source_grade') != SOURCE_GRADE:
        return 'SOURCE_GRADE_NOT_DECLARED'
    if receipt.get('native_grant') != NATIVE_GRANT:
        return 'SOURCE_RECEIPT_CANNOT_CARRY_NATIVE_GRANT'
    if receipt.get('origin_key_id') != ORIGIN_KEY_ID:
        return 'SOURCE_ORIGIN_KEY_UNKNOWN'
    payload = _material_payload(material)
    if receipt.get('body_hash') != h_obj(payload):
        return 'MATERIAL_BODY_HASH_MISMATCH'
    expected_mac = _mac(_MATERIAL_MAC_DOMAIN, payload,
                        _receipt_without_mac(receipt))
    if not hmac.compare_digest(str(receipt.get('mac')), expected_mac):
        return 'SOURCE_RECEIPT_MAC_INVALID'
    if material.get('event_id') != h_obj(
            {k: v for k, v in material.items() if k != 'event_id'}):
        return 'MATERIAL_EVENT_ID_NOT_SOURCE_BOUND'
    if payload['owner_id'] != JOINT_OWNER:
        return 'MATERIAL_OWNER_NOT_FIXTURE_ORIGIN'
    if payload['permission'] != 'RESEARCH_JOINT_WITNESS_ONLY':
        return 'MATERIAL_PERMISSION_NOT_ISSUED'
    if type(payload['effective_index']) is not int or payload['effective_index'] < 0:
        return 'MATERIAL_EFFECTIVE_INDEX_NOT_ISSUED'
    if payload['place'] != 'INST_WORKSHOP_A':
        return 'MATERIAL_PLACE_NOT_ISSUED'
    if type(payload['material_units']) is not int or not (
            1 <= payload['material_units'] <= MATERIAL_MAX_UNITS):
        return 'MATERIAL_UNITS_OUTSIDE_SOURCE_SCHEDULE'
    if type(payload['payment_per_actor']) is not int or not (
            1 <= payload['payment_per_actor'] <= MATERIAL_MAX_PAYMENT):
        return 'MATERIAL_PAYMENT_OUTSIDE_SOURCE_SCHEDULE'
    if type(payload['task_hours']) is not int or not (
            1 <= payload['task_hours'] <= MATERIAL_MAX_TASK_HOURS):
        return 'MATERIAL_TASK_HOURS_OUTSIDE_SOURCE_SCHEDULE'
    if type(payload['permit']) is not bool:
        return 'MATERIAL_PERMIT_NOT_TYPED'
    return None


def verify_material_source(material):
    """Return ``(accepted, reason, canonical_payload)`` for a material packet."""
    problem = _material_problem(material)
    if problem is not None:
        return False, problem, None
    return True, None, _material_payload(material)


def require_material_source(material):
    accepted, reason, payload = verify_material_source(material)
    if not accepted:
        raise MaterialSourceRefusal(reason)
    return payload


def material_payload(material):
    return require_material_source(material)


def _action_body(action):
    return {k: deepcopy(action[k]) for k in _ACTION_BODY_FIELDS}


def _action_receipt(action_body, material):
    receipt = dict(
        schema=ACTION_RECEIPT_SCHEMA,
        source_owner=JOINT_OWNER,
        scope=FIXTURE_SCOPE,
        source_grade=SOURCE_GRADE,
        native_grant=NATIVE_GRANT,
        material_receipt_id=h_obj(material['source_receipt']),
        material_event_ref=material['event_id'],
        actor=action_body['owner_id'],
        history_hash=action_body['history_hash'],
        action_status=action_body['status'],
        body_hash=h_obj(action_body),
        origin_key_id=ORIGIN_KEY_ID,
    )
    receipt['mac'] = _mac(_ACTION_MAC_DOMAIN, action_body, receipt)
    return receipt


def _action_problem(action, material=None):
    if not isinstance(action, dict):
        return 'ACTION_NOT_OBJECT'
    if set(action) != _ACTION_PACKET_FIELDS:
        return 'ACTION_SHAPE_NOT_SOURCE_SCHEMA'
    if action.get('kind') != 'PARTICIPATION_ACTION':
        return 'ACTION_KIND_NOT_PARTICIPATION'
    if action.get('status') != 'PERFORMED':
        return 'ACTION_NOT_PERFORMED'
    receipt = action.get('source_receipt')
    if not isinstance(receipt, dict) or set(receipt) != _ACTION_RECEIPT_FIELDS:
        return 'ACTION_RECEIPT_SHAPE_NOT_ISSUED'
    if receipt.get('schema') != ACTION_RECEIPT_SCHEMA:
        return 'ACTION_RECEIPT_SCHEMA_UNKNOWN'
    if receipt.get('source_owner') != JOINT_OWNER:
        return 'ACTION_SOURCE_OWNER_NOT_FIXTURE_ORIGIN'
    if receipt.get('scope') != FIXTURE_SCOPE:
        return 'ACTION_SCOPE_NOT_FIXTURE_ONLY'
    if receipt.get('source_grade') != SOURCE_GRADE:
        return 'ACTION_GRADE_NOT_DECLARED'
    if receipt.get('native_grant') != NATIVE_GRANT:
        return 'ACTION_RECEIPT_CANNOT_CARRY_NATIVE_GRANT'
    if receipt.get('origin_key_id') != ORIGIN_KEY_ID:
        return 'ACTION_ORIGIN_KEY_UNKNOWN'
    body = _action_body(action)
    if receipt.get('body_hash') != h_obj(body):
        return 'ACTION_BODY_HASH_MISMATCH'
    expected_mac = _mac(_ACTION_MAC_DOMAIN, body,
                        _receipt_without_mac(receipt))
    if not hmac.compare_digest(str(receipt.get('mac')), expected_mac):
        return 'ACTION_RECEIPT_MAC_INVALID'
    if action.get('event_id') != h_obj(
            {k: v for k, v in action.items() if k != 'event_id'}):
        return 'ACTION_EVENT_ID_NOT_SOURCE_BOUND'
    if receipt.get('actor') != action.get('owner_id'):
        return 'ACTION_OWNER_RECEIPT_MISMATCH'
    if receipt.get('material_event_ref') != action.get('material_event_ref'):
        return 'ACTION_MATERIAL_REF_RECEIPT_MISMATCH'
    if receipt.get('history_hash') != action.get('history_hash'):
        return 'ACTION_HISTORY_RECEIPT_MISMATCH'
    if receipt.get('action_status') != action.get('status'):
        return 'ACTION_STATUS_RECEIPT_MISMATCH'
    before = action.get('before')
    after = action.get('after')
    if not isinstance(before, dict) or not isinstance(after, dict):
        return 'ACTION_STATE_NOT_OBJECT'
    for key in ('cash', 'free_hours', 'completed_units'):
        if type(before.get(key)) is not int or type(after.get(key)) is not int:
            return 'ACTION_STATE_FIELD_NOT_INTEGER:' + key
    if after.get('cash', 0) < 0 or after.get('free_hours', 0) < 0 or after.get(
            'completed_units', 0) < 0:
        return 'ACTION_AFTER_STATE_NEGATIVE'
    if material is not None:
        accepted, reason, payload = verify_material_source(material)
        if not accepted:
            return reason
        if receipt.get('material_receipt_id') != h_obj(material['source_receipt']):
            return 'ACTION_MATERIAL_RECEIPT_NOT_BOUND'
        if action.get('material_event_ref') != material['event_id']:
            return 'ACTION_MATERIAL_EVENT_REF_MISMATCH'
        expected = deepcopy(before)
        expected['cash'] += payload['payment_per_actor']
        expected['free_hours'] -= payload['task_hours']
        expected['completed_units'] += payload['material_units']
        if after != expected:
            return 'ACTION_AFTER_STATE_NOT_MATERIAL_CONSERVING'
    return None


def verify_performed_action(action, material=None):
    """Return ``(accepted, reason)`` for a source-issued performed action."""
    problem = _action_problem(action, material)
    if problem is not None:
        return False, problem
    return True, None


def perform_participation(events, material):
    r = replay_history(events)
    s = r['state']
    actor = s['actor_id']
    material_ok, material_reason, payload = verify_material_source(material)
    lawful = (
        material_ok and r['valid']
        and not validate_psyche(events, derive_psyche(events), r)
        and payload['owner_id'] == JOINT_OWNER
        and payload['permission'] == 'RESEARCH_JOINT_WITNESS_ONLY'
        and type(payload.get('effective_index')) is int
        and payload['effective_index'] > max(
            (e['effective_index'] for e in events), default=-1)
        and payload.get('place') == s['place']
        and payload.get('permit') is True
        and type(payload.get('task_hours')) is int
        and 0 < payload['task_hours'] <= s['free_hours']
        and type(payload.get('material_units')) is int
        and payload['material_units'] > 0
        and type(payload.get('payment_per_actor')) is int
        and 1 <= payload['payment_per_actor'] <= MATERIAL_MAX_PAYMENT
    )
    source = [
        w for w in r['value_witnesses']
        if w['kind'] in {'PROJECT', 'STRIVING', 'PRACTICE_FORMATION',
                         'COMMISSIONED_WORK'}
    ]
    lawful = lawful and {w['kind'] for w in source} >= {
        'PROJECT', 'STRIVING', 'PRACTICE_FORMATION', 'COMMISSIONED_WORK'}
    after = deepcopy(s)
    if lawful:
        after['cash'] += payload['payment_per_actor']
        after['free_hours'] -= payload['task_hours']
        after['completed_units'] += payload['material_units']
    body = dict(
        owner_id=actor,
        kind='PARTICIPATION_ACTION',
        status='PERFORMED' if lawful else 'REFUSED',
        effective_index=(payload.get('effective_index', -2) + 1
                         if material_ok else -1),
        history_hash=r['history_hash'],
        material_event_ref=material.get('event_id') if isinstance(material, dict) else None,
        causal_parent_event_ids=[w['event_id'] for w in source]
        + [material.get('event_id') if isinstance(material, dict) else None],
        before=s,
        after=after,
        values_read=source,
    )
    if lawful:
        body['source_receipt'] = _action_receipt(body, material)
    action = dict(event_id=h_obj(body), **body)
    return action


def observe_joint_actions(anchor, dad_events, material):
    maternal = anchor.get('history_events', [])
    a = perform_participation(maternal, material)
    b = perform_participation(dad_events, material)
    material_ok, _, _ = verify_material_source(material)
    valid = (
        material_ok
        and a['status'] == b['status'] == 'PERFORMED'
        and a['owner_id'] != b['owner_id']
        and a['owner_id'] == anchor.get('actor_id')
        and a['after']['completed_units'] > a['before']['completed_units']
        and b['after']['completed_units'] > b['before']['completed_units']
        and material.get('event_id') == h_obj(
            {k: v for k, v in material.items() if k != 'event_id'})
    )
    body = dict(
        owner_id=JOINT_OWNER,
        registry_hash=h_obj(JOINT_REGISTRY),
        kind='JOINT_TASK_WITNESS',
        status='WITNESSED' if valid else 'REFUSED',
        effective_index=material.get('effective_index', -3) + 2
        if material_ok else -1,
        causal_parent_event_ids=[
            material.get('event_id'),
            a['event_id'],
            b['event_id']],
        material=deepcopy(material),
        actions=[a, b],
        participants=[a['owner_id'], b['owner_id']],
        maternal_history_hash=h_obj(maternal),
        paternal_history_hash=h_obj(dad_events),
        source_receipt_schema=SOURCE_RECEIPT_SCHEMA,
        action_receipt_schema=ACTION_RECEIPT_SCHEMA,
        source_grade=SOURCE_GRADE,
        native_grant=NATIVE_GRANT,
    )
    return dict(event_id=h_obj(body), **body)


def validate_joint(anchor, dad_events, evidence):
    if not isinstance(evidence, dict) or evidence.get('owner_id') != JOINT_OWNER:
        return False
    expected = observe_joint_actions(anchor, dad_events, evidence.get('material', {}))
    return evidence == expected and expected['status'] == 'WITNESSED'


def observe_continued_contact(relation, continuations, material):
    """A second task contact, witnessed only after both independent continuations.
    No relationship persistence is presumed from the first contact alone.
    """
    material_ok, material_reason, payload = verify_material_source(material)
    obj = relation.get('objective_relation', {})
    participants = obj.get('participants', [])
    valid = (
        material_ok
        and relation.get('relationship_committed') is True
        and len(participants) == 2
        and len(continuations) == 2
        and {e['actor'] for e in continuations} == set(participants)
        and type(payload.get('effective_index')) is int
        and payload['effective_index'] > max(
            [e['effective_index'] for e in continuations]
            + [obj.get('witness', {}).get('effective_index', -1)])
        and material.get('event_id') not in obj.get('shared_event_refs', [])
        and payload.get('permit') is True
    )
    actions = []
    for e in continuations:
        before = e['payload']['after']
        after = deepcopy(before)
        allowed = (
            valid and before['place'] == payload.get('place')
            and type(payload.get('task_hours')) is int
            and 0 < payload['task_hours'] <= before['free_hours']
            and type(payload.get('material_units')) is int
            and payload['material_units'] > 0
            and type(payload.get('payment_per_actor')) is int
            and 1 <= payload['payment_per_actor'] <= MATERIAL_MAX_PAYMENT
        )
        if allowed:
            after['cash'] += payload['payment_per_actor']
            after['free_hours'] -= payload['task_hours']
            after['completed_units'] += payload['material_units']
        a = dict(
            owner_id=e['actor'],
            effective_index=payload.get('effective_index', -2) + 1,
            kind='CONTINUED_CONTACT_ACTION',
            status='PERFORMED' if allowed else 'REFUSED',
            causal_parent_event_ids=[e['event_id'], material.get('event_id')],
            before=before,
            after=after,
        )
        actions.append(dict(event_id=h_obj(a), **a))
    body = dict(
        kind='WITNESSED_RELATION_CONTINUATION',
        owner_id=JOINT_OWNER,
        effective_index=payload.get('effective_index', -3) + 2
        if material_ok else -1,
        causal_parent_event_ids=obj.get('shared_event_refs', [])
        + [a['event_id'] for a in actions] + [material.get('event_id')],
        status='WITNESSED' if valid and len(actions) == 2 and all(
            a['status'] == 'PERFORMED' for a in actions) else 'NO_CHANGE',
        previous_relation_ref=obj.get('relation_id'),
        previous_witness_refs=obj.get('shared_event_refs', []),
        material_source=deepcopy(material),
        actions=actions,
        household_admission='NOT_GRANTED',
        parenthood_admission='NOT_GRANTED',
        source_receipt_schema=SOURCE_RECEIPT_SCHEMA,
        source_grade=SOURCE_GRADE,
        native_grant=NATIVE_GRANT,
    )
    return dict(event_id=h_obj(body), **body)


def joint_event_closure(relation, continuation):
    closure = []
    witness = relation.get('objective_relation', {}).get('witness')
    if witness and witness.get('status') == 'WITNESSED':
        material = witness['material']
        closure.extend([dict(material, causal_parent_event_ids=[]),
                        *witness['actions'], witness])
    later = continuation.get('research_relation_continuation')
    if later and later.get('status') == 'WITNESSED':
        closure.extend([dict(later['material_source'],
                             causal_parent_event_ids=[]),
                        *later['actions'], later])
    return closure
