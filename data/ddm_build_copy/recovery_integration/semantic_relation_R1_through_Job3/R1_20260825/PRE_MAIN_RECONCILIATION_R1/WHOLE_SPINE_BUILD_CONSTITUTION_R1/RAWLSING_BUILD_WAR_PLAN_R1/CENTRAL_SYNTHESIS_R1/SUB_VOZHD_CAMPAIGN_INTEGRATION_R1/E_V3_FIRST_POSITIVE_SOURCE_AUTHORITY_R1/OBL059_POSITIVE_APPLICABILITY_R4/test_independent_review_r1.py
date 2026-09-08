"""Fresh independent bounded review for frozen OBL059 R4.

Review-only: this file does not repair or modify the frozen candidate.
"""
from __future__ import annotations

import importlib.util
import json
import unittest
from collections.abc import Mapping
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / "positive_applicability_authority_r4.py"

spec = importlib.util.spec_from_file_location("_obl059_r4_review_target", CANDIDATE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load frozen R4 candidate: {CANDIDATE}")
r4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r4)

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
    actor = "urn:rawlsing:noncurrent-synthetic:v3:actor:obl059:r4-independent"
    world = "urn:rawlsing:noncurrent-synthetic:v3:world:obl059:r4-independent"
    time = "urn:rawlsing:noncurrent-synthetic:v3:time:obl059:r4-independent"
    opportunity = "urn:rawlsing:noncurrent-synthetic:v3:adp010-opportunity:obl059:r4-independent"
    return {
        "execution_scope": r4.SYNTHETIC_SCOPE,
        "actor_id": actor,
        "subject_id": r4.FIRST_CANARY_SUBJECT_ID,
        "world_id": world,
        "time_id": time,
        "adp010_opportunity_id": opportunity,
        "opportunity": {
            "actor_id": actor,
            "subject_id": r4.FIRST_CANARY_SUBJECT_ID,
            "world_id": world,
            "time_id": time,
            "opportunity_id": opportunity,
            "consumer_rule": r4.ADP010_CONSUMER,
        },
        "evidence": {
            "subject_classification": {
                "semantic_owner": "NONCURRENT_SYNTHETIC_OBL048_COMPETENT_SOURCE@R4_REVIEW",
                "jurisdiction": "OBL048_SUBJECT_CLASSIFICATION",
                "subject_id": r4.FIRST_CANARY_SUBJECT_ID,
                "predicate": r4.SUBJECT_CLASSIFICATION_PREDICATE,
                "fresh_for_time_id": time,
                "stale": False,
            },
            "actor_activation": {
                "semantic_owner": r4.ADP007_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "state": "ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
            "developmental_phase": {
                "semantic_owner": r4.ADP008_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "phase": "V3DP_DEVELOPMENT_ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
        },
    }


class ThrowingMapping(Mapping):
    def __getitem__(self, key):
        raise RuntimeError("getitem-must-not-run")
    def __iter__(self):
        raise RuntimeError("iter-must-not-run")
    def __len__(self):
        raise RuntimeError("len-must-not-run")
    def items(self):
        raise TypeError("items-must-not-run")
    def keys(self):
        raise ValueError("keys-must-not-run")
    def values(self):
        raise RuntimeError("values-must-not-run")
    def __contains__(self, item):
        raise RuntimeError("contains-must-not-run")
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


class ThrowingProtocolObject:
    def __iter__(self):
        raise RuntimeError("iter-must-not-run")
    def __len__(self):
        raise RuntimeError("len-must-not-run")
    def __getitem__(self, key):
        raise RuntimeError("getitem-must-not-run")
    def __bytes__(self):
        raise RuntimeError("bytes-must-not-run")
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


class StableHashThrowingElse:
    def __hash__(self):
        return 928371
    def __repr__(self):
        raise RuntimeError("repr-must-not-run")
    def __str__(self):
        raise RuntimeError("str-must-not-run")
    def __eq__(self, other):
        raise RuntimeError("eq-must-not-run")
    def __lt__(self, other):
        raise RuntimeError("order-must-not-run")
    def __iter__(self):
        raise RuntimeError("iter-must-not-run")


class CustomSequenceLike:
    def __iter__(self):
        raise RuntimeError("custom-sequence-iter")
    def __len__(self):
        raise RuntimeError("custom-sequence-len")
    def __getitem__(self, key):
        raise RuntimeError("custom-sequence-getitem")


class CustomBytesLike:
    def __bytes__(self):
        raise RuntimeError("custom-bytes-conversion")


class OBL059R4IndependentReview(unittest.TestCase):
    REQUIRED = tuple(r4._REQUIRED_BINDINGS)

    def assert_no_effect(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def malformed_at(self, key, value):
        packet = fixture()
        packet[key] = value
        return packet

    def assert_negative(self, packet, reason_prefix=None):
        try:
            result = r4.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(
                "commissioned malformed binding escaped negative-receipt construction: "
                f"{type(exc).__name__}: {exc}"
            )
        self.assertEqual(result["decision"], r4.NEGATIVE_DECISION, result)
        if reason_prefix is not None:
            self.assertTrue(result["reason"].startswith(reason_prefix), result)
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64, result)
        self.assert_no_effect(result)
        return result

    def test_01_positive_and_negative_controls(self):
        positive = r4.evaluate_direct_positive_applicability(fixture())
        self.assertEqual(positive["decision"], r4.POSITIVE_DECISION, positive)
        self.assert_no_effect(positive)
        negative = fixture()
        negative["execution_scope"] = "PROJECT_CURRENT"
        result = r4.evaluate_direct_positive_applicability(negative)
        self.assertEqual(result["decision"], r4.NEGATIVE_DECISION, result)
        self.assert_no_effect(result)

    def test_02_json_safe_r3_behavior_is_exact(self):
        cases = [fixture()]
        p = fixture(); p["execution_scope"] = "PROJECT_CURRENT"; cases.append(p)
        p = fixture(); p["actor_id"] = 7; cases.append(p)
        p = fixture(); del p["world_id"]; cases.append(p)
        for index, packet in enumerate(cases):
            with self.subTest(index=index):
                self.assertEqual(
                    r4.evaluate_direct_positive_applicability(packet),
                    r4._r3.evaluate_direct_positive_applicability(packet),
                )

    def test_03_custom_mapping_protocols_are_not_needed(self):
        for key in self.REQUIRED:
            with self.subTest(key=key):
                self.assert_negative(
                    self.malformed_at(key, ThrowingMapping()),
                    f"MALFORMED_BINDING:{key}",
                )

    def test_04_custom_sequence_and_bytes_like_protocols_are_not_needed(self):
        makers = (CustomSequenceLike, CustomBytesLike, ThrowingProtocolObject)
        for key in self.REQUIRED:
            for maker in makers:
                with self.subTest(key=key, maker=maker.__name__):
                    self.assert_negative(
                        self.malformed_at(key, maker()),
                        f"MALFORMED_BINDING:{key}",
                    )

    def test_05_builtin_containers_with_throwing_custom_values_close(self):
        makers = (
            lambda: [ThrowingProtocolObject()],
            lambda: (ThrowingProtocolObject(),),
            lambda: {"value": ThrowingProtocolObject()},
            lambda: {StableHashThrowingElse()},
            lambda: frozenset({StableHashThrowingElse()}),
        )
        for key in self.REQUIRED:
            for index, maker in enumerate(makers):
                with self.subTest(key=key, maker=index):
                    self.assert_negative(
                        self.malformed_at(key, maker()),
                        f"MALFORMED_BINDING:{key}",
                    )

    def test_06_heterogeneous_non_json_mapping_keys_close(self):
        def maker():
            return {
                "text": b"bytes-value",
                5: {"set-value"},
                ("tuple", 1): object(),
                frozenset({"frozen"}): b"x",
                StableHashThrowingElse(): object(),
            }
        for key in self.REQUIRED:
            with self.subTest(key=key):
                self.assert_negative(
                    self.malformed_at(key, maker()),
                    f"MALFORMED_BINDING:{key}",
                )

    def test_07_cycles_and_shared_references_close(self):
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
        def shared():
            node = [object()]
            return [node, node, {"node": node}]
        for key in self.REQUIRED:
            for maker in (circular_list, circular_dict, mutual, shared):
                with self.subTest(key=key, maker=maker.__name__):
                    self.assert_negative(
                        self.malformed_at(key, maker()),
                        f"MALFORMED_BINDING:{key}",
                    )

    def test_08_depth_ceiling_is_deterministic(self):
        def nested(depth):
            value = object()
            for _ in range(depth):
                value = [value]
            return value
        for depth in (63, 64, 65, 96, 300):
            with self.subTest(depth=depth):
                a = self.assert_negative(self.malformed_at("actor_id", nested(depth)), "MALFORMED_BINDING:actor_id")
                b = self.assert_negative(self.malformed_at("actor_id", nested(depth)), "MALFORMED_BINDING:actor_id")
                self.assertEqual(a, b)

    def test_09_breadth_heavy_projection_is_deterministic(self):
        def broad():
            return [object() for _ in range(2048)]
        a = self.assert_negative(self.malformed_at("world_id", broad()), "MALFORMED_BINDING:world_id")
        b = self.assert_negative(self.malformed_at("world_id", broad()), "MALFORMED_BINDING:world_id")
        self.assertEqual(a, b)

    def test_10_nested_non_json_combinations_every_required_binding(self):
        def mixed():
            return {"outer": [b"bytes", {"set", "inside"}, frozenset({"f"}), {b"key": object()}]}
        for key in self.REQUIRED:
            with self.subTest(key=key):
                self.assert_negative(self.malformed_at(key, mixed()), f"MALFORMED_BINDING:{key}")

    def test_11_equivalent_malformed_classes_are_deterministic(self):
        makers = (
            lambda: {b"k": "v"},
            lambda: [object(), b"v"],
            ThrowingProtocolObject,
        )
        for key in self.REQUIRED:
            for index, maker in enumerate(makers):
                with self.subTest(key=key, maker=index):
                    a = self.assert_negative(self.malformed_at(key, maker()), f"MALFORMED_BINDING:{key}")
                    b = self.assert_negative(self.malformed_at(key, maker()), f"MALFORMED_BINDING:{key}")
                    self.assertEqual(a, b)
                    self.assertEqual(a["proof_sha256"], b["proof_sha256"])

    def test_12_distinct_malformed_structures_remain_distinguishable(self):
        one = self.assert_negative(self.malformed_at("actor_id", [object()]), "MALFORMED_BINDING:actor_id")
        two = self.assert_negative(self.malformed_at("actor_id", [object(), object()]), "MALFORMED_BINDING:actor_id")
        nested = self.assert_negative(self.malformed_at("actor_id", [[object()]]), "MALFORMED_BINDING:actor_id")
        self.assertNotEqual(one["proof_sha256"], two["proof_sha256"])
        self.assertNotEqual(one["proof_sha256"], nested["proof_sha256"])

    def test_13_malformed_values_are_never_normalized_to_identifier_strings(self):
        values = (ThrowingMapping(), ThrowingProtocolObject(), [object()], {b"k": "v"})
        for key in self.REQUIRED:
            for index, value in enumerate(values):
                with self.subTest(key=key, value=index):
                    result = self.assert_negative(self.malformed_at(key, value), f"MALFORMED_BINDING:{key}")
                    self.assertNotIsInstance(result["bindings"][key], str)

    def test_14_scope_authority_evidence_and_project_current_stay_negative(self):
        cases = []
        p = fixture(); p["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong"; cases.append(p)
        p = fixture(); p["claimed_positive_applicability_source"] = "V554"; cases.append(p)
        p = fixture(); p["evidence"]["developmental_phase"]["stale"] = True; cases.append(p)
        p = fixture(); p["evidence"]["actor_activation"]["semantic_owner"] = "CAN-001"; cases.append(p)
        p = fixture(); p["execution_scope"] = "PROJECT_CURRENT"; cases.append(p)
        for index, packet in enumerate(cases):
            with self.subTest(index=index):
                result = r4.evaluate_direct_positive_applicability(packet)
                self.assertEqual(result["decision"], r4.NEGATIVE_DECISION, result)
                self.assert_no_effect(result)

    def test_15_narrative_and_adjacent_fields_do_not_substitute_for_evidence(self):
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
        result = r4.evaluate_direct_positive_applicability(packet)
        self.assertEqual(result["decision"], r4.NEGATIVE_DECISION, result)
        self.assert_no_effect(result)

    def test_16_unrelated_internal_errors_remain_visible(self):
        original = r4._r3.evaluate_direct_positive_applicability
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("independent-review-deliberate-internal-error")
                r4._r3.evaluate_direct_positive_applicability = deliberate
                with self.assertRaisesRegex(exc_type, "independent-review-deliberate-internal-error"):
                    r4.evaluate_direct_positive_applicability(fixture())
        finally:
            r4._r3.evaluate_direct_positive_applicability = original

    def test_17_large_exact_integer_malformed_binding_must_close(self):
        # CPython's default integer-to-string conversion ceiling is 4300 digits.
        # R4 marks exact ints structurally JSON-safe before canonical encoding.
        very_large_integer = 10 ** 5000
        for key in self.REQUIRED:
            with self.subTest(key=key):
                result = self.assert_negative(
                    self.malformed_at(key, very_large_integer),
                    f"MALFORMED_BINDING:{key}",
                )
                self.assertNotIsInstance(result["bindings"][key], str)

    def test_18_revision_identity_is_exact(self):
        self.assertEqual(r4.R4_CANDIDATE_REVISION, "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R4")


if __name__ == "__main__":
    unittest.main(verbosity=2)
