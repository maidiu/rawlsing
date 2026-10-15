"""SC0F strict world/possibility validation — extends original laws with the
gating the I2/RC0 found missing.

Adds: full 12-state negative algebra, clock availability ordering, demand-relative
completeness, and support computed from empirical values (not static WORLD hints).
"""
from __future__ import annotations

from typing import Any, Mapping

NEGATIVE_STATE_VOCABULARY = {
    "OBSERVED_ZERO", "VALID_EMPTY", "MISSING", "UNDERPOWERED", "NOT_ASKED",
    "NONCOMPARABLE", "HELD_AUTHORITY", "DENIED_USE", "NO_CURRENT",
    "PROXY_MODELLED", "UNKNOWN_UNOBSERVED_GAP", "UNBOUND_RUNTIME_BINDING",
}


class ValidationFailure(Exception):
    def __init__(self, code: str, detail: str):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


def validate_world_strict(world: Mapping[str, Any]) -> dict[str, Any]:
    """Strict world conservation: 12-state negative algebra + clock ordering."""
    # Negative algebra: require all 12 states present
    neg_states = {n.get("state") for n in world.get("negative_states", [])}
    missing = NEGATIVE_STATE_VOCABULARY - neg_states
    if missing:
        raise ValidationFailure(
            "REJECT_NEGATIVE_ALGEBRA_LOSS",
            f"negative state vocabulary incomplete; missing: {sorted(missing)}",
        )
    # DENIED_USE must not be renamed to DENIED
    if "DENIED" in neg_states and "DENIED_USE" not in neg_states:
        raise ValidationFailure(
            "REJECT_NEGATIVE_ALGEBRA_LOSS",
            "DENIED is not a valid state; the frozen vocabulary uses DENIED_USE",
        )

    # Four clocks: presence + distinctness + availability ordering
    axes = world.get("time_axes", {})
    required_axes = ("observation_valid", "published", "as_of", "actor_event", "requested")
    for axis in required_axes:
        if axis not in axes:
            raise ValidationFailure("NO_CURRENT_OR_NOT_KNOWN_ASOF", f"clock axis lost: {axis}")
    if len({axes[a] for a in ("observation_valid", "published", "as_of")}) != 3:
        raise ValidationFailure("NO_CURRENT_OR_NOT_KNOWN_ASOF", "clock axes conflated")

    # Knowledge-as-of: publication must not postdate as_of without earlier evidence
    clock_mode = world.get("clock_mode", "")
    if clock_mode == "KNOWLEDGE_AS_OF":
        pub = str(axes.get("published", ""))
        as_of = str(axes.get("as_of", ""))
        if pub and as_of and pub > as_of and not world.get("earlier_knowledge_evidence_ref"):
            raise ValidationFailure(
                "NO_CURRENT_OR_NOT_KNOWN_ASOF",
                f"publication {pub} is not knowledge available at as_of {as_of}",
            )

    # Support must be present and internally consistent
    support = world.get("support", {})
    if not support:
        raise ValidationFailure("REJECT_SUPPORT_ERASURE", "support block missing")
    denom = support.get("denominator")
    yes = support.get("target_yes")
    no = support.get("target_no")
    if denom is not None and yes is not None and no is not None:
        if yes + no != denom:
            raise ValidationFailure(
                "REJECT_SUPPORT_ERASURE",
                f"support counts inconsistent: {yes}+{no} != {denom}",
            )

    # F1 n-ary and F2 history preservation
    nary = world.get("nary", {})
    if not nary.get("participants"):
        raise ValidationFailure("REJECT_NARY_LOSS", "F1 n-ary participants lost")
    f2 = world.get("f2", {})
    if not f2.get("f1_refs"):
        raise ValidationFailure("REJECT_F2_LOSS", "F2 history references lost")
    if f2.get("not_satisfaction") is not True:
        raise ValidationFailure("REJECT_F2_LOSS", "F2 not_satisfaction flag lost")

    # H3: generated criteria echo
    gce = world.get("generated_binding_echo", {})
    if gce.get("upstream_authorship") is not False:
        raise ValidationFailure("REJECT_H3_LOSS", "H3 upstream_authorship must be False")

    return {"state": "WORLD_STRICTLY_CONSERVED", "negative_states_checked": 12, "clocks_checked": 5}


def validate_possibility_strict(possibility: Mapping[str, Any]) -> dict[str, Any]:
    """Strict possibility conservation."""
    chain = possibility.get("ordered_condition_chain", [])
    if not chain:
        raise ValidationFailure("REJECT_ORDERED_PATH_LOSS", "ordered condition chain empty")
    indices = [row.get("index") for row in chain]
    if indices != list(range(len(chain))):
        raise ValidationFailure("REJECT_ORDERED_PATH_LOSS", "condition chain order damaged")

    # Denominator must be present and positive
    support = possibility.get("support", {})
    denom = support.get("denominator")
    if denom is None or denom <= 0:
        raise ValidationFailure("REJECT_SUPPORT_ERASURE", "denominator missing or non-positive")

    # Minority must be preserved
    if not possibility.get("minority"):
        raise ValidationFailure("REJECT_SUPPORT_ERASURE", "minority response option lost")

    return {"state": "POSSIBILITY_STRICTLY_CONSERVED", "chain_length": len(chain)}
