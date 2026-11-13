"""Fast dependency-free contract test for the pre-commit provider proxy."""
from __future__ import annotations

import sys
from pathlib import Path
import pytest

HERE = Path(__file__).resolve().parent
A_DIR = HERE.parent / "SOROK-D03-E01-1010-AGENT-A-R1"
if str(A_DIR) not in sys.path:
    sys.path.insert(0, str(A_DIR))
from post_provider_guard import GuardedProvider  # noqa: E402


class Provider:
    def __init__(self, trace):
        self.trace = trace

    def call(self, request):
        self.trace.append("provider")
        return {"prospective": request}


def test_b_guard_runs_before_world_writer():
    trace = []
    guarded = GuardedProvider(Provider(trace), lambda: trace.append("validate"))
    assert guarded.call({"hello": "world"}) == {"prospective": {"hello": "world"}}
    trace.append("writer")
    assert trace == ["provider", "validate", "writer"]


def test_b_failed_guard_prevents_world_writer():
    trace = []
    def fail():
        trace.append("validate")
        raise ValueError("P3_CHANGED")
    guarded = GuardedProvider(Provider(trace), fail)
    with pytest.raises(ValueError, match="P3_CHANGED"):
        guarded.call({})
    assert trace == ["provider", "validate"]


def test_b_guard_requires_callable_validator():
    with pytest.raises(TypeError, match="callback"):
        GuardedProvider(Provider([]), None)


def test_b_old_postwrite_check_is_too_late_differential():
    """Isolated order falsifier, not an integrated P2/P3 S2 execution."""
    trace = []
    state = {"head": "before"}

    class MutatingProvider:
        def call(self, request):
            trace.append("provider")
            state["head"] = "after"
            return {"prospective": []}

    def validate():
        if state["head"] != "before":
            trace.append("detect-drift")
            raise ValueError("STALE_P3")

    def world_write(_result):
        trace.append("world-write")

    # A's former order: provider -> world commit -> P3 head check.
    result = MutatingProvider().call({})
    world_write(result)
    with pytest.raises(ValueError, match="STALE_P3"):
        validate()
    assert trace == ["provider", "world-write", "detect-drift"]

    # B's order: provider -> guard -> (only if valid) world commit.
    trace.clear()
    state["head"] = "before"
    with pytest.raises(ValueError, match="STALE_P3"):
        result = GuardedProvider(MutatingProvider(), validate).call({})
        world_write(result)
    assert trace == ["provider", "detect-drift"]
