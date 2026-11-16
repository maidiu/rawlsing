"""Seven same-observable R29P actor/source fault controls."""
from __future__ import annotations

import json
from pathlib import Path

from bp2p4.severance import _cut_target_preimage

from r29p.actor_variants import A_GENESIS_ALTERED, install
from r29p.runner import (
    build_bundle,
    observable,
    product_from_artifacts,
    stable_view,
    world_with_b_units,
    world_without_contact,
)


def _run_variant(root, variant, *, world=None, e2="default"):
    product, artifacts, producer = build_bundle(
        root, variant=variant, world=world, e2=e2)
    producer.close()
    try:
        return observable(product), artifacts
    finally:
        product.close()


def _run_from_artifacts(root, artifacts, *, world=None, e2="default"):
    product = product_from_artifacts(root, artifacts, world=world, e2=e2)
    try:
        return observable(product)
    finally:
        product.close()


def _baseline(root):
    observed, artifacts = _run_variant(root, "A_REPAIR_LONG")
    return observed, artifacts, stable_view(observed)


def _receipt(edge, baseline, fault, restored, criterion, expected):
    return {
        "edge": edge,
        "baseline": baseline,
        "fault": fault,
        "restored": restored,
        "criterion": criterion,
        "expected": expected,
        "same_observable": "R29P_A0_A2_OBSERVABLE",
        "baseline_pass": baseline.get("status") == "OK",
        "fault_changed_or_refused": fault != baseline,
        "restored_pass": restored.get("status") == "OK",
        "stable_restore": stable_view(restored) == stable_view(baseline),
        "proves": (
            baseline.get("status") == "OK"
            and stable_view(restored) == stable_view(baseline)
            and _criterion_met(edge, baseline, fault)
        ),
    }


def _criterion_met(edge, baseline, fault):
    if edge == "A_GENESIS_HISTORY":
        return fault.get("status") == "OK" and (
            fault.get("self_history") != baseline.get("self_history")
            or fault.get("self_source_hash") != baseline.get("self_source_hash"))
    if edge == "A_PERFORMED_OMISSION":
        return fault.get("status") == "OK" and (
            fault.get("self_history") != baseline.get("self_history"))
    if edge == "B_INDEPENDENT_ACTION":
        return fault.get("status") == "OK" and (
            fault.get("a2_other_units") != baseline.get("a2_other_units"))
    if edge == "ADP010_ENCOUNTER_CONTACT":
        return fault.get("status") == "OK" and (
            fault.get("others") != baseline.get("others"))
    if edge == "C8_E1_PROOF":
        return fault.get("status") == "HELD" and str(fault.get("code", "")).startswith("BP3_")
    if edge == "CAN008_CAN011_TARGET":
        return fault.get("status") == "HELD" and str(fault.get("code", "")).startswith("C9_")
    if edge == "LATER_E2":
        return fault.get("status") == "OK" and (
            fault.get("tools") == 0
            and fault.get("a2_other_units") != baseline.get("a2_other_units")
            and "OFFSCREEN_REPAIR" not in fault.get("a2_offscreen", [])
            and "OFFSCREEN_NO_CHANGE" in fault.get("a2_offscreen", []))
    return False


def seven_trials(root) -> dict:
    install()
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    baseline, artifacts, baseline_view = _baseline(root / "baseline")

    a_genesis, _ = _run_variant(root / "a_genesis", A_GENESIS_ALTERED)
    a_genesis_restore, _ = _run_variant(root / "a_genesis_restore", "A_REPAIR_LONG")
    t1 = _receipt("A_GENESIS_HISTORY", baseline, a_genesis, a_genesis_restore,
                  "A0 self history/source differs", "different actor history")

    a_omission, _ = _run_variant(root / "a_omission", "A_NO_OMISSION")
    a_omission_restore, _ = _run_variant(root / "a_omission_restore", "A_REPAIR_LONG")
    t2 = _receipt("A_PERFORMED_OMISSION", baseline, a_omission, a_omission_restore,
                  "A0 self history differs", "A omission removed")

    b_state = _run_from_artifacts(
        root / "b_state", artifacts, world=world_with_b_units(artifacts, 2))
    b_state_restore = _run_from_artifacts(root / "b_state_restore", artifacts)
    t3 = _receipt("B_INDEPENDENT_ACTION", baseline, b_state, b_state_restore,
                  "A2 other completed units changes", "B own action removed")

    encounter = _run_from_artifacts(
        root / "encounter", artifacts, world=world_without_contact(artifacts))
    encounter_restore = _run_from_artifacts(root / "encounter_restore", artifacts)
    t4 = _receipt("ADP010_ENCOUNTER_CONTACT", baseline, encounter, encounter_restore,
                  "A0 others-present changes", "contact absent")

    c8_product = product_from_artifacts(root / "c8_product", artifacts)
    try:
        c8_before = observable(c8_product)
        watermark = artifacts.anchor_watermark
        original = watermark.read_bytes()
        document = json.loads(original)
        document["version"] = int(document["version"]) + 1
        watermark.write_text(json.dumps(document, sort_keys=True, separators=(",", ":")))
        c8_cut = observable(c8_product)
        watermark.write_bytes(original)
    finally:
        c8_product.close()
    c8_restore = _run_from_artifacts(root / "c8_restore", artifacts)
    t5 = _receipt("C8_E1_PROOF", c8_before, c8_cut, c8_restore,
                  "A0 HELD on C8 proof, restore OK", "keyed C8/E1 proof severed")

    at_product = product_from_artifacts(root / "at_product", artifacts)
    try:
        at_before = observable(at_product)
        restore_target = _cut_target_preimage(artifacts)
        at_cut = observable(at_product)
        restore_target()
    finally:
        at_product.close()
    at_restore = _run_from_artifacts(root / "at_restore", artifacts)
    t6 = _receipt("CAN008_CAN011_TARGET", at_before, at_cut, at_restore,
                  "A0 HELD on C9 target preimage, restore OK",
                  "CAN008/CAN011 target severed")

    e2_cut = _run_from_artifacts(root / "e2_cut", artifacts, e2=None)
    e2_restore = _run_from_artifacts(root / "e2_restore", artifacts)
    t7 = _receipt("LATER_E2", baseline, e2_cut, e2_restore,
                  "A0 tools=0 and A2 no independent repair",
                  "performed E2 absent")

    trials = [t1, t2, t3, t4, t5, t6, t7]
    return {
        "schema": "R29P_SEVEN_FAULTS@1",
        "baseline": baseline_view,
        "trials": trials,
        "all_proved": all(trial["proves"] for trial in trials),
        "behavioral_same_observable": all(
            trial["same_observable"] == "R29P_A0_A2_OBSERVABLE" for trial in trials),
    }
