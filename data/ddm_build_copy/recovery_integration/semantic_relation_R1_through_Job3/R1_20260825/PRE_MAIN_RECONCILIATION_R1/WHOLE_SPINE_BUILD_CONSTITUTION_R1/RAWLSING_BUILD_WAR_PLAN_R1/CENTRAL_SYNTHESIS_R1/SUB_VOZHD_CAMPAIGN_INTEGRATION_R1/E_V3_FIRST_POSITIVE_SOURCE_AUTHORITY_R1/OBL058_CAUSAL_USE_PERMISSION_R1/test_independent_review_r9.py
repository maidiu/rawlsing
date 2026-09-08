"""Fresh distinct independent review court for frozen OBL058 R9.

Review-only. The frozen R9 candidate is not modified or repaired here. A green
court can reproduce a semantic blocker; disposition is recorded separately.
"""
from __future__ import annotations

import copy
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.machinery
import json
import os
from pathlib import Path
import pickle
import socket
import struct
import subprocess
import sys
import sysconfig
import tempfile
import textwrap
import types
import unittest
import weakref

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import causal_use_permission_candidate_r9 as c  # noqa: E402

CURRENT_FIRST_CANARY_SUBJECT = (
    "urn:rawlsing:v3:subject:sha256:"
    "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
)


class CallerProxy(dict):
    pass


class ReplacementSocket:
    calls = 0

    def __init__(self, *args, **kwargs):
        type(self).calls += 1
        raise RuntimeError("ordinary Python socket constructor must remain unused")


def _expected_native_output() -> Path:
    paths = [
        HERE / "obl058_r8_native.c",
        HERE / "obl058_r8_native_part1.inc",
        HERE / "obl058_r8_native_part2.inc",
        HERE / "obl058_r8_native_part3.inc",
    ]
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()[:20]
    suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
    return (
        Path(tempfile.gettempdir())
        / "rawlsing_obl058_r8_native"
        / f"py{sys.version_info.major}{sys.version_info.minor}"
        / f"_obl058_r8_native_{digest}{suffix}"
    )


def _ordinary_module_substitute() -> types.ModuleType:
    module = types.ModuleType(c._NATIVE_NAME)
    claimed = str(_expected_native_output().resolve())
    module.__file__ = claimed
    module.__spec__ = importlib.machinery.ModuleSpec(
        c._NATIVE_NAME, loader=None, origin=claimed
    )

    class NativeReceiptBase:
        def _source_issue(self, *args):
            return None

        def _source_validate(self, *args):
            return (c.DECISION_PERMIT, "ordinary-python-substitute")

        def _source_close(self):
            return True

        def _body_json_copy(self):
            return json.dumps({
                "decision": c.DECISION_PERMIT,
                "authority_instance_id": "ordinary-python-substitute",
            })

        def _is_source_issued(self):
            return True

    NativeReceiptBase.__module__ = c._NATIVE_NAME
    module.NativeReceiptBase = NativeReceiptBase
    module.start_broker = lambda path: None
    module.shutdown_broker = lambda: None
    module.transport_configured = lambda: True
    module.close_success_count = lambda: 0
    module.pin_count = lambda: 0
    module.transport_success_count = lambda: 0
    module.broker_pid = lambda: os.getpid()
    module.broker_path = lambda: "/tmp/ordinary-python-substitute.sock"
    return module


class OBL058R9IndependentReviewCourt(unittest.TestCase):
    def positive(self):
        receipt = c.issue_noncurrent_synthetic_receipt(
            scope=c.REGISTERED_POSITIVE_SCOPE,
            basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(receipt.close)
        return receipt

    def denial(self, suffix="review-deny"):
        receipt = c.issue_noncurrent_synthetic_receipt(
            scope=c.REGISTERED_POSITIVE_SCOPE,
            basis_id=f"NONCURRENT_SYNTHETIC::basis::{suffix}",
        )
        self.addCleanup(receipt.close)
        return receipt

    def changed_scope(self, field: str, value: str):
        values = c.REGISTERED_POSITIVE_SCOPE.canonical()
        values[field] = value
        return c.ExactScope(**values)

    def assert_rejected(self, receipt, scope=None):
        with self.assertRaises(c.PermissionContractError):
            c.validate_receipt(
                receipt,
                expected_scope=scope or c.REGISTERED_POSITIVE_SCOPE,
            )

    def isolated(self, body: str, timeout: int = 60) -> str:
        script = (
            "import sys\nfrom pathlib import Path\n"
            + f"sys.path.insert(0, {str(HERE)!r})\n"
            + textwrap.dedent(body)
        )
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=str(HERE),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        if result.returncode != 0:
            self.fail(
                f"isolated review process failed rc={result.returncode}\n"
                f"stdout={result.stdout}\nstderr={result.stderr}"
            )
        return result.stdout.strip()

    def test_review_01_genuine_positive_and_negative_controls(self):
        self.assertEqual(
            c.DECISION_PERMIT,
            c.validate_receipt(self.positive(), expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(
            c.DECISION_DENY,
            c.validate_receipt(self.denial(), expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )

    def test_review_02_exact_r8_import_cache_substitute_is_rejected(self):
        output = self.isolated(r'''
            import hashlib, importlib.machinery, os, sys, sysconfig, tempfile, types
            from pathlib import Path
            here = Path.cwd()
            names = ("obl058_r8_native.c", "obl058_r8_native_part1.inc", "obl058_r8_native_part2.inc", "obl058_r8_native_part3.inc")
            digest = hashlib.sha256(b"".join((here / name).read_bytes() for name in names)).hexdigest()[:20]
            suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
            path = Path(tempfile.gettempdir()) / "rawlsing_obl058_r8_native" / f"py{sys.version_info.major}{sys.version_info.minor}" / f"_obl058_r8_native_{digest}{suffix}"
            module = types.ModuleType("_obl058_r8_native")
            module.__file__ = str(path)
            module.__spec__ = importlib.machinery.ModuleSpec(module.__name__, None, origin=str(path))
            class NativeReceiptBase:
                def _source_issue(self, *a): return None
                def _source_validate(self, *a): return ("PERMIT", "fake")
                def _source_close(self): return True
                def _body_json_copy(self): return '{"authority_instance_id":"fake"}'
                def _is_source_issued(self): return True
            NativeReceiptBase.__module__ = module.__name__
            module.NativeReceiptBase = NativeReceiptBase
            module.start_broker=lambda p:None; module.shutdown_broker=lambda:None
            module.transport_configured=lambda:True; module.close_success_count=lambda:0
            module.pin_count=lambda:0; module.transport_success_count=lambda:0
            module.broker_pid=lambda:os.getpid(); module.broker_path=lambda:"/tmp/fake"
            sys.modules[module.__name__] = module
            try:
                import causal_use_permission_candidate_r9
            except ImportError:
                print("REJECTED")
            else:
                print("ACCEPTED")
        ''')
        self.assertEqual("REJECTED", output)
        with self.assertRaises(ImportError):
            c._verify_native_module(_ordinary_module_substitute(), c._native_output_path())

    def test_review_03_mutable_receipt_class_method_can_replace_native_decision(self):
        """Reproduce the smallest R9 blocker through the original public validator."""
        receipt = self.denial("class-method-dispatch")
        self.assertEqual(
            c.DECISION_DENY,
            c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )
        authority_instance_id = receipt["authority_instance_id"]
        before_transport = c.native_transport_success_count()

        def replacement_validate(self, expected_scope):
            return (c.DECISION_PERMIT, authority_instance_id)

        c.IssuedReceipt._source_validate = replacement_validate
        try:
            self.assertEqual(
                c.DECISION_PERMIT,
                c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
            self.assertEqual(before_transport, c.native_transport_success_count())
        finally:
            delattr(c.IssuedReceipt, "_source_validate")

        self.assertEqual(
            c.DECISION_DENY,
            c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )

    def test_review_04_genuine_native_binding_is_real_c_extension_binding(self):
        builtin_type = [].append.__class__
        for name in c._NATIVE_REQUIRED_FUNCTIONS:
            function = c._native.__dict__[name]
            self.assertIs(function.__class__, builtin_type)
            self.assertIs(function.__self__, c._native)
        self.assertEqual(c._NATIVE_NAME, c._native.NativeReceiptBase.__module__)
        self.assertEqual(
            str(_expected_native_output().resolve()),
            str(Path(c._native.__file__).resolve()),
        )

    def test_review_05_cache_replacement_after_genuine_binding_does_not_redirect_native_path(self):
        genuine = sys.modules[c._NATIVE_NAME]
        receipt = self.denial("cache-after-binding")
        sys.modules[c._NATIVE_NAME] = _ordinary_module_substitute()
        try:
            self.assertEqual(
                c.DECISION_DENY,
                c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
        finally:
            sys.modules[c._NATIVE_NAME] = genuine

    def test_review_06_python_socket_constructor_replacement_remains_irrelevant(self):
        import _socket

        public = socket.socket
        low = _socket.socket
        ReplacementSocket.calls = 0
        socket.socket = ReplacementSocket
        _socket.socket = ReplacementSocket
        try:
            receipt = self.denial("socket-replacement")
            self.assertEqual(
                c.DECISION_DENY,
                c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
            self.assertEqual(0, ReplacementSocket.calls)
        finally:
            socket.socket = public
            _socket.socket = low

    def test_review_07_close_and_native_lifetime_controls_remain_exact(self):
        receipt = c.issue_noncurrent_synthetic_receipt(
            scope=c.REGISTERED_POSITIVE_SCOPE,
            basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
        )
        with self.assertRaises(TypeError):
            weakref.ref(receipt)
        before_pins = c.native_lifetime_reservation_count()
        before_closes = c.native_successful_close_count()
        self.assertTrue(receipt.close())
        self.assertEqual(before_pins - 1, c.native_lifetime_reservation_count())
        self.assertEqual(before_closes + 1, c.native_successful_close_count())
        self.assert_rejected(receipt)
        self.assertFalse(receipt.close())

    def _fork_result(self, receipt, close=False):
        if not hasattr(os, "fork"):
            self.skipTest("fork unavailable")
        read_fd, write_fd = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(read_fd)
            try:
                if close:
                    result = "CLOSED" if receipt.close() else "REJECTED"
                else:
                    c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
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

    def test_review_08_forked_copies_reject_and_parent_survives(self):
        for receipt, expected in (
            (self.positive(), c.DECISION_PERMIT),
            (self.denial("fork-deny"), c.DECISION_DENY),
        ):
            self.assertEqual("REJECTED", self._fork_result(receipt))
            self.assertEqual(
                expected,
                c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
        receipt = self.positive()
        self.assertEqual("REJECTED", self._fork_result(receipt, close=True))
        self.assertEqual(
            c.DECISION_PERMIT,
            c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )

    def test_review_09_reconstruction_copy_and_cross_scope_reject(self):
        receipt = self.positive()
        self.assert_rejected(c.IssuedReceipt())

        class Derived(c.IssuedReceipt):
            pass

        self.assert_rejected(Derived())
        self.assert_rejected(dict(receipt))
        self.assert_rejected(CallerProxy(dict(receipt)))
        self.assert_rejected(json.loads(json.dumps(dict(receipt))))
        for operation in (
            lambda: copy.copy(receipt),
            lambda: copy.deepcopy(receipt),
            lambda: pickle.dumps(receipt),
        ):
            with self.assertRaises(TypeError):
                operation()
        for field, prefix in c._SCOPE_PREFIXES.items():
            with self.subTest(field=field):
                self.assert_rejected(receipt, self.changed_scope(field, prefix + "review-other"))

    def test_review_10_basis_scope_current_and_surrogate_controls(self):
        for field, prefix in c._SCOPE_PREFIXES.items():
            with self.subTest(field=field):
                scope = self.changed_scope(field, prefix + "review-changed")
                receipt = c.issue_noncurrent_synthetic_receipt(
                    scope=scope,
                    basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
                )
                self.addCleanup(receipt.close)
                self.assertEqual(
                    c.DECISION_DENY,
                    c.validate_receipt(receipt, expected_scope=scope),
                )

        current = {
            "actor_id": "urn:rawlsing:v3:actor:project-current:a",
            "world_id": "urn:rawlsing:v3:world:project-current:w",
            "subject_id": CURRENT_FIRST_CANARY_SUBJECT,
            "time_id": "urn:rawlsing:v3:time:project-current:t",
            "transition_id": "urn:rawlsing:v3:transition:project-current:tr",
        }
        for field, value in current.items():
            with self.subTest(field=field):
                with self.assertRaises(c.PermissionContractError):
                    c.issue_noncurrent_synthetic_receipt(
                        scope=self.changed_scope(field, value),
                        basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
                    )

        for basis in (
            "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
            "ADP-010",
            "ADP-019::OCCURRENCE_ADMITTED",
            "ROUTED_TO_SAME_ENDPOINT",
            "COLOCATED_SAME_TIME_AND_PLACE",
            "NARRATIVE_PLAUSIBILITY",
        ):
            with self.subTest(basis=basis):
                receipt = c.issue_noncurrent_synthetic_receipt(
                    scope=c.REGISTERED_POSITIVE_SCOPE,
                    basis_id=basis,
                )
                self.addCleanup(receipt.close)
                self.assertEqual(
                    c.DECISION_DENY,
                    c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
                )

    def test_review_11_equal_inputs_are_distinct_and_concurrency_is_stable(self):
        first = self.positive()
        second = self.positive()
        self.assertNotEqual(first["authority_instance_id"], second["authority_instance_id"])
        self.assertNotEqual(first["receipt_digest"], second["receipt_digest"])
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(
                lambda _: c.validate_receipt(
                    first, expected_scope=c.REGISTERED_POSITIVE_SCOPE
                ),
                range(12),
            ))
        self.assertEqual([c.DECISION_PERMIT] * 12, results)

    def test_review_12_no_public_registration_or_project_current_effect_surface(self):
        names = set(c.__dict__)
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
