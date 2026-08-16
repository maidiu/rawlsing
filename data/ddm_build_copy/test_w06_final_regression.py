from __future__ import annotations

import ast
import csv
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "data" / "ddm_build_copy"

from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    PIPELINE_BOUNDARY_CONTRACT_VERSION,
    BoundaryContractError,
    boundary_state_from_payload,
    load_closed_35_waves,
)
from data.ddm_build_copy.ddm_v550_question_relation_authority import DEFAULT_AUTHORITY_PATH
from data.ddm_build_copy.ddm_v552j_handoff import build_v552j_join


def _function_source(path: Path, name: str) -> str:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return "\n".join(lines[node.lineno - 1 : node.end_lineno])
    raise AssertionError(f"missing function {name} in {path}")


def _state(evidence: str = "PRESENT", permission: str = "ALLOW") -> dict[str, str]:
    return {
        "run_integrity_status": "PASS",
        "evidence_status": evidence,
        "downstream_permission_status": permission,
    }

EVS_1999_IS_SEMANTICS = {
    "v108": {"relation_axis_id": "religious_ceremony_importance", "target_entity_id": "marriage", "driver_facet_id": "ritual_religiosity"},
    "v213": {"relation_axis_id": "democratic_system_satisfaction", "target_entity_id": "current_democracy", "driver_facet_id": "democracy_supply_demand"},
}


def _evs_packet(packet_id: str, question_id: str, *, review: bool = False) -> dict[str, object]:
    semantic = EVS_1999_IS_SEMANTICS[question_id]
    return {
        "run_id": "evs-1999-is-canary",
        "packet_id": packet_id,
        "source": "EVS",
        "source_family": "EVS",
        "wave": "1999",
        "canonical_wave": "1999",
        "country_code": "IS",
        "relation_axis_ids_json": f'["{semantic["relation_axis_id"]}"]',
        "target_entity_ids_json": f'["{semantic["target_entity_id"]}"]',
        "driver_facet_ids_json": f'["{semantic["driver_facet_id"]}"]',
        "question_ids_json": f'["{question_id}"]',
        "certification_status": "REVIEW_REQUIRED_AUTHORITY_GAP" if review else "CERTIFIED_JOINT_RELATION_EVIDENCE",
        "joint_support_status": "underpowered" if review else "sufficient_support",
        "joint_directionality_authority_status": "REVIEW_REQUIRED" if review else "CERTIFIED",
        "joint_evidence_authority_status": "REVIEW_REQUIRED" if review else "CERTIFIED",
        "review_required": review,
    }


def _evs_fact(fact_id: str, question_id: str, *, pressure: float = 0.25, status: str = "OBSERVED_NONZERO", source: str = "EVS") -> dict[str, object]:
    semantic = EVS_1999_IS_SEMANTICS[question_id]
    return {
        "run_id": "evs-1999-is-canary",
        "source": source,
        "source_family": source,
        "wave": "1999",
        "canonical_wave": "1999",
        "country_code": "IS",
        "v552_structural_fact_id": fact_id,
        "source_artifact": "v552_pressure_observation_index",
        "source_row_index": 0,
        "source_row_id": f"obs-{fact_id}",
        "relation_axis_id": semantic["relation_axis_id"],
        "target_entity_id": semantic["target_entity_id"],
        "driver_facet_id": semantic["driver_facet_id"],
        "question_id": question_id,
        "structural_channel_id": "evs_1999_is",
        "horizon_constraint_id": "",
        "semantic_signature": f"EVS|1999|IS|{question_id}",
        "structural_fact_lane": "primary_pressure",
        "structural_fact_grain": "empirical_distribution_pressure_observation",
        "structural_fact_status": "PRESENT" if status.startswith("OBSERVED") else status,
        "pressure_score": pressure,
        "pressure_score_status": status,
        "measurement_evidence_status": "PRESENT" if status.startswith("OBSERVED") else status,
        "downstream_permission_status": "ALLOW" if status.startswith("OBSERVED") else "DENY",
        "schema_version": "v3.0",
        "compiler_version": "v3.0",
    }


class TestW06C_EVS1999IcelandCanary(unittest.TestCase):
    def test_governed_authority_contains_evs_1999_iceland_rows(self) -> None:
        self.assertTrue(DEFAULT_AUTHORITY_PATH.exists(), f"governed authority missing: {DEFAULT_AUTHORITY_PATH}")
        with DEFAULT_AUTHORITY_PATH.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        iceland = [
            row for row in rows
            if str(row.get("source_family", "")).strip() == "EVS"
            and str(row.get("canonical_wave", "")).strip() == "1999"
            and str(row.get("country_code_scope", row.get("country_code", ""))).strip() == "IS"
        ]
        self.assertGreater(len(iceland), 0)
        variables = {str(row.get("var_code", "")).strip() for row in iceland}
        self.assertTrue({"v108", "v213"}.issubset(variables), variables)

    def test_true_joint_and_low_support_review_survive_exact_scope_v552j_join(self) -> None:
        certified = pd.DataFrame([_evs_packet("evs-is-certified", "v108")])
        review = pd.DataFrame([_evs_packet("evs-is-review-low-support", "v213", review=True)])
        facts = pd.DataFrame([
            _evs_fact("fact-v108", "v108", pressure=0.33),
            _evs_fact("fact-v213", "v213", pressure=0.0, status="OBSERVED_ZERO"),
            _evs_fact("wrong-source-strong", "v108", pressure=0.99, source="OTHER"),
        ])
        result = build_v552j_join(
            run_id="evs-1999-is-canary",
            v551j_certified=certified,
            v551j_review=review,
            v552_structural_facts=facts,
            v551j_state=_state(),
            v552_state=_state(),
        )
        joined = result["join_index"]
        self.assertEqual(set(joined["packet_id"]), {"evs-is-certified", "evs-is-review-low-support"})
        permissions = dict(zip(joined["packet_id"], joined["join_permission"]))
        self.assertEqual(permissions["evs-is-certified"], "ALLOW")
        self.assertEqual(permissions["evs-is-review-low-support"], "REVIEW_ONLY")
        self.assertEqual(result["metrics"]["constraint_count"], 1)
        self.assertEqual(result["metrics"]["review_context_count"], 1)
        selected = dict(zip(joined["packet_id"], joined["v552_structural_fact_id"]))
        self.assertEqual(selected["evs-is-certified"], "fact-v108")
        self.assertEqual(selected["evs-is-review-low-support"], "fact-v213")
        review_row = joined.loc[joined["packet_id"].eq("evs-is-review-low-support")].iloc[0]
        self.assertTrue(bool(review_row["observed_zero"]))
        self.assertEqual(review_row["repair_debt_status"], "REVIEW_REQUIRED")


class TestW06CClosed35Waves(unittest.TestCase):
    def test_governed_closed_35_waves_exact_scope(self) -> None:
        waves = load_closed_35_waves(DEFAULT_AUTHORITY_PATH)
        self.assertEqual(len(waves), 35)
        self.assertIn(("EVS", "1999", ""), waves)
        self.assertNotIn(("Asian Barometer", "W6", ""), waves)

    def test_zero_cardinality_does_not_redefine_typed_boundary_state(self) -> None:
        cases = [
            ("PRESENT", "ALLOW"),
            ("VALID_EMPTY", "NOT_APPLICABLE"),
            ("NOT_APPLICABLE", "NOT_APPLICABLE"),
            ("APPLICABLE_UNRESOLVED", "DENY"),
        ]
        for evidence, permission in cases:
            with self.subTest(evidence=evidence, permission=permission):
                state = boundary_state_from_payload({
                    "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
                    "run_integrity_status": "PASS",
                    "evidence_status": evidence,
                    "downstream_permission_status": permission,
                    "row_count": 0,
                    "atom_count": 0,
                    "candidate_count": 0,
                })
                self.assertEqual(state.run_integrity_status, "PASS")
                self.assertEqual(state.evidence_status, evidence)
                self.assertEqual(state.downstream_permission_status, permission)

    def test_unknown_typed_state_fails_closed(self) -> None:
        with self.assertRaises(BoundaryContractError):
            boundary_state_from_payload({
                "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
                "run_integrity_status": "PASS",
                "evidence_status": "UNKNOWN_READY",
                "downstream_permission_status": "ALLOW",
            })

    def test_all_four_repaired_stages_publish_typed_state_fields(self) -> None:
        for name in (
            "compile_v551_relation_evidence_atoms.py",
            "compile_v551j_joint_evidence_packets.py",
            "compile_v552_structural_ddm.py",
            "compile_v552j_structural_handoff.py",
        ):
            source = (BUILD / name).read_text(encoding="utf-8")
            with self.subTest(name=name):
                self.assertIn("run_integrity_status", source)
                self.assertIn("evidence_status", source)
                self.assertIn("downstream_permission_status", source)


class TestW06CDeferredContainment(unittest.TestCase):
    def test_watch_001_v553_probe_zero_cannot_become_authority(self) -> None:
        body = _function_source(BUILD / "ddm_v553_temporal_pressure.py", "_build_v553_temporal_pressure_field_contract")
        self.assertIn('authorized_structural_pressure_value is not None', body)
        self.assertIn('allowed_downstream_use = bool(temporal_status == "observed_authorized_anchor"', body)
        self.assertIn('authorized_structural_pressure_value = None', body)
        self.assertIn('pressure_value_kind = "gap"', body)
        self.assertNotIn('pressure_value == 0', body)

    def test_watch_002_v554_missing_point_estimate_remains_blocker_only(self) -> None:
        body = _function_source(BUILD / "ddm_v554_seed_contract.py", "_build_seed_affordance_index")
        permission = _function_source(BUILD / "ddm_v554_seed_contract.py", "_seed_permission")
        self.assertIn('pressure_distribution.get("point_estimate", 0.0)', body)
        self.assertIn('readiness = "blocker_only"', body)
        self.assertIn('if seed_readiness_status == "blocker_only":', permission)
        self.assertIn('return "blocker_only"', permission)
        self.assertNotIn('if pressure_value == 0', body)

    def test_watch_006_thin_numeric_defaults_are_diagnostic_not_runtime_authority(self) -> None:
        report_score = _function_source(BUILD / "ddm_v5_thin_end_to_end.py", "_report_score")
        status = _function_source(BUILD / "ddm_v5_thin_end_to_end.py", "_status_for")
        summary = _function_source(BUILD / "ddm_v5_thin_end_to_end.py", "_summarize_readiness_report")
        whole = (BUILD / "ddm_v5_thin_end_to_end.py").read_text(encoding="utf-8")
        self.assertIn('report.get(key, 0.0)', report_score)
        self.assertNotIn("score", status)
        self.assertIn('"ready_for_runtime_consumption": False', whole)
        self.assertIn('incorrectly marked runtime-ready', whole)
        self.assertNotIn('downstream_permission_status == "ALLOW"', report_score)
        self.assertNotIn('run_integrity_status == "PASS"', report_score)
        self.assertIn('if key.endswith("_score")', summary)

    def test_downstream_absence_unresolved_and_true_zero_remain_distinct_in_v552j(self) -> None:
        empty = build_v552j_join(
            run_id="evs-1999-is-canary",
            v551j_certified=pd.DataFrame(),
            v551j_review=pd.DataFrame(),
            v552_structural_facts=pd.DataFrame(),
            v551j_state=_state("NOT_APPLICABLE", "NOT_APPLICABLE"),
            v552_state=_state("NOT_APPLICABLE", "NOT_APPLICABLE"),
        )
        self.assertEqual(empty["state"]["evidence_status"], "NOT_APPLICABLE")
        self.assertEqual(empty["metrics"]["constraint_count"], 0)
        self.assertIsNone(empty["metrics"]["mean_readiness_score"])

        unresolved = build_v552j_join(
            run_id="evs-1999-is-canary",
            v551j_certified=pd.DataFrame([_evs_packet("u", "v108")]),
            v551j_review=pd.DataFrame(),
            v552_structural_facts=pd.DataFrame([_evs_fact("uf", "v108", pressure=float("nan"), status="APPLICABLE_BUT_UNRESOLVED")]),
            v551j_state=_state(),
            v552_state=_state("APPLICABLE_UNRESOLVED", "DENY"),
        )
        self.assertEqual(unresolved["state"]["evidence_status"], "APPLICABLE_UNRESOLVED")
        self.assertEqual(unresolved["metrics"]["observed_zero_count"], 0)

        zero = build_v552j_join(
            run_id="evs-1999-is-canary",
            v551j_certified=pd.DataFrame([_evs_packet("z", "v108")]),
            v551j_review=pd.DataFrame(),
            v552_structural_facts=pd.DataFrame([_evs_fact("zf", "v108", pressure=0.0, status="OBSERVED_ZERO")]),
            v551j_state=_state(),
            v552_state=_state(),
        )
        self.assertEqual(zero["state"]["evidence_status"], "PRESENT")
        self.assertEqual(zero["metrics"]["observed_zero_count"], 1)
        self.assertEqual(zero["join_index"].iloc[0]["pressure_score"], 0.0)


class TestW06CCrossStageNegativeControls(unittest.TestCase):
    def test_v552j_producer_compiler_contains_fail_closed_controls(self) -> None:
        source = (BUILD / "compile_v552j_structural_handoff.py").read_text(encoding="utf-8")
        for token in (
            "ARTIFACT_FILE_SHA256_MISMATCH",
            "RUN_INTEGRITY_NOT_PASS",
            "SCHEMA_VERSION_MISMATCH",
            "COMPILER_VERSION_MISMATCH",
            "CROSS_RUN_MISMATCH",
            "CROSS_SCOPE_MISMATCH",
            "publish_staged_directory",
            "validate_machine_output_policy",
        ):
            with self.subTest(token=token):
                self.assertIn(token, source)

    def test_exact_scope_match_precedes_semantic_score(self) -> None:
        source = (BUILD / "ddm_v552j_handoff.py").read_text(encoding="utf-8")
        match = _function_source(BUILD / "ddm_v552j_handoff.py", "_structural_fact_match_score")
        self.assertIn("if not _same_scope(packet_row,fact_row):return -1", match.replace("\n", ""))
        self.assertIn("_same_scope", source)


if __name__ == "__main__":
    unittest.main()
