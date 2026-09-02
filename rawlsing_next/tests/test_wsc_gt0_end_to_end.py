from dataclasses import dataclass, replace
from typing import Any, Mapping

import pytest

from rawlsing_next.wsc_gt0_end_to_end import (
    EXPECTED_STAGE_SEQUENCE,
    GT0_AUTHORITY_CEILING,
    GT0_FINAL_TERMINAL,
    GT0_J01A_REF,
    GT0_SEED_ID,
    GT0_SEED_MEMBERS,
    GT0_SEED_TYPE,
    GT0HarnessContractError,
    GT0SeedBinding,
    GT0StageAPI,
    deterministic_content_hash,
    run_gt0_end_to_end,
)


SOURCE_OWNER = "AFROBAROMETER_SOURCE_STRUCTURE_PRODUCER"
INITIAL_PERMISSION = ("QUERY_IDENTITY_ONLY", "REFERENCE_ONLY")
NARROW_PERMISSION = ("REFERENCE_ONLY",)


@dataclass(frozen=True)
class FakeEnvelope:
    object_id: str
    object_type: str
    producer_authority: str
    authority_ceiling: str
    semantic_owner: str
    consumer_permission: tuple[str, ...]
    members: tuple[str, ...]
    upstream_refs: tuple[str, ...] = ()
    typed_state: str = "PASS"
    information_loss: str = "NONE__REFERENCE_PRESERVING"


@dataclass(frozen=True)
class FakeReceipt:
    stage: str
    status: str
    envelope: FakeEnvelope
    metadata: Mapping[str, Any]


def _next_envelope(
    prior: FakeReceipt,
    *,
    owner: str | None = None,
    permission: tuple[str, ...] | None = None,
) -> FakeEnvelope:
    env = prior.envelope
    return FakeEnvelope(
        object_id=env.object_id,
        object_type=env.object_type,
        producer_authority=env.producer_authority,
        authority_ceiling=env.authority_ceiling,
        semantic_owner=owner if owner is not None else env.semantic_owner,
        consumer_permission=(
            permission if permission is not None else env.consumer_permission
        ),
        members=env.members,
        upstream_refs=(deterministic_content_hash(prior),),
    )


def _stage_api(
    *,
    mutate_owner: bool = False,
    manufacture_structure: bool = False,
    mutate_v3: bool = False,
    positive_render: bool = False,
) -> GT0StageAPI:
    def bind_gt0_f0(seed: GT0SeedBinding) -> FakeReceipt:
        assert seed.object_id == GT0_SEED_ID
        assert seed.producer_authority_ref == GT0_J01A_REF
        assert seed.object_type == GT0_SEED_TYPE
        assert seed.members == GT0_SEED_MEMBERS
        assert seed.authority_ceiling == GT0_AUTHORITY_CEILING
        return FakeReceipt(
            "F0_BIND",
            "PASS",
            FakeEnvelope(
                object_id=seed.object_id,
                object_type=seed.object_type,
                producer_authority=seed.producer_authority_ref,
                authority_ceiling=seed.authority_ceiling,
                semantic_owner=SOURCE_OWNER,
                consumer_permission=INITIAL_PERMISSION,
                members=seed.members,
            ),
            {},
        )

    def run_gt0_preff(prior: FakeReceipt) -> FakeReceipt:
        return FakeReceipt(
            "PRE_FF",
            "PASS",
            _next_envelope(prior, permission=NARROW_PERMISSION),
            {"producer_reference_preserved": True},
        )

    def run_gt0_field_forge_ingress(prior: FakeReceipt) -> FakeReceipt:
        owner = "FIELD_FORGE_REOWNED_SOURCE" if mutate_owner else None
        return FakeReceipt(
            "FIELD_FORGE_INGRESS",
            "PASS",
            _next_envelope(prior, owner=owner),
            {
                "actor_independent": True,
                "strong_noun_minted": False,
            },
        )

    def run_gt0_prev3(prior: FakeReceipt) -> FakeReceipt:
        if manufacture_structure:
            return FakeReceipt(
                "PRE_V3",
                "PASS",
                _next_envelope(prior),
                {
                    "positive_structural_object_count": 1,
                    "v555_route_count": 1,
                    "v556_object_count": 0,
                    "positive_structural_object_refs": ("urn:forbidden:structure",),
                },
            )
        return FakeReceipt(
            "PRE_V3",
            "UNDEFINED_FOR_OBJECT",
            _next_envelope(prior),
            {
                "positive_structural_object_count": 0,
                "v555_route_count": 0,
                "v556_object_count": 0,
                "positive_structural_object_refs": (),
            },
        )

    def run_gt0_prev3_v3(prior: FakeReceipt) -> FakeReceipt:
        ledger_after = "ledger:mutated" if mutate_v3 else "ledger:zero"
        return FakeReceipt(
            "PRE_V3_TO_V3",
            "BLOCKED_POSITIVE_TRANSITION_AUTHORITY",
            _next_envelope(prior),
            {
                "v3_fingerprint_before": "v3:fingerprint:zero",
                "v3_fingerprint_after": "v3:fingerprint:zero",
                "ledger_hash_before": "ledger:zero",
                "ledger_hash_after": ledger_after,
                "rng_state_hash_before": "rng:zero",
                "rng_state_hash_after": "rng:zero",
                "scheduler_state_hash_before": "scheduler:zero",
                "scheduler_state_hash_after": "scheduler:zero",
                "v3_causal_mutation_count": 0 if not mutate_v3 else 1,
            },
        )

    def run_gt0_v3_v2(prior: FakeReceipt) -> FakeReceipt:
        return FakeReceipt(
            "V3_TO_V2",
            (
                "PASS"
                if positive_render
                else "BLOCKED_NAMED_AUTHORITY_REQUIRED"
            ),
            _next_envelope(prior),
            {
                "actor_claim_count": 1 if positive_render else 0,
                "positive_render_count": 1 if positive_render else 0,
                "model_called": positive_render,
            },
        )

    return GT0StageAPI(
        bind_gt0_f0,
        run_gt0_preff,
        run_gt0_field_forge_ingress,
        run_gt0_prev3,
        run_gt0_prev3_v3,
        run_gt0_v3_v2,
    )


def test_gt0_end_to_end_blocked_path_conserves_semantics_and_replays_deterministically():
    first = run_gt0_end_to_end(_stage_api())
    second = run_gt0_end_to_end(_stage_api())

    assert first == second
    assert first.seed_id == GT0_SEED_ID
    assert first.seed_authority_ref == GT0_J01A_REF
    assert first.authority_ceiling == GT0_AUTHORITY_CEILING
    assert first.semantic_owner == SOURCE_OWNER
    assert first.permission_ceiling == NARROW_PERMISSION
    assert first.v3_fingerprint_before == first.v3_fingerprint_after
    assert first.final_terminal == GT0_FINAL_TERMINAL
    assert len(first.full_thread_hash) == 64
    assert len(first.stage_receipt_hashes) == len(EXPECTED_STAGE_SEQUENCE)
    assert tuple(stage for stage, _ in first.stage_statuses) == EXPECTED_STAGE_SEQUENCE
    assert first.stage_statuses == (
        ("F0_BIND", "PASS"),
        ("PRE_FF", "PASS"),
        ("FIELD_FORGE_INGRESS", "PASS"),
        ("PRE_V3", "UNDEFINED_FOR_OBJECT"),
        ("PRE_V3_TO_V3", "BLOCKED_POSITIVE_TRANSITION_AUTHORITY"),
        ("V3_TO_V2", "BLOCKED_NAMED_AUTHORITY_REQUIRED"),
    )


def test_gt0_harness_rejects_semantic_reownership_by_wrapper_handoff():
    with pytest.raises(
        GT0HarnessContractError,
        match="changed producer semantic ownership",
    ):
        run_gt0_end_to_end(_stage_api(mutate_owner=True))


def test_gt0_harness_rejects_prev3_manufactured_structure_from_f0_candidacy():
    with pytest.raises(
        GT0HarnessContractError,
        match="PRE_V3 must abstain/block",
    ):
        run_gt0_end_to_end(_stage_api(manufacture_structure=True))


def test_gt0_harness_rejects_any_v3_state_ledger_rng_or_scheduler_mutation():
    with pytest.raises(
        GT0HarnessContractError,
        match="zero-effect invariant failed",
    ):
        run_gt0_end_to_end(_stage_api(mutate_v3=True))


def test_gt0_harness_rejects_actor_claim_or_positive_render_from_f0():
    with pytest.raises(
        GT0HarnessContractError,
        match="must block/deny/empty",
    ):
        run_gt0_end_to_end(_stage_api(positive_render=True))


def test_deterministic_hash_covers_upstream_receipt_content_and_changes_on_drift():
    api = _stage_api()
    seed = GT0SeedBinding()
    f0 = api.bind_gt0_f0(seed)
    preff = api.run_gt0_preff(f0)

    baseline = deterministic_content_hash(preff)
    drifted = replace(
        preff,
        metadata={
            **dict(preff.metadata),
            "producer_reference_preserved": False,
        },
    )

    assert deterministic_content_hash(drifted) != baseline
