"""Fresh independent review for frozen OBL059 R8.

Review-only. This file does not repair or modify the frozen candidate.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from collections.abc import Mapping
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / "positive_applicability_authority_r8.py"

spec = importlib.util.spec_from_file_location("_obl059_r8_review_target", CANDIDATE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load frozen R8 candidate: {CANDIDATE}")
r8 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r8)

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

NODES = (
    "opportunity",
    "evidence",
    "subject_classification",
    "actor_activation",
    "developmental_phase",
)

FAILURE_REASONS = {
    "opportunity": "OPPORTUNITY_BINDING_MISSING_OR_MALFORMED",
    "evidence": "EVIDENCE_MISSING_OR_MALFORMED",
    "subject_classification": "STRUCTURAL_CLASSIFICATION_EVIDENCE_MISSING",
    "actor_activation": "ACTOR_ACTIVATION_EVIDENCE_MISSING",
    "developmental_phase": "DEVELOPMENTAL_PHASE_EVIDENCE_MISSING",
}


def fixture():
    actor = "urn:rawlsing:noncurrent-synthetic:v3:actor:obl059:r8-independent"
    world = "urn:rawlsing:noncurrent-synthetic:v3:world:obl059:r8-independent"
    time = "urn:rawlsing:noncurrent-synthetic:v3:time:obl059:r8-independent"
    opportunity = "urn:rawlsing:noncurrent-synthetic:v3:adp010-opportunity:obl059:r8-independent"
    return {
        "execution_scope": r8.SYNTHETIC_SCOPE,
        "actor_id": actor,
        "subject_id": r8.FIRST_CANARY_SUBJECT_ID,
        "world_id": world,
        "time_id": time,
        "adp010_opportunity_id": opportunity,
        "opportunity": {
            "actor_id": actor,
            "subject_id": r8.FIRST_CANARY_SUBJECT_ID,
            "world_id": world,
            "time_id": time,
            "opportunity_id": opportunity,
            "consumer_rule": r8.ADP010_CONSUMER,
        },
        "evidence": {
            "subject_classification": {
                "semantic_owner": "NONCURRENT_SYNTHETIC_OBL048_COMPETENT_SOURCE@R8_REVIEW",
                "jurisdiction": "OBL048_SUBJECT_CLASSIFICATION",
                "subject_id": r8.FIRST_CANARY_SUBJECT_ID,
                "predicate": r8.SUBJECT_CLASSIFICATION_PREDICATE,
                "fresh_for_time_id": time,
                "stale": False,
            },
            "actor_activation": {
                "semantic_owner": r8.ADP007_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "state": "ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
            "developmental_phase": {
                "semantic_owner": r8.ADP008_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "phase": "V3DP_DEVELOPMENT_ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
        },
    }


def node_value(packet, node):
    if node == "opportunity":
        return packet["opportunity"]
    if node == "evidence":
        return packet["evidence"]
    return packet["evidence"][node]


def install_node(packet, node, value):
    if node == "opportunity":
        packet["opportunity"] = value
    elif node == "evidence":
        packet["evidence"] = value
    else:
        packet["evidence"][node] = value


class StableMapping(Mapping):
    def __init__(self, data):
        self._data = dict(data)

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)


class ThrowingSnapshotMapping(StableMapping):
    def __init__(self, data, fail):
        super().__init__(data)
        self._fail = fail

    def _maybe(self, name):
        if self._fail == name:
            raise RuntimeError(f"review-{name}-failure")

    def keys(self):
        self._maybe("keys")
        return self._data.keys()

    def __iter__(self):
        self._maybe("iter")
        return iter(self._data)

    def __getitem__(self, key):
        self._maybe("getitem")
        return self._data[key]

    def __len__(self):
        self._maybe("len")
        return len(self._data)


class ConvenienceMethodsRaiseMapping(StableMapping):
    def items(self):
        raise RuntimeError("items-must-not-be-needed")

    def values(self):
        raise RuntimeError("values-must-not-be-needed")

    def get(self, key, default=None):
        raise RuntimeError("get-must-not-be-needed")

    def __contains__(self, key):
        raise RuntimeError("contains-must-not-be-needed")

    def __repr__(self):
        raise RuntimeError("repr-must-not-be-needed")

    def __str__(self):
        raise RuntimeError("str-must-not-be-needed")

    def __hash__(self):
        raise RuntimeError("hash-must-not-be-needed")

    def __eq__(self, other):
        raise RuntimeError("equality-must-not-be-needed")

    def __lt__(self, other):
        raise RuntimeError("ordering-must-not-be-needed")


class OneShotMapping(Mapping):
    def __init__(self, data):
        self._data = dict(data)
        self._keys = list(self._data.keys())
        self._reads = 0
        self._sealed = False

    def _check(self):
        if self._sealed:
            raise RuntimeError("nested-carrier-read-after-snapshot")

    def keys(self):
        self._check()
        return list(self._keys)

    def __getitem__(self, key):
        self._check()
        value = self._data[key]
        self._reads += 1
        if self._reads >= len(self._keys):
            self._sealed = True
        return value

    def __iter__(self):
        self._check()
        return iter(self._keys)

    def __len__(self):
        return len(self._keys)


class MutatesLaterNodeMapping(StableMapping):
    """Stable snapshot content whose first snapshot step changes a later consumed node."""

    def __init__(self, data, callback):
        super().__init__(data)
        self._callback = callback
        self._fired = False

    def keys(self):
        if not self._fired:
            self._fired = True
            self._callback()
        return self._data.keys()


class OBL059R8IndependentReview(unittest.TestCase):
    def setUp(self):
        self.original_limit = sys.get_int_max_str_digits()
        self.minimum_limit = sys.int_info.str_digits_check_threshold

    def tearDown(self):
        sys.set_int_max_str_digits(self.original_limit)

    def assert_no_effect(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def assert_negative(self, packet, reason=None):
        try:
            result = r8.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(f"commissioned review case raised {type(exc).__name__}: {exc}")
        self.assertEqual(result["decision"], r8.NEGATIVE_DECISION, result)
        if reason is not None:
            self.assertEqual(result["reason"], reason, result)
        json.dumps(result, sort_keys=True)
        self.assert_no_effect(result)
        return result

    def test_01_exact_dict_positive_and_negative_controls(self):
        positive = r8.evaluate_direct_positive_applicability(fixture())
        self.assertEqual(positive["decision"], r8.POSITIVE_DECISION, positive)
        self.assert_no_effect(positive)

        negative = fixture()
        negative["execution_scope"] = "PROJECT_CURRENT"
        self.assert_negative(negative, "PROJECT_CURRENT_ISSUANCE_FORBIDDEN_IN_R1")

    def test_02_stable_custom_mapping_equivalence_at_all_five_nodes(self):
        for node in NODES:
            with self.subTest(node=node):
                exact_packet = fixture()
                expected = r8.evaluate_direct_positive_applicability(copy.deepcopy(exact_packet))
                mapped_packet = fixture()
                install_node(
                    mapped_packet,
                    node,
                    StableMapping(copy.deepcopy(node_value(mapped_packet, node))),
                )
                actual = r8.evaluate_direct_positive_applicability(mapped_packet)
                self.assertEqual(actual, expected)
                self.assertEqual(actual["decision"], r8.POSITIVE_DECISION)
                self.assert_no_effect(actual)

    def test_03_snapshot_failures_at_all_five_nodes_are_field_specific(self):
        for node in NODES:
            for fail in ("keys", "iter", "getitem", "len"):
                with self.subTest(node=node, fail=fail):
                    packet = fixture()
                    install_node(
                        packet,
                        node,
                        ThrowingSnapshotMapping(
                            copy.deepcopy(node_value(packet, node)),
                            fail,
                        ),
                    )
                    self.assert_negative(packet, FAILURE_REASONS[node])

    def test_04_non_snapshot_convenience_methods_are_not_needed(self):
        for node in NODES:
            with self.subTest(node=node):
                packet = fixture()
                install_node(
                    packet,
                    node,
                    ConvenienceMethodsRaiseMapping(
                        copy.deepcopy(node_value(packet, node))
                    ),
                )
                result = r8.evaluate_direct_positive_applicability(packet)
                self.assertEqual(result["decision"], r8.POSITIVE_DECISION, result)
                self.assert_no_effect(result)

    def test_05_successful_nested_snapshots_are_one_shot(self):
        for node in NODES:
            with self.subTest(node=node):
                packet = fixture()
                install_node(
                    packet,
                    node,
                    OneShotMapping(copy.deepcopy(node_value(packet, node))),
                )
                result = r8.evaluate_direct_positive_applicability(packet)
                self.assertEqual(result["decision"], r8.POSITIVE_DECISION, result)
                self.assert_no_effect(result)

    def test_06_outer_and_nested_snapshot_composition_preserves_meaning(self):
        packet = fixture()
        packet["opportunity"] = StableMapping(packet["opportunity"])
        packet["evidence"]["actor_activation"] = StableMapping(
            packet["evidence"]["actor_activation"]
        )
        exact = fixture()
        actual = r8.evaluate_direct_positive_applicability(StableMapping(packet))
        expected = r8.evaluate_direct_positive_applicability(exact)
        self.assertEqual(actual, expected)
        self.assertEqual(actual["decision"], r8.POSITIVE_DECISION)

    def test_07_shared_one_shot_carrier_across_consumed_nodes_closes_deterministically(self):
        def make_packet():
            packet = fixture()
            actor = packet["actor_id"]
            world = packet["world_id"]
            time = packet["time_id"]
            shared_data = {
                "semantic_owner": r8.ADP007_OWNER,
                "jurisdiction": "OBL048_SUBJECT_CLASSIFICATION",
                "subject_id": r8.FIRST_CANARY_SUBJECT_ID,
                "predicate": r8.SUBJECT_CLASSIFICATION_PREDICATE,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "state": "ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            }
            shared = OneShotMapping(shared_data)
            packet["evidence"]["subject_classification"] = shared
            packet["evidence"]["actor_activation"] = shared
            return packet

        first = self.assert_negative(
            make_packet(), "ACTOR_ACTIVATION_EVIDENCE_MISSING"
        )
        second = self.assert_negative(
            make_packet(), "ACTOR_ACTIVATION_EVIDENCE_MISSING"
        )
        self.assertEqual(first, second)

    def test_08_cross_node_snapshot_mutation_cannot_turn_initial_negative_into_positive(self):
        baseline = fixture()
        baseline["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"
        baseline_result = r8.evaluate_direct_positive_applicability(
            copy.deepcopy(baseline)
        )
        self.assertEqual(
            baseline_result["reason"],
            "ACTOR_ACTIVATION_WRONG_AUTHORITY",
            baseline_result,
        )
        self.assertEqual(baseline_result["decision"], r8.NEGATIVE_DECISION)

        packet = fixture()
        packet["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"
        valid_actor = copy.deepcopy(fixture()["evidence"]["actor_activation"])
        opportunity_data = copy.deepcopy(packet["opportunity"])

        def replace_later_actor_node():
            packet["evidence"]["actor_activation"] = valid_actor

        packet["opportunity"] = MutatesLaterNodeMapping(
            opportunity_data,
            replace_later_actor_node,
        )
        result = r8.evaluate_direct_positive_applicability(packet)
        self.assertEqual(
            result["decision"],
            r8.NEGATIVE_DECISION,
            "a successful earlier nested snapshot changed a later consumed node "
            "and converted the initial negative packet into a positive result",
        )

    def test_09_oversized_integer_behavior_remains_total_across_supported_settings(self):
        value = 10 ** 5000
        for setting in (0, self.minimum_limit):
            with self.subTest(setting=setting):
                sys.set_int_max_str_digits(setting)
                packet = fixture()
                packet["actor_id"] = value
                self.assert_negative(packet, "MALFORMED_BINDING:actor_id")

    def test_10_nested_custom_mapping_with_oversized_binding_remains_negative(self):
        packet = fixture()
        actor_component = copy.deepcopy(packet["evidence"]["actor_activation"])
        actor_component["actor_id"] = 10 ** 5000
        packet["evidence"]["actor_activation"] = StableMapping(actor_component)
        self.assert_negative(packet, "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id")

    def test_11_scope_authority_stale_and_adjacent_field_controls(self):
        cases = []
        p = fixture()
        p["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong"
        cases.append(p)

        p = fixture()
        p["claimed_positive_applicability_source"] = "V554"
        cases.append(p)

        p = fixture()
        p["evidence"]["developmental_phase"]["stale"] = True
        cases.append(p)

        p = fixture()
        del p["evidence"]
        p.update(
            {
                "classification": "public clinic",
                "routing": "eligible",
                "occurrence": True,
                "causal_use_permission": True,
                "contact_witness_independence": True,
                "narrative_plausibility": "obvious",
            }
        )
        cases.append(p)

        for index, packet in enumerate(cases):
            with self.subTest(index=index):
                self.assert_negative(packet)

    def test_12_unrelated_delegate_errors_remain_visible_after_successful_snapshot(self):
        original = r8._r7.evaluate_direct_positive_applicability
        packet = fixture()
        packet["opportunity"] = StableMapping(packet["opportunity"])
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("review-deliberate-implementation-error")
                r8._r7.evaluate_direct_positive_applicability = deliberate
                with self.subTest(exc_type=exc_type.__name__):
                    with self.assertRaisesRegex(
                        exc_type, "review-deliberate-implementation-error"
                    ):
                        r8.evaluate_direct_positive_applicability(packet)
        finally:
            r8._r7.evaluate_direct_positive_applicability = original

    def test_13_revision_and_frozen_target_identity_are_exact(self):
        self.assertEqual(
            r8.R8_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R8",
        )
        self.assertEqual(CANDIDATE.name, "positive_applicability_authority_r8.py")


if __name__ == "__main__":
    unittest.main(verbosity=2)
