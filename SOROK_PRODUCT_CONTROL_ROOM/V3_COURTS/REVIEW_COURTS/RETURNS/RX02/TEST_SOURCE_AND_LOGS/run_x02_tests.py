"""Run X02's 17 historical V3 test files sourcefree with a read-only YAML bridge."""
from __future__ import annotations
import json, os, subprocess, sys, types
from pathlib import Path
SOURCE = Path(os.environ["X02_SOURCE_ROOT"])
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))
_RUBY = "require 'yaml'; require 'json'; print JSON.generate(YAML.safe_load(STDIN.read, [], [], true))"
def _conv(o):
    if isinstance(o, dict):
        return {(int(k) if isinstance(k, str) and k.isdigit() else k): _conv(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_conv(x) for x in o]
    return o
def safe_load(value):
    if hasattr(value, "read"):
        value = value.read()
    p = subprocess.run(["ruby", "-e", _RUBY], input=value, capture_output=True, text=True)
    if p.returncode != 0:
        raise ValueError("YAML_PARSE_FAILED: " + p.stderr.strip()[:300])
    return _conv(json.loads(p.stdout))
m = sys.modules.get("yaml") or types.ModuleType("yaml")
m.safe_load = safe_load
sys.modules["yaml"] = m
import pytest
FILES = [
 "v3/tests/test_v5_pressure_flow.py",
 "v3/tests/test_v5_pressureflow_golden_run.py",
 "v3/tests/test_v5_pressureflow_mediates_relation_state_without_surface_leak.py",
 "v3/tests/test_v5_surface_psyche_profile.py",
 "v3/tests/test_v5_sublimation_channels.py",
 "v3/tests/test_v5_baseline_load.py",
 "v3/tests/test_phase3_activation_gate.py",
 "v3/tests/test_v5_vitality_fatigue.py",
 "v3/tests/test_v5_insulation_registry.py",
 "v3/tests/test_v5_vessel_hints.py",
 "v3/tests/test_step_logic.py",
 "v3/tests/test_v5_render_surface_psyche.py",
 "v3/tests/test_v5_persona_sheet_surface_psyche.py",
 "v3/tests/test_v5_v2_chat_prompt_no_raw_v5_leaks.py",
 "v3/tests/test_v5_structural_diagnostics.py",
 "v3/tests/test_architecture_invariants.py",
 "v3/tests/test_invariants.py",
]
raise SystemExit(pytest.main(["-q", "-p", "no:cacheprovider", *FILES]))
