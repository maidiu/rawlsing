# v3/engine/step_runner.py — Load config and step order; run N years.

from __future__ import annotations

from pathlib import Path

from v3.core.config_loader import load_v3config, load_step_order
from v3.core.state import BackboneState
from v3.core.derived import DerivedIndices, compute_all_derived
from v3.engine.yearly_step import run_one_year


def run_n_years(
    state: BackboneState,
    n: int,
    v3config_path: Path | None = None,
    step_order_path: Path | None = None,
    collect_json_per_year: bool = False,
) -> tuple[BackboneState, list[str] | None]:
    """Run n years. Returns (final_state, json_per_year or None). If collect_json_per_year, list has n entries (after each year)."""
    v3config = load_v3config(v3config_path)
    step_order = load_step_order(step_order_path)
    derived = compute_all_derived(state)
    outputs: list[str] | None = [] if collect_json_per_year else None

    for _ in range(n):
        run_one_year(state, derived, v3config, step_order)
        if collect_json_per_year and outputs is not None:
            from v3.io.json_codec import state_to_json
            outputs.append(state_to_json(state))
    return state, outputs
