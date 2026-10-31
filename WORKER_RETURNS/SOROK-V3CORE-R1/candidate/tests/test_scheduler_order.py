from __future__ import annotations

import copy
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from v3core_adapter.contracts import ANNUAL_STEP_IDS
from v3core_adapter.scheduler import SchedulerRefusal, load_plan, validate_step_order

ROOT = Path(__file__).resolve().parents[1]


def _step_order() -> dict:
    return yaml.safe_load((ROOT / "vendor" / "v3" / "v3_yearly_step_order.yaml").read_text())


def test_core_spine_is_the_exact_nineteen_step_sequence() -> None:
    plan = load_plan()
    assert plan.core_ids == ANNUAL_STEP_IDS
    assert len(plan.core_ids) == 19
    ids = [step["id"] for step in plan.steps if step.get("id")]
    assert ids.index("field_update") < ids.index("event_sampling") < ids.index("render_layer")


def test_render_layer_moved_before_field_update_is_refused() -> None:
    order = copy.deepcopy(_step_order())
    steps = order["steps"]
    render = next(step for step in steps if step["id"] == "render_layer")
    steps.remove(render)
    field_position = next(i for i, step in enumerate(steps) if step["id"] == "field_update")
    steps.insert(field_position, render)
    with pytest.raises(SchedulerRefusal) as error:
        validate_step_order(order)
    assert error.value.code == "CORE_STEP_ORDER_MUTATED"


def test_unchanged_original_test_catches_mutated_order(tmp_path: Path) -> None:
    target = tmp_path / "mutated"
    shutil.copytree(ROOT / "vendor" / "v3", target / "v3")
    order_path = target / "v3" / "v3_yearly_step_order.yaml"
    order = yaml.safe_load(order_path.read_text())
    render = next(step for step in order["steps"] if step["id"] == "render_layer")
    order["steps"].remove(render)
    order["steps"].insert(0, render)
    order_path.write_text(yaml.safe_dump(order, sort_keys=False))
    env = dict(os.environ)
    env["PYTHONPATH"] = f"{target}:{ROOT / 'vendor' / 'py3deps'}"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-o",
            "addopts=",
            "-q",
            "-p",
            "no:cacheprovider",
            "v3/tests/test_architecture_invariants.py::test_step_order_immutable",
        ],
        cwd=target,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "Core step id 'render_layer' missing or out of order" in result.stdout
