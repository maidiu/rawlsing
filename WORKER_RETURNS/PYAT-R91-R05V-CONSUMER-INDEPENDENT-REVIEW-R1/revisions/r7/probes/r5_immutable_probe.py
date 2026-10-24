"""R05V R5 independent coordinator-input and route-qualification probes.

These inspect the actual R5 interface/tests for the High decision's required
native input associations and trusted-coordinator coverage of discovery/
recursive/joint routes. They do not modify candidate code.
"""
from __future__ import annotations

from dataclasses import fields
import inspect
import json
from pathlib import Path

import pytest

from rawlsing_next.pre553_learned_world_composition import (
    NativeGraphSlot,
    TrustedNativeGraphCoordinator,
)
import rawlsing_next.tests.test_universal_learned_consumer as t

OUTCOMES = Path(__file__).resolve().parents[1] / "outcomes"
OBSERVATIONS: list[dict] = []


def _record(name: str, observed: dict) -> None:
    OBSERVATIONS.append({"probe": name, **observed})


@pytest.fixture(scope="module", autouse=True)
def _dump():
    yield
    OUTCOMES.mkdir(parents=True, exist_ok=True)
    (OUTCOMES / "r05v_r5_observations.json").write_text(
        json.dumps({"schema": "R91_R05V_R5_INDEPENDENT_OBSERVATIONS@1", "probes": OBSERVATIONS}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def test_native_graph_slot_carries_actual_native_input_associations():
    names = {field.name for field in fields(NativeGraphSlot)}
    required = {
        "discovery_result", "discovery_receipt_ref", "discovery_frontier_ref",
        "recursive_handoff", "recursive_lineage_refs", "root_parent_ref",
        "condition_value_witness", "target_arity", "joint_order_semantics",
        "m1_disposition", "m2_release", "b5_selection", "require_current_selection",
        "e41_input",
    }
    missing = sorted(required - names)
    _record("slot_fields", {"fields": sorted(names), "missing": missing})
    assert not missing


def test_coordinator_execute_binds_discovery_recursive_e41_inputs():
    source = inspect.getsource(TrustedNativeGraphCoordinator.execute)
    required_terms = ("discovery", "recursive", "handoff", "lineage", "frontier", "e41", "m1", "m2", "b5", "currentness")
    missing = [term for term in required_terms if term not in source.lower()]
    _record("coordinator_inputs", {"missing_terms": missing})
    assert not missing


def test_actual_discovery_recursive_use_trusted_coordinator():
    disc = inspect.getsource(t.test_actual_discovery_route_learned_and_consumer)
    rec = inspect.getsource(t.test_actual_recursive_route_learned_and_consumer)
    _record(
        "trusted_coordinator_route_coverage",
        {"discovery_has_reader": "trusted_graph_reader" in disc,
         "recursive_has_reader": "trusted_graph_reader" in rec},
    )
    assert "trusted_graph_reader" in disc
    assert "trusted_graph_reader" in rec


def test_actual_source_sever_and_e41_route_on_discovery_recursive():
    disc = inspect.getsource(t.test_actual_discovery_route_learned_and_consumer)
    rec = inspect.getsource(t.test_actual_recursive_route_learned_and_consumer)
    combined = (disc + rec).lower()
    _record(
        "actual_source_e41_coverage",
        {"has_wrong_source_or_evidence": any(x in combined for x in ("wrong_source", "changed_source", "source_change", "evidence_change")),
         "has_e41_extension": "provide_empirical_possibility_slice_ext" in combined or "e41" in combined},
    )
    assert any(x in combined for x in ("wrong_source", "changed_source", "source_change", "evidence_change"))
    assert "provide_empirical_possibility_slice_ext" in combined or "e41" in combined
