# v3/engine/validators.py — Pass 2 render output validation (particularity, jaggedness, no_repeats).
# Used by phenomenology and tests; re-prompt on failure with pass2_corrective_instruction(failures).

from __future__ import annotations

from typing import Any

PARTICULARITY_ANCHORS = (
    "place_anchor",
    "object_anchor",
    "schedule_anchor",
    "money_anchor",
    "language_anchor",
    "power_anchor",
    "body_anchor",
    "social_risk_anchor",
)


def _anchor_value(anchor: Any) -> str:
    """Extract display value from an anchor dict or string."""
    if isinstance(anchor, str):
        return anchor.strip()
    if isinstance(anchor, dict):
        v = anchor.get("value") or anchor.get("micro_detail") or anchor.get("name")
        if v is not None:
            return str(v).strip()
        for k, v in anchor.items():
            if isinstance(v, str) and v.strip():
                return v.strip()
    return ""


def validate_particularity(parsed: dict[str, Any]) -> tuple[bool, list[str]]:
    """Require 8 anchors with non-empty values. Returns (ok, failure_messages)."""
    failures: list[str] = []
    part = parsed.get("particularity") or {}
    if not isinstance(part, dict):
        return False, ["particularity must be an object with 8 anchors"]
    for key in PARTICULARITY_ANCHORS:
        if key not in part:
            failures.append(f"particularity missing anchor: {key}")
            continue
        val = _anchor_value(part[key])
        if not val:
            failures.append(f"particularity.{key} has no value")
    return len(failures) == 0, failures


def validate_jaggedness(parsed: dict[str, Any]) -> tuple[bool, list[str]]:
    """Require at least 2 contradiction pairs, each with 'and' list of 2. Returns (ok, failure_messages)."""
    failures: list[str] = []
    jag = parsed.get("jaggedness") or []
    if not isinstance(jag, list):
        return False, ["jaggedness must be an array"]
    if len(jag) < 2:
        failures.append("jaggedness must have at least 2 entries")
    for i, entry in enumerate(jag[:5]):
        if not isinstance(entry, dict):
            failures.append(f"jaggedness[{i}] must be an object")
            continue
        and_pair = entry.get("and")
        if not isinstance(and_pair, list) or len(and_pair) < 2:
            failures.append(f"jaggedness[{i}] must have 'and' array of 2 items")
    return len(failures) == 0, failures


def validate_no_repeats(
    parsed: dict[str, Any],
    history: list[dict[str, Any]] | None = None,
    min_novel_anchors: int = 2,
    history_years_used: int = 3,
) -> tuple[bool, list[str]]:
    """
    Require at least min_novel_anchors novel particularity anchors vs last history_years_used years.
    Lenient if history is short or particularity missing. Returns (ok, failure_messages).
    """
    failures: list[str] = []
    part = parsed.get("particularity") or {}
    if not isinstance(part, dict) or not part:
        return True, []  # no particularity => skip repeat check
    history = history or []
    recent = history[-history_years_used:] if len(history) > history_years_used else history
    if not recent:
        return True, []

    past_values: set[str] = set()
    for h in recent:
        p = h.get("particularity") or {}
        if isinstance(p, dict):
            for key in PARTICULARITY_ANCHORS:
                if key in p:
                    past_values.add(_anchor_value(p[key]).lower())

    novel = 0
    for key in PARTICULARITY_ANCHORS:
        if key not in part:
            continue
        v = _anchor_value(part[key]).lower()
        if v and v not in past_values:
            novel += 1
    if novel < min_novel_anchors:
        failures.append(
            f"no_repeats: need at least {min_novel_anchors} novel particularity anchors (found {novel})"
        )
    return len(failures) == 0, failures


def validate_render_output(
    parsed: dict[str, Any],
    history: list[dict[str, Any]] | None = None,
) -> tuple[bool, list[str]]:
    """
    Run particularity, jaggedness, and no_repeats validators.
    Returns (all_passed, list of failure messages).
    """
    all_failures: list[str] = []
    ok_p, failures_p = validate_particularity(parsed)
    if not ok_p:
        all_failures.extend(failures_p)
    ok_j, failures_j = validate_jaggedness(parsed)
    if not ok_j:
        all_failures.extend(failures_j)
    ok_r, failures_r = validate_no_repeats(parsed, history=history)
    if not ok_r:
        all_failures.extend(failures_r)
    return len(all_failures) == 0, all_failures
