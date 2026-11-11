"""Mechanical rule tests, not actual-P2 integration or native psychology proof."""
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from p3 import test_rules as rules
from developmental_recursion.contracts import RecursionRefusal, detached, digest


def sealed(body):
    return dict(detached(body), hash=digest(body))


def fixture(*, clock=106, phase="FORMATION", outcomes=("recognized_plan",), material=True):
    source = digest({"fixture": "nonrespondent mechanical rule unit"})
    identity = {"root": digest({"root": "different from B1"}), "actor": "ACTOR-47",
                "branch": "fork-two", "clock": clock, "state_hash": digest({"clock": clock})}
    proposal = {"event_id": "selected-" + str(clock), "event_time": clock,
                "operation": "ADMIT_EVENT", "source_refs": ["P2_INPUT:unit"],
                "participants": ["ACTOR-47", "COACTOR-3"], "circumstances": {}, "interval": None}
    registry = rules.make_registry(source)
    plan = {k: identity[k] for k in ("root", "actor", "branch")}
    plan.update(grade=rules.GRADE, source_hash=source, registry_hash=registry["hash"],
                proposal_hash=digest(proposal), event_id=proposal["event_id"],
                permitted_rules=rules.rule_descriptors(), phase=phase,
                project="project-97", counterpart="COACTOR-3", activation_roles=["peer"],
                relation_refs=["relation-9"], obligation_refs=[])
    history = []
    for i, outcome in enumerate(outcomes):
        h = {k: identity[k] for k in ("root", "actor", "branch")}
        h.update(episode_id="history-" + str(i), project=plan["project"],
                 counterpart=plan["counterpart"], time=90 + i,
                 activity="compare_plans_in_task", outcome=outcome,
                 parent_refs=[history[-1]["hash"]] if history else [],
                 grade=rules.GRADE, source_hash=source)
        history.append(sealed(h))
    event = {"actor_id": identity["actor"], "branch_id": identity["branch"],
             "event_time": clock, "action_event_id": "action-" + str(clock), "performed": True,
             "e1_event_hash": digest({"admitted mechanical witness": clock})}
    realized = {"after": identity, "objective": {"event": event},
                "accessible": {"status": "OBSERVED", "actor_ref": identity["actor"],
                               "events": [{"event_id": event["action_event_id"]}]},
                "consequences": {"immediate_response": {"objective_material_eligible": material}}}
    return dict(identity=identity, proposal=proposal, realized=realized, history=history,
                records=[], plan=sealed(plan), source_hash=source, registry=registry)


def test_recovered_b1_predicate_is_actor_local_and_preserves_opposed_parents():
    args = fixture(outcomes=("recognized_plan", "imposed_plan"))
    before = detached(args)
    result = rules.evaluate_event(**args)
    assert args == before
    assert [r["payload"]["mode"] for r in result["records"]] == ["joint_check", "private_check"]
    assert {r["actor"] for r in result["records"]} == {"ACTOR-47"}
    assert len({r["record_id"] for r in result["records"]}) == 2
    assert all(r["causal_parents"][0] == args["realized"]["objective"]["event"]["e1_event_hash"]
               for r in result["records"])
    assert all(r["payload"]["origin_access"] == "NOT_GRANTED_AS_MEMORY" for r in result["records"])


def test_later_response_requires_the_exact_prior_record_and_separate_activation_reader():
    formed = rules.evaluate_event(**fixture())["records"]
    later = fixture(clock=112, phase="RECRUIT")
    control = rules.evaluate_event(**later)
    later["records"] = formed
    with pytest.raises(RecursionRefusal, match="ACTIVATION_READER_REQUIRED"):
        rules.evaluate_event(**later)
    # Explicit mechanical activation fixture: its real producer is tested by
    # the separate projection worker and must be exercised in P2 integration.
    activation = {"identity": later["identity"], "registry_hash": later["registry"]["hash"],
                  "entries": [{"record_id": formed[0]["record_id"],
                               "record_hash": formed[0]["hash"], "activation": "ELIGIBLE"}],
                  "contradictions": []}
    positive = rules.evaluate_event(**later, activation=activation)
    assert positive["response"]["streams"][0]["candidate_activity"] == "joint_check:COACTOR-3"
    assert control["response"]["streams"][0]["candidate_activity"] == "inspect_alone:COACTOR-3"
    assert positive["response"]["streams"][0]["record_hash"] == formed[0]["hash"]
    assert later["realized"] == fixture(clock=112, phase="RECRUIT")["realized"]
    assert positive["records"] == []
    activation["identity"] = dict(later["identity"], actor="foreign")
    with pytest.raises(RecursionRefusal, match="ACTIVATION_IDENTITY"):
        rules.evaluate_event(**later, activation=activation)


def test_absent_actor_access_cannot_be_replaced_with_a_user_view_or_prose():
    args = fixture()
    args["realized"]["accessible"] = {"status": "HELD", "user_saw_it": True,
                                     "impressions": ["I remember the plan."]}
    result = rules.evaluate_event(**args)
    assert result["records"] == []
    assert result["response"]["status"] == "HELD"
    assert result["memory_formation"] == "MISSING_RULE"


def test_material_denial_is_not_repaired_by_a_mediator_or_native_claim():
    args = fixture(material=False)
    result = rules.evaluate_event(**args)
    assert result["records"]  # test-only organization may persist without a tool
    assert result["response"]["streams"][0]["material_eligible"] is False
    assert result["response"]["streams"][0]["native_action_performed"] is False
    assert args["realized"]["consequences"]["immediate_response"]["objective_material_eligible"] is False
    assert result["response"]["first_person_claims"] == []
    assert rules.production_guard()["status"] == "DENY_ZERO_EFFECT"


def test_wrong_version_and_exact_source_severance_refuse_and_restore(tmp_path, monkeypatch):
    args = fixture()
    bad = detached(args["plan"])
    bad["permitted_rules"][0]["rule_version"] = "other"
    args["plan"] = sealed({k: v for k, v in bad.items() if k != "hash"})
    with pytest.raises(RecursionRefusal, match="PLAN_RULE_VERSION"):
        rules.evaluate_event(**args)
    args = fixture()
    source = tmp_path / "bfirst.py"
    exact = rules.B1_PATH.read_bytes()
    source.write_bytes(exact + b"\n# severed bytes\n")
    monkeypatch.setattr(rules, "B1_PATH", source)
    with pytest.raises(RecursionRefusal, match="B1_SOURCE_SEVERED"):
        rules.evaluate_event(**args)
    source.write_bytes(exact)
    assert rules.evaluate_event(**args)["records"][0]["payload"]["mode"] == "joint_check"
