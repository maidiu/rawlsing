"""P3 owner integration tests.

The durable normalized store is an independently assigned dependency. When the
returned ``p3.state_store`` is absent these integration checks are explicitly
skipped, not replaced with a fake store or an in-memory fallback. The negative
mode test does not need a store and always executes.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from p3 import p3_owner
from p3 import test_rules
from developmental_recursion.contracts import (
    EventProposal,
    RecursionRefusal,
    detached,
    digest,
)
from developmental_recursion.p2_owner import P2Owner, load_p2


def _store_available() -> bool:
    try:
        import p3.state_store  # noqa: F401
    except Exception:
        return False
    return True


STORE_BLOCK = "DEPENDENT_EXECUTION_NOT_RUN_MISSING_RETURNED_STATE_STORE"
requires_store = pytest.mark.skipif(not _store_available(), reason=STORE_BLOCK)


def seal(body):
    return dict(detached(body), hash=digest(body))


def _actual_base(tmp_path: Path):
    fanin = load_p2().start(tmp_path / "actual-p2")
    case = fanin.deps["case_for"](True)
    owner = P2Owner(
        fanin,
        case=case,
        source=fanin.deps["source_for"](case),
        participants=tuple(fanin.session.read_root()["actor_ids"]),
    )
    return fanin, owner


def _source(owner, initial, base_ref=None):
    body = {
        "grade": test_rules.GRADE,
        "root": initial.root,
        "actor": initial.actor,
        "branch": initial.branch,
        "source_ref": base_ref or owner.source_ref,
        "base_source_ref": base_ref or owner.source_ref,
        "purpose": "P3 owner integration test, sourcefree only",
    }
    return body


def _history(initial, source_hash):
    rows = []
    for index, outcome in enumerate(("recognized_plan", "imposed_plan")):
        row = {key: getattr(initial, key) for key in ("root", "actor", "branch")}
        row.update(
            grade=test_rules.GRADE,
            source_hash=source_hash,
            episode_id="owner-history-" + str(index),
            project="owner-plan-comparison",
            counterpart="owner-counterpart",
            time=initial.clock - 3 + index,
            activity="compare_plans_in_task",
            outcome=outcome,
            parent_refs=[rows[-1]["hash"]] if rows else [],
        )
        rows.append(seal(row))
    return rows


def _plan(initial, proposal, source_hash, phase="FORMATION", counterpart=None,
          project="owner-plan-comparison"):
    body = {key: getattr(initial, key) for key in ("root", "actor", "branch")}
    body.update(
        grade=test_rules.GRADE,
        source_hash=source_hash,
        registry_hash=test_rules.make_registry(source_hash)["hash"],
        proposal_hash=digest(proposal.document()),
        event_id=proposal.event_id,
        permitted_rules=test_rules.rule_descriptors(),
        phase=phase,
        project=project,
        counterpart=counterpart or "owner-counterpart",
        activation_roles=["peer"],
        relation_refs=["owner-collaboration"],
        obligation_refs=[],
        interlocutor_role="peer",
    )
    return seal(body)


def _standpoint(initial, source_hash):
    body = {key: getattr(initial, key) for key in ("root", "actor", "branch", "clock")}
    body.update(
        interlocutor_ref="owner-observer",
        role="observer",
        permissions=["OBSERVE_PUBLIC_ACTION", "READ_PUBLIC_DIALOGUE"],
        source_refs=[source_hash],
        grade=test_rules.GRADE,
    )
    return seal(body)


def _build(tmp_path: Path, *, history=True, phase="FORMATION"):
    fanin, owner = _actual_base(tmp_path)
    initial = owner.snapshot()
    source = _source(owner, initial)
    source_hash = digest(source)
    history_rows = _history(initial, source_hash) if history else []
    proposal = EventProposal(
        "owner-event-" + phase.lower(), initial.clock + 6, "ADMIT_EVENT",
        (owner.source_ref,), owner.participants, {},
    )
    plan = _plan(initial, proposal, source_hash, phase=phase)
    config = {
        "source": source,
        "history": history_rows,
        "plans": [plan],
        "standpoints": [_standpoint(initial, source_hash)],
    }
    return fanin, owner, initial, source_hash, config, proposal


def test_non_test_only_refuses_before_base_or_store_access():
    with pytest.raises(RecursionRefusal, match="P3_MODE_REFUSED_BEFORE_WRITES"):
        p3_owner.P3Owner(
            None, source={"grade": test_rules.GRADE}, history=[], plans=[],
            mode="PRODUCTION",
        )


def test_missing_returned_store_is_explicit_not_a_fallback():
    if _store_available():
        pytest.skip("returned state store is present")
    with pytest.raises(RecursionRefusal, match=STORE_BLOCK):
        p3_owner._store_class()


def _child_roots() -> tuple[Path, Path, Path]:
    return (
        Path(__file__).resolve().parents[1],
        Path(__file__).resolve().parents[2] / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1",
        Path(__file__).resolve().parents[3],
    )


def _child_environment() -> dict:
    p3_root, engine_root, repo_root = _child_roots()
    environment = dict(os.environ)
    inherited = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = os.pathsep.join(
        [str(p3_root), str(engine_root), str(repo_root)]
        + ([inherited] if inherited else []))
    return environment


def test_process_reopens_same_actual_p2_root(tmp_path):
    fanin, owner = _actual_base(tmp_path)
    root_hash = fanin.session.read_root()["root_hash"]
    initial_state = owner.snapshot().document()
    owner.close()
    payload = tmp_path / "owner-root-payload.json"
    payload.write_text(json.dumps({"root_hash": root_hash,
                                   "initial_state": initial_state}), encoding="utf-8")
    p3_root, engine_root, repo_root = _child_roots()
    code = r'''
import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
from developmental_recursion.p2_owner import P2Owner, load_p2
root = Path(sys.argv[3]).resolve()
p = json.loads(Path(sys.argv[4]).read_text())
fanin = load_p2().open(root / "actual-p2")
assert Path(fanin.session.state_root).resolve() == (root / "actual-p2").resolve()
assert fanin.session.read_root()["root_hash"] == p["root_hash"]
case = fanin.deps["case_for"](True)
base = P2Owner(fanin, case=case, source=fanin.deps["source_for"](case),
               participants=tuple(fanin.session.read_root()["actor_ids"]))
assert base.snapshot().document() == p["initial_state"]
base.close()
'''
    completed = subprocess.run(
        [sys.executable, "-c", code, str(p3_root), str(engine_root),
         str(tmp_path), str(payload)],
        env=_child_environment(), capture_output=True, text=True, timeout=120,
    )
    assert completed.returncode == 0, completed.stderr
    fanin2 = load_p2().open(tmp_path / "actual-p2")
    case2 = fanin2.deps["case_for"](True)
    base2 = P2Owner(fanin2, case=case2, source=fanin2.deps["source_for"](case2),
                    participants=tuple(fanin2.session.read_root()["actor_ids"]))
    try:
        assert fanin2.session.read_root()["root_hash"] == root_hash
        assert base2.snapshot().document() == initial_state
    finally:
        base2.close()


@requires_store
def test_actual_p2_root_configuration_and_combined_statehash(tmp_path):
    fanin, owner, initial, source_hash, config, _proposal = _build(tmp_path)
    p3 = p3_owner.P3Owner(owner, **config)
    try:
        base = owner.snapshot()
        snapshot = p3.snapshot()
        assert p3.base_owner is owner
        assert snapshot.root == initial.root == base.root
        assert snapshot.actor == initial.actor == base.actor
        assert snapshot.branch == initial.branch == base.branch
        assert snapshot.clock == base.clock
        assert snapshot.state_hash != base.state_hash
        assert p3.config_hash == digest(p3.config)
        assert p3._config_path.is_file()
        assert json.loads(p3._config_path.read_text(encoding="utf-8"))[
            "config_hash"] == p3.config_hash
        assert p3.store.head()["hash"] == p3._head_hash()
        assert p3.registry == test_rules.make_registry(source_hash)
    finally:
        p3.close()


@requires_store
def test_formation_stored_records_pure_views_and_later_response(tmp_path):
    fanin, owner, initial, source_hash, config, first = _build(tmp_path)
    second = EventProposal(
        "owner-event-response", initial.clock + 12, "ADMIT_EVENT",
        (owner.source_ref,), owner.participants, {},
    )
    second_plan = _plan(
        initial, second, source_hash, phase="RECRUIT",
        counterpart="owner-counterpart",
    )
    config["plans"] = [config["plans"][0], second_plan]
    p3 = p3_owner.P3Owner(owner, **config)
    try:
        p3.validate_proposal(first)
        realized_first = p3.realize("owner-operation-1", first, p3.snapshot())
        assert realized_first.accessible["status"] == "OBSERVED"
        assert realized_first.accessible["memory_formation"] == "MISSING_RULE"
        assert realized_first.consequences["durable_psychological_transition"] == "MISSING_RULE"
        assert realized_first.consequences["native_action"] == "NOT_ISSUED_BY_P3_RULE"
        formation_receipt = p3.store.get_operation("owner-operation-1")["effects_receipt"]
        assert realized_first.consequences["effects_receipt_hash"] == (
            formation_receipt["receipt_hash"])
        assert realized_first.receipt_ref == (
            "P3_PSYCH:" + formation_receipt["response_hash"])
        assert realized_first.accessible == formation_receipt["projection"]["actor"]
        assert realized_first.after.clock == first.event_time
        assert p3.snapshot() == realized_first.after
        records = p3.store.query(
            project="owner-plan-comparison", counterpart="owner-counterpart",
            as_of=realized_first.after.clock,
        )
        assert len(records) == 2
        assert {row["payload"]["mode"] for row in records} == {
            "joint_check", "private_check"}
        user = realized_first.consequences["test_only_user_surface"]
        assert user["claims_status"] == "DEFER_MISSING_AUTHORITY"
        assert user["memory_formation"] == "MISSING_RULE"
        public = owner.fanin.view()
        assert {row["event_id"] for row in user["visible_events"]} <= {
            row["event_id"] for row in public["visible_events"]}

        realized_second = p3.realize(
            "owner-operation-2", second, p3.snapshot())
        response = realized_second.consequences["test_only_psychological"]
        assert response["status"] == "COMPUTED_TEST_ONLY_RESPONSE"
        assert response["first_person_claims"] == []
        assert response["native_action"] == "NOT_ISSUED_BY_P3_RULE"
        assert all(stream["native_action_performed"] is False
                   for stream in response["streams"])
        assert any(stream["mode"] != "inspect_alone"
                   for stream in response["streams"])
        assert realized_second.accessible["status"] == "OBSERVED"
        assert realized_second.consequences["durable_psychological_transition"] == (
            "MISSING_RULE")
    finally:
        p3.close()


@requires_store
def test_later_no_mediator_control_uses_inspect_alone(tmp_path):
    fanin, owner, initial, source_hash, config, proposal = _build(
        tmp_path, history=False, phase="RECRUIT")
    p3 = p3_owner.P3Owner(owner, **config)
    try:
        realized = p3.realize("owner-control-operation", proposal, p3.snapshot())
        response = realized.consequences["test_only_psychological"]
        assert response["status"] == "COMPUTED_TEST_ONLY_RESPONSE"
        assert [stream["mode"] for stream in response["streams"]] == ["inspect_alone"]
        assert response["streams"][0]["native_action_performed"] is False
        assert response["streams"][0]["material_eligible"] == (
            realized.consequences["immediate_response"]["objective_material_eligible"])
    finally:
        p3.close()


@requires_store
def test_wrong_source_rule_version_and_config_change_refuse_before_new_effects(tmp_path):
    fanin, owner, initial, source_hash, config, proposal = _build(tmp_path)
    p3 = p3_owner.P3Owner(owner, **config)
    try:
        bad_source = detached(config["source"])
        bad_source["root"] = "foreign-root"
        with pytest.raises(RecursionRefusal, match="P3_SOURCE_IDENTITY"):
            p3_owner.P3Owner(owner, source=bad_source, history=config["history"],
                              plans=config["plans"], standpoints=config["standpoints"])
        bad_plan = detached(config["plans"][0])
        bad_plan["permitted_rules"][0]["rule_version"] = "other"
        bad_plan = seal({key: value for key, value in bad_plan.items()
                         if key != "hash"})
        with pytest.raises(RecursionRefusal, match="P3_PLAN_RULE_VERSION"):
            p3_owner.P3Owner(owner, source=config["source"],
                              history=config["history"], plans=[bad_plan],
                              standpoints=config["standpoints"])
        document = json.loads(p3._config_path.read_text(encoding="utf-8"))
        document["config_hash"] = "0" * 64
        p3._config_path.write_text(json.dumps(document), encoding="utf-8")
        with pytest.raises(RecursionRefusal, match="P3_CONFIG_CHANGED"):
            p3.snapshot()
    finally:
        p3.close()


@requires_store
def test_idempotent_replay_and_reopened_owner_return_immutable_result(tmp_path):
    fanin, owner, initial, source_hash, config, proposal = _build(tmp_path)
    p3 = p3_owner.P3Owner(owner, **config)
    try:
        result = p3.realize("owner-replay-operation", proposal, p3.snapshot())
        state_after = owner.snapshot()
        again = p3.realize("owner-replay-operation", proposal, p3.snapshot())
        assert again.document() == result.document()
        assert owner.snapshot() == state_after
        cold = p3_owner.P3Owner(owner, **config)
        try:
            replay = cold.realize("owner-replay-operation", proposal, cold.snapshot())
            assert replay.document() == result.document()
            assert owner.snapshot() == state_after
        finally:
            cold.store.close()
    finally:
        p3.close()


@requires_store
def test_compression_evidence_survives_psych_committed_crash(tmp_path):
    """M2: a cold crash after commit must recover receipt compression evidence."""
    from p3_fixture_support import build_case, reopen_owner

    case = build_case(tmp_path, include_compression=True)
    recovered_owner = None
    try:
        owner = case.owner
        proposal = case.proposals[0]
        original_finish = owner.store.finish
        calls = {"count": 0}

        def crash_once(operation_id, result):
            calls["count"] += 1
            if calls["count"] == 1:
                raise RuntimeError("INJECTED_CRASH_AFTER_PSYCH_COMMIT")
            return original_finish(operation_id, result)

        owner.store.finish = crash_once
        with pytest.raises(RuntimeError, match="INJECTED_CRASH"):
            owner.realize("m2-compression-crash", proposal, owner.snapshot())
        operation = owner.store.get_operation("m2-compression-crash")
        assert operation["phase"] == "PSYCH_COMMITTED"
        receipt = operation["effects_receipt"]
        evidence = receipt["compression"]
        assert evidence["status"] == "BOUND"
        owner.close()
        _base2, recovered_owner = reopen_owner(case)
        recovered = recovered_owner.realize(
            "m2-compression-crash", proposal, recovered_owner.snapshot())
        assert recovered.consequences["test_only_compression_evidence"] == evidence
        assert recovered.consequences["effects_receipt_hash"] == (
            receipt["receipt_hash"])
        assert recovered.receipt_ref == "P3_PSYCH:" + receipt["response_hash"]
        completed = recovered_owner.store.get_operation("m2-compression-crash")
        assert completed["phase"] == "COMPLETE"
        assert completed["result"]["consequences"][
            "test_only_compression_evidence"] == evidence
    finally:
        if recovered_owner is not None:
            recovered_owner.close()
        else:
            case.owner.close()


@pytest.mark.skipif(not _store_available(), reason=STORE_BLOCK)
def test_real_subprocess_crash_boundary_recovers_prepared_base(tmp_path):
    """Kill after the actual base effect, before P3 save_world.

    The child uses the real P2Owner and the returned store. The parent reopens
    the exact same root, reconciles the completed base operation by its saved
    base_before, and commits the psychological sidecar once.
    """
    fanin, owner, initial, source_hash, config, proposal = _build(tmp_path)
    initial_root_hash = fanin.session.read_root()["root_hash"]
    initial_state = owner.snapshot().document()
    payload = {
        "source": config["source"],
        "history": config["history"],
        "plans": config["plans"],
        "standpoints": config["standpoints"],
        "proposal": proposal.document(),
        "root_hash": initial_root_hash,
        "initial_state": initial_state,
    }
    payload_path = tmp_path / "owner-crash-payload.json"
    payload_path.write_text(json.dumps(payload), encoding="utf-8")
    p3_root = Path(__file__).resolve().parents[1]
    engine_root = Path(__file__).resolve().parents[2] / (
        "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1")
    repo_root = Path(__file__).resolve().parents[3]
    # Cold child: the parent closes its P2 handle before the child reopens the
    # exact same frozen root. The child must not call start() on this root.
    owner.close()
    code = r'''
import json, os, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
from developmental_recursion.p2_owner import P2Owner, load_p2
from p3 import p3_owner
from developmental_recursion.contracts import EventProposal
root = Path(sys.argv[3]).resolve()
p = json.loads(Path(sys.argv[4]).read_text())
fanin = load_p2().open(root / "actual-p2")
case = fanin.deps["case_for"](True)
assert Path(fanin.session.state_root).resolve() == (root / "actual-p2").resolve()
assert fanin.session.read_root()["root_hash"] == p["root_hash"]
base = P2Owner(fanin, case=case, source=fanin.deps["source_for"](case),
               participants=tuple(fanin.session.read_root()["actor_ids"]))
assert base.snapshot().document() == p["initial_state"]
owner = p3_owner.P3Owner(base, source=p["source"], history=p["history"],
                        plans=p["plans"], standpoints=p["standpoints"])
proposal_doc = dict(p["proposal"])
proposal_doc["source_refs"] = tuple(proposal_doc["source_refs"])
proposal_doc["participants"] = tuple(proposal_doc["participants"])
proposal = EventProposal(**proposal_doc)
original = base.realize
def crash_after_base(operation_id, proposal_arg, expected):
    result = original(operation_id, proposal_arg, expected)
    os._exit(17)
base.realize = crash_after_base
owner.realize("owner-crash-operation", proposal, owner.snapshot())
'''
    environment = dict(os.environ)
    inherited = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = os.pathsep.join(
        [str(p3_root), str(engine_root), str(repo_root)]
        + ([inherited] if inherited else []))
    completed = subprocess.run(
        [sys.executable, "-c", code, str(p3_root), str(engine_root),
         str(tmp_path), str(payload_path)],
        env=environment, capture_output=True, text=True, timeout=120,
    )
    assert completed.returncode == 17, completed.stderr
    # The parent reopens the same P2 and P3 roots. The store remains PREPARED;
    # the base operation is already complete and must be replayed exactly.
    fanin2 = load_p2().open(tmp_path / "actual-p2")
    assert fanin2.session.read_root()["root_hash"] == initial_root_hash
    case2 = fanin2.deps["case_for"](True)
    base2 = P2Owner(fanin2, case=case2, source=fanin2.deps["source_for"](case2),
                    participants=tuple(fanin2.session.read_root()["actor_ids"]))
    owner2 = p3_owner.P3Owner(base2, source=config["source"],
                              history=config["history"], plans=config["plans"],
                              standpoints=config["standpoints"])
    try:
        recovered = owner2.realize("owner-crash-operation", proposal,
                                   owner2.snapshot())
        assert recovered.accessible["status"] == "OBSERVED"
        assert recovered.consequences["durable_psychological_transition"] == (
            "MISSING_RULE")
        assert owner2.snapshot() == recovered.after
        assert owner2.store.get_operation("owner-crash-operation")["phase"] == "COMPLETE"
    finally:
        owner2.close()
