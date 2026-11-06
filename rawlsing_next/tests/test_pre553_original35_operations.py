"""Bound original35 operation adapter and current-compiler consumer tests."""
from __future__ import annotations

from dataclasses import replace
from functools import lru_cache
import hashlib
import json
import subprocess
import time
from pathlib import Path

import pytest

from rawlsing_next.pre553_original35_operations import (
    EXECUTABLE, DEFERRED, HELD, INAPPLICABLE, OPERATION_F1, OPERATION_F2,
    OPERATION_F3H, OPERATION_F3R, OPERATION_F4, SOURCE_PRESENT,
    Original35OperationError, account_all35_frontiers, bind_governed_frontier,
    build_frontier_inputs_from_plan, build_original35_operation_plan,
    execute_plan_universal,
)
from rawlsing_next.tests.test_universal_source_projection import (
    build_s3, s3_rows,
)
from rawlsing_next.tests.test_universal_workload import (
    AS_OF, HOST, PURPOSE, _frontier_bundle, _frontier_fixture,
)
from rawlsing_next.pre553_universal_workload import execute_governed_frontier

R157 = "1924499ef52403a0f331b8aff9b7c7eff99bf1e2"
CUSTODY = "b90708f7d79624faae3da2408932829e569e5ae2"
CUSTODY_PATH = ("WORKER_COMMISSIONS/PROGRAMMA_PYAT_UNIVERSAL35_20261106_R1/"
                "01_LOCAL_SOURCE_CUSTODY_OBSERVATION.json")
EXPECTED_ITEMS = 18276
EXPECTED_SLOTS = 18413


def _git_show(object_name: str) -> str:
    return subprocess.check_output(
        ["git", "show", object_name], text=True, timeout=120)


@lru_cache(maxsize=1)
def _packs():
    names = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", R157,
         "rawlsing_next/source_configuration/data"],
        text=True, timeout=120).splitlines()
    docs = []
    for name in names:
        if not name.endswith(".config.json") or "fixture" in name:
            continue
        docs.append(json.loads(_git_show(f"{R157}:{name}")))
    return tuple(docs)


@lru_cache(maxsize=1)
def _presence():
    custody = json.loads(_git_show(f"{CUSTODY}:{CUSTODY_PATH}"))
    return {row["source_id"]: {
        "present": True,
        "presence_grade": row["presence_grade"],
        "source_sha256": row["source_sha256"],
    } for row in custody["rows"]}


def _fixture_config(bundle, source_id="SRC01"):
    codes = sorted(bundle.question_refs)
    response_slots = []
    items = []
    for ordinal, code in enumerate(codes, start=1):
        qref = bundle.question_refs[code]
        values = []
        for slot in bundle.projection.response_slots:
            if slot.question_binding.native_question_ref != qref:
                continue
            for rule in slot.values:
                if (rule.response_state == "SUBSTANTIVE_RESPONSE"
                        and rule.canonical_value is not None):
                    values.append({
                        "raw_value": rule.canonical_value,
                        "missing_state": "OBSERVED_STORAGE_VALUE",
                        "response_state": "SUBSTANTIVE_RESPONSE",
                        "canonical_value": str(rule.canonical_value),
                    })
        if not values:
            continue
        response_slots.append({"slot": {"ordinal": ordinal, "name": code},
                               "question_id": code, "values": values})
        items.append({
            "implementation_id": "fixture." + code,
            "source_variable_code": code,
            "exact_identity_sha256": hashlib.sha256(code.encode()).hexdigest(),
            "question_text": code,
            "disposition": "SUPPORTED_SOURCE_NATIVE_RESPONSE",
            "response_classes": "fixture",
            "mapping_status": "accepted",
            "authority_status": "TEST_ONLY",
            "evidence_refs": [],
            "limits": [],
            "relation": {"manual_response_topology": "scalar"},
        })
    return {
        "schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
        "config_id": "fixture-" + source_id,
        "config_revision": 1,
        "config_purpose": "SOURCE_PREPARATION",
        "identity": {
            "source_id": source_id, "family": "fixture", "wave": "W1",
            "source_family_id": "fixture", "study_product_id": "fixture",
            "release_id": "fixture", "instrument_release_id": "fixture",
            "source_artifact_id": "fixture.sav",
            "expected_source_sha256": bundle.source_sha256,
            "source_row_count": bundle.physical_stream.row_count,
            "source_format": "SAV", "source_column_count": len(codes),
            "source_bytes": 1, "codebook_rows": len(codes),
            "original_item_count": len(items),
        },
        "binding": {
            "identity_class": "ORIGINAL_SOURCE",
            "source_sha256": bundle.source_sha256,
            "row_count": bundle.physical_stream.row_count,
        },
        "respondents": {"subject_unit": "SOURCE_INTERVIEW_ROW"},
        "supported_scope": {"supported_form_slice": "SINGLE_SAV_FILE_NO_FORM_VARIABLE_EVIDENCE"},
        "items": items, "physical_slots": [
            {"ordinal": index} for index in range(1, len(items) + 1)
        ], "response_slots": response_slots, "coordinate_slots": [],
        "weight_slots": [], "routing": [
            {"question_id": code, "typed_state": "ELIGIBLE_APPLICABLE"}
            for code in codes
        ],
    }


def test_all35_no_drop_plan_accounts_every_original_item_and_slot():
    started = time.time()
    plan = build_original35_operation_plan(
        _packs(), source_presence=_presence(), require_all35=True,
        expected_item_count=EXPECTED_ITEMS,
        expected_physical_slot_count=EXPECTED_SLOTS)
    elapsed = time.time() - started
    assert len(plan.rows) == 35
    assert plan.item_count == EXPECTED_ITEMS
    assert plan.physical_slot_count == EXPECTED_SLOTS
    assert plan.no_drop_ok is True
    assert set(plan.counts) == {
        EXECUTABLE, HELD, "ABSTAIN", INAPPLICABLE, DEFERRED, "NOT_REQUESTED"}
    assert sum(plan.counts.values()) == len(plan.operations)
    assert plan.counts[EXECUTABLE] > 0
    assert plan.counts[HELD] > 0
    assert plan.pair_selected < plan.pair_candidates
    assert plan.joint_selected < plan.joint_candidates
    assert all(row.source_presence == "LOCAL_BYTES_PRESENT_EXACT_SHA"
               for row in plan.rows)
    assert all(row.item_ids and row.physical_slots for row in plan.rows)
    assert any(op.unit == "household" for op in plan.operations)
    assert any(op.topology not in {"SCALAR_SINGULAR", "scalar"}
               for op in plan.operations)
    kinds = {op.kind for op in plan.operations}
    assert {OPERATION_F1, OPERATION_F2, OPERATION_F3H,
            OPERATION_F3R, OPERATION_F4} <= kinds
    triples = [op for op in plan.operations
               if op.kind == OPERATION_F4 and op.joint_arity >= 3]
    assert triples
    both = {(op.item_ids[0], op.conditioner_item_id) for op in plan.operations
            if op.kind == OPERATION_F2}
    assert any((a, b) in both and (b, a) in both for a, b in both if a != b)
    again = build_original35_operation_plan(
        _packs(), source_presence=_presence(), require_all35=True)
    assert again.plan_ref == plan.plan_ref
    # Bounded whole-estate construction; broad but finite.
    accounting = account_all35_frontiers(plan)
    assert accounting["sources"] == 35
    assert (accounting["explicit_frontier_sources"]
            + accounting["no_explicit_request_sources"]) == 35
    assert accounting["no_explicit_request_sources"] == 15
    assert accounting["frontier_operation_count"] > 0
    assert elapsed < 60


def test_missing_optional_weight_does_not_hold_raw_and_missing_slot_holds_only_dependent():
    docs = {doc["identity"]["source_id"]: doc for doc in _packs()}
    weighted = json.loads(json.dumps(docs["SRC01"]))
    weighted["weight_slots"] = []
    plan = build_original35_operation_plan(
        [weighted], source_presence={"SRC01": True}, require_all35=False)
    assert plan.rows[0].weight_status == "ABSENT_OPTIONAL_RAW_SUPPORTED"
    assert plan.counts[EXECUTABLE] > 0
    assert not any(op.measure_kind == "GOVERNED_WEIGHTED"
                   for op in plan.operations)

    source = json.loads(json.dumps(docs["SRC31"]))
    question = source["response_slots"][0]["question_id"]
    before = build_original35_operation_plan(
        [source], source_presence={"SRC31": True}, require_all35=False)
    source["response_slots"] = [
        row for row in source["response_slots"]
        if row["question_id"] != question]
    after = build_original35_operation_plan(
        [source], source_presence={"SRC31": True}, require_all35=False)
    assert after.counts[HELD] > before.counts[HELD]
    assert after.counts[EXECUTABLE] < before.counts[EXECUTABLE]
    assert after.no_drop_ok is True


def test_terminal_current_universal_consumer_executes_and_restores(tmp_path):
    path = tmp_path / "s35.sav"
    bundle = build_s3(path, s3_rows(respondents=6, occasions=2))
    config = _fixture_config(bundle)
    plan = build_original35_operation_plan(
        [config], source_presence={"SRC01": True}, require_all35=False)
    lowering, result = execute_plan_universal(
        plan, bundle=bundle, source_factory=lambda _ref: bundle.physical_stream,
        as_of=AS_OF, host=HOST, purpose=PURPOSE)
    assert lowering.no_drop_ok is True
    assert result.anti_join()["no_drop_ok"] is True
    assert result.executed_operation_ids
    assert result.fact_refs
    good_facts = result.fact_refs

    from dataclasses import replace
    bad_stream = replace(bundle.physical_stream, source_sha256="b" * 64)
    with pytest.raises(Original35OperationError):
        execute_plan_universal(
            plan, bundle=bundle, source_factory=lambda _ref: bad_stream,
            as_of=AS_OF, host=HOST, purpose=PURPOSE)
    restored, restored_result = execute_plan_universal(
        plan, bundle=bundle, source_factory=lambda _ref: bundle.physical_stream,
        as_of=AS_OF, host=HOST, purpose=PURPOSE)
    assert restored.no_drop_ok is True
    assert restored_result.fact_refs == good_facts


def test_terminal_current_governed_frontier_joint_consumer(tmp_path):
    bundle, _rows = _frontier_bundle(tmp_path / "s35_frontier.sav")
    config = _fixture_config(bundle)
    plan = build_original35_operation_plan(
        [config], source_presence={"SRC01": True}, require_all35=False)
    compilation = bind_governed_frontier(
        plan, bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    result = execute_governed_frontier(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream)
    assert result.anti_join["no_drop_ok"] is True
    assert result.operation_anti_join["no_drop_ok"] is True
    assert result.fact_refs
    assert any(record.status == "SUPPORTED"
               for record in compilation.plan.records)


def test_plan_refuses_incomplete_roster_and_wrong_expected_counts():
    docs = _packs()[:34]
    with pytest.raises(Original35OperationError):
        build_original35_operation_plan(
            list(docs), source_presence=_presence(), require_all35=True)
    with pytest.raises(Original35OperationError):
        build_original35_operation_plan(
            _packs(), source_presence=_presence(), require_all35=True,
            expected_item_count=1)


def test_governed_binding_actual_payload_change_severs_and_restores(tmp_path):
    bundle, _rows = _frontier_bundle(tmp_path / "s35_payload.sav")
    config = _fixture_config(bundle)
    plan = build_original35_operation_plan(
        [config], source_presence={"SRC01": True}, require_all35=False)
    baseline = bind_governed_frontier(
        plan, bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    assert baseline.content_hash
    assert baseline.expected_candidate_ids

    with pytest.raises(Original35OperationError):
        bind_governed_frontier(
            replace(plan, operations=()), bundle=bundle,
            as_of=AS_OF, host=HOST, purpose=PURPOSE)

    f2 = next(op for op in plan.operations
              if op.kind == OPERATION_F2 and op.status == EXECUTABLE
              and op.conditioner_item_id)
    conditioner_code = f2.source_variable_codes[1]
    changed = tuple(
        replace(op, response_values=tuple(sorted(set(op.response_values) | {"9"})))
        if op.kind == OPERATION_F1 and op.source_variable_codes[0] == conditioner_code
        else replace(op, conditioner_values=("9",))
        if op is f2
        else op
        for op in plan.operations)
    changed_plan = replace(plan, operations=changed)
    changed_compilation = bind_governed_frontier(
        changed_plan, bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    assert changed_compilation.content_hash != baseline.content_hash
    assert changed_compilation.issued.record.expected_jobs != (
        baseline.issued.record.expected_jobs)
    restored = bind_governed_frontier(
        plan, bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    assert restored.content_hash == baseline.content_hash


def test_original_id_identity_refusals_and_route_unknown_not_administered(tmp_path):
    bundle, _ = _frontier_bundle(tmp_path / "s35_identity.sav")
    config = _fixture_config(bundle)
    plan = build_original35_operation_plan(
        [config], source_presence={"SRC01": True}, require_all35=False)
    baseline = bind_governed_frontier(
        plan, bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    f2 = next(op for op in plan.operations
              if op.kind == OPERATION_F2 and op.conditioner_item_id)

    conflict = tuple(
        replace(op, item_ids=(op.item_ids[0] + "-WRONG",) + op.item_ids[1:])
        if op is f2 else op for op in plan.operations)
    with pytest.raises(Original35OperationError):
        bind_governed_frontier(
            replace(plan, operations=conflict), bundle=bundle,
            as_of=AS_OF, host=HOST, purpose=PURPOSE)

    missing = tuple(
        replace(op, item_ids=("",) + op.item_ids[1:]) if op is f2 else op
        for op in plan.operations)
    with pytest.raises(Original35OperationError):
        bind_governed_frontier(
            replace(plan, operations=missing), bundle=bundle,
            as_of=AS_OF, host=HOST, purpose=PURPOSE)

    wrong_code = tuple(
        replace(op, source_variable_codes=(op.source_variable_codes[0],
                                           "NOT_A_PHYSICAL_CODE")
                + op.source_variable_codes[2:])
        if op is f2 else op for op in plan.operations)
    with pytest.raises(Original35OperationError):
        bind_governed_frontier(
            replace(plan, operations=wrong_code), bundle=bundle,
            as_of=AS_OF, host=HOST, purpose=PURPOSE)

    restored = bind_governed_frontier(
        plan, bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    assert restored.content_hash == baseline.content_hash

    unknown_config = _fixture_config(bundle)
    unknown_config["routing"][0]["typed_state"] = "ROUTING_UNKNOWN"
    unknown_plan = build_original35_operation_plan(
        [unknown_config], source_presence={"SRC01": True}, require_all35=False)
    inventory, _policy, frontier = build_frontier_inputs_from_plan(
        unknown_plan, source_id="SRC01")
    code = next(op.source_variable_codes[0] for op in unknown_plan.operations
                if op.kind == OPERATION_F1 and op.route_status == "ROUTING_UNKNOWN")
    original_id = next(item_id for item_id, physical in zip(
        next(op for op in unknown_plan.operations
             if op.kind == OPERATION_F1 and op.source_variable_codes[0] == code).item_ids,
        next(op for op in unknown_plan.operations
             if op.kind == OPERATION_F1 and op.source_variable_codes[0] == code).source_variable_codes))
    occurrence = next(o for o in inventory.occurrences
                      if o.key.item_id == original_id)
    assert occurrence.administration == "UNKNOWN"
    assert occurrence.route_state == "UNKNOWN"
    assert all(not (op.targets and op.targets[0].item_id == original_id
                    and op.disposition == "ELIGIBLE")
               for op in frontier.operations)


def test_supplied_frontier_must_be_exact_plan_derived_no_extras(tmp_path):
    bundle, _ = _frontier_bundle(tmp_path / "s35_exact_frontier.sav")
    config = _fixture_config(bundle)
    plan = build_original35_operation_plan(
        [config], source_presence={"SRC01": True}, require_all35=False)
    inventory, policy, frontier = build_frontier_inputs_from_plan(
        plan, source_id="SRC01")
    baseline = bind_governed_frontier(
        plan, bundle=bundle, inventory=inventory, policy=policy,
        frontier=frontier, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    assert baseline.content_hash

    extra = replace(frontier, operations=frontier.operations + (frontier.operations[0],))
    with pytest.raises(Original35OperationError):
        bind_governed_frontier(
            plan, bundle=bundle, inventory=inventory, policy=policy,
            frontier=extra, as_of=AS_OF, host=HOST, purpose=PURPOSE)

    substituted = replace(
        frontier, operations=(replace(frontier.operations[0], disposition="HELD",
                                      reasons=("SUBSTITUTED",)),)
        + frontier.operations[1:])
    with pytest.raises(Original35OperationError):
        bind_governed_frontier(
            plan, bundle=bundle, inventory=inventory, policy=policy,
            frontier=substituted, as_of=AS_OF, host=HOST, purpose=PURPOSE)

    missing = replace(frontier, operations=frontier.operations[:-1])
    with pytest.raises(Original35OperationError):
        bind_governed_frontier(
            plan, bundle=bundle, inventory=inventory, policy=policy,
            frontier=missing, as_of=AS_OF, host=HOST, purpose=PURPOSE)

    restored = bind_governed_frontier(
        plan, bundle=bundle, inventory=inventory, policy=policy,
        frontier=frontier, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    assert restored.content_hash == baseline.content_hash
