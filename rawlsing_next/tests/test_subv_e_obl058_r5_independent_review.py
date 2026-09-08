"""Governed wrapper for the fresh OBL058 R5 independent review.

This wrapper exposes the independently authored lane-local review court to the
bounded-court protocol. It does not modify the frozen semantic candidate.

The three overrides below correct runner-mechanics discovered by the first
execution: CPython address reuse is allocator-dependent, and a second dynamic
module must be registered in sys.modules before dataclass execution. The frozen
matrix and the deterministic forked-process source-origin finding are unchanged.
"""
from __future__ import annotations

import gc
import importlib.util
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL058_CAUSAL_USE_PERMISSION_R1/test_independent_review_r5.py"

spec = importlib.util.spec_from_file_location("_obl058_r5_independent_review_lane", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load OBL058 R5 independent review: {TARGET}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestOBL058R5IndependentReview(module.OBL058R5IndependentReview):
    """Expose the lane-local independent review TestCase to governed pytest."""

    def test_b02_stale_broker_record_accepts_new_exact_type_after_cpython_id_reuse(self):
        """Exercise stale identity state without making allocator reuse a prerequisite."""
        original = module.IssuedReceipt()
        response = self.direct_broker_issue(original)
        old_id = id(original)
        body_json = response["body_json"]
        del original
        gc.collect()

        replacement = None
        for _ in range(100000):
            probe = module.IssuedReceipt()
            if id(probe) == old_id:
                replacement = probe
                break
            del probe

        if replacement is not None:
            try:
                object.__setattr__(replacement, "_body_json", body_json)
                self.assertEqual(
                    module.DECISION_PERMIT,
                    module.validate_receipt(
                        replacement,
                        expected_scope=module.REGISTERED_POSITIVE_SCOPE,
                    ),
                )
            finally:
                replacement.close()
            return

        # The runner did not recycle this address in the bounded loop. Prove the
        # authoritative broker mapping nevertheless outlived the Python object:
        # the same integer identity remains occupied until explicitly closed.
        try:
            with self.assertRaisesRegex(
                module.PermissionContractError, "object_identity_already_issued"
            ):
                module.candidate._bound_broker_request({
                    "op": "issue",
                    "object_id": old_id,
                    "scope": module.REGISTERED_POSITIVE_SCOPE.canonical(),
                    "basis_id": module.REGISTERED_POSITIVE_BASIS_ID,
                    "fixture_class": module.FIXTURE_CLASS,
                    "request_id": module.uuid.uuid4().hex,
                })
        finally:
            module.candidate._bound_broker_request({
                "op": "close",
                "object_id": old_id,
                "request_id": module.uuid.uuid4().hex,
            })

    def test_b04_fork_child_can_recycle_inherited_id_after_clearing_copied_lifetime_pins(self):
        """Deterministically establish that process generation is absent from the key."""
        if not hasattr(os, "fork"):
            self.skipTest("fork unavailable")
        receipt = self.positive()
        parent_id = id(receipt)
        read_fd, write_fd = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(read_fd)
            try:
                child_id = id(receipt)
                decision = module.validate_receipt(
                    receipt,
                    expected_scope=module.REGISTERED_POSITIVE_SCOPE,
                )
                payload = f"{child_id}|{decision}".encode("utf-8")
            except Exception as exc:  # pragma: no cover - child report path
                payload = f"ERROR:{type(exc).__name__}:{exc}".encode("utf-8")
            try:
                os.write(write_fd, payload)
            finally:
                os.close(write_fd)
                os._exit(0)
        os.close(write_fd)
        payload = os.read(read_fd, 4096).decode("utf-8")
        os.close(read_fd)
        _child, status = os.waitpid(pid, 0)
        self.assertTrue(os.WIFEXITED(status))
        child_id_text, decision = payload.split("|", 1)
        self.assertEqual(parent_id, int(child_id_text))
        self.assertEqual(module.DECISION_PERMIT, decision)

    def test_e02_fresh_module_instance_does_not_accept_other_instance_receipt(self):
        script = r'''
import importlib.util, sys
from pathlib import Path
import causal_use_permission_candidate_r5 as a
path = Path(a.__file__).resolve()
spec = importlib.util.spec_from_file_location('obl058_r5_second_instance', path)
b = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = b
spec.loader.exec_module(b)
r = a.issue_noncurrent_synthetic_receipt(scope=a.REGISTERED_POSITIVE_SCOPE, basis_id=a.REGISTERED_POSITIVE_BASIS_ID)
try:
    b.validate_receipt(r, expected_scope=b.REGISTERED_POSITIVE_SCOPE)
    print('INCORRECT_POSITIVE')
except b.PermissionContractError:
    print('REJECTED')
'''
        result = module._run_isolated(script)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("REJECTED", result.stdout.strip())
