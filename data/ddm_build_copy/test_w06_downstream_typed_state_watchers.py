from __future__ import annotations

import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "data" / "ddm_build_copy"


def _function_source(path: Path, name: str) -> str:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return "\n".join(lines[node.lineno - 1 : node.end_lineno])
    raise AssertionError(f"missing function {name} in {path}")


class TestW06DeferredTypedStateWatchers(unittest.TestCase):
    def test_watch_001_v553_zero_probe_cannot_be_authoritative(self):
        body = _function_source(BUILD / "ddm_v553_temporal_pressure.py", "_build_v553_temporal_pressure_field_contract")
        self.assertIn('authorized_structural_pressure_value is not None', body)
        self.assertIn('allowed_downstream_use = bool(temporal_status == "observed_authorized_anchor"', body)
        self.assertIn('pressure_level = None', body)
        self.assertIn('authorized_structural_pressure_value = None', body)
        self.assertIn('pressure_value_kind = "gap"', body)

    def test_watch_002_v554_missing_point_estimate_stays_blocker_only(self):
        body = _function_source(BUILD / "ddm_v554_seed_contract.py", "_build_seed_affordance_index")
        permission = _function_source(BUILD / "ddm_v554_seed_contract.py", "_seed_permission")
        self.assertIn('pressure_distribution.get("point_estimate", 0.0)', body)
        self.assertIn('readiness = "blocker_only"', body)
        self.assertIn('if seed_readiness_status == "blocker_only":', permission)
        self.assertIn('return "blocker_only"', permission)
        self.assertNotIn('if pressure_value == 0', body)

    def test_watch_006_thin_numeric_score_is_diagnostic_not_authority_gate(self):
        common = _function_source(BUILD / "ddm_v5_thin_end_to_end.py", "_common_payload")
        status = _function_source(BUILD / "ddm_v5_thin_end_to_end.py", "_status_for")
        self.assertIn('"known_absences_are_preserved": True', common)
        self.assertIn('"input_status": input_inspection["input_status"]', common)
        self.assertNotIn("boundary_readiness_score", status)
        self.assertIn('if input_status == "blocked_missing_required_input"', status)

    @unittest.expectedFailure
    def test_watch_006_typed_producer_state_survives_thin_diagnostic_summary(self):
        # Desired deferred regression.  Current V553-V558 ownership is explicitly
        # outside W06-A; keep this as an expected-failure watcher until Vozhd
        # reassigns the downstream summary adapter or its owner lands the hook.
        body = _function_source(BUILD / "ddm_v5_thin_end_to_end.py", "_summarize_readiness_report")
        self.assertIn('"run_integrity_status"', body)
        self.assertIn('"evidence_status"', body)
        self.assertIn('"downstream_permission_status"', body)


if __name__ == "__main__":
    unittest.main()
