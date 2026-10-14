"""HQ297 V2R: UNADOPTED TEST_ONLY original role↔query binding boundary.

Exact hashes prove integrity, never original U/O3/E_pre competence. Existing
V2K/P01 and owner code remain unchanged. No real-source entrypoint exists.
"""
from collections import Counter
from dataclasses import dataclass, replace
import hashlib,json
from rawlsing_next import pre553_original_identity_v2k_successor_candidate as K
from rawlsing_next.pre553_empirical_objects import exact_ref, semantic_hash

SCHEMA='HQ297_V2R_SOURCE_NATIVE_ROLE_QUERY_BINDING_CANDIDATE@1.0.0'
REGISTER_SCHEMA='HQ297_V2R_INDEPENDENT_TEST_ONLY_REGISTER@1.0.0'


class RoleBindingError(ValueError):
    """Typed binding refusal; does not issue or authenticate source semantics."""


def _canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)


def _fields(value,names,code):
    if not isinstance(value,dict) or set(value)!=set(names):raise RoleBindingError(code)


def _ref(raw):
    try:return exact_ref(raw)
    except ValueError as e:raise RoleBindingError('EXACT_SOURCE_NATIVE_REF_REQUIRED') from e


@dataclass(frozen=True)
class FrozenSourceNativeRegister:
    """Prospective separately supplied TEST_ONLY roster, not a trust root.

    Completeness is proved only RELATIVE TO this register. Real issuer identity,
    independent custody and pre-result chronology require outside competence.
    A coherent caller refreeze can describe another hypothetical roster; it
    cannot receive original-source qualification from this class.
    """
    payload_json:str
    payload_sha256:str

    @classmethod
    def from_payload(cls,payload):
        text=_canonical(payload)
        result=cls(text,hashlib.sha256(text.encode()).hexdigest());result.checked();return result

    def checked(self):
        if hashlib.sha256(self.payload_json.encode()).hexdigest()!=self.payload_sha256:
            raise RoleBindingError('REGISTER_DIGEST_MISMATCH')
        payload=json.loads(self.payload_json)
        _fields(payload,('schema','origin','competence','records'),'REGISTER_FIELDS_MISSING_OR_UNKNOWN')
        if (payload['schema']!=REGISTER_SCHEMA or payload['origin']!='PROSPECTIVE_INDEPENDENT_TEST_ONLY'
            or payload['competence']!='TEST_ONLY_NOT_SOURCE_QUALIFIED'):
            raise RoleBindingError('CANNOT_QUALIFY_ORIGINAL:INDEPENDENT_U_O3_E_PRE_COMPETENCE_UNAVAILABLE')
        if not isinstance(payload['records'],list) or not payload['records']:
            raise RoleBindingError('COMPLETE_ORIGINAL_REGISTER_REQUIRED')
        keys=[]
        for row in payload['records']:
            _fields(row,('record','binding'),'REGISTER_ROW_FIELDS_MISSING_OR_UNKNOWN')
            work=K.OriginalExpectedWork.from_record(row['record']);keys.append(work.key)
            _fields(row['binding'],('native_order','risk_ref','raw_denominator','profile'),'QUERY_BINDING_FIELDS_MISSING_OR_UNKNOWN')
            native=row['binding']['native_order']
            if not isinstance(native,list) or not native:raise RoleBindingError('NATIVE_ROLE_ORDER_REQUIRED')
            for r in native:_ref(r)
            _ref(row['binding']['risk_ref'])
            denominator=row['binding']['raw_denominator']
            if work.legacy.is_runnable and (not isinstance(denominator,int) or isinstance(denominator,bool) or denominator<0):
                raise RoleBindingError('RAW_DENOMINATOR_WITNESS_REQUIRED')
            if not work.legacy.is_runnable and denominator is not None:
                raise RoleBindingError('HELD_WORK_DENOMINATOR_MUST_REMAIN_UNISSUED')
            if work.legacy.is_runnable and not isinstance(row['binding']['profile'],dict):
                raise RoleBindingError('CONDITIONAL_SUPPORT_WITNESS_REQUIRED')
        if len(set(keys))!=len(keys):raise RoleBindingError('DUPLICATE_ORIGINAL_REGISTER_KEY_NOT_GOVERNED')
        return payload['records']


def _check_query(query,work,binding,*,direct):
    if semantic_hash(query.semantic_projection())!=query.content_hash:
        raise RoleBindingError('QUERY_OBJECT_PREIMAGE_MISMATCH')
    if tuple(_ref(r) for r in query.target_refs)!=tuple(_ref(r) for r in binding['native_order']):
        raise RoleBindingError('ROLE_QUERY_SEMANTIC_MISMATCH:NATIVE_PARTICIPANT_ORDER')
    if {_ref(r) for r in query.empirical_universe_refs}!={work.original.empirical_universe_ref}:
        raise RoleBindingError('ROLE_QUERY_UNIVERSE_MISMATCH')
    if _ref(query.risk_set_ref)!=_ref(binding['risk_ref']):raise RoleBindingError('ROLE_QUERY_RISK_MISMATCH')
    if direct and (query.ref!=work.legacy.query_ref or _ref(query.condition_predicate_ref)!=work.legacy.predicate_ref):
        raise RoleBindingError('ROLE_QUERY_PREDICATE_OR_EXACT_QUERY_MISMATCH')


def _check_fact(fact,query,work,binding):
    _check_query(query,work,binding,direct=work.legacy.query_ref is not None)
    if semantic_hash(fact.semantic_projection())!=fact.content_hash:
        raise RoleBindingError('SAVED_FACT_OBJECT_PREIMAGE_MISMATCH')
    if _ref(fact.empirical_query_spec_ref)!=query.ref or _ref(fact.condition_predicate_ref)!=_ref(query.condition_predicate_ref):
        raise RoleBindingError('SAVED_FACT_ACTUAL_QUERY_MISMATCH')
    if {_ref(r) for r in fact.empirical_universe_refs}!={work.original.empirical_universe_ref}:
        raise RoleBindingError('SAVED_FACT_UNIVERSE_MISMATCH')
    if _ref(fact.risk_set_ref)!=_ref(binding['risk_ref']):raise RoleBindingError('SAVED_FACT_RISK_MISMATCH')
    if fact.raw_denominator_support!=binding['raw_denominator']:
        raise RoleBindingError('SAVED_FACT_RAW_DENOMINATOR_MISMATCH')
    if fact.weighted_denominator_support_if_authorized is not None:
        raise RoleBindingError('RAW_ROLE_BINDING_CANNOT_AUTHORIZE_WEIGHTED_DENOMINATOR')


def _validated_scope(scope,by_key):
    catalog=scope.p01_kwargs['runtime_catalog']
    direct={};discovery={}
    for key in scope.original_work_keys:
        if key not in by_key:raise RoleBindingError('SELECTED_ORIGINAL_KEY_NOT_REGISTERED')
        row=by_key[key];work=K.OriginalExpectedWork.from_record(row['record']);d=work.legacy;b=row['binding']
        if tuple(_ref(r) for r in b['native_order'])!=work.original.native_item_refs:
            raise RoleBindingError('ROLE_QUERY_SEMANTIC_MISMATCH:ORIGINAL_NATIVE_ORDER')
        if d.measure_kind!='RAW' or d.multiplicity!=1:raise RoleBindingError('ROLE_QUERY_MEASURE_OR_MULTIPLICITY_UNSUPPORTED')
        if d.risk_identity!=_ref(b['risk_ref']).key:raise RoleBindingError('DECLARED_NATIVE_RISK_MISMATCH')
        if d.query_ref is not None:
            if d.semantic_roles!=('CONDITIONER','TARGET') or len(b['native_order'])!=2:
                raise RoleBindingError('ROLE_QUERY_SEMANTIC_MISMATCH:DECLARED_ROLE_MASK')
            query=catalog.resolve_query_exact(d.query_ref);_check_query(query,work,b,direct=True)
            direct[query.ref.key]=(work,b,query)
        else:
            if d.semantic_roles!=('BASE',) or len(b['native_order'])!=2:
                raise RoleBindingError('ROLE_QUERY_SEMANTIC_MISMATCH:BOUNDED_DISCOVERY_BASE')
            authority=catalog.resolve_discovery_authority_exact(d.discovery_authority_ref)
            if semantic_hash(authority.semantic_projection())!=authority.content_hash:
                raise RoleBindingError('DISCOVERY_AUTHORITY_PREIMAGE_MISMATCH')
            if work.original.empirical_universe_ref not in {_ref(r) for r in authority.source_universe_scope['allowed_universe_refs']}:
                raise RoleBindingError('DISCOVERY_SOURCE_UNIVERSE_MISMATCH')
            if _ref(b['risk_ref']) not in {_ref(r) for r in authority.risk_set_scope['allowed_risk_set_refs']}:
                raise RoleBindingError('DISCOVERY_NATIVE_RISK_MISMATCH')
            discovery[authority.ref.key]=(work,b)
    kwargs=dict(scope.p01_kwargs);resolve=kwargs['resolve_fact'];resolve_discovery=kwargs.get('resolve_discovery')
    def resolve_checked(ref):
        fact=resolve(ref);signature=direct.get(_ref(fact.empirical_query_spec_ref).key)
        if signature is None:raise RoleBindingError('UNREGISTERED_SAVED_FACT_QUERY')
        _check_fact(fact,signature[2],signature[0],signature[1]);return fact
    def discovery_checked(ref):
        result=resolve_discovery(ref);signature=discovery.get(result.discovery_authority_ref.key)
        if signature is None:raise RoleBindingError('UNREGISTERED_DISCOVERY_RESULT')
        work,b=signature
        queries={q.ref:q for q in result.executed_queries}
        # Every bounded derived query keeps original source-native target order,
        # universe and risk. Only winner facts have the independent winner support.
        for q in result.executed_queries:_check_query(q,work,b,direct=False)
        for receipt in result.receipts:
            if receipt.typed_state!='DISCOVERED_RESULT_SUPPORTED':continue
            winning=_ref(receipt.winning_predicate_ref)
            declared={_ref(r) for r in receipt.empirical_fact_refs}
            for fact in result.empirical_facts:
                if fact.ref in declared and _ref(fact.condition_predicate_ref)==winning:
                    query=queries.get(_ref(fact.empirical_query_spec_ref))
                    if query is None:raise RoleBindingError('UNREGISTERED_DISCOVERY_WINNER_QUERY')
                    _check_fact(fact,query,work,b)
        return result
    kwargs['resolve_fact']=resolve_checked
    if discovery:kwargs['resolve_discovery']=discovery_checked
    return replace(scope,p01_kwargs=kwargs)


def run_sourcefree(*,expected,selected_scopes,register,prior_consumer_refs=None):
    """Bind independent TEST_ONLY original roster to actual unmodified owners.

    Pre-effect: full original-record multiset, role/native/query/risk/universe
    and existing C11 routing checks. Saved-fact risk/denominator checks occur
    after durable commit, before Field Forge consumption. Consumer profile
    checks occur after values-read; no rollback/external atomicity is claimed.
    """
    if not isinstance(register,FrozenSourceNativeRegister):
        raise RoleBindingError('CANNOT_QUALIFY_ORIGINAL:INDEPENDENT_REGISTER_REQUIRED')
    rows=register.checked();works=expected.checked()
    if Counter(_canonical(w.record()) for w in works)!=Counter(_canonical(r['record']) for r in rows):
        raise RoleBindingError('ORIGINAL_REGISTER_MULTISET_MISMATCH')
    by_key={r['record']['expected_work_key']:r for r in rows}
    scopes=tuple(_validated_scope(s,by_key) for s in selected_scopes)
    report=K.run_sourcefree(expected=expected,selected_scopes=scopes,prior_consumer_refs=prior_consumer_refs)
    for link in report['links']:
        row=by_key[link['original_expected_work_key']];work=K.OriginalExpectedWork.from_record(row['record']);binding=row['binding'];mat=link['consumer_material']
        if mat['roles']['CONDITIONER']['ref']!=binding['native_order'][0] or mat['roles']['TARGET']['ref']!=binding['native_order'][1]:
            raise RoleBindingError('ACTUAL_CONSUMER_ROLE_QUERY_MISMATCH')
        if _ref(mat['risk_set_ref'])!=_ref(binding['risk_ref']):raise RoleBindingError('ACTUAL_CONSUMER_RISK_MISMATCH')
        if {_ref(r) for r in mat['empirical_universe_refs']}!={work.original.empirical_universe_ref}:
            raise RoleBindingError('ACTUAL_CONSUMER_UNIVERSE_MISMATCH')
        if mat['producer_fact_ref']!=link['producer_result_ref'] or (work.legacy.query_ref is not None and _ref(mat['producer_query_ref'])!=work.legacy.query_ref):
            raise RoleBindingError('ACTUAL_CONSUMER_SAVED_FACT_QUERY_MISMATCH')
        profile={str(r['condition_state']):dict(denominator=r['condition_denominator_support'],targets={str(t['target_state']):t['joint_support_count'] for t in r['target_counts']}) for r in mat['conditional_count_profile']}
        if profile!=binding['profile']:raise RoleBindingError('ACTUAL_CONSUMER_PROFILE_DENOMINATOR_MISMATCH')
    if Counter(_canonical(w.record()) for w in works if not w.legacy.is_runnable)!=Counter(_canonical(r) for r in report['nonrunnable']):
        raise RoleBindingError('ORIGINAL_NONRUNNABLE_MULTISET_LOST')
    return {**report,'schema':SCHEMA,'legacy_schema':K.SCHEMA,'claim_grade':'TEST_ONLY_VERSIONED_ROLE_BINDING_UNADOPTED',
        'register_digest':register.payload_sha256,'original_qualification':'CANNOT_QUALIFY_ORIGINAL',
        'competence_holds':['ORIGINAL_U_O3_E_PRE_ISSUANCE_NOT_AUTHENTICATED','EXTERNAL_CUSTODY_AND_PROSPECTIVE_CHRONOLOGY_NOT_AUTHENTICATED','SOURCE_USE_NOT_GRANTED','INDEPENDENT_SEMANTIC_ADOPTION_NOT_GRANTED'],
        'values_read':'ACTUAL_SAVED_FACT_AND_FIELD_FORGE_CONDITIONAL_SUPPORT',
        'native_variable_label_grade':'RETAINED_GT2_LABELS_NOT_GENERIC_NATIVE_SOURCE_AUTHORITY'}
