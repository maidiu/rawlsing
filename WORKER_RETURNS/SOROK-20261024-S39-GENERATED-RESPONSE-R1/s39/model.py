"""Finite source-bound constructive response generation for S39."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .bootstrap import install

install()

from candidate import digest, seal  # noqa: E402

from .sources import (  # noqa: E402
    CONTEXT_KINDS,
    IGNORED_LABEL_KINDS,
    validate_source,
)

GRADE = "TEST_ONLY_CONSTRUCTIVE_GENERATION"
PROVENANCE = "TEST_ONLY_CONSTRUCTIVE_GENERATION_NOT_EXTERNALLY_OBSERVED"
RULE_ID = "S39_GUARDED_CONTEXTUAL_COMPARISON"
RULE_VERSION = "1"


class S39GenerationRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


@dataclass(frozen=True)
class GenerationOption:
    option_id: str
    s36_response_kind: str
    action: str
    performer: str


OPTIONS = (
    GenerationOption("ATTEND_OBJECT", "ATTEND_OBJECT", "INSPECT_OBJECT", "bp4.inspect"),
    GenerationOption("REQUEST_TOOL", "REQUEST_TOOL", "REQUEST_TOOL", "targetless.speech_request"),
    GenerationOption("EXPLICIT_REFUSAL", "EXPLICIT_REFUSAL", "EXPLICIT_REFUSAL", "targetless.refusal_event"),
)
OPTION_BY_ID = {item.option_id: item for item in OPTIONS}

REASON_MAP = {
    "REPAIR_URGENT": (
        ("REQUEST_TOOL", "SUPPORTS"),
        ("ATTEND_OBJECT", "SUPPORTS"),
        ("EXPLICIT_REFUSAL", "OBSTRUCTS"),
    ),
    "AVOID_DEBT": (
        ("REQUEST_TOOL", "OBSTRUCTS"),
        ("ATTEND_OBJECT", "SUPPORTS"),
        ("EXPLICIT_REFUSAL", "SUPPORTS"),
    ),
    "PREFER_INDEPENDENT": (
        ("ATTEND_OBJECT", "SUPPORTS"),
        ("REQUEST_TOOL", "OBSTRUCTS"),
    ),
    "PRIOR_B_SHARE": (
        ("REQUEST_TOOL", "SUPPORTS"),
        ("EXPLICIT_REFUSAL", "OBSTRUCTS"),
    ),
    "PRIOR_B_REFUSAL": (
        ("REQUEST_TOOL", "OBSTRUCTS"),
        ("EXPLICIT_REFUSAL", "SUPPORTS"),
    ),
}


@dataclass(frozen=True)
class ComparisonRule:
    rule_id: str
    version: str
    comparisons: tuple[Mapping[str, Any], ...]
    premises: tuple[str, ...]
    coverage: str = "FULL"

    def as_dict(self) -> dict:
        return {
            "schema": "S39_DECLARED_COMPARISON_RULE@1",
            "rule_id": self.rule_id,
            "version": self.version,
            "coverage": self.coverage,
            "premises": list(self.premises),
            "comparisons": [dict(row) for row in self.comparisons],
        }

    @property
    def content_hash(self) -> str:
        return digest(self.as_dict())


FULL_RULE = ComparisonRule(
    RULE_ID,
    RULE_VERSION,
    (
        {"id": "C1", "winner": "REQUEST_TOOL", "loser": "ATTEND_OBJECT",
         "all_of": ("REPAIR_URGENT", "PRIOR_B_SHARE", "EVENT_ACCESS", "ACTOR_PRESENT")},
        {"id": "C2", "winner": "REQUEST_TOOL", "loser": "EXPLICIT_REFUSAL",
         "all_of": ("REPAIR_URGENT", "PRIOR_B_SHARE", "EVENT_ACCESS")},
        {"id": "C3", "winner": "ATTEND_OBJECT", "loser": "REQUEST_TOOL",
         "all_of": ("PREFER_INDEPENDENT", "EVENT_ACCESS")},
        {"id": "C4", "winner": "EXPLICIT_REFUSAL", "loser": "REQUEST_TOOL",
         "all_of": ("PRIOR_B_REFUSAL", "EVENT_ACCESS")},
        {"id": "C5", "winner": "ATTEND_OBJECT", "loser": "EXPLICIT_REFUSAL",
         "all_of": ("PREFER_INDEPENDENT", "EVENT_ACCESS")},
        {"id": "C6", "winner": "EXPLICIT_REFUSAL", "loser": "ATTEND_OBJECT",
         "all_of": ("PRIOR_B_REFUSAL", "EVENT_ACCESS"), "none_of": ("REPAIR_URGENT",)},
        {"id": "C7", "winner": "ATTEND_OBJECT", "loser": "REQUEST_TOOL",
         "all_of": ("AVOID_DEBT", "PREFER_INDEPENDENT", "EVENT_ACCESS")},
        {"id": "C8", "winner": "EXPLICIT_REFUSAL", "loser": "REQUEST_TOOL",
         "all_of": ("AVOID_DEBT", "PRIOR_B_REFUSAL", "EVENT_ACCESS")},
    ),
    (
        "REPAIR_URGENT and PREFER_INDEPENDENT and AVOID_DEBT are explicit synthetic actor-context model premises",
        "PRIOR_B_SHARE and PRIOR_B_REFUSAL are synthetic historical episode model premises",
        "guarded pairwise comparisons are the declared finite constructive selection rule",
        "no scalar motive, random draw, first-option fallback, or default inaction",
    ),
    "FULL",
)


def _flags(sources: list[Mapping[str, Any]]) -> tuple[dict, list[dict]]:
    flags: dict[str, int] = {}
    used: list[dict] = []
    for record in sources:
        kind = record.get("source_class")
        if kind in IGNORED_LABEL_KINDS:
            continue
        if kind not in CONTEXT_KINDS:
            raise S39GenerationRefusal("S39_SOURCE_CLASS_INVALID", str(kind))
        predicate = str(record.get("predicate", ""))
        if predicate in flags and flags[predicate] != int(record.get("value", 0)):
            raise S39GenerationRefusal("S39_CONFLICTING_CONTEXT_SOURCE", predicate)
        flags[predicate] = int(record.get("value", 0))
        used.append(record)
    return flags, used


def _conditions_ok(row: Mapping[str, Any], flags: Mapping[str, int]) -> bool:
    if any(not flags.get(name, 0) for name in row.get("all_of", ())):
        return False
    if any(flags.get(name, 0) for name in row.get("none_of", ())):
        return False
    return True


def _has_cycle(edges: Mapping[str, set[str]], nodes: tuple[str, ...]) -> bool:
    state: dict[str, int] = {}

    def visit(node: str) -> bool:
        if state.get(node) == 1:
            return True
        if state.get(node) == 2:
            return False
        state[node] = 1
        for other in edges.get(node, set()):
            if visit(other):
                return True
        state[node] = 2
        return False

    return any(visit(node) for node in nodes)


def generate_choice(
    *,
    actor_id: str,
    branch_id: str,
    event_ref: str,
    event_time: int,
    as_of: int,
    c8_state_digest: str,
    access_witness: Mapping[str, Any],
    access_outcome: str,
    source_records: list[Mapping[str, Any]],
    world: Mapping[str, Any],
    rule: ComparisonRule = FULL_RULE,
) -> dict:
    if access_witness.get("actor_id") != actor_id:
        raise S39GenerationRefusal("S39_ACCESS_ACTOR_MISMATCH")
    if access_witness.get("event_ref") != event_ref:
        raise S39GenerationRefusal("S39_ACCESS_EVENT_MISMATCH")
    if access_outcome not in {
        "RECEIVABLE_NO_OBSERVED_UPTAKE",
        "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION",
        "OBSERVED_CURRENT_REFUSAL",
    }:
        raise S39GenerationRefusal("S39_EVENT_ACCESS_UNAVAILABLE", access_outcome)

    try:
        validated = [
            validate_source(record, actor_id=actor_id, branch_id=branch_id, as_of=as_of)
            for record in source_records
        ]
    except ValueError as exc:
        raise S39GenerationRefusal("S39_SOURCE_INTEGRITY_REFUSAL", str(exc)) from exc
    flags, used = _flags(validated)
    flags["EVENT_ACCESS"] = 1
    flags["ACTOR_PRESENT"] = 1 if world.get("actor_present") else 0
    flags["TOOL_ACCESSIBLE"] = 1 if world.get("tool_available") else 0
    flags["MATERIAL_AVAILABLE"] = 1 if world.get("material_available") else 0
    flags["FREE_HOURS"] = 1 if world.get("free_hours") else 0

    eligible = [
        option.option_id
        for option in OPTIONS
        if flags.get("EVENT_ACCESS") and flags.get("ACTOR_PRESENT")
    ]
    if not eligible:
        raise S39GenerationRefusal("S39_NO_ELIGIBLE_OPTION")

    reasons = []
    for record in used:
        predicate = str(record.get("predicate", ""))
        for option_id, relation in REASON_MAP.get(predicate, ()):
            reasons.append({
                "option_id": option_id,
                "relation": relation,
                "predicate": predicate,
                "source_ref": record["source_ref"],
                "source_hash": record["source_hash"],
                "source_class": record["source_class"],
                "recruitment_mode": record.get("recruitment_mode", ""),
                "model_premise": True,
            })

    defeated = []
    edges: dict[str, set[str]] = {option: set() for option in eligible}
    for row in rule.comparisons:
        if row.get("winner") not in eligible or row.get("loser") not in eligible:
            continue
        if _conditions_ok(row, flags):
            defeated.append({
                "comparison_id": row["id"],
                "winner": row["winner"],
                "loser": row["loser"],
                "conditions": list(row.get("all_of", ())),
            })
            edges[row["winner"]].add(row["loser"])

    if _has_cycle(edges, tuple(eligible)):
        status = "CONFLICT_UNRESOLVED"
        unresolved_reason = "COMPARISON_CYCLE"
        undominated: list[str] = []
    else:
        incoming = {option: set() for option in eligible}
        for winner, losers in edges.items():
            for loser in losers:
                incoming[loser].add(winner)
        undominated = sorted(option for option in eligible if not incoming[option])
        if len(undominated) == 1:
            status = "UNIQUE_SELECTED"
            unresolved_reason = ""
        elif len(undominated) > 1:
            status = "OPEN_CHOICE_SET"
            unresolved_reason = (
                "MISSING_COMPARISON" if rule.coverage != "FULL" else "MULTIPLE_SURVIVORS"
            )
        else:
            status = "CONFLICT_UNRESOLVED"
            unresolved_reason = "NO_UNDOMINATED_OPTION"

    selected = undominated[0] if status == "UNIQUE_SELECTED" else ""
    supporting = [row for row in reasons if row["option_id"] == selected and row["relation"] == "SUPPORTS"] if selected else []
    contrary = [row for row in reasons if row["option_id"] == selected and row["relation"] == "OBSTRUCTS"] if selected else []
    attempt_request = None
    if selected:
        option = OPTION_BY_ID[selected]
        attempt_request = seal({
            "schema": "S39_GENERATED_ATTEMPT_REQUEST@1",
            "grade": GRADE,
            "provenance": PROVENANCE,
            "native": False,
            "actor_id": actor_id,
            "branch_id": branch_id,
            "event_ref": event_ref,
            "event_time": event_time,
            "as_of": as_of,
            "c8_state_digest": c8_state_digest,
            "access_witness_hash": access_witness.get("hash", ""),
            "access_source_ref": access_witness.get("source_ref", ""),
            "access_source_hash": access_witness.get("source_hash", ""),
            "option_id": selected,
            "s36_response_kind": option.s36_response_kind,
            "action": option.action,
            "performer": option.performer,
            "supporting_reason_refs": [row["source_ref"] for row in supporting],
            "contrary_reason_refs": [row["source_ref"] for row in contrary],
            "selection_rule": {
                "rule_id": rule.rule_id,
                "version": rule.version,
                "content_hash": rule.content_hash,
                "coverage": rule.coverage,
            },
            "selection_basis": [row["comparison_id"] for row in defeated],
            "world_prerequisites": dict(world),
            "model_premises": list(rule.premises),
            "target_proposals": [],
        })

    receipt = seal({
        "schema": "S39_CONSTRUCTIVE_GENERATION_RECEIPT@1",
        "grade": GRADE,
        "provenance": PROVENANCE,
        "native": False,
        "actor_id": actor_id,
        "branch_id": branch_id,
        "event_ref": event_ref,
        "event_time": event_time,
        "as_of": as_of,
        "c8_state_digest": c8_state_digest,
        "access_witness_hash": access_witness.get("hash", ""),
        "access_source_ref": access_witness.get("source_ref", ""),
        "access_source_hash": access_witness.get("source_hash", ""),
        "access_outcome": access_outcome,
        "input_contains_desired_action": False,
        "options": [
            {"option_id": option.option_id, "action": option.action,
             "s36_response_kind": option.s36_response_kind,
             "eligible": option.option_id in eligible}
            for option in OPTIONS
        ],
        "reasons": reasons,
        "eligible_options": eligible,
        "defeated_pairs": defeated,
        "undominated_options": undominated,
        "selection_status": status,
        "unresolved_reason": unresolved_reason,
        "selected_option": selected,
        "supporting_reasons": supporting,
        "contrary_reasons": contrary,
        "attempt_request": attempt_request,
        "rule": {
            "rule_id": rule.rule_id,
            "version": rule.version,
            "content_hash": rule.content_hash,
            "coverage": rule.coverage,
            "premises": list(rule.premises),
        },
        "world_prerequisites": dict(world),
        "source_refs": [record["source_ref"] for record in used],
        "ignored_label_count": len(validated) - len(used),
        "target_proposals": [],
    })
    return receipt


__all__ = [
    "ComparisonRule",
    "FULL_RULE",
    "GRADE",
    "GenerationOption",
    "OPTIONS",
    "PROVENANCE",
    "RULE_ID",
    "RULE_VERSION",
    "S39GenerationRefusal",
    "generate_choice",
]
