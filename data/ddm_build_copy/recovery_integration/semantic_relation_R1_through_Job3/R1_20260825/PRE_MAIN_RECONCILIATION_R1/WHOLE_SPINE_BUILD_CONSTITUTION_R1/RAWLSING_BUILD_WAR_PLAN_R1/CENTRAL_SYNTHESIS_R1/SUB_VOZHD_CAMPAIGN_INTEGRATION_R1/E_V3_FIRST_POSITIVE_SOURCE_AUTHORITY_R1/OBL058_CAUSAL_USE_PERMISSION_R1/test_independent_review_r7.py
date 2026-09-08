"""Fresh distinct independent review for frozen OBL058 R7.

The court independently checks the R7 native lifecycle mechanism and preserved
source-origin semantics.  One blocking check intentionally asserts a reproduced
incorrect-positive path through ordinary Python runtime substitution.  A green
court therefore proves reproducibility; semantic disposition is recorded by the
reviewer separately.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import copy
import dis
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

import causal_use_permission_candidate_r7 as candidate  # noqa: E402
from causal_use_permission_candidate_r7 import (  # noqa: E402
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
    native_lifetime_reservation_count,
    validate_receipt,
)

CURRENT_FIRST_CANARY_SUBJECT = (
    "urn:rawlsing:v3:subject:sha256:"
    "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
)


class CallerProxy(dict):
    pass


def _bound_fast_constant(function, local_name):
    instructions = list(dis.get_instructions(function))
    for index, instruction in enumerate(instructions):
        if instruction.opname == "STORE_FAST" and instruction.argval == local_name:
            previous = instructions[index - 1]
            if previous.opname == "LOAD_CONST":
                return previous.argval
    raise AssertionError(f"bound constant not found: {local_name}")


class OBL058R7IndependentReview(unittest.TestCase):
    def positive(self):
        receipt = issue_noncurrent_synthetic_receipt(
            scope=REGISTERED_POSITIVE_SCOPE,
            basis_id=REGISTERED_POSITIVE_BASIS_ID,
        )
        self.addCleanup(receipt.close)
        return receipt

    def denial(self, suffix="r7-review-unregistered"):
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

    def run_isolated(self, body: str):
        script = "import sys\nfrom pathlib import Path\n" + f"sys.path.insert(0, {str(HERE)!r})\n" + textwrap.dedent(body)
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=str(HERE),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
            check=False,
        )
        if result.returncode != 0:
            self.fail(
                f"isolated review process failed rc={result.returncode}\n"
                f"stdout={result.stdout}\nstderr={result.stderr}"
            )
        return result.stdout.strip()

    # Baseline and R6 lifecycle regression.

    def test_r7i_01_valid_positive_and_negative_controls(self):
        self.assertEqual(
            DECISION_PERMIT,
            validate_receipt(self.positive(), expected_scope=REGISTERED_POSITIVE_SCOPE),
        )
        self.assertEqual(
            DECISION_DENY,
            validate_receipt(self.denial(), expected_scope=REGISTERED_POSITIVE_SCOPE),
        )

    def test_r7i_02_exact_authority_schema_and_mechanism(self):
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0", AUTHORITY_ID)
        self.assertEqual("OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0", SCHEMA_VERSION)
        self.assertEqual(
            "OBL058_CAUSAL_USE_PERMISSION_OBJECT_GENERATION_MECHANISM_R7@1.0.0",
            MECHANISM_REVISION,
        )

    def test_r7i_03_no_detachable_python_weakref_cleanup_controls_receipt(self):
        receipt = self.positive()
        with self.assertRaises(TypeError):
            weakref.ref(receipt)
        with self.assertRaises(TypeError):
            weakref.finalize(receipt, lambda: None)
        self.assertFalse(hasattr(receipt, "__dict__"))
        self.assertNotIn("weakref", candidate.issue_noncurrent_synthetic_receipt.__code__.co_names)

    def test_r7i_04_reference_release_keeps_native_generation_reserved(self):
        output = self.run_isolated(
            """
            import gc, json
            import causal_use_permission_candidate_r7 as c
            before = c.native_lifetime_reservation_count()
            r = c.issue_noncurrent_synthetic_receipt(
                scope=c.REGISTERED_POSITIVE_SCOPE,
                basis_id=c.REGISTERED_POSITIVE_BASIS_ID,
            )
            mid = c.native_lifetime_reservation_count()
            del r
            gc.collect()
            after = c.native_lifetime_reservation_count()
            print(json.dumps([before, mid, after]))
            """
        )
        before, mid, after = json.loads(output)
        self.assertEqual(before + 1, mid)
        self.assertEqual(mid, after)

    # Native identity and close invariants.

    def test_r7i_05_native_generation_state_not_exposed_as_assignable_python_attribute(self):
        receipt = self.positive()
        for name in ("authority_key", "_authority_key", "generation_key", "_generation_key"):
            with self.subTest(name=name):
                self.assertFalse(hasattr(receipt, name))
                with self.assertRaises(AttributeError):
                    object.__setattr__(receipt, name, 1)
        self.assertFalse(hasattr(candidate._native, "pin_head"))
        self.assertFalse(hasattr(candidate._native, "next_authority_key"))
        self.assertFalse(hasattr(candidate._native, "authority_key"))

    def test_r7i_06_explicit_close_revokes_before_reservation_release(self):
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

    def test_r7i_07_bounded_issue_close_cycles_return_reservation_count_to_baseline(self):
        baseline = native_lifetime_reservation_count()
        for index in range(40):
            receipt = issue_noncurrent_synthetic_receipt(
                scope=REGISTERED_POSITIVE_SCOPE,
                basis_id=(
                    REGISTERED_POSITIVE_BASIS_ID
                    if index % 2 == 0
                    else f"NONCURRENT_SYNTHETIC::basis::cycle-{index}"
                ),
            )
            expected = DECISION_PERMIT if index % 2 == 0 else DECISION_DENY
            self.assertEqual(expected, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))
            self.assertTrue(receipt.close())
            self.assert_origin_rejected(receipt)
        gc.collect()
        self.assertEqual(baseline, native_lifetime_reservation_count())

    # Process-generation and receipt separation.

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

    def test_r7i_08_forked_positive_and_negative_copies_reject_and_parent_survives(self):
        for label, receipt, expected in (
            ("permit", self.positive(), DECISION_PERMIT),
            ("deny", self.denial("fork"), DECISION_DENY),
        ):
            with self.subTest(label=label):
                self.assertEqual("REJECTED", self._fork_result(receipt))
                self.assertEqual("REJECTED", self._fork_result(receipt))
                self.assertEqual(expected, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_r7i_09_forked_close_cannot_retire_parent(self):
        receipt = self.positive()
        self.assertEqual("REJECTED", self._fork_result(receipt, do_close=True))
        self.assertEqual(DECISION_PERMIT, validate_receipt(receipt, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_r7i_10_equal_semantic_inputs_have_distinct_authority_instances(self):
        first = self.positive()
        second = self.positive()
        self.assertNotEqual(first["authority_instance_id"], second["authority_instance_id"])
        self.assertNotEqual(first["receipt_digest"], second["receipt_digest"])
        self.assertEqual(DECISION_PERMIT, validate_receipt(first, expected_scope=REGISTERED_POSITIVE_SCOPE))
        self.assertEqual(DECISION_PERMIT, validate_receipt(second, expected_scope=REGISTERED_POSITIVE_SCOPE))

    def test_r7i_11_reconstruction_copy_serialization_and_subclass_forms_reject(self):
        receipt = self.positive()
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
        self.assert_origin_rejected(dict(receipt))
        self.assert_origin_rejected(CallerProxy(dict(receipt)))
        self.assert_origin_rejected(json.loads(json.dumps(dict(receipt))))
        for operation in (lambda: copy.copy(receipt), lambda: copy.deepcopy(receipt), lambda: pickle.dumps(receipt)):
            with self.assertRaises(TypeError):
                operation()

    def test_r7i_12_cross_scope_validation_rejects_all_five_fields(self):
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
                with self.assertRaises(PermissionContractError):
                    validate_receipt(receipt, expected_scope=self.changed_scope(field, value))

    # Module/import behavior.

    def test_r7i_13_alias_import_keeps_authority_instances_separate(self):
        output = self.run_isolated(
            """
            import importlib.util, json, sys
            from pathlib import Path
            import causal_use_permission_candidate_r7 as c
            spec = importlib.util.spec_from_file_location("obl058_r7_alias_review", Path(c.__file__))
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
                    cross.append("ACCEPTED")
                except Exception:
                    cross.append("REJECTED")
            ids = [r1["authority_instance_id"], r2["authority_instance_id"]]
            r1.close(); r2.close()
            print(json.dumps({"own": own, "cross": cross, "distinct": ids[0] != ids[1]}))
            """
        )
        result = json.loads(output)
        self.assertEqual([DECISION_PERMIT, DECISION_PERMIT], result["own"])
        self.assertEqual(["REJECTED", "REJECTED"], result["cross"])
        self.assertTrue(result["distinct"])

    # Destructive process-loss checks are isolated from the main review process.

    def test_r7i_14_broker_loss_fails_closed(self):
        output = self.run_isolated(
            """
            import dis, os, signal, time
            import causal_use_permission_candidate_r7 as c
            def bound(name):
                ins = list(dis.get_instructions(c._r6._bound_broker_request))
                for i, op in enumerate(ins):
                    if op.opname == 'STORE_FAST' and op.argval == name and ins[i-1].opname == 'LOAD_CONST':
                        return ins[i-1].argval
                raise RuntimeError(name)
            r = c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE, basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
            pid = bound('_pid')
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

    def test_r7i_15_authority_child_loss_fails_closed(self):
        output = self.run_isolated(
            """
            import dis, os, signal, time
            import causal_use_permission_candidate_r7 as c
            def bound(name):
                ins = list(dis.get_instructions(c._r6._bound_broker_request))
                for i, op in enumerate(ins):
                    if op.opname == 'STORE_FAST' and op.argval == name and ins[i-1].opname == 'LOAD_CONST':
                        return ins[i-1].argval
                raise RuntimeError(name)
            r = c.issue_noncurrent_synthetic_receipt(scope=c.REGISTERED_POSITIVE_SCOPE, basis_id=c.REGISTERED_POSITIVE_BASIS_ID)
            broker = bound('_pid')
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

    # Blocking family: mutable Python socket constructor substitutes the bound broker exchange.

    def test_r7i_b01_mutable_socket_constructor_can_return_permit_without_source_broker_decision(self):
        output = self.run_isolated(
            """
            import dis, json, socket, struct
            import causal_use_permission_candidate_r7 as c

            def bound(name):
                ins = list(dis.get_instructions(c._r6._bound_broker_request))
                for i, op in enumerate(ins):
                    if op.opname == 'STORE_FAST' and op.argval == name and ins[i-1].opname == 'LOAD_CONST':
                        return ins[i-1].argval
                raise RuntimeError(name)

            expected_pid = bound('_pid')
            expected_uid = bound('_uid')
            real_socket = socket.socket

            # Genuine source path first: this basis is not registered and must DENY.
            genuine = c.issue_noncurrent_synthetic_receipt(
                scope=c.REGISTERED_POSITIVE_SCOPE,
                basis_id='NONCURRENT_SYNTHETIC::basis::independent-socket-control',
            )
            genuine_decision = c.validate_receipt(genuine, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
            genuine.close()

            class SubstitutedSocket:
                def __init__(self, *args, **kwargs):
                    self.response = b''
                def settimeout(self, value):
                    pass
                def connect(self, path):
                    pass
                def getsockopt(self, level, option, size):
                    return struct.pack('3i', expected_pid, expected_uid, 0)
                def sendall(self, wire):
                    request = json.loads(wire.decode('utf-8').split('\\n', 1)[0])
                    response = {'ok': True, 'request_id': request['request_id']}
                    if request['op'] == 'issue':
                        response['body_json'] = json.dumps({'decision': 'PERMIT'}, separators=(',', ':'))
                        response['authority_instance_id'] = 'substituted-runtime-response'
                    elif request['op'] == 'validate':
                        response['decision'] = 'PERMIT'
                        response['authority_instance_id'] = 'substituted-runtime-response'
                    elif request['op'] == 'close':
                        response['closed'] = True
                    elif request['op'] == 'ping':
                        response['pong'] = True
                    self.response = (json.dumps(response, separators=(',', ':')) + '\\n').encode('utf-8')
                def recv(self, size):
                    if self.response:
                        result = self.response
                        self.response = b''
                        return result
                    return b''
                def close(self):
                    pass

            socket.socket = SubstitutedSocket
            try:
                receipt = c.issue_noncurrent_synthetic_receipt(
                    scope=c.REGISTERED_POSITIVE_SCOPE,
                    basis_id='NONCURRENT_SYNTHETIC::basis::independent-socket-control',
                )
                observed = c.validate_receipt(receipt, expected_scope=c.REGISTERED_POSITIVE_SCOPE)
                receipt.close()
            finally:
                socket.socket = real_socket

            print(json.dumps({'genuine': genuine_decision, 'substituted': observed}))
            """
        )
        result = json.loads(output)
        self.assertEqual(DECISION_DENY, result["genuine"])
        # This assertion intentionally records the independently reproduced blocker.
        self.assertEqual(DECISION_PERMIT, result["substituted"])

    # Semantic/current-state preservation controls.

    def test_r7i_16_registered_basis_exact_binding_across_scope_fields(self):
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

    def test_r7i_17_project_current_namespaces_and_exact_canary_reject(self):
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

    def test_r7i_18_surrogate_basis_strings_deny(self):
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

    def test_r7i_19_repeated_and_concurrent_validation_stable(self):
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

    def test_r7i_20_no_registration_or_project_current_effect_surfaces(self):
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
