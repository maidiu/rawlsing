from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import types

import pytest

import rawlsing_next.ee_p2x_darwin_stage_backend as backend
import rawlsing_next.fiabc_final_oracle_freeze_producers as producer
from rawlsing_next.pre553_carrier_execution import materialize_public_object
from rawlsing_next.fiabc_final_oracle_freeze_producers import FinalOracleProducerError
from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import authority_ref, canonicalize
from rawlsing_next.pre553_runtime_context import bind_runtime


ROOT = Path(__file__).resolve().parents[2]
RETURN = ROOT / "WORKER_RETURNS/PREMAIN-FIABC-LITS-EXECUTED-ROLE-CLOSURE-REPAIR-AND-SOURCE-RETRY-R1"
PRECHECK = RETURN / "court/oracle_producers/LITS_I/current_i05_precheck.json"
PRECHECK_SHA256 = "1ffbcb0f02e0c6b89a09cb255ce9342cbcb162ab2a1302de0ca8ade24990eed6"
MIXED_REF = {
    "authority_id": "urn:rawlsing:prev3:p2r4a:pre553:mixed-predicate-grammar",
    "authority_version": "1.0.0-candidate",
    "authority_content_hash": "0d7cfaac1d63cd438d29b109b590cb828805bd113fc37759a6f6f4c88d3c8f55",
}
MIXED_PREDICATE_HASH = "3dba42ac25eb61d46958587c46ecacbb4fff83f87de535a72d0d793e5c49b508"
MIXED_QUERY_HASH = "3419fd8377bd3b681315191bd22a3c37a95443946c0a0477b2c591e6690bfbd0"


@pytest.fixture(scope="module")
def source_free_materialization(tmp_path_factory):
    work_root = tmp_path_factory.mktemp("fiabc-r4a-source-free")
    ctx = types.SimpleNamespace(work_root=work_root)
    services = types.SimpleNamespace(repo_root=ROOT)
    projection, _projection_context, _banked = backend._lits_projection(
        ctx, services, {}, None
    )
    runtime = backend._lits_runtime(ctx, services, projection)
    support = backend._support_module(ctx, services)
    catalog, candidates, _primitives, _queries, _definition = support.catalog_and_frontier()
    roles = [role for candidate in candidates for role in candidate.query_roles]
    return support, runtime, catalog, candidates, roles


def _precheck():
    raw = PRECHECK.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PRECHECK_SHA256
    return json.loads(raw)


def test_exact_hq_adopted_snapshot_resolves_without_mutating_candidate_fixture(source_free_materialization):
    support, runtime, _catalog, _candidates, _roles = source_free_materialization
    fixture = json.loads(
        (ROOT / "rawlsing_next/tests/fixtures/ee_p2r6a_r4a_03_mixed.json").read_text()
    )
    successor = json.loads(
        (ROOT / "rawlsing_next/tests/fixtures/ee_p2r6a_r4a_05_successor.json").read_text()
    )
    assert fixture["status"] == "CANDIDATE__HQ_ADOPTION_REQUIRED"
    snapshot = runtime["runtime_authority_set"].resolve_exact_runtime_authority(MIXED_REF)
    assert snapshot is not None
    assert snapshot.authority_ref.as_dict() == MIXED_REF
    assert snapshot.typed_state == snapshot.decision_state == "ALLOW"
    assert snapshot.authority_kind == "PREDICATE_GRAMMAR"
    assert tuple(snapshot.governed_operations) == ("AND",)
    assert tuple(snapshot.governed_object_families) == ("EmpiricalPredicate@1.0.0",)
    identity = fixture["identity_material"]
    assert snapshot.interpretation_semantics_fingerprint == MIXED_REF["authority_content_hash"]
    assert canonicalize(snapshot.scope_envelope["exact_workload_scope"]) == canonicalize(
        identity["exact_workload_scope"]
    )
    assert canonicalize(snapshot.scope_envelope["allowed_input_grammar_refs"]) == canonicalize(
        identity["allowed_input_grammar_refs"]
    )
    assert canonicalize(snapshot.scope_envelope["permitted_mixed_composition"]) == canonicalize(
        identity["permitted_mixed_composition"]
    )
    assert canonicalize(snapshot.scope_envelope["leaf_operation_families"]) == canonicalize(
        identity["leaf_operation_families"]
    )
    assert canonicalize(snapshot.scope_envelope["respondent_binding_compatibility_ref"]) == canonicalize(
        identity["respondent_binding_compatibility_ref"]
    )
    assert canonicalize(snapshot.scope_envelope["identity_preservation"]) == canonicalize(
        identity["identity_preservation"]
    )
    assert canonicalize(snapshot.scope_envelope["negative_cases"]) == canonicalize(
        identity["negative_cases"]
    )
    assert snapshot.scope_envelope["no_adjacent_family_inference"] is True
    assert snapshot.scope_envelope["fail_closed"] is True
    assert canonicalize(snapshot.parent_authority_refs) == canonicalize(
        identity["parent_authority_refs"]
    )
    assert snapshot.negative_limit_refs == ()  # All adopted negative limits are explicit in scope.
    assert len(snapshot.dependency_refs) == 1
    assert snapshot.dependency_refs[0].as_dict() == {
        "kind": "HQ_ADOPTION_DECISION",
        "object_id": "urn:rawlsing:hq:decision:HQD-2026-09-18-044",
        "content_hash": "38ccf7e51fde4366f86c9d181b18da6efd59751be8f4b84f16685953cd79d891",
    }
    assert canonicalize(snapshot.replay_protocol_ref) == canonicalize(snapshot.dependency_refs[0])
    assert snapshot.content_hash == "c22cccad0add0048047f4edc3852ebce5d7f87ca0e7b81acb18587abb98ece4e"
    assert support.R4A_ADOPTION_DECISION_ID == "HQD-2026-09-18-044"
    assert successor["identity_material"]["mixed_grammar_authority_ref"] == MIXED_REF


def test_77_role_refs_and_60_fact_chains_resolve_and_query_predicate_preimages_round_trip(source_free_materialization):
    _support, runtime, catalog, candidates, roles = source_free_materialization
    precheck = _precheck()
    assert len(candidates) == precheck["candidate_count"] == 50
    assert len(roles) == precheck["query_role_count"] == 77
    query_by_hash = {role.query.content_hash: role.query for role in roles}
    predicate_by_hash = {role.predicate.content_hash: role.predicate for role in roles}
    assert len(query_by_hash) == 60
    assert len(predicate_by_hash) == 27

    by_rule = {
        row["candidate_hash"]: row["rule_id"] for row in precheck["by_rule"]
    }
    assert {candidate.candidate_hash for candidate in candidates} == set(by_rule)
    for candidate in candidates:
        assert by_rule[candidate.candidate_hash] == candidate.rule_id

    for role in roles:
        assert role.query.condition_predicate_ref["content_hash"] == role.predicate.content_hash
    for public_object in (*query_by_hash.values(), *predicate_by_hash.values()):
        round_tripped = materialize_public_object(public_object.as_dict())
        assert canonicalize(round_tripped.as_dict()) == canonicalize(public_object.as_dict())

    with bind_runtime(
        runtime["runtime_authority_set"],
        runtime_catalog_identity=backend.R6O_RUNTIME_CATALOG,
    ):
        for public_object in (*query_by_hash.values(), *predicate_by_hash.values()):
            for ref in public_object.authority_snapshot_refs:
                assert catalog.authority_registry.resolve_exact(ref).ref == ref

    facts = precheck["empirical_facts"]
    assert len(facts) == 60
    for fact in facts:
        query_hash = fact["empirical_query_spec_ref"]["content_hash"]
        predicate_hash = fact["condition_predicate_ref"]["content_hash"]
        assert query_hash in query_by_hash
        assert predicate_hash in predicate_by_hash
        assert query_by_hash[query_hash].condition_predicate_ref["content_hash"] == predicate_hash

    mixed = [role for role in roles if role.predicate.content_hash == MIXED_PREDICATE_HASH]
    assert len(mixed) == 1
    assert mixed[0].query.content_hash == MIXED_QUERY_HASH
    assert any(ref.as_dict() == MIXED_REF for ref in mixed[0].predicate.authority_snapshot_refs)
    assert mixed[0].query.condition_predicate_ref["content_hash"] == MIXED_PREDICATE_HASH
    for fact in facts:
        fact_ref = fact["fact_ref"]
        assert fact_ref["object_id"].endswith(f"sha256:{fact_ref['content_hash']}")
    assert precheck["current_execution_identity"] == "e547bfc6b27e89fc3a205d808cc7d5ff295e54ef7f34bf0c825c4bc3be3b85c5"
    assert precheck["current_semantic_replay_identity"] == "dbd18f3c3393256b2062061f2096adcbf4c44605ad5b592b75d59824c0428640"
    assert precheck["candidate_processes_started"] == 0
    assert "StructuralEmpiricalAdmission@1.0.0" not in {
        f"{obj.schema_id}@{obj.schema_version}"
        for obj in (*query_by_hash.values(), *predicate_by_hash.values())
    }


def test_missing_substituted_and_mutated_authority_remain_fail_closed(source_free_materialization):
    support, runtime, catalog, _candidates, _roles = source_free_materialization
    authority_set = runtime["runtime_authority_set"]
    ref = authority_ref(MIXED_REF)
    snapshot = authority_set.resolve_exact_runtime_authority(ref)
    assert snapshot is not None

    without = copy.copy(authority_set)
    historical = dict(authority_set._historical_authority_snapshots)
    historical.pop(ref.key)
    without._historical_authority_snapshots = type(authority_set._historical_authority_snapshots)(historical)
    with bind_runtime(without, runtime_catalog_identity=backend.R6O_RUNTIME_CATALOG):
        with pytest.raises(Pre553AuthorityError, match="exact historical authority unavailable"):
            catalog.authority_registry.resolve_exact(ref)

    wrong_version = snapshot.as_dict()
    wrong_version["semantic_fields"]["authority_version"] = "1.0.0"
    # Keep the canonical serialized shape, but ask the constructor to recompute
    # the identity for this substituted authority version.
    wrong_version["object_id"] = None
    wrong_version["content_hash"] = None
    substitute = materialize_public_object(wrong_version)
    from rawlsing_next.pre553_empirical_authority import AuthorityRegistry

    with pytest.raises(Pre553AuthorityError, match="exact historical authority unavailable"):
        AuthorityRegistry([substitute]).resolve_exact(ref)
    assert authority_set.resolve_exact_runtime_authority(
        {**MIXED_REF, "authority_content_hash": "f" * 64}
    ) is None
    assert authority_set.resolve_exact_runtime_authority(
        {**MIXED_REF, "authority_version": "LATEST"}
    ) is None

    fixture = json.loads(
        (ROOT / "rawlsing_next/tests/fixtures/ee_p2r6a_r4a_03_mixed.json").read_text()
    )
    successor = json.loads(
        (ROOT / "rawlsing_next/tests/fixtures/ee_p2r6a_r4a_05_successor.json").read_text()
    )
    mutated = copy.deepcopy(fixture)
    mutated["identity_material"]["permitted_mixed_composition"]["maximum_arity"] = 4
    with pytest.raises(Pre553AuthorityError, match="preimage/hash mismatch"):
        support._r4a_mixed_grammar_adoption_snapshot(mutated, successor)
    with pytest.raises(Pre553AuthorityError, match="adoption decision must resolve once"):
        support._r4a_mixed_grammar_adoption_snapshot(fixture, successor, decision_records=[])


def test_canonical_closure_retains_exact_hq_adopted_snapshot_preimage(source_free_materialization):
    _support, runtime, catalog, _candidates, roles = source_free_materialization
    role = next(role for role in roles if role.predicate.content_hash == MIXED_PREDICATE_HASH)
    authority_set = runtime["runtime_authority_set"]
    public_objects = [role.predicate, role.query]
    exact_ref = authority_ref(MIXED_REF)
    catalog_snapshots = [
        obj for obj in catalog.authorities
        if getattr(obj, "schema_id", None) == "AuthoritySnapshot"
    ]
    catalog_snapshot_keys = {obj.authority_ref.key for obj in catalog_snapshots}
    assert exact_ref.key not in catalog_snapshot_keys
    for obj in public_objects:
        for ref in obj.authority_snapshot_refs:
            assert ref == exact_ref or ref.key in catalog_snapshot_keys
    # Simulate the exact pre-repair state: every authority snapshot already in
    # the runtime catalog is retained, while the HQ-adopted mixed ref is absent.
    objects_with_prior_closure = [*public_objects, *catalog_snapshots]

    retained = producer._retain_exact_runtime_authority_snapshots(
        objects_with_prior_closure, authority_set
    )
    retained_target = [
        obj for obj in retained
        if getattr(obj, "schema_id", None) == "AuthoritySnapshot"
        and obj.authority_ref == exact_ref
    ]
    assert len(retained_target) == 1
    assert retained[0].as_dict() == role.predicate.as_dict()
    assert retained[1].as_dict() == role.query.as_dict()
    assert canonicalize(
        materialize_public_object(retained_target[0].as_dict()).as_dict()
    ) == canonicalize(retained_target[0].as_dict())

    without = copy.copy(authority_set)
    historical = dict(authority_set._historical_authority_snapshots)
    historical.pop(exact_ref.key)
    without._historical_authority_snapshots = type(
        authority_set._historical_authority_snapshots
    )(historical)
    with pytest.raises(FinalOracleProducerError, match="cannot resolve exact adopted authority snapshot preimage"):
        producer._retain_exact_runtime_authority_snapshots(
            objects_with_prior_closure, without
        )


def test_wvs7_frozen_identities_are_unchanged_and_no_structural_path_is_present():
    overlay = json.loads(
        (ROOT / "rawlsing_next/runtime/ee_p2x/03_LITS_RUNTIME_AUTHORITY_OVERLAY_BINDING.json").read_text()
    )
    assert overlay["wvs7_preservation"]["oracle_identity"] == "3694b8bd0b5468433a1a83bd469337c7e36e552c3a9a5fef65fff88df8fce800"
    assert overlay["wvs7_preservation"]["truth_payload_identity"] == "eb2f9224219385dbf21af70d317e0978383012ff057ce2ac857b59c130472405"
    assert overlay["scope"]["measured_p2x_authorized"] is False
    assert overlay["checkpoint_law"]["canonical_current_empirical_closure_required"] is True
