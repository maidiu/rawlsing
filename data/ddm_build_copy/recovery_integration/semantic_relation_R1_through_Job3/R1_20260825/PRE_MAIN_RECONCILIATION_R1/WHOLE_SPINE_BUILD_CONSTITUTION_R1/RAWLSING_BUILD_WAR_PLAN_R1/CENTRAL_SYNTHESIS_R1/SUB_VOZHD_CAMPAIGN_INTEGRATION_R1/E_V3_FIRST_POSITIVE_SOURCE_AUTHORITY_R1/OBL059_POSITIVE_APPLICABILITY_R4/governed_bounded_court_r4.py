"""Governed bounded court for OBL059 R4 malformed-diagnostic projection repair."""

from __future__ import annotations

import importlib.util
import json
import unittest
from collections.abc import Mapping
from pathlib import Path

HERE = Path(__file__).resolve().parent
R3_DIR = HERE.parent / "OBL059_POSITIVE_APPLICABILITY_R3"
R4_AUTHORITY = HERE / "positive_applicability_authority_r4.py"

r4_spec = importlib.util.spec_from_file_location("_obl059_r4_authority", R4_AUTHORITY)
if r4_spec is None or r4_spec.loader is None:
    raise RuntimeError(f"cannot load R4 authority: {R4_AUTHORITY}")
r4 = importlib.util.module_from_spec(r4_spec)
r4_spec.loader.exec_module(r4)

r3_court_path = R3_DIR / "governed_bounded_court_r3.py"
r3_spec = importlib.util.spec_from_file_location("_obl059_r3_court", r3_court_path)
if r3_spec is None or r3_spec.loader is None:
    raise RuntimeError(f"cannot load R3 court: {r3_court_path}")
r3_court = importlib.util.module_from_spec(r3_spec)
r3_spec.loader.exec_module(r3_court)

r3_court.r3.evaluate_direct_positive_applicability = r4.evaluate_direct_positive_applicability
r3_court.r2_court.r2.evaluate_direct_positive_applicability = r4.evaluate_direct_positive_applicability
r3_court.r2_court.r1_court.evaluate_direct_positive_applicability = r4.evaluate_direct_positive_applicability

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
    return r3_court.fixture()


class ThrowingItemsMapping(Mapping):
    def __getitem__(self, key):
        raise AssertionError("__getitem__ must not run")

    def __iter__(self):
        return iter(("placeholder",))

    def __len__(self):
        return 1

    def items(self):
        raise TypeError("throwing-items-must-not-escape")


class NoTouchMapping(Mapping):
    def __getitem__(self, key):
        raise AssertionError("__getitem__ must not run")

    def __iter__(self):
        raise AssertionError("__iter__ must not run")

    def __len__(self):
        raise AssertionError("__len__ must not run")

    def items(self):
        raise AssertionError("items must not run")

    def keys(self):
        raise AssertionError("keys must not run")

    def values(self):
        raise AssertionError("values must not run")

    def __repr__(self):
        raise AssertionError("__repr__ must not run")

    def __str__(self):
        raise AssertionError("__str__ must not run")

    def __hash__(self):
        raise AssertionError("__hash__ must not run")

    def __eq__(self, other):
        raise AssertionError("__eq__ must not run")

    def __lt__(self, other):
        raise AssertionError("__lt__ must not run")


class PoisonOpaque:
    def __repr__(self):
        raise AssertionError("__repr__ must not run")

    def __str__(self):
        raise AssertionError("__str__ must not run")

    def __eq__(self, other):
        raise AssertionError("__eq__ must not run")

    def __lt__(self, other):
        raise AssertionError("__lt__ must not run")


class ArmedKey:
    def __init__(self):
        self.armed = False

    def __hash__(self):
        if self.armed:
            raise AssertionError("__hash__ must not run after insertion")
        return 17

    def __eq__(self, other):
        if self.armed:
            raise AssertionError("__eq__ must not run after insertion")
        return self is other

    def __repr__(self):
        raise AssertionError("__repr__ must not run")

    def __str__(self):
        raise AssertionError("__str__ must not run")


class CourtR4(r3_court.CourtR3):
    REQUIRED = tuple(r4._REQUIRED_BINDINGS)

    def assert_negative_receipt(self, packet, key):
        result = r4.evaluate_direct_positive_applicability(packet)
        self.assertEqual(result["decision"], r4.NEGATIVE_DECISION, result)
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

    def test_45_throwing_items_mapping_closes_at_every_required_binding(self):
        for key in self.REQUIRED:
            with self.subTest(key=key):
                self.assert_negative_receipt(self.malformed_at(key, ThrowingItemsMapping()), key)

    def test_46_custom_mapping_protocol_methods_are_never_needed(self):
        for key in self.REQUIRED:
            with self.subTest(key=key):
                result = self.assert_negative_receipt(self.malformed_at(key, NoTouchMapping()), key)
                self.assertEqual(result["bindings"][key], {"__non_json_type__": "custom_object"})

    def test_47_hostile_builtin_mapping_keys_and_values_close_without_callbacks(self):
        for key in self.REQUIRED:
            with self.subTest(key=key):
                hostile_key = ArmedKey()
                value = {hostile_key: PoisonOpaque()}
                hostile_key.armed = True
                self.assert_negative_receipt(self.malformed_at(key, value), key)

    def test_48_mixed_nested_custom_and_builtin_malformed_structures_close(self):
        for key in self.REQUIRED:
            with self.subTest(key=key):
                value = {
                    "outer": [
                        NoTouchMapping(),
                        {b"bytes-key": PoisonOpaque()},
                        [ThrowingItemsMapping(), frozenset({"x", "y"})],
                    ]
                }
                self.assert_negative_receipt(self.malformed_at(key, value), key)

    def test_49_cycles_mutual_shared_and_deep_graphs_remain_bounded(self):
        def circular_list():
            value = []
            value.append(value)
            return value

        def circular_mapping():
            value = {}
            value["self"] = value
            return value

        def mutual():
            left = []
            right = {"left": left}
            left.append(right)
            return {"left": left, "right": right}

        def shared():
            node = {b"k": PoisonOpaque()}
            return [node, node]

        def deep():
            root = []
            cursor = root
            for _ in range(96):
                nxt = []
                cursor.append(nxt)
                cursor = nxt
            cursor.append(b"leaf")
            return root

        makers = (circular_list, circular_mapping, mutual, shared, deep)
        for key in self.REQUIRED:
            for maker in makers:
                with self.subTest(key=key, maker=maker.__name__):
                    self.assert_negative_receipt(self.malformed_at(key, maker()), key)

    def test_50_original_non_json_shapes_remain_closed(self):
        makers = (
            lambda: b"not-an-id",
            lambda: {"bad", "set"},
            lambda: frozenset({"bad", "frozen"}),
            object,
        )
        for key in self.REQUIRED:
            for maker in makers:
                with self.subTest(key=key, maker=getattr(maker, "__name__", "lambda")):
                    self.assert_negative_receipt(self.malformed_at(key, maker()), key)

    def test_51_equivalent_malformed_classes_are_deterministic(self):
        makers = (
            ThrowingItemsMapping,
            NoTouchMapping,
            lambda: {b"k": "v"},
            lambda: [NoTouchMapping(), b"x"],
        )
        for key in self.REQUIRED:
            for maker in makers:
                with self.subTest(key=key, maker=getattr(maker, "__name__", "lambda")):
                    a = self.assert_negative_receipt(self.malformed_at(key, maker()), key)
                    b = self.assert_negative_receipt(self.malformed_at(key, maker()), key)
                    self.assertEqual(a, b)
                    self.assertEqual(a["proof_sha256"], b["proof_sha256"])

    def test_52_distinct_builtin_structure_remains_distinguishable(self):
        one = self.assert_negative_receipt(self.malformed_at("actor_id", [NoTouchMapping()]), "actor_id")
        two = self.assert_negative_receipt(self.malformed_at("actor_id", [NoTouchMapping(), NoTouchMapping()]), "actor_id")
        nested = self.assert_negative_receipt(self.malformed_at("actor_id", [[NoTouchMapping()]]), "actor_id")
        self.assertNotEqual(one["proof_sha256"], two["proof_sha256"])
        self.assertNotEqual(one["proof_sha256"], nested["proof_sha256"])

    def test_53_json_safe_positive_negative_and_malformed_are_exactly_r3(self):
        positive = fixture()
        negative = fixture()
        negative["execution_scope"] = "PROJECT_CURRENT"
        malformed = fixture()
        malformed["actor_id"] = 7
        for packet in (positive, negative, malformed):
            self.assertEqual(
                r4.evaluate_direct_positive_applicability(packet),
                r4._r3.evaluate_direct_positive_applicability(packet),
            )

    def test_54_scope_authority_evidence_and_project_current_controls_remain_closed(self):
        packets = []
        wrong_scope = fixture()
        wrong_scope["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong"
        packets.append(wrong_scope)
        wrong_authority = fixture()
        wrong_authority["claimed_positive_applicability_source"] = "V554"
        packets.append(wrong_authority)
        wrong_evidence = fixture()
        wrong_evidence["evidence"]["actor_activation"]["semantic_owner"] = "ROUTING"
        packets.append(wrong_evidence)
        stale = fixture()
        stale["evidence"]["developmental_phase"]["stale"] = True
        packets.append(stale)
        project_current = fixture()
        project_current["execution_scope"] = "PROJECT_CURRENT"
        packets.append(project_current)
        for index, packet in enumerate(packets):
            with self.subTest(index=index):
                result = r4.evaluate_direct_positive_applicability(packet)
                self.assertEqual(result["decision"], r4.NEGATIVE_DECISION, result)
                for effect in EFFECT_KEYS:
                    self.assertFalse(result[effect], effect)

    def test_55_unrelated_programmer_errors_remain_visible(self):
        original = r4._r3.evaluate_direct_positive_applicability
        def raise_type_error(_packet):
            raise TypeError("r4-deliberate-programmer-error")
        def raise_value_error(_packet):
            raise ValueError("r4-deliberate-programmer-error")
        def raise_runtime_error(_packet):
            raise RuntimeError("r4-deliberate-programmer-error")
        try:
            for exc_type, func in (
                (TypeError, raise_type_error),
                (ValueError, raise_value_error),
                (RuntimeError, raise_runtime_error),
            ):
                with self.subTest(exc_type=exc_type.__name__):
                    r4._r3.evaluate_direct_positive_applicability = func
                    with self.assertRaisesRegex(exc_type, "r4-deliberate-programmer-error"):
                        r4.evaluate_direct_positive_applicability(fixture())
        finally:
            r4._r3.evaluate_direct_positive_applicability = original

    def test_56_malformed_values_never_become_positive_identifiers(self):
        values = (
            NoTouchMapping(),
            ThrowingItemsMapping(),
            {b"k": "v"},
            [PoisonOpaque()],
        )
        for key in self.REQUIRED:
            for value in values:
                with self.subTest(key=key, value_type=type(value).__name__):
                    result = self.assert_negative_receipt(self.malformed_at(key, value), key)
                    self.assertNotEqual(result["decision"], r4.POSITIVE_DECISION)

    def test_57_r4_revision_identity_is_exact(self):
        self.assertEqual(r4.R4_CANDIDATE_REVISION, "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R4")


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CourtR4)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({
        "court": "OBL059_R4_GOVERNED_BOUNDED_COURT",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "successful": result.wasSuccessful(),
        "execution_scope": r4.SYNTHETIC_SCOPE,
        "project_current_state_created": False,
        "independent_review_performed": False,
    }, sort_keys=True))
    raise SystemExit(0 if result.wasSuccessful() else 1)
