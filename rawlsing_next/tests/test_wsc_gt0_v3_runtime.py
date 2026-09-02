from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib

import pytest

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PossibilitySliceEvidence,
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
    SpecificityWalkbackStep,
    evaluate_positioned_subject_possibility,
)
from rawlsing_next.wsc_gt0_v3_runtime import (
    GT0V3RuntimeCheckpoint,
    GT0V3RuntimeIntegrityError,
    run_gt0_prev3_v3,
)


def h(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class FakeStatus(str, Enum):
    PASS = "PASS"
    OBSERVED_ZERO = "OBSERVED_ZERO"
    VALID_EMPTY = "VALID_EMPTY"
    UNDEFINED_FOR_OBJECT = "UNDEFINED_FOR_OBJECT"
    BLOCKED_EXPLICIT_AUTHORITY = "BLOCKED_EXPLICIT_AUTHORITY"
    BLOCKED_COMPARATOR_ANCESTRY = "BLOCKED_COMPARATOR_ANCESTRY"
    BLOCKED_POSITIVE_TRANSITION_AUTHORITY = "BLOCKED_POSITIVE_TRANSITION_AUTHORITY"
    BLOCKED_NAMED_AUTHORITY_REQUIRED = "BLOCKED_NAMED_AUTHORITY_REQUIRED"
    NONCOMPARABLE = "NONCOMPARABLE"
    UNRESOLVED = "UNRESOLVED"
    DENIED = "DENIED"
    INTEGRITY_FAILURE = "INTEGRITY_FAILURE"


@dataclass(frozen=True)
class FakeStageReceipt:
    receipt_id: str
    content_hash: str
    stage_id: str
    status: FakeStatus
    envelope_ref: str
    upstream_refs: tuple[str, ...]
    producer_refs: tuple[str, ...]
    output_refs: tuple[str, ...]
    semantic_owner: str
    consumer_permission: str
    information_loss: str
    replay_refs: tuple[str, ...]
    details: dict[str, object]


class FakeProtocol:
    GT0StageStatus = FakeStatus
    GT0StageReceipt = FakeStageReceipt


@dataclass(frozen=True)
class FakeEnvelope:
    content_hash: str


@dataclass(frozen=True)
class FakePrev3Receipt:
    content_hash: str
    status: FakeStatus
    consumer_permission: str = "PREV3_REFERENCE_ONLY"
    information_loss: str = "NONE__REFERENCE_PRESERVING"


def checkpoint() -> GT0V3RuntimeCheckpoint:
    return GT0V3RuntimeCheckpoint(
        actor_id="gt0-actor",
        actor_state_hash=h("actor-state"),
        causal_ledger_hash=h("causal-ledger"),
        causal_cursor=0,
        rng_state_hash=h("rng-state"),
        scheduler_state_hash=h("scheduler-state"),
    )


def envelope() -> FakeEnvelope:
    return FakeEnvelope(h("gt0-envelope"))


def prev3(status: FakeStatus = FakeStatus.UNDEFINED_FOR_OBJECT) -> FakePrev3Receipt:
    return FakePrev3Receipt(h(f"prev3:{status.value}"), status)


def ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:wsc002e:{kind.lower()}:{tag}", h(f"{kind}:{tag}"))


def auth(tag: str) -> AuthorityRef:
    return AuthorityRef(f"WSC002E-{tag}", "1.0.0", h(f"authority:{tag}"))


U = ref("EmpiricalUniverse@1.0.0", "u")
R = ref("C11LogicalRelease", "r")
T = ref("TARGET", "t")


def binding(tag: str) -> ConditionerBinding:
    return ConditionerBinding(
        tag,
        ref("GENERATED_SUBJECT_FACT", tag),
        ref("EMPIRICAL_COORDINATE", tag),
        auth(f"cmp-{tag}"),
        U,
        R,
        "2026-R1",
    )


def query() -> PositionedSubjectPossibilityQuery:
    return PositionedSubjectPossibilityQuery(
        "q-wsc002e",
        ref("GENERATED_SUBJECT", "subject"),
        T,
        U,
        R,
        (binding("country"), binding("education"), binding("age")),
        {"kind": "JOINT_DISTRIBUTION"},
    )


def evidence(
    ids: tuple[str, ...],
    state: str = "SUPPORTED",
    tag: str = "evidence",
    *,
    geometry: dict[str, object] | None = None,
    n: int | None = 100,
) -> PossibilitySliceEvidence:
    if geometry is None and state == "SUPPORTED":
        geometry = {"modes": {"A": 60, "B": 40}}
    return PossibilitySliceEvidence(
        ref("EmpiricalFact@1.0.0", tag),
        U,
        R,
        T,
        ids,
        state,
        geometry,
        n,
        "GOVERNED_UPSTREAM_STATE",
        (ref("PROVENANCE", tag),),
        (auth(f"evidence-{tag}"),),
    )


def rule(*steps: SpecificityWalkbackStep) -> PositionedSubjectPossibilityModelRule:
    return PositionedSubjectPossibilityModelRule(
        auth("model"),
        auth("walkback"),
        (U,),
        tuple(steps),
        tuple(step.proxy_authority_ref for step in steps),
    )


def step(tag: str, ids: tuple[str, ...]) -> SpecificityWalkbackStep:
    return SpecificityWalkbackStep(
        tag,
        ids,
        auth(f"proxy-{tag}"),
        U,
        R,
        f"authorized specificity loss {tag}",
    )


def exact_supported():
    q = query()
    ex = evidence(q.conditioner_ids, tag="exact-supported")
    return evaluate_positioned_subject_possibility(query=q, rule=rule(), evidence=(ex,))


def exact_valid_empty():
    q = query()
    ex = evidence(q.conditioner_ids, "VALID_EMPTY", "exact-empty", geometry=None, n=0)
    return evaluate_positioned_subject_possibility(query=q, rule=rule(), evidence=(ex,))


def exact_noncomparable():
    q = query()
    ex = evidence(q.conditioner_ids, "NONCOMPARABLE", "exact-nc", geometry=None, n=None)
    return evaluate_positioned_subject_possibility(query=q, rule=rule(), evidence=(ex,))


def unresolved_proxy():
    q = query()
    exact = evidence(q.conditioner_ids, "UNDERPOWERED", "exact-under", geometry=None, n=8)
    broad = evidence(("country", "education"), tag="broad")
    s = step("drop-age", ("country", "education"))
    return evaluate_positioned_subject_possibility(query=q, rule=rule(s), evidence=(exact, broad))


def run(*, psepf=None, status: FakeStatus = FakeStatus.UNDEFINED_FOR_OBJECT):
    return run_gt0_prev3_v3(
        envelope(),
        prev3(status),
        actor_id="gt0-actor",
        runtime_checkpoint=checkpoint(),
        prev3_producer_refs=("urn:test:gt0:producer:f0",),
        psepf_result=psepf,
        protocol_module=FakeProtocol,
    )


def assert_zero_effect(out) -> None:
    assert out.zero_effect is True
    assert out.pre_checkpoint == out.post_checkpoint
    assert out.pre_checkpoint.checkpoint_hash == out.post_checkpoint.checkpoint_hash
    assert out.disposition.actor_state_effect == "ZERO"
    assert out.disposition.causal_ledger_appends == 0
    assert out.disposition.causal_cursor_delta == 0
    assert out.disposition.rng_mutations == 0
    assert out.disposition.scheduler_mutations == 0


def test_gt0_baseline_undefined_prev3_blocks_comparator_without_fabricating_psepf() -> None:
    out = run()
    assert_zero_effect(out)
    assert out.disposition.decision_status == "BLOCKED_COMPARATOR_ANCESTRY"
    assert out.stage_receipt.status is FakeStatus.BLOCKED_COMPARATOR_ANCESTRY
    assert out.disposition.psepf_result_ref is None
    assert out.disposition.psepf_result_hash is None
    assert "NO_POSITIONED_SUBJECT_POSSIBILITY_FABRICATED" in out.disposition.reason_code
    assert "UNDEFINED_FOR_OBJECT" in out.disposition.reason_code
    assert out.disposition.upstream_permission == "PREV3_REFERENCE_ONLY"
    assert out.disposition.upstream_information_loss == "NONE__REFERENCE_PRESERVING"
    assert out.stage_receipt.consumer_permission == "ZERO_EFFECT_ONLY__NO_ACTOR_MUTATION"


def test_exact_supported_psepf_preserves_full_exact_ref_and_current_guard_is_zero_positive() -> None:
    psepf = exact_supported()
    out = run(psepf=psepf, status=FakeStatus.PASS)
    assert_zero_effect(out)
    assert out.disposition.decision_status == "BLOCKED_COMPARATOR_ANCESTRY"
    assert out.stage_receipt.status is FakeStatus.BLOCKED_COMPARATOR_ANCESTRY
    assert out.disposition.psepf_result_ref == psepf.ref.key
    assert out.disposition.psepf_result_hash == psepf.result_hash
    assert out.disposition.guard_outcome == "DENY_ZERO_EFFECT"
    assert out.disposition.guard_reason == "ZERO_POSITIVE_REGISTRY"
    assert "OBL031" in out.disposition.reason_code


def test_psepf_valid_empty_is_preserved_as_typed_zero_effect_not_default_probability() -> None:
    out = run(psepf=exact_valid_empty(), status=FakeStatus.PASS)
    assert_zero_effect(out)
    assert out.disposition.decision_status == "VALID_EMPTY"
    assert out.stage_receipt.status is FakeStatus.VALID_EMPTY
    assert out.disposition.guard_outcome is None
    assert out.disposition.information_loss == "NO_DEFAULT_VALUE_SUBSTITUTION"


def test_psepf_noncomparable_is_preserved_without_proxy_rescue() -> None:
    out = run(psepf=exact_noncomparable(), status=FakeStatus.PASS)
    assert_zero_effect(out)
    assert out.disposition.decision_status == "NONCOMPARABLE"
    assert out.stage_receipt.status is FakeStatus.NONCOMPARABLE
    assert "NO_PROXY_RESCUE" in out.disposition.reason_code


def test_explicit_lower_specificity_proxy_stays_unresolved_and_records_upstream_loss() -> None:
    out = run(psepf=unresolved_proxy(), status=FakeStatus.PASS)
    assert_zero_effect(out)
    assert out.disposition.decision_status == "UNRESOLVED"
    assert out.stage_receipt.status is FakeStatus.UNRESOLVED
    assert "EXACT_UNRESOLVED_PROXY_AVAILABLE" in out.disposition.reason_code
    assert "UPSTREAM_PROXY_SPECIFICITY_LOSS_PRESERVED" in out.disposition.information_loss


def test_same_immutable_inputs_reproduce_same_disposition_and_protocol_receipt_hash() -> None:
    psepf = exact_supported()
    first = run(psepf=psepf, status=FakeStatus.PASS)
    second = run(psepf=psepf, status=FakeStatus.PASS)
    assert first.disposition.decision_hash == second.disposition.decision_hash
    assert first.disposition.ref == second.disposition.ref
    assert first.stage_receipt.content_hash == second.stage_receipt.content_hash
    assert first.stage_receipt.receipt_id == second.stage_receipt.receipt_id
    assert first.stage_receipt.replay_refs == second.stage_receipt.replay_refs


def test_non_current_psepf_object_is_typed_integrity_failure_and_still_zero_effect() -> None:
    out = run(psepf={"pretend": "psepf"}, status=FakeStatus.PASS)
    assert_zero_effect(out)
    assert out.disposition.decision_status == "INTEGRITY_FAILURE"
    assert out.stage_receipt.status is FakeStatus.INTEGRITY_FAILURE
    assert out.disposition.psepf_result_ref is None


def test_mutable_or_fuzzy_producer_selector_fails_closed_before_receipt_creation() -> None:
    with pytest.raises(GT0V3RuntimeIntegrityError, match="mutable/fuzzy"):
        run_gt0_prev3_v3(
            envelope(),
            prev3(),
            actor_id="gt0-actor",
            runtime_checkpoint=checkpoint(),
            prev3_producer_refs=("latest",),
            protocol_module=FakeProtocol,
        )


def test_actor_checkpoint_mismatch_fails_closed() -> None:
    with pytest.raises(GT0V3RuntimeIntegrityError, match="does not match"):
        run_gt0_prev3_v3(
            envelope(),
            prev3(),
            actor_id="different-actor",
            runtime_checkpoint=checkpoint(),
            prev3_producer_refs=("urn:test:gt0:producer:f0",),
            protocol_module=FakeProtocol,
        )
