import copy
import unittest

from causal_use_permission_candidate import (
    AUTHORITY_ID,
    DECISION_DENY,
    DECISION_PERMIT,
    FIXTURE_CLASS,
    ExactScope,
    PermissionContractError,
    issue_noncurrent_synthetic_receipt,
    receipt_digest,
    validate_receipt,
)


class OBL058BoundedCourt(unittest.TestCase):
    def setUp(self):
        self.scope = ExactScope(
            actor_id="NONCURRENT_SYNTHETIC::actor::first-canary-shape",
            world_id="NONCURRENT_SYNTHETIC::world::w1",
            subject_id="NONCURRENT_SYNTHETIC::subject::public-clinic-shape",
            time_id="NONCURRENT_SYNTHETIC::time::t1",
            transition_id="NONCURRENT_SYNTHETIC::transition::tr1",
        )

    def issue(self, **kw):
        args = dict(
            scope=self.scope,
            explicit_source_permission=True,
            basis_kind="EXPLICIT_SOURCE_OWNED_CAUSAL_USE_PERMISSION",
            basis_id="NONCURRENT_SYNTHETIC::basis::p1",
        )
        args.update(kw)
        return issue_noncurrent_synthetic_receipt(**args)

    def test_01_exact_scoped_positive_fixture_permits(self):
        r = self.issue()
        self.assertEqual(DECISION_PERMIT, validate_receipt(r, expected_scope=self.scope))
        self.assertEqual(FIXTURE_CLASS, r["fixture_class"])

    def test_02_exact_scoped_negative_fixture_denies(self):
        r = self.issue(explicit_source_permission=False)
        self.assertEqual(DECISION_DENY, validate_receipt(r, expected_scope=self.scope))

    def test_03_missing_actor_scope_fails_closed(self):
        with self.assertRaises(PermissionContractError):
            self.issue(scope=ExactScope("", self.scope.world_id, self.scope.subject_id, self.scope.time_id, self.scope.transition_id))

    def _wrong_scope_rejected(self, **changes):
        d = self.scope.canonical(); d.update(changes)
        wrong = ExactScope(**d)
        with self.assertRaises(PermissionContractError):
            validate_receipt(self.issue(), expected_scope=wrong)

    def test_04_wrong_actor_rejected(self): self._wrong_scope_rejected(actor_id="NONCURRENT_SYNTHETIC::actor::other")
    def test_05_wrong_world_rejected(self): self._wrong_scope_rejected(world_id="NONCURRENT_SYNTHETIC::world::other")
    def test_06_wrong_subject_rejected(self): self._wrong_scope_rejected(subject_id="NONCURRENT_SYNTHETIC::subject::other")
    def test_07_stale_or_wrong_time_rejected(self): self._wrong_scope_rejected(time_id="NONCURRENT_SYNTHETIC::time::stale")
    def test_08_wrong_transition_rejected(self): self._wrong_scope_rejected(transition_id="NONCURRENT_SYNTHETIC::transition::other")

    def test_09_wrong_authority_rejected(self):
        r = self.issue(); r["authority_id"] = "FOREIGN_AUTHORITY"; r["receipt_digest"] = receipt_digest(r)
        with self.assertRaisesRegex(PermissionContractError, "wrong_authority"):
            validate_receipt(r, expected_scope=self.scope)

    def test_10_malformed_scope_digest_rejected(self):
        r = self.issue(); r["scope_digest"] = "0" * 64; r["receipt_digest"] = receipt_digest(r)
        with self.assertRaisesRegex(PermissionContractError, "scope_digest_mismatch"):
            validate_receipt(r, expected_scope=self.scope)

    def test_11_extra_field_rejected(self):
        r = self.issue(); r["downstream_claim"] = "please trust me"
        with self.assertRaisesRegex(PermissionContractError, "malformed_receipt_keys"):
            validate_receipt(r, expected_scope=self.scope)

    def _surrogate_denies(self, basis_kind):
        r = self.issue(basis_kind=basis_kind)
        self.assertEqual(DECISION_DENY, validate_receipt(r, expected_scope=self.scope))

    def test_12_public_clinic_classification_does_not_imply_permission(self): self._surrogate_denies("SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL")
    def test_13_adp010_realization_authority_does_not_self_supply_permission(self): self._surrogate_denies("ADP010_REALIZATION_AUTHORITY")
    def test_14_occurrence_admission_does_not_imply_permission(self): self._surrogate_denies("OCCURRENCE_ADMISSION")
    def test_15_proximity_does_not_imply_permission(self): self._surrogate_denies("ACTOR_WORLD_TIME_PROXIMITY")
    def test_16_narrative_plausibility_does_not_imply_permission(self): self._surrogate_denies("NARRATIVE_PLAUSIBILITY")
    def test_17_downstream_consumption_does_not_imply_permission(self): self._surrogate_denies("DOWNSTREAM_CONSUMPTION")

    def test_18_project_current_fixture_issuance_is_forbidden(self):
        with self.assertRaisesRegex(PermissionContractError, "project_current_or_unknown_fixture_not_authorized"):
            self.issue(fixture_class="PROJECT_CURRENT")

    def test_19_unknown_positive_basis_denies(self):
        self._surrogate_denies("NICE_STORY_NOT_SOURCE_AUTHORITY")

    def test_20_tampering_after_issue_breaks_integrity(self):
        r = self.issue(); tampered = copy.deepcopy(r); tampered["basis_id"] = "NONCURRENT_SYNTHETIC::basis::tampered"
        with self.assertRaisesRegex(PermissionContractError, "receipt_integrity_mismatch"):
            validate_receipt(tampered, expected_scope=self.scope)

    def test_21_forged_positive_on_surrogate_basis_fails_closed(self):
        r = self.issue(basis_kind="SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL")
        r["decision"] = DECISION_PERMIT; r["receipt_digest"] = receipt_digest(r)
        with self.assertRaisesRegex(PermissionContractError, "positive_decision_without_source_owned_basis"):
            validate_receipt(r, expected_scope=self.scope)

    def test_22_candidate_authority_identity_is_exact(self):
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.0.0", AUTHORITY_ID)


if __name__ == "__main__":
    unittest.main(verbosity=2)
