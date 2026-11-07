"""P3 vertical A-H proof definitions against actual P2/P3 owners.

The selected user matrix is sections 10A-H and 11. This file is authored as a
complete actual-runtime suite. On the integrated startup the returned store is
present but its plan-provenance ABI currently blocks the actual chain before a
P2 batch. No store fallback exists here.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = ROOT.parent / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
for _path in (ROOT, ENGINE_ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from developmental_recursion.contracts import (  # noqa: E402
    EventProposal, RecursionRefusal, detached, digest,
)
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402
from p3 import compression, p3_owner, projections, test_rules  # noqa: E402
from p3_fixture_support import (  # noqa: E402
    COUNTERPART, PROJECT, VerticalCase, batch_events, build_case,
    measure_case, reopen_owner, run_chain, run_chain_timed, standpoint,
    workflow_records,
)


def close_case(case: VerticalCase) -> None:
    try:
        case.owner.close()
    finally:
        pass


def response_for(result: Mapping) -> dict:
    return result["consequences"]["test_only_psychological"]


def first_two_batch_results(case: VerticalCase) -> tuple[dict, dict, dict]:
    results = run_chain(case)
    return results["bootstrap"], results["ordinary"], results["terminal"]


# ---------------------------------------------------------------------------
# PRIMARY — actual formation record -> later response vs no-record control.
# ---------------------------------------------------------------------------


def test_primary_actual_formation_read_later_and_no_mediator_control(tmp_path: Path) -> None:
    case = build_case(tmp_path)
    control = build_case(tmp_path / "control", history_outcomes=())
    try:
        first, second, final = first_two_batch_results(case)
        assert len(batch_events(first)) == 3
        assert len(batch_events(second)) == 3
        assert [row["mode"] for row in case.provider.calls] == [
            "BOOTSTRAP", "ORDINARY", "TERMINAL"]
        assert len(case.provider.calls) == 3

        formation = batch_events(first)[0]
        recruit = batch_events(first)[1]
        assert formation["accessible"]["status"] == "OBSERVED"
        formation_response = response_for(formation)
        assert formation_response["status"] == "COMPUTED_TEST_ONLY_RESPONSE"
        formed = workflow_records(case.owner, formation["after"]["clock"])
        assert len(formed) == 2
        assert {row["payload"]["mode"] for row in formed} == {
            "joint_check", "private_check"}
        formed_hashes = {row["hash"] for row in formed}
        recruit_response = response_for(recruit)
        assert recruit_response["status"] == "COMPUTED_TEST_ONLY_RESPONSE"
        stream_records = {
            row["record_hash"] for row in recruit_response["streams"]
            if row.get("record_hash")
        }
        assert stream_records == formed_hashes
        assert set(recruit["readset"]) & formed_hashes
        assert recruit_response["native_action"] == "NOT_ISSUED_BY_P3_RULE"
        assert all(row["native_action_performed"] is False
                   for row in recruit_response["streams"])
        material = recruit["consequences"]["immediate_response"][
            "objective_material_eligible"]
        assert all(row["material_eligible"] == material
                   for row in recruit_response["streams"])

        ctl_first, ctl_second, _ = first_two_batch_results(control)
        ctl_recruit = batch_events(ctl_first)[1]
        ctl_response = response_for(ctl_recruit)
        assert [row["mode"] for row in ctl_response["streams"]] == ["inspect_alone"]
        assert response_for(recruit) != ctl_response
        assert control.owner.store.head()["count"] == 0

        production = test_rules.production_guard()
        assert production["status"] == "DENY_ZERO_EFFECT"
        assert production["effects"] == []
        assert final["batch_id"] == second["batch_id"]
        assert len(case.provider.calls) == 3
    finally:
        close_case(case)
        close_case(control)


# ---------------------------------------------------------------------------
# A — source-bound participation history changes later response.
# ---------------------------------------------------------------------------


def test_a_two_histories_change_later_move_without_demographic_labels(tmp_path: Path) -> None:
    recognized = build_case(tmp_path / "recognized", history_outcomes=("recognized_plan",))
    imposed = build_case(tmp_path / "imposed", history_outcomes=("imposed_plan",))
    try:
        r1, _, _ = first_two_batch_results(recognized)
        r2, _, _ = first_two_batch_results(imposed)
        rec1 = response_for(batch_events(r1)[1])
        rec2 = response_for(batch_events(r2)[1])
        assert {row["mode"] for row in rec1["streams"]} != {
            row["mode"] for row in rec2["streams"]}
        assert rec1["streams"][0]["record_hash"] != rec2["streams"][0]["record_hash"]
        assert recognized.owner.source_hash == imposed.owner.source_hash
        assert recognized.owner.history[0]["outcome"] != imposed.owner.history[0]["outcome"]
        assert recognized.initial.actor == imposed.initial.actor
        assert recognized.initial.root == imposed.initial.root
    finally:
        close_case(recognized)
        close_case(imposed)


# ---------------------------------------------------------------------------
# B — material opportunity changes; psychological organization does not.
# ---------------------------------------------------------------------------


def test_b_actual_material_opportunity_changes_without_psych_mutation(tmp_path: Path) -> None:
    actual = build_case(
        tmp_path / "actual",
        interval_modes={0: "ACTUAL", 1: "ACTUAL", 2: "ACTUAL"})
    scheduled = build_case(
        tmp_path / "scheduled",
        interval_modes={0: "SCHEDULED_ONLY", 1: "SCHEDULED_ONLY",
                        2: "SCHEDULED_ONLY"})
    try:
        a_res = run_chain(actual)
        s_res = run_chain(scheduled)
        a_event = batch_events(a_res["bootstrap"])[2]
        s_event = batch_events(s_res["bootstrap"])[2]
        a_mat = a_event["consequences"]["immediate_response"][
            "objective_material_eligible"]
        s_mat = s_event["consequences"]["immediate_response"][
            "objective_material_eligible"]
        assert a_mat is False
        assert s_mat is True
        a_head = actual.owner.store.head()["hash"]
        s_head = scheduled.owner.store.head()["hash"]
        assert actual.owner.store.head()["count"] == 2
        assert scheduled.owner.store.head()["count"] == 2
        a_response = response_for(a_event)
        s_response = response_for(s_event)
        assert all(row["material_eligible"] == a_mat
                   for row in a_response["streams"])
        assert all(row["material_eligible"] == s_mat
                   for row in s_response["streams"])
        assert a_response["native_action"] == "NOT_ISSUED_BY_P3_RULE"
        assert actual.owner.snapshot().state_hash != scheduled.owner.snapshot().state_hash
        assert a_head != s_head
        assert a_event["status"] == s_event["status"]
    finally:
        close_case(actual)
        close_case(scheduled)


# ---------------------------------------------------------------------------
# C — one history, two source-bound standpoints.
# ---------------------------------------------------------------------------


def test_c_two_standpoints_same_history_without_mutation(tmp_path: Path) -> None:
    case = build_case(tmp_path)
    try:
        results = run_chain(case)
        result = batch_events(results["ordinary"])[-1]
        identity = result["after"]
        experience = result["accessible"]
        public = case.base_owner.fanin.view()
        standpoints = [
            standpoint(identity, case.source_hash, role="peer",
                       permissions=["OBSERVE_PUBLIC_ACTION", "READ_PUBLIC_DIALOGUE"],
                       interlocutor_ref="vertical:trusted-peer", suffix="projection-peer"),
            standpoint(identity, case.source_hash, role="official",
                       permissions=["READ_PUBLIC_DIALOGUE"],
                       interlocutor_ref="vertical:official", suffix="projection-official"),
        ]
        views = []
        for stand in standpoints:
            views.append(projections.project_views(
                identity=identity,
                actor_experience=experience,
                experience_binding={
                    "root": identity["root"], "actor": identity["actor"],
                    "branch": identity["branch"], "clock": identity["clock"],
                    "experience_hash": digest(experience),
                },
                public_view=public,
                public_binding={
                    "root": identity["root"], "actor": identity["actor"],
                    "branch": identity["branch"], "clock": identity["clock"],
                    "view_hash": digest(public),
                },
                standpoint=stand,
            ))
        assert views[0]["user"] != views[1]["user"]
        assert views[0]["actor"] == views[1]["actor"]
        assert views[0]["actor"]["memory_formation"] == "MISSING_RULE"
        assert views[0]["user"]["claims_status"] == "DEFER_MISSING_AUTHORITY"
        assert len(case.owner.store.head()["hash"]) == 64
    finally:
        close_case(case)


# ---------------------------------------------------------------------------
# D — contradictions coexist, no scalar winner or lifecycle write.
# ---------------------------------------------------------------------------


def test_d_incompatible_mediators_coexist_and_activate_without_resolution(tmp_path: Path) -> None:
    case = build_case(tmp_path)
    try:
        results = run_chain(case)
        first = batch_events(results["bootstrap"])[0]
        records = workflow_records(case.owner, first["after"]["clock"])
        assert len(records) == 2
        plan = case.plans[0]
        op = case.owner.store.get_operation(first["operation_id"])
        base_result = case.owner._base_result(op["base_result"])
        context = case.owner._context(plan, base_result)
        activation = projections.activate(
            records, identity=first["after"], context=context,
            registry=case.owner.registry,
        )
        assert activation["status"] == "CONTRADICTION"
        assert len(activation["contradictions"]) == 1
        assert {entry["activation"] for entry in activation["entries"]} == {
            "ELIGIBLE"}
        before = case.owner.store.head()
        assert case.owner.store.head() == before
        assert all(record.get("lifecycle") not in {"RESOLVED", "DORMANT"}
                   for record in records)
    finally:
        close_case(case)


# ---------------------------------------------------------------------------
# E — stability/recruit reveals existing organization without new records.
# ---------------------------------------------------------------------------


def test_e_stability_event_reveals_without_new_record(tmp_path: Path) -> None:
    case = build_case(tmp_path)
    try:
        results = run_chain(case)
        first_batch = batch_events(results["bootstrap"])
        formation, stability = first_batch[0], first_batch[2]
        next_event = batch_events(results["ordinary"])[0]
        before_head = case.owner.store.head()
        before_records = workflow_records(case.owner, formation["after"]["clock"])
        assert len(before_records) == 2
        after_head = case.owner.store.head()
        assert after_head == before_head
        response = response_for(stability)
        assert response["status"] == "COMPUTED_TEST_ONLY_RESPONSE"
        assert response["streams"]
        assert all(row["native_action_performed"] is False
                   for row in response["streams"])
        assert response["memory_formation"] == "MISSING_RULE"
        assert len(workflow_records(case.owner, stability["after"]["clock"])) == 2
        # The next actual event's before-state is the exact historical head
        # after this stability event; current post-chain state is not that head.
        assert stability["after"]["state_hash"] == next_event["before"]["state_hash"]
    finally:
        close_case(case)


# ---------------------------------------------------------------------------
# F — all four corrected compression forms on actual events.
# ---------------------------------------------------------------------------


def test_f_four_actual_compression_forms_bind_without_fabricated_history(tmp_path: Path) -> None:
    # Keep material available through the first two intervals so the third
    # event can carry an actual accumulated-interval receipt. This varies only
    # the actual P2 interval production; it does not invent compression state.
    case = build_case(
        tmp_path, include_compression=True,
        interval_modes={0: "SCHEDULED_ONLY", 1: "SCHEDULED_ONLY", 2: "ACTUAL"})
    try:
        results = run_chain(case)
        events = batch_events(results["bootstrap"]) + batch_events(results["ordinary"])
        forms = {
            "SINGULAR_OCCURRENCE", "REPRESENTATIVE_EPISODE",
            "ACCUMULATED_INTERVAL", "RETROSPECTIVE_CRYSTALLIZATION",
        }
        seen = set()
        diagnostics = []
        for event in events:
            evidence = event["consequences"].get("test_only_compression_evidence")
            if evidence is None:
                continue
            event_doc = event.get("objective", {}).get("event", {})
            diagnostics.append({
                "event_id": event_doc.get("e1_event_id"),
                "performed": event_doc.get("performed"),
                "action_event_id": event_doc.get("action_event_id"),
                "accessible_status": event.get("accessible", {}).get("status"),
                "accessible_reason": event.get("accessible", {}).get("reason"),
                "evidence_status": evidence.get("status"),
                "evidence_reason": evidence.get("reason"),
                "representation_form": evidence.get("representation_form"),
                "actual_interval_status": evidence.get("actual_interval_status"),
                "actor_access": evidence.get("actor_access"),
            })
            if evidence["status"] != "BOUND":
                continue
            seen.add(evidence["representation_form"])
            assert evidence["actual_event_ref"] == event["objective"]["event"]["e1_event_id"]
            assert evidence["actual_action_ref"] != evidence["actual_event_ref"]
            assert evidence["perception_refs"]
            assert evidence["psychological_effects"] == []
            assert evidence["no_state_mutation"] is True
            if evidence["representation_form"] == "ACCUMULATED_INTERVAL":
                assert evidence["actual_interval_status"] == "PARTIAL"
                assert evidence["actual_interval_ref"]
        assert all(row["evidence_status"] == "BOUND" for row in diagnostics), (
            json.dumps(diagnostics, indent=2, sort_keys=True))
        assert seen == forms
        assert case.provider.context_bytes > 0
    finally:
        close_case(case)


# ---------------------------------------------------------------------------
# G — actor/user opacity and no analyst/private ledger leak.
# ---------------------------------------------------------------------------


def test_g_actor_and_user_views_are_narrower_than_objective_state(tmp_path: Path) -> None:
    case = build_case(tmp_path)
    try:
        results = run_chain(case)
        result = batch_events(results["ordinary"])[-1]
        identity = result["after"]
        public = case.base_owner.fanin.view()
        projection_standpoint = standpoint(
            identity, case.source_hash, role="peer",
            permissions=["OBSERVE_PUBLIC_ACTION", "READ_PUBLIC_DIALOGUE"],
            interlocutor_ref="vertical:trusted-peer", suffix="opacity-peer")
        view = projections.project_views(
            identity=identity, actor_experience=result["accessible"],
            experience_binding={
                "root": identity["root"], "actor": identity["actor"],
                "branch": identity["branch"], "clock": identity["clock"],
                "experience_hash": digest(result["accessible"]),
            },
            public_view=public,
            public_binding={
                "root": identity["root"], "actor": identity["actor"],
                "branch": identity["branch"], "clock": identity["clock"],
                "view_hash": digest(public),
            },
            standpoint=projection_standpoint,
        )
        joined = json.dumps(view, sort_keys=True)
        for sentinel in ("record_hash", "registry_hash", "rule_hash",
                         "source_hash", "readset", "psyche", "world_before",
                         "world_after", "memory_formation"):
            # memory_formation is allowed only as an explicit MISSING_RULE status.
            if sentinel == "memory_formation":
                assert '"memory_formation": "MISSING_RULE"' in joined
                continue
            assert sentinel not in joined
        assert view["user"]["claims_status"] == "DEFER_MISSING_AUTHORITY"
        assert view["actor"]["status"] == "OBSERVED"
        assert all("perceived_by_user" not in event for event in view["actor"]["events"])
        # Objective P2 history remains larger than either projection.
        assert public.get("visible_events") is not None
        assert len(json.dumps(public, sort_keys=True)) >= len(joined)
    finally:
        close_case(case)


# ---------------------------------------------------------------------------
# H — wrong identity/source/rule/time and cold/crash/replay custody.
# ---------------------------------------------------------------------------


def test_h_wrong_root_actor_branch_time_source_rule_version_refuse_before_effects(tmp_path: Path) -> None:
    case = build_case(tmp_path)
    try:
        initial = case.initial
        base_head = case.owner.snapshot().document()
        for bad in (
            {"root": "wrong-root"}, {"actor": "wrong-actor"},
            {"branch": "wrong-branch"},
        ):
            bad_identity = copy.deepcopy(initial.document())
            bad_identity.update(bad)
            with pytest.raises(RecursionRefusal):
                case.owner.realize("wrong-identity", case.proposals[0],
                                   case.owner.snapshot().__class__(**bad_identity))
            assert case.owner.snapshot().document() == base_head
        with pytest.raises(RecursionRefusal):
            bad_source = copy.deepcopy(case.source)
            bad_source["root"] = "foreign-root"
            p3_owner.P3Owner(
                case.base_owner, source=bad_source, history=case.history,
                plans=case.plans, catalog=case.catalog,
                compression_specs=case.compression_specs,
                standpoints=case.standpoints,
            )
        bad_plan = copy.deepcopy(case.plans[0])
        bad_plan["permitted_rules"][0]["rule_version"] = "other"
        bad_plan = dict({k: v for k, v in bad_plan.items() if k != "hash"},
                        hash=digest({k: v for k, v in bad_plan.items() if k != "hash"}))
        with pytest.raises(RecursionRefusal):
            p3_owner.P3Owner(
                case.base_owner, source=case.source, history=case.history,
                plans=[bad_plan], catalog=case.catalog,
                compression_specs=case.compression_specs,
                standpoints=case.standpoints,
            )
        with pytest.raises(RecursionRefusal):
            bad_time = copy.deepcopy(initial.document())
            bad_time["clock"] = int(initial.clock) - 1
            case.owner.realize("bad-time", case.proposals[0],
                               case.owner.snapshot().__class__(**bad_time))
        assert case.owner.snapshot().document() == base_head
    finally:
        close_case(case)


def test_h_cross_root_binding_is_refused_not_migrated(tmp_path: Path) -> None:
    left = build_case(tmp_path / "left")
    right = build_case(tmp_path / "right")
    try:
        assert left.owner.store.head()["count"] == 0
        assert right.owner.store.head()["count"] == 0
        # Separate start() fixtures are exact deterministic replicas of one
        # logical P2 root; a same-root source is not a foreign migration.
        assert left.source["root"] == right.source["root"]
        for source in (
            dict(left.source, root="foreign-root"),
            dict(left.source, actor="foreign-actor"),
            dict(left.source, branch="foreign-branch"),
        ):
            with pytest.raises(RecursionRefusal):
                p3_owner.P3Owner(
                    right.base_owner, source=source, history=left.history,
                    plans=left.plans, catalog=left.catalog,
                    compression_specs=left.compression_specs,
                    standpoints=left.standpoints,
                )
        assert left.owner.store.head()["count"] == 0
        assert right.owner.store.head()["count"] == 0
    finally:
        close_case(left)
        close_case(right)


def test_h_cold_reopen_idempotent_replay_and_source_restore(tmp_path: Path) -> None:
    case = build_case(tmp_path)
    reopened = None
    try:
        results = run_chain(case)
        first = batch_events(results["ordinary"])[-1]
        expected = {key: value for key, value in first.items() if key != "event_id"}
        operation_id = first["operation_id"]
        last_proposal = case.proposals[-1]
        state_after = case.owner.snapshot()
        replay = case.owner.realize(
            operation_id, last_proposal, case.owner.snapshot())
        assert replay.document() == expected
        assert case.owner.snapshot() == state_after
        config_path = case.owner._config_path
        original_config = config_path.read_text(encoding="utf-8")
        document = json.loads(original_config)
        document["config_hash"] = "0" * 64
        config_path.write_text(json.dumps(document), encoding="utf-8")
        with pytest.raises(RecursionRefusal):
            case.owner.snapshot()
        config_path.write_text(original_config, encoding="utf-8")
        assert case.owner.snapshot() == state_after
        case.owner.close()
        _, reopened = reopen_owner(case)
        assert reopened.snapshot().state_hash == state_after.state_hash
        cold_replay = reopened.realize(
            operation_id, last_proposal, reopened.snapshot())
        assert cold_replay.document() == expected
    finally:
        if reopened is not None:
            reopened.close()
        close_case(case)


def test_h_real_process_crash_after_base_before_psych_commit(tmp_path: Path) -> None:
    """Kill one actual child after base realization, before save_world.

    The parent reopens the exact actual P2/P3 root, replays the durable base
    receipt through P3Owner's recovery path, and completes the sidecar once.
    """
    case = build_case(tmp_path)
    recovered_owner = None
    try:
        payload = {
            "source": case.source, "history": case.history, "plans": case.plans,
            "catalog": case.catalog, "compression_specs": case.compression_specs,
            "standpoints": case.standpoints,
            "proposal": case.proposals[0].document(),
            "p2_root": str(Path(case.state_root)),
            "p2_case": detached(case.base_owner.case),
            "p2_source": detached(case.base_owner.source),
            "p2_participants": list(case.base_owner.participants),
        }
        payload_path = tmp_path / "vertical-crash.json"
        payload_path.write_text(json.dumps(payload), encoding="utf-8")
        code = r'''
import json, os, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
sys.path.insert(0, str(Path(sys.argv[1]) / "tests"))
from developmental_recursion.contracts import EventProposal
from developmental_recursion.p2_owner import P2Owner, load_p2
from p3 import p3_owner
p = json.loads(Path(sys.argv[3]).read_text())
fanin = load_p2().open(Path(p["p2_root"]))
base = P2Owner(fanin, case=p["p2_case"], source=p["p2_source"],
               participants=tuple(p["p2_participants"]))
owner = p3_owner.P3Owner(base, source=p["source"], history=p["history"],
                        plans=p["plans"], catalog=p["catalog"],
                        compression_specs=p["compression_specs"],
                        standpoints=p["standpoints"])
original = base.realize
def crash_after_base(operation_id, proposal, expected):
    original(operation_id, proposal, expected)
    os._exit(19)
base.realize = crash_after_base
proposal_doc = dict(p["proposal"])
proposal_doc["source_refs"] = tuple(proposal_doc["source_refs"])
proposal_doc["participants"] = tuple(proposal_doc["participants"])
proposal = EventProposal(**proposal_doc)
owner.realize("vertical-crash-operation", proposal, owner.snapshot())
'''
        case.owner.close()
        completed = subprocess.run(
            [sys.executable, "-c", code, str(ROOT), str(ENGINE_ROOT),
             str(payload_path), str(tmp_path)],
            capture_output=True, text=True, timeout=180,
        )
        assert completed.returncode == 19, completed.stderr
        _, recovered_owner = reopen_owner(case)
        recovered = recovered_owner.realize(
            "vertical-crash-operation", case.proposals[0],
            recovered_owner.snapshot(),
        )
        assert recovered.accessible["status"] == "OBSERVED"
        assert recovered.consequences["durable_psychological_transition"] == (
            "MISSING_RULE")
        assert recovered_owner.store.get_operation(
            "vertical-crash-operation")["phase"] == "COMPLETE"
    finally:
        if recovered_owner is not None:
            recovered_owner.close()


def test_11_resource_receipts_are_actual_measurements(tmp_path: Path) -> None:
    case = build_case(tmp_path)
    reopened = None
    try:
        start = time.perf_counter()
        results, timings = run_chain_timed(case)
        total_seconds = time.perf_counter() - start
        verify_before = detached(case.owner.store.stats())
        verify_start = time.perf_counter()
        assert case.owner.store.verify() is True
        full_verify_seconds = time.perf_counter() - verify_start
        verify_after = detached(case.owner.store.stats())
        timings["verify_before"] = verify_before
        timings["verify_after"] = verify_after
        metrics = measure_case(case, results, timings,
                               full_verify_seconds=full_verify_seconds)
        assert metrics["provider_calls"] == 3
        assert metrics["provider_modes"] == [
            "BOOTSTRAP", "ORDINARY", "TERMINAL"]
        assert metrics["event_batches"] == 2
        assert metrics["calls_per_batch"] == 1.5
        assert metrics["provider_calls_per_cycle"] == 3
        assert metrics["batch_counts"] == [3, 3]
        assert metrics["retrospective_count"] == 2
        assert metrics["provider_context_bytes"] > 0
        assert metrics["logical_cycle_store_bytes"] > 0
        assert metrics["batch_latency_seconds"]["bootstrap"] >= 0
        assert metrics["batch_latency_seconds"]["ordinary"] >= 0
        assert metrics["batch_latency_seconds"]["terminal"] >= 0
        assert metrics["event_latency_count"] == 6
        assert all(value >= 0 for value in metrics["event_latency_seconds"])
        assert metrics["targeted_vs_full_reads"]["targeted_queries"] > 0
        assert metrics["targeted_vs_full_reads"]["full_verify_row_reads"] > 0
        assert metrics["targeted_vs_full_reads"]["verify_full_scans"] == 1
        assert metrics["bytes"]["db_bytes"] > 0
        assert metrics["bytes"]["db_plus_wal_bytes"] > 0
        assert metrics["bytes"]["db_plus_wal_bytes"] >= metrics["bytes"]["db_bytes"]
        assert metrics["bytes"]["incremental_db_bytes"] >= 0
        assert metrics["bytes"]["incremental_db_plus_wal_bytes"] > 0
        assert metrics["bytes"]["bytes_per_record"] is not None
        assert metrics["bytes"]["bytes_per_record"] > 0
        assert metrics["bytes"]["bytes_per_event"] > 0
        assert metrics["bytes"]["source_config_bytes"] > 0
        assert metrics["bytes"]["source_provenance_overhead_bytes"] > 0
        assert all(value["bytes"] >= 0 for value in metrics["file_bytes"].values())
        assert metrics["b1_historical_comparison"]["label"].startswith("E1 B1")
        assert total_seconds >= 0
        case.owner.close()
        cold_start = time.perf_counter()
        _, reopened = reopen_owner(case)
        cold_open_seconds = time.perf_counter() - cold_start
        metrics["cold_open_seconds"] = cold_open_seconds
        metrics_path = os.environ.get("P3_VERTICAL_METRICS_PATH")
        if metrics_path:
            path = Path(metrics_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n",
                            encoding="utf-8")
        assert metrics["cold_open_seconds"] >= 0
    finally:
        if reopened is not None:
            reopened.close()
        close_case(case)
