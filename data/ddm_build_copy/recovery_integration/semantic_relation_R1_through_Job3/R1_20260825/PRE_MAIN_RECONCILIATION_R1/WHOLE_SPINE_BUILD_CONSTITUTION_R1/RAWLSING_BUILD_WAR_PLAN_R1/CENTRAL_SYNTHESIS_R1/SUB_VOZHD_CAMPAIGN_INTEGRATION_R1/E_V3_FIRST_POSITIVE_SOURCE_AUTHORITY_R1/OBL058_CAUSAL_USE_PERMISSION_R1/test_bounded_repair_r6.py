"""Producer bounded-repair court for OBL058 R6.

This verifies the requester/object-generation repair and preservation controls.
It is producer-side verification only, not the later fresh independent review.
"""
from __future__ import annotations

import copy
import gc
import inspect
import json
import os
import pickle
import signal
import threading
import time
import unittest
import weakref

import causal_use_permission_candidate_r6 as candidate
from causal_use_permission_candidate_r6 import (
    AUTHORITY_ID,
    SCHEMA_VERSION,
    DECISION_DENY,
    DECISION_PERMIT,
    FIXTURE_CLASS,
    REGISTERED_POSITIVE_BASIS_ID,
    REGISTERED_POSITIVE_SCOPE,
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


def _bound_metadata():
    consts = candidate.validate_receipt.__code__.co_consts
    path_index = next(
        i for i, value in enumerate(consts)
        if isinstance(value, str) and value.endswith("authority.sock")
    )
    return (
        consts[path_index],
        consts[path_index + 1],
        consts[path_index + 2],
        consts[path_index + 3],
    )


class CallerProxy(dict):
    pass


class OBL058BoundedRepairR6Court(unittest.TestCase):
    def positive(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(receipt.close)
        return receipt

    def denial(self, suffix="r6-unregistered"):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=f"NONCURRENT_SYNTHETIC::basis::{suffix}",
        )
        self.addCleanup(receipt.close)
        return receipt

    def changed_scope(self, field, value):
        values = REGISTERED_POSITIVE_SCOPE.canonical()
        values[field] = value
        return ExactScope(**values)

    def assert_origin_rejected(self, receipt, scope=REGISTERED_POSITIVE_SCOPE):
        with self.assertRaises(PermissionContractError):
            validate_receipt(receipt, expected_scope=scope)

    def fork_validate_messages(self, receipt, attempts=1):
        if not hasattr(os, "fork"):
            self.skipTest("fork unavailable")
        read_fd, write_fd = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(read_fd)
            messages = []
            for _ in range(attempts):
                try:
                    result = validate_receipt(
                        receipt, expected_scope=REGISTERED_POSITIVE_SCOPE
                    )
                    messages.append("OK:" + result)
                except Exception as exc:
                    messages.append(
                        "ERR:" + type(exc).__name__ + ":" + str(exc)
                    )
            os.write(write_fd, ("\n".join(messages)).encode("utf-8"))
            os.close(write_fd)
            os._exit(0)
        os.close(write_fd)
        data = b""
        while True:
            chunk = os.read(read_fd, 4096)
            if not chunk:
                break
            data += chunk
        os.close(read_fd)
        _pid, status = os.waitpid(pid, 0)
        self.assertTrue(os.WIFEXITED(status))
        return data.decode("utf-8").splitlines()

    def test_r6_01_valid_source_owned_positive_and_negative_controls(self):
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(
                self.positive(), expected_scope=REGISTERED_POSITIVE_SCOPE
            ),
        )
        self.assertEqual(
            DECISION_DENY,
            validate_receipt(
                self.denial(), expected_scope=REGISTERED_POSITIVE_SCOPE
            ),
        )

    def test_r6_02_exact_authority_and_schema_revision(self):
        self.assertEqual(
            "OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0",
            AUTHORITY_ID,
        )
        self.assertEqual(
            "OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0",
            SCHEMA_VERSION,
        )
        receipt = self.positive()
        self.assertEqual(AUTHORITY_ID, receipt["authority_id"])
        self.assertEqual(SCHEMA_VERSION, receipt["schema_version"])

    def test_r6_03_forked_positive_copy_fails_closed(self):
        receipt = self.positive()
        messages = self.fork_validate_messages(receipt)
        self.assertEqual(1, len(messages))
        self.assertTrue(
            messages[0].startswith("ERR:PermissionContractError:"), messages
        )
        self.assertIn("requester_process_generation_mismatch", messages[0])

    def test_r6_04_forked_denial_copy_fails_closed(self):
        receipt = self.denial("fork-deny")
        messages = self.fork_validate_messages(receipt)
        self.assertTrue(
            messages[0].startswith("ERR:PermissionContractError:"), messages
        )
        self.assertIn("requester_process_generation_mismatch", messages[0])

    def test_r6_05_forked_child_repeated_validation_remains_rejected(self):
        receipt = self.positive()
        messages = self.fork_validate_messages(receipt, attempts=3)
        self.assertEqual(3, len(messages))
        self.assertTrue(
            all(
                "requester_process_generation_mismatch" in message
                for message in messages
            ),
            messages,
        )

    def test_r6_06_parent_still_validates_after_forked_child_rejection(self):
        receipt = self.positive()
        self.fork_validate_messages(receipt)
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_r6_07_forked_child_close_cannot_retire_parent_record(self):
        if not hasattr(os, "fork"):
            self.skipTest("fork unavailable")
        receipt = self.positive()
        pid = os.fork()
        if pid == 0:
            receipt.close()
            os._exit(0)
        os.waitpid(pid, 0)
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_r6_08_broker_protocol_rejects_caller_supplied_requester_identity_fields(self):
        receipt = self.positive()
        body_json = object.__getattribute__(receipt, "_body_json")
        with self.assertRaises(PermissionContractError):
            candidate._bound_broker_request({
                "op": "validate",
                "object_id": id(receipt),
                "body_json": body_json,
                "expected_scope": REGISTERED_POSITIVE_SCOPE.canonical(),
                "request_id": "manual",
                "requester_pid": os.getpid(),
            })

    def test_r6_09_broker_derives_peer_process_generation_from_os(self):
        source = inspect.getsource(candidate._broker_service_loop_r6)
        self.assertIn("_peer_identity(conn)", source)
        self.assertIn("peer_pid != owner_pid", source)
        self.assertIn("peer_start != owner_start", source)
        self.assertNotIn("requester_pid", source)

    def test_r6_10_weakref_finalization_retires_broker_record(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        object_id = id(receipt)
        body_json = object.__getattribute__(receipt, "_body_json")
        ref = weakref.ref(receipt)
        del receipt
        gc.collect()
        self.assertIsNone(ref())
        deadline = time.monotonic() + 2
        while True:
            try:
                candidate._bound_broker_request({
                    "op": "validate",
                    "object_id": object_id,
                    "body_json": body_json,
                    "expected_scope": REGISTERED_POSITIVE_SCOPE.canonical(),
                    "request_id": "stale-check",
                })
            except PermissionContractError as exc:
                if "receipt_not_issued_by_source_authority" in str(exc):
                    break
                raise
            if time.monotonic() > deadline:
                self.fail("broker record was not retired by finalization")
            time.sleep(0.01)

    def test_r6_11_duplicate_close_is_idempotent(self):
        receipt = self.positive()
        object_id = id(receipt)
        receipt.close()
        response = candidate._bound_broker_request({
            "op": "close",
            "object_id": object_id,
            "request_id": "duplicate-close",
        })
        self.assertFalse(response["closed"])

    def test_r6_12_direct_duplicate_issue_for_live_object_id_is_rejected(self):
        receipt = self.positive()
        with self.assertRaisesRegex(
            PermissionContractError, "object_identity_already_issued"
        ):
            candidate._bound_broker_request({
                "op": "issue",
                "object_id": id(receipt),
                "scope": REGISTERED_POSITIVE_SCOPE.canonical(),
                "basis_id": REGISTERED_POSITIVE_BASIS_ID,
                "fixture_class": FIXTURE_CLASS,
                "request_id": "duplicate-issue",
            })

    def test_r6_13_same_process_repeated_validation_is_stable(self):
        receipt = self.positive()
        for _ in range(6):
            self.assertEqual(
                DECISION_PERMIT,
                validate_receipt(
                    receipt, expected_scope=REGISTERED_POSITIVE_SCOPE
                ),
            )

    def test_r6_14_same_process_concurrent_validation_is_stable(self):
        receipt = self.positive()
        results = []
        errors = []
        lock = threading.Lock()

        def worker():
            try:
                value = validate_receipt(
                    receipt, expected_scope=REGISTERED_POSITIVE_SCOPE
                )
                with lock:
                    results.append(value)
            except Exception as exc:
                with lock:
                    errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertFalse(errors, errors)
        self.assertEqual([DECISION_PERMIT] * 8, results)

    def test_r6_15_equal_semantic_issuances_have_distinct_authority_instances(self):
        first = self.positive()
        second = self.positive()
        self.assertIsNot(first, second)
        self.assertNotEqual(
            first["authority_instance_id"], second["authority_instance_id"]
        )

    def test_r6_16_cross_receipt_body_rebinding_fails(self):
        first = self.positive()
        second = self.positive()
        saved = object.__getattribute__(first, "_body_json")
        object.__setattr__(
            first,
            "_body_json",
            object.__getattribute__(second, "_body_json"),
        )
        try:
            self.assert_origin_rejected(first)
        finally:
            object.__setattr__(first, "_body_json", saved)

    def test_r6_17_denial_to_positive_body_substitution_fails(self):
        denial = self.denial("body-substitution")
        positive = self.positive()
        saved = object.__getattribute__(denial, "_body_json")
        object.__setattr__(
            denial,
            "_body_json",
            object.__getattribute__(positive, "_body_json"),
        )
        try:
            self.assert_origin_rejected(denial)
        finally:
            object.__setattr__(denial, "_body_json", saved)
        self.assertEqual(
            DECISION_DENY,
            validate_receipt(denial, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_r6_18_constructor_object_new_subclass_mapping_and_proxy_fail(self):
        receipt = self.positive()
        base = type(receipt)
        self.assert_origin_rejected(base())
        self.assert_origin_rejected(object.__new__(base))

        class CallerReceipt(base):
            pass

        self.assert_origin_rejected(CallerReceipt())
        self.assert_origin_rejected(dict(receipt))
        self.assert_origin_rejected(CallerProxy(dict(receipt)))

    def test_r6_19_copy_deepcopy_pickle_and_json_reconstruction_fail(self):
        receipt = self.positive()
        for operation in (
            lambda: copy.copy(receipt),
            lambda: copy.deepcopy(receipt),
            lambda: pickle.dumps(receipt),
        ):
            with self.assertRaises(TypeError):
                operation()
        reconstructed = json.loads(json.dumps(dict(receipt)))
        self.assert_origin_rejected(reconstructed)

    def test_r6_20_registered_basis_is_exactly_bound_across_all_scope_fields(self):
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
                self.assertEqual(
                    DECISION_DENY,
                    validate_receipt(receipt, expected_scope=scope),
                )

    def test_r6_21_cross_scope_replay_rejected_for_all_scope_fields(self):
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
                with self.assertRaisesRegex(
                    PermissionContractError, "scope_mismatch_or_stale"
                ):
                    validate_receipt(
                        receipt,
                        expected_scope=self.changed_scope(field, replacement),
                    )

    def test_r6_22_project_current_namespaces_and_first_canary_rejected(self):
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
        with self.assertRaises(PermissionContractError):
            issue_noncurrent_synthetic_receipt(
                scope=self.changed_scope(
                    "subject_id", CURRENT_FIRST_CANARY_SUBJECT
                ),
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
            )

    def test_r6_23_wrong_field_namespace_empty_suffix_fixture_and_basis_fail(self):
        with self.assertRaises(PermissionContractError):
            issue_noncurrent_synthetic_receipt(
                scope=self.changed_scope(
                    "actor_id", "NONCURRENT_SYNTHETIC::world::wrong"
                ),
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
            )
        with self.assertRaises(PermissionContractError):
            issue_noncurrent_synthetic_receipt(
                scope=self.changed_scope(
                    "actor_id", "NONCURRENT_SYNTHETIC::actor::   "
                ),
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
            )
        with self.assertRaisesRegex(
            PermissionContractError,
            "project_current_or_unknown_fixture_not_authorized",
        ):
            issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
                fixture_class="PROJECT_CURRENT",
            )
        with self.assertRaisesRegex(
            PermissionContractError, "missing_basis_id"
        ):
            issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE, basis_id="   "
            )

    def test_r6_24_inference_like_surrogates_do_not_imply_permission(self):
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
                    validate_receipt(
                        receipt, expected_scope=REGISTERED_POSITIVE_SCOPE
                    ),
                )

    def _tamper(self, field, value, expected_error, recompute=False):
        receipt = self.positive()
        body = json.loads(object.__getattribute__(receipt, "_body_json"))
        body[field] = value
        if recompute:
            body["receipt_digest"] = receipt_digest(body)
        object.__setattr__(
            receipt, "_body_json", candidate._canonical_json(body)
        )
        with self.assertRaisesRegex(PermissionContractError, expected_error):
            validate_receipt(
                receipt, expected_scope=REGISTERED_POSITIVE_SCOPE
            )

    def test_r6_25_authority_schema_fixture_decision_tampering_fail_closed(self):
        self._tamper("authority_id", "WRONG", "wrong_authority", True)
        self._tamper("schema_version", "WRONG", "wrong_schema", True)
        self._tamper(
            "fixture_class",
            "PROJECT_CURRENT",
            "project_current_or_unknown_fixture_not_authorized",
            True,
        )
        self._tamper("decision", "MAYBE", "invalid_decision", True)

    def test_r6_26_integrity_proof_scope_and_instance_tampering_fail_closed(self):
        self._tamper(
            "receipt_digest", "0" * 64, "receipt_integrity_mismatch"
        )
        self._tamper(
            "basis_proof_digest",
            "0" * 64,
            "source_basis_proof_mismatch",
            True,
        )
        self._tamper(
            "basis_scope_digest",
            "0" * 64,
            "basis_scope_mismatch",
            True,
        )
        self._tamper(
            "authority_instance_id",
            "wrong",
            "receipt_not_issued_by_source_authority",
            True,
        )

    def test_r6_27_caller_permission_boolean_and_basis_kind_inputs_remain_absent(self):
        parameters = inspect.signature(
            issue_noncurrent_synthetic_receipt
        ).parameters
        self.assertNotIn("explicit_source_permission", parameters)
        self.assertNotIn("basis_kind", parameters)

    def test_r6_28_broker_identity_is_bound_and_no_process_handles_live_on_receipt(self):
        receipt = self.positive()
        self.assertEqual(
            ("_body_json", "__weakref__"), IssuedReceipt.__slots__
        )
        self.assertFalse(hasattr(receipt, "_proc"))
        self.assertFalse(hasattr(receipt, "_read_fd"))
        self.assertFalse(hasattr(receipt, "_write_fd"))
        path, pid, start, uid = _bound_metadata()
        self.assertTrue(path.endswith("authority.sock"))
        self.assertEqual(candidate._proc_starttime(pid), start)
        self.assertEqual(os.getuid(), uid)

    def test_r6_29_broker_death_fails_closed(self):
        receipt = self.positive()
        _path, broker_pid, _start, _uid = _bound_metadata()
        os.kill(broker_pid, signal.SIGTERM)
        deadline = time.monotonic() + 2
        while (
            os.path.exists(f"/proc/{broker_pid}")
            and time.monotonic() < deadline
        ):
            time.sleep(0.01)
        with self.assertRaises(PermissionContractError):
            validate_receipt(
                receipt, expected_scope=REGISTERED_POSITIVE_SCOPE
            )

    def test_r6_30_authority_child_death_fails_closed(self):
        code = r'''
import os, signal, time, socket, struct, subprocess
import causal_use_permission_candidate_r6 as c
r = c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE, basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
consts = c.validate_receipt.__code__.co_consts
i = next(i for i,v in enumerate(consts) if isinstance(v,str) and v.endswith('authority.sock'))
path = consts[i]
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(path)
creds = s.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize('3i'))
broker_pid, _uid, _gid = struct.unpack('3i', creds)
s.close()
raw = ''
for _ in range(100):
    raw = subprocess.run(['ps','--ppid',str(broker_pid),'-o','pid='], capture_output=True, text=True).stdout.strip()
    if raw:
        break
    time.sleep(0.01)
child_pids = [int(x) for x in raw.split()]
for pid in child_pids:
    os.kill(pid, signal.SIGTERM)
time.sleep(0.05)
try:
    c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
except c.PermissionContractError:
    raise SystemExit(0)
raise SystemExit(2)
'''
        proc = __import__("subprocess").run(
            [__import__("sys").executable, "-c", code],
            env={
                **os.environ,
                "PYTHONPATH": os.path.dirname(candidate.__file__),
            },
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(0, proc.returncode, proc.stderr + proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
