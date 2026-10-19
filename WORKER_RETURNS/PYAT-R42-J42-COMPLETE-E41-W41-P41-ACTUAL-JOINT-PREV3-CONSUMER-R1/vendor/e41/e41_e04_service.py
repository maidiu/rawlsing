"""E41 bridge: original E04 NONPARENT_OPTIONS client over E41-computed slices.

This module implements a sourcefree TEST_ONLY service whose ``possibilities``
step is computed by the real E41 N10E path (accepted provider via the versioned
extension) on the frozen AT07 / AT08 synthetic laws — never by caller-supplied
or vendored fixture probabilities. The original E04 ``product.nonparent.consume``
client (vendored byte-identical; see ``vendor/__init__.py``) consumes it.

Structural policy fields are modeled TEST_ONLY booleans/tokens exactly as in the
independently reviewed E04L return; they carry no survey science.
"""
from __future__ import annotations

from copy import deepcopy
import importlib.util
from pathlib import Path
import sys
from typing import Any

RETURN_DIR = Path(__file__).resolve().parent
if str(RETURN_DIR) not in sys.path:
    sys.path.insert(0, str(RETURN_DIR))

import bootstrap  # noqa: F401

VENDOR_DIR = RETURN_DIR / "vendor"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

# Retained E03 sourcefree module, registered exactly as the E04L return does
# (byte-identical vendored copy at vendor/aux/, provenance in vendor/__init__.py).
if "rawlsing_next" not in sys.modules:
    import rawlsing_next  # noqa: F401

_AUX_NAME = "rawlsing_next.pre553_n9_n10w_progressive_candidate"
if _AUX_NAME not in sys.modules:
    import rawlsing_next as _rn

    _spec = importlib.util.spec_from_file_location(
        _AUX_NAME, VENDOR_DIR / "aux" / "pre553_n9_n10w_progressive_candidate.py"
    )
    _module = importlib.util.module_from_spec(_spec)
    sys.modules[_AUX_NAME] = _module
    _spec.loader.exec_module(_module)
    setattr(_rn, "pre553_n9_n10w_progressive_candidate", _module)

from e41_provider_extension import provide_empirical_possibility_slice_ext

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.tests import c1_at08_at13_fixture as fx
from rawlsing_next.tests import n10e_empirical_slice_fixture as n10e
from rawlsing_next.tests.test_pre553_analytical_composition_higher_order import (
    _attitude_domain,
    _attitude_source_and_authority,
)
from rawlsing_next.tests.test_pre553_empirical_query import _query_authority, _registry

from product.empirical import build_source
from product.world import SelectedWorldCatalog

SERVICE_CONTRACT = "E41_N10E_COMPUTED_SLICE_E04_SERVICE@1"
GRADE = "TEST_ONLY_SOURCEFREE_CANDIDATE"


def _material_for_at07(direction: str = "forward") -> dict[str, Any]:
    case = n10e.build_provider_case(direction)
    return {
        "repository": case["source"]["repo"],
        "empirical_query": case["empirical_query"],
        "predicate": case["predicate"],
        "authority_registry": case["registry"],
        "release_refs": case["release_refs"],
        "consumer_query": case["consumer_query"],
        "model_rule": case["model_rule"],
        "condition_binding_witness": case["condition_binding_witness"],
    }


def _material_for_at08(tag: str, value: str) -> dict[str, Any]:
    from e41_tranche import direct_material

    source = _attitude_source_and_authority(tag)[0]
    qauth = _query_authority(tag)
    registry = _registry(source, qauth)
    return direct_material(
        source=source,
        qauth=qauth,
        registry=registry,
        conditions=[("RESPONSE", "ATT1", value)],
        target_question="ATT2",
        tag=tag,
        target_domain=_attitude_domain(),
    )


def _computed_step(material: dict[str, Any], *, target: str, conditioners: list[list[str]]) -> dict[str, Any]:
    """One step computed by the real E41 N10E path; no invented geometry."""

    result = provide_empirical_possibility_slice_ext(**material)
    if result.provider_state != "EXACT_SUPPORTED_SLICE_PRODUCED":
        return {
            "target": target,
            "conditioners": conditioners,
            "denominator": None,
            "cells": [],
            "state": "TYPED_UNAVAILABLE",
            "reason": result.refusal_state,
            "evidence_ref": None,
        }
    cells = [
        {"cell": _cell_key(row["cell"]), "raw_numerator_support": int(row["raw_numerator_support"])}
        for row in result.composition_result.complete_cell_geometry
    ]
    evidence_ref = result.generated_evidence_or_null.evidence_ref
    return {
        "target": target,
        "conditioners": conditioners,
        "denominator": int(result.composition_result.raw_denominator_support),
        "cells": cells,
        "state": "EXACT_SUPPORTED",
        "evidence_ref": evidence_ref.as_dict(),
        "composed_result_identity_hash": result.composition_result.composed_result_identity_hash,
        "provider_route": result.producer_route,
    }


def _cell_key(cell: Any) -> str:
    if isinstance(cell, (tuple, list)):
        return "|".join(str(part) for part in cell)
    return str(cell)


class E41ComputedSliceService:
    """Original-E04-compatible service backed by E41-computed N10E slices."""

    CONTRACT = SERVICE_CONTRACT

    def __init__(self) -> None:
        self.catalog = SelectedWorldCatalog(build_source())
        self.value_reads: list[dict[str, Any]] = []
        self.receipts: dict[str, Any] = {}

    # -- selected-world surface (delegated to the vendored TEST_ONLY catalog) --
    def select(self, **kwargs: Any) -> Any:
        return self.catalog.select(**kwargs)

    def structural(self, snapshot: Any, key: str, consumer: str) -> Any:
        value = self.catalog.read(snapshot, key)
        self.value_reads.append(
            dict(
                consumer=consumer,
                channel="structural",
                scope=key,
                source_ref=value.get("field_ref", value.get("requested_ref")),
                state=value["state"],
                value_read=value.get("value"),
                native_unit=value.get("unit"),
                snapshot_ref=snapshot.snapshot_hash,
            )
        )
        return value

    # -- empirical possibility surface (E41 computed slices) ------------------
    def possibilities(
        self,
        snapshot: Any,
        *,
        target: str = "ANSWER",
        conditions: tuple[tuple[str, str], ...] = (("POSITION", "P1"),),
        consumer: str = "GENERIC",
    ) -> dict[str, Any]:
        source = self.catalog.read(snapshot, "empirical")
        if source["state"] != "SUPPORTED_TEST_ONLY":
            self.value_reads.append(
                dict(
                    consumer=consumer,
                    channel="empirical",
                    scope="e41-computed-slice",
                    state=source["state"],
                    value_read=None,
                    snapshot_ref=snapshot.snapshot_hash,
                )
            )
            return dict(
                state=source["state"],
                steps=[],
                dependencies=["empirical"],
                source_ref=source.get("source_universe_ref", source.get("requested_ref")),
            )

        steps: list[dict[str, Any]] = []
        at07 = _computed_step(
            _material_for_at07("forward"),
            target="ANSWER",
            conditioners=[["POSITION", "P1"]],
        )
        steps.append(at07)
        at08 = _computed_step(
            _material_for_at08("e41-e04-att08", "agree"),
            target="ATT2",
            conditioners=[["ATT1", "agree"]],
        )
        steps.append(at08)

        for step in steps:
            self.value_reads.append(
                dict(
                    consumer=consumer,
                    channel="empirical",
                    scope="e41-computed-slice",
                    state=step["state"],
                    evidence_ref=step.get("evidence_ref"),
                    value_read=deepcopy(step["cells"]) if step["cells"] else None,
                    denominator=step["denominator"],
                    query_condition_order=deepcopy(step["conditioners"]),
                    target=step["target"],
                    snapshot_ref=snapshot.snapshot_hash,
                )
            )
        all_exact = all(step["state"] == "EXACT_SUPPORTED" for step in steps)
        return dict(
            state="PRODUCTIVE_TEST_ONLY" if all_exact else "PARTIAL_TYPED_EMPIRICAL_SUPPORT",
            steps=steps,
            dependencies=["empirical"],
            source_root="TEST_ONLY_E04_SOURCE_ROOT",
            claim_ceiling="SOURCE_LOCAL_EMPIRICAL_POSSIBILITY_NOT_CAUSAL_OR_PERSONAL",
        )

    # -- receipt ---------------------------------------------------------------
    def _record(self, material: dict[str, Any]) -> dict[str, Any]:
        material = deepcopy(material)
        material.update(
            service_contract=SERVICE_CONTRACT,
            grade=GRADE,
            operative_N9=False,
            operative_N10W=False,
            new_issuer=False,
            actor_executions=0,
            model_calls=0,
        )
        digest = semantic_hash(material)
        self.receipts[digest] = deepcopy(material)
        return dict(receipt_hash=digest, material=material)


def drive_original_e04_client() -> dict[str, Any]:
    """Run the unchanged original E04 NONPARENT_OPTIONS client over E41 slices."""

    from product.nonparent import consume

    service = E41ComputedSliceService()
    snapshot = service.select(
        mode="TEST_CURRENT",
        valid_at="2027-09-01",
        published_asof="2027-09-01",
        test_now="2027-09-01",
    )
    receipt = consume(service, snapshot)
    return {
        "receipt": receipt,
        "value_reads": service.value_reads,
        "snapshot_ref": snapshot.snapshot_hash,
    }


__all__ = [
    "SERVICE_CONTRACT",
    "E41ComputedSliceService",
    "drive_original_e04_client",
]
