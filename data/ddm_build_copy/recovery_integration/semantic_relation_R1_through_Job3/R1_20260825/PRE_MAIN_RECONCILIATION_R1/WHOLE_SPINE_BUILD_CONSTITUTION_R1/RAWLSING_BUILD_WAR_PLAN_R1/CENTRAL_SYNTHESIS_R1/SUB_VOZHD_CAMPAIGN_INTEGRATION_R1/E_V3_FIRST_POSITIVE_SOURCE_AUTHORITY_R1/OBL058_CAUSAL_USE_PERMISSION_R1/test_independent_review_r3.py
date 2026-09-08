"""Fresh distinct independent review for frozen OBL058 R3 candidate.

Blocking probes intentionally assert that caller-reproducible provenance bypasses
are accepted. A green court proves the observed behavior is reproducible; the
reviewer's semantic PASS/FAIL is adjudicated separately.
"""
from __future__ import annotations

from collections.abc import Mapping
import copy
import hashlib
import json
import pickle
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import causal_use_permission_candidate as candidate  # noqa: E402
from causal_use_permission_candidate import (  # noqa: E402
    AUTHORITY_ID,
    DECISION_DENY,
    DECISION_PERMIT,
    FIXTURE_CLASS,
    NO_MATCHING_BASIS_KIND,
    REGISTERED_POSITIVE_BASIS_ID,
    REGISTERED_POSITIVE_SCOPE,
    SCHEMA_VERSION,
    SOURCE_BASIS_KIND,
    ExactScope,
    PermissionContractError,
    issue_noncurrent_synthetic_receipt,
    receipt_digest,
    scope_digest,
    validate_receipt,
)

CURRENT_FIRST_CANARY_SUBJECT = (
    "urn:rawlsing:v3:subject:sha256:"
    "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
)


def _closure_value(function, name):
    cells = dict(zip(function.__code__.co_freevars, function.__closure__ or ()))
    if name not in cells:
        raise AssertionError(f"closure value not reachable: {name}; got={tuple(cells)}")
    return cells[name].cell_contents


def _canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _public_positive_body():
    sd = scope_digest(REGISTERED_POSITIVE_SCOPE)
    proof_payload = {
        "basis_id": REGISTERED_POSITIVE_BASIS_ID,
        "scope_digest": sd,
        "basis_kind": SOURCE_BASIS_KIND,
        "decision": DECISION_PERMIT,
    }
    proof = hashlib.sha256(_canonical_json(proof_payload).encode("utf-8")).hexdigest()
    body = {
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


class CallerProxy(Mapping):
    def __init__(self, body):
        self.body = body

    def __getitem__(self, key):
        return self.body[key]

    def __iter__(self):
        return iter(self.body)

    def __len__(self):
        return len(self.body)


class OBL058R3IndependentReview(unittest.TestCase):
    def positive(self):
        return issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )

    def denial(self, suffix="independent-unregistered"):
        return issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=f"NONCURRENT_SYNTHETIC::basis::{suffix}",
        )

    def ledger(self):
        lookup = _closure_value(validate_receipt, "_lookup_exact_issued_body")
        return _closure_value(lookup, "issued_ledger")

    def replace_ledger_body(self, receipt, body):
        ledger = self.ledger()
        for index, (issued, original) in enumerate(ledger):
            if issued is receipt:
                ledger[index] = (issued, body)
                return ledger, index, original
        self.fail("issued receipt absent from source ledger")

    def assert_origin_rejected(self, receipt, expected_scope=REGISTERED_POSITIVE_SCOPE):
        with self.assertRaisesRegex(
            PermissionContractError, "receipt_not_issued_by_source_authority"
        ):
            validate_receipt(receipt, expected_scope=expected_scope)

    # Blocking source-origin probes. Green means the bypass is reproducible.

    def test_b01_issue_closure_exposes_internal_minting_helper(self):
        helper = _closure_value(issue_noncurrent_synthetic_receipt, "_new_issued_receipt")
        self.assertTrue(callable(helper))
        self.assertIn("issued_ledger", helper.__code__.co_freevars)

    def test_b02_closure_recovered_helper_mints_caller_positive_body(self):
        helper = _closure_value(issue_noncurrent_synthetic_receipt, "_new_issued_receipt")
        fabricated = helper(_public_positive_body())
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(fabricated, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_b03_closure_recovered_ledger_accepts_fabricated_exact_type_identity(self):
        source = self.denial("ledger-type-source")
        receipt_type = type(source)
        fabricated = object.__new__(receipt_type)
        ledger = self.ledger()
        ledger.append((fabricated, _public_positive_body()))
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(fabricated, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_b04_closure_recovered_ledger_rebinds_issued_denial_body_to_positive(self):
        receipt = self.denial("ledger-rebind")
        self.assertEqual(
            DECISION_DENY,
            validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )
        ledger, index, original = self.replace_ledger_body(receipt, _public_positive_body())
        try:
            self.assertEqual(
                DECISION_PERMIT,
                validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
            )
        finally:
            ledger[index] = (receipt, original)

    # Positive/negative and ordinary source-origin controls.

    def test_c01_registered_positive_control(self):
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(self.positive(), expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_c02_unregistered_basis_negative_control(self):
        self.assertEqual(
            DECISION_DENY,
            validate_receipt(self.denial(), expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_c03_plain_copy_and_proxy_are_not_source_issued(self):
        receipt = self.positive()
        self.assert_origin_rejected(dict(receipt))
        self.assert_origin_rejected(CallerProxy(dict(receipt)))

    def test_c04_exact_type_ordinary_and_object_new_construction_are_rejected_without_ledger(self):
        receipt_type = type(self.positive())
        ordinary = receipt_type()
        fabricated = object.__new__(receipt_type)
        self.assert_origin_rejected(ordinary)
        self.assert_origin_rejected(fabricated)

    def test_c05_copy_deepcopy_and_pickle_do_not_create_a_new_accepted_identity(self):
        receipt = self.positive()
        for label, operation in (
            ("copy", lambda: copy.copy(receipt)),
            ("deepcopy", lambda: copy.deepcopy(receipt)),
        ):
            with self.subTest(label=label):
                try:
                    clone = operation()
                except (TypeError, AttributeError, ValueError, pickle.PickleError):
                    continue
                if clone is receipt:
                    self.assertEqual(
                        DECISION_PERMIT,
                        validate_receipt(clone, expected_scope=REGISTERED_POSITIVE_SCOPE),
                    )
                else:
                    self.assert_origin_rejected(clone)
        try:
            payload = pickle.dumps(receipt)
            reconstructed = pickle.loads(payload)
        except (TypeError, AttributeError, ValueError, pickle.PickleError):
            return
        if reconstructed is not receipt:
            self.assert_origin_rejected(reconstructed)

    def test_c06_subclass_and_caller_defined_mapping_behavior_are_rejected(self):
        base = type(self.positive())

        class CallerReceipt(base):
            __slots__ = ()

            def __getitem__(self, key):
                return _public_positive_body()[key]

            def __iter__(self):
                return iter(_public_positive_body())

            def __len__(self):
                return len(_public_positive_body())

        self.assert_origin_rejected(object.__new__(CallerReceipt))

    def test_c07_public_scope_copy_mutation_does_not_change_authoritative_body(self):
        receipt = self.positive()
        public_scope = receipt["scope"]
        public_scope["actor_id"] = "NONCURRENT_SYNTHETIC::actor::caller-mutated"
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(
            REGISTERED_POSITIVE_SCOPE.actor_id,
            receipt["scope"]["actor_id"],
        )

    def test_c08_repeated_issuance_keeps_distinct_exact_identities(self):
        first = self.positive()
        second = self.positive()
        denial = self.denial("identity-sequence")
        self.assertIsNot(first, second)
        self.assertIsNot(first, denial)
        self.assertEqual(DECISION_PERMIT, validate_receipt(first, expected_scope=REGISTERED_POSITIVE_SCOPE))
        self.assertEqual(DECISION_PERMIT, validate_receipt(second, expected_scope=REGISTERED_POSITIVE_SCOPE))
        self.assertEqual(DECISION_DENY, validate_receipt(denial, expected_scope=REGISTERED_POSITIVE_SCOPE))

    # Exact scope/basis/fixture jurisdiction.

    def test_j01_registered_basis_is_exactly_bound_across_all_five_scope_fields(self):
        replacements = {
            "actor_id": "NONCURRENT_SYNTHETIC::actor::review-a2",
            "world_id": "NONCURRENT_SYNTHETIC::world::review-w2",
            "subject_id": "NONCURRENT_SYNTHETIC::subject::review-s2",
            "time_id": "NONCURRENT_SYNTHETIC::time::review-t2",
            "transition_id": "NONCURRENT_SYNTHETIC::transition::review-tr2",
        }
        for field, replacement in replacements.items():
            with self.subTest(field=field):
                values = REGISTERED_POSITIVE_SCOPE.canonical()
                values[field] = replacement
                scope = ExactScope(**values)
                receipt = issue_noncurrent_synthetic_receipt(
                    scope=scope, basis_id=REGISTERED_POSITIVE_BASIS_ID
                )
                self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=scope))

    def test_j02_replay_against_changed_expected_scope_rejected_for_all_five_fields(self):
        receipt = self.positive()
        replacements = {
            "actor_id": "NONCURRENT_SYNTHETIC::actor::replay-a",
            "world_id": "NONCURRENT_SYNTHETIC::world::replay-w",
            "subject_id": "NONCURRENT_SYNTHETIC::subject::replay-s",
            "time_id": "NONCURRENT_SYNTHETIC::time::replay-t",
            "transition_id": "NONCURRENT_SYNTHETIC::transition::replay-tr",
        }
        for field, replacement in replacements.items():
            with self.subTest(field=field):
                values = REGISTERED_POSITIVE_SCOPE.canonical()
                values[field] = replacement
                with self.assertRaisesRegex(PermissionContractError, "scope_mismatch_or_stale"):
                    validate_receipt(receipt, expected_scope=ExactScope(**values))

    def test_j03_field_specific_noncurrent_namespaces_reject_wrong_prefix(self):
        currentish = {
            "actor_id": "urn:rawlsing:v3:actor:project-current:a",
            "world_id": "urn:rawlsing:v3:world:project-current:w",
            "subject_id": "urn:rawlsing:v3:subject:project-current:s",
            "time_id": "urn:rawlsing:v3:time:project-current:t",
            "transition_id": "urn:rawlsing:v3:transition:project-current:tr",
        }
        for field, replacement in currentish.items():
            with self.subTest(field=field):
                values = REGISTERED_POSITIVE_SCOPE.canonical()
                values[field] = replacement
                with self.assertRaisesRegex(PermissionContractError, "noncurrent_synthetic_scope_required"):
                    issue_noncurrent_synthetic_receipt(
                        scope=ExactScope(**values), basis_id=REGISTERED_POSITIVE_BASIS_ID
                    )

    def test_j04_empty_suffix_rejected_for_all_five_namespaces(self):
        prefixes = {
            "actor_id": "NONCURRENT_SYNTHETIC::actor::",
            "world_id": "NONCURRENT_SYNTHETIC::world::",
            "subject_id": "NONCURRENT_SYNTHETIC::subject::",
            "time_id": "NONCURRENT_SYNTHETIC::time::",
            "transition_id": "NONCURRENT_SYNTHETIC::transition::",
        }
        for field, prefix in prefixes.items():
            with self.subTest(field=field):
                values = REGISTERED_POSITIVE_SCOPE.canonical()
                values[field] = prefix + "   "
                with self.assertRaisesRegex(PermissionContractError, "missing_or_invalid_scope"):
                    issue_noncurrent_synthetic_receipt(
                        scope=ExactScope(**values), basis_id=REGISTERED_POSITIVE_BASIS_ID
                    )

    def test_j05_wrong_field_namespace_rejected_for_all_five_fields(self):
        wrong = {
            "actor_id": "NONCURRENT_SYNTHETIC::world::wrong",
            "world_id": "NONCURRENT_SYNTHETIC::subject::wrong",
            "subject_id": "NONCURRENT_SYNTHETIC::time::wrong",
            "time_id": "NONCURRENT_SYNTHETIC::transition::wrong",
            "transition_id": "NONCURRENT_SYNTHETIC::actor::wrong",
        }
        for field, replacement in wrong.items():
            with self.subTest(field=field):
                values = REGISTERED_POSITIVE_SCOPE.canonical()
                values[field] = replacement
                with self.assertRaisesRegex(PermissionContractError, "noncurrent_synthetic_scope_required"):
                    issue_noncurrent_synthetic_receipt(
                        scope=ExactScope(**values), basis_id=REGISTERED_POSITIVE_BASIS_ID
                    )

    def test_j06_exact_current_first_canary_subject_rejected(self):
        values = REGISTERED_POSITIVE_SCOPE.canonical()
        values["subject_id"] = CURRENT_FIRST_CANARY_SUBJECT
        with self.assertRaisesRegex(PermissionContractError, "noncurrent_synthetic_scope_required:subject_id"):
            issue_noncurrent_synthetic_receipt(
                scope=ExactScope(**values), basis_id=REGISTERED_POSITIVE_BASIS_ID
            )

    def test_j07_non_synthetic_fixture_is_rejected(self):
        with self.assertRaisesRegex(PermissionContractError, "project_current_or_unknown_fixture_not_authorized"):
            issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
                fixture_class="PROJECT_CURRENT",
            )

    def test_j08_classification_routing_proximity_and_narrative_strings_cannot_infer_permission(self):
        inference_like_basis_ids = (
            "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
            "ADP-010",
            "ADP-019::OCCURRENCE_ADMITTED",
            "ROUTED_TO_SAME_ENDPOINT",
            "COLOCATED_SAME_TIME_AND_PLACE",
            "NARRATIVE_PLAUSIBILITY",
        )
        for basis_id in inference_like_basis_ids:
            with self.subTest(basis_id=basis_id):
                receipt = issue_noncurrent_synthetic_receipt(
                    scope=REGISTERED_POSITIVE_SCOPE, basis_id=basis_id
                )
                self.assertEqual(
                    DECISION_DENY,
                    validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
                )

    # Validation integrity controls, exercised by temporarily replacing only the
    # review process's ledger entry and restoring it after each subtest.

    def test_v01_wrong_authority_schema_fixture_and_decision_are_fail_closed(self):
        cases = (
            ("authority_id", "WRONG", "wrong_authority"),
            ("schema_version", "WRONG", "wrong_schema"),
            ("fixture_class", "PROJECT_CURRENT", "project_current_or_unknown_fixture_not_authorized"),
            ("decision", "MAYBE", "invalid_decision"),
        )
        for field, value, error in cases:
            with self.subTest(field=field):
                receipt = self.positive()
                body = dict(receipt)
                body[field] = value
                body["receipt_digest"] = receipt_digest(body)
                ledger, index, original = self.replace_ledger_body(receipt, body)
                try:
                    with self.assertRaisesRegex(PermissionContractError, error):
                        validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)
                finally:
                    ledger[index] = (receipt, original)

    def test_v02_missing_extra_and_malformed_scope_fields_fail_closed(self):
        for label in ("missing", "extra", "malformed_scope"):
            with self.subTest(label=label):
                receipt = self.positive()
                body = dict(receipt)
                if label == "missing":
                    body.pop("basis_id")
                elif label == "extra":
                    body["caller_extra"] = True
                else:
                    body["scope"] = "not-a-mapping"
                ledger, index, original = self.replace_ledger_body(receipt, body)
                try:
                    error = "malformed_receipt_keys" if label != "malformed_scope" else "malformed_scope"
                    with self.assertRaisesRegex(PermissionContractError, error):
                        validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)
                finally:
                    ledger[index] = (receipt, original)

    def test_v03_scope_and_basis_scope_digests_fail_closed(self):
        cases = (
            ("scope_digest", "0" * 64, "scope_digest_mismatch"),
            ("basis_scope_digest", "1" * 64, "basis_scope_mismatch"),
        )
        for field, value, error in cases:
            with self.subTest(field=field):
                receipt = self.positive()
                body = dict(receipt)
                body[field] = value
                body["receipt_digest"] = receipt_digest(body)
                ledger, index, original = self.replace_ledger_body(receipt, body)
                try:
                    with self.assertRaisesRegex(PermissionContractError, error):
                        validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)
                finally:
                    ledger[index] = (receipt, original)

    def test_v04_basis_proof_and_receipt_integrity_fail_closed(self):
        receipt = self.positive()
        body = dict(receipt)
        body["basis_proof_digest"] = "2" * 64
        body["receipt_digest"] = receipt_digest(body)
        ledger, index, original = self.replace_ledger_body(receipt, body)
        try:
            with self.assertRaisesRegex(PermissionContractError, "source_basis_proof_mismatch"):
                validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)
        finally:
            ledger[index] = (receipt, original)

        receipt = self.positive()
        body = dict(receipt)
        body["receipt_digest"] = "3" * 64
        ledger, index, original = self.replace_ledger_body(receipt, body)
        try:
            with self.assertRaisesRegex(PermissionContractError, "receipt_integrity_mismatch"):
                validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)
        finally:
            ledger[index] = (receipt, original)

    def test_v05_denial_basis_kind_and_proof_are_checked(self):
        receipt = self.denial("denial-integrity")
        body = dict(receipt)
        self.assertEqual(NO_MATCHING_BASIS_KIND, body["basis_kind"])
        body["basis_proof_digest"] = "4" * 64
        body["receipt_digest"] = receipt_digest(body)
        ledger, index, original = self.replace_ledger_body(receipt, body)
        try:
            with self.assertRaisesRegex(PermissionContractError, "denial_basis_proof_mismatch"):
                validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)
        finally:
            ledger[index] = (receipt, original)

    def test_n01_review_surface_remains_noncurrent_and_has_no_downstream_execution_api(self):
        forbidden_public_effect_names = {
            "create_actor",
            "activate_actor",
            "execute_adp008",
            "admit_adp019_occurrence",
            "install_obl056_positive",
            "execute_obl055",
            "create_encounter",
            "realize_oee",
            "adopt_hq",
        }
        self.assertTrue(forbidden_public_effect_names.isdisjoint(set(dir(candidate))))
        self.assertEqual("NONCURRENT_SYNTHETIC", FIXTURE_CLASS)


if __name__ == "__main__":
    unittest.main()
