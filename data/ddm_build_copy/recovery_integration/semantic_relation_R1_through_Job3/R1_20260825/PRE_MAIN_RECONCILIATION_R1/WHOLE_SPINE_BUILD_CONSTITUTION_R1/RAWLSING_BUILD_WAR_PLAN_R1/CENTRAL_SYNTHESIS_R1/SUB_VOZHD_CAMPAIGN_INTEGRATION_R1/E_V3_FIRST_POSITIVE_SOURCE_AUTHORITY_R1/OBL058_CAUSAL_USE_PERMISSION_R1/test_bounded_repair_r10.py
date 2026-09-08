"""Producer governed verification for OBL058 R10 bounded repair.

Producer-side verification only. No independent review is performed here.
"""
from __future__ import annotations

import copy
from concurrent.futures import ThreadPoolExecutor
import gc
import json
import os
from pathlib import Path
import pickle
import signal
import socket
import subprocess
import sys
import textwrap
import types
import unittest
import weakref

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import causal_use_permission_candidate_r10 as c  # noqa: E402

CANARY = (
    "urn:rawlsing:v3:subject:sha256:"
    "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
)


class OBL058BoundedRepairR10Court(unittest.TestCase):
    def positive(self):
        r = c.issue_noncurrent_synthetic_receipt(
            scope=c.REGISTERED_POSITIVE_SCOPE,
            basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(r.close)
        return r

    def denial(self, suffix="r10-deny"):
        r = c.issue_noncurrent_synthetic_receipt(
            scope=c.REGISTERED_POSITIVE_SCOPE,
            basis_id=f"NONCURRENT_SYNTHETIC::basis::{suffix}",
        )
        self.addCleanup(r.close)
        return r

    def changed_scope(self, field, value):
        values = c.REGISTERED_POSITIVE_SCOPE.canonical()
        values[field] = value
        return c.ExactScope(**values)

    def reject(self, receipt, scope=None):
        with self.assertRaises(c.PermissionContractError):
            c.validate_receipt(receipt, expected_scope=scope or c.REGISTERED_POSITIVE_SCOPE)

    def isolated(self, body, timeout=60):
        script = f"import sys\nsys.path.insert(0,{str(HERE)!r})\n" + textwrap.dedent(body)
        result = subprocess.run(
            [sys.executable, "-c", script], cwd=HERE, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout,
        )
        if result.returncode:
            self.fail(f"isolated rc={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}")
        return result.stdout.strip()

    def test_r10_01_valid_permit_deny_and_exact_revision(self):
        self.assertEqual(c.DECISION_PERMIT, c.validate_receipt(self.positive(), expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        self.assertEqual(c.DECISION_DENY, c.validate_receipt(self.denial(), expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0", c.AUTHORITY_ID)
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0", c.SCHEMA_VERSION)
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_PUBLIC_NATIVE_DISPATCH_R10@1.0.0", c.MECHANISM_REVISION)

    def test_r10_02_exact_r9_class_method_override_cannot_substitute_deny(self):
        r = self.denial("exact-r9")
        instance = r["authority_instance_id"]
        before = c.native_transport_success_count()
        original = c.IssuedReceipt._source_validate
        calls = []
        def replacement(self, scope):
            calls.append(scope)
            return (c.DECISION_PERMIT, instance)
        c.IssuedReceipt._source_validate = replacement
        try:
            self.assertEqual(c.DECISION_DENY, c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            self.assertEqual([], calls)
            self.assertGreater(c.native_transport_success_count(), before)
        finally:
            c.IssuedReceipt._source_validate = original

    def test_r10_03_override_before_issue_after_issue_and_between_validations_is_irrelevant(self):
        original = c.IssuedReceipt._source_validate
        def fake(self, scope):
            return (c.DECISION_PERMIT, "not-native")
        try:
            c.IssuedReceipt._source_validate = fake
            r = self.denial("before-issue")
            self.assertEqual(c.DECISION_DENY, c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            c.IssuedReceipt._source_validate = original
            r2 = self.denial("after-issue")
            self.assertEqual(c.DECISION_DENY, c.validate_receipt(r2, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            c.IssuedReceipt._source_validate = fake
            self.assertEqual(c.DECISION_DENY, c.validate_receipt(r2, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            c.IssuedReceipt._source_validate = original
            self.assertEqual(c.DECISION_DENY, c.validate_receipt(r2, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        finally:
            c.IssuedReceipt._source_validate = original

    def test_r10_04_descriptor_property_and_getattribute_override_cannot_redirect(self):
        r = self.denial("descriptor")
        original_validate = c.IssuedReceipt._source_validate
        original_getattribute = c.IssuedReceipt.__getattribute__
        class Redirect:
            def __get__(self, obj, owner=None):
                return lambda scope: (c.DECISION_PERMIT, r["authority_instance_id"])
        try:
            c.IssuedReceipt._source_validate = Redirect()
            self.assertEqual(c.DECISION_DENY, c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            c.IssuedReceipt.__getattribute__ = lambda self, name: ((lambda scope: (c.DECISION_PERMIT, "fake")) if name == "_source_validate" else original_getattribute(self, name))
            self.assertEqual(c.DECISION_DENY, c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        finally:
            c.IssuedReceipt._source_validate = original_validate
            c.IssuedReceipt.__getattribute__ = original_getattribute

    def test_r10_05_instance_and_subclass_surfaces_cannot_redirect(self):
        r = self.denial("instance")
        self.assertFalse(hasattr(r, "__dict__"))
        with self.assertRaises(AttributeError):
            object.__setattr__(r, "_source_validate", lambda scope: (c.DECISION_PERMIT, "fake"))
        class Derived(c.IssuedReceipt):
            def _source_validate(self, scope):
                return (c.DECISION_PERMIT, "fake")
        self.reject(Derived())
        try:
            r.__class__ = Derived
        except (TypeError, AttributeError):
            pass
        else:
            self.reject(r)

    def test_r10_06_module_alias_cache_and_dispatch_attribute_rebinding_do_not_change_saved_public_validator(self):
        r = self.denial("module-alias")
        validator = c.validate_receipt
        genuine_dispatch = c._dispatch
        genuine_native = c._native
        fake = types.SimpleNamespace(public_validate=lambda *a, **k: c.DECISION_PERMIT)
        try:
            c._dispatch = fake
            c._native = fake
            sys.modules[c._DISPATCH_NAME] = types.ModuleType(c._DISPATCH_NAME)
            sys.modules[c._NATIVE_NAME] = types.ModuleType(c._NATIVE_NAME)
            self.assertEqual(c.DECISION_DENY, validator(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        finally:
            c._dispatch = genuine_dispatch
            c._native = genuine_native
            sys.modules[c._DISPATCH_NAME] = genuine_dispatch
            sys.modules[c._NATIVE_NAME] = genuine_native

    def test_r10_07_public_validator_is_genuine_bound_c_function_and_native_transport_is_reached(self):
        btype = [].append.__class__
        self.assertIs(c.validate_receipt.__class__, btype)
        self.assertIs(c.validate_receipt.__self__, c._dispatch)
        for receipt, expected in ((self.positive(), c.DECISION_PERMIT), (self.denial("native-proof"), c.DECISION_DENY)):
            before = c.native_transport_success_count()
            self.assertEqual(expected, c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            self.assertGreater(c.native_transport_success_count(), before)

    def test_r10_08_fake_dispatch_cache_before_import_is_rejected(self):
        out = self.isolated(r'''
            import hashlib, importlib.machinery, sys, sysconfig, tempfile, types
            from pathlib import Path
            src=Path.cwd()/"obl058_r10_dispatch.c"
            d=hashlib.sha256(src.read_bytes()).hexdigest()[:20]
            s=sysconfig.get_config_var("EXT_SUFFIX") or ".so"
            p=Path(tempfile.gettempdir())/"rawlsing_obl058_r10_dispatch"/f"py{sys.version_info.major}{sys.version_info.minor}"/f"_obl058_r10_dispatch_{d}{s}"
            m=types.ModuleType("_obl058_r10_dispatch"); m.__file__=str(p); m.__spec__=importlib.machinery.ModuleSpec(m.__name__,None,origin=str(p))
            m.bind_contract=lambda *a:None; m.public_validate=lambda *a,**k:"PERMIT"; m.bound_descriptor_identity=lambda:1
            sys.modules[m.__name__]=m
            try: import causal_use_permission_candidate_r10
            except ImportError: print("REJECTED")
            else: print("ACCEPTED")
        ''')
        self.assertEqual("REJECTED", out)

    def test_r10_09_r9_fake_native_cache_before_import_remains_rejected(self):
        out = self.isolated(r'''
            import importlib.machinery, os, sys, types
            m=types.ModuleType("_obl058_r8_native"); m.__file__="/tmp/fake.so"; m.__spec__=importlib.machinery.ModuleSpec(m.__name__,None,origin=m.__file__)
            m.start_broker=lambda p:None; m.shutdown_broker=lambda:None; m.transport_configured=lambda:True
            m.close_success_count=lambda:0; m.pin_count=lambda:0; m.transport_success_count=lambda:0; m.broker_pid=lambda:os.getpid(); m.broker_path=lambda:"/tmp/fake"
            class NativeReceiptBase: pass
            NativeReceiptBase.__module__=m.__name__; m.NativeReceiptBase=NativeReceiptBase
            sys.modules[m.__name__]=m
            try: import causal_use_permission_candidate_r10
            except ImportError: print("REJECTED")
            else: print("ACCEPTED")
        ''')
        self.assertEqual("REJECTED", out)

    def test_r10_10_python_socket_constructor_rebinding_remains_irrelevant(self):
        import _socket
        class FakeSocket:
            calls=0
            def __init__(self,*a,**k):
                type(self).calls+=1
                raise RuntimeError("unused")
        public, low = socket.socket, _socket.socket
        socket.socket = FakeSocket; _socket.socket = FakeSocket
        try:
            r = self.denial("socket")
            self.assertEqual(c.DECISION_DENY, c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            self.assertEqual(0, FakeSocket.calls)
        finally:
            socket.socket = public; _socket.socket = low

    def test_r10_11_lifecycle_close_duplicate_and_bounded_cycles_preserved(self):
        r=self.positive()
        with self.assertRaises(TypeError): weakref.ref(r)
        with self.assertRaises(TypeError): weakref.finalize(r, lambda:None)
        base=c.native_lifetime_reservation_count()
        t=c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
        self.assertEqual(base+1,c.native_lifetime_reservation_count())
        del t; gc.collect(); self.assertEqual(base+1,c.native_lifetime_reservation_count())
        t=c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
        pins=c.native_lifetime_reservation_count(); closes=c.native_successful_close_count()
        self.assertTrue(t.close()); self.assertEqual(pins-1,c.native_lifetime_reservation_count()); self.assertEqual(closes+1,c.native_successful_close_count())
        self.reject(t); self.assertFalse(t.close())
        baseline=c.native_lifetime_reservation_count()
        for i in range(15):
            basis=c.REGISTERED_POSITIVE_BASIS_ID if i%2==0 else f"NONCURRENT_SYNTHETIC::basis::cycle-{i}"
            expected=c.DECISION_PERMIT if i%2==0 else c.DECISION_DENY
            x=c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id=basis)
            self.assertEqual(expected,c.validate_receipt(x,expected_scope=c.REGISTERED_POSITIVE_SCOPE)); self.assertTrue(x.close())
        self.assertEqual(baseline,c.native_lifetime_reservation_count())

    def fork_result(self, receipt, do_close=False):
        if not hasattr(os,"fork"): self.skipTest("fork unavailable")
        rd,wr=os.pipe(); pid=os.fork()
        if pid==0:
            os.close(rd)
            try:
                if do_close: result="CLOSED" if receipt.close() else "REJECTED"
                else: c.validate_receipt(receipt,expected_scope=c.REGISTERED_POSITIVE_SCOPE); result="ACCEPTED"
            except Exception: result="REJECTED"
            os.write(wr,result.encode()); os.close(wr); os._exit(0)
        os.close(wr); result=os.read(rd,64).decode(); os.close(rd); os.waitpid(pid,0); return result

    def test_r10_12_requester_generation_and_fork_parent_child_controls_preserved(self):
        for r,expected in ((self.positive(),c.DECISION_PERMIT),(self.denial("fork"),c.DECISION_DENY)):
            self.assertEqual("REJECTED",self.fork_result(r))
            self.assertEqual(expected,c.validate_receipt(r,expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        r=self.positive(); self.assertEqual("REJECTED",self.fork_result(r,True)); self.assertEqual(c.DECISION_PERMIT,c.validate_receipt(r,expected_scope=c.REGISTERED_POSITIVE_SCOPE))

    def test_r10_13_construction_reconstruction_copy_and_serialization_reject(self):
        r=self.positive(); self.reject(c.IssuedReceipt())
        class Derived(c.IssuedReceipt): pass
        self.reject(Derived()); self.reject(dict(r)); self.reject(json.loads(json.dumps(dict(r))))
        for op in (lambda:copy.copy(r),lambda:copy.deepcopy(r),lambda:pickle.dumps(r)):
            with self.assertRaises(TypeError): op()
        other=self.positive(); self.assertNotEqual(r["authority_instance_id"],other["authority_instance_id"]); self.assertNotEqual(r["receipt_digest"],other["receipt_digest"])

    def test_r10_14_exact_five_field_cross_scope_and_basis_binding_preserved(self):
        for field,prefix in c._SCOPE_PREFIXES.items():
            self.reject(self.positive(), self.changed_scope(field,prefix+"other"))
            scope=self.changed_scope(field,prefix+"changed")
            r=c.issue_noncurrent_synthetic_receipt(scope=scope,basis_id=c.REGISTERED_POSITIVE_BASIS_ID); self.addCleanup(r.close)
            self.assertEqual(c.DECISION_DENY,c.validate_receipt(r,expected_scope=scope))

    def test_r10_15_current_shaped_wrong_fixture_and_surrogate_basis_controls_preserved(self):
        values={
            "actor_id":"urn:rawlsing:v3:actor:project-current:a",
            "world_id":"urn:rawlsing:v3:world:project-current:w",
            "subject_id":CANARY,
            "time_id":"urn:rawlsing:v3:time:project-current:t",
            "transition_id":"urn:rawlsing:v3:transition:project-current:tr",
        }
        for field,value in values.items():
            with self.subTest(field=field):
                with self.assertRaises(c.PermissionContractError):
                    c.issue_noncurrent_synthetic_receipt(scope=self.changed_scope(field,value),basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
        with self.assertRaises(c.PermissionContractError):
            c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id=c.REGISTERED_POSITIVE_BASIS_ID,fixture_class="PROJECT_CURRENT")
        for basis in ("ADP-010","ADP-019::OCCURRENCE_ADMITTED","ROUTED_TO_SAME_ENDPOINT","NARRATIVE_PLAUSIBILITY"):
            r=c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id=basis); self.addCleanup(r.close)
            self.assertEqual(c.DECISION_DENY,c.validate_receipt(r,expected_scope=c.REGISTERED_POSITIVE_SCOPE))

    def test_r10_16_repeated_and_concurrent_validation_stays_native_and_stable(self):
        r=self.positive(); before=c.native_transport_success_count()
        for _ in range(4): self.assertEqual(c.DECISION_PERMIT,c.validate_receipt(r,expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        with ThreadPoolExecutor(max_workers=4) as pool:
            results=list(pool.map(lambda _:c.validate_receipt(r,expected_scope=c.REGISTERED_POSITIVE_SCOPE),range(8)))
        self.assertEqual([c.DECISION_PERMIT]*8,results)
        self.assertGreaterEqual(c.native_transport_success_count(),before+12)

    def test_r10_17_broker_loss_fails_closed(self):
        out=self.isolated(r'''
            import os,signal
            import causal_use_permission_candidate_r10 as c
            r=c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
            os.kill(c.native_broker_pid(),signal.SIGKILL)
            try: c.validate_receipt(r,expected_scope=c.REGISTERED_POSITIVE_SCOPE)
            except c.PermissionContractError: print("REJECTED")
            else: print("ACCEPTED")
        ''')
        self.assertEqual("REJECTED",out)

    def test_r10_18_programmer_call_shape_errors_remain_visible(self):
        with self.assertRaises(TypeError):
            c.validate_receipt()
        with self.assertRaises(TypeError):
            c.validate_receipt(self.positive(), unexpected_scope=c.REGISTERED_POSITIVE_SCOPE)

    def test_r10_19_no_public_source_registration_or_current_effect_surfaces(self):
        names=set(c.__dict__)
        for name in (
            "register_source_basis","execute_obl055","install_obl056_positive",
            "create_actor","activate_actor","create_encounter","realize_oee",
        ):
            self.assertNotIn(name,names)

    def test_r10_20_original_public_validator_object_survives_candidate_attribute_rebinding(self):
        r=self.denial("saved-public")
        validator=c.validate_receipt
        original=c.validate_receipt
        try:
            c.validate_receipt=lambda *a,**k:c.DECISION_PERMIT
            self.assertEqual(c.DECISION_DENY,validator(r,expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        finally:
            c.validate_receipt=original


if __name__ == "__main__":
    unittest.main(verbosity=2)
