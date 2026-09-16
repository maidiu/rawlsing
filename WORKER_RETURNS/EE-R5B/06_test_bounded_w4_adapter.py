from __future__ import annotations
import hashlib, importlib.util, json, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("r5b_bridge", HERE / "05_BOUNDED_W4_ADAPTER.py")
bridge = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(bridge)


def h(text): return hashlib.sha256(text.encode()).hexdigest()


def envelope(op, action):
    return {
        "schema": bridge.HARNESS_SCHEMA,
        "workload_id": "EE_R5B_MECHANICAL_QUALIFICATION",
        "plan_sha256": h("plan"),
        "step_ordinal": 0,
        "step_id": f"T_{op}_{action}",
        "universe_id": "EEU_LITS_I_2006_EXACT_SOURCE",
        "operation_id": op,
        "phase": "other",
        "action": action,
        "ee_requirement_ids": ["EE01"],
        "hostile_case_id": None,
        "request": {"qualification_fixture": "NO_EMPIRICAL_OUTCOME_USED"},
        "invalidation_targets": [] if "INVALIDATE" not in action else ["D04"],
    }


def good_owner(**kw):
    candidate = kw["candidate_id"]
    physical = {"accelerators": []}
    if candidate == "C":
        physical = {"accelerators": ["CACC1_LITS1_SEMANTIC_EXECUTION_BUNDLE", "CACC2_FRONTIER_ATOMIC_PREDICATE_RISK_MASK_BANK"]}
    return {
        "owner_binding": dict(kw["owner_binding"]),
        "semantic_output_sha256": h(candidate + kw["operation_id"] + kw["action"]),
        "identities": {"deterministic_output_identity": h("identity:" + kw["operation_id"])},
        "telemetry": {"source_open_count": 1, "source_decode_count": 1, "rewritten_bytes": 0},
        "physical_execution": physical,
    }


class BridgeTests(unittest.TestCase):
    def test_exact_27_cell_surface_accepts_bound_owner_receipts(self):
        primary_actions = {
            "EEW1-OP001":"EXECUTE", "EEW1-OP002":"EXECUTE", "EEW1-OP003":"EXECUTE",
            "EEW1-OP004":"EXECUTE", "EEW1-OP005":"EXECUTE", "EEW1-OP006":"EXECUTE",
            "EEW1-OP020":"REBUILD", "EEW1-OP021":"INVALIDATE_SOURCE", "EEW1-OP022":"INVALIDATE_AUTHORITY",
        }
        seen = []
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for candidate in "ABC":
                for op in bridge.OPERATIONS:
                    response = bridge.adapt_step(candidate, envelope(op, primary_actions[op]), scratch=root/candidate/op/"scratch", durable=root/candidate/op/"durable", owner_executor=good_owner)
                    self.assertEqual(response["status"], "OK")
                    self.assertEqual(len(response["semantic_output_sha256"]), 64)
                    seen.append((candidate, op))
        self.assertEqual(len(seen), 27)
        self.assertEqual(len(set(seen)), 27)

    def test_all_lifecycle_candidate_actions_translate(self):
        actions = {
            "EEW1-OP020": ["REBUILD", "REPLAY", "AUDIT"],
            "EEW1-OP021": ["REBUILD", "INVALIDATE_SOURCE", "REPLAY", "AUDIT"],
            "EEW1-OP022": ["REBUILD", "INVALIDATE_AUTHORITY", "REPLAY", "AUDIT"],
        }
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for candidate in "ABC":
                for op, values in actions.items():
                    for action in values:
                        out = bridge.adapt_step(candidate, envelope(op, action), scratch=root/"s", durable=root/"d", owner_executor=good_owner)
                        self.assertEqual(out["status"], "OK")

    def test_owner_pin_mismatch_rejected(self):
        def bad(**kw):
            r = good_owner(**kw); r["owner_binding"] = dict(r["owner_binding"]); r["owner_binding"]["blob"] = "0"*40; return r
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(bridge.BridgeError):
                bridge.adapt_step("A", envelope("EEW1-OP004", "EXECUTE"), scratch=Path(td)/"s", durable=Path(td)/"d", owner_executor=bad)

    def test_candidate_c_extra_accelerator_rejected(self):
        def bad(**kw):
            r = good_owner(**kw); r["physical_execution"] = {"accelerators":["CACC1_LITS1_SEMANTIC_EXECUTION_BUNDLE", "EXTRA_CACHE"]}; return r
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(bridge.BridgeError):
                bridge.adapt_step("C", envelope("EEW1-OP004", "EXECUTE"), scratch=Path(td)/"s", durable=Path(td)/"d", owner_executor=bad)

    def test_a_b_accelerators_rejected(self):
        def bad(**kw):
            r = good_owner(**kw); r["physical_execution"] = {"accelerators":["CACC1_LITS1_SEMANTIC_EXECUTION_BUNDLE"]}; return r
        with tempfile.TemporaryDirectory() as td:
            for c in "AB":
                with self.assertRaises(bridge.BridgeError):
                    bridge.adapt_step(c, envelope("EEW1-OP004", "EXECUTE"), scratch=Path(td)/"s", durable=Path(td)/"d", owner_executor=bad)

    def test_wrong_action_rejected(self):
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_w4_request("A", envelope("EEW1-OP001", "INVALIDATE_SOURCE"))

    def test_outside_operation_rejected(self):
        x = envelope("EEW1-OP001", "EXECUTE"); x["operation_id"] = "EEW1-OP007"
        with self.assertRaises(bridge.BridgeError): bridge.validate_w4_request("A", x)

    def test_invalid_telemetry_rejected(self):
        def bad(**kw):
            r = good_owner(**kw); r["telemetry"] = {"source_open_count": -1, "source_decode_count": 0}; return r
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(bridge.BridgeError):
                bridge.adapt_step("B", envelope("EEW1-OP005", "EXECUTE"), scratch=Path(td)/"s", durable=Path(td)/"d", owner_executor=bad)

    def test_ranking_field_rejected(self):
        def bad(**kw):
            r = good_owner(**kw); r["winner"] = "A"; return r
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(bridge.BridgeError):
                bridge.adapt_step("A", envelope("EEW1-OP006", "EXECUTE"), scratch=Path(td)/"s", durable=Path(td)/"d", owner_executor=bad)


if __name__ == "__main__": unittest.main(verbosity=2)
