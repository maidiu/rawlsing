from __future__ import annotations

import ast
from pathlib import Path

from conftest import event, projection, snapshot, year_input
from v3.core.state import Crack, Framework, MetabolizationProcess, NarrationSupport
from v3core_adapter.contracts import Status
from v3core_adapter.quarantine import (
    assert_no_forbidden_defaults,
    build_projection_state,
    forbidden_default_reasons,
    quarantine_manifest,
)
from v3core_adapter.scheduler import run_year

ROOT = Path(__file__).resolve().parents[1]


def _fresh_state():
    return build_projection_state(annual_year=1, age=None, snapshot=snapshot())


def test_fresh_projection_state_has_no_forbidden_defaults() -> None:
    state = _fresh_state()
    assert_no_forbidden_defaults(state)
    assert state.wound_vector.shame == 0
    assert state.psychological_capacity.vitality == 0
    assert state.expectation_baseline == {}
    assert state.cracks == []
    assert state.frameworks == []
    assert state.metabolization_processes == []
    assert state.domains["empire_occupation"].A == 0
    assert state.reproduction_constraints.legal_status == 0


def test_identity_seeded_wound_is_rejected() -> None:
    state = _fresh_state()
    state.wound_vector.shame = 70
    reasons = forbidden_default_reasons(state)
    assert "wound_vector_nonzero_identity_or_default" in reasons


def test_hopeful_parent_default_is_rejected() -> None:
    state = _fresh_state()
    state.expectation_baseline = {"attachment": "hopeful"}
    reasons = forbidden_default_reasons(state)
    assert "expectation_baseline_present" in reasons
    assert "forbidden_token:hopeful" in reasons


def test_placeholder_crack_and_framework_are_rejected() -> None:
    state = _fresh_state()
    state.cracks.append(Crack(type="placeholder", intensity=5.0))
    state.frameworks.append(Framework(id="placeholder_0", weight=5.0))
    reasons = forbidden_default_reasons(state)
    assert "cracks_present" in reasons
    assert "frameworks_present" in reasons
    assert "forbidden_token:placeholder" in reasons


def test_random_metabolization_process_is_rejected() -> None:
    state = _fresh_state()
    state.metabolization_processes.append(MetabolizationProcess(cluster="random_rupture"))
    reasons = forbidden_default_reasons(state)
    assert "metabolization_processes_present" in reasons
    assert "forbidden_token:random_rupture" in reasons


def test_enneagram_type_determinism_is_rejected() -> None:
    state = _fresh_state()
    state.child_model = {"enneagram_type": "4"}
    reasons = forbidden_default_reasons(state)
    assert "enneagram_or_type_determinism" in reasons
    assert "forbidden_token:enneagram" in reasons


def test_narration_midpoint_default_is_rejected() -> None:
    state = _fresh_state()
    state.narration_support = NarrationSupport()
    reasons = forbidden_default_reasons(state)
    assert "narration_support_midpoint_default" in reasons


def test_injected_default_blocks_the_year_without_commit() -> None:
    proj = projection()
    proj.state.wound_vector.shame = 70
    before = proj.state_hash()
    result = run_year(proj, year_input())
    assert result.status == Status.HELD_FORBIDDEN_DEFAULT
    assert result.committed is False
    assert proj.state_hash() == before
    assert "wound_vector_nonzero_identity_or_default" in result.reason


def test_quarantine_manifest_is_hash_bound() -> None:
    manifest = quarantine_manifest()
    assert len(manifest) == 8
    mechanisms = {row["mechanism"] for row in manifest}
    assert "M08_IDENTITY_SEEDED_WOUND" in mechanisms
    assert "M15_M36_MISSING_PARENT_MIDPOINT_AND_HOPEFUL_DEFAULTS" in mechanisms
    assert "M31_ENNEAGRAM_TYPE_DETERMINISM" in mechanisms
    assert "M34_SYNTHETIC_FALLBACK_PRACTICE" in mechanisms
    assert "M35_PLACEHOLDER_CRACKS_AND_FRAMEWORKS" in mechanisms
    assert "M39_RANDOM_AGE_BAND_RUPTURE" in mechanisms
    for row in manifest:
        assert len(row["source_sha256"]) == 64
        assert row["active_path"] == "EXCLUDED_FROM_ADAPTER"


def _module_level_imports(path: Path) -> list[tuple[str, str]]:
    tree = ast.parse(path.read_text())
    imports: list[tuple[str, str]] = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append((module, alias.name))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((alias.name, ""))
    return imports


def test_adapter_does_not_import_forbidden_mechanisms() -> None:
    forbidden_modules = {
        "v3.psyche.channels",
        "v3.io.parent_baseline_from_behavior",
        "v3.engine.expectation_baseline",
        "v3.engine.llm_contract",
        "v3.engine.run_llm_band",
        "v3.engine.effects.metabolization_effects",
        "v2.enneagram_wisdom",
        "v2.parent_type_inference",
    }
    forbidden_names = {"ensure_min_cracks", "ensure_min_frameworks", "seed_wound_vector_from_identity"}
    problems: list[str] = []
    for path in sorted((ROOT / "v3core_adapter").glob("*.py")):
        for module, name in _module_level_imports(path):
            if module in forbidden_modules or module.startswith(tuple(forbidden_modules)):
                problems.append(f"{path.name}:{module}:{name}")
            if name in forbidden_names:
                problems.append(f"{path.name}:{module}:{name}")
    assert problems == []


def test_flow_quarantine_imports_historical_flow_lazily() -> None:
    imports = _module_level_imports(ROOT / "v3core_adapter" / "flow_quarantine.py")
    assert ("v3.psyche.flow", "") not in imports
    source = (ROOT / "v3core_adapter" / "flow_quarantine.py").read_text()
    assert "from v3.psyche.flow import run_pressure_flow_cycle" in source
