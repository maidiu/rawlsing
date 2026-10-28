"""Retained B0 SRC09 nonrespondent fixture native engineering seam.

This module reconstructs the already-retained B0 P0 fixture objects through the
existing source-configuration, C11, I03 and discovery owners.  It is deliberately
fixture/test-only: the source is SRC09's repository-generated nonrespondent
fixture, not original SRC04 and not an original respondent product.

The fixture files are exact copies of the B0 commit's P0 example fixture.  No
original SRC04 or SRC09 source file is read here.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Mapping

from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_discovery_exact import CANDIDATE_GRAMMAR_SCHEMA
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    DiscoveryAuthority,
    ExactRef,
    exact_ref,
    make_empirical_predicate,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_native_workload_binding import (
    OperationFixture,
    build_projection_catalog,
)
from rawlsing_next.source_configuration.factory import (
    build_governed_c11_projection,
    build_validated_c11_release_from_config,
)
from rawlsing_next.source_configuration.fixture import (
    fixture_document_sha256,
    fixture_stream_from_document,
)
from rawlsing_next.source_configuration.schema import SourceConfig

from .consumer import (
    DiscoveryConsumer,
    ProducerBundle,
    ProducerContract,
    SUPPORTED_COMPONENT_CLAIM,
)

LANE = Path(__file__).resolve().parent
FIXTURE_DIR = LANE / "evidence" / "b0_fixture"
CONFIG_PATH = FIXTURE_DIR / "SRC09_q101_fixture.config.json"
FIXTURE_PATH = FIXTURE_DIR / "SRC09_q101_nonrespondent.json"

B0_FIXTURE_CONFIG_SHA256 = "f69e2ec3bf514da34f1d9e0d60b2cf51e8ac0879655d7a4ad7cec609877359d6"
B0_FIXTURE_FILE_SHA256 = "cc7a587a57943251acbef1679a8a4aff808c6c65ff399c06428026d3371efb1d"
B0_FIXTURE_SOURCE_SHA256 = "a93b4dab00a2b7cbd559d8a0bb1ca498caaa87f27bd1bd73e9fceb0f2820a491"
B0_FIXTURE_RELEASE_SHA256 = "9a6db7b4aa8b5d7bbd8d366dec55e60fd07cb956d2935f1d7d705ecf99f10e3f"
B0_FIXTURE_FACT_SHA256 = "a377bc42e15134ca8774fe5940ab537789cb5797bf3c2e72e8db981b4869cecc"
B0_FIXTURE_SCOPE = "NONRESPONDENT_FIXTURE_ONLY__NOT_ORIGINAL_NOT_SRC04"
DISCOVERY_OPERATION = "I03-OP-B0-SRC09-Q101-DISCOVERY"


class B0NativeFixtureRefusal(ValueError):
    """Refusal to rebuild the retained B0 engineering fixture."""

    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


def _sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _jsonable(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _derived_ref(kind: str, namespace: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:rawlsing:campaign-src04-completion:{namespace}:sha256:{digest}", digest)


def _b0_fixture_material() -> tuple[dict[str, Any], dict[str, Any]]:
    if _sha_file(CONFIG_PATH) != B0_FIXTURE_CONFIG_SHA256:
        raise B0NativeFixtureRefusal("B0_FIXTURE_CONFIG_SHA_MISMATCH")
    if _sha_file(FIXTURE_PATH) != B0_FIXTURE_FILE_SHA256:
        raise B0NativeFixtureRefusal("B0_FIXTURE_FILE_SHA_MISMATCH")
    config_doc = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    fixture_doc = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return config_doc, fixture_doc


def _fixture_source_sha(fixture_doc: Mapping[str, Any]) -> str:
    return str(fixture_doc["fixture_source_sha256"])


def _mutate_q101_2_to_1(
    config_doc: dict[str, Any], fixture_doc: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Apply one explicit fixture-only upstream value mutation.

    The mutation changes exactly one synthetic q101 cell from 2.0 to 1.0.  It is
    an engineering value-sensitivity probe, never a scientific edit.
    """
    config_doc = deepcopy(config_doc)
    fixture_doc = deepcopy(fixture_doc)
    changed = False
    for cell in fixture_doc["cells"]:
        if cell.get("variable_name") == "q101" and cell.get("raw_value") == 2.0:
            cell["raw_value"] = 1.0
            changed = True
            break
    if not changed:
        raise B0NativeFixtureRefusal("B0_MUTATION_POINT_NOT_FOUND")
    fixture_doc["fixture_source_sha256"] = fixture_document_sha256(fixture_doc)
    config_doc["config_id"] = f"{config_doc['config_id']}-MUTATED-Q101-2-TO-1"
    config_doc["binding"]["source_sha256"] = fixture_doc["fixture_source_sha256"]
    config_doc["binding"]["source_snapshot_ref"]["content_hash"] = fixture_doc["fixture_source_sha256"]
    return config_doc, fixture_doc


def _substantive_q101_member_refs(release: Any, question_ref: ExactRef) -> tuple[ExactRef, ...]:
    members: list[ExactRef] = []
    for obj in release.public_objects:
        if getattr(obj, "schema_id", None) != "RespondentEvent":
            continue
        if getattr(obj, "typed_state", None) != "SUBSTANTIVE_RESPONSE":
            continue
        if exact_ref(obj.native_question_ref).key != question_ref.key:
            continue
        members.append(exact_ref(obj.scoped_respondent_ref))
    if not members:
        raise B0NativeFixtureRefusal("B0_SUBSTANTIVE_MEMBERS_EMPTY")
    return tuple(sorted(set(members), key=lambda ref: ref.key))


def _subset_branch_predicate(
    baseline: Any,
    *,
    members: tuple[ExactRef, ...],
    fixture_source_sha256: str,
) -> Any:
    material = {
        "fixture_source_sha256": fixture_source_sha256,
        "member_refs": [ref.as_dict() for ref in members],
        "parent": "B0_SRC09_Q101_SUBSTANTIVE",
    }
    membership_ref = _derived_ref("BRANCH_MEMBERSHIP", "b0-q101-substantive-membership", material)
    replay_ref = _derived_ref("BRANCH_REPLAY", "b0-q101-substantive-replay", material)
    ast = dict(baseline.predicate_ast)
    ast["branch_definition_id"] = "BRANCH-B0-SRC09-Q101-SUBSTANTIVE"
    ast["resolved_predicate_hash_or_exact_membership_ref"] = membership_ref
    ast["branch_membership_replay_ref"] = replay_ref
    ast["exact_member_respondent_refs"] = members
    return make_empirical_predicate(
        predicate_ast=ast,
        typed_state=baseline.typed_state,
        authority_snapshot_refs=baseline.authority_snapshot_refs,
        dependency_refs=baseline.dependency_refs,
        producer_replay_locator_or_reference_root=replay_ref,
        grammar_authority_ref=baseline.grammar_authority_ref,
        coordinate_question_value_refs=baseline.coordinate_question_value_refs,
        risk_set_refs=baseline.risk_set_refs,
        scope_refs=baseline.scope_refs,
        same_respondent_binding_semantics=baseline.same_respondent_binding_semantics,
        operator_semantics_refs=baseline.operator_semantics_refs,
    )


def _discovery_consumer(
    *,
    release: Any,
    projection: Any,
    fixture_source_sha256: str,
    baseline: Any,
    response_predicate: Any,
    query: Any,
    risk_set_ref: ExactRef,
) -> DiscoveryConsumer:
    members = _substantive_q101_member_refs(release, exact_ref(query.target_refs[0]))
    subset_baseline = _subset_branch_predicate(
        baseline,
        members=members,
        fixture_source_sha256=fixture_source_sha256,
    )
    scope_material = {
        "fixture_source_sha256": fixture_source_sha256,
        "operation": DISCOVERY_OPERATION,
        "baseline_fact_members": [ref.as_dict() for ref in members],
    }
    snapshot = AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_derived_ref(
            "REPLAY_ROOT", "b0-q101-discovery-authority-replay", scope_material
        ),
        authority_id="B0-TEST-ONLY-I05-DISCOVERY",
        authority_version="1.0.0",
        authority_content_hash=semantic_hash({"b0_discovery_authority": scope_material}),
        authority_kind="DISCOVERY_FRONTIER",
        decision_state="ALLOW",
        governed_operations=(DISCOVERY_OPERATION,),
        governed_object_families=(
            "DiscoveryAuthority@1.0.0",
            "DiscoveryResultReceipt@1.0.0",
        ),
        scope_envelope={
            "fixture_only": True,
            "grade": "NONRESPONDENT_FIXTURE_ONLY",
            "source_id": "SRC09",
            "source_sha256": fixture_source_sha256,
        },
        effective_time_or_interval="B0_P0_FIXTURE",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash(
            {"b0_discovery_semantics": scope_material}
        ),
        replay_protocol_ref=_derived_ref(
            "REPLAY_PROTOCOL", "b0-q101-discovery-replay-protocol", scope_material
        ),
    )
    grammar = {
        "schema": CANDIDATE_GRAMMAR_SCHEMA,
        "discovery_operation": DISCOVERY_OPERATION,
        "atoms": (
            {
                "atom_id": "SUBSTANTIVE_Q101_BASELINE",
                "predicate_ref": subset_baseline.ref,
                "kind": "BRANCH",
                "ancestry_refs": (),
            },
            {
                "atom_id": "Q101_EQ_1",
                "predicate_ref": response_predicate.ref,
                "kind": "RESPONSE",
                "ancestry_refs": (),
            },
        ),
        "query_templates": (
            {"template_id": "Q101", "query_ref": query.ref},
        ),
        "rules": (
            {
                "rule_id": "q101_substantive_distribution",
                "family": "PAIR_RESPONSE_COTRAVEL",
                "form": "SINGLE_ATOM",
                "atom_ids": ("Q101_EQ_1",),
                "baseline_atom_id": "SUBSTANTIVE_Q101_BASELINE",
                "query_template_id": "Q101",
                "validation": {"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            },
        ),
        "limits": {
            "maximum_conditioner_arity_K": 1,
            "maximum_target_arity_J": 4,
        },
        "allow_empty_frontier": False,
    }
    grammar_ref = ExactRef(
        "PRE553_I05_CANDIDATE_GRAMMAR",
        f"urn:rawlsing:campaign-src04-completion:b0-q101-grammar:sha256:{semantic_hash(grammar)}",
        semantic_hash(grammar),
    )
    authority = DiscoveryAuthority(
        typed_state="EXACT_BOUNDED_AUTHORIZED",
        authority_snapshot_refs=(snapshot.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_derived_ref(
            "REPLAY_ROOT", "b0-q101-discovery-authority", scope_material
        ),
        candidate_grammar_ref=grammar_ref,
        candidate_universe_definition=grammar,
        source_universe_scope={"allowed_universe_refs": (projection.universes[0].ref,)},
        risk_set_scope={"allowed_risk_set_refs": (risk_set_ref,)},
        topology_scope={"maximum_target_arity_J": 4},
        measure_scope={"allowed_measure_kinds": ("RAW", "GOVERNED_WEIGHTED")},
        support_rules={"minimum_raw_denominator": 1},
        validation_rules={"kinds": ("DISTRIBUTION_DIFFERS_FROM_BASELINE",)},
        coverage_claim="COMPLETE_FOR_EXACT_DECLARED_FRONTIER",
        pruning_contract={"kind": "NONE_EXACT_EVALUATE_ALL"},
        algorithm_identity_if_semantically_required="PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0",
        tie_order_rules="CANONICAL_CANDIDATE_HASH_ORDER",
        rng_policy_if_any="NONE",
        mode="EXACT_BOUNDED",
        candidate_scoring_or_ranking_rule_if_any={"kind": "NONE", "controls_frontier": False},
    )
    return DiscoveryConsumer(
        authority=authority,
        authority_snapshot=snapshot,
        predicate_catalog=(subset_baseline, response_predicate),
        query_template_catalog=(query,),
        scope=B0_FIXTURE_SCOPE,
    )


def load_b0_native_bundle(*, mutate_q101_2_to_1: bool = False) -> ProducerBundle:
    """Build the exact B0 fixture-native bundle, optionally with one value probe."""
    config_doc, fixture_doc = _b0_fixture_material()
    expected_source_sha = _fixture_source_sha(fixture_doc)
    if expected_source_sha != B0_FIXTURE_SOURCE_SHA256:
        raise B0NativeFixtureRefusal("B0_FIXTURE_SOURCE_SHA_MISMATCH")
    if mutate_q101_2_to_1:
        config_doc, fixture_doc = _mutate_q101_2_to_1(config_doc, fixture_doc)
        expected_source_sha = _fixture_source_sha(fixture_doc)
    config = SourceConfig(config_doc)
    stream = fixture_stream_from_document(fixture_doc)
    if stream.source_sha256 != expected_source_sha:
        raise B0NativeFixtureRefusal("B0_STREAM_SOURCE_SHA_MISMATCH")
    projection = build_governed_c11_projection(
        config, source_sha256=stream.source_sha256, row_count=stream.row_count
    )
    release = build_validated_c11_release_from_config(config, stream=stream)
    if not mutate_q101_2_to_1 and release.release_ref.content_hash != B0_FIXTURE_RELEASE_SHA256:
        raise B0NativeFixtureRefusal("B0_FIXTURE_RELEASE_HASH_MISMATCH")
    question_refs = {
        q["question_id"]: exact_ref(q["native_question_ref"], "b0_question_ref")
        for q in config.document["questions"]
    }
    route = next(
        x for x in config.document["routing"] if x["question_id"] == "q101"
    )
    risk_ref = exact_ref(route["risk_set_ref"], "b0_risk_set_ref")
    bundle = SimpleNamespace(
        projection=projection,
        source_sha256=stream.source_sha256,
        question_refs=question_refs,
        administered_ids=tuple(question_refs),
        risk_set_ref=risk_ref,
        source_format="SAV",
        physical_stream=stream,
        release=release,
        administered=(),
        held=(),
        excluded=(),
        unknown=(),
        bundle_hash="b0-native-fixture-bundle",
        respondent_rows=(),
        occurrence_bindings=(),
    )
    catalog, request = build_projection_catalog(
        bundle=bundle,
        operation=OperationFixture(
            fixture_id="B0-SRC09-P0-FIXTURE-Q101",
            target_variable_code="q101",
            response_value="1",
            measure_kind="RAW",
        ),
        as_of="2026-10-27",
    )
    query = catalog.resolve_query_exact(request.query_ref)
    predicate = catalog.resolve_predicate_exact(request.predicate_ref)
    registry = AuthorityRegistry((*catalog.authorities,))
    repository = C11Repository((release,))
    execution = execute_empirical_query(
        repository=repository,
        query=query,
        predicate=predicate,
        authority_registry=registry,
        release_refs=(release.release_ref,),
    )
    if len(execution.facts) != 1:
        raise B0NativeFixtureRefusal("B0_FACT_COUNT_NOT_ONE")
    fact = execution.facts[0]
    if fact.typed_state != "SUPPORTED":
        raise B0NativeFixtureRefusal("B0_FACT_NOT_SUPPORTED", fact.typed_state)
    expected = 2 if mutate_q101_2_to_1 else 1
    if fact.raw_numerator_support != expected or fact.raw_denominator_support != expected:
        raise B0NativeFixtureRefusal(
            "B0_SUPPORT_MISMATCH",
            f"{fact.raw_numerator_support}/{fact.raw_denominator_support} expected {expected}/{expected}",
        )
    if not mutate_q101_2_to_1 and fact.ref.content_hash != B0_FIXTURE_FACT_SHA256:
        raise B0NativeFixtureRefusal("B0_FIXTURE_FACT_HASH_MISMATCH", fact.ref.content_hash)
    baseline = next(
        p for p in catalog.predicates
        if p.predicate_ast.get("leaf_type") == "DERIVED_BRANCH_COHORT"
    )
    discovery = _discovery_consumer(
        release=release,
        projection=projection,
        fixture_source_sha256=stream.source_sha256,
        baseline=baseline,
        response_predicate=predicate,
        query=query,
        risk_set_ref=risk_ref,
    )
    contract = ProducerContract(
        source_id="SRC09",
        source_sha256=stream.source_sha256,
        source_rows=stream.row_count,
        release_ref=release.release_ref,
        query_ref=query.ref,
        predicate_ref=predicate.ref,
        fact_ref=fact.ref,
        producer_family=(
            "C11LogicalRelease",
            "EmpiricalQuerySpec@1.0.0",
            "EmpiricalPredicate@1.0.0",
            "EmpiricalFact@1.0.0",
        ),
        evidence_tier="PARTIAL_AUTHORITY",
        claim_ceiling=SUPPORTED_COMPONENT_CLAIM,
        use_scopes=(SUPPORTED_COMPONENT_CLAIM,),
        native_authority_refs=tuple(fact.authority_snapshot_refs),
        fixture_only=True,
    )
    return ProducerBundle(
        release=release,
        query=query,
        predicate=predicate,
        repository=repository,
        authority_registry=AuthorityRegistry((*catalog.authorities, discovery.authority_snapshot)),
        contract=contract,
        discovery=discovery,
    )


def b0_native_identity(*, mutate_q101_2_to_1: bool = False) -> dict[str, Any]:
    """Return identity material for evidence without exposing fixture cells."""
    bundle = load_b0_native_bundle(mutate_q101_2_to_1=mutate_q101_2_to_1)
    return {
        "scope": B0_FIXTURE_SCOPE,
        "fixture_config_path": str(CONFIG_PATH.relative_to(LANE)),
        "fixture_config_file_sha256": _sha_file(CONFIG_PATH),
        "fixture_path": str(FIXTURE_PATH.relative_to(LANE)),
        "fixture_file_sha256": _sha_file(FIXTURE_PATH),
        "fixture_source_sha256": bundle.contract.source_sha256,
        "fixture_release_ref": bundle.contract.release_ref.as_dict(),
        "fixture_query_ref": bundle.contract.query_ref.as_dict(),
        "fixture_predicate_ref": bundle.contract.predicate_ref.as_dict(),
        "fixture_fact_ref": bundle.contract.fact_ref.as_dict(),
        "fixture_only": True,
        "original_source_read": False,
        "respondent_cells_emitted": False,
    }


__all__ = [
    "B0_FIXTURE_SCOPE",
    "B0NativeFixtureRefusal",
    "b0_native_identity",
    "load_b0_native_bundle",
]
