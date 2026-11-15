"""E6 reviewer-owned adversarial checks. Not part of the candidate commit."""
from __future__ import annotations

from dataclasses import replace
from threading import Barrier, Thread

import pytest

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_learned_product_lifecycle import (
    LearnedProductLifecycleConflict,
    LearnedProductLifecycleError,
    LearnedProductLifecycleExecutor as B5,
)
from rawlsing_next.pre553_learned_product_release import (
    M2_PUBLICATION_CONTRACT_REF,
    M2ReleaseError,
    M2Repository,
    PublicationBinding,
    RepresentationRecord,
    publish_binding,
    resolve_release_exact,
)
from rawlsing_next.tests.s06g_fixtures import checkpoint_with_publication, m2_fixture, ref, register, subject
from rawlsing_next.tests.test_pre553_learned_product_lifecycle import _key, _select
from rawlsing_next.tests.test_pre553_learned_product_release import (
    bind_representation,
    build_fixture,
)


def snapshot(repo: M2Repository):
    return {name: dict(getattr(repo, name)) for name in repo._store_names}


def import_foreign(target: M2Repository, source: M2Repository, release) -> None:
    target.register_subject(source.subject_exact(release.release_subject_ref))
    for field in (
        "authority_closure_ref",
        "dependency_closure_ref",
        "determinant_closure_ref",
        "replay_reconstruction_ref",
        "explanation_lineage_ref",
    ):
        target.register_closure(source.closure_exact(getattr(release, field)))
    target.register_release(release)


def test_ind_m2_17_early_refusal_then_lawful_foreign_import_preserves_oracle():
    repo, first, _, _, _, _ = build_fixture(subject_label="ind-first")
    foreign, second, source, producer, _, _ = build_fixture(subject_label="ind-second")
    locator = ref("ind-foreign:locator", "RepresentationLocator")
    integrity = ref("ind-foreign:integrity", "RepresentationIntegrity")
    record = RepresentationRecord(
        release_ref=second.ref,
        resolved_subject_ref=source,
        producer_contract_ref=producer,
        resolution_mode="CONTENT_ADDRESSED_MATERIALIZATION",
        resolver_or_locator_ref=locator,
        representation_integrity_ref=integrity,
    )
    before = snapshot(repo)
    with pytest.raises(M2ReleaseError) as exc:
        repo.register_representation(record)
    assert exc.value.code == "RELEASE_UNAVAILABLE"
    assert snapshot(repo) == before

    import_foreign(repo, foreign, second)
    repo.register_representation(record)
    with pytest.raises(M2ReleaseError) as exc:
        publish_binding(
            repo,
            release_ref=first.ref,
            resolution_mode="CONTENT_ADDRESSED_MATERIALIZATION",
            resolver_or_locator_ref=locator,
            representation_integrity_ref=integrity,
        )
    assert exc.value.code == "PUBLICATION_BINDING_MISMATCH"


def test_ind_m2_18_early_refusal_then_lawful_foreign_import_preserves_failover_oracle():
    repo, release, source, producer, _, _ = build_fixture(subject_label="ind-main")
    first, _, _ = bind_representation(
        repo, release, source, producer, label="ind-a", mode="CONTENT_ADDRESSED_MATERIALIZATION"
    )
    second, _, _ = bind_representation(
        repo, release, source, producer, label="ind-b", mode="CONTENT_ADDRESSED_MATERIALIZATION"
    )
    result = resolve_release_exact(
        repo,
        release.ref,
        publication_binding_refs=(first.ref, second.ref),
        unavailable_binding_refs=(first.ref,),
    )
    assert result.receipt.used_publication_binding_ref == second.ref

    foreign, other, osource, oproducer, _, _ = build_fixture(subject_label="ind-foreign")
    binding, locator, _ = bind_representation(
        foreign, other, osource, oproducer, label="ind-foreign", mode="CONTENT_ADDRESSED_MATERIALIZATION"
    )
    before = snapshot(repo)
    with pytest.raises(M2ReleaseError) as exc:
        repo.register_binding(binding)
    assert exc.value.code == "RELEASE_UNAVAILABLE"
    assert snapshot(repo) == before

    import_foreign(repo, foreign, other)
    repo.register_representation(foreign.representation_exact(locator))
    repo.register_binding(binding)
    with pytest.raises(M2ReleaseError) as exc:
        resolve_release_exact(
            repo,
            release.ref,
            publication_binding_refs=(first.ref, binding.ref),
            unavailable_binding_refs=(first.ref,),
        )
    assert exc.value.code == "PUBLICATION_BINDING_MISMATCH"


def test_ind_direct_release_insertion_requires_local_subject_and_closures():
    local, local_release, _, _, _, _ = build_fixture(subject_label="ind-local")
    foreign, foreign_release, _, _, _, _ = build_fixture(subject_label="ind-foreign-release")
    before = snapshot(local)
    with pytest.raises(M2ReleaseError):
        local.register_release(foreign_release)
    assert snapshot(local) == before
    assert local.releases == (local_release,)


def test_ind_binding_writer_checks_contract_and_representation():
    repo, release, source, producer, _, _ = build_fixture(subject_label="ind-bind")
    record = RepresentationRecord(
        release_ref=release.ref,
        resolved_subject_ref=source,
        producer_contract_ref=producer,
        resolution_mode="CONTENT_ADDRESSED_MATERIALIZATION",
        resolver_or_locator_ref=ref("ind-bind:locator", "RepresentationLocator"),
        representation_integrity_ref=ref("ind-bind:integrity", "RepresentationIntegrity"),
    )
    repo.register_representation(record)
    wrong_contract = PublicationBinding(
        release_ref=release.ref,
        publication_contract_ref=ref("ind-bind:contract", "WrongContract"),
        resolution_mode=record.resolution_mode,
        resolver_or_locator_ref=record.resolver_or_locator_ref,
        representation_integrity_ref=record.representation_integrity_ref,
    )
    before = snapshot(repo)
    with pytest.raises(M2ReleaseError):
        repo.register_binding(wrong_contract)
    assert snapshot(repo) == before
    good = PublicationBinding(
        release_ref=release.ref,
        publication_contract_ref=M2_PUBLICATION_CONTRACT_REF,
        resolution_mode=record.resolution_mode,
        resolver_or_locator_ref=record.resolver_or_locator_ref,
        representation_integrity_ref=record.representation_integrity_ref,
    )
    repo.register_binding(good)
    assert repo.binding_exact(good.ref) == good


def test_ind_nested_payload_immutable_and_export_detached():
    executor, item, checkpoint = checkpoint_with_publication()
    event = executor.events[-1]
    old_ref = event.ref
    with pytest.raises(TypeError):
        event.payload["replay_root_ref"]["object_id"] = "alien"
    assert event.ref == old_ref
    exported = event.as_dict()
    exported["payload"]["replay_root_ref"]["object_id"] = "export-only"
    assert event.ref == old_ref
    assert executor.export_checkpoint() == checkpoint


def test_ind_cold_replay_detaches_caller_checkpoint_after_restore():
    executor, _, checkpoint = checkpoint_with_publication()
    restored = B5.from_checkpoint(checkpoint)
    original = restored.export_checkpoint()
    checkpoint["checkpoint_payload"]["events"][-1]["payload"]["replay_root_ref"]["object_id"] = "caller"
    checkpoint["checkpoint_payload"]["events"].clear()
    assert restored.export_checkpoint() == original
    assert B5.from_checkpoint(original).export_checkpoint() == original


def test_ind_rehashed_publication_event_is_refused_on_cold_replay():
    executor, _, checkpoint = checkpoint_with_publication()
    replacement = dict(executor.events[-1].payload)
    replacement["replay_root_ref"] = ref("Alien", "replay").as_dict()
    checkpoint["checkpoint_payload"]["events"][-1] = replace(
        executor.events[-1], payload=replacement
    ).as_dict()
    checkpoint["checkpoint_hash"] = semantic_hash(checkpoint["checkpoint_payload"])
    with pytest.raises(LearnedProductLifecycleConflict):
        B5.from_checkpoint(checkpoint)


def test_ind_two_writer_selection_is_serialized_and_cold_replays():
    for _ in range(8):
        executor = B5()
        a = register(executor, subject("ind-race-a"), publish=True)
        b = register(executor, subject("ind-race-b"), publish=True)
        key = _key(executor, a)
        barrier = Barrier(2)
        winners, errors = [], []

        def run(item):
            barrier.wait(timeout=5)
            try:
                winners.append(_select(executor, key, item))
            except Exception as exc:
                errors.append(exc)

        threads = [Thread(target=run, args=(item,)) for item in (a, b)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=6)
        assert all(not thread.is_alive() for thread in threads)
        assert len(winners) == len(errors) == 1
        assert isinstance(errors[0], LearnedProductLifecycleConflict)
        checkpoint = executor.export_checkpoint()
        assert B5.from_checkpoint(checkpoint).export_checkpoint() == checkpoint


def test_ind_saved_helpers_and_unwrapped_bodies_refuse():
    executor, item, checkpoint = checkpoint_with_publication()
    event = executor._event(
        event_kind="PRODUCT_PUBLISHED",
        subject=subject("ind-unregistered"),
        event_authority_ref=ref("Authority", "ind"),
        event_rule_ref=ref("Rule", "ind"),
    )
    with pytest.raises(LearnedProductLifecycleConflict, match="transaction"):
        executor._append_events((event,))
    with pytest.raises(LearnedProductLifecycleConflict, match="transaction"):
        executor._commit_selection_transition_receipts(())
    assert executor.export_checkpoint() == checkpoint
    repo = M2Repository()
    with pytest.raises(M2ReleaseError, match="transaction"):
        repo._insert(repo._releases, ref("Release", "ind-alien"), "untyped", "COLLISION")
    staged_before = executor.staged_release_refs
    with pytest.raises(LearnedProductLifecycleConflict, match="transaction"):
        B5.stage_release.__wrapped__(executor, subject("ind-outside"))
    assert executor.staged_release_refs == staged_before


def test_ind_external_mode_is_held_and_saved_alias_does_not_elevate():
    executor, item, _ = checkpoint_with_publication()
    assert executor.native_security_mode == "LOCAL_UNAUTHENTICATED"
    with pytest.raises(LearnedProductLifecycleError, match="EXTERNAL_ISSUER_HOLD"):
        executor.require_external_issuer("ind")
    executor._native_security_mode = "EXTERNAL_CUSTODY"
    with pytest.raises(LearnedProductLifecycleError, match="EXTERNAL_ISSUER_HOLD"):
        executor.publish_product(
            item.release_ref,
            event_authority_ref=ref("Authority", "ind"),
            event_rule_ref=ref("Rule", "ind"),
        )
    repo, release, source, _, _ = m2_fixture()
    before = snapshot(repo)
    repo._native_security_mode = "PROTECTED_CURRENT"
    with pytest.raises(M2ReleaseError, match="EXTERNAL_ISSUER_HOLD"):
        repo.register_subject(repo.subject_exact(source))
    assert snapshot(repo) == before


def test_ind_m2_competing_subject_preimages_do_not_overwrite():
    repo, _, source, _, _ = m2_fixture()
    first = replace(repo.subject_exact(source), ref=ref("Subject", "ind-collision"))
    second = replace(first, typed_state="UNKNOWN")
    barrier = Barrier(2)
    winners, errors = [], []

    def write(record):
        barrier.wait(timeout=5)
        try:
            winners.append(repo.register_subject(record))
        except Exception as exc:
            errors.append(exc)

    threads = [Thread(target=write, args=(record,)) for record in (first, second)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=6)
    assert all(not thread.is_alive() for thread in threads)
    assert len(winners) == len(errors) == 1
    assert isinstance(errors[0], M2ReleaseError)
    assert errors[0].code == "SEMANTIC_REOWNERSHIP_ATTEMPT"
    assert repo.subject_exact(first.ref) == winners[0]
