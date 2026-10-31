# v3/tests/test_distribution_smoke.py
# Pre–Wave 3 (or early Wave 3) smoke test: catch sign errors and collapse before full logic.
# Run 50 agents with randomized reproduction + capacity, 20 years headless; assert distribution bounds.

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from v3.core.config_loader import load_v3config, load_step_order
from v3.core.derived import compute_all_derived
from v3.engine.yearly_step import step_one_year
from v3.io.seeds import randomized_seed

# Tunable thresholds (catch sign errors; relax if design intentionally pushes boundaries).
PEAK_REGIME_RATE_MAX = 0.02  # At most 2% of agents in peak_regime by year 20.
HOSTAGE_INDEX_SPREAD_MIN = 10.0  # max - min hostage_index across agents should span at least this.
AC_IN_BAND_MIN = 0.80  # At least 80% of agents should have AC in [5, 95] (not collapsed/saturated).
YEARS = 20
N_AGENTS = 50


def test_distribution_smoke_50_agents_20_years() -> None:
    """Seed 50 agents with randomized reproduction + capacity; run 20 years headless; assert sane distributions."""
    config = load_v3config()
    step_order = load_step_order()
    hostage_indices = []
    ac_values = []
    peak_regime_count = 0

    for i in range(N_AGENTS):
        state = randomized_seed(seed=42 + i, year=2000, age=25)
        derived = compute_all_derived(state)
        for _ in range(YEARS):
            derived = step_one_year(state, config, step_order, derived)
        hostage_indices.append(derived.hostage_index)
        ac_values.append(derived.agency_capacity_AC)
        if derived.peak_regime:
            peak_regime_count += 1

    rate_peak = peak_regime_count / N_AGENTS
    assert rate_peak <= PEAK_REGIME_RATE_MAX, (
        f"peak_regime rate {rate_peak:.2%} exceeds {PEAK_REGIME_RATE_MAX:.0%}. "
        "Tune PEAK_REGIME_RATE_MAX or fix logic."
    )

    spread_hi = max(hostage_indices) - min(hostage_indices)
    assert spread_hi >= HOSTAGE_INDEX_SPREAD_MIN, (
        f"hostage_index spread {spread_hi:.1f} < {HOSTAGE_INDEX_SPREAD_MIN}. "
        "Distribution should span a range (e.g. 0–70) depending on seeds."
    )

    in_band = sum(1 for ac in ac_values if 5 <= ac <= 95)
    assert in_band / N_AGENTS >= AC_IN_BAND_MIN, (
        f"Only {in_band}/{N_AGENTS} agents have AC in [5, 95]. "
        "AC should not collapse to 0 or saturate to 100 for most agents."
    )
    spread_hi = max(hostage_indices) - min(hostage_indices)
    print(
        f"  {N_AGENTS} agents × {YEARS} years: hostage_index spread={spread_hi:.1f} (min={min(hostage_indices):.1f}, max={max(hostage_indices):.1f}), "
        f"peak_regime rate={rate_peak:.1%}, AC in [5,95]={in_band}/{N_AGENTS} ({100*in_band/N_AGENTS:.0f}%)"
    )
if __name__ == "__main__":
    import inspect
    print("--- test_distribution_smoke ---")
    for _name, obj in inspect.getmembers(sys.modules[__name__], predicate=inspect.isfunction):
        if _name.startswith("test_"):
            obj()
            print(f"  {_name} passed")
    print("All tests passed.")