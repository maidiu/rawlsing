# v3/tests/test_step_sanity.py — Run 10–20 years; no crash; invariants hold.

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from v3.core.state import BackboneState
from v3.core.derived import compute_all_derived
from v3.engine.step_runner import run_n_years


def test_run_10_years_no_crash() -> None:
    state = BackboneState(year=2000, age=25)
    final, _ = run_n_years(state, 10)
    assert final.year == 2010
    assert final.age == 35
    print(f"  run_n_years(10): year 2000→{final.year}, age 25→{final.age}")


def test_run_20_years_stable() -> None:
    state = BackboneState(year=1990, age=10)
    final, jsons = run_n_years(state, 20, collect_json_per_year=True)
    assert final.year == 2010
    assert final.age == 30
    assert jsons is not None
    assert len(jsons) == 20
    for j in jsons:
        assert '"year"' in j and '"age"' in j
    print(f"  run_n_years(20, collect_json_per_year=True): {len(jsons)} JSON snapshots, year {final.year}, age {final.age}")


def test_derived_computed_after_run() -> None:
    state = BackboneState(year=2000, age=30)
    derived = compute_all_derived(state)
    assert 0 <= derived.hostage_index <= 100
    assert 0 <= derived.agency_capacity_AC <= 100
    assert 0 <= derived.structural_lucidity_SL <= 100
    print(
        f"  derived: hostage_index={derived.hostage_index:.1f}, AC={derived.agency_capacity_AC:.1f}, "
        f"SL={derived.structural_lucidity_SL:.1f}, mis_aim_risk={derived.mis_aim_risk:.1f}"
    )
if __name__ == "__main__":
    import inspect
    print("--- test_step_sanity ---")
    for _name, obj in inspect.getmembers(sys.modules[__name__], predicate=inspect.isfunction):
        if _name.startswith("test_"):
            obj()
            print(f"  {_name} passed")
    print("All tests passed.")