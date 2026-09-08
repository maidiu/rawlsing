"""Fresh independent review for frozen OBL059 R6.

Review-only. This file does not modify or repair the frozen candidate.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
import threading
import unittest
from collections.abc import Mapping
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / "positive_applicability_authority_r6.py"

spec = importlib.util.spec_from_file_location("_obl059_r6_independent_target", CANDIDATE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load frozen R6 candidate: {CANDIDATE}")
r6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r6)

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
    actor = "urn:rawlsing:noncurrent-synthetic:v3:actor:obl059:r6-independent"
    world = "urn:rawlsing:noncurrent-synthetic:v3:world:obl059:r6-independent"
    time = "urn:rawlsing:noncurrent-synthetic:v3:time:obl059:r6-independent"
    opportunity = "urn:rawlsing:noncurrent-synthetic:v3:adp010-opportunity:obl059:r6-independent"
    return {
        "execution_scope": r6.SYNTHETIC_SCOPE,
        "actor_id": actor,
        "subject_id": r6.FIRST_CANARY_SUBJECT_ID,
        "world_id": world,
        "time_id": time,
        "adp010_opportunity_id": opportunity,
        "opportunity": {
            "actor_id": actor,
            "subject_id": r6.FIRST_CANARY_SUBJECT_ID,
            "world_id": world,
            "time_id": time,
            "opportunity_id": opportunity,
            "consumer_rule": r6.ADP010_CONSUMER,
        },
        "evidence": {
            "subject_classification": {
                "semantic_owner": "NONCURRENT_SYNTHETIC_OBL048_COMPETENT_SOURCE@R6_REVIEW",
                "jurisdiction": "OBL048_SUBJECT_CLASSIFICATION",
                "subject_id": r6.FIRST_CANARY_SUBJECT_ID,
                "predicate": r6.SUBJECT_CLASSIFICATION_PREDICATE,
                "fresh_for_time_id": time,
                "stale": False,
            },
            "actor_activation": {
                "semantic_owner": r6.ADP007_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "state": "ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
            "developmental_phase": {
                "semantic_owner": r6.ADP008_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "phase": "V3DP_DEVELOPMENT_ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
        },
    }


class ThrowingProtocolObject:
    def __iter__(self):
        raise RuntimeError("iter-must-not-run")
    def __len__(self):
        raise RuntimeError("len-must-not-run")
    def __getitem__(self, key):
        raise RuntimeError("getitem-must-not-run")
    def __repr__(self):
        raise RuntimeError("repr-must-not-run")
    def __str__(self):
        raise RuntimeError("str-must-not-run")
    def __hash__(self):
        raise RuntimeError("hash-must-not-run")
    def __eq__(self, other):
        raise RuntimeError("eq-must-not-run")
    def __lt__(self, other):
        raise RuntimeError("order-must-not-run")


class ThrowingValueMapping(Mapping):
    def __getitem__(self, key):
        raise RuntimeError("value-getitem-must-not-run")
    def __iter__(self):
        raise RuntimeError("value-iter-must-not-run")
    def __len__(self):
        raise RuntimeError("value-len-must-not-run")
    def items(self):
        raise RuntimeError("value-items-must-not-run")
    def keys(self):
        raise RuntimeError("value-keys-must-not-run")
    def __repr__(self):
        raise RuntimeError("value-repr-must-not-run")
    def __str__(self):
        raise RuntimeError("value-str-must-not-run")


class ThrowingPacketMapping(Mapping):
    """Mapping-shaped packet with valid backing data but caller-controlled traversal."""
    def __init__(self, data):
        self._data = data
    def __getitem__(self, key):
        return self._data[key]
    def __iter__(self):
        raise RuntimeError("packet-iter-must-not-run")
    def __len__(self):
        raise RuntimeError("packet-len-must-not-run")
    def keys(self):
        raise RuntimeError("packet-keys-must-not-run")
    def items(self):
        raise RuntimeError("packet-items-must-not-run")
    def __repr__(self):
        raise RuntimeError("packet-repr-must-not-run")
    def __str__(self):
        raise RuntimeError("packet-str-must-not-run")


class IntSubclass(int):
    def __repr__(self):
        raise RuntimeError("int-subclass-repr-must-not-run")
    def __str__(self):
        raise RuntimeError("int-subclass-str-must-not-run")


class OBL059R6IndependentReview(unittest.TestCase):
    REQUIRED = tuple(r6._REQUIRED_BINDINGS)

    def setUp(self):
        self.original_limit = sys.get_int_max_str_digits()
        self.minimum_limit = int(sys.int_info.str_digits_check_threshold)
        self.threshold = 10 ** self.minimum_limit

    def tearDown(self):
        sys.set_int_max_str_digits(self.original_limit)

    def malformed_at(self, key, value):
        packet = fixture()
        packet[key] = value
        return packet

    def assert_no_effect(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def assert_negative_total(self, packet, reason_prefix=None):
        try:
            result = r6.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(
                "commissioned malformed-input path raised instead of returning a negative receipt: "
                f"{type(exc).__name__}: {exc}"
            )
        self.assertEqual(result["decision"], r6.NEGATIVE_DECISION, result)
        if reason_prefix is not None:
            self.assertTrue(result["reason"].startswith(reason_prefix), result)
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64, result)
        self.assert_no_effect(result)
        return result

    def test_01_valid_positive_and_valid_negative_controls_prove_not_fail_all(self):
        positive = r6.evaluate_direct_positive_applicability(fixture())
        self.assertEqual(positive["decision"], r6.POSITIVE_DECISION, positive)
        self.assert_no_effect(positive)

        negative_packet = fixture()
        negative_packet["execution_scope"] = "PROJECT_CURRENT"
        negative = r6.evaluate_direct_positive_applicability(negative_packet)
        self.assertEqual(negative["decision"], r6.NEGATIVE_DECISION, negative)
        self.assert_no_effect(negative)

    def test_02_stable_threshold_neighbors_are_exact_for_positive_and_negative_values(self):
        below = self.threshold - 1
        at = self.threshold
        above = self.threshold + 1
        for setting_name, setting in (
            ("unlimited", 0),
            ("minimum", self.minimum_limit),
            ("larger", max(self.minimum_limit * 2, 1000)),
        ):
            sys.set_int_max_str_digits(setting)
            with self.subTest(setting=setting_name):
                self.assertTrue(r6._exact_int_stable_for_all_supported_limits(below))
                self.assertTrue(r6._exact_int_stable_for_all_supported_limits(-below))
                self.assertFalse(r6._exact_int_stable_for_all_supported_limits(at))
                self.assertFalse(r6._exact_int_stable_for_all_supported_limits(-at))
                self.assertFalse(r6._exact_int_stable_for_all_supported_limits(above))
                self.assertFalse(r6._exact_int_stable_for_all_supported_limits(-above))

    def test_03_unsafe_exact_integers_are_projected_before_inherited_evaluation(self):
        original = r6._r5.evaluate_direct_positive_applicability

        def must_not_run(_packet):
            raise RuntimeError("inherited-evaluation-must-not-run-for-unsafe-int")

        try:
            r6._r5.evaluate_direct_positive_applicability = must_not_run
            values = (self.threshold, -self.threshold, 10 ** 5000, -(10 ** 7000))
            for key in self.REQUIRED:
                for index, value in enumerate(values):
                    with self.subTest(key=key, case=index):
                        result = self.assert_negative_total(
                            self.malformed_at(key, value),
                            f"MALFORMED_BINDING:{key}",
                        )
                        self.assertEqual(
                            result["bindings"][key]["__non_json_int__"],
                            "decimal_conversion_limit_exceeded",
                        )
        finally:
            r6._r5.evaluate_direct_positive_applicability = original

    def test_04_zero_to_minimum_setting_change_during_same_evaluation_remains_total(self):
        packet = self.malformed_at("actor_id", 10 ** 5000)
        original_requires = r6._requires_total_projection_stable
        entered = threading.Event()
        release = threading.Event()
        state = {}

        def gated_requires(candidate_packet, reason):
            decision = original_requires(candidate_packet, reason)
            state["classification"] = decision
            entered.set()
            if not release.wait(timeout=10):
                raise RuntimeError("independent-review-barrier-timeout")
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
            self.assertTrue(entered.wait(timeout=10), "classification barrier not reached")
            self.assertTrue(state.get("classification"))
            sys.set_int_max_str_digits(self.minimum_limit)
            release.set()
            worker.join(timeout=10)
            self.assertFalse(worker.is_alive(), "review worker did not finish")
            self.assertNotIn("exception", state)
            result = state["result"]
            self.assertEqual(result["decision"], r6.NEGATIVE_DECISION)
            self.assert_no_effect(result)
            json.dumps(result, sort_keys=True)
        finally:
            release.set()
            r6._requires_total_projection_stable = original_requires

    def test_05_same_oversized_value_is_deterministic_across_supported_settings(self):
        value = 10 ** 5000
        results = []
        settings = (0, self.minimum_limit, max(self.minimum_limit * 2, 1000), 0)
        for setting in settings:
            sys.set_int_max_str_digits(setting)
            results.append(
                self.assert_negative_total(
                    self.malformed_at("world_id", value),
                    "MALFORMED_BINDING:world_id",
                )
            )
        for result in results[1:]:
            self.assertEqual(result, results[0])
            self.assertEqual(result["proof_sha256"], results[0]["proof_sha256"])

    def test_06_oversized_integer_diagnostic_sign_bit_length_digest_and_distinction_are_exact(self):
        magnitude = 10 ** 5000
        cases = (magnitude, -magnitude, magnitude + 1)
        results = []
        for index, value in enumerate(cases):
            with self.subTest(case=index):
                result = self.assert_negative_total(
                    self.malformed_at("time_id", value),
                    "MALFORMED_BINDING:time_id",
                )
                projected = result["bindings"]["time_id"]
                abs_value = value if value >= 0 else -value
                byte_length = max(1, (int.bit_length(abs_value) + 7) // 8)
                expected_digest = hashlib.sha256(
                    int.to_bytes(abs_value, byte_length, "big", signed=False)
                ).hexdigest()
                self.assertEqual(projected["sign"], -1 if value < 0 else 1)
                self.assertEqual(projected["bit_length"], int.bit_length(value))
                self.assertEqual(projected["binary_magnitude_sha256"], expected_digest)
                results.append(result)
        self.assertNotEqual(results[0]["proof_sha256"], results[1]["proof_sha256"])
        self.assertNotEqual(results[0]["proof_sha256"], results[2]["proof_sha256"])

    def test_07_nested_oversized_keys_values_cycles_shared_and_depth_forms_remain_total(self):
        huge = 10 ** 5000

        circular = []
        circular.append(circular)
        circular.append(huge)

        shared_node = [huge, -huge]
        shared = [shared_node, shared_node, {"node": shared_node}]

        deep = huge
        for _ in range(80):
            deep = [deep]

        makers = (
            lambda: {huge: "value", "nested": [-huge]},
            lambda: ["prefix", {"inner": huge}],
            lambda: ("prefix", {huge: [huge, -huge]}),
            lambda: {huge, huge + 1},
            lambda: frozenset({huge, huge + 1}),
            lambda: circular,
            lambda: shared,
            lambda: deep,
        )
        for key in self.REQUIRED:
            for index, maker in enumerate(makers):
                with self.subTest(key=key, case=index):
                    self.assert_negative_total(
                        self.malformed_at(key, maker()),
                        f"MALFORMED_BINDING:{key}",
                    )

    def test_08_adjacent_primitive_and_exact_int_subclass_cases_stay_negative_and_total(self):
        subclass_value = IntSubclass(10 ** 1000)
        values = (
            True,
            1.25,
            float("nan"),
            float("inf"),
            float("-inf"),
            b"bytes",
            {"set-value"},
            frozenset({"frozen-value"}),
            subclass_value,
            object(),
        )
        for key in self.REQUIRED:
            for index, value in enumerate(values):
                with self.subTest(key=key, case=index):
                    result = self.assert_negative_total(
                        self.malformed_at(key, value),
                        f"MALFORMED_BINDING:{key}",
                    )
                    self.assertNotEqual(result["decision"], r6.POSITIVE_DECISION)

    def test_09_custom_value_protocols_are_not_needed_for_negative_projection(self):
        values = (ThrowingProtocolObject(), ThrowingValueMapping())
        for key in self.REQUIRED:
            for index, value in enumerate(values):
                with self.subTest(key=key, case=index):
                    self.assert_negative_total(
                        self.malformed_at(key, value),
                        f"MALFORMED_BINDING:{key}",
                    )

    def test_10_custom_mapping_packet_with_oversized_binding_does_not_require_caller_traversal(self):
        packet_data = fixture()
        packet_data["actor_id"] = 10 ** 5000
        packet = ThrowingPacketMapping(packet_data)
        self.assert_negative_total(packet, "MALFORMED_BINDING:actor_id")

    def test_11_repeated_and_concurrent_evaluations_remain_total_while_setting_changes(self):
        huge = 10 ** 7000
        stop = threading.Event()
        toggler_errors = []
        worker_errors = []
        proof_sets = {key: set() for key in self.REQUIRED}

        def toggler():
            try:
                while not stop.is_set():
                    sys.set_int_max_str_digits(0)
                    sys.set_int_max_str_digits(self.minimum_limit)
            except Exception as exc:
                toggler_errors.append(exc)

        def evaluator(key):
            try:
                for _ in range(12):
                    result = r6.evaluate_direct_positive_applicability(self.malformed_at(key, huge))
                    if result["decision"] != r6.NEGATIVE_DECISION:
                        raise AssertionError("concurrent malformed input was not negative")
                    proof_sets[key].add(result["proof_sha256"])
                    self.assert_no_effect(result)
            except Exception as exc:
                worker_errors.append(exc)

        toggle_thread = threading.Thread(target=toggler, daemon=True)
        workers = [threading.Thread(target=evaluator, args=(key,), daemon=True) for key in self.REQUIRED]
        toggle_thread.start()
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join(timeout=15)
        stop.set()
        toggle_thread.join(timeout=10)

        self.assertFalse(toggle_thread.is_alive())
        self.assertTrue(all(not worker.is_alive() for worker in workers))
        self.assertEqual(toggler_errors, [])
        self.assertEqual(worker_errors, [])
        for key in self.REQUIRED:
            self.assertEqual(len(proof_sets[key]), 1, key)

    def test_12_ordinary_r5_semantics_are_preserved_for_json_safe_controls(self):
        packets = [fixture()]
        p = fixture(); p["execution_scope"] = "PROJECT_CURRENT"; packets.append(p)
        p = fixture(); p["actor_id"] = 7; packets.append(p)
        p = fixture(); del p["world_id"]; packets.append(p)
        for index, packet in enumerate(packets):
            with self.subTest(case=index):
                self.assertEqual(
                    r6.evaluate_direct_positive_applicability(packet),
                    r6._r5.evaluate_direct_positive_applicability(packet),
                )

    def test_13_scope_authority_evidence_current_and_adjacent_claim_controls_remain_negative(self):
        cases = []
        p = fixture(); p["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong"; cases.append(p)
        p = fixture(); p["claimed_positive_applicability_source"] = "V554"; cases.append(p)
        p = fixture(); p["evidence"]["developmental_phase"]["stale"] = True; cases.append(p)
        p = fixture(); p["evidence"]["actor_activation"]["semantic_owner"] = "ROUTING"; cases.append(p)
        p = fixture(); p["execution_scope"] = "PROJECT_CURRENT"; cases.append(p)
        p = fixture(); del p["evidence"]; p.update({
            "classification": "public clinic",
            "routing": "eligible",
            "occurrence": True,
            "causal_use_permission": True,
            "contact_witness_independence": True,
            "narrative_plausibility": "obvious",
        }); cases.append(p)
        for index, packet in enumerate(cases):
            with self.subTest(case=index):
                result = r6.evaluate_direct_positive_applicability(packet)
                self.assertEqual(result["decision"], r6.NEGATIVE_DECISION, result)
                self.assert_no_effect(result)

    def test_14_deliberate_unrelated_programmer_errors_remain_visible(self):
        original = r6._r5.evaluate_direct_positive_applicability
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("independent-r6-deliberate-programmer-error")
                r6._r5.evaluate_direct_positive_applicability = deliberate
                with self.assertRaisesRegex(exc_type, "independent-r6-deliberate-programmer-error"):
                    r6.evaluate_direct_positive_applicability(fixture())
        finally:
            r6._r5.evaluate_direct_positive_applicability = original

    def test_15_candidate_identity_and_stable_floor_are_exact(self):
        self.assertEqual(
            r6.R6_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R6",
        )
        self.assertEqual(
            r6._MIN_SUPPORTED_NONZERO_INT_STR_DIGITS,
            int(sys.int_info.str_digits_check_threshold),
        )
        self.assertEqual(
            r6._STABLE_DECIMAL_THRESHOLD,
            10 ** int(sys.int_info.str_digits_check_threshold),
        )

    def test_16_safe_threshold_neighbor_remains_encodable_under_minimum_setting(self):
        value = self.threshold - 1
        sys.set_int_max_str_digits(self.minimum_limit)
        for key in self.REQUIRED:
            with self.subTest(key=key):
                result = self.assert_negative_total(
                    self.malformed_at(key, value),
                    f"MALFORMED_BINDING:{key}",
                )
                self.assertNotIsInstance(result["bindings"][key], dict)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(OBL059R6IndependentReview)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({
        "court": "OBL059_R6_FRESH_INDEPENDENT_REVIEW_R1",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "successful": result.wasSuccessful(),
        "frozen_candidate": "5ca7380bd17b3dec271fe5a8c6bf22656f55b647",
        "review_count": 1,
        "repair_performed_by_reviewer": False,
        "project_current_state_created": False,
    }, sort_keys=True))
    raise SystemExit(0 if result.wasSuccessful() else 1)
