"""Fresh independent bounded review for frozen OBL059 R7.

Review-only. This file does not repair or modify the frozen candidate.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import threading
import unittest
from collections.abc import Mapping
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / "positive_applicability_authority_r7.py"

spec = importlib.util.spec_from_file_location("_obl059_r7_review_target", CANDIDATE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load frozen R7 candidate: {CANDIDATE}")
r7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r7)

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
    actor = "urn:rawlsing:noncurrent-synthetic:v3:actor:obl059:r7-review"
    world = "urn:rawlsing:noncurrent-synthetic:v3:world:obl059:r7-review"
    time = "urn:rawlsing:noncurrent-synthetic:v3:time:obl059:r7-review"
    opportunity = "urn:rawlsing:noncurrent-synthetic:v3:adp010-opportunity:obl059:r7-review"
    return {
        "execution_scope": r7.SYNTHETIC_SCOPE,
        "actor_id": actor,
        "subject_id": r7.FIRST_CANARY_SUBJECT_ID,
        "world_id": world,
        "time_id": time,
        "adp010_opportunity_id": opportunity,
        "opportunity": {
            "actor_id": actor,
            "subject_id": r7.FIRST_CANARY_SUBJECT_ID,
            "world_id": world,
            "time_id": time,
            "opportunity_id": opportunity,
            "consumer_rule": r7.ADP010_CONSUMER,
        },
        "evidence": {
            "subject_classification": {
                "semantic_owner": "NONCURRENT_SYNTHETIC_OBL048_COMPETENT_SOURCE@R7_REVIEW",
                "jurisdiction": "OBL048_SUBJECT_CLASSIFICATION",
                "subject_id": r7.FIRST_CANARY_SUBJECT_ID,
                "predicate": r7.SUBJECT_CLASSIFICATION_PREDICATE,
                "fresh_for_time_id": time,
                "stale": False,
            },
            "actor_activation": {
                "semantic_owner": r7.ADP007_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "state": "ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
            "developmental_phase": {
                "semantic_owner": r7.ADP008_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "phase": "V3DP_DEVELOPMENT_ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
        },
    }


class StableMapping(Mapping):
    def __init__(self, data):
        self._data = data
    def __getitem__(self, key):
        return self._data[key]
    def __iter__(self):
        return iter(self._data)
    def __len__(self):
        return len(self._data)


class ThrowKeysMapping(StableMapping):
    def keys(self):
        raise RuntimeError("review-keys-failure")


class ThrowIterMapping(StableMapping):
    def __iter__(self):
        raise RuntimeError("review-iter-failure")


class ThrowGetitemMapping(StableMapping):
    def keys(self):
        return list(self._data.keys())
    def __getitem__(self, key):
        raise RuntimeError("review-getitem-failure")


class UnusedMethodsRaiseMapping(StableMapping):
    def items(self):
        raise RuntimeError("items-must-not-be-needed")
    def values(self):
        raise RuntimeError("values-must-not-be-needed")
    def get(self, key, default=None):
        raise RuntimeError("get-must-not-be-needed")
    def __contains__(self, key):
        raise RuntimeError("contains-must-not-be-needed")


class OneShotMapping(Mapping):
    def __init__(self, data):
        self._data = data
        self._keys = list(data.keys())
        self._reads = 0
        self._sealed = False
    def keys(self):
        if self._sealed:
            raise RuntimeError("carrier-read-after-snapshot")
        return list(self._keys)
    def __getitem__(self, key):
        if self._sealed:
            raise RuntimeError("carrier-read-after-snapshot")
        value = self._data[key]
        self._reads += 1
        if self._reads == len(self._keys):
            self._sealed = True
        return value
    def __iter__(self):
        if self._sealed:
            raise RuntimeError("carrier-read-after-snapshot")
        return iter(self._keys)
    def __len__(self):
        return len(self._keys)


class RemovingMapping(StableMapping):
    def __init__(self, data):
        super().__init__(dict(data))
        self._keys = list(self._data.keys())
        self._first = True
    def keys(self):
        return list(self._keys)
    def __getitem__(self, key):
        if self._first:
            self._first = False
            victim = self._keys[-1]
            if victim != key:
                self._data.pop(victim, None)
        return self._data[key]


class MappingLookalike:
    def keys(self):
        raise RuntimeError("lookalike-keys-must-not-run")
    def __getitem__(self, key):
        raise RuntimeError("lookalike-getitem-must-not-run")
    def __iter__(self):
        raise RuntimeError("lookalike-iter-must-not-run")
    def __len__(self):
        raise RuntimeError("lookalike-len-must-not-run")


class ThrowingNestedMapping(Mapping):
    def __getitem__(self, key):
        raise RuntimeError("nested-field-access-failure")
    def __iter__(self):
        return iter(("placeholder",))
    def __len__(self):
        return 1
    def get(self, key, default=None):
        raise RuntimeError("nested-get-failure")


class OBL059R7IndependentReview(unittest.TestCase):
    def setUp(self):
        self.original_limit = sys.get_int_max_str_digits()
        self.minimum_limit = sys.int_info.str_digits_check_threshold

    def tearDown(self):
        sys.set_int_max_str_digits(self.original_limit)

    def assert_no_effect(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def assert_negative(self, packet, reason_prefix=None):
        try:
            result = r7.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(f"commissioned malformed packet raised {type(exc).__name__}: {exc}")
        self.assertEqual(result["decision"], r7.NEGATIVE_DECISION, result)
        if reason_prefix is not None:
            self.assertTrue(result["reason"].startswith(reason_prefix), result)
        json.dumps(result, sort_keys=True)
        self.assert_no_effect(result)
        return result

    def test_01_stable_mapping_positive_matches_exact_dict(self):
        packet = fixture()
        mapped = r7.evaluate_direct_positive_applicability(StableMapping(packet))
        exact = r7.evaluate_direct_positive_applicability(packet)
        self.assertEqual(mapped, exact)
        self.assertEqual(mapped["decision"], r7.POSITIVE_DECISION)
        self.assert_no_effect(mapped)

    def test_02_stable_mapping_project_current_is_negative(self):
        packet = fixture()
        packet["execution_scope"] = "PROJECT_CURRENT"
        self.assert_negative(StableMapping(packet), "PROJECT_CURRENT_ISSUANCE_FORBIDDEN")

    def test_03_outer_snapshot_failures_return_packet_malformed(self):
        makers = (ThrowKeysMapping, ThrowIterMapping, ThrowGetitemMapping)
        for maker in makers:
            with self.subTest(maker=maker.__name__):
                result = self.assert_negative(maker(fixture()), "PACKET_MALFORMED")
                self.assertIsNone(result["bindings"]["actor_id"])

    def test_04_unused_mapping_convenience_methods_are_not_required(self):
        result = r7.evaluate_direct_positive_applicability(UnusedMethodsRaiseMapping(fixture()))
        self.assertEqual(result["decision"], r7.POSITIVE_DECISION, result)
        self.assert_no_effect(result)

    def test_05_successful_snapshot_is_single_use(self):
        result = r7.evaluate_direct_positive_applicability(OneShotMapping(fixture()))
        self.assertEqual(result["decision"], r7.POSITIVE_DECISION, result)
        self.assert_no_effect(result)

    def test_06_mutating_mapping_that_breaks_snapshot_closes(self):
        self.assert_negative(RemovingMapping(fixture()), "PACKET_MALFORMED")

    def test_07_mapping_lookalike_does_not_gain_carrier_status(self):
        self.assert_negative(MappingLookalike(), "PACKET_MALFORMED")

    def test_08_stable_outer_mapping_preserves_oversized_integer_closure(self):
        packet = fixture()
        packet["actor_id"] = 10 ** 5000
        self.assert_negative(StableMapping(packet), "MALFORMED_BINDING:actor_id")

    def test_09_nested_opportunity_mapping_failure_must_close(self):
        packet = fixture()
        packet["opportunity"] = ThrowingNestedMapping()
        self.assert_negative(packet)

    def test_10_nested_evidence_mapping_failure_must_close(self):
        packet = fixture()
        packet["evidence"] = ThrowingNestedMapping()
        self.assert_negative(packet)

    def test_11_nested_actor_evidence_mapping_failure_must_close(self):
        packet = fixture()
        packet["evidence"]["actor_activation"] = ThrowingNestedMapping()
        self.assert_negative(packet)

    def test_12_inflight_integer_setting_change_remains_total(self):
        packet = fixture()
        packet["actor_id"] = 10 ** 5000
        original_requires = r7._r6._requires_total_projection_stable
        entered = threading.Event()
        release = threading.Event()
        state = {}

        def gated(candidate_packet, reason):
            decision = original_requires(candidate_packet, reason)
            entered.set()
            if not release.wait(timeout=10):
                raise RuntimeError("review barrier timeout")
            return decision

        def run():
            try:
                state["result"] = r7.evaluate_direct_positive_applicability(packet)
            except Exception as exc:
                state["exception"] = exc

        try:
            sys.set_int_max_str_digits(0)
            r7._r6._requires_total_projection_stable = gated
            worker = threading.Thread(target=run, daemon=True)
            worker.start()
            self.assertTrue(entered.wait(timeout=10))
            sys.set_int_max_str_digits(self.minimum_limit)
            release.set()
            worker.join(timeout=10)
            self.assertFalse(worker.is_alive())
            self.assertNotIn("exception", state)
            self.assertEqual(state["result"]["decision"], r7.NEGATIVE_DECISION)
        finally:
            release.set()
            r7._r6._requires_total_projection_stable = original_requires

    def test_13_unrelated_error_after_successful_snapshot_remains_visible(self):
        original = r7._r6.evaluate_direct_positive_applicability
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("review-deliberate-implementation-error")
                r7._r6.evaluate_direct_positive_applicability = deliberate
                with self.subTest(exc_type=exc_type.__name__):
                    with self.assertRaisesRegex(exc_type, "review-deliberate-implementation-error"):
                        r7.evaluate_direct_positive_applicability(StableMapping(fixture()))
        finally:
            r7._r6.evaluate_direct_positive_applicability = original

    def test_14_adjacent_fields_cannot_substitute_for_evidence(self):
        packet = fixture()
        del packet["evidence"]
        packet.update({
            "classification": "public clinic",
            "routing": "eligible",
            "occurrence": True,
            "causal_use_permission": True,
            "contact_witness_independence": True,
            "narrative_plausibility": "obvious",
        })
        self.assert_negative(StableMapping(packet))

    def test_15_wrong_scope_authority_stale_and_current_controls(self):
        cases = []
        p = fixture(); p["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong"; cases.append(p)
        p = fixture(); p["claimed_positive_applicability_source"] = "V554"; cases.append(p)
        p = fixture(); p["evidence"]["developmental_phase"]["stale"] = True; cases.append(p)
        p = fixture(); p["execution_scope"] = "PROJECT_CURRENT"; cases.append(p)
        for index, packet in enumerate(cases):
            with self.subTest(index=index):
                self.assert_negative(StableMapping(packet))

    def test_16_equivalent_snapshot_results_are_deterministic(self):
        a = r7.evaluate_direct_positive_applicability(StableMapping(fixture()))
        b = r7.evaluate_direct_positive_applicability(StableMapping(fixture()))
        self.assertEqual(a, b)
        fa = self.assert_negative(ThrowKeysMapping(fixture()), "PACKET_MALFORMED")
        fb = self.assert_negative(ThrowKeysMapping(fixture()), "PACKET_MALFORMED")
        self.assertEqual(fa, fb)

    def test_17_revision_identity_is_exact(self):
        self.assertEqual(
            r7.R7_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R7",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
