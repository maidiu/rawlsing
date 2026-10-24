"""R07 independent dynamic probe: request-slot learned association rewrite.

Captures the actual R7 AT10 discovery coordinator call, then constructs a request
slot with the same admitted id/base fields but a different learned M1/M2/B5
association. The coordinator should reject the mismatch; the trusted consumer
should not serve the alternate learned object.
"""
from __future__ import annotations

from dataclasses import replace
import inspect
import json
from pathlib import Path

import rawlsing_next.pre553_learned_world_composition as i4
import rawlsing_next.tests.test_universal_learned_consumer as t

OUTCOMES = Path(__file__).resolve().parents[1] / "outcomes"
OBSERVATIONS: list[dict] = []


def _dump():
    OUTCOMES.mkdir(parents=True, exist_ok=True)
    (OUTCOMES / "r05v_r7_observations.json").write_text(
        json.dumps({"schema": "R91_R05V_R7_INDEPENDENT_OBSERVATIONS@1", "probes": OBSERVATIONS}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _capture():
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
        return real_eval(*args, **kwargs)

    t._learned_from_discovery = learned_wrap
    i4.evaluate_learned_world_consumer = eval_wrap
    try:
        t.test_actual_discovery_route_learned_and_consumer()
    finally:
        t._learned_from_discovery = real_learned
        i4.evaluate_learned_world_consumer = real_eval
    return captured, real_eval


def test_request_slot_cannot_rewrite_admitted_learned_association():
    captured, real_eval = _capture()
    assert captured.get("trusted_calls"), "R7 discovery test made no trusted-reader call"
    args, kwargs = captured["trusted_calls"][0]
    coordinator = kwargs["trusted_graph_reader"]
    admitted = list(coordinator._admitted_slots.values())
    assert admitted, "discovery coordinator has no admitted slot"
    original_slot = admitted[0]
    learned1 = captured["learned1"]
    learned2 = captured["learned2"]
    forged_slot = replace(
        original_slot,
        m1_disposition=learned2.m1_disposition,
        m2_release=learned2.m2_artifacts.release.ref,
        b5_selection=(
            None
            if learned2.b5_selection_receipt is None
            else learned2.b5_selection_receipt.ref
        ),
    )
    request = i4.NativeGraphExecutionRequest((forged_slot,))
    bound = coordinator.execute(request)
    # Reuse the actual discovery consumer call, but with the alternate learned
    # object and the request-forged retained original.
    call_args = (learned2, *args[1:]) if "learned" not in kwargs else args
    call_kwargs = dict(kwargs)
    if "learned" in call_kwargs:
        call_kwargs["learned"] = learned2
    call_kwargs["composition"] = bound.view.compositions[0]
    call_kwargs["product_graph"] = bound
    call_kwargs["trusted_graph_reader"] = coordinator
    result = real_eval(*call_args, **call_kwargs)
    OBSERVATIONS.append(
        {
            "probe": "request_slot_learned_rewrite",
            "state": result.state,
            "reason": result.reason_code,
            "original_m1": learned1.m1_disposition.ref.content_hash,
            "forged_m1": learned2.m1_disposition.ref.content_hash,
            "request_slot_m1": forged_slot.m1_disposition.ref.content_hash,
        }
    )
    _dump()
    assert result.state != "LEARNED_CONSUMER_EXACT_SUPPORTED"
