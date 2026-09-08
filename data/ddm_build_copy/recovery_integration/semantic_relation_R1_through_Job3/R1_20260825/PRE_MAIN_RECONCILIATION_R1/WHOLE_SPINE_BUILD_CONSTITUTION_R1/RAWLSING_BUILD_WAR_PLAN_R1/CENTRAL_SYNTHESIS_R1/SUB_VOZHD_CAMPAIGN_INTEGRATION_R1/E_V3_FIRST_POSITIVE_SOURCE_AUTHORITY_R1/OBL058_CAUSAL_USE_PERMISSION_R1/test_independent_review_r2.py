"""Fresh distinct independent robustness review for frozen OBL058 R2 candidate.

Some checks intentionally assert that an incorrect-positive construction is accepted.
A green execution proves that behavior is reproducible; semantic PASS/FAIL is returned
separately by the independent reviewer.
"""
from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path
from types import MappingProxyType

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
    scope_digest,
    validate_receipt,
)


class OBL058R2IndependentReview(unittest.TestCase):
    def positive(self):
        return issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )

    def denial(self):
        return issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id="NONCURRENT_SYNTHETIC::basis::independent-unregistered",
        )

    def public_positive_body(self) -> dict[str, object]:
        sd = scope_digest(REGISTERED_POSITIVE_SCOPE)
        proof_payload = {
            "basis_id": REGISTERED_POSITIVE_BASIS_ID,
            "scope_digest": sd,
            "basis_kind": SOURCE_BASIS_KIND,
            "decision": DECISION_PERMIT,
        }
        proof = hashlib.sha256(
            json.dumps(
                proof_payload,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=True,
            ).encode("utf-8")
        ).hexdigest()
        body: dict[str, object] = {
            "authority_id": AUTHORITY_ID,
            "schema_version": SCHEMA_VERSION,
            "fixture_class": FIXTURE_CLASS,
            "scope": REGISTERED_POSITIVE_SCOPE.canonical(),
            "scope_digest": sd,
            "decision": DECISION_PERMIT,
            "basis_kind": SOURCE_BASIS_KIND,
            "basis_id": REGISTERED_POSITIVE_BASIS_ID,
            "basis_scope_digest": sd,
            "basis_proof_digest": proof,
        }
        body["receipt_digest"] = receipt_digest(body)
        return body

    # Blocking incorrect-positive probes. Green means the candidate reproduced them.

    def test_i01_module_wrapper_turns_caller_mapping_into_recognized_source_receipt(self):
        body = self.public_positive_body()
        wrapper = getattr(candidate, "_wrap_source_issued_receipt")
        reconstructed = wrapper(body)
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(reconstructed, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_i02_issued_denial_internal_data_can_be_rebound_to_positive(self):
        receipt = self.denial()
        self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))
        receipt._data = MappingProxyType(self.public_positive_body())  # type: ignore[attr-defined]
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_i03_marker_from_issued_denial_can_construct_new_recognized_positive(self):
        source_receipt = self.denial()
        receipt_type = type(source_receipt)
        recreated = receipt_type(
            self.public_positive_body(),
            source_receipt._marker,  # type: ignore[attr-defined]
        )
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(recreated, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_i04_subclass_can_self_assert_source_provenance(self):
        base_type = type(self.denial())
        body = self.public_positive_body()

        class CallerConstructedReceipt(base_type):
            __slots__ = ("_caller_data",)

            def __init__(self, data):
                self._caller_data = data

            def __getitem__(self, key):
                return self._caller_data[key]

            def __iter__(self):
                return iter(self._caller_data)

            def __len__(self):
                return len(self._caller_data)

            def _has_source_provenance(self):
                return True

        constructed = CallerConstructedReceipt(body)
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(constructed, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    # Controls confirming the repaired public semantic checks otherwise operate.

    def test_i05_registered_positive_still_validates(self):
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(self.positive(), expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_i06_plain_mapping_copy_is_rejected(self):
        copied = dict(self.positive())
        with self.assertRaisesRegex(PermissionContractError, "receipt_not_issued_by_source_authority"):
            validate_receipt(copied, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_i07_unregistered_basis_denies(self):
        self.assertEqual(
            DECISION_DENY,
            validate_receipt(self.denial(), expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_i08_registered_basis_is_exact_scope_bound(self):
        fields = {
            "actor_id": "NONCURRENT_SYNTHETIC::actor::independent-a2",
            "world_id": "NONCURRENT_SYNTHETIC::world::independent-w2",
            "subject_id": "NONCURRENT_SYNTHETIC::subject::independent-s2",
            "time_id": "NONCURRENT_SYNTHETIC::time::independent-t2",
            "transition_id": "NONCURRENT_SYNTHETIC::transition::independent-tr2",
        }
        for field, replacement in fields.items():
            with self.subTest(field=field):
                values = REGISTERED_POSITIVE_SCOPE.canonical()
                values[field] = replacement
                scope = ExactScope(**values)
                receipt = issue_noncurrent_synthetic_receipt(
                    scope=scope,
                    basis_id=REGISTERED_POSITIVE_BASIS_ID,
                )
                self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=scope))

    def test_i09_project_current_namespaces_fail_closed_for_every_scope_field(self):
        fields = {
            "actor_id": "urn:rawlsing:v3:actor:project-current:a",
            "world_id": "urn:rawlsing:v3:world:project-current:w",
            "subject_id": "urn:rawlsing:v3:subject:project-current:s",
            "time_id": "urn:rawlsing:v3:time:project-current:t",
            "transition_id": "urn:rawlsing:v3:transition:project-current:tr",
        }
        for field, replacement in fields.items():
            with self.subTest(field=field):
                values = REGISTERED_POSITIVE_SCOPE.canonical()
                values[field] = replacement
                scope = ExactScope(**values)
                with self.assertRaisesRegex(PermissionContractError, "noncurrent_synthetic_scope_required"):
                    issue_noncurrent_synthetic_receipt(
                        scope=scope,
                        basis_id=REGISTERED_POSITIVE_BASIS_ID,
                    )

    def test_i10_current_first_canary_subject_fails_closed(self):
        values = REGISTERED_POSITIVE_SCOPE.canonical()
        values["subject_id"] = "urn:rawlsing:v3:subject:sha256:a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
        scope = ExactScope(**values)
        with self.assertRaisesRegex(PermissionContractError, "noncurrent_synthetic_scope_required:subject_id"):
            issue_noncurrent_synthetic_receipt(
                scope=scope,
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
            )

    def test_i11_wrong_fixture_label_fails_closed(self):
        with self.assertRaisesRegex(PermissionContractError, "project_current_or_unknown_fixture_not_authorized"):
            issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
                fixture_class="PROJECT_CURRENT",
            )

    def test_i12_wrong_expected_scope_is_rejected(self):
        values = REGISTERED_POSITIVE_SCOPE.canonical()
        values["actor_id"] = "NONCURRENT_SYNTHETIC::actor::wrong-expected"
        wrong = ExactScope(**values)
        with self.assertRaisesRegex(PermissionContractError, "scope_mismatch_or_stale"):
            validate_receipt(self.positive(), expected_scope=wrong)

    def test_i13_nested_scope_mutation_is_detected(self):
        receipt = self.positive()
        receipt["scope"]["actor_id"] = "NONCURRENT_SYNTHETIC::actor::mutated"  # type: ignore[index]
        with self.assertRaises(PermissionContractError):
            validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_i14_wrapped_wrong_authority_is_still_rejected(self):
        body = self.public_positive_body()
        body["authority_id"] = "FOREIGN_AUTHORITY"
        body["receipt_digest"] = receipt_digest(body)
        wrapped = candidate._wrap_source_issued_receipt(body)
        with self.assertRaisesRegex(PermissionContractError, "wrong_authority"):
            validate_receipt(wrapped, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_i15_wrapped_wrong_schema_is_still_rejected(self):
        body = self.public_positive_body()
        body["schema_version"] = "FOREIGN_SCHEMA"
        body["receipt_digest"] = receipt_digest(body)
        wrapped = candidate._wrap_source_issued_receipt(body)
        with self.assertRaisesRegex(PermissionContractError, "wrong_schema"):
            validate_receipt(wrapped, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_i16_wrapped_bad_basis_proof_is_rejected(self):
        body = self.public_positive_body()
        body["basis_proof_digest"] = "0" * 64
        body["receipt_digest"] = receipt_digest(body)
        wrapped = candidate._wrap_source_issued_receipt(body)
        with self.assertRaisesRegex(PermissionContractError, "source_basis_proof_mismatch"):
            validate_receipt(wrapped, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_i17_wrapped_basis_scope_mismatch_is_rejected(self):
        body = self.public_positive_body()
        body["basis_scope_digest"] = "0" * 64
        body["receipt_digest"] = receipt_digest(body)
        wrapped = candidate._wrap_source_issued_receipt(body)
        with self.assertRaisesRegex(PermissionContractError, "basis_scope_mismatch"):
            validate_receipt(wrapped, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_i18_wrapped_denial_conflicting_with_registered_positive_is_rejected(self):
        body = self.public_positive_body()
        body["decision"] = DECISION_DENY
        body["basis_kind"] = NO_MATCHING_BASIS_KIND
        body["receipt_digest"] = receipt_digest(body)
        wrapped = candidate._wrap_source_issued_receipt(body)
        with self.assertRaisesRegex(PermissionContractError, "denial_conflicts_with_registered_source_basis"):
            validate_receipt(wrapped, expected_scope=REGISTERED_POSITIVE_SCOPE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
