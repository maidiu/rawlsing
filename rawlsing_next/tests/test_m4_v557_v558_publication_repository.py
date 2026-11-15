from dataclasses import replace

import pytest

from rawlsing_next.m1_temporal_v554_admission_dedup import (
    M1_CONTRACT_ID,
    M1DecisionState,
    M1Evaluation,
    semantic_hash,
)
from rawlsing_next.m2_v555_atomic_route import (
    CHANNEL_STRUCTURAL_ROLE_ID,
    M2_CONTRACT_ID,
    M2DecisionState,
    M2Evaluation,
    RECEIVING_CONSTRAINT_KIND,
    ROUTE_RULE_ID,
    ROUTE_RULE_VERSION,
    ROUTE_SHAPE_ID,
    ROUTE_SHAPE_VERSION,
    SEMANTIC_FAMILY as V555_SEMANTIC_FAMILY,
)
from rawlsing_next.m3_v556_higher_order_structural import (
    M3_CONTRACT_ID,
    M3DecisionState,
    M3Evaluation,
)
from rawlsing_next.m4_v557_v558_publication_repository import (
    AUDIT_ONLY_CLASSES,
    M4IntegrityError,
    PermissionWideningError,
    ClosureIntegrityError,
    ReferenceClassError,
    AuthorityRef,
    ContextQueryItem,
    RepositoryEntry,
    ResolverPolicy,
    V557DecisionState,
    V557PublicationEntry,
    build_v557_publication_bundle,
    build_v558_repository_bundle,
    exact_resolution_key,
    govern_v557,
    make_context_query,
    make_external_resolution_binding,
    make_external_stub,
    make_producer_locator,
    make_reference_edge,
    make_structural_object,
    resolve_v558,
    structural_object_from_m2,
    structural_object_from_m3,
    structural_objects_from_m1,
)


def _h(label: str) -> str:
    return semantic_hash({"label": label})


def _authority(label: str) -> AuthorityRef:
    return AuthorityRef(f"AUTH-{label}", "1.0.0", _h(f"authority-{label}"))


def _obj(
    tag: str,
    *,
    family: str = "V553",
    semantic_class: str = "TEMPORAL_KEY",
    state: str = "SUPPORTED",
    uses=("REVIEW",),
    required=(),
    negative=(),
    payload=None,
):
    body = payload if payload is not None else {"tag": tag, "semantic_class": semantic_class, "state": state}
    return make_structural_object(
        producer_family=family,
        semantic_class=semantic_class,
        object_id=f"urn:test:{family.lower()}:{tag}",
        schema_id=f"TEST_{family}_SCHEMA",
        schema_version="1.0.0",
        typed_state=state,
        producer_allowed_uses=uses,
        payload=body,
        source_stage=f"TEST-{tag}",
        required_dependency_refs=required,
        negative_dependency_refs=negative,
    )


def _gov(obj, uses=("REVIEW",), state=V557DecisionState.ALLOW_REVIEW_ONLY):
    return govern_v557(
        obj,
        decision_state=state,
        v557_allowed_uses=uses,
        authority_ref=_authority(f"gov-{obj.object_id}"),
    )


def _loc(obj, gov, tag: str, *, provenance=None, storage=None):
    return make_producer_locator(
        obj,
        gov,
        logical_collection_kind=f"COLLECTION-{obj.producer_family}",
        authoritative_build_id=f"BUILD-{tag}",
        authoritative_build_hash=_h(f"build-{tag}"),
        producer_contract_id=f"CONTRACT-{obj.producer_family}",
        producer_contract_version="1.0.0",
        producer_contract_hash=_h(f"contract-{obj.producer_family}"),
        producer_rule_bindings=(_authority(f"rule-{tag}"),),
        storage_locator=storage,
        provenance_locator=provenance,
    )


def _entry(obj, tag: str, *, uses=("REVIEW",), state=V557DecisionState.ALLOW_REVIEW_ONLY, provenance=None, storage=None):
    gov = _gov(obj, uses=uses, state=state)
    loc = _loc(obj, gov, tag, provenance=provenance, storage=storage)
    return RepositoryEntry(obj, gov, loc)


def _repo_for_roots(entries):
    roots = tuple(V557PublicationEntry(e.obj, e.governance) for e in entries)
    publication = build_v557_publication_bundle(roots)
    return publication, build_v558_repository_bundle(publication, entries)


def _m1_eval(tag: str) -> M1Evaluation:
    f1 = {
        "family": "F1",
        "state": "ELIGIBLE",
        "f1_id": f"urn:rawlsing:v554:f1:sha256:{_h('m1-f1-' + tag)}",
        "material": {"tag": tag, "target_use": "STRUCTURAL_MEDIATION_INPUT"},
    }
    b1 = {
        "family": "B1",
        "decision_state": "ELIGIBLE",
        "b1_id": f"urn:rawlsing:v554:b1:sha256:{_h('m1-b1-' + tag)}",
        "material": {"tag": tag, "f1_id_or_null": f1["f1_id"]},
    }
    refs = (
        {"family": "F1", "object_id": f1["f1_id"], "content_hash": semantic_hash(f1)},
        {"family": "B1", "object_id": b1["b1_id"], "content_hash": semantic_hash(b1)},
    )
    return M1Evaluation(
        M1_CONTRACT_ID,
        M1DecisionState.ELIGIBLE,
        "test exact direct M1 handoff",
        f"USE-{tag}",
        "DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION",
        1,
        f"urn:test:basis:{tag}",
        f1,
        (),
        b1,
        {"route": "V554_TO_V557_DIRECT", "object_refs": refs},
        (),
    )


def _m2_eval(tag: str, *, uses=("REVIEW",)) -> M2Evaluation:
    f1_payload = {"tag": f"f1-{tag}"}
    b1_payload = {"tag": f"b1-{tag}"}
    f1_ref = {
        "kind": "F1",
        "object_id": f"urn:test:f1:{tag}",
        "content_hash": semantic_hash(f1_payload),
    }
    b1_ref = {
        "kind": "B1",
        "object_id": f"urn:test:b1:{tag}",
        "content_hash": semantic_hash(b1_payload),
    }
    channel = {"kind": "STRUCTURAL_CHANNEL", "object_id": f"urn:test:channel:{tag}", "content_hash": _h(f"channel-{tag}")}
    receiver = {"kind": "STRUCTURAL_POSITION", "object_id": f"urn:test:receiver:{tag}", "content_hash": _h(f"receiver-{tag}")}
    ident = (
        f1_ref["object_id"],
        f"{ROUTE_RULE_ID}@{ROUTE_RULE_VERSION}",
        f"{ROUTE_SHAPE_ID}@{ROUTE_SHAPE_VERSION}",
        CHANNEL_STRUCTURAL_ROLE_ID,
        channel,
        RECEIVING_CONSTRAINT_KIND,
        receiver,
    )
    ih = semantic_hash(list(ident))
    route = {
        "semantic_family": V555_SEMANTIC_FAMILY,
        "route_id": f"urn:rawlsing:v555:route:sha256:{ih}",
        "canonical_route_identity": ident,
        "canonical_route_identity_hash": ih,
        "producer_allowed_uses": tuple(uses),
        "ordered_structure": (
            {"ordinal": 1, "role": "SOURCE", "binding": {"kind": "STRUCTURAL_POSITION", "object_id": f"urn:test:source:{tag}", "content_hash": _h(f"source-{tag}")}},
            {"ordinal": 2, "role": "MEDIATION_LOCUS", "binding": channel, "channel_structural_role_id": CHANNEL_STRUCTURAL_ROLE_ID},
            {"ordinal": 3, "role": "RECEIVER", "binding": receiver, "receiving_constraint_kind": RECEIVING_CONSTRAINT_KIND},
        ),
    }
    route_hash = semantic_hash(route)
    return M2Evaluation(
        M2_CONTRACT_ID,
        M2DecisionState.ROUTE_CANDIDATE_AUTHORIZED,
        "test exact M2 route",
        M1DecisionState.ELIGIBLE.value,
        f1_ref,
        b1_ref,
        (),
        ident,
        ih,
        route,
        {"state": "VALID_EMPTY", "registered_predicate_count": 0},
        {
            "route": "V555_TO_V557_DIRECT",
            "route_ref": {"kind": V555_SEMANTIC_FAMILY, "object_id": route["route_id"], "content_hash": route_hash},
        },
        _h(f"replay-{tag}"),
    )


def _m3_eval(tag: str, route_refs) -> M3Evaluation:
    roles = ("SOURCE_SIDE", "RECEIVER_SIDE")
    bindings = tuple(
        {
            "v555_route_identity_ref": ref,
            "role": role,
            "ordinal_or_null": index,
            "multiplicity_index": 0,
        }
        for index, (ref, role) in enumerate(zip(route_refs, roles), start=1)
    )
    replay = _h(f"m3-replay-{tag}")
    obj = {
        "object_id": f"urn:rawlsing:v556:higher-order:sha256:{replay}",
        "semantic_family": "V556_TOPOLOGY",
        "typed_outcome_state": "SUPPORTED",
        "rule_authority": {
            "semantic_family": "V556_TOPOLOGY",
            "minimum_cardinality": 2,
            "maximum_cardinality_or_unbounded_marker": "UNBOUNDED",
            "participant_order_policy": "ORDERED",
            "participant_roles": roles,
            "same_route_reuse_policy": "FORBIDDEN",
        },
        "participant_bindings": bindings,
        "source_composition_authority": None,
        "semantic_payload": {"topology_kind": "EXACT_TEST_RELATION", "tag": tag},
        "producer_allowed_uses": ("REVIEW",),
        "replay_key_hash": replay,
        "actor_independent": True,
    }
    return M3Evaluation(
        M3_CONTRACT_ID,
        M3DecisionState.SUPPORTED,
        "test exact M3 object",
        "V556_EVALUATED",
        bindings,
        obj,
        (),
        replay,
    )


def test_v557_permission_nonwidening_and_locator_provenance_never_grants_permission():
    obj = _obj("permission", uses=("REVIEW",))
    with pytest.raises(PermissionWideningError):
        _gov(obj, uses=("CONTEXT",), state=V557DecisionState.ALLOW_CONTEXT_ONLY)

    gov = _gov(obj, uses=("REVIEW",))
    loc = _loc(obj, gov, "permission", provenance="audit://AUTHORIZED/ACTIVE_CAUSAL")
    entry = RepositoryEntry(obj, gov, loc)
    publication = build_v557_publication_bundle((V557PublicationEntry(obj, gov),))
    repo = build_v558_repository_bundle(publication, (entry,))
    query = make_context_query((ContextQueryItem(exact_resolution_key(loc), ("CONTEXT",)),))
    result = resolve_v558(repo, query)
    assert result.receipt.result_state == "RESOLUTION_DENIED_OR_NOT_APPLICABLE"
    assert result.selection_records[0].decision == "PERMISSION_DENIED"
    assert result.resolved_entries == ()


def test_v557_and_v558_remain_distinct_and_resolver_is_deterministic_without_rsc_fabrication():
    obj = _obj("distinct", uses=("REVIEW", "CONTEXT"))
    entry = _entry(obj, "distinct", uses=("REVIEW", "CONTEXT"), state=V557DecisionState.ALLOW_CONTEXT_ONLY)
    publication, repo = _repo_for_roots((entry,))
    assert publication.publication_id.startswith("V557PUB:")
    assert repo.repository_id.startswith("V558REPO:")
    assert publication.publication_id != repo.repository_id
    assert repo.publication_bundle_ref == publication.ref

    query = make_context_query((ContextQueryItem(exact_resolution_key(entry.locator), ("REVIEW",)),))
    first = resolve_v558(repo, query)
    second = resolve_v558(repo, query)
    assert first.receipt.receipt_hash == second.receipt.receipt_hash
    assert first.selection_records[0].selection_record_hash == second.selection_records[0].selection_record_hash
    assert first.resolved_structural_context is None
    assert first.receipt.result_state == "RESOLUTION_COMPLETE"


def test_direct_m1_m2_and_m3_paths_coexist_without_filler_or_reidentification():
    m1_objects = structural_objects_from_m1(_m1_eval("coexist"), producer_allowed_uses=("REVIEW",))
    assert {x.semantic_class for x in m1_objects} == {"F1", "B1"}

    m2_eval = _m2_eval("coexist")
    m2_obj = structural_object_from_m2(m2_eval)
    assert m2_obj.object_id == m2_eval.route["route_id"]
    assert tuple(m2_obj.payload["canonical_route_identity"]) == m2_eval.canonical_route_identity

    second_m2 = _m2_eval("coexist-2")
    route_refs = (
        {"kind": V555_SEMANTIC_FAMILY, "object_id": m2_eval.route["route_id"], "content_hash": semantic_hash(m2_eval.route)},
        {"kind": V555_SEMANTIC_FAMILY, "object_id": second_m2.route["route_id"], "content_hash": semantic_hash(second_m2.route)},
    )
    m3_eval = _m3_eval("coexist", route_refs)
    m3_obj = structural_object_from_m3(m3_eval)
    assert m3_obj.object_id == m3_eval.v556_object["object_id"]
    assert len(m3_obj.required_dependency_refs) == 2
    assert m3_obj.content_hash == semantic_hash(m3_eval.v556_object)

    objects = (*m1_objects, m2_obj, m3_obj)
    entries = tuple(V557PublicationEntry(o, _gov(o)) for o in objects)
    publication = build_v557_publication_bundle(entries)
    assert {e.obj.producer_family for e in publication.entries} == {"V554", "V555", "V556"}
    assert len(publication.entries) == len(objects)


def test_v555_tuple_field_one_must_remain_exact_f1_and_b1_cannot_be_promoted():
    original = _m2_eval("tuple-guard")
    bad_ident = ("urn:test:f1:wrong",) + original.canonical_route_identity[1:]
    bad_hash = semantic_hash(list(bad_ident))
    bad_route = dict(original.route)
    bad_route["canonical_route_identity"] = bad_ident
    bad_route["canonical_route_identity_hash"] = bad_hash
    bad_route["route_id"] = f"urn:rawlsing:v555:route:sha256:{bad_hash}"
    bad = replace(original, canonical_route_identity=bad_ident, canonical_route_identity_hash=bad_hash, route=bad_route)
    with pytest.raises(M4IntegrityError, match="field 1"):
        structural_object_from_m2(bad, require_direct_handoff=False)

    b1_ident = (original.exact_v554_b1_ref["object_id"],) + original.canonical_route_identity[1:]
    b1_hash = semantic_hash(list(b1_ident))
    b1_route = dict(original.route)
    b1_route["canonical_route_identity"] = b1_ident
    b1_route["canonical_route_identity_hash"] = b1_hash
    b1_route["route_id"] = f"urn:rawlsing:v555:route:sha256:{b1_hash}"
    b1_bad = replace(original, canonical_route_identity=b1_ident, canonical_route_identity_hash=b1_hash, route=b1_route)
    with pytest.raises(M4IntegrityError):
        structural_object_from_m2(b1_bad, require_direct_handoff=False)


def test_m3_rule_owned_cardinality_is_enforced_without_changing_producer_bytes():
    p1_payload = {"route": "p1-card"}
    p2_payload = {"route": "p2-card"}
    refs = (
        {"kind": V555_SEMANTIC_FAMILY, "object_id": "urn:test:v555:p1-card", "content_hash": semantic_hash(p1_payload)},
        {"kind": V555_SEMANTIC_FAMILY, "object_id": "urn:test:v555:p2-card", "content_hash": semantic_hash(p2_payload)},
    )
    good = _m3_eval("cardinality", refs)
    wrapped = structural_object_from_m3(good)
    assert wrapped.content_hash == semantic_hash(good.v556_object)

    bad_obj = dict(good.v556_object)
    bad_rule = dict(bad_obj["rule_authority"])
    bad_rule["minimum_cardinality"] = 3
    bad_obj["rule_authority"] = bad_rule
    bad = replace(good, v556_object=bad_obj)
    with pytest.raises(M4IntegrityError, match="occurrence count"):
        structural_object_from_m3(bad)


def test_v556_role_order_cardinality_multiplicity_survives_and_partial_nary_fails_closed():
    p1_payload = {"route": "p1"}
    p2_payload = {"route": "p2"}
    p1_ref = {"kind": V555_SEMANTIC_FAMILY, "object_id": "urn:test:v555:p1", "content_hash": semantic_hash(p1_payload)}
    p2_ref = {"kind": V555_SEMANTIC_FAMILY, "object_id": "urn:test:v555:p2", "content_hash": semantic_hash(p2_payload)}
    m3_obj = structural_object_from_m3(_m3_eval("structure", (p1_ref, p2_ref)))
    p1 = make_structural_object(
        producer_family="V555", semantic_class=V555_SEMANTIC_FAMILY, object_id=p1_ref["object_id"],
        schema_id="TEST_V555", schema_version="1.0.0", typed_state="ROUTE_CANDIDATE_AUTHORIZED",
        producer_allowed_uses=("REVIEW",), payload=p1_payload, source_stage="TEST",
    )
    p2 = make_structural_object(
        producer_family="V555", semantic_class=V555_SEMANTIC_FAMILY, object_id=p2_ref["object_id"],
        schema_id="TEST_V555", schema_version="1.0.0", typed_state="ROUTE_CANDIDATE_AUTHORIZED",
        producer_allowed_uses=("REVIEW",), payload=p2_payload, source_stage="TEST",
    )
    root_e = _entry(m3_obj, "v556")
    p1_e = _entry(p1, "p1")
    p2_e = _entry(p2, "p2")
    publication = build_v557_publication_bundle((V557PublicationEntry(root_e.obj, root_e.governance),))
    contract = _authority("v556-participant-ref")
    e1 = make_reference_edge(
        root_e.locator, p1_e.locator, reference_contract=contract, edge_role="PARTICIPANT",
        participant_role="SOURCE_SIDE", declared_cardinality="2..n", multiplicity_key="0",
        order_significant=True, semantic_ordinal=1,
    )
    e2 = make_reference_edge(
        root_e.locator, p2_e.locator, reference_contract=contract, edge_role="PARTICIPANT",
        participant_role="RECEIVER_SIDE", declared_cardinality="2..n", multiplicity_key="0",
        order_significant=True, semantic_ordinal=2,
    )
    with pytest.raises(ClosureIntegrityError, match="partial n-ary"):
        build_v558_repository_bundle(publication, (root_e, p1_e, p2_e), reference_edges=(e1,))
    repo = build_v558_repository_bundle(publication, (root_e, p1_e, p2_e), reference_edges=(e1, e2))
    participant_edges = sorted(
        (e for e in repo.reference_edges if e.edge_role == "PARTICIPANT"),
        key=lambda e: e.semantic_ordinal,
    )
    assert [(e.participant_role, e.semantic_ordinal, e.multiplicity_key, e.declared_cardinality) for e in participant_edges] == [
        ("SOURCE_SIDE", 1, "0", "2..n"), ("RECEIVER_SIDE", 2, "0", "2..n")
    ]


def test_standalone_closure_requires_positive_and_negative_dependencies_and_exact_edges():
    positive = _obj("positive-dep", semantic_class="AUTHORITY")
    negative = _obj("negative-dep", semantic_class="TEMPORAL_LIMIT", state="NEGATIVE_AUTHORITY")
    root = _obj("closure-root", required=(positive.ref,), negative=(negative.ref,))
    root_e = _entry(root, "closure-root")
    pos_e = _entry(positive, "positive-dep")
    neg_e = _entry(negative, "negative-dep")
    publication = build_v557_publication_bundle((V557PublicationEntry(root, root_e.governance),))
    contract = _authority("closure")
    pos_edge = make_reference_edge(root_e.locator, pos_e.locator, reference_contract=contract, edge_role="AUTHORITY")
    neg_edge = make_reference_edge(root_e.locator, neg_e.locator, reference_contract=contract, edge_role="NEGATIVE_LIMIT")
    with pytest.raises(ClosureIntegrityError, match="positive/negative dependency lacks"):
        build_v558_repository_bundle(publication, (root_e, pos_e, neg_e), reference_edges=(pos_edge,))
    repo = build_v558_repository_bundle(publication, (root_e, pos_e, neg_e), reference_edges=(pos_edge, neg_edge))
    assert len(repo.reference_edges) == 2


def test_exact_external_cas_resolution_and_hash_failure_are_integrity_not_semantic_missing():
    leaf_payload = {"leaf": "immutable", "negative_state": "VALID_EMPTY"}
    leaf_hash = semantic_hash(leaf_payload)
    leaf = make_external_stub(
        producer_family="V554", semantic_class="F2", object_id="urn:test:external:leaf",
        content_hash=leaf_hash, schema_id="TEST_F2", schema_version="1.0.0",
        typed_state="VALID_EMPTY", producer_allowed_uses=("REVIEW",), source_stage="TEST-EXTERNAL",
    )
    root = _obj("external-root", required=(leaf.ref,))
    root_e = _entry(root, "external-root")
    leaf_g = _gov(leaf)
    leaf_l = _loc(leaf, leaf_g, "external-leaf", storage=f"cas://sha256/{leaf_hash}")
    leaf_e = RepositoryEntry(leaf, leaf_g, leaf_l)
    publication = build_v557_publication_bundle((V557PublicationEntry(root, root_e.governance),))
    edge = make_reference_edge(root_e.locator, leaf_l, reference_contract=_authority("external-edge"), edge_role="AUTHORITY")
    binding = make_external_resolution_binding(leaf, resolver_authority=_authority("external-resolver"))
    repo = build_v558_repository_bundle(
        publication, (root_e, leaf_e), reference_edges=(edge,), external_bindings=(binding,)
    )
    query = make_context_query((ContextQueryItem(exact_resolution_key(root_e.locator), ("REVIEW",)),))

    missing = resolve_v558(repo, query)
    assert missing.receipt.result_state == "RESOLUTION_INTEGRITY_FAILED"
    assert missing.selection_records[0].decision == "INTEGRITY_FAILURE"
    assert missing.selection_records[0].typed_state == root.typed_state

    bad = resolve_v558(repo, query, external_store={leaf.object_id: {"leaf": "stale"}})
    assert bad.receipt.result_state == "RESOLUTION_INTEGRITY_FAILED"
    assert "hash mismatch" in bad.selection_records[0].reason

    good = resolve_v558(repo, query, external_store={leaf.object_id: leaf_payload})
    assert good.receipt.result_state == "RESOLUTION_COMPLETE"
    assert good.resolved_entries[0].producer_object_ref == root.ref


def test_stale_or_corrupt_locator_fails_before_repository_acceptance():
    obj = _obj("locator")
    gov = _gov(obj)
    loc = _loc(obj, gov, "locator")
    stale = replace(loc, authoritative_object_hash=_h("different-object"))
    with pytest.raises(M4IntegrityError, match="reversibly preserve"):
        RepositoryEntry(obj, gov, stale)


def test_stale_repository_and_query_checksums_fail_closed():
    obj = _obj("checksums")
    entry = _entry(obj, "checksums")
    publication, repo = _repo_for_roots((entry,))
    query = make_context_query((ContextQueryItem(exact_resolution_key(entry.locator), ("REVIEW",)),))

    stale_repo = replace(repo, repository_hash=_h("stale-repository"))
    with pytest.raises(ClosureIntegrityError, match="repository bundle checksum"):
        resolve_v558(stale_repo, query)

    stale_query = replace(query, query_hash=_h("stale-query"))
    with pytest.raises(M4IntegrityError, match="ContextQuery identity/hash"):
        resolve_v558(repo, stale_query)


def test_exact_index_key_has_no_fuzzy_latest_or_missing_key_repair():
    obj = _obj("index")
    entry = _entry(obj, "index")
    publication, repo = _repo_for_roots((entry,))
    with pytest.raises(M4IntegrityError):
        ContextQueryItem("latest", ("REVIEW",))
    missing_key = _h("not-present")
    query = make_context_query((ContextQueryItem(missing_key, ("REVIEW",)),))
    result = resolve_v558(repo, query)
    assert result.receipt.result_state == "RESOLUTION_MISSING_REQUIRED_AUTHORITY"
    assert result.selection_records[0].decision == "UNRESOLVED_EXACT_KEY"
    assert result.resolved_entries == ()


def test_same_provenance_or_colocation_never_creates_source_composition_or_v556_relation():
    one = _obj("source-one", family="V555", semantic_class=V555_SEMANTIC_FAMILY)
    two = _obj("source-two", family="V555", semantic_class=V555_SEMANTIC_FAMILY)
    shared_provenance = "audit://shared-source/COLOCATED"
    e1 = _entry(one, "source-one", provenance=shared_provenance)
    e2 = _entry(two, "source-two", provenance=shared_provenance)
    publication, repo = _repo_for_roots((e1, e2))
    query = make_context_query((
        ContextQueryItem(exact_resolution_key(e1.locator), ("REVIEW",)),
        ContextQueryItem(exact_resolution_key(e2.locator), ("REVIEW",)),
    ))
    result = resolve_v558(repo, query)
    assert result.receipt.result_state == "RESOLUTION_COMPLETE"
    assert {r.canonical_producer_family for r in result.resolved_entries} == {"V555"}
    assert all(e.obj.producer_family != "V556" for e in repo.entries)
    assert all(e.obj.payload.get("source_composition_authority") is None for e in repo.entries if e.obj.payload and "source_composition_authority" in e.obj.payload)


@pytest.mark.parametrize("semantic_class", [
    "ActorComparatorReceipt",
    "V3EmpiricalPossibilityInput",
    "PSEPF",
    "V2_PERSONA",
    "RenderedExpression_or_Persona",
])
def test_actor_v3_v2_and_render_objects_are_rejected_from_structural_repository(semantic_class):
    bad = _obj("forbidden", semantic_class=semantic_class)
    gov = _gov(bad)
    with pytest.raises(ReferenceClassError):
        build_v557_publication_bundle((V557PublicationEntry(bad, gov),))


def test_forbidden_reverse_lane_dependency_is_rejected_even_when_root_is_lawful():
    root = _obj("lawful-root")
    bad = _obj("bad-dependency", semantic_class="V3EmpiricalPossibilityInput")
    root_e = _entry(root, "lawful-root")
    bad_e = _entry(bad, "bad-dependency")
    publication = build_v557_publication_bundle((V557PublicationEntry(root, root_e.governance),))
    with pytest.raises(ReferenceClassError):
        build_v558_repository_bundle(publication, (root_e, bad_e))


def test_audit_only_receipts_cannot_be_semantic_publication_roots():
    assert "ReplayReceipt" in AUDIT_ONLY_CLASSES
    audit = _obj("audit", semantic_class="ReplayReceipt")
    with pytest.raises(ReferenceClassError):
        build_v557_publication_bundle((V557PublicationEntry(audit, _gov(audit)),))


def test_dependency_permission_is_checked_itemwise_and_root_permission_does_not_inherit():
    dep = _obj("dep-review-only", uses=("REVIEW",))
    root = _obj("root-context", uses=("REVIEW", "CONTEXT"), required=(dep.ref,))
    root_e = _entry(root, "root-context", uses=("REVIEW", "CONTEXT"), state=V557DecisionState.ALLOW_CONTEXT_ONLY)
    dep_e = _entry(dep, "dep-review-only")
    publication = build_v557_publication_bundle((V557PublicationEntry(root, root_e.governance),))
    edge = make_reference_edge(root_e.locator, dep_e.locator, reference_contract=_authority("permission-edge"), edge_role="AUTHORITY")
    repo = build_v558_repository_bundle(publication, (root_e, dep_e), reference_edges=(edge,))
    query = make_context_query((ContextQueryItem(exact_resolution_key(root_e.locator), ("CONTEXT",)),))
    result = resolve_v558(repo, query)
    assert result.receipt.result_state == "RESOLUTION_DENIED_OR_NOT_APPLICABLE"
    assert result.selection_records[0].decision == "PERMISSION_DENIED"


def test_resolver_policy_is_frozen_and_latest_policy_cannot_be_substituted():
    with pytest.raises(M4IntegrityError):
        ResolverPolicy(policy_version="latest")
