"""Mutation tests for the RRIF custody validator."""
from __future__ import annotations
import json, shutil, tempfile, unittest
from pathlib import Path
from validate_custody import ValidationError, validate

ROOT = Path(__file__).resolve().parent.parent
FILES = [
    "BRANCH_LOCATION_SUMMARY.jsonl", "CODE_LOCATION_LEDGER.jsonl",
    "UNCERTAIN_OR_MISSING_CODE.jsonl", "EXACT_CURRENT_SUBTRACTION.json",
    "BRANCH_IDENTITY_CUSTODY.json", "INTEGRATION_RECEIVER_MAP.json",
    "COUNTEREXAMPLE_AUDIT.json", "BRANCH_LOCATION_COUNTS.json",
    "CODE_LOCATION_COUNTS.json",
]

class Tests(unittest.TestCase):
    def test_baseline(self):
        r = validate(ROOT); self.assertEqual(r["result"], "PASS")
        self.assertEqual(r["counts"]["branch_names"], 845)
        self.assertEqual(r["counts"]["functions"], 3135)

    def _copy(self):
        t = tempfile.TemporaryDirectory(); d = Path(t.name)
        for f in FILES: shutil.copy2(ROOT / f, d / f)
        return t, d

    def _jsonl(self, d, name):
        return [json.loads(x) for x in (d / name).read_text().splitlines() if x]

    def _write(self, d, name, rows):
        (d / name).write_text("".join(json.dumps(x, separators=(",", ":")) + "\n" for x in rows))

    def test_dropped_branch_fails(self):
        t, d = self._copy()
        try:
            rows = self._jsonl(d, "BRANCH_LOCATION_SUMMARY.jsonl"); rows.pop(); self._write(d, "BRANCH_LOCATION_SUMMARY.jsonl", rows)
            with self.assertRaises(ValidationError): validate(d)
        finally: t.cleanup()

    def test_duplicate_function_fails(self):
        t, d = self._copy()
        try:
            rows = self._jsonl(d, "CODE_LOCATION_LEDGER.jsonl"); rows[1]["function_id"] = rows[0]["function_id"]; self._write(d, "CODE_LOCATION_LEDGER.jsonl", rows)
            with self.assertRaises(ValidationError): validate(d)
        finally: t.cleanup()

    def test_wrong_current_blob_fails(self):
        t, d = self._copy()
        try:
            rows = self._jsonl(d, "CODE_LOCATION_LEDGER.jsonl")
            row = next(x for x in rows if x["current_path"] and x["current_blob"])
            row["current_blob"] = "0" * 40; self._write(d, "CODE_LOCATION_LEDGER.jsonl", rows)
            with self.assertRaises(ValidationError): validate(d)
        finally: t.cleanup()

    def test_semantic_equivalence_claim_fails(self):
        t, d = self._copy()
        try:
            rows = self._jsonl(d, "CODE_LOCATION_LEDGER.jsonl"); rows[0]["semantic_equivalence"] = True; self._write(d, "CODE_LOCATION_LEDGER.jsonl", rows)
            with self.assertRaises(ValidationError): validate(d)
        finally: t.cleanup()

    def test_dropped_subtraction_fails(self):
        t, d = self._copy()
        try:
            data = json.loads((d / "EXACT_CURRENT_SUBTRACTION.json").read_text()); data["functions"].pop(); (d / "EXACT_CURRENT_SUBTRACTION.json").write_text(json.dumps(data))
            with self.assertRaises(ValidationError): validate(d)
        finally: t.cleanup()

    def test_wrong_custody_tip_fails(self):
        t, d = self._copy()
        try:
            data = json.loads((d / "BRANCH_IDENTITY_CUSTODY.json").read_text()); data["branches"][0]["tip"] = "0" * 40; (d / "BRANCH_IDENTITY_CUSTODY.json").write_text(json.dumps(data))
            with self.assertRaises(ValidationError): validate(d)
        finally: t.cleanup()

if __name__ == "__main__":
    unittest.main()
