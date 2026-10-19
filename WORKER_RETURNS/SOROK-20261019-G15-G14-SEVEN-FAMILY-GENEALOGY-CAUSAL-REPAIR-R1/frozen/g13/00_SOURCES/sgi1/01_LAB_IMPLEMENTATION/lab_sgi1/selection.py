"""Governed simulation-selection policy with full ADP020-style receipts.

PROVISIONAL_LAB_RULE__NOT_ADOPTED.
Distinctly recorded: hard feasibility | synthetic support | model plausibility |
simulation-selection weights. No verbal ranking becomes a fake frequency.
No unreported redraws. Scope hash never contains future-child material.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from .core import h_obj, h_concat, typed, S, ScopedRNG, Ledger

DECISION_KIND = "CONCEPTION_SCENARIO_SELECTION"
DECISION_SEMANTICS_VERSION = "SELECTION_DECISION_SEMANTICS@1.0-LAB"
STREAM = "v3.causal.adp015.conception_scenario_selection"

POLICIES = {
    "SIM_UNIFORM_CLASSES": {
        "method": "UNIFORM_CANDIDATE",
        "integer_weight_units": None,
        "status": "SIMULATION_POLICY",
        "no_claim_of_population_frequency_IF_SIMULATION": True,
    },
    "SIM_INTEGER_WEIGHT_A": {
        "method": "WEIGHTED_CANDIDATE_INTEGER",
        "integer_weight_units": [3, 2, 1, 1, 1, 1],
        "status": "SIMULATION_POLICY",
        "no_claim_of_population_frequency_IF_SIMULATION": True,
    },
    "SIM_INTEGER_WEIGHT_B": {
        "method": "WEIGHTED_CANDIDATE_INTEGER",
        "integer_weight_units": [1, 1, 3, 2, 1, 1],
        "status": "SIMULATION_POLICY",
        "no_claim_of_population_frequency_IF_SIMULATION": True,
    },
}


def policy_hash(policy_name: str) -> str:
    return h_obj({"policy": policy_name, "def": POLICIES[policy_name]})


def scope_hash(causal_run_id: str, mother_anchor_hash: str, target_hash: str,
               grammar_version: str) -> str:
    """Scope binds run+anchor+target+grammar+decision semantics ONLY.

    NEVER child outcome, mutable model wording, or transient loop count.
    """
    return h_concat(
        "GENEALOGY_SCOPE",
        causal_run_id,
        mother_anchor_hash,
        target_hash,
        grammar_version,
        DECISION_SEMANTICS_VERSION,
    )


def _weights_for(policy_name: str, n_classes: int) -> List[int]:
    p = POLICIES[policy_name]
    if p["method"] == "UNIFORM_CANDIDATE":
        return [1] * n_classes
    units = p["integer_weight_units"]
    if len(units) >= n_classes:
        return units[:n_classes]
    return units + [1] * (n_classes - len(units))


def adp020_select(policy_name: str, eligible_classes: List[Dict[str, Any]],
                  root_seed: str, scope: str, occurrence_index: int = 0,
                  force_index: Optional[int] = None,
                  upstream_class_set_hash: Optional[str] = None) -> Dict[str, Any]:
    """Deterministic selection over canonical class order.

    Deterministic singleton consumes ZERO draws. Every draw is receipted.
    force_index is used ONLY by explicitly-declared counterfactual test hooks
    (e.g. RETRY-BIAS forced-C1) and is recorded in the receipt as a declared
    intervention, never a silent redraw.
    """
    if policy_name not in POLICIES:
        return typed(S.SELECTION_AUTHORITY_UNBOUND,
                     reason="policy not registered", policy=policy_name)
    if not eligible_classes:
        return typed(S.SCENARIOS_VALID_EMPTY,
                     reason="no eligible classes; zero draws", n_draws=0)

    ordered = sorted(eligible_classes, key=lambda c: c["class_key"])
    # candidate_set_hash binds semantic classes only (class key + semantic-derived
    # representative id); phrasing multiplicity and input order cannot alter it.
    class_set_hash = h_obj(sorted(
        (c["class_key"], c["representative_id"]) for c in ordered
    ))
    n = len(ordered)
    weights = _weights_for(policy_name, n)
    total = sum(weights)

    rng = ScopedRNG(root_seed, STREAM, scope)
    ledger: Dict[str, Any] = {
        "decision_kind": DECISION_KIND,
        "decision_semantics_version": DECISION_SEMANTICS_VERSION,
        "stream": STREAM,
        "scope_hash": scope,
        "root_seed": root_seed,
        "policy_name": policy_name,
        "policy_hash": policy_hash(policy_name),
        "policy_status": POLICIES[policy_name]["status"],
        "no_population_frequency_claim": True,
        "candidate_set_hash": class_set_hash,
        "upstream_class_set_hash": upstream_class_set_hash,
        "canonical_class_order": [c["class_key"] for c in ordered],
        "eligible_set": [c["representative_id"] for c in ordered],
        "class_weights": [
            {"class_key": c["class_key"], "weight_units": w}
            for c, w in zip(ordered, weights)
        ],
        "total_weight_units": total,
        "occurrence_index": occurrence_index,
    }

    if n == 1 and force_index is None:
        ledger["draw"] = None
        ledger["draw_receipts"] = []
        ledger["n_draws"] = 0
        ledger["draw_mode"] = "DETERMINISTIC_SINGLETON_ZERO_DRAWS"
        chosen = ordered[0]
        ledger["selected_class_key"] = chosen["class_key"]
        ledger["selected_representative_id"] = chosen["representative_id"]
        ledger["status"] = S.COMMITTED
        ledger["unreported_redraws"] = 0
        return ledger

    if force_index is not None:
        chosen = ordered[force_index % n]
        ledger["draw"] = None
        ledger["draw_receipts"] = []
        ledger["n_draws"] = 0
        ledger["draw_mode"] = "DECLARED_TEST_INTERVENTION_FORCE_INDEX"
        ledger["declared_intervention"] = {"force_index": force_index}
        ledger["selected_class_key"] = chosen["class_key"]
        ledger["selected_representative_id"] = chosen["representative_id"]
        ledger["status"] = S.COMMITTED
        ledger["unreported_redraws"] = 0
        ledger["bias_note"] = (
            "declared counterfactual hook; NOT a stochastic draw; "
            "excluded from empirical acceptance-rate accounting"
        )
        return ledger

    rec = rng.draw(total, "conception_scenario_selection", class_set_hash,
                   occurrence_index)
    acc = 0
    chosen = ordered[-1]
    for c, w in zip(ordered, weights):
        acc += w
        if rec.draw_value < acc:
            chosen = c
            break
    ledger["draw"] = rec.as_dict()
    ledger["draw_receipts"] = [r.as_dict() for r in rng.draws]
    ledger["n_draws"] = rng.draw_count
    ledger["draw_mode"] = "SCOPED_DETERMINISTIC_STREAM"
    ledger["selected_class_key"] = chosen["class_key"]
    ledger["selected_representative_id"] = chosen["representative_id"]
    ledger["status"] = S.COMMITTED
    ledger["unreported_redraws"] = 0
    return ledger
