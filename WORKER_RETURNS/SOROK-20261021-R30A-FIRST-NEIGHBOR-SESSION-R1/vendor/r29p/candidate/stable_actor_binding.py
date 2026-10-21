"""R27P stable explicit historical-actor injection into BP2P4J.

No global module function is rewritten. A narrow subclass overrides only the
BP2 producer's world-occurrence stage and sets the candidate life explicitly.
"""
from __future__ import annotations

import dataclasses
import json
import sqlite3
import sys
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import historical_actor_producer as H  # noqa: E402
import bp2_joined.producer as P  # noqa: E402

from bp2_joined.producer import JoinedProducer, build_world_occurrence  # noqa: E402
from bp2p4 import reunion as R  # noqa: E402
from bp2p4.product import JoinedProduct  # noqa: E402

# Explicit encounter cut variant, not a global mutation.
H.VARIANTS["NO_ENCOUNTER"] = dataclasses.replace(
    H.VARIANTS["A_REPAIR_LONG"], variant="NO_ENCOUNTER", joint_time=0,
    payment=0, task_hours=0)

_ORIGINAL_BUILDER = P.build_two_actor_life


class StableJoinedProducer(JoinedProducer):
    """Explicit source-owner injection; no global builder monkeypatch."""

    def __init__(self, root, *, variant: str, actor: str = "A"):
        self.historical_variant = variant
        self.historical_life = H.build_life(variant)
        super().__init__(root, actor=actor)

    def stage_world(self):
        self.stage = "world_occurrence"
        self.life = self.historical_life
        self.occurrence = build_world_occurrence(self.life, actor=self.actor_key)
        self.clock["value"] = self.occurrence.event_time
        return self.occurrence


def _product_result(product, artifacts, variant):
    observed = product.observe()
    waited = product.wait(30)
    other = product.other()
    offscreen = [product.store.world_event(product.branch_id, x)["kind"]
                 for x in waited["offscreen_events"]]
    c12_state = product.store.latest_state(product.branch_id)
    c12_clock = product.store.last_clock(product.branch_id)
    result = {
        "schema": "R27P_STABLE_PRODUCT@1",
        "variant": variant,
        "life": artifacts.life.historical_receipt,
        "actor_source_hash": artifacts.life.a_source.source_hash,
        "actor_id": artifacts.life.a_source.actor_id,
        "target_id": artifacts.target_id,
        "target_record_hash": artifacts.target_record_hash,
        "consumed_state_hash": artifacts.consumed_state_hash,
        "c8_state_digest": artifacts.c8_state_digest,
        "e1_event_hash": artifacts.e1_event_hash,
        "rule_a_hash": artifacts.rule_a_hash,
        "rule_t_hash": artifacts.rule_t_hash,
        "response_hash": artifacts.response_hash,
        "grant_hash": artifacts.grant_hash,
        "e2_receipt_hash": artifacts.e2_receipt_hash,
        "a0_claims": [c["kind"] for c in observed["claims"]],
        "a0_projects": observed["self"]["state"]["projects"],
        "a0_tools_remaining": observed["self"]["state"]["tools_remaining"],
        "a2_clock": waited["clock"],
        "a2_offscreen_kinds": offscreen,
        "a2_other_completed_units": other["public"]["completed_units"],
        "c12_world_hash": c12_state["world"]["hash"],
        "c12_clock": c12_clock,
        "native_claims": observed["native_claims"],
    }
    product.close()
    return result


def run_from_artifacts(artifacts, root, *, variant="A_REPAIR_LONG", e2="default"):
    product = JoinedProduct(Path(root), artifacts=artifacts, e2=e2)
    return _product_result(product, artifacts, variant)


def run_stable(variant="A_REPAIR_LONG", root=None):
    if P.build_two_actor_life is not _ORIGINAL_BUILDER:
        raise RuntimeError("GLOBAL_ACTOR_BUILDER_MUTATED")
    root = Path(root or (HERE.parent / "evidence" / "runtime" / variant))
    root.mkdir(parents=True, exist_ok=True)
    producer = StableJoinedProducer(root / "bp2", variant=variant)
    try:
        outcome = producer.run()
        if not outcome.ok:
            raise RuntimeError("BP2_PRODUCER_REFUSED:" + outcome.stage_reached + ":" + outcome.failure_code)
        receipt = outcome.receipt()
        persisted = receipt["persisted"]
        env = producer.env
        paths = {
            "journal_path": Path(persisted["journal_path"]),
            "key_path": env.key_path, "key_id": env.key_store.key_id,
            "anchor_log": env.anchor.log_path,
            "anchor_watermark": env.anchor.watermark_path,
            "c9_path": Path(persisted["c9_db_path"]),
        }
        artifacts = R._assemble(
            mode="FRESH", root=root / "bp2", life=producer.life,
            persisted=persisted, paths=paths, receipt=receipt, e2=None)
        result = run_from_artifacts(artifacts, root / "product", variant=variant)
        result["artifacts"] = artifacts
        return result
    finally:
        producer.close()


def assert_stable(result, *, expected_target=None, expected_source_hash=None):
    if expected_target is not None and result.get("target_id") != expected_target:
        raise AssertionError("R27P_TARGET_NOT_BOUND_TO_ACTOR_HISTORY")
    if expected_source_hash is not None and result.get("actor_source_hash") != expected_source_hash:
        raise AssertionError("R27P_ACTOR_SOURCE_NOT_BOUND")
    if result.get("a0_claims") != ["ARRIVAL"]:
        raise AssertionError("R27P_A0_CLAIMS:" + str(result.get("a0_claims")))
    if result.get("a0_tools_remaining") != 1:
        raise AssertionError("R27P_PRACTICE_TOOL_MISSING")
    if result.get("a2_clock") != 40:
        raise AssertionError("R27P_A2_CLOCK")
    if "OFFSCREEN_REPAIR" not in result.get("a2_offscreen_kinds", []):
        raise AssertionError("R27P_A2_OFFSCREEN_REPAIR_MISSING")
    if result.get("native_claims", {}).get("actor") is not False:
        raise AssertionError("R27P_NATIVE_ACTOR_CLAIM")
    return {"assertion": "r27p_stable_assertion", "status": "PASS",
            "target_id": result["target_id"],
            "actor_source_hash": result["actor_source_hash"],
            "a0_claims": result["a0_claims"], "a2": result["a2_clock"]}


def _trial(edge, baseline, run_red, restore):
    try:
        red = run_red()
        red_error = red.get("error", "")
    except Exception as exc:  # product construction refusal is RED
        red = {"status": "RED", "error": f"{type(exc).__name__}:{exc}"}
        red_error = str(exc)
    restored = restore()
    restored_ok = isinstance(restored, dict) and bool(restored.get("target_id"))
    return {
        "edge": edge,
        "baseline": {"status": "PASS", "target_id": baseline.get("target_id")},
        "red": red,
        "red_error": red_error,
        "restored": {"status": "PASS" if restored_ok else "RED",
                      "target_id": restored.get("target_id") if isinstance(restored, dict) else None},
        "proves": red.get("status") != "PASS" and restored_ok,
    }


def seven_actor_source_faults(tmp_root):
    tmp_root = Path(tmp_root); tmp_root.mkdir(parents=True, exist_ok=True)
    good = run_stable("A_REPAIR_LONG", tmp_root / "baseline")
    expected_target = good["target_id"]
    expected_source = good["actor_source_hash"]
    assert assert_stable(good, expected_target=expected_target,
                         expected_source_hash=expected_source)["status"] == "PASS"

    # 1. Actor genesis/source mutation.
    fault_life = dataclasses.replace(good["artifacts"].life)
    fault_life.a_source = dataclasses.replace(
        fault_life.a_source, source_ref=fault_life.a_source.source_ref + "_FAULTED")
    fault_artifacts = dataclasses.replace(good["artifacts"], life=fault_life)
    t1 = _trial("ACTOR_SOURCE_GENESIS",
                good, lambda: _red_from_artifacts(fault_artifacts, tmp_root / "t1",
                                                  expected_source),
                lambda: run_stable("A_REPAIR_LONG", tmp_root / "t1r"))

    # 2. A own omission removed.
    t2 = _trial("A_OWN_OMISSION",
                good, lambda: _checked_variant("A_NO_OMISSION", tmp_root / "t2", expected_target),
                lambda: run_stable("A_REPAIR_LONG", tmp_root / "t2r"))

    # 3. Independent B refusal removed.
    t3 = _trial("B_INDEPENDENT_ACT",
                good, lambda: _checked_variant("B_NO_REFUSAL", tmp_root / "t3", expected_target),
                lambda: run_stable("A_REPAIR_LONG", tmp_root / "t3r"))

    # 4. ADP010 encounter removed.
    t4 = _trial("ADP010_ENCOUNTER",
                good, lambda: _checked_variant("NO_ENCOUNTER", tmp_root / "t4", expected_target),
                lambda: run_stable("A_REPAIR_LONG", tmp_root / "t4r"))

    # 5. C8/E1 keyed proof cut: rewrite external anchor watermark.
    watermark = good["artifacts"].anchor_watermark
    original = watermark.read_bytes()
    doc = json.loads(original)
    doc["version"] = int(doc["version"]) + 1
    watermark.write_text(json.dumps(doc, sort_keys=True, separators=(",", ":")))
    def _restore5():
        watermark.write_bytes(original)
        return run_stable("A_REPAIR_LONG", tmp_root / "t5r")
    t5 = _trial("E1_C8_PROOF",
                good, lambda: _red_from_artifacts(good["artifacts"], tmp_root / "t5"),
                _restore5)

    # 6. Distinct A/T target/grant cut: delete target journal row.
    from bp2p4.severance import _cut_target_journal
    restore_target = _cut_target_journal(good["artifacts"])
    t6 = _trial("A_T_TARGET_GRANT",
                good, lambda: _red_from_artifacts(good["artifacts"], tmp_root / "t6"),
                lambda: (restore_target() or run_stable("A_REPAIR_LONG", tmp_root / "t6r")))

    # 7. Independent E2 cut: same committed target, no performed E2.
    t7 = _trial("INDEPENDENT_E2",
                good, lambda: _e2_cut(good["artifacts"], tmp_root / "t7", expected_target),
                lambda: run_stable("A_REPAIR_LONG", tmp_root / "t7r"))
    return {"baseline": good, "trials": [t1, t2, t3, t4, t5, t6, t7],
            "all_proved": all(t["proves"] for t in (t1, t2, t3, t4, t5, t6, t7))}


def _red_from_artifacts(artifacts, root, expected_source=None):
    result = run_from_artifacts(artifacts, root)
    try:
        assert_stable(result, expected_target=result["target_id"],
                      expected_source_hash=expected_source)
        return {"status": "PASS"}
    except AssertionError as exc:
        return {"status": "RED", "error": str(exc)}


def _checked_variant(variant, root, expected_target):
    result = run_stable(variant, root)
    try:
        assert_stable(result, expected_target=expected_target)
        return {"status": "PASS"}
    except AssertionError as exc:
        return {"status": "RED", "error": str(exc)}


def _e2_cut(artifacts, root, expected_target):
    result = run_from_artifacts(artifacts, root, e2=None)
    try:
        assert_stable(result, expected_target=expected_target)
        return {"status": "PASS"}
    except AssertionError as exc:
        return {"status": "RED", "error": str(exc)}
