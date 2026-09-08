"""Fresh independent bounded review for frozen OBL059 R3.

Review-only.  This file does not repair or modify the frozen candidate.
"""
from __future__ import annotations

import importlib.util
import json
import unittest
from collections.abc import Mapping
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / "positive_applicability_authority_r3.py"

spec = importlib.util.spec_from_file_location("_obl059_r3_independent_target", CANDIDATE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load frozen R3 candidate: {CANDIDATE}")
r3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r3)


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
    actor = "urn:rawlsing:noncurrent-synthetic:v3:actor:obl059:r3-independent"
    world = "urn:rawlsing:noncurrent-synthetic:v3:world:obl059:r3-independent"
    time = "urn:rawlsing:noncurrent-synthetic:v3:time:obl059:r3-independent"
    opportunity = "urn:rawlsing:noncurrent-synthetic:v3:adp010-opportunity:obl059:r3-independent"
    return {
        "execution_scope": r3.SYNTHETIC_SCOPE,
        "actor_id": actor,
        "subject_id": r3.FIRST_CANARY_SUBJECT_ID,
        "world_id": world,
        "time_id": time,
        "adp010_opportunity_id": opportunity,
        "opportunity": {
            "actor_id": actor,
            "subject_id": r3.FIRST_CANARY_SUBJECT_ID,
            "world_id": world,
            "time_id": time,
            "opportunity_id": opportunity,
            "consumer_rule": r3.ADP010_CONSUMER,
        },
        "evidence": {
            "subject_classification": {
                "semantic_owner": "NONCURRENT_SYNTHETIC_OBL048_COMPETENT_SOURCE@R3_INDEPENDENT",
                "jurisdiction": "OBL048_SUBJECT_CLASSIFICATION",
                "subject_id": r3.FIRST_CANARY_SUBJECT_ID,
                "predicate": r3.SUBJECT_CLASSIFICATION_PREDICATE,
                "fresh_for_time_id": time,
                "stale": False,
            },
            "actor_activation": {
                "semantic_owner": r3.ADP007_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "state": "ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
            "developmental_phase": {
                "semantic_owner": r3.ADP008_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "phase": "V3DP_DEVELOPMENT_ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
        },
    }


class PoisonDisplayOpaque:
    def __repr__(self):
        raise RuntimeError("repr-must-not-run")

    def __str__(self):
        raise RuntimeError("str-must-not-run")


class HostileHashOpaque:
    def __hash__(self):
        raise RuntimeError("hash-must-not-run")


class HostileEqualityOpaque:
    def __eq__(self, other):
        raise RuntimeError("equality-must-not-run")


class HostileItemsMapping(Mapping):
    """Copyable Mapping whose diagnostic items traversal is hostile."""

    def __init__(self):
        self._data = {"placeholder": "value"}

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def items(self):
        raise TypeError("commissioned-hostile-mapping-items")


class PairMapping(Mapping):
    """Mapping that exposes opaque key/value pairs without hashing those objects."""

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __getitem__(self, key):
        if key == "placeholder":
            return self.value
        raise KeyError(key)

    def __iter__(self):
        return iter(("placeholder",))

    def __len__(self):
        return 1

    def items(self):
        return [(self.key, self.value)]


class OBL059R3IndependentReview(unittest.TestCase):
    REQUIRED = tuple(r3._REQUIRED_BINDINGS)

    def assert_no_current_effect(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def assert_negative_receipt(self, packet, reason_prefix=None):
        try:
            result = r3.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(
                "commissioned malformed input escaped negative-receipt boundary: "
                f"{type(exc).__name__}: {exc}"
            )
        self.assertEqual(result["decision"], r3.NEGATIVE_DECISION, result)
        if reason_prefix is not None:
            self.assertTrue(result["reason"].startswith(reason_prefix), result)
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64, result)
        self.assert_no_current_effect(result)
        return result

    def malformed_at(self, key, value):
        packet = fixture()
        packet[key] = value
        return packet

    def test_01_noncurrent_positive_and_negative_controls(self):
        positive = r3.evaluate_direct_positive_applicability(fixture())
        self.assertEqual(positive["decision"], r3.POSITIVE_DECISION, positive)
        self.assertEqual(positive["execution_scope"], r3.SYNTHETIC_SCOPE)
        self.assert_no_current_effect(positive)

        negative_packet = fixture()
        negative_packet["execution_scope"] = "PROJECT_CURRENT"
        negative = r3.evaluate_direct_positive_applicability(negative_packet)
        self.assertEqual(negative["decision"], r3.NEGATIVE_DECISION, negative)
        self.assert_no_current_effect(negative)

    def test_02_json_safe_r2_behavior_is_exact(self):
        cases = []
        cases.append(fixture())

        wrong_scope = fixture()
        wrong_scope["execution_scope"] = "PROJECT_CURRENT"
        cases.append(wrong_scope)

        malformed = fixture()
        malformed["actor_id"] = 7
        cases.append(malformed)

        missing = fixture()
        del missing["world_id"]
        cases.append(missing)

        extra = fixture()
        extra["uncommissioned_extra"] = {"narrative": "plausible"}
        cases.append(extra)

        for index, packet in enumerate(cases):
            with self.subTest(index=index):
                self.assertEqual(
                    r3.evaluate_direct_positive_applicability(packet),
                    r3._r2.evaluate_direct_positive_applicability(packet),
                )

    def test_03_original_non_json_shapes_every_required_binding(self):
        factories = {
            "bytes": lambda: b"not-a-valid-id",
            "set": lambda: {"not", "valid"},
            "frozenset": lambda: frozenset({"not", "valid"}),
            "opaque": object,
            "nested_opaque": lambda: {"outer": [object()]},
            "mixed": lambda: {"outer": [b"bytes", {"set", "inside"}, object()]},
        }
        for key in self.REQUIRED:
            for label, factory in factories.items():
                with self.subTest(key=key, shape=label):
                    result = self.assert_negative_receipt(
                        self.malformed_at(key, factory()),
                        f"MALFORMED_BINDING:{key}",
                    )
                    self.assertNotIsInstance(result["bindings"][key], str)

    def test_04_non_json_mapping_keys_every_required_binding(self):
        class StableOpaqueKey:
            pass

        factories = {
            "bytes_key": lambda: {b"k": "v"},
            "tuple_key": lambda: {("k", 1): {"nested": b"v"}},
            "opaque_key": lambda: {StableOpaqueKey(): [b"v"]},
            "nested_key_value": lambda: {
                "outer": [{("tuple", 2): {b"bytes-key": frozenset({"x", "y"})}}]
            },
        }
        for key in self.REQUIRED:
            for label, factory in factories.items():
                with self.subTest(key=key, shape=label):
                    self.assert_negative_receipt(
                        self.malformed_at(key, factory()),
                        f"MALFORMED_BINDING:{key}",
                    )

    def test_05_cycles_mutual_cycles_and_shared_graphs(self):
        def circular_list():
            value = []
            value.append(value)
            return value

        def circular_dict():
            value = {}
            value["self"] = value
            return value

        def mutual():
            left = []
            right = {"left": left}
            left.append(right)
            return {"left": left, "right": right}

        def deep_cycle():
            root = []
            cursor = root
            for _ in range(20):
                nxt = []
                cursor.append(nxt)
                cursor = nxt
            cursor.append(root)
            return root

        def shared_graph():
            shared = {b"shared-key": [object()]}
            return [shared, shared]

        factories = (circular_list, circular_dict, mutual, deep_cycle, shared_graph)
        for key in self.REQUIRED:
            for factory in factories:
                with self.subTest(key=key, shape=factory.__name__):
                    self.assert_negative_receipt(
                        self.malformed_at(key, factory()),
                        f"MALFORMED_BINDING:{key}",
                    )

    def test_06_deep_nesting_hits_deterministic_projection_ceiling(self):
        def make_deep():
            value = b"leaf"
            for _ in range(96):
                value = [value]
            return value

        first = self.assert_negative_receipt(
            self.malformed_at("actor_id", make_deep()),
            "MALFORMED_BINDING:actor_id",
        )
        second = self.assert_negative_receipt(
            self.malformed_at("actor_id", make_deep()),
            "MALFORMED_BINDING:actor_id",
        )
        self.assertEqual(first, second)
        self.assertIn("__projection_depth_limit__", json.dumps(first, sort_keys=True))

    def test_07_throwing_repr_and_str_are_not_invoked_or_coerced(self):
        for key in self.REQUIRED:
            with self.subTest(key=key):
                result = self.assert_negative_receipt(
                    self.malformed_at(key, PoisonDisplayOpaque()),
                    f"MALFORMED_BINDING:{key}",
                )
                projected = result["bindings"][key]
                self.assertIsInstance(projected, dict)
                self.assertIn("__non_json_type__", projected)
                self.assertNotIsInstance(projected, str)

    def test_08_hostile_hash_and_equality_are_not_needed_for_projection(self):
        values = (
            PairMapping(HostileHashOpaque(), PoisonDisplayOpaque()),
            PairMapping(HostileEqualityOpaque(), PoisonDisplayOpaque()),
        )
        for key in self.REQUIRED:
            for index, value in enumerate(values):
                with self.subTest(key=key, hostile=index):
                    self.assert_negative_receipt(
                        self.malformed_at(key, value),
                        f"MALFORMED_BINDING:{key}",
                    )

    def test_09_hostile_mapping_items_projection_exception_must_close(self):
        # The current campaign adjudication explicitly commissions throwing
        # mapping/iteration behavior reachable by diagnostic projection and
        # forbids uncaught projection exceptions once the required binding is
        # already semantically malformed.
        for key in self.REQUIRED:
            with self.subTest(key=key):
                self.assert_negative_receipt(
                    self.malformed_at(key, HostileItemsMapping()),
                    f"MALFORMED_BINDING:{key}",
                )

    def test_10_equivalent_malformed_classes_are_deterministic(self):
        makers = (
            lambda: {b"k": "v"},
            lambda: [b"not", {"valid"}],
            lambda: PoisonDisplayOpaque(),
        )
        for key in self.REQUIRED:
            for index, maker in enumerate(makers):
                with self.subTest(key=key, maker=index):
                    a = self.assert_negative_receipt(
                        self.malformed_at(key, maker()),
                        f"MALFORMED_BINDING:{key}",
                    )
                    b = self.assert_negative_receipt(
                        self.malformed_at(key, maker()),
                        f"MALFORMED_BINDING:{key}",
                    )
                    self.assertEqual(a, b)
                    self.assertEqual(a["proof_sha256"], b["proof_sha256"])

    def test_11_distinct_malformed_structures_remain_distinguishable(self):
        one = self.assert_negative_receipt(
            self.malformed_at("actor_id", [PoisonDisplayOpaque()]),
            "MALFORMED_BINDING:actor_id",
        )
        two = self.assert_negative_receipt(
            self.malformed_at("actor_id", [PoisonDisplayOpaque(), PoisonDisplayOpaque()]),
            "MALFORMED_BINDING:actor_id",
        )
        nested = self.assert_negative_receipt(
            self.malformed_at("actor_id", [[PoisonDisplayOpaque()]]),
            "MALFORMED_BINDING:actor_id",
        )
        self.assertNotEqual(one["proof_sha256"], two["proof_sha256"])
        self.assertNotEqual(one["proof_sha256"], nested["proof_sha256"])
        for result in (one, two, nested):
            self.assertNotIsInstance(result["bindings"]["actor_id"], str)

    def test_12_scope_binding_authority_and_freshness_attacks_stay_negative(self):
        attacks = []

        wrong_actor = fixture()
        wrong_actor["opportunity"]["actor_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-actor"
        attacks.append(wrong_actor)

        wrong_world = fixture()
        wrong_world["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-world"
        attacks.append(wrong_world)

        wrong_subject = fixture()
        wrong_subject["subject_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-subject"
        wrong_subject["opportunity"]["subject_id"] = wrong_subject["subject_id"]
        attacks.append(wrong_subject)

        wrong_time = fixture()
        wrong_time["opportunity"]["time_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-time"
        attacks.append(wrong_time)

        wrong_opportunity = fixture()
        wrong_opportunity["opportunity"]["opportunity_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-opportunity"
        attacks.append(wrong_opportunity)

        wrong_owner = fixture()
        wrong_owner["evidence"]["actor_activation"]["semantic_owner"] = "V554"
        attacks.append(wrong_owner)

        wrong_jurisdiction = fixture()
        wrong_jurisdiction["evidence"]["subject_classification"]["jurisdiction"] = "ROUTING"
        attacks.append(wrong_jurisdiction)

        wrong_predicate = fixture()
        wrong_predicate["evidence"]["subject_classification"]["predicate"] = "NARRATIVE_PLAUSIBILITY"
        attacks.append(wrong_predicate)

        stale = fixture()
        stale["evidence"]["developmental_phase"]["stale"] = True
        attacks.append(stale)

        mismatch = fixture()
        mismatch["evidence"]["actor_activation"]["fresh_for_time_id"] = "urn:rawlsing:noncurrent-synthetic:other-time"
        attacks.append(mismatch)

        for index, packet in enumerate(attacks):
            with self.subTest(index=index):
                result = r3.evaluate_direct_positive_applicability(packet)
                self.assertEqual(result["decision"], r3.NEGATIVE_DECISION, result)
                self.assert_no_current_effect(result)

    def test_13_alias_and_narrative_fields_cannot_substitute_for_evidence(self):
        packet = fixture()
        del packet["evidence"]
        packet.update(
            {
                "V554": True,
                "CAN-001": True,
                "CAN-003": True,
                "routing": "eligible",
                "classification": "public clinic",
                "occurrence": True,
                "causal_use_permission": True,
                "contact_witness_independence": True,
                "adp010_realized": True,
                "narrative_plausibility": "obvious",
            }
        )
        result = r3.evaluate_direct_positive_applicability(packet)
        self.assertEqual(result["decision"], r3.NEGATIVE_DECISION, result)
        self.assert_no_current_effect(result)

    def test_14_project_current_scope_is_hard_closed(self):
        packet = fixture()
        packet["execution_scope"] = "PROJECT_CURRENT"
        packet["claimed_positive_applicability_source"] = r3.AUTHORITY_ID
        result = r3.evaluate_direct_positive_applicability(packet)
        self.assertEqual(result["decision"], r3.NEGATIVE_DECISION, result)
        self.assert_no_current_effect(result)

    def test_15_unrelated_delegated_programmer_error_remains_visible(self):
        original = r3._r2.evaluate_direct_positive_applicability

        def deliberate_programmer_error(_packet):
            raise RuntimeError("independent-review-deliberate-programmer-error")

        try:
            r3._r2.evaluate_direct_positive_applicability = deliberate_programmer_error
            with self.assertRaisesRegex(
                RuntimeError, "independent-review-deliberate-programmer-error"
            ):
                r3.evaluate_direct_positive_applicability(fixture())
        finally:
            r3._r2.evaluate_direct_positive_applicability = original

    def test_16_revision_identity_is_exact(self):
        self.assertEqual(
            r3.R3_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R3",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
