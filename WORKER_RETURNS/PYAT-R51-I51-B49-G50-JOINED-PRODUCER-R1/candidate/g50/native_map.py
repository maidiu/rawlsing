"""Stable mapping from symbolic operations to the bounded native I05 rule set."""
from __future__ import annotations

from .types import ScientificOperation

NATIVE_PREFIX = "I05_EXACT:"
SUPPORTED_CONDITION_ITEMS = ("A", "B", "M")


def native_rule_key(op: ScientificOperation) -> str | None:
    """Return the exact native coverage tag, or None when not natively expressible."""

    if op.state_variant != "COMPLETE_RESPONSE" or op.branch_depth not in (0, 1):
        return None
    if op.claim_class == "DIST" and op.targets == ("Y",) and not op.conditions:
        return "DIST-Y"
    if (
        op.claim_class in {"CONDITIONAL", "FORK"}
        and op.targets == ("Y",)
        and len(op.conditions) == 1
        and op.conditions[0][0] in SUPPORTED_CONDITION_ITEMS
        and op.conditions[0][1] in (0, 1)
    ):
        item, value = op.conditions[0]
        return f"COND-{item}{value}"
    if (
        op.claim_class == "INTERACTION"
        and op.targets == ("Y",)
        and op.condition_mode == "AND"
        and len(op.conditions) == 2
        and {c for c, _ in op.conditions} == {"A", "B"}
    ):
        return "GRID-AB"
    if (
        op.claim_class == "INTERACTION"
        and op.targets == ("Y",)
        and op.condition_mode == "XOR_EXACTLY_ONE"
        and op.conditions == (("A", 1), ("B", 1))
    ):
        return "XOR-AB"
    if (
        op.claim_class in {"JOINT", "CO_TRAVEL"}
        and op.targets == ("Y", "M")
        and not op.conditions
    ):
        return "JOINT-YM"
    if (
        op.claim_class == "FORK"
        and op.targets == ("Y",)
        and op.conditions == (("A", 1), ("M", 1))
        and op.branch_depth == 1
    ):
        return "FORK-A1-M1"
    return None


__all__ = ["native_rule_key", "NATIVE_PREFIX", "SUPPORTED_CONDITION_ITEMS"]
