from dataclasses import dataclass
import hashlib

import pytest

from rawlsing_next.m6_actor_safe_expression import (
    ActorSafeRef,
    ReceiverSnapshot,
    ScopeCeiling,
    make_actor_accessible_render_envelope,
    make_actor_safe_claim_entry,
    make_nonrenderable_decision,
    make_replay_closure,
)
from rawlsing_next.wsc_gt0_v2_mediation import (
    GT0V3V2IntegrityError,
    run_gt0_v3_v2,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ActorSafeRef:
    return ActorSafeRef(kind, f"urn:test:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def _entry(tag: str):
    return make_actor_safe_claim_entry(
        claim_ref=_ref("CLAIM", tag),
        stance_record_ref=_ref("STANCE", tag),
        accessibility_state="CLAIM_ACCESSIBLE",
        first_person_permission="PERMIT_FIRST_PERSON_BELIEF",
        memory_refs=(_ref("MEMORY", tag),),
        source_transition_refs=(_ref("TRANSITION", tag),),
    )


def _bindings(actor_id: str, entries) -> dict[str, str]:
    result = {}
    for entry in entries:
        for ref in (
            entry.stance_record_ref,
            *entry.memory_refs,
            *entry.actor_perceived_view_refs,
            *entry.source_transition_refs,
        ):
            result[ref.key] = actor_id
    return result


def _bundle(tag: str, *, entries=(), decisions=(), actor_id="ACTOR-GT0", as_of=7):
    entries = tuple(entries)
    decisions = tuple(decisions)
    gp = _h(f"gp:{tag}")
    actor_state = _h(f"actor:{tag}")
    memory = _h(f"memory:{tag}")
    epistemic = _h(f"epistemic:{tag}")
    closure = make_replay_closure(
        actor_id=actor_id,
        as_of_causal_time=as_of,
        source_generated_person_record_hash=gp,
        source_actor_state_hash=actor_state,
        source_memory_state_hash=memory,
        source_epistemic_state_hash=epistemic,
        exact_causal_parent_sequence_ref_hash=_h(f"parents:{tag}"),
        canonical_claim_refs=tuple(entry.claim_ref for entry in entries),
        adp016_memory_object_and_transition_refs=tuple(
            ref for entry in entries for ref in entry.memory_refs
        ),
        epistemic_effect_and_transition_refs=tuple(
            ref for entry in entries for ref in entry.source_transition_refs
        ),
        permission_record_refs=tuple(item.permission_record_ref for item in decisions),
        actor_perceived_view_refs=tuple(
            ref for entry in entries for ref in entry.actor_perceived_view_refs
        ),
        entry_hashes=tuple(entry.entry_hash for entry in entries),
        decision_ref_hashes=tuple(item.decision_ref_hash for item in decisions),
    )
    envelope = make_actor_accessible_render_envelope(
        actor_id=actor_id,
        as_of_causal_time=as_of,
        source_generated_person_record_hash=gp,
        source_actor_state_hash=actor_state,
        source_memory_state_hash=memory,
        source_epistemic_state_hash=epistemic,
        replay_closure=closure,
        allowed_claim_entries=entries,
        explicit_denial_refs=decisions,
    )
    receiver = ReceiverSnapshot(
        actor_id,
        as_of,
        gp,
        actor_state,
        memory,
        epistemic,
        ref_actor_bindings=_bindings(actor_id, entries),
    )
    return closure, envelope, receiver


def _fingerprint():
    return {
        "actor_state_hash": _h("v3-actor"),
        "causal_ledger_hash": _h("v3-ledger"),
        "causal_cursor": 11,
        "rng_state_hash": _h("v3-rng"),
        "scheduler_state_hash": _h("v3-scheduler"),
    }


@dataclass(frozen=True)
class _FakeStageReceipt:
    stage_id: str
    status: str
    typed_state: str
    upstream_refs: tuple[str, ...]
    content_hash: str


def _stage_factory(material):
    return _FakeStageReceipt(
        stage_id=material["stage_id"],
        status=material["status"],
        typed_state=material["typed_state"],
        upstream_refs=tuple(material["upstream_refs"]),
        content_hash=material["content_hash"],
    )


def _base_kwargs(closure, envelope, receiver, claim, permission):
    return {
        "conservation_envelope": object(),
        "upstream_stage_receipt": object(),
        "actor_safe_envelope": envelope,
        "replay_closure": closure,
        "receiver": receiver,
        "requested_claim_ref": claim,
        "source_scope_ceiling": ScopeCeiling(),
        "requested_first_person_permission": permission,
        "v3_runtime_fingerprint": _fingerprint(),
        "exact_upstream_refs": (
            "GT0:F0:cssu.r1.afrobarometer.r1.005b474d6eb4253cb166",
            "GT0:V3:zero-effect-receipt:exact",
        ),
        "stage_receipt_factory": _stage_factory,
    }


def test_positive_actor_safe_claim_stops_at_named_authority_block_and_never_renders():
    entry = _entry("positive")
    closure, envelope, receiver = _bundle("positive", entries=(entry,))
    kwargs = _base_kwargs(
        closure,
        envelope,
        receiver,
        entry.claim_ref,
        entry.first_person_permission,
    )
    conservation = kwargs["conservation_envelope"]
    upstream = kwargs["upstream_stage_receipt"]
    before = dict(kwargs["v3_runtime_fingerprint"])

    first = run_gt0_v3_v2(**kwargs)
    second = run_gt0_v3_v2(**kwargs)

    assert first.protocol_status_name == "BLOCKED_NAMED_AUTHORITY_REQUIRED"
    assert first.render_state == "BLOCKED_NAMED_AUTHORITY_REQUIRED"
    assert "FINAL_ADMITTED_V2_SEMANTIC_PLAN" in first.block_reason
    assert first.model_called is False
    assert first.semantic_output is False
    assert first.rendered_artifact is None
    assert first.v3_unchanged is True
    assert kwargs["v3_runtime_fingerprint"] == before
    assert first.conservation_envelope is conservation
    assert first.upstream_stage_receipt is upstream
    assert first.stage_receipt.status == "BLOCKED_NAMED_AUTHORITY_REQUIRED"
    assert first.stage_receipt.content_hash == first.audit_hash
    assert first.audit_hash == second.audit_hash
    assert first.stage_receipt == second.stage_receipt


def test_valid_empty_actor_safe_envelope_stays_empty_and_never_calls_model():
    missing_claim = _ref("CLAIM", "missing")
    closure, envelope, receiver = _bundle("empty", entries=())
    result = run_gt0_v3_v2(
        **_base_kwargs(
            closure,
            envelope,
            receiver,
            missing_claim,
            "PERMIT_FIRST_PERSON_BELIEF",
        )
    )

    assert result.protocol_status_name == "VALID_EMPTY"
    assert result.render_state == "VALID_EMPTY_NO_MODEL_CALL"
    assert result.model_called is False
    assert result.semantic_output is False
    assert result.rendered_artifact is None
    assert result.v3_unchanged is True


def test_explicit_actor_side_denial_remains_denied_not_negative_truth_or_render():
    claim = _ref("CLAIM", "denied")
    decision = make_nonrenderable_decision(
        claim_ref=claim,
        permission_record_ref=_ref("PERMISSION", "denied"),
        accessibility_state="CLAIM_INACCESSIBLE",
        first_person_permission="DENY_FIRST_PERSON_CLAIM",
    )
    closure, envelope, receiver = _bundle("denied", entries=(), decisions=(decision,))
    result = run_gt0_v3_v2(
        **_base_kwargs(
            closure,
            envelope,
            receiver,
            claim,
            "PERMIT_FIRST_PERSON_BELIEF",
        )
    )

    assert result.protocol_status_name == "DENIED"
    assert result.render_state == "BLOCKED_M6_DENY"
    assert result.receiver_state == "DENIED_EXPLICIT_FIRST_PERSON_CLAIM"
    assert result.model_called is False
    assert result.semantic_output is False
    assert result.rendered_artifact is None
    assert result.v3_unchanged is True


def test_v3_runtime_fingerprint_is_required_and_mutable_selection_is_rejected():
    claim = _ref("CLAIM", "fingerprint")
    closure, envelope, receiver = _bundle("fingerprint", entries=())
    kwargs = _base_kwargs(
        closure,
        envelope,
        receiver,
        claim,
        "PERMIT_FIRST_PERSON_BELIEF",
    )
    kwargs["v3_runtime_fingerprint"] = {
        "actor_state_hash": _h("actor"),
        "causal_ledger_hash": _h("ledger"),
        "causal_cursor": 1,
        "rng_state_hash": _h("rng"),
    }
    with pytest.raises(GT0V3V2IntegrityError):
        run_gt0_v3_v2(**kwargs)

    kwargs["v3_runtime_fingerprint"] = _fingerprint()
    kwargs["v3_runtime_fingerprint"]["scheduler_state_hash"] = "latest"
    with pytest.raises(GT0V3V2IntegrityError):
        run_gt0_v3_v2(**kwargs)


def test_exact_upstream_refs_cannot_use_latest_default_or_wildcard():
    claim = _ref("CLAIM", "refs")
    closure, envelope, receiver = _bundle("refs", entries=())
    kwargs = _base_kwargs(
        closure,
        envelope,
        receiver,
        claim,
        "PERMIT_FIRST_PERSON_BELIEF",
    )
    kwargs["exact_upstream_refs"] = ("latest",)
    with pytest.raises(GT0V3V2IntegrityError):
        run_gt0_v3_v2(**kwargs)
