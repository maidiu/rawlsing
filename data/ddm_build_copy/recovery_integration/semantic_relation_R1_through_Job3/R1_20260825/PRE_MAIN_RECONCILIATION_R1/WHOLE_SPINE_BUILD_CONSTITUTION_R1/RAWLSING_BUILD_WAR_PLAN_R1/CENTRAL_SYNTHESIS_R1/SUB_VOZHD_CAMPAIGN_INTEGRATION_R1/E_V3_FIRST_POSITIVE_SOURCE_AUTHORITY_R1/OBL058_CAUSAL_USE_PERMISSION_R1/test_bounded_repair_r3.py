"""Governed bounded repair court for OBL058 repaired candidate R3.

Producer-side verification only. This court is not the required fresh distinct
independent review of the frozen R3 candidate.
"""
from __future__ import annotations

import copy
import inspect
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import causal_use_permission_candidate as candidate  # noqa: E402
from causal_use_permission_candidate import (  # noqa: E402
    AUTHORITY_ID,
    SCHEMA_VERSION,
    DECISION_DENY,
    DECISION_PERMIT,
    FIXTURE_CLASS,
    NO_MATCHING_BASIS_KIND,
    REGISTERED_POSITIVE_BASIS_ID,
    REGISTERED_POSITIVE_SCOPE,
    SOURCE_BASIS_KIND,
    ExactScope,
    PermissionContractError,
    issue_noncurrent_synthetic_receipt,
    receipt_digest,
    validate_receipt,
)


class OBL058BoundedRepairR3Court(unittest.TestCase):
    def positive(self):
        return issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )

    def denial(self):
        return issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id="NONCURRENT_SYNTHETIC::basis::obl058-r3-unregistered",
        )

    def changed_scope(self, **changes) -> ExactScope:
        values = REGISTERED_POSITIVE_SCOPE.canonical()
        values.update(changes)
        return ExactScope(**values)

    def test_r3_01_registered_source_basis_permits_exact_scope(self):
        receipt = self.positive()
        self.assertEqual(DECISION_PERMIT, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_r3_02_revised_authority_and_schema_are_exact(self):
        receipt = self.positive()
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.2.0", AUTHORITY_ID)
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_RECEIPT@3.0.0", SCHEMA_VERSION)
        self.assertEqual(AUTHORITY_ID, receipt["authority_id"])
        self.assertEqual(SCHEMA_VERSION, receipt["schema_version"])

    def test_r3_03_registered_basis_proof_remains_exact_scope_bound(self):
        receipt = self.positive()
        self.assertEqual(SOURCE_BASIS_KIND, receipt["basis_kind"])
        self.assertEqual(REGISTERED_POSITIVE_BASIS_ID, receipt["basis_id"])
        self.assertEqual(receipt["scope_digest"], receipt["basis_scope_digest"])
        self.assertTrue(receipt["basis_proof_digest"])

    def test_r3_04_arbitrary_basis_id_denies(self):
        receipt = self.denial()
        self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))
        self.assertEqual(NO_MATCHING_BASIS_KIND, receipt["basis_kind"])

    def test_r3_05_whitespace_basis_id_fails_closed(self):
        with self.assertRaisesRegex(PermissionContractError, "missing_basis_id"):
            issue_noncurrent_synthetic_receipt(scope=REGISTERED_POSITIVE_SCOPE, basis_id="   ")

    def test_r3_06_caller_permission_boolean_remains_absent(self):
        parameters = inspect.signature(issue_noncurrent_synthetic_receipt).parameters
        self.assertNotIn("explicit_source_permission", parameters)

    def test_r3_07_caller_basis_kind_remains_absent(self):
        parameters = inspect.signature(issue_noncurrent_synthetic_receipt).parameters
        self.assertNotIn("basis_kind", parameters)

    def test_r3_08_no_arbitrary_body_origin_wrapper_is_module_visible(self):
        self.assertFalse(hasattr(candidate, "_wrap_source_issued_receipt"))
        self.assertFalse(hasattr(candidate, "_has_source_issued_provenance"))

    def test_r3_09_issued_receipt_has_no_transferable_marker_or_payload_slots(self):
        receipt = self.positive()
        self.assertFalse(hasattr(receipt, "_marker"))
        self.assertFalse(hasattr(receipt, "_data"))
        self.assertFalse(hasattr(receipt, "__dict__"))

    def test_r3_10_object_setattr_cannot_add_payload_slot(self):
        receipt = self.positive()
        with self.assertRaises(AttributeError):
            object.__setattr__(receipt, "_data", {})

    def test_r3_11_object_setattr_cannot_add_marker_slot(self):
        receipt = self.positive()
        with self.assertRaises(AttributeError):
            object.__setattr__(receipt, "_marker", object())

    def test_r3_12_public_scope_copy_mutation_does_not_rebind_issued_content(self):
        receipt = self.positive()
        visible_scope = receipt["scope"]
        visible_scope["actor_id"] = "NONCURRENT_SYNTHETIC::actor::caller-mutated-copy"
        self.assertEqual(DECISION_PERMIT, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))
        self.assertEqual(REGISTERED_POSITIVE_SCOPE.actor_id, receipt["scope"]["actor_id"])

    def test_r3_13_plain_copy_of_positive_is_not_source_issued(self):
        copied = dict(self.positive())
        with self.assertRaisesRegex(PermissionContractError, "receipt_not_issued_by_source_authority"):
            validate_receipt(copied, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_r3_14_recovered_concrete_type_fresh_instance_is_not_source_issued(self):
        receipt = self.positive()
        recovered_type = type(receipt)
        fresh = object.__new__(recovered_type)
        with self.assertRaisesRegex(PermissionContractError, "receipt_not_issued_by_source_authority"):
            validate_receipt(fresh, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_r3_15_recovered_concrete_type_normal_constructor_is_not_source_issued(self):
        receipt = self.positive()
        recovered_type = type(receipt)
        fresh = recovered_type()
        with self.assertRaisesRegex(PermissionContractError, "receipt_not_issued_by_source_authority"):
            validate_receipt(fresh, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_r3_16_copy_copy_does_not_acquire_source_origin(self):
        receipt = self.positive()
        copied = copy.copy(receipt)
        self.assertIsNot(receipt, copied)
        with self.assertRaisesRegex(PermissionContractError, "receipt_not_issued_by_source_authority"):
            validate_receipt(copied, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_r3_17_subclass_object_is_rejected_by_exact_type_identity(self):
        receipt = self.positive()
        base = type(receipt)

        class CallerSubclass(base):
            pass

        fake = object.__new__(CallerSubclass)
        with self.assertRaisesRegex(PermissionContractError, "receipt_not_issued_by_source_authority"):
            validate_receipt(fake, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_r3_18_subclass_origin_predicate_override_is_irrelevant(self):
        receipt = self.positive()
        base = type(receipt)

        class CallerSubclass(base):
            def _has_source_provenance(self):
                return True

        fake = object.__new__(CallerSubclass)
        with self.assertRaisesRegex(PermissionContractError, "receipt_not_issued_by_source_authority"):
            validate_receipt(fake, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_r3_19_denial_cannot_be_rewritten_into_accepted_positive_by_copy(self):
        denial = self.denial()
        rewritten = dict(denial)
        positive = self.positive()
        rewritten["decision"] = DECISION_PERMIT
        rewritten["basis_kind"] = SOURCE_BASIS_KIND
        rewritten["basis_id"] = REGISTERED_POSITIVE_BASIS_ID
        rewritten["basis_scope_digest"] = positive["basis_scope_digest"]
        rewritten["basis_proof_digest"] = positive["basis_proof_digest"]
        rewritten["receipt_digest"] = receipt_digest(rewritten)
        with self.assertRaisesRegex(PermissionContractError, "receipt_not_issued_by_source_authority"):
            validate_receipt(rewritten, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_r3_20_two_genuine_issuances_are_distinct_and_each_validate(self):
        first = self.positive()
        second = self.positive()
        self.assertIsNot(first, second)
        self.assertEqual(DECISION_PERMIT, validate_receipt(first, expected_scope=REGISTERED_POSITIVE_SCOPE))
        self.assertEqual(DECISION_PERMIT, validate_receipt(second, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def _assert_registered_basis_denies_changed_scope(self, other: ExactScope) -> None:
        receipt = issue_noncurrent_synthetic_receipt(scope=other, basis_id=REGISTERED_POSITIVE_BASIS_ID)
        self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=other))

    def test_r3_21_registered_basis_cannot_rebind_actor(self):
        self._assert_registered_basis_denies_changed_scope(
            self.changed_scope(actor_id="NONCURRENT_SYNTHETIC::actor::obl058-r3-a2")
        )

    def test_r3_22_registered_basis_cannot_rebind_world(self):
        self._assert_registered_basis_denies_changed_scope(
            self.changed_scope(world_id="NONCURRENT_SYNTHETIC::world::obl058-r3-w2")
        )

    def test_r3_23_registered_basis_cannot_rebind_subject(self):
        self._assert_registered_basis_denies_changed_scope(
            self.changed_scope(subject_id="NONCURRENT_SYNTHETIC::subject::obl058-r3-s2")
        )

    def test_r3_24_registered_basis_cannot_rebind_time(self):
        self._assert_registered_basis_denies_changed_scope(
            self.changed_scope(time_id="NONCURRENT_SYNTHETIC::time::obl058-r3-t2")
        )

    def test_r3_25_registered_basis_cannot_rebind_transition(self):
        self._assert_registered_basis_denies_changed_scope(
            self.changed_scope(transition_id="NONCURRENT_SYNTHETIC::transition::obl058-r3-tr2")
        )

    def _assert_scope_field_rejected(self, field: str, value: str) -> None:
        values = REGISTERED_POSITIVE_SCOPE.canonical()
        values[field] = value
        bad = ExactScope(**values)
        with self.assertRaisesRegex(PermissionContractError, f"noncurrent_synthetic_scope_required:{field}"):
            issue_noncurrent_synthetic_receipt(scope=bad, basis_id=REGISTERED_POSITIVE_BASIS_ID)

    def test_r3_26_project_current_actor_namespace_rejected(self):
        self._assert_scope_field_rejected("actor_id", "urn:rawlsing:v3:actor:project-current:a")

    def test_r3_27_project_current_world_namespace_rejected(self):
        self._assert_scope_field_rejected("world_id", "urn:rawlsing:v3:world:project-current:w")

    def test_r3_28_project_current_subject_namespace_rejected(self):
        self._assert_scope_field_rejected("subject_id", "urn:rawlsing:v3:subject:project-current:s")

    def test_r3_29_current_first_canary_subject_rejected(self):
        self._assert_scope_field_rejected(
            "subject_id",
            "urn:rawlsing:v3:subject:sha256:a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33",
        )

    def test_r3_30_project_current_time_namespace_rejected(self):
        self._assert_scope_field_rejected("time_id", "urn:rawlsing:v3:time:project-current:t")

    def test_r3_31_project_current_transition_namespace_rejected(self):
        self._assert_scope_field_rejected("transition_id", "urn:rawlsing:v3:transition:project-current:tr")

    def test_r3_32_explicit_project_current_fixture_label_rejected(self):
        with self.assertRaisesRegex(PermissionContractError, "project_current_or_unknown_fixture_not_authorized"):
            issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
                fixture_class="PROJECT_CURRENT",
            )

    def test_r3_33_wrong_expected_scope_rejected(self):
        receipt = self.positive()
        wrong = self.changed_scope(actor_id="NONCURRENT_SYNTHETIC::actor::wrong-expected")
        with self.assertRaisesRegex(PermissionContractError, "scope_mismatch_or_stale"):
            validate_receipt(receipt, expected_scope=wrong)

    def test_r3_34_fixture_class_is_exact_on_issued_receipt(self):
        self.assertEqual(FIXTURE_CLASS, self.positive()["fixture_class"])

    def test_r3_35_no_public_basis_registration_api_exists(self):
        self.assertFalse(hasattr(candidate, "register_source_basis"))
        self.assertFalse(hasattr(candidate, "register_noncurrent_synthetic_basis"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
