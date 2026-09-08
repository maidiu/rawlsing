"""Governed bounded court for OBL059 R9 consistency and receipt-totality repair."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from collections.abc import Mapping
from pathlib import Path

HERE = Path(__file__).resolve().parent
R8_DIR = HERE.parent / "OBL059_POSITIVE_APPLICABILITY_R8"
R9_AUTHORITY = HERE / "positive_applicability_authority_r9.py"

r9_spec = importlib.util.spec_from_file_location("_obl059_r9_authority", R9_AUTHORITY)
if r9_spec is None or r9_spec.loader is None:
    raise RuntimeError(f"cannot load R9 authority: {R9_AUTHORITY}")
r9 = importlib.util.module_from_spec(r9_spec)
r9_spec.loader.exec_module(r9)

r8_court_path = R8_DIR / "governed_bounded_court_r8.py"
r8_spec = importlib.util.spec_from_file_location("_obl059_r8_court_for_r9", r8_court_path)
if r8_spec is None or r8_spec.loader is None:
    raise RuntimeError(f"cannot load R8 court: {r8_court_path}")
r8_court = importlib.util.module_from_spec(r8_spec)
r8_spec.loader.exec_module(r8_court)

r9._r8 = r8_court.r8
r9._r7 = r8_court.r8._r7
r9._r6 = r9._r7._r6
r9._r1 = r9._r6._r5._r4._r3._r2._r1
FROZEN_R8_EVALUATE = r8_court.r8.evaluate_direct_positive_applicability

r8_court.r8.evaluate_direct_positive_applicability = r9.evaluate_direct_positive_applicability
r8_court.r7_wrapper.module.r6_court.r6.evaluate_direct_positive_applicability = r9.evaluate_direct_positive_applicability
r8_court.r7_wrapper.module.r6_court.r5_court.r5.evaluate_direct_positive_applicability = r9.evaluate_direct_positive_applicability
r8_court.r7_wrapper.module.r6_court.r5_court.r4_court.r4.evaluate_direct_positive_applicability = r9.evaluate_direct_positive_applicability
r8_court.r7_wrapper.module.r6_court.r5_court.r4_court.r3_court.r3.evaluate_direct_positive_applicability = r9.evaluate_direct_positive_applicability
r8_court.r7_wrapper.module.r6_court.r5_court.r4_court.r3_court.r2_court.r2.evaluate_direct_positive_applicability = r9.evaluate_direct_positive_applicability
r8_court.r7_wrapper.module.r6_court.r5_court.r4_court.r3_court.r2_court.r1_court.evaluate_direct_positive_applicability = r9.evaluate_direct_positive_applicability

EFFECT_KEYS = tuple(r8_court.EFFECT_KEYS)


def fixture():
    return r8_court.fixture()


class MutatingMapping(Mapping):
    def __init__(self, data, callback):
        self._data = dict(data)
        self._callback = callback
        self._fired = False
        self.keys_calls = 0

    def _fire(self):
        if not self._fired:
            self._fired = True
            self._callback()

    def keys(self):
        self.keys_calls += 1
        self._fire()
        return list(self._data.keys())

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)


class CountingMapping(Mapping):
    def __init__(self, data):
        self._data = dict(data)
        self.keys_calls = 0

    def keys(self):
        self.keys_calls += 1
        return list(self._data.keys())

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)


NODE_REASONS = {
    "opportunity": "OPPORTUNITY_BINDING_MISSING_OR_MALFORMED",
    "evidence": "EVIDENCE_MISSING_OR_MALFORMED",
    "subject_classification": "STRUCTURAL_CLASSIFICATION_EVIDENCE_MISSING",
    "actor_activation": "ACTOR_ACTIVATION_EVIDENCE_MISSING",
    "developmental_phase": "DEVELOPMENTAL_PHASE_EVIDENCE_MISSING",
}


def node_value(packet, node):
    if node in ("opportunity", "evidence"):
        return packet[node]
    return packet["evidence"][node]


def install_node(packet, node, value):
    if node in ("opportunity", "evidence"):
        packet[node] = value
    else:
        packet["evidence"][node] = value


class CourtR9(r8_court.CourtR8):
    def assert_no_effect(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def assert_negative(self, packet, reason=None):
        try:
            result = r9.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(f"R9 commissioned negative case raised {type(exc).__name__}: {exc}")
        self.assertEqual(result["decision"], r9.NEGATIVE_DECISION, result)
        if reason is not None:
            self.assertEqual(result["reason"], reason, result)
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64)
        self.assert_no_effect(result)
        return result

    def test_106_exact_r8_primary_cross_node_case_stays_negative(self):
        packet = fixture()
        packet["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"
        valid_actor = copy.deepcopy(fixture()["evidence"]["actor_activation"])
        opportunity_data = copy.deepcopy(packet["opportunity"])

        def replace_later_actor():
            packet["evidence"]["actor_activation"] = valid_actor

        packet["opportunity"] = MutatingMapping(opportunity_data, replace_later_actor)
        result = self.assert_negative(packet, "ACTOR_ACTIVATION_WRONG_AUTHORITY")
        self.assertEqual(packet["opportunity"].keys_calls, 1)

    def test_107_top_level_mutation_directions_use_precaptured_nodes(self):
        packet = fixture()
        packet["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-world"
        valid_opportunity = copy.deepcopy(fixture()["opportunity"])
        evidence_data = copy.deepcopy(packet["evidence"])

        def replace_opportunity():
            packet["opportunity"] = valid_opportunity

        packet["evidence"] = MutatingMapping(evidence_data, replace_opportunity)
        self.assert_negative(packet, "OPPORTUNITY_SCOPE_MISMATCH:world_id")

        packet = fixture()
        packet["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"
        valid_evidence = copy.deepcopy(fixture()["evidence"])
        opportunity_data = copy.deepcopy(packet["opportunity"])

        def replace_evidence():
            packet["evidence"] = valid_evidence

        packet["opportunity"] = MutatingMapping(opportunity_data, replace_evidence)
        self.assert_negative(packet, "ACTOR_ACTIVATION_WRONG_AUTHORITY")

    def test_108_component_mutation_directions_use_precaptured_components(self):
        packet = fixture()
        packet["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"
        valid_actor = copy.deepcopy(fixture()["evidence"]["actor_activation"])
        classification_data = copy.deepcopy(packet["evidence"]["subject_classification"])

        def replace_actor():
            packet["evidence"]["actor_activation"] = valid_actor

        packet["evidence"]["subject_classification"] = MutatingMapping(
            classification_data, replace_actor
        )
        self.assert_negative(packet, "ACTOR_ACTIVATION_WRONG_AUTHORITY")

        packet = fixture()
        packet["evidence"]["subject_classification"]["predicate"] = "WRONG_PREDICATE"
        valid_classification = copy.deepcopy(fixture()["evidence"]["subject_classification"])
        phase_data = copy.deepcopy(packet["evidence"]["developmental_phase"])

        def replace_classification():
            packet["evidence"]["subject_classification"] = valid_classification

        packet["evidence"]["developmental_phase"] = MutatingMapping(
            phase_data, replace_classification
        )
        self.assert_negative(packet, "SUBJECT_CLASSIFICATION_PREDICATE_MISMATCH")

        packet = fixture()
        packet["evidence"]["developmental_phase"]["phase"] = "V3DP_OTHER"
        valid_phase = copy.deepcopy(fixture()["evidence"]["developmental_phase"])
        actor_data = copy.deepcopy(packet["evidence"]["actor_activation"])

        def replace_phase():
            packet["evidence"]["developmental_phase"] = valid_phase

        packet["evidence"]["actor_activation"] = MutatingMapping(actor_data, replace_phase)
        self.assert_negative(packet, "DEVELOPMENTAL_PHASE_NOT_ACTIVE")

    def test_109_outer_plus_nested_mutation_composes_without_semantic_rewrite(self):
        packet = fixture()
        packet["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"
        valid_actor = copy.deepcopy(fixture()["evidence"]["actor_activation"])
        opportunity_data = copy.deepcopy(packet["opportunity"])

        def replace_actor():
            packet["evidence"]["actor_activation"] = valid_actor

        packet["opportunity"] = MutatingMapping(opportunity_data, replace_actor)
        outer = r8_court.r7_wrapper.module.CarrierMapping(packet)
        self.assert_negative(outer, "ACTOR_ACTIVATION_WRONG_AUTHORITY")

    def test_110_aliased_custom_carrier_is_snapshotted_once(self):
        packet = fixture()
        actor_data = copy.deepcopy(packet["evidence"]["actor_activation"])
        shared = CountingMapping(actor_data)
        packet["evidence"]["actor_activation"] = shared
        packet["evidence"]["developmental_phase"] = shared
        self.assert_negative(packet)
        self.assertEqual(shared.keys_calls, 1)

    def test_111_all_five_stable_custom_mappings_preserve_exact_dict_positive(self):
        exact = fixture()
        packet = fixture()
        packet["opportunity"] = r8_court.StableNestedMapping(packet["opportunity"])
        packet["evidence"]["subject_classification"] = r8_court.StableNestedMapping(packet["evidence"]["subject_classification"])
        packet["evidence"]["actor_activation"] = r8_court.StableNestedMapping(packet["evidence"]["actor_activation"])
        packet["evidence"]["developmental_phase"] = r8_court.StableNestedMapping(packet["evidence"]["developmental_phase"])
        packet["evidence"] = r8_court.StableNestedMapping(packet["evidence"])
        self.assertEqual(
            r9.evaluate_direct_positive_applicability(packet),
            r9.evaluate_direct_positive_applicability(exact),
        )

    def test_112_actual_nested_snapshot_failures_are_field_specific(self):
        makers = (r8_court.ThrowKeysNested, r8_court.ThrowGetitemNested)
        nodes = (
            "opportunity",
            "evidence",
            "subject_classification",
            "actor_activation",
            "developmental_phase",
        )
        for node in nodes:
            for maker in makers:
                with self.subTest(node=node, maker=maker.__name__):
                    packet = fixture()
                    install_node(packet, node, maker(copy.deepcopy(node_value(packet, node))))
                    self.assert_negative(packet, NODE_REASONS[node])

    def test_113_nested_oversized_actor_id_returns_total_negative_receipt(self):
        def make_packet():
            packet = fixture()
            actor = copy.deepcopy(packet["evidence"]["actor_activation"])
            actor["actor_id"] = 10 ** 5000
            packet["evidence"]["actor_activation"] = r8_court.StableNestedMapping(actor)
            return packet

        first = self.assert_negative(make_packet(), "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id")
        second = self.assert_negative(make_packet(), "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id")
        self.assertEqual(first, second)
        self.assertEqual(first["proof_sha256"], second["proof_sha256"])

    def test_114_nested_integer_threshold_and_runtime_settings_are_stable(self):
        original_limit = sys.get_int_max_str_digits()
        minimum = int(sys.int_info.str_digits_check_threshold)
        threshold = r9._r6._STABLE_DECIMAL_THRESHOLD
        values = (
            threshold - 1,
            threshold,
            -threshold,
            10 ** 5000,
            -(10 ** 5000),
        )
        try:
            baseline = []
            sys.set_int_max_str_digits(0)
            for value in values:
                packet = fixture()
                packet["evidence"]["actor_activation"]["actor_id"] = value
                baseline.append(self.assert_negative(packet, "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id"))

            sys.set_int_max_str_digits(minimum)
            for index, value in enumerate(values):
                packet = fixture()
                packet["evidence"]["actor_activation"]["actor_id"] = value
                result = self.assert_negative(packet, "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id")
                self.assertEqual(result, baseline[index])
        finally:
            sys.set_int_max_str_digits(original_limit)

    def test_115_nested_builtin_structures_with_oversized_ints_are_total(self):
        huge = 10 ** 6000
        values = (
            {"nested": [huge]},
            ["prefix", huge],
            ("prefix", {"nested": huge}),
            {"set": {huge}},
            {"frozen": frozenset({huge})},
        )
        for value in values:
            with self.subTest(value_type=type(value).__name__):
                packet = fixture()
                packet["evidence"]["actor_activation"]["actor_id"] = value
                self.assert_negative(packet, "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id")

    def test_116_exact_dict_controls_remain_exactly_r8(self):
        cases = [fixture()]
        packet = fixture(); packet["execution_scope"] = "PROJECT_CURRENT"; cases.append(packet)
        packet = fixture(); packet["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"; cases.append(packet)
        packet = fixture(); packet["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong"; cases.append(packet)
        for index, packet in enumerate(cases):
            with self.subTest(index=index):
                self.assertEqual(
                    r9.evaluate_direct_positive_applicability(copy.deepcopy(packet)),
                    FROZEN_R8_EVALUATE(copy.deepcopy(packet)),
                )

    def test_117_unrelated_error_after_successful_preparation_remains_visible(self):
        original = r9._r7.evaluate_direct_positive_applicability
        packet = fixture()
        packet["opportunity"] = r8_court.StableNestedMapping(packet["opportunity"])
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r9-post-preparation-programmer-error")
                r9._r7.evaluate_direct_positive_applicability = deliberate
                with self.assertRaisesRegex(exc_type, "r9-post-preparation-programmer-error"):
                    r9.evaluate_direct_positive_applicability(packet)
        finally:
            r9._r7.evaluate_direct_positive_applicability = original

    def test_118_r9_revision_identity_is_exact(self):
        self.assertEqual(
            r9.R9_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R9",
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CourtR9)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({
        "court": "OBL059_R9_GOVERNED_BOUNDED_COURT",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "successful": result.wasSuccessful(),
        "execution_scope": r9.SYNTHETIC_SCOPE,
        "project_current_state_created": False,
        "independent_review_performed": False,
    }, sort_keys=True))
    raise SystemExit(0 if result.wasSuccessful() else 1)
