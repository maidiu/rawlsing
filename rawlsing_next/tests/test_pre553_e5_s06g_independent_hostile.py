"""Independent E2 hostile tests for the S06G B5/M2 hardening candidate.

These tests use only public production APIs plus the accepted synthetic release
fixture helpers. They are written to pass on the S06G candidate overlay and to
demonstrate current PRE-MAIN defect presence when run unpatched.
"""
from __future__ import annotations

from dataclasses import replace
from threading import Barrier, Thread

import pytest

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    semantic_hash,
)
from rawlsing_next.pre553_learned_product_lifecycle import (
    LearnedProductLifecycleConflict,
    LearnedProductLifecycleError,
    LearnedProductLifecycleExecutor,
    LearnedProductLifecycleSubject,
)
from rawlsing_next.pre553_learned_product_release import (
    M2ReleaseError,
    M2Repository,
)
from rawlsing_next.tests.test_pre553_learned_product_release import (
    bind_representation,
    build_fixture,
)


def R(kind: str, tag: str) -> ExactRef:
    digest = semantic_hash({"kind": kind, "tag": tag})
    return ExactRef(kind, f"urn:test:e2:{kind}:{tag}:sha256:{digest}", digest)


def S(tag: str, *, dependency=(), materialization_class=None):
    determinant = R("DETERMINANT", f"{tag}-det")
    return LearnedProductLifecycleSubject(
        release_ref=R("LearnedProductRelease", tag),
        product_ref=R("LearnedProduct", tag),
        product_family_ref=R("ProductFamily", "shared"),
        producer_owner_ref=R("ProducerOwner", tag),
        producer_contract_ref=R("ProducerContract", tag),
        semantic_projection_hash=semantic_hash({"semantic": tag}),
        authority_snapshot_refs=(AuthorityRef(f"AUTH-{tag}", "1.0.0", semantic_hash(tag)),),
        direct_dependency_refs=tuple(dependency),
        determinant_refs=(determinant,),
        determinant_set_hash=semantic_hash([determinant.as_dict()]),
        replay_root_ref=R("ReplayRoot", tag),
        selection_scope_ref=R("SelectionScope", "shared"),
        build_or_release_receipt_refs=(R("BuildReceipt", tag),),
        producer_permission_ceiling_ref=R("PermissionCeiling", tag),
        replay_state="REPLAY_COMPLETE",
        materialization_class=materialization_class or "MANDATORY_RETAINED_CAPITAL",
    )


def reg(x: LearnedProductLifecycleExecutor, s, publish=True):
    x.stage_release(s)
    x.register_product(s.release_ref, event_authority_ref=R("EventAuthority", "reg"),
                       event_rule_ref=R("EventRule", "reg"))
    if publish:
        x.publish_product(s.release_ref, event_authority_ref=R("EventAuthority", "pub"),
                          event_rule_ref=R("EventRule", "pub"))
    return s


def key(x: LearnedProductLifecycleExecutor, s):
    return x.selection_key(product_family_ref=s.product_family_ref,
                           selection_scope_ref=s.selection_scope_ref,
                           selection_purpose_ref=R("SelectionPurpose", "serve"))


def select(x, k, s, previous=None):
    return x.select_current(k.ref, s.release_ref, expected_previous_receipt_ref=previous,
                            event_authority_ref=R("EventAuthority", "select"),
                            event_rule_ref=R("EventRule", "select"),
                            selection_attestation_ref=R("Attestation", "select"))


def cp():
    x = LearnedProductLifecycleExecutor()
    s = reg(x, S("base"))
    return x, s, x.export_checkpoint()


def test_nested_payload_frozen_and_export_detached():
    x, s, _ = cp()
    event = x.events[-1]
    old = event.ref
    with pytest.raises((TypeError, AttributeError)):
        event.payload["replay_root_ref"]["object_id"] = "alien"
    assert event.ref == old
    exported = event.as_dict()
    exported["payload"]["replay_root_ref"]["object_id"] = "export-only"
    assert event.ref == old


@pytest.mark.parametrize("field", ["replay_root_ref", "determinant_set_hash", "producer_permission_ceiling"])
def test_rehashed_publication_payload_field_refused(field):
    x, s, checkpoint = cp()
    payload = dict(x.events[-1].payload)
    payload[field] = semantic_hash("alien") if field == "determinant_set_hash" else R("Alien", field).as_dict()
    checkpoint["checkpoint_payload"]["events"][-1] = replace(x.events[-1], payload=payload).as_dict()
    checkpoint["checkpoint_hash"] = semantic_hash(checkpoint["checkpoint_payload"])
    with pytest.raises(LearnedProductLifecycleConflict):
        LearnedProductLifecycleExecutor.from_checkpoint(checkpoint)


def test_torn_publish_rolls_back_and_prior_checkpoint_restores(monkeypatch):
    x = LearnedProductLifecycleExecutor()
    s = reg(x, S("torn"), publish=False)
    prior = x.export_checkpoint()
    append = x._append_events

    def interrupted(events):
        append(events)
        raise RuntimeError("injected after append")

    monkeypatch.setattr(x, "_append_events", interrupted)
    with pytest.raises(RuntimeError):
        x.publish_product(s.release_ref, event_authority_ref=R("EventAuthority", "pub"),
                          event_rule_ref=R("EventRule", "pub"))
    assert x.events[-1].event_kind == "PRODUCT_REGISTERED"
    assert x.export_checkpoint() == prior
    assert LearnedProductLifecycleExecutor.from_checkpoint(prior).export_checkpoint() == prior


def test_concurrent_selection_one_winner_one_conflict_and_cold_restore():
    x = LearnedProductLifecycleExecutor()
    a = reg(x, S("race-a"))
    b = reg(x, S("race-b"))
    k = key(x, a)
    barrier = Barrier(2)
    winners, errors = [], []

    def run(item):
        barrier.wait(timeout=5)
        try:
            winners.append(select(x, k, item))
        except Exception as exc:
            errors.append(exc)

    threads = [Thread(target=run, args=(item,)) for item in (a, b)]
    for t in threads: t.start()
    for t in threads: t.join(timeout=6)
    assert all(not t.is_alive() for t in threads)
    assert len(winners) == 1 and len(errors) == 1
    assert isinstance(errors[0], LearnedProductLifecycleConflict)
    restored = LearnedProductLifecycleExecutor.from_checkpoint(x.export_checkpoint())
    assert restored.export_checkpoint() == x.export_checkpoint()


def test_saved_helpers_require_owner_transaction():
    x, s, checkpoint = cp()
    event = x._event(event_kind="PRODUCT_PUBLISHED", subject=S("unregistered"),
                     event_authority_ref=R("Authority", "unissued"),
                     event_rule_ref=R("Rule", "unissued"))
    with pytest.raises(LearnedProductLifecycleConflict, match="transaction"):
        x._append_events((event,))
    repo = M2Repository()
    with pytest.raises(M2ReleaseError, match="requires native writer transaction"):
        repo._insert(repo._releases, R("Release", "alien"), "not-a-release", "COLLISION")
    assert x.export_checkpoint() == checkpoint


def test_rebuild_receipt_cross_release_rehash_refused():
    x = LearnedProductLifecycleExecutor()
    a = reg(x, S("a"), publish=False)
    b = reg(x, S("b"), publish=False)
    receipt = x.record_rebuild_eligibility(a.release_ref, execution_mechanism_ref=None,
                                           event_authority_ref=R("Authority", "rebuild"),
                                           event_rule_ref=R("Rule", "rebuild"))
    checkpoint = x.export_checkpoint()
    checkpoint["checkpoint_payload"]["rebuild_eligibility"] = [
        replace(receipt, release_ref=b.release_ref).as_dict()
    ]
    checkpoint["checkpoint_hash"] = semantic_hash(checkpoint["checkpoint_payload"])
    with pytest.raises(LearnedProductLifecycleConflict):
        LearnedProductLifecycleExecutor.from_checkpoint(checkpoint)


def test_m2_foreign_binding_refused_before_later_oracle():
    repo, release, subject, producer, _, _ = build_fixture(subject_label="e2-first")
    foreign, other, osource, oproducer, _, _ = build_fixture(subject_label="e2-foreign")
    binding, _, _ = bind_representation(foreign, other, osource, oproducer,
                                        label="e2-foreign", mode="CONTENT_ADDRESSED_MATERIALIZATION")
    with pytest.raises(M2ReleaseError) as exc:
        repo.register_binding(binding)
    assert exc.value.code == "RELEASE_UNAVAILABLE"


def test_honest_local_unauthenticated_downgrade():
    x, s, _ = cp()
    assert x.native_security_mode == "LOCAL_UNAUTHENTICATED"
    with pytest.raises(LearnedProductLifecycleError, match="EXTERNAL_ISSUER_HOLD"):
        x.require_external_issuer("e2-probe")
