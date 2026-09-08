"""Producer governed bounded-repair court for frozen OBL058 R5 candidate.

Repair verification only. This court does not perform the later fresh distinct
independent review.
"""
from __future__ import annotations

import copy
import inspect
import json
import os
from pathlib import Path
import pickle
import signal
import subprocess
import sys
import threading
import unittest

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import causal_use_permission_candidate_r5 as candidate  # noqa: E402
from causal_use_permission_candidate_r5 import (  # noqa: E402
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


class CallerProxy(dict):
    pass


class OBL058BoundedRepairR5Court(unittest.TestCase):
    def positive(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(receipt.close)
        return receipt

    def denial(self, suffix: str = "r5-court-deny"):
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

    def assert_rejected(self, receipt, scope=REGISTERED_POSITIVE_SCOPE, pattern=None):
        if pattern is None:
            with self.assertRaises(PermissionContractError):
                validate_receipt(receipt, expected_scope=scope)
        else:
            with self.assertRaisesRegex(PermissionContractError, pattern):
                validate_receipt(receipt, expected_scope=scope)

    def raw_child(self):
        proc = subprocess.Popen(
            [sys.executable, "-S", str(Path(candidate.__file__).resolve()), "--receipt-authority-service-r5"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        def cleanup():
            candidate._terminate_proc(proc)
            for stream in (proc.stdin, proc.stdout, proc.stderr):
                if stream is not None:
                    try:
                        stream.close()
                    except Exception:
                        pass
        self.addCleanup(cleanup)
        return proc

    def send_raw_child(self, proc, request):
        self.assertIsNotNone(proc.stdin)
        self.assertIsNotNone(proc.stdout)
        proc.stdin.write(json.dumps(request, separators=(",", ":")) + "\n")
        proc.stdin.flush()
        line = proc.stdout.readline()
        self.assertTrue(line)
        return json.loads(line)

    def test_r5_01_valid_source_owned_positive_and_negative_controls(self):
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(self.positive(), expected_scope=REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(
            DECISION_DENY,
            validate_receipt(self.denial(), expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_r5_02_revision_identities_are_exact(self):
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.4.0", AUTHORITY_ID)
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_RECEIPT@5.0.0", SCHEMA_VERSION)
        receipt = self.positive()
        self.assertEqual(AUTHORITY_ID, receipt["authority_id"])
        self.assertEqual(SCHEMA_VERSION, receipt["schema_version"])
        self.assertTrue(receipt["authority_instance_id"])

    def test_r5_03_receipt_contains_no_parent_transport_or_process_slots(self):
        self.assertEqual(("_body_json",), IssuedReceipt.__slots__)
        receipt = self.positive()
        for name in ("_write_fd", "_read_fd", "_proc", "_socket", "_broker"):
            with self.subTest(name=name):
                self.assertFalse(hasattr(receipt, name))
                with self.assertRaises(AttributeError):
                    object.__setattr__(receipt, name, object())

    def test_r5_04_exact_type_fabrication_with_real_positive_body_is_rejected(self):
        positive = self.positive()
        fabricated = IssuedReceipt()
        object.__setattr__(
            fabricated, "_body_json", object.__getattribute__(positive, "_body_json")
        )
        self.assert_rejected(fabricated, pattern="receipt_not_issued_by_source_authority")

    def test_r5_05_source_denial_body_cannot_be_rebound_to_positive(self):
        denial = self.denial("body-rebind")
        positive = self.positive()
        original = object.__getattribute__(denial, "_body_json")
        object.__setattr__(denial, "_body_json", object.__getattribute__(positive, "_body_json"))
        try:
            self.assert_rejected(denial, pattern="receipt_not_issued_by_source_authority")
        finally:
            object.__setattr__(denial, "_body_json", original)
        self.assertEqual(DECISION_DENY, validate_receipt(denial, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_r5_06_cross_receipt_positive_body_reuse_is_rejected(self):
        first = self.positive()
        second = self.positive()
        second_original = object.__getattribute__(second, "_body_json")
        object.__setattr__(second, "_body_json", object.__getattribute__(first, "_body_json"))
        try:
            self.assert_rejected(second, pattern="receipt_not_issued_by_source_authority")
        finally:
            object.__setattr__(second, "_body_json", second_original)
        self.assertEqual(DECISION_PERMIT, validate_receipt(second, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_r5_07_parent_request_helper_substitution_does_not_change_validator(self):
        positive = self.positive()
        fabricated = IssuedReceipt()
        object.__setattr__(fabricated, "_body_json", object.__getattribute__(positive, "_body_json"))
        original = candidate._bound_broker_request
        candidate._bound_broker_request = lambda request: {
            "ok": True,
            "request_id": request.get("request_id"),
            "decision": DECISION_PERMIT,
            "authority_instance_id": positive["authority_instance_id"],
        }
        try:
            self.assert_rejected(fabricated)
            self.assertEqual(
                DECISION_PERMIT,
                validate_receipt(positive, expected_scope=REGISTERED_POSITIVE_SCOPE),
            )
        finally:
            candidate._bound_broker_request = original

    def test_r5_08_validator_is_no_closure_no_defaults_and_bound_to_one_broker(self):
        self.assertIsNone(validate_receipt.__closure__)
        self.assertIsNone(validate_receipt.__defaults__)
        self.assertIsNone(validate_receipt.__kwdefaults__)
        self.assertEqual((), validate_receipt.__code__.co_freevars)
        constants = validate_receipt.__code__.co_consts
        self.assertTrue(any(isinstance(v, str) and v.endswith("/authority.sock") for v in constants))
        self.assertNotIn("_broker_proc", candidate.__dict__)
        self.assertNotIn("_broker_socket_path", candidate.__dict__)
        self.assertFalse(any(isinstance(v, subprocess.Popen) for v in candidate.__dict__.values()))

    def test_r5_09_broker_issue_protocol_rejects_caller_built_body_field(self):
        request_id = "r5-extra-body-field"
        with self.assertRaisesRegex(PermissionContractError, "broker_protocol_error"):
            candidate._bound_broker_request({
                "op": "issue",
                "object_id": 987654321,
                "scope": REGISTERED_POSITIVE_SCOPE.canonical(),
                "basis_id": REGISTERED_POSITIVE_BASIS_ID,
                "fixture_class": FIXTURE_CLASS,
                "body_json": "{}",
                "request_id": request_id,
            })

    def test_r5_10_duplicate_broker_issue_for_existing_identity_is_rejected(self):
        receipt = self.positive()
        with self.assertRaisesRegex(PermissionContractError, "object_identity_already_issued"):
            candidate._bound_broker_request({
                "op": "issue",
                "object_id": id(receipt),
                "scope": REGISTERED_POSITIVE_SCOPE.canonical(),
                "basis_id": REGISTERED_POSITIVE_BASIS_ID,
                "fixture_class": FIXTURE_CLASS,
                "request_id": "duplicate-r5-identity",
            })

    def test_r5_11_broker_protocol_has_no_post_issue_mutation_operations(self):
        receipt = self.denial("mutation-ops")
        for operation in ("append", "replace", "rebind", "delete", "reinsert", "register", "mint"):
            with self.subTest(operation=operation):
                with self.assertRaisesRegex(PermissionContractError, "broker_protocol_error"):
                    candidate._bound_broker_request({
                        "op": operation,
                        "object_id": id(receipt),
                        "body_json": object.__getattribute__(receipt, "_body_json"),
                        "request_id": f"operation-{operation}",
                    })

    def test_r5_12_one_shot_child_rejects_caller_body_initialization(self):
        proc = self.raw_child()
        response = self.send_raw_child(proc, {
            "op": "initialize",
            "object_id": 111,
            "scope": REGISTERED_POSITIVE_SCOPE.canonical(),
            "basis_id": REGISTERED_POSITIVE_BASIS_ID,
            "fixture_class": FIXTURE_CLASS,
            "request_id": "child-extra-body",
            "body_json": "{}",
        })
        self.assertFalse(response["ok"])
        self.assertEqual("service_protocol_error", response["error"])

    def test_r5_13_one_shot_child_rejects_validate_before_initialize(self):
        proc = self.raw_child()
        response = self.send_raw_child(proc, {
            "op": "validate",
            "object_id": 111,
            "body_json": "{}",
            "expected_scope": REGISTERED_POSITIVE_SCOPE.canonical(),
            "request_id": "before-init",
        })
        self.assertFalse(response["ok"])
        self.assertEqual("service_protocol_error", response["error"])

    def test_r5_14_one_shot_child_rejects_duplicate_initialization(self):
        proc = self.raw_child()
        first = self.send_raw_child(proc, {
            "op": "initialize",
            "object_id": 222,
            "scope": REGISTERED_POSITIVE_SCOPE.canonical(),
            "basis_id": REGISTERED_POSITIVE_BASIS_ID,
            "fixture_class": FIXTURE_CLASS,
            "request_id": "init-one",
        })
        self.assertTrue(first["ok"])
        second = self.send_raw_child(proc, {
            "op": "initialize",
            "object_id": 222,
            "scope": REGISTERED_POSITIVE_SCOPE.canonical(),
            "basis_id": REGISTERED_POSITIVE_BASIS_ID,
            "fixture_class": FIXTURE_CLASS,
            "request_id": "init-two",
        })
        self.assertFalse(second["ok"])
        self.assertEqual("service_protocol_error", second["error"])

    def test_r5_15_closed_source_authority_cannot_validate_stale_receipt(self):
        receipt = self.positive()
        receipt.close()
        self.assert_rejected(receipt)

    def test_r5_16_repeated_validation_is_stable(self):
        positive = self.positive()
        denial = self.denial("repeat")
        for _ in range(6):
            self.assertEqual(DECISION_PERMIT, validate_receipt(positive, expected_scope=REGISTERED_POSITIVE_SCOPE))
            self.assertEqual(DECISION_DENY, validate_receipt(denial, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_r5_17_concurrent_validation_does_not_cross_responses(self):
        positive = self.positive()
        denial = self.denial("concurrent")
        results = []
        errors = []
        lock = threading.Lock()

        def work(receipt, expected):
            try:
                value = validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)
                with lock:
                    results.append((expected, value))
            except Exception as exc:
                with lock:
                    errors.append(exc)

        threads = []
        for _ in range(5):
            threads.append(threading.Thread(target=work, args=(positive, DECISION_PERMIT)))
            threads.append(threading.Thread(target=work, args=(denial, DECISION_DENY)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10)
        self.assertFalse(errors)
        self.assertEqual(10, len(results))
        self.assertTrue(all(expected == actual for expected, actual in results))

    def test_r5_18_exact_type_constructor_object_new_subclass_mapping_proxy_rejected(self):
        positive = self.positive()
        self.assert_rejected(IssuedReceipt())
        raw = object.__new__(IssuedReceipt)
        self.assert_rejected(raw)

        class CallerReceipt(IssuedReceipt):
            pass

        self.assert_rejected(CallerReceipt())
        self.assert_rejected(dict(positive))
        self.assert_rejected(CallerProxy(dict(positive)))

    def test_r5_19_copy_deepcopy_pickle_and_json_reconstruction_are_rejected(self):
        receipt = self.positive()
        for operation in (
            lambda: copy.copy(receipt),
            lambda: copy.deepcopy(receipt),
            lambda: pickle.dumps(receipt),
        ):
            with self.assertRaises(TypeError):
                operation()
        reconstructed = json.loads(json.dumps(dict(receipt)))
        self.assert_rejected(reconstructed)

    def test_r5_20_public_scope_copy_mutation_does_not_change_authoritative_body(self):
        receipt = self.positive()
        visible = receipt["scope"]
        visible["actor_id"] = "NONCURRENT_SYNTHETIC::actor::changed-copy"
        self.assertEqual(DECISION_PERMIT, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_r5_21_registered_basis_is_exactly_bound_across_all_five_scope_fields(self):
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

    def test_r5_22_cross_scope_replay_is_rejected_for_every_scope_field(self):
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
                self.assert_rejected(
                    receipt,
                    scope=self.changed_scope(field, replacement),
                    pattern="scope_mismatch_or_stale",
                )

    def test_r5_23_project_current_namespaces_and_first_canary_are_rejected(self):
        replacements = {
            "actor_id": "urn:rawlsing:v3:actor:project-current:a",
            "world_id": "urn:rawlsing:v3:world:project-current:w",
            "subject_id": "urn:rawlsing:v3:subject:project-current:s",
            "time_id": "urn:rawlsing:v3:time:project-current:t",
            "transition_id": "urn:rawlsing:v3:transition:project-current:tr",
        }
        for field, replacement in replacements.items():
            with self.subTest(field=field):
                with self.assertRaisesRegex(PermissionContractError, "noncurrent_synthetic_scope_required"):
                    issue_noncurrent_synthetic_receipt(
                        scope=self.changed_scope(field, replacement),
                        basis_id=REGISTERED_POSITIVE_BASIS_ID,
                    )
        with self.assertRaisesRegex(PermissionContractError, "noncurrent_synthetic_scope_required:subject_id"):
            issue_noncurrent_synthetic_receipt(
                scope=self.changed_scope("subject_id", CURRENT_FIRST_CANARY_SUBJECT),
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
            )

    def test_r5_24_wrong_field_namespace_empty_suffix_fixture_and_basis_fail_closed(self):
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
        with self.assertRaisesRegex(PermissionContractError, "project_current_or_unknown_fixture_not_authorized"):
            issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
                fixture_class="PROJECT_CURRENT",
            )
        with self.assertRaisesRegex(PermissionContractError, "missing_basis_id"):
            issue_noncurrent_synthetic_receipt(scope=REGISTERED_POSITIVE_SCOPE, basis_id="  ")

    def test_r5_25_inference_like_basis_ids_remain_denials(self):
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
                self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def _tamper(self, field, value, pattern, recompute_integrity=False):
        receipt = self.positive()
        body = json.loads(object.__getattribute__(receipt, "_body_json"))
        body[field] = value
        if recompute_integrity:
            body["receipt_digest"] = receipt_digest(body)
        object.__setattr__(receipt, "_body_json", candidate._canonical_json(body))
        self.assert_rejected(receipt, pattern=pattern)

    def test_r5_26_authority_schema_fixture_decision_and_instance_tampering_fail_closed(self):
        self._tamper("authority_id", "WRONG", "wrong_authority", True)
        self._tamper("schema_version", "WRONG", "wrong_schema", True)
        self._tamper("fixture_class", "PROJECT_CURRENT", "project_current_or_unknown_fixture_not_authorized", True)
        self._tamper("decision", "MAYBE", "invalid_decision", True)
        self._tamper("authority_instance_id", "other-instance", "receipt_not_issued_by_source_authority", True)

    def test_r5_27_integrity_basis_proof_and_basis_scope_tampering_fail_closed(self):
        self._tamper("receipt_digest", "0" * 64, "receipt_integrity_mismatch")
        self._tamper("basis_proof_digest", "0" * 64, "source_basis_proof_mismatch", True)
        self._tamper("basis_scope_digest", "0" * 64, "basis_scope_mismatch", True)

    def test_r5_28_caller_permission_boolean_basis_kind_and_source_registration_surfaces_absent(self):
        parameters = inspect.signature(issue_noncurrent_synthetic_receipt).parameters
        self.assertNotIn("explicit_source_permission", parameters)
        self.assertNotIn("basis_kind", parameters)
        names = set(candidate.__dict__)
        for name in (
            "register_source_basis",
            "install_obl056_positive",
            "execute_obl055",
            "create_encounter",
            "realize_oee",
            "create_actor",
            "activate_actor",
        ):
            self.assertNotIn(name, names)

    def test_r5_29_broker_peer_binding_rejects_replacement_server_in_isolated_process(self):
        script = r"""
import json, os, socket, sys, threading
sys.path.insert(0, __BASE__)
import causal_use_permission_candidate_r5 as c
real = c.issue_noncurrent_synthetic_receipt(
    scope=c.REGISTERED_POSITIVE_SCOPE,
    basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
)
consts = c.validate_receipt.__code__.co_consts
path = next(x for x in consts if isinstance(x, str) and x.endswith("/authority.sock"))
os.unlink(path)
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(path)
server.listen(2)
def respond():
    conn, _ = server.accept()
    with conn:
        conn.recv(65536)
        conn.sendall(b'{"ok":true,"request_id":"wrong","decision":"PERMIT","authority_instance_id":"x"}\n')
threading.Thread(target=respond, daemon=True).start()
fabricated = c.IssuedReceipt()
object.__setattr__(fabricated, "_body_json", object.__getattribute__(real, "_body_json"))
try:
    c.validate_receipt(fabricated, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
except c.PermissionContractError:
    print("REJECTED")
else:
    print("ACCEPTED")
server.close()
""".replace("__BASE__", repr(str(HERE)))
        completed = subprocess.run(
            [sys.executable, "-S", "-c", script],
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("REJECTED", completed.stdout)
        self.assertNotIn("ACCEPTED", completed.stdout)

    def test_r5_30_broker_request_ids_and_instance_ids_are_exactly_echoed(self):
        receipt = self.positive()
        body = json.loads(object.__getattribute__(receipt, "_body_json"))
        request_id = "direct-validation-request"
        response = candidate._bound_broker_request({
            "op": "validate",
            "object_id": id(receipt),
            "body_json": object.__getattribute__(receipt, "_body_json"),
            "expected_scope": REGISTERED_POSITIVE_SCOPE.canonical(),
            "request_id": request_id,
        })
        self.assertEqual(request_id, response["request_id"])
        self.assertEqual(body["authority_instance_id"], response["authority_instance_id"])
        self.assertEqual(DECISION_PERMIT, response["decision"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
