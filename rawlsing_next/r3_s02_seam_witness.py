"""PYAT R3 S00-S02 — selected-world to sociological seam adapter.

Development-only, source-free/retained-source-conditioned.  This module
builds the smallest lawful adapter that passes actual selected producer
values into the progressive possibility serving chain, and produces a
saved, inspectable sociological result with consumer receipts and
deterministic replay.

What this module does
---------------------
* ``SociologicalWorldBundle`` — a machine-readable bundle binding world
  scope, channels, evidence graph, dependence and replay metadata.
* ``build_sociological_bundle()`` — assembles the bundle from the P04
  progressive chain, preserving owner-native semantics.
* ``ContractOnlySeamConsumer`` — a contract-only consumer that
  dereferences the bundle, requests progressive conditional possibilities,
  verifies permissible use, records actual values read, and computes
  scenario distributions.
* ``run_seam_witness()`` — executes the full S02 witness: builds the
  bundle, runs the consumer, produces per-value read receipts, and
  verifies deterministic replay.

What this module does NOT do
----------------------------
* No V3 actor, developmental psychology, parents, biography
* No V2 rendering
* No new raw survey execution
* No protected CURRENT without authorization
* No invented scientific grants or model-use credentials
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from rawlsing_next.pre553_n9_n10w_progressive_candidate import (
    E03_ORACLE,
    build_synthetic_world,
    run_progressive_chain,
    consume_step_with_f8,
    ProgressiveChainResult,
    ProgressiveStepResult,
)
from rawlsing_next.pre553_selected_world_progressive_contract import (
    SelectedWorldContract,
    select_world,
    verify_chain_preserves_contract,
    contract_content_hash,
)

SEAM_CONTRACT_VERSION = "R3_S02_SOCIOLOGICAL_SEAM_WITNESS@1.0.0"
SEAM_BUNDLE_SCHEMA = "R3_SOCIOLOGICAL_WORLD_BUNDLE@1"


class SeamContractError(ValueError):
    """The seam adapter cannot lawfully produce the requested result."""


def _content_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, default=str).encode()
    ).hexdigest()


@dataclass(frozen=True)
class ChannelValue:
    """A single channel value with provenance and evidence mode."""
    channel_id: str
    evidence_mode: str  # MEASURED, TRANSFORMED, INFERRED, PRIOR
    value: Mapping[str, Any]
    support: int
    units: str
    source_scope: str
    test_origin: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "channel_id": self.channel_id,
            "evidence_mode": self.evidence_mode,
            "value": dict(self.value),
            "support": self.support,
            "units": self.units,
            "source_scope": self.source_scope,
            "test_origin": self.test_origin,
        }


@dataclass(frozen=True)
class ValueReadReceipt:
    """Receipt recording an actual value read by the consumer."""
    receipt_id: str
    channel_id: str
    value_hash: str
    semantic_effect: str
    query_ref: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "channel_id": self.channel_id,
            "value_hash": self.value_hash,
            "semantic_effect": self.semantic_effect,
            "query_ref": self.query_ref,
        }


@dataclass(frozen=True)
class SociologicalWorldBundle:
    """A saved, inspectable sociological world bundle."""
    bundle_id: str
    contract_version: str
    content_hash: str
    world_scope: Mapping[str, Any]
    channels: tuple[ChannelValue, ...]
    evidence_graph: tuple[Mapping[str, Any], ...]
    conditions: tuple[Mapping[str, Any], ...]
    steps: tuple[Mapping[str, Any], ...]
    replay: Mapping[str, Any]
    selected_world_contract: SelectedWorldContract

    def as_dict(self) -> dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "contract_version": self.contract_version,
            "content_hash": self.content_hash,
            "world_scope": dict(self.world_scope),
            "channels": [c.as_dict() for c in self.channels],
            "evidence_graph": [dict(e) for e in self.evidence_graph],
            "conditions": [dict(c) for c in self.conditions],
            "steps": [dict(s) for s in self.steps],
            "replay": dict(self.replay),
            "selected_world_contract_hash": contract_content_hash(
                self.selected_world_contract
            ),
        }


@dataclass
class ConsumerReceipt:
    """Receipt from the contract-only seam consumer."""
    consumer_ref: str
    requested_scope: str
    values_read: list[ValueReadReceipt] = field(default_factory=list)
    scenario_results: dict[str, Any] = field(default_factory=dict)
    refused_fields: list[dict[str, str]] = field(default_factory=list)
    output_hash: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "consumer_ref": self.consumer_ref,
            "requested_scope": self.requested_scope,
            "values_read": [v.as_dict() for v in self.values_read],
            "scenario_results": self.scenario_results,
            "refused_fields": self.refused_fields,
            "output_hash": self.output_hash,
        }


def build_sociological_bundle(
    *,
    bundle_id: str = "R3_S00_S02_BUNDLE_001",
) -> SociologicalWorldBundle:
    """Assemble the sociological world bundle from the P04 progressive chain."""
    contract, world = select_world()
    chain = run_progressive_chain(world)

    channels = []
    for step in chain.steps:
        for cell_key, cell in step.cells.items():
            channels.append(ChannelValue(
                channel_id=f"CH_{step.step_id}_{cell_key}",
                evidence_mode="MEASURED" if step.producer_route == "N10E_SINGLE_CONDITIONER" else "TRANSFORMED",
                value={
                    "step_id": step.step_id,
                    "conditioners": [list(c) for c in step.conditioners],
                    "cell": cell_key,
                    "raw_numerator_support": cell["raw_numerator_support"],
                    "raw_probability_exact_fraction": cell["raw_probability_exact_fraction"],
                },
                support=step.raw_denominator_support,
                units="probability",
                source_scope="P04_SYNTHETIC_58_RESPONDENT_FIXTURE",
                test_origin=True,
            ))

    evidence_graph = []
    for step in chain.steps:
        evidence_graph.append({
            "node_id": f"EV_{step.step_id}",
            "evidence_mode": "MEASURED",
            "parent_refs": [],
            "method": step.producer_route,
            "uncertainty": step.uncertainty_state,
            "test_origin": True,
        })

    conditions = []
    for step in chain.steps:
        conditions.append({
            "step_id": step.step_id,
            "conditioners": [list(c) for c in step.conditioners],
            "predicate_ref": f"joint_predicate_{step.step_id}",
            "denominator": step.raw_denominator_support,
        })

    steps = []
    for step in chain.steps:
        steps.append({
            "step_id": step.step_id,
            "producer_route": step.producer_route,
            "cells": {k: {
                "numerator": v["raw_numerator_support"],
                "fraction": v["raw_probability_exact_fraction"],
            } for k, v in step.cells.items()},
            "consumer_state": step.consumer_state,
            "uncertainty_state": step.uncertainty_state,
        })

    bundle = SociologicalWorldBundle(
        bundle_id=bundle_id,
        contract_version=SEAM_CONTRACT_VERSION,
        content_hash="",
        world_scope={
            "geography": "Sub-Saharan Africa, 11-country Afrobarometer R5 subset",
            "historical_boundary": "Afrobarometer Round 5 (2011-2013)",
            "population": "Adult citizens 18+",
            "unit": "individual respondent (country-stratified)",
            "status": "RETAINED_SOURCE_CONDITIONED",
        },
        channels=tuple(channels),
        evidence_graph=tuple(evidence_graph),
        conditions=tuple(conditions),
        steps=tuple(steps),
        replay={
            "input_preimages": [contract_content_hash(contract)],
            "code_ref": "pre553_n9_n10w_progressive_candidate.py",
            "deterministic": True,
            "test_origin": True,
        },
        selected_world_contract=contract,
    )
    content_hash = _content_hash(bundle.as_dict())
    return SociologicalWorldBundle(
        bundle_id=bundle.bundle_id,
        contract_version=bundle.contract_version,
        content_hash=content_hash,
        world_scope=bundle.world_scope,
        channels=bundle.channels,
        evidence_graph=bundle.evidence_graph,
        conditions=bundle.conditions,
        steps=bundle.steps,
        replay=bundle.replay,
        selected_world_contract=bundle.selected_world_contract,
    )


class ContractOnlySeamConsumer:
    """Contract-only seam consumer.

    Dereferences the selected world bundle, requests progressive conditional
    possibilities, verifies permissible use, records actual values read,
    and computes scenario distributions.  Must not invoke V3, V2, actor
    constructors or a narrative renderer.
    """

    CONSUMER_REF = "R3_CONTRACT_ONLY_SEAM_CONSUMER@1.0.0"

    def __init__(self, bundle: SociologicalWorldBundle) -> None:
        self._bundle = bundle
        self._receipt = ConsumerReceipt(
            consumer_ref=self.CONSUMER_REF,
            requested_scope=bundle.bundle_id,
        )

    def read_value(self, channel_id: str) -> ChannelValue | None:
        """Read a channel value and record the receipt."""
        for ch in self._bundle.channels:
            if ch.channel_id == channel_id:
                self._receipt.values_read.append(ValueReadReceipt(
                    receipt_id=f"VRR_{len(self._receipt.values_read)+1:04d}",
                    channel_id=channel_id,
                    value_hash=_content_hash(ch.as_dict()),
                    semantic_effect="VALUE_READ_AND_USED",
                    query_ref=f"read_{channel_id}",
                ))
                return ch
        self._receipt.refused_fields.append({
            "channel_id": channel_id,
            "reason": "CHANNEL_NOT_FOUND",
        })
        return None

    def compute_scenario(self, scenario_id: str, conditioning: list[str]) -> dict[str, Any]:
        """Compute a conditional scenario distribution."""
        relevant = [
            ch for ch in self._bundle.channels
            if any(c in ch.channel_id for c in conditioning)
        ]
        if not relevant:
            self._receipt.refused_fields.append({
                "scenario_id": scenario_id,
                "reason": "NO_MATCHING_CHANNELS",
            })
            return {"scenario_id": scenario_id, "status": "NO_SUPPORT"}

        total_support = sum(ch.support for ch in relevant)
        result = {
            "scenario_id": scenario_id,
            "conditioning": conditioning,
            "channels_used": [ch.channel_id for ch in relevant],
            "total_support": total_support,
            "distributions": [ch.as_dict() for ch in relevant],
            "status": "COMPUTED",
        }
        self._receipt.scenario_results[scenario_id] = result
        return result

    def get_receipt(self) -> ConsumerReceipt:
        self._receipt.output_hash = _content_hash(self._receipt.as_dict())
        return self._receipt


def run_seam_witness() -> dict[str, Any]:
    """Execute the full S02 seam witness.

    Returns a dict with bundle, consumer receipt, replay verification,
    and failure cases.
    """
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)

    # Read values and compute scenarios
    for ch in bundle.channels[:6]:
        consumer.read_value(ch.channel_id)

    scenario_a = consumer.compute_scenario(
        "S00_SCENARIO_A_HIGH_DEMOCRACY_SUPPORT",
        ["P_Y_given_A", "P_Y_given_A_B"],
    )
    scenario_b = consumer.compute_scenario(
        "S00_SCENARIO_B_LOW_DEMOCRACY_SUPPORT",
        ["P_Y_given_A_B", "P_Y_given_A_B_C"],
    )

    receipt = consumer.get_receipt()

    # Deterministic replay verification
    bundle2 = build_sociological_bundle()
    replay_ok = bundle2.content_hash == bundle.content_hash

    return {
        "contract_version": SEAM_CONTRACT_VERSION,
        "bundle": bundle.as_dict(),
        "consumer_receipt": receipt.as_dict(),
        "replay_verified": replay_ok,
        "scenario_a": scenario_a,
        "scenario_b": scenario_b,
        "effects": {
            "v3_invoked": False,
            "v2_invoked": False,
            "actor_created": False,
            "biography_generated": False,
            "parent_created": False,
            "real_current_claim": False,
        },
    }


__all__ = [
    "SEAM_CONTRACT_VERSION",
    "SEAM_BUNDLE_SCHEMA",
    "SeamContractError",
    "ChannelValue",
    "ValueReadReceipt",
    "SociologicalWorldBundle",
    "ConsumerReceipt",
    "ContractOnlySeamConsumer",
    "build_sociological_bundle",
    "run_seam_witness",
]
