"""Native-ready input ports: fail-closed currentness, owners and empty registries."""
from __future__ import annotations

import pytest

from bp2_joined import ports
from bp2_joined.producer import make_rule_a, make_target_grant, make_target_rule
from bp2_joined.severance import run_severance


@pytest.fixture(scope="module")
def occurrence(tmp_path_factory):
    from bp2_joined.binding import build_world_occurrence
    from bp1.composer import build_two_actor_life

    return build_world_occurrence(build_two_actor_life(), actor="A")


def test_production_registries_are_empty_by_construction():
    registries = ports.production_registries()
    assert registries["response_rule_count"] == 0
    assert registries["target_rule_count"] == 0
    assert registries["status"] == (
        "PRODUCTION_RULE_REGISTRIES_EMPTY_AWAITING_COMPETENT_ISSUER")


def test_resource_currentness_states_are_typed(occurrence):
    rule = make_rule_a(occurrence, as_of=202)
    assert rule.check(now=203) is ports.Currentness.CURRENT
    future = ports.test_only_rule_resource(
        resource_id="TEST_ONLY_FUTURE", version="1", body={"a": 1},
        issuer_ref="TEST_ONLY_I", source_owner="O", permission_ref="P",
        effective_from=300, readset_refs=(), currentness_as_of=202)
    assert future.check(now=203) is ports.Currentness.NOT_YET_EFFECTIVE
    expired = ports.revoke(rule)
    assert expired.check(now=203) is ports.Currentness.REVOKED
    stale = ports.test_only_rule_resource(
        resource_id="TEST_ONLY_X", version="1", body={"a": 1},
        issuer_ref="TEST_ONLY_I", source_owner="O", permission_ref="P",
        effective_from=0, readset_refs=(), currentness_as_of=999)
    assert stale.check(now=10) is ports.Currentness.STALE
    assert rule.check(now=203, expected_version="2") is ports.Currentness.VERSION_MISMATCH
    assert rule.check(now=203, expected_hash="X") is ports.Currentness.HASH_MISMATCH
    assert rule.check(
        now=203, required_readset=("NOT_IN_READSET",)) is ports.Currentness.MISSING_READSET
    unissued = ports.Resource(
        resource_id="R", schema=ports.PORT_SCHEMA, version="1", content_hash="",
        issuer_ref="I", issuer_grade=ports.UNISSUED_GRADE, source_owner="O",
        permission_ref="P", effective_from=0, expires_at=None, revoked=False,
        readset_refs=(), currentness_as_of=0, body={})
    assert unissued.check(now=10) is ports.Currentness.UNISSUED


def test_adp019_port_cannot_mint_an_admission_receipt():
    port = ports.ADP019EventPort()
    with pytest.raises(ports.PortRefusal) as excinfo:
        port.admit_native(resource=None, now=202)
    assert excinfo.value.code == "ADP019_ADMISSION_RECEIPT_ABSENT"
    with pytest.raises(ports.PortRefusal) as excinfo:
        port.bind_test_only_e1(
            occurrence={"occurrence_id": "OCC-0001", "identity_digest": "x"},
            event_time=202, verified_proof=False)
    assert excinfo.value.code == "ADP019_E1_PROOF_UNVERIFIED"
    binding = port.bind_test_only_e1(
        occurrence={"occurrence_id": "OCC-0001", "identity_digest": "x"},
        event_time=202, verified_proof=True)
    assert binding.adp019_admission_receipt == "ADP019_ADMISSION_RECEIPT_ABSENT"
    assert binding.native_grant == "NOT_GRANTED"
    assert binding.admission_status == "TEST_ONLY_E1_BOUND_ADP019_NOT_ISSUED"


def test_adp010_port_never_promotes_availability_to_an_encounter():
    port = ports.ADP010EncounterPort("TEST_ONLY_WORLD_MATERIAL")
    available = port.availability()
    assert available.stage == "AVAILABLE"
    assert "NOT_ACTOR_ENCOUNTER" in available.status
    with pytest.raises(ports.PortRefusal) as excinfo:
        port.opportunity(subject_ref="TEST_ONLY_BP1_ACTOR_A", resource=None, now=202)
    assert excinfo.value.code == "ADP010_OPPORTUNITY_UNISSUED"
    with pytest.raises(ports.PortRefusal) as excinfo:
        port.encounter(subject_ref="TEST_ONLY_BP1_ACTOR_A", resource=None, now=202)
    assert excinfo.value.code == "ADP010_ENCOUNTER_UNISSUED"


def test_can008_port_refuses_unissued_wrong_subject_and_revoked(occurrence):
    port = ports.CAN008RulePort()
    with pytest.raises(ports.PortRefusal) as excinfo:
        port.bind(rule=None, subject=occurrence.actor_id,
                  conditioning_class="ResolvedStructuralContext", now=202)
    assert excinfo.value.code == "CAN008_RULE_A_UNISSUED"
    rule = make_rule_a(occurrence, as_of=202)
    with pytest.raises(ports.PortRefusal) as excinfo:
        port.bind(rule=rule, subject="TEST_ONLY_OTHER_ACTOR",
                  conditioning_class="ResolvedStructuralContext", now=203)
    assert excinfo.value.code == "CAN008_RULE_A_SUBJECT_NOT_ALLOWED"
    with pytest.raises(ports.PortRefusal) as excinfo:
        port.bind(rule=ports.revoke(rule), subject=occurrence.actor_id,
                  conditioning_class="ResolvedStructuralContext", now=203)
    assert excinfo.value.code == "RESOURCE_REVOKED"
    future_rule = ports.test_only_rule_resource(
        resource_id="TEST_ONLY_BP2_CAN008_RULE_A_RESOURCE", version="1",
        body=dict(rule.body), issuer_ref=ports.__dict__ and dict(
            rule.body)["issuer_ref"], source_owner=rule.source_owner,
        permission_ref=rule.permission_ref, effective_from=300,
        readset_refs=("ResolvedStructuralContext",), currentness_as_of=202)
    with pytest.raises(ports.PortRefusal) as excinfo:
        port.bind(rule=future_rule, subject=occurrence.actor_id,
                  conditioning_class="ResolvedStructuralContext", now=203)
    assert excinfo.value.code == "RESOURCE_NOT_YET_EFFECTIVE"


def test_can011_port_requires_a_separate_target_owner(occurrence):
    rule_a = make_rule_a(occurrence, as_of=202)
    rule_a_hash = dict(rule_a.body)["rule_content_hash"]
    from bp2_joined.producer import RULE_A_ISSUER, TARGET_OWNER

    rule_t = make_target_rule(occurrence, rule_a_hash, as_of=202)
    port = ports.CAN011TargetPort(response_owner=RULE_A_ISSUER)
    assert port.bind_rule(rule=rule_t, now=203) is rule_t
    not_separate = ports.test_only_rule_resource(
        resource_id="TEST_ONLY_BP2_CAN011_RULE_T_RESOURCE", version="1",
        body=dict(rule_t.body), issuer_ref=RULE_A_ISSUER,
        source_owner="TEST_ONLY_CAN011_TARGET_OFFICE",
        permission_ref=rule_t.permission_ref, effective_from=202,
        readset_refs=("V3MS_PRACTICE",), currentness_as_of=202)
    with pytest.raises(ports.PortRefusal) as excinfo:
        port.bind_rule(rule=not_separate, now=203)
    assert excinfo.value.code == "CAN011_TARGET_ISSUER_NOT_SEPARATE"
    assert TARGET_OWNER != RULE_A_ISSUER
    with pytest.raises(ports.PortRefusal) as excinfo:
        port.bind_grant(grant=None, rule=rule_t, actor_id=occurrence.actor_id,
                        response_hash="R", before_target_hash="B", now=203)
    assert excinfo.value.code == "CAN011_TARGET_GRANT_UNISSUED"
    grant = make_target_grant(
        occurrence=occurrence, rule_t=rule_t, response_hash="R",
        before_target_hash="B", as_of=202)
    with pytest.raises(ports.PortRefusal) as excinfo:
        port.bind_grant(grant=grant, rule=rule_t, actor_id=occurrence.actor_id,
                        response_hash="WRONG", before_target_hash="B", now=203)
    assert excinfo.value.code == "RESOURCE_MISSING_READSET"
    inconsistent = ports.test_only_rule_resource(
        resource_id="TEST_ONLY_BP2_CAN011_TARGET_GRANT_RESOURCE", version="1",
        body={**dict(grant.body), "response_hash": "BODY"},
        issuer_ref=grant.issuer_ref, source_owner=grant.source_owner,
        permission_ref=grant.permission_ref, effective_from=grant.effective_from,
        readset_refs=("REQUESTED", "B"), currentness_as_of=grant.currentness_as_of)
    with pytest.raises(ports.PortRefusal) as excinfo:
        port.bind_grant(grant=inconsistent, rule=rule_t,
                        actor_id=occurrence.actor_id, response_hash="REQUESTED",
                        before_target_hash="B", now=203)
    assert excinfo.value.code == "CAN011_GRANT_RESPONSE_MISMATCH"


def test_e2_port_refuses_self_performance_and_wrong_state(occurrence):
    port = ports.E2OwnerPort()
    with pytest.raises(ports.PortRefusal) as excinfo:
        port.bind(receipt=None, actor_id=occurrence.actor_id,
                  act="inspect_with_tool", consumed_state_hash="S",
                  target_commit_time=202, now=212)
    assert excinfo.value.code == "E2_OWNER_RECEIPT_UNISSUED"
    resource = ports.test_only_rule_resource(
        resource_id="TEST_ONLY_E2", version="1",
        body={"actor_id": occurrence.actor_id, "act": "inspect_with_tool",
              "actuator_ref": occurrence.actor_id,
              "occurrence_ref": "TEST_ONLY_OCCURRENCE_X",
              "consumed_state_hash": "S", "action_time": 212},
        issuer_ref="TEST_ONLY_OWNER", source_owner="TEST_ONLY_OWNER",
        permission_ref="P", effective_from=0, readset_refs=("S",),
        currentness_as_of=212)
    with pytest.raises(ports.PortRefusal) as excinfo:
        port.bind(receipt=resource, actor_id=occurrence.actor_id,
                  act="inspect_with_tool", consumed_state_hash="S",
                  target_commit_time=202, now=212)
    assert excinfo.value.code == "E2_ACTUATOR_SELF_BOUND"
    resource2 = ports.test_only_rule_resource(
        resource_id="TEST_ONLY_E2", version="1",
        body={"actor_id": occurrence.actor_id, "act": "inspect_with_tool",
              "actuator_ref": "TEST_ONLY_ACTUATOR_X",
              "occurrence_ref": occurrence.actor_id,
              "consumed_state_hash": "S", "action_time": 212},
        issuer_ref="TEST_ONLY_OWNER", source_owner="TEST_ONLY_OWNER",
        permission_ref="P", effective_from=0, readset_refs=("S",),
        currentness_as_of=212)
    with pytest.raises(ports.PortRefusal) as excinfo:
        port.bind(receipt=resource2, actor_id=occurrence.actor_id,
                  act="inspect_with_tool", consumed_state_hash="S",
                  target_commit_time=202, now=212)
    assert excinfo.value.code == "E2_OCCURRENCE_SELF_BOUND"
    resource3 = ports.test_only_rule_resource(
        resource_id="TEST_ONLY_E2", version="1",
        body={"actor_id": occurrence.actor_id, "act": "inspect_with_tool",
              "actuator_ref": "TEST_ONLY_ACTUATOR_X",
              "occurrence_ref": "TEST_ONLY_OCCURRENCE_X",
              "consumed_state_hash": "OTHER", "action_time": 212},
        issuer_ref="TEST_ONLY_OWNER", source_owner="TEST_ONLY_OWNER",
        permission_ref="P", effective_from=0, readset_refs=("OTHER",),
        currentness_as_of=212)
    with pytest.raises(ports.PortRefusal) as excinfo:
        port.bind(receipt=resource3, actor_id=occurrence.actor_id,
                  act="inspect_with_tool", consumed_state_hash="S",
                  target_commit_time=202, now=212)
    assert excinfo.value.code == "E2_RECEIPT_CONSUMED_STATE_MISMATCH"


def test_source_closure_manifest_verifies():
    manifest = ports.__dict__  # keep flake quiet about unused import
    from bp2_joined import verify_sources

    verified = verify_sources()
    assert verified["file_count"] == 30
    assert manifest is not None
    origins = {row["origin_commit"] for row in verified["files"]}
    assert "b4e07ef515e9464c7bc8177e394ac29f4a4af72a" in origins
    assert "7faaa0722336231335d974bebc70c1282c79ce3e" in origins
    assert "6fa2939972ce5a2c0cc4f2b033946b276f1c2934" in origins


def test_severance_module_is_reachable_from_the_package():
    assert callable(run_severance)
