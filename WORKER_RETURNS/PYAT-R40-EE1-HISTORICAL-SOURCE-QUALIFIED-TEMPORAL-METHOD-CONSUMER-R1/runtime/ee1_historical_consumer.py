"""EE1 historical comparison consumer.

Composes the ACTUAL accepted two-epoch selected-world receipts (staged T35
runtime) with the EE1 temporal verdict into one historical comparison product.
A synthetic/probe delta is never promoted to a measured historical delta; a
refused comparison yields typed nonavailability with a null delta; archival
receipts support archival comparison only.
"""
from __future__ import annotations

from ee1_world import N8E, serve_two_epochs
from ee1_temporal_owner import ARCHIVAL_COMPARISON_ONLY__NOT_FRESH_USE


def _routes(receipt):
    return {key: value["state"] for key, value in
            receipt["consumers"][0]["consumer_material"]["structural_routes"].items()}


def _steps(receipt):
    return [dict(denominator=s["denominator"],
                 cells={c["cell"]: c["raw_numerator_support"] for c in s["cells"]})
            for s in receipt["empirical_steps"]]


def accepted_epoch_facts():
    e1, e2, adapters = serve_two_epochs()
    r1, r2 = e1["receipt"], e2["receipt"]
    facts = {
        "E1": {
            "receipt_hash": r1["receipt_hash"],
            "snapshot_hash": r1["snapshot_hash"],
            "state": r1["state"],
            "fee": r1["structural_values"]["training_fee"]["value"],
            "exit_cost": r1["structural_values"]["exit_cost"]["value"],
            "fee_publication": r1["structural_values"]["training_fee"]["publication"],
            "fee_revision": r1["structural_values"]["training_fee"]["revision"],
            "routes": _routes(r1),
            "empirical_steps": _steps(r1),
            "publication_clocks": list(r1["publication_clocks"]),
            "effective_clocks": list(r1["effective_clocks"]),
        },
        "E2": {
            "receipt_hash": r2["receipt_hash"],
            "snapshot_hash": r2["snapshot_hash"],
            "state": r2["state"],
            "fee": r2["structural_values"]["training_fee"]["value"],
            "exit_cost": r2["structural_values"]["exit_cost"]["value"],
            "fee_publication": r2["structural_values"]["training_fee"]["publication"],
            "fee_revision": r2["structural_values"]["training_fee"]["revision"],
            "routes": _routes(r2),
            "empirical_steps": _steps(r2),
            "publication_clocks": list(r2["publication_clocks"]),
            "effective_clocks": list(r2["effective_clocks"]),
        },
    }
    return facts, (e1, e2, adapters)


def build_comparison_product(verdict, *, epochs=None, archival=False):
    facts, served = epochs if epochs is not None else accepted_epoch_facts()
    delta_block = None
    measured_delta = None
    if verdict.get("delta"):
        delta = dict(verdict["delta"])
        delta_block = delta
        if delta.get("delta_interpretation_permission"):
            measured_delta = delta["delta_value"]
    return {
        "schema": "PYAT_R40_EE1_HISTORICAL_COMPARISON_PRODUCT@1",
        "test_only": True,
        "sourcefree": True,
        "comparison_state": (ARCHIVAL_COMPARISON_ONLY__NOT_FRESH_USE if archival
                             else verdict["state"]),
        "institutional": {
            "rule_only_change": (facts["E1"]["fee"] == 2 and facts["E2"]["fee"] == 6
                                 and facts["E1"]["exit_cost"] == 2
                                 and facts["E2"]["exit_cost"] == 8),
            "training_route_changed": (facts["E1"]["routes"]["training"]
                                       != facts["E2"]["routes"]["training"]),
            "epochs": facts,
        },
        "empirical_channel": {
            "steps_identical": facts["E1"]["empirical_steps"]
            == facts["E2"]["empirical_steps"],
            "historical_measured_delta": measured_delta,
            "delta_block": delta_block,
        },
        "comparability": {
            "state": verdict["state"],
            "identity": verdict.get("identity"),
            "trusted_measurement": False,
        },
        "archival": {
            "archival_only": bool(archival),
            "fresh_use_authorized": not archival,
        },
        "authority": {
            "operative_N9": False, "operative_OC05": False,
            "installed_OC05": False, "ee12_issued": False,
            "ghana_claim": False, "n8e_product": False,
            "source_read": False, "actor_executions": 0, "model_calls": 0,
        },
        "ghana_hold": N8E.ghana_n03_state(),
        "ghana_null_all": N8E.ghana_null_checks()["all_null"],
    }, served


def archival_comparison(verdict, *, epochs=None):
    facts, served = epochs if epochs is not None else accepted_epoch_facts()
    adapters = served[2]
    archival_receipt = adapters[0].historical_receipt(
        facts["E1"]["receipt_hash"])
    product, _ = build_comparison_product(verdict, epochs=(facts, served),
                                          archival=True)
    product["archival_receipt"] = {
        "archival_only": archival_receipt["archival_only"],
        "fresh_use_authorized": archival_receipt["fresh_use_authorized"],
        "receipt_hash_removed": "receipt_hash" not in archival_receipt["receipt"],
    }
    return product
