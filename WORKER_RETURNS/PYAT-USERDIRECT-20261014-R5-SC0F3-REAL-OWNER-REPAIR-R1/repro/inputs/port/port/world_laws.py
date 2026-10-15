"""Structural conservation laws for the SC0 port (K10 mutation detector).

Independently encoded checks over the semantic world/possibility payloads.  Each
law names the frozen K10 expected class it enforces.  Signature-ordered: the
most specific mutation signature wins so each of the 28 frozen classes is
reproducible exactly.  Anything unexpected is RED, never normalized.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from port.contracts import (
    NEGATIVE_STATES,
    PSYCHIC_TOKENS,
    PortContractError,
    SemanticLossError,
)

REQUIRED_WORLD_KEYS = (
    "semantic_world_id",
    "source_ref",
    "source_release_ref",
    "epistemic_grade",
    "native_unit",
    "native_strata",
    "absolute_horizon",
    "nary",
    "f2",
    "f1_refs",
    "f2_requirement_ref",
    "public_categories",
    "public_sanctions",
    "authority_ref",
    "time_axes",
    "clock_mode",
    "contradictory_alternatives",
    "support",
    "negative_states",
    "routes",
    "permission_ceiling",
    "values",
    "generated_binding_echo",
)

REQUIRED_TIME_AXES = ("observation_valid", "published", "as_of", "actor_event", "requested")
REQUIRED_VALUE_KEYS = ("fx:AH", "fx:stratum:A", "fx:stratum:B", "fx:rule:public_access_2008", "fx:rule:mutual_aid")


def validate_world(world: Mapping[str, Any]) -> dict[str, Any]:
    """Full structural validation; raises typed errors naming the frozen class."""

    missing = [k for k in REQUIRED_WORLD_KEYS if k not in world]
    if missing:
        raise SemanticLossError("REJECT_SEMANTIC_LOSS", f"declared world fields dropped: {missing}")

    values = world["values"]

    # K10_23 OPAQUE_HASH_NO_VALUES: values replaced by opaque hashes (most specific)
    if values and all(
        isinstance(v, str) and v.startswith("sha256:") for v in values.values()
    ):
        raise PortContractError(
            "REJECT_UNVERIFIABLE_CONSUMER_USE", "opaque hashes replaced readable world values"
        )

    # K10_01 DROP_AH
    ah = world["absolute_horizon"]
    if not ah or ah not in values:
        raise SemanticLossError("REJECT_SEMANTIC_LOSS", "absolute horizon dropped or not dereferenceable")

    for key in REQUIRED_VALUE_KEYS:
        if key not in values:
            raise PortContractError(
                "REJECT_UNVERIFIABLE_CONSUMER_USE", f"selected world value missing: {key}"
            )

    # K10_02 STRATUM_TRANSLATION: non-injective stratum coordinate mapping
    labels = []
    for s in world["native_strata"]:
        entry = values.get(s)
        if not isinstance(entry, Mapping) or entry.get("label") is None:
            raise SemanticLossError("REJECT_NONINJECTIVE_COORDINATE", f"stratum {s} lost its native value")
        labels.append(entry.get("label"))
    if len(set(labels)) != len(labels):
        raise SemanticLossError("REJECT_NONINJECTIVE_COORDINATE", "stratum translation is non-injective")

    # K10_03 DYADIZE_NARY
    nary = world["nary"]
    if nary.get("cardinality") != 3 or len(nary.get("participants", [])) != 3:
        raise SemanticLossError("REJECT_CARDINALITY_ROLE_TOPOLOGY_LOSS", "n-ary triad was dyadized or truncated")
    ordinals = [p.get("ordinal") for p in nary["participants"]]
    if ordinals != sorted(ordinals) or nary.get("ordered") is not True:
        raise SemanticLossError("REJECT_CARDINALITY_ROLE_TOPOLOGY_LOSS", "roles/order changed")
    roles = [p.get("role") for p in nary["participants"]]
    if roles != ["institution", "applicant", "third-party"]:
        raise SemanticLossError("REJECT_CARDINALITY_ROLE_TOPOLOGY_LOSS", "participant roles changed")

    # K10_04 DROP_F2_HISTORY_REQUIREMENT
    f2 = world["f2"]
    if not f2.get("history_requirement_ref") or f2.get("history_requirement_ref") != world.get("f2_requirement_ref"):
        raise SemanticLossError("REJECT_F2_PREREQUISITE_LOSS", "F2 history/prerequisite requirement dropped")
    if not f2.get("predicate_ref"):
        raise SemanticLossError("REJECT_F2_PREREQUISITE_LOSS", "F2 predicate requirement dropped")

    # K10_05 PREDICATE_BECOMES_EXPERIENCE (f2 predicate/history area)
    f2_blob = repr(f2).upper()
    for token in PSYCHIC_TOKENS:
        if token in f2_blob:
            raise PortContractError(
                "REJECT_ACTOR_FIREWALL", f"predicate/history became experience: {token}"
            )

    # K10_25 UPSTREAM_PSYCHIC_FIELDS (other world fields)
    world_without_f2 = repr({k: v for k, v in world.items() if k not in ("f2",)}).upper()
    for token in PSYCHIC_TOKENS:
        if token in world_without_f2:
            raise PortContractError(
                "REJECT_ACTOR_JURISDICTION", f"upstream psychic field present: {token}"
            )

    # K10_06 CONTRADICTION_DOMINANT_ONLY
    states = {row.get("state") for row in world["contradictory_alternatives"]}
    if "POSSIBLE" not in states or "CONTRADICTORY_SOURCE_SCOPE" not in states:
        raise SemanticLossError("REJECT_ALTERNATIVE_ERASURE", "contradictory/minority alternative erased")

    # K10_07 MINORITY_ERASE
    support = world["support"]
    if support.get("target_yes") != 54 or support.get("target_no") != 6 or support.get("denominator") != 60:
        raise SemanticLossError("REJECT_SUPPORT_ERASURE", "support/minority counts changed")
    if support.get("minority_ratio") != "6/60":
        raise SemanticLossError("REJECT_SUPPORT_ERASURE", "minority ratio erased")

    # K10_08/09/10 negative algebra by exact scope
    by_scope = {row.get("scope"): row for row in world["negative_states"]}
    expected_states = {
        "fx:scope:measured-zero": "OBSERVED_ZERO",
        "fx:scope:complete-empty": "VALID_EMPTY",
        "fx:scope:missing": "MISSING",
        "fx:scope:power": "UNDERPOWERED",
        "fx:scope:notasked": "NOT_ASKED",
        "fx:scope:incomparable": "NONCOMPARABLE",
        "fx:scope:held": "HELD_AUTHORITY",
        "fx:scope:denied": "DENIED",
    }
    notasked = by_scope.get("fx:scope:notasked")
    if notasked is None or notasked.get("state") != "NOT_ASKED":
        raise PortContractError("REJECT_ROUTING_NONRESPONSE_LOSS", "not-asked routing state lost")
    power = by_scope.get("fx:scope:power")
    if power is None or power.get("state") == "VALID_EMPTY" or power.get("measure") is not None:
        raise PortContractError("REJECT_UNDERPOWERED_ERASURE", "underpowered erased")
    missing_row = by_scope.get("fx:scope:missing")
    if missing_row is None or missing_row.get("measure") is not None:
        raise SemanticLossError("REJECT_NEGATIVE_ALGEBRA_COLLAPSE", "missing collapsed into measured")
    zero_row = by_scope.get("fx:scope:measured-zero")
    if zero_row is None or zero_row.get("measure") != 0 or zero_row.get("state") != "OBSERVED_ZERO":
        raise SemanticLossError("REJECT_NEGATIVE_ALGEBRA_COLLAPSE", "observed zero collapsed")
    if set(by_scope) != set(expected_states) or {
        s: by_scope[s].get("state") for s in by_scope
    } != expected_states:
        raise SemanticLossError("REJECT_NEGATIVE_ALGEBRA_COLLAPSE", f"negative state algebra changed: {sorted(by_scope)}")

    # K10_17 BINDING_AS_OBSERVATION
    echo = world["generated_binding_echo"]
    if echo.get("upstream_authorship") is not False:
        raise PortContractError("REJECT_GENERATED_FACT_PROMOTION", "generated binding promoted to observation")
    if echo.get("channel") != "H3_GENERATED_BINDING_ECHO_FILTER_ONLY":
        raise PortContractError("REJECT_GENERATED_FACT_PROMOTION", "H3 echo semantics lost")

    # K10_22 PROXY_AS_OBSERVED (grade or route grade promoted)
    if world["epistemic_grade"] != "TEST_FIXTURE_ONLY":
        raise PortContractError("REJECT_EPISTEMIC_PROMOTION", f"grade promoted to {world['epistemic_grade']!r}")
    for rid, route in world["routes"].items():
        if route.get("epistemic_grade") not in (None, "TEST_FIXTURE_ONLY"):
            raise PortContractError("REJECT_EPISTEMIC_PROMOTION", f"route {rid} promoted to {route.get('epistemic_grade')!r}")

    # K10_26 F2_PUBLIC_SANCTION
    if len(world["public_categories"]) != 2 or len(world["public_sanctions"]) != 2:
        raise SemanticLossError("REJECT_PUBLIC_RULE_AND_OWNER_LOSS", "public category/sanction set lost")
    for rid, route in world["routes"].items():
        if not route.get("rule_ref") or not route.get("sanction_refs"):
            raise SemanticLossError("REJECT_PUBLIC_RULE_AND_OWNER_LOSS", "route lost public rule/sanction owner")

    # K10_15 CLOCK_CONFLATION
    axes = world["time_axes"]
    for axis in REQUIRED_TIME_AXES:
        if axis not in axes:
            raise PortContractError("NO_CURRENT_OR_NOT_KNOWN_ASOF", f"clock axis lost: {axis}")
    if world.get("clock_mode") != "KNOWLEDGE_AS_OF":
        raise PortContractError("NO_CURRENT_OR_NOT_KNOWN_ASOF", "clock mode conflated")
    if len({axes[a] for a in ("observation_valid", "published", "as_of")}) != 3:
        raise PortContractError("NO_CURRENT_OR_NOT_KNOWN_ASOF", "clock axes conflated")

    return {"state": "WORLD_STRUCTURALLY_CONSERVED", "checked_laws": 16}


def validate_possibility(receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Ordered-possibility conservation laws (K10_11/13/14/24)."""

    chain = receipt.get("ordered_condition_chain") or []
    idx = [row.get("index") for row in chain]
    if idx != sorted(idx) or idx != list(range(len(idx))):
        raise PortContractError("REJECT_ORDERED_PATH_LOSS", "ordered conditioner path sorted/set-collapsed")
    if [row.get("n") for row in chain] != [60, 30, 12]:
        raise PortContractError("REJECT_ORDERED_PATH_LOSS", "ordered 60->30->12 path damaged")
    if receipt.get("sampling_unit") != "RESPONDENT":
        raise PortContractError("REFUSE_SAMPLING_UNIT_JOINT", "sampling unit not native respondent unit")
    if receipt.get("uncertainty") in ("POINT_ESTIMATE", None):
        raise PortContractError("REJECT_MODEL_PRECISION_INVENTION", "uncertainty replaced by point estimate")
    if receipt.get("model_use") not in ("TEST_ONLY", "UNISSUED"):
        raise PortContractError("REFUSE_UNAUTHORIZED_COMPOSITION", "implicit model cross-product without issuer")
    return {"state": "POSSIBILITY_STRUCTURALLY_CONSERVED"}


def context_fingerprint(selection: Mapping[str, Any]) -> dict[str, Any]:
    world = selection.get("world", {})
    return {
        "binding_echo": world.get("generated_binding_echo"),
        "published": (world.get("time_axes") or {}).get("published"),
        "binding_generation": selection.get("binding_generation"),
        "publication_generation": selection.get("publication_generation"),
    }


def validate_freshness(
    current_selection: Mapping[str, Any],
    *,
    prior_fingerprint: Mapping[str, Any],
) -> dict[str, Any]:
    """K10_18/19: content drift without its H2 refresh successor is stale context."""

    current = context_fingerprint(current_selection)
    if current["binding_echo"] != prior_fingerprint["binding_echo"]:
        if current["binding_generation"] == prior_fingerprint["binding_generation"]:
            raise PortContractError(
                "REJECT_STALE_BINDING_CONTEXT",
                "generated binding changed without an H2 binding-refresh successor",
            )
    if current["published"] != prior_fingerprint["published"]:
        if current["publication_generation"] == prior_fingerprint["publication_generation"]:
            raise PortContractError(
                "REJECT_STALE_REPOSITORY_CONTEXT",
                "publication boundary crossed without an H2 publication-refresh successor",
            )
    return {"state": "FRESH_CONTEXT"}


def _load_frozen_k10_classes() -> dict:
    """Frozen expected classes are read from the pinned SC0 oracle, never retyped."""

    import json

    oracle = Path(__file__).resolve().parents[1] / "oracles" / "03_K10_STRUCTURAL_INFO_LOSS_ORACLES.json"
    data = json.loads(oracle.read_text())
    return {row["id"]: row["expected"] for row in data["cases"]}


K10_EXPECTED_CLASSES = _load_frozen_k10_classes()
