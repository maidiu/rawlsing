"""Bounded sourcefree repair for the S3 selected-world numeric seam.

This is an explicit bounded alternative, not the original S3 module. It binds
the selected world contract to the exact source-owned synthetic numeric cells.
Changing the cells requires a new contract; mutating saved channels while
retaining the old contract is refused. No original N9 world, source value,
scientific rule, actor state or production adoption is claimed.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
import hashlib
import json
from typing import Any, Mapping

CONTRACT_ID = "RRIF_SELECTED_WORLD_NUMERIC_REPAIR@1.0.0"
SCOPE = "SOURCEFREE_SYNTHETIC_ONLY__NOT_ORIGINAL_N9"


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _cells_material(cells: Mapping[tuple[int, int], int]) -> list[list[int]]:
    return [[x, y, int(cells[(x, y)])] for x in (0, 1) for y in (0, 1)]


@dataclass(frozen=True)
class SelectedWorldContract:
    contract_id: str
    world_tag: str
    source_universe_ref: str
    risk_set_ref: str
    cells: tuple[tuple[int, int, int], ...]
    scope: str = SCOPE

    @property
    def contract_hash(self) -> str:
        return _hash({
            "contract_id": self.contract_id,
            "world_tag": self.world_tag,
            "source_universe_ref": self.source_universe_ref,
            "risk_set_ref": self.risk_set_ref,
            "cells": [list(cell) for cell in self.cells],
            "scope": self.scope,
        })

    def as_dict(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "world_tag": self.world_tag,
            "source_universe_ref": self.source_universe_ref,
            "risk_set_ref": self.risk_set_ref,
            "cells": [list(cell) for cell in self.cells],
            "scope": self.scope,
            "contract_hash": self.contract_hash,
        }


@dataclass(frozen=True)
class SourceOwnedJointWorld:
    contract: SelectedWorldContract
    channels: tuple[Mapping[str, Any], ...]
    conditions: tuple[Mapping[str, Any], ...]
    steps: tuple[Mapping[str, Any], ...]
    content_hash: str

    def as_dict(self, *, include_content_hash: bool = True) -> dict[str, Any]:
        body = {
            "contract": self.contract.as_dict(),
            "channels": [dict(channel) for channel in self.channels],
            "conditions": [dict(condition) for condition in self.conditions],
            "steps": [dict(step) for step in self.steps],
            "scope": SCOPE,
        }
        if include_content_hash:
            body["content_hash"] = self.content_hash
        return body


def _cell_map(contract: SelectedWorldContract) -> dict[tuple[int, int], int]:
    return {(x, y): n for x, y, n in contract.cells}


def build_source_owned_joint(
    cells: Mapping[tuple[int, int], int],
    *,
    world_tag: str = "rrif-selected-world-2x2",
) -> SourceOwnedJointWorld:
    expected = {(0, 0), (0, 1), (1, 0), (1, 1)}
    if set(cells) != expected or any(type(v) is not int or v < 0 for v in cells.values()):
        raise ValueError("EXACT_NONNEGATIVE_2X2_REQUIRED")
    material = {"tag": world_tag, "cells": _cells_material(cells)}
    digest = _hash(material)
    contract = SelectedWorldContract(
        contract_id=CONTRACT_ID,
        world_tag=world_tag,
        source_universe_ref=f"urn:test:rrif:selected-world:source:{digest}",
        risk_set_ref=f"urn:test:rrif:selected-world:risk:{digest}",
        cells=tuple((x, y, cells[(x, y)]) for x in (0, 1) for y in (0, 1)),
    )
    return _from_contract(contract)


def rebind_source_owned_joint(
    world: SourceOwnedJointWorld,
    cells: Mapping[tuple[int, int], int],
) -> SourceOwnedJointWorld:
    return build_source_owned_joint(cells, world_tag=world.contract.world_tag)


def _from_contract(contract: SelectedWorldContract) -> SourceOwnedJointWorld:
    cells = _cell_map(contract)
    channels: list[Mapping[str, Any]] = []
    conditions: list[Mapping[str, Any]] = []
    steps: list[Mapping[str, Any]] = []
    for conditioner in (0, 1):
        step_id = f"P_Q86A_given_Q86B_{conditioner}"
        denominator = cells[(conditioner, 0)] + cells[(conditioner, 1)]
        for outcome in (0, 1):
            numerator = cells[(conditioner, outcome)]
            fraction = None
            if denominator:
                value = Fraction(numerator, denominator)
                fraction = {"$exact_fraction": [value.numerator, value.denominator]}
            channels.append({
                "channel_id": f"CH_{step_id}_{outcome}",
                "step_id": step_id,
                "conditioners": [["Q86B", str(conditioner)]],
                "cell": str(outcome),
                "raw_numerator_support": numerator,
                "raw_probability_exact_fraction": fraction,
                "support": denominator,
                "source_scope": SCOPE,
                "test_origin": True,
            })
        conditions.append({
            "step_id": step_id,
            "conditioners": [["Q86B", str(conditioner)]],
            "denominator": denominator,
            "risk_set_ref": contract.risk_set_ref,
        })
        steps.append({
            "step_id": step_id,
            "conditioners": [["Q86B", str(conditioner)]],
            "cells": {
                str(outcome): {
                    "numerator": cells[(conditioner, outcome)],
                    "fraction": None if not denominator else {
                        "$exact_fraction": [
                            Fraction(cells[(conditioner, outcome)], denominator).numerator,
                            Fraction(cells[(conditioner, outcome)], denominator).denominator,
                        ]
                    },
                }
                for outcome in (0, 1)
            },
            "denominator": denominator,
        })
    body = {
        "contract": contract.as_dict(),
        "channels": channels,
        "conditions": conditions,
        "steps": steps,
        "scope": SCOPE,
    }
    return SourceOwnedJointWorld(
        contract=contract,
        channels=tuple(channels),
        conditions=tuple(conditions),
        steps=tuple(steps),
        content_hash=_hash(body),
    )


def _refuse(reason: str, *, status: str = "REFUSED") -> dict[str, Any]:
    return {"status": status, "reason": reason, "scope": SCOPE}


def _validate_world(world: SourceOwnedJointWorld) -> str | None:
    body = world.as_dict(include_content_hash=False)
    if _hash(body) != world.content_hash:
        return "BUNDLE_CONTENT_HASH_MISMATCH"
    if len(world.contract.cells) != 4:
        return "SELECTED_WORLD_CONTRACT_DOMAIN_MISMATCH"
    expected = {(x, y): n for x, y, n in world.contract.cells}
    saved = {}
    for channel in world.channels:
        key = (int(channel["conditioners"][0][1]), int(channel["cell"]))
        saved[key] = int(channel["raw_numerator_support"])
    if saved != expected:
        return "SOURCE_VALUE_CONTRACT_MISMATCH"
    if any(channel.get("source_scope") != SCOPE or channel.get("test_origin") is not True
           for channel in world.channels):
        return "SOURCE_SCOPE_OR_VALUE_ORIGIN_MISMATCH"
    for step in world.steps:
        cells = step["cells"]
        if set(cells) != {"0", "1"}:
            return "INCOMPLETE_PRODUCER_CELL_DOMAIN"
        if any(int(cells[k]["numerator"]) < 0 for k in cells):
            return "INVALID_RAW_NUMERATOR"
    return None


def read_selected_world(
    world: SourceOwnedJointWorld,
    step_id: str,
) -> dict[str, Any]:
    issue = _validate_world(world)
    if issue:
        return _refuse(issue)
    condition = next((c for c in world.conditions if c["step_id"] == step_id), None)
    if condition is None:
        return _refuse("NO_MATCHING_CHANNEL", status="NO_SUPPORT")
    channels = [c for c in world.channels if c["step_id"] == step_id]
    denominator = int(condition["denominator"])
    if denominator == 0:
        return _refuse("ZERO_DENOMINATOR_ABSTENTION", status="ZERO_SUPPORT")
    numerators = {c["cell"]: int(c["raw_numerator_support"]) for c in channels}
    if any(int(c["support"]) != denominator for c in channels):
        return _refuse("SOURCE_COUNT_CLOSURE_MISMATCH")
    probabilities = {}
    for cell, numerator in numerators.items():
        value = Fraction(numerator, denominator)
        probabilities[cell] = {"$exact_fraction": [value.numerator, value.denominator]}
    dependency = {
        "contract_hash": world.contract.contract_hash,
        "used_input_refs": [
            {"channel_id": c["channel_id"], "value_hash": _hash(dict(c))}
            for c in channels
        ],
    }
    return {
        "status": "COMPUTED",
        "step_id": step_id,
        "raw_denominator_support": denominator,
        "raw_numerators": numerators,
        "exact_probabilities": probabilities,
        "source_value_dependency": dependency,
        "scope": SCOPE,
    }


def stale_mutation_with_old_contract(
    world: SourceOwnedJointWorld,
    new_cells: Mapping[tuple[int, int], int],
) -> SourceOwnedJointWorld:
    updated = build_source_owned_joint(new_cells, world_tag=world.contract.world_tag)
    channels = tuple(dict(channel) for channel in updated.channels)
    body = {
        "contract": world.contract.as_dict(),
        "channels": [dict(c) for c in channels],
        "conditions": [dict(c) for c in updated.conditions],
        "steps": [dict(s) for s in updated.steps],
        "scope": SCOPE,
    }
    return SourceOwnedJointWorld(
        contract=world.contract,
        channels=channels,
        conditions=updated.conditions,
        steps=updated.steps,
        content_hash=_hash(body),
    )


def cold_restore(world: SourceOwnedJointWorld, payload: str | Mapping[str, Any]) -> SourceOwnedJointWorld:
    material = json.loads(payload) if isinstance(payload, str) else dict(payload)
    contract = material.get("contract") or {}
    contract_cells = tuple(tuple(int(v) for v in row) for row in contract.get("cells", []))
    restored_contract = SelectedWorldContract(
        contract_id=contract["contract_id"],
        world_tag=contract["world_tag"],
        source_universe_ref=contract["source_universe_ref"],
        risk_set_ref=contract["risk_set_ref"],
        cells=contract_cells,
        scope=contract.get("scope", SCOPE),
    )
    if restored_contract.contract_hash != contract.get("contract_hash"):
        raise ValueError("RESTORED_CONTRACT_HASH_MISMATCH")
    channels = tuple(dict(c) for c in material.get("channels", []))
    conditions = tuple(dict(c) for c in material.get("conditions", []))
    steps = tuple(dict(s) for s in material.get("steps", []))
    body = {
        "contract": restored_contract.as_dict(),
        "channels": channels,
        "conditions": conditions,
        "steps": steps,
        "scope": material.get("scope", SCOPE),
    }
    restored = SourceOwnedJointWorld(
        contract=restored_contract,
        channels=channels,
        conditions=conditions,
        steps=steps,
        content_hash=material.get("content_hash", ""),
    )
    if restored.content_hash != _hash(body):
        raise ValueError("RESTORED_CONTENT_HASH_MISMATCH")
    if _validate_world(restored):
        raise ValueError("RESTORED_WORLD_INVALID")
    return restored
