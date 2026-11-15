from __future__ import annotations

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_learned_product_release import (
    M2Repository,
    M2ReleaseError,
    M2_RELEASE_CONTRACT_REF,
    affected_release_refs,
    constitute_closure,
    constitute_release,
    explain_release,
    publish_binding,
    register_producer_subject,
    register_representation,
    resolve_release_exact,
    resolve_subject_exact,
)


def ref(label: str, kind: str = "TEST") -> ExactRef:
    digest = semantic_hash({"label": label, "kind": kind})
    return ExactRef(kind, f"urn:test:{label}:sha256:{digest}", digest)


def build_fixture(
    *,
    state: str = "SUPPORTED",
    subject_kind: str = "TYPED_DISPOSITION",
    replay_grade: str = "EXACT_DETERMINISTIC_REBUILD",
    subject_label: str = "subject",
):
    repo = M2Repository()
    producer = ref(f"{subject_label}:producer", "ProducerContract")
    subject = ref(subject_label, "LearnedEmpiricalDisposition")
    required = {
        "authority": ref(f"{subject_label}:authority", "Authority"),
        "dependency": ref(f"{subject_label}:dependency", "Dependency"),
        "determinant": ref(f"{subject_label}:determinant", "Determinant"),
        "replay": ref(f"{subject_label}:replay", "ReplayDeterminant"),
        "explanation": ref(f"{subject_label}:explanation", "ExplanationNode"),
    }
    register_producer_subject(
        repo,
        subject_ref=subject,
        subject_kind=subject_kind,
        producer_contract_ref=producer,
        typed_state=state,
        required_authority_refs=(required["authority"],),
        required_dependency_refs=(required["dependency"],),
        required_determinant_refs=(required["determinant"],),
        required_replay_refs=(required["replay"],),
        required_explanation_refs=(required["explanation"],),
    )
    closures = {
        "authority": constitute_closure(
            repo,
            closure_kind="AUTHORITY",
            member_refs=(producer, required["authority"]),
        ),
        "dependency": constitute_closure(
            repo,
            closure_kind="DEPENDENCY",
            member_refs=(required["dependency"],),
        ),
        "determinant": constitute_closure(
            repo,
            closure_kind="DETERMINANT",
            member_refs=(required["determinant"],),
        ),
        "replay": constitute_closure(
            repo,
            closure_kind="REPLAY_RECONSTRUCTION",
            member_refs=(required["replay"],),
            metadata={"replay_grade": replay_grade},
        ),
        "explanation": constitute_closure(
            repo,
            closure_kind="EXPLANATION_LINEAGE",
            member_refs=(subject, producer, required["explanation"]),
        ),
    }
    release = constitute_release(
        repo,
        release_subject_ref=subject,
        release_subject_kind=subject_kind,
        semantic_producer_contract_ref=producer,
        authority_closure_ref=closures["authority"].ref,
        dependency_closure_ref=closures["dependency"].ref,
        determinant_closure_ref=closures["determinant"].ref,
        replay_reconstruction_ref=closures["replay"].ref,
        explanation_lineage_ref=closures["explanation"].ref,
    )
    return repo, release, subject, producer, required, closures


def bind_representation(repo, release, subject, producer, *, label, mode):
    locator = ref(f"{label}:locator", "RepresentationLocator")
    integrity = ref(f"{label}:integrity", "RepresentationIntegrity")
    register_representation(
        repo,
        release_ref=release.ref,
        resolution_mode=mode,
        resolver_or_locator_ref=locator,
        representation_integrity_ref=integrity,
        resolved_subject_ref=subject,
        producer_contract_ref=producer,
    )
    binding = publish_binding(
        repo,
        release_ref=release.ref,
        resolution_mode=mode,
        resolver_or_locator_ref=locator,
        representation_integrity_ref=integrity,
    )
    return binding, locator, integrity


def assert_code(exc: pytest.ExceptionInfo[M2ReleaseError], code: str):
    assert exc.value.code == code


def test_01_same_exact_preimage_same_release_id():
    repo, release, subject, producer, _, closures = build_fixture()
    duplicate = constitute_release(
        repo,
        release_subject_ref=subject,
        release_subject_kind="TYPED_DISPOSITION",
        semantic_producer_contract_ref=producer,
        authority_closure_ref=closures["authority"].ref,
        dependency_closure_ref=closures["dependency"].ref,
        determinant_closure_ref=closures["determinant"].ref,
        replay_reconstruction_ref=closures["replay"].ref,
        explanation_lineage_ref=closures["explanation"].ref,
        release_contract_ref=M2_RELEASE_CONTRACT_REF,
    )
    assert duplicate.ref == release.ref


def test_02_constitutive_closure_change_changes_release_id():
    repo, release, subject, producer, required, closures = build_fixture()
    extra = ref("extra-authority", "Authority")
    authority2 = constitute_closure(
        repo,
        closure_kind="AUTHORITY",
        member_refs=(producer, required["authority"], extra),
    )
    release2 = constitute_release(
        repo,
        release_subject_ref=subject,
        release_subject_kind="TYPED_DISPOSITION",
        semantic_producer_contract_ref=producer,
        authority_closure_ref=authority2.ref,
        dependency_closure_ref=closures["dependency"].ref,
        determinant_closure_ref=closures["determinant"].ref,
        replay_reconstruction_ref=closures["replay"].ref,
        explanation_lineage_ref=closures["explanation"].ref,
    )
    assert release2.ref != release.ref
    assert release2.release_subject_ref == release.release_subject_ref


def test_03_physical_relayout_changes_binding_not_release_core():
    repo, release, subject, producer, _, _ = build_fixture()
    b1, _, _ = bind_representation(
        repo, release, subject, producer,
        label="path-a", mode="CONTENT_ADDRESSED_MATERIALIZATION",
    )
    b2, _, _ = bind_representation(
        repo, release, subject, producer,
        label="path-b", mode="CONTENT_ADDRESSED_MATERIALIZATION",
    )
    assert b1.release_ref == b2.release_ref == release.ref
    assert b1.ref != b2.ref


def test_04_exact_subject_required():
    repo, _, _, producer, _, closures = build_fixture()
    with pytest.raises(M2ReleaseError) as exc:
        constitute_release(
            repo,
            release_subject_ref="latest",
            release_subject_kind="TYPED_DISPOSITION",
            semantic_producer_contract_ref=producer,
            authority_closure_ref=closures["authority"].ref,
            dependency_closure_ref=closures["dependency"].ref,
            determinant_closure_ref=closures["determinant"].ref,
            replay_reconstruction_ref=closures["replay"].ref,
            explanation_lineage_ref=closures["explanation"].ref,
        )
    assert_code(exc, "FORBIDDEN_SELECTOR")


def test_05_producer_contract_mismatch_fails_closed():
    repo, _, subject, _, _, closures = build_fixture()
    with pytest.raises(M2ReleaseError) as exc:
        constitute_release(
            repo,
            release_subject_ref=subject,
            release_subject_kind="TYPED_DISPOSITION",
            semantic_producer_contract_ref=ref("wrong-producer", "ProducerContract"),
            authority_closure_ref=closures["authority"].ref,
            dependency_closure_ref=closures["dependency"].ref,
            determinant_closure_ref=closures["determinant"].ref,
            replay_reconstruction_ref=closures["replay"].ref,
            explanation_lineage_ref=closures["explanation"].ref,
        )
    assert_code(exc, "PRODUCER_CONTRACT_MISMATCH")


def test_06_incomplete_required_closure_fails_closed():
    repo, _, subject, producer, _, closures = build_fixture()
    incomplete = constitute_closure(
        repo,
        closure_kind="DETERMINANT",
        member_refs=(),
        complete=False,
    )
    with pytest.raises(M2ReleaseError) as exc:
        constitute_release(
            repo,
            release_subject_ref=subject,
            release_subject_kind="TYPED_DISPOSITION",
            semantic_producer_contract_ref=producer,
            authority_closure_ref=closures["authority"].ref,
            dependency_closure_ref=closures["dependency"].ref,
            determinant_closure_ref=incomplete.ref,
            replay_reconstruction_ref=closures["replay"].ref,
            explanation_lineage_ref=closures["explanation"].ref,
        )
    assert_code(exc, "DETERMINANT_CLOSURE_INCOMPLETE")


@pytest.mark.parametrize("selector", ["latest", "default", "fuzzy", "nearest", "semver"])
def test_07_no_latest_default_fuzzy_nearest_semver_fallback(selector):
    repo, _, _, _, _, _ = build_fixture()
    with pytest.raises(M2ReleaseError) as exc:
        resolve_release_exact(repo, selector)
    assert_code(exc, "FORBIDDEN_SELECTOR")


def test_08_virtual_rebuild_parity_and_mismatch_detection():
    repo, release, subject, producer, _, _ = build_fixture(
        replay_grade="EXACT_DETERMINISTIC_REBUILD"
    )
    binding, _, _ = bind_representation(
        repo, release, subject, producer,
        label="virtual-ok", mode="GOVERNED_VIRTUAL_REBUILDER",
    )
    result = resolve_release_exact(
        repo, release.ref, publication_binding_refs=(binding.ref,)
    )
    assert result.subject is not None and result.subject.ref == subject

    wrong_subject = ref("wrong-rebuild-subject", "LearnedEmpiricalDisposition")
    with pytest.raises(M2ReleaseError) as exc:
        register_representation(
            repo,
            release_ref=release.ref,
            resolution_mode="GOVERNED_VIRTUAL_REBUILDER",
            resolver_or_locator_ref=ref("virtual-bad:locator", "RepresentationLocator"),
            representation_integrity_ref=ref("virtual-bad:integrity", "RepresentationIntegrity"),
            resolved_subject_ref=wrong_subject,
            producer_contract_ref=producer,
        )
    assert_code(exc, "REBUILD_SEMANTIC_MISMATCH")


def test_09_materialized_virtual_semantic_parity():
    repo, release, subject, producer, _, _ = build_fixture(
        replay_grade="EXACT_DETERMINISTIC_REBUILD"
    )
    materialized, _, _ = bind_representation(
        repo, release, subject, producer,
        label="materialized", mode="CONTENT_ADDRESSED_MATERIALIZATION",
    )
    virtual, _, _ = bind_representation(
        repo, release, subject, producer,
        label="virtual", mode="GOVERNED_VIRTUAL_REBUILDER",
    )
    r1 = resolve_release_exact(
        repo, release.ref, publication_binding_refs=(materialized.ref,)
    )
    r2 = resolve_release_exact(
        repo, release.ref, publication_binding_refs=(virtual.ref,)
    )
    assert r1.release_core.ref == r2.release_core.ref == release.ref
    assert r1.subject.ref == r2.subject.ref == subject
    assert r1.receipt.used_publication_binding_ref != r2.receipt.used_publication_binding_ref


def test_10_valid_empty_disposition_publishes_without_positive_invention():
    repo, release, subject, producer, _, _ = build_fixture(state="VALID_EMPTY")
    binding, _, _ = bind_representation(
        repo, release, subject, producer,
        label="valid-empty", mode="CONTENT_ADDRESSED_MATERIALIZATION",
    )
    result = resolve_release_exact(
        repo, release.ref, publication_binding_refs=(binding.ref,)
    )
    assert result.subject.typed_state == "VALID_EMPTY"
    assert result.release_core.release_subject_kind == "TYPED_DISPOSITION"


@pytest.mark.parametrize(
    "state",
    ["NONCOMPARABLE", "BLOCKED", "UNKNOWN", "INTEGRITY_FAILURE"],
)
def test_11_nonpositive_states_preserved(state):
    repo, release, _, _, _, _ = build_fixture(
        state=state, subject_label=f"subject-{state.lower()}"
    )
    result = resolve_release_exact(repo, release.ref)
    assert result.subject is not None
    assert result.subject.typed_state == state


def test_12_no_negative_state_laundering_through_representation():
    repo, release, subject, producer, _, _ = build_fixture(state="VALID_EMPTY")
    positive_subject = ref("positive-other-subject", "LearnedEmpiricalDisposition")
    with pytest.raises(M2ReleaseError) as exc:
        register_representation(
            repo,
            release_ref=release.ref,
            resolution_mode="CONTENT_ADDRESSED_MATERIALIZATION",
            resolver_or_locator_ref=ref("launder:locator", "RepresentationLocator"),
            representation_integrity_ref=ref("launder:integrity", "RepresentationIntegrity"),
            resolved_subject_ref=positive_subject,
            producer_contract_ref=producer,
        )
    assert_code(exc, "REPRESENTATION_INTEGRITY_FAILURE")
    assert resolve_subject_exact(repo, release.ref).ref == subject


def test_13_no_b5_lifecycle_published_state_minted():
    repo, release, subject, producer, _, _ = build_fixture()
    binding, _, _ = bind_representation(
        repo, release, subject, producer,
        label="no-b5", mode="CONTENT_ADDRESSED_MATERIALIZATION",
    )
    result = resolve_release_exact(
        repo, release.ref, publication_binding_refs=(binding.ref,)
    )
    assert result.receipt.lifecycle_publication_effect is False
    assert not hasattr(binding, "published")
    assert not hasattr(release, "published")


def test_14_no_current_selection_minted():
    repo, release, _, _, _, _ = build_fixture()
    result = resolve_release_exact(repo, release.ref)
    assert result.receipt.current_selection_effect is False
    assert not hasattr(release, "current")
    with pytest.raises(M2ReleaseError):
        resolve_release_exact(repo, "latest")


def test_15_no_consumer_permission_minted():
    repo, release, _, _, _, _ = build_fixture()
    result = resolve_release_exact(repo, release.ref)
    assert result.receipt.consumer_permission_effect is False
    assert not hasattr(release, "consumer_permission")


def test_16_direct_producer_dereference_preserves_owner():
    repo, release, subject, producer, _, _ = build_fixture()
    resolved = resolve_subject_exact(repo, release.ref)
    assert resolved.ref == subject
    assert resolved.producer_contract_ref == producer
    explanation = explain_release(repo, release.ref)
    assert explanation.release_subject_ref == subject
    assert explanation.semantic_producer_contract_ref == producer


def test_17_binding_cannot_resolve_different_release():
    repo1, release1, _, _, _, _ = build_fixture(subject_label="release-one")
    repo2, release2, subject2, producer2, _, _ = build_fixture(subject_label="release-two")
    # Recreate release-two representation inside repo1 only as a foreign exact record.
    # First copy its producer subject/closures is intentionally avoided; a foreign
    # representation exact-ref is enough to test release mismatch at publication.
    locator = ref("foreign:locator", "RepresentationLocator")
    integrity = ref("foreign:integrity", "RepresentationIntegrity")
    from rawlsing_next.pre553_learned_product_release import RepresentationRecord
    repo1.register_representation(
        RepresentationRecord(
            release_ref=release2.ref,
            resolved_subject_ref=subject2,
            producer_contract_ref=producer2,
            resolution_mode="CONTENT_ADDRESSED_MATERIALIZATION",
            resolver_or_locator_ref=locator,
            representation_integrity_ref=integrity,
        )
    )
    with pytest.raises(M2ReleaseError) as exc:
        publish_binding(
            repo1,
            release_ref=release1.ref,
            resolution_mode="CONTENT_ADDRESSED_MATERIALIZATION",
            resolver_or_locator_ref=locator,
            representation_integrity_ref=integrity,
        )
    assert_code(exc, "PUBLICATION_BINDING_MISMATCH")


def test_18_endpoint_failover_only_among_same_release():
    repo, release, subject, producer, _, _ = build_fixture(subject_label="failover-one")
    b1, _, _ = bind_representation(
        repo, release, subject, producer,
        label="failover-a", mode="CONTENT_ADDRESSED_MATERIALIZATION",
    )
    b2, _, _ = bind_representation(
        repo, release, subject, producer,
        label="failover-b", mode="CONTENT_ADDRESSED_MATERIALIZATION",
    )
    result = resolve_release_exact(
        repo,
        release.ref,
        publication_binding_refs=(b1.ref, b2.ref),
        unavailable_binding_refs=(b1.ref,),
    )
    assert result.receipt.used_publication_binding_ref == b2.ref

    repo_other, release_other, subject_other, producer_other, _, _ = build_fixture(
        subject_label="failover-other"
    )
    other_binding, _, _ = bind_representation(
        repo_other,
        release_other,
        subject_other,
        producer_other,
        label="other-endpoint",
        mode="CONTENT_ADDRESSED_MATERIALIZATION",
    )
    # Register exact foreign binding into repo solely to attack the failover list.
    repo.register_binding(other_binding)
    with pytest.raises(M2ReleaseError) as exc:
        resolve_release_exact(
            repo,
            release.ref,
            publication_binding_refs=(b1.ref, other_binding.ref),
            unavailable_binding_refs=(b1.ref,),
        )
    assert_code(exc, "PUBLICATION_BINDING_MISMATCH")


def test_19_deterministic_historical_resolution():
    repo, release, subject, producer, _, _ = build_fixture(subject_label="historical")
    binding, _, _ = bind_representation(
        repo, release, subject, producer,
        label="historical-binding", mode="CONTENT_ADDRESSED_MATERIALIZATION",
    )
    first = resolve_release_exact(
        repo, release.ref, publication_binding_refs=(binding.ref,)
    )
    second = resolve_release_exact(
        repo, release.ref, publication_binding_refs=(binding.ref,)
    )
    assert first.receipt.ref == second.receipt.ref
    assert first.receipt.selector_substitution is False


def test_20_m1_learned_empirical_disposition_is_exact_release_subject():
    repo, release, subject, producer, _, _ = build_fixture(
        state="RULE_SATISFIED",
        subject_kind="TYPED_DISPOSITION",
        subject_label="m1-learned-empirical-disposition",
    )
    assert subject.kind == "LearnedEmpiricalDisposition"
    resolved = resolve_release_exact(repo, release.ref)
    assert resolved.subject.ref == subject
    assert resolved.subject.producer_contract_ref == producer
    assert resolved.release_core.release_subject_kind == "TYPED_DISPOSITION"


def test_21_affected_release_refs_is_graph_only_and_selective():
    repo, release, _, _, required, _ = build_fixture(subject_label="affected")
    unrelated = ref("unrelated-determinant", "Determinant")
    affected = affected_release_refs(repo, required["determinant"])
    not_affected = affected_release_refs(repo, unrelated)
    assert affected == (release.ref,)
    assert not_affected == ()
