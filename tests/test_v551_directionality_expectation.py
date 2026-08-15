import sys
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v551_directionality_expectation import (
    build_v551_directionality_expected_bridge,
    build_v551_directionality_stamp_audit,
    summarize_v551_directionality_stamp_coverage,
)


def base_row(**overrides):
    row = {
        "source": "gss",
        "source_family": "gss",
        "wave": "2010",
        "canonical_wave": "2010",
        "country_code": "US",
        "question_id": "q1",
        "var_code": "x1",
        "response_value_raw": "1",
        "response_value_normalized": "1",
        "response_label": "Agree",
        "source_row_hash": "row-1",
        "bridge_evidence_lane": "direct_relation_response",
        "source_table": "answer_distribution",
        "semantic_role": "RELATION_EVIDENCE",
        "question_use_contract_joined": True,
        "current_directional_atom_eligible": True,
        "directional_certification_status": "CERTIFIED",
        "directionality_authority_status": "CERTIFIED",
        "is_substantive": True,
        "is_missing": False,
        "is_special": False,
        # Row-level stamping fields. These must NOT determine denominator
        # membership, only whether the expected row has been stamped.
        "v551_relation_evidence_eligible": False,
        "response_option_map_matched": False,
        "response_direction": "",
        "response_intensity": None,
        "usable_for_evidence": False,
        "support_status": "missing_support",
        "response_semantics_status": "",
        "source_structure_fields_joined": False,
    }
    row.update(overrides)
    return row


class DirectionalityExpectationTests(unittest.TestCase):
    def test_directional_variable_missing_row_stamp_is_still_expected(self):
        frame = pd.DataFrame([base_row()])
        expected = build_v551_directionality_expected_bridge(frame)
        self.assertEqual(len(expected), 1)
        self.assertTrue(bool(expected.loc[0, "v551_directionality_expected"]))

    def test_existing_v551_eligibility_does_not_control_denominator(self):
        frame = pd.DataFrame([base_row(v551_relation_evidence_eligible=False)])
        expected = build_v551_directionality_expected_bridge(frame)
        self.assertEqual(len(expected), 1)

    def test_downstream_certification_status_does_not_redefine_authority_denominator(self):
        frame = pd.DataFrame([
            base_row(
                directional_certification_status="NOT_CERTIFIED",
                directionality_authority_status="NOT_CERTIFIED",
                question_use_contract_joined=False,
                semantic_role="STRUCTURAL_CONTEXT",
            )
        ])
        expected = build_v551_directionality_expected_bridge(frame)
        self.assertEqual(len(expected), 1)

    def test_non_directional_variable_is_not_expected(self):
        frame = pd.DataFrame([base_row(current_directional_atom_eligible=False)])
        expected = build_v551_directionality_expected_bridge(frame)
        self.assertTrue(expected.empty)

    def test_wrong_lane_special_and_missing_are_not_expected(self):
        frame = pd.DataFrame([
            base_row(bridge_evidence_lane="position_context", source_row_hash="row-2"),
            base_row(is_special=True, source_row_hash="row-3"),
            base_row(is_missing=True, source_row_hash="row-4"),
        ])
        expected = build_v551_directionality_expected_bridge(frame)
        self.assertTrue(expected.empty)

    def test_unmatched_directional_row_is_a_visible_missing_stamp(self):
        audit = build_v551_directionality_stamp_audit(pd.DataFrame([base_row()]))
        self.assertEqual(len(audit), 1)
        self.assertEqual(audit.loc[0, "directionality_stamp_status"], "MISSING_OR_INCOMPLETE_STAMP")
        reasons = audit.loc[0, "directionality_stamp_failure_reason"]
        self.assertIn("response_option_map_unmatched", reasons)
        self.assertIn("missing_certified_response_direction", reasons)
        self.assertIn("missing_response_intensity", reasons)

    def test_complete_directional_row_is_stamped(self):
        audit = build_v551_directionality_stamp_audit(
            pd.DataFrame([
                base_row(
                    response_option_map_matched=True,
                    response_direction="positive",
                    response_intensity=1.0,
                )
            ])
        )
        self.assertEqual(audit.loc[0, "directionality_stamp_status"], "STAMPED")
        self.assertEqual(audit.loc[0, "directionality_stamp_failure_reason"], "")

    def test_neutral_zero_is_a_valid_stamp(self):
        audit = build_v551_directionality_stamp_audit(
            pd.DataFrame([
                base_row(
                    response_option_map_matched=True,
                    response_direction="neutral",
                    response_intensity=0.0,
                )
            ])
        )
        self.assertEqual(audit.loc[0, "directionality_stamp_status"], "STAMPED")

    def test_non_directional_rows_do_not_enter_stamp_audit(self):
        audit = build_v551_directionality_stamp_audit(
            pd.DataFrame([base_row(current_directional_atom_eligible=False)])
        )
        self.assertTrue(audit.empty)

    def test_coverage_summary_counts_only_expected_rows(self):
        frame = pd.DataFrame([
            base_row(
                source_row_hash="row-1",
                response_option_map_matched=True,
                response_direction="positive",
                response_intensity=1.0,
            ),
            base_row(
                source_row_hash="row-2",
                response_value_normalized="2",
                response_option_map_matched=False,
                response_direction="",
                response_intensity=None,
            ),
            base_row(
                source_row_hash="row-3",
                current_directional_atom_eligible=False,
            ),
        ])
        audit = build_v551_directionality_stamp_audit(frame)
        summary = summarize_v551_directionality_stamp_coverage(audit)
        self.assertEqual(summary["directionality_expected_rows"], 2)
        self.assertEqual(summary["directionality_stamped_rows"], 1)
        self.assertEqual(summary["directionality_missing_stamp_rows"], 1)
        self.assertEqual(summary["directionality_stamp_coverage"], 0.5)
        self.assertFalse(summary["directionality_stamp_coverage_complete"])

    def test_missing_expectation_contract_column_blocks(self):
        frame = pd.DataFrame([base_row()]).drop(columns=["current_directional_atom_eligible"])
        with self.assertRaisesRegex(ValueError, "MISSING_DIRECTIONAL_EXPECTATION_CONTRACT"):
            build_v551_directionality_expected_bridge(frame)

    def test_missing_stamp_contract_column_blocks_expected_rows(self):
        frame = pd.DataFrame([base_row()]).drop(columns=["response_direction"])
        with self.assertRaisesRegex(ValueError, "MISSING_DIRECTIONAL_STAMP_CONTRACT"):
            build_v551_directionality_stamp_audit(frame)


if __name__ == "__main__":
    unittest.main()
