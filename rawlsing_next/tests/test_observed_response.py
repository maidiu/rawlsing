"""Focused nonrespondent tests for observed-response / co-observed execution.

The SRC04 release used here is the repository's labelled NONRESPONDENT fixture.
No original respondent row is read, printed, committed or inferred.  The test
operation authority is intentionally fixture-only; the fixture itself proves the
engineering boundary, not an original scientific result.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from types import SimpleNamespace
from pathlib import Path
import hashlib

import pytest

import rawlsing_next._pre553_query_eval as qeval
from rawlsing_next.pre553_c11_integrity import RespondentIdentity
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry, Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    ExactRef,
    EmpiricalQuerySpec,
    authority_ref,
    canonical_json,
    exact_ref,
    make_empirical_predicate,
)
from rawlsing_next.pre553_empirical_query import (
    EmpiricalQueryExecutionError,
    execute_empirical_query,
    replay_empirical_query,
)
from rawlsing_next.pre553_observed_response import (
    CO_OBSERVED_RESPONSE_RISK_SET,
    OBSERVED_RESPONSE_RISK_SET,
    ObservedResponseContract,
    ObservedResponseTopologyBinding,
    validate_contract_authority,
)
from rawlsing_next.source_configuration.factory import build_validated_c11_release_from_config
from rawlsing_next.source_configuration.fixture import load_fixture_stream
from rawlsing_next.source_configuration.schema import load_source_config

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "source_pre553_validation/SRC04/fixture.config.json"
FIXTURE_PATH = ROOT / "source_pre553_validation/SRC04/fixture.json"
ORIGINAL_SHA = "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18"
OPERATION = "OBSERVED_RESPONSE_DISTRIBUTION@1.0.0"


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:observed-response:{kind.lower()}:{tag}", _h(f"observed:{kind}:{tag}"))


def _auth(tag: str, kind: str, operations, families, scope) -> AuthoritySnapshot:
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"authority-{tag}"),
        authority_id=f"OBS-TEST-{tag}",
        authority_version="1.0.0",
        authority_content_hash=_h(f"authority:{tag}"),
        authority_kind=kind,
        decision_state="ALLOW",
        governed_operations=tuple(operations),
        governed_object_families=tuple(families),
        scope_envelope=scope,
        effective_time_or_interval="NONRESPONDENT_FIXTURE",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"semantics:{tag}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", tag),
    )


class _Context:
    def __init__(self) -> None:
        self.config = load_source_config(CONFIG_PATH)
        self.stream = load_fixture_stream(FIXTURE_PATH)
        self.release = build_validated_c11_release_from_config(self.config, stream=self.stream)
        self.universe = next(
            obj for obj in self.release.public_objects if obj.schema_id == "EmpiricalUniverse"
        )
        self.respondents = sorted(
            (record for record in self.release.internal_records
             if isinstance(record, RespondentIdentity)),
            key=lambda record: record.ref.key,
        )
        self.questions = {q["question_id"]: q for q in self.config.document["questions"]}
        self.responses = {r["question_id"]: r for r in self.config.document["response_slots"]}
        self.risk_set_ref = _ref("RISK_SET", "SRC04-OBSERVED")
        self.query_authority = _auth(
            "QUERY",
            "PREDICATE_GRAMMAR",
            (OPERATION,),
            ("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"),
            {
                "fixture_only": True,
                "grade": "NONRESPONDENT_FIXTURE_ONLY",
                "source_id": "SRC04",
                "source_sha256": ORIGINAL_SHA,
                "source_universe_refs": [self.universe.ref.as_dict()],
                "predicate_or_risk_set_refs": [self.risk_set_ref.as_dict()],
            },
        )
        self.release_authorities = tuple(
            obj for obj in self.release.public_objects if obj.schema_id == "AuthoritySnapshot"
        )
        self.registry = AuthorityRegistry((*self.release_authorities, self.query_authority))
        self.repository = C11Repository((self.release,))
        self.target_refs = tuple(sorted(
            (exact_ref(self.questions[q]["native_question_ref"], "native_question_ref")
             for q in ("q102", "q206", "q236")),
            key=lambda ref: ref.key,
        ))
        self.topology_bindings = tuple(sorted(
            (self._topology_binding(q) for q in ("q102", "q206", "q236")),
            key=lambda binding: binding.target_ref.key,
        ))
        self.observed_states = ("SUBSTANTIVE_RESPONSE", "DK", "SOURCE_SPECIFIC_SPECIAL")
        self.contract = ObservedResponseContract(
            contract_id="OBS-TEST-SRC04-FIXTURE",
            contract_version="1.0.0",
            contract_state="AUTHORIZED",
            authority_grade="NONRESPONDENT_FIXTURE_ONLY",
            source_id="SRC04",
            source_sha256=ORIGINAL_SHA,
            source_snapshot_ref=exact_ref(
                self.config.document["binding"]["source_snapshot_ref"], "source_snapshot_ref"),
            source_artifact_ref=self.release.source_artifact_ref,
            source_release_manifest_hash=self.release.source_release_manifest_hash,
            release_ref=self.release.release_ref,
            universe_ref=self.universe.ref,
            operation=OPERATION,
            operation_authority_ref=self.query_authority.authority_ref,
            risk_set_ref=self.risk_set_ref,
            target_refs=self.target_refs,
            observed_states=self.observed_states,
            missing_states=("MISSING",),
            denominator_policies=("CO_OBSERVED_TARGETS", "PER_TARGET_OBSERVED"),
            condition_observation_policy="ALL_REFERENCED_RESPONSE_VARIABLES_OBSERVED",
            topology_bindings=self.topology_bindings,
        )
        validate_contract_authority(self.contract, self.registry)

    def _topology_binding(self, question_id: str) -> ObservedResponseTopologyBinding:
        question = self.questions[question_id]
        occurrence = self.responses[question_id]["values"][0]["occurrences"][0]
        return ObservedResponseTopologyBinding(
            target_ref=exact_ref(question["native_question_ref"], "native_question_ref"),
            source_native_topology_ref=exact_ref(occurrence["topology_ref"], "topology_ref"),
            source_native_kind=occurrence["multiplicity_order_rank_fields"]["kind"],
            i03_topology="SCALAR_SINGULAR",
            topology_operation="R157_PREPARE_SOURCE_TOPOLOGY",
            topology_authority_ref=authority_ref(question["topology_authority_ref"], "topology_authority_ref"),
            response_semantic_authority_refs=(
                authority_ref(question["semantic_authority_ref"], "semantic_authority_ref"),
            ),
        )

    def domain(self, question_id: str) -> tuple:
        values = []
        seen = set()
        for value in self.responses[question_id]["values"]:
            if value["response_state"] not in self.observed_states:
                continue
            cell = (
                value["canonical_value"]
                if value["response_state"] == "SUBSTANTIVE_RESPONSE"
                else {"typed_response_state": value["response_state"]}
            )
            key = canonical_json(cell)
            if key not in seen:
                seen.add(key)
                values.append(cell)
        return tuple(values)

    def branch_predicate_ast(self) -> dict:
        return {
            "op": "LEAF",
            "leaf_type": "DERIVED_BRANCH_COHORT",
            "branch_definition_id": "ALL-NONRESPONDENT-FIXTURE-RESPONDENTS",
            "resolved_predicate_hash_or_exact_membership_ref": _ref("BRANCH_MEMBERSHIP", "all").as_dict(),
            "parent_ancestry_ref": _ref("BRANCH_PARENT", "all").as_dict(),
            "branch_algorithm_authority_ref": self.query_authority.authority_ref.as_dict(),
            "branch_membership_replay_ref": _ref("BRANCH_REPLAY", "all").as_dict(),
            "branch_source_scope_ref": self.universe.ref.as_dict(),
            "exact_member_respondent_refs": [r.ref.as_dict() for r in self.respondents],
        }

    def condition_ast(self, question_id: str, value) -> dict:
        question = self.questions[question_id]
        return {
            "op": "LEAF",
            "leaf_type": "SURVEY_RESPONSE_EVENT",
            "question_semantic_ref": question["native_question_ref"],
            "component_or_event_selector_ref": _ref("EVENT_SELECTOR", f"{question_id}-any").as_dict(),
            "response_value_or_state_ref": _ref("VALUE_REF", f"{question_id}-{value}").as_dict(),
            "response_topology_authority_ref": question["topology_authority_ref"],
            "response_semantic_authority_ref": question["semantic_authority_ref"],
            "operator": "EQ",
            "exact_value": str(value),
        }

    def query(self, targets, risk_type, predicate_ast, *, contract=None,
              measure="RAW", operation=OPERATION, tag="query") -> EmpiricalQuerySpec:
        contract = contract or self.contract
        components = []
        for question_id in targets:
            question = self.questions[question_id]
            components.append({
                "target_ref": question["native_question_ref"],
                "topology": "SCALAR_SINGULAR",
                "domain": list(self.domain(question_id)),
                "target_domain_replay_ref": _ref("TARGET_DOMAIN", f"{tag}-{question_id}").as_dict(),
                "topology_authority_refs": [question["topology_authority_ref"]],
                "response_semantic_authority_refs": [question["semantic_authority_ref"]],
                "included_states": list(contract.observed_states),
            })
        predicate = make_empirical_predicate(
            predicate_ast=predicate_ast,
            typed_state="PREDICATE_RESOLVED_AUTHORIZED",
            authority_snapshot_refs=(self.query_authority.authority_ref,),
            dependency_refs=(),
            producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"predicate-{tag}"),
            grammar_authority_ref=self.query_authority.authority_ref,
            coordinate_question_value_refs=(),
            risk_set_refs=(self.risk_set_ref,),
            scope_refs=(self.universe.ref,),
            same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
            operator_semantics_refs=(_ref("OPERATOR_SEMANTICS", "BOOLEAN-AND-OR-NOT"),),
        )
        grain = {
            "source_scope_mode": "SINGLE_UNIVERSE",
            "measure_kind": measure,
            "risk_set_type": risk_type,
            "response_state_semantics_ref": _ref("RESPONSE_STATE_SEMANTICS", "OBSERVED").as_dict(),
            "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
            "query_operation": operation,
            "observed_response_contract_ref": contract.ref.as_dict(),
            "observed_response_contract": contract.semantic_projection(),
        }
        if measure == "GOVERNED_WEIGHTED":
            grain["weight_basis_id"] = "W"
        query = EmpiricalQuerySpec(
            typed_state="QUERY_AUTHORIZED_RESOLVABLE",
            authority_snapshot_refs=(self.query_authority.authority_ref,),
            dependency_refs=(predicate.ref, contract.ref),
            producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"query-{tag}"),
            target_refs=tuple(exact_ref(self.questions[q]["native_question_ref"], "target_ref")
                              for q in targets),
            target_arity_and_topology={
                "arity": len(targets),
                "joint_order_semantics": "SEMANTIC_ORDERED",
                "components": components,
            },
            condition_predicate_ref=predicate.ref,
            risk_set_ref=self.risk_set_ref,
            empirical_universe_refs=(self.universe.ref,),
            scope_refs=(self.universe.ref,),
            measure_basis_ref=_ref("MEASURE_BASIS", measure),
            requested_output_grain=grain,
            query_authority_refs=(self.query_authority.authority_ref,),
        )
        return query, predicate

    def run(self, targets, risk_type, predicate_ast, *, contract=None,
            measure="RAW", operation=OPERATION, registry=None, tag="query"):
        query, predicate = self.query(
            targets, risk_type, predicate_ast, contract=contract,
            measure=measure, operation=operation, tag=tag,
        )
        return execute_empirical_query(
            repository=self.repository,
            query=query,
            predicate=predicate,
            authority_registry=registry or self.registry,
            release_refs=(self.release.release_ref,),
        ).facts[0]


@pytest.fixture(scope="module")
def context():
    return _Context()


def _ledger(fact):
    observed = fact.target_topology.get("observed_response")
    assert observed is not None
    return observed["ledger"]


def _cell_counts(fact):
    return {
        canonical_json(row["cell"]): row["raw_numerator_support"]
        for row in fact.target_topology["complete_cell_semantic_projection"]
    }


def test_unary_observed_distribution_excludes_missing_and_preserves_ledger(context):
    fact = context.run(["q236"], OBSERVED_RESPONSE_RISK_SET,
                       context.branch_predicate_ast(), tag="unary")
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 7
    assert fact.raw_numerator_support == 7
    ledger = _ledger(fact)
    assert ledger["scoped_respondents"] == 8
    assert ledger["target_observed"] == 7
    assert ledger["target_unobserved"] == 1
    assert ledger["denominator"] == 7
    assert ledger["not_eligible_population_estimate"] is True
    counts = _cell_counts(fact)
    assert counts[canonical_json({"typed_response_state": "DK"})] == 2
    assert any(cell_state == "OBSERVED_POSITIVE" for cell_state in
               (row["cell_state"] for row in fact.target_topology["complete_cell_semantic_projection"]))


def test_co_observed_joint_requires_both_answers(context):
    fact = context.run(["q236", "q206"], CO_OBSERVED_RESPONSE_RISK_SET,
                       context.branch_predicate_ast(), tag="joint")
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 6
    assert fact.raw_numerator_support == 6
    ledger = _ledger(fact)
    assert ledger["target_observed"] == 6
    assert ledger["target_unobserved"] == 2
    assert ledger["denominator_policy"] == "CO_OBSERVED_TARGETS"
    assert sum(_cell_counts(fact).values()) == 6


def test_three_way_co_observed_joint_is_not_pairwise_synthesis(context):
    fact = context.run(
        ["q102", "q206", "q236"], CO_OBSERVED_RESPONSE_RISK_SET,
        context.branch_predicate_ast(), tag="triple-joint")
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 6
    assert _ledger(fact)["target_observed"] == 6
    assert sum(_cell_counts(fact).values()) == 6
    assert len(fact.target_topology["complete_cell_semantic_projection"]) > 6


def test_conditional_preserves_risk_and_condition_denominator_ledgers(context):
    value = next(
        item["canonical_value"] for item in context.responses["q206"]["values"]
        if item["response_state"] == "SUBSTANTIVE_RESPONSE"
    )
    condition = context.condition_ast("q206", value)
    fact = context.run(["q236"], OBSERVED_RESPONSE_RISK_SET, condition, tag="conditional")
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 1
    ledger = _ledger(fact)
    assert ledger["risk_member_count"] == 7
    assert ledger["condition_unobserved"] == 1
    assert ledger["condition_false"] == 5
    assert ledger["denominator"] == 1
    assert any(
        row["cell_state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
        for row in fact.target_topology["complete_cell_semantic_projection"]
    )


def test_observed_profile_does_not_call_eligible_risk_membership(context, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("_risk_membership must not be called for observed-response profile")

    monkeypatch.setattr(qeval, "_risk_membership", forbidden)
    fact = context.run(["q236"], OBSERVED_RESPONSE_RISK_SET,
                       context.branch_predicate_ast(), tag="no-risk-membership")
    assert fact.typed_state == "SUPPORTED"


def test_unresolved_routing_still_refuses_existing_eligible_profile():
    profile = SimpleNamespace(risk_set_type="WHOLE_QUESTION_RISK_SET")
    with pytest.raises(Exception, match="unresolved"):
        qeval._risk_membership(("ROUTING_UNKNOWN",), profile=profile)


def test_contract_requires_exact_operation_authority(context):
    query, predicate = context.query(
        ["q236"], OBSERVED_RESPONSE_RISK_SET, context.branch_predicate_ast(),
        operation="DIFFERENT-OBSERVED-RESPONSE-OPERATION", tag="wrong-operation")
    result = execute_empirical_query(
        repository=context.repository,
        query=query,
        predicate=predicate,
        authority_registry=context.registry,
        release_refs=(context.release.release_ref,),
    )
    assert result.facts[0].typed_state == "UNAVAILABLE"
    assert result.facts[0].p02_failure_state in {
        "OBSERVED_RESPONSE_AUTHORITY_UNAVAILABLE", "MISSING_REQUIRED_AUTHORITY"}


def test_contract_release_mismatch_refuses(context):
    bad_contract = replace(
        context.contract,
        release_ref=_ref("C11LogicalRelease", "wrong-release"),
    )
    fact = context.run(
        ["q236"], OBSERVED_RESPONSE_RISK_SET, context.branch_predicate_ast(),
        contract=bad_contract, tag="wrong-release")
    assert fact.typed_state == "UNAVAILABLE"
    assert fact.p02_failure_state == "OBSERVED_RESPONSE_AUTHORITY_UNAVAILABLE"


def test_fixture_authority_cannot_be_promoted_to_original_scientific_grade(context):
    original_contract = replace(context.contract, authority_grade="ORIGINAL_SCIENTIFIC")
    with pytest.raises(Pre553AuthorityError, match="fixture-only"):
        validate_contract_authority(original_contract, context.registry)


def test_weighted_observed_operation_is_rejected(context):
    with pytest.raises(EmpiricalQueryExecutionError, match="weighted"):
        context.run(
            ["q236"], OBSERVED_RESPONSE_RISK_SET, context.branch_predicate_ast(),
            measure="GOVERNED_WEIGHTED", tag="weighted-observed")


def test_routing_predicate_in_observed_condition_is_refused(context):
    question = context.questions["q236"]
    routing_ast = {
        "op": "LEAF",
        "leaf_type": "ROUTING_APPLICABILITY_STATE",
        "question_semantic_ref": question["native_question_ref"],
        "routing_or_applicability_state_ref": _ref("ROUTING_STATE", "unknown").as_dict(),
        "routing_authority_ref": context.config.document["routing"][0]["authority_ref"],
        "routing_state": "ROUTING_UNKNOWN",
    }
    fact = context.run(
        ["q236"], OBSERVED_RESPONSE_RISK_SET, routing_ast, tag="routing-condition")
    assert fact.typed_state == "UNAVAILABLE"
    assert fact.p02_failure_state == "OBSERVED_RESPONSE_AUTHORITY_UNAVAILABLE"


def test_replay_is_exact(context):
    first = context.run(["q236"], OBSERVED_RESPONSE_RISK_SET,
                        context.branch_predicate_ast(), tag="replay")
    second = context.run(["q236"], OBSERVED_RESPONSE_RISK_SET,
                         context.branch_predicate_ast(), tag="replay")
    assert first.ref == second.ref
    assert first.replay_ref == second.replay_ref


def test_existing_replay_owner_accepts_observed_fact_ref(context):
    query, predicate = context.query(
        ["q236"], OBSERVED_RESPONSE_RISK_SET,
        context.branch_predicate_ast(), tag="replay-owner")
    first = execute_empirical_query(
        repository=context.repository, query=query, predicate=predicate,
        authority_registry=context.registry,
        release_refs=(context.release.release_ref,),
    )
    replayed = replay_empirical_query(
        repository=context.repository, query=query, predicate=predicate,
        authority_registry=context.registry,
        release_refs=(context.release.release_ref,),
        expected_fact_refs=(first.facts[0].ref,),
    )
    assert replayed.facts[0].ref == first.facts[0].ref
