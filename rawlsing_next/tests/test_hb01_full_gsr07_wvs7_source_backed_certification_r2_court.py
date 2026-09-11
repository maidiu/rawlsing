from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_source_backed_c11_facade import (
    build_source_backed_c11_repository,
    execute_source_backed_empirical_query,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate,
    _query,
    _query_authority,
)
from rawlsing_next.tests.test_hb01_full_gsr07_wvs7_source_backed_certification_r2 import (
    ACCEPTED_WVS7_DUAL_ROLE_42,
    _fixture,
    test_exact_42_dual_owner_slots_release_deterministically_without_weight_promotion as _release_and_replay_court,
    test_frozen_real_source_certification_constants_are_exact_and_noncollapsed as _source_identity_court,
    test_owner_family_authority_closure_is_exact_and_reciprocal_substitution_fails_closed as _owner_closure_court,
)


def test_source_identity_and_certification_constants():
    _source_identity_court()


def test_release_replay_routing_and_no_weight_promotion():
    _release_and_replay_court()


def test_exact_owner_family_authority_closure():
    _owner_closure_court()


def test_frozen_i03_wrapper_direct_parity_on_sealed_source_backed_release():
    fx = _fixture()
    repo, release = build_source_backed_c11_repository(fx["stream"], fx["projection"])
    qa = _query_authority("hb01-r2-frozen-i03")
    source_auth = fx["authorities"][0]
    source = {
        "repo": repo,
        "release_ref": release.release_ref,
        "universe": fx["universe"],
        "respondents": {"SOURCE_ROW_1": fx["respondent"]},
        "qrefs": fx["qrefs"],
        "risk_refs": {"R": fx["risk_ref"]},
        "authorities": fx["authorities"],
        "source_auth": source_auth,
    }
    predicate = _branch_predicate(source, qa, tag="hb01-r2")
    query = _query(source, qa, predicate, (ACCEPTED_WVS7_DUAL_ROLE_42[0],), tag="hb01-r2")
    registry = AuthorityRegistry((*fx["authorities"], qa))
    direct = execute_empirical_query(
        repository=repo,
        query=query,
        predicate=predicate,
        authority_registry=registry,
        release_refs=(release.release_ref,),
    )
    wrapped = execute_source_backed_empirical_query(
        source=fx["stream"],
        projection=fx["projection"],
        query=query,
        predicate=predicate,
        authority_registry=registry,
    )
    assert direct.query_ref == wrapped.query_ref
    assert direct.release_refs == wrapped.release_refs == (release.release_ref,)
    assert tuple(f.ref for f in direct.facts) == tuple(f.ref for f in wrapped.facts)
    assert tuple(f.semantic_projection() for f in direct.facts) == tuple(f.semantic_projection() for f in wrapped.facts)
    assert all(f.typed_state != "SUPPORTED" for f in direct.facts)
