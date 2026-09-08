"""Fresh distinct independent review for frozen OBL058 R4 candidate.

Blocking tests intentionally assert the independently discovered caller-response
substitution path. A green governed court means the observed behavior is
reproducible; semantic PASS/FAIL is recorded separately by the reviewer.
"""
from __future__ import annotations

from collections.abc import Mapping
import copy
import inspect
import json
import os
from pathlib import Path
import pickle
import subprocess
import sys
import threading
import unittest

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import causal_use_permission_candidate_r4 as candidate  # noqa: E402
from causal_use_permission_candidate_r4 import (  # noqa: E402
    AUTHORITY_ID,
    DECISION_DENY,
    DECISION_PERMIT,
    FIXTURE_CLASS,
    REGISTERED_POSITIVE_BASIS_ID,
    REGISTERED_POSITIVE_SCOPE,
    SCHEMA_VERSION,
    ExactScope,
    IssuedReceipt,
    PermissionContractError,
    issue_noncurrent_synthetic_receipt,
    receipt_digest,
    validate_receipt,
)

CURRENT_FIRST_CANARY_SUBJECT = (
    "urn:rawlsing:v3:subject:sha256:"
    "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
)


def _close_fd(fd: int) -> None:
    try:
        os.close(fd)
    except OSError:
        pass


class CallerProxy(Mapping):
    def __init__(self, body):
        self.body = body

    def __getitem__(self, key):
        return self.body[key]

    def __iter__(self):
        return iter(self.body)

    def __len__(self):
        return len(self.body)


class OBL058R4IndependentReview(unittest.TestCase):
    def positive(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(receipt.close)
        return receipt

    def denial(self, suffix="r4-review-deny"):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=f"NONCURRENT_SYNTHETIC::basis::{suffix}",
        )
        self.addCleanup(receipt.close)
        return receipt

    def assert_origin_rejected(self, receipt, expected_scope=REGISTERED_POSITIVE_SCOPE):
        with self.assertRaises(PermissionContractError):
            validate_receipt(receipt, expected_scope=expected_scope)

    def install_caller_response_transport(self, receipt, response):
        """Rebind parent-visible transport to a caller-controlled responder."""
        request_r, request_w = os.pipe()
        response_r, response_w = os.pipe()
        proc = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(60)"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        def responder():
            try:
                buffered = b""
                while True:
                    chunk = os.read(request_r, 4096)
                    if not chunk:
                        return
                    buffered += chunk
                    while b"\n" in buffered:
                        _line, buffered = buffered.split(b"\n", 1)
                        payload = (json.dumps(response, separators=(",", ":")) + "\n").encode("utf-8")
                        os.write(response_w, payload)
            except OSError:
                return
            finally:
                _close_fd(request_r)
                _close_fd(response_w)

        thread = threading.Thread(target=responder, daemon=True)
        thread.start()

        object.__setattr__(receipt, "_write_fd", request_w)
        object.__setattr__(receipt, "_read_fd", response_r)
        object.__setattr__(receipt, "_proc", proc)

        def cleanup():
            _close_fd(request_w)
            _close_fd(response_r)
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=2)

        self.addCleanup(cleanup)
        return proc

    def spawn_raw_authority(self):
        proc = subprocess.Popen(
            [sys.executable, str(Path(candidate.__file__).resolve()), "--receipt-authority-service"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self.addCleanup(lambda: candidate._terminate_proc(proc))
        return proc

    def send_raw(self, proc, request):
        self.assertIsNotNone(proc.stdin)
        self.assertIsNotNone(proc.stdout)
        proc.stdin.write(json.dumps(request, separators=(",", ":")) + "\n")
        proc.stdin.flush()
        line = proc.stdout.readline()
        self.assertTrue(line)
        return json.loads(line)

    # Blocking family: validator trusts caller-rebindable transport and response.

    def test_b01_exact_type_fabrication_with_caller_response_validates_permit(self):
        fabricated = IssuedReceipt()
        object.__setattr__(fabricated, "_body_json", "caller-visible-nonauthoritative-body")
        self.install_caller_response_transport(
            fabricated, {"ok": True, "decision": DECISION_PERMIT}
        )
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(fabricated, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_b02_existing_denial_can_be_rebound_to_caller_permit_response(self):
        receipt = self.denial("response-substitution")
        self.assertEqual(
            DECISION_DENY,
            validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )
        receipt.close()
        self.install_caller_response_transport(
            receipt, {"ok": True, "decision": DECISION_PERMIT}
        )
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_b03_transport_and_process_slots_are_parent_rebindable(self):
        receipt = self.positive()
        for slot in ("_body_json", "_write_fd", "_read_fd", "_proc"):
            self.assertIn(slot, IssuedReceipt.__slots__)
            self.assertIsNotNone(object.__getattribute__(receipt, slot))
        self.assertTrue(callable(candidate._service_roundtrip))
        self.assertTrue(callable(candidate._start_receipt_authority))

    def test_b04_validator_only_checks_running_popen_not_fd_process_binding(self):
        source = inspect.getsource(candidate.validate_receipt)
        self.assertIn("isinstance(proc, subprocess.Popen)", source)
        self.assertNotIn("proc.stdin.fileno()", source)
        self.assertNotIn("proc.stdout.fileno()", source)

    # Initialization/protocol controls: the child itself is one-shot and body-safe.

    def test_p01_initialize_rejects_caller_supplied_body_field(self):
        proc = self.spawn_raw_authority()
        response = self.send_raw(proc, {
            "op": "initialize",
            "object_id": 12345,
            "scope": REGISTERED_POSITIVE_SCOPE.canonical(),
            "basis_id": REGISTERED_POSITIVE_BASIS_ID,
            "fixture_class": FIXTURE_CLASS,
            "body_json": "caller-selected",
        })
        self.assertFalse(response["ok"])
        self.assertEqual("service_protocol_error", response["error"])

    def test_p02_validate_before_initialize_is_rejected(self):
        proc = self.spawn_raw_authority()
        response = self.send_raw(proc, {
            "op": "validate",
            "object_id": 12345,
            "body_json": "x",
            "expected_scope": REGISTERED_POSITIVE_SCOPE.canonical(),
        })
        self.assertFalse(response["ok"])
        self.assertEqual("service_protocol_error", response["error"])

    def test_p03_duplicate_initialize_cannot_reinitialize_child(self):
        proc = self.spawn_raw_authority()
        first = self.send_raw(proc, {
            "op": "initialize",
            "object_id": 12345,
            "scope": REGISTERED_POSITIVE_SCOPE.canonical(),
            "basis_id": REGISTERED_POSITIVE_BASIS_ID,
            "fixture_class": FIXTURE_CLASS,
        })
        self.assertTrue(first["ok"])
        second = self.send_raw(proc, {
            "op": "initialize",
            "object_id": 54321,
            "scope": REGISTERED_POSITIVE_SCOPE.canonical(),
            "basis_id": REGISTERED_POSITIVE_BASIS_ID,
            "fixture_class": FIXTURE_CLASS,
        })
        self.assertFalse(second["ok"])
        self.assertEqual("service_protocol_error", second["error"])

    def test_p04_launcher_has_no_caller_body_parameter(self):
        params = tuple(inspect.signature(candidate._start_receipt_authority).parameters)
        self.assertEqual(("object_id", "scope", "basis_id", "fixture_class"), params)

    # Identity/body preservation controls with the real authority child.

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

    def test_c03_plain_copy_proxy_exact_type_and_object_new_are_rejected(self):
        receipt = self.positive()
        self.assert_origin_rejected(dict(receipt))
        self.assert_origin_rejected(CallerProxy(dict(receipt)))
        self.assert_origin_rejected(IssuedReceipt())
        self.assert_origin_rejected(object.__new__(IssuedReceipt))

    def test_c04_copy_deepcopy_and_pickle_do_not_create_accepted_identity(self):
        receipt = self.positive()
        for operation in (copy.copy, copy.deepcopy):
            with self.assertRaises(TypeError):
                operation(receipt)
        with self.assertRaises(TypeError):
            pickle.dumps(receipt)

    def test_c05_subclass_is_rejected(self):
        class CallerReceipt(IssuedReceipt):
            __slots__ = ()
        self.assert_origin_rejected(CallerReceipt())

    def test_c06_parent_body_mutation_does_not_change_real_child_authority(self):
        receipt = self.positive()
        original = object.__getattribute__(receipt, "_body_json")
        body = json.loads(original)
        body["decision"] = DECISION_DENY
        body["receipt_digest"] = receipt_digest(body)
        object.__setattr__(receipt, "_body_json", json.dumps(body, sort_keys=True, separators=(",", ":")))
        self.assert_origin_rejected(receipt)

    def test_c07_cross_receipt_body_and_handle_substitution_fails_with_real_children(self):
        positive = self.positive()
        denial = self.denial("cross-receipt")
        denial_body = object.__getattribute__(denial, "_body_json")
        object.__setattr__(positive, "_body_json", denial_body)
        self.assert_origin_rejected(positive)

    def test_c08_repeated_real_validation_is_stable(self):
        receipt = self.positive()
        for _ in range(5):
            self.assertEqual(
                DECISION_PERMIT,
                validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
            )

    def test_c09_terminated_child_fails_closed(self):
        receipt = self.positive()
        receipt.close()
        self.assert_origin_rejected(receipt)

    def test_c10_malformed_caller_response_fails_closed(self):
        fabricated = IssuedReceipt()
        object.__setattr__(fabricated, "_body_json", "x")
        self.install_caller_response_transport(fabricated, {"ok": True, "decision": "MAYBE"})
        self.assert_origin_rejected(fabricated)

    # Scope, namespace, fixture, proof and inference preservation.

    def test_s01_registered_basis_wrong_each_scope_field_denies(self):
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
                self.addCleanup(receipt.close)
                self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=scope))

    def test_s02_cross_scope_replay_rejected_for_each_field(self):
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
                self.assert_origin_rejected(receipt, ExactScope(**values))

    def test_s03_wrong_field_namespace_and_empty_suffix_rejected(self):
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
                with self.assertRaises(PermissionContractError):
                    issue_noncurrent_synthetic_receipt(
                        scope=ExactScope(**values), basis_id=REGISTERED_POSITIVE_BASIS_ID
                    )
        values = REGISTERED_POSITIVE_SCOPE.canonical()
        values["actor_id"] = "NONCURRENT_SYNTHETIC::actor::   "
        with self.assertRaises(PermissionContractError):
            issue_noncurrent_synthetic_receipt(
                scope=ExactScope(**values), basis_id=REGISTERED_POSITIVE_BASIS_ID
            )

    def test_s04_current_first_canary_and_current_shaped_ids_rejected(self):
        values = REGISTERED_POSITIVE_SCOPE.canonical()
        values["subject_id"] = CURRENT_FIRST_CANARY_SUBJECT
        with self.assertRaises(PermissionContractError):
            issue_noncurrent_synthetic_receipt(
                scope=ExactScope(**values), basis_id=REGISTERED_POSITIVE_BASIS_ID
            )
        values = REGISTERED_POSITIVE_SCOPE.canonical()
        values["world_id"] = "urn:rawlsing:v3:world:project-current:w"
        with self.assertRaises(PermissionContractError):
            issue_noncurrent_synthetic_receipt(
                scope=ExactScope(**values), basis_id=REGISTERED_POSITIVE_BASIS_ID
            )

    def test_s05_project_current_fixture_rejected(self):
        with self.assertRaises(PermissionContractError):
            issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
                fixture_class="PROJECT_CURRENT",
            )

    def test_s06_inference_like_basis_ids_all_deny(self):
        for basis_id in (
            "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
            "ADP-010",
            "ADP-019::OCCURRENCE_ADMITTED",
            "ROUTED_TO_SAME_ENDPOINT",
            "COLOCATED_SAME_TIME_AND_PLACE",
            "NARRATIVE_PLAUSIBILITY",
        ):
            with self.subTest(basis_id=basis_id):
                receipt = issue_noncurrent_synthetic_receipt(
                    scope=REGISTERED_POSITIVE_SCOPE, basis_id=basis_id
                )
                self.addCleanup(receipt.close)
                self.assertEqual(
                    DECISION_DENY,
                    validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
                )

    def test_s07_authority_schema_fixture_scope_proof_and_integrity_mutations_fail(self):
        mutations = (
            ("authority_id", "WRONG"),
            ("schema_version", "WRONG"),
            ("fixture_class", "PROJECT_CURRENT"),
            ("scope_digest", "0" * 64),
            ("basis_scope_digest", "1" * 64),
            ("basis_proof_digest", "2" * 64),
            ("receipt_digest", "3" * 64),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                receipt = self.positive()
                body = json.loads(object.__getattribute__(receipt, "_body_json"))
                body[field] = value
                if field != "receipt_digest":
                    body["receipt_digest"] = receipt_digest(body)
                object.__setattr__(
                    receipt, "_body_json", json.dumps(body, sort_keys=True, separators=(",", ":"))
                )
                self.assert_origin_rejected(receipt)

    def test_s08_no_public_registration_or_current_effect_api(self):
        exported = set(dir(candidate))
        self.assertFalse(any("register" in name.lower() for name in exported))
        forbidden = {
            "execute_obl055", "create_encounter", "realize_oee",
            "install_current_positive_obl056", "unblock_obl061",
            "activate_current_actor", "create_current_actor",
        }
        self.assertTrue(forbidden.isdisjoint(exported))


if __name__ == "__main__":
    unittest.main()
