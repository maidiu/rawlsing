"""Governed bounded court for OBL059 R3 serialization-boundary repair."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
R2_DIR = HERE.parent / "OBL059_POSITIVE_APPLICABILITY_R2"
R3_AUTHORITY = HERE / "positive_applicability_authority_r3.py"

r3_spec = importlib.util.spec_from_file_location("_obl059_r3_authority", R3_AUTHORITY)
if r3_spec is None or r3_spec.loader is None:
    raise RuntimeError(f"cannot load R3 authority: {R3_AUTHORITY}")
r3 = importlib.util.module_from_spec(r3_spec)
r3_spec.loader.exec_module(r3)

r2_court_path = R2_DIR / "governed_bounded_court_r2.py"
r2_spec = importlib.util.spec_from_file_location("_obl059_r2_court", r2_court_path)
if r2_spec is None or r2_spec.loader is None:
    raise RuntimeError(f"cannot load R2 court: {r2_court_path}")
r2_court = importlib.util.module_from_spec(r2_spec)
r2_spec.loader.exec_module(r2_court)

r2_court.r2.evaluate_direct_positive_applicability = r3.evaluate_direct_positive_applicability
r2_court.r1_court.evaluate_direct_positive_applicability = r3.evaluate_direct_positive_applicability


def fixture():
    return r2_court.r1_court.fixture()


class CourtR3(r2_court.CourtR2):
    REQUIRED = tuple(r3._REQUIRED_BINDINGS)

    def assert_nonserializable_binding_closes(self, key, value):
        packet = fixture()
        packet[key] = value
        result = r3.evaluate_direct_positive_applicability(packet)
        self.assertEqual(result["decision"], r3.NEGATIVE_DECISION, result)
        self.assertEqual(result["reason"], f"MALFORMED_BINDING:{key}", result)
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64)
        self.assertNotIsInstance(result["bindings"][key], str)
        for effect in (
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
        ):
            self.assertFalse(result[effect], effect)
        return result

    def test_35_mapping_with_bytes_key_closes_at_every_required_binding(self):
        for key in self.REQUIRED:
            with self.subTest(key=key):
                self.assert_nonserializable_binding_closes(
                    key, {b"non-json-key": "value"}
                )

    def test_36_circular_list_closes_at_every_required_binding(self):
        for key in self.REQUIRED:
            with self.subTest(key=key):
                circular = []
                circular.append(circular)
                self.assert_nonserializable_binding_closes(key, circular)

    def test_37_circular_mapping_closes_at_every_required_binding(self):
        for key in self.REQUIRED:
            with self.subTest(key=key):
                circular = {}
                circular["self"] = circular
                self.assert_nonserializable_binding_closes(key, circular)

    def test_38_original_non_json_shapes_close_at_every_required_binding(self):
        factories = {
            "bytes": lambda: b"not-a-valid-id",
            "set": lambda: {"not", "a", "valid", "id"},
            "frozenset": lambda: frozenset({"not", "a", "valid", "id"}),
            "opaque_object": object,
        }
        for key in self.REQUIRED:
            for label, factory in factories.items():
                with self.subTest(key=key, shape=label):
                    self.assert_nonserializable_binding_closes(key, factory())

    def test_39_nested_non_json_structures_close_at_every_required_binding(self):
        for key in self.REQUIRED:
            with self.subTest(key=key, shape="nested_bytes_key_set"):
                value = {"outer": [{b"k": {"set-value", "other"}}]}
                self.assert_nonserializable_binding_closes(key, value)
            with self.subTest(key=key, shape="nested_cycle"):
                loop = []
                value = {"outer": [loop]}
                loop.append(value)
                self.assert_nonserializable_binding_closes(key, value)

    def test_40_repeated_receipts_are_deterministic_for_same_malformed_class(self):
        def mapping_packet():
            p = fixture()
            p["actor_id"] = {b"k": "v"}
            return p

        def circular_packet():
            p = fixture()
            loop = []
            loop.append(loop)
            p["world_id"] = loop
            return p

        def opaque_packet():
            p = fixture()
            p["adp010_opportunity_id"] = object()
            return p

        for maker in (mapping_packet, circular_packet, opaque_packet):
            with self.subTest(maker=maker.__name__):
                a = r3.evaluate_direct_positive_applicability(maker())
                b = r3.evaluate_direct_positive_applicability(maker())
                self.assertEqual(a, b)
                json.dumps(a, sort_keys=True)

    def test_41_valid_json_safe_positive_and_negative_are_exactly_r2(self):
        positive = fixture()
        self.assertEqual(
            r3.evaluate_direct_positive_applicability(positive),
            r3._r2.evaluate_direct_positive_applicability(positive),
        )

        negative = fixture()
        negative["execution_scope"] = "PROJECT_CURRENT"
        self.assertEqual(
            r3.evaluate_direct_positive_applicability(negative),
            r3._r2.evaluate_direct_positive_applicability(negative),
        )

        malformed_but_json_safe = fixture()
        malformed_but_json_safe["actor_id"] = 7
        self.assertEqual(
            r3.evaluate_direct_positive_applicability(malformed_but_json_safe),
            r3._r2.evaluate_direct_positive_applicability(malformed_but_json_safe),
        )

    def test_42_wrong_scope_authority_and_project_current_controls_remain_closed(self):
        wrong_scope = fixture()
        wrong_scope["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong"
        self.assertEqual(
            r3.evaluate_direct_positive_applicability(wrong_scope)["decision"],
            r3.NEGATIVE_DECISION,
        )

        wrong_authority = fixture()
        wrong_authority["claimed_positive_applicability_source"] = "V554"
        self.assertEqual(
            r3.evaluate_direct_positive_applicability(wrong_authority)["decision"],
            r3.NEGATIVE_DECISION,
        )

        project_current = fixture()
        project_current["execution_scope"] = "PROJECT_CURRENT"
        result = r3.evaluate_direct_positive_applicability(project_current)
        self.assertEqual(result["decision"], r3.NEGATIVE_DECISION)
        self.assertFalse(result["project_current_state_created"])
        self.assertFalse(result["current_positive_obl056_installed"])
        self.assertFalse(result["obl055_executed"])
        self.assertFalse(result["encounter_created"])
        self.assertFalse(result["oee_realized"])

    def test_43_unrelated_programmer_errors_are_not_masked(self):
        original = r3._r2.evaluate_direct_positive_applicability

        def raise_type_error(_packet):
            raise TypeError("deliberate-programmer-error")

        def raise_value_error(_packet):
            raise ValueError("deliberate-programmer-error")

        try:
            r3._r2.evaluate_direct_positive_applicability = raise_type_error
            with self.assertRaisesRegex(TypeError, "deliberate-programmer-error"):
                r3.evaluate_direct_positive_applicability(fixture())

            r3._r2.evaluate_direct_positive_applicability = raise_value_error
            with self.assertRaisesRegex(ValueError, "deliberate-programmer-error"):
                r3.evaluate_direct_positive_applicability(fixture())
        finally:
            r3._r2.evaluate_direct_positive_applicability = original

    def test_44_r3_revision_identity_is_exact(self):
        self.assertEqual(
            r3.R3_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R3",
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CourtR3)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(
        json.dumps(
            {
                "court": "OBL059_R3_GOVERNED_BOUNDED_COURT",
                "tests_run": result.testsRun,
                "failures": len(result.failures),
                "errors": len(result.errors),
                "successful": result.wasSuccessful(),
                "execution_scope": r3.SYNTHETIC_SCOPE,
                "project_current_state_created": False,
                "independent_review_performed": False,
            },
            sort_keys=True,
        )
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
