"""J42 W41 isolated driver: fresh ObjectiveWorld reads for all 84 views.

Run inside the W41 staged environment (its own bootstrap/reconstructed owners);
writes one JSON receipt. Creation timestamps are excluded from the scientific
projection; the returned W41 artifact bank is dereferenced by hash for custody.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
W41 = PACKET / "vendor/w41"
sys.path.insert(0, str(W41))
import w41_bootstrap  # noqa: E402,F401  (reconstructs owners; isolated process)
import objective_world as ow  # noqa: E402


def _view(material):
    consumer = material["native_consumer"]["material"]
    return dict(
        family=material["family"],
        clock=material["clock"],
        budget_tokens=material["budget_tokens"],
        snapshot_hash=material["snapshot_hash"],
        acceptance=material["acceptance"],
        content_hash=material["content_hash"],
        grade=material["grade"],
        operative_N9=material["operative_N9"],
        route_probability=material["route_probability"],
        learned_binding=material["learned_binding"],
        structural_values={
            key: {name: value.get(name) for name in
                  ("value", "state", "unit", "revision", "publication",
                   "effective_from", "field_ref", "requested_ref")}
            for key, value in material["structural_values"].items()},
        native_consumer=dict(
            state=consumer["state"],
            routes={key: value["state"]
                    for key, value in consumer["structural_routes"].items()},
            empirical_steps=[
                dict(target=step["target"],
                     conditioners=[list(c) for c in step["conditioners"]],
                     denominator=step["denominator"],
                     cells={cell["cell"]: cell["raw_numerator_support"]
                            for cell in step["cells"]})
                for step in consumer["empirical"]["steps"]],
            source_balance=[row["source_balance_count"]
                            for row in consumer["source_balance_reads"]],
            route_probability=consumer.get("route_probability"),
            route_probability_reason=consumer.get("route_probability_reason")))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    worlds = {}
    for family in ow.FAMILIES:
        world = ow.ObjectiveWorld(family)
        for mode in ow.CLOCKS:
            for budget in (0, 2, 5, 10):
                worlds[f"{family}/{mode}/budget{budget}"] = _view(
                    world.read(mode, budget=budget))
    multifield = {f"W{i}": ow.f6_evidence(f"W{i}") for i in range(1, 9)}
    temporal = ow.temporal_methods()
    purposes = ow.purpose_refusals()
    retained = ow.context_read_or_refusal()
    position = ow.position_context()
    fields = ow.independent_fields()
    evidence_view = ow.ObjectiveWorld().evidence_view("W2")
    evidence_view_hold = dict(
        matching_decision=evidence_view["matching_decision"],
        route_probability=evidence_view["route_probability"],
        content_hash=evidence_view["content_hash"],
        has_retained_gt2_link=False)
    custody = {}
    for name in ("objective_world.py", "P41_A41_HAND_BACK.json",
                 "current_historical_asof_world_consumer_receipts.json",
                 "00_FROZEN_CONSUMER_ORACLE.json",
                 "01_FROZEN_BREADTH_SUPPLEMENT.json"):
        local = W41 / name
        if local.exists():
            data = local.read_bytes()
        else:
            # Large returned artifacts are pinned by git object identity
            # instead of being duplicated on this branch.
            proc = subprocess.run(
                ["git", "-C", str(PACKET.parents[1]), "cat-file", "blob",
                 "b0a68e4ff5d5e2ca62b080376fda6b5f5431a6c2:"
                 "WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/" + name],
                capture_output=True)
            if proc.returncode != 0:
                raise RuntimeError("W41 returned artifact unavailable: " + name)
            data = proc.stdout
        custody[name] = dict(sha256=hashlib.sha256(data).hexdigest(),
                             bytes=len(data))
    payload = dict(
        schema="J42_W41_FRESH_RUN@1",
        source_commit="b0a68e4ff5d5e2ca62b080376fda6b5f5431a6c2",
        contract="W41_READONLY_SOURCE_QUALIFIED_WORLD@1",
        families=list(ow.FAMILIES), modes=list(ow.CLOCKS), budgets=[0, 2, 5, 10],
        worlds=worlds,
        retained_context=retained,
        position_context=position,
        independent_fields=fields,
        multifield=multifield,
        temporal=temporal,
        purposes=purposes,
        evidence_view_hold=evidence_view_hold,
        returned_artifact_custody=custody,
        no_original_source_read=True)
    Path(args.out).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"views": len(worlds),
                      "purposes": sorted(purposes),
                      "retained_state": retained.get("state"),
                      "multifield_states": {k: v["state"] for k, v in multifield.items()}},
                     indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
