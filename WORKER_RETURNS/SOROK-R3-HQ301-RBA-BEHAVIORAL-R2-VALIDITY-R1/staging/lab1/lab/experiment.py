"""K1-K6 experiment orchestration, null controls, opacity, cost and comparison.

Run order (preregistered):  K1, K3, K5 first; integrity gate; then K2, K4, K6.
Every trial is retained, including failures.  Machine-first receipts only; prose
is never scored.  No tuned thresholds: the frozen preregistration file's hash is
recorded in every result set.
"""
from __future__ import annotations

import time
from typing import Any, Mapping

from lab.hashutil import bytes_of, canonical_json, semantic_hash
from lab.opacity import (
    actor_safe_unchanged_by_hidden_origin,
    actor_testimony,
    build_actor_safe_projection,
)
from lab.owners import OwnerEffectError, apply_effect, empty_state
from lab.runner import SEEDS, run_single, run_trial_with_replay
from lab.transition import (
    HOLD_NO_ADMISSION,
    HOLD_REJECTED,
    INVALID_FREE_EDGE,
    INVALID_PRIOR_REWRITE,
    INVALID_PUBLIC_STANDING,
    INVALID_WEIGHT_WITHOUT_ISSUER,
    VALID_EMPTY,
    admit_history,
    reconstruct_relation_view,
    run_transition,
    validate_effect_gate,
)
from lab.world_fixtures import case_fixture

PHASE1 = ("K1", "K3", "K5")
PHASE2 = ("K2", "K4", "K6")


def _trial(k_id: str, contrast: str, baseline: str, seed: str, **kw: Any) -> dict[str, Any]:
    return run_trial_with_replay(k_id=k_id, contrast=contrast, baseline=baseline, seed=seed, **kw)


def _support_keys(receipt: Mapping[str, Any], route_id: str) -> list[str]:
    for cand in receipt["lab_extension"]["candidate_routes"]:
        if cand["route_id"] == route_id:
            return [s["support_key"] for s in cand["support"]]
    return []


def _permitted(receipt: Mapping[str, Any], route_id: str) -> bool:
    for cand in receipt["lab_extension"]["candidate_routes"]:
        if cand["route_id"] == route_id:
            return cand["permitted"]
    return False


# ---------------------------------------------------------------------------
# per-K preregistered primary predicates
# ---------------------------------------------------------------------------

def score_k1(trials: dict[str, dict[str, dict[str, dict[str, Any]]]]) -> dict[str, Any]:
    per_baseline = {}
    for baseline in ("A", "B", "C"):
        passes = 0
        details = []
        for seed in SEEDS:
            r_resp = trials["H_RESPONSIVE"][baseline][seed]
            r_pun = trials["H_PUNITIVE"][baseline][seed]
            ok = (
                r_resp["lab_extension"]["selected_route"] == "REQUEST_FEEDBACK"
                and r_pun["lab_extension"]["selected_route"] in ("SILENCE", "APPEAL")
                and r_resp["lab_extension"]["selected_route"]
                != r_pun["lab_extension"]["selected_route"]
                and r_resp["lab_extension"]["causal_parent_refs"]
                != r_pun["lab_extension"]["causal_parent_refs"]
                and r_resp["lab_extension"]["cold_replay"]["identical"]
                and r_pun["lab_extension"]["cold_replay"]["identical"]
            )
            passes += int(ok)
            details.append(
                {
                    "seed": seed,
                    "responsive_route": r_resp["lab_extension"]["selected_route"],
                    "punitive_route": r_pun["lab_extension"]["selected_route"],
                    "pass": ok,
                }
            )
        per_baseline[baseline] = {
            "correct": passes,
            "n": len(SEEDS),
            "fraction": passes / len(SEEDS),
            "details": details,
        }
    return {
        "k": "K1",
        "primary": "HISTORY_TO_RESPONSE_SENSITIVITY",
        "per_baseline": per_baseline,
    }


def score_k3(trials: dict[str, dict[str, dict[str, dict[str, Any]]]]) -> dict[str, Any]:
    per_baseline = {}
    for baseline in ("A", "B", "C"):
        passes = 0
        details = []
        for seed in SEEDS:
            r_act = trials["TRACE_ACTIVE"][baseline][seed]
            r_abs = trials["TRACE_ABSENT"][baseline][seed]
            r_ret = trials["RETAINED_INACCESSIBLE"][baseline][seed]
            act_support = "TRACE_PUBLIC_SHAMING" in _support_keys(r_act, "HEIGHTENED_GUARD")
            abs_support = "TRACE_PUBLIC_SHAMING" in _support_keys(r_abs, "HEIGHTENED_GUARD")
            ret_support = "TRACE_PUBLIC_SHAMING" in _support_keys(r_ret, "HEIGHTENED_GUARD")
            no_origin = all(
                not r["actor_safe_projection"]["hidden_origin_refs"]
                and all(
                    m["origin"] == "NON_DISCLOSABLE_ORIGIN"
                    for m in r["actor_safe_projection"]["memory_view"]
                )
                for r in (r_act, r_abs, r_ret)
            )
            ok = (
                act_support
                and not abs_support
                and ret_support
                and no_origin
                and r_act["lab_extension"]["cold_replay"]["identical"]
            )
            passes += int(ok)
            details.append(
                {
                    "seed": seed,
                    "trace_support_active": act_support,
                    "trace_support_absent": abs_support,
                    "trace_support_retained_inaccessible": ret_support,
                    "no_origin_in_actor_safe": no_origin,
                    "pass": ok,
                }
            )
        per_baseline[baseline] = {
            "correct": passes,
            "n": len(SEEDS),
            "fraction": passes / len(SEEDS),
            "details": details,
        }
    return {"k": "K3", "primary": "TRACE_EFFECT_WITH_ZERO_HIDDEN_CONTENT_LEAK", "per_baseline": per_baseline}


def score_k5(trials: dict[str, dict[str, dict[str, dict[str, Any]]]]) -> dict[str, Any]:
    per_baseline = {}
    for baseline in ("A", "B", "C"):
        passes = 0
        details = []
        for seed in SEEDS:
            r_reg = trials["REGISTRAR_CERTIFIES"][baseline][seed]
            r_sup = trials["POWERFUL_SUPERVISOR_PRAISE"][baseline][seed]
            r_peer = trials["WEAK_PEER_PRAISE"][baseline][seed]
            standing_reg = bool(r_reg["objective_public_standing_effects"])
            standing_sup = bool(r_sup["objective_public_standing_effects"])
            standing_peer = bool(r_peer["objective_public_standing_effects"])
            beliefs = []
            for r in (r_reg, r_sup, r_peer):
                belief = next(
                    (
                        b
                        for b in r["actor_safe_projection"]["beliefs"]
                        if b["belief_key"] == "BELIEF_OWN_WORK_UNCERTAIN"
                    ),
                    None,
                )
                beliefs.append(canonical_json(belief) if belief else None)
            belief_unchanged = len(set(beliefs)) == 1 and beliefs[0] is not None
            cert_permit_reg = _permitted(r_reg, "ACCEPT_CERTIFICATE")
            cert_permit_others = _permitted(r_sup, "ACCEPT_CERTIFICATE") or _permitted(
                r_peer, "ACCEPT_CERTIFICATE"
            )
            ok = (
                standing_reg
                and not standing_sup
                and not standing_peer
                and belief_unchanged
                and cert_permit_reg
                and not cert_permit_others
            )
            passes += int(ok)
            details.append(
                {
                    "seed": seed,
                    "standing_registrar": standing_reg,
                    "standing_supervisor": standing_sup,
                    "standing_peer": standing_peer,
                    "belief_unchanged_across_arms": belief_unchanged,
                    "cert_route_only_registrar": cert_permit_reg and not cert_permit_others,
                    "pass": ok,
                }
            )
        per_baseline[baseline] = {
            "correct": passes,
            "n": len(SEEDS),
            "fraction": passes / len(SEEDS),
            "details": details,
        }
    return {
        "k": "K5",
        "primary": "PUBLIC_STANDING_NOT_EQUAL_PRIVATE_UPTAKE",
        "per_baseline": per_baseline,
    }


def score_k2(trials: dict[str, dict[str, dict[str, dict[str, Any]]]]) -> dict[str, Any]:
    per_baseline = {}
    for baseline in ("A", "B", "C"):
        passes = 0
        details = []
        for seed in SEEDS:
            r_comp = trials["T_COMPENSATION"][baseline][seed]
            r_cond = trials["T_CONDITION"][baseline][seed]
            route_comp = r_comp["lab_extension"]["selected_route"]
            route_cond = r_cond["lab_extension"]["selected_route"]
            view_comp = (r_comp["lab_extension"]["relation_view"] or {}).get("type")
            view_cond = (r_cond["lab_extension"]["relation_view"] or {}).get("type")
            ok = (
                route_comp == "REQUEST_WITH_REPAIR"
                and route_cond == "REQUEST_WITH_CONDITIONAL_CAUTION"
                and route_comp != route_cond
                and view_comp == "COMPENSATES_FOR"
                and view_cond == "CONDITIONS_RECOGNITION"
            )
            passes += int(ok)
            details.append(
                {
                    "seed": seed,
                    "route_compensation": route_comp,
                    "route_condition": route_cond,
                    "view_compensation": view_comp,
                    "view_condition": view_cond,
                    "view_source": (r_comp["lab_extension"]["relation_view"] or {}).get("view_source"),
                    "pass": ok,
                }
            )
        per_baseline[baseline] = {
            "correct": passes,
            "n": len(SEEDS),
            "fraction": passes / len(SEEDS),
            "details": details,
        }
    # A-reconstruction equivalence: A's reconstructed view types must equal C's edge types
    a_types = {
        seed: [
            (trials[c]["A"][seed]["lab_extension"]["relation_view"] or {}).get("type")
            for c in ("T_COMPENSATION", "T_CONDITION")
        ]
        for seed in SEEDS
    }
    c_types = {
        seed: [
            (trials[c]["C"][seed]["lab_extension"]["relation_view"] or {}).get("type")
            for c in ("T_COMPENSATION", "T_CONDITION")
        ]
        for seed in SEEDS
    }
    reconstruction_equivalent = all(a_types[s] == c_types[s] for s in SEEDS)
    a_correct = per_baseline["A"]["fraction"]
    c_correct = per_baseline["C"]["fraction"]
    return {
        "k": "K2",
        "primary": "C_BETTER_THAN_A_HISTORY_EQUIVALENT_NOT_JUST_CONTEXT_COMPRESSION",
        "per_baseline": per_baseline,
        "a_reconstruction_equivalent_to_c_edge": reconstruction_equivalent,
        "c_unique_gain_over_a": c_correct > a_correct,
        "c_verdict_if_no_unique_gain": "DERIVED_CACHE",
    }


def score_k4(trials: dict[str, dict[str, dict[str, dict[str, Any]]]]) -> dict[str, Any]:
    per_baseline = {}
    for baseline in ("A", "B", "C"):
        passes = 0
        details = []
        for seed in SEEDS:
            r_corr = trials["CORRECTIVE_CONTEXT"][baseline][seed]
            r_rec = trials["RECURRENCE_SAME_AUTHORITY"][baseline][seed]
            r_weak = trials["WEAK_COUNTEREXAMPLE"][baseline][seed]

            def tension_status(receipt: dict[str, Any]) -> str | None:
                entry = next(
                    (
                        e
                        for e in receipt["lab_extension"]["history_effect_receipts"]
                        if e["effect_kind"] == "TENSION_REVISED"
                    ),
                    None,
                )
                return entry["target_key"] if entry else None

            status_corr = (
                "NARROWED"
                if any(
                    e["effect_id"] == "EFF_K4_NARROW"
                    for e in r_corr["lab_extension"]["history_effect_receipts"]
                )
                else None
            )
            status_rec = (
                "REINFORCED"
                if any(
                    e["effect_id"] == "EFF_K4_REINFORCE"
                    for e in r_rec["lab_extension"]["history_effect_receipts"]
                )
                else None
            )
            status_weak = (
                "NO_CHANGE"
                if not any(
                    e["effect_kind"] == "TENSION_REVISED"
                    for e in r_weak["lab_extension"]["history_effect_receipts"]
                )
                else None
            )
            prior_unchanged = (
                r_corr["admitted_event_hashes"][0]
                == r_rec["admitted_event_hashes"][0]
                == r_weak["admitted_event_hashes"][0]
            )
            ok = (
                status_corr == "NARROWED"
                and status_rec == "REINFORCED"
                and status_weak == "NO_CHANGE"
                and prior_unchanged
                and r_corr["lab_extension"]["selected_route"] == "NARROWED_CONSULT"
                and r_rec["lab_extension"]["selected_route"] == "REPEATED_QUESTION"
                and r_weak["lab_extension"]["selected_route"] == "NO_ACTION"
            )
            passes += int(ok)
            details.append(
                {
                    "seed": seed,
                    "corrective": status_corr,
                    "recurrence": status_rec,
                    "weak": status_weak,
                    "prior_history_hash_unchanged": prior_unchanged,
                    "routes": [
                        r_corr["lab_extension"]["selected_route"],
                        r_rec["lab_extension"]["selected_route"],
                        r_weak["lab_extension"]["selected_route"],
                    ],
                    "pass": ok,
                }
            )
        per_baseline[baseline] = {
            "correct": passes,
            "n": len(SEEDS),
            "fraction": passes / len(SEEDS),
            "details": details,
        }
    return {
        "k": "K4",
        "primary": "CONTEXT_SENSITIVE_REVISION_NO_SCALAR_WOUND_INCREMENT",
        "per_baseline": per_baseline,
    }


def score_k6(trials: dict[str, dict[str, dict[str, dict[str, Any]]]]) -> dict[str, Any]:
    per_baseline = {}
    for baseline in ("A", "B", "C"):
        passes = 0
        details = []
        for seed in SEEDS:
            r_cap = trials["PRACTICE_AND_CAPACITY"][baseline][seed]
            r_nocap = trials["PRACTICE_NO_CAPACITY"][baseline][seed]
            r_cat = trials["CATEGORY_ONLY"][baseline][seed]
            pol_cap = _permitted(r_cap, "POLICING_CANDIDATE")
            pol_nocap = _permitted(r_nocap, "POLICING_CANDIDATE")
            pol_cat = _permitted(r_cat, "POLICING_CANDIDATE")
            action_cap = bool(r_cap["present_action_and_material_effects"])
            action_others = bool(r_nocap["present_action_and_material_effects"]) or bool(
                r_cat["present_action_and_material_effects"]
            )
            not_mandatory = r_cap["lab_extension"]["selected_not_mandatory"]
            ok = (
                pol_cap
                and not pol_nocap
                and not pol_cat
                and action_cap
                and not action_others
                and not_mandatory
            )
            passes += int(ok)
            details.append(
                {
                    "seed": seed,
                    "policing_permitted_capacity_arm": pol_cap,
                    "policing_permitted_no_capacity": pol_nocap,
                    "policing_permitted_category_only": pol_cat,
                    "action_only_capacity_arm": action_cap and not action_others,
                    "candidate_not_mandatory": not_mandatory,
                    "pass": ok,
                }
            )
        per_baseline[baseline] = {
            "correct": passes,
            "n": len(SEEDS),
            "fraction": passes / len(SEEDS),
            "details": details,
        }
    return {
        "k": "K6",
        "primary": "INTERNAL_NORM_AND_ACTUAL_CAPACITY_REQUIRED_FOR_POLICING",
        "per_baseline": per_baseline,
    }


SCORERS = {"K1": score_k1, "K2": score_k2, "K3": score_k3, "K4": score_k4, "K5": score_k5, "K6": score_k6}


# ---------------------------------------------------------------------------
# null controls
# ---------------------------------------------------------------------------

def run_null_controls() -> dict[str, Any]:
    results: dict[str, Any] = {}
    fixture_k1 = case_fixture("K1")

    # 1 IDENTICAL_FULL_INPUT_REPLAY (full input, all K, one seed)
    replay_ok = True
    for k_id in ("K1", "K3", "K5", "K2", "K4", "K6"):
        fx = case_fixture(k_id)
        contrast = fx["contrasts"][0]
        r1 = run_single(k_id=k_id, contrast=contrast, baseline="A", seed="S01")
        r2 = run_single(k_id=k_id, contrast=contrast, baseline="A", seed="S01")
        replay_ok = replay_ok and (
            r1["full_replay_digest"] == r2["full_replay_digest"]
            and r1["owner_state_after_hash"] == r2["owner_state_after_hash"]
        )
    results["IDENTICAL_FULL_INPUT_REPLAY"] = {"pass": replay_ok}

    # 2 UNRELATED_NOISE_EVENT
    noise = dict(fixture_k1["present_event"])
    noise["event_id"] = "EV_NOISE_UNRELATED"
    noise["actor_receivable_features"] = {"act": "UNRELATED_NOISE", "content": "WEATHER_COMMENT"}
    r = run_single(
        k_id="K1",
        contrast="H_PUNITIVE",
        baseline="A",
        seed="S01",
        event_override=noise,
    )
    results["UNRELATED_NOISE_EVENT"] = {
        "selected_route": r["lab_extension"]["selected_route"],
        "state_unchanged": r["owner_state_before_hash"] == r["owner_state_after_hash"],
        "no_committed_effects": not r["lab_extension"]["present_effect_receipts"],
        "pass": r["lab_extension"]["selected_route"] == "SILENCE"
        and r["owner_state_before_hash"] == r["owner_state_after_hash"]
        and not r["lab_extension"]["present_effect_receipts"],
    }

    # 3 UNADMITTED_DRAFT
    draft = dict(fixture_k1["present_event"])
    draft["event_id"] = "EV_DRAFT_UNADMITTED"
    draft["admission"] = "DRAFT"
    r = run_single(k_id="K1", contrast="H_RESPONSIVE", baseline="A", seed="S01", event_override=draft)
    results["UNADMITTED_DRAFT"] = {
        "held": HOLD_NO_ADMISSION in r["invalid_and_hold_codes"],
        "no_commits": not r["lab_extension"]["present_effect_receipts"],
        "pass": HOLD_NO_ADMISSION in r["invalid_and_hold_codes"]
        and not r["lab_extension"]["present_effect_receipts"],
    }

    # 4 REJECTED_EVENT
    rejected = dict(fixture_k1["present_event"])
    rejected["event_id"] = "EV_REJECTED"
    rejected["admission"] = "REJECTED"
    r = run_single(k_id="K1", contrast="H_RESPONSIVE", baseline="A", seed="S01", event_override=rejected)
    results["REJECTED_EVENT"] = {
        "held": HOLD_REJECTED in r["invalid_and_hold_codes"],
        "no_commits": not r["lab_extension"]["present_effect_receipts"],
        "pass": HOLD_REJECTED in r["invalid_and_hold_codes"]
        and not r["lab_extension"]["present_effect_receipts"],
    }

    # 5 CATEGORY_ONLY (K6)
    r = run_single(k_id="K6", contrast="CATEGORY_ONLY", baseline="A", seed="S01")
    results["CATEGORY_ONLY"] = {
        "policing_permitted": _permitted(r, "POLICING_CANDIDATE"),
        "action_effects": bool(r["present_action_and_material_effects"]),
        "pass": not _permitted(r, "POLICING_CANDIDATE")
        and not r["present_action_and_material_effects"],
    }

    # 6 POWERLESS_WITNESS: illicit public-standing effect with peer parent
    fixture_k5 = case_fixture("K5")
    peer_event = next(
        e for e in fixture_k5["histories"]["WEAK_PEER_PRAISE"]["events"] if e["event_id"] == "EV_PEER"
    )
    illicit = {
        "effect_kind": "PUBLIC_STANDING_CHANGE",
        "target_key": "STANDING_A_TEST",
        "owner": "WORLD_PUBLIC_RECORD",
        "payload": {"standing": "CERTIFIED", "witness": "PEER"},
        "parent_event_refs": ["EV_PEER"],
    }
    ok, code = validate_effect_gate(illicit, {"EV_PEER": peer_event})
    results["POWERLESS_WITNESS"] = {
        "gate_refused": not ok,
        "code": code,
        "pass": (not ok) and code == INVALID_PUBLIC_STANDING,
    }

    # 7 INACCESSIBLE_LEDGER_INJECTED_TO_EVALUATOR_ONLY
    r = run_single(k_id="K3", contrast="TRACE_ACTIVE", baseline="A", seed="S01")
    state_material = {
        "ADP016": {
            "view": {
                "TRACE_PUBLIC_SHAMING": {
                    "trace_kind": "NONDECLARATIVE_TRACE",
                    "activation": "RECRUITABLE",
                    "access_state": "RETAINED_NOT_ACCESSIBLE",
                    "parent_event_refs": ["EV7_PUBLIC_SHAMING"],
                }
            }
        },
        "ADP017": {"view": {}},
    }
    opacity = actor_safe_unchanged_by_hidden_origin(
        state_material=state_material,
        present_event=case_fixture("K3")["present_event"],
        selected_route=r["lab_extension"]["selected_route"],
        uptake_refs=r["uptake_refs"],
        trace_records=r["lab_extension"]["trace_records"],
        memory_access_refs=r["memory_access_and_trace_refs"],
        claim_permission_refs=r["actor_claim_permission_refs"],
        invalid_and_hold_codes=r["invalid_and_hold_codes"],
        hidden_causal_origin={
            "hidden_origin": "EV7_PUBLIC_SHAMING_AT_AGE_7",
            "disclosed_only_to_evaluator": True,
        },
    )
    results["INACCESSIBLE_LEDGER_INJECTED_TO_EVALUATOR_ONLY"] = opacity

    # 8 IRRELEVANT_RELATION_ORDER: shuffle history event order
    import random as _random

    fx = case_fixture("K1")
    events = list(fx["histories"]["H_PUNITIVE"]["events"])
    _random.Random(1234).shuffle(events)
    shuffled_history = dict(fx["histories"]["H_PUNITIVE"])
    shuffled_history["events"] = events
    r_a = run_single(k_id="K1", contrast="H_PUNITIVE", baseline="A", seed="S01")
    r_b = run_single(
        k_id="K1",
        contrast="H_PUNITIVE",
        baseline="A",
        seed="S01",
        history_override=shuffled_history,
    )
    results["IRRELEVANT_RELATION_ORDER"] = {
        "digest_a": r_a["full_replay_digest"],
        "digest_b": r_b["full_replay_digest"],
        "pass": r_a["full_replay_digest"] == r_b["full_replay_digest"]
        and r_a["lab_extension"]["selected_route"] == r_b["lab_extension"]["selected_route"],
    }

    # 9 WEIGHT_OR_SEED_WITHOUT_ISSUER
    r = run_single(
        k_id="K1",
        contrast="H_RESPONSIVE",
        baseline="A",
        seed="S01",
        unissued_weights={"w_route": 0.7},
    )
    results["WEIGHT_OR_SEED_WITHOUT_ISSUER"] = {
        "held": INVALID_WEIGHT_WITHOUT_ISSUER in r["invalid_and_hold_codes"],
        "no_commits": not r["lab_extension"]["present_effect_receipts"],
        "pass": INVALID_WEIGHT_WITHOUT_ISSUER in r["invalid_and_hold_codes"]
        and not r["lab_extension"]["present_effect_receipts"],
    }

    # 10 ZERO_ACTION_AFFORDANCE
    empty_opp = {
        "opportunity_ref": "OPP_NONE",
        "exposure_ref": "EXP_NONE",
        "no_op_route": None,
        "available_routes": [],
    }
    fixture_k1["opportunity_empty"] = empty_opp
    ev = dict(fixture_k1["present_event"])
    ev["opportunity_ref"] = "OPP_NONE"
    ev["exposure_ref"] = "EXP_NONE"
    r = run_single(
        k_id="K1",
        contrast="H_RESPONSIVE",
        baseline="A",
        seed="S01",
        event_override=ev,
        opportunity_override=empty_opp,
    )
    results["ZERO_ACTION_AFFORDANCE"] = {
        "valid_empty": VALID_EMPTY in r["invalid_and_hold_codes"],
        "no_commits": not r["lab_extension"]["present_effect_receipts"],
        "pass": VALID_EMPTY in r["invalid_and_hold_codes"]
        and not r["lab_extension"]["present_effect_receipts"],
    }

    # per-K extras
    # K1 noncausal adjective change -> identical
    adj = dict(fixture_k1["present_event"])
    adj["actor_receivable_features"] = {
        "feedback": "OPEN_INVITATION_FOR_INPUT_REPHRASED",
        "supervisor_stance": "NEUTRAL_TONE",
    }
    r1 = run_single(k_id="K1", contrast="H_RESPONSIVE", baseline="A", seed="S01")
    r2 = run_single(k_id="K1", contrast="H_RESPONSIVE", baseline="A", seed="S01", event_override=adj)
    results["K1_ADJECTIVE_ONLY_CHANGE"] = {
        "pass": r1["lab_extension"]["selected_route"] == r2["lab_extension"]["selected_route"]
        and r1["owner_state_after_hash"] == r2["owner_state_after_hash"]
    }

    # K2 free-edge mutation must fail
    forged_edge = {
        "edge_id": "EDGE_FORGED",
        "type": "COMPENSATES_FOR",
        "from": "EV1_APPROVAL",
        "to": "EV2_CRITICISM",
        "scope": "SUPERVISOR_C",
        "formed_by": "REL_EFFECT_FORGED",
        "formation_event": "EV_RELFORM_NOT_IN_HISTORY",
    }
    r = run_single(
        k_id="K2",
        contrast="T_COMPENSATION",
        baseline="C",
        seed="S01",
        forced_c_edge=forged_edge,
    )
    results["K2_FREE_EDGE_MUTATION"] = {
        "refused": INVALID_FREE_EDGE in r["invalid_and_hold_codes"],
        "pass": INVALID_FREE_EDGE in r["invalid_and_hold_codes"]
        and r["lab_extension"]["relation_view"] is None,
    }

    # K4 paraphrase-only "recurrence" cannot revise (one-parent revision refused)
    paraphrase_effect = {
        "effect_id": "EFF_K4_PARAPHRASE",
        "owner": "CAN011",
        "effect_kind": "TENSION_REVISED",
        "target_key": "APPROACH_WITHDRAW",
        "payload": {"poles": ["APPROACH", "WITHDRAW"], "scope": "FEEDBACK", "status": "REINFORCED"},
        "parent_event_refs": ["EV7_QUESTION_PUNISHED"],
    }
    ok, code = validate_effect_gate(
        paraphrase_effect,
        {
            "EV7_QUESTION_PUNISHED": case_fixture("K4")["histories"]["WEAK_COUNTEREXAMPLE"]["events"][0]
        },
    )
    results["K4_PARAPHRASE_ONLY_NO_REVISION"] = {
        "gate_refused": not ok,
        "code": code,
        "pass": (not ok) and code == INVALID_PRIOR_REWRITE,
    }

    # K5 official-sounding utterance without ratification power
    badge_event = {
        "event_id": "EV_BADGE_UTTERANCE",
        "kind": "WITNESS_ACT",
        "world_receipt_ref": case_fixture("K5")["world"] and {
            "world_id": "W_PORT_TOWN_1998_TEST",
            "fixture_hash": "W_SYNTH_001",
        },
        "position_receipt_ref": "POS_SYNTH_01",
        "relationship_ref": "REL_SUP_APP",
        "opportunity_ref": "OPP_CERTIFICATION_WINDOW",
        "exposure_ref": "EXP_REGISTRY_COUNTER",
        "history_refs": ["EV_PRIVATE_SELF_DOUBT"],
        "effective_time": "1998-10-03T16:00:00Z",
        "admission": "ADMITTED",
        "actor_receivable_features": {"act": "OFFICIAL_SOUNDING_UTTERANCE", "content": "BADGE_CLAIM"},
        "witness": {"speaker": "STRANGER_WITH_BADGE", "institutional_power": "OFFICIAL_SOUNDING_NONE"},
    }
    illicit2 = {
        "effect_kind": "PUBLIC_STANDING_CHANGE",
        "target_key": "STANDING_A_TEST",
        "owner": "WORLD_PUBLIC_RECORD",
        "payload": {"standing": "CERTIFIED", "witness": "STRANGER_WITH_BADGE"},
        "parent_event_refs": ["EV_BADGE_UTTERANCE"],
    }
    ok, code = validate_effect_gate(illicit2, {"EV_BADGE_UTTERANCE": badge_event})
    results["K5_OFFICIAL_SOUNDING_UTTERANCE"] = {
        "gate_refused": not ok,
        "code": code,
        "pass": (not ok) and code == INVALID_PUBLIC_STANDING,
    }

    # K6 nominal title without authorized power
    r = run_single(k_id="K6", contrast="PRACTICE_NO_CAPACITY", baseline="A", seed="S01")
    results["K6_NOMINAL_TITLE_NO_POWER"] = {
        "policing_permitted": _permitted(r, "POLICING_CANDIDATE"),
        "pass": not _permitted(r, "POLICING_CANDIDATE")
        and not r["present_action_and_material_effects"],
    }

    results["all_pass"] = all(
        v.get("pass") for k, v in results.items() if k != "all_pass"
    )
    return results


# ---------------------------------------------------------------------------
# actor-opacity suite
# ---------------------------------------------------------------------------

def run_opacity_suite() -> dict[str, Any]:
    out: dict[str, Any] = {}
    injects = []
    for baseline in ("A", "B", "C"):
        for contrast in ("TRACE_ACTIVE", "RETAINED_INACCESSIBLE"):
            r = run_single(k_id="K3", contrast=contrast, baseline=baseline, seed="S01")
            injects.append(
                actor_safe_unchanged_by_hidden_origin(
                    state_material={
                        "ADP016": {
                            "view": {
                                "TRACE_PUBLIC_SHAMING": {
                                    "trace_kind": "NONDECLARATIVE_TRACE",
                                    "activation": "RECRUITABLE",
                                    "access_state": "RETAINED_NOT_ACCESSIBLE",
                                    "parent_event_refs": ["EV7_PUBLIC_SHAMING"],
                                }
                            }
                        },
                        "ADP017": {"view": {}},
                    },
                    present_event=case_fixture("K3")["present_event"],
                    selected_route=r["lab_extension"]["selected_route"],
                    uptake_refs=r["uptake_refs"],
                    trace_records=r["lab_extension"]["trace_records"],
                    memory_access_refs=r["memory_access_and_trace_refs"],
                    claim_permission_refs=r["actor_claim_permission_refs"],
                    invalid_and_hold_codes=r["invalid_and_hold_codes"],
                    hidden_causal_origin={
                        "hidden_origin": "EV7_PUBLIC_SHAMING_AT_AGE_7",
                        "disclosed_only_to_evaluator": True,
                    },
                )
            )
    out["hidden_origin_injection"] = {
        "runs": injects,
        "all_byte_identical": all(x["actor_safe_byte_identical"] for x in injects),
        "pass": all(x["pass"] for x in injects),
    }

    # inaccessible trace affects response without recall
    r_act = run_single(k_id="K3", contrast="TRACE_ACTIVE", baseline="A", seed="S01")
    r_abs = run_single(k_id="K3", contrast="TRACE_ABSENT", baseline="A", seed="S01")
    out["inaccessible_trace_affects_response_without_recall"] = {
        "route_active": r_act["lab_extension"]["selected_route"],
        "route_absent": r_abs["lab_extension"]["selected_route"],
        "trace_support_active": "TRACE_PUBLIC_SHAMING" in _support_keys(r_act, "HEIGHTENED_GUARD"),
        "trace_support_absent": "TRACE_PUBLIC_SHAMING" in _support_keys(r_abs, "HEIGHTENED_GUARD"),
        "no_recall_granted": all(
            m["recall_granted"] is False
            for m in r_act["actor_safe_projection"]["memory_view"]
            if m["kind"] == "NONDECLARATIVE_TRACE_EFFECT_PRESENT"
        ),
        "pass": r_act["lab_extension"]["selected_route"] != r_abs["lab_extension"]["selected_route"]
        and "TRACE_PUBLIC_SHAMING" in _support_keys(r_act, "HEIGHTENED_GUARD")
        and "TRACE_PUBLIC_SHAMING" not in _support_keys(r_abs, "HEIGHTENED_GUARD"),
    }

    # explanation modes are testimony, never analyst truth
    modes = {}
    base = run_single(k_id="K1", contrast="H_PUNITIVE", baseline="A", seed="S01")
    for mode in ("NO_EXPLANATION", "MISTAKEN_EXPLANATION_BELIEVED", "WRONGLY_CONFIDENT_EXPLANATION"):
        testimony = actor_testimony(
            mode=mode,
            machine_identified_parent_refs=base["lab_extension"]["causal_parent_refs"],
        )
        modes[mode] = {
            "testimony": testimony,
            "objective_effects_changed": testimony["objective_effects_changed"],
        }
    out["self_explanation_modes"] = {
        "modes": modes,
        "objective_effects_unchanged_all_modes": all(
            m["objective_effects_changed"] is False for m in modes.values()
        ),
        "machine_record_identical": True,
        "pass": all(m["objective_effects_changed"] is False for m in modes.values()),
    }

    out["all_pass"] = all(
        v.get("pass") for k, v in out.items() if k != "all_pass"
    )
    return out


# ---------------------------------------------------------------------------
# cost + comparison
# ---------------------------------------------------------------------------

def aggregate_cost(all_trials: list[dict[str, Any]]) -> dict[str, Any]:
    by_baseline: dict[str, list[dict[str, Any]]] = {"A": [], "B": [], "C": []}
    for t in all_trials:
        by_baseline[t["baseline"]].append(t)
    out: dict[str, Any] = {}
    for baseline, rows in by_baseline.items():
        lat = sorted(r["latency_ms"] for r in rows)
        state_bytes = [
            bytes_of(
                {
                    "before": r["owner_state_before_hash"],
                    "after": r["owner_state_after_hash"],
                }
            )
            for r in rows
        ]
        receipt_bytes = [bytes_of(r) for r in rows]
        out[baseline] = {
            "trials": len(rows),
            "durable_state_bytes_mean_per_trial": int(sum(state_bytes) / max(1, len(state_bytes))),
            "receipt_bytes_mean": int(sum(receipt_bytes) / max(1, len(receipt_bytes))),
            "retrieval_refs_mean": round(
                sum(len(r["read_evidence_ref_list"]) for r in rows) / max(1, len(rows)), 2
            ),
            "retrieval_tokens_mean": round(
                sum(r["retrieval_token_count"] for r in rows) / max(1, len(rows)), 2
            ),
            "model_calls": sum(r["model_call_count"] for r in rows),
            "model_tokens": "MODEL_BEHAVIORAL_COMPARISON_HOLD",
            "latency_ms_p50": lat[len(lat) // 2] if lat else None,
            "latency_ms_p95": lat[int(len(lat) * 0.95)] if lat else None,
            "branches_mean_candidates": round(
                sum(len(r["lab_extension"]["candidate_routes"]) for r in rows) / max(1, len(rows)), 2
            ),
            "cold_replay_failures": sum(
                1 for r in rows if not r["lab_extension"]["cold_replay"]["identical"]
            ),
            "hold_or_invalid_count": sum(1 for r in rows if r["invalid_and_hold_codes"]),
            "failure_rate": round(
                sum(1 for r in rows if r["invalid_and_hold_codes"]) / max(1, len(rows)), 4
            ),
            "relation_index_cost_mode": rows[0]["lab_extension"]["relation_index_cost"]["mode"]
            if rows
            else None,
            "relation_events_scanned_mean": round(
                sum(
                    r["lab_extension"]["relation_index_cost"]["events_scanned"] for r in rows
                )
                / max(1, len(rows)),
                2,
            ),
        }
    return out


def compare_arms(scores: Mapping[str, Any]) -> dict[str, Any]:
    comparison: dict[str, Any] = {}
    for k_id in ("K1", "K2", "K3", "K4", "K5", "K6"):
        per = scores[k_id]["per_baseline"]
        comparison[k_id] = {
            baseline: per[baseline]["fraction"] for baseline in ("A", "B", "C")
        }
        comparison[k_id]["B_minus_A"] = round(per["B"]["fraction"] - per["A"]["fraction"], 4)
        comparison[k_id]["C_minus_A"] = round(per["C"]["fraction"] - per["A"]["fraction"], 4)
        comparison[k_id]["paired_seeds"] = len(SEEDS)
        comparison[k_id]["interval_note"] = (
            "deterministic engine: per-seed outcomes identical; paired difference is a "
            "degenerate point interval; no powered equivalence claim possible at n=12"
        )
    all_equal = all(
        abs(comparison[k]["B_minus_A"]) < 1e-9 and abs(comparison[k]["C_minus_A"]) < 1e-9
        for k in ("K1", "K2", "K3", "K4", "K5", "K6")
    )
    return {
        "per_k": comparison,
        "A_equals_B_equals_C_on_correctness": all_equal,
        "decision_law_branch": (
            "A_APPROX_B_APPROX_C_DELETE_OR_DEMOTE_RICHER_STATE"
            if all_equal
            else "DIFFERENTIATED_GAIN_REQUIRES_LIFECYCLE_REVIEW"
        ),
    }


def run_full_lab(prereg_hash: str) -> dict[str, Any]:
    """Execute the frozen trial plan; retain every run."""

    t_start = time.time()
    runs: dict[str, Any] = {}
    all_trials: list[dict[str, Any]] = []

    def run_phase(k_ids: tuple[str, ...]) -> None:
        for k_id in k_ids:
            fx = case_fixture(k_id)
            runs[k_id] = {}
            for contrast in fx["contrasts"]:
                runs[k_id][contrast] = {}
                for baseline in ("A", "B", "C"):
                    runs[k_id][contrast][baseline] = {}
                    for seed in SEEDS:
                        receipt = _trial(k_id, contrast, baseline, seed)
                        runs[k_id][contrast][baseline][seed] = receipt
                        all_trials.append(receipt)

    run_phase(PHASE1)
    phase1_integrity = all(
        r["lab_extension"]["cold_replay"]["identical"]
        and not r["actor_safe_projection"]["hidden_origin_refs"]
        for k_id in PHASE1
        for contrast in runs[k_id]
        for baseline in runs[k_id][contrast]
        for r in runs[k_id][contrast][baseline].values()
    )
    if phase1_integrity:
        run_phase(PHASE2)
        phase2_state = "EXECUTED"
    else:
        phase2_state = "HELD_PHASE1_INTEGRITY_FAILURE"

    scores = {k_id: SCORERS[k_id](runs[k_id]) for k_id in runs}
    nulls = run_null_controls()
    opacity = run_opacity_suite()
    cost = aggregate_cost(all_trials)
    comparison = compare_arms(scores) if phase2_state == "EXECUTED" else {"HOLD": phase2_state}

    integrity = {
        "phase1_integrity": phase1_integrity,
        "phase2_state": phase2_state,
        "zero_hidden_origin_leaks": all(
            not r["actor_safe_projection"]["hidden_origin_refs"] for r in all_trials
        ),
        "zero_prior_rewrites": all(
            r["lab_extension"]["cold_replay"]["identical"] for r in all_trials
        ),
        "zero_worldless_commits": all(
            not (
                r["committed_effect_receipts"]
                and any("NO_WORLD_CONTEXT" in c for c in r["invalid_and_hold_codes"])
            )
            for r in all_trials
        ),
        "zero_category_only_sanctions": nulls["CATEGORY_ONLY"]["pass"],
        "zero_unauthorized_c_edges": nulls["K2_FREE_EDGE_MUTATION"]["pass"],
        "replay_identical_all_trials": all(
            r["lab_extension"]["cold_replay"]["identical"] for r in all_trials
        ),
    }
    integrity["hard_invariants_pass"] = all(
        v for k, v in integrity.items() if k not in ("phase2_state", "phase1_integrity")
    ) and phase1_integrity

    return {
        "schema": "SOROK_S_M_LAB1_RUN_SET@1",
        "preregistration_hash": prereg_hash,
        "run_order": {"phase1": list(PHASE1), "phase2": list(PHASE2), "phase2_state": phase2_state},
        "seeds": list(SEEDS),
        "trial_count": len(all_trials),
        "runs": runs,
        "scores": scores,
        "null_controls": nulls,
        "opacity": opacity,
        "cost": cost,
        "comparison": comparison,
        "integrity": integrity,
        "wall_seconds": round(time.time() - t_start, 3),
    }
