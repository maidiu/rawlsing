"""HQ295 V2K: isolated SOURCE-FREE original expected-work identity successor.

Published V2 keys/owners are unchanged. New keys bind explicit original inputs;
legacy keys remain separately named P01 execution links. Digests are identity /
integrity only, never source, scientific or independent-custody authority. This
candidate deliberately has no original-source execution entrypoint.
"""
from dataclasses import dataclass, fields
import json
from collections.abc import Mapping
from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref, canonical_json, semantic_hash
from rawlsing_next import pre553_original_workload_contract_v2_candidate as C
from rawlsing_next import pre553_v2_durable_consumer_integration_candidate as P

SCHEMA = 'HQ295_ORIGINAL_EXPECTED_WORK_V2K_CANDIDATE@1.0.0'
ORIGIN = 'INDEPENDENT_SOURCEFREE_BEFORE_EXECUTION'


class IdentityError(ValueError):
    """Typed original identity, binding, or outer reconciliation failure."""


def _record_fields(raw, names):
    if not isinstance(raw, Mapping) or set(raw) != set(names):
        raise IdentityError('ORIGINAL_RECORD_FIELDS_MISSING_OR_UNKNOWN')
    return dict(raw)


def _ref(value):
    if not isinstance(value, ExactRef):
        raise IdentityError('EXACT_REF_REQUIRED')
    return value.as_dict()


@dataclass(frozen=True)
class OriginalIdentity:
    source_release_ref: ExactRef
    empirical_universe_ref: ExactRef
    native_item_refs: tuple[ExactRef, ...]
    respondent_namespace: str
    respondent_unit: str
    form: str
    language: str
    instrument_release: str
    administered_occurrence: str
    option_scope: tuple[str, ...]
    routing_refs: tuple[ExactRef, ...]
    original_item_scope_ref: ExactRef

    def __post_init__(self):
        for name in ('respondent_namespace', 'respondent_unit', 'form', 'language',
                     'instrument_release', 'administered_occurrence'):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                raise IdentityError('ORIGINAL_IDENTITY_FIELD_REQUIRED:' + name)
        for name in ('native_item_refs', 'routing_refs'):
            values = getattr(self, name)
            if not isinstance(values, tuple) or not values or len(set(values)) != len(values):
                raise IdentityError('NONEMPTY_UNIQUE_EXACT_REF_TUPLE_REQUIRED:' + name)
            for value in values:
                _ref(value)
        if not isinstance(self.option_scope, tuple) or not self.option_scope or not all(
            isinstance(v, str) and v for v in self.option_scope):
            raise IdentityError('ORIGINAL_OPTION_SCOPE_REQUIRED')
        _ref(self.source_release_ref); _ref(self.empirical_universe_ref); _ref(self.original_item_scope_ref)

    def preimage(self):
        return dict(source_release_ref=_ref(self.source_release_ref),
            empirical_universe_ref=_ref(self.empirical_universe_ref),
            native_item_refs=[_ref(r) for r in self.native_item_refs],
            respondent_namespace=self.respondent_namespace, respondent_unit=self.respondent_unit,
            form=self.form, language=self.language, instrument_release=self.instrument_release,
            administered_occurrence=self.administered_occurrence, option_scope=list(self.option_scope),
            routing_refs=[_ref(r) for r in sorted(self.routing_refs, key=lambda r: r.key)],
            original_item_scope_ref=_ref(self.original_item_scope_ref))

    @classmethod
    def from_preimage(cls, raw):
        values = _record_fields(raw, (f.name for f in fields(cls)))
        for name in ('source_release_ref', 'empirical_universe_ref', 'original_item_scope_ref'):
            values[name] = ExactRef(**values[name])
        for name in ('native_item_refs', 'routing_refs'):
            values[name] = tuple(ExactRef(**r) for r in values[name])
        values['option_scope'] = tuple(values['option_scope'])
        return cls(**values)


def legacy_preimage(declaration):
    raw = {f.name: getattr(declaration, f.name) for f in fields(declaration)}
    for name in ('query_ref', 'predicate_ref', 'discovery_authority_ref'):
        if raw[name] is not None:
            raw[name] = _ref(raw[name])
    for name in ('semantic_roles', 'condition_order'):
        raw[name] = list(raw[name])
    return raw


def legacy_from_preimage(raw):
    values = dict(raw)
    for name in ('query_ref', 'predicate_ref', 'discovery_authority_ref'):
        if values.get(name) is not None:
            values[name] = ExactRef(**values[name])
    for name in ('semantic_roles', 'condition_order'):
        values[name] = tuple(values[name])
    return C.V2ExpectedWorkDeclaration(**values)


@dataclass(frozen=True)
class OriginalExpectedWork:
    original: OriginalIdentity
    legacy: C.V2ExpectedWorkDeclaration
    original_operation_scope_ref: ExactRef
    original_U_ref: ExactRef
    independent_E_ref: ExactRef
    independent_custody_ref: ExactRef

    def __post_init__(self):
        if not isinstance(self.original, OriginalIdentity) or not isinstance(self.legacy, C.V2ExpectedWorkDeclaration):
            raise IdentityError('TYPED_ORIGINAL_AND_LEGACY_REQUIRED')
        if self.legacy.schema_version != C.V2_SCHEMA_VERSION:
            raise IdentityError('LEGACY_SCHEMA_MUST_REMAIN_PUBLISHED_V2')
        if not isinstance(self.legacy.semantic_roles, tuple) or not isinstance(self.legacy.condition_order, tuple):
            raise IdentityError('IMMUTABLE_LEGACY_ROLE_AND_CONDITION_TUPLES_REQUIRED')
        for name in ('source', 'wave', 'item', 'slot', 'target', 'authority_ref', 'risk_identity',
                     'topology_identity', 'required_consumer'):
            if not isinstance(getattr(self.legacy, name), str) or not getattr(self.legacy, name).strip():
                raise IdentityError('LEGACY_BINDING_FIELD_REQUIRED:' + name)
        if self.original.form != self.legacy.form:
            raise IdentityError('ORIGINAL_FORM_BINDING_MISMATCH')
        if self.original.source_release_ref.content_hash != self.legacy.source_identity:
            raise IdentityError('ORIGINAL_SOURCE_BINDING_MISMATCH')
        for name in ('original_operation_scope_ref', 'original_U_ref', 'independent_E_ref', 'independent_custody_ref'):
            _ref(getattr(self, name))
        if len({self.original_U_ref, self.independent_E_ref, self.independent_custody_ref}) != 3:
            raise IdentityError('U_E_CUSTODY_REFS_MUST_BE_DISTINCT')

    def identity_preimage(self):
        d = self.legacy
        # No consumer/state conflation; exact executable refs explicitly bind
        # operation identity, alongside ordered scientific roles and conditions.
        return dict(schema=SCHEMA, kind='ORIGINAL_EXPECTED_WORK', original=self.original.preimage(),
            operation=dict(source=d.source, wave=d.wave, item=d.item, slot=d.slot,
                semantic_op_class=d.semantic_op_class, semantic_roles=list(d.semantic_roles),
                target=d.target, condition_order=list(d.condition_order), measure_kind=d.measure_kind, multiplicity=d.multiplicity,
                authority_ref=d.authority_ref, risk_identity=d.risk_identity, topology_identity=d.topology_identity,
                query_ref=_ref(d.query_ref) if d.query_ref else None,
                predicate_ref=_ref(d.predicate_ref) if d.predicate_ref else None,
                discovery_authority_ref=_ref(d.discovery_authority_ref) if d.discovery_authority_ref else None),
            original_operation_scope_ref=_ref(self.original_operation_scope_ref),
            original_U_ref=_ref(self.original_U_ref), independent_E_ref=_ref(self.independent_E_ref),
            independent_custody_ref=_ref(self.independent_custody_ref))

    @property
    def key(self):
        return semantic_hash(self.identity_preimage())

    def record(self):
        return dict(original=self.original.preimage(), legacy=legacy_preimage(self.legacy),
            original_operation_scope_ref=_ref(self.original_operation_scope_ref),
            original_U_ref=_ref(self.original_U_ref), independent_E_ref=_ref(self.independent_E_ref),
            independent_custody_ref=_ref(self.independent_custody_ref), expected_work_key=self.key)

    @classmethod
    def from_record(cls, raw):
        value = _record_fields(raw, [*(f.name for f in fields(cls)), 'expected_work_key'])
        supplied = value.pop('expected_work_key')
        value['original'] = OriginalIdentity.from_preimage(value['original'])
        value['legacy'] = legacy_from_preimage(value['legacy'])
        for name in ('original_operation_scope_ref', 'original_U_ref', 'independent_E_ref', 'independent_custody_ref'):
            value[name] = ExactRef(**value[name])
        work = cls(**value)
        if supplied != work.key:
            raise IdentityError('ORIGINAL_KEY_PREIMAGE_MISMATCH')
        return work


@dataclass(frozen=True)
class FrozenOriginalExpected:
    payload_json: str
    payload_sha256: str

    @classmethod
    def from_records(cls, records, *, input_origin):
        if input_origin != ORIGIN:
            raise IdentityError('EXPECTED_SET_NOT_INDEPENDENT_SOURCEFREE_INPUT')
        records = tuple(records)
        if not records or not all(isinstance(r, OriginalExpectedWork) for r in records):
            raise IdentityError('EXPECTED_ORIGINAL_RECORDS_REQUIRED')
        raw = canonical_json(dict(schema=SCHEMA, input_origin=input_origin,
            records=[r.record() for r in sorted(records, key=lambda r: r.key)]))
        value = cls(raw, semantic_hash(json.loads(raw)))
        value.checked()
        return value

    def checked(self):
        payload = json.loads(self.payload_json)
        if semantic_hash(payload) != self.payload_sha256:
            raise IdentityError('ORIGINAL_EXPECTATION_DIGEST_MISMATCH')
        _record_fields(payload, ('schema', 'input_origin', 'records'))
        if not isinstance(payload['records'], list):
            raise IdentityError('ORIGINAL_RECORDS_LIST_REQUIRED')
        if payload['schema'] != SCHEMA or payload['input_origin'] != ORIGIN:
            raise IdentityError('ORIGINAL_EXPECTATION_SCHEMA_OR_ORIGIN_MISMATCH')
        works = tuple(OriginalExpectedWork.from_record(r) for r in payload['records'])
        if not works or len({w.key for w in works}) != len(works):
            raise IdentityError('DUPLICATE_OR_EMPTY_ORIGINAL_EXPECTED_KEYS')
        if not any(w.legacy.is_runnable for w in works):
            raise IdentityError('NO_RUNNABLE_ORIGINAL_WORK')
        return works


@dataclass(frozen=True)
class OwnerScopePlan:
    """Selected original keys plus one existing, exact P01 source-free scope."""
    original_work_keys: tuple[str, ...]
    p01_kwargs: Mapping


def _validate_original_against_c11(work, kwargs):
    identity = work.original; session = kwargs['session']
    releases = tuple(session.repository.resolve_release_exact(r) for r in session.identity.release_refs)
    relevant = [r for r in releases if r.source_artifact_ref == identity.source_release_ref]
    if len(relevant) != 1:
        raise IdentityError('ORIGINAL_SOURCE_RELEASE_NOT_EXACT')
    release = relevant[0]
    universe = next((o for o in release.public_objects if o.ref == identity.empirical_universe_ref), None)
    if universe is None or universe.FAMILY != 'EmpiricalUniverse@1.0.0':
        raise IdentityError('ORIGINAL_UNIVERSE_NOT_EXACT')
    if universe.respondent_namespace != identity.respondent_namespace:
        raise IdentityError('ORIGINAL_RESPONDENT_NAMESPACE_MISMATCH')
    if universe.instrument_release != identity.instrument_release:
        raise IdentityError('ORIGINAL_INSTRUMENT_BINDING_MISMATCH')
    routes = {o.ref: o for o in release.public_objects if o.FAMILY == 'RoutingEligibilityFact@1.0.0'}
    if not set(identity.routing_refs) <= set(routes):
        raise IdentityError('ORIGINAL_ROUTING_NOT_EXACT')
    if any(exact_ref(routes[r].empirical_universe_ref) != identity.empirical_universe_ref for r in identity.routing_refs):
        raise IdentityError('ORIGINAL_ROUTING_UNIVERSE_MISMATCH')
    items = {exact_ref(o.native_question_ref) for o in release.public_objects if o.FAMILY == 'RespondentEvent@1.0.0'
             and exact_ref(o.empirical_universe_ref) == identity.empirical_universe_ref}
    if not set(identity.native_item_refs) <= items:
        raise IdentityError('ORIGINAL_NATIVE_ITEM_NOT_EXACT')
    catalog = kwargs['runtime_catalog']
    route_risks = {exact_ref(routes[r].risk_set_ref) for r in identity.routing_refs}
    if work.legacy.query_ref is not None:
        query = catalog.resolve_query_exact(work.legacy.query_ref)
        if tuple(exact_ref(r) for r in query.target_refs) != identity.native_item_refs:
            raise IdentityError('ORIGINAL_ORDERED_ITEM_QUERY_BINDING_MISMATCH')
        if identity.empirical_universe_ref not in {exact_ref(r) for r in query.empirical_universe_refs}:
            raise IdentityError('ORIGINAL_QUERY_UNIVERSE_MISMATCH')
        if route_risks != {exact_ref(query.risk_set_ref)}:
            raise IdentityError('ORIGINAL_QUERY_ROUTING_RISK_MISMATCH')
    else:
        discovery = catalog.resolve_discovery_authority_exact(work.legacy.discovery_authority_ref)
        if identity.empirical_universe_ref not in {exact_ref(r) for r in
                discovery.source_universe_scope['allowed_universe_refs']}:
            raise IdentityError('ORIGINAL_DISCOVERY_UNIVERSE_MISMATCH')
        if not route_risks <= {exact_ref(r) for r in discovery.risk_set_scope['allowed_risk_set_refs']}:
            raise IdentityError('ORIGINAL_DISCOVERY_ROUTING_RISK_MISMATCH')


def run_sourcefree(*, expected, selected_scopes, prior_consumer_refs=None):
    """Outer original-E reconciliation BEFORE all actual owner durable calls.

    Multiple actual C11 scopes may alias old V2 keys. Translation is explicit
    (original key, universe, legacy key, unit, result, consumer); no coercion or
    legacy key concatenation. Original input/custody authenticity stays HELD.
    """
    works = expected.checked(); by_key = {w.key: w for w in works}
    runnable = {w.key for w in works if w.legacy.is_runnable}
    scopes = tuple(selected_scopes)
    selected = [key for scope in scopes for key in scope.original_work_keys]
    if len(set(selected)) != len(selected):
        raise IdentityError('DUPLICATE_ORIGINAL_SELECTED_WORK')
    if set(selected) != runnable:
        raise IdentityError('ORIGINAL_EXPECTED_SELECTED_ANTI_JOIN:' + canonical_json(
            dict(missing=sorted(runnable-set(selected)), extra=sorted(set(selected)-runnable))))
    if prior_consumer_refs is not None and set(prior_consumer_refs) != runnable:
        raise IdentityError('ORIGINAL_REPLAY_CONSUMER_KEY_SET_MISMATCH')
    # Validate every scope before executing even the first scope.
    owner_units = set()
    for scope in scopes:
        kwargs = scope.p01_kwargs
        if tuple(kwargs['producer_permission_ceiling']) != ('SOURCE_FREE_DEV',):
            raise IdentityError('SOURCEFREE_ONLY_NO_REAL_EXECUTION')
        kwargs['expected'].checked()
        rows = json.loads(kwargs['expected'].payload_json)['declarations']
        rows = {C.V2ExpectedWorkDeclaration(**{
            k: ExactRef(**v) if k in ('query_ref','predicate_ref','discovery_authority_ref') and v else
            tuple(v) if k in ('semantic_roles','condition_order') else v for k,v in r.items()}).expected_work_key: r
            for r in rows if r.get('state','RUNNABLE') == 'RUNNABLE'}
        selected_works = [by_key[k] for k in scope.original_work_keys]
        if len({w.legacy.expected_work_key for w in selected_works}) != len(selected_works):
            raise IdentityError('LEGACY_ALIAS_WITHIN_ONE_OWNER_SCOPE')
        if set(rows) != {w.legacy.expected_work_key for w in selected_works}:
            raise IdentityError('P01_EXPECTED_ORIGINAL_BINDING_ANTI_JOIN')
        for work in selected_works:
            if legacy_from_preimage(rows[work.legacy.expected_work_key]) != work.legacy:
                raise IdentityError('P01_DECLARATION_ORIGINAL_BINDING_MISMATCH')
            _validate_original_against_c11(work, kwargs)
            job_ref = work.legacy.query_ref or work.legacy.discovery_authority_ref
            if len([u for u in kwargs['session'].manifest.units if u.job_ref == job_ref]) != 1:
                raise IdentityError('ORIGINAL_OWNER_BATCH_JOB_NOT_EXACT')
            unit = next(u for u in kwargs['session'].manifest.units if u.job_ref == job_ref)
            if unit.unit_ref in owner_units:
                raise IdentityError('ORIGINAL_MULTI_IDENTITY_TO_ONE_OWNER_UNIT_NOT_GOVERNED')
            owner_units.add(unit.unit_ref)
    links = []; owner_reports = []
    for scope in scopes:
        kwargs = dict(scope.p01_kwargs)
        if prior_consumer_refs is not None:
            kwargs['prior_consumer_refs'] = {by_key[k].legacy.expected_work_key: prior_consumer_refs[k]
                                            for k in scope.original_work_keys}
        report = P.run_integrated(**kwargs); owner_reports.append(report)
        products = {p['expected_work_key']: p for p in report['consumer_products']}
        for key in scope.original_work_keys:
            work = by_key[key]; product = products.get(work.legacy.expected_work_key)
            if product is not None:
                unit = next(u for u in kwargs['session'].manifest.units
                    if u.job_ref == (work.legacy.query_ref or work.legacy.discovery_authority_ref))
                links.append(dict(original_expected_work_key=key, original_identity=work.identity_preimage(),
                    legacy_expected_work_key=work.legacy.expected_work_key,
                    owner_job_ref=_ref(unit.job_ref), batch_unit_ref=_ref(unit.unit_ref),
                    c11_release_refs=[_ref(r) for r in unit.release_refs],
                    empirical_universe_ref=_ref(work.original.empirical_universe_ref),
                    producer_result_ref=product['result_ref'], consumer_ref=product['consumer_ref'],
                    consumer_material=product['consumer_material']))
    consumed = {l['original_expected_work_key'] for l in links}
    return dict(schema=SCHEMA, claim_grade='SOURCEFREE_SUCCESSOR_CANDIDATE_NOT_ADOPTED',
        ok=all(r['ok'] for r in owner_reports) and consumed == runnable,
        original_expected_digest=expected.payload_sha256, links=sorted(links,key=lambda l:l['original_expected_work_key']),
        nonrunnable=[w.record() for w in works if not w.legacy.is_runnable],
        missing_consumers=sorted(runnable-consumed), owner_reports=owner_reports,
        holds=['ORIGINAL_U_E_CUSTODY_NOT_AUTHENTICATED','SOURCE_USE_NOT_GRANTED','SEMANTIC_OWNER_ADOPTION_NOT_GRANTED'])
