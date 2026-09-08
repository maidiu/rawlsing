"""Fresh independent hostile court for frozen OBL058 candidate.

Important: several tests intentionally assert that a hostile construction is ACCEPTED.
A green execution proves the false-positive path is reproducible; it does not mean the
candidate passes hostile adjudication. See the independent hostile return artifact.
"""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from causal_use_permission_candidate import (  # noqa: E402
    AUTHORITY_ID,
    SCHEMA_VERSION,
    DECISION_DENY,
    DECISION_PERMIT,
    FIXTURE_CLASS,
    ExactScope,
    PermissionContractError,
    issue_noncurrent_synthetic_receipt,
    receipt_digest,
    scope_digest,
    validate_receipt,
)

MAGIC_BASIS = "EXPLICIT_SOURCE_OWNED_CAUSAL_USE_PERMISSION"
CURRENT_SUBJECT = "urn:rawlsing:v3:subject:sha256:a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"


class OBL058IndependentHostileReview(unittest.TestCase):
    def setUp(self) -> None:
        self.scope = ExactScope(
            actor_id="NONCURRENT_SYNTHETIC::actor::hostile-a1",
            world_id="NONCURRENT_SYNTHETIC::world::hostile-w1",
            subject_id="NONCURRENT_SYNTHETIC::subject::hostile-s1",
            time_id="NONCURRENT_SYNTHETIC::time::hostile-t1",
            transition_id="NONCURRENT_SYNTHETIC::transition::hostile-tr1",
        )

    def issue(self, scope: ExactScope | None = None, **kw):
        args = dict(
            scope=scope or self.scope,
            explicit_source_permission=True,
            basis_kind=MAGIC_BASIS,
            basis_id="NONCURRENT_SYNTHETIC::basis::shared-hostile-basis",
        )
        args.update(kw)
        return issue_noncurrent_synthetic_receipt(**args)

    def forge(self, scope: ExactScope | None = None, **kw):
        target = scope or self.scope
        receipt = {
            "authority_id": AUTHORITY_ID,
            "schema_version": SCHEMA_VERSION,
            "fixture_class": FIXTURE_CLASS,
            "scope": target.canonical(),
            "scope_digest": scope_digest(target),
            "decision": DECISION_PERMIT,
            "basis_kind": MAGIC_BASIS,
            "basis_id": "ATTACKER::UNVERIFIED::BASIS",
        }
        receipt.update(kw)
        receipt["receipt_digest"] = receipt_digest(receipt)
        return receipt

    # Blocking false-positive probes. Green means the vulnerability reproduced.

    def test_h01_caller_asserted_true_plus_magic_literal_mints_permit(self):
        r = self.issue(basis_id="ATTACKER::ARBITRARY::BASIS")
        self.assertEqual(DECISION_PERMIT, validate_receipt(r, expected_scope=self.scope))

    def test_h02_handcrafted_never_issued_receipt_validates_permit(self):
        r = self.forge()
        self.assertEqual(DECISION_PERMIT, validate_receipt(r, expected_scope=self.scope))

    def test_h03_deny_can_be_changed_to_permit_and_publicly_rehashed(self):
        r = self.issue(explicit_source_permission=False)
        self.assertEqual(DECISION_DENY, validate_receipt(r, expected_scope=self.scope))
        r["decision"] = DECISION_PERMIT
        r["receipt_digest"] = receipt_digest(r)
        self.assertEqual(DECISION_PERMIT, validate_receipt(r, expected_scope=self.scope))

    def test_h04_surrogate_denial_can_be_relabelled_magic_and_rehashed(self):
        r = self.issue(basis_kind="SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL")
        self.assertEqual(DECISION_DENY, validate_receipt(r, expected_scope=self.scope))
        r["basis_kind"] = MAGIC_BASIS
        r["decision"] = DECISION_PERMIT
        r["receipt_digest"] = receipt_digest(r)
        self.assertEqual(DECISION_PERMIT, validate_receipt(r, expected_scope=self.scope))

    def test_h05_any_nonempty_basis_id_supports_positive_issuance(self):
        r = self.issue(basis_id="attacker-picked-id-with-no-source-proof")
        self.assertEqual(DECISION_PERMIT, validate_receipt(r, expected_scope=self.scope))

    def test_h06_whitespace_only_basis_id_supports_positive_issuance(self):
        r = self.issue(basis_id="   ")
        self.assertEqual(DECISION_PERMIT, validate_receipt(r, expected_scope=self.scope))

    def test_h07_forged_nonstring_basis_id_validates_positive(self):
        r = self.forge(basis_id={"attacker": "structured-unverified-basis"})
        self.assertEqual(DECISION_PERMIT, validate_receipt(r, expected_scope=self.scope))

    def _different_scope(self, **changes) -> ExactScope:
        values = self.scope.canonical()
        values.update(changes)
        return ExactScope(**values)

    def _assert_same_basis_permits_both(self, other: ExactScope) -> None:
        a = self.issue(self.scope)
        b = self.issue(other)
        self.assertEqual(a["basis_id"], b["basis_id"])
        self.assertEqual(DECISION_PERMIT, validate_receipt(a, expected_scope=self.scope))
        self.assertEqual(DECISION_PERMIT, validate_receipt(b, expected_scope=other))

    def test_h08_same_unverified_basis_reused_across_actor(self):
        self._assert_same_basis_permits_both(self._different_scope(actor_id="NONCURRENT_SYNTHETIC::actor::hostile-a2"))

    def test_h09_same_unverified_basis_reused_across_world(self):
        self._assert_same_basis_permits_both(self._different_scope(world_id="NONCURRENT_SYNTHETIC::world::hostile-w2"))

    def test_h10_same_unverified_basis_reused_across_subject(self):
        self._assert_same_basis_permits_both(self._different_scope(subject_id="NONCURRENT_SYNTHETIC::subject::hostile-s2"))

    def test_h11_same_unverified_basis_reused_across_time(self):
        self._assert_same_basis_permits_both(self._different_scope(time_id="NONCURRENT_SYNTHETIC::time::hostile-t2"))

    def test_h12_same_unverified_basis_reused_across_transition(self):
        self._assert_same_basis_permits_both(self._different_scope(transition_id="NONCURRENT_SYNTHETIC::transition::hostile-tr2"))

    def test_h13_project_current_shaped_scope_masquerades_under_synthetic_label(self):
        current_shaped = ExactScope(
            actor_id="urn:rawlsing:v3:actor:project-current:hostile-a",
            world_id="urn:rawlsing:v3:world:project-current:hostile-w",
            subject_id="urn:rawlsing:v3:subject:project-current:hostile-s",
            time_id="urn:rawlsing:v3:time:project-current:hostile-t",
            transition_id="urn:rawlsing:v3:transition:project-current:hostile-tr",
        )
        r = self.issue(current_shaped)
        self.assertEqual(FIXTURE_CLASS, r["fixture_class"])
        self.assertEqual(DECISION_PERMIT, validate_receipt(r, expected_scope=current_shaped))

    def test_h14_current_first_canary_subject_is_not_bound_out_of_synthetic_fixture(self):
        mixed = ExactScope(
            actor_id="urn:rawlsing:v3:actor:project-current:hostile-a",
            world_id="urn:rawlsing:v3:world:project-current:hostile-w",
            subject_id=CURRENT_SUBJECT,
            time_id="urn:rawlsing:v3:time:project-current:hostile-t",
            transition_id="urn:rawlsing:v3:transition:project-current:hostile-tr",
        )
        r = self.issue(mixed)
        self.assertEqual(DECISION_PERMIT, validate_receipt(r, expected_scope=mixed))

    def test_h15_public_authority_strings_and_hashing_are_sufficient_to_impersonate_issuer(self):
        r = self.forge(basis_id="ATTACKER::NOT_ISSUED_BY_SOURCE_OWNER")
        self.assertEqual(AUTHORITY_ID, r["authority_id"])
        self.assertEqual(DECISION_PERMIT, validate_receipt(r, expected_scope=self.scope))

    def test_h16_positive_receipt_drops_the_permission_assertion_it_claims_to_prove(self):
        r = self.issue()
        self.assertNotIn("explicit_source_permission", r)
        self.assertEqual(DECISION_PERMIT, validate_receipt(r, expected_scope=self.scope))

    # Controls: existing fail-closed checks still operate, but do not cure H01-H16.

    def test_h17_control_wrong_authority_rejected_even_after_rehash(self):
        r = self.forge(authority_id="FOREIGN_AUTHORITY")
        with self.assertRaisesRegex(PermissionContractError, "wrong_authority"):
            validate_receipt(r, expected_scope=self.scope)

    def test_h18_control_known_surrogate_basis_still_denies(self):
        r = self.issue(basis_kind="OCCURRENCE_ADMISSION")
        self.assertEqual(DECISION_DENY, validate_receipt(r, expected_scope=self.scope))

    def test_h19_control_wrong_expected_scope_is_rejected(self):
        r = self.issue()
        wrong = self._different_scope(actor_id="NONCURRENT_SYNTHETIC::actor::wrong")
        with self.assertRaisesRegex(PermissionContractError, "scope_mismatch_or_stale"):
            validate_receipt(r, expected_scope=wrong)

    def test_h20_control_explicit_project_current_fixture_label_is_rejected(self):
        with self.assertRaisesRegex(PermissionContractError, "project_current_or_unknown_fixture_not_authorized"):
            self.issue(fixture_class="PROJECT_CURRENT")


if __name__ == "__main__":
    unittest.main(verbosity=2)
