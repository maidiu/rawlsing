"""Governed bounded court for OBL059 R5 large-integer receipt repair."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
R4_DIR = HERE.parent / "OBL059_POSITIVE_APPLICABILITY_R4"
R5_AUTHORITY = HERE / "positive_applicability_authority_r5.py"

r5_spec = importlib.util.spec_from_file_location("_obl059_r5_authority", R5_AUTHORITY)
if r5_spec is None or r5_spec.loader is None:
    raise RuntimeError(f"cannot load R5 authority: {R5_AUTHORITY}")
r5 = importlib.util.module_from_spec(r5_spec)
r5_spec.loader.exec_module(r5)

r4_court_path = R4_DIR / "governed_bounded_court_r4.py"
r4_spec = importlib.util.spec_from_file_location("_obl059_r4_court_for_r5", r4_court_path)
if r4_spec is None or r4_spec.loader is None:
    raise RuntimeError(f"cannot load R4 court: {r4_court_path}")
r4_court = importlib.util.module_from_spec(r4_spec)
r4_spec.loader.exec_module(r4_court)

# Route all inherited public evaluation points through the frozen R5 candidate.
r4_court.r4.evaluate_direct_positive_applicability = r5.evaluate_direct_positive_applicability
r4_court.r3_court.r3.evaluate_direct_positive_applicability = r5.evaluate_direct_positive_applicability
r4_court.r3_court.r2_court.r2.evaluate_direct_positive_applicability = r5.evaluate_direct_positive_applicability
r4_court.r3_court.r2_court.r1_court.evaluate_direct_positive_applicability = r5.evaluate_direct_positive_applicability

EFFECT_KEYS = tuple(r4_court.EFFECT_KEYS)


def fixture():
    return r4_court.fixture()


class CourtR5(r4_court.CourtR4):
    REQUIRED = tuple(r5._REQUIRED_BINDINGS)

    def assert_negative_receipt(self, packet, key):
        result = r5.evaluate_direct_positive_applicability(packet)
        self.assertEqual(result["decision"], r5.NEGATIVE_DECISION, result)
        self.assertEqual(result["reason"], f"MALFORMED_BINDING:{key}", result)
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64)
        self.assertNotIsInstance(result["bindings"][key], str)
        for effect in EFFECT_KEYS:
            self.assertFalse(result[effect], effect)
        return result

    def malformed_at(self, key, value):
        packet = fixture()
        packet[key] = value
        return packet

    def test_55_unrelated_programmer_errors_remain_visible(self):
        """Route the inherited preservation check to R5's actual R4 delegate."""
        original = r5._r4.evaluate_direct_positive_applicability

        def raise_type_error(_packet):
            raise TypeError("r5-deliberate-programmer-error")

        def raise_value_error(_packet):
            raise ValueError("r5-deliberate-programmer-error")

        def raise_runtime_error(_packet):
            raise RuntimeError("r5-deliberate-programmer-error")

        try:
            for exc_type, func in (
                (TypeError, raise_type_error),
                (ValueError, raise_value_error),
                (RuntimeError, raise_runtime_error),
            ):
                with self.subTest(exc_type=exc_type.__name__):
                    r5._r4.evaluate_direct_positive_applicability = func
                    with self.assertRaisesRegex(exc_type, "r5-deliberate-programmer-error"):
                        r5.evaluate_direct_positive_applicability(fixture())
        finally:
            r5._r4.evaluate_direct_positive_applicability = original

    def test_58_reproduced_large_positive_integer_closes_at_all_required_bindings(self):
        value = 10 ** 5000
        for key in self.REQUIRED:
            with self.subTest(key=key):
                result = self.assert_negative_receipt(self.malformed_at(key, value), key)
                projected = result["bindings"][key]
                self.assertEqual(
                    projected["__non_json_int__"],
                    "decimal_conversion_limit_exceeded",
                )
                self.assertEqual(projected["sign"], 1)

    def test_59_reproduced_large_negative_integer_closes_at_all_required_bindings(self):
        value = -(10 ** 5000)
        for key in self.REQUIRED:
            with self.subTest(key=key):
                result = self.assert_negative_receipt(self.malformed_at(key, value), key)
                projected = result["bindings"][key]
                self.assertEqual(projected["sign"], -1)
                self.assertGreater(projected["bit_length"], 0)

    def test_60_exact_runtime_decimal_boundary_is_classified_without_decimal_conversion(self):
        limit = sys.get_int_max_str_digits()
        if limit == 0:
            self.skipTest("runtime decimal integer conversion limit is disabled")

        safe_edge = 10 ** (limit - 1)
        unsafe_edge = 10 ** limit
        self.assertTrue(r5._exact_int_decimal_conversion_safe(safe_edge))
        self.assertTrue(r5._exact_int_decimal_conversion_safe(-safe_edge))
        self.assertFalse(r5._exact_int_decimal_conversion_safe(unsafe_edge))
        self.assertFalse(r5._exact_int_decimal_conversion_safe(-unsafe_edge))
        self.assertTrue(r5._exact_int_decimal_conversion_safe(0))
        self.assertTrue(r5._exact_int_decimal_conversion_safe(7))
        self.assertTrue(r5._exact_int_decimal_conversion_safe(-7))

    def test_61_magnitudes_beyond_reproduced_case_remain_total(self):
        values = (10 ** 5000, 10 ** 10000, -(10 ** 12000))
        for key in self.REQUIRED:
            for value in values:
                with self.subTest(key=key, bits=int.bit_length(value)):
                    result = self.assert_negative_receipt(self.malformed_at(key, value), key)
                    json.dumps(result, sort_keys=True)

    def test_62_nested_oversized_integers_in_exact_builtin_containers_close(self):
        makers = (
            lambda huge: {"huge": huge},
            lambda huge: ["prefix", huge],
            lambda huge: ("prefix", {"nested": huge}),
            lambda huge: {"outer": [1, {"inner": huge}]},
        )
        huge = 10 ** 7000
        for key in self.REQUIRED:
            for maker in makers:
                with self.subTest(key=key, maker=maker.__name__):
                    result = self.assert_negative_receipt(self.malformed_at(key, maker(huge)), key)
                    json.dumps(result, sort_keys=True)

    def test_63_repeated_oversized_integer_receipts_and_proofs_are_deterministic(self):
        for key in self.REQUIRED:
            with self.subTest(key=key):
                value = 10 ** 6000
                a = self.assert_negative_receipt(self.malformed_at(key, value), key)
                b = self.assert_negative_receipt(self.malformed_at(key, value), key)
                self.assertEqual(a, b)
                self.assertEqual(a["proof_sha256"], b["proof_sha256"])

    def test_64_distinct_oversized_integer_values_remain_distinguishable(self):
        first_value = 10 ** 6000
        second_value = first_value + 1
        first = self.assert_negative_receipt(self.malformed_at("actor_id", first_value), "actor_id")
        second = self.assert_negative_receipt(self.malformed_at("actor_id", second_value), "actor_id")
        self.assertEqual(
            first["bindings"]["actor_id"]["bit_length"],
            second["bindings"]["actor_id"]["bit_length"],
        )
        self.assertNotEqual(
            first["bindings"]["actor_id"]["binary_magnitude_sha256"],
            second["bindings"]["actor_id"]["binary_magnitude_sha256"],
        )
        self.assertNotEqual(first["proof_sha256"], second["proof_sha256"])

    def test_65_zero_small_and_ordinary_integers_preserve_exact_r4_behavior(self):
        values = (0, 1, -1, 7, -7, 123456789)
        for key in self.REQUIRED:
            for value in values:
                with self.subTest(key=key, value=value):
                    packet = self.malformed_at(key, value)
                    self.assertEqual(
                        r5.evaluate_direct_positive_applicability(packet),
                        r5._r4.evaluate_direct_positive_applicability(packet),
                    )

    def test_66_oversized_integer_projection_never_becomes_identifier_text(self):
        value = 10 ** 9000
        for key in self.REQUIRED:
            with self.subTest(key=key):
                result = self.assert_negative_receipt(self.malformed_at(key, value), key)
                projected = result["bindings"][key]
                self.assertIsInstance(projected, dict)
                self.assertNotIsInstance(projected, str)
                self.assertNotEqual(result["decision"], r5.POSITIVE_DECISION)
                self.assertEqual(len(projected["binary_magnitude_sha256"]), 64)

    def test_67_positive_and_negative_json_safe_controls_remain_exactly_r4(self):
        positive = fixture()
        negative = fixture()
        negative["execution_scope"] = "PROJECT_CURRENT"
        for packet in (positive, negative):
            self.assertEqual(
                r5.evaluate_direct_positive_applicability(packet),
                r5._r4.evaluate_direct_positive_applicability(packet),
            )

    def test_68_r5_revision_identity_is_exact(self):
        self.assertEqual(
            r5.R5_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R5",
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CourtR5)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({
        "court": "OBL059_R5_GOVERNED_BOUNDED_COURT",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "successful": result.wasSuccessful(),
        "execution_scope": r5.SYNTHETIC_SCOPE,
        "project_current_state_created": False,
        "independent_review_performed": False,
    }, sort_keys=True))
    raise SystemExit(0 if result.wasSuccessful() else 1)
