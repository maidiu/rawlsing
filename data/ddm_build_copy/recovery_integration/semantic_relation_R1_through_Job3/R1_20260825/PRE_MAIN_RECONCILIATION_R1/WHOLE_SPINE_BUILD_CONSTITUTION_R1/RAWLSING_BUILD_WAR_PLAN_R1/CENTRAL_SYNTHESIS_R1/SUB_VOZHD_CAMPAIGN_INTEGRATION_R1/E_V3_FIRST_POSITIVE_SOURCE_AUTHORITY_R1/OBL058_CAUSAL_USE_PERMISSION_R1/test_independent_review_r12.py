"""Fresh distinct independent review for frozen OBL058 R12.

This surface is review-only.  It does not modify or repair the frozen R12
candidate.  Producer tests are not imported as the independent finding.
"""
from __future__ import annotations

import copy
from concurrent.futures import ThreadPoolExecutor
import gc
import hashlib
import importlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import pickle
import shlex
import socket
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

import causal_use_permission_candidate_r12 as c  # noqa: E402

CANARY = (
    "urn:rawlsing:v3:subject:sha256:"
    "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
)


# A materially distinct native capability used only inside an isolated fresh
# process.  It exposes genuine CPython built-in module methods at the exact
# names R12 authenticates and returns a callable client whose identity property
# corresponds to its bound public_validate object, but it is not compiled from
# the frozen R12 capability source and always returns PERMIT.
SUBSTITUTE_CAPABILITY_C = r'''
#define PY_SSIZE_T_CLEAN
#include <Python.h>

typedef struct {
    PyObject_HEAD
    PyObject *capability;
} ReviewClient;

static void review_client_dealloc(ReviewClient *self) {
    Py_CLEAR(self->capability);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *review_client_call(PyObject *self, PyObject *args, PyObject *kwargs) {
    (void)self; (void)args; (void)kwargs;
    return PyUnicode_FromString("PERMIT");
}

static PyObject *review_client_identity(ReviewClient *self, void *closure) {
    (void)closure;
    return PyLong_FromVoidPtr((void *)self->capability);
}

static PyGetSetDef review_client_getset[] = {
    {"retained_capability_identity", (getter)review_client_identity, NULL, NULL, NULL},
    {NULL, NULL, NULL, NULL, NULL}
};

static PyTypeObject ReviewClientType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "_obl058_r12_authority_client.AuthorityClient",
    .tp_basicsize = sizeof(ReviewClient),
    .tp_dealloc = (destructor)review_client_dealloc,
    .tp_call = review_client_call,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_getset = review_client_getset,
};

static PyObject *review_public_validate(PyObject *module, PyObject *args, PyObject *kwargs) {
    (void)module; (void)args; (void)kwargs;
    return PyUnicode_FromString("PERMIT");
}

static PyObject *review_establish(PyObject *module, PyObject *args) {
    if (!PyTuple_Check(args) || PyTuple_GET_SIZE(args) != 5) {
        PyErr_SetString(PyExc_TypeError, "five_arguments_required");
        return NULL;
    }
    PyObject *module_dict = PyModule_GetDict(module);
    if (module_dict == NULL) return NULL;
    PyObject *capability = PyDict_GetItemString(module_dict, "public_validate");
    if (capability == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "public_validate_missing");
        return NULL;
    }
    ReviewClient *client = PyObject_New(ReviewClient, &ReviewClientType);
    if (client == NULL) return NULL;
    client->capability = Py_NewRef(capability);
    return (PyObject *)client;
}

static PyMethodDef review_methods[] = {
    {"establish_authority_client", (PyCFunction)review_establish, METH_VARARGS, NULL},
    {"public_validate", (PyCFunction)(void(*)(void))review_public_validate, METH_VARARGS | METH_KEYWORDS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef review_module = {
    PyModuleDef_HEAD_INIT,
    "_obl058_r12_authority_client",
    "Independent-review native cache substitute.",
    -1,
    review_methods
};

PyMODINIT_FUNC PyInit__obl058_r12_authority_client(void) {
    if (PyType_Ready(&ReviewClientType) < 0) return NULL;
    return PyModule_Create(&review_module);
}
'''


class OBL058R12FreshIndependentReview(unittest.TestCase):
    def setUp(self):
        self.client = c.AUTHORITY_CLIENT

    def positive(self):
        receipt = c.issue_noncurrent_synthetic_receipt(
            scope=c.REGISTERED_POSITIVE_SCOPE,
            basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(receipt.close)
        return receipt

    def negative(self, suffix: str = "independent-negative"):
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

    def reject(self, receipt, scope=None):
        with self.assertRaises(c.PermissionContractError):
            self.client(receipt, expected_scope=scope or c.REGISTERED_POSITIVE_SCOPE)

    def isolated(self, body: str, *, fresh_tmp: bool = False, timeout: int = 120) -> str:
        script = f"import sys\nsys.path.insert(0,{str(HERE)!r})\n" + textwrap.dedent(body)
        env = os.environ.copy()
        if fresh_tmp:
            with tempfile.TemporaryDirectory(prefix="obl058-r12-independent-") as tmp:
                env["TMPDIR"] = tmp
                result = subprocess.run(
                    [sys.executable, "-c", script],
                    cwd=HERE,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=env,
                    timeout=timeout,
                )
        else:
            result = subprocess.run(
                [sys.executable, "-c", script],
                cwd=HERE,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                timeout=timeout,
            )
        if result.returncode:
            self.fail(
                f"isolated rc={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}"
            )
        return result.stdout.strip()

    def test_i01_genuine_positive_negative_exact_identities_and_native_path(self):
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0", c.AUTHORITY_ID)
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0", c.SCHEMA_VERSION)
        self.assertEqual("NONCURRENT_SYNTHETIC", c.FIXTURE_CLASS)
        self.assertEqual("PERMIT", c.DECISION_PERMIT)
        self.assertEqual("DENY", c.DECISION_DENY)
        self.assertEqual(
            "OBL058_CAUSAL_USE_PERMISSION_AUTHORITY_CLIENT_BOUNDARY_R12@1.0.0",
            c.MECHANISM_REVISION,
        )
        self.assertEqual(
            "EXPLICIT_SOURCE_OWNED_CAUSAL_USE_PERMISSION", c.SOURCE_BASIS_KIND
        )
        positive = self.positive()
        negative = self.negative("i01")
        before = c.native_transport_success_count()
        self.assertEqual(
            c.DECISION_PERMIT,
            self.client(positive, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )
        mid = c.native_transport_success_count()
        self.assertEqual(
            c.DECISION_DENY,
            self.client(negative, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )
        after = c.native_transport_success_count()
        self.assertGreater(mid, before)
        self.assertGreater(after, mid)

    def test_i02_saved_client_exact_capability_survives_module_export_and_class_mediation(self):
        client = self.client
        cap = c._verified_public_validate
        cap_module = c._capability_module
        candidate_module = sys.modules[c.__name__]
        builtin_type = [].append.__class__
        self.assertIs(cap.__class__, builtin_type)
        self.assertIs(cap.__self__, cap_module)
        self.assertEqual(id(cap), client.retained_capability_identity)
        self.assertIs(c.AUTHORITY_CLIENT, c._retained_authority_client)
        self.assertFalse(hasattr(client, "__dict__"))

        negative = self.negative("module-mediation")
        positive = self.positive()
        candidate_class = candidate_module.__class__
        capability_class = cap_module.__class__
        originals = {
            "AUTHORITY_CLIENT": candidate_module.__dict__["AUTHORITY_CLIENT"],
            "_retained_authority_client": candidate_module.__dict__["_retained_authority_client"],
            "_verified_public_validate": candidate_module.__dict__["_verified_public_validate"],
            "cap_validate": cap_module.__dict__["public_validate"],
            "cap_establish": cap_module.__dict__["establish_authority_client"],
        }
        mediated = []

        class CandidateMediation(types.ModuleType):
            def __getattribute__(self, name):
                if name in {"AUTHORITY_CLIENT", "_retained_authority_client", "_verified_public_validate"}:
                    mediated.append("candidate:" + name)
                    return lambda *a, **k: c.DECISION_PERMIT
                return super().__getattribute__(name)

        class CapabilityMediation(types.ModuleType):
            def __getattribute__(self, name):
                if name in {"public_validate", "establish_authority_client"}:
                    mediated.append("capability:" + name)
                    return lambda *a, **k: c.DECISION_PERMIT
                return super().__getattribute__(name)

        fake = lambda *a, **k: c.DECISION_PERMIT
        candidate_module.__class__ = CandidateMediation
        cap_module.__class__ = CapabilityMediation
        candidate_module.__dict__["AUTHORITY_CLIENT"] = fake
        candidate_module.__dict__["_retained_authority_client"] = fake
        candidate_module.__dict__["_verified_public_validate"] = fake
        cap_module.__dict__["public_validate"] = fake
        cap_module.__dict__["establish_authority_client"] = fake
        try:
            before = c.native_transport_success_count()
            self.assertEqual(c.DECISION_DENY, client(negative, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            self.assertEqual(c.DECISION_PERMIT, client(positive, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            self.assertGreaterEqual(c.native_transport_success_count(), before + 2)
            self.assertEqual(id(cap), client.retained_capability_identity)
            self.assertEqual([], mediated)
        finally:
            candidate_module.__class__ = candidate_class
            cap_module.__class__ = capability_class
            candidate_module.__dict__["AUTHORITY_CLIENT"] = originals["AUTHORITY_CLIENT"]
            candidate_module.__dict__["_retained_authority_client"] = originals["_retained_authority_client"]
            candidate_module.__dict__["_verified_public_validate"] = originals["_verified_public_validate"]
            cap_module.__dict__["public_validate"] = originals["cap_validate"]
            cap_module.__dict__["establish_authority_client"] = originals["cap_establish"]

    def test_i03_saved_client_survives_sys_modules_alias_fresh_import_and_reload_resolution(self):
        out = self.isolated(r'''
            import importlib, json, sys, types
            import causal_use_permission_candidate_r12 as c
            client = c.AUTHORITY_CLIENT
            scope = c.REGISTERED_POSITIVE_SCOPE
            receipt = c.issue_noncurrent_synthetic_receipt(
                scope=scope,
                basis_id="NONCURRENT_SYNTHETIC::basis::fresh-resolution-negative",
            )
            genuine_candidate = sys.modules[c.__name__]
            genuine_cap = sys.modules[c._CAPABILITY_NAME]
            fake = types.ModuleType(c.__name__)
            fake.AUTHORITY_CLIENT = lambda *a, **k: "PERMIT"
            sys.modules[c.__name__] = fake
            sys.modules[c._CAPABILITY_NAME] = types.ModuleType(c._CAPABILITY_NAME)
            sys.modules["obl058_r12_alias"] = fake
            namespace = {}
            exec("from causal_use_permission_candidate_r12 import AUTHORITY_CLIENT as later", namespace)
            later = namespace["later"]
            substituted_discovery = later(receipt, expected_scope=scope)
            first = client(receipt, expected_scope=scope)
            sys.modules[c.__name__] = genuine_candidate
            sys.modules[c._CAPABILITY_NAME] = genuine_cap
            try:
                importlib.reload(genuine_candidate)
            except Exception:
                reload_state = "FAIL_CLOSED"
            else:
                reload_state = "RELOADED"
            second = client(receipt, expected_scope=scope)
            print(json.dumps([substituted_discovery, first, reload_state, second]))
            receipt.close()
        ''')
        values = json.loads(out)
        self.assertEqual("PERMIT", values[0])
        self.assertEqual(c.DECISION_DENY, values[1])
        self.assertIn(values[2], {"FAIL_CLOSED", "RELOADED"})
        self.assertEqual(c.DECISION_DENY, values[3])

    def test_i04_receipt_class_descriptor_instance_and_subclass_surfaces_are_non_authoritative(self):
        negative = self.negative("receipt-surfaces")
        positive = self.positive()
        receipt_type = c.IssuedReceipt
        class_dict = receipt_type.__dict__
        sentinel = object()
        old_validate = class_dict.get("_source_validate", sentinel)
        old_body = class_dict.get("_body_json_copy", sentinel)
        old_getattribute = class_dict.get("__getattribute__", sentinel)
        observed = []

        def fake_validate(self, scope):
            observed.append("validate")
            return c.DECISION_PERMIT, "substitute"

        def fake_body(self):
            observed.append("body")
            return '{"authority_instance_id":"substitute"}'

        def fake_getattribute(self, name):
            if name in {"_source_validate", "_body_json_copy", "decision"}:
                observed.append("get:" + name)
                if name == "_source_validate":
                    return fake_validate.__get__(self, receipt_type)
                if name == "_body_json_copy":
                    return fake_body.__get__(self, receipt_type)
                return c.DECISION_PERMIT
            return object.__getattribute__(self, name)

        receipt_type._source_validate = fake_validate
        receipt_type._body_json_copy = fake_body
        receipt_type.__getattribute__ = fake_getattribute
        try:
            self.assertEqual(c.DECISION_DENY, self.client(negative, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            self.assertEqual(c.DECISION_PERMIT, self.client(positive, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            self.assertEqual([], observed)
            with self.assertRaises((AttributeError, TypeError)):
                negative._source_validate = fake_validate
        finally:
            for name, old in (
                ("_source_validate", old_validate),
                ("_body_json_copy", old_body),
                ("__getattribute__", old_getattribute),
            ):
                if old is sentinel:
                    delattr(receipt_type, name)
                else:
                    setattr(receipt_type, name, old)

        class Derived(receipt_type):
            def _source_validate(self, scope):
                return c.DECISION_PERMIT, "substitute"

        self.reject(Derived())
        with self.assertRaises(TypeError):
            c._native.NativeReceiptBase._source_validate = fake_validate

    def test_i05_client_receipt_construction_reconstruction_copy_and_serialization_are_non_authoritative(self):
        client_type = type(self.client)
        with self.assertRaises(TypeError):
            client_type()
        with self.assertRaises(TypeError):
            object.__new__(client_type)
        with self.assertRaises(TypeError):
            class DerivedClient(client_type):
                pass
        with self.assertRaises((AttributeError, TypeError)):
            self.client.retained_capability_identity = 1
        with self.assertRaises(TypeError):
            weakref.ref(self.client)
        for operation in (
            lambda: copy.copy(self.client),
            lambda: copy.deepcopy(self.client),
            lambda: pickle.dumps(self.client),
            lambda: json.dumps(self.client),
        ):
            with self.assertRaises(TypeError):
                operation()

        receipt = self.positive()
        self.reject(c.IssuedReceipt())
        try:
            constructed = object.__new__(c.IssuedReceipt)
        except TypeError:
            constructed = None
        if constructed is not None:
            self.reject(constructed)

        class DerivedReceipt(c.IssuedReceipt):
            pass

        self.reject(DerivedReceipt())
        body = dict(receipt)
        self.reject(body)
        self.reject(types.MappingProxyType(body))
        self.reject(json.loads(json.dumps(body)))
        class MappingLookalike(dict):
            pass
        self.reject(MappingLookalike(body))
        for operation in (
            lambda: copy.copy(receipt),
            lambda: copy.deepcopy(receipt),
            lambda: pickle.dumps(receipt),
        ):
            with self.assertRaises(TypeError):
                operation()

    def test_i06_exact_scope_basis_noncurrent_and_caller_metadata_controls(self):
        for field, prefix in c._SCOPE_PREFIXES.items():
            wrong_expected = self.changed_scope(field, prefix + "independent-wrong")
            self.reject(self.positive(), wrong_expected)
            changed_receipt = c.issue_noncurrent_synthetic_receipt(
                scope=wrong_expected,
                basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
            )
            self.addCleanup(changed_receipt.close)
            self.assertEqual(c.DECISION_DENY, self.client(changed_receipt, expected_scope=wrong_expected))

        for basis in (
            "ADP-010",
            "ADP-019::OCCURRENCE_ADMITTED",
            "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
            "ROUTED_TO_SAME_ENDPOINT",
            "COLOCATED_SAME_TIME_AND_PLACE",
            "NARRATIVE_PLAUSIBILITY",
            "NONCURRENT_SYNTHETIC::basis::surrogate",
        ):
            receipt = c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE, basis_id=basis)
            self.addCleanup(receipt.close)
            self.assertEqual(c.DECISION_DENY, self.client(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE))

        replacements = {
            "actor_id": "urn:rawlsing:v3:actor:project-current:a",
            "world_id": "urn:rawlsing:v3:world:project-current:w",
            "subject_id": CANARY,
            "time_id": "urn:rawlsing:v3:time:project-current:t",
            "transition_id": "urn:rawlsing:v3:transition:project-current:tr",
        }
        for field, value in replacements.items():
            with self.assertRaises(c.PermissionContractError):
                c.issue_noncurrent_synthetic_receipt(
                    scope=self.changed_scope(field, value),
                    basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
                )
        with self.assertRaises(c.PermissionContractError):
            c.issue_noncurrent_synthetic_receipt(
                scope=c.REGISTERED_POSITIVE_SCOPE,
                basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
                fixture_class="PROJECT_CURRENT",
            )

        negative = self.negative("caller-metadata")
        copied = dict(negative)
        copied["decision"] = c.DECISION_PERMIT
        copied["peer_decision"] = c.DECISION_PERMIT
        copied["peer_authority"] = c.AUTHORITY_ID
        self.reject(copied)
        self.assertEqual(c.DECISION_DENY, self.client(negative, expected_scope=c.REGISTERED_POSITIVE_SCOPE))

    def test_i07_equal_semantics_distinct_authority_identity_and_repeated_concurrent_stability(self):
        first = self.positive()
        second = self.positive()
        negative = self.negative("concurrent")
        self.assertNotEqual(first["authority_instance_id"], second["authority_instance_id"])
        self.assertNotEqual(first["receipt_digest"], second["receipt_digest"])
        self.assertEqual(first["scope"], second["scope"])
        before = c.native_transport_success_count()
        for _ in range(5):
            self.assertEqual(c.DECISION_PERMIT, self.client(first, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            self.assertEqual(c.DECISION_DENY, self.client(negative, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        jobs = [(first, c.DECISION_PERMIT), (negative, c.DECISION_DENY)] * 8
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(
                lambda pair: self.client(pair[0], expected_scope=c.REGISTERED_POSITIVE_SCOPE),
                jobs,
            ))
        self.assertEqual([expected for _, expected in jobs], results)
        self.assertGreaterEqual(c.native_transport_success_count(), before + 26)

    def test_i08_close_duplicate_close_stale_and_bounded_lifecycle_accounting(self):
        baseline = c.native_lifetime_reservation_count()
        close_before = c.native_successful_close_count()
        receipt = c.issue_noncurrent_synthetic_receipt(
            scope=c.REGISTERED_POSITIVE_SCOPE,
            basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
        )
        self.assertEqual(baseline + 1, c.native_lifetime_reservation_count())
        self.assertTrue(receipt.close())
        self.assertEqual(baseline, c.native_lifetime_reservation_count())
        self.assertEqual(close_before + 1, c.native_successful_close_count())
        self.reject(receipt)
        self.assertFalse(receipt.close())
        self.assertEqual(close_before + 1, c.native_successful_close_count())

        cycle_base = c.native_lifetime_reservation_count()
        for index in range(12):
            basis = c.REGISTERED_POSITIVE_BASIS_ID if index % 2 == 0 else f"NONCURRENT_SYNTHETIC::basis::cycle-{index}"
            expected = c.DECISION_PERMIT if index % 2 == 0 else c.DECISION_DENY
            item = c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE, basis_id=basis)
            self.assertEqual(expected, self.client(item, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            self.assertTrue(item.close())
        gc.collect()
        self.assertEqual(cycle_base, c.native_lifetime_reservation_count())

    def _fork_result(self, receipt, *, close: bool = False):
        if not hasattr(os, "fork"):
            self.skipTest("fork unavailable")
        rd, wr = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(rd)
            try:
                if close:
                    value = "CLOSED" if receipt.close() else "REJECTED"
                else:
                    self.client(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
                    value = "ACCEPTED"
            except Exception:
                value = "REJECTED"
            os.write(wr, value.encode("ascii"))
            os.close(wr)
            os._exit(0)
        os.close(wr)
        value = os.read(rd, 64).decode("ascii")
        os.close(rd)
        os.waitpid(pid, 0)
        return value

    def test_i09_requester_generation_fork_copy_child_close_and_parent_survival(self):
        for receipt, expected in (
            (self.positive(), c.DECISION_PERMIT),
            (self.negative("fork-negative"), c.DECISION_DENY),
        ):
            self.assertEqual("REJECTED", self._fork_result(receipt))
            self.assertEqual(expected, self.client(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        parent = self.positive()
        self.assertEqual("REJECTED", self._fork_result(parent, close=True))
        self.assertEqual(c.DECISION_PERMIT, self.client(parent, expected_scope=c.REGISTERED_POSITIVE_SCOPE))

    def test_i10_python_socket_constructors_remain_outside_native_transport(self):
        import _socket

        class ReplacementSocket:
            calls = 0
            def __init__(self, *args, **kwargs):
                type(self).calls += 1
                raise RuntimeError("python socket constructor should not be used")

        public_socket = socket.socket
        low_socket = _socket.socket
        socket.socket = ReplacementSocket
        _socket.socket = ReplacementSocket
        try:
            negative = self.negative("socket-negative")
            positive = self.positive()
            before = c.native_transport_success_count()
            self.assertEqual(c.DECISION_DENY, self.client(negative, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            self.assertEqual(c.DECISION_PERMIT, self.client(positive, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            self.assertEqual(0, ReplacementSocket.calls)
            self.assertGreaterEqual(c.native_transport_success_count(), before + 2)
        finally:
            socket.socket = public_socket
            _socket.socket = low_socket

    def test_i11_broker_loss_fails_closed(self):
        out = self.isolated(r'''
            import os, signal, time
            import causal_use_permission_candidate_r12 as c
            client = c.AUTHORITY_CLIENT
            receipt = c.issue_noncurrent_synthetic_receipt(
                scope=c.REGISTERED_POSITIVE_SCOPE,
                basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
            )
            pid = c.native_broker_pid()
            os.kill(pid, signal.SIGTERM)
            for _ in range(100):
                if not os.path.exists(f"/proc/{pid}"):
                    break
                time.sleep(0.01)
            try:
                client(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
            except Exception:
                print("REJECTED")
            else:
                print("ACCEPTED")
        ''')
        self.assertEqual("REJECTED", out)

    def test_i12_plain_python_capability_and_r9_native_cache_substitutes_fail_closed(self):
        cap = self.isolated(r'''
            import hashlib, importlib.machinery, sys, sysconfig, tempfile, types
            from pathlib import Path
            source = Path.cwd() / "obl058_r12_authority_client.c"
            digest = hashlib.sha256(source.read_bytes()).hexdigest()[:20]
            suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
            output = Path(tempfile.gettempdir()) / "rawlsing_obl058_r12_authority_client" / f"py{sys.version_info.major}{sys.version_info.minor}" / f"_obl058_r12_authority_client_{digest}{suffix}"
            m = types.ModuleType("_obl058_r12_authority_client")
            m.__file__ = str(output)
            m.__spec__ = importlib.machinery.ModuleSpec(m.__name__, None, origin=str(output))
            m.establish_authority_client = lambda *a: (lambda *x, **k: "PERMIT")
            m.public_validate = lambda *a, **k: "PERMIT"
            sys.modules[m.__name__] = m
            try:
                import causal_use_permission_candidate_r12
            except ImportError:
                print("REJECTED")
            else:
                print("ACCEPTED")
        ''', fresh_tmp=True)
        self.assertEqual("REJECTED", cap)

        native = self.isolated(r'''
            import hashlib, importlib.machinery, os, sys, sysconfig, tempfile, types
            from pathlib import Path
            here = Path.cwd()
            names = ("obl058_r8_native.c", "obl058_r8_native_part1.inc", "obl058_r8_native_part2.inc", "obl058_r8_native_part3.inc")
            digest = hashlib.sha256(b"".join((here / n).read_bytes() for n in names)).hexdigest()[:20]
            suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
            output = Path(tempfile.gettempdir()) / "rawlsing_obl058_r8_native" / f"py{sys.version_info.major}{sys.version_info.minor}" / f"_obl058_r8_native_{digest}{suffix}"
            m = types.ModuleType("_obl058_r8_native")
            m.__file__ = str(output)
            m.__spec__ = importlib.machinery.ModuleSpec(m.__name__, None, origin=str(output))
            for name in ("start_broker", "shutdown_broker", "transport_configured", "close_success_count", "pin_count", "transport_success_count", "broker_pid", "broker_path"):
                setattr(m, name, lambda *a, **k: None)
            class NativeReceiptBase: pass
            NativeReceiptBase.__module__ = m.__name__
            m.NativeReceiptBase = NativeReceiptBase
            sys.modules[m.__name__] = m
            try:
                import causal_use_permission_candidate_r12
            except ImportError:
                print("REJECTED")
            else:
                print("ACCEPTED")
        ''', fresh_tmp=True)
        self.assertEqual("REJECTED", native)

    def test_i13_native_capability_cache_substitute_is_accepted_and_can_fail_open(self):
        source_literal = repr(SUBSTITUTE_CAPABILITY_C)
        out = self.isolated(f'''
            import hashlib, json, shlex, subprocess, sys, sysconfig, tempfile
            from pathlib import Path
            here = Path.cwd()
            source = here / "obl058_r12_authority_client.c"
            digest = hashlib.sha256(source.read_bytes()).hexdigest()[:20]
            suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
            root = Path(tempfile.gettempdir()) / "rawlsing_obl058_r12_authority_client" / f"py{{sys.version_info.major}}{{sys.version_info.minor}}"
            root.mkdir(parents=True, exist_ok=True)
            output = root / f"_obl058_r12_authority_client_{{digest}}{{suffix}}"
            substitute_source = root / "independent_substitute.c"
            substitute_source.write_text({source_literal}, encoding="utf-8")
            linker = shlex.split(sysconfig.get_config_var("LDSHARED") or "cc -shared")
            include_dir = sysconfig.get_path("include")
            result = subprocess.run(
                linker + ["-fPIC", "-O2", "-std=c11", f"-I{{include_dir}}", str(substitute_source), "-o", str(output)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if result.returncode:
                raise SystemExit("substitute compile failed: " + result.stderr[-2000:])
            import causal_use_permission_candidate_r12 as c
            receipt = c.issue_noncurrent_synthetic_receipt(
                scope=c.REGISTERED_POSITIVE_SCOPE,
                basis_id="NONCURRENT_SYNTHETIC::basis::must-deny-native-cache-substitute",
            )
            before = c.native_transport_success_count()
            decision = c.AUTHORITY_CLIENT(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
            after = c.native_transport_success_count()
            payload = {{
                "decision": decision,
                "transport_delta": after - before,
                "identity_matches": c.AUTHORITY_CLIENT.retained_capability_identity == id(c._verified_public_validate),
                "capability_file": str(Path(c._capability_module.__file__).resolve()),
                "expected_file": str(output.resolve()),
                "builtin": c._verified_public_validate.__class__ is [].append.__class__,
                "bound": c._verified_public_validate.__self__ is c._capability_module,
            }}
            print(json.dumps(payload, sort_keys=True))
            receipt.close()
        ''', fresh_tmp=True)
        values = json.loads(out)
        # Green execution here intentionally reproduces the semantic blocker.
        self.assertEqual(c.DECISION_PERMIT, values["decision"])
        self.assertEqual(0, values["transport_delta"])
        self.assertTrue(values["identity_matches"])
        self.assertTrue(values["builtin"])
        self.assertTrue(values["bound"])
        self.assertEqual(values["expected_file"], values["capability_file"])

    def test_i14_no_public_registration_or_downstream_current_effect_surface_and_no_fail_all_genuine_controls(self):
        names = set(c.__dict__)
        self.assertNotIn("validate_receipt", names)
        self.assertIn("AUTHORITY_CLIENT", names)
        for name in (
            "register_source_basis",
            "register_basis",
            "set_source_basis",
            "execute_obl055",
            "install_obl056_positive",
            "create_encounter",
            "realize_oee",
            "create_actor",
            "activate_actor",
            "authority_index_add",
            "unblock_obl061",
        ):
            self.assertNotIn(name, names)
            self.assertFalse(hasattr(self.client, name))
        self.assertEqual(c.DECISION_PERMIT, self.client(self.positive(), expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        self.assertEqual(c.DECISION_DENY, self.client(self.negative("final-control"), expected_scope=c.REGISTERED_POSITIVE_SCOPE))


if __name__ == "__main__":
    unittest.main(verbosity=2)
