"""Governed bounded repair court for OBL058 repaired candidate R2.

This is producer-side repair verification, not the required independent review.
"""
from __future__ import annotations

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


class OBL058BoundedRepairR2Court(unittest.TestCase):
    def positive(self):
        return issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )

    def changed_scope(self, **changes) -> ExactScope:
        values = REGISTERED_POSITIVE_SCOPE.canonical()
        values.update(changes)
        return ExactScope(**values)

    def test_r2_01_registered_source_basis_permits_exact_scope(self):
        receipt = self.positive()
        self.assertEqual(DECISION_PERMIT, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_r2_02_positive_receipt_uses_revised_authority_and_schema(self):
        receipt = self.positive()
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.1.0", AUTHORITY_ID)
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_RECEIPT@2.0.0", SCHEMA_VERSION)
        self.assertEqual(AUTHORITY_ID, receipt["authority_id"])
        self.assertEqual(SCHEMA_VERSION, receipt["schema_version"])

    def test_r2_03_positive_receipt_carries_exact_basis_binding_proof(self):
        receipt = self.positive()
        self.assertEqual(SOURCE_BASIS_KIND, receipt["basis_kind"])
        self.assertEqual(REGISTERED_POSITIVE_BASIS_ID, receipt["basis_id"])
        self.assertEqual(receipt["scope_digest"], receipt["basis_scope_digest"])
        self.assertIsInstance(receipt["basis_proof_digest"], str)
        self.assertTrue(receipt["basis_proof_digest"])

    def test_r2_04_arbitrary_basis_id_cannot_mint_positive(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id="NONCURRENT_SYNTHETIC::basis::caller-arbitrary",
        )
        self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))
        self.assertEqual(NO_MATCHING_BASIS_KIND, receipt["basis_kind"])

    def test_r2_05_whitespace_basis_id_fails_closed(self):
        with self.assertRaisesRegex(PermissionContractError, "missing_basis_id"):
            issue_noncurrent_synthetic_receipt(scope=REGISTERED_POSITIVE_SCOPE, basis_id="   ")

    def test_r2_06_caller_permission_boolean_removed(self):
        parameters = inspect.signature(issue_noncurrent_synthetic_receipt).parameters
        self.assertNotIn("explicit_source_permission", parameters)

    def test_r2_07_caller_basis_kind_removed(self):
        parameters = inspect.signature(issue_noncurrent_synthetic_receipt).parameters
        self.assertNotIn("basis_kind", parameters)

    def test_r2_08_plain_copy_of_valid_receipt_loses_source_provenance(self):
        copied = dict(self.positive())
        with self.assertRaisesRegex(PermissionContractError, "receipt_not_issued_by_source_authority"):
            validate_receipt(copied, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_r2_09_manually_reconstructed_positive_is_rejected_even_with_matching_digest(self):
        copied = dict(self.positive())
        copied["receipt_digest"] = receipt_digest(copied)
        with self.assertRaisesRegex(PermissionContractError, "receipt_not_issued_by_source_authority"):
            validate_receipt(copied, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_r2_10_denial_rewrite_and_rehash_is_rejected(self):
        denial = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id="NONCURRENT_SYNTHETIC::basis::not-registered",
        )
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

    def test_r2_11_source_issued_receipt_is_read_only(self):
        receipt = self.positive()
        with self.assertRaises(TypeError):
            receipt["decision"] = DECISION_DENY  # type: ignore[index]

    def _assert_registered_basis_denies_changed_scope(self, other: ExactScope) -> None:
        receipt = issue_noncurrent_synthetic_receipt(
            scope=other,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=other))

    def test_r2_12_registered_basis_cannot_rebind_actor(self):
        self._assert_registered_basis_denies_changed_scope(
            self.changed_scope(actor_id="NONCURRENT_SYNTHETIC::actor::obl058-r2-a2")
        )

    def test_r2_13_registered_basis_cannot_rebind_world(self):
        self._assert_registered_basis_denies_changed_scope(
            self.changed_scope(world_id="NONCURRENT_SYNTHETIC::world::obl058-r2-w2")
        )

    def test_r2_14_registered_basis_cannot_rebind_subject(self):
        self._assert_registered_basis_denies_changed_scope(
            self.changed_scope(subject_id="NONCURRENT_SYNTHETIC::subject::obl058-r2-s2")
        )

    def test_r2_15_registered_basis_cannot_rebind_time(self):
        self._assert_registered_basis_denies_changed_scope(
            self.changed_scope(time_id="NONCURRENT_SYNTHETIC::time::obl058-r2-t2")
        )

    def test_r2_16_registered_basis_cannot_rebind_transition(self):
        self._assert_registered_basis_denies_changed_scope(
            self.changed_scope(transition_id="NONCURRENT_SYNTHETIC::transition::obl058-r2-tr2")
        )

    def _assert_scope_field_rejected(self, field: str, value: str) -> None:
        values = REGISTERED_POSITIVE_SCOPE.canonical()
        values[field] = value
        bad = ExactScope(**values)
        with self.assertRaisesRegex(PermissionContractError, f"noncurrent_synthetic_scope_required:{field}"):
            issue_noncurrent_synthetic_receipt(scope=bad, basis_id=REGISTERED_POSITIVE_BASIS_ID)

    def test_r2_17_project_current_actor_namespace_rejected(self):
        self._assert_scope_field_rejected("actor_id", "urn:rawlsing:v3:actor:project-current:a")

    def test_r2_18_project_current_world_namespace_rejected(self):
        self._assert_scope_field_rejected("world_id", "urn:rawlsing:v3:world:project-current:w")

    def test_r2_19_project_current_subject_namespace_rejected(self):
        self._assert_scope_field_rejected("subject_id", "urn:rawlsing:v3:subject:project-current:s")

    def test_r2_20_current_first_canary_subject_rejected(self):
        self._assert_scope_field_rejected(
            "subject_id",
            "urn:rawlsing:v3:subject:sha256:a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33",
        )

    def test_r2_21_project_current_time_namespace_rejected(self):
        self._assert_scope_field_rejected("time_id", "urn:rawlsing:v3:time:project-current:t")

    def test_r2_22_project_current_transition_namespace_rejected(self):
        self._assert_scope_field_rejected("transition_id", "urn:rawlsing:v3:transition:project-current:tr")

    def test_r2_23_explicit_project_current_fixture_label_rejected(self):
        with self.assertRaisesRegex(PermissionContractError, "project_current_or_unknown_fixture_not_authorized"):
            issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
                fixture_class="PROJECT_CURRENT",
            )

    def test_r2_24_wrong_expected_scope_rejected(self):
        receipt = self.positive()
        wrong = self.changed_scope(actor_id="NONCURRENT_SYNTHETIC::actor::wrong-expected")
        with self.assertRaisesRegex(PermissionContractError, "scope_mismatch_or_stale"):
            validate_receipt(receipt, expected_scope=wrong)

    def test_r2_25_fixture_class_is_exact_on_issued_receipt(self):
        self.assertEqual(FIXTURE_CLASS, self.positive()["fixture_class"])

    def test_r2_26_no_public_basis_registration_api_exists(self):
        self.assertFalse(hasattr(candidate, "register_source_basis"))
        self.assertFalse(hasattr(candidate, "register_noncurrent_synthetic_basis"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
