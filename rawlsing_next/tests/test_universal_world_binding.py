"""R95 R06 source-separated world selected-view qualification (TEST_ONLY)."""
from __future__ import annotations

from copy import copy
from dataclasses import replace
from types import SimpleNamespace
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile

import pytest

import rawlsing_next.pre553_learned_world_composition as i4
from rawlsing_next.pre553_analytical_composition import compose_positioned_subject_possibility
from rawlsing_next.pre553_universal_empirical_extension import provide_empirical_possibility_slice_ext
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_universal_world_binding import (
    JoinedWorldField, JoinedWorldSelectionRequest,
    ProgressivePrefixInput, ProgressiveWorldRequest,
    R05ActualExecution, R05WorldConsumerRequest, R05WorldField,
    WorldBindingError, configure_progressive_world_context,
    configure_trusted_execution_context, progressive_source_rows_identity,
    WorldFieldBinding, WorldSelectionRequest,
    progressive_world_view, select_joined_world_view,
    select_r05_world_view, select_world_view,
)
from rawlsing_next.tests import c1_at08_at13_fixture as fx
from rawlsing_next.tests.test_pre553_empirical_query import (
    _build_source, _predicate, _query, _query_authority, _registry,
    _response_leaf,
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
    assert refused.reason_code == "CROSS_UNIT_LINKED_QUERY_UNAVAILABLE"

    contextual = (
        request.fields[0],
        replace(request.fields[1], role="CONTEXT"),
    )
    refused = select_world_view(replace(request, fields=contextual))
    assert refused.reason_code == "CONTEXT_STRUCTURAL_AUTHORITY_HELD"

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
    refused = select_world_view(replace(
        request, fields=fields,
        relation_transport_ref=transport, relation_transport_authorized=True,
        temporal_pair_ref=pair, observed_temporal_pair_refs=(pair,),
    ))
    assert refused.state == "REFUSED"
    assert refused.reason_code == "CROSS_UNIT_LINKED_QUERY_UNAVAILABLE"


J42_COMMIT = "f53cb0d2bce52640268c844c398bbd8007d28edc"
J42_PACKET = ("WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-"
              "ACTUAL-JOINT-PREV3-CONSUMER-R1")
J42_ROWS_HASH = "4320b3a505478c274fc756ce0e025e36685e0742e940072aae80ce11286e4c02"


def _run_j42_build():
    base = Path(tempfile.mkdtemp(prefix=".r06-j42-", dir=REPO_ROOT))
    try:
        archive = base / "packet.tar"
        subprocess.run(
            ["git", "archive", J42_COMMIT, J42_PACKET, "-o", str(archive)],
            cwd=str(REPO_ROOT), check=True, capture_output=True, timeout=180,
        )
        with tarfile.open(archive) as handle:
            handle.extractall(base)
        packet = base / J42_PACKET
        env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
        env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
        proc = subprocess.run(
            [sys.executable, str(packet / "runtime/j42_build.py"),
             "--outdir", str(base / "out")],
            cwd=str(REPO_ROOT), env=env, capture_output=True, text=True,
            timeout=900,
        )
        assert proc.returncode == 0, (proc.stdout[-3000:] + proc.stderr[-3000:])
        receipts = json.loads(
            (packet / "n9_n10e_n10w_real_joined_consumer_receipts.json").read_text()
        )
        return receipts
    finally:
        shutil.rmtree(base, ignore_errors=True)


@pytest.fixture(scope="module")
def j42_receipts():
    return _run_j42_build()


def _joined_request(receipts, view_key="base/TEST_CURRENT/budget5", **changes):
    training = False if view_key.startswith("formal/") else True
    sanction = view_key.startswith("civil_sanction/")
    key_fields = (
        JoinedWorldField("training_access", training),
        JoinedWorldField("civil_sanction", sanction),
    )
    values = dict(
        joined_receipts=receipts, view_key=view_key, fields=key_fields,
        source_rows_hash=J42_ROWS_HASH,
    )
    values.update(changes)
    return JoinedWorldSelectionRequest(**values)


def test_r06_actual_j42_n9_n10w_e04_two_fields(j42_receipts):
    receipts = j42_receipts
    base = select_joined_world_view(_joined_request(receipts))
    assert base.state == "SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER"
    values = base.consumer_values_read
    assert values["families"]["n9"].startswith("W41_")
    assert values["families"]["n10e"].startswith("E41_")
    assert values["families"]["n10w"].startswith("P41_")
    assert len(values["n10e_steps"]) == 3
    assert values["n10e_steps"][0]["state"] == "EXACT_SUPPORTED"
    assert values["n9_routes"]["training"] == "ELIGIBLE"
    assert values["n9_routes"]["civil"] == "ELIGIBLE"
    formal = select_joined_world_view(_joined_request(receipts, "formal/TEST_CURRENT/budget5"))
    assert formal.state == "SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER"
    assert formal.consumer_values_read["n9_routes"]["training"] == "BLOCKED_BY_MODELED_RULE"
    assert formal.view_hash != base.view_hash
    sanction = select_joined_world_view(_joined_request(receipts, "civil_sanction/TEST_CURRENT/budget5"))
    assert sanction.state == "SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER"
    assert sanction.consumer_values_read["n9_routes"]["civil"] == "BLOCKED_BY_MODELED_RULE"
    assert sanction.view_hash not in (base.view_hash, formal.view_hash)
    historical = select_joined_world_view(_joined_request(receipts, "base/HISTORICAL/budget5"))
    assert historical.state == "SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER"
    assert historical.consumer_values_read["n9_clock"]["valid_at"] == "2026-06-01"
    assert historical.consumer_values_read["n9_clock"]["valid_at"] != (
        base.consumer_values_read["n9_clock"]["valid_at"]
    )
    assert historical.view_hash != base.view_hash
    again = select_joined_world_view(_joined_request(receipts))
    assert again.view_hash == base.view_hash


def test_r06_actual_j42_cold_process_replay(j42_receipts):
    base = select_joined_world_view(_joined_request(j42_receipts))
    cold = select_joined_world_view(_joined_request(_run_j42_build()))
    assert cold.view_hash == base.view_hash
    assert cold.consumer_values_read["n10e_steps"] == base.consumer_values_read["n10e_steps"]
    assert cold.consumer_values_read["n10w"] == base.consumer_values_read["n10w"]


def test_r06_actual_j42_separation_controls_refuse_restore(j42_receipts):
    base = select_joined_world_view(_joined_request(j42_receipts))
    assert base.state == "SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER"
    refused = select_joined_world_view(_joined_request(
        j42_receipts, source_rows_hash="f" * 64))
    assert refused.reason_code == "JOINED_SOURCE_ROWS_MISMATCH"
    refused = select_joined_world_view(_joined_request(
        j42_receipts, fields=(JoinedWorldField("training_access", True),)))
    assert refused.reason_code == "WORLD_REQUIRES_AT_LEAST_TWO_FIELDS"
    fields = _joined_request(j42_receipts).fields
    refused = select_joined_world_view(_joined_request(
        j42_receipts, fields=(fields[0], replace(fields[1], role="CONTEXT"))))
    assert refused.reason_code == "CONTEXT_STRUCTURAL_AUTHORITY_HELD"
    refused = select_joined_world_view(_joined_request(
        j42_receipts, fields=(replace(fields[0], unit="person"),
                              replace(fields[1], unit="household"))))
    assert refused.reason_code == "CROSS_UNIT_LINKED_QUERY_UNAVAILABLE"
    refused = select_joined_world_view(_joined_request(
        j42_receipts, fields=(replace(fields[0], clock_ref="T0"),
                              replace(fields[1], clock_ref="T1"))))
    assert refused.reason_code == "UNOBSERVED_TEMPORAL_PAIR"
    refused = select_joined_world_view(_joined_request(j42_receipts, currentness="REVOKED"))
    assert refused.reason_code == "WORLD_CURRENTNESS_NOT_CURRENT"
    restored = select_joined_world_view(_joined_request(j42_receipts))
    assert restored.view_hash == base.view_hash


P41_COMMIT = "f27d1101048638bba395143a48efb7ef00bfcda4"
P41_PACKET = ("WORKER_RETURNS/PYAT-R41-P41-GENERIC-PROGRESSIVE-"
              "N10E-N10W-SERVING-R1")


def _materialize_p41_runtime():
    base = Path(tempfile.mkdtemp(prefix=".r06r2-p41-", dir=REPO_ROOT))
    archive = base / "p41.tar"
    subprocess.run(
        ["git", "archive", P41_COMMIT, P41_PACKET, "-o", str(archive)],
        cwd=str(REPO_ROOT), check=True, capture_output=True, timeout=180,
    )
    with tarfile.open(archive) as handle:
        handle.extractall(base)
    return base / P41_PACKET / "runtime", base


@pytest.fixture(scope="module")
def p41_runtime():
    runtime, base = _materialize_p41_runtime()
    try:
        yield str(runtime)
    finally:
        shutil.rmtree(base, ignore_errors=True)


def _build_r05_learned_inprocess():
    """Build the actual accepted R05 learned object + retained-original coordinator view."""
    case = _build_case()
    disposition = case["learned"].m1_disposition
    objects = {
        obj.ref: obj for obj in (
            case["m01_result"].object_graph.empirical_facts
            + case["m01_result"].object_graph.executed_queries
            + case["m01_result"].object_graph.executed_predicates
        )
    }
    query = objects[disposition.empirical_query_spec_refs[0]]
    predicate = objects[disposition.empirical_predicate_refs[1]]
    fact = objects[disposition.empirical_fact_refs[1]]
    conditioner = case["consumer_query"].conditioner_bindings[0]
    pairing = conditioner.comparability_authority_ref
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:r06r2:actual:r05",
        consumer_query=case["consumer_query"],
        producer_query=query,
        producer_predicate=predicate,
        bindings=[conditioner],
        coordinate_value_pairs=[(case["m01"]["qrefs"]["X"], 1)],
        pairing_authority=pairing,
        source_universe_ref=case["consumer_query"].source_universe_ref,
        release_ref=case["consumer_query"].release_ref,
    )
    extension = provide_empirical_possibility_slice_ext(
        repository=case["repository"], empirical_query=query,
        predicate=predicate, authority_registry=case["registry"],
        release_refs=(case["release"],), consumer_query=case["consumer_query"],
        model_rule=case["model_rule"], condition_binding_witness=witness,
    )
    slot = i4.NativeGraphSlot(
        "r06r2-actual-r05", case["consumer_query"].source_universe_ref,
        case["consumer_query"].release_ref, query.ref, predicate.ref,
        case["consumer_query"].ref, case["model_rule"].rule_hash,
        "DIRECT_I03_TO_POSITIONED_SUBJECT",
        condition_value_witness=witness, target_arity=1,
        joint_order_semantics="SEMANTIC_ORDERED",
        m1_disposition=case["learned"].m1_disposition,
        m2_release=case["learned"].m2_artifacts.release.ref,
        e41_input=extension, repository=case["repository"],
        empirical_query=query, predicate=predicate,
        authority_registry=case["registry"],
        consumer_query=case["consumer_query"], model_rule=case["model_rule"],
    )
    coordinator = i4.TrustedNativeGraphCoordinator(
        admitted_slots={slot.slot_id: slot}
    )
    execution_request = i4.NativeGraphExecutionRequest((slot,))
    bound = coordinator.execute(execution_request)
    learned = i4.evaluate_learned_world_consumer(
        case["learned"], composition=bound.view.compositions[0],
        consumer_query=case["consumer_query"], model_rule=case["model_rule"],
        producer_query_ref=query.ref, producer_predicate_ref=predicate.ref,
        product_graph=bound, trusted_graph_reader=coordinator,
    )
    assert learned.state == "LEARNED_CONSUMER_EXACT_SUPPORTED", learned.reason_code
    step = {
        "schema": "R06R2_R05_LEARNED_PROVIDER@1",
        "state": "EXACT_SUPPORTED",
        "route": learned.producer_route,
        "target": "Y", "conditioners": [["X", 1]],
        "denominator": learned.denominator,
        "cells": [dict(cell) for cell in learned.cells],
        "uncertainty": "UNCERTAINTY_UNQUANTIFIED",
        "evidence_ref": None if learned.evidence_ref is None else learned.evidence_ref.as_dict(),
        "producer_query_ref": query.ref.as_dict(),
        "producer_fact_ref": fact.ref.as_dict(),
        "producer_predicate_ref": predicate.ref.as_dict(),
        "condition_witness_ref": witness.witness_ref.as_dict(),
        "model_rule_hash": case["model_rule"].rule_hash,
        "risk_set_ref": case["m01"]["risk"].as_dict(),
        "release_ref": case["release"].as_dict(),
        "content_hash": learned.consumer_result.result_hash,
    }
    return dict(
        case=case, learned=learned, step=step,
        source_universe_ref=case["consumer_query"].source_universe_ref,
        release_ref=case["consumer_query"].release_ref,
        source_rows_hash=case["m01"]["stream"].source_sha256,
        coordinator_original_ref=bound.original_ref,
        coordinator=coordinator,
        execution_request=execution_request,
        bound=bound,
    )


def _build_r05_p41_receipts(p41_runtime: str):
    """Subprocess entrypoint: actual R05 objects -> actual P41 N9/N10W/E04 view."""
    if p41_runtime not in sys.path:
        sys.path.insert(0, p41_runtime)
    import bootstrap
    bootstrap.install()
    from p41_service import P41Service
    from product.world import SelectedWorldCatalog

    data = _build_r05_learned_inprocess()
    case = data["case"]
    m01 = case["m01"]
    universe = case["consumer_query"].source_universe_ref
    release = case["consumer_query"].release_ref
    empirical = {
        "source": {
            "universe": case["m01"]["projection"].universes[0],
            "release_ref": release,
            "risk_refs": {"R": m01["risk"]},
            "qrefs": m01["qrefs"],
            "repo": case["repository"],
        },
        "release_ref": release,
        "risk_refs": {"R": m01["risk"]},
        "rows_hash": data["source_rows_hash"],
        "publication": "2026-03-01",
    }
    catalog = SelectedWorldCatalog(empirical, structural_revision=True)
    snapshots = {
        "T0": catalog.select(mode="HISTORICAL", valid_at="2026-06-01",
                             published_asof="2026-04-15"),
        "T1": catalog.select(mode="AS_OF", valid_at="2027-09-01",
                             published_asof="2027-09-01"),
    }
    step = data["step"]

    class R05Provider:
        def __init__(self):
            self.world = {"query_permits": {"Y": {}}}
            self.trace = []

        def _validate(self, target, ordered):
            if target != "Y" or tuple(tuple(c) for c in ordered) != (("X", 1),):
                raise ValueError("R06R2_R05_CONDITION_AUTHORITY")

        def progressive(self, target, ordered):
            self._validate(target, ordered)
            self.trace.append(dict(
                call="R05_LEARNED_CONSUMER_READ",
                consumer_result_hash=step["content_hash"],
            ))
            return [dict(step)]

    class R05StructuralService:
        def __init__(self, catalog):
            self.catalog = catalog
            self.value_reads = []

        def structural(self, snapshot, key, consumer):
            value = self.catalog.read(snapshot, key)
            self.value_reads.append(dict(
                consumer=consumer, key=key, state=value["state"],
                value=value.get("value"), snapshot_ref=snapshot.snapshot_hash,
            ))
            return value

        def possibilities(self, snapshot, *, target="Y",
                          conditions=(("X", 1),), consumer="GENERIC"):
            self.value_reads.append(dict(
                consumer=consumer, key="empirical", state="EXACT_SUPPORTED",
                value=self.catalog.read(snapshot, "empirical"),
                snapshot_ref=snapshot.snapshot_hash,
            ))
            return dict(
                state="PRODUCTIVE_TEST_ONLY", steps=[dict(step)],
                dependencies=["empirical"], source_root="TEST_ONLY_E04_SOURCE_ROOT",
            )

        def _record(self, material):
            import copy
            from rawlsing_next.pre553_empirical_objects import semantic_hash
            material = copy.deepcopy(material)
            material.update(
                service_contract="R06R2_R05_WORLD_SERVICE@1",
                grade="TEST_ONLY", operative_N9=False, operative_N10W=False,
                new_issuer=False, actor_executions=0, model_calls=0,
            )
            digest = semantic_hash(material)
            return dict(receipt_hash=digest, material=material)

    class R05P41Service(P41Service):
        def __init__(self, provider, structural):
            self.prepared = object()
            self.readthrough = structural
            self.provider = provider
            self.receipts = {}

        def _world_block(self, snapshot):
            block = super()._world_block(snapshot)
            block["r05_binding"] = {
                "source_universe_ref": universe.as_dict(),
                "release_ref": release.as_dict(),
                "source_rows_hash": data["source_rows_hash"],
                "learned_receipt_ref": data["learned"].learned_receipt_ref.as_dict(),
                "m1_disposition_ref": data["learned"].m1_disposition_ref.as_dict(),
                "m2_release_ref": data["learned"].m2_release_ref.as_dict(),
                "coordinator_original_ref": data["coordinator_original_ref"].as_dict(),
                "consumer_result_hash": data["learned"].consumer_result.result_hash,
                "evidence_ref": step["evidence_ref"],
            }
            return block

    receipts = {}
    for label, snapshot in snapshots.items():
        provider = R05Provider()
        structural = R05StructuralService(catalog)
        service = R05P41Service(provider, structural)
        receipts[label] = service.progressive(
            target="Y", conditions=(("X", 1),), snapshot=snapshot
        )
    return receipts


_PERSISTENT_P41_RUNTIME = None
_LAST_P41_RUNTIME = None


def _persistent_p41_runtime():
    global _PERSISTENT_P41_RUNTIME
    if _PERSISTENT_P41_RUNTIME is None:
        runtime, _base = _materialize_p41_runtime()
        _PERSISTENT_P41_RUNTIME = str(runtime)
    return _PERSISTENT_P41_RUNTIME


def _run_r05_p41(p41_runtime: str):
    global _LAST_P41_RUNTIME
    _LAST_P41_RUNTIME = _persistent_p41_runtime()
    code = (
        "import json,sys;"
        "from rawlsing_next.tests.test_universal_world_binding import "
        "_build_r05_p41_receipts;"
        "print(json.dumps(_build_r05_p41_receipts(sys.argv[1]), sort_keys=True))"
    )
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-c", code, p41_runtime], cwd=str(REPO_ROOT),
        env=env, capture_output=True, text=True, timeout=900,
    )
    assert proc.returncode == 0, proc.stdout[-3000:] + proc.stderr[-3000:]
    return json.loads(proc.stdout)


def _actual_execution_for(data, runtime, *, structural_revision=True, step=None):
    m01 = data["case"]["m01"]
    empirical = {
        "source": {
            "universe": data["case"]["m01"]["projection"].universes[0],
            "release_ref": data["release_ref"],
            "risk_refs": {"R": m01["risk"]},
            "qrefs": m01["qrefs"],
            "repo": data["case"]["repository"],
        },
        "release_ref": data["release_ref"],
        "risk_refs": {"R": m01["risk"]},
        "rows_hash": data["source_rows_hash"],
        "publication": "2026-03-01",
    }
    step_data = dict(step or data["step"])
    try:
        handle = configure_trusted_execution_context(
            p41_runtime=runtime,
            learned_consumer=data["learned"],
            step=step_data,
            empirical=empirical,
            structural_revision=structural_revision,
            coordinator=data["coordinator"],
            execution_request=data["execution_request"],
            original_ref=data["coordinator_original_ref"],
            original_view=data["bound"],
        )
    except WorldBindingError:
        handle = None
    return R05ActualExecution(
        runtime, empirical, step_data, data["learned"],
        structural_revision=structural_revision,
        coordinator_original_ref=data["coordinator_original_ref"],
        execution_handle=handle,
    )


def _r05_request(data, receipts=None, *, actual_execution=None, **changes):
    pair = ExactRef("R06R2_SYNTHETIC_TEMPORAL_PAIR", "urn:test:r06r2:pair", "a" * 64)
    runtime = _LAST_P41_RUNTIME
    if actual_execution is None and runtime is not None:
        actual_execution = _actual_execution_for(data, runtime)
    values = dict(
        learned_consumer=data["learned"],
        fields=(
            R05WorldField("training_access", True, "modeled policy eligibility boolean", temporal_expected_value=False),
            R05WorldField("civil_sanction", False, "modeled policy eligibility boolean"),
        ),
        consumer=None,
        source_universe_ref=data["source_universe_ref"],
        release_ref=data["release_ref"],
        source_rows_hash=data["source_rows_hash"],
        temporal_pair_ref=pair,
        observed_temporal_pair_refs=(pair,),
        actual_execution=actual_execution,
        claimed_receipts=receipts,
        execution_handle=(
            None if actual_execution is None else actual_execution.execution_handle
        ),
    )
    values.update(changes)
    return R05WorldConsumerRequest(**values)


def test_r06r2_actual_r05_learned_to_p41_world_with_synthetic_pair(p41_runtime):
    data = _build_r05_learned_inprocess()
    receipts = _run_r05_p41(p41_runtime)
    view = select_r05_world_view(_r05_request(data, receipts))
    assert view.state == "R05_WORLD_SELECTED_VIEW", view.reason_code
    assert view.temporal_changed is True
    values = view.consumer_values_read
    assert values["t0_routes"]["training"] == "ELIGIBLE"
    assert values["t1_routes"]["training"] == "BLOCKED_BY_MODELED_RULE"
    assert values["t0_routes"]["exit_constraint"] == "WITHIN_MODELED_BUDGET"
    assert values["t1_routes"]["exit_constraint"] == "RESOURCE_CONSTRAINED"
    assert values["t0_clock"]["valid_at"] == "2026-06-01"
    assert values["t1_clock"]["valid_at"] == "2027-09-01"
    assert values["t0_n10e_steps"][0]["content_hash"] == values["consumer_result_hash"]
    assert values["t1_n10e_steps"][0]["content_hash"] == values["consumer_result_hash"]
    assert values["t0_receipt_hash"] != values["t1_receipt_hash"]
    assert values["coordinator_original_ref"] is not None
    again = select_r05_world_view(_r05_request(data, receipts))
    assert again.view_hash == view.view_hash


def test_r06r2_actual_r05_world_cold_replay(p41_runtime):
    data = _build_r05_learned_inprocess()
    fresh = _run_r05_p41(p41_runtime)
    view = select_r05_world_view(_r05_request(data, fresh))
    cold_receipts = _run_r05_p41(p41_runtime)
    cold = select_r05_world_view(_r05_request(data, cold_receipts))
    assert cold.view_hash == view.view_hash
    assert cold.consumer_values_read["t0_n10w"] == view.consumer_values_read["t0_n10w"]
    assert cold.consumer_values_read["t1_routes"] == view.consumer_values_read["t1_routes"]


def test_r06r2_actual_r05_world_separation_refusals_restore(p41_runtime):
    data = _build_r05_learned_inprocess()
    receipts = _run_r05_p41(p41_runtime)
    base = select_r05_world_view(_r05_request(data, receipts))
    assert base.state == "R05_WORLD_SELECTED_VIEW"
    refused = select_r05_world_view(_r05_request(data, receipts, source_rows_hash="f" * 64))
    assert refused.reason_code == "R05_ACTUAL_EMPIRICAL_ROWS_MISMATCH"
    refused = select_r05_world_view(_r05_request(
        data, receipts,
        fields=(R05WorldField("training_access", True, "modeled policy eligibility boolean", temporal_expected_value=False),),
    ))
    assert refused.reason_code == "R05_WORLD_REQUIRES_AT_LEAST_TWO_FIELDS"
    fields = _r05_request(data, receipts).fields
    refused = select_r05_world_view(_r05_request(
        data, receipts, fields=(fields[0], replace(fields[1], role="CONTEXT")),
    ))
    assert refused.reason_code == "CONTEXT_STRUCTURAL_AUTHORITY_HELD"
    refused = select_r05_world_view(_r05_request(
        data, receipts,
        fields=(replace(fields[0], unit="person"), replace(fields[1], unit="household")),
    ))
    assert refused.reason_code == "CROSS_UNIT_LINKED_QUERY_UNAVAILABLE"
    refused = select_r05_world_view(_r05_request(
        data, receipts, observed_temporal_pair_refs=(),
    ))
    assert refused.reason_code == "UNOBSERVED_TEMPORAL_PAIR"
    refused = select_r05_world_view(_r05_request(data, receipts, currentness="REVOKED"))
    assert refused.reason_code == "R05_CURRENTNESS_NOT_CURRENT"
    tampered = json.loads(json.dumps(receipts))
    tampered["T1"]["structural"]["routes"]["training"] = "ELIGIBLE"
    tampered["T1"].pop("content_hash", None)
    tampered["T1"]["content_hash"] = semantic_hash(tampered["T1"])
    refused = select_r05_world_view(_r05_request(data, tampered))
    assert refused.reason_code == "R05_CLAIMED_RECEIPT_MISMATCH"
    wrong_learned = replace(
        data["learned"],
        learned_receipt_ref=ExactRef(
            "LearnedWorldCompositionReceipt",
            "urn:test:r06r2:wrong-learned", "b" * 64,
        ),
    )
    changed = dict(data, learned=wrong_learned)
    original_execution = _actual_execution_for(data, _LAST_P41_RUNTIME)
    refused = select_r05_world_view(_r05_request(
        changed, receipts, actual_execution=original_execution,
    ))
    assert refused.reason_code == "R05_LEARNED_ORIGINAL_MISMATCH"
    evidence_tampered = json.loads(json.dumps(receipts))
    evidence_tampered["T0"]["n9_world"]["r05_binding"]["evidence_ref"] = ExactRef(
        "C1_POSITIONED_SUBJECT_SLICE_EVIDENCE@1",
        "urn:test:r06r2:foreign-evidence", "c" * 64,
    ).as_dict()
    evidence_tampered["T0"].pop("content_hash", None)
    evidence_tampered["T0"]["content_hash"] = semantic_hash(evidence_tampered["T0"])
    refused = select_r05_world_view(_r05_request(data, evidence_tampered))
    assert refused.reason_code == "R05_CLAIMED_RECEIPT_MISMATCH"
    fact_tampered = json.loads(json.dumps(receipts))
    fact_tampered["T0"]["n10e_steps"][0]["producer_fact_ref"] = ExactRef(
        "EmpiricalFact@1.0.0",
        "urn:test:r06r2:foreign-fact", "d" * 64,
    ).as_dict()
    fact_tampered["T0"].pop("content_hash", None)
    fact_tampered["T0"]["content_hash"] = semantic_hash(fact_tampered["T0"])
    refused = select_r05_world_view(_r05_request(data, fact_tampered))
    assert refused.reason_code == "R05_CLAIMED_RECEIPT_MISMATCH"
    restored = select_r05_world_view(_r05_request(data, receipts))
    assert restored.view_hash == base.view_hash


def _run_actual_world_view(p41_runtime):
    code = (
        "import json,sys;"
        "from rawlsing_next.tests.test_universal_world_binding import "
        "_build_r05_learned_inprocess,_actual_execution_for,_r05_request;"
        "from rawlsing_next.pre553_universal_world_binding import select_r05_world_view;"
        "data=_build_r05_learned_inprocess();"
        "execution=_actual_execution_for(data,sys.argv[1]);"
        "view=select_r05_world_view(_r05_request(data,actual_execution=execution));"
        "print(json.dumps(view.material(),sort_keys=True))"
    )
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-c", code, p41_runtime], cwd=str(REPO_ROOT),
        env=env, capture_output=True, text=True, timeout=900,
    )
    assert proc.returncode == 0, proc.stdout[-3000:] + proc.stderr[-3000:]
    return json.loads(proc.stdout)


def test_r06r3_actual_wrapper_cold_fresh_process(p41_runtime):
    _run_r05_p41(p41_runtime)
    data = _build_r05_learned_inprocess()
    execution = _actual_execution_for(data, _persistent_p41_runtime())
    view = select_r05_world_view(_r05_request(data, actual_execution=execution))
    assert view.state == "R05_WORLD_SELECTED_VIEW"
    cold = _run_actual_world_view(_persistent_p41_runtime())
    assert cold["state"] == view.state
    assert cold["view_hash"] == view.view_hash
    assert cold["consumer_values_read"]["t0_routes"] == (
        view.consumer_values_read["t0_routes"]
    )


def test_r06r3_no_actual_temporal_change_refuses(p41_runtime):
    _run_r05_p41(p41_runtime)
    data = _build_r05_learned_inprocess()
    execution = _actual_execution_for(
        data, _persistent_p41_runtime(), structural_revision=False,
    )
    fields = (
        R05WorldField(
            "training_access", True, "modeled policy eligibility boolean",
            temporal_expected_value=True,
        ),
        R05WorldField("civil_sanction", False, "modeled policy eligibility boolean"),
    )
    view = select_r05_world_view(_r05_request(
        data, fields=fields, actual_execution=execution,
    ))
    assert view.state == "REFUSED"
    assert view.reason_code == "R05_TEMPORAL_PAIR_NOT_CONSUMED"


def test_r06r3_actual_transport_and_context_refusals(p41_runtime):
    _run_r05_p41(p41_runtime)
    data = _build_r05_learned_inprocess()
    execution = _actual_execution_for(data, _persistent_p41_runtime())
    fields = _r05_request(data).fields
    relation = ExactRef(
        "R06R3_TRANSPORT_RELATION", "urn:test:r06r3:transport", "e" * 64,
    )
    linked_claim = (
        replace(fields[0], unit="person", relation_ref=relation),
        replace(fields[1], unit="household", relation_ref=relation),
    )
    refused = select_r05_world_view(_r05_request(
        data, fields=linked_claim, actual_execution=execution,
        relation_transport_authorized=True, relation_transport_ref=relation,
    ))
    assert refused.reason_code == "CROSS_UNIT_LINKED_QUERY_UNAVAILABLE"
    promoted = (fields[0], replace(fields[1], role="CONTEXT"))
    bogus_ff = ExactRef(
        "R06R3_BOGUS_FF_AUTHORITY", "urn:test:r06r3:bogus-ff", "f" * 64,
    )
    refused = select_r05_world_view(_r05_request(
        data, fields=promoted, actual_execution=execution,
        ff_structural_authority_ref=bogus_ff,
    ))
    assert refused.reason_code == "CONTEXT_STRUCTURAL_AUTHORITY_HELD"
    calls = []
    refused = select_r05_world_view(_r05_request(
        data, actual_execution=execution,
        consumer=lambda label: calls.append(label) or {},
    ))
    assert refused.reason_code == "CALLER_CALLBACK_NOT_ACCEPTED"
    assert calls == []


def test_r06r3_actual_step_severance_refuses_restore(p41_runtime):
    _run_r05_p41(p41_runtime)
    data = _build_r05_learned_inprocess()
    execution = _actual_execution_for(data, _persistent_p41_runtime())
    base = select_r05_world_view(_r05_request(data, actual_execution=execution))
    assert base.state == "R05_WORLD_SELECTED_VIEW"
    foreign = ExactRef(
        "C1_POSITIONED_SUBJECT_SLICE_EVIDENCE@1",
        "urn:test:r06r3:foreign-evidence", "9" * 64,
    )
    bad_step = dict(data["step"])
    bad_step["evidence_ref"] = foreign.as_dict()
    bad = _actual_execution_for(
        data, _persistent_p41_runtime(), step=bad_step,
    )
    refused = select_r05_world_view(_r05_request(data, actual_execution=bad))
    assert refused.state == "REFUSED"
    assert refused.reason_code in {
        "R05_N10E_EVIDENCE_BINDING_MISMATCH",
        "R05_ACTUAL_STEP_CONSUMER_MISMATCH",
    }
    restored = select_r05_world_view(_r05_request(data, actual_execution=execution))
    assert restored.view_hash == base.view_hash


def test_r06r4_forged_p41_runtime_is_refused(tmp_path, p41_runtime):
    _run_r05_p41(p41_runtime)
    data = _build_r05_learned_inprocess()
    fake = tmp_path / "forged-p41"
    fake.mkdir()
    (fake / "p41_service.py").write_text("class P41Service:\n    pass\n")
    execution = _actual_execution_for(data, str(fake))
    view = select_r05_world_view(_r05_request(data, actual_execution=execution))
    assert view.state == "REFUSED"
    assert view.reason_code == "UNTRUSTED_P41_RUNTIME"


def test_r06r4_subject_selected_coordinator_original_is_refused(p41_runtime):
    _run_r05_p41(p41_runtime)
    data = _build_r05_learned_inprocess()
    execution = replace(
        _actual_execution_for(data, _persistent_p41_runtime()),
        coordinator_original_ref=ExactRef(
            "R06R4_FORGED_COORDINATOR_ORIGINAL",
            "urn:test:r06r4:forged-original", "a" * 64,
        ),
    )
    view = select_r05_world_view(_r05_request(data, actual_execution=execution))
    assert view.state == "REFUSED"
    assert view.reason_code == "R05_COORDINATOR_ORIGINAL_MISMATCH"


def test_r06r4_context_authority_is_held_in_all_public_wrappers(j42_receipts, p41_runtime):
    _run_r05_p41(p41_runtime)
    data = _build_r05_learned_inprocess()
    execution = _actual_execution_for(data, _persistent_p41_runtime())
    fields = _r05_request(data).fields
    plausible = SimpleNamespace(
        typed_state="ADMITTED_FOR_EXACT_STRUCTURAL_USE",
        target_use="STRUCTURAL_MEDIATION_INPUT",
        source_universe_refs=(data["source_universe_ref"],),
        structural_semantic_identity_refs=(fields[1].field_ref,),
    )
    view = select_r05_world_view(_r05_request(
        data, fields=(fields[0], replace(fields[1], role="CONTEXT")),
        actual_execution=execution, ff_structural_admission=plausible,
    ))
    assert view.reason_code == "CONTEXT_STRUCTURAL_AUTHORITY_HELD"
    joined_fields = _joined_request(j42_receipts).fields
    view = select_joined_world_view(_joined_request(
        j42_receipts, fields=(joined_fields[0], replace(joined_fields[1], role="CONTEXT")),
        ff_structural_admission=plausible,
    ))
    assert view.reason_code == "CONTEXT_STRUCTURAL_AUTHORITY_HELD"
    case, request, _ = _world_case("AB")
    view = select_world_view(replace(
        request, fields=(request.fields[0], replace(request.fields[1], role="CONTEXT")),
        ff_structural_admission=plausible,
    ))
    assert view.reason_code == "CONTEXT_STRUCTURAL_AUTHORITY_HELD"


def _progressive_prefix(source, qauth, registry, model_rule, target, conds, tag,
                        pairing):
    predicate = _predicate(
        source, qauth,
        {"op": "AND", "children": [
            _response_leaf(source, qauth, q, value) for q, value in conds
        ]},
        tag=tag,
    )
    query = _query(source, qauth, predicate, (target,), tag=tag)
    bindings = [
        fx.make_conditioner_binding(
            binding_id=q.lower(),
            subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, q, value)),
            empirical_coordinate_ref=source["qrefs"][q],
            comparability_authority_ref=pairing,
            source_universe_ref=source["universe"].ref,
            release_ref=source["release_ref"],
        )
        for q, value in conds
    ]
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id=f"r107-{tag}",
        subject_ref=ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
            f"urn:test:r107:{tag}", semantic_hash({"fixture": "R107"}),
        ),
        target_ref=source["qrefs"][target],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=bindings, projection_kind="R107_PROGRESSIVE",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id=f"urn:test:r107:{tag}",
        consumer_query=consumer_query, producer_query=query,
        producer_predicate=predicate, bindings=bindings,
        coordinate_value_pairs=[
            (source["qrefs"][q], value) for q, value in conds
        ],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    return ProgressivePrefixInput(
        tag, source["qrefs"][target],
        tuple((source["qrefs"][q], value) for q, value in conds),
        source["repo"], source["release_ref"], query, predicate, registry,
        consumer_query, model_rule, witness,
    )


def _progressive_fixture(target="Y", conds=(("X", 1), ("O", "AB")),
                         revoked_scope=None):
    rows = []
    groups = [
        ("X1OABY1", {"X": 1, "O": "AB", "Y": 1}, 30),
        ("X1OBAY0", {"X": 1, "O": "BA", "Y": 0}, 10),
        ("X0OABY0", {"X": 0, "O": "AB", "Y": 0}, 20),
        ("X0OBAY1", {"X": 0, "O": "BA", "Y": 1}, 20),
    ]
    for prefix, responses, count in groups:
        rows.extend({"id": f"{prefix}{n:03d}", "responses": dict(responses)}
                    for n in range(count))
    risk = {q: {row["id"] for row in rows} for q in ("X", "Y", "O")}
    source = _build_source("r107", rows, question_namespace="r107",
                           risk_sets={"R": risk})
    qauth = _query_authority("r107-query")
    registry = _registry(source, qauth)
    model = fx.make_model_rule(source["universe"].ref, "r107")
    pairing = fx.make_pairing_authority("r107")
    prefixes = tuple(
        _progressive_prefix(source, qauth, registry, model, target,
                            conds[:depth], f"r107-{target}-{depth}", pairing)
        for depth in range(1, len(conds) + 1)
    )
    world_empirical = {
        "source": {
            "universe": source["universe"],
            "release_ref": source["release_ref"],
            "risk_refs": {"R": source["risk_refs"]["R"]},
            "qrefs": source["qrefs"], "repo": source["repo"],
        },
        "release_ref": source["release_ref"],
        "risk_refs": {"R": source["risk_refs"]["R"]},
        "rows_hash": progressive_source_rows_identity(
            source["repo"], source["release_ref"]),
        "publication": "2026-03-01",
    }
    conditions = tuple((source["qrefs"][q], value) for q, value in conds)
    handle = configure_progressive_world_context(
        target_ref=source["qrefs"][target], conditions=conditions,
        prefixes=prefixes, world_empirical=world_empirical,
        revoked_scope=revoked_scope,
    )
    return handle


def test_r107_actual_n9_n10e_to_n10w_progressive():
    handle = _progressive_fixture()
    t0 = progressive_world_view(ProgressiveWorldRequest(
        handle, "T0", "GENERIC_POSITIONED_SUBJECT", "HISTORICAL"))
    t1 = progressive_world_view(ProgressiveWorldRequest(
        handle, "T1", "GENERIC_POSITIONED_SUBJECT", "AS_OF"))
    assert t0.state == "PROGRESSIVE_WORLD_SELECTED_VIEW", t0.reason_code
    assert t1.state == "PROGRESSIVE_WORLD_SELECTED_VIEW", t1.reason_code
    assert t0.prefix_count == 2
    assert len(t0.n10e_steps) == 2
    assert len(t0.n10w["progressive_update_identity"]) == 2
    assert t0.n10e_steps[0]["cells"] != t0.n10e_steps[1]["cells"]
    assert any(cell["cell_state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
               for cell in t0.alternatives[1]["cells"])
    assert min(cell["raw_numerator_support"]
               for cell in t0.alternatives[0]["cells"]) < max(
                   cell["raw_numerator_support"]
                   for cell in t0.alternatives[0]["cells"])
    assert t0.n10w["positioned_consumptions"]
    assert t0.world_routes is not None and t1.world_routes is not None
    assert t0.world_routes != t1.world_routes
    assert t0.world_routes["training"] == "ELIGIBLE"
    assert t1.world_routes["training"] == "BLOCKED_BY_MODELED_RULE"
    assert t0.actor_state == "NOT_TOUCHED"
    assert t0.view_hash != t1.view_hash


def test_r107_reusable_target_and_prefix_shape():
    handle = _progressive_fixture(target="X", conds=(("Y", 1), ("O", "AB")))
    view = progressive_world_view(ProgressiveWorldRequest(
        handle, "T0", "GENERIC_POSITIONED_SUBJECT", "HISTORICAL"))
    assert view.state == "PROGRESSIVE_WORLD_SELECTED_VIEW", view.reason_code
    assert view.target_ref.kind == "QUESTION_NATIVE"
    assert view.prefix_count == 2
    assert len(view.n10e_steps) == 2
    assert view.world_routes is not None


def test_r107_refuses_wrong_handle_snapshot_currentness_and_prefix_order():
    handle = _progressive_fixture()
    refused = progressive_world_view(ProgressiveWorldRequest(
        "missing-handle", "T0"))
    assert refused.reason_code == "PROGRESSIVE_EXECUTION_HANDLE_INVALID"
    refused = progressive_world_view(ProgressiveWorldRequest(handle, "T9"))
    assert refused.reason_code == "PROGRESSIVE_WORLD_SNAPSHOT_UNKNOWN"
    refused = progressive_world_view(ProgressiveWorldRequest(
        handle, "T0", "GENERIC_POSITIONED_SUBJECT", "AS_OF"))
    assert refused.reason_code == "PROGRESSIVE_CURRENTNESS_MISMATCH"
    refused = progressive_world_view(ProgressiveWorldRequest(
        handle, "T0", "GENERIC_POSITIONED_SUBJECT", "HISTORICAL", "1999-01-01"))
    assert refused.reason_code == "PROGRESSIVE_AS_OF_MISMATCH"
    target, conditions, prefixes, world_empirical = _progressive_fixture_parts()
    with pytest.raises(WorldBindingError):
        configure_progressive_world_context(
            target_ref=target, conditions=conditions,
            prefixes=(prefixes[0], replace(prefixes[1], conditions=(
                prefixes[1].conditions[1], prefixes[1].conditions[0]))),
            world_empirical=world_empirical)


def _progressive_fixture_parts():
    rows = [
        {"id": f"R{i}", "responses": {"X": i % 2, "Y": 1, "O": "AB"}}
        for i in range(8)
    ]
    source = _build_source("r107parts", rows, question_namespace="r107parts",
                           risk_sets={"R": {q: {row["id"] for row in rows}
                                            for q in ("X", "Y", "O")}})
    qauth = _query_authority("r107parts-query")
    registry = _registry(source, qauth)
    model = fx.make_model_rule(source["universe"].ref, "r107parts")
    pairing = fx.make_pairing_authority("r107parts")
    conditions = ((source["qrefs"]["X"], 1), (source["qrefs"]["O"], "AB"))
    prefixes = tuple(
        _progressive_prefix(source, qauth, registry, model, "Y",
                            (("X", 1), ("O", "AB"))[:depth],
                            f"r107parts-{depth}", pairing)
        for depth in range(1, 3)
    )
    world = {
        "source": {"universe": source["universe"],
                   "release_ref": source["release_ref"],
                   "risk_refs": {"R": source["risk_refs"]["R"]},
                   "qrefs": source["qrefs"], "repo": source["repo"]},
        "release_ref": source["release_ref"],
        "risk_refs": {"R": source["risk_refs"]["R"]},
        "rows_hash": progressive_source_rows_identity(
            source["repo"], source["release_ref"]),
        "publication": "2026-03-01",
    }
    return source["qrefs"]["Y"], conditions, prefixes, world


def test_r107_configure_rejects_target_and_condition_mismatch():
    target, conditions, prefixes, world_empirical = _progressive_fixture_parts()
    with pytest.raises(WorldBindingError):
        configure_progressive_world_context(
            target_ref=ExactRef("QUESTION_NATIVE", "urn:test:r107:wrong-target", "f" * 64),
            conditions=conditions, prefixes=prefixes,
            world_empirical=world_empirical)
    with pytest.raises(WorldBindingError):
        configure_progressive_world_context(
            target_ref=target,
            conditions=((conditions[0][0], 0), conditions[1]),
            prefixes=prefixes, world_empirical=world_empirical)


def _run_r107_view_subprocess():
    code = (
        "import json;"
        "from rawlsing_next.tests.test_universal_world_binding import _progressive_fixture;"
        "from rawlsing_next.pre553_universal_world_binding import ProgressiveWorldRequest,progressive_world_view;"
        "h=_progressive_fixture();"
        "v=progressive_world_view(ProgressiveWorldRequest(h,'T0','GENERIC_POSITIONED_SUBJECT','HISTORICAL'));"
        "print(json.dumps({'state':v.state,'view_hash':v.view_hash,"
        "'receipt':v.receipt_hash,'steps':len(v.n10e_steps),"
        "'routes':v.world_routes,'n10w':len(v.n10w['progressive_update_identity'])}))"
    )
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-c", code], cwd=str(REPO_ROOT), env=env,
        capture_output=True, text=True, timeout=900,
    )
    assert proc.returncode == 0, proc.stdout[-3000:] + proc.stderr[-3000:]
    return json.loads(proc.stdout)


def test_r107_revoked_world_scope_is_typed_unavailable_and_restores():
    handle = _progressive_fixture(revoked_scope="training_access")
    view = progressive_world_view(ProgressiveWorldRequest(
        handle, "T1", "GENERIC_POSITIONED_SUBJECT", "AS_OF"))
    assert view.state == "PROGRESSIVE_WORLD_UNAVAILABLE"
    assert view.world_routes["training"].startswith("UNAVAILABLE")
    restored_handle = _progressive_fixture()
    restored = progressive_world_view(ProgressiveWorldRequest(
        restored_handle, "T1", "GENERIC_POSITIONED_SUBJECT", "AS_OF"))
    assert restored.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"


def test_r107_cold_replay_same_world_and_progressive_view():
    handle = _progressive_fixture()
    view = progressive_world_view(ProgressiveWorldRequest(
        handle, "T0", "GENERIC_POSITIONED_SUBJECT", "HISTORICAL"))
    cold = _run_r107_view_subprocess()
    assert cold["state"] == view.state
    assert cold["view_hash"] == view.view_hash
    assert cold["receipt"] == view.receipt_hash
    assert cold["steps"] == len(view.n10e_steps)
    assert cold["routes"] == dict(view.world_routes)
    assert cold["n10w"] == len(view.n10w["progressive_update_identity"])


def test_r110_foreign_world_identity_refuses_before_serving():
    target, conditions, prefixes, world = _progressive_fixture_parts()
    foreign = ExactRef("C11LogicalRelease", "REL-r110-foreign", "f" * 64)
    bad = dict(world)
    bad["release_ref"] = foreign
    bad["source"] = dict(world["source"])
    bad["source"]["release_ref"] = foreign
    handle = configure_progressive_world_context(
        target_ref=target, conditions=conditions, prefixes=prefixes,
        world_empirical=bad)
    view = progressive_world_view(ProgressiveWorldRequest(
        handle, "T0", "GENERIC_POSITIONED_SUBJECT", "HISTORICAL"))
    assert view.state == "REFUSED"
    assert view.reason_code == "PROGRESSIVE_WORLD_SOURCE_RELEASE_RISK_MISMATCH"


def test_r110_empirical_revocation_is_typed_unavailable_and_restores():
    handle = _progressive_fixture(revoked_scope="empirical")
    view = progressive_world_view(ProgressiveWorldRequest(
        handle, "T1", "GENERIC_POSITIONED_SUBJECT", "AS_OF"))
    assert view.state == "PROGRESSIVE_WORLD_UNAVAILABLE"
    assert view.reason_code == "WORLD_EMPIRICAL_REVOKED_OR_UNAVAILABLE"
    assert view.n9_world["empirical"]["state"] == "REVOKED"
    restored = progressive_world_view(ProgressiveWorldRequest(
        _progressive_fixture(), "T1", "GENERIC_POSITIONED_SUBJECT", "AS_OF"))
    assert restored.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"


def test_r110_n10w_positioned_consumptions_bind_actual_n10e_hashes():
    view = progressive_world_view(ProgressiveWorldRequest(
        _progressive_fixture(), "T0", "GENERIC_POSITIONED_SUBJECT", "HISTORICAL"))
    assert view.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    step_hashes = {step["content_hash"] for step in view.n10e_steps}
    positioned = view.n10w["positioned_consumptions"]
    observed = [entry.get("consumer_result_hash") for entry in positioned]
    assert len(observed) == len(view.n10e_steps)
    assert all(isinstance(value, str) and value for value in observed)
    assert set(observed) == step_hashes
    assert all(entry.get("source") == "LIVE_TRACE" for entry in positioned)


def test_r115_world_rows_hash_must_match_actual_owner_rows():
    target, conditions, prefixes, world = _progressive_fixture_parts()
    bad = dict(world)
    bad["rows_hash"] = "f" * 64
    handle = configure_progressive_world_context(
        target_ref=target, conditions=conditions, prefixes=prefixes,
        world_empirical=bad)
    view = progressive_world_view(ProgressiveWorldRequest(
        handle, "T0", "GENERIC_POSITIONED_SUBJECT", "HISTORICAL"))
    assert view.state == "REFUSED"
    assert view.reason_code == "PROGRESSIVE_WORLD_SOURCE_RELEASE_RISK_MISMATCH"


def test_r115_world_source_repository_is_required():
    target, conditions, prefixes, world = _progressive_fixture_parts()
    bad = dict(world)
    bad["source"] = {
        key: value for key, value in world["source"].items() if key != "repo"
    }
    handle = configure_progressive_world_context(
        target_ref=target, conditions=conditions, prefixes=prefixes,
        world_empirical=bad)
    view = progressive_world_view(ProgressiveWorldRequest(
        handle, "T0", "GENERIC_POSITIONED_SUBJECT", "HISTORICAL"))
    assert view.state == "REFUSED"
    assert view.reason_code == "PROGRESSIVE_WORLD_SOURCE_RELEASE_RISK_MISMATCH"


def test_r115_mixed_prefix_repository_identity_refuses():
    target, conditions, prefixes, world = _progressive_fixture_parts()
    mixed = (prefixes[0], replace(
        prefixes[1], repository=copy(prefixes[1].repository),
    ))
    handle = configure_progressive_world_context(
        target_ref=target, conditions=conditions, prefixes=mixed,
        world_empirical=world)
    view = progressive_world_view(ProgressiveWorldRequest(
        handle, "T0", "GENERIC_POSITIONED_SUBJECT", "HISTORICAL"))
    assert view.state == "REFUSED"
    assert view.reason_code == "PROGRESSIVE_WORLD_SOURCE_RELEASE_RISK_MISMATCH"


def test_r117_mixed_prefix_model_identity_refuses():
    target, conditions, prefixes, world = _progressive_fixture_parts()
    other = fx.make_model_rule(
        prefixes[0].model_rule.source_universe_refs[0], "r117-other-model")
    mixed = (prefixes[0], replace(prefixes[1], model_rule=other))
    handle = configure_progressive_world_context(
        target_ref=target, conditions=conditions, prefixes=mixed,
        world_empirical=world)
    view = progressive_world_view(ProgressiveWorldRequest(
        handle, "T0", "GENERIC_POSITIONED_SUBJECT", "HISTORICAL"))
    assert view.state == "REFUSED"
    assert view.reason_code == "PROGRESSIVE_WORLD_SOURCE_RELEASE_RISK_MISMATCH"


def test_r117_consistent_alternate_model_remains_valid():
    target, conditions, prefixes, world = _progressive_fixture_parts()
    other = fx.make_model_rule(
        prefixes[0].model_rule.source_universe_refs[0], "r117-consistent-model")
    consistent = tuple(
        replace(prefix, model_rule=other) for prefix in prefixes
    )
    handle = configure_progressive_world_context(
        target_ref=target, conditions=conditions, prefixes=consistent,
        world_empirical=world)
    view = progressive_world_view(ProgressiveWorldRequest(
        handle, "T0", "GENERIC_POSITIONED_SUBJECT", "HISTORICAL"))
    assert view.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    hashes = {step["model_rule_hash"] for step in view.n10e_steps}
    assert hashes == {other.rule_hash}
