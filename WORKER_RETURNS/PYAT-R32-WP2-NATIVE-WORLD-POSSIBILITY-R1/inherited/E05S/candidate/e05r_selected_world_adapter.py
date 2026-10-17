"""R13 E05R — repaired N9-facing selected-world adapter (sourcefree, noninstalling).

A bounded, versioned request / acceptance / receipt interface that lets a
lawful N9-shaped consumer read a coherent multi-field selected-world snapshot
carrying exact native field values, publication / as-of clocks, source and
permission identities, and a nonpooled multi-field readset.

The adapter LINKS existing owners rather than reimplementing them:

* E04's sealed `product.service.GenericSelectedWorldService` supplies the atomic
  selected snapshot, the M4/M5 V557/V558 + M5 RSC structural resolution, and
  the empirical N10E/C1/F8 progressive possibility chain (9/16 -> 5/8 -> 3/4).
* HQ297 N9C's `pre553_hq297_n9c_two_field_reader` supplies the exact
  two-native-unit, two-permission nonpooled readset contract.

It deliberately does NOT install OC05, does not issue N5/N6, does not claim an
operative N9, and never pools the two native fields or infers persons.
"""
from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass, field
import hashlib
import json
from datetime import date

from product.nonparent import consume
from product.scenario import evaluate

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_hq297_n9c_two_field_reader import (
    GSS,
    NCA,
    TestOnlyReadError,
    read_historical_test_only,
)
from rawlsing_next.objective_consumer_bounded_evidence import (
    OC05, installation_manifest)

CONTRACT = 'R13_E05R_N9_SELECTED_WORLD_INTERFACE@2'
REQUEST_SCHEMA = 'N9_SELECTED_WORLD_REQUEST@2'
ACCEPTANCE_SCHEMA = 'N9_SELECTED_WORLD_ACCEPTANCE@2'
RECEIPT_SCHEMA = 'N9_SELECTED_WORLD_RECEIPT@2'

N9_CLOCK_MODES = ('HISTORICAL_PUBLICATION_AWARE',)
SELECTION_MODES = ('TEST_CURRENT', 'AS_OF', 'HISTORICAL')
STRUCTURAL_KEYS = ('training_access', 'training_fee', 'exit_cost',
                   'civil_open', 'civil_sanction')
# The two separately native units carried by the exact N9C reader contract.
NATIVE_FIELD_ROLES = (GSS, NCA)

N9_INSTALLATION_STATE = 'NOT_YET_APPLICABLE'
NONINSTALLING_GRADE = 'NONINSTALLING_SOURCEFREE_ADAPTER_CANDIDATE'


class N9SelectedWorldRefusal(ValueError):
    """Typed refusal of an N9-shaped selected-world request."""


class SelectedWorldInconsistency(N9SelectedWorldRefusal):
    """Atomic selected-snapshot consistency failure across channels."""


def _canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def _refs(value) -> tuple:
    if not isinstance(value, (list, tuple)) or not value:
        raise N9SelectedWorldRefusal('NONEMPTY_EXACT_REF_TUPLE_REQUIRED')
    out = []
    for item in value:
        if not isinstance(item, Mapping) or set(item) != {'kind', 'object_id', 'content_hash'}:
            raise N9SelectedWorldRefusal('EXACT_REF_REQUIRED')
        out.append(_canonical(item))
    if len(set(out)) != len(out):
        raise N9SelectedWorldRefusal('DUPLICATE_EXACT_REF_REQUIRED')
    return tuple(out)


@dataclass(frozen=True)
class SelectedWorldClock:
    """Explicit synthetic selection clocks; never the wall clock."""

    mode: str
    valid_at: str
    published_asof: str
    test_now: str | None = None

    def __post_init__(self) -> None:
        if self.mode not in SELECTION_MODES:
            raise N9SelectedWorldRefusal('UNKNOWN_SELECTION_MODE:' + str(self.mode))
        for name in ('valid_at', 'published_asof'):
            value = getattr(self, name)
            if not isinstance(value, str) or len(value) != 10:
                raise N9SelectedWorldRefusal('EXACT_ISO_DATE_REQUIRED:' + name)
            try:
                if date.fromisoformat(value).isoformat() != value:
                    raise ValueError()
            except ValueError as exc:
                raise N9SelectedWorldRefusal('EXACT_ISO_DATE_REQUIRED:' + name) from exc
        if self.mode == 'TEST_CURRENT':
            if not self.test_now:
                raise N9SelectedWorldRefusal('EXPLICIT_TEST_CURRENT_CLOCK_REQUIRED')
            if self.valid_at != self.test_now or self.published_asof != self.test_now:
                raise N9SelectedWorldRefusal('EXPLICIT_TEST_CURRENT_CLOCK_REQUIRED')

    def binding(self) -> dict:
        return dict(mode=self.mode, valid_at=self.valid_at,
                    published_asof=self.published_asof, test_now=self.test_now)


@dataclass(frozen=True)
class N9SelectedWorldRequest:
    """Versioned N9-shaped selected-world request."""

    contract: str
    purpose: str
    structural_keys: tuple
    empirical_target: str
    empirical_conditions: tuple
    native_field_roles: tuple
    clock: SelectedWorldClock
    requested_pooling: bool = False
    requested_person_exposure: bool = False
    requested_model_use: bool = False

    def __post_init__(self) -> None:
        if self.contract != CONTRACT:
            raise N9SelectedWorldRefusal('UNKNOWN_N9_INTERFACE_CONTRACT:' + str(self.contract))
        if self.purpose != 'TEST_ONLY_CONTEXT':
            raise N9SelectedWorldRefusal('SOURCEFREE_ONLY_PURPOSE_REQUIRED')
        if self.requested_pooling or self.requested_person_exposure or \
                self.requested_model_use:
            raise N9SelectedWorldRefusal('PERSON_POOLING_OR_MODEL_PROMOTION_FORBIDDEN')
        if not isinstance(self.structural_keys, tuple) or not self.structural_keys:
            raise N9SelectedWorldRefusal('NONEMPTY_EXACT_STRUCTURAL_READSET_REQUIRED')
        if len(set(self.structural_keys)) != len(self.structural_keys):
            raise N9SelectedWorldRefusal('DUPLICATE_STRUCTURAL_KEY_REQUIRED')
        for key in self.structural_keys:
            if key not in STRUCTURAL_KEYS:
                raise N9SelectedWorldRefusal('UNKNOWN_STRUCTURAL_FIELD_KEY:' + str(key))
        if not isinstance(self.empirical_target, str) or not self.empirical_target:
            raise N9SelectedWorldRefusal('EXACT_NATIVE_TARGET_REQUIRED')
        if not isinstance(self.empirical_conditions, tuple) or not self.empirical_conditions:
            raise N9SelectedWorldRefusal('EXACT_NONEMPTY_UNIQUE_ORDERED_CONDITIONERS_REQUIRED')
        seen = []
        for pair in self.empirical_conditions:
            if not isinstance(pair, tuple) or len(pair) != 2:
                raise N9SelectedWorldRefusal('ORDERED_EXACT_NATIVE_VALUE_BINDINGS_REQUIRED')
            name, value = pair
            if not isinstance(name, str) or not name:
                raise N9SelectedWorldRefusal('ORDERED_EXACT_NATIVE_VALUE_BINDINGS_REQUIRED')
            if isinstance(value, bool) or not isinstance(value, int):
                raise N9SelectedWorldRefusal('ORDERED_EXACT_NATIVE_VALUE_BINDINGS_REQUIRED')
            if name in seen:
                raise N9SelectedWorldRefusal('EXACT_NONEMPTY_UNIQUE_ORDERED_CONDITIONERS_REQUIRED')
            seen.append(name)
        if not isinstance(self.native_field_roles, tuple) or not self.native_field_roles:
            raise N9SelectedWorldRefusal('NONEMPTY_EXACT_NATIVE_FIELD_READSET_REQUIRED')
        if len(set(self.native_field_roles)) != len(self.native_field_roles):
            raise N9SelectedWorldRefusal('DUPLICATE_NATIVE_FIELD_ROLE_REQUIRED')
        for role in self.native_field_roles:
            if role not in NATIVE_FIELD_ROLES:
                raise N9SelectedWorldRefusal('UNKNOWN_NATIVE_FIELD_ROLE:' + str(role))
        if len(self.native_field_roles) < 2:
            raise N9SelectedWorldRefusal('TWO_SEPARATELY_NATIVE_UNITS_REQUIRED')
        if not isinstance(self.clock, SelectedWorldClock):
            raise N9SelectedWorldRefusal('TYPED_SELECTION_CLOCK_REQUIRED')

    @property
    def request_hash(self) -> str:
        return semantic_hash(json.loads(json.dumps(self.binding(), sort_keys=True)))

    def binding(self) -> dict:
        return dict(schema=REQUEST_SCHEMA, contract=CONTRACT, purpose=self.purpose,
                    structural_keys=list(self.structural_keys),
                    empirical_target=self.empirical_target,
                    empirical_conditions=[list(c) for c in self.empirical_conditions],
                    native_field_roles=list(self.native_field_roles),
                    clock=self.clock.binding(),
                    requested_pooling=self.requested_pooling,
                    requested_person_exposure=self.requested_person_exposure,
                    requested_model_use=self.requested_model_use)

    @classmethod
    def from_binding(cls, raw: Mapping) -> 'N9SelectedWorldRequest':
        if set(raw) != {'schema', 'contract', 'purpose', 'structural_keys',
                        'empirical_target', 'empirical_conditions', 'native_field_roles',
                        'clock', 'requested_pooling', 'requested_person_exposure',
                        'requested_model_use'}:
            raise N9SelectedWorldRefusal('REQUEST_RECORD_FIELDS_MISSING_OR_UNKNOWN')
        if raw['schema'] != REQUEST_SCHEMA:
            raise N9SelectedWorldRefusal('REQUEST_SCHEMA_VERSION_MISMATCH')
        clock_raw = raw['clock']
        if set(clock_raw) != {'mode', 'valid_at', 'published_asof', 'test_now'}:
            raise N9SelectedWorldRefusal('CLOCK_RECORD_FIELDS_MISSING_OR_UNKNOWN')
        return cls(
            contract=raw['contract'], purpose=raw['purpose'],
            structural_keys=tuple(raw['structural_keys']),
            empirical_target=raw['empirical_target'],
            empirical_conditions=tuple(tuple(c) for c in raw['empirical_conditions']),
            native_field_roles=tuple(raw['native_field_roles']),
            clock=SelectedWorldClock(**clock_raw),
            requested_pooling=bool(raw['requested_pooling']),
            requested_person_exposure=bool(raw['requested_person_exposure']),
            requested_model_use=bool(raw['requested_model_use']))


def _float_free(value):
    """Exact, float-free projection so semantic identity stays total.

    A published decimal is carried losslessly as an exact decimal literal; the
    verbatim value is preserved in the receipt payload and locked by the
    payload digest, so no result-bearing number is lost or rounded.
    """
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, float):
        return {'$exact_decimal': repr(value)}
    if isinstance(value, Mapping):
        return {k: _float_free(v) for k, v in sorted(value.items())}
    if isinstance(value, (list, tuple)):
        return [_float_free(v) for v in value]
    return value


@dataclass(frozen=True)
class N9SelectedWorldAcceptance:
    """Versioned acceptance: the atomic snapshot the request is bound to."""

    request_hash: str
    snapshot_hash: str
    catalog_hash: str
    structural_keys: tuple
    native_field_roles: tuple
    native_field_refs: tuple
    empirical_source_identity: dict
    permission_roots: tuple
    publication_clocks: tuple
    effective_clocks: tuple
    field_clock_bindings: dict
    acceptance_state: str
    inconsistencies: tuple

    @property
    def acceptance_hash(self) -> str:
        return semantic_hash(json.loads(json.dumps(self.binding(), sort_keys=True)))

    def binding(self) -> dict:
        return dict(
            schema=ACCEPTANCE_SCHEMA, contract=CONTRACT,
            request_hash=self.request_hash, snapshot_hash=self.snapshot_hash,
            catalog_hash=self.catalog_hash,
            structural_keys=list(self.structural_keys),
            native_field_roles=list(self.native_field_roles),
            native_field_refs=list(self.native_field_refs),
            empirical_source_identity=self.empirical_source_identity,
            permission_roots=list(self.permission_roots),
            publication_clocks=list(self.publication_clocks),
            effective_clocks=list(self.effective_clocks),
            field_clock_bindings=self.field_clock_bindings,
            acceptance_state=self.acceptance_state,
            inconsistencies=list(self.inconsistencies))


class N9SelectedWorldAdapter:
    """Sourcefree, noninstalling N9-shaped selected-world adapter."""

    def __init__(self, *, service, registry, service_options: Mapping | None = None):
        self.service = service
        self.registry = registry
        self._field_refs = registry.refs_by_role()
        self._relation = dict(
            kind='TEST_ONLY_NONPOOLED_COPRESENCE', fixture_only=True, issued_EE13=False,
            ordered_refs=[self._field_refs[role] for role in NATIVE_FIELD_ROLES],
            population_join=False)
        self._native_revoked: dict = {}
        self.acceptances: dict = {}
        self.receipts: dict = {}
        self.value_reads: list = []
        self.installation = {row['policy_id']: row for row in installation_manifest()}
        assert self.installation[OC05]['current_applicability'] == N9_INSTALLATION_STATE
        assert self.installation[OC05]['consumer_seam'] is None

    # -- snapshot ---------------------------------------------------------
    def build_snapshot(self, request: N9SelectedWorldRequest):
        """The single atomic selected snapshot for this request's clocks.

        N9C's as-of clock is DERIVED from the snapshot's published clock, so a
        caller cannot split the world and field clocks apart.
        """
        clock = request.clock
        try:
            return self.service.select(
                mode=clock.mode, valid_at=clock.valid_at,
                published_asof=clock.published_asof, test_now=clock.test_now,
                purpose=request.purpose)
        except ValueError as exc:
            raise SelectedWorldInconsistency(
                'SELECTED_SNAPSHOT_CONSTRUCTION_REFUSED:' + str(exc)) from exc

    # -- native field readset (exact N9C contract) ------------------------
    def _read_native_fields(self, request, snapshot, selected_refs=None):
        """Nonpooled multi-field readset through the exact N9C reader contract.

        The as-of clock is taken from the atomic snapshot, never from the
        caller, so world currentness and field currentness cannot diverge.
        """
        as_of = snapshot.material['published_asof']
        refs = self._field_refs if selected_refs is None else selected_refs
        relation = dict(self._relation, ordered_refs=[refs[r] for r in NATIVE_FIELD_ROLES])
        try:
            return read_historical_test_only(
                self.registry, selected_refs=refs, relation=relation,
                as_of=as_of, clock_mode='HISTORICAL_PUBLICATION_AWARE',
                partial_allowed=True, requested_person_exposure=request.requested_person_exposure,
                requested_pooling=request.requested_pooling,
                requested_model_use=request.requested_model_use)
        except TestOnlyReadError as exc:
            raise SelectedWorldInconsistency(
                'NATIVE_FIELD_READSET_REFUSED:' + exc.code) from exc

    def _verify_selection(self, request, snapshot):
        """Use the original catalog registration and exact producer selection."""
        snapshot.verify()
        material = snapshot.material
        expected = dict(mode=request.clock.mode, valid_at=request.clock.valid_at,
                        published_asof=request.clock.published_asof,
                        purpose=request.purpose)
        if any(material.get(k) != v for k, v in expected.items()):
            raise SelectedWorldInconsistency('REQUEST_SNAPSHOT_CLOCK_OR_PURPOSE_MISMATCH')
        # Verifies source catalog, original registered snapshot, and current grant.
        self.service.catalog.read(snapshot, 'empirical')
        for key in request.structural_keys:
            slot = material['fields'].get(key) or {}
            record = self.service.catalog._select_record(
                key, request.clock.valid_at, request.clock.published_asof)
            if record is not None:
                ref = slot.get('field_ref')
                if ref != record['ref']:
                    raise SelectedWorldInconsistency('SELECTED_NATIVE_PRODUCER_BINDING_MISMATCH')

    def _fresh_native(self, request, snapshot, entry):
        # Re-read the currently attached original registry using ACCEPTED refs.
        # New same-value releases cannot renew old grants. Missing/rekeyed arms
        # stay dependencies with typed refusal; never substitute by number.
        try:
            self.registry.refs_by_role()  # uniqueness/current registry, never a cached index
        except TestOnlyReadError as exc:
            raise SelectedWorldInconsistency('CURRENT_NATIVE_REGISTRY_REFUSED:' + exc.code) from exc
        native = self._read_native_fields(request, snapshot,
                                         selected_refs=entry['selected_refs'])
        revoked = set(self._native_revoked)
        for value in list(native['values_read']):
            if value['role'] in revoked:
                native['values_read'].remove(value)
                native['refusals'].append(dict(role=value['role'],
                    fixture_ref=value['fixture_ref'], reason='SOURCE_REVOKED'))
        native['successful_value_refset'] = [v['fixture_ref'] for v in native['values_read']]
        native['state'] = ('TWO_VALUES_READ_TEST_ONLY' if len(native['values_read']) == 2
                           else 'PARTIAL_TEST_ONLY_NOT_POSITIVE' if native['values_read']
                           else 'REFUSED_REQUIRED_FIELD_TEST_ONLY')
        # N9C's original snapshot identity is valid only for its original output.
        # Local withdrawal overlay has its own explicitly named identity.
        if revoked:
            native['original_n9c_snapshot_ref'] = native.pop('test_snapshot_ref')
            native['adapter_withdrawal_scopes'] = sorted(revoked)
            native['adapter_read_hash'] = semantic_hash(_float_free(native))
        return native

    def _consumers(self, request, snapshot, supplied):
        if not supplied:
            return []
        if not isinstance(supplied, (tuple, list)) or len(supplied) != 2:
            raise SelectedWorldInconsistency('TWO_ORIGINAL_CONSUMERS_REQUIRED')
        if [c.get('consumer') for c in supplied] != [
                'NONPARENT_OPTIONS', 'CONCEPTION_SCENARIO_PROPOSALS']:
            raise SelectedWorldInconsistency('TWO_ORIGINAL_CONSUMERS_REQUIRED')
        if (request.empirical_target != 'Y' or request.empirical_conditions !=
                (('A', 1), ('B', 1), ('C', 1)) or
                set(request.structural_keys) != set(STRUCTURAL_KEYS)):
            raise SelectedWorldInconsistency('CONSUMER_READSET_OUTSIDE_ACCEPTED_REQUEST')
        try:
            proposals = [dict(scenario_id=p['scenario_id'], route=p['route'])
                         for p in supplied[1]['scenarios']]
            # Exact original consumer functions execute within this boundary.
            # Their envelopes are compared in FULL, never via caller hashes.
            actual = [consume(self.service, snapshot)['material'],
                      evaluate(self.service, snapshot, proposals)['material']]
        except (KeyError, TypeError, ValueError) as exc:
            raise SelectedWorldInconsistency('CONSUMER_MATERIAL_REFUSED:' + str(exc)) from exc
        if _canonical(actual) != _canonical(supplied):
            raise SelectedWorldInconsistency('CONSUMER_MATERIAL_NOT_EXACT_ORIGINAL_OUTPUT')
        return actual

    # -- acceptance -------------------------------------------------------
    def accept(self, request: N9SelectedWorldRequest, snapshot) -> N9SelectedWorldAcceptance:
        """Bind the request to one atomic snapshot and verify consistency."""
        self._verify_selection(request, snapshot)
        snapshot_hash = snapshot.snapshot_hash
        catalog_hash = snapshot.material['catalog_hash']
        empirical = snapshot.material['empirical']
        field_roles = []
        for key in request.structural_keys:
            slot = snapshot.material['fields'].get(key)
            if slot is None:
                field_roles.append('MISSING:' + key)
        for role in request.native_field_roles:
            if role not in self._field_refs:
                field_roles.append('UNREGISTERED:' + role)

        roles = [role for role in request.native_field_roles
                 if role in self._field_refs]
        native_refs = tuple(self._field_refs[role] for role in roles)

        permission_roots = {empirical.get('permission_root')}
        publication_clocks = {empirical.get('publication')}
        for key in request.structural_keys:
            slot = snapshot.material['fields'].get(key)
            if not slot:
                continue
            payload = slot.get('payload') or {}
            if payload.get('source_root'):
                permission_roots.add(payload['source_root'])
            if payload.get('publication'):
                publication_clocks.add(payload['publication'])
        permission_roots.discard(None)
        publication_clocks.discard(None)

        native = self._read_native_fields(request, snapshot)
        inconsistencies = []
        for item in native.get('refusals') or ():
            inconsistencies.append('NATIVE_FIELD_REFUSAL:' + item['reason'])
        if len(permission_roots) > 1:
            inconsistencies.append('FRAGMENTED_PERMISSION_ROOT')
        for problem in field_roles:
            if problem.startswith('MISSING:') or problem.startswith('UNREGISTERED:'):
                inconsistencies.append(problem)
        # Atomic clock consistency: every resolved field must be inside the
        # ONE selection clock pair carried by this snapshot.  Distinct
        # effective_from values are a legitimate structural revision, not an
        # inconsistency, so they are reported, never refused.
        clock_bindings = {}
        for key in request.structural_keys:
            payload = (snapshot.material['fields'].get(key) or {}).get('payload') or {}
            if not payload:
                continue
            clock_bindings[key] = dict(
                effective_from=payload.get('effective_from'),
                effective_to=payload.get('effective_to'),
                publication=payload.get('publication'),
                revision=payload.get('revision'))
            if not (payload['effective_from'] <= snapshot.material['valid_at']
                    < payload['effective_to']):
                inconsistencies.append('FIELD_EFFECTIVE_CLOCK_OUTSIDE_SELECTION:' + key)
            if payload['publication'] > snapshot.material['published_asof']:
                inconsistencies.append('FIELD_PUBLICATION_CLOCK_OUTSIDE_SELECTION:' + key)
        if empirical.get('publication') and \
                empirical['publication'] > snapshot.material['published_asof']:
            inconsistencies.append('EMPIRICAL_PUBLICATION_CLOCK_OUTSIDE_SELECTION')
        # The native readset must cover exactly the requested roles, never a
        # silently different set.
        if set(r['role'] for r in native['values_read']) - set(request.native_field_roles):
            inconsistencies.append('NATIVE_FIELDSET_OUTSIDE_REQUEST')
        if len(native['dependency_readset']) != len(request.native_field_roles):
            inconsistencies.append('NATIVE_DEPENDENCY_READSET_ARM_NOT_EXACT')
        # Nonpooling: the two native fields must not collapse into one class.
        read_roles = [r['role'] for r in native['values_read']]
        if len(read_roles) == 2 and len({r['source_family'] for r in native['values_read']}) != 2:
            inconsistencies.append('ORIGINAL_SOURCE_CLASS_COLLISION')

        state = 'ACCEPTED_ATOMIC_SELECTED_SNAPSHOT' if not inconsistencies else \
            'ACCEPTED_WITH_TYPED_PARTIAL'
        acceptance = N9SelectedWorldAcceptance(
            request_hash=request.request_hash, snapshot_hash=snapshot_hash,
            catalog_hash=catalog_hash, structural_keys=request.structural_keys,
            native_field_roles=request.native_field_roles, native_field_refs=native_refs,
            empirical_source_identity=dict(
                source_universe_ref=empirical.get('source_universe_ref'),
                release_ref=empirical.get('release_ref'),
                risk_set_ref=empirical.get('risk_set_ref'),
                rows_hash=empirical.get('rows_hash'),
                permission_root=empirical.get('permission_root'),
                publication=empirical.get('publication'),
                field_time=empirical.get('field_time'),
                native_geography=empirical.get('native_geography'),
                native_unit=empirical.get('native_unit'),
                grade=empirical.get('grade'),
                state=empirical.get('state')),
            permission_roots=tuple(sorted(permission_roots)),
            publication_clocks=tuple(sorted(publication_clocks)),
            effective_clocks=tuple(sorted(clock_bindings[k]['effective_from']
                                          for k in sorted(clock_bindings))),
            field_clock_bindings=clock_bindings,
            acceptance_state=state, inconsistencies=tuple(inconsistencies))
        self.acceptances[acceptance.acceptance_hash] = dict(
            acceptance=deepcopy(acceptance), snapshot_material=deepcopy(snapshot.material),
            request_binding=deepcopy(request.binding()),
            selected_refs=deepcopy(self._field_refs), native=deepcopy(native))
        return acceptance

    # -- receipt ----------------------------------------------------------
    def serve(self, request: N9SelectedWorldRequest, acceptance,
              snapshot, *, consumers=()) -> dict:
        """Read the actual result-bearing selected-world values.

        Every channel is read through the accepted atomic snapshot.  The two
        native fields are carried separately with their own native units and
        are never pooled, converted or combined.
        """
        entry = self.acceptances.get(acceptance.acceptance_hash)
        if entry is None:
            raise SelectedWorldInconsistency('ACCEPTANCE_BINDING_MISMATCH')
        snapshot.verify()
        if entry['snapshot_material'] != snapshot.material:
            raise SelectedWorldInconsistency('ACCEPTED_SNAPSHOT_SUBSTITUTION')
        if entry['acceptance'] != acceptance:
            raise SelectedWorldInconsistency('ACCEPTANCE_BINDING_MISMATCH')

        if (request.request_hash != acceptance.request_hash or
                request.binding() != entry['request_binding']):
            raise SelectedWorldInconsistency('REQUEST_ACCEPTANCE_BINDING_MISMATCH')
        if snapshot.snapshot_hash != acceptance.snapshot_hash:
            raise SelectedWorldInconsistency('ACCEPTED_SNAPSHOT_SUBSTITUTION')
        self._verify_selection(request, snapshot)
        native = self._fresh_native(request, snapshot, entry)
        # E04N found mutable E04 cache projections are not owner proof. Clear
        # only this candidate's transient query cache, then execute the exact
        # original provider and owners. No E04R adoption or owner patch.
        self.service.provider.cache.clear()
        consumers = self._consumers(request, snapshot, consumers)
        structural_values = {}
        structural_refs = {}
        for key in request.structural_keys:
            read = self.service.structural(snapshot, key, 'N9_SELECTED_WORLD')
            structural_refs[key] = (read.get('field_ref'), read.get('requested_ref'))
            if read['state'] == 'SUPPORTED_TEST_ONLY':
                structural_values[key] = dict(
                    value=read['value'], unit=read['payload']['unit'],
                    field_ref=read['field_ref'], revision=read['payload']['revision'],
                    publication=read['payload']['publication'],
                    effective_from=read['payload']['effective_from'],
                    epistemic_class=read['payload']['epistemic_class'],
                    currentness_grade=read.get('currentness_grade'),
                    rsc_ref=read.get('rsc_ref'), validation_ref=read.get('validation_ref'))
            else:
                structural_values[key] = dict(
                    state=read['state'], requested_ref=read.get('requested_ref'))

        empirical = self.service.possibilities(
            snapshot, target=request.empirical_target,
            conditions=request.empirical_conditions, consumer='N9_SELECTED_WORLD')
        empirical_steps = deepcopy(empirical['steps'])

        field_values = [dict(record) for record in native['values_read']]
        field_refusals = [dict(item) for item in native['refusals']]

        # Nonpooled, two separately native units: the readset carries both
        # roles, both refs and both values; there is no cross-field ratio.
        units = sorted({r['native_unit'] for r in field_values})
        families = sorted({r['source_family'] for r in field_values})
        if len(field_values) == 2 and len(families) != 2:
            raise SelectedWorldInconsistency('ORIGINAL_SOURCE_CLASS_COLLISION')
        if len(field_values) == 2 and len(units) != 2:
            raise SelectedWorldInconsistency('NATIVE_UNIT_COLLISION')

        receipt = dict(
            schema=RECEIPT_SCHEMA, contract=CONTRACT,
            grade=NONINSTALLING_GRADE,
            claim_ceiling=empirical.get('claim_ceiling'),
            acceptance_hash=acceptance.acceptance_hash,
            acceptance_state=acceptance.acceptance_state,
            request_hash=acceptance.request_hash,
            snapshot_hash=acceptance.snapshot_hash,
            catalog_hash=acceptance.catalog_hash,
            selection=dict(mode=snapshot.material['mode'],
                           valid_at=snapshot.material['valid_at'],
                           published_asof=snapshot.material['published_asof'],
                           purpose=snapshot.material['purpose']),
            permission_roots=list(acceptance.permission_roots),
            publication_clocks=list(acceptance.publication_clocks),
            effective_clocks=list(acceptance.effective_clocks),
            structural_readset=list(request.structural_keys),
            structural_values=structural_values,
            structural_value_refs={k: v for k, v in structural_refs.items()},
            empirical_target=request.empirical_target,
            empirical_condition_order=request.empirical_conditions,
            empirical_state=empirical['state'],
            empirical_steps=empirical_steps,
            empirical_native_time=empirical.get('native_time'),
            native_field_readset=dict(
                roles=list(request.native_field_roles),
                refs=[entry['selected_refs'][r] for r in request.native_field_roles],
                dependency_readset=list(native['dependency_readset']),
                successful_value_refset=list(native['successful_value_refset']),
                values_read=field_values, refusals=field_refusals,
                as_of=snapshot.material['published_asof'],
                state=native['state']),
            pooling=False, person_exposure=False, model_use=False,
            native_units=units, source_families=families,
            operative_N9=False, operative_OC05=False, installed_OC05=self.installation,
            issued_N5N6=False, issued_EE13=False, new_issuer=False,
            consumers=[dict(consumer=c.get('consumer'), state=c.get('state'),
                            consumer_material=deepcopy(c))
                       for c in consumers],
        )
        inconsistencies = list(acceptance.inconsistencies)
        for consumer in consumers:
            if consumer['state'] not in ('OPTIONS_AND_SOURCE_SUPPORT_PRODUCED',
                                         'FINITE_PROPOSALS_EVALUATED'):
                inconsistencies.append('CONSUMER_TYPED_PARTIAL:' + consumer['consumer'])
        if empirical['state'] != 'PRODUCTIVE_TEST_ONLY':
            inconsistencies.append('EMPIRICAL_NOT_PRODUCTIVE:' + empirical['state'])
        if native['state'] != 'TWO_VALUES_READ_TEST_ONLY':
            inconsistencies.append('NATIVE_FIELDSET_NOT_COMPLETE:' + native['state'])
        for key, value in structural_values.items():
            if 'state' in value:
                inconsistencies.append('STRUCTURAL_FIELD_UNAVAILABLE:' + key + ':' +
                                       value['state'])
        receipt['inconsistencies'] = inconsistencies
        receipt['state'] = ('SELECTED_WORLD_VALUES_SERVED' if not inconsistencies
                            else 'TYPED_PARTIAL_SELECTED_WORLD')
        # Two explicit identities: a total float-free semantic identity over the
        # receipt content, and a byte digest over the verbatim receipt (which
        # carries receipt_hash) preserving every published decimal exactly.
        receipt_hash = semantic_hash(_float_free(receipt))
        receipt['receipt_hash'] = receipt_hash
        receipt['receipt_payload_sha256'] = hashlib.sha256(
            _canonical(receipt).encode()).hexdigest()
        self.receipts[receipt_hash] = deepcopy(receipt)
        self.value_reads.append(dict(
            consumer='N9_SELECTED_WORLD', snapshot_hash=acceptance.snapshot_hash,
            receipt_hash=receipt_hash, state=receipt['state'],
            structural=[dict(key=k, value=v.get('value'), unit=v.get('unit'))
                        for k, v in structural_values.items()],
            empirical=[dict(target=s['target'], denominator=s['denominator'],
                            cells={c['cell']: c['raw_numerator_support']
                                   for c in s['cells']})
                       for s in empirical_steps],
            native_fields=[dict(role=r['role'], unit=r['native_unit'],
                                values=r['values'])
                           for r in field_values]))
        return receipt

    def invalidate(self, scope, reason='TEST_ONLY_PERMISSION_REVOCATION'):
        """Revoke a world or field permission scope.

        The underlying selected-world service revokes the scope; every receipt
        that depends on it is invalidated for fresh use while retained as
        historical evidence.  Unrelated receipts stay servable.
        """
        if scope in NATIVE_FIELD_ROLES:
            self._native_revoked[scope] = reason
            revocation = dict(scope=scope, reason=reason, fixture_only=True,
                              state='REVOKED_FOR_FRESH_ADAPTER_USE')
        else:
            revocation = self.service.catalog.revoke(scope, reason)
        affected = []
        for receipt_hash, receipt in list(self.receipts.items()):
            dependencies = set(receipt.get('structural_readset') or ())
            dependencies.add('empirical')
            dependencies.update(
                r for r in receipt['native_field_readset']['roles'])
            if scope in dependencies:
                affected.append(receipt_hash)
        unaffected = [h for h in self.receipts if h not in affected]
        return dict(revocation=revocation, scope=scope, reason=reason,
                    invalidated_for_fresh_use=sorted(affected),
                    unaffected=sorted(unaffected),
                    historical_receipts_retained=True,
                    old_receipt_hashes=sorted(self.receipts))

    def historical_receipt(self, receipt_hash):
        receipt = deepcopy(self.receipts[receipt_hash])
        receipt.pop('receipt_hash', None)
        receipt.pop('receipt_payload_sha256', None)
        return dict(receipt=receipt, archival_only=True, fresh_use_authorized=False)

    # -- one-shot ---------------------------------------------------------
    def request_and_serve(self, request: N9SelectedWorldRequest, *, consumers=(),
                          snapshot=None) -> dict:
        """Accept and serve in one call, always against one atomic snapshot."""
        snapshot = snapshot if snapshot is not None else self.build_snapshot(request)
        acceptance = self.accept(request, snapshot)
        return self.serve(request, acceptance, snapshot, consumers=consumers)


def standard_request(*, label: str, structural_keys=STRUCTURAL_KEYS,
                     target: str = 'Y', conditions=(('A', 1), ('B', 1), ('C', 1)),
                     **flags) -> N9SelectedWorldRequest:
    """A canonical N9-shaped request over the two separately native fields."""
    clocks = {
        'CURRENT_TEST_CLOCK': SelectedWorldClock(
            mode='TEST_CURRENT', valid_at='2027-09-01', published_asof='2027-09-01',
            test_now='2027-09-01'),
        'HISTORICAL_AS_OF': SelectedWorldClock(
            mode='AS_OF', valid_at='2026-06-01', published_asof='2026-03-01'),
        'TYPED_PARTIAL_PRE_NCA_PUBLICATION': SelectedWorldClock(
            mode='AS_OF', valid_at='2022-06-01', published_asof='2022-06-01'),
    }
    return N9SelectedWorldRequest(
        contract=CONTRACT, purpose='TEST_ONLY_CONTEXT', structural_keys=tuple(structural_keys),
        empirical_target=target, empirical_conditions=tuple(
            tuple(c) for c in conditions),
        native_field_roles=NATIVE_FIELD_ROLES, clock=clocks[label], **flags)
