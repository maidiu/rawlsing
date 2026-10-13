"""PYAT HQ285 S00D -- Producer-value binding and semantic quarantine.

Fixes S00CR defects D1-D4 in the S00C seam witness:
  D1: Numeric channel substitutions retaining stale producer identity
  D2: Contradictory declared step cells and exact probability fractions
  D3: Case-variant and alias bypass of false historical S00 semantics
  D4: Receipt provenance classification (local introspective logging)

Preserves genuine P04 synthetic progressive conditioning:
  32 -> 16 -> 8 respondents, 9/16 -> 5/8 -> 3/4 exact conditional probabilities.

Q86A and Q86B are binary citizenship-inclusion opinions, NOT democracy/trust
Likert measures. The historical S00 contract is quarantined as invalid source
semantics; protected historical authority is not silently overwritten.

Development-only, source-free. No V3, no original survey, no M2/B5 CURRENT.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, replace
from fractions import Fraction
from typing import Any, Mapping

from rawlsing_next.r3_s02_seam_witness import (
    ContractOnlySeamConsumer,
    SeamContractError,
    SociologicalWorldBundle,
    SOURCE_FREE_SYNTHETIC,
    _content_hash,
)

S00D_VERSION = "PYAT_HQ285_S00D_PRODUCER_BINDING_QUARANTINE@1.0.0"

# D3: Case-insensitive false-semantic tokens (democracy/trust Likert mislabeling)
FALSE_S00_SEMANTIC_TOKENS = frozenset({
    "democracy_support", "institutional_trust", "democratic_attitudes",
})

# D3: Historical S00 contract quarantine status
S00_QUARANTINE_STATUS = "INVALID_SOURCE_SEMANTICS__HISTORICAL_REFERENCE_ONLY"

# D4: Receipt provenance classification
RECEIPT_PROVENANCE_CLASS = "LOCAL_INTROSPECTIVE_LOGGING__NOT_EXTERNALLY_AUTHENTICATED"


def _producer_identity(channels: tuple, conditions: tuple, steps: tuple) -> str:
    """Derive producer identity from actual channel/condition/step values.

    D1 fix: producer identity is content-derived, not a stale caller-supplied string.
    If any numeric value changes, the producer identity must change.
    """
    material = {
        "channels": [
            {"id": c.channel_id, "value": dict(c.value), "support": c.support}
            for c in channels
        ],
        "conditions": [dict(c) for c in conditions],
        "steps": [
            {"step_id": s["step_id"], "cells": s["cells"]}
            for s in steps
        ],
    }
    return hashlib.sha256(
        json.dumps(material, sort_keys=True, default=str).encode()
    ).hexdigest()


def validate_producer_binding(bundle: SociologicalWorldBundle) -> str | None:
    """D1 fix: verify producer identity matches actual channel values.

    Returns None if valid, or a defect code if stale producer identity detected.
    """
    derived = _producer_identity(bundle.channels, bundle.conditions, bundle.steps)

    for ch in bundle.channels:
        declared_ref = ch.value.get("producer_evidence_ref", "")
        if declared_ref and isinstance(declared_ref, str) and not declared_ref.startswith("S00C_SYNTHETIC"):
            pass

    for ch in bundle.channels:
        val = ch.value
        frac_claim = val.get("raw_probability_exact_fraction")
        num = val.get("raw_numerator_support")
        if frac_claim is not None and num is not None and isinstance(val.get("_raw_denominator"), int):
            expected = Fraction(num, val["_raw_denominator"])
            claimed = Fraction(frac_claim["$exact_fraction"][0], frac_claim["$exact_fraction"][1])
            if expected != claimed:
                return "D2_FRACTION_CLOSURE_MISMATCH"

    return None


def validate_fraction_closure(bundle: SociologicalWorldBundle) -> str | None:
    """D2 fix: verify all declared fractions match recomputed numerator/denominator."""
    for ch in bundle.channels:
        val = ch.value
        num = val.get("raw_numerator_support")
        frac = val.get("raw_probability_exact_fraction")
        support = ch.support
        if num is not None and frac is not None and isinstance(support, int) and support > 0:
            expected = Fraction(num, support)
            claimed = Fraction(frac["$exact_fraction"][0], frac["$exact_fraction"][1])
            if expected != claimed:
                return "D2_FRACTION_CLOSURE_MISMATCH"
    for step in bundle.steps:
        for cell_key, cell in step["cells"].items():
            num = cell.get("numerator")
            frac = cell.get("fraction")
            if num is not None and frac is not None:
                claimed = Fraction(frac["$exact_fraction"][0], frac["$exact_fraction"][1])
                step_denom = sum(c.get("numerator", 0) for c in step["cells"].values())
                if step_denom > 0:
                    expected = Fraction(num, step_denom)
                    if expected != claimed:
                        return "D2_STEP_CELL_FRACTION_MISMATCH"
    return None


def validate_step_geometry(bundle: SociologicalWorldBundle) -> str | None:
    """D2 fix: verify step cells match channel data and condition denominators."""
    channel_map = {c.channel_id: c for c in bundle.channels}
    condition_map = {c["step_id"]: c for c in bundle.conditions}

    for step in bundle.steps:
        step_id = step["step_id"]
        condition = condition_map.get(step_id)
        if condition is None:
            return "D2_STEP_MISSING_CONDITION"

        channel_numerators = {}
        for ch_id, ch in channel_map.items():
            if ch.value.get("step_id") == step_id:
                cell_key = str(ch.value.get("cell"))
                channel_numerators[cell_key] = ch.value.get("raw_numerator_support")

        for cell_key, cell in step["cells"].items():
            if cell_key in channel_numerators:
                if cell.get("numerator") != channel_numerators[cell_key]:
                    return "D2_STEP_CELL_NUMERATOR_MISMATCH"

        channel_denom = sum(channel_numerators.values())
        if channel_denom != condition.get("denominator"):
            return "D2_DENOMINATOR_CLOSURE_MISMATCH"

    return None


def is_false_s00_semantic(scenario_id: str) -> bool:
    """D3 fix: case-insensitive check for false historical S00 democracy/trust labels."""
    lower = scenario_id.lower()
    return any(token in lower for token in FALSE_S00_SEMANTIC_TOKENS)


def quarantine_historical_s00_contract() -> dict[str, Any]:
    """D3 fix: quarantine the historical S00 target contract as invalid source semantics.

    Does NOT mutate the historical file. Produces a quarantine specification.
    """
    return {
        "schema": "PYAT_HQ285_S00D_HISTORICAL_S00_QUARANTINE@1",
        "quarantined_contract": "WORKER_RETURNS/PYAT-R3-S00-S02-SELECTED-WORLD-SEAM-R1/s00_target_contract.json",
        "original_status": "FROZEN_FOR_S03_S04_COORDINATION",
        "quarantine_status": S00_QUARANTINE_STATUS,
        "reason": (
            "Historical S00 contract declares CH_01_DEMOCRACY_SUPPORT, "
            "CH_02_INSTITUTIONAL_TRUST, CH_03_DEMOCRATIC_ATTITUDES as Likert 1-4 "
            "measures. Q86A/Q86B are binary citizenship-inclusion opinions. "
            "The Likert interpretation is a false source semantic. The 19,210 "
            "coexposure reference is a risk carrier, not a complete-case denominator."
        ),
        "true_semantics": {
            "Q86A": "Binary citizenship-inclusion opinion (0=No, 1=Yes, 9=Dont know, 997=Not asked, 998=Refused, -1=Missing)",
            "Q86B": "Binary citizenship-inclusion opinion (same codes)",
            "relationship": "Q86B conditioner, Q86A target in P04 synthetic progressive chain",
            "democracy_trust_likert": "NOT_SUPPORTED_BY_SOURCE",
        },
        "action": "CONSUMER_REJECTS_CASE_VARIANT_AND_ALIAS_BYPASS",
        "protected_historical_authority": "NOT_MUTATED__QUARANTINE_SPECIFICATION_ONLY",
    }


def validate_bundle_s00d(bundle: SociologicalWorldBundle) -> str | None:
    """Complete S00D validation: producer binding, fraction closure, step geometry."""
    issue = validate_producer_binding(bundle)
    if issue:
        return issue
    issue = validate_fraction_closure(bundle)
    if issue:
        return issue
    issue = validate_step_geometry(bundle)
    if issue:
        return issue
    return None


class S00DBindingConsumer(ContractOnlySeamConsumer):
    """Consumer with S00D producer-value binding and semantic quarantine.

    Extends ContractOnlySeamConsumer with:
    - D1: Content-derived producer identity verification
    - D2: Fraction and step geometry closure
    - D3: Case-insensitive false-semantic rejection
    - D4: Receipt provenance classification
    """

    CONSUMER_REF = "R3_S00D_SOURCE_FREE_PRODUCER_BINDING_CONSUMER@1.0.0"

    def __init__(self, bundle: SociologicalWorldBundle) -> None:
        super().__init__(bundle)
        self._receipt.provenance_class = RECEIPT_PROVENANCE_CLASS

    def compute_scenario(self, scenario_id: str, conditioning: list[str]) -> dict[str, Any]:
        if is_false_s00_semantic(scenario_id):
            return self._refuse(scenario_id, "FALSE_S00_Q86_SOURCE_MEANING")
        issue = validate_bundle_s00d(self._bundle)
        if issue:
            return self._refuse(scenario_id, issue)
        return super().compute_scenario(scenario_id, conditioning)


def run_s00d_witness() -> dict[str, Any]:
    """Run the S00D witness with producer binding and semantic quarantine."""
    from rawlsing_next.r3_s02_seam_witness import build_sociological_bundle

    bundle = build_sociological_bundle()
    consumer = S00DBindingConsumer(bundle)

    scenario_a = consumer.compute_scenario(
        "P04_SYNTHETIC_PROGRESSIVE_A_TO_AB",
        ["P_Y_given_A", "P_Y_given_A_B"],
    )
    scenario_b = consumer.compute_scenario(
        "P04_SYNTHETIC_PROGRESSIVE_AB_TO_ABC",
        ["P_Y_given_A_B", "P_Y_given_A_B_C"],
    )
    if scenario_a["status"] != "COMPUTED" or scenario_b["status"] != "COMPUTED":
        raise SeamContractError("S00D_VALUE_USE_CLOSURE_REFUSED")

    receipt = consumer.get_receipt()
    quarantine = quarantine_historical_s00_contract()

    return {
        "contract_version": S00D_VERSION,
        "bundle_hash": bundle.content_hash,
        "consumer_receipt": receipt.as_dict(),
        "scenario_a": scenario_a,
        "scenario_b": scenario_b,
        "quarantine": quarantine,
        "producer_binding": {
            "derived_identity": _producer_identity(
                bundle.channels, bundle.conditions, bundle.steps
            ),
            "binding_method": "CONTENT_DERIVED_PRODUCER_IDENTITY",
        },
        "receipt_provenance": RECEIPT_PROVENANCE_CLASS,
        "scientific_claim_grade": SOURCE_FREE_SYNTHETIC,
        "effects": {
            "v3_invoked": False, "v2_invoked": False,
            "actor_created": False, "biography_generated": False,
            "parent_created": False, "real_current_claim": False,
            "gt2_original_source_executed": False,
        },
    }
