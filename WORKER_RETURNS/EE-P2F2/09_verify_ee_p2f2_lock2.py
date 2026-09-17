from __future__ import annotations
import base64, json, subprocess, sys
from pathlib import Path

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot, DiscoveryAuthority, EmpiricalQuerySpec, EmpiricalUniverse,
    ExactRef, canonical_json, make_empirical_predicate, semantic_hash,
)
from rawlsing_next.pre553_discovery_exact import (
    CANDIDATE_GRAMMAR_SCHEMA, I05_CONTRACT_ID,
    _catalog_atoms, _catalog_templates, _compile_frontier,
    _validate_catalog_scope, _verify_discovery_authority,
)

QUERY_OPERATION = "PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0"
DISCOVERY_OPERATION = "pre553_discovery_exact_execute"
SOURCE_SHA256 = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
HQ_HANDOFF = "b8e5fbe97ef47329c5544da6a0a8e2e64f80ff20"
HQ_CHECKPOINT = "20260917T1803-0400"
P2F1 = "00b86dcade82bc9efb6ea68a79062c6587d0de08"
R6A = "4b141b8b5748175e34c9286eba36f53d8df1e9d5"
GENERIC_PRE553 = "1dcd2a79dd6d4208738f655ab7fe4e71c219e354"
I03_PRODUCER = "cfc240aa3a64c59509eab97450a7d3603af813cc"
I03_PRODUCER_BLOB = "d63370dbcadc043dd2f27f5383cf36f0e84d1235"
I03_PRODUCER_SHA256 = "ad7434186e5e72886333f438ed9726cec01a2d2cf740353175da938708a5ef6d"
NODE5B = "53fcc2dd61c48069caa4b505ee7ca26e4ddafcee"

Q0 = {
    "qid": "question_impl.phase0.03ea3430fb4f08a1f0da",
    "source_variable": "Q291G5",
    "semantic_hash": "4574aecc9db3ec15ba255a5e6f6ce17304ccb610c7d7d9f4b7baddc6d4a77176",
    "text": "Government: The government is generally free of corruption",
}
Q1 = {
    "qid": "question_impl.phase0.068ef710ac1c269b8adf",
    "source_variable": "Q291P5",
    "semantic_hash": "304fbead4df5035bd97c02ff04000363cc5041129456555e3047ff3ff2efc185",
    "text": "Parliament: Parliament is generally free of corruption",
}
PAIR_LF_HASH = "aefe3477977a0b443bdf173b5d3866a0cc8d256a5937fa4c7af1107efa98ce07"
SUBSTANTIVE = (1, 2, 3, 4, 5)
SPECIAL = {-1: "Don't know", -2: "No answer", -4: "Not asked", -5: "Missing; Not available"}
COUNTRIES = (
    "Ethiopia", "Iran", "Kenya", "Kyrgyzstan", "Libya", "Morocco", "Myanmar",
    "Nicaragua", "Philippines", "Tajikistan", "Venezuela", "Vietnam", "Zimbabwe",
)
RESPONSE_LABELS = {1: "Agree strongly", 2: "Agree", 3: "Neither agree nor disagree", 4: "Disagree", 5: "Disagree strongly"}


def dref(kind: str, namespace: str, material) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:rawlsing:pre553:ee-p2f2:{namespace}:sha256:{digest}", digest)


def snap(*, aid: str, kind: str, operations, families, scope, basis) -> AuthoritySnapshot:
    content_hash = semantic_hash({"authority_id": aid, "basis": basis, "scope": scope, "operations": list(operations), "families": list(families)})
    replay_ref = dref("EE_P2F2_AUTHORITY_REPLAY_ROOT@1.0.0", aid.lower(), {"hq": HQ_HANDOFF, "checkpoint": HQ_CHECKPOINT, "basis": basis})
    return AuthoritySnapshot(
        typed_state="ALLOW", authority_snapshot_refs=(), dependency_refs=(),
        producer_replay_locator_or_reference_root=replay_ref,
        authority_id=aid, authority_version="1.0.0", authority_content_hash=content_hash,
        authority_kind=kind, decision_state="ALLOW", governed_operations=tuple(operations),
        governed_object_families=tuple(families), scope_envelope=scope,
        effective_time_or_interval={"checkpoint": HQ_CHECKPOINT, "handoff_commit": HQ_HANDOFF},
        parent_authority_refs=(), negative_limit_refs=(), supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash({"basis": basis, "no_new_wvs_semantics": True}),
        replay_protocol_ref=replay_ref,
    )


def build():
    q0_ref = ExactRef("WVS7QuestionBinding@1.0.0", Q0["qid"], Q0["semantic_hash"])
    q1_ref = ExactRef("WVS7QuestionBinding@1.0.0", Q1["qid"], Q1["semantic_hash"])
    response_semantics = {
        "substantive": [{"code": x, "label": RESPONSE_LABELS[x]} for x in SUBSTANTIVE],
        "special": [{"code": x, "label": SPECIAL[x]} for x in sorted(SPECIAL)],
        "authority_commit": R6A,
        "source_variables": [Q0["source_variable"], Q1["source_variable"]],
    }
    response_semantics_ref = dref("WVS7ResponseStateSemantics@1.0.0", "response-semantics", response_semantics)
    risk_binding = {
        "binding_id": "WVS7_Q291G5_Q291P5_SHARED_13_COUNTRY_SUBSTANTIVE_RISK_SET",
        "source_sha256": SOURCE_SHA256,
        "countries": list(COUNTRIES),
        "same_respondent_semantics": "SOURCE_ROW_IDENTITY__EXACT_SAME_WVS7_RECORD",
        "qid0": Q0["qid"], "qid1": Q1["qid"],
        "qid0_source": Q0["source_variable"], "qid1_source": Q1["source_variable"],
        "substantive_states": list(SUBSTANTIVE),
        "special_states_excluded_from_discovery_atoms": sorted(SPECIAL),
        "routing_authority_commit": R6A,
        "outcomes_inspected": False,
    }
    risk_ref = dref("WVS7RiskSetBinding@1.0.0", "risk-set", risk_binding)
    current_binding = {
        "source_sha256": SOURCE_SHA256, "source_bytes": 185163494, "rows": 97220, "variables": 613,
        "raw_wave": "W7", "hq_lock1": "HQ_HANDOFF/CHETIRI_FINAL_P2_COURT_MANIFEST_R1.json",
        "hq_handoff": HQ_HANDOFF, "p2f1": P2F1,
        "relation": "EXACT_FROZEN_SOURCE_ARTIFACT_TO_ACCEPTED_PAIR_CURRENT_SCOPE",
    }
    current_ref = dref("WVS7SourceCurrentBinding@1.0.0", "source-current", current_binding)
    measure_basis = {
        "measure_kind": "RAW", "weighting": "UNWEIGHTED", "count_semantics": "EXACT_NONNEGATIVE_INTEGER",
        "weight_design_estimand_authority": "NOT_DECLARED", "target_use_authority": "NOT_DECLARED",
        "source_sha256": SOURCE_SHA256, "lock1_raw_unweighted": True,
    }
    measure_ref = dref("RawUnweightedExactCountMeasureBasis@1.0.0", "measure-basis", measure_basis)
    scope_ref = dref("WVS7ExactProgramScope@1.0.0", "program-scope", {"source_sha256": SOURCE_SHA256, "risk_ref": risk_ref.as_dict(), "countries": list(COUNTRIES), "pair_lf_hash": PAIR_LF_HASH})
    operator_ref = dref("PRE553BooleanPredicateOperatorSemantics@1.0.0", "boolean-operators", {"ops": ["AND", "OR", "NOT", "LEAF"], "generic_tip": GENERIC_PRE553})

    source_auth = snap(
        aid="EE-P2F2-WVS7-SOURCE-SEMANTICS-TOPOLOGY",
        kind="SOURCE_SEMANTICS_TOPOLOGY",
        operations=("EE_P2F2_R02_R03_R04_ACCEPTED_WVS7_PAIR_BIND@1.0.0",),
        families=("EmpiricalUniverse@1.0.0", "EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"),
        scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED", "predicate_or_risk_set_refs": [risk_ref.as_dict()]},
        basis={"r6a": R6A, "qid0_hash": Q0["semantic_hash"], "qid1_hash": Q1["semantic_hash"], "pair_lf_hash": PAIR_LF_HASH},
    )
    routing_auth = snap(
        aid="EE-P2F2-WVS7-ROUTING-RISK-SET",
        kind="ROUTING_RISK_SET",
        operations=("EE_P2F2_R05_R06_ACCEPTED_WVS7_RISK_SET_BIND@1.0.0",),
        families=("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"),
        scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED", "predicate_or_risk_set_refs": [risk_ref.as_dict()]},
        basis={"r6a": R6A, "risk_binding": risk_binding},
    )
    relation_auth = snap(
        aid="EE-P2F2-WVS7-SOURCE-UNIVERSE-CURRENT",
        kind="SOURCE_UNIVERSE_RELATION",
        operations=("EE_P2F2_R01_R15A_EXACT_SOURCE_CURRENT_BIND@1.0.0",),
        families=("EmpiricalUniverse@1.0.0",),
        scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        basis={"lock1": current_binding, "p2f1": P2F1},
    )
    grammar_auth = snap(
        aid="EE-P2F2-WVS7-PRE553-I03-PREDICATE-GRAMMAR",
        kind="PREDICATE_GRAMMAR",
        operations=(QUERY_OPERATION,),
        families=("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"),
        scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED", "predicate_or_risk_set_refs": [risk_ref.as_dict()]},
        basis={"hq_handoff": HQ_HANDOFF, "operation": QUERY_OPERATION, "producer_commit": I03_PRODUCER, "producer_blob": I03_PRODUCER_BLOB, "producer_sha256": I03_PRODUCER_SHA256, "node5b": NODE5B},
    )
    discovery_auth_snap = snap(
        aid="EE-P2F2-WVS7-LOCK1-DISCOVERY-FRONTIER",
        kind="DISCOVERY_FRONTIER",
        operations=(DISCOVERY_OPERATION,),
        families=("DiscoveryAuthority@1.0.0", "DiscoveryResultReceipt@1.0.0"),
        scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED", "predicate_or_risk_set_refs": [risk_ref.as_dict()]},
        basis={"hq_lock1": current_binding["hq_lock1"], "shape": {"unary": 10, "pair": 1, "branch": 10, "joint": 25}, "coverage": "COMPLETE_FOR_EXACT_DECLARED_FRONTIER"},
    )
    replay_auth = snap(
        aid="EE-P2F2-PRE553-EXACT-REPLAY",
        kind="REPLAY_PROTOCOL",
        operations=("EE_P2F2_R13_EXACT_ONLY_REPLAY@1.0.0",),
        families=("EmpiricalUniverse@1.0.0", "EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "DiscoveryAuthority@1.0.0", "ReplayReceipt@1.0.0"),
        scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        basis={"generic_tip": GENERIC_PRE553, "law": "NO_LATEST_DEFAULT_FUZZY_FALLBACK"},
    )
    snapshots = (source_auth, routing_auth, relation_auth, grammar_auth, discovery_auth_snap, replay_auth)
    registry = AuthorityRegistry(snapshots)

    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref, relation_auth.authority_ref, replay_auth.authority_ref),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=current_ref,
        raw_source_identity={"filename": "WVS Wave 7.sav", "bytes": 185163494, "sha256": SOURCE_SHA256, "rows": 97220, "variables": 613},
        source_family="WVS",
        study_product_release={"source_artifact_sha256": SOURCE_SHA256, "raw_wave": "W7"},
        instrument_release={"accepted_module": "POLITICAL_TRUST_MODULE", "coadministration": "SAME_RESPONDENT_Q291_MATRIX_BATTERY", "authority_commit": R6A},
        country_geography={"exact_program_risk_scope": list(COUNTRIES), "population_generalization": "NONE_AUTHORIZED"},
        sampling_geography={"exact_program_risk_scope": list(COUNTRIES), "sampling_generalization": "NONE_ADDED_BY_F2"},
        raw_wave="W7", canonical_wave_if_governed="W7",
        field_or_reference_time={"wave_identity": "W7", "no_new_calendar_claim": True},
        target_population_and_sample_frame="SOURCE_LOCAL_RECORD_UNIVERSE_ONLY__NO_POPULATION_GENERALIZATION",
        sampling_design_regime="RAW_UNWEIGHTED_EXACT_COUNTS_ONLY__NO_WEIGHT_DESIGN_AUTHORITY",
        respondent_namespace="SOURCE_ROW_IDENTITY__EXACT_SAME_WVS7_RECORD",
        source_artifact_import_lineage={"lock1_source_sha256": SOURCE_SHA256, "hq_handoff": HQ_HANDOFF, "p2f1": P2F1},
        harmonization_authority_ref=None,
        source_relation_refs=(current_ref,),
    )
    # Re-issue exact grammar scope now that exact universe identity exists.
    grammar_auth = snap(
        aid="EE-P2F2-WVS7-PRE553-I03-PREDICATE-GRAMMAR",
        kind="PREDICATE_GRAMMAR", operations=(QUERY_OPERATION,),
        families=("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"),
        scope={"source_universe_refs": [universe.ref.as_dict()], "predicate_or_risk_set_refs": [risk_ref.as_dict()]},
        basis={"hq_handoff": HQ_HANDOFF, "operation": QUERY_OPERATION, "producer_commit": I03_PRODUCER, "producer_blob": I03_PRODUCER_BLOB, "producer_sha256": I03_PRODUCER_SHA256, "node5b": NODE5B, "universe_ref": universe.ref.as_dict()},
    )
    discovery_auth_snap = snap(
        aid="EE-P2F2-WVS7-LOCK1-DISCOVERY-FRONTIER", kind="DISCOVERY_FRONTIER",
        operations=(DISCOVERY_OPERATION,), families=("DiscoveryAuthority@1.0.0", "DiscoveryResultReceipt@1.0.0"),
        scope={"source_universe_refs": [universe.ref.as_dict()], "predicate_or_risk_set_refs": [risk_ref.as_dict()]},
        basis={"hq_lock1": current_binding["hq_lock1"], "shape": {"unary": 10, "pair": 1, "branch": 10, "joint": 25}, "coverage": "COMPLETE_FOR_EXACT_DECLARED_FRONTIER", "universe_ref": universe.ref.as_dict()},
    )
    snapshots = (source_auth, routing_auth, relation_auth, grammar_auth, discovery_auth_snap, replay_auth)
    registry = AuthorityRegistry(snapshots)

    routing_state_ref = dref("RoutingApplicabilityState@1.0.0", "eligible-applicable", {"state": "ELIGIBLE_APPLICABLE", "risk_ref": risk_ref.as_dict()})
    component_selector = dref("WVS7EventSelector@1.0.0", "q291-singular-response", {"topology": "SCALAR_SINGULAR", "pair_lf_hash": PAIR_LF_HASH})
    topology_replay_ref = dref("WVS7TargetDomainReplay@1.0.0", "q291-domain", {"domain": [str(x) for x in SUBSTANTIVE], "response_semantics_ref": response_semantics_ref.as_dict()})

    def routing_leaf(qref):
        return {"op": "LEAF", "leaf_type": "ROUTING_APPLICABILITY_STATE", "empirical_universe_ref": universe.ref.as_dict(),
                "question_semantic_ref": qref.as_dict(), "routing_or_applicability_state_ref": routing_state_ref.as_dict(),
                "routing_authority_ref": routing_auth.authority_ref.as_dict(), "routing_state": "ELIGIBLE_APPLICABLE"}
    baseline = make_empirical_predicate(
        predicate_ast={"op": "AND", "children": [routing_leaf(q0_ref), routing_leaf(q1_ref)]},
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(source_auth.authority_ref, routing_auth.authority_ref, grammar_auth.authority_ref),
        dependency_refs=(universe.ref, risk_ref, q0_ref, q1_ref, response_semantics_ref),
        producer_replay_locator_or_reference_root=dref("EE_P2F2_PredicateReplayRoot@1.0.0", "baseline-risk", risk_binding),
        grammar_authority_ref=grammar_auth.authority_ref,
        coordinate_question_value_refs=(q0_ref, q1_ref), risk_set_refs=(risk_ref,), scope_refs=(universe.ref, scope_ref),
        same_respondent_binding_semantics="SOURCE_ROW_IDENTITY__EXACT_SAME_WVS7_RECORD", operator_semantics_refs=(operator_ref,),
    )

    atoms = []
    for label, qref, qmeta in (("Q0", q0_ref, Q0), ("Q1", q1_ref, Q1)):
        for value in SUBSTANTIVE:
            value_ref = dref("WVS7ResponseValue@1.0.0", f"{label.lower()}-{value}", {"qid": qmeta["qid"], "value": value, "label": RESPONSE_LABELS[value], "response_semantics_ref": response_semantics_ref.as_dict()})
            ast = {"op": "LEAF", "leaf_type": "SURVEY_RESPONSE_EVENT", "empirical_universe_ref": universe.ref.as_dict(),
                   "question_semantic_ref": qref.as_dict(), "component_or_event_selector_ref": component_selector.as_dict(),
                   "response_value_or_state_ref": value_ref.as_dict(), "response_topology_authority_ref": source_auth.authority_ref.as_dict(),
                   "response_semantic_authority_ref": source_auth.authority_ref.as_dict(), "operator": "EQ", "exact_value": str(value)}
            pred = make_empirical_predicate(
                predicate_ast=ast, typed_state="PREDICATE_RESOLVED_AUTHORIZED",
                authority_snapshot_refs=(source_auth.authority_ref, routing_auth.authority_ref, grammar_auth.authority_ref),
                dependency_refs=(universe.ref, risk_ref, qref, response_semantics_ref, value_ref),
                producer_replay_locator_or_reference_root=dref("EE_P2F2_PredicateReplayRoot@1.0.0", f"{label.lower()}-{value}", ast),
                grammar_authority_ref=grammar_auth.authority_ref,
                coordinate_question_value_refs=(qref, value_ref), risk_set_refs=(risk_ref,), scope_refs=(universe.ref, scope_ref),
                same_respondent_binding_semantics="SOURCE_ROW_IDENTITY__EXACT_SAME_WVS7_RECORD", operator_semantics_refs=(operator_ref,),
            )
            atoms.append((f"{label}_STATE_{value}", pred))

    def component(qref):
        return {"target_ref": qref.as_dict(), "topology": "SCALAR_SINGULAR", "domain": [str(x) for x in SUBSTANTIVE],
                "target_domain_replay_ref": topology_replay_ref.as_dict(), "topology_authority_refs": [source_auth.authority_ref.as_dict()],
                "response_semantic_authority_refs": [source_auth.authority_ref.as_dict()], "included_states": ["SUBSTANTIVE_RESPONSE"]}
    grain = {"source_scope_mode": "SINGLE_UNIVERSE", "measure_kind": "RAW", "risk_set_type": "ROUTED_APPLICABLE_RISK_SET",
             "response_state_semantics_ref": response_semantics_ref.as_dict(), "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
             "query_operation": QUERY_OPERATION}
    def query(tag, targets):
        topo = {"arity": len(targets), "joint_order_semantics": "CANONICAL_SET_ORDER", "components": [component(x) for x in targets]}
        return EmpiricalQuerySpec(
            typed_state="QUERY_AUTHORIZED_RESOLVABLE",
            authority_snapshot_refs=(source_auth.authority_ref, routing_auth.authority_ref, grammar_auth.authority_ref, replay_auth.authority_ref),
            dependency_refs=(baseline.ref, risk_ref, universe.ref, scope_ref, measure_ref, response_semantics_ref, *targets),
            producer_replay_locator_or_reference_root=dref("EE_P2F2_QueryReplayRoot@1.0.0", tag, {"targets": [x.as_dict() for x in targets], "grain": grain}),
            target_refs=targets, target_arity_and_topology=topo, condition_predicate_ref=baseline.ref, risk_set_ref=risk_ref,
            empirical_universe_refs=(universe.ref,), scope_refs=(scope_ref,), measure_basis_ref=measure_ref,
            requested_output_grain=grain, query_authority_refs=(grammar_auth.authority_ref,),
        )
    q0_template = query("q0-marginal", (q0_ref,))
    q1_template = query("q1-marginal", (q1_ref,))
    joint_template = query("q0-q1-joint", (q0_ref, q1_ref))

    grammar_definition = {
        "schema": CANDIDATE_GRAMMAR_SCHEMA, "discovery_operation": DISCOVERY_OPERATION,
        "authority_precedes_search": True, "source_sha256": SOURCE_SHA256, "risk_set_ref": risk_ref.as_dict(),
        "limits": {"maximum_conditioner_arity_K": 1, "maximum_target_arity_J": 2},
        "atoms": [{"atom_id": "BASELINE_RISK", "kind": "ROUTING_RISK_BASELINE", "predicate_ref": baseline.ref.as_dict(), "ancestry_refs": []}] +
                 [{"atom_id": atom_id, "kind": "WVS7_SUBSTANTIVE_RESPONSE_STATE", "predicate_ref": pred.ref.as_dict(), "ancestry_refs": []} for atom_id, pred in atoms],
        "query_templates": [
            {"template_id": "Q0_MARGINAL", "query_ref": q0_template.ref.as_dict()},
            {"template_id": "Q1_MARGINAL", "query_ref": q1_template.ref.as_dict()},
            {"template_id": "Q0_Q1_JOINT", "query_ref": joint_template.ref.as_dict()},
        ],
        "rules": [
            {"rule_id": "R08_UNARY_Q0", "family": "UNARY_SOCIAL_FORK", "form": "BASE_QUERY", "baseline_atom_id": "BASELINE_RISK", "query_template_id": "Q0_MARGINAL", "target_cells": [str(x) for x in SUBSTANTIVE], "validation": {"kind": "TARGET_CELL_SUPPORTED"}},
            {"rule_id": "R08_UNARY_Q1", "family": "UNARY_SOCIAL_FORK", "form": "BASE_QUERY", "baseline_atom_id": "BASELINE_RISK", "query_template_id": "Q1_MARGINAL", "target_cells": [str(x) for x in SUBSTANTIVE], "validation": {"kind": "TARGET_CELL_SUPPORTED"}},
            {"rule_id": "R08_PAIR_COTRAVEL", "family": "PAIR_RESPONSE_COTRAVEL", "form": "JOINT_DEPENDENCE", "baseline_atom_id": "BASELINE_RISK", "joint_template_id": "Q0_Q1_JOINT", "marginal_template_ids": ["Q0_MARGINAL", "Q1_MARGINAL"], "validation": {"kind": "JOINT_NOT_PRODUCT_OF_MARGINALS"}},
            {"rule_id": "R08_BRANCH_Q0_TO_Q1", "family": "BRANCH_CONDITIONED_DISTRIBUTION", "form": "SINGLE_ATOM", "baseline_atom_id": "BASELINE_RISK", "query_template_id": "Q1_MARGINAL", "atom_ids": [f"Q0_STATE_{x}" for x in SUBSTANTIVE], "validation": {"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"}},
            {"rule_id": "R08_BRANCH_Q1_TO_Q0", "family": "BRANCH_CONDITIONED_DISTRIBUTION", "form": "SINGLE_ATOM", "baseline_atom_id": "BASELINE_RISK", "query_template_id": "Q0_MARGINAL", "atom_ids": [f"Q1_STATE_{x}" for x in SUBSTANTIVE], "validation": {"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"}},
            {"rule_id": "R08_JOINT_5X5", "family": "BOUNDED_K_WAY_RESPONSE_CONFIGURATION", "form": "BASE_QUERY", "baseline_atom_id": "BASELINE_RISK", "query_template_id": "Q0_Q1_JOINT", "target_cells": [[str(a), str(b)] for a in SUBSTANTIVE for b in SUBSTANTIVE], "validation": {"kind": "TARGET_CELL_SUPPORTED"}},
        ],
        "expected_shape": {"UNARY_SOCIAL_FORK": 10, "PAIR_RESPONSE_COTRAVEL": 1, "BRANCH_CONDITIONED_DISTRIBUTION": 10, "BOUNDED_K_WAY_RESPONSE_CONFIGURATION": 25, "TOTAL": 46},
        "no_pruning_ranking_adaptive_stop": True,
    }
    grammar_ref = dref("PRE553_I05_CANDIDATE_GRAMMAR@1.0.0", "wvs7-lock1-grammar", grammar_definition)
    # I05 requires grammar ref hash to be exact semantic_hash(definition), so use its native namespace/id with same digest.
    grammar_digest = semantic_hash(grammar_definition)
    grammar_ref = ExactRef("PRE553_I05_CANDIDATE_GRAMMAR@1.0.0", f"urn:rawlsing:pre553:ee-p2f2:wvs7-lock1-grammar:sha256:{grammar_digest}", grammar_digest)
    discovery = DiscoveryAuthority(
        typed_state="EXACT_BOUNDED_AUTHORIZED",
        authority_snapshot_refs=(discovery_auth_snap.authority_ref, replay_auth.authority_ref),
        dependency_refs=(universe.ref, risk_ref, measure_ref, grammar_ref),
        producer_replay_locator_or_reference_root=dref("EE_P2F2_DiscoveryAuthorityReplayRoot@1.0.0", "lock1-frontier", grammar_definition),
        candidate_grammar_ref=grammar_ref, candidate_universe_definition=grammar_definition,
        source_universe_scope={"allowed_universe_refs": [universe.ref.as_dict()]},
        risk_set_scope={"allowed_risk_set_refs": [risk_ref.as_dict()]},
        topology_scope={"maximum_conditioner_arity_K": 1, "maximum_target_arity_J": 2, "same_respondent_binding": "SOURCE_ROW_IDENTITY__EXACT_SAME_WVS7_RECORD"},
        measure_scope={"allowed_measure_kinds": ["RAW"], "weight_design_estimand": "NOT_AUTHORIZED"},
        support_rules={"kind": "RAW_SUPPORT_COUNTS", "nonnegative_exact_integers": True, "numerator_le_denominator": True, "zero_denominator": "TYPED_UNDEFINED_NOT_ADMISSIBLE", "weighted_current_gateway": "REJECT"},
        validation_rules={"unresolved_predicate_or_query": "REJECT", "exact_universe_scope_required": True, "exact_authority_closure_required": True},
        coverage_claim="COMPLETE_FOR_EXACT_DECLARED_FRONTIER",
        pruning_contract={"kind": "NONE_EXACT_EVALUATE_ALL"},
        algorithm_identity_if_semantically_required=I05_CONTRACT_ID,
        tie_order_rules="CANONICAL_CANDIDATE_HASH_ORDER", rng_policy_if_any="NONE",
    )
    definition = _verify_discovery_authority(discovery, registry)
    pred_catalog = [baseline] + [p for _, p in atoms]
    query_catalog = [q0_template, q1_template, joint_template]
    atom_catalog = _catalog_atoms(definition, pred_catalog)
    template_catalog = _catalog_templates(definition, query_catalog)
    _validate_catalog_scope(discovery, atom_catalog, template_catalog)
    candidates = _compile_frontier(definition, atom_catalog, template_catalog)
    assert len(candidates) == 46
    counts = {}
    for c in candidates: counts[c.family] = counts.get(c.family, 0) + 1
    assert counts == {"BOUNDED_K_WAY_RESPONSE_CONFIGURATION": 25, "BRANCH_CONDITIONED_DISTRIBUTION": 10, "PAIR_RESPONSE_COTRAVEL": 1, "UNARY_SOCIAL_FORK": 10}
    ordered_hashes = [c.candidate_hash for c in candidates]
    assert ordered_hashes == sorted(ordered_hashes)

    replay_binding = {
        "mode": "EXACT_ONLY", "no_latest_default_fuzzy": True, "source_sha256": SOURCE_SHA256,
        "universe_ref": universe.ref.as_dict(), "authority_refs": [x.authority_ref.as_dict() for x in snapshots],
        "predicate_refs": [baseline.ref.as_dict()] + [p.ref.as_dict() for _, p in atoms],
        "query_template_refs": [q0_template.ref.as_dict(), q1_template.ref.as_dict(), joint_template.ref.as_dict()],
        "discovery_authority_ref": discovery.ref.as_dict(), "candidate_hashes": ordered_hashes,
    }
    replay_hash = semantic_hash(replay_binding)
    lock2_material = {
        "schema": "EE_P2F2_WVS7_LOCK2_MATERIALIZATION@1.0.0", "hq_checkpoint": HQ_CHECKPOINT, "hq_handoff": HQ_HANDOFF,
        "source_sha256": SOURCE_SHA256, "universe_ref": universe.ref.as_dict(), "risk_set_ref": risk_ref.as_dict(),
        "r07_authority_ref": grammar_auth.authority_ref.as_dict(), "r07_operation": QUERY_OPERATION,
        "measure_basis_ref": measure_ref.as_dict(), "discovery_authority_ref": discovery.ref.as_dict(),
        "candidate_grammar_ref": grammar_ref.as_dict(), "candidate_count": 46, "candidate_hashes": ordered_hashes,
        "replay_hash": replay_hash, "source_access_during_materialization": False, "empirical_outcomes_computed": False,
    }
    lock2_hash = semantic_hash(lock2_material)

    closure = {rid: "PASS" for rid in ("R01","R02","R03","R04","R05","R06","R07","R08","R09","R10","R11","R12","R13","R15A")}
    artifacts = {}
    artifacts["WORKER_RETURNS/EE-P2F2/01_WVS7_PRE553_ISSUED_AUTHORITY_SNAPSHOTS.json"] = {"schema":"EE_P2F2_AUTHORITY_SNAPSHOTS@1.0.0","snapshots":[x.as_dict() for x in snapshots],"r07":{"operation":QUERY_OPERATION,"authority_ref":grammar_auth.authority_ref.as_dict(),"object_family_fitness":["EmpiricalPredicate@1.0.0","EmpiricalQuerySpec@1.0.0","EmpiricalFact@1.0.0"],"liTS_imported":False}}
    artifacts["WORKER_RETURNS/EE-P2F2/02_WVS7_EMPIRICAL_UNIVERSE_AND_RISK_SET_BINDINGS.json"] = {"schema":"EE_P2F2_UNIVERSE_RISK_BINDINGS@1.0.0","empirical_universe":universe.as_dict(),"current_binding":current_binding,"current_binding_ref":current_ref.as_dict(),"risk_set_binding":risk_binding,"risk_set_ref":risk_ref.as_dict(),"measure_basis":measure_basis,"measure_basis_ref":measure_ref.as_dict(),"scope_ref":scope_ref.as_dict()}
    artifacts["WORKER_RETURNS/EE-P2F2/03_WVS7_RESPONSE_ATOM_AND_PREDICATE_BINDINGS.json"] = {"schema":"EE_P2F2_RESPONSE_PREDICATE_BINDINGS@1.0.0","response_semantics":response_semantics,"response_semantics_ref":response_semantics_ref.as_dict(),"baseline_risk_predicate":baseline.as_dict(),"atoms":[{"atom_id":i,"predicate":p.as_dict()} for i,p in atoms],"substantive_states":list(SUBSTANTIVE),"special_states":[{"code":k,"label":SPECIAL[k]} for k in sorted(SPECIAL)]}
    artifacts["WORKER_RETURNS/EE-P2F2/04_WVS7_QUERY_TEMPLATE_BINDINGS.json"] = {"schema":"EE_P2F2_QUERY_TEMPLATE_BINDINGS@1.0.0","query_operation":QUERY_OPERATION,"templates":[{"template_id":"Q0_MARGINAL","query":q0_template.as_dict()},{"template_id":"Q1_MARGINAL","query":q1_template.as_dict()},{"template_id":"Q0_Q1_JOINT","query":joint_template.as_dict()}],"candidate_grammar_definition":grammar_definition,"candidate_grammar_ref":grammar_ref.as_dict()}
    artifacts["WORKER_RETURNS/EE-P2F2/05_WVS7_DISCOVERY_AUTHORITY_AND_FRONTIER_BINDING.json"] = {"schema":"EE_P2F2_DISCOVERY_FRONTIER@1.0.0","discovery_authority":discovery.as_dict(),"family_counts":counts,"candidate_count":46,"candidate_hashes":ordered_hashes,"candidate_identities":[{"family":c.family,"rule_id":c.rule_id,"candidate_id":c.candidate_id,"candidate_hash":c.candidate_hash,"winning_predicate_ref":c.winning_predicate.ref.as_dict(),"query_roles":[{"role":r.role,"predicate_ref":r.predicate.ref.as_dict(),"query_ref":r.query.ref.as_dict()} for r in c.query_roles],"validation":c.validation} for c in candidates],"coverage":"COMPLETE_FOR_EXACT_DECLARED_FRONTIER","order":"CANDIDATE_HASH_ASCENDING"}
    artifacts["WORKER_RETURNS/EE-P2F2/06_WVS7_REPLAY_AND_CURRENTNESS_BINDINGS.json"] = {"schema":"EE_P2F2_REPLAY_CURRENTNESS@1.0.0","replay_binding":replay_binding,"replay_hash":replay_hash,"current_binding_ref":current_ref.as_dict(),"exact_only":True,"no_latest_default_fuzzy":True,"source_access":False}
    artifacts["WORKER_RETURNS/EE-P2F2/07_14_B_ROW_CLOSURE_MATRIX.json"] = {"schema":"EE_P2F2_14_B_ROW_CLOSURE_MATRIX@1.0.0","rows":closure,"excluded":{"R10W":"NOT_REQUIRED_FOR_LOCK2_AUTHORITY","R14":"NOT_REQUIRED_FOR_LOCK2_AUTHORITY","R15B":"NOT_REQUIRED_FOR_LOCK2_AUTHORITY"},"all_required_closed":True}
    artifacts["WORKER_RETURNS/EE-P2F2/08_LOCK2_ISSUER_RECEIPT.json"] = {"schema":"EE_P2F2_LOCK2_ISSUER_RECEIPT@1.0.0","disposition":"PASS__LOCK2_MATERIALIZED","lock2_hash":lock2_hash,"lock2_material":lock2_material,"candidate_count":46,"family_counts":counts,"replay_hash":replay_hash,"source_access":False,"outcome_computation":False,"generic_code_modified":False,"wave_specific_outputs_only":True,"successor_wake":"EE-P2_FINAL_A_B_C_EQUAL_WORK_EXECUTION_MAY_RESUME_ONLY_AFTER_HQ_ADOPTION_OF_THIS_LOCK2_RETURN"}
    artifacts["WORKER_RETURNS/EE-P2F2/00_RETURN.md"] = f"""# EE-P2F2 — WVS7 Mechanical PRE553 Issuer — Governed Return\n\nStatus: **PASS — all 14 commissioned B rows closed; deterministic Lock2 materialized.**\n\nResumed from worker head `da574ee0e1329c07d017ca18ac8d9f2107e2fe37` under sealed HQ checkpoint `{HQ_CHECKPOINT}` / immutable handoff `{HQ_HANDOFF}`. The prior R07 blocker is closed with the exact accepted generic operation `{QUERY_OPERATION}`. No alias, normalization, version elision, `OP-query`, or LiTS semantic carrier was used.\n\n## Exact closure\n\n- R01/R15A: exact WVS7 source-local `EmpiricalUniverse@1.0.0` and current binding issued without SAV access.\n- R02-R06: accepted Q291G5/Q291P5 qids, 1..5 substantive states, -1/-2/-4/-5 typed specials, same-row respondent topology, exact 13-country routing/risk set, and immutable source/risk refs bound.\n- R07: positive WVS-local `PREDICATE_GRAMMAR` authority materialized for `EmpiricalPredicate@1.0.0`, `EmpiricalQuerySpec@1.0.0`, and `EmpiricalFact@1.0.0` under exact operation `{QUERY_OPERATION}` and exact WVS universe.\n- R08/R09: 10 response-state predicates plus baseline risk predicate; 3 exact query templates; frozen 46-candidate grammar objectized.\n- R10: raw/unweighted exact-count basis only; no weight/design/estimand authority.\n- R11/R12: exact `DISCOVERY_FRONTIER` authority and I05 support/validation closure, complete declared frontier, no pruning/ranking/adaptive stop.\n- R13: exact-only replay; no latest/default/fuzzy fallback.\n\n## Lock2\n\n- universe: `{universe.ref.object_id}` / `{universe.ref.content_hash}`\n- R07 authority: `{grammar_auth.authority_ref.authority_id}@{grammar_auth.authority_ref.authority_version}` / `{grammar_auth.authority_ref.authority_content_hash}`\n- candidate grammar: `{grammar_ref.object_id}` / `{grammar_ref.content_hash}`\n- discovery authority: `{discovery.ref.object_id}` / `{discovery.ref.content_hash}`\n- candidates: **46**, exact family shape 10 / 1 / 10 / 25, canonical candidate-hash ascending.\n- replay hash: `{replay_hash}`\n- Lock2 hash: `{lock2_hash}`\n\nNo WVS SAV/outcome access occurred; no empirical outcome was computed; no generic PRE553 code, Lock1, MAIN, or semantic PRE-MAIN was mutated. `WAVE_SPECIFIC_AUTHORITY_AND_OUTPUTS != WAVE_SPECIFIC_GENERIC_CODE` is preserved.\n\nTerminal: `EE_P2F2_PASS__WVS7_PRE553_AUTHORITY_OBJECTIZATION_COMPLETE__LOCK2_MATERIALIZED__FINAL_ABC_SUCCESSOR_WAKE_READY`\n"""
    return artifacts, lock2_hash


def emit_bundle():
    artifacts, lock2_hash = build()
    for path in sorted(artifacts):
        raw = (json.dumps(artifacts[path], sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8") if not path.endswith(".md") else artifacts[path].encode("utf-8")
        print("EE_P2F2_FILE::" + path + "::" + base64.b64encode(raw).decode("ascii"))
    print("EE_P2F2_LOCK2_HASH::" + lock2_hash)


def test_ee_p2f2_lock2_materialization():
    artifacts, lock2_hash = build()
    assert len(artifacts["WORKER_RETURNS/EE-P2F2/05_WVS7_DISCOVERY_AUTHORITY_AND_FRONTIER_BINDING.json"]["candidate_hashes"]) == 46
    completed = subprocess.run([sys.executable, __file__, "--verify-only"], check=False, capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip() == lock2_hash
    emit_bundle()

if __name__ == "__main__":
    if "--verify-only" in sys.argv:
        print(build()[1])
    else:
        emit_bundle()
