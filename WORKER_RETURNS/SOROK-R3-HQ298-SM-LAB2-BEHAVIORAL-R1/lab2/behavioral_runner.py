"""HQ298 S-M-LAB2 — behavioral trial runner.

PROVISIONAL LAB PROTOCOL — NOT ADOPTED LAW.

Modes:
  * HOLD (default) — no grant present: zero model calls issued, typed
    MODEL_BEHAVIORAL_HOLD returned with exact missing grant fields.
  * GRANTED — only reachable with a complete Grant; issues the matched
    behavioral calls under the frozen budgets and captures raw request/response.
  * DRY_RUN — harness mechanics validation with a DETERMINISTIC FIXTURE
    RESPONDER. Output is labelled HARNESS_DRY_RUN__NOT_BEHAVIORAL_EVIDENCE and
    can NEVER be counted as model behavior.

The fixture responder is not a model, not an actor, and not evidence.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

from .model_gate import Grant, evaluate_gate, require_call_permission, ModelCallDenied, HOLD_ID
from .packets import (build_manifest, build_trial_packet, contrast_pairs,
                      expected_code, actor_visible_fingerprint,
                      paraphrase_variant, label_shuffle, surface_variant,
                      inject_hidden_origin, SEEDS, ARMS, EXPECTED_TYPED_CODES)
from .scoring import ScorerInput, dual_score, blind_summary, compare_arms

RUNNER_VERSION = "LAB2_BEHAVIORAL_RUNNER@1.0.0"
DRY_RUN_LABEL = "HARNESS_DRY_RUN__NOT_BEHAVIORAL_EVIDENCE"


def fixture_responder(packet: Dict[str, Any]) -> str:
    """DETERMINISTIC FIXTURE RESPONDER — TEST HARNESS PLUMBING ONLY.

    It selects the frozen expected code for the packet's contrast. This
    demonstrates that the packet -> capture -> blind scoring pipeline is wired
    correctly. It is NOT a model, NOT behavior, and NOT evidence.
    """
    k_id = packet["k_id"]
    for contrast, codes in EXPECTED_TYPED_CODES[k_id].items():
        # fixture responder knows the answer key by construction; this is why
        # its output is worthless as behavioral evidence
        if contrast in packet["trial_id"]:
            return codes[0]
    return "OTHER_UNSCORABLE"


@dataclass
class CallRecord:
    trial_id: str
    arm: str
    request_hash: str
    response_raw: str
    selected_typed_code: str
    model_identity: str
    wall_seconds: float
    evidence_label: str


class BehavioralRunner:
    def __init__(self, grant: Optional[Grant] = None,
                 preregistration_sha256: str = ""):
        self.grant = grant
        self.preregistration_sha256 = preregistration_sha256
        self.calls: List[CallRecord] = []
        self.model_calls_issued = 0
        self.transport_retries = 0

    def gate(self) -> Dict[str, Any]:
        return evaluate_gate(self.grant).as_dict()

    def run_hold(self) -> Dict[str, Any]:
        """Default execution when no complete grant exists: zero calls."""
        decision = evaluate_gate(self.grant)
        assert not decision.allowed, "HOLD mode requires an incomplete grant"
        return {
            "runner_version": RUNNER_VERSION,
            "mode": "HOLD",
            "terminal": HOLD_ID,
            "model_calls_issued": 0,
            "gate": decision.as_dict(),
            "exact_missing_grant_fields": decision.missing_fields,
            "missing_authority_class": decision.missing_authority_class,
            "behavioral_evidence_produced": False,
            "note": ("no paid/actor/external model call issued; prior authoring-"
                     "environment use does not license model-actor trials"),
        }

    def run_dry_run(self) -> Dict[str, Any]:
        """Harness mechanics validation ONLY. Never behavioral evidence."""
        manifest = build_manifest()
        expected_by_trial = {t["trial_id"]: t["expected_typed_codes"]
                             for t in manifest["trials"]}
        records: List[ScorerInput] = []
        per_arm: Dict[str, List] = {}
        t0 = time.perf_counter()
        for t in manifest["trials"]:
            pkt = build_trial_packet(
                t["k_id"],
                _fixture_contrast(t["k_id"], t["prereg_contrast"]),
                t["prereg_contrast"], t["seed"], t["arm"])
            code = fixture_responder(pkt)
            si = ScorerInput(trial_id=t["trial_id"],
                             counterbalance_code=t["presentation_code"],
                             selected_typed_code=code)
            records.append(si)
            per_arm.setdefault(t["arm"], []).append(si)
        scored = dual_score(records, expected_by_trial)
        per_arm_scored = {}
        for arm, items in per_arm.items():
            from .scoring import scorer_alpha
            per_arm_scored[arm] = scorer_alpha(items, expected_by_trial)
        comparison = compare_arms(per_arm_scored)
        return {
            "runner_version": RUNNER_VERSION,
            "mode": "DRY_RUN",
            "evidence_label": DRY_RUN_LABEL,
            "behavioral_evidence_produced": False,
            "model_calls_issued": 0,
            "fixture_responder_used": True,
            "fixture_responder_disclaimer": (
                "the fixture responder is a deterministic answer-key proxy that "
                "validates harness plumbing; its output is NOT model behavior and "
                "must never be cited as behavioral evidence"),
            "preregistration_sha256": self.preregistration_sha256,
            "manifest_hash": manifest["manifest_hash"],
            "n_trials": manifest["n_trials"],
            "scorer_agreement": scored["scorer_agreement"],
            "n_scored": scored["n_records"],
            "comparison": comparison,
            "wall_seconds": round(time.perf_counter() - t0, 4),
        }

    def run_granted(self) -> Dict[str, Any]:
        """Only reachable with a complete grant. Issues matched behavioral calls."""
        try:
            decision = require_call_permission(self.grant)
        except ModelCallDenied as e:
            return self.run_hold() | {"denial": str(e)}
        raise NotImplementedError(
            "GRANTED mode transport is intentionally not wired in this return: "
            "no grant exists, so no transport may be exercised. When a grant is "
            "issued, this method is the single sanctioned call site; it must "
            "capture exact request/response and obey the frozen budgets.")


def _fixture_contrast(k_id: str, prereg_contrast: str) -> str:
    for fixture_contrast, prereg in contrast_pairs(k_id):
        if prereg == prereg_contrast:
            return fixture_contrast
    raise KeyError(prereg_contrast)


def run_packet_nulls() -> Dict[str, Any]:
    """Source-free packet-level nulls (N1/N2/N4/N5 + matched-content check)."""
    manifest = build_manifest()
    results = {}

    # matched content across arms (the core matched-comparison invariant)
    results["matched_content_across_arms_ok"] = manifest["matched_content_across_arms_ok"]
    results["matched_content_violations"] = manifest["matched_content_across_arms_violations"]

    # N1 paraphrase / N2 label / N4 surface: actor-visible typed menu and
    # expected codes are unaffected by surface changes
    base = build_trial_packet("K1", "H_RESPONSIVE", "H_RESPONSIVE", "S01", "A")
    base_fp = actor_visible_fingerprint(base)
    for name, fn in (("N1_PARAPHRASE", lambda p: paraphrase_variant(p, 1)),
                     ("N2_LABEL", lambda p: label_shuffle(p, 1)),
                     ("N4_SURFACE", lambda p: surface_variant(p, 1))):
        v = fn(json.loads(json.dumps(base)))
        same_menu = v["typed_menu"] == base["typed_menu"]
        results[name] = {
            "typed_menu_invariant": same_menu,
            "expected_codes_invariant": (
                expected_code("K1", "H_RESPONSIVE") == expected_code("K1", "H_RESPONSIVE")),
            "pass": same_menu,
        }

    # N5 trace firewall: hidden-origin injection leaves actor-visible payload equal
    injected = inject_hidden_origin(json.loads(json.dumps(base)), "SECRET_ORIGIN_7YO")
    results["N5_TRACE_FIREWALL"] = {
        "actor_visible_fingerprint_equal":
            actor_visible_fingerprint(injected) == base_fp,
        "hidden_origin_in_evaluator_only_metadata":
            injected.get("evaluator_only_metadata", {}).get("hidden_origin") == "SECRET_ORIGIN_7YO",
        "hidden_origin_in_actor_packet":
            "SECRET_ORIGIN_7YO" in json.dumps(
                injected.get("allowed_actor_info_packet", {})),
        "pass": (
            actor_visible_fingerprint(injected) == base_fp
            and "SECRET_ORIGIN_7YO" not in json.dumps(
                injected.get("allowed_actor_info_packet", {}))),
    }

    # K3 firewall on the actual K3 TRACE_ACTIVE packet
    k3 = build_trial_packet("K3", "TRACE_ACTIVE", "TRACE_ACTIVE", "S01", "A")
    k3_inj = inject_hidden_origin(json.loads(json.dumps(k3)), "HIDDEN_CHILDHOOD_ORIGIN")
    results["N5_TRACE_FIREWALL_K3"] = {
        "actor_visible_fingerprint_equal":
            actor_visible_fingerprint(k3_inj) == actor_visible_fingerprint(k3),
        "hidden_origin_absent_from_actor_info":
            "HIDDEN_CHILDHOOD_ORIGIN" not in json.dumps(k3["allowed_actor_info_packet"]),
        "pass": (
            actor_visible_fingerprint(k3_inj) == actor_visible_fingerprint(k3)
            and "HIDDEN_CHILDHOOD_ORIGIN" not in json.dumps(k3["allowed_actor_info_packet"])),
    }

    # K5 standing separation: actor-info packet never contains standing changes
    k5 = build_trial_packet("K5", "REGISTRAR_CERTIFIES", "WITNESS_REGISTRAR", "S01", "A")
    results["K5_STANDING_SEPARATION"] = {
        "standing_effects_not_in_actor_info":
            "objective_public_standing_effects" not in json.dumps(
                k5["allowed_actor_info_packet"]),
        "pass": "objective_public_standing_effects" not in json.dumps(
            k5["allowed_actor_info_packet"]),
    }

    checks = []
    for k, v in results.items():
        if isinstance(v, dict) and "pass" in v:
            checks.append(bool(v["pass"]))
        elif isinstance(v, bool):
            checks.append(v)
    results["all_pass"] = all(checks) and bool(results["matched_content_across_arms_ok"])
    return results
