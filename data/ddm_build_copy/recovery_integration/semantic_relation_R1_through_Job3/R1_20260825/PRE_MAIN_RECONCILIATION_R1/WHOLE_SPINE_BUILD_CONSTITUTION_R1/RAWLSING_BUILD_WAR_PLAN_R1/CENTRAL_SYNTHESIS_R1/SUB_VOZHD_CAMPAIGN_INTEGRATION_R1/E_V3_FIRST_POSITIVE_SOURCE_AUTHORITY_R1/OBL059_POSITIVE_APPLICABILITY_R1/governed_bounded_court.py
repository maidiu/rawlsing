"""Lane-local governed bounded court for OBL059 R1."""

from __future__ import annotations

import copy
import json
import unittest

from positive_applicability_authority import (
    ADP007_OWNER,
    ADP008_OWNER,
    ADP010_CONSUMER,
    AUTHORITY_ID,
    FIRST_CANARY_SUBJECT_ID,
    NEGATIVE_DECISION,
    POSITIVE_DECISION,
    SYNTHETIC_SCOPE,
    evaluate_direct_positive_applicability,
)


def fixture():
    actor = "urn:rawlsing:noncurrent-synthetic:v3:actor:obl059:r1"
    world = "urn:rawlsing:noncurrent-synthetic:v3:world:obl059:r1"
    time = "urn:rawlsing:noncurrent-synthetic:v3:time:obl059:r1"
    opportunity = "urn:rawlsing:noncurrent-synthetic:v3:adp010-opportunity:obl059:r1"
    return {
        "execution_scope": SYNTHETIC_SCOPE,
        "actor_id": actor,
        "subject_id": FIRST_CANARY_SUBJECT_ID,
        "world_id": world,
        "time_id": time,
        "adp010_opportunity_id": opportunity,
        "opportunity": {
            "actor_id": actor,
            "subject_id": FIRST_CANARY_SUBJECT_ID,
            "world_id": world,
            "time_id": time,
            "opportunity_id": opportunity,
            "consumer_rule": ADP010_CONSUMER,
        },
        "evidence": {
            "subject_classification": {
                "semantic_owner": "NONCURRENT_SYNTHETIC_OBL048_COMPETENT_SOURCE@R1",
                "jurisdiction": "OBL048_SUBJECT_CLASSIFICATION",
                "subject_id": FIRST_CANARY_SUBJECT_ID,
                "predicate": "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
                "fresh_for_time_id": time,
                "stale": False,
            },
            "actor_activation": {
                "semantic_owner": ADP007_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "state": "ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
            "developmental_phase": {
                "semantic_owner": ADP008_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "phase": "V3DP_DEVELOPMENT_ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
        },
    }


class Court(unittest.TestCase):
    def assert_closed(self, packet, reason_prefix=None):
        result = evaluate_direct_positive_applicability(packet)
        self.assertEqual(result["decision"], NEGATIVE_DECISION, result)
        self.assertFalse(result["project_current_state_created"])
        self.assertFalse(result["actor_created_or_activated"])
        self.assertFalse(result["adp008_phase_transition_executed"])
        self.assertFalse(result["adp019_occurrence_admitted"])
        self.assertFalse(result["causal_use_permission_owned"])
        self.assertFalse(result["contact_witness_independence_owned"])
        self.assertFalse(result["encounter_created"])
        self.assertFalse(result["oee_realized"])
        self.assertFalse(result["obl055_executed"])
        self.assertFalse(result["current_positive_obl056_installed"])
        if reason_prefix:
            self.assertTrue(result["reason"].startswith(reason_prefix), result)
        return result

    def test_01_positive_noncurrent_synthetic_exact_scope(self):
        result = evaluate_direct_positive_applicability(fixture())
        self.assertEqual(result["decision"], POSITIVE_DECISION)
        self.assertEqual(result["authority_id"], AUTHORITY_ID)
        self.assertEqual(result["execution_scope"], SYNTHETIC_SCOPE)
        self.assertFalse(result["project_current_state_created"])
        self.assertEqual(
            [x["kind"] for x in result["evidence_ownership"]],
            ["subject_classification", "actor_activation", "developmental_phase"],
        )

    def test_02_project_current_issuance_blocked(self):
        p = fixture()
        p["execution_scope"] = "PROJECT_CURRENT"
        self.assert_closed(p, "PROJECT_CURRENT_ISSUANCE_FORBIDDEN")

    def test_03_each_required_binding_missing_fails_closed(self):
        for key in ("actor_id", "subject_id", "world_id", "time_id", "adp010_opportunity_id"):
            with self.subTest(key=key):
                p = fixture()
                del p[key]
                self.assert_closed(p, f"MISSING_BINDING:{key}")

    def test_04_each_required_binding_malformed_fails_closed(self):
        for key, bad in (
            ("actor_id", ""),
            ("subject_id", 7),
            ("world_id", " has-space"),
            ("time_id", "bad time"),
            ("adp010_opportunity_id", None),
        ):
            with self.subTest(key=key):
                p = fixture()
                p[key] = bad
                self.assert_closed(p, f"MALFORMED_BINDING:{key}")

    def test_05_wrong_first_canary_subject_fails(self):
        p = fixture()
        p["subject_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-subject"
        p["opportunity"]["subject_id"] = p["subject_id"]
        p["evidence"]["subject_classification"]["subject_id"] = p["subject_id"]
        self.assert_closed(p, "WRONG_FIRST_CANARY_SUBJECT")

    def test_06_opportunity_missing_fails(self):
        p = fixture()
        del p["opportunity"]
        self.assert_closed(p, "OPPORTUNITY_BINDING_MISSING_OR_MALFORMED")

    def test_07_wrong_actor_in_opportunity_fails(self):
        p = fixture()
        p["opportunity"]["actor_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-actor"
        self.assert_closed(p, "OPPORTUNITY_SCOPE_MISMATCH:actor_id")

    def test_08_wrong_world_in_opportunity_fails(self):
        p = fixture()
        p["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-world"
        self.assert_closed(p, "OPPORTUNITY_SCOPE_MISMATCH:world_id")

    def test_09_wrong_time_in_opportunity_fails(self):
        p = fixture()
        p["opportunity"]["time_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-time"
        self.assert_closed(p, "OPPORTUNITY_SCOPE_MISMATCH:time_id")

    def test_10_wrong_opportunity_id_fails(self):
        p = fixture()
        p["opportunity"]["opportunity_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-opportunity"
        self.assert_closed(p, "OPPORTUNITY_SCOPE_MISMATCH:opportunity_id")

    def test_11_wrong_consumer_rule_fails(self):
        p = fixture()
        p["opportunity"]["consumer_rule"] = "OTHER_RULE"
        self.assert_closed(p, "OPPORTUNITY_SCOPE_MISMATCH:consumer_rule")

    def test_12_structural_classification_alone_is_insufficient(self):
        p = fixture()
        p["evidence"] = {"subject_classification": p["evidence"]["subject_classification"]}
        self.assert_closed(p, "ACTOR_ACTIVATION_EVIDENCE_MISSING")

    def test_13_routing_is_insufficient(self):
        p = fixture()
        p["evidence"] = {"routing": {"route": "ADP-010"}}
        self.assert_closed(p, "STRUCTURAL_CLASSIFICATION_EVIDENCE_MISSING")

    def test_14_v554_can001_can003_not_alias_authority(self):
        for alias in ("V554", "CAN-001", "CAN-003"):
            with self.subTest(alias=alias):
                p = fixture()
                p["claimed_positive_applicability_source"] = alias
                self.assert_closed(p, f"FORBIDDEN_SOURCE_AUTHORITY_ALIAS:{alias}")

    def test_15_adp010_cannot_self_authorize(self):
        p = fixture()
        p["claimed_positive_applicability_source"] = ADP010_CONSUMER
        self.assert_closed(p, "FORBIDDEN_SOURCE_AUTHORITY_ALIAS")

    def test_16_routing_cannot_alias_authority(self):
        p = fixture()
        p["claimed_positive_applicability_source"] = "ROUTING"
        self.assert_closed(p, "FORBIDDEN_SOURCE_AUTHORITY_ALIAS:ROUTING")

    def test_17_unrecognized_source_claim_fails(self):
        p = fixture()
        p["claimed_positive_applicability_source"] = "SOME_DOWNSTREAM_CONSUMER"
        self.assert_closed(p, "UNRECOGNIZED_SOURCE_AUTHORITY_CLAIM")

    def test_18_subject_classification_stale_fails(self):
        p = fixture()
        p["evidence"]["subject_classification"]["stale"] = True
        self.assert_closed(p, "STALE_OR_UNDECLARED_FRESHNESS:subject_classification")

    def test_19_actor_activation_stale_fails(self):
        p = fixture()
        p["evidence"]["actor_activation"]["stale"] = True
        self.assert_closed(p, "STALE_OR_UNDECLARED_FRESHNESS:actor_activation")

    def test_20_phase_stale_fails(self):
        p = fixture()
        p["evidence"]["developmental_phase"]["stale"] = True
        self.assert_closed(p, "STALE_OR_UNDECLARED_FRESHNESS:developmental_phase")

    def test_21_wrong_actor_runtime_receipt_fails(self):
        p = fixture()
        p["evidence"]["actor_activation"]["actor_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-actor"
        self.assert_closed(p, "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id")

    def test_22_wrong_world_runtime_receipt_fails(self):
        p = fixture()
        p["evidence"]["actor_activation"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-world"
        self.assert_closed(p, "ACTOR_ACTIVATION_SCOPE_MISMATCH:world_id")

    def test_23_wrong_time_runtime_receipt_fails(self):
        p = fixture()
        p["evidence"]["actor_activation"]["time_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-time"
        self.assert_closed(p, "ACTOR_ACTIVATION_SCOPE_MISMATCH:time_id")

    def test_24_wrong_actor_authority_fails(self):
        p = fixture()
        p["evidence"]["actor_activation"]["semantic_owner"] = ADP010_CONSUMER
        self.assert_closed(p, "ACTOR_ACTIVATION_WRONG_AUTHORITY")

    def test_25_wrong_phase_authority_fails(self):
        p = fixture()
        p["evidence"]["developmental_phase"]["semantic_owner"] = ADP010_CONSUMER
        self.assert_closed(p, "DEVELOPMENTAL_PHASE_WRONG_AUTHORITY")

    def test_26_wrong_phase_fails(self):
        p = fixture()
        p["evidence"]["developmental_phase"]["phase"] = "V3DP_OTHER"
        self.assert_closed(p, "DEVELOPMENTAL_PHASE_NOT_ACTIVE")

    def test_27_wrong_time_freshness_fails(self):
        p = fixture()
        p["evidence"]["actor_activation"]["fresh_for_time_id"] = "urn:rawlsing:noncurrent-synthetic:other-time"
        self.assert_closed(p, "WRONG_TIME_FRESHNESS:actor_activation")

    def test_28_consumed_evidence_owners_are_preserved_not_absorbed(self):
        p = fixture()
        owner = p["evidence"]["subject_classification"]["semantic_owner"]
        result = evaluate_direct_positive_applicability(p)
        owners = {x["kind"]: x["semantic_owner"] for x in result["evidence_ownership"]}
        self.assertEqual(owners["subject_classification"], owner)
        self.assertEqual(owners["actor_activation"], ADP007_OWNER)
        self.assertEqual(owners["developmental_phase"], ADP008_OWNER)
        self.assertNotEqual(owners["subject_classification"], AUTHORITY_ID)
        self.assertNotEqual(owners["actor_activation"], AUTHORITY_ID)
        self.assertNotEqual(owners["developmental_phase"], AUTHORITY_ID)

    def test_29_candidate_never_owns_forbidden_effects_even_when_positive(self):
        result = evaluate_direct_positive_applicability(fixture())
        self.assertEqual(result["decision"], POSITIVE_DECISION)
        for key in (
            "project_current_state_created",
            "actor_created_or_activated",
            "adp008_phase_transition_executed",
            "adp019_occurrence_admitted",
            "causal_use_permission_owned",
            "contact_witness_independence_owned",
            "encounter_created",
            "oee_realized",
            "obl055_executed",
            "current_positive_obl056_installed",
        ):
            self.assertFalse(result[key], key)

    def test_30_positive_receipt_is_exactly_bound_and_deterministic(self):
        p = fixture()
        a = evaluate_direct_positive_applicability(p)
        b = evaluate_direct_positive_applicability(copy.deepcopy(p))
        self.assertEqual(a, b)
        self.assertEqual(a["bindings"]["actor_id"], p["actor_id"])
        self.assertEqual(a["bindings"]["subject_id"], p["subject_id"])
        self.assertEqual(a["bindings"]["world_id"], p["world_id"])
        self.assertEqual(a["bindings"]["time_id"], p["time_id"])
        self.assertEqual(a["bindings"]["adp010_opportunity_id"], p["adp010_opportunity_id"])


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Court)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(
        json.dumps(
            {
                "court": "OBL059_R1_GOVERNED_BOUNDED_COURT",
                "tests_run": result.testsRun,
                "failures": len(result.failures),
                "errors": len(result.errors),
                "successful": result.wasSuccessful(),
                "execution_scope": SYNTHETIC_SCOPE,
                "project_current_state_created": False,
            },
            sort_keys=True,
        )
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
