"""Hostile exact-query fixture/oracle pack for PRE553 Wave-03 R12.

Test-only. This module deliberately reuses the accepted I03 sealed-C11 fixture
builders so R12 probes the accepted public executor rather than inventing a
parallel empirical substrate. No discovery, structural admission, V553,
generated-person, actor/V3/V2, deployment, or cutover semantics live here.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Mapping

from rawlsing_next.pre553_c11_ingest import (
    INGEST_CONTRACT_VERSION, C11SourceReleaseCandidate, SourceReleaseManifest,
    build_candidate_replay_manifest, ingest_c11_source_release,
)
from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, RespondentIdentity, TypedAbsence
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalCoordinateFact, EmpiricalQuerySpec, EmpiricalUniverse,
    RespondentEvent, RoutingEligibilityFact, make_empirical_predicate,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.tests.test_pre553_empirical_query import (
    _auth, _branch_predicate, _build_source, _cell_map, _coordinate_leaf,
    _h, _predicate, _query, _query_authority, _ref, _response_leaf, _run,
)


@dataclass(frozen=True)
class FixtureOracle:
    fixture_id: str
    frontier: tuple[str, ...]
    expected: Mapping[str, Any]
    loss_signature: str


FIXTURE_ORACLES: Mapping[str, FixtureOracle] = {
    "XOR_ZERO_UNARY": FixtureOracle(
        "XOR_ZERO_UNARY", ("XOR", "ZERO_UNARY_SIGNAL", "SAME_RESPONDENT", "K_WAY_JOINT"),
        {
            "X0_Z1": (1, 2), "X1_Z1": (1, 2), "Y0_Z1": (1, 2), "Y1_Z1": (1, 2),
            "XOR_Z1": (2, 2), "JOINT_DENOMINATOR": 4,
            "JOINT_SUPPORTED": {
                ("0", "0", "0"): 1, ("0", "1", "1"): 1,
                ("1", "0", "1"): 1, ("1", "1", "0"): 1,
            },
            "JOINT_ZERO": {
                ("0", "0", "1"), ("0", "1", "0"),
                ("1", "0", "0"), ("1", "1", "1"),
            },
        },
        "Any unary-ranking prerequisite loses the exact XOR relation even though the same-respondent joint determines Z.",
    ),
    "SIMPSON_REVERSAL": FixtureOracle(
        "SIMPSON_REVERSAL", ("SIMPSON_REVERSAL", "CONDITION_IDENTITY", "DENOMINATOR_IDENTITY"),
        {"pooled_X1": (5, 13), "pooled_X0": (8, 12), "A_X1": (3, 3), "A_X0": (8, 10), "B_X1": (2, 10), "B_X0": (0, 2)},
        "Pooling erases the exact conditioning coordinate and reverses the within-stratum direction.",
    ),
    "SAME_MARGINALS_DIFFERENT_JOINT": FixtureOracle(
        "SAME_MARGINALS_DIFFERENT_JOINT", ("SAME_MARGINALS_DIFFERENT_JOINT", "SOURCE_INDEXED", "JOINT"),
        {
            "left": {("0", "0"): 2, ("0", "1"): 0, ("1", "0"): 0, ("1", "1"): 2},
            "right": {("0", "0"): 0, ("0", "1"): 2, ("1", "0"): 2, ("1", "1"): 0},
            "marginal_X0": 2, "marginal_Y0": 2, "denominator": 4,
        },
        "Marginal equality cannot identify a joint fact; respondent pairings differ exactly.",
    ),
    "RESPONSE_POSITION_CONJUNCTION": FixtureOracle(
        "RESPONSE_POSITION_CONJUNCTION", ("RESPONSE_X_POSITION", "ARBITRARY_CONJUNCTION", "SAME_RESPONDENT"),
        {"denominator": 1, "Y1": 1, "member_ids": ("R1",)},
        "Independent response/coordinate marginals would fabricate members not satisfying both predicates on the same respondent.",
    ),
    "RESPONSE_RESPONSE_COTRAVEL": FixtureOracle(
        "RESPONSE_RESPONSE_COTRAVEL", ("RESPONSE_RESPONSE", "SAME_RESPONDENT_COTRAVEL"),
        {"denominator": 3, "Y1": 2, "Y0": 1, "member_ids": ("R1", "R2", "R3")},
        "Aggregate co-occurrence cannot replace exact same-respondent incidence.",
    ),
    "ROUTING_RISK_ASYMMETRY": FixtureOracle(
        "ROUTING_RISK_ASYMMETRY", ("ROUTING", "RISK_SET", "DENOMINATOR_ASYMMETRY", "JOINT"),
        {"X_denominator": 3, "Y_denominator": 3, "joint_denominator": 2, "joint_member_ids": ("R2", "R3")},
        "Equal per-target denominator counts do not imply equal/common member sets; the lawful joint denominator is the exact intersection.",
    ),
    "RAW_WEIGHTED_DIVERGENCE": FixtureOracle(
        "RAW_WEIGHTED_DIVERGENCE", ("RAW", "AUTHORIZED_WEIGHTED", "MEASURE_IDENTITY"),
        {"raw_denominator": 2, "raw_Y1": 1, "weighted_denominator": {"$exact_fraction": [4, 1]}, "weighted_Y1": {"$exact_fraction": [3, 1]}},
        "Raw and governed-weighted measures are distinct exact facts even over the same respondent member set.",
    ),
    "OBSERVED_ZERO_VS_ZERO_SUPPORT": FixtureOracle(
        "OBSERVED_ZERO_VS_ZERO_SUPPORT", ("OBSERVED_ZERO", "ZERO_SUPPORT", "TYPED_ZERO"),
        {"observed_state": "SUPPORTED", "observed_denominator": 2, "Y1_cell_state": "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET", "zero_support_state": "ZERO_SUPPORT", "zero_support_denominator": 0},
        "Zero numerator inside positive support must never collapse with absence of denominator support.",
    ),
    "SPECIAL_STATE_NONCOLLAPSE": FixtureOracle(
        "SPECIAL_STATE_NONCOLLAPSE", ("MISSING", "DK", "REFUSAL", "IAP", "NOT_ASKED", "TYPED_ABSENCE"),
        {
            "eligible_denominator": 4,
            "eligible_cells": {"1": 1, "MISSING": 1, "DK": 1, "REFUSAL": 1, "IAP": 0, "NOT_ASKED": 0},
            "carrier_states": ("DK", "IAP", "MISSING", "NOT_ASKED", "REFUSAL", "SUBSTANTIVE_RESPONSE"),
            "routing_states": ("ELIGIBLE_APPLICABLE", "INAPPLICABLE", "NOT_ASKED"),
        },
        "Typed special responses and routing exclusions remain explicit; missing rows are never allowed to stand in for these states.",
    ),
    "SOURCE_INDEXED_DISAGREEMENT": FixtureOracle(
        "SOURCE_INDEXED_DISAGREEMENT", ("SOURCE_INDEXED", "SOURCE_DISAGREEMENT", "NO_POOLING"),
        {"left": {"denominator": 2, "Y1": 2, "Y0": 0}, "right": {"denominator": 2, "Y1": 0, "Y0": 2}},
        "Equal question labels do not authorize source pooling; disagreement must remain source-indexed.",
    ),
    "MULTI_UNIVERSE_NONCOMPARABLE": FixtureOracle(
        "MULTI_UNIVERSE_NONCOMPARABLE", ("MULTI_UNIVERSE", "NONCOMPARABLE", "COMPOSITION_AUTHORITY"),
        {"typed_state": "NONCOMPARABLE", "p02_failure_state": "UNRESOLVED_SOURCE_RELATION", "raw_denominator": 0},
        "A requested composite without operation-specific pooling/nonduplication/estimand authority must fail closed rather than silently pool.",
    ),
    "ORDERED_RANKED_MULTIPLICITY": FixtureOracle(
        "ORDERED_RANKED_MULTIPLICITY", ("ORDERED_SEQUENCE", "RANKED_RESPONSE", "REPEATED_EVENT", "TOPOLOGY"),
        {
            "ordered": ["A", "B"], "ranked": ["HIGH", "LOW"],
            "repeated": [
                {"event_id": "M-1", "multiplicity_order_rank_fields": {"kind": "REPEATED_EVENT", "multiplicity_index": 0}, "value": "A"},
                {"event_id": "M-2", "multiplicity_order_rank_fields": {"kind": "REPEATED_EVENT", "multiplicity_index": 1}, "value": "A"},
            ],
        },
        "Scalar collapse loses semantic order, rank, repeated occurrence identity and multiplicity.",
    ),
    "K_WAY_BOUNDED_JOINT": FixtureOracle(
        "K_WAY_BOUNDED_JOINT", ("K_WAY", "PARITY", "BOUNDED_JOINT"),
        {"arity": 4, "denominator": 8, "domain_cells": 16, "supported_cells": 8, "zero_cells": 8},
        "All lower-order views can miss a bounded higher-order parity relation; the exact 4-way topology must survive.",
    ),
}
FIXTURE_INVENTORY = tuple(FIXTURE_ORACLES)


def _rate(fact):
    return _cell_map(fact)["1"]["raw_numerator_support"], fact.raw_denominator_support


def _ids_from_fact(fact, source):
    by_ref = {respondent.ref.object_id: rid for rid, respondent in source["respondents"].items()}
    return tuple(sorted(by_ref[ref["object_id"]] for ref in fact.denominator_member_refs))


def _multi_source_predicate(left, right, qa, *, tag):
    members = tuple(left["respondents"].values()) + tuple(right["respondents"].values())
    refs = tuple(sorted((member.ref for member in members), key=lambda ref: ref.key))
    return make_empirical_predicate(
        predicate_ast={
            "op": "LEAF", "leaf_type": "DERIVED_BRANCH_COHORT", "branch_definition_id": f"R12-{tag}",
            "resolved_predicate_hash_or_exact_membership_ref": _ref("BRANCH_MEMBERSHIP", f"r12-{tag}"),
            "parent_ancestry_ref": _ref("BRANCH_PARENT", f"r12-{tag}"),
            "branch_algorithm_authority_ref": qa.authority_ref,
            "branch_membership_replay_ref": _ref("BRANCH_REPLAY", f"r12-{tag}"),
            "branch_source_scope_ref": _ref("SOURCE_SCOPE", f"r12-{tag}"),
            "exact_member_respondent_refs": refs,
        },
        typed_state="PREDICATE_RESOLVED_AUTHORIZED", authority_snapshot_refs=(qa.authority_ref,),
        dependency_refs=(), producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"r12-predicate-{tag}"),
        grammar_authority_ref=qa.authority_ref, coordinate_question_value_refs=(),
        risk_set_refs=(left["risk_refs"]["R"],), scope_refs=(left["universe"].ref, right["universe"].ref),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(_ref("OPERATOR_SEMANTICS", "BOOLEAN-AND-OR-NOT"),),
    )


def _combined_repo(left, right):
    return C11Repository((left["repo"].resolve_release_exact(left["release_ref"]), right["repo"].resolve_release_exact(right["release_ref"])))


def xor_zero_unary_fixture():
    source = _build_source("r12-xor", [
        {"id": "R00", "responses": {"X": 0, "Y": 0, "Z": 0}}, {"id": "R01", "responses": {"X": 0, "Y": 1, "Z": 1}},
        {"id": "R10", "responses": {"X": 1, "Y": 0, "Z": 1}}, {"id": "R11", "responses": {"X": 1, "Y": 1, "Z": 0}},
    ])
    qa = _query_authority("r12-xor")
    facts = {}
    for var in ("X", "Y"):
        for value in (0, 1):
            pred = _predicate(source, qa, _response_leaf(source, qa, var, value), tag=f"{var}{value}")
            facts[f"{var}{value}"] = _run(source, qa, pred, _query(source, qa, pred, ("Z",), tag=f"{var}{value}")).facts[0]
    x, y = _response_leaf(source, qa, "X", 1), _response_leaf(source, qa, "Y", 1)
    xor_pred = _predicate(source, qa, {"op": "AND", "children": [{"op": "OR", "children": [x, y]}, {"op": "NOT", "children": [{"op": "AND", "children": [x, y]}]}]}, tag="xor")
    xor_fact = _run(source, qa, xor_pred, _query(source, qa, xor_pred, ("Z",), tag="xor")).facts[0]
    all_pred = _branch_predicate(source, qa, tag="all")
    joint = _run(source, qa, all_pred, _query(source, qa, all_pred, ("X", "Y", "Z"), tag="joint")).facts[0]
    return source, qa, facts, xor_fact, joint


def simpson_reversal_fixture():
    rows = []
    for i in range(3): rows.append({"id": f"A1-{i}", "responses": {"X": 1, "Y": 1}, "coords": {"G": "A"}})
    for i in range(8): rows.append({"id": f"A0s-{i}", "responses": {"X": 0, "Y": 1}, "coords": {"G": "A"}})
    for i in range(2): rows.append({"id": f"A0f-{i}", "responses": {"X": 0, "Y": 0}, "coords": {"G": "A"}})
    for i in range(2): rows.append({"id": f"B1s-{i}", "responses": {"X": 1, "Y": 1}, "coords": {"G": "B"}})
    for i in range(8): rows.append({"id": f"B1f-{i}", "responses": {"X": 1, "Y": 0}, "coords": {"G": "B"}})
    for i in range(2): rows.append({"id": f"B0-{i}", "responses": {"X": 0, "Y": 0}, "coords": {"G": "B"}})
    source, qa, facts = _build_source("r12-simpson", rows), _query_authority("r12-simpson"), {}
    for x in (0, 1):
        for group in (None, "A", "B"):
            children = [_response_leaf(source, qa, "X", x)]
            if group is not None: children.append(_coordinate_leaf(source, "G", group))
            ast = children[0] if len(children) == 1 else {"op": "AND", "children": children}
            pred = _predicate(source, qa, ast, tag=f"x{x}-{group or 'pool'}")
            facts[(x, group)] = _run(source, qa, pred, _query(source, qa, pred, ("Y",), tag=f"x{x}-{group or 'pool'}")).facts[0]
    return source, facts


def same_marginals_different_joint_fixture():
    left = _build_source("r12-joint-left", [
        {"id": "R1", "responses": {"X": 0, "Y": 0}}, {"id": "R2", "responses": {"X": 0, "Y": 0}},
        {"id": "R3", "responses": {"X": 1, "Y": 1}}, {"id": "R4", "responses": {"X": 1, "Y": 1}},
    ], question_namespace="r12-joint-shared", risk_namespace="r12-joint-shared")
    right = _build_source("r12-joint-right", [
        {"id": "R1", "responses": {"X": 0, "Y": 1}}, {"id": "R2", "responses": {"X": 0, "Y": 1}},
        {"id": "R3", "responses": {"X": 1, "Y": 0}}, {"id": "R4", "responses": {"X": 1, "Y": 0}},
    ], question_namespace="r12-joint-shared", risk_namespace="r12-joint-shared")
    qa, pred = _query_authority("r12-joint"), None
    pred = _multi_source_predicate(left, right, qa, tag="same-marginals")
    query = _query(left, qa, pred, ("X", "Y"), source_mode="SOURCE_INDEXED_MULTI_UNIVERSE", universe_refs=(left["universe"].ref, right["universe"].ref), tag="same-marginals", target_authority_refs=(left["source_auth"].authority_ref, right["source_auth"].authority_ref))
    result = execute_empirical_query(repository=_combined_repo(left, right), query=query, predicate=pred, authority_registry=AuthorityRegistry((*left["authorities"], *right["authorities"], qa)), release_refs=(left["release_ref"], right["release_ref"]))
    by_u = {fact.empirical_universe_refs[0]["object_id"]: fact for fact in result.facts}
    return left, right, by_u[left["universe"].object_id], by_u[right["universe"].object_id]


def response_position_fixture():
    source = _build_source("r12-response-position", [
        {"id": "R1", "responses": {"X": 1, "Y": 1}, "coords": {"G": "A", "H": 1}},
        {"id": "R2", "responses": {"X": 0, "Y": 0}, "coords": {"G": "A", "H": 0}},
        {"id": "R3", "responses": {"X": 1, "Y": 0}, "coords": {"G": "B", "H": 1}},
    ])
    qa = _query_authority("r12-response-position")
    pred = _predicate(source, qa, {"op": "AND", "children": [_response_leaf(source, qa, "X", 1), _coordinate_leaf(source, "G", "A"), _coordinate_leaf(source, "H", 1)]}, tag="response-position")
    return source, _run(source, qa, pred, _query(source, qa, pred, ("Y",), tag="response-position")).facts[0]


def response_response_cotravel_fixture():
    source = _build_source("r12-cotravel", [
        {"id": "R1", "responses": {"X": 1, "Y": 1}}, {"id": "R2", "responses": {"X": 1, "Y": 1}},
        {"id": "R3", "responses": {"X": 1, "Y": 0}}, {"id": "R4", "responses": {"X": 0, "Y": 1}},
    ])
    qa = _query_authority("r12-cotravel")
    pred = _predicate(source, qa, _response_leaf(source, qa, "X", 1), tag="x1")
    return source, _run(source, qa, pred, _query(source, qa, pred, ("Y",), tag="y-given-x1")).facts[0]


def routing_risk_asymmetry_fixture():
    rows = [{"id": "R1", "responses": {"X": 0, "Y": 0}}, {"id": "R2", "responses": {"X": 0, "Y": 1}}, {"id": "R3", "responses": {"X": 1, "Y": 0}}, {"id": "R4", "responses": {"X": 1, "Y": 1}}]
    source = _build_source("r12-risk", rows, risk_sets={"R": {"X": {"R1", "R2", "R3"}, "Y": {"R2", "R3", "R4"}}})
    qa, pred = _query_authority("r12-risk"), None
    pred = _branch_predicate(source, qa, tag="all")
    return source, _run(source, qa, pred, _query(source, qa, pred, ("X",), tag="x")).facts[0], _run(source, qa, pred, _query(source, qa, pred, ("Y",), tag="y")).facts[0], _run(source, qa, pred, _query(source, qa, pred, ("X", "Y"), tag="xy")).facts[0]


def raw_weighted_divergence_fixture():
    source = _build_source("r12-weight", [{"id": "R1", "responses": {"Y": 0}}, {"id": "R2", "responses": {"Y": 1}}], weights={"R1": ("WEIGHT_VALID_AUTHORIZED", "1"), "R2": ("WEIGHT_VALID_AUTHORIZED", "3")})
    qa, pred = _query_authority("r12-weight"), None
    pred = _branch_predicate(source, qa, tag="all")
    return source, _run(source, qa, pred, _query(source, qa, pred, ("Y",), measure="RAW", tag="raw")).facts[0], _run(source, qa, pred, _query(source, qa, pred, ("Y",), measure="GOVERNED_WEIGHTED", tag="weighted")).facts[0]


def observed_zero_zero_support_fixture():
    source = _build_source("r12-zero", [{"id": "R1", "responses": {"Y": 0}}, {"id": "R2", "responses": {"Y": 0}}])
    qa = _query_authority("r12-zero")
    full, empty = _branch_predicate(source, qa, tag="full"), _branch_predicate(source, qa, members=(), tag="empty")
    return _run(source, qa, full, _query(source, qa, full, ("Y",), tag="observed")).facts[0], _run(source, qa, empty, _query(source, qa, empty, ("Y",), tag="zero-support")).facts[0]


def source_indexed_disagreement_fixture():
    left = _build_source("r12-disagree-left", [{"id": "L1", "responses": {"Y": 1}}, {"id": "L2", "responses": {"Y": 1}}], question_namespace="r12-disagree-shared", risk_namespace="r12-disagree-shared")
    right = _build_source("r12-disagree-right", [{"id": "R1", "responses": {"Y": 0}}, {"id": "R2", "responses": {"Y": 0}}], question_namespace="r12-disagree-shared", risk_namespace="r12-disagree-shared")
    qa = _query_authority("r12-disagree")
    pred = _multi_source_predicate(left, right, qa, tag="disagree")
    query = _query(left, qa, pred, ("Y",), source_mode="SOURCE_INDEXED_MULTI_UNIVERSE", universe_refs=(left["universe"].ref, right["universe"].ref), tag="disagree", target_authority_refs=(left["source_auth"].authority_ref, right["source_auth"].authority_ref))
    result = execute_empirical_query(repository=_combined_repo(left, right), query=query, predicate=pred, authority_registry=AuthorityRegistry((*left["authorities"], *right["authorities"], qa)), release_refs=(left["release_ref"], right["release_ref"]))
    by_u = {fact.empirical_universe_refs[0]["object_id"]: fact for fact in result.facts}
    return left, right, by_u[left["universe"].object_id], by_u[right["universe"].object_id]


def multi_universe_noncomparable_fixture():
    left = _build_source("r12-nc-left", [{"id": "L1", "responses": {"Y": 1}}], question_namespace="r12-nc-shared", risk_namespace="r12-nc-shared")
    right = _build_source("r12-nc-right", [{"id": "R1", "responses": {"Y": 0}}], question_namespace="r12-nc-shared", risk_namespace="r12-nc-shared")
    qa = _query_authority("r12-nc")
    pred = _multi_source_predicate(left, right, qa, tag="noncomparable")
    query = _query(left, qa, pred, ("Y",), source_mode="AUTHORIZED_COMPOSITE", universe_refs=(left["universe"].ref, right["universe"].ref), tag="noncomparable", target_authority_refs=(left["source_auth"].authority_ref, right["source_auth"].authority_ref))
    return execute_empirical_query(repository=_combined_repo(left, right), query=query, predicate=pred, authority_registry=AuthorityRegistry((*left["authorities"], *right["authorities"], qa)), release_refs=(left["release_ref"], right["release_ref"])).facts[0]


def _build_event_source(tag, rows, topology_by_question):
    source_auth = _auth(f"r12-source-{tag}", "SOURCE_SEMANTICS_TOPOLOGY", families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"))
    routing_auth = _auth(f"r12-routing-{tag}", "ROUTING_RISK_SET", families=("RoutingEligibilityFact@1.0.0",))
    coord_auth = _auth(f"r12-coord-{tag}", "COORDINATE_SEMANTICS", families=("EmpiricalCoordinateFact@1.0.0",))
    replay_auth = _auth(f"r12-replay-{tag}", "REPLAY_PROTOCOL", families=("ReplayReceipt@1.0.0",))
    authorities = (source_auth, routing_auth, coord_auth, replay_auth)
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED", authority_snapshot_refs=(source_auth.authority_ref,), dependency_refs=(), producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"r12-universe-{tag}"),
        raw_source_identity=f"R12-RAW-{tag}", source_family="SURVEY", study_product_release=f"R12-STUDY-{tag}/REL-1", instrument_release=f"R12-INST-{tag}", country_geography="US", sampling_geography="US-NATIONAL", raw_wave="W1", canonical_wave_if_governed=None,
        field_or_reference_time="2026-01", target_population_and_sample_frame="ADULTS", sampling_design_regime="DESIGN-R12", respondent_namespace=f"R12-NS-{tag}", source_artifact_import_lineage=f"R12-SOURCE-{tag}", harmonization_authority_ref=None, source_relation_refs=(),
    )
    qrefs = {q: _ref("QUESTION_NATIVE", f"r12-{tag}-{q}") for q in sorted(topology_by_question)}
    risk_ref = _ref("RISK_SET", f"r12-{tag}-R")
    questions = tuple(QuestionVariableBinding(empirical_universe_ref=universe.ref, native_question_ref=qrefs[q], instrument_question_version="1", canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"), component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"), semantic_authority_ref=source_auth.authority_ref, topology_authority_ref=source_auth.authority_ref) for q in sorted(qrefs))
    respondents, events, routing, coords = {}, [], [], []
    for row in rows:
        respondent = RespondentIdentity(empirical_universe_ref=universe.ref, respondent_key=row["id"], source_native_respondent_key_ref_or_typed_absence=_ref("SOURCE_RESPONDENT", f"r12-{tag}-{row['id']}"), identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"))
        respondents[row["id"]] = respondent
        coords.append(EmpiricalCoordinateFact(typed_state="OBSERVED_COORDINATE", authority_snapshot_refs=(coord_auth.authority_ref,), dependency_refs=(), producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"r12-{tag}-{row['id']}-inert"), empirical_universe_ref=universe.ref, scoped_respondent_ref=respondent.ref, native_coordinate_ref=_ref("COORDINATE_NATIVE", f"r12-{tag}-INERT"), canonical_coordinate_ref_if_authorized=None, raw_coordinate_value="1", canonical_coordinate_value_if_authorized=None, unit_category_taxonomy_ref=_ref("UNIT_TAXONOMY", f"r12-{tag}-INERT"), effective_or_reference_time="2026-01", coordinate_state="OBSERVED_COORDINATE", normalization_crosswalk_authority_ref=None, source_semantic_authority_ref=coord_auth.authority_ref))
        for q in sorted(qrefs):
            rstate = row.get("routing", {}).get(q, "ELIGIBLE_APPLICABLE")
            routing.append(RoutingEligibilityFact(typed_state=rstate, authority_snapshot_refs=(routing_auth.authority_ref,), dependency_refs=(), producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"r12-routing-{tag}-{row['id']}-{q}"), empirical_universe_ref=universe.ref, scoped_respondent_ref=respondent.ref, question_or_target_ref=qrefs[q], risk_set_ref=risk_ref, routing_rule_ref=_ref("ROUTING_RULE", f"r12-{tag}-{q}"), applicability_state=rstate, routing_state=rstate, parent_predicate_refs=(), member_set_replay_ref=_ref("MEMBER_SET", f"r12-{tag}-{q}-{rstate}")))
            for ordinal, spec in enumerate(row.get("events", {}).get(q, ())):
                state = spec.get("state", "SUBSTANTIVE_RESPONSE")
                events.append(RespondentEvent(typed_state=state, authority_snapshot_refs=(source_auth.authority_ref,), dependency_refs=(), producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"r12-event-{tag}-{row['id']}-{q}-{ordinal}"), empirical_universe_ref=universe.ref, scoped_respondent_ref=respondent.ref, native_question_ref=qrefs[q], canonical_question_ref_if_authorized=None, component_or_subitem_ref=None, event_group_id=f"R12-GROUP-{tag}-{row['id']}-{q}", response_event_id_or_deterministic_index=spec.get("event_id", f"{row['id']}-{q}-{ordinal}"), raw_response_value=spec.get("value"), canonical_response_value_if_authorized=None, value_transform_authority_ref=None, response_topology_ref=_ref("TOPOLOGY", f"r12-{tag}-{q}-{topology_by_question[q]}"), multiplicity_order_rank_fields={"kind": topology_by_question[q], **spec.get("order_fields", {})}, response_state=state))
    source_hash = _h(f"r12-source-artifact:{tag}")
    counts = {"EmpiricalUniverse": 1, "RespondentIdentity": len(respondents), "QuestionVariableBinding": len(questions), "RespondentEvent": len(events), "RoutingEligibilityFact": len(routing), "EmpiricalCoordinateFact": len(coords), "WeightMeasureFact": 0, "AuthoritySnapshot": len(authorities), "SourceUniverseRelation": 0, "EmpiricalPredicateReplayBinding": 0, "ComparatorReplayBinding": 0, "DiscoveryBranchReplayBinding": 0, "StructuralAdmissionReplayBinding": 0, "ReplayManifest": 1}
    manifest = SourceReleaseManifest(source_artifact_id=f"R12-SOURCE-{tag}", source_artifact_content_hash=source_hash, source_family_id="SURVEY", study_product_id=f"R12-STUDY-{tag}", release_id=f"R12-REL-{tag}", instrument_release_id=f"R12-INST-{tag}", ingest_contract_version=INGEST_CONTRACT_VERSION, declared_universe_refs=(universe.ref,), declared_authority_snapshot_refs=tuple(a.authority_ref for a in authorities), declared_record_counts_by_logical_family=counts, source_snapshot_retention_ref=_ref("SOURCE_SNAPSHOT", f"r12-{tag}-{source_hash[:12]}"))
    candidate = C11SourceReleaseCandidate(source_release_manifest=manifest, empirical_universes=(universe,), respondent_identities=tuple(respondents.values()), question_variable_bindings=questions, respondent_events=tuple(events), routing_eligibility_facts_or_exact_rules=tuple(routing), empirical_coordinate_facts=tuple(coords), weight_measure_facts_or_typed_absence=TypedAbsence("NOT_APPLICABLE"), authority_snapshots=authorities, source_universe_relations_or_explicit_distinct_default=TypedAbsence("DISTINCT_BY_DEFAULT"), predicate_replay_bindings_when_retained_objects_require_them=TypedAbsence("NOT_APPLICABLE"), comparator_replay_bindings_or_typed_deferred_state=TypedAbsence("DEFERRED"), discovery_branch_replay_bindings_or_typed_deferred_state=TypedAbsence("DEFERRED"), structural_admission_replay_bindings_or_typed_not_applicable_state=TypedAbsence("NOT_APPLICABLE"), candidate_replay_manifest=None)
    replay = build_candidate_replay_manifest(candidate, replay_protocol_authority_ref=replay_auth.authority_ref, deterministic_tie_order_rules_ref=_ref("ORDER_RULE", "CANONICAL-REF-SORT"), replay_protocol_version="1.0.0")
    candidate = replace(candidate, candidate_replay_manifest=replay)
    repo = C11Repository(); result = ingest_c11_source_release(candidate, repo); assert result.accepted, result.errors
    return {"repo": repo, "release_ref": result.release_ref, "universe": universe, "respondents": respondents, "qrefs": qrefs, "crefs": {"INERT": _ref("COORDINATE_NATIVE", f"r12-{tag}-INERT")}, "risk_refs": {"R": risk_ref}, "source_auth": source_auth, "coord_auth": coord_auth, "routing_auth": routing_auth, "weight_auth": None, "authorities": authorities}


def _custom_query(source, qa, predicate, target, *, topology, domain, included_states, tag):
    return EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE", authority_snapshot_refs=(qa.authority_ref,), dependency_refs=(predicate.ref,), producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"r12-query-{tag}"),
        target_refs=(source["qrefs"][target],), target_arity_and_topology={"arity": 1, "joint_order_semantics": "SEMANTIC_ORDERED", "components": [{"target_ref": source["qrefs"][target], "topology": topology, "domain": domain, "target_domain_replay_ref": _ref("TARGET_DOMAIN", f"r12-{tag}"), "topology_authority_refs": [source["source_auth"].authority_ref], "response_semantic_authority_refs": [source["source_auth"].authority_ref], "included_states": list(included_states)}]},
        condition_predicate_ref=predicate.ref, risk_set_ref=source["risk_refs"]["R"], empirical_universe_refs=(source["universe"].ref,), scope_refs=(source["universe"].ref,), measure_basis_ref=_ref("MEASURE_BASIS", "RAW"),
        requested_output_grain={"source_scope_mode": "SINGLE_UNIVERSE", "measure_kind": "RAW", "risk_set_type": "WHOLE_QUESTION_RISK_SET", "response_state_semantics_ref": _ref("RESPONSE_STATE_SEMANTICS", f"r12-{tag}"), "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED"}, query_authority_refs=(qa.authority_ref,),
    )


def special_state_fixture():
    rows = [
        {"id": "SUB", "events": {"Q": ({"state": "SUBSTANTIVE_RESPONSE", "value": "1"},)}},
        {"id": "MISS", "events": {"Q": ({"state": "MISSING", "value": None},)}},
        {"id": "DK", "events": {"Q": ({"state": "DK", "value": None},)}},
        {"id": "REF", "events": {"Q": ({"state": "REFUSAL", "value": None},)}},
        {"id": "IAP", "routing": {"Q": "INAPPLICABLE"}, "events": {"Q": ({"state": "IAP", "value": None},)}},
        {"id": "NA", "routing": {"Q": "NOT_ASKED"}, "events": {"Q": ({"state": "NOT_ASKED", "value": None},)}},
    ]
    source = _build_event_source("special", rows, {"Q": "SCALAR_SINGULAR"}); qa = _query_authority("r12-special"); pred = _branch_predicate(source, qa, tag="all")
    domain = ["1", {"typed_response_state": "MISSING"}, {"typed_response_state": "DK"}, {"typed_response_state": "REFUSAL"}, {"typed_response_state": "IAP"}, {"typed_response_state": "NOT_ASKED"}]
    fact = _run(source, qa, pred, _custom_query(source, qa, pred, "Q", topology="SCALAR_SINGULAR", domain=domain, included_states=("SUBSTANTIVE_RESPONSE", "MISSING", "DK", "REFUSAL", "IAP", "NOT_ASKED"), tag="special")).facts[0]
    release = source["repo"].resolve_release_exact(source["release_ref"])
    event_states = tuple(sorted(obj.typed_state for obj in release.public_objects if isinstance(obj, RespondentEvent)))
    routing_states = tuple(sorted(set(obj.typed_state for obj in release.public_objects if isinstance(obj, RoutingEligibilityFact))))
    return source, fact, event_states, routing_states


def topology_fixture():
    rows = [{"id": "R1", "events": {
        "ORDER": ({"value": "B", "event_id": "O-2", "order_fields": {"semantic_ordinal": 2}}, {"value": "A", "event_id": "O-1", "order_fields": {"semantic_ordinal": 1}}),
        "RANK": ({"value": "LOW", "event_id": "R-2", "order_fields": {"rank": 2}}, {"value": "HIGH", "event_id": "R-1", "order_fields": {"rank": 1}}),
        "MULTI": ({"value": "A", "event_id": "M-2", "order_fields": {"multiplicity_index": 1}}, {"value": "A", "event_id": "M-1", "order_fields": {"multiplicity_index": 0}}),
    }}]
    source = _build_event_source("topology", rows, {"ORDER": "ORDERED_SEQUENCE", "RANK": "RANKED_RESPONSE", "MULTI": "REPEATED_EVENT"})
    qa = _query_authority("r12-topology"); pred = _branch_predicate(source, qa, tag="all"); repeated = FIXTURE_ORACLES["ORDERED_RANKED_MULTIPLICITY"].expected["repeated"]
    queries = {
        "ordered": _custom_query(source, qa, pred, "ORDER", topology="ORDERED_SEQUENCE", domain=[["A", "B"], ["B", "A"]], included_states=("SUBSTANTIVE_RESPONSE",), tag="ordered"),
        "ranked": _custom_query(source, qa, pred, "RANK", topology="RANKED_RESPONSE", domain=[["HIGH", "LOW"], ["LOW", "HIGH"]], included_states=("SUBSTANTIVE_RESPONSE",), tag="ranked"),
        "repeated": _custom_query(source, qa, pred, "MULTI", topology="REPEATED_EVENT", domain=[repeated], included_states=("SUBSTANTIVE_RESPONSE",), tag="repeated"),
    }
    return source, {name: _run(source, qa, pred, query).facts[0] for name, query in queries.items()}


def k_way_bounded_joint_fixture():
    rows = [{"id": f"R{a}{b}{c}", "responses": {"A": a, "B": b, "C": c, "Y": a ^ b ^ c}} for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    source = _build_source("r12-kway", rows); qa = _query_authority("r12-kway"); pred = _branch_predicate(source, qa, tag="all")
    return source, _run(source, qa, pred, _query(source, qa, pred, ("A", "B", "C", "Y"), tag="four-way")).facts[0]


__all__ = [
    "FixtureOracle", "FIXTURE_ORACLES", "FIXTURE_INVENTORY", "xor_zero_unary_fixture", "simpson_reversal_fixture",
    "same_marginals_different_joint_fixture", "response_position_fixture", "response_response_cotravel_fixture",
    "routing_risk_asymmetry_fixture", "raw_weighted_divergence_fixture", "observed_zero_zero_support_fixture",
    "special_state_fixture", "source_indexed_disagreement_fixture", "multi_universe_noncomparable_fixture",
    "topology_fixture", "k_way_bounded_joint_fixture", "_cell_map", "_ids_from_fact", "_rate",
]
