from dataclasses import replace

import pytest

from rawlsing_next.pre553_candidate_c_production_binding import (
    CACC1_ID,
    CACC2_ID,
    CANDIDATE_C_HASH,
    CANDIDATE_C_OWNER_BLOB,
    CANDIDATE_C_OWNER_COMMIT,
    CANDIDATE_C_OWNER_PATH,
    LITS_I_CURRENT_SPEC,
    WVS7_CURRENT_SPEC,
    CandidateCProductionBindingError,
    CandidateCSourceBindingSpec,
    bind_candidate_c_repository,
    candidate_c_builder_identity,
    candidate_c_repository_builder_for_source,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_source_backed_c11_facade import (
    CONTRACT_ID as SOURCE_BACKED_C11_CONTRACT_ID,
    build_source_backed_c11_repository,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate,
    _h,
    _query,
    _query_authority,
)
from rawlsing_next.tests.test_pre553_source_backed_c11_facade import (
    _fixture,
    _source_dict,
)


def _fallback_spec(fx, *, source_name="TEST_LITS", permitted=(CACC1_ID, CACC2_ID)):
    return CandidateCSourceBindingSpec(
        source_name=source_name,
        source_sha256=fx["source_sha"],
        projection_cache_identity=fx["projection"].cache_identity,
        permitted_accelerators=permitted,
        applicable_accelerators=(),
        realization_strategy="EXACT_SOURCE_BACKED_TEST_FALLBACK",
        scope_reason="test exact projection deliberately uses the source-backed fallback contract",
    )


def _i03(fx, binding, tag="frozen"):
    source = _source_dict(fx, binding.repository, binding.release)
    qauth = _query_authority(f"candidate-c-{tag}")
    predicate = _branch_predicate(source, qauth, tag=f"candidate-c-{tag}")
    query = _query(source, qauth, predicate, ("Y",), tag=f"candidate-c-{tag}")
    registry = AuthorityRegistry((*fx["authorities"], qauth))
    return execute_empirical_query(
        repository=binding.repository,
        query=query,
        predicate=predicate,
        authority_registry=registry,
        release_refs=(binding.release.release_ref,),
    )


def test_current_candidate_c_specs_freeze_exact_source_projection_and_accelerator_law():
    assert LITS_I_CURRENT_SPEC.source_name == "LITS_I"
    assert LITS_I_CURRENT_SPEC.source_sha256 == "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
    assert LITS_I_CURRENT_SPEC.projection_cache_identity == "84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872"
    assert LITS_I_CURRENT_SPEC.permitted_accelerators == (CACC1_ID, CACC2_ID)
    assert LITS_I_CURRENT_SPEC.applicable_accelerators == ()
    assert "q310/q311" in LITS_I_CURRENT_SPEC.scope_reason

    assert WVS7_CURRENT_SPEC.source_name == "WVS7"
    assert WVS7_CURRENT_SPEC.source_sha256 == "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
    assert WVS7_CURRENT_SPEC.projection_cache_identity == "f400c804fea9b526f25eac823138ecb30e10efaad3207c4578661f684adee665"
    assert WVS7_CURRENT_SPEC.permitted_accelerators == ()
    assert WVS7_CURRENT_SPEC.applicable_accelerators == ()


def test_lits_accelerator_deletion_or_nonavailability_preserves_c11_replay_and_i03_identity():
    fx = _fixture("candidate-c-delete")
    spec = _fallback_spec(fx)

    with_accelerators = bind_candidate_c_repository(
        spec=spec,
        source=fx["incidence"],
        projection=fx["projection"],
        accelerator_inventory=(CACC1_ID, CACC2_ID),
    )
    after_delete = bind_candidate_c_repository(
        spec=spec,
        source=fx["incidence"],
        projection=fx["projection"],
        accelerator_inventory=(),
    )
    direct_repo, direct_release = build_source_backed_c11_repository(
        fx["incidence"], fx["projection"], cache=None
    )

    assert with_accelerators.release.release_ref == after_delete.release.release_ref == direct_release.release_ref
    assert with_accelerators.release.replay_manifest.ref == after_delete.release.replay_manifest.ref == direct_release.replay_manifest.ref
    assert with_accelerators.c11_semantic_result_identity == after_delete.c11_semantic_result_identity
    assert tuple(x.ref for x in with_accelerators.release.public_objects) == tuple(
        x.ref for x in after_delete.release.public_objects
    )
    assert direct_repo.resolve_release_exact(direct_release.release_ref).release_ref == direct_release.release_ref

    left = _i03(fx, with_accelerators)
    right = _i03(fx, after_delete)
    assert tuple(f.ref for f in left.facts) == tuple(f.ref for f in right.facts)
    assert left.facts == right.facts


def test_source_backed_fallback_remains_candidate_c_and_does_not_move_semantic_ownership():
    fx = _fixture("candidate-c-identity")
    binding = bind_candidate_c_repository(
        spec=_fallback_spec(fx),
        source=fx["incidence"],
        projection=fx["projection"],
        accelerator_inventory=(),
    )
    receipt = binding.receipt()

    assert binding.candidate_identity == "C"
    assert receipt["candidate_identity"] == "C"
    assert receipt["candidate_policy"] == "SOURCE_BACKED_HYBRID_WITH_REGENERABLE_ACCELERATORS"
    assert receipt["candidate_owner"] == {
        "commit": CANDIDATE_C_OWNER_COMMIT,
        "path": CANDIDATE_C_OWNER_PATH,
        "blob": CANDIDATE_C_OWNER_BLOB,
        "candidate_hash": CANDIDATE_C_HASH,
    }
    assert receipt["semantic_owner_contract"] == SOURCE_BACKED_C11_CONTRACT_ID
    assert receipt["semantic_owner_moved"] is False
    assert receipt["candidate_b_identity_substituted"] is False
    assert receipt["accelerator_authoritative"] is False
    assert receipt["applied_accelerators"] == []
    builder_identity = candidate_c_builder_identity("LITS_I")
    assert builder_identity["candidate"] == "C"
    assert builder_identity["owner_blob"] == CANDIDATE_C_OWNER_BLOB
    assert builder_identity["candidate_b_identity_substituted"] is False
    assert candidate_c_repository_builder_for_source("LITS_I").__name__ == "build_lits_candidate_c_repository"
    assert candidate_c_repository_builder_for_source("WVS7").__name__ == "build_wvs7_candidate_c_repository"


def test_physical_inventory_changes_binding_cost_provenance_not_semantic_or_candidate_identity():
    fx = _fixture("candidate-c-physical-state")
    spec = _fallback_spec(fx)
    present = bind_candidate_c_repository(
        spec=spec,
        source=fx["incidence"],
        projection=fx["projection"],
        accelerator_inventory=(CACC1_ID,),
    )
    absent = bind_candidate_c_repository(
        spec=spec,
        source=fx["incidence"],
        projection=fx["projection"],
        accelerator_inventory=(),
    )
    present_receipt = present.receipt()
    absent_receipt = absent.receipt()

    assert present_receipt["binding_identity"] != absent_receipt["binding_identity"]
    assert present_receipt["candidate_identity"] == absent_receipt["candidate_identity"] == "C"
    assert present_receipt["c11_semantic_result_identity"] == absent_receipt["c11_semantic_result_identity"]
    assert present_receipt["semantic_release_ref"] == absent_receipt["semantic_release_ref"]
    assert present_receipt["semantic_replay_ref"] == absent_receipt["semantic_replay_ref"]


def test_wvs_zero_accelerator_scope_rejects_lits_accelerator_creep():
    fx = _fixture("candidate-c-wvs-zero")
    spec = _fallback_spec(fx, source_name="TEST_WVS", permitted=())
    binding = bind_candidate_c_repository(
        spec=spec,
        source=fx["incidence"],
        projection=fx["projection"],
        accelerator_inventory=(),
    )
    assert binding.receipt()["observed_accelerators"] == []
    assert binding.receipt()["candidate_identity"] == "C"

    with pytest.raises(CandidateCProductionBindingError, match="exceeds accepted source scope"):
        bind_candidate_c_repository(
            spec=spec,
            source=fx["incidence"],
            projection=fx["projection"],
            accelerator_inventory=(CACC1_ID,),
        )


def test_cacc3_unknown_accelerator_and_partial_scope_claim_fail_closed():
    fx = _fixture("candidate-c-hostile-accel")
    spec = _fallback_spec(fx)
    with pytest.raises(CandidateCProductionBindingError, match="unaccepted Candidate-C accelerator"):
        bind_candidate_c_repository(
            spec=spec,
            source=fx["incidence"],
            projection=fx["projection"],
            accelerator_inventory=("CACC3_FORBIDDEN",),
        )

    false_full_coverage = replace(spec, applicable_accelerators=(CACC1_ID,))
    with pytest.raises(CandidateCProductionBindingError, match="may not claim an accelerator"):
        bind_candidate_c_repository(
            spec=false_full_coverage,
            source=fx["incidence"],
            projection=fx["projection"],
            accelerator_inventory=(CACC1_ID,),
        )


def test_source_and_projection_scope_mismatch_fail_closed_without_inference():
    fx = _fixture("candidate-c-mismatch")
    spec = _fallback_spec(fx)

    wrong_source = replace(spec, source_sha256=_h("wrong-candidate-c-source"))
    with pytest.raises(CandidateCProductionBindingError, match="exact source identity mismatch"):
        bind_candidate_c_repository(
            spec=wrong_source,
            source=fx["incidence"],
            projection=fx["projection"],
        )

    wrong_projection = replace(spec, projection_cache_identity=_h("wrong-candidate-c-projection"))
    with pytest.raises(CandidateCProductionBindingError, match="exact projection identity mismatch"):
        bind_candidate_c_repository(
            spec=wrong_projection,
            source=fx["incidence"],
            projection=fx["projection"],
        )
