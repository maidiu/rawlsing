"""Two-contract adapter — RC0-repaired value-bearing port (sourcefree candidate).

Repairs over the HQ298 candidate (all demanded by RC0's independent court):
  * RC0_PERMISSION_ENTRYPOINT  — WORLD_READ fail-closed at adapter entry, even
    after revocation; no value or consumer effect is emitted before the check.
  * RC0_PARTIAL_ENTRYPOINT     — demand-relative source closure; a foreign
    demand is served PARTIAL_DEFERRED, never self-labelled COMPLETE; the
    candidate owns the partial-selection gate (K10_21).
  * RC0_CLOCK_LOOKAHEAD        — KNOWLEDGE_AS_OF cannot consume a later
    publication without a separately declared prior-knowledge binding.
  * RC0_REVERSAL_SCOPE         — reverse grants dereference scope, target and
    the independent REVERSE direction; the reverse slice is computed from the
    grant's own bindings, never from the forward receipt.
  * RC0_EXTRA_NEGATIVES        — complete 12-state negative algebra preserved
    with the original schema codes.
  * RC0_FROZEN_ENVELOPE        — receipts are produced by the TRUE SERIALIZER
    (port/envelope.py) and validate against the pinned draft-2020-12 envelope.
  * RC0_FACADE_SCOPE           — the facade binds consumer values/effects
    lineage; round-trip must not silently discard them.
  * RC0_PE_PORT_SEAM           — the empirical lane is computed through the
    pinned PE/C1/N10E producers with a real call counter.
"""
from __future__ import annotations

from typing import Any, Mapping

from port.contracts import (
    FACADE_CONTRACT_ID,
    POSSIBILITY_CONTRACT_ID,
    WORLD_CONTRACT_ID,
    PermissionDenied,
    PortContractError,
    canonical_json,
    compare_projections,
    consumer_effect_projection,
    ordered_possibility_projection,
    semantic_digest,
    semantic_world_projection,
)
from port.consumers import apply_consumers
from port.envelope import (
    project_possibility_receipt,
    project_world_receipt,
    validate_against_envelope,
)
from port.pinned_producer import ProducerCallCounter, compute_pinned_empirical_lane
from port.world_laws import (
    assert_complete_claim,
    validate_demand_closure,
    validate_knowledge_clock,
    validate_possibility,
    validate_world,
)


class TwoContractAdapter:
    """Adapter over any conforming provider; preserves both contracts exactly."""

    def __init__(self, provider: Any):
        self.provider = provider

    # ----------------------------------------------------------- entry gates
    def _fail_closed_entry(self, selection: Mapping[str, Any], demand: Mapping[str, Any]) -> None:
        """RC0_PERMISSION_ENTRYPOINT + RC0_CLOCK_LOOKAHEAD, before any value read."""

        ceiling = selection["world"].get("permission_ceiling") or {}
        revoked = set(ceiling.get("revoked_atoms") or [])
        allowed = set(ceiling.get("use_atoms") or [])
        if "WORLD_READ" in revoked or "WORLD_READ" not in allowed:
            raise PermissionDenied(
                "DENIED_USE",
                "WORLD_READ is revoked or absent from the source use ceiling; "
                "no selected values or consumer effects may be emitted",
            )
        validate_knowledge_clock(selection["world"])

    @staticmethod
    def _check_lane_support(lane: Mapping[str, Any], world: Mapping[str, Any]) -> None:
        """Producer-derived support must equal the declared fixture support.

        A static empirical hint can never satisfy the connection oracle: the
        served support is the computed lane's, and divergence is an integrity
        failure, not a silent substitution.
        """

        computed = lane.get("support") or {}
        declared = world.get("support") or {}
        for key in ("target_yes", "target_no", "denominator", "base_ratio", "minority_ratio"):
            if computed.get(key) != declared.get(key):
                raise PortContractError(
                    "INTEGRITY_FAILURE",
                    f"pinned producer lane support {key}={computed.get(key)!r} does not match "
                    f"the declared fixture support {declared.get(key)!r}",
                )
        if not lane.get("connected") or not lane.get("call_total"):
            raise PortContractError(
                "INTEGRITY_FAILURE",
                "empirical lane is not producer-connected (no pinned PE/C1/N10E calls)",
            )

    # --------------------------------------------------------------- run
    def run(
        self,
        demand: Mapping[str, Any] | None = None,
        consumer_ids: tuple[str, ...] | None = None,
    ) -> dict[str, Any]:
        demand = dict(demand or {"scope": "fx:universe:single_source|fx:release:v1"})

        with ProducerCallCounter() as counter:
            selection = self.provider.resolve_world_selection(demand)
            self._fail_closed_entry(selection, demand)
            validate_world(selection["world"])
            possibility = self.provider.ordered_possibility(selection, demand)
            validate_possibility(possibility)
            lane = compute_pinned_empirical_lane(counter=counter)
            self._check_lane_support(lane, selection["world"])
            effects = apply_consumers(self.provider, selection, possibility)
        if consumer_ids is not None:
            effects = {k: v for k, v in effects.items() if k in consumer_ids}

        closure = validate_demand_closure(demand, selection["world"])
        selection_state = selection["selection_state"]
        use_atoms = {
            "source_allowed": list(
                (selection["world"].get("permission_ceiling") or {}).get("use_atoms") or []
            ),
            "requested": list(self._requested_atoms(demand)),
            "effective": ["WORLD_READ", "POSSIBILITY_QUERY"],
        }
        refresh_state = {
            "predictable_boundaries": ["PUBLICATION_BOUNDARY", "GENERATED_BINDING"],
            "binding_fingerprint": semantic_digest(
                selection["world"]["generated_binding_echo"]
            ),
            "binding_generation": selection["binding_generation"],
            "publication_generation": selection["publication_generation"],
        }
        negative_states = list(selection["world"]["negative_states"])
        state_code = "PRESENT" if selection_state == "COMPLETE" else "PARTIAL_DEFERRED"
        state_reason = (
            "demand-relative source closure complete"
            if selection_state == "COMPLETE"
            else closure["reason"]
        )

        world_receipt = project_world_receipt(
            world=selection["world"],
            demand=demand,
            provider_lineage=self.provider.physical_lineage,
            selection_state=selection_state,
            selection_records=self._selection_records(selection),
            values_read={"values": {k: v for cid in effects
                                    for k, v in effects[cid]["values_read"].get("values", {}).items()}},
            use_atoms=use_atoms,
            refresh_state=refresh_state,
            generated_echo=selection["world"]["generated_binding_echo"],
            state_code=state_code,
            state_reason=state_reason,
            negative_states=negative_states,
        )
        possibility_receipt = project_possibility_receipt(
            world=selection["world"],
            possibility=possibility,
            computed_lane=lane,
            world_receipt=world_receipt,
            state_code="PRESENT",
        )

        facade = {
            "contract": FACADE_CONTRACT_ID,
            "role": "TAGGED_TRANSPORT_ONLY_NO_CALCULATION_NO_GRANT",
            "world_contract": world_receipt,
            "possibility_contract": possibility_receipt,
            "consumer_effects": effects,
            "consumer_effects_lineage": {
                cid: {
                    "consumer_digest": effects[cid]["consumer_digest"],
                    "values_read_digest": effects[cid]["values_read"]["digest"],
                    "value_keys": list(effects[cid]["values_read"]["keys"]),
                }
                for cid in sorted(effects)
            },
            "empirical_lane": {
                "producer": lane["producer"],
                "connected": lane["connected"],
                "calls": lane["calls"],
                "call_total": lane["call_total"],
                "lane_digest": lane["lane_digest"],
            },
            "facade_digest": semantic_digest(
                {
                    "world": world_receipt["receipt_ref"],
                    "possibility": possibility_receipt["receipt_ref"],
                    "consumers": {cid: effects[cid]["consumer_digest"] for cid in sorted(effects)},
                }
            ),
        }
        return {
            "world_receipt": world_receipt,
            "possibility_receipt": possibility_receipt,
            "consumer_effects": effects,
            "facade": facade,
            "world_model": selection["world"],
            "selection_state": selection_state,
            "empirical_lane": lane,
        }

    @staticmethod
    def _requested_atoms(demand: Mapping[str, Any]) -> tuple:
        return tuple(demand.get("requested_use_atoms") or ("WORLD_READ", "POSSIBILITY_QUERY"))

    @staticmethod
    def _selection_records(selection: Mapping[str, Any]) -> list:
        world = selection["world"]
        records = []
        for key in ("semantic_world_id", "absolute_horizon"):
            records.append({
                "demand_key": key,
                "decision": "SELECTED",
                "object_ref": {"kind": "WORLD_OBJECT", "id": key,
                               "hash": semantic_digest(world.get(key))},
                "status": {
                    "code": "PRESENT",
                    "scope_ref": {"kind": "SCOPE", "id": key, "hash": semantic_digest(key)},
                    "reason": "exact demand key resolved in source closure",
                    "recoverability": "NONE_SOURCE_INTRINSIC",
                },
                "use_atoms": ["WORLD_READ"],
                "dependency_refs": [],
            })
        return records

    # ------------------------------------------------------- facade round-trip
    @staticmethod
    def round_trip_two_contracts(facade_bundle: Mapping[str, Any]) -> dict[str, Any]:
        """Reversible dereference: BOTH contracts AND consumer lineage must survive."""

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
        # RC0_FACADE_SCOPE: consumer values/effects lineage may not be discarded
        lineage = facade.get("consumer_effects_lineage")
        if lineage is None:
            raise PortContractError(
                "REJECT_SEMANTIC_LOSS", "facade carries no consumer values/effects lineage")
        effects = facade.get("consumer_effects") or {}
        if set(lineage) != set(effects):
            raise PortContractError(
                "REJECT_SEMANTIC_LOSS", "consumer lineage does not cover the consumer effects")
        for cid, entry in lineage.items():
            effect = effects[cid]
            if entry["consumer_digest"] != effect["consumer_digest"]:
                raise PortContractError(
                    "REJECT_SEMANTIC_LOSS", f"consumer digest lost in round-trip: {cid}")
            if entry["values_read_digest"] != effect["values_read"]["digest"]:
                raise PortContractError(
                    "REJECT_SEMANTIC_LOSS", f"consumer values-read lineage lost: {cid}")
            if list(effect["values_read"]["keys"]) != list(entry["value_keys"]):
                raise PortContractError(
                    "REJECT_SEMANTIC_LOSS", f"consumer value keys lost: {cid}")
        return {
            "state": "LOSSLESS_TWO_CONTRACT_ROUNDTRIP_WITH_CONSUMER_LINEAGE",
            "facade_digest": facade["facade_digest"],
            "consumers_bound": sorted(lineage),
        }

    # --------------------------------------------------------------- gates
    @staticmethod
    def assert_complete(selection_state: str, *, context: str = "") -> dict:
        return assert_complete_claim(selection_state, context=context)

    @staticmethod
    def validate_receipts(bundle: Mapping[str, Any]) -> dict:
        """Validate BOTH receipts against the pinned envelope (true serializer view)."""

        errors = {
            "world_receipt": validate_against_envelope(bundle["world_receipt"]),
            "possibility_receipt": validate_against_envelope(bundle["possibility_receipt"]),
        }
        return {"errors": errors, "valid": not any(errors.values())}


def provider_equivalence_report(a_bundle: Mapping[str, Any], b_bundle: Mapping[str, Any]) -> dict[str, Any]:
    """K9 equivalence: conserved projections equal; physical lineage may differ."""

    wa = semantic_world_projection(a_bundle["world_model"])
    wb = semantic_world_projection(b_bundle["world_model"])
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
