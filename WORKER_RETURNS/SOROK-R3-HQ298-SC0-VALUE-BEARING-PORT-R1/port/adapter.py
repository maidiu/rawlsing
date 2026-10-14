"""Two-contract adapter: strictly lossless tagged dispatcher (transport only).

Carries a GENERIC_WORLD_SELECTION receipt and a GENERIC_ORDERED_POSSIBILITY
receipt as two distinct contracts; the optional facade is transport, never a
third authority or a merged estimator.  Reversible dereference is provided by
round-trip back to the two original receipts with their lineages intact.
"""
from __future__ import annotations

from typing import Any, Mapping

from port.contracts import (
    FACADE_CONTRACT_ID,
    POSSIBILITY_CONTRACT_ID,
    WORLD_CONTRACT_ID,
    PortContractError,
    canonical_json,
    compare_projections,
    consumer_effect_projection,
    ordered_possibility_projection,
    semantic_digest,
    semantic_world_projection,
)
from port.consumers import apply_consumers
from port.world_laws import validate_possibility, validate_world


class TwoContractAdapter:
    """Adapter over any conforming provider; preserves both contracts exactly."""

    def __init__(self, provider: Any):
        self.provider = provider

    def run(
        self,
        demand: Mapping[str, Any] | None = None,
        consumer_ids: tuple[str, ...] | None = None,
    ) -> dict[str, Any]:
        demand = dict(demand or {"scope": "fx:scope:town2008"})
        selection = self.provider.resolve_world_selection(demand)
        validate_world(selection["world"])
        possibility = self.provider.ordered_possibility(selection, demand)
        validate_possibility(possibility)
        effects = apply_consumers(self.provider, selection, possibility)
        if consumer_ids is not None:
            effects = {k: v for k, v in effects.items() if k in consumer_ids}
        world_receipt = {
            "contract": WORLD_CONTRACT_ID,
            "selection_digest": selection["selection_digest"],
            "provider": selection["provider"],
            "world": selection["world"],
            "selection_state": selection["selection_state"],
            "binding_generation": selection["binding_generation"],
            "publication_generation": selection["publication_generation"],
            "grade": selection["grade"],
        }
        possibility_receipt = {
            **possibility,
            "values_read_by_consumers": {
                cid: effects[cid]["values_read"] for cid in sorted(effects)
            },
            "n9_snapshot_ref": selection["selection_digest"],
        }
        facade = {
            "contract": FACADE_CONTRACT_ID,
            "role": "TAGGED_TRANSPORT_ONLY_NO_CALCULATION_NO_GRANT",
            "world_contract": world_receipt,
            "possibility_contract": possibility_receipt,
            "consumer_effects": effects,
            "facade_digest": semantic_digest(
                {
                    "world": world_receipt["selection_digest"],
                    "possibility": possibility_receipt["replay_digest"],
                    "consumers": {cid: effects[cid]["consumer_digest"] for cid in sorted(effects)},
                }
            ),
        }
        return {
            "world_receipt": world_receipt,
            "possibility_receipt": possibility_receipt,
            "consumer_effects": effects,
            "facade": facade,
        }

    @staticmethod
    def round_trip_two_contracts(facade_bundle: Mapping[str, Any]) -> dict[str, Any]:
        """Reversible dereference: split the facade back to the two contracts."""

        facade = facade_bundle["facade"]
        if facade["role"] != "TAGGED_TRANSPORT_ONLY_NO_CALCULATION_NO_GRANT":
            raise PortContractError("REJECT_SEMANTIC_LOSS", "facade is not transport-only")
        world = facade["world_contract"]
        possibility = facade["possibility_contract"]
        if world["contract"] != WORLD_CONTRACT_ID or possibility["contract"] != POSSIBILITY_CONTRACT_ID:
            raise PortContractError("REJECT_SEMANTIC_LOSS", "facade tag drift")
        if canonical_json(world) != canonical_json(facade_bundle["world_receipt"]):
            raise PortContractError("REJECT_SEMANTIC_LOSS", "world contract did not round-trip")
        if canonical_json(possibility) != canonical_json(facade_bundle["possibility_receipt"]):
            raise PortContractError("REJECT_SEMANTIC_LOSS", "possibility contract did not round-trip")
        return {"state": "LOSSLESS_TWO_CONTRACT_ROUNDTRIP", "facade_digest": facade["facade_digest"]}


def provider_equivalence_report(a_bundle: Mapping[str, Any], b_bundle: Mapping[str, Any]) -> dict[str, Any]:
    """K9 equivalence: conserved projections equal; physical lineage may differ."""

    wa = semantic_world_projection(a_bundle["world_receipt"])
    wb = semantic_world_projection(b_bundle["world_receipt"])
    pa = ordered_possibility_projection(a_bundle["possibility_receipt"])
    pb = ordered_possibility_projection(b_bundle["possibility_receipt"])
    world_diffs = compare_projections(wa, wb)
    possibility_diffs = compare_projections(pa, pb)
    consumer_diffs = []
    for cid in sorted(a_bundle["consumer_effects"]):
        ca = consumer_effect_projection({"consumer_effects": a_bundle["consumer_effects"]}, cid)
        cb = consumer_effect_projection({"consumer_effects": b_bundle["consumer_effects"]}, cid)
        consumer_diffs.extend(compare_projections(ca, cb))
    lineage_differs = (
        a_bundle["world_receipt"]["provider"]["physical_provider_id"]
        != b_bundle["world_receipt"]["provider"]["physical_provider_id"]
    )
    return {
        "world_projection_diffs": world_diffs,
        "possibility_projection_diffs": possibility_diffs,
        "consumer_effect_diffs": consumer_diffs,
        "physical_provider_ids_differ": lineage_differs,
        "equivalent_except_physical_lineage": not world_diffs
        and not possibility_diffs
        and not consumer_diffs
        and lineage_differs,
    }
