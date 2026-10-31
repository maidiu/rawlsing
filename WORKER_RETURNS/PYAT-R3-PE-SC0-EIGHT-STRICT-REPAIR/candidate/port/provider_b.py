"""Provider B — normalized-multifile physical encoding (independent of provider A).

Separate construction path: normalized rows, split temporal / n-ary / value
tables, shuffled record order, renamed stage-shaped files (renamed_data,
join_index).  Semantically equivalent to provider A by construction target;
equivalence is proven by test, not assumed.
"""
from __future__ import annotations

import copy
import random
from typing import Any, Mapping

from port.contracts import (
    PermissionDenied,
    PortContractError,
    ReversalHeld,
    semantic_digest,
)
from port.world_baseline import BASELINE_WORLD, EMPIRICAL

PROVIDER_ID_B = "fx:B:normalized-multifile"
RENAME_MAP = {"stage_one": "renamed_data", "stage_two": "join_index"}


def _shuffle(rows: list[Any], seed: int) -> list[Any]:
    out = list(rows)
    random.Random(seed).shuffle(out)
    return out


class ProviderB:
    """Normalized rows with split temporal and n-ary tables."""

    def __init__(self, world: Mapping[str, Any] | None = None, empirical: Mapping[str, Any] | None = None, seed: int = 20261014):
        base = copy.deepcopy(dict(world if world is not None else BASELINE_WORLD))
        emp = copy.deepcopy(dict(empirical if empirical is not None else EMPIRICAL))
        self._seed = seed
        # normalized row tables (physical shape differs from A's tagged map)
        self._table_header = [
            {"row": 0, "col": "semantic_world_id", "val": base["semantic_world_id"]},
            {"row": 1, "col": "source_ref", "val": base["source_ref"]},
            {"row": 2, "col": "source_release_ref", "val": base["source_release_ref"]},
            {"row": 3, "col": "epistemic_grade", "val": base["epistemic_grade"]},
            {"row": 4, "col": "authority_ref", "val": base["authority_ref"]},
            {"row": 5, "col": "clock_mode", "val": base["clock_mode"]},
            {"row": 6, "col": "native_unit", "val": base["native_unit"]},
            {"row": 7, "col": "absolute_horizon", "val": base["absolute_horizon"]},
            {"row": 8, "col": "f2_requirement_ref", "val": base["f2_requirement_ref"]},
        ]
        self._table_temporal = [
            {"axis": axis, "val": val} for axis, val in sorted(base["time_axes"].items())
        ]
        self._table_nary = [
            {"rel": base["nary"]["id"], **p} for p in base["nary"]["participants"]
        ]
        self._table_values = [
            {"key": k, "val": v} for k, v in sorted(base["values"].items())
        ]
        self._table_struct = {
            "strata": list(base["native_strata"]),
            "nary_meta": {
                "id": base["nary"]["id"],
                "ordered": base["nary"]["ordered"],
                "cardinality": base["nary"]["cardinality"],
                "route_refs": list(base["nary"]["route_refs"]),
            },
            "f2": copy.deepcopy(base["f2"]),
            "f1_refs": list(base["f1_refs"]),
            "public_categories": list(base["public_categories"]),
            "public_sanctions": list(base["public_sanctions"]),
            "contradictory_alternatives": copy.deepcopy(base["contradictory_alternatives"]),
            "support": dict(base["support"]),
            "negative_states": copy.deepcopy(base["negative_states"]),
            "routes": copy.deepcopy(base["routes"]),
            "generated_binding_echo": copy.deepcopy(base["generated_binding_echo"]),
            "permission_ceiling": dict(base["permission_ceiling"]),
            "empirical": copy.deepcopy(emp),
        }
        self._state = {"binding_generation": 0, "publication_generation": 0}

    @property
    def provider_id(self) -> str:
        return PROVIDER_ID_B

    @property
    def physical_lineage(self) -> dict[str, Any]:
        return {
            "physical_provider_id": PROVIDER_ID_B,
            "physical_storage_locator": "bundle://B/normalized-multifile",
            "physical_serialization": "normalized rows with split temporal and n-ary tables",
            "physical_lineage_blob": "phys-B",
            "nonsemantic_cache_ids": ["cache-B-7", "cache-B-9"],
            "stage_names": [RENAME_MAP["stage_one"], RENAME_MAP["stage_two"]],
        }

    def resolve_world_selection(self, demand: Mapping[str, Any]) -> dict[str, Any]:
        header = {row["col"]: row["val"] for row in self._table_header}
        temporal = {row["axis"]: row["val"] for row in self._table_temporal}
        nary_meta = self._table_struct["nary_meta"]
        # shuffled participant rows reassembled by ordinal (order-preserving semantics)
        participants = _shuffle(self._table_nary, self._seed)
        participants = sorted(
            [{"role": p["role"], "ordinal": p["ordinal"], "ref": p["ref"]} for p in participants],
            key=lambda p: p["ordinal"],
        )
        values = {row["key"]: copy.deepcopy(row["val"]) for row in self._table_values}
        struct = self._table_struct
        world = {
            "semantic_world_id": header["semantic_world_id"],
            "source_ref": header["source_ref"],
            "source_release_ref": header["source_release_ref"],
            "epistemic_grade": header["epistemic_grade"],
            "authority_ref": header["authority_ref"],
            "clock_mode": header["clock_mode"],
            "time_axes": dict(temporal),
            "native_unit": header["native_unit"],
            "native_strata": list(struct["strata"]),
            "absolute_horizon": header["absolute_horizon"],
            "permission_ceiling": dict(struct["permission_ceiling"]),
            "nary": {
                "id": nary_meta["id"],
                "participants": participants,
                "ordered": nary_meta["ordered"],
                "cardinality": nary_meta["cardinality"],
                "route_refs": list(nary_meta["route_refs"]),
            },
            "f2": copy.deepcopy(struct["f2"]),
            "f1_refs": list(struct["f1_refs"]),
            "f2_requirement_ref": header["f2_requirement_ref"],
            "public_categories": list(struct["public_categories"]),
            "public_sanctions": list(struct["public_sanctions"]),
            "contradictory_alternatives": copy.deepcopy(struct["contradictory_alternatives"]),
            "support": dict(struct["support"]),
            "negative_states": copy.deepcopy(struct["negative_states"]),
            "routes": copy.deepcopy(struct["routes"]),
            "values": values,
            "generated_binding_echo": copy.deepcopy(struct["generated_binding_echo"]),
        }
        selection = {
            "contract": "GENERIC_WORLD_SELECTION@1.0.0",
            "grade": "TEST_FIXTURE_ONLY__SOURCEFREE__NOT_OPERATIVE_N9__NOT_MODEL_USE",
            "provider": self.physical_lineage,
            "world": world,
            "empirical_hint": copy.deepcopy(struct["empirical"]),
            "demand": dict(demand),
            "selection_state": "COMPLETE",
            "binding_generation": self._state["binding_generation"],
            "publication_generation": self._state["publication_generation"],
        }
        selection["selection_digest"] = semantic_digest(
            {k: v for k, v in selection.items() if k != "provider"}
        )
        return selection

    def read_values(self, selection: Mapping[str, Any], keys: list[str]) -> dict[str, Any]:
        # the selected value surface includes rules/AH/strata AND route objects
        values = {**selection["world"]["values"], **selection["world"]["routes"]}
        out: dict[str, Any] = {}
        for key in keys:
            if key not in values:
                raise PortContractError("REJECT_UNVERIFIABLE_CONSUMER_USE", f"value key absent: {key}")
            out[key] = copy.deepcopy(values[key])
        return {
            "kind": "VALUES_READ",
            "provider_id": self.provider_id,
            "keys": list(keys),
            "values": out,
            "digest": semantic_digest(out),
        }

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

    def refresh_binding_generation(self) -> dict[str, Any]:
        self._state["binding_generation"] += 1
        echo = self._table_struct["generated_binding_echo"]
        self._table_struct["generated_binding_echo"] = {
            **echo,
            "caller_fact": f"location-binding-echo-{self._state['binding_generation']}",
        }
        return {"channel": "H2_GENERATED_BINDING_REFRESH", "generation": self._state["binding_generation"]}

    def refresh_publication_generation(self) -> dict[str, Any]:
        self._state["publication_generation"] += 1
        return {"channel": "H2_PUBLICATION_BOUNDARY_REFRESH", "generation": self._state["publication_generation"]}

    def revoked_use(self, selection: Mapping[str, Any], atom: str) -> dict[str, Any]:
        # authority is THIS provider's ceiling; a cached foreign selection cannot bypass
        own = self._table_struct["permission_ceiling"]
        ceiling = own
        if atom in ceiling.get("revoked_atoms", []) or atom not in ceiling.get("use_atoms", []):
            raise PermissionDenied("DENIED_USE", f"use atom not permitted: {atom}")
        return {"state": "PERMITTED", "atom": atom}


def build_provider_b() -> ProviderB:
    return ProviderB()
