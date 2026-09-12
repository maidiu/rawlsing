from dataclasses import replace
import inspect

import pytest

from rawlsing_next.m1_temporal_v554_admission_dedup import semantic_hash
from rawlsing_next.m4_v557_v558_publication_repository import (
    AuthorityRef,
    ExactRef,
    RepositoryEntry,
    V557DecisionState,
    V557PublicationEntry,
    build_v557_publication_bundle,
    build_v558_repository_bundle,
    govern_v557,
    make_producer_locator,
    make_structural_object,
)
from rawlsing_next.prev3_objective_world_release_root import (
    OBJECTIVE_WORLD_SCOPE_REF_KIND,
    OBJECTIVE_WORLD_VALIDITY_REF_KIND,
    WORLD_ROOT_REF_KIND,
    ObjectiveWorldRootError,
    build_objective_world_release_root,
    replay_objective_world_release_root,
)


def _h(label: str) -> str:
    return semantic_hash({"w2-d01": label})


def _authority(label: str) -> AuthorityRef:
    return AuthorityRef(f"W2-D01-{label}", "1.0.0", _h(f"authority:{label}"))


def _ref(kind: str, label: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:w2-d01:{label}", _h(f"{kind}:{label}"))


def _repo():
    obj = make_structural_object(
        producer_family="V554",
        semantic_class="F1",
        object_id="urn:test:w2-d01:v554:f1",
        schema_id="TEST_W2_D01_V554",
        schema_version="1.0.0",
        typed_state="SUPPORTED",
        producer_allowed_uses=("REVIEW",),
        payload={"scope": "objective", "state": "SUPPORTED", "tag": "real-surface-shape"},
        source_stage="TEST-W2-D01",
    )
    governance = govern_v557(
        obj,
        decision_state=V557DecisionState.ALLOW_REVIEW_ONLY,
        v557_allowed_uses=("REVIEW",),
        authority_ref=_authority("V557"),
    )
    locator = make_producer_locator(
        obj,
        governance,
        logical_collection_kind="W2_D01_OBJECTIVE_TEST",
        authoritative_build_id="W2-D01-BUILD-1",
        authoritative_build_hash=_h("build"),
        producer_contract_id="W2_D01_TEST_PRODUCER",
        producer_contract_version="1.0.0",
        producer_contract_hash=_h("producer-contract"),
        producer_rule_bindings=(_authority("RULE"),),
    )
    entry = RepositoryEntry(obj, governance, locator)
    publication = build_v557_publication_bundle((V557PublicationEntry(obj, governance),))
    repository = build_v558_repository_bundle(publication, (entry,))
    return publication, repository


def _root(repository, *, validity_label="validity-r1", predecessor=None):
    return build_objective_world_release_root(
        release_authority_ref=_authority("RELEASE"),
        repository=repository,
        publication_bundle_ref=repository.publication_bundle_ref,
        index_manifest_ref=repository.index_manifest.ref,
        objective_world_scope_ref=_ref(OBJECTIVE_WORLD_SCOPE_REF_KIND, "scope-r1"),
        valid_time_authority_ref=_authority("VALID-TIME"),
        world_validity_ref=_ref(OBJECTIVE_WORLD_VALIDITY_REF_KIND, validity_label),
        predecessor_world_root_ref=predecessor,
    )


def test_same_tuple_is_content_addressed_and_replays_exactly():
    _, repository = _repo()
    first = _root(repository)
    second = _root(repository)
    replayed = replay_objective_world_release_root(first, repository=repository)
    assert first.ref == second.ref == replayed.ref
    assert first.root_id == f"PREV3WORLD:{first.root_hash}"
    assert first.ref.kind == WORLD_ROOT_REF_KIND


def test_repository_publication_and_index_must_be_exactly_coupled():
    _, repository = _repo()
    with pytest.raises(ObjectiveWorldRootError, match="publication_bundle_ref"):
        build_objective_world_release_root(
            release_authority_ref=_authority("RELEASE"),
            repository=repository,
            publication_bundle_ref=_ref("V557_PUBLICATION_BUNDLE", "wrong-publication"),
            index_manifest_ref=repository.index_manifest.ref,
            objective_world_scope_ref=_ref(OBJECTIVE_WORLD_SCOPE_REF_KIND, "scope-r1"),
            valid_time_authority_ref=_authority("VALID-TIME"),
            world_validity_ref=_ref(OBJECTIVE_WORLD_VALIDITY_REF_KIND, "validity-r1"),
        )
    with pytest.raises(ObjectiveWorldRootError, match="index_manifest_ref"):
        build_objective_world_release_root(
            release_authority_ref=_authority("RELEASE"),
            repository=repository,
            publication_bundle_ref=repository.publication_bundle_ref,
            index_manifest_ref=_ref("V558_INDEX_MANIFEST", "wrong-index"),
            objective_world_scope_ref=_ref(OBJECTIVE_WORLD_SCOPE_REF_KIND, "scope-r1"),
            valid_time_authority_ref=_authority("VALID-TIME"),
            world_validity_ref=_ref(OBJECTIVE_WORLD_VALIDITY_REF_KIND, "validity-r1"),
        )


def test_stale_repository_checksum_fails_before_root_identity_is_minted():
    _, repository = _repo()
    stale = replace(repository, repository_hash=_h("stale-repository"))
    with pytest.raises(ObjectiveWorldRootError, match="repository checksum"):
        _root(stale)


def test_scope_and_world_validity_are_exact_objective_owned_ref_classes():
    _, repository = _repo()
    with pytest.raises(ObjectiveWorldRootError, match="objective_world_scope_ref"):
        build_objective_world_release_root(
            release_authority_ref=_authority("RELEASE"),
            repository=repository,
            publication_bundle_ref=repository.publication_bundle_ref,
            index_manifest_ref=repository.index_manifest.ref,
            objective_world_scope_ref=_ref("V3_ACTOR_SCOPE", "scope-r1"),
            valid_time_authority_ref=_authority("VALID-TIME"),
            world_validity_ref=_ref(OBJECTIVE_WORLD_VALIDITY_REF_KIND, "validity-r1"),
        )
    with pytest.raises(ObjectiveWorldRootError, match="world_validity_ref"):
        build_objective_world_release_root(
            release_authority_ref=_authority("RELEASE"),
            repository=repository,
            publication_bundle_ref=repository.publication_bundle_ref,
            index_manifest_ref=repository.index_manifest.ref,
            objective_world_scope_ref=_ref(OBJECTIVE_WORLD_SCOPE_REF_KIND, "scope-r1"),
            valid_time_authority_ref=_authority("VALID-TIME"),
            world_validity_ref=_ref("M5_STRUCTURAL_CURRENTNESS_RECEIPT", "m5-currentness"),
        )


def test_v3_actor_person_cursor_and_latest_cannot_bootstrap_world_validity():
    _, repository = _repo()
    for label in ("actor-validity", "person-validity", "v3-validity", "cursor-validity", "latest"):
        with pytest.raises(ObjectiveWorldRootError):
            build_objective_world_release_root(
                release_authority_ref=_authority("RELEASE"),
                repository=repository,
                publication_bundle_ref=repository.publication_bundle_ref,
                index_manifest_ref=repository.index_manifest.ref,
                objective_world_scope_ref=_ref(OBJECTIVE_WORLD_SCOPE_REF_KIND, "scope-r1"),
                valid_time_authority_ref=_authority("VALID-TIME"),
                world_validity_ref=ExactRef(
                    OBJECTIVE_WORLD_VALIDITY_REF_KIND,
                    f"urn:test:w2-d01:{label}",
                    _h(f"validity:{label}"),
                ),
            )


def test_changed_world_validity_changes_only_root_identity_when_producer_refs_are_fixed():
    _, repository = _repo()
    first = _root(repository, validity_label="validity-r1")
    second = _root(repository, validity_label="validity-r2")
    assert first.ref != second.ref
    assert first.repository_ref == second.repository_ref == repository.ref
    assert first.publication_bundle_ref == second.publication_bundle_ref
    assert first.index_manifest_ref == second.index_manifest_ref


def test_predecessor_must_be_exact_immutable_world_root_ref():
    _, repository = _repo()
    first = _root(repository)
    successor = _root(repository, validity_label="validity-r2", predecessor=first.ref)
    assert successor.predecessor_world_root_ref == first.ref
    assert successor.ref != first.ref
    with pytest.raises(ObjectiveWorldRootError, match="predecessor_world_root_ref"):
        _root(repository, predecessor=_ref("OTHER_ROOT", "wrong-predecessor"))


def test_constructor_surface_has_no_v3_actor_cursor_wall_clock_or_latest_inputs():
    names = set(inspect.signature(build_objective_world_release_root).parameters)
    forbidden = {
        "actor_id", "person_id", "persona", "v3_state", "v3_cursor",
        "runtime_cursor", "wall_clock", "timestamp", "latest", "default",
    }
    assert not names & forbidden
