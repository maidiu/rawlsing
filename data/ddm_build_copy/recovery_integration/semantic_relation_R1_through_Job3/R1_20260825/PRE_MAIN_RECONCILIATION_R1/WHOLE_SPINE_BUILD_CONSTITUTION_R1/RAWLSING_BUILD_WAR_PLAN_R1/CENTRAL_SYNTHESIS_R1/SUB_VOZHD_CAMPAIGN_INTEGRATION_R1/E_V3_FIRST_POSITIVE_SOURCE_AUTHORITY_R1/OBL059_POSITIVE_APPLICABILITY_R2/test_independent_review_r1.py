"""Fresh independent bounded review for frozen OBL059 R2.

This file is review-only. It does not repair or modify the candidate.
"""
from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / "positive_applicability_authority_r2.py"

spec = importlib.util.spec_from_file_location("_obl059_r2_review_target", CANDIDATE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load frozen R2 candidate: {CANDIDATE}")
r2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r2)


def fixture():
    actor = "urn:rawlsing:noncurrent-synthetic:v3:actor:obl059:r2-review"
    world = "urn:rawlsing:noncurrent-synthetic:v3:world:obl059:r2-review"
    time = "urn:rawlsing:noncurrent-synthetic:v3:time:obl059:r2-review"
    opportunity = "urn:rawlsing:noncurrent-synthetic:v3:adp010-opportunity:obl059:r2-review"
    return {
        "execution_scope": r2.SYNTHETIC_SCOPE,
        "actor_id": actor,
        "subject_id": r2.FIRST_CANARY_SUBJECT_ID,
        "world_id": world,
        "time_id": time,
        "adp010_opportunity_id": opportunity,
        "opportunity": {
            "actor_id": actor,
            "subject_id": r2.FIRST_CANARY_SUBJECT_ID,
            "world_id": world,
            "time_id": time,
            "opportunity_id": opportunity,
            "consumer_rule": r2.ADP010_CONSUMER,
        },
        "evidence": {
            "subject_classification": {
                "semantic_owner": "NONCURRENT_SYNTHETIC_OBL048_COMPETENT_SOURCE@R2_REVIEW",
                "jurisdiction": "OBL048_SUBJECT_CLASSIFICATION",
                "subject_id": r2.FIRST_CANARY_SUBJECT_ID,
                "predicate": r2.SUBJECT_CLASSIFICATION_PREDICATE,
                "fresh_for_time_id": time,
                "stale": False,
            },
            "actor_activation": {
                "semantic_owner": r2.ADP007_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "state": "ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
            "developmental_phase": {
                "semantic_owner": r2.ADP008_OWNER,
                "actor_id": actor,
                "world_id": world,
                "time_id": time,
                "phase": "V3DP_DEVELOPMENT_ACTIVE",
                "fresh_for_time_id": time,
                "stale": False,
            },
        },
    }


class OBL059R2IndependentReview(unittest.TestCase):
    def assert_closed(self, packet, reason_prefix):
        try:
            result = r2.evaluate_direct_positive_applicability(packet)
        except Exception as exc:  # review assertion: malformed input must not escape as an exception
            self.fail(f"malformed binding escaped negative-receipt path: {type(exc).__name__}: {exc}")
        self.assertEqual(result["decision"], r2.NEGATIVE_DECISION, result)
        self.assertTrue(result["reason"].startswith(reason_prefix), result)
        json.dumps(result, sort_keys=True)
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
        return result

    def test_01_known_bytes_case_remains_closed(self):
        packet = fixture()
        packet["actor_id"] = b"not-a-valid-id"
        self.assert_closed(packet, "MALFORMED_BINDING:actor_id")

    def test_02_mapping_with_non_json_key_required_binding_closes(self):
        packet = fixture()
        packet["actor_id"] = {b"non-json-key": "value"}
        self.assert_closed(packet, "MALFORMED_BINDING:actor_id")

    def test_03_circular_required_binding_closes(self):
        packet = fixture()
        circular = []
        circular.append(circular)
        packet["world_id"] = circular
        self.assert_closed(packet, "MALFORMED_BINDING:world_id")

    def test_04_frozen_revision_identity_is_r2(self):
        self.assertEqual(
            r2.R2_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R2",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
