"""D01 discriminating tests over the actual P3 owner/store and rule producer."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

D01_ROOT = Path(__file__).resolve().parents[1]
WORKER_RETURNS = D01_ROOT.parent
P3_ROOT = WORKER_RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
ENGINE_ROOT = WORKER_RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
for _path in (D01_ROOT, P3_ROOT, ENGINE_ROOT, P3_ROOT / "tests"):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import d01_reuse  # noqa: E402
from developmental_recursion.contracts import (  # noqa: E402
    RecursionRefusal,
    detached,
    digest,
)
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402
from p3 import p3_owner, test_rules  # noqa: E402
from p3.state_store import PsycheStore  # noqa: E402
from p3_fixture_support import (  # noqa: E402
    COUNTERPART,
    PROJECT,
    build_case,
)


def _open_base(case):
    fanin = load_p2().open(Path(case.state_root))
    try:
        actual = fanin.deps["case_for"](True)
        return P2Owner(
            fanin,
            case=actual,
            source=fanin.deps["source_for"](actual),
            participants=tuple(fanin.session.read_root()["actor_ids"]),
        )
    except BaseException:
        fanin.close()
        raise


def _cold_open(case):
    base = _open_base(case)
    try:
        owner = d01_reuse.open_cold_owner(base, state_root=case.state_root)
    except BaseException:
        base.close()
        raise
    return base, owner


def _rule_fixture(*, outcomes=("recognized_plan",), phase="FORMATION", clock=106,
                  accessible=None):
    source = digest({"fixture": "D01 nonrespondent mechanical rule unit"})
    identity = {
        "root": digest({"root": "D01 different from B1"}),
        "actor": "ACTOR-D01", "branch": "d01-branch", "clock": clock,
        "state_hash": digest({"clock": clock}),
    }
    proposal = {
        "event_id": "d01-selected-" + str(clock), "event_time": clock,
        "operation": "ADMIT_EVENT", "source_refs": ["P2_INPUT:unit"],
        "participants": ["ACTOR-D01", "COACTOR-D01"],
        "circumstances": {}, "interval": None,
    }
    registry = test_rules.make_registry(source)
    plan = {key: identity[key] for key in ("root", "actor", "branch")}
    plan.update(
        grade=test_rules.GRADE, source_hash=source,
        registry_hash=registry["hash"], proposal_hash=digest(proposal),
        event_id=proposal["event_id"],
        permitted_rules=test_rules.rule_descriptors(), phase=phase,
        project="d01-project", counterpart="COACTOR-D01",
        activation_roles=["peer"], relation_refs=["d01-relation"],
        obligation_refs=[],
    )
    history = []
    for index, outcome in enumerate(outcomes):
        row = {key: identity[key] for key in ("root", "actor", "branch")}
        row.update(
            episode_id="d01-history-" + str(index), project=plan["project"],
            counterpart=plan["counterpart"], time=90 + index,
            activity="compare_plans_in_task", outcome=outcome,
            parent_refs=[history[-1]["hash"]] if history else [],
            grade=test_rules.GRADE, source_hash=source,
        )
        history.append(dict(detached(row), hash=digest(row)))
    if accessible is None:
        accessible = {
            "status": "OBSERVED", "actor_ref": identity["actor"],
            "events": [{"event_id": "action-" + str(clock)}],
        }
    realized = {
        "after": identity,
        "objective": {"event": {
            "actor_id": identity["actor"], "branch_id": identity["branch"],
            "event_time": clock, "action_event_id": "action-" + str(clock),
            "performed": True,
            "e1_event_hash": digest({"admitted mechanical witness": clock}),
        }},
        "accessible": accessible,
        "consequences": {"immediate_response": {
            "objective_material_eligible": True}},
    }
    return {
        "identity": identity, "proposal": proposal, "realized": realized,
        "history": history, "records": [],
        "plan": dict(detached(plan), hash=digest(plan)),
        "source_hash": source, "registry": registry,
    }


def _activated_later(fixture, records):
    activation = {
        "identity": fixture["identity"],
        "registry_hash": fixture["registry"]["hash"],
        "entries": [
            {"record_id": record["record_id"], "record_hash": record["hash"],
             "activation": "ELIGIBLE"}
            for record in records
        ],
        "contradictions": [],
    }
    body = dict(fixture)
    body["records"] = list(records)
    return test_rules.evaluate_event(**body, activation=activation)


def test_rule_value_change_controls_later_response() -> None:
    recognized_fixture = _rule_fixture()
    imposed_fixture = _rule_fixture(outcomes=("imposed_plan",))
    assert recognized_fixture["realized"]["objective"]["event"]["e1_event_hash"] == (
        imposed_fixture["realized"]["objective"]["event"]["e1_event_hash"])
    recognized = test_rules.evaluate_event(**recognized_fixture)
    imposed = test_rules.evaluate_event(**imposed_fixture)
    assert recognized["records"][0]["payload"]["mode"] == "joint_check"
    assert imposed["records"][0]["payload"]["mode"] == "private_check"
    assert recognized["records"][0]["payload"]["mode"] != (
        imposed["records"][0]["payload"]["mode"])
    assert recognized["records"][0]["hash"] != imposed["records"][0]["hash"]
    assert recognized["records"][0]["record_id"] != (
        imposed["records"][0]["record_id"])

    later_recognized = _rule_fixture(
        outcomes=("recognized_plan",), phase="RECRUIT", clock=112)
    later_imposed = _rule_fixture(
        outcomes=("imposed_plan",), phase="RECRUIT", clock=112)
    recognized_response = _activated_later(
        later_recognized, recognized["records"])
    imposed_response = _activated_later(
        later_imposed, imposed["records"])
    assert [row["mode"] for row in recognized_response["response"]["streams"]] == [
        "joint_check"]
    assert [row["mode"] for row in imposed_response["response"]["streams"]] == [
        "private_check"]
    assert recognized_response["response"]["native_rule"] == "MISSING_RULE"
    assert imposed_response["response"]["native_action"] == (
        "NOT_ISSUED_BY_P3_RULE")
    assert recognized_response["records"] == imposed_response["records"] == []


def test_cold_reopen_later_consumer_reads_exact_owner_held_record(tmp_path: Path) -> None:
    case = build_case(tmp_path)
    first = case.owner.realize(
        "d01-cold-formation", case.proposals[0], case.owner.snapshot(),
    )
    read = d01_reuse.read_sourcefree_records(
        case.owner, project=PROJECT, counterpart=COUNTERPART,
        as_of=first.after.clock,
    )
    assert len(read["hashes"]) == 2
    assert read["head"]["count"] == 2
    case.owner.close()

    base, cold = _cold_open(case)
    try:
        assert cold.store.head() == read["head"]
        assert cold.store.verify() is True
        reread = d01_reuse.read_sourcefree_records(
            cold, project=PROJECT, counterpart=COUNTERPART,
            as_of=first.after.clock,
        )
        assert reread["hashes"] == read["hashes"]
        assert reread["records"] == read["records"]

        later = d01_reuse.later_consumer(
            cold, "d01-cold-later", case.proposals[1],
            require_record_hashes=read["hashes"],
        )
        formation_response = first.consequences["test_only_psychological"]
        assert later["response"]["event_ref"] != formation_response["event_ref"]
        assert later["operation_id"] == "d01-cold-later"
        assert set(later["record_hashes"]) == set(read["hashes"])
        assert set(read["hashes"]) <= set(later["readset"])
        assert cold.store.head() == read["head"]
        assert later["actor_surface"]["status"] == "OBSERVED"
        assert later["actor_surface"]["memory_formation"] == "MISSING_RULE"
    finally:
        cold.close()


def test_cold_no_record_consumer_differs_and_fabricates_nothing(tmp_path: Path) -> None:
    case = build_case(tmp_path / "empty")
    assert case.owner.store.head()["count"] == 0
    case.owner.close()

    base, cold = _cold_open(case)
    try:
        assert cold.store.head()["count"] == 0
        later = d01_reuse.later_consumer(
            cold, "d01-empty-later", case.proposals[1],
        )
        assert later["record_hashes"] == []
        assert [row["mode"] for row in later["response"]["streams"]] == [
            "inspect_alone"]
        assert cold.store.head()["count"] == 0
    finally:
        cold.close()


def test_config_and_source_severance_refuse_then_exact_restore(
    tmp_path: Path, monkeypatch,
) -> None:
    case = build_case(tmp_path)
    first = case.owner.realize(
        "d01-severance-formation", case.proposals[0], case.owner.snapshot(),
    )
    read = d01_reuse.read_sourcefree_records(
        case.owner, project=PROJECT, counterpart=COUNTERPART,
        as_of=first.after.clock,
    )
    config_path = Path(case.state_root) / p3_owner.CONFIG_FILE
    saved = config_path.read_bytes()
    case.owner.close()

    config_path.unlink()
    with pytest.raises(RecursionRefusal, match="D01_COLD_CONFIG_MISSING"):
        _cold_open(case)

    base = _open_base(case)
    try:
        with pytest.raises(
            RecursionRefusal, match="P3_CONFIG_MISSING_WITH_EXISTING_STORE",
        ):
            p3_owner.P3Owner(
                base, source=case.source, history=case.history, plans=case.plans,
                catalog=case.catalog, compression_specs=case.compression_specs,
                standpoints=case.standpoints, mode="TEST_ONLY",
            )
    finally:
        base.close()

    config_path.write_bytes(saved)
    base, cold = _cold_open(case)
    try:
        assert cold.store.head() == read["head"]
        assert cold.store.verify() is True

        document = json.loads(config_path.read_text(encoding="utf-8"))
        document["config"]["source"]["root"] = "foreign-root"
        document["config"]["source_hash"] = digest(document["config"]["source"])
        document["config_hash"] = digest(document["config"])
        config_path.write_text(json.dumps(document), encoding="utf-8")
        with pytest.raises(RecursionRefusal, match="D01_COLD_BASE_IDENTITY:root"):
            _cold_open(case)
        config_path.write_bytes(saved)

        document = json.loads(config_path.read_text(encoding="utf-8"))
        document["config"]["source"]["branch"] = "foreign-branch"
        document["config"]["source_hash"] = digest(document["config"]["source"])
        document["config_hash"] = digest(document["config"])
        config_path.write_text(json.dumps(document), encoding="utf-8")
        with pytest.raises(RecursionRefusal, match="D01_COLD_BASE_IDENTITY:branch"):
            _cold_open(case)
        config_path.write_bytes(saved)

        with pytest.raises(RecursionRefusal, match="STORE_REOPEN_BINDING_MISMATCH"):
            PsycheStore(
                Path(case.state_root) / p3_owner.STORE_FILE,
                binding={"root": "foreign-root", "actor": cold.snapshot().actor,
                         "branch": cold.snapshot().branch},
                registry_hash=cold.registry["hash"],
                source_hash=cold.source_hash,
            )

        missing = Path(tmp_path) / "missing-bfirst.py"
        with monkeypatch.context() as scoped:
            scoped.setattr(test_rules, "B1_PATH", missing)
            with pytest.raises(RecursionRefusal, match="P3_B1_SOURCE_SEVERED"):
                d01_reuse.later_consumer(
                    cold, "d01-severed-later", case.proposals[1],
                    require_record_hashes=read["hashes"],
                )
        assert cold.store.head() == read["head"]
    finally:
        cold.close()

    base, restored = _cold_open(case)
    try:
        later = d01_reuse.later_consumer(
            restored, "d01-restored-later", case.proposals[1],
            require_record_hashes=read["hashes"],
        )
        assert set(later["record_hashes"]) == set(read["hashes"])
        assert restored.store.head() == read["head"]
    finally:
        restored.close()


def test_narrative_and_native_claims_are_not_durable_sourcefree_records() -> None:
    result = test_rules.evaluate_event(**_rule_fixture(
        accessible={"status": "HELD", "user_saw_it": True,
                    "impressions": ["I remember the plan."]}))
    assert result["records"] == []
    assert result["response"]["status"] == "HELD"
    assert result["memory_formation"] == "MISSING_RULE"
    assert test_rules.production_guard() == {
        "status": "DENY_ZERO_EFFECT",
        "reason": "ZERO_POSITIVE_REGISTRY",
        "effects": [],
        "native_rule": "MISSING_RULE",
    }
    selected = d01_reuse.producer_identity()
    assert selected["production_guard"]["status"] == "DENY_ZERO_EFFECT"
    assert selected["native_rule"] == "MISSING_RULE"
    assert selected["authority"] == "SOURCEFREE_TEST_ONLY"
    assert selected["selected_rule"]["rule_id"] == (
        "TEST_ONLY_P3_B1_SCOPED_MEDIATOR_CREATE")

    with pytest.raises(RecursionRefusal, match="D01_NATIVE_RULE_CLAIM"):
        d01_reuse.validate_sourcefree_response({
            "status": "COMPUTED_TEST_ONLY_RESPONSE",
            "native_rule": "CAN008_ISSUED",
            "native_action": "NOT_ISSUED_BY_P3_RULE",
            "memory_formation": "MISSING_RULE",
            "first_person_claims": [],
        })
    with pytest.raises(RecursionRefusal, match="D01_FIRST_PERSON_CLAIM"):
        d01_reuse.validate_sourcefree_response({
            "status": "COMPUTED_TEST_ONLY_RESPONSE",
            "native_rule": "MISSING_RULE",
            "native_action": "NOT_ISSUED_BY_P3_RULE",
            "memory_formation": "MISSING_RULE",
            "first_person_claims": ["I remember"],
        })
    valid = d01_reuse.validate_sourcefree_response({
        "status": "COMPUTED_TEST_ONLY_RESPONSE",
        "native_rule": "MISSING_RULE",
        "native_action": "NOT_ISSUED_BY_P3_RULE",
        "memory_formation": "MISSING_RULE",
        "first_person_claims": [],
    })
    assert valid["native_rule"] == "MISSING_RULE"
