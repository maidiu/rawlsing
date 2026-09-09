"""Fresh distinct independent review for frozen OBL058 R11.

Review-only. The frozen candidate is imported and exercised unchanged. A small
number of checks intentionally record any incorrect-positive public-path
substitution so governed execution can reproduce the semantic finding without
turning workflow color into the disposition itself.
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


class OBL058R11IndependentReview(unittest.TestCase):
    def positive(self):
        receipt = c.issue_noncurrent_synthetic_receipt(
            scope=c.REGISTERED_POSITIVE_SCOPE,
            basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(receipt.close)
        return receipt

    def denial(self, suffix="r11-independent-deny"):
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
            c._retained_validation_capability(
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

    def test_01_genuine_controls_and_exact_identity(self):
        self.assertEqual(
            c.DECISION_PERMIT,
            c._retained_validation_capability(
                self.positive(), expected_scope=c.REGISTERED_POSITIVE_SCOPE
            ),
        )
        self.assertEqual(
            c.DECISION_DENY,
            c._retained_validation_capability(
                self.denial(), expected_scope=c.REGISTERED_POSITIVE_SCOPE
            ),
        )
        self.assertEqual(
            "OBL058_CAUSAL_USE_PERMISSION_RETAINED_VALIDATION_CAPABILITY_R11@1.0.0",
            c.MECHANISM_REVISION,
        )
        self.assertIs(c._verified_public_validate, c._retained_validation_capability)
        self.assertIs(c.validate_receipt, c._retained_validation_capability)
        builtin_type = [].append.__class__
        self.assertIs(c._retained_validation_capability.__class__, builtin_type)
        self.assertIs(c._retained_validation_capability.__self__, c._capability_module)

    def test_02_saved_retained_capability_advances_native_transport_for_both_decisions(self):
        for receipt, expected in (
            (self.positive(), c.DECISION_PERMIT),
            (self.denial("transport-deny"), c.DECISION_DENY),
        ):
            before = c.native_transport_success_count()
            self.assertEqual(
                expected,
                c._retained_validation_capability(
                    receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE
                ),
            )
            self.assertGreater(c.native_transport_success_count(), before)

    def test_03_r10_capability_module_attribute_mediation_does_not_redirect_saved_capability(self):
        receipt = self.denial("r10-regression")
        validator = c._retained_validation_capability
        module_object = c._capability_module
        original_class = module_object.__class__
        calls = []

        class MediatedModule(types.ModuleType):
            def __getattribute__(self, name):
                if name in {"establish_capability", "public_validate"}:
                    calls.append(name)
                    return lambda *a, **k: c.DECISION_PERMIT
                return super().__getattribute__(name)

        module_object.__class__ = MediatedModule
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

    def test_04_candidate_public_export_rebinding_can_substitute_new_public_lookup(self):
        receipt = self.denial("public-export")
        saved = c._retained_validation_capability
        original = c.validate_receipt
        c.validate_receipt = lambda *a, **k: c.DECISION_PERMIT
        try:
            before = c.native_transport_success_count()
            observed = c.validate_receipt(
                receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE
            )
            after = c.native_transport_success_count()
            # Intentionally record the public-path result; a green check here is
            # semantic evidence, not a PASS recommendation.
            self.assertEqual(c.DECISION_PERMIT, observed)
            self.assertEqual(0, after - before)
            self.assertEqual(
                c.DECISION_DENY,
                saved(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
        finally:
            c.validate_receipt = original

    def test_05_candidate_module_attribute_mediation_can_substitute_public_lookup_without_changing_dict(self):
        receipt = self.denial("candidate-module-class")
        module_object = sys.modules[c.__name__]
        original_class = module_object.__class__
        genuine = module_object.__dict__["validate_receipt"]
        calls = []

        class MediatedCandidate(types.ModuleType):
            def __getattribute__(self, name):
                if name == "validate_receipt":
                    calls.append(name)
                    return lambda *a, **k: c.DECISION_PERMIT
                return super().__getattribute__(name)

        module_object.__class__ = MediatedCandidate
        try:
            self.assertIs(module_object.__dict__["validate_receipt"], genuine)
            before = c.native_transport_success_count()
            observed = module_object.validate_receipt(
                receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE
            )
            after = c.native_transport_success_count()
            self.assertEqual(c.DECISION_PERMIT, observed)
            self.assertEqual(0, after - before)
            self.assertEqual(["validate_receipt"], calls)
            self.assertEqual(
                c.DECISION_DENY,
                genuine(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
        finally:
            module_object.__class__ = original_class

    def test_06_fresh_imported_public_name_after_module_mediation_receives_substitute(self):
        receipt = self.denial("fresh-import")
        module_object = sys.modules[c.__name__]
        original_class = module_object.__class__

        class MediatedCandidate(types.ModuleType):
            def __getattribute__(self, name):
                if name == "validate_receipt":
                    return lambda *a, **k: c.DECISION_PERMIT
                return super().__getattribute__(name)

        module_object.__class__ = MediatedCandidate
        try:
            namespace = {}
            exec(
                "from causal_use_permission_candidate_r11 import validate_receipt as imported",
                namespace,
            )
            imported = namespace["imported"]
            before = c.native_transport_success_count()
            observed = imported(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
            after = c.native_transport_success_count()
            self.assertEqual(c.DECISION_PERMIT, observed)
            self.assertEqual(0, after - before)
        finally:
            module_object.__class__ = original_class

    def test_07_plain_python_capability_cache_lookalike_rejects(self):
        out = self.isolated(r'''
            import hashlib, importlib.machinery, sys, sysconfig, tempfile, types
            from pathlib import Path
            source=Path.cwd()/"obl058_r11_dispatch_capability.c"
            digest=hashlib.sha256(source.read_bytes()).hexdigest()[:20]
            suffix=sysconfig.get_config_var("EXT_SUFFIX") or ".so"
            output=Path(tempfile.gettempdir())/"rawlsing_obl058_r11_capability"/f"py{sys.version_info.major}{sys.version_info.minor}"/f"_obl058_r11_dispatch_capability_{digest}{suffix}"
            m=types.ModuleType("_obl058_r11_dispatch_capability")
            m.__file__=str(output); m.__spec__=importlib.machinery.ModuleSpec(m.__name__,None,origin=str(output))
            m.establish_capability=lambda *a:(lambda *x,**k:"PERMIT")
            m.public_validate=lambda *a,**k:"PERMIT"
            m.bound_descriptor_identity=lambda:1
            sys.modules[m.__name__]=m
            try: import causal_use_permission_candidate_r11
            except ImportError: print("REJECTED")
            else: print("ACCEPTED")
        ''')
        self.assertEqual("REJECTED", out)

    def test_08_loader_produced_python_capability_fails_closed(self):
        out = self.isolated(r'''
            import importlib.machinery, importlib.util, types
            real=importlib.util.spec_from_file_location
            class Loader:
                def create_module(self,spec):
                    m=types.ModuleType(spec.name); m.__file__=str(spec.origin); return m
                def exec_module(self,m):
                    m.establish_capability=lambda *a:(lambda *x,**k:"PERMIT")
                    m.public_validate=lambda *a,**k:"PERMIT"
                    m.bound_descriptor_identity=lambda:1
            importlib.util.spec_from_file_location=lambda name,path: importlib.machinery.ModuleSpec(name,Loader(),origin=str(path))
            try: import causal_use_permission_candidate_r11
            except Exception: print("REJECTED")
            else: print("ACCEPTED")
            finally: importlib.util.spec_from_file_location=real
        ''')
        self.assertEqual("REJECTED", out)

    def test_09_receipt_class_dispatch_replacement_does_not_redirect_retained_capability(self):
        receipt = self.denial("receipt-class")
        original = c.IssuedReceipt._source_validate
        calls = []

        def replacement(self, scope):
            calls.append(scope)
            return c.DECISION_PERMIT, receipt["authority_instance_id"]

        c.IssuedReceipt._source_validate = replacement
        try:
            self.assertEqual(
                c.DECISION_DENY,
                c._retained_validation_capability(
                    receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE
                ),
            )
            self.assertEqual([], calls)
        finally:
            c.IssuedReceipt._source_validate = original

    def test_10_sys_modules_replacement_after_establishment_does_not_redirect_saved_capability(self):
        receipt = self.denial("cache-after")
        validator = c._retained_validation_capability
        genuine_capability = c._capability_module
        genuine_native = c._native
        try:
            sys.modules[c._CAPABILITY_NAME] = types.ModuleType(c._CAPABILITY_NAME)
            sys.modules[c._NATIVE_NAME] = types.ModuleType(c._NATIVE_NAME)
            self.assertEqual(
                c.DECISION_DENY,
                validator(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
        finally:
            sys.modules[c._CAPABILITY_NAME] = genuine_capability
            sys.modules[c._NATIVE_NAME] = genuine_native

    def test_11_python_socket_constructor_rebinding_remains_irrelevant(self):
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
                c._retained_validation_capability(
                    receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE
                ),
            )
            self.assertEqual(0, FakeSocket.calls)
            self.assertGreater(c.native_transport_success_count(), before)
        finally:
            socket.socket = public
            _socket.socket = low

    def test_12_close_duplicate_close_and_lifecycle_accounting(self):
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
        for index in range(10):
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
                c._retained_validation_capability(
                    item, expected_scope=c.REGISTERED_POSITIVE_SCOPE
                ),
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
                    c._retained_validation_capability(
                        receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE
                    )
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

    def test_13_fork_requester_generation_and_parent_survival(self):
        for receipt, expected in (
            (self.positive(), c.DECISION_PERMIT),
            (self.denial("fork"), c.DECISION_DENY),
        ):
            self.assertEqual("REJECTED", self._fork_result(receipt))
            self.assertEqual(
                expected,
                c._retained_validation_capability(
                    receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE
                ),
            )
        receipt = self.positive()
        self.assertEqual("REJECTED", self._fork_result(receipt, close=True))
        self.assertEqual(
            c.DECISION_PERMIT,
            c._retained_validation_capability(
                receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE
            ),
        )

    def test_14_reconstruction_subclass_mapping_json_copy_and_pickle_reject(self):
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
        self.reject(json.loads(json.dumps(dict(receipt))))
        for operation in (
            lambda: copy.copy(receipt),
            lambda: copy.deepcopy(receipt),
            lambda: pickle.dumps(receipt),
        ):
            with self.assertRaises(TypeError):
                operation()

        second = self.positive()
        self.assertNotEqual(
            receipt["authority_instance_id"], second["authority_instance_id"]
        )
        self.assertNotEqual(receipt["receipt_digest"], second["receipt_digest"])

    def test_15_exact_five_field_scope_and_registered_basis_binding(self):
        for field, prefix in c._SCOPE_PREFIXES.items():
            self.reject(self.positive(), self.changed_scope(field, prefix + "review-other"))
            changed = self.changed_scope(field, prefix + "review-changed")
            receipt = c.issue_noncurrent_synthetic_receipt(
                scope=changed, basis_id=c.REGISTERED_POSITIVE_BASIS_ID
            )
            self.addCleanup(receipt.close)
            self.assertEqual(
                c.DECISION_DENY,
                c._retained_validation_capability(receipt, expected_scope=changed),
            )

    def test_16_current_shaped_wrong_fixture_and_surrogate_basis_controls(self):
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
                c._retained_validation_capability(
                    receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE
                ),
            )

    def test_17_repeated_and_concurrent_saved_capability_validation_is_stable(self):
        receipt = self.positive()
        for _ in range(5):
            self.assertEqual(
                c.DECISION_PERMIT,
                c._retained_validation_capability(
                    receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE
                ),
            )
        with ThreadPoolExecutor(max_workers=6) as executor:
            results = list(
                executor.map(
                    lambda _: c._retained_validation_capability(
                        receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE
                    ),
                    range(18),
                )
            )
        self.assertEqual([c.DECISION_PERMIT] * 18, results)

    def test_18_no_registration_or_project_current_effect_surfaces(self):
        names = set(c.__dict__)
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

    def test_19_broker_loss_fails_closed_in_isolated_process(self):
        out = self.isolated(r'''
            import os, signal, time
            import causal_use_permission_candidate_r11 as c
            r=c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE,basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
            pid=c.native_broker_pid()
            os.kill(pid, signal.SIGTERM)
            for _ in range(100):
                if not os.path.exists(f"/proc/{pid}"):
                    break
                time.sleep(0.01)
            try:
                c._retained_validation_capability(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
            except Exception: print("REJECTED")
            else: print("ACCEPTED")
        ''')
        self.assertEqual("REJECTED", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
