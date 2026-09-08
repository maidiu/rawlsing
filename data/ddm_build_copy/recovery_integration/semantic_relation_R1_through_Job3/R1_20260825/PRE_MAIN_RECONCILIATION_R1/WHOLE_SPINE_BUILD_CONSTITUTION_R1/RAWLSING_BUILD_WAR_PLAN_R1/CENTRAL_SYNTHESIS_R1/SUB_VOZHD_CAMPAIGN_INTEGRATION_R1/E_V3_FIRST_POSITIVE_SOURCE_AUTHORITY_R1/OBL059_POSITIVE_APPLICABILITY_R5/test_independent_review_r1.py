"""Fresh independent review for frozen OBL059 R5 POSITIVE_APPLICABILITY candidate.

Review-only. This file does not repair or modify the frozen candidate.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import threading
import time
import unittest
from collections.abc import Mapping
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / "positive_applicability_authority_r5.py"

spec = importlib.util.spec_from_file_location("_obl059_r5_independent_review_target", CANDIDATE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load frozen R5 candidate: {CANDIDATE}")
r5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r5)

EFFECT_KEYS = (
    "project_current_state_created",
    "actor_created_or_activated",
    "adp008_phase_transition_executed",
    "adp019_occurrence_admitted",
    "causal_use_permission_owned",
    "contact_witness_independence_owned",
    "encounter_created",
    "oee_realized",
    "obl055_executed",
    "current_positive_obl056_installed",
)


def fixture():
    actor = "urn:rawlsing:noncurrent-synthetic:v3:actor:obl059:r5-independent"
    world = "urn:rawlsing:noncurrent-synthetic:v3:world:obl059:r5-independent"
    time_id = "urn:rawlsing:noncurrent-synthetic:v3:time:obl059:r5-independent"
    opportunity = "urn:rawlsing:noncurrent-synthetic:v3:adp010-opportunity:obl059:r5-independent"
    return {
        "execution_scope": r5.SYNTHETIC_SCOPE,
        "actor_id": actor,
        "subject_id": r5.FIRST_CANARY_SUBJECT_ID,
        "world_id": world,
        "time_id": time_id,
        "adp010_opportunity_id": opportunity,
        "opportunity": {
            "actor_id": actor,
            "subject_id": r5.FIRST_CANARY_SUBJECT_ID,
            "world_id": world,
            "time_id": time_id,
            "opportunity_id": opportunity,
            "consumer_rule": r5.ADP010_CONSUMER,
        },
        "evidence": {
            "subject_classification": {
                "semantic_owner": "NONCURRENT_SYNTHETIC_OBL048_COMPETENT_SOURCE@R5_REVIEW",
                "jurisdiction": "OBL048_SUBJECT_CLASSIFICATION",
                "subject_id": r5.FIRST_CANARY_SUBJECT_ID,
                "predicate": r5.SUBJECT_CLASSIFICATION_PREDICATE,
                "fresh_for_time_id": time_id,
                "stale": False,
            },
            "actor_activation": {
                "semantic_owner": r5.ADP007_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time_id,
                "state": "ACTIVE",
                "fresh_for_time_id": time_id,
                "stale": False,
            },
            "developmental_phase": {
                "semantic_owner": r5.ADP008_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time_id,
                "phase": "V3DP_DEVELOPMENT_ACTIVE",
                "fresh_for_time_id": time_id,
                "stale": False,
            },
        },
    }


class NoTouchMapping(Mapping):
    def __getitem__(self, key):
        raise AssertionError("custom __getitem__ must not run")

    def __iter__(self):
        raise AssertionError("custom __iter__ must not run")

    def __len__(self):
        raise AssertionError("custom __len__ must not run")

    def items(self):
        raise AssertionError("custom items must not run")

    def keys(self):
        raise AssertionError("custom keys must not run")

    def values(self):
        raise AssertionError("custom values must not run")

    def __repr__(self):
        raise AssertionError("custom repr must not run")

    def __str__(self):
        raise AssertionError("custom str must not run")

    def __hash__(self):
        raise AssertionError("custom hash must not run")

    def __eq__(self, other):
        raise AssertionError("custom equality must not run")

    def __lt__(self, other):
        raise AssertionError("custom ordering must not run")


class NoTouchSequence:
    def __iter__(self):
        raise AssertionError("custom sequence iteration must not run")

    def __len__(self):
        raise AssertionError("custom sequence length must not run")

    def __getitem__(self, key):
        raise AssertionError("custom sequence indexing must not run")

    def __repr__(self):
        raise AssertionError("custom sequence repr must not run")


class StableHashNoTouch:
    def __hash__(self):
        return 918273

    def __repr__(self):
        raise AssertionError("custom key repr must not run")

    def __str__(self):
        raise AssertionError("custom key str must not run")

    def __eq__(self, other):
        raise AssertionError("custom key equality must not run")

    def __lt__(self, other):
        raise AssertionError("custom key ordering must not run")


class IntSubclass(int):
    pass


class OBL059R5IndependentReview(unittest.TestCase):
    REQUIRED = tuple(r5._REQUIRED_BINDINGS)

    def setUp(self):
        self.original_limit = sys.get_int_max_str_digits()
        self.minimum_limit = sys.int_info.str_digits_check_threshold

    def tearDown(self):
        sys.set_int_max_str_digits(self.original_limit)

    def assert_no_effect(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def malformed_at(self, key, value):
        packet = fixture()
        packet[key] = value
        return packet

    def assert_negative(self, packet, reason=None):
        try:
            result = r5.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(
                "commissioned malformed input escaped negative-receipt construction: "
                f"{type(exc).__name__}: {exc}"
            )
        self.assertEqual(result["decision"], r5.NEGATIVE_DECISION)
        if reason is not None:
            self.assertEqual(result["reason"], reason)
        json.dumps(
            result,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )
        self.assertEqual(len(result["proof_sha256"]), 64)
        self.assert_no_effect(result)
        return result

    def test_01_positive_and_project_current_controls(self):
        positive = r5.evaluate_direct_positive_applicability(fixture())
        self.assertEqual(positive["decision"], r5.POSITIVE_DECISION)
        self.assert_no_effect(positive)

        packet = fixture()
        packet["execution_scope"] = "PROJECT_CURRENT"
        negative = r5.evaluate_direct_positive_applicability(packet)
        self.assertEqual(negative["decision"], r5.NEGATIVE_DECISION)
        self.assert_no_effect(negative)

    def test_02_active_integer_boundary_and_neighbors_all_required_bindings(self):
        sys.set_int_max_str_digits(self.minimum_limit)
        limit = sys.get_int_max_str_digits()
        safe_edge = (10 ** limit) - 1
        unsafe_edge = 10 ** limit
        values = (
            safe_edge,
            -safe_edge,
            unsafe_edge,
            -unsafe_edge,
            10 ** (limit + 1000),
            -(10 ** (limit + 1000)),
        )
        for key in self.REQUIRED:
            for index, value in enumerate(values):
                with self.subTest(key=key, index=index, bit_length=int.bit_length(value)):
                    self.assert_negative(
                        self.malformed_at(key, value),
                        f"MALFORMED_BINDING:{key}",
                    )

    def test_03_default_minimum_unlimited_and_cache_reuse(self):
        huge = 10 ** 5000
        first_minimum = None
        second_minimum = None
        try:
            sys.set_int_max_str_digits(self.minimum_limit)
            first_minimum = self.assert_negative(
                self.malformed_at("actor_id", huge),
                "MALFORMED_BINDING:actor_id",
            )

            sys.set_int_max_str_digits(0)
            unlimited = self.assert_negative(
                self.malformed_at("actor_id", huge),
                "MALFORMED_BINDING:actor_id",
            )
            self.assertNotEqual(unlimited["decision"], r5.POSITIVE_DECISION)

            sys.set_int_max_str_digits(self.minimum_limit)
            second_minimum = self.assert_negative(
                self.malformed_at("actor_id", huge),
                "MALFORMED_BINDING:actor_id",
            )
        finally:
            sys.set_int_max_str_digits(self.original_limit)

        self.assertEqual(first_minimum, second_minimum)

    def test_04_setting_change_after_structural_classification_remains_total(self):
        """Controlled barrier for a process-global setting change between phases."""
        huge = 10 ** 5000
        packet = self.malformed_at("actor_id", huge)
        original_requires = r5._requires_total_projection
        entered = threading.Event()
        release = threading.Event()
        state = {}
        worker = None

        def gated_requires(candidate_packet, reason):
            decision = original_requires(candidate_packet, reason)
            state["classification_result"] = decision
            entered.set()
            if not release.wait(timeout=10):
                raise RuntimeError("review barrier timeout")
            return decision

        def run_candidate():
            try:
                state["result"] = r5.evaluate_direct_positive_applicability(packet)
            except Exception as exc:
                state["exception_type"] = type(exc).__name__
                state["exception_text"] = str(exc)

        try:
            sys.set_int_max_str_digits(0)
            r5._requires_total_projection = gated_requires
            worker = threading.Thread(target=run_candidate, daemon=True)
            worker.start()
            self.assertTrue(entered.wait(timeout=10), "classification barrier not reached")
            self.assertFalse(state.get("classification_result"))

            # The same process-global setting may legitimately change while the
            # already-classified call is still in flight.
            sys.set_int_max_str_digits(self.minimum_limit)
            release.set()
            worker.join(timeout=10)
            self.assertFalse(worker.is_alive(), "review worker did not finish")

            if "exception_type" in state:
                self.fail(
                    "integer conversion setting changed after classification and "
                    "negative-receipt construction raised instead of remaining total: "
                    f"{state['exception_type']}: {state['exception_text']}"
                )

            result = state["result"]
            self.assertEqual(result["decision"], r5.NEGATIVE_DECISION)
            self.assertEqual(result["reason"], "MALFORMED_BINDING:actor_id")
            self.assert_no_effect(result)
        finally:
            release.set()
            if worker is not None:
                worker.join(timeout=1)
            r5._requires_total_projection = original_requires
            sys.set_int_max_str_digits(self.original_limit)

    def test_05_large_but_bounded_runtime_limit_is_proportionate(self):
        large_limit = 100_000
        sys.set_int_max_str_digits(large_limit)
        started = time.perf_counter()
        threshold = r5._decimal_safe_threshold(large_limit)
        elapsed = time.perf_counter() - started
        self.assertIsNotNone(threshold)
        self.assertGreater(int.bit_length(threshold), 300_000)
        self.assertLess(elapsed, 5.0)
        result = self.assert_negative(
            self.malformed_at("world_id", 10 ** 5000),
            "MALFORMED_BINDING:world_id",
        )
        self.assertEqual(result["decision"], r5.NEGATIVE_DECISION)

    def test_06_oversized_projection_sign_bit_length_and_binary_digest(self):
        sys.set_int_max_str_digits(self.minimum_limit)
        magnitude = (10 ** 5000) + 12345
        byte_length = max(1, (int.bit_length(magnitude) + 7) // 8)
        expected_digest = hashlib.sha256(
            int.to_bytes(magnitude, byte_length, "big", signed=False)
        ).hexdigest()

        positive = self.assert_negative(
            self.malformed_at("actor_id", magnitude),
            "MALFORMED_BINDING:actor_id",
        )
        negative = self.assert_negative(
            self.malformed_at("actor_id", -magnitude),
            "MALFORMED_BINDING:actor_id",
        )
        p = positive["bindings"]["actor_id"]
        n = negative["bindings"]["actor_id"]
        self.assertEqual(p["sign"], 1)
        self.assertEqual(n["sign"], -1)
        self.assertEqual(p["bit_length"], int.bit_length(magnitude))
        self.assertEqual(n["bit_length"], int.bit_length(magnitude))
        self.assertEqual(p["binary_magnitude_sha256"], expected_digest)
        self.assertEqual(n["binary_magnitude_sha256"], expected_digest)
        self.assertNotEqual(positive["proof_sha256"], negative["proof_sha256"])

    def test_07_repeated_and_nearby_oversized_values_are_stable_and_distinct(self):
        sys.set_int_max_str_digits(self.minimum_limit)
        one = 10 ** 6000
        two = one + 1
        first = self.assert_negative(self.malformed_at("time_id", one), "MALFORMED_BINDING:time_id")
        repeat = self.assert_negative(self.malformed_at("time_id", one), "MALFORMED_BINDING:time_id")
        nearby = self.assert_negative(self.malformed_at("time_id", two), "MALFORMED_BINDING:time_id")
        self.assertEqual(first, repeat)
        self.assertEqual(first["proof_sha256"], repeat["proof_sha256"])
        self.assertNotEqual(first["proof_sha256"], nearby["proof_sha256"])

    def test_08_builtin_container_combinations_with_oversized_integers(self):
        sys.set_int_max_str_digits(self.minimum_limit)
        huge = 10 ** 5000
        makers = (
            lambda: {huge: [huge, {"nested": -huge}]},
            lambda: [huge, {"nested": (huge, -huge)}],
            lambda: (huge, [huge, {"deep": huge}]),
            lambda: {huge, huge + 1},
            lambda: frozenset({huge, huge + 2}),
        )
        for key in self.REQUIRED:
            for index, maker in enumerate(makers):
                with self.subTest(key=key, index=index):
                    self.assert_negative(
                        self.malformed_at(key, maker()),
                        f"MALFORMED_BINDING:{key}",
                    )

    def test_09_cycles_shared_references_and_depth_with_oversized_integers(self):
        sys.set_int_max_str_digits(self.minimum_limit)
        huge = 10 ** 5000

        circular = [huge]
        circular.append(circular)

        left = [huge]
        right = {"left": left, "huge": huge}
        left.append(right)
        mutual = {"left": left, "right": right}

        shared_node = {"huge": huge}
        shared = [shared_node, shared_node, {"again": shared_node}]

        deep = huge
        for _ in range(96):
            deep = [deep]

        for index, value in enumerate((circular, mutual, shared, deep)):
            with self.subTest(index=index):
                self.assert_negative(
                    self.malformed_at("subject_id", value),
                    "MALFORMED_BINDING:subject_id",
                )

    def test_10_custom_protocol_objects_combined_with_oversized_integers(self):
        sys.set_int_max_str_digits(self.minimum_limit)
        huge = 10 ** 5000
        custom_key = StableHashNoTouch()
        values = (
            [huge, NoTouchMapping()],
            {"huge": huge, "custom": NoTouchSequence()},
            {custom_key: huge},
            (huge, NoTouchMapping(), {"nested": NoTouchSequence()}),
        )
        for key in self.REQUIRED:
            for index, value in enumerate(values):
                with self.subTest(key=key, index=index):
                    self.assert_negative(
                        self.malformed_at(key, value),
                        f"MALFORMED_BINDING:{key}",
                    )

    def test_11_int_subclass_bool_zero_and_ordinary_integer_boundaries(self):
        values = (
            IntSubclass(7),
            True,
            False,
            0,
            1,
            -1,
            123456789,
        )
        for key in self.REQUIRED:
            for index, value in enumerate(values):
                with self.subTest(key=key, index=index, type_name=type(value).__name__):
                    result = self.assert_negative(
                        self.malformed_at(key, value),
                        f"MALFORMED_BINDING:{key}",
                    )
                    self.assertNotEqual(result["decision"], r5.POSITIVE_DECISION)

    def test_12_float_nonfinite_string_bool_and_null_boundaries(self):
        values = (1.25, float("nan"), float("inf"), float("-inf"), True, False, None)
        for key in self.REQUIRED:
            for index, value in enumerate(values):
                with self.subTest(key=key, index=index, type_name=type(value).__name__):
                    result = self.assert_negative(
                        self.malformed_at(key, value),
                        f"MALFORMED_BINDING:{key}",
                    )
                    self.assertNotEqual(result["decision"], r5.POSITIVE_DECISION)

        # A valid identifier-shaped string is not a malformed primitive. It may
        # still be rejected later for exact scope mismatch, which is the expected
        # contract behavior.
        packet = fixture()
        packet["actor_id"] = "urn:rawlsing:noncurrent-synthetic:v3:actor:other"
        result = r5.evaluate_direct_positive_applicability(packet)
        self.assertEqual(result["decision"], r5.NEGATIVE_DECISION)
        self.assert_no_effect(result)

    def test_13_scope_source_evidence_stale_and_current_controls(self):
        cases = []
        packet = fixture(); packet["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong"; cases.append(packet)
        packet = fixture(); packet["claimed_positive_applicability_source"] = "V554"; cases.append(packet)
        packet = fixture(); packet["evidence"]["developmental_phase"]["stale"] = True; cases.append(packet)
        packet = fixture(); packet["evidence"]["actor_activation"]["semantic_owner"] = "CAN-001"; cases.append(packet)
        packet = fixture(); packet["evidence"]["subject_classification"]["predicate"] = "OTHER"; cases.append(packet)
        packet = fixture(); packet["execution_scope"] = "PROJECT_CURRENT"; cases.append(packet)
        for index, packet in enumerate(cases):
            with self.subTest(index=index):
                result = r5.evaluate_direct_positive_applicability(packet)
                self.assertEqual(result["decision"], r5.NEGATIVE_DECISION)
                self.assert_no_effect(result)

    def test_14_adjacent_claims_do_not_substitute_for_required_evidence(self):
        packet = fixture()
        del packet["evidence"]
        packet.update({
            "classification": "public clinic",
            "routing": "eligible",
            "occurrence": True,
            "causal_use_permission": True,
            "contact_witness_independence": True,
            "adp010_realization": True,
            "narrative_plausibility": "obvious",
        })
        result = r5.evaluate_direct_positive_applicability(packet)
        self.assertEqual(result["decision"], r5.NEGATIVE_DECISION)
        self.assert_no_effect(result)

    def test_15_unrelated_programmer_errors_remain_visible(self):
        original = r5._r4.evaluate_direct_positive_applicability
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r5-independent-deliberate-programmer-error")
                r5._r4.evaluate_direct_positive_applicability = deliberate
                with self.assertRaisesRegex(exc_type, "r5-independent-deliberate-programmer-error"):
                    r5.evaluate_direct_positive_applicability(fixture())
        finally:
            r5._r4.evaluate_direct_positive_applicability = original

    def test_16_revision_identity_and_no_current_effect_fields(self):
        self.assertEqual(
            r5.R5_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R5",
        )
        result = r5.evaluate_direct_positive_applicability(fixture())
        self.assert_no_effect(result)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(OBL059R5IndependentReview)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({
        "court": "OBL059_R5_FRESH_INDEPENDENT_REVIEW_R1",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "successful": result.wasSuccessful(),
        "execution_scope": r5.SYNTHETIC_SCOPE,
        "project_current_state_created": False,
        "repair_performed_by_reviewer": False,
        "second_review_commissioned": False,
    }, sort_keys=True))
    raise SystemExit(0 if result.wasSuccessful() else 1)
