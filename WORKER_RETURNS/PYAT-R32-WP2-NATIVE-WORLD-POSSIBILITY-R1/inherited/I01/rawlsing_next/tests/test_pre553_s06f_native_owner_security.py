"""S06F source-free native B5/M2 regression fixtures.

These tests do NOT establish external issuer, protected CURRENT, source rights,
or independent acceptance. Frozen S06R acceptance expectations are unmodified.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from inspect import getsource

import pytest

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash
from rawlsing_next.pre553_learned_product_lifecycle import (
    LearnedProductLifecycleConflict, LearnedProductLifecycleError,
    LearnedProductLifecycleExecutor, LearnedProductLifecycleSubject,
    LearnedProductLifecycleEvent,
)
from rawlsing_next.pre553_learned_product_release import (
    M2ReleaseError, M2Repository, ReleaseCore, RepresentationRecord,
    PublicationBinding, M2_RELEASE_CONTRACT_REF, M2_PUBLICATION_CONTRACT_REF,
    register_producer_subject, constitute_closure, constitute_release,
    register_representation, publish_binding,
)


def ref(kind: str, tag: str) -> ExactRef:
    digest = semantic_hash({"kind": kind, "tag": tag})
    return ExactRef(kind, f"urn:test:{kind}:{tag}:sha256:{digest}", digest)


def subject(tag: str, *, dependency=(), family=None, scope=None):
    determinant = ref("DETERMINANT", f"{tag}-det")
    return LearnedProductLifecycleSubject(
        release_ref=ref("LearnedProductRelease", tag),
        product_ref=ref("LearnedProduct", tag),
        product_family_ref=family or ref("ProductFamily", "shared"),
        producer_owner_ref=ref("ProducerOwner", tag),
        producer_contract_ref=ref("ProducerContract", tag),
        semantic_projection_hash=semantic_hash({"semantic": tag}),
        authority_snapshot_refs=(AuthorityRef(f"AUTH-{tag}", "1.0.0", semantic_hash(tag)),),
        direct_dependency_refs=tuple(dependency),
        determinant_refs=(determinant,),
        determinant_set_hash=semantic_hash([determinant.as_dict()]),
        replay_root_ref=ref("ReplayRoot", tag),
        selection_scope_ref=scope or ref("SelectionScope", "shared"),
        build_or_release_receipt_refs=(ref("BuildReceipt", tag),),
        producer_permission_ceiling_ref=ref("PermissionCeiling", tag),
        replay_state="REPLAY_COMPLETE",
    )


def register(executor, obj, *, publish=False):
    executor.stage_release(obj)
    executor.register_product(
        obj.release_ref,
        event_authority_ref=ref("EventAuthority", f"reg-{obj.release_ref.object_id}"),
        event_rule_ref=ref("EventRule", "register"),
    )
    if publish:
        executor.publish_product(
            obj.release_ref,
            event_authority_ref=ref("EventAuthority", "publish"),
            event_rule_ref=ref("EventRule", "publish"),
        )
    return obj


def checkpoint_with_publication():
    executor = LearnedProductLifecycleExecutor()
    item = register(executor, subject("x"), publish=True)
    return executor, item, executor.export_checkpoint()


def m2_fixture():
    repo = M2Repository()
    producer = ref("ProducerContract", "m2-producer")
    source = ref("LearnedEmpiricalDisposition", "m2-source")
    required = {
        "AUTHORITY": ref("Authority", "m2-auth"),
        "DEPENDENCY": ref("Dependency", "m2-dep"),
        "DETERMINANT": ref("Determinant", "m2-det"),
        "REPLAY_RECONSTRUCTION": ref("ReplayDeterminant", "m2-replay"),
        "EXPLANATION_LINEAGE": ref("ExplanationNode", "m2-explain"),
    }
    register_producer_subject(
        repo, subject_ref=source, subject_kind="TYPED_DISPOSITION",
        producer_contract_ref=producer, typed_state="SUPPORTED",
        required_authority_refs=(required["AUTHORITY"],),
        required_dependency_refs=(required["DEPENDENCY"],),
        required_determinant_refs=(required["DETERMINANT"],),
        required_replay_refs=(required["REPLAY_RECONSTRUCTION"],),
        required_explanation_refs=(required["EXPLANATION_LINEAGE"],),
    )
    members = {
        "AUTHORITY": (producer, required["AUTHORITY"]),
        "DEPENDENCY": (required["DEPENDENCY"],),
        "DETERMINANT": (required["DETERMINANT"],),
        "REPLAY_RECONSTRUCTION": (required["REPLAY_RECONSTRUCTION"],),
        "EXPLANATION_LINEAGE": (source, producer, required["EXPLANATION_LINEAGE"]),
    }
    closures = {
        kind: constitute_closure(
            repo, closure_kind=kind, member_refs=mem,
            metadata={"replay_grade": "EXACT_DETERMINISTIC_REBUILD"}
            if kind == "REPLAY_RECONSTRUCTION" else None,
        )
        for kind, mem in members.items()
    }
    release = constitute_release(
        repo, release_subject_ref=source, release_subject_kind="TYPED_DISPOSITION",
        semantic_producer_contract_ref=producer,
        authority_closure_ref=closures["AUTHORITY"].ref,
        dependency_closure_ref=closures["DEPENDENCY"].ref,
        determinant_closure_ref=closures["DETERMINANT"].ref,
        replay_reconstruction_ref=closures["REPLAY_RECONSTRUCTION"].ref,
        explanation_lineage_ref=closures["EXPLANATION_LINEAGE"].ref,
    )
    return repo, release, source, producer, closures


def test_b5_valid_native_checkpoint_local_roundtrip():
    executor, item, cp = checkpoint_with_publication()
    restored = LearnedProductLifecycleExecutor.from_checkpoint(cp)
    assert restored.export_checkpoint()["checkpoint_hash"] == cp["checkpoint_hash"]
    assert restored.lifecycle_state(item.release_ref).publication == "PUBLISHED"
    assert restored.native_security_mode == "LOCAL_UNAUTHENTICATED"


@pytest.mark.parametrize("alteration", ["truncate_published", "alter_publication", "drop_registered"])
def test_b5_native_checkpoint_rejects_self_rehashed_inconsistent_state(alteration):
    _, _, cp = checkpoint_with_publication()
    forged = deepcopy(cp)
    payload = forged["checkpoint_payload"]
    if alteration == "truncate_published":
        payload["events"].pop()
    elif alteration == "alter_publication":
        payload["publication"][0] = (payload["publication"][0][0], "UNPUBLISHED")
    else:
        payload["registered_release_refs"].clear()
    forged["checkpoint_hash"] = semantic_hash(payload)
    with pytest.raises((LearnedProductLifecycleConflict, LearnedProductLifecycleError)):
        LearnedProductLifecycleExecutor.from_checkpoint(forged)


def test_b5_typed_unknown_event_rejected_before_append():
    executor, item, _ = checkpoint_with_publication()
    before = executor.export_checkpoint()["checkpoint_hash"]
    with pytest.raises(LearnedProductLifecycleError, match="unknown lifecycle event"):
        LearnedProductLifecycleEvent(
            ordinal=3, event_kind="UNISSUED_EVENT", release_ref=item.release_ref,
            product_ref=item.product_ref, selection_scope_ref=item.selection_scope_ref,
            event_authority_ref=ref("EventAuthority", "x"), event_rule_ref=ref("EventRule", "x"),
            parent_lifecycle_event_ref=executor.events[-1].ref,
        )
    assert executor.export_checkpoint()["checkpoint_hash"] == before


def test_b5_transitive_determinants_and_unaffected_sibling():
    executor = LearnedProductLifecycleExecutor()
    a = register(executor, subject("a"))
    b = register(executor, subject("b", dependency=(a.release_ref,)))
    c = register(executor, subject("c", dependency=(b.release_ref,)))
    sibling = register(executor, subject("sibling"))
    result = executor.declare_invalidation(
        a.determinant_refs, event_authority_ref=ref("EventAuthority", "invalidate"),
        event_rule_ref=ref("EventRule", "invalidate"),
        dependency_closure_receipt_ref=ref("DependencyClosure", "chain"),
        selection_attestation_ref=ref("SelectionAttestation", "chain"),
    )
    assert a.release_ref in result.directly_affected_release_refs
    assert b.release_ref in result.transitively_affected_release_refs
    assert c.release_ref in result.transitively_affected_release_refs
    assert sibling.release_ref in result.unaffected_product_refs or (
        sibling.product_ref in result.unaffected_product_refs
    )
    assert executor.lifecycle_state(c.release_ref).validity == "INVALIDATED_REBUILD_REQUIRED"
    assert executor.lifecycle_state(sibling.release_ref).validity == "VALID"
    restored = LearnedProductLifecycleExecutor.from_checkpoint(executor.export_checkpoint())
    assert restored.lifecycle_state(c.release_ref).validity == "INVALIDATED_REBUILD_REQUIRED"


def test_b5_no_current_subject_must_match_family_scope():
    executor = LearnedProductLifecycleExecutor()
    a = register(executor, subject("a", scope=ref("SelectionScope", "a")))
    b = register(executor, subject("b", scope=ref("SelectionScope", "b")))
    key = executor.selection_key(
        product_family_ref=a.product_family_ref,
        selection_scope_ref=a.selection_scope_ref,
        selection_purpose_ref=ref("SelectionPurpose", "serve"),
    )
    with pytest.raises(LearnedProductLifecycleError, match="subject family/scope mismatch"):
        executor.declare_no_current(
            key.ref, expected_previous_receipt_ref=None,
            event_authority_ref=ref("EventAuthority", "clear"),
            event_rule_ref=ref("EventRule", "clear"),
            selection_attestation_ref=ref("SelectionAttestation", "clear"),
            reason_ref=ref("Reason", "clear"),
            subject_release_ref=b.release_ref,
        )


def test_b5_protected_current_and_external_custody_are_explicit_holds():
    executor = LearnedProductLifecycleExecutor()
    with pytest.raises(LearnedProductLifecycleError, match="EXTERNAL_ISSUER_HOLD"):
        executor.require_external_issuer("PROTECTED_CURRENT")
    with pytest.raises(LearnedProductLifecycleError, match="EXTERNAL_ISSUER_HOLD"):
        executor.require_external_issuer("EXTERNAL_CUSTODY")
    saved = LearnedProductLifecycleExecutor.stage_release
    executor._native_security_mode = "PROTECTED_CURRENT"
    with pytest.raises(LearnedProductLifecycleError, match="EXTERNAL_ISSUER_HOLD"):
        saved(executor, subject("guarded"))


def test_native_b5_all_mutators_have_in_body_preflight():
    methods = (
        "stage_release", "stage_protocol", "register_product", "publish_product",
        "record_recertification", "selection_key", "select_current",
        "declare_no_current", "supersede_current", "withdraw_product",
        "declare_invalidation", "record_rebuild_eligibility", "link_rebuild",
        "record_cache_materialized", "record_cache_dropped",
        "attest_gc_eligibility", "record_payload_gc",
    )
    for name in methods:
        assert f'self._native_mutation_preflight("{name}")' in getsource(
            getattr(LearnedProductLifecycleExecutor, name)
        )


def test_m2_direct_release_registration_requires_native_subject():
    repo = M2Repository()
    foreign = ref("TEST", "unbound")
    bogus = ReleaseCore(
        release_contract_ref=M2_RELEASE_CONTRACT_REF,
        release_subject_ref=foreign, release_subject_kind="TYPED_DISPOSITION",
        semantic_producer_contract_ref=ref("ProducerContract", "x"),
        authority_closure_ref=foreign, dependency_closure_ref=foreign,
        determinant_closure_ref=foreign, replay_reconstruction_ref=foreign,
        explanation_lineage_ref=foreign,
    )
    with pytest.raises(M2ReleaseError):
        M2Repository.register_release(repo, bogus)
    assert not repo.releases


def test_m2_native_valid_release_and_direct_representation_binding():
    repo, release, source, producer, _ = m2_fixture()
    assert repo.release_exact(release.ref) == release
    location = ref("RepresentationLocator", "native")
    integrity = ref("RepresentationIntegrity", "native")
    record = RepresentationRecord(
        release_ref=release.ref, resolved_subject_ref=source,
        producer_contract_ref=producer,
        resolution_mode="CONTENT_ADDRESSED_MATERIALIZATION",
        resolver_or_locator_ref=location, representation_integrity_ref=integrity,
    )
    repo.register_representation(record)
    binding = PublicationBinding(
        release_ref=release.ref, publication_contract_ref=M2_PUBLICATION_CONTRACT_REF,
        resolution_mode=record.resolution_mode, resolver_or_locator_ref=location,
        representation_integrity_ref=integrity,
    )
    repo.register_binding(binding)
    assert repo.binding_exact(binding.ref) == binding
    wrong = RepresentationRecord(
        release_ref=release.ref, resolved_subject_ref=ref("TEST", "alien"),
        producer_contract_ref=producer,
        resolution_mode="CONTENT_ADDRESSED_MATERIALIZATION",
        resolver_or_locator_ref=ref("RepresentationLocator", "alien"),
        representation_integrity_ref=integrity,
    )
    with pytest.raises(M2ReleaseError, match="REBUILD_SEMANTIC_MISMATCH"):
        repo.register_representation(wrong)


def test_m2_saved_method_alias_cannot_claim_protected_issuance():
    repo, _, _, _, _ = m2_fixture()
    saved = M2Repository.register_closure
    repo._native_security_mode = "PROTECTED_CURRENT"
    with pytest.raises(M2ReleaseError) as exc:
        saved(repo, repo._closures[next(iter(repo._closures))])
    assert exc.value.code == "EXTERNAL_ISSUER_HOLD"
    with pytest.raises(M2ReleaseError, match="EXTERNAL_ISSUER_HOLD"):
        repo.require_external_issuer("EXTERNAL_CUSTODY")


def test_native_m2_all_registration_routes_reach_in_method_preflight():
    for name in ("register_subject", "register_closure", "register_release",
                 "register_representation", "register_binding"):
        assert f'self._native_mutation_preflight("{name}")' in getsource(
            getattr(M2Repository, name)
        )
    for function, target in (
        (register_producer_subject, "register_subject"),
        (constitute_closure, "register_closure"),
        (constitute_release, "register_release"),
        (register_representation, "register_representation"),
        (publish_binding, "register_binding"),
    ):
        assert f"repository.{target}(" in getsource(function)


def test_b5_m2_cross_owner_release_ref_is_not_subject_ref():
    repo, release, producer_subject_ref, producer, _ = m2_fixture()
    executor = LearnedProductLifecycleExecutor()
    b5 = replace(
        subject("m2-cross-owner"),
        release_ref=release.ref,
        producer_contract_ref=producer,
    )
    executor.stage_release(b5)
    assert executor.verify_m2_release_subject_exact(repo, release.ref) == b5
    # The producer subject and the M2 release are different exact identities.
    assert producer_subject_ref != release.ref
    with pytest.raises(M2ReleaseError):
        repo.subject_exact(release.ref)
    wrong = LearnedProductLifecycleExecutor()
    wrong.stage_release(replace(b5, producer_contract_ref=ref("ProducerContract", "wrong")))
    with pytest.raises(LearnedProductLifecycleConflict, match="identity mismatch"):
        wrong.verify_m2_release_subject_exact(repo, release.ref)


def test_no_caller_trusted_flag_or_arbitrary_token_on_native_owners():
    executor = LearnedProductLifecycleExecutor()
    repo = M2Repository()
    with pytest.raises(TypeError):
        executor.stage_release(subject("flag"), trusted=True)
    with pytest.raises(TypeError):
        repo.register_subject(None, trusted=True)
    with pytest.raises(LearnedProductLifecycleError, match="EXTERNAL_ISSUER_HOLD"):
        executor.require_external_issuer("PROTECTED_CURRENT")
    with pytest.raises(M2ReleaseError, match="EXTERNAL_ISSUER_HOLD"):
        repo.require_external_issuer("EXTERNAL_CUSTODY")


def test_b5_changed_runtime_schema_fails_even_with_new_local_hash():
    _, _, cp = checkpoint_with_publication()
    tampered = deepcopy(cp)
    tampered["checkpoint_payload"]["runtime_schema"] = "UNISSUED_SCHEMA"
    tampered["checkpoint_hash"] = semantic_hash(tampered["checkpoint_payload"])
    with pytest.raises(LearnedProductLifecycleError, match="runtime schema mismatch"):
        LearnedProductLifecycleExecutor.from_checkpoint(tampered)


def test_b5_duplicate_checkpoint_projection_key_fails_closed():
    _, _, cp = checkpoint_with_publication()
    altered = deepcopy(cp)
    altered["checkpoint_payload"]["publication"].append(
        altered["checkpoint_payload"]["publication"][0]
    )
    altered["checkpoint_hash"] = semantic_hash(altered["checkpoint_payload"])
    with pytest.raises(LearnedProductLifecycleConflict, match="repeats key"):
        LearnedProductLifecycleExecutor.from_checkpoint(altered)


def test_local_checkpoint_has_no_external_epoch_revocation_or_custody_claim():
    executor, _, cp = checkpoint_with_publication()
    assert "epoch" not in cp["checkpoint_payload"]
    assert "revoked" not in cp["checkpoint_payload"]
    assert "external_custody" not in cp["checkpoint_payload"]
    assert executor.native_security_mode == "LOCAL_UNAUTHENTICATED"
    with pytest.raises(LearnedProductLifecycleError, match="EXTERNAL_ISSUER_HOLD"):
        executor.require_external_issuer("checkpoint historical completeness")
