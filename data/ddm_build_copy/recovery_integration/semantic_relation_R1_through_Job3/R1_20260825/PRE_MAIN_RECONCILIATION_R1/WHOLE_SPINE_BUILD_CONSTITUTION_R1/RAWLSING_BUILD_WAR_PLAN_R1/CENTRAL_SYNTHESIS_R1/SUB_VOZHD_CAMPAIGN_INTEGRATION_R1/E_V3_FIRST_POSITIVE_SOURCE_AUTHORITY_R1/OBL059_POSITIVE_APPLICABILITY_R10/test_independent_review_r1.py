"""Fresh independent review for frozen OBL059 R10.

Review-only. This file does not modify or repair the frozen candidate.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import multiprocessing
import sys
import unittest
from collections import ChainMap
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import MappingProxyType

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / "positive_applicability_authority_r10.py"

spec = importlib.util.spec_from_file_location("_obl059_r10_independent_target", CANDIDATE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load frozen R10 candidate: {CANDIDATE}")
r10 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r10)

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

COMPONENTS = (
    "subject_classification",
    "actor_activation",
    "developmental_phase",
)

MISSING_REASONS = {
    "subject_classification": "STRUCTURAL_CLASSIFICATION_EVIDENCE_MISSING",
    "actor_activation": "ACTOR_ACTIVATION_EVIDENCE_MISSING",
    "developmental_phase": "DEVELOPMENTAL_PHASE_EVIDENCE_MISSING",
}

FAIL_REASONS = {
    "opportunity": "OPPORTUNITY_BINDING_MISSING_OR_MALFORMED",
    "evidence": "EVIDENCE_MISSING_OR_MALFORMED",
    "subject_classification": "STRUCTURAL_CLASSIFICATION_EVIDENCE_MISSING",
    "actor_activation": "ACTOR_ACTIVATION_EVIDENCE_MISSING",
    "developmental_phase": "DEVELOPMENTAL_PHASE_EVIDENCE_MISSING",
}


def fixture():
    actor = "urn:rawlsing:noncurrent-synthetic:v3:actor:obl059:r10-independent"
    world = "urn:rawlsing:noncurrent-synthetic:v3:world:obl059:r10-independent"
    time = "urn:rawlsing:noncurrent-synthetic:v3:time:obl059:r10-independent"
    opportunity = "urn:rawlsing:noncurrent-synthetic:v3:adp010-opportunity:obl059:r10-independent"
    return {
        "execution_scope": r10.SYNTHETIC_SCOPE,
        "actor_id": actor,
        "subject_id": r10.FIRST_CANARY_SUBJECT_ID,
        "world_id": world,
        "time_id": time,
        "adp010_opportunity_id": opportunity,
        "opportunity": {
            "actor_id": actor,
            "subject_id": r10.FIRST_CANARY_SUBJECT_ID,
            "world_id": world,
            "time_id": time,
            "opportunity_id": opportunity,
            "consumer_rule": r10.ADP010_CONSUMER,
        },
        "evidence": {
            "subject_classification": {
                "semantic_owner": "NONCURRENT_SYNTHETIC_OBL048_COMPETENT_SOURCE@R10_REVIEW",
                "jurisdiction": "OBL048_SUBJECT_CLASSIFICATION",
                "subject_id": r10.FIRST_CANARY_SUBJECT_ID,
                "predicate": r10.SUBJECT_CLASSIFICATION_PREDICATE,
                "fresh_for_time_id": time,
                "stale": False,
            },
            "actor_activation": {
                "semantic_owner": r10.ADP007_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "state": "ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
            "developmental_phase": {
                "semantic_owner": r10.ADP008_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "phase": "V3DP_DEVELOPMENT_ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
        },
    }


class StableCarrier(Mapping):
    def __init__(self, data):
        self._data = dict(data)

    def keys(self):
        return list(self._data.keys())

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def replace(self, key, value):
        self._data[key] = value

    def remove(self, key):
        self._data.pop(key, None)


class SideEffectCarrier(StableCarrier):
    def __init__(self, data, callback):
        super().__init__(data)
        self._callback = callback
        self._fired = False

    def keys(self):
        if not self._fired:
            self._fired = True
            self._callback()
        return super().keys()


class FailKeysCarrier(StableCarrier):
    def keys(self):
        raise RuntimeError("r10-independent-keys-failure")


class FailGetitemCarrier(StableCarrier):
    def __getitem__(self, key):
        raise RuntimeError("r10-independent-getitem-failure")


class SharedCountCarrier(StableCarrier):
    def __init__(self, data, counter):
        super().__init__(data)
        self._counter = counter

    def keys(self):
        with self._counter.get_lock():
            self._counter.value += 1
        return super().keys()


class AmbiguousBackingCarrier(Mapping):
    """Stable Mapping whose composed view has two equally plausible backing dicts."""

    def __init__(self, data):
        items = list(dict(data).items())
        cut = max(1, len(items) // 2)
        self._left = dict(items[:cut])
        self._right = dict(items[cut:])

    def _combined(self):
        merged = dict(self._left)
        merged.update(self._right)
        return merged

    def keys(self):
        return list(self._combined().keys())

    def __getitem__(self, key):
        if key in self._right:
            return self._right[key]
        return self._left[key]

    def __iter__(self):
        return iter(self._combined())

    def __len__(self):
        return len(self._combined())


def evidence_backing(packet):
    evidence = packet["evidence"]
    if isinstance(evidence, StableCarrier):
        return evidence._data
    return evidence


def get_node(packet, node):
    if node == "opportunity":
        return packet["opportunity"]
    if node == "evidence":
        return packet["evidence"]
    evidence = evidence_backing(packet)
    return evidence[node]


def install_node(packet, node, value):
    if node == "opportunity":
        packet["opportunity"] = value
        return
    if node == "evidence":
        packet["evidence"] = value
        return
    evidence = evidence_backing(packet)
    evidence[node] = value


def source_entry_data(packet, node):
    value = get_node(packet, node)
    if isinstance(value, StableCarrier):
        return dict(value._data)
    if node == "evidence" and type(value) is dict:
        return dict.copy(value)
    return copy.deepcopy(value)


def install_invalid_target(packet, target, source):
    if target == "opportunity":
        data = copy.deepcopy(fixture()["opportunity"])
        data["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-world"
        carrier = StableCarrier(data)
        install_node(packet, target, carrier)

        def restore():
            carrier.replace("world_id", packet["world_id"])

        return restore, "OPPORTUNITY_SCOPE_MISMATCH:world_id"

    if target == "evidence":
        data = copy.deepcopy(fixture()["evidence"])
        missing = next(key for key in COMPONENTS if key != source)
        saved = data.pop(missing)
        carrier = StableCarrier(data)
        install_node(packet, target, carrier)

        def restore():
            carrier._data[missing] = saved

        return restore, MISSING_REASONS[missing]

    if target == "subject_classification":
        data = copy.deepcopy(fixture()["evidence"]["subject_classification"])
        data["predicate"] = "WRONG_PREDICATE"
        carrier = StableCarrier(data)
        install_node(packet, target, carrier)

        def restore():
            carrier.replace("predicate", r10.SUBJECT_CLASSIFICATION_PREDICATE)

        return restore, "SUBJECT_CLASSIFICATION_PREDICATE_MISMATCH"

    if target == "actor_activation":
        data = copy.deepcopy(fixture()["evidence"]["actor_activation"])
        data["semantic_owner"] = "WRONG_AUTHORITY"
        carrier = StableCarrier(data)
        install_node(packet, target, carrier)

        def restore():
            carrier.replace("semantic_owner", r10.ADP007_OWNER)

        return restore, "ACTOR_ACTIVATION_WRONG_AUTHORITY"

    data = copy.deepcopy(fixture()["evidence"]["developmental_phase"])
    data["phase"] = "V3DP_OTHER"
    carrier = StableCarrier(data)
    install_node(packet, target, carrier)

    def restore():
        carrier.replace("phase", "V3DP_DEVELOPMENT_ACTIVE")

    return restore, "DEVELOPMENTAL_PHASE_NOT_ACTIVE"


def install_valid_target(packet, target, source):
    if target == "opportunity":
        carrier = StableCarrier(copy.deepcopy(fixture()["opportunity"]))
        install_node(packet, target, carrier)

        def invalidate():
            carrier.replace("world_id", "urn:rawlsing:noncurrent-synthetic:late-wrong")

        return invalidate

    if target == "evidence":
        carrier = StableCarrier(copy.deepcopy(fixture()["evidence"]))
        install_node(packet, target, carrier)
        break_key = next(key for key in COMPONENTS if key != source)

        def invalidate():
            carrier.remove(break_key)

        return invalidate

    if target == "subject_classification":
        carrier = StableCarrier(copy.deepcopy(fixture()["evidence"]["subject_classification"]))
        install_node(packet, target, carrier)

        def invalidate():
            carrier.replace("predicate", "LATE_WRONG_PREDICATE")

        return invalidate

    if target == "actor_activation":
        carrier = StableCarrier(copy.deepcopy(fixture()["evidence"]["actor_activation"]))
        install_node(packet, target, carrier)

        def invalidate():
            carrier.replace("semantic_owner", "LATE_WRONG_AUTHORITY")

        return invalidate

    carrier = StableCarrier(copy.deepcopy(fixture()["evidence"]["developmental_phase"]))
    install_node(packet, target, carrier)

    def invalidate():
        carrier.replace("phase", "V3DP_LATE_OTHER")

    return invalidate


def install_source(packet, source, callback):
    data = source_entry_data(packet, source)
    carrier = SideEffectCarrier(data, callback)
    install_node(packet, source, carrier)
    return carrier


class OBL059R10IndependentReview(unittest.TestCase):
    def assert_no_effect(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def assert_json_receipt(self, result):
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64)
        self.assert_no_effect(result)
        return result

    def assert_negative(self, packet, reason=None):
        try:
            result = r10.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(
                "commissioned negative case raised instead of returning a receipt: "
                f"{type(exc).__name__}: {exc}"
            )
        self.assertEqual(result["decision"], r10.NEGATIVE_DECISION, result)
        if reason is not None:
            self.assertEqual(result["reason"], reason, result)
        return self.assert_json_receipt(result)

    def test_01_revision_and_exact_dict_controls(self):
        self.assertEqual(
            r10.R10_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R10",
        )
        positive = r10.evaluate_direct_positive_applicability(fixture())
        self.assertEqual(positive["decision"], r10.POSITIVE_DECISION, positive)
        self.assert_json_receipt(positive)

        negative = fixture()
        negative["execution_scope"] = "PROJECT_CURRENT"
        self.assert_negative(negative, "PROJECT_CURRENT_ISSUANCE_FORBIDDEN_IN_R1")

    def test_02_all_pairwise_negative_to_positive_internal_mutations_use_entry_view(self):
        for source in NODES:
            for target in NODES:
                if source == target:
                    continue
                with self.subTest(source=source, target=target):
                    packet = fixture()
                    restore, reason = install_invalid_target(packet, target, source)
                    install_source(packet, source, restore)
                    self.assert_negative(packet, reason)

    def test_03_all_pairwise_positive_to_negative_child_local_mutations_do_not_rewrite_entry_view(self):
        for source in NODES:
            for target in NODES:
                if source == target:
                    continue
                with self.subTest(source=source, target=target):
                    packet = fixture()
                    invalidate = install_valid_target(packet, target, source)
                    install_source(packet, source, invalidate)
                    result = r10.evaluate_direct_positive_applicability(packet)
                    self.assertEqual(result["decision"], r10.POSITIVE_DECISION, result)
                    self.assert_json_receipt(result)

    def test_04_parent_and_component_slot_replacement_uses_entry_view(self):
        cases = []

        packet = fixture()
        packet["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-parent"

        def replace_opportunity():
            packet["opportunity"] = copy.deepcopy(fixture()["opportunity"])

        packet["evidence"] = SideEffectCarrier(dict.copy(packet["evidence"]), replace_opportunity)
        cases.append((packet, "OPPORTUNITY_SCOPE_MISMATCH:world_id"))

        packet = fixture()
        packet["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"

        def replace_actor():
            packet["evidence"]["actor_activation"] = copy.deepcopy(
                fixture()["evidence"]["actor_activation"]
            )

        packet["opportunity"] = SideEffectCarrier(
            copy.deepcopy(packet["opportunity"]), replace_actor
        )
        cases.append((packet, "ACTOR_ACTIVATION_WRONG_AUTHORITY"))

        for index, (packet, reason) in enumerate(cases):
            with self.subTest(index=index):
                self.assert_negative(packet, reason)

    def test_05_outer_plus_nested_custom_mapping_composition_preserves_entry_semantics(self):
        packet = fixture()
        actor_data = copy.deepcopy(packet["evidence"]["actor_activation"])
        actor_data["semantic_owner"] = "WRONG_AUTHORITY"
        actor = StableCarrier(actor_data)
        packet["evidence"]["actor_activation"] = actor

        opportunity_data = copy.deepcopy(packet["opportunity"])

        def make_actor_valid_child_local():
            actor.replace("semantic_owner", r10.ADP007_OWNER)

        packet["opportunity"] = SideEffectCarrier(
            opportunity_data, make_actor_valid_child_local
        )
        outer = StableCarrier(packet)
        self.assert_negative(outer, "ACTOR_ACTIVATION_WRONG_AUTHORITY")

    def test_06_shared_alias_is_validated_once_and_nested_aliases_do_not_rewrite_entry_view(self):
        counter = multiprocessing.Value("i", 0)
        packet = fixture()
        shared = SharedCountCarrier(
            copy.deepcopy(packet["evidence"]["actor_activation"]), counter
        )
        packet["evidence"]["actor_activation"] = shared
        packet["evidence"]["developmental_phase"] = shared
        packet["opportunity"]["shared_alias"] = shared
        self.assert_negative(packet)
        self.assertEqual(counter.value, 1)

    def test_07_standard_stable_composed_mappings_preserve_exact_dict_positive_semantics(self):
        baseline = r10.evaluate_direct_positive_applicability(fixture())
        self.assertEqual(baseline["decision"], r10.POSITIVE_DECISION)

        for node in NODES:
            with self.subTest(node=node):
                packet = fixture()
                data = copy.deepcopy(get_node(packet, node))
                install_node(packet, node, ChainMap(data, {}))
                result = r10.evaluate_direct_positive_applicability(packet)
                self.assertEqual(
                    result,
                    baseline,
                    f"stable ChainMap at {node} did not preserve exact-dict meaning",
                )

    def test_08_mapping_proxy_stable_positive_controls(self):
        baseline = r10.evaluate_direct_positive_applicability(fixture())
        for node in NODES:
            with self.subTest(node=node):
                packet = fixture()
                data = copy.deepcopy(get_node(packet, node))
                install_node(packet, node, MappingProxyType(data))
                result = r10.evaluate_direct_positive_applicability(packet)
                self.assertEqual(result, baseline)

    def test_09_ambiguous_backing_view_fails_closed_deterministically(self):
        for node in NODES:
            with self.subTest(node=node):
                first_packet = fixture()
                first_data = copy.deepcopy(get_node(first_packet, node))
                install_node(first_packet, node, AmbiguousBackingCarrier(first_data))
                first = self.assert_negative(first_packet, FAIL_REASONS[node])

                second_packet = fixture()
                second_data = copy.deepcopy(get_node(second_packet, node))
                install_node(second_packet, node, AmbiguousBackingCarrier(second_data))
                second = self.assert_negative(second_packet, FAIL_REASONS[node])
                self.assertEqual(first, second)

    def test_10_invoked_mapping_failures_are_field_specific_and_deterministic(self):
        for node in NODES:
            for maker in (FailKeysCarrier, FailGetitemCarrier):
                with self.subTest(node=node, maker=maker.__name__):
                    packet = fixture()
                    data = copy.deepcopy(get_node(packet, node))
                    install_node(packet, node, maker(data))
                    first = self.assert_negative(packet, FAIL_REASONS[node])

                    packet2 = fixture()
                    data2 = copy.deepcopy(get_node(packet2, node))
                    install_node(packet2, node, maker(data2))
                    second = self.assert_negative(packet2, FAIL_REASONS[node])
                    self.assertEqual(first, second)

    def test_11_cycle_in_consumed_custom_backing_remains_total_on_negative_path(self):
        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        cycle = []
        cycle.append(cycle)
        actor["actor_id"] = cycle
        packet["evidence"]["actor_activation"] = StableCarrier(actor)
        result = self.assert_negative(
            packet, "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id"
        )
        json.dumps(result, sort_keys=True)

    def test_12_oversized_integer_and_runtime_setting_preservation(self):
        original_limit = sys.get_int_max_str_digits()
        minimum = int(sys.int_info.str_digits_check_threshold)
        huge = 10 ** 5000
        try:
            for limit in (0, minimum):
                sys.set_int_max_str_digits(limit)
                for key in tuple(r10._REQUIRED_BINDINGS):
                    with self.subTest(limit=limit, key=key):
                        packet = fixture()
                        packet[key] = huge
                        self.assert_negative(packet)

                packet = fixture()
                actor = copy.deepcopy(packet["evidence"]["actor_activation"])
                actor["actor_id"] = huge
                packet["evidence"]["actor_activation"] = StableCarrier(actor)
                self.assert_negative(
                    packet, "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id"
                )
        finally:
            sys.set_int_max_str_digits(original_limit)

    def test_13_proof_determinism_and_distinction_for_oversized_nested_values(self):
        huge = 10 ** 5000

        def make(value):
            packet = fixture()
            actor = copy.deepcopy(packet["evidence"]["actor_activation"])
            actor["actor_id"] = value
            packet["evidence"]["actor_activation"] = StableCarrier(actor)
            return packet

        first = self.assert_negative(
            make(huge), "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id"
        )
        again = self.assert_negative(
            make(huge), "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id"
        )
        other = self.assert_negative(
            make(huge + 1), "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id"
        )
        self.assertEqual(first, again)
        self.assertNotEqual(first["proof_sha256"], other["proof_sha256"])

    def test_14_scope_authority_stale_and_adjacent_fields_stay_negative(self):
        cases = []
        packet = fixture()
        packet["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong"
        cases.append(packet)

        packet = fixture()
        packet["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"
        cases.append(packet)

        packet = fixture()
        packet["evidence"]["developmental_phase"]["stale"] = True
        cases.append(packet)

        packet = fixture()
        packet.update({
            "classification": "public clinic",
            "routing": "eligible",
            "occurrence": True,
            "narrative_plausibility": "obvious",
        })
        del packet["evidence"]
        cases.append(packet)

        for index, packet in enumerate(cases):
            with self.subTest(index=index):
                self.assert_negative(packet)

    def test_15_unrelated_post_preparation_errors_remain_visible(self):
        original = r10._r9._evaluate_prepared

        def deliberate(_packet):
            raise RuntimeError("r10-independent-deliberate-post-preparation-error")

        try:
            r10._r9._evaluate_prepared = deliberate
            with self.assertRaisesRegex(
                RuntimeError, "r10-independent-deliberate-post-preparation-error"
            ):
                r10.evaluate_direct_positive_applicability(fixture())
        finally:
            r10._r9._evaluate_prepared = original

    def test_16_repeated_and_concurrent_exact_dict_evaluations_are_deterministic(self):
        expected = r10.evaluate_direct_positive_applicability(fixture())
        for _ in range(20):
            self.assertEqual(r10.evaluate_direct_positive_applicability(fixture()), expected)

        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(
                pool.map(
                    lambda _index: r10.evaluate_direct_positive_applicability(fixture()),
                    range(32),
                )
            )
        self.assertTrue(all(result == expected for result in results))


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        OBL059R10IndependentReview
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({
        "court": "OBL059_R10_FRESH_DISTINCT_INDEPENDENT_REVIEW_R1",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "successful": result.wasSuccessful(),
        "project_current_state_created": False,
        "repair_performed_by_reviewer": False,
        "second_review_commissioned": False,
    }, sort_keys=True))
    raise SystemExit(0 if result.wasSuccessful() else 1)
