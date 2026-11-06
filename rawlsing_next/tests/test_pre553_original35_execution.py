"""D original35 manifest selection and bounded execution bridge tests."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
from collections import Counter
from types import SimpleNamespace

import pytest

from dataclasses import asdict, dataclass, replace
from rawlsing_next.pre553_original35_execution import (
    Original35ExecutionError, _RecordingResolver,
    execute_native_compiler_source, execute_source,
    consume_requested_joint_transport, execute_requested_two_target_joints,
    execute_two_target_joint_from_plan,
    load_runtime_binding, write_field_forge_envelopes,
    write_requested_joint_transport,
)
from rawlsing_next.pre553_original35_operations import build_original35_operation_plan
from rawlsing_next.source_configuration.library import SourceConfigLibrary
from rawlsing_next.pre553_original35_operations import (
    bind_governed_frontier, build_original35_operation_plan,
)
from rawlsing_next.pre553_universal_workload import execute_governed_frontier
from rawlsing_next.pre553_field_forge_empirical_ingress import (
    ingest_envelope,
)
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState
from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.tests.test_pre553_original35_operations import _fixture_config
from rawlsing_next.tests.test_universal_workload import (
    AS_OF, HOST, PURPOSE, _frontier_bundle,
)
from rawlsing_next.tests.test_universal_source_projection import (
    decode_sav, package, write_rows,
)
from rawlsing_next.pre553_source_native_preimage_adapter import (
    NativeSourceRule, materialize_native_preimages,
)

INDEX = "source_pre553_validation/integration/SOURCE_LIBRARY_INDEX.json"
REPO = Path(__file__).resolve().parents[2]


def _binding():
    try:
        return load_runtime_binding()
    except Original35ExecutionError:
        pytest.skip("local source runtime binding unavailable")


def test_all35_manifest_selection_and_operation_accounting():
    binding = _binding()
    root = binding["USER_ORIGINAL35_DATA_ROOT"]
    library = SourceConfigLibrary(index_path=INDEX, source_root=root)
    docs = [library.load_original(sid).document for sid in library.source_ids()]
    plan = build_original35_operation_plan(
        docs, source_presence={sid: True for sid in library.source_ids()},
        require_all35=True, expected_item_count=18276,
        expected_physical_slot_count=18413)
    assert len(plan.rows) == 35
    assert plan.item_count == 18276
    assert plan.physical_slot_count == 18413
    assert plan.no_drop_ok is True
    assert set(plan.counts) == {
        "EXECUTABLE_RAW", "HELD", "ABSTAIN", "INAPPLICABLE",
        "DEFERRED", "NOT_REQUESTED"}
    assert sum(plan.counts.values()) == len(plan.operations) == 18467
    assert plan.counts == {
        "ABSTAIN": 0, "DEFERRED": 51, "EXECUTABLE_RAW": 5630,
        "HELD": 4655, "INAPPLICABLE": 8131, "NOT_REQUESTED": 0}
    for sid in library.source_ids():
        selected = library.select(sid, source_root=root)
        assert selected["source_resolution"]["status"] == "RESOLVED_UNDER_EFFECTIVE_ROOT"
        assert selected["source_read_performed"] is False


def test_manifest_only_source_result_and_typed_path_resolution():
    binding = _binding()
    root = binding["USER_ORIGINAL35_DATA_ROOT"]
    library = SourceConfigLibrary(index_path=INDEX, source_root=root)
    result = execute_source(
        "SRC31", library=library, source_root=root, allow_decode=False)
    assert result.status == "MANIFEST_ONLY"
    assert result.source_id == "SRC31"
    assert result.row_count == 0
    assert result.physical_slots == 68
    assert result.response_slots == 64
    assert result.operation_counts["EXECUTABLE_RAW"] > 0
    assert result.reasons == ("MANIFEST_ONLY_NOT_DECODED",)
    assert result.material()["native"] is False


def test_native_path_refuses_without_current_source_read_decision():
    binding = _binding()
    root = binding["USER_ORIGINAL35_DATA_ROOT"]
    library = SourceConfigLibrary(index_path=INDEX, source_root=root)
    with pytest.raises(Original35ExecutionError) as exc:
        execute_native_compiler_source(
            "SRC09", library=library, source_root=root,
            host="local-d", purpose="ORIGINAL_RAW_ENGINEERING",
            as_of="2026-11-06")
    assert "CURRENT_SOURCE_READ_DECISION_REQUIRED_BEFORE_IO" in str(exc.value)


@dataclass(frozen=True)
class _FakeDecision:
    decision_ref: str
    host: str


class _SequenceResolver:
    def __init__(self, decisions):
        self.decisions = list(decisions)

    def resolve_current(self, request):
        return self.decisions.pop(0)


def test_recording_resolver_binds_actual_decode_decision_not_extra_precall():
    # G sequence A,B,B,A previously had an extra wrapper pre-call A. After the
    # repair the recorded calls are decode-B, decode-post-B, consumer-A.
    a = _FakeDecision("A", "host-a")
    b = _FakeDecision("B", "host-b")
    recording = _RecordingResolver(_SequenceResolver((b, b, a)))
    assert recording.resolve_current(None) is b
    assert recording.resolve_current(None) is b
    assert recording.resolve_current(None) is a
    assert recording.captured[0] == asdict(b)
    assert recording.captured[-1] == asdict(a)
    assert recording.captured[0] != recording.captured[-1]

    same = _RecordingResolver(_SequenceResolver((a, a, a)))
    for _ in range(3):
        same.resolve_current(None)
    assert same.captured[0] == same.captured[-1]


def test_governed_facts_queries_become_exact_cold_e_envelopes(tmp_path):
    bundle, _rows = _frontier_bundle(tmp_path / "e_transport.sav")
    config = _fixture_config(bundle)
    plan = build_original35_operation_plan(
        [config], source_presence={"SRC01": True}, require_all35=False)
    compilation = bind_governed_frontier(
        plan, bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    result = execute_governed_frontier(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream)
    no_permission_root = tmp_path / "no_permission"
    with pytest.raises(Original35ExecutionError):
        write_field_forge_envelopes(
            result, source_id="SRC01", state_root=no_permission_root,
            producer_permission_ceiling=None)
    with pytest.raises(Original35ExecutionError):
        write_field_forge_envelopes(
            result, source_id="SRC01", state_root=no_permission_root,
            producer_permission_ceiling=())
    assert not list(no_permission_root.glob("*.field_forge_envelopes.json"))

    ceiling = ("FIELD_FORGE_RELATION_PRODUCTION",)
    summary = write_field_forge_envelopes(
        result, source_id="SRC01", state_root=tmp_path,
        producer_permission_ceiling=ceiling)
    assert summary["fact_count"] == summary["envelope_count"] == 30
    document = json.loads(Path(summary["path"]).read_text())
    assert document["schema"] == "PRE553_ORIGINAL35_E_TRANSPORT@1.0.0"
    assert document["raw_respondent_rows_included"] is False
    assert all(tuple(envelope["permissions"]["producer_permission_ceiling"])
               == ceiling for envelope in document["envelopes"])
    arities = Counter(
        envelope["query"]["semantic_fields"]["target_arity_and_topology"]["arity"]
        for envelope in document["envelopes"])
    assert arities == {1: 30}
    responses = [ingest_envelope(envelope) for envelope in document["envelopes"]]
    assert Counter((response["state"], response["refusal_code"])
                   for response in responses) == {
        ("TYPED_REFUSAL", "FIELD_FORGE_TWO_TARGET_RELATION_REQUIRED"): 30}
    assert all(response["structural_grant"] is False for response in responses)
    envelope_path = tmp_path / "first_envelope.json"
    envelope_path.write_text(json.dumps(document["envelopes"][0], sort_keys=True))
    run = subprocess.run(
        [sys.executable, "-B", "-m",
         "rawlsing_next.pre553_field_forge_empirical_ingress",
         "--envelope", str(envelope_path)],
        cwd=str(REPO),
        env={**os.environ, "PYTHONPATH": str(REPO),
             "PYTHONDONTWRITEBYTECODE": "1"},
        text=True, capture_output=True, timeout=120)
    assert run.returncode == 0, run.stderr[-2000:]
    cold = json.loads(run.stdout)
    assert cold["schema"] == "PRE553_FIELD_FORGE_EMPIRICAL_INGRESS_RESULT@1"
    assert cold["state"] == "TYPED_REFUSAL"
    assert cold["refusal_code"] == "FIELD_FORGE_TWO_TARGET_RELATION_REQUIRED"
    assert cold["structural_grant"] is False

    missing_root = tmp_path / "missing_query"
    missing_root.mkdir(parents=True)
    prior = missing_root / "SRC01.field_forge_envelopes.json"
    prior.write_text("PRIOR_VALID_ARTIFACT\n")
    fake = SimpleNamespace(
        native_execution=SimpleNamespace(native_result=SimpleNamespace(
            empirical_facts=result.native_execution.native_result.empirical_facts,
            executed_queries=())),
        compilation=SimpleNamespace(runtime_catalog=SimpleNamespace(queries=())))
    with pytest.raises(Original35ExecutionError):
        write_field_forge_envelopes(
            fake, source_id="SRC01", state_root=missing_root,
            producer_permission_ceiling=ceiling)
    assert prior.read_text() == "PRIOR_VALID_ARTIFACT\n"
    assert not list(missing_root.glob("*.staged-tmp"))

    broken = json.loads(json.dumps(document))
    broken["envelopes"][0]["permissions"] = {}
    with pytest.raises(Exception):
        ingest_envelope(broken["envelopes"][0])
    broken = json.loads(json.dumps(document))
    broken["envelopes"][0]["replay"]["fact_replay_ref"] = {
        "kind": "WRONG", "object_id": "wrong", "content_hash": "0" * 64}
    with pytest.raises(Exception):
        ingest_envelope(broken["envelopes"][0])


def _asymmetric_bundle(tmp_path):
    rows = []
    for index in range(12):
        a = 0 if index < 6 else 1
        b = 0 if index < 6 else (0 if index < 8 else 1)
        rows.append({"A": float(a), "B": float(b), "G": float(index % 2)})
    path = tmp_path / "asymmetric_joint.sav"
    write_rows(path, rows)
    pkg = package(
        path, len(rows),
        (NativeSourceRule("impl.a", "A"), NativeSourceRule("impl.b", "B")),
        coordinate="G")
    return materialize_native_preimages(
        package=pkg, incidence=decode_sav(path))


def _profile_rows(response):
    assert response["state"] == "CONDITIONAL_SUPPORT_PROFILE"
    return response["profile"]["conditional_count_profile"]


def test_existing_joint_engine_exact_requested_conditional_direction(tmp_path):
    bundle = _asymmetric_bundle(tmp_path)
    config = _fixture_config(bundle)
    plan = build_original35_operation_plan(
        [config], source_presence={"SRC01": True}, require_all35=False)
    f2 = [op for op in plan.operations if op.kind == "F2_CONDITIONAL"]
    ba = next(op for op in f2 if op.source_variable_codes == ("B", "A"))
    ab = next(op for op in f2 if op.source_variable_codes == ("A", "B"))
    ids = [ba.operation_id, ba.operation_id, ab.operation_id, ab.operation_id]
    values = [("0",), ("1",), ("0",), ("1",)]
    results = execute_requested_two_target_joints(
        plan, bundle=bundle, source_id="SRC01",
        requested_operation_ids=ids, requested_conditioner_values=values,
        as_of=AS_OF, host=HOST, purpose=PURPOSE)
    assert [row["status"] for row in results] == ["OK"] * 4
    assert [row["joint_target_order"] for row in results] == [
        [ba.conditioner_item_id, ba.item_ids[0]],
        [ba.conditioner_item_id, ba.item_ids[0]],
        [ab.conditioner_item_id, ab.item_ids[0]],
        [ab.conditioner_item_id, ab.item_ids[0]]]
    assert [row["conditioner_values"] for row in results] == [
        ["0"], ["1"], ["0"], ["1"]]

    ceiling = ("FIELD_FORGE_RELATION_PRODUCTION",)
    summary = write_requested_joint_transport(
        results, source_id="SRC01", state_root=tmp_path,
        producer_permission_ceiling=ceiling)
    consumed = consume_requested_joint_transport(
        summary["path"], producer_permission_ceiling=ceiling)
    rows = consumed["requests"]
    assert [row["status"] for row in rows] == ["OK"] * 4
    assert rows[0]["backing_fact_refs"] == rows[1]["backing_fact_refs"]
    assert rows[0]["backing_query_refs"] == rows[1]["backing_query_refs"]
    assert rows[0]["selections"][0]["selected_result_id"] != (
        rows[1]["selections"][0]["selected_result_id"])
    assert rows[2]["backing_fact_refs"] == rows[3]["backing_fact_refs"]
    assert rows[2]["selections"][0]["selected_result_id"] != (
        rows[3]["selections"][0]["selected_result_id"])

    def selection(row):
        assert len(row["selections"]) == 1
        selected = row["selections"][0]
        return selected["condition_denominator_support"], {
            item["target_state"]: item["joint_support_count"]
            for item in selected["target_counts"]}

    assert selection(rows[0]) == (6, {"0": 6, "1": 0})
    assert selection(rows[1]) == (6, {"0": 2, "1": 4})
    assert selection(rows[2]) == (8, {"0": 6, "1": 2})
    assert selection(rows[3]) == (4, {"0": 0, "1": 4})

    cells = tuple(bundle.physical_stream.iter_cells())
    def changed_cells():
        out = []
        changed = False
        for cell in cells:
            if (not changed and cell.variable_name == "B"
                    and cell.missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE):
                out.append(replace(cell, raw_value=1.0))
                changed = True
            else:
                out.append(cell)
        return tuple(out)
    changed_stream = ExactPhysicalCellStream(
        source_sha256=bundle.source_sha256,
        row_count=bundle.physical_stream.row_count,
        cell_iter_factory=changed_cells)
    changed_bundle = replace(bundle, physical_stream=changed_stream)
    changed_results = execute_requested_two_target_joints(
        plan, bundle=changed_bundle, source_id="SRC01",
        requested_operation_ids=[ba.operation_id, ba.operation_id],
        requested_conditioner_values=[("0",), ("1",)],
        as_of=AS_OF, host=HOST, purpose=PURPOSE)
    changed_summary = write_requested_joint_transport(
        changed_results, source_id="SRC01", state_root=tmp_path,
        producer_permission_ceiling=ceiling)
    changed_rows = consume_requested_joint_transport(
        changed_summary["path"], producer_permission_ceiling=ceiling)["requests"]
    assert selection(changed_rows[0]) == (6, {"0": 5, "1": 1})
    assert selection(changed_rows[1]) == (6, {"0": 2, "1": 4})
    restored_results = execute_requested_two_target_joints(
        plan, bundle=bundle, source_id="SRC01",
        requested_operation_ids=[ba.operation_id, ba.operation_id],
        requested_conditioner_values=[("0",), ("1",)],
        as_of=AS_OF, host=HOST, purpose=PURPOSE)
    restored_summary = write_requested_joint_transport(
        restored_results, source_id="SRC01", state_root=tmp_path,
        producer_permission_ceiling=ceiling)
    restored_rows = consume_requested_joint_transport(
        restored_summary["path"], producer_permission_ceiling=ceiling)["requests"]
    assert selection(restored_rows[0]) == (6, {"0": 6, "1": 0})
    assert selection(restored_rows[1]) == (6, {"0": 2, "1": 4})

    weighted_plan = replace(
        plan, operations=tuple(
            replace(op, measure_kind="GOVERNED_WEIGHTED")
            if op.operation_id == ba.operation_id else op
            for op in plan.operations))
    weighted = execute_requested_two_target_joints(
        weighted_plan, bundle=bundle, source_id="SRC01",
        requested_operation_ids=[ba.operation_id],
        requested_conditioner_values=[("0",)],
        as_of=AS_OF, host=HOST, purpose=PURPOSE)
    assert weighted[0]["status"] == "REFUSED"
    assert "WEIGHTED_REQUEST_NOT_AUTHORIZED" in weighted[0]["code"]

    invalid = execute_requested_two_target_joints(
        plan, bundle=bundle, source_id="SRC01",
        requested_operation_ids=[ba.operation_id],
        requested_conditioner_values=[("9",)],
        as_of=AS_OF, host=HOST, purpose=PURPOSE)
    assert invalid[0]["status"] == "REFUSED"
    assert invalid[0]["code"] == "REQUESTED_CONDITIONER_VALUE_NOT_IN_PLAN"

    unknown = execute_requested_two_target_joints(
        plan, bundle=bundle, source_id="SRC01",
        requested_operation_ids=["missing-operation-id"],
        requested_conditioner_values=[("0",)],
        as_of=AS_OF, host=HOST, purpose=PURPOSE)
    assert unknown[0]["status"] == "REFUSED"
    assert unknown[0]["code"] == "REQUESTED_OPERATION_NOT_IN_PLAN"

    broken = json.loads(Path(summary["path"]).read_text())
    broken["requests"][0]["envelopes"][0]["permissions"] = {}
    broken_path = tmp_path / "broken.json"
    broken_path.write_text(json.dumps(broken))
    with pytest.raises(Exception):
        consume_requested_joint_transport(
            broken_path, producer_permission_ceiling=ceiling)
    broken = json.loads(Path(summary["path"]).read_text())
    broken["requests"][0]["envelopes"][0]["replay"]["fact_replay_ref"] = {
        "kind": "WRONG", "object_id": "wrong", "content_hash": "0" * 64}
    broken_path.write_text(json.dumps(broken))
    with pytest.raises(Exception):
        consume_requested_joint_transport(
            broken_path, producer_permission_ceiling=ceiling)

    for field, value in (
        ("conditioner_ref", {"kind": "WRONG", "object_id": "wrong",
                             "content_hash": "0" * 64}),
        ("target_ref", {"kind": "WRONG", "object_id": "wrong",
                        "content_hash": "0" * 64}),
        ("fact_refs", [{"kind": "WRONG", "object_id": "wrong",
                        "content_hash": "0" * 64}]),
        ("query_refs", [{"kind": "WRONG", "object_id": "wrong",
                         "content_hash": "0" * 64}]),
    ):
        broken = json.loads(Path(summary["path"]).read_text())
        broken["requests"][0][field] = value
        broken_path.write_text(json.dumps(broken))
        with pytest.raises(Original35ExecutionError):
            consume_requested_joint_transport(
                broken_path, producer_permission_ceiling=ceiling)

    for values, code in (
        ([], "REQUESTED_CONDITIONER_VALUES_EMPTY"),
        ([None], "REQUESTED_CONDITIONER_VALUE_NONCANONICAL"),
        (["UNKNOWN"], "REQUESTED_CONDITIONER_VALUE_NOT_IN_PROFILE"),
    ):
        broken = json.loads(Path(summary["path"]).read_text())
        request = broken["requests"][0]
        request["conditioner_values"] = values
        request["request_binding_id"] = semantic_hash({
            "requested_operation_id": request.get("requested_operation_id"),
            "conditioner_item_id": request.get("conditioner_item_id"),
            "target_item_id": request.get("target_item_id"),
            "conditioner_values": values,
            "conditioner_ref": request.get("conditioner_ref"),
            "target_ref": request.get("target_ref"),
            "fact_ref": request["fact_refs"][0],
            "query_ref": request["query_refs"][0],
        })
        broken_path.write_text(json.dumps(broken))
        consumed_broken = consume_requested_joint_transport(
            broken_path, producer_permission_ceiling=ceiling)
        assert consumed_broken["requests"][0]["status"] == "REFUSED"
        assert consumed_broken["requests"][0]["code"] == code
