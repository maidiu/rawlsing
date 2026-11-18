#!/usr/bin/env python3
"""No-body checks for the witness runner's preflight guard functions."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import witness_runner as w


class RunnerTests(unittest.TestCase):
    def test_wrong_root_refused(self):
        with self.assertRaises(w.PreflightRefusal) as ctx:
            w.verify_roots("actual", "expected", label="reopen")
        self.assertEqual(ctx.exception.code, "WRONG_ROOT_REOPEN")

    def test_wrong_accounting_refused(self):
        class Stats: source_rows=7337
        with self.assertRaises(w.PreflightRefusal) as ctx:
            w.verify_accounting({"RespondentEvent": 0, "EmpiricalCoordinateFact": 22011}, Stats())
        self.assertEqual(ctx.exception.code, "ACCOUNTING_MISMATCH_RespondentEvent")

    def test_source_id_is_witness_only(self):
        with self.assertRaises(w.PreflightRefusal) as ctx:
            w.preflight(candidate_tree=Path("/nonexistent"),config_path=Path("/nonexistent"),
                        config_pin=HERE/"SRC04_WITNESS_SCOPE.json",
                        binding_dir=HERE.parent/"ANVIL_ALL35_EXISTING_GRANT_ADMISSION_20261118",
                        outdir=HERE/"DRY_RUN",source_id="SRC17")
        self.assertEqual(ctx.exception.code, "WITNESS_ONLY_SRC04_IMPLEMENTED")


if __name__=="__main__":
    unittest.main(verbosity=2)
