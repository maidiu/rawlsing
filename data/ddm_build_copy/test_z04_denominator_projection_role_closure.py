from __future__ import annotations

import json
import unittest

import pandas as pd

from data.ddm_build_copy import compile_v552j_structural_handoff as compiler
from data.ddm_build_copy import ddm_v552_structural as v552
from data.ddm_build_copy import ddm_v552j_handoff as handoff
from data.ddm_build_copy import ddm_v553_canonical_harmonization as consumer


def _packet() -> dict:
    denominator_vector = [
        {"item_order": 1, "empirical_distribution_id": "dist-relation", "n_respondents": 100},
        {"item_order": 2, "empirical_distribution_id": "", "n_respondents": None},
    ]
    return {
        "run_id": "z04-run", "packet_id": "z04-packet", "packet_contract_hash": "packet-contract",
        "pattern_id": "z04-pattern", "family_id": "JCFG-Z04", "source": "TEST", "source_family": "TEST",
        "wave": "W1", "canonical_wave": "W1", "country_code": "XX", "pattern_item_count": 2,
        "component_contract_hashes_ordered_json": json.dumps(["component-contract-1", "component-contract-2"]),
        "joint_response_identity_signature": "joint-response", "joint_semantic_signature": "joint-semantic",
        "joint_orientation_signature": "joint-orientation", "joint_topology_signature": "joint-topology",
        "joint_target_signature": "joint-target", "joint_structural_signature": "joint-structural",
        "joint_measurement_contract_hash": "joint-measurement",
        "component_response_vector_json": json.dumps(["yes", "context"]),
        "component_semantic_vector_json": json.dumps(["support", "context"]),
        "component_orientation_vector_json": json.dumps(["positive", "not_applicable"]),
        "component_topology_vector_json": json.dumps(["binary", "context"]),
        "component_target_vector_json": json.dumps(["target", ""]),
        "component_structural_vector_json": json.dumps(["axis", ""]),
        "component_denominator_vector_json": json.dumps(denominator_vector),
        "denominator_separation_status": "PASS",
        "joint_pattern_count_unweighted": 25, "joint_n_unweighted": 80,
        "joint_n_weighted": None, "joint_support_status": "sufficient_support",
        "joint_semantic_authority_status": "CERTIFIED", "joint_directionality_authority_status": "CERTIFIED",
        "joint_family_target_authority_status": "CERTIFIED", "joint_structural_authority_status": "CERTIFIED",
        "joint_measurement_authority_status": "CERTIFIED", "joint_evidence_authority_status": "CERTIFIED",
        "certification_status": "CERTIFIED_JOINT_RELATION_EVIDENCE_WITH_CONTEXT", "review_required": False,
        "v550j_pattern_index_artifact_hash": "a" * 64, "v550j_pattern_item_index_artifact_hash": "b" * 64,
        "v550j_manifest_hash": "c" * 64, "relation_axis_ids_json": json.dumps(["axis"]),
        "target_entity_ids_json": json.dumps(["target"]), "driver_facet_ids_json": json.dumps(["facet"]),
        "question_ids_json": json.dumps(["q1"]),
    }


def _components(*, erase_relation_role: bool = False) -> pd.DataFrame:
    return pd.DataFrame([
        {
            "run_id": "z04-run", "packet_id": "z04-packet", "pattern_id": "z04-pattern", "family_id": "JCFG-Z04",
            "item_order": 1, "component_id": "component-1", "component_contract_hash": "component-contract-1",
            "source": "TEST", "source_family": "TEST", "canonical_wave": "W1", "country_code": "XX",
            "v550j_item_role": "substantive_response", "component_evidence_role": "relation_component",
            "component_certification_contribution": "relation_component",
            "v551_evidence_role": "CONTEXT_EVIDENCE" if erase_relation_role else "RELATION_EVIDENCE",
            "v551_evidence_role_status": "VALID_CONTEXT_EVIDENCE_ROLE" if erase_relation_role else "VALID_RELATION_EVIDENCE_ROLE",
            "v551_empirical_distribution_id": "dist-relation", "v551_n_respondents": 100,
            "v551_semantic_role_authority_status": "CERTIFIED", "v551_response_semantics_authority_status": "CERTIFIED",
            "v551_directionality_authority_status": "CERTIFIED", "v551_measurement_contract_hash": "measure-1",
            "v551_atom_id": "atom-1", "v551_atom_contract_hash": "atom-contract-1",
            "schema_version": "v2.2.3", "compiler_version": "v551j_joint_evidence_contract_v2_2_3",
        },
        {
            "run_id": "z04-run", "packet_id": "z04-packet", "pattern_id": "z04-pattern", "family_id": "JCFG-Z04",
            "item_order": 2, "component_id": "component-2", "component_contract_hash": "component-contract-2",
            "source": "TEST", "source_family": "TEST", "canonical_wave": "W1", "country_code": "XX",
            "v550j_item_role": "context_only", "component_evidence_role": "context_component",
            "component_certification_contribution": "context_component",
            "v551_evidence_role": "CONTEXT_EVIDENCE", "v551_evidence_role_status": "VALID_CONTEXT_EVIDENCE_ROLE",
            "v551_empirical_distribution_id": "", "v551_n_respondents": None,
            "v551_semantic_role_authority_status": "CERTIFIED", "v551_response_semantics_authority_status": "CERTIFIED",
            "v551_directionality_authority_status": "NOT_APPLICABLE", "v551_measurement_contract_hash": "context-measure",
            "v551_atom_id": "atom-context", "v551_atom_contract_hash": "atom-contract-context",
            "schema_version": "v2.2.3", "compiler_version": "v551j_joint_evidence_contract_v2_2_3",
        },
    ])


def _fact() -> dict:
    return {
        "run_id": "z04-run", "source": "TEST", "source_family": "TEST", "wave": "W1", "canonical_wave": "W1",
        "country_code": "XX", "v552_structural_fact_id": "fact-1", "source_artifact": "v552_pressure_observation_index",
        "relation_axis_id": "axis", "target_entity_id": "target", "driver_facet_id": "facet", "question_id": "q1",
        "structural_channel_id": "channel", "horizon_constraint_id": "horizon",
        "structural_fact_lane": "primary_pressure", "structural_fact_grain": "empirical_distribution_pressure_observation",
        "structural_fact_status": "PRESENT", "pressure_score": 0.25, "pressure_score_status": "OBSERVED_NONZERO",
        "measurement_evidence_status": "PRESENT", "downstream_permission_status": "ALLOW",
    }


def _state() -> dict:
    return {"run_integrity_status": "PASS", "evidence_status": "PRESENT", "downstream_permission_status": "ALLOW"}


def _join(*, components: pd.DataFrame | None = None) -> pd.DataFrame:
    p = _packet()
    result = handoff.build_v552j_join(
        run_id="z04-run", v551j_certified=pd.DataFrame([p]), v551j_review=pd.DataFrame(),
        v551j_components=_components() if components is None else components,
        v552_structural_facts=pd.DataFrame([_fact()]), v551j_state=_state(), v552_state=_state(),
        v551j_manifest_sha256="1" * 64, v552_manifest_sha256="2" * 64,
    )
    return result["join_index"]


class TestZ04DenominatorProjectionRoleClosure(unittest.TestCase):
    def test_joint_denominator_and_relation_denominator_remain_distinct_while_context_has_no_forced_denominator(self):
        join = _join()
        self.assertEqual(join.iloc[0]["join_permission"], "ALLOW")
        envelope = consumer._read_v551j_conservation_envelopes(compiler._v553_compatibility_frame(join))[0]
        packet = envelope["packet"]
        components = envelope["components"]
        self.assertEqual(packet["joint_n_unweighted"], 80)
        self.assertEqual(components[0]["v551_n_respondents"], 100)
        self.assertIsNone(components[1]["v551_n_respondents"])
        self.assertEqual(
            json.loads(packet["component_denominator_vector_json"]),
            [
                {"item_order": 1, "empirical_distribution_id": "dist-relation", "n_respondents": 100},
                {"item_order": 2, "empirical_distribution_id": "", "n_respondents": None},
            ],
        )

    def test_denominator_vector_substitution_fails_closed_even_with_rehashed_envelope(self):
        compat = compiler._v553_compatibility_frame(_join())
        packet = json.loads(compat.loc[0, "v551j_joint_packet_semantics_json"])
        components = json.loads(compat.loc[0, "v551j_components_semantics_json"])
        packet["component_denominator_vector_json"] = json.dumps([
            {"item_order": 1, "empirical_distribution_id": "dist-relation", "n_respondents": 80},
            {"item_order": 2, "empirical_distribution_id": "", "n_respondents": 80},
        ])
        compat.loc[0, "v551j_joint_packet_semantics_json"] = json.dumps(packet, sort_keys=True, separators=(",", ":"))
        compat.loc[0, "v551j_conservation_envelope_sha256"] = handoff._conservation_hash(
            packet, components, handoff.V552J_NONSCALAR_POLICY
        )
        with self.assertRaisesRegex(ValueError, "DENOMINATOR_VECTOR_MISMATCH"):
            consumer._read_v551j_conservation_envelopes(compat)

    def test_fail_rom_relation_evidence_role_erasure_cannot_pass_on_field_presence(self):
        result = handoff.build_v552j_join(
            run_id="z04-run", v551j_certified=pd.DataFrame([_packet()]), v551j_review=pd.DataFrame(),
            v551j_components=_components(erase_relation_role=True),
            v552_structural_facts=pd.DataFrame([_fact()]), v551j_state=_state(), v552_state=_state(),
        )
        row = result["join_index"].iloc[0]
        self.assertEqual(row["join_permission"], "DENY")
        self.assertEqual(row["repair_debt_status"], "CONSERVATION_GAP")
        self.assertIn("relation_authority_role_erased", row["v551j_conservation_blockers_json"])

    def test_actual_consumer_rechecks_relation_authority_role_after_valid_hash(self):
        compat = compiler._v553_compatibility_frame(_join())
        packet = json.loads(compat.loc[0, "v551j_joint_packet_semantics_json"])
        components = json.loads(compat.loc[0, "v551j_components_semantics_json"])
        components[0]["v551_evidence_role"] = "CONTEXT_EVIDENCE"
        components[0]["v551_evidence_role_status"] = "VALID_CONTEXT_EVIDENCE_ROLE"
        compat.loc[0, "v551j_components_semantics_json"] = json.dumps(components, sort_keys=True, separators=(",", ":"))
        compat.loc[0, "v551j_conservation_envelope_sha256"] = handoff._conservation_hash(
            packet, components, handoff.V552J_NONSCALAR_POLICY
        )
        with self.assertRaisesRegex(ValueError, "RELATION_AUTHORITY_ROLE_ERASED|RELATION_AUTHORITY_ROLE_IDENTITY_INVALID"):
            consumer._read_v551j_conservation_envelopes(compat)

    def test_v552_consumes_v551_canonical_projection_and_ignores_conflicting_label_code_order_inputs(self):
        base = {
            "v551_signed_side": "positive", "v551_signed_intensity": 0.75,
            "v551_projection_rule_id": "governed-rule", "v551_projection_authority_hash": "a" * 64,
            "response_direction": "negative", "response_intensity": 999,
            "response_label": "NEGATIVE LABEL", "response_value_raw": "999", "response_value_normalized": "opposite",
            "ordinal_rank": -100, "scale_direction": "reversed",
        }
        a = v552.resolve_v552_signed_component(base)
        altered = dict(base)
        altered.update(response_direction="neutral", response_intensity=-123, response_label="OTHER", response_value_raw="x",
                       response_value_normalized="y", ordinal_rank=999, scale_direction="forward")
        b = v552.resolve_v552_signed_component(altered)
        self.assertEqual(a.canonical_signed_component, 0.75)
        self.assertEqual(b.canonical_signed_component, 0.75)
        self.assertEqual(a.scale_encoding_status, "CONSUMED_V551_CANONICAL_PROJECTION")
        self.assertEqual(b.scale_encoding_status, "CONSUMED_V551_CANONICAL_PROJECTION")

    def test_invalid_or_missing_v551_canonical_projection_fails_closed_in_v552(self):
        missing = v552.resolve_v552_signed_component({"response_direction": "positive", "response_intensity": 1.0})
        invalid = v552.resolve_v552_signed_component({"v551_signed_side": "neutral", "v551_signed_intensity": 0.5})
        self.assertIsNone(missing.canonical_signed_component)
        self.assertTrue(missing.scale_encoding_status.startswith("BLOCKED"))
        self.assertIsNone(invalid.canonical_signed_component)
        self.assertTrue(invalid.scale_encoding_status.startswith("BLOCKED"))


if __name__ == "__main__":
    unittest.main()
