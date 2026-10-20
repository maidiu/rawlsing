"""Governed simulation-selection policy with full ADP020-style receipts.

PROVISIONAL_LAB_RULE__NOT_ADOPTED.
Distinctly recorded: hard feasibility | synthetic support | model plausibility |
simulation-selection weights. No verbal ranking becomes a fake frequency.
No unreported redraws. Scope hash never contains future-child material.

G13 REPAIR (defect family 6 -- selector integrity).

The pre-repair ``class_set_hash`` hashed only ``(class_key, representative_id)``.
A candidate whose substantive payload was mutated after deduplication therefore
kept an identical selection identity and an identical replay hash: "same ID,
changed payload" could masquerade as the same candidate. ADP-020 s10 requires an
immutable ``candidate_replay_hash`` per entry precisely to forbid that.

The repaired selector recomputes every candidate's authoritative replay hash from
its ACTUAL content and binds those hashes into the canonical candidate set, so a
stale class identity can no longer preserve selection authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from .core import h_obj, h_concat, typed, S, ScopedRNG, Ledger, RngAuthorityError

DECISION_KIND = "CONCEPTION_SCENARIO_SELECTION"
DECISION_SEMANTICS_VERSION = "SELECTION_DECISION_SEMANTICS@1.1-G13-REPAIRED"
STREAM = "v3.causal.adp015.conception_scenario_selection"

# Keys that constitute the class IDENTITY itself. Everything else in a candidate
# entry is substantive payload and is bound by its replay hash.
_CLASS_IDENTITY_KEYS = frozenset({"class_key", "representative_id"})

# Deduplication bookkeeping about HOW MANY paraphrases collapsed into a class.
# This is not candidate content: N phrasings of one scenario must not change the
# candidate's replay identity (the original dedup contract, and ADP-020's
# "phrasing multiplicity cannot alter the class set"). It is receipted in
# `merge_receipts` / `class_member_index` instead.
_MULTIPLICITY_KEYS = frozenset({"member_ids", "member_count"})

ADP020_CANDIDATE_SET_PREFIX = "ADP020_CANDIDATE_SET_V1\x00"

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


def candidate_replay_hash(entry: Dict[str, Any]) -> str:
    """ADP-020 s10 immutable per-candidate replay hash over ACTUAL content.

    Binds the substantive payload of the candidate entry, not merely its class
    identity, so a mutated payload cannot retain a stale class identity.

    Dedup multiplicity (``member_ids``/``member_count``) is deliberately NOT
    bound: how many paraphrases collapsed into a class is not candidate content,
    and binding it would let phrasing count alter the replay identity.
    """
    payload = {k: v for k, v in entry.items()
               if k not in _CLASS_IDENTITY_KEYS and k not in _MULTIPLICITY_KEYS}
    return h_obj({
        "candidate_id": entry.get("class_key"),
        "representative_id": entry.get("representative_id"),
        "bound_payload_keys": sorted(payload),
        "bound_payload": payload,
    })


def candidate_set_hash(ordered: List[Dict[str, Any]], weights: List[int],
                       policy_name: str) -> str:
    """ADP-020 s10.2 canonical candidate-set hash binding replay hashes."""
    entries = [
        {
            "candidate_id": e.get("class_key"),
            "representative_id": e.get("representative_id"),
            "candidate_replay_hash": candidate_replay_hash(e),
            "weight_units": w,
        }
        for e, w in zip(ordered, weights)
    ]
    entries.sort(key=lambda x: (str(x["candidate_id"]),
                                x["candidate_replay_hash"]))
    canonical = h_obj({
        "identity_mode": "SET_CANONICAL",
        "candidate_owner_authority": "SOROK_SOURCEFREE_GENEALOGY_LAB",
        "policy_name": policy_name,
        "entries": entries,
    })
    import hashlib as _h
    return "sha256:" + _h.sha256(
        ADP020_CANDIDATE_SET_PREFIX.encode("utf-8") + canonical.encode("utf-8")
    ).hexdigest()


def adp020_select(policy_name: str, eligible_classes: List[Dict[str, Any]],
                  root_seed: str, scope: str, occurrence_index: int = 0,
                  force_index: Optional[int] = None,
                  upstream_class_set_hash: Optional[str] = None) -> Dict[str, Any]:
    """Deterministic selection over canonical class order.

    Deterministic singleton consumes ZERO draws. Every draw is receipted.
    force_index is used ONLY by explicitly-declared counterfactual test hooks
    (e.g. RETRY-BIAS forced-C1) and is recorded in the receipt as a declared
    intervention, never a silent redraw.

    G13 repair: a malformed root seed is refused with a typed RNG failure BEFORE
    any draw, and the candidate-set hash binds actual candidate payload.
    """
    if policy_name not in POLICIES:
        return typed(S.SELECTION_AUTHORITY_UNBOUND,
                     reason="policy not registered", policy=policy_name)
    if not eligible_classes:
        return typed(S.SCENARIOS_VALID_EMPTY,
                     reason="no eligible classes; zero draws", n_draws=0)

    ordered = sorted(eligible_classes, key=lambda c: c["class_key"])
    n = len(ordered)
    weights = _weights_for(policy_name, n)
    total = sum(weights)
    class_set_hash = candidate_set_hash(ordered, weights, policy_name)
    replay_hashes = {e["class_key"]: candidate_replay_hash(e) for e in ordered}

    try:
        rng = ScopedRNG(root_seed, STREAM, scope)
        # Classify eagerly inside the guard: an unlawful root is refused here,
        # BEFORE any draw and BEFORE any selection identity is published.
        rng.classification
    except RngAuthorityError as exc:
        return typed(
            S.NOT_EXECUTED_AUTHORITY_HOLD,
            reason="root seed metadata unlawful; no draw consumed",
            rng_failure_code=exc.code,
            rng_failure_detail=exc.detail,
            n_draws=0,
            unreported_redraws=0,
            status_is_HOLD_not_INFEASIBLE=True,
        )

    ledger: Dict[str, Any] = {
        "decision_kind": DECISION_KIND,
        "decision_semantics_version": DECISION_SEMANTICS_VERSION,
        "stream": STREAM,
        "scope_hash": scope,
        "root_seed": root_seed,
        "root_seed_provenance": rng.classification["root_seed_provenance"],
        "adp020_entitlement": rng.classification["adp020_entitlement"],
        "adp020_hold": rng.classification.get("hold"),
        "sampler": (rng.draws[0].sampler if rng.draws else None),
        "policy_name": policy_name,
        "policy_hash": policy_hash(policy_name),
        "policy_status": POLICIES[policy_name]["status"],
        "no_population_frequency_claim": True,
        "candidate_set_hash": class_set_hash,
        "candidate_set_hash_binds_payload": True,
        "candidate_replay_hashes": replay_hashes,
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
