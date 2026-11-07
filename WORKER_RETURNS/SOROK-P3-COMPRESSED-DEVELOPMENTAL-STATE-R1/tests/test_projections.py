from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
ENGINE = ROOT / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
for path in (str(ROOT), str(ENGINE)):
    if path not in sys.path:
        sys.path.insert(0, path)

from developmental_recursion.contracts import RecursionRefusal, digest
from p3.projections import activate, project_views


def h(value):
    return digest(value)


def identity(clock=10):
    return {"root": "root-a", "actor": "A", "branch": "branch-a",
            "clock": clock, "state_hash": h({"state": "initial"})}


def registry():
    rules = [
        {"rule_id": "r-approach", "rule_version": "1", "rule_hash": h({"rule": "approach"})},
        {"rule_id": "r-avoid", "rule_version": "1", "rule_hash": h({"rule": "avoid"})},
    ]
    doc = {"grade": "SOURCEFREE_TEST_ONLY", "rules": rules,
           "source_hash": h({"source": "owner-source"}),
           "incompatible_modes": [["APPROACH", "AVOID"]]}
    doc["hash"] = h(doc)
    return doc


def context(**overrides):
    doc = {
        "root": "root-a", "actor": "A", "branch": "branch-a", "clock": 10,
        "project": "work", "counterpart": "B",
        "interlocutor_role": "employer", "relation_ref": "rel-1",
        "obligation_refs": ["ob-1"], "actor_observed": True,
        "material_eligible": False, "source_refs": [h({"source": "context"})],
        "grade": "SOURCEFREE_TEST_ONLY",
    }
    doc.update(overrides)
    doc["hash"] = h(doc)
    return doc


def record(reg, *, mode="APPROACH", rule=None, selectors=None,
           record_id="record-1", project="work", counterpart="B",
           effective_from=1, rule_id="r-approach"):
    if rule is None:
        rule = next(x for x in reg["rules"] if x["rule_id"] == rule_id)
    payload = {"mode": mode}
    payload.update(selectors or {})
    doc = {
        "root": "root-a", "actor": "A", "branch": "branch-a",
        "project": project, "counterpart": counterpart,
        "record_id": record_id, "kind": "V3MS_MEDIATOR",
        "payload": payload, "rule_id": rule["rule_id"],
        "rule_version": rule["rule_version"], "rule_hash": rule["rule_hash"],
        "registry_hash": reg["hash"], "source_hash": reg["source_hash"],
        "effective_from": effective_from,
        "causal_parents": [h({"event": "event-1"})],
        "grade": "SOURCEFREE_TEST_ONLY",
    }
    doc["hash"] = h(doc)
    return doc


def test_activate_returns_eligible_and_independent_material():
    reg = registry()
    rec = record(reg, selectors={"activation_roles": ["employer"],
                                 "relation_refs": ["rel-1"],
                                 "obligation_refs": ["ob-1"],
                                 "requires_actor_access": True})
    ctx = context(material_eligible=False)
    before = copy.deepcopy((reg, rec, ctx))
    result = activate([rec], identity=identity(), context=ctx, registry=reg)
    assert result["grade"] == "SOURCEFREE_TEST_ONLY"
    assert result["entries"][0]["activation"] == "ELIGIBLE"
    assert result["entries"][0]["material_eligible"] is False
    assert result["status"] == "OK"
    assert (reg, rec, ctx) == before  # pure read, no input mutation


def test_activate_role_relation_obligation_and_access_selectors():
    reg = registry()
    rec = record(reg, selectors={
        "activation_roles": ["employer"], "relation_refs": ["rel-1"],
        "obligation_refs": ["ob-1"], "requires_actor_access": True,
    })
    unknown_role = activate([rec], identity=identity(), context=context(
        interlocutor_role=None), registry=reg)
    assert unknown_role["entries"][0]["activation"] == "UNKNOWN"
    mismatch = activate([rec], identity=identity(), context=context(
        interlocutor_role="friend"), registry=reg)
    assert mismatch["entries"][0]["activation"] == "INHIBITED"
    unknown_relation = activate([rec], identity=identity(), context=context(
        relation_ref=None), registry=reg)
    assert unknown_relation["entries"][0]["activation"] == "UNKNOWN"
    unmet_obligation = activate([rec], identity=identity(), context=context(
        obligation_refs=["other"]), registry=reg)
    assert unmet_obligation["entries"][0]["activation"] == "INHIBITED"
    no_access = activate([rec], identity=identity(), context=context(
        actor_observed=False), registry=reg)
    assert no_access["entries"][0]["activation"] == "INHIBITED"


def test_contradiction_is_declared_and_streams_remain_addressable():
    reg = registry()
    approach = record(reg, record_id="record-approach", mode="APPROACH",
                      rule_id="r-approach")
    avoid = record(reg, record_id="record-avoid", mode="AVOID",
                   rule_id="r-avoid")
    result = activate([avoid, approach], identity=identity(), context=context(),
                      registry=reg)
    assert result["status"] == "CONTRADICTION"
    assert result["contradictions"] == [["record-approach", "record-avoid"]]
    assert {row["record_id"] for row in result["entries"]} == {
        "record-approach", "record-avoid"}
    assert all(row["activation"] == "ELIGIBLE" for row in result["entries"])
    assert "winner" not in result and "score" not in result


def test_contradiction_requires_same_scope_and_registry_pair():
    reg = registry()
    approach = record(reg, record_id="a", mode="APPROACH", rule_id="r-approach")
    avoid = record(reg, record_id="b", mode="AVOID", rule_id="r-avoid",
                   counterpart="C")
    result = activate([approach, avoid], identity=identity(),
                      context=context(counterpart="B"), registry=reg)
    assert result["status"] == "OK"
    assert result["contradictions"] == []


def test_activate_rejects_wrong_identity_hash_source_and_version():
    reg = registry()
    rec = record(reg)
    ctx = context()
    with pytest.raises(RecursionRefusal):
        activate([rec], identity=identity(clock=11), context=ctx, registry=reg)
    with pytest.raises(RecursionRefusal):
        activate([rec], identity=identity(), context=context(clock=11), registry=reg)
    for key, value in (("root", "wrong-root"), ("actor", "wrong-actor"),
                       ("branch", "wrong-branch")):
        bad = copy.deepcopy(rec)
        bad[key] = value
        with pytest.raises(RecursionRefusal):
            activate([bad], identity=identity(), context=ctx, registry=reg)
    bad = copy.deepcopy(rec)
    bad["source_hash"] = h({"source": "wrong"})
    with pytest.raises(RecursionRefusal):
        activate([bad], identity=identity(), context=ctx, registry=reg)
    bad = copy.deepcopy(rec)
    bad["rule_hash"] = h({"rule": "wrong"})
    with pytest.raises(RecursionRefusal):
        activate([bad], identity=identity(), context=ctx, registry=reg)
    bad = copy.deepcopy(rec)
    bad["payload"] = {"mode": "APPROACH", "class": "worker"}
    bad["hash"] = h({k: v for k, v in bad.items() if k != "hash"})
    with pytest.raises(RecursionRefusal):
        activate([bad], identity=identity(), context=ctx, registry=reg)


def _public_event(event_id="public-action", kind="ACTION"):
    return {
        "event_id": event_id, "kind": kind, "clock": 10, "location": "workshop",
        "actor_visible_id": "A", "summary": "public action",
        "body_public": {"text": "hello", "observable": True,
                        "private_motive": "must-not-leak",
                        "nested": {"source_hash": "must-not-leak"}},
        "source_ref": "PUBLIC_REF", "perceived_by_user": True,
        "private_motive": "must-not-leak", "source_hash": "must-not-leak",
    }


def _actor_event(event_id="actor-action"):
    return {
        "event_id": event_id, "kind": "ACTION", "clock": 9,
        "location": "workshop", "actor_visible_id": "actor-alias",
        "summary": "actor sees this", "body_public": {"text": "actor",
                                                     "private_motive": "secret"},
        "source_ref": "ACTOR_REF", "perceived_by_user": True,
        "perception": {"clock": 9, "channel": "sight"},
        "private_motive": "secret", "source_hash": "secret",
    }


def views_fixture(*, actor=None, public=None, permissions=None):
    ident = identity()
    actor_doc = actor if actor is not None else {
        "schema": "SOROK_ACTOR_EXPERIENCE@1",
        "grade": "TEST_ONLY_S47_OWNER_NOT_NATIVE_DEVELOPMENTAL_SCIENCE",
        "actor_ref": "A", "status": "OBSERVED",
        "events": [_actor_event()], "memory_formation": "MISSING_RULE",
    }
    public_doc = public if public is not None else {
        "schema": "SOROK_WP19_ENCOUNTER_VIEW@1",
        "grade": "TEST_ONLY_S45_WP19_PROJECTION_NOT_NATIVE",
        "clock": 10, "location": "workshop",
        "visible_events": [_public_event("public-action", "ACTION"),
                           _public_event("public-speech", "SPEECH")],
        "visible_actions": [_public_event("public-action", "ACTION")],
        "visible_speech": [{"event_id": "public-speech", "speaker": "B",
                            "clock": 10, "text": "hello",
                            "labeled_english": "hello", "gesture": "wave",
                            "strategy": "PUBLIC", "summary": "speech",
                            "source_event_hash": "must-not-leak",
                            "readset": ["must-not-leak"]}],
        "private_motive": "must-not-leak", "source_hash": "must-not-leak",
    }
    ctx = context()
    exp = {"root": "root-a", "actor": "A", "branch": "branch-a",
           "clock": 10, "experience_hash": h(actor_doc)}
    pub = {"root": "root-a", "actor": "A", "branch": "branch-a",
           "clock": 10, "view_hash": h(public_doc)}
    stand = {
        "root": "root-a", "actor": "A", "branch": "branch-a", "clock": 10,
        "interlocutor_ref": "U", "role": "user",
        "permissions": ["OBSERVE_PUBLIC_ACTION", "READ_PUBLIC_DIALOGUE"]
        if permissions is None else permissions,
        "source_refs": [h({"source": "standpoint"})],
        "grade": "SOURCEFREE_TEST_ONLY",
    }
    stand["hash"] = h(stand)
    return ident, actor_doc, exp, public_doc, pub, stand


def test_project_views_actor_and_user_are_separate_and_sanitized():
    ident, actor, exp, public, pub, stand = views_fixture()
    before = copy.deepcopy((ident, actor, exp, public, pub, stand))
    result = project_views(identity=ident, actor_experience=actor,
                           experience_binding=exp, public_view=public,
                           public_binding=pub, standpoint=stand)
    assert result["grade"] == "SOURCEFREE_TEST_ONLY"
    assert result["actor"]["status"] == "OBSERVED"
    assert {row["event_id"] for row in result["actor"]["events"]} == {"actor-action"}
    assert {row["event_id"] for row in result["user"]["visible_events"]} == {
        "public-action"}
    assert {row["event_id"] for row in result["user"]["visible_actions"]} == {
        "public-action"}
    assert {row["event_id"] for row in result["user"]["visible_speech"]} == {
        "public-speech"}
    assert all("perceived_by_user" not in row for row in result["actor"]["events"])
    assert "must-not-leak" not in str(result)
    assert "source_hash" not in str(result)
    assert result["claims_status"] == "DEFER_MISSING_AUTHORITY"
    assert result["actor"]["memory_formation"] == "MISSING_RULE"
    assert result["user"]["memory_formation"] == "MISSING_RULE"
    assert (ident, actor, exp, public, pub, stand) == before
    public_ids = {row["event_id"] for row in public["visible_events"]}
    user_ids = {row["event_id"] for row in result["user"]["visible_events"]}
    assert user_ids <= public_ids


def test_project_views_permission_surfaces_and_absent_actor():
    ident, actor, exp, public, pub, stand = views_fixture()
    action_only = views_fixture(permissions=["OBSERVE_PUBLIC_ACTION"])
    result = project_views(identity=action_only[0], actor_experience=action_only[1],
                           experience_binding=action_only[2],
                           public_view=action_only[3], public_binding=action_only[4],
                           standpoint=action_only[5])
    assert result["user"]["visible_speech"] == []
    assert result["user"]["visible_actions"]

    dialogue_only = views_fixture(permissions=["READ_PUBLIC_DIALOGUE"])
    result = project_views(identity=dialogue_only[0], actor_experience=dialogue_only[1],
                           experience_binding=dialogue_only[2],
                           public_view=dialogue_only[3], public_binding=dialogue_only[4],
                           standpoint=dialogue_only[5])
    assert result["user"]["visible_actions"] == []
    assert result["user"]["visible_events"] == []
    assert result["user"]["visible_speech"]

    no_permissions = views_fixture(permissions=[])
    result = project_views(identity=no_permissions[0], actor_experience=no_permissions[1],
                           experience_binding=no_permissions[2],
                           public_view=no_permissions[3], public_binding=no_permissions[4],
                           standpoint=no_permissions[5])
    assert result["user"]["status"] == "HELD"
    assert result["user"]["visible_events"] == []
    assert result["user"]["visible_actions"] == []
    assert result["user"]["visible_speech"] == []

    held = copy.deepcopy(actor)
    held.update(status="HELD", events=[], reason="P2_ACTOR_PERCEPTION_UNAVAILABLE")
    held_exp = copy.deepcopy(exp)
    held_exp["experience_hash"] = h(held)
    result = project_views(identity=ident, actor_experience=held,
                           experience_binding=held_exp, public_view=public,
                           public_binding=pub, standpoint=stand)
    assert result["actor"]["status"] == "HELD"
    assert result["actor"]["events"] == []
    assert result["user"]["visible_events"]


def test_project_views_wrong_bindings_and_permissions_refuse():
    ident, actor, exp, public, pub, stand = views_fixture()
    bad = copy.deepcopy(exp)
    bad["experience_hash"] = h({"wrong": True})
    with pytest.raises(RecursionRefusal):
        project_views(identity=ident, actor_experience=actor,
                      experience_binding=bad, public_view=public,
                      public_binding=pub, standpoint=stand)
    bad = copy.deepcopy(pub)
    bad["view_hash"] = h({"wrong": True})
    with pytest.raises(RecursionRefusal):
        project_views(identity=ident, actor_experience=actor,
                      experience_binding=exp, public_view=public,
                      public_binding=bad, standpoint=stand)
    bad = copy.deepcopy(stand)
    bad["permissions"] = ["OBSERVE_PUBLIC_ACTION", "READ_PRIVATE"]
    bad["hash"] = h({k: v for k, v in bad.items() if k != "hash"})
    with pytest.raises(RecursionRefusal):
        project_views(identity=ident, actor_experience=actor,
                      experience_binding=exp, public_view=public,
                      public_binding=pub, standpoint=bad)
    bad = copy.deepcopy(stand)
    bad["root"] = "wrong-root"
    bad["hash"] = h({k: v for k, v in bad.items() if k != "hash"})
    with pytest.raises(RecursionRefusal):
        project_views(identity=ident, actor_experience=actor,
                      experience_binding=exp, public_view=public,
                      public_binding=pub, standpoint=bad)
    bad_public = copy.deepcopy(public)
    bad_public["clock"] = 9
    bad_pub = copy.deepcopy(pub)
    bad_pub["view_hash"] = h(bad_public)
    with pytest.raises(RecursionRefusal):
        project_views(identity=ident, actor_experience=actor,
                      experience_binding=exp, public_view=bad_public,
                      public_binding=bad_pub, standpoint=stand)
