"""Deterministic tests for pure historical dependency-group admission."""

from copy import deepcopy
import hashlib

from rawlsing_next.sorok_history.admission import evaluate


def ref(kind, object_id):
    material = kind + "|" + object_id
    return {
        "kind": kind,
        "object_id": "urn:test:" + object_id,
        "content_hash": hashlib.sha256(material.encode()).hexdigest(),
    }


TARGET = "target:bench"
OTHER_TARGET = "target:mug"
ROOT = "root:shared"
BRANCH = "branch:main"
AUTH = ref("AUTHORITY", "current")
EVENT = ref("WORLD_EVENT", "event-known")
PLACE = ref("PLACE", "workshop")
ACTOR = ref("ACTOR", "nadia")
SLACK = ref("CAUSAL_SLACK", "existing-project")
CLOSED = ref("WORLD_EVENT", "closed-effect")
KNOWN_MATERIAL = ref("KNOWN_FACT", "material-wood")
KNOWN_NEGATIVE_OWNER = ref("KNOWN_FACT", "owner-other")
KNOWN_UNKNOWN = ref("KNOWN_FACT", "provenance-unknown")


def packet(**overrides):
    base = {
        "schema": "SOROK_HISTORY_ADMISSION_PACKET@1",
        "request_id": "request:1",
        "root": ROOT, "branch": BRANCH, "time": 100,
        "target_ids": [TARGET],
        "surface": {
            TARGET: {
                "physical": {"color": "brown", "material": "wood"},
                "known_fact_refs": [KNOWN_MATERIAL, KNOWN_NEGATIVE_OWNER, KNOWN_UNKNOWN],
                "unresolved": ["provenance"],
            }
        },
        "known_facts": [
            {"ref": KNOWN_MATERIAL, "target_id": TARGET, "predicate": "material",
             "value": "wood", "state": "KNOWN"},
            {"ref": KNOWN_NEGATIVE_OWNER, "target_id": TARGET, "predicate": "owner",
             "value": "other-person", "state": "KNOWN_NEGATIVE"},
            {"ref": KNOWN_UNKNOWN, "target_id": TARGET, "predicate": "provenance",
             "value": None, "state": "UNKNOWN"},
        ],
        "world_refs": [PLACE, SLACK],
        "actor_refs": [ACTOR],
        "event_refs": [EVENT],
        "authority": {
            "ref": AUTH, "root": ROOT, "branch": BRANCH,
            "valid_from": 0, "valid_to": 100,
            "allowed_H_classes": ["H0", "H1", "H2"],
        },
        "chronology": {
            "time": 100, "window": [0, 100],
            "closed_event_refs": [CLOSED],
            "records": [
                {"ref": EVENT, "time": 50, "targets": [TARGET],
                 "condition": [{"target_id": TARGET, "predicate": "material",
                                "value": "wood", "valid_from": 0, "valid_to": 100}],
                 "custody": [{"target_id": TARGET, "custodian_ref": ACTOR,
                              "valid_from": 0, "valid_to": 100}]},
                {"ref": SLACK, "time": 40, "targets": [TARGET]},
                {"ref": CLOSED, "time": 60, "targets": [TARGET], "closed": True},
            ],
        },
        "causal_closure": {
            "closed_event_refs": [CLOSED],
            "closed_owner_effect_refs": [CLOSED],
            "allowed_slack_refs": [SLACK],
        },
        "budgets": {"max_groups": 8, "max_facts": 16,
                    "max_occurrences": 8, "max_links": 8,
                    "max_dependencies": 8, "max_refs": 64, "max_depth": 4},
    }
    base.update(overrides)
    return base


def group(group_id="g1", parents=None, parent_groups=None, h="H0"):
    return {
        "group_id": group_id,
        "parent_refs": [EVENT] if parents is None else parents,
        "parent_groups": [] if parent_groups is None else parent_groups,
        "asserted_H_class": h,
    }


def fact(fid="f1", group_id="g1", h="H0", **overrides):
    row = {
        "ref": ref("FACT", fid),
        "target_id": TARGET,
        "predicate": "color",
        "value": "brown",
        "effective_time": 90,
        "evidence_class": "GENERAL_PRIOR",
        "source_refs": [],
        "dependency_group": group_id,
        "asserted_H_class": h,
    }
    row.update(overrides)
    return row


def occurrence(oid="o1", group_id="g1", h="H1", **overrides):
    row = {
        "ref": ref("OCCURRENCE", oid),
        "effective_time": 90,
        "place_ref": PLACE,
        "actor_refs": [ACTOR],
        "target_ids": [TARGET],
        "action": "GIFT",
        "effects": [],
        "causal_parents": [EVENT],
        "source_refs": [],
        "dependency_group": group_id,
        "asserted_H_class": h,
    }
    row.update(overrides)
    return row


def candidate(**overrides):
    base = {
        "schema": "SOROK_HISTORY_ADMISSION_CANDIDATE@1",
        "request_id": "request:1",
        "facts": [fact()],
        "occurrences": [],
        "links": [],
        "dependencies": [group()],
    }
    base.update(overrides)
    return base


def test_lawful_h0_group_is_atomic_pure_and_deterministic():
    packet_value = packet()
    candidate_value = candidate()
    original_packet = deepcopy(packet_value)
    original_candidate = deepcopy(candidate_value)
    first = evaluate(packet_value, candidate_value)
    second = evaluate(packet_value, candidate_value)
    assert packet_value == original_packet
    assert candidate_value == original_candidate
    assert first == second
    assert first["status"] == "ACCEPTED"
    assert first["accepted_groups"][0]["group_id"] == "g1"
    assert ref("FACT", "f1") in first["accepted_groups"][0]["refs"]
    assert EVENT in first["accepted_groups"][0]["refs"]
    assert first["held"] == first["rejected"] == []


def test_contradictory_surface_rejects_whole_group():
    result = evaluate(packet(), candidate(facts=[
        fact("f1", value="red"),
        fact("f2", predicate="material", value="wood"),
    ]))
    assert result["status"] == "REJECTED"
    assert result["accepted_groups"] == []
    assert result["rejected"][0]["reason"] == "SURFACE_CONTRADICTION"


def test_missing_parent_rejects_group():
    missing = ref("WORLD_EVENT", "missing-parent")
    result = evaluate(packet(), candidate(dependencies=[group(parents=[missing])]))
    assert result["status"] == "REJECTED"
    assert result["rejected"][0]["reason"] == "MISSING_PARENT"


def test_authority_missing_and_H_class_not_allowed():
    missing = packet(authority=None)
    assert evaluate(missing, candidate())["rejected"][0]["reason"] == "AUTHORITY_REQUIRED"
    denied = packet(authority={
        "ref": AUTH, "root": ROOT, "branch": BRANCH,
        "valid_from": 0, "valid_to": 100, "allowed_H_classes": ["H0"],
    })
    result = evaluate(denied, candidate(
        facts=[], occurrences=[occurrence()], dependencies=[group(h="H1")]))
    assert result["status"] == "HELD"
    assert result["held"][0]["reason"] == "H_CLASS_NOT_ALLOWED"


def test_h1_undercalled_h3_is_held_not_accepted():
    effect = {"kind": "ACTOR_STATE", "actor_state": "new-capability"}
    result = evaluate(packet(), candidate(
        facts=[], occurrences=[occurrence(action="VISIT", effects=[effect])],
        dependencies=[group(h="H1")]))
    assert result["status"] == "HELD"
    assert result["accepted_groups"] == []
    assert result["held"][0]["reason"] == "H_CLASS_UNDERCALLED"


def test_h3_is_held_and_h2_needs_existing_slack_reference():
    h3 = evaluate(packet(), candidate(
        facts=[fact(h="H3")], dependencies=[group(h="H3")]))
    assert h3["status"] == "HELD"
    assert h3["held"][0]["reason"] == "H3_HELD"
    h2_no_ref = evaluate(packet(), candidate(
        facts=[fact(h="H2")], dependencies=[group(parents=[PLACE], h="H2")]))
    assert h2_no_ref["held"][0]["reason"] == "H2_SOURCE_REF_REQUIRED"
    h2 = evaluate(packet(), candidate(
        facts=[fact(h="H2")], dependencies=[group(parents=[SLACK], h="H2")]))
    assert h2["status"] == "ACCEPTED"


def test_unknown_is_not_a_negative_and_known_negative_blocks_positive():
    unknown = evaluate(packet(), candidate(facts=[fact(value="UNKNOWN")]))
    assert unknown["status"] == "HELD"
    assert unknown["held"][0]["reason"] == "UNKNOWN_NOT_FACT"
    negative = evaluate(packet(), candidate(facts=[
        fact(predicate="owner", value="candidate-person")]))
    assert negative["status"] == "REJECTED"
    assert negative["rejected"][0]["reason"] == "KNOWN_NEGATIVE_CONFLICT"


def test_external_verified_fact_and_closed_effect_are_rejected():
    external = evaluate(packet(), candidate(facts=[
        fact(evidence_class="EXTERNAL_VERIFIED")]))
    assert external["rejected"][0]["reason"] == "EXTERNAL_FACT_NOT_ADMITTED"
    closed = evaluate(packet(), candidate(dependencies=[group(parents=[CLOSED])]))
    assert closed["rejected"][0]["reason"] == "CLOSED_OWNER_EFFECT"


def test_budget_overflow_rejects_before_acceptance():
    result = evaluate(packet(budgets={"max_facts": 1}), candidate(
        facts=[fact("f1"), fact("f2", predicate="material")]))
    assert result["status"] == "REJECTED"
    assert result["rejected"][0]["reason"] == "BUDGET_EXCEEDED"


def test_parent_group_must_be_accepted_before_child():
    child = {
        "group_id": "g2", "parent_refs": [EVENT],
        "parent_groups": ["g1"], "asserted_H_class": "H0",
    }
    held_parent = evaluate(packet(), candidate(
        facts=[fact("f1", group_id="g1", value="red"),
               fact("f2", group_id="g2", predicate="material")],
        dependencies=[group("g1"), child]))
    assert held_parent["status"] == "REJECTED"
    assert {row["group_id"] for row in held_parent["rejected"]} == {"g1"}
    assert held_parent["held"][0]["group_id"] == "g2"
    assert held_parent["held"][0]["reason"] == "PARENT_GROUP_HELD"


def test_cross_group_occurrence_needs_accepted_parent_group():
    first = occurrence("o1", group_id="g1", action="VISIT")
    second = occurrence("o2", group_id="g2", action="VISIT", causal_parents=[first["ref"]])
    without_parent = evaluate(packet(), candidate(
        facts=[], occurrences=[first, second],
        dependencies=[group("g1", h="H1"), group("g2", h="H1")]))
    assert {row["group_id"]: row["status"] for row in without_parent["held"] + without_parent["rejected"]} == {"g2": "REJECTED"}
    assert (without_parent["held"] + without_parent["rejected"])[0]["reason"] == "MISSING_PARENT"
    with_parent = evaluate(packet(), candidate(
        facts=[], occurrences=[first, second],
        dependencies=[group("g1", h="H1"),
                      group("g2", parent_groups=["g1"], h="H1")]))
    assert with_parent["status"] == "ACCEPTED"


def test_occurrence_cycle_inside_group_is_rejected():
    self_ref = occurrence("o1", group_id="g1", action="VISIT")
    self_ref["causal_parents"] = [self_ref["ref"]]
    result = evaluate(packet(), candidate(
        facts=[], occurrences=[self_ref], dependencies=[group("g1", h="H1")]))
    assert result["status"] == "REJECTED"
    assert result["rejected"][0]["reason"] == "DEPENDENCY_CYCLE"


def test_accepted_fact_conflict_applies_to_later_group():
    first = fact("f1", group_id="g1", value="brown")
    second = fact("f2", group_id="g2", value="red")
    result = evaluate(packet(), candidate(
        facts=[first, second],
        dependencies=[group("g1"), group("g2")]))
    assert [row["group_id"] for row in result["accepted_groups"]] == ["g1"]
    assert result["rejected"][0]["group_id"] == "g2"
    assert result["rejected"][0]["reason"] == "KNOWN_FACT_CONFLICT"


def test_owner_chronology_late_parent_is_rejected():
    late = packet()
    late["chronology"]["records"][0]["time"] = 95
    result = evaluate(late, candidate(
        facts=[], occurrences=[occurrence(action="VISIT")],
        dependencies=[group(h="H1")]))
    assert result["status"] == "REJECTED"
    assert result["rejected"][0]["reason"] == "PARENT_AFTER_CHILD"


def test_contradictory_custody_and_impossible_condition_are_rejected():
    other = ref("ACTOR", "other-custodian")
    custody = occurrence("o1", action="VISIT", effects=[{
        "kind": "CUSTODY", "target_id": TARGET, "custodian_ref": other,
    }])
    custody_result = evaluate(packet(), candidate(
        facts=[], occurrences=[custody], dependencies=[group(h="H1")]))
    assert custody_result["status"] == "REJECTED"
    assert custody_result["rejected"][0]["reason"] == "CONTRADICTORY_CUSTODY"
    condition = occurrence("o2", action="VISIT", effects=[{
        "kind": "PHYSICAL_CONDITION", "target_id": TARGET,
        "predicate": "material", "value": "metal",
    }])
    condition_result = evaluate(packet(), candidate(
        facts=[], occurrences=[condition], dependencies=[group(h="H1")]))
    assert condition_result["status"] == "REJECTED"
    assert condition_result["rejected"][0]["reason"] == "IMPOSSIBLE_STATE_TRANSITION"


def test_missing_owner_material_is_held_not_model_certified():
    no_records = packet()
    no_records["chronology"]["records"] = []
    result = evaluate(no_records, candidate(
        facts=[], occurrences=[occurrence(action="VISIT")],
        dependencies=[group(h="H1")]))
    assert result["status"] == "HELD"
    assert result["held"][0]["reason"] == "OWNER_MATERIAL_REQUIRED"


def test_arbitrary_effect_is_held():
    arbitrary = occurrence("o1", action="VISIT", effects=[{"kind": "MAGIC"}])
    result = evaluate(packet(), candidate(
        facts=[], occurrences=[arbitrary], dependencies=[group(h="H1")]))
    assert result["status"] == "HELD"
    assert result["held"][0]["reason"] == "UNSUPPORTED_EFFECT"


def test_lawful_bounded_h1_episode_is_accepted():
    result = evaluate(packet(), candidate(
        facts=[], occurrences=[occurrence(action="VISIT")],
        dependencies=[group(h="H1")]))
    assert result["status"] == "ACCEPTED"
    assert result["accepted_groups"][0]["asserted_H_class"] == "H1"
    assert result["accepted_groups"][0]["claims"][0]["action"] == "VISIT"
