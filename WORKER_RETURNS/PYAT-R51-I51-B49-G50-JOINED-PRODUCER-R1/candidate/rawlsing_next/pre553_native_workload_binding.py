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
from dataclasses import dataclass
from typing import Any, Mapping

from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    ExactRef,
    make_empirical_predicate,
)
from rawlsing_next.pre553_issued_workload import (
    IssuedWorkloadRecord,
    NativeWorkload,
    NativeWorkloadResult,
    admit,
    execute_issued_workload,
)
from rawlsing_next.pre553_route_b_production import I03ExecutionRequest
from rawlsing_next.pre553_source_backed_c11_facade import GovernedC11Projection
from rawlsing_next.pre553_source_native_preimage_adapter import NativePreimageBundle

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


def build_projection_catalog(
    *,
    bundle: NativePreimageBundle,
    operation: OperationFixture,
    as_of: str,
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
        a for a in bundle.authorities if a.authority_kind == "SOURCE_SEMANTICS_TOPOLOGY"
        and "RespondentEvent@1.0.0" in a.governed_object_families
        and "EmpiricalCoordinateFact@1.0.0" in a.governed_object_families
    )
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
    target_domain = tuple(sorted({
        rule.canonical_value
        for slot in projection.response_slots
        if slot.question_binding.native_question_ref == target.native_question_ref
        for rule in slot.values
        if rule.response_state == "SUBSTANTIVE_RESPONSE" and rule.canonical_value is not None
    }))
    from rawlsing_next.pre553_empirical_objects import EmpiricalQuerySpec

    grain = {
        "source_scope_mode": "SINGLE_UNIVERSE",
        "measure_kind": operation.measure_kind,
        "risk_set_type": "WHOLE_QUESTION_RISK_SET",
        "response_state_semantics_ref": _ref("RESPONSE_STATE_SEMANTICS", "SUBSTANTIVE"),
        "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
    }
    if operation.measure_kind == "GOVERNED_WEIGHTED":
        grain["weight_basis_id"] = projection.weight_slots[0].weight_basis_id
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
                "topology": "SCALAR_SINGULAR",
                "domain": [str(v) for v in target_domain],
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
        authorities=tuple((*bundle.authorities, query_auth)),
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
            "weight_basis": projection.weight_slots[0].weight_basis_id,
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
    "build_projection_catalog",
    "build_test_only_workload",
    "execute_test_only_workload",
    "profile_risk_tag",
]
