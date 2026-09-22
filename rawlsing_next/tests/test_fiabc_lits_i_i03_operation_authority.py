from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest

from rawlsing_next.fiabc_lits_i_i03_operation_authority import (
    AUTHORITY_CONTENT_HASH,
    NEGATIVE_LIMITS,
    PART_A_PROJECTION_AUTHORITY_HASH,
    QUERY_REFS,
    RUNTIME_CATALOG_IDENTITY,
    SCHEMA,
    historical_projection_authority_snapshot,
    operation_successor_authority_record,
)
from rawlsing_next.fiabc_lits_i_d03_risk_set_authority import (
    AUTHORITY_CONTENT_HASH as D03_AUTHORITY_CONTENT_HASH,
    Q301_2_REF,
    Q301_7_REF,
    RELEASE_REFS,
    RELEASE_REF,
    RISK_SET_REF,
    ROOTS,
    ROW_COUNT,
    SCHEMA as D03_SCHEMA,
    SUCCESSOR_RELEASE_REF,
    UNIVERSE_REF,
    decode_membership_payload,
    risk_set_successor_authority_record,
)
from rawlsing_next.fiabc_lits_i_f02_event_representation_authority import (
    AUTHORITY_CONTENT_HASH as F02_REPRESENTATION_AUTHORITY_CONTENT_HASH,
    FROZEN_SCOPE_REF as F02_FROZEN_SCOPE_REF,
    QUESTION_REFS as F02_QUESTION_REFS,
    RESPONSE_HASHES as F02_RESPONSE_HASHES,
    SCHEMA as F02_REPRESENTATION_SCHEMA,
    SOURCE_SHA256 as F02_SOURCE_SHA256,
    SUCCESSOR_RELEASE_REF as F02_SUCCESSOR_RELEASE_REF,
    event_representation_successor_authority_record,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry, Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import exact_ref, semantic_hash
from rawlsing_next.pre553_empirical_query import _require_exact_i03_authority_fitness
from rawlsing_next.pre553_runtime_authority import Pre553RuntimeAuthoritySet
from rawlsing_next.pre553_runtime_context import bind_runtime


REPO = Path(__file__).resolve().parents[2]
MATERIALIZER = REPO / "rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py"


def _runtime_module():
    spec = importlib.util.spec_from_file_location("fiabc_lits_i03_runtime_test", MATERIALIZER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _catalog(package):
    return RuntimeObjectCatalog.from_documents(
        authority_documents=package["authority_documents"],
        predicate_documents=package["predicate_documents"],
        query_documents=package["query_documents"],
        discovery_authority_documents=package["discovery_authority_documents"],
    )


def test_lits_i03_operation_successor_record_is_exact_and_narrow():
    record = operation_successor_authority_record()
    assert record["schema"] == SCHEMA
    assert record["authority_content_hash"] == AUTHORITY_CONTENT_HASH
    assert semantic_hash(record["identity_material"]) == AUTHORITY_CONTENT_HASH
    assert record["identity_material"]["runtime_catalog_identity"] == RUNTIME_CATALOG_IDENTITY
    assert len(record["identity_material"]["query_refs"]) == 60
    assert record["identity_material"]["frozen_workload"] == {
        "candidate_count": 50,
        "query_role_executions": 77,
    }
    assert "NO_GENERIC_OPERATION_ALIAS" in NEGATIVE_LIMITS
    assert "NO_OTHER_QUERY_REFS" in NEGATIVE_LIMITS
    assert "NO_CANDIDATE_OUTPUT_PARENTAGE" in NEGATIVE_LIMITS


def test_lits_historical_projection_authority_is_exact_runtime_only_closure():
    snapshot = historical_projection_authority_snapshot()
    assert snapshot.authority_ref.authority_content_hash == PART_A_PROJECTION_AUTHORITY_HASH
    assert snapshot.governed_operations == ("AS2B_LITS1_PART_A_PROJECTION",)
    assert set(snapshot.governed_object_families) == {
        "EmpiricalUniverse@1.0.0",
        "RespondentEvent@1.0.0",
        "EmpiricalCoordinateFact@1.0.0",
        "RoutingEligibilityFact@1.0.0",
    }
    registry = AuthorityRegistry(())
    with pytest.raises(Pre553AuthorityError, match="historical authority unavailable"):
        registry.resolve_exact(snapshot.authority_ref)

    module = _runtime_module()
    with bind_runtime(module.materialize_runtime_authority_set()):
        assert registry.resolve_exact(snapshot.authority_ref).snapshot == snapshot


def test_lits_frozen_catalog_is_unchanged_and_exact_successor_closes_i03_gate():
    module = _runtime_module()
    package = module.materialize_runtime_package()
    assert package["runtime_catalog_identity"] == RUNTIME_CATALOG_IDENTITY
    catalog, candidates, *_ = module.catalog_and_frontier()
    assert {
        role.query.ref for candidate in candidates for role in candidate.query_roles
    } == set(QUERY_REFS)
    runtime = module.materialize_runtime_authority_set()

    for candidate in candidates:
        for role in candidate.query_roles:
            query = role.query
            predicate = role.predicate
            universe_refs = tuple(
                exact_ref(value) for value in query.empirical_universe_refs
            )
            with pytest.raises(Pre553AuthorityError):
                _require_exact_i03_authority_fitness(
                    query=query,
                    predicate=predicate,
                    authority_registry=catalog.authority_registry,
                    universe_refs=universe_refs,
                )
            with bind_runtime(runtime):
                _require_exact_i03_authority_fitness(
                    query=query,
                    predicate=predicate,
                    authority_registry=catalog.authority_registry,
                    universe_refs=universe_refs,
                )


def test_lits_i03_successor_rejects_unadopted_or_tampered_record():
    record = operation_successor_authority_record()
    with pytest.raises(Pre553AuthorityError, match="not exactly adopted"):
        Pre553RuntimeAuthoritySet(i03_operation_successor_authorities=(record,))

    tampered = copy.deepcopy(record)
    tampered["identity_material"]["successor_operation"] = "OTHER_OPERATION"
    with pytest.raises(Pre553AuthorityError, match="identity_material hash mismatch"):
        Pre553RuntimeAuthoritySet(
            adopted_authority_hashes=(AUTHORITY_CONTENT_HASH,),
            i03_operation_successor_authorities=(tampered,),
        )


def test_lits_d03_risk_set_payload_is_exact_lossless_authority():
    record = risk_set_successor_authority_record()
    assert record["schema"] == D03_SCHEMA
    assert semantic_hash(record["identity_material"]) == D03_AUTHORITY_CONTENT_HASH
    memberships = decode_membership_payload()
    assert {key: len(value) for key, value in memberships.items()} == {
        key: row["member_count"] for key, row in ROOTS.items()
    }
    assert memberships["R27"] == memberships["R2"] & memberships["R7"]
    assert min(memberships["R2"]) >= 1
    assert max(memberships["R7"]) <= ROW_COUNT


def test_lits_d03_risk_set_contract_is_exact_query_and_scope_only():
    module = _runtime_module()
    _catalog, candidates, *_ = module.catalog_and_frontier()
    runtime = module.materialize_runtime_authority_set()
    by_targets = {}
    for candidate in candidates:
        for role in candidate.query_roles:
            targets = tuple(exact_ref(ref) for ref in role.query.target_refs)
            by_targets.setdefault(targets, role.query)

    memberships = decode_membership_payload()
    for targets, root_id in {
        (Q301_2_REF,): "R2",
        (Q301_7_REF,): "R7",
        (Q301_2_REF, Q301_7_REF): "R27",
    }.items():
        query = by_targets[targets]
        contracts = [
            runtime.resolve_exact_risk_set_successor(
                query=query,
                release_ref=release_ref,
                source_universe_ref=UNIVERSE_REF,
                risk_set_ref=RISK_SET_REF,
                target_refs=targets,
            )
            for release_ref in RELEASE_REFS
        ]
        assert all(contract is not None for contract in contracts)
        assert contracts[0] is contracts[1]
        contract = contracts[0]
        member = min(memberships[root_id])
        nonmember = min(set(range(1, ROW_COUNT + 1)) - memberships[root_id])
        prefix = contract.respondent_key_prefix
        assert contract.is_member(
            respondent_key=f"{prefix}{member:012d}", target_refs=targets
        )
        assert not contract.is_member(
            respondent_key=f"{prefix}{nonmember:012d}", target_refs=targets
        )

    query = next(iter(by_targets.values()))
    assert runtime.resolve_exact_risk_set_successor(
        query=query,
        release_ref=exact_ref({
            **RELEASE_REF.as_dict(),
            "object_id": "urn:test:wrong-release",
        }),
        source_universe_ref=UNIVERSE_REF,
        risk_set_ref=RISK_SET_REF,
        target_refs=tuple(exact_ref(ref) for ref in query.target_refs),
    ) is None


def test_lits_d03_risk_set_successor_scope_is_exactly_base_and_adopted_r5b_release():
    record = risk_set_successor_authority_record()
    material = record["identity_material"]
    assert material["release_refs"] == [ref.as_dict() for ref in RELEASE_REFS]
    preservation = material["accepted_successor_preservation"]
    assert preservation["base_release_ref"] == RELEASE_REF.as_dict()
    assert preservation["successor_release_ref"] == SUCCESSOR_RELEASE_REF.as_dict()
    assert preservation["r5b_commit"] == "648a39ad5bed42f66e066410af5869604d29c12d"
    assert preservation["successor_replay_hash"] == (
        "30c168fbdf8425b23cbf2a2b2d2c9ab56f3438851f52e3562510089f1d381a08"
    )
    assert "ADDS_ONLY_F02_Q310_Q311" in preservation["preservation_law"]


def test_lits_d03_risk_set_record_rejects_unadopted_and_tampered_payload():
    record = risk_set_successor_authority_record()
    with pytest.raises(Pre553AuthorityError, match="not exactly adopted"):
        Pre553RuntimeAuthoritySet(exact_risk_set_successor_authorities=(record,))

    tampered = copy.deepcopy(record)
    tampered["payload_base64"] = "A" + tampered["payload_base64"][1:]
    with pytest.raises(Pre553AuthorityError, match="payload"):
        Pre553RuntimeAuthoritySet(
            adopted_authority_hashes=(D03_AUTHORITY_CONTENT_HASH,),
            exact_risk_set_successor_authorities=(tampered,),
        )


def _dialect_leaves(node):
    if node.get("op") == "LEAF" and node.get("operation") == "survey_response_EQ":
        yield node
    for child in node.get("children", ()):
        yield from _dialect_leaves(child)


def test_lits_f02_dialect_uses_typed_canonical_scalar_tokens_without_coercion():
    module = _runtime_module()
    _catalog, candidates, *_ = module.catalog_and_frontier()
    runtime = module.materialize_runtime_authority_set()
    predicates = {
        role.predicate.ref: role.predicate
        for candidate in candidates
        for role in candidate.query_roles
    }
    leaves = {
        (
            leaf["question_ref"]["content_hash"],
            leaf["source_native_value"],
        ): (predicate, leaf)
        for predicate in predicates.values()
        for leaf in _dialect_leaves(predicate.predicate_ast)
    }
    assert set(leaves) == {
        (question_hash, native_value)
        for question_hash in {
            "c4b0f76b7a37d8083a103ffd316f2eb009eeca7b5cbf5910e51d364b39641534",
            "8680064d936efb99d64457edc3a2385e8862a2aac6bf50efd423afe83e77aed9",
        }
        for native_value in (1, 2, 3)
    }

    validated_bindings = set()
    for predicate, leaf in leaves.values():
        contract = runtime.resolve_predicate_dialect(
            predicate.grammar_authority_ref, leaf
        )
        question_ref, response_ref, native_value, scope_ref = contract.validate_leaf(leaf)
        assert scope_ref == F02_FROZEN_SCOPE_REF
        validated_bindings.add(
            (question_ref.content_hash, response_ref.content_hash, native_value)
        )
    assert validated_bindings == {
        (
            binding["question_ref"]["content_hash"],
            binding["response_value_ref"]["content_hash"],
            binding["source_native_value"],
        )
        for binding in event_representation_successor_authority_record()[
            "identity_material"
        ]["bindings"]
    }

    predicate, integer_leaf = next(
        value for key, value in leaves.items() if key[1] == 1
    )
    string_leaf = dict(integer_leaf)
    string_leaf["source_native_value"] = "1"
    contract = runtime.resolve_predicate_dialect(
        predicate.grammar_authority_ref, string_leaf
    )
    with pytest.raises(
        Pre553AuthorityError,
        match="exact question/value binding mismatch",
    ):
        contract.validate_leaf(string_leaf)


def test_lits_f02_event_representation_authority_is_exact_six_binding_domain():
    record = event_representation_successor_authority_record()
    material = record["identity_material"]
    assert record["schema"] == F02_REPRESENTATION_SCHEMA
    assert record["authority_content_hash"] == F02_REPRESENTATION_AUTHORITY_CONTENT_HASH
    assert semantic_hash(material) == F02_REPRESENTATION_AUTHORITY_CONTENT_HASH
    assert material["source_sha256"] == F02_SOURCE_SHA256
    assert material["frozen_scope_ref"] == F02_FROZEN_SCOPE_REF.as_dict()
    assert material["runtime_release_ref"] == F02_SUCCESSOR_RELEASE_REF.as_dict()
    assert len(material["bindings"]) == 6
    assert {
        (
            binding["question_ref"]["content_hash"],
            binding["response_value_ref"]["content_hash"],
            binding["source_native_value"],
            binding["exact_event_raw_response_value"]["$exact_decimal"],
            binding["required_event_state"],
        )
        for binding in material["bindings"]
    } == {
        (
            F02_QUESTION_REFS[question].content_hash,
            F02_RESPONSE_HASHES[question][value],
            value,
            str(value),
            "SUBSTANTIVE_RESPONSE",
        )
        for question in ("q310", "q311")
        for value in (1, 2, 3)
    }
    assert {
        "NO_GENERIC_INT_FLOAT_DECIMAL_COERCION",
        "NO_STRING_NUMERIC_EQUIVALENCE",
        "NO_OTHER_SOURCE_RELEASE_SCOPE_QUESTION_VALUE_OR_STATE",
        "NO_C11_EVENT_OR_RELEASE_MUTATION",
        "NO_CANDIDATE_OUTPUT_PARENTAGE",
    } <= set(material["negative_limits"])


def test_lits_f02_event_representation_authority_rejects_unadopted_and_tampered():
    record = event_representation_successor_authority_record()
    with pytest.raises(Pre553AuthorityError, match="not exactly adopted"):
        Pre553RuntimeAuthoritySet(
            event_representation_successor_authorities=(record,)
        )

    tampered = copy.deepcopy(record)
    tampered["identity_material"]["bindings"][0][
        "exact_event_raw_response_value"
    ] = {"$exact_decimal": "1.0"}
    with pytest.raises(Pre553AuthorityError, match="identity_material hash mismatch"):
        Pre553RuntimeAuthoritySet(
            adopted_authority_hashes=(F02_REPRESENTATION_AUTHORITY_CONTENT_HASH,),
            event_representation_successor_authorities=(tampered,),
        )


def test_lits_f02_event_representation_matches_only_exact_adopted_successor_witness():
    module = _runtime_module()
    runtime = module.materialize_runtime_authority_set()
    binding = event_representation_successor_authority_record()["identity_material"][
        "bindings"
    ][0]
    question_ref = exact_ref(binding["question_ref"])
    response_ref = exact_ref(binding["response_value_ref"])
    native_value = binding["source_native_value"]
    exact_witness = binding["exact_event_raw_response_value"]

    assert runtime.match_exact_event_representation(
        frozen_scope_ref=F02_FROZEN_SCOPE_REF,
        runtime_release_ref=F02_SUCCESSOR_RELEASE_REF,
        question_ref=question_ref,
        response_value_ref=response_ref,
        source_native_value=native_value,
        event_raw_response_value=exact_witness,
    )

    with pytest.raises(
        Pre553AuthorityError,
        match="runtime event witness differs from exact adopted representation",
    ):
        runtime.match_exact_event_representation(
            frozen_scope_ref=F02_FROZEN_SCOPE_REF,
            runtime_release_ref=F02_SUCCESSOR_RELEASE_REF,
            question_ref=question_ref,
            response_value_ref=response_ref,
            source_native_value=native_value,
            event_raw_response_value={"$exact_decimal": "1.0"},
        )

    wrong_release = exact_ref({
        **F02_SUCCESSOR_RELEASE_REF.as_dict(),
        "object_id": "urn:test:wrong-release",
    })
    assert not runtime.match_exact_event_representation(
        frozen_scope_ref=F02_FROZEN_SCOPE_REF,
        runtime_release_ref=wrong_release,
        question_ref=question_ref,
        response_value_ref=response_ref,
        source_native_value=native_value,
        event_raw_response_value=exact_witness,
    )
    wrong_response = exact_ref({
        **response_ref.as_dict(),
        "object_id": "urn:test:wrong-response",
    })
    assert not runtime.match_exact_event_representation(
        frozen_scope_ref=F02_FROZEN_SCOPE_REF,
        runtime_release_ref=F02_SUCCESSOR_RELEASE_REF,
        question_ref=question_ref,
        response_value_ref=wrong_response,
        source_native_value=native_value,
        event_raw_response_value=exact_witness,
    )

    # The predecessor law remains exact canonical equality and gains no coercion.
    assert runtime.match_exact_event_representation(
        frozen_scope_ref=F02_FROZEN_SCOPE_REF,
        runtime_release_ref=wrong_release,
        question_ref=question_ref,
        response_value_ref=wrong_response,
        source_native_value=1,
        event_raw_response_value=1,
    )
    assert not runtime.match_exact_event_representation(
        frozen_scope_ref=F02_FROZEN_SCOPE_REF,
        runtime_release_ref=wrong_release,
        question_ref=question_ref,
        response_value_ref=wrong_response,
        source_native_value=1,
        event_raw_response_value="1",
    )
