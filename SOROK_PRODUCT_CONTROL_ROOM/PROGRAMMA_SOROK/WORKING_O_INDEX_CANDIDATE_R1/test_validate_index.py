"""Tests for the sourcefree O-INDEX validator."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_index import ValidationError, validate

ROOT = Path(__file__).resolve().parent


class ValidatorTests(unittest.TestCase):
    def test_candidate_passes(self) -> None:
        report = validate(ROOT)
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(report["counts"]["sorok_rows"], 144)
        self.assertEqual(report["counts"]["pyat_rows"], 23)
        self.assertEqual(report["counts"]["priority_decisions_made"], 0)

    def _mutated_root(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        target = Path(temp.name)
        for item in ROOT.iterdir():
            if item.is_file():
                shutil.copy2(item, target / item.name)
        return temp, target

    def _rewrite(self, path: Path, value: dict) -> None:
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def test_dropped_s16_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            registry_path = target / "01_SOURCE_OF_TRUTH_REGISTRY.json"
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            registry["rows"] = [row for row in registry["rows"] if row["id"] != "S16"]
            self._rewrite(registry_path, registry)
            with self.assertRaises(ValidationError):
                validate(target)
        finally:
            temp.cleanup()

    def test_original_workstream_source_removed_fails(self) -> None:
        """Source-presence must be proven, not just 17 S IDs or a hardcoded 0/17."""
        temp, target = self._mutated_root()
        try:
            registry_path = target / "01_SOURCE_OF_TRUTH_REGISTRY.json"
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            original = next(row for row in registry["rows"] if row["id"] == "S0")
            original["evidence_source"] = None
            self._rewrite(registry_path, registry)
            with self.assertRaises(ValidationError):
                validate(target)
        finally:
            temp.cleanup()

    def test_original_workstream_wrong_blob_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            registry_path = target / "01_SOURCE_OF_TRUTH_REGISTRY.json"
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            original = next(row for row in registry["rows"] if row["id"] == "S16")
            original["evidence_source"]["blob"] = "0" * 40
            self._rewrite(registry_path, registry)
            with self.assertRaises(ValidationError):
                validate(target)
        finally:
            temp.cleanup()

    def test_native_promotion_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            registry_path = target / "01_SOURCE_OF_TRUTH_REGISTRY.json"
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            next(row for row in registry["rows"] if row["id"] == "A5")["native_product_accepted"] = True
            self._rewrite(registry_path, registry)
            with self.assertRaises(ValidationError):
                validate(target)
        finally:
            temp.cleanup()

    def test_orphan_l3_function_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            index_path = target / "02_L0_L5_LINKED_ORCHESTRATION_INDEX.json"
            index = json.loads(index_path.read_text(encoding="utf-8"))
            index["edges"] = [edge for edge in index["edges"] if edge["from"] != "M01"]
            self._rewrite(index_path, index)
            with self.assertRaises(ValidationError):
                validate(target)
        finally:
            temp.cleanup()

    def test_missing_pyat_n11_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            registry_path = target / "01_SOURCE_OF_TRUTH_REGISTRY.json"
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            namespace = registry["pyat_namespace"]
            namespace["rows"] = [row for row in namespace["rows"] if row["id"] != "PYAT_N11"]
            self._rewrite(registry_path, registry)
            with self.assertRaises(ValidationError):
                validate(target)
        finally:
            temp.cleanup()

    def test_untyped_cycle_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            index_path = target / "02_L0_L5_LINKED_ORCHESTRATION_INDEX.json"
            index = json.loads(index_path.read_text(encoding="utf-8"))
            index["edges"].append({"from": "M01", "to": "M01", "relation": "untyped_cycle", "status": "BAD", "hq_judgment_required": True})
            self._rewrite(index_path, index)
            with self.assertRaises(ValidationError):
                validate(target)
        finally:
            temp.cleanup()

    def test_priority_decision_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            slots_path = target / "04_UNDECIDED_SCIENCE_DEPENDENCY_AND_OWNER_SLOTS.json"
            slots = json.loads(slots_path.read_text(encoding="utf-8"))
            slots["counts"]["priority_decisions_made"] = 1
            self._rewrite(slots_path, slots)
            with self.assertRaises(ValidationError):
                validate(target)
        finally:
            temp.cleanup()


if __name__ == "__main__":
    unittest.main()
