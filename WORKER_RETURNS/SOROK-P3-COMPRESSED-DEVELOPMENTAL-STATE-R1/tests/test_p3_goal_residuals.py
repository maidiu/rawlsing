"""Targeted proofs for the three original P3 residuals.

These are author-run actual P2/P3 checks, not independent acceptance. They do
not rerun the 13-case matrix or the 71-test inherited suite and do not alter
runtime, fixtures, checkers, accepted source or prior evidence.

Residuals:
1. same source/history/later world, with only prior formation vs no mediator;
2. genuinely distinct sourcefree root and cross-root source denial;
3. exact B1 source severance/restore in an actual P2 -> P3 event chain.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = ROOT.parent / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
for _path in (ROOT, ENGINE_ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from developmental_recursion.contracts import (  # noqa: E402
    EventProposal,
    RecursionRefusal,
    detached,
    digest,
)
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402
from p3 import p3_owner, test_rules  # noqa: E402
from p3_fixture_support import build_case, workflow_records  # noqa: E402
from test_p3_owner import _build  # noqa: E402


def _response(result):
    return result.consequences["test_only_psychological"]


def _same_history_scenario(root: Path, first_phase: str):
    """Build one actual P2/P3 case with a controlled first plan phase.

    The two fixtures use the same deterministic sourcefree P2 root/seed,
    source, history, and later proposal/world construction. The only
    authorized difference is FORMATION versus STABILITY on the first event.
    """
    fanin, owner, initial, source_hash, config, first = _build(
        root, history=True, phase=first_phase)
    second = EventProposal(
        "same-history-later", initial.clock + 12, "ADMIT_EVENT",
        (owner.source_ref,), owner.participants, {},
    )
    second_plan = _plan_for(
        initial, second, source_hash, phase="RECRUIT")
    config["plans"] = [config["plans"][0], second_plan]
    p3 = p3_owner.P3Owner(owner, **config)
    try:
        r1 = p3.realize(
            "same-history-" + first_phase.lower() + "-first",
            first, p3.snapshot(),
        )
        records_after_first = p3.store.query(
            project="owner-plan-comparison", counterpart="owner-counterpart",
            as_of=r1.after.clock,
        )
        r2 = p3.realize(
            "same-history-" + first_phase.lower() + "-later",
            second, p3.snapshot(),
        )
        return {
            "fanin": fanin,
            "owner": owner,
            "p3": p3,
            "initial": initial,
            "source_hash": source_hash,
            "config": config,
            "first": first,
            "second": second,
            "r1": r1,
            "r2": r2,
            "records_after_first": records_after_first,
            "base_after": owner.snapshot(),
            "world_after": detached(vars(fanin.session.world())),
            "head_after": p3.store.head(),
        }
    except BaseException:
        p3.close()
        raise


def _plan_for(initial, proposal, source_hash, phase):
    body = {
        "root": initial.root, "actor": initial.actor, "branch": initial.branch,
        "grade": test_rules.GRADE,
        "source_hash": source_hash,
        "registry_hash": test_rules.make_registry(source_hash)["hash"],
        "proposal_hash": digest(proposal.document()),
        "event_id": proposal.event_id,
        "permitted_rules": test_rules.rule_descriptors(),
        "phase": phase,
        "project": "owner-plan-comparison",
        "counterpart": "owner-counterpart",
        "activation_roles": ["peer"],
        "relation_refs": ["owner-collaboration"],
        "obligation_refs": [],
        "interlocutor_role": "peer",
    }
    return dict(body, hash=digest(body))


def test_same_history_only_prior_formation_changes_later_response(tmp_path: Path):
    """Only authorized prior formation differs; history and later world match."""
    formation = _same_history_scenario(tmp_path / "formation", "FORMATION")
    control = _same_history_scenario(tmp_path / "control", "STABILITY")
    try:
        # Exact same P2 source, history, initial state and later proposal.
        for key in ("root", "actor", "branch", "clock"):
            assert getattr(formation["initial"], key) == getattr(control["initial"], key)
        assert formation["source_hash"] == control["source_hash"]
        assert formation["owner"].source_ref == control["owner"].source_ref
        assert [row["hash"] for row in formation["config"]["history"]] == [
            row["hash"] for row in control["config"]["history"]]
        assert formation["second"].document() == control["second"].document()
        assert formation["config"]["plans"][1] == control["config"]["plans"][1]

        # Only the first authorized plan phase differs: FORMATION vs STABILITY.
        assert formation["config"]["plans"][0]["phase"] == "FORMATION"
        assert control["config"]["plans"][0]["phase"] == "STABILITY"

        # Formation contains the prior mediator records; control has none.
        assert len(formation["records_after_first"]) == 2
        assert {row["payload"]["mode"] for row in formation["records_after_first"]} == {
            "joint_check", "private_check"}
        assert formation["head_after"]["count"] == 2
        assert control["records_after_first"] == []
        assert control["head_after"]["count"] == 0

        f_response = _response(formation["r2"])
        c_response = _response(control["r2"])
        assert f_response["status"] == "COMPUTED_TEST_ONLY_RESPONSE"
        assert c_response["status"] == "COMPUTED_TEST_ONLY_RESPONSE"
        assert [row["mode"] for row in f_response["streams"]] != [
            row["mode"] for row in c_response["streams"]]
        assert {row["mode"] for row in f_response["streams"]} == {
            "joint_check", "private_check"}
        assert [row["mode"] for row in c_response["streams"]] == ["inspect_alone"]

        # The formation later readset carries the exact prior record hashes;
        # the no-mediator control does not.
        formed_hashes = {row["hash"] for row in formation["records_after_first"]}
        assert formed_hashes <= set(formation["r2"].readset)
        assert not (formed_hashes & set(control["r2"].readset))
        assert all(row.get("native_action_performed") is False
                   for row in f_response["streams"] + c_response["streams"])

        # Actual P2 state after the later proposal is identical; the difference
        # is the authorized P3 sidecar, not a changed native material outcome.
        assert formation["world_after"] == control["world_after"]
        assert formation["base_after"].clock == control["base_after"].clock
        assert formation["base_after"].root == control["base_after"].root
        assert formation["base_after"].actor == control["base_after"].actor
        assert formation["base_after"].branch == control["base_after"].branch
        assert formation["r2"].consequences["immediate_response"][
            "objective_material_eligible"] == control["r2"].consequences[
                "immediate_response"]["objective_material_eligible"]
    finally:
        formation["p3"].close()
        control["p3"].close()


def _distinct_base(tmp_path: Path, seed: str):
    fanin = load_p2().start(tmp_path / "actual-p2", seed=seed)
    case = fanin.deps["case_for"](True)
    base = P2Owner(
        fanin, case=case, source=fanin.deps["source_for"](case),
        participants=tuple(fanin.session.read_root()["actor_ids"]),
    )
    return fanin, base


def test_distinct_sourcefree_root_rejects_cross_root_source_before_effects(tmp_path: Path):
    """Use two different actual P2 roots; neither replicas nor string mutation."""
    left = build_case(tmp_path / "left")
    right_fanin = None
    right = None
    try:
        # Put a real source-bound P3 record on the left root.
        first = left.proposals[0]
        left.owner.realize("residual-left-formation", first, left.owner.snapshot())
        left_records = workflow_records(left.owner, first.event_time)
        assert len(left_records) == 2
        assert all(row["root"] == left.initial.root for row in left_records)

        right_fanin, right = _distinct_base(tmp_path / "right", "02" * 32)
        right_before = right.snapshot()
        right_root = right.snapshot().root
        assert left.initial.root != right_root
        assert left.source["root"] == left.initial.root
        assert right_root != left.source["root"]
        right_sidecar_dir = Path(right.fanin.session.state_root)

        with pytest.raises(RecursionRefusal):
            p3_owner.P3Owner(
                right, source=left.source, history=left.history,
                plans=left.plans, catalog=left.catalog,
                compression_specs=left.compression_specs,
                standpoints=left.standpoints,
            )

        # No right-side P2 effect and no right P3 sidecar/config creation.
        assert right.snapshot().document() == right_before.document()
        assert not (right_sidecar_dir / "p3_owner_config.json").exists()
        assert not (right_sidecar_dir / "p3_psyche.sqlite3").exists()

        # The left records remain bound to the left root; no record migration.
        assert left.owner.store.query(
            project="vertical:project", counterpart="vertical:counterpart",
            as_of=first.event_time,
        ) == left_records
        assert all(row["root"] != right_root for row in left_records)
    finally:
        if right is not None:
            right.close()
        elif right_fanin is not None:
            right_fanin.close()
        left.owner.close()


def test_actual_chain_source_severance_and_exact_restore(tmp_path: Path, monkeypatch):
    """B1 source absence/mismatch refuses before P2/P3 effects; exact restore works."""
    fanin, owner, initial, source_hash, config, proposal = _build(tmp_path)
    p3 = p3_owner.P3Owner(owner, **config)
    original_path = test_rules.B1_PATH
    original_bytes = original_path.read_bytes()
    try:
        base_before = owner.snapshot()
        head_before = p3.store.head()
        missing = tmp_path / "missing-bfirst.py"
        with monkeypatch.context() as scoped:
            scoped.setattr(test_rules, "B1_PATH", missing)
            with pytest.raises(RecursionRefusal, match="P3_B1_SOURCE_SEVERED"):
                p3.realize("residual-source-missing", proposal, p3.snapshot())
        assert owner.snapshot().document() == base_before.document()
        assert p3.store.head() == head_before
        assert p3.store.get_operation("residual-source-missing") is None

        altered = tmp_path / "altered-bfirst.py"
        altered.write_bytes(original_bytes + b"\n# exact-severance-test\n")
        with monkeypatch.context() as scoped:
            scoped.setattr(test_rules, "B1_PATH", altered)
            with pytest.raises(RecursionRefusal, match="P3_B1_SOURCE_SEVERED"):
                p3.realize("residual-source-mismatch", proposal, p3.snapshot())
        assert owner.snapshot().document() == base_before.document()
        assert p3.store.head() == head_before
        assert p3.store.get_operation("residual-source-mismatch") is None

        # Exact original bytes restored at the exact owner path; legitimate
        # actual P2 -> P3 continuation now commits and completes.
        assert test_rules.B1_PATH == original_path
        assert test_rules.B1_PATH.read_bytes() == original_bytes
        result = p3.realize("residual-source-restored", proposal, p3.snapshot())
        assert result.accessible["status"] == "OBSERVED"
        assert result.consequences["durable_psychological_transition"] == (
            "MISSING_RULE")
        assert p3.store.get_operation("residual-source-restored")["phase"] == "COMPLETE"
        state_after = p3.snapshot()
        base_after = owner.snapshot()
        replay = p3.realize("residual-source-restored", proposal, state_after)
        assert replay.document() == result.document()
        assert p3.snapshot() == state_after
        assert owner.snapshot() == base_after
    finally:
        p3.close()
