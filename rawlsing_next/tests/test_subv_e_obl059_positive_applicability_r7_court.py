"""Governed-court wrapper for frozen OBL059 R7 bounded repair."""
from __future__ import annotations

import importlib.util
import json
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL059_POSITIVE_APPLICABILITY_R7/governed_bounded_court_r7.py"

spec = importlib.util.spec_from_file_location("_obl059_r7_bounded_repair_lane", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load OBL059 R7 court: {TARGET}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestOBL059R7BoundedRepair(module.CourtR7):
    """Route inherited R6 preservation checks through R7's actual delegate chain."""

    def assert_negative_total(self, packet, key=None):
        try:
            result = module.r7.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(f"R7 negative path raised {type(exc).__name__}: {exc}")
        self.assertEqual(result["decision"], module.r7.NEGATIVE_DECISION, result)
        if key is not None:
            self.assertEqual(result["reason"], f"MALFORMED_BINDING:{key}", result)
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64)
        for effect in module.EFFECT_KEYS:
            self.assertFalse(result[effect], effect)
        return result

    def test_43_unrelated_programmer_errors_are_not_masked(self):
        original = module.r7._r6._r5.evaluate_direct_positive_applicability
        try:
            for exc_type in (TypeError, ValueError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r7-deliberate-programmer-error")
                module.r7._r6._r5.evaluate_direct_positive_applicability = deliberate
                with self.assertRaisesRegex(exc_type, "r7-deliberate-programmer-error"):
                    module.r7.evaluate_direct_positive_applicability(module.fixture())
        finally:
            module.r7._r6._r5.evaluate_direct_positive_applicability = original

    def test_55_unrelated_programmer_errors_remain_visible(self):
        original = module.r7._r6._r5.evaluate_direct_positive_applicability
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r7-deliberate-programmer-error")
                module.r7._r6._r5.evaluate_direct_positive_applicability = deliberate
                with self.assertRaisesRegex(exc_type, "r7-deliberate-programmer-error"):
                    module.r7.evaluate_direct_positive_applicability(module.fixture())
        finally:
            module.r7._r6._r5.evaluate_direct_positive_applicability = original

    def test_70_reproduced_zero_to_minimum_barrier_remains_total(self):
        huge = 10 ** 5000
        packet = self.malformed_at("actor_id", huge)
        original_requires = module.r7._r6._requires_total_projection_stable
        entered = threading.Event()
        release = threading.Event()
        state = {}

        def gated_requires(candidate_packet, reason):
            decision = original_requires(candidate_packet, reason)
            state["classification_result"] = decision
            entered.set()
            if not release.wait(timeout=10):
                raise RuntimeError("r7 barrier timeout")
            return decision

        def run_candidate():
            try:
                state["result"] = module.r7.evaluate_direct_positive_applicability(packet)
            except Exception as exc:
                state["exception"] = exc

        try:
            sys.set_int_max_str_digits(0)
            module.r7._r6._requires_total_projection_stable = gated_requires
            worker = threading.Thread(target=run_candidate, daemon=True)
            worker.start()
            self.assertTrue(entered.wait(timeout=10))
            self.assertTrue(state.get("classification_result"))
            sys.set_int_max_str_digits(self.minimum_limit)
            release.set()
            worker.join(timeout=10)
            self.assertFalse(worker.is_alive())
            self.assertNotIn("exception", state)
            result = state["result"]
            self.assertEqual(result["decision"], module.r7.NEGATIVE_DECISION)
            json.dumps(result, sort_keys=True)
        finally:
            release.set()
            module.r7._r6._requires_total_projection_stable = original_requires

    def test_72_setting_change_after_projection_before_canonical_is_safe(self):
        huge = 10 ** 5000
        packet = self.malformed_at("time_id", huge)
        original_canonical = module.r7._r6._canonical
        changed = {"done": False}

        def changing_canonical(value):
            if not changed["done"]:
                changed["done"] = True
                sys.set_int_max_str_digits(self.minimum_limit)
            return original_canonical(value)

        try:
            sys.set_int_max_str_digits(0)
            module.r7._r6._canonical = changing_canonical
            result = self.assert_negative_total(packet, "time_id")
            self.assertTrue(changed["done"])
            json.dumps(result, sort_keys=True)
        finally:
            module.r7._r6._canonical = original_canonical
