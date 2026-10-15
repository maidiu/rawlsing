"""HQ298 S-M-LAB2 — pre-typed blind scoring (typed codes only; prose never scored).

PROVISIONAL LAB PROTOCOL — NOT ADOPTED LAW.
Two independent scorer implementations must agree (dual-scorer agreement).
Scorer inputs are restricted to (trial_id, counterbalance_code, selected_typed_code).
Any scoring that reads prose is INVALID by construction: prose objects are not
accepted by the scorer API at all.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Sequence

CODE_UNIVERSE = (
    "REQUEST_FEEDBACK", "SILENCE",
    "REQUEST_WITH_REPAIR", "REQUEST_WITH_CONDITIONAL_CAUTION",
    "HEIGHTENED_GUARD", "NEUTRAL_RESPONSE",
    "NARROWED_CONSULT", "REPEATED_QUESTION", "NO_ACTION",
    "ACCEPT_CERTIFICATE", "NO_STANDING_CHANGE_ACTION",
    "POLICING_CANDIDATE", "NO_SANCTION",
    "OTHER_UNSCORABLE",
)


class ScorerIntegrityError(ValueError):
    pass


@dataclass(frozen=True)
class ScorerInput:
    """The ONLY data a scorer may see. Prose is structurally absent."""
    trial_id: str
    counterbalance_code: str
    selected_typed_code: str

    def __post_init__(self):
        if not isinstance(self.selected_typed_code, str):
            raise ScorerIntegrityError("selected_typed_code must be a string")
        if "prose" in vars(self):
            raise ScorerIntegrityError("prose must never reach the scorer")


@dataclass
class ScoreRecord:
    trial_id: str
    counterbalance_code: str
    selected_typed_code: str
    expected_typed_codes: List[str]
    correct: bool
    scorable: bool


def scorer_alpha(inputs: Sequence[ScorerInput],
                 expected_by_trial: Dict[str, List[str]]) -> List[ScoreRecord]:
    """Scorer implementation ALPHA: direct membership test."""
    out: List[ScoreRecord] = []
    for i in inputs:
        exp = expected_by_trial.get(i.trial_id, [])
        scorable = i.selected_typed_code in CODE_UNIVERSE and i.selected_typed_code != "OTHER_UNSCORABLE"
        out.append(ScoreRecord(
            trial_id=i.trial_id,
            counterbalance_code=i.counterbalance_code,
            selected_typed_code=i.selected_typed_code,
            expected_typed_codes=list(exp),
            correct=bool(exp) and i.selected_typed_code in exp,
            scorable=scorable,
        ))
    return out


def scorer_beta(inputs: Sequence[ScorerInput],
                expected_by_trial: Dict[str, List[str]]) -> List[ScoreRecord]:
    """Scorer implementation BETA: independent set-based implementation.
    Must agree with ALPHA on every record (dual-scorer agreement)."""
    out: List[ScoreRecord] = []
    for i in inputs:
        exp_set = frozenset(expected_by_trial.get(i.trial_id) or ())
        scorable = (i.selected_typed_code in frozenset(CODE_UNIVERSE)
                    and i.selected_typed_code != "OTHER_UNSCORABLE")
        ok = False
        if exp_set:
            ok = i.selected_typed_code in exp_set
        out.append(ScoreRecord(
            trial_id=i.trial_id,
            counterbalance_code=i.counterbalance_code,
            selected_typed_code=i.selected_typed_code,
            expected_typed_codes=sorted(exp_set),
            correct=ok,
            scorable=scorable,
        ))
    return out


def dual_score(inputs: Sequence[ScorerInput],
               expected_by_trial: Dict[str, List[str]]) -> Dict[str, Any]:
    a = scorer_alpha(inputs, expected_by_trial)
    b = scorer_beta(inputs, expected_by_trial)
    disagreements = []
    for ra, rb in zip(a, b):
        if (ra.correct != rb.correct or ra.scorable != rb.scorable
                or ra.selected_typed_code != rb.selected_typed_code):
            disagreements.append({"trial_id": ra.trial_id,
                                  "alpha": asdict(ra), "beta": asdict(rb)})
    if disagreements:
        raise ScorerIntegrityError(
            f"SCORER_INTEGRITY_FAILURE: {len(disagreements)} disagreements")
    return {
        "scorer_agreement": True,
        "n_records": len(a),
        "records": [asdict(r) for r in a],
    }


def correctness_fraction(records: Sequence[ScoreRecord]) -> float:
    scorable = [r for r in records if r.scorable]
    if not scorable:
        return 0.0
    return sum(1 for r in scorable if r.correct) / len(scorable)


def blind_summary(records: Sequence[ScoreRecord],
                  group_key_fn) -> Dict[str, Any]:
    """Aggregate correctness per blind group (group label resolved AFTER scoring)."""
    groups: Dict[str, List[ScoreRecord]] = {}
    for r in records:
        groups.setdefault(group_key_fn(r), []).append(r)
    return {
        g: {
            "n": len(v),
            "correctness_fraction": round(correctness_fraction(v), 6),
            "n_correct": sum(1 for r in v if r.correct),
        }
        for g, v in sorted(groups.items())
    }


def compare_arms(per_arm_records: Dict[str, List[ScoreRecord]]) -> Dict[str, Any]:
    """Paired arm comparison vs A on typed correctness (promotion screening)."""
    base = correctness_fraction(per_arm_records.get("A", []))
    deltas = {}
    for arm, recs in per_arm_records.items():
        if arm == "A":
            continue
        frac = correctness_fraction(recs)
        deltas[arm] = {
            "correctness_fraction": round(frac, 6),
            "delta_vs_A_pp": round((frac - base) * 100.0, 3),
            "meets_plus_10pp_screen": (frac - base) >= 0.10,
            "equivalence_5pp": (
                "INDETERMINATE_WITHOUT_PROSPECTIVE_POWER"
                if abs(frac - base) < 0.05 else "DIFFERENTIATED"),
        }
    return {"A_correctness_fraction": round(base, 6), "comparisons": deltas}
