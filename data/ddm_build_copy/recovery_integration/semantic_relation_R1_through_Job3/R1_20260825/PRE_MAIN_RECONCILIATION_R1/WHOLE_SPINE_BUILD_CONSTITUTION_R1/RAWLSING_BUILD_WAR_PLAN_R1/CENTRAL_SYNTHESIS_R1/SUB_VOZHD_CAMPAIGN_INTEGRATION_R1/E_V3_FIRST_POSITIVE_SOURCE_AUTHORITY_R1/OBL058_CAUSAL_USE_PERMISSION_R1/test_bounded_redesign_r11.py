"""Producer governed verification for OBL058 R11 retained-capability redesign.

Producer-side verification only. No self-review or independent review is
performed by this surface.
"""
from __future__ import annotations

import copy
from concurrent.futures import ThreadPoolExecutor
import gc
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import pickle
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

import causal_use_permission_candidate_r11 as c  # noqa: E402

CANARY = (
    "urn:rawlsing:v3:subject:sha256:"
    "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
)


class ReviewProxy(dict):
    pass


class OBL058BoundedRedesignR11Court(unittest.TestCase):
    def positive(self):
        receipt = c.issue_noncurrent_synthetic_receipt(
            scope=c.REGISTERED_POSITIVE_SCOPE,
            basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(receipt.close)
        return receipt

    def denial(self, suffix="r11-deny"):
        receipt = c.issue_noncurrent_synthetic_receipt(
            scope=c.REGISTERED_POSITIVE_SCOPE,
            basis_id=f"NONCURRENT_SYNTHETIC::basis::{suffix}",
        )
        self.addCleanup(receipt.close)
        return receipt

    def changed_scope(self, field, value):
        values = c.REGISTERED_POSITIVE_SCOPE.canonical()
        values[field] = value
        return c.ExactScope(**values)

    def reject(self, receipt, scope=None):
        with self.assertRaises(c.PermissionContractError):
            c.validate_receipt(
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

    def test_r11_01_genuine_permit_deny_and_revision(self):
        self.assertEqual(
            c.DECISION_PERMIT,
            c.validate_receipt(self.positive(), expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(
            c.DECISION_DENY,
            c.validate_receipt(self.denial(), expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(
            "OBL058_CAUSAL_USE_PERMISSION_RETAINED_VALIDATION_CAPABILITY_R11@1.0.0",
            c.MECHANISM_REVISION,
        )

    def test_r11_02_exact_r10_module_attribute_divergence_cannot_redirect(self):
        out = self.isolated(r'''
            import hashlib, importlib.util, sys, sysconfig, tempfile, types
            from pathlib import Path
            here = Path.cwd()
            source = here / "obl058_r11_dispatch_capability.c"
            digest = hashlib.sha256(source.read_bytes()).hexdigest()[:20]
            suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
            output = Path(tempfile.gettempdir())/"rawlsing_obl058_r11_capability"/f"py{sys.version_info.major}{sys.version_info.minor}"/f"_obl058_r11_dispatch_capability_{digest}{suffix}"
            if not output.exists():
                raise SystemExit("expected producer-built R11 capability extension is absent")
            spec = importlib.util.spec_from_file_location("_obl058_r11_dispatch_capability", output)
            module_object = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module_object)
            calls = []
            class module(types.ModuleType):
                def __getattribute__(self, name):
                    if name == "establish_capability":
                        def fake_establish(*args):
                            calls.append("establish")
                            return lambda *a, **k: "PERMIT"
                        return fake_establish
                    if name == "public_validate":
                        def fake_validate(*args, **kwargs):
                            calls.append("validate")
                            return "PERMIT"
                        return fake_validate
                    return super().__getattribute__(name)
            module_object.__class__ = module
            sys.modules["_obl058_r11_dispatch_capability"] = module_object
            import causal_use_permission_candidate_r11 as candidate
            receipt = candidate.issue_noncurrent_synthetic_receipt(
                scope=candidate.REGISTERED_POSITIVE_SCOPE,
                basis_id="NONCURRENT_SYNTHETIC::basis::r11-r10-regression-deny",
            )
            before = candidate.native_transport_success_count()
            result = candidate.validate_receipt(receipt, expected_scope=candidate.REGISTERED_POSITIVE_SCOPE)
            after = candidate.native_transport_success_count()
            print(result, after-before, len(calls), candidate.validate_receipt.__class__.__name__)
            receipt.close()
        ''')
        parts = out.split()
        self.assertEqual(c.DECISION_DENY, parts[0])
        self.assertGreater(int(parts[1]), 0)
        self.assertEqual("0", parts[2])
        self.assertIn(parts[3], {"builtin_function_or_method", "builtin_function"})

    def test_r11_03_mediated_dictionary_with_python_substitute_fails_closed(self):
        out = self.isolated(r'''
            import hashlib, importlib.util, sys, sysconfig, tempfile, types
            from pathlib import Path
            source=Path.cwd()/"obl058_r11_dispatch_capability.c"
            digest=hashlib.sha256(source.read_bytes()).hexdigest()[:20]
            suffix=sysconfig.get_config_var("EXT_SUFFIX") or ".so"
            output=Path(tempfile.gettempdir())/"rawlsing_obl058_r11_capability"/f"py{sys.version_info.major}{sys.version_info.minor}"/f"_obl058_r11_dispatch_capability_{digest}{suffix}"
            spec=importlib.util.spec_from_file_location("_obl058_r11_dispatch_capability",output)
            m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
            real_dict=m.__dict__
            class module(types.ModuleType):
                def __getattribute__(self,name):
                    if name == "__dict__":
                        fake=dict(real_dict)
                        fake["public_validate"] = lambda *a,**k: "PERMIT"
                        return fake
                    return super().__getattribute__(name)
            m.__class__=module
            sys.modules[m.__name__]=m
            try: import causal_use_permission_candidate_r11
            except ImportError: print("REJECTED")
            else: print("ACCEPTED")
        ''')
        self.assertEqual("REJECTED", out)

    def test_r11_04_post_establishment_module_mediation_cannot_redirect_retained_capability(self):
        receipt = self.denial("post-establish")
        validator = c.validate_receipt
        module_object = c._capability_module
        original_class = module_object.__class__
        calls = []
        class module(types.ModuleType):
            def __getattribute__(self, name):
                if name in {"establish_capability", "public_validate"}:
                    calls.append(name)
                    return lambda *a, **k: c.DECISION_PERMIT
                return super().__getattribute__(name)
        module_object.__class__ = module
        try:
            before = c.native_transport_success_count()
            self.assertEqual(
                c.DECISION_DENY,
                validator(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
            self.assertEqual([], calls)
            self.assertGreater(c.native_transport_success_count(), before)
        finally:
            module_object.__class__ = original_class

    def test_r11_05_capability_identity_is_exactly_verified_and_retained(self):
        builtin_type = [].append.__class__
        self.assertIs(c._establish_capability.__class__, builtin_type)
        self.assertIs(c._verified_public_validate.__class__, builtin_type)
        self.assertIs(c._establish_capability.__self__, c._capability_module)
        self.assertIs(c._verified_public_validate.__self__, c._capability_module)
        self.assertIs(c.validate_receipt, c._verified_public_validate)
        self.assertIs(c.validate_receipt, c._retained_validation_capability)

    def test_r11_06_sys_modules_alias_and_export_rebinding_do_not_change_saved_capability(self):
        receipt = self.denial("module-rebind")
        validator = c.validate_receipt
        genuine = c._capability_module
        original_export = c.validate_receipt
        try:
            sys.modules[c._CAPABILITY_NAME] = types.ModuleType(c._CAPABILITY_NAME)
            sys.modules["obl058_r11_alias"] = types.SimpleNamespace(validate_receipt=lambda *a,**k:"PERMIT")
            c.validate_receipt = lambda *a, **k: c.DECISION_PERMIT
            self.assertEqual(
                c.DECISION_DENY,
                validator(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
        finally:
            sys.modules[c._CAPABILITY_NAME] = genuine
            sys.modules.pop("obl058_r11_alias", None)
            c.validate_receipt = original_export

    def test_r11_07_plain_python_capability_cache_lookalike_rejects(self):
        out = self.isolated(r'''
            import hashlib, importlib.machinery, sys, sysconfig, tempfile, types
            from pathlib import Path
            source=Path.cwd()/"obl058_r11_dispatch_capability.c"
            digest=hashlib.sha256(source.read_bytes()).hexdigest()[:20]
            suffix=sysconfig.get_config_var("EXT_SUFFIX") or ".so"
            output=Path(tempfile.gettempdir())/"rawlsing_obl058_r11_capability"/f"py{sys.version_info.major}{sys.version_info.minor}"/f"_obl058_r11_dispatch_capability_{digest}{suffix}"
            m=types.ModuleType("_obl058_r11_dispatch_capability")
            m.__file__=str(output); m.__spec__=importlib.machinery.ModuleSpec(m.__name__,None,origin=str(output))
            m.establish_capability=lambda *a: (lambda *x,**k:"PERMIT")
            m.public_validate=lambda *a,**k:"PERMIT"
            m.bound_descriptor_identity=lambda:1
            sys.modules[m.__name__]=m
            try: import causal_use_permission_candidate_r11
            except ImportError: print("REJECTED")
            else: print("ACCEPTED")
        ''')
        self.assertEqual("REJECTED", out)

    def test_r11_08_loader_substitution_cannot_establish_python_fallback(self):
        out = self.isolated(r'''
            import importlib.machinery, importlib.util, sys, types
            real = importlib.util.spec_from_file_location
            class L:
                def create_module(self, spec):
                    m=types.ModuleType(spec.name); m.__file__=str(spec.origin); return m
                def exec_module(self,m):
                    m.establish_capability=lambda *a:(lambda *x,**k:"PERMIT")
                    m.public_validate=lambda *a,**k:"PERMIT"
                    m.bound_descriptor_identity=lambda:1
            importlib.util.spec_from_file_location=lambda name,path: importlib.machinery.ModuleSpec(name,L(),origin=str(path))
            try: import causal_use_permission_candidate_r11
            except Exception: print("REJECTED")
            else: print("ACCEPTED")
            finally: importlib.util.spec_from_file_location=real
        ''')
        self.assertEqual("REJECTED", out)

    def test_r11_09_r9_receipt_class_dispatch_replacement_remains_irrelevant(self):
        receipt = self.denial("r9-regression")
        validator = c.validate_receipt
        original = c.IssuedReceipt._source_validate
        calls = []
        def replacement(self, scope):
            calls.append(scope)
            return c.DECISION_PERMIT, receipt["authority_instance_id"]
        c.IssuedReceipt._source_validate = replacement
        try:
            self.assertEqual(
                c.DECISION_DENY,
                validator(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
            self.assertEqual([], calls)
        finally:
            c.IssuedReceipt._source_validate = original

    def test_r11_10_python_socket_constructor_rebinding_remains_irrelevant(self):
        import _socket
        class FakeSocket:
            calls = 0
            def __init__(self,*a,**k):
                type(self).calls += 1
                raise RuntimeError("unused")
        public, low = socket.socket, _socket.socket
        socket.socket = FakeSocket; _socket.socket = FakeSocket
        try:
            receipt = self.denial("socket")
            self.assertEqual(
                c.DECISION_DENY,
                c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
            self.assertEqual(0, FakeSocket.calls)
        finally:
            socket.socket = public; _socket.socket = low

    def test_r11_11_close_duplicate_close_and_lifecycle_accounting(self):
        receipt = c.issue_noncurrent_synthetic_receipt(
            scope=c.REGISTERED_POSITIVE_SCOPE,
            basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
        )
        with self.assertRaises(TypeError): weakref.ref(receipt)
        before = c.native_lifetime_reservation_count()
        self.assertTrue(receipt.close())
        self.assertEqual(before - 1, c.native_lifetime_reservation_count())
        self.reject(receipt)
        self.assertFalse(receipt.close())
        baseline = c.native_lifetime_reservation_count()
        for index in range(12):
            basis = c.REGISTERED_POSITIVE_BASIS_ID if index % 2 == 0 else f"NONCURRENT_SYNTHETIC::basis::cycle-{index}"
            expected = c.DECISION_PERMIT if index % 2 == 0 else c.DECISION_DENY
            item = c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id=basis)
            self.assertEqual(expected,c.validate_receipt(item,expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            self.assertTrue(item.close())
        gc.collect()
        self.assertEqual(baseline, c.native_lifetime_reservation_count())

    def _fork_result(self, receipt, *, close=False):
        if not hasattr(os, "fork"):
            self.skipTest("fork unavailable")
        rd, wr = os.pipe(); pid = os.fork()
        if pid == 0:
            os.close(rd)
            try:
                if close:
                    result = "CLOSED" if receipt.close() else "REJECTED"
                else:
                    c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
                    result = "ACCEPTED"
            except Exception:
                result = "REJECTED"
            os.write(wr, result.encode("ascii")); os.close(wr); os._exit(0)
        os.close(wr); result = os.read(rd,64).decode("ascii"); os.close(rd); os.waitpid(pid,0)
        return result

    def test_r11_12_fork_requester_generation_and_parent_survival(self):
        for receipt, expected in ((self.positive(),c.DECISION_PERMIT),(self.denial("fork"),c.DECISION_DENY)):
            self.assertEqual("REJECTED", self._fork_result(receipt))
            self.assertEqual(expected,c.validate_receipt(receipt,expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        receipt = self.positive()
        self.assertEqual("REJECTED", self._fork_result(receipt, close=True))
        self.assertEqual(c.DECISION_PERMIT,c.validate_receipt(receipt,expected_scope=c.REGISTERED_POSITIVE_SCOPE))

    def test_r11_13_reconstruction_subclass_mapping_json_copy_and_pickle_reject(self):
        receipt = self.positive()
        self.reject(c.IssuedReceipt())
        class Derived(c.IssuedReceipt): pass
        self.reject(Derived()); self.reject(dict(receipt)); self.reject(ReviewProxy(dict(receipt)))
        self.reject(json.loads(json.dumps(dict(receipt))))
        for op in (lambda:copy.copy(receipt),lambda:copy.deepcopy(receipt),lambda:pickle.dumps(receipt)):
            with self.assertRaises(TypeError): op()
        second = self.positive()
        self.assertNotEqual(receipt["authority_instance_id"],second["authority_instance_id"])
        self.assertNotEqual(receipt["receipt_digest"],second["receipt_digest"])

    def test_r11_14_exact_five_field_scope_and_registered_basis_binding(self):
        for field, prefix in c._SCOPE_PREFIXES.items():
            self.reject(self.positive(), self.changed_scope(field, prefix + "other"))
            changed = self.changed_scope(field, prefix + "changed")
            receipt = c.issue_noncurrent_synthetic_receipt(scope=changed,basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
            self.addCleanup(receipt.close)
            self.assertEqual(c.DECISION_DENY,c.validate_receipt(receipt,expected_scope=changed))

    def test_r11_15_current_shaped_wrong_fixture_and_surrogate_basis_controls(self):
        replacements={
            "actor_id":"urn:rawlsing:v3:actor:project-current:a",
            "world_id":"urn:rawlsing:v3:world:project-current:w",
            "subject_id":CANARY,
            "time_id":"urn:rawlsing:v3:time:project-current:t",
            "transition_id":"urn:rawlsing:v3:transition:project-current:tr",
        }
        for field,value in replacements.items():
            with self.assertRaises(c.PermissionContractError):
                c.issue_noncurrent_synthetic_receipt(scope=self.changed_scope(field,value),basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
        with self.assertRaises(c.PermissionContractError):
            c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id=c.REGISTERED_POSITIVE_BASIS_ID,fixture_class="PROJECT_CURRENT")
        for basis in ("ADP-010","ADP-019::OCCURRENCE_ADMITTED","ROUTED_TO_SAME_ENDPOINT","NARRATIVE_PLAUSIBILITY"):
            receipt=c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id=basis)
            self.addCleanup(receipt.close)
            self.assertEqual(c.DECISION_DENY,c.validate_receipt(receipt,expected_scope=c.REGISTERED_POSITIVE_SCOPE))

    def test_r11_16_repeated_and_concurrent_validation_remains_native_and_stable(self):
        receipt=self.positive(); before=c.native_transport_success_count()
        for _ in range(4):
            self.assertEqual(c.DECISION_PERMIT,c.validate_receipt(receipt,expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        with ThreadPoolExecutor(max_workers=5) as pool:
            results=list(pool.map(lambda _: c.validate_receipt(receipt,expected_scope=c.REGISTERED_POSITIVE_SCOPE),range(10)))
        self.assertEqual([c.DECISION_PERMIT]*10,results)
        self.assertGreaterEqual(c.native_transport_success_count(),before+14)

    def test_r11_17_no_public_registration_or_project_current_effect_surfaces(self):
        names=set(c.__dict__)
        for name in (
            "register_source_basis","execute_obl055","install_obl056_positive",
            "create_encounter","realize_oee","create_actor","activate_actor","unblock_obl061",
        ):
            self.assertNotIn(name,names)


if __name__ == "__main__":
    unittest.main(verbosity=2)
