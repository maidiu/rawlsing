"""Producer governed verification for frozen OBL058 R7 mechanism repair.

This court checks the R6 object-generation retirement finding directly while
preserving the already-reviewed R6 process-generation and semantic controls.
It is producer-side verification only, not independent review.
"""
from __future__ import annotations

import copy
from concurrent.futures import ThreadPoolExecutor
import gc
import inspect
import json
import os
from pathlib import Path
import pickle
import sys
import unittest
import weakref

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import causal_use_permission_candidate_r7 as candidate  # noqa: E402
from causal_use_permission_candidate_r7 import (  # noqa: E402
    AUTHORITY_ID,
    DECISION_DENY,
    DECISION_PERMIT,
    FIXTURE_CLASS,
    MECHANISM_REVISION,
    REGISTERED_POSITIVE_BASIS_ID,
    REGISTERED_POSITIVE_SCOPE,
    SCHEMA_VERSION,
    ExactScope,
    IssuedReceipt,
    PermissionContractError,
    issue_noncurrent_synthetic_receipt,
    native_lifetime_reservation_count,
    native_successful_close_count,
    validate_receipt,
)

CURRENT_FIRST_CANARY_SUBJECT = (
    "urn:rawlsing:v3:subject:sha256:"
    "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
)


class CallerProxy(dict):
    pass


class OBL058BoundedRepairR7Court(unittest.TestCase):
    def positive(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(receipt.close)
        return receipt

    def denial(self, suffix="r7-unregistered"):
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
        with self.assertRaises(PermissionContractError):
            validate_receipt(receipt, expected_scope=scope)

    def test_r7_01_valid_source_owned_positive_and_negative_controls(self):
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(self.positive(), expected_scope=REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(
            DECISION_DENY,
            validate_receipt(self.denial(), expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_r7_02_authority_schema_and_mechanism_revision_are_exact(self):
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0", AUTHORITY_ID)
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0", SCHEMA_VERSION)
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_OBJECT_GENERATION_MECHANISM_R7@1.0.0", MECHANISM_REVISION)

    def test_r7_03_no_python_weakref_or_finalize_registration_can_control_lifetime(self):
        receipt = self.positive()
        with self.assertRaises(TypeError):
            weakref.ref(receipt)
        with self.assertRaises(TypeError):
            weakref.finalize(receipt, lambda: None)
        source = inspect.getsource(candidate.issue_noncurrent_synthetic_receipt)
        self.assertNotIn("weakref", source)
        self.assertNotIn("finalize", source)

    def test_r7_04_native_source_reservation_survives_caller_reference_release(self):
        before = native_lifetime_reservation_count()
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        self.assertEqual(before + 1, native_lifetime_reservation_count())
        del receipt
        gc.collect()
        self.assertEqual(before + 1, native_lifetime_reservation_count())

    def test_r7_05_native_reservation_is_not_a_python_container_referrer(self):
        receipt = self.positive()
        referrers = gc.get_referrers(receipt)
        self.assertFalse(any(type(value) in {list, dict, set} for value in referrers))

    def test_r7_06_explicit_close_retires_authority_and_releases_native_reservation(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        before_pins = native_lifetime_reservation_count()
        before_closes = native_successful_close_count()
        self.assertEqual(DECISION_PERMIT, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))
        self.assertTrue(receipt.close())
        self.assertEqual(before_pins - 1, native_lifetime_reservation_count())
        self.assertEqual(before_closes + 1, native_successful_close_count())
        self.assert_origin_rejected(receipt)
        self.assertFalse(receipt.close())

    def test_r7_07_native_broker_binding_is_one_time(self):
        with self.assertRaises(RuntimeError):
            candidate._native.bind_broker(lambda request: {"decision": DECISION_PERMIT})

    def test_r7_08_native_generation_key_is_not_a_python_attribute(self):
        receipt = self.positive()
        self.assertFalse(hasattr(receipt, "authority_key"))
        self.assertFalse(hasattr(receipt, "_authority_key"))
        self.assertFalse(hasattr(receipt, "__dict__"))
        with self.assertRaises(AttributeError):
            object.__setattr__(receipt, "authority_key", 1)
        with self.assertRaises(AttributeError):
            object.__setattr__(receipt, "_body_json", "caller-selected")

    def test_r7_09_direct_constructor_and_object_new_are_unissued(self):
        self.assert_origin_rejected(IssuedReceipt())
        self.assert_origin_rejected(object.__new__(IssuedReceipt))

    def test_r7_10_second_source_issue_on_same_generation_is_rejected(self):
        receipt = self.positive()
        with self.assertRaises((PermissionContractError, ValueError)):
            receipt._source_issue(
                REGISTERED_POSITIVE_SCOPE.canonical(),
                REGISTERED_POSITIVE_BASIS_ID,
                FIXTURE_CLASS,
            )

    def test_r7_11_subclass_mapping_proxy_json_copy_and_serialization_are_rejected(self):
        receipt = self.positive()
        base = type(receipt)

        class CallerReceipt(base):
            pass

        self.assert_origin_rejected(CallerReceipt())
        self.assert_origin_rejected(dict(receipt))
        self.assert_origin_rejected(CallerProxy(dict(receipt)))
        self.assert_origin_rejected(json.loads(json.dumps(dict(receipt))))
        for operation in (
            lambda: copy.copy(receipt),
            lambda: copy.deepcopy(receipt),
            lambda: pickle.dumps(receipt),
        ):
            with self.assertRaises(TypeError):
                operation()

    def test_r7_12_public_body_cannot_be_rebound_between_receipts(self):
        first = self.positive()
        second = self.positive()
        self.assertNotEqual(first["authority_instance_id"], second["authority_instance_id"])
        with self.assertRaises(AttributeError):
            object.__setattr__(first, "_body_json", second._body_json_copy())
        self.assertEqual(DECISION_PERMIT, validate_receipt(first, expected_scope=REGISTERED_POSITIVE_SCOPE))
        self.assertEqual(DECISION_PERMIT, validate_receipt(second, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def _fork_result(self, receipt, *, do_close=False) -> str:
        if not hasattr(os, "fork"):
            self.skipTest("fork unavailable")
        read_fd, write_fd = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(read_fd)
            try:
                if do_close:
                    result = "CLOSED" if receipt.close() else "REJECTED"
                else:
                    validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)
                    result = "ACCEPTED"
            except Exception:
                result = "REJECTED"
            os.write(write_fd, result.encode("ascii"))
            os.close(write_fd)
            os._exit(0)
        os.close(write_fd)
        result = os.read(read_fd, 64).decode("ascii")
        os.close(read_fd)
        os.waitpid(pid, 0)
        return result

    def test_r7_13_forked_positive_and_negative_copies_are_rejected(self):
        for label, receipt in (("permit", self.positive()), ("deny", self.denial("fork"))):
            with self.subTest(label=label):
                self.assertEqual("REJECTED", self._fork_result(receipt))

    def test_r7_14_forked_close_cannot_retire_parent_authority(self):
        receipt = self.positive()
        self.assertEqual("REJECTED", self._fork_result(receipt, do_close=True))
        self.assertEqual(DECISION_PERMIT, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_r7_15_registered_basis_is_exactly_bound_across_all_five_fields(self):
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

    def test_r7_16_cross_scope_replay_is_rejected_for_all_fields(self):
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
                with self.assertRaises(PermissionContractError):
                    validate_receipt(receipt, expected_scope=self.changed_scope(field, replacement))

    def test_r7_17_project_current_shaped_namespaces_fail_closed(self):
        replacements = {
            "actor_id": "urn:rawlsing:v3:actor:project-current:a",
            "world_id": "urn:rawlsing:v3:world:project-current:w",
            "subject_id": "urn:rawlsing:v3:subject:project-current:s",
            "time_id": "urn:rawlsing:v3:time:project-current:t",
            "transition_id": "urn:rawlsing:v3:transition:project-current:tr",
        }
        for field, replacement in replacements.items():
            with self.subTest(field=field):
                with self.assertRaises(PermissionContractError):
                    issue_noncurrent_synthetic_receipt(
                        scope=self.changed_scope(field, replacement),
                        basis_id=REGISTERED_POSITIVE_BASIS_ID,
                    )

    def test_r7_18_exact_current_first_canary_subject_is_rejected(self):
        with self.assertRaises(PermissionContractError):
            issue_noncurrent_synthetic_receipt(
                scope=self.changed_scope("subject_id", CURRENT_FIRST_CANARY_SUBJECT),
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
            )

    def test_r7_19_wrong_fixture_and_empty_basis_fail_closed(self):
        with self.assertRaises(PermissionContractError):
            issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
                fixture_class="PROJECT_CURRENT",
            )
        with self.assertRaises(PermissionContractError):
            issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id="   ",
            )

    def test_r7_20_surrogate_basis_strings_do_not_imply_permission(self):
        values = (
            "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
            "ADP-010",
            "ADP-019::OCCURRENCE_ADMITTED",
            "ROUTED_TO_SAME_ENDPOINT",
            "COLOCATED_SAME_TIME_AND_PLACE",
            "NARRATIVE_PLAUSIBILITY",
        )
        for basis_id in values:
            with self.subTest(basis_id=basis_id):
                receipt = issue_noncurrent_synthetic_receipt(
                    scope=REGISTERED_POSITIVE_SCOPE, basis_id=basis_id
                )
                self.addCleanup(receipt.close)
                self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_r7_21_same_process_repeated_and_concurrent_validation_is_stable(self):
        receipt = self.positive()
        for _ in range(5):
            self.assertEqual(DECISION_PERMIT, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(
                lambda _: validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
                range(8),
            ))
        self.assertEqual([DECISION_PERMIT] * 8, results)

    def test_r7_22_caller_permission_and_basis_kind_inputs_remain_absent(self):
        parameters = inspect.signature(issue_noncurrent_synthetic_receipt).parameters
        self.assertNotIn("explicit_source_permission", parameters)
        self.assertNotIn("basis_kind", parameters)

    def test_r7_23_native_source_uses_raw_c_pin_not_python_finalizer_registry(self):
        source = Path(candidate.__file__).with_name("obl058_r7_native.c").read_text(encoding="utf-8")
        self.assertIn("PinNode", source)
        self.assertIn("PyMem_Malloc", source)
        self.assertNotIn("weakref", source.lower())
        self.assertNotIn("PyList_Append", source)

    def test_r7_24_no_project_current_effect_or_registration_surfaces_exist(self):
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
