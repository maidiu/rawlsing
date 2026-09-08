"""Producer governed verification for OBL058 R9 bounded repair.

Producer-side verification only. No independent review is performed here.
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

CANARY = "urn:rawlsing:v3:subject:sha256:a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"


def expected_output() -> Path:
    paths = [HERE / name for name in (
        "obl058_r8_native.c", "obl058_r8_native_part1.inc",
        "obl058_r8_native_part2.inc", "obl058_r8_native_part3.inc",
    )]
    digest = hashlib.sha256(b"".join(p.read_bytes() for p in paths)).hexdigest()[:20]
    suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
    return Path(tempfile.gettempdir()) / "rawlsing_obl058_r8_native" / f"py{sys.version_info.major}{sys.version_info.minor}" / f"_obl058_r8_native_{digest}{suffix}"


def fake_native() -> types.ModuleType:
    m = types.ModuleType(c._NATIVE_NAME)
    p = str(expected_output().resolve())
    m.__file__ = p
    m.__spec__ = importlib.machinery.ModuleSpec(c._NATIVE_NAME, loader=None, origin=p)

    class NativeReceiptBase:
        def _source_issue(self, *a): return '{"decision":"PERMIT","authority_instance_id":"fake"}'
        def _source_validate(self, *a): return ("PERMIT", "fake")
        def _source_close(self): return True
        def _body_json_copy(self): return '{"decision":"PERMIT","authority_instance_id":"fake"}'
        def _is_source_issued(self): return True

    NativeReceiptBase.__module__ = c._NATIVE_NAME
    m.NativeReceiptBase = NativeReceiptBase
    m.start_broker = lambda path: None
    m.shutdown_broker = lambda: None
    m.transport_configured = lambda: True
    m.close_success_count = lambda: 0
    m.pin_count = lambda: 0
    m.transport_success_count = lambda: 0
    m.broker_pid = lambda: os.getpid()
    m.broker_path = lambda: "/tmp/fake-r9.sock"
    return m


class FakeSocket:
    calls = 0
    def __init__(self, *a, **k):
        type(self).calls += 1
        raise RuntimeError("Python socket constructor should not be used")


class OBL058BoundedRepairR9Court(unittest.TestCase):
    def positive(self):
        r = c.issue_noncurrent_synthetic_receipt(
            scope=c.REGISTERED_POSITIVE_SCOPE,
            basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(r.close)
        return r

    def denial(self, suffix="r9-deny"):
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

    def test_r9_01_controls_and_exact_revision(self):
        self.assertEqual(c.DECISION_PERMIT, c.validate_receipt(self.positive(), expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        self.assertEqual(c.DECISION_DENY, c.validate_receipt(self.denial(), expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0", c.AUTHORITY_ID)
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0", c.SCHEMA_VERSION)
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_NATIVE_BINDING_MECHANISM_R9@1.0.0", c.MECHANISM_REVISION)

    def test_r9_02_exact_r8_preseed_substitute_is_rejected(self):
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
            try: import causal_use_permission_candidate_r9
            except ImportError: print("REJECTED")
            else: print("ACCEPTED")
        ''')
        self.assertEqual("REJECTED", out)
        with self.assertRaises(ImportError):
            c._verify_native_module(fake_native(), c._native_output_path())

    def test_r9_03_genuine_binding_is_c_bound_to_exact_module(self):
        btype = [].append.__class__
        for name in c._NATIVE_REQUIRED_FUNCTIONS:
            fn = c._native.__dict__[name]
            self.assertIs(fn.__class__, btype)
            self.assertIs(fn.__self__, c._native)
        self.assertEqual(c._NATIVE_NAME, c._native.NativeReceiptBase.__module__)
        self.assertEqual(str(expected_output().resolve()), str(Path(c._native.__file__).resolve()))

    def test_r9_04_cache_replacement_before_and_after_issue_cannot_change_deny(self):
        genuine = sys.modules[c._NATIVE_NAME]
        for phase in ("before", "after"):
            with self.subTest(phase=phase):
                if phase == "before":
                    sys.modules[c._NATIVE_NAME] = fake_native()
                    r = self.denial("cache-before")
                else:
                    r = self.denial("cache-after")
                    sys.modules[c._NATIVE_NAME] = fake_native()
                try:
                    self.assertEqual(c.DECISION_DENY, c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
                finally:
                    sys.modules[c._NATIVE_NAME] = genuine

    def test_r9_05_reimport_reload_and_loader_substitution_fail_closed_or_rebind_genuine(self):
        out = self.isolated(r'''
            import importlib, importlib.machinery, importlib.util, sys, types, json
            import causal_use_permission_candidate_r9 as c
            results=[]
            sys.modules[c._NATIVE_NAME]=types.ModuleType(c._NATIVE_NAME)
            try: importlib.reload(c)
            except ImportError: results.append("CACHE_REJECTED")
            else: results.append("CACHE_ACCEPTED")
            sys.modules.pop(c._NATIVE_NAME,None)
            try: c=importlib.reload(c)
            except ImportError: results.append("REMOVAL_FAIL_CLOSED")
            else:
                r=c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id="NONCURRENT_SYNTHETIC::basis::reload-deny")
                results.append(c.validate_receipt(r,expected_scope=c.REGISTERED_POSITIVE_SCOPE)); r.close()
            print(json.dumps(results))
        ''')
        values = json.loads(out)
        self.assertEqual("CACHE_REJECTED", values[0])
        self.assertIn(values[1], {"REMOVAL_FAIL_CLOSED", c.DECISION_DENY})

        out = self.isolated(r'''
            import importlib, importlib.machinery, importlib.util, sys, types
            import causal_use_permission_candidate_r9 as c
            sys.modules.pop(c._NATIVE_NAME,None)
            real=importlib.util.spec_from_file_location
            class L:
                def create_module(self,s):
                    m=types.ModuleType(c._NATIVE_NAME); m.__file__=str(c._native_output_path()); return m
                def exec_module(self,m): pass
            importlib.util.spec_from_file_location=lambda name,path: importlib.machinery.ModuleSpec(name,L(),origin=str(path))
            try: importlib.reload(c)
            except Exception: print("REJECTED")
            else: print("ACCEPTED")
            finally: importlib.util.spec_from_file_location=real
        ''')
        self.assertEqual("REJECTED", out)

    def test_r9_06_python_transport_constructor_rebinding_remains_irrelevant(self):
        import _socket
        public, low = socket.socket, _socket.socket
        FakeSocket.calls = 0
        socket.socket = FakeSocket; _socket.socket = FakeSocket
        try:
            r = self.denial("socket-rebind")
            self.assertEqual(c.DECISION_DENY, c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE))
            self.assertEqual(0, FakeSocket.calls)
        finally:
            socket.socket = public; _socket.socket = low

        out = self.isolated(r'''
            import socket,_socket,json
            class F:
                calls=0
                def __init__(self,*a,**k): type(self).calls+=1; raise RuntimeError("unused")
            socket.socket=F; _socket.socket=F
            import causal_use_permission_candidate_r9 as c
            r=c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id="NONCURRENT_SYNTHETIC::basis::preimport-deny")
            d=c.validate_receipt(r,expected_scope=c.REGISTERED_POSITIVE_SCOPE); r.close()
            print(json.dumps([d,F.calls]))
        ''')
        self.assertEqual([c.DECISION_DENY, 0], json.loads(out))

    def test_r9_07_lifecycle_close_and_bounded_cycles_preserved(self):
        r = self.positive()
        with self.assertRaises(TypeError): weakref.ref(r)
        with self.assertRaises(TypeError): weakref.finalize(r, lambda: None)
        self.assertFalse(hasattr(r, "authority_key")); self.assertFalse(hasattr(r, "__dict__"))

        base = c.native_lifetime_reservation_count()
        temp = c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
        self.assertEqual(base + 1, c.native_lifetime_reservation_count())
        del temp; gc.collect(); self.assertEqual(base + 1, c.native_lifetime_reservation_count())

        temp = c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
        pins=c.native_lifetime_reservation_count(); closes=c.native_successful_close_count()
        self.assertTrue(temp.close()); self.assertEqual(pins-1,c.native_lifetime_reservation_count()); self.assertEqual(closes+1,c.native_successful_close_count())
        self.reject(temp); self.assertFalse(temp.close())

        baseline=c.native_lifetime_reservation_count()
        for i in range(20):
            basis=c.REGISTERED_POSITIVE_BASIS_ID if i%2==0 else f"NONCURRENT_SYNTHETIC::basis::cycle-{i}"
            expected=c.DECISION_PERMIT if i%2==0 else c.DECISION_DENY
            x=c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id=basis)
            self.assertEqual(expected,c.validate_receipt(x,expected_scope=c.REGISTERED_POSITIVE_SCOPE)); self.assertTrue(x.close())
        self.assertEqual(baseline,c.native_lifetime_reservation_count())

    def fork_result(self, receipt, close=False):
        if not hasattr(os,"fork"): self.skipTest("fork unavailable")
        rd,wr=os.pipe(); pid=os.fork()
        if pid==0:
            os.close(rd)
            try:
                if close: result="CLOSED" if receipt.close() else "REJECTED"
                else: c.validate_receipt(receipt,expected_scope=c.REGISTERED_POSITIVE_SCOPE); result="ACCEPTED"
            except Exception: result="REJECTED"
            os.write(wr,result.encode()); os.close(wr); os._exit(0)
        os.close(wr); result=os.read(rd,64).decode(); os.close(rd); os.waitpid(pid,0); return result

    def test_r9_08_requester_generation_and_fork_isolation_preserved(self):
        for receipt, expected in ((self.positive(),c.DECISION_PERMIT),(self.denial("fork"),c.DECISION_DENY)):
            self.assertEqual("REJECTED",self.fork_result(receipt))
            self.assertEqual(expected,c.validate_receipt(receipt,expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        r=self.positive(); self.assertEqual("REJECTED",self.fork_result(r,True)); self.assertEqual(c.DECISION_PERMIT,c.validate_receipt(r,expected_scope=c.REGISTERED_POSITIVE_SCOPE))

    def test_r9_09_receipt_reconstruction_and_cross_scope_controls(self):
        r=self.positive(); self.reject(c.IssuedReceipt())
        class Derived(c.IssuedReceipt): pass
        self.reject(Derived()); self.reject(dict(r)); self.reject(json.loads(json.dumps(dict(r))))
        for op in (lambda:copy.copy(r),lambda:copy.deepcopy(r),lambda:pickle.dumps(r)):
            with self.assertRaises(TypeError): op()
        other=self.positive(); self.assertNotEqual(r["authority_instance_id"],other["authority_instance_id"]); self.assertNotEqual(r["receipt_digest"],other["receipt_digest"])
        for field,prefix in c._SCOPE_PREFIXES.items():
            self.reject(r,self.changed_scope(field,prefix+"other"))

    def test_r9_10_exact_basis_scope_and_current_boundaries_preserved(self):
        for field,prefix in c._SCOPE_PREFIXES.items():
            scope=self.changed_scope(field,prefix+"changed")
            r=c.issue_noncurrent_synthetic_receipt(scope=scope,basis_id=c.REGISTERED_POSITIVE_BASIS_ID); self.addCleanup(r.close)
            self.assertEqual(c.DECISION_DENY,c.validate_receipt(r,expected_scope=scope))
        current={
            "actor_id":"urn:rawlsing:v3:actor:project-current:a",
            "world_id":"urn:rawlsing:v3:world:project-current:w",
            "subject_id":CANARY,
            "time_id":"urn:rawlsing:v3:time:project-current:t",
            "transition_id":"urn:rawlsing:v3:transition:project-current:tr",
        }
        for field,value in current.items():
            with self.assertRaises(c.PermissionContractError): c.issue_noncurrent_synthetic_receipt(scope=self.changed_scope(field,value),basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
        for basis in ("ADP-010","ADP-019::OCCURRENCE_ADMITTED","ROUTED_TO_SAME_ENDPOINT","COLOCATED_SAME_TIME_AND_PLACE","NARRATIVE_PLAUSIBILITY"):
            r=c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id=basis); self.addCleanup(r.close)
            self.assertEqual(c.DECISION_DENY,c.validate_receipt(r,expected_scope=c.REGISTERED_POSITIVE_SCOPE))
        with self.assertRaises(c.PermissionContractError): c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id=c.REGISTERED_POSITIVE_BASIS_ID,fixture_class="PROJECT_CURRENT")

    def test_r9_11_repeated_concurrent_and_alias_module_isolation(self):
        r=self.positive()
        self.assertEqual([c.DECISION_PERMIT]*6,[c.validate_receipt(r,expected_scope=c.REGISTERED_POSITIVE_SCOPE) for _ in range(6)])
        with ThreadPoolExecutor(max_workers=6) as ex:
            self.assertEqual([c.DECISION_PERMIT]*18,list(ex.map(lambda _:c.validate_receipt(r,expected_scope=c.REGISTERED_POSITIVE_SCOPE),range(18))))
        spec=importlib.util.spec_from_file_location("obl058_r9_alias",Path(c.__file__)); alias=importlib.util.module_from_spec(spec); sys.modules[spec.name]=alias
        try:
            spec.loader.exec_module(alias)
            a=alias.issue_noncurrent_synthetic_receipt(scope=alias.REGISTERED_POSITIVE_SCOPE,basis_id=alias.REGISTERED_POSITIVE_BASIS_ID)
            try:
                with self.assertRaises(c.PermissionContractError): c.validate_receipt(a,expected_scope=c.REGISTERED_POSITIVE_SCOPE)
                with self.assertRaises(alias.PermissionContractError): alias.validate_receipt(r,expected_scope=alias.REGISTERED_POSITIVE_SCOPE)
            finally: a.close()
        finally: sys.modules.pop(spec.name,None)

    def test_r9_12_broker_child_and_endpoint_loss_fail_closed(self):
        for mode in ("broker","child","endpoint"):
            with self.subTest(mode=mode):
                out=self.isolated(f'''
                    import os, signal, socket, time
                    import causal_use_permission_candidate_r9 as c
                    r=c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
                    broker=c.native_broker_pid()
                    mode={mode!r}
                    server=None
                    if mode=="broker": os.kill(broker,signal.SIGTERM); time.sleep(0.1)
                    elif mode=="child":
                        f=f"/proc/{{broker}}/task/{{broker}}/children"; kids=[]
                        for _ in range(100):
                            try: kids=[int(v) for v in open(f).read().split()]
                            except FileNotFoundError: kids=[]
                            if kids: break
                            time.sleep(0.01)
                        if not kids: raise RuntimeError("child unavailable")
                        os.kill(kids[-1],signal.SIGTERM); time.sleep(0.05)
                    else:
                        p=c.native_broker_socket_path(); os.unlink(p); server=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM); server.bind(p); server.listen(1)
                    try: c.validate_receipt(r,expected_scope=c.REGISTERED_POSITIVE_SCOPE)
                    except Exception: print("REJECTED")
                    else: print("ACCEPTED")
                    finally:
                        if server: server.close()
                ''')
                self.assertEqual("REJECTED",out)

    def test_r9_13_no_public_peer_decision_registration_or_current_effect_surface(self):
        import inspect
        params=inspect.signature(c.issue_noncurrent_synthetic_receipt).parameters
        for name in ("decision","peer_pid","peer_uid","peer_starttime","authority_instance_id","basis_kind","explicit_source_permission"):
            self.assertNotIn(name,params)
        names=set(c.__dict__)
        for name in ("register_source_basis","execute_obl055","install_obl056_positive","create_encounter","realize_oee","create_actor","activate_actor","unblock_obl061"):
            self.assertNotIn(name,names)


if __name__ == "__main__":
    unittest.main(verbosity=2)
