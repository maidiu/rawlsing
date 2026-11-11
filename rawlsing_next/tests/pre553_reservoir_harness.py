"""PRE553 R13 non-semantic reservoir preintegration harness.

This module is test-only wiring. It never creates a structural admission decision or
interprets an EmpiricalFact. Callers supply already-decided StructuralEmpiricalAdmission-
shaped fixtures and explicit V553/authority stubs; frozen M1-M4 perform every downstream
semantic transition that is exercised here.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from rawlsing_next.m1_temporal_v554_admission_dedup import (
    BasisKind,
    M1DecisionState,
    M1Evaluation,
    SIG_002,
    TemporalCompleteness,
    evaluate_m1_temporal_v554_admission_dedup,
    semantic_hash,
)
from rawlsing_next.m2_v555_atomic_route import (
    CHANNEL_STRUCTURAL_ROLE_ID,
    M2DecisionState,
    M2Evaluation,
    RECEIVING_CONSTRAINT_KIND,
    ROUTE_AUTHORITY_ID,
    ROUTE_AUTHORITY_VERSION,
    ROUTE_RULE_ID,
    ROUTE_RULE_VERSION,
    ROUTE_SHAPE_ID,
    ROUTE_SHAPE_VERSION,
    SEMANTIC_FAMILY as V555_SEMANTIC_FAMILY,
    evaluate_m2_v555_atomic_route,
)
from rawlsing_next.m3_v556_higher_order_structural import (
    M3_CONTRACT_ID,
    M3DecisionState,
    M3Evaluation,
    PERSON_STATE_SEMANTICS,
    RESULT_CONTRACT_BINDING_REF_KIND,
    RESULT_JURISDICTION,
    RESULT_SCHEMA_REF_KIND,
    evaluate_m3_v556_higher_order_structural,
)
from rawlsing_next.m4_v557_v558_publication_repository import (
    AuthorityRef,
    ContextQueryItem,
    RepositoryEntry,
    V557DecisionState,
    V557PublicationEntry,
    build_v557_publication_bundle,
    build_v558_repository_bundle,
    exact_resolution_key,
    govern_v557,
    make_context_query,
    make_producer_locator,
    make_reference_edge,
    resolve_v558,
    structural_object_from_m2,
    structural_object_from_m3,
    structural_objects_from_m1,
)

ASSIGNMENT_ID = "PRE553-W03-R13-001"
HARNESS_CONTRACT_ID = "PRE553_R13_RESERVOIR_PREINTEGRATION_HARNESS@1.0.0"
EXACT_BASE_SHA = "53ebe82da36187c38aec305109a9482c433dd0e3"
_SHA = re.compile(r"^[0-9a-f]{64}$")

FROZEN_DOWNSTREAM_BLOBS = MappingProxyType({
    "m1_temporal_v554_admission_dedup.py": "e8bd6376720a2de132b384e7771d71d8d39cf261",
    "m2_v555_atomic_route.py": "deef8a60613635a10faf7d89cd8cdf0c3b8a0710",
    "m3_v556_higher_order_structural.py": "a4749541273c921ebe4ff7a0b91460bb1e016b87",
    "m4_v557_v558_publication_repository.py": "9005308fb06686b593783666e77d06619645b2bb",
    "m5_runtime_rsc_peer_prior.py": "18735bdb31a220aed032aa722574d685e2bdddf5",
    "m6_actor_safe_expression.py": "74d9701cdc7dabccf61eb5089498db290c1efd9c",
    "render_bounded_expression.py": "eef88095d1d647b5332aa5186a3a5df218fcf9f8",
    "v3_psepf_zero_positive_guard.py": "e0528d65215cb431196570c38bac4eae94217a1b",
})

HARNESS_CONTRACT = MappingProxyType({
    "contract_id": HARNESS_CONTRACT_ID,
    "assignment_id": ASSIGNMENT_ID,
    "exact_base": EXACT_BASE_SHA,
    "semantic_authority": False,
    "runtime_authority": False,
    "admission_decision_service": False,
    "fixture_content_is_authority": False,
    "positive_path": (
        "PREDECIDED_STRUCTURAL_EMPIRICAL_ADMISSION_SHAPE",
        "EXPLICIT_V553_STUB",
        "FROZEN_M1_V554",
        "FROZEN_M2_V555",
        "FROZEN_M3_V556",
        "FROZEN_M4_V557",
        "FROZEN_M4_V558_STRUCTURAL_PRIOR_REPOSITORY",
    ),
    "forbidden": (
        "EMPIRICAL_FACT_TO_STRUCTURAL_INTERPRETATION",
        "ADMISSION_DECISION_MANUFACTURE",
        "V553_INGRESS_WIDENING",
        "DOWNSTREAM_RUNTIME_MUTATION",
        "V3_ACTOR_STATE_FABRICATION",
        "IMPLICIT_SOURCE_COMPOSITION",
    ),
})
HARNESS_CONTRACT_HASH = semantic_hash(HARNESS_CONTRACT)

ADMISSION_SHAPE_FIELDS = frozenset({
    "structural_empirical_admission_id",
    "structural_empirical_admission_content_hash",
    "admission_authority_id",
    "admission_authority_version",
    "admission_authority_hash",
    "admission_decision_state",
    "focal_structural_proposition_ref",
    "structural_semantic_identity_refs",
    "native_scope_identity_refs",
    "target_use_permission_refs",
    "effective_time_or_interval_refs_required_by_target_use",
    "source_universe_refs",
    "estimand_refs",
    "measure_and_weight_authority_refs",
    "applicable_negative_denial_noncomparability_refs",
    "interpretation_critical_authority_refs",
    "producer_replay_locator_or_reference_root",
})

V554_RULE_STUB = MappingProxyType({
    "id": "PRE553_R13_TEST_ONLY_V554_RULE",
    "version": "test-only-1",
    "hash": semantic_hash({"stub": "v554-rule", "assignment": ASSIGNMENT_ID}),
})


class HarnessFixtureError(ValueError):
    pass


def _h(label: str) -> str:
    return semantic_hash({"pre553_r13_fixture": label})


def _ref(kind: str, object_id: str) -> dict[str, str]:
    return {"kind": kind, "object_id": object_id, "content_hash": _h(f"ref:{kind}:{object_id}")}


def _assert_sha(value: Any, name: str) -> str:
    if not isinstance(value, str) or not _SHA.fullmatch(value):
        raise HarnessFixtureError(f"{name} must be exact lowercase sha256")
    return value


def _assert_string_sequence(value: Any, name: str, *, nonempty: bool = False) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise HarnessFixtureError(f"{name} must be a sequence")
    out = tuple(value)
    if any(not isinstance(x, str) or not x for x in out):
        raise HarnessFixtureError(f"{name} must contain non-empty strings")
    if nonempty and not out:
        raise HarnessFixtureError(f"{name} must be non-empty")
    return out


def make_admission_fixture(
    *, tag: str, source_universe: str, decision_state: str,
    negative_refs: Sequence[str] = (),
) -> dict[str, Any]:
    """Create shape-only test material with a caller-selected decision state.

    The helper does not infer or choose the decision. The returned object is never
    represented as accepted production authority.
    """
    material = {
        "tag": tag,
        "source_universe": source_universe,
        "decision_state": decision_state,
        "negative_refs": list(negative_refs),
    }
    admission_id = f"urn:rawlsing:test:pre553-r13:admission:{semantic_hash(material)}"
    return {
        "structural_empirical_admission_id": admission_id,
        "structural_empirical_admission_content_hash": semantic_hash(material),
        "admission_authority_id": "PRE553_R13_TEST_ONLY_ADMISSION_AUTHORITY_STUB",
        "admission_authority_version": "test-only-1",
        "admission_authority_hash": _h("admission-authority-stub"),
        "admission_decision_state": decision_state,
        "focal_structural_proposition_ref": f"prop:{tag}",
        "structural_semantic_identity_refs": [f"struct:{tag}"],
        "native_scope_identity_refs": [f"scope:{tag}"],
        "target_use_permission_refs": [f"permission:{tag}"],
        "effective_time_or_interval_refs_required_by_target_use": [f"time:{tag}"],
        "source_universe_refs": [source_universe],
        "estimand_refs": [f"estimand:{tag}"],
        "measure_and_weight_authority_refs": [f"measure:{tag}"],
        "applicable_negative_denial_noncomparability_refs": list(negative_refs),
        "interpretation_critical_authority_refs": [f"interpretation-authority:{tag}"],
        "producer_replay_locator_or_reference_root": f"replay:admission:{tag}",
    }


def validate_admission_fixture(admission: Mapping[str, Any]) -> None:
    if not isinstance(admission, Mapping) or set(admission) != ADMISSION_SHAPE_FIELDS:
        raise HarnessFixtureError("admission fixture must match exact StructuralEmpiricalAdmission-shaped field set")
    _assert_sha(admission["structural_empirical_admission_content_hash"], "admission content hash")
    _assert_sha(admission["admission_authority_hash"], "admission authority hash")
    for name in (
        "structural_semantic_identity_refs", "native_scope_identity_refs", "target_use_permission_refs",
        "source_universe_refs", "estimand_refs", "measure_and_weight_authority_refs",
        "interpretation_critical_authority_refs",
    ):
        _assert_string_sequence(admission[name], name, nonempty=True)
    _assert_string_sequence(
        admission["effective_time_or_interval_refs_required_by_target_use"],
        "effective_time_or_interval_refs_required_by_target_use",
    )
    _assert_string_sequence(
        admission["applicable_negative_denial_noncomparability_refs"],
        "applicable_negative_denial_noncomparability_refs",
    )


def make_v553_stub(
    admission: Mapping[str, Any], *, tag: str, scr553_decision_state: str,
    temporal_completeness: str, include_candidate: bool,
    condition_kinds: Sequence[str] = (),
) -> dict[str, Any]:
    """Build a literal V553 seam stub; no empirical or structural interpretation occurs."""
    validate_admission_fixture(admission)
    source = admission["source_universe_refs"][0]
    eq = {
        "focal_structural_proposition_ref": admission["focal_structural_proposition_ref"],
        "target_use": "STRUCTURAL_MEDIATION_INPUT",
        "v554_rule_id": V554_RULE_STUB["id"],
        "v554_rule_version": V554_RULE_STUB["version"],
        "v554_rule_hash": V554_RULE_STUB["hash"],
        "rule_relevant_structural_semantic_identity_fingerprint": admission["structural_semantic_identity_refs"][0],
        "native_scope_identity_fingerprint": admission["native_scope_identity_refs"][0],
        "rule_relevant_effective_time_semantics_fingerprint": admission["effective_time_or_interval_refs_required_by_target_use"][0],
        "originating_structural_empirical_admission_lineage_fingerprint": admission["structural_empirical_admission_id"],
        "source_universe_fingerprint": source,
        "estimand_fingerprint": admission["estimand_refs"][0],
        "measure_and_weight_authority_fingerprint": admission["measure_and_weight_authority_refs"][0],
        "rule_relevant_source_relation_comparability_authority_fingerprint": f"comparability:{source}",
        "interpretation_critical_semantic_authority_fingerprint": admission["interpretation_critical_authority_refs"][0],
    }
    candidates: list[dict[str, Any]] = []
    if include_candidate:
        v553_material = {
            "fixture_only": True,
            "tag": tag,
            "originating_admission_ref": admission["structural_empirical_admission_id"],
            "source_universe": source,
            "temporal_families": ["TEMPORAL_KEY", "TEMPORAL_OBSERVATION"],
        }
        object_hash = semantic_hash(v553_material)
        object_id = f"urn:rawlsing:test:pre553-r13:v553:{object_hash}"
        projection = {
            "v553_object_id": object_id,
            "v553_object_content_hash": object_hash,
            "v553_object_family": "TEMPORAL_OBSERVATION",
            "originating_structural_empirical_admission_refs": [admission["structural_empirical_admission_id"]],
            "focal_structural_proposition_ref": admission["focal_structural_proposition_ref"],
            "rule_relevant_temporal_semantic_refs": ["TEMPORAL_KEY", "TEMPORAL_OBSERVATION"],
            "native_scope_identity_refs": list(admission["native_scope_identity_refs"]),
            "source_universe_refs": list(admission["source_universe_refs"]),
            "estimand_refs": list(admission["estimand_refs"]),
            "measure_and_weight_authority_refs": list(admission["measure_and_weight_authority_refs"]),
            "source_relation_comparability_authority_refs_where_required": [f"comparability:{source}"],
            "applicable_temporal_limit_negative_refs": list(admission["applicable_negative_denial_noncomparability_refs"]),
            "interpretation_critical_authority_refs": list(admission["interpretation_critical_authority_refs"]),
            "producer_replay_locator_or_reference_root": f"replay:v553:{tag}",
        }
        candidates.append({
            "basis_kind": BasisKind.V553.value,
            "basis_ref": {"kind": BasisKind.V553.value, "object_id": object_id, "content_hash": object_hash},
            "projection": projection,
            "projection_hash": semantic_hash(projection),
            "equivalence_key": eq,
            "selected_rule_relevant_basis_semantics": v553_material,
            "v553_families": ["TEMPORAL_KEY", "TEMPORAL_OBSERVATION"],
            "all_relation_required_support_limit_refs": False,
        })
    conditions = [
        {
            "candidate_semantic_key": f"fixture-candidate:{tag}",
            "condition_kind_id": kind,
            "predicate_id": f"PRE553-R13-{kind}",
            "predicate_version": "test-only-1",
            "semantic_owner": "V554",
            "resolution_owner": "V554",
            "binding_producer": "V554",
            "evaluator_owner": "V554",
            "canonical_argument_envelope_fingerprint": f"args:{tag}:{kind}",
            "producer_negative_or_requirement_refs": [f"negative:{tag}:{kind}"],
        }
        for kind in condition_kinds
    ]
    return {
        "tag": tag,
        "scr553_decision_state": scr553_decision_state,
        "temporal_completeness": temporal_completeness,
        "candidates": candidates,
        "conditions": conditions,
        "equivalence_key": eq,
    }


def build_m1_invocation(admission: Mapping[str, Any], v553_stub: Mapping[str, Any]) -> dict[str, Any]:
    validate_admission_fixture(admission)
    if not isinstance(v553_stub, Mapping):
        raise HarnessFixtureError("V553 stub must be mapping")
    candidates = list(v553_stub.get("candidates", ()))
    decision = admission["admission_decision_state"]
    if decision != "ADMITTED" and candidates:
        raise HarnessFixtureError("nonpositive admission fixture may not carry a positive V553 candidate")
    if decision != "ADMITTED" and v553_stub.get("scr553_decision_state") != "NO_POSITIVE_V553_OUTPUT__ADMISSION_NOT_POSITIVE":
        raise HarnessFixtureError("nonpositive admission must remain explicitly nonpositive at V553 seam")
    tag = str(v553_stub.get("tag", "fixture"))
    payload = {
        "governed_use_id": f"PRE553-R13-USE:{tag}",
        "use_owner": "V554",
        "v554_rule_ref": dict(V554_RULE_STUB),
        "signature_id": SIG_002,
        "target_use": "STRUCTURAL_MEDIATION_INPUT",
        "focal_structural_proposition_ref": admission["focal_structural_proposition_ref"],
        "originating_admission_refs": [admission["structural_empirical_admission_id"]],
        "scr553_decision_state": v553_stub["scr553_decision_state"],
        "scr553_request_ref": _ref("V553TemporalizationRequest", f"pre553-r13:{tag}"),
        "required_temporal_operations": ["EXPRESS_TIME_SCOPED_OBSERVATION"],
        "required_authority_snapshot_refs": ["PRE553_R13_TEST_ONLY_AUTHORITY_SNAPSHOT"],
        "temporal_completeness": v553_stub["temporal_completeness"],
        "candidates": candidates,
        "conditions": list(v553_stub.get("conditions", ())),
        "authority_bundle_material": {
            "fixture_only": True,
            "semantic_authority": False,
            "assignment": ASSIGNMENT_ID,
            "admission_authority_ref": {
                "id": admission["admission_authority_id"],
                "version": admission["admission_authority_version"],
                "hash": admission["admission_authority_hash"],
            },
        },
        "producer_reference_spine_fingerprint": f"pre553-r13-spine:{tag}",
        "publication_authority": {
            "authority_id": "PRE553_R13_TEST_ONLY_V554_PUBLICATION_STUB",
            "authority_version": "test-only-1",
            "authority_hash": _h("v554-publication-stub"),
            "producer": "V554",
            "publisher": "V557",
            "governed_use_id": f"PRE553-R13-USE:{tag}",
            "rule_ref": dict(V554_RULE_STUB),
            "decision": "AUTHORIZED",
            "allowed_object_families": ["F1", "F2", "B1"],
        },
    }
    return payload


def evaluate_ingress(admission: Mapping[str, Any], v553_stub: Mapping[str, Any]) -> M1Evaluation:
    return evaluate_m1_temporal_v554_admission_dedup(build_m1_invocation(admission, v553_stub))


def _route_request(m1: M1Evaluation, tag: str) -> dict[str, Any]:
    if m1.f1 is None:
        return {}
    f1_ref = {"kind": "F1", "object_id": m1.f1["f1_id"], "content_hash": semantic_hash(m1.f1)}
    closure_material = {
        "f1_id": f1_ref["object_id"],
        "f1_content_hash": f1_ref["content_hash"],
        "source_structural_position_ref": _ref("StructuralPosition", f"source-position:{tag}"),
        "structural_channel_ref": _ref("StructuralChannel", f"channel:{tag}"),
        "receiving_structural_position_ref": _ref("StructuralPosition", f"receiver-position:{tag}"),
        "closure_authority_ref": _ref("V554ReferenceClosure", f"closure-authority:{tag}"),
    }
    closure = {**closure_material, "closure_content_hash": semantic_hash(closure_material)}
    return {
        "route_authority_ref": {"id": ROUTE_AUTHORITY_ID, "version": ROUTE_AUTHORITY_VERSION, "content_hash": _h("v555-route-registry-stub")},
        "route_rule_ref": {"id": ROUTE_RULE_ID, "version": ROUTE_RULE_VERSION, "content_hash": _h("v555-route-rule-stub")},
        "route_shape_ref": {"id": ROUTE_SHAPE_ID, "version": ROUTE_SHAPE_VERSION, "content_hash": _h("v555-route-shape-stub")},
        "f1_reference_closure": closure,
        "channel_structural_role_id": CHANNEL_STRUCTURAL_ROLE_ID,
        "receiving_constraint_kind": RECEIVING_CONSTRAINT_KIND,
        "producer_allowed_uses": ["REVIEW"],
        "v556_higher_order_semantics_required": True,
        "v557_publication_authority": None,
    }


def evaluate_route(m1: M1Evaluation, *, tag: str) -> M2Evaluation:
    return evaluate_m2_v555_atomic_route(m1, _route_request(m1, tag))


def _route_ref(m2: M2Evaluation) -> dict[str, str]:
    if m2.decision_state is not M2DecisionState.ROUTE_CANDIDATE_AUTHORIZED or m2.route is None:
        raise HarnessFixtureError("positive V556 harness requires exact positive V555 routes")
    return {
        "kind": V555_SEMANTIC_FAMILY,
        "object_id": m2.route["route_id"],
        "content_hash": semantic_hash(m2.route),
    }


def _v556_result_schema_stub() -> dict[str, Any]:
    return {
        "schema_id": "PRE553_R13_TEST_ONLY_OBJECTIVE_TOPOLOGY",
        "schema_version": "2.0.0",
        "semantic_class": "OBJECTIVE_STRUCTURAL_RESULT",
        "root": {
            "type": "object",
            "semantic_role": "OBJECTIVE_GROUPING",
            "fields": {
                "topology_kind": {
                    "type": "string",
                    "semantic_role": "OBJECTIVE_STRUCTURAL_RELATION",
                    "allowed_values_or_unbounded_marker": ["PRE553_R13_EXACT_PAIR_FIXTURE"],
                },
            },
            "required": ["topology_kind"],
            "additional_fields": False,
        },
    }


def _v556_result_contract_stub(rule_id: str, rule_version: str) -> tuple[dict[str, Any], dict[str, str]]:
    schema = _v556_result_schema_stub()
    schema_ref = {
        "kind": RESULT_SCHEMA_REF_KIND,
        "object_id": f"{schema['schema_id']}@{schema['schema_version']}",
        "content_hash": semantic_hash(schema),
    }
    material = {
        "contract_id": M3_CONTRACT_ID,
        "binding_id": "PRE553_R13_TEST_ONLY_V556_RESULT_BINDING",
        "binding_version": "2.0.0",
        "authorization_state": "AUTHORIZED_CURRENT",
        "bound_rule_id": rule_id,
        "bound_rule_version": rule_version,
        "result_schema_ref": schema_ref,
        "result_semantic_owner_ref": _ref("M3_RESULT_SEMANTIC_OWNER", "PRE553_R13_TEST_ONLY_OBJECTIVE_OWNER"),
        "result_semantic_owner_current_selection_ref": _ref(
            "M3_RESULT_OWNER_CURRENT_SELECTION", "PRE553_R13_TEST_ONLY_OBJECTIVE_OWNER_CURRENT"
        ),
        "semantic_jurisdiction": RESULT_JURISDICTION,
        "actor_indexing_mode": "NO_ACTOR_INDEX",
        "person_state_semantics": PERSON_STATE_SEMANTICS,
        "result_schema": schema,
    }
    binding_hash = semantic_hash(material)
    binding = {k: v for k, v in material.items() if k != "contract_id"}
    binding["binding_content_hash"] = binding_hash
    binding_ref = {
        "kind": RESULT_CONTRACT_BINDING_REF_KIND,
        "object_id": f"{binding['binding_id']}@{binding['binding_version']}",
        "content_hash": binding_hash,
    }
    return binding, binding_ref


def v556_rule_stub() -> dict[str, Any]:
    rule_id = "PRE553_R13_TEST_ONLY_V556_PAIR_RULE"
    rule_version = "test-only-2"
    _, result_ref = _v556_result_contract_stub(rule_id, rule_version)
    body_material = {
        "contract_id": M3_CONTRACT_ID,
        "rule_id": rule_id,
        "rule_version": rule_version,
        "semantic_family": "V556_TOPOLOGY",
        "participant_roles": ["SOURCE_SIDE", "RECEIVER_SIDE"],
        "participant_order_policy": "ORDERED",
        "minimum_cardinality": 2,
        "maximum_cardinality_or_unbounded_marker": 2,
        "multiplicity_policy": "EXACT_OCCURRENCE_INDEX",
        "same_route_reuse_policy": "FORBIDDEN",
        "source_composition_policy": "NONE_BY_DEFAULT",
        "allowed_typed_outcome_states": sorted({
            "SUPPORTED", "VALID_EMPTY", "DENIED", "NONCOMPARABLE", "CONFLICTING_AUTHORITY"
        }),
        "producer_allowed_uses": ["REVIEW"],
        "result_contract_binding_ref": result_ref,
    }
    return {
        "authority_id": "PRE553_R13_TEST_ONLY_V556_AUTHORITY_STUB",
        "authority_version": "test-only-2",
        "authority_content_hash": _h("v556-authority-stub-r2"),
        **{k: v for k, v in body_material.items() if k != "contract_id"},
        "rule_content_hash": semantic_hash(body_material),
    }

def _rule_key(rule: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(rule[k] for k in (
        "authority_id", "authority_version", "authority_content_hash",
        "rule_id", "rule_version", "rule_content_hash",
    ))


def _source_ref(source_universe: str) -> dict[str, str]:
    return _ref("SourceUniverse", source_universe)


def v556_bindings(routes: Sequence[M2Evaluation], sources: Sequence[str]) -> list[dict[str, Any]]:
    if len(routes) != 2 or len(sources) != 2:
        raise HarnessFixtureError("first-tranche R13 fixture requires exactly two route occurrences")
    return [
        {
            "v555_route_identity_ref": _route_ref(route),
            "role": role,
            "ordinal_or_null": ordinal,
            "multiplicity_index": 0,
            "source_universe_ref": _source_ref(source),
        }
        for route, source, role, ordinal in zip(
            routes, sources, ("SOURCE_SIDE", "RECEIVER_SIDE"), (1, 2)
        )
    ]


def make_source_composition_stub(bindings: Sequence[Mapping[str, Any]], *, decision: str) -> dict[str, Any]:
    return {
        "authority_id": "PRE553_R13_TEST_ONLY_SOURCE_COMPOSITION_STUB",
        "authority_version": "test-only-1",
        "authority_content_hash": _h(f"source-composition:{decision}"),
        "operation_id": "PRE553_R13_TEST_ONLY_COMPOSE_ROUTES",
        "covered_source_universe_refs": [dict(x["source_universe_ref"]) for x in bindings],
        "covered_participant_bindings": [
            {k: x[k] for k in ("v555_route_identity_ref", "role", "ordinal_or_null", "multiplicity_index")}
            for x in bindings
        ],
        "compatibility_scope": "EXACT_PARTICIPANTS",
        "decision": decision,
    }


def _composition_key(value: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(value[k] for k in (
        "authority_id", "authority_version", "authority_content_hash", "operation_id"
    ))


def evaluate_v556(
    routes: Sequence[M2Evaluation], sources: Sequence[str], *,
    governed_state: str = "SUPPORTED",
    composition: Mapping[str, Any] | None = None,
) -> M3Evaluation:
    rule = v556_rule_stub()
    result_contract, result_ref = _v556_result_contract_stub(rule["rule_id"], rule["rule_version"])
    if rule["result_contract_binding_ref"] != result_ref:
        raise HarnessFixtureError("R2 result-contract stub does not match rule binding reference")
    bindings = v556_bindings(routes, sources)
    request = {
        "higher_order_semantics_required": True,
        "rule_authority": rule,
        "participant_bindings": bindings,
        "source_composition_authority": composition,
        "result_contract_binding": result_contract,
        "governed_result": {
            "state": governed_state,
            "semantic_payload": {"topology_kind": "PRE553_R13_EXACT_PAIR_FIXTURE"},
        },
        "intended_use": "REVIEW",
    }
    active_composition = [_composition_key(composition)] if composition is not None else []
    return evaluate_m3_v556_higher_order_structural(
        routes,
        request,
        active_rule_keys=[_rule_key(rule)],
        active_source_composition_keys=active_composition,
        active_result_contract_refs=[result_ref],
    )


@dataclass(frozen=True)
class LaneArtifacts:
    admission: Mapping[str, Any]
    v553_stub: Mapping[str, Any]
    m1: M1Evaluation
    m2: M2Evaluation
    source_universe: str


@dataclass(frozen=True)
class ReservoirArtifacts:
    lanes: tuple[LaneArtifacts, LaneArtifacts]
    m3: M3Evaluation
    publication: Any
    repository: Any
    entries: tuple[RepositoryEntry, ...]
    reference_edges: tuple[Any, ...]
    root_entry: RepositoryEntry
    resolution: Any


def run_lane(admission: Mapping[str, Any], v553_stub: Mapping[str, Any], *, tag: str) -> LaneArtifacts:
    m1 = evaluate_ingress(admission, v553_stub)
    m2 = evaluate_route(m1, tag=tag)
    return LaneArtifacts(admission, v553_stub, m1, m2, admission["source_universe_refs"][0])


def _entry_for_object(obj: Any, *, tag: str) -> RepositoryEntry:
    governance = govern_v557(
        obj,
        decision_state=V557DecisionState.ALLOW_REVIEW_ONLY,
        v557_allowed_uses=("REVIEW",),
        authority_ref=AuthorityRef(
            "PRE553_R13_TEST_ONLY_V557_GOVERNANCE_STUB",
            "test-only-1",
            _h("v557-governance-stub"),
        ),
    )
    locator = make_producer_locator(
        obj,
        governance,
        logical_collection_kind=f"PRE553_R13_{obj.producer_family}",
        authoritative_build_id=f"PRE553-R13-BUILD:{tag}",
        authoritative_build_hash=_h(f"build:{tag}"),
        producer_contract_id=f"PRE553_R13_TEST_ONLY_{obj.producer_family}_CONTRACT_STUB",
        producer_contract_version="test-only-1",
        producer_contract_hash=_h(f"producer-contract:{obj.producer_family}"),
        producer_rule_bindings=(AuthorityRef(
            "PRE553_R13_TEST_ONLY_PRODUCER_RULE_STUB", "test-only-1", _h("producer-rule-stub")
        ),),
        provenance_locator=f"audit://pre553-r13/{tag}",
    )
    return RepositoryEntry(obj, governance, locator)


def build_positive_repository(lanes: Sequence[LaneArtifacts]) -> ReservoirArtifacts:
    if len(lanes) != 2:
        raise HarnessFixtureError("positive V556 reservoir harness requires exactly two lanes")
    if any(x.m1.decision_state is not M1DecisionState.ELIGIBLE for x in lanes):
        raise HarnessFixtureError("positive repository build requires M1 ELIGIBLE on both lanes")
    if any(x.m2.decision_state is not M2DecisionState.ROUTE_CANDIDATE_AUTHORIZED for x in lanes):
        raise HarnessFixtureError("positive repository build requires exact positive V555 routes")
    m3 = evaluate_v556(
        [x.m2 for x in lanes], [x.source_universe for x in lanes], governed_state="SUPPORTED"
    )
    if m3.decision_state is not M3DecisionState.SUPPORTED or m3.v556_object is None:
        raise HarnessFixtureError(f"positive same-source V556 fixture failed: {m3.decision_state}: {m3.reason}")

    structural_objects = []
    for lane in lanes:
        group = structural_objects_from_m1(lane.m1, producer_allowed_uses=("REVIEW",))
        if not group:
            raise HarnessFixtureError("M1 fixture did not expose exact frozen V554 publication objects")
        structural_objects.extend(group)
    route_objects = [structural_object_from_m2(x.m2, require_direct_handoff=False) for x in lanes]
    structural_objects.extend(route_objects)
    v556_object = structural_object_from_m3(m3)
    structural_objects.append(v556_object)

    entries = tuple(
        _entry_for_object(obj, tag=f"{i}:{obj.producer_family}:{obj.object_id}")
        for i, obj in enumerate(structural_objects)
    )
    by_object = {(e.obj.semantic_class, e.obj.object_id, e.obj.content_hash): e for e in entries}

    def target_for(ref: Any) -> RepositoryEntry:
        if isinstance(ref, Mapping):
            key = (ref["kind"], ref["object_id"], ref["content_hash"])
        else:
            key = (ref.kind, ref.object_id, ref.content_hash)
        if key not in by_object:
            raise HarnessFixtureError(f"missing exact repository dependency for {key!r}")
        return by_object[key]

    ref_contract = AuthorityRef(
        "PRE553_R13_TEST_ONLY_REFERENCE_CONTRACT_STUB",
        "test-only-1",
        _h("reference-contract-stub"),
    )
    edges = []
    for route_obj in route_objects:
        route_entry = by_object[(route_obj.semantic_class, route_obj.object_id, route_obj.content_hash)]
        for dep in (*route_obj.required_dependency_refs, *route_obj.negative_dependency_refs):
            target = target_for(dep)
            edges.append(make_reference_edge(
                route_entry.locator,
                target.locator,
                reference_contract=ref_contract,
                edge_role=f"V555_{dep.kind}_DEPENDENCY",
            ))

    root_entry = by_object[(v556_object.semantic_class, v556_object.object_id, v556_object.content_hash)]
    cardinality = str(v556_object.payload["rule_authority"]["minimum_cardinality"])
    for binding in m3.canonical_participant_bindings:
        target = target_for(binding["v555_route_identity_ref"])
        ordinal = binding["ordinal_or_null"]
        edges.append(make_reference_edge(
            root_entry.locator,
            target.locator,
            reference_contract=ref_contract,
            edge_role="PARTICIPANT",
            participant_role=binding["role"],
            declared_cardinality=cardinality,
            multiplicity_key=str(binding["multiplicity_index"]),
            order_significant=ordinal is not None,
            semantic_ordinal=ordinal,
        ))

    publication = build_v557_publication_bundle((V557PublicationEntry(root_entry.obj, root_entry.governance),))
    repository = build_v558_repository_bundle(publication, entries, reference_edges=tuple(edges))
    query = make_context_query((ContextQueryItem(exact_resolution_key(root_entry.locator), ("REVIEW",)),))
    resolution = resolve_v558(repository, query)
    return ReservoirArtifacts(tuple(lanes), m3, publication, repository, entries, tuple(edges), root_entry, resolution)


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
