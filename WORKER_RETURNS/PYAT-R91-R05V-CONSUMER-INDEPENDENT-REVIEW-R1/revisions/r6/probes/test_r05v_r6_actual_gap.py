"""R05V R6 independent actual-function probes.

These exercise the installed coordinator/consumer behavior, not merely field
names: unadmitted executor originals, learned M1/M2/B5 association against the
retained original, and whether the actual joint route uses the trusted reader.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import rawlsing_next.pre553_learned_world_composition as i4
import rawlsing_next.tests.test_universal_learned_consumer as t

OUTCOMES = Path(__file__).resolve().parents[1] / "outcomes"
OBSERVATIONS: list[dict] = []


def _record(name: str, observed: dict) -> None:
    OBSERVATIONS.append({"probe": name, **observed})


@pytest.fixture(scope="module", autouse=True)
def _dump():
    yield
    OUTCOMES.mkdir(parents=True, exist_ok=True)
    (OUTCOMES / "r05v_r6_observations.json").write_text(
        json.dumps({"schema": "R91_R05V_R6_INDEPENDENT_OBSERVATIONS@1", "probes": OBSERVATIONS}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def test_unadmitted_executor_cannot_mint_trusted_original():
    case = t._build_case()
    comp = case["composition"]
    slot = i4.NativeGraphSlot(
        "unadmitted",
        comp.source_universe_refs[0],
        case["release"],
        comp.producer_query_ref,
        comp.producer_predicate_ref,
        comp.consumer_query_ref,
        comp.consumer_model_rule_hash,
        comp.producer_route,
    )
    coordinator = i4.TrustedNativeGraphCoordinator({"unadmitted": lambda slot: comp})
    bound = coordinator.execute(i4.NativeGraphExecutionRequest((slot,)))
    result = i4.evaluate_learned_world_consumer(
        case["learned"],
        composition=bound.view.compositions[0],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        producer_query_ref=case["producer_query"].ref,
        producer_predicate_ref=case["predicate"].ref,
        product_graph=bound,
        trusted_graph_reader=coordinator,
    )
    _record("unadmitted_executor", {"state": result.state, "reason": result.reason_code})
    assert result.state != "LEARNED_CONSUMER_EXACT_SUPPORTED"


def _capture_actual_discovery():
    real_learned = t._learned_from_discovery
    real_eval = i4.evaluate_learned_world_consumer
    captured = {}

    def learned_wrap(source, qauth, dauth, authority, discovery, *, tag):
        learned1, disposition1 = real_learned(source, qauth, dauth, authority, discovery, tag=tag)
        learned2, disposition2 = real_learned(
            source, qauth, dauth, authority, discovery, tag=tag + "-alt"
        )
        captured["learned1"] = learned1
        captured["learned2"] = learned2
        return learned1, disposition1

    def eval_wrap(*args, **kwargs):
        if kwargs.get("trusted_graph_reader") is not None:
            captured.setdefault("trusted_calls", []).append((args, dict(kwargs)))
        else:
            captured.setdefault("raw_calls", []).append((args, dict(kwargs)))
        return real_eval(*args, **kwargs)

    t._learned_from_discovery = learned_wrap
    i4.evaluate_learned_world_consumer = eval_wrap
    try:
        t.test_actual_discovery_route_learned_and_consumer()
    finally:
        t._learned_from_discovery = real_learned
        i4.evaluate_learned_world_consumer = real_eval
    return captured, real_eval


def test_trusted_consumer_binds_learned_m1_m2_b5_to_original():
    captured, real_eval = _capture_actual_discovery()
    assert captured.get("trusted_calls"), "R6 discovery test made no trusted-reader call"
    args, kwargs = captured["trusted_calls"][0]
    learned2 = captured["learned2"]
    kwargs = dict(kwargs)
    if "learned" in kwargs:
        kwargs["learned"] = learned2
        call_args = args
    else:
        call_args = (learned2, *args[1:])
    result = real_eval(*call_args, **kwargs)
    _record(
        "learned_m1_m2_b5_association",
        {
            "state": result.state,
            "default_m1": captured["learned1"].m1_disposition.ref.as_dict(),
            "alternate_m1": learned2.m1_disposition.ref.as_dict(),
        },
    )
    assert result.state != "LEARNED_CONSUMER_EXACT_SUPPORTED"


def test_actual_joint_route_uses_trusted_coordinator():
    captured, _ = _capture_actual_discovery()
    joint_calls = [
        (a, k)
        for a, k in captured.get("raw_calls", [])
        if getattr(k.get("composition"), "joint_component_count", None) == 2
    ]
    trusted_joint = [
        (a, k)
        for a, k in captured.get("trusted_calls", [])
        if getattr(k.get("composition"), "joint_component_count", None) == 2
    ]
    _record(
        "joint_route",
        {"raw_joint_calls": len(joint_calls), "trusted_joint_calls": len(trusted_joint)},
    )
    assert trusted_joint
