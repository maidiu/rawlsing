"""Producer governed bounded-repair court for frozen OBL058 R4 candidate.

This is repair verification only. It does not perform the required fresh distinct
independent review of the frozen R4 candidate.
"""
from __future__ import annotations

import copy
import inspect
import json
import pickle
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import causal_use_permission_candidate_r4 as candidate  # noqa: E402
from causal_use_permission_candidate_r4 import (  # noqa: E402
    DECISION_DENY,
    DECISION_PERMIT,
    FIXTURE_CLASS,
    REGISTERED_POSITIVE_BASIS_ID,
    REGISTERED_POSITIVE_SCOPE,
    ExactScope,
    PermissionContractError,
    issue_noncurrent_synthetic_receipt,
    validate_receipt,
)

CURRENT_FIRST_CANARY_SUBJECT = (
    "urn:rawlsing:v3:subject:sha256:"
    "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
)


class CallerProxy(dict):
    pass


class OBL058BoundedRepairR4Court(unittest.TestCase):
    def positive(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(receipt.close)
        return receipt

    def denial(self, suffix: str = "court-unregistered"):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=f"NONCURRENT_SYNTHETIC::basis::{suffix}",
        )
        self.addCleanup(receipt.close)
        return receipt

    def changed_scope(self, field: str, value: str) -> ExactScope:
        values = REGISTERED_POSITIVE_SCOPE.canonical()
        values[field] = value
        return ExactScope(**values)

    def assert_origin_rejected(self, receipt, scope=REGISTERED_POSITIVE_SCOPE):
        with self.assertRaisesRegex(
            PermissionContractError, "receipt_not_issued_by_source_authority"
        ):
            validate_receipt(receipt, expected_scope=scope)

    def test_r4_01_valid_source_owned_positive_and_negative_controls(self):
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(self.positive(), expected_scope=REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(
            DECISION_DENY,
            validate_receipt(self.denial(), expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_r4_02_parent_introspection_exposes_no_authoritative_ledger_or_closure_state(self):
        functions = (
            issue_noncurrent_synthetic_receipt,
            validate_receipt,
            candidate._start_receipt_authority,
            candidate._service_roundtrip,
        )
        for function in functions:
            with self.subTest(function=function.__name__):
                self.assertIsNone(function.__closure__)
                self.assertEqual((), function.__code__.co_freevars)
                self.assertFalse(function.__dict__)
                self.assertIs(function.__globals__, candidate.__dict__)
        self.assertNotIn("issued_ledger", candidate.__dict__)
        self.assertNotIn("_SOURCE_BASIS_REGISTRY", candidate.__dict__)
        self.assertNotIn("register_source_basis", candidate.__dict__)
        self.assertFalse(
            any(isinstance(value, subprocess.Popen) for value in candidate.__dict__.values())
        )

    def test_r4_03_one_shot_child_rejects_second_initialization_and_caller_body_registration(self):
        receipt = self.denial("protocol")
        write_fd = object.__getattribute__(receipt, "_write_fd")
        read_fd = object.__getattribute__(receipt, "_read_fd")
        with self.assertRaisesRegex(PermissionContractError, "service_protocol_error"):
            candidate._service_roundtrip(
                write_fd,
                read_fd,
                {
                    "op": "initialize",
                    "object_id": id(receipt),
                    "scope": REGISTERED_POSITIVE_SCOPE.canonical(),
                    "basis_id": REGISTERED_POSITIVE_BASIS_ID,
                    "fixture_class": FIXTURE_CLASS,
                },
            )
        with self.assertRaises(TypeError):
            candidate._start_receipt_authority(
                object_id=id(receipt),
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
                fixture_class=FIXTURE_CLASS,
                body_json="{}",
            )

    def test_r4_04_issued_denial_body_cannot_be_rebound_to_positive(self):
        denial = self.denial("rebind")
        positive = self.positive()
        original = object.__getattribute__(denial, "_body_json")
        positive_body = object.__getattribute__(positive, "_body_json")
        object.__setattr__(denial, "_body_json", positive_body)
        try:
            self.assert_origin_rejected(denial)
        finally:
            object.__setattr__(denial, "_body_json", original)
        self.assertEqual(
            DECISION_DENY,
            validate_receipt(denial, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_r4_05_copying_all_parent_visible_positive_state_to_denial_identity_fails(self):
        denial = self.denial("state-swap")
        positive = self.positive()
        attrs = ("_body_json", "_write_fd", "_read_fd", "_proc")
        saved = [object.__getattribute__(denial, name) for name in attrs]
        for name in attrs:
            object.__setattr__(denial, name, object.__getattribute__(positive, name))
        try:
            self.assert_origin_rejected(denial)
        finally:
            for name, value in zip(attrs, saved):
                object.__setattr__(denial, name, value)

    def test_r4_06_exact_receipt_type_constructor_and_object_new_fabrication_fail(self):
        receipt_type = type(self.positive())
        self.assert_origin_rejected(receipt_type())
        self.assert_origin_rejected(object.__new__(receipt_type))

    def test_r4_07_exact_type_with_copied_positive_state_still_fails_identity_binding(self):
        positive = self.positive()
        fabricated = type(positive)()
        for name in ("_body_json", "_write_fd", "_read_fd", "_proc"):
            object.__setattr__(fabricated, name, object.__getattribute__(positive, name))
        self.assert_origin_rejected(fabricated)

    def test_r4_08_subclass_plain_mapping_and_proxy_reconstruction_fail(self):
        positive = self.positive()
        base = type(positive)

        class CallerReceipt(base):
            pass

        self.assert_origin_rejected(CallerReceipt())
        self.assert_origin_rejected(dict(positive))
        self.assert_origin_rejected(CallerProxy(dict(positive)))

    def test_r4_09_copy_deepcopy_and_pickle_are_rejected(self):
        receipt = self.positive()
        for label, operation in (
            ("copy", lambda: copy.copy(receipt)),
            ("deepcopy", lambda: copy.deepcopy(receipt)),
            ("pickle", lambda: pickle.dumps(receipt)),
        ):
            with self.subTest(label=label):
                with self.assertRaises(TypeError):
                    operation()

    def test_r4_10_json_serialized_deserialized_mapping_is_not_source_issued(self):
        receipt = self.positive()
        reconstructed = json.loads(json.dumps(dict(receipt)))
        self.assert_origin_rejected(reconstructed)

    def test_r4_11_public_scope_copy_mutation_does_not_change_authoritative_body(self):
        receipt = self.positive()
        visible_scope = receipt["scope"]
        visible_scope["actor_id"] = "NONCURRENT_SYNTHETIC::actor::caller-mutated"
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_r4_12_registered_basis_is_exactly_bound_across_all_five_scope_fields(self):
        replacements = {
            "actor_id": "NONCURRENT_SYNTHETIC::actor::changed",
            "world_id": "NONCURRENT_SYNTHETIC::world::changed",
            "subject_id": "NONCURRENT_SYNTHETIC::subject::changed",
            "time_id": "NONCURRENT_SYNTHETIC::time::changed",
            "transition_id": "NONCURRENT_SYNTHETIC::transition::changed",
        }
        for field, replacement in replacements.items():
            with self.subTest(field=field):
                scope = self.changed_scope(field, replacement)
                receipt = issue_noncurrent_synthetic_receipt(
                    scope=scope, basis_id=REGISTERED_POSITIVE_BASIS_ID
                )
                self.addCleanup(receipt.close)
                self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=scope))

    def test_r4_13_cross_scope_replay_is_rejected_for_every_scope_field(self):
        receipt = self.positive()
        replacements = {
            "actor_id": "NONCURRENT_SYNTHETIC::actor::replay",
            "world_id": "NONCURRENT_SYNTHETIC::world::replay",
            "subject_id": "NONCURRENT_SYNTHETIC::subject::replay",
            "time_id": "NONCURRENT_SYNTHETIC::time::replay",
            "transition_id": "NONCURRENT_SYNTHETIC::transition::replay",
        }
        for field, replacement in replacements.items():
            with self.subTest(field=field):
                with self.assertRaisesRegex(PermissionContractError, "scope_mismatch_or_stale"):
                    validate_receipt(
                        receipt,
                        expected_scope=self.changed_scope(field, replacement),
                    )

    def test_r4_14_project_current_shaped_namespaces_fail_closed_for_every_field(self):
        replacements = {
            "actor_id": "urn:rawlsing:v3:actor:project-current:a",
            "world_id": "urn:rawlsing:v3:world:project-current:w",
            "subject_id": "urn:rawlsing:v3:subject:project-current:s",
            "time_id": "urn:rawlsing:v3:time:project-current:t",
            "transition_id": "urn:rawlsing:v3:transition:project-current:tr",
        }
        for field, replacement in replacements.items():
            with self.subTest(field=field):
                with self.assertRaisesRegex(
                    PermissionContractError, "noncurrent_synthetic_scope_required"
                ):
                    issue_noncurrent_synthetic_receipt(
                        scope=self.changed_scope(field, replacement),
                        basis_id=REGISTERED_POSITIVE_BASIS_ID,
                    )

    def test_r4_15_exact_current_first_canary_subject_is_rejected(self):
        with self.assertRaisesRegex(
            PermissionContractError, "noncurrent_synthetic_scope_required:subject_id"
        ):
            issue_noncurrent_synthetic_receipt(
                scope=self.changed_scope("subject_id", CURRENT_FIRST_CANARY_SUBJECT),
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
            )

    def test_r4_16_wrong_field_namespace_and_empty_suffix_are_rejected(self):
        with self.assertRaises(PermissionContractError):
            issue_noncurrent_synthetic_receipt(
                scope=self.changed_scope("actor_id", "NONCURRENT_SYNTHETIC::world::wrong"),
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
            )
        with self.assertRaises(PermissionContractError):
            issue_noncurrent_synthetic_receipt(
                scope=self.changed_scope("actor_id", "NONCURRENT_SYNTHETIC::actor::   "),
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
            )

    def test_r4_17_classification_routing_occurrence_proximity_and_narrative_do_not_imply_permission(self):
        basis_ids = (
            "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
            "ADP-010",
            "ADP-019::OCCURRENCE_ADMITTED",
            "ROUTED_TO_SAME_ENDPOINT",
            "COLOCATED_SAME_TIME_AND_PLACE",
            "NARRATIVE_PLAUSIBILITY",
        )
        for basis_id in basis_ids:
            with self.subTest(basis_id=basis_id):
                receipt = issue_noncurrent_synthetic_receipt(
                    scope=REGISTERED_POSITIVE_SCOPE, basis_id=basis_id
                )
                self.addCleanup(receipt.close)
                self.assertEqual(
                    DECISION_DENY,
                    validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
                )

    def test_r4_18_wrong_fixture_and_empty_basis_fail_closed(self):
        with self.assertRaisesRegex(
            PermissionContractError, "project_current_or_unknown_fixture_not_authorized"
        ):
            issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
                fixture_class="PROJECT_CURRENT",
            )
        with self.assertRaisesRegex(PermissionContractError, "missing_basis_id"):
            issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id="   ",
            )

    def _tamper(self, field, value, expected_error, *, recompute_integrity=False):
        receipt = self.positive()
        body = json.loads(object.__getattribute__(receipt, "_body_json"))
        body[field] = value
        if recompute_integrity:
            body["receipt_digest"] = candidate.receipt_digest(body)
        object.__setattr__(receipt, "_body_json", candidate._canonical_json(body))
        with self.assertRaisesRegex(PermissionContractError, expected_error):
            validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_r4_19_authority_schema_fixture_and_decision_tampering_fail_closed(self):
        self._tamper("authority_id", "WRONG", "wrong_authority", recompute_integrity=True)
        self._tamper("schema_version", "WRONG", "wrong_schema", recompute_integrity=True)
        self._tamper(
            "fixture_class",
            "PROJECT_CURRENT",
            "project_current_or_unknown_fixture_not_authorized",
            recompute_integrity=True,
        )
        self._tamper("decision", "MAYBE", "invalid_decision", recompute_integrity=True)

    def test_r4_20_integrity_proof_and_basis_scope_tampering_fail_closed(self):
        self._tamper("receipt_digest", "0" * 64, "receipt_integrity_mismatch")
        self._tamper(
            "basis_proof_digest", "0" * 64, "source_basis_proof_mismatch", recompute_integrity=True
        )
        self._tamper(
            "basis_scope_digest", "0" * 64, "basis_scope_mismatch", recompute_integrity=True
        )

    def test_r4_21_caller_permission_boolean_and_basis_kind_inputs_remain_absent(self):
        parameters = inspect.signature(issue_noncurrent_synthetic_receipt).parameters
        self.assertNotIn("explicit_source_permission", parameters)
        self.assertNotIn("basis_kind", parameters)

    def test_r4_22_recovered_launcher_cannot_accept_caller_built_receipt_content(self):
        with self.assertRaises(TypeError):
            candidate._start_receipt_authority(
                object_id=123,
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
                fixture_class=FIXTURE_CLASS,
                body={"decision": DECISION_PERMIT},
            )

    def test_r4_23_no_project_current_effect_or_source_registration_surfaces_exist(self):
        names = set(candidate.__dict__)
        for name in (
            "execute_obl055",
            "install_obl056_positive",
            "create_encounter",
            "realize_oee",
            "create_actor",
            "activate_actor",
            "register_source_basis",
        ):
            self.assertNotIn(name, names)

    def test_r4_24_post_initialization_protocol_has_no_mutation_operations(self):
        receipt = self.denial("mutation-ops")
        write_fd = object.__getattribute__(receipt, "_write_fd")
        read_fd = object.__getattribute__(receipt, "_read_fd")
        body_json = object.__getattribute__(receipt, "_body_json")
        for operation in ("append", "replace", "rebind", "delete", "reinsert", "register", "mint"):
            with self.subTest(operation=operation):
                with self.assertRaisesRegex(PermissionContractError, "service_protocol_error"):
                    candidate._service_roundtrip(
                        write_fd,
                        read_fd,
                        {
                            "op": operation,
                            "object_id": id(receipt),
                            "body_json": body_json,
                            "expected_scope": REGISTERED_POSITIVE_SCOPE.canonical(),
                        },
                    )

    def test_r4_25_closed_authority_process_fails_closed(self):
        receipt = self.positive()
        receipt.close()
        self.assert_origin_rejected(receipt)


if __name__ == "__main__":
    unittest.main(verbosity=2)
