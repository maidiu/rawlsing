"""PRE553 native issued-workload binding (B49 T4).

Binds a source-native projection (T2) plus an explicitly TEST_ONLY synthetic
operation fixture to the existing U43 ``NativeWorkload`` / Route B / C11 /
Batch / I03 owners. The resolver record is TEST_ONLY and is never a current
original-issuer grant; prospective original E_pre stays NULL.

This module adds no new manifest engine, batch factory or discovery generator.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner,
    BatchManifest,
    BatchUnitSpec,
    ExecutionOutcome,
    ExecutorBinding,
)
from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_carrier_execution import (
    CarrierNeutralResearchExecutor, RuntimeObjectCatalog,
)
from rawlsing_next.pre553_discovery_exact import (
    COVERAGE_CLAIM, I05_CONTRACT_ID,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    DiscoveryAuthority,
    EmpiricalQuerySpec,
    ExactRef,
    RespondentEvent,
    exact_ref,
    make_empirical_predicate,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_authority import require_positive_authority
from rawlsing_next.pre553_issued_workload import (
    IssuedWorkloadRecord,
    NativeWorkload,
    NativeWorkloadResult,
    admit,
    execute_issued_workload,
)
from rawlsing_next.pre553_route_b_production import I03ExecutionRequest
from rawlsing_next.pre553_source_backed_c11_facade import (
    GovernedC11Projection, build_source_backed_c11_repository,
)
from rawlsing_next.pre553_source_native_preimage_adapter import NativePreimageBundle
from rawlsing_next.universal_grammar.native_map import NativeCatalog
from rawlsing_next.universal_grammar.types import (
    OccurrenceKey, SourceInventory, typed_value_key,
)

SCHEMA = "PRE553_TEST_ONLY_NATIVE_WORKLOAD_BINDING@1.0.0"
TEST_ONLY_SCOPE = "TEST_ONLY_SOURCEFREE"

DESCRIPTOR_FIELDS = frozenset({
    "source_edition", "native_item_ids", "release_tag", "routing_and_risk",
    "carrier", "country_and_population", "weight_design_estimand",
    "missing_and_occurrence_policy", "target_conditioner_roles",
})


class WorkloadBindingRefusal(ValueError):
    """A test-only native workload could not be bound without inventing authority."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _hash(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode()).hexdigest()


def _ref(kind: str, tag: str, material: Any = None) -> ExactRef:
    return ExactRef(kind, f"urn:rawlsing:b49:{kind.lower()}:{tag}",
                    _hash({"kind": kind, "tag": tag, "material": material}))


@dataclass(frozen=True)
class OperationFixture:
    """One explicit TEST_ONLY operation fixture supplied by the caller.

    The fixture names the exact target variable and response value for a
    single-target presence query. It is not a scientific E_pre decision.
    """

    fixture_id: str
    target_variable_code: str
    response_value: str
    measure_kind: str = "RAW"

    def __post_init__(self) -> None:
        if not self.target_variable_code.strip():
            raise WorkloadBindingRefusal("FIXTURE_TARGET_REQUIRED")
        if self.measure_kind not in ("RAW", "GOVERNED_WEIGHTED"):
            raise WorkloadBindingRefusal("FIXTURE_MEASURE_UNSUPPORTED", self.measure_kind)


def _event_order_key(event: RespondentEvent) -> tuple[Any, ...]:
    fields = event.multiplicity_order_rank_fields
    if isinstance(fields, Mapping):
        for name in ("semantic_ordinal", "semantic_order", "semantic_order_key",
                     "ordinal", "order", "rank", "index", "multiplicity_index"):
            if name in fields:
                value = fields[name]
                if isinstance(value, int) and not isinstance(value, bool):
                    return (0, value, event.ref.key)
                if isinstance(value, str):
                    return (1, value, event.ref.key)
    return (2, event.ref.key)


def _event_value(event: RespondentEvent) -> Any:
    if event.typed_state == "SUBSTANTIVE_RESPONSE":
        return event.canonical_response_value_if_authorized
    return {"typed_response_state": event.typed_state}


def native_target_configuration(
    *,
    bundle: NativePreimageBundle,
    target_ref: ExactRef,
    included_states: tuple[str, ...] = ("SUBSTANTIVE_RESPONSE",),
) -> tuple[str, tuple[Any, ...]]:
    """Derive exact target topology/domain from the materialized native release."""
    projection = bundle.projection
    respondent_by_ref = {respondent.ref.key: respondent.respondent_key
                         for respondent in projection.respondents}
    grouped: dict[str, list[RespondentEvent]] = {}
    for obj in bundle.release.public_objects:
        if not isinstance(obj, RespondentEvent):
            continue
        if exact_ref(obj.native_question_ref) != target_ref:
            continue
        if obj.typed_state not in included_states:
            continue
        respondent_ref = exact_ref(obj.scoped_respondent_ref)
        respondent_key = respondent_by_ref.get(respondent_ref.key)
        if respondent_key is None:
            raise WorkloadBindingRefusal("TARGET_RESPONDENT_NOT_IN_PROJECTION")
        grouped.setdefault(respondent_key, []).append(obj)
    if not grouped:
        raise WorkloadBindingRefusal("NO_NATIVE_TARGET_EVENTS")
    topologies = {str(event.multiplicity_order_rank_fields.get("kind") or
                      event.multiplicity_order_rank_fields.get("topology_kind"))
                  for events in grouped.values() for event in events}
    topologies.discard("None")
    if len(topologies) != 1:
        raise WorkloadBindingRefusal("MIXED_NATIVE_TARGET_TOPOLOGY", repr(sorted(topologies)))
    topology = next(iter(topologies))
    ordered = {
        key: sorted(events, key=_event_order_key)
        for key, events in grouped.items()
    }
    if topology in {"REPEATED_EVENT", "REPEATED_MEASUREMENT"}:
        domain = tuple(
            [{
                "event_id": event.response_event_id_or_deterministic_index,
                "multiplicity_order_rank_fields": dict(event.multiplicity_order_rank_fields),
                "value": _event_value(event),
            } for event in ordered[key]]
            for key in sorted(ordered)
        )
    elif topology in {"ORDERED_SEQUENCE", "RANKED_RESPONSE"}:
        domain = tuple([_event_value(event) for event in ordered[key]]
                       for key in sorted(ordered))
    elif topology in {"UNORDERED_MULTISELECT_SET", "UNORDERED_MULTISELECT", "MULTISELECT"}:
        domain = tuple(sorted(
            ([_event_value(event) for event in ordered[key]] for key in sorted(ordered)),
            key=lambda values: json.dumps(values, sort_keys=True)))
    elif topology == "COMPONENTIZED_RESPONSE":
        domain = tuple(
            [{
                "component_or_subitem_ref": exact_ref(event.component_or_subitem_ref).as_dict()
                if event.component_or_subitem_ref is not None else None,
                "value": _event_value(event),
            } for event in ordered[key]]
            for key in sorted(ordered)
        )
    elif topology in {"SCALAR_SINGULAR", "ROUTED_RESPONSE"}:
        domain = tuple(sorted({_event_value(event) for events in ordered.values()
                               for event in events}, key=lambda value: json.dumps(value, sort_keys=True)))
    else:
        raise WorkloadBindingRefusal("UNSUPPORTED_NATIVE_TARGET_TOPOLOGY", topology)
    return topology, domain


_QUERY_SCOPE_FIELDS = frozenset({
    "source_universe_refs", "target_use_refs", "predicate_or_risk_set_refs",
    "source_sha256", "grade", "as_of", "measure", "measure_kind",
    "measure_kinds", "grammar", "frontier",
})


def _exact_external_query_authority(
    *, authority: AuthoritySnapshot, bundle: NativePreimageBundle, as_of: str,
    expected_measure_kinds: tuple[str, ...] | None = None,
) -> str:
    if not isinstance(authority, AuthoritySnapshot):
        raise WorkloadBindingRefusal("SUPPLIED_QUERY_AUTHORITY_REQUIRED")
    if (authority.typed_state != "ALLOW" or authority.decision_state != "ALLOW"
            or authority.authority_kind != "PREDICATE_GRAMMAR"):
        raise WorkloadBindingRefusal("SUPPLIED_QUERY_AUTHORITY_NOT_POSITIVE")
    scope = authority.scope_envelope
    if not isinstance(scope, Mapping):
        raise WorkloadBindingRefusal("SUPPLIED_QUERY_AUTHORITY_SCOPE_REQUIRED")
    unsupported = set(scope) - _QUERY_SCOPE_FIELDS
    if unsupported:
        raise WorkloadBindingRefusal(
            "SUPPLIED_QUERY_AUTHORITY_UNSUPPORTED_SCOPE_FIELD", repr(sorted(unsupported)))
    for unsupported_constraint in ("grammar", "frontier"):
        if unsupported_constraint in scope:
            raise WorkloadBindingRefusal(
                "SUPPLIED_QUERY_AUTHORITY_UNSUPPORTED_CONSTRAINT", unsupported_constraint)
    target_use = scope.get("target_use_refs")
    if target_use is not None and target_use != "EXPLICIT_UNRESTRICTED":
        raise WorkloadBindingRefusal("SUPPLIED_QUERY_AUTHORITY_TARGET_USE_MISMATCH")
    declared_as_of = scope.get("as_of")
    if declared_as_of is not None and declared_as_of != as_of:
        raise WorkloadBindingRefusal("SUPPLIED_QUERY_AUTHORITY_AS_OF_MISMATCH")
    if expected_measure_kinds is not None:
        raw_measure = scope.get("measure")
        if raw_measure is None:
            raw_measure = scope.get("measure_kind")
        if raw_measure is None:
            raw_measure = scope.get("measure_kinds")
        if raw_measure is not None:
            if isinstance(raw_measure, str):
                supplied_measures = {raw_measure}
            elif isinstance(raw_measure, Sequence) and not isinstance(raw_measure, (bytes, bytearray)):
                supplied_measures = {str(value) for value in raw_measure}
            else:
                raise WorkloadBindingRefusal("SUPPLIED_QUERY_AUTHORITY_MEASURE_UNSUPPORTED")
            if not supplied_measures <= set(expected_measure_kinds):
                raise WorkloadBindingRefusal("SUPPLIED_QUERY_AUTHORITY_MEASURE_MISMATCH")
    if scope.get("source_sha256") != bundle.source_sha256:
        raise WorkloadBindingRefusal("SUPPLIED_QUERY_AUTHORITY_SOURCE_MISMATCH")
    universe_raw = scope.get("source_universe_refs")
    risk_raw = scope.get("predicate_or_risk_set_refs")
    if (isinstance(universe_raw, (str, bytes)) or not isinstance(universe_raw, Sequence)
            or isinstance(risk_raw, (str, bytes)) or not isinstance(risk_raw, Sequence)):
        raise WorkloadBindingRefusal("SUPPLIED_QUERY_AUTHORITY_EXACT_SCOPE_REQUIRED")
    declared_universes = tuple(sorted(
        (exact_ref(value, "query_authority.scope.source_universe_refs") for value in universe_raw),
        key=lambda ref: ref.key))
    expected_universes = tuple(sorted(
        (universe.ref for universe in bundle.projection.universes), key=lambda ref: ref.key))
    if declared_universes != expected_universes:
        raise WorkloadBindingRefusal("SUPPLIED_QUERY_AUTHORITY_UNIVERSE_MISMATCH")
    declared_risks = tuple(sorted(
        (exact_ref(value, "query_authority.scope.predicate_or_risk_set_refs") for value in risk_raw),
        key=lambda ref: ref.key))
    if declared_risks != (bundle.risk_set_ref,):
        raise WorkloadBindingRefusal("SUPPLIED_QUERY_AUTHORITY_RISK_MISMATCH")
    operations = tuple(authority.governed_operations)
    if len(operations) != 1 or not isinstance(operations[0], str) or not operations[0].strip():
        raise WorkloadBindingRefusal("SUPPLIED_QUERY_AUTHORITY_OPERATION_NOT_EXACT")
    operation = operations[0].strip()
    for family in ("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"):
        for universe_ref in expected_universes:
            require_positive_authority(
                authority, authority_kind="PREDICATE_GRAMMAR", operation=operation,
                object_family=family, source_universe_ref=universe_ref.as_dict(),
                predicate_or_risk_set_ref=bundle.risk_set_ref.as_dict(),
            )
    return operation


def build_projection_catalog(
    *,
    bundle: NativePreimageBundle,
    operation: OperationFixture,
    as_of: str,
    query_authority: AuthoritySnapshot | None = None,
) -> tuple[RuntimeObjectCatalog, I03ExecutionRequest]:
    """Build the exact RuntimeObjectCatalog for one TEST_ONLY query operation.

    Reuses the existing predicate/query/catalog owners. Refuses when the
    fixture target is not an administered item of the projection.
    """
    projection = bundle.projection
    target_ref = bundle.question_refs.get(operation.target_variable_code)
    target = next(
        (q for q in projection.questions if q.native_question_ref == target_ref),
        None,
    ) if target_ref is not None else None
    if target is None:
        raise WorkloadBindingRefusal(
            "FIXTURE_TARGET_NOT_ADMINISTERED", operation.target_variable_code
        )
    projection_auth = next(
        a for a in bundle.projection.authority_snapshots if a.authority_kind == "SOURCE_SEMANTICS_TOPOLOGY"
        and "RespondentEvent@1.0.0" in a.governed_object_families
        and "EmpiricalCoordinateFact@1.0.0" in a.governed_object_families
    )
    query_operation: str | None = None
    if query_authority is None:
        query_auth_digest = _hash({
            "tag": "b49-query", "source_sha256": bundle.source_sha256, "as_of": as_of,
        })
        query_auth = AuthoritySnapshot(
            typed_state="ALLOW",
            authority_snapshot_refs=(),
            dependency_refs=(),
            producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "query-authority"),
            authority_id="B49-TEST-ONLY-QUERY-AUTH",
            authority_version="1.0.0",
            authority_content_hash=query_auth_digest,
            authority_kind="PREDICATE_GRAMMAR",
            decision_state="ALLOW",
            governed_operations=("B49-OP-query",),
            governed_object_families=(
                "EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0",
            ),
            scope_envelope={
                "source_universe_refs": "EXPLICIT_UNRESTRICTED",
                "target_use_refs": "EXPLICIT_UNRESTRICTED",
                "predicate_or_risk_set_refs": "EXPLICIT_UNRESTRICTED",
                "source_sha256": bundle.source_sha256,
                "as_of": as_of,
                "grade": "TEST_ONLY_SOURCEFREE",
            },
            effective_time_or_interval=as_of,
            parent_authority_refs=(),
            negative_limit_refs=(),
            supersession_refs=(),
            interpretation_semantics_fingerprint=_hash({"tag": "b49-query", "as_of": as_of}),
            replay_protocol_ref=_ref("REPLAY_PROTOCOL", "query-authority"),
        )
    else:
        query_operation = _exact_external_query_authority(
            authority=query_authority, bundle=bundle, as_of=as_of,
            expected_measure_kinds=(operation.measure_kind,),
        )
        query_auth = query_authority
    universe = projection.universes[0]
    members = tuple(sorted((r.ref for r in projection.respondents), key=lambda r: r.key))
    membership = _ref(
        "BRANCH_MEMBERSHIP",
        f"b49-all-{_hash([m.key for m in members])[:12]}",
    )
    branch_ast = {
        "op": "LEAF",
        "leaf_type": "DERIVED_BRANCH_COHORT",
        "branch_definition_id": "BRANCH-b49-all",
        "resolved_predicate_hash_or_exact_membership_ref": membership,
        "parent_ancestry_ref": _ref("BRANCH_PARENT", "b49-all"),
        "branch_algorithm_authority_ref": query_auth.authority_ref,
        "branch_membership_replay_ref": _ref("BRANCH_REPLAY", "b49-all"),
        "branch_source_scope_ref": universe.ref,
        "exact_member_respondent_refs": members,
    }
    branch = make_empirical_predicate(
        predicate_ast=branch_ast,
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(query_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "predicate-b49-all"),
        grammar_authority_ref=query_auth.authority_ref,
        coordinate_question_value_refs=(),
        risk_set_refs=(),
        scope_refs=(universe.ref,),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(_ref("OPERATOR_SEMANTICS", "BOOLEAN-AND-OR-NOT"),),
    )
    response_ast = {
        "op": "LEAF",
        "leaf_type": "SURVEY_RESPONSE_EVENT",
        "question_semantic_ref": target.native_question_ref,
        "component_or_event_selector_ref": _ref(
            "EVENT_SELECTOR", f"{operation.target_variable_code}-ANY"
        ),
        "response_value_or_state_ref": _ref(
            "VALUE_REF", f"{operation.target_variable_code}-{operation.response_value}"
        ),
        "response_topology_authority_ref": projection_auth.authority_ref,
        "response_semantic_authority_ref": projection_auth.authority_ref,
        "operator": "EQ",
        "exact_value": str(operation.response_value),
    }
    response_predicate = make_empirical_predicate(
        predicate_ast=response_ast,
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(query_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref(
            "REPLAY_ROOT", "predicate-b49-response"
        ),
        grammar_authority_ref=query_auth.authority_ref,
        coordinate_question_value_refs=(),
        risk_set_refs=(),
        scope_refs=(universe.ref,),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(_ref("OPERATOR_SEMANTICS", "BOOLEAN-AND-OR-NOT"),),
    )
    if query_operation is None:
        target_domain = tuple(sorted({
            rule.canonical_value
            for slot in projection.response_slots
            if slot.question_binding.native_question_ref == target.native_question_ref
            for rule in slot.values
            if rule.response_state == "SUBSTANTIVE_RESPONSE" and rule.canonical_value is not None
        }))
        target_topology = "SCALAR_SINGULAR"
    else:
        target_topology, target_domain = native_target_configuration(
            bundle=bundle, target_ref=target.native_question_ref)
    from rawlsing_next.pre553_empirical_objects import EmpiricalQuerySpec

    grain = {
        "source_scope_mode": "SINGLE_UNIVERSE",
        "measure_kind": operation.measure_kind,
        "risk_set_type": "WHOLE_QUESTION_RISK_SET",
        "response_state_semantics_ref": _ref("RESPONSE_STATE_SEMANTICS", "SUBSTANTIVE"),
        "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
    }
    if operation.measure_kind == "GOVERNED_WEIGHTED":
        if not projection.weight_slots:
            raise WorkloadBindingRefusal("WEIGHTED_MEASURE_WITHOUT_WEIGHT_SLOT")
        grain["weight_basis_id"] = projection.weight_slots[0].weight_basis_id
    if query_operation is not None:
        grain["query_operation"] = query_operation
    query = EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(query_auth.authority_ref,),
        dependency_refs=(response_predicate.ref,),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "query-b49"),
        target_refs=(target.native_question_ref,),
        target_arity_and_topology={
            "arity": 1,
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": [{
                "target_ref": target.native_question_ref,
                "topology": target_topology,
                "domain": ([str(v) for v in target_domain]
                           if target_topology in {"SCALAR_SINGULAR", "ROUTED_RESPONSE"}
                           else list(target_domain)),
                "target_domain_replay_ref": _ref(
                    "TARGET_DOMAIN", f"{operation.target_variable_code}-domain"
                ),
                "topology_authority_refs": [projection_auth.authority_ref],
                "response_semantic_authority_refs": [projection_auth.authority_ref],
                "included_states": ["SUBSTANTIVE_RESPONSE"],
            }],
        },
        condition_predicate_ref=response_predicate.ref,
        risk_set_ref=bundle.risk_set_ref or _ref("RISK_SET", profile_risk_tag(projection)),
        empirical_universe_refs=(universe.ref,),
        scope_refs=(universe.ref,),
        measure_basis_ref=_ref("MEASURE_BASIS", operation.measure_kind),
        requested_output_grain=grain,
        query_authority_refs=(query_auth.authority_ref,),
    )
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*bundle.projection.authority_snapshots, query_auth)),
        predicates=(branch, response_predicate),
        queries=(query,),
        discovery_authorities=(),
    )
    return catalog, I03ExecutionRequest(query.ref, response_predicate.ref)


def profile_risk_tag(projection: GovernedC11Projection) -> str:
    """Return the deterministic whole-question risk tag used by the fixture."""
    return f"{projection.source_artifact_id}-whole"


@dataclass(frozen=True)
class TestOnlyIssuedWorkload:
    """One TEST_ONLY native workload plus the exact resolver record it binds."""

    workload: NativeWorkload
    record: IssuedWorkloadRecord
    descriptor: Mapping[str, Any]
    envelope_sha256: str


def build_test_only_workload(
    *,
    bundle: NativePreimageBundle,
    projection: GovernedC11Projection,
    catalog: RuntimeObjectCatalog,
    request: I03ExecutionRequest,
    operation: OperationFixture,
    as_of: str,
    host: str,
    purpose: str,
) -> TestOnlyIssuedWorkload:
    """Build one TEST_ONLY NativeWorkload and its matching resolver record.

    The descriptor carries every closed field from the exact source-native
    projection. The resolver record is explicitly ``TEST_ONLY_SOURCEFREE``;
    it is not a current original-issuer grant and confers no source right.
    """
    if projection is not bundle.projection:
        raise WorkloadBindingRefusal("PROJECTION_NOT_FROM_BUNDLE")
    native_item_ids = tuple(
        sorted(item.source_variable_code for item in bundle.administered)
    )
    descriptor = {
        "source_edition": bundle.source_sha256,
        "native_item_ids": list(native_item_ids),
        "release_tag": projection.instrument_release_id,
        "routing_and_risk": {
            "routing_facts": len(projection.routing),
            "risk_tag": profile_risk_tag(projection),
        },
        "carrier": {
            "source_format": "SYNTHETIC_NONRESPONDENT_FIXTURE",
            "source_artifact_id": projection.source_artifact_id,
        },
        "country_and_population": {
            "country": projection.universes[0].country_geography,
            "population": projection.universes[0].target_population_and_sample_frame,
        },
        "weight_design_estimand": {
            "weight_basis": (projection.weight_slots[0].weight_basis_id
                             if projection.weight_slots else "NO_WEIGHT_DECLARED"),
            "estimand": "TEST_ONLY_SYNTHETIC_ESTIMAND",
        },
        "missing_and_occurrence_policy": {
            "missing": "EXPLICIT_TYPED_STATES",
            "occurrence": "SCALAR_SINGULAR",
        },
        "target_conditioner_roles": {
            "target": operation.target_variable_code,
            "conditioner": None,
            "measure_kind": operation.measure_kind,
        },
    }
    if set(descriptor) != DESCRIPTOR_FIELDS:
        raise WorkloadBindingRefusal("DESCRIPTOR_FIELD_SET_MISMATCH")
    descriptor_bytes = _canonical(descriptor).encode()
    original_u_root = _hash({
        "projection": projection.projection_identity_ref.as_dict(),
        "administered": list(native_item_ids),
    })
    expected_frontier_root = _hash({
        "descriptor": descriptor,
        "source_sha256": bundle.source_sha256,
        "test_only": True,
    })
    decision_ref = _ref("TEST_ONLY_DECISION", f"{operation.fixture_id}-{as_of}")
    workload = NativeWorkload(
        decision_ref=decision_ref,
        source_factory_ref=_ref("SOURCE_FACTORY", bundle.source_sha256),
        descriptor=descriptor_bytes,
        projection=projection,
        catalog=catalog,
        requests=(request,),
        discoveries=(),
        original_u_root=original_u_root,
        expected_frontier_root=expected_frontier_root,
    )
    envelope_sha256 = _hash(workload.envelope())
    record = IssuedWorkloadRecord(
        decision_ref=decision_ref,
        source_permission_ref=_ref("TEST_ONLY_SOURCE_PERMISSION", operation.fixture_id),
        scientific_permission_refs=(
            _ref("TEST_ONLY_SCIENTIFIC_PERMISSION", operation.fixture_id),
        ),
        host=host,
        purpose=purpose,
        source_sha256=bundle.source_sha256,
        envelope_sha256=envelope_sha256,
        original_u_root=original_u_root,
        expected_frontier_root=expected_frontier_root,
        expected_jobs=(("QUERY", request.query_ref.key, request.predicate_ref.key),),
        currentness="CURRENT_GRANTED",
        scope=TEST_ONLY_SCOPE,
        original_wave_identity=None,
        native_universe_refs=(projection.universes[0].ref,),
    )
    return TestOnlyIssuedWorkload(
        workload=workload,
        record=record,
        descriptor=descriptor,
        envelope_sha256=envelope_sha256,
    )


class TestOnlyDecisionResolver:
    """A resolver that returns exactly one explicitly TEST_ONLY record.

    This is a fixed test double, not a credential store and not an issuer. It
    refuses any decision ref other than the one it was constructed with.
    """

    __test__ = False

    def __init__(self, record: IssuedWorkloadRecord) -> None:
        if record.scope != TEST_ONLY_SCOPE:
            raise WorkloadBindingRefusal("TEST_ONLY_RESOLVER_REQUIRES_TEST_ONLY_SCOPE")
        self._record = record

    def resolve_current(self, decision_ref: ExactRef) -> IssuedWorkloadRecord:
        if decision_ref != self._record.decision_ref:
            raise WorkloadBindingRefusal("UNKNOWN_DECISION_REF")
        return self._record


def execute_test_only_workload(
    *,
    issued: TestOnlyIssuedWorkload,
    source_factory: Any,
    host: str,
    purpose: str,
) -> NativeWorkloadResult:
    """Execute one TEST_ONLY workload through the existing U43/B/C11/I03 path."""
    resolver = TestOnlyDecisionResolver(issued.record)
    admit(issued.workload, resolver, host=host, purpose=purpose, allow_test_only=True)
    return execute_issued_workload(
        issued.workload,
        resolver,
        source_factory=source_factory,
        host=host,
        purpose=purpose,
        allow_test_only=True,
    )


__all__ = [
    "DESCRIPTOR_FIELDS",
    "OperationFixture",
    "SCHEMA",
    "TEST_ONLY_SCOPE",
    "TestOnlyIssuedWorkload",
    "TestOnlyDecisionResolver",
    "WorkloadBindingRefusal",
    "DISCOVERY_WORKLOAD_SCHEMA",
    "NativeDiscoveryExecution",
    "build_discovery_authority",
    "build_frontier_native_catalog",
    "build_projection_catalog",
    "build_test_only_discovery_workload",
    "build_test_only_workload",
    "execute_test_only_discovery_workload",
    "execute_test_only_workload",
    "profile_risk_tag",
]


DISCOVERY_WORKLOAD_SCHEMA = "PRE553_R03_TEST_ONLY_DISCOVERY_WORKLOAD@1.0.0"


def _target_key(targets: Sequence[OccurrenceKey]) -> str:
    return json.dumps(
        [target.key for target in targets], sort_keys=False, separators=(",", ":")
    )


def _measure_native_kind(measure_kind: str) -> str:
    if measure_kind == "SAMPLE":
        return "RAW"
    if measure_kind == "POPULATION":
        return "GOVERNED_WEIGHTED"
    raise WorkloadBindingRefusal("UNKNOWN_MEASURE_KIND", measure_kind)


def _branch_predicate_for_bundle(
    *, bundle: NativePreimageBundle, query_auth: AuthoritySnapshot, as_of: str
) -> Any:
    projection = bundle.projection
    universe = projection.universes[0]
    members = tuple(sorted((r.ref for r in projection.respondents), key=lambda r: r.key))
    membership = _ref(
        "BRANCH_MEMBERSHIP",
        f"r03-all-{_hash([m.key for m in members])[:12]}",
    )
    branch_ast = {
        "op": "LEAF",
        "leaf_type": "DERIVED_BRANCH_COHORT",
        "branch_definition_id": "BRANCH-r03-all",
        "resolved_predicate_hash_or_exact_membership_ref": membership,
        "parent_ancestry_ref": _ref("BRANCH_PARENT", "r03-all"),
        "branch_algorithm_authority_ref": query_auth.authority_ref,
        "branch_membership_replay_ref": _ref("BRANCH_REPLAY", "r03-all"),
        "branch_source_scope_ref": universe.ref,
        "exact_member_respondent_refs": members,
    }
    return make_empirical_predicate(
        predicate_ast=branch_ast,
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(query_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "predicate-r03-all"),
        grammar_authority_ref=query_auth.authority_ref,
        coordinate_question_value_refs=(),
        risk_set_refs=(),
        scope_refs=(universe.ref,),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(_ref("OPERATOR_SEMANTICS", "BOOLEAN-AND-OR-NOT"),),
    )


def _response_predicate_for_bundle(
    *,
    bundle: NativePreimageBundle,
    query_auth: AuthoritySnapshot,
    projection_auth: AuthoritySnapshot,
    source_variable_code: str,
    response_value: Any,
    as_of: str,
) -> Any:
    qref = bundle.question_refs.get(source_variable_code)
    if qref is None:
        raise WorkloadBindingRefusal(
            "FIXTURE_TARGET_NOT_ADMINISTERED", source_variable_code
        )
    ast = {
        "op": "LEAF",
        "leaf_type": "SURVEY_RESPONSE_EVENT",
        "question_semantic_ref": qref,
        "component_or_event_selector_ref": _ref(
            "EVENT_SELECTOR", f"{source_variable_code}-ANY"
        ),
        "response_value_or_state_ref": _ref(
            "VALUE_REF", f"{source_variable_code}-{response_value}"
        ),
        "response_topology_authority_ref": projection_auth.authority_ref,
        "response_semantic_authority_ref": projection_auth.authority_ref,
        "operator": "EQ",
        "exact_value": str(response_value),
    }
    return make_empirical_predicate(
        predicate_ast=ast,
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(query_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref(
            "REPLAY_ROOT", f"predicate-r03-response-{source_variable_code}-{response_value}"
        ),
        grammar_authority_ref=query_auth.authority_ref,
        coordinate_question_value_refs=(),
        risk_set_refs=(),
        scope_refs=(bundle.projection.universes[0].ref,),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(_ref("OPERATOR_SEMANTICS", "BOOLEAN-AND-OR-NOT"),),
    )


def _query_for_bundle(
    *,
    bundle: NativePreimageBundle,
    query_auth: AuthoritySnapshot,
    projection_auth: AuthoritySnapshot,
    baseline: Any,
    targets: Sequence[OccurrenceKey],
    occurrence_by_key: Mapping[OccurrenceKey, Any],
    measure_kind: str,
    as_of: str,
) -> EmpiricalQuerySpec:
    projection = bundle.projection
    universe = projection.universes[0]
    risk_ref = bundle.risk_set_ref or _ref(
        "RISK_SET", profile_risk_tag(projection)
    )
    components = []
    target_refs = []
    for target in targets:
        occurrence = occurrence_by_key[target]
        qref = bundle.question_refs.get(target.item_id)
        if qref is None:
            raise WorkloadBindingRefusal(
                "FIXTURE_TARGET_NOT_ADMINISTERED", target.item_id
            )
        target_refs.append(qref)
        components.append({
            "target_ref": qref,
            "topology": occurrence.topology,
            "domain": [str(value) for value in occurrence.domain],
            "target_domain_replay_ref": _ref(
                "TARGET_DOMAIN",
                f"{target.key}-{_hash([str(v) for v in occurrence.domain])[:12]}",
            ),
            "topology_authority_refs": [projection_auth.authority_ref],
            "response_semantic_authority_refs": [projection_auth.authority_ref],
            "included_states": ["SUBSTANTIVE_RESPONSE"],
        })
    native_measure = _measure_native_kind(measure_kind)
    if native_measure == "GOVERNED_WEIGHTED" and not projection.weight_slots:
        raise WorkloadBindingRefusal("WEIGHTED_MEASURE_WITHOUT_WEIGHT_SLOT")
    grain = {
        "source_scope_mode": "SINGLE_UNIVERSE",
        "measure_kind": native_measure,
        "risk_set_type": "WHOLE_QUESTION_RISK_SET",
        "response_state_semantics_ref": _ref(
            "RESPONSE_STATE_SEMANTICS", "SUBSTANTIVE"
        ),
        "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
    }
    if native_measure == "GOVERNED_WEIGHTED":
        grain["weight_basis_id"] = projection.weight_slots[0].weight_basis_id
    return EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(query_auth.authority_ref,),
        dependency_refs=(baseline.ref,),
        producer_replay_locator_or_reference_root=_ref(
            "REPLAY_ROOT", f"query-r03-{'-'.join(t.item_id for t in targets)}"
        ),
        target_refs=tuple(target_refs),
        target_arity_and_topology={
            "arity": len(targets),
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": components,
        },
        condition_predicate_ref=baseline.ref,
        risk_set_ref=risk_ref,
        empirical_universe_refs=(universe.ref,),
        scope_refs=(universe.ref,),
        measure_basis_ref=_ref("MEASURE_BASIS", native_measure),
        requested_output_grain=grain,
        query_authority_refs=(query_auth.authority_ref,),
    )


def build_frontier_native_catalog(
    *,
    bundle: NativePreimageBundle,
    inventory: SourceInventory,
    policy: Any,
    frontier: Any,
    as_of: str,
    query_authority: AuthoritySnapshot | None = None,
) -> tuple[NativeCatalog, AuthoritySnapshot, Any, ExactRef]:
    """Build exact I05 capability objects for the supplied governed frontier.

    Every operation keeps its policy disposition. Missing native objects become
    typed lowering refusals; they are never dropped or replaced by a narrower
    question list.
    """
    if not isinstance(bundle, NativePreimageBundle):
        raise WorkloadBindingRefusal("NATIVE_PREIMAGE_BUNDLE_REQUIRED")
    if not isinstance(inventory, SourceInventory):
        raise WorkloadBindingRefusal("SOURCE_INVENTORY_REQUIRED")
    if inventory.source_sha256 != bundle.source_sha256:
        raise WorkloadBindingRefusal("INVENTORY_SOURCE_EDITION_MISMATCH")
    projection = bundle.projection
    try:
        projection_auth = next(
            a for a in projection.authority_snapshots
            if a.authority_kind == "SOURCE_SEMANTICS_TOPOLOGY"
            and "RespondentEvent@1.0.0" in a.governed_object_families
            and "EmpiricalCoordinateFact@1.0.0" in a.governed_object_families
        )
    except StopIteration as exc:
        raise WorkloadBindingRefusal("PROJECTION_AUTHORITY_UNAVAILABLE") from exc
    if query_authority is None:
        query_auth = AuthoritySnapshot(
            typed_state="ALLOW",
            authority_snapshot_refs=(),
            dependency_refs=(),
            producer_replay_locator_or_reference_root=_ref(
                "REPLAY_ROOT", "r03-query-authority"
            ),
            authority_id="R03-TEST-ONLY-FRONTIER-QUERY-AUTH",
            authority_version="1.0.0",
            authority_content_hash=_hash({
                "tag": "r03-query", "source_sha256": bundle.source_sha256, "as_of": as_of,
            }),
            authority_kind="PREDICATE_GRAMMAR",
            decision_state="ALLOW",
            governed_operations=("R03-OP-query",),
            governed_object_families=(
                "EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0",
                "EmpiricalFact@1.0.0",
            ),
            scope_envelope={
                "source_universe_refs": "EXPLICIT_UNRESTRICTED",
                "target_use_refs": "EXPLICIT_UNRESTRICTED",
                "predicate_or_risk_set_refs": "EXPLICIT_UNRESTRICTED",
                "source_sha256": bundle.source_sha256,
                "as_of": as_of,
                "grade": "TEST_ONLY_SOURCEFREE",
            },
            effective_time_or_interval=as_of,
            parent_authority_refs=(),
            negative_limit_refs=(),
            supersession_refs=(),
            interpretation_semantics_fingerprint=_hash({
                "tag": "r03-query", "as_of": as_of,
            }),
            replay_protocol_ref=_ref("REPLAY_PROTOCOL", "r03-query-authority"),
        )
    else:
        expected_measure_kinds = tuple(sorted({
            "RAW" if operation.measure_kind == "SAMPLE" else "GOVERNED_WEIGHTED"
            for operation in frontier.operations
            if operation.measure_kind in ("SAMPLE", "POPULATION")
        }))
        _exact_external_query_authority(
            authority=query_authority, bundle=bundle, as_of=as_of,
            expected_measure_kinds=expected_measure_kinds or None,
        )
        query_auth = query_authority
    baseline = _branch_predicate_for_bundle(
        bundle=bundle, query_auth=query_auth, as_of=as_of
    )
    occurrence_by_key = inventory.by_key()
    state_map = dict(inventory.state_map)
    if not inventory.inventory_complete:
        raise WorkloadBindingRefusal("INVENTORY_INCOMPLETE_NOT_PROSPECTIVE")
    predicate_refs: dict[str, ExactRef] = {}
    predicate_objects: dict[str, Any] = {}
    cell_codec: dict[str, Any] = {}
    for occurrence in inventory.occurrences:
        qref = bundle.question_refs.get(occurrence.key.item_id)
        if qref is None:
            continue
        for value in occurrence.domain:
            try:
                value_key = typed_value_key(value)
            except Exception as exc:
                raise WorkloadBindingRefusal(
                    "INVENTORY_VALUE_NOT_TYPED", occurrence.key.item_id
                ) from exc
            cell_codec.setdefault(value_key, str(value))
            try:
                predicate = _response_predicate_for_bundle(
                    bundle=bundle, query_auth=query_auth,
                    projection_auth=projection_auth,
                    source_variable_code=occurrence.key.item_id,
                    response_value=value, as_of=as_of,
                )
            except WorkloadBindingRefusal:
                continue
            predicate_refs[occurrence.key.key + "|" + value_key] = predicate.ref
            predicate_objects[predicate.ref.key] = predicate
    predicate_objects.setdefault(baseline.ref.key, baseline)
    target_tuples: set[tuple[OccurrenceKey, ...]] = set()
    measure_kinds: set[str] = set()
    for operation in frontier.operations:
        if operation.measure_kind not in ("SAMPLE", "POPULATION"):
            continue
        target_tuples.add(tuple(operation.targets))
        measure_kinds.add(operation.measure_kind)
        for target in operation.targets:
            target_tuples.add((target,))
    if not target_tuples:
        target_tuples.add(tuple())
    query_refs: dict[str, ExactRef] = {}
    joint_query_refs: dict[str, ExactRef] = {}
    marginal_query_refs: dict[str, ExactRef] = {}
    query_objects: dict[str, EmpiricalQuerySpec] = {}
    allowed_measures = ("SAMPLE",) + (
        ("POPULATION",) if projection.weight_slots else ()
    )
    for targets in sorted(target_tuples, key=lambda items: tuple(t.key for t in items)):
        if not targets or len(targets) > int(policy.bounds["J"]):
            continue
        if any(target not in occurrence_by_key for target in targets):
            continue
        if any(
            occurrence_by_key[target].topology != "SCALAR_SINGULAR"
            for target in targets
        ):
            continue
        for measure_kind in sorted(measure_kinds or {"SAMPLE"}):
            if measure_kind not in allowed_measures:
                continue
            try:
                query = _query_for_bundle(
                    bundle=bundle, query_auth=query_auth,
                    projection_auth=projection_auth, baseline=baseline,
                    targets=targets, occurrence_by_key=occurrence_by_key,
                    measure_kind=measure_kind, as_of=as_of,
                )
            except WorkloadBindingRefusal:
                continue
            query_refs[_target_key(targets) + "|" + measure_kind] = query.ref
            query_objects[query.ref.key] = query
            if len(targets) == 1:
                marginal_query_refs.setdefault(targets[0].key, query.ref)
            else:
                joint_query_refs.setdefault(_target_key(targets), query.ref)
    catalog = NativeCatalog(
        catalog_ref=f"urn:r03:native-catalog:{inventory.content_hash}",
        baseline_predicate_ref=baseline.ref,
        predicate_refs=predicate_refs,
        query_refs=query_refs,
        joint_query_refs=joint_query_refs,
        marginal_query_refs=marginal_query_refs,
        supported_claims=(
            "DIST", "CONDITIONAL", "JOINT", "CO_TRAVEL", "FORK",
            "INTERACTION", "STATE_ROBUSTNESS",
        ),
        supported_topologies=("SCALAR_SINGULAR",),
        supported_condition_modes=("AND", "XOR_EXACTLY_ONE"),
        maximum_target_arity=int(policy.bounds["J"]),
        maximum_conditioner_arity=int(policy.bounds["K"]),
        supported_measures=allowed_measures,
        cell_codec=cell_codec,
        predicate_objects=predicate_objects,
        query_objects=query_objects,
        discovery_authority_ref=None,
        batch_unit_refs=(),
        evidence_grade_ceiling="SOURCEFREE_TEST_ONLY",
    )
    return catalog, query_auth, baseline, projection_auth.authority_ref


def build_discovery_authority(
    *,
    bundle: NativePreimageBundle,
    grammar: Mapping[str, Any],
    policy: Any,
    as_of: str,
    authority: AuthoritySnapshot | None = None,
) -> tuple[AuthoritySnapshot, DiscoveryAuthority]:
    """Create one exact-bounded TEST_ONLY authority for a frozen grammar."""
    if not isinstance(bundle, NativePreimageBundle):
        raise WorkloadBindingRefusal("NATIVE_PREIMAGE_BUNDLE_REQUIRED")
    projection = bundle.projection
    operations = sorted({
        str(rule["validation"]["kind"]) for rule in grammar.get("rules", ())
    })
    if not operations:
        operations = ["TARGET_CELL_SUPPORTED"]
    validation_kinds = tuple(sorted({
        "DISTRIBUTION_DIFFERS_FROM_BASELINE",
        "JOINT_NOT_PRODUCT_OF_MARGINALS",
        "CONDITIONAL_REVERSAL",
        "TARGET_CELL_SUPPORTED",
        *operations,
    }))
    digest = semantic_hash(grammar)
    if authority is None:
        authority = AuthoritySnapshot(
            typed_state="ALLOW",
            authority_snapshot_refs=(),
            dependency_refs=(),
            producer_replay_locator_or_reference_root=_ref(
                "REPLAY_ROOT", "r03-discovery-authority"
            ),
            authority_id="R03-TEST-ONLY-DISCOVERY-AUTH",
            authority_version="1.0.0",
            authority_content_hash=_hash({
                "tag": "r03-discovery", "grammar": digest, "source": bundle.source_sha256,
                "as_of": as_of,
            }),
            authority_kind="DISCOVERY_FRONTIER",
            decision_state="ALLOW",
            governed_operations=(str(grammar["discovery_operation"]),),
            governed_object_families=(
                "DiscoveryAuthority@1.0.0", "DiscoveryResultReceipt@1.0.0",
                "EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0",
                "EmpiricalFact@1.0.0",
            ),
            scope_envelope={
                "source_universe_refs": "EXPLICIT_UNRESTRICTED",
                "target_use_refs": "EXPLICIT_UNRESTRICTED",
                "predicate_or_risk_set_refs": "EXPLICIT_UNRESTRICTED",
                "source_sha256": bundle.source_sha256,
                "as_of": as_of,
                "grade": "TEST_ONLY_SOURCEFREE",
            },
            effective_time_or_interval=as_of,
            parent_authority_refs=(),
            negative_limit_refs=(),
            supersession_refs=(),
            interpretation_semantics_fingerprint=_hash({
                "tag": "r03-discovery", "as_of": as_of,
            }),
            replay_protocol_ref=_ref("REPLAY_PROTOCOL", "r03-discovery-authority"),
        )
    else:
        if not isinstance(authority, AuthoritySnapshot):
            raise WorkloadBindingRefusal("SUPPLIED_DISCOVERY_AUTHORITY_REQUIRED")
        scope = authority.scope_envelope
        if not isinstance(scope, Mapping) or scope.get("source_sha256") != bundle.source_sha256:
            raise WorkloadBindingRefusal("SUPPLIED_DISCOVERY_AUTHORITY_SOURCE_MISMATCH")
        universes = scope.get("source_universe_refs")
        risks = scope.get("predicate_or_risk_set_refs")
        if (isinstance(universes, (str, bytes)) or not isinstance(universes, Sequence)
                or isinstance(risks, (str, bytes)) or not isinstance(risks, Sequence)):
            raise WorkloadBindingRefusal("SUPPLIED_DISCOVERY_AUTHORITY_EXACT_SCOPE_REQUIRED")
        declared_universes = tuple(sorted(
            (exact_ref(value, "discovery_authority.scope.source_universe_refs")
             for value in universes), key=lambda ref: ref.key))
        expected_universes = tuple(sorted(
            (universe.ref for universe in bundle.projection.universes),
            key=lambda ref: ref.key))
        declared_risks = tuple(sorted(
            (exact_ref(value, "discovery_authority.scope.predicate_or_risk_set_refs")
             for value in risks), key=lambda ref: ref.key))
        if declared_universes != expected_universes:
            raise WorkloadBindingRefusal("SUPPLIED_DISCOVERY_AUTHORITY_UNIVERSE_MISMATCH")
        if declared_risks != (bundle.risk_set_ref,):
            raise WorkloadBindingRefusal("SUPPLIED_DISCOVERY_AUTHORITY_RISK_MISMATCH")
        operation = str(grammar["discovery_operation"])
        for family in ("DiscoveryAuthority@1.0.0", "DiscoveryResultReceipt@1.0.0",
                       "EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0",
                       "EmpiricalFact@1.0.0"):
            for universe_ref in expected_universes:
                require_positive_authority(
                    authority, authority_kind="DISCOVERY_FRONTIER",
                    operation=operation, object_family=family,
                    source_universe_ref=universe_ref.as_dict(),
                    predicate_or_risk_set_ref=bundle.risk_set_ref.as_dict(),
                )
    risk_ref = bundle.risk_set_ref or _ref(
        "RISK_SET", profile_risk_tag(projection)
    )
    discovery = DiscoveryAuthority(
        typed_state="EXACT_BOUNDED_AUTHORIZED",
        authority_snapshot_refs=(authority.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref(
            "REPLAY_ROOT", "r03-discovery"
        ),
        candidate_grammar_ref=ExactRef(
            "PRE553_I05_CANDIDATE_GRAMMAR",
            f"urn:r03:i05:grammar:{digest}",
            digest,
        ),
        candidate_universe_definition=grammar,
        source_universe_scope={
            "allowed_universe_refs": (projection.universes[0].ref,),
        },
        risk_set_scope={"allowed_risk_set_refs": (risk_ref,)},
        topology_scope={
            "maximum_target_arity_J": int(policy.bounds["J"]),
        },
        measure_scope={"allowed_measure_kinds": ("RAW", "GOVERNED_WEIGHTED")},
        support_rules={"minimum_raw_denominator": 1},
        validation_rules={"kinds": validation_kinds},
        coverage_claim=COVERAGE_CLAIM,
        pruning_contract={"kind": "NONE_EXACT_EVALUATE_ALL"},
        algorithm_identity_if_semantically_required=I05_CONTRACT_ID,
        tie_order_rules="CANONICAL_CANDIDATE_HASH_ORDER",
        rng_policy_if_any="NONE",
        mode="EXACT_BOUNDED",
        candidate_scoring_or_ranking_rule_if_any={
            "kind": "NONE", "controls_frontier": False,
        },
    )
    return authority, discovery


def build_test_only_discovery_workload(
    *,
    bundle: NativePreimageBundle,
    projection: GovernedC11Projection,
    catalog: RuntimeObjectCatalog,
    authority: DiscoveryAuthority,
    descriptor: Mapping[str, Any],
    inventory: SourceInventory,
    plan_hash: str,
    as_of: str,
    host: str,
    purpose: str,
) -> TestOnlyIssuedWorkload:
    """Issue one TEST_ONLY discovery workload without inventing source rights."""
    if projection is not bundle.projection:
        raise WorkloadBindingRefusal("PROJECTION_NOT_FROM_BUNDLE")
    native_item_ids = tuple(
        sorted(item.source_variable_code for item in bundle.administered)
    )
    closed_descriptor = {
        "source_edition": bundle.source_sha256,
        "native_item_ids": list(native_item_ids),
        "release_tag": projection.instrument_release_id,
        "routing_and_risk": {
            "routing_facts": len(projection.routing),
            "risk_tag": profile_risk_tag(projection),
        },
        "carrier": {
            "source_format": "SYNTHETIC_NONRESPONDENT_FIXTURE",
            "source_artifact_id": projection.source_artifact_id,
        },
        "country_and_population": {
            "country": projection.universes[0].country_geography,
            "population": projection.universes[0].target_population_and_sample_frame,
        },
        "weight_design_estimand": {
            "weight_basis": (
                projection.weight_slots[0].weight_basis_id
                if projection.weight_slots else "NO_WEIGHT_DECLARED"
            ),
            "estimand": "TEST_ONLY_SYNTHETIC_ESTIMAND",
        },
        "missing_and_occurrence_policy": {
            "missing": "EXPLICIT_TYPED_STATES",
            "occurrence": "FRONTIER_DECLARED_TOPOLOGY",
        },
        "target_conditioner_roles": dict(descriptor),
    }
    if set(closed_descriptor) != DESCRIPTOR_FIELDS:
        raise WorkloadBindingRefusal("DESCRIPTOR_FIELD_SET_MISMATCH")
    decision_ref = _ref("TEST_ONLY_DECISION", f"r03-discovery-{plan_hash[:16]}-{as_of}")
    workload = NativeWorkload(
        decision_ref=decision_ref,
        source_factory_ref=_ref("SOURCE_FACTORY", bundle.source_sha256),
        descriptor=_canonical(closed_descriptor).encode(),
        projection=projection,
        catalog=catalog,
        requests=(),
        discoveries=(authority.ref,),
        original_u_root=semantic_hash({
            "inventory": inventory.content_hash,
            "source_sha256": bundle.source_sha256,
            "native_item_ids": list(native_item_ids),
        }),
        expected_frontier_root=plan_hash,
    )
    envelope_sha256 = _hash(workload.envelope())
    record = IssuedWorkloadRecord(
        decision_ref=decision_ref,
        source_permission_ref=_ref(
            "TEST_ONLY_SOURCE_PERMISSION", f"r03-discovery-{plan_hash[:16]}"
        ),
        scientific_permission_refs=(
            _ref("TEST_ONLY_SCIENTIFIC_PERMISSION", f"r03-discovery-{plan_hash[:16]}"),
        ),
        host=host,
        purpose=purpose,
        source_sha256=bundle.source_sha256,
        envelope_sha256=envelope_sha256,
        original_u_root=workload.original_u_root,
        expected_frontier_root=plan_hash,
        expected_jobs=(("DISCOVERY", authority.ref.key, ""),),
        currentness="CURRENT_GRANTED",
        scope=TEST_ONLY_SCOPE,
        original_wave_identity=None,
        native_universe_refs=(projection.universes[0].ref,),
    )
    return TestOnlyIssuedWorkload(
        workload=workload, record=record, descriptor=closed_descriptor,
        envelope_sha256=envelope_sha256,
    )


@dataclass(frozen=True)
class NativeDiscoveryExecution:
    native_result: Any
    manifest: BatchManifest
    receipts: tuple[Any, ...]
    envelope_sha256: str
    decision_ref: ExactRef
    scope: str


def execute_test_only_discovery_workload(
    *,
    issued: TestOnlyIssuedWorkload,
    source_factory: Any,
    host: str,
    purpose: str,
) -> NativeDiscoveryExecution:
    """Execute one issued discovery through Batch -> C11 -> I05 exactly once.

    U43's unbounded Route B path also invokes I05, so this bounded ingress
    deliberately reuses U43 admission/envelope plus the actual Batch/I05/C11
    owners without a second discovery call.
    """
    if not isinstance(issued, TestOnlyIssuedWorkload):
        raise WorkloadBindingRefusal("TEST_ONLY_WORKLOAD_REQUIRED")
    resolver = TestOnlyDecisionResolver(issued.record)
    admitted = admit(
        issued.workload, resolver, host=host, purpose=purpose, allow_test_only=True
    )

    def check_current() -> None:
        current = admit(
            issued.workload, resolver, host=host, purpose=purpose,
            allow_test_only=True,
        )
        if current != admitted:
            raise WorkloadBindingRefusal("ISSUER_SNAPSHOT_CHANGED_DURING_EXECUTION")

    source = source_factory(issued.workload.source_factory_ref)
    if getattr(source, "source_sha256", None) != issued.record.source_sha256:
        raise WorkloadBindingRefusal("SOURCE_FACTORY_RETURNED_WRONG_EDITION")
    check_current()
    repository, release = build_source_backed_c11_repository(
        source, issued.workload.projection
    )
    executor = CarrierNeutralResearchExecutor(
        repository, (release.release_ref,), issued.workload.catalog
    )
    discovery_ref = issued.workload.discoveries[0]
    manifest = BatchManifest((
        BatchUnitSpec(
            "DISCOVERY", discovery_ref, (release.release_ref,),
            (issued.workload.decision_ref,),
        ),
    ))
    outputs: dict[str, Any] = {}

    def execute(unit: BatchUnitSpec) -> ExecutionOutcome:
        result = executor.execute_i05(discovery_authority_ref=unit.job_ref)
        outputs[unit.unit_hash] = result
        return ExecutionOutcome(
            tuple(receipt.ref for receipt in result.receipts),
            (release.replay_manifest.ref, issued.workload.decision_ref),
        )

    executor_ref = ExactRef(
        "U43_ISSUED_NATIVE_TRANSPORT",
        "urn:r03:batch-discovery:" + issued.envelope_sha256,
        issued.envelope_sha256,
    )
    runner = BatchExecutionRunner(manifest=manifest, repository=repository)
    runner.run(executors={
        "DISCOVERY": ExecutorBinding(executor_ref, execute),
    })
    check_current()
    if len(runner.receipts) != 1 or runner.receipts[0].state != "COMPLETED":
        raise WorkloadBindingRefusal("NATIVE_DISCOVERY_EXECUTION_INCOMPLETE")
    native_result = outputs[manifest.units[0].unit_hash]
    return NativeDiscoveryExecution(
        native_result=native_result,
        manifest=manifest,
        receipts=runner.receipts,
        envelope_sha256=issued.envelope_sha256,
        decision_ref=issued.record.decision_ref,
        scope=issued.record.scope,
    )
