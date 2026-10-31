# v3/tests/test_invariants.py
# Wave 2.1: State/config invariants (clamps, cracks/buffers/frameworks limits).

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from v3.core.invariants import assert_backbone_invariants, assert_all_numeric_clamped
from v3.core.state import BackboneState


def test_backbone_invariants_pass_on_default_state() -> None:
    """Default BackboneState satisfies all backbone invariants (repair_min_counts adds placeholder cracks/frameworks)."""
    state = BackboneState(year=2000, age=30)
    assert_backbone_invariants(state, config=None, repair_min_counts=True)
    print(f"  state(year={state.year}, age={state.age}): backbone invariants passed (clamps, min/max cracks/frameworks)")


def test_all_numeric_clamped_pass_in_range() -> None:
    """assert_all_numeric_clamped does not raise when values in [0, 100]."""
    state = BackboneState(year=1990, age=25)
    assert_all_numeric_clamped(state)
    print(f"  state(year={state.year}, age={state.age}): all numeric fields in [0,100], year/age excluded from clamp")


if __name__ == "__main__":
    import inspect
    print("--- test_invariants ---")
    for _name, obj in inspect.getmembers(sys.modules[__name__], predicate=inspect.isfunction):
        if _name.startswith("test_"):
            obj()
            print(f"  {_name} passed")
    print("All tests passed.")
