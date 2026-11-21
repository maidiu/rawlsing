"""Tests for the sourcefree O-INDEX validator."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_index import ValidationError, validate
from verify_source_manifest import verify as verify_git_source_manifest

ROOT = Path(__file__).resolve().parent


class ValidatorTests(unittest.TestCase):

    def test_forged_non_s_source_path_and_consumer_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            path = target / "01_SOURCE_OF_TRUTH_REGISTRY.json"
            registry = json.loads(path.read_text(encoding="utf-8"))
            row = next(item for item in registry["rows"] if item["id"] == "A5")
            row["evidence_source"]["path"] = "FORGED/NOT_A_SOURCE.py"
            row["evidence_source"]["blob"] = "1" * 40
            row["evidence_source"]["object_id"] = "1" * 40
            row["first_consumer"] = "FABRICATED_ACTUAL_CONSUMER"
            row["first_consumer_required"] = "FABRICATED_ACTUAL_CONSUMER"
            row["actual_consumer_state"] = "ACTUAL"
            row["actual_consumer_evidence"] = {
                "commit": "5fc1d43e3d5412194d1f1eaa30ff448f84635e99",
                "path": "FORGED/CONSUMER.py",
                "object_type": "blob",
                "object_id": "2" * 40,
            }
            self._rewrite(path, registry)
            with self.assertRaises(ValidationError) as error:
                validate(target)
            self.assertIn("manifest mismatch", str(error.exception))
        finally:
            temp.cleanup()

    def test_forged_source_timestamp_and_metadata_fail(self) -> None:
        temp, target = self._mutated_root()
        try:
            path = target / "01_SOURCE_OF_TRUTH_REGISTRY.json"
            registry = json.loads(path.read_text(encoding="utf-8"))
            next(item for item in registry["rows"] if item["id"] == "A5")["source_timestamp"] = "FORGED"
            self._rewrite(path, registry)
            with self.assertRaises(ValidationError) as error:
                validate(target)
            self.assertIn("source_timestamp manifest mismatch", str(error.exception))
        finally:
            temp.cleanup()
        temp, target = self._mutated_root()
        try:
            path = target / "01_SOURCE_OF_TRUTH_REGISTRY.json"
            registry = json.loads(path.read_text(encoding="utf-8"))
            commit = next(item for item in registry["rows"] if item["id"] == "A5")["evidence_source"]["commit"]
            registry["source_cut_metadata"][commit]["timestamp"] = "FORGED"
            self._rewrite(path, registry)
            with self.assertRaises(ValidationError) as error:
                validate(target)
            self.assertIn("source metadata timestamp manifest mismatch", str(error.exception))
        finally:
            temp.cleanup()

    def test_forged_pyat_source_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            path = target / "01_SOURCE_OF_TRUTH_REGISTRY.json"
            registry = json.loads(path.read_text(encoding="utf-8"))
            row = next(item for item in registry["pyat_namespace"]["rows"] if item["id"] == "PYAT_N11")
            row["source"]["path"] = "FORGED/PYAT.py"
            row["source"]["blob"] = "2" * 40
            row["source"]["object_id"] = "2" * 40
            self._rewrite(path, registry)
            with self.assertRaises(ValidationError) as error:
                validate(target)
            self.assertIn("manifest mismatch", str(error.exception))
        finally:
            temp.cleanup()

    def test_damaged_lineage_sources_fail(self) -> None:
        cases = {
            "B1": ("blob", None),
            "B3A": ("path", "candidate/integration.py"),
            "B3AS": ("path", "candidate/integration.py"),
            "S39_S52": ("path", "s52/session.py"),
        }
        for sid, (field, value) in cases.items():
            with self.subTest(source=sid):
                temp, target = self._mutated_root()
                try:
                    path = target / "01_SOURCE_OF_TRUTH_REGISTRY.json"
                    registry = json.loads(path.read_text(encoding="utf-8"))
                    next(item for item in registry["rows"]
                         if item["id"] == sid)["evidence_source"][field] = value
                    self._rewrite(path, registry)
                    with self.assertRaises(ValidationError) as error:
                        validate(target)
                    self.assertIn("manifest mismatch", str(error.exception))
                finally:
                    temp.cleanup()

    def test_r15_tree_as_file_blob_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            path = target / "01_SOURCE_OF_TRUTH_REGISTRY.json"
            registry = json.loads(path.read_text(encoding="utf-8"))
            row = next(item for item in registry["rows"] if item["id"] == "R15_V2")
            row["evidence_source"]["object_type"] = "blob"
            row["evidence_source"]["object_id"] = "1" * 40
            row["evidence_source"]["blob"] = "1" * 40
            self._rewrite(path, registry)
            with self.assertRaises(ValidationError) as error:
                validate(target)
            self.assertIn("object_type manifest mismatch", str(error.exception))
        finally:
            temp.cleanup()

    def test_actual_consumer_without_evidence_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            path = target / "01_SOURCE_OF_TRUTH_REGISTRY.json"
            registry = json.loads(path.read_text(encoding="utf-8"))
            row = next(item for item in registry["rows"] if item["id"] == "A5")
            row["actual_consumer_state"] = "ACTUAL"
            row["actual_consumer_evidence"] = None
            self._rewrite(path, registry)
            with self.assertRaises(ValidationError) as error:
                validate(target)
            self.assertIn("ACTUAL consumer lacks source evidence", str(error.exception))
        finally:
            temp.cleanup()

    def test_manifest_digest_mutation_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            path = target / "source_manifest.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["manifest_digest"] = "0" * 64
            self._rewrite(path, manifest)
            with self.assertRaises(ValidationError) as error:
                validate(target)
            self.assertIn("manifest digest mismatch", str(error.exception))
        finally:
            temp.cleanup()

    def test_missing_product_link_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            path = target / "01_SOURCE_OF_TRUTH_REGISTRY.json"
            registry = json.loads(path.read_text(encoding="utf-8"))
            next(item for item in registry["rows"] if item["id"] == "S5").pop("product_link", None)
            self._rewrite(path, registry)
            with self.assertRaises(ValidationError) as error:
                validate(target)
            self.assertIn("S5: missing product link", str(error.exception))
        finally:
            temp.cleanup()

    def test_generic_only_product_path_fails(self) -> None:
        temp, target = self._mutated_root()
        try:
            path = target / "02_L0_L5_LINKED_ORCHESTRATION_INDEX.json"
            index = json.loads(path.read_text(encoding="utf-8"))
            index["edges"] = [edge for edge in index["edges"]
                              if not (edge["from"] == "L1_S5_FLOURISHING" and edge["to"] == "S5")]
            self._rewrite(path, index)
            with self.assertRaises(ValidationError) as error:
                validate(target)
            self.assertIn("missing product path", str(error.exception))
        finally:
            temp.cleanup()

    def test_missing_owner_native_and_n11_collision_fail(self) -> None:
        temp, target = self._mutated_root()
        try:
            path = target / "01_SOURCE_OF_TRUTH_REGISTRY.json"
            registry = json.loads(path.read_text(encoding="utf-8"))
            next(item for item in registry["rows"] if item["id"] == "A5")["owner"] = ""
            self._rewrite(path, registry)
            with self.assertRaises(ValidationError) as error:
                validate(target)
            self.assertIn("A5: missing owner", str(error.exception))
        finally:
            temp.cleanup()
        temp, target = self._mutated_root()
        try:
            path = target / "01_SOURCE_OF_TRUTH_REGISTRY.json"
            registry = json.loads(path.read_text(encoding="utf-8"))
            next(item for item in registry["pyat_namespace"]["rows"] if item["id"] == "PYAT_N11")["id"] = "S5"
            self._rewrite(path, registry)
            with self.assertRaises(ValidationError) as error:
                validate(target)
            self.assertIn("Pyat N0-N12/F1-F8 id set", str(error.exception))
        finally:
            temp.cleanup()

    def test_restored_candidate_returns_green(self) -> None:
        report = validate(ROOT)
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(report["counts"]["owner_slots"], 46)
        self.assertEqual(report["counts"]["edges"], 461)

    def test_refresh_verifier_rejects_forged_manifest_blob(self) -> None:
        temp, target = self._mutated_root()
        try:
            path = target / "source_manifest.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            next(item for item in manifest["rows"]
                 if item["namespace"] == "SOROK" and item["id"] == "A5")["object_id"] = "1" * 40
            self._rewrite(path, manifest)
            report = verify_git_source_manifest(target, ROOT.parents[2])
            self.assertEqual(report["result"], "FAIL")
            self.assertTrue(any("object_id" in error for error in report["errors"]))
        finally:
            temp.cleanup()

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
