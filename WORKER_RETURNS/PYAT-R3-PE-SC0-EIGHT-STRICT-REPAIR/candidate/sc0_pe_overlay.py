"""SC0 value-bearing overlay for the pinned PE candidate.

The overlay is TEST_FIXTURE_ONLY and SOURCEFREE.  It does not edit the pinned
PE module, issue operative N9, grant source/actor rights or claim model use.
It executes the frozen HQ298 SC0 fixture provider and attaches value-bearing
world/consumer fields to a PE receipt only after the original PE service has
accepted the request and produced exact C1/N10E geometry.
"""
from __future__ import annotations

import copy
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
import rawlsing_next.pre553_postastra_pe_generic_world_possibility as pe
from port.adapter import TwoContractAdapter
from port.provider_a import build_provider_a

GRADE = "TEST_FIXTURE_ONLY__SOURCEFREE__NOT_OPERATIVE_N9__NOT_MODEL_USE"
OVERLAY_ID = "PYAT_R3_PE_SC0_VALUE_BEARING_OVERLAY@1"
REQUIRED_STATUSES = frozenset({
    "OBSERVED_ZERO", "VALID_EMPTY", "MISSING", "UNDERPOWERED",
    "NOT_ASKED", "NONCOMPARABLE", "HELD_AUTHORITY", "DENIED_USE",
})
REQUIRED_CLOCKS = frozenset({
    "observation_effective", "publication_knowledge",
    "actor_event", "request_currentness",
})
REQUIRED_CONSUMERS = (
    "CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY",
    "NONPARENT_APPRENTICESHIP_ENTRY",
)
SC0_WORLD_FIELDS = (
    "absolute_horizon", "native_strata", "nary", "f2",
    "public_sanctions", "public_categories", "contradictory_alternatives",
)


class Sc0OverlayContractError(RuntimeError):
    """Fail-closed overlay error; no partially enriched receipt is returned."""


def fixture_bundle() -> dict[str, Any]:
    provider = build_provider_a()
    return TwoContractAdapter(provider).run()


def _require(condition: bool, reason: str) -> None:
    if not condition:
        raise Sc0OverlayContractError(reason)


def _validate_bundle(bundle: Mapping[str, Any]) -> None:
    world_receipt = bundle.get("world_receipt") or {}
    world = world_receipt.get("world") or {}
    possibility = bundle.get("possibility_receipt") or {}
    effects = bundle.get("consumer_effects") or {}
    _require(world_receipt.get("selection_digest"), "MISSING_WORLD_SELECTION_DIGEST")
    _require(possibility.get("ordered_condition_chain"), "MISSING_ORDERED_CONDITION_CHAIN")
    for name in SC0_WORLD_FIELDS:
        _require(name in world, f"MISSING_SC0_WORLD_FIELD:{name}")
    _require((world.get("time_axes") or {}).get("observation_valid"), "MISSING_OBSERVATION_CLOCK")
    _require((world.get("time_axes") or {}).get("published"), "MISSING_PUBLICATION_CLOCK")
    _require(world.get("support", {}).get("denominator"), "MISSING_WORLD_DENOMINATOR")
    _require((world.get("generated_binding_echo") or {}).get("upstream_authorship") is False,
             "GENERATED_BINDING_ECHO_SOURCE_PROMOTION")
    statuses = {
        ("DENIED_USE" if row.get("state") == "DENIED" else row.get("state"))
        for row in world.get("negative_states") or ()
    }
    _require(REQUIRED_STATUSES <= statuses, "MISSING_NEGATIVE_STATUS_ALGEBRA")
    for consumer_id in REQUIRED_CONSUMERS:
        effect = effects.get(consumer_id)
        _require(isinstance(effect, Mapping), f"MISSING_CONSUMER_EFFECT:{consumer_id}")
        _require(effect.get("values_read", {}).get("keys"), f"MISSING_CONSUMER_VALUES_READ:{consumer_id}")
        _require(effect.get("consumer_digest"), f"MISSING_CONSUMER_DIGEST:{consumer_id}")
    nonparent = effects["NONPARENT_APPRENTICESHIP_ENTRY"]
    _require(nonparent.get("output", {}).get("apprenticeship_access_routes"),
             "MISSING_NONPARENT_ROUTE_OUTPUT")
    _require(nonparent.get("person_generation") == "NONE", "NONPARENT_PERSON_GENERATION_FORBIDDEN")
    conception = effects["CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY"]
    _require(conception.get("output", {}).get("eligible_scenario_constraints"),
             "MISSING_CONCEPTION_CONSTRAINT_OUTPUT")
    _require(conception.get("person_generation") == "NONE", "CONCEPTION_PERSON_GENERATION_FORBIDDEN")


def _validate_geometry(result: Any) -> tuple[Mapping[str, Any], Any, int]:
    geometry = result.receipt.consumer_exact_geometry or {}
    cells = list(geometry.get("cells") or [])
    denominator = (geometry.get("denominator") or {}).get("raw_denominator_support")
    _require(bool(cells), "MISSING_PE_CONSUMER_EXACT_GEOMETRY_CELLS")
    _require(isinstance(denominator, int) and denominator > 0, "MISSING_PE_RAW_DENOMINATOR")
    first = cells[0]
    numerator = first.get("raw_numerator_support")
    _require(isinstance(numerator, int), "MISSING_PE_RAW_NUMERATOR")
    _require(numerator <= denominator, "PE_NUMERATOR_EXCEEDS_DENOMINATOR")
    _require(geometry.get("denominator", {}).get("raw_denominator_support") == denominator,
             "PE_DENOMINATOR_MISMATCH")
    return geometry, first, denominator


def _n9_world(original: Mapping[str, Any], request: Any, bundle: Mapping[str, Any]) -> dict[str, Any]:
    world = bundle["world_receipt"]["world"]
    n9 = dict(original)
    n9.update({
        "absolute_horizon": copy.deepcopy(world["absolute_horizon"]),
        "native_strata": copy.deepcopy(world["native_strata"]),
        "nary": copy.deepcopy(world["nary"]),
        "f2": copy.deepcopy(world["f2"]),
        "public_sanctions": copy.deepcopy(world["public_sanctions"]),
        "public_categories": copy.deepcopy(world["public_categories"]),
        "contradictory_alternatives": copy.deepcopy(world["contradictory_alternatives"]),
        "binding_echo": {
            **copy.deepcopy(world["generated_binding_echo"]),
            "tag": "GENERATED_RUNTIME_FACT_REF",
            "may_use_as_source_observation": False,
        },
        "clocks": {
            "observation_effective": world["time_axes"]["observation_valid"],
            "publication_knowledge": world["time_axes"]["published"],
            "actor_event": None,
            "request_currentness": request.request_time,
        },
        "actor_event_reason": "NO_ACTOR_EVENT_AUTHORITY__TEST_FIXTURE_ONLY",
        "scoped_status_rows": [
            {
                "state": "DENIED_USE" if row["state"] == "DENIED" else row["state"],
                "scope": row.get("scope"),
                "measure": row.get("measure"),
                "observed_complete": row.get("observed_complete"),
            }
            for row in world["negative_states"]
        ],
        "native_sampling_unit": world["native_unit"],
        "native_risk_set_ref": world["support"]["risk_set"],
        "original_routing_ref": world["support"]["routing"],
        "world_carriage_grade": GRADE,
    })
    _require(set(n9["clocks"]) == REQUIRED_CLOCKS, "CLOCK_AXES_NOT_EXACT")
    return n9


def _refresh_receipts(bundle: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    world_receipt = bundle["world_receipt"]
    world = world_receipt["world"]
    selection_digest = world_receipt["selection_digest"]
    publication_generation = world_receipt["publication_generation"]
    binding_generation = world_receipt["binding_generation"]
    publication = {
        "channel": "H2_PUBLICATION_BOUNDARY_REFRESH",
        "world_result_ref": selection_digest,
        "generation": publication_generation,
        "successor_ref": semantic_hash({
            "channel": "H2_PUBLICATION_BOUNDARY_REFRESH",
            "selection_digest": selection_digest,
            "generation": publication_generation,
            "time_axes": world["time_axes"],
        }),
    }
    binding = {
        "channel": "H2_GENERATED_BINDING_REFRESH",
        "world_result_ref": selection_digest,
        "generation": binding_generation,
        "successor_ref": semantic_hash({
            "channel": "H2_GENERATED_BINDING_REFRESH",
            "selection_digest": selection_digest,
            "generation": binding_generation,
            "generated_binding_echo": world["generated_binding_echo"],
        }),
    }
    _require(publication != binding, "REFRESH_RECEIPTS_NOT_DISTINCT")
    return publication, binding


def enrich_material(
    result: Any,
    request: Any,
    bundle: Mapping[str, Any],
) -> dict[str, Any]:
    _validate_bundle(bundle)
    geometry, first_cell, denominator = _validate_geometry(result)
    cells = list(geometry["cells"])
    target_cell = first_cell
    if result.receipt.role_direction != pe.ROLE_REVERSE:
        target_cell = next((cell for cell in cells if cell["cell"] == "yes"), first_cell)
    material = dict(result.receipt.material())
    material["n9_world"] = _n9_world(material["n9_world"], request, bundle)
    effects = bundle["consumer_effects"]
    nonparent = effects["NONPARENT_APPRENTICESHIP_ENTRY"]
    conception = effects["CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY"]
    primary_consumer_id = (
        "NONPARENT_APPRENTICESHIP_ENTRY"
        if result.receipt.role_direction == pe.ROLE_REVERSE
        else "CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY"
    )
    primary_values = effects[primary_consumer_id]["values_read"]
    publication, binding = _refresh_receipts(bundle)
    material.update({
        "sc0_overlay": {
            "overlay_id": OVERLAY_ID,
            "grade": GRADE,
            "pinned_pe_contract": pe.CONTRACT_ID,
            "pinned_pe_role_direction": pe.ROLE_REVERSE,
            "applied_after_original_pe_exact_result": True,
            "source": "HQ298 SC0 fixture provider + original PE/C1 geometry",
        },
        "sc0_overlay_provenance": {
            "n9_world_values": "HQ298 SC0 ProviderA fixture world; TEST_FIXTURE_ONLY__SOURCEFREE__NOT_OPERATIVE_N9",
            "n10e_values_read": "original PE receipt consumer_exact_geometry; numerator/denominator copied from executed C1/N10E geometry",
            "n9_values_read": "HQ298 SC0 ProviderA values_read keys/digest; fixture keys only",
            "consumer_effects": "HQ298 SC0 generic consumers over the fixture world; not PE empirical consumer or actor state",
            "clocks": "fixture SC0 time axes + PE request_time; actor_event is null and no actor authority is asserted",
            "refresh_receipts": "distinct H2 publication/binding generations over the fixture world; not production refresh",
        },
        "structural_publication_refresh_receipt": publication,
        "generated_binding_refresh_receipt": binding,
        "n9_values_read_receipt": {
            "consumer_id": primary_consumer_id,
            "provider_id": primary_values["provider_id"],
            "provider_grade": GRADE,
            "exact_owner_value_refs": list(primary_values["keys"]),
            "values_digest": primary_values["digest"],
            "n9_snapshot_ref": request.n9_world.n9_snapshot_ref.as_dict(),
            "n9_asof_ref": request.n9_world.n9_asof_ref.as_dict(),
        },
        "n10e_values_read_receipt": {
            "provider": "original PE receipt consumer_exact_geometry / C1_N10E",
            "exact_numerator_and_denominator": {
                "cell": target_cell["cell"],
                "numerator": target_cell["raw_numerator_support"],
                "denominator": denominator,
                "cells": copy.deepcopy(cells),
                "denominator_record": copy.deepcopy(geometry["denominator"]),
            },
            "condition_ids": list(result.receipt.conditioner_ids),
            "role_direction": result.receipt.role_direction,
        },
        "consumer_effect": {
            consumer_id: copy.deepcopy(effects[consumer_id])
            for consumer_id in REQUIRED_CONSUMERS
        },
        "generic_consumers": {
            "NONPARENT_APPRENTICESHIP_ENTRY": {
                "route_constraints": copy.deepcopy(nonparent["output"]["apprenticeship_access_routes"]),
                "values_read": copy.deepcopy(nonparent["values_read"]),
                "restrictions": list(nonparent["restrictions"]),
                "no_generated_person": nonparent["person_generation"] == "NONE",
            },
            "CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY": {
                "proposed_constraints": copy.deepcopy(conception["output"]["eligible_scenario_constraints"]),
                "values_read": copy.deepcopy(conception["values_read"]),
                "restrictions": list(conception["restrictions"]),
                "no_parent_actor_created": conception["person_generation"] == "NONE",
            },
        },
    })
    _require(material["n9_world"]["binding_echo"]["may_use_as_source_observation"] is False,
             "BINDING_ECHO_SOURCE_PROMOTION")
    _require(material["generic_consumers"]["NONPARENT_APPRENTICESHIP_ENTRY"]["no_generated_person"] is True,
             "NONPARENT_PERSON_GENERATION_FORBIDDEN")
    _require(material["generic_consumers"]["CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY"]["no_parent_actor_created"] is True,
             "CONCEPTION_PARENT_ACTOR_FORBIDDEN")
    return material


class EnrichedReceipt:
    def __init__(self, original: Any, material: Mapping[str, Any]):
        object.__setattr__(self, "_original", original)
        object.__setattr__(self, "_material", copy.deepcopy(material))

    def __getattr__(self, name: str) -> Any:
        return getattr(self._original, name)

    def material(self) -> dict[str, Any]:
        return copy.deepcopy(self._material)

    @property
    def receipt_hash(self) -> str:
        return semantic_hash(self._material)

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            "POSTASTRA_PE_SC0_ENRICHED_RECEIPT@1",
            f"urn:test:postastra-pe:sc0-enriched:{self.receipt_hash}",
            self.receipt_hash,
        )


class EnrichedResult:
    def __init__(self, original: Any, receipt: EnrichedReceipt):
        object.__setattr__(self, "_original", original)
        object.__setattr__(self, "receipt", receipt)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._original, name)

    def __repr__(self) -> str:
        return repr(self._original)


def _competent(registry: Any, ref: Any, *, target_ref: Any, denominator_basis_ref: Any) -> bool:
    try:
        snapshot = registry.require(
            ref,
            authority_kind="TARGET_USE_PERMISSION",
            operation=pe.ROLE_REVERSE,
            target_use_ref=target_ref,
            predicate_or_risk_set_ref=denominator_basis_ref,
        )
    except Exception:
        return False
    return (
        getattr(snapshot, "typed_state", None) == "ALLOW"
        and getattr(snapshot, "decision_state", None) == "ALLOW"
        and pe.ROLE_REVERSE in getattr(snapshot, "governed_operations", ())
        and pe.CONTRACT_ID in getattr(snapshot, "governed_object_families", ())
    )


def serve(*args: Any, **kwargs: Any) -> Any:
    request = kwargs.get("request")
    registry = kwargs.get("authority_registry")
    model_rule = kwargs.get("model_rule")
    if request is not None and request.role_direction == pe.ROLE_REVERSE:
        ref = request.role_reversal_authority_ref
        if ref is None or not _competent(
            registry,
            ref,
            target_ref=request.target_ref,
            denominator_basis_ref=request.denominator_basis_ref,
        ):
            return pe._refusal(
                request=request,
                model_rule=model_rule,
                inference_lane=pe.LANE_WORLD_ONLY,
                refusal_state=pe.REFUSAL_REVERSED_UNAUTHORIZED_ROLE,
                refusal_reason=(
                    "REVERSE_DIRECTION_REQUIRES_POSITIVELY_SCOPED_ROLE_REVERSAL_AUTHORITY__"
                    "P_A_GIVEN_D_IS_NOT_P_D_GIVEN_A__EXACT_ISSUER_DEREFERENCE_REQUIRED"
                ),
            )
    result = pe._original_serve(*args, **kwargs)
    if result.result_state != "EXACT_SUPPORTED":
        return result
    bundle = fixture_bundle()
    material = enrich_material(result, request, bundle)
    return EnrichedResult(result, EnrichedReceipt(result.receipt, material))


def install() -> None:
    if not hasattr(pe, "_original_serve"):
        pe._original_serve = pe.serve_generic_world_situated_possibility
    pe.serve_generic_world_situated_possibility = serve
