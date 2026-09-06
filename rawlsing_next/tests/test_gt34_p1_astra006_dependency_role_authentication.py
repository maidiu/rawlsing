from dataclasses import replace

import pytest

from rawlsing_next.m4_v557_v558_publication_repository import (
    AuthorityRef,
    ClosureIntegrityError,
    ContextQueryItem,
    ExactRef,
    M4IntegrityError,
    RepositoryEntry,
    V557DecisionState,
    V557PublicationEntry,
    V558_DEPENDENCY_ROLE_AUTH_EXACT,
    V558_DEPENDENCY_ROLE_AUTH_LEGACY,
    build_role_authenticated_v558_repository_bundle,
    build_v557_publication_bundle,
    build_v558_repository_bundle,
    exact_resolution_key,
    govern_v557,
    make_context_query,
    make_dependency_role_binding,
    make_producer_locator,
    make_reference_edge,
    make_structural_object,
    require_authenticated_dependency_roles,
    resolve_v558,
    semantic_hash,
)
from rawlsing_next.m5_runtime_rsc_peer_prior import (
    M5RuntimeIntegrityError,
    StructuralCurrentnessState,
    make_structural_currentness_receipt,
    materialize_resolved_structural_context,
)


def _h(label: str) -> str:
    return semantic_hash({"label": label})


def _authority(label: str) -> AuthorityRef:
    return AuthorityRef(f"AUTH-{label}", "1.0.0", _h(f"authority-{label}"))


def _obj(
    tag: str,
    *,
    uses=("REVIEW",),
    required=(),
    negative=(),
    payload=None,
):
    body = payload if payload is not None else {"tag": tag, "semantic_class": "TEMPORAL_KEY"}
    return make_structural_object(
        producer_family="V553",
        semantic_class="TEMPORAL_KEY",
        object_id=f"urn:test:v553:{tag}",
        schema_id="TEST_V553_SCHEMA",
        schema_version="1.0.0",
        typed_state="SUPPORTED",
        producer_allowed_uses=uses,
        payload=body,
        source_stage=f"TEST-{tag}",
        required_dependency_refs=required,
        negative_dependency_refs=negative,
    )


def _entry(
    obj,
    tag: str,
    *,
    uses=("REVIEW",),
    state=V557DecisionState.ALLOW_REVIEW_ONLY,
):
    governance = govern_v557(
        obj,
        decision_state=state,
        v557_allowed_uses=uses,
        authority_ref=_authority(f"gov-{tag}"),
    )
    locator = make_producer_locator(
        obj,
        governance,
        logical_collection_kind=f"COLLECTION-{tag}",
        authoritative_build_id=f"BUILD-{tag}",
        authoritative_build_hash=_h(f"build-{tag}"),
        producer_contract_id="TEST_V553_CONTRACT",
        producer_contract_version="1.0.0",
        producer_contract_hash=_h("test-v553-contract"),
        producer_rule_bindings=(_authority(f"rule-{tag}"),),
    )
    return RepositoryEntry(obj, governance, locator)


def _closure_fixture():
    positive = _obj("positive")
    negative = _obj("negative")
    root = _obj("root", required=(positive.ref,), negative=(negative.ref,))
    root_e = _entry(root, "root")
    pos_e = _entry(positive, "positive")
    neg_e = _entry(negative, "negative")
    publication = build_v557_publication_bundle(
        (V557PublicationEntry(root_e.obj, root_e.governance),)
    )
    contract = _authority("closure")
    pos_edge = make_reference_edge(
        root_e.locator,
        pos_e.locator,
        reference_contract=contract,
        edge_role="AUTHORITY",
    )
    neg_edge = make_reference_edge(
        root_e.locator,
        neg_e.locator,
        reference_contract=contract,
        edge_role="NEGATIVE_LIMIT",
    )
    return root, positive, negative, root_e, pos_e, neg_e, publication, pos_edge, neg_edge


def _binding_for(repository, producer_ref):
    return next(
        binding
        for binding in repository.dependency_role_bindings
        if binding.producer_object_ref == producer_ref
    )


def test_o3_public_reconstruction_attack_reproduces_on_legacy_boundary():
    root, positive, negative, root_e, pos_e, neg_e, publication, pos_edge, neg_edge = _closure_fixture()
    weakened = _obj("root", required=(positive.ref,))
    assert weakened.ref == root.ref
    assert weakened.negative_dependency_refs == ()
    weakened_e = RepositoryEntry(weakened, root_e.governance, root_e.locator)

    legacy = build_v558_repository_bundle(
        publication,
        (weakened_e, pos_e, neg_e),
        reference_edges=(pos_edge, neg_edge),
    )
    query = make_context_query(
        (ContextQueryItem(exact_resolution_key(root_e.locator), ("REVIEW",)),)
    )
    result = resolve_v558(legacy, query)
    assert result.receipt.result_state == "RESOLUTION_COMPLETE"
    assert result.resolved_entries[0].producer_object_ref == root.ref


def test_role_authenticated_boundary_changes_effective_identity_when_role_is_stripped():
    root, positive, negative, root_e, pos_e, neg_e, publication, pos_edge, neg_edge = _closure_fixture()
    complete = build_role_authenticated_v558_repository_bundle(
        publication,
        (root_e, pos_e, neg_e),
        reference_edges=(pos_edge, neg_edge),
    )
    weakened = _obj("root", required=(positive.ref,))
    weakened_e = RepositoryEntry(weakened, root_e.governance, root_e.locator)
    weakened_repo = build_role_authenticated_v558_repository_bundle(
        publication,
        (weakened_e, pos_e, neg_e),
        reference_edges=(pos_edge, neg_edge),
    )

    assert weakened.ref == root.ref
    assert complete.ref != weakened_repo.ref
    assert _binding_for(complete, root.ref).ref != _binding_for(weakened_repo, root.ref).ref
    require_authenticated_dependency_roles(complete)
    require_authenticated_dependency_roles(weakened_repo)


def test_dropping_negative_with_original_binding_fails_closed():
    root, positive, negative, root_e, pos_e, neg_e, publication, pos_edge, neg_edge = _closure_fixture()
    complete = build_role_authenticated_v558_repository_bundle(
        publication,
        (root_e, pos_e, neg_e),
        reference_edges=(pos_edge, neg_edge),
    )
    weakened = _obj("root", required=(positive.ref,))
    weakened_e = RepositoryEntry(weakened, root_e.governance, root_e.locator)

    with pytest.raises(ClosureIntegrityError, match="differs from exact producer role declarations"):
        build_v558_repository_bundle(
            publication,
            (weakened_e, pos_e, neg_e),
            reference_edges=(pos_edge, neg_edge),
            dependency_role_bindings=complete.dependency_role_bindings,
            dependency_role_authentication=V558_DEPENDENCY_ROLE_AUTH_EXACT,
        )


@pytest.mark.parametrize(
    "required,negative",
    [
        pytest.param(lambda positive, negative: (negative.ref,), lambda positive, negative: (positive.ref,), id="required-to-negative-and-negative-to-required"),
        pytest.param(lambda positive, negative: (positive.ref, negative.ref), lambda positive, negative: (), id="negative-to-required"),
        pytest.param(lambda positive, negative: (), lambda positive, negative: (positive.ref, negative.ref), id="required-to-negative"),
    ],
)
def test_role_reclassification_cannot_reuse_accepted_binding(required, negative):
    root, positive, negative_obj, root_e, pos_e, neg_e, publication, pos_edge, neg_edge = _closure_fixture()
    complete = build_role_authenticated_v558_repository_bundle(
        publication,
        (root_e, pos_e, neg_e),
        reference_edges=(pos_edge, neg_edge),
    )
    reclassified = _obj(
        "root",
        required=required(positive, negative_obj),
        negative=negative(positive, negative_obj),
    )
    assert reclassified.ref == root.ref
    reclassified_e = RepositoryEntry(reclassified, root_e.governance, root_e.locator)

    with pytest.raises(ClosureIntegrityError, match="differs from exact producer role declarations"):
        build_v558_repository_bundle(
            publication,
            (reclassified_e, pos_e, neg_e),
            reference_edges=(pos_edge, neg_edge),
            dependency_role_bindings=complete.dependency_role_bindings,
            dependency_role_authentication=V558_DEPENDENCY_ROLE_AUTH_EXACT,
        )


def test_noncanonical_authentication_mode_spelling_fails_before_hashing():
    root, positive, negative, root_e, pos_e, neg_e, publication, pos_edge, neg_edge = _closure_fixture()
    complete = build_role_authenticated_v558_repository_bundle(
        publication,
        (root_e, pos_e, neg_e),
        reference_edges=(pos_edge, neg_edge),
    )
    with pytest.raises(M4IntegrityError, match="must be canonical exact text"):
        build_v558_repository_bundle(
            publication,
            (root_e, pos_e, neg_e),
            reference_edges=(pos_edge, neg_edge),
            dependency_role_bindings=complete.dependency_role_bindings,
            dependency_role_authentication=f" {V558_DEPENDENCY_ROLE_AUTH_EXACT} ",
        )


def test_stale_role_binding_hash_fails():
    root, positive, negative, root_e, pos_e, neg_e, publication, pos_edge, neg_edge = _closure_fixture()
    complete = build_role_authenticated_v558_repository_bundle(
        publication,
        (root_e, pos_e, neg_e),
        reference_edges=(pos_edge, neg_edge),
    )
    root_binding = _binding_for(complete, root.ref)
    stale = replace(root_binding, binding_hash=_h("stale-role-binding"))
    bindings = tuple(
        stale if binding.producer_object_ref == root.ref else binding
        for binding in complete.dependency_role_bindings
    )

    with pytest.raises(ClosureIntegrityError, match="identity/hash is stale or corrupt"):
        build_v558_repository_bundle(
            publication,
            (root_e, pos_e, neg_e),
            reference_edges=(pos_edge, neg_edge),
            dependency_role_bindings=bindings,
            dependency_role_authentication=V558_DEPENDENCY_ROLE_AUTH_EXACT,
        )


def test_wrong_producer_role_binding_fails():
    root, positive, negative, root_e, pos_e, neg_e, publication, pos_edge, neg_edge = _closure_fixture()
    complete = build_role_authenticated_v558_repository_bundle(
        publication,
        (root_e, pos_e, neg_e),
        reference_edges=(pos_edge, neg_edge),
    )
    other = _obj("other")
    wrong = make_dependency_role_binding(other)
    bindings = tuple(
        wrong if binding.producer_object_ref == root.ref else binding
        for binding in complete.dependency_role_bindings
    )

    with pytest.raises(ClosureIntegrityError, match="wrong or absent producer ref"):
        build_v558_repository_bundle(
            publication,
            (root_e, pos_e, neg_e),
            reference_edges=(pos_edge, neg_edge),
            dependency_role_bindings=bindings,
            dependency_role_authentication=V558_DEPENDENCY_ROLE_AUTH_EXACT,
        )


def test_role_complete_safe_bundle_resolves_same_producer_as_legacy():
    root, positive, negative, root_e, pos_e, neg_e, publication, pos_edge, neg_edge = _closure_fixture()
    legacy = build_v558_repository_bundle(
        publication,
        (root_e, pos_e, neg_e),
        reference_edges=(pos_edge, neg_edge),
    )
    safe = build_role_authenticated_v558_repository_bundle(
        publication,
        (root_e, pos_e, neg_e),
        reference_edges=(pos_edge, neg_edge),
    )
    query = make_context_query(
        (ContextQueryItem(exact_resolution_key(root_e.locator), ("REVIEW",)),)
    )
    legacy_result = resolve_v558(legacy, query)
    safe_result = resolve_v558(safe, query)

    assert legacy_result.receipt.result_state == safe_result.receipt.result_state == "RESOLUTION_COMPLETE"
    assert [entry.producer_object_ref for entry in legacy_result.resolved_entries] == [
        entry.producer_object_ref for entry in safe_result.resolved_entries
    ]
    assert legacy.ref != safe.ref


def test_opaque_lineage_in_payload_remains_non_dependency():
    lineage = ExactRef("OPAQUE_LINEAGE", "urn:test:lineage", _h("lineage"))
    root = _obj("opaque", payload={"lineage_ref": lineage.as_dict(), "meaning": "audit only"})
    root_e = _entry(root, "opaque")
    publication = build_v557_publication_bundle(
        (V557PublicationEntry(root_e.obj, root_e.governance),)
    )
    safe = build_role_authenticated_v558_repository_bundle(publication, (root_e,))
    binding = _binding_for(safe, root.ref)

    assert binding.required_dependency_refs == ()
    assert binding.negative_dependency_refs == ()
    assert safe.reference_edges == ()


def test_itemwise_permission_behavior_is_unchanged():
    dep = _obj("review-only", uses=("REVIEW",))
    root = _obj("context-root", uses=("REVIEW", "CONTEXT"), required=(dep.ref,))
    root_e = _entry(
        root,
        "context-root",
        uses=("REVIEW", "CONTEXT"),
        state=V557DecisionState.ALLOW_CONTEXT_ONLY,
    )
    dep_e = _entry(dep, "review-only")
    publication = build_v557_publication_bundle(
        (V557PublicationEntry(root_e.obj, root_e.governance),)
    )
    edge = make_reference_edge(
        root_e.locator,
        dep_e.locator,
        reference_contract=_authority("permission-edge"),
        edge_role="AUTHORITY",
    )
    safe = build_role_authenticated_v558_repository_bundle(
        publication,
        (root_e, dep_e),
        reference_edges=(edge,),
    )
    query = make_context_query(
        (ContextQueryItem(exact_resolution_key(root_e.locator), ("CONTEXT",)),)
    )
    result = resolve_v558(safe, query)
    assert result.receipt.result_state == "RESOLUTION_DENIED_OR_NOT_APPLICABLE"
    assert result.selection_records[0].decision == "PERMISSION_DENIED"


def test_legacy_repository_hash_material_remains_unchanged():
    root = _obj("legacy")
    root_e = _entry(root, "legacy")
    publication = build_v557_publication_bundle(
        (V557PublicationEntry(root_e.obj, root_e.governance),)
    )
    legacy = build_v558_repository_bundle(publication, (root_e,))

    old_material = {
        "schema": legacy.schema,
        "m4_contract_id": "M4_SCR5578_MIXED_PRODUCER_FINAL_SEAM@1.0.0",
        "publication_bundle_ref": publication.ref.as_dict(),
        "entries": [{
            "object_ref": root_e.obj.ref.as_dict(),
            "producer_family": root_e.obj.producer_family,
            "typed_state": root_e.obj.typed_state,
            "governance_ref": root_e.governance.ref.as_dict(),
            "locator_ref": root_e.locator.ref.as_dict(),
        }],
        "reference_edges": [],
        "external_bindings": [],
        "index_manifest_ref": legacy.index_manifest.ref.as_dict(),
    }
    assert legacy.repository_hash == semantic_hash(old_material)
    assert legacy.dependency_role_authentication == V558_DEPENDENCY_ROLE_AUTH_LEGACY
    assert legacy.dependency_role_bindings == ()


def test_m5_exact_reresolution_rejects_weakened_role_bound_repository_against_accepted_evidence():
    root, positive, negative, root_e, pos_e, neg_e, publication, pos_edge, neg_edge = _closure_fixture()
    safe = build_role_authenticated_v558_repository_bundle(
        publication,
        (root_e, pos_e, neg_e),
        reference_edges=(pos_edge, neg_edge),
    )
    query = make_context_query(
        (ContextQueryItem(exact_resolution_key(root_e.locator), ("REVIEW",)),)
    )
    resolution = resolve_v558(safe, query)
    currentness = make_structural_currentness_receipt(
        resolution,
        state=StructuralCurrentnessState.CURRENT,
        authority_ref=_authority("currentness"),
        structural_currentness_basis_ref=ExactRef("CURRENTNESS_BASIS", "urn:test:current", _h("current")),
        decision_effective_time_ref=ExactRef("TIME", "urn:test:time", _h("time")),
    )
    materialize_resolved_structural_context(safe, query, resolution, currentness)

    weakened = _obj("root", required=(positive.ref,))
    weakened_e = RepositoryEntry(weakened, root_e.governance, root_e.locator)
    weakened_safe = build_role_authenticated_v558_repository_bundle(
        publication,
        (weakened_e, pos_e, neg_e),
        reference_edges=(pos_edge, neg_edge),
    )

    with pytest.raises(M5RuntimeIntegrityError, match="differs from deterministic exact re-resolution"):
        materialize_resolved_structural_context(
            weakened_safe,
            query,
            resolution,
            currentness,
        )
