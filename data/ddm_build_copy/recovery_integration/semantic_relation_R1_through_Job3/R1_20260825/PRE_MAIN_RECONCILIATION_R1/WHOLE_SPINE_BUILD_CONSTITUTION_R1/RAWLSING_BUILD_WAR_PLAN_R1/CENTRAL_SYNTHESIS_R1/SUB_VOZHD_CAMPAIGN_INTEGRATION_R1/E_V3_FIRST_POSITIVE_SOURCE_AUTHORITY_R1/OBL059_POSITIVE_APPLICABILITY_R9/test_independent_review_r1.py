"""Fresh independent review for frozen OBL059 R9.

Review-only. This file does not modify or repair the frozen candidate.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / "positive_applicability_authority_r9.py"

spec = importlib.util.spec_from_file_location("_obl059_r9_independent_target", CANDIDATE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load frozen R9 candidate: {CANDIDATE}")
r9 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r9)

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
    actor = "urn:rawlsing:noncurrent-synthetic:v3:actor:obl059:r9-independent"
    world = "urn:rawlsing:noncurrent-synthetic:v3:world:obl059:r9-independent"
    time = "urn:rawlsing:noncurrent-synthetic:v3:time:obl059:r9-independent"
    opportunity = "urn:rawlsing:noncurrent-synthetic:v3:adp010-opportunity:obl059:r9-independent"
    return {
        "execution_scope": r9.SYNTHETIC_SCOPE,
        "actor_id": actor,
        "subject_id": r9.FIRST_CANARY_SUBJECT_ID,
        "world_id": world,
        "time_id": time,
        "adp010_opportunity_id": opportunity,
        "opportunity": {
            "actor_id": actor,
            "subject_id": r9.FIRST_CANARY_SUBJECT_ID,
            "world_id": world,
            "time_id": time,
            "opportunity_id": opportunity,
            "consumer_rule": r9.ADP010_CONSUMER,
        },
        "evidence": {
            "subject_classification": {
                "semantic_owner": "NONCURRENT_SYNTHETIC_OBL048_COMPETENT_SOURCE@R9_REVIEW",
                "jurisdiction": "OBL048_SUBJECT_CLASSIFICATION",
                "subject_id": r9.FIRST_CANARY_SUBJECT_ID,
                "predicate": r9.SUBJECT_CLASSIFICATION_PREDICATE,
                "fresh_for_time_id": time,
                "stale": False,
            },
            "actor_activation": {
                "semantic_owner": r9.ADP007_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "state": "ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
            "developmental_phase": {
                "semantic_owner": r9.ADP008_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "phase": "V3DP_DEVELOPMENT_ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
        },
    }


class MutableCarrier(Mapping):
    def __init__(self, data):
        self._data = dict(data)
        self.keys_calls = 0
        self.getitem_calls = 0

    def keys(self):
        self.keys_calls += 1
        return list(self._data.keys())

    def __getitem__(self, key):
        self.getitem_calls += 1
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def replace(self, key, value):
        self._data[key] = value


class SideEffectCarrier(MutableCarrier):
    def __init__(self, data, callback):
        super().__init__(data)
        self._callback = callback
        self._fired = False

    def keys(self):
        self.keys_calls += 1
        if not self._fired:
            self._fired = True
            self._callback()
        return list(self._data.keys())


class FailKeysCarrier(MutableCarrier):
    def keys(self):
        self.keys_calls += 1
        raise RuntimeError("independent-review-keys-failure")


class FailGetitemCarrier(MutableCarrier):
    def __getitem__(self, key):
        self.getitem_calls += 1
        raise RuntimeError("independent-review-getitem-failure")


class OuterCarrier(Mapping):
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


class OBL059R9IndependentReview(unittest.TestCase):
    def assert_no_effect(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def assert_negative(self, packet, reason=None):
        try:
            result = r9.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(
                "commissioned negative case raised instead of returning a receipt: "
                f"{type(exc).__name__}: {exc}"
            )
        self.assertEqual(result["decision"], r9.NEGATIVE_DECISION, result)
        if reason is not None:
            self.assertEqual(result["reason"], reason, result)
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64, result)
        self.assert_no_effect(result)
        return result

    def test_01_revision_and_positive_negative_controls(self):
        self.assertEqual(
            r9.R9_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R9",
        )
        positive = r9.evaluate_direct_positive_applicability(fixture())
        self.assertEqual(positive["decision"], r9.POSITIVE_DECISION, positive)
        self.assert_no_effect(positive)

        negative = fixture()
        negative["execution_scope"] = "PROJECT_CURRENT"
        self.assert_negative(negative, "PROJECT_CURRENT_ISSUANCE_FORBIDDEN_IN_R1")

    def test_02_exact_r8_parent_slot_case_remains_negative(self):
        packet = fixture()
        packet["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"
        valid_actor = copy.deepcopy(fixture()["evidence"]["actor_activation"])
        opportunity_data = copy.deepcopy(packet["opportunity"])

        def replace_parent_slot():
            packet["evidence"]["actor_activation"] = valid_actor

        packet["opportunity"] = SideEffectCarrier(opportunity_data, replace_parent_slot)
        self.assert_negative(packet, "ACTOR_ACTIVATION_WRONG_AUTHORITY")

    def test_03_evidence_snapshot_cannot_rewrite_captured_custom_opportunity_contents(self):
        packet = fixture()
        correct_world = packet["world_id"]

        wrong_opportunity = copy.deepcopy(packet["opportunity"])
        wrong_opportunity["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-world"
        opportunity_carrier = MutableCarrier(wrong_opportunity)
        packet["opportunity"] = opportunity_carrier

        evidence_data = copy.deepcopy(packet["evidence"])

        def make_opportunity_valid_before_its_snapshot():
            opportunity_carrier.replace("world_id", correct_world)

        packet["evidence"] = SideEffectCarrier(
            evidence_data,
            make_opportunity_valid_before_its_snapshot,
        )
        self.assert_negative(packet, "OPPORTUNITY_SCOPE_MISMATCH:world_id")

    def test_04_opportunity_snapshot_cannot_rewrite_captured_actor_contents(self):
        packet = fixture()
        actor_data = copy.deepcopy(packet["evidence"]["actor_activation"])
        actor_data["semantic_owner"] = "WRONG_AUTHORITY"
        actor_carrier = MutableCarrier(actor_data)
        packet["evidence"]["actor_activation"] = actor_carrier

        opportunity_data = copy.deepcopy(packet["opportunity"])

        def make_actor_valid_before_actor_snapshot():
            actor_carrier.replace("semantic_owner", r9.ADP007_OWNER)

        packet["opportunity"] = SideEffectCarrier(
            opportunity_data,
            make_actor_valid_before_actor_snapshot,
        )
        self.assert_negative(packet, "ACTOR_ACTIVATION_WRONG_AUTHORITY")

    def test_05_component_snapshot_cannot_rewrite_later_component_contents(self):
        packet = fixture()
        actor_data = copy.deepcopy(packet["evidence"]["actor_activation"])
        actor_data["semantic_owner"] = "WRONG_AUTHORITY"
        actor_carrier = MutableCarrier(actor_data)
        packet["evidence"]["actor_activation"] = actor_carrier

        classification_data = copy.deepcopy(packet["evidence"]["subject_classification"])

        def make_actor_valid_before_actor_snapshot():
            actor_carrier.replace("semantic_owner", r9.ADP007_OWNER)

        packet["evidence"]["subject_classification"] = SideEffectCarrier(
            classification_data,
            make_actor_valid_before_actor_snapshot,
        )
        self.assert_negative(packet, "ACTOR_ACTIVATION_WRONG_AUTHORITY")

    def test_06_later_component_mutation_does_not_change_already_frozen_earlier_component(self):
        packet = fixture()
        classification_data = copy.deepcopy(packet["evidence"]["subject_classification"])
        classification_data["predicate"] = "WRONG_PREDICATE"
        classification_carrier = MutableCarrier(classification_data)
        packet["evidence"]["subject_classification"] = classification_carrier

        phase_data = copy.deepcopy(packet["evidence"]["developmental_phase"])

        def make_classification_valid_late():
            classification_carrier.replace(
                "predicate",
                r9.SUBJECT_CLASSIFICATION_PREDICATE,
            )

        packet["evidence"]["developmental_phase"] = SideEffectCarrier(
            phase_data,
            make_classification_valid_late,
        )
        self.assert_negative(packet, "SUBJECT_CLASSIFICATION_PREDICATE_MISMATCH")

    def test_07_aliasing_shared_carrier_is_snapshotted_once(self):
        packet = fixture()
        shared = MutableCarrier(copy.deepcopy(packet["evidence"]["actor_activation"]))
        packet["evidence"]["actor_activation"] = shared
        packet["evidence"]["developmental_phase"] = shared
        self.assert_negative(packet)
        self.assertEqual(shared.keys_calls, 1)

    def test_08_stable_custom_mapping_equivalence_all_consumed_nodes(self):
        exact = fixture()
        for node in (
            "opportunity",
            "evidence",
            "subject_classification",
            "actor_activation",
            "developmental_phase",
        ):
            packet = fixture()
            install_node(packet, node, MutableCarrier(copy.deepcopy(node_value(packet, node))))
            with self.subTest(node=node):
                self.assertEqual(
                    r9.evaluate_direct_positive_applicability(packet),
                    r9.evaluate_direct_positive_applicability(copy.deepcopy(exact)),
                )

    def test_09_outer_and_nested_custom_mapping_composition(self):
        packet = fixture()
        packet["opportunity"] = MutableCarrier(copy.deepcopy(packet["opportunity"]))
        packet["evidence"]["actor_activation"] = MutableCarrier(
            copy.deepcopy(packet["evidence"]["actor_activation"])
        )
        result = r9.evaluate_direct_positive_applicability(OuterCarrier(packet))
        baseline = r9.evaluate_direct_positive_applicability(fixture())
        self.assertEqual(result, baseline)

    def test_10_invoked_snapshot_failures_are_field_specific_and_deterministic(self):
        for node in (
            "opportunity",
            "evidence",
            "subject_classification",
            "actor_activation",
            "developmental_phase",
        ):
            for maker in (FailKeysCarrier, FailGetitemCarrier):
                with self.subTest(node=node, maker=maker.__name__):
                    packet = fixture()
                    install_node(
                        packet,
                        node,
                        maker(copy.deepcopy(node_value(packet, node))),
                    )
                    first = self.assert_negative(packet, NODE_REASONS[node])

                    packet2 = fixture()
                    install_node(
                        packet2,
                        node,
                        maker(copy.deepcopy(node_value(packet2, node))),
                    )
                    second = self.assert_negative(packet2, NODE_REASONS[node])
                    self.assertEqual(first, second)

    def test_11_nested_oversized_integer_receipt_is_total_across_settings(self):
        original_limit = sys.get_int_max_str_digits()
        minimum = int(sys.int_info.str_digits_check_threshold)

        def make_packet(value):
            packet = fixture()
            actor = copy.deepcopy(packet["evidence"]["actor_activation"])
            actor["actor_id"] = value
            packet["evidence"]["actor_activation"] = MutableCarrier(actor)
            return packet

        try:
            sys.set_int_max_str_digits(0)
            baseline = self.assert_negative(
                make_packet(10 ** 5000),
                "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id",
            )
            negative_baseline = self.assert_negative(
                make_packet(-(10 ** 5000)),
                "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id",
            )

            sys.set_int_max_str_digits(minimum)
            self.assertEqual(
                self.assert_negative(
                    make_packet(10 ** 5000),
                    "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id",
                ),
                baseline,
            )
            self.assertEqual(
                self.assert_negative(
                    make_packet(-(10 ** 5000)),
                    "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id",
                ),
                negative_baseline,
            )
        finally:
            sys.set_int_max_str_digits(original_limit)

    def test_12_nested_stable_threshold_neighbors_and_structures_are_total(self):
        threshold = r9._r6._STABLE_DECIMAL_THRESHOLD
        values = (
            threshold - 1,
            threshold,
            -threshold,
            {"nested": [10 ** 5000]},
            ["prefix", -(10 ** 5000)],
            ("prefix", {"nested": 10 ** 6000}),
            {"set": {10 ** 5000}},
            {"frozen": frozenset({-(10 ** 5000)})},
        )
        for value in values:
            with self.subTest(value_type=type(value).__name__):
                packet = fixture()
                actor = copy.deepcopy(packet["evidence"]["actor_activation"])
                actor["actor_id"] = value
                packet["evidence"]["actor_activation"] = MutableCarrier(actor)
                self.assert_negative(
                    packet,
                    "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id",
                )

    def test_13_wrong_scope_authority_stale_and_adjacent_fields_remain_negative(self):
        cases = []
        p = fixture()
        p["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-world"
        cases.append(p)

        p = fixture()
        p["claimed_positive_applicability_source"] = "V554"
        cases.append(p)

        p = fixture()
        p["evidence"]["developmental_phase"]["stale"] = True
        cases.append(p)

        p = fixture()
        p["evidence"]["actor_activation"]["semantic_owner"] = "ROUTING"
        cases.append(p)

        for index, packet in enumerate(cases):
            with self.subTest(index=index):
                self.assert_negative(packet)

        p = fixture()
        del p["evidence"]
        p.update(
            {
                "classification": "public clinic",
                "routing": "eligible",
                "occurrence": True,
                "causal_use_permission": True,
                "contact_witness_independence": True,
                "adp010_realized": True,
                "narrative_plausibility": "obvious",
            }
        )
        self.assert_negative(p, "EVIDENCE_MISSING_OR_MALFORMED")

    def test_14_unrelated_errors_after_successful_preparation_remain_visible(self):
        original = r9._r7.evaluate_direct_positive_applicability
        packet = fixture()
        packet["opportunity"] = MutableCarrier(copy.deepcopy(packet["opportunity"]))
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("independent-r9-deliberate-programmer-error")
                r9._r7.evaluate_direct_positive_applicability = deliberate
                with self.assertRaisesRegex(
                    exc_type,
                    "independent-r9-deliberate-programmer-error",
                ):
                    r9.evaluate_direct_positive_applicability(packet)
        finally:
            r9._r7.evaluate_direct_positive_applicability = original

    def test_15_repeated_and_concurrent_exact_dict_evaluation_is_deterministic(self):
        packet = fixture()
        baseline = r9.evaluate_direct_positive_applicability(copy.deepcopy(packet))
        repeated = [
            r9.evaluate_direct_positive_applicability(copy.deepcopy(packet))
            for _ in range(8)
        ]
        self.assertTrue(all(result == baseline for result in repeated))

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(
                executor.map(
                    lambda _: r9.evaluate_direct_positive_applicability(
                        copy.deepcopy(packet)
                    ),
                    range(16),
                )
            )
        self.assertTrue(all(result == baseline for result in results))

    def test_16_no_current_effects_on_reviewed_positive_and_negative_paths(self):
        positive = r9.evaluate_direct_positive_applicability(fixture())
        self.assertEqual(positive["decision"], r9.POSITIVE_DECISION)
        self.assert_no_effect(positive)

        negative = fixture()
        negative["execution_scope"] = "PROJECT_CURRENT"
        result = self.assert_negative(
            negative,
            "PROJECT_CURRENT_ISSUANCE_FORBIDDEN_IN_R1",
        )
        self.assert_no_effect(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
