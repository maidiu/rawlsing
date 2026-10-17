from __future__ import annotations

from dataclasses import dataclass

import pytest

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash
from rawlsing_next.pre553_learned_product_lifecycle import (
    B5_EVENT_KINDS,
    LIFECYCLE_CONTRACT_ID,
    CurrentSelectionReceipt,
    GCElegibilityReceipt,
    LearnedProductLifecycleConflict,
    LearnedProductLifecycleError,
    LearnedProductLifecycleExecutor,
    LearnedProductLifecycleSubject,
    NoCurrentReceipt,
)


def _ref(kind: str, tag: str) -> ExactRef:
    digest = semantic_hash({"kind": kind, "tag": tag})
    return ExactRef(kind, f"urn:test:{kind.lower()}:{tag}:sha256:{digest}", digest)


def _auth(tag: str) -> AuthorityRef:
    return AuthorityRef(
        f"AUTH-{tag}",
        "1.0.0",
        semantic_hash({"authority": tag}),
    )


def _subject(
    tag: str,
    *,
    dependency_refs: tuple[ExactRef, ...] = (),
    determinant_refs: tuple[ExactRef, ...] | None = None,
    semantic_tag: str | None = None,
    materialization_class: str = "MANDATORY_RETAINED_CAPITAL",
    replay_state: str = "REPLAY_COMPLETE",
    selection_scope_ref: ExactRef | None = None,
    product_family_ref: ExactRef | None = None,
    release_kind: str = "LearnedProductRelease",
) -> LearnedProductLifecycleSubject:
    determinants = determinant_refs or (_ref("DETERMINANT", f"{tag}-D"),)
    semantic_hash_value = semantic_hash({"semantic": semantic_tag or tag})
    return LearnedProductLifecycleSubject(
        release_ref=_ref(release_kind, f"{tag}-release"),
        product_ref=_ref("LearnedSemanticProduct", f"{tag}-product"),
        product_family_ref=product_family_ref or _ref("ProductFamily", "family-A"),
        producer_owner_ref=_ref("ProducerOwner", f"{tag}-owner"),
        producer_contract_ref=_ref("ProducerContract", f"{tag}-contract"),
        semantic_projection_hash=semantic_hash_value,
        authority_snapshot_refs=(_auth(f"{tag}-semantic"),),
        direct_dependency_refs=dependency_refs,
        determinant_refs=determinants,
        determinant_set_hash=semantic_hash([ref.as_dict() for ref in sorted(set(determinants), key=lambda r: r.key)]),
        replay_root_ref=_ref("ReplayRoot", f"{tag}-replay"),
        selection_scope_ref=selection_scope_ref or _ref("SelectionScope", "scope-A"),
        build_or_release_receipt_refs=(_ref("BuildReceipt", f"{tag}-build"),),
        producer_permission_ceiling_ref=_ref("PermissionCeiling", f"{tag}-ceiling"),
        replay_state=replay_state,
        materialization_class=materialization_class,
    )


def _authority(tag: str = "life") -> ExactRef:
    return _ref("LifecycleAuthority", tag)


def _rule(tag: str = "rule") -> ExactRef:
    return _ref("LifecycleRule", tag)


def _attest(tag: str = "attest") -> ExactRef:
    return _ref("SelectionAttestation", tag)


def _register(
    executor: LearnedProductLifecycleExecutor,
    subject: LearnedProductLifecycleSubject,
    *,
    publish: bool = False,
) -> LearnedProductLifecycleSubject:
    executor.stage_release(subject)
    executor.register_product(
        subject.release_ref,
        event_authority_ref=_authority(f"register-{subject.release_ref.content_hash[:8]}"),
        event_rule_ref=_rule("register"),
    )
    if publish:
        executor.publish_product(
            subject.release_ref,
            event_authority_ref=_authority(f"publish-{subject.release_ref.content_hash[:8]}"),
            event_rule_ref=_rule("publish"),
        )
    return subject


def _key(
    executor: LearnedProductLifecycleExecutor,
    subject: LearnedProductLifecycleSubject,
    *,
    purpose: str = "serve",
    partition: str | None = None,
):
    return executor.selection_key(
        product_family_ref=subject.product_family_ref,
        selection_scope_ref=subject.selection_scope_ref,
        selection_purpose_ref=_ref("SelectionPurpose", purpose),
        consumer_context_partition_ref=(
            None if partition is None else _ref("ConsumerPartition", partition)
        ),
    )


def _select(
    executor: LearnedProductLifecycleExecutor,
    key,
    subject: LearnedProductLifecycleSubject,
    *,
    previous: ExactRef | None = None,
    tag: str = "select",
) -> CurrentSelectionReceipt:
    return executor.select_current(
        key.ref,
        subject.release_ref,
        expected_previous_receipt_ref=previous,
        event_authority_ref=_authority(tag),
        event_rule_ref=_rule(tag),
        selection_attestation_ref=_attest(tag),
    )


def test_h01_repository_presence_is_not_lifecycle_registration():
    executor = LearnedProductLifecycleExecutor()
    subject = _subject("repo-only")
    executor.stage_release(subject)

    assert executor.staged_release_refs == (subject.release_ref,)
    assert executor.registered_release_refs == ()
    with pytest.raises(LearnedProductLifecycleError, match="repository presence"):
        executor.lifecycle_state(subject.release_ref)


def test_h02_registration_is_not_publication():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("registered"))

    state = executor.lifecycle_state(subject.release_ref)
    assert state.registered is True
    assert state.publication == "UNPUBLISHED"
    assert executor.events[-1].event_kind == "PRODUCT_REGISTERED"


def test_h03_publication_is_not_current_selection():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("published"), publish=True)
    key = _key(executor, subject)

    assert executor.lifecycle_state(subject.release_ref).publication == "PUBLISHED"
    with pytest.raises(LearnedProductLifecycleError, match="UNKNOWN_CURRENTNESS"):
        executor.current_selection_receipt_ref(key.ref)


def test_h04_only_exact_selection_receipt_resolves_currentness():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("exact-current"), publish=True)
    key = _key(executor, subject)
    receipt = _select(executor, key, subject)

    resolved = executor.resolve_selection_exact(key.ref, receipt.ref)
    assert resolved.state == "CURRENT_SELECTED"
    assert resolved.selected_release_ref == subject.release_ref

    with pytest.raises(LearnedProductLifecycleError):
        executor.resolve_selection_exact(key.ref, _ref("CurrentSelectionReceipt", "wrong"))


def test_h05_no_latest_default_newest_semver_or_file_order_api_exists():
    executor = LearnedProductLifecycleExecutor()
    forbidden = (
        "resolve_latest",
        "resolve_default",
        "resolve_newest",
        "resolve_semver",
        "resolve_best_version",
        "select_latest",
        "auto_promote_on_release",
    )
    for name in forbidden:
        assert not hasattr(executor, name)


def test_h06_explicit_no_current_is_first_class_and_exact():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("no-current"), publish=True)
    key = _key(executor, subject)
    selected = _select(executor, key, subject)
    cleared = executor.declare_no_current(
        key.ref,
        expected_previous_receipt_ref=selected.ref,
        event_authority_ref=_authority("clear"),
        event_rule_ref=_rule("clear"),
        selection_attestation_ref=_attest("clear"),
        reason_ref=_ref("Reason", "maintenance-gap"),
    )

    assert isinstance(cleared, NoCurrentReceipt)
    resolved = executor.resolve_selection_exact(key.ref, cleared.ref)
    assert resolved.state == "NO_CURRENT"
    assert resolved.selected_release_ref is None
    assert executor.lifecycle_state(subject.release_ref).validity == "VALID"


def test_h07_recertification_does_not_silently_select():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("recert"), publish=True)
    key = _key(executor, subject)

    event = executor.record_recertification(
        subject.release_ref,
        event_authority_ref=_authority("recert"),
        event_rule_ref=_rule("recert"),
        attestation_ref=_ref("RecertificationAttestation", "recert"),
    )
    assert event.event_kind == "RECERTIFIES"
    with pytest.raises(LearnedProductLifecycleError, match="UNKNOWN_CURRENTNESS"):
        executor.current_selection_receipt_ref(key.ref)


def test_h08_b5_supersession_is_explicit_selection_transition_and_nondestructive():
    executor = LearnedProductLifecycleExecutor()
    scope = _ref("SelectionScope", "supersede")
    family = _ref("ProductFamily", "supersede")
    old = _register(
        executor,
        _subject("sup-old", selection_scope_ref=scope, product_family_ref=family),
        publish=True,
    )
    new = _register(
        executor,
        _subject("sup-new", selection_scope_ref=scope, product_family_ref=family),
        publish=True,
    )
    key = _key(executor, old)
    old_selection = _select(executor, key, old, tag="old")

    superseded = executor.supersede_current(
        key.ref,
        predecessor_release_ref=old.release_ref,
        successor_release_ref=new.release_ref,
        expected_previous_receipt_ref=old_selection.ref,
        event_authority_ref=_authority("supersede"),
        event_rule_ref=_rule("supersede"),
        selection_attestation_ref=_attest("supersede"),
        supersession_basis_ref=_ref("SupersessionBasis", "exact"),
    )

    assert executor.resolve_selection_exact(key.ref, superseded.ref).selected_release_ref == new.release_ref
    assert executor.lifecycle_state(old.release_ref).validity == "VALID"
    assert any(e.event_kind == "CURRENT_SUPERSEDED" for e in executor.release_history(new.release_ref))


def test_h09_current_withdrawal_requires_explicit_clear_or_replacement_and_preserves_history():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("withdraw"), publish=True)
    key = _key(executor, subject)
    current = _select(executor, key, subject)
    before = executor.export_checkpoint()["checkpoint_hash"]

    with pytest.raises(LearnedProductLifecycleError, match="every affected current"):
        executor.withdraw_product(
            subject.release_ref,
            withdrawal_reason_ref=_ref("WithdrawalReason", "reason"),
            withdrawal_scope_ref=subject.selection_scope_ref,
            event_authority_ref=_authority("withdraw"),
            event_rule_ref=_rule("withdraw"),
            selection_attestation_ref=_attest("withdraw"),
        )
    assert executor.export_checkpoint()["checkpoint_hash"] == before

    withdrawal = executor.withdraw_product(
        subject.release_ref,
        withdrawal_reason_ref=_ref("WithdrawalReason", "reason"),
        withdrawal_scope_ref=subject.selection_scope_ref,
        event_authority_ref=_authority("withdraw"),
        event_rule_ref=_rule("withdraw"),
        selection_attestation_ref=_attest("withdraw"),
        current_transitions={key.ref.key: None},
    )

    assert withdrawal.event_kind == "PRODUCT_WITHDRAWN"
    assert executor.lifecycle_state(subject.release_ref).validity == "WITHDRAWN"
    selection_ref = executor.current_selection_receipt_ref(key.ref)
    assert executor.resolve_selection_exact(key.ref, selection_ref).state == "NO_CURRENT"
    assert any(e.event_kind == "CURRENT_SELECTED" for e in executor.release_history(subject.release_ref))


def test_h10_stale_concurrent_selection_conflict_fails_closed_without_mutation():
    executor = LearnedProductLifecycleExecutor()
    scope = _ref("SelectionScope", "conflict")
    family = _ref("ProductFamily", "conflict")
    a = _register(executor, _subject("conflict-a", selection_scope_ref=scope, product_family_ref=family), publish=True)
    b = _register(executor, _subject("conflict-b", selection_scope_ref=scope, product_family_ref=family), publish=True)
    key = _key(executor, a)
    first = _select(executor, key, a, tag="first")
    before = executor.export_checkpoint()["checkpoint_hash"]

    with pytest.raises(LearnedProductLifecycleConflict, match="CONFLICTING_CURRENT_SELECTION"):
        _select(executor, key, b, previous=None, tag="stale")

    assert executor.export_checkpoint()["checkpoint_hash"] == before
    assert executor.resolve_selection_exact(key.ref, first.ref).selected_release_ref == a.release_ref


def test_h11_historical_current_as_of_uses_exact_event_not_git_time():
    executor = LearnedProductLifecycleExecutor()
    scope = _ref("SelectionScope", "asof")
    family = _ref("ProductFamily", "asof")
    a = _register(executor, _subject("asof-a", selection_scope_ref=scope, product_family_ref=family), publish=True)
    b = _register(executor, _subject("asof-b", selection_scope_ref=scope, product_family_ref=family), publish=True)
    key = _key(executor, a)
    r1 = _select(executor, key, a, tag="asof-a")
    event1 = next(e for e in executor.events if e.ref == r1.current_select_event_ref)
    r2 = _select(executor, key, b, previous=r1.ref, tag="asof-b")

    historical = executor.resolve_current_as_of(key.ref, as_of_event_ref=event1.ref)
    assert historical.state == "CURRENT_SELECTED"
    assert historical.selected_release_ref == a.release_ref
    assert executor.resolve_selection_exact(key.ref, r2.ref).selected_release_ref == b.release_ref


def test_h12_determinant_local_invalidation_reaches_direct_and_transitive_only():
    executor = LearnedProductLifecycleExecutor()
    determinant = _ref("SemanticDeterminant", "D")
    unrelated_determinant = _ref("SemanticDeterminant", "U")
    a = _register(executor, _subject("inv-a", determinant_refs=(determinant,)), publish=True)
    b = _register(
        executor,
        _subject("inv-b", dependency_refs=(a.product_ref,), determinant_refs=(_ref("SemanticDeterminant", "B"),)),
        publish=True,
    )
    c = _register(executor, _subject("inv-c", determinant_refs=(unrelated_determinant,)), publish=True)

    receipt = executor.declare_invalidation(
        (determinant,),
        event_authority_ref=_authority("invalidate"),
        event_rule_ref=_rule("invalidate"),
        dependency_closure_receipt_ref=_ref("DependencyClosure", "inv"),
        selection_attestation_ref=_attest("invalidate"),
        current_transitions={},
    )

    assert set(receipt.directly_affected_release_refs) == {a.release_ref}
    assert set(receipt.transitively_affected_release_refs) == {b.release_ref}
    assert set(receipt.unaffected_product_refs) == {c.product_ref}
    assert executor.lifecycle_state(a.release_ref).validity == "INVALIDATED_REBUILD_REQUIRED"
    assert executor.lifecycle_state(b.release_ref).validity == "INVALIDATED_REBUILD_REQUIRED"
    assert executor.lifecycle_state(c.release_ref).validity == "VALID"


def test_h13_unrelated_same_family_product_remains_unaffected():
    executor = LearnedProductLifecycleExecutor()
    d1 = _ref("SemanticDeterminant", "same-family-1")
    d2 = _ref("SemanticDeterminant", "same-family-2")
    a = _register(executor, _subject("same-a", determinant_refs=(d1,)))
    b = _register(executor, _subject("same-b", determinant_refs=(d2,)))

    executor.declare_invalidation(
        (d1,),
        event_authority_ref=_authority("same"),
        event_rule_ref=_rule("same"),
        dependency_closure_receipt_ref=_ref("DependencyClosure", "same"),
        selection_attestation_ref=_attest("same"),
        current_transitions={},
    )
    assert executor.lifecycle_state(a.release_ref).validity == "INVALIDATED_REBUILD_REQUIRED"
    assert executor.lifecycle_state(b.release_ref).validity == "VALID"


def test_h14_optional_cache_loss_changes_performance_materialization_only():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(
        executor,
        _subject("cache", materialization_class="OPTIONAL_CACHE_ACCELERATOR"),
        publish=True,
    )
    key = _key(executor, subject)
    current = _select(executor, key, subject)
    before = executor.lifecycle_state(subject.release_ref)

    executor.record_cache_dropped(
        subject.release_ref,
        cache_ref=_ref("Cache", "cache"),
        event_authority_ref=_authority("cache-drop"),
        event_rule_ref=_rule("cache-drop"),
    )
    after = executor.lifecycle_state(subject.release_ref)

    assert before.validity == after.validity == "VALID"
    assert before.publication == after.publication == "PUBLISHED"
    assert after.payload_materialized is False
    assert executor.resolve_selection_exact(key.ref, current.ref).selected_release_ref == subject.release_ref


def test_h15_semantic_change_on_rebuild_requires_new_upstream_product_identity():
    executor = LearnedProductLifecycleExecutor()
    old = _register(executor, _subject("rebuild-old", semantic_tag="old"))
    changed = _subject("rebuild-new", semantic_tag="new")
    changed_same_product = LearnedProductLifecycleSubject(
        **{**changed.__dict__, "product_ref": old.product_ref}
    )

    # The B5 owner refuses the contradiction at the earliest lawful boundary:
    # a changed semantic projection cannot even be staged under the old product id.
    with pytest.raises(LearnedProductLifecycleConflict, match="same product_ref"):
        executor.stage_release(changed_same_product)


def test_h16_missing_rebuild_inputs_yield_typed_blocker_not_fabricated_successor():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("rebuild-blocked"))

    receipt = executor.record_rebuild_eligibility(
        subject.release_ref,
        event_authority_ref=_authority("rebuild-block"),
        event_rule_ref=_rule("rebuild-block"),
        execution_mechanism_ref=None,
        source_or_upstream_refs=(),
    )
    assert receipt.rebuild_state == "REBUILD_BLOCKED"
    assert "REBUILD_NOT_PROVED" in receipt.blocker_states
    assert executor.lifecycle_state(subject.release_ref).rebuild == "REBUILD_BLOCKED"


def test_h17_gc_only_for_proven_recomputable_payload_never_mandatory_history():
    executor = LearnedProductLifecycleExecutor()
    recomputable = _register(
        executor,
        _subject(
            "gc-ok",
            dependency_refs=(_ref("SourceRelease", "gc-ok-source"),),
            materialization_class="RECOMPUTABLE_PRODUCT_PAYLOAD",
        ),
    )
    mandatory = _register(
        executor,
        _subject("gc-no", materialization_class="MANDATORY_RETAINED_CAPITAL"),
    )
    executor.record_rebuild_eligibility(
        recomputable.release_ref,
        event_authority_ref=_authority("gc-rebuild"),
        event_rule_ref=_rule("gc-rebuild"),
        execution_mechanism_ref=_ref("ExecutionMechanism", "gc"),
        source_or_upstream_refs=(_ref("SourceRelease", "gc-ok-source"),),
    )

    receipt = executor.attest_gc_eligibility(
        recomputable.release_ref,
        reconstruction_proof_ref=_ref("Proof", "reconstruct"),
        historical_retention_proof_ref=_ref("Proof", "history"),
        serving_reconstruction_proof_ref=_ref("Proof", "serve"),
        downstream_byte_dependency_absence_proof_ref=_ref("Proof", "no-byte-dep"),
        source_carrier_retention_proof_ref=_ref("Proof", "source-retained"),
        event_authority_ref=_authority("gc"),
        event_rule_ref=_rule("gc"),
    )
    assert isinstance(receipt, GCElegibilityReceipt)
    assert receipt.source_carrier_retirement_authorized_false is True

    executor.record_payload_gc(
        receipt.ref,
        event_authority_ref=_authority("gc-record"),
        event_rule_ref=_rule("gc-record"),
    )
    assert executor.lifecycle_state(recomputable.release_ref).payload_materialized is False

    with pytest.raises(LearnedProductLifecycleError, match="GC_NOT_AUTHORIZED"):
        executor.attest_gc_eligibility(
            mandatory.release_ref,
            reconstruction_proof_ref=_ref("Proof", "m-reconstruct"),
            historical_retention_proof_ref=_ref("Proof", "m-history"),
            serving_reconstruction_proof_ref=_ref("Proof", "m-serve"),
            downstream_byte_dependency_absence_proof_ref=_ref("Proof", "m-no-byte"),
            source_carrier_retention_proof_ref=_ref("Proof", "m-source"),
            event_authority_ref=_authority("m-gc"),
            event_rule_ref=_rule("m-gc"),
        )


def test_h18_runtime_exposes_no_source_or_carrier_retirement_authority():
    executor = LearnedProductLifecycleExecutor()
    for name in (
        "retire_source",
        "retire_carrier",
        "authorize_cutover",
        "delete_source_snapshot",
        "grant_retirement_credit",
    ):
        assert not hasattr(executor, name)


@pytest.mark.parametrize("kind", ["AuthoritySnapshot", "AuthoritySnapshot@1.0.0"])
def test_h19_authority_snapshot_cannot_alias_learned_product_release(kind: str):
    base = _subject("authority-alias")
    with pytest.raises(LearnedProductLifecycleError, match="cannot alias"):
        LearnedProductLifecycleSubject(
            **{
                **base.__dict__,
                "release_ref": _ref(kind, "bad"),
            }
        )


def test_h20_authority_release_receipt_cannot_alias_lifecycle_current_receipt():
    base = _subject("authority-release-alias")
    with pytest.raises(LearnedProductLifecycleError, match="cannot alias"):
        LearnedProductLifecycleSubject(
            **{
                **base.__dict__,
                "release_ref": _ref("AuthorityReleaseReceipt", "bad"),
            }
        )
    assert CurrentSelectionReceipt is not NoCurrentReceipt


def test_h21_currentness_does_not_create_consumer_permission_api():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("permission"), publish=True)
    key = _key(executor, subject, partition="consumer-x")
    receipt = _select(executor, key, subject)
    assert executor.resolve_selection_exact(key.ref, receipt.ref).state == "CURRENT_SELECTED"
    for name in ("grant_permission", "authorize_consumer", "permit_target_use"):
        assert not hasattr(executor, name)


def test_h22_checkpoint_restart_and_replay_identity_are_exact():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("checkpoint"), publish=True)
    key = _key(executor, subject)
    selected = _select(executor, key, subject, tag="checkpoint")
    executor.record_recertification(
        subject.release_ref,
        event_authority_ref=_authority("checkpoint-recert"),
        event_rule_ref=_rule("checkpoint-recert"),
        attestation_ref=_ref("RecertificationAttestation", "checkpoint"),
    )
    executor.declare_no_current(
        key.ref,
        expected_previous_receipt_ref=selected.ref,
        event_authority_ref=_authority("checkpoint-clear"),
        event_rule_ref=_rule("checkpoint-clear"),
        selection_attestation_ref=_attest("checkpoint-clear"),
        reason_ref=_ref("Reason", "checkpoint-clear"),
    )

    checkpoint = executor.export_checkpoint()
    restored = LearnedProductLifecycleExecutor.from_checkpoint(checkpoint)
    assert restored.export_checkpoint()["checkpoint_hash"] == checkpoint["checkpoint_hash"]
    assert restored.events == executor.events

    replay = executor.audit_replay()
    assert replay.replay_state == "REPLAY_VERIFIED"
    assert replay.original_checkpoint_hash == replay.replayed_checkpoint_hash


def test_h23_failed_selection_is_atomic_and_does_not_expose_half_state():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("atomic"), publish=False)
    key = _key(executor, subject)
    before = executor.export_checkpoint()["checkpoint_hash"]

    with pytest.raises(LearnedProductLifecycleError, match="publication lifecycle"):
        _select(executor, key, subject)

    assert executor.export_checkpoint()["checkpoint_hash"] == before
    with pytest.raises(LearnedProductLifecycleError, match="UNKNOWN_CURRENTNESS"):
        executor.current_selection_receipt_ref(key.ref)


def test_h24_b5_machine_rule_event_parity_and_required_common_fields():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("parity"), publish=True)
    key = _key(executor, subject)
    _select(executor, key, subject)

    for event in executor.events:
        assert event.event_kind in B5_EVENT_KINDS
        exported = event.as_dict()
        for required in (
            "event_kind",
            "product_ref",
            "selection_scope_ref",
            "event_authority_ref",
            "event_rule_ref",
            "parent_lifecycle_event_ref",
            "evidence_refs",
            "event_content_hash",
        ):
            assert required in exported
        assert exported["event_content_hash"] == event.ref.content_hash
    assert LIFECYCLE_CONTRACT_ID == "PRE553_LEARNED_PRODUCT_LIFECYCLE_CANDIDATE@1.0.0"


def test_publication_requires_exact_replay_closure():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(
        executor,
        _subject("bad-replay", replay_state="REPLAY_BLOCKED_MISSING_DETERMINANT"),
    )
    with pytest.raises(LearnedProductLifecycleError, match="MISSING_REPLAY_CLOSURE"):
        executor.publish_product(
            subject.release_ref,
            event_authority_ref=_authority("bad-publish"),
            event_rule_ref=_rule("bad-publish"),
        )


def test_two_selection_purposes_can_hold_distinct_current_releases():
    executor = LearnedProductLifecycleExecutor()
    scope = _ref("SelectionScope", "purposes")
    family = _ref("ProductFamily", "purposes")
    a = _register(executor, _subject("purpose-a", selection_scope_ref=scope, product_family_ref=family), publish=True)
    b = _register(executor, _subject("purpose-b", selection_scope_ref=scope, product_family_ref=family), publish=True)
    serve = _key(executor, a, purpose="serve")
    audit = _key(executor, a, purpose="audit")
    rs = _select(executor, serve, a, tag="serve")
    ra = _select(executor, audit, b, tag="audit")

    assert executor.resolve_selection_exact(serve.ref, rs.ref).selected_release_ref == a.release_ref
    assert executor.resolve_selection_exact(audit.ref, ra.ref).selected_release_ref == b.release_ref


def test_selection_scope_cannot_bleed_to_other_scope():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("scope-bleed"), publish=True)
    wrong = executor.selection_key(
        product_family_ref=subject.product_family_ref,
        selection_scope_ref=_ref("SelectionScope", "other"),
        selection_purpose_ref=_ref("SelectionPurpose", "serve"),
    )
    with pytest.raises(LearnedProductLifecycleError, match="scope mismatch"):
        _select(executor, wrong, subject)


def test_current_invalidation_requires_explicit_no_current_or_replacement_atomically():
    executor = LearnedProductLifecycleExecutor()
    determinant = _ref("SemanticDeterminant", "current-inv")
    subject = _register(executor, _subject("current-inv", determinant_refs=(determinant,)), publish=True)
    key = _key(executor, subject)
    current = _select(executor, key, subject)
    before = executor.export_checkpoint()["checkpoint_hash"]

    with pytest.raises(LearnedProductLifecycleError, match="current invalidation"):
        executor.declare_invalidation(
            (determinant,),
            event_authority_ref=_authority("current-inv"),
            event_rule_ref=_rule("current-inv"),
            dependency_closure_receipt_ref=_ref("DependencyClosure", "current-inv"),
            selection_attestation_ref=_attest("current-inv"),
            current_transitions={},
        )
    assert executor.export_checkpoint()["checkpoint_hash"] == before
    assert executor.resolve_selection_exact(key.ref, current.ref).state == "CURRENT_SELECTED"

    receipt = executor.declare_invalidation(
        (determinant,),
        event_authority_ref=_authority("current-inv"),
        event_rule_ref=_rule("current-inv"),
        dependency_closure_receipt_ref=_ref("DependencyClosure", "current-inv"),
        selection_attestation_ref=_attest("current-inv"),
        current_transitions={key.ref.key: None},
    )
    assert subject.product_ref in receipt.affected_product_refs
    no_current_ref = executor.current_selection_receipt_ref(key.ref)
    assert executor.resolve_selection_exact(key.ref, no_current_ref).state == "NO_CURRENT"


def test_unrelated_changed_determinant_produces_exact_noop_invalidation():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("noop"))
    before = executor.lifecycle_state(subject.release_ref)
    receipt = executor.declare_invalidation(
        (_ref("SemanticDeterminant", "unrelated"),),
        event_authority_ref=_authority("noop"),
        event_rule_ref=_rule("noop"),
        dependency_closure_receipt_ref=_ref("DependencyClosure", "noop"),
        selection_attestation_ref=_attest("noop"),
        current_transitions={},
    )
    assert receipt.affected_product_refs == ()
    assert executor.lifecycle_state(subject.release_ref) == before


def test_cache_operations_are_rejected_for_semantic_product_payload_classes():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("not-cache"))
    with pytest.raises(LearnedProductLifecycleError, match="OPTIONAL_CACHE_ACCELERATOR"):
        executor.record_cache_dropped(
            subject.release_ref,
            cache_ref=_ref("Cache", "not-cache"),
            event_authority_ref=_authority("not-cache"),
            event_rule_ref=_rule("not-cache"),
        )


def test_gc_receipt_cannot_claim_source_carrier_retirement():
    with pytest.raises(LearnedProductLifecycleError, match="cannot authorize"):
        GCElegibilityReceipt(
            release_ref=_ref("LearnedProductRelease", "gc-illegal"),
            materialization_class="RECOMPUTABLE_PRODUCT_PAYLOAD",
            reconstruction_proof_ref=_ref("Proof", "a"),
            historical_retention_proof_ref=_ref("Proof", "b"),
            serving_reconstruction_proof_ref=_ref("Proof", "c"),
            downstream_byte_dependency_absence_proof_ref=_ref("Proof", "d"),
            source_carrier_retention_proof_ref=_ref("Proof", "e"),
            source_carrier_retirement_authorized_false=False,
            event_ref=_ref("B5Lifecycle:EVENT", "gc"),
        )


@dataclass(frozen=True)
class _FakeM2Adapter:
    release_ref: ExactRef
    product_ref: ExactRef
    product_family_ref: ExactRef
    producer_owner_ref: ExactRef
    producer_contract_ref: ExactRef
    semantic_projection_hash: str
    authority_snapshot_refs: tuple[AuthorityRef, ...]
    direct_dependency_refs: tuple[ExactRef, ...]
    determinant_refs: tuple[ExactRef, ...]
    determinant_set_hash: str
    replay_root_ref: ExactRef
    selection_scope_ref: ExactRef
    build_or_release_receipt_refs: tuple[ExactRef, ...]
    producer_permission_ceiling_ref: ExactRef


def test_m2_interface_is_narrow_protocol_not_release_core_reimplementation():
    original = _subject("protocol")
    fake = _FakeM2Adapter(
        release_ref=original.release_ref,
        product_ref=original.product_ref,
        product_family_ref=original.product_family_ref,
        producer_owner_ref=original.producer_owner_ref,
        producer_contract_ref=original.producer_contract_ref,
        semantic_projection_hash=original.semantic_projection_hash,
        authority_snapshot_refs=original.authority_snapshot_refs,
        direct_dependency_refs=original.direct_dependency_refs,
        determinant_refs=original.determinant_refs,
        determinant_set_hash=original.determinant_set_hash,
        replay_root_ref=original.replay_root_ref,
        selection_scope_ref=original.selection_scope_ref,
        build_or_release_receipt_refs=original.build_or_release_receipt_refs,
        producer_permission_ceiling_ref=original.producer_permission_ceiling_ref,
    )
    executor = LearnedProductLifecycleExecutor()
    staged = executor.stage_protocol(fake)
    assert staged == original
    assert executor.registered_release_refs == ()


def test_unknown_currentness_never_selects_only_or_newest_release():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("unknown"), publish=True)
    key = _key(executor, subject)
    with pytest.raises(LearnedProductLifecycleError, match="UNKNOWN_CURRENTNESS"):
        executor.current_selection_receipt_ref(key.ref)


def test_withdrawal_can_atomically_replace_current_with_other_lawful_product():
    executor = LearnedProductLifecycleExecutor()
    scope = _ref("SelectionScope", "withdraw-replace")
    family = _ref("ProductFamily", "withdraw-replace")
    old = _register(executor, _subject("wr-old", selection_scope_ref=scope, product_family_ref=family), publish=True)
    replacement = _register(executor, _subject("wr-new", selection_scope_ref=scope, product_family_ref=family), publish=True)
    key = _key(executor, old)
    current = _select(executor, key, old, tag="wr-old")

    executor.withdraw_product(
        old.release_ref,
        withdrawal_reason_ref=_ref("WithdrawalReason", "wr"),
        withdrawal_scope_ref=scope,
        event_authority_ref=_authority("wr"),
        event_rule_ref=_rule("wr"),
        selection_attestation_ref=_attest("wr"),
        current_transitions={key.ref.key: replacement.release_ref},
    )

    new_receipt_ref = executor.current_selection_receipt_ref(key.ref)
    assert new_receipt_ref != current.ref
    assert executor.resolve_selection_exact(key.ref, new_receipt_ref).selected_release_ref == replacement.release_ref
    assert executor.lifecycle_state(old.release_ref).validity == "WITHDRAWN"
    assert executor.lifecycle_state(replacement.release_ref).validity == "VALID"


def test_select_after_explicit_no_current_requires_and_accepts_exact_no_current_receipt():
    executor = LearnedProductLifecycleExecutor()
    scope = _ref("SelectionScope", "after-no-current")
    family = _ref("ProductFamily", "after-no-current")
    a = _register(executor, _subject("anc-a", selection_scope_ref=scope, product_family_ref=family), publish=True)
    b = _register(executor, _subject("anc-b", selection_scope_ref=scope, product_family_ref=family), publish=True)
    key = _key(executor, a)
    selected = _select(executor, key, a, tag="anc-a")
    cleared = executor.declare_no_current(
        key.ref,
        expected_previous_receipt_ref=selected.ref,
        event_authority_ref=_authority("anc-clear"),
        event_rule_ref=_rule("anc-clear"),
        selection_attestation_ref=_attest("anc-clear"),
        reason_ref=_ref("Reason", "anc-clear"),
    )
    reselected = _select(executor, key, b, previous=cleared.ref, tag="anc-b")
    assert executor.resolve_selection_exact(key.ref, reselected.ref).selected_release_ref == b.release_ref


def test_withdrawn_release_cannot_replace_itself_current():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("withdraw-self"), publish=True)
    key = _key(executor, subject)
    _select(executor, key, subject)
    before = executor.export_checkpoint()["checkpoint_hash"]
    with pytest.raises(LearnedProductLifecycleError, match="cannot be its own"):
        executor.withdraw_product(
            subject.release_ref,
            withdrawal_reason_ref=_ref("WithdrawalReason", "self"),
            withdrawal_scope_ref=subject.selection_scope_ref,
            event_authority_ref=_authority("withdraw-self"),
            event_rule_ref=_rule("withdraw-self"),
            selection_attestation_ref=_attest("withdraw-self"),
            current_transitions={key.ref.key: subject.release_ref},
        )
    assert executor.export_checkpoint()["checkpoint_hash"] == before


def test_invalidated_release_cannot_be_selected_as_its_own_replacement():
    executor = LearnedProductLifecycleExecutor()
    determinant = _ref("SemanticDeterminant", "invalid-self")
    subject = _register(executor, _subject("invalid-self", determinant_refs=(determinant,)), publish=True)
    key = _key(executor, subject)
    _select(executor, key, subject)
    before = executor.export_checkpoint()["checkpoint_hash"]
    with pytest.raises(LearnedProductLifecycleError, match="invalidated release"):
        executor.declare_invalidation(
            (determinant,),
            event_authority_ref=_authority("invalid-self"),
            event_rule_ref=_rule("invalid-self"),
            dependency_closure_receipt_ref=_ref("DependencyClosure", "invalid-self"),
            selection_attestation_ref=_attest("invalid-self"),
            current_transitions={key.ref.key: subject.release_ref},
        )
    assert executor.export_checkpoint()["checkpoint_hash"] == before


def test_lcr009_authority_change_routes_as_explicit_neutral_determinant():
    executor = LearnedProductLifecycleExecutor()
    subject = _register(executor, _subject("authority-determinant"))
    changed_authority = subject.authority_snapshot_refs[0]

    receipt = executor.declare_invalidation(
        (changed_authority,),
        event_authority_ref=_authority("authority-change"),
        event_rule_ref=_rule("authority-change"),
        dependency_closure_receipt_ref=_ref("DependencyClosure", "authority-change"),
        selection_attestation_ref=_attest("authority-change"),
        current_transitions={},
    )

    assert receipt.directly_affected_release_refs == (subject.release_ref,)
    assert executor.lifecycle_state(subject.release_ref).validity == "INVALIDATED_REBUILD_REQUIRED"
    assert not hasattr(executor, "promote_authority")
