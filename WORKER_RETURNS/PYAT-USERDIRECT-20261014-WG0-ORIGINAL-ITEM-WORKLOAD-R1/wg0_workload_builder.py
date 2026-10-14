"""PYAT WG0 -- Source-free generic item-to-workload producer.

Mechanically enumerates original item instances and independently authorized
operations into reproducible C11/I03/I05/batch manifests. Source-free only.
No raw survey execution, no canonical changes, no V3.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class Disposition(str, Enum):
    PRODUCED = "PRODUCED"
    HELD = "HELD"
    INADMISSIBLE = "INADMISSIBLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNDECIDED = "UNDECIDED"


class ResponseKind(str, Enum):
    ORDINAL = "ORDINAL"
    MULTIPLE_RESPONSE = "MULTIPLE_RESPONSE"
    ROUTED = "ROUTED"
    HOUSEHOLD = "HOUSEHOLD"
    OPEN = "OPEN"


@dataclass(frozen=True)
class NativeItem:
    item_id: str
    source_id: str
    wave: str
    response_kind: ResponseKind
    options: tuple[str, ...]
    missing_codes: tuple[str, ...]
    route_condition: Optional[str]
    unit: str  # "respondent" or "household"
    version: str
    population: str


@dataclass(frozen=True)
class OperationCandidate:
    op_id: str
    item_ids: tuple[str, ...]
    op_class: str
    target: str
    conditioners: tuple[str, ...]
    authority_ref: str
    risk_set_ref: str


@dataclass
class WorkloadManifest:
    items: list[NativeItem] = field(default_factory=list)
    operations: list[OperationCandidate] = field(default_factory=list)
    dispositions: dict[str, Disposition] = field(default_factory=dict)
    frontier_frozen: bool = False
    content_hash: str = ""

    def freeze(self) -> str:
        self.frontier_frozen = True
        material = {
            "items": [vars(i) for i in self.items],
            "operations": [vars(o) for o in self.operations],
            "dispositions": {k: v.value for k, v in self.dispositions.items()},
        }
        self.content_hash = hashlib.sha256(
            json.dumps(material, sort_keys=True, default=str).encode()
        ).hexdigest()
        return self.content_hash


def _hash(data: Any) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()


class WorkloadBuilder:
    """Source-free generic builder for item-to-workload manifests."""

    def __init__(self) -> None:
        self.manifest = WorkloadManifest()

    def add_item(self, item: NativeItem) -> str:
        if self.manifest.frontier_frozen:
            return "FRONTIER_FROZEN"
        if any(i.item_id == item.item_id for i in self.manifest.items):
            return "DUPLICATE_ITEM_ID"
        self.manifest.items.append(item)
        return "OK"

    def add_operation(self, op: OperationCandidate) -> str:
        if self.manifest.frontier_frozen:
            return "FRONTIER_FROZEN"
        if any(o.op_id == op.op_id for o in self.manifest.operations):
            return "DUPLICATE_OP_ID"
        self.manifest.operations.append(op)
        return "OK"

    def enumerate_operations(self, operation_classes: list[str]) -> list[OperationCandidate]:
        """Mechanically enumerate eligible operations from items."""
        candidates = []
        for item in self.manifest.items:
            for op_class in operation_classes:
                if op_class == "MARGINAL_DISTRIBUTION":
                    candidates.append(OperationCandidate(
                        op_id=f"OP-{item.item_id}-MARGINAL",
                        item_ids=(item.item_id,),
                        op_class=op_class,
                        target=item.item_id,
                        conditioners=(),
                        authority_ref="SOURCEFREE_FIXTURE",
                        risk_set_ref=f"RISK-{item.source_id}-{item.wave}",
                    ))
                elif op_class == "CONDITIONAL_DISTRIBUTION":
                    for cond_item in self.manifest.items:
                        if cond_item.item_id != item.item_id and cond_item.unit == item.unit:
                            candidates.append(OperationCandidate(
                                op_id=f"OP-{item.item_id}-GIVEN-{cond_item.item_id}",
                                item_ids=(item.item_id, cond_item.item_id),
                                op_class=op_class,
                                target=item.item_id,
                                conditioners=(cond_item.item_id,),
                                authority_ref="SOURCEFREE_FIXTURE",
                                risk_set_ref=f"RISK-{item.source_id}-{item.wave}",
                            ))
        return candidates

    def disposition_all(self) -> dict[str, Disposition]:
        """Assign disposition to every item and operation."""
        for item in self.manifest.items:
            if not item.options:
                self.manifest.dispositions[item.item_id] = Disposition.HELD
            elif item.route_condition and not item.route_condition.strip():
                self.manifest.dispositions[item.item_id] = Disposition.NOT_APPLICABLE
            else:
                self.manifest.dispositions[item.item_id] = Disposition.PRODUCED
        for op in self.manifest.operations:
            if op.op_id not in self.manifest.dispositions:
                self.manifest.dispositions[op.op_id] = Disposition.PRODUCED
        return dict(self.manifest.dispositions)

    def no_drop_oracle(self) -> dict:
        """Independent oracle: every input item+op has exact disposition."""
        item_ids = {i.item_id for i in self.manifest.items}
        op_ids = {o.op_id for o in self.manifest.operations}
        disposition_ids = set(self.manifest.dispositions.keys())
        missing_items = item_ids - disposition_ids
        missing_ops = op_ids - disposition_ids
        return {
            "total_items": len(item_ids),
            "total_operations": len(op_ids),
            "total_dispositions": len(disposition_ids),
            "missing_items": sorted(missing_items),
            "missing_operations": sorted(missing_ops),
            "no_drop": len(missing_items) == 0 and len(missing_ops) == 0,
        }

    def shard(self, num_shards: int) -> list[list[str]]:
        """Deterministic sharding of operations."""
        op_ids = sorted(o.op_id for o in self.manifest.operations)
        shards = [[] for _ in range(num_shards)]
        for i, op_id in enumerate(op_ids):
            shards[i % num_shards].append(op_id)
        return shards

    def resume(self, completed_op_ids: set[str]) -> list[str]:
        """Return remaining operation IDs after resume."""
        return sorted(o.op_id for o in self.manifest.operations if o.op_id not in completed_op_ids)


def make_invented_items() -> list[NativeItem]:
    """Two heterogeneous invented fixture items with exact source-custody HOLD."""
    return [
        NativeItem(
            item_id="ITEM-ORDINAL-001",
            source_id="FIXTURE-SRC-A",
            wave="W1",
            response_kind=ResponseKind.ORDINAL,
            options=("0", "1", "2", "3", "9"),
            missing_codes=("9", "997", "998"),
            route_condition=None,
            unit="respondent",
            version="v1",
            population="adults_18plus",
        ),
        NativeItem(
            item_id="ITEM-HOUSEHOLD-MR-002",
            source_id="FIXTURE-SRC-B",
            wave="W2",
            response_kind=ResponseKind.HOUSEHOLD,
            options=("food", "rent", "health", "education", "none"),
            missing_codes=("997", "998"),
            route_condition="if_household_size > 0",
            unit="household",
            version="v2",
            population="households",
        ),
    ]
