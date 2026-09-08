"""Fresh distinct independent review for frozen OBL058 R8.

This court independently checks the R8 native broker-transport boundary and the
preserved receipt/lifecycle/semantic controls. One blocking check intentionally
records a reproduced incorrect-positive path through an ordinary Python import
cache substitution. A green court therefore proves the check executed as
designed; semantic disposition is recorded separately by the reviewer.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import copy
import gc
import importlib.util
import json
import os
from pathlib import Path
import pickle
import signal
import socket
import subprocess
import sys
import textwrap
import time
import types
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
    native_transport_success_count,
    validate_receipt,
)

CURRENT_FIRST_CANARY_SUBJECT = (
    "urn:rawlsing:v3:subject:sha256:"
    "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
)


class CallerProxy(dict):
    pass


class OBL058R8IndependentReview(unittest.TestCase):
    def positive(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(receipt.close)
        return receipt

    def denial(self, suffix="r8-review-unregistered"):
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

    def run_isolated(self, body: str, *, timeout=40):
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
                f"isolated review process failed rc={result.returncode}\n"
                f"stdout={result.stdout}\nstderr={result.stderr}"
            )
        return result.stdout.strip()

    def test_r8i_01_valid_positive_and_negative_controls(self):
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(self.positive(), expected_scope=REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(
            DECISION_DENY,
            validate_receipt(self.denial(), expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_r8i_02_exact_authority_schema_and_mechanism(self):
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0", AUTHORITY_ID)
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0", SCHEMA_VERSION)
        self.assertEqual(
            "OBL058_CAUSAL_USE_PERMISSION_BROKER_TRANSPORT_MECHANISM_R8@1.0.0",
            MECHANISM_REVISION,
        )

    def test_r8i_03_socket_constructor_rebinding_after_import_does_not_change_denial(self):
        real_socket = socket.socket

        class Replacement:
            def __init__(self, *args, **kwargs):
                raise AssertionError("Python socket constructor must not be used")

        socket.socket = Replacement
        try:
            receipt = issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id="NONCURRENT_SYNTHETIC::basis::r8-runtime-rebind",
            )
            self.addCleanup(receipt.close)
            self.assertEqual(
                DECISION_DENY,
                validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
            )
        finally:
            socket.socket = real_socket

    def test_r8i_04_socket_constructor_rebinding_before_import_does_not_change_denial(self):
        output = self.run_isolated(
            """
            import json, socket
            real_socket = socket.socket
            calls = []
            class Replacement:
                def __init__(self, *args, **kwargs):
                    calls.append('called')
                    raise AssertionError('parent Python socket constructor used')
            socket.socket = Replacement
            try:
                import causal_use_permission_candidate_r8 as c
                r = c.issue_noncurrent_synthetic_receipt(
                    scope=c.REGISTERED_POSITIVE_SCOPE,
                    basis_id='NONCURRENT_SYNTHETIC::basis::before-import',
                )
                decision = c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
                r.close()
                print(json.dumps({'decision': decision, 'calls': calls}))
            finally:
                socket.socket = real_socket
            """
        )
        result = json.loads(output)
        self.assertEqual(DECISION_DENY, result["decision"])
        self.assertEqual([], result["calls"])

    def test_r8i_05_low_level_socket_module_rebinding_before_import_does_not_change_denial(self):
        output = self.run_isolated(
            """
            import json, _socket
            real_socket = _socket.socket
            calls = []
            def replacement(*args, **kwargs):
                calls.append('called')
                raise AssertionError('parent _socket.socket used')
            _socket.socket = replacement
            try:
                import causal_use_permission_candidate_r8 as c
                r = c.issue_noncurrent_synthetic_receipt(
                    scope=c.REGISTERED_POSITIVE_SCOPE,
                    basis_id='NONCURRENT_SYNTHETIC::basis::low-level-rebind',
                )
                decision = c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
                r.close()
                print(json.dumps({'decision': decision, 'calls': calls}))
            finally:
                _socket.socket = real_socket
            """
        )
        result = json.loads(output)
        self.assertEqual(DECISION_DENY, result["decision"])
        self.assertEqual([], result["calls"])

    def test_r8i_b01_prepopulated_native_import_cache_can_substitute_source_decision(self):
        output = self.run_isolated(
            """
            import json, sys, types

            fake = types.ModuleType('_obl058_r8_native')

            class NativeReceiptBase:
                __slots__ = ('_fake_body', '_fake_live')
                def __init__(self):
                    self._fake_body = ''
                    self._fake_live = False
                def _source_issue(self, scope, basis_id, fixture_class):
                    self._fake_live = True
                    self._fake_body = json.dumps(
                        {'authority_instance_id': 'ordinary-import-cache-instance'},
                        separators=(',', ':'),
                    )
                    return self._fake_body
                def _source_validate(self, expected_scope):
                    if not self._fake_live:
                        raise ValueError('receipt_not_issued_by_source_authority')
                    return ('PERMIT', 'ordinary-import-cache-instance')
                def _source_close(self):
                    if not self._fake_live:
                        return False
                    self._fake_live = False
                    return True
                def _body_json_copy(self):
                    return self._fake_body
                def _is_source_issued(self):
                    return self._fake_live

            fake.NativeReceiptBase = NativeReceiptBase
            fake.start_broker = lambda script: None
            fake.pin_count = lambda: 0
            fake.close_success_count = lambda: 0
            fake.transport_success_count = lambda: 0
            fake.broker_pid = lambda: None
            fake.broker_path = lambda: None
            sys.modules['_obl058_r8_native'] = fake

            import causal_use_permission_candidate_r8 as c
            r = c.issue_noncurrent_synthetic_receipt(
                scope=c.REGISTERED_POSITIVE_SCOPE,
                basis_id='NONCURRENT_SYNTHETIC::basis::independent-import-cache-control',
            )
            observed = c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
            transport_count = c.native_transport_success_count()
            r.close()
            print(json.dumps({'observed': observed, 'transport_count': transport_count}))
            """
        )
        result = json.loads(output)
        # The genuine R8 source law for this unregistered basis is DENY. This
        # assertion intentionally records the independently reproduced blocker:
        # ordinary sys.modules prepopulation replaces the native core entirely.
        self.assertEqual(DECISION_PERMIT, result["observed"])
        self.assertEqual(0, result["transport_count"])

    def test_r8i_06_no_caller_peer_or_decision_parameters_exist(self):
        parameters = set(__import__('inspect').signature(issue_noncurrent_synthetic_receipt).parameters)
        for name in (
            "peer_pid", "peer_uid", "peer_starttime", "decision",
            "authority_instance_id", "explicit_source_permission", "basis_kind",
        ):
            self.assertNotIn(name, parameters)

    def test_r8i_07_native_transport_roundtrip_count_tracks_genuine_exchange(self):
        before = native_transport_success_count()
        receipt = self.denial("transport-count")
        mid = native_transport_success_count()
        self.assertGreater(mid, before)
        self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))
        self.assertGreater(native_transport_success_count(), mid)

    def test_r8i_08_unrelated_endpoint_replacement_fails_closed(self):
        output = self.run_isolated(
            """
            import os, socket
            import causal_use_permission_candidate_r8 as c
            r = c.issue_noncurrent_synthetic_receipt(
                scope=c.REGISTERED_POSITIVE_SCOPE,
                basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
            )
            path = c.native_broker_socket_path()
            moved = path + '.real'
            os.rename(path, moved)
            fake = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            fake.bind(path)
            fake.listen(1)
            try:
                try:
                    c.validate_receipt(r, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
                    print('ACCEPTED')
                except Exception:
                    print('REJECTED')
            finally:
                fake.close()
                try: os.unlink(path)
                except FileNotFoundError: pass
            """
        )
        self.assertEqual("REJECTED", output)

    def test_r8i_09_broker_loss_fails_closed(self):
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
            for _ in range(100):
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

    def test_r8i_10_authority_child_loss_fails_closed(self):
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
            for _ in range(100):
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

    def test_r8i_11_no_detachable_python_weakref_cleanup_controls_receipt(self):
        receipt = self.positive()
        with self.assertRaises(TypeError):
            weakref.ref(receipt)
        with self.assertRaises(TypeError):
            weakref.finalize(receipt, lambda: None)
        self.assertFalse(hasattr(receipt, "__dict__"))

    def test_r8i_12_explicit_close_duplicate_close_and_lifecycle_accounting(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        before = native_lifetime_reservation_count()
        self.assertEqual(DECISION_PERMIT, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))
        self.assertTrue(receipt.close())
        self.assertEqual(before - 1, native_lifetime_reservation_count())
        self.assert_origin_rejected(receipt)
        self.assertFalse(receipt.close())
        self.assert_origin_rejected(receipt)

    def test_r8i_13_bounded_issue_close_cycles_return_lifecycle_count_to_baseline(self):
        baseline = native_lifetime_reservation_count()
        for index in range(24):
            receipt = issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id=(
                    REGISTERED_POSITIVE_BASIS_ID
                    if index % 2 == 0
                    else f"NONCURRENT_SYNTHETIC::basis::r8-cycle-{index}"
                ),
            )
            expected = DECISION_PERMIT if index % 2 == 0 else DECISION_DENY
            self.assertEqual(expected, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))
            self.assertTrue(receipt.close())
        gc.collect()
        self.assertEqual(baseline, native_lifetime_reservation_count())

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

    def test_r8i_14_forked_positive_and_negative_copies_reject_and_parent_survives(self):
        for label, receipt, expected in (
            ("permit", self.positive(), DECISION_PERMIT),
            ("deny", self.denial("fork"), DECISION_DENY),
        ):
            with self.subTest(label=label):
                self.assertEqual("REJECTED", self._fork_result(receipt))
                self.assertEqual("REJECTED", self._fork_result(receipt))
                self.assertEqual(expected, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_r8i_15_forked_close_cannot_retire_parent(self):
        receipt = self.positive()
        self.assertEqual("REJECTED", self._fork_result(receipt, do_close=True))
        self.assertEqual(DECISION_PERMIT, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_r8i_16_equal_inputs_distinct_and_reconstruction_forms_reject(self):
        first = self.positive()
        second = self.positive()
        self.assertNotEqual(first["authority_instance_id"], second["authority_instance_id"])
        self.assertNotEqual(first["receipt_digest"], second["receipt_digest"])
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
        self.assert_origin_rejected(dict(first))
        self.assert_origin_rejected(CallerProxy(dict(first)))
        self.assert_origin_rejected(json.loads(json.dumps(dict(first))))
        for operation in (
            lambda: copy.copy(first),
            lambda: copy.deepcopy(first),
            lambda: pickle.dumps(first),
        ):
            with self.assertRaises(TypeError):
                operation()

    def test_r8i_17_cross_scope_validation_rejects_all_five_fields(self):
        receipt = self.positive()
        replacements = {
            "actor_id": "NONCURRENT_SYNTHETIC::actor::review-other",
            "world_id": "NONCURRENT_SYNTHETIC::world::review-other",
            "subject_id": "NONCURRENT_SYNTHETIC::subject::review-other",
            "time_id": "NONCURRENT_SYNTHETIC::time::review-other",
            "transition_id": "NONCURRENT_SYNTHETIC::transition::review-other",
        }
        for field, value in replacements.items():
            with self.subTest(field=field):
                self.assert_origin_rejected(receipt, self.changed_scope(field, value))

    def test_r8i_18_alias_import_keeps_receipt_types_separate(self):
        output = self.run_isolated(
            """
            import importlib.util, json, sys
            from pathlib import Path
            import causal_use_permission_candidate_r8 as c
            spec = importlib.util.spec_from_file_location('obl058_r8_alias_review', Path(c.__file__))
            alias = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = alias
            spec.loader.exec_module(alias)
            r1 = c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE, basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
            r2 = alias.issue_noncurrent_synthetic_receipt(scope=alias.REGISTERED_POSITIVE_SCOPE, basis_id=alias.REGISTERED_POSITIVE_BASIS_ID)
            own = [
                c.validate_receipt(r1, expected_scope=c.REGISTERED_POSITIVE_SCOPE),
                alias.validate_receipt(r2, expected_scope=alias.REGISTERED_POSITIVE_SCOPE),
            ]
            cross = []
            for fn, receipt, scope in (
                (c.validate_receipt, r2, c.REGISTERED_POSITIVE_SCOPE),
                (alias.validate_receipt, r1, alias.REGISTERED_POSITIVE_SCOPE),
            ):
                try:
                    fn(receipt, expected_scope=scope)
                    cross.append('ACCEPTED')
                except Exception:
                    cross.append('REJECTED')
            r1.close(); r2.close()
            print(json.dumps({'own': own, 'cross': cross}))
            """
        )
        result = json.loads(output)
        self.assertEqual([DECISION_PERMIT, DECISION_PERMIT], result["own"])
        self.assertEqual(["REJECTED", "REJECTED"], result["cross"])

    def test_r8i_19_registered_basis_exact_binding_across_scope_fields(self):
        replacements = {
            "actor_id": "NONCURRENT_SYNTHETIC::actor::different",
            "world_id": "NONCURRENT_SYNTHETIC::world::different",
            "subject_id": "NONCURRENT_SYNTHETIC::subject::different",
            "time_id": "NONCURRENT_SYNTHETIC::time::different",
            "transition_id": "NONCURRENT_SYNTHETIC::transition::different",
        }
        for field, value in replacements.items():
            with self.subTest(field=field):
                scope = self.changed_scope(field, value)
                receipt = issue_noncurrent_synthetic_receipt(scope=scope, basis_id=REGISTERED_POSITIVE_BASIS_ID)
                self.addCleanup(receipt.close)
                self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=scope))

    def test_r8i_20_project_current_namespaces_and_exact_canary_reject(self):
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

    def test_r8i_21_surrogate_basis_strings_deny(self):
        for basis_id in (
            "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
            "ADP-010",
            "ADP-019::OCCURRENCE_ADMITTED",
            "ROUTED_TO_SAME_ENDPOINT",
            "COLOCATED_SAME_TIME_AND_PLACE",
            "NARRATIVE_PLAUSIBILITY",
        ):
            with self.subTest(basis_id=basis_id):
                receipt = issue_noncurrent_synthetic_receipt(scope=REGISTERED_POSITIVE_SCOPE, basis_id=basis_id)
                self.addCleanup(receipt.close)
                self.assertEqual(DECISION_DENY, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_r8i_22_repeated_and_concurrent_validation_stable(self):
        receipt = self.positive()
        self.assertEqual([DECISION_PERMIT] * 8, [
            validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE)
            for _ in range(8)
        ])
        with ThreadPoolExecutor(max_workers=6) as executor:
            results = list(executor.map(
                lambda _: validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE),
                range(18),
            ))
        self.assertEqual([DECISION_PERMIT] * 18, results)

    def test_r8i_23_no_registration_or_project_current_effect_surfaces(self):
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
