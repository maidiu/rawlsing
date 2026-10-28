"""Independent review tests for the C observed-profile -> D native consumer boundary.

The only source objects read here are the repository's labelled SRC04
NONRESPONDENT fixture configuration and fixture cells.  No original SAV is
stat'ed, hashed, opened, decoded, or read.  This module is review-owned and is
not a C/D author test.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import rawlsing_next._pre553_query_eval as qeval
from campaign_src04_completion.consumers.consumer import (
    ConsumerRefusal,
    DiscoveryConsumer,
    ProducerBundle,
    ProducerContract,
    consume_native_producer,
)
from campaign_src04_completion.empirical import fixture_native_workload_evidence as fixture_evidence
from campaign_src04_completion.empirical.native_workload import (
    NativeWorkloadRefusal,
    WorkloadPolicy,
    build_native_workload,
    execute_native_workload,
    plan_from_scope,
)
from rawlsing_next.pre553_c11_integrity import RespondentIdentity
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_discovery_exact import CANDIDATE_GRAMMAR_SCHEMA
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry, Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    DiscoveryAuthority,
    ExactRef,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query, replay_empirical_query
from rawlsing_next.pre553_observed_response import (
    ObservedResponseContract,
    ObservedResponseTopologyBinding,
    validate_contract_authority,
)
from rawlsing_next.source_configuration.factory import build_validated_c11_release_from_config
from rawlsing_next.source_configuration.fixture import (
    fixture_document_sha256,
    fixture_stream_from_document,
    load_fixture_stream,
)
from rawlsing_next.source_configuration.schema import SourceConfig, load_source_config

ROOT = Path(__file__).resolve().parents[3]
CONFIG_PATH = ROOT / "source_pre553_validation/SRC04/fixture.config.json"
FIXTURE_PATH = ROOT / "source_pre553_validation/SRC04/fixture.json"
SCOPE_PATH = ROOT / "campaign_src04_completion/empirical/SCOPE_LEDGER_V2.json"
CONTRACT_PATH = ROOT / "campaign_src04_completion/empirical/CONTRACT_APPROVAL_READY_V2.json"
OPERATION = fixture_evidence.OPERATION
TARGETS = fixture_evidence.TARGETS


class _FixtureContext:
    """Build the exact C fixture objects without invoking the C evidence writer."""

    def __init__(
        self,
        *,
        config_document: dict | None = None,
        fixture_document: dict | None = None,
    ) -> None:
        if config_document is None:
            self.config = load_source_config(CONFIG_PATH)
        else:
            self.config = SourceConfig(config_document)
        if fixture_document is None:
            self.stream = load_fixture_stream(FIXTURE_PATH)
        else:
            self.stream = fixture_stream_from_document(fixture_document)
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
        self.risk_set_ref = fixture_evidence._ref("RISK_SET", "fixture-observed-response")
        self.operation_authority = fixture_evidence._auth(
            "QUERY",
            "PREDICATE_GRAMMAR",
            (OPERATION,),
            ("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"),
            {
                "fixture_only": True,
                "grade": "NONRESPONDENT_FIXTURE_ONLY",
                "source_id": "SRC04",
                "source_sha256": fixture_evidence.ORIGINAL_SHA,
                "source_universe_refs": [self.universe.ref.as_dict()],
                "predicate_or_risk_set_refs": [self.risk_set_ref.as_dict()],
            },
        )
        self.release_authorities = tuple(
            obj for obj in self.release.public_objects if obj.schema_id == "AuthoritySnapshot"
        )
        self.registry = AuthorityRegistry((*self.release_authorities, self.operation_authority))
        self.repository = C11Repository((self.release,))
        bindings = []
        for question_id in TARGETS:
            question = self.questions[question_id]
            occurrence = self.responses[question_id]["values"][0]["occurrences"][0]
            bindings.append(ObservedResponseTopologyBinding(
                target_ref=exact_ref(question["native_question_ref"], "native_question_ref"),
                source_native_topology_ref=exact_ref(occurrence["topology_ref"], "topology_ref"),
                source_native_kind=occurrence["multiplicity_order_rank_fields"]["kind"],
                i03_topology="SCALAR_SINGULAR",
                topology_operation="R157_PREPARE_SOURCE_TOPOLOGY",
                topology_authority_ref=fixture_evidence.authority_ref(
                    question["topology_authority_ref"], "topology_authority_ref"),
                response_semantic_authority_refs=(
                    fixture_evidence.authority_ref(
                        question["semantic_authority_ref"], "semantic_authority_ref"),
                ),
            ))
        self.bindings = tuple(sorted(bindings, key=lambda binding: binding.target_ref.key))
        self.contract = ObservedResponseContract(
            contract_id="FIXTURE-NATIVE-OBSERVED-RESPONSE-V2",
            contract_version="2.0.0",
            contract_state="AUTHORIZED",
            authority_grade="NONRESPONDENT_FIXTURE_ONLY",
            source_id="SRC04",
            source_sha256=fixture_evidence.ORIGINAL_SHA,
            source_snapshot_ref=exact_ref(
                self.config.document["binding"]["source_snapshot_ref"], "source_snapshot_ref"),
            source_artifact_ref=self.release.source_artifact_ref,
            source_release_manifest_hash=self.release.source_release_manifest_hash,
            release_ref=self.release.release_ref,
            universe_ref=self.universe.ref,
            operation=OPERATION,
            operation_authority_ref=self.operation_authority.authority_ref,
            risk_set_ref=self.risk_set_ref,
            target_refs=tuple(binding.target_ref for binding in self.bindings),
            observed_states=("DK", "REFUSAL", "SOURCE_SPECIFIC_SPECIAL", "SUBSTANTIVE_RESPONSE"),
            missing_states=("MISSING",),
            denominator_policies=("CO_OBSERVED_TARGETS", "PER_TARGET_OBSERVED"),
            condition_observation_policy="ALL_REFERENCED_RESPONSE_VARIABLES_OBSERVED",
            topology_bindings=self.bindings,
        )
        self.policy = WorkloadPolicy(
            policy_id="FIXTURE-NATIVE-FINITE-FRONTIER",
            families=(
                "UNARY_OBSERVED_DISTRIBUTION",
                "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION",
                "SAME_RESPONDENT_JOINT_DISTRIBUTION",
            ),
            max_arity=2,
        )
        self.workload = build_native_workload(
            repository=self.repository,
            release_ref=self.release.release_ref,
            contract=self.contract,
            policy=self.policy,
        )
        self.executed = execute_native_workload(
            repository=self.repository,
            release_ref=self.release.release_ref,
            contract=self.contract,
            authority_registry=self.registry,
            policy=self.policy,
        )

    def operation(self, *, family: str, target_object_id: str | None = None):
        for operation in self.executed.operations:
            if operation.family != family:
                continue
            if target_object_id is not None and not any(
                target.object_id == target_object_id for target in operation.target_refs
            ):
                continue
            return operation
        raise AssertionError(f"operation not found: {family} {target_object_id}")

    def joined_bundle(self) -> tuple[ProducerBundle, object]:
        """Build the actual C fact plus an exact-scope D discovery recipient."""
        base = self.operation(
            family="UNARY_OBSERVED_DISTRIBUTION",
            target_object_id="urn:rawlsing:r157:fixture:SRC04:item:question_impl.phase0.b44503bdea5cce83bc79",
        )
        condition = next(
            operation for operation in self.executed.operations
            if operation.family == "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION"
            and operation.target_refs[0].key == base.target_refs[0].key
            and operation.condition_ref is not None
            and operation.condition_ref.object_id.endswith("04064b279e14d3d39123")
        )
        material = {
            "source_sha256": self.stream.source_sha256,
            "universe": self.universe.ref.as_dict(),
            "risk": self.risk_set_ref.as_dict(),
            "rule": "review-q236-conditioned",
        }
        discovery_snapshot = AuthoritySnapshot(
            typed_state="ALLOW",
            authority_snapshot_refs=(),
            dependency_refs=(),
            producer_replay_locator_or_reference_root=fixture_evidence._ref(
                "REPLAY_ROOT", "review-discovery-replay"),
            authority_id="REVIEW-SRC04-C-DISCOVERY",
            authority_version="1.0.0",
            authority_content_hash=semantic_hash(material),
            authority_kind="DISCOVERY_FRONTIER",
            decision_state="ALLOW",
            governed_operations=("REVIEW-SRC04-C-DISCOVERY@1.0.0",),
            governed_object_families=(
                "DiscoveryAuthority@1.0.0",
                "DiscoveryResultReceipt@1.0.0",
            ),
            scope_envelope={
                "fixture_only": True,
                "grade": "NONRESPONDENT_FIXTURE_ONLY",
                "source_id": "SRC04",
                "source_sha256": self.stream.source_sha256,
            },
            effective_time_or_interval="NONRESPONDENT_FIXTURE",
            parent_authority_refs=(),
            negative_limit_refs=(),
            supersession_refs=(),
            interpretation_semantics_fingerprint=semantic_hash({"semantics": material}),
            replay_protocol_ref=fixture_evidence._ref("REPLAY_PROTOCOL", "review-discovery"),
        )
        grammar = {
            "schema": CANDIDATE_GRAMMAR_SCHEMA,
            "discovery_operation": "REVIEW-SRC04-C-DISCOVERY@1.0.0",
            "atoms": (
                {
                    "atom_id": "BASELINE",
                    "predicate_ref": base.predicate.ref.as_dict(),
                    "kind": "BRANCH",
                    "ancestry_refs": (),
                },
                {
                    "atom_id": "CONDITION",
                    "predicate_ref": condition.predicate.ref.as_dict(),
                    "kind": "RESPONSE",
                    "ancestry_refs": (),
                },
            ),
            "query_templates": ({"template_id": "Q236", "query_ref": base.query.ref.as_dict()},),
            "rules": (
                {
                    "rule_id": "q236_conditioned_distribution",
                    "family": "BRANCH_CONDITIONED_DISTRIBUTION",
                    "form": "SINGLE_ATOM",
                    "atom_ids": ("CONDITION",),
                    "baseline_atom_id": "BASELINE",
                    "query_template_id": "Q236",
                    "validation": {"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
                },
            ),
            "limits": {"maximum_conditioner_arity_K": 1, "maximum_target_arity_J": 1},
            "allow_empty_frontier": False,
        }
        grammar_ref = ExactRef(
            "PRE553_I05_CANDIDATE_GRAMMAR",
            f"urn:review:src04:c:grammar:{semantic_hash(grammar)}",
            semantic_hash(grammar),
        )
        discovery_authority = DiscoveryAuthority(
            typed_state="EXACT_BOUNDED_AUTHORIZED",
            authority_snapshot_refs=(discovery_snapshot.authority_ref,),
            dependency_refs=(),
            producer_replay_locator_or_reference_root=fixture_evidence._ref(
                "REPLAY_ROOT", "review-discovery-authority"),
            candidate_grammar_ref=grammar_ref,
            candidate_universe_definition=grammar,
            source_universe_scope={"allowed_universe_refs": (self.universe.ref,)},
            risk_set_scope={"allowed_risk_set_refs": (self.risk_set_ref,)},
            topology_scope={"maximum_target_arity_J": 1},
            measure_scope={"allowed_measure_kinds": ("RAW",)},
            support_rules={"minimum_raw_denominator": 1},
            validation_rules={"kinds": ("DISTRIBUTION_DIFFERS_FROM_BASELINE",)},
            coverage_claim="COMPLETE_FOR_EXACT_DECLARED_FRONTIER",
            pruning_contract={"kind": "NONE_EXACT_EVALUATE_ALL"},
            algorithm_identity_if_semantically_required=(
                "PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0"
            ),
            tie_order_rules="CANONICAL_CANDIDATE_HASH_ORDER",
            rng_policy_if_any="NONE",
            mode="EXACT_BOUNDED",
            candidate_scoring_or_ranking_rule_if_any={
                "kind": "NONE",
                "controls_frontier": False,
            },
        )
        discovery = DiscoveryConsumer(
            authority=discovery_authority,
            authority_snapshot=discovery_snapshot,
            predicate_catalog=(base.predicate, condition.predicate),
            query_template_catalog=(base.query,),
            scope="SRC04_NONRESPONDENT_FIXTURE_ONLY",
        )
        registry = AuthorityRegistry((
            *self.release_authorities,
            self.operation_authority,
            discovery_snapshot,
        ))
        result = execute_empirical_query(
            repository=self.repository,
            query=base.query,
            predicate=base.predicate,
            authority_registry=registry,
            release_refs=(self.release.release_ref,),
        )
        fact = result.facts[0]
        contract = ProducerContract(
            source_id="SRC04",
            source_sha256=self.release.source_artifact_ref.content_hash,
            source_rows=self.stream.row_count,
            release_ref=self.release.release_ref,
            query_ref=base.query.ref,
            predicate_ref=base.predicate.ref,
            fact_ref=fact.ref,
            producer_family=(
                "C11LogicalRelease",
                "EmpiricalQuerySpec@1.0.0",
                "EmpiricalPredicate@1.0.0",
                "EmpiricalFact@1.0.0",
            ),
            evidence_tier="PARTIAL_AUTHORITY",
            claim_ceiling="SUPPORTED_COMPONENT_ONLY",
            use_scopes=("SUPPORTED_COMPONENT_ONLY",),
            native_authority_refs=tuple(fact.authority_snapshot_refs),
            fixture_only=True,
        )
        bundle = ProducerBundle(
            release=self.release,
            query=base.query,
            predicate=base.predicate,
            repository=self.repository,
            authority_registry=registry,
            contract=contract,
            discovery=discovery,
        )
        return bundle, fact

    def consume_joined(self) -> dict:
        bundle, fact = self.joined_bundle()
        product = consume_native_producer(
            bundle,
            expected_source_id="SRC04",
            requested_claim_ceiling="SUPPORTED_COMPONENT_ONLY",
            use_scope="SUPPORTED_COMPONENT_ONLY",
            allow_fixture_engineering=True,
        )
        return {"product": product, "fact": fact, "bundle": bundle}


@pytest.fixture(scope="module")
def context():
    return _FixtureContext()


def _unary(context):
    return context.operation(
        family="UNARY_OBSERVED_DISTRIBUTION",
        target_object_id="urn:rawlsing:r157:fixture:SRC04:item:question_impl.phase0.04064b279e14d3d39123",
    )


def test_c_unary_joint_and_conditional_ledgers_are_exact(context):
    unary = _unary(context)
    assert unary.status == "EXECUTED"
    assert unary.fact_state == "SUPPORTED"
    assert (unary.raw_numerator, unary.raw_denominator) == (7, 7)
    ledger = unary.observed_ledger
    assert ledger["scoped_respondents"] == 8
    assert ledger["target_observed"] == 7
    assert ledger["target_unobserved"] == 1
    assert ledger["denominator_policy"] == "PER_TARGET_OBSERVED"
    assert ledger["not_eligible_population_estimate"] is True
    assert ledger["risk_set_type"] == "OBSERVED_RESPONSE_RISK_SET"

    joint = next(
        operation for operation in context.executed.operations
        if operation.family == "SAME_RESPONDENT_JOINT_DISTRIBUTION"
    )
    assert joint.status == "EXECUTED"
    assert joint.raw_denominator == 6
    joint_ledger = joint.observed_ledger
    assert joint_ledger["denominator_policy"] == "CO_OBSERVED_TARGETS"
    assert joint_ledger["target_observed"] == 6
    assert joint_ledger["target_unobserved"] == 2
    assert joint_ledger["not_eligible_population_estimate"] is True

    conditional = next(
        operation for operation in context.executed.operations
        if operation.family == "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION"
    )
    assert conditional.status == "EXECUTED"
    assert conditional.condition_ref is not None
    assert conditional.condition_value_ref is not None
    assert conditional.observed_ledger["condition_observation_policy"] == (
        "ALL_REFERENCED_RESPONSE_VARIABLES_OBSERVED"
    )
    assert conditional.observed_ledger["denominator_policy"] == "PER_TARGET_OBSERVED"
    assert conditional.observed_ledger["condition_unobserved"] == 1
    assert conditional.observed_ledger["condition_false"] == 5
    assert conditional.observed_ledger["denominator"] == 1
    assert conditional.observed_ledger["not_eligible_population_estimate"] is True


def test_c_workload_resume_scope_and_finite_arity(context):
    assert len(context.workload.operations) == 44
    assert context.executed.accounting["executed_operations"] == 44
    assert context.executed.accounting["refused_operations"] == 0
    assert context.executed.accounting["operations_by_family"] == {
        "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION": 38,
        "SAME_RESPONDENT_JOINT_DISTRIBUTION": 3,
        "UNARY_OBSERVED_DISTRIBUTION": 3,
    }
    assert context.executed.accounting["requested_higher_order_not_authorized"] == 1
    assert not any(
        operation.family == "HIGHER_ORDER_CO_OBSERVED_JOINT"
        for operation in context.executed.operations
    )
    conditional = [
        operation for operation in context.executed.operations
        if operation.family == "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION"
    ]
    assert len(conditional) == 38
    assert all(
        operation.condition_ref is not None
        and operation.condition_value_ref is not None
        and operation.query is not None
        and operation.predicate is not None
        for operation in conditional
    )
    assert all(
        "ser" not in target.object_id
        for operation in context.executed.operations
        for target in operation.target_refs
    )
    resumed = execute_native_workload(
        repository=context.repository,
        release_ref=context.release.release_ref,
        contract=context.contract,
        authority_registry=context.registry,
        policy=context.policy,
        start_after_operation_id=context.workload.operations[0].operation_id,
    )
    assert resumed.accounting["executed_operations"] == 43
    assert resumed.operations[0].operation_id == context.workload.operations[0].operation_id
    assert resumed.operations[0].fact_ref is None
    replayed = replay_empirical_query(
        repository=context.repository,
        query=_unary(context).query,
        predicate=_unary(context).predicate,
        authority_registry=context.registry,
        release_refs=(context.release.release_ref,),
        expected_fact_refs=(_unary(context).fact_ref,),
    )
    assert replayed.facts[0].ref == _unary(context).fact_ref


def _mutated_fixture_context() -> _FixtureContext:
    """Change one labelled q236 fixture cell in memory; never write a source file."""
    config_doc = deepcopy(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
    fixture_doc = deepcopy(json.loads(FIXTURE_PATH.read_text(encoding="utf-8")))
    changed = False
    for cell in fixture_doc["cells"]:
        if (
            cell.get("variable_name") == "q236"
            and cell.get("row_ordinal") == 3
            and cell.get("raw_value") == 95.0
        ):
            cell["raw_value"] = 1.0
            changed = True
            break
    if not changed:
        raise AssertionError("fixture q236 mutation point absent")
    new_sha = fixture_document_sha256(fixture_doc)
    fixture_doc["fixture_source_sha256"] = new_sha
    config_doc["binding"]["source_sha256"] = new_sha
    config_doc["binding"]["source_snapshot_ref"]["content_hash"] = new_sha
    config_doc["config_id"] = f"{config_doc['config_id']}-REVIEW-Q236-MUTATED"
    return _FixtureContext(config_document=config_doc, fixture_document=fixture_doc)


def test_c_observed_profile_does_not_use_eligible_risk_membership(context, monkeypatch):
    with pytest.raises(Exception, match="unresolved"):
        qeval._risk_membership(
            ("ROUTING_UNKNOWN",),
            profile=SimpleNamespace(risk_set_type="WHOLE_QUESTION_RISK_SET"),
        )

    def forbidden(*args, **kwargs):
        raise AssertionError("_risk_membership must not be called for observed profiles")

    monkeypatch.setattr(qeval, "_risk_membership", forbidden)
    unary = _unary(context)
    assert unary.fact_state == "SUPPORTED"


def test_c_authority_fixture_promotion_and_identity_refusals(context):
    with pytest.raises(Pre553AuthorityError, match="fixture-only"):
        validate_contract_authority(
            replace(context.contract, authority_grade="ORIGINAL_SCIENTIFIC"),
            context.registry,
        )
    with pytest.raises(NativeWorkloadRefusal, match="CONTRACT_RELEASE_MISMATCH"):
        build_native_workload(
            repository=context.repository,
            release_ref=context.release.release_ref,
            contract=replace(
                context.contract,
                release_ref=ExactRef("C11LogicalRelease", "urn:test:wrong-release", "0" * 64),
            ),
            policy=context.policy,
        )
    with pytest.raises(NativeWorkloadRefusal, match="CONTRACT_SOURCE_ARTIFACT_MISMATCH"):
        build_native_workload(
            repository=context.repository,
            release_ref=context.release.release_ref,
            contract=replace(
                context.contract,
                source_artifact_ref=ExactRef(
                    "SOURCE_ARTIFACT", "urn:test:wrong-source-artifact", "1" * 64),
            ),
            policy=context.policy,
        )
    wrong_authority = AuthorityRef("REVIEW-WRONG-AUTHORITY", "1.0.0", "2" * 64)
    with pytest.raises(Pre553AuthorityError):
        validate_contract_authority(
            replace(context.contract, operation_authority_ref=wrong_authority),
            context.registry,
        )


def test_d_joined_path_is_positive_but_currently_omits_observed_ledger_DEFECT(context):
    joined = context.consume_joined()
    product = joined["product"]
    fact = joined["fact"]
    assert product["status"] == "FIXTURE_ONLY_NATIVE_ENGINEERING_POSITIVE"
    assert product["downstream_value_effect"] == "SUBSTANTIVE_DISCOVERY_RESULT_SUPPORTED"
    assert product["downstream_discovery"]["supported_candidate_count"] >= 1
    assert product["fact_ref"] == fact.ref.as_dict()

    observed = fact.target_topology["observed_response"]
    assert observed["status"] == "OBSERVED_RESPONSE_NOT_ELIGIBLE_POPULATION"
    assert observed["not_eligible_population_estimate"] is True
    assert observed["ledger"]["target_observed"] == 7
    assert observed["ledger"]["target_unobserved"] == 1
    assert observed["ledger"]["denominator_policy"] == "PER_TARGET_OBSERVED"

    # Falsifiable current failure: the real consumer product has no observed
    # status, contract provenance, or ledger, and its discovery facts omit the
    # same fields.  This is the REVISE discriminator, not a C/D acceptance claim.
    assert "observed_response" not in product
    assert "observed_ledger" not in product
    assert all(
        "observed_response" not in item
        for item in product["downstream_discovery"]["empirical_facts"]
    )


def test_d_joined_value_change_and_restoration(context):
    original = context.consume_joined()["product"]
    mutated = _mutated_fixture_context().consume_joined()["product"]
    restored = context.consume_joined()["product"]
    assert mutated["source_sha256"] != original["source_sha256"]
    assert mutated["fact_ref"] != original["fact_ref"]
    assert (
        mutated["downstream_discovery"]["empirical_fact_refs"]
        != original["downstream_discovery"]["empirical_fact_refs"]
    )
    assert restored["source_sha256"] == original["source_sha256"]
    assert restored["fact_ref"] == original["fact_ref"]
    assert (
        restored["downstream_discovery"]["empirical_fact_refs"]
        == original["downstream_discovery"]["empirical_fact_refs"]
    )


def test_d_joined_refusals_are_exact(context):
    joined = context.consume_joined()
    bundle = joined["bundle"]
    common = {
        "expected_source_id": "SRC04",
        "requested_claim_ceiling": "SUPPORTED_COMPONENT_ONLY",
        "use_scope": "SUPPORTED_COMPONENT_ONLY",
        "allow_fixture_engineering": True,
    }
    wrong_source = replace(bundle.contract, source_sha256="0" * 64)
    with pytest.raises(ConsumerRefusal) as exc:
        consume_native_producer(replace(bundle, contract=wrong_source), **common)
    assert exc.value.code == "NATIVE_SOURCE_IDENTITY_MISMATCH"

    wrong_release = replace(
        bundle.contract,
        release_ref=ExactRef("C11LogicalRelease", "urn:test:wrong-release", "1" * 64),
    )
    with pytest.raises(ConsumerRefusal) as exc:
        consume_native_producer(replace(bundle, contract=wrong_release), **common)
    assert exc.value.code == "WRONG_RELEASE_IDENTITY"

    wrong_fact = replace(
        bundle.contract,
        fact_ref=ExactRef("EmpiricalFact@1.0.0", "urn:test:wrong-fact", "2" * 64),
    )
    with pytest.raises(ConsumerRefusal) as exc:
        consume_native_producer(replace(bundle, contract=wrong_fact), **common)
    assert exc.value.code == "FACT_SET_MISMATCH"

    missing_authority = replace(
        bundle.contract,
        native_authority_refs=(),
        policy_authority_refs=(),
    )
    with pytest.raises(ConsumerRefusal) as exc:
        consume_native_producer(replace(bundle, contract=missing_authority), **common)
    assert exc.value.code == "MISSING_AUTHORITY"


def test_scope_ledger_is_current_175_fields_and_residuals_are_explicit():
    import json

    scope = json.loads(SCOPE_PATH.read_text(encoding="utf-8"))
    raw_contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    contract = ObservedResponseContract.from_mapping(raw_contract["contract"])
    policy = WorkloadPolicy.from_mapping(scope["workload_policy"])
    plan = plan_from_scope(scope=scope, contract=contract, policy=policy)
    assert scope["physical_accounting"]["available_response_fields"] == 175
    assert scope["physical_accounting"]["held_response_fields"] == 3
    assert scope["physical_accounting"]["all_181_slots_accounted"] is True
    assert set(scope["held_field_ids"]) == {
        "q217", "q715withoutmorocco", "q716withoutmorocco",
    }
    assert len(contract.target_refs) == 175
    assert plan["operations"]["unary_operations"] == 175
    assert plan["operations"]["joint_pair_operations"] == 15_225
    assert plan["operations"]["conditional_target_pairs_awaiting_release_values"] == 30_450
    assert plan["operations"]["higher_order_requested_not_authorized"] == 877_975
    ser = next(item for item in scope["coordinate_ledger"] if item["name"] == "ser")
    assert ser["status"] == "IDENTITY_ONLY"
    assert ser["analytical_eligible"] is False
