from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.prev3_objective_position_materializer import (
    ObjectivePositionInput,
    PositionMaterializerError,
    PositionResultState,
    materialize_objective_position,
    typed_nonpositive_result,
)
from rawlsing_next.m4_v557_v558_publication_repository import (
    M4IntegrityError,
    ContextQueryItem,
    ReferenceClassError,
    RepositoryEntry,
    V557PublicationEntry,
    build_v557_publication_bundle,
    exact_resolution_key,
    make_context_query,
)
from rawlsing_next.prev3_objective_position_v557_v558_publication import (
    J04_AUTHORITY_REF,
    M4_CONTEXT_USE,
    PROVING_FACT_HASH,
    PROVING_FACT_ID,
    SOURCE_DOMAIN_USE,
    ObjectivePositionPublicationError,
    make_bound_objective_position_context_query,
    publish_objective_position_fact,
    replay_objective_position_publication,
    require_bound_objective_position_context_query,
    validate_objective_position_publication_carrier,
)

SUITE_ID = "J04_PREV3_OBJECTIVE_POSITION_FACT_V557_PUBLICATION_HOSTILE_QUALIFICATION_R1"


def _r(kind: str, object_id: str, content_hash: str) -> ExactRef:
    return ExactRef(kind, object_id, content_hash)


def _a(authority_id: str, version: str, content_hash: str) -> AuthorityRef:
    return AuthorityRef(authority_id, version, content_hash)


def _input() -> ObjectivePositionInput:
    materializer = _r(
        "PREV3_OBJECTIVE_POSITION_MATERIALIZER_IMPLEMENTATION",
        "urn:rawlsing:prev3:objective-position-materializer:sha256:8bba7e866879d856d5b741e3df7410a0861cdb1f01cd37fd3298bc9eb8089503",
        "8bba7e866879d856d5b741e3df7410a0861cdb1f01cd37fd3298bc9eb8089503",
    )
    source_universe = _r(
        "SOURCE_UNIVERSE",
        "urn:rawlsing:source:afrobarometer:r5:sha256:c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651",
        "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651",
    )
    source_release = _r(
        "FFP014_R5_CURRENT_RESPONDENT_CARRIER",
        "urn:rawlsing:field-forge:ffp014:r5-current-respondent-carrier:sha256:6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5",
        "6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5",
    )
    source_claim = _r(
        "FFP014_Q73A_SOURCE_CLAIM",
        "urn:rawlsing:field-forge:ffp014:r5:q73a:ben0002:native-state-1",
        "f42065f6c174dff98f7a163d704c8ae12b029bb331a1f11debf4937c728a963f",
    )
    role_receipt = _r(
        "FIELD_FORGE_CLAIM_BOUNDED_POSITION_ROLE_RECEIPT",
        "urn:rawlsing:field-forge:ffp029:pra:001",
        "63ff1fbc1ad6d819c259be7f850b73976f8d44ebf87fe99ee873f6d70d18fa24",
    )
    negative = _r(
        "PREV3_OBJECTIVE_POSITION_NEGATIVE_CEILING",
        "urn:rawlsing:prev3:objective-position:ffp014-q73a-ben0002:negative-ceiling:r1",
        "a560f910ea0b92201b553c3f17e5515851e50755d7d4347815f3e8a6efabec32",
    )
    valid_time = _r(
        "PREV3_OBJECTIVE_POSITION_VALID_TIME_BASIS",
        "urn:rawlsing:prev3:objective-position:ffp014-q73a-ben0002:r5-observation-grain",
        "753cc2b5ccbf0a93f61f117cb35cd9c4ee1a4924e22bc7af0bb80c9a615e8e70",
    )
    currentness = _r(
        "PREV3_OBJECTIVE_POSITION_CURRENTNESS_RECEIPT",
        "urn:rawlsing:prev3:objective-position:ffp014-q73a-ben0002:current-project-representation-of-r5-observation",
        "1dd635621a2033424d54c09d4c4f973481b52ec265091f7e624df78874a5ad4e",
    )
    admission = _r(
        "FFP014_CURRENT_ADMISSION_RECEIPT",
        "urn:rawlsing:field-forge:ffp014:admission:sha256:1a01cf216a4c70ffe9e9663ea8dd77381b2aecf8bea2d59c5853c234955ca244",
        "1a01cf216a4c70ffe9e9663ea8dd77381b2aecf8bea2d59c5853c234955ca244",
    )
    return ObjectivePositionInput(
        materializer_implementation_ref=materializer,
        position_producer_authority_ref=_a(
            "urn:rawlsing:prev3:authority:objective-position-producer:ffp014-q73a-ben0002:r1",
            "F03@1.0.0",
            "8817ac59bfb76e48cd018a73128bffcf3a94b0e2ad19fd1889a4a54f77d9cca6",
        ),
        position_semantic_authority_ref=_a(
            "urn:rawlsing:field-forge:ffp029:pra:001",
            "FFP029_SECOND_CANARY_PRA_DOCKET_GRAIN@1",
            "63ff1fbc1ad6d819c259be7f850b73976f8d44ebf87fe99ee873f6d70d18fa24",
        ),
        entity_or_actor_ref=_r(
            "FFP014_R5_RESPONDENT",
            "urn:rawlsing:field-forge:ffp014:r5:respondent:sha256:cd60ba8e8879643f15535d9eb704f8bd73fd7a2e058dbe7172b7cb9e7526e729",
            "cd60ba8e8879643f15535d9eb704f8bd73fd7a2e058dbe7172b7cb9e7526e729",
        ),
        objective_position_role_identity_ref=_r(
            "PREV3_OBJECTIVE_POSITION_ROLE_IDENTITY",
            "urn:rawlsing:field-forge:ffp029:pra:001:q73a-active-position",
            "63ff1fbc1ad6d819c259be7f850b73976f8d44ebf87fe99ee873f6d70d18fa24",
        ),
        source_universe_ref=source_universe,
        source_release_ref=source_release,
        source_claim_ref=source_claim,
        source_claim_authority_ref=_a(
            "urn:rawlsing:field-forge:ffp014:r5-q73a-current-admission",
            "FFP014_CURRENT_RESPONDENT_EXECUTION_BINDING_ADMISSION_RECEIPT@1",
            "1a01cf216a4c70ffe9e9663ea8dd77381b2aecf8bea2d59c5853c234955ca244",
        ),
        supporting_evidence_refs=(
            admission,
            _r(
                "FFP014_Q73A_RESPONSE_BINDING",
                "urn:rawlsing:field-forge:ffp014:q73a-response:sha256:ad62093fbc98eb7453a72015cc0fccdee9578379e46d8a9f35d64d99d5efa39d",
                "ad62093fbc98eb7453a72015cc0fccdee9578379e46d8a9f35d64d99d5efa39d",
            ),
            _r(
                "FFP014_Q73A_EXPOSURE_EXECUTION",
                "urn:rawlsing:field-forge:ffp014:q73a-exposure:sha256:2ff4e74a3fc04a49da95925b02dad7865384f896849b4309c06f92464a85a3bf",
                "2ff4e74a3fc04a49da95925b02dad7865384f896849b4309c06f92464a85a3bf",
            ),
            role_receipt,
        ),
        position_role_receipt_ref=role_receipt,
        position_role_not_applicable_authority_ref=None,
        target_outcome_firewall_ref=_r(
            "FIELD_FORGE_TARGET_OUTCOME_FIREWALL",
            "urn:rawlsing:field-forge:ffp029:target-result-inspection-zero",
            "826df342ccad4b4f0c2c02b92f9b95ed596353270e38c3589b2eaf4702b21a54",
        ),
        applicability_authority_ref=_a(
            "urn:rawlsing:field-forge:ffp014:r5-q73a-applicability",
            "FFP014_CURRENT_RESPONDENT_EXECUTION_BINDING_ADMISSION_RECEIPT@1",
            "1a01cf216a4c70ffe9e9663ea8dd77381b2aecf8bea2d59c5853c234955ca244",
        ),
        applicability_receipt_ref=_r(
            "FFP014_Q73A_APPLICABILITY_RECEIPT",
            "urn:rawlsing:field-forge:ffp014:r5:q73a:ben0002:exposed-proved",
            "a781f4e66b1d24a28e16472886fab866525ed50018efbb73bbe929c73a87dedc",
        ),
        permission_authority_ref=_a(
            "urn:rawlsing:prev3:authority:objective-position-permission:ffp014-q73a-ben0002:r1",
            "F03@1.0.0",
            "e02ef5e77bb95a02d5fd02c7f5e300463bd98153f6bf97424c21d8a10546c662",
        ),
        allowed_uses=(SOURCE_DOMAIN_USE,),
        negative_ceiling_ref=negative,
        valid_time_authority_ref=_a(
            "urn:rawlsing:prev3:authority:objective-position-valid-time:ffp014-q73a-ben0002:r1",
            "F03@1.0.0",
            "5860749ebf23a2fe1a8adc81f05d6df601830447c3bffcf73bbd8c9e484b7b0d",
        ),
        valid_time_basis_ref=valid_time,
        currentness_authority_ref=_a(
            "urn:rawlsing:prev3:authority:objective-position-currentness:ffp014-q73a-ben0002:r1",
            "F03@1.0.0",
            "55328a2f52673028774118863807287100391118eedd18404f4f4a64338431ac",
        ),
        currentness_receipt_ref=currentness,
        provenance_refs=(
            admission,
            role_receipt,
            _r(
                "E03_GOVERNED_QUALIFICATION_RECEIPT",
                "urn:rawlsing:prev3:e03:qualification:run:34774291726",
                "9ffb0ada5b22ac5b4339aa2797635602072097b14735135693df5e7f091e36c7",
            ),
            _r(
                "F03_HQ_AUTHORIZATION",
                "urn:rawlsing:prev3:hq:f03:authority:3781860269c20006d82f9bec40df3a24b90861a0",
                "8412242b2843fd22db310ea7f896ddaf66f72ff25bb971cad9b291b047dc00c0",
            ),
        ),
        dependency_refs=(
            materializer,
            source_universe,
            source_release,
            source_claim,
            role_receipt,
            negative,
            valid_time,
            currentness,
        ),
        replay_authority_ref=_a(
            "urn:rawlsing:prev3:authority:objective-position-replay:d03-r1",
            "PREV3_OBJECTIVE_POSITION_MATERIALIZER_CONTRACT@1.0.0",
            "734c969406b38f6d5670c7079c9b06ca41caa7b6a7608b46da2e6baf4971500c",
        ),
        predecessor_position_fact_ref=None,
    )


def _fact():
    fact = materialize_objective_position(_input(), require_target_outcome_firewall=True)
    assert fact.fact_ref.object_id == PROVING_FACT_ID
    assert fact.fact_ref.content_hash == PROVING_FACT_HASH
    return fact


def _carrier():
    return publish_objective_position_fact(_fact())


def test_j04_h00_exact_proving_fact_publication_and_replay():
    carrier = _carrier()
    assert carrier.fact_ref.object_id == PROVING_FACT_ID
    assert carrier.root_entry.obj.producer_family == "PREV3_OBJECTIVE_POSITION_FACT"
    assert carrier.root_entry.obj.semantic_class == "PREV3_OBJECTIVE_POSITION_FACT"
    assert carrier.root_entry.obj.content_hash == PROVING_FACT_HASH
    assert carrier.root_entry.obj.typed_state == "POSITION_FACT_AUTHORIZED"
    assert carrier.root_entry.obj.producer_allowed_uses == ("CONTEXT",)
    assert carrier.root_entry.governance.authority_ref == J04_AUTHORITY_REF
    assert len(carrier.dependency_entries) == 8
    assert len(carrier.dependency_external_bindings) == 8
    assert all(binding.storage_locator == f"cas://sha256/{binding.object_ref.content_hash}" for binding in carrier.dependency_external_bindings)
    replay = replay_objective_position_publication(_fact(), carrier)
    assert replay.replay_identity == carrier.replay_identity
    with pytest.raises(ReferenceClassError):
        build_v557_publication_bundle((V557PublicationEntry(carrier.root_entry.obj, carrier.root_entry.governance),))


def test_j04_h01_relabel_producer_family_as_v552_rejected():
    root = _carrier().root_entry
    bad = replace(root.obj, producer_family="V552")
    with pytest.raises(M4IntegrityError):
        RepositoryEntry(bad, root.governance, root.locator)


def test_j04_h02_relabel_as_v553_v554_v555_v556_rejected():
    root = _carrier().root_entry
    for family in ("V553", "V554", "V555", "V556"):
        bad = replace(root.obj, producer_family=family)
        with pytest.raises(M4IntegrityError):
            RepositoryEntry(bad, root.governance, root.locator)


def test_j04_h03_schema_or_version_mutation_rejected():
    root = _carrier().root_entry
    bad = replace(root.obj, schema_id="V554_FAKE", schema_version="9.9.9")
    with pytest.raises(M4IntegrityError):
        RepositoryEntry(bad, root.governance, root.locator)


def test_j04_h04_fact_ref_kind_mutation_rejected():
    root = _carrier().root_entry
    bad = replace(root.obj, semantic_class="V554")
    with pytest.raises(M4IntegrityError):
        V557PublicationEntry(bad, root.governance)


def test_j04_h05_prev3pos_object_id_mutation_rejected():
    root = _carrier().root_entry
    bad = replace(root.obj, object_id=f"PREV3POS:{'0' * 64}")
    with pytest.raises(M4IntegrityError):
        RepositoryEntry(bad, root.governance, root.locator)


def test_j04_h06_content_hash_mutation_rejected():
    root = _carrier().root_entry
    with pytest.raises(M4IntegrityError):
        replace(root.obj, content_hash="0" * 64)


def test_j04_h07_nonpositive_position_result_not_publication_root():
    negative = typed_nonpositive_result(
        PositionResultState.UNAVAILABLE,
        reason_ref=_r("POSITION_REASON", "urn:test:position:unavailable", "1" * 64),
    )
    with pytest.raises(ObjectivePositionPublicationError):
        publish_objective_position_fact(negative)  # type: ignore[arg-type]


def test_j04_h08_source_domain_use_widen_or_substitute_rejected():
    changed = replace(_input(), allowed_uses=("SOME_OTHER_OBJECTIVE_USE",))
    fact = materialize_objective_position(changed, require_target_outcome_firewall=True)
    with pytest.raises(ObjectivePositionPublicationError):
        publish_objective_position_fact(fact)


def test_j04_h09_bare_context_without_domain_binding_rejected():
    carrier = _carrier()
    bare = make_context_query((
        ContextQueryItem(exact_resolution_key(carrier.root_entry.locator), (M4_CONTEXT_USE,)),
    ))
    with pytest.raises(ObjectivePositionPublicationError, match="bare CONTEXT"):
        require_bound_objective_position_context_query(carrier, bare)


def test_j04_h10_active_causal_request_rejected():
    carrier = _carrier()
    query = make_context_query(
        (ContextQueryItem(exact_resolution_key(carrier.root_entry.locator), ("ACTIVE_CAUSAL",)),),
        generated_binding_refs=(carrier.domain_use_binding.ref,),
    )
    with pytest.raises(ObjectivePositionPublicationError):
        require_bound_objective_position_context_query(carrier, query)


def test_j04_h11_review_is_not_inferred_from_context_mapping():
    carrier = _carrier()
    query = make_context_query(
        (ContextQueryItem(exact_resolution_key(carrier.root_entry.locator), ("REVIEW",)),),
        generated_binding_refs=(carrier.domain_use_binding.ref,),
    )
    with pytest.raises(ObjectivePositionPublicationError):
        require_bound_objective_position_context_query(carrier, query)


def test_j04_h12_drop_canonical_dependency_rejected():
    original = _input()
    changed = replace(original, dependency_refs=original.dependency_refs[:-1])
    fact = materialize_objective_position(changed, require_target_outcome_firewall=True)
    with pytest.raises(ObjectivePositionPublicationError):
        publish_objective_position_fact(fact)


def test_j04_h13_invent_dependency_ref_rejected():
    original = _input()
    changed = replace(
        original,
        dependency_refs=original.dependency_refs + (
            _r("INVENTED_DEP", "urn:test:invented", "2" * 64),
        ),
    )
    fact = materialize_objective_position(changed, require_target_outcome_firewall=True)
    with pytest.raises(ObjectivePositionPublicationError):
        publish_objective_position_fact(fact)


def test_j04_h14_negative_ceiling_mutation_rejected():
    changed = replace(
        _input(),
        negative_ceiling_ref=_r(
            "PREV3_OBJECTIVE_POSITION_NEGATIVE_CEILING",
            "urn:test:mutated-negative-ceiling",
            "3" * 64,
        ),
    )
    fact = materialize_objective_position(changed, require_target_outcome_firewall=True)
    with pytest.raises(ObjectivePositionPublicationError):
        publish_objective_position_fact(fact)


def test_j04_h15_runtime_clock_temporal_surrogate_rejected():
    changed = replace(
        _input(),
        valid_time_basis_ref=_r(
            "RUNTIME_CLOCK",
            "urn:test:runtime-clock:2026-now",
            "4" * 64,
        ),
    )
    fact = materialize_objective_position(changed, require_target_outcome_firewall=True)
    with pytest.raises(ObjectivePositionPublicationError):
        publish_objective_position_fact(fact)


def test_j04_h16_present_day_persistence_substitution_rejected():
    changed = replace(
        _input(),
        currentness_receipt_ref=_r(
            "PREV3_OBJECTIVE_POSITION_CURRENTNESS_RECEIPT",
            "urn:test:present-day-persistence:2026",
            "5" * 64,
        ),
    )
    fact = materialize_objective_position(changed, require_target_outcome_firewall=True)
    with pytest.raises(ObjectivePositionPublicationError):
        publish_objective_position_fact(fact)


def test_j04_h17_strip_evidence_or_provenance_rejected():
    original = _input()
    changed = replace(
        original,
        supporting_evidence_refs=original.supporting_evidence_refs[:-1],
        provenance_refs=original.provenance_refs[:-1],
    )
    fact = materialize_objective_position(changed, require_target_outcome_firewall=True)
    with pytest.raises(ObjectivePositionPublicationError):
        publish_objective_position_fact(fact)


def test_j04_h18_authority_ref_mutation_rejected():
    changed = replace(
        _input(),
        permission_authority_ref=_a(
            "urn:rawlsing:prev3:authority:objective-position-permission:ffp014-q73a-ben0002:r1",
            "F03@1.0.0",
            "6" * 64,
        ),
    )
    fact = materialize_objective_position(changed, require_target_outcome_firewall=True)
    with pytest.raises(ObjectivePositionPublicationError):
        publish_objective_position_fact(fact)


def test_j04_h19_latest_default_fuzzy_resolution_rejected():
    with pytest.raises(M4IntegrityError):
        ContextQueryItem("latest", (M4_CONTEXT_USE,))


def test_j04_h20_person_v3_psychological_use_rejected():
    with pytest.raises(PositionMaterializerError):
        replace(_input(), allowed_uses=("V3_PERSON_STATE",))


def test_j04_h21_m2_m3_stage_authority_not_inferred_from_publication():
    carrier = _carrier()
    with pytest.raises(ObjectivePositionPublicationError):
        make_bound_objective_position_context_query(
            carrier,
            requested_source_domain_use="M2_ROUTE_AUTHORITY",
        )
    assert all("m2" not in key.lower() and "m3" not in key.lower() for key in carrier.replay_identity)


def test_j04_h22_setlike_reordering_replays_identically():
    original = _input()
    reordered = replace(
        original,
        supporting_evidence_refs=tuple(reversed(original.supporting_evidence_refs)),
        provenance_refs=tuple(reversed(original.provenance_refs)),
        dependency_refs=tuple(reversed(original.dependency_refs)),
    )
    fact = materialize_objective_position(reordered, require_target_outcome_firewall=True)
    assert fact.fact_ref.object_id == PROVING_FACT_ID
    first = _carrier()
    second = publish_objective_position_fact(fact)
    assert second.replay_identity == first.replay_identity


def test_j04_h23_v558_locator_reidentification_rejected():
    root = _carrier().root_entry
    bad_locator = replace(root.locator, authoritative_object_id=f"PREV3POS:{'7' * 64}")
    with pytest.raises(M4IntegrityError, match="reversibly preserve"):
        RepositoryEntry(root.obj, root.governance, bad_locator)
