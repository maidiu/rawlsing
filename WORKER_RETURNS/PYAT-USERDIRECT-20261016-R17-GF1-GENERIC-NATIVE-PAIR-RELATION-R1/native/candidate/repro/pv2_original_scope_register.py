"""R10 PV2 — original-scope identity and prospectively frozen E_pre binding.

Bounded sourcefree repair of the five defects the independent post-Astra PV
court proved against the adopted V2K original-identity successor:

  (a) coherent foreign U/E/custody/operation-scope refs accepted,
  (b) dropping ALL HELD original E members accepted,
  (c) cherry-picking an A-only E silently accepted,
  (d) reversed semantic-role mask accepted against an unchanged X→Y producer,
  (e) foreign native form / respondent-unit labels accepted.

The repair anchors the *complete* original test-only opportunity scope
(including HELD obligations) to an independently authored, prospectively
committed register BEFORE any accepted-owner execution.  The register carries
the trusted original metadata, the authorized test-only issuer refs and the
independently spelled source-native inventory, so a candidate caller can no
longer relabel, rekey, suppress or cherry-pick by supplying its own E.

This module never reimplements the accepted owners' arithmetic: it routes
through the adopted V2K successor (and therefore real C11 ingest, real I03
query, real I05 discovery and the real P01 Field Forge consumer).  Genuine
prospective original source U/E issuers remain HELD throughout.
"""
from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass, field
import json

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next import pre553_original_identity_v2k_successor_candidate as K

SCHEMA = 'R10_PV2_ORIGINAL_SCOPE_REGISTER@1.0.0'
ORIGIN = 'INDEPENDENT_SOURCEFREE_BEFORE_EXECUTION'

CONDITIONER_ROLE = 'CONDITIONER'
TARGET_ROLE = 'TARGET'
BASE_ROLE = 'BASE'

TEST_ONLY_SOURCE_KIND = 'TEST_ONLY_SYNTHETIC_NOT_OBSERVED'
TEST_ONLY_ISSUER = 'R10-PV2-TEST-ONLY-FIXTURE-ISSUER'
TEST_ONLY_GRANT = 'TEST_ONLY_FIXTURE_GRANT'
WITHDRAWN_GRANT = 'WITHDRAWN'


class OriginalScopeIdentityError(ValueError):
    """Typed original-scope identity, binding or expected-set failure."""


def _short_name(ref: ExactRef) -> str:
    """Short native item name from an owner QUESTION_NATIVE object_id."""
    return str(ref.object_id).split(':')[-1].split('-')[-1]


def _exact(value) -> ExactRef:
    return value if isinstance(value, ExactRef) else ExactRef(**value)


def _canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


# ---------------------------------------------------------------------------
# Independently spelled sourcefree register material
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SourceNativeCell:
    """One independently spelled source-native response cell (test-only)."""

    respondent_namespace: str
    respondent_key: str
    item_short_name: str
    raw_value: str
    response_state: str = 'SUBSTANTIVE_RESPONSE'

    @property
    def identity(self) -> dict:
        return dict(respondent_namespace=self.respondent_namespace,
                    respondent_key=self.respondent_key, item=self.item_short_name,
                    raw_value=self.raw_value, response_state=self.response_state)


@dataclass(frozen=True)
class RegisterObligation:
    """One independently authored original-scope opportunity, runnable or HELD."""

    respondent_namespace: str
    slot: str
    form: str
    respondent_unit: str
    language: str
    instrument_release: str
    administered_occurrence: str
    semantic_op_class: str
    semantic_roles: tuple
    condition_order: tuple
    target: str
    item: str
    state: str
    hold_reason: str | None
    source_native_items: tuple
    option_scope: tuple
    respondent_keys: tuple
    original_U_ref: ExactRef
    independent_E_ref: ExactRef
    independent_custody_ref: ExactRef
    original_operation_scope_ref: ExactRef

    def __post_init__(self) -> None:
        for name in ('respondent_namespace', 'slot', 'form', 'respondent_unit', 'language',
                     'instrument_release', 'administered_occurrence', 'semantic_op_class',
                     'target', 'item', 'state'):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                raise OriginalScopeIdentityError('PV2_OBLIGATION_FIELD_REQUIRED:' + name)
        if self.state == 'RUNNABLE' and self.hold_reason is not None:
            raise OriginalScopeIdentityError('PV2_RUNNABLE_CANNOT_CARRY_HOLD')
        if self.state != 'RUNNABLE' and not self.hold_reason:
            raise OriginalScopeIdentityError('PV2_HELD_OBLIGATION_REQUIRES_REASON:' + self.slot)
        for name in ('semantic_roles', 'source_native_items', 'option_scope', 'respondent_keys'):
            values = getattr(self, name)
            if not isinstance(values, tuple) or not values:
                raise OriginalScopeIdentityError('PV2_OBLIGATION_TUPLE_REQUIRED:' + name)
        if not isinstance(self.condition_order, tuple):
            raise OriginalScopeIdentityError('PV2_OBLIGATION_TUPLE_REQUIRED:condition_order')
        for name in ('original_U_ref', 'independent_E_ref', 'independent_custody_ref',
                     'original_operation_scope_ref'):
            if not isinstance(getattr(self, name), ExactRef):
                raise OriginalScopeIdentityError('PV2_OBLIGATION_EXACT_REF_REQUIRED:' + name)
        if len({self.original_U_ref, self.independent_E_ref,
                self.independent_custody_ref}) != 3:
            raise OriginalScopeIdentityError('PV2_U_E_CUSTODY_REFS_MUST_BE_DISTINCT')

    @property
    def obligation_key(self) -> tuple:
        """Independent identity anchor: the original scope slot in its namespace."""
        return (self.respondent_namespace, self.slot)

    @property
    def source_inventory_root(self) -> str:
        """Independently spelled source-native inventory root."""
        cells = sorted(tuple(c.identity.items()) for c in self.source_native_cells)
        return semantic_hash(json.loads(_canonical([[list(c) for c in cell] for cell in cells])))

    def binding(self) -> dict:
        return dict(
            respondent_namespace=self.respondent_namespace, slot=self.slot, form=self.form,
            respondent_unit=self.respondent_unit, language=self.language,
            instrument_release=self.instrument_release,
            administered_occurrence=self.administered_occurrence,
            semantic_op_class=self.semantic_op_class,
            semantic_roles=list(self.semantic_roles),
            condition_order=list(self.condition_order), target=self.target, item=self.item,
            state=self.state, hold_reason=self.hold_reason,
            source_native_items=list(self.source_native_items),
            option_scope=list(self.option_scope),
            respondent_keys=list(self.respondent_keys),
            issuer_refs=dict(
                original_U_ref=self.original_U_ref.as_dict(),
                independent_E_ref=self.independent_E_ref.as_dict(),
                independent_custody_ref=self.independent_custody_ref.as_dict(),
                original_operation_scope_ref=self.original_operation_scope_ref.as_dict()),
        )


@dataclass(frozen=True)
class FixtureUseGrant:
    """TEST_ONLY fixture-owner custody, never a genuine prospective issuance."""

    grant: str = TEST_ONLY_GRANT
    issuer: str = TEST_ONLY_ISSUER
    ceiling: tuple = ('SOURCE_FREE_DEV',)
    scope: str = 'sourcefree synthetic native rows only; no survey microdata'
    revoked: bool = False
    revocation_reason: str | None = None

    def binding(self) -> dict:
        return dict(grant=self.grant, issuer=self.issuer, ceiling=list(self.ceiling),
                    scope=self.scope, revoked=self.revoked,
                    revocation_reason=self.revocation_reason)


@dataclass(frozen=True)
class PrecommittedOriginalRegister:
    """The complete original test-only opportunity scope, prospectively frozen."""

    obligations: tuple
    source_artifact_identity: str
    source_native_inventory: tuple = ()
    source_kind: str = TEST_ONLY_SOURCE_KIND
    expected_consumer: str = 'FIELD_FORGE_CONDITIONAL_SUPPORT'
    fixture_use_grant: FixtureUseGrant = field(default_factory=FixtureUseGrant)
    schema: str = SCHEMA
    origin: str = ORIGIN

    def __post_init__(self) -> None:
        if not self.obligations or not all(
                isinstance(o, RegisterObligation) for o in self.obligations):
            raise OriginalScopeIdentityError('PV2_REGISTER_OBLIGATIONS_REQUIRED')
        keys = [o.obligation_key for o in self.obligations]
        if len(set(keys)) != len(keys):
            raise OriginalScopeIdentityError('PV2_REGISTER_DUPLICATE_OBLIGATION_KEY')
        if not any(o.state == 'RUNNABLE' for o in self.obligations):
            raise OriginalScopeIdentityError('PV2_REGISTER_NO_RUNNABLE_ORIGINAL_WORK')
        held = [o for o in self.obligations if o.state != 'RUNNABLE']
        if len(held) < 2:
            raise OriginalScopeIdentityError(
                'PV2_REGISTER_REQUIRES_AT_LEAST_TWO_HELD_OBLIGATIONS')
        if not self.source_native_inventory or not all(
                isinstance(c, SourceNativeCell) for c in self.source_native_inventory):
            raise OriginalScopeIdentityError('PV2_REGISTER_SOURCE_INVENTORY_REQUIRED')

    @property
    def obligation_multiset(self) -> Counter:
        return Counter(o.obligation_key for o in self.obligations)

    @property
    def runnable_multiset(self) -> Counter:
        return Counter(o.obligation_key for o in self.obligations if o.state == 'RUNNABLE')

    @property
    def held_multiset(self) -> Counter:
        return Counter(o.obligation_key for o in self.obligations if o.state != 'RUNNABLE')

    def obligation_for(self, respondent_namespace: str, slot: str) -> RegisterObligation:
        for o in self.obligations:
            if o.obligation_key == (respondent_namespace, slot):
                return o
        raise OriginalScopeIdentityError(
            'PV2_UNREGISTERED_ORIGINAL_SCOPE:' + _canonical([respondent_namespace, slot]))

    @property
    def source_inventory_root(self) -> str:
        rows = [_canonical(c.identity) for c in self.source_native_inventory]
        return semantic_hash(json.loads(json.dumps(sorted(rows), sort_keys=True)))

    def binding(self) -> dict:
        return dict(schema=SCHEMA, origin=ORIGIN,
                    source_kind=self.source_kind,
                    source_artifact_identity=self.source_artifact_identity,
                    expected_consumer=self.expected_consumer,
                    fixture_use_grant=self.fixture_use_grant.binding(),
                    obligation_multiset=sorted(
                        [list(k), n] for k, n in sorted(self.obligation_multiset.items())),
                    held_multiset=sorted(
                        [list(k), n] for k, n in sorted(self.held_multiset.items())),
                    source_inventory_root=self.source_inventory_root,
                    obligations=[o.binding() for o in sorted(
                        self.obligations, key=lambda o: o.obligation_key)])

    @property
    def committed_root(self) -> str:
        """Prospectively committed independent expected source-inventory root."""
        return semantic_hash(json.loads(json.dumps(self.binding(), sort_keys=True)))


# ---------------------------------------------------------------------------
# Semantically independent register authorship (never fixture-derived)
# ---------------------------------------------------------------------------

def _test_only_ref(kind: str, label: str) -> ExactRef:
    return ExactRef(kind, f'urn:r10:pv2:{kind.lower()}:{label}',
                    semantic_hash(json.loads(json.dumps(
                        dict(kind=kind, label=label)))))


def _register_obligation(*, namespace, slot, roles, order, state, hold_reason,
                          item, target, source_artifact_identity,
                          native_items=None) -> RegisterObligation:
    """Independently author one original-scope obligation.

    Cells are spelled literally from the synthetic sourcefree rows; they are
    never reconstructed from an owner result or from the candidate fixture.
    """
    return RegisterObligation(
        respondent_namespace=namespace, slot=slot,
        form='F1',
        respondent_unit='TEST_ONLY_ADULT',
        language='PV2-LANGUAGE',
        instrument_release=f'INST-{namespace}/F1',
        administered_occurrence='PV2-FIRST-ADMINISTRATION',
        semantic_op_class='NONSCALAR_TOPOLOGY_PRESERVATION' if slot == 'ORDERED'
                          else ('BOUNDED_DISCOVERY' if slot == 'DISCOVERY'
                                else 'PAIR_RESPONSE_COTRAVEL'),
        semantic_roles=tuple(roles), condition_order=tuple(order),
        target=target, item=item, state=state, hold_reason=hold_reason,
        source_native_items=tuple(native_items) if native_items else (
            tuple(order) if order else (item,)),
        option_scope=('AB', 'BA') if item == 'O' else ('0', '1'),
        respondent_keys=('R1', 'R2', 'R3'),
        original_U_ref=_test_only_ref('R10_PV2_ORIGINAL_U', f'{namespace}-{slot}'),
        independent_E_ref=_test_only_ref('R10_PV2_PROSPECTIVE_E', f'{namespace}-{slot}'),
        independent_custody_ref=_test_only_ref('R10_PV2_CUSTODY_WITNESS', f'{namespace}-{slot}'),
        original_operation_scope_ref=_test_only_ref(
            'R10_PV2_OPERATION_SCOPE', f'{namespace}-{slot}'))


def _register_native_inventory(*, namespace: str) -> tuple:
    """Independently spelled full source-native inventory, all native items.

    Spelled literally from the synthetic sourcefree rows; never reconstructed
    from an owner result or from the candidate fixture.
    """
    native = {
        'X': (('R1', '1'), ('R2', '0'), ('R3', '1')),
        'Y': (('R1', '1'), ('R2', '0'), ('R3', '1')),
        'O': (('R1', 'AB'), ('R2', 'BA'), ('R3', 'AB')),
        'R': (('R1', 'XY'), ('R2', 'XZ'), ('R3', 'XY')),
    }
    occurrences = {'X': 1, 'Y': 1, 'O': 2, 'R': 2}
    return tuple(
        SourceNativeCell(respondent_namespace=namespace, respondent_key=respondent,
                         item_short_name=item, raw_value=value)
        for item in sorted(native) for respondent, value in native[item]
        for _ in range(occurrences[item]))


def author_sourcefree_original_scope_register() -> PrecommittedOriginalRegister:
    """Author the complete original test-only scope, independently and in full.

    Two synthetic namespaces x four slots.  Six opportunities are RUNNABLE,
    two ORDERED-lineage obligations are HELD because the ordered-topology
    semantic owner is not issued.  Nothing here is derived from any owner
    result, so a candidate caller cannot relabel or suppress it.
    """
    obligations = []
    for namespace in ('PV2-ADULT-A', 'PV2-ADULT-B'):
        obligations.append(_register_obligation(
            namespace=namespace, slot='PAIR', roles=(CONDITIONER_ROLE, TARGET_ROLE),
            order=('X', 'Y'), state='RUNNABLE', hold_reason=None,
            item='X', target='XY',
            source_artifact_identity=''))
        obligations.append(_register_obligation(
            namespace=namespace, slot='B', roles=(CONDITIONER_ROLE, TARGET_ROLE),
            order=('Y', 'X'), state='RUNNABLE', hold_reason=None,
            item='Y', target='YX',
            source_artifact_identity=''))
        obligations.append(_register_obligation(
            namespace=namespace, slot='DISCOVERY', roles=(BASE_ROLE,), order=(),
            state='RUNNABLE', hold_reason=None, item='X', target='XY',
            native_items=('X', 'Y'), source_artifact_identity=''))
        obligations.append(_register_obligation(
            namespace=namespace, slot='ORDERED', roles=(BASE_ROLE,), order=(),
            state='HELD', hold_reason='ORDERED_OWNER_NOT_ISSUED', item='O', target='O',
            native_items=('O',), source_artifact_identity=''))
    inventory = tuple(
        cell for namespace in ('PV2-ADULT-A', 'PV2-ADULT-B')
        for cell in _register_native_inventory(namespace=namespace))
    return PrecommittedOriginalRegister(
        obligations=tuple(obligations),
        source_artifact_identity='PV2-SOURCEFREE-SYNTHETIC-NOT-OBSERVED',
        source_native_inventory=inventory)


# ---------------------------------------------------------------------------
# Outer gate: reconcile candidate E against the precommitted register
# ---------------------------------------------------------------------------

def register_binding_payload(register: PrecommittedOriginalRegister) -> dict:
    """The prospectively committed payload, serializable before execution."""
    return register.binding()


def frozen_root_from_payload(payload: Mapping) -> str:
    return semantic_hash(json.loads(json.dumps(payload, sort_keys=True)))


def _key_for(ref: ExactRef, refs: Mapping) -> str:
    """Reverse-map an exact respondent ref onto its trusted respondent key."""
    for key, value in refs.items():
        if value is not None and _exact(value).key == ref.key:
            return key
    raise OriginalScopeIdentityError('PV2_UNMAPPED_RESPONDENT_REF:' + ref.key)


def _plain_raw_value(witnessed) -> str:
    """Plain source-native value from the owner's exact physical value witness."""
    value = witnessed.get('$raw_physical_value') if isinstance(witnessed, Mapping) else None
    if isinstance(value, Mapping):
        token = value.get('token')
        if isinstance(token, Mapping):
            return str(token.get('v'))
        return str(value)
    return str(witnessed)


def register_inventory_rows(register: PrecommittedOriginalRegister) -> list:
    """The independently authored source-native inventory rows."""
    return [dict(respondent_namespace=c.respondent_namespace,
                 respondent_key=c.respondent_key, item=c.item_short_name,
                 raw_value=c.raw_value, response_state=c.response_state)
            for c in register.source_native_inventory]


def caller_inventory_rows(expected, *, respondent_namespace: str,
                          respondent_refs: Mapping) -> list:
    """The caller-declared source inventory, projected to the register's grain."""
    rows = []
    payload = json.loads(expected.payload_json)
    for row in payload.get('source_inventory') or ():
        rows.append(dict(
            respondent_namespace=respondent_namespace,
            respondent_key=_key_for(ExactRef(**row['respondent_ref']), respondent_refs),
            item=_short_name(ExactRef(**row['item_ref'])),
            raw_value=_plain_raw_value(row['raw_response_value']),
            response_state=row['response_state']))
    return rows


def reconcile_expected_against_register(expected, register: PrecommittedOriginalRegister,
                                       actual_inventory_rows=None) -> dict:
    """Reconcile the caller-supplied E against the precommitted register.

    Refuses every omission, extra, relabel, rekey or suppression, including
    dropped HELD obligations and A-only cherry-picks.  Runs BEFORE any
    accepted-owner durable call.
    """
    if not isinstance(register, PrecommittedOriginalRegister):
        raise OriginalScopeIdentityError('PV2_PRECOMMITTED_REGISTER_REQUIRED')
    if frozen_root_from_payload(register.binding()) != register.committed_root:
        raise OriginalScopeIdentityError('PV2_REGISTER_COMMITTED_ROOT_MISMATCH')
    if register.fixture_use_grant.revoked:
        raise OriginalScopeIdentityError('PV2_FIXTURE_USE_REVOKED_BEFORE_EXECUTION')

    works = expected.checked()
    actual_multiset = Counter(
        (w.original.respondent_namespace, w.legacy.slot) for w in works)
    expected_multiset = register.obligation_multiset
    if actual_multiset != expected_multiset:
        raise OriginalScopeIdentityError(
            'PV2_ORIGINAL_EXPECTED_SCOPE_ANTI_JOIN:' + _canonical(dict(
                missing=sorted([list(k)] * (expected_multiset - actual_multiset).get(k, 0)
                               for k in sorted(expected_multiset - actual_multiset)),
                extra=sorted([list(k)] * (actual_multiset - expected_multiset).get(k, 0)
                             for k in sorted(actual_multiset - expected_multiset)),
                expected=sorted([list(k), n] for k, n in expected_multiset.items()),
                actual=sorted([list(k), n] for k, n in actual_multiset.items()))))

    # Per-obligation trusted metadata, issuer refs and source inventory.
    for work in works:
        obligation = register.obligation_for(
            work.original.respondent_namespace, work.legacy.slot)
        original, legacy = work.original, work.legacy
        checks = (
            ('FORM', original.form, obligation.form),
            ('RESPONDENT_UNIT', original.respondent_unit, obligation.respondent_unit),
            ('LANGUAGE', original.language, obligation.language),
            ('INSTRUMENT_RELEASE', original.instrument_release,
             obligation.instrument_release),
            ('ADMINISTERED_OCCURRENCE', original.administered_occurrence,
             obligation.administered_occurrence),
            ('OPTION_SCOPE', tuple(original.option_scope), tuple(obligation.option_scope)),
            ('SEMANTIC_ROLES', tuple(legacy.semantic_roles), tuple(obligation.semantic_roles)),
            ('CONDITION_ORDER', tuple(legacy.condition_order),
             tuple(obligation.condition_order)),
            ('SEMANTIC_OP_CLASS', legacy.semantic_op_class, obligation.semantic_op_class),
            ('TARGET', legacy.target, obligation.target),
            ('SLOT_ITEM', legacy.item, obligation.item),
            ('STATE', legacy.state, obligation.state),
            ('HOLD_REASON', legacy.hold_reason, obligation.hold_reason),
            ('SOURCE_NATIVE_ITEMS', tuple(_short_name(r) for r in original.native_item_refs),
             tuple(obligation.source_native_items)),
        )
        for code, actual, declared in checks:
            if actual != declared:
                raise OriginalScopeIdentityError(
                    'PV2_' + code + '_BINDING_MISMATCH:' + _canonical(
                        dict(scope=list(obligation.obligation_key), expected=declared,
                             actual=actual)))
        for code, actual, authorized in (
                ('ORIGINAL_U', work.original_U_ref, obligation.original_U_ref),
                ('INDEPENDENT_E', work.independent_E_ref, obligation.independent_E_ref),
                ('CUSTODY', work.independent_custody_ref, obligation.independent_custody_ref),
                ('OPERATION_SCOPE', work.original_operation_scope_ref,
                 obligation.original_operation_scope_ref)):
            if actual != authorized:
                raise OriginalScopeIdentityError(
                    'PV2_' + code + '_ISSUER_NOT_AUTHENTICATED:' + _canonical(
                        dict(scope=list(obligation.obligation_key),
                             authorized=authorized.as_dict(), actual=actual.as_dict())))

    # Independent source-native inventory anchor, before any C11/I03/I05 call.
    register_rows = register_inventory_rows(register)
    inventory_root = semantic_hash(json.loads(
        json.dumps(sorted(_canonical(r) for r in register_rows), sort_keys=True)))
    if inventory_root != register.source_inventory_root:
        raise OriginalScopeIdentityError('PV2_REGISTER_SOURCE_INVENTORY_ROOT_UNSTABLE')
    if actual_inventory_rows is not None:
        expected_rows = Counter(_canonical(r) for r in register_rows)
        observed_rows = Counter(_canonical(r) for r in actual_inventory_rows)
        if expected_rows != observed_rows:
            raise OriginalScopeIdentityError(
                'PV2_ORIGINAL_SOURCE_INVENTORY_ANCHOR_MISMATCH:' + _canonical(dict(
                    missing=sorted((expected_rows - observed_rows).elements()),
                    extra=sorted((observed_rows - expected_rows).elements()),
                    expected_root=register.source_inventory_root)))

    return dict(works=tuple(works), register_committed_root=register.committed_root,
                source_inventory_root=register.source_inventory_root,
                obligation_multiset=dict(expected_multiset),
                held_obligations=sorted(
                    [list(o.obligation_key), o.hold_reason] for o in register.obligations
                    if o.state != 'RUNNABLE'))


def validate_declared_roles_against_topology(work, runtime_catalog, obligation) -> None:
    """Reject a reversed or masked semantic role against actual producer topology.

    The accepted owner assigns the conditioner and target positionally from the
    query's exact target order; a declared role mask must agree with it.
    """
    legacy = work.legacy
    declared = tuple(legacy.semantic_roles)
    if declared != tuple(obligation.semantic_roles):
        raise OriginalScopeIdentityError(
            'PV2_REGISTER_SEMANTIC_ROLE_MISMATCH:' + _canonical(
                dict(scope=list(obligation.obligation_key),
                     expected=list(obligation.semantic_roles), actual=list(declared))))
    if legacy.query_ref is None or len(legacy.condition_order) < 2:
        return
    query = runtime_catalog.resolve_query_exact(legacy.query_ref)
    owner_order = K.C._v2_owner_short_order(query)
    if len(owner_order) < 2:
        return
    positional = tuple(CONDITIONER_ROLE if index == 0 else TARGET_ROLE
                       for index in range(len(owner_order)))
    if declared != positional:
        raise OriginalScopeIdentityError(
            'PV2_SEMANTIC_ROLE_MASK_TOPOLOGY_MISMATCH:' + _canonical(
                dict(scope=list(obligation.obligation_key), query_order=list(owner_order),
                     declared_roles=list(declared), producer_positional_roles=list(positional))))
    if tuple(legacy.condition_order) != owner_order:
        raise OriginalScopeIdentityError(
            'PV2_ROLE_ORDER_TARGET_TOPOLOGY_MISMATCH:' + _canonical(
                dict(scope=list(obligation.obligation_key), declared=list(legacy.condition_order),
                     owner_order=list(owner_order))))


def validate_consumer_roles_against_declared(links, register) -> None:
    """Confirm the actual Field Forge consumer role material matches declared roles.

    For a conditioner/target obligation the declared role mask must bind the
    native item in that position exactly.  For a base/discovery obligation both
    participants must be declared native items in the owner's exact order.
    """
    for link in links:
        material = link.get('consumer_material')
        if not isinstance(material, Mapping):
            continue
        roles = material.get('roles')
        if not isinstance(roles, Mapping):
            continue
        original = link['original_identity']['original']
        namespace = original['respondent_namespace']
        slot = link['original_identity']['operation']['slot']
        obligation = register.obligation_for(namespace, slot)
        items = [_exact(r) for r in original['native_item_refs']]
        conditioner_ref = roles.get(CONDITIONER_ROLE, {}).get('ref')
        target_ref = roles.get(TARGET_ROLE, {}).get('ref')
        if conditioner_ref is None or target_ref is None:
            continue
        conditioner, target = _exact(conditioner_ref), _exact(target_ref)
        declared = list(obligation.semantic_roles)
        scope = list(obligation.obligation_key)
        if CONDITIONER_ROLE in declared and TARGET_ROLE in declared:
            if declared[0] != CONDITIONER_ROLE:
                raise OriginalScopeIdentityError(
                    'PV2_CONSUMER_REVERSED_CONDITIONER_ROLE:' + _canonical(
                        dict(scope=scope, declared=declared)))
            if len(items) < 2 or conditioner != items[0]:
                raise OriginalScopeIdentityError(
                    'PV2_CONSUMER_CONDITIONER_ITEM_MISMATCH:' + _canonical(
                        dict(scope=scope, declared=declared,
                             conditioner=conditioner.as_dict())))
            if len(items) < 2 or target != items[1]:
                raise OriginalScopeIdentityError(
                    'PV2_CONSUMER_TARGET_ITEM_MISMATCH:' + _canonical(
                        dict(scope=scope, declared=declared, target=target.as_dict())))
        else:
            for role, ref in ((CONDITIONER_ROLE, conditioner), (TARGET_ROLE, target)):
                if ref not in items:
                    raise OriginalScopeIdentityError(
                        'PV2_CONSUMER_UNDECLARED_PARTICIPANT_ITEM:' + _canonical(
                            dict(scope=scope, role=role, ref=ref.as_dict(),
                                 declared_items=[i.as_dict() for i in items])))
            if conditioner != items[0] or target != items[1]:
                raise OriginalScopeIdentityError(
                    'PV2_CONSUMER_BASE_TOPOLOGY_ORDER_MISMATCH:' + _canonical(
                        dict(scope=scope, declared=declared,
                             owner_order=[i.as_dict() for i in items])))


def run_sourcefree_with_register(*, expected, selected_scopes,
                                 register: PrecommittedOriginalRegister,
                                 prior_consumer_refs=None,
                                 validate_topology: bool = True,
                                 anchor_c11_inventory: bool = True,
                                 scope_metadata: tuple | None = None) -> dict:
    """Route the precommitted original scope through the adopted owners.

    Reconciles the complete expected set (including HELD obligations) against
    the independently precommitted register BEFORE execution, validates the
    declared semantic roles against the real producer topology, then delegates
    to the adopted V2K successor, and finally confirms the actual Field Forge
    consumer role material.
    """
    scope_list = tuple(selected_scopes)
    if anchor_c11_inventory:
        if scope_metadata is None or len(tuple(scope_metadata)) != len(scope_list):
            raise OriginalScopeIdentityError('PV2_SCOPE_METADATA_REQUIRED')
        caller_rows = []
        for scope, metadata in zip(scope_list, tuple(scope_metadata)):
            refs = (metadata or {}).get('respondent_refs') or {}
            namespace = (metadata or {}).get('respondent_namespace')
            if not refs or not namespace:
                raise OriginalScopeIdentityError('PV2_INVENTORY_REF_MAPS_REQUIRED')
            caller_rows.extend(caller_inventory_rows(
                scope.p01_kwargs['expected'], respondent_namespace=namespace,
                respondent_refs=refs))
        actual_inventory_rows = caller_rows or None
    else:
        actual_inventory_rows = None
    reconciliation = reconcile_expected_against_register(
        expected, register, actual_inventory_rows=actual_inventory_rows)
    works = reconciliation['works']
    by_key = {w.key: w for w in works}

    if validate_topology:
        selected = [key for scope in tuple(selected_scopes) for key in scope.original_work_keys]
        for key in selected:
            work = by_key[key]
            obligation = register.obligation_for(
                work.original.respondent_namespace, work.legacy.slot)
            for scope in tuple(selected_scopes):
                if key not in scope.original_work_keys:
                    continue
                kwargs = scope.p01_kwargs
                if kwargs.get('runtime_catalog') is not None:
                    validate_declared_roles_against_topology(
                        work, kwargs['runtime_catalog'], obligation)
                break

    report = K.run_sourcefree(expected=expected, selected_scopes=selected_scopes,
                              prior_consumer_refs=prior_consumer_refs)
    report = dict(report)
    report['pv2_register'] = dict(
        committed_root=reconciliation['register_committed_root'],
        source_inventory_root=reconciliation['source_inventory_root'],
        obligation_multiset=[list(k) for k in sorted(
            reconciliation['obligation_multiset'])],
        held_obligations=reconciliation['held_obligations'],
        schema=SCHEMA, origin=ORIGIN,
        claim_grade='SOURCEFREE_ORIGINAL_SCOPE_CANDIDATE_NOT_ADOPTED')
    validate_consumer_roles_against_declared(report['links'], register)
    report['pv2_role_topology_verified'] = True
    return report


def read_current_consumer_material(register: PrecommittedOriginalRegister,
                                   report: Mapping) -> dict:
    """Dereference current fixture-use permission at consumer read.

    A revoked TEST_ONLY fixture use cannot newly serve previously computed
    facts; they remain immutable historical records only.
    """
    grant = register.fixture_use_grant
    if grant.revoked:
        return dict(servable=False, revocation_reason=grant.revocation_reason,
                    historical_links=len(report.get('links', [])),
                    claim='PV2_REVOKED_FIXTURE_USE_HISTORICAL_RECORD_ONLY')
    return dict(servable=True, links=list(report.get('links', [])),
                grant=grant.binding(),
                claim='PV2_TEST_ONLY_FIXTURE_USE_CURRENTLY_AVAILABLE')
