"""Tests for the RRIF sourcefree validator."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_rrif import ValidationError, validate

ROOT = Path(__file__).resolve().parent.parent


class ValidatorTests(unittest.TestCase):
    def test_baseline_passes(self) -> None:
        report = validate(ROOT)
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(report["counts"]["families"], 1885)
        self.assertEqual(report["counts"]["function_ids"], 3135)
        self.assertEqual(report["counts"]["negative_records"], 2595)
        self.assertEqual(report["counts"]["six_boundary_families"], 11)

    def _mutated_root(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        target = Path(temp.name)
        for name in (
            "ALL_1885_FAMILY_DISPOSITIONS.jsonl",
            "HISTORICAL_NEGATIVES_AND_ANTI_REBUILD.jsonl",
            "FUNCTION_ID_CUSTODY.jsonl",
            "BRANCH_ROSTER_845.json",
            "CONSEQUENTIALLY_JUSTIFIED_FANIN_MANIFEST.json",
            "LEDGER_BUILD_SUMMARY.json",
            "POST_S7FIX_RETURN_NEGATIVES.jsonl",
        ):
            shutil.copy2(ROOT / name, target / name)
        return temp, target

    def _read(self, target: Path, name: str) -> list[dict]:
        return [json.loads(line) for line in (target / name).read_text(encoding="utf-8").splitlines() if line]

    def _write(self, target: Path, name: str, rows: list[dict]) -> None:
        (target / name).write_text("".join(json.dumps(row, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8")

    def test_missing_family_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            rows = self._read(target, "ALL_1885_FAMILY_DISPOSITIONS.jsonl")
            rows.pop()
            self._write(target, "ALL_1885_FAMILY_DISPOSITIONS.jsonl", rows)
            with self.assertRaises(ValidationError):
                validate(target)
        finally:
            temp.cleanup()

    def test_duplicate_function_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            rows = self._read(target, "FUNCTION_ID_CUSTODY.jsonl")
            rows[1]["function_id"] = rows[0]["function_id"]
            self._write(target, "FUNCTION_ID_CUSTODY.jsonl", rows)
            with self.assertRaises(ValidationError):
                validate(target)
        finally:
            temp.cleanup()

    def test_native_promotion_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            rows = self._read(target, "ALL_1885_FAMILY_DISPOSITIONS.jsonl")
            rows[0]["grades"]["native_product_accepted"] = True
            self._write(target, "ALL_1885_FAMILY_DISPOSITIONS.jsonl", rows)
            with self.assertRaises(ValidationError):
                validate(target)
        finally:
            temp.cleanup()

    def test_nested_boundary_promotion_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            rows = self._read(target, "ALL_1885_FAMILY_DISPOSITIONS.jsonl")
            row = next(item for item in rows if item["family_id"] == "S7FAM-3ced5b9ab5b98431")
            row["disposition"]["status"] = "ALREADY_CURRENT"
            row["disposition"]["decision"] = "PRESERVE_HISTORICAL"
            self._write(target, "ALL_1885_FAMILY_DISPOSITIONS.jsonl", rows)
            with self.assertRaises(ValidationError):
                validate(target)
        finally:
            temp.cleanup()

    def test_dropped_negative_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            rows = self._read(target, "HISTORICAL_NEGATIVES_AND_ANTI_REBUILD.jsonl")
            rows.pop()
            self._write(target, "HISTORICAL_NEGATIVES_AND_ANTI_REBUILD.jsonl", rows)
            with self.assertRaises(ValidationError):
                validate(target)
        finally:
            temp.cleanup()

    def test_false_receiver_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            rows = self._read(target, "ALL_1885_FAMILY_DISPOSITIONS.jsonl")
            rows[0]["current"]["production_receiver_verified"] = True
            self._write(target, "ALL_1885_FAMILY_DISPOSITIONS.jsonl", rows)
            with self.assertRaises(ValidationError):
                validate(target)
        finally:
            temp.cleanup()


if __name__ == "__main__":
    unittest.main()
