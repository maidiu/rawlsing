"""PYAT HQ282 P04 — evidence recorder for the selected-world progressive contract.

Executes the full P04 chain and records the evidence as JSON.
Source-free: no raw data, no real subjects, no G0b/B5/Field-Forge.
"""

from __future__ import annotations

import json
import pathlib
import time

import rawlsing_next.pre553_selected_world_progressive_contract as p04
import rawlsing_next.pre553_n9_n10w_progressive_candidate as pc


def main() -> dict:
    started = time.time()
    contract, world = p04.select_world()
    chain = p04.run_selected_world_progressive_chain(contract, world=world)
    checks = p04.verify_chain_preserves_contract(contract, chain)
    elapsed = time.time() - started

    evidence = {
        "contract_id": contract.contract_id,
        "contract_content_hash": p04.contract_content_hash(contract),
        "world_tag": contract.world_tag,
        "real_current": contract.real_current,
        "selection_metadata": dict(contract.selection_metadata),
        "steps": [],
        "f8_consumptions": [],
        "invocation_log": [],
        "checks": dict(checks),
        "effects": dict(p04.effects()),
        "elapsed_seconds": round(elapsed, 3),
    }

    for step in chain.steps:
        evidence["steps"].append({
            "step_id": step.step_id,
            "conditioners": [list(c) for c in step.conditioners],
            "producer_route": step.producer_route,
            "producer_fact_state": step.producer_fact_state,
            "raw_denominator_support": step.raw_denominator_support,
            "cells": {k: {
                "raw_numerator_support": v["raw_numerator_support"],
                "raw_probability_exact_fraction": v["raw_probability_exact_fraction"],
            } for k, v in step.cells.items()},
            "consumer_state": step.consumer_state,
            "release_ref": step.release_ref.as_dict(),
            "risk_set_ref": dict(step.risk_set_ref),
            "uncertainty_state": step.uncertainty_state,
            "produced_evidence_ref": step.produced_evidence.evidence_ref.as_dict(),
        })

    for cons in chain.f8_consumptions:
        evidence["f8_consumptions"].append(dict(cons))

    for entry in chain.invocation_log:
        evidence["invocation_log"].append(dict(entry))

    return evidence


if __name__ == "__main__":
    result = main()
    out = pathlib.Path(__file__).parent / "p04_evidence.json"
    out.write_text(json.dumps(result, indent=2, default=str))
    print(f"evidence written to {out}")
    print(f"steps: {len(result['steps'])}, f8: {len(result['f8_consumptions'])}, "
          f"elapsed: {result['elapsed_seconds']}s")
    print(f"checks: {result['checks']}")
