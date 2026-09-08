"""Governed bounded court for OBL059 R2 serialization repair."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
R1_DIR = HERE.parent / "OBL059_POSITIVE_APPLICABILITY_R1"
R2_AUTHORITY = HERE / "positive_applicability_authority_r2.py"

r2_spec = importlib.util.spec_from_file_location("_obl059_r2_authority", R2_AUTHORITY)
if r2_spec is None or r2_spec.loader is None:
    raise RuntimeError(f"cannot load R2 authority: {R2_AUTHORITY}")
r2 = importlib.util.module_from_spec(r2_spec)
r2_spec.loader.exec_module(r2)

r1_court_path = R1_DIR / "governed_bounded_court.py"
sys.path.insert(0, str(R1_DIR))
try:
    r1_spec = importlib.util.spec_from_file_location("_obl059_r1_court", r1_court_path)
    if r1_spec is None or r1_spec.loader is None:
        raise RuntimeError(f"cannot load R1 court: {r1_court_path}")
    r1_court = importlib.util.module_from_spec(r1_spec)
    r1_spec.loader.exec_module(r1_court)
finally:
    sys.path.pop(0)

r1_court.evaluate_direct_positive_applicability = r2.evaluate_direct_positive_applicability


class CourtR2(r1_court.Court):
    def _assert_non_json_binding_closes(self, key, bad_value):
        packet = r1_court.fixture()
        packet[key] = bad_value
        result = r2.evaluate_direct_positive_applicability(packet)
        self.assertEqual(result["decision"], r2.NEGATIVE_DECISION, result)
        self.assertEqual(result["reason"], f"MALFORMED_BINDING:{key}", result)
        self.assertFalse(result["project_current_state_created"])
        self.assertFalse(result["actor_created_or_activated"])
        self.assertFalse(result["adp008_phase_transition_executed"])
        self.assertFalse(result["adp019_occurrence_admitted"])
        self.assertFalse(result["causal_use_permission_owned"])
        self.assertFalse(result["contact_witness_independence_owned"])
        self.assertFalse(result["encounter_created"])
        self.assertFalse(result["oee_realized"])
        self.assertFalse(result["obl055_executed"])
        self.assertFalse(result["current_positive_obl056_installed"])
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64)
        return result

    def test_31_bytes_actor_binding_returns_json_safe_negative_receipt(self):
        self._assert_non_json_binding_closes("actor_id", b"not-a-valid-id")

    def test_32_set_world_binding_returns_json_safe_negative_receipt(self):
        self._assert_non_json_binding_closes("world_id", {"not", "a", "valid", "id"})

    def test_33_object_opportunity_binding_returns_json_safe_negative_receipt(self):
        self._assert_non_json_binding_closes("adp010_opportunity_id", object())

    def test_34_json_safe_behavior_is_exactly_r1_preserved(self):
        positive = r1_court.fixture()
        self.assertEqual(
            r2.evaluate_direct_positive_applicability(positive),
            r2._r1.evaluate_direct_positive_applicability(positive),
        )

        negative = r1_court.fixture()
        negative["execution_scope"] = "PROJECT_CURRENT"
        self.assertEqual(
            r2.evaluate_direct_positive_applicability(negative),
            r2._r1.evaluate_direct_positive_applicability(negative),
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CourtR2)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(
        json.dumps(
            {
                "court": "OBL059_R2_GOVERNED_BOUNDED_COURT",
                "tests_run": result.testsRun,
                "failures": len(result.failures),
                "errors": len(result.errors),
                "successful": result.wasSuccessful(),
                "execution_scope": r2.SYNTHETIC_SCOPE,
                "project_current_state_created": False,
                "independent_review_performed": False,
            },
            sort_keys=True,
        )
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
