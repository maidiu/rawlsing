from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Mapping

import pytest

from rawlsing_next.m1_temporal_v554_admission_dedup import (
    M1_CONTRACT_ID,
    M1DecisionState,
    M1Evaluation,
    semantic_hash as m1_semantic_hash,
)
import rawlsing_next.m4_v557_v558_publication_repository as m4
import rawlsing_next.m5_runtime_rsc_peer_prior as m5
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef as Pre553AuthorityRef,
    EmpiricalFact,
    ExactRef as Pre553ExactRef,
    StructuralEmpiricalAdmission,
    assert_zero_actor_v3_v2_effect,
)
import rawlsing_next.v3_psepf_zero_positive_guard as v3


NONAUTHORITATIVE_INTERFACE_FIXTURE = (
    "NONAUTHORITATIVE_INTERFACE_FIXTURE__NO_SEMANTIC_ACCEPTANCE_EFFECT"
)

GT1_ID = "GT1_R5_Q86A_RAW_UNARY_EXACT_RISK_SET@1"
GT2_ID = "GT2_R5_Q86A_X_Q86B_RAW_JOINT_EXACT_RISK_SET@1"
RISK_SET_ID = "FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1"
RISK_SET_ROWS = 19_210
RISK_SET_MEMBER_SHA256 = (
    "0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b"
)
RELATION_FAMILY = "EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0"
ADMISSION_RULE = "FIELD_FORGE_RELATION_ADMISSION_RULE@1.0.0"
ADMISSION_FAMILY = "PREV3_FIELD_FORGE_RELATION_ADMISSION@1.0.0"
RELATION_M1_CONTRACT_ID = "M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0"
RELATION_BASIS_KIND = "ADMITTED_FIELD_FORGE_RELATION"
RELATION_SIGNATURE = "V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT"
TARGET_USE = "STRUCTURAL_MEDIATION_INPUT"
GT1_TERMINAL = "POSITIVE_EMPIRICAL_FACT__NO_STRUCTURAL_OR_ACTOR_PROMOTION_PASS"
GT2_TERMINAL = "POSITIVE_PREV3_STRUCTURAL_WORLD__V3_ZERO_EFFECT_PASS"

FORBIDDEN_STRONG_NOUNS = frozenset(
    {
        "FIELD",
        "FIELD_SPECIFIC_CAPITAL",
        "HEGEMONY",
        "SUBHEGEMONY",
        "HOMOLOGY",
        "PRESSURE_FOOTPRINT",
        "PRESSURE_PATHWAY",
        "STRUCTURAL_MECHANISM",
        "CONDITIONAL_REDISTRIBUTION_MECHANISM",
    }
)


@dataclass(frozen=True)
class IntegratedGT2Artifacts:
    """Nonsemantic acceptance envelope for actual centrally integrated objects."""

    joint_fact: EmpiricalFact
    relation: object
    admission: object
    m1_evaluation: M1Evaluation
    publication: m4.V557PublicationBundle
    repository: m4.V558RepositoryBundle
    query: m4.ContextQuery
    resolution: m4.ResolutionResult
    rsc: m5.ResolvedStructuralContext | None = None


def _h(label: str) -> str:
    return m1_semantic_hash({"gt12f": label})


def _pre_ref(kind: str, label: str) -> Pre553ExactRef:
    return Pre553ExactRef(kind, f"urn:test:gt12f:{kind.lower()}:{label}", _h(f"pre:{kind}:{label}"))


def _pre_authority(label: str) -> Pre553AuthorityRef:
    return Pre553AuthorityRef(
        f"GT12F-PRE-AUTH-{label}", "1.0.0", _h(f"pre-authority:{label}")
    )


def _m4_ref(kind: str, label: str) -> m4.ExactRef:
    return m4.ExactRef(kind, f"urn:test:gt12f:{kind.lower()}:{label}", _h(f"m4:{kind}:{label}"))


def _m4_authority(label: str) -> m4.AuthorityRef:
    return m4.AuthorityRef(
        f"GT12F-M4-AUTH-{label}", "1.0.0", _h(f"m4-authority:{label}")
    )


def _surface_tokens(obj: object) -> set[str]:
    names: set[str] = set()
    for field in (
        "family",
        "schema_id",
        "contract_id",
        "semantic_class",
        "relation_family",
        "relation_rule_id",
        "typed_state",
    ):
        value = getattr(obj, field, None)
        if isinstance(value, str):
            names.add(value.upper())
    semantic_fields = getattr(obj, "semantic_fields", None)
    if isinstance(semantic_fields, Mapping):
        for field in ("relation_family", "semantic_class", "relation_kind", "strong_noun"):
            value = semantic_fields.get(field)
            if isinstance(value, str):
                names.add(value.upper())
    return names


def assert_no_relation_i04_coercion(relation: object, admission: object) -> None:
    assert not isinstance(relation, EmpiricalFact)
    assert not isinstance(relation, StructuralEmpiricalAdmission)
    assert not isinstance(admission, EmpiricalFact)
    assert not isinstance(admission, StructuralEmpiricalAdmission)


def assert_no_strong_noun_promotion(*objects: object) -> None:
    for obj in objects:
        assert not (_surface_tokens(obj) & FORBIDDEN_STRONG_NOUNS)


def assert_gt1_positive_fact(
    fact: EmpiricalFact,
    *,
    expected_query_ref: Pre553ExactRef | None = None,
    expected_risk_set_ref: Pre553ExactRef | None = None,
) -> str:
    assert isinstance(fact, EmpiricalFact)
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == RISK_SET_ROWS
    assert fact.weighted_numerator_support_if_authorized is None
    assert fact.weighted_denominator_support_if_authorized is None
    if expected_query_ref is not None:
        assert fact.empirical_query_spec_ref == expected_query_ref.as_dict()
    if expected_risk_set_ref is not None:
        assert fact.risk_set_ref == expected_risk_set_ref.as_dict()
    assert_zero_actor_v3_v2_effect(fact)
    assert not isinstance(fact, StructuralEmpiricalAdmission)
    assert_no_strong_noun_promotion(fact)
    return GT1_TERMINAL


def _assert_exact_m1_to_m4_identity(
    evaluation: M1Evaluation,
    publication: m4.V557PublicationBundle,
    repository: m4.V558RepositoryBundle,
) -> None:
    handoff = evaluation.direct_v557_handoff
    assert isinstance(handoff, Mapping)
    assert handoff.get("route") == "V554_TO_V557_DIRECT"
    refs = handoff.get("object_refs")
    assert isinstance(refs, (tuple, list))
    expected = {
        (item["family"], item["object_id"], item["content_hash"])
        for item in refs
    }
    published = {
        (entry.obj.semantic_class, entry.obj.object_id, entry.obj.content_hash)
        for entry in publication.entries
    }
    repo_objects = {
        (entry.obj.semantic_class, entry.obj.object_id, entry.obj.content_hash)
        for entry in repository.entries
    }
    assert expected == published
    assert expected <= repo_objects
    assert {entry.obj.producer_family for entry in publication.entries} == {"V554"}
    assert all(entry.obj.producer_family not in {"V555", "V556"} for entry in repository.entries)


def _assert_permission_conservation(resolution: m4.ResolutionResult) -> None:
    assert resolution.receipt.result_state in {
        "RESOLUTION_COMPLETE",
        "RESOLUTION_COMPLETE_VALID_EMPTY",
    }
    for selection in resolution.selection_records:
        if selection.decision != "SELECTED":
            continue
        assert set(selection.resolver_allowed_uses) <= set(selection.v557_allowed_uses)
        assert set(selection.v557_allowed_uses) <= set(selection.producer_allowed_uses)


def _guard_structural_success(
    *,
    repository: m4.V558RepositoryBundle,
    rsc: m5.ResolvedStructuralContext | None,
) -> v3.GuardDecision:
    if rsc is None:
        source_class = "StructuralPriorRepository"
        source_ref = repository.repository_id
        source_hash = repository.repository_hash
    else:
        source_class = "ResolvedStructuralContext"
        source_ref = rsc.context_id
        source_hash = rsc.context_content_hash

    checkpoint = {
        "actor_state_hash": _h("actor-before"),
        "causal_ledger_hash": _h("ledger-before"),
        "causal_cursor": 0,
        "rng_state_hash": _h("rng-before"),
        "scheduler_state_hash": _h("scheduler-before"),
    }
    decision = v3.evaluate_psepf_zero_positive_guard(
        {
            "actor_id": "GT12F_ACCEPTANCE_NONAUTHORITATIVE_ACTOR_HANDLE",
            "source_class": source_class,
            "source_ref": source_ref,
            "source_hash": source_hash,
            "source_lineage": [],
            "transition_surface_id": "GT12_PREV3_TO_V3_ACCEPTANCE_BOUNDARY",
            "operation_class": "NO_POSITIVE_TRANSITION_AUTHORIZED",
            "state_fingerprint": checkpoint,
            "authority": None,
        }
    )
    assert dict(v3.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES) == {}
    assert decision.outcome is v3.GuardOutcome.DENY_ZERO_EFFECT
    assert decision.reason is v3.GuardReason.ZERO_POSITIVE_REGISTRY
    assert decision.delegated_owner_rule_id is None
    assert decision.zero_effect is True
    assert decision.actor_state_effect == "ZERO"
    assert decision.causal_ledger_appends == 0
    assert decision.causal_cursor_delta == 0
    assert decision.rng_mutations == 0
    assert decision.scheduler_mutations == 0
    assert decision.pre_state_fingerprint == decision.post_guard_state_fingerprint
    return decision


def assert_integrated_gt2_acceptance(artifacts: IntegratedGT2Artifacts) -> str:
    """Run only on actual A-E objects after central integration."""

    assert isinstance(artifacts.joint_fact, EmpiricalFact)
    assert artifacts.joint_fact.typed_state == "SUPPORTED"
    assert artifacts.joint_fact.raw_denominator_support == RISK_SET_ROWS
    assert artifacts.joint_fact.weighted_numerator_support_if_authorized is None
    assert artifacts.joint_fact.weighted_denominator_support_if_authorized is None
    assert_zero_actor_v3_v2_effect(artifacts.joint_fact)

    assert_no_relation_i04_coercion(artifacts.relation, artifacts.admission)
    assert_no_strong_noun_promotion(artifacts.relation, artifacts.admission)

    evaluation = artifacts.m1_evaluation
    assert isinstance(evaluation, M1Evaluation)
    assert evaluation.contract_id == RELATION_M1_CONTRACT_ID
    assert evaluation.decision_state is M1DecisionState.ELIGIBLE
    assert evaluation.required_basis_kind == RELATION_BASIS_KIND
    assert evaluation.support_count == 1
    assert evaluation.canonical_basis_semantic_id
    assert evaluation.f1 is not None
    assert evaluation.b1 is not None
    assert evaluation.direct_v557_handoff is not None

    _assert_exact_m1_to_m4_identity(
        evaluation, artifacts.publication, artifacts.repository
    )
    rerun = m4.resolve_v558(artifacts.repository, artifacts.query)
    assert rerun == artifacts.resolution
    assert rerun.resolved_structural_context is None
    _assert_permission_conservation(rerun)

    if artifacts.rsc is not None:
        assert isinstance(artifacts.rsc, m5.ResolvedStructuralContext)
        fields = {name.lower() for name in artifacts.rsc.__dataclass_fields__}
        assert "belief" not in fields
        assert "memory" not in fields
        assert "persona" not in fields
        assert "actorcausalstate" not in "".join(fields)

    _guard_structural_success(repository=artifacts.repository, rsc=artifacts.rsc)
    return GT2_TERMINAL


def _gt1_interface_fact() -> tuple[EmpiricalFact, Pre553ExactRef, Pre553ExactRef]:
    query_ref = _pre_ref("EMPIRICAL_QUERY_SPEC", GT1_ID)
    risk_ref = Pre553ExactRef(
        "RISK_SET",
        RISK_SET_ID,
        RISK_SET_MEMBER_SHA256,
    )
    fact = EmpiricalFact(
        typed_state="SUPPORTED",
        authority_snapshot_refs=(_pre_authority("gt1"),),
        dependency_refs=(query_ref,),
        producer_replay_locator_or_reference_root=_pre_ref("REPLAY_ROOT", "gt1"),
        empirical_query_spec_ref=query_ref,
        empirical_universe_refs=(_pre_ref("EMPIRICAL_UNIVERSE", "afrobarometer-r5"),),
        target_topology={
            "kind": "SCALAR_SINGULAR_SOURCE_NATIVE_DISTRIBUTION",
            "target": "Q86A",
            "fixture_notice": NONAUTHORITATIVE_INTERFACE_FIXTURE,
        },
        condition_predicate_ref=_pre_ref("EMPIRICAL_PREDICATE", "gt1"),
        risk_set_ref=risk_ref,
        raw_numerator_support=RISK_SET_ROWS,
        raw_denominator_support=RISK_SET_ROWS,
        weighted_numerator_support_if_authorized=None,
        weighted_denominator_support_if_authorized=None,
        measure_basis_ref=_pre_ref("MEASURE_BASIS", "RAW"),
        response_state_semantics_ref=_pre_ref("RESPONSE_STATE_SEMANTICS", "Q86A"),
        uncertainty_method_or_typed_state="NOT_APPLICABLE",
        source_empirical_provenance_refs=(
            _pre_ref("SOURCE_PROVENANCE", "afrobarometer-r5"),
        ),
        replay_ref=_pre_ref("REPLAY_RECEIPT", "gt1"),
    )
    return fact, query_ref, risk_ref


def _m1_interface_fixture() -> M1Evaluation:
    """Exercise downstream mechanics only; this is not GT2 relation authority."""

    f1 = {
        "family": "F1",
        "state": "ELIGIBLE",
        "f1_id": f"urn:rawlsing:v554:f1:sha256:{_h('fixture-f1')}",
        "material": {
            "fixture_notice": NONAUTHORITATIVE_INTERFACE_FIXTURE,
            "target_use": TARGET_USE,
            "signature_id": RELATION_SIGNATURE,
        },
    }
    b1 = {
        "family": "B1",
        "decision_state": "ELIGIBLE",
        "b1_id": f"urn:rawlsing:v554:b1:sha256:{_h('fixture-b1')}",
        "material": {
            "fixture_notice": NONAUTHORITATIVE_INTERFACE_FIXTURE,
            "f1_id_or_null": f1["f1_id"],
            "allowed_v555_structural_use": False,
        },
    }
    refs = (
        {
            "family": "F1",
            "object_id": f1["f1_id"],
            "content_hash": m1_semantic_hash(f1),
        },
        {
            "family": "B1",
            "object_id": b1["b1_id"],
            "content_hash": m1_semantic_hash(b1),
        },
    )
    return M1Evaluation(
        M1_CONTRACT_ID,
        M1DecisionState.ELIGIBLE,
        NONAUTHORITATIVE_INTERFACE_FIXTURE,
        GT2_ID,
        "DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION",
        1,
        f"urn:test:gt12f:basis:{_h('fixture-basis')}",
        f1,
        (),
        b1,
        {"route": "V554_TO_V557_DIRECT", "object_refs": refs},
        (),
    )


def _downstream_interface_fixture():
    evaluation = _m1_interface_fixture()
    objects = m4.structural_objects_from_m1(
        evaluation, producer_allowed_uses=("REVIEW",)
    )
    assert objects
    assert {obj.producer_family for obj in objects} == {"V554"}

    entries = []
    publication_entries = []
    for index, obj in enumerate(objects):
        authority = _m4_authority(f"v557-{index}")
        governance = m4.govern_v557(
            obj,
            decision_state=m4.V557DecisionState.ALLOW_REVIEW_ONLY,
            v557_allowed_uses=("REVIEW",),
            authority_ref=authority,
        )
        publication_entries.append(m4.V557PublicationEntry(obj, governance))
        locator = m4.make_producer_locator(
            obj,
            governance,
            logical_collection_kind="GT12F_NONAUTHORITATIVE_INTERFACE_FIXTURE",
            authoritative_build_id=f"GT12F-FIXTURE-BUILD-{index}",
            authoritative_build_hash=_h(f"fixture-build-{index}"),
            producer_contract_id=M1_CONTRACT_ID,
            producer_contract_version="1.0.0",
            producer_contract_hash=_h("fixture-m1-contract"),
            producer_rule_bindings=(authority,),
        )
        entries.append(m4.RepositoryEntry(obj, governance, locator))

    publication = m4.build_v557_publication_bundle(tuple(publication_entries))
    repository = m4.build_v558_repository_bundle(publication, tuple(entries))
    f1_entry = next(entry for entry in entries if entry.obj.semantic_class == "F1")
    query = m4.make_context_query(
        (
            m4.ContextQueryItem(
                m4.exact_resolution_key(f1_entry.locator), ("REVIEW",)
            ),
        )
    )
    resolution = m4.resolve_v558(repository, query)
    assert resolution.receipt.result_state == "RESOLUTION_COMPLETE"

    currentness = m5.make_structural_currentness_receipt(
        resolution,
        state=m5.StructuralCurrentnessState.CURRENT,
        authority_ref=_m4_authority("currentness"),
        structural_currentness_basis_ref=_m4_ref(
            "CURRENTNESS_BASIS", "interface-fixture"
        ),
        decision_effective_time_ref=_m4_ref(
            "EFFECTIVE_TIME", "interface-fixture"
        ),
    )
    rsc = m5.materialize_resolved_structural_context(
        repository, query, resolution, currentness
    )
    validation = m5.validate_resolved_structural_context(
        rsc, repository, query, resolution, currentness
    )
    assert validation.result == m5.M5_RSC_SUCCESS
    return evaluation, publication, repository, query, resolution, rsc, entries


def test_gt12f_interface_fixture_is_explicitly_nonauthoritative() -> None:
    assert NONAUTHORITATIVE_INTERFACE_FIXTURE.endswith(
        "NO_SEMANTIC_ACCEPTANCE_EFFECT"
    )
    evaluation = _m1_interface_fixture()
    assert evaluation.contract_id == M1_CONTRACT_ID
    assert evaluation.contract_id != RELATION_M1_CONTRACT_ID
    assert evaluation.reason == NONAUTHORITATIVE_INTERFACE_FIXTURE


def test_gt1_acceptance_assertion_requires_positive_empirical_fact_only() -> None:
    fact, query_ref, risk_ref = _gt1_interface_fact()
    assert (
        assert_gt1_positive_fact(
            fact,
            expected_query_ref=query_ref,
            expected_risk_set_ref=risk_ref,
        )
        == GT1_TERMINAL
    )
    with pytest.raises(AssertionError):
        assert_gt1_positive_fact(object())  # type: ignore[arg-type]


def test_gt2_downstream_interface_fixture_uses_actual_m4_m5_v3_without_v555_v556() -> None:
    (
        evaluation,
        publication,
        repository,
        query,
        resolution,
        rsc,
        _,
    ) = _downstream_interface_fixture()

    _assert_exact_m1_to_m4_identity(evaluation, publication, repository)
    assert m4.resolve_v558(repository, query) == resolution
    _assert_permission_conservation(resolution)
    assert {entry.obj.producer_family for entry in repository.entries} == {"V554"}
    assert all(entry.obj.producer_family not in {"V555", "V556"} for entry in repository.entries)

    decision = _guard_structural_success(repository=repository, rsc=rsc)
    assert decision.zero_effect is True


def test_hostile_permission_widening_fails_closed() -> None:
    *_, entries = _downstream_interface_fixture()
    obj = entries[0].obj
    with pytest.raises(m4.PermissionWideningError):
        m4.govern_v557(
            obj,
            decision_state=m4.V557DecisionState.ALLOW_CONTEXT_ONLY,
            v557_allowed_uses=("REVIEW", "CONTEXT"),
            authority_ref=_m4_authority("widen"),
        )


def test_hostile_exact_repository_hash_corruption_fails_closed() -> None:
    _, _, repository, query, _, _, _ = _downstream_interface_fixture()
    corrupted = replace(repository, repository_hash=_h("corrupted-repository"))
    with pytest.raises(m4.ClosureIntegrityError):
        m4.resolve_v558(corrupted, query)


def test_hostile_exact_query_hash_corruption_fails_closed() -> None:
    _, _, repository, query, _, _, _ = _downstream_interface_fixture()
    corrupted = replace(query, query_hash=_h("corrupted-query"))
    with pytest.raises(m4.M4IntegrityError):
        m4.resolve_v558(repository, corrupted)


def test_hostile_actor_reverse_lane_object_is_rejected() -> None:
    obj = m4.make_structural_object(
        producer_family="V554",
        semantic_class="V3_ACTOR_STATE",
        object_id=f"urn:test:gt12f:actor:{_h('actor-object')}",
        schema_id="GT12F_TEST",
        schema_version="1.0.0",
        typed_state="ELIGIBLE",
        producer_allowed_uses=("REVIEW",),
        payload={"fixture_notice": NONAUTHORITATIVE_INTERFACE_FIXTURE},
        source_stage="GT12F_TEST_ONLY",
    )
    governance = m4.govern_v557(
        obj,
        decision_state=m4.V557DecisionState.ALLOW_REVIEW_ONLY,
        v557_allowed_uses=("REVIEW",),
        authority_ref=_m4_authority("actor-reject"),
    )
    with pytest.raises(m4.ReferenceClassError):
        m4.build_v557_publication_bundle(
            (m4.V557PublicationEntry(obj, governance),)
        )


def test_hostile_i04_coercion_and_strong_noun_promotion_are_explicitly_forbidden() -> None:
    relation = type(
        "InterfaceRelation",
        (),
        {
            "family": RELATION_FAMILY,
            "semantic_class": "CONDITIONAL_SUPPORT_PROFILE",
            "fixture_notice": NONAUTHORITATIVE_INTERFACE_FIXTURE,
        },
    )()
    admission = type(
        "InterfaceAdmission",
        (),
        {
            "schema_id": ADMISSION_FAMILY,
            "contract_id": ADMISSION_RULE,
            "fixture_notice": NONAUTHORITATIVE_INTERFACE_FIXTURE,
        },
    )()
    assert_no_relation_i04_coercion(relation, admission)
    assert_no_strong_noun_promotion(relation, admission)

    fact, _, _ = _gt1_interface_fact()
    with pytest.raises(AssertionError):
        assert_no_relation_i04_coercion(fact, admission)

    bad = type(
        "StrongNounPromotion",
        (),
        {"semantic_class": "STRUCTURAL_MECHANISM"},
    )()
    with pytest.raises(AssertionError):
        assert_no_strong_noun_promotion(bad)


def test_integrated_acceptance_rejects_empirical_contract_as_relation_m1_authority() -> None:
    fact, _, _ = _gt1_interface_fact()
    evaluation, publication, repository, query, resolution, rsc, _ = (
        _downstream_interface_fixture()
    )
    relation = object()
    admission = object()
    artifacts = IntegratedGT2Artifacts(
        fact,
        relation,
        admission,
        evaluation,
        publication,
        repository,
        query,
        resolution,
        rsc,
    )
    with pytest.raises(AssertionError):
        assert_integrated_gt2_acceptance(artifacts)
