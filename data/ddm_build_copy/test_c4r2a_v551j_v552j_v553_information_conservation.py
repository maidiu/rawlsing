from __future__ import annotations

import json
import unittest

import pandas as pd

from data.ddm_build_copy import compile_v552j_structural_handoff as compiler
from data.ddm_build_copy import ddm_v552j_handoff as handoff
from data.ddm_build_copy import ddm_v553_canonical_harmonization as consumer


def packet(*, review: bool = False) -> dict:
    return {
        "run_id": "run",
        "packet_id": "packet-1",
        "packet_contract_hash": "packet-contract",
        "pattern_id": "pattern-1",
        "family_id": "JCFG-TEST",
        "family_label": "Test joint configuration",
        "family_type": "test",
        "family_structure_type": "test",
        "source": "TEST",
        "source_family": "TEST",
        "wave": "W1",
        "canonical_wave": "W1",
        "country_code": "XX",
        "v550j_pattern_index_artifact_hash": "a" * 64,
        "v550j_pattern_item_index_artifact_hash": "b" * 64,
        "v550j_relation_signature_artifact_hash": "c" * 64,
        "v550j_manifest_hash": "d" * 64,
        "v550j_readiness_report_hash": "e" * 64,
        "question_family_registry_hash": "f" * 64,
        "pattern_item_count": 2,
        "component_contract_complete": True,
        "component_order_integrity_status": "PASS",
        "component_contract_hashes_ordered_json": json.dumps(
            ["component-contract-1", "component-contract-2"]
        ),
        "joint_response_identity_signature": "joint-response-signature",
        "joint_empirical_distribution_signature": "joint-distribution-signature",
        "joint_semantic_signature": "joint-semantic-signature",
        "joint_orientation_signature": "joint-orientation-signature",
        "joint_topology_signature": "joint-topology-signature",
        "joint_target_signature": "joint-target-signature",
        "joint_structural_signature": "joint-structural-signature",
        "joint_component_measurement_signature": "joint-component-measurement",
        "joint_measurement_contract_hash": "joint-measurement-contract",
        "component_response_vector_json": json.dumps(["yes", "no"]),
        "component_semantic_vector_json": json.dumps(["support", "oppose"]),
        "component_orientation_vector_json": json.dumps(["positive", "negative"]),
        "component_topology_vector_json": json.dumps(["binary", "binary"]),
        "component_target_vector_json": json.dumps(["target-a", "target-b"]),
        "component_structural_vector_json": json.dumps(["axis-a", "axis-b"]),
        "component_denominator_vector_json": json.dumps([100, 100]),
        "component_pressure_linkage_vector_json": json.dumps(["v552_linkable", "v552_linkable"]),
        "component_empirical_distribution_ids_ordered_json": json.dumps(["dist-1", "dist-2"]),
        "joint_pattern_count_unweighted": 25,
        "joint_n_unweighted": 100,
        "joint_n_weighted": 98.5,
        "joint_weighted_count_basis": "respondent_weight",
        "joint_support_status": "underpowered" if review else "sufficient_support",
        "joint_support_gate_status": "review" if review else "pass",
        "joint_measurement_status": "COMPLETE_PATTERN_MEASUREMENT_CONTRACT",
        "joint_evidence_class": "joint_directional_relation_observation",
        "joint_semantic_authority_status": "CERTIFIED",
        "joint_directionality_authority_status": "CERTIFIED",
        "joint_family_target_authority_status": "CERTIFIED",
        "joint_structural_authority_status": "CERTIFIED",
        "joint_measurement_authority_status": "CERTIFIED",
        "joint_evidence_authority_status": "REVIEW_REQUIRED" if review else "CERTIFIED",
        "denominator_separation_status": "PASS",
        "certification_status": "REVIEW_REQUIRED_AUTHORITY_GAP" if review else "CERTIFIED_JOINT_RELATION_EVIDENCE",
        "review_required": review,
        "relation_axis_ids_json": json.dumps(["axis"]),
        "target_entity_ids_json": json.dumps(["target"]),
        "driver_facet_ids_json": json.dumps(["facet"]),
        "question_ids_json": json.dumps(["q1"]),
    }


def component(item_order: int) -> dict:
    return {
        "run_id": "run",
        "packet_id": "packet-1",
        "pattern_id": "pattern-1",
        "family_id": "JCFG-TEST",
        "item_order": item_order,
        "component_id": f"component-{item_order}",
        "component_contract_hash": f"component-contract-{item_order}",
        "source": "TEST",
        "source_family": "TEST",
        "canonical_wave": "W1",
        "country_code": "XX",
        "v550j_item_var_code": f"q{item_order}",
        "v550j_item_question_id": f"question-{item_order}",
        "v550j_item_role": f"governed-role-{item_order}",
        "v550j_item_semantic_response_role": "support" if item_order == 1 else "oppose",
        "v551_evidence_role": "relation",
        "v551_evidence_role_status": "CERTIFIED",
        "v551_atom_id": f"atom-{item_order}",
        "v551_atom_contract_hash": f"atom-contract-{item_order}",
        "v551_measurement_contract_hash": f"measurement-{item_order}",
        "v551_empirical_object_id": f"object-{item_order}",
        "v551_empirical_distribution_id": f"dist-{item_order}",
        "v551_n_unweighted": 100,
        "v551_n_respondents": 100,
        "v551_n_weighted": 98.5,
        "v551_semantic_role_authority_status": "CERTIFIED",
        "v551_response_semantics_authority_status": "CERTIFIED",
        "v551_directionality_authority_status": "CERTIFIED",
        "v551_evidence_basis": "exact_v551_atom",
        "v551_provenance_basis": f"source-row-{item_order}",
        "component_evidence_role": "relation_component",
        "component_certification_contribution": "relation_component",
        "component_v552_linkage_class": "v552_linkable",
        "schema_version": "v2.2.3",
        "compiler_version": "v551j_joint_evidence_contract_v2_2_3",
    }


def fact() -> dict:
    return {
        "run_id": "run",
        "source": "TEST",
        "source_family": "TEST",
        "wave": "W1",
        "canonical_wave": "W1",
        "country_code": "XX",
        "v552_structural_fact_id": "fact-1",
        "source_artifact": "v552_pressure_observation_index",
        "relation_axis_id": "axis",
        "target_entity_id": "target",
        "driver_facet_id": "facet",
        "question_id": "q1",
        "structural_channel_id": "channel",
        "horizon_constraint_id": "horizon",
        "structural_fact_lane": "primary_pressure",
        "structural_fact_grain": "empirical_distribution_pressure_observation",
        "structural_fact_status": "PRESENT",
        "pressure_score": 0.25,
        "pressure_score_status": "OBSERVED_NONZERO",
        "measurement_evidence_status": "PRESENT",
        "downstream_permission_status": "ALLOW",
    }


def state(permission: str = "ALLOW") -> dict:
    return {
        "run_integrity_status": "PASS",
        "evidence_status": "PRESENT",
        "downstream_permission_status": permission,
    }


def joined(*, review: bool = False, components: pd.DataFrame | None = None) -> pd.DataFrame:
    p = packet(review=review)
    result = handoff.build_v552j_join(
        run_id="run",
        v551j_certified=pd.DataFrame() if review else pd.DataFrame([p]),
        v551j_review=pd.DataFrame([p]) if review else pd.DataFrame(),
        v551j_components=components if components is not None else pd.DataFrame([component(1), component(2)]),
        v552_structural_facts=pd.DataFrame([fact()]),
        v551j_state=state("DENY" if review else "ALLOW"),
        v552_state=state(),
        v551j_manifest_sha256="1" * 64,
        v552_manifest_sha256="2" * 64,
    )
    return result["join_index"]


class TestC4R2AInformationConservation(unittest.TestCase):
    def test_all_seven_banked_gaps_round_trip_through_actual_consumer(self):
        join = joined()
        self.assertEqual(len(join), 1)
        row = join.iloc[0]
        self.assertEqual(row["v551j_conservation_status"], handoff.V552J_CONSERVATION_STATUS)
        self.assertEqual(row["join_permission"], "ALLOW")

        compatibility = compiler._v553_compatibility_frame(join)
        envelopes = consumer._read_v551j_conservation_envelopes(compatibility)
        self.assertEqual(len(envelopes), 1)
        envelope = envelopes[0]
        p = envelope["packet"]
        components = envelope["components"]

        # Gap 1: source-native joint-configuration semantic identity.
        self.assertEqual(p["family_id"], "JCFG-TEST")
        self.assertEqual(p["pattern_id"], "pattern-1")
        self.assertEqual(p["joint_semantic_signature"], "joint-semantic-signature")

        # Gap 2: same-respondent premise / joint measurement identity.
        self.assertEqual(row["v551j_same_respondent_premise_status"], "PRESERVED_V550J_RESPONDENT_GROUPED_PATTERN_VIA_V551J_JOINT_IDENTITY")
        self.assertEqual(p["joint_response_identity_signature"], "joint-response-signature")
        self.assertEqual(p["joint_n_unweighted"], 100)
        self.assertEqual(p["joint_measurement_contract_hash"], "joint-measurement-contract")

        # Gap 3: component identity, ordering and contracts.
        self.assertEqual([c["component_id"] for c in components], ["component-1", "component-2"])
        self.assertEqual([c["item_order"] for c in components], [1, 2])
        self.assertEqual([c["component_contract_hash"] for c in components], ["component-contract-1", "component-contract-2"])

        # Gap 4: component-level and multi-axis authority vector.
        self.assertEqual(p["joint_semantic_authority_status"], "CERTIFIED")
        self.assertEqual(p["joint_directionality_authority_status"], "CERTIFIED")
        self.assertEqual(p["joint_family_target_authority_status"], "CERTIFIED")
        self.assertEqual(p["joint_structural_authority_status"], "CERTIFIED")
        self.assertEqual(p["joint_measurement_authority_status"], "CERTIFIED")
        self.assertEqual(p["joint_evidence_authority_status"], "CERTIFIED")
        self.assertTrue(all(c["v551_directionality_authority_status"] == "CERTIFIED" for c in components))

        # Gap 5: component and certification-contribution roles.
        self.assertEqual([c["v550j_item_role"] for c in components], ["governed-role-1", "governed-role-2"])
        self.assertTrue(all(c["component_certification_contribution"] == "relation_component" for c in components))

        # Gap 6: non-scalar vectors remain exact; readiness is explicitly derived-only.
        self.assertEqual(json.loads(p["component_response_vector_json"]), ["yes", "no"])
        self.assertEqual(json.loads(p["component_semantic_vector_json"]), ["support", "oppose"])
        self.assertEqual(row["v551j_scalarization_policy"], handoff.V552J_NONSCALAR_POLICY)
        altered = compatibility.copy()
        altered.loc[0, "readiness_score"] = 0.0
        self.assertEqual(
            consumer._read_v551j_conservation_envelopes(altered)[0]["packet"]["component_response_vector_json"],
            p["component_response_vector_json"],
        )

        # Gap 7: denominator/context certification contract.
        self.assertEqual(p["denominator_separation_status"], "PASS")
        self.assertEqual(json.loads(p["component_denominator_vector_json"]), [100, 100])
        self.assertEqual([c["v551_n_respondents"] for c in components], [100, 100])
        self.assertEqual([c["v551_empirical_distribution_id"] for c in components], ["dist-1", "dist-2"])

    def test_component_order_tamper_is_rejected_by_actual_consumer(self):
        compatibility = compiler._v553_compatibility_frame(joined())
        components = json.loads(compatibility.loc[0, "v551j_components_semantics_json"])
        components.reverse()
        compatibility.loc[0, "v551j_components_semantics_json"] = json.dumps(
            components, sort_keys=True, separators=(",", ":")
        )
        with self.assertRaisesRegex(ValueError, "HASH_MISMATCH|ORDER_OR_HASH_MISMATCH"):
            consumer._read_v551j_conservation_envelopes(compatibility)

    def test_envelope_hash_tamper_is_rejected_by_actual_consumer(self):
        compatibility = compiler._v553_compatibility_frame(joined())
        compatibility.loc[0, "v551j_conservation_envelope_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "HASH_MISMATCH"):
            consumer._read_v551j_conservation_envelopes(compatibility)

    def test_missing_component_semantics_fail_closed_before_allow(self):
        p = packet()
        result = handoff.build_v552j_join(
            run_id="run",
            v551j_certified=pd.DataFrame([p]),
            v551j_review=pd.DataFrame(),
            v551j_components=pd.DataFrame(),
            v552_structural_facts=pd.DataFrame([fact()]),
            v551j_state=state(),
            v552_state=state(),
        )
        row = result["join_index"].iloc[0]
        self.assertEqual(row["join_permission"], "DENY")
        self.assertEqual(row["repair_debt_status"], "CONSERVATION_GAP")
        self.assertNotEqual(row["v551j_conservation_status"], handoff.V552J_CONSERVATION_STATUS)
        self.assertEqual(result["state"]["evidence_status"], "APPLICABLE_UNRESOLVED")
        self.assertEqual(result["metrics"]["conservation_gap_count"], 1)

    def test_review_lane_keeps_exact_envelope_but_never_promotes_to_allow(self):
        join = joined(review=True)
        row = join.iloc[0]
        self.assertEqual(row["v551j_conservation_status"], handoff.V552J_CONSERVATION_STATUS)
        self.assertEqual(row["v551j_lane"], "reviewable_context")
        self.assertEqual(row["join_permission"], "REVIEW_ONLY")
        envelope = consumer._read_v551j_conservation_envelopes(
            compiler._v553_compatibility_frame(join)
        )[0]
        self.assertEqual(envelope["packet"]["certification_status"], "REVIEW_REQUIRED_AUTHORITY_GAP")

    def test_actual_v553_contract_requires_conservation_columns(self):
        for column in (
            "v551j_conservation_status",
            "v551j_conservation_envelope_sha256",
            "v551j_joint_packet_semantics_json",
            "v551j_components_semantics_json",
            "v551j_component_count",
            "v551j_same_respondent_premise_status",
            "v551j_scalarization_policy",
        ):
            self.assertIn(column, consumer.V553_CANONICAL_INDEX_REQUIRED_COLUMNS)


if __name__ == "__main__":
    unittest.main()
