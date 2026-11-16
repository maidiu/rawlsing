import hashlib

import pytest

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553SemanticCollapseError,
)
from rawlsing_next.pre553_source_relations import (
    DEFAULT_RELATION_STATE,
    I03_COMPOSITE_TARGET_USE,
    RELATION_DECISION_MATRIX,
    SourceRelationAuthorizationError,
    SourceRelationIntegrityError,
    SourceRelationResolver,
    guard_backfill,
    guard_estimand_composition,
    guard_i03_authorized_composite_query,
    guard_sample_pooling,
    make_source_universe_relation,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:i07:{kind.lower()}:{tag}", _h(f"i07:{kind}:{tag}"))


U1 = _ref("EmpiricalUniverse@1.0.0", "u1")
U2 = _ref("EmpiricalUniverse@1.0.0", "u2")
U3 = _ref("EmpiricalUniverse@1.0.0", "u3")
SOURCES = (U1, U2)
BASE_SCOPE = {"query_ref": _ref("EmpiricalQuerySpec@1.0.0", "base-query").as_dict()}
BASE_USE = "TEST_COMPOSITE_USE"
BASE_EFFECTIVE = {"release_scope": "2026-R1"}


def _authority(
    tag: str,
    kind: str,
    operation: str,
    *,
    sources=SOURCES,
    operation_scope=BASE_SCOPE,
    target_use=BASE_USE,
    state="ALLOW",
):
    return AuthoritySnapshot(
        typed_state=state,
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"authority-{tag}"),
        authority_id=f"I07-AUTH-{tag}",
        authority_version="1.0.0",
        authority_content_hash=_h(f"authority:{tag}:1.0.0"),
        authority_kind=kind,
        decision_state=state,
        governed_operations=(operation,),
        governed_object_families=("SourceUniverseRelation@1.0.0", "EmpiricalFact@1.0.0"),
        scope_envelope={
            "source_universe_refs": tuple(source.as_dict() for source in sources),
            "target_use_refs": (target_use,),
            "predicate_or_risk_set_refs": (operation_scope,),
        },
        effective_time_or_interval="2026-R1",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"semantics:{tag}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", tag),
    )


def _semantic_material(tag="base"):
    return {
        "left_semantic_ref": _ref("SEMANTIC_ELEMENT", f"{tag}-left"),
        "right_semantic_ref": _ref("SEMANTIC_ELEMENT", f"{tag}-right"),
        "equivalence_scope": {"meaning": "EXACT_TARGET_SEMANTICS", "tag": tag},
        "transformation_authority_refs": (_ref("TRANSFORM_AUTHORITY", tag),),
    }


def _linkage_material(tag="base"):
    return {
        "scoped_respondent_or_event_keys": (
            {"source": U1.as_dict(), "key": f"{tag}-left"},
            {"source": U2.as_dict(), "key": f"{tag}-right"},
        ),
        "linkage_cardinality": "ONE_TO_ONE",
        "linkage_basis": _ref("LINKAGE_BASIS", tag),
        "confidence_or_certainty_state_if_authorized": "EXACT_AUTHORIZED",
    }


def _overlap_material(tag="base"):
    return {
        "sampling_unit_definition": _ref("SAMPLING_UNIT_DEFINITION", tag),
        "covered_risk_set_or_sample_scope": _ref("SAMPLE_SCOPE", tag),
        "overlap_state": "PROVEN_DISJOINT",
        "deduplication_or_partition_rule_ref_or_NONE": _ref("DEDUP_RULE", tag),
    }


def _pooling_material(semantic_ref, overlap_ref, tag="base"):
    return {
        "target_query_or_estimand_ref": _ref("EmpiricalQuerySpec@1.0.0", f"{tag}-target"),
        "risk_set_and_denominator_authority_refs": (_ref("RISK_DENOM_AUTHORITY", tag),),
        "sample_design_compatibility_ref": _ref("SAMPLE_DESIGN_COMPATIBILITY", tag),
        "semantic_equivalence_refs": (semantic_ref,),
        "overlap_nonduplication_ref": overlap_ref,
        "weight_measure_authority_refs": (_ref("WEIGHT_MEASURE_AUTHORITY", tag),),
        "typed_missingness_applicability_rule_ref": _ref("MISSINGNESS_RULE", tag),
        "composition_method_id_version_hash": _ref("COMPOSITION_METHOD", tag),
    }


def _composition_material(semantic_ref, overlap_ref, tag="base"):
    return {
        "component_estimand_refs": (
            _ref("ESTIMAND", f"{tag}-left"),
            _ref("ESTIMAND", f"{tag}-right"),
        ),
        "target_estimand_ref": _ref("ESTIMAND", f"{tag}-target"),
        "measure_and_scale_compatibility_refs": (_ref("MEASURE_COMPATIBILITY", tag),),
        "semantic_equivalence_refs": (semantic_ref,),
        "overlap_treatment_ref": overlap_ref,
        "weight_or_mixture_rule_ref": _ref("MIXTURE_RULE", tag),
        "uncertainty_propagation_rule_ref_or_typed_unquantified_state": _ref(
            "UNCERTAINTY_RULE", tag
        ),
    }


def _backfill_material(semantic_ref, overlap_ref, *, target=U1, donor=U2, tag="base"):
    return {
        "target_source_universe_ref": target,
        "donor_source_universe_ref": donor,
        "target_semantic_ref": _ref("SEMANTIC_ELEMENT", f"{tag}-target"),
        "donor_semantic_ref": _ref("SEMANTIC_ELEMENT", f"{tag}-donor"),
        "eligible_target_missingness_states": ("MISSING", "UNSPECIFIED"),
        "semantic_equivalence_ref": semantic_ref,
        "sample_estimand_design_compatibility_refs": (_ref("DESIGN_COMPATIBILITY", tag),),
        "overlap_nonduplication_ref": overlap_ref,
        "weight_measure_rule_refs": (_ref("WEIGHT_MEASURE_RULE", tag),),
    }


def _relation(
    kind,
    authority,
    operation,
    material,
    *,
    sources=SOURCES,
    operation_scope=BASE_SCOPE,
    target_use=BASE_USE,
    effective_scope=BASE_EFFECTIVE,
    direction="SYMMETRIC",
    decision="AUTHORIZED",
    tag="base",
):
    return make_source_universe_relation(
        relation_kind=kind,
        source_universe_refs=sources,
        authority_snapshot=authority,
        authority_operation=operation,
        operation_scope=operation_scope,
        target_use=target_use,
        effective_scope=effective_scope,
        directionality_or_symmetric=direction,
        operation_authority_material=material,
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"relation-{kind}-{tag}"),
        decision=decision,
    )


def _positive_bundle(*, scope=BASE_SCOPE, use=BASE_USE, effective=BASE_EFFECTIVE, tag="base"):
    sem_op = "I07_SOURCE_SEMANTIC_EQUIVALENCE"
    overlap_op = "I07_OVERLAP_NON_DUPLICATION"
    pool_op = "I07_SAMPLE_POOLING"
    composition_op = "I07_ESTIMAND_COMPOSITION"
    sem_auth = _authority(f"{tag}-sem", "SOURCE_EQUIVALENCE", sem_op,
                          operation_scope=scope, target_use=use)
    overlap_auth = _authority(f"{tag}-overlap", "SOURCE_UNIVERSE_RELATION", overlap_op,
                              operation_scope=scope, target_use=use)
    pool_auth = _authority(f"{tag}-pool", "SOURCE_COMPOSITION_POOLING", pool_op,
                           operation_scope=scope, target_use=use)
    composition_auth = _authority(
        f"{tag}-composition", "SOURCE_COMPOSITION_POOLING", composition_op,
        operation_scope=scope, target_use=use,
    )
    sem = _relation(
        "SOURCE_SEMANTIC_EQUIVALENCE", sem_auth, sem_op, _semantic_material(tag),
        operation_scope=scope, target_use=use, effective_scope=effective, tag=tag,
    )
    overlap = _relation(
        "OVERLAP_NON_DUPLICATION", overlap_auth, overlap_op, _overlap_material(tag),
        operation_scope=scope, target_use=use, effective_scope=effective, tag=tag,
    )
    pool = _relation(
        "SAMPLE_POOLING", pool_auth, pool_op, _pooling_material(sem.ref, overlap.ref, tag),
        operation_scope=scope, target_use=use, effective_scope=effective, tag=tag,
    )
    composition = _relation(
        "ESTIMAND_COMPOSITION", composition_auth, composition_op,
        _composition_material(sem.ref, overlap.ref, tag),
        operation_scope=scope, target_use=use, effective_scope=effective, tag=tag,
    )
    authorities = (sem_auth, overlap_auth, pool_auth, composition_auth)
    relations = (sem, overlap, pool, composition)
    return {
        "sem_op": sem_op,
        "overlap_op": overlap_op,
        "pool_op": pool_op,
        "composition_op": composition_op,
        "sem_auth": sem_auth,
        "overlap_auth": overlap_auth,
        "pool_auth": pool_auth,
        "composition_auth": composition_auth,
        "sem": sem,
        "overlap": overlap,
        "pool": pool,
        "composition": composition,
        "authorities": authorities,
        "relations": relations,
        "resolver": SourceRelationResolver(
            relations=relations, authority_registry=AuthorityRegistry(authorities)
        ),
    }


def test_relation_decision_matrix_contains_all_eight_noncollapsed_domains():
    assert set(RELATION_DECISION_MATRIX) == {
        "SOURCE_SEMANTIC_EQUIVALENCE",
        "RESPONDENT_LINKAGE",
        "OVERLAP_NON_DUPLICATION",
        "SAMPLE_POOLING",
        "ESTIMAND_COMPOSITION",
        "BACKFILL",
        "PROVENANCE_ORIGIN",
        "HARMONIZATION_ALIAS",
    }
    assert RELATION_DECISION_MATRIX["SOURCE_SEMANTIC_EQUIVALENCE"]["positive_authority_kind"] == "SOURCE_EQUIVALENCE"
    assert RELATION_DECISION_MATRIX["RESPONDENT_LINKAGE"]["positive_authority_kind"] == "SOURCE_RESPONDENT_LINKAGE"
    assert RELATION_DECISION_MATRIX["SAMPLE_POOLING"]["positive_authority_kind"] == "SOURCE_COMPOSITION_POOLING"
    assert RELATION_DECISION_MATRIX["BACKFILL"]["positive_authority_kind"] == "SOURCE_BACKFILL"


def test_no_relation_and_shared_labels_or_ids_remain_distinct_by_default():
    resolver = SourceRelationResolver(relations=(), authority_registry=AuthorityRegistry(()))
    decision = resolver.decide(
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
        source_universe_refs=SOURCES,
        operation_scope={"shared_label": "SAME", "shared_id": "123"},
        target_use=BASE_USE,
        effective_scope=BASE_EFFECTIVE,
    )
    assert decision.state == DEFAULT_RELATION_STATE
    assert not decision.authorized
    assert decision.relation_ref is None


def test_provenance_and_alias_can_never_be_positive_relation_authority():
    provenance_auth = _authority(
        "provenance", "SOURCE_UNIVERSE_RELATION", "I07_PROVENANCE",
    )
    alias_auth = _authority(
        "alias", "SOURCE_UNIVERSE_RELATION", "I07_ALIAS",
    )
    with pytest.raises(Pre553SemanticCollapseError):
        _relation(
            "PROVENANCE_ORIGIN", provenance_auth, "I07_PROVENANCE",
            {"provenance_refs": (_ref("PROVENANCE", "shared"),)}, tag="prov",
        )
    with pytest.raises(Pre553SemanticCollapseError):
        _relation(
            "HARMONIZATION_ALIAS", alias_auth, "I07_ALIAS",
            {"alias_refs": (_ref("ALIAS", "shared"),)}, tag="alias",
        )


def test_semantic_equivalence_is_exact_scope_use_and_source_bounded():
    bundle = _positive_bundle()
    resolver = bundle["resolver"]
    ok = resolver.require(
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
        source_universe_refs=SOURCES,
        operation_scope=BASE_SCOPE,
        target_use=BASE_USE,
        effective_scope=BASE_EFFECTIVE,
        relation_ref=bundle["sem"].ref,
        expected_authority_operation=bundle["sem_op"],
    )
    assert ok.authorized
    assert resolver.decide(
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
        source_universe_refs=SOURCES,
        operation_scope={"query_ref": _ref("EmpiricalQuerySpec@1.0.0", "other").as_dict()},
        target_use=BASE_USE,
        effective_scope=BASE_EFFECTIVE,
        relation_ref=bundle["sem"].ref,
    ).state == DEFAULT_RELATION_STATE
    assert resolver.decide(
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
        source_universe_refs=(U1, U3),
        operation_scope=BASE_SCOPE,
        target_use=BASE_USE,
        effective_scope=BASE_EFFECTIVE,
        relation_ref=bundle["sem"].ref,
    ).state == DEFAULT_RELATION_STATE


def test_equivalence_does_not_grant_respondent_linkage():
    bundle = _positive_bundle()
    resolver = SourceRelationResolver(
        relations=(bundle["sem"],), authority_registry=AuthorityRegistry((bundle["sem_auth"],))
    )
    assert resolver.require(
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE", source_universe_refs=SOURCES,
        operation_scope=BASE_SCOPE, target_use=BASE_USE, effective_scope=BASE_EFFECTIVE,
        relation_ref=bundle["sem"].ref, expected_authority_operation=bundle["sem_op"],
    ).authorized
    linkage = resolver.decide(
        relation_kind="RESPONDENT_LINKAGE", source_universe_refs=SOURCES,
        operation_scope=BASE_SCOPE, target_use=BASE_USE, effective_scope=BASE_EFFECTIVE,
    )
    assert linkage.state == DEFAULT_RELATION_STATE
    assert not linkage.authorized


def test_respondent_linkage_does_not_grant_pooling():
    op = "I07_RESPONDENT_LINKAGE"
    auth = _authority("link", "SOURCE_RESPONDENT_LINKAGE", op)
    link = _relation("RESPONDENT_LINKAGE", auth, op, _linkage_material(), tag="link")
    resolver = SourceRelationResolver(relations=(link,), authority_registry=AuthorityRegistry((auth,)))
    assert resolver.require(
        relation_kind="RESPONDENT_LINKAGE", source_universe_refs=SOURCES,
        operation_scope=BASE_SCOPE, target_use=BASE_USE, effective_scope=BASE_EFFECTIVE,
        relation_ref=link.ref, expected_authority_operation=op,
    ).authorized
    pooling = resolver.decide(
        relation_kind="SAMPLE_POOLING", source_universe_refs=SOURCES,
        operation_scope=BASE_SCOPE, target_use=BASE_USE, effective_scope=BASE_EFFECTIVE,
    )
    assert pooling.state == DEFAULT_RELATION_STATE


def test_nonduplication_does_not_grant_estimand_composition():
    bundle = _positive_bundle()
    resolver = SourceRelationResolver(
        relations=(bundle["overlap"],),
        authority_registry=AuthorityRegistry((bundle["overlap_auth"],)),
    )
    assert resolver.require(
        relation_kind="OVERLAP_NON_DUPLICATION", source_universe_refs=SOURCES,
        operation_scope=BASE_SCOPE, target_use=BASE_USE, effective_scope=BASE_EFFECTIVE,
        relation_ref=bundle["overlap"].ref,
        expected_authority_operation=bundle["overlap_op"],
    ).authorized
    decision = resolver.decide(
        relation_kind="ESTIMAND_COMPOSITION", source_universe_refs=SOURCES,
        operation_scope=BASE_SCOPE, target_use=BASE_USE, effective_scope=BASE_EFFECTIVE,
    )
    assert decision.state == DEFAULT_RELATION_STATE


def test_pooling_does_not_grant_backfill():
    bundle = _positive_bundle()
    resolver = SourceRelationResolver(
        relations=(bundle["sem"], bundle["overlap"], bundle["pool"]),
        authority_registry=AuthorityRegistry(
            (bundle["sem_auth"], bundle["overlap_auth"], bundle["pool_auth"])
        ),
    )
    assert guard_sample_pooling(
        resolver=resolver, source_universe_refs=SOURCES,
        operation_scope=BASE_SCOPE, target_use=BASE_USE, effective_scope=BASE_EFFECTIVE,
        semantic_equivalence_ref=bundle["sem"].ref,
        overlap_nonduplication_ref=bundle["overlap"].ref,
        pooling_ref=bundle["pool"].ref,
        pooling_authority_operation=bundle["pool_op"],
        semantic_equivalence_authority_operation=bundle["sem_op"],
        overlap_authority_operation=bundle["overlap_op"],
    ).operation_kind == "SAMPLE_POOLING"
    assert resolver.decide(
        relation_kind="BACKFILL", source_universe_refs=SOURCES,
        operation_scope=BASE_SCOPE, target_use=BASE_USE, effective_scope=BASE_EFFECTIVE,
        directionality_or_symmetric={
            "donor_source_universe_ref": U2.as_dict(),
            "target_source_universe_ref": U1.as_dict(),
        },
    ).state == DEFAULT_RELATION_STATE


def test_sample_pooling_requires_semantic_equivalence_nonduplication_and_own_authority():
    bundle = _positive_bundle()
    resolver = bundle["resolver"]
    receipt = guard_sample_pooling(
        resolver=resolver, source_universe_refs=SOURCES,
        operation_scope=BASE_SCOPE, target_use=BASE_USE, effective_scope=BASE_EFFECTIVE,
        semantic_equivalence_ref=bundle["sem"].ref,
        overlap_nonduplication_ref=bundle["overlap"].ref,
        pooling_ref=bundle["pool"].ref,
        pooling_authority_operation=bundle["pool_op"],
        semantic_equivalence_authority_operation=bundle["sem_op"],
        overlap_authority_operation=bundle["overlap_op"],
    )
    assert receipt.operation_kind == "SAMPLE_POOLING"
    assert set(receipt.relation_refs) == {bundle["sem"].ref, bundle["overlap"].ref, bundle["pool"].ref}

    no_semantic = SourceRelationResolver(
        relations=(bundle["overlap"], bundle["pool"]),
        authority_registry=AuthorityRegistry((bundle["overlap_auth"], bundle["pool_auth"])),
    )
    with pytest.raises(SourceRelationIntegrityError):
        guard_sample_pooling(
            resolver=no_semantic, source_universe_refs=SOURCES,
            operation_scope=BASE_SCOPE, target_use=BASE_USE, effective_scope=BASE_EFFECTIVE,
            semantic_equivalence_ref=bundle["sem"].ref,
            overlap_nonduplication_ref=bundle["overlap"].ref,
            pooling_ref=bundle["pool"].ref,
            pooling_authority_operation=bundle["pool_op"],
            semantic_equivalence_authority_operation=bundle["sem_op"],
            overlap_authority_operation=bundle["overlap_op"],
        )


def test_pooling_must_bind_the_exact_semantic_and_overlap_receipts():
    bundle = _positive_bundle(tag="binding")
    wrong_sem = _ref("SourceUniverseRelation@1.0.0", "wrong-semantic")
    bad_pool = _relation(
        "SAMPLE_POOLING", bundle["pool_auth"], bundle["pool_op"],
        _pooling_material(wrong_sem, bundle["overlap"].ref, "bad-pool"),
        tag="bad-pool",
    )
    resolver = SourceRelationResolver(
        relations=(bundle["sem"], bundle["overlap"], bad_pool),
        authority_registry=AuthorityRegistry(
            (bundle["sem_auth"], bundle["overlap_auth"], bundle["pool_auth"])
        ),
    )
    with pytest.raises(SourceRelationAuthorizationError, match="semantic-equivalence"):
        guard_sample_pooling(
            resolver=resolver, source_universe_refs=SOURCES,
            operation_scope=BASE_SCOPE, target_use=BASE_USE, effective_scope=BASE_EFFECTIVE,
            semantic_equivalence_ref=bundle["sem"].ref,
            overlap_nonduplication_ref=bundle["overlap"].ref,
            pooling_ref=bad_pool.ref,
            pooling_authority_operation=bundle["pool_op"],
            semantic_equivalence_authority_operation=bundle["sem_op"],
            overlap_authority_operation=bundle["overlap_op"],
        )


def test_estimand_composition_requires_its_own_exact_relation_even_when_pooling_exists():
    bundle = _positive_bundle()
    resolver = bundle["resolver"]
    receipt = guard_estimand_composition(
        resolver=resolver, source_universe_refs=SOURCES,
        operation_scope=BASE_SCOPE, target_use=BASE_USE, effective_scope=BASE_EFFECTIVE,
        semantic_equivalence_ref=bundle["sem"].ref,
        overlap_nonduplication_ref=bundle["overlap"].ref,
        estimand_composition_ref=bundle["composition"].ref,
        composition_authority_operation=bundle["composition_op"],
        semantic_equivalence_authority_operation=bundle["sem_op"],
        overlap_authority_operation=bundle["overlap_op"],
    )
    assert receipt.operation_kind == "ESTIMAND_COMPOSITION"

    no_composition = SourceRelationResolver(
        relations=(bundle["sem"], bundle["overlap"], bundle["pool"]),
        authority_registry=AuthorityRegistry(
            (bundle["sem_auth"], bundle["overlap_auth"], bundle["pool_auth"])
        ),
    )
    with pytest.raises(SourceRelationIntegrityError):
        guard_estimand_composition(
            resolver=no_composition, source_universe_refs=SOURCES,
            operation_scope=BASE_SCOPE, target_use=BASE_USE, effective_scope=BASE_EFFECTIVE,
            semantic_equivalence_ref=bundle["sem"].ref,
            overlap_nonduplication_ref=bundle["overlap"].ref,
            estimand_composition_ref=bundle["composition"].ref,
            composition_authority_operation=bundle["composition_op"],
            semantic_equivalence_authority_operation=bundle["sem_op"],
            overlap_authority_operation=bundle["overlap_op"],
        )


def _backfill_bundle(*, target=U1, donor=U2, tag="backfill"):
    sem_op = "I07_SOURCE_SEMANTIC_EQUIVALENCE"
    overlap_op = "I07_OVERLAP_NON_DUPLICATION"
    backfill_op = "I07_DIRECTIONAL_BACKFILL"
    sem_auth = _authority(f"{tag}-sem", "SOURCE_EQUIVALENCE", sem_op)
    overlap_auth = _authority(f"{tag}-overlap", "SOURCE_UNIVERSE_RELATION", overlap_op)
    backfill_auth = _authority(f"{tag}-backfill", "SOURCE_BACKFILL", backfill_op)
    sem = _relation(
        "SOURCE_SEMANTIC_EQUIVALENCE", sem_auth, sem_op, _semantic_material(tag), tag=tag,
    )
    overlap = _relation(
        "OVERLAP_NON_DUPLICATION", overlap_auth, overlap_op, _overlap_material(tag), tag=tag,
    )
    direction = {
        "donor_source_universe_ref": donor.as_dict(),
        "target_source_universe_ref": target.as_dict(),
    }
    backfill = _relation(
        "BACKFILL", backfill_auth, backfill_op,
        _backfill_material(sem.ref, overlap.ref, target=target, donor=donor, tag=tag),
        direction=direction, tag=tag,
    )
    resolver = SourceRelationResolver(
        relations=(sem, overlap, backfill),
        authority_registry=AuthorityRegistry((sem_auth, overlap_auth, backfill_auth)),
    )
    return {
        "sem": sem, "overlap": overlap, "backfill": backfill,
        "sem_op": sem_op, "overlap_op": overlap_op, "backfill_op": backfill_op,
        "resolver": resolver,
    }


def test_backfill_is_directional_and_only_explicit_missingness_is_eligible():
    bundle = _backfill_bundle()
    receipt = guard_backfill(
        resolver=bundle["resolver"], target_source_universe_ref=U1,
        donor_source_universe_ref=U2, operation_scope=BASE_SCOPE, target_use=BASE_USE,
        effective_scope=BASE_EFFECTIVE, target_missingness_state="MISSING",
        semantic_equivalence_ref=bundle["sem"].ref,
        overlap_nonduplication_ref=bundle["overlap"].ref,
        backfill_ref=bundle["backfill"].ref,
        backfill_authority_operation=bundle["backfill_op"],
        semantic_equivalence_authority_operation=bundle["sem_op"],
        overlap_authority_operation=bundle["overlap_op"],
    )
    assert receipt.operation_kind == "BACKFILL"
    with pytest.raises(SourceRelationAuthorizationError):
        guard_backfill(
            resolver=bundle["resolver"], target_source_universe_ref=U2,
            donor_source_universe_ref=U1, operation_scope=BASE_SCOPE, target_use=BASE_USE,
            effective_scope=BASE_EFFECTIVE, target_missingness_state="MISSING",
            semantic_equivalence_ref=bundle["sem"].ref,
            overlap_nonduplication_ref=bundle["overlap"].ref,
            backfill_ref=bundle["backfill"].ref,
            backfill_authority_operation=bundle["backfill_op"],
            semantic_equivalence_authority_operation=bundle["sem_op"],
            overlap_authority_operation=bundle["overlap_op"],
        )
    with pytest.raises(SourceRelationAuthorizationError, match="not named"):
        guard_backfill(
            resolver=bundle["resolver"], target_source_universe_ref=U1,
            donor_source_universe_ref=U2, operation_scope=BASE_SCOPE, target_use=BASE_USE,
            effective_scope=BASE_EFFECTIVE, target_missingness_state="UNKNOWN_BUT_NOT_NAMED",
            semantic_equivalence_ref=bundle["sem"].ref,
            overlap_nonduplication_ref=bundle["overlap"].ref,
            backfill_ref=bundle["backfill"].ref,
            backfill_authority_operation=bundle["backfill_op"],
            semantic_equivalence_authority_operation=bundle["sem_op"],
            overlap_authority_operation=bundle["overlap_op"],
        )


@pytest.mark.parametrize(
    "state",
    ["OBSERVED_ZERO", "ZERO_SUPPORT", "NONCOMPARABLE", "NOT_APPLICABLE", "SOURCE_NOT_APPLICABLE"],
)
def test_backfill_never_launders_zero_or_negative_states(state):
    bundle = _backfill_bundle(tag=f"negative-{state}")
    with pytest.raises(SourceRelationAuthorizationError):
        guard_backfill(
            resolver=bundle["resolver"], target_source_universe_ref=U1,
            donor_source_universe_ref=U2, operation_scope=BASE_SCOPE, target_use=BASE_USE,
            effective_scope=BASE_EFFECTIVE, target_missingness_state=state,
            semantic_equivalence_ref=bundle["sem"].ref,
            overlap_nonduplication_ref=bundle["overlap"].ref,
            backfill_ref=bundle["backfill"].ref,
            backfill_authority_operation=bundle["backfill_op"],
            semantic_equivalence_authority_operation=bundle["sem_op"],
            overlap_authority_operation=bundle["overlap_op"],
        )


def test_conflicting_positive_and_denied_relation_receipts_fail_closed():
    op = "I07_SOURCE_SEMANTIC_EQUIVALENCE"
    allow_auth = _authority("conflict-allow", "SOURCE_EQUIVALENCE", op)
    deny_auth = _authority("conflict-deny", "SOURCE_EQUIVALENCE", op, state="DENY")
    positive = _relation(
        "SOURCE_SEMANTIC_EQUIVALENCE", allow_auth, op, _semantic_material("conflict"),
        tag="conflict-allow",
    )
    denied = _relation(
        "SOURCE_SEMANTIC_EQUIVALENCE", deny_auth, op, _semantic_material("conflict"),
        decision="DENIED", tag="conflict-deny",
    )
    resolver = SourceRelationResolver(
        relations=(positive, denied), authority_registry=AuthorityRegistry((allow_auth, deny_auth))
    )
    decision = resolver.decide(
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE", source_universe_refs=SOURCES,
        operation_scope=BASE_SCOPE, target_use=BASE_USE, effective_scope=BASE_EFFECTIVE,
    )
    assert decision.state == "CONFLICTING_AUTHORITY"
    assert not decision.authorized


def test_relation_authority_must_be_available_by_exact_historical_ref():
    op = "I07_SOURCE_SEMANTIC_EQUIVALENCE"
    auth = _authority("historical", "SOURCE_EQUIVALENCE", op)
    relation = _relation(
        "SOURCE_SEMANTIC_EQUIVALENCE", auth, op, _semantic_material("historical"),
        tag="historical",
    )
    with pytest.raises(SourceRelationIntegrityError, match="authority snapshot unavailable"):
        SourceRelationResolver(relations=(relation,), authority_registry=AuthorityRegistry(()))


def test_same_exact_relation_inputs_replay_identically_independent_of_registration_order():
    bundle = _positive_bundle(tag="replay")
    registry = AuthorityRegistry(bundle["authorities"])
    left = SourceRelationResolver(relations=bundle["relations"], authority_registry=registry)
    right = SourceRelationResolver(relations=tuple(reversed(bundle["relations"])), authority_registry=registry)
    kwargs = dict(
        relation_kind="SAMPLE_POOLING", source_universe_refs=SOURCES,
        operation_scope=BASE_SCOPE, target_use=BASE_USE, effective_scope=BASE_EFFECTIVE,
        relation_ref=bundle["pool"].ref, expected_authority_operation=bundle["pool_op"],
    )
    assert left.require(**kwargs) == right.require(**kwargs)
    assert left.require(**kwargs).replay_identity == right.require(**kwargs).replay_identity


def _i03_query(*, pool_auth, nondup_auth, composition_auth, tag="i03"):
    target = _ref("QUESTION_NATIVE", f"{tag}-Y")
    predicate = _ref("EmpiricalPredicate@1.0.0", f"{tag}-predicate")
    risk = _ref("RISK_SET", f"{tag}-risk")
    measure = _ref("MEASURE", "RAW")
    response_state = _ref("STATE_SEMANTICS", f"{tag}-response")
    query_authority = AuthorityRef(
        f"I07-QUERY-AUTH-{tag}", "1.0.0", _h(f"query-authority:{tag}")
    )
    return EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(query_authority,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"query-{tag}"),
        target_refs=(target,),
        target_arity_and_topology={
            "arity": 1,
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": ({
                "target_ref": target.as_dict(),
                "topology": "SCALAR_SINGULAR",
                "domain": ("0", "1"),
                "target_domain_replay_ref": _ref("TARGET_DOMAIN", tag).as_dict(),
                "topology_authority_refs": (query_authority.as_dict(),),
                "response_semantic_authority_refs": (query_authority.as_dict(),),
                "included_states": ("SUBSTANTIVE_RESPONSE",),
            },),
        },
        condition_predicate_ref=predicate,
        risk_set_ref=risk,
        empirical_universe_refs=SOURCES,
        scope_refs=(_ref("SCOPE", tag),),
        measure_basis_ref=measure,
        requested_output_grain={
            "source_scope_mode": "AUTHORIZED_COMPOSITE",
            "measure_kind": "RAW",
            "risk_set_type": "WHOLE_QUESTION_RISK_SET",
            "response_state_semantics_ref": response_state.as_dict(),
            "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
            "source_relation_effective_scope": {"release_scope": f"{tag}-R1"},
            "authorized_composite_authority_refs": {
                "pooling": {
                    "authority_ref": pool_auth.authority_ref.as_dict(),
                    "operation": "I03_POOL_EXACT",
                },
                "nonduplication": {
                    "authority_ref": nondup_auth.authority_ref.as_dict(),
                    "operation": "I03_NONDUP_EXACT",
                },
                "estimand_composition": {
                    "authority_ref": composition_auth.authority_ref.as_dict(),
                    "operation": "I03_ESTIMAND_EXACT",
                },
            },
        },
        query_authority_refs=(query_authority,),
    )


def _i03_scope(query):
    return {
        "i03_query_ref": query.ref.as_dict(),
        "condition_predicate_ref": query.condition_predicate_ref,
        "risk_set_ref": query.risk_set_ref,
        "measure_basis_ref": query.measure_basis_ref,
        "target_refs": query.target_refs,
    }


def _i03_relation_bundle(tag="i03"):
    # The query must be constructed before relation authority scope because I07
    # binds the exact query identity as operation scope.  I03's own three-role
    # authority refs are themselves independent of the relation receipts.
    placeholder_scope = {"placeholder": tag}
    placeholder_use = I03_COMPOSITE_TARGET_USE
    pool_stub = _authority(
        f"{tag}-pool", "SOURCE_COMPOSITION_POOLING", "I03_POOL_EXACT",
        operation_scope=placeholder_scope, target_use=placeholder_use,
    )
    nondup_stub = _authority(
        f"{tag}-nondup", "SOURCE_UNIVERSE_RELATION", "I03_NONDUP_EXACT",
        operation_scope=placeholder_scope, target_use=placeholder_use,
    )
    composition_stub = _authority(
        f"{tag}-composition", "SOURCE_COMPOSITION_POOLING", "I03_ESTIMAND_EXACT",
        operation_scope=placeholder_scope, target_use=placeholder_use,
    )
    query = _i03_query(
        pool_auth=pool_stub, nondup_auth=nondup_stub,
        composition_auth=composition_stub, tag=tag,
    )
    scope = _i03_scope(query)
    effective = query.requested_output_grain["source_relation_effective_scope"]
    # Recreate the snapshots with identical exact refs but correct scope.  The
    # AuthoritySnapshot public object may change; its authority_ref stays exact
    # because the authority content hash is the externally frozen authority ID.
    pool_auth = _authority(
        f"{tag}-pool", "SOURCE_COMPOSITION_POOLING", "I03_POOL_EXACT",
        operation_scope=scope, target_use=placeholder_use,
    )
    nondup_auth = _authority(
        f"{tag}-nondup", "SOURCE_UNIVERSE_RELATION", "I03_NONDUP_EXACT",
        operation_scope=scope, target_use=placeholder_use,
    )
    composition_auth = _authority(
        f"{tag}-composition", "SOURCE_COMPOSITION_POOLING", "I03_ESTIMAND_EXACT",
        operation_scope=scope, target_use=placeholder_use,
    )
    assert pool_auth.authority_ref == pool_stub.authority_ref
    assert nondup_auth.authority_ref == nondup_stub.authority_ref
    assert composition_auth.authority_ref == composition_stub.authority_ref
    sem_auth = _authority(
        f"{tag}-sem", "SOURCE_EQUIVALENCE", "I07_SOURCE_SEMANTIC_EQUIVALENCE",
        operation_scope=scope, target_use=placeholder_use,
    )
    sem = _relation(
        "SOURCE_SEMANTIC_EQUIVALENCE", sem_auth, "I07_SOURCE_SEMANTIC_EQUIVALENCE",
        _semantic_material(tag), operation_scope=scope, target_use=placeholder_use,
        effective_scope=effective, tag=tag,
    )
    overlap = _relation(
        "OVERLAP_NON_DUPLICATION", nondup_auth, "I03_NONDUP_EXACT",
        _overlap_material(tag), operation_scope=scope, target_use=placeholder_use,
        effective_scope=effective, tag=tag,
    )
    pool = _relation(
        "SAMPLE_POOLING", pool_auth, "I03_POOL_EXACT",
        _pooling_material(sem.ref, overlap.ref, tag), operation_scope=scope,
        target_use=placeholder_use, effective_scope=effective, tag=tag,
    )
    composition = _relation(
        "ESTIMAND_COMPOSITION", composition_auth, "I03_ESTIMAND_EXACT",
        _composition_material(sem.ref, overlap.ref, tag), operation_scope=scope,
        target_use=placeholder_use, effective_scope=effective, tag=tag,
    )
    authorities = (sem_auth, nondup_auth, pool_auth, composition_auth)
    relations = (sem, overlap, pool, composition)
    resolver = SourceRelationResolver(
        relations=relations, authority_registry=AuthorityRegistry(authorities)
    )
    return {
        "query": query,
        "scope": scope,
        "effective": effective,
        "sem": sem,
        "overlap": overlap,
        "pool": pool,
        "composition": composition,
        "resolver": resolver,
        "relation_refs": {
            "SOURCE_SEMANTIC_EQUIVALENCE": sem.ref,
            "OVERLAP_NON_DUPLICATION": overlap.ref,
            "SAMPLE_POOLING": pool.ref,
            "ESTIMAND_COMPOSITION": composition.ref,
        },
    }


def test_i03_authorized_composite_guard_binds_exact_p07_relations_without_changing_i03_bundle():
    bundle = _i03_relation_bundle()
    receipt = guard_i03_authorized_composite_query(
        query=bundle["query"], resolver=bundle["resolver"],
        relation_refs=bundle["relation_refs"],
    )
    assert receipt.query_ref == bundle["query"].ref
    assert receipt.semantic_equivalence_ref == bundle["sem"].ref
    assert receipt.overlap_nonduplication_ref == bundle["overlap"].ref
    assert receipt.pooling_ref == bundle["pool"].ref
    assert receipt.estimand_composition_ref == bundle["composition"].ref
    i03_authorities = bundle["query"].requested_output_grain["authorized_composite_authority_refs"]
    assert {ref.key for ref in receipt.i03_authority_refs} == {
        AuthorityRef(**i03_authorities[role]["authority_ref"]).key
        for role in ("pooling", "nonduplication", "estimand_composition")
    }


def test_i03_guard_rejects_missing_relation_kind_even_when_i03_authority_bundle_is_present():
    bundle = _i03_relation_bundle(tag="missing-relation")
    refs = dict(bundle["relation_refs"])
    refs.pop("SOURCE_SEMANTIC_EQUIVALENCE")
    with pytest.raises(SourceRelationAuthorizationError, match="requires exact"):
        guard_i03_authorized_composite_query(
            query=bundle["query"], resolver=bundle["resolver"], relation_refs=refs,
        )


def test_i03_guard_rejects_relation_authority_that_does_not_equal_exact_i03_role_authority():
    bundle = _i03_relation_bundle(tag="authority-mismatch")
    query = bundle["query"]
    grain = dict(query.requested_output_grain)
    roles = {key: dict(value) for key, value in grain["authorized_composite_authority_refs"].items()}
    alien = AuthorityRef("I07-ALIEN-POOL", "1.0.0", _h("alien-pool"))
    roles["pooling"] = {"authority_ref": alien.as_dict(), "operation": "I03_POOL_EXACT"}
    grain["authorized_composite_authority_refs"] = roles
    fields = dict(query.semantic_fields)
    fields["requested_output_grain"] = grain
    altered = EmpiricalQuerySpec(
        typed_state=query.typed_state,
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=query.dependency_refs,
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "altered-i03-query"),
        **fields,
    )
    with pytest.raises(SourceRelationAuthorizationError):
        guard_i03_authorized_composite_query(
            query=altered, resolver=bundle["resolver"], relation_refs=bundle["relation_refs"],
        )


def test_i03_guard_rejects_alias_or_provenance_substitution_for_semantic_equivalence():
    bundle = _i03_relation_bundle(tag="alias-substitution")
    alias_auth = _authority(
        "alias-descriptive", "SOURCE_UNIVERSE_RELATION", "I07_ALIAS_DESCRIPTIVE",
        operation_scope=bundle["scope"], target_use=I03_COMPOSITE_TARGET_USE,
    )
    alias = _relation(
        "HARMONIZATION_ALIAS", alias_auth, "I07_ALIAS_DESCRIPTIVE",
        {"alias_refs": (_ref("ALIAS", "same-label"),)},
        operation_scope=bundle["scope"], target_use=I03_COMPOSITE_TARGET_USE,
        effective_scope=bundle["effective"], decision="NOT_APPLICABLE",
        tag="alias-descriptive",
    )
    resolver = SourceRelationResolver(
        relations=(*bundle["resolver"]._by_ref.values(), alias),
        authority_registry=AuthorityRegistry((
            *[bundle["resolver"]._registry.resolve_exact(ref).snapshot for ref in receipt_authority_refs(bundle)],
            alias_auth,
        )),
    )
    refs = dict(bundle["relation_refs"])
    refs["SOURCE_SEMANTIC_EQUIVALENCE"] = alias.ref
    with pytest.raises(SourceRelationAuthorizationError):
        guard_i03_authorized_composite_query(
            query=bundle["query"], resolver=resolver, relation_refs=refs,
        )


def receipt_authority_refs(bundle):
    return tuple(
        relation.authority_snapshot_refs[0]
        for relation in (bundle["sem"], bundle["overlap"], bundle["pool"], bundle["composition"])
    )
