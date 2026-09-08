"""Fresh distinct independent review for frozen OBL058 R6 candidate.

One blocking check intentionally asserts a reproduced later-object-generation
acceptance. A green governed execution proves the observation is reproducible;
semantic PASS/FAIL is recorded separately by the reviewer.
"""
from __future__ import annotations

from collections.abc import Mapping
import copy
import gc
import json
import os
from pathlib import Path
import pickle
import signal
import socket
import struct
import subprocess
import sys
import threading
import time
import unittest
import uuid
import weakref

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import causal_use_permission_candidate_r6 as candidate  # noqa: E402
from causal_use_permission_candidate_r6 import (  # noqa: E402
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
    validate_receipt,
)

CURRENT_FIRST_CANARY_SUBJECT = (
    "urn:rawlsing:v3:subject:sha256:"
    "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
)


class CallerProxy(Mapping):
    def __init__(self, body):
        self.body = body

    def __getitem__(self, key):
        return self.body[key]

    def __iter__(self):
        return iter(self.body)

    def __len__(self):
        return len(self.body)


def _broker_path() -> str:
    paths = [
        value for value in validate_receipt.__code__.co_consts
        if isinstance(value, str) and value.endswith("/authority.sock")
    ]
    if len(paths) != 1:
        raise AssertionError(f"expected one bound broker path, got {paths!r}")
    return paths[0]


def _broker_peer_pid(path: str) -> int:
    conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        conn.connect(path)
        raw = conn.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i"))
        pid, _uid, _gid = struct.unpack("3i", raw)
        return pid
    finally:
        conn.close()


def _find_receipt_finalizer(receipt):
    registry = getattr(weakref.finalize, "_registry", {})
    matches = []
    for fin in list(registry):
        try:
            peeked = fin.peek()
        except Exception:
            continue
        if peeked and peeked[0] is receipt:
            matches.append(fin)
    if len(matches) != 1:
        raise AssertionError(f"expected exactly one receipt finalizer, got {len(matches)}")
    return matches[0]


def _run_isolated(script: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(HERE)
    return subprocess.run(
        [sys.executable, "-c", script],
        cwd=HERE,
        env=env,
        text=True,
        capture_output=True,
        timeout=45,
        check=False,
    )


class OBL058R6IndependentReview(unittest.TestCase):
    def positive(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(receipt.close)
        return receipt

    def denial(self, suffix="r6-independent-deny"):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=f"NONCURRENT_SYNTHETIC::basis::{suffix}",
        )
        self.addCleanup(receipt.close)
        return receipt

    def changed_scope(self, field, value):
        data = REGISTERED_POSITIVE_SCOPE.canonical()
        data[field] = value
        return ExactScope(**data)

    def assert_rejected(self, receipt, scope=REGISTERED_POSITIVE_SCOPE):
        with self.assertRaises(PermissionContractError):
            validate_receipt(receipt, expected_scope=scope)

    # Blocking lifecycle finding: retirement correctness depends on an inspectable
    # weakref.finalize registration that a caller can detach before object release.

    def test_b01_detached_finalizer_leaves_stale_record_for_later_exact_type_generation(self):
        original = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        old_id = id(original)
        body_json = object.__getattribute__(original, "_body_json")
        fin = _find_receipt_finalizer(original)
        detached = fin.detach()
        self.assertIsNotNone(detached)
        del detached
        del fin
        del original
        gc.collect()

        replacement = None
        for _ in range(250000):
            probe = IssuedReceipt()
            if id(probe) == old_id:
                replacement = probe
                break
            del probe
        self.assertIsNotNone(replacement, "CPython did not reuse the released exact-type object id")
        try:
            object.__setattr__(replacement, "_body_json", body_json)
            self.assertEqual(
                DECISION_PERMIT,
                validate_receipt(replacement, expected_scope=REGISTERED_POSITIVE_SCOPE),
            )
        finally:
            if replacement is not None:
                replacement.close()

    # Process-generation checks.

    def _fork_observe(self, receipt, *, close_first=False):
        if not hasattr(os, "fork"):
            self.skipTest("fork unavailable")
        read_fd, write_fd = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(read_fd)
            try:
                if close_first:
                    receipt.close()
                    payload = b"CLOSE_RETURNED"
                else:
                    result = validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)
                    payload = f"RESULT:{result}".encode()
            except Exception as exc:
                payload = f"ERROR:{type(exc).__name__}:{exc}".encode()
            try:
                os.write(write_fd, payload)
            finally:
                os.close(write_fd)
                os._exit(0)
        os.close(write_fd)
        payload = os.read(read_fd, 4096).decode()
        os.close(read_fd)
        _child, status = os.waitpid(pid, 0)
        self.assertTrue(os.WIFEXITED(status))
        return payload

    def test_p01_forked_positive_copy_is_rejected_and_parent_remains_valid(self):
        receipt = self.positive()
        payload = self._fork_observe(receipt)
        self.assertTrue(payload.startswith("ERROR:PermissionContractError:"), payload)
        self.assertIn("requester_process_generation_mismatch", payload)
        self.assertEqual(DECISION_PERMIT, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_p02_forked_denial_copy_is_rejected(self):
        receipt = self.denial("fork-deny")
        payload = self._fork_observe(receipt)
        self.assertTrue(payload.startswith("ERROR:PermissionContractError:"), payload)
        self.assertIn("requester_process_generation_mismatch", payload)
        self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_p03_forked_close_cannot_retire_parent_record(self):
        receipt = self.positive()
        payload = self._fork_observe(receipt, close_first=True)
        self.assertEqual("CLOSE_RETURNED", payload)
        self.assertEqual(DECISION_PERMIT, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_p04_caller_supplied_requester_identity_fields_are_rejected(self):
        shell = IssuedReceipt()
        request_id = uuid.uuid4().hex
        with self.assertRaises(PermissionContractError):
            candidate._bound_broker_request({
                "op": "issue",
                "object_id": id(shell),
                "scope": REGISTERED_POSITIVE_SCOPE.canonical(),
                "basis_id": REGISTERED_POSITIVE_BASIS_ID,
                "fixture_class": FIXTURE_CLASS,
                "request_id": request_id,
                "requester_pid": os.getpid(),
            })

    # Ordinary lifecycle and identity controls.

    def test_l01_normal_finalizer_retires_record_deterministically(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        object_id = id(receipt)
        body_json = object.__getattribute__(receipt, "_body_json")
        del receipt
        gc.collect()
        with self.assertRaises(PermissionContractError):
            candidate._bound_broker_request({
                "op": "validate",
                "object_id": object_id,
                "body_json": body_json,
                "expected_scope": REGISTERED_POSITIVE_SCOPE.canonical(),
                "request_id": uuid.uuid4().hex,
            })

    def test_l02_duplicate_close_is_idempotent_and_closed_receipt_rejects(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        receipt.close()
        receipt.close()
        self.assert_rejected(receipt)

    def test_l03_equal_inputs_produce_distinct_authority_instances(self):
        first = self.positive()
        second = self.positive()
        self.assertNotEqual(first["authority_instance_id"], second["authority_instance_id"])
        self.assertIsNot(first, second)
        self.assertEqual(DECISION_PERMIT, validate_receipt(first, expected_scope=REGISTERED_POSITIVE_SCOPE))
        self.assertEqual(DECISION_PERMIT, validate_receipt(second, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_l04_cross_receipt_body_reuse_is_rejected(self):
        first = self.positive()
        second = self.positive()
        saved = object.__getattribute__(second, "_body_json")
        object.__setattr__(second, "_body_json", object.__getattribute__(first, "_body_json"))
        try:
            self.assert_rejected(second)
        finally:
            object.__setattr__(second, "_body_json", saved)

    # Reconstruction and replay.

    def test_r01_constructor_object_new_subclass_mapping_proxy_and_json_reject(self):
        receipt = self.positive()
        self.assert_rejected(IssuedReceipt())
        self.assert_rejected(object.__new__(IssuedReceipt))
        class Derived(IssuedReceipt):
            pass
        self.assert_rejected(Derived())
        body = dict(receipt)
        self.assert_rejected(body)
        self.assert_rejected(CallerProxy(body))
        self.assert_rejected(json.loads(json.dumps(body)))

    def test_r02_copy_deepcopy_and_pickle_are_rejected(self):
        receipt = self.positive()
        with self.assertRaises(TypeError):
            copy.copy(receipt)
        with self.assertRaises(TypeError):
            copy.deepcopy(receipt)
        with self.assertRaises(TypeError):
            pickle.dumps(receipt)

    def test_r03_cross_scope_replay_is_rejected_for_all_fields(self):
        receipt = self.positive()
        replacements = {
            "actor_id": "NONCURRENT_SYNTHETIC::actor::review-other",
            "world_id": "NONCURRENT_SYNTHETIC::world::review-other",
            "subject_id": "NONCURRENT_SYNTHETIC::subject::review-other",
            "time_id": "NONCURRENT_SYNTHETIC::time::review-other",
            "transition_id": "NONCURRENT_SYNTHETIC::transition::review-other",
        }
        for field, value in replacements.items():
            with self.subTest(field=field):
                self.assert_rejected(receipt, self.changed_scope(field, value))

    # Broker and request isolation.

    def test_broker01_broker_death_fails_closed_in_isolated_process(self):
        script = r'''
import os, signal, socket, struct, time
from causal_use_permission_candidate_r6 import *
r = issue_noncurrent_synthetic_receipt(scope=REGISTERED_POSITIVE_SCOPE, basis_id=REGISTERED_POSITIVE_BASIS_ID)
path = [x for x in validate_receipt.__code__.co_consts if isinstance(x, str) and x.endswith('/authority.sock')][0]
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); s.connect(path)
raw=s.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,struct.calcsize('3i')); pid,uid,gid=struct.unpack('3i',raw); s.close()
os.kill(pid, signal.SIGTERM); time.sleep(.1)
try:
    validate_receipt(r, expected_scope=REGISTERED_POSITIVE_SCOPE)
    print('ACCEPTED')
except PermissionContractError:
    print('REJECTED')
'''
        result = _run_isolated(script)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("REJECTED", result.stdout)
        self.assertNotIn("ACCEPTED", result.stdout)

    def test_broker02_repeated_and_concurrent_validation_is_stable(self):
        receipt = self.positive()
        results = []
        errors = []
        lock = threading.Lock()
        def worker():
            try:
                value = validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)
                with lock:
                    results.append(value)
            except Exception as exc:
                with lock:
                    errors.append(exc)
        threads = [threading.Thread(target=worker) for _ in range(8)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=20)
        self.assertFalse(errors, errors)
        self.assertEqual([DECISION_PERMIT] * 8, sorted(results))

    # Exact semantic/current-state boundaries.

    def test_s01_registered_positive_and_unregistered_denial_are_functional(self):
        self.assertEqual(DECISION_PERMIT, validate_receipt(self.positive(), expected_scope=REGISTERED_POSITIVE_SCOPE))
        self.assertEqual(DECISION_DENY, validate_receipt(self.denial(), expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_s02_registered_basis_is_exactly_bound_across_all_five_fields(self):
        replacements = {
            "actor_id": "NONCURRENT_SYNTHETIC::actor::changed",
            "world_id": "NONCURRENT_SYNTHETIC::world::changed",
            "subject_id": "NONCURRENT_SYNTHETIC::subject::changed",
            "time_id": "NONCURRENT_SYNTHETIC::time::changed",
            "transition_id": "NONCURRENT_SYNTHETIC::transition::changed",
        }
        for field, value in replacements.items():
            with self.subTest(field=field):
                scope = self.changed_scope(field, value)
                receipt = issue_noncurrent_synthetic_receipt(scope=scope, basis_id=REGISTERED_POSITIVE_BASIS_ID)
                self.addCleanup(receipt.close)
                self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=scope))

    def test_s03_project_current_shapes_and_exact_first_canary_are_rejected(self):
        cases = {
            "actor_id": "urn:rawlsing:v3:actor:project-current:a",
            "world_id": "urn:rawlsing:v3:world:project-current:w",
            "subject_id": CURRENT_FIRST_CANARY_SUBJECT,
            "time_id": "urn:rawlsing:v3:time:project-current:t",
            "transition_id": "urn:rawlsing:v3:transition:project-current:tr",
        }
        for field, value in cases.items():
            with self.subTest(field=field):
                with self.assertRaises(PermissionContractError):
                    issue_noncurrent_synthetic_receipt(
                        scope=self.changed_scope(field, value),
                        basis_id=REGISTERED_POSITIVE_BASIS_ID,
                    )

    def test_s04_surrogate_basis_strings_do_not_imply_permission(self):
        for basis_id in (
            "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
            "ADP-010",
            "ADP-019::OCCURRENCE_ADMITTED",
            "ROUTED_TO_SAME_ENDPOINT",
            "COLOCATED_SAME_TIME_AND_PLACE",
            "NARRATIVE_PLAUSIBILITY",
        ):
            with self.subTest(basis_id=basis_id):
                receipt = issue_noncurrent_synthetic_receipt(scope=REGISTERED_POSITIVE_SCOPE, basis_id=basis_id)
                self.addCleanup(receipt.close)
                self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_s05_authority_schema_fixture_and_no_current_effect_surface_are_exact(self):
        receipt = self.positive()
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0", AUTHORITY_ID)
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0", SCHEMA_VERSION)
        self.assertEqual(FIXTURE_CLASS, receipt["fixture_class"])
        names = set(candidate.__dict__)
        for name in (
            "execute_obl055", "install_obl056_positive", "create_encounter",
            "realize_oee", "create_actor", "activate_actor", "register_source_basis",
        ):
            self.assertNotIn(name, names)


if __name__ == "__main__":
    unittest.main(verbosity=2)
