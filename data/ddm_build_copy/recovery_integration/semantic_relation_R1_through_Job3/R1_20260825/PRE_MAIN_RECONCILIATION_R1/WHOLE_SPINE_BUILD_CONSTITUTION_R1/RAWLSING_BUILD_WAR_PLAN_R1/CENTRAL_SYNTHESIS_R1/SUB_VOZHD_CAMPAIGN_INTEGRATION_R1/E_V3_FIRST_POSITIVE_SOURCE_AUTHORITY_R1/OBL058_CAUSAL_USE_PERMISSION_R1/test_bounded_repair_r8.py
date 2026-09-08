"""Producer governed verification for OBL058 R8 bounded repair.

This is producer-side verification only.  It closes the R7 mutable Python
transport-construction finding while preserving the independently confirmed R7
lifecycle, process-generation, scope, source-basis, and no-current-effect law.
"""
from __future__ import annotations

import copy
from concurrent.futures import ThreadPoolExecutor
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
import textwrap
import time
import unittest
import weakref

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import causal_use_permission_candidate_r8 as candidate  # noqa: E402
from causal_use_permission_candidate_r8 import (  # noqa: E402
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
    native_broker_pid,
    native_broker_socket_path,
    native_lifetime_reservation_count,
    native_successful_close_count,
    native_transport_success_count,
    validate_receipt,
)

CURRENT_FIRST_CANARY_SUBJECT = (
    "urn:rawlsing:v3:subject:sha256:"
    "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
)


class CallerProxy(dict):
    pass


class FakePythonSocket:
    """R7-review-style Python transport substitute; R8 must never call it."""

    calls = 0

    def __init__(self, *args, **kwargs):
        type(self).calls += 1
        self.response = b""

    def settimeout(self, value):
        pass

    def connect(self, path):
        pass

    def getsockopt(self, level, option, size):
        return struct.pack("3i", native_broker_pid(), os.getuid(), 0)

    def sendall(self, wire):
        request = json.loads(wire.decode("utf-8").split("\n", 1)[0])
        response = {"ok": True, "request_id": request["request_id"]}
        if request["op"] == "issue":
            response["body_json"] = json.dumps(
                {"decision": "PERMIT", "authority_instance_id": "python-substitute"},
                separators=(",", ":"),
            )
            response["authority_instance_id"] = "python-substitute"
        elif request["op"] == "validate":
            response["decision"] = "PERMIT"
            response["authority_instance_id"] = "python-substitute"
        elif request["op"] == "close":
            response["closed"] = True
        self.response = (json.dumps(response, separators=(",", ":")) + "\n").encode()

    def recv(self, size):
        if not self.response:
            return b""
        result, self.response = self.response, b""
        return result

    def close(self):
        pass


class OBL058BoundedRepairR8Court(unittest.TestCase):
    def positive(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(receipt.close)
        return receipt

    def denial(self, suffix="r8-unregistered"):
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

    def run_isolated(self, body: str, timeout: int = 45) -> str:
        script = (
            "import sys\nfrom pathlib import Path\n"
            + f"sys.path.insert(0, {str(HERE)!r})\n"
            + textwrap.dedent(body)
        )
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=str(HERE),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            check=False,
        )
        if result.returncode != 0:
            self.fail(
                f"isolated R8 process failed rc={result.returncode}\n"
                f"stdout={result.stdout}\nstderr={result.stderr}"
            )
        return result.stdout.strip()

    def patch_python_socket(self):
        import _socket

        FakePythonSocket.calls = 0
        real_public = socket.socket
        real_low = _socket.socket
        socket.socket = FakePythonSocket
        _socket.socket = FakePythonSocket
        self.addCleanup(setattr, socket, "socket", real_public)
        self.addCleanup(setattr, _socket, "socket", real_low)
        return FakePythonSocket

    def test_r8_01_valid_registered_permit_and_unregistered_deny(self):
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(self.positive(), expected_scope=REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(
            DECISION_DENY,
            validate_receipt(self.denial(), expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_r8_02_exact_authority_schema_and_mechanism_revision(self):
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0", AUTHORITY_ID)
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0", SCHEMA_VERSION)
        self.assertEqual(
            "OBL058_CAUSAL_USE_PERMISSION_BROKER_TRANSPORT_MECHANISM_R8@1.0.0",
            MECHANISM_REVISION,
        )

    def test_r8_03_r7_python_socket_substitute_before_issue_cannot_change_deny(self):
        fake = self.patch_python_socket()
        before = native_transport_success_count()
        receipt = self.denial("socket-before-issue")
        self.assertEqual(
            DECISION_DENY,
            validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(0, fake.calls)
        self.assertGreaterEqual(native_transport_success_count(), before + 2)

    def test_r8_04_r7_python_socket_substitute_after_issue_cannot_change_deny(self):
        receipt = self.denial("socket-after-issue")
        fake = self.patch_python_socket()
        before = native_transport_success_count()
        self.assertEqual(
            DECISION_DENY,
            validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(0, fake.calls)
        self.assertGreaterEqual(native_transport_success_count(), before + 1)

    def test_r8_05_python_socket_substitute_during_repeated_validation_is_irrelevant(self):
        receipt = self.positive()
        fake = self.patch_python_socket()
        results = [
            validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)
            for _ in range(6)
        ]
        self.assertEqual([DECISION_PERMIT] * 6, results)
        self.assertEqual(0, fake.calls)

    def test_r8_06_socket_constructor_replacement_before_module_import_is_irrelevant(self):
        output = self.run_isolated(
            """
            import json, socket
            import _socket
            class Fake:
                calls = 0
                def __init__(self, *a, **k):
                    type(self).calls += 1
                    raise RuntimeError('python socket constructor should not run')
            socket.socket = Fake
            _socket.socket = Fake
            import causal_use_permission_candidate_r8 as c
            r = c.issue_noncurrent_synthetic_receipt(
                scope=c.REGISTERED_POSITIVE_SCOPE,
                basis_id='NONCURRENT_SYNTHETIC::basis::preimport-deny',
            )
            result = c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
            r.close()
            print(json.dumps({'decision': result, 'calls': Fake.calls}))
            """
        )
        result = json.loads(output)
        self.assertEqual(DECISION_DENY, result["decision"])
        self.assertEqual(0, result["calls"])

    def test_r8_07_native_transport_does_not_expose_reconfiguration_surface(self):
        self.assertFalse(hasattr(candidate._native, "configure_transport"))
        with self.assertRaises(RuntimeError):
            candidate._native.start_broker("/tmp/not-the-source-broker.py")

    def test_r8_08_candidate_has_no_python_socket_transport_dependency(self):
        names = set(candidate.__dict__)
        self.assertNotIn("socket", names)
        self.assertNotIn("_socket", names)
        source = Path(candidate.__file__).read_text(encoding="utf-8")
        self.assertNotIn("socket.socket", source)
        native_source = Path(candidate.__file__).with_name("obl058_r8_native_part1.inc").read_text(encoding="utf-8")
        self.assertIn("SO_PEERCRED", native_source)
        self.assertIn("connect(fd", native_source)
        self.assertIn("send_all", native_source)
        self.assertNotIn("PyImport_ImportModule(\"socket\")", native_source)

    def test_r8_09_native_generation_is_not_weakref_or_python_attribute_controlled(self):
        receipt = self.positive()
        with self.assertRaises(TypeError):
            weakref.ref(receipt)
        with self.assertRaises(TypeError):
            weakref.finalize(receipt, lambda: None)
        self.assertFalse(hasattr(receipt, "authority_key"))
        self.assertFalse(hasattr(receipt, "_authority_key"))
        self.assertFalse(hasattr(receipt, "__dict__"))
        with self.assertRaises(AttributeError):
            object.__setattr__(receipt, "authority_key", 1)

    def test_r8_10_reference_release_keeps_live_native_generation_reserved(self):
        baseline = native_lifetime_reservation_count()
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        self.assertEqual(baseline + 1, native_lifetime_reservation_count())
        del receipt
        gc.collect()
        self.assertEqual(baseline + 1, native_lifetime_reservation_count())

    def test_r8_11_explicit_close_revokes_before_reservation_release_and_duplicate_is_idempotent(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        before_pins = native_lifetime_reservation_count()
        before_closes = native_successful_close_count()
        self.assertTrue(receipt.close())
        self.assertEqual(before_pins - 1, native_lifetime_reservation_count())
        self.assertEqual(before_closes + 1, native_successful_close_count())
        self.assert_origin_rejected(receipt)
        self.assertFalse(receipt.close())
        self.assert_origin_rejected(receipt)

    def test_r8_12_bounded_issue_close_cycles_return_native_reservation_to_baseline(self):
        baseline = native_lifetime_reservation_count()
        for index in range(30):
            basis = (
                REGISTERED_POSITIVE_BASIS_ID
                if index % 2 == 0
                else f"NONCURRENT_SYNTHETIC::basis::cycle-{index}"
            )
            expected = DECISION_PERMIT if index % 2 == 0 else DECISION_DENY
            receipt = issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE, basis_id=basis
            )
            self.assertEqual(
                expected,
                validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
            )
            self.assertTrue(receipt.close())
        gc.collect()
        self.assertEqual(baseline, native_lifetime_reservation_count())

    def test_r8_13_direct_constructor_object_new_subclass_and_mapping_forms_reject(self):
        self.assert_origin_rejected(IssuedReceipt())
        try:
            fabricated = object.__new__(IssuedReceipt)
        except TypeError:
            fabricated = None
        if fabricated is not None:
            self.assert_origin_rejected(fabricated)

        class Derived(IssuedReceipt):
            pass

        self.assert_origin_rejected(Derived())
        receipt = self.positive()
        self.assert_origin_rejected(dict(receipt))
        self.assert_origin_rejected(CallerProxy(dict(receipt)))
        self.assert_origin_rejected(json.loads(json.dumps(dict(receipt))))

    def test_r8_14_copy_deepcopy_and_pickle_reject(self):
        receipt = self.positive()
        for operation in (
            lambda: copy.copy(receipt),
            lambda: copy.deepcopy(receipt),
            lambda: pickle.dumps(receipt),
        ):
            with self.subTest(operation=operation):
                with self.assertRaises(TypeError):
                    operation()

    def test_r8_15_equal_semantic_inputs_have_distinct_authority_instances(self):
        first = self.positive()
        second = self.positive()
        self.assertNotEqual(first["authority_instance_id"], second["authority_instance_id"])
        self.assertNotEqual(first["receipt_digest"], second["receipt_digest"])

    def test_r8_16_cross_scope_validation_rejects_all_five_fields(self):
        receipt = self.positive()
        replacements = {
            "actor_id": "NONCURRENT_SYNTHETIC::actor::other",
            "world_id": "NONCURRENT_SYNTHETIC::world::other",
            "subject_id": "NONCURRENT_SYNTHETIC::subject::other",
            "time_id": "NONCURRENT_SYNTHETIC::time::other",
            "transition_id": "NONCURRENT_SYNTHETIC::transition::other",
        }
        for field, value in replacements.items():
            with self.subTest(field=field):
                self.assert_origin_rejected(receipt, self.changed_scope(field, value))

    def test_r8_17_registered_basis_is_exactly_bound_across_all_five_fields(self):
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
                receipt = issue_noncurrent_synthetic_receipt(
                    scope=scope, basis_id=REGISTERED_POSITIVE_BASIS_ID
                )
                self.addCleanup(receipt.close)
                self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=scope))

    def test_r8_18_project_current_shaped_scope_and_current_canary_reject(self):
        replacements = {
            "actor_id": "urn:rawlsing:v3:actor:project-current:a",
            "world_id": "urn:rawlsing:v3:world:project-current:w",
            "subject_id": CURRENT_FIRST_CANARY_SUBJECT,
            "time_id": "urn:rawlsing:v3:time:project-current:t",
            "transition_id": "urn:rawlsing:v3:transition:project-current:tr",
        }
        for field, value in replacements.items():
            with self.subTest(field=field):
                with self.assertRaises(PermissionContractError):
                    issue_noncurrent_synthetic_receipt(
                        scope=self.changed_scope(field, value),
                        basis_id=REGISTERED_POSITIVE_BASIS_ID,
                    )

    def test_r8_19_wrong_fixture_and_empty_basis_fail_closed(self):
        with self.assertRaises(PermissionContractError):
            issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id=REGISTERED_POSITIVE_BASIS_ID,
                fixture_class="PROJECT_CURRENT",
            )
        with self.assertRaises(PermissionContractError):
            issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE, basis_id="   "
            )

    def test_r8_20_surrogate_basis_strings_remain_deny(self):
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

    def _fork_result(self, receipt, *, do_close=False):
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

    def test_r8_21_forked_permit_and_deny_copies_reject_parent_remains_valid(self):
        for label, receipt, expected in (
            ("permit", self.positive(), DECISION_PERMIT),
            ("deny", self.denial("fork"), DECISION_DENY),
        ):
            with self.subTest(label=label):
                self.assertEqual("REJECTED", self._fork_result(receipt))
                self.assertEqual(
                    expected,
                    validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
                )

    def test_r8_22_forked_close_cannot_retire_parent(self):
        receipt = self.positive()
        self.assertEqual("REJECTED", self._fork_result(receipt, do_close=True))
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_r8_23_repeated_and_concurrent_same_process_validation_is_stable(self):
        receipt = self.positive()
        self.assertEqual(
            [DECISION_PERMIT] * 6,
            [
                validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)
                for _ in range(6)
            ],
        )
        with ThreadPoolExecutor(max_workers=5) as pool:
            results = list(
                pool.map(
                    lambda _: validate_receipt(
                        receipt, expected_scope=REGISTERED_POSITIVE_SCOPE
                    ),
                    range(12),
                )
            )
        self.assertEqual([DECISION_PERMIT] * 12, results)

    def test_r8_24_alias_import_reuses_native_transport_but_keeps_receipt_types_separate(self):
        spec = importlib.util.spec_from_file_location("obl058_r8_alias", candidate.__file__)
        alias = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = alias
        self.addCleanup(sys.modules.pop, spec.name, None)
        assert spec.loader is not None
        spec.loader.exec_module(alias)
        first = self.positive()
        second = alias.issue_noncurrent_synthetic_receipt(
            scope=alias.REGISTERED_POSITIVE_SCOPE,
            basis_id=alias.REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(second.close)
        self.assertEqual(
            DECISION_PERMIT,
            alias.validate_receipt(second, expected_scope=alias.REGISTERED_POSITIVE_SCOPE),
        )
        with self.assertRaises(Exception):
            alias.validate_receipt(first, expected_scope=alias.REGISTERED_POSITIVE_SCOPE)
        with self.assertRaises(Exception):
            validate_receipt(second, expected_scope=REGISTERED_POSITIVE_SCOPE)

    def test_r8_25_python_module_rebinding_after_import_cannot_replace_native_transport(self):
        fake = self.patch_python_socket()
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id="NONCURRENT_SYNTHETIC::basis::module-rebind-deny",
        )
        self.addCleanup(receipt.close)
        self.assertEqual(
            DECISION_DENY,
            validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(0, fake.calls)

    def test_r8_26_broker_loss_fails_closed(self):
        output = self.run_isolated(
            """
            import os, signal, time
            import causal_use_permission_candidate_r8 as c
            r = c.issue_noncurrent_synthetic_receipt(
                scope=c.REGISTERED_POSITIVE_SCOPE,
                basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
            )
            pid = c.native_broker_pid()
            os.kill(pid, signal.SIGTERM)
            for _ in range(200):
                if not os.path.exists(f'/proc/{pid}'):
                    break
                time.sleep(0.01)
            try:
                c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
                print('ACCEPTED')
            except Exception:
                print('REJECTED')
            """
        )
        self.assertEqual("REJECTED", output)

    def test_r8_27_authority_child_loss_fails_closed(self):
        output = self.run_isolated(
            """
            import os, signal, time
            import causal_use_permission_candidate_r8 as c
            r = c.issue_noncurrent_synthetic_receipt(
                scope=c.REGISTERED_POSITIVE_SCOPE,
                basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
            )
            broker = c.native_broker_pid()
            child_file = f'/proc/{broker}/task/{broker}/children'
            children = []
            for _ in range(200):
                try:
                    children = [int(v) for v in open(child_file).read().split()]
                except FileNotFoundError:
                    children = []
                if children:
                    break
                time.sleep(0.01)
            if not children:
                raise RuntimeError('authority child not observed')
            os.kill(children[-1], signal.SIGTERM)
            time.sleep(0.05)
            try:
                c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
                print('ACCEPTED')
            except Exception:
                print('REJECTED')
            """
        )
        self.assertEqual("REJECTED", output)

    def test_r8_28_unrelated_same_user_endpoint_replacement_cannot_validate(self):
        output = self.run_isolated(
            """
            import os, signal, socket, time
            import causal_use_permission_candidate_r8 as c
            r = c.issue_noncurrent_synthetic_receipt(
                scope=c.REGISTERED_POSITIVE_SCOPE,
                basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
            )
            pid = c.native_broker_pid()
            path = c.native_broker_socket_path()
            os.kill(pid, signal.SIGTERM)
            for _ in range(200):
                if not os.path.exists(f'/proc/{pid}'):
                    break
                time.sleep(0.01)
            try:
                os.unlink(path)
            except FileNotFoundError:
                pass
            server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            server.bind(path)
            server.listen(1)
            try:
                c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
                print('ACCEPTED')
            except Exception:
                print('REJECTED')
            finally:
                server.close()
            """
        )
        self.assertEqual("REJECTED", output)

    def test_r8_29_native_response_request_identity_check_is_present(self):
        source = Path(candidate.__file__).with_name("obl058_r8_native_part1.inc").read_text(encoding="utf-8")
        self.assertIn("authority_broker_response_mismatch", source)
        self.assertIn("PyObject_RichCompareBool(request_id, response_id", source)
        self.assertIn("response_instance_id", Path(candidate.__file__).read_text(encoding="utf-8"))

    def test_r8_30_no_public_registration_or_project_current_effect_surfaces(self):
        names = set(candidate.__dict__)
        for name in (
            "register_source_basis",
            "execute_obl055",
            "install_obl056_positive",
            "create_encounter",
            "realize_oee",
            "create_actor",
            "activate_actor",
            "unblock_obl061",
        ):
            self.assertNotIn(name, names)


if __name__ == "__main__":
    unittest.main(verbosity=2)
