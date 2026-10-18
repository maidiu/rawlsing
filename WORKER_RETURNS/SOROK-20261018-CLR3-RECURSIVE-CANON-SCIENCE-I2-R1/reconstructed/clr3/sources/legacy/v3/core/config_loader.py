# v3/core/config_loader.py
# Load v3config.yaml and v3_yearly_step_order.yaml. Validate and expose for runner/state.

from pathlib import Path
from typing import Any

import yaml


def _v3_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def load_v3config(path: Path | None = None) -> dict[str, Any]:
    """Load v3config.yaml. Default: v3/v3config.yaml."""
    p = path or (_v3_dir() / "v3config.yaml")
    if not p.exists():
        raise FileNotFoundError(f"v3config not found: {p}")
    with open(p) as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("v3config must be a YAML mapping")
    return data


def load_step_order(path: Path | None = None) -> dict[str, Any]:
    """Load v3_yearly_step_order.yaml. Default: v3/v3_yearly_step_order.yaml."""
    p = path or (_v3_dir() / "v3_yearly_step_order.yaml")
    if not p.exists():
        raise FileNotFoundError(f"step order not found: {p}")
    with open(p) as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("step order must be a YAML mapping")
    return data


def get_step_list(step_order: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the ordered list of steps from step order config."""
    steps = step_order.get("steps")
    if not isinstance(steps, list):
        raise ValueError("step order must have a 'steps' list")
    return steps


def get_core_step_ids(step_order: dict[str, Any]) -> list[str]:
    """Return the core spine: step ids that must appear in order as a subsequence of steps."""
    core = step_order.get("core_steps")
    if isinstance(core, list) and core:
        return [str(x) for x in core]
    # Fallback: first N steps from steps list (backward compat if core_steps missing)
    steps = get_step_list(step_order)
    return [s["id"] for s in steps if s.get("id")][:14]


def get_extension_policy(step_order: dict[str, Any]) -> str:
    """Return 'append_only' or 'permitted_slots'. Extensions must respect this."""
    return step_order.get("extension_policy") or "append_only"


def get_derived_schedule(step_order: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Return derived_indices_schedule: index name -> {compute_after_step: step_id}."""
    s = step_order.get("derived_indices_schedule")
    if not isinstance(s, dict):
        return {}
    return {k: v if isinstance(v, dict) else {} for k, v in s.items()}


def get_execution(step_order: dict[str, Any]) -> dict[str, Any]:
    """Return execution config (timestep, max_events_per_year, clamp_after_each_step, etc.)."""
    return step_order.get("execution") or {}
