from __future__ import annotations

import json
import warnings

from rawlsing_next import field_forge_conditional_support as ff
from rawlsing_next import gt12_c_to_d_relation_bridge as c_to_d
from rawlsing_next import gt12_d_to_m4_typed_bridge as d_to_m4
from rawlsing_next import wave1_ff_prev3_relation_admission as adm
from rawlsing_next.gt12_e2b_publication_governance_binding import (
    BUNDLE_CONTENT_HASH,
    load_current_gt12_e2b_publication_governance_binding,
)
from rawlsing_next.gt12_permission_translation_authority import (
    ADOPTED_V557_ALLOWED_USES,
    ADOPTED_V558_REQUESTED_USES,
)
from rawlsing_next.m1_temporal_v554_admission_dedup import M1DecisionState, semantic_hash
from rawlsing_next.m4_v557_v558_publication_repository import (
    AuthorityRef,
    ExactRef,
    V557DecisionState,
)
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_repo_native_seal import load_current_gt2_query_fact
from rawlsing_next.prev3_objective_world_release_root import (
    build_objective_world_release_root,
    replay_objective_world_release_root,
)

CURRENT_QUERY_HASH = "e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0"
CURRENT_FACT_HASH = "540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46"
CURRENT_REPLAY_HASH = "c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f"
CURRENT_PREDICATE_HASH = "bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3"
EXPECTED_PUBLICATION_GOVERNANCE_HASH = "f7d4d2313bcc70faf104cff205b0eb7aaa7d88556c895c8ea123a3725105cf14"
EXPECTED_PUBLICATION_HASH = "2c7fb3f81343179ad75c6441fadcd09201aa47b9dc0e032383071e83cc4e022a"
EXPECTED_REPOSITORY_HASH = "47594be9aaf284122f76e3f2e3d74af29054ae3e1d6228134e4eccfdacfa46d1"
EXPECTED_F1 = ExactRef(
    "F1",
    "urn:rawlsing:v554:f1:sha256:3530f08f43e704ad67e0fb74984b03b7ad0f068ea1de4bcf658f3b2d591bd56d",
    "a008553dc94af138de44e73ade8ddbcc1e2bb3a5c40cec575aad694aae104cbb",
)
SCOPE_REF = ExactRef(
    "PREV3_OBJECTIVE_WORLD_SCOPE",
    "PREV3SCOPE:f5ff97d598f6e3535643216e30427692f3d564fbe55e7de389c6ac2e0fdfb320",
    "f5ff97d598f6e3535643216e30427692f3d564fbe55e7de389c6ac2e0fdfb320",
)
VALID_TIME_AUTHORITY = AuthorityRef(
    "PREV3_OBJECTIVE_WORLD_VALID_TIME_AUTHORITY",
    "1.0.0",
    "4a912bd0bf1217b1095eaa5da4376bc1d55314fcfc80c62d2ef7fa085b5e3c02",
)
CURRENTNESS_REF = ExactRef(
    "PREV3_OBJECTIVE_WORLD_GRAIN_CURRENTNESS",
    "PREV3WCT:dd71fa2c3ff7781a196a98a63c4984602e213f31d3264bd6875e7f9923926bc9",
    "dd71fa2c3ff7781a196a98a63c4984602e213f31d3264bd6875e7f9923926bc9",
)
STATUS_BINDING_REF = ExactRef(
    "PREV3_NONTEMPORAL_RELEASE_STATUS_BINDING",
    "urn:rawlsing:prev3:nontemporal-release-status-binding:sha256:de1726bfb708840212e7b2968eef37ab68e3c897fedf9947fbf1cddf8c16d880",
    "de1726bfb708840212e7b2968eef37ab68e3c897fedf9947fbf1cddf8c16d880",
)
STATUS_AUTHORITY = AuthorityRef(
    "PREV3_NONTEMPORAL_STRUCTURAL_PRODUCT_RELEASE_STATUS_AUTHORITY",
    "1.0.0",
    "65c0cfcf8d33bcbf9bb88813eb43c6951377bd0ce5d268bd03f1c72799059509",
)
WORLD_TIME_PRODUCER = AuthorityRef(
    "PREV3_OBJECTIVE_WORLD_TIME_PRODUCER",
    "1.1.0",
    "e5c0ea62a7ff2ae006fa9722676245addbcba0d079f2e1d2079f3a9ffe247e10",
)


def _current_pre_v3_repository():
    query, fact = load_current_gt2_query_fact()
    assert query.content_hash == CURRENT_QUERY_HASH
    assert fact.content_hash == CURRENT_FACT_HASH
    assert exact_ref(fact.replay_ref, "fact.replay_ref").content_hash == CURRENT_REPLAY_HASH
    assert exact_ref(query.condition_predicate_ref, "query.condition_predicate_ref").content_hash == CURRENT_PREDICATE_HASH
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 19210

    targets = tuple(exact_ref(ref, "query.target_refs") for ref in query.target_refs)
    assert len(targets) == 2
    relation = ff.produce_exact_conditional_support_profile(
        joint_fact=fact,
        joint_query=query,
        conditioner_ref=targets[0],
        target_ref=targets[1],
        producer_permission_ceiling=(adm.GT2_TARGET_USE,),
        relation_permission_ceiling=(adm.GT2_TARGET_USE,),
    )
    assert relation.typed_state == "SUPPORTED"
    assert not relation.producer_state_blocking

    admitted = c_to_d.admit_gt12_c_relation(relation)
    assert admitted.admission.decision is adm.AdmissionDecision.ADMITTED

    binding = load_current_gt12_e2b_publication_governance_binding()
    assert binding.bundle_content_hash == EXPECTED_PUBLICATION_GOVERNANCE_HASH == BUNDLE_CONTENT_HASH
    _, evaluation = d_to_m4.evaluate_typed_d_to_e_at_v554(
        admitted.admission,
        governed_use_id=binding.governed_use_id,
        v554_rule_ref=binding.v554_rule_ref,
        publication_authority=binding.publication_authority,
    )
    assert evaluation.decision_state is M1DecisionState.ELIGIBLE
    assert tuple(item["family"] for item in evaluation.direct_v557_handoff["object_refs"]) == ("F1",)

    terminal = d_to_m4.publish_and_resolve_relation_v554_at_current_m4(
        admitted.admission,
        evaluation,
        v557_allowed_uses=ADOPTED_V557_ALLOWED_USES,
        requested_resolution_uses=ADOPTED_V558_REQUESTED_USES,
        v557_authority_ref=binding.v557_authority_ref,
        v557_decision_state=V557DecisionState.ALLOW_CONTEXT_ONLY,
    )
    assert terminal.repository.ref.content_hash == EXPECTED_REPOSITORY_HASH
    assert terminal.publication.ref.content_hash == EXPECTED_PUBLICATION_HASH
    assert terminal.repository.publication_bundle_ref == terminal.publication.ref
    assert len(terminal.repository.entries) == 1
    assert terminal.repository.entries[0].obj.ref == EXPECTED_F1
    assert terminal.resolution.receipt.result_state == "RESOLUTION_COMPLETE"
    return binding, terminal.repository


def _world_validity_material(repository, release_authority: AuthorityRef):
    if repository.ref.content_hash != EXPECTED_REPOSITORY_HASH:
        raise AssertionError("K01 release identity / reconstructed V558 repository mismatch")
    if repository.publication_bundle_ref.content_hash != EXPECTED_PUBLICATION_HASH:
        raise AssertionError("K01 release identity / reconstructed V557 publication mismatch")
    if len(repository.entries) != 1 or repository.entries[0].obj.ref != EXPECTED_F1:
        raise AssertionError("K01 1/1 world constituent denominator mismatch")
    return {
        "schema": "PREV3_OBJECTIVE_WORLD_VALIDITY_R1",
        "objective_world_scope_ref": SCOPE_REF.as_dict(),
        "valid_time_authority_ref": VALID_TIME_AUTHORITY.as_dict(),
        "release_authority_ref": release_authority.as_dict(),
        "world_currentness_receipt_ref": CURRENTNESS_REF.as_dict(),
        "world_time_producer_authority_ref": WORLD_TIME_PRODUCER.as_dict(),
        "immutable_release_identity": {
            "publication_governance_bundle_hash": EXPECTED_PUBLICATION_GOVERNANCE_HASH,
            "v557_publication_bundle_hash": EXPECTED_PUBLICATION_HASH,
            "v558_repository_hash": EXPECTED_REPOSITORY_HASH,
        },
        "constituent_status_bindings": [
            {
                "constituent_object_ref": EXPECTED_F1.as_dict(),
                "status_domain": "RELEASE_STATUS_ONLY__NOT_PRODUCT_TIME",
                "status_class": "NONTEMPORAL_PRODUCT__PROJECT_CURRENT_RELEASE_MEMBERSHIP",
                "binding_ref": STATUS_BINDING_REF.as_dict(),
                "competent_status_authority_ref": STATUS_AUTHORITY.as_dict(),
                "effective_time_or_historical_time_ref": None,
            }
        ],
        "bounded_completeness_declaration": {
            "scope": "EXACT_E01_BOUNDED_RELEASE_ONLY",
            "constituent_denominator": 1,
            "lawfully_bound": 1,
            "blocked": 0,
            "duplicate_bindings": 0,
            "extra_bindings": 0,
            "complete": True,
        },
        "assertion_ceiling": "PROJECT_CURRENT_BOUNDED_OBJECTIVE_WORLD_RELEASE_CURRENTNESS_ONLY__NO_PRODUCT_TIME_OR_PRESENT_DAY_PERSISTENCE",
    }


def test_l01_first_real_objective_world_validity_and_root_replay():
    binding, repository = _current_pre_v3_repository()
    publication_authority = binding.publication_authority
    release_authority = AuthorityRef(
        publication_authority["authority_id"],
        publication_authority["authority_version"],
        publication_authority["authority_hash"],
    )

    validity_material = _world_validity_material(repository, release_authority)
    first_validity_hash = semantic_hash(validity_material)
    second_validity_hash = semantic_hash(_world_validity_material(repository, release_authority))
    assert first_validity_hash == second_validity_hash
    validity_ref = ExactRef(
        "PREV3_OBJECTIVE_WORLD_VALIDITY",
        f"PREV3WVALID:{first_validity_hash}",
        first_validity_hash,
    )

    root = build_objective_world_release_root(
        release_authority_ref=release_authority,
        repository=repository,
        publication_bundle_ref=repository.publication_bundle_ref,
        index_manifest_ref=repository.index_manifest.ref,
        objective_world_scope_ref=SCOPE_REF,
        valid_time_authority_ref=VALID_TIME_AUTHORITY,
        world_validity_ref=validity_ref,
        predecessor_world_root_ref=None,
    )
    replayed = replay_objective_world_release_root(root, repository=repository)
    second = build_objective_world_release_root(
        release_authority_ref=release_authority,
        repository=repository,
        publication_bundle_ref=repository.publication_bundle_ref,
        index_manifest_ref=repository.index_manifest.ref,
        objective_world_scope_ref=SCOPE_REF,
        valid_time_authority_ref=VALID_TIME_AUTHORITY,
        world_validity_ref=validity_ref,
        predecessor_world_root_ref=None,
    )
    assert root.ref == replayed.ref == second.ref
    assert root.repository_ref == repository.ref
    assert root.publication_bundle_ref == repository.publication_bundle_ref
    assert root.index_manifest_ref == repository.index_manifest.ref
    assert root.objective_world_scope_ref == SCOPE_REF
    assert root.world_validity_ref == validity_ref
    assert root.predecessor_world_root_ref is None

    evidence = {
        "schema": "L01_FIRST_REAL_OBJECTIVE_WORLD_VALIDITY_AND_ROOT_EXECUTION_R1",
        "world_validity_material": validity_material,
        "world_validity_ref": validity_ref.as_dict(),
        "world_validity_replay": {
            "first": first_validity_hash,
            "second": second_validity_hash,
            "parity": "PASS",
        },
        "world_root_material": root.canonical_material(),
        "world_root_ref": root.ref.as_dict(),
        "world_root_replay_ref": replayed.ref.as_dict(),
        "repository_ref": repository.ref.as_dict(),
        "publication_bundle_ref": repository.publication_bundle_ref.as_dict(),
        "index_manifest_ref": repository.index_manifest.ref.as_dict(),
        "constituent_denominator": 1,
        "constituent_ref": EXPECTED_F1.as_dict(),
        "assertion_ceiling": validity_material["assertion_ceiling"],
    }
    warnings.warn(
        "L01_FIRST_REAL_OBJECTIVE_WORLD_EVIDENCE="
        + json.dumps(evidence, sort_keys=True, separators=(",", ":")),
        RuntimeWarning,
    )


def test_l01_validity_fails_closed_on_world_denominator_or_release_mismatch():
    binding, repository = _current_pre_v3_repository()
    publication_authority = binding.publication_authority
    release_authority = AuthorityRef(
        publication_authority["authority_id"],
        publication_authority["authority_version"],
        publication_authority["authority_hash"],
    )
    assert _world_validity_material(repository, release_authority)["bounded_completeness_declaration"]["complete"] is True
