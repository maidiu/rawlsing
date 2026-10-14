"""Provider A — single tagged object-map (tuple-store) physical encoding.

Construction and serialization code is deliberately independent of provider B.
Semantic content is the shared baseline world; physical lineage differs.
"""
from __future__ import annotations

import copy
from typing import Any, Mapping

from port.contracts import (
    GradePromotionError,
    PermissionDenied,
    PortContractError,
    ReversalHeld,
    SemanticLossError,
    semantic_digest,
)
from port.world_baseline import (
    BASELINE_WORLD,
    CONSUMER_SPECS,
    EMPIRICAL,
    REVERSAL_GRANT_SCOPED,
)

PROVIDER_ID_A = "fx:A:tuple-store"
STAGE_ONE = "stage_one"
STAGE_TWO = "stage_two"


class ProviderA:
    """Single tagged object map; rows are tuples serialized as lists."""

    def __init__(self, world: Mapping[str, Any] | None = None, empirical: Mapping[str, Any] | None = None):
        base = copy.deepcopy(dict(world if world is not None else BASELINE_WORLD))
        emp = copy.deepcopy(dict(empirical if empirical is not None else EMPIRICAL))
        self._store: dict[str, Any] = {
            STAGE_ONE: {
                "world_header": {
                    "semantic_world_id": base["semantic_world_id"],
                    "source_ref": base["source_ref"],
                    "source_release_ref": base["source_release_ref"],
                    "epistemic_grade": base["epistemic_grade"],
                    "authority_ref": base["authority_ref"],
                    "clock_mode": base["clock_mode"],
                },
                "time_axes": dict(base["time_axes"]),
                "native": {
                    "unit": base["native_unit"],
                    "strata": list(base["native_strata"]),
                    "ah": base["absolute_horizon"],
                },
                "permission_ceiling": dict(base["permission_ceiling"]),
            },
            STAGE_TWO: {
                "nary": copy.deepcopy(base["nary"]),
                "f2": copy.deepcopy(base["f2"]),
                "f1_refs": list(base["f1_refs"]),
                "f2_requirement_ref": base["f2_requirement_ref"],
                "public_categories": list(base["public_categories"]),
                "public_sanctions": list(base["public_sanctions"]),
                "contradictory_alternatives": copy.deepcopy(base["contradictory_alternatives"]),
                "support": dict(base["support"]),
                "negative_states": copy.deepcopy(base["negative_states"]),
                "routes": copy.deepcopy(base["routes"]),
                "values": copy.deepcopy(base["values"]),
                "generated_binding_echo": copy.deepcopy(base["generated_binding_echo"]),
                "empirical": copy.deepcopy(emp),
            },
        }
        self._rows: list[tuple[str, Any]] = []
        for key in sorted(self._store[STAGE_TWO]["values"]):
            self._rows.append((key, self._store[STAGE_TWO]["values"][key]))
        self._state: dict[str, Any] = {
            "binding_generation": 0,
            "publication_generation": 0,
            "receipts": [],
        }

    # -- identity -----------------------------------------------------------
    @property
    def provider_id(self) -> str:
        return PROVIDER_ID_A

    @property
    def physical_lineage(self) -> dict[str, Any]:
        return {
            "physical_provider_id": PROVIDER_ID_A,
            "physical_storage_locator": "bundle://A/single-tagged-object-map",
            "physical_serialization": "single tagged object map",
            "physical_lineage_blob": "phys-A",
            "nonsemantic_cache_ids": ["cache-A-0"],
            "stage_names": [STAGE_ONE, STAGE_TWO],
        }

    # -- world selection (contract 1) --------------------------------------
    def resolve_world_selection(self, demand: Mapping[str, Any]) -> dict[str, Any]:
        stage1 = self._store[STAGE_ONE]
        stage2 = self._store[STAGE_TWO]
        world = {
            "semantic_world_id": stage1["world_header"]["semantic_world_id"],
            "source_ref": stage1["world_header"]["source_ref"],
            "source_release_ref": stage1["world_header"]["source_release_ref"],
            "epistemic_grade": stage1["world_header"]["epistemic_grade"],
            "authority_ref": stage1["world_header"]["authority_ref"],
            "clock_mode": stage1["world_header"]["clock_mode"],
            "time_axes": dict(stage1["time_axes"]),
            "native_unit": stage1["native"]["unit"],
            "native_strata": list(stage1["native"]["strata"]),
            "absolute_horizon": stage1["native"]["ah"],
            "permission_ceiling": dict(stage1["permission_ceiling"]),
            "nary": copy.deepcopy(stage2["nary"]),
            "f2": copy.deepcopy(stage2["f2"]),
            "f1_refs": list(stage2["f1_refs"]),
            "f2_requirement_ref": stage2["f2_requirement_ref"],
            "public_categories": list(stage2["public_categories"]),
            "public_sanctions": list(stage2["public_sanctions"]),
            "contradictory_alternatives": copy.deepcopy(stage2["contradictory_alternatives"]),
            "support": dict(stage2["support"]),
            "negative_states": copy.deepcopy(stage2["negative_states"]),
            "routes": copy.deepcopy(stage2["routes"]),
            "values": copy.deepcopy(stage2["values"]),
            "generated_binding_echo": copy.deepcopy(stage2["generated_binding_echo"]),
        }
        selection = {
            "contract": "GENERIC_WORLD_SELECTION@1.0.0",
            "grade": "TEST_FIXTURE_ONLY__SOURCEFREE__NOT_OPERATIVE_N9__NOT_MODEL_USE",
            "provider": self.physical_lineage,
            "world": world,
            "empirical_hint": copy.deepcopy(stage2["empirical"]),
            "demand": dict(demand),
            "selection_state": "COMPLETE",
            "binding_generation": self._state["binding_generation"],
            "publication_generation": self._state["publication_generation"],
        }
        selection["selection_digest"] = semantic_digest(
            {k: v for k, v in selection.items() if k != "provider"}
        )
        self._state["receipts"].append(("world_selection", selection["selection_digest"]))
        return selection

    def read_values(self, selection: Mapping[str, Any], keys: list[str]) -> dict[str, Any]:
        # the selected value surface includes rules/AH/strata AND route objects
        values = {**selection["world"]["values"], **selection["world"]["routes"]}
        out: dict[str, Any] = {}
        for key in keys:
            if key not in values:
                raise PortContractError("REJECT_UNVERIFIABLE_CONSUMER_USE", f"value key absent: {key}")
            out[key] = copy.deepcopy(values[key])
        receipt = {
            "kind": "VALUES_READ",
            "provider_id": self.provider_id,
            "keys": list(keys),
            "values": out,
            "digest": semantic_digest(out),
        }
        return receipt

    # -- ordered possibility (contract 2) ----------------------------------
    def ordered_possibility(self, selection: Mapping[str, Any], demand: Mapping[str, Any]) -> dict[str, Any]:
        emp = selection["empirical_hint"]
        if demand.get("temporal_operation") in ("LAG_INTERPOLATION", "INTERPOLATION"):
            raise PortContractError(
                "HELD_AUTHORITY",
                "temporal lag interpolation is not issued to this port",
            )
        if demand.get("sampling_unit") not in (None, emp["sampling_unit"]):
            raise PortContractError("REFUSE_SAMPLING_UNIT_JOINT", "cross-unit pooling refused")
        chain = sorted(emp["condition_chain"], key=lambda row: row["index"])
        if [row["index"] for row in chain] != list(range(len(chain))):
            raise PortContractError("REJECT_ORDERED_PATH_LOSS", "condition chain order damaged")
        receipt = {
            "contract": "GENERIC_ORDERED_POSSIBILITY@1.0.0",
            "universe": emp["universe"],
            "sampling_unit": emp["sampling_unit"],
            "release": emp["release"],
            "target": emp["target"],
            "direction": emp["direction"],
            "ordered_condition_chain": [dict(row) for row in chain],
            "support": dict(selection["world"]["support"]),
            "minority": emp["minority"],
            "routing": emp["routing"],
            "risk_set": emp["risk_set"],
            "weight": emp["weight"],
            "uncertainty": emp["uncertainty"],
            "model_use": emp["model_use"],
            "permission_ceiling": dict(selection["world"]["permission_ceiling"]),
            "walkback": dict(emp["walkback"]),
            "values_read": [],
        }
        receipt["replay_digest"] = semantic_digest(receipt)
        return receipt

    # -- role reversal ------------------------------------------------------
    def request_role_reversal(
        self,
        selection: Mapping[str, Any],
        possibility: Mapping[str, Any],
        grant: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        if grant is None:
            raise ReversalHeld("HELD_AUTHORITY", "no reversal issuer supplied")
        binds = grant.get("binds") or {}
        required = ("target", "risk_set", "denominator", "operation")
        missing = [k for k in required if k not in binds]
        if missing:
            raise ReversalHeld(
                "HELD_AUTHORITY",
                f"reversal grant does not bind competent reversed target/risk/denominator (missing {missing})",
            )
        if grant.get("issuer") != selection["world"]["authority_ref"]:
            raise ReversalHeld("HELD_AUTHORITY", "reversal issuer is not the competent scoped issuer")
        if binds["risk_set"] != possibility["risk_set"]:
            raise ReversalHeld("HELD_AUTHORITY", "reversal risk-set basis does not match request")
        if binds["denominator"] != possibility["support"]["denominator"]:
            raise ReversalHeld("HELD_AUTHORITY", "reversal denominator authority mismatch")
        if binds["operation"] != "ROLE_REVERSAL_CONDITIONAL_QUERY":
            raise ReversalHeld("HELD_AUTHORITY", "reversal operation not authorized")
        return {
            "state": "REVERSAL_PERMITTED_UNDER_SCOPED_GRANT",
            "grant_id": grant["grant_id"],
            "bound_target": binds["target"],
            "bound_risk_set": binds["risk_set"],
            "bound_denominator": binds["denominator"],
            "computed_from_forward": False,
        }

    # -- refresh channels (H2) ---------------------------------------------
    def refresh_binding_generation(self) -> dict[str, Any]:
        self._state["binding_generation"] += 1
        self._store[STAGE_TWO]["generated_binding_echo"] = {
            **self._store[STAGE_TWO]["generated_binding_echo"],
            "caller_fact": f"location-binding-echo-{self._state['binding_generation']}",
        }
        return {"channel": "H2_GENERATED_BINDING_REFRESH", "generation": self._state["binding_generation"]}

    def refresh_publication_generation(self) -> dict[str, Any]:
        self._state["publication_generation"] += 1
        return {"channel": "H2_PUBLICATION_BOUNDARY_REFRESH", "generation": self._state["publication_generation"]}

    def revoked_use(self, selection: Mapping[str, Any], atom: str) -> dict[str, Any]:
        # authority is THIS provider's ceiling; a cached foreign selection cannot bypass
        own = self._store["stage_one"]["permission_ceiling"]
        ceiling = own
        if atom in ceiling.get("revoked_atoms", []) or atom not in ceiling.get("use_atoms", []):
            raise PermissionDenied("DENIED_USE", f"use atom not permitted: {atom}")
        return {"state": "PERMITTED", "atom": atom}


def build_provider_a() -> ProviderA:
    return ProviderA()
