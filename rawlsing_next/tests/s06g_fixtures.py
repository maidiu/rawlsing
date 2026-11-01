"""Standalone source-free fixtures for the S06G B5/M2 hardening tests.

These are extracted from the historical S06F test helper only: the helper
functions are needed by the S06G test module on current PRE-MAIN, which does not
carry the S06F test module. No S06F acceptance test is imported or executed.

No external issuer, protected CURRENT, native source or production authority is
created by these fixtures.
"""
from __future__ import annotations

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash
from rawlsing_next.pre553_learned_product_lifecycle import (
    LearnedProductLifecycleExecutor,
    LearnedProductLifecycleSubject,
)
from rawlsing_next.pre553_learned_product_release import (
    M2Repository,
    constitute_closure,
    constitute_release,
    register_producer_subject,
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
