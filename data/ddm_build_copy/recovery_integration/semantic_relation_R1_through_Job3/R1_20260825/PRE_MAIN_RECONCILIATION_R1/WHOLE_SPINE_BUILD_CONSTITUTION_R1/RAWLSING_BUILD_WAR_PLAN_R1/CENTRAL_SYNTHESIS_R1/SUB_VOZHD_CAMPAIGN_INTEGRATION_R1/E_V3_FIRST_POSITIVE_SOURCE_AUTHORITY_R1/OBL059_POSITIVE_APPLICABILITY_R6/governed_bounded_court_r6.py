"""Governed bounded court for OBL059 R6 stable malformed-int repair."""

from __future__ import annotations

import importlib.util
import json
import sys
import threading
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
R5_DIR = HERE.parent / "OBL059_POSITIVE_APPLICABILITY_R5"
R6_AUTHORITY = HERE / "positive_applicability_authority_r6.py"

r6_spec = importlib.util.spec_from_file_location("_obl059_r6_authority", R6_AUTHORITY)
if r6_spec is None or r6_spec.loader is None:
    raise RuntimeError(f"cannot load R6 authority: {R6_AUTHORITY}")
r6 = importlib.util.module_from_spec(r6_spec)
r6_spec.loader.exec_module(r6)

r5_court_path = R5_DIR / "governed_bounded_court_r5.py"
r5_spec = importlib.util.spec_from_file_location("_obl059_r5_court_for_r6", r5_court_path)
if r5_spec is None or r5_spec.loader is None:
    raise RuntimeError(f"cannot load R5 court: {r5_court_path}")
r5_court = importlib.util.module_from_spec(r5_spec)
r5_spec.loader.exec_module(r5_court)

# Route inherited public evaluation points through frozen R6.
r5_court.r5.evaluate_direct_positive_applicability = r6.evaluate_direct_positive_applicability
r5_court.r4_court.r4.evaluate_direct_positive_applicability = r6.evaluate_direct_positive_applicability
r5_court.r4_court.r3_court.r3.evaluate_direct_positive_applicability = r6.evaluate_direct_positive_applicability
r5_court.r4_court.r3_court.r2_court.r2.evaluate_direct_positive_applicability = r6.evaluate_direct_positive_applicability
r5_court.r4_court.r3_court.r2_court.r1_court.evaluate_direct_positive_applicability = r6.evaluate_direct_positive_applicability

EFFECT_KEYS = tuple(r5_court.EFFECT_KEYS)


def fixture():
    return r5_court.fixture()


class CourtR6(r5_court.CourtR5):
    REQUIRED = tuple(r6._REQUIRED_BINDINGS)

    def setUp(self):
        super_method = getattr(super(), "setUp", None)
        if callable(super_method):
            super_method()
        self.original_limit = sys.get_int_max_str_digits()
        self.minimum_limit = int(sys.int_info.str_digits_check_threshold)

    def tearDown(self):
        sys.set_int_max_str_digits(self.original_limit)
        super_method = getattr(super(), "tearDown", None)
        if callable(super_method):
            super_method()

    def malformed_at(self, key, value):
        packet = fixture()
        packet[key] = value
        return packet

    def assert_negative_total(self, packet, key):
        try:
            result = r6.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(f"R6 malformed negative path raised {type(exc).__name__}: {exc}")
        self.assertEqual(result["decision"], r6.NEGATIVE_DECISION, result)
        self.assertEqual(result["reason"], f"MALFORMED_BINDING:{key}", result)
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64)
        for effect in EFFECT_KEYS:
            self.assertFalse(result[effect], effect)
        return result

    # Override inherited routing-only preservation checks so they target R6's
    # actual delegate instance rather than separately loaded ancestor modules.
    def test_43_unrelated_programmer_errors_are_not_masked(self):
        original = r6._r5.evaluate_direct_positive_applicability
        try:
            for exc_type in (TypeError, ValueError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r6-deliberate-programmer-error")
                r6._r5.evaluate_direct_positive_applicability = deliberate
                with self.assertRaisesRegex(exc_type, "r6-deliberate-programmer-error"):
                    r6.evaluate_direct_positive_applicability(fixture())
        finally:
            r6._r5.evaluate_direct_positive_applicability = original

    def test_55_unrelated_programmer_errors_remain_visible(self):
        original = r6._r5.evaluate_direct_positive_applicability
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r6-deliberate-programmer-error")
                r6._r5.evaluate_direct_positive_applicability = deliberate
                with self.assertRaisesRegex(exc_type, "r6-deliberate-programmer-error"):
                    r6.evaluate_direct_positive_applicability(fixture())
        finally:
            r6._r5.evaluate_direct_positive_applicability = original

    def test_69_r6_revision_and_immutable_floor_are_exact(self):
        self.assertEqual(
            r6.R6_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R6",
        )
        self.assertEqual(r6._MIN_SUPPORTED_NONZERO_INT_STR_DIGITS, self.minimum_limit)
        self.assertEqual(r6._STABLE_DECIMAL_THRESHOLD, 10 ** self.minimum_limit)

    def test_70_reproduced_zero_to_minimum_barrier_remains_total(self):
        huge = 10 ** 5000
        packet = self.malformed_at("actor_id", huge)
        original_requires = r6._requires_total_projection_stable
        entered = threading.Event()
        release = threading.Event()
        state = {}

        def gated_requires(candidate_packet, reason):
            decision = original_requires(candidate_packet, reason)
            state["classification_result"] = decision
            entered.set()
            if not release.wait(timeout=10):
                raise RuntimeError("r6 barrier timeout")
            return decision

        def run_candidate():
            try:
                state["result"] = r6.evaluate_direct_positive_applicability(packet)
            except Exception as exc:
                state["exception"] = exc

        try:
            sys.set_int_max_str_digits(0)
            r6._requires_total_projection_stable = gated_requires
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
            self.assertEqual(result["decision"], r6.NEGATIVE_DECISION)
            json.dumps(result, sort_keys=True)
        finally:
            release.set()
            r6._requires_total_projection_stable = original_requires

    def test_71_reverse_and_repeated_setting_changes_preserve_same_negative(self):
        huge = -(10 ** 5000)
        settings = [self.minimum_limit, 0, self.original_limit, self.minimum_limit, 0]
        results = []
        for setting in settings:
            sys.set_int_max_str_digits(setting)
            results.append(self.assert_negative_total(self.malformed_at("world_id", huge), "world_id"))
        for result in results[1:]:
            self.assertEqual(result, results[0])

    def test_72_setting_change_after_projection_before_canonical_is_safe(self):
        huge = 10 ** 5000
        packet = self.malformed_at("time_id", huge)
        original_canonical = r6._canonical
        changed = {"done": False}

        def changing_canonical(value):
            if not changed["done"]:
                changed["done"] = True
                sys.set_int_max_str_digits(self.minimum_limit)
            return original_canonical(value)

        try:
            sys.set_int_max_str_digits(0)
            r6._canonical = changing_canonical
            result = self.assert_negative_total(packet, "time_id")
            self.assertTrue(changed["done"])
            json.dumps(result, sort_keys=True)
        finally:
            r6._canonical = original_canonical

    def test_73_concurrent_supported_setting_changes_do_not_escape(self):
        huge = 10 ** 7000
        stop = threading.Event()
        failures = []

        def toggler():
            try:
                while not stop.is_set():
                    sys.set_int_max_str_digits(0)
                    sys.set_int_max_str_digits(self.minimum_limit)
            except Exception as exc:
                failures.append(exc)

        worker = threading.Thread(target=toggler, daemon=True)
        worker.start()
        try:
            for index in range(25):
                key = self.REQUIRED[index % len(self.REQUIRED)]
                self.assert_negative_total(self.malformed_at(key, huge), key)
        finally:
            stop.set()
            worker.join(timeout=10)
        self.assertFalse(worker.is_alive())
        self.assertEqual(failures, [])

    def test_74_stable_threshold_edges_are_independent_of_current_setting(self):
        safe = (10 ** self.minimum_limit) - 1
        unsafe = 10 ** self.minimum_limit
        for setting in (0, self.minimum_limit, self.original_limit):
            sys.set_int_max_str_digits(setting)
            with self.subTest(setting=setting):
                self.assertTrue(r6._exact_int_stable_for_all_supported_limits(safe))
                self.assertTrue(r6._exact_int_stable_for_all_supported_limits(-safe))
                self.assertFalse(r6._exact_int_stable_for_all_supported_limits(unsafe))
                self.assertFalse(r6._exact_int_stable_for_all_supported_limits(-unsafe))

    def test_75_positive_and_negative_oversized_integers_close_all_bindings(self):
        for key in self.REQUIRED:
            for value in (10 ** 5000, -(10 ** 5000), 10 ** 12000):
                with self.subTest(key=key, bits=int.bit_length(value)):
                    result = self.assert_negative_total(self.malformed_at(key, value), key)
                    projected = result["bindings"][key]
                    self.assertEqual(projected["__non_json_int__"], "decimal_conversion_limit_exceeded")
                    self.assertEqual(projected["sign"], -1 if value < 0 else 1)
                    self.assertEqual(projected["bit_length"], int.bit_length(value))

    def test_76_nested_oversized_integers_and_integer_keys_are_stable(self):
        huge = 10 ** 6000
        makers = (
            lambda: {huge: "value"},
            lambda: ["prefix", huge],
            lambda: ("prefix", {"inner": -huge}),
            lambda: {"outer": [1, {huge: [huge, -huge]}]},
            lambda: {huge, huge + 1},
            lambda: frozenset({huge, huge + 1}),
        )
        for key in self.REQUIRED:
            for maker in makers:
                with self.subTest(key=key, maker=maker.__name__):
                    self.assert_negative_total(self.malformed_at(key, maker()), key)

    def test_77_same_malformed_input_has_identical_proof_across_settings(self):
        huge = 10 ** 9000
        packet = self.malformed_at("adp010_opportunity_id", huge)
        results = []
        for setting in (0, self.minimum_limit, self.original_limit):
            sys.set_int_max_str_digits(setting)
            results.append(self.assert_negative_total(packet, "adp010_opportunity_id"))
        self.assertEqual(results[0], results[1])
        self.assertEqual(results[1], results[2])
        self.assertEqual(results[0]["proof_sha256"], results[2]["proof_sha256"])

    def test_78_large_configured_limit_does_not_change_stable_classification(self):
        large_setting = 10000
        sys.set_int_max_str_digits(large_setting)
        value = 10 ** 12000
        self.assertFalse(r6._exact_int_stable_for_all_supported_limits(value))
        self.assert_negative_total(self.malformed_at("subject_id", value), "subject_id")

    def test_79_ordinary_json_safe_r5_behavior_is_exact(self):
        packets = [fixture()]
        p = fixture(); p["execution_scope"] = "PROJECT_CURRENT"; packets.append(p)
        p = fixture(); p["actor_id"] = 7; packets.append(p)
        p = fixture(); del p["world_id"]; packets.append(p)
        for index, packet in enumerate(packets):
            with self.subTest(index=index):
                self.assertEqual(
                    r6.evaluate_direct_positive_applicability(packet),
                    r6._r5.evaluate_direct_positive_applicability(packet),
                )

    def test_80_scope_authority_evidence_and_current_controls_remain_negative(self):
        packets = []
        p = fixture(); p["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong"; packets.append(p)
        p = fixture(); p["claimed_positive_applicability_source"] = "V554"; packets.append(p)
        p = fixture(); p["evidence"]["developmental_phase"]["stale"] = True; packets.append(p)
        p = fixture(); p["evidence"]["actor_activation"]["semantic_owner"] = "ROUTING"; packets.append(p)
        p = fixture(); p["execution_scope"] = "PROJECT_CURRENT"; packets.append(p)
        for index, packet in enumerate(packets):
            with self.subTest(index=index):
                result = r6.evaluate_direct_positive_applicability(packet)
                self.assertEqual(result["decision"], r6.NEGATIVE_DECISION, result)
                for effect in EFFECT_KEYS:
                    self.assertFalse(result[effect], effect)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CourtR6)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({
        "court": "OBL059_R6_GOVERNED_BOUNDED_COURT",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "successful": result.wasSuccessful(),
        "execution_scope": r6.SYNTHETIC_SCOPE,
        "project_current_state_created": False,
        "independent_review_performed": False,
    }, sort_keys=True))
    raise SystemExit(0 if result.wasSuccessful() else 1)
