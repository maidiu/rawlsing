"""PYAT R3 S00-S02 — selected-world to sociological seam adapter.

Development-only, SOURCE_FREE_SYNTHETIC; original-source GT2 values are HELD.  This module
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
from dataclasses import dataclass, field, replace
from types import MappingProxyType
from fractions import Fraction
from typing import Any, Mapping

from rawlsing_next.pre553_n9_n10w_progressive_candidate import (
    E03_ORACLE,
    build_synthetic_world,
    run_progressive_chain,
    consume_step_with_f8,
    ProgressiveChainResult,
    ProgressiveStepResult,
)
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_selected_world_progressive_contract import (
    SelectedWorldContract,
    select_world,
    verify_chain_preserves_contract,
    contract_content_hash,
)

SEAM_CONTRACT_VERSION = "R3_S02_SOCIOLOGICAL_SEAM_WITNESS@1.0.0"
SEAM_BUNDLE_SCHEMA = "R3_SOCIOLOGICAL_WORLD_BUNDLE@1"
SOURCE_FREE_SYNTHETIC = "SOURCE_FREE_SYNTHETIC"
GT2_VALUE_HOLD = "SOURCE_VALUE_UNAVAILABLE__ISSUED_GT2_AGGREGATE_AND_USE_AUTHORITY_HOLD"
P04_FIXTURE_SCOPE = "P04_SYNTHETIC_58_RESPONDENT_FIXTURE"
NATIVE_SYNTHETIC_SCOPE = "SOURCE_FREE_SYNTHETIC_Q86B_Q86A_JOINT"
Q86_CODES = {"0": "No", "1": "Yes", "9": "Dont know", "997": "Not asked", "998": "Refused", "-1": "Missing"}
P04_STEPS = ("P_Y_given_A", "P_Y_given_A_B", "P_Y_given_A_B_C")



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
    used_in: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "channel_id": self.channel_id,
            "value_hash": self.value_hash,
            "semantic_effect": self.semantic_effect,
            "query_ref": self.query_ref,
            "used_in": self.used_in,
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
    """Source-free P04 numerical fixture. Historical S00 Q86 construct claims are rejected."""
    contract, world = select_world()
    chain = run_progressive_chain(world)
    if not all(verify_chain_preserves_contract(contract, chain).values()):
        raise SeamContractError("P04_OWNER_CHAIN_BINDING_INVALID")

    channels = []
    for step in chain.steps:
        for cell_key, cell in step.cells.items():
            channels.append(ChannelValue(
                channel_id=f"CH_{step.step_id}_{cell_key}",
                evidence_mode="TRANSFORMED",
                value={
                    "step_id": step.step_id,
                    "conditioners": [list(c) for c in step.conditioners],
                    "cell": cell_key,
                    "raw_numerator_support": cell["raw_numerator_support"],
                    "raw_probability_exact_fraction": cell["raw_probability_exact_fraction"],
                    "producer_evidence_ref": step.produced_evidence.evidence_ref.as_dict(),
                },
                support=step.raw_denominator_support,
                units="synthetic_exact_conditional_fraction",
                source_scope=P04_FIXTURE_SCOPE,
                test_origin=True,
            ))

    evidence_graph = []
    for step in chain.steps:
        evidence_graph.append({
            "node_id": f"EV_{step.step_id}",
            "evidence_mode": "TRANSFORMED",
            "parent_refs": [step.produced_evidence.evidence_ref.as_dict()],
            "method": step.producer_route,
            "uncertainty": step.uncertainty_state,
            "test_origin": True,
            "source_scope": P04_FIXTURE_SCOPE,
        })

    conditions = []
    for step in chain.steps:
        conditions.append({
            "step_id": step.step_id,
            "conditioners": [list(c) for c in step.conditioners],
            "predicate_ref": f"joint_predicate_{step.step_id}",
            "denominator": step.raw_denominator_support,
            "risk_set_ref": (step.risk_set_ref.as_dict()
                             if hasattr(step.risk_set_ref, "as_dict")
                             else dict(step.risk_set_ref)),
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
            "geography": "NONE__P04_SYNTHETIC_TEST_ONLY",
            "historical_boundary": "NONE__P04_SYNTHETIC_TEST_ONLY",
            "population": "58 synthetic A/B/C/Y fixture respondents",
            "unit": "synthetic fixture respondent",
            "status": SOURCE_FREE_SYNTHETIC,
            "qualified_real_source_value_read": False,
            "source_measurement": "P04_SIMULATED_A_B_C_Y__NOT_AFRO_R5_Q86",
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
            "source_permission": "SOURCE_FREE_ONLY",
            "qualified_gt2_numeric_cells": False,
        },
        selected_world_contract=contract,
    )
    content_hash = _content_hash(bundle.as_dict())  # hash material has empty content_hash
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


def build_source_free_native_joint_bundle(
    joint_cells: Mapping[tuple[int, int], int],
    *,
    bundle_id: str = "S00C_Q86B_Q86A_BINARY_TEST_ONLY",
) -> SociologicalWorldBundle:
    """Exercise native Q86B conditioner / Q86A target on an INVENTED 2x2.

    This is a separate source-free hostile fixture, never retained GT2.
    Four input cells preserve (Q86B, Q86A) semantic order. The production
    source/routing/permission bridge remains blocked.
    """
    expected = {(0, 0), (0, 1), (1, 0), (1, 1)}
    if (not isinstance(joint_cells, Mapping)
            or set(joint_cells) != expected
            or any(type(v) is not int or v < 0 for v in joint_cells.values())):
        raise SeamContractError("NATIVE_TEST_REQUIRES_EXACT_NONNEGATIVE_2X2")
    # Native 2x2 synthetic world MUST NOT borrow P04's distinct 58-row risk.
    material = {"schema": "S00C_SOURCE_FREE_Q86B_Q86A_2X2@1",
                "cells": [[x, y, joint_cells[(x, y)]]
                          for x in (0, 1) for y in (0, 1)]}
    def sref(kind: str, role: str) -> ExactRef:
        return ExactRef(kind, f"urn:test:s00c:binary-joint:{role}",
                        _content_hash({"role": role, "material": material}))
    contract = SelectedWorldContract(
        contract_id="S00C_SOURCE_FREE_BINARY_JOINT_SELECTION@1.0.0",
        world_tag="s00c-synthetic-q86-native",
        source_universe_ref=sref("SYNTHETIC_UNIVERSE", "source"),
        release_ref=sref("SYNTHETIC_RELEASE", "release"),
        risk_set_ref=sref("SYNTHETIC_RISK_SET", "joint-risk"),
        selection_metadata={
            "schema": "S00C_BINARY_JOINT_SELECTION@1",
            "fixture_id": "S00C_SOURCE_FREE_NATIVE_2X2",
            "row_count": sum(joint_cells.values()),
            "selection_kind": SOURCE_FREE_SYNTHETIC,
            "real_current": False,
        },
        real_current=False,
    )
    channels, conditions, steps = [], [], []
    for x in (0, 1):
        step_id = f"P_Q86A_given_Q86B_{x}"
        denom = joint_cells[(x, 0)] + joint_cells[(x, 1)]
        for y in (0, 1):
            num = joint_cells[(x, y)]
            frac = Fraction(num, denom) if denom > 0 else None
            channels.append(ChannelValue(
                channel_id=f"CH_{step_id}_{y}",
                evidence_mode="TRANSFORMED",
                value={
                    "step_id": step_id, "conditioners": [["Q86B", str(x)]],
                    "cell": str(y), "raw_numerator_support": num,
                    "raw_probability_exact_fraction": None if frac is None else
                    {"$exact_fraction": [frac.numerator, frac.denominator]},
                    "producer_evidence_ref": "S00C_SYNTHETIC_2X2_INPUT_ONLY",
                },
                support=denom, units="synthetic_exact_conditional_fraction",
                source_scope=NATIVE_SYNTHETIC_SCOPE, test_origin=True,
            ))
        conditions.append({
            "step_id": step_id, "conditioners": [["Q86B", str(x)]],
            "predicate_ref": f"SOURCE_FREE_TEST_Q86B_{x}",
            "denominator": denom, "risk_set_ref": contract.risk_set_ref.as_dict(),
        })
        steps.append({
            "step_id": step_id, "producer_route": "SOURCE_FREE_2X2_VALUE_COURT",
            "cells": {str(y): {"numerator": joint_cells[(x, y)]}
                      for y in (0, 1)},
            "consumer_state": "TEST_ONLY",
            "uncertainty_state": "NOT_REAL_SOURCE",
        })
    empty = SociologicalWorldBundle(
        bundle_id=bundle_id, contract_version=SEAM_CONTRACT_VERSION,
        content_hash="",
        world_scope={
            "geography": "NONE__SYNTHETIC_TEST_ONLY",
            "historical_boundary": "NONE__SYNTHETIC_TEST_ONLY",
            "population": "invented 2x2 native semantic test",
            "unit": "synthetic joint cell",
            "status": SOURCE_FREE_SYNTHETIC,
            "qualified_real_source_value_read": False,
            "source_measurement": "BINARY_Q86B_CONDITIONER_Q86A_TARGET_TEST__NOT_GT2",
            "target": "Q86A",
            "conditioner": "Q86B",
            "native_codes": dict(Q86_CODES),
            "native_semantic_limit": "CITIZENSHIP_INCLUSION_OPINIONS__NO_DEMOCRACY_TRUST",
        },
        channels=tuple(channels),
        evidence_graph=({
            "node_id": "S00C_NATIVE_SYNTHETIC_2X2",
            "evidence_mode": "TRANSFORMED",
            "method": "HAND_CONSTRUCTED_JOINT_HOSTILE",
            "source_scope": NATIVE_SYNTHETIC_SCOPE,
            "parent_refs": [], "test_origin": True,
        },),
        conditions=tuple(conditions),
        steps=tuple(steps),
        replay={
            "input_preimages": [contract_content_hash(contract)],
            "code_ref": "S00C_SYNTHETIC_NATIVE_2X2_ONLY",
            "deterministic": True, "test_origin": True,
            "source_permission": "SOURCE_FREE_ONLY",
            "qualified_gt2_numeric_cells": False,
        },
        selected_world_contract=contract,
    )
    return replace(empty, content_hash=_content_hash(empty.as_dict()))


def build_retained_gt2_bundle(*, issued_source_owned_values: Any = None,
                              issued_use_authority: Any = None) -> SociologicalWorldBundle:
    """Exact scientific HOLD, not a caller-constructible source issuer.

    Actual retained source-owned EmpiricalFact / Field Forge numerical cells,
    exact 11-country risk member set, source-native missingness, and issuer-held
    operation-use permission are not supplied at this bounded commission.
    Arbitrary dicts or strings are NEVER promoted into measured GT2.
    """
    raise SeamContractError(GT2_VALUE_HOLD)


class ContractOnlySeamConsumer:
    """Exact producer-value-reading source-free consumer; never a GT2 grant."""

    CONSUMER_REF = "R3_S00C_SOURCE_FREE_VALUE_USE_CONSUMER@1.0.0"

    def __init__(self, bundle: SociologicalWorldBundle) -> None:
        self._bundle = bundle
        self._receipt = ConsumerReceipt(
            consumer_ref=self.CONSUMER_REF,
            requested_scope=bundle.bundle_id,
        )

    def _refuse(self, scenario_id: str, reason: str, *,
                status: str = "REFUSED") -> dict[str, Any]:
        self._receipt.refused_fields.append({
            "scenario_id": scenario_id, "reason": reason,
        })
        return {
            "scenario_id": scenario_id, "status": status,
            "reason": reason, "scientific_claim_grade": SOURCE_FREE_SYNTHETIC,
        }

    def _validate_bundle(self) -> str | None:
        if self._bundle.content_hash != _content_hash(
            replace(self._bundle, content_hash="").as_dict()
        ):
            return "BUNDLE_CONTENT_HASH_MISMATCH"
        scope = self._bundle.world_scope
        if (scope.get("status") != SOURCE_FREE_SYNTHETIC
                or scope.get("qualified_real_source_value_read") is not False):
            return "UNISSUED_SOURCE_QUALIFICATION"
        if self._bundle.selected_world_contract.real_current is not False:
            return "PROTECTED_CURRENT_NOT_AUTHORIZED"
        if (self._bundle.replay.get("test_origin") is not True
                or self._bundle.replay.get("source_permission") != "SOURCE_FREE_ONLY"
                or self._bundle.replay.get("qualified_gt2_numeric_cells") is not False):
            return "MISSING_SOURCE_FREE_ORIGIN_BINDING"
        if self._bundle.replay.get("input_preimages") != [
            contract_content_hash(self._bundle.selected_world_contract)
        ]:
            return "SELECTED_WORLD_BINDING_MISMATCH"
        expected_risk = self._bundle.selected_world_contract.risk_set_ref.as_dict()
        if any(c.get("risk_set_ref") != expected_risk for c in self._bundle.conditions):
            return "RISK_SET_OR_SELECTION_BINDING_MISMATCH"
        if not self._bundle.channels:
            return "NO_SOURCE_OWNED_CHANNELS"
        if len({c.channel_id for c in self._bundle.channels}) != len(
            self._bundle.channels
        ):
            return "DUPLICATE_CHANNEL_ID"
        expected_scope = (P04_FIXTURE_SCOPE if scope.get("target") is None else
                          NATIVE_SYNTHETIC_SCOPE if scope.get("target") == "Q86A" else None)
        if expected_scope is None:
            return "UNSUPPORTED_TARGET_SEMANTICS"
        if any(ch.source_scope != expected_scope or ch.test_origin is not True
               or ch.evidence_mode != "TRANSFORMED" for ch in self._bundle.channels):
            return "SOURCE_SCOPE_OR_VALUE_ORIGIN_MISMATCH"
        frac_issue = self._validate_fraction_closure()
        if frac_issue:
            return frac_issue
        step_issue = self._validate_step_geometry()
        if step_issue:
            return step_issue
        return None

    def _validate_fraction_closure(self) -> str | None:
        for ch in self._bundle.channels:
            val = ch.value
            num = val.get("raw_numerator_support")
            frac = val.get("raw_probability_exact_fraction")
            support = ch.support
            if num is not None and frac is not None and isinstance(support, int) and support > 0:
                from fractions import Fraction as _F
                expected = _F(num, support)
                claimed = _F(frac["$exact_fraction"][0], frac["$exact_fraction"][1])
                if expected != claimed:
                    return "FRACTION_CLOSURE_MISMATCH"
        for step in self._bundle.steps:
            for cell_key, cell in step["cells"].items():
                num = cell.get("numerator")
                frac = cell.get("fraction")
                if num is not None and frac is not None:
                    from fractions import Fraction as _F
                    step_denom = sum(c.get("numerator", 0) for c in step["cells"].values())
                    if step_denom > 0:
                        expected = _F(num, step_denom)
                        claimed = _F(frac["$exact_fraction"][0], frac["$exact_fraction"][1])
                        if expected != claimed:
                            return "STEP_CELL_FRACTION_MISMATCH"
        return None

    def _validate_step_geometry(self) -> str | None:
        channel_map = {c.channel_id: c for c in self._bundle.channels}
        condition_map = {c["step_id"]: c for c in self._bundle.conditions}
        for step in self._bundle.steps:
            step_id = step["step_id"]
            condition = condition_map.get(step_id)
            if condition is None:
                return "STEP_MISSING_CONDITION"
            channel_numerators = {}
            for ch_id, ch in channel_map.items():
                if ch.value.get("step_id") == step_id:
                    cell_key = str(ch.value.get("cell"))
                    channel_numerators[cell_key] = ch.value.get("raw_numerator_support")
            for cell_key, cell in step["cells"].items():
                if cell_key in channel_numerators:
                    if cell.get("numerator") != channel_numerators[cell_key]:
                        return "STEP_CELL_NUMERATOR_MISMATCH"
            channel_denom = sum(channel_numerators.values())
            if channel_denom != condition.get("denominator"):
                return "DENOMINATOR_CLOSURE_MISMATCH"
        return None

    def read_value(self, channel_id: str, *, query_ref: str = "") -> ChannelValue | None:
        """A retrieval is never evidence of use until the arithmetic consumes it."""
        for ch in self._bundle.channels:
            if ch.channel_id == channel_id:
                self._receipt.values_read.append(ValueReadReceipt(
                    receipt_id=f"VRR_{len(self._receipt.values_read)+1:04d}",
                    channel_id=channel_id,
                    value_hash=_content_hash(ch.as_dict()),
                    semantic_effect="VALUE_READ_ONLY",
                    query_ref=query_ref or f"read_{channel_id}",
                ))
                return ch
        self._receipt.refused_fields.append({
            "channel_id": channel_id, "reason": "CHANNEL_NOT_FOUND",
        })
        return None

    def compute_scenario(self, scenario_id: str, conditioning: list[str]) -> dict[str, Any]:
        """Calculate exact conditional counts/fractions FROM read producer cells.

        Conditioning is an exact, ordered set of P04 successive step refs.
        Distinct steps never contribute an overlapping denominator sum.
        """
        issue = self._validate_bundle()
        if issue:
            return self._refuse(scenario_id, issue)
        _lower_id = scenario_id.lower()
        if (any(t in _lower_id for t in (
            "democracy_support", "institutional_trust", "democratic_attitudes",
        ))):
            return self._refuse(scenario_id, "FALSE_S00_Q86_SOURCE_MEANING")
        if not isinstance(conditioning, (list, tuple)) or not conditioning:
            return self._refuse(scenario_id, "NO_CONDITION_SPEC", status="NO_SUPPORT")
        native_steps = ("P_Q86A_given_Q86B_0", "P_Q86A_given_Q86B_1")
        allowed_steps = native_steps if self._bundle.world_scope.get("target") == "Q86A" else P04_STEPS
        if any(x not in allowed_steps for x in conditioning):
            return self._refuse(scenario_id, "NO_MATCHING_CHANNELS", status="NO_SUPPORT")
        indices = [allowed_steps.index(x) for x in conditioning]
        if (len(indices) > 1 and allowed_steps == native_steps) or indices != list(range(indices[0], indices[0] + len(indices))):
            return self._refuse(scenario_id, "NONCUMULATIVE_P04_STEP_SEQUENCE")
        conditions = {c["step_id"]: c for c in self._bundle.conditions}
        if len(conditions) != len(self._bundle.conditions):
            return self._refuse(scenario_id, "DUPLICATE_PREDICATE_ID")
        trace = []
        for step_id in conditioning:
            condition = conditions.get(step_id)
            if condition is None:
                return self._refuse(scenario_id, "MISSING_PREDICATE")
            inputs = []
            receipt_indices = []
            for cell in ("0", "1"):
                channel = self.read_value(
                    f"CH_{step_id}_{cell}", query_ref=f"{scenario_id}:{step_id}"
                )
                if channel is None:
                    return self._refuse(scenario_id, "MISSING_CONDITIONED_TARGET_CELL")
                receipt_indices.append(len(self._receipt.values_read) - 1)
                val = channel.value
                if (val.get("step_id") != step_id or str(val.get("cell")) != cell
                        or val.get("conditioners") != condition.get("conditioners")):
                    return self._refuse(scenario_id, "SOURCE_NATIVE_PREDICATE_DRIFT")
                count = val.get("raw_numerator_support")
                if type(count) is not int or count < 0:
                    return self._refuse(scenario_id, "INVALID_RAW_NUMERATOR")
                if type(channel.support) is not int or channel.support < 0:
                    return self._refuse(scenario_id, "INVALID_RAW_DENOMINATOR")
                inputs.append((channel, count))
            denom = sum(count for _, count in inputs)
            if (type(condition.get("denominator")) is not int
                    or denom != condition["denominator"]
                    or any(ch.support != denom for ch, _ in inputs)):
                return self._refuse(scenario_id, "SOURCE_COUNT_CLOSURE_MISMATCH")
            if denom == 0:
                return self._refuse(
                    scenario_id, "ZERO_DENOMINATOR_ABSTENTION", status="ZERO_SUPPORT"
                )
            for i in receipt_indices:
                rr = self._receipt.values_read[i]
                self._receipt.values_read[i] = replace(
                    rr, semantic_effect="VALUE_USED_IN_EXACT_CONDITIONAL",
                    used_in=f"{scenario_id}:{step_id}",
                )
            trace.append({
                "step_id": step_id,
                "predicate_ref": condition["predicate_ref"],
                "conditioners": condition["conditioners"],
                "raw_denominator_support": denom,
                "raw_numerators": {
                    cell: inputs[int(cell)][1] for cell in ("0", "1")
                },
                "exact_probabilities": {
                    cell: {"$exact_fraction": [
                        Fraction(inputs[int(cell)][1], denom).numerator,
                        Fraction(inputs[int(cell)][1], denom).denominator,
                    ]} for cell in ("0", "1")
                },
                "used_input_refs": [
                    {"channel_id": ch.channel_id, "value_hash": _content_hash(ch.as_dict())}
                    for ch, _ in inputs
                ],
            })
        last = trace[-1]
        final_ids = [v["channel_id"] for v in last["used_input_refs"]]
        result = {
            "scenario_id": scenario_id, "conditioning": list(conditioning),
            "channels_used": final_ids,
            "total_support": last["raw_denominator_support"],
            "raw_denominator_support": last["raw_denominator_support"],
            "raw_numerators": last["raw_numerators"],
            "exact_probabilities": last["exact_probabilities"],
            "distributions": [
                ch.as_dict() for ch in self._bundle.channels if ch.channel_id in final_ids
            ],
            "progressive_trace": trace,
            "source_value_dependency": {
                "value_reads_used": sum(len(t["used_input_refs"]) for t in trace),
                "used_input_refs": last["used_input_refs"],
                "source_permission": "SOURCE_FREE_ONLY",
            },
            "scientific_claim_grade": SOURCE_FREE_SYNTHETIC,
            "status": "COMPUTED",
        }
        self._receipt.scenario_results[scenario_id] = result
        return result

    def get_receipt(self) -> ConsumerReceipt:
        material = self._receipt.as_dict()
        material["output_hash"] = ""  # hash excludes itself
        self._receipt.output_hash = _content_hash(material)
        return self._receipt


def run_seam_witness() -> dict[str, Any]:
    """P04 source-free cumulative value-use witness, NOT an R5 measurement."""
    bundle = build_sociological_bundle()
    consumer = ContractOnlySeamConsumer(bundle)

    scenario_a = consumer.compute_scenario(
        "P04_SYNTHETIC_PROGRESSIVE_A_TO_AB",
        ["P_Y_given_A", "P_Y_given_A_B"],
    )
    scenario_b = consumer.compute_scenario(
        "P04_SYNTHETIC_PROGRESSIVE_AB_TO_ABC",
        ["P_Y_given_A_B", "P_Y_given_A_B_C"],
    )
    if scenario_a["status"] != "COMPUTED" or scenario_b["status"] != "COMPUTED":
        raise SeamContractError("P04_VALUE_USE_CLOSURE_REFUSED")
    receipt = consumer.get_receipt()
    replay = build_sociological_bundle()
    return {
        "contract_version": SEAM_CONTRACT_VERSION,
        "bundle": bundle.as_dict(),
        "consumer_receipt": receipt.as_dict(),
        "replay_verified": replay.content_hash == bundle.content_hash,
        "scenario_a": scenario_a,
        "scenario_b": scenario_b,
        "scientific_claim_grade": SOURCE_FREE_SYNTHETIC,
        "real_gt2_value_use": GT2_VALUE_HOLD,
        "historic_s00_source_contract": "REJECTED_FALSE_Q86_DEMOCRACY_TRUST_SEMANTICS",
        "effects": {
            "v3_invoked": False, "v2_invoked": False,
            "actor_created": False, "biography_generated": False,
            "parent_created": False, "real_current_claim": False,
            "gt2_original_source_executed": False,
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
    "build_source_free_native_joint_bundle",
    "build_retained_gt2_bundle",
    "SOURCE_FREE_SYNTHETIC",
    "GT2_VALUE_HOLD",
    "run_seam_witness",
]
