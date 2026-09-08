"""Fresh distinct independent review for frozen OBL058 R10.

This is review-only.  The frozen candidate is imported and observed; it is never
modified.  One check intentionally reproduces the smallest source-binding
finding so a green governed court can support semantic FAIL.
"""
from __future__ import annotations

import copy
from concurrent.futures import ThreadPoolExecutor
import gc
import hashlib
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

import causal_use_permission_candidate_r10 as c  # noqa: E402

CANARY = (
    "urn:rawlsing:v3:subject:sha256:"
    "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
)


class ReviewProxy(dict):
    pass


class OBL058R10IndependentReview(unittest.TestCase):
    def positive(self):
        receipt = c.issue_noncurrent_synthetic_receipt(
            scope=c.REGISTERED_POSITIVE_SCOPE,
            basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(receipt.close)
        return receipt

    def denial(self, suffix="r10-independent-deny"):
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

    def test_01_genuine_permit_deny_and_revision(self):
        self.assertEqual(
            c.DECISION_PERMIT,
            c.validate_receipt(self.positive(), expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(
            c.DECISION_DENY,
            c.validate_receipt(self.denial(), expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(
            "OBL058_CAUSAL_USE_PERMISSION_PUBLIC_NATIVE_DISPATCH_R10@1.0.0",
            c.MECHANISM_REVISION,
        )

    def test_02_r9_class_method_replacement_does_not_redirect_saved_validator(self):
        receipt = self.denial("r9-regression")
        validator = c.validate_receipt
        original = c.IssuedReceipt._source_validate
        calls = []

        def substituted(self, scope):
            calls.append(scope)
            return c.DECISION_PERMIT, receipt["authority_instance_id"]

        before = c.native_transport_success_count()
        c.IssuedReceipt._source_validate = substituted
        try:
            self.assertEqual(
                c.DECISION_DENY,
                validator(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
            self.assertEqual([], calls)
            self.assertGreater(c.native_transport_success_count(), before)
        finally:
            c.IssuedReceipt._source_validate = original

    def test_03_descriptor_and_getattribute_replacement_do_not_redirect_saved_validator(self):
        receipt = self.denial("descriptor")
        validator = c.validate_receipt
        original_validate = c.IssuedReceipt._source_validate
        original_getattribute = c.IssuedReceipt.__getattribute__

        class RedirectDescriptor:
            def __get__(self, obj, owner=None):
                return lambda scope: (
                    c.DECISION_PERMIT,
                    receipt["authority_instance_id"],
                )

        try:
            c.IssuedReceipt._source_validate = RedirectDescriptor()
            c.IssuedReceipt.__getattribute__ = lambda self, name: (
                (lambda scope: (c.DECISION_PERMIT, "substituted"))
                if name == "_source_validate"
                else original_getattribute(self, name)
            )
            self.assertEqual(
                c.DECISION_DENY,
                validator(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
        finally:
            c.IssuedReceipt._source_validate = original_validate
            c.IssuedReceipt.__getattribute__ = original_getattribute

    def test_04_preimport_genuine_dispatch_module_attribute_mediation_substitutes_public_validator(self):
        """Reproduce the smallest R10 blocker under ordinary module mutation.

        The real extension module remains in use and its actual ``__dict__``
        contains the genuine built-in functions.  A normal ModuleType subclass
        changes only ordinary attribute lookup for ``public_validate``.  R10's
        verifier inspects ``module.__dict__`` but later retrieves
        ``_dispatch.public_validate`` through ordinary module attribute lookup,
        so the two observations can disagree.
        """
        out = self.isolated(r'''
            import hashlib
            import importlib.util
            import sys
            import sysconfig
            import tempfile
            import types
            from pathlib import Path

            here = Path.cwd()
            source = here / "obl058_r10_dispatch.c"
            digest = hashlib.sha256(source.read_bytes()).hexdigest()[:20]
            suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
            output = (
                Path(tempfile.gettempdir())
                / "rawlsing_obl058_r10_dispatch"
                / f"py{sys.version_info.major}{sys.version_info.minor}"
                / f"_obl058_r10_dispatch_{digest}{suffix}"
            )
            if not output.exists():
                raise SystemExit("expected producer-built dispatch extension is absent")

            spec = importlib.util.spec_from_file_location("_obl058_r10_dispatch", output)
            module_object = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module_object)

            class module(types.ModuleType):
                def __getattribute__(self, name):
                    if name == "public_validate":
                        def substituted_validator(receipt, *, expected_scope):
                            return "PERMIT"
                        return substituted_validator
                    return super().__getattribute__(name)

            module_object.__class__ = module
            sys.modules["_obl058_r10_dispatch"] = module_object

            import causal_use_permission_candidate_r10 as candidate

            receipt = candidate.issue_noncurrent_synthetic_receipt(
                scope=candidate.REGISTERED_POSITIVE_SCOPE,
                basis_id="NONCURRENT_SYNTHETIC::basis::r10-review-module-dispatch-deny",
            )
            before = candidate.native_transport_success_count()
            result = candidate.validate_receipt(
                receipt, expected_scope=candidate.REGISTERED_POSITIVE_SCOPE
            )
            after = candidate.native_transport_success_count()
            print(result, after - before, candidate.validate_receipt.__class__.__name__)
            receipt.close()
        ''')
        # A green reproduction of this wrong-positive state is semantic FAIL.
        self.assertEqual("PERMIT 0 function", out)

    def test_05_plain_python_dispatch_cache_lookalike_rejects(self):
        out = self.isolated(r'''
            import hashlib, importlib.machinery, sys, sysconfig, tempfile, types
            from pathlib import Path
            source=Path.cwd()/"obl058_r10_dispatch.c"
            digest=hashlib.sha256(source.read_bytes()).hexdigest()[:20]
            suffix=sysconfig.get_config_var("EXT_SUFFIX") or ".so"
            output=Path(tempfile.gettempdir())/"rawlsing_obl058_r10_dispatch"/f"py{sys.version_info.major}{sys.version_info.minor}"/f"_obl058_r10_dispatch_{digest}{suffix}"
            m=types.ModuleType("_obl058_r10_dispatch")
            m.__file__=str(output)
            m.__spec__=importlib.machinery.ModuleSpec(m.__name__,None,origin=str(output))
            m.bind_contract=lambda *args: None
            m.public_validate=lambda *args,**kwargs: "PERMIT"
            m.bound_descriptor_identity=lambda: 1
            sys.modules[m.__name__]=m
            try:
                import causal_use_permission_candidate_r10
            except ImportError:
                print("REJECTED")
            else:
                print("ACCEPTED")
        ''')
        self.assertEqual("REJECTED", out)

    def test_06_postbinding_module_alias_and_cache_replacement_do_not_redirect_saved_validator(self):
        receipt = self.denial("postbinding-cache")
        validator = c.validate_receipt
        genuine_dispatch = c._dispatch
        genuine_native = c._native
        try:
            c._dispatch = types.SimpleNamespace(public_validate=lambda *a, **k: "PERMIT")
            c._native = types.SimpleNamespace()
            sys.modules[c._DISPATCH_NAME] = types.ModuleType(c._DISPATCH_NAME)
            sys.modules[c._NATIVE_NAME] = types.ModuleType(c._NATIVE_NAME)
            self.assertEqual(
                c.DECISION_DENY,
                validator(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
        finally:
            c._dispatch = genuine_dispatch
            c._native = genuine_native
            sys.modules[c._DISPATCH_NAME] = genuine_dispatch
            sys.modules[c._NATIVE_NAME] = genuine_native

    def test_07_public_name_rebinding_does_not_change_saved_validator_object(self):
        receipt = self.denial("public-name")
        validator = c.validate_receipt
        original = c.validate_receipt
        try:
            c.validate_receipt = lambda *a, **k: c.DECISION_PERMIT
            self.assertEqual(
                c.DECISION_DENY,
                validator(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
        finally:
            c.validate_receipt = original

    def test_08_genuine_validator_is_native_and_advances_transport_for_both_decisions(self):
        builtin_type = [].append.__class__
        self.assertIs(c.validate_receipt.__class__, builtin_type)
        self.assertIs(c.validate_receipt.__self__, c._dispatch)
        for receipt, expected in (
            (self.positive(), c.DECISION_PERMIT),
            (self.denial("native-deny"), c.DECISION_DENY),
        ):
            with self.subTest(expected=expected):
                before = c.native_transport_success_count()
                self.assertEqual(
                    expected,
                    c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
                )
                self.assertGreater(c.native_transport_success_count(), before)

    def test_09_close_duplicate_close_and_stale_validation(self):
        receipt = c.issue_noncurrent_synthetic_receipt(
            scope=c.REGISTERED_POSITIVE_SCOPE,
            basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
        )
        self.assertEqual(
            c.DECISION_PERMIT,
            c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
        )
        self.assertTrue(receipt.close())
        self.reject(receipt)
        self.assertFalse(receipt.close())

    def test_10_native_lifetime_and_bounded_issue_close_cycles(self):
        with self.assertRaises(TypeError):
            weakref.ref(self.positive())
        baseline = c.native_lifetime_reservation_count()
        for index in range(12):
            basis = (
                c.REGISTERED_POSITIVE_BASIS_ID
                if index % 2 == 0
                else f"NONCURRENT_SYNTHETIC::basis::review-cycle-{index}"
            )
            expected = c.DECISION_PERMIT if index % 2 == 0 else c.DECISION_DENY
            receipt = c.issue_noncurrent_synthetic_receipt(
                scope=c.REGISTERED_POSITIVE_SCOPE,
                basis_id=basis,
            )
            self.assertEqual(
                expected,
                c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
            self.assertTrue(receipt.close())
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
                    c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
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

    def test_11_fork_requester_generation_and_parent_survival(self):
        for receipt, expected in (
            (self.positive(), c.DECISION_PERMIT),
            (self.denial("fork"), c.DECISION_DENY),
        ):
            with self.subTest(expected=expected):
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

    def test_12_reconstruction_subclass_mapping_json_copy_and_pickle_reject(self):
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

    def test_13_equal_semantic_inputs_keep_distinct_authority_instances(self):
        first = self.positive()
        second = self.positive()
        self.assertNotEqual(
            first["authority_instance_id"], second["authority_instance_id"]
        )
        self.assertNotEqual(first["receipt_digest"], second["receipt_digest"])

    def test_14_exact_five_field_scope_and_registered_basis_binding(self):
        for field, prefix in c._SCOPE_PREFIXES.items():
            with self.subTest(field=field):
                self.reject(self.positive(), self.changed_scope(field, prefix + "review-other"))
                changed = self.changed_scope(field, prefix + "review-changed")
                receipt = c.issue_noncurrent_synthetic_receipt(
                    scope=changed,
                    basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
                )
                self.addCleanup(receipt.close)
                self.assertEqual(
                    c.DECISION_DENY,
                    c.validate_receipt(receipt, expected_scope=changed),
                )

    def test_15_current_shaped_inputs_and_wrong_fixture_reject(self):
        replacements = {
            "actor_id": "urn:rawlsing:v3:actor:project-current:a",
            "world_id": "urn:rawlsing:v3:world:project-current:w",
            "subject_id": CANARY,
            "time_id": "urn:rawlsing:v3:time:project-current:t",
            "transition_id": "urn:rawlsing:v3:transition:project-current:tr",
        }
        for field, value in replacements.items():
            with self.subTest(field=field):
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

    def test_16_surrogate_and_unregistered_bases_remain_deny(self):
        for basis in (
            "ADP-010",
            "ADP-019::OCCURRENCE_ADMITTED",
            "ROUTED_TO_SAME_ENDPOINT",
            "NARRATIVE_PLAUSIBILITY",
            "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
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

    def test_17_repeated_and_concurrent_validation_remains_stable(self):
        receipt = self.positive()
        for _ in range(4):
            self.assertEqual(
                c.DECISION_PERMIT,
                c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
            )
        with ThreadPoolExecutor(max_workers=4) as pool:
            values = list(
                pool.map(
                    lambda _: c.validate_receipt(
                        receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE
                    ),
                    range(8),
                )
            )
        self.assertEqual([c.DECISION_PERMIT] * 8, values)

    def test_18_no_public_registration_or_current_effect_surfaces(self):
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
