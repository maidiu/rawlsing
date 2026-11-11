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
from rawlsing_next.tests.test_universal_world_binding import _persistent_p41_runtime
REPO_ROOT = Path(__file__).resolve().parents[2]


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
        "from rawlsing_next.tests.test_l01_reviewed_progressive_world import _progressive_fixture;"
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
