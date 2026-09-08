"""Fresh distinct independent review for frozen OBL058 R5 candidate.

Blocking checks intentionally assert independently reproduced incorrect-positive
source-origin behavior. A green governed execution proves the observation is
reproducible; semantic PASS/FAIL is recorded separately by the reviewer.
"""
from __future__ import annotations

from collections.abc import Mapping
import atexit
import copy
import gc
import importlib.util
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
import unittest
import uuid

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
        conn.settimeout(5)
        conn.connect(path)
        raw = conn.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i"))
        pid, _uid, _gid = struct.unpack("3i", raw)
        return pid
    finally:
        conn.close()


def _run_isolated(script: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(HERE)
    return subprocess.run(
        [sys.executable, "-c", script],
        cwd=HERE,
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )


class OBL058R5IndependentReview(unittest.TestCase):
    def positive(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(receipt.close)
        return receipt

    def denial(self, suffix="r5-independent-deny"):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=f"NONCURRENT_SYNTHETIC::basis::{suffix}",
        )
        self.addCleanup(receipt.close)
        return receipt

    def changed_scope(self, field: str, value: str) -> ExactScope:
        body = REGISTERED_POSITIVE_SCOPE.canonical()
        body[field] = value
        return ExactScope(**body)

    def assert_rejected(self, receipt, scope=REGISTERED_POSITIVE_SCOPE):
        with self.assertRaises(PermissionContractError):
            validate_receipt(receipt, expected_scope=scope)

    def direct_broker_issue(self, receipt, *, basis_id=REGISTERED_POSITIVE_BASIS_ID):
        request_id = uuid.uuid4().hex
        return candidate._bound_broker_request({
            "op": "issue",
            "object_id": id(receipt),
            "scope": REGISTERED_POSITIVE_SCOPE.canonical(),
            "basis_id": basis_id,
            "fixture_class": FIXTURE_CLASS,
            "request_id": request_id,
        })

    # Blocking exact-object-generation/process-binding findings.

    def test_b01_parent_reachable_broker_issue_accepts_caller_selected_object_id(self):
        shell = IssuedReceipt()
        response = self.direct_broker_issue(shell)
        self.assertIsInstance(response.get("body_json"), str)
        object.__setattr__(shell, "_body_json", response["body_json"])
        try:
            self.assertEqual(
                DECISION_PERMIT,
                validate_receipt(shell, expected_scope=REGISTERED_POSITIVE_SCOPE),
            )
        finally:
            shell.close()

    def test_b02_stale_broker_record_accepts_new_exact_type_after_cpython_id_reuse(self):
        original = IssuedReceipt()
        response = self.direct_broker_issue(original)
        old_id = id(original)
        body_json = response["body_json"]
        del original
        gc.collect()

        replacement = None
        for _ in range(100000):
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

    def test_b03_forked_process_copy_of_positive_receipt_still_validates_positive(self):
        if not hasattr(os, "fork"):
            self.skipTest("fork unavailable")
        receipt = self.positive()
        read_fd, write_fd = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(read_fd)
            try:
                result = validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)
                payload = result.encode("utf-8")
            except Exception as exc:  # pragma: no cover - child report path
                payload = f"ERROR:{type(exc).__name__}:{exc}".encode("utf-8")
            try:
                os.write(write_fd, payload)
            finally:
                os.close(write_fd)
                os._exit(0)
        os.close(write_fd)
        payload = os.read(read_fd, 4096).decode("utf-8")
        os.close(read_fd)
        _child, status = os.waitpid(pid, 0)
        self.assertTrue(os.WIFEXITED(status))
        self.assertEqual(DECISION_PERMIT, payload)

    def test_b04_fork_child_can_recycle_inherited_id_after_clearing_copied_lifetime_pins(self):
        if not hasattr(os, "fork") or not hasattr(atexit, "_clear"):
            self.skipTest("required CPython fork/atexit surface unavailable")
        receipt = self.positive()
        body_json = object.__getattribute__(receipt, "_body_json")
        old_id = id(receipt)
        read_fd, write_fd = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(read_fd)
            try:
                # This clears only the fork child's copied exit callbacks. The
                # source broker remains the parent-owned broker process.
                atexit._clear()  # type: ignore[attr-defined]
                receipt = None
                gc.collect()
                replacement = None
                for _ in range(100000):
                    probe = IssuedReceipt()
                    if id(probe) == old_id:
                        replacement = probe
                        break
                    del probe
                if replacement is None:
                    payload = b"NO_ID_REUSE"
                else:
                    object.__setattr__(replacement, "_body_json", body_json)
                    payload = validate_receipt(
                        replacement, expected_scope=REGISTERED_POSITIVE_SCOPE
                    ).encode("utf-8")
            except Exception as exc:  # pragma: no cover - child report path
                payload = f"ERROR:{type(exc).__name__}:{exc}".encode("utf-8")
            try:
                os.write(write_fd, payload)
            finally:
                os.close(write_fd)
                os._exit(0)
        os.close(write_fd)
        payload = os.read(read_fd, 4096).decode("utf-8")
        os.close(read_fd)
        os.waitpid(pid, 0)
        self.assertEqual(DECISION_PERMIT, payload)

    # Broker/process identity and fail-closed transport controls.

    def test_c01_bound_validator_does_not_follow_module_helper_rebinding(self):
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

    def test_c02_socket_path_rebinding_to_unrelated_same_user_server_fails_closed(self):
        script = r'''
import os, socket, threading
import causal_use_permission_candidate_r5 as c
r = c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE, basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
path = next(x for x in c.validate_receipt.__code__.co_consts if isinstance(x, str) and x.endswith('/authority.sock'))
os.unlink(path)
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(path)
server.listen(1)
def answer():
    conn, _ = server.accept()
    try:
        conn.recv(65536)
        conn.sendall(b'{"ok":true,"request_id":"x","decision":"PERMIT","authority_instance_id":"x"}\n')
    except Exception:
        pass
    finally:
        conn.close()
t = threading.Thread(target=answer, daemon=True); t.start()
try:
    c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
    print('INCORRECT_POSITIVE')
except c.PermissionContractError:
    print('REJECTED')
finally:
    server.close()
'''
        result = _run_isolated(script)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("REJECTED", result.stdout.strip())

    def test_c03_broker_death_fails_closed(self):
        script = r'''
import os, signal, socket, struct
import causal_use_permission_candidate_r5 as c
r = c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE, basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
path = next(x for x in c.validate_receipt.__code__.co_consts if isinstance(x, str) and x.endswith('/authority.sock'))
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); s.connect(path)
raw = s.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize('3i')); s.close()
pid, uid, gid = struct.unpack('3i', raw)
os.kill(pid, signal.SIGTERM)
os.waitpid(pid, 0)
try:
    c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
    print('INCORRECT_POSITIVE')
except c.PermissionContractError:
    print('REJECTED')
'''
        result = _run_isolated(script)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("REJECTED", result.stdout.strip())

    def test_c04_authority_child_death_fails_closed(self):
        script = r'''
import os, signal, socket, struct, time
from pathlib import Path
import causal_use_permission_candidate_r5 as c
r = c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE, basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
path = next(x for x in c.validate_receipt.__code__.co_consts if isinstance(x, str) and x.endswith('/authority.sock'))
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); s.connect(path)
raw = s.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize('3i')); s.close()
broker_pid = struct.unpack('3i', raw)[0]
children_path = Path(f'/proc/{broker_pid}/task/{broker_pid}/children')
children = [int(x) for x in children_path.read_text().split()]
if not children:
    print('NO_CHILD')
else:
    os.kill(children[-1], signal.SIGTERM)
    time.sleep(0.05)
    try:
        c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
        print('INCORRECT_POSITIVE')
    except c.PermissionContractError:
        print('REJECTED')
'''
        result = _run_isolated(script)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("REJECTED", result.stdout.strip())

    # Receipt/body/instance correspondence and construction controls.

    def test_d01_denial_to_positive_body_substitution_is_rejected(self):
        denial = self.denial("body-substitution")
        positive = self.positive()
        original = object.__getattribute__(denial, "_body_json")
        object.__setattr__(denial, "_body_json", object.__getattribute__(positive, "_body_json"))
        try:
            self.assert_rejected(denial)
        finally:
            object.__setattr__(denial, "_body_json", original)

    def test_d02_cross_receipt_equal_positive_body_reuse_is_rejected(self):
        first = self.positive()
        second = self.positive()
        self.assertNotEqual(first["authority_instance_id"], second["authority_instance_id"])
        original = object.__getattribute__(second, "_body_json")
        object.__setattr__(second, "_body_json", object.__getattribute__(first, "_body_json"))
        try:
            self.assert_rejected(second)
        finally:
            object.__setattr__(second, "_body_json", original)

    def test_d03_constructor_object_new_subclass_mapping_proxy_and_serialization_do_not_validate(self):
        positive = self.positive()
        body = object.__getattribute__(positive, "_body_json")
        ordinary = IssuedReceipt(); object.__setattr__(ordinary, "_body_json", body)
        raw = object.__new__(IssuedReceipt); object.__setattr__(raw, "_body_json", body)

        class ChildReceipt(IssuedReceipt):
            pass

        subclassed = ChildReceipt(); object.__setattr__(subclassed, "_body_json", body)
        for value in (ordinary, raw, subclassed, dict(positive), CallerProxy(dict(positive))):
            with self.subTest(kind=type(value).__name__):
                self.assert_rejected(value)
        for op in (lambda: copy.copy(positive), lambda: copy.deepcopy(positive), lambda: pickle.dumps(positive)):
            with self.assertRaises(TypeError):
                op()
        self.assert_rejected(json.loads(json.dumps(dict(positive))))

    def test_d04_body_integrity_and_authority_instance_mutations_fail_closed(self):
        fields = (
            ("authority_id", "WRONG"),
            ("schema_version", "WRONG"),
            ("fixture_class", "PROJECT_CURRENT"),
            ("decision", DECISION_DENY),
            ("basis_scope_digest", "0" * 64),
            ("basis_proof_digest", "0" * 64),
            ("authority_instance_id", "wrong-instance"),
            ("receipt_digest", "0" * 64),
        )
        for field, value in fields:
            with self.subTest(field=field):
                receipt = self.positive()
                original = object.__getattribute__(receipt, "_body_json")
                body = json.loads(original)
                body[field] = value
                if field != "receipt_digest":
                    try:
                        body["receipt_digest"] = receipt_digest(body)
                    except Exception:
                        pass
                object.__setattr__(receipt, "_body_json", json.dumps(body, sort_keys=True, separators=(",", ":")))
                try:
                    self.assert_rejected(receipt)
                finally:
                    object.__setattr__(receipt, "_body_json", original)

    # Repetition, concurrency, multiple instances, and semantic jurisdiction.

    def test_e01_repeated_and_concurrent_validation_keeps_genuine_controls_stable(self):
        positive = self.positive()
        denial = self.denial("concurrent")
        for _ in range(3):
            self.assertEqual(DECISION_PERMIT, validate_receipt(positive, expected_scope=REGISTERED_POSITIVE_SCOPE))
            self.assertEqual(DECISION_DENY, validate_receipt(denial, expected_scope=REGISTERED_POSITIVE_SCOPE))

        results = []
        errors = []
        lock = threading.Lock()
        def run(receipt, expected):
            try:
                got = validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)
                with lock:
                    results.append((expected, got))
            except Exception as exc:
                with lock:
                    errors.append(exc)
        threads = []
        for _ in range(4):
            threads.append(threading.Thread(target=run, args=(positive, DECISION_PERMIT)))
            threads.append(threading.Thread(target=run, args=(denial, DECISION_DENY)))
        for thread in threads: thread.start()
        for thread in threads: thread.join(timeout=10)
        self.assertFalse(errors)
        self.assertEqual(8, len(results))
        self.assertTrue(all(expected == got for expected, got in results))

    def test_e02_fresh_module_instance_does_not_accept_other_instance_receipt(self):
        script = r'''
import importlib.util
from pathlib import Path
import causal_use_permission_candidate_r5 as a
path = Path(a.__file__).resolve()
spec = importlib.util.spec_from_file_location('obl058_r5_second_instance', path)
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
r = a.issue_noncurrent_synthetic_receipt(scope=a.REGISTERED_POSITIVE_SCOPE, basis_id=a.REGISTERED_POSITIVE_BASIS_ID)
try:
    b.validate_receipt(r, expected_scope=b.REGISTERED_POSITIVE_SCOPE)
    print('INCORRECT_POSITIVE')
except b.PermissionContractError:
    print('REJECTED')
'''
        result = _run_isolated(script)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("REJECTED", result.stdout.strip())

    def test_e03_registered_basis_is_exact_scope_bound_and_cross_scope_replay_rejects(self):
        replacements = {
            "actor_id": "NONCURRENT_SYNTHETIC::actor::review-changed",
            "world_id": "NONCURRENT_SYNTHETIC::world::review-changed",
            "subject_id": "NONCURRENT_SYNTHETIC::subject::review-changed",
            "time_id": "NONCURRENT_SYNTHETIC::time::review-changed",
            "transition_id": "NONCURRENT_SYNTHETIC::transition::review-changed",
        }
        source = self.positive()
        for field, replacement in replacements.items():
            with self.subTest(field=field):
                scope = self.changed_scope(field, replacement)
                receipt = issue_noncurrent_synthetic_receipt(
                    scope=scope, basis_id=REGISTERED_POSITIVE_BASIS_ID
                )
                self.addCleanup(receipt.close)
                self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=scope))
                self.assert_rejected(source, scope=scope)

    def test_e04_current_shaped_wrong_field_empty_suffix_first_canary_and_fixture_reject(self):
        currentish = {
            "actor_id": "urn:rawlsing:v3:actor:project-current:a",
            "world_id": "urn:rawlsing:v3:world:project-current:w",
            "subject_id": "urn:rawlsing:v3:subject:project-current:s",
            "time_id": "urn:rawlsing:v3:time:project-current:t",
            "transition_id": "urn:rawlsing:v3:transition:project-current:tr",
        }
        for field, replacement in currentish.items():
            with self.subTest(field=field):
                with self.assertRaises(PermissionContractError):
                    issue_noncurrent_synthetic_receipt(
                        scope=self.changed_scope(field, replacement),
                        basis_id=REGISTERED_POSITIVE_BASIS_ID,
                    )
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
        with self.assertRaises(PermissionContractError):
            issue_noncurrent_synthetic_receipt(
                scope=self.changed_scope("subject_id", CURRENT_FIRST_CANARY_SUBJECT),
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
            )
        with self.assertRaises(PermissionContractError):
            issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
                fixture_class="PROJECT_CURRENT",
            )

    def test_e05_inference_like_basis_strings_deny_and_unregistered_basis_denies(self):
        values = (
            "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
            "ADP-010",
            "ADP-019::OCCURRENCE_ADMITTED",
            "ROUTED_TO_SAME_ENDPOINT",
            "COLOCATED_SAME_TIME_AND_PLACE",
            "NARRATIVE_PLAUSIBILITY",
            "NONCURRENT_SYNTHETIC::basis::unregistered-independent",
        )
        for basis_id in values:
            with self.subTest(basis_id=basis_id):
                receipt = issue_noncurrent_synthetic_receipt(
                    scope=REGISTERED_POSITIVE_SCOPE,
                    basis_id=basis_id,
                )
                self.addCleanup(receipt.close)
                self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_e06_no_project_current_or_downstream_effect_surfaces(self):
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
            with self.subTest(name=name):
                self.assertNotIn(name, names)


if __name__ == "__main__":
    unittest.main(verbosity=2)
