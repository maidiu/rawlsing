"""R112 world-conditioned progressive successor (TEST_ONLY).

Reuses the original pinned nonparent.consume per empirical prefix over the same
selected world. Historical P41 owners remain read-only.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash


class WorldConditionedProgressiveError(ValueError):
    pass


@dataclass(frozen=True)
class WorldConditionedPrefix:
    prefix_id: str
    target: str
    conditioners: tuple[tuple[str, Any], ...]
    step: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not self.prefix_id or not self.target:
            raise WorldConditionedProgressiveError("PREFIX_IDENTITY_REQUIRED")


@dataclass(frozen=True)
class WorldConditionedPrefixResult:
    prefix_id: str
    target: str
    conditioners: tuple[tuple[str, Any], ...]
    n10e_consumer_hash: str
    world_snapshot_hash: str
    native_receipt_hash: str
    native_material: Mapping[str, Any]

    def material(self) -> Mapping[str, Any]:
        return {
            "prefix_id": self.prefix_id,
            "target": self.target,
            "conditioners": [
                [key, canonicalize(value)] for key, value in self.conditioners
            ],
            "n10e_consumer_hash": self.n10e_consumer_hash,
            "world_snapshot_hash": self.world_snapshot_hash,
            "native_receipt_hash": self.native_receipt_hash,
            "native_material": canonicalize(self.native_material),
        }


def _e05_read_date(value: Any) -> str:
    """E04 tested as-of dates must be canonical ISO dates."""
    from datetime import date
    if not isinstance(value, str):
        raise WorldConditionedProgressiveError("E05_EXACT_FIELD_CLOCK_REQUIRED")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise WorldConditionedProgressiveError("E05_EXACT_FIELD_CLOCK_REQUIRED") from exc
    if parsed.isoformat() != value:
        raise WorldConditionedProgressiveError("E05_EXACT_FIELD_CLOCK_REQUIRED")
    return value


def _verify_e05_field_read(snapshot: Any, key: str, value: Mapping[str, Any]) -> None:
    """Original E05 identity and clock checks at EXISTING R112 read boundary."""
    if value.get("state") != "SUPPORTED_TEST_ONLY":
        return
    material = snapshot.material
    if material.get("schema") != "E04_TEST_ONLY_SELECTED_WORLD_SNAPSHOT@1":
        raise WorldConditionedProgressiveError("E05_SELECTED_WORLD_SCHEMA_REQUIRED")
    payload = value.get("payload")
    if not isinstance(payload, Mapping) or payload.get("key") != key:
        raise WorldConditionedProgressiveError("E05_FIELD_PRODUCER_BINDING_MISMATCH")
    root = material.get("source_permission_root")
    if not root or payload.get("source_root") != root:
        raise WorldConditionedProgressiveError("E05_FIELD_PERMISSION_ROOT_MISMATCH")
    valid = _e05_read_date(material.get("valid_at"))
    start, end = (_e05_read_date(payload.get(name))
                  for name in ("effective_from", "effective_to"))
    if not start <= valid < end:
        raise WorldConditionedProgressiveError("E05_FIELD_EFFECTIVE_CLOCK_OUTSIDE_SELECTION")
    if _e05_read_date(payload.get("publication")) > _e05_read_date(material.get("published_asof")):
        raise WorldConditionedProgressiveError("E05_FIELD_PUBLICATION_AFTER_SELECTION")
    bound = material.get("fields", {}).get(key)
    if (not isinstance(bound, Mapping) or bound.get("state") != "SUPPORTED_TEST_ONLY"
            or bound.get("field_ref") != value.get("field_ref")):
        raise WorldConditionedProgressiveError("E05_SELECTED_FIELD_REF_MISMATCH")
    if (semantic_hash(payload) != value.get("payload_hash")
            or value.get("payload_hash") != bound.get("payload_hash")
            or value.get("value") != payload.get("value")
            or value.get("unit") != payload.get("unit")):
        raise WorldConditionedProgressiveError("E05_FIELD_PAYLOAD_HASH_MISMATCH")


class _PrefixBoundService:
    def __init__(self, catalog, snapshot, prefix: WorldConditionedPrefix):
        self.catalog = catalog
        self.snapshot = snapshot
        self.prefix = prefix
        self.value_reads: list[Mapping[str, Any]] = []

    def structural(self, snapshot, key, consumer):
        value = self.catalog.read(snapshot, key)
        _verify_e05_field_read(snapshot, key, value)
        self.value_reads.append({
            "consumer": consumer, "channel": "structural", "key": key,
            "state": value["state"], "value": value.get("value"),
            "field_ref": value.get("field_ref"),
            "snapshot_ref": snapshot.snapshot_hash,
        })
        return value

    def possibilities(self, snapshot, *, target="Y", conditions=(), consumer="GENERIC"):
        step = dict(self.prefix.step)
        self.value_reads.append({
            "consumer": consumer, "channel": "empirical",
            "state": step.get("state"), "denominator": step.get("denominator"),
            "cells": canonicalize(step.get("cells")),
            "evidence_ref": step.get("evidence_ref"),
            "snapshot_ref": snapshot.snapshot_hash,
            "n10e_consumer_hash": step.get("content_hash"),
        })
        return {
            "state": ("PRODUCTIVE_TEST_ONLY"
                      if step.get("state") == "EXACT_SUPPORTED"
                      else step.get("state")),
            "steps": [step],
            "dependencies": ["empirical"],
            "source_root": "R112_WORLD_CONDITIONED_SOURCE",
        }

    def _record(self, material):
        material = dict(material)
        material.update(
            service_contract="R112_WORLD_CONDITIONED_PREFIX_CONSUMER@1",
            grade="SOURCEFREE_TEST_ONLY",
            operative_N9=False,
            operative_N10W=False,
            new_issuer=False,
            actor_executions=0,
            model_calls=0,
        )
        digest = semantic_hash(material)
        return {"receipt_hash": digest, "material": material}


def _pinned_nonparent_consume():
    from rawlsing_next.sourcefree_world.nonparent import consume
    return consume


def consume_world_conditioned_prefixes(
    *,
    snapshot: Any,
    catalog: Any,
    prefixes: Sequence[WorldConditionedPrefix],
    budget_tokens: int = 5,
) -> tuple[WorldConditionedPrefixResult, ...]:
    if not prefixes:
        raise WorldConditionedProgressiveError("NONEMPTY_PREFIXES_REQUIRED")
    consume = _pinned_nonparent_consume()
    empirical = catalog.read(snapshot, "empirical")
    if empirical.get("state") == "SUPPORTED_TEST_ONLY":
        if (empirical != snapshot.material.get("empirical")
                or not snapshot.material.get("source_permission_root")
                or empirical.get("permission_root")
                   != snapshot.material.get("source_permission_root")):
            raise WorldConditionedProgressiveError("E05_EMPIRICAL_PERMISSION_ROOT_MISMATCH")
    if empirical.get("state") != "SUPPORTED_TEST_ONLY":
        return tuple(
            WorldConditionedPrefixResult(
                prefix_id=prefix.prefix_id, target=prefix.target,
                conditioners=prefix.conditioners,
                n10e_consumer_hash=str(prefix.step.get("content_hash")),
                world_snapshot_hash=snapshot.snapshot_hash,
                native_receipt_hash="",
                native_material={
                    "state": "EMPIRICAL_REVOKED_OR_UNAVAILABLE",
                    "structural_routes": {},
                    "source_balance_reads": [],
                    "route_probability": None,
                    "route_probability_reason": "NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL",
                    "typed_unavailable_reason": empirical.get("state"),
                },
            )
            for prefix in prefixes
        )
    results = []
    for prefix in prefixes:
        if prefix.step.get("state") != "EXACT_SUPPORTED":
            results.append(WorldConditionedPrefixResult(
                prefix_id=prefix.prefix_id, target=prefix.target,
                conditioners=prefix.conditioners,
                n10e_consumer_hash=str(prefix.step.get("content_hash")),
                world_snapshot_hash=snapshot.snapshot_hash,
                native_receipt_hash="",
                native_material={
                    "state": prefix.step.get("state"),
                    "structural_routes": {},
                    "source_balance_reads": [],
                    "route_probability": None,
                    "route_probability_reason": "NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL",
                    "typed_unavailable_reason": "PREFIX_NOT_EXACT_SUPPORTED",
                },
            ))
            continue
        service = _PrefixBoundService(catalog, snapshot, prefix)
        result = consume(service, snapshot, budget_tokens=budget_tokens)
        material = result["material"]
        if material.get("empirical", {}).get("steps"):
            step = material["empirical"]["steps"][0]
            if step.get("content_hash") != prefix.step.get("content_hash"):
                raise WorldConditionedProgressiveError("N10E_CONSUMER_BINDING_MISMATCH")
        results.append(WorldConditionedPrefixResult(
            prefix_id=prefix.prefix_id, target=prefix.target,
            conditioners=prefix.conditioners,
            n10e_consumer_hash=str(prefix.step.get("content_hash")),
            world_snapshot_hash=snapshot.snapshot_hash,
            native_receipt_hash=result["receipt_hash"],
            native_material=material,
        ))
    return tuple(results)


__all__ = [
    "WorldConditionedProgressiveError", "WorldConditionedPrefix",
    "WorldConditionedPrefixResult", "consume_world_conditioned_prefixes",
]
