"""R95 R06 source-separated world selected-view qualification (TEST_ONLY)."""
from __future__ import annotations

from dataclasses import replace
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from rawlsing_next.pre553_analytical_composition import compose_positioned_subject_possibility
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_universal_world_binding import (
    WorldFieldBinding, WorldSelectionRequest, select_world_view,
)
from rawlsing_next.tests import c1_at08_at13_fixture as fx
from rawlsing_next.tests.test_pre553_empirical_query import (
    _predicate, _query, _response_leaf,
)
from rawlsing_next.tests.test_universal_learned_consumer import _build_case


def _world_case(o_value="AB", x_value=1):
    case = _build_case()
    m = case["m01"]
    pairing = fx.make_pairing_authority("r95-r06-world")
    source = {
        "repo": case["repository"], "release_ref": case["release"],
        "universe": m["projection"].universes[0], "qrefs": m["qrefs"],
        "risk_refs": {"R": m["risk"]}, "source_auth": m["projection_auth"],
        "authorities": tuple(m["projection"].authority_snapshots),
    }
    predicate = _predicate(
        source, m["qauth"],
        {"op": "AND", "children": [
            _response_leaf(source, m["qauth"], "X", x_value),
            _response_leaf(source, m["qauth"], "O", o_value),
        ]},
        tag=f"r95-r06-{o_value}",
    )
    producer = _query(source, m["qauth"], predicate, ("Y",), tag=f"r95-r06-y-{o_value}")
    x_binding = fx.make_conditioner_binding(
        binding_id="x",
        subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, "X", x_value)),
        empirical_coordinate_ref=m["qrefs"]["X"],
        comparability_authority_ref=pairing,
        source_universe_ref=case["consumer_query"].source_universe_ref,
        release_ref=case["consumer_query"].release_ref,
    )
    o_binding = fx.make_conditioner_binding(
        binding_id="o",
        subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, "O", o_value)),
        empirical_coordinate_ref=m["qrefs"]["O"],
        comparability_authority_ref=pairing,
        source_universe_ref=case["consumer_query"].source_universe_ref,
        release_ref=case["consumer_query"].release_ref,
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id=f"r95-r06-world-{o_value}",
        subject_ref=case["consumer_query"].subject_ref,
        target_ref=case["consumer_query"].target_ref,
        source_universe_ref=case["consumer_query"].source_universe_ref,
        release_ref=case["consumer_query"].release_ref,
        bindings=[x_binding, o_binding],
        projection_kind="R95_R06_WORLD",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id=f"urn:test:r95:r06:world:{o_value}",
        consumer_query=consumer_query,
        producer_query=producer,
        producer_predicate=predicate,
        bindings=[x_binding, o_binding],
        coordinate_value_pairs=[
            (m["qrefs"]["X"], x_value), (m["qrefs"]["O"], o_value),
        ],
        pairing_authority=pairing,
        source_universe_ref=consumer_query.source_universe_ref,
        release_ref=consumer_query.release_ref,
    )
    composition = compose_positioned_subject_possibility(
        repository=case["repository"], empirical_query=producer,
        predicate=predicate, authority_registry=case["registry"],
        release_refs=(case["release"],), consumer_query=consumer_query,
        model_rule=case["model_rule"], condition_binding_witness=witness,
    )
    assert composition.analytical_state == "SUPPORTED"
    fields = (
        WorldFieldBinding(
            "x", m["qrefs"]["X"], x_value, x_binding.subject_fact_ref,
            consumer_query.source_universe_ref, consumer_query.release_ref,
            unit="person", clock_ref="T0",
        ),
        WorldFieldBinding(
            "o", m["qrefs"]["O"], o_value, o_binding.subject_fact_ref,
            consumer_query.source_universe_ref, consumer_query.release_ref,
            unit="person", clock_ref="T0",
        ),
    )
    request = WorldSelectionRequest(
        fields=fields, repository=case["repository"], empirical_query=producer,
        predicate=predicate, authority_registry=case["registry"],
        release_refs=(case["release"],), consumer_query=consumer_query,
        model_rule=case["model_rule"], condition_binding_witness=witness,
        as_of_ref="ASOF-R95-R06",
    )
    return case, request, composition


def test_r06_two_fields_affect_same_actual_consumer_view():
    case, request, composition = _world_case("AB")
    view = select_world_view(request)
    assert view.state == "SUPPORTED"
    assert view.consumer_result.result_hash == composition.consumer_result_or_null.result_hash
    assert view.consumer_values_read["consumer_result_hash"] == view.consumer_result.result_hash
    _, request_b, composition_b = _world_case("BA", 0)
    view_b = select_world_view(request_b)
    assert view_b.state == "SUPPORTED"
    assert view_b.view_hash != view.view_hash
    assert view_b.consumer_result.result_hash != view.consumer_result.result_hash
    # Deterministic cold recomputation of the same selected view.
    again = select_world_view(request)
    assert again.view_hash == view.view_hash


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_r06_world_view_cold_subprocess_replay():
    _, request, _ = _world_case("AB")
    view = select_world_view(request)
    code = """
import json
from rawlsing_next.tests.test_universal_world_binding import _world_case
from rawlsing_next.pre553_universal_world_binding import select_world_view
_, request, _ = _world_case("AB")
view = select_world_view(request)
print(json.dumps({"state": view.state, "view_hash": view.view_hash,
                  "consumer_hash": view.consumer_result.result_hash}, sort_keys=True))
"""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-c", code], cwd=str(REPO_ROOT), env=env,
        capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 0, proc.stderr[-2000:]
    child = json.loads(proc.stdout)
    assert child["state"] == view.state
    assert child["view_hash"] == view.view_hash
    assert child["consumer_hash"] == view.consumer_result.result_hash


def test_r06_world_separation_and_authority_refusals():
    case, request, _ = _world_case("AB")
    foreign = ExactRef("EmpiricalUniverse@1.0.0", "urn:test:foreign", "a" * 64)
    bad_field = replace(request.fields[1], source_universe_ref=foreign)
    refused = select_world_view(replace(request, fields=(request.fields[0], bad_field)))
    assert refused.state == "REFUSED"
    assert refused.reason_code == "WORLD_FIELD_SOURCE_RELEASE_MISMATCH"

    pooled = (
        replace(request.fields[0], unit="person"),
        replace(request.fields[1], unit="household"),
    )
    refused = select_world_view(replace(request, fields=pooled))
    assert refused.reason_code == "UNLINKED_UNIT_POOLING_UNAUTHORIZED"

    contextual = (
        request.fields[0],
        replace(request.fields[1], role="CONTEXT"),
    )
    refused = select_world_view(replace(request, fields=contextual))
    assert refused.reason_code == "CONTEXT_AS_STRUCTURAL_UNAUTHORIZED"

    temporal = (
        request.fields[0],
        replace(request.fields[1], clock_ref="T1"),
    )
    refused = select_world_view(replace(request, fields=temporal))
    assert refused.reason_code == "UNOBSERVED_TEMPORAL_PAIR"

    refused = select_world_view(replace(request, currentness="REVOKED"))
    assert refused.reason_code == "WORLD_CURRENTNESS_NOT_CURRENT"
    assert refused.z_unresolved is True


def test_r06_actual_relation_transport_and_observed_temporal_pair_controls():
    case, request, _ = _world_case("AB")
    transport = ExactRef("F6Authority", "urn:test:r06:transport", "b" * 64)
    pair = ExactRef("F7TemporalPair", "urn:test:r06:pair", "c" * 64)
    fields = (
        replace(request.fields[0], unit="person", relation_ref=transport, clock_ref="T0"),
        replace(request.fields[1], unit="household", relation_ref=transport, clock_ref="T1"),
    )
    authorized = select_world_view(replace(
        request, fields=fields,
        relation_transport_ref=transport, relation_transport_authorized=True,
        temporal_pair_ref=pair, observed_temporal_pair_refs=(pair,),
    ))
    assert authorized.state == "SUPPORTED"
    assert authorized.reason_code == "WORLD_SELECTED_VIEW"
