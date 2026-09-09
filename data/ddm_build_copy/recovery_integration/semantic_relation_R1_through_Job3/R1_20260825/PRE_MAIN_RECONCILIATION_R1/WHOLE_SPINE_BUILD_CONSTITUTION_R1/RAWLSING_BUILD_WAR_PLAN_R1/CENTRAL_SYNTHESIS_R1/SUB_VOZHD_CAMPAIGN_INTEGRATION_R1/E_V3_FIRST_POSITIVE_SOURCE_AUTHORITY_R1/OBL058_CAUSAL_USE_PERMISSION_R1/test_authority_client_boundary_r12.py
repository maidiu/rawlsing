"""Producer governed verification for OBL058 R12 authority-client boundary.

Producer-side verification only. No self-review or independent review is
performed by this surface.
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
import signal
import socket
import subprocess
import sys
import sysconfig
import tempfile
import textwrap
import time
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


class ReviewProxy(dict):
    pass


class OBL058AuthorityClientBoundaryR12Court(unittest.TestCase):
    def setUp(self):
        self.client = c.AUTHORITY_CLIENT

    def positive(self):
        receipt = c.issue_noncurrent_synthetic_receipt(
            scope=c.REGISTERED_POSITIVE_SCOPE,
            basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(receipt.close)
        return receipt

    def denial(self, suffix="r12-deny"):
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
            self.client(
                receipt,
                expected_scope=scope or c.REGISTERED_POSITIVE_SCOPE,
            )

    def isolated(self, body: str, timeout: int = 90) -> str:
        script = f"import sys\nsys.path.insert(0,{str(HERE)!r})\n" + textwrap.dedent(body)
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=HERE,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        if result.returncode:
            self.fail(
                f"isolated rc={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}"
            )
        return result.stdout.strip()

    def test_r12_01_genuine_client_permit_deny_and_revision(self):
        before = c.native_transport_success_count()
        self.assertEqual(
            c.DECISION_PERMIT,
            self.client(self.positive(), expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(
            c.DECISION_DENY,
            self.client(self.denial(), expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )
        self.assertGreaterEqual(c.native_transport_success_count(), before + 2)
        self.assertEqual(
            "OBL058_CAUSAL_USE_PERMISSION_AUTHORITY_CLIENT_BOUNDARY_R12@1.0.0",
            c.MECHANISM_REVISION,
        )

    def test_r12_02_client_retains_exact_authenticated_capability_by_identity(self):
        builtin_type = [].append.__class__
        self.assertIs(c._establish_authority_client.__class__, builtin_type)
        self.assertIs(c._verified_public_validate.__class__, builtin_type)
        self.assertIs(c._establish_authority_client.__self__, c._capability_module)
        self.assertIs(c._verified_public_validate.__self__, c._capability_module)
        self.assertIs(c.AUTHORITY_CLIENT, c._retained_authority_client)
        self.assertEqual(
            id(c._verified_public_validate),
            self.client.retained_capability_identity,
        )
        self.assertEqual("_obl058_r12_authority_client", type(self.client).__module__)
        self.assertFalse(hasattr(self.client, "__dict__"))

    def test_r12_03_post_creation_module_exports_and_module_class_cannot_redirect_saved_client(self):
        receipt = self.denial("post-create-module")
        client = self.client
        expected = c.DECISION_DENY
        scope = c.REGISTERED_POSITIVE_SCOPE
        transport_count = c.native_transport_success_count
        candidate_module = sys.modules[c.__name__]
        capability_module = c._capability_module
        candidate_class = candidate_module.__class__
        capability_class = capability_module.__class__
        original = {
            "AUTHORITY_CLIENT": candidate_module.__dict__["AUTHORITY_CLIENT"],
            "_retained_authority_client": candidate_module.__dict__["_retained_authority_client"],
            "_verified_public_validate": candidate_module.__dict__["_verified_public_validate"],
            "_establish_authority_client": candidate_module.__dict__["_establish_authority_client"],
            "issue_noncurrent_synthetic_receipt": candidate_module.__dict__["issue_noncurrent_synthetic_receipt"],
            "cap_establish": capability_module.__dict__["establish_authority_client"],
            "cap_validate": capability_module.__dict__["public_validate"],
        }
        calls = []

        class MediatedCandidate(types.ModuleType):
            def __getattribute__(self, name):
                if name in {"AUTHORITY_CLIENT", "_retained_authority_client", "_verified_public_validate"}:
                    calls.append("candidate:" + name)
                    return lambda *a, **k: "PERMIT"
                return super().__getattribute__(name)

        class MediatedCapability(types.ModuleType):
            def __getattribute__(self, name):
                if name in {"establish_authority_client", "public_validate"}:
                    calls.append("capability:" + name)
                    return lambda *a, **k: "PERMIT"
                return super().__getattribute__(name)

        fake = lambda *a, **k: "PERMIT"
        candidate_module.__class__ = MediatedCandidate
        capability_module.__class__ = MediatedCapability
        candidate_module.__dict__["AUTHORITY_CLIENT"] = fake
        candidate_module.__dict__["_retained_authority_client"] = fake
        candidate_module.__dict__["_verified_public_validate"] = fake
        candidate_module.__dict__["_establish_authority_client"] = fake
        candidate_module.__dict__["issue_noncurrent_synthetic_receipt"] = fake
        capability_module.__dict__["establish_authority_client"] = fake
        capability_module.__dict__["public_validate"] = fake
        try:
            before = transport_count()
            self.assertEqual(expected, client(receipt, expected_scope=scope))
            self.assertGreater(transport_count(), before)
            self.assertEqual(id(original["_verified_public_validate"]), client.retained_capability_identity)
            self.assertEqual([], calls)
        finally:
            candidate_module.__class__ = candidate_class
            capability_module.__class__ = capability_class
            candidate_module.__dict__["AUTHORITY_CLIENT"] = original["AUTHORITY_CLIENT"]
            candidate_module.__dict__["_retained_authority_client"] = original["_retained_authority_client"]
            candidate_module.__dict__["_verified_public_validate"] = original["_verified_public_validate"]
            candidate_module.__dict__["_establish_authority_client"] = original["_establish_authority_client"]
            candidate_module.__dict__["issue_noncurrent_synthetic_receipt"] = original["issue_noncurrent_synthetic_receipt"]
            capability_module.__dict__["establish_authority_client"] = original["cap_establish"]
            capability_module.__dict__["public_validate"] = original["cap_validate"]

    def test_r12_04_fresh_module_name_resolution_is_not_the_authoritative_validation_contract(self):
        receipt = self.denial("fresh-name")
        client = self.client
        module_object = sys.modules[c.__name__]
        original_class = module_object.__class__
        genuine = module_object.__dict__["AUTHORITY_CLIENT"]
        fake = lambda *a, **k: c.DECISION_PERMIT

        class MediatedCandidate(types.ModuleType):
            def __getattribute__(self, name):
                if name == "AUTHORITY_CLIENT":
                    return fake
                return super().__getattribute__(name)

        module_object.__class__ = MediatedCandidate
        try:
            namespace = {}
            exec(
                "from causal_use_permission_candidate_r12 import AUTHORITY_CLIENT as later",
                namespace,
            )
            later = namespace["later"]
            self.assertIsNot(later, client)
            self.assertIs(module_object.__dict__["AUTHORITY_CLIENT"], genuine)
            self.assertIs(type(client), type(genuine))
            self.assertIsNot(type(later), type(client))
            self.assertEqual(
                c.DECISION_DENY,
                client(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
        finally:
            module_object.__class__ = original_class

    def test_r12_05_sys_modules_alias_reimport_reload_and_loader_state_do_not_redirect_saved_client(self):
        out = self.isolated(r'''
            import importlib, importlib.util, sys, types, json
            import causal_use_permission_candidate_r12 as c
            client=c.AUTHORITY_CLIENT
            scope=c.REGISTERED_POSITIVE_SCOPE
            receipt=c.issue_noncurrent_synthetic_receipt(scope=scope,basis_id="NONCURRENT_SYNTHETIC::basis::r12-cache-deny")
            genuine_candidate=sys.modules[c.__name__]
            genuine_cap=sys.modules[c._CAPABILITY_NAME]
            genuine_native=sys.modules[c._NATIVE_NAME]
            fake=types.SimpleNamespace(AUTHORITY_CLIENT=lambda *a,**k:"PERMIT")
            sys.modules[c.__name__]=fake
            sys.modules[c._CAPABILITY_NAME]=types.ModuleType(c._CAPABILITY_NAME)
            sys.modules[c._NATIVE_NAME]=types.ModuleType(c._NATIVE_NAME)
            sys.modules["obl058_r12_alias"]=fake
            first=client(receipt,expected_scope=scope)
            sys.modules[c.__name__]=genuine_candidate
            sys.modules[c._CAPABILITY_NAME]=genuine_cap
            sys.modules[c._NATIVE_NAME]=genuine_native
            reload_state="UNKNOWN"
            try: importlib.reload(genuine_candidate)
            except Exception: reload_state="FAIL_CLOSED"
            else: reload_state="RELOADED"
            second=client(receipt,expected_scope=scope)
            real=importlib.util.spec_from_file_location
            importlib.util.spec_from_file_location=lambda *a,**k: None
            try: third=client(receipt,expected_scope=scope)
            finally: importlib.util.spec_from_file_location=real
            print(json.dumps([first,reload_state,second,third,type(client).__name__]))
            receipt.close()
        ''')
        values = json.loads(out)
        self.assertEqual(c.DECISION_DENY, values[0])
        self.assertIn(values[1], {"FAIL_CLOSED", "RELOADED"})
        self.assertEqual(c.DECISION_DENY, values[2])
        self.assertEqual(c.DECISION_DENY, values[3])
        self.assertEqual("AuthorityClient", values[4])

    def test_r12_06_receipt_class_descriptor_and_instance_substitution_cannot_redirect_client(self):
        receipt = self.denial("receipt-substitution")
        client = self.client
        scope = c.REGISTERED_POSITIVE_SCOPE
        receipt_type = c.IssuedReceipt
        original_validate = receipt_type._source_validate
        original_body = receipt_type._body_json_copy
        calls = []

        def fake_validate(self, scope_dict):
            calls.append("validate")
            return c.DECISION_PERMIT, "fake"

        def fake_body(self):
            calls.append("body")
            return '{"authority_instance_id":"fake"}'

        receipt_type._source_validate = fake_validate
        receipt_type._body_json_copy = fake_body
        try:
            self.assertEqual(c.DECISION_DENY, client(receipt, expected_scope=scope))
            self.assertEqual([], calls)
            with self.assertRaises((AttributeError, TypeError)):
                receipt._source_validate = fake_validate
            with self.assertRaises(TypeError):
                c._native.NativeReceiptBase._source_validate = fake_validate
        finally:
            receipt_type._source_validate = original_validate
            receipt_type._body_json_copy = original_body

        class Derived(receipt_type):
            pass

        derived = Derived()
        self.reject(derived)
        try:
            receipt.__class__ = Derived
        except TypeError:
            pass
        else:
            try:
                self.reject(receipt)
            finally:
                receipt.__class__ = receipt_type

    def test_r12_07_native_client_type_is_nonforgeable_nonmutable_and_nonserializable(self):
        client = self.client
        client_type = type(client)
        with self.assertRaises(TypeError):
            client_type()
        with self.assertRaises(TypeError):
            object.__new__(client_type)
        with self.assertRaises(TypeError):
            setattr(client_type, "__call__", lambda *a, **k: c.DECISION_PERMIT)
        with self.assertRaises(TypeError):
            client.__class__ = object
        with self.assertRaises(TypeError):
            client.retained_capability_identity = 1
        with self.assertRaises(TypeError):
            weakref.ref(client)
        with self.assertRaises(TypeError):
            class DerivedClient(client_type):
                pass
        for operation in (
            lambda: copy.copy(client),
            lambda: copy.deepcopy(client),
            lambda: pickle.dumps(client),
            lambda: json.dumps(client),
        ):
            with self.assertRaises(TypeError):
                operation()

    def test_r12_08_plain_python_capability_cache_lookalike_rejects(self):
        out = self.isolated(r'''
            import hashlib, importlib.machinery, sys, sysconfig, tempfile, types
            from pathlib import Path
            source=Path.cwd()/"obl058_r12_authority_client.c"
            digest=hashlib.sha256(source.read_bytes()).hexdigest()[:20]
            suffix=sysconfig.get_config_var("EXT_SUFFIX") or ".so"
            output=Path(tempfile.gettempdir())/"rawlsing_obl058_r12_authority_client"/f"py{sys.version_info.major}{sys.version_info.minor}"/f"_obl058_r12_authority_client_{digest}{suffix}"
            m=types.ModuleType("_obl058_r12_authority_client")
            m.__file__=str(output); m.__spec__=importlib.machinery.ModuleSpec(m.__name__,None,origin=str(output))
            m.establish_authority_client=lambda *a: (lambda *x,**k:"PERMIT")
            m.public_validate=lambda *a,**k:"PERMIT"
            sys.modules[m.__name__]=m
            try: import causal_use_permission_candidate_r12
            except ImportError: print("REJECTED")
            else: print("ACCEPTED")
        ''')
        self.assertEqual("REJECTED", out)

    def test_r12_09_loader_produced_python_capability_fails_closed(self):
        out = self.isolated(r'''
            import importlib.machinery, importlib.util, types
            real=importlib.util.spec_from_file_location
            class Loader:
                def create_module(self,spec):
                    m=types.ModuleType(spec.name); m.__file__=str(spec.origin); return m
                def exec_module(self,m):
                    m.establish_authority_client=lambda *a:(lambda *x,**k:"PERMIT")
                    m.public_validate=lambda *a,**k:"PERMIT"
            importlib.util.spec_from_file_location=lambda name,path: importlib.machinery.ModuleSpec(name,Loader(),origin=str(path))
            try: import causal_use_permission_candidate_r12
            except Exception: print("REJECTED")
            else: print("ACCEPTED")
            finally: importlib.util.spec_from_file_location=real
        ''')
        self.assertEqual("REJECTED", out)

    def test_r12_10_r9_native_source_origin_and_import_cache_controls_remain_closed(self):
        out = self.isolated(r'''
            import hashlib, importlib.machinery, os, sys, sysconfig, tempfile, types
            from pathlib import Path
            here=Path.cwd(); names=("obl058_r8_native.c","obl058_r8_native_part1.inc","obl058_r8_native_part2.inc","obl058_r8_native_part3.inc")
            d=hashlib.sha256(b"".join((here/n).read_bytes() for n in names)).hexdigest()[:20]
            s=sysconfig.get_config_var("EXT_SUFFIX") or ".so"
            p=Path(tempfile.gettempdir())/"rawlsing_obl058_r8_native"/f"py{sys.version_info.major}{sys.version_info.minor}"/f"_obl058_r8_native_{d}{s}"
            m=types.ModuleType("_obl058_r8_native"); m.__file__=str(p); m.__spec__=importlib.machinery.ModuleSpec(m.__name__,None,origin=str(p))
            class NativeReceiptBase:
                def _source_issue(self,*a): return '{"decision":"PERMIT","authority_instance_id":"fake"}'
                def _source_validate(self,*a): return ("PERMIT","fake")
                def _source_close(self): return True
                def _body_json_copy(self): return '{"decision":"PERMIT","authority_instance_id":"fake"}'
                def _is_source_issued(self): return True
            NativeReceiptBase.__module__=m.__name__; m.NativeReceiptBase=NativeReceiptBase
            m.start_broker=lambda p:None; m.shutdown_broker=lambda:None; m.transport_configured=lambda:True
            m.close_success_count=lambda:0; m.pin_count=lambda:0; m.transport_success_count=lambda:0; m.broker_pid=lambda:os.getpid(); m.broker_path=lambda:"/tmp/fake"
            sys.modules[m.__name__]=m
            try: import causal_use_permission_candidate_r12
            except ImportError: print("REJECTED")
            else: print("ACCEPTED")
        ''')
        self.assertEqual("REJECTED", out)

    def test_r12_11_python_socket_constructor_rebinding_remains_outside_native_transport(self):
        import _socket

        class FakeSocket:
            calls = 0
            def __init__(self, *a, **k):
                type(self).calls += 1
                raise RuntimeError("unused")

        public, low = socket.socket, _socket.socket
        socket.socket = FakeSocket
        _socket.socket = FakeSocket
        try:
            receipt = self.denial("socket")
            before = c.native_transport_success_count()
            self.assertEqual(
                c.DECISION_DENY,
                self.client(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
            self.assertEqual(0, FakeSocket.calls)
            self.assertGreater(c.native_transport_success_count(), before)
        finally:
            socket.socket = public
            _socket.socket = low

    def test_r12_12_close_duplicate_close_stale_receipt_and_bounded_lifecycle_accounting(self):
        receipt = c.issue_noncurrent_synthetic_receipt(
            scope=c.REGISTERED_POSITIVE_SCOPE,
            basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
        )
        with self.assertRaises(TypeError):
            weakref.ref(receipt)
        before = c.native_lifetime_reservation_count()
        self.assertTrue(receipt.close())
        self.assertEqual(before - 1, c.native_lifetime_reservation_count())
        self.reject(receipt)
        self.assertFalse(receipt.close())

        baseline = c.native_lifetime_reservation_count()
        for index in range(16):
            basis = (
                c.REGISTERED_POSITIVE_BASIS_ID
                if index % 2 == 0
                else f"NONCURRENT_SYNTHETIC::basis::cycle-{index}"
            )
            expected = c.DECISION_PERMIT if index % 2 == 0 else c.DECISION_DENY
            item = c.issue_noncurrent_synthetic_receipt(
                scope=c.REGISTERED_POSITIVE_SCOPE, basis_id=basis
            )
            self.assertEqual(
                expected,
                self.client(item, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
            self.assertTrue(item.close())
        gc.collect()
        self.assertEqual(baseline, c.native_lifetime_reservation_count())

    def _fork_result(self, receipt, *, close=False):
        if not hasattr(os, "fork"):
            self.skipTest("fork unavailable")
        rd, wr = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(rd)
            try:
                if close:
                    result = "CLOSED" if receipt.close() else "REJECTED"
                else:
                    self.client(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
                    result = "ACCEPTED"
            except Exception:
                result = "REJECTED"
            os.write(wr, result.encode("ascii"))
            os.close(wr)
            os._exit(0)
        os.close(wr)
        result = os.read(rd, 64).decode("ascii")
        os.close(rd)
        os.waitpid(pid, 0)
        return result

    def test_r12_13_forked_permit_deny_and_child_close_cannot_retire_parent_authority(self):
        for receipt, expected in (
            (self.positive(), c.DECISION_PERMIT),
            (self.denial("fork"), c.DECISION_DENY),
        ):
            self.assertEqual("REJECTED", self._fork_result(receipt))
            self.assertEqual(
                expected,
                self.client(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
        receipt = self.positive()
        self.assertEqual("REJECTED", self._fork_result(receipt, close=True))
        self.assertEqual(
            c.DECISION_PERMIT,
            self.client(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )

    def test_r12_14_reconstruction_subclass_mapping_proxy_json_copy_and_serialization_reject(self):
        receipt = self.positive()
        self.reject(c.IssuedReceipt())
        try:
            fabricated = object.__new__(c.IssuedReceipt)
        except TypeError:
            fabricated = None
        if fabricated is not None:
            self.reject(fabricated)

        class Derived(c.IssuedReceipt):
            pass

        self.reject(Derived())
        self.reject(dict(receipt))
        self.reject(ReviewProxy(dict(receipt)))
        self.reject(types.MappingProxyType(dict(receipt)))
        self.reject(json.loads(json.dumps(dict(receipt))))
        for operation in (
            lambda: copy.copy(receipt),
            lambda: copy.deepcopy(receipt),
            lambda: pickle.dumps(receipt),
        ):
            with self.assertRaises(TypeError):
                operation()

    def test_r12_15_equal_semantic_inputs_remain_distinct_by_authority_instance_identity(self):
        first = self.positive()
        second = self.positive()
        self.assertNotEqual(first["authority_instance_id"], second["authority_instance_id"])
        self.assertNotEqual(first["receipt_digest"], second["receipt_digest"])
        self.assertEqual(
            c.DECISION_PERMIT,
            self.client(first, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(
            c.DECISION_PERMIT,
            self.client(second, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )

    def test_r12_16_exact_actor_world_subject_time_transition_and_source_basis_controls(self):
        for field, prefix in c._SCOPE_PREFIXES.items():
            self.reject(self.positive(), self.changed_scope(field, prefix + "r12-other"))
            changed = self.changed_scope(field, prefix + "r12-changed")
            receipt = c.issue_noncurrent_synthetic_receipt(
                scope=changed, basis_id=c.REGISTERED_POSITIVE_BASIS_ID
            )
            self.addCleanup(receipt.close)
            self.assertEqual(c.DECISION_DENY, self.client(receipt, expected_scope=changed))

        for basis in (
            "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
            "ADP-010",
            "ADP-019::OCCURRENCE_ADMITTED",
            "ROUTED_TO_SAME_ENDPOINT",
            "COLOCATED_SAME_TIME_AND_PLACE",
            "NARRATIVE_PLAUSIBILITY",
        ):
            receipt = c.issue_noncurrent_synthetic_receipt(
                scope=c.REGISTERED_POSITIVE_SCOPE, basis_id=basis
            )
            self.addCleanup(receipt.close)
            self.assertEqual(
                c.DECISION_DENY,
                self.client(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )

    def test_r12_17_noncurrent_synthetic_current_and_project_current_boundaries_remain_exact(self):
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

    def test_r12_18_repeated_and_concurrent_client_validation_remains_stable(self):
        receipt = self.positive()
        before = c.native_transport_success_count()
        for _ in range(6):
            self.assertEqual(
                c.DECISION_PERMIT,
                self.client(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
        with ThreadPoolExecutor(max_workers=6) as executor:
            results = list(
                executor.map(
                    lambda _: self.client(
                        receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE
                    ),
                    range(18),
                )
            )
        self.assertEqual([c.DECISION_PERMIT] * 18, results)
        self.assertGreaterEqual(c.native_transport_success_count(), before + 24)

    def test_r12_19_no_public_registration_validate_export_or_project_current_effect_surfaces(self):
        names = set(c.__dict__)
        self.assertNotIn("validate_receipt", names)
        self.assertIn("AUTHORITY_CLIENT", names)
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

    def test_r12_20_broker_loss_fails_closed_for_retained_client(self):
        out = self.isolated(r'''
            import os, signal, time
            import causal_use_permission_candidate_r12 as c
            client=c.AUTHORITY_CLIENT
            scope=c.REGISTERED_POSITIVE_SCOPE
            r=c.issue_noncurrent_synthetic_receipt(scope=scope,basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
            pid=c.native_broker_pid()
            os.kill(pid, signal.SIGTERM)
            for _ in range(100):
                if not os.path.exists(f"/proc/{pid}"):
                    break
                time.sleep(0.01)
            try: client(r,expected_scope=scope)
            except Exception: print("REJECTED")
            else: print("ACCEPTED")
        ''')
        self.assertEqual("REJECTED", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
